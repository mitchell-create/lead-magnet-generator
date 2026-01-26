"""
Layer 2: Prospeo Connection
Fetches leads (persons) from Prospeo API with pagination support.
"""
import logging
import requests
import time
from typing import Dict, List, Optional
import config
from utils import build_prospeo_filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProspeoClient:
    """Client for interacting with Prospeo API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.PROSPEO_API_KEY
        self.base_url = config.PROSPEO_BASE_URL
        self.search_person_endpoint = config.PROSPEO_SEARCH_PERSON_ENDPOINT
        self.search_company_endpoint = config.PROSPEO_SEARCH_COMPANY_ENDPOINT
        self.headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        # Create a session with proxies disabled to avoid Windows proxy issues
        self.session = requests.Session()
        self.session.proxies = {'http': None, 'https': None}
        # Also disable proxy from environment
        self.session.trust_env = False
    
    def fetch_persons_page(self, page: int = 1, limit: int = None, filters: Dict = None) -> Dict:
        """
        Fetch a page of persons from Prospeo API.
        
        Args:
            page: Page number (1-indexed)
            limit: Number of results per page (default from config)
            filters: Filter dictionary for search criteria
        
        Returns:
            Dictionary containing 'data' (list of persons) and 'meta' (pagination info)
        """
        limit = limit or config.PROSPEO_BATCH_SIZE
        
        payload = {
            "page": page,
            "limit": limit
        }
        
        # Add filters if provided
        if filters:
            # Remove 'keywords' if present - Prospeo doesn't support it
            if 'keywords' in filters:
                logger.warning("Removing 'keywords' filter - not supported by Prospeo search-person endpoint")
                filters = {k: v for k, v in filters.items() if k != 'keywords'}
            
            if filters:  # Only add if we have valid filters
                payload["filters"] = filters
            else:
                # If only keywords were provided, use minimal default
                payload["filters"] = {"company_industry": {"include": ["Technology"]}}
        else:
            # Prospeo requires filters, so add a minimal default if none provided
            payload["filters"] = {"company_industry": {"include": ["Technology"]}}
        
        try:
            logger.info(f"Fetching Prospeo page {page} with filters: {payload.get('filters')}")
            response = self.session.post(
                self.search_person_endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('data', []))} persons from page {page}")
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                logger.warning("Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                return self.fetch_persons_page(page, limit, filters)  # Retry
            else:
                # Log the actual error response for debugging
                try:
                    error_detail = response.json()
                    logger.error(f"HTTP error fetching Prospeo page {page}: {e}")
                    logger.error(f"Prospeo API error details: {error_detail}")
                    
                    # Extract and format user-friendly error message for industry/seniority errors
                    if error_detail.get('error') and error_detail.get('filter_error'):
                        filter_error = error_detail.get('filter_error')
                        # Check if it's an industry-related error
                        if 'company_industry' in filter_error.lower() or 'industry' in filter_error.lower():
                            user_error = (
                                f"❌ Prospeo API Error: {filter_error}\n\n"
                                f"**How to fix:**\n"
                                f"• Industry must match Prospeo's list *exactly* (e.g. \"General Retail\" not \"General\")\n"
                                f"• Full list: https://prospeo.io/api-docs/enum/industries\n"
                                f"• Case-sensitive"
                            )
                            error_detail['user_friendly_message'] = user_error
                            
                except:
                    logger.error(f"HTTP error fetching Prospeo page {page}: {e}")
                    logger.error(f"Response status: {response.status_code}, Response text: {response.text[:500]}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching Prospeo page {page}: {e}")
            raise
    
    def fetch_all_pages(self, max_pages: int = 20, filters: Dict = None) -> List[Dict]:
        """
        Fetch multiple pages of persons (for testing).
        
        Args:
            max_pages: Maximum number of pages to fetch
            filters: Filter dictionary for search criteria
        
        Returns:
            List of all person records
        """
        all_persons = []
        page = 1
        
        while page <= max_pages:
            result = self.fetch_persons_page(page, filters=filters)
            persons = result.get('data', [])
            
            if not persons:
                logger.info(f"No more results after page {page - 1}")
                break
            
            all_persons.extend(persons)
            
            # Check if there are more pages
            meta = result.get('meta', {})
            if meta.get('has_more', False) is False:
                logger.info(f"Reached last page: {page}")
                break
            
            page += 1
            time.sleep(0.5)  # Small delay between requests
        
        return all_persons
    
    def fetch_persons_at_company(
        self, 
        company_id: str = None,
        company_name: str = None,
        company_domain: str = None,
        page: int = 1,
        limit: int = None,
        additional_filters: Dict = None
    ) -> Dict:
        """
        Search for persons at a specific company with optional seniority filter.
        Used after company qualification to find persons with specific seniority levels.
        
        Args:
            company_id: Company ID from Prospeo
            company_name: Company name (alternative to company_id)
            company_domain: Company domain/website (alternative to company_id)
            page: Page number (1-indexed)
            limit: Number of results per page
            additional_filters: Additional filters (e.g., person_seniority)
        
        Returns:
            Dictionary containing 'data' (list of persons) and 'meta' (pagination info)
        """
        limit = limit or config.PROSPEO_BATCH_SIZE
        
        payload = {
            "page": page,
            "limit": limit
        }
        
        # Build filters for company search
        filters = {}
        
        # Add company filter (one of: company_id, company_name, company_domain)
        if company_id:
            filters['company_id'] = {"include": [company_id]}
        elif company_name:
            filters['company_name'] = {"include": [company_name]}
        elif company_domain:
            filters['company_domain'] = {"include": [company_domain]}
        else:
            raise ValueError("Must provide company_id, company_name, or company_domain")
        
        # Add additional filters (e.g., person_seniority)
        if additional_filters:
            filters.update(additional_filters)
        
        payload["filters"] = filters
        
        try:
            logger.info(f"Fetching persons at company (ID: {company_id}, Name: {company_name}) with filters: {additional_filters}")
            response = self.session.post(
                self.search_person_endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            persons = data.get('data', [])
            logger.info(f"Successfully fetched {len(persons)} persons at company from page {page}")
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                logger.warning("Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                return self.fetch_persons_at_company(company_id, company_name, company_domain, page, limit, additional_filters)
            else:
                try:
                    error_detail = response.json()
                    logger.error(f"HTTP error fetching persons at company: {e}")
                    logger.error(f"Prospeo API error details: {error_detail}")
                except:
                    logger.error(f"HTTP error fetching persons at company: {e}")
                    logger.error(f"Response status: {response.status_code}, Response text: {response.text[:500]}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching persons at company: {e}")
            raise
    
    def fetch_companies_page(self, page: int = 1, limit: int = None, filters: Dict = None) -> Dict:
        """
        Fetch a page of companies from Prospeo API using /search-company endpoint.
        
        This is more efficient for company discovery as it supports company_keywords filter
        and returns companies directly (not persons).
        
        Args:
            page: Page number (1-indexed)
            limit: Number of results per page (default from config)
            filters: Filter dictionary for search criteria
                   - Supports: company_industry, company_location, company_keywords
        
        Returns:
            Dictionary containing 'data' (list of companies) and 'meta' (pagination info)
        """
        limit = limit or config.PROSPEO_BATCH_SIZE
        
        payload = {
            "page": page,
            "limit": limit
        }
        
        # Add filters if provided
        if filters:
            # /search-company expects company_keywords, not "keywords". Normalize so we never send "keywords".
            f = dict(filters)
            if 'keywords' in f:
                logger.warning("Removing 'keywords' from filters for /search-company; use company_keywords only.")
                kw_val = f.pop('keywords')
                if 'company_keywords' not in f and kw_val:
                    f['company_keywords'] = kw_val if isinstance(kw_val, str) else ', '.join(kw_val) if isinstance(kw_val, (list, tuple)) else str(kw_val)
            payload["filters"] = f
        else:
            # Prospeo requires filters, so add a minimal default if none provided
            payload["filters"] = {"company_industry": {"include": ["Technology"]}}
        
        try:
            logger.info(f"Fetching companies page {page} with filters: {payload.get('filters')}")
            response = self.session.post(
                self.search_company_endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            raw = response.json()
            # Prospeo /search-company returns 'results' and 'pagination', not 'data'/'meta'
            results = raw.get('results', raw.get('data', []))
            pagination = raw.get('pagination', raw.get('meta', {}))
            # Each result has a 'company' object; flatten so downstream gets id/name/industry etc. at top level
            companies = []
            for r in results:
                c = r.get('company', r) if isinstance(r, dict) else r
                if isinstance(c, dict):
                    companies.append(c)
            total_pages = pagination.get('total_pages') or pagination.get('total_page') or pagination.get('totalPages') or 1
            current = pagination.get('page') or pagination.get('current_page') or page
            has_more = current < total_pages if total_pages else bool(companies)
            meta = {'has_more': has_more, 'total_pages': total_pages, 'page': current, **pagination}
            data = {'data': companies, 'meta': meta}
            logger.info(f"Successfully fetched {len(companies)} companies from page {page}")
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                logger.warning("Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                return self.fetch_companies_page(page, limit, filters)  # Retry
            else:
                # Log the actual error response for debugging
                try:
                    error_detail = response.json()
                    logger.error(f"HTTP error fetching companies page {page}: {e}")
                    logger.error(f"Prospeo API error details: {error_detail}")
                    
                    # Extract and format user-friendly error message
                    if error_detail.get('error') and error_detail.get('filter_error'):
                        filter_error = error_detail.get('filter_error')
                        low = filter_error.lower()
                        if 'keyword' in low:
                            user_error = (
                                f"❌ Prospeo API Error: {filter_error}\n\n"
                                f"**How to fix:**\n"
                                f"• Prospeo may not accept that exact keyword value. Try rephrasing (e.g. \"vape shops\" instead of \"vape\").\n"
                                f"• Or use only `industry=` and rely on AI to match keywords (e.g. `/lead-magnet industry=General Retail | our-company-details=\"...\"`)."
                            )
                        else:
                            user_error = (
                                f"❌ Prospeo API Error: {filter_error}\n\n"
                                f"**How to fix:**\n"
                                f"• Industry must match Prospeo's list *exactly* (e.g. \"General Retail\" not \"General\")\n"
                                f"• Full list: https://prospeo.io/api-docs/enum/industries\n"
                                f"• Case-sensitive"
                            )
                        # Store in error_detail for potential Slack notification
                        error_detail['user_friendly_message'] = user_error
                        
                except:
                    logger.error(f"HTTP error fetching companies page {page}: {e}")
                    logger.error(f"Response status: {response.status_code}, Response text: {response.text[:500]}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching companies page {page}: {e}")
            raise
    
    def enrich_person(self, person_id: str) -> Dict:
        """
        Enrich a person to get verified email and additional contact information.
        
        Args:
            person_id: The person ID from Prospeo search results
        
        Returns:
            Dictionary containing enriched person data including email
        """
        enrich_endpoint = f"{self.base_url}/enrich-person"
        
        payload = {
            "person_id": person_id
        }
        
        try:
            logger.info(f"Enriching person ID: {person_id}")
            response = self.session.post(
                enrich_endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully enriched person {person_id}")
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limited
                logger.warning("Rate limited during enrichment. Waiting 60 seconds...")
                time.sleep(60)
                return self.enrich_person(person_id)  # Retry
            else:
                try:
                    error_detail = response.json()
                    logger.error(f"HTTP error enriching person {person_id}: {e}")
                    logger.error(f"Prospeo API error details: {error_detail}")
                except:
                    logger.error(f"HTTP error enriching person {person_id}: {e}")
                    logger.error(f"Response status: {response.status_code}, Response text: {response.text[:500]}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error enriching person {person_id}: {e}")
            raise


def test_fetch_page_1():
    """Test function: Fetch and print first page of leads."""
    print("=== LAYER 2 TEST: Prospeo Connection ===")
    
    # Initialize client
    client = ProspeoClient()
    
    # Test filters (adjust based on your needs)
    test_filters = {
        "keywords": ["SaaS"],
        "industry": "Technology"
    }
    
    try:
        # Fetch first page
        result = client.fetch_persons_page(page=1, limit=25, filters=test_filters)
        
        persons = result.get('data', [])
        print(f"\nFetched {len(persons)} persons from page 1")
        print("\nFirst person (raw JSON):")
        if persons:
            import json
            print(json.dumps(persons[0], indent=2))
        else:
            print("No persons returned")
        
        print("\nMeta information:")
        print(json.dumps(result.get('meta', {}), indent=2))
        
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Make sure PROSPEO_API_KEY is set in your .env file")
        print("=" * 50)


if __name__ == "__main__":
    test_fetch_page_1()
