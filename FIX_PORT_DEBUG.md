# Debug Port Issue

## Issue

PORT is set to 3000 in Railway, but app logs show it's running on 8080.

## What I Added

I've added logging to see what port values the app is receiving. After redeploy, check logs to see:
- What PORT env var Railway is providing
- What SLACK_PORT config value is
- What port the app actually uses

## Solution Attempt

Changed the code to **prefer SLACK_PORT** (3000) over Railway's PORT env var.

This ensures:
- If SLACK_PORT=3000 is set → uses 3000
- Otherwise falls back to Railway's PORT

## Next Steps

1. **Commit and push the updated code**
2. **Wait for Railway to redeploy**
3. **Check logs** - should show debug info about ports
4. **See what port it actually uses**

## Alternative: Remove PORT Variable

If Railway is overriding PORT=3000 with its own value:
1. In Railway → Variables
2. **Remove** `PORT` variable (if it exists)
3. Keep only `SLACK_PORT=3000`
4. The app will use SLACK_PORT (3000)

This might force Railway to route to port 3000 correctly.
