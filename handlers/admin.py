"""
Admin command handlers for the Telegram Bot
Handles ban, kick, promote, demote and other admin functions
"""

import logging
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden
from utils.decorators import admin_required, bot_admin_required
from utils.helpers import get_user_from_message, format_user_mention
from config import EMOJIS, MESSAGES

logger = logging.getLogger(__name__)

@admin_required
@bot_admin_required
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user from the group"""
    try:
        user_to_ban = await get_user_from_message(update, context)
        if not user_to_ban:
            await update.message.reply_text(
                f"{EMOJIS['error']} **User not found!**\n\n"
                f"🔍 **How to specify a user:**\n"
                f"• Reply to their message and use `/ban`\n"
                f"• Use `/ban [user_id]` with their Telegram ID\n"
                f"• Use `/ban @username` (works for admins)\n\n"
                f"💡 **Tip:** Reply method works best for all users!",
                parse_mode='Markdown'
            )
            return
            
        # Safety checks
        if user_to_ban.id == context.bot.id:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Ban Myself!**\n\n"
                f"🤖 I cannot ban myself from the group\n"
                f"💡 This is a safety feature"
            )
            return
            
        if user_to_ban.id == update.effective_user.id:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Ban Yourself!**\n\n"
                f"👤 You cannot ban yourself\n"
                f"💡 Ask another admin if needed"
            )
            return
        
        # Check if user is admin or creator
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_ban.id)
        if chat_member.status in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Ban Admin!**\n\n"
                f"👑 Cannot ban administrators or group owner\n"
                f"💡 Demote them first if necessary"
            )
            return
            
        # Ban the user
        await context.bot.ban_chat_member(update.effective_chat.id, user_to_ban.id)
        
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        await update.message.reply_text(
            f"{EMOJIS['ban']} **User Banned!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_ban)}\n"
            f"👑 **Banned by:** {format_user_mention(update.effective_user)}\n"
            f"📝 **Reason:** {reason}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_ban.id} banned from chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to ban user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in ban_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user from the group"""
    try:
        user_to_unban = await get_user_from_message(update, context)
        if not user_to_unban:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to unban!\n"
                f"Usage: `/unban @username` or user ID"
            )
            return
            
        # Unban the user
        await context.bot.unban_chat_member(update.effective_chat.id, user_to_unban.id)
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **User Unbanned!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_unban)}\n"
            f"👑 **Unbanned by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_unban.id} unbanned from chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to unban user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in unban_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kick a user from the group"""
    try:
        user_to_kick = await get_user_from_message(update, context)
        if not user_to_kick:
            await update.message.reply_text(
                f"{EMOJIS['error']} **User not found!**\n\n"
                f"🔍 **How to specify a user:**\n"
                f"• Reply to their message and use `/kick`\n"
                f"• Use `/kick [user_id]` with their Telegram ID\n\n"
                f"💡 **Tip:** Reply method works best!",
                parse_mode='Markdown'
            )
            return
            
        # Safety checks
        if user_to_kick.id == context.bot.id:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Kick Myself!**\n\n"
                f"🤖 I cannot kick myself from the group\n"
                f"💡 This is a safety feature"
            )
            return
            
        if user_to_kick.id == update.effective_user.id:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Kick Yourself!**\n\n"
                f"👤 You cannot kick yourself\n"
                f"💡 Ask another admin if needed"
            )
            return
        
        # Check if user is admin or creator
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_kick.id)
        if chat_member.status in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Cannot Kick Admin!**\n\n"
                f"👑 Cannot kick administrators or group owner\n"
                f"💡 Demote them first if necessary"
            )
            return
            
        # Kick the user (ban then unban)
        await context.bot.ban_chat_member(update.effective_chat.id, user_to_kick.id)
        await context.bot.unban_chat_member(update.effective_chat.id, user_to_kick.id)
        
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        
        await update.message.reply_text(
            f"{EMOJIS['kick']} **User Kicked!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_kick)}\n"
            f"👑 **Kicked by:** {format_user_mention(update.effective_user)}\n"
            f"📝 **Reason:** {reason}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_kick.id} kicked from chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to kick user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in kick_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promote a user to admin"""
    try:
        user_to_promote = await get_user_from_message(update, context)
        if not user_to_promote:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to promote!\n"
                f"Usage: `/promote @username` or reply to a message"
            )
            return
            
        # Check if user is already admin
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_promote.id)
        if chat_member.status in ['administrator', 'creator']:
            await update.message.reply_text(MESSAGES['already_admin'])
            return
            
        # Promote the user
        await context.bot.promote_chat_member(
            update.effective_chat.id,
            user_to_promote.id,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **User Promoted!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_promote)}\n"
            f"👑 **Promoted by:** {format_user_mention(update.effective_user)}\n"
            f"🔧 **Permissions:** Delete, Restrict, Pin messages\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_promote.id} promoted in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to promote user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in promote_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def demote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Demote an admin to regular member"""
    try:
        user_to_demote = await get_user_from_message(update, context)
        if not user_to_demote:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to demote!\n"
                f"Usage: `/demote @username` or reply to a message"
            )
            return
            
        # Check if user is admin
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_demote.id)
        if chat_member.status not in ['administrator']:
            await update.message.reply_text(MESSAGES['not_admin'])
            return
            
        # Demote the user
        await context.bot.promote_chat_member(
            update.effective_chat.id,
            user_to_demote.id,
            can_delete_messages=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **User Demoted!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_demote)}\n"
            f"👑 **Demoted by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_demote.id} demoted in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to demote user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in demote_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def pin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pin a message in the chat"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please reply to a message to pin it!"
            )
            return
            
        await context.bot.pin_chat_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id
        )
        
        await update.message.reply_text(
            f"{EMOJIS['pin']} **Message Pinned!**\n\n"
            f"👑 **Pinned by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Message pinned in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to pin message: {str(e)}")
    except Exception as e:
        logger.error(f"Error in pin_message: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def unpin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unpin a message in the chat"""
    try:
        if update.message.reply_to_message:
            await context.bot.unpin_chat_message(
                update.effective_chat.id,
                update.message.reply_to_message.message_id
            )
        else:
            await context.bot.unpin_all_chat_messages(update.effective_chat.id)
            
        await update.message.reply_text(
            f"{EMOJIS['success']} **Message(s) Unpinned!**\n\n"
            f"👑 **Unpinned by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Message(s) unpinned in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to unpin message: {str(e)}")
    except Exception as e:
        logger.error(f"Error in unpin_message: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def set_group_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set group profile picture"""
    try:
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please reply to a photo to set as group picture!"
            )
            return
            
        photo = update.message.reply_to_message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)
        
        await context.bot.set_chat_photo(
            update.effective_chat.id,
            photo_file.file_path
        )
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **Group Picture Updated!**\n\n"
            f"👑 **Updated by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Group picture updated in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to set group picture: {str(e)}")
    except Exception as e:
        logger.error(f"Error in set_group_pic: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def set_group_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set group title"""
    try:
        if not context.args:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please provide a new title!\n"
                f"Usage: `/settitle New Group Title`"
            )
            return
            
        new_title = ' '.join(context.args)
        await context.bot.set_chat_title(update.effective_chat.id, new_title)
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **Group Title Updated!**\n\n"
            f"📝 **New Title:** {new_title}\n"
            f"👑 **Updated by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Group title updated in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to set group title: {str(e)}")
    except Exception as e:
        logger.error(f"Error in set_group_title: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def set_group_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set group description"""
    try:
        if not context.args:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please provide a new description!\n"
                f"Usage: `/setdescription New group description`"
            )
            return
            
        new_description = ' '.join(context.args)
        await context.bot.set_chat_description(update.effective_chat.id, new_description)
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **Group Description Updated!**\n\n"
            f"📄 **New Description:** {new_description}\n"
            f"👑 **Updated by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Group description updated in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to set group description: {str(e)}")
    except Exception as e:
        logger.error(f"Error in set_group_description: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])
