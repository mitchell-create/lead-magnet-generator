# Final Keyword Matching Logic - Clarified

## Key Clarifications

### 1. Wholesale Check = FALSE
- **Action:** Skip entirely, move on
- **Reason:** Company type doesn't change - if they're not a wholesale partner, they won't become one
- **No re-check needed**

### 2. Keyword Matching for Existing Companies
- **Approach:** Hybrid (quick match first, then AI if uncertain)
- **Step 1:** Match new keywords against stored `product_categories` using simple matching logic
- **Step 2:** If match is clear → use result (no AI needed)
- **Step 3:** If uncertain/ambiguous → re-run AI Check #2 with new keywords

---

## Updated Logic Flow

### For Existing Companies in Supabase:

**Case 1: `wholesale_partner_check = FALSE`**
```
❌ Skip this company entirely
   → Not a wholesale partner, won't become one
   → Move to next company
```

**Case 2: `wholesale_partner_check = TRUE` AND has stored `product_categories`**
```
✅ Skip Check #1 (already verified)

Step 1: Quick Match (No AI)
   → Match new keywords against stored product_categories
   → Use simple matching logic (case-insensitive, partial match)
   
Step 2: Determine Match Confidence
   - Strong Match (keywords clearly match categories):
     ✅ Use stored qualification (qualified for this search)
     ✅ Update is_qualified for THIS search
     ❌ No AI re-run needed (saves credits)
   
   - No Match (keywords clearly don't match):
     ❌ Mark as not qualified for THIS search (pre-check)
     ⚠️ BUT: Track this company in "no_match_but_wholesale" list
     ⚠️ If this company appears in Prospeo results → Re-run AI Check #2
     → Prospeo returned it, so it matches filters - worth re-checking with AI
   
   - Uncertain/Ambiguous (can't determine):
     ⚠️ Re-run AI Check #2 with new keywords
     ✅ Get fresh product_categories and verdict
     ✅ Update stored categories with new results
```

### Special Case: No-Match Company Appears in Prospeo Results

**If company was marked `no_match` in pre-check BUT appears in Prospeo search:**
```
⚠️ Re-run AI Check #2 with new keywords
   → Prospeo returned it (matches industry/location filters)
   → Quick match might have been too strict
   → AI might find it's actually a match
   
Result:
- If AI Check #2 passes → Qualified for THIS search
- If AI Check #2 fails → Not qualified (confirm quick match was correct)
- Update product_categories with new AI results
```

**Case 3: `wholesale_partner_check = TRUE` but NO stored `product_categories`**
```
⚠️ Re-run AI Check #2 with new keywords
   → First time running keyword check on this company
   → Store product_categories for future use
```

**Case 4: Company is NEW (not in Supabase)**
```
✅ Run Check #1 (wholesale partner)
✅ Run Check #2 (keyword match)
✅ Store both results + product_categories
```

---

## Quick Match Logic

### Simple Keyword Matching Function:

```python
def quick_match_keywords_against_categories(
    new_keywords: List[str],
    stored_categories: List[str]
) -> Dict[str, Any]:
    """
    Quick match without AI.
    
    Returns:
    {
        'confidence': 'strong_match' | 'no_match' | 'uncertain',
        'matched': bool or None (None if uncertain),
        'match_count': int,
        'reasoning': str
    }
    """
    
    # Normalize (lowercase, strip)
    keywords_normalized = [kw.lower().strip() for kw in new_keywords]
    categories_normalized = [cat.lower().strip() for cat in stored_categories]
    
    # Check for matches
    matches = []
    for keyword in keywords_normalized:
        # Exact match
        if keyword in categories_normalized:
            matches.append(keyword)
            continue
        
        # Partial match (keyword contained in category)
        for category in categories_normalized:
            if keyword in category or category in keyword:
                matches.append(f"{keyword} → {category}")
                break
    
    match_count = len(matches)
    total_keywords = len(keywords_normalized)
    
    # Determine confidence
    if match_count == 0:
        return {
            'confidence': 'no_match',
            'matched': False,
            'match_count': 0,
            'reasoning': f'No keywords matched stored categories'
        }
    elif match_count == total_keywords:
        return {
            'confidence': 'strong_match',
            'matched': True,
            'match_count': match_count,
            'reasoning': f'All {total_keywords} keywords matched categories'
        }
    elif match_count >= total_keywords * 0.5:  # At least 50% match
        return {
            'confidence': 'strong_match',
            'matched': True,
            'match_count': match_count,
            'reasoning': f'{match_count}/{total_keywords} keywords matched (strong match)'
        }
    else:
        return {
            'confidence': 'uncertain',
            'matched': None,  # Uncertain
            'match_count': match_count,
            'reasoning': f'Only {match_count}/{total_keywords} keywords matched - ambiguous, needs AI check'
        }
```

### Example Matching:

**Stored Categories:** ["Golf Equipment", "Golf Apparel", "Pro Shop Items", "Athletic Footwear"]

**New Keywords: "golf equipment"**
- ✅ Strong match (exact match)
- No AI re-run needed

**New Keywords: "fishing gear"**
- ❌ No match
- No AI re-run needed (clearly not a fit)

**New Keywords: "golf, athletic"**
- ✅ Strong match (both match)
- No AI re-run needed

**New Keywords: "outdoor sports, recreation"**
- ⚠️ Uncertain (could be related, but not clear)
- Re-run AI Check #2

---

## Implementation in Pre-Check

### Step 0: Pre-Check Supabase

```python
def check_existing_companies_in_supabase(keywords, qualification_criteria):
    """
    1. Query: WHERE wholesale_partner_check = TRUE
    2. For each company:
       a. If wholesale_partner_check = FALSE → Skip (not a fit)
       b. If wholesale_partner_check = TRUE:
          - Check if has product_categories
          - Run quick_match_keywords_against_categories()
          - If strong_match:
            → Add to qualified list (no AI needed)
          - If no_match:
            → Mark as not qualified
            → Add to "no_match_but_wholesale" list (for later re-check if appears in Prospeo)
          - If uncertain:
            → Re-run AI Check #2
            → Add to qualified list if passes
    3. Return:
       - qualified_companies: List of companies qualified for this search
       - no_match_but_wholesale: List of companies to re-check if they appear in Prospeo
    """
```

### Step 3: Check Prospeo Companies

```python
for company in prospeo_companies:
    company_id = company['id']
    
    # Check if this company was in pre-check
    if company_id in no_match_but_wholesale_list:
        # Was marked no_match in pre-check, but Prospeo returned it
        # Re-run AI Check #2 (might actually be a match)
        keyword_result = run_ai_check_2(company, new_keywords)
        
        if keyword_result['matches']:
            # AI says it's a match - qualified!
            qualified_companies.append(company)
            update_company(company_id, keyword_result)
        else:
            # AI confirms it's not a match
            mark_as_not_qualified(company_id)
    
    elif company_id in pre_check_qualified_list:
        # Already qualified in pre-check - skip
        continue
    
    elif company_exists_in_supabase(company_id):
        # Exists but wasn't in pre-check (might be wholesale_partner_check = FALSE)
        if wholesale_partner_check == FALSE:
            skip_company()
        else:
            # Run quick match or AI check
            ...
    else:
        # New company - run both checks
        ...
```

---

## Benefits

1. ✅ **Saves AI Credits**: Most matches resolved without AI re-run
2. ✅ **Fast**: Quick matching is instant vs. AI API call
3. ✅ **Accurate**: AI still used when uncertain
4. ✅ **Smart**: Leverages stored product_categories for efficiency

---

## Updated Flow Summary

### Step 0: Pre-Check Supabase

**wholesale_partner_check = FALSE**
→ Skip, move on

**wholesale_partner_check = TRUE**
→ Quick match new keywords vs. stored categories
→ If strong match: Add to qualified list (no AI)
→ If no match: Mark as not qualified, BUT add to "re-check if in Prospeo" list
→ If uncertain: Re-run AI Check #2

**Returns:**
- `qualified_companies`: Companies qualified for this search
- `no_match_but_wholesale`: Companies to re-check if they appear in Prospeo

### Step 2: Prospeo Company Search
→ Search for NEW companies (not in pre-check qualified list)

### Step 3: Check Each Prospeo Company

**If company in `no_match_but_wholesale` list:**
→ Re-run AI Check #2 (Prospeo returned it, worth re-checking)
→ If AI passes: Qualified for this search
→ If AI fails: Confirm not qualified

**If company in pre-check qualified list:**
→ Already qualified, skip

**If company exists but `wholesale_partner_check = FALSE`:**
→ Skip entirely

**If company is NEW:**
→ Run both Check #1 and Check #2
→ Store all results including product_categories

---

This hybrid approach maximizes efficiency while maintaining accuracy!
