# Setting Up Slack Request URL with ngrok

## Problem
Slack requires a publicly accessible HTTPS URL. `localhost` or `http://` URLs won't work.

## Solution: Use ngrok (Free Tunnel)

### Step 1: Download ngrok
1. Go to https://ngrok.com/download
2. Download for Windows
3. Extract `ngrok.exe` to a folder (or add to PATH)

### Step 2: Start Your Flask Server
```bash
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
python layer1_slack_listener.py
```
The server will start on port 3000.

### Step 3: Start ngrok in a NEW terminal
```bash
ngrok http 3000
```

### Step 4: Copy the HTTPS URL
ngrok will display something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:3000
```

**Copy the HTTPS URL:** `https://abc123.ngrok.io`

### Step 5: Use in Slack
For **Event Subscriptions** Request URL:
```
https://abc123.ngrok.io/slack/events
```

For **Slash Command** Request URL:
```
https://abc123.ngrok.io/slack/commands
```

## Important Notes

⚠️ **Free ngrok URLs change each time you restart ngrok**
- Each time you restart ngrok, you get a new URL
- You'll need to update the URLs in Slack settings

💡 **Pro Tip**: Sign up for a free ngrok account and get a reserved domain:
1. Sign up at https://dashboard.ngrok.com/signup
2. Get your authtoken
3. Run: `ngrok authtoken YOUR_TOKEN`
4. Use reserved domain: `ngrok http 3000 --domain=your-reserved-domain`

## Alternative: Deploy to a Server

Instead of ngrok, you can deploy to:
- Heroku
- Railway
- Render
- AWS/DigitalOcean
- Any server with a public IP and HTTPS
