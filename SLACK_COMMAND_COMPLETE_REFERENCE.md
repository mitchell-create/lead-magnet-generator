# Slack Command - Complete Reference Guide

## Command Template

```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```

---

## Component Breakdown

### 1. **`keywords=`** - REQUIRED ✅

**Purpose:** Keywords for AI keyword match check (Check #2)

**Format:**
```
keywords=keyword1,keyword2,keyword3
```

**Examples:**
```
keywords=golf retailers
keywords=golf retailers, pro shops
keywords=athletic wear, sportswear retailers
keywords=IT resellers, tech distributors
```

**What happens if excluded:**
- ❌ Check #2 (Keyword Match) is skipped
- ⚠️ Only wholesale partner check runs
- ⚠️ No keyword filtering

**Required:** YES

---

### 2. **`industry=`** - RECOMMENDED ⚠️

**Purpose:** Filter companies by industry in Prospeo search

**Format:**
```
industry=Industry1,Industry2
```

**Examples:**
```
industry=Retail
industry=Retail,Sports
industry=Technology,Software
industry=Healthcare,Medical
```

**What happens if excluded:**
- ⚠️ Searches ALL industries
- ⚠️ Very broad results
- ⚠️ More irrelevant companies processed

**Required:** NO (but highly recommended)

**See:** `PROSPEO_INDUSTRIES.md` for complete industry list

---

### 3. **`location=`** - RECOMMENDED ⚠️

**Purpose:** Filter companies by location

**Format:**
```
location=Location1,Location2
```

**Examples:**
```
location=United States
location=California,New York
location=United States,Canada
location=Europe
```

**What happens if excluded:**
- ⚠️ Searches ALL locations worldwide
- ⚠️ International companies included
- ⚠️ More processing time/cost

**Required:** NO (but recommended)

---

### 4. **`seniority=`** - RECOMMENDED ⚠️

**Purpose:** Filter persons by seniority level

**Format:**
```
seniority=Level1,Level2
```

**Examples:**
```
seniority=Founder
seniority=Founder,C-Suite
seniority=Founder,C-Suite,VP
seniority=Director,Manager
```

**What happens if excluded:**
- ⚠️ Gets ALL seniority levels
- ⚠️ Includes juniors, assistants, entry-level
- ⚠️ Lower quality for decision-makers

**Required:** NO (but highly recommended)

**See:** `PROSPEO_SENIORITY_LEVELS.md` for complete list with descriptions

**Available Values (from Prospeo dashboard):**
- `Founder/Owner` - Company founders/business owners
- `C-Suite` - C-level executives
- `Partner` - Business partners
- `Vice President` - VP level
- `Head` - Head of department/function
- `Director` - Director level
- `Manager` - Manager level
- `Senior` - Senior individual contributor
- `Intern` - Intern positions (usually NOT for B2B)
- `Entry` - Entry-level positions (usually NOT for B2B)

---

### 5. **`our-company-details=`** - RECOMMENDED ⚠️

**Purpose:** Your company description for AI context

**Format:**
```
our-company-details="Your description here"
```

**Examples:**
```
our-company-details="We sell premium golf equipment and accessories"
our-company-details="We are a B2B technology reseller specializing in enterprise software"
our-company-details="We sell athletic clothing and sportswear"
```

**What happens if excluded:**
- ✅ Uses default: "Multi-brand retailer/reseller looking for partners to stock our products"
- ⚠️ Less context for AI
- ⚠️ May be less accurate

**Required:** NO (but recommended for better results)

---

## Complete Examples

### Example 1: Golf Equipment
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail,Sports | location=United States | seniority=Founder,C-Suite | our-company-details="We sell premium golf equipment and accessories"
```

### Example 2: Athletic Clothing
```
/lead-magnet keywords=athletic wear, sportswear retailers | industry=Retail,Fashion | location=United States,Canada | seniority=Founder,C-Suite,VP | our-company-details="We sell premium athletic clothing and sportswear"
```

### Example 3: Tech Resellers
```
/lead-magnet keywords=IT resellers, tech distributors | industry=Technology | location=United States | seniority=Founder,C-Suite,VP,Director | our-company-details="We are a B2B technology reseller specializing in enterprise software solutions"
```

---

## Minimum vs Recommended

### **Minimum (Keywords Only):**
```
/lead-magnet keywords={{keywords}}
```
- ✅ Will work, but very broad
- ⚠️ Processes many irrelevant companies

### **Recommended:**
```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```
- ✅ Narrow, focused search
- ✅ Higher quality leads
- ✅ Better AI qualification

---

## Notes

### Email Enrichment
- ❌ **NO `verified-email` parameter needed**
- ✅ Emails automatically enriched AFTER qualification
- ✅ Only qualified companies get email enrichment
- ✅ Saves money by not enriching unqualified companies

### Separators
- Use `|` (pipe) or space to separate filters
- Use `,` (comma) to separate multiple values within a filter

### Quoting
- Use quotes for values with spaces: `our-company-details="We sell golf equipment"`
- No quotes needed for single words: `keywords=golf retailers`
- No quotes needed for comma-separated: `industry=Retail,Sports`

### Order
- Order doesn't matter - all equivalent:
  - `keywords=golf | industry=Retail`
  - `industry=Retail | keywords=golf`

---

## Quick Reference

| Component | Required? | Purpose | Example |
|-----------|-----------|---------|---------|
| `keywords=` | ✅ YES | AI keyword match | `keywords=golf retailers` |
| `industry=` | ⚠️ Recommended | Narrow Prospeo search | `industry=Retail` |
| `location=` | ⚠️ Recommended | Narrow Prospeo search | `location=United States` |
| `seniority=` | ⚠️ Recommended | Get decision-makers | `seniority=Founder,C-Suite` |
| `our-company-details=` | ⚠️ Recommended | Better AI context | `our-company-details="We sell..."` |

---

## Related Documentation

- **SLACK_COMMAND_TEMPLATE.md** - Template and examples
- **PROSPEO_INDUSTRIES.md** - Complete industry list
- **PROSPEO_SENIORITY_LEVELS.md** - Seniority levels with descriptions
- **VERIFIED_EMAIL_WORKFLOW.md** - Email enrichment details
