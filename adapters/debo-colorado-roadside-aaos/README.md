# DEBO Roadside | Android Automotive OS POI companion v0.1

Source pilot only. Not built into an APK, not emulator-tested, not approved for Google Play, and not installed in a vehicle.

Purpose: a legitimate in-car points-of-interest companion that uses Google built-in's car templates to find fuel, tire services, auto repair, and auto parts by handing navigation queries to the car host. This is NOT the private DEBO Colorado maintenance dashboard, which remains the separate v0.2 iPhone/PWA application.

## Build
Open this folder in Android Studio; install JDK 17 and Android SDK 35. Gradle dependencies: Android Gradle Plugin 8.8.2, Kotlin 2.0.21, AndroidX Car App Library 1.7.0. Run `gradle :app:assembleDebug` or use Android Studio. Test on Android Automotive OS emulator with Google Automotive App Host and a navigation app, then do distraction/host-compatibility checks. Vehicle Play eligibility and publication require separate evaluation and approval.

## Security
No VIN, vehicle photos, repair records, odometer, owner details, passwords, OnStar integration, car sensor reads or location storage. Debug-only permissive host validation; release uses the known-host signature allowlist. This source does not include an unrestricted browser or WebView.

Official references:
https://developer.android.com/training/cars/apps/poi
https://developer.android.com/training/cars/apps/automotive-os
https://developer.android.com/training/cars/distribute
https://developer.android.com/reference/androidx/car/app/CarContext
