# Why the Fix is Needed

## Current Problem

**Health endpoint doesn't work** because:
- Railway networking is configured for port **3000**
- But app is listening on port **8080**
- Railway routes external traffic → port 3000 → nothing listening there → error

## The Fix

**Make app listen on port 3000:**
- This matches Railway's networking config
- Railway routes → port 3000 → app listening → works! ✅

## Why This Will Fix It

1. **Port mismatch** is why health endpoint fails
2. **Once ports match** (both 3000), Railway can route traffic correctly
3. **Then** health endpoint will work
4. **Then** Slack can verify the URL

## Root Cause

Railway might be auto-setting PORT=8080, but your networking is configured for 3000. By forcing the app to use SLACK_PORT (3000), we align both.

## Yes, Make the Changes!

This fix is necessary to make the health endpoint work. Without it, Railway can't route traffic to your app.
