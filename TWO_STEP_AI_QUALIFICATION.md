# Two-Step AI Qualification Strategy

## Overview

We use **TWO separate, focused AI checks** instead of one combined check. This improves accuracy and makes debugging easier.

---

## Why Two Separate Checks?

### ✅ **Better Accuracy**
- Each AI check focuses on ONE specific task
- Less cognitive load = better results
- `gpt-oss-20b` performs better with focused prompts

### ✅ **Better Debugging**
- Know exactly which check failed
- Can optimize each prompt independently
- Clearer logs: "Failed wholesale check" vs "Failed keyword check"

### ✅ **Cost Efficiency**
- If wholesale check fails, skip keyword check (saves money)
- Two smaller, focused prompts may be more efficient than one large prompt

---

## The Two Checks

### **Check #1: Wholesale Partner Type**
**Question:** Is this a multi-brand retailer/reseller (not a manufacturer)?

**Focus:**
- ✅ Multi-brand retailers who could stock our products
- ❌ Manufacturers who only sell their own products

**Response:** YES or NO

---

### **Check #2: Keyword Match** (Only if Check #1 passes)
**Question:** Does this company match our keywords?

**Focus:**
- ✅ Company matches specified keywords (e.g., "golf retailers")
- ❌ Company does NOT match keywords

**Response:** YES or NO

---

## Final Qualification

**Company is QUALIFIED only if:**
- ✅ Check #1: YES (is a wholesale partner)
- ✅ Check #2: YES (matches keywords)

**If either check fails → Company is NOT qualified**

---

## Example Flow

### Example 1: Qualified Company

**Company:** Golf Pro Shop Inc.

**Check #1: Wholesale Partner Type**
- Has "Brands" section showing Titleist, Callaway, TaylorMade
- Product titles include brand names
- **Result:** YES ✅

**Check #2: Keyword Match**
- Keywords: "golf retailers, pro shops"
- Company description mentions "golf equipment retailer"
- Website has "golf" in title and products
- **Result:** YES ✅

**Final:** QUALIFIED ✅

---

### Example 2: Fails Wholesale Check

**Company:** Golf Ball Manufacturing Co.

**Check #1: Wholesale Partner Type**
- Has "Dealers" page recruiting stores
- Products are all their own brand
- "We manufacture" in description
- **Result:** NO ❌

**Check #2: Keyword Match**
- **SKIPPED** (Check #1 failed)

**Final:** NOT QUALIFIED ❌

---

### Example 3: Fails Keyword Check

**Company:** Multi-Brand Sports Retailer

**Check #1: Wholesale Partner Type**
- Carries multiple brands (Nike, Adidas, Under Armour)
- **Result:** YES ✅

**Check #2: Keyword Match**
- Keywords: "golf retailers, pro shops"
- Company sells general sports equipment, NOT golf-specific
- **Result:** NO ❌

**Final:** NOT QUALIFIED ❌

---

## Code Structure

### `AIQualifier` Class Methods

```python
# Check #1: Wholesale Partner Type
is_wholesale_partner, response1 = qualifier.check_wholesale_partner_type(
    company_data=company_data,
    scraped_content=scraped_content
)

# Check #2: Keyword Match (only if Check #1 passes)
if is_wholesale_partner and keywords:
    matches_keywords, response2 = qualifier.check_keyword_match(
        company_data=company_data,
        keywords=keywords,
        scraped_content=scraped_content
    )
else:
    matches_keywords = False  # Skip if not wholesale partner

# Final qualification
is_qualified = is_wholesale_partner and matches_keywords
```

---

## Logging

Each check is logged separately:

```
INFO: Wholesale check for Acme Corp: YES
INFO: Keyword check for Acme Corp: YES (keywords: golf retailers, pro shops)
INFO: Final qualification for Acme Corp: Wholesale: YES | Keywords: YES -> QUALIFIED: True
```

This makes it easy to see exactly where a company failed!

---

## Benefits Summary

1. ✅ **Better accuracy** - Focused prompts work better
2. ✅ **Cost savings** - Skip keyword check if wholesale fails
3. ✅ **Easier debugging** - Know exactly which check failed
4. ✅ **Independent optimization** - Improve each prompt separately
5. ✅ **Clearer results** - Understand why a company qualified or not
