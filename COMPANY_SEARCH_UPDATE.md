# Company Search Update - Using /search-company Endpoint

## ✅ Updated to Use Prospeo's /search-company Endpoint

Based on Prospeo support's confirmation, we now use the `/search-company` endpoint for company discovery, which supports `company_keywords` filter!

---

## 🎯 What Changed

### Before:
- Used `/search-person` to find companies
- Extracted unique companies from person results
- Keywords were NOT used in Prospeo search (only for AI qualification)

### After:
- **Uses `/search-company` endpoint directly** ✅
- **Keywords are converted to `company_keywords` filter** ✅
- Prospeo pre-filters companies by keywords before AI qualification
- More efficient: Less companies to process through AI

---

## 🔄 New Workflow

### Phase 1: Discover Companies (IMPROVED)
- **Uses:** `/search-company` endpoint
- **Filters:** 
  - `company_industry`
  - `company_location`
  - `company_keywords` (converted from `keywords` in Slack command)
- **Result:** Companies directly (not extracted from persons)

### Phase 2: Qualify Companies
- AI qualification (wholesale check + keyword refinement)
- Same as before

### Phase 3: Find Persons at Qualified Companies
- Search persons at qualified companies
- WITH seniority filter
- Same as before

### Phase 4: Enrich Emails
- Enrich emails for all persons
- Same as before

---

## 📝 How Keywords Work Now

### Slack Command:
```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder/Owner
```

### What Happens:

1. **Parsing:**
   - `keywords=golf retailers` extracted
   - Stored in `parsed_input['prospeo_filters']['keywords']`

2. **Company Search (Phase 1):**
   - Converted to `company_keywords: "golf retailers"`
   - Sent to Prospeo `/search-company` endpoint
   - Prospeo pre-filters companies by keywords
   - Returns: Companies matching "golf retailers"

3. **AI Qualification (Phase 2):**
   - Still uses keywords for more nuanced matching
   - Checks wholesale partner type + keyword/product fit

---

## ✅ Benefits

1. **More Efficient:**
   - Prospeo filters by keywords first (reduces AI processing)
   - Less companies to run through AI qualification

2. **Better Results:**
   - Companies are pre-filtered by keywords at database level
   - AI does nuanced matching on already-relevant companies

3. **Cost Effective:**
   - Less AI calls needed (fewer companies to qualify)
   - Prospeo does initial keyword filtering (free)

---

## 🔧 Code Changes

### `config.py`
- Added `PROSPEO_SEARCH_COMPANY_ENDPOINT`

### `layer2_prospeo_client.py`
- Added `fetch_companies_page()` method
- Uses `/search-company` endpoint

### `utils.py`
- Updated `build_prospeo_filters()` with `for_company_search` parameter
- Converts `keywords` → `company_keywords` when `for_company_search=True`

### `layer4_lead_processor.py`
- Updated Phase 1 to use `fetch_companies_page()` instead of `fetch_persons_page()`
- Works with companies directly (no extraction needed)

### `main.py`
- Updated to use `for_company_search=True` when building filters

---

## 📋 Testing

When testing, verify:
1. ✅ Companies are fetched using `/search-company` endpoint
2. ✅ `company_keywords` filter is sent to Prospeo
3. ✅ Companies are pre-filtered by keywords
4. ✅ AI qualification still works with keywords for nuanced matching

---

## 💡 Note

Keywords are now used in **two places**:
1. **Prospeo search** (`company_keywords`) - Initial filtering
2. **AI qualification** (still in prompts) - Nuanced matching

This provides the best of both worlds: database-level filtering + AI-level intelligence!
