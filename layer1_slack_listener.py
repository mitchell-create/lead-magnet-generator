"""
Layer 1: Slack Listener
Receives triggers from Slack (slash commands or channel messages)
and extracts search criteria and qualification rules.

Force rebuild to install new dependencies.
"""
import logging
import os
import sys
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from utils import parse_natural_language_input
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)
handler = SlackRequestHandler(app)

# Flask app for webhook
flask_app = Flask(__name__)

# Store parsed triggers (in production, use a queue like Redis or database)
trigger_queue = []


@app.command("/lead-magnet")
def handle_slash_command(ack, respond, command):
    """
    Handle Slack slash command: /lead-magnet <criteria>
    """
    ack()  # Acknowledge the command immediately
    
    # Extract search criteria from command text
    search_text = command.get('text', '')
    
    if not search_text:
        respond("""Please provide search criteria. 

**New Format:**
`/lead-magnet industry=SaaS,Fintech | location=California | seniority=Founder,C-Suite | verified-email=true | size>50`

**Available Filters:**
- `industry=` - Company industries (comma-separated)
- `location=` - Locations (comma-separated)  
- `seniority=` - Seniority levels (comma-separated)
- `keywords=` - Keywords (comma-separated)
- `verified-email=` - true/false

**Example:**
`/lead-magnet keywords=golf pro shops | seniority=Founder | location=United States`""")
        return
    
    # Parse the input
    parsed_input = parse_natural_language_input(search_text)
    
    logger.info(f"Slash command received. Parsed input: {parsed_input}")
    print(f"=== LAYER 1 TEST: Parsed Input ===")
    print(f"Search Criteria: {parsed_input}")
    print(f"Target Companies: {parsed_input.get('target_companies', [])}")
    print(f"Qualification Criteria: {parsed_input.get('qualification_criteria', {})}")
    print("=" * 50)
    
    # Add metadata
    trigger_data = {
        'type': 'slash_command',
        'parsed_input': parsed_input,
        'slack_user_id': command.get('user_id'),
        'slack_channel_id': command.get('channel_id'),
        'slack_trigger_id': command.get('trigger_id'),
        'raw_text': search_text
    }
    
    # Add to queue for processing
    trigger_queue.append(trigger_data)
    
    # Respond to user
    respond(f"✅ Lead search initiated! Processing leads based on: {search_text}")
    
    # Trigger processing (in production, this would be async)
    try:
        from main import process_lead_search
        process_lead_search(trigger_data)
    except Exception as e:
        logger.error(f"Error processing lead search: {e}")
        respond(f"❌ Error processing leads: {str(e)}")


@app.event("message")
def handle_message_events(event, say):
    """
    Handle message events in channels.
    Only processes messages that look like lead search requests.
    """
    # Skip bot messages and messages in threads
    if event.get('subtype') or event.get('thread_ts'):
        return
    
    # Optionally filter by channel
    if config.SLACK_CHANNEL_ID and event.get('channel') != config.SLACK_CHANNEL_ID:
        return
    
    message_text = event.get('text', '')
    
    # Check if message looks like a lead search request
    # Keywords that indicate a lead search
    trigger_keywords = ['find leads', 'lead search', 'get leads', 'search for leads', 
                       'qualify leads', 'lead magnet']
    
    if not any(keyword in message_text.lower() for keyword in trigger_keywords):
        return
    
    # Parse the input
    parsed_input = parse_natural_language_input(message_text)
    
    logger.info(f"Message event received. Parsed input: {parsed_input}")
    print(f"=== LAYER 1 TEST: Message Event ===")
    print(f"Search Criteria: {parsed_input}")
    print(f"Target Companies: {parsed_input.get('target_companies', [])}")
    print(f"Qualification Criteria: {parsed_input.get('qualification_criteria', {})}")
    print("=" * 50)
    
    # Add metadata
    trigger_data = {
        'type': 'message',
        'parsed_input': parsed_input,
        'slack_user_id': event.get('user'),
        'slack_channel_id': event.get('channel'),
        'slack_trigger_id': event.get('ts'),  # Message timestamp as trigger ID
        'raw_text': message_text
    }
    
    # Add to queue
    trigger_queue.append(trigger_data)
    
    # Acknowledge in channel
    say(f"✅ Lead search initiated! Processing leads based on your criteria.")
    
    # Trigger processing
    try:
        from main import process_lead_search
        process_lead_search(trigger_data)
    except Exception as e:
        logger.error(f"Error processing lead search: {e}")
        say(f"❌ Error processing leads: {str(e)}")


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack Events API requests."""
    return handler.handle(request)


@flask_app.route("/slack/commands", methods=["POST"])
def slack_commands():
    """Handle Slack Slash Commands."""
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "queue_size": len(trigger_queue)})


def run_server():
    """Run the Flask server to listen for Slack events."""
    # Railway sets PORT environment variable, but we want to use SLACK_PORT (3000)
    # Prefer SLACK_PORT since that's what Railway networking is configured for
    railway_port = os.getenv('PORT')
    slack_port = config.SLACK_PORT
    
    logger.info(f"PORT env var: {railway_port}")
    logger.info(f"SLACK_PORT config: {slack_port}")
    
    # Use SLACK_PORT (3000) - this matches Railway networking config
    port = slack_port
    
    logger.info(f"Using port: {port}")
    logger.info(f"Starting Slack listener on port {port}")
    # Bind to 0.0.0.0 to be accessible from outside container
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    import sys
    
    # Check if --server flag is passed or if running in production
    if "--server" in sys.argv or os.getenv("RAILWAY_ENVIRONMENT"):
        # Start the server
        run_server()
    else:
        # Test the parser (for local testing)
        print("Testing Layer 1: Slack Listener")
        print("=" * 50)
        
        test_inputs = [
            "Target: SaaS companies | Criteria: Size>50 employees, Industry=Technology",
            "Find leads: SaaS companies with >50 employees",
            "https://linkedin.com/company/acme-corp | Criteria: Size>100",
        ]
        
        for test_input in test_inputs:
            print(f"\nInput: {test_input}")
            parsed = parse_natural_language_input(test_input)
            print(f"Parsed: {parsed}\n")
        
        print("\nTo start the server, run: python layer1_slack_listener.py --server")
