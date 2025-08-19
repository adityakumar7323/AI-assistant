#!/bin/bash

# Aditya AI Setup Script
echo "🤖 Setting up Aditya AI with OpenAI API..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "🔑 Please edit the .env file and add your OpenAI API key:"
    echo "   nano .env"
    echo ""
    echo "Replace 'your-openai-api-key-here' with your actual API key from:"
    echo "   https://platform.openai.com/api-keys"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo "🚀 To start Aditya AI, run:"
echo "   source .env && python app.py"
echo ""
echo "📖 Or manually set the environment variable:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo "   python app.py"
