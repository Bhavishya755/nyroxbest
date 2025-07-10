# UptimeRobot Setup Guide

## Step 1: Get Your Replit URL
1. Once your server is running, your Replit will have a URL like:
   ```
   https://your-repl-name.your-username.repl.co
   ```
2. The health endpoint will be:
   ```
   https://your-repl-name.your-username.repl.co/health
   ```

## Step 2: Create UptimeRobot Account
1. Go to [https://uptimerobot.com](https://uptimerobot.com)
2. Sign up for a free account
3. Verify your email address

## Step 3: Add Monitor
1. Click **"+ Add New Monitor"**
2. **Monitor Type**: HTTP(s)
3. **Friendly Name**: "Telegram Bot - Your Bot Name"
4. **URL**: `https://your-repl-name.your-username.repl.co/health`
5. **Monitoring Interval**: 5 minutes
6. **Monitor Timeout**: 30 seconds
7. **HTTP Method**: GET
8. Click **"Create Monitor"**

## Step 4: Configure Alerts (Optional)
1. In your monitor settings, click **"Alert Contacts"**
2. Add your email for downtime notifications
3. Set alert thresholds:
   - Send alert when DOWN
   - Send alert when UP (recovery)

## Step 5: Verify Setup
1. After creating the monitor, wait 5-10 minutes
2. Check if UptimeRobot shows your bot as "Up"
3. Visit your health endpoint to see increasing check counts

## Free Plan Limits
- Up to 50 monitors
- 5-minute monitoring interval
- Email alerts included
- 2-month log retention

## URLs to Monitor
- **Health Check**: `/health` - Main monitoring endpoint
- **Bot Status**: `/` - General status information  
- **Statistics**: `/stats` - Detailed bot statistics

## Expected Response
Your health endpoint should return:
```json
{
  "status": "healthy",
  "bot_status": "running", 
  "timestamp": "2025-07-10T22:59:39.123456",
  "check_count": 123
}
```

## Troubleshooting
- If UptimeRobot shows "Down", check your Replit console for errors
- Ensure your Flask server is binding to `0.0.0.0:5000`
- Verify the health endpoint returns HTTP 200 status
- Check Replit's "Always On" feature is enabled (Hacker plan required)

## Notes
- UptimeRobot will ping every 5 minutes automatically
- This keeps your Replit active and prevents hibernation
- Your Telegram bot will stay online 24/7
- Monitor logs will show uptime statistics