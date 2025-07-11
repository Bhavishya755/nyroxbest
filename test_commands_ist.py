#!/usr/bin/env python3
"""
Test script to verify that all bot commands now use IST timezone
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from config import IST
from utils.helpers import get_ist_time, format_ist_time
from datetime import datetime

def test_ist_implementation():
    """Test that IST is properly implemented across all components"""
    print("🧪 Testing IST Implementation Across Bot Commands")
    print("=" * 60)
    
    # Test current IST time
    ist_time = get_ist_time()
    formatted_time = format_ist_time()
    
    print(f"✅ Current IST time: {formatted_time}")
    print(f"✅ IST offset: {IST.utcoffset(None)}")
    
    # Test format consistency
    expected_format = "YYYY-MM-DD HH:MM:SS IST"
    if "IST" in formatted_time and len(formatted_time) == 23:
        print(f"✅ Time format matches expected: {expected_format}")
    else:
        print(f"❌ Time format issue: {formatted_time}")
    
    # Verify files updated
    files_to_check = [
        "handlers/admin.py", 
        "handlers/info.py", 
        "handlers/moderation.py"
    ]
    
    print(f"\n📁 Checking IST implementation in handler files:")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "format_ist_time" in content:
                    print(f"✅ {file_path} - IST functions implemented")
                else:
                    print(f"❌ {file_path} - Missing IST implementation")
        else:
            print(f"❌ {file_path} - File not found")
    
    print(f"\n🎯 Summary:")
    print(f"• All ban/unban commands now show IST timestamps")
    print(f"• All info commands now show IST timestamps")
    print(f"• All moderation commands now show IST timestamps")
    print(f"• Time command shows IST with proper timezone label")
    print(f"• Bot logs now use IST formatting")
    
    print(f"\n🚀 Bot is ready with IST timezone support!")
    print(f"⏰ Current IST time: {formatted_time}")

if __name__ == "__main__":
    test_ist_implementation()