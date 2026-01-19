# Install Python 3.12 for Local Development

## Current Status
- ❌ Python 3.14.2 installed (has compatibility issues)
- ❌ Python 3.12 NOT installed
- ⚠️ OpenAI and Supabase imports fail locally

## Solution: Install Python 3.12

### Step 1: Download Python 3.12
1. Go to: https://www.python.org/downloads/release/python-31212/
2. Scroll to "Files" section
3. Download: **Windows installer (64-bit)**
   - File: `python-3.12.12-amd64.exe`

### Step 2: Install Python 3.12
1. Run the installer
2. ⚠️ **IMPORTANT:** Check "Add Python 3.12 to PATH"
3. Click "Install Now"
4. Wait for installation to complete

### Step 3: Verify Installation
Open a NEW PowerShell window and run:
```powershell
py -3.12 --version
```
Should show: `Python 3.12.12`

### Step 4: Install Dependencies for Python 3.12
```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
py -3.12 -m pip install -r requirements.txt
```

### Step 5: Test Imports
```powershell
py -3.12 -c "import openai; import supabase; print('✅ All imports work!')"
```

### Step 6: Update Railway Configuration

In Railway, you can specify Python version by creating a `runtime.txt` file:

**Create `runtime.txt` in project root:**
```
python-3.12.12
```

Or Railway will auto-detect from your `requirements.txt` (which we should update).
