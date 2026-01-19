# Deploy to Railway with GitHub - Complete Step-by-Step Guide

## Prerequisites ✅
- ✅ GitHub account
- ✅ Railway paid account
- ✅ All API keys ready (in .env file)
- ✅ Code tested and working

---

## STEP 1: Prepare Code for GitHub

### 1.1 Check Current Status

Make sure you're in the project folder:
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

### 1.2 Initialize Git (if not already done)

```powershell
git init
```

### 1.3 Stage All Files

```powershell
git add .
```

### 1.4 Make Initial Commit

```powershell
git commit -m "Initial commit: Lead Magnet Generator - Ready for deployment"
```

---

## STEP 2: Create GitHub Repository

### 2.1 Create New Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `lead-magnet-generator`
3. Description: "Automated lead qualification tool using Prospeo, OpenRouter, and Slack"
4. Choose: **Private** or **Public** (your choice)
5. **DO NOT** check:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
6. Click **"Create repository"**

### 2.2 Push Code to GitHub

GitHub will show you commands. Use these (replace `YOUR_USERNAME` with your GitHub username):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
git branch -M main
git push -u origin main
```

**If prompted for authentication:**
- Use your GitHub username and a Personal Access Token (not password)
- To create token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
- Give it `repo` permissions

---

## STEP 3: Create Railway Project

### 3.1 Sign In to Railway

1. Go to: https://railway.app
2. Sign in (use GitHub to sign in if you prefer)

### 3.2 Create New Project from GitHub

1. Click **"New Project"** (top right)
2. Select **"Deploy from GitHub repo"**
3. If first time, authorize Railway to access GitHub
4. Find and select your `lead-magnet-generator` repository
5. Click **"Deploy Now"**

Railway will automatically:
- Detect Python
- Start building your project
- Create a service

---

## STEP 4: Configure Railway Service

### 4.1 Set Start Command

1. In Railway, click on your service (or the service that was created)
2. Click **"Settings"** tab
3. Scroll to **"Start Command"**
4. Enter: `python layer1_slack_listener.py`
5. Click **"Update"**

### 4.2 Generate Public Domain

1. Still in Settings, scroll to **"Networking"** section
2. Click **"Generate Domain"**
3. Railway will create a domain like: `lead-magnet-generator-production-xxxx.up.railway.app`
4. **COPY THIS FULL URL** - you'll need it for Slack!

---

## STEP 5: Add Environment Variables

### 5.1 Open Variables Tab

1. In Railway project, click **"Variables"** tab (top menu)
2. You'll see a table to add variables

### 5.2 Add Each Variable

Click **"New Variable"** and add these one by one:

**Variable 1:**
- Key: `PROSPEO_API_KEY`
- Value: `pk_your_prospeo_api_key_here`
- Click **"Add"**

**Variable 2:**
- Key: `OPENROUTER_API_KEY`
- Value: `sk-or-v1-your-openrouter-api-key-here`
- Click **"Add"**

**Variable 3:**
- Key: `SUPABASE_URL`
- Value: `https://utdwvqfnzkcysdsbsvwv.supabase.co`
- Click **"Add"**

**Variable 4:**
- Key: `SUPABASE_KEY`
- Value: `your_supabase_service_role_key_here`
- Click **"Add"**

**Variable 5:**
- Key: `SLACK_BOT_TOKEN`
- Value: `xoxb-your-slack-bot-token-here`
- Click **"Add"**

**Variable 6:**
- Key: `SLACK_SIGNING_SECRET`
- Value: `e162fc8db05db56d9d6b20a1c23d5d04`
- Click **"Add"**

**Variable 7:**
- Key: `SLACK_PORT`
- Value: `3000`
- Click **"Add"**

**Variable 8:**
- Key: `SLACK_CHANNEL_ID`
- Value: `C0A9N873LAE`
- Click **"Add"**

**Variable 9:**
- Key: `OUTPUT_DIR`
- Value: `./output`
- Click **"Add"**

**✅ Important:** Make sure all 9 variables are added!

---

## STEP 6: Wait for Deployment

### 6.1 Monitor Build

1. Click on **"Deployments"** tab
2. Watch the deployment progress
3. You'll see:
   - "Building..." → Installing dependencies
   - "Deploying..." → Starting your app
   - "Active" → Your app is running!

### 6.2 Check Logs

1. Click on the latest deployment
2. Click **"View Logs"**
3. You should see:
   ```
   Starting Slack listener on port 3000
   ```
   If you see this, your app is running! ✅

---

## STEP 7: Configure Slack App URLs

### 7.1 Get Your Railway URL

Your Railway URL should be something like:
```
https://lead-magnet-generator-production-xxxx.up.railway.app
```

### 7.2 Update Event Subscriptions

1. Go to: https://api.slack.com/apps
2. Click on your app
3. Go to **"Event Subscriptions"** (left sidebar)
4. Toggle **"Enable Events"** to ON
5. Under **"Request URL"**, enter:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/events
   ```
   (Replace `YOUR_RAILWAY_DOMAIN` with your actual domain)
6. Click **"Save Changes"**
7. Slack will verify the URL - you should see a green checkmark ✅

### 7.3 Subscribe to Bot Events

Still in Event Subscriptions:
1. Scroll to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add: `message.channels`
4. Click **"Save Changes"**

### 7.4 Update Slash Command

1. Go to **"Slash Commands"** (left sidebar)
2. Click on `/lead-magnet` command (or create new)
3. Update **"Request URL"** to:
   ```
   https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/commands
   ```
4. Click **"Save"**

### 7.5 Reinstall App (if needed)

If you added new scopes:
1. Go to **"OAuth & Permissions"**
2. Click **"Reinstall to Workspace"**
3. Authorize the app

---

## STEP 8: Test Everything

### 8.1 Test Slash Command

In Slack, type:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees
```

You should get a response from the bot! ✅

### 8.2 Test Message Event

Post in your Slack channel:
```
Find leads: SaaS companies with >50 employees
```

The bot should respond! ✅

### 8.3 Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Click **"Deployments"** → Latest deployment → **"View Logs"**
4. You should see activity when you trigger commands

---

## STEP 9: Create Supabase Table (If Not Done)

### 9.1 Go to Supabase

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Go to **"SQL Editor"**

### 9.2 Run Schema SQL

1. Open `supabase_schema.sql` from your project folder
2. Copy all the SQL code
3. Paste into Supabase SQL Editor
4. Click **"Run"**
5. Table will be created! ✅

---

## ✅ Deployment Complete!

**What you have now:**
- ✅ Code on GitHub
- ✅ App deployed on Railway
- ✅ Permanent HTTPS URL
- ✅ Slack integrated
- ✅ Auto-deploys when you push to GitHub

**Your Railway URL:**
```
https://YOUR_DOMAIN.up.railway.app
```

**Slack URLs:**
- Events: `https://YOUR_DOMAIN.up.railway.app/slack/events`
- Commands: `https://YOUR_DOMAIN.up.railway.app/slack/commands`

---

## Future Updates

**To update your app:**
1. Make changes to code locally
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Your update message"
   git push
   ```
3. Railway automatically detects the push and redeploys! 🚀

---

## Troubleshooting

**Railway deployment fails:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check start command is: `python layer1_slack_listener.py`

**Slack URL verification fails:**
- Make sure Railway app is running (check logs)
- Verify URL is exactly: `https://your-domain.up.railway.app/slack/events`
- Try the URL in browser - should respond

**App doesn't respond in Slack:**
- Check Railway logs for errors
- Verify all environment variables are set
- Check Slack bot token and signing secret

---

## Quick Command Reference

```powershell
# Navigate to project
cd C:\Users\ReadyPlayerOne\lead-magnet-generator

# Check git status
git status

# Add and commit changes
git add .
git commit -m "Your message"
git push

# Check Railway deployment (via web dashboard)
# https://railway.app
```

---

**Ready to deploy? Start with STEP 1!** 🚀
