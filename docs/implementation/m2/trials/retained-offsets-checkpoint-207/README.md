# Retained descriptor outer-layer regressions — checkpoint207

Frozen for actualClaude review; unselected/uninstalled.354productpins351unchanged205. Only security/lib.rs documentation,security/custody.rs test andstorage/store_root.rs test change. No production behavioral/API/dependency/SQL/publicschema changes;37fixtures unchanged.

205T1: the shared bounded reader consumes to EOF on success. Public-capture and marker tests now verify the retained File offset equals the length of nonempty captured bytes before any replacement. A descriptor reopened before method return would have offset0. This checks all three previously surviving reopen sites(publicfacade,boundwrapper,markerwrapper).3compiledmutants+baseline allcaught. This evidence is scoped to those regressions; an intentionally reopened-and-seeked handle is not proven impossible by an offset alone. Native same-object replacement and custody tests from205 remain.

205N2: file() documentation says metadata/policy checks;bytes() is captured evidence. Re-reading or seeking the shared-offset handle does not repeat the capture's brackets. No lease tie, continuous custody, admission or current-authority claim. 205N1 actualfuturesecurity-sidepolicyjoin stillowed.

91storage-r1/161security-r1/strictworkspaceClippy-r1PASS. No new isolatedhostlane for this test/documentation-only change:host127's448workspace+2docs qualifies its205sourcepins, not207's exact test source. Cumulativeinstallation checks stillowed. Actualparent205review archived separately. AllM2–M6remainopen.
