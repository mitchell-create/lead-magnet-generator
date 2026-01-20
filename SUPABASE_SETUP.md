# Supabase Setup Guide

## Step 1: Create the Database Table

### In Supabase Dashboard:
1. Go to: **https://supabase.com/dashboard**
2. Select your project (or create one if needed)
3. Click **"SQL Editor"** in the left sidebar
4. Click **"New Query"**

### Run This SQL:

```sql
-- Create table for lead magnet candidates
CREATE TABLE IF NOT EXISTS lead_magnet_candidates (
    id BIGSERIAL PRIMARY KEY,
    person_name TEXT,
    person_email TEXT,
    person_title TEXT,
    person_linkedin_url TEXT,
    company_name TEXT,
    company_domain TEXT,
    company_website TEXT,
    company_description TEXT,
    company_industry TEXT,
    company_size TEXT,
    company_location TEXT,
    qualified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    search_criteria TEXT,
    qualification_criteria JSONB,
    slack_user_id TEXT,
    slack_channel_id TEXT,
    slack_trigger_id TEXT,
    raw_slack_input TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_qualified_at ON lead_magnet_candidates(qualified_at);
CREATE INDEX IF NOT EXISTS idx_slack_channel ON lead_magnet_candidates(slack_channel_id);
```

5. Click **"Run"** (or press Ctrl+Enter)
6. You should see: `Success. No rows returned`

---

## Step 2: Verify Your Supabase Credentials

### Get Your Credentials:
1. In Supabase Dashboard → **"Project Settings"** (gear icon)
2. Click **"API"** in the left sidebar
3. You'll see:
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **Service Role Key** (anon key): `eyJhbGc...` (long JWT token)

### What You Already Have:
- **SUPABASE_URL**: `https://utdwvqfnzkcysdsbsvwv.supabase.co`
- **SUPABASE_KEY**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your service role key)

---

## Step 3: Add to Railway Environment Variables

### In Railway:
1. Go to **Railway Dashboard** → Your Service
2. Click **"Variables"** tab
3. Verify these are set:

| Variable | Value |
|----------|-------|
| `SUPABASE_URL` | `https://utdwvqfnzkcysdsbsvwv.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0ZHd2cWZuemtjeXNkc2Jzdnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODc4NDk4OCwiZXhwIjoyMDg0MzYwOTg4fQ.tfYTjn7z0lbEJx7NnGeivyDPUrbqFHwOy0RgcO4IERs` |

### If Missing:
1. Click **"New Variable"**
2. Add each variable (URL and KEY)
3. Click **"Save"**
4. Railway will redeploy automatically

---

## Step 4: Verify Table Was Created

### In Supabase Dashboard:
1. Click **"Table Editor"** (left sidebar)
2. You should see: **`lead_magnet_candidates`** table
3. Click on it to view structure

### Check Columns:
The table should have these columns:
- `id` (primary key)
- `person_name`, `person_email`, `person_title`, etc.
- `qualified_at`
- `created_at`
- etc.

---

## Step 5: Test the Connection

After Railway redeploys with Supabase credentials:
1. Run a test command in Slack:
   ```
   /lead-magnet Target: Software companies | Criteria: Size>10
   ```
2. Check Railway logs for:
   - `Supabase client initialized`
   - `Successfully inserted X leads into Supabase`
   - Or any Supabase errors

3. Check Supabase:
   - Go to **Table Editor** → `lead_magnet_candidates`
   - You should see new rows appear!

---

## Troubleshooting

### "Table doesn't exist" Error:
- ✅ Run the SQL schema in Supabase SQL Editor
- ✅ Verify table name is exactly: `lead_magnet_candidates`

### "Authentication failed" Error:
- ✅ Check SUPABASE_KEY is the **Service Role Key** (not anon key)
- ✅ Verify the key is correct in Railway Variables
- ✅ Key should start with `eyJhbGc...`

### "Connection refused" Error:
- ✅ Check SUPABASE_URL is correct (should end with `.supabase.co`)
- ✅ No trailing slash in URL
- ✅ Verify URL is accessible

---

## Quick Reference

**Supabase URL:**
```
https://utdwvqfnzkcysdsbsvwv.supabase.co
```

**Railway Variables Needed:**
- `SUPABASE_URL`
- `SUPABASE_KEY`

**Table Name:**
```
lead_magnet_candidates
```

---

## After Setup

Once done:
1. ✅ Table created in Supabase
2. ✅ Variables set in Railway
3. ✅ Railway redeployed
4. ✅ Test with `/lead-magnet` command
5. ✅ Check Supabase table for results!
