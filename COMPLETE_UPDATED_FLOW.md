# Complete Updated Flow - Final Version

## Complete Step-by-Step Process

### Step 0: Pre-Check Supabase (BEFORE Prospeo Search)

**What happens:**
1. Query Supabase for companies where `wholesale_partner_check = TRUE`
2. For each company:
   - If `wholesale_partner_check = FALSE` → Skip (not a fit)
   - If `wholesale_partner_check = TRUE`:
     - Quick match: new keywords vs. stored `product_categories`
     - **Strong match** → Add to `qualified_companies` list (no AI needed)
     - **No match** → Mark as not qualified, add to `no_match_but_wholesale` list
     - **Uncertain** → Re-run AI Check #2, add to qualified if passes

**Returns:**
- `qualified_companies`: Companies already qualified for this search
- `no_match_but_wholesale`: Companies to re-check if they appear in Prospeo

---

### Step 1: User Sends Slack Command
- Parse command
- Extract keywords, industry, location, seniority, etc.
- Validate seniority values

---

### Step 2: Prospeo Company Search
- Search Prospeo for companies matching filters
- **Skip companies** already in `qualified_companies` from Step 0
- Get list of NEW companies from Prospeo

---

### Step 3: Check Each Prospeo Company Against Supabase

**For each company from Prospeo:**

**Case A: Company in `no_match_but_wholesale` list**
```
⚠️ Was marked no_match in pre-check, but Prospeo returned it
   → Prospeo returned it (matches industry/location filters)
   → Quick match might have been too strict
   → Re-run AI Check #2 with new keywords
   
Result:
- If AI Check #2 passes → Qualified for THIS search
- If AI Check #2 fails → Not qualified (confirm quick match was correct)
- Update product_categories with new AI results
```

**Case B: Company in `qualified_companies` from pre-check**
```
✅ Already qualified in Step 0
   → Skip verification
   → Add to final qualified list
```

**Case C: Company exists in Supabase but `wholesale_partner_check = FALSE`**
```
❌ Skip entirely
   → Not a wholesale partner, won't become one
   → Move to next company
```

**Case D: Company exists in Supabase, `wholesale_partner_check = TRUE`, but wasn't in pre-check**
```
⚠️ Might have been added after pre-check or edge case
   → Run quick match
   → If uncertain → Re-run AI Check #2
```

**Case E: Company is NEW (not in Supabase)**
```
✅ Save company to Supabase (person_id = NULL)
✅ Run Check #1 (wholesale partner)
✅ Run Check #2 (keyword match)
✅ Store both results + product_categories
```

---

### Step 4: Save Companies to Supabase
- For NEW companies from Prospeo
- Save as company-only records (`person_id = NULL`)
- Mark `is_qualified = FALSE` initially

---

### Step 5: AI Qualification

**For each company (new or existing that needs verification):**

**Check #1: Wholesale Partner Type**
- Skip if `wholesale_partner_check = TRUE` (already verified)
- Run if new or `wholesale_partner_check = FALSE`
- Save: `wholesale_partner_check`, `wholesale_partner_response`

**Check #2: Keyword/Product Fit**
- Always run for new companies
- Run for existing companies if:
  - Quick match was uncertain
  - Company was in `no_match_but_wholesale` list
- Output: VERDICT, PRODUCT_CATEGORIES, MARKET_SEGMENTS, REASONING, EVIDENCE
- Save: `keyword_match_check`, `keyword_match_response`, `product_categories[]`, `market_segments[]`

---

### Step 6: Update Company Qualification Status
- Update company record in Supabase:
  - Both check results
  - Product categories array
  - Market segments array
  - `is_qualified = (wholesale_partner_check AND keyword_match_check)`
  - `qualified_at` timestamp if qualified

---

### Step 7: Scraped Content Management
- Before AI qualification, check if `company_scraped_content` exists and is < 180 days old
- If yes: Use stored content
- If no: Scrape website, save to Supabase with `scraped_content_date`

---

### Step 8: Find Persons at Qualified Companies
- For each qualified company
- Search Prospeo for persons at that company
- WITH seniority filter
- Get ALL persons matching seniority

---

### Step 9: Save Persons to Supabase
- For each person found at qualified companies
- Save as person records (`person_id IS NOT NULL`)
- Include company data (duplicated)
- Mark `is_qualified = TRUE` (company is qualified)

---

### Step 10: Enrich Emails for Persons
- For each person saved in Step 9
- Call Prospeo `/enrich-person` endpoint
- Get verified email

---

### Step 11: Update Person Records with Emails
- Update Supabase record with enriched email
- Mark `_email_enriched = True`

---

### Step 12: Continue Until 50 Contacts
- Check if `len(qualified_leads) >= 50`
- If not, continue from Step 2 (next page of Prospeo results)
- Kill switch: Stop if processed 500 companies

---

### Step 13: Generate CSV
- After reaching 50 contacts or hitting kill switch
- Generate CSV file with all qualified leads
- Include person + company data + emails

---

## Key Logic Points

### Pre-Check (Step 0):
- Quick match for efficiency
- Track `no_match_but_wholesale` for re-check

### Prospeo Search (Step 2):
- Skip companies already qualified in pre-check
- Get new companies

### Company Verification (Step 3):
- Re-check `no_match_but_wholesale` companies with AI
- Skip `wholesale_partner_check = FALSE` companies
- Verify new companies

### AI Qualification (Step 5):
- Skip Check #1 if already TRUE
- Always run Check #2 for new companies
- Re-run Check #2 for `no_match_but_wholesale` companies

---

## Benefits

1. ✅ **Efficiency**: Quick match saves AI credits for most cases
2. ✅ **Accuracy**: Re-check `no_match` companies if Prospeo returns them
3. ✅ **Smart**: Leverages stored data while staying current
4. ✅ **Cost-Effective**: Minimal AI calls, maximum reuse
