"""
Internal Keep-Alive System for Replit
This creates periodic activity to prevent hibernation without needing external access
"""

import threading
import time
import logging
import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

logger = logging.getLogger(__name__)

class InternalKeepAlive:
    def __init__(self):
        self.running = True
        self.ping_count = 0
        self.start_time = datetime.now()
        
    def self_ping(self):
        """Internal activity generator to maintain keep-alive"""
        while self.running:
            try:
                # Create file activity to keep system active
                self.ping_count += 1
                
                status_file = "keepalive_status.json"
                status = {
                    "last_activity": datetime.now().isoformat(),
                    "activity_count": self.ping_count,
                    "uptime_minutes": int((datetime.now() - self.start_time).total_seconds() / 60),
                    "status": "active"
                }
                
                with open(status_file, 'w') as f:
                    json.dump(status, f, indent=2)
                    
                logger.info(f"🔄 Keep-alive activity #{self.ping_count} - {datetime.now().strftime('%H:%M:%S')}")
                    
            except Exception as e:
                logger.warning(f"Keep-alive activity failed: {e}")
            
            # Wait 4 minutes between activities
            time.sleep(240)
    
    def start(self):
        """Start the internal keep-alive system"""
        logger.info("🔄 Starting internal keep-alive system...")
        
        # Start self-ping in background thread
        ping_thread = threading.Thread(target=self.self_ping, daemon=True)
        ping_thread.start()
        
        logger.info("✅ Internal keep-alive active - generating activity every 4 minutes")
        
        return ping_thread
    
    def stop(self):
        """Stop the keep-alive system"""
        self.running = False
        logger.info("🛑 Internal keep-alive stopped")

# Enhanced health handler with keep-alive info
class EnhancedHealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Read keep-alive status
                keepalive_info = {"activity_count": 0, "last_activity": None}
                try:
                    with open("keepalive_status.json", 'r') as f:
                        keepalive_info = json.load(f)
                except:
                    pass
                
                uptime_seconds = (datetime.now() - start_time).total_seconds()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                uptime = f"{hours}h {minutes}m"
                
                response = {
                    'status': 'healthy',
                    'bot_status': 'running',
                    'uptime': uptime,
                    'timestamp': datetime.now().isoformat(),
                    'keep_alive': {
                        'activity_count': keepalive_info.get('activity_count', 0),
                        'last_activity': keepalive_info.get('last_activity'),
                        'system': 'active'
                    },
                    'note': 'Bot running with internal keep-alive system'
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
                    'timestamp': datetime.now().isoformat(),
                    'keep_alive_system': 'Internal (no external URL needed)',
                    'note': 'Bot will stay active with internal keep-alive pings'
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Not found'}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP request logs to reduce noise"""
        pass

# Global variables
start_time = datetime.now()
keep_alive_system = None

def start_enhanced_server():
    """Start enhanced server with internal keep-alive"""
    global keep_alive_system
    
    def run_server():
        port = int(os.environ.get('PORT', 5000))
        server = HTTPServer(('0.0.0.0', port), EnhancedHealthHandler)
        
        logger.info(f"🌐 Enhanced health server starting on port {port}")
        logger.info(f"📍 Health endpoint: /health")
        logger.info(f"📊 Status endpoint: /")
        
        try:
            server.serve_forever()
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    # Start keep-alive system
    keep_alive_system = InternalKeepAlive()
    keep_alive_system.start()
    
    # Start server in daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    logger.info("✅ Enhanced server with internal keep-alive started")

if __name__ == '__main__':
    # Start enhanced server with keep-alive
    start_enhanced_server()
    
    # Import and run main bot
    logger.info("🤖 Starting Telegram Bot with Internal Keep-Alive...")
    from main import main
    main()