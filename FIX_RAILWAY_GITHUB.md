# Fix: Railway "Repository not found" Error

## Problem
Railway can't access your GitHub repository, likely due to:
- GitHub app integration disconnected
- Repository permissions changed
- Need to reconnect GitHub account

## Solution Options

### Option 1: Reconnect GitHub in Railway (Recommended)

1. **Go to Railway Dashboard**
2. **Click your profile icon** (top right)
3. **Go to "Settings"** or "Account Settings"
4. **Find "GitHub" or "Integrations"** section
5. **Disconnect and reconnect** your GitHub account
6. **Re-authorize Railway** to access your repositories
7. **Make sure your repository** (`lead-magnet-generator`) is selected/allowed

### Option 2: Check Repository Settings in GitHub

1. **Go to GitHub** → Your repository
2. **Settings** → **Integrations** → **GitHub Apps**
3. **Find "Railway"** in the list
4. **Check if it has access** to your repo
5. **Grant access** if needed

### Option 3: Re-link Repository in Railway Service

1. **Railway Dashboard** → Your Service
2. **Settings** tab
3. **Find "Repository" or "Source"** section
4. **Click "Change" or "Connect Repository"**
5. **Re-select your repository**
6. **Re-authenticate if prompted**

### Option 4: Manual Deploy (Temporary Workaround)

If you can't reconnect, you can trigger a redeploy by making a small code change:

1. **Make a tiny change** (add a comment or space)
2. **Commit and push** via PowerShell:
   ```powershell
   git add .
   git commit -m "Trigger redeploy"
   git push
   ```
3. Railway should detect the push and redeploy

---

## Quick Fix Steps

**Most common solution:**

1. Railway Dashboard → **Settings** (your profile)
2. **GitHub Integration** → **Disconnect**
3. **Reconnect GitHub** → Authorize
4. **Select repository** → Grant access
5. **Go back to service** → Try redeploy again

---

## Alternative: Force Redeploy via Git Push

If Railway integration is broken, just push a change to trigger redeploy:

**In PowerShell:**
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
# Make a tiny change (or just commit current state)
git commit --allow-empty -m "Trigger Railway redeploy"
git push
```

This will trigger Railway to redeploy automatically (if the integration is working).

---

## Check Railway Service Settings

1. Railway Dashboard → Your Service
2. **Settings** tab
3. Look for:
   - "Source" or "Repository" connection
   - GitHub App status
   - Deployment triggers

---

## Need Help?

If none of these work, check:
- Railway support documentation
- Your Railway account permissions
- Whether you're using the correct Railway account

The key is re-establishing the Railway ↔ GitHub connection!
