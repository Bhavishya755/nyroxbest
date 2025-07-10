"""
Simplified approach: Run bot directly and add health endpoint
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import logging
import os
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot status tracking
bot_status = {
    'running': False,
    'start_time': datetime.now(),
    'last_update': datetime.now(),
    'health_checks': 0
}

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            bot_status['health_checks'] += 1
            bot_status['last_update'] = datetime.now()
            
            if self.path == '/':
                response = {
                    'message': 'Bot is running!',
                    'status': 'online',
                    'uptime': f"{int((datetime.now() - bot_status['start_time']).total_seconds() // 3600)}h {int(((datetime.now() - bot_status['start_time']).total_seconds() % 3600) // 60)}m",
                    'health_checks': bot_status['health_checks'],
                    'timestamp': datetime.now().isoformat()
                }
            elif self.path == '/health':
                response = {
                    'status': 'healthy',
                    'bot_running': True,
                    'timestamp': datetime.now().isoformat(),
                    'check_count': bot_status['health_checks']
                }
            elif self.path == '/stats':
                uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                
                response = {
                    'bot_name': 'Telegram Admin Bot',
                    'version': '2.1.0',
                    'status': 'operational',
                    'uptime': f"{hours}h {minutes}m",
                    'features': ['Admin Commands', 'Moderation Tools', 'Fun Commands', 'Information Commands', 'Utility Tools'],
                    'health_checks': bot_status['health_checks'],
                    'server_time': datetime.now().isoformat()
                }
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Not found'}
                self.wfile.write(json.dumps(response).encode())
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP request logs to reduce noise"""
        pass

def start_health_server():
    """Start health check server in background"""
    def run_server():
        port = int(os.environ.get('PORT', 5000))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        logger.info(f"✅ Health server running on port {port}")
        logger.info(f"🌐 Main: http://localhost:{port}/")
        logger.info(f"🏥 Health: http://localhost:{port}/health")
        logger.info(f"📊 Stats: http://localhost:{port}/stats")
        server.serve_forever()
    
    health_thread = threading.Thread(target=run_server, daemon=True)
    health_thread.start()
    time.sleep(3)  # Give server more time to bind to port

def keep_alive():
    """Keep-alive function"""
    logger.info("🚀 Starting Keep-Alive Server...")
    start_health_server()
    logger.info("📍 For UptimeRobot, use: [your-replit-url]/health")

if __name__ == '__main__':
    keep_alive()
    # Import and run main bot directly
    from main import main
    main()