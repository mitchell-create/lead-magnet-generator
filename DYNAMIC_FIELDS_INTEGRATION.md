# Dynamic Fields Integration Plan

## Current Dynamic Fields in Prompt

The keyword match prompt uses these dynamic placeholders:

1. **`{{our_company_details}}`** - Description of our company/products
   - **Current Source:** `qualification_criteria.get('our_company_details')` or default
   - **Need:** How should this be provided?

2. **`{{target_company_keywords}}`** - Keywords from Slack
   - **Current Source:** ✅ From Slack command `keywords=` parameter
   - **Status:** Working

3. **`{{website}}`** - Company website URL
   - **Current Source:** ✅ From Prospeo `company_data.get('website')` or `domain`
   - **Status:** Working

4. **`{{company_description}}`** - Company description
   - **Current Source:** ✅ From Prospeo `company_data.get('description')`
   - **Status:** Working

---

## Questions for Integration

### 1. What is "Instantly"?
- Is this a platform/service we need to integrate?
- What data does it provide?
- How do we access it (API, webhook, etc.)?

### 2. Which Fields Should Come from Instantly?
- `{{our_company_details}}`?
- Company information?
- Product details?
- Campaign/campaign details?

### 3. How Should We Integrate Instantly Data?
- **Option A:** Pass via Slack command
  ```
  /lead-magnet keywords=golf retailers | our-company="We sell premium golf equipment"
  ```
  
- **Option B:** Environment variable / config
  ```
  OUR_COMPANY_DETAILS="We sell premium golf equipment"
  ```
  
- **Option C:** Instantly API integration
  ```python
  instantly_data = fetch_from_instantly(campaign_id)
  our_company_details = instantly_data.get('company_description')
  ```

- **Option D:** Database/Storage
  - Store company details in Supabase
  - Fetch by campaign/user ID

---

## Current Implementation

The prompt template is already set up for dynamic fields:

```python
prompt = f"""...
Our Company: {our_company_info}
Target Keywords/Industries: {keywords_list}
Company Website: {company_website}
Company Description: {company_data.get('description', 'N/A')}
..."""
```

**All fields are dynamic** - the prompt works for:
- ✅ Golf equipment
- ✅ Clothing companies  
- ✅ Tech products
- ✅ Any industry

The examples in the prompt (golf courses, ski resorts) are just **examples** - not hardcoded to golf!

---

## Next Steps

1. **Clarify Instantly integration**
2. **Determine data flow** (where does each field come from)
3. **Update Slack command** to accept Instantly fields if needed
4. **Update qualification_criteria** structure to include Instantly data
5. **Test with multiple use cases** (golf, clothing, tech, etc.)

---

## Example: How It Works for Any Industry

### Golf Example:
```
keywords=golf retailers, pro shops
our_company="We sell premium golf equipment"
→ Prompt dynamically inserts these fields
```

### Clothing Example:
```
keywords=athletic wear, sportswear retailers
our_company="We sell premium athletic clothing"
→ Same prompt, different dynamic fields
```

### Tech Example:
```
keywords=IT resellers, tech distributors
our_company="We sell enterprise software solutions"
→ Same prompt, different dynamic fields
```

**The prompt template stays the same - only the dynamic fields change!**
