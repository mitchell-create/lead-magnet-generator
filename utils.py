"""
Utility functions for parsing, formatting, and helper operations.
"""
import re
import json
from typing import Dict, Optional, Tuple, List, Any


def parse_natural_language_input(text: str) -> Dict:
    """
    Parse natural language input from Slack command.
    Extracts filters like keywords, industry, location, seniority, etc.
    
    Args:
        text: Raw text from Slack command
    
    Returns:
        Dictionary with parsed filters and metadata
    """
    result = {
        'target_companies': [],
        'qualification_criteria': {},
        'search_keywords': [],
        'prospeo_filters': {}
    }
    
    if not text:
        return result
    
    # Split by | or space for filter separation
    filters = re.split(r'\||\s+', text)
    
    for filter_part in filters:
        filter_part = filter_part.strip()
        if not filter_part:
            continue
        
        # Parse key=value pairs
        if '=' in filter_part:
            key, value = filter_part.split('=', 1)
            key = key.strip().lower()
            value = value.strip().strip('"').strip("'")
            
            # Handle comma-separated values
            if ',' in value:
                values = [v.strip() for v in value.split(',')]
            else:
                values = [value]
            
            # Map to Prospeo filter names and internal structure
            if key == 'keywords':
                result['target_companies'] = values
                result['search_keywords'] = values
                result['prospeo_filters']['company_keywords'] = ', '.join(values)  # Convert to string for Prospeo
            elif key == 'industry':
                result['prospeo_filters']['company_industry'] = values
            elif key == 'location':
                result['prospeo_filters']['company_location'] = values
            elif key == 'seniority':
                result['prospeo_filters']['person_seniority'] = values
            elif key == 'our-company-details':
                result['qualification_criteria']['our_company_details'] = value
    
    return result


def build_prospeo_filters(parsed_input: Dict, include_seniority: bool = False) -> Dict:
    """
    Build Prospeo API filter dictionary from parsed input.
    
    Args:
        parsed_input: Parsed input from parse_natural_language_input
        include_seniority: Whether to include person_seniority in filters (only for person search, not company search)
    
    Returns:
        Dictionary with Prospeo filter structure
    """
    filters = {}
    prospeo_filters = parsed_input.get('prospeo_filters', {})
    
    # Never send "keywords" to Prospeo; only company_keywords for /search-company.
    # If something put "keywords" in prospeo_filters, treat it as company_keywords.
    if 'keywords' in prospeo_filters and 'company_keywords' not in prospeo_filters:
        kw = prospeo_filters['keywords']
        prospeo_filters = dict(prospeo_filters)
        prospeo_filters['company_keywords'] = kw if isinstance(kw, str) else ', '.join(kw) if isinstance(kw, (list, tuple)) else str(kw)
        del prospeo_filters['keywords']
    
    # Company-level filters (for /search-company)
    if 'company_industry' in prospeo_filters:
        filters['company_industry'] = {
            'include': prospeo_filters['company_industry'] if isinstance(prospeo_filters['company_industry'], list) else [prospeo_filters['company_industry']]
        }
    
    # Company location filter (DISABLED - requires exact values from Prospeo dashboard)
    # 
    # STATUS: Currently disabled because exact location format values are not available.
    # Prospeo requires exact location strings that match their internal format.
    # 
    # To enable location filtering in the future:
    # 1. Log into Prospeo dashboard
    # 2. Build a search with location filters
    # 3. Click "API JSON" or "View API Request" to see the exact format
    # 4. Copy the exact location values (e.g., "United States", "US", "California", etc.)
    # 5. Uncomment the code below and use those exact values
    # 
    # Until then, location filtering is skipped to avoid API errors.
    # Companies can still be filtered by location in post-processing if needed.
    #
    # if 'company_location' in prospeo_filters:
    #     location_values = prospeo_filters['company_location']
    #     if isinstance(location_values, list) and location_values:
    #         # Only add if we have valid location values
    #         # User should verify these match Prospeo dashboard exactly
    #         filters['company_location'] = {
    #             'include': location_values
    #     elif location_values:  # Single string value
    #         filters['company_location'] = {
    #             'include': [location_values]
    #         }
    
    # Company keywords for /search-company (Prospeo supports this on company search)
    # Per COMPANY_SEARCH_UPDATE.md, /search-company accepts company_keywords as a string.
    # If the API returns INVALID_FILTERS for this field, we can fall back to AI-only keyword use.
    if 'company_keywords' in prospeo_filters and prospeo_filters['company_keywords']:
        kw = prospeo_filters['company_keywords']
        filters['company_keywords'] = (
            kw if isinstance(kw, str) else ', '.join(kw) if isinstance(kw, (list, tuple)) else str(kw)
        )
    
    # Person-level filters (only if include_seniority is True, for /search-person)
    if include_seniority and 'person_seniority' in prospeo_filters:
        filters['person_seniority'] = {
            'include': prospeo_filters['person_seniority'] if isinstance(prospeo_filters['person_seniority'], list) else [prospeo_filters['person_seniority']]
        }
    
    return filters


def format_wholesale_partner_prompt(
    company_data: Dict,
    scraped_content: Optional[str] = None
) -> str:
    """
    Format the wholesale partner check prompt (Check #1).
    Focuses ONLY on whether company is a multi-brand retailer/reseller.
    
    Args:
        company_data: Company information dictionary
        scraped_content: Scraped website content (optional)
    
    Returns:
        Formatted prompt string for wholesale partner check
    """
    company_website = company_data.get('website') or company_data.get('domain') or 'N/A'
    
    if company_website and company_website != 'N/A' and not company_website.startswith('http'):
        company_website = f"https://{company_website}"
    
    prompt = f"""Determine if this company is a MULTI-BRAND RETAILER/RESELLER (wholesale partner type).

MULTI-BRAND RETAILER/RESELLER = A company that sells products from multiple brands/manufacturers to end customers (B2C or B2B2C).

Why we want these companies: They already have distribution channels and can stock our products alongside other brands. They're ideal partners because they're set up to carry multiple product lines.

Positive indicators:
- Website shows multiple brands/products from different manufacturers
- Product pages list various brands (e.g., "Shop by Brand", "Brands we carry")
- Retail store, e-commerce site, or distributor that stocks multiple vendors
- Categories/collections that include products from different manufacturers
- "About" section mentions carrying multiple brands or being a retailer/reseller

NOT a multi-brand retailer:
- Manufacturer selling only their own products
- Single-brand store (only one brand's products)
- Service provider with no product retail component (unless they have a pro shop/retail section)
- B2B manufacturer that doesn't resell products to end customers

Respond with ONLY:
VERDICT: YES (if multi-brand retailer/reseller) or NO (if not)

REASONING: [1-2 sentences explaining your verdict]

---

Company Website: {company_website}
Company Description: {company_data.get('description', 'N/A')}
Company Name: {company_data.get('name', 'N/A')}
Company Industry: {company_data.get('industry', 'N/A')}

{chr(10) + '='*80 + chr(10) + 'SCRAPED WEBSITE CONTENT:' + chr(10) + '='*80 + chr(10) + scraped_content + chr(10) + '='*80 if scraped_content else ''}"""
    
    return prompt


def format_keyword_match_prompt(
    company_data: Dict,
    keywords: list,
    scraped_content: Optional[str] = None,
    our_company_details: str = None
) -> str:
    """
    Format the keyword match check prompt (Check #2).
    Focuses ONLY on whether company matches the specified keywords/product categories.
    
    Args:
        company_data: Company information dictionary
        keywords: List of keywords to match against
        scraped_content: Scraped website content (optional)
        our_company_details: Description of our company and products (optional)
    
    Returns:
        Formatted prompt string for keyword match check
    """
    company_website = company_data.get('website') or company_data.get('domain') or 'N/A'
    
    if company_website and company_website != 'N/A' and not company_website.startswith('http'):
        company_website = f"https://{company_website}"
    
    keywords_list = ', '.join(keywords) if keywords else 'N/A'
    our_company_info = our_company_details or 'Multi-brand retailer/reseller looking for partners to stock our products'
    
    prompt = f"""Determine if this company is a GOOD PRODUCT/INDUSTRY FIT based on whether the products they sell align with our company's products and target market.

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

PRODUCT_CATEGORIES: [List of specific product categories they sell, comma-separated. Examples: Golf Equipment, Athletic Apparel, Pro Shop Items, Sporting Goods. Be specific and comprehensive - these will be used for future keyword matching.]

MARKET_SEGMENTS: [List of market segments they serve, comma-separated. Examples: Golf Courses, Pro Shops, Athletic Retailers, Sporting Goods Stores. Describe their target customer base.]

REASONING: [1-2 sentences explaining why their product focus does or doesn't align with our target market]

EVIDENCE: [Top 2-3 specific categories, products, or website elements that support your verdict]

---

Now analyze this company:

Our Company: {our_company_info}

Target Keywords/Industries: {keywords_list}

Company Website: {company_website}

Company Description: {company_data.get('description', 'N/A')}

Company Name: {company_data.get('name', 'N/A')}

Company Industry: {company_data.get('industry', 'N/A')}

{chr(10) + '='*80 + chr(10) + 'SCRAPED WEBSITE CONTENT:' + chr(10) + '='*80 + chr(10) + scraped_content + chr(10) + '='*80 if scraped_content else ''}"""
    
    return prompt


def extract_person_and_company_data(prospeo_response: Dict) -> Tuple[Dict, Dict]:
    """
    Extract person and company data from Prospeo API response.
    
    Args:
        prospeo_response: Raw response from Prospeo API
    
    Returns:
        Tuple of (person_data, company_data) dictionaries
    """
    # Handle person response structure
    person_data = {}
    company_data = {}
    
    if 'person' in prospeo_response:
        person_data = prospeo_response['person']
    elif 'id' in prospeo_response and 'name' in prospeo_response:
        person_data = prospeo_response
    else:
        person_data = prospeo_response
    
    # Extract company data
    if 'company' in prospeo_response:
        company_data = prospeo_response['company']
    elif 'company' in person_data:
        company_data = person_data['company']
    
    return person_data, company_data


def sanitize_csv_field(value: Any) -> str:
    """
    Sanitize a field value for CSV output.
    
    Args:
        value: Value to sanitize
    
    Returns:
        Sanitized string
    """
    if value is None:
        return ''
    
    # Convert to string
    str_value = str(value)
    
    # Remove or escape problematic characters
    str_value = str_value.replace('\n', ' ').replace('\r', ' ')
    str_value = str_value.replace('"', '""')  # Escape quotes for CSV
    
    return str_value


def extract_unique_companies_from_persons(persons: List[Dict]) -> List[Dict]:
    """
    Extract unique companies from a list of person responses.
    
    Args:
        persons: List of person response dictionaries
    
    Returns:
        List of unique company dictionaries
    """
    seen_company_ids = set()
    unique_companies = []
    
    for person in persons:
        person_data, company_data = extract_person_and_company_data(person)
        
        if company_data:
            company_id = company_data.get('id') or company_data.get('company_id')
            if company_id and company_id not in seen_company_ids:
                seen_company_ids.add(company_id)
                unique_companies.append(company_data)
    
    return unique_companies


def extract_person_seniority_filter(parsed_input: Dict) -> Dict:
    """
    Extract person seniority filter from parsed input.
    
    Args:
        parsed_input: Parsed input dictionary
    
    Returns:
        Dictionary with person_seniority filter structure for Prospeo
    """
    prospeo_filters = parsed_input.get('prospeo_filters', {})
    
    if 'person_seniority' in prospeo_filters:
        seniority_values = prospeo_filters['person_seniority']
        if isinstance(seniority_values, list):
            return {
                'person_seniority': {
                    'include': seniority_values
                }
            }
        else:
            return {
                'person_seniority': {
                    'include': [seniority_values]
                }
            }
    
    return {}


def parse_keyword_check_response(response_text: str) -> Dict[str, Any]:
    """
    Parse structured AI response from Check #2 to extract:
    - VERDICT (YES/NO)
    - PRODUCT_CATEGORIES (list)
    - MARKET_SEGMENTS (list)
    - REASONING (text)
    - EVIDENCE (text)
    
    Args:
        response_text: Full AI response text
    
    Returns:
        Dictionary with parsed components
    """
    result = {
        'matches_keywords': False,
        'response_text': response_text,
        'product_categories': [],
        'market_segments': [],
        'reasoning': '',
        'evidence': ''
    }
    
    response_upper = response_text.upper()
    
    # Extract VERDICT
    if 'VERDICT:' in response_upper:
        verdict_line = [line for line in response_text.split('\n') if 'VERDICT:' in line.upper()]
        if verdict_line:
            verdict_text = verdict_line[0].upper()
            result['matches_keywords'] = 'YES' in verdict_text and 'NO' not in verdict_text.split(':')[1]
    else:
        # Fallback: check first line or entire response for YES/NO
        first_line = response_text.split('\n')[0].upper()
        result['matches_keywords'] = 'YES' in first_line or ('VERDICT' not in response_upper and 'YES' in response_upper.split('\n')[0])
    
    # Extract PRODUCT_CATEGORIES
    if 'PRODUCT_CATEGORIES:' in response_upper:
        categories_match = re.search(r'PRODUCT_CATEGORIES:\s*(.*?)(?=\n(?:MARKET_SEGMENTS|REASONING|EVIDENCE|$))', response_text, re.IGNORECASE | re.DOTALL)
        if categories_match:
            categories_str = categories_match.group(1).strip()
            # Parse comma-separated or line-separated categories
            categories = [cat.strip() for cat in re.split(r'[,\n]', categories_str) if cat.strip()]
            # Remove brackets if present
            categories = [re.sub(r'^\[|\]$', '', cat).strip() for cat in categories]
            result['product_categories'] = categories
    
    # Extract MARKET_SEGMENTS
    if 'MARKET_SEGMENTS:' in response_upper:
        segments_match = re.search(r'MARKET_SEGMENTS:\s*(.*?)(?=\n(?:REASONING|EVIDENCE|$))', response_text, re.IGNORECASE | re.DOTALL)
        if segments_match:
            segments_str = segments_match.group(1).strip()
            # Parse comma-separated or line-separated segments
            segments = [seg.strip() for seg in re.split(r'[,\n]', segments_str) if seg.strip()]
            # Remove brackets if present
            segments = [re.sub(r'^\[|\]$', '', seg).strip() for seg in segments]
            result['market_segments'] = segments
    
    # Extract REASONING
    if 'REASONING:' in response_upper:
        reasoning_match = re.search(r'REASONING:\s*(.*?)(?=\n(?:EVIDENCE|$))', response_text, re.IGNORECASE | re.DOTALL)
        if reasoning_match:
            result['reasoning'] = reasoning_match.group(1).strip()
    
    # Extract EVIDENCE
    if 'EVIDENCE:' in response_upper:
        evidence_match = re.search(r'EVIDENCE:\s*(.*?)(?=\n|$)', response_text, re.IGNORECASE | re.DOTALL)
        if evidence_match:
            result['evidence'] = evidence_match.group(1).strip()
    
    return result


def quick_match_keywords_against_categories(
    new_keywords: List[str],
    stored_categories: List[str]
) -> Dict[str, Any]:
    """
    Quick match without AI - match new keywords against stored product categories.
    
    Args:
        new_keywords: List of keywords from current search
        stored_categories: List of product categories stored from previous Check #2
    
    Returns:
        Dictionary with:
        - confidence: 'strong_match' | 'no_match' | 'uncertain'
        - matched: bool or None (None if uncertain)
        - match_count: int
        - reasoning: str
    """
    if not new_keywords or not stored_categories:
        return {
            'confidence': 'uncertain',
            'matched': None,
            'match_count': 0,
            'reasoning': 'Missing keywords or categories for matching'
        }
    
    # Normalize (lowercase, strip)
    keywords_normalized = [kw.lower().strip() for kw in new_keywords]
    categories_normalized = [cat.lower().strip() for cat in stored_categories]
    
    # Check for matches
    matches = []
    for keyword in keywords_normalized:
        # Exact match
        if keyword in categories_normalized:
            matches.append(keyword)
            continue
        
        # Partial match (keyword contained in category or vice versa)
        for category in categories_normalized:
            if keyword in category or category in keyword:
                matches.append(f"{keyword} → {category}")
                break
    
    match_count = len(matches)
    total_keywords = len(keywords_normalized)
    
    # Determine confidence
    if match_count == 0:
        return {
            'confidence': 'no_match',
            'matched': False,
            'match_count': 0,
            'reasoning': f'No keywords matched stored categories: {stored_categories}'
        }
    elif match_count == total_keywords:
        return {
            'confidence': 'strong_match',
            'matched': True,
            'match_count': match_count,
            'reasoning': f'All {total_keywords} keywords matched categories: {matches}'
        }
    elif match_count >= total_keywords * 0.5:  # At least 50% match
        return {
            'confidence': 'strong_match',
            'matched': True,
            'match_count': match_count,
            'reasoning': f'{match_count}/{total_keywords} keywords matched (strong match): {matches}'
        }
    else:
        return {
            'confidence': 'uncertain',
            'matched': None,  # Uncertain
            'match_count': match_count,
            'reasoning': f'Only {match_count}/{total_keywords} keywords matched - ambiguous, needs AI check: {matches}'
        }
