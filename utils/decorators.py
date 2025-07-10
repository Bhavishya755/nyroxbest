"""
Decorators for the Telegram Bot
Provides admin checking, rate limiting and other useful decorators
"""

import logging
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
                
            # Get user's chat member status
            chat_member = await context.bot.get_chat_member(
                update.effective_chat.id, 
                update.effective_user.id
            )
            
            # Check if user is admin or creator
            if chat_member.status not in ['administrator', 'creator']:
                await update.message.reply_text(MESSAGES['admin_only'])
                return
                
            return await func(update, context, *args, **kwargs)
            
        except BadRequest as e:
            logger.error(f"BadRequest in admin_required: {e}")
            await update.message.reply_text(f"{EMOJIS['error']} Could not verify admin status!")
        except Exception as e:
            logger.error(f"Error in admin_required decorator: {e}")
            await update.message.reply_text(MESSAGES['action_failed'])
    
    return wrapper

def bot_admin_required(func):
    """Decorator to check if bot has admin permissions before executing command"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            # Skip check in private chats
            if update.effective_chat.type == 'private':
                await update.message.reply_text(
                    f"{EMOJIS['error']} This command only works in groups!"
                )
                return
                
            # Get bot's chat member status
            bot_member = await context.bot.get_chat_member(
                update.effective_chat.id, 
                context.bot.id
            )
            
            # Check if bot is admin
            if bot_member.status not in ['administrator']:
                await update.message.reply_text(
                    f"{EMOJIS['error']} **Bot Admin Required!**\n\n"
                    f"🤖 I need admin permissions to execute this command.\n"
                    f"👑 Please promote me to admin with necessary permissions:\n"
                    f"• Delete messages\n"
                    f"• Restrict members\n"
                    f"• Pin messages\n"
                    f"• Manage chat",
                    parse_mode='Markdown'
                )
                return
                
            return await func(update, context, *args, **kwargs)
            
        except BadRequest as e:
            logger.error(f"BadRequest in bot_admin_required: {e}")
            await update.message.reply_text(f"{EMOJIS['error']} Could not verify bot admin status!")
        except Exception as e:
            logger.error(f"Error in bot_admin_required decorator: {e}")
            await update.message.reply_text(MESSAGES['action_failed'])
    
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
