# Prospeo Keywords Filter Issue

## Error
```
Invalid value 'golf' for filter 'keywords'
```

This suggests Prospeo doesn't accept `keywords` as a filter at all, or it needs a different format.

## Possible Solutions

### Option 1: Remove Keywords Filter
If Prospeo doesn't support `keywords`, we might need to:
- Remove it from filters
- Use other supported filters (industry, location, etc.)
- Do keyword filtering in post-processing

### Option 2: Different Keywords Format
Maybe keywords need to be:
- In a different field
- Part of a search query parameter
- Combined with other filters

### Option 3: Use Company Search Instead
Maybe keywords should be used in a company search endpoint, not person search.

## Next Steps

Need to check Prospeo API documentation to see:
1. What filters are actually supported for search-person
2. If keywords is a valid filter
3. What the correct format is
