# How to Restart PowerShell Properly

## Why Restart?

After installing Git (or any program that adds to PATH), you need to restart PowerShell so it picks up the new environment variables.

---

## Method 1: Close and Reopen (Recommended)

### Steps:
1. **Close the current PowerShell window** completely
   - Click the X button
   - Or type `exit` and press Enter

2. **Open a NEW PowerShell window:**
   - Press `Windows Key`
   - Type: `powershell`
   - Press Enter
   - OR right-click Start button → "Windows PowerShell"

3. **Verify Git is working:**
   ```powershell
   git --version
   ```
   Should show: `git version 2.x.x`

---

## Method 2: Use `refreshenv` (If you have Chocolatey)

If you have Chocolatey installed:
```powershell
refreshenv
git --version
```

---

## Method 3: Reload Environment Variables Manually

You can reload environment variables without closing PowerShell:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

Then verify:
```powershell
git --version
```

**Note:** This doesn't always work perfectly - Method 1 is more reliable.

---

## Verify Git is Working

After restarting, test with:

```powershell
git --version
```

**Expected output:**
```
git version 2.43.0 (or similar)
```

**If you still get an error:**
- Make sure Git was installed successfully
- Check if Git is in PATH: `$env:Path -split ';' | Select-String -Pattern 'git'`
- You may need to restart your computer

---

## Quick Checklist

- [ ] Close current PowerShell window completely
- [ ] Open a NEW PowerShell window
- [ ] Navigate to project: `cd C:\Users\ReadyPlayerOne\lead-magnet-generator`
- [ ] Test: `git --version`
- [ ] If it works → Continue with GitHub setup!

---

## After Restart

Once PowerShell restarts and Git works, you can proceed with:

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git init
git add .
git commit -m "Initial commit"
# ... rest of GitHub setup
```
