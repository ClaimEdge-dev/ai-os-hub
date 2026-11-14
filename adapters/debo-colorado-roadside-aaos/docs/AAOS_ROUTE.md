# DEBO Colorado: AAOS / Google Play route

Status BUILT SOURCE / STATIC QA ONLY. Not compiled, installed, approved or released.

Google car Play supports only eligible categories. We built a POI driver-optimized roadside search companion. The private Colorado maintenance, costs, diagnostics and photo archive remain in the separate existing v0.2 PWA, not in the car Play package.

Car POI app uses AndroidX Car App Library 1.7.0. It delegates nearby fuel, tire, repair and parts searches to an installed car navigation app with CarContext.ACTION_NAVIGATE, without reading car data or storing user location.

Required gates: Gradle build; Android Automotive OS emulator and Google Templates Host render and tap verification; navigation intent test; host validation, driving state and car quality tests; actual 2024 Colorado Google built-in compatibility and Google Play Console availability; review for legitimate POI category; developer registration and explicit approval for public release. No sideload/security bypass.

Do not reclassify vehicle repair dashboard as navigation, media, game, browser or other ineligible category. Do not publish private vehicle data in the DEBO Core public repository.

References: https://developer.android.com/training/cars/apps/poi ; https://developer.android.com/training/cars/apps/automotive-os ; https://developer.android.com/training/cars/distribute
