-- Supabase Table Schema for Lead Magnet Candidates
-- Run this SQL in your Supabase SQL editor to create the table

CREATE TABLE IF NOT EXISTS lead_magnet_candidates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Person Data (from Prospeo)
    person_id TEXT,
    person_name TEXT,
    person_email TEXT,
    person_title TEXT,
    person_linkedin_url TEXT,
    
    -- Company Data
    company_id TEXT,
    company_name TEXT,
    company_description TEXT,
    company_domain TEXT,
    company_website TEXT,
    company_industry TEXT,
    company_size TEXT,
    company_location TEXT,
    
    -- Qualification Metadata
    is_qualified BOOLEAN DEFAULT FALSE,  -- Whether AI qualified this lead
    qualified_at TIMESTAMP WITH TIME ZONE,  -- When qualification happened (nullable if not qualified)
    qualification_criteria TEXT,  -- JSON of criteria used
    search_criteria TEXT,  -- Original search input
    prospeo_page_number INTEGER,
    processing_order INTEGER,  -- Order in which this lead was processed
    
    -- Slack Metadata
    slack_user_id TEXT,
    slack_channel_id TEXT,
    slack_trigger_id TEXT,
    
    -- Full JSON (for flexibility)
    raw_prospeo_data JSONB,
    openrouter_response TEXT
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_lead_magnet_created_at ON lead_magnet_candidates(created_at);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_company_domain ON lead_magnet_candidates(company_domain);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_user ON lead_magnet_candidates(slack_user_id);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_is_qualified ON lead_magnet_candidates(is_qualified);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_trigger ON lead_magnet_candidates(slack_trigger_id);