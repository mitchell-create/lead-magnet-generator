# Cost Estimate: Building 50 Qualified Leads

## Scenario
- **Target:** 50 qualified leads matching "golf retailers" criteria
- **Input:** 20,000 prospects from Prospeo
- **Success Rate:** 0.25% (50 out of 20,000)

---

## Cost Breakdown

### 1. **Prospeo API Costs** 📊

**Search-Person Endpoint:**
- Each page request = **1 credit** (returns up to 25 results)
- 20,000 prospects ÷ 25 per page = **800 page requests**
- Cost: **800 credits**

**Prospeo Pricing (per credit):**
| Plan | Monthly Cost | Credits/Month | Cost per Credit |
|------|--------------|---------------|-----------------|
| Starter | $39 | 1,000 | $0.039 |
| Growth | $99 | 5,000 | $0.0198 |
| Pro | $199 | 20,000 | **$0.00995** ⭐ |

**Search Cost (Pro plan):**
- 800 credits × $0.00995 = **$7.96** ≈ **$8**

**Enrichment for 50 final leads:**
- Email finder: 1 credit per lead
- Email verification: 0.5 credits per lead
- Total: 1.5 credits × 50 = 75 credits
- Cost: 75 × $0.00995 = **$0.75**

**Prospeo Total: $8.75** (using Pro plan)

---

### 2. **OpenRouter AI Costs** 🤖

**Current Setup:**
- Model: `gpt-oss-20b` (or your configured model)
- System message: ~50 tokens
- User prompt: ~1,500-2,500 tokens (wholesale partner template + scraped content)
- Output: ~5 tokens (YES/NO)

**Per Prospect:**
- Input tokens: ~1,550-2,550 tokens (average ~2,000 tokens)
- Output tokens: ~5 tokens
- Total: ~2,005 tokens per prospect

**For 20,000 prospects:**
- Total tokens: 20,000 × 2,005 = **40,100,000 tokens** (40.1M tokens)

**OpenRouter Pricing for `gpt-oss-20b`:**

Note: Pricing varies by model. For cost-effective models:
- Cheapest models: **$0.20-$0.50 per 1M input tokens**
- Mid-tier: **$1-$3 per 1M input tokens**
- Premium: **$5-$15 per 1M input tokens**

**Estimated Costs:**

| Model Tier | Input Cost/1M | Output Cost/1M | Total Cost |
|------------|---------------|----------------|------------|
| **Budget** (e.g., Grok-4 Fast) | $0.20 | $0.50 | **~$8** |
| **Mid-Tier** (most models) | $1.50 | $2.00 | **~$60** |
| **Premium** (GPT-4 class) | $10.00 | $30.00 | **~$410** |

**Recommended: Budget-Mid Tier = $8-$60**

**OpenRouter Platform Fee:**
- Additional 5.5% platform fee
- Budget tier: $8 × 1.055 = **$8.44**
- Mid-tier: $60 × 1.055 = **$63.30**

---

### 3. **Website Scraping Costs** 🌐

**Cost: FREE** (just HTTP requests)
- No API costs
- Only server bandwidth (negligible on Railway)
- Time cost: ~1-3 seconds per website

---

### 4. **Supabase Storage Costs** 💾

**Cost: FREE to ~$0.01**
- 20,000 records with metadata
- Storage: ~50MB max
- Well within free tier limits (500MB free)

---

## Total Cost Estimate

### Best Case (Budget AI Model):
| Component | Cost |
|-----------|------|
| Prospeo (Pro plan) | $8.75 |
| OpenRouter (Budget model) | $8.44 |
| Website Scraping | $0 |
| Supabase | $0 |
| **TOTAL** | **~$17** |

### Realistic Case (Mid-Tier AI Model):
| Component | Cost |
|-----------|------|
| Prospeo (Pro plan) | $8.75 |
| OpenRouter (Mid-tier) | $63.30 |
| Website Scraping | $0 |
| Supabase | $0 |
| **TOTAL** | **~$72** |

### Worst Case (Premium AI Model):
| Component | Cost |
|-----------|------|
| Prospeo (Pro plan) | $8.75 |
| OpenRouter (Premium) | $410 |
| Website Scraping | $0 |
| Supabase | $0 |
| **TOTAL** | **~$419** |

---

## Cost Optimization Strategies 💡

### 1. **Use Cheaper AI Model**
- **Save: $350+**
- Trade-off: Slightly less accurate (but for YES/NO, probably fine)

### 2. **Pre-filter with Prospeo**
- Use better Prospeo filters (industry, location) to reduce prospects
- **Example:** If you can narrow to 5,000 prospects instead of 20,000:
  - Prospeo: $2.19 (instead of $8.75)
  - OpenRouter: $2-$16 (instead of $8-$60)
  - **Total savings: ~75%**

### 3. **Limit Scraped Content**
- Only scrape if website URL exists
- Limit scraped content size (first 5000 chars)
- **Save: ~30% on tokens**

### 4. **Early Stopping**
- If qualified count reaches 50, stop immediately
- Don't process remaining prospects
- **Save: Variable** (depends on success rate)

### 5. **Batch Processing**
- Process in batches
- Stop early if target reached
- **Save: Variable**

---

## Realistic Budget Recommendation 💰

**For 50 qualified leads from 20,000 prospects:**

### Conservative Estimate: **$70-$100**
- Prospeo Pro plan: $9
- OpenRouter (mid-tier model): $60
- Buffer for errors/retries: $10-$30

### Optimized Estimate: **$20-$40**
- Pre-filter with Prospeo: 5,000 prospects
- Use budget AI model
- Early stopping when 50 found

---

## Cost Per Qualified Lead

| Scenario | Total Cost | Cost per Lead |
|----------|------------|---------------|
| Best Case | $17 | **$0.34** |
| Realistic | $72 | **$1.44** |
| Optimized | $30 | **$0.60** |

---

## Key Takeaways ✅

1. **Prospeo is cheap** (~$9 for 20,000 searches)
2. **AI costs are the main variable** ($8-$410 depending on model)
3. **Website scraping is free**
4. **Total cost: $17-$100** for 50 qualified leads
5. **Cost per lead: $0.34-$2.00**

**Recommendation:** Use a budget-to-mid-tier AI model to keep costs around **$30-$70** per 50 leads.
