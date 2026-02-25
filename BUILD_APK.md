# Building the Android APK

This guide shows you how to build the Voice Q&A Assistant Android app.

---

## Prerequisites

### On macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install autoconf automake libtool pkg-config
brew install libffi openssl

# Install Python 3.10 (Kivy works best with 3.10)
brew install python@3.10

# Create virtual environment with Python 3.10
python3.10 -m venv venv
source venv/bin/activate

# Install buildozer and dependencies
pip install --upgrade pip
pip install buildozer cython==0.29.33
pip install -r requirements.txt
```

### On Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

pip3 install --upgrade pip
pip3 install buildozer cython==0.29.33
pip3 install -r requirements.txt
```

---

## Building the APK

### Step 1: Clean Previous Builds (Optional)

```bash
buildozer android clean
```

### Step 2: Build Debug APK

```bash
# This will take 30-60 minutes on first run
buildozer android debug
```

The APK will be created in: `bin/voiceqa-0.1-debug.apk`

### Step 3: Build Release APK (For Distribution)

```bash
buildozer android release
```

---

## Installing on Android Device

### Method 1: USB Installation

1. **Enable USB Debugging** on your Android device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times to enable Developer Mode
   - Go to Settings → Developer Options
   - Enable "USB Debugging"

2. **Connect device via USB**

3. **Install ADB** (if not already):
   ```bash
   # macOS
   brew install android-platform-tools
   
   # Linux
   sudo apt install adb
   ```

4. **Install the APK**:
   ```bash
   adb install bin/voiceqa-0.1-debug.apk
   ```

### Method 2: Direct Transfer

1. Copy `bin/voiceqa-0.1-debug.apk` to your phone
2. Open the file on your phone
3. Allow "Install from Unknown Sources" if prompted
4. Install the app

---

## Setting Up API Key on Android

The app needs your Anthropic API key. There are two ways to provide it:

### Option 1: Environment Variable (Build Time)

Before building, create a `.env` file:

```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

Then rebuild the APK.

### Option 2: Manual Entry (Runtime)

Modify `main.py` to add an API key input screen on first launch.

---

## Troubleshooting

### Build Fails with "Command failed"

```bash
# Clean and try again
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### "SDK not found" Error

Buildozer will download the Android SDK automatically. If it fails:

```bash
# Manually specify SDK path
export ANDROID_SDK_ROOT=$HOME/.buildozer/android/platform/android-sdk
```

### App Crashes on Launch

Check logs:
```bash
adb logcat | grep python
```

### Permissions Denied

Make sure `buildozer.spec` includes all required permissions:
- `INTERNET`
- `RECORD_AUDIO`
- `WRITE_EXTERNAL_STORAGE`

---

## Reducing APK Size

The full APK with all ML models will be ~500MB. To reduce size:

### Option 1: Use Cloud Speech Recognition

Replace local Whisper with Google Cloud Speech API or similar.

### Option 2: Download Models on First Run

Don't bundle models in APK, download them when app first runs.

### Option 3: Use Smaller Models

Replace `base` Whisper model with `tiny` model.

---

## Distribution Options

### 1. Direct APK Sharing
- Share the `.apk` file via Google Drive, email, etc.
- Users install directly (requires "Unknown Sources" permission)
- **Free**

### 2. Google Play Store
- Create a Google Play Developer account ($25 one-time fee)
- Upload signed APK
- Reaches millions of users
- Requires privacy policy and app review

### 3. F-Droid (Open Source)
- Free alternative to Play Store
- Only for open-source apps
- No fees, no review process

### 4. Amazon Appstore
- Alternative to Play Store
- Free to publish
- Smaller user base

---

## Building Signed APK for Play Store

```bash
# Generate keystore
keytool -genkey -v -keystore voiceqa.keystore -alias voiceqa -keyalg RSA -keysize 2048 -validity 10000

# Build release APK
buildozer android release

# Sign the APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore voiceqa.keystore bin/voiceqa-0.1-release-unsigned.apk voiceqa

# Align the APK
zipalign -v 4 bin/voiceqa-0.1-release-unsigned.apk bin/voiceqa-0.1-release.apk
```

---

## Testing the APK

Before distributing:

1. **Test on multiple devices** (different Android versions)
2. **Check permissions** work correctly
3. **Test microphone** recording
4. **Verify API calls** work
5. **Test voice enrollment** and recognition
6. **Check battery usage**

---

## Next Steps

After building the APK:

1. **Test thoroughly** on real devices
2. **Get feedback** from beta testers
3. **Optimize performance** (battery, speed)
4. **Add features**:
   - Wake word detection
   - Offline mode
   - Multiple language support
5. **Publish** to app store

---

## Estimated Timeline

- **First build**: 1-2 hours (mostly waiting)
- **Debugging**: 2-4 hours
- **Testing**: 1-2 hours
- **Play Store submission**: 1-2 days (review time)

**Total**: 1-2 days for a working APK
