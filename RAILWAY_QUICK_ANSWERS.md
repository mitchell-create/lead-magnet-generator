# Railway Quick Answers

## 1. How to Check if Using `python layer1_slack_listener.py`

### Method 1: Check Logs (Easiest)

1. In Railway, go to your service
2. Click **"Deployments"** tab
3. Click on the **latest deployment**
4. Click **"View Logs"** or **"Logs"**
5. Look for:
   ```
   Starting Slack listener on port 3000
   ```
   If you see this, it's using the correct command! ✅

### Method 2: Check railway.toml

Since we created `railway.toml` with the start command, Railway should be using it automatically.

**To verify:**
1. In Railway service, go to **"Settings"** tab
2. Look for **"Start Command"** or **"Deploy"** section
3. Should show: `python layer1_slack_listener.py`

### Method 3: Check Deployment Logs

In the deployment logs, you should see:
- Python installing dependencies
- Then running: `python layer1_slack_listener.py`

---

## 2. Bulk Add API Keys

### Option 1: Railway UI (One by One)

Unfortunately, Railway's UI requires adding variables one by one. But it's quick!

**Quick tip:** Copy-paste these in order:

```
PROSPEO_API_KEY=pk_18aa056cf585e436de7ad62b3ccd7baf1ad9e633b7e403aa5f9a35ff7fb3b01d
OPENROUTER_API_KEY=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
SUPABASE_URL=https://utdwvqfnzkcysdsbsvwv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0ZHd2cWZuemtjeXNkc2Jzdnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODc4NDk4OCwiZXhwIjoyMDg0MzYwOTg4fQ.tfYTjn7z0lbEJx7NnGeivyDPUrbqFHwOy0RgcO4IERs
SLACK_BOT_TOKEN=xoxb-3507979379937-10326210258854-Cm4WgC7tdXuW1k4XgeY7fueD
SLACK_SIGNING_SECRET=e162fc8db05db56d9d6b20a1c23d5d04
SLACK_PORT=3000
SLACK_CHANNEL_ID=C0A9N873LAE
OUTPUT_DIR=./output
```

For each one:
1. Click "New Variable"
2. Copy the key name (left side of =)
3. Paste as "Key"
4. Copy the value (right side of =)
5. Paste as "Value"
6. Click "Add"

### Option 2: Railway CLI (Advanced)

If you have Railway CLI installed, you can bulk import, but the UI method is usually faster for 9 variables.

---

## 3. Domain Questions

### Is it Public?

**Yes!** Railway domains are:
- ✅ Publicly accessible
- ✅ HTTPS (secure)
- ✅ No authentication required
- ✅ Anyone with the URL can access it

**But:** Only if they know the URL. Railway domains are long and random, so they're not easily guessable.

### What Port Number?

**No port number needed!** 

Railway handles this automatically:
- **External:** Railway domain uses HTTPS (port 443) - you don't specify
- **Internal:** Your app runs on port 3000 (as set in SLACK_PORT)
- **Railway routes:** Automatically routes external HTTPS → your app's port 3000

**For Slack URLs, use:**
```
https://your-domain.up.railway.app/slack/events
https://your-domain.up.railway.app/slack/commands
```

**No port number in the URL!** ✅

---

## Quick Reference

**Domain format:**
```
https://lead-magnet-generator-production-xxxx.up.railway.app
```

**Slack URLs (no port):**
```
https://your-domain.up.railway.app/slack/events
https://your-domain.up.railway.app/slack/commands
```

**Your app runs on:** Port 3000 internally (handled automatically)

---

## Summary

1. **Check start command:** View deployment logs
2. **Bulk add keys:** One by one in UI (takes 2 minutes)
3. **Domain:** Public HTTPS, no port number needed
