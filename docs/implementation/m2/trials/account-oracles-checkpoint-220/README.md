# Native account oracles and private debug output — checkpoint220

Private unselected/uninstalled successor to218;356files355unchanged,onlyplatform/account.rs. No lookup algorithm, dependency, fixture, schema or API-shape change. Proposed inventoryv52 covers this module but remains unselected.

ActualClaude218T1: real OS adapter was tested only for absolute home. A macOS-only independent getpwuid oracle now copies libc's documented thread-specific pw_dir before any further same-thread lookup and compares exact bytes to observe_account, with boolean-only failure output. Never uses HOME or prints either path. The test is deliberately not compiled on Linux, where static non-reentrant storage has different thread-safety constraints. A separate actual one-byte getpwuid_r call must yield LargerBuffer/ERANGE. No fabricated unused UID or extra name-service census. Existing bounded/reentrant production lookup unchanged.

218W1: AccountObservation now has a manual Debug emitting only AccountObservation { .. }, with a test over synthetic values. Real/effective UIDs and raw home remain accessible only through explicit getters. No log/trace integration or authority claim introduced. Source proof against mutation is not an OS-failure/sanitizer guarantee;218's remaining fault-injection limits and no Linux execution remain.

Validation:50platform/strictworkspaceClippy-r1PASS. Three compiled mutants plusbaselinePASS: shell-instead-home, realERANGE-as-error, debug-home-disclosure. Host132236sources51deps467workspace+2docs/build/metadata/version/help/source-lockunchangedPASS,HOME/TMPDIR absent. No failed local round. Current macOS host only; full actor/custody/discovery/lease/admission, formal source/runtime selection and cumulative readiness remain owed. Fresh actual review required.
