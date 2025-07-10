"""
Simplified approach: Run bot directly and add health endpoint
"""

import json
import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot status tracking
health_checks = 0
start_time = datetime.now()

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global health_checks
        """Handle GET requests"""
        try:
            if self.path == '/health':
                health_checks += 1
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                uptime_seconds = (datetime.now() - start_time).total_seconds()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                uptime = f"{hours}h {minutes}m"
                
                response = {
                    'status': 'healthy',
                    'bot_status': 'running',
                    'uptime': uptime,
                    'timestamp': datetime.now().isoformat(),
                    'check_count': health_checks
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == '/' or self.path == '/status':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                uptime_seconds = (datetime.now() - start_time).total_seconds()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                uptime = f"{hours}h {minutes}m"
                
                response = {
                    'bot_name': 'Telegram Admin Bot',
                    'status': 'online',
                    'uptime': uptime,
                    'health_checks': health_checks,
                    'timestamp': datetime.now().isoformat(),
                    'endpoints': {
                        'health': '/health',
                        'status': '/',
                        'uptimerobot': 'Use /health endpoint'
                    }
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Not found', 'available_endpoints': ['/health', '/']}
                self.wfile.write(json.dumps(response).encode())
                
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
        
        logger.info(f"🌐 Health server starting on port {port}")
        logger.info(f"📍 Health endpoint: /health")
        logger.info(f"📊 Status endpoint: /")
        
        try:
            server.serve_forever()
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    # Start server in daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Let server start
    logger.info("✅ Health server started")

if __name__ == '__main__':
    # Start health server
    start_health_server()
    
    # Import and run main bot
    logger.info("🤖 Starting Telegram Bot...")
    from main import main
    main()