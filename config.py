"""
Configuration file for the Telegram Bot
Contains bot settings, commands, and constants
"""

import os

# Bot Token - Get from environment or use the provided token
BOT_TOKEN = os.getenv("BOT_TOKEN", "7749307110:AAHohAq2WqBWdBXN2RjtQ55VY2BEbzsNUo4")

# Bot Information
BOT_NAME = "🤖 Admin Pro Bot"
BOT_VERSION = "2.0.0"
BOT_DESCRIPTION = "Comprehensive admin and moderation bot with emoji-rich interface"

# Command Categories
ADMIN_COMMANDS = {
    "ban": "🚫 Ban a user from the group",
    "unban": "✅ Unban a user from the group", 
    "kick": "👢 Kick a user from the group",
    "promote": "⬆️ Promote user to admin",
    "demote": "⬇️ Demote admin to member",
    "pin": "📌 Pin a message",
    "unpin": "📌 Unpin a message",
    "setgrouppic": "🖼️ Set group profile picture",
    "settitle": "📝 Set group title",
    "setdescription": "📄 Set group description"
}

MODERATION_COMMANDS = {
    "mute": "🔇 Mute a user",
    "unmute": "🔊 Unmute a user",
    "warn": "⚠️ Warn a user",
    "unwarn": "❌ Remove warning from user",
    "warnings": "📋 Check user warnings",
    "del": "🗑️ Delete a message",
    "purge": "🧹 Delete multiple messages",
    "lock": "🔒 Lock chat for members",
    "unlock": "🔓 Unlock chat for members"
}

INFO_COMMANDS = {
    "info": "👤 Get user information",
    "chatinfo": "💬 Get chat information",
    "admins": "👑 List chat admins",
    "members": "👥 Get member count",
    "id": "🆔 Get user/chat ID",
    "rules": "📜 Show group rules",
    "setrules": "📝 Set group rules"
}

FUN_COMMANDS = {
    "dice": "🎲 Roll a dice",
    "coin": "🪙 Flip a coin",
    "quote": "💭 Get random quote",
    "joke": "😂 Get random joke",
    "fact": "🧠 Get random fact",
    "8ball": "🎱 Magic 8-ball",
    "choose": "🤔 Choose between options"
}

UTILITY_COMMANDS = {
    "translate": "🌐 Translate text between languages",
    "time": "🕐 Get current time and date", 
    "calc": "🧮 Calculate math expressions",
    "password": "🔐 Generate secure passwords",
    "test": "✅ Test bot functionality"
}

GENERAL_COMMANDS = {
    "start": "🚀 Start the bot",
    "help": "❓ Get help",
    "menu": "📋 Show main menu"
}

# Emojis
EMOJIS = {
    "success": "✅",
    "error": "❌", 
    "warning": "⚠️",
    "info": "ℹ️",
    "admin": "👑",
    "user": "👤",
    "group": "👥",
    "ban": "🚫",
    "kick": "👢",
    "mute": "🔇",
    "delete": "🗑️",
    "pin": "📌",
    "lock": "🔒",
    "unlock": "🔓"
}

# Messages
MESSAGES = {
    "no_permission": f"{EMOJIS['error']} You don't have permission to use this command!",
    "admin_only": f"{EMOJIS['admin']} This command is for admins only!",
    "user_not_found": f"{EMOJIS['error']} User not found!",
    "cant_act_on_admin": f"{EMOJIS['warning']} Cannot perform this action on an admin!",
    "already_admin": f"{EMOJIS['info']} User is already an admin!",
    "not_admin": f"{EMOJIS['info']} User is not an admin!",
    "action_failed": f"{EMOJIS['error']} Action failed! Please try again.",
    "success": f"{EMOJIS['success']} Action completed successfully!"
}

# Settings
MAX_WARNINGS = 3
DEFAULT_MUTE_TIME = 3600  # 1 hour in seconds
MAX_PURGE_MESSAGES = 100
