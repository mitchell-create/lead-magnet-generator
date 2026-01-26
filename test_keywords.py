"""Quick test to verify Prospeo filters work"""
from layer2_prospeo_client import ProspeoClient
from utils import build_prospeo_filters

# Test with industry only (no location, no keywords)
parsed_input = {
    'prospeo_filters': {
        'company_industry': ['General Retail', 'Spectator Sports']
    }
}

filters = build_prospeo_filters(parsed_input)
print(f"Filters: {filters}")

client = ProspeoClient()
try:
    result = client.fetch_companies_page(1, 25, filters)
    print(f"Success! Found {len(result.get('data', []))} companies")
    if result.get('data'):
        print(f"First company: {result['data'][0].get('name', 'N/A')}")
        print(f"Industry: {result['data'][0].get('industry', 'N/A')}")
except Exception as e:
    print(f"Error: {e}")
