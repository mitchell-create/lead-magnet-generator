# Current Workflow - Step by Step

## 📋 Current Process Flow

### Step 1: Slack Trigger ✅
- User sends command: `/lead-magnet industry=SaaS | size>50`
- Slack sends to Railway endpoint
- Parser extracts filters and criteria

---

### Step 2: Prospeo Search ✅
- Fetch leads from Prospeo API (in batches of 25)
- Get raw leads based on filters (industry, location, etc.)

---

### Step 3: AI Qualification (OpenRouter) ✅
**THIS HAPPENS IMMEDIATELY** - For each lead from Prospeo:
- Send lead to OpenRouter/AI for qualification
- AI checks against qualification criteria (size>50, etc.)
- AI returns YES or NO

---

### Step 4: Filter Qualified Leads
- Only leads that get "YES" from AI are kept
- Unqualified leads are **discarded** (not saved)
- Qualified leads stored **in memory** temporarily

---

### Step 5: Loop Back
- If we have < 50 qualified leads:
  - Fetch next page from Prospeo
  - Repeat Steps 2-4
- Continue until:
  - ✅ 50 qualified leads found, OR
  - ⚠️ 500 leads processed (kill switch)

---

### Step 6: Save to Supabase ✅
**ONLY QUALIFIED LEADS** go to Supabase:
- Take all qualified leads (up to 50)
- Insert into `lead_magnet_candidates` table
- Save with metadata (Slack info, criteria, etc.)

---

### Step 7: Generate CSV ✅
- Create CSV file with qualified leads
- Downloadable output

---

## 🔍 Answer to Your Question

**Question:** "Is the next step to use OpenRouter to verify leads? Or does the Prospeo list first go into Supabase?"

**Answer:** 
- ✅ **OpenRouter verification happens FIRST**
- ❌ **Prospeo leads do NOT go to Supabase first**
- ✅ **Only qualified leads go to Supabase**

**Flow:** Prospeo → AI Qualification → Supabase (qualified only)

---

## 📊 What Gets Saved

**In Supabase:**
- ✅ Only AI-qualified leads (up to 50)
- ✅ With qualification metadata
- ✅ Slack trigger info
- ✅ Search criteria used

**NOT Saved:**
- ❌ Raw Prospeo leads (unqualified)
- ❌ Leads that failed AI check

---

## 💡 Why This Design?

**Benefits:**
- ✅ Supabase only contains good leads (saves storage)
- ✅ No need to filter later
- ✅ Clean dataset ready to use
- ✅ Efficient processing (filter before saving)

**Trade-offs:**
- ⚠️ Can't see which leads were rejected (no audit trail of unqualified)
- ⚠️ If qualification criteria changes, need to re-run search

---

## 🤔 Do You Want to Change This?

**Option A: Current (Qualify → Save)**
- Only qualified leads in Supabase
- Clean, ready-to-use data

**Option B: Save All → Qualify**
- Save all Prospeo leads first
- Then mark qualified/unqualified in database
- Can re-qualify later if criteria changes

**Option C: Save Both**
- Save all leads with qualification status
- Keep both qualified and unqualified
- Full audit trail

Which approach do you prefer?
