"""
Simple Keep-Alive Server for 24/7 Bot Operation
This creates a minimal web server that keeps the Replit running continuously
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle all GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Bot is ALIVE - {current_time}"
        self.wfile.write(message.encode())
    
    def log_message(self, format, *args):
        """Suppress request logs"""
        pass

def start_server():
    """Start the keep-alive server"""
    try:
        port = 5000
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        logger.info(f"Keep-alive server started on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Server error: {e}")
        # Retry after 5 seconds
        time.sleep(5)
        start_server()

def keep_alive():
    """Start keep-alive server in background thread"""
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give server time to start
    time.sleep(2)
    logger.info("✅ Keep-alive system active")

if __name__ == '__main__':
    keep_alive()
    input("Press Enter to stop...")