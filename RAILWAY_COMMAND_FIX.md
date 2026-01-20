# Railway Start Command - Two Options

## Option 1: Find in UI (Try First)

1. Click on your **service** in Railway
2. Look for **"Settings"** tab
3. In Settings, look for:
   - "Deploy" section
   - "Build & Start" section  
   - "Start Command" field

**If you find it:** Enter `python layer1_slack_listener.py`

---

## Option 2: Use railway.toml File (Easier!)

I've created a `railway.toml` file for you. This tells Railway what command to run.

### Steps:

1. **Commit and push the file:**
   ```powershell
   cd C:\Users\ReadyPlayerOne\lead-magnet-generator
   git add railway.toml
   git commit -m "Add Railway start command configuration"
   git push
   ```

2. **Railway will automatically:**
   - Detect the `railway.toml` file
   - Use the start command from it
   - Restart your service with the new command

---

## Verify It's Working

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click on latest deployment → **"View Logs"**
5. You should see:
   ```
   Starting Slack listener on port 3000
   ```

If you see that, it's working! ✅

---

## What the railway.toml File Does

```toml
[build]
builder = "nixpacks"  # Uses Railway's auto-detection for Python

[deploy]
startCommand = "python layer1_slack_listener.py"  # What to run
```

This file tells Railway exactly how to start your app, so you don't need to set it in the UI!

---

## Recommended: Use railway.toml

**Why it's better:**
- ✅ Version controlled (in your code)
- ✅ Works the same every time
- ✅ No need to configure in UI
- ✅ Team members can see it in GitHub

**Just commit and push it, and Railway will use it automatically!**
