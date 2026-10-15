# B1B-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS**

The 449-byte subject manifest matches SHA-256 `c1968f0933ef6116b060df6a3537d5a73ca830f9b77b8652ec4e74df9914781f`. Its sole member is 10,949 bytes and matches SHA-256 `441547162b42493d89b2adfb5f3138891b842062abdde487db8f2c07ca971f7e`. Product and architecture HEADs match the requested bases; tracked checkouts are clean, and the product has no untracked changes.

The proposed deliverables match MB:876: project/local carriers, installation-private global settings, invocation mode and the environment structural check, with FW-01, SL:3 and --project coverage. Descriptor retention, bounded charged reads, CI non-probing, the intended placement/chain-before-carrier order and deferred J1 wiring are appropriate. Acceptance is blocked by the following plan defects.

## B1B-PLAN-R1-RF-01: Specify independent carrier absence observations and rechecks

Severity: high. Location: PLAN-r1.md:64-69; section 0 recheck-set facts; section 2 carrier controls.

The plan relies on selection already recording opensip.json absence and the marker observation covering absent .opensip. At the pinned base Selected.config is only a boolean and ProjectRootAdmission::recheck never checks the config name. observe_marker returns the same MarkerObservation::Absent for a missing .opensip and for a present .opensip without project-id.v1. Thus opensip.json can appear after selection, or an initially absent .opensip can appear containing local.json but no marker, without either inherited recheck detecting it. The chain checks identity/birth and custody, not unchanged directory mtime. Section 0 also incorrectly describes every inherited field as a full DescriptorMetadata equality check.

Required correction: Specify explicit charged negative observations for opensip.json and, in interactive mode, local.json or its absent .opensip parent, retained against the appropriate parent and rechecked under the fence. Keep CI free of local-carrier lookups. Correct the inherited-recheck facts. Add controls for opensip.json appearing after absence and .opensip appearing with local.json but no project-id.v1, in addition to the existing absent-leaf control.

Evidence at the requested bases:

- crates/security/src/custody/project_admission.rs:78-96, 806-825
- crates/security/src/custody/project_admission.rs:561-600
- crates/security/src/custody/project_chain.rs:59-67
- X2 r9 item 3a; MB items 2 and 3

## B1B-PLAN-R1-RF-02: Resolve the exception-list conflict with the accepted law

Severity: high. Location: PLAN-r1.md:114-122; section 2 environment controls.

MB item 9 says the audited list holds exactly git_tracking::process_environment and the test-only crash-matrix seams. LD-B1B-3 explicitly adds other fixture reads on the ground that they are equally test-only, while section 4 claims no law change. That expands an exact exception set without a corresponding accepted authority. Moreover the plan says it lists each exception but supplies only a category, not the concrete items the promised pin test would audit. Existing reads include custody HOME fixtures, host admission RUSTC/CARGO/helper reads, journal child helpers and fence/root test helpers. The section 2 controls also omit MB item 9's hostile-environment byte-equivalence control.

Required correction: Either remove/inject the non-authorized fixture environment dependencies so the accepted list is obeyed, or explicitly obtain the required law correction before implementing expanded exceptions. Enumerate every allowed item and reason, with cfg(test)/test-target confinement, rather than a broad fixture category; pin that concrete list. Include the required hostile HOME/PATH/CI/XDG_* invariance control, preserving the refusal-only Git outcome exception.

Evidence at the requested bases:

- docs/implementation/m3/config-discovery-b/PROPOSAL.md:295-312
- crates/security/src/custody/read_premise_tests.rs:104
- crates/security/src/journal_store.rs:1277
- crates/host/tests/admission_tests.rs:1257, 1283, 2341, 2482

## B1B-PLAN-R1-RF-03: Make preservation of legacy admission behavior explicit

Severity: medium. Location: PLAN-r1.md:82-86; section 2 order controls.

The compatibility wrapper is specified as exactly the composition of a phase that captures carriers and a registry phase. Existing read-session and write-gate admissions do not read configuration bytes, accept no invocation-mode argument and charge no carrier reads. Composing the new phases therefore adds I/O, budget consumption and new race/read failures to existing callers; choosing non-interactive alone still reads opensip.json. Interactive use could also introduce local.json refusals. The asserted unchanged behavior does not follow from the proposed API, and no compatibility control is provided.

Required correction: Define an explicit non-capturing legacy path or policy that preserves the old callers' reads, charges, refusals and mode behavior, while requiring the analysis path to capture carriers before configuration/pack resolution and registry capture. Identify how read-session and write-gate wrappers use that path, retaining their rechecks and latching behavior. Add focused compatibility controls demonstrating no added carrier reads or local probing, and retain the refused-pack pre-registry control for the analysis path.

Evidence at the requested bases:

- crates/security/src/custody/project_admission.rs:859-888
- crates/security/src/custody/installation_read.rs:171-224
- crates/security/src/custody/first_registration.rs:2098-2137
- crates/security/src/custody/ordinary_writer.rs:95-109

## Remaining assessments and scope

LD-B1B-2 is sound at plan level: optional global capture uses installation-private custody, positively records absence in the session recheck set, latches custody failures and never creates settings or its parent. Implementing an absent-prefix outcome must retain the positive absence under its judged existing parent, as the plan's general absence-recheck rule requires. The global allowlist remains B1-a's.

Invocation-mode unification is sound at plan level: remove the duplicate type, compute the conjunction of stdin/stderr terminal observations without environment input and leave production wiring to J1. The proposed per-crate Clippy scope and planted host production read are appropriate; RF-02 concerns the authorized exceptions and missing behavioral control, rather than extending the check into platform.

The refused project-pack control correctly requires configuration and pack resolution before registry capture, RESERVED rows, leases or journals. FW-01's before/after no-write checks are appropriate. Carrier absence and compatibility controls require the additions above. No code, binding, law amendment or product qualification is accepted by this plan review.

Review was limited to read-only source/authority inspection, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane or network was run. Neither repository nor the stage or control files was edited. Only this review directory's REVIEW.md and review.json were written.
