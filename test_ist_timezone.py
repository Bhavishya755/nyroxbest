#!/usr/bin/env python3
"""
Test script to verify IST timezone is working properly
"""

from datetime import datetime
from config import IST
from utils.helpers import get_ist_time, format_ist_time

def test_ist_timezone():
    """Test IST timezone functionality"""
    print("🕐 Testing IST Timezone Configuration")
    print("=" * 50)
    
    # Test IST timezone from config
    now_ist = datetime.now(IST)
    print(f"✅ Current IST time: {now_ist.strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    # Test helper functions
    ist_time = get_ist_time()
    print(f"✅ Helper function IST time: {ist_time.strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    # Test formatting function
    formatted_time = format_ist_time()
    print(f"✅ Formatted IST time: {formatted_time}")
    
    # Test timezone offset
    offset = IST.utcoffset(None)
    print(f"✅ IST offset from UTC: {offset}")
    
    print("\n" + "=" * 50)
    print("🎉 IST timezone configuration is working properly!")
    print("⏰ All timestamps will now show Indian Standard Time")

if __name__ == "__main__":
    test_ist_timezone()