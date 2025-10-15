# GitHub Copilot Workspace Instructions
# Code Critique Engine - VS Code Specific

## 🎯 Quick Context Loading

**Always start by reading these files:**
1. `documentation/CHANGELOG.md` (top 20 lines) - Recent changes
2. `documentation/PRODUCTION_ROADMAP.md` - Current priorities  
3. `documentation/IMPLEMENTATION_SUMMARY.md` - Architecture overview

## 🔧 Available VS Code Tools

### #codebase Search
Search entire project for patterns, functions, classes:
```
#codebase @require_auth decorator
#codebase analyze_code function
#codebase apiRequest
```

### #file References
Reference specific files for context:
```
#file:app/config.py
#file:app/services/ai_service.py
#file:static/js/api.js
#file:documentation/CHANGELOG.md
```

### @workspace Commands
Ask questions about the entire workspace:
```
@workspace where is authentication implemented?
@workspace show me all API endpoints
@workspace how does concurrent AI analysis work?
```

### Terminal Commands (Use with @terminal)
```
@terminal ./verify_system.sh       # Full system check
@terminal ./verify_auth.sh         # Auth flow test
@terminal ./verify_week3_4.sh      # Feature validation
@terminal ./start_server.sh        # Start Flask server
```

## 📂 Key Files Auto-Context

**Configuration:**
- `app/config.py` - All environment variables and settings
- `.vscode/settings.json` - VS Code project settings

**Backend:**
- `app/services/ai_service.py` - Gemini AI integration, concurrent analysis
- `app/services/pocketbase_service.py` - Database operations
- `app/api/auth.py` - Authentication decorator pattern
- `app/api/analysis.py` - Analysis endpoints
- `server.py` - Flask app entry point

**Frontend:**
- `static/js/router.js` - SPA routing
- `static/js/api.js` - API client with auth
- `static/js/auth.js` - Auth service singleton
- `static/js/pages/*.js` - Page modules

**Documentation:**
- `documentation/AI_AGENT_GUIDE.md` - Doc maintenance rules
- `documentation/CHANGELOG.md` - All changes (update after EVERY change)
- `documentation/PRODUCTION_ROADMAP.md` - Current phase and priorities

## 🚀 Common Workflows

### Starting a Development Session
1. Check current phase: `#file:documentation/PRODUCTION_ROADMAP.md`
2. Review recent changes: `#file:documentation/CHANGELOG.md` (top 20 lines)
3. Ask: `@workspace what's the current task?`

### Adding a New Feature
1. Check roadmap: `@workspace what features are planned?`
2. Find similar code: `#codebase similar feature name`
3. Follow patterns in existing code
4. **Update CHANGELOG.md** at the TOP after implementation

### Debugging an Issue
1. Check server status: `@terminal curl http://127.0.0.1:5000/health`
2. Find related code: `#codebase error message or function name`
3. Check logs: View `server.log` or terminal output
4. Run verification: `@terminal ./verify_system.sh`

### Understanding Code Patterns
1. **Authentication:** `#file:app/api/auth.py` - See `@require_auth` decorator
2. **AI Service:** `#file:app/services/ai_service.py` - Concurrent analysis pattern
3. **Frontend API:** `#file:static/js/api.js` - `apiRequest()` function
4. **Routing:** `#file:static/js/router.js` - SPA navigation

## 📋 Code Patterns to Follow

### Backend Pattern: Protected Routes
```python
@blueprint.route('/endpoint', methods=['POST'])
@require_auth
def my_endpoint(current_user):  # MUST accept current_user
    user_id = current_user['id']
    # Route logic...
```

### Frontend Pattern: API Calls
```javascript
import { apiRequest } from '../api.js';

const result = await apiRequest('/api/endpoint', {
    method: 'POST',
    body: JSON.stringify({ data })
});
```

### Service Pattern: Configuration
```python
from app.config import config  # Import singleton

# Use config values
api_key = config.GEMINI_API_KEY
timeout = config.AI_REQUEST_TIMEOUT
```

## 🔍 Search Strategies

### Finding Implementations
```
#codebase function_name implementation
#codebase class ClassName
#codebase @decorator_name
```

### Finding Files
```
@workspace where is the login page?
@workspace find all API endpoint files
#file:app/api/
```

### Understanding Data Flow
```
@workspace how does code analysis work end-to-end?
@workspace trace authentication flow
#codebase analyze_code flow
```

## ⚠️ Critical Rules

1. **ALWAYS use `@require_auth` decorator** on protected routes
2. **ALWAYS update `documentation/CHANGELOG.md`** after code changes (add at TOP)
3. **ALWAYS use `apiRequest()`** for frontend API calls (never raw `fetch()`)
4. **NEVER duplicate documentation** - update existing files
5. **ALWAYS verify** with `./verify_system.sh` before committing

## 🎯 Smart Context Usage

### When Adding Features
Attach these files:
- `#file:documentation/PRODUCTION_ROADMAP.md` - Check priorities
- `#file:app/services/ai_service.py` - AI patterns
- `#file:app/api/auth.py` - Auth patterns

### When Fixing Bugs
Attach these files:
- `#file:server.log` - Check errors
- `#file:app/config.py` - Verify settings
- Related service/API files

### When Refactoring
Use:
- `#codebase pattern_to_refactor` - Find all occurrences
- `@workspace show all usages of function_name`
- `#file:documentation/IMPLEMENTATION_SUMMARY.md` - Architecture guide

## 📊 Project Status

**Current Phase:** Week 3-4 Complete → Moving to Week 5-6 (Monetization)

**Tech Stack:**
- Backend: Flask (Python 3.11+)
- Database: PocketBase (SQLite)
- Frontend: Vanilla JavaScript SPA
- AI: Google Gemini 1.5 Flash

**Running Services:**
- PocketBase: http://127.0.0.1:8090
- Flask: http://127.0.0.1:5000
- Frontend: http://127.0.0.1:5500 (Live Server)

**Environment:**
- API Key: Set in `.vscode/settings.json` terminal env
- Virtual Env: `.venv/` (Python 3.11+)

## 💡 Pro Tips

1. **Use `@workspace` first** - Get overview before diving into code
2. **Use `#codebase`** - Find patterns across entire project
3. **Use `#file`** - Reference specific files for detailed context
4. **Chain commands** - `@workspace find X, then #codebase show implementation`
5. **Always verify** - Run verification scripts after changes
6. **Update docs** - CHANGELOG.md is the single source of truth for changes

## 🔗 Related Files

When working on:
- **Authentication** → `app/api/auth.py`, `static/js/auth.js`
- **Analysis** → `app/services/ai_service.py`, `app/api/analysis.py`
- **Projects** → `app/api/projects.py`, `static/js/pages/project.js`
- **Dashboard** → `static/js/pages/dashboard.js`
- **Routing** → `static/js/router.js`
- **Config** → `app/config.py`, `.vscode/settings.json`

---

**Remember:** This project follows a strict documentation pattern. Always update `documentation/CHANGELOG.md` after making changes!
