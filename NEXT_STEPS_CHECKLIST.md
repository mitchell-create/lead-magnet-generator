# Next Steps Checklist ✅

## Step 1: Wait for Railway Deployment ⏳

**Status:** Automatic (happening now)

1. Go to **Railway Dashboard**
2. Check **Deployments** tab
3. Wait for latest deployment to complete (2-3 minutes)
4. Look for: ✅ "Deployed successfully"

**Check logs** to see:
- Dependencies installing (beautifulsoup4, lxml, html5lib)
- Server starting successfully

---

## Step 2: Verify OpenRouter Model Setting 🔧

**Location:** Railway Dashboard → Your Service → **Variables**

**Check if `OPENROUTER_MODEL` is set:**
- ✅ If exists: Verify value is `gpt-oss-20b` (or correct model name)
- ❌ If missing: Add it:
  - Key: `OPENROUTER_MODEL`
  - Value: `gpt-oss-20b` (or exact model name from OpenRouter)

**To find exact model name:**
- Check OpenRouter docs: https://openrouter.ai/models
- Or use their API to list models

---

## Step 3: Test End-to-End 🧪

**Test in Slack:**

1. Send test command:
   ```
   /lead-magnet keywords=golf retailers,outdoor gear stores | seniority=Founder,Owner
   ```

2. **What to watch for:**
   - ✅ Bot responds: "Lead search initiated!"
   - ✅ Railway logs show Prospeo API calls
   - ✅ Railway logs show website scraping attempts
   - ✅ Railway logs show AI qualification results
   - ✅ Leads appear in Supabase

---

## Step 4: Monitor Railway Logs 📊

**Location:** Railway Dashboard → Your Service → **Deployments** → Latest → **Logs**

**Look for:**
1. ✅ **Prospeo API calls**
   - "Fetching Prospeo page X"
   - "Successfully fetched Y persons"

2. ✅ **Website scraping**
   - "Scraping website: https://..."
   - "Successfully scraped..."
   - Or warnings if scraping fails (that's OK, will fall back)

3. ✅ **AI qualification**
   - "Qualifying: [Company Name]"
   - "Qualification result: YES/NO"

4. ✅ **Supabase saves**
   - "Saved lead X to Supabase"
   - "Successfully inserted Y records"

5. ❌ **Any errors**
   - Check what failed and why

---

## Step 5: Verify Supabase Data 💾

**Location:** Supabase Dashboard → **Table Editor** → `lead_magnet_candidates`

**Check:**
1. ✅ New rows are being inserted
2. ✅ `is_qualified` column exists
3. ✅ Both qualified and unqualified leads are saved
4. ✅ Website URLs are in the data
5. ✅ Company descriptions are present

**Query example:**
```sql
SELECT 
  company_name, 
  is_qualified, 
  company_website,
  created_at
FROM lead_magnet_candidates
ORDER BY created_at DESC
LIMIT 10;
```

---

## Step 6: Test CSV Generation 📄

**Check Railway logs for:**
- "CSV file generated: ..."

**Note:** CSV is generated on Railway's server. You can:
- Download via Railway file system (if accessible)
- Or add code to save to cloud storage (future enhancement)
- Or query Supabase directly for leads

---

## Step 7: Verify Website Scraping 🔍

**Check logs for specific examples:**

**Good signs:**
- ✅ "Scraping website: https://..."
- ✅ "Successfully scraped..."
- ✅ Navigation items extracted
- ✅ Brand mentions found

**If scraping fails:**
- ⚠️ That's OK - system falls back to company description
- ⚠️ Some sites block scrapers (expected)
- ⚠️ AI can still qualify based on description

---

## Step 8: Test Different Search Criteria 🎯

**Try various searches:**

1. **Simple:**
   ```
   /lead-magnet keywords=retailers | seniority=Founder
   ```

2. **Multiple keywords:**
   ```
   /lead-magnet keywords=golf pro shops,sporting goods stores | location=United States
   ```

3. **With industry:**
   ```
   /lead-magnet industry=Retail | keywords=outdoor gear | verified-email=true
   ```

4. **Complex:**
   ```
   /lead-magnet industry=Retail,E-commerce | location=California,New York | seniority=C-Suite,VP | verified-email=true
   ```

---

## Troubleshooting 🔧

### If Prospeo fails:
- Check `PROSPEO_API_KEY` in Railway Variables
- Check Prospeo API status
- Verify filter format

### If scraping fails:
- Check logs for error messages
- Some sites block scrapers (normal)
- System will fall back to description

### If AI fails:
- Check `OPENROUTER_API_KEY` in Railway Variables
- Verify `OPENROUTER_MODEL` is correct
- Check OpenRouter API status

### If Supabase fails:
- Check `SUPABASE_URL` and `SUPABASE_KEY` in Railway Variables
- Verify table exists and has `is_qualified` column
- Check Supabase dashboard for errors

---

## ✅ Success Criteria

You'll know everything works when:

1. ✅ Railway deployment completes successfully
2. ✅ Test command in Slack gets response
3. ✅ Railway logs show all steps working:
   - Prospeo API calls
   - Website scraping
   - AI qualification
   - Supabase saves
4. ✅ Leads appear in Supabase table
5. ✅ Qualified leads are marked (`is_qualified = TRUE`)
6. ✅ Unqualified leads are also saved (`is_qualified = FALSE`)

---

## 🎯 Ready to Test!

Start with **Step 1** - wait for Railway to finish deploying, then work through the checklist!
