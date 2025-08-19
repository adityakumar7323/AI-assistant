#!/bin/zsh

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found"
fi

# Start Aditya AI
echo "🤖 Starting Aditya AI..."
"/Users/aditya/ai project/.venv/bin/python" app.py
