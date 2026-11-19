
[app]

title = Taha Drift
package.name = tahadrift
package.domain = org.tahagames

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0.0

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

p4a.branch = v2024.01.21
p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1

