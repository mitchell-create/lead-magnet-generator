-- Migration: Create lead_magnet_candidates table with all columns and indexes
-- This migration consolidates the initial schema and all subsequent updates
-- Created: 2026-01-23

-- ============================================================================
-- TABLE CREATION
-- ============================================================================

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
    is_qualified BOOLEAN DEFAULT FALSE,
    qualified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    qualification_criteria TEXT,
    search_criteria TEXT,
    prospeo_page_number INTEGER,
    processing_order INTEGER,
    
    -- Slack Metadata
    slack_user_id TEXT,
    slack_channel_id TEXT,
    slack_trigger_id TEXT,
    
    -- Full JSON (for flexibility)
    raw_prospeo_data JSONB,
    openrouter_response TEXT,
    
    -- AI Check Results columns
    wholesale_partner_check BOOLEAN,
    wholesale_partner_response TEXT,
    keyword_match_check BOOLEAN,
    keyword_match_response TEXT,
    
    -- Arrays for structured AI output (reusable for future keyword matching)
    product_categories TEXT[],
    market_segments TEXT[],
    
    -- Scraped content columns
    company_scraped_content TEXT,
    scraped_content_date TIMESTAMP WITH TIME ZONE,
    last_scraped_at TIMESTAMP WITH TIME ZONE
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Basic indexes from initial schema
CREATE INDEX IF NOT EXISTS idx_lead_magnet_created_at ON lead_magnet_candidates(created_at);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_company_domain ON lead_magnet_candidates(company_domain);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_user ON lead_magnet_candidates(slack_user_id);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_is_qualified ON lead_magnet_candidates(is_qualified);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_trigger ON lead_magnet_candidates(slack_trigger_id);

-- Additional indexes for AI qualification and lookups
CREATE INDEX IF NOT EXISTS idx_company_id ON lead_magnet_candidates(company_id);
CREATE INDEX IF NOT EXISTS idx_company_name ON lead_magnet_candidates(company_name);
CREATE INDEX IF NOT EXISTS idx_wholesale_partner_check ON lead_magnet_candidates(wholesale_partner_check);
CREATE INDEX IF NOT EXISTS idx_keyword_match_check ON lead_magnet_candidates(keyword_match_check);
CREATE INDEX IF NOT EXISTS idx_person_id ON lead_magnet_candidates(person_id);

-- GIN index for array searches (allows fast searches on product_categories array)
CREATE INDEX IF NOT EXISTS idx_product_categories ON lead_magnet_candidates USING GIN(product_categories);

-- ============================================================================
-- NOTES
-- ============================================================================
-- 
-- This migration creates the complete lead_magnet_candidates table with:
-- 1. Base schema (person and company data from Prospeo)
-- 2. Qualification metadata (is_qualified flag and timestamps)
-- 3. Slack integration fields
-- 4. AI qualification results (wholesale partner check, keyword matching)
-- 5. Structured arrays for product categories and market segments
-- 6. Web scraping fields for company content
-- 
-- All indexes are created for optimal query performance on common lookups.
-- The qualified_at column is nullable by default (no NOT NULL constraint).
--
