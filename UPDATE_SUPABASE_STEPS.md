# How to Update Supabase Schema

## ⚠️ Important: Supabase Updates vs Code Updates

**Two separate things:**

1. **Supabase Schema Update** = Run SQL in Supabase Dashboard (web interface)
2. **Code Changes** = Commit/push via PowerShell (deploys to Railway)

---

## Step 1: Update Supabase Schema (In Supabase Dashboard)

### Option A: If Table Already Exists (Add New Column)

1. Go to: **https://supabase.com/dashboard**
2. Select your project
3. Click **"SQL Editor"** (left sidebar)
4. Click **"New Query"**
5. **Paste and run this SQL:**

```sql
-- Add is_qualified column if it doesn't exist
ALTER TABLE lead_magnet_candidates 
ADD COLUMN IF NOT EXISTS is_qualified BOOLEAN DEFAULT FALSE;

-- Make qualified_at nullable (if it exists and isn't already nullable)
ALTER TABLE lead_magnet_candidates 
ALTER COLUMN qualified_at DROP NOT NULL;

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_lead_magnet_is_qualified ON lead_magnet_candidates(is_qualified);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_trigger ON lead_magnet_candidates(slack_trigger_id);
```

6. Click **"Run"** (or press Ctrl+Enter)
7. You should see: `Success. No rows returned` ✅

---

### Option B: If Creating Table Fresh

1. Go to Supabase Dashboard → **SQL Editor** → **New Query**
2. **Paste and run the entire `supabase_schema.sql` file**
3. This creates the table with all columns including `is_qualified`

---

## Step 2: Deploy Code Changes (In PowerShell)

**This deploys your Python code to Railway:**

```powershell
cd C:\Users\ReadyPlayerOne\lead-magnet-generator
git add .
git commit -m "Save all leads to Supabase first, then qualify"
git push
```

**What this does:**
- ✅ Updates Railway with new code
- ✅ Railway redeploys automatically
- ❌ Does NOT update Supabase schema (you did that in Step 1)

---

## Summary

| Step | Where | What It Does |
|------|-------|--------------|
| 1. Update Schema | **Supabase Dashboard** (web) | Adds `is_qualified` column to database |
| 2. Deploy Code | **PowerShell** (terminal) | Deploys Python code to Railway |

---

## Verify It Worked

**Check Supabase:**
1. Go to Supabase Dashboard → **Table Editor**
2. Click on `lead_magnet_candidates` table
3. You should see `is_qualified` column ✅

**Check Railway:**
1. Go to Railway Dashboard
2. See new deployment after git push
3. Check logs for any errors

---

**TL;DR:** Update Supabase schema in Supabase Dashboard (web), then deploy code via PowerShell! 🚀
