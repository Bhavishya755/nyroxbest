"""
Decorators for the Telegram Bot
Provides admin checking, rate limiting and other useful decorators
"""

import logging
import asyncio
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from config import EMOJIS, MESSAGES

logger = logging.getLogger(__name__)

def admin_required(func):
    """Decorator to check if user is admin before executing command"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            # Skip check in private chats
            if update.effective_chat.type == 'private':
                return await func(update, context, *args, **kwargs)
                
            # Ensure we have a valid update and user
            if not update or not update.effective_user or not update.effective_chat:
                logger.error("Invalid update object in admin_required")
                return
                
            # Get user's chat member status with retry logic
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    chat_member = await context.bot.get_chat_member(
                        update.effective_chat.id, 
                        update.effective_user.id
                    )
                    break
                except BadRequest as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to get chat member after {max_retries} attempts: {e}")
                        await update.message.reply_text(
                            f"{EMOJIS['error']} **Permission Check Failed!**\n\n"
                            f"❌ Could not verify your admin status\n"
                            f"🔄 Please try the command again"
                        )
                        return
                    await asyncio.sleep(0.5)  # Brief delay before retry
            
            # Check if user is admin or creator
            if chat_member.status not in ['administrator', 'creator']:
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Admin Only Command!**\n\n"
                    f"👑 This command requires administrator privileges\n"
                    f"💡 Contact a group admin if you need assistance"
                )
                return
                
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Unexpected error in admin_required decorator: {e}")
            if update and update.message:
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Command Error!**\n\n"
                    f"⚠️ Something went wrong processing this command\n"
                    f"🔄 Please try again in a moment"
                )
    
    return wrapper

def bot_admin_required(func):
    """Decorator to check if bot has admin permissions before executing command"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            # Skip check in private chats
            if update.effective_chat.type == 'private':
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Group Command Only!**\n\n"
                    f"📱 This command only works in groups\n"
                    f"💬 Please use it in a group chat where I'm an admin"
                )
                return
                
            # Ensure we have valid objects
            if not update or not update.effective_chat or not context or not context.bot:
                logger.error("Invalid update/context in bot_admin_required")
                return
                
            # Get bot's chat member status with retry logic
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    bot_member = await context.bot.get_chat_member(
                        update.effective_chat.id, 
                        context.bot.id
                    )
                    break
                except BadRequest as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to get bot member status after {max_retries} attempts: {e}")
                        await update.message.reply_text(
                            f"{EMOJIS['error']} **Bot Status Check Failed!**\n\n"
                            f"❌ Could not verify my admin status\n"
                            f"🔄 Please try again or check my permissions"
                        )
                        return
                    await asyncio.sleep(0.5)
            
            # Check if bot is admin
            if bot_member.status not in ['administrator']:
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Bot Admin Required!**\n\n"
                    f"🤖 I need admin permissions to execute this command\n\n"
                    f"👑 **Required Permissions:**\n"
                    f"• Delete messages\n"
                    f"• Restrict members\n"
                    f"• Pin messages\n"
                    f"• Manage chat\n\n"
                    f"🔧 Please promote me to admin with these permissions",
                    parse_mode='Markdown'
                )
                return
                
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Unexpected error in bot_admin_required decorator: {e}")
            if update and update.message:
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Permission Error!**\n\n"
                    f"⚠️ Could not verify bot permissions\n"
                    f"🔄 Please try again"
                )
    
    return wrapper

def private_chat_only(func):
    """Decorator to restrict command to private chats only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            if update.effective_chat.type != 'private':
                await update.message.reply_text(
                    f"{EMOJIS['error']} This command only works in private chats!\n"
                    f"💬 Please message me directly to use this feature."
                )
                return
                
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in private_chat_only decorator: {e}")
            await update.message.reply_text(MESSAGES['action_failed'])
    
    return wrapper

def group_chat_only(func):
    """Decorator to restrict command to group chats only"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            if update.effective_chat.type == 'private':
                await update.message.reply_text(
                    f"{EMOJIS['error']} This command only works in groups!\n"
                    f"👥 Please use this command in a group chat."
                )
                return
                
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in group_chat_only decorator: {e}")
            await update.message.reply_text(MESSAGES['action_failed'])
    
    return wrapper

def rate_limit(max_calls=5, time_window=60):
    """Decorator to rate limit command usage"""
    user_calls = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            try:
                import time
                
                user_id = update.effective_user.id
                current_time = time.time()
                
                # Clean old entries
                if user_id in user_calls:
                    user_calls[user_id] = [
                        call_time for call_time in user_calls[user_id] 
                        if current_time - call_time < time_window
                    ]
                else:
                    user_calls[user_id] = []
                
                # Check rate limit
                if len(user_calls[user_id]) >= max_calls:
                    await update.message.reply_text(
                        f"{EMOJIS['warning']} **Rate Limit Exceeded!**\n\n"
                        f"⏰ Please wait before using this command again.\n"
                        f"📊 Limit: {max_calls} calls per {time_window} seconds"
                    )
                    return
                
                # Add current call
                user_calls[user_id].append(current_time)
                
                return await func(update, context, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Error in rate_limit decorator: {e}")
                await update.message.reply_text(MESSAGES['action_failed'])
        
        return wrapper
    return decorator

def log_command_usage(func):
    """Decorator to log command usage"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            command_name = func.__name__
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            username = update.effective_user.username or "No username"
            
            logger.info(
                f"Command '{command_name}' used by user {user_id} ({username}) "
                f"in chat {chat_id}"
            )
            
            return await func(update, context, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in log_command_usage decorator: {e}")
            return await func(update, context, *args, **kwargs)
    
    return wrapper
