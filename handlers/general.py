"""
General command handlers for the Telegram Bot
Handles start, help, menu and other general functions
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import (BOT_NAME, BOT_VERSION, BOT_DESCRIPTION, EMOJIS, 
                   ADMIN_COMMANDS, MODERATION_COMMANDS, FUN_COMMANDS, 
                   INFO_COMMANDS, GENERAL_COMMANDS)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued"""
    try:
        user_name = update.effective_user.first_name
        chat_type = update.effective_chat.type
        
        if chat_type == 'private':
            welcome_text = f"🎉 **Welcome to {BOT_NAME}!**\n\n"
            welcome_text += f"👋 Hi {user_name}! I'm your comprehensive admin and moderation bot.\n\n"
            welcome_text += f"🚀 **Version:** {BOT_VERSION}\n"
            welcome_text += f"📝 **Description:** {BOT_DESCRIPTION}\n\n"
            welcome_text += f"💡 **Quick Start:**\n"
            welcome_text += f"• Add me to your group\n"
            welcome_text += f"• Make me an admin\n" 
            welcome_text += f"• Use `/help` to see all commands\n\n"
            welcome_text += f"🔧 **Features:**\n"
            welcome_text += f"• 🛡️ Advanced moderation tools\n"
            welcome_text += f"• 👑 Admin management commands\n"
            welcome_text += f"• 🎮 Fun entertainment features\n"
            welcome_text += f"• 📊 Information and statistics\n"
            welcome_text += f"• 🎨 Rich emoji interface\n\n"
            welcome_text += f"📚 Use `/menu` to explore all features!"
        else:
            welcome_text = f"🎉 **{BOT_NAME} is now active!**\n\n"
            welcome_text += f"👋 Hello everyone! I'm ready to help manage this group.\n\n"
            welcome_text += f"🛡️ **Ready to provide:**\n"
            welcome_text += f"• Advanced moderation tools\n"
            welcome_text += f"• Admin management features\n"
            welcome_text += f"• Fun entertainment commands\n"
            welcome_text += f"• Group information tools\n\n"
            welcome_text += f"📚 Type `/help` or `/menu` to get started!"
            
        # Create inline keyboard for private chats
        if chat_type == 'private':
            keyboard = [
                [InlineKeyboardButton("📚 Help", callback_data="help"),
                 InlineKeyboardButton("📋 Menu", callback_data="menu")],
                [InlineKeyboardButton("🛡️ Admin Commands", callback_data="admin_help"),
                 InlineKeyboardButton("🎮 Fun Commands", callback_data="fun_help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None
            
        await update.message.reply_text(
            welcome_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        logger.info(f"Start command used by user {update.effective_user.id} in chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to send welcome message!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message with all available commands"""
    try:
        help_text = f"📚 **{BOT_NAME} - Help Center**\n\n"
        help_text += f"🤖 **Version:** {BOT_VERSION}\n"
        help_text += f"📝 **Description:** {BOT_DESCRIPTION}\n\n"
        
        # General Commands
        help_text += f"🔧 **General Commands:**\n"
        for cmd, desc in GENERAL_COMMANDS.items():
            help_text += f"• `/{cmd}` - {desc}\n"
        help_text += "\n"
        
        # Admin Commands
        help_text += f"👑 **Admin Commands:**\n"
        for cmd, desc in list(ADMIN_COMMANDS.items())[:5]:  # Show first 5
            help_text += f"• `/{cmd}` - {desc}\n"
        help_text += f"• _...and {len(ADMIN_COMMANDS)-5} more admin commands_\n\n"
        
        # Moderation Commands  
        help_text += f"🛡️ **Moderation Commands:**\n"
        for cmd, desc in list(MODERATION_COMMANDS.items())[:5]:  # Show first 5
            help_text += f"• `/{cmd}` - {desc}\n"
        help_text += f"• _...and {len(MODERATION_COMMANDS)-5} more moderation commands_\n\n"
        
        # Info Commands
        help_text += f"📊 **Information Commands:**\n"
        for cmd, desc in list(INFO_COMMANDS.items())[:4]:  # Show first 4
            help_text += f"• `/{cmd}` - {desc}\n"
        help_text += f"• _...and {len(INFO_COMMANDS)-4} more info commands_\n\n"
        
        # Fun Commands
        help_text += f"🎮 **Fun Commands:**\n"
        for cmd, desc in list(FUN_COMMANDS.items())[:4]:  # Show first 4
            help_text += f"• `/{cmd}` - {desc}\n"
        help_text += f"• _...and {len(FUN_COMMANDS)-4} more fun commands_\n\n"
        
        help_text += f"🛠️ **Utility Commands:**\n"
        help_text += f"• `/translate` - 🌐 Translate text between languages\n"
        help_text += f"• `/time` - 🕐 Get current time and date\n"
        help_text += f"• `/calc` - 🧮 Calculate math expressions\n"
        help_text += f"• `/password` - 🔐 Generate secure passwords\n\n"
        
        help_text += f"💡 **Tips:**\n"
        help_text += f"• Use `/menu` for an interactive command browser\n"
        help_text += f"• Most admin commands require admin permissions\n"
        help_text += f"• Reply to messages for user-specific commands\n"
        help_text += f"• Bot needs admin rights for moderation features\n\n"
        
        help_text += f"🆘 **Need more help?** Use `/menu` for detailed command categories!"
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("📋 Interactive Menu", callback_data="menu"),
             InlineKeyboardButton("🔄 Refresh", callback_data="help")],
            [InlineKeyboardButton("👑 Admin Help", callback_data="admin_help"),
             InlineKeyboardButton("🛡️ Moderation Help", callback_data="mod_help")],
            [InlineKeyboardButton("📊 Info Help", callback_data="info_help"),
             InlineKeyboardButton("🎮 Fun Help", callback_data="fun_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        logger.info(f"Help command used by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to send help message!")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send interactive menu with command categories"""
    try:
        menu_text = f"📋 **{BOT_NAME} - Interactive Menu**\n\n"
        menu_text += f"🎯 Choose a category to explore commands:\n\n"
        
        menu_text += f"👑 **Admin Commands** ({len(ADMIN_COMMANDS)})\n"
        menu_text += f"├ Ban, kick, promote users\n"
        menu_text += f"├ Manage group settings\n"
        menu_text += f"└ Pin messages and more\n\n"
        
        menu_text += f"🛡️ **Moderation Commands** ({len(MODERATION_COMMANDS)})\n"
        menu_text += f"├ Mute, warn users\n"
        menu_text += f"├ Delete and purge messages\n"
        menu_text += f"└ Lock/unlock chat\n\n"
        
        menu_text += f"📊 **Information Commands** ({len(INFO_COMMANDS)})\n"
        menu_text += f"├ User and chat info\n"
        menu_text += f"├ Admin lists and rules\n"
        menu_text += f"└ Member statistics\n\n"
        
        menu_text += f"🎮 **Fun Commands** ({len(FUN_COMMANDS)})\n"
        menu_text += f"├ Games and entertainment\n"
        menu_text += f"├ Random quotes and jokes\n"
        menu_text += f"└ Interactive features\n\n"
        
        menu_text += f"💡 **Tip:** Click buttons below to explore each category!"
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton(f"👑 Admin ({len(ADMIN_COMMANDS)})", callback_data="admin_help"),
             InlineKeyboardButton(f"🛡️ Moderation ({len(MODERATION_COMMANDS)})", callback_data="mod_help")],
            [InlineKeyboardButton(f"📊 Information ({len(INFO_COMMANDS)})", callback_data="info_help"),
             InlineKeyboardButton(f"🎮 Fun ({len(FUN_COMMANDS)})", callback_data="fun_help")],
            [InlineKeyboardButton("📚 Full Help", callback_data="help"),
             InlineKeyboardButton("🔄 Refresh Menu", callback_data="menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            menu_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        logger.info(f"Menu command used by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in menu_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to send menu!")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses from inline keyboards"""
    try:
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "help":
            await show_help_callback(query)
        elif callback_data == "menu":
            await show_menu_callback(query)
        elif callback_data == "admin_help":
            await show_admin_help_callback(query)
        elif callback_data == "mod_help":
            await show_mod_help_callback(query)
        elif callback_data == "info_help":
            await show_info_help_callback(query)
        elif callback_data == "fun_help":
            await show_fun_help_callback(query)
            
        logger.info(f"Button callback: {callback_data} by user {query.from_user.id}")
        
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")

async def show_help_callback(query):
    """Show help via callback"""
    help_text = f"📚 **{BOT_NAME} - Help Center**\n\n"
    help_text += f"🎯 **Quick Command Reference:**\n\n"
    
    # Sample commands from each category
    help_text += f"👑 **Admin:** `/ban` `/kick` `/promote` `/demote`\n"
    help_text += f"🛡️ **Moderation:** `/mute` `/warn` `/del` `/purge`\n"
    help_text += f"📊 **Info:** `/info` `/admins` `/members` `/rules`\n"
    help_text += f"🎮 **Fun:** `/dice` `/joke` `/quote` `/8ball`\n\n"
    
    help_text += f"💡 **Usage Examples:**\n"
    help_text += f"• `/ban @username` - Ban a user\n"
    help_text += f"• `/mute @username 1h` - Mute for 1 hour\n"
    help_text += f"• `/warn @username reason` - Warn with reason\n"
    help_text += f"• `/joke` - Get a random joke\n\n"
    
    help_text += f"🔧 **Requirements:**\n"
    help_text += f"• Bot must be admin for moderation\n"
    help_text += f"• You must be admin for admin commands\n"
    help_text += f"• Some commands work via reply to messages"
    
    keyboard = [
        [InlineKeyboardButton("📋 Back to Menu", callback_data="menu"),
         InlineKeyboardButton("🔄 Refresh", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_menu_callback(query):
    """Show menu via callback"""
    menu_text = f"📋 **{BOT_NAME} - Command Menu**\n\n"
    menu_text += f"🎯 **Select a category to view detailed commands:**\n\n"
    
    categories = [
        (f"👑 **Admin Commands** ({len(ADMIN_COMMANDS)})", "User management, group settings"),
        (f"🛡️ **Moderation** ({len(MODERATION_COMMANDS)})", "Chat moderation, warnings"),
        (f"📊 **Information** ({len(INFO_COMMANDS)})", "User info, statistics, rules"),
        (f"🎮 **Fun Commands** ({len(FUN_COMMANDS)})", "Games, jokes, entertainment")
    ]
    
    for category, description in categories:
        menu_text += f"{category}\n└ {description}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("👑 Admin", callback_data="admin_help"),
         InlineKeyboardButton("🛡️ Moderation", callback_data="mod_help")],
        [InlineKeyboardButton("📊 Information", callback_data="info_help"),
         InlineKeyboardButton("🎮 Fun", callback_data="fun_help")],
        [InlineKeyboardButton("📚 Full Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_admin_help_callback(query):
    """Show admin commands via callback"""
    admin_text = f"👑 **Admin Commands**\n\n"
    admin_text += f"🔒 **Requirements:** Admin permissions required\n\n"
    
    for cmd, desc in ADMIN_COMMANDS.items():
        admin_text += f"• `/{cmd}` - {desc}\n"
    
    admin_text += f"\n💡 **Usage Examples:**\n"
    admin_text += f"• `/ban @username reason` - Ban user with reason\n"
    admin_text += f"• `/promote @username` - Promote to admin\n"
    admin_text += f"• `/settitle New Group Name` - Change title\n"
    admin_text += f"• `/pin` - Pin replied message\n\n"
    
    admin_text += f"⚠️ **Note:** Bot needs admin rights to execute these commands"
    
    keyboard = [
        [InlineKeyboardButton("🛡️ Moderation", callback_data="mod_help"),
         InlineKeyboardButton("📊 Information", callback_data="info_help")],
        [InlineKeyboardButton("📋 Back to Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_mod_help_callback(query):
    """Show moderation commands via callback"""
    mod_text = f"🛡️ **Moderation Commands**\n\n"
    mod_text += f"🔒 **Requirements:** Admin permissions required\n\n"
    
    for cmd, desc in MODERATION_COMMANDS.items():
        mod_text += f"• `/{cmd}` - {desc}\n"
    
    mod_text += f"\n💡 **Usage Examples:**\n"
    mod_text += f"• `/mute @username 1h` - Mute for 1 hour\n"
    mod_text += f"• `/warn @username spam` - Warn for spam\n"
    mod_text += f"• `/del` - Delete replied message\n"
    mod_text += f"• `/lock` - Lock chat for members\n\n"
    
    mod_text += f"📊 **Auto-moderation:**\n"
    mod_text += f"• Users are auto-banned after 3 warnings\n"
    mod_text += f"• Warnings are tracked per user"
    
    keyboard = [
        [InlineKeyboardButton("👑 Admin", callback_data="admin_help"),
         InlineKeyboardButton("📊 Information", callback_data="info_help")],
        [InlineKeyboardButton("📋 Back to Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(mod_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_info_help_callback(query):
    """Show info commands via callback"""
    info_text = f"📊 **Information Commands**\n\n"
    info_text += f"🔓 **Requirements:** Available to all users\n\n"
    
    for cmd, desc in INFO_COMMANDS.items():
        info_text += f"• `/{cmd}` - {desc}\n"
    
    info_text += f"\n💡 **Usage Examples:**\n"
    info_text += f"• `/info @username` - Get user details\n"
    info_text += f"• `/admins` - List all admins\n"
    info_text += f"• `/members` - Get member count\n"
    info_text += f"• `/id` - Get your ID\n\n"
    
    info_text += f"📝 **Special Features:**\n"
    info_text += f"• Detailed user profiles with permissions\n"
    info_text += f"• Group statistics and member info\n"
    info_text += f"• Custom rules management"
    
    keyboard = [
        [InlineKeyboardButton("👑 Admin", callback_data="admin_help"),
         InlineKeyboardButton("🎮 Fun", callback_data="fun_help")],
        [InlineKeyboardButton("📋 Back to Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(info_text, parse_mode='Markdown', reply_markup=reply_markup)

async def show_fun_help_callback(query):
    """Show fun commands via callback"""
    fun_text = f"🎮 **Fun Commands**\n\n"
    fun_text += f"🔓 **Requirements:** Available to all users\n\n"
    
    for cmd, desc in FUN_COMMANDS.items():
        fun_text += f"• `/{cmd}` - {desc}\n"
    
    fun_text += f"\n💡 **Usage Examples:**\n"
    fun_text += f"• `/dice` - Roll a dice (1-6)\n"
    fun_text += f"• `/8ball Will I win?` - Ask magic 8-ball\n"
    fun_text += f"• `/choose pizza burger tacos` - Pick option\n"
    fun_text += f"• `/joke` - Get random joke\n\n"
    
    fun_text += f"🎊 **Entertainment Features:**\n"
    fun_text += f"• Random quotes for inspiration\n"
    fun_text += f"• Fun facts to learn new things\n"
    fun_text += f"• Interactive games and choices"
    
    keyboard = [
        [InlineKeyboardButton("🛡️ Moderation", callback_data="mod_help"),
         InlineKeyboardButton("📊 Information", callback_data="info_help")],
        [InlineKeyboardButton("📋 Back to Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(fun_text, parse_mode='Markdown', reply_markup=reply_markup)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members to the group"""
    try:
        new_members = update.message.new_chat_members
        
        for member in new_members:
            if member.is_bot:
                continue
                
            welcome_text = f"🎉 **Welcome to the group!**\n\n"
            welcome_text += f"👋 Hi {member.first_name}! Welcome to {update.effective_chat.title}!\n\n"
            welcome_text += f"📋 **Quick Start:**\n"
            welcome_text += f"• Read the group rules: `/rules`\n"
            welcome_text += f"• Get help with commands: `/help`\n"
            welcome_text += f"• Have fun and be respectful! 😊\n\n"
            welcome_text += f"🤖 I'm here to help manage the group. Feel free to explore my features!"
            
            await update.message.reply_text(welcome_text, parse_mode='Markdown')
            
        logger.info(f"Welcomed {len(new_members)} new members to chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in welcome_new_member: {e}")

async def goodbye_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Say goodbye to leaving members"""
    try:
        left_member = update.message.left_chat_member
        
        if left_member and not left_member.is_bot:
            goodbye_text = f"👋 **Goodbye!**\n\n"
            goodbye_text += f"😢 {left_member.first_name} has left the group.\n"
            goodbye_text += f"We'll miss you! Feel free to come back anytime. 💙"
            
            await update.message.reply_text(goodbye_text, parse_mode='Markdown')
            
        logger.info(f"Said goodbye to user {left_member.id} from chat {update.effective_chat.id}")
        
    except Exception as e:
        logger.error(f"Error in goodbye_member: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors that occur during bot operation"""
    try:
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                f"{EMOJIS['error']} **Oops! Something went wrong.**\n\n"
                f"🔧 Please try again or contact an admin if the problem persists.\n"
                f"📝 Error has been logged for debugging."
            )
            
    except Exception as e:
        logger.error(f"Error in error_handler: {e}")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command to verify bot functionality"""
    try:
        await update.message.reply_text(
            f"✅ **Bot Test Successful!**\n\n"
            f"🤖 **Bot Status:** Online and working\n"
            f"👤 **Your ID:** `{update.effective_user.id}`\n"
            f"💬 **Chat ID:** `{update.effective_chat.id}`\n"
            f"⏰ Time: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"🔧 **Admin Commands:** Try replying to a message and use `/ban` or `/kick`\n"
            f"🎮 **Fun Commands:** Working perfectly (dice, jokes, etc.)\n"
            f"📊 **Info Commands:** All functional",
            parse_mode='Markdown'
        )
        logger.info(f"Test command used by user {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Error in test_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Test failed!")
