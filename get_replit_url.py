#!/usr/bin/env python3
"""
Helper script to get your Replit URL for UptimeRobot setup
"""

import os
import requests
import time

def get_replit_url():
    """Get the current Replit URL"""
    # Try to get from environment variables
    replit_slug = os.environ.get('REPL_SLUG', 'your-repl')
    replit_owner = os.environ.get('REPL_OWNER', 'your-username')
    
    # Different possible URL formats
    possible_urls = [
        f"https://{replit_slug}.{replit_owner}.repl.co",
        f"https://{replit_slug}-{replit_owner}.repl.co",
        # Get from REPLIT_DOMAINS if available
        os.environ.get('REPLIT_DOMAINS', '').split(',')[0] if os.environ.get('REPLIT_DOMAINS') else None
    ]
    
    print("🔍 Detecting your Replit URL...")
    print(f"📝 Repl: {replit_slug}")
    print(f"👤 Owner: {replit_owner}")
    print()
    
    for url in possible_urls:
        if url and url.startswith('http'):
            print(f"🌐 Possible URL: {url}")
    
    # Try to detect from REPLIT_DOMAINS
    domains = os.environ.get('REPLIT_DOMAINS', '')
    if domains:
        domain = domains.split(',')[0]
        if domain:
            full_url = f"https://{domain}"
            print(f"✅ Found URL from REPLIT_DOMAINS: {full_url}")
            return full_url
    
    # Fallback
    fallback_url = f"https://{replit_slug}.{replit_owner}.repl.co"
    print(f"🔄 Using fallback URL: {fallback_url}")
    return fallback_url

def test_health_endpoint():
    """Test the health endpoint"""
    base_url = get_replit_url()
    health_url = f"{base_url}/health"
    
    print("\n" + "="*50)
    print("🏥 TESTING HEALTH ENDPOINT")
    print("="*50)
    print(f"Testing: {health_url}")
    
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ SUCCESS! Health endpoint is working")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ ERROR: Got status code {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("\n💡 This might mean:")
        print("   - Your Repl isn't publicly accessible yet")
        print("   - You need to deploy your Repl first")
        print("   - The URL format might be different")
    
    print("\n" + "="*50)
    print("📋 FOR UPTIMEROBOT SETUP:")
    print("="*50)
    print(f"🎯 Monitor URL: {health_url}")
    print("⚙️  Monitor Type: HTTP(s)")
    print("⏰ Interval: 5 minutes")
    print("🔄 Method: GET")
    print("✅ Expected Status: 200")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Replit URL Detection Tool")
    print("="*50)
    
    # Show environment info
    print("📋 Environment Variables:")
    for key in ['REPL_SLUG', 'REPL_OWNER', 'REPLIT_DOMAINS']:
        value = os.environ.get(key, 'Not set')
        print(f"   {key}: {value}")
    
    print("\n")
    test_health_endpoint()
    
    print("\n💡 Quick Steps:")
    print("1. Copy the Monitor URL above")
    print("2. Go to uptimerobot.com and create account")
    print("3. Add new HTTP monitor with that URL")
    print("4. Set interval to 5 minutes")
    print("5. Your bot will stay alive 24/7!")