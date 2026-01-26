# Prospeo Keywords Filter - Confirmed

## ❌ No Keywords Filter in Prospeo API

**Confirmed:** Prospeo's `search-person` endpoint does NOT support a `keywords` filter.

### What Prospeo Supports
- ✅ `company_industry` - Specific industries
- ✅ `company_location` - Locations
- ✅ `person_seniority` - Seniority levels
- ✅ `person_location` - Person locations
- ✅ `company_technology` - Tech stack
- ✅ `company_funding` - Funding info
- ✅ `only_verified_email` - Email verification
- ❌ **`keywords` - NOT SUPPORTED**

### Why?
Prospeo uses **structured, predefined filters** (ENUMs), not free-text keyword search. The API will reject any attempt to use `keywords` as a filter.

---

## ✅ Our Solution (Best Available)

Since Prospeo doesn't support keywords:

1. **Use structured filters** for Prospeo search:
   - `industry=Retail`
   - `seniority=Founder`
   - `location=California`

2. **Use keywords for AI qualification**:
   - Keywords filter results AFTER fetching
   - AI checks company descriptions/websites
   - More flexible than Prospeo filters

### How It Works
```
/lead-magnet keywords=golf retailers | industry=Retail
```

1. Prospeo: Search by `industry=Retail` ✅
2. Get results from Prospeo
3. AI: Filter by `keywords=golf retailers` ✅
4. Save qualified leads

---

## Alternative Approaches (Not Recommended)

### Option 1: Map Keywords to Industry
- Could map "golf retailers" → `industry=Retail`
- But loses specificity (too broad)

### Option 2: Filter Client-Side
- Fetch all results, filter by `company.keywords` field
- But Prospeo returns `keywords` field, not a filter
- Would still need AI or manual filtering

### Option 3: Use Prospeo UI
- Dashboard might have keyword search
- But not available in API

---

## Conclusion

✅ **Our current approach is the best solution:**
- Prospeo filters → Narrow search (industry, seniority, location)
- AI qualification → Filter by keywords (flexible, accurate)

This gives you the best of both worlds!
