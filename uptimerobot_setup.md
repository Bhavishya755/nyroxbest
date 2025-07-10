# UptimeRobot Setup Guide for Replit Development Environment

## Your Current Setup Status
✅ Bot is running and responding to commands
✅ Health server active on port 5000 
✅ Keep-alive endpoints working properly

## Getting Your Replit URL

### Option 1: Use Replit's Built-in URL (Recommended)
1. Look at your Replit's web view panel
2. Your URL will be something like: `https://46b8a09e-bff5-4893-852b-5944a5b0cf27-00-19d3zbcqmgxy4.kirk.repl.co`
3. This is your bot's URL - it's already available!

### Option 2: Share Your Replit Publicly
1. Click the **"Share"** button in the top right
2. Toggle **"Publish to Community Gallery"** ON
3. This will give you a cleaner URL like: `https://your-repl-name.your-username.repl.co`

## UptimeRobot Configuration

### Step 1: Create UptimeRobot Account
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up for free account
3. Verify your email

### Step 2: Add Bot Monitor
1. Click **"+ Add New Monitor"**
2. **Monitor Type**: `HTTP(s)`
3. **Friendly Name**: `Telegram Bot Keep-Alive`
4. **URL**: `https://your-repl-url/health`
   - Use the URL from your Replit webview
   - Add `/health` at the end
5. **Monitoring Interval**: `5 minutes`
6. **Monitor Timeout**: `30 seconds`
7. **HTTP Method**: `GET`
8. Click **"Create Monitor"**

### Step 3: Verify Setup
1. Check that UptimeRobot shows your monitor as "Up" (green)
2. You should see successful pings every 5 minutes
3. Your bot will stay active due to regular HTTP requests

## Your Health Endpoint Response
When UptimeRobot pings your `/health` endpoint, it will receive:
```json
{
  "status": "healthy",
  "bot_status": "running",
  "uptime": "0h 15m",
  "timestamp": "2025-07-10T23:05:17.216878",
  "check_count": 3
}
```

## Finding Your Replit URL

### Method 1: From Webview
- Look at the URL bar in your Replit's webview
- Copy the full URL (it's quite long but works perfectly)

### Method 2: From Console
- Look for any network requests in your console logs
- The base URL will be shown there

### Method 3: Environment Variable
- Your Replit automatically sets the `REPLIT_DOMAIN` environment variable
- Use: `https://${REPLIT_DOMAIN}`

## How It Works
1. **UptimeRobot** sends HTTP GET request to your `/health` endpoint every 5 minutes
2. **Your health server** responds with bot status and uptime data
3. **Replit** sees the regular traffic and keeps your app active
4. **Your bot** continues running 24/7 without hibernation

## Important Notes
- Your bot is already configured and ready for UptimeRobot
- The health endpoint is working perfectly
- You just need to find your Replit URL and add it to UptimeRobot
- Free UptimeRobot accounts get 50 monitors and 5-minute intervals
- This setup will significantly reduce hibernation on Replit's free tier

## Troubleshooting
If UptimeRobot shows "Down":
1. Check your Replit console for errors
2. Verify the health endpoint returns HTTP 200
3. Make sure the URL is correct with `/health` at the end
4. Test the URL directly in your browser first

Your bot is ready for 24/7 operation with UptimeRobot monitoring!