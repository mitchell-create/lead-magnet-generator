# Detailed Steps: Verify Python & Install Dependencies

## STEP 1: Verify Python 3.12 Installation

### Why We Need This
We need to make sure Python 3.12.10 is properly installed and accessible before we install the project dependencies.

---

### Step 1.1: Open a NEW PowerShell Window

**IMPORTANT:** You MUST open a **NEW** PowerShell window because:
- The old window might still be using the old Python path
- New windows pick up the updated PATH environment variable

**How to open PowerShell:**
1. Press `Windows Key` on your keyboard
2. Type: `powershell`
3. Click on "Windows PowerShell" (or "PowerShell")
4. A blue/black terminal window will open

**OR:**
1. Right-click the Start button
2. Select "Windows PowerShell" or "Terminal"

---

### Step 1.2: Navigate to Your Project Folder

Once PowerShell is open, you'll see a prompt that looks like:
```
PS C:\Users\ReadyPlayerOne>
```

**Type this command exactly:**
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

**Press Enter**

You should now see:
```
PS C:\Users\ReadyPlayerOne\lead-magnet-generator>
```

This means you're in the correct folder.

---

### Step 1.3: Check Python Version

**Type this command:**
```powershell
python --version
```

**Press Enter**

**Expected output:**
```
Python 3.12.10
```

✅ **Success!** If you see `Python 3.12.10` (or `3.12.x`), Python is installed correctly.

---

### Step 1.4: Alternative Check (If `python --version` doesn't work)

If the above command shows an error or still shows Python 3.14, try:

**Type this command:**
```powershell
py -3.12 --version
```

**Press Enter**

**Expected output:**
```
Python 3.12.10
```

✅ **Success!** If this works, Python 3.12 is installed but you'll use `py -3.12` instead of `python` for commands.

---

### Troubleshooting Step 1

**Problem:** `python --version` says "Python 3.14.2" or shows old version
**Solution:** 
1. Close ALL PowerShell windows
2. Open a NEW PowerShell window
3. Try again

**Problem:** `python` command not found
**Solution:**
1. Reinstall Python 3.12.10
2. Make sure "Add Python 3.12 to PATH" is checked during installation
3. Restart your computer if needed

**Problem:** Both `python` and `py -3.12` don't work
**Solution:**
1. Check if Python is installed: `Get-Command python` or `Get-Command py`
2. If nothing found, reinstall Python 3.12.10

---

## STEP 2: Install Project Dependencies

### Why We Need This
Your project needs specific Python libraries (packages) to work. These are listed in `requirements.txt`. We need to install them for Python 3.12.

---

### Step 2.1: Make Sure You're in the Right Folder

You should still be in the project folder from Step 1.2. Verify by checking your prompt:

```
PS C:\Users\ReadyPlayerOne\lead-magnet-generator>
```

If you're NOT in this folder, type:
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
```

---

### Step 2.2: Upgrade pip (Package Installer)

Before installing dependencies, let's make sure `pip` (Python's package installer) is up to date.

**Type this command:**
```powershell
python -m pip install --upgrade pip
```

**Press Enter**

**What you'll see:**
- It will download and install the latest pip
- You'll see lines like: "Requirement already satisfied" or "Successfully installed pip-XX.X.X"

**Expected output:**
```
Collecting pip
  Downloading pip-XX.X.X-py3-none-any.whl (X.X MB)
Installing collected packages: pip
Successfully installed pip-XX.X.X
```

✅ **Success!** pip is now up to date.

**If you're using `py -3.12` instead of `python`, use:**
```powershell
py -3.12 -m pip install --upgrade pip
```

---

### Step 2.3: Install All Dependencies

Now we'll install all the libraries your project needs.

**Type this command:**
```powershell
python -m pip install -r requirements.txt
```

**Press Enter**

**What will happen:**
- Python will read the `requirements.txt` file
- It will download and install each library listed:
  - slack-bolt
  - flask
  - requests
  - supabase
  - openai
  - python-dotenv

**Expected output:**
```
Collecting slack-bolt==1.18.0
  Downloading slack_bolt-1.18.0-py2.py3-none-any.whl (194 kB)
Collecting flask==3.0.0
  Downloading flask-3.0.0-py3-none-any.whl (99 kB)
...
Installing collected packages: slack-sdk, werkzeug, jinja2, ... slack-bolt, flask, requests, supabase, openai, python-dotenv
Successfully installed slack-bolt-1.18.0 flask-3.0.0 requests-2.31.0 supabase-2.0.0 openai-1.3.0 python-dotenv-1.0.0
```

**This might take 1-3 minutes** - be patient!

✅ **Success!** When you see "Successfully installed" for all packages, you're done!

**If you're using `py -3.12` instead of `python`, use:**
```powershell
py -3.12 -m pip install -r requirements.txt
```

---

### Step 2.4: Verify Installation

Let's make sure everything installed correctly.

**Type this command:**
```powershell
python test_python.py
```

**Press Enter**

**Expected output:**
```
============================================================
Python Version Check
============================================================
Python Version: 3.12.10 (tags/v3.12.10:...)
Python Executable: C:\...\python.exe

Testing Core Libraries:
------------------------------------------------------------
[OK] slack_bolt      (Slack integration)
[OK] flask           (Flask web server)
[OK] requests        (HTTP requests)
[OK] openai          (OpenAI/OpenRouter API)
[OK] supabase        (Supabase database)
[OK] dotenv          (Environment variables)

============================================================
Summary
============================================================
[SUCCESS] All libraries imported successfully!
[SUCCESS] Your Python version is compatible
============================================================
```

✅ **Perfect!** If all libraries show `[OK]`, everything is installed correctly!

**If you're using `py -3.12`, use:**
```powershell
py -3.12 test_python.py
```

---

### Troubleshooting Step 2

**Problem:** "pip: command not found" or "python: No module named pip"
**Solution:**
1. Make sure Python 3.12.10 is properly installed
2. Try: `python -m ensurepip --upgrade`
3. Then try Step 2.2 again

**Problem:** Installation fails with permission errors
**Solution:**
1. Close PowerShell
2. Right-click PowerShell icon
3. Select "Run as Administrator"
4. Navigate to project folder again
5. Try installation again

**Problem:** Some packages fail to install
**Solution:**
1. Make sure you're using Python 3.12 (check with `python --version`)
2. Try installing individually: `python -m pip install slack-bolt flask requests`
3. Check your internet connection
4. Some packages might need Visual C++ Redistributable (Windows will prompt you)

**Problem:** Test script shows errors for openai or supabase
**Solution:**
1. Make sure you're using Python 3.12, not 3.14
2. Try: `python -m pip uninstall openai supabase` then `python -m pip install openai supabase`
3. Check that you're in the correct project folder

---

## Quick Reference: Commands Summary

**After installation, these are the commands you'll use:**

```powershell
# Navigate to project
cd C:\Users\ReadyPlayerOne\lead-magnet-generator

# Check Python version
python --version

# Install/upgrade packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Test everything
python test_python.py

# Run your app
python layer1_slack_listener.py
python main.py
```

**If you need to use `py -3.12` instead:**
```powershell
# Replace 'python' with 'py -3.12' in all commands
py -3.12 --version
py -3.12 -m pip install -r requirements.txt
py -3.12 test_python.py
py -3.12 layer1_slack_listener.py
```

---

## What's Next?

Once Steps 1 and 2 are complete:
✅ Python 3.12.10 is installed and working
✅ All dependencies are installed
✅ You can test locally before deploying

**Next steps:**
- Test individual layers (Layer 1, Layer 2, etc.)
- Deploy to Railway
- Configure Slack integration
