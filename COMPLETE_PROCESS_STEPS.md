# Complete Process Steps - Detailed Breakdown

## Current Implementation Status

### Step-by-Step Process:

#### **Step 1: User Provides Slack Command** ✅ IMPLEMENTED
- **Location:** `layer1_slack_listener.py`
- **What happens:**
  - User types `/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder/Owner,C-Suite`
  - Slack listener receives command
  - Validates command (seniority values)
  - Parses input to extract filters
- **Status:** ✅ Working

---

#### **Step 2: Prospeo Company Search** ✅ IMPLEMENTED
- **Location:** `layer2_prospeo_client.py` → `fetch_companies_page()`
- **What happens:**
  - Calls Prospeo `/search-company` endpoint
  - Filters: `company_keywords` (from `keywords=`), `company_industry`, `company_location`
  - Returns list of companies matching criteria
  - No seniority filter at this stage
- **Status:** ✅ Working

---

#### **Step 3: Save Companies to Supabase** ❌ **NOT IMPLEMENTED**
- **What should happen:**
  - Save ALL companies from Prospeo search to Supabase
  - Mark as `is_qualified=False` initially
  - Store company data for tracking
- **Current behavior:**
  - Companies are NOT saved to Supabase
  - Only persons (from Step 7) are saved
- **Status:** ❌ **MISSING - NEEDS TO BE ADDED**
- **TODO:** Add company saving step before AI qualification

---

#### **Step 4: OpenRouter Verifies Company Fit** ✅ IMPLEMENTED
- **Location:** `layer3_ai_judge.py` → `qualify_person()` / `check_wholesale_partner_type()` / `check_keyword_match()`
- **What happens:**
  - Check #1: Is it a wholesale partner (multi-brand retailer)?
  - Check #2: Does it match keywords/product fit?
  - Only qualifies if BOTH checks pass
  - Returns `is_qualified` boolean + reasoning
- **Status:** ✅ Working

---

#### **Step 5: Add Fit Info to Supabase** ⚠️ **PARTIALLY IMPLEMENTED**
- **What should happen:**
  - Update company record in Supabase with `is_qualified=True`
  - Add qualification reasoning/response
  - Mark `qualified_at` timestamp
- **Current behavior:**
  - Companies are not saved in Step 3, so there's nothing to update
  - Fit info is stored when persons are saved (Step 7)
- **Status:** ⚠️ **DEPENDS ON STEP 3 - Can't update what doesn't exist**
- **TODO:** Implement after Step 3 is added

---

#### **Step 6: If Fit, Find People with Seniority Level in Prospeo** ✅ IMPLEMENTED
- **Location:** `layer2_prospeo_client.py` → `fetch_persons_at_company()`
- **What happens:**
  - For each qualified company
  - Calls Prospeo `/search-person` endpoint
  - Filters: `company_id` (or `company_name`) + `person_seniority` filter
  - Returns ALL persons at that company matching seniority criteria
- **Status:** ✅ Working

---

#### **Step 7: Save Persons to Supabase** ✅ IMPLEMENTED
- **Location:** `layer5_output.py` → `save_lead_to_supabase()`
- **What happens:**
  - For each person found at qualified companies
  - Saves person + company data to Supabase
  - Marks as `is_qualified=True` (company is qualified)
  - Person email may not be available yet
- **Status:** ✅ Working
- **Note:** This happens in `layer4_lead_processor.py` line 178

---

#### **Step 8: Enrich Email for Persons** ✅ IMPLEMENTED
- **Location:** `layer2_prospeo_client.py` → `enrich_person()`
- **What happens:**
  - For each person saved in Step 7
  - Calls Prospeo `/enrich-person` endpoint
  - Gets verified email
  - Updates Supabase record with email
  - Marks as `_email_enriched=True`
- **Status:** ✅ Working

---

#### **Step 9: Update Person Record with Email in Supabase** ✅ IMPLEMENTED
- **Location:** `layer5_output.py` → `update_lead_qualification_status()`
- **What happens:**
  - After email enrichment (Step 8)
  - Updates person record in Supabase with enriched email
  - Email added to `person_email` field
- **Status:** ✅ Working

---

#### **Step 10: Continue Running Until 50 Contacts** ✅ IMPLEMENTED
- **Location:** `layer4_lead_processor.py` → main loop
- **What happens:**
  - Checks if `len(qualified_leads) >= target_count` (default: 50)
  - Continues processing companies until target reached
  - Kill switch: Stops if `max_processed` companies reached (default: 500)
- **Status:** ✅ Working

---

#### **Step 11: Generate CSV File** ✅ IMPLEMENTED
- **Location:** `layer5_output.py` → `generate_csv()`
- **What happens:**
  - After reaching target or hitting kill switch
  - Generates CSV file with all qualified leads
  - Includes person + company data + email
  - Saved locally (or accessible via Railway)
- **Status:** ✅ Working

---

## Complete Flow Diagram

```
1. User sends Slack command
   ↓
2. Prospeo company search (/search-company)
   ↓
3. ❌ MISSING: Save ALL companies to Supabase (is_qualified=False)
   ↓
4. AI qualifies each company (OpenRouter)
   ↓
5. ⚠️ MISSING: Update company record in Supabase (is_qualified=True)
   ↓
6. For qualified companies: Search persons with seniority (Prospeo)
   ↓
7. Save persons to Supabase (is_qualified=True, no email yet)
   ↓
8. Enrich email for each person (Prospeo /enrich-person)
   ↓
9. Update person record with email in Supabase
   ↓
10. Check: Have 50 contacts? If no, continue from Step 2
   ↓
11. Generate CSV file with all qualified leads
```

---

## Missing Steps (TODO)

### **TODO 1: Save Companies to Supabase Before Qualification** ❌
**Location:** `layer4_lead_processor.py` after Step 2 (company search)

**What needs to be added:**
- After fetching companies from Prospeo (Step 2)
- Before AI qualification (Step 4)
- Save each company to Supabase with:
  - All company data
  - `is_qualified=False` (will be updated later)
  - Metadata (slack_trigger_id, search_criteria, etc.)

**Implementation:**
- Add `save_company_to_supabase()` method in `layer5_output.py`
- Or modify `save_lead_to_supabase()` to handle company-only records
- Call in `layer4_lead_processor.py` after fetching companies

---

### **TODO 2: Update Company Qualification Status in Supabase** ❌
**Location:** `layer4_lead_processor.py` after Step 4 (AI qualification)

**What needs to be added:**
- After AI qualification determines if company is qualified
- Update company record in Supabase:
  - `is_qualified=True/False`
  - `qualified_at` timestamp (if qualified)
  - `openrouter_response` with reasoning

**Implementation:**
- Add `update_company_qualification_status()` method in `layer5_output.py`
- Or modify existing update method to work with companies
- Call in `layer4_lead_processor.py` after AI qualification

---

## Current vs. Ideal Flow

### **Current Flow:**
```
Company Search → AI Qualification → Person Search → Save Persons → Enrich Emails
(No company saving)
```

### **Ideal Flow:**
```
Company Search → Save Companies → AI Qualification → Update Companies → 
Person Search → Save Persons → Enrich Emails
```

---

## Summary

### ✅ Implemented (9 steps):
1. Slack command handling
2. Prospeo company search
3. AI company qualification
4. Prospeo person search (with seniority)
5. Save persons to Supabase
6. Enrich emails
7. Update persons with emails
8. Loop until 50 contacts
9. Generate CSV

### ❌ Missing (2 steps):
1. **Save companies to Supabase** (before qualification)
2. **Update company qualification status** (after AI qualification)

### Impact:
- Companies are not persisted in database
- Cannot track which companies were processed
- Cannot see companies that failed qualification
- Only qualified persons are saved

---

## Next Steps

1. **Add company saving step** (Step 3)
2. **Add company qualification update step** (Step 5)
3. **Update Supabase schema** (if needed) to ensure company records can be saved properly
4. **Test the complete flow** with company persistence
