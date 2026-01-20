"""
Layer 5: Output
Saves qualified leads to Supabase and generates CSV file.
"""
import logging
import csv
import json
import os
from datetime import datetime
from typing import List, Dict
from supabase import create_client, Client
import config
from utils import extract_person_and_company_data, sanitize_csv_field

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
    
    def update_lead_qualification_status(self, lead: Dict, metadata: Dict, is_qualified: bool) -> bool:
        """
        Update qualification status for a lead already in Supabase.
        
        Args:
            lead: Lead dictionary with metadata
            metadata: Metadata including Slack info
            is_qualified: New qualification status
        
        Returns:
            True if updated successfully
        """
        if not self.supabase:
            return False
        
        # Use slack_trigger_id + processing_order to identify the record
        slack_trigger_id = metadata.get('slack_trigger_id')
        processing_order = lead.get('_processing_order')
        
        if not slack_trigger_id or not processing_order:
            logger.warning("Cannot update qualification status: missing trigger_id or processing_order")
            return False
        
        update_data = {
            "is_qualified": is_qualified,
            "openrouter_response": lead.get('_openrouter_response', '')
        }
        
        if is_qualified:
            from datetime import datetime
            update_data["qualified_at"] = datetime.now().isoformat()
        
        try:
            response = self.supabase.table("lead_magnet_candidates")\
                .update(update_data)\
                .eq("slack_trigger_id", slack_trigger_id)\
                .eq("processing_order", processing_order)\
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
