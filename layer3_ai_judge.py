"""
Layer 3: AI Judge (Qualification)
Uses OpenRouter API to qualify leads based on company description and criteria.
Includes website scraping for better analysis.
"""
import logging
import os
from openai import OpenAI
from typing import Dict, Optional, Tuple
import config
from utils import extract_person_and_company_data
from website_scraper import WebsiteScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIQualifier:
    """AI-powered lead qualifier using OpenRouter."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or config.OPENROUTER_API_KEY
        self.model = model or config.OPENROUTER_MODEL
        self.base_url = config.OPENROUTER_BASE_URL
        
        # Initialize OpenAI client configured for OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Initialize website scraper
        self.scraper = WebsiteScraper()
    
    def check_wholesale_partner_type(
        self,
        company_data: Dict,
        scraped_content: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Check if company is a multi-brand retailer/reseller (not a manufacturer).
        This is Check #1 of 2.
        
        Args:
            company_data: Company information dictionary
            scraped_content: Scraped website content (optional)
        
        Returns:
            Tuple of (is_wholesale_partner: bool, response_text: str)
        """
        from utils import format_wholesale_partner_prompt
        
        # Format the wholesale partner check prompt
        prompt = format_wholesale_partner_prompt(
            company_data=company_data,
            scraped_content=scraped_content
        )
        
        try:
            logger.debug(f"Wholesale check: {company_data.get('name', 'Unknown')}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a wholesale partner type classifier. Determine if a company is a multi-brand retailer/reseller (YES) or a manufacturer who only sells their own products (NO). Respond with ONLY 'YES' or 'NO'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=5,
                temperature=0.0
            )
            
            response_text = response.choices[0].message.content.strip().upper()
            is_wholesale_partner = "YES" in response_text
            
            logger.info(f"Wholesale check for {company_data.get('name')}: {response_text}")
            
            return is_wholesale_partner, response_text
            
        except Exception as e:
            logger.error(f"Error in wholesale partner check: {e}")
            # This string is stored in Supabase as wholesale_response/keyword_response/openrouter_response.
            # If you see "Error: 401" or "Unauthorized" there, OpenRouter auth failed (check OPENROUTER_API_KEY).
            return False, f"Error: {str(e)}"
    
    def check_keyword_match(
        self,
        company_data: Dict,
        keywords: list,
        scraped_content: Optional[str] = None,
        our_company_details: str = None
    ) -> Tuple[bool, str]:
        """
        Check if company matches the specified keywords/criteria.
        This is Check #2 of 2.
        
        Args:
            company_data: Company information dictionary
            keywords: List of keywords to match against
            scraped_content: Scraped website content (optional)
            our_company_details: Description of our company and products (optional)
        
        Returns:
            Tuple of (matches_keywords: bool, response_text: str)
            Note: response_text will contain structured output with PRODUCT_CATEGORIES and MARKET_SEGMENTS
        """
        from utils import format_keyword_match_prompt, parse_keyword_check_response
        
        # Format the keyword match prompt
        prompt = format_keyword_match_prompt(
            company_data=company_data,
            keywords=keywords,
            scraped_content=scraped_content,
            our_company_details=our_company_details
        )
        
        try:
            logger.debug(f"Keyword check: {company_data.get('name', 'Unknown')} for keywords: {keywords}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a product/industry fit classifier. Analyze if a company's product categories align with the target keywords/industries. Respond with VERDICT: YES or NO, plus PRODUCT_CATEGORIES, MARKET_SEGMENTS, REASONING and EVIDENCE as specified in the prompt."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,  # Increased for PRODUCT_CATEGORIES, MARKET_SEGMENTS, REASONING and EVIDENCE
                temperature=0.0
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse structured response
            parsed_response = parse_keyword_check_response(response_text)
            matches_keywords = parsed_response['matches_keywords']
            
            logger.info(f"Keyword check for {company_data.get('name')}: {matches_keywords} (keywords: {keywords})")
            logger.debug(f"Full AI response: {response_text}")
            logger.debug(f"Parsed categories: {parsed_response.get('product_categories')}")
            logger.debug(f"Parsed segments: {parsed_response.get('market_segments')}")
            
            return matches_keywords, response_text
            
        except Exception as e:
            logger.error(f"Error in keyword match check: {e}")
            # This string is stored in Supabase as openrouter_response. "Error: 401" there means OpenRouter auth failed.
            return False, f"Error: {str(e)}"
    
    def qualify_person(
        self,
        prospeo_person_response: Dict,
        target_companies: list,
        qualification_criteria: Dict
    ) -> Dict:
        """
        Qualify a person/company using TWO separate AI checks:
        1. Is it a wholesale partner (multi-brand retailer)?
        2. Does it match the keywords?
        
        Only qualifies if BOTH checks pass.
        
        Args:
            prospeo_person_response: Raw person data from Prospeo API (or mock with company data)
            target_companies: List of keywords to match (used for Check #2)
            qualification_criteria: Dictionary of qualification criteria (e.g., our_company_details)
        
        Returns:
            Dictionary with detailed qualification results:
            {
                'is_qualified': bool,
                'wholesale_check': {'passed': bool, 'response': str},
                'keyword_check': {
                    'matches_keywords': bool,
                    'response_text': str,
                    'product_categories': list,
                    'market_segments': list,
                    'reasoning': str,
                    'evidence': str
                },
                'scraped_content': str or None
            }
        """
        from utils import parse_keyword_check_response
        
        # Extract person and company data
        person_data, company_data = extract_person_and_company_data(prospeo_person_response)
        
        # Scrape website content once (used for both checks)
        company_website = company_data.get('website') or company_data.get('domain') or None
        scraped_content = None
        
        if company_website:
            try:
                scraped_data = self.scraper.scrape_website(company_website)
                if scraped_data:
                    scraped_content = self.scraper.format_scraped_content_for_ai(scraped_data)
                    logger.info(f"Scraped website content for {company_data.get('name')}")
            except Exception as e:
                logger.warning(f"Error scraping website {company_website}: {e}")
        
        # Check #1: Is it a wholesale partner?
        is_wholesale_partner, wholesale_response = self.check_wholesale_partner_type(
            company_data=company_data,
            scraped_content=scraped_content
        )
        
        # Check #2: Does it match keywords? (only if Check #1 passed)
        matches_keywords = False  # Default to False
        keyword_response_text = "SKIP (not wholesale partner)"
        parsed_keyword_response = {
            'matches_keywords': False,
            'response_text': keyword_response_text,
            'product_categories': [],
            'market_segments': [],
            'reasoning': '',
            'evidence': ''
        }
        
        if is_wholesale_partner and target_companies:
            # Get our company details from qualification_criteria if provided
            our_company_details = qualification_criteria.get('our_company_details') if qualification_criteria else None
            
            matches_keywords, keyword_response_text = self.check_keyword_match(
                company_data=company_data,
                keywords=target_companies,
                scraped_content=scraped_content,
                our_company_details=our_company_details
            )
            parsed_keyword_response = parse_keyword_check_response(keyword_response_text)
            matches_keywords = parsed_keyword_response['matches_keywords']  # Use parsed verdict
            
        elif not is_wholesale_partner:
            logger.info(f"Company {company_data.get('name')} failed wholesale check, skipping keyword check")
        
        # Final qualification: BOTH checks must pass
        is_qualified = is_wholesale_partner and matches_keywords
        
        final_response_summary = f"Wholesale: {'YES' if is_wholesale_partner else 'NO'} | Keywords: {'YES' if matches_keywords else 'NO'} -> QUALIFIED: {is_qualified}"
        logger.info(f"Final qualification for {company_data.get('name')}: {final_response_summary}")
        
        return {
            'is_qualified': is_qualified,
            'wholesale_check': {
                'passed': is_wholesale_partner,
                'response': wholesale_response
            },
            'keyword_check': parsed_keyword_response,  # Store parsed details
            'scraped_content': scraped_content  # Pass scraped content for storage
        }


def test_qualify_single_lead():
    """Test function: Qualify a single lead."""
    print("=== LAYER 3 TEST: AI Judge ===")
    
    # Mock Prospeo person response (adjust structure based on actual API response)
    mock_person = {
        "id": "person123",
        "name": "John Doe",
        "title": "VP of Sales",
        "email": "john@example.com",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "company": {
            "id": "company456",
            "name": "Acme Corp",
            "description": "Acme Corp is a leading SaaS company providing cloud-based solutions for enterprise customers. Founded in 2015, we serve over 200 clients with 150+ employees.",
            "domain": "acme.com",
            "website": "https://acme.com",
            "industry": "Technology",
            "size": "150",
            "location": "San Francisco, CA"
        }
    }
    
    # Test criteria
    target_companies = ["SaaS companies", "Technology"]
    qualification_criteria = {
        "industry": "Technology",
        "min_employees": 50
    }
    
    try:
        qualifier = AIQualifier()
        is_qualified, response = qualifier.qualify_person(
            mock_person,
            target_companies,
            qualification_criteria
        )
        
        print(f"\nPerson: {mock_person['name']} at {mock_person['company']['name']}")
        print(f"Company Description: {mock_person['company']['description'][:100]}...")
        print(f"\nQualification Result: {response}")
        print(f"Is Qualified: {'YES' if is_qualified else 'NO'}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure OPENROUTER_API_KEY is set in your .env file")
        print("=" * 50)


if __name__ == "__main__":
    test_qualify_single_lead()
