#!/bin/bash
# VS Code + GitHub Copilot Setup Verification

echo "🔍 Verifying VS Code + GitHub Copilot Setup..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
passed=0
failed=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $2"
        ((failed++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $2"
        ((failed++))
    fi
}

# Function to check command exists
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $2"
        ((passed++))
    else
        echo -e "${YELLOW}○${NC} $2 (optional)"
    fi
}

# Function to check JSON setting
check_setting() {
    if grep -q "$1" .vscode/settings.json; then
        echo -e "${GREEN}✓${NC} $2"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $2"
        ((failed++))
    fi
}

echo "📁 Checking Configuration Files..."
check_file ".vscode/settings.json" "VS Code settings configured"
check_file ".vscode/tasks.json" "VS Code tasks configured"
check_file ".vscode/launch.json" "VS Code launch config exists"
check_file ".vscode/extensions.json" "Recommended extensions listed"
check_file ".github/copilot-instructions.md" "Main Copilot instructions"
check_file ".github/copilot-workspace-instructions.md" "Workspace-specific instructions"
check_file "VSCODE_COPILOT_SETUP.md" "Setup guide exists"
echo ""

echo "⚙️  Checking GitHub Copilot Settings..."
check_setting "github.copilot.enable" "Copilot enabled"
check_setting "useInstructionFiles" "Instruction files enabled"
check_setting "experimental.codeSearch.enabled" "Code search enabled"
check_setting "experimental.terminalIntegration.enabled" "Terminal integration enabled"
echo ""

echo "📚 Checking Documentation..."
check_dir "documentation" "Documentation directory"
check_file "documentation/CHANGELOG.md" "Changelog exists"
check_file "documentation/PRODUCTION_ROADMAP.md" "Production roadmap exists"
check_file "documentation/IMPLEMENTATION_SUMMARY.md" "Implementation summary exists"
check_file "documentation/AI_AGENT_GUIDE.md" "AI Agent guide exists"
echo ""

echo "🐍 Checking Python Environment..."
check_dir ".venv" "Virtual environment exists"
check_file "requirements.txt" "Requirements file exists"
check_setting "python.defaultInterpreterPath" "Python interpreter configured"
echo ""

echo "🔧 Checking Tools & Commands..."
check_command "python3" "Python 3 installed"
check_command "pip3" "pip3 installed"
check_command "npx" "npx installed (for MCP servers)"
check_command "git" "Git installed"
check_command "curl" "curl installed"
echo ""

echo "🚀 Checking Project Scripts..."
check_file "start_server.sh" "Start server script"
check_file "verify_system.sh" "System verification script"
check_file "verify_auth.sh" "Auth verification script"
check_file "verify_week3_4.sh" "Week 3-4 verification script"
echo ""

echo "🗄️  Checking Database..."
check_file "pocketbase" "PocketBase executable"
check_dir "pb_data" "PocketBase data directory"
check_dir "pb_migrations" "PocketBase migrations directory"
echo ""

echo "🌐 Checking Application Structure..."
check_dir "app" "App directory"
check_dir "app/services" "Services directory"
check_dir "app/api" "API directory"
check_dir "static" "Static files directory"
check_dir "static/js" "JavaScript directory"
check_dir "static/js/pages" "Pages directory"
check_file "server.py" "Flask server entry point"
echo ""

echo "🔐 Checking Environment Configuration..."
check_setting "GEMINI_API_KEY" "Gemini API key configured"
check_setting "POCKETBASE_URL" "PocketBase URL configured"
echo ""

# MCP Servers Check (optional)
echo "🔌 Checking MCP Server Configuration..."
check_setting "mcp.servers" "MCP servers configured"
check_setting "filesystem" "Filesystem MCP server"
check_setting "git" "Git MCP server"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Passed: $passed${NC}"
echo -e "${RED}Failed: $failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ All critical checks passed!${NC}"
    echo ""
    echo "🎯 Next Steps:"
    echo "1. Open VS Code"
    echo "2. Press Ctrl+Shift+I to open Copilot Chat"
    echo "3. Type: @workspace what's the current development phase?"
    echo "4. Read VSCODE_COPILOT_SETUP.md for usage guide"
    echo ""
    echo "📖 Quick Commands:"
    echo "   @workspace - Ask about project"
    echo "   #codebase - Search code"
    echo "   #file:path - Reference files"
    echo "   @terminal - Run commands"
else
    echo -e "${RED}⚠️  Some checks failed. Review the output above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Missing files: Create from templates in documentation/"
    echo "- Settings issues: Check .vscode/settings.json"
    echo "- Instructions: Ensure .github/copilot-instructions.md exists"
fi

echo ""
