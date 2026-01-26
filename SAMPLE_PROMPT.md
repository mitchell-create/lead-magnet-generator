# Sample AI Qualification Prompt with Dynamic Keywords

## Overview

This prompt analyzes companies to determine if they match your criteria. Keywords from Slack are dynamically inserted into the prompt.

---

## Slack Command Format

```bash
/lead-magnet keywords=golf retailers, pro shops | industry=Retail | seniority=Founder
```

**Example with different keywords:**
```bash
/lead-magnet keywords=outdoor gear, camping supplies | industry=Retail
```

---

## How Keywords Work

1. **Slack Input:** `keywords=golf retailers, pro shops`
2. **Extracted:** `['golf retailers', 'pro shops']`
3. **Inserted into Prompt:** Dynamically placed in the "TARGET CRITERIA" section

---

## Sample Prompt Structure (What the AI Sees)

### With Keywords: "golf retailers, pro shops"

```
You are analyzing a company to determine if they are a GOOD FIT based on specific criteria.

🎯 TARGET CRITERIA / KEYWORDS TO MATCH:
golf retailers, pro shops

The company MUST match the above keywords/criteria to be considered a good fit. 
Analyze the company information, website content, and description to determine if 
they align with these target criteria.

QUALIFICATION CRITERIA:

1. WHOLESALE PARTNER TYPE - They must be a RETAILER/RESELLER who carries multiple 
   brands (and could stock our products), NOT a manufacturer who only sells their 
   own products.

✅ GOOD FIT = Multi-brand retailers who resell other companies' products
   Positive indicators:
   - "Brands" (plural), "Companies We Carry," "Shop by Brand" in navigation/footer
   - Brand filter dropdowns in product collections
   - Product titles include brand names (e.g., "Stanley 2L Water Bottle")
   - Multiple recognizable third-party brand names across products
   - OK if they also sell some house brand products (as long as primarily multi-brand)

❌ NOT A FIT = Manufacturers/brands who only sell their own products
   Negative indicators:
   - "Brand" (singular) section about their company story
   - "Dealers," "Wholesale," "Become a Distributor" pages (they're recruiting sellers)
   - "Where to Buy" or "Stockists" pages (they're the brand being distributed)
   - Product titles without brand names (all their own products)
   - FAQs only reference their own brand name
   - Focus on "our technology," "we manufacture" (indicates they're a maker, not reseller)

2. KEYWORD/CONTENT MATCH - The company must align with the target criteria/keywords 
   specified above.
   - Check if their products, services, or business model matches the keywords
   - Review company description, website content, and scraped data
   - Look for relevant industry terms, product categories, or business types

KEY INVESTIGATION STEPS:
1. Analyze company description and industry for keyword alignment
2. Check website navigation/menu/footer for brand indicators
3. Review product listings for brand variety
4. Look for dealer/wholesale pages (negative indicator)
5. Evaluate overall business model (retailer vs manufacturer)

COMPANY INFORMATION TO ANALYZE:

Company Name: Acme Golf Supply
Company Website: https://acmegolf.com
Company LinkedIn: https://linkedin.com/company/acme-golf
Company Description: Acme Golf Supply is a leading retailer of golf equipment, 
apparel, and accessories. We carry top brands including Titleist, Callaway, 
TaylorMade, and more.
Company Industry: Retail
Company Location: United States

================================================================================
SCRAPED WEBSITE CONTENT:
================================================================================
Navigation: Home, Brands, Products, About, Contact
Footer: Shop by Brand, Customer Service, Wholesale Inquiries
Brands Section: Titleist, Callaway, TaylorMade, Ping, Cobra, Mizuno...
Product Titles: Titleist Pro V1 Golf Balls, Callaway Driver, TaylorMade Irons...
================================================================================

VERDICT:
Based on the company information above, determine if this company:
1. Is a multi-brand retailer/reseller (not a manufacturer)
2. Matches the target keywords/criteria specified above

Respond with ONLY:
- YES - if the company meets BOTH criteria (is a retailer/reseller AND matches keywords)
- NO - if the company does NOT meet both criteria or you are unsure
```

---

## How Dynamic Keywords Are Inserted

### Code Location: `utils.py` → `format_qualification_template()`

```python
# Keywords from Slack are passed as target_companies parameter
keywords_list = ', '.join(target_companies)  # e.g., "golf retailers, pro shops"

# Inserted into prompt
keywords_section = f"""
🎯 TARGET CRITERIA / KEYWORDS TO MATCH:
{keywords_list}

The company MUST match the above keywords/criteria...
"""
```

---

## Example Scenarios

### Scenario 1: Golf Retailers
**Slack Command:**
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail
```

**Keywords in Prompt:**
```
🎯 TARGET CRITERIA / KEYWORDS TO MATCH:
golf retailers, pro shops
```

**AI Checks:**
- ✅ Do they sell golf products? (keyword match)
- ✅ Are they a retailer/reseller? (business model)
- ✅ Multi-brand or own brand only? (wholesale fit)

---

### Scenario 2: Outdoor Gear
**Slack Command:**
```
/lead-magnet keywords=outdoor gear, camping supplies, hiking equipment
```

**Keywords in Prompt:**
```
🎯 TARGET CRITERIA / KEYWORDS TO MATCH:
outdoor gear, camping supplies, hiking equipment
```

**AI Checks:**
- ✅ Do they sell outdoor/camping/hiking products? (keyword match)
- ✅ Are they a retailer/reseller? (business model)
- ✅ Multi-brand or own brand only? (wholesale fit)

---

### Scenario 3: Technology Resellers
**Slack Command:**
```
/lead-magnet keywords=IT resellers, tech distributors, software partners
```

**Keywords in Prompt:**
```
🎯 TARGET CRITERIA / KEYWORDS TO MATCH:
IT resellers, tech distributors, software partners
```

**AI Checks:**
- ✅ Do they resell IT/tech products? (keyword match)
- ✅ Are they a retailer/reseller? (business model)
- ✅ Multi-brand or own brand only? (wholesale fit)

---

## Customizing Keywords

You can use any keywords relevant to your industry:

```
/lead-magnet keywords=your keyword 1, your keyword 2, your keyword 3
```

The AI will check if the company matches these keywords in:
- Company description
- Website content
- Scraped website data
- Industry classification
- Product listings

---

## Notes

1. **Multiple Keywords:** Separate with commas (handled automatically)
2. **Case Insensitive:** Keywords are matched flexibly
3. **Context Aware:** AI understands meaning, not just exact matches
4. **Dynamic:** Keywords are inserted fresh for each qualification
