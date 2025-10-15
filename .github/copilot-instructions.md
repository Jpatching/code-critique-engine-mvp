# Code Critique Engine - AI Agent Instructions

## 📚 CRITICAL: READ THIS FIRST

### **Documentation Strategy** ⚠️
**BEFORE making any changes:**
1. Read `documentation/AI_AGENT_GUIDE.md` - **MANDATORY** - Documentation maintenance rules
2. Read `documentation/CHANGELOG.md` - Recent changes (top 20 lines)
3. Read `documentation/PRODUCTION_ROADMAP.md` - Current priorities

### **Core Principle: UPDATE, DON'T DUPLICATE**
- ✅ **UPDATE** existing docs (`CHANGELOG.md`, `IMPLEMENTATION_SUMMARY.md`, `QUICK_START.md`)
- ❌ **DON'T** create new docs for bug fixes or small features
- ✅ **CREATE** new docs only for major milestones (e.g., `WEEK5_6_COMPLETE.md`)
- 📝 **ALWAYS** update `documentation/CHANGELOG.md` after EVERY code change (add entry at TOP)

---

## Project Overview
Full-stack AI-powered code coaching SaaS platform that analyzes AI-generated code and provides production-readiness scores, detailed reports, and architectural guidance. Built with Flask (Python), PocketBase (database), Vanilla JavaScript (SPA frontend), and Google Gemini AI.

**Phase:** Week 3-4 Complete (Enhanced Analysis Experience) → Moving to Week 5-6 (Monetization)  
**Gemini API Key:** `AIzaSyBf0cGONzMrHzsGYY9Cm19g--B5PYrtWn8`

## Architecture Overview

### Service Layer Pattern
- **`app/services/ai_service.py`** - All Gemini API interactions, concurrent analysis, prompt management
- **`app/services/pocketbase_service.py`** - Database CRUD operations, authentication verification
- **`app/api/`** - Blueprint-based API modules (`analysis.py`, `auth.py`, `projects.py`, `analyses.py`)
- **`app/config.py`** - Centralized config with environment-based validation

### Three-Layer Authentication Enforcement
1. **Frontend Router** (`static/js/router.js`) - Redirects unauthenticated users to `/auth`
2. **API Client** (`static/js/api.js`) - Automatically includes JWT tokens in requests
3. **Backend Decorator** (`app/api/auth.py`) - `@require_auth` validates tokens, passes `current_user` to routes

**Critical Pattern:** Protected routes MUST have `@require_auth` decorator and accept `current_user` as first parameter:
```python
@analysis_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_code(current_user):  # current_user is passed by decorator
    # Access user data via current_user['id'], current_user['email']
```

### Concurrent AI Analysis Architecture
**Location:** `app/services/ai_service.py` → `analyze_code()`

Three parallel Gemini API calls using `ThreadPoolExecutor`:
1. **Scores Prompt** → `total_score` (0-25), `reliability_score` (0-10), `mastery_score` (0-15), `explanation_summary`, `debug_prognosis`
2. **Reports Prompt** → 5 detailed reports: `clarity`, `modularity`, `efficiency`, `security`, `documentation`
3. **Refactor Prompt** → `refactored_code`, `project_roadmap` (converted from string to array)

**Data Transformation Pattern:** `_combine_results()` merges concurrent responses and transforms data for frontend:
- Flattens nested `report` object into root level
- Splits `project_roadmap` string on newlines → array
- Renames `explanation` → `explanation_summary` for compatibility
- Adds `original_code` for diff comparison

### Frontend SPA Architecture
**Router:** `static/js/router.js` with dynamic route matching (`/projects/:id`, `/analysis/:id`)
**Pages:** Lazy-loaded modules in `static/js/pages/` (e.g., `dashboard.js`, `analyze.js`, `analysis-detail.js`)
**Global Services:** `authService` (singleton in `auth.js`), `apiRequest()` (in `api.js`)

## Critical Development Workflows

### Server Startup Sequence (MUST FOLLOW THIS ORDER)
```bash
# Terminal 1: Start PocketBase first
./pocketbase serve  # Port 8090

# Terminal 2: Flask with required environment variable
source .venv/bin/activate
export GEMINI_API_KEY="your_key_here"  # CRITICAL - server fails without this
python3 server.py  # Port 5000

# Terminal 3: Frontend (VS Code Live Server)
# Right-click static/index.html → "Open with Live Server" (Port 5500)
```

**Quick Start Alternative:** `./start_server.sh` (exports API key and runs Flask)

### Testing & Verification Scripts
- **`./verify_auth.sh`** - Tests authentication flow (signup → login → token validation)
- **`./verify_week3_4.sh`** - Validates Week 3-4 features (analysis detail, comparison, export)
- **`./verify_system.sh`** - Full system health check

### Database Schema (PocketBase Collections)
- **`users`** - Auto-created by PocketBase auth system
- **`projects`** - User projects with tech stack context (`user_id`, `name`, `stack[]`, `architecture_type`, `code_style`)
- **`analyses`** - Code analysis results with full AI response JSON (`user_id`, `project_id`, scores, reports)
- **`project_ideas`** - (Legacy) Original MVP collection, still present

**Key Pattern:** All collections have `user_id` foreign key for multi-tenancy. Backend decorators verify ownership before CRUD operations.

## Project-Specific Conventions

### Configuration Management
**File:** `app/config.py` - Single dataclass with environment variable defaults

**Key Config Values:**
- `GEMINI_API_KEY` (required) - Validated in `config.validate()`
- `GEMINI_MODEL` - Defaults to `models/gemini-1.5-flash` (free tier)
- `MAX_CONCURRENT_AI_REQUESTS` - Default: 3 (matches ThreadPoolExecutor workers)
- `CORS_ORIGINS` - CSV string, defaults to `http://127.0.0.1:5500`

**Convention:** All services import `from app.config import config` (singleton instance)

### Prompt Engineering Standards
**Location:** `app/services/ai_service.py` → `_get_scores_prompt()`, `_get_reports_prompt()`, `_get_refactor_prompt()`

All prompts follow this structure:
1. Role definition ("You are an expert AI Code Reviewer")
2. Project context injection (optional) → `{project_context}` placeholder
3. Strict JSON schema enforcement: "Your output MUST be a JSON object with the following keys..."
4. Input placeholders: `{prompt}`, `{code}`, `{project_context}`
5. Final instruction: "Ensure your output is ONLY the raw JSON object."

**Critical:** Gemini responses must be sanitized to strip markdown fences (`````json`, `````) before JSON parsing.

### Frontend API Request Pattern
**File:** `static/js/api.js` → `apiRequest()`

**Standard Usage:**
```javascript
const result = await apiRequest('/api/analyses/compare?ids=id1,id2', {
    method: 'GET'  // Defaults to GET
});
// Automatically handles: JWT injection, 401 redirects, JSON parsing, error responses
```

**Convention:** Use `apiRequest()` for all backend calls (never raw `fetch()`). It centralizes:
- Authorization header injection
- Token expiration handling (auto-logout on 401)
- Error response parsing
- Content-Type headers

### Week 3-4 Enhanced Features (Just Built)
**New Pages:**
- **`/analysis/:id`** - Tabbed detail view (Overview, Security, Performance, Architecture, Refactoring)
- **`/compare?id1=X&id2=Y`** - Side-by-side analysis comparison with score deltas

**New Backend Endpoints:**
- `GET /api/analyses/compare?ids=id1,id2` - Returns comparison with `score_deltas`, `percentage_improvements`, `trend` summary
- `POST /api/analyses/:id/export` - Generates Markdown export (PDF placeholder)

**UI Patterns:**
- Tab switching via `data-tab` attributes with `.active` class toggling
- Score cards use CSS custom properties: `style.setProperty('--score', value)`
- Export triggers download via `Blob` + `URL.createObjectURL()`

## Common Debugging Scenarios

### Authentication Issues
**Symptom:** 500 errors on protected endpoints after signup/login  
**Check:** Verify decorated routes have `(current_user)` parameter - the `@require_auth` decorator passes user as first arg

**Symptom:** Infinite redirect to `/auth`  
**Check:** `localStorage` token presence → `authService.isAuthenticated()` logic → Backend `/auth/me` endpoint

### AI Analysis Failures
**Symptom:** 500 errors on `/analyze` endpoint  
**Check in order:**
1. `GEMINI_API_KEY` environment variable set
2. Concurrent API call timeouts (check `AI_REQUEST_TIMEOUT` config)
3. JSON parsing failures (look for unstripped markdown fences in AI response)
4. Project context fetch errors (non-fatal, should continue without context)

**Debugging Pattern:** Server logs include request details:
```
Analysis Request:
  User: user@example.com
  Project ID: abc123
  Prompt: Original AI prompt...
  Code length: 1234 characters
```

### Frontend State Issues
**Symptom:** Page doesn't update after API call  
**Check:** Router navigation flow - ensure `router.navigate()` triggers re-render, not just URL change

**Symptom:** "Missing analysis IDs" error on comparison page  
**Check:** Query parameter extraction in router - `queryParams.get('id1')` must exist

## Development vs Production

### Current State (Development)
- Flask dev server (`app.run(debug=True)`)
- PocketBase embedded SQLite
- No rate limiting enforced
- CORS open to localhost

### Production Readiness Path (See `documentation/PRODUCTION_ROADMAP.md`)
- **WSGI:** Use `wsgi.py` with Gunicorn (`gunicorn wsgi:application`)
- **Rate Limiting:** Implement per-user analysis quotas (tied to paid tiers)
- **Environment:** All secrets via environment variables, no hardcoded keys
- **Monitoring:** Add structured logging (JSON format for log aggregation)