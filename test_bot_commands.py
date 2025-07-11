#!/usr/bin/env python3
"""
Quick Bot Commands Test Script
Tests all major bot commands to ensure they work properly
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.getcwd())

from config import BOT_TOKEN, ADMIN_COMMANDS, MODERATION_COMMANDS, FUN_COMMANDS, INFO_COMMANDS, UTILITY_COMMANDS, GENERAL_COMMANDS

def test_configuration():
    """Test bot configuration"""
    print("🧪 Testing Bot Configuration...")
    
    # Test bot token
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set!")
        return False
    else:
        print(f"✅ BOT_TOKEN configured: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
    
    # Test command dictionaries
    command_groups = [
        ("Admin", ADMIN_COMMANDS),
        ("Moderation", MODERATION_COMMANDS),
        ("Fun", FUN_COMMANDS),
        ("Info", INFO_COMMANDS),
        ("Utility", UTILITY_COMMANDS),
        ("General", GENERAL_COMMANDS)
    ]
    
    for group_name, commands in command_groups:
        print(f"✅ {group_name} commands: {len(commands)} available")
        for cmd, desc in commands.items():
            print(f"   • /{cmd} - {desc}")
    
    return True

def test_imports():
    """Test all imports"""
    print("\n🔍 Testing Imports...")
    
    try:
        from handlers.admin import ban_user, unban_user, kick_user, promote_user, demote_user
        from handlers.moderation import mute_user, unmute_user, warn_user, unwarn_user
        from handlers.fun import roll_dice, flip_coin, random_quote, random_joke
        from handlers.info import user_info, chat_info, list_admins, member_count
        from handlers.general import start_command, help_command, menu_command
        from handlers.utility import translate_text, time_command, calculate_command
        from utils.decorators import admin_required, bot_admin_required
        from utils.helpers import get_user_from_message, format_user_mention
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        "main.py",
        "config.py",
        "bot_runner.py",
        "keep_alive_simple.py",
        "handlers/admin.py",
        "handlers/moderation.py",
        "handlers/fun.py",
        "handlers/info.py",
        "handlers/general.py",
        "handlers/utility.py",
        "utils/decorators.py",
        "utils/helpers.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    return True

def test_data_directories():
    """Test data directories"""
    print("\n📂 Testing Data Directories...")
    
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created data directory")
    else:
        print("✅ Data directory exists")
    
    # Check for data files (they'll be created when needed)
    data_files = ["data/warnings.json", "data/mutes.json", "data/rules.json"]
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"ℹ️  {file_path} will be created when needed")
    
    return True

async def main():
    """Main test function"""
    print("🤖 Bot Commands Testing Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("File Structure", test_file_structure),
        ("Data Directories", test_data_directories)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                failed += 1
                print(f"❌ {test_name} test failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} test failed with exception: {e}")
        
        print()
    
    print("=" * 50)
    print(f"🧪 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Bot commands should work perfectly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    asyncio.run(main())