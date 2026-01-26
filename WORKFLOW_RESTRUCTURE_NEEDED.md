# Workflow Restructure Needed

## Current Problem ❌

We're using `person_seniority` filter in the INITIAL search, but we should be:

1. **Searching COMPANIES first** (without seniority)
2. **Qualifying companies**
3. **THEN searching PERSONS at qualified companies** (with seniority)
4. **THEN enriching emails**

---

## Current Code Issue

**In `layer4_lead_processor.py`:**
```python
# Currently searches PERSONS with seniority filter upfront
result = self.prospeo_client.fetch_persons_page(
    page=current_page,
    filters=filters  # <-- includes person_seniority!
)
```

**Problem:** This returns persons, not companies-first approach!

---

## What We Need to Change

### Option 1: Use Prospeo Search-Company Endpoint

1. Add `fetch_companies_page()` method to ProspeoClient
2. Search companies (industry, location only - NO seniority)
3. Qualify companies
4. For qualified companies, search persons with seniority filter
5. Enrich emails for persons

### Option 2: Extract Unique Companies from Person Search

1. Search persons WITHOUT seniority filter (industry, location only)
2. Extract unique companies
3. Deduplicate companies
4. Qualify companies
5. For qualified companies, search persons WITH seniority filter
6. Enrich emails

---

## Recommendation

**Option 2 is probably easier** since we're already using `search-person` endpoint:
- Just remove `person_seniority` from initial search
- Extract unique companies
- Qualify companies
- Then search persons at qualified companies with seniority filter

---

## New Workflow Structure Needed

```
1. Search PERSONS (industry, location only - NO seniority)
   ↓
2. Extract unique COMPANIES from person results
   ↓
3. AI Qualify Companies (Check #1 + Check #2)
   ↓
4. For each qualified company:
   a. Search PERSONS at that company
   b. WITH seniority filter
   ↓
5. Enrich emails for persons found
```

---

## What Needs to Change

### In ProspeoClient:
- Keep `fetch_persons_page()` for initial company discovery
- Add method to search persons at specific company with seniority

### In LeadProcessor:
- Remove `person_seniority` from initial filters
- Extract unique companies
- Qualify companies
- Then search persons at qualified companies with seniority
- Then enrich emails

---

## Questions to Answer

1. Does Prospeo have `search-company` endpoint, or should we use `search-person` and extract companies?
2. Should we deduplicate companies before qualifying?
3. How to handle multiple persons at same qualified company?
