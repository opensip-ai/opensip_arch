# B2-b3c r1 review

Verdict: **REQUIRED-FINDINGS**. One correction is required.

## Exact subject

Independently rehashed the 6,390-byte subject manifest to SHA-256 `7cc7c41e5e4ce2dc92e3580eb55732c78f2595b4550b1a6c5e24b3f243c2a9b7`. All 29 members match their declared lengths and hashes. All three product-map paths match the candidate worktree, staged archive and parent bytes, and equal the complete worktree change set. All twelve source authority pins and the product-lock pin match.

Candidate HEAD is product base `aa037d09995f7710bda5f8993ff9133f829e3df3`; architecture HEAD is `4d30d0a00473179625cf9403d208531cd0746666`. The lock remains at inventory v194 and 164 contract successors.

## B2B3C-R1-RF-1: Handle the operation end outcome instead of dropping its failures

Location: crates/security/src/scenario.rs:440, ScenarioHome::discover.

The seam unconditionally drops operation.end(JournalOutcome::Certain), then returns the discovery records. OperationEnd explicitly includes Failed(EndFailure) and RolledOver { end: Err(..), .. }; its contract says failures are disclosed by the caller. The existing commit_session end_step_failure/rollover projections demonstrate this distinction. Thus an end-path fence, owner, carrier or unlock refusal can disappear, and an ordinary successful-looking DiscoveryRecords value is still returned. This conflicts with the seam's stated non-discovery-refusals-as-Err behavior and fails to preserve the full planned operation/end composition.

Required correction: Match and handle OperationEnd, including failed end steps after rollover and any required rollover disclosure. Preserve the original discovery outcome as required by the end contract; report the separate end failure through Err or an explicit plain end-disclosure field rather than silently dropping it. NotEntered is not itself a failure. Add a focused control that an end failure remains observable and cannot be mistaken for clean completion, without adding a new shared fixture gate.

## Other implementation results

The admission and traversal order before the end projection follows amended plan r3: typed waiver construction; phase 1 with explicit path and UpwardRecord; caller resolution/pack admission over captured carriers; phase 2 with the waiver; tracking with empty environment/system-source inputs; conditional first registration; begin_operation; the existing discovery_root lending; and discover_downward on one fresh discovery ledger. Unit source is chosen from the resolved roots before traversal. End is invoked after the walk even when walking refuses, but its outcome is mishandled as described above; consequently seamOrderSound is false for the complete operation, not for the phase ordering.

Selection refusals use UpwardRecord::discovery_refusal, including its stage guard. Other admission failures return Err. Resolution refusal returns a plain explicit resolution-refusal record before phase 2, tracking, registration or downward observation. Walker NameUnrepresentable uses WalkRefusal::discovery_refusal; other walker failures return Err. Pure-core typed refusals remain discovery records. Apart from the discarded end outcome and the inventory observation below, the mappings preserve their respective stages.

The fixture chain reaches only existing X8 gates. No feature cfg site, fixture producer, shared-gate widening or third discovery-root constructor is added. The security scenario feature remains the enclosing gate. Using the owner uid of ScenarioHome's created scratch home is sound for this synthetic fixture: its creator owns the home, while native admission uses that account. This is not authority to accept an arbitrary production caller-supplied uid.

DiscoveryRequest and DiscoveryRecords contain paths, booleans, strings and collections only. The resolver callback supplies ordinary root strings; no receipt, admission, ledger, operation or retained descriptor is returned. Retained fixture producers are kept in ScenarioHome to outlive the operation. Returning cloneable records does not lend execution/custody authority.

## Flag controls and placement

The seven new host tests meet the amended COV method for their exact synthetic scope:

- Explicit project selection is tested from a different launch, with explicit mode/stop, expected units and no resolution for an absent explicit path.
- The typed waiver is recorded, other-write still refuses, and waiver-without-project construction refuses. Foreign-owner behavior remains with the accepted predecessor vectors as authorized by plan r3.
- Configuration keys attempting project/owner-waiver consent impersonation are rejected by the actual resolver before phase 2 or walking.
- CLI workspace roots win over project roots, with flag-layer and Flags-source provenance; absent CLI roots retain their source and refuse rather than falling through.
- Configuration-only roots and the automatic case with neither source are covered.
- Refused pack and empty flag roots stop at resolution, with phase_two/walked false.
- Records are cloneable values with V3 inventory, and a second discovery opens a new writer.

The resolver callback calls resolve_analysis_configuration, which performs resolution and immediate pack admission, and preserves the winning roots' provenance. The module is declared in lib.rs under cfg(all(test, target_os = "macos")); configuration.rs is unchanged. This avoids B1-a's pinned configuration test-include surface. The integration owner crates/host/tests/discovery_tests.rs remains planned for J1, as the accepted amendment requires. These rows do not claim public CLI composition or full production qualification.

## Verification and evidence

Independently ran only the expressly permitted checks:

- Source operability census: passed, 114 rows, no findings.
- Environment exceptions pin: 10 tests passed.
- FW-01 structural pin: 7 tests passed.

The submitted, hash-pinned lane-r2 evidence is internally consistent:

- Security has identical 14 named failures and 1117 passes at base/candidate. Host has identical 8 named failures, with passes 336 to 343, satisfying the seven-new-tests requirement. These are equal baseline failure sets, not wholly green suites.
- All five legacy admission spend/outcome lines match exactly.
- Locked/offline all-targets Clippy for opensip-host and opensip-security with -D warnings reports exit 0 with a matching completion log.
- All three edited/new Rust paths are rustfmt-clean; both inherited edited paths were base-clean.
- Scan, upward and walk vector checks, configuration tables, census and verify_design report success. The design evidence selects v194 and claims no qualification. Vector tools and verify_design were not independently rerun because this request permits only the three checks above.
- All five mutation logs have failing-test summaries containing the tests named by controls.json. Resolution continuation, ignored roots, missing waiver record, dropped selection refusal and omitted flag resolution are each caught.

No Cargo, rustc, Rust tests, builds, lane, Clippy or rustfmt was run during this review. Those results are inspected submitted evidence.

## Non-blocking observation

**B2B3C-R1-NBO-1:** The if-let-Ok boundary_inventory projection also suppresses Locator instrument faults. NotAccepted is expected for a refused discovery result; on an accepted result, require inventory conversion to succeed or return Err, rather than quietly producing inventory=None. Current valid walker outputs should not hit Locator, but keeping that invariant visible makes the seam a stronger control.

The diff adds only the feature-scoped seam/plain records, the host test module and its test-only declaration. No production caller, public composition, discovery export, environment read or law change is added. The inventory successor is still owed; the subject's claimed completion of B2-b3 is not accepted until this finding is corrected and the unit is accepted/bound. B2-b4 and its all-entry margin gate remain open.

Only REVIEW.md and review.json were written. Neither repository, worktree, stage nor controls were edited. No network, other panes, delegation, private fixture, installation directory, signing keys, held trees or T2 held-outs were accessed. No binding, integration, push, product qualification or entire-plan completion is claimed.
