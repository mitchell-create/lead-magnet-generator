# Slack Command Template & Reference

## Command Template

```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```

---

## Complete Command with All Components

### Full Template:
```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```

### Real Example:
```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail,Sports | location=United States | seniority=Founder,C-Suite | our-company-details="We sell premium golf equipment and accessories"
```

---

## Component Details

### 1. **`keywords=`** - REQUIRED
**Purpose:** Keywords for AI keyword match check (Check #2)

**Format:** `keywords=keyword1,keyword2,keyword3`

**Example:**
- `keywords=golf retailers`
- `keywords=golf retailers, pro shops`
- `keywords=athletic wear, sportswear retailers`

**If excluded:** Check #2 (Keyword Match) is skipped ❌

---

### 2. **`industry=`** - RECOMMENDED
**Purpose:** Filter companies by industry in Prospeo search

**Format:** `industry=Industry1,Industry2`

**Example:**
- `industry=Retail`
- `industry=Retail,Sports`
- `industry=Technology,Software`

**If excluded:** Searches ALL industries (very broad)

---

### 3. **`location=`** - RECOMMENDED
**Purpose:** Filter companies by location

**Format:** `location=Location1,Location2`

**Example:**
- `location=United States`
- `location=California,New York`
- `location=United States,Canada`

**If excluded:** Searches ALL locations worldwide

---

### 4. **`seniority=`** - RECOMMENDED
**Purpose:** Filter persons by seniority level

**Format:** `seniority=Level1,Level2`

**Example:**
- `seniority=Founder`
- `seniority=Founder,C-Suite`
- `seniority=Founder,C-Suite,VP`

**If excluded:** Gets all seniority levels (including juniors)

---

### 5. **`our-company-details=`** - RECOMMENDED
**Purpose:** Your company description for AI context

**Format:** `our-company-details="Your description"`

**Example:**
- `our-company-details="We sell premium golf equipment and accessories"`
- `our-company-details="We are a B2B technology reseller specializing in enterprise software"`

**If excluded:** Uses generic default description

---

## Component Order

Order doesn't matter! All of these are equivalent:

```
/lead-magnet keywords=golf retailers | industry=Retail | location=United States
/lead-magnet industry=Retail | keywords=golf retailers | location=United States
/lead-magnet location=United States | keywords=golf retailers | industry=Retail
```

---

## Minimum Command

**Absolute minimum (keywords only):**
```
/lead-magnet keywords={{keywords}}
```

**Recommended minimum:**
```
/lead-magnet keywords={{keywords}} | industry={{industry}}
```

**Best practice (includes all recommended components):**
```
/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"
```

---

## Notes

### Email Enrichment
- ❌ **NO `verified-email` parameter needed**
- ✅ Emails are automatically enriched AFTER qualification
- ✅ Only qualified companies get email enrichment (saves money!)

### Quoting
- Use quotes for values with spaces: `our-company-details="We sell golf equipment"`
- No quotes needed for single words: `keywords=golf retailers`
- No quotes needed for comma-separated values: `industry=Retail,Sports`

### Separators
- Use `|` (pipe) or space to separate filters
- Use `,` (comma) to separate multiple values within a filter
