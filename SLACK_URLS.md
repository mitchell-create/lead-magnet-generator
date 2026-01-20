# Slack URLs Configuration

## Your Railway Domain
```
https://lead-magnet-generator-production.up.railway.app
```

---

## Slack URLs to Use

### Event Subscriptions URL:
```
https://lead-magnet-generator-production.up.railway.app/slack/events
```

### Slash Command URL:
```
https://lead-magnet-generator-production.up.railway.app/slack/commands
```

---

## Where to Use Each

### In Slack App → Event Subscriptions:
- **Request URL:** `https://lead-magnet-generator-production.up.railway.app/slack/events`

### In Slack App → Slash Commands:
- **Request URL:** `https://lead-magnet-generator-production.up.railway.app/slack/commands`

---

## Important Notes

✅ **Include the `/slack/events` and `/slack/commands` paths**
- These are the endpoints your Flask app listens on
- Without them, Slack won't know where to send events

✅ **Use HTTPS (not HTTP)**
- Railway provides HTTPS automatically
- Slack requires HTTPS

✅ **No port number needed**
- Railway handles port routing automatically
- Your app runs on port 3000 internally, but externally it's just HTTPS

---

## Quick Copy-Paste

**For Event Subscriptions:**
```
https://lead-magnet-generator-production.up.railway.app/slack/events
```

**For Slash Commands:**
```
https://lead-magnet-generator-production.up.railway.app/slack/commands
```
