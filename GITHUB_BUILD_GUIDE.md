# Building Android APK with GitHub Actions

This guide shows you how to build your Android APK automatically using GitHub Actions (completely free, no local Linux needed).

---

## Why GitHub Actions?

✅ **Free** - Unlimited builds for public repos  
✅ **No Linux needed** - Runs in the cloud  
✅ **Automatic** - Builds on every push  
✅ **Fast** - Parallel builds, cached dependencies  
✅ **Easy** - Just push code, get APK  

---

## Step-by-Step Guide

### Step 1: Create GitHub Account (if you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process

### Step 2: Install Git on Your Mac

```bash
# Check if Git is installed
git --version

# If not installed, install via Homebrew
brew install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Initialize Git Repository

```bash
cd /Users/rajanarenderreddylingaladinne/CascadeProjects/voice-qa-app-mobile

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Voice Q&A Mobile App"
```

### Step 4: Create GitHub Repository

**Option A - Via GitHub Website:**

1. Go to https://github.com/new
2. Repository name: `voice-qa-mobile`
3. Description: "Voice Q&A Assistant - Android Mobile App"
4. Choose **Public** (for free Actions) or **Private** (still free for Actions)
5. **Do NOT** initialize with README (you already have files)
6. Click "Create repository"

**Option B - Via GitHub CLI:**

```bash
# Install GitHub CLI
brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create voice-qa-mobile --public --source=. --remote=origin --push
```

### Step 5: Push Code to GitHub

If you created the repo via website, run:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/voice-qa-mobile.git

# Push code
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 6: Verify GitHub Actions Workflow

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/voice-qa-mobile`
2. Click on the **"Actions"** tab
3. You should see the workflow "Build Android APK" running
4. Click on it to watch the build progress

### Step 7: Wait for Build to Complete

⏱️ **First build**: 30-60 minutes (downloads Android SDK/NDK)  
⏱️ **Subsequent builds**: 10-20 minutes (uses cache)

The build will:
- Set up Ubuntu Linux environment
- Install Android SDK and NDK
- Install Python dependencies
- Compile the APK
- Upload the APK as an artifact

### Step 8: Download Your APK

Once the build completes:

1. Go to the **Actions** tab
2. Click on the completed workflow run
3. Scroll down to **"Artifacts"**
4. Download **"voice-qa-app-debug"**
5. Unzip the downloaded file
6. You'll find `voiceqa-0.1-debug.apk`

### Step 9: Install APK on Android

**Method 1 - USB:**
```bash
adb install voiceqa-0.1-debug.apk
```

**Method 2 - Direct Transfer:**
1. Copy APK to your phone (email, Google Drive, etc.)
2. Open the APK file on your phone
3. Allow "Install from Unknown Sources"
4. Install the app

---

## Automatic Builds

The workflow is configured to build automatically when you:

- **Push to main branch** - Builds on every code change
- **Create pull request** - Builds to test changes
- **Manual trigger** - Click "Run workflow" in Actions tab

---

## Creating Releases

To create a release version with a version number:

```bash
# Tag your release
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Build the APK
- Create a GitHub Release
- Attach the APK to the release
- Make it easy to share/download

---

## Troubleshooting

### Build Fails

**Check the logs:**
1. Go to Actions tab
2. Click on the failed build
3. Expand the failed step
4. Read the error message

**Common issues:**

**"Buildozer failed"**
- Check `buildozer.spec` configuration
- Verify all requirements are listed

**"Permission denied"**
- GitHub Actions has all needed permissions by default
- No action needed

**"Out of disk space"**
- Reduce APK size by removing large models
- Use smaller Whisper model

### Build Takes Too Long

**First build**: Normal (30-60 min)  
**Subsequent builds**: Should be faster (10-20 min) due to caching

If still slow:
- Check if caching is working
- Reduce dependencies in `requirements.txt`

### APK Won't Install

**"App not installed"**
- Enable "Unknown Sources" in Android settings
- Check Android version (need 8.0+)
- Verify APK isn't corrupted (re-download)

---

## Advanced: Build Signed APK for Play Store

### Step 1: Generate Keystore

```bash
keytool -genkey -v -keystore voiceqa.keystore \
  -alias voiceqa -keyalg RSA -keysize 2048 -validity 10000
```

### Step 2: Add Secrets to GitHub

1. Go to repository Settings → Secrets and variables → Actions
2. Add these secrets:
   - `KEYSTORE_FILE` - Base64 encoded keystore
   - `KEYSTORE_PASSWORD` - Your keystore password
   - `KEY_ALIAS` - Your key alias
   - `KEY_PASSWORD` - Your key password

```bash
# Encode keystore to base64
base64 voiceqa.keystore | pbcopy
# Paste this as KEYSTORE_FILE secret
```

### Step 3: Update Workflow

Add signing step to `.github/workflows/build-apk.yml`:

```yaml
- name: Sign APK
  run: |
    echo "${{ secrets.KEYSTORE_FILE }}" | base64 -d > voiceqa.keystore
    jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
      -keystore voiceqa.keystore \
      -storepass "${{ secrets.KEYSTORE_PASSWORD }}" \
      -keypass "${{ secrets.KEY_PASSWORD }}" \
      bin/*.apk "${{ secrets.KEY_ALIAS }}"
```

---

## Monitoring Builds

### Email Notifications

GitHub sends email notifications when builds:
- ✅ Succeed
- ❌ Fail

### Status Badge

Add to your README.md:

```markdown
![Build Status](https://github.com/YOUR_USERNAME/voice-qa-mobile/workflows/Build%20Android%20APK/badge.svg)
```

---

## Cost

**GitHub Actions for Public Repos**: FREE unlimited  
**GitHub Actions for Private Repos**: 2,000 minutes/month FREE  

Each build uses ~30-60 minutes, so you get:
- **Public repo**: Unlimited builds
- **Private repo**: ~30-60 builds/month free

---

## Next Steps

After successful build:

1. ✅ **Test APK** on multiple Android devices
2. ✅ **Get feedback** from beta testers
3. ✅ **Fix bugs** and push updates (auto-builds)
4. ✅ **Create release** with version tag
5. ✅ **Publish** to Play Store or share directly

---

## Quick Reference Commands

```bash
# Push updates (triggers build)
git add .
git commit -m "Update: description of changes"
git push

# Create release
git tag v1.0.1
git push origin v1.0.1

# Check build status
gh run list

# Download latest APK
gh run download
```

---

## Summary

1. **Push code to GitHub** ✅
2. **GitHub Actions builds APK automatically** ✅
3. **Download APK from Actions tab** ✅
4. **Install on Android** ✅
5. **Push updates → Auto-rebuild** ✅

No Linux needed, no local build setup, completely automated! 🚀
