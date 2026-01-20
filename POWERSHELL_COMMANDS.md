# When to Use PowerShell - Quick Guide

## ✅ YES - Use PowerShell For:

### 1. Committing and Pushing Code Changes
Whenever I make code changes, you need to push them to GitHub:

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git add .
git commit -m "Description of what changed"
git push
```

**This deploys your code to Railway automatically.**

---

## ❌ NO - Don't Use PowerShell For:

### 1. Installing Dependencies
- ❌ **Don't run**: `pip install beautifulsoup4`
- ✅ **Railway does this automatically** when you push code (reads `requirements.txt`)

### 2. Updating Supabase
- ❌ **Don't use PowerShell** for database changes
- ✅ **Use Supabase Dashboard** (web interface) - SQL Editor

### 3. Setting Environment Variables
- ❌ **Don't use PowerShell** to set Railway variables
- ✅ **Use Railway Dashboard** (web interface) - Variables tab

### 4. Testing Code Locally
- ⚠️ **Optional** - Only if you want to test before deploying
- ✅ **Usually not needed** - Railway will handle it

---

## 🚀 Current Step: Push Website Scraping Code

**YES, run this in PowerShell:**

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git add .
git commit -m "Add website scraping for wholesale partner qualification"
git push
```

**What happens:**
1. ✅ Code pushed to GitHub
2. ✅ Railway automatically detects the push
3. ✅ Railway installs new dependencies (beautifulsoup4, lxml, html5lib)
4. ✅ Railway redeploys your app
5. ✅ Website scraping is now active!

---

## 📋 Going Forward

**I'll always clearly state:**
- ✅ **"Run this in PowerShell:"** = You need to run commands
- ❌ **"This happens automatically"** = No PowerShell needed
- 📝 **"Update in Railway/Supabase Dashboard"** = Use web interface

---

## Quick Reference

| Task | Where | PowerShell? |
|------|-------|-------------|
| Commit/push code | PowerShell | ✅ YES |
| Install dependencies | Railway (auto) | ❌ NO |
| Update Supabase schema | Supabase Dashboard | ❌ NO |
| Set API keys | Railway Dashboard | ❌ NO |
| Deploy code | Railway (auto) | ❌ NO |

---

**TL;DR:** Only use PowerShell for `git add`, `git commit`, `git push`! Everything else is automatic or done in web dashboards.
