#!/bin/bash

echo "🚀 Voice Q&A Mobile - GitHub Actions Setup"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Installing via Homebrew..."
    brew install git
fi

echo "✓ Git is installed"
echo ""

# Configure git if not configured
if [ -z "$(git config --global user.name)" ]; then
    echo "📝 Git not configured. Let's set it up:"
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    echo "✓ Git configured"
fi

echo ""
echo "📦 Initializing Git repository..."

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Add all files
git add .

# Create initial commit if needed
if ! git rev-parse HEAD > /dev/null 2>&1; then
    git commit -m "Initial commit: Voice Q&A Mobile App"
    echo "✓ Initial commit created"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository at: https://github.com/new"
echo "   - Name it: voice-qa-mobile"
echo "   - Make it Public (for free Actions)"
echo "   - Do NOT initialize with README"
echo ""
echo "2. Run these commands (replace YOUR_USERNAME):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/voice-qa-mobile.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Go to your repo's Actions tab to watch the build"
echo ""
echo "4. Download the APK from the Actions artifacts"
echo ""
echo "See GITHUB_BUILD_GUIDE.md for detailed instructions"
echo "=========================================="
