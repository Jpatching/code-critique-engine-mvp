#!/bin/bash
# Authentication System Verification Test
# Run this to verify all auth endpoints are working

echo "================================================"
echo "🧪 Authentication System Verification"
echo "================================================"
echo ""

API_URL="http://127.0.0.1:5000"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "Test 1: Checking API health..."
HEALTH=$(curl -s $API_URL/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ API is healthy${NC}"
else
    echo -e "${RED}❌ API is not responding${NC}"
    exit 1
fi
echo ""

# Test 2: Signup
echo "Test 2: Testing user signup..."
SIGNUP_EMAIL="verify-$(date +%s)@test.com"
SIGNUP_RESPONSE=$(curl -s -X POST $API_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$SIGNUP_EMAIL\",\"password\":\"testpass123\",\"passwordConfirm\":\"testpass123\",\"name\":\"Verification Test\"}")

if echo "$SIGNUP_RESPONSE" | grep -q "token"; then
    echo -e "${GREEN}✅ Signup successful${NC}"
    TOKEN=$(echo "$SIGNUP_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
    USER_ID=$(echo "$SIGNUP_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['id'])" 2>/dev/null)
    echo "   User ID: $USER_ID"
    echo "   Token: ${TOKEN:0:30}..."
else
    echo -e "${RED}❌ Signup failed${NC}"
    echo "Response: $SIGNUP_RESPONSE"
    exit 1
fi
echo ""

# Test 3: Login
echo "Test 3: Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$SIGNUP_EMAIL\",\"password\":\"testpass123\"}")

if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    echo -e "${GREEN}✅ Login successful${NC}"
    NEW_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
    echo "   New Token: ${NEW_TOKEN:0:30}..."
else
    echo -e "${RED}❌ Login failed${NC}"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi
echo ""

# Test 4: Protected Endpoint (with token)
echo "Test 4: Testing protected endpoint with valid token..."
ME_RESPONSE=$(curl -s $API_URL/auth/me \
  -H "Authorization: Bearer $TOKEN")

if echo "$ME_RESPONSE" | grep -q "user"; then
    echo -e "${GREEN}✅ Protected endpoint accessible${NC}"
    USER_EMAIL=$(echo "$ME_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['email'])" 2>/dev/null)
    echo "   Authenticated as: $USER_EMAIL"
else
    echo -e "${RED}❌ Protected endpoint failed${NC}"
    echo "Response: $ME_RESPONSE"
    exit 1
fi
echo ""

# Test 5: Protected Endpoint (without token)
echo "Test 5: Testing protected endpoint without token..."
NO_AUTH_RESPONSE=$(curl -s $API_URL/auth/me)

if echo "$NO_AUTH_RESPONSE" | grep -q "Missing authorization header"; then
    echo -e "${GREEN}✅ Protected endpoint properly rejects unauthenticated requests${NC}"
else
    echo -e "${RED}❌ Protected endpoint security check failed${NC}"
    echo "Response: $NO_AUTH_RESPONSE"
    exit 1
fi
echo ""

# Test 6: Invalid credentials
echo "Test 6: Testing login with wrong password..."
WRONG_PASS_RESPONSE=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$SIGNUP_EMAIL\",\"password\":\"wrongpassword\"}")

if echo "$WRONG_PASS_RESPONSE" | grep -q "Invalid email or password"; then
    echo -e "${GREEN}✅ Invalid credentials properly rejected${NC}"
else
    echo -e "${RED}❌ Invalid credentials check failed${NC}"
    echo "Response: $WRONG_PASS_RESPONSE"
    exit 1
fi
echo ""

# Test 7: Input validation
echo "Test 7: Testing input validation..."
INVALID_EMAIL_RESPONSE=$(curl -s -X POST $API_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"notanemail","password":"test123","passwordConfirm":"test123"}')

if echo "$INVALID_EMAIL_RESPONSE" | grep -q "Invalid email format"; then
    echo -e "${GREEN}✅ Input validation working${NC}"
else
    echo -e "${RED}❌ Input validation failed${NC}"
    echo "Response: $INVALID_EMAIL_RESPONSE"
    exit 1
fi
echo ""

# Summary
echo "================================================"
echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
echo "================================================"
echo ""
echo "Authentication system is fully functional:"
echo "  ✅ User signup"
echo "  ✅ User login"
echo "  ✅ JWT token generation"
echo "  ✅ Protected routes"
echo "  ✅ Authorization validation"
echo "  ✅ Error handling"
echo "  ✅ Input validation"
echo ""
echo "Next Steps:"
echo "  1. Open http://127.0.0.1:5500/auth.html in your browser"
echo "  2. Sign up for a new account"
echo "  3. See your name appear in the navigation!"
echo ""
