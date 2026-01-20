# Next Steps: Testing & Verification

## ✅ What's Done
- ✅ Code deployed to Railway
- ✅ Health endpoint working
- ✅ Slack URLs configured
- ✅ Event Subscriptions set up
- ✅ Slash Commands set up

---

## Step 1: Test Slack Integration

### Test Slash Command
1. Open your Slack workspace
2. In any channel, type:
   ```
   /lead-magnet Target: SaaS companies | Criteria: Size>50 employees
   ```
3. You should see: `✅ Lead search initiated! Processing leads based on your criteria.`
4. Check Railway logs to see if the command was received

### Test Message Event
1. Post a message in your configured Slack channel:
   ```
   Find leads: SaaS companies with >50 employees
   ```
2. The bot should respond: `✅ Lead search initiated! Processing leads based on your criteria.`
3. Check Railway logs for activity

---

## Step 2: Verify Full Pipeline

Once Slack is working, the system should:
1. ✅ Receive trigger from Slack
2. ✅ Parse search criteria
3. ✅ Fetch leads from Prospeo (Layer 2)
4. ✅ Qualify leads with AI (Layer 3)
5. ✅ Stop when 50 qualified leads found (Layer 4)
6. ✅ Save to Supabase (Layer 5)
7. ✅ Generate CSV file (Layer 5)

---

## Step 3: Check Logs

Monitor Railway logs during testing:
- **Railway Dashboard → Your Service → Deployments → Latest → Logs**

Look for:
- ✅ Slack events received
- ✅ Prospeo API calls
- ✅ AI qualification results
- ✅ Supabase insertions
- ❌ Any errors

---

## Step 4: Verify Database

1. Go to **Supabase Dashboard**
2. Check table: `lead_magnet_candidates`
3. Should see qualified leads being inserted

---

## Step 5: Download CSV

1. Check Railway logs for CSV file path (or check locally if running locally)
2. CSV should contain 50 qualified leads (or fewer if max processed)

---

## Troubleshooting

### If Slack doesn't respond:
- Check Railway logs for errors
- Verify bot is in the channel
- Check SLACK_BOT_TOKEN is set in Railway

### If Prospeo fails:
- Verify PROSPEO_API_KEY is set
- Check Prospeo API rate limits
- Look for API errors in logs

### If AI qualification fails:
- Verify OPENROUTER_API_KEY is set
- Check model is available/affordable
- Look for API errors in logs

### If Supabase fails:
- Verify SUPABASE_URL and SUPABASE_KEY are set
- Check table exists (run supabase_schema.sql)
- Look for database errors in logs

---

## Expected Behavior

### First Test (Small)
Try a simple test first:
```
/lead-magnet Target: Software companies | Criteria: Size>10
```

This should process fewer leads and complete faster.

### Full Production Test
Once confirmed working:
```
/lead-magnet Target: SaaS companies | Criteria: Size>50 employees, Industry=Technology
```

This will process up to 500 leads to find 50 qualified ones.

---

## Next Actions

1. **Test slash command** in Slack
2. **Check Railway logs** for activity
3. **Verify leads are being processed**
4. **Check Supabase** for results
5. **Monitor for errors**

Once everything is working, you're done! 🎉
