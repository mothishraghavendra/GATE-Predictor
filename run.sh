#!/bin/bash

# GATE Mark Predictor - Run Script

echo "🎯 Starting GATE Mark Predictor..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists, if not create from example
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your SECRET_KEY before deploying to production"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Flask application..."
echo "📍 Access the application at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run the Flask app
python app.py
