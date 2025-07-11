"""
Moderation command handlers for the Telegram Bot
Handles mute, warn, delete, purge and other moderation functions
"""

import logging
import json
import os
from datetime import datetime, timezone
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from utils.decorators import admin_required, bot_admin_required
from utils.helpers import get_user_from_message, format_user_mention, parse_time, get_ist_time, format_ist_time
from config import EMOJIS, MESSAGES, MAX_WARNINGS, DEFAULT_MUTE_TIME, IST

logger = logging.getLogger(__name__)

# Simple file-based storage for warnings and mutes
WARNINGS_FILE = "data/warnings.json"
MUTES_FILE = "data/mutes.json"

def load_warnings():
    """Load warnings from file"""
    try:
        if os.path.exists(WARNINGS_FILE):
            with open(WARNINGS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_warnings(warnings):
    """Save warnings to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(WARNINGS_FILE, 'w') as f:
            json.dump(warnings, f)
    except Exception as e:
        logger.error(f"Error saving warnings: {e}")

def load_mutes():
    """Load mutes from file"""
    try:
        if os.path.exists(MUTES_FILE):
            with open(MUTES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_mutes(mutes):
    """Save mutes to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(MUTES_FILE, 'w') as f:
            json.dump(mutes, f)
    except Exception as e:
        logger.error(f"Error saving mutes: {e}")

@admin_required
@bot_admin_required
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user in the chat"""
    try:
        user_to_mute = await get_user_from_message(update, context)
        if not user_to_mute:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to mute!\n"
                f"Usage: `/mute @username [time]` or reply to a message"
            )
            return
            
        # Check if user is admin
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_mute.id)
        if chat_member.status in ['administrator', 'creator']:
            await update.message.reply_text(MESSAGES['cant_act_on_admin'])
            return
            
        # Parse mute duration
        mute_time = DEFAULT_MUTE_TIME
        time_str = "1 hour"
        
        if len(context.args) > 1:
            time_arg = context.args[1]
            parsed_time = parse_time(time_arg)
            if parsed_time:
                mute_time = parsed_time
                time_str = time_arg
                
        # Mute the user
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False
        )
        
        until_date = datetime.now() + timedelta(seconds=mute_time)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_to_mute.id,
            permissions,
            until_date=until_date
        )
        
        # Store mute info
        mutes = load_mutes()
        chat_id = str(update.effective_chat.id)
        user_id = str(user_to_mute.id)
        
        if chat_id not in mutes:
            mutes[chat_id] = {}
        mutes[chat_id][user_id] = {
            "until": until_date.isoformat(),
            "muted_by": update.effective_user.id,
            "reason": ' '.join(context.args[2:]) if len(context.args) > 2 else "No reason provided"
        }
        save_mutes(mutes)
        
        reason = mutes[chat_id][user_id]["reason"]
        
        await update.message.reply_text(
            f"{EMOJIS['mute']} **User Muted!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_mute)}\n"
            f"👑 **Muted by:** {format_user_mention(update.effective_user)}\n"
            f"⏱️ **Duration:** {time_str}\n"
            f"📝 **Reason:** {reason}\n"
            f"⏰ **Until:** {until_date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_mute.id} muted in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to mute user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in mute_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unmute a user in the chat"""
    try:
        user_to_unmute = await get_user_from_message(update, context)
        if not user_to_unmute:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to unmute!\n"
                f"Usage: `/unmute @username` or reply to a message"
            )
            return
            
        # Unmute the user (restore permissions)
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False
        )
        
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_to_unmute.id,
            permissions
        )
        
        # Remove from mutes
        mutes = load_mutes()
        chat_id = str(update.effective_chat.id)
        user_id = str(user_to_unmute.id)
        
        if chat_id in mutes and user_id in mutes[chat_id]:
            del mutes[chat_id][user_id]
            save_mutes(mutes)
        
        await update.message.reply_text(
            f"{EMOJIS['success']} **User Unmuted!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_unmute)}\n"
            f"👑 **Unmuted by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_to_unmute.id} unmuted in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to unmute user: {str(e)}")
    except Exception as e:
        logger.error(f"Error in unmute_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Warn a user"""
    try:
        user_to_warn = await get_user_from_message(update, context)
        if not user_to_warn:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to warn!\n"
                f"Usage: `/warn @username [reason]` or reply to a message"
            )
            return
            
        # Check if user is admin
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_warn.id)
        if chat_member.status in ['administrator', 'creator']:
            await update.message.reply_text(MESSAGES['cant_act_on_admin'])
            return
            
        # Add warning
        warnings = load_warnings()
        chat_id = str(update.effective_chat.id)
        user_id = str(user_to_warn.id)
        
        if chat_id not in warnings:
            warnings[chat_id] = {}
        if user_id not in warnings[chat_id]:
            warnings[chat_id][user_id] = []
            
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
        warning_data = {
            "reason": reason,
            "warned_by": update.effective_user.id,
            "date": datetime.now().isoformat()
        }
        
        warnings[chat_id][user_id].append(warning_data)
        warning_count = len(warnings[chat_id][user_id])
        save_warnings(warnings)
        
        await update.message.reply_text(
            f"{EMOJIS['warning']} **User Warned!**\n\n"
            f"👤 **User:** {format_user_mention(user_to_warn)}\n"
            f"👑 **Warned by:** {format_user_mention(update.effective_user)}\n"
            f"📝 **Reason:** {reason}\n"
            f"⚠️ **Warning:** {warning_count}/{MAX_WARNINGS}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        # Auto-action if max warnings reached
        if warning_count >= MAX_WARNINGS:
            await context.bot.ban_chat_member(update.effective_chat.id, user_to_warn.id)
            warnings[chat_id][user_id] = []  # Reset warnings
            save_warnings(warnings)
            
            await update.message.reply_text(
                f"{EMOJIS['ban']} **Auto-Ban Triggered!**\n\n"
                f"👤 **User:** {format_user_mention(user_to_warn)}\n"
                f"📊 **Reason:** Reached maximum warnings ({MAX_WARNINGS})\n"
                f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
                parse_mode='Markdown'
            )
        
        logger.info(f"User {user_to_warn.id} warned in chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in warn_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
async def unwarn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove a warning from user"""
    try:
        user_to_unwarn = await get_user_from_message(update, context)
        if not user_to_unwarn:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please specify a user to unwarn!\n"
                f"Usage: `/unwarn @username` or reply to a message"
            )
            return
            
        warnings = load_warnings()
        chat_id = str(update.effective_chat.id)
        user_id = str(user_to_unwarn.id)
        
        if chat_id in warnings and user_id in warnings[chat_id] and warnings[chat_id][user_id]:
            warnings[chat_id][user_id].pop()  # Remove last warning
            warning_count = len(warnings[chat_id][user_id])
            save_warnings(warnings)
            
            await update.message.reply_text(
                f"{EMOJIS['success']} **Warning Removed!**\n\n"
                f"👤 **User:** {format_user_mention(user_to_unwarn)}\n"
                f"👑 **Removed by:** {format_user_mention(update.effective_user)}\n"
                f"⚠️ **Warnings:** {warning_count}/{MAX_WARNINGS}\n"
                f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"{EMOJIS['info']} User has no warnings to remove."
            )
        
        logger.info(f"Warning removed from user {user_to_unwarn.id} in chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in unwarn_user: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

async def check_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check warnings for a user"""
    try:
        user_to_check = await get_user_from_message(update, context)
        if not user_to_check:
            user_to_check = update.effective_user
            
        warnings = load_warnings()
        chat_id = str(update.effective_chat.id)
        user_id = str(user_to_check.id)
        
        user_warnings = []
        if chat_id in warnings and user_id in warnings[chat_id]:
            user_warnings = warnings[chat_id][user_id]
            
        warning_count = len(user_warnings)
        
        if warning_count == 0:
            await update.message.reply_text(
                f"{EMOJIS['success']} **No Warnings**\n\n"
                f"👤 **User:** {format_user_mention(user_to_check)}\n"
                f"⚠️ **Warnings:** 0/{MAX_WARNINGS}\n"
                f"✅ **Status:** Clean record",
                parse_mode='Markdown'
            )
        else:
            warning_text = f"{EMOJIS['warning']} **Warning History**\n\n"
            warning_text += f"👤 **User:** {format_user_mention(user_to_check)}\n"
            warning_text += f"⚠️ **Warnings:** {warning_count}/{MAX_WARNINGS}\n\n"
            
            for i, warning in enumerate(user_warnings[-5:], 1):  # Show last 5 warnings
                date = datetime.fromisoformat(warning['date']).strftime('%Y-%m-%d %H:%M')
                warning_text += f"**{i}.** {warning['reason']} _{date}_\n"
                
            await update.message.reply_text(warning_text, parse_mode='Markdown')
        
        logger.info(f"Warnings checked for user {user_to_check.id} in chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in check_warnings: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a message"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please reply to a message to delete it!"
            )
            return
            
        await context.bot.delete_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id
        )
        
        # Delete the command message too
        await context.bot.delete_message(
            update.effective_chat.id,
            update.message.message_id
        )
        
        logger.info(f"Message deleted in chat {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to delete message: {str(e)}")
    except Exception as e:
        logger.error(f"Error in delete_message: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete multiple messages"""
    try:
        if not update.message.reply_to_message:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please reply to a message to start purging from!"
            )
            return
            
        start_id = update.message.reply_to_message.message_id
        end_id = update.message.message_id
        
        deleted_count = 0
        for msg_id in range(start_id, end_id + 1):
            try:
                await context.bot.delete_message(update.effective_chat.id, msg_id)
                deleted_count += 1
            except:
                continue
                
        await update.message.reply_text(
            f"{EMOJIS['success']} **Messages Purged!**\n\n"
            f"🗑️ **Deleted:** {deleted_count} messages\n"
            f"👑 **Purged by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"{deleted_count} messages purged in chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in purge_messages: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def lock_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lock chat for regular members"""
    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False
        )
        
        await context.bot.set_chat_permissions(update.effective_chat.id, permissions)
        
        await update.message.reply_text(
            f"{EMOJIS['lock']} **Chat Locked!**\n\n"
            f"🔒 **Status:** Only admins can send messages\n"
            f"👑 **Locked by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Chat locked: {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to lock chat: {str(e)}")
    except Exception as e:
        logger.error(f"Error in lock_chat: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])

@admin_required
@bot_admin_required
async def unlock_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unlock chat for regular members"""
    try:
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False
        )
        
        await context.bot.set_chat_permissions(update.effective_chat.id, permissions)
        
        await update.message.reply_text(
            f"{EMOJIS['unlock']} **Chat Unlocked!**\n\n"
            f"🔓 **Status:** Members can send messages\n"
            f"👑 **Unlocked by:** {format_user_mention(update.effective_user)}\n"
            f"⏰ **Time:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Chat unlocked: {update.effective_chat.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to unlock chat: {str(e)}")
    except Exception as e:
        logger.error(f"Error in unlock_chat: {e}")
        await update.message.reply_text(MESSAGES['action_failed'])
