# Fix: App Not Starting Server

## Problem Found

The app was running **test code** instead of starting the Flask server!

**What was happening:**
- Railway ran: `python layer1_slack_listener.py`
- The script executed test code (parser tests)
- Flask server never started
- So Slack couldn't reach the app

## Fix Applied

I've updated the code to:
1. Check if `--server` flag is passed
2. Check if running in Railway (via environment variable)
3. If either is true → Start Flask server
4. Otherwise → Run tests (for local development)

## Changes Made

1. **Updated `layer1_slack_listener.py`:**
   - Now starts server when `--server` flag is used
   - Or when running in Railway environment

2. **Updated `railway.toml`:**
   - Changed start command to: `python layer1_slack_listener.py --server`

## Next Steps

### Step 1: Wait for Railway to Redeploy

Railway will automatically detect the code change and redeploy. This takes 2-3 minutes.

### Step 2: Check Logs Again

After redeployment, check Railway logs. You should now see:
```
Starting Slack listener on port 3000
```

Instead of the test output.

### Step 3: Test the Endpoint

Once redeployed, test in browser:
```
https://lead-magnet-generator-production.up.railway.app/health
```

Should respond with JSON now!

### Step 4: Try Slack URL Verification Again

Go back to Slack → Event Subscriptions and try the URL again. It should work now!

---

## How to Monitor

1. Go to Railway → Your service → Deployments
2. Watch for a new deployment (triggered by the git push)
3. Wait for it to complete
4. Check logs - should see "Starting Slack listener on port 3000"

---

## Expected Timeline

- **Now:** Code pushed to GitHub
- **1-2 minutes:** Railway detects change, starts building
- **2-3 minutes:** Deployment completes
- **Then:** App should be running and responding!
