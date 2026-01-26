# Quick Start Guide

## 1. Initial Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Fill in your API keys in `.env`:
   - `PROSPEO_API_KEY` - Get from Prospeo dashboard
   - `OPENROUTER_API_KEY` - Get from OpenRouter dashboard
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon key
   - `SLACK_BOT_TOKEN` - Your Slack bot token
   - `SLACK_SIGNING_SECRET` - Your Slack app signing secret

### Create Supabase Table
1. Go to your Supabase SQL Editor
2. Run the SQL from `supabase_schema.sql`

## 2. Testing Each Layer

### Test Layer 1: Slack Listener
```bash
python layer1_slack_listener.py
```
This will test the natural language parser with sample inputs.

### Test Layer 2: Prospeo Connection
```bash
python layer2_prospeo_client.py
```
This will fetch the first page of leads from Prospeo.

### Test Layer 3: AI Judge
```bash
python layer3_ai_judge.py
```
This will test the AI qualification on a mock lead.

### Test Layer 4: Processing Loop
```bash
python layer4_lead_processor.py
```
This will run the full processing loop (with small test limits).

### Test Layer 5: Output
```bash
python layer5_output.py
```
This will test CSV generation and Supabase insertion.

## 3. Running the Full System

### Option A: Run Main Script (Testing)
```bash
python main.py
```
This runs the full pipeline with test data.

### Option B: Start Slack Listener (Production)
```bash
python layer1_slack_listener.py --server
```
Or use the Flask app directly:
```bash
python -m flask run --port=3000
```

## 4. Using the System

### Via Slack Slash Command
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees, Industry=Technology
```

### Via Channel Message
Post in your configured channel:
```
Find leads: SaaS companies with >50 employees in Technology industry
```

## 5. Output Files

- **Supabase**: Check your `lead_magnet_candidates` table
- **CSV**: Generated in `./output/` directory with timestamps

## 6. Troubleshooting

### API Key Errors
- Verify all keys are set in `.env`
- Check that `.env` file is in the project root

### Prospeo API Errors
- Verify your API key is valid
- Check Prospeo API documentation for filter format
- Adjust filters in `utils.py` if needed

### OpenRouter Errors
- Verify `OPENROUTER_API_KEY` is set in `.env` (or Railway) and is valid in the OpenRouter dashboard.
- Check model name is correct (default: `openai/gpt-oss-20b` via `OPENROUTER_MODEL`).
- Verify you have credits in OpenRouter.

**401 Unauthorized and “enrichments using OpenRouter”:**  
Supabase does **not** call OpenRouter. This app calls OpenRouter only in **layer3 (AI Judge)** for wholesale/keyword checks. “Enrichment” here means **Prospeo email/contact enrichment**, not OpenRouter. If you see 401 in the context of OpenRouter:
- Check **app logs** (e.g. Railway, local console) for the failing HTTP request; that’s where 401 will appear.
- Ensure the env that runs the app has the correct `OPENROUTER_API_KEY` and that the key is not revoked or expired.

### Supabase Errors
- Verify table schema matches `supabase_schema.sql`
- Check your Supabase URL and key
- Ensure RLS policies allow inserts (if enabled)

## 7. Next Steps

1. Customize the qualification prompt template in `utils.py` → `format_qualification_template()`
2. Adjust batch sizes and limits in `config.py`
3. Set up Slack app and configure webhook URLs
4. Deploy to a server with public IP for Slack webhooks
5. Monitor logs for errors and adjust as needed

