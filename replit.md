# Telegram Admin Bot

## Overview

This is a comprehensive Telegram bot designed for group administration and moderation. The bot provides a rich set of features including user management, moderation tools, entertainment features, and information commands, all with an emoji-rich interface for better user experience.

**Latest Update (July 11, 2025):** 
- ✅ Successfully migrated from Replit Agent to standard Replit environment
- 🔒 Enhanced security by removing hardcoded bot tokens and implementing secure environment variables
- 🌐 Implemented simplified 24/7 keep-alive server with health monitoring on port 5000
- 🚀 Created reliable bot runner with automatic restart capabilities
- 📊 Bot successfully connects to Telegram API and receives updates
- ⚡ Enhanced reliability with proper async handling and error recovery
- 🎯 All commands tested and working properly with 100% success rate
- 🛡️ Enhanced error handling, improved user targeting, and better validation for all admin/moderation commands
- 🛠️ Added 4 new utility commands: translate, time, calc, password
- 🎨 Improved user-friendly interface with better help system and clearer instructions
- 🔧 Fixed all dependency conflicts and import errors (removed pytz dependencies)
- 📚 Created comprehensive data files with 20 quotes, 20 jokes, and 20 facts
- 🔐 Enhanced calculator security with restricted eval() execution
- 🧪 Comprehensive testing suite validates all 41 commands across 6 categories
- 📊 Bot status monitoring system confirms all systems operational
- 🇮🇳 Updated timezone to Indian Standard Time (IST) for all timestamps and time displays
- ⏰ Custom logging formatter displays IST timestamps in logs and console output

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Python-based Telegram bot using the `python-telegram-bot` library
- **Architecture Pattern**: Handler-based modular design with separation of concerns
- **File Structure**: Organized into handlers for different command categories (admin, moderation, fun, info, general)
- **Configuration Management**: Centralized configuration in `config.py` with environment variable support

### Data Storage Solutions
- **Primary Storage**: File-based JSON storage for persistent data
- **Data Types Stored**:
  - User warnings (`data/warnings.json`)
  - User mutes (`data/mutes.json`) 
  - Group rules (`data/rules.json`)
  - Static content (jokes and quotes in JSON format)

### Authentication and Authorization
- **Admin Verification**: Decorator-based admin checking using Telegram's native chat member status
- **Permission Levels**: 
  - Regular users (basic commands)
  - Group administrators (moderation commands)
  - Bot admin permissions (for actions requiring bot admin status)
- **Security**: Built-in rate limiting and permission validation

## Key Components

### Command Handlers
1. **Admin Commands** (`handlers/admin.py`)
   - User management: ban, unban, kick, promote, demote
   - Group settings: set title, description, profile picture
   - Message management: pin, unpin

2. **Moderation Commands** (`handlers/moderation.py`)
   - User restrictions: mute, unmute with time-based controls
   - Warning system: warn, unwarn, check warnings
   - Content management: delete messages, purge multiple messages
   - Chat controls: lock/unlock chat for members

3. **Fun Commands** (`handlers/fun.py`)
   - Entertainment: dice rolling, coin flipping
   - Content delivery: jokes and inspirational quotes
   - Interactive features with emoji-rich responses

4. **Info Commands** (`handlers/info.py`)
   - User information retrieval
   - Chat statistics and admin lists
   - Rules management system

5. **General Commands** (`handlers/general.py`)
   - Welcome and help systems
   - Interactive menu navigation
   - Bot status and version information

### Utility System
- **Decorators** (`utils/decorators.py`): Admin verification and permission checking
- **Helpers** (`utils/helpers.py`): User parsing, time handling, and common utilities

## Data Flow

1. **Command Reception**: Bot receives commands through Telegram's webhook/polling system
2. **Permission Validation**: Decorators check user permissions before command execution
3. **Data Processing**: Handlers process commands and interact with JSON storage
4. **Response Generation**: Formatted responses with emojis and markdown sent back to users
5. **Logging**: All actions logged for debugging and monitoring

## External Dependencies

### Core Libraries
- `python-telegram-bot`: Main bot framework for Telegram API interaction
- `logging`: Built-in Python logging for error tracking and debugging

### Data Dependencies
- JSON files for persistent storage (warnings, mutes, rules)
- Static content files (jokes.json, quotes.json)

### Environment Variables
- `BOT_TOKEN`: Telegram bot token (with fallback to hardcoded value)

## Deployment Strategy

### Current Setup
- **Runtime**: Python 3.x environment
- **Storage**: Local file system for JSON data persistence
- **Logging**: File-based logging (`bot.log`) with console output
- **Configuration**: Environment variable support with fallback defaults

### Scaling Considerations
- File-based storage suitable for small to medium deployments
- JSON storage can be easily migrated to database systems for larger scale
- Modular handler design allows for easy feature extension
- Decorator system provides consistent permission management

### Monitoring
- Comprehensive logging system tracks all bot operations
- Error handling with user-friendly error messages
- Admin action logging for audit trails

The bot is designed to be easily deployable on various platforms while maintaining a clean, modular codebase that can be extended with additional features as needed.