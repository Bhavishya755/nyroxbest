"""
Keep-Alive HTTP Server for Telegram Bot
Uses Python's built-in http.server to avoid Flask dependency issues
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot status tracking
bot_status = {
    'running': False,
    'start_time': None,
    'last_update': None,
    'health_checks': 0
}

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                uptime = None
                if bot_status['start_time']:
                    uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
                    hours = int(uptime_seconds // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    uptime = f"{hours}h {minutes}m"
                
                response = {
                    'message': 'Bot is running!',
                    'status': 'online' if bot_status['running'] else 'offline',
                    'uptime': uptime,
                    'last_update': bot_status['last_update'].isoformat() if bot_status['last_update'] else None,
                    'health_checks': bot_status['health_checks'],
                    'timestamp': datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            elif self.path == '/health':
                bot_status['health_checks'] += 1
                bot_status['last_update'] = datetime.now()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'healthy',
                    'bot_running': bot_status['running'],
                    'timestamp': datetime.now().isoformat(),
                    'check_count': bot_status['health_checks']
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == '/stats':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                uptime_seconds = 0
                if bot_status['start_time']:
                    uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
                
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                uptime = f"{hours}h {minutes}m"
                
                response = {
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
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'error': 'Not found', 'available_endpoints': ['/', '/health', '/stats']}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Internal server error'}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Custom logging to reduce spam"""
        if '/health' not in format % args:  # Don't log health checks
            logger.info(f"HTTP {self.address_string()} - {format % args}")

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
        
        # Import and run the threaded bot
        from bot_threaded import run_bot_threaded
        run_bot_threaded()
        
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
    """Keep-alive function to start HTTP server"""
    port = int(os.environ.get('PORT', 5000))
    
    logger.info("=" * 50)
    logger.info("🚀 Starting Keep-Alive HTTP Server")
    logger.info("=" * 50)
    logger.info(f"Server running on port {port}")
    logger.info(f"Main endpoint: http://localhost:{port}/")
    logger.info(f"Health endpoint: http://localhost:{port}/health")
    logger.info(f"Stats endpoint: http://localhost:{port}/stats")
    logger.info("=" * 50)
    
    # Start bot in background thread
    start_bot_thread()
    
    # Add small delay to let bot initialize
    time.sleep(2)
    
    # Start HTTP server
    server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
    
    logger.info("✅ Server ready - Bot is now running 24/7!")
    logger.info("📍 For UptimeRobot, use: [your-replit-url]/health")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        server.shutdown()

if __name__ == '__main__':
    keep_alive()