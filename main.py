#!/usr/bin/env python3
"""
Comprehensive Telegram Bot with Admin Commands and Moderation Features
Author: AI Assistant
Date: July 10, 2025
"""

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update
from telegram.ext import ContextTypes

from config import BOT_TOKEN, ADMIN_COMMANDS, MODERATION_COMMANDS, FUN_COMMANDS, INFO_COMMANDS
from handlers.admin import *
from handlers.moderation import *
from handlers.fun import *
from handlers.info import *
from handlers.general import *

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot."""
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        
        # General commands
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("menu", menu_command))
        
        # Admin commands
        application.add_handler(CommandHandler("ban", ban_user))
        application.add_handler(CommandHandler("unban", unban_user))
        application.add_handler(CommandHandler("kick", kick_user))
        application.add_handler(CommandHandler("promote", promote_user))
        application.add_handler(CommandHandler("demote", demote_user))
        application.add_handler(CommandHandler("pin", pin_message))
        application.add_handler(CommandHandler("unpin", unpin_message))
        application.add_handler(CommandHandler("setgrouppic", set_group_pic))
        application.add_handler(CommandHandler("settitle", set_group_title))
        application.add_handler(CommandHandler("setdescription", set_group_description))
        
        # Moderation commands
        application.add_handler(CommandHandler("mute", mute_user))
        application.add_handler(CommandHandler("unmute", unmute_user))
        application.add_handler(CommandHandler("warn", warn_user))
        application.add_handler(CommandHandler("unwarn", unwarn_user))
        application.add_handler(CommandHandler("warnings", check_warnings))
        application.add_handler(CommandHandler("del", delete_message))
        application.add_handler(CommandHandler("purge", purge_messages))
        application.add_handler(CommandHandler("lock", lock_chat))
        application.add_handler(CommandHandler("unlock", unlock_chat))
        
        # Info commands
        application.add_handler(CommandHandler("info", user_info))
        application.add_handler(CommandHandler("chatinfo", chat_info))
        application.add_handler(CommandHandler("admins", list_admins))
        application.add_handler(CommandHandler("members", member_count))
        application.add_handler(CommandHandler("id", get_id))
        application.add_handler(CommandHandler("rules", show_rules))
        application.add_handler(CommandHandler("setrules", set_rules))
        
        # Fun commands
        application.add_handler(CommandHandler("dice", roll_dice))
        application.add_handler(CommandHandler("coin", flip_coin))
        application.add_handler(CommandHandler("quote", random_quote))
        application.add_handler(CommandHandler("joke", random_joke))
        application.add_handler(CommandHandler("fact", random_fact))
        application.add_handler(CommandHandler("8ball", magic_8ball))
        application.add_handler(CommandHandler("choose", choose_option))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
        application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye_member))
        
        # Callback query handler for inline keyboards
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("🚀 Bot is starting...")
        print("🤖 Telegram Bot is running!")
        print("📊 Bot Token: " + BOT_TOKEN[:10] + "..." + BOT_TOKEN[-10:])
        
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()
