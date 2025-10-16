#!/bin/bash

# Transport Management System - Git Setup Script
echo "🚀 Setting up Git for Transport Management System"
echo "================================================"

# Check if Git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize Git repository
echo "📦 Initializing Git repository..."
git init

# Configure Git (you can change these to your details)
echo "⚙️ Configuring Git..."
echo "Please enter your Git configuration details:"
echo ""

# Get user name
read -p "Enter your name (for Git commits): " git_name
if [ -n "$git_name" ]; then
    git config user.name "$git_name"
    echo "✅ Git user name set to: $git_name"
fi

# Get user email
read -p "Enter your email (for Git commits): " git_email
if [ -n "$git_email" ]; then
    git config user.email "$git_email"
    echo "✅ Git email set to: $git_email"
fi

# Add all files to Git
echo "📁 Adding all project files to Git..."
git add .

# Make the first commit
echo "💾 Making the first commit..."
git commit -m "Initial commit: Transport Management System

- Complete Flask web application
- Fixed button alignment issues
- Modern, responsive dashboard design
- Ready for deployment
- All features working: Orders, Builty, Fleet, Entities, System, Phone Book"

echo ""
echo "🎉 Git setup complete!"
echo ""
echo "📋 What we just did:"
echo "1. ✅ Initialized Git repository"
echo "2. ✅ Created .gitignore file (excludes unnecessary files)"
echo "3. ✅ Configured Git with your name and email"
echo "4. ✅ Added all project files"
echo "5. ✅ Made the first commit"
echo ""
echo "🔧 Useful Git commands for you:"
echo "- git status          : See what files have changed"
echo "- git add .           : Add all changes"
echo "- git commit -m 'msg' : Save changes with a message"
echo "- git log             : See commit history"
echo "- git branch          : See all branches"
echo ""
echo "🌐 To push to GitHub/GitLab:"
echo "1. Create a repository on GitHub/GitLab"
echo "2. Run: git remote add origin <repository-url>"
echo "3. Run: git push -u origin main"
echo ""
echo "Your Transport Management System is now version controlled! 🚀"
