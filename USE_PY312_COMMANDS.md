# How to Use Python 3.12 - Important!

## Problem
The `python` command points to the Windows Store stub (which doesn't work).
But Python 3.12.10 IS installed! You just need to use `py -3.12` instead.

## Solution: Use `py -3.12` Instead of `python`

### ✅ Correct Commands:

**Instead of:** `python --version`  
**Use:** `py -3.12 --version`

**Instead of:** `python -m pip install ...`  
**Use:** `py -3.12 -m pip install ...`

**Instead of:** `python test_python.py`  
**Use:** `py -3.12 test_python.py`

---

## Step-by-Step Instructions

### STEP 1: Verify Python 3.12

```powershell
py -3.12 --version
```

Should show: `Python 3.12.10` (or 3.12.x)

---

### STEP 2: Upgrade pip

```powershell
py -3.12 -m pip install --upgrade pip
```

---

### STEP 3: Install Dependencies

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
py -3.12 -m pip install -r requirements.txt
```

---

### STEP 4: Test Everything

```powershell
py -3.12 test_python.py
```

---

## Quick Reference

**All commands use `py -3.12` instead of `python`:**

```powershell
# Check version
py -3.12 --version

# Install packages
py -3.12 -m pip install package_name
py -3.12 -m pip install -r requirements.txt

# Run scripts
py -3.12 layer1_slack_listener.py
py -3.12 main.py
py -3.12 test_python.py
```

---

## Why This Happens

Windows has a "python" alias that points to the Microsoft Store.
The actual Python installation uses the `py` launcher instead.
This is normal and actually better because you can easily switch between Python versions!

---

## Optional: Fix `python` Command (If You Want)

If you really want `python` to work, you need to disable the Windows Store alias:

1. Press `Windows Key`
2. Type: "App execution aliases"
3. Click "App execution aliases"
4. Find "python.exe" and "python3.exe"
5. Turn OFF both toggles
6. Restart PowerShell

But honestly, using `py -3.12` is perfectly fine and actually better!
