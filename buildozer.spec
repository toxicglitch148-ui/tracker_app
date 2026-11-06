[app]
title = SystemService
package.name = systemservice
package.domain = org.sys
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,requests,pyjnius,plyer,android
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_SMS,READ_CONTACTS,READ_CALL_LOG
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
orientation = portrait
android.accept_sdk_license = True
