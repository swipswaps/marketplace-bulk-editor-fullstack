#!/bin/bash

# Marketplace Bulk Editor - Backend Startup Script

echo "========================================="
echo "Marketplace Bulk Editor - Backend"
echo "========================================="
echo ""

# Check if --skip-checks flag is provided
SKIP_CHECKS=false
if [[ "$1" == "--skip-checks" ]]; then
    SKIP_CHECKS=true
    echo "⚠ Skipping pre-flight checks (--skip-checks flag provided)"
    echo ""
fi

# Run pre-flight checks unless skipped
if [ "$SKIP_CHECKS" = false ]; then
    if [ -f "pre-flight.sh" ]; then
        echo "Running pre-flight checks..."
        chmod +x pre-flight.sh
        ./pre-flight.sh
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Pre-flight checks failed. Fix errors or run with --skip-checks"
            exit 1
        fi
        echo ""
        echo "========================================="
        echo "STARTING BACKEND SERVER"
        echo "========================================="
        echo ""
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

# Create logs directory
mkdir -p logs

# Initialize database
echo "Initializing database..."
python init_db.py

# Start Flask development server
echo ""
echo "========================================="
echo "Starting Flask development server..."
echo "API will be available at http://localhost:5000"
echo "========================================="
echo ""

export FLASK_APP=app.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000 --debug

