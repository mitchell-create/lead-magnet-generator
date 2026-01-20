# Website Scraping Added ✅

## What's Been Added

### 1. Website Scraper Module (`website_scraper.py`)
- Scrapes company websites using BeautifulSoup
- Extracts key content:
  - Navigation menu items
  - Footer content
  - Product listings
  - Brand mentions (positive and negative indicators)
  - Main content
  - Meta description

### 2. Integration with AI Qualification
- Automatically scrapes company website before qualification
- Includes scraped content in AI prompt
- Falls back gracefully if scraping fails

### 3. Dependencies Added
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser
- `html5lib` - Alternative parser

---

## How It Works

### Flow:
1. Fetch lead from Prospeo
2. **Scrape company website** (if URL available)
3. Extract navigation, footer, products, brand indicators
4. Format scraped content for AI
5. Send to AI with scraped content + company description
6. AI analyzes actual website structure (not just description)

---

## What Gets Scraped

### Navigation Menu
- All menu items and links
- Looks for "Brands", "Shop by Brand", etc.

### Footer
- Footer content
- Looks for "Dealers", "Wholesale", etc.

### Brand Indicators
**Positive (Multi-brand retailer):**
- "Brands" (plural) in navigation
- "Companies We Carry"
- "Shop by Brand"
- Brand filter dropdowns

**Negative (Manufacturer):**
- "Dealer Sign Up"
- "Become a Distributor"
- "Where to Buy"
- "Stockists"

### Product Listings
- Product titles
- Checks if brand names are in titles

---

## Benefits

✅ **Actual website analysis** - Not just description  
✅ **Navigation structure** - See menu items  
✅ **Brand indicators** - Find "Brands" sections  
✅ **Product analysis** - Check product titles  
✅ **Better accuracy** - AI can see actual website structure  

---

## Limitations

⚠️ **JavaScript-heavy sites** - May not work perfectly (needs Selenium/Playwright for full JS support)  
⚠️ **Rate limiting** - Some sites may block scrapers  
⚠️ **Timeout** - 10 second timeout per site  
⚠️ **Content length** - Limited to 50KB of content  

---

## Future Enhancements

1. **Add Selenium/Playwright** for JavaScript-heavy sites
2. **Caching** - Store scraped content in Supabase
3. **Retry logic** - Retry failed scrapes
4. **Proxy support** - Use proxies to avoid blocking
5. **Async scraping** - Scrape multiple sites in parallel

---

## Testing

Test the scraper:
```python
python website_scraper.py
```

Or test in qualification:
```
/lead-magnet keywords=golf retailers | seniority=Founder
```

Check Railway logs to see:
- Website scraping attempts
- Scraped content
- AI qualification results

---

## Configuration

Scraper settings (in `website_scraper.py`):
- `timeout`: 10 seconds (request timeout)
- `max_content_length`: 50,000 chars (content limit)

You can adjust these if needed.

---

## ✅ Ready to Use!

The system now:
1. ✅ Scrapes company websites
2. ✅ Extracts brand indicators
3. ✅ Analyzes navigation/footer
4. ✅ Sends to AI for qualification
5. ✅ Falls back gracefully if scraping fails

Much better accuracy for wholesale partner qualification! 🚀
