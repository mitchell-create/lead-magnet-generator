# Updated Implementation Plan - Company Saving & Supabase Pre-Check

## User Requirements Summary

1. ✅ **Two Separate AI Checks Confirmed**: Wholesale fit (Check #1) and Keyword/product fit (Check #2)
2. **Save company information** to Supabase before qualification
3. **Check Supabase BEFORE Prospeo** for existing wholesale-fit companies
4. **Modify Check #2** to output reusable structured data (product categories + reasoning)
5. **Store scraped content** in Supabase, re-scrape every 180 days
6. **Reuse existing companies** if they're a good fit for new keyword searches

---

## Key Design Decision: Enhanced Check #2 Output

### Current Check #2 Output:
- VERDICT: YES/NO
- REASONING: Text explanation
- EVIDENCE: Supporting details

### New Check #2 Output Format:
```
VERDICT: YES/NO
PRODUCT_CATEGORIES: [Golf Equipment, Athletic Apparel, Pro Shop Items, Sporting Goods]
MARKET_SEGMENTS: [Golf courses, Pro shops, Athletic retailers]
REASONING: [Detailed explanation]
EVIDENCE: [Supporting website elements]
```

**Benefits:**
- `PRODUCT_CATEGORIES` can be matched against new keywords quickly
- `REASONING` provides context for nuanced matching
- Enables reusability without re-running AI check
- Can do quick keyword matching against stored categories

---

## Implementation Steps

### Phase 1: Enhance Supabase Schema

**File:** `supabase_schema.sql`

**Add Fields:**
```sql
-- Company qualification results (separate checks)
wholesale_partner_check BOOLEAN,  -- Result of Check #1
wholesale_partner_response TEXT,  -- AI response text from Check #1

keyword_match_check BOOLEAN,  -- Result of Check #2
keyword_match_response TEXT,  -- Full AI response from Check #2
product_categories TEXT[],  -- Array of product categories extracted from Check #2
market_segments TEXT[],  -- Array of market segments extracted from Check #2

-- Scraped content
company_scraped_content TEXT,  -- Scraped website HTML/text
scraped_content_date TIMESTAMP WITH TIME ZONE,  -- When content was scraped

-- Re-scraping logic
last_scraped_at TIMESTAMP WITH TIME ZONE,  -- Track last scrape date
```

**Add Indexes:**
```sql
CREATE INDEX idx_company_id ON lead_magnet_candidates(company_id);
CREATE INDEX idx_company_name ON lead_magnet_candidates(company_name);
CREATE INDEX idx_wholesale_partner_check ON lead_magnet_candidates(wholesale_partner_check);
CREATE INDEX idx_keyword_match_check ON lead_magnet_candidates(keyword_match_check);
CREATE INDEX idx_product_categories ON lead_magnet_candidates USING GIN(product_categories);  -- For array searches
```

---

### Phase 2: Modify Check #2 Prompt

**File:** `utils.py` → `format_keyword_match_prompt()`

**New Prompt Format:**
- Request structured output: PRODUCT_CATEGORIES and MARKET_SEGMENTS
- Keep VERDICT, REASONING, EVIDENCE
- Format as structured text that can be parsed

**Example Output:**
```
VERDICT: YES

PRODUCT_CATEGORIES: Golf Equipment, Golf Apparel, Pro Shop Items, Athletic Footwear

MARKET_SEGMENTS: Golf Courses, Pro Shops, Athletic Retailers, Sporting Goods Stores

REASONING: This company operates a pro shop selling golf equipment and apparel. They carry multiple brands including Titleist, Callaway, and Nike. Their product categories align with golf equipment and athletic apparel markets.

EVIDENCE: Website has "Golf Equipment" and "Pro Shop" sections. Product pages show multiple brands. About page mentions serving golf courses and pro shops.
```

---

### Phase 3: Parse Check #2 Response

**File:** `layer3_ai_judge.py` → `check_keyword_match()`

**New Return Format:**
```python
{
    'matches_keywords': bool,
    'response_text': str,  # Full AI response
    'product_categories': List[str],  # Parsed categories
    'market_segments': List[str],  # Parsed segments
    'reasoning': str,  # Parsed reasoning
    'evidence': str  # Parsed evidence
}
```

**Parser Function:**
```python
def parse_keyword_check_response(response_text: str) -> Dict:
    """
    Parse structured AI response to extract:
    - VERDICT (YES/NO)
    - PRODUCT_CATEGORIES (list)
    - MARKET_SEGMENTS (list)
    - REASONING (text)
    - EVIDENCE (text)
    """
```

---

### Phase 4: Save Companies to Supabase (Before Qualification)

**File:** `layer5_output.py` → Add `save_company_to_supabase()`

**What it does:**
- Save ALL companies from Prospeo search
- Store company data fields
- Mark `is_qualified=False`
- Mark `wholesale_partner_check=None`, `keyword_match_check=None`
- Store `slack_trigger_id`, `search_criteria`

**Location:** `layer4_lead_processor.py` - After Step 2 (company search), before Step 4 (AI qualification)

---

### Phase 5: Update Company Qualification Status

**File:** `layer5_output.py` → Add `update_company_qualification_status()`

**What it does:**
- After AI qualification, update company record:
  - `wholesale_partner_check` = result of Check #1
  - `wholesale_partner_response` = AI response text
  - `keyword_match_check` = result of Check #2
  - `keyword_match_response` = full AI response
  - `product_categories` = array of categories
  - `market_segments` = array of segments
  - `is_qualified` = True if both checks passed
  - `qualified_at` = timestamp if qualified
  - `company_scraped_content` = scraped HTML/text
  - `scraped_content_date` = current timestamp

**Location:** `layer4_lead_processor.py` - After Step 4 (AI qualification)

---

### Phase 6: Supabase Pre-Check (BEFORE Prospeo Search)

**File:** `layer5_output.py` → Add `check_existing_companies_in_supabase()`

**Logic:**
1. Query Supabase for companies where:
   - `wholesale_partner_check = TRUE` (passed Check #1)
   - Company data exists

2. For each found company:
   - **ALWAYS re-run Check #2** (keyword match) with NEW keywords
   - This ensures company is a fit for the current search criteria
   - If Check #2 passes → Company is qualified for THIS search
   - If Check #2 fails → Company is NOT qualified for THIS search (even if it was before)
   
3. Return:
   - Companies where Check #2 passes with new keywords (skip Prospeo search)
   - Update product_categories with new Check #2 results

**Matching Logic:**
```python
def check_keyword_match_against_categories(
    stored_categories: List[str],
    new_keywords: List[str]
) -> bool:
    """
    Check if new keywords match stored product categories.
    Returns True if any keyword matches any category.
    """
    # Case-insensitive matching
    # Partial matching (e.g., "golf" matches "Golf Equipment")
```

**Location:** `layer4_lead_processor.py` - BEFORE Step 2 (Prospeo search)

**Integration:**
```python
# Check Supabase first
existing_qualified_companies = output_manager.check_existing_companies_in_supabase(
    filters=filters,
    keywords=target_companies,
    qualification_criteria=qualification_criteria
)

# Skip Prospeo search for companies that are still a good fit
# Only search Prospeo for companies not found in Supabase
```

---

### Phase 7: Scraped Content Management

**File:** `layer4_lead_processor.py` → Enhance scraping logic

**Logic:**
1. Before scraping, check Supabase:
   - If `company_scraped_content` exists AND `scraped_content_date` < 180 days old
   - Use stored content (skip scraping)
   
2. If no stored content OR > 180 days old:
   - Scrape website
   - Save to Supabase: `company_scraped_content` + `scraped_content_date`

3. Always use fresh or stored scraped content for AI qualification

---

## Updated Complete Flow

```
0. NEW: Check Supabase for existing wholesale-fit companies
   ↓
   - Find companies where wholesale_partner_check = TRUE
   - Check if product_categories match new keywords
   - Return companies to skip Prospeo search for
   
1. User sends Slack command
   ↓
2. Prospeo company search (only for companies NOT found in Supabase)
   ↓
3. For each company from Prospeo:
   a. Check if company exists in Supabase
   b. If EXISTS and wholesale_partner_check = TRUE:
      - ✅ Skip Check #1 (already verified as wholesale partner)
      - ⚠️ ALWAYS re-run Check #2 with NEW keywords
      - Update product_categories with new Check #2 results
   c. If EXISTS but wholesale_partner_check = FALSE:
      - Re-run BOTH checks
   d. If NEW:
      - Save company to Supabase
      - Run BOTH checks
   
   For each company (existing or new):
   a. Check if scraped content exists and is < 180 days old
      - If yes: Use stored content
      - If no: Scrape website, save to Supabase
   
   b. AI Check #1: Wholesale partner type (skip if already TRUE)
      - Save: wholesale_partner_check, wholesale_partner_response
   
   c. AI Check #2: Keyword/product fit (ALWAYS run with current search keywords)
      - Output: VERDICT, PRODUCT_CATEGORIES, MARKET_SEGMENTS, REASONING, EVIDENCE
      - Parse and save: keyword_match_check, keyword_match_response, 
                        product_categories[], market_segments[]
   
5. Update company record in Supabase:
   - Both check results
   - Product categories array
   - Market segments array
   - is_qualified = (wholesale_partner_check AND keyword_match_check)
   
6. For qualified companies: Search persons with seniority
   ↓
7. Save persons to Supabase
   ↓
8. Enrich emails for persons
   ↓
9. Update person records with emails
   ↓
10. Continue until 50 contacts
   ↓
11. Generate CSV
```

---

## Files to Modify

1. **`supabase_schema.sql`**
   - Add new fields for qualification tracking
   - Add indexes

2. **`utils.py`**
   - Modify `format_keyword_match_prompt()` to request structured output
   - Add `parse_keyword_check_response()` function

3. **`layer3_ai_judge.py`**
   - Modify `check_keyword_match()` to parse and return structured data
   - Update return format

4. **`layer5_output.py`**
   - Add `save_company_to_supabase()`
   - Add `update_company_qualification_status()`
   - Add `check_existing_companies_in_supabase()`
   - Add `check_keyword_match_against_categories()`

5. **`layer4_lead_processor.py`**
   - Add Supabase pre-check step (BEFORE Prospeo search)
   - Add company saving step (after Prospeo search)
   - Add company qualification update step (after AI qualification)
   - Enhance scraping logic (check stored content, re-scrape if > 180 days)

---

## Decision Points

### 1. Re-qualification Logic
- **If keywords changed significantly:** Re-run Check #2 to update product_categories
- **If keywords match stored categories:** Use existing qualification
- **Always store:** Both the matching result AND the product categories for future use

### 2. Company Matching
- Match by: `company_id` (preferred), `company_name`, or `company_domain`
- If multiple matches: Use most recent record

### 3. Scraped Content Expiry
- Re-scrape if: `scraped_content_date` is NULL OR > 180 days old
- Always save: New scraped content to update `scraped_content_date`

---

## Benefits of This Approach

1. ✅ **Credits Savings**: Reuse existing wholesale-fit companies
2. ✅ **Speed**: Skip Prospeo search for known good companies
3. ✅ **Flexibility**: Product categories enable keyword matching without re-running AI
4. ✅ **Accuracy**: Always use fresh or recent scraped content
5. ✅ **Traceability**: Track both check results separately
6. ✅ **Future-Proof**: Stored categories work for any future keyword search
