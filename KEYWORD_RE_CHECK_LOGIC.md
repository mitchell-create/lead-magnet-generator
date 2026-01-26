# Keyword Re-Check Logic for Existing Companies

## Important Clarification

**For existing companies in Supabase, we ALWAYS re-run Check #2 (keyword match) with the NEW search keywords**, even if the company was previously qualified.

---

## Why Re-Check Keywords?

### Scenario Example:
- **Previous Search:** Keywords = "golf equipment"
- **Company XYZ:** Qualified (matches "golf equipment")
- **New Search:** Keywords = "fishing gear"
- **Company XYZ:** Should NOT qualify (doesn't match "fishing gear")

### The Problem:
If we skip verification, Company XYZ would be added to the qualified list even though it doesn't match the new keywords.

### The Solution:
Always re-run Check #2 (keyword match) with the current search's keywords.

---

## Updated Logic Flow

### For Existing Companies in Supabase:

**Case 1: Company has `wholesale_partner_check = FALSE`**
```
❌ Skip this company entirely
   → Not a wholesale partner (won't become one)
   → Move to next company
   → No checks needed
```

**Case 2: Company has `wholesale_partner_check = TRUE`**
```
✅ Skip Check #1 (wholesale verification)
   → Company type doesn't change (still a multi-brand retailer)
   
Step 1: Quick Match (No AI)
   → Match new keywords against stored product_categories
   → Use simple matching logic
   
Step 2: Determine Result
   - Strong Match → Qualified for THIS search (no AI needed)
   - No Match → NOT qualified for THIS search (no AI needed)
   - Uncertain → Re-run AI Check #2 with NEW keywords
   
Result:
- Most cases: No AI re-run needed (saves credits)
- Uncertain cases: Re-run Check #2 to get accurate result
- Update product_categories if AI was re-run
```

**Case 3: Company is NEW (not in Supabase)**
```
✅ Run Check #1 (wholesale verification)
✅ Run Check #2 (keyword match)
✅ Save all results
```

---

## Implementation Details

### Step 0: Pre-Check Supabase (BEFORE Prospeo)

```python
def check_existing_companies_in_supabase(keywords, qualification_criteria):
    """
    1. Query Supabase for companies where wholesale_partner_check = TRUE
    2. For each company:
       a. Re-run Check #2 with NEW keywords
       b. If Check #2 passes → Add to qualified list
       c. Update product_categories with new results
    3. Return list of companies qualified for THIS search
    """
```

### Step 3: Check Prospeo Companies Against Supabase

```python
for company in prospeo_companies:
    existing_company = check_company_exists(company_id)
    
    if existing_company:
        if existing_company['wholesale_partner_check'] == True:
            # Skip Check #1 - already verified as wholesale partner
            # ALWAYS re-run Check #2 with NEW keywords
            keyword_result = run_check_2(
                company=company,
                keywords=NEW_KEYWORDS,  # Current search keywords
                qualification_criteria=qualification_criteria
            )
            
            # Update company record with new Check #2 results
            update_company(
                company_id=company_id,
                keyword_match_check=keyword_result['matches'],
                keyword_match_response=keyword_result['response'],
                product_categories=keyword_result['categories'],
                is_qualified=keyword_result['matches']  # Only qualified if Check #2 passes
            )
            
            if keyword_result['matches']:
                qualified_companies.append(company)
        else:
            # Re-run both checks
            run_both_checks(...)
    else:
        # New company - run both checks
        save_and_verify_company(...)
```

---

## Benefits of This Approach

1. ✅ **Accurate Results**: Companies only qualify if they match CURRENT search keywords
2. ✅ **Saves Credits**: Skip Check #1 for existing wholesale partners (doesn't change)
3. ✅ **Fresh Data**: Always get current keyword match results
4. ✅ **Updated Categories**: product_categories always reflect latest Check #2 analysis

---

## Summary

**Key Rule:**
- **Check #1 (Wholesale)**: Can be skipped if already TRUE (company type doesn't change)
- **Check #2 (Keywords)**: ALWAYS re-run with new search keywords (criteria change per search)

This ensures companies are only qualified if they match the CURRENT search criteria, not previous search criteria.
