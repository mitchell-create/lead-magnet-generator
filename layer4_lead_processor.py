"""
Layer 4: The Loop (Core Logic)
Processes leads in batches until exactly 50 qualified leads are found.
Saves ALL leads to Supabase first, then qualifies them.
Includes kill switch at 500 processed leads.
"""
import logging
from typing import List, Dict
import config
from layer2_prospeo_client import ProspeoClient
from layer3_ai_judge import AIQualifier
from layer5_output import OutputManager

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
        output_metadata: Dict = None
    ) -> Dict:
        """
        Process leads until target count of qualified leads is reached.
        
        Args:
            target_count: Target number of qualified leads (default from config)
            max_processed: Maximum number of leads to process (kill switch)
            filters: Prospeo API filters
            target_companies: List of target companies for qualification
            qualification_criteria: Criteria dictionary for qualification
        
        Returns:
            Dictionary with qualified_leads, stats, and metadata
        """
        target_count = target_count or config.TARGET_QUALIFIED_COUNT
        max_processed = max_processed or config.MAX_PROCESSED_LEADS
        
        qualified_leads = []
        total_processed = 0
        current_page = 1
        
        logger.info(f"Starting lead processing: target={target_count}, max_processed={max_processed}")
        
        while len(qualified_leads) < target_count and total_processed < max_processed:
            # Fetch page from Prospeo
            logger.info(f"Fetching page {current_page}...")
            try:
                result = self.prospeo_client.fetch_persons_page(
                    page=current_page,
                    limit=config.PROSPEO_BATCH_SIZE,
                    filters=filters
                )
                persons = result.get('data', [])
                
                if not persons:
                    logger.info(f"No more results after page {current_page - 1}")
                    break
                
                # Process each lead: Save first, then qualify
                for person in persons:
                    if total_processed >= max_processed:
                        logger.warning(f"Reached max processed limit ({max_processed})")
                        break
                    
                    if len(qualified_leads) >= target_count:
                        logger.info(f"Reached target count ({target_count})")
                        break
                    
                    total_processed += 1
                    
                    # Add metadata for tracking
                    person['_prospeo_page'] = current_page
                    person['_processing_order'] = total_processed
                    person['_qualified'] = False  # Default to unqualified
                    
                    # Save ALL leads to Supabase immediately (before qualification)
                    try:
                        if output_metadata:
                            self.output_manager.save_lead_to_supabase(
                                person, 
                                output_metadata, 
                                is_qualified=False
                            )
                            logger.debug(f"Saved lead {total_processed} to Supabase (before qualification)")
                    except Exception as e:
                        logger.warning(f"Error saving lead to Supabase: {e}")
                        # Continue even if save fails
                    
                    # Now qualify the lead
                    try:
                        is_qualified, response_text = self.ai_qualifier.qualify_person(
                            prospeo_person_response=person,
                            target_companies=target_companies or [],
                            qualification_criteria=qualification_criteria or {}
                        )
                        
                        # Update qualification status in Supabase
                        person['_qualified'] = is_qualified
                        person['_openrouter_response'] = response_text
                        
                        if is_qualified:
                            # Update the record in Supabase with qualification status
                            try:
                                if output_metadata:
                                    self.output_manager.update_lead_qualification_status(
                                        person, 
                                        output_metadata,
                                        is_qualified=True
                                    )
                            except Exception as e:
                                logger.warning(f"Error updating qualification status: {e}")
                            
                            qualified_leads.append(person)
                            logger.info(f"✅ Qualified lead {len(qualified_leads)}/{target_count}: {person.get('company', {}).get('name', 'Unknown')}")
                        else:
                            # Update record to mark as unqualified
                            try:
                                if output_metadata:
                                    self.output_manager.update_lead_qualification_status(
                                        person,
                                        output_metadata,
                                        is_qualified=False
                                    )
                            except Exception as e:
                                logger.warning(f"Error updating qualification status: {e}")
                        
                    except Exception as e:
                        logger.error(f"Error qualifying lead: {e}")
                        # Continue with next lead
                        continue
                
                # Check if we've reached our goals
                if len(qualified_leads) >= target_count:
                    break
                
                if total_processed >= max_processed:
                    logger.warning(f"Kill switch activated: processed {total_processed} leads, found {len(qualified_leads)} qualified")
                    break
                
                # Check if there are more pages
                meta = result.get('meta', {})
                if not meta.get('has_more', True):
                    logger.info(f"No more pages available")
                    break
                
                current_page += 1
                
            except Exception as e:
                logger.error(f"Error fetching page {current_page}: {e}")
                # Try next page or break
                current_page += 1
                if current_page > 100:  # Safety limit on pages
                    break
                continue
        
        stats = {
            'qualified_count': len(qualified_leads),
            'total_processed': total_processed,
            'pages_processed': current_page - 1,
            'target_reached': len(qualified_leads) >= target_count,
            'kill_switch_activated': total_processed >= max_processed
        }
        
        logger.info(f"Processing complete: {stats}")
        
        return {
            'qualified_leads': qualified_leads,
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
