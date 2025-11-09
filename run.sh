#!/bin/bash

# Language Translator AI - Run Script
# This script installs dependencies and runs the application

set -e

echo "🚀 Language Translator AI - Setup & Run"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating .env.example..."
    if [ ! -f .env.example ]; then
        echo "GOOGLE_GEMINI_API_KEY=your_api_key_here" > .env.example
        echo "📝 Please create a .env file with your Google Gemini API key"
        echo "   You can copy .env.example to .env and add your API key"
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Running Language Translator AI..."
echo ""

# Run the application
python3 app.py

