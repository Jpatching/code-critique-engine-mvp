# VS Code + GitHub Copilot Setup Guide
## Code Critique Engine

## ✅ What's Already Configured

### 1. **Prompt Files** ✅
Your master instructions are at:
- `.github/copilot-instructions.md` - Main project instructions
- `.github/copilot-workspace-instructions.md` - VS Code specific workflows

GitHub Copilot automatically reads these files when you interact with it.

### 2. **Tool Sets** ✅
All tools are enabled in `.vscode/settings.json`:
- ✅ **Code Search** - `#codebase` command
- ✅ **File Search** - `#file:` command  
- ✅ **Terminal Integration** - `@terminal` command
- ✅ **Workspace Context** - `@workspace` command
- ✅ **Web Search** - Built into Copilot Chat

### 3. **Auto-Context** ✅
Configured in `.vscode/settings.json`:
- Copilot automatically reads instruction files
- Workspace context is enabled
- Code search is experimental-enabled
- Terminal integration is experimental-enabled

### 4. **MCP Servers** ✅
Basic MCP servers configured:
- **filesystem** - File operations context
- **git** - Repository history context

### 5. **Python Environment** ✅
Already configured:
- Python interpreter: `.venv/bin/python`
- Pylance analysis: Basic type checking
- Auto-import completions: Enabled
- Environment activation: Automatic

### 6. **Terminal Environment** ✅
Pre-configured environment variables:
- `GEMINI_API_KEY` - Already set
- `POCKETBASE_URL` - Already set

## 🚀 How to Use GitHub Copilot Chat

### Starting a Chat Session

1. **Open Copilot Chat:**
   - Press `Ctrl+Shift+I` (Linux) or `Cmd+Shift+I` (Mac)
   - Or click the chat icon in the sidebar

2. **Available Commands:**

#### `@workspace` - Ask about your project
```
@workspace what's the current development phase?
@workspace where is authentication implemented?
@workspace show me all API endpoints
@workspace how does the analysis flow work?
```

#### `#codebase` - Search across all code
```
#codebase @require_auth decorator
#codebase analyze_code function
#codebase apiRequest usage
#codebase authentication flow
```

#### `#file:` - Reference specific files
```
#file:documentation/CHANGELOG.md show recent changes
#file:app/config.py what are the configuration options?
#file:app/services/ai_service.py explain the concurrent analysis
```

#### `@terminal` - Execute commands
```
@terminal ./verify_system.sh
@terminal ./verify_auth.sh
@terminal curl http://127.0.0.1:5000/health
```

### Common Workflows

#### 🔍 **Understanding the Project**
```
@workspace give me an overview of the project structure
#file:documentation/PRODUCTION_ROADMAP.md what's the current phase?
#file:documentation/IMPLEMENTATION_SUMMARY.md explain the architecture
```

#### 🐛 **Debugging Issues**
```
@workspace I'm getting a 500 error on /analyze endpoint, what could be wrong?
#codebase analyze_code error handling
#file:server.log show recent errors
@terminal ./verify_system.sh
```

#### ✨ **Adding New Features**
```
@workspace where should I add a new analysis feature?
#codebase similar existing feature
#file:app/services/ai_service.py show me the pattern
#file:documentation/CHANGELOG.md
```

#### 📝 **Code Review**
```
@workspace review this file for security issues
#codebase @require_auth find all protected routes
@workspace check if all routes are properly authenticated
```

## 🎯 Best Practices

### 1. **Start with Context**
Always begin with `@workspace` to get an overview:
```
@workspace I need to add user profile editing, where should I start?
```

### 2. **Reference Documentation**
Use `#file:` to load relevant docs:
```
#file:documentation/PRODUCTION_ROADMAP.md
#file:documentation/CHANGELOG.md (first 20 lines)
#file:.github/copilot-instructions.md
```

### 3. **Search Before Asking**
Use `#codebase` to find existing patterns:
```
#codebase similar pattern to what I want to implement
```

### 4. **Chain Commands**
Combine commands for better context:
```
@workspace find the authentication flow, then #codebase show implementation details
```

### 5. **Use Inline Chat**
For quick edits:
- Select code in editor
- Press `Ctrl+I` (Linux) or `Cmd+I` (Mac)
- Ask: "Add error handling" or "Optimize this function"

## 🔧 Advanced Features

### Slash Commands in Chat

#### `/explain`
Explain selected code:
```
/explain this function
/explain the authentication decorator pattern
```

#### `/fix`
Fix issues in code:
```
/fix this error
/fix the authentication bug
```

#### `/tests`
Generate tests:
```
/tests generate unit tests for this function
/tests create integration test for authentication
```

#### `/doc`
Generate documentation:
```
/doc add docstring to this function
/doc create API documentation
```

### Editor Commands

#### Quick Fix (Right-click)
- Right-click on code
- Select "Copilot: Generate..."
- Choose from suggestions

#### Inline Suggestions
- Type code naturally
- Press `Tab` to accept Copilot suggestions
- Press `Alt+]` for next suggestion
- Press `Alt+[` for previous suggestion

## 📊 Monitoring & Verification

### Check Copilot Status
```
Ctrl+Shift+P → "GitHub Copilot: Check Status"
```

### View Copilot Logs
```
Ctrl+Shift+P → "GitHub Copilot: Show Output"
```

### Test MCP Servers
```
@terminal npx --version  # Verify npx is installed
```

## 🛠️ Installation & Setup

### Required Extensions (Already Recommended)
Install these from `.vscode/extensions.json`:

1. **GitHub Copilot** (Required)
   - `github.copilot`
   - `github.copilot-chat`

2. **Python Development**
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `ms-python.debugpy`

3. **Web Development**
   - `ritwickdey.liveserver`

4. **Documentation**
   - `yzhang.markdown-all-in-one`

### Install Extensions
```
Ctrl+Shift+P → "Extensions: Show Recommended Extensions"
Click "Install All"
```

### Setup MCP Servers (Optional)
If you want full MCP support:

```bash
# Install MCP filesystem server
npm install -g @modelcontextprotocol/server-filesystem

# Install MCP git server
npm install -g @modelcontextprotocol/server-git
```

Then restart VS Code.

## 🎓 Tips & Tricks

### 1. **Multi-File Context**
Copilot automatically sees:
- Currently open file
- Related files in workspace
- Recent changes
- Git context

### 2. **Better Questions**
❌ Bad: "How do I do X?"
✅ Good: "@workspace where is X implemented and how can I add Y?"

### 3. **Iterative Refinement**
Start broad, then narrow:
```
1. @workspace overview of authentication
2. #codebase @require_auth implementation
3. #file:app/api/auth.py show decorator details
```

### 4. **Use Context Operators**
Combine for powerful queries:
```
@workspace #codebase analyze_code #file:app/services/ai_service.py 
explain the complete analysis flow
```

### 5. **Document as You Go**
After making changes:
```
@workspace update documentation/CHANGELOG.md with these changes:
[describe changes]
```

## 🚨 Troubleshooting

### Copilot Not Working?
1. Check status: `Ctrl+Shift+P` → "GitHub Copilot: Check Status"
2. Sign in: `Ctrl+Shift+P` → "GitHub Copilot: Sign In"
3. Restart: Reload VS Code window

### Instructions Not Loading?
1. Verify `.github/copilot-instructions.md` exists
2. Check `.vscode/settings.json` has `useInstructionFiles: true`
3. Reload VS Code

### Terminal Commands Not Working?
1. Verify `experimental.terminalIntegration.enabled: true`
2. Check terminal is using bash
3. Ensure scripts have execute permissions: `chmod +x verify_*.sh`

### MCP Servers Not Starting?
1. Check `npx` is installed: `npx --version`
2. Install MCP packages (see Installation section)
3. Restart VS Code

## 📚 Quick Reference

### Essential Commands
| Command | Purpose |
|---------|---------|
| `@workspace` | Ask about project |
| `#codebase` | Search all code |
| `#file:path` | Reference specific file |
| `@terminal` | Run commands |
| `/explain` | Explain code |
| `/fix` | Fix issues |
| `/tests` | Generate tests |

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+I` | Open Copilot Chat |
| `Ctrl+I` | Inline Chat |
| `Tab` | Accept suggestion |
| `Alt+]` | Next suggestion |
| `Alt+[` | Previous suggestion |

### Project-Specific
| Command | Purpose |
|---------|---------|
| `@terminal ./verify_system.sh` | Full system check |
| `@terminal ./verify_auth.sh` | Test authentication |
| `@terminal ./start_server.sh` | Start Flask server |
| `#file:documentation/CHANGELOG.md` | Recent changes |
| `#file:documentation/PRODUCTION_ROADMAP.md` | Current phase |

## 🎯 Next Steps

1. **Test Copilot Chat:**
   ```
   Press Ctrl+Shift+I
   Type: @workspace what's the current development phase?
   ```

2. **Try Code Search:**
   ```
   Type: #codebase @require_auth
   ```

3. **Reference Documentation:**
   ```
   Type: #file:documentation/CHANGELOG.md show recent changes
   ```

4. **Run Verification:**
   ```
   Type: @terminal ./verify_system.sh
   ```

## 📖 Additional Resources

- **GitHub Copilot Docs:** https://docs.github.com/copilot
- **VS Code Docs:** https://code.visualstudio.com/docs
- **Project Docs:** `documentation/` folder
- **Quick Start:** `documentation/QUICK_START.md`
- **Agent Guide:** `documentation/AI_AGENT_GUIDE.md`

---

**Everything is already configured! Just open Copilot Chat (`Ctrl+Shift+I`) and start asking questions!** 🚀
