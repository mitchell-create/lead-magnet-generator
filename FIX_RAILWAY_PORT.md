# Fix Railway Port Configuration

## Problem

App is running on port **8080** (Railway's default PORT env var)
But Railway networking might be configured for port **3000**

## Solution: Align Ports

### Option 1: Set PORT=3000 in Railway (Recommended)

1. Go to Railway → Your service → **Variables** tab
2. Look for `PORT` variable (or create new)
3. Set value to: `3000`
4. Save

This tells Railway the app listens on 3000, and the code will use that.

### Option 2: Remove SLACK_PORT Variable

If you have `SLACK_PORT=3000` set:
1. Remove `SLACK_PORT` variable from Railway
2. The app will use Railway's `PORT` env var instead

**Actually, keep both:** The code uses `PORT` if available, falls back to `SLACK_PORT`.

## Quick Fix

**In Railway Variables:**
1. Add or update: `PORT=3000`
2. Keep: `SLACK_PORT=3000` (for fallback)

This ensures Railway routes to port 3000, and the app listens on 3000.

## After Fix

1. Railway will redeploy automatically (if variables changed)
2. Wait 1-2 minutes
3. Test: `https://lead-magnet-generator-production.up.railway.app/health`
4. Should work! ✅
