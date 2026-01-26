# Using Keywords + Filters Together

## ✅ You CAN Use Both!

**Keywords and filters work together, but serve different purposes:**

### How They Work

**Prospeo Filters (industry, location, seniority, etc.):**
- ✅ Sent to Prospeo API
- ✅ Used to narrow the search
- ✅ Reduce number of leads fetched
- ✅ Examples: `industry=Retail`, `seniority=Founder`, `location=California`

**Keywords:**
- ❌ NOT sent to Prospeo (they don't support keywords filter)
- ✅ Used by AI for qualification
- ✅ Filters the leads AFTER fetching
- ✅ Examples: `keywords=golf retailers`, `keywords=outdoor gear`

### Example Commands

**Using both together:**
```
/lead-magnet keywords=golf retailers | industry=Retail | seniority=Founder
```

**How this works:**
1. Prospeo searches for: `industry=Retail` + `seniority=Founder`
2. Gets results matching those filters
3. AI qualifies each lead: "Does this company match 'golf retailers'?"
4. Only qualified leads are saved

**Keywords only:**
```
/lead-magnet keywords=golf retailers
```

**How this works:**
1. Prospeo searches broadly (no filters)
2. Gets results
3. AI qualifies each lead: "Does this company match 'golf retailers'?"
4. Only qualified leads are saved

**Filters only:**
```
/lead-magnet industry=Retail | seniority=Founder
```

**How this works:**
1. Prospeo searches for: `industry=Retail` + `seniority=Founder`
2. Gets results matching those filters
3. AI qualifies based on your qualification criteria (if any)
4. All matching leads are saved (unless AI disqualifies)

---

## Summary

✅ **Keywords** → Used by AI, not Prospeo  
✅ **Other filters** → Used by Prospeo, not AI  
✅ **You can use both together** → Prospeo narrows search, AI filters by keywords  

They complement each other!
