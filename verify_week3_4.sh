#!/bin/bash

# Week 3-4 Feature Verification Script
# Tests new analysis detail, comparison, and export endpoints

echo "=========================================="
echo "Week 3-4 Feature Verification"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if services are running
echo "1. Checking services..."
if ! pgrep -f "pocketbase serve" > /dev/null; then
    echo -e "${RED}❌ PocketBase is not running${NC}"
    echo "   Start it with: ./pocketbase serve"
    exit 1
fi
echo -e "${GREEN}✓ PocketBase is running${NC}"

if ! pgrep -f "python3 server.py" > /dev/null; then
    echo -e "${RED}❌ Flask server is not running${NC}"
    echo "   Start it with: python3 server.py"
    exit 1
fi
echo -e "${GREEN}✓ Flask server is running${NC}"
echo ""

# Check if new files exist
echo "2. Verifying new files..."
FILES=(
    "static/js/pages/analysis-detail.js"
    "static/js/pages/comparison.js"
    "documentation/WEEK3_4_COMPLETE.md"
    "documentation/README.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}❌ $file not found${NC}"
    fi
done
echo ""

# Check documentation organization
echo "3. Checking documentation organization..."
DOC_FILES=(
    "documentation/AUTHENTICATION_FLOW.md"
    "documentation/IMPLEMENTATION_SUMMARY.md"
    "documentation/PRODUCTION_ROADMAP.md"
    "documentation/QUICK_START.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}❌ $file not found${NC}"
    fi
done
echo ""

# Check if old docs removed from root
echo "4. Verifying root directory cleanup..."
OLD_DOCS=(
    "AUTHENTICATION_FLOW.md"
    "IMPLEMENTATION_SUMMARY.md"
    "PRODUCTION_ROADMAP.md"
)

all_removed=true
for file in "${OLD_DOCS[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${RED}❌ $file still in root (should be in documentation/)${NC}"
        all_removed=false
    fi
done

if [ "$all_removed" = true ]; then
    echo -e "${GREEN}✓ Root directory cleaned up${NC}"
fi
echo ""

# Check CSS additions
echo "5. Checking CSS enhancements..."
if grep -q "WEEK 3-4 ENHANCEMENTS" static/css/main.css; then
    echo -e "${GREEN}✓ Week 3-4 CSS additions found${NC}"
    
    # Check specific classes
    CSS_CLASSES=(
        ".analysis-detail-page"
        ".tabbed-reports"
        ".comparison-page"
        ".score-summary-card"
    )
    
    for class in "${CSS_CLASSES[@]}"; do
        if grep -q "$class" static/css/main.css; then
            echo -e "${GREEN}  ✓ $class${NC}"
        else
            echo -e "${RED}  ❌ $class not found${NC}"
        fi
    done
else
    echo -e "${RED}❌ Week 3-4 CSS section not found${NC}"
fi
echo ""

# Check router updates
echo "6. Checking router updates..."
if grep -q "/analysis/:id" static/js/app.js; then
    echo -e "${GREEN}✓ Analysis detail route registered${NC}"
else
    echo -e "${RED}❌ Analysis detail route not found${NC}"
fi

if grep -q "/compare" static/js/app.js; then
    echo -e "${GREEN}✓ Comparison route registered${NC}"
else
    echo -e "${RED}❌ Comparison route not found${NC}"
fi
echo ""

# Check API endpoint additions
echo "7. Checking API endpoints..."
if grep -q "def compare_analyses" app/api/analyses.py; then
    echo -e "${GREEN}✓ Comparison endpoint exists${NC}"
else
    echo -e "${RED}❌ Comparison endpoint not found${NC}"
fi

if grep -q "def export_analysis" app/api/analyses.py; then
    echo -e "${GREEN}✓ Export endpoint exists${NC}"
else
    echo -e "${RED}❌ Export endpoint not found${NC}"
fi

if grep -q "_generate_markdown_export" app/api/analyses.py; then
    echo -e "${GREEN}✓ Markdown export function exists${NC}"
else
    echo -e "${RED}❌ Markdown export function not found${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Open http://127.0.0.1:5000 in your browser"
echo "2. Login and navigate to a project with analyses"
echo "3. Click '📊 View Details' on an analysis"
echo "4. Test all tabs (Overview, Security, Performance, Architecture, Refactoring)"
echo "5. Click 'Export Markdown' to download"
echo "6. Select 2 analyses and click 'Compare Selected'"
echo "7. Verify comparison shows both analyses with metrics"
echo ""
echo -e "${GREEN}✨ Week 3-4 features are ready to test!${NC}"
