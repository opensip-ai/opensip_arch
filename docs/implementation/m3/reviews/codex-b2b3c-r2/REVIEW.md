# B2-b3c r2 review

Verdict: **ACCEPT-UNIT**. No required findings or new non-blocking observations.

## Exact subject and scope

Independently rehashed the 7,571-byte subject manifest to SHA-256 `6c592c677c30f95cdd3dae893c90b5436f588d216c318ebe957cb1737e5b7da2` and verified all 34 members' lengths and hashes. Verified all 12 authority pins, the product lock, and every product-map parent, candidate and archived byte set. The candidate's complete changed/untracked path set is exactly the five mapped paths. Product and architecture HEADs match the requested bases; product main is clean. Architecture has unrelated untracked E2s evidence paths, whose contents were not inspected or changed. The pinned authorities match despite those unrelated files.

The product lock still selects inventory v194 and has 164 contract successors. `configuration.rs` is unchanged. There is one new product path, `crates/host/src/discovery_flag_tests.rs`, for the separately reviewed inventory successor.

## Round-one corrections

**B2B3C-R1-RF-1 is resolved.** `OperationEnd::entered` distinguishes `NotEntered` from an entered end step. `failure` returns the failure for both `Failed` and `RolledOver { end: Err(..), .. }`; clean ends and `NotEntered` return none. These methods borrow existing values and create no authority or fixture gate.

`ScenarioHome::discover` now records `end_entered`, `end_rolled_over` and the separate `end_failure` row immediately after ending the operation, before projecting the discovery result. A returned discovery record therefore preserves its discovery outcome while exposing an end failure. The security unit control constructs a failed end and checks its host-I/O disclosure and the non-failing `NotEntered` case. The existing host control checks an entered, clean end without rollover. Their corresponding mutations are caught. This is a focused correction without a new failure-injection gate.

**B2B3C-R1-NBO-1 is addressed.** Accepted discovery results must produce a boundary inventory, canonical bytes and UTF-8 text, or return `Err`. Refused results do not request an inventory. Locator/conversion failures are no longer silently turned into a missing accepted inventory. The skipped-inventory mutation is caught.

## Composition, records and flag rows

The phase ordering follows amended plan r3 LD-B2B3-12: typed waiver; phase-one selection with the explicit path and `UpwardRecord`; resolver and immediate pack admission over captured carriers; item 5 with the waiver; tracking with empty environment/system sources; first registration when needed; operation handoff; `discovery_root`; downward walk/core on a fresh discovery ledger with the source selected before traversal; and end disclosure. Resolution refusal returns before item 5 and traversal. The registration/handoff follows the existing `InstallationAt::operation` composition.

Only existing X8 fixture gates are reached. The revision adds no feature site, shared-fixture widening or discovery-root constructor. The scratch home's owner uid is sound for this synthetic fixture's invoking account; it grants no production uid authority.

Selection and walker refusals are projected through `UpwardRecord::discovery_refusal` and `WalkRefusal::discovery_refusal`; unmapped infrastructure failures remain `Err`. Core typed discovery refusals remain records. The request, callback result and records contain plain paths, booleans, strings and collections; no operation, admission, receipt, descriptor or ledger is lent. End disclosure also contains only plain values.

The seven host controls retain the previously reviewed COV method: exact explicit selection from a different launch; invalid explicit selection before resolution; limited owner-waiver reach and rejection without an explicit project; configuration refusing consent impersonation; flag roots winning with flag-layer/source provenance; missing flag roots refusing without automatic fall-through; configuration-only and automatic cases; resolver/pack refusal before phase two; and cloneable records with a repeat discovery using a new writer. Foreign-owner coverage remains in the accepted predecessor vectors as plan r3 authorizes.

The host module is declared under `cfg(all(test, target_os = "macos"))` in `lib.rs`. Its real resolver callback performs resolution and pack admission. The pinned configuration test includes remain unchanged. COV's integration-test owner remains planned for J1; these controls do not establish public CLI composition.

## Verification

Independently executed only the three permitted checks:

- Source operability: 114 rows, no findings, passed.
- Environment-exception controls: 10 passed.
- FW-01 structural controls: 7 passed.

Inspected the hash-pinned lane-r3 evidence and its runner without executing the lane:

- All 13 checks report exit zero. Security passes increase from 1117 to 1118 with the same 14 named failures. Host passes increase from 336 to 343 with the same 8 named failures. These are unchanged baseline failure sets, not wholly passing Rust suites.
- All five legacy admission spend/outcome lines match.
- Locked/offline Clippy for host and security uses `--all-targets -- -D warnings` and has a successful completion log.
- Rustfmt classifies all five Rust paths. The four new/base-clean paths pass. `operation_handoff.rs` is format-dirty at both base and candidate and is explicitly excluded under the baseline classification; this is not a claim that all five files are format-clean.
- Scan/upward/walk vector checks and configuration-table controls report success. Supplied verify_design evidence reports success and selects v194 with qualification false.
- All eight mutations are caught; each supplied mutation log contains a failing-test summary matching its named controls, including end-failure hiding, omitted end recording and omitted accepted inventory.

No Cargo, rustc, Rust tests, builds, lane, Clippy, rustfmt, vector generator or verify_design was run during this review. Those outcomes are submitted evidence, distinct from the three independently executed checks.

No production caller, public composition, export, environment read or law change is added. Acceptance is for this exact unit. Lead assent/publication, the product commit and separately reviewed inventory successor remain publication/integration steps. B2-b4 and its all-entry margin gate, J1 composition and later work remain; neither product qualification nor entire-plan completion is claimed.

Only `REVIEW.md` and `review.json` were written. Neither repository, candidate, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, keys, held trees or T2 held-outs were accessed.
