# Fix: Flask Not Accessible

## Problem

Flask is running on `127.0.0.1:3000` which is **localhost only** - not accessible from outside the container.

**Error in logs:**
```
Running on http://127.0.0.1:3000
```

This means Railway can't route traffic to your app!

## Fix Applied

Changed Flask to bind to `0.0.0.0` instead of `127.0.0.1`:
- `0.0.0.0` = Listen on all network interfaces (accessible from outside)
- Also uses Railway's `PORT` environment variable (Railway might set a different port)

## Changes Made

Updated `layer1_slack_listener.py`:
```python
flask_app.run(host='0.0.0.0', port=port, debug=False)
```

## Next Steps

### Step 1: Commit and Push

Run in PowerShell:
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git add layer1_slack_listener.py
git commit -m "Fix: Bind Flask to 0.0.0.0 for Railway"
git push
```

### Step 2: Wait for Redeployment

Railway will automatically redeploy (2-3 minutes).

### Step 3: Check Logs

After redeployment, logs should show:
```
Running on http://0.0.0.0:3000
```

### Step 4: Test Endpoints

Test in browser:
- Health: `https://lead-magnet-generator-production.up.railway.app/health`
- Should respond with JSON now! ✅

### Step 5: Try Slack URL Again

Go back to Slack → Event Subscriptions and try the URL verification again.

## Why This Happens

Flask's default is `127.0.0.1` (localhost), which only works on the same machine. For containers/cloud, it needs `0.0.0.0` to be accessible externally.
