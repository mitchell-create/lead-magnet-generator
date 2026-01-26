# Workflow Clarification - Company-First Approach

## The Issue You Identified ✅

You're absolutely right! The current workflow has a problem:

**Current Flow (WRONG):**
1. Search for PERSONS with seniority filter
2. Extract companies from person results
3. Qualify companies
4. Enrich emails

**Problem:** We're using seniority in the initial search, but we should be searching for COMPANIES first!

---

## Correct Workflow (What We Should Do)

**Step 1: Search for COMPANIES** (not persons)
- Use Prospeo search to find companies matching:
  - `industry`
  - `location`
  - **NO seniority filter here** (we don't know persons yet!)

**Step 2: AI Qualify Companies**
- Run AI checks on companies
- Save qualified companies to Supabase

**Step 3: Search for PERSONS at Qualified Companies**
- For each qualified company, search for persons at that company
- **NOW use seniority filter:** `person_seniority=Founder/Owner,C-Suite`
- This is when seniority matters!

**Step 4: Enrich Emails for Persons**
- Enrich persons found in Step 3 to get verified emails

---

## How This Should Work

### Current Problem:
```
Initial Search: search-person with person_seniority filter
↓
Returns: Persons (already filtered by seniority)
↓
Extract companies
↓
Qualify companies
↓
Enrich email for the person we already have
```

### What We Should Do:
```
Step 1: Search Companies
  - industry, location filters
  - NO seniority filter
↓
Step 2: Qualify Companies (AI)
  - Save qualified companies
↓
Step 3: For each qualified company:
  - Search persons at that company
  - WITH seniority filter
↓
Step 4: Enrich emails for persons found
```

---

## Options to Fix This

### Option A: Use Prospeo's Search-Company Endpoint (If Available)
- Search for companies directly
- No person data in initial search
- Then search persons at qualified companies

### Option B: Extract Unique Companies from Person Search
- Search persons without seniority filter
- Extract unique companies
- Deduplicate
- Qualify companies
- Then search persons at qualified companies WITH seniority filter

---

## The Seniority Filter Should Be Used When:

✅ **Searching for persons at qualified companies** (Step 3)
❌ **NOT in the initial company search** (Step 1)

---

## Next Steps Needed

We need to restructure the workflow to:

1. **Separate company search from person search**
2. **Store qualified companies first**
3. **Then search for persons at qualified companies with seniority filter**
4. **Then enrich emails for those persons**

---

## Question

Does Prospeo have a `search-company` endpoint, or should we:
- Extract unique companies from `search-person` results (without seniority filter)?
- Then search persons at those companies (with seniority filter)?

What's your preference?
