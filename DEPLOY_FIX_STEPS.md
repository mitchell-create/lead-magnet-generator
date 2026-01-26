# Deploy the Keywords Fix

## Status
✅ Fix is in the code (utils.py line 320-321)
❌ Railway still running old code (logs show list format)

## Steps to Deploy

### 1. Check if Changes Are Committed
```powershell
git status
```

**If utils.py or layer2_prospeo_client.py show as modified:**
- They need to be committed

### 2. Commit and Push
```powershell
git add utils.py layer2_prospeo_client.py
git commit -m "Fix Prospeo keywords filter format - use string not list"
git push
```

### 3. Wait for Railway Redeploy
- Railway should auto-detect push
- Wait 2-3 minutes
- Check Railway Dashboard → Deployments

### 4. Verify Fix Deployed
After Railway redeploys, check logs should show:
- `{'keywords': 'golf'}` (string, not list)

### 5. Test Again
```
/lead-magnet keywords=golf retailers | seniority=Founder
```

Should work now!
