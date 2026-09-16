# Native and report codec integration02 — pending review

This successor combines native01's closed-profile/eight-output integration with
codec02's profile6 report reader (27,829,365 bytes/depth39), preserving the default
4MiB/depth32 envelope/descriptor boundary. Native algorithms, full IDL guard,
external joins and TS closure adapter are unchanged. See README-native01.md for
those inherited checks and limits.

Fresh eight-e/eight-f are identical. Seven output files are byte-identical to
native01; only report.ts changes to use the current larger reader. All six Rust
files therefore retain native01's9 tests,2 compile-fail doctests and scoped
Clippy qualification. They were not rebuilt merely for a TS reader change.
Strict TypeScript compilation passes with all inherited native/provider probes.
The combined reader passes71 generated checks:64 current report/envelope cases,
4,202,613-byte dense report exact round trip, unchanged default envelope refusal,
and unselected/stale profile/inventory refusal.

Initial emitting compilation required TS6's explicit rootDir; compile02 failure
is preserved. The corrected compile03 command supplies integrated02/generated
as rootDir. No generated/source code was changed to bypass that compiler rule.
Old check_integration.py and status files describe native01 historical bytes;
codec-integration-result02.json and status02.json describe this successor.

Both base sources have archive manifests checked before generation; the
formatter binary is pinned in addition to its retained source/Cargo.lock.
Declared compiler140 files, Node, prepared projection and renderTypes are checked.
This remains observed local reproduction; loader confinement, final reproducible
bootstrap, source semantic selection and independent review remain pending.
No product files were installed. Final closed source/inventory integration,
real native codec/admission/sender and host/report behavior remain unfinished.
