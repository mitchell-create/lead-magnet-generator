-- Migration: Add is_qualified column and update indexes
-- Run this SQL in Supabase SQL Editor if the table already exists

-- Add is_qualified column if it doesn't exist
ALTER TABLE lead_magnet_candidates 
ADD COLUMN IF NOT EXISTS is_qualified BOOLEAN DEFAULT FALSE;

-- Make qualified_at nullable (in case it doesn't exist or is not nullable)
ALTER TABLE lead_magnet_candidates 
ALTER COLUMN qualified_at DROP NOT NULL;

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_lead_magnet_is_qualified ON lead_magnet_candidates(is_qualified);
CREATE INDEX IF NOT EXISTS idx_lead_magnet_slack_trigger ON lead_magnet_candidates(slack_trigger_id);

-- Verify the update
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'lead_magnet_candidates'
ORDER BY ordinal_position;
