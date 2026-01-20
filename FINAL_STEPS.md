# Final Steps: Complete Setup

## ✅ Completed
- ✅ API keys added to Railway
- ✅ Domain created
- ✅ Start command configured

---

## STEP 1: Verify Deployment is Working

### 1.1 Check Railway Logs

1. In Railway, go to your service
2. Click **"Deployments"** tab
3. Click on the **latest deployment**
4. Click **"View Logs"** or **"Logs"**

**What to look for:**
```
Starting Slack listener on port 3000
```

✅ **If you see this:** Your app is running! Continue to next step.

❌ **If you see errors:** Check the error messages and let me know.

---

## STEP 2: Update Slack URLs

### 2.1 Get Your Railway Domain

Your Railway domain should look like:
```
https://lead-magnet-generator-production-xxxx.up.railway.app
```

**Copy this full URL** - you'll need it!

### 2.2 Configure Event Subscriptions

1. Go to: **https://api.slack.com/apps** → Your App
2. Click **"Event Subscriptions"** (left sidebar)
3. Toggle **"Enable Events"** to ON
4. Under **"Request URL"**, enter:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/events
   ```
   (Replace `YOUR_RAILWAY_DOMAIN` with your actual Railway domain)
5. Click **"Save Changes"**
6. Slack will verify the URL - you should see a **green checkmark** ✅

### 2.3 Subscribe to Bot Events

Still in Event Subscriptions:
1. Scroll to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add: `message.channels`
4. Click **"Save Changes"**

### 2.4 Update Slash Command

1. Go to **"Slash Commands"** (left sidebar)
2. Click on `/lead-magnet` command (or create new if it doesn't exist)
3. Update **"Request URL"** to:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/commands
   ```
4. Click **"Save"**

### 2.5 Reinstall App (If Needed)

If you added new scopes or events:
1. Go to **"OAuth & Permissions"**
2. Click **"Reinstall to Workspace"** (if there's a banner)
3. Authorize the app

---

## STEP 3: Create Supabase Table

### 3.1 Go to Supabase

1. Go to: **https://supabase.com/dashboard**
2. Select your project

### 3.2 Open SQL Editor

1. Click **"SQL Editor"** in the left sidebar
2. Click **"New query"**

### 3.3 Run Schema SQL

1. Open `supabase_schema.sql` from your project folder
2. **Copy ALL the SQL code**
3. **Paste** into Supabase SQL Editor
4. Click **"Run"** (or press Ctrl+Enter)
5. You should see: "Success. No rows returned"

✅ **Table created!**

---

## STEP 4: Test Everything

### 4.1 Test Slash Command

In Slack, type:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees
```

**Expected:** Bot should respond! ✅

### 4.2 Test Message Event

Post in your Slack channel:
```
Find leads: SaaS companies with >50 employees
```

**Expected:** Bot should respond! ✅

### 4.3 Check Railway Logs

1. Go back to Railway
2. View logs
3. You should see activity when you trigger commands

---

## STEP 5: Verify GitHub Actions (Optional)

Since you're using Option B (GitHub Actions + Railway):

1. Go to: **https://github.com/mitchell-create/lead-magnet-generator**
2. Click **"Actions"** tab
3. You should see workflows running (or completed)
4. Tests should have run automatically

---

## Troubleshooting

### Slack URL Verification Fails

**Check:**
- Railway app is running (check logs)
- URL is exactly: `https://your-domain.up.railway.app/slack/events`
- No typos in the domain

**Test in browser:**
- Try: `https://your-domain.up.railway.app/health`
- Should respond with JSON

### Bot Doesn't Respond in Slack

**Check:**
- Railway logs for errors
- All environment variables are set
- Slack bot token is correct
- App was reinstalled after adding scopes

### Supabase Table Creation Fails

**Check:**
- You're in the correct Supabase project
- Copied ALL the SQL from `supabase_schema.sql`
- No syntax errors in SQL

---

## Quick Checklist

- [ ] Railway deployment successful (check logs)
- [ ] Slack Event Subscriptions URL updated
- [ ] Slack Slash Command URL updated
- [ ] Bot events subscribed (message.channels)
- [ ] Supabase table created
- [ ] Test slash command works
- [ ] Test message event works
- [ ] GitHub Actions tests passing (optional check)

---

## What Happens Next

**Everything is automated!**

- ✅ Push code to GitHub → Railway auto-deploys
- ✅ GitHub Actions runs tests automatically
- ✅ Your app runs 24/7 on Railway
- ✅ Slack can reach your app via permanent URL

---

## Success! 🎉

If all tests pass, your Lead Magnet Generator is live and ready to use!
