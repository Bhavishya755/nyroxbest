"""
Main entry point for the Telegram Bot with Keep-Alive Server
This combines the bot and web server for 24/7 operation on Replit
"""

import logging
from simple_server import keep_alive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🚀 Starting Telegram Bot with Keep-Alive Server")
    logger.info("=" * 50)
    
    # Start keep-alive server
    keep_alive()
    
    # Start bot directly
    from main import main
    main()