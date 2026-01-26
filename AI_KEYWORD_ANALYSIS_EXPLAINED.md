# AI Keyword Analysis - How It Works

## ✅ Using OpenRouter for AI Qualification

### Technology Stack
- **API:** OpenRouter API
- **Model:** Configurable via `OPENROUTER_MODEL` (default: set to your preferred model)
- **Prompt:** Wholesale partner qualification prompt
- **Website Scraping:** BeautifulSoup to get actual website content

---

## How Keywords Are Used for AI Analysis

### 1. Keywords Extracted from Slack Input
When you send: `/lead-magnet keywords=golf retailers | industry=Retail`

**What happens:**
- Keywords: `golf retailers` → Stored for AI
- Industry: `Retail` → Sent to Prospeo API

### 2. Prospeo Search (Without Keywords)
- Prospeo searches using: `industry=Retail`
- Returns companies matching that industry
- Keywords are NOT sent to Prospeo (they don't support it)

### 3. AI Qualification (With Keywords)
For each lead from Prospeo:

**Step A: Website Scraping**
- Scrapes company website
- Extracts: navigation, footer, product listings, brand indicators

**Step B: AI Analysis via OpenRouter**
- Sends to AI:
  - Company website URL
  - Scraped website content
  - Company description
  - **Keywords: "golf retailers"**
  - Qualification criteria

**Step C: AI Prompt**
The AI receives your wholesale partner prompt PLUS:
- "Target Companies/Industries: golf retailers"
- Scraped website content
- Company information

**Step D: AI Response**
- AI analyzes: "Is this company a multi-brand retailer who would stock golf-related products?"
- Returns: YES or NO

---

## Example Flow

**Input:**
```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder
```

**Process:**

1. **Prospeo Search:**
   - Filters: `industry=Retail`, `seniority=Founder`
   - Gets 100 leads from Prospeo

2. **For Each Lead:**
   - Save to Supabase (is_qualified = FALSE)
   - Scrape company website
   - Send to OpenRouter AI:
     ```
     "Target Companies/Industries: golf retailers"
     "Company Website: https://example.com"
     [Scraped content with navigation, products, etc.]
     ```
   - AI analyzes: "Is this a retailer who could stock golf products?"
   - AI responds: YES or NO

3. **Update Qualification:**
   - If YES → Update Supabase: is_qualified = TRUE
   - If NO → Keep is_qualified = FALSE

---

## What the AI Sees

The AI receives:
- ✅ Company website (URL)
- ✅ Scraped website content (navigation, products, brands)
- ✅ Company description from Prospeo
- ✅ **Your keywords** ("golf retailers")
- ✅ Qualification criteria (seniority, size, etc.)
- ✅ Your wholesale partner qualification prompt

The AI uses all of this to determine if the company is a good fit!

---

## OpenRouter Configuration

**Current Setup:**
- Model: Configurable via `OPENROUTER_MODEL` env var
- Default: Set to your preferred model
- Temperature: 0.0 (deterministic)
- Max tokens: 5 (just YES/NO)

**You can change the model** by setting `OPENROUTER_MODEL` in Railway Variables.

---

## Summary

✅ **OpenRouter is used** for AI keyword analysis  
✅ **Keywords are passed to AI** via `target_companies` parameter  
✅ **Website scraping** provides actual content for analysis  
✅ **AI uses keywords** to qualify leads based on company info  

The whole system works together: Prospeo finds leads → AI qualifies them using keywords!
