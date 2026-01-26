# "Positive in Slack, but no run in Railway" – Fix

## What’s going on

You see a success-style message in Slack (e.g. “Lead search initiated!”), but nothing runs in Railway. That usually means:

**Slack is calling a different URL than Railway.**

Slack sends `/lead-magnet` to the **Request URL** configured in your Slack app. If that URL is your **local app** (e.g. via ngrok) or an **old host**, that server responds and you see the positive message. **Railway never receives the request**, so there’s no run and no logs there.

---

## What to do: Point Slack at Railway

### 1. Get your Railway URL

1. Open [Railway](https://railway.app) → your **project** → the **service** that runs the lead-magnet app.
2. Go to **Settings** (or the deployment), and find **Domains** / **Public URL**.
3. Copy the public URL. It often looks like:
   - `https://lead-magnet-generator-production.up.railway.app`
   - or `https://your-app-name.up.railway.app`
4. Your **Slash Command URL** must be that domain **plus** `/slack/commands`, for example:
   - `https://lead-magnet-generator-production.up.railway.app/slack/commands`

### 2. Set the Slash Command Request URL in Slack

1. Go to **https://api.slack.com/apps**
2. Select the app you use for the lead-magnet.
3. In the left sidebar, open **Slash Commands**.
4. Click **/lead-magnet** (or create it if it doesn’t exist).
5. Set **Request URL** to your Railway Slash Command URL from step 1, e.g.:
   - `https://YOUR-RAILWAY-DOMAIN.up.railway.app/slack/commands`  
   Replace `YOUR-RAILWAY-DOMAIN` with your real Railway domain (no trailing slash).
6. **Save** at the bottom.

### 3. Optional: Events URL

If you also use “find leads” or other **events** (not only the slash command):

1. In the same Slack app, go to **Event Subscriptions**.
2. Set **Request URL** to:
   - `https://YOUR-RAILWAY-DOMAIN.up.railway.app/slack/events`
3. Save.

### 4. Test again

1. In Slack, run `/lead-magnet` again (e.g. with your keywords and filters).
2. In Railway, open your service → **Deployments** → latest deployment → **Logs**.
3. You should see log lines when the command is received (e.g. “Slash command received”, “Processing lead search”). New rows should appear in Supabase from that run.

---

## Checklist

- [ ] Railway service is **deployed** and **running** (no failed/crashed state).
- [ ] You know the **public domain** of that service (e.g. `something.up.railway.app`).
- [ ] In Slack: **Slash Commands** → **/lead-magnet** → **Request URL** = `https://<that-domain>/slack/commands`.
- [ ] If you use events: **Event Subscriptions** → **Request URL** = `https://<that-domain>/slack/events`.
- [ ] You **saved** in the Slack app after changing URLs.

Once the Request URL points at Railway, the “positive message in Slack” will come from Railway, and you’ll see the run and logs there.
