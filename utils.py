"""
Utility functions for parsing, formatting, and helper operations.
"""
import re
import json
from typing import Dict, Optional, Tuple


def parse_natural_language_input(text: str) -> Dict[str, any]:
    """
    Parse Slack input to extract Prospeo search filters and AI qualification criteria.
    
    New Format:
    - "industry=SaaS,Fintech | location=California | seniority=Founder | verified-email=true | size>50"
    - "keywords=golf pro shops | seniority=C-Suite,VP | location=United States"
    
    Legacy Format (still supported):
    - "Target: Company1, Company2 | Criteria: Industry=SaaS, Size>50"
    
    Returns:
        dict with keys: 'prospeo_filters', 'qualification_criteria', 'raw_text'
    """
    result = {
        'prospeo_filters': {},
        'qualification_criteria': {},
        'raw_text': text,
        # Legacy fields for backwards compatibility
        'target_companies': [],
        'search_keywords': []
    }
    
    # Split by | to separate Prospeo filters from AI qualification
    parts = text.split('|')
    prospeo_part = parts[0].strip() if len(parts) > 0 else text.strip()
    qualification_part = parts[1].strip() if len(parts) > 1 else ""
    
    # Parse Prospeo filters (left side of |)
    if prospeo_part:
        result['prospeo_filters'] = parse_prospeo_filters(prospeo_part)
    
    # Parse AI qualification criteria (right side of |)
    if qualification_part:
        result['qualification_criteria'] = parse_criteria_string(qualification_part)
    
    # Legacy parsing for backwards compatibility
    # Check if it's legacy format first
    if 'target:' in text.lower() or 'criteria:' in text.lower():
        return parse_legacy_format(text)
    
    # Extract keywords for legacy compatibility
    if 'keywords' in result['prospeo_filters']:
        result['search_keywords'] = result['prospeo_filters']['keywords']
    
    return result


def parse_prospeo_filters(filter_text: str) -> Dict[str, any]:
    """
    Parse Prospeo filter string into dictionary.
    
    Format: filter_name=value1,value2 | filter_name=value
    Examples:
    - "industry=SaaS,Fintech"
    - "location=California,New York | seniority=Founder,C-Suite"
    - "keywords=golf pro shops | verified-email=true"
    
    Returns:
        Dictionary of Prospeo filters
    """
    filters = {}
    
    # Split by spaces (filters are space-separated, values are comma-separated)
    # Handle quoted values that might contain spaces
    parts = []
    current_part = ""
    in_quotes = False
    
    for char in filter_text:
        if char == '"':
            in_quotes = not in_quotes
            current_part += char
        elif char == ' ' and not in_quotes:
            if current_part.strip():
                parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    
    if current_part.strip():
        parts.append(current_part.strip())
    
    # Parse each filter
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip().strip('"').strip("'")
            
            # Map Slack filter names to Prospeo API names
            prospeo_key = map_filter_name_to_prospeo(key)
            
            # Parse value (handle comma-separated lists and booleans)
            if prospeo_key == 'only_verified_email':
                # Boolean filter
                filters[prospeo_key] = value.lower() in ['true', '1', 'yes', 'on']
            elif ',' in value:
                # Multiple values (comma-separated)
                filters[prospeo_key] = [v.strip() for v in value.split(',')]
            else:
                # Single value (convert to list for consistency)
                filters[prospeo_key] = [value] if value else []
    
    return filters


def map_filter_name_to_prospeo(slack_filter_name: str) -> str:
    """
    Map Slack filter names to Prospeo API filter names.
    
    Slack Name -> Prospeo API Name
    """
    mapping = {
        'industry': 'company_industry',
        'company_industry': 'company_industry',
        'location': 'company_location',  # Default to company_location, could be person_location
        'company_location': 'company_location',
        'person_location': 'person_location',
        'seniority': 'person_seniority',
        'person_seniority': 'person_seniority',
        'keywords': 'keywords',
        'verified-email': 'only_verified_email',
        'verified_email': 'only_verified_email',
        'only_verified_email': 'only_verified_email',
    }
    return mapping.get(slack_filter_name, slack_filter_name)


def parse_legacy_format(text: str) -> Dict[str, any]:
    """
    Parse legacy format for backwards compatibility.
    
    Formats:
    - "Target: Company1, Company2 | Criteria: Industry=SaaS, Size>50"
    - "Find leads: SaaS companies with >50 employees"
    """
    result = {
        'target_companies': [],
        'search_keywords': [],
        'qualification_criteria': {},
        'prospeo_filters': {},
        'raw_text': text
    }
    
    # Pattern 1: Structured format with "Target:" and "Criteria:"
    if '|' in text:
        parts = text.split('|')
        for part in parts:
            part = part.strip()
            if part.lower().startswith('target:'):
                targets = part[7:].strip()
                result['target_companies'] = [t.strip() for t in targets.split(',')]
            elif part.lower().startswith('criteria:') or part.lower().startswith('good fit:'):
                criteria_text = part.split(':', 1)[1].strip()
                result['qualification_criteria'] = parse_criteria_string(criteria_text)
    
    # Pattern 2: Look for LinkedIn URLs
    linkedin_url_pattern = r'linkedin\.com/company/([^/\s]+)'
    linkedin_matches = re.findall(linkedin_url_pattern, text, re.IGNORECASE)
    if linkedin_matches:
        result['target_companies'].extend(linkedin_matches)
    
    # Pattern 3: Extract keywords (industry mentions, etc.)
    industry_keywords = ['SaaS', 'B2B', 'fintech', 'ecommerce', 'healthcare', 
                        'technology', 'software', 'tech']
    found_keywords = [kw for kw in industry_keywords if kw.lower() in text.lower()]
    result['search_keywords'] = found_keywords
    
    # Pattern 4: Extract size/employee criteria
    size_pattern = r'(?:size|employees?)\s*(?:>|more than|at least)\s*(\d+)'
    size_match = re.search(size_pattern, text, re.IGNORECASE)
    if size_match:
        result['qualification_criteria']['min_employees'] = int(size_match.group(1))
    
    # Pattern 5: Extract industry criteria
    industry_pattern = r'industry\s*=\s*([^,\s|]+)'
    industry_match = re.search(industry_pattern, text, re.IGNORECASE)
    if industry_match:
        result['qualification_criteria']['industry'] = industry_match.group(1)
        result['prospeo_filters']['company_industry'] = [industry_match.group(1)]
    
    # Convert legacy to new format
    if result['target_companies']:
        result['prospeo_filters']['keywords'] = result['target_companies']
    if result['search_keywords']:
        if 'keywords' in result['prospeo_filters']:
            result['prospeo_filters']['keywords'].extend(result['search_keywords'])
        else:
            result['prospeo_filters']['keywords'] = result['search_keywords']
    
    return result


def parse_criteria_string(criteria_text: str) -> Dict[str, any]:
    """
    Parse criteria string into structured dictionary.
    
    Examples:
    - "Industry=SaaS, Size>50" -> {'industry': 'SaaS', 'min_employees': 50}
    - "Revenue>$1M, Location=USA" -> {'min_revenue': 1000000, 'location': 'USA'}
    """
    criteria = {}
    
    # Split by comma
    parts = [p.strip() for p in criteria_text.split(',')]
    
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            criteria[key] = value
        elif '>' in part:
            match = re.match(r'(\w+)\s*>\s*(.+)', part)
            if match:
                key = match.group(1).lower()
                value_str = match.group(2).strip()
                # Try to parse as number
                value = parse_number_with_suffix(value_str)
                if value is not None:
                    criteria[f'min_{key}'] = value
                else:
                    criteria[f'min_{key}'] = value_str
    
    return criteria


def parse_number_with_suffix(text: str) -> Optional[int]:
    """Parse numbers with suffixes like '50', '1M', '500K', etc."""
    text = text.strip().upper()
    
    # Remove currency symbols and spaces
    text = text.replace('$', '').replace(',', '').strip()
    
    multipliers = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000
    }
    
    for suffix, multiplier in multipliers.items():
        if text.endswith(suffix):
            try:
                number = float(text[:-1])
                return int(number * multiplier)
            except ValueError:
                return None
    
    try:
        return int(float(text))
    except ValueError:
        return None


def build_prospeo_filters(parsed_input: Dict) -> Dict:
    """
    Convert parsed input to Prospeo API filter format.
    
    Supports:
    - company_industry (list)
    - company_location (list)
    - person_location (list)
    - person_seniority (list)
    - keywords (list)
    - only_verified_email (boolean)
    
    Returns filters dictionary ready for Prospeo API.
    Format: {"filter_name": {"include": [...]}} or {"filter_name": true/false}
    """
    filters = {}
    
    # Get prospeo_filters from parsed input (new format)
    prospeo_filters = parsed_input.get('prospeo_filters', {})
    
    # Handle company_industry
    if 'company_industry' in prospeo_filters:
        industries = prospeo_filters['company_industry']
        if isinstance(industries, list) and industries:
            filters['company_industry'] = {"include": industries}
        elif isinstance(industries, str):
            filters['company_industry'] = {"include": [industries]}
    
    # Handle company_location
    if 'company_location' in prospeo_filters:
        locations = prospeo_filters['company_location']
        if isinstance(locations, list) and locations:
            filters['company_location'] = {"include": locations}
        elif isinstance(locations, str):
            filters['company_location'] = {"include": [locations]}
    
    # Handle person_location
    if 'person_location' in prospeo_filters:
        locations = prospeo_filters['person_location']
        if isinstance(locations, list) and locations:
            filters['person_location'] = {"include": locations}
        elif isinstance(locations, str):
            filters['person_location'] = {"include": [locations]}
    
    # Handle person_seniority
    if 'person_seniority' in prospeo_filters:
        seniorities = prospeo_filters['person_seniority']
        if isinstance(seniorities, list) and seniorities:
            filters['person_seniority'] = {"include": seniorities}
        elif isinstance(seniorities, str):
            filters['person_seniority'] = {"include": [seniorities]}
    
    # Handle keywords
    if 'keywords' in prospeo_filters:
        keywords = prospeo_filters['keywords']
        if isinstance(keywords, list) and keywords:
            filters['keywords'] = keywords
        elif isinstance(keywords, str):
            filters['keywords'] = [keywords]
    else:
        # Legacy support: check for search_keywords or target_companies
        keywords = []
        if parsed_input.get('search_keywords'):
            keywords.extend(parsed_input['search_keywords'])
        if parsed_input.get('target_companies'):
            # Convert target companies to keywords
            for company in parsed_input['target_companies']:
                cleaned = company.lower().replace('companies', '').replace('company', '').strip()
                if cleaned:
                    keywords.append(cleaned)
        if keywords:
            # Remove duplicates
            unique_keywords = []
            seen = set()
            for kw in keywords:
                if kw.lower() not in seen:
                    unique_keywords.append(kw)
                    seen.add(kw.lower())
            filters['keywords'] = unique_keywords
    
    # Handle only_verified_email (boolean)
    if 'only_verified_email' in prospeo_filters:
        filters['only_verified_email'] = prospeo_filters['only_verified_email']
    
    # Legacy support: map industry from qualification_criteria
    qual_criteria = parsed_input.get('qualification_criteria', {})
    if 'industry' in qual_criteria and 'company_industry' not in filters:
        industry = qual_criteria['industry']
        filters['company_industry'] = {"include": [industry]}
    
    # If no filters at all, add default keywords to avoid 400 error
    if not filters:
        filters['keywords'] = ["software"]
    
    return filters


def format_qualification_template(
    person_data: Dict,
    company_data: Dict,
    target_companies: list,
    qualification_criteria: Dict,
    scraped_content: Optional[str] = None
) -> str:
    """
    Format the wholesale partner qualification prompt template with dynamic data.
    
    Args:
        person_data: Person information from Prospeo
        company_data: Company information from Prospeo
        target_companies: List of target company names/industries
        qualification_criteria: Dictionary of qualification criteria
    
    Returns:
        Formatted prompt string for wholesale partner qualification
    """
    # Get company website and LinkedIn from Prospeo data
    company_website = company_data.get('website') or company_data.get('domain') or 'N/A'
    # Try to get LinkedIn from person data or company data
    company_linkedin = person_data.get('linkedin_url', '').replace('/in/', '/company/') if person_data.get('linkedin_url') else company_data.get('linkedin_url', 'N/A')
    
    # If website is a domain, prepend https://
    if company_website and company_website != 'N/A' and not company_website.startswith('http'):
        company_website = f"https://{company_website}"
    
    # Build the comprehensive wholesale partner qualification prompt
    template = f"""Determine if this company is a RETAILER/RESELLER who carries multiple brands (and could stock our products), or if they only sell their own products. 

GOOD FIT = Multi-brand retailers who resell other companies' products 

Why we want these companies: They stock and sell products from various brands, meaning they could potentially carry and resell OUR products in their store or catalog. 

Positive indicators to look for:
- "Brands" (plural), "Companies We Carry," "Shop by Brand" in header/navigation/menu/footer WHY: This shows they organize their inventory by multiple brands they stock, not just their own
- Brand filter dropdowns in product collections WHY: Filters allow customers to narrow down by brand, which only makes sense if they carry multiple brands
- Product titles that lead with or end with brand names (e.g., "Stanley 2L Water Bottle" or "Water Bottle - Yeti") WHY: Including brand names in product titles indicates they're selling other companies' products and need to differentiate between brands
- Multiple recognizable third-party brand names across different products WHY: Variety of brands proves they're a reseller, not just selling their own line
- It's OK if they also sell some of their own branded products, as long as they primarily carry other brands WHY: Many retailers have a small house brand alongside the many brands they carry - this doesn't disqualify them

NOT A FIT = Companies who only sell their own brand or would compete with us 

Why we want to avoid these companies: These are manufacturers/brands who only sell their own products. They wouldn't stock our products - they would compete with us or expect us to distribute THEIR products. 

Negative indicators to look for:
- "Brand" (singular) section talking about their own company story WHY: Singular "brand" is usually an "About Us" page describing THEIR brand identity, not a catalog of brands they carry
- "Dealers," "Dealer Sign Up," "Wholesale," "Become a Distributor/Seller," "Retail Partners" in menu/navigation/footer WHY: These pages are for recruiting OTHER stores to sell THEIR products, meaning they're the manufacturer/brand, not a retailer who would stock ours
- "Where to Buy" or "Stockists" pages listing retail locations WHY: This shows where customers can buy THEIR products from other retailers - they're the brand being distributed, not the distributor
- Product titles without brand names (just "2L Water Bottle" instead of "Stanley 2L Water Bottle") WHY: If all products lack brand prefixes, it's likely everything is their own brand (redundant to say "CompanyName 2L Water Bottle" on every product when it's all theirs)
- FAQs reference only their own brand name (e.g., "How do I clean my [Company Name] products?") WHY: If FAQs only mention their brand, they don't carry other brands (otherwise FAQs would be generic or cover multiple brands)
- Only sell brands within their own corporate umbrella/portfolio WHY: Some companies own multiple brands but don't stock outside products - they're still a closed system, not open to new suppliers
- Focus on their own product development, innovation, or manufacturing WHY: Language about "our technology," "our designs," "we manufacture" indicates they're a brand/maker, not a reseller

EXAMPLES:

Example 1 - GOOD FIT:
Website: https://cranes-country-store.com/
Analysis: Has "Brands" (plural) section in header showing they organize by multiple brands. Product titles include brand names like "Stanley water bottles" proving they sell third-party products. Also sells their own "Crane's Gear" but primarily a multi-brand retailer → GOOD FIT

Example 2 - GOOD FIT:
Website: http://www.getzs.com
Analysis: Has "All Brands" section in header. Collection pages have brand filter dropdown showing multiple brands they carry, which is only useful if stocking multiple brands → GOOD FIT

Example 3 - NOT A FIT:
Website: https://www.rockybrands.com/
Analysis: Has "Brands" section but investigation shows they only sell brands within their own corporate portfolio (Rocky Brands Inc.). This is a closed portfolio system, not open to outside brands → NOT A FIT

Example 4 - NOT A FIT:
Website: https://www.freemanoutdoorgear.com/
Analysis: "Brand" (singular) section is about their own company story. Has "Dealers" page showing OTHER stores sell their products, meaning they're the manufacturer looking for distributors, not a retailer who stocks other brands → NOT A FIT

Example 5 - NOT A FIT:
Website: https://viktos.com/
Analysis: No "Brands" page. Product titles lack brand names (just "Ranger Trainer Boot" not "[Brand] Ranger Trainer Boot") indicating everything is their own line. "Dealer Sign Up" in footer means they recruit stores to sell THEIR products. FAQ asks "How do I clean my Viktos Apparel?" only mentioning their brand. They're a manufacturer selling TO retailers, not a retailer → NOT A FIT

KEY INVESTIGATION STEPS:
1. Check header/navigation/menu/footer for "Brands" (plural), "Companies We Carry," "Shop by Brand" vs "Brand" (singular)
2. Look for "Dealers," "Wholesale," "Become a Distributor/Seller," "Stockists," or "Where to Buy" in menu/navigation/footer (red flag - they're a manufacturer)
3. Check product titles - do they lead with or end with brand names? ("Stanley 2L Water Bottle" = good sign; "2L Water Bottle" = likely their own product)
4. Look for brand filter options in product collections
5. Check FAQ - does it reference only their own brand name?

MAKING JUDGMENT CALLS:
If a company shows BOTH positive and negative indicators, prioritize based on:
- If they have "Dealers/Wholesale" pages AND sell multiple brands, they might be a hybrid (manufacturer + retailer) - mark as a GOOD FIT and note both aspects
- If they have a "Brands" section but it's clearly only their portfolio companies, they're NOT A FIT
- If they sell mostly other brands but have 1-2 of their own products mixed in, they're a GOOD FIT
- The core question: "Would this company stock and resell OUR products, or would they expect US to distribute THEIRS?"

Company Website: {company_website}
Company LinkedIn: {company_linkedin}
Company Name: {company_data.get('name', 'N/A')}
Company Description: {company_data.get('description', 'N/A')}
Company Industry: {company_data.get('industry', 'N/A')}

{chr(10) + '='*80 + chr(10) + 'SCRAPED WEBSITE CONTENT:' + chr(10) + '='*80 + chr(10) + scraped_content + chr(10) + '='*80 if scraped_content else ''}

VERDICT: Only respond with YES, if they are a good fit, or NO, if they are not a good fit or you are not sure."""

    return template


def extract_person_and_company_data(prospeo_person_response: Dict) -> Tuple[Dict, Dict]:
    """
    Extract person and company data from Prospeo API response.
    
    Returns:
        Tuple of (person_data, company_data) dictionaries
    """
    person_data = {
        'id': prospeo_person_response.get('id'),
        'name': prospeo_person_response.get('name'),
        'email': prospeo_person_response.get('email'),
        'title': prospeo_person_response.get('title'),
        'linkedin_url': prospeo_person_response.get('linkedin_url'),
    }
    
    # Company data might be nested or separate
    company = prospeo_person_response.get('company') or {}
    company_data = {
        'id': company.get('id') or prospeo_person_response.get('company_id'),
        'name': company.get('name') or prospeo_person_response.get('company_name'),
        'description': company.get('description') or prospeo_person_response.get('company_description'),
        'domain': company.get('domain') or prospeo_person_response.get('company_domain'),
        'website': company.get('website') or prospeo_person_response.get('company_website'),
        'industry': company.get('industry') or prospeo_person_response.get('company_industry'),
        'size': company.get('size') or prospeo_person_response.get('company_size'),
        'location': company.get('location') or prospeo_person_response.get('company_location'),
    }
    
    return person_data, company_data


def sanitize_csv_field(value: any) -> str:
    """Sanitize a value for CSV output."""
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value).replace('\n', ' ').replace('\r', '')
