# SQL Schema Files - Consolidated into Migration

## Status: ✅ MIGRATED

All SQL schema files have been consolidated into a single versioned migration:
- **Migration file**: `supabase/migrations/20260123140000_create_lead_magnet_candidates.sql`
- **Applied**: 2026-01-23
- **Migration version**: `20260123201610`

## Old Files (No Longer Needed)

The following files were consolidated into the migration and can be deleted:
- `supabase_schema.sql` - Base table schema (Tab 1)
- `SUPABASE_SCHEMA_UPDATE.sql` - AI qualification columns (Tab 3)

Note: Tab 2 (adding `is_qualified` column) was also consolidated.

## Why This Change?

1. **Version Control**: Migrations provide proper version tracking
2. **Reproducibility**: Can recreate schema in any environment
3. **Team Collaboration**: Single source of truth for schema changes
4. **Deployment**: Easier to apply to production/staging environments

## Current Workflow

- **Python Code**: Uses Supabase Python client (no SQL files needed)
- **Database Schema**: Managed through Supabase migrations
- **Manual Changes**: Use Supabase Dashboard SQL Editor or create new migrations

## Future Schema Changes

To add new columns or modify the schema:
1. Create a new migration file in `supabase/migrations/`
2. Use format: `YYYYMMDDHHMMSS_description.sql`
3. Apply using Supabase MCP or CLI
