"""
Layer 4: The Loop (Core Logic)
Processes leads in batches until exactly 50 qualified leads are found.

New Company-First Workflow:
1. Search companies (persons WITHOUT seniority filter)
2. Extract unique companies
3. Qualify companies with AI
4. Search persons at qualified companies (WITH seniority filter)
5. Enrich emails for persons found

Saves ALL leads to Supabase first, then qualifies them.
Includes kill switch at 500 processed leads.
"""
import logging
from typing import List, Dict, Set
import config
from layer2_prospeo_client import ProspeoClient
from layer3_ai_judge import AIQualifier
from layer5_output import OutputManager
from utils import (
    extract_person_and_company_data,
    extract_unique_companies_from_persons,
    extract_person_seniority_filter
)
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeadProcessor:
    """Main processor that orchestrates fetching and qualifying leads."""
    
    def __init__(self):
        self.prospeo_client = ProspeoClient()
        self.ai_qualifier = AIQualifier()
        self.output_manager = OutputManager()
    
    def process_until_qualified(
        self,
        target_count: int = None,
        max_processed: int = None,
        filters: Dict = None,
        target_companies: list = None,
        qualification_criteria: Dict = None,
        output_metadata: Dict = None,
        parsed_input: Dict = None
    ) -> Dict:
        """
        Process leads using Company-First Workflow:
        1. Search companies (persons WITHOUT seniority filter)
        2. Extract unique companies
        3. Qualify companies with AI
        4. Search persons at qualified companies (WITH seniority filter)
        5. Enrich emails for persons found
        
        Args:
            target_count: Target number of qualified leads (default from config)
            max_processed: Maximum number of companies to process (kill switch)
            filters: Prospeo API filters (company-level only, no seniority)
            target_companies: Keywords for AI qualification (list)
            qualification_criteria: Criteria dictionary for qualification
            output_metadata: Metadata for saving to Supabase
            parsed_input: Original parsed input (for extracting seniority filter)
        
        Returns:
            Dictionary with qualified_leads, stats, and metadata
        """
        target_count = target_count or config.TARGET_QUALIFIED_COUNT
        max_processed = max_processed or config.MAX_PROCESSED_LEADS
        
        qualified_leads = []  # Final list of qualified persons with emails
        qualified_companies = []  # List of companies that passed AI qualification
        total_companies_processed = 0
        current_page = 1
        
        # Extract seniority filter for use in Phase 3 (person search)
        seniority_filter = {}
        if parsed_input:
            seniority_filter = extract_person_seniority_filter(parsed_input)
        
        logger.info(f"Starting COMPANY-FIRST lead processing: target={target_count} qualified persons")
        
        # ===== PHASE 0: SUPABASE PRE-CHECK FOR EXISTING QUALIFIED COMPANIES =====
        # This will add already qualified persons from existing companies to qualified_leads
        # and return a set of company_ids to skip Prospeo search for.
        companies_to_skip_prospeo_search = set()
        no_match_but_wholesale = set()
        
        if self.output_manager.supabase:  # Only run if Supabase is configured
            logger.info("Phase 0: Checking Supabase for existing qualified companies...")
            pre_check_results = self.output_manager.check_existing_companies_for_new_keywords(
                current_keywords=target_companies or [],
                target_count=target_count,
                current_qualified_leads=qualified_leads,  # Pass current list to append to
                output_metadata=output_metadata or {},
                seniority_filter=seniority_filter
            )
            companies_to_skip_prospeo_search = pre_check_results['skipped_company_ids']
            no_match_but_wholesale = pre_check_results['no_match_but_wholesale']
            logger.info(f"Found {len(companies_to_skip_prospeo_search)} companies in Supabase to skip Prospeo search for.")
            logger.info(f"Found {len(no_match_but_wholesale)} companies marked as no_match but wholesale (will re-check if appear in Prospeo).")
            logger.info(f"Currently have {len(qualified_leads)} qualified persons from Supabase pre-check.")
        
        # ===== PHASE 1: DISCOVER COMPANIES USING /search-company ONLY =====
        # We do NOT use /search-person here. Prospeo /search-company accepts company_keywords;
        # /search-person does not. Discovery is company-only.
        seen_company_ids: Set[str] = set()
        logger.info("Phase 1: Discovering companies via /search-company ONLY (no /search-person)")
        if filters:
            logger.info(f"Phase 1 filters (sent to search-company): {list(filters.keys())}")
        
        while len(qualified_companies) < max_processed:
            logger.info(f"Phase 1 - Fetching companies page {current_page}...")
            try:
                # Use /search-company endpoint which supports company_keywords filter
                result = self.prospeo_client.fetch_companies_page(
                    page=current_page,
                    limit=config.PROSPEO_BATCH_SIZE,
                    filters=filters  # Company-level filters including company_keywords (from keywords)
                )
                companies = result.get('data', [])
                
                if not companies:
                    logger.info(f"No more companies after page {current_page - 1}")
                    break
                
                logger.info(f"Found {len(companies)} companies on page {current_page}")
                
                # ===== PHASE 2: QUALIFY COMPANIES =====
                for company_data in companies:
                    company_id = company_data.get('id') or company_data.get('company_id')
                    company_name = company_data.get('name', 'Unknown')
                    
                    # Skip if already processed in this run or from Supabase pre-check
                    if company_id and (company_id in seen_company_ids or company_id in companies_to_skip_prospeo_search):
                        logger.debug(f"Skipping company {company_name} (ID: {company_id}) - already processed or from Supabase pre-check.")
                        continue
                    if company_id:
                        seen_company_ids.add(company_id)
                    
                    if total_companies_processed >= max_processed:
                        logger.warning(f"Reached max processed companies limit ({max_processed})")
                        break
                    
                    total_companies_processed += 1
                    
                    logger.info(f"Processing company {total_companies_processed}: {company_name}")
                    
                    # Check if company exists in Supabase (for re-qualification logic)
                    existing_company_record = None
                    if self.output_manager.supabase:
                        existing_company_record = self.output_manager.get_company_from_supabase(
                            company_id=company_id,
                            company_name=company_name,
                            company_domain=company_data.get('domain')
                        )
                        if existing_company_record:
                            logger.info(f"Company {company_name} (ID: {company_id}) found in Supabase. Checking qualification status.")
                    
                    # Save ALL companies to Supabase immediately (before qualification)
                    # This creates a record for every company fetched from Prospeo
                    company_supabase_id = None
                    try:
                        if output_metadata:
                            company_supabase_id = self.output_manager.save_company_to_supabase(
                                company_data,
                                output_metadata,
                                is_qualified=False,  # Default to unqualified
                                scraped_content=None,  # Will be updated after scraping
                                scraped_content_date=None
                            )
                            logger.debug(f"Saved company {company_name} to Supabase (ID: {company_supabase_id}) for qualification.")
                    except Exception as e:
                        logger.warning(f"Error saving initial company to Supabase: {e}")
                        # Continue processing even if initial save fails
                        pass
                    
                    # Scrape website content for better analysis (if not already scraped recently)
                    company_website = company_data.get('website') or company_data.get('domain') or None
                    scraped_content = None
                    scraped_content_date = None
                    
                    if company_website:
                        # Check if scraped content exists and is recent in existing_company_record
                        if existing_company_record and existing_company_record.get('company_scraped_content') and \
                            existing_company_record.get('scraped_content_date'):
                            scraped_date_val = existing_company_record.get('scraped_content_date')
                            try:
                                if isinstance(scraped_date_val, str):
                                    scraped_date = datetime.fromisoformat(scraped_date_val.replace('Z', '+00:00'))
                                elif isinstance(scraped_date_val, datetime):
                                    scraped_date = scraped_date_val
                                else:
                                    scraped_date = None
                                if scraped_date is not None:
                                    if scraped_date.tzinfo is None:
                                        scraped_date = scraped_date.replace(tzinfo=timezone.utc)
                                    delta = datetime.now(timezone.utc) - scraped_date
                                    days_old = delta.days if isinstance(delta, timedelta) else 999
                                else:
                                    days_old = 999
                                
                                if days_old < 180:
                                    scraped_content = existing_company_record['company_scraped_content']
                                    scraped_content_date = scraped_date
                                    logger.info(f"Using cached scraped content for {company_name} (scraped {days_old} days ago).")
                                else:
                                    logger.info(f"Scraped content for {company_name} is {days_old} days old (>180). Will re-scrape.")
                            except Exception as e:
                                logger.warning(f"Error parsing scraped_content_date: {e}. Will re-scrape.")
                        
                        # Scrape if we don't have recent content
                        if not scraped_content:
                            logger.info(f"Scraping website: {company_website}")
                            try:
                                scraped_data = self.ai_qualifier.scraper.scrape_website(company_website)
                                if scraped_data:
                                    scraped_content = self.ai_qualifier.scraper.format_scraped_content_for_ai(scraped_data)
                                    scraped_content_date = datetime.now(timezone.utc)
                                    logger.info(f"Scraped content for {company_website}: {scraped_content[:100]}...")
                            except Exception as e:
                                logger.error(f"Error scraping website {company_website}: {e}")
                                scraped_content = None  # Ensure it's None on error
                    
                    # Determine if wholesale check needs to be run
                    run_wholesale_check = True
                    if existing_company_record and existing_company_record.get('wholesale_partner_check') is False:
                        # If already determined NOT a wholesale partner, skip both checks
                        logger.info(f"Company {company_name} previously failed wholesale check. Skipping all AI qualification.")
                        is_qualified = False
                        wholesale_check_passed = False
                        keyword_check_passed = False
                        wholesale_response_text = existing_company_record.get('wholesale_partner_response', 'Previously failed wholesale check.')
                        keyword_response_text = "SKIP (not wholesale partner)"
                        product_categories = []
                        market_segments = []
                        run_wholesale_check = False
                    elif existing_company_record and existing_company_record.get('wholesale_partner_check') is True:
                        # If already a wholesale partner, skip wholesale check, but re-run keyword check
                        logger.info(f"Company {company_name} previously passed wholesale check. Skipping wholesale check, re-running keyword check.")
                        wholesale_check_passed = True
                        wholesale_response_text = existing_company_record.get('wholesale_partner_response', 'Previously passed wholesale check.')
                        run_wholesale_check = False  # Don't run wholesale check again
                    
                    # Special case: Company was marked no_match but appears in Prospeo - re-run AI Check #2
                    if company_id in no_match_but_wholesale:
                        logger.info(f"Company {company_name} was marked no_match in pre-check but appears in Prospeo results. Re-running AI Check #2.")
                        # Force re-run of keyword check even if wholesale_check_passed
                        run_wholesale_check = False
                        wholesale_check_passed = True  # Assume wholesale (it's in the no_match_but_wholesale list)
                        wholesale_response_text = "Previously determined wholesale partner (from Supabase pre-check)"
                    
                    # Qualify the company using AI
                    try:
                        if run_wholesale_check:
                            # Create a mock person record with company data for AI qualification
                            mock_person = {
                                'id': None,  # No person ID for company-only search
                                'company': company_data
                            }
                            
                            # Run full AI qualification (both checks)
                            ai_qualification_results = self.ai_qualifier.qualify_person(
                                prospeo_person_response=mock_person,
                                target_companies=target_companies or [],
                                qualification_criteria=qualification_criteria or {}
                            )
                            
                            is_qualified = ai_qualification_results['is_qualified']
                            wholesale_check_passed = ai_qualification_results['wholesale_check']['passed']
                            wholesale_response_text = ai_qualification_results['wholesale_check']['response']
                            keyword_check_passed = ai_qualification_results['keyword_check']['matches_keywords']
                            keyword_response_text = ai_qualification_results['keyword_check']['response_text']
                            product_categories = ai_qualification_results['keyword_check']['product_categories']
                            market_segments = ai_qualification_results['keyword_check']['market_segments']
                            
                        else:  # If wholesale check was skipped
                            # Only re-run keyword check if wholesale_check_passed is True (from existing record)
                            if wholesale_check_passed and target_companies:
                                # Get our company details from qualification_criteria if provided
                                our_company_details = qualification_criteria.get('our_company_details') if qualification_criteria else None
                                
                                matches_keywords, keyword_response_text = self.ai_qualifier.check_keyword_match(
                                    company_data=company_data,
                                    keywords=target_companies,
                                    scraped_content=scraped_content,
                                    our_company_details=our_company_details
                                )
                                from utils import parse_keyword_check_response
                                parsed_keyword_response = parse_keyword_check_response(keyword_response_text)
                                keyword_check_passed = parsed_keyword_response['matches_keywords']
                                product_categories = parsed_keyword_response['product_categories']
                                market_segments = parsed_keyword_response['market_segments']
                                is_qualified = wholesale_check_passed and keyword_check_passed
                            else:  # If wholesale check was False, or no target_companies
                                is_qualified = False
                                keyword_check_passed = False
                                keyword_response_text = "SKIP (not wholesale partner or no keywords)"
                                product_categories = []
                                market_segments = []
                        
                        # Update company qualification status in Supabase
                        if company_supabase_id:
                            try:
                                self.output_manager.update_company_qualification_status(
                                    supabase_id=company_supabase_id,
                                    is_qualified=is_qualified,
                                    wholesale_check_passed=wholesale_check_passed,
                                    wholesale_response=wholesale_response_text,
                                    keyword_check_passed=keyword_check_passed,
                                    keyword_response=keyword_response_text,
                                    product_categories=product_categories,
                                    market_segments=market_segments,
                                    scraped_content=scraped_content,
                                    scraped_content_date=scraped_content_date
                                )
                                logger.info(f"Updated company {company_name} (ID: {company_supabase_id}) qualification status: {is_qualified}")
                            except Exception as e:
                                logger.error(f"Error updating company qualification status in Supabase for ID {company_supabase_id}: {e}")
                        
                        if is_qualified:
                            qualified_companies.append(company_data)
                            logger.info(f"✅ Company qualified: {company_name}. Now searching for persons.")
                            
                            # ===== PHASE 3: SEARCH PERSONS AT QUALIFIED COMPANY (WITH SENIORITY) =====
                            logger.info(f"Searching persons at qualified company: {company_name}")
                            
                            try:
                                # Search persons at this company WITH seniority filter
                                persons_result = self.prospeo_client.fetch_persons_at_company(
                                    company_id=company_id,
                                    company_name=company_name if not company_id else None,
                                    company_domain=company_data.get('domain') or company_data.get('website'),
                                    page=1,
                                    limit=100,  # Get all matching persons
                                    additional_filters=seniority_filter if seniority_filter else {}
                                )
                                
                                company_persons = persons_result.get('data', [])
                                logger.info(f"Found {len(company_persons)} persons at {company_name} matching seniority filter")
                                
                                # ===== PHASE 4: ENRICH EMAILS FOR PERSONS =====
                                for person in company_persons:
                                    # Check if we've reached target
                                    if len(qualified_leads) >= target_count:
                                        logger.info(f"✅ Reached target count ({target_count}) qualified persons!")
                                        break
                                    
                                    person_id = person.get('id')
                                    person_name = person.get('name', 'Unknown')
                                    
                                    # Add company data to person record
                                    person['company'] = company_data
                                    person['_qualified_company'] = True
                                    person['_openrouter_response'] = keyword_response_text  # Store company's AI response
                                    
                                    # Save person to Supabase (initial save)
                                    person_supabase_id = None
                                    try:
                                        if output_metadata:
                                            person_supabase_id = self.output_manager.save_lead_to_supabase(
                                                person,
                                                output_metadata,
                                                is_qualified=True  # Person is qualified if company is
                                            )
                                    except Exception as e:
                                        logger.warning(f"Error saving person to Supabase: {e}")
                                    
                                    # Enrich email for this person
                                    if person_id:
                                        try:
                                            logger.info(f"Enriching person {person_name} at {company_name}...")
                                            enriched_data = self.prospeo_client.enrich_person(person_id)
                                            
                                            if enriched_data:
                                                enriched_person_data = enriched_data.get('person', {}) or enriched_data
                                                if enriched_person_data.get('email'):
                                                    person['person_email'] = enriched_person_data.get('email')
                                                    person['_email_enriched'] = True
                                                    
                                                    # Update Supabase with enriched email
                                                    if person_supabase_id:
                                                        try:
                                                            self.output_manager.update_lead_qualification_status(
                                                                person_supabase_id,  # Use the ID of the person record
                                                                is_qualified=True,
                                                                openrouter_response=person['_openrouter_response'],
                                                                qualification_criteria=qualification_criteria,
                                                                enriched_email=person['person_email']
                                                            )
                                                        except Exception as e:
                                                            logger.warning(f"Error updating person email in Supabase for ID {person_supabase_id}: {e}")
                                                    
                                                    qualified_leads.append(person)
                                                    logger.info(f"✅ Qualified lead {len(qualified_leads)}/{target_count}: {person_name} at {company_name} ({enriched_person_data.get('email')})")
                                                else:
                                                    logger.warning(f"No email found for {person_name} at {company_name}")
                                                    person['_email_enriched'] = False
                                            else:
                                                logger.warning(f"No enrichment data for {person_name} at {company_name}")
                                                person['_email_enriched'] = False
                                        except Exception as e:
                                            logger.error(f"Error enriching person {person_name}: {e}")
                                            person['_email_enriched'] = False
                                    else:
                                        logger.warning(f"No person_id for {person_name}, skipping email enrichment")
                                
                                if len(qualified_leads) >= target_count:
                                    break
                                    
                            except Exception as e:
                                logger.error(f"Error searching persons at company {company_name}: {e}")
                                continue
                        else:
                            logger.info(f"❌ Company not qualified: {company_name}")
                            
                    except Exception as e:
                        logger.error(f"Error qualifying company {company_name}: {e}")
                        continue
                    
                    if len(qualified_leads) >= target_count:
                        break
                
                # Check if we've reached our goals
                if len(qualified_leads) >= target_count:
                    logger.info(f"✅ Reached target count of {target_count} qualified persons!")
                    break
                
                if total_companies_processed >= max_processed:
                    logger.warning(f"Kill switch activated: processed {total_companies_processed} companies")
                    break
                
                # Check if there are more pages
                meta = result.get('meta', {})
                if not meta.get('has_more', True):
                    logger.info(f"No more pages available for company discovery")
                    break
                
                current_page += 1
                
            except Exception as e:
                logger.error(f"Error fetching page {current_page}: {e}")
                
                # Check if it's a filter error (e.g., invalid industry)
                error_str = str(e)
                if "filter_error" in error_str or "INVALID_FILTERS" in error_str:
                    logger.error("Filter error detected - likely invalid industry or other filter value")
                    logger.error("Prospeo API will validate filters - check dashboard 'API JSON' builder for exact values")
                    # Re-raise to be caught by main.py and shown to user in Slack
                    raise
                
                current_page += 1
                if current_page > 100:  # Safety limit
                    break
                continue
        
        stats = {
            'qualified_persons_count': len(qualified_leads),
            'qualified_companies_count': len(qualified_companies),
            'total_companies_processed': total_companies_processed,
            'pages_processed': current_page - 1,
            'target_reached': len(qualified_leads) >= target_count,
            'kill_switch_activated': total_companies_processed >= max_processed
        }
        
        logger.info(f"Processing complete: {stats}")
        
        return {
            'qualified_leads': qualified_leads,
            'qualified_companies': qualified_companies,
            'stats': stats,
            'filters': filters,
            'target_companies': target_companies,
            'qualification_criteria': qualification_criteria
        }


def test_processing_loop():
    """Test function: Run processing loop with mock data."""
    print("=== LAYER 4 TEST: Processing Loop ===")
    print("Note: This will make real API calls. Reduce target_count for testing.")
    print("=" * 50)
    
    processor = LeadProcessor()
    
    # Test with small target for testing
    test_filters = {
        "keywords": ["SaaS"],
        "industry": "Technology"
    }
    
    result = processor.process_until_qualified(
        target_count=5,  # Small number for testing
        max_processed=50,  # Small limit for testing
        filters=test_filters,
        target_companies=["SaaS companies"],
        qualification_criteria={"industry": "Technology", "min_employees": 50}
    )
    
    print(f"\nProcessing Results:")
    print(f"Qualified Leads: {result['stats']['qualified_count']}")
    print(f"Total Processed: {result['stats']['total_processed']}")
    print(f"Pages Processed: {result['stats']['pages_processed']}")
    print(f"Target Reached: {result['stats']['target_reached']}")
    print(f"Kill Switch: {result['stats']['kill_switch_activated']}")
    
    if result['qualified_leads']:
        print(f"\nFirst Qualified Lead:")
        lead = result['qualified_leads'][0]
        company = lead.get('company', {})
        print(f"  Company: {company.get('name', 'Unknown')}")
        print(f"  Person: {lead.get('name', 'Unknown')}")
    
    print("=" * 50)


if __name__ == "__main__":
    test_processing_loop()
