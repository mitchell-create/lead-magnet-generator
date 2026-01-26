# Force Update requirements.txt

## Issue
requirements.txt is already committed, but Railway isn't installing beautifulsoup4. 

Possible causes:
1. The file in GitHub doesn't actually have the dependencies
2. Railway cached the old version
3. Need to force an update

## Solution: Force Update requirements.txt

Even though it's already committed, let's make a small change to force Railway to rebuild:

### Option 1: Touch the file (add a blank line)
Add a blank line at the end of requirements.txt, then commit and push.

### Option 2: Verify GitHub version
Check your GitHub repository to see if requirements.txt actually has beautifulsoup4.

### Option 3: Explicitly add all dependencies again
We can re-add the dependencies to ensure they're there.

## Quick Fix

**In PowerShell:**
```powershell
# Add a blank line to requirements.txt (just to force change)
Add-Content -Path requirements.txt -Value ""

# Then commit and push
git add requirements.txt
git commit -m "Force update requirements.txt for Railway rebuild"
git push
```

This will trigger a rebuild and Railway should install all dependencies.
