"""
Helper functions for the Telegram Bot
Provides utility functions for user handling, time parsing, and more
"""

import logging
import re
from datetime import datetime, timedelta
from telegram import Update, User
from telegram.ext import ContextTypes
from telegram.error import BadRequest

logger = logging.getLogger(__name__)

async def get_user_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Extract user from command arguments or replied message
    Returns User object or None
    """
    try:
        # If replying to a message, get user from that message (most reliable)
        if update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user
            logger.info(f"Found user via reply: {target_user.id} ({target_user.first_name})")
            return target_user
            
        # If command has arguments, try to parse user
        if context.args and len(context.args) > 0:
            user_input = context.args[0].strip()
            
            # Try to parse user ID (most reliable for API)
            if user_input.isdigit():
                user_id = int(user_input)
                try:
                    chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
                    logger.info(f"Found user via ID: {chat_member.user.id} ({chat_member.user.first_name})")
                    return chat_member.user
                except BadRequest as e:
                    logger.warning(f"User ID {user_id} not found in chat: {e}")
                    return None
                    
            # Try to parse username (remove @ if present)
            elif user_input.startswith('@'):
                username = user_input[1:].lower()
                try:
                    # Search through administrators first (they're most likely to be targeted)
                    administrators = await context.bot.get_chat_administrators(update.effective_chat.id)
                    for admin in administrators:
                        if admin.user.username and admin.user.username.lower() == username:
                            logger.info(f"Found admin user via username: {admin.user.id} ({admin.user.first_name})")
                            return admin.user
                    
                    # If not found in admins, try a broader search (limited by Telegram API)
                    # Note: This is limited but covers most use cases
                    logger.warning(f"Username @{username} not found in admin list")
                    return None
                except Exception as e:
                    logger.error(f"Error searching for username @{username}: {e}")
                    return None
                    
            # Try parsing as plain username without @
            else:
                try:
                    administrators = await context.bot.get_chat_administrators(update.effective_chat.id)
                    for admin in administrators:
                        if admin.user.username and admin.user.username.lower() == user_input.lower():
                            logger.info(f"Found admin user via plain username: {admin.user.id} ({admin.user.first_name})")
                            return admin.user
                    return None
                except Exception as e:
                    logger.error(f"Error searching for plain username {user_input}: {e}")
                    return None
                    
        logger.warning("No user specified in command or reply")
        return None
        
    except Exception as e:
        logger.error(f"Error in get_user_from_message: {e}")
        return None

def format_user_mention(user: User) -> str:
    """
    Format user mention with fallback to name if no username
    """
    try:
        if user.username:
            return f"@{user.username}"
        else:
            # Create a text mention using first name
            return f"[{user.first_name}](tg://user?id={user.id})"
    except:
        return "Unknown User"

def parse_time(time_str: str) -> int:
    """
    Parse time string and return seconds
    Supports formats like: 1h, 30m, 45s, 2d
    """
    try:
        time_str = time_str.lower().strip()
        
        # Define multipliers
        multipliers = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800
        }
        
        # Extract number and unit
        match = re.match(r'^(\d+)([smhdw])$', time_str)
        if match:
            number = int(match.group(1))
            unit = match.group(2)
            return number * multipliers.get(unit, 1)
            
        # Try to parse as plain number (assume seconds)
        if time_str.isdigit():
            return int(time_str)
            
        return None
        
    except Exception as e:
        logger.error(f"Error parsing time string '{time_str}': {e}")
        return None

def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human readable string
    """
    try:
        if seconds < 60:
            return f"{seconds} second{'s' if seconds != 1 else ''}"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = seconds // 86400
            return f"{days} day{'s' if days != 1 else ''}"
    except:
        return "unknown duration"

def escape_markdown(text: str) -> str:
    """
    Escape markdown special characters in text
    """
    try:
        escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in escape_chars:
            text = text.replace(char, f'\\{char}')
        return text
    except:
        return str(text)

def get_chat_type_emoji(chat_type: str) -> str:
    """
    Get emoji for chat type
    """
    chat_type_emojis = {
        'private': '👤',
        'group': '👥',
        'supergroup': '🏢',
        'channel': '📢'
    }
    return chat_type_emojis.get(chat_type, '❓')

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human readable string
    """
    try:
        if size_bytes == 0:
            return "0 B"
            
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    except:
        return "Unknown size"

def is_valid_user_id(user_id_str: str) -> bool:
    """
    Check if string is a valid Telegram user ID
    """
    try:
        user_id = int(user_id_str)
        # Telegram user IDs are positive integers
        return user_id > 0
    except:
        return False

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis
    """
    try:
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    except:
        return str(text)

def format_timestamp(timestamp: datetime) -> str:
    """
    Format timestamp to readable string
    """
    try:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return "Unknown time"

def get_username_or_name(user: User) -> str:
    """
    Get username or fallback to first name
    """
    try:
        if user.username:
            return f"@{user.username}"
        return user.first_name or "Unknown User"
    except:
        return "Unknown User"

def clean_command_args(args: list) -> list:
    """
    Clean and filter command arguments
    """
    try:
        # Remove empty strings and strip whitespace
        cleaned = [arg.strip() for arg in args if arg.strip()]
        return cleaned
    except:
        return []

def is_admin_command(command: str) -> bool:
    """
    Check if command requires admin permissions
    """
    admin_commands = [
        'ban', 'unban', 'kick', 'promote', 'demote', 'pin', 'unpin',
        'setgrouppic', 'settitle', 'setdescription', 'mute', 'unmute',
        'warn', 'unwarn', 'del', 'purge', 'lock', 'unlock', 'setrules'
    ]
    return command.lower() in admin_commands

def validate_reason(reason: str) -> str:
    """
    Validate and clean reason text
    """
    try:
        if not reason or reason.strip() == "":
            return "No reason provided"
        
        # Limit reason length
        reason = reason.strip()
        if len(reason) > 200:
            reason = reason[:197] + "..."
            
        return reason
    except:
        return "No reason provided"

def get_time_until(future_time: datetime) -> str:
    """
    Get human readable time until future datetime
    """
    try:
        now = datetime.now()
        if future_time <= now:
            return "Already passed"
            
        delta = future_time - now
        
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            
        if not parts:
            return "Less than a minute"
            
        return ", ".join(parts)
    except:
        return "Unknown time"
