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
        self.search_endpoint = config.PROSPEO_SEARCH_PERSON_ENDPOINT
        self.headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }
    
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
            payload["filters"] = filters
        
        try:
            logger.info(f"Fetching Prospeo page {page} with filters: {filters}")
            response = requests.post(
                self.search_endpoint,
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
                logger.error(f"HTTP error fetching Prospeo page {page}: {e}")
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
