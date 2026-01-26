# Updated Keyword Match Prompt

## Overview

The keyword match prompt has been updated with your detailed, comprehensive version that focuses on product/industry fit rather than just keyword matching.

---

## Key Features

### 1. **Product/Industry Fit Focus**
- Determines if company sells products that align with your target market
- Checks if their product categories match your keywords
- Evaluates customer base and market positioning alignment

### 2. **Service Business Support**
- ✅ Recognizes service businesses with retail components (golf courses with pro shops)
- ❌ Excludes pure service providers with no retail component

### 3. **Comprehensive Analysis**
- Navigation/categories alignment
- Product collections review
- Service business retail component detection
- Price point and market segment evaluation
- Customer demographic alignment

### 4. **Structured Response Format**
The AI now provides:
- **VERDICT:** YES or NO
- **REASONING:** 1-2 sentences explaining the decision
- **EVIDENCE:** Top 2-3 specific supporting elements

---

## Response Parsing

The code extracts the VERDICT from responses like:

```
VERDICT: YES

REASONING: They have a dedicated golf equipment section and pro shop services, making them a perfect fit for golf product distribution.

EVIDENCE: Pro Shop navigation item, Golf Equipment category, Product listings include golf clubs and accessories
```

The system will correctly identify YES or NO from the VERDICT line.

---

## Optional: Our Company Details

You can optionally provide details about your company for better context:

**In Slack command (future enhancement):**
```
/lead-magnet keywords=golf retailers | our-company="We sell premium golf equipment and accessories"
```

**Or in qualification_criteria:**
```python
qualification_criteria = {
    'our_company_details': 'We sell premium golf equipment and accessories'
}
```

This helps the AI better understand your products when evaluating fit.

---

## Example Usage

**Input:**
- Keywords: `['golf retailers', 'pro shops']`
- Company: Acme Golf Supply (multi-brand retailer)

**AI Analysis:**
- Checks product categories → Golf equipment ✅
- Checks navigation → "Pro Shop" section ✅
- Checks products → Golf clubs, balls, accessories ✅
- Checks customer base → Golf enthusiasts ✅

**Response:**
```
VERDICT: YES

REASONING: They have a dedicated pro shop section and sell golf equipment across multiple brands, making them an ideal retail partner for golf products.

EVIDENCE: Pro Shop navigation item, Golf Equipment category with multiple brands, Product listings include Titleist, Callaway, and TaylorMade
```

**Result:** QUALIFIED ✅

---

## Integration

The prompt is now integrated into:
- ✅ `utils.py` → `format_keyword_match_prompt()`
- ✅ `layer3_ai_judge.py` → `check_keyword_match()`
- ✅ Response parsing handles VERDICT/REASONING/EVIDENCE format
- ✅ Logging includes full AI response for debugging

---

## Benefits

1. **More Accurate:** Focuses on product fit, not just keyword presence
2. **Better Context:** Understands service businesses with retail components
3. **Actionable Insights:** REASONING and EVIDENCE help understand AI decisions
4. **Flexible:** Handles adjacent categories and complementary products
5. **Clear Guidelines:** Detailed examples help AI make consistent judgments
