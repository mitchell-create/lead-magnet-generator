# Fix: Port Mismatch Issue

## Problem

The logs show:
- App is running on port **8080** (Railway's PORT env var)
- But Railway might be configured to expect port **3000**

## Solution

We have two options:

### Option 1: Use Railway's PORT (8080) - Recommended

Railway automatically sets `PORT=8080`. The app should use that.

**Check Railway settings:**
1. Go to Railway → Your service → Settings
2. Look for **"Port"** or **"Expose Port"** setting
3. Make sure it's set to **8080** (or remove it and let Railway auto-detect)

### Option 2: Force Port 3000

If Railway needs port 3000:
1. In Railway → Variables
2. Add/update: `PORT=3000`

But the app code already handles this - it uses Railway's PORT env var if available.

## Current Status

Looking at logs:
- ✅ App is running on `0.0.0.0:8080` (correct - accessible)
- ❓ Railway might not be routing to port 8080

## Quick Check

Test in browser:
```
https://lead-magnet-generator-production.up.railway.app/health
```

If this doesn't work, Railway might need the port configured.

## Fix Steps

1. **Check Railway port setting:**
   - Railway → Service → Settings
   - Look for port/expose settings
   - Should match what PORT env var is (8080)

2. **Or explicitly set PORT in Railway:**
   - Variables → Add `PORT=3000`
   - Remove `SLACK_PORT` variable (app uses PORT)

3. **Wait for redeploy** and test again
