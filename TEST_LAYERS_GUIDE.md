# Testing Each Layer Locally

## ✅ Layer 1: PASSED
**Status:** Working perfectly!
**What it tests:** Natural language parsing for Slack input
**Command:**
```powershell
py -3.12 layer1_slack_listener.py
```

---

## Next: Test Layer 2 (Prospeo Connection)

**What it tests:** Connecting to Prospeo API and fetching leads

**Command:**
```powershell
py -3.12 layer2_prospeo_client.py
```

**Expected:**
- Will try to fetch first page of leads from Prospeo
- **Note:** Requires valid PROSPEO_API_KEY in .env file
- If API key is valid, you'll see JSON data
- If API key is missing/invalid, you'll see an error

**What to check:**
- ✅ If you see JSON data with leads = Success!
- ❌ If you see authentication error = Check your .env file has correct PROSPEO_API_KEY

---

## Test Layer 3 (AI Judge)

**What it tests:** Using OpenRouter to qualify a lead

**Command:**
```powershell
py -3.12 layer3_ai_judge.py
```

**Expected:**
- Will test qualification on a mock lead
- **Note:** Requires valid OPENROUTER_API_KEY in .env file
- Will send a test prompt to OpenRouter
- Should return YES or NO

**What to check:**
- ✅ If you see "Qualification Result: YES" or "NO" = Success!
- ❌ If you see authentication error = Check your .env file has correct OPENROUTER_API_KEY

---

## Test Layer 4 (Processing Loop)

**What it tests:** The main loop that processes leads

**Command:**
```powershell
py -3.12 layer4_lead_processor.py
```

**Expected:**
- Will attempt to run the full processing loop
- **Note:** Requires both PROSPEO_API_KEY and OPENROUTER_API_KEY
- Uses small test limits (5 qualified leads, max 50 processed)
- **Warning:** This will make real API calls and may cost money!

**What to check:**
- ✅ If you see "Qualified Leads: X" = Success!
- ⚠️ Monitor the output - it will show progress

---

## Test Layer 5 (Output)

**What it tests:** CSV generation and Supabase insertion

**Command:**
```powershell
py -3.12 layer5_output.py
```

**Expected:**
- Will generate a test CSV file
- Will try to insert test data to Supabase
- **Note:** Requires valid SUPABASE_URL and SUPABASE_KEY in .env file
- CSV file will be created in `./output/` folder

**What to check:**
- ✅ If you see "CSV generated: output/qualified_leads_XXXXXX.csv" = Success!
- ✅ Check the output folder for the CSV file
- Supabase insert may skip if not configured (that's OK for testing)

---

## Test Full Application

**What it tests:** The complete pipeline end-to-end

**Command:**
```powershell
py -3.12 main.py
```

**Expected:**
- Runs the complete workflow with test data
- Requires all API keys to be configured
- **Warning:** This will make real API calls and may cost money!

---

## Testing Order (Recommended)

1. ✅ **Layer 1** - Already tested, working!
2. ⏭️ **Layer 5** - Safe to test (just creates CSV, no API calls)
3. ⏭️ **Layer 2** - Test Prospeo connection
4. ⏭️ **Layer 3** - Test OpenRouter connection
5. ⏭️ **Layer 4** - Test full processing (uses API calls)
6. ⏭️ **Main** - Test complete application (uses API calls)

---

## Notes

- **Layer 1 & 5** don't require API keys (safe to test anytime)
- **Layer 2, 3, 4** require API keys and will make real API calls
- Make sure your `.env` file has all API keys before testing layers that need them
- API calls may incur costs (Prospeo and OpenRouter)

---

## Quick Test Commands

```powershell
# Safe tests (no API calls)
py -3.12 layer1_slack_listener.py
py -3.12 layer5_output.py

# API tests (requires .env with keys)
py -3.12 layer2_prospeo_client.py
py -3.12 layer3_ai_judge.py
py -3.12 layer4_lead_processor.py

# Full test
py -3.12 main.py
```
