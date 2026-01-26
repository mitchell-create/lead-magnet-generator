# Seniority Filter - How It Works

## ✅ You DO Provide Seniority in Your Slack Command!

You include it in your Slack command just like before:

```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder/Owner,C-Suite | our-company-details="We sell premium golf equipment"
```

---

## 🔄 What Happens Behind the Scenes

### Step 1: Slack Command Parsing
- Your command is parsed
- `seniority=Founder/Owner,C-Suite` is extracted
- Stored in `parsed_input['prospeo_filters']['person_seniority']`

### Step 2: Company Discovery (Phase 1)
- **Seniority filter is EXCLUDED** from initial company search
- Only company-level filters are used: `industry`, `location`, etc.
- This searches for companies (not persons with specific seniority)

### Step 3: Company Qualification (Phase 2)
- AI qualifies companies based on wholesale partner type + keyword match
- Seniority is NOT involved in this step

### Step 4: Person Search at Qualified Companies (Phase 3)
- **Seniority filter is NOW USED** ✅
- For each qualified company, the system searches for persons
- Uses `seniority=Founder/Owner,C-Suite` filter
- Finds ALL persons at that company matching the seniority criteria

### Step 5: Email Enrichment (Phase 4)
- Enriches emails for all persons found in Phase 4

---

## 📝 Example Flow

**Your Slack Command:**
```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder/Owner,C-Suite
```

**What Happens:**

1. **Initial Search** (no seniority):
   - Searches: `company_industry=Retail`
   - Returns: Persons from retail companies
   - Extracts: 50 unique retail companies

2. **AI Qualification**:
   - Qualifies: 10 golf retailers

3. **Person Search** (WITH seniority):
   - For each of 10 qualified companies:
   - Searches: Persons at that company with `person_seniority=Founder/Owner,C-Suite`
   - Finds: 2-3 founders/executives per company = 25 persons total

4. **Email Enrichment**:
   - Enriches all 25 persons
   - Gets verified emails for 20 persons

**Result:** 20 qualified leads (founders/executives at golf retailers)

---

## ✅ Summary

- **You provide seniority in Slack command:** ✅ Yes, same as before
- **It's used for company discovery:** ❌ No (excluded)
- **It's used for person search:** ✅ Yes (at qualified companies)
- **Where is it stored:** In `parsed_input['prospeo_filters']['person_seniority']`
- **How it's extracted:** Using `extract_person_seniority_filter(parsed_input)`

---

## 🔍 Code Reference

### Where Seniority is Extracted:
```python
# In layer4_lead_processor.py
seniority_filter = extract_person_seniority_filter(parsed_input)
```

### Where Seniority is Used:
```python
# When searching persons at qualified companies
persons_result = self.prospeo_client.fetch_persons_at_company(
    company_id=company_id,
    additional_filters=seniority_filter  # <-- Used here!
)
```

### Where Seniority is Excluded:
```python
# In main.py
prospeo_filters = build_prospeo_filters(parsed_input, include_seniority=False)
#                                                                        ^^^^ 
#                                                             Excludes seniority from Phase 1
```

---

## ❓ What If You Don't Provide Seniority?

If you don't include `seniority=` in your Slack command:
- Phase 1: Company discovery still works (no seniority filter)
- Phase 2: Company qualification still works
- Phase 3: Person search will find **ALL persons** at qualified companies (no seniority filter)
- Result: More leads, but may include lower-level contacts

**Recommendation:** Always include seniority to target decision-makers!
