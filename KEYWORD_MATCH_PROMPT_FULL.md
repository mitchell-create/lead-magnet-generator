# Full Keyword Match Prompt (Check #2)

This is the prompt used to determine if a company matches your keywords and is a good product/industry fit.

---

## The Full Prompt

```
Determine if this company is a GOOD PRODUCT/INDUSTRY FIT based on whether the products they sell align with our company's products and target market.

CONTEXT: This company has already been identified as a multi-brand retailer/reseller. Now we need to determine if they sell products in categories that align with ours.

GOOD FIT = Their product categories align with our products and target market

Why we want these companies: They already sell products similar to or complementary with ours, meaning our products would fit naturally into their existing catalog and customer base.

Positive indicators to look for:
- Product categories on their website match our target keywords/industries
  WHY: If they already have sections for our product type, they have existing customers looking for what we sell
  
- Collections or departments that align with our product categories
  WHY: Organized sections show they dedicate shelf space and marketing to our product type
  
- Selling products that are complementary to ours (not identical, but used by the same customers)
  WHY: Complementary products mean their customers would be interested in our products too
  
- Customer base and market positioning aligns with our target market
  WHY: If they serve the same demographic/use case, our products will resonate with their existing customers
  
- Mentions categories, use cases, or customer segments that match our target keywords
  WHY: This shows they actively market to the audience we want to reach

- SERVICE-BASED BUSINESSES THAT SELL RELEVANT PRODUCTS: Even if the company is primarily a service provider (e.g., golf courses, ski resorts, fitness centers, salons), they are a GOOD FIT if they have a pro shop, retail section, or sell products related to our category
  WHY: Service businesses often have retail components where they sell relevant products to their customers. A golf course with a pro shop is a perfect fit for golf equipment. A ski resort with a gear shop is perfect for winter sports equipment. These are legitimate retail partners even though retail isn't their primary business.

NOT A FIT = Their product focus doesn't align with our category

Why we want to avoid these companies: Even if they're a great multi-brand retailer, if they don't sell products in our category, they won't be interested in stocking our products and their customers won't be our target audience.

Negative indicators to look for:
- Product categories are completely different from our target keywords
  WHY: If they specialize in unrelated categories, our products won't fit their catalog or appeal to their customers
  
- Focus on a different price point or market segment than ours
  WHY: A luxury retailer won't stock mass-market products, and vice versa - misalignment in positioning means they won't carry our products
  
- Serve a completely different customer demographic or use case
  WHY: If their customers have different needs/interests, our products won't sell well in their store
  
- No existing categories where our products would naturally fit
  WHY: If there's no logical section for our products, they'd have to create entirely new categories - unlikely to happen
  
- Website description or about page indicates they specialize in categories far from ours
  WHY: Companies that position themselves as specialists in other areas typically won't dilute their brand with unrelated products

- Service-based business with NO retail component or product sales
  WHY: If they're purely a service provider with no pro shop, retail section, or product sales, they can't stock our products

KEY INVESTIGATION STEPS:
1. Review their main navigation/categories - do any align with our target keywords?
2. Check their product collections - are they selling items in our category or adjacent categories?
3. For service-based businesses (golf courses, gyms, resorts, etc.) - look for "Pro Shop," "Shop," "Gear," "Retail," or product pages
4. Look at their "About" section - do they describe themselves using any of our target keywords/industries?
5. Review sample product pages - what's the price point, quality level, and customer demographic?
6. Check their website copy and imagery - does it match our brand positioning and target market?

MAKING JUDGMENT CALLS:
- If their categories are ADJACENT to ours (complementary but not identical), they're still a GOOD FIT
  Example: We sell camping gear, they sell outdoor apparel - GOOD FIT (same customers)
  
- If they have ONE relevant category among many unrelated ones, they're still a GOOD FIT
  Example: They sell home goods, garden supplies, AND outdoor gear (our category) - GOOD FIT
  
- Service businesses with retail components are a GOOD FIT
  Example: Golf course with pro shop selling golf equipment - GOOD FIT
  Example: Ski resort with gear shop selling ski/snowboard equipment - GOOD FIT
  Example: Fitness center with retail section selling athletic apparel - GOOD FIT
  Example: Salon with product retail area - GOOD FIT (if we sell beauty/hair products)
  
- Service businesses WITHOUT any retail component are NOT A FIT
  Example: Golf course with no pro shop or product sales - NOT A FIT
  Example: Pure service provider with no merchandise - NOT A FIT
  
- If their market positioning is drastically different (luxury vs. budget), lean toward NOT A FIT even if categories overlap
  Example: We sell affordable hiking gear, they only sell premium/luxury outdoor equipment - Consider carefully
  
- If you're uncertain whether a category aligns, err on the side of GOOD FIT - we can refine later
  
- The core question: "Would their existing customers be interested in our products, and do they have a retail channel to sell them?"

Respond with:

VERDICT: Only respond with YES if they are a good fit, or NO if they are not a good fit or you are not sure.

REASONING: [1-2 sentences explaining why their product focus does or doesn't align with our target market]

EVIDENCE: [Top 2-3 specific categories, products, or website elements that support your verdict]

---

Now analyze this company:

Our Company: {{our_company_details}}

Target Keywords/Industries: {{target_company_keywords}}

Company Website: {{website}}

Company Description: {{company_description}}

Company Name: {{company_name}}

Company Industry: {{company_industry}}

================================================================================
SCRAPED WEBSITE CONTENT:
================================================================================
{{scraped_content}}
================================================================================
```

---

## Dynamic Fields (Inserted from Slack/Prospeo)

The `{{field}}` placeholders get replaced with actual data:

- **`{{our_company_details}}`** → From Slack `our-company-details=` parameter
- **`{{target_company_keywords}}`** → From Slack `keywords=` parameter  
- **`{{website}}`** → From Prospeo company data
- **`{{company_description}}`** → From Prospeo company data
- **`{{company_name}}`** → From Prospeo company data
- **`{{company_industry}}`** → From Prospeo company data
- **`{{scraped_content}}`** → From website scraper

---

## Response Format

The AI responds with:

```
VERDICT: YES (or NO)

REASONING: [1-2 sentences explaining the decision]

EVIDENCE: [Top 2-3 specific supporting elements]
```

The system extracts YES/NO from the VERDICT line.

---

## Two-Step Process

**Check #1: Wholesale Partner Type**
- Is this a multi-brand retailer/reseller?
- MUST pass before Check #2 runs

**Check #2: Keyword Match** (This Prompt)
- Does the company match your keywords?
- Only runs if Check #1 passes
- Uses the prompt above

**Final Qualification:** Both checks must pass!
