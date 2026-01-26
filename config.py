"""
Configuration file for Lead Magnet Generator.
Loads environment variables and defines constants.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

# Configuration Constants
TARGET_QUALIFIED_COUNT = 50
MAX_PROCESSED_LEADS = 500
PROSPEO_BATCH_SIZE = 25
# Only gpt-oss-20b. Override via OPENROUTER_MODEL if needed (must be openai/gpt-oss-20b or equivalent).
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Prospeo API Configuration
PROSPEO_BASE_URL = "https://api.prospeo.io"
PROSPEO_SEARCH_PERSON_ENDPOINT = f"{PROSPEO_BASE_URL}/search-person"
PROSPEO_SEARCH_COMPANY_ENDPOINT = f"{PROSPEO_BASE_URL}/search-company"

# Flask/Slack Configuration
SLACK_PORT = int(os.getenv("SLACK_PORT", "3000"))
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "")  # Optional: specific channel ID to listen to

# CSV Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
CSV_FILENAME_PREFIX = "qualified_leads"

# Validate required environment variables
def validate_config():
    """Validate that all required configuration is present."""
    required_vars = {
        "PROSPEO_API_KEY": PROSPEO_API_KEY,
        "OPENROUTER_API_KEY": OPENROUTER_API_KEY,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
        "SLACK_SIGNING_SECRET": SLACK_SIGNING_SECRET,
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return True
