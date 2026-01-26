# Location Filter Status

## Current Status: **DISABLED**

The `company_location` filter has been **temporarily disabled** because exact location format values are not available from Prospeo's API documentation.

## Why It's Disabled

Prospeo's API requires **exact location strings** that match their internal format. Without knowing the exact format (e.g., "United States" vs "US" vs "United States of America"), the API returns `INVALID_FILTERS` errors.

## How to Enable Location Filtering (When You Have Access)

1. **Log into Prospeo Dashboard**
2. **Build a search** with location filters enabled
3. **View the API Request** - Look for "API JSON", "View API Request", or similar button
4. **Copy the exact location values** from the API request (e.g., `"United States"`, `"California"`, etc.)
5. **Uncomment the location filter code** in `utils.py` (lines ~91-102)
6. **Use those exact values** in your search queries

## Current Workaround Options

### Option 1: Skip Location Filtering (Current)
- ✅ **Status**: Already implemented
- ✅ **Benefit**: No API errors, works immediately
- ⚠️ **Trade-off**: May fetch companies from all locations, then filter in post-processing

### Option 2: Post-Process Filtering
- Filter companies by location **after** fetching from Prospeo
- Use the `company_location` field in the response data
- Less efficient but works without knowing exact API format

### Option 3: Manual Testing
- Try common formats: `"United States"`, `"US"`, `"California"`, `"CA"`
- Test each format and see which ones work
- Document successful formats for future use

## Code Location

Location filter code is in:
- **`utils.py`**: Lines ~87-102 (currently commented out)
- **`test_new_features.py`**: No location filters in test (as expected)

## Impact on Current Workflow

✅ **No impact** - The workflow works fine without location filtering:
- Industry filtering still works (`company_industry`)
- Keywords are used for AI qualification (not API filtering)
- Seniority filtering works for person searches
- All other filters function normally

## Next Steps

1. ✅ **Current**: Location filtering is disabled - tests should run successfully
2. **Future**: When you have access to Prospeo dashboard, enable location filtering using the steps above
3. **Alternative**: If you need location filtering now, use post-processing filtering on the `company_location` field in company data
