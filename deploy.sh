#!/bin/bash

# Transport Management System - Deployment Script
echo "🚀 Deploying Transport Management System..."

# Check if we're in the right directory
if [ ! -f "run.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
FLASK_APP=run.py python3 -m flask db upgrade

# Create uploads directory if it doesn't exist
echo "📁 Creating uploads directory..."
mkdir -p uploads

# Set production environment variables
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

echo "✅ Deployment setup complete!"
echo ""
echo "To run the application:"
echo "1. For development: python3 run.py"
echo "2. For production: gunicorn --bind 0.0.0.0:8000 wsgi:application"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the default password after first login!"
