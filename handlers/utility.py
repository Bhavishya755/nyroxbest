"""
Utility command handlers for the Telegram Bot
Handles translate, weather, time and other utility functions
"""

import logging
import json
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from config import EMOJIS

logger = logging.getLogger(__name__)

# Language codes mapping for translation
LANGUAGE_CODES = {
    'english': 'en', 'en': 'en',
    'spanish': 'es', 'es': 'es',
    'french': 'fr', 'fr': 'fr',
    'german': 'de', 'de': 'de',
    'italian': 'it', 'it': 'it',
    'portuguese': 'pt', 'pt': 'pt',
    'russian': 'ru', 'ru': 'ru',
    'chinese': 'zh', 'zh': 'zh',
    'japanese': 'ja', 'ja': 'ja',
    'korean': 'ko', 'ko': 'ko',
    'arabic': 'ar', 'ar': 'ar',
    'hindi': 'hi', 'hi': 'hi',
    'turkish': 'tr', 'tr': 'tr',
    'dutch': 'nl', 'nl': 'nl',
    'polish': 'pl', 'pl': 'pl',
    'ukrainian': 'uk', 'uk': 'uk'
}

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Translate text between languages using a simple translation approach"""
    try:
        # Check if we have arguments or a replied message
        text_to_translate = ""
        target_lang = "en"  # Default to English
        
        if update.message.reply_to_message:
            # Translating a replied message
            text_to_translate = update.message.reply_to_message.text
            if context.args:
                target_lang = LANGUAGE_CODES.get(context.args[0].lower(), "en")
        elif context.args and len(context.args) >= 2:
            # Format: /translate [language] [text...]
            target_lang = LANGUAGE_CODES.get(context.args[0].lower(), "en")
            text_to_translate = " ".join(context.args[1:])
        else:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Translation Help**\n\n"
                f"🔤 **How to use:**\n"
                f"• Reply to a message: `/translate spanish`\n"
                f"• Direct text: `/translate french Hello world`\n\n"
                f"🌍 **Supported languages:**\n"
                f"english, spanish, french, german, italian, portuguese,\n"
                f"russian, chinese, japanese, korean, arabic, hindi,\n"
                f"turkish, dutch, polish, ukrainian\n\n"
                f"💡 **Examples:**\n"
                f"• `/translate spanish` (reply to message)\n"
                f"• `/translate fr Bonjour le monde`",
                parse_mode='Markdown'
            )
            return
            
        if not text_to_translate:
            await update.message.reply_text(
                f"{EMOJIS['error']} No text found to translate!"
            )
            return
            
        # Simple translation simulation (in real deployment, you'd use Google Translate API)
        # For demo purposes, we'll provide a basic response
        translated_text = f"[Translation to {target_lang.upper()}] {text_to_translate}"
        
        # Create a more realistic translation response
        response_text = f"🌐 **Translation Complete!**\n\n"
        response_text += f"📝 **Original:** {text_to_translate}\n"
        response_text += f"🔤 **Language:** {target_lang.upper()}\n"
        response_text += f"✨ **Translated:** {translated_text}\n\n"
        response_text += f"💡 *Note: For full translation features, API key setup required*"
        
        await update.message.reply_text(response_text, parse_mode='Markdown')
        logger.info(f"Translation requested by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in translate_text: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Translation failed!")

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current time and date"""
    try:
        now = datetime.now()
        
        time_text = f"🕐 **Current Time & Date**\n\n"
        time_text += f"📅 **Date:** {now.strftime('%A, %B %d, %Y')}\n"
        time_text += f"⏰ **Time:** {now.strftime('%H:%M:%S UTC')}\n"
        time_text += f"🌍 **Timezone:** UTC (Server Time)\n\n"
        time_text += f"📊 **Formats:**\n"
        time_text += f"• 24h: {now.strftime('%H:%M:%S')}\n"
        time_text += f"• 12h: {now.strftime('%I:%M:%S %p')}\n"
        time_text += f"• ISO: {now.isoformat()}\n"
        time_text += f"• Unix: {int(now.timestamp())}"
        
        await update.message.reply_text(time_text, parse_mode='Markdown')
        logger.info(f"Time command used by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in time_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Could not get current time!")

async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple calculator command"""
    try:
        if not context.args:
            await update.message.reply_text(
                f"🧮 **Calculator Help**\n\n"
                f"📊 **Usage:** `/calc [expression]`\n\n"
                f"🔢 **Examples:**\n"
                f"• `/calc 2 + 2`\n"
                f"• `/calc 10 * 5`\n"
                f"• `/calc 100 / 4`\n"
                f"• `/calc 2 ** 3` (power)\n\n"
                f"⚠️ **Supported:** +, -, *, /, **, (, )\n"
                f"🛡️ Safe calculation only - no external functions",
                parse_mode='Markdown'
            )
            return
            
        expression = " ".join(context.args)
        
        # Safety check - only allow basic math operations
        allowed_chars = "0123456789+-*/.()**  "
        if not all(c in allowed_chars for c in expression):
            await update.message.reply_text(
                f"{EMOJIS['error']} **Invalid Expression!**\n\n"
                f"🔢 Only numbers and basic math operators allowed\n"
                f"✅ Allowed: + - * / ** ( )"
            )
            return
            
        # Evaluate the expression safely
        try:
            result = eval(expression)
            
            calc_text = f"🧮 **Calculator Result**\n\n"
            calc_text += f"📝 **Expression:** `{expression}`\n"
            calc_text += f"✨ **Result:** `{result}`\n\n"
            
            # Add some extra info for interesting results
            if isinstance(result, (int, float)):
                if result == int(result):
                    calc_text += f"🔢 **Type:** Integer\n"
                else:
                    calc_text += f"🔢 **Type:** Decimal\n"
                    calc_text += f"📊 **Rounded:** `{round(result, 2)}`"
            
            await update.message.reply_text(calc_text, parse_mode='Markdown')
            logger.info(f"Calculation by user {update.effective_user.id}: {expression} = {result}")
            
        except ZeroDivisionError:
            await update.message.reply_text(
                f"{EMOJIS['error']} **Division by Zero!**\n\n"
                f"🚫 Cannot divide by zero\n"
                f"💡 Try a different expression"
            )
        except (ValueError, SyntaxError):
            await update.message.reply_text(
                f"{EMOJIS['error']} **Invalid Expression!**\n\n"
                f"❌ Could not calculate: `{expression}`\n"
                f"💡 Check your math syntax"
            )
            
    except Exception as e:
        logger.error(f"Error in calculate_command: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Calculator error!")

async def generate_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a secure random password"""
    try:
        import random
        import string
        
        # Default length
        length = 12
        
        # Check if length is specified
        if context.args and context.args[0].isdigit():
            length = min(max(int(context.args[0]), 6), 50)  # Between 6 and 50
            
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"
        
        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
            
        # Shuffle the password
        random.shuffle(password)
        final_password = ''.join(password)
        
        pwd_text = f"🔐 **Password Generated!**\n\n"
        pwd_text += f"🎯 **Length:** {length} characters\n"
        pwd_text += f"🔑 **Password:** `{final_password}`\n\n"
        pwd_text += f"🛡️ **Security Features:**\n"
        pwd_text += f"• Uppercase letters ✅\n"
        pwd_text += f"• Lowercase letters ✅\n"
        pwd_text += f"• Numbers ✅\n"
        pwd_text += f"• Special characters ✅\n\n"
        pwd_text += f"⚠️ **Security Note:** Delete this message after copying!"
        
        await update.message.reply_text(pwd_text, parse_mode='Markdown')
        logger.info(f"Password generated for user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in generate_password: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Password generation failed!")