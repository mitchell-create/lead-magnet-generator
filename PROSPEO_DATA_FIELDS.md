# Prospeo Data Fields - What We Get

## Available Company Data from Prospeo

Based on the code structure, Prospeo API returns company data that includes:

### Standard Fields We're Using:
- `company.name` - Company name
- `company.description` - Company description
- `company.domain` - Company domain (e.g., "acme.com")
- `company.website` - Full website URL (if available)
- `company.industry` - Industry classification
- `company.size` - Company size
- `company.location` - Geographic location
- `company.id` - Company ID

### Person/LinkedIn Fields:
- `person.linkedin_url` - Person's LinkedIn profile URL
- `person.name` - Person's name
- `person.title` - Person's job title
- `person.email` - Person's email

---

## ⚠️ Website and LinkedIn URLs

### What Prospeo Provides:
- ✅ **Company Domain**: Usually available (e.g., "acme.com")
- ✅ **Company Website**: May be available as full URL
- ⚠️ **Company LinkedIn**: May or may not be directly in company data
- ✅ **Person LinkedIn**: Available from person record

### Our Solution:
1. **Company Website**: Use `company.website` if available, otherwise construct from `company.domain`
2. **Company LinkedIn**: 
   - Try to get from `company.linkedin_url` if available
   - Or derive from person's LinkedIn (replace `/in/` with `/company/`)
   - Note: This may not always be accurate

---

## 🔍 What We Can Analyze

### From Prospeo Data Directly:
- Company name
- Company description (may contain brand/product info)
- Company domain/website
- Industry
- Location
- Size

### What We CANNOT Get from Prospeo:
- ❌ Actual website content (HTML, pages, navigation)
- ❌ Product listings
- ❌ Brand filter dropdowns
- ❌ FAQ pages
- ❌ Detailed page structure

---

## 💡 Recommendation

Since we **cannot scrape website content** from Prospeo alone, we have options:

### Option 1: Use Company Description + Domain (Current)
- Prospeo's `company.description` often contains useful info
- We provide website URL in prompt so AI can reference it
- **Limitation**: AI model may need to have seen the website or rely on description

### Option 2: Add Web Scraping (Future Enhancement)
- After fetching from Prospeo, scrape company website
- Extract: navigation menu, product listings, brand mentions
- Feed this into the AI prompt
- **Benefits**: More accurate qualification
- **Costs**: Additional processing time, need scraping service

### Option 3: Use AI with Website Access
- Use a model that can browse/access websites
- Pass URL directly, let AI analyze
- **Benefits**: Most accurate
- **Costs**: Requires model with browsing capability

---

## ✅ Current Implementation

**What we're doing:**
- Using `company.website` or `company.domain` from Prospeo
- Including in prompt for AI analysis
- AI uses company description + website URL to make determination
- AI may need to rely on description if website isn't accessible

**Prompt includes:**
- Company Website URL (from Prospeo)
- Company LinkedIn URL (from person or company data)
- Company Name
- Company Description (from Prospeo)
- Company Industry

**AI analyzes based on:**
- Available description
- Website URL (for reference)
- Patterns in company name/description

---

## 🚀 Future Enhancement Ideas

1. **Add Web Scraping**: Use services like ScrapingBee, ScraperAPI, or BeautifulSoup
2. **Use Browser-based AI**: Models that can access websites directly
3. **Cache Website Content**: Store scraped content in Supabase for faster re-qualification
4. **Manual Review Queue**: Flag uncertain cases for manual review

---

## ⚠️ Important Note

**The prompt you provided is designed for analyzing actual website content.** Since Prospeo doesn't provide scraped website content, the AI will:
1. Use the company description from Prospeo (if detailed)
2. Reference the website URL (if AI has knowledge of it)
3. Make best judgment based on available data

**For best results, consider adding web scraping** to actually analyze the website structure, navigation, and product listings as described in your prompt.
