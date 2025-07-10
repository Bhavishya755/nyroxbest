"""
Info command handlers for the Telegram Bot
Handles user info, chat info, admin list and other information functions
"""

import logging
import json
import os
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from utils.helpers import get_user_from_message, format_user_mention
from utils.decorators import admin_required
from config import EMOJIS

logger = logging.getLogger(__name__)

# Simple file-based storage for rules
RULES_FILE = "data/rules.json"

def load_rules():
    """Load rules from file"""
    try:
        if os.path.exists(RULES_FILE):
            with open(RULES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_rules(rules):
    """Save rules to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(RULES_FILE, 'w') as f:
            json.dump(rules, f)
    except Exception as e:
        logger.error(f"Error saving rules: {e}")

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about a user"""
    try:
        user_to_check = await get_user_from_message(update, context)
        if not user_to_check:
            user_to_check = update.effective_user
            
        # Get chat member info
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_to_check.id)
        
        # Status mapping
        status_emoji = {
            'creator': '👑',
            'administrator': '⭐',
            'member': '👤',
            'restricted': '🔇',
            'left': '❌',
            'kicked': '🚫'
        }
        
        status_text = {
            'creator': 'Owner',
            'administrator': 'Administrator', 
            'member': 'Member',
            'restricted': 'Restricted',
            'left': 'Left',
            'kicked': 'Banned'
        }
        
        info_text = f"👤 **User Information**\n\n"
        info_text += f"🆔 **ID:** `{user_to_check.id}`\n"
        info_text += f"👤 **Name:** {format_user_mention(user_to_check)}\n"
        
        if user_to_check.username:
            info_text += f"📛 **Username:** @{user_to_check.username}\n"
            
        info_text += f"{status_emoji.get(chat_member.status, '❓')} **Status:** {status_text.get(chat_member.status, 'Unknown')}\n"
        
        if user_to_check.language_code:
            info_text += f"🌍 **Language:** {user_to_check.language_code.upper()}\n"
            
        if chat_member.status == 'administrator':
            perms = []
            if hasattr(chat_member, 'can_delete_messages') and chat_member.can_delete_messages:
                perms.append("Delete Messages")
            if hasattr(chat_member, 'can_restrict_members') and chat_member.can_restrict_members:
                perms.append("Restrict Members")
            if hasattr(chat_member, 'can_promote_members') and chat_member.can_promote_members:
                perms.append("Promote Members")
            if hasattr(chat_member, 'can_pin_messages') and chat_member.can_pin_messages:
                perms.append("Pin Messages")
                
            if perms:
                info_text += f"🔧 **Permissions:** {', '.join(perms)}\n"
                
        if chat_member.status == 'restricted':
            restrictions = []
            if hasattr(chat_member, 'can_send_messages') and not chat_member.can_send_messages:
                restrictions.append("Cannot send messages")
            if hasattr(chat_member, 'can_send_media_messages') and not chat_member.can_send_media_messages:
                restrictions.append("Cannot send media")
                
            if restrictions:
                info_text += f"🚫 **Restrictions:** {', '.join(restrictions)}\n"
                
        info_text += f"\n📅 **Checked:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        await update.message.reply_text(info_text, parse_mode='Markdown')
        
        logger.info(f"User info checked for {user_to_check.id}")
        
    except BadRequest as e:
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get user info: {str(e)}")
    except Exception as e:
        logger.error(f"Error in user_info: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get user information!")

async def chat_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about the current chat"""
    try:
        chat = await context.bot.get_chat(update.effective_chat.id)
        
        chat_type_emoji = {
            'private': '👤',
            'group': '👥', 
            'supergroup': '🏢',
            'channel': '📢'
        }
        
        info_text = f"💬 **Chat Information**\n\n"
        info_text += f"🆔 **Chat ID:** `{chat.id}`\n"
        info_text += f"📝 **Title:** {chat.title or 'N/A'}\n"
        info_text += f"{chat_type_emoji.get(chat.type, '❓')} **Type:** {chat.type.title()}\n"
        
        if chat.username:
            info_text += f"📛 **Username:** @{chat.username}\n"
            
        if chat.description:
            info_text += f"📄 **Description:** {chat.description[:100]}{'...' if len(chat.description) > 100 else ''}\n"
            
        # Get member count
        try:
            member_count = await context.bot.get_chat_member_count(chat.id)
            info_text += f"👥 **Members:** {member_count:,}\n"
        except:
            pass
            
        if hasattr(chat, 'invite_link') and chat.invite_link:
            info_text += f"🔗 **Invite Link:** {chat.invite_link}\n"
            
        info_text += f"\n📅 **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        await update.message.reply_text(info_text, parse_mode='Markdown')
        
        logger.info(f"Chat info generated for chat {chat.id}")
        
    except Exception as e:
        logger.error(f"Error in chat_info: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get chat information!")

async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all administrators in the chat"""
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        
        admin_list = f"👑 **Chat Administrators**\n\n"
        
        owner = None
        administrators = []
        
        for admin in admins:
            if admin.status == 'creator':
                owner = admin
            elif admin.status == 'administrator':
                administrators.append(admin)
                
        if owner:
            admin_list += f"👑 **Owner:**\n"
            admin_list += f"   • {format_user_mention(owner.user)}\n\n"
            
        if administrators:
            admin_list += f"⭐ **Administrators:** ({len(administrators)})\n"
            for i, admin in enumerate(administrators, 1):
                admin_list += f"   {i}. {format_user_mention(admin.user)}\n"
        else:
            admin_list += f"⭐ **Administrators:** None\n"
            
        admin_list += f"\n📊 **Total:** {len(admins)} admin(s)"
        admin_list += f"\n📅 **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        await update.message.reply_text(admin_list, parse_mode='Markdown')
        
        logger.info(f"Admin list generated for chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in list_admins: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get administrator list!")

async def member_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get member count of the chat"""
    try:
        count = await context.bot.get_chat_member_count(update.effective_chat.id)
        
        await update.message.reply_text(
            f"👥 **Member Count**\n\n"
            f"📊 **Total Members:** {count:,}\n"
            f"💬 **Chat:** {update.effective_chat.title or 'This Chat'}\n"
            f"📅 **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Member count checked for chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in member_count: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get member count!")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user or chat ID"""
    try:
        user_to_check = await get_user_from_message(update, context)
        
        id_text = f"🆔 **ID Information**\n\n"
        id_text += f"💬 **Chat ID:** `{update.effective_chat.id}`\n"
        id_text += f"👤 **Your ID:** `{update.effective_user.id}`\n"
        
        if user_to_check and user_to_check.id != update.effective_user.id:
            id_text += f"👥 **Target User ID:** `{user_to_check.id}`\n"
            
        if update.message.reply_to_message:
            id_text += f"💬 **Message ID:** `{update.message.reply_to_message.message_id}`\n"
            
        await update.message.reply_text(id_text, parse_mode='Markdown')
        
        logger.info(f"ID info provided to user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in get_id: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get ID information!")

async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show group rules"""
    try:
        rules = load_rules()
        chat_id = str(update.effective_chat.id)
        
        if chat_id in rules and rules[chat_id]:
            rules_text = f"📜 **Group Rules**\n\n"
            rules_text += f"📝 {rules[chat_id]}\n\n"
            rules_text += f"⚠️ Please follow these rules to maintain a healthy community!\n"
            rules_text += f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d')}"
        else:
            rules_text = f"📜 **Group Rules**\n\n"
            rules_text += f"❌ No rules have been set for this group yet.\n"
            rules_text += f"👑 Admins can set rules using `/setrules`"
            
        await update.message.reply_text(rules_text, parse_mode='Markdown')
        
        logger.info(f"Rules displayed for chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in show_rules: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to show rules!")

@admin_required
async def set_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set group rules"""
    try:
        if not context.args:
            await update.message.reply_text(
                f"{EMOJIS['error']} Please provide the rules!\n"
                f"Usage: `/setrules Be respectful and follow community guidelines`"
            )
            return
            
        new_rules = ' '.join(context.args)
        
        rules = load_rules()
        chat_id = str(update.effective_chat.id)
        rules[chat_id] = new_rules
        save_rules(rules)
        
        await update.message.reply_text(
            f"📜 **Rules Updated!**\n\n"
            f"📝 **New Rules:** {new_rules}\n\n"
            f"👑 **Set by:** {format_user_mention(update.effective_user)}\n"
            f"📅 **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Rules updated for chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in set_rules: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to set rules!")
