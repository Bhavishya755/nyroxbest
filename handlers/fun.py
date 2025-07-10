"""
Fun command handlers for the Telegram Bot
Handles dice, coin flip, jokes, quotes and other entertainment functions
"""

import logging
import json
import random
from telegram import Update
from telegram.ext import ContextTypes
from config import EMOJIS

logger = logging.getLogger(__name__)

# Load jokes and quotes
def load_json_data(filename, default_data):
    """Load data from JSON file with fallback"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return default_data

async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice"""
    try:
        # Send dice emoji
        dice_result = await context.bot.send_dice(update.effective_chat.id, emoji="🎲")
        
        await update.message.reply_text(
            f"🎲 **Dice Roll!**\n\n"
            f"👤 **Player:** {update.effective_user.first_name}\n"
            f"🎯 **Result:** {dice_result.dice.value}\n"
            f"🍀 **Luck Level:** {'🔥 ON FIRE!' if dice_result.dice.value == 6 else '😭 UNLUCKY!' if dice_result.dice.value == 1 else '🙂 Not bad!'}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Dice rolled by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in roll_dice: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to roll dice!")

async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin"""
    try:
        result = random.choice(["Heads", "Tails"])
        emoji = "👑" if result == "Heads" else "⚡"
        
        await update.message.reply_text(
            f"🪙 **Coin Flip!**\n\n"
            f"👤 **Player:** {update.effective_user.first_name}\n"
            f"🎯 **Result:** {emoji} {result}\n"
            f"🎊 **Status:** {'You called it!' if len(context.args) > 0 and context.args[0].lower() == result.lower() else 'Better luck next time!'}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Coin flipped by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in flip_coin: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to flip coin!")

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random inspirational quote"""
    try:
        quotes_data = load_json_data('data/quotes.json', {
            "quotes": [
                {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
                {"text": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
                {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
                {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
                {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"}
            ]
        })
        
        quote = random.choice(quotes_data["quotes"])
        
        await update.message.reply_text(
            f"💭 **Random Quote**\n\n"
            f"📝 *\"{quote['text']}\"*\n\n"
            f"👨‍💼 **— {quote['author']}**\n\n"
            f"🌟 Requested by {update.effective_user.first_name}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Quote sent to user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in random_quote: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get quote!")

async def random_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random joke"""
    try:
        jokes_data = load_json_data('data/jokes.json', {
            "jokes": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "Why did the math book look so sad? Because it was full of problems!"
            ]
        })
        
        joke = random.choice(jokes_data["jokes"])
        
        await update.message.reply_text(
            f"😂 **Random Joke**\n\n"
            f"🎭 {joke}\n\n"
            f"😄 Hope that made you smile, {update.effective_user.first_name}!",
            parse_mode='Markdown'
        )
        
        logger.info(f"Joke sent to user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in random_joke: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get joke!")

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fun fact"""
    try:
        facts = [
            "🐙 Octopuses have three hearts and blue blood!",
            "🍯 Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
            "🧠 Your brain uses about 20% of your body's total energy!",
            "🌍 There are more possible games of chess than there are atoms in the observable universe!",
            "🦒 A giraffe's tongue can be up to 20 inches long!",
            "🌊 The Pacific Ocean is larger than all the continents combined!",
            "⚡ Lightning strikes the Earth about 100 times per second!",
            "🐘 Elephants are the only animals that can't jump!",
            "🍌 Bananas are berries, but strawberries aren't!",
            "🌙 The Moon is moving away from Earth at about 1.5 inches per year!"
        ]
        
        fact = random.choice(facts)
        
        await update.message.reply_text(
            f"🧠 **Random Fun Fact**\n\n"
            f"📚 {fact}\n\n"
            f"🤓 Learn something new every day, {update.effective_user.first_name}!",
            parse_mode='Markdown'
        )
        
        logger.info(f"Fact sent to user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in random_fact: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to get fact!")

async def magic_8ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Magic 8-ball responses"""
    try:
        if not context.args:
            await update.message.reply_text(
                f"🎱 **Magic 8-Ball**\n\n"
                f"❓ Please ask a question!\n"
                f"💡 Usage: `/8ball Will I be successful?`"
            )
            return
            
        question = ' '.join(context.args)
        
        responses = [
            "🔮 It is certain",
            "🔮 Without a doubt", 
            "🔮 Yes definitely",
            "🔮 You may rely on it",
            "🔮 As I see it, yes",
            "🔮 Most likely",
            "🔮 Outlook good",
            "🔮 Yes",
            "🔮 Signs point to yes",
            "🔮 Reply hazy, try again",
            "🔮 Ask again later",
            "🔮 Better not tell you now",
            "🔮 Cannot predict now",
            "🔮 Concentrate and ask again",
            "🔮 Don't count on it",
            "🔮 My reply is no",
            "🔮 My sources say no",
            "🔮 Outlook not so good",
            "🔮 Very doubtful"
        ]
        
        response = random.choice(responses)
        
        await update.message.reply_text(
            f"🎱 **Magic 8-Ball**\n\n"
            f"❓ **Question:** {question}\n\n"
            f"🔮 **Answer:** {response}\n\n"
            f"👤 Asked by {update.effective_user.first_name}",
            parse_mode='Markdown'
        )
        
        logger.info(f"8-ball question asked by user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in magic_8ball: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to consult magic 8-ball!")

async def choose_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Choose between given options"""
    try:
        if len(context.args) < 2:
            await update.message.reply_text(
                f"🤔 **Choose Command**\n\n"
                f"❓ Please provide at least 2 options!\n"
                f"💡 Usage: `/choose pizza burger tacos`"
            )
            return
            
        options = context.args
        choice = random.choice(options)
        
        await update.message.reply_text(
            f"🤔 **Random Choice**\n\n"
            f"📝 **Options:** {', '.join(options)}\n\n"
            f"🎯 **My Choice:** **{choice}**\n\n"
            f"👤 Chosen for {update.effective_user.first_name}",
            parse_mode='Markdown'
        )
        
        logger.info(f"Choice made for user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in choose_option: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} Failed to make choice!")
