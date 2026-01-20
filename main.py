"""
Main orchestrator for Lead Magnet Generator.
Integrates all layers and handles the complete workflow.
"""
import logging
import sys
from typing import Dict
from layer2_prospeo_client import ProspeoClient
from layer3_ai_judge import AIQualifier
from layer4_lead_processor import LeadProcessor
from layer5_output import OutputManager
from utils import build_prospeo_filters
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def send_slack_notification(message: str, channel_id: str = None):
    """
    Send notification to Slack (if Slack client is available).
    This is a placeholder - in production, use the Slack client from layer1.
    """
    logger.info(f"Slack notification: {message}")
    # TODO: Implement actual Slack notification using slack_bolt


def process_lead_search(trigger_data: Dict):
    """
    Main processing function triggered by Slack.
    
    Args:
        trigger_data: Dictionary containing parsed input and Slack metadata
    """
    try:
        parsed_input = trigger_data.get('parsed_input', {})
        
        # Extract data from parsed input
        target_companies = parsed_input.get('target_companies', [])
        qualification_criteria = parsed_input.get('qualification_criteria', {})
        search_keywords = parsed_input.get('search_keywords', [])
        
        # Build Prospeo filters
        prospeo_filters = build_prospeo_filters(parsed_input)
        
        logger.info(f"Processing lead search with filters: {prospeo_filters}")
        logger.info(f"Target companies: {target_companies}")
        logger.info(f"Qualification criteria: {qualification_criteria}")
        
        # Initialize processor
        processor = LeadProcessor()
        
        # Prepare metadata for output (needed during processing for saving leads)
        output_metadata = {
            'search_criteria': trigger_data.get('raw_text', ''),
            'qualification_criteria': qualification_criteria,
            'slack_user_id': trigger_data.get('slack_user_id'),
            'slack_channel_id': trigger_data.get('slack_channel_id'),
            'slack_trigger_id': trigger_data.get('slack_trigger_id')
        }
        
        # Process leads (saves all leads to Supabase, then qualifies)
        result = processor.process_until_qualified(
            target_count=config.TARGET_QUALIFIED_COUNT,
            max_processed=config.MAX_PROCESSED_LEADS,
            filters=prospeo_filters,
            target_companies=target_companies,
            qualification_criteria=qualification_criteria,
            output_metadata=output_metadata
        )
        
        stats = result['stats']
        qualified_leads = result['qualified_leads']
        
        # Note: All leads are already saved to Supabase during processing
        # Now just generate CSV with qualified leads
        output_manager = OutputManager()
        
        if qualified_leads:
            # Generate CSV (only qualified leads)
            try:
                csv_path = output_manager.generate_csv(qualified_leads, output_metadata)
                logger.info(f"Generated CSV: {csv_path}")
            except Exception as e:
                logger.error(f"Error generating CSV: {e}")
                csv_path = None
        else:
            logger.warning("No qualified leads found")
            csv_path = None
        
        # Log summary
        logger.info(f"Processing complete: {stats['total_processed']} total leads saved, {stats['qualified_count']} qualified")
        
        # Send completion notification
        message = f"""✅ Lead search completed!
        
📊 Results:
• Qualified Leads: {stats['qualified_count']}
• Total Processed: {stats['total_processed']}
• Pages Processed: {stats['pages_processed']}
• Target Reached: {'Yes' if stats['target_reached'] else 'No'}
• Kill Switch: {'Activated' if stats['kill_switch_activated'] else 'No'}

📁 Output:
• Supabase: {len(qualified_leads)} records saved
• CSV: {csv_path if csv_path else 'Not generated'}"""
        
        send_slack_notification(message, trigger_data.get('slack_channel_id'))
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing lead search: {e}", exc_info=True)
        error_message = f"❌ Error processing lead search: {str(e)}"
        send_slack_notification(error_message, trigger_data.get('slack_channel_id'))
        raise


def main():
    """Main entry point when running directly (for testing)."""
    print("=" * 60)
    print("Lead Magnet Generator - Main Orchestrator")
    print("=" * 60)
    
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease create a .env file with all required variables.")
        print("See .env.example for reference.")
        sys.exit(1)
    
    # Example trigger data for testing
    test_trigger_data = {
        'type': 'test',
        'parsed_input': {
            'target_companies': ['SaaS companies'],
            'qualification_criteria': {
                'industry': 'Technology',
                'min_employees': 50
            },
            'search_keywords': ['SaaS'],
            'raw_text': 'Test: SaaS companies with >50 employees'
        },
        'slack_user_id': 'test_user',
        'slack_channel_id': 'test_channel',
        'slack_trigger_id': 'test_123',
        'raw_text': 'Test: SaaS companies with >50 employees'
    }
    
    print("\nStarting lead search processing...")
    print("Note: For production, use the Slack listener (layer1_slack_listener.py)")
    print("-" * 60)
    
    try:
        result = process_lead_search(test_trigger_data)
        
        print("\n" + "=" * 60)
        print("Processing Complete!")
        print("=" * 60)
        print(f"Qualified Leads: {result['stats']['qualified_count']}")
        print(f"Total Processed: {result['stats']['total_processed']}")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        logger.exception("Unhandled exception")
        sys.exit(1)


if __name__ == "__main__":
    main()
