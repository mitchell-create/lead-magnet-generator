"""
Layer 5: Output
Saves qualified leads to Supabase and generates CSV file.
"""
import logging
import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Set
from supabase import create_client, Client
import config
from utils import extract_person_and_company_data, sanitize_csv_field, quick_match_keywords_against_categories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutputManager:
    """Manages output to Supabase and CSV."""
    
    def __init__(self):
        self.supabase: Client = None
        if config.SUPABASE_URL and config.SUPABASE_KEY:
            try:
                self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not configured")
    
    def save_lead_to_supabase(self, lead: Dict, metadata: Dict, is_qualified: bool = False) -> str:
        """
        Save a single lead to Supabase (called immediately after fetching from Prospeo).
        
        Args:
            lead: Single lead dictionary from Prospeo
            metadata: Metadata including Slack info, criteria, etc.
            is_qualified: Whether this lead is qualified (default False, updated later)
        
        Returns:
            ID of inserted record (or None if failed)
        """
        if not self.supabase:
            return None
        
        # Extract person and company data
        person_data, company_data = extract_person_and_company_data(lead)
        
        record = {
            # Person Data
            "person_id": person_data.get('id'),
            "person_name": person_data.get('name'),
            "person_email": person_data.get('email'),
            "person_title": person_data.get('title'),
            "person_linkedin_url": person_data.get('linkedin_url'),
            
            # Company Data
            "company_id": company_data.get('id'),
            "company_name": company_data.get('name'),
            "company_description": company_data.get('description'),
            "company_domain": company_data.get('domain'),
            "company_website": company_data.get('website'),
            "company_industry": company_data.get('industry'),
            "company_size": company_data.get('size'),
            "company_location": company_data.get('location'),
            
            # Qualification Metadata
            "is_qualified": is_qualified,
            "qualified_at": datetime.now().isoformat() if is_qualified else None,
            "qualification_criteria": json.dumps(metadata.get('qualification_criteria', {})),
            "search_criteria": metadata.get('search_criteria', ''),
            "prospeo_page_number": lead.get('_prospeo_page'),
            "processing_order": lead.get('_processing_order'),
            
            # Slack Metadata
            "slack_user_id": metadata.get('slack_user_id'),
            "slack_channel_id": metadata.get('slack_channel_id'),
            "slack_trigger_id": metadata.get('slack_trigger_id'),
            
            # Full JSON
            "raw_prospeo_data": lead,
            "openrouter_response": lead.get('_openrouter_response')
        }
        
        try:
            response = self.supabase.table("lead_magnet_candidates").insert(record).execute()
            if response.data:
                record_id = response.data[0].get('id')
                return record_id
            return None
        except Exception as e:
            logger.error(f"Error inserting lead to Supabase: {e}")
            raise
    
    def update_lead_qualification_status(
        self,
        supabase_id: str,
        is_qualified: bool,
        openrouter_response: Optional[str] = None,
        qualification_criteria: Optional[Dict] = None,
        enriched_email: Optional[str] = None
    ) -> bool:
        """
        Update qualification status for a lead already in Supabase using Supabase ID.
        
        Args:
            supabase_id: UUID of the record in Supabase
            is_qualified: New qualification status
            openrouter_response: AI response text
            qualification_criteria: Qualification criteria dict
            enriched_email: Enriched email address
        
        Returns:
            True if updated successfully
        """
        if not self.supabase:
            return False
        
        update_data = {
            "is_qualified": is_qualified,
        }
        
        if is_qualified:
            update_data["qualified_at"] = datetime.now().isoformat()
        
        if openrouter_response:
            update_data["openrouter_response"] = openrouter_response
        
        if enriched_email:
            update_data["person_email"] = enriched_email
        
        if qualification_criteria:
            update_data["qualification_criteria"] = json.dumps(qualification_criteria)
        
        try:
            response = self.supabase.table("lead_magnet_candidates")\
                .update(update_data)\
                .eq("id", supabase_id)\
                .execute()
            
            return len(response.data) > 0 if response.data else False
        except Exception as e:
            logger.error(f"Error updating qualification status: {e}")
            return False
    
    def save_to_supabase(self, qualified_leads: List[Dict], metadata: Dict) -> int:
        """
        Save qualified leads to Supabase table.
        
        Args:
            qualified_leads: List of qualified lead dictionaries
            metadata: Metadata including Slack info, criteria, etc.
        
        Returns:
            Number of records inserted
        """
        if not self.supabase:
            logger.warning("Supabase not configured, skipping database save")
            return 0
        
        records = []
        
        for idx, lead in enumerate(qualified_leads):
            # Extract person and company data
            person_data, company_data = extract_person_and_company_data(lead)
            
            record = {
                # Person Data
                "person_id": person_data.get('id'),
                "person_name": person_data.get('name'),
                "person_email": person_data.get('email'),
                "person_title": person_data.get('title'),
                "person_linkedin_url": person_data.get('linkedin_url'),
                
                # Company Data
                "company_id": company_data.get('id'),
                "company_name": company_data.get('name'),
                "company_description": company_data.get('description'),
                "company_domain": company_data.get('domain'),
                "company_website": company_data.get('website'),
                "company_industry": company_data.get('industry'),
                "company_size": company_data.get('size'),
                "company_location": company_data.get('location'),
                
                # Qualification Metadata
                "is_qualified": lead.get('_qualified', True),  # Assume qualified if in this list
                "qualified_at": datetime.now().isoformat() if lead.get('_qualified', True) else None,
                "qualification_criteria": json.dumps(metadata.get('qualification_criteria', {})),
                "search_criteria": metadata.get('search_criteria', ''),
                "prospeo_page_number": lead.get('_prospeo_page'),
                "processing_order": lead.get('_processing_order', idx + 1),
                
                # Slack Metadata
                "slack_user_id": metadata.get('slack_user_id'),
                "slack_channel_id": metadata.get('slack_channel_id'),
                "slack_trigger_id": metadata.get('slack_trigger_id'),
                
                # Full JSON
                "raw_prospeo_data": lead,
                "openrouter_response": lead.get('_openrouter_response')
            }
            
            records.append(record)
        
        try:
            # Bulk insert
            response = self.supabase.table("lead_magnet_candidates").insert(records).execute()
            inserted_count = len(response.data) if response.data else len(records)
            logger.info(f"Successfully inserted {inserted_count} records to Supabase")
            return inserted_count
            
        except Exception as e:
            logger.error(f"Error inserting to Supabase: {e}")
            raise
    
    def save_company_to_supabase(
        self,
        company_data: Dict,
        output_metadata: Dict,
        is_qualified: bool = False,
        scraped_content: Optional[str] = None,
        scraped_content_date: Optional[datetime] = None
    ) -> Optional[str]:
        """
        Save a company record to Supabase (company-only, person_id = NULL).
        Called immediately after fetching company from Prospeo, before AI qualification.
        
        Args:
            company_data: Company dictionary from Prospeo
            output_metadata: Metadata including Slack info, criteria, etc.
            is_qualified: Initial qualification status (default False, updated after AI check)
            scraped_content: Scraped website content (optional)
            scraped_content_date: When content was scraped (optional)
        
        Returns:
            ID of inserted record (or None if failed)
        """
        if not self.supabase:
            logger.warning("Supabase not configured, skipping company database save")
            return None
        
        company_id = company_data.get('id') or company_data.get('company_id')
        
        record = {
            # Person Data (NULL for company-only records)
            "person_id": None,
            "person_name": None,
            "person_email": None,
            "person_title": None,
            "person_linkedin_url": None,
            
            # Company Data
            "company_id": company_id,
            "company_name": company_data.get('name'),
            "company_description": company_data.get('description'),
            "company_domain": company_data.get('domain'),
            "company_website": company_data.get('website'),
            "company_industry": company_data.get('industry'),
            "company_size": company_data.get('size'),
            "company_location": company_data.get('location'),
            
            # Qualification Metadata
            "is_qualified": is_qualified,
            "qualified_at": datetime.now().isoformat() if is_qualified else None,
            "qualification_criteria": json.dumps(output_metadata.get('qualification_criteria', {})),
            "search_criteria": output_metadata.get('search_criteria', ''),
            
            # Slack Metadata
            "slack_user_id": output_metadata.get('slack_user_id'),
            "slack_channel_id": output_metadata.get('slack_channel_id'),
            "slack_trigger_id": output_metadata.get('slack_trigger_id'),
            
            # Scraped Content
            "company_scraped_content": scraped_content,
            "scraped_content_date": scraped_content_date.isoformat() if scraped_content_date else None,
            "last_scraped_at": datetime.now().isoformat() if scraped_content else None,
            
            # Full JSON
            "raw_prospeo_data": company_data
        }
        
        try:
            response = self.supabase.table("lead_magnet_candidates").insert(record).execute()
            if response.data:
                record_id = response.data[0].get('id')
                logger.info(f"Saved company {company_data.get('name')} to Supabase (ID: {record_id})")
                return record_id
            return None
        except Exception as e:
            logger.error(f"Error inserting company to Supabase: {e}")
            raise
    
    def get_company_from_supabase(
        self,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get an existing company record from Supabase.
        
        Args:
            company_id: Company ID from Prospeo
            company_name: Company name
            company_domain: Company domain
        
        Returns:
            Company record dictionary or None if not found
        """
        if not self.supabase:
            return None
        
        try:
            query = self.supabase.table("lead_magnet_candidates").select("*")
            
            # Query by company_id first (most reliable), then name, then domain
            if company_id:
                query = query.eq("company_id", company_id)
            elif company_name:
                query = query.eq("company_name", company_name)
            elif company_domain:
                query = query.eq("company_domain", company_domain)
            else:
                return None
            
            # Filter for company-only records (person_id IS NULL)
            query = query.is_("person_id", "null")
            
            # Get the most recent record for this company
            query = query.order("created_at", desc=True).limit(1)
            
            response = query.execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting company from Supabase: {e}")
            return None
    
    def update_company_qualification_status(
        self,
        supabase_id: str,
        is_qualified: bool,
        wholesale_check_passed: bool,
        wholesale_response: str,
        keyword_check_passed: bool,
        keyword_response: str,
        product_categories: List[str],
        market_segments: List[str],
        scraped_content: Optional[str],
        scraped_content_date: Optional[datetime]
    ):
        """
        Update the qualification status and AI results for an existing company in Supabase.
        
        Args:
            supabase_id: UUID of the company record in Supabase
            is_qualified: Final qualification status (both checks passed)
            wholesale_check_passed: Result of Check #1
            wholesale_response: AI response text from Check #1
            keyword_check_passed: Result of Check #2
            keyword_response: Full AI response from Check #2
            product_categories: Array of product categories from Check #2
            market_segments: Array of market segments from Check #2
            scraped_content: Scraped website content
            scraped_content_date: When content was scraped
        """
        if not self.supabase:
            logger.warning("Supabase not configured, skipping company database update")
            return
        
        update_data = {
            "is_qualified": is_qualified,
            "qualified_at": datetime.now().isoformat() if is_qualified else None,
            "wholesale_partner_check": wholesale_check_passed,
            "wholesale_partner_response": wholesale_response,
            "keyword_match_check": keyword_check_passed,
            "keyword_match_response": keyword_response,
            "product_categories": product_categories,
            "market_segments": market_segments,
            "company_scraped_content": scraped_content,
            "scraped_content_date": scraped_content_date.isoformat() if scraped_content_date else None,
            "last_scraped_at": datetime.now().isoformat()  # Update last scraped date
        }
        
        try:
            response = self.supabase.table("lead_magnet_candidates").update(update_data).eq("id", supabase_id).execute()
            if response.data:
                logger.info(f"Updated company qualification status for ID {supabase_id}.")
            else:
                logger.warning(f"No company record found to update for ID {supabase_id}.")
        except Exception as e:
            logger.error(f"Error updating company qualification status for ID {supabase_id}: {e}")
            raise
    
    def check_existing_companies_for_new_keywords(
        self,
        current_keywords: List[str],
        target_count: int,
        current_qualified_leads: List[Dict],
        output_metadata: Dict,
        seniority_filter: Dict
    ) -> Dict:
        """
        Check Supabase for existing wholesale-fit companies and re-evaluate them
        against new keywords using quick match + optional AI re-run.
        
        Args:
            current_keywords: Keywords from current search
            target_count: Target number of qualified leads
            current_qualified_leads: List to append qualified persons to
            output_metadata: Metadata for saving persons
            seniority_filter: Seniority filter for person search
        
        Returns:
            Dictionary with:
            - skipped_company_ids: Set of company_ids to skip in Prospeo search
            - no_match_but_wholesale: Set of company_ids that were no_match but are wholesale partners
        """
        from datetime import timezone
        
        if not self.supabase:
            logger.warning("Supabase not configured, skipping pre-check")
            return {'skipped_company_ids': set(), 'no_match_but_wholesale': set()}
        
        skipped_company_ids = set()
        no_match_but_wholesale = set()
        
        try:
            # Query for companies where wholesale_partner_check = TRUE
            response = self.supabase.table("lead_magnet_candidates")\
                .select("*")\
                .eq("wholesale_partner_check", True)\
                .is_("person_id", "null")\
                .execute()
            
            companies = response.data if response.data else []
            logger.info(f"Found {len(companies)} existing wholesale-fit companies in Supabase")
            
            for company_record in companies:
                company_id = company_record.get('company_id')
                if not company_id:
                    continue
                
                stored_categories = company_record.get('product_categories', []) or []
                
                # Quick match: new keywords vs stored categories
                if stored_categories:
                    match_result = quick_match_keywords_against_categories(
                        new_keywords=current_keywords,
                        stored_categories=stored_categories
                    )
                    
                    if match_result['confidence'] == 'strong_match' and match_result['matched']:
                        # Strong match - company is qualified for this search
                        logger.info(f"Company {company_record.get('company_name')} has strong keyword match. Checking for persons...")
                        
                        # TODO: Search for persons at this company and add to qualified_leads
                        # For now, just mark to skip Prospeo search
                        skipped_company_ids.add(company_id)
                        
                    elif match_result['confidence'] == 'no_match':
                        # No match - mark for potential re-check if appears in Prospeo
                        logger.info(f"Company {company_record.get('company_name')} has no keyword match. Will re-check if appears in Prospeo.")
                        no_match_but_wholesale.add(company_id)
                        
                    else:  # uncertain
                        # Uncertain - will need AI re-run later
                        logger.info(f"Company {company_record.get('company_name')} has uncertain keyword match. Will re-run AI check.")
                        # Don't skip - will process normally and re-run AI
                
                else:
                    # No stored categories - will need AI check
                    logger.info(f"Company {company_record.get('company_name')} has no stored categories. Will run AI check.")
                    # Don't skip - will process normally
            
            logger.info(f"Pre-check complete: {len(skipped_company_ids)} companies to skip, {len(no_match_but_wholesale)} no-match companies to re-check")
            
        except Exception as e:
            logger.error(f"Error in Supabase pre-check: {e}")
        
        return {
            'skipped_company_ids': skipped_company_ids,
            'no_match_but_wholesale': no_match_but_wholesale
        }
    
    def generate_csv(self, qualified_leads: List[Dict], metadata: Dict = None) -> str:
        """
        Generate CSV file from qualified leads.
        
        Args:
            qualified_leads: List of qualified lead dictionaries
            metadata: Optional metadata
        
        Returns:
            Path to generated CSV file
        """
        # Ensure output directory exists
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{config.CSV_FILENAME_PREFIX}_{timestamp}.csv"
        filepath = os.path.join(config.OUTPUT_DIR, filename)
        
        # Define CSV columns (based on Prospeo Person data structure)
        fieldnames = [
            'person_name',
            'person_email',
            'person_title',
            'person_linkedin_url',
            'company_name',
            'company_domain',
            'company_website',
            'company_description',
            'company_industry',
            'company_size',
            'company_location',
            'qualified_at',
            'search_criteria',
            'qualification_criteria'
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for lead in qualified_leads:
                    person_data, company_data = extract_person_and_company_data(lead)
                    
                    row = {
                        'person_name': sanitize_csv_field(person_data.get('name')),
                        'person_email': sanitize_csv_field(person_data.get('email')),
                        'person_title': sanitize_csv_field(person_data.get('title')),
                        'person_linkedin_url': sanitize_csv_field(person_data.get('linkedin_url')),
                        'company_name': sanitize_csv_field(company_data.get('name')),
                        'company_domain': sanitize_csv_field(company_data.get('domain')),
                        'company_website': sanitize_csv_field(company_data.get('website')),
                        'company_description': sanitize_csv_field(company_data.get('description')),
                        'company_industry': sanitize_csv_field(company_data.get('industry')),
                        'company_size': sanitize_csv_field(company_data.get('size')),
                        'company_location': sanitize_csv_field(company_data.get('location')),
                        'qualified_at': datetime.now().isoformat(),
                        'search_criteria': sanitize_csv_field(metadata.get('search_criteria', '') if metadata else ''),
                        'qualification_criteria': sanitize_csv_field(json.dumps(metadata.get('qualification_criteria', {})) if metadata else '')
                    }
                    
                    writer.writerow(row)
            
            logger.info(f"CSV file generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            raise


def test_output():
    """Test function: Generate test output."""
    print("=== LAYER 5 TEST: Output ===")
    
    # Mock qualified leads
    mock_leads = [
        {
            "id": "person1",
            "name": "John Doe",
            "title": "VP of Sales",
            "email": "john@example.com",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "company": {
                "id": "company1",
                "name": "Acme Corp",
                "description": "SaaS company",
                "domain": "acme.com",
                "website": "https://acme.com",
                "industry": "Technology",
                "size": "150",
                "location": "San Francisco, CA"
            },
            "_qualified": True,
            "_openrouter_response": "YES",
            "_prospeo_page": 1,
            "_processing_order": 1
        }
    ]
    
    metadata = {
        "search_criteria": "SaaS companies",
        "qualification_criteria": {"industry": "Technology", "min_employees": 50},
        "slack_user_id": "U123456",
        "slack_channel_id": "C123456",
        "slack_trigger_id": "1234567890.123456"
    }
    
    manager = OutputManager()
    
    # Test CSV generation
    try:
        csv_path = manager.generate_csv(mock_leads, metadata)
        print(f"CSV generated: {csv_path}")
        print(f"File exists: {os.path.exists(csv_path)}")
    except Exception as e:
        print(f"CSV generation error: {e}")
    
    # Test Supabase (will skip if not configured)
    try:
        count = manager.save_to_supabase(mock_leads, metadata)
        print(f"Supabase: {count} records inserted (or skipped if not configured)")
    except Exception as e:
        print(f"Supabase error: {e}")
    
    print("=" * 50)


if __name__ == "__main__":
    test_output()
