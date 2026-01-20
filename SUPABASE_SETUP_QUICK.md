# Quick Supabase Setup

## ✅ Step 1: Create Table in Supabase

1. Go to: **https://supabase.com/dashboard**
2. Select your project
3. Click **"SQL Editor"** → **"New Query"**
4. **Paste and Run** this SQL:

```sql
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

CREATE INDEX IF NOT EXISTS idx_qualified_at ON lead_magnet_candidates(qualified_at);
CREATE INDEX IF NOT EXISTS idx_slack_channel ON lead_magnet_candidates(slack_channel_id);
```

5. Click **"Run"** ✅

---

## ✅ Step 2: Verify Railway Variables

1. Go to **Railway Dashboard** → Your Service → **"Variables"** tab
2. **Verify these are set:**

   | Variable | Your Value |
   |----------|------------|
   | `SUPABASE_URL` | `https://utdwvqfnzkcysdsbsvwv.supabase.co` |
   | `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (your full key) |

3. **If missing**, add them:
   - Click **"New Variable"**
   - Add each one
   - Railway will redeploy automatically

---

## ✅ Step 3: Test It

1. In Slack, type:
   ```
   /lead-magnet Target: Software companies | Criteria: Size>10
   ```

2. Check Railway logs for: `Successfully inserted X leads into Supabase`

3. Check Supabase:
   - **Table Editor** → `lead_magnet_candidates`
   - You should see new rows! 🎉

---

## ⚠️ Common Issues

**"Table doesn't exist"** → Run the SQL in Step 1  
**"Auth error"** → Check SUPABASE_KEY is correct (should be Service Role Key)  
**"Connection error"** → Check SUPABASE_URL is correct (no trailing slash)

---

**That's it!** Once the table is created and variables are set, you're good to go! 🚀
