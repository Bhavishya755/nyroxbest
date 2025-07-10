"""
Threaded version of the Telegram bot for use with keep_alive.py
This version properly handles asyncio in threading environment
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import all handlers
from handlers.general import (start_command, help_command, menu_command, button_callback, 
                            welcome_new_member, goodbye_member, error_handler, test_command)
from handlers.admin import (ban_user, unban_user, kick_user, promote_user, demote_user, 
                          pin_message, unpin_message, set_group_pic, set_group_title, set_group_description)
from handlers.moderation import (mute_user, unmute_user, warn_user, unwarn_user, check_warnings, 
                               delete_message, purge_messages, lock_chat, unlock_chat)
from handlers.info import (user_info, chat_info, list_admins, member_count, get_id, show_rules, set_rules)
from handlers.fun import (roll_dice, flip_coin, random_quote, random_joke, random_fact, magic_8ball, choose_option)
from handlers.utility import (translate_text, time_command, calculate_command, generate_password)
from config import BOT_TOKEN

logger = logging.getLogger(__name__)

async def main_async():
    """Async main function for the bot"""
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
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
        application.add_handler(CommandHandler("test", test_command))
        
        # Utility commands
        application.add_handler(CommandHandler("translate", translate_text))
        application.add_handler(CommandHandler("time", time_command))
        application.add_handler(CommandHandler("calc", calculate_command))
        application.add_handler(CommandHandler("password", generate_password))
        
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
        
        # Initialize and start polling
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
        # Keep the bot running
        await application.updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        print(f"❌ Error starting bot: {e}")

def run_bot_threaded():
    """Run bot in thread with proper event loop"""
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async main function
        loop.run_until_complete(main_async())
        
    except Exception as e:
        logger.error(f"❌ Bot thread error: {e}")
        print(f"❌ Bot thread error: {e}")
    finally:
        loop.close()

if __name__ == '__main__':
    run_bot_threaded()