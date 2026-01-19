# GitHub Repository Setup - Detailed Steps

## STEP 1: Create GitHub Repository (On Website)

### 1.1 Go to GitHub

1. Open your browser
2. Go to: **https://github.com/new**
3. Sign in if needed

### 1.2 Fill in Repository Details

**Repository name:**
```
lead-magnet-generator
```

**Description (optional):**
```
Automated lead qualification tool using Prospeo, OpenRouter AI, and Slack
```

**Visibility:**
- Choose **Private** (recommended - keeps your code and API keys private)
- OR **Public** (if you want to share)

**IMPORTANT: DO NOT CHECK:**
- ❌ Add a README file
- ❌ Add .gitignore (we already have one)
- ❌ Choose a license

**Why?** Because you already have code locally, and checking these will cause merge conflicts.

### 1.3 Create Repository

Click the green **"Create repository"** button

---

## STEP 2: Initialize Git Locally (In PowerShell)

### 2.1 Open PowerShell

Make sure you're in the project folder:
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

### 2.2 Initialize Git Repository

```powershell
git init
```

**Expected output:**
```
Initialized empty Git repository in C:/Users/ReadyPlayerOne/lead-magnet-generator/.git/
```

### 2.3 Configure Git (If First Time)

**Set your name:**
```powershell
git config --global user.name "Your Name"
```

**Set your email (use your GitHub email):**
```powershell
git config --global user.email "your.email@example.com"
```

### 2.4 Check What Will Be Committed

```powershell
git status
```

You should see all your files listed as "Untracked files"

---

## STEP 3: Stage and Commit Files

### 3.1 Stage All Files

```powershell
git add .
```

This tells Git to include all files in the commit.

### 3.2 Verify What's Staged

```powershell
git status
```

You should see files listed as "Changes to be committed"

### 3.3 Make Initial Commit

```powershell
git commit -m "Initial commit: Lead Magnet Generator with GitHub Actions"
```

**Expected output:**
```
[main (root-commit) xxxxxx] Initial commit: Lead Magnet Generator with GitHub Actions
 X files changed, X insertions(+)
```

---

## STEP 4: Connect to GitHub Repository

### 4.1 Get Your Repository URL

After creating the GitHub repo (Step 1), GitHub will show you a page with commands. Look for a URL like:

```
https://github.com/YOUR_USERNAME/lead-magnet-generator.git
```

**OR** if you closed that page, you can find it by:
1. Going to your repository on GitHub
2. Click the green **"Code"** button
3. Copy the HTTPS URL

### 4.2 Add Remote Repository

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```powershell
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
```

**Example (if your username is "johndoe"):**
```powershell
git remote add origin https://github.com/johndoe/lead-magnet-generator.git
```

### 4.3 Verify Remote Added

```powershell
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/lead-magnet-generator.git (fetch)
origin  https://github.com/YOUR_USERNAME/lead-magnet-generator.git (push)
```

---

## STEP 5: Push Code to GitHub

### 5.1 Rename Branch to Main

```powershell
git branch -M main
```

### 5.2 Push to GitHub

```powershell
git push -u origin main
```

### 5.3 Authentication

**If prompted for credentials:**

**Username:** Your GitHub username

**Password:** 
- ❌ **NOT your GitHub password!**
- ✅ **Use a Personal Access Token**

**To create a Personal Access Token:**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: `Railway Deployment`
4. Select expiration: `90 days` (or `No expiration` if you prefer)
5. Check these scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click **"Generate token"** at bottom
7. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!
8. Use this token as your password

**If successful, you'll see:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/YOUR_USERNAME/lead-magnet-generator.git
 * [new branch]      main -> main
Branch 'main' set up to track 'remote branch 'main' from 'origin'.
```

---

## STEP 6: Verify on GitHub

1. Go to: **https://github.com/YOUR_USERNAME/lead-magnet-generator**
2. You should see all your files!
3. Check for:
   - ✅ All Python files (layer1, layer2, etc.)
   - ✅ requirements.txt
   - ✅ .github/workflows/ folder (with GitHub Actions)
   - ✅ runtime.txt
   - ✅ .gitignore

---

## Common Issues & Solutions

### Issue: "fatal: not a git repository"

**Solution:**
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git init
```

### Issue: Authentication failed

**Solution:**
- Make sure you're using a Personal Access Token, not password
- Token needs `repo` scope
- Try creating a new token

### Issue: "remote origin already exists"

**Solution:**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git
```

### Issue: "fatal: refusing to merge unrelated histories"

**Solution:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Issue: "failed to push some refs"

**Solution:**
```powershell
git pull origin main --rebase
git push -u origin main
```

---

## Quick Command Reference

```powershell
# Navigate to project
cd C:\Users\ReadyPlayerOne\lead-magnet-generator

# Initialize git
git init

# Configure (first time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Stage files
git add .

# Commit
git commit -m "Initial commit"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/lead-magnet-generator.git

# Push
git branch -M main
git push -u origin main
```

---

## What's Next?

After successfully pushing to GitHub:

1. ✅ Your code is on GitHub
2. ⏭️ Next: Connect Railway to this GitHub repo
3. ⏭️ Then: Add environment variables in Railway
4. ⏭️ Finally: Update Slack URLs

---

## Need Help?

If you get stuck on any step, let me know:
- What command you ran
- What error message you see
- Which step you're on

I'll help you troubleshoot! 🚀
