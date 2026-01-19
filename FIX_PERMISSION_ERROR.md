# Fix: Permission Denied Error

## Problem

You're trying to run `git init` in `C:\WINDOWS\system32`, which is a protected system directory.

**Error:** `C:/Windows/System32/.git: Permission denied`

## Solution

You need to navigate to your project folder first!

---

## Step-by-Step Fix

### Step 1: Navigate to Your Project Folder

Run this command:

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

### Step 2: Verify You're in the Right Place

Check your current directory:

```powershell
pwd
```

**OR**

```powershell
Get-Location
```

**Should show:**
```
C:\Users\ReadyPlayerOne\lead-magnet-generator
```

### Step 3: Now Run Git Commands

Once you're in the project folder, THEN run:

```powershell
git init
```

---

## Quick Checklist

- [ ] Navigate to project: `cd C:\Users\ReadyPlayerOne\lead-magnet-generator`
- [ ] Verify location: `pwd` (should show project folder)
- [ ] Now run: `git init`
- [ ] Should work! ✅

---

## Visual Guide

**WRONG (what you did):**
```
PS C:\WINDOWS\system32> git init
❌ Permission denied - you're in system32!
```

**RIGHT (what to do):**
```
PS C:\WINDOWS\system32> cd C:\Users\ReadyPlayerOne\lead-magnet-generator
PS C:\Users\ReadyPlayerOne\lead-magnet-generator> git init
✅ Success!
```

---

## Common Mistake

If you close PowerShell and reopen it, you might start in `system32` again. Always navigate to your project folder first!

---

## Pro Tip

Create a shortcut or alias:
```powershell
# Add to your PowerShell profile
function goto-project {
    cd C:\Users\ReadyPlayerOne\lead-magnet-generator
}
```

Then you can just type: `goto-project`
