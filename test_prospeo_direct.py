"""
Minimal Prospeo /search-company debug script.
Calls API with 1 broad industry, prints raw response.
"""
import os
import sys
os.environ.setdefault("HTTP_PROXY", "")
os.environ.setdefault("HTTPS_PROXY", "")
os.environ.setdefault("NO_PROXY", "*")

import config
from layer2_prospeo_client import ProspeoClient

def main():
    config.validate_config()
    client = ProspeoClient()

    # Single broad industry
    filters = {"company_industry": {"include": ["IT Services and IT Consulting"]}}
    print("Calling /search-company with filters:", filters)
    print()

    try:
        data = client.fetch_companies_page(1, 25, filters)
        companies = data.get("data", [])
        meta = data.get("meta", {})
        print("Normalized: data length =", len(companies), "| meta =", meta)
        if companies:
            c = companies[0]
            print("First company:", c.get("name"), "|", c.get("industry"))
        else:
            print("No companies in response.")
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
