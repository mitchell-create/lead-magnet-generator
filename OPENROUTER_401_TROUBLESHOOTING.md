# Fixing OpenRouter 401 (wholesale_partner_response shows "Error: 401")

---

## What are we doing here? (plain English)

Your lead-magnet app uses **OpenRouter** (an AI service) to decide if a company is a good fit. To talk to OpenRouter, the app needs a secret **API key** — like a password — that proves you’re allowed to use it.

Right now the app doesn’t have a valid key (or OpenRouter can’t see it). So every time it tries to ask OpenRouter “Is this company a wholesale partner?”, OpenRouter says “Who are you? I don’t recognize you” — that’s the **401 error**. The app then saves that error message into Supabase, which is why you see `Error: 401` in `wholesale_partner_response`.

**What we’re doing:** We’re going to get a valid OpenRouter key, put it in a **config file** called `.env`, and make sure the app actually uses it. Once that’s done, the app can talk to OpenRouter, and you’ll see real answers (like “YES” or “NO”) instead of “Error: 401”.

---

## Where is the .env **file**? (it’s a file, not a folder)

**`.env` is a file**, not a folder. It lives **inside** your project folder.

- **Your project folder** is:  
  `C:\Users\ReadyPlayerOne\lead-magnet-generator`  
  That’s the folder that contains things like `main.py`, `diagnose_openrouter.py`, `layer3_ai_judge.py`, etc.

- **The `.env` file** is **inside** that folder. So its full path is:  
  `C:\Users\ReadyPlayerOne\lead-magnet-generator\.env`

**How to find or create it:**

1. Open **File Explorer**.
2. Go to `C:\Users\ReadyPlayerOne\lead-magnet-generator` (or use the sidebar in Cursor and open that folder).
3. Look for a file named **`.env`** (the name starts with a dot).  
   - If you see it, **double‑click it** to open it in Notepad or Cursor.  
   - If you **don’t** see it:  
     - Look for a file named **`.env.example`**. If it exists, **copy** it, **paste** it in the same folder, and **rename** the copy to **`.env`**.  
     - If there’s no `.env.example`, create a **new text file** in that folder and name it exactly **`.env`** (including the dot at the start).
4. Inside `.env` you’ll add a line like:  
   `OPENROUTER_API_KEY=sk-or-v1-your-key-here`  
   (That’s the “config” the app reads so it can talk to OpenRouter.)

**Summary:** The “.env folder” doesn’t exist — it’s the **.env file** in **`C:\Users\ReadyPlayerOne\lead-magnet-generator`**. Open that folder, find or create the file named `.env`, and edit that file.

---

## Where do I start? (PowerShell or any terminal)

**Yes — use PowerShell** (or Command Prompt, or the terminal in Cursor/VS Code). All the commands below work in PowerShell.

1. **Open PowerShell**
   - Press `Win + X` → choose **Windows PowerShell** or **Terminal**, or  
   - Open **Cursor**, then **Terminal → New Terminal** (it often uses PowerShell).

2. **Go to your project folder**
   - Type (use your real path if different):
     ```
     cd C:\Users\ReadyPlayerOne\lead-magnet-generator
     ```
   - Press Enter. You should be “inside” the folder that has `diagnose_openrouter.py` and `.env`.

3. **Then follow the steps below** — Step 1 (get key), Step 2 (put it in `.env`, run the diagnostic), etc.

---

## Next steps (do these in order)

### Step 1: Get an OpenRouter API key

1. Go to **https://openrouter.ai**
2. Sign in or create an account.
3. Open **Keys** (or **Settings → API Keys**).
4. Create a new API key.
5. Copy the key. It usually looks like: `sk-or-v1-xxxxxxxxxxxx...`
   - Use an **OpenRouter** key, not an OpenAI key.

---

### Step 2: Test the key on your computer

1. Open your project folder in File Explorer (same folder that has `diagnose_openrouter.py`).  
   Or stay in PowerShell — you’re already there if you did “Where do I start?” above.
2. Open the `.env` file in that folder in Notepad or Cursor (create it from `.env.example` if it doesn’t exist).
3. Add or edit this line (paste your real key, no quotes):
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```
4. Save the file.
5. In **PowerShell** (or the same terminal you used earlier), make sure you’re in the project folder, then run:
   ```
   python diagnose_openrouter.py
   ```
6. Check the result:
   - **"OpenRouter request: SUCCESS"** → Key works. Go to Step 3.
   - **"OPENROUTER_API_KEY: NOT SET or empty"** → The app is not reading `.env`. Fix the key in `.env` and run the script again from the **project folder**.
   - **"OpenRouter request: FAILED"** with 401 → Key is wrong, expired, or revoked. Create a new key at openrouter.ai and update `.env`, then run the script again.

---

### Step 3: Use the same key where the app runs

The app must see the key in **the environment it actually uses** when you run lead searches.

**If you run the app on your computer (e.g. `python main.py` or a Slack listener):**

- The key must be in the `.env` file in the project folder.
- You already did that in Step 2. You’re done with this step.

**If you run the app on Railway (or another host):**

1. Open your project on Railway.
2. Go to the **Variables** (or **Environment**) tab.
3. Add or edit:
   - **Name:** `OPENROUTER_API_KEY`
   - **Value:** the same key that worked in Step 2 (paste it, no quotes).
4. Save.
5. Redeploy or restart the app so it loads the new variable.

---

### Step 4: Confirm it’s fixed

1. Run a **new** lead search (e.g. from Slack or `python main.py` with test data).
2. In Supabase, look at **new** rows (from this run).
3. In `wholesale_partner_response` you should see **"YES"** or **"NO"**, not `"Error: 401"` or `"Unauthorized"`.

If you still see 401 on new rows:

- If the diagnostic **succeeds** on your computer but the app on Railway still shows 401, the key is missing or wrong in Railway’s Variables. Repeat Step 3 and restart/redeploy.
- If the diagnostic **fails** on your computer, fix that first (new key, correct `.env`, run script from project folder).

---

## Quick reference

| Where you see the problem | What to do |
|---------------------------|------------|
| Diagnostic says "NOT SET" | Put `OPENROUTER_API_KEY=your-key` in `.env` in the project folder and run the script from that folder. |
| Diagnostic says "FAILED" with 401 | Use a valid OpenRouter key (from openrouter.ai). Create a new one if needed, then update `.env`. |
| Diagnostic succeeds, Supabase still 401 | The key is not set (or is wrong) where the app runs. For Railway, set `OPENROUTER_API_KEY` in Variables and redeploy. |
| You use Railway | The key in **Railway Variables** is what counts. `.env` on your PC is only for local runs and the diagnostic. |

---

## Why this happens (short)

- **401** = “Unauthorized.” OpenRouter is rejecting the request because the API key is missing, wrong, or invalid.
- **Scraping** runs before the OpenRouter call. It does not cause 401. Fixing the key fixes the 401.
