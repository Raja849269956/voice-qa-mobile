[app]
title = Voice QA Assistant
package.name = voiceqa
package.domain = com.voiceqa

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy,anthropic,numpy,torch,torchaudio,speechbrain,faster-whisper,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
