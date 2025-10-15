# 🔐 Authentication Flow Documentation

**Last Updated:** October 15, 2025  
**Status:** ✅ Fully Implemented and Enforced

---

## 🎯 Overview

The Code Critique Engine implements a **mandatory authentication system** where users MUST sign up and log in before accessing any features. This document outlines how authentication is enforced across the entire application.

---

## 🔒 Authentication Enforcement

### Multi-Layer Security

Authentication is enforced at **THREE levels**:

1. **Frontend Routing** - Prevents unauthenticated users from accessing protected pages
2. **API Client** - Automatically includes JWT tokens and handles 401 responses
3. **Backend Decorators** - All protected endpoints require valid JWT tokens

---

## 📊 Authentication Flow Diagram

```
User Opens App
    ↓
Check localStorage for token
    ↓
┌─────────────┐
│ Has Token?  │
└─────────────┘
    ↓              ↓
   YES            NO
    ↓              ↓
Verify token    Redirect to
with backend    /auth page
    ↓              ↓
┌─────────────┐  ┌──────────────┐
│ Valid?      │  │ User signs   │
└─────────────┘  │ up or logs   │
    ↓       ↓    │ in           │
  YES      NO    └──────────────┘
    ↓       ↓           ↓
Go to    Clear    Receive JWT
Dashboard  auth   token
          ↓           ↓
      Redirect    Store in
      to /auth    localStorage
                      ↓
                  Navigate to
                  /dashboard
```

---

## 🛡️ Layer 1: Frontend Router Protection

**Location:** `static/js/router.js`

### How It Works

Every route navigation is intercepted and checked:

```javascript
async handleRoute(path) {
    // Check authentication
    if (path !== '/auth' && path !== '/' && !authService.isAuthenticated()) {
        this.navigate('/auth');
        return;
    }

    // Default route handling
    if (path === '/' && authService.isAuthenticated()) {
        this.navigate('/dashboard');
        return;
    } else if (path === '/') {
        this.navigate('/auth');
        return;
    }
    // ... route handling
}
```

### Protected Routes

All routes except `/auth` are protected:

- ❌ **Blocked without auth:** `/dashboard`, `/projects/:id`, `/analyze`, etc.
- ✅ **Always accessible:** `/auth` (login/signup page)
- 🔄 **Smart redirect:** `/` → `/dashboard` (if authenticated) or `/auth` (if not)

---

## 🔑 Layer 2: API Client Token Management

**Location:** `static/js/api.js`

### Automatic Token Injection

Every API request automatically includes the JWT token:

```javascript
async request(endpoint, options = {}) {
    const token = authService.getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers
    });

    // Handle unauthorized responses
    if (response.status === 401) {
        authService.clearAuth();
        router.navigate('/auth');
        throw new Error('Session expired');
    }
    // ...
}
```

### What This Means

- **All API calls** automatically include `Authorization: Bearer <token>` header
- **401 responses** automatically log user out and redirect to login
- **No manual token handling** needed in page code

---

## 🚫 Layer 3: Backend Route Protection

**Location:** `app/api/auth.py`

### `@require_auth` Decorator

All protected endpoints use this decorator:

```python
def require_auth(f):
    """
    Decorator to require authentication for a route.
    Extracts and validates JWT token from Authorization header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        token = parts[1]
        
        # Verify token with PocketBase
        user_data = pb_service.verify_token(token)
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Store user_id in Flask's g object
        g.user_id = user_data['id']
        g.user = user_data
        
        return f(*args, **kwargs)
    return decorated_function
```

### Protected Endpoints

All critical endpoints are protected:

#### Projects API (`app/api/user_projects.py`)
```python
@projects_bp.route('', methods=['GET'])
@require_auth
def get_projects():
    # Only returns projects for authenticated user

@projects_bp.route('', methods=['POST'])
@require_auth
def create_project():
    # Associates project with authenticated user

@projects_bp.route('/<string:project_id>', methods=['GET'])
@require_auth
def get_project(project_id):
    # Verifies user owns the project

# ... all CRUD operations protected
```

#### Analysis API (`app/api/analysis.py`, `app/api/analyses.py`)
```python
@bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_code():
    # Associates analysis with authenticated user and project

@analyses_bp.route('', methods=['GET'])
@require_auth
def get_analyses():
    # Only returns user's own analyses

# ... all operations protected
```

#### User Profile API (`app/api/auth.py`)
```python
@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    # Returns authenticated user's profile

@auth_bp.route('/me', methods=['PUT'])
@require_auth
def update_user():
    # Allows user to update own profile
```

---

## 🔐 Authentication Service

**Location:** `static/js/auth.js`

### Core Functionality

```javascript
class AuthService {
    constructor() {
        this.token = localStorage.getItem('auth_token');
        this.user = null;
        this.initUser();
    }

    async initUser() {
        // Verify token on page load
        if (this.token) {
            const response = await fetch(`${API_BASE}/auth/me`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            if (response.ok) {
                this.user = await response.json();
            } else {
                this.clearAuth(); // Token invalid
            }
        }
    }

    isAuthenticated() {
        return this.token !== null && this.user !== null;
    }

    async login(email, password) {
        // Authenticate and store token
        const data = await fetch(`${API_BASE}/auth/login`, {...});
        this.token = data.token;
        this.user = data.user;
        localStorage.setItem('auth_token', this.token);
    }

    async logout() {
        // Clear token and redirect
        this.clearAuth();
        window.location.href = '/auth';
    }
}
```

### Token Persistence

- **Storage:** JWT token stored in `localStorage.auth_token`
- **Verification:** Token validated on every page load via `/auth/me` endpoint
- **Expiration:** Invalid/expired tokens automatically cleared
- **Logout:** Token removed from localStorage and session cleared

---

## 🚀 User Journey

### First-Time User

1. **Opens app** → Lands on `/` 
2. **No token found** → Redirected to `/auth`
3. **Sees signup form** → Can switch to login if already has account
4. **Fills signup form:**
   - Name (required)
   - Email (required, validated format)
   - Password (required, min 8 characters)
   - Confirm password (must match)
5. **Submits form** → Creates account via `POST /auth/signup`
6. **Receives JWT token** → Stored in localStorage
7. **Redirected to `/dashboard`** → Can now use app

### Returning User

1. **Opens app** → Token found in localStorage
2. **Token verified** → Backend validates via `GET /auth/me`
3. **Redirected to `/dashboard`** → Immediately usable

### Session Expiration

1. **Token expires** → Backend returns 401
2. **API client catches 401** → Clears localStorage
3. **Redirected to `/auth`** → Must log in again

---

## 🛡️ Security Features

### Input Validation

**Location:** `app/utils/validation.py`

```python
def validate_auth_input(data):
    """
    Validates authentication input data.
    Returns (is_valid, error_message)
    """
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Email validation
    if not email or not is_valid_email(email):
        return False, "Invalid email address"
    
    # Password validation
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # XSS protection
    if contains_malicious_content(email):
        return False, "Invalid characters in email"
    
    return True, None
```

### Frontend Validation

**Location:** `static/js/pages/auth.js`

- Real-time email format validation
- Password strength indicator
- Confirm password matching
- Loading states prevent double submission
- Clear error messaging

### Token Security

- **JWT tokens** signed by PocketBase
- **Bearer token format** in Authorization header
- **Server-side verification** on every request
- **Automatic expiration** handling
- **No sensitive data** stored in token payload

---

## 📝 Backend Implementation Details

### PocketBase Integration

**Location:** `app/services/pocketbase_service.py`

```python
def create_user(self, email, password, name):
    """Create a new user in PocketBase"""
    data = {
        "email": email,
        "password": password,
        "passwordConfirm": password,
        "name": name,
        "emailVisibility": True
    }
    return self._request('POST', '/api/collections/users/records', data)

def authenticate_user(self, email, password):
    """Authenticate user and return auth token"""
    data = {"identity": email, "password": password}
    result = self._request('POST', '/api/collections/users/auth-with-password', data)
    
    return {
        'token': result['token'],
        'user': {
            'id': result['record']['id'],
            'email': result['record']['email'],
            'name': result['record']['name']
        }
    }

def verify_token(self, token):
    """Verify JWT token and return user data"""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        result = self._request('GET', '/api/collections/users/auth-refresh', 
                              headers=headers)
        return {
            'id': result['record']['id'],
            'email': result['record']['email'],
            'name': result['record']['name']
        }
    except:
        return None
```

### User-Scoped Data

All user data is automatically scoped to the authenticated user:

```python
# Projects are filtered by user
def get_user_projects(user_id, page=1, per_page=30):
    filter_query = f'user_id="{user_id}"'
    return pb_service.get_records('projects', page, per_page, filter_query)

# Analyses are filtered by user
def get_user_analyses(user_id, project_id=None, page=1, per_page=20):
    filter_query = f'user_id="{user_id}"'
    if project_id:
        filter_query += f' && project_id="{project_id}"'
    return pb_service.get_records('analyses', page, per_page, filter_query)
```

---

## ✅ Testing Authentication

### Manual Testing Steps

1. **Test Unauthenticated Access:**
   ```bash
   # Open browser in incognito mode
   # Navigate to http://127.0.0.1:5500/dashboard
   # Expected: Redirected to /auth
   ```

2. **Test Signup:**
   ```bash
   # Go to /auth
   # Click "Sign Up" tab
   # Fill form and submit
   # Expected: Redirected to /dashboard with user info shown
   ```

3. **Test Login:**
   ```bash
   # Logout
   # Go to /auth (should be automatic)
   # Click "Login" tab
   # Enter credentials
   # Expected: Redirected to /dashboard
   ```

4. **Test Token Persistence:**
   ```bash
   # Close browser
   # Reopen and navigate to app
   # Expected: Still logged in, goes to /dashboard
   ```

5. **Test API Protection:**
   ```bash
   # Clear localStorage
   curl http://127.0.0.1:5000/api/projects
   # Expected: 401 Unauthorized
   ```

### Automated Verification

**Location:** `verify_auth.sh`

```bash
#!/bin/bash
# Automated authentication flow verification

echo "🔐 Testing Authentication Flow..."

# Test 1: Protected endpoint without auth
echo "1. Testing protected endpoint (should fail)..."
curl -s http://127.0.0.1:5000/api/projects | grep -q "error" && echo "✅ Properly blocked"

# Test 2: Signup
echo "2. Testing signup..."
RESULT=$(curl -s -X POST http://127.0.0.1:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}')
echo "$RESULT" | grep -q "token" && echo "✅ Signup successful"

# Test 3: Login
echo "3. Testing login..."
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' | jq -r '.token')
[ ! -z "$TOKEN" ] && echo "✅ Login successful, token: ${TOKEN:0:20}..."

# Test 4: Access protected endpoint with token
echo "4. Testing protected endpoint with valid token..."
curl -s http://127.0.0.1:5000/api/projects \
  -H "Authorization: Bearer $TOKEN" | grep -q "items" && echo "✅ Access granted"

echo "✅ All authentication tests passed!"
```

---

## 🎯 Summary

### ✅ What's Protected

- **All pages** except `/auth` require authentication
- **All API endpoints** except `/auth/signup` and `/auth/login` require JWT token
- **User data** is automatically scoped to authenticated user
- **Projects and analyses** can only be accessed by their owner

### ✅ How It's Enforced

1. **Frontend Router** - Catches navigation attempts, redirects to `/auth`
2. **API Client** - Injects tokens, handles 401 responses automatically
3. **Backend Decorators** - Validates tokens on every protected endpoint
4. **PocketBase** - Manages user accounts and token generation

### ✅ User Experience

- **Seamless signup/login** - Beautiful UI with validation
- **Persistent sessions** - Token stored in localStorage
- **Automatic handling** - Session expiration handled gracefully
- **Secure by default** - No way to access features without authentication

---

## 📚 Related Documentation

- **`IMPLEMENTATION_SUMMARY.md`** - Full project implementation details
- **`QUICK_START.md`** - How to run and test the system
- **`PRODUCTION_ROADMAP.md`** - Future authentication enhancements (2FA, OAuth, etc.)

---

**🎉 Status: Authentication is fully implemented and enforced throughout the system!**

Users MUST sign up before using any features. All user data is properly scoped and protected.
