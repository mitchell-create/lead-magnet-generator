# ✅ Workflow Restructure Complete

## Summary

The code has been restructured to implement the **Company-First Workflow** as you requested.

---

## ✅ New Workflow (Company-First Approach)

### Phase 1: Discover Companies
- Search persons WITHOUT seniority filter
- Use filters: `company_industry`, `company_location` (company-level only)
- Extract unique companies from person results

### Phase 2: Qualify Companies
- Run AI qualification checks on each unique company
- Check #1: Wholesale partner type (multi-brand retailer?)
- Check #2: Keyword match (product/industry fit?)
- Save qualified companies

### Phase 3: Find Persons at Qualified Companies
- For each qualified company, search persons AT that company
- **NOW use seniority filter**: `person_seniority=Founder/Owner,C-Suite`, etc.
- Get ALL persons matching the seniority criteria

### Phase 4: Enrich Emails
- For each person found at qualified companies
- Enrich to get verified email
- Save to Supabase

---

## 🎯 Key Changes

### 1. Seniority Filter Separation
- **Before**: Used in initial search (wrong)
- **After**: Only used when searching persons at qualified companies (correct)

### 2. New Workflow Structure
```
Initial Search → Persons (no seniority)
    ↓
Extract Unique Companies
    ↓
Qualify Companies (AI)
    ↓
Search Persons at Qualified Companies (WITH seniority)
    ↓
Enrich Emails
```

### 3. Code Changes

#### `utils.py`
- Added `include_seniority` parameter to `build_prospeo_filters()`
- Added `extract_person_seniority_filter()` to extract seniority separately
- Added `extract_unique_companies_from_persons()` to deduplicate companies

#### `layer2_prospeo_client.py`
- Added `fetch_persons_at_company()` method
- Searches persons at specific company with seniority filter

#### `layer4_lead_processor.py`
- Completely restructured `process_until_qualified()`
- Now follows company-first workflow:
  1. Phase 1: Discover companies
  2. Phase 2: Qualify companies
  3. Phase 3: Find persons at qualified companies (with seniority)
  4. Phase 4: Enrich emails

#### `main.py`
- Updated to pass `parsed_input` to processor
- Updated stats logging for new workflow
- Uses `build_prospeo_filters(parsed_input, include_seniority=False)`

---

## ✅ How Seniority Now Works

1. **Initial Search**: NO seniority filter
   - Searches for companies using industry/location filters
   - Returns persons (but we extract companies from them)

2. **After Company Qualification**: YES seniority filter
   - For each qualified company, search persons AT that company
   - Filter by seniority: `Founder/Owner`, `C-Suite`, `Director`, etc.
   - Get ALL matching persons

3. **Email Enrichment**: For all persons found
   - Enrich to get verified emails
   - Save to Supabase

---

## 📋 Example Flow

**Input:**
```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder/Owner,C-Suite
```

**Process:**
1. **Phase 1**: Search persons at retail companies (no seniority)
   - Returns: 100 persons from 50 unique companies
   
2. **Phase 2**: Qualify companies
   - AI checks each of the 50 companies
   - 10 companies qualify (golf retailers)
   
3. **Phase 3**: Find persons at qualified companies
   - For each of 10 qualified companies
   - Search persons with `seniority=Founder/Owner,C-Suite`
   - Finds 25 persons total (2-3 per company)
   
4. **Phase 4**: Enrich emails
   - Enrich all 25 persons
   - Get verified emails for 20 persons
   - These are the final qualified leads

---

## ✅ Testing Recommendations

1. Test with a small target (e.g., 5 qualified persons)
2. Verify seniority filter is NOT used in initial search
3. Verify seniority filter IS used when searching persons at qualified companies
4. Verify all persons matching seniority are returned (not just one)
5. Verify emails are enriched for all persons

---

## 🐛 Potential Issues to Watch For

1. **Company Filter Format**: The `fetch_persons_at_company()` method uses `company_id`, `company_name`, or `company_domain`. If Prospeo API uses different filter names, we may need to adjust.

2. **Multiple Persons per Company**: The code now finds ALL persons matching seniority at each qualified company. Make sure this matches your expectations.

3. **Email Enrichment Rate Limits**: If there are many persons per company, email enrichment might hit rate limits. The code includes retry logic.

---

## 📝 Next Steps

1. Test the new workflow with a small query
2. Monitor logs to ensure:
   - Companies are discovered without seniority filter
   - Seniority filter is applied in Phase 3
   - All matching persons are found and enriched
3. Adjust filters/limits if needed based on results
