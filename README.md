# Lead Magnet Generator

Automated lead qualification tool that fetches leads from Prospeo, qualifies them using AI (OpenRouter), and outputs to Supabase and CSV.

## Architecture

The system is built in 5 layers:
1. **Slack Listener** - Receives triggers via Slack (slash commands or channel messages)
2. **Prospeo Client** - Fetches leads in batches with pagination
3. **AI Judge** - Qualifies leads using OpenRouter AI
4. **Lead Processor** - Main loop that processes until 50 qualified leads found
5. **Output** - Saves to Supabase and generates CSV

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`
   - Fill in all required API keys and configuration

3. **Create Supabase Table:**
   - Run `supabase_schema.sql` in your Supabase SQL editor

4. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

### Via Slash Command:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees, Industry=Technology
```

### Via Channel Message:
Simply mention your criteria in the configured channel:
```
Find leads: SaaS companies with >50 employees in Technology industry
```

## Configuration

Edit `config.py` to adjust:
- Target qualified count (default: 50)
- Max processed leads (default: 500)
- Batch size (default: 25)
- OpenRouter model

## Output

- **Supabase:** All qualified leads are saved to `lead_magnet_candidates` table
- **CSV:** Generated in `./output/` directory with timestamp

## Safety Features

- Kill switch: Stops after processing 500 leads (prevents excessive API costs)
- Error notifications sent to Slack
- Partial results saved on errors
