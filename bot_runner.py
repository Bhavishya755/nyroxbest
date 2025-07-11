"""
Simple Bot Runner with Keep-Alive for 24/7 Operation
This approach prioritizes reliability and simplicity
"""

import logging
import threading
import time
import os
from keep_alive_simple import keep_alive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run the Telegram bot"""
    try:
        logger.info("🚀 Starting Telegram Bot...")
        
        # Import main bot function
        from main import main
        
        # Run the bot
        main()
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
        logger.info("Restarting bot in 10 seconds...")
        time.sleep(10)
        run_bot()  # Restart on error

def main():
    """Main function to start both keep-alive and bot"""
    try:
        logger.info("=" * 50)
        logger.info("🤖 Starting 24/7 Telegram Bot System")
        logger.info("=" * 50)
        
        # Start keep-alive server first
        keep_alive()
        
        # Start bot
        run_bot()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"System error: {e}")
        logger.info("Restarting system...")
        time.sleep(5)
        main()

if __name__ == '__main__':
    main()