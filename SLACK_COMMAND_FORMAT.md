# Slack Command Format - Complete Guide

## Command Structure

```
/lead-magnet <filters>
```

---

## Complete Command Template

```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```

---

## All Available Components

### 1. **`keywords=`** - REQUIRED ✅

**Purpose:** Keywords to match companies against. Automatically converted to Prospeo's `company_keywords` filter for company search AND used for AI qualification.

**Important:** Use `keywords=` in Slack commands (NOT `company_keywords=`). The system automatically converts `keywords=` to `company_keywords` when calling Prospeo API.

**Format:**
```
keywords=value1,value2,value3
```

**Examples:**
```
keywords=golf retailers
keywords=golf retailers, pro shops
keywords=athletic wear, sportswear retailers
keywords=IT resellers, tech distributors
```

**What happens if excluded:**
- ⚠️ Error: Keywords are required for meaningful qualification

**Required:** YES

---

### 2. **`industry=`** - RECOMMENDED ⚠️

**Purpose:** Filter companies by their industry in Prospeo search.

**Format:**
```
industry=value1,value2
```

**Examples:**
```
industry=Retail
industry=Retail,Sports
industry=Technology,Software
```

**Important Notes:**
- 💡 **Use Prospeo dashboard "API JSON" builder to find exact industry enum values**
- Values are **case-sensitive** and must match exactly
- If invalid, Prospeo API will return an error with the exact problem

**How to find valid values:**
1. Go to Prospeo dashboard
2. Build a search with industry filter
3. Click "..." → "API JSON"
4. See exact enum values used

**What happens if excluded:**
- Searches ALL industries
- Very broad results
- More irrelevant companies processed

**Required:** NO (but highly recommended)

---

### 3. **`location=`** - RECOMMENDED ⚠️

**Purpose:** Filter companies by their geographical location.

**Format:**
```
location=value1,value2
```

**Examples:**
```
location=United States
location=California,New York
location=United States,Canada
location=London,Paris
```

**What happens if excluded:**
- Searches ALL locations worldwide
- Very broad results
- More irrelevant companies processed

**Required:** NO (but highly recommended)

---

### 4. **`seniority=`** - RECOMMENDED ⚠️

**Purpose:** Filter persons by their seniority level. Applied when searching for persons at qualified companies.

**Format:**
```
seniority=value1,value2
```

**Valid Values:**
- `Founder/Owner`
- `C-Suite`
- `Partner`
- `Vice President`
- `Head`
- `Director`
- `Manager`
- `Senior`
- `Intern`
- `Entry`

**Examples:**
```
seniority=Founder/Owner
seniority=Founder/Owner,C-Suite
seniority=C-Suite,Vice President,Director
seniority=Director,Manager
```

**Important Notes:**
- Values are **validated** before sending to API
- Must use exact values listed above
- Applied ONLY when searching persons at qualified companies (not in initial company discovery)

**What happens if excluded:**
- Finds persons of ALL seniority levels at qualified companies
- May include entry-level, interns, etc.
- Less targeted results

**Required:** NO (but highly recommended for targeting decision-makers)

**Reference:** See `PROSPEO_SENIORITY_LEVELS.md` for detailed explanations.

---

### 5. **`our-company-details=`** - RECOMMENDED ⚠️

**Purpose:** Provides a description of your company and products to the AI, helping it better understand your target market and product alignment.

**Format:**
```
our-company-details="Your description here"
```

**Examples:**
```
our-company-details="We sell premium golf equipment and accessories"
our-company-details="We are a B2B technology reseller specializing in cloud solutions"
our-company-details="We manufacture outdoor gear for camping and hiking"
```

**What happens if excluded:**
- Uses a generic default description
- AI qualification might be less precise without specific context about your offerings

**Required:** NO (but recommended for optimal AI qualification)

---

## Complete Examples

### Example 1: Golf Equipment Retailers
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail,Sports | location=United States | seniority=Founder/Owner,C-Suite | our-company-details="We sell premium golf equipment and accessories"
```

### Example 2: Tech Resellers
```
/lead-magnet keywords=IT resellers, tech distributors | industry=Technology | location=United States,Canada | seniority=C-Suite,Vice President | our-company-details="We are a B2B technology reseller specializing in cloud solutions"
```

### Example 3: Minimal (Keywords Only)
```
/lead-magnet keywords=athletic wear retailers
```
⚠️ **Note:** This will search ALL industries and ALL locations - not recommended

### Example 4: Without Seniority
```
/lead-magnet keywords=golf retailers | industry=Retail | location=United States
```
⚠️ **Note:** Will find persons of ALL seniority levels at qualified companies

---

## How the Workflow Works

1. **Company Discovery**: Searches companies using `keywords`, `industry`, `location` filters
   - **`keywords=` from Slack command is automatically converted to `company_keywords`** for Prospeo `/search-company` API endpoint
   - Seniority is NOT used in this phase

2. **AI Qualification**: Qualifies companies using:
   - Wholesale partner check (multi-brand retailer?)
   - Keyword/product fit check (using `keywords` and `our-company-details`)

3. **Person Search**: For each qualified company, searches persons with `seniority` filter
   - Seniority filter applied here
   - Finds ALL persons matching seniority criteria

4. **Email Enrichment**: Enriches emails for all persons found

---

## Validation & Error Handling

### Seniority Validation
- ✅ **Pre-validated** before sending to API
- If invalid: Slack shows error with valid values list
- Example error: "Invalid seniority level(s): CEO"

### Industry Validation
- ✅ **Validated by Prospeo API** directly
- If invalid: Prospeo returns clear error message
- Slack shows formatted error with guidance
- Example error: "The value 'RetailStores' is not supported for the filter 'company_industry'"

### Keywords
- ✅ **Required** - Must be provided
- Use `keywords=` in Slack command (NOT `company_keywords=`)
- Automatically converted to `company_keywords` for Prospeo API
- Multiple keywords separated by commas

---

## Best Practices

1. **Always include `keywords`** - Required for meaningful results
2. **Include `industry`** - Use dashboard "API JSON" to find exact values
3. **Include `location`** - Narrow down geographic scope
4. **Include `seniority`** - Target decision-makers
5. **Include `our-company-details`** - Improve AI qualification accuracy

---

## Finding Exact Filter Values

### Industry Values
1. Go to Prospeo dashboard
2. Navigate to Company Search
3. Add industry filter
4. Click "..." → "API JSON"
5. See exact enum values

### Seniority Values
- Use exact values from the list above
- See `PROSPEO_SENIORITY_LEVELS.md` for detailed explanations

---

## Quick Reference

| Component | Required | Validated By | Notes |
|-----------|----------|--------------|-------|
| `keywords` | ✅ Yes | - | Multiple values comma-separated |
| `industry` | ⚠️ Recommended | Prospeo API | Use dashboard "API JSON" for exact values |
| `location` | ⚠️ Recommended | Prospeo API | Case-sensitive, must match exactly |
| `seniority` | ⚠️ Recommended | Pre-validated | Exact values required (see list above) |
| `our-company-details` | ⚠️ Recommended | - | Quoted string recommended |

---

## Common Mistakes

❌ **Incorrect:**
```
/lead-magnet industry=tech  (wrong: lowercase, should be "Technology")
/lead-magnet seniority=CEO  (wrong: should be "C-Suite")
/lead-magnet keywords=golf  (missing other filters - too broad)
```

✅ **Correct:**
```
/lead-magnet keywords=golf retailers | industry=Retail | location=United States | seniority=C-Suite
```

---

## Need Help?

- See `PROSPEO_SENIORITY_LEVELS.md` for seniority explanations
- See `INDUSTRY_VALIDATION_UPDATE.md` for industry validation details
- Check Prospeo dashboard "API JSON" builder for exact filter values
