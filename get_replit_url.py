#!/usr/bin/env python3
"""
Helper script to get your Replit URL for UptimeRobot setup
"""

import os
import json

def get_replit_url():
    """Get the current Replit URL"""
    
    # Method 1: Check environment variables
    domain = os.environ.get('REPLIT_DOMAIN')
    if domain:
        url = f"https://{domain}"
        print(f"🌐 Your Replit URL: {url}")
        print(f"📍 Health endpoint: {url}/health")
        print(f"📊 Status endpoint: {url}/")
        return url
    
    # Method 2: Try to detect from current request
    replit_url = os.environ.get('REPLIT_URL')
    if replit_url:
        print(f"🌐 Your Replit URL: {replit_url}")
        print(f"📍 Health endpoint: {replit_url}/health")
        print(f"📊 Status endpoint: {replit_url}/")
        return replit_url
    
    # Method 3: Check for other Replit environment variables
    replit_id = os.environ.get('REPLIT_ID')
    if replit_id:
        print(f"🆔 Replit ID: {replit_id}")
        print("💡 Your URL will be something like:")
        print(f"   https://your-long-id.repl.co")
    
    print("\n📝 To find your URL:")
    print("1. Look at your Replit's webview panel")
    print("2. Copy the URL from the address bar")
    print("3. Add '/health' at the end for UptimeRobot")
    
    return None

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        import urllib.request
        import urllib.error
        
        with urllib.request.urlopen('http://localhost:5000/health') as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                print(f"✅ Health endpoint working!")
                print(f"📊 Status: {data.get('status')}")
                print(f"🤖 Bot Status: {data.get('bot_status')}")
                print(f"⏱️ Uptime: {data.get('uptime')}")
                print(f"🔄 Health Checks: {data.get('check_count')}")
            else:
                print(f"❌ Health endpoint returned status: {response.getcode()}")
    except Exception as e:
        print(f"❌ Could not test health endpoint: {e}")

if __name__ == "__main__":
    print("🔍 Finding your Replit URL for UptimeRobot setup...\n")
    
    # Test local health endpoint first
    test_health_endpoint()
    print()
    
    # Get Replit URL
    url = get_replit_url()
    
    print("\n" + "="*50)
    print("📋 UptimeRobot Setup Instructions:")
    print("="*50)
    print("1. Go to uptimerobot.com and create free account")
    print("2. Click '+ Add New Monitor'")
    print("3. Monitor Type: HTTP(s)")
    print("4. URL: [Your Replit URL]/health")
    print("5. Interval: 5 minutes")
    print("6. Create monitor")
    print("\n✅ Your bot will stay alive 24/7!")