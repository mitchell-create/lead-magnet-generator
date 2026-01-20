# Fix: Prospeo API 400 Bad Request Error

## Problem

Prospeo API is rejecting requests with 400 Bad Request because the filter format is incorrect.

**Invalid filters being sent:**
- `company_name` - Not a valid Prospeo filter field
- `company_size_min` - Not a valid Prospeo filter field

## Solution

Updated `build_prospeo_filters()` to:
1. ✅ Use only `keywords` and `industry` (valid Prospeo filters)
2. ✅ Convert `target_companies` to `keywords` instead of `company_name`
3. ✅ Remove `company_size_min` (Prospeo doesn't support size filtering in API)
4. ✅ Company size filtering happens in AI qualification step instead

## What Changed

**Before:**
```python
filters = {
    'company_name': ['Software companies'],  # ❌ Invalid
    'company_size_min': 10  # ❌ Invalid
}
```

**After:**
```python
filters = {
    'keywords': ['software', 'companies'],  # ✅ Valid
    'industry': 'Technology'  # ✅ Valid (if provided)
}
```

## Next Steps

1. **Commit and push the fix:**
   ```powershell
   git add utils.py layer2_prospeo_client.py
   git commit -m "Fix: Use only valid Prospeo filter fields (keywords, industry)"
   git push
   ```

2. **Wait for Railway redeploy** (1-2 minutes)

3. **Test again in Slack:**
   ```
   /lead-magnet Target: SaaS companies | Criteria: Size>10
   ```

4. **Check Railway logs** - should see successful API calls now!

---

## Note

- ✅ Company size filtering (`Size>10`) will still work, but it's done by AI qualification, not Prospeo API filtering
- ✅ This is actually better because we get more leads to evaluate, then filter intelligently with AI
