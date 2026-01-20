# Wholesale Partner Qualification Setup

## ✅ Updates Made

### 1. New Qualification Prompt
- Replaced generic qualification with your **wholesale partner** qualification prompt
- Focuses on identifying multi-brand retailers vs manufacturers
- Includes all your examples and investigation steps

### 2. Model Updated
- Changed to use `gpt-oss-20b` (via `OPENROUTER_MODEL` environment variable)
- **Action Required**: Set `OPENROUTER_MODEL` in Railway Variables to exact model name

### 3. Data Extraction
- Uses company website and LinkedIn from Prospeo data
- Includes company description and industry
- Passes all relevant info to AI for analysis

---

## ⚠️ Important: Prospeo Data Limitations

### What Prospeo Provides:
✅ Company name  
✅ Company description  
✅ Company domain/website URL  
✅ Company industry  
✅ Person LinkedIn (may indicate company)  

### What Prospeo Does NOT Provide:
❌ Actual website HTML content  
❌ Scraped navigation menus  
❌ Product listings  
❌ Brand filter dropdowns  
❌ FAQ pages  

---

## 🔍 How It Works Now

### Current Flow:
1. Fetch lead from Prospeo (includes company domain/website)
2. Extract company website URL and LinkedIn
3. Send to AI with your prompt:
   - Company Website URL
   - Company LinkedIn URL
   - Company Name
   - Company Description
4. AI analyzes based on:
   - Company description (may mention brands/products)
   - URL references (if AI has knowledge)
   - Patterns in company name/industry

### Limitation:
**The AI prompt is designed to analyze website content** (navigation, product pages, etc.), but we're only providing:
- Company description (from Prospeo)
- Website URL (for reference)

**The AI may need to rely heavily on the description** if it can't access the actual website.

---

## 💡 Recommendation: Add Web Scraping

For **best results**, consider adding web scraping to actually fetch:
- Website navigation/menu items
- Product listing pages
- Brand mentions
- FAQ content

This would enable the AI to perform the detailed analysis your prompt describes.

### Options:
1. **ScrapingBee API** - Simple scraping service
2. **ScraperAPI** - Another scraping service
3. **BeautifulSoup** - Python library (may need proxies)
4. **Browser-based AI** - Models that can access websites directly

---

## 🚀 Setup Steps

### Step 1: Set OpenRouter Model in Railway

1. Go to Railway Dashboard → Your Service → **Variables**
2. Add or update:
   - **Key**: `OPENROUTER_MODEL`
   - **Value**: `gpt-oss-20b` (or exact model name from OpenRouter)

**To find exact model name:**
- Check OpenRouter docs: https://openrouter.ai/models
- Or use their model list endpoint

### Step 2: Verify Prospeo Data

The code expects Prospeo to return:
- `company.website` or `company.domain`
- `company.description`
- `person.linkedin_url` (for company LinkedIn)

**If Prospeo uses different field names**, we may need to update `extract_person_and_company_data()` in `utils.py`.

### Step 3: Test

Run a test search:
```
/lead-magnet keywords=golf retailers | seniority=Founder
```

Check Railway logs to see:
- What company data is being extracted
- What's being sent to AI
- AI qualification results

---

## 📝 Model Name Note

If `gpt-oss-20b` isn't the exact OpenRouter model name, you may need to:
1. Check OpenRouter's model list: https://openrouter.ai/models
2. Use the exact format (e.g., `openrouter/gpt-o1` or similar)
3. Update the `OPENROUTER_MODEL` variable in Railway

---

## 🔄 Future Enhancements

1. **Add web scraping** to fetch actual website content
2. **Cache scraped content** in Supabase for faster re-qualification
3. **Manual review queue** for uncertain cases
4. **Batch qualification** using scraped content

---

## ✅ What's Ready Now

- ✅ Wholesale partner qualification prompt integrated
- ✅ Company website/LinkedIn URLs included
- ✅ Model configurable via environment variable
- ⚠️ Limited to Prospeo description data (not full website scraping)

The system will work, but for **maximum accuracy**, consider adding website scraping! 🚀
