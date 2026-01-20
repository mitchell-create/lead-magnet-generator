"""
Website Scraper Module
Scrapes company websites to extract content for AI qualification.
"""
import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import time
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteScraper:
    """Scrapes website content for company analysis."""
    
    def __init__(self, timeout: int = 10, max_content_length: int = 50000):
        """
        Initialize website scraper.
        
        Args:
            timeout: Request timeout in seconds
            max_content_length: Maximum content length to scrape (chars)
        """
        self.timeout = timeout
        self.max_content_length = max_content_length
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_website(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a website and extract relevant content.
        
        Args:
            url: Website URL to scrape
        
        Returns:
            Dictionary with scraped content, or None if failed
        """
        if not url or url == 'N/A':
            return None
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        try:
            logger.info(f"Scraping website: {url}")
            
            # Fetch the page
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract key content
            scraped_data = {
                'url': url,
                'title': self._extract_title(soup),
                'navigation': self._extract_navigation(soup),
                'footer': self._extract_footer(soup),
                'main_content': self._extract_main_content(soup),
                'product_listings': self._extract_product_listings(soup),
                'brand_mentions': self._extract_brand_mentions(soup),
                'meta_description': self._extract_meta_description(soup)
            }
            
            logger.info(f"Successfully scraped {url}")
            return scraped_data
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ""
    
    def _extract_navigation(self, soup: BeautifulSoup) -> str:
        """Extract navigation menu items."""
        nav_items = []
        
        # Look for nav, header, menu elements
        for selector in ['nav', 'header nav', '.navigation', '.menu', '#menu', '.navbar']:
            nav = soup.select_one(selector)
            if nav:
                links = nav.find_all('a', href=True)
                for link in links:
                    text = link.get_text(strip=True)
                    if text:
                        nav_items.append(text)
        
        # Also check for common menu patterns
        for link in soup.find_all('a', href=True, class_=lambda x: x and ('menu' in str(x).lower() or 'nav' in str(x).lower())):
            text = link.get_text(strip=True)
            if text and text not in nav_items:
                nav_items.append(text)
        
        return " | ".join(nav_items[:20])  # Limit to 20 items
    
    def _extract_footer(self, soup: BeautifulSoup) -> str:
        """Extract footer content."""
        footer = soup.find('footer')
        if footer:
            # Get all text from footer
            footer_text = footer.get_text(separator=' | ', strip=True)
            # Limit length
            return footer_text[:1000] if len(footer_text) > 1000 else footer_text
        return ""
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content area."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find main content area
        main_content = ""
        for selector in ['main', '.main-content', '#main', '.content', 'article', 'body']:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                if len(text) > len(main_content):
                    main_content = text
        
        # Limit content length
        if len(main_content) > self.max_content_length:
            main_content = main_content[:self.max_content_length] + "..."
        
        return main_content
    
    def _extract_product_listings(self, soup: BeautifulSoup) -> str:
        """Extract product listing information."""
        product_info = []
        
        # Look for product-related elements
        for selector in ['.product', '.item', '[class*="product"]', '[class*="item"]']:
            products = soup.select(selector)
            for product in products[:10]:  # Limit to 10 products
                # Get product title/name
                title_elem = product.find(['h1', 'h2', 'h3', 'h4', '.title', '.name', 'a'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and title not in product_info:
                        product_info.append(title)
        
        return " | ".join(product_info[:20])  # Limit to 20 products
    
    def _extract_brand_mentions(self, soup: BeautifulSoup) -> str:
        """Extract mentions of brands or brand-related content."""
        brand_indicators = []
        
        # Look for "Brands" (plural) in navigation/links
        for link in soup.find_all('a', href=True):
            text = link.get_text(strip=True).lower()
            href = link.get('href', '').lower()
            
            if any(keyword in text or keyword in href for keyword in ['brands', 'companies we carry', 'shop by brand', 'all brands']):
                brand_indicators.append(link.get_text(strip=True))
        
        # Look for brand filter dropdowns
        for select in soup.find_all('select'):
            if 'brand' in select.get('name', '').lower() or 'brand' in select.get('id', '').lower():
                options = [opt.get_text(strip=True) for opt in select.find_all('option')]
                if len(options) > 1:  # Multiple brands
                    brand_indicators.append(f"Brand filter with {len(options)} options")
        
        # Look for "Dealers", "Wholesale", etc. (negative indicators)
        negative_indicators = []
        for text in soup.stripped_strings:
            text_lower = text.lower()
            if any(keyword in text_lower for keyword in ['dealer sign up', 'become a distributor', 'where to buy', 'stockists', 'retail partners']):
                negative_indicators.append(text[:100])  # First 100 chars
        
        return {
            'positive': " | ".join(brand_indicators[:10]),
            'negative': " | ".join(negative_indicators[:10])
        }
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        return ""
    
    def format_scraped_content_for_ai(self, scraped_data: Dict) -> str:
        """
        Format scraped content into a readable string for AI analysis.
        
        Args:
            scraped_data: Dictionary from scrape_website()
        
        Returns:
            Formatted string for AI prompt
        """
        if not scraped_data:
            return "Website content not available."
        
        formatted = f"""WEBSITE CONTENT ANALYSIS:

URL: {scraped_data.get('url', 'N/A')}
Page Title: {scraped_data.get('title', 'N/A')}

NAVIGATION MENU ITEMS:
{scraped_data.get('navigation', 'Not found')}

FOOTER CONTENT:
{scraped_data.get('footer', 'Not found')}

BRAND INDICATORS:
Positive (Multi-brand retailer signs): {scraped_data.get('brand_mentions', {}).get('positive', 'None found')}
Negative (Manufacturer signs): {scraped_data.get('brand_mentions', {}).get('negative', 'None found')}

PRODUCT LISTINGS:
{scraped_data.get('product_listings', 'Not found')}

MAIN CONTENT (excerpt):
{scraped_data.get('main_content', 'Not found')[:2000]}

META DESCRIPTION:
{scraped_data.get('meta_description', 'Not found')}
"""
        return formatted


def test_scraper():
    """Test the website scraper."""
    print("=== WEBSITE SCRAPER TEST ===")
    
    scraper = WebsiteScraper()
    
    # Test with a known website
    test_url = "https://cranes-country-store.com"
    
    print(f"\nScraping: {test_url}")
    result = scraper.scrape_website(test_url)
    
    if result:
        print("\n✅ Scraping successful!")
        print(f"Title: {result.get('title')}")
        print(f"Navigation items: {result.get('navigation')[:200]}")
        print(f"Brand mentions (positive): {result.get('brand_mentions', {}).get('positive', 'None')[:200]}")
        
        formatted = scraper.format_scraped_content_for_ai(result)
        print(f"\nFormatted content (first 500 chars):\n{formatted[:500]}")
    else:
        print("❌ Scraping failed")
    
    print("=" * 50)


if __name__ == "__main__":
    test_scraper()
