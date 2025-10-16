#!/bin/bash

# Transport Management System - Platform Deployment Script

echo "🚀 Transport Management System - Platform Deployment"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - TMS ready for deployment"
fi

# Function to deploy to Railway
deploy_railway() {
    echo "🚂 Deploying to Railway..."
    echo "1. Go to https://railway.app"
    echo "2. Sign up with GitHub"
    echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "4. Select this repository"
    echo "5. Railway will auto-deploy!"
    echo ""
    echo "Your app will be live at: https://your-app-name.railway.app"
}

# Function to deploy to Render
deploy_render() {
    echo "🎨 Deploying to Render..."
    echo "1. Go to https://render.com"
    echo "2. Connect GitHub account"
    echo "3. Create 'Web Service'"
    echo "4. Select this repository"
    echo "5. Configure:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: gunicorn --bind 0.0.0.0:\$PORT wsgi:application"
    echo "6. Deploy!"
    echo ""
    echo "Your app will be live at: https://your-app-name.onrender.com"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🟣 Deploying to Heroku..."
    if ! command -v heroku &> /dev/null; then
        echo "Installing Heroku CLI..."
        brew install heroku/brew/heroku
    fi
    
    echo "1. Run: heroku login"
    echo "2. Run: heroku create your-app-name"
    echo "3. Run: git push heroku main"
    echo "4. Run: heroku run flask db upgrade"
    echo ""
    echo "Your app will be live at: https://your-app-name.herokuapp.com"
}

# Main menu
echo "Select deployment platform:"
echo "1) Railway (Recommended - Free)"
echo "2) Render (Free tier available)"
echo "3) Heroku (Paid plans)"
echo "4) Show all options"
echo "5) Exit"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        deploy_railway
        ;;
    2)
        deploy_render
        ;;
    3)
        deploy_heroku
        ;;
    4)
        echo "🌐 All Deployment Options:"
        echo ""
        deploy_railway
        echo ""
        deploy_render
        echo ""
        deploy_heroku
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📋 Important Notes:"
echo "- Default login: admin / admin123"
echo "- Change password after first login!"
echo "- Health check endpoint: /health"
echo ""
echo "✅ Deployment instructions provided above!"
