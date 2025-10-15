# 🤖 AI Agent Documentation Guide

**Purpose:** Ensure AI agents update existing docs instead of creating duplicates, and maintain context for next steps.

**Last Updated:** October 15, 2025

---

## 📋 Core Principle: UPDATE, DON'T DUPLICATE

### ❌ DON'T Create New Files For:
- Bug fixes → Update `CHANGELOG.md`
- Feature completions → Update the relevant `WEEK*_COMPLETE.md`
- Configuration changes → Update `QUICK_START.md` or `IMPLEMENTATION_SUMMARY.md`
- Process updates → Update existing workflow docs

### ✅ DO Create New Files For:
- Major milestones (e.g., `WEEK5_6_COMPLETE.md`)
- New architectural patterns not covered elsewhere
- Significant incidents requiring detailed postmortem

---

## 📚 Master Documentation Map

### 1. **CHANGELOG.md** - Historical Record
**When to Update:** Every code change, bug fix, feature addition
**Format:**
```markdown
## [Date] - [Type of Change]
- Changed: [What changed]
- Fixed: [What was broken]
- Added: [What's new]
- Impact: [What areas affected]
```

### 2. **IMPLEMENTATION_SUMMARY.md** - Living Technical Doc
**When to Update:** Architecture changes, tech stack updates, API changes
**Sections to Maintain:**
- Tech Stack
- Architecture Overview
- API Endpoints
- Database Schema
- Current Status

### 3. **WEEK*_COMPLETE.md** - Milestone Docs
**When to Update:** When a week's planned features are done
**Current Active:**
- `WEEK3_4_COMPLETE.md` (Latest)
- Create `WEEK5_6_COMPLETE.md` only when Week 5-6 work begins

### 4. **QUICK_START.md** - Setup Instructions
**When to Update:** 
- New dependencies added
- Environment variables changed
- Setup process modified

### 5. **AUTHENTICATION_FLOW.md** - Security Docs
**When to Update:** Auth logic changes, security updates, new auth endpoints

### 6. **PRODUCTION_ROADMAP.md** - Planning Doc
**When to Update:** 
- Phase completions (mark ✅)
- Priority changes
- Scope adjustments

---

## 🔄 Daily Update Workflow

### For Every Code Session:

**1. Start of Session:**
```markdown
Read these files first (in order):
1. CHANGELOG.md (last 20 lines) - What happened recently
2. PRODUCTION_ROADMAP.md - What's the current priority
3. Relevant WEEK*_COMPLETE.md - What's the current phase
```

**2. During Development:**
- Track what you're changing
- Note any bugs found
- Document workarounds

**3. End of Session:**
```markdown
Update in this order:
1. CHANGELOG.md - Add today's changes at the TOP
2. IMPLEMENTATION_SUMMARY.md - Update affected sections
3. PRODUCTION_ROADMAP.md - Mark completed items with ✅
```

---

## 📝 Standard Update Patterns

### Pattern 1: Bug Fix
**Update:** `CHANGELOG.md` only
```markdown
## October 15, 2025 - Bug Fix

**Fixed:** Authentication decorator not passing current_user parameter
- Modified: app/api/auth.py line 43
- Impact: All 26+ protected endpoints now functional
- Files changed: 1
- Tests: Manual verification successful
```

### Pattern 2: Feature Addition
**Update:** `CHANGELOG.md` + `WEEK*_COMPLETE.md`
```markdown
# In CHANGELOG.md:
## October 15, 2025 - Feature

**Added:** Export analysis to PDF functionality
- New endpoint: POST /api/analyses/:id/export
- Files added: app/utils/pdf_export.py
- Frontend: Export button in analysis detail page

# In WEEK3_4_COMPLETE.md:
Update the relevant section with ✅ marker
```

### Pattern 3: Configuration Change
**Update:** `CHANGELOG.md` + `QUICK_START.md`
```markdown
# In CHANGELOG.md:
## October 15, 2025 - Config

**Changed:** Added required environment variable
- New var: STRIPE_API_KEY required for payment processing
- Updated: .env.example

# In QUICK_START.md:
Add to Environment Variables section
```

---

## 🎯 Context Preservation Strategy

### Create Session Context File
For complex multi-day work, create: `documentation/CURRENT_WORK.md`

```markdown
# Current Work in Progress

**Started:** October 15, 2025
**Phase:** Week 5-6 - Monetization
**Current Task:** Stripe integration

## What's Done
- [x] Stripe account created
- [x] API keys obtained
- [ ] Payment endpoint created

## Next Steps
1. Create payment processing endpoint
2. Add subscription model to database
3. Implement quota enforcement
4. Add pricing page to frontend

## Important Context
- Using Stripe Checkout (not Elements)
- Webhook endpoint: /api/webhooks/stripe
- Test mode keys stored in .env

## Blockers
- None currently

## Notes
- Customer wants monthly/yearly billing
- Free tier: 10 analyses/month
- Pro tier: unlimited analyses
```

**Delete this file when the phase is complete!**

---

## 🗂️ File Organization Rules

### Living Documents (Update These)
- `CHANGELOG.md` - Append at top
- `IMPLEMENTATION_SUMMARY.md` - Update sections
- `QUICK_START.md` - Update procedures
- `PRODUCTION_ROADMAP.md` - Mark progress
- `AUTHENTICATION_FLOW.md` - Update flows
- `CURRENT_WORK.md` - Update daily (if exists)

### Historical Documents (Don't Modify)
- `WEEK1_COMPLETE_SUMMARY.md` - Frozen
- `WEEK1_AUTH_COMPLETE.md` - Frozen  
- `WEEK1_PROJECT_CONTEXT_COMPLETE.md` - Frozen
- `AUTH_FIX_OCT15.md` - Incident report (frozen)

### Create New Only When:
- New week/phase starts → `WEEK*_COMPLETE.md`
- Major incident → `*_FIX_[DATE].md`
- New feature area → `*_FLOW.md` or `*_GUIDE.md`

---

## 🤖 AI Agent Checklist

Before creating a new doc, ask:

1. ✅ Is this a changelog item? → Update `CHANGELOG.md`
2. ✅ Is this a tech detail? → Update `IMPLEMENTATION_SUMMARY.md`
3. ✅ Is this setup-related? → Update `QUICK_START.md`
4. ✅ Is this a phase completion? → Update existing `WEEK*_COMPLETE.md` or create new
5. ✅ Is this truly unique? → Only then create new file

---

## 📊 Documentation Health Metrics

### Good Documentation:
- ✅ CHANGELOG has today's date at the top
- ✅ No duplicate files (e.g., multiple auth guides)
- ✅ PRODUCTION_ROADMAP shows current phase clearly
- ✅ All code changes reflected in docs within 24hrs

### Needs Cleanup:
- ❌ Multiple files covering same topic
- ❌ CHANGELOG not updated in 2+ days
- ❌ Orphaned docs not linked anywhere
- ❌ Conflicting information across docs

---

## 🎓 Examples of Good Updates

### Good Example 1: Quick Bug Fix
```bash
# Only touched:
- CHANGELOG.md (added 5 lines at top)
```

### Good Example 2: Feature Completion
```bash
# Touched:
- CHANGELOG.md (added feature entry)
- WEEK3_4_COMPLETE.md (marked feature as ✅)
- PRODUCTION_ROADMAP.md (marked task complete)
```

### Good Example 3: Major Milestone
```bash
# Touched:
- CHANGELOG.md (added milestone entry)
- Created: WEEK5_6_COMPLETE.md (new phase)
- PRODUCTION_ROADMAP.md (marked entire phase)
- README.md (updated current phase)
```

---

## 🚀 Quick Reference

**Before starting work:**
```bash
Read: CHANGELOG.md (recent), PRODUCTION_ROADMAP.md (priorities)
```

**After making changes:**
```bash
Update: CHANGELOG.md (always), relevant living docs (as needed)
```

**When stuck:**
```bash
Check: CURRENT_WORK.md, IMPLEMENTATION_SUMMARY.md, WEEK*_COMPLETE.md
```

**When phase completes:**
```bash
Create: WEEK*_COMPLETE.md
Update: PRODUCTION_ROADMAP.md, README.md
Delete: CURRENT_WORK.md (if exists)
```

---

**Remember:** Good documentation is updated documentation, not duplicated documentation! 📝
