Grok review: unit X4B-a r1, the first trust acceptance producer. Claude Opus 5.5 leads, and you are the single reviewer.

## Rules
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4ba-r1`.
- If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, and python3.14 at `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.

## The law
Arch paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`.

**X4B r5** (`trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e…c62c`) is accepted. It is the reviewed r5 (`PROPOSAL-r5.md`, `97c2eef3…29a3`) plus the acceptance note. X4B-a is item 11's producer: the records and the publication of items 2 to 6. Two other units are not in this review:
- X4B-b, the wiring at X4T's fenced first read: the monitor, the F-absent branch and the one confirming admission;
- X4B-c, moving X4T-0 onto this producer.

**Related laws:**
- X4T r9 (`trust-admission-x4t/PROPOSAL.md`, accepted): items 1, 2, 7, 8 and 11. Item 7's publication protocol has one owner, `floor_publication::publish`, and this unit reuses it.
- Law 463 r9 and its code successor 463h (product 19e3e5b). See `reviews/grok-initial-core-463h-r1/` and its judgment call 7.

This host is BASELINE-ATTESTED, and a dev build embeds no release. Every test payload is a test-signed release, built with the public quorum62 seeds and produced into an `InitialCore` through 463's injected-image test constructor.

## Subject
**Worktree.** `/Users/sb/code/opensip-ai/opensip-x4ba`, detached at product main `daa7b01`. Nothing is committed, and the two new files are intent-to-add.
- `git diff`: 101814 bytes, sha256 `04ce6fd0a6aaa83c8d66caf58d35eff162e9a4a4b390fa46bee429e1215efc77`.
- 8 files changed: 2294 insertions and 47 deletions.
- `hashes.txt` pins every file.

**New files:**
- `crates/security/src/trust/trust_bootstrap.rs`: the producer. It is a macOS child of `current_trust_admission.rs`, beside `floor_publication.rs`.
- `crates/security/src/trust/trust_bootstrap_tests.rs`: its tests.

**Changed files:**
- **`trust/initial_core.rs`:**
  - `BootstrapDocuments` also retains the revocation pair's stored bytes. Item 5 verified them, but until now only the parsed evidence was kept.
  - `bootstrap_release()` lends the anchor's root binding, the bootstrap manifest and core inventory pairs, and the root chain's pairs.
  - Nothing new is opened, judged or granted.
- **`trust/core_authentication.rs`** (the test builder only):
  - Component manifests are signed before the catalog, and the catalog lists one release row per signed component. 463h call 7 left `releases: []`, and the retained reader's catalog join refuses that as `MissingRelease`.
  - Three `Spec` knobs: `catalog_expires`, `revocation_issued` and `root_expires`.
- **`trust/floor_publication.rs`:**
  - `may_create` also admits the `trust/objects` collection directory (call 9).
  - `TrustWrite` gains accessors, plus a `cfg(test)` path accessor.
- **`trust/current_trust_admission.rs`:** declares the child module.
- **`trust/role_machine.rs`:** `bootstrap_sequence` dispatches item 4's sequence through the private `decide`.
- **`trust_time.rs`:** `evaluate_fresh_install` runs S4 step 2 through the unchanged `assess_kernel`, on a record with no floor, no L and no anchor. The `TimeAdmission` projection is moved, unchanged, into `admission_of` and shared.

## What the producer does
**`BootstrapPayload::from_initial_core`** copies exactly the pairs `InitialCore` retains, charging every byte:
- the embedded binding;
- the manifest and inventory;
- the root chain;
- the revocation, catalog and component manifests.

**`build_acceptance`** runs against the retained P0 owner. It refuses unless the owner is P0, then:
1. **Item 2, authentication:**
   - The chain's index-0 root must match the embedded binding.
   - The chain is authenticated within `ChainBudget{16, 16 MiB}`.
   - The list is verified under the final root. Its keyIds re-filter the index-0 root, every link's continuity and possession quorums, and the list's own quorum (463 item 5's order).
   - The manifest (TR-BUNDLE), inventory (TR-CORE), catalog (TR-INDEX) and each component manifest (TR-COMPONENT) are verified against the final root at their thresholds.
   - A missing catalog, or any failure, is `PAYLOAD-NOT-ADMISSIBLE` with its subject. Chain errors take X4T's `chain_row`.
2. **Item 3, time:** S4 step 2 runs on the caller's observation. A future payload is `PAYLOAD-NOT-ADMISSIBLE` (`time`); beyond the horizon is `CLOCK-EXCURSION-FORWARD` (`beyond-horizon`). Otherwise tEval = F = max(W, A), L = A, and the anchor is the observation.
3. **Item 4, roles:** each carried role runs through `bootstrap_sequence` (calls 4 and 5). With no component manifest, TR-COMPONENT dispatches nothing.
4. **Item 5, records:**
   - objects;
   - the `PayloadMetadataClosureV1`;
   - the `bootstrap` operation;
   - `TimeEvidenceV1`, whose `SignedTimeSourceV1` is `{ordinary, closure}`;
   - the P0 image record;
   - `RootAdmissionNodeV1` (ordinary, for the final root);
   - the catalog and revocation `MetadataAdmissionNodeV1`s;
   - `RevocationHistoryNodeV1` (list);
   - the clock-write event and the role events, each with its `RoleChangeV1` and `PublicationEventV1` row, chained in dispatch order;
   - the revision-2 descriptor, in P0's by-predecessor bucket;
   - the retained capsule.

   Each record is canonically encoded and admitted by its closed shape. Then `current_record_bindings::bind`, `successor_record_bindings::bind` (against P0) and `publication_events::bind_events` (from P0's roles and head) run over exactly those bytes before anything is written.

**`accept_bootstrap`** rechecks the fence and the owner, builds, then calls `publish`. `publish` writes the dependencies, then `state.v1` last, and advances the owner from the confirming reread. The producer does not call it from any read path.

## Judgment calls
1. **The revocation bytes.** X4B r5 item 2 takes "the pairs InitialCore retains". `InitialCore` kept the verified list's evidence but not its stored bytes, which acceptance must write and verify again. So `BootstrapDocuments` now also retains the revocation pair. 463 r9 item 2's store already held the pair; this is retention only. `bootstrap_release` lends the other documents from the authenticated release. No trust decision is added to `InitialCore`.
2. **Authentication order.** The order follows `core_authentication::authenticate_embedded_release`. The anchor is the chain's index-0 body, checked against the anchor record's binding, which is the embedded binding `InitialCore` was built from. The links are authenticated with an empty initial set; the list's keyIds then re-filter.
3. **Every document must verify.** Each document is verified unfiltered at its role's threshold. Any failure refuses before any write. Item 2 r5 makes that rule explicit for the catalog and component manifests, and the authentication row (item 7) covers the bundle and core. The producer therefore always reaches `PresentOrdinary { Admissible }`. `Inactive` and `Rejected` are reachable only through `bootstrap_sequence`, and they record nothing (tested there).
4. **What revokes a role (item 4's Revoke).** A list entry revokes a role when it names any of these:
   - a keyId among the valid signers of that role's documents, before filtering;
   - a namespace one of those documents is signed for;
   - the running core's `release` (TR-CORE only);
   - the catalog's `catalogSnapshot` (TR-INDEX only).

   These are X4T item 4's closure components, assigned to roles. `newer_and_byte_valid` is true, because nothing was accepted before.
5. **What expires a role (item 4's Clock).** This uses the S4 kernel's states at tEval:
   - an expired final root expires every carried role;
   - an expired catalog expires TR-INDEX;
   - a stale list (issue time + 90 d < tEval) makes every carried role stale.

   No other document carries an expiry that acceptance reads. When both expired and stale hold, `decide` stores `Expired`.
6. **Time inputs.** A uses the retained reader's own set (`project_times`):
   - the newest issue time of the manifest, catalog and list;
   - the final root's issue time.

   The inventory and component manifests are not inputs. So the confirming admission computes the same A, and its write-ahead finds nothing to write (tested).
7. **Record forms follow X4T-0's.**
   - The time evidence is `S4EvaluationInputV1`. V2 needs `authority`, the root admission, whose context cites the time evidence, which would be a cycle.
   - The clock-write event goes `unevaluated` → `evaluated`, as the schema forces from `unevaluated`, while the capsule is `retained`.
   - Role events cite the clock write as their clock input.
   - Accepted standings carry the final root binding, the root admission, the role's root namespaces, `catalog` for TR-INDEX only, and `by` set to the role's `EV-PRESENT-PAYLOAD`.
8. **What is written.**
   - Objects: the chain bodies and envelopes, the list, catalog, manifest and component pairs.
   - The core inventory pair is verified but not written: no record references it.
   - Closure members are the manifest's `envelopes` and `manifests` slots, sorted by (slot, path).
   - A manifest listing artifacts, permission policies or repair material with a path refuses `PAYLOAD-NOT-ADMISSIBLE`, because `InitialCore` retains no such bytes.
9. **`trust/objects`.**
   - P0's closed tree (law 467; see `initial_manifest`'s test) has no objects collection, so the first acceptance must create it.
   - `may_create` now admits that one directory, through the same private create and both barriers it uses for `by-predecessor`.
   - This is the only change to the shared protocol, and it is reserved in `file_cost` as before.
10. **The builder** gains catalog release rows and three time knobs, as 463h call 7 anticipated. 463h's own tests are unchanged and pass.
11. **A non-P0 predecessor** is the host I/O row (`acceptance-predecessor`). X4B-b calls the producer only on F absent, so this is a caller invariant.
12. **Stated gap: multi-root chains.**
    - X4T-a's reader (`current_trust_admission::authenticate`, then `verify_captured_core`) passes the head root as both the accepted and the signing root. So the confirming admission admits only a closure whose `rootChain` is the head alone.
    - X4B-a records the chain exactly as the manifest lists it, because the inventory's `RootCount` join requires that. Its `heads.root` is the final root.
    - The default test release rotates root 1 to root 2. Its acceptance completes, and the confirming admission then refuses `FirstIdentity` (incomplete row). The test pins this.
    - **Recommendation:** an X4T-a reader successor before X4B-b. When the closure chain is longer than one root, it should take the chain's first root as the accepted root and the head as the signing root. All other tests use a single-root release.
13. **Not tested in this unit:**
    - The uncertain pointer replacement belongs to `publish`, and X4T-b's tests cover it.
    - `CORE.NO_EMBEDDED_RELEASE` is upstream. A dev build has no `InitialCore`, and `from_initial_core` is the only production constructor (`from_parts` is crate-visible for the binding test).
    - The ordering, monitor, lease, read-only and second-F-absent cases belong to X4B-b.
14. **Budget (item 8).**
    - The payload copies and every built record are charged on the caller's ledger.
    - The binders load through `Budget::borrowed`.
    - `publish` reserves the writes and the confirmation before the first effect. A short ledger is the budget row, and P0 remains current.

## Tests (law item 10, X4B-a's part)
16 tests in `trust_bootstrap_tests.rs`:
- P0 is accepted. BUNDLE, COMPONENT, CORE and INDEX are each `ST-TRUSTED` from one `EV-PRESENT-PAYLOAD`; PROFILE and REPAIR stay blank. The one confirming admission (`fenced_first_read`, same sample) admits with `InstallGateRequiredForNewProcess` and writes nothing.
- X4T-a's native reread (`admit_native`) admits the written store, and every record is canonical and content-addressed.
- Time: tEval = A when W < A; a future payload and beyond-horizon write nothing; exactly A + 90 d is admitted.
- An expired catalog gives Present then Clock, `ST-EXPIRED`, `accepted.by` naming the Present event, and `ExistingOnly`.
- An expired root expires all four roles, and the confirming admission refuses `core:expired`.
- A stale list gives `core:stale-revocation`.
- A revoked signer gives Present then Revoke, with `revokedBy` set, and `index:revoked`.
- Expired and revoked gives three events, ending `ST-REVOKED`.
- Inactive or rejected entries record no event.
- No catalog, or a catalog or component manifest signed outside its role, refuses `PAYLOAD-NOT-ADMISSIBLE` and writes nothing.
- No component manifest leaves `component:unbootstrapped`.
- A crash before the pointer is followed by a rerun that admits the equal records; a rerun at another instant uses fresh names.
- A changed `state.v1` is `required-files-changed`, with nothing written.
- A short ledger is the budget row, with P0 unchanged.
- A non-P0 predecessor, a foreign root binding and a tampered manifest envelope all refuse.
- The two-root chain is recorded in full, with the reader gap pinned (call 12).

**Lead's runs:**
- `cargo test --locked --offline -p opensip-security --lib trust_bootstrap`: 16 passed.
- `cargo test --locked --offline --workspace`, run twice on these exact bytes: 1506 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: clean.
- `cargo fmt --all --check`: clean. The two new include files were also run through `rustfmt --edition 2024`.

## Inventory v113
Built on the inventory the lock selects at daa7b01: `repository-file-inventory.v114.json`, 393913 bytes, sha256 `5a6f2b74f549e2e7b8bce26e6df9f3e9b00c01039728f47e68521fc5002fceb4` (unit X9-0).
- `repository-file-inventory.v113.json`: 397366 bytes, sha256 `057e2944772a64e079754218e7a53cc0204fc2035e88619893326aee77ed5c32`. It has 806 files: all 804 v114 rows by value, plus the two new rows.
- `trust-bootstrap-x4ba-inventory-v113/successor.json`: 20193 bytes, sha256 `1995ec4077f2191b4180f66e5f76b4f149b49746ce239990a3678eadf9b25fed`. It carries the sixteen description overrides re-projected by path.
- `evidence/build_v113.py` is v114's builder method. It is rerunnable, gives identical bytes on rerun, refuses tracked paths, and refuses while a lock selects v113. Its README lists each existing row this diff touches and whether its description stays true; the D1 items are `initial_core.rs` and `current_trust_admission.rs`.
- `verify_projection.py` against the real lock: 16 rows, PASS, 83 corruptions refused.
- `evidence/verify_scratch.py` on the worktree: passed, with 78 inventory successors, 72 contract successors, 16 inheritance rows, and v113 selected.
- `check_package_edges --lane host` against v113: passed, 19 declared and 19 resolved.
- All of these files are untracked. X4a (v116) and X8a (v117) are in flight; whichever integrates first, the others rebuild their parent.

**Subject manifest:** `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113-subject.json`, 2144 bytes, sha256 `b0beabe0a68b66f3b818492604f975a76d6340c8b1e0ab8bcafe073d836ccade`.

## Decide
1. Does the producer implement X4B r5 items 2 to 6 exactly, within X4T r9 items 7 and 8's shared protocol?
2. Are judgment calls 1 to 14 the narrowest reading? Call 12 needs particular attention: is the multi-root reader gap correctly owned by an X4T-a successor rather than by this unit?
3. Is anything else wrong?

## review.json
review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `b0beabe0a68b66f3b818492604f975a76d6340c8b1e0ab8bcafe073d836ccade`;
- "inventoryCandidateAssessment": an object with:
  - verdict and requiredFindings;
  - path `docs/implementation/m2/repository-file-inventory.v113.json`, bytes 397366, sha256 `057e2944772a64e079754218e7a53cc0204fc2035e88619893326aee77ed5c32`;
  - parent: the v114 pin above;
  - successorRecord: path `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113/successor.json`, bytes 20193, sha256 `1995ec4077f2191b4180f66e5f76b4f149b49746ce239990a3678eadf9b25fed`.

Write REVIEW.md and review.json. Do not commit.
