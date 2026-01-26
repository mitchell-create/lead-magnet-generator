# Slack Dynamic Fields Integration

## Overview

You can now pass dynamic fields via Slack command that will be plugged into the AI qualification prompts!

---

## How It Works

### Slack Command Format

```
/lead-magnet keywords=<keywords> | our-company-details="<your company description>"
```

**All fields in the prompt use dynamic values:**
- ✅ `{{target_company_keywords}}` → from `keywords=` parameter
- ✅ `{{our_company_details}}` → from `our-company-details=` parameter
- ✅ `{{website}}` → from Prospeo company data
- ✅ `{{company_description}}` → from Prospeo company data

---

## Available Dynamic Fields

### 1. **`keywords=`** (for AI keyword match check)
**Example:**
```
keywords=golf retailers, pro shops
keywords=athletic wear, sportswear retailers
keywords=IT resellers, tech distributors
```

**Gets inserted into prompt as:**
```
Target Keywords/Industries: golf retailers, pro shops
```

---

### 2. **`our-company-details=`** (NEW - for AI prompt context)
**Example:**
```
our-company-details="We sell premium golf equipment and accessories"
our-company-details="We are a B2B technology reseller specializing in enterprise software"
our-company-details="We sell athletic clothing and sportswear for active lifestyles"
```

**Gets inserted into prompt as:**
```
Our Company: We sell premium golf equipment and accessories
```

**Why this matters:**
- Helps AI understand your products
- Better context for matching companies
- More accurate qualification decisions

---

## Complete Examples

### Example 1: Golf Equipment
```
/lead-magnet keywords=golf retailers, pro shops | our-company-details="We sell premium golf equipment and accessories for golf enthusiasts"
```

**What happens:**
- Keywords: `golf retailers, pro shops` → Used in keyword match check
- Company Details: `We sell premium golf equipment...` → Used in prompt context
- Works for any company (golf-related or not!)

---

### Example 2: Athletic Clothing
```
/lead-magnet keywords=athletic wear, sportswear retailers | our-company-details="We sell premium athletic clothing and sportswear"
```

**Same prompt template, different dynamic values!**

---

### Example 3: Tech Resellers
```
/lead-magnet keywords=IT resellers, tech distributors | our-company-details="We are a B2B technology reseller specializing in enterprise software solutions"
```

**Same prompt template, different dynamic values!**

---

## How Dynamic Fields Flow

```
Slack Command
    ↓
Parse Slack Input
    ↓
Extract Dynamic Fields
    ├─ keywords → target_companies
    └─ our-company-details → qualification_criteria['our_company_details']
    ↓
Pass to AI Qualification
    ├─ Check #1: Wholesale Partner Type
    └─ Check #2: Keyword Match (uses dynamic fields)
        ├─ Keywords from Slack
        ├─ Our Company Details from Slack
        ├─ Company Website from Prospeo
        └─ Company Description from Prospeo
    ↓
AI Prompt with All Dynamic Fields Inserted
```

---

## The Prompt is 100% General!

The prompt template itself is **completely industry-agnostic**. It uses:
- ✅ Dynamic keywords (works for golf, clothing, tech, anything!)
- ✅ Dynamic company details (works for any product category!)
- ✅ Examples are just guidance (not hardcoded to golf)

**Examples in the prompt (golf courses, ski resorts) are just examples** - the AI understands they're illustrative, not requirements!

---

## Testing

Try these different industries:

**Golf:**
```
/lead-magnet keywords=golf retailers | our-company-details="We sell golf equipment"
```

**Clothing:**
```
/lead-magnet keywords=athletic wear retailers | our-company-details="We sell athletic clothing"
```

**Tech:**
```
/lead-magnet keywords=IT resellers | our-company-details="We sell enterprise software"
```

**All use the same prompt template - only dynamic fields change!**

---

## Benefits

1. ✅ **Fully Dynamic** - Works for any industry
2. ✅ **Flexible** - Pass any keywords/company details via Slack
3. ✅ **Reusable** - Same codebase for all use cases
4. ✅ **Easy to Use** - Just pass fields in Slack command

---

## Future Dynamic Fields

You can easily add more dynamic fields:

**In Slack:**
```
our-company-details=
target-price-point=
target-customer-segment=
```

**In Code:**
Just add to `parse_prospeo_filters()`:
```python
if key in ['target-price-point', ...]:
    qualification_criteria['target_price_point'] = value
```

Then use in prompt:
```python
{qualification_criteria.get('target_price_point', 'N/A')}
```
