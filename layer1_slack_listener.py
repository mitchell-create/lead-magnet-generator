"""
Layer 1: Slack Listener
Receives triggers from Slack (slash commands or channel messages)
and extracts search criteria and qualification rules.

Force rebuild to install new dependencies.
"""
import hashlib
import hmac
import logging
import os
import sys
import threading
import time
from io import BytesIO
from urllib.parse import parse_qs
from flask import Flask, request, jsonify, g
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from utils import parse_natural_language_input
from validators import validate_slack_command
import config
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(token=config.SLACK_BOT_TOKEN, signing_secret=config.SLACK_SIGNING_SECRET)
handler = SlackRequestHandler(app)

# Flask app for webhook
flask_app = Flask(__name__)

# Store parsed triggers (in production, use a queue like Redis or database)
trigger_queue = []

_LEAD_MAGNET_HELP = """Please provide search criteria.

**New Format:**
`/lead-magnet industry=SaaS,Fintech | location=California | seniority=Founder,C-Suite | verified-email=true | size>50`

**Available Filters:**
- `keywords=` - **REQUIRED** - Keywords for company/product matching (comma-separated)
  - Note: Automatically converted to `company_keywords` for Prospeo API
  - Use `keywords=` NOT `company_keywords=`
- `industry=` - Company industries (comma-separated) - **Must match Prospeo exactly**
  - "General" is invalid -> use "General Retail"
  - All allowed values: https://prospeo.io/api-docs/enum/industries
  - Case-sensitive; use the exact spelling from that list
- `location=` - Locations (comma-separated) - Recommended
- `seniority=` - Seniority levels (comma-separated) - Recommended
  - Valid values: Founder/Owner, C-Suite, Partner, Vice President, Head, Director, Manager, Senior, Intern, Entry
- `our-company-details=` - Your company description for AI context - Recommended

**Template:**
`/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"`

**Example:**
`/lead-magnet keywords=golf pro shops | industry=General Retail | seniority=Founder,C-Suite | our-company-details="We sell premium golf equipment"`

**Note:** Emails are automatically enriched AFTER qualification (no verified-email parameter needed)."""


def _verify_slack_signature(body: bytes, timestamp: str, signature: str) -> bool:
    """Verify Slack request using X-Slack-Signature and X-Slack-Request-Timestamp."""
    if not body or not timestamp or not signature or not getattr(config, "SLACK_SIGNING_SECRET", None):
        return False
    try:
        if abs(time.time() - int(timestamp)) > 60 * 5:
            return False
        sig_basestring = f"v0:{timestamp}:{body.decode('utf-8', errors='replace')}"
        my_sig = "v0=" + hmac.new(
            config.SLACK_SIGNING_SECRET.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(my_sig, signature)
    except Exception:
        return False


def _post_to_response_url(response_url: str, text: str) -> None:
    """Post a message to Slack's response_url (e.g. for validation errors from background thread)."""
    if not response_url:
        return
    try:
        requests.post(response_url, json={"text": text}, timeout=5)
    except Exception as e:
        logger.warning("Failed to post to response_url: %s", e)


def _run_lead_search_background(search_text: str, command_payload: dict) -> None:
    """Runs in a background thread: parse, validate, then process_lead_search. Post errors to response_url."""
    response_url = (command_payload or {}).get("response_url")
    try:
        parsed_input = parse_natural_language_input(search_text)
        is_valid, error_message = validate_slack_command(parsed_input)
        if not is_valid:
            logger.warning("Invalid command received: %s", error_message)
            _post_to_response_url(response_url, error_message)
            return
        logger.info("Slash command (background). Parsed input: %s", parsed_input)
        trigger_data = {
            "type": "slash_command",
            "parsed_input": parsed_input,
            "slack_user_id": (command_payload or {}).get("user_id"),
            "slack_channel_id": (command_payload or {}).get("channel_id"),
            "slack_trigger_id": (command_payload or {}).get("trigger_id"),
            "raw_text": search_text,
        }
        trigger_queue.append(trigger_data)
        from main import process_lead_search
        process_lead_search(trigger_data)
    except Exception as e:
        logger.error("Error processing lead search: %s", e, exc_info=True)
        _post_to_response_url(response_url, f"Error processing lead search: {e}")


@app.command("/lead-magnet")
def handle_slash_command(ack, respond, command):
    """
    Handle Slack slash command: /lead-magnet <criteria>
    """
    try:
        ack()  # Acknowledge the command immediately so Slack gets 200 within 3s
    except Exception as e:
        logger.error(f"ack() failed: {e}", exc_info=True)
        return

    # Use text from raw POST body when set in slack_commands() so multi-word values (e.g. "General Retail") are preserved.
    # Slack sends the full string; Bolt’s command["text"] can sometimes expose only the first token.
    # Do not use Flask g here: Bolt may run this in a thread without app context.
    search_text = (command.get("text") or "").strip()

    if not search_text:
        respond("""Please provide search criteria. 

**New Format:**
`/lead-magnet industry=SaaS,Fintech | location=California | seniority=Founder,C-Suite | verified-email=true | size>50`

**Available Filters:**
- `keywords=` - **REQUIRED** - Keywords for company/product matching (comma-separated)
  - Note: Automatically converted to `company_keywords` for Prospeo API
  - Use `keywords=` NOT `company_keywords=`
- `industry=` - Company industries (comma-separated) - **Must match Prospeo exactly**
  - ❌ \"General\" is invalid → ✅ use \"General Retail\"
  - All allowed values: https://prospeo.io/api-docs/enum/industries
  - Case-sensitive; use the exact spelling from that list
- `location=` - Locations (comma-separated) - Recommended
- `seniority=` - Seniority levels (comma-separated) - Recommended
  - Valid values: Founder/Owner, C-Suite, Partner, Vice President, Head, Director, Manager, Senior, Intern, Entry
- `our-company-details=` - Your company description for AI context - Recommended

**Template:**
`/lead-magnet keywords={{keywords}} | industry={{industry}} | location={{location}} | seniority={{seniority}} | our-company-details="{{our-company-details}}"`

**Example:**
`/lead-magnet keywords=golf pro shops | industry=General Retail | seniority=Founder,C-Suite | our-company-details="We sell premium golf equipment"`

**Note:** Emails are automatically enriched AFTER qualification (no verified-email parameter needed).""")
        return
    
    # Parse the input
    parsed_input = parse_natural_language_input(search_text)
    
    # Validate the command (industry and seniority values)
    is_valid, error_message = validate_slack_command(parsed_input)
    
    if not is_valid:
        respond(error_message)
        logger.warning(f"Invalid command received: {error_message}")
        return
    
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
    
    # Respond to user immediately so Slack gets a response within 3 seconds (avoids dispatch_failed)
    respond(f"✅ Lead search initiated! Processing leads in the background. Results will be saved to Supabase.")

    # Run the long-running search in a background thread so we return quickly to Slack
    def run_lead_search():
        try:
            from main import process_lead_search
            process_lead_search(trigger_data)
        except Exception as e:
            logger.error(f"Error processing lead search: {e}", exc_info=True)

    thread = threading.Thread(target=run_lead_search, daemon=True)
    thread.start()


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
    
    # Validate the command (industry and seniority values)
    is_valid, error_message = validate_slack_command(parsed_input)
    
    if not is_valid:
        say(error_message)
        logger.warning(f"Invalid command received: {error_message}")
        return
    
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
        logger.error(f"Error processing lead search: {e}", exc_info=True)
        
        # Check if it's a Prospeo API error with user-friendly message
        error_str = str(e)
        if "filter_error" in error_str or "INVALID_FILTERS" in error_str:
            # Try to extract Prospeo's error message
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                try:
                    error_detail = e.response.json()
                    if error_detail.get('filter_error'):
                        say(
                            f"❌ **Prospeo API Error:** {error_detail.get('filter_error')}\n\n"
                            f"**How to fix:**\n"
                            f"• Check the exact filter values in Prospeo dashboard\n"
                            f"• Use the 'API JSON' builder in dashboard to see exact enum values\n"
                            f"• Industry values are case-sensitive and must match exactly"
                        )
                        return
                except:
                    pass
        
        # Generic error message
        say(f"❌ Error processing leads: {str(e)}\n\nIf this is a filter error, check Prospeo dashboard 'API JSON' builder for exact values.")


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack Events API requests."""
    return handler.handle(request)


@flask_app.route("/slack/commands", methods=["POST"])
def slack_commands():
    """
    Handle Slack Slash Commands. Returns HTTP 200 immediately to avoid dispatch_failed.
    Bypasses Bolt for this route so no framework latency; verifies signature and responds in-process.
    """
    logger.info("[/slack/commands] fast path")
    raw = request.get_data(as_text=False)
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    if not _verify_slack_signature(raw, timestamp, signature):
        return "", 403

    if not raw:
        return jsonify({"text": _LEAD_MAGNET_HELP}), 200

    try:
        params = parse_qs(raw.decode("utf-8", errors="replace"), keep_blank_values=True)
    except Exception as e:
        logger.warning("Could not parse slash command body: %s", e)
        return jsonify({"text": "Unable to parse request."}), 200

    text = (params.get("text") or [""])[0].strip()
    response_url = (params.get("response_url") or [""])[0]
    user_id = (params.get("user_id") or [""])[0]
    channel_id = (params.get("channel_id") or [""])[0]
    trigger_id = (params.get("trigger_id") or [""])[0]

    if not text:
        return jsonify({"text": _LEAD_MAGNET_HELP}), 200

    payload = {
        "response_url": response_url,
        "user_id": user_id,
        "channel_id": channel_id,
        "trigger_id": trigger_id,
    }
    threading.Thread(
        target=_run_lead_search_background,
        args=(text, payload),
        daemon=True,
    ).start()
    return (
        jsonify({
            "text": "Lead search initiated. Processing in the background. Results will be saved to Supabase."
        }),
        200,
    )


@flask_app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "queue_size": len(trigger_queue)})


def run_server():
    """Run the Flask server to listen for Slack events."""
    # Railway injects PORT and routes traffic to it; we must listen on that port.
    # Locally, fall back to SLACK_PORT (3000) when PORT is unset.
    port = int(os.getenv('PORT', config.SLACK_PORT))
    
    logger.info(f"PORT env: {os.getenv('PORT')} -> using port {port}")
    logger.info(f"Starting Slack listener on port {port}")
    # Force Railway rebuild - break cache for dependency installation
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
