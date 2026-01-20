# Fix: Slack URL Verification Error

## Problem

Slack can't verify your URL. This usually means:
1. App isn't running on Railway
2. App isn't responding to Slack's challenge
3. Wrong URL or routing issue

---

## STEP 1: Check if App is Running

### 1.1 Check Railway Logs

1. Go to Railway → Your service
2. Click **"Deployments"** tab
3. Click latest deployment → **"View Logs"**

**What to look for:**
```
Starting Slack listener on port 3000
```

**If you see errors:**
- Check what the error says
- Common issues: Missing environment variables, import errors, etc.

**If app isn't running:**
- Check the logs for startup errors
- Verify all environment variables are set

---

## STEP 2: Test the Endpoint Manually

### 2.1 Test Health Endpoint

Open in browser:
```
https://lead-magnet-generator-production.up.railway.app/health
```

**Expected:** Should show JSON: `{"status": "ok", ...}`

**If this doesn't work:** App isn't running or not accessible.

### 2.2 Test Slack Events Endpoint

The endpoint should respond to Slack's challenge. Slack Bolt handles this automatically, but let's verify.

---

## STEP 3: Common Issues & Fixes

### Issue 1: App Not Running

**Symptoms:**
- Logs show errors
- /health endpoint doesn't respond

**Fix:**
- Check Railway logs for errors
- Verify all environment variables are set
- Check if deployment succeeded

### Issue 2: Wrong URL

**Symptoms:**
- URL doesn't respond at all

**Fix:**
- Verify URL is exactly: `https://lead-magnet-generator-production.up.railway.app/slack/events`
- Try it in browser (might get an error, but should respond)
- Check for typos

### Issue 3: Port Configuration

**Symptoms:**
- App is running but Slack can't connect

**Fix:**
- Make sure Railway knows the app listens on port 3000
- Check if you set the port correctly in Railway

### Issue 4: App Not Responding to Challenge

**Symptoms:**
- App is running but verification fails

**Fix:**
- Slack Bolt should handle this automatically
- May need to check if Flask app is set up correctly

---

## STEP 4: Verify Code Setup

The Slack Bolt adapter should automatically handle URL verification. Let's verify the code is correct.

---

## Quick Checklist

- [ ] Railway logs show app running
- [ ] /health endpoint responds
- [ ] URL is exactly correct (no typos)
- [ ] Port 3000 is configured in Railway
- [ ] All environment variables are set
- [ ] Deployment shows "Active" status

---

## Next Steps

1. **First:** Check Railway logs - is the app actually running?
2. **Second:** Test /health endpoint in browser
3. **Third:** Verify URL is exactly correct in Slack settings
4. **Fourth:** Check if there are any errors in Railway logs

Let me know what you find in the Railway logs!
