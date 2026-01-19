# Deployment Guide for Lead Magnet Generator

## Development vs Production

### Development Phase (Current)
- ✅ Use **ngrok** (free) for temporary URLs
- ✅ Run locally on your machine
- ✅ Good for testing and development
- ⚠️ URLs change each time you restart ngrok

### Production Phase (Later)
- ✅ Need **permanent HTTPS URL**
- ✅ Server must be always running
- ✅ Stable, reliable, and accessible 24/7

---

## GitHub Actions vs Railway/Render

### Can we use GitHub Actions alone? ❌ NO

**GitHub Actions is NOT for hosting:**
- ❌ Runs jobs temporarily (max 6 hours)
- ❌ Not meant for long-running servers
- ❌ No permanent URLs
- ❌ Not accessible 24/7

**GitHub Actions IS for:**
- ✅ Automated testing (when you push code)
- ✅ Running tests automatically
- ✅ Deploying TO Railway/Render (CI/CD)
- ✅ Quality checks before deployment

### Best Setup: GitHub Actions + Railway/Render ✅

**How they work together:**
1. **Railway/Render** = Hosts your app 24/7 (the actual server)
2. **GitHub Actions** = Automatically deploys to Railway when you push code (CI/CD)

**Workflow:**
```
You push code → GitHub Actions runs tests → 
If tests pass → GitHub Actions deploys to Railway → 
Railway runs your app 24/7
```

---

## Deployment Options

### Option 1: Render.com (Recommended - FREE)

**Pros:**
- Free tier available
- Automatic HTTPS (permanent URL)
- Easy deployment from GitHub
- Auto-deploys on code changes
- Managed service (no server maintenance)

**Steps:**
1. Push code to GitHub
2. Sign up at https://render.com
3. Create "Web Service"
4. Connect GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python layer1_slack_listener.py`
7. Add environment variables (from your .env file)
8. Deploy!

**You'll get:** `https://lead-magnet-generator.onrender.com`

**Slack URLs:**
- Events: `https://lead-magnet-generator.onrender.com/slack/events`
- Commands: `https://lead-magnet-generator.onrender.com/slack/commands`

**Cost:** FREE (with limits) or $7/month for always-on

---

### Option 2: Railway.app (FREE Tier)

Similar to Render:
1. Push to GitHub
2. Sign up at https://railway.app
3. Deploy from GitHub
4. Add environment variables
5. Get permanent URL

**Cost:** FREE tier available, $5/month for always-on

---

### Option 3: ngrok Reserved Domain ($8/month)

If you want to keep running locally:
1. Sign up for ngrok paid plan
2. Reserve a domain: `https://lead-magnet.ngrok.io`
3. Use command: `ngrok http 3000 --domain=lead-magnet`
4. Permanent URL!

**Pros:** Keep everything local
**Cons:** Your computer must be on 24/7, costs money

---

### Option 4: Cloudflare Tunnel (FREE)

Similar to ngrok but free:
1. Install cloudflared
2. Create tunnel
3. Get permanent subdomain
4. Free forever

**Docs:** https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

---

## Recommended Path

### Phase 1: Development (Now)
```
✅ Use ngrok free version
✅ Test everything locally
✅ Make sure it works end-to-end
```

### Phase 2: Production (When Ready)
```
Option A: Simple (Recommended for starting)
✅ Deploy directly to Railway/Render (connects to GitHub)
✅ Auto-deploys when you push code
✅ Update Slack URLs to permanent URL
✅ Test in production

Option B: Advanced (With CI/CD)
✅ Set up GitHub Actions for automated testing
✅ GitHub Actions deploys to Railway/Render
✅ Tests run automatically before deployment
✅ More robust, professional setup
```

---

## Environment Variables in Production

When deploying, you'll need to add all your `.env` variables to the platform:

- `PROSPEO_API_KEY`
- `OPENROUTER_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `SLACK_PORT=3000`
- `SLACK_CHANNEL_ID`

Most platforms let you add these in their dashboard (Settings → Environment Variables).

---

## Checklist Before Production

- [ ] Code is working locally with ngrok
- [ ] All environment variables documented
- [ ] Supabase table created and tested
- [ ] Error handling tested
- [ ] Logging set up
- [ ] Deploy to chosen platform
- [ ] Update Slack app URLs
- [ ] Test slash command in production
- [ ] Test message events in production
- [ ] Monitor for errors

---

## Cost Summary

| Option | Cost | Best For |
|--------|------|----------|
| Render.com Free | $0 | Starting out, small projects |
| Render.com Paid | $7/mo | Production, always-on |
| Railway Free | $0 | Starting out |
| Railway Paid | $5/mo | Production |
| ngrok Reserved | $8/mo | Local development, permanent URL |
| Cloudflare Tunnel | $0 | Free alternative to ngrok |
| VPS | $5-12/mo | Full control, technical users |

---

## My Recommendation

**Start with Render.com free tier:**
- Easiest to set up
- Permanent URL immediately
- Free to start
- Can upgrade later if needed
- No need to keep your computer on 24/7

When you're ready to deploy, I can help you with the Render setup process!
