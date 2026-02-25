# Voice Q&A Assistant - Mobile (Android)

A mobile version of the Voice Q&A Assistant app for Android devices.

## Features

- 🎤 Voice enrollment and recognition
- 🤖 AI-powered answers using Claude
- 📱 Touch-friendly mobile interface
- 🔋 Battery-optimized (push-to-talk)
- 🔒 Secure API key handling

## Quick Start

### Building the APK

```bash
# Install dependencies
pip install buildozer cython==0.29.33
pip install -r requirements.txt

# Build APK (first time takes 30-60 minutes)
buildozer android debug

# APK will be in: bin/voiceqa-0.1-debug.apk
```

### Installing on Android

```bash
# Via USB
adb install bin/voiceqa-0.1-debug.apk

# Or transfer the APK file to your phone and install directly
```

## Differences from Desktop Version

| Feature | Desktop | Mobile |
|---------|---------|--------|
| UI Framework | PySide6 (Qt) | Kivy |
| Listening Mode | Always-on | Push-to-talk |
| Model Size | Full (~2GB) | Optimized (~500MB) |
| Battery Impact | N/A | Optimized |
| Permissions | Microphone only | Microphone + Storage |

## Requirements

- Android 8.0+ (API 26+)
- 2GB RAM minimum
- Microphone
- Internet connection
- Anthropic API key

## Setup

1. **Get API Key**: https://console.anthropic.com/
2. **Add to app**: First launch will prompt for API key
3. **Grant permissions**: Microphone and storage access
4. **Enroll voice**: Record 15 seconds
5. **Start listening**: Tap the button to listen for questions

## Building from Source

See [BUILD_APK.md](BUILD_APK.md) for detailed build instructions.

## File Structure

```
voice-qa-app-mobile/
├── main.py              # Main Kivy app
├── buildozer.spec       # Android build configuration
├── requirements.txt     # Python dependencies
├── BUILD_APK.md        # Build instructions
└── README.md           # This file
```

## Troubleshooting

**App won't install**: Enable "Unknown Sources" in Android settings

**No microphone access**: Grant permissions in app settings

**API errors**: Check API key is correct and has credits

**App crashes**: Check `adb logcat` for error messages

## Distribution

- **Direct APK**: Share the `.apk` file
- **Google Play**: Requires developer account ($25)
- **F-Droid**: Free for open-source apps

## License

MIT License - Same as desktop version
