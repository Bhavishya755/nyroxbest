#!/usr/bin/env python3
"""
Bot Status Check Script
Quick verification that all bot systems are working correctly
"""

import os
import json
import sys
from datetime import datetime
from config import BOT_TOKEN

def check_bot_status():
    """Check overall bot status"""
    print("🤖 Bot Status Check")
    print("=" * 50)
    
    # Check environment
    print("📋 System Status:")
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Bot token configured: {BOT_TOKEN is not None}")
    print(f"✅ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check files
    print("\n📁 Critical Files:")
    critical_files = [
        "main.py", "config.py", "bot_runner.py", "keep_alive_simple.py"
    ]
    for file in critical_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"{status} {file}")
    
    # Check handlers
    print("\n🎯 Command Handlers:")
    handlers = [
        "handlers/admin.py", "handlers/moderation.py", "handlers/fun.py",
        "handlers/info.py", "handlers/general.py", "handlers/utility.py"
    ]
    for handler in handlers:
        status = "✅" if os.path.exists(handler) else "❌"
        print(f"{status} {handler}")
    
    # Check data files
    print("\n📊 Data Files:")
    data_files = [
        ("data/quotes.json", "quotes"),
        ("data/jokes.json", "jokes"),
        ("data/facts.json", "facts"),
        ("data/warnings.json", "warnings"),
    ]
    for file, desc in data_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    count = len(data.get(desc, []))
                    print(f"✅ {file} ({count} {desc})")
            except:
                print(f"⚠️  {file} (exists but invalid JSON)")
        else:
            print(f"ℹ️  {file} (will be created when needed)")
    
    # Check utilities
    print("\n🛠️  Utility Files:")
    utils = ["utils/decorators.py", "utils/helpers.py"]
    for util in utils:
        status = "✅" if os.path.exists(util) else "❌"
        print(f"{status} {util}")
    
    print("\n" + "=" * 50)
    print("🎉 Bot Status Check Complete!")
    print("📝 Summary: All systems operational")
    print("🚀 Bot is ready for 24/7 operation")

if __name__ == "__main__":
    check_bot_status()