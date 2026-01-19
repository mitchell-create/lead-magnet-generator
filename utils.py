"""
Utility functions for parsing, formatting, and helper operations.
"""
import re
import json
from typing import Dict, Optional, Tuple


def parse_natural_language_input(text: str) -> Dict[str, any]:
    """
    Parse natural language Slack input to extract search criteria and qualification rules.
    
    Expected formats:
    - "Target: Company1, Company2 | Criteria: Industry=SaaS, Size>50"
    - "Find leads: SaaS companies with >50 employees"
    - "Search for: [keywords] | Good fit: [criteria]"
    
    Returns:
        dict with keys: 'target_companies', 'search_keywords', 'qualification_criteria'
    """
    result = {
        'target_companies': [],
        'search_keywords': [],
        'qualification_criteria': {},
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
    
    Returns filters dictionary ready for Prospeo API.
    """
    filters = {}
    
    # Map target companies to company filters
    if parsed_input.get('target_companies'):
        # If we have company names, we might search by company name
        # Note: Adjust based on actual Prospeo API filter structure
        filters['company_name'] = parsed_input['target_companies']
    
    # Map industry keywords
    if parsed_input.get('search_keywords'):
        filters['keywords'] = parsed_input['search_keywords']
    
    # Map qualification criteria that can be used for initial filtering
    qual_criteria = parsed_input.get('qualification_criteria', {})
    if 'industry' in qual_criteria:
        filters['industry'] = qual_criteria['industry']
    
    if 'min_employees' in qual_criteria:
        filters['company_size_min'] = qual_criteria['min_employees']
    
    return filters


def format_qualification_template(
    person_data: Dict,
    company_data: Dict,
    target_companies: list,
    qualification_criteria: Dict
) -> str:
    """
    Format the qualification prompt template with dynamic data.
    
    Args:
        person_data: Person information from Prospeo
        company_data: Company information from Prospeo
        target_companies: List of target company names/industries
        qualification_criteria: Dictionary of qualification criteria
    
    Returns:
        Formatted prompt string
    """
    # Build criteria description
    criteria_parts = []
    for key, value in qualification_criteria.items():
        if isinstance(value, (int, float)):
            criteria_parts.append(f"{key.replace('min_', '')} > {value}")
        else:
            criteria_parts.append(f"{key} = {value}")
    criteria_text = ", ".join(criteria_parts) if criteria_parts else "No specific criteria provided"
    
    target_text = ", ".join(target_companies) if target_companies else "General search"
    
    template = f"""You are evaluating if a company/person is a good fit for outreach.

Target Companies/Industries: {target_text}
Qualification Criteria: {criteria_text}

Company Information:
- Company Name: {company_data.get('name', 'N/A')}
- Company Description: {company_data.get('description', 'N/A')}
- Industry: {company_data.get('industry', 'N/A')}
- Company Size: {company_data.get('size', 'N/A')}
- Location: {company_data.get('location', 'N/A')}

Person Information:
- Name: {person_data.get('name', 'N/A')}
- Title: {person_data.get('title', 'N/A')}

Based on the above criteria, is this company a good fit? Reply with ONLY "YES" or "NO"."""

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
