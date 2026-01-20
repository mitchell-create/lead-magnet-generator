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
from utils import format_qualification_template, extract_person_and_company_data
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
    
    def qualify_person(
        self,
        prospeo_person_response: Dict,
        target_companies: list,
        qualification_criteria: Dict
    ) -> Tuple[bool, Optional[str]]:
        """
        Qualify a person/company using AI.
        
        Args:
            prospeo_person_response: Raw person data from Prospeo API
            target_companies: List of target company names/industries
            qualification_criteria: Dictionary of qualification criteria
        
        Returns:
            Tuple of (is_qualified: bool, response_text: str)
        """
        # Extract person and company data
        person_data, company_data = extract_person_and_company_data(prospeo_person_response)
        
        # Scrape website content for better analysis
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
                # Continue without scraped content
        
        # Format the qualification prompt (includes scraped content if available)
        prompt = format_qualification_template(
            person_data=person_data,
            company_data=company_data,
            target_companies=target_companies,
            qualification_criteria=qualification_criteria,
            scraped_content=scraped_content
        )
        
        try:
            # Call OpenRouter API
            logger.debug(f"Qualifying: {company_data.get('name', 'Unknown')} / {person_data.get('name', 'Unknown')}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a wholesale partner qualification assistant. Analyze the company website and LinkedIn to determine if they are a multi-brand retailer/reseller (YES) or a manufacturer who only sells their own products (NO). Respond with ONLY 'YES' or 'NO'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=5,  # We only need YES or NO
                temperature=0.0  # Zero temperature for deterministic responses
            )
            
            response_text = response.choices[0].message.content.strip().upper()
            
            # Parse response
            is_qualified = "YES" in response_text
            
            logger.info(f"Qualification result for {company_data.get('name')}: {response_text} -> {is_qualified}")
            
            return is_qualified, response_text
            
        except Exception as e:
            logger.error(f"Error qualifying lead: {e}")
            # On error, default to False (not qualified)
            return False, f"Error: {str(e)}"


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
