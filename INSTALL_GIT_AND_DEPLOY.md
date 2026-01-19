# Quick Start: Install Git & Deploy to Railway

## STEP 0: Install Git (Required for GitHub)

### Option 1: Download Git for Windows (Recommended)

1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer
4. **Important settings during installation:**
   - Use default options
   - Check "Git from the command line and also from 3rd-party software"
   - Use default editor (or choose your preference)
5. After installation, **restart PowerShell** (close and reopen)

### Option 2: Install via winget (if available)

```powershell
winget install Git.Git
```

Then restart PowerShell.

### Verify Git Installation

Open a **NEW** PowerShell window and run:
```powershell
git --version
```

Should show: `git version 2.x.x`

---

## STEP 1: Prepare Code for GitHub

### 1.1 Navigate to Project

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

### 1.2 Initialize Git Repository

```powershell
git init
```

### 1.3 Stage All Files

```powershell
git add .
```

### 1.4 Make Initial Commit

```powershell
git commit -m "Initial commit: Lead Magnet Generator ready for deployment"
```

---

## STEP 2: Create GitHub Repository

### 2.1 Create New Repository

1. Go to: https://github.com/new
2. Repository name: `lead-magnet-generator`
3. Description: "Automated lead qualification tool"
4. Choose: **Private** (recommended) or **Public**
5. **DO NOT** check any boxes (README, .gitignore, license)
6. Click **"Create repository"**

### 2.2 Push Code to GitHub

After creating the repo, GitHub will show you commands. Use these (replace `YOUR_USERNAME`):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)

**To create a Personal Access Token:**
1. GitHub → Settings (your profile) → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Name it: "Railway Deployment"
5. Check: `repo` (full control)
6. Generate token
7. **COPY THE TOKEN** - use this as your password

---

## STEP 3: Connect Railway to GitHub

### 3.1 Create Railway Project

1. Go to: https://railway.app
2. Sign in (use GitHub if you prefer)
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway (if first time)
6. Select your `lead-magnet-generator` repository
7. Click **"Deploy Now"**

Railway will automatically start building!

---

## STEP 4: Configure Railway

### 4.1 Set Start Command

1. Click on your service in Railway
2. Go to **"Settings"** tab
3. Find **"Start Command"**
4. Set to: `python layer1_slack_listener.py`
5. Click **"Update"**

### 4.2 Generate Domain

1. In Settings, scroll to **"Networking"**
2. Click **"Generate Domain"**
3. **COPY THE DOMAIN** - you'll need it for Slack!

---

## STEP 5: Add Environment Variables

1. In Railway, click **"Variables"** tab
2. Add each variable (click "New Variable" for each):

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

---

## STEP 6: Update Slack URLs

1. Go to: https://api.slack.com/apps → Your App
2. **Event Subscriptions:**
   - Request URL: `https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/events`
3. **Slash Commands:**
   - Request URL: `https://YOUR_RAILWAY_DOMAIN.up.railway.app/slack/commands`

---

## Complete Guide

See `DEPLOY_TO_RAILWAY_STEPS.md` for detailed step-by-step instructions!
