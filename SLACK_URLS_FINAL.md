# Slack Request URLs - Complete Guide

## Your Railway Domain
```
https://lead-magnet-generator-production.up.railway.app
```

---

## Slack URLs You Need

### 1. Event Subscriptions URL
**Location:** Slack App → Event Subscriptions → Request URL

**URL:**
```
https://lead-magnet-generator-production.up.railway.app/slack/events
```

**What it does:**
- Receives Slack events (like messages in channels)
- Handles URL verification challenge from Slack
- Processes `message.channels` events

---

### 2. Slash Command URL
**Location:** Slack App → Slash Commands → `/lead-magnet` → Request URL

**URL:**
```
https://lead-magnet-generator-production.up.railway.app/slack/commands
```

**What it does:**
- Receives slash command requests (`/lead-magnet`)
- Processes the command and responds to user

---

## Setup Steps

### Step 1: Event Subscriptions

1. Go to: **https://api.slack.com/apps** → Your App
2. Click **"Event Subscriptions"** (left sidebar)
3. Toggle **"Enable Events"** to ON
4. Under **"Request URL"**, enter:
   ```
   https://lead-magnet-generator-production.up.railway.app/slack/events
   ```
5. Click **"Save Changes"**
6. Slack will verify the URL - you should see a **green checkmark** ✅

### Step 2: Subscribe to Bot Events

Still in Event Subscriptions:
1. Scroll to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Add: `message.channels`
4. Click **"Save Changes"**

### Step 3: Slash Command

1. Go to **"Slash Commands"** (left sidebar)
2. Click on `/lead-magnet` command (or create new if needed)
3. **Request URL:**
   ```
   https://lead-magnet-generator-production.up.railway.app/slack/commands
   ```
4. **Short Description:** `Generate qualified leads from Prospeo`
5. **Usage Hint:** `Target: SaaS companies | Criteria: Size>50 employees`
6. Click **"Save"**

---

## Important Notes

✅ **Both URLs use HTTPS** (required by Slack)  
✅ **Both include the full path** (`/slack/events` and `/slack/commands`)  
✅ **No port number** in URLs  
✅ **Same domain** for both, just different paths  

---

## Quick Reference

**Event Subscriptions:**
```
https://lead-magnet-generator-production.up.railway.app/slack/events
```

**Slash Commands:**
```
https://lead-magnet-generator-production.up.railway.app/slack/commands
```

---

## After Setting Up

Once both URLs are configured:
1. Test slash command: `/lead-magnet Target: SaaS companies`
2. Test message event: Post in your channel
3. Check Railway logs to see activity
