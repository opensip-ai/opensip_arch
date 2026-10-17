# C1A3-r1 review

Verdict: **REQUIRED-FINDINGS** — two required findings and one non-blocking observation.

## Exact subject

Verified the 18,479-byte manifest SHA-256 `00a182bdf220ee8940488278eb548f69a23ba1cd75876644d99a3cf5a25d7121` and all 79 members, then rehashed them before writing. All ten product-map candidates match the detached worktree and architecture archive; all eight parent pins match `e937dac74c8e529fee3efb6f84439d05280e48ea`. The worktree is at that base with eight edited and two new files.

Read the C1a sealing plan and M3-C carrier/VCS/bounds/order rules, the implementation, tests, tracking proof and identity encoder/admission interfaces. Related r9 law work is outside this code acceptance.

## Required findings

### C1A3-R1-RF-1 — Charge or eliminate the encoder's digest-hex temporary allocations

Location: `crates/host/src/snapshot_seal.rs:207`.

push_row calls digest_hex for every inventory row. The imported helper is crates/identity/src/digests.rs::hex, which allocates String::with_capacity(64). Charging owned_record(inventory_len) pays for the inventory Vec, not these additional temporary strings; WorkLedger explicitly requires temporary copies to be charged separately. none_observation allocates another digest-hex string, and seal allocates the VCS digest string at line 356 in addition to the charged 160-byte VCS buffer. These are sealing-owned allocations outside the separately bounded IdentityCandidate admission, so LD-C1A3-4's every-allocation-before-it-happens claim is not met.

Required change: Write hex directly into the precharged destination, or use fixed stack arrays, to remove the temporary heap strings; alternatively charge every distinct temporary before allocation, including per-row and both VCS-path conversions. Add a focused accounting/allocation control that catches reintroducing an uncharged conversion. Update the sealing-charge evidence and any dependent r9 derivation if the charged terms change.

### C1A3-R1-RF-2 — Complete the mixed-error precedence controls required by C1A-T6

Location: `crates/host/src/snapshot_seal_tests.rs:491`.

The accepted C1a r6 C1A-T6 requires an over-8-GiB inventory followed separately by a read I/O failure, a ChangedDuringRead failure, and a custody or open failure, each preceding the totalBytes refusal. walk_refusals_come_before_the_bounds injects only the later read I/O error. The zero-read synthetic step-5 bound tests and source pin showing no total bound in the walker are useful, but neither exercises the later changed-file or custody/open branches on an already over-bound inventory. SCOPE's structural explanation is also stronger than the API: SnapshotWalkReport is public, Default and Clone and is supplied separately from the session/root, so its type alone does not prove that it is this session's successful walk.

Required change: Keep the efficient split rather than writing 8 GiB: preload the synthetic reached over-bound capture, then add one later metadata-change case and one later custody/open-failure case through the actual session walk/sealing composition, asserting the original refusal and no sealing output. Retain the no-total source pin and exact step-5 bound controls. Describe successful-walk provenance as an explicit composition precondition unless the API enforces it; do not count the report's type as a structural proof.

## Implementation assessment

The successful path follows item 6's intended order: caller-completed walk; the currently empty read set; ordered unique reached inventory and counts; leftover and carrier joins; the interim VCS gate; rows, full canonical descriptor length and total-byte bounds; then identity-v3 snapshot admission. Placing leftovers and the carrier join with the inventory checks is coherent. Treating every pre-walk capture as depended on by a resolved input is the stated preparatory contract; C1c must revisit that relationship when read-set captures are composed.

The carrier table is implemented consistently. Present/regular compares the retained row digest; disappearance, type replacement and exclusion have distinct transitions; absent admits only with an absent root listing entry and otherwise refuses absent-present. The walk classifies the root carrier from its observed kind and the combined exclusion predicate, before kind-dependent work. The predicate preserves the prior short-circuit order: shared rule, ignorePaths, then kind-independent boundary exclusion. No charge is introduced by the report field.

SnapshotRoot's durable tracking flag comes from the operation's own NoRepository proof. member_precondition checks both tracking and the never-reused retained-chain identity; it is not a caller assertion. The ephemeral route remains Unobserved and refuses VcsPending, which is the correct conservative interim. The member gate rejects even a NoRepository root when admitted D15 members are supplied; Git and member observation remain C1b's. No false kind:none is minted for those inputs.

The hand encoder matches the identity canonical rules for string escaping, decimal integers, member ordering and raw UTF-8. Inventory rows have exactly path/sha256/bytes. The inventory SHA-256 is distinct from the snapshot identity hash and is retained as a custody blob; the none VCS record is canonical and its raw digest enters the six-member descriptor. The descriptor is finally admitted through IdentityCandidate. The 160-byte VCS allocation is charged as its requested capacity; its encoded value is 154 bytes. The missing charges in RF-1 are additional heap strings, not a complaint about that capacity.

The pre-build descriptor calculation includes the whole envelope, separators, escaped path lengths and integer widths. Bounds have the specified order and strict greater-than comparisons. Tests cover exactly 4 MiB versus one byte over, inventory fitting while the descriptor does not, exactly 8 GiB versus one over, and the row limit (100,000 rows pass that check but fail the earlier-in-practice descriptor capacity). Synthetic reached captures are appropriate for isolated step-5 controls and make no filesystem custody or large-payload claim. RF-2 concerns the remaining explicitly required mixed-error cases.

The new custody_mut access is crate-private and used for the inventory blob; test helpers remain cfg(test). No production caller, snapshot profile or cap is introduced. The two new paths have no existing planned inventory row and need two additions after acceptance.

## Model, rules and verification

The KIND_FREE_BOUNDARY anchor is reattached to the combined predicate without changing its semantic order. Independently compared both regenerated vector documents with base: every field other than pins is unchanged, including every predicted charge. Both permitted live commands passed:

- `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`
- `python3 -I -B tools/check_operability.py source --repository .` — 114 rows, no findings.

Reviewed the pinned attempt-2 lane and its logs rather than running Cargo or a lane. Host has the same eight failures at base/candidate and nine new passing tests; security has the same fourteen failures and no new tests. These are equal-failure-set results, not whole-suite passes. Focused sealing tests pass 9/9; session/custody pass 19 with one ignored; source/walk pass 17. Warning-denied all-targets Clippy and the rustfmt classifications pass. The model, archived lead-readable census check, FW-01, environment exceptions, operability, closure and verify_design checks pass. The census result was inspected only; no T2 input was read.

All eleven mutations cause the expected test failures, with no compiler-error substitute. They do not test the uncharged hex allocations or the two missing mixed-error branches. Attempt 1 correctly records the failed mint-audit check; the production usize::from calls were replaced, while audited exceptions stayed unchanged. The current source check confirms no added mint-census call. No new production environment read or ignored let binding was identified. Independently checked the ten changed paths against the 19-file census closure: no intersection.

## Non-blocking observation

**C1A3-R1-NBO-1 — Bind successful-walk provenance when the production composition is added** (`crates/host/src/snapshot_seal.rs:255`). seal accepts independent references to a mutable CaptureSession, a SnapshotRoot and a freely constructible SnapshotWalkReport. The current tests correctly obtain a report from that session, but the signature does not prevent a default report, a report from another root/session or stale reuse. When J2 composes the production path, retain an opaque session-bound completion token or a single helper that walks and then seals, and consider consuming/freezing the session against later source reads. This is a future composition obligation, not an assertion that a production caller currently exists.

## Scope and boundaries

C1a3 remains preparatory library work. C1a4/r9, C1b, C1c and J2b/J2c composition retain their own gates. No complete C1a, Plan/Run production path or qualification is accepted here.

Only the two permitted Python checks were run. No Cargo, rustc, build or lane was run, and no network, other pane or delegation was used. No private 413 fixture, installation, signing key, held tree, T2 store or T2 cache was accessed. Neither repository, worktree nor control files were edited. Only the requested REVIEW.md and review.json were written.
