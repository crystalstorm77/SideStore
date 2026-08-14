# Basic HealthKit support for free Personal Teams

This branch builds SideStore 0.6.3 with a narrowly scoped AltSign patch for
basic HealthKit access. It does not enable sensitive clinical records,
background delivery, or any private entitlement.

The input application's `com.apple.developer.healthkit` entitlement is mapped
to Apple's `HK421J6T7P` App ID feature. Basic HealthKit is also retained when
SideStore requests a provisioning profile for a free Personal Team. AltSign's
existing profile-driven signer remains unchanged, so the entitlement is placed
in the installed application only when Apple includes it in the freshly issued
profile.

The pull-request workflow applies the guarded source transformation to the
pinned AltSign submodule, builds a fake-signed SideStore IPA, and verifies that
the compiled executable contains both the entitlement and App ID feature
identifiers. Final app signing continues to happen on the user's device through
SideStore.
