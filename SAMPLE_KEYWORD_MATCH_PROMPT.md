# Sample Keyword Match Prompt (Check #2)

## Overview

This is the prompt used for **Check #2: Keyword Match**. It focuses ONLY on determining if the company matches the specified keywords/criteria from your Slack command.

---

## Example Scenario

**Slack Command:**
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail
```

**Extracted Keywords:** `['golf retailers', 'pro shops']`

---

## Sample Prompt (What the AI Sees)

```
Determine if this company matches the specified keywords/criteria.

KEYWORD MATCH CHECK:

🎯 TARGET KEYWORDS/CRITERIA TO MATCH:
golf retailers, pro shops

The company must align with these keywords/criteria. Check if their products, services, business model, industry, or content matches the keywords.

How to check:
- Review company description for keyword matches
- Check website content for relevant terms
- Look for products/services related to keywords
- Evaluate industry classification
- Check product listings or service offerings

Match examples:
- If keywords are "golf retailers" → Look for golf equipment, golf products, golf-related services
- If keywords are "outdoor gear" → Look for camping, hiking, outdoor equipment
- If keywords are "tech resellers" → Look for IT products, technology distribution

COMPANY INFORMATION:

Company Name: Acme Golf Supply
Company Website: https://acmegolf.com
Company Description: Acme Golf Supply is a leading retailer of golf equipment, apparel, and accessories. We carry top brands including Titleist, Callaway, TaylorMade, and more. Our pro shop offers custom club fitting and golf lessons.
Company Industry: Retail

================================================================================
SCRAPED WEBSITE CONTENT:
================================================================================
Navigation: Home, Shop Golf Equipment, Brands, Pro Shop, Lessons, About
Footer: Golf Clubs, Golf Balls, Golf Apparel, Golf Accessories, Pro Shop Services
Product Categories: Drivers, Irons, Putters, Wedges, Golf Balls, Golf Bags, Golf Apparel
Brands Carried: Titleist, Callaway, TaylorMade, Ping, Cobra, Mizuno
Product Examples: Titleist Pro V1 Golf Balls, Callaway Driver, TaylorMade Irons
Services: Custom Club Fitting, Golf Lessons, Pro Shop Services
================================================================================

VERDICT:
Respond with ONLY:
- YES - if the company matches the keywords/criteria above
- NO - if the company does NOT match the keywords or you are unsure
```

---

## Analysis of This Example

**Keywords to Match:** `golf retailers, pro shops`

**Company Evidence:**
- ✅ Company name includes "Golf"
- ✅ Description mentions "golf equipment, apparel, and accessories"
- ✅ Description mentions "pro shop"
- ✅ Website has "Pro Shop" in navigation
- ✅ Services include "Pro Shop Services"
- ✅ All products are golf-related
- ✅ Industry is Retail (matches "retailers")

**AI Decision:** YES ✅

**Reasoning:** Company clearly matches "golf retailers" (sells golf equipment) and "pro shops" (has pro shop services).

---

## More Examples

### Example 2: Strong Match

**Keywords:** `outdoor gear, camping supplies`

**Company:** Mountain Outdoor Supply
**Description:** "We specialize in camping gear, hiking equipment, and outdoor adventure supplies."

**Scraped Content:**
- Products: Tents, Sleeping Bags, Hiking Backpacks, Camping Stoves
- Categories: Camping, Hiking, Outdoor Gear

**AI Decision:** YES ✅ (clearly matches "outdoor gear, camping supplies")

---

### Example 3: Weak Match

**Keywords:** `golf retailers, pro shops`

**Company:** Sports Equipment Warehouse
**Description:** "We sell a wide variety of sports equipment including basketball, soccer, tennis, and some golf items."

**Scraped Content:**
- Products: Basketballs, Soccer Balls, Tennis Rackets, Golf Clubs (small selection)
- Focus: General sports, not golf-specific
- No pro shop services

**AI Decision:** NO ❌ (golf is a small part, doesn't match "golf retailers" or "pro shops")

---

### Example 4: Partial Match

**Keywords:** `tech resellers, IT distributors`

**Company:** Tech Solutions Inc.
**Description:** "We provide IT consulting services and occasionally resell software licenses."

**Scraped Content:**
- Services: IT Consulting, Cloud Migration, Software Licensing
- Focus: Services first, occasional reselling
- Not primarily a reseller/distributor

**AI Decision:** NO ❌ (primarily a service company, not a reseller/distributor)

---

### Example 5: No Match

**Keywords:** `golf retailers, pro shops`

**Company:** Fashion Boutique LLC
**Description:** "We sell trendy women's clothing and accessories."

**Scraped Content:**
- Products: Dresses, Handbags, Shoes, Jewelry
- No golf-related content at all

**AI Decision:** NO ❌ (completely unrelated to golf)

---

## Key Matching Criteria

The AI looks for matches in:

1. **Company Name**
   - Does it contain keywords or related terms?
   - Example: "Golf Pro Shop" → matches "golf retailers, pro shops"

2. **Company Description**
   - Mentions of keywords or related products/services
   - Example: "sells golf equipment" → matches "golf retailers"

3. **Scraped Website Content**
   - Navigation menu items
   - Product categories
   - Service offerings
   - Brand names (if relevant)
   - Footer links

4. **Industry Classification**
   - Industry tag matches keyword context
   - Example: "Retail" industry + golf products → matches "golf retailers"

5. **Products/Services**
   - Product listings match keywords
   - Service offerings align with keywords

---

## What Counts as a Match?

### ✅ Strong Match
- Company name directly contains keywords
- Description explicitly mentions keywords
- Products/services are clearly related to keywords
- Website content is heavily focused on keyword topics

### ⚠️ Weak Match / Unclear
- Company sells many products, keywords are a small subset
- Description is vague or mentions keywords indirectly
- Products/services are tangentially related

### ❌ No Match
- Company has nothing to do with keywords
- Keywords mentioned but not primary focus
- Industry/description don't align

---

## Prompt Variations

### With Multiple Keywords

**Keywords:** `golf retailers, pro shops, custom club fitting`

The AI will check if the company matches ANY of these criteria (OR logic):
- Sells golf equipment (retailer)
- Has a pro shop
- Offers custom club fitting

If company matches at least one → YES

---

### With Single Keyword

**Keywords:** `golf retailers`

The AI focuses on a single criterion:
- Is this company a golf retailer?

More precise matching expected.

---

## Tips for Best Results

1. **Be Specific:** Use clear, specific keywords
   - ✅ Good: "golf retailers, pro shops"
   - ❌ Less clear: "golf stuff"

2. **Multiple Keywords:** Include related terms
   - ✅ Good: "outdoor gear, camping supplies, hiking equipment"
   - ❌ Too narrow: "tents" (might miss camping suppliers)

3. **Use Synonyms:** The AI understands context
   - "retailers" = "retail stores" = "shops" = "outlets"

4. **Industry Terms:** Include industry-specific language
   - "B2B distributors" vs "retailers"
   - "wholesalers" vs "resellers"

---

## Integration with Check #1

Remember: This keyword check only runs AFTER Check #1 (Wholesale Partner) passes.

**Flow:**
1. Check #1: Is it a wholesale partner? → YES ✅
2. Check #2: Does it match keywords? → YES ✅
3. Final: QUALIFIED ✅

If Check #1 fails, Check #2 is skipped entirely (saves cost).

---

## Sample Log Output

```
INFO: Keyword check for Acme Golf Supply: YES (keywords: golf retailers, pro shops)
```

Or if it fails:
```
INFO: Keyword check for Sports Warehouse: NO (keywords: golf retailers, pro shops)
```
