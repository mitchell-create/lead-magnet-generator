# GitHub Actions + Railway Setup Guide

## Understanding the Setup

### What Each Tool Does

**Railway/Render:**
- 🏠 **Hosts your app** 24/7
- 🌐 **Provides permanent URL** for Slack
- 💻 **Runs your Flask server** continuously
- ⚡ **Auto-deploys** from GitHub (can be triggered manually or via GitHub Actions)

**GitHub Actions:**
- ✅ **Runs tests** automatically when you push code
- 🚀 **Deploys to Railway** after tests pass
- 🔍 **Quality checks** before deployment
- 📊 **CI/CD pipeline** (Continuous Integration/Continuous Deployment)

---

## Setup Options

### Option A: Simple (Railway Auto-Deploy) ⭐ Recommended

**Railway can auto-deploy directly from GitHub without GitHub Actions:**

1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Railway watches for changes and auto-deploys
4. Done! ✅

**Pros:**
- Simplest setup
- No GitHub Actions needed
- Railway handles everything
- Still gets permanent URL

**Cons:**
- No automated testing
- Less control over deployment process

---

### Option B: Advanced (GitHub Actions + Railway) 🚀

**Use GitHub Actions for testing, then deploy to Railway:**

1. Push code to GitHub
2. GitHub Actions runs tests
3. If tests pass → GitHub Actions deploys to Railway
4. Railway runs your app

**Pros:**
- Automated testing
- Professional CI/CD pipeline
- Catch bugs before deployment
- More control

**Cons:**
- More setup required
- Need to configure GitHub Actions
- Slightly more complex

---

## Recommended: Start Simple, Add Actions Later

### Phase 1: Start with Railway Auto-Deploy
```
✅ Railway connected to GitHub
✅ Auto-deploys on push
✅ Simple and works great
```

### Phase 2: Add GitHub Actions (Later)
```
✅ Add automated testing
✅ Add quality checks
✅ Professional CI/CD pipeline
```

---

## Setup Instructions

### Option A: Railway Auto-Deploy (5 minutes)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create Railway account:**
   - Go to https://railway.app
   - Sign up with GitHub

3. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Configure environment variables:**
   - Go to Variables tab
   - Add all variables from your `.env` file:
     - `PROSPEO_API_KEY`
     - `OPENROUTER_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SLACK_BOT_TOKEN`
     - `SLACK_SIGNING_SECRET`
     - `SLACK_PORT=3000`
     - `SLACK_CHANNEL_ID`

5. **Configure start command:**
   - Settings → Start Command: `python layer1_slack_listener.py`

6. **Get your URL:**
   - Railway provides: `https://your-app.railway.app`
   - Use in Slack: `https://your-app.railway.app/slack/events`

7. **Done!** ✅
   - Railway auto-deploys when you push to GitHub
   - Your app runs 24/7
   - Permanent URL for Slack

---

### Option B: GitHub Actions + Railway (15 minutes)

**Prerequisites:**
- Code already on GitHub
- Railway account created

**Steps:**

1. **Get Railway token:**
   - Railway → Account Settings → Tokens
   - Create new token
   - Copy the token

2. **Add token to GitHub Secrets:**
   - GitHub repo → Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `RAILWAY_TOKEN`
   - Value: (paste your Railway token)

3. **GitHub Actions workflows are already created:**
   - `.github/workflows/test.yml` - Runs tests
   - `.github/workflows/deploy.yml` - Deploys to Railway

4. **Push code:**
   ```bash
   git add .
   git commit -m "Add GitHub Actions"
   git push
   ```

5. **Watch it work:**
   - GitHub Actions runs tests
   - If tests pass → Deploys to Railway
   - Check Actions tab to see progress

---

## Cost Comparison

| Setup | Cost | Complexity | Testing |
|-------|------|------------|---------|
| Railway Auto-Deploy | $0-5/mo | ⭐ Simple | Manual |
| Railway + GitHub Actions | $0-5/mo | ⭐⭐ Medium | Automated |

**Both use Railway for hosting** (same cost), difference is automation level.

---

## My Recommendation

**Start with Railway Auto-Deploy:**
- ✅ Simplest
- ✅ Gets you live in 5 minutes
- ✅ Works perfectly for your needs
- ✅ Can add GitHub Actions later if needed

**Add GitHub Actions when:**
- You want automated testing
- You're working with a team
- You want more deployment control

---

## Quick Answer

**Do you need Railway?** ✅ YES - You need Railway/Render to host your app

**Do you need GitHub Actions?** ⚠️ OPTIONAL - Nice to have, not required

**Can you use GitHub Actions alone?** ❌ NO - GitHub Actions doesn't host apps

**Best combo?** ✅ Railway (hosting) + GitHub Actions (testing/deployment) = Professional setup
