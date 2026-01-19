# Complete Setup Guide: GitHub Actions + Railway

## Prerequisites ✅
- ✅ GitHub account
- ✅ Railway paid account
- ✅ All API keys ready (already in .env file)

---

## Step 1: Prepare Your Code for GitHub

### 1.1 Initialize Git Repository (if not already done)

```bash
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git init
```

### 1.2 Create .gitignore File

We need to make sure sensitive files aren't committed.

### 1.3 Stage and Commit Your Code

```bash
git add .
git commit -m "Initial commit: Lead Magnet Generator"
```

### 1.4 Create GitHub Repository and Push

1. Go to https://github.com/new
2. Repository name: `lead-magnet-generator` (or your preferred name)
3. Choose Private or Public
4. **Do NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

6. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
git branch -M main
git push -u origin main
```

---

## Step 2: Set Up Railway Project

### 2.1 Create New Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `lead-magnet-generator` repository
5. Railway will start deploying (we'll configure it in next steps)

### 2.2 Get Railway API Token

1. In Railway, click your profile (top right)
2. Click "Account Settings"
3. Go to "Tokens" tab
4. Click "New Token"
5. Give it a name: `github-actions-deploy`
6. **Copy the token** - you'll need it for GitHub Secrets
   - Format: `railway_xxxxxxxxxxxxx`

### 2.3 Get Railway Service ID

1. In your Railway project, click on the service (or create one if needed)
2. Go to Settings tab
3. Look for "Service ID" - copy this value
   - Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

---

## Step 3: Configure Railway Environment Variables

### 3.1 Add All Environment Variables to Railway

1. In Railway project, go to "Variables" tab
2. Click "New Variable"
3. Add each variable from your `.env` file:

```
PROSPEO_API_KEY=your_prospeo_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token-here
SLACK_SIGNING_SECRET=e162fc8db05db56d9d6b20a1c23d5d04
SLACK_PORT=3000
SLACK_CHANNEL_ID=C0A9N873LAE
OUTPUT_DIR=./output
```

### 3.2 Configure Railway Start Command

1. In Railway project, go to Settings tab
2. Scroll to "Start Command"
3. Set: `python layer1_slack_listener.py`

### 3.3 Generate Railway Domain (Get Permanent URL)

1. In Railway project, go to "Settings" tab
2. Scroll to "Networking"
3. Click "Generate Domain"
4. Railway will create a domain like: `lead-magnet-generator-production.up.railway.app`
5. **Copy this URL** - you'll need it for Slack configuration

---

## Step 4: Set Up GitHub Secrets

### 4.1 Add Railway Token to GitHub Secrets

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/lead-magnet-generator`
2. Click "Settings" tab
3. In left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add these secrets one by one:

**Secret 1: Railway Token**
- Name: `RAILWAY_TOKEN`
- Value: (paste your Railway token from Step 2.2)

**Secret 2: Railway Service ID**
- Name: `RAILWAY_SERVICE_ID`
- Value: (paste your Service ID from Step 2.3)

**Optional: Add API Keys for Testing (if you want tests to use real keys)**
- You can add your API keys as secrets for GitHub Actions testing, but this is optional since Railway will have them.

---

## Step 5: Configure GitHub Actions Workflows

### 5.1 The workflows are already created!

The following files should already exist:
- `.github/workflows/test.yml` - Runs tests
- `.github/workflows/deploy.yml` - Deploys to Railway

### 5.2 Update deploy.yml with Your Service Name

We need to update the deploy workflow to match your Railway service.

---

## Step 6: Update Deployment Workflow

The deploy.yml file needs your Railway service name. We'll update it in the next step.

---

## Step 7: Test the Setup

### 7.1 Push Code to Trigger GitHub Actions

```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push
```

### 7.2 Monitor GitHub Actions

1. Go to your GitHub repo
2. Click "Actions" tab
3. You should see workflows running:
   - "Test Application" - runs tests
   - "Deploy to Railway" - deploys if tests pass

### 7.3 Check Railway Deployment

1. Go to Railway dashboard
2. Check your project
3. You should see the deployment status
4. Check logs to ensure the app started correctly

---

## Step 8: Configure Slack App URLs

### 8.1 Update Slack Event Subscriptions URL

1. Go to https://api.slack.com/apps → Your App
2. Go to "Event Subscriptions"
3. Update Request URL to: `https://YOUR_RAILWAY_DOMAIN.railway.app/slack/events`
   - Replace `YOUR_RAILWAY_DOMAIN` with your actual Railway domain
4. Click "Save Changes"
5. Slack should verify the URL and show a green checkmark ✅

### 8.2 Update Slash Command URL

1. In Slack app, go to "Slash Commands"
2. Click on `/lead-magnet` command
3. Update Request URL to: `https://YOUR_RAILWAY_DOMAIN.railway.app/slack/commands`
4. Click "Save"

---

## Step 9: Test Everything

### 9.1 Test Slack Slash Command

In Slack, type:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees
```

You should get a response and the system should start processing.

### 9.2 Test Message Event

Post in your configured Slack channel:
```
Find leads: SaaS companies with >50 employees
```

The bot should respond.

### 9.3 Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on latest deployment
5. View logs to see what's happening

---

## Troubleshooting

### GitHub Actions Fails

- Check Actions tab for error messages
- Ensure all secrets are set correctly
- Check that Railway token has proper permissions

### Railway Deployment Fails

- Check Railway logs
- Verify environment variables are set
- Check that start command is correct: `python layer1_slack_listener.py`

### Slack URL Verification Fails

- Ensure Railway app is running (check logs)
- Verify the URL is exactly: `https://your-domain.railway.app/slack/events`
- Check that the endpoint is responding (try in browser)

### App Starts But Slack Doesn't Work

- Check Railway logs for errors
- Verify all environment variables are set
- Check Slack bot token and signing secret are correct

---

## What Happens on Each Push

1. You push code to GitHub
2. GitHub Actions automatically:
   - Runs tests (test.yml workflow)
   - If tests pass → Deploys to Railway (deploy.yml workflow)
3. Railway automatically:
   - Builds your app
   - Starts your Flask server
   - Keeps it running 24/7

---

## Next Steps

- ✅ Monitor first few deployments
- ✅ Test Slack integration thoroughly
- ✅ Set up alerts/monitoring (optional)
- ✅ Consider adding more tests to test.yml

You're all set! 🎉
