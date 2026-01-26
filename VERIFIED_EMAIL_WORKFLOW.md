# Verified Email Workflow - Updated Plan

## Your New Workflow

1. **Pull company list** (no emails) from Prospeo
2. **AI qualify companies** (OpenRouter checks if they're a good fit)
3. **THEN get emails** for qualified companies only

---

## Is `verified-email` Necessary in Slack Command?

### ❌ **NO - Not Necessary for Your Workflow**

**Why:**
- `verified-email=true` is a **Prospeo search filter** that filters the initial search results
- It only returns persons who already have verified emails in the search results
- But you're doing **company-first approach** - you don't need emails in the initial search!

**What `verified-email` does:**
- Filters Prospeo search to only return persons with verified emails
- This is for the **initial search**, not for enrichment later

**For your workflow:**
- You want to search for companies WITHOUT filtering by email
- Then qualify them with AI
- Then enrich ONLY qualified companies with emails

---

## Current System Status

### ✅ What Works:
- Pulls company list from Prospeo (no email filter needed)
- AI qualifies companies
- Saves all companies to Supabase
- Updates qualification status

### ❌ What's Missing:
- **Automatic email enrichment for qualified companies**
- The system does NOT automatically get emails for qualified companies
- You'll need to add this step

---

## What Happens If You Don't Include `verified-email`

### If you exclude `verified-email`:
```
/lead-magnet keywords=golf retailers | industry=Retail
```

**Result:**
- ✅ Prospeo search returns companies (with or without emails)
- ✅ AI qualifies companies
- ✅ Qualified companies saved to Supabase
- ❌ **Emails are NOT automatically enriched** (you need to add this step)

---

## Recommended Slack Command (Without verified-email)

```
/lead-magnet keywords=golf retailers, pro shops | industry=Retail | location=United States | seniority=Founder | our-company-details="We sell golf equipment"
```

**Why no `verified-email`:**
- You're searching for companies, not filtering by email
- You'll enrich emails AFTER qualification
- Saves Prospeo credits (don't filter out companies without emails yet)

---

## Adding Email Enrichment Step

You'll need to add a step to enrich qualified companies with emails. Options:

### Option 1: Prospeo Enrich Person API
After qualification, for each qualified company:
```python
# Enrich person to get email
enriched_person = prospeo_client.enrich_person(person_id)
email = enriched_person.get('email')
```

### Option 2: Separate Enrichment Process
1. Query Supabase for `is_qualified = TRUE`
2. For each qualified company, call Prospeo enrich API
3. Update Supabase with email

### Option 3: Manual Export
1. Export qualified companies from Supabase
2. Use Prospeo UI or API to enrich in bulk
3. Import emails back to Supabase

---

## Summary

### ✅ **You DON'T need `verified-email` in Slack command**
- It's a search filter, not needed for company-first approach
- You'll enrich emails AFTER qualification

### ⚠️ **System does NOT automatically enrich emails**
- You need to add email enrichment step for qualified companies
- Can use Prospeo enrich API or separate process

### 📝 **Recommended Command:**
```
/lead-magnet keywords=<keywords> | industry=<industry> | location=<location> | seniority=<seniority> | our-company-details="<description>"
```

**No `verified-email` needed!**
