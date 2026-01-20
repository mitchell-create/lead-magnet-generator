# New Workflow: Save All Leads First ✅

## Updated Process Flow

### Step 1: Slack Trigger ✅
- User sends command: `/lead-magnet industry=SaaS | size>50`
- Slack sends to Railway endpoint
- Parser extracts filters and criteria

---

### Step 2: Prospeo Search ✅
- Fetch leads from Prospeo API (in batches of 25)
- Get raw leads based on filters

---

### Step 3: Save ALL Leads to Supabase ✅ **NEW**
**Immediately after fetching each lead:**
- Save lead to Supabase with `is_qualified = FALSE`
- Preserve all data we paid for
- Store with metadata (Slack info, search criteria, etc.)

---

### Step 4: AI Qualification (OpenRouter) ✅
**After saving, qualify each lead:**
- Send lead to OpenRouter/AI for qualification
- AI checks against qualification criteria
- AI returns YES or NO

---

### Step 5: Update Qualification Status ✅ **NEW**
**Update the Supabase record:**
- If qualified: Set `is_qualified = TRUE`, add `qualified_at` timestamp
- If not qualified: Keep `is_qualified = FALSE` (already set)
- Store AI response (`openrouter_response`)

---

### Step 6: Loop Back
- If we have < 50 qualified leads:
  - Fetch next page from Prospeo
  - Repeat Steps 2-5
- Continue until:
  - ✅ 50 qualified leads found, OR
  - ⚠️ 500 leads processed (kill switch)

---

### Step 7: Generate CSV ✅
- Create CSV file with **qualified leads only** (for easy use)
- All leads still in Supabase with qualification status

---

## ✅ What Changed

**Before:**
1. Fetch from Prospeo
2. Qualify with AI
3. Only save qualified leads to Supabase

**After:**
1. Fetch from Prospeo
2. **Save ALL leads to Supabase immediately**
3. Qualify with AI
4. **Update qualification status in Supabase**

---

## 📊 Database Schema Updates

**New Column:**
- `is_qualified` (BOOLEAN) - Marks if lead passed AI qualification
- `qualified_at` (TIMESTAMP, nullable) - When qualification happened

**Updated Indexes:**
- Added index on `is_qualified` for fast filtering
- Added index on `slack_trigger_id` for updates

---

## 💡 Benefits

✅ **No data loss** - All Prospeo leads saved  
✅ **Can re-qualify** - Change criteria later and re-run qualification  
✅ **Full audit trail** - See which leads were rejected and why  
✅ **Cost effective** - Don't waste money on leads we discard  
✅ **CSV still clean** - Only qualified leads exported  

---

## 🔍 Querying Supabase

**Get all qualified leads:**
```sql
SELECT * FROM lead_magnet_candidates 
WHERE is_qualified = TRUE 
ORDER BY qualified_at DESC;
```

**Get all leads from a search:**
```sql
SELECT * FROM lead_magnet_candidates 
WHERE slack_trigger_id = 'your-trigger-id'
ORDER BY processing_order;
```

**Get qualification rate:**
```sql
SELECT 
  COUNT(*) as total_leads,
  SUM(CASE WHEN is_qualified THEN 1 ELSE 0 END) as qualified_leads,
  ROUND(100.0 * SUM(CASE WHEN is_qualified THEN 1 ELSE 0 END) / COUNT(*), 2) as qualification_rate
FROM lead_magnet_candidates
WHERE slack_trigger_id = 'your-trigger-id';
```

---

## 📝 Next Steps

1. **Run the updated Supabase schema** (adds `is_qualified` column)
2. **Deploy updated code**
3. **Test the new workflow**

All leads will be preserved! 🎉
