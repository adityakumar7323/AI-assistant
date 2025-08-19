#!/bin/zsh

echo "🤖 Aditya AI Google Gemini API Key Setup"
echo "========================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    exit 1
fi

# Check current API key
current_key=$(grep "GOOGLE_API_KEY=" .env | cut -d'=' -f2)

if [[ "$current_key" == "your-google-gemini-api-key-here" ]]; then
    echo "⚠️  You need to add your real Google Gemini API key!"
    echo ""
    echo "📝 Steps to get your API key:"
    echo "   1. Go to: https://aistudio.google.com/app/apikey"
    echo "   2. Sign in to your Google account"
    echo "   3. Click 'Create API key'"
    echo "   4. Copy the key (starts with 'AIza')"
    echo ""
    echo "✏️  Then edit the .env file:"
    echo "   code .env"
    echo "   # Replace the placeholder with your actual key"
    echo ""
    echo "🚀 After adding your key, run:"
    echo "   ./start.sh"
    echo ""
    
    # Ask if user wants to open the .env file
    echo "Would you like me to open the .env file for editing? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        code .env
        echo "✅ Opened .env file for editing"
        echo "   Replace 'your-google-gemini-api-key-here'"
        echo "   with your real API key from Google AI Studio"
    fi
    
elif [[ "$current_key" =~ ^sk-.+ ]]; then
    echo "✅ API key found! Starting Aditya AI..."
    echo ""
    
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
    
    # Start the application
    echo "🤖 Starting Aditya AI with Gemini integration..."
    "/Users/aditya/ai project/.venv/bin/python" app.py
    
else
    echo "⚠️  Invalid API key format. OpenAI keys start with 'sk-'"
    echo "   Please check your .env file and ensure the key is correct."
fi
