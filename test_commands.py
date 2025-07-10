#!/usr/bin/env python3
"""
Command Reliability Test Script for Telegram Bot
Tests all major commands to ensure they respond correctly
"""

import asyncio
import logging
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes
from unittest.mock import Mock, AsyncMock
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import handlers
from handlers.general import start_command, help_command, test_command
from handlers.fun import roll_dice, flip_coin, random_quote
from handlers.admin import ban_user, kick_user
from handlers.moderation import warn_user, mute_user
from handlers.info import user_info, chat_info

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockBot:
    """Mock bot for testing"""
    def __init__(self):
        self.id = 123456789
        
    async def get_chat_member(self, chat_id, user_id):
        # Mock admin user
        mock_member = Mock()
        mock_member.status = 'administrator'
        mock_member.user = Mock()
        mock_member.user.id = user_id
        mock_member.user.first_name = "Test User"
        mock_member.user.username = "testuser"
        return mock_member
        
    async def get_chat_administrators(self, chat_id):
        mock_admin = Mock()
        mock_admin.user = Mock()
        mock_admin.user.id = 987654321
        mock_admin.user.username = "testadmin"
        mock_admin.user.first_name = "Test Admin"
        return [mock_admin]

def create_mock_update(command_text="/start", user_id=987654321, chat_id=-1001234567890):
    """Create a mock update object for testing"""
    # Create mock user
    user = Mock(spec=User)
    user.id = user_id
    user.first_name = "Test"
    user.username = "testuser"
    user.is_bot = False
    
    # Create mock chat
    chat = Mock(spec=Chat)
    chat.id = chat_id
    chat.type = "supergroup"
    chat.title = "Test Group"
    
    # Create mock message
    message = Mock(spec=Message)
    message.text = command_text
    message.from_user = user
    message.chat = chat
    message.reply_to_message = None
    message.date = asyncio.get_event_loop().time()
    message.reply_text = AsyncMock()
    
    # Create mock update
    update = Mock(spec=Update)
    update.message = message
    update.effective_user = user
    update.effective_chat = chat
    
    return update

def create_mock_context(args=None):
    """Create a mock context object for testing"""
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = args or []
    context.bot = MockBot()
    return context

async def test_command(command_func, command_name, *args, **kwargs):
    """Test a single command function"""
    try:
        logger.info(f"Testing {command_name}...")
        
        update = create_mock_update(*args, **kwargs)
        context = create_mock_context()
        
        # Run the command
        await command_func(update, context)
        
        # Check if reply_text was called
        if update.message.reply_text.called:
            logger.info(f"✅ {command_name} - Command executed successfully")
            return True
        else:
            logger.warning(f"⚠️ {command_name} - Command didn't send a response")
            return False
            
    except Exception as e:
        logger.error(f"❌ {command_name} - Error: {e}")
        return False

async def run_reliability_test():
    """Run comprehensive command reliability test"""
    logger.info("🚀 Starting Command Reliability Test")
    logger.info("=" * 50)
    
    test_results = {}
    
    # Test general commands
    logger.info("📋 Testing General Commands...")
    test_results['start'] = await test_command(start_command, "/start")
    test_results['help'] = await test_command(help_command, "/help")
    test_results['test'] = await test_command(test_command, "/test")
    
    # Test fun commands
    logger.info("🎮 Testing Fun Commands...")
    test_results['dice'] = await test_command(roll_dice, "/dice")
    test_results['coin'] = await test_command(flip_coin, "/coin")
    test_results['quote'] = await test_command(random_quote, "/quote")
    
    # Test info commands
    logger.info("📊 Testing Info Commands...")
    test_results['user_info'] = await test_command(user_info, "/user")
    test_results['chat_info'] = await test_command(chat_info, "/chatinfo")
    
    # Test moderation commands (with proper context)
    logger.info("🛡️ Testing Moderation Commands...")
    context_with_args = create_mock_context(args=["987654321", "test reason"])
    
    # These require special handling due to decorators
    try:
        update = create_mock_update("/warn")
        await warn_user(update, context_with_args)
        test_results['warn'] = True
        logger.info("✅ /warn - Command executed successfully")
    except Exception as e:
        test_results['warn'] = False
        logger.error(f"❌ /warn - Error: {e}")
    
    # Test admin commands
    logger.info("👑 Testing Admin Commands...")
    try:
        update = create_mock_update("/ban")
        await ban_user(update, context_with_args)
        test_results['ban'] = True
        logger.info("✅ /ban - Command executed successfully")
    except Exception as e:
        test_results['ban'] = False
        logger.error(f"❌ /ban - Error: {e}")
    
    # Calculate success rate
    logger.info("=" * 50)
    logger.info("📊 Test Results Summary:")
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    success_rate = (passed / total) * 100
    
    for command, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {command}: {status}")
    
    logger.info(f"\n🎯 Overall Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        logger.info("🎉 Command reliability test PASSED!")
        return True
    else:
        logger.warning("⚠️ Command reliability test needs improvement")
        return False

if __name__ == "__main__":
    asyncio.run(run_reliability_test())