# Supabase Migrations

This directory contains database migrations for the lead-magnet-generator project.

## Migration Files

- `20260123140000_create_lead_magnet_candidates.sql` - Initial schema creation with all columns and indexes

## How to Apply Migrations

### Option 1: Using Supabase CLI (Recommended)

If you have the Supabase CLI installed:

```bash
# Link to your project
supabase link --project-ref utdwvqfnzkcysdsbsvwv

# Apply migrations
supabase db push
```

### Option 2: Using Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy the contents of the migration file
4. Paste and run the SQL

### Option 3: Using MCP (Model Context Protocol)

The migration can be applied programmatically using the Supabase MCP server.

## Migration History

- **2026-01-23**: Initial migration consolidating all three SQL tabs into a single versioned migration

## Notes

- All migrations use `IF NOT EXISTS` clauses for idempotency
- The `qualified_at` column is nullable (no NOT NULL constraint)
- All indexes are created for optimal query performance
