# Fix Remote Configuration

## Check and Fix Your Remote

If you added the remote with "YOUR_USERNAME" instead of your actual username, we need to fix it.

---

## Step 1: Check Current Remote

In PowerShell, run:

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git remote -v
```

**What you might see (WRONG):**
```
origin  https://github.com/YOUR_USERNAME/lead-magnet-generator.git (fetch)
origin  https://github.com/YOUR_USERNAME/lead-magnet-generator.git (push)
```

**What you SHOULD see (CORRECT):**
```
origin  https://github.com/mitchell-create/lead-magnet-generator.git (fetch)
origin  https://github.com/mitchell-create/lead-magnet-generator.git (push)
```

---

## Step 2: Remove Wrong Remote (If Needed)

If it shows the wrong URL (with "YOUR_USERNAME" or any other wrong URL), remove it:

```powershell
git remote remove origin
```

---

## Step 3: Add Correct Remote

Add the correct remote with your actual username:

```powershell
git remote add origin https://github.com/mitchell-create/lead-magnet-generator.git
```

---

## Step 4: Verify It's Correct

Check again:

```powershell
git remote -v
```

Should now show:
```
origin  https://github.com/mitchell-create/lead-magnet-generator.git (fetch)
origin  https://github.com/mitchell-create/lead-magnet-generator.git (push)
```

---

## Step 5: Make Sure All Files Are Committed

Check what's ready to push:

```powershell
git status
```

If you see "Untracked files" or "Changes not staged", you need to add and commit them:

```powershell
git add .
git commit -m "Initial commit: Lead Magnet Generator"
```

---

## Step 6: Push to GitHub

Now push your code:

```powershell
git branch -M main
git push -u origin main
```

---

## Quick Fix Commands (Copy-Paste All)

Run these in order:

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git remote -v
git remote remove origin
git remote add origin https://github.com/mitchell-create/lead-magnet-generator.git
git remote -v
git status
git add .
git commit -m "Initial commit: Lead Magnet Generator"
git branch -M main
git push -u origin main
```

---

## What Each Command Does

1. `git remote -v` - Check current remote (see what's wrong)
2. `git remote remove origin` - Remove the wrong remote
3. `git remote add origin ...` - Add correct remote with your username
4. `git remote -v` - Verify it's fixed
5. `git status` - See what files need to be committed
6. `git add .` - Stage all files
7. `git commit` - Commit the files
8. `git branch -M main` - Make sure branch is named "main"
9. `git push -u origin main` - Push to GitHub!

---

## After Pushing

1. Go to: https://github.com/mitchell-create/lead-magnet-generator
2. Refresh the page
3. You should see all your files! ✅

---

## Troubleshooting

**Error: "remote origin already exists"**
- That's fine, just run `git remote remove origin` first, then add it again

**Error: "Nothing to commit"**
- Good! Your files are already committed. Just push them:
  ```powershell
  git push -u origin main
  ```

**Error: Authentication failed**
- Create Personal Access Token: https://github.com/settings/tokens
- Use it as password when prompted
