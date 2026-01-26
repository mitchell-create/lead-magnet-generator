# Slack Command Structure - Complete Guide

## Command Format

```
/lead-magnet <filters>
```

---

## All Available Components

### 1. **`keywords=`** - TARGET KEYWORDS (For AI Keyword Match Check)
**Purpose:** Keywords to match companies against (used in Check #2)

**Format:**
```
keywords=value1,value2,value3
```

**Examples:**
```
keywords=golf retailers
keywords=golf retailers, pro shops
keywords=athletic wear, sportswear retailers
```

**What happens if excluded:**
- ❌ **Check #2 (Keyword Match) will be SKIPPED**
- ⚠️ Only Check #1 (Wholesale Partner Type) will run
- ⚠️ Companies will be qualified based ONLY on being a multi-brand retailer
- ⚠️ No keyword filtering will occur

**Required:** YES (for meaningful qualification)

---

### 2. **`our-company-details=`** - YOUR COMPANY DESCRIPTION (For AI Context)
**Purpose:** Describes your company/products for better AI qualification

**Format:**
```
our-company-details="Your description here"
```

**Examples:**
```
our-company-details="We sell premium golf equipment and accessories"
our-company-details="We are a B2B technology reseller"
```

**What happens if excluded:**
- ✅ System uses default: `"Multi-brand retailer/reseller looking for partners to stock our products"`
- ⚠️ AI has less context about your products
- ⚠️ May be less accurate in determining fit

**Required:** NO (optional, but recommended for better results)

---

### 3. **`industry=`** - COMPANY INDUSTRIES (Prospeo Filter)
**Purpose:** Filters companies by industry in Prospeo search

**Format:**
```
industry=Industry1,Industry2
```

**Examples:**
```
industry=Retail
industry=Retail,Sports
industry=Technology,Software
```

**What happens if excluded:**
- ✅ Prospeo will search ALL industries
- ⚠️ Much broader search results
- ⚠️ May process more irrelevant companies (costs more time/money)
- ⚠️ Default filter may be applied: `{"company_industry": {"include": ["Technology"]}}`

**Required:** NO (but recommended to narrow search)

---

### 4. **`location=`** - COMPANY LOCATION (Prospeo Filter)
**Purpose:** Filters companies by location in Prospeo search

**Format:**
```
location=Location1,Location2
```

**Examples:**
```
location=United States
location=California,New York
location=United States,Canada
```

**What happens if excluded:**
- ✅ Prospeo will search ALL locations
- ⚠️ Much broader search results
- ⚠️ International companies included
- ⚠️ May process more irrelevant companies

**Required:** NO (but recommended to narrow search)

---

### 5. **`seniority=`** - PERSON SENIORITY (Prospeo Filter)
**Purpose:** Filters persons by seniority level in Prospeo search

**Format:**
```
seniority=Level1,Level2
```

**Examples:**
```
seniority=Founder
seniority=Founder,C-Suite
seniority=VP,Director
```

**What happens if excluded:**
- ✅ Prospeo will return persons at ANY seniority level
- ⚠️ Much broader search results
- ⚠️ May include junior employees, assistants, etc.

**Required:** NO (but recommended for decision-makers)

---

### 6. **`verified-email=`** - EMAIL VERIFICATION (Prospeo Filter)
**Purpose:** Only return persons with verified email addresses

**Format:**
```
verified-email=true
verified-email=false
```

**Examples:**
```
verified-email=true
verified-email=false
```

**What happens if excluded:**
- ✅ Defaults to `false` (includes unverified emails)
- ⚠️ May get more results but lower quality contacts

**Required:** NO (optional, but `true` recommended for quality)

---

## Complete Command Examples

### Minimal Command (Keywords Only)
```
/lead-magnet keywords=golf retailers
```
**What runs:**
- ✅ Prospeo: Searches ALL industries, ALL locations, ALL seniorities
- ✅ Check #1: Wholesale Partner Type
- ✅ Check #2: Keyword Match (golf retailers)
- ⚠️ Very broad search - may process many irrelevant companies

---

### Recommended Command
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail | location=United States | seniority=Founder,C-Suite | our-company-details="We sell premium golf equipment" | verified-email=true
```

**What runs:**
- ✅ Prospeo: Narrow search (Retail industry, US location, Founder/C-Suite)
- ✅ Check #1: Wholesale Partner Type
- ✅ Check #2: Keyword Match (golf retailers, pro shops)
- ✅ Better AI context (our company details)
- ✅ Quality contacts (verified emails only)

---

### Full Command with All Components
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail,Sports | location=United States,Canada | seniority=Founder,C-Suite,VP | our-company-details="We sell premium golf equipment and accessories for golf enthusiasts" | verified-email=true
```

---

## Command Structure Rules

### Filter Separator
- Use `|` (pipe) or space to separate filters
- Both work: `keywords=golf | industry=Retail` or `keywords=golf industry=Retail`

### Value Separator
- Use `,` (comma) to separate multiple values within a filter
- Example: `keywords=golf retailers, pro shops`

### Quoting Values
- Use quotes for values with spaces: `our-company-details="We sell golf equipment"`
- Single values don't need quotes: `keywords=golf retailers`
- Multiple comma-separated values don't need quotes: `keywords=golf retailers,pro shops`

---

## What's Required vs Optional

### **REQUIRED:**
1. **`keywords=`** - Must have at least one keyword for Check #2 to run
   - Without it, only wholesale partner check runs (no keyword filtering)

### **HIGHLY RECOMMENDED:**
2. **`industry=`** - Narrow Prospeo search
3. **`location=`** - Narrow Prospeo search
4. **`seniority=`** - Get decision-makers
5. **`our-company-details=`** - Better AI qualification

### **OPTIONAL:**
6. **`verified-email=`** - Quality filter (defaults to false)

---

## What Happens When Components Are Excluded

### Scenario 1: Only Keywords Provided
```
/lead-magnet keywords=golf retailers
```
**Result:**
- ✅ Prospeo: Very broad search (all industries, locations, seniorities)
- ✅ Check #1: Runs (wholesale partner check)
- ✅ Check #2: Runs (keyword match)
- ⚠️ Many irrelevant companies processed
- ⚠️ Higher cost/time

---

### Scenario 2: No Keywords Provided
```
/lead-magnet industry=Retail | location=United States
```
**Result:**
- ✅ Prospeo: Narrow search (Retail industry, US location)
- ✅ Check #1: Runs (wholesale partner check)
- ❌ Check #2: SKIPPED (no keywords to match)
- ⚠️ ALL multi-brand retailers qualify (no keyword filtering)
- ⚠️ Very broad qualification

---

### Scenario 3: Only Industry Provided
```
/lead-magnet industry=Retail
```
**Result:**
- ✅ Prospeo: Narrow search (Retail industry only)
- ✅ Check #1: Runs (wholesale partner check)
- ❌ Check #2: SKIPPED (no keywords)
- ⚠️ All retail multi-brand retailers qualify
- ⚠️ No keyword filtering

---

## Best Practices

### ✅ DO:
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail | location=United States | seniority=Founder | our-company-details="We sell golf equipment" | verified-email=true
```

### ❌ DON'T:
```
/lead-magnet industry=Retail  # No keywords = no keyword filtering
/lead-magnet keywords=golf retailers  # Too broad = processes many irrelevant companies
```

---

## Summary Table

| Component | Required | Purpose | What If Excluded |
|-----------|----------|---------|------------------|
| `keywords=` | ✅ YES | AI keyword match | Check #2 skipped |
| `our-company-details=` | ⚠️ Recommended | AI context | Uses default generic description |
| `industry=` | ⚠️ Recommended | Narrow Prospeo search | Searches all industries |
| `location=` | ⚠️ Recommended | Narrow Prospeo search | Searches all locations |
| `seniority=` | ⚠️ Recommended | Get decision-makers | Gets all seniority levels |
| `verified-email=` | ❌ Optional | Quality filter | Defaults to false (includes unverified) |

---

## Quick Reference

**Minimum viable command:**
```
/lead-magnet keywords=<your keywords>
```

**Recommended command:**
```
/lead-magnet keywords=<keywords> | industry=<industry> | location=<location> | seniority=<seniority> | our-company-details="<description>" | verified-email=true
```
