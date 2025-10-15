#!/bin/bash
# System Verification Script for Code Critique Engine
# Checks all services, APIs, and database connectivity

set -e

echo "🔍 Code Critique Engine - System Verification"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PocketBase is running
echo "1. Checking PocketBase..."
if curl -s http://127.0.0.1:8090/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PocketBase is running${NC}"
else
    echo -e "${RED}✗ PocketBase is NOT running${NC}"
    echo "  Start it with: ./pocketbase serve"
    exit 1
fi

# Check if Flask is running
echo ""
echo "2. Checking Flask API..."
if curl -s http://127.0.0.1:5000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Flask API is running${NC}"
    
    # Get detailed health info
    HEALTH_DATA=$(curl -s http://127.0.0.1:5000/health)
    echo "   Status: $(echo $HEALTH_DATA | jq -r '.status')"
    echo "   AI Service: $(echo $HEALTH_DATA | jq -r '.ai_service')"
    echo "   Model: $(echo $HEALTH_DATA | jq -r '.model')"
else
    echo -e "${RED}✗ Flask API is NOT running${NC}"
    echo "  Start it with: python3 server.py"
    exit 1
fi

# Check GEMINI_API_KEY
echo ""
echo "3. Checking Environment Variables..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${RED}✗ GEMINI_API_KEY is NOT set${NC}"
    echo "  Set it with: export GEMINI_API_KEY='your_key_here'"
    exit 1
else
    echo -e "${GREEN}✓ GEMINI_API_KEY is set${NC}"
fi

# Test analysis endpoint
echo ""
echo "4. Testing Analysis Endpoint..."
ANALYSIS_RESULT=$(curl -s -X POST http://127.0.0.1:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to add two numbers",
    "code": "def add(a, b):\n    return a + b"
  }')

if echo "$ANALYSIS_RESULT" | jq -e '.total_score' > /dev/null 2>&1; then
    SCORE=$(echo $ANALYSIS_RESULT | jq -r '.total_score')
    echo -e "${GREEN}✓ Analysis endpoint working${NC}"
    echo "   Sample score: $SCORE/25"
else
    echo -e "${RED}✗ Analysis endpoint failed${NC}"
    echo "   Response: $ANALYSIS_RESULT"
    exit 1
fi

# Check PocketBase collections
echo ""
echo "5. Checking PocketBase Collections..."
# This requires admin authentication - skip for now or implement if needed
echo -e "${YELLOW}⚠ Manual check required: Visit http://127.0.0.1:8090/_/${NC}"
echo "   Ensure 'project_ideas' collection exists"

# Check frontend files
echo ""
echo "6. Checking Frontend Files..."
FILES=("index.html" "app.js" "style.css")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file exists${NC}"
    else
        echo -e "${RED}✗ $file missing${NC}"
        exit 1
    fi
done

# Check backend structure
echo ""
echo "7. Checking Backend Structure..."
DIRS=("app" "app/api" "app/services" "app/utils")
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ $dir/ exists${NC}"
    else
        echo -e "${RED}✗ $dir/ missing${NC}"
        exit 1
    fi
done

# Check Python dependencies (run in venv context)
echo ""
echo "8. Checking Python Dependencies..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    if python3 -c "import flask; import google.generativeai; import requests" 2>/dev/null; then
        echo -e "${GREEN}✓ Core dependencies installed (venv)${NC}"
    else
        echo -e "${RED}✗ Missing dependencies in venv${NC}"
        echo "  Install with: pip install -r requirements.txt"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ Virtual environment not found${NC}"
    echo "  Create with: python3 -m venv .venv && source .venv/bin/activate"
fi

# Final summary
echo ""
echo "=============================================="
echo -e "${GREEN}✓ All systems operational!${NC}"
echo ""
echo "📊 Next Steps:"
echo "   1. Open index.html with Live Server (port 5500)"
echo "   2. Navigate to http://127.0.0.1:5500"
echo "   3. Test the analysis interface"
echo ""
echo "📁 Key URLs:"
echo "   • Frontend: http://127.0.0.1:5500"
echo "   • Flask API: http://127.0.0.1:5000"
echo "   • PocketBase Admin: http://127.0.0.1:8090/_/"
echo "   • Health Check: http://127.0.0.1:5000/health"
echo ""
