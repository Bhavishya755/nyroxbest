"""
Flask Keep-Alive Server for Telegram Bot
Provides a web server that keeps the bot running 24/7 on Replit
"""

from flask import Flask, jsonify
import threading
import time
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Bot status tracking
bot_status = {
    'running': False,
    'start_time': None,
    'last_update': None,
    'health_checks': 0
}

@app.route('/')
def home():
    """Main endpoint - returns bot status"""
    uptime = None
    if bot_status['start_time']:
        uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        uptime = f"{hours}h {minutes}m"
    
    return jsonify({
        'message': 'Bot is running!',
        'status': 'online' if bot_status['running'] else 'offline',
        'uptime': uptime,
        'last_update': bot_status['last_update'].isoformat() if bot_status['last_update'] else None,
        'health_checks': bot_status['health_checks'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for UptimeRobot"""
    bot_status['health_checks'] += 1
    bot_status['last_update'] = datetime.now()
    
    return jsonify({
        'status': 'healthy',
        'bot_running': bot_status['running'],
        'timestamp': datetime.now().isoformat(),
        'check_count': bot_status['health_checks']
    })

@app.route('/stats')
def stats():
    """Bot statistics endpoint"""
    uptime_seconds = 0
    if bot_status['start_time']:
        uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
    
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    uptime = f"{hours}h {minutes}m"
    
    return jsonify({
        'bot_name': 'Telegram Admin Bot',
        'version': '2.1.0',
        'status': 'operational' if bot_status['running'] else 'stopped',
        'uptime': uptime,
        'features': [
            'Admin Commands',
            'Moderation Tools', 
            'Fun Commands',
            'Information Commands',
            'Utility Tools'
        ],
        'health_checks': bot_status['health_checks'],
        'server_time': datetime.now().isoformat()
    })

def update_bot_status(running=True):
    """Update bot status"""
    bot_status['running'] = running
    if running and not bot_status['start_time']:
        bot_status['start_time'] = datetime.now()
    bot_status['last_update'] = datetime.now()

def run_bot():
    """Run the Telegram bot in a separate thread"""
    try:
        logger.info("Starting Telegram bot thread...")
        update_bot_status(True)
        
        # Import and run the main bot
        from main import main as run_telegram_bot
        run_telegram_bot()
        
    except Exception as e:
        logger.error(f"Bot thread error: {e}")
        update_bot_status(False)

def start_bot_thread():
    """Start bot in background thread"""
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started")
    return bot_thread

def keep_alive():
    """Keep-alive function to start Flask server"""
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting Flask keep-alive server on port {port}")
    logger.info(f"Health endpoint: http://localhost:{port}/health")
    logger.info(f"Status endpoint: http://localhost:{port}/")
    logger.info(f"Stats endpoint: http://localhost:{port}/stats")
    
    # Start bot in background
    start_bot_thread()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    keep_alive()