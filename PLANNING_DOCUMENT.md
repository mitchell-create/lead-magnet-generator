# Lead Magnet Generator - Planning & Architecture Document

## 1. Prospeo Search Criteria Options

### Available Prospeo API Filters (search-person endpoint)

#### Company Filters
- **`company_industry`** - Include/exclude industries
  - Format: `{"include": ["SaaS", "Financial Services"]}` or `{"exclude": ["Industry"]}`
- **`company_location`** - Geographic filtering
  - Format: `{"include": ["California, United States", "New York, United States"]}`
  - ⚠️ **Must match exact strings from Prospeo dashboard** (e.g., "California, United States" not "CA")
- **`company_technology`** - Tech stack filtering
  - Format: `{"include": ["Stripe", "AWS", "Shopify"]}`
- **`company_funding`** - Funding stage/date filtering
  - Format: `{"stage": {"include": ["Series A", "Seed"]}, "date": {"max": 180}}` (days ago)
- **`employee_range`** - Company size by employees
  - Format: `{"min": 50, "max": 500}`
- **`company.websites`** or **`company.names`** - Specific company lists
  - Format: `{"include": ["company1.com", "company2.com"]}` (max ~500 entries)
- **`company_email_provider`** - Filter by email provider
- **`company_naics`** / **`company_sics`** - Industry codes

#### Person Filters
- **`person_seniority`** - Job seniority level
  - Format: `{"include": ["Founder/Owner", "C-Suite", "VP", "Director"]}`
- **`person_year_of_experience`** - Experience level
  - Format: `{"min": 5, "max": 30}`
- **`person_departments`** - Department filtering
  - Format: `{"include": ["Sales", "Marketing", "Product"]}`
- **`person_location`** - Person's location
  - Format: `{"include": ["California, United States"]}` (exact strings required)

#### Other Options
- **`keywords`** - Keyword search (what we currently use)
- **`only_verified_email`** - Boolean, only return leads with verified emails

---

## 2. Recommended Slack Command Structure

### Option A: Detailed Structured Format (Recommended)
```
/lead-magnet Search: industry=SaaS | seniority=Founder,C-Suite | location=California | size=50-500 | verified-email=true
```

### Option B: Natural Language Format
```
/lead-magnet Find founders at SaaS companies in California with 50-500 employees
```

### Option C: Simple Keyword-Based (Current)
```
/lead-magnet Target: SaaS companies | Criteria: Size>50, Industry=Technology
```

### **Recommended: Hybrid Approach**

**Format:**
```
/lead-magnet [Search Filters] | [AI Qualification Criteria]
```

**Examples:**

1. **Basic:**
   ```
   /lead-magnet industry=SaaS | size>50, seniority=Founder
   ```

2. **Detailed:**
   ```
   /lead-magnet industry=SaaS,Software | location=California,New York | seniority=Founder,C-Suite,VP | size=50-500 | verified-email=true | tech=Stripe,AWS
   ```

3. **For Instantly Integration (auto-generated):**
   ```
   /lead-magnet keywords=golf course pro shops,golf retailers stores | size>10
   ```

**How it maps:**
- **Before `|`** = Prospeo search filters (what to fetch)
- **After `|`** = AI qualification criteria (how to filter fetched leads)

---

## 3. Supabase Row Structure

### Current Schema (from `supabase_schema.sql`)

```sql
CREATE TABLE lead_magnet_candidates (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP,
    
    -- Person Data (from Prospeo)
    person_id TEXT,
    person_name TEXT,
    person_email TEXT,
    person_title TEXT,
    person_linkedin_url TEXT,
    
    -- Company Data
    company_id TEXT,
    company_name TEXT,
    company_description TEXT,
    company_domain TEXT,
    company_website TEXT,
    company_industry TEXT,
    company_size TEXT,
    company_location TEXT,
    
    -- Qualification Metadata
    qualified_at TIMESTAMP,
    qualification_criteria TEXT,  -- JSON
    search_criteria TEXT,
    prospeo_page_number INTEGER,
    processing_order INTEGER,
    
    -- Slack Metadata
    slack_user_id TEXT,
    slack_channel_id TEXT,
    slack_trigger_id TEXT,
    
    -- Full JSON (for flexibility)
    raw_prospeo_data JSONB,
    openrouter_response TEXT
);
```

### Recommended Additions for Instantly Integration

```sql
-- Add these columns:
instantly_campaign_id TEXT,           -- Which Instantly campaign triggered this
instantly_reply_id TEXT,              -- The positive reply ID from Instantly
instantly_company_name TEXT,          -- Original company that replied
instantly_contact_email TEXT,         -- Contact who replied
instantly_dynamic_variables JSONB,    -- All dynamic vars from the reply
instantly_good_fit_companies TEXT,    -- The {{good fit companies}} value
trigger_source TEXT,                  -- 'slack_manual', 'instantly_webhook', etc.
```

---

## 4. Instantly Integration Workflow

### Architecture Overview

```
Instantly Positive Reply 
  → Instantly Webhook (Railway endpoint)
  → Parse {{good fit companies}} variable
  → Format as Prospeo search
  → Trigger lead search
  → Save to Supabase with Instantly metadata
  → Send notification to Slack
```

### Step-by-Step Flow

1. **Instantly sends webhook** to Railway endpoint when positive reply received
   - Webhook URL: `https://lead-magnet-generator-production.up.railway.app/instantly/webhook`
   - Payload includes: campaign info, contact info, dynamic variables

2. **Parse webhook payload:**
   - Extract `{{good fit companies}}` value (e.g., "golf course pro shops, golf retailers stores")
   - Extract original company info (who replied)
   - Extract campaign ID

3. **Convert to Prospeo search:**
   - Split `{{good fit companies}}` by comma
   - Format as Prospeo `keywords` filter
   - Add default qualification criteria (or from campaign config)

4. **Trigger lead search:**
   - Use existing `process_lead_search()` function
   - Pass Instantly metadata

5. **Save with Instantly metadata:**
   - Link leads back to original Instantly campaign
   - Track which company triggered the search
   - Store dynamic variables for reference

### Example Instantly Webhook Payload (Estimated)

```json
{
  "event": "reply_positive",
  "campaign_id": "abc123",
  "campaign_name": "Wholesale Outreach",
  "contact": {
    "email": "contact@company.com",
    "name": "John Doe"
  },
  "company": {
    "name": "Golf Hat Co",
    "domain": "golfhatco.com"
  },
  "dynamic_variables": {
    "good_fit_companies": "golf course pro shops, golf retailers stores",
    "contact_name": "John",
    "company_name": "Golf Hat Co"
  },
  "reply_content": "...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### New Files Needed

1. **`instantly_webhook_handler.py`** - Handles Instantly webhooks
2. **`instantly_parser.py`** - Parses Instantly payloads and converts to search format
3. **Database migration** - Add Instantly columns to Supabase

---

## 5. Decisions Needed

### Prospeo Filters - Which to Support?

**Must Have:**
- [ ] `keywords` (current) - ✅ Already supported
- [ ] `company_industry` - Most important for targeting
- [ ] `employee_range` (company size) - Critical for qualification
- [ ] `person_seniority` - For decision-maker targeting

**Should Have:**
- [ ] `company_location` - Geographic targeting
- [ ] `only_verified_email` - Quality filtering
- [ ] `person_departments` - Role-based targeting

**Nice to Have:**
- [ ] `company_technology` - Tech stack matching
- [ ] `company_funding` - Growth stage targeting
- [ ] `person_year_of_experience` - Seniority verification

**Recommendation:** Start with Must Have + Should Have (7 filters total)

---

### Slack Command Format - Which Style?

**Recommendation: Hybrid (Option C enhanced)**

```
/lead-magnet [prospeo-filters] | [ai-qualification]
```

**Example:**
```
/lead-magnet industry=SaaS | size>50, seniority=Founder
```

**Pros:**
- Clear separation of search vs qualification
- Flexible (can omit either part)
- Easy to auto-generate from Instantly
- Backwards compatible with current format

---

### Supabase Schema - Add Instantly Columns?

**Recommendation: YES**

Add the columns listed in Section 3 to track:
- Which Instantly campaign triggered the search
- Original company that replied
- Dynamic variables used
- Link back to Instantly for reporting

---

## 6. Implementation Priority

### Phase 1: Current System Fixes
1. ✅ Fix Prospeo filter format (done)
2. ✅ Update to use valid Prospeo filters
3. 📝 Decide on final Slack command format
4. 📝 Update parser for new format

### Phase 2: Prospeo Filter Enhancement
1. 📝 Add support for structured filters (industry, seniority, etc.)
2. 📝 Update `build_prospeo_filters()` to handle new filters
3. 📝 Test with various filter combinations

### Phase 3: Instantly Integration
1. 📝 Create Instantly webhook endpoint
2. 📝 Add Instantly columns to Supabase
3. 📝 Parse Instantly dynamic variables
4. 📝 Auto-trigger lead searches
5. 📝 Add Instantly metadata to saved leads

---

## Next Steps

**Please decide:**

1. **Which Prospeo filters** do you want to support? (from Section 5)
2. **Which Slack command format** do you prefer? (from Section 2)
3. **Do we add Instantly columns** to Supabase? (yes/no)
4. **Instantly webhook details:**
   - Do you have Instantly API docs/webhook format?
   - What's your Instantly API key (if needed)?
   - What's the webhook URL format Instantly expects?

Once you decide, I'll implement!
