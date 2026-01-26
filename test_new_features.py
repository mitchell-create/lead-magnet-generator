"""
Test script for new company pre-check and re-qualification features.
Tests the complete workflow including Supabase pre-check and re-check logic.
"""
import sys
import os
# Fix encoding for Windows console
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from main import process_lead_search
import config

def test_new_workflow():
    """Test the new company-first workflow with pre-check and re-qualification."""
    print("=" * 70)
    print("Testing New Company Pre-Check and Re-Qualification Features")
    print("=" * 70)
    print()
    
    # Validate configuration first
    try:
        config.validate_config()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure your .env file has all required variables.")
        return False
    
    print("\n" + "-" * 70)
    print("Test 1: Vape Shops – Initial Search (save companies, qualify with AI)")
    print("-" * 70)
    
    # Smoke-test: small target + 1 page cap so test finishes quickly
    original_target = config.TARGET_QUALIFIED_COUNT
    original_max = config.MAX_PROCESSED_LEADS
    config.TARGET_QUALIFIED_COUNT = 5
    config.MAX_PROCESSED_LEADS = 25  # 1 page only
    
    # Industries (Prospeo enum) – retail + health/personal care where vape shops often sit
    VAPE_INDUSTRIES = [
        'General Retail',
        'Retail Health and Personal Care Products',
        'Consumer Services',
        'Retail Groceries',  # some vape/smoke shops overlap
    ]
    VAPE_KEYWORDS = ['vape shops', 'vaping', 'e-cigarettes', 'vape stores']
    OUR_DETAILS = (
        'We supply vaping products, e-cigarettes, and accessories to retailers. '
        'We want to reach vape shop owners, multi-store operators, and smoke shops.'
    )
    test_trigger_data_1 = {
        'type': 'test',
        'parsed_input': {
            'target_companies': VAPE_KEYWORDS,
            'qualification_criteria': {'our_company_details': OUR_DETAILS},
            'search_keywords': VAPE_KEYWORDS,
            'prospeo_filters': {
                'company_keywords': 'vape shops',
                'company_industry': VAPE_INDUSTRIES,
                'person_seniority': ['Founder/Owner', 'C-Suite']
            },
            'raw_text': 'keywords=vape shops,vaping,e-cigarettes | industry=General Retail,Retail Health | our-company-details="We supply vaping products to retailers"'
        },
        'slack_user_id': 'test_user',
        'slack_channel_id': 'test_channel',
        'slack_trigger_id': 'test_vape_1_' + str(os.getpid()),
        'raw_text': 'keywords=vape shops,vaping | industry=General Retail,Retail Health'
    }
    
    try:
        print(f"\nStarting vape-shop search (smoke-test: 1 page, max 25 companies)...")
        print(f"Target: {config.TARGET_QUALIFIED_COUNT} qualified persons")
        print(f"Industries: {test_trigger_data_1['parsed_input']['prospeo_filters']['company_industry']}")
        print(f"Keywords: {test_trigger_data_1['parsed_input']['target_companies']}")
        print(f"Our company: {OUR_DETAILS[:80]}...")
        print()
        
        result_1 = process_lead_search(test_trigger_data_1)
        
        print("\n" + "=" * 70)
        print("Search 1 Results:")
        print("=" * 70)
        print(f"✅ Qualified Persons: {result_1['stats']['qualified_persons_count']}")
        print(f"✅ Qualified Companies: {result_1['stats']['qualified_companies_count']}")
        print(f"✅ Total Companies Processed: {result_1['stats']['total_companies_processed']}")
        print(f"✅ Pages Processed: {result_1['stats']['pages_processed']}")
        
        # Check Supabase for saved companies
        from layer5_output import OutputManager
        output_manager = OutputManager()
        
        if output_manager.supabase:
            print("\n" + "-" * 70)
            print("Checking Supabase for saved companies...")
            print("-" * 70)
            
            # Query for companies saved in this test
            response = output_manager.supabase.table("lead_magnet_candidates")\
                .select("company_name, is_qualified, wholesale_partner_check, keyword_match_check, product_categories")\
                .eq("slack_trigger_id", test_trigger_data_1['slack_trigger_id'])\
                .is_("person_id", "null")\
                .limit(5)\
                .execute()
            
            companies = response.data if response.data else []
            print(f"Found {len(companies)} company records in Supabase")
            for company in companies:
                print(f"  - {company.get('company_name')}: "
                      f"Qualified={company.get('is_qualified')}, "
                      f"Wholesale={company.get('wholesale_partner_check')}, "
                      f"Keyword={company.get('keyword_match_check')}, "
                      f"Categories={company.get('product_categories')}")
        else:
            print("\n⚠️  Supabase not configured - skipping database check")
        
        print("\n" + "-" * 70)
        print("Test 2: Repeat Search (should use pre-check logic)")
        print("-" * 70)
        
        # Same vape-shop search again – should trigger pre-check
        test_trigger_data_2 = {
            'type': 'test',
            'parsed_input': {
                'target_companies': VAPE_KEYWORDS,
                'qualification_criteria': {'our_company_details': OUR_DETAILS},
                'search_keywords': VAPE_KEYWORDS,
                'prospeo_filters': {
                    'company_keywords': 'vape shops',
                    'company_industry': VAPE_INDUSTRIES,
                    'person_seniority': ['Founder/Owner', 'C-Suite']
                },
                'raw_text': 'keywords=vape shops,vaping,e-cigarettes | industry=General Retail,Retail Health | our-company-details="We supply vaping products"'
            },
            'slack_user_id': 'test_user',
            'slack_channel_id': 'test_channel',
            'slack_trigger_id': 'test_vape_2_' + str(os.getpid()),
            'raw_text': 'keywords=vape shops,vaping | industry=General Retail,Retail Health'
        }
        
        print(f"\nStarting search 2 (same vape-shop keywords, pre-check)...")
        print()
        
        result_2 = process_lead_search(test_trigger_data_2)
        
        print("\n" + "=" * 70)
        print("Search 2 Results (should show pre-check working):")
        print("=" * 70)
        print(f"✅ Qualified Persons: {result_2['stats']['qualified_persons_count']}")
        print(f"✅ Qualified Companies: {result_2['stats']['qualified_companies_count']}")
        print(f"✅ Total Companies Processed: {result_2['stats']['total_companies_processed']}")
        
        # Restore config
        config.TARGET_QUALIFIED_COUNT = original_target
        config.MAX_PROCESSED_LEADS = original_max
        
        print("\n" + "=" * 70)
        print("✅ Testing Complete!")
        print("=" * 70)
        print("\nWhat to check:")
        print("  1. Companies were saved to Supabase before qualification")
        print("  2. AI check results (wholesale_partner_check, keyword_match_check) are stored")
        print("  3. Product categories are stored in product_categories array")
        print("  4. Second search should show pre-check messages in logs")
        print("  5. Scraped content should be cached (check scraped_content_date)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        config.TARGET_QUALIFIED_COUNT = original_target
        config.MAX_PROCESSED_LEADS = original_max
        return False


if __name__ == "__main__":
    success = test_new_workflow()
    sys.exit(0 if success else 1)
