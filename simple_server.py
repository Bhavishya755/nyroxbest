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
                # HTML dashboard for easy monitoring
                uptime_seconds = (datetime.now() - bot_status['start_time']).total_seconds()
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Telegram Bot Status</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .status-online {{
            color: #22c55e;
            font-weight: bold;
        }}
        .metric {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #22c55e;
        }}
        .metric-title {{
            font-weight: bold;
            color: #333;
        }}
        .metric-value {{
            font-size: 1.2em;
            margin-top: 5px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            text-align: center;
            margin-top: 20px;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }}
        .feature {{
            background: #e0f2fe;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }}
    </style>
    <script>
        setTimeout(function(){{
            location.reload();
        }}, 30000); // Auto-refresh every 30 seconds
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Telegram Admin Bot</h1>
            <h2 class="status-online">🟢 ONLINE & RUNNING</h2>
        </div>
        
        <div class="metric">
            <div class="metric-title">⏱️ Uptime</div>
            <div class="metric-value">{hours}h {minutes}m</div>
        </div>
        
        <div class="metric">
            <div class="metric-title">🔍 Health Checks</div>
            <div class="metric-value">{bot_status['health_checks']}</div>
        </div>
        
        <div class="metric">
            <div class="metric-title">📅 Started</div>
            <div class="metric-value">{bot_status['start_time'].strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="metric">
            <div class="metric-title">🔧 Features Available</div>
            <div class="features">
                <div class="feature">👑 Admin Commands</div>
                <div class="feature">🛡️ Moderation Tools</div>
                <div class="feature">🎮 Fun Commands</div>
                <div class="feature">📊 Info Commands</div>
                <div class="feature">🛠️ Utility Tools</div>
            </div>
        </div>
        
        <div class="metric">
            <div class="metric-title">🌐 API Endpoints</div>
            <div style="font-family: monospace; margin-top: 10px;">
                <div>GET / - Dashboard (this page)</div>
                <div>GET /health - Health check for UptimeRobot</div>
                <div>GET /stats - JSON statistics</div>
            </div>
        </div>
        
        <div class="timestamp">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
            Auto-refresh every 30 seconds
        </div>
    </div>
</body>
</html>
                """
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(html_content.encode())
                return
            elif self.path == '/health':
                # Simple text response for UptimeRobot monitoring
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                health_message = f"OK - Bot is running - Uptime: {int((datetime.now() - bot_status['start_time']).total_seconds() // 3600)}h {int(((datetime.now() - bot_status['start_time']).total_seconds() % 3600) // 60)}m - Checks: {bot_status['health_checks']}"
                self.wfile.write(health_message.encode())
                return
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