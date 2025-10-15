#!/bin/bash
# Quick Start Script - Code Critique Engine
# Run this to start Flask server with proper configuration

echo "🚀 Starting Code Critique Engine Flask Server..."
echo ""

# Export Gemini API Key
export GEMINI_API_KEY="AIzaSyBf0cGONzMrHzsGYY9Cm19g--B5PYrtWn8"

# Check if PocketBase is running
if ! pgrep -f "./pocketbase serve" > /dev/null; then
    echo "⚠️  WARNING: PocketBase is not running!"
    echo "You need to start PocketBase in a separate terminal:"
    echo "  cd /home/jp/dev\ projects/code-critique-engine-mvp"
    echo "  ./pocketbase serve"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run: python3 -m venv .venv"
    exit 1
fi

# Kill any existing server processes
echo "🧹 Cleaning up old server processes..."
pkill -9 -f "python3 server.py" 2>/dev/null
sleep 1

# Start Flask server in background
echo "✅ Starting Flask server with Gemini API..."
nohup python3 server.py > server.log 2>&1 &
SERVER_PID=$!

# Wait and verify
sleep 3
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started successfully (PID: $SERVER_PID)"
    echo "📊 Server log: tail -f server.log"
    echo "🌐 Access at: http://127.0.0.1:5000"
else
    echo "❌ Server failed to start. Check server.log for errors"
    exit 1
fi
