# Final Specifications

## ✅ Prospeo Filters (Selected)

### Company Filters
- `company_industry` - Multiple industries supported (comma-separated)
- `company_location` - Multiple locations supported (comma-separated)
- `only_verified_email` - Boolean (true/false)

### Person Filters
- `person_seniority` - Multiple seniority levels (comma-separated)
- `person_location` - Multiple locations supported (comma-separated)

### General
- `keywords` - Multiple keywords supported (comma-separated)

---

## 📝 Slack Command Format

### New Format (Supports Multiple Values)

```
/lead-magnet [filters] | [ai-qualification-criteria]
```

### Filter Format

Each filter: `filter_name=value1,value2,value3`

**Available Filters:**
- `industry=` - Company industries (comma-separated)
- `location=` - Company/person locations (comma-separated)
- `seniority=` - Person seniority levels (comma-separated)
- `keywords=` - Keywords (comma-separated)
- `verified-email=` - Boolean (true/false)

### Examples

**Simple:**
```
/lead-magnet industry=SaaS,Software | size>50
```

**Multiple values:**
```
/lead-magnet industry=SaaS,Fintech,E-commerce | location=California,New York | seniority=Founder,C-Suite,VP | verified-email=true
```

**With keywords:**
```
/lead-magnet keywords=golf course pro shops,golf retailers stores | size>10
```

**Multiple keywords + seniority:**
```
/lead-magnet keywords=wholesale,retail,distribution | seniority=Founder,Owner,C-Suite | location=United States
```

---

## ⚠️ Job Title Support

**Note:** Prospeo API uses `person_seniority` for seniority levels (Founder, C-Suite, VP, Director, etc.) but **does NOT have a specific job title filter**.

**Workaround Options:**

1. **Use Keywords** - Search for specific job titles via keywords:
   ```
   /lead-magnet keywords=CEO,Chief Executive Officer | seniority=C-Suite
   ```

2. **Use Seniority + Keywords Combination** - Filter by seniority first, then keywords:
   ```
   /lead-magnet seniority=C-Suite | keywords=CEO,President
   ```

3. **AI Qualification** - Use Prospeo to get seniority, then AI to filter by specific titles:
   ```
   /lead-magnet seniority=C-Suite | title=CEO,President (AI qualification)
   ```

**Recommendation:** Use option 1 or 2 for now. We can add title filtering in the AI qualification step.

---

## 🗄️ Supabase Schema

**Current schema is good** - no Instantly columns needed for now.

Only saving Prospeo contacts (not Instantly contacts).

---

## 📋 Implementation Plan

1. ✅ Update Slack command parser to handle new format
2. ✅ Support multiple values (comma-separated) for all filters
3. ✅ Update `build_prospeo_filters()` to format correctly
4. ✅ Map Slack filter names to Prospeo API filter names
5. ✅ Handle job titles via keywords (since Prospeo doesn't support title filter)

---

## 🚀 Next Steps

1. Implement new parser
2. Update filter builder
3. Test with multiple values
4. Test job title searches via keywords
