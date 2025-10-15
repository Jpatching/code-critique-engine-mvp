# 🧠 Code Critique Engine MVP

This is a Minimum Viable Product (MVP) for an AI-powered code coaching tool. It uses a Python Flask backend to connect to the Google Gemini API, generating a "Code Mastery Score" and detailed refactoring reports based on custom best-practice criteria.

## 🚀 How to Run Locally

### 1. Prerequisites

* Python 3.8+
* A Gemini API Key (Available from Google AI Studio)
* VS Code with the Live Server extension
* PocketBase (included in repo)

### 2. Setup (Backend)

1.  **Clone/Download** this repository.
2.  **Open your terminal** in the project's root directory (`code-critique-engine-mvp`).
3.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set Your API Key:** You MUST set the key as an environment variable in the terminal session where you run the server.
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
6.  **Start PocketBase (Database):**
    ```bash
    # In a separate terminal
    ./pocketbase serve
    ```
    PocketBase will run on `http://127.0.0.1:8090`.

7.  **Start the Flask Backend:**
    ```bash
    python server.py
    ```
    The server will run on `http://127.0.0.1:5000`.

### 3. Setup (Frontend)

1.  In VS Code, open the project folder.
2.  Right-click `index.html` and select **"Open with Live Server"**.
    * This will open the frontend in your browser (usually on port 5500).

### 4. Usage

With PocketBase, Flask server, and Live Server all running:

1.  **Sign Up/Login** - You'll be prompted to create an account (authentication is required!)
2.  **Create a Project** - Add your tech stack and architecture details for context-aware analysis
3.  **Analyze Code** - Paste your AI-generated code and receive detailed critiques
4.  **View History** - See all your past analyses and track improvement over time

### 🔐 Authentication Required

**Important:** As of Week 1 completion, the system now requires user authentication. You must sign up before using any features. This enables:
- Saving your projects and analysis history
- Context-aware AI recommendations based on YOUR tech stack
- Tracking code quality improvements over time
- Multi-project management

See `AUTHENTICATION_FLOW.md` for technical details on how auth is enforced.

---

## 📚 Documentation

### Quick Links
- **`documentation/QUICK_START.md`** - Fast developer setup guide
- **`documentation/AUTHENTICATION_FLOW.md`** - Complete auth system documentation
- **`documentation/DOCUMENTATION_INDEX.md`** - Full documentation navigation guide
- **`documentation/PRODUCTION_ROADMAP.md`** - 8-week development plan
- **`documentation/IMPLEMENTATION_SUMMARY.md`** - Technical implementation details

### Testing
```bash
# Test authentication flow
./verify_auth.sh

# Test full system
./verify_system.sh
```

---

## 🎯 Project Status

**Phase:** Week 3-4 Complete ✅ → Moving to Week 5-6  
**Latest:** Enhanced analysis experience with tabbed reports and comparison features  

**Key Features:**
- ✅ User authentication (signup/login required)
- ✅ Project management with tech stack configuration
- ✅ Context-aware code analysis
- ✅ Analysis history tracking
- ✅ Multi-page SPA with routing
- ✅ Dashboard with statistics
- ✅ Tabbed analysis detail view (5 sections)
- ✅ Analysis comparison with score deltas
- ✅ Export to Markdown functionality

**Next Steps:**
- 🎯 Landing page with value proposition
- 🎯 Stripe payment integration
- 🎯 Pricing tiers and quota enforcement
- 🎯 Marketing features and analytics

See `documentation/PRODUCTION_ROADMAP.md` for the complete 8-week plan.

---

**Your project is now a full-featured SaaS application with user accounts, project context, and analysis history!**