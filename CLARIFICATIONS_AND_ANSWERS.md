# Clarifications: Company Matching & Person Storage

## Question 1: How Does It Know If a Company Is New?

### Current Implementation Issue
The system currently doesn't check if companies already exist in Supabase. Here's what needs to happen:

### Proposed Flow:

**Step 0: Pre-Check Supabase (BEFORE Prospeo Search)**
1. Query Supabase for companies where:
   - `wholesale_partner_check = TRUE` (passed Check #1 previously)
   - `product_categories` match new keywords from Slack command
   
2. For matching companies:
   - Add to "already qualified" list
   - Skip Prospeo search for these companies
   - Go directly to Step 7 (find persons at these companies)
   - These count toward the 50 contacts goal

**Step 2: Prospeo Company Search**
- Search Prospeo ONLY for companies NOT found in Supabase pre-check
- Get list of NEW companies from Prospeo

**Step 3: Check Each Prospeo Company Against Supabase**
- For each company from Prospeo search:
  - Check if `company_id`/`company_name`/`company_domain` already exists in Supabase
  - **If EXISTS:**
    - Check if `wholesale_partner_check = TRUE` (passed Check #1 before)
    - **If wholesale_partner_check = TRUE:**
      - ✅ Skip Check #1 (wholesale verification) - company type doesn't change
      - ⚠️ **ALWAYS re-run Check #2** (keyword match) with NEW keywords from current search
      - If Check #2 passes with new keywords → Qualified for THIS search
      - If Check #2 fails with new keywords → NOT qualified for THIS search (even though it was qualified before)
    - **If wholesale_partner_check = FALSE:**
      - Re-run BOTH checks (might now qualify)
  - **If NEW:**
    - Save company to Supabase (Step 3)
    - Run BOTH checks (Step 4)

### Implementation Logic:

```python
# Step 0: Pre-check Supabase
existing_qualified = check_existing_companies_in_supabase(
    keywords=target_companies,
    qualification_criteria=qualification_criteria
)
# Returns: List of companies that are wholesale-fit AND match keywords

# Step 2: Prospeo search (only for new companies)
# Skip companies already found in pre-check

# Step 3: For each Prospeo company
for company in prospeo_companies:
    existing_company = check_company_exists_in_supabase(
        company_id=company['id'],
        company_name=company['name'],
        company_domain=company['domain']
    )
    
    if existing_company:
        if existing_company['is_qualified']:
            # Already qualified - skip verification
            qualified_companies.append(company)
        else:
            # Exists but not qualified - might re-qualify with new criteria
            # Save company again (or update) and run verification
            save_company_to_supabase(company)
            # Run verification...
    else:
        # New company - save and verify
        save_company_to_supabase(company)
        # Run verification...
```

---

## Question 2: How Are Persons Stored in Supabase?

### Current Schema Structure

**Answer: Same table, separate rows for each person**

The `lead_magnet_candidates` table stores **one row per person**, where each row contains:
- **Person data** (person_id, person_name, person_email, person_title, person_linkedin_url)
- **Company data** (company_id, company_name, company_description, company_domain, etc.) - **duplicated** for each person

### Example:

If Company XYZ has 3 persons:
- **Row 1:** Person A (VP) + Company XYZ data
- **Row 2:** Person B (Director) + Company XYZ data  
- **Row 3:** Person C (Manager) + Company XYZ data

### Implications:

1. **Company data is duplicated** across multiple person rows
2. **No separate company table** - company info is in every person record
3. **To find a company**, we search by `company_id`/`company_name`/`company_domain`
4. **Multiple rows** will have the same `company_id` but different `person_id`

### Problem This Creates:

When we want to save companies separately (before persons are found), we need to decide:
- **Option A:** Save company-only records in the same table (with `person_id = NULL`)
- **Option B:** Create a separate `companies` table
- **Option C:** Use a flag/field to distinguish company records from person records

### Recommended Approach: Option A (Company-only records)

**Modify schema to allow:**
- Company records: `person_id = NULL`, `person_name = NULL`, etc.
- Person records: All fields populated

**Benefits:**
- Same table structure
- Easy to query: `WHERE person_id IS NULL` for companies, `WHERE person_id IS NOT NULL` for persons
- Company data stored once when saved, then referenced when persons are added

**Example Row Structure:**

| person_id | person_name | company_id | company_name | is_company_record |
|-----------|-------------|------------|--------------|-------------------|
| NULL      | NULL        | comp123    | Acme Corp    | TRUE              |
| pers456   | John Doe    | comp123    | Acme Corp    | FALSE             |
| pers789   | Jane Smith  | comp123    | Acme Corp    | FALSE             |

---

## Updated Flow with Clarifications

### Step 0: Pre-Check Supabase for Existing Qualified Companies
```
Query: WHERE wholesale_partner_check = TRUE 
  AND product_categories matches new keywords
Result: List of companies already qualified for this search
Action: Add to qualified list, skip Prospeo search
```

### Step 1: User sends Slack command

### Step 2: Prospeo Company Search (only NEW companies)
```
Search Prospeo for companies matching filters
BUT: Skip companies already found in Step 0
```

### Step 3: Check Each Prospeo Company
```
For each company from Prospeo:
  - Check if company_id/name/domain exists in Supabase
  
  If EXISTS:
    - If wholesale_partner_check = TRUE:
      → Skip Check #1 (already verified as wholesale partner)
      → ALWAYS re-run Check #2 with NEW keywords
      → Update product_categories if needed
      → If Check #2 passes: Qualified for THIS search
      → If Check #2 fails: NOT qualified for THIS search
    
    - If wholesale_partner_check = FALSE:
      → Re-run BOTH checks (might now qualify)
  
  If NEW:
    → Save company record, run BOTH checks
```

### Step 4: Save Company to Supabase
```
Save as company-only record:
- person_id = NULL
- All company fields populated
- is_qualified = FALSE (initially)
```

### Step 5: AI Qualification
```
Run Check #1 and Check #2
Update company record with results
```

### Step 6: Find Persons at Qualified Companies
```
Search Prospeo for persons at company
WITH seniority filter
```

### Step 7: Save Persons to Supabase
```
Save as person records:
- person_id = populated
- Same company data (duplicated)
- is_qualified = TRUE (company qualified)
```

---

## Schema Changes Needed

### Option 1: Add Flag Field
```sql
ALTER TABLE lead_magnet_candidates 
ADD COLUMN is_company_record BOOLEAN DEFAULT FALSE;

-- Company records: is_company_record = TRUE, person_id = NULL
-- Person records: is_company_record = FALSE, person_id IS NOT NULL
```

### Option 2: Use person_id as Distinguisher
- Company records: `person_id IS NULL`
- Person records: `person_id IS NOT NULL`
- No schema change needed, just logic

**Recommendation:** Option 2 (no schema change, just use NULL person_id to identify company records)

---

## Summary

### Q1 Answer:
- **Pre-check** Supabase first for wholesale-fit companies that match keywords
- Add those to qualified list (skip Prospeo)
- When Prospeo returns companies, check if they exist in Supabase
- If exists and qualified → skip verification
- If exists but not qualified → re-verify (criteria might have changed)
- If new → save and verify

### Q2 Answer:
- **Same table** (`lead_magnet_candidates`)
- **Company-only records**: `person_id = NULL` (saved before persons found)
- **Person records**: `person_id IS NOT NULL` (saved after persons found)
- Company data duplicated in each person row
- Query by `company_id` to find all persons at a company
