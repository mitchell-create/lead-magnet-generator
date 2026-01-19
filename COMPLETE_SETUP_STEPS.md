# Complete Step-by-Step Setup: GitHub Actions + Railway

## Overview

You'll set up:
1. ✅ GitHub repository with your code
2. ✅ Railway project connected to GitHub (auto-deploys)
3. ✅ GitHub Actions for automated testing
4. ✅ Slack app configured with permanent Railway URL

---

## STEP-BY-STEP INSTRUCTIONS

### STEP 1: Prepare Your Code for GitHub

#### 1.1 Navigate to Project Directory
```bash
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

#### 1.2 Initialize Git (if not already done)
```bash
git init
```

#### 1.3 Add and Commit All Files
```bash
git add .
git commit -m "Initial commit: Lead Magnet Generator with GitHub Actions"
```

#### 1.4 Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `lead-magnet-generator`
3. Description: "Automated lead qualification tool using Prospeo, OpenRouter, and Slack"
4. Choose **Private** or **Public** (your choice)
5. **Do NOT** check "Initialize with README" or any other options
6. Click "Create repository"

#### 1.5 Push Code to GitHub
GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username.**

---

### STEP 2: Set Up Railway Project

#### 2.1 Create New Railway Project from GitHub
1. Go to: https://railway.app
2. Click **"New Project"** (top right)
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub (if first time)
5. Find and select your `lead-magnet-generator` repository
6. Click **"Deploy Now"**

#### 2.2 Configure Railway Service
1. Railway will create a service automatically
2. Click on the service to configure it

#### 2.3 Set Start Command
1. In your Railway service, click **"Settings"** tab
2. Scroll to **"Start Command"**
3. Enter: `python layer1_slack_listener.py`
4. Click **"Update"**

#### 2.4 Generate Public Domain
1. Still in Settings, scroll to **"Networking"** section
2. Click **"Generate Domain"**
3. Railway will create: `https://lead-magnet-generator-production-xxxx.up.railway.app`
4. **Copy this full URL** - you'll need it for Slack!

#### 2.5 Add Environment Variables
1. In Railway project, click **"Variables"** tab
2. Click **"New Variable"**
3. Add each variable one by one:

**Variable 1:**
- Name: `PROSPEO_API_KEY`
- Value: `pk_18aa056cf585e436de7ad62b3ccd7baf1ad9e633b7e403aa5f9a35ff7fb3b01d`

**Variable 2:**
- Name: `OPENROUTER_API_KEY`
- Value: `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`

**Variable 3:**
- Name: `SUPABASE_URL`
- Value: `https://utdwvqfnzkcysdsbsvwv.supabase.co`

**Variable 4:**
- Name: `SUPABASE_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0ZHd2cWZuemtjeXNkc2Jzdnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODc4NDk4OCwiZXhwIjoyMDg0MzYwOTg4fQ.tfYTjn7z0lbEJx7NnGeivyDPUrbqFHwOy0RgcO4IERs`

**Variable 5:**
- Name: `SLACK_BOT_TOKEN`
- Value: `xoxb-3507979379937-10326210258854-Cm4WgC7tdXuW1k4XgeY7fueD`

**Variable 6:**
- Name: `SLACK_SIGNING_SECRET`
- Value: `e162fc8db05db56d9d6b20a1c23d5d04`

**Variable 7:**
- Name: `SLACK_PORT`
- Value: `3000`

**Variable 8:**
- Name: `SLACK_CHANNEL_ID`
- Value: `C0A9N873LAE`

**Variable 9:**
- Name: `OUTPUT_DIR`
- Value: `./output`

✅ **Important:** Make sure all variables are added correctly!

---

### STEP 3: Set Up GitHub Actions (Testing)

#### 3.1 Add GitHub Secrets (for testing)

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/lead-magnet-generator`
2. Click **"Settings"** tab (top of repo)
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"**

**Add these secrets (optional - only if you want tests to use real API keys):**

- Name: `PROSPEO_API_KEY` | Value: `pk_18aa056cf585e436de7ad62b3ccd7baf1ad9e633b7e403aa5f9a35ff7fb3b01d`
- Name: `OPENROUTER_API_KEY` | Value: `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`
- Name: `SUPABASE_URL` | Value: `https://utdwvqfnzkcysdsbsvwv.supabase.co`
- Name: `SUPABASE_KEY` | Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0ZHd2cWZuemtjeXNkc2Jzdnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODc4NDk4OCwiZXhwIjoyMDg0MzYwOTg4fQ.tfYTjn7z0lbEJx7NnGeivyDPUrbqFHwOy0RgcO4IERs`
- Name: `SLACK_BOT_TOKEN` | Value: `xoxb-3507979379937-10326210258854-Cm4WgC7tdXuW1k4XgeY7fueD`
- Name: `SLACK_SIGNING_SECRET` | Value: `e162fc8db05db56d9d6b20a1c23d5d04`

**Note:** These are optional. The test workflow will still run without them (it will just skip config validation).

---

### STEP 4: Test GitHub Actions

#### 4.1 Push Code to Trigger Tests

The GitHub Actions workflows are already in your code. Let's trigger them:

```bash
# Make a small change to trigger the workflow
echo "# Test commit" >> README.md
git add .
git commit -m "Test: Trigger GitHub Actions"
git push
```

#### 4.2 Check GitHub Actions Status

1. Go to your GitHub repo
2. Click **"Actions"** tab
3. You should see:
   - ✅ **"Test Application"** workflow running
   - This will test your code imports and configuration

#### 4.3 Check Railway Deployment

1. Go to Railway dashboard
2. Your project should automatically deploy (Railway watches GitHub)
3. Check the deployment status - it should show "Deployed" ✅
4. Click on the deployment to see logs

---

### STEP 5: Configure Slack App

#### 5.1 Get Your Railway URL

From Step 2.4, you have your Railway domain. It should be something like:
`https://lead-magnet-generator-production-xxxx.up.railway.app`

#### 5.2 Configure Event Subscriptions

1. Go to: https://api.slack.com/apps
2. Click on your app
3. Click **"Event Subscriptions"** (left sidebar)
4. Toggle **"Enable Events"** to ON
5. Under **"Request URL"**, enter:
   ```
   https://YOUR_RAILWAY_DOMAIN.railway.app/slack/events
   ```
   Replace `YOUR_RAILWAY_DOMAIN` with your actual Railway domain.
6. Click **"Save Changes"**
7. Slack will verify the URL - you should see a green checkmark ✅

#### 5.3 Subscribe to Bot Events

Still in Event Subscriptions:
1. Scroll to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add: `message.channels`
4. Click **"Save Changes"**

#### 5.4 Configure Slash Command

1. In Slack app, click **"Slash Commands"** (left sidebar)
2. Click **"Create New Command"**
3. Fill in:
   - **Command:** `/lead-magnet`
   - **Request URL:** `https://YOUR_RAILWAY_DOMAIN.railway.app/slack/commands`
   - **Short Description:** `Generate qualified leads from Prospeo`
   - **Usage Hint:** `Target: SaaS companies | Criteria: Size>50 employees`
4. Click **"Save"**

#### 5.5 Reinstall App to Workspace (if needed)

If you added new scopes or events:
1. Go to **"OAuth & Permissions"**
2. Click **"Reinstall to Workspace"**
3. Authorize the app

---

### STEP 6: Test Everything

#### 6.1 Test Railway Deployment

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click on latest deployment
5. Check logs - you should see:
   ```
   Starting Slack listener on port 3000
   ```

#### 6.2 Test Slack Slash Command

In Slack, type:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees
```

You should get a response from the bot!

#### 6.3 Test Message Event

Post in your Slack channel (C0A9N873LAE):
```
Find leads: SaaS companies with >50 employees
```

The bot should respond.

---

### STEP 7: Verify Auto-Deployment Works

#### 7.1 Make a Small Change

```bash
# Make a small change
echo "Test auto-deploy" >> test.txt
git add .
git commit -m "Test auto-deployment"
git push
```

#### 7.2 Watch the Magic Happen

1. **GitHub Actions:** Will run tests automatically
2. **Railway:** Will automatically detect the push and deploy
3. Check both:
   - GitHub → Actions tab → See test results
   - Railway → See new deployment

---

## ✅ Setup Complete Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created and connected to GitHub
- [ ] All environment variables added to Railway
- [ ] Start command set: `python layer1_slack_listener.py`
- [ ] Railway domain generated and copied
- [ ] GitHub Actions workflows committed
- [ ] Slack Event Subscriptions URL configured
- [ ] Slack Slash Command URL configured
- [ ] Test slash command works
- [ ] Test message event works
- [ ] Auto-deployment verified

---

## 🎉 You're All Set!

**What happens now:**
1. ✅ Push code → GitHub Actions runs tests
2. ✅ Tests pass → Railway auto-deploys
3. ✅ Your app runs 24/7 on Railway
4. ✅ Slack can reach your app via permanent URL

**Railway URL for Slack:**
```
https://YOUR_RAILWAY_DOMAIN.railway.app
```

**Event URL:** `https://YOUR_RAILWAY_DOMAIN.railway.app/slack/events`
**Command URL:** `https://YOUR_RAILWAY_DOMAIN.railway.app/slack/commands`

---

## Troubleshooting

**Railway deployment fails:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check start command is correct

**Slack URL verification fails:**
- Ensure Railway app is running (check logs)
- Verify URL is exactly correct (including `/slack/events`)
- Try the URL in browser - should see "OK" or similar

**GitHub Actions fails:**
- Check Actions tab for specific error
- Verify secrets are set (optional)
- Check that Python version matches (3.12)

Need help? Check the logs in both GitHub Actions and Railway!
