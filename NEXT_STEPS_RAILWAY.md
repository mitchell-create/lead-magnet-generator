# Next Steps: Railway Deployment (Option B)

## ✅ Completed
- ✅ Code pushed to GitHub
- ✅ Repository: https://github.com/mitchell-create/lead-magnet-generator

---

## STEP 1: Connect Railway to GitHub

### 1.1 Create Railway Project

1. Go to: **https://railway.app**
2. Sign in (use GitHub if you prefer)
3. Click **"New Project"** (top right)
4. Select **"Deploy from GitHub repo"**
5. If first time, authorize Railway to access GitHub
6. Find and select your **`lead-magnet-generator`** repository
7. Click **"Deploy Now"**

Railway will automatically:
- Detect Python
- Start building your project
- Create a service

---

## STEP 2: Configure Railway Service

### 2.1 Set Start Command

1. In Railway, click on your service (the one that was created)
2. Click **"Settings"** tab
3. Scroll to **"Start Command"**
4. Enter: `python layer1_slack_listener.py`
5. Click **"Update"**

### 2.2 Generate Public Domain

1. Still in Settings, scroll to **"Networking"** section
2. Click **"Generate Domain"**
3. Railway will create: `https://lead-magnet-generator-production-xxxx.up.railway.app`
4. **COPY THIS FULL URL** - you'll need it for Slack!

---

## STEP 3: Add Environment Variables

1. In Railway project, click **"Variables"** tab (top menu)
2. Click **"New Variable"** for each one

**Add these 9 variables:**

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

**Important:** Make sure all 9 variables are added!

---

## STEP 4: Monitor Deployment

1. Click **"Deployments"** tab
2. Watch the deployment progress
3. You'll see:
   - "Building..." → Installing dependencies
   - "Deploying..." → Starting your app
   - "Active" → Your app is running!

4. Click on the deployment → **"View Logs"**
5. You should see:
   ```
   Starting Slack listener on port 3000
   ```
   If you see this, your app is running! ✅

---

## STEP 5: Update Slack URLs

### 5.1 Get Your Railway URL

Your Railway domain should be something like:
```
https://lead-magnet-generator-production-xxxx.up.railway.app
```

### 5.2 Configure Event Subscriptions

1. Go to: **https://api.slack.com/apps** → Your App
2. Click **"Event Subscriptions"** (left sidebar)
3. Toggle **"Enable Events"** to ON
4. Under **"Request URL"**, enter:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/events
   ```
   (Replace `YOUR_RAILWAY_DOMAIN` with your actual domain)
5. Click **"Save Changes"**
6. Slack will verify the URL - you should see a green checkmark ✅

### 5.3 Subscribe to Bot Events

Still in Event Subscriptions:
1. Scroll to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add: `message.channels`
4. Click **"Save Changes"**

### 5.4 Update Slash Command

1. Go to **"Slash Commands"** (left sidebar)
2. Click on `/lead-magnet` command (or create new)
3. Update **"Request URL"** to:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/commands
   ```
4. Click **"Save"**

---

## STEP 6: Create Supabase Table

### 6.1 Go to Supabase

1. Go to: **https://supabase.com/dashboard**
2. Select your project
3. Go to **"SQL Editor"**

### 6.2 Run Schema SQL

1. Open `supabase_schema.sql` from your project folder
2. Copy all the SQL code
3. Paste into Supabase SQL Editor
4. Click **"Run"**
5. Table will be created! ✅

---

## STEP 7: Test Everything

### 7.1 Test Slash Command

In Slack, type:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees
```

You should get a response from the bot! ✅

### 7.2 Test Message Event

Post in your Slack channel:
```
Find leads: SaaS companies with >50 employees
```

The bot should respond! ✅

---

## Quick Checklist

- [ ] Railway project created from GitHub
- [ ] Start command set: `python layer1_slack_listener.py`
- [ ] Railway domain generated and copied
- [ ] All 9 environment variables added
- [ ] Deployment successful (check logs)
- [ ] Slack Event Subscriptions URL updated
- [ ] Slack Slash Command URL updated
- [ ] Supabase table created
- [ ] Test slash command works
- [ ] Test message event works

---

## What Happens Next

**Auto-Deployment:**
- When you push code to GitHub → Railway automatically deploys!
- No manual steps needed

**GitHub Actions:**
- Tests run automatically when you push
- Check GitHub → Actions tab to see test results

---

## Troubleshooting

**Railway deployment fails:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check start command is correct

**Slack URL verification fails:**
- Make sure Railway app is running (check logs)
- Verify URL is exactly: `https://your-domain.up.railway.app/slack/events`
- Try the URL in browser - should respond

**App doesn't respond in Slack:**
- Check Railway logs for errors
- Verify all environment variables are set
- Check Slack bot token and signing secret

---

## Ready to Start?

Begin with **STEP 1: Connect Railway to GitHub**! 🚀
