#!/bin/bash

echo "🚀 Automated GitHub Setup & Push"
echo "================================="
echo ""

# Check for git
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    brew install git
fi

# Check for GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI for easier setup..."
    brew install gh
    echo ""
    echo "Please run: gh auth login"
    echo "Then run this script again."
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "🔐 Please login to GitHub first:"
    gh auth login
fi

echo ""
read -p "Enter repository name (default: voice-qa-mobile): " repo_name
repo_name=${repo_name:-voice-qa-mobile}

read -p "Make repository public? (y/n, default: y): " is_public
is_public=${is_public:-y}

echo ""
echo "📝 Setting up Git repository..."

# Initialize git if needed
if [ ! -d ".git" ]; then
    git init
fi

# Add all files
git add .

# Commit if needed
if ! git rev-parse HEAD > /dev/null 2>&1; then
    git commit -m "Initial commit: Voice Q&A Mobile App with GitHub Actions"
fi

echo ""
echo "🌐 Creating GitHub repository..."

# Create repo
if [ "$is_public" = "y" ]; then
    gh repo create "$repo_name" --public --source=. --remote=origin --push
else
    gh repo create "$repo_name" --private --source=. --remote=origin --push
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Repository created and pushed!"
    echo "=========================================="
    echo ""
    echo "📍 Repository URL:"
    gh repo view --web --json url -q .url
    echo ""
    echo "🔨 GitHub Actions is now building your APK!"
    echo ""
    echo "To watch the build:"
    echo "  1. Go to: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/actions"
    echo "  2. Click on the running workflow"
    echo "  3. Wait 30-60 minutes for first build"
    echo "  4. Download APK from 'Artifacts' section"
    echo ""
    echo "Or run: gh run watch"
    echo "=========================================="
else
    echo ""
    echo "❌ Failed to create repository"
    echo "You can create it manually at: https://github.com/new"
    echo "Then run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/$repo_name.git"
    echo "  git push -u origin main"
fi
