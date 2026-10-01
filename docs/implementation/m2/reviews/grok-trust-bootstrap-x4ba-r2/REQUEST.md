Grok review: unit X4B-a r2, the first trust acceptance producer, after your r1 RF-1. This round also rebases onto product c2352ae and rebuilds inventory v113 on v117. Claude Opus 5.5 leads, and you are the single reviewer.

## Rules
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4ba-r2`.
- If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.
- Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, and python3.14 at `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.

## Background
Arch paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`.

Your r1 review is in `reviews/grok-trust-bootstrap-x4ba-r1/` (REVIEW.md and review.json), copied from `/tmp/opensip-implementation/reviews/grok-trust-bootstrap-x4ba-r1/`. It found:
- **RF-1:** the document quorums ignored the embedded revocation;
- judgment calls 1, 2, 4 to 11, 13 and 14: accepted;
- judgment call 12 (the multi-root reader gap): not a finding for this unit. X4T r9 item 3 is to be amended, and an X4T-a3 reader successor follows, before X4B-b. The lead tracks that separately, and the pinning test is unchanged.
- inventory v113: ACCEPT on v114.

**The law is unchanged:** X4B r5 (`trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e27028a50af5d1b49cccdd835a365c8066d6955052f263d87823fc62c`). X4B-a is item 11's producer: the records and the publication of items 2 to 6. This host is BASELINE-ATTESTED, and every test payload is a test-signed release (public quorum62 seeds) produced into an `InitialCore` through 463's injected-image test constructor.

## The rebase
X8a integrated after r1. Product main is now `c2352ae`, and the lock selects inventory117.

The worktree `/Users/sb/code/opensip-ai/opensip-x4ba` was moved from daa7b01 to c2352ae:
1. the intent-to-add entries were reset;
2. stash with untracked, detached checkout, stash pop;
3. the two new files were made intent-to-add again.

No product file X4B-a touches differs between the two commits (`git diff --stat daa7b01 c2352ae` on the eight paths is empty). Before the RF-1 edit, `git diff` was byte-identical to r1's (sha256 `04ce6fd0…fc77`).

## RF-1 fix (code)
Only `trust_bootstrap.rs` and `trust_bootstrap_tests.rs` change against r1. The other six files are byte-identical to r1 (see `hashes.txt`).

**`trust_bootstrap.rs`:**
- `verify` takes the embedded list's keyId set and passes it to `filter_envelope_revoked`. This applies to every document it checks: the revocation list, the bootstrap manifest (TR-BUNDLE), the core inventory (TR-CORE), the catalog (TR-INDEX) and each component manifest (TR-COMPONENT).
- A quorum that is not met after the exclusion refuses `PAYLOAD-NOT-ADMISSIBLE`, with that document's subject, before any write.
- `Document.signers` still holds every valid signature from before the exclusion. Item 4's Revoke reads those, so Revoke happens only for a document whose quorum survives.

**Revised judgment call 3:** each document is verified against the final root with the list's keyIds excluded (X4B r5 item 2; law 463 item 5 step 3), at its role's threshold. Any failure refuses before any write. The producer therefore always reaches `PresentOrdinary { Admissible }`. `Inactive` and `Rejected` are reachable only through `bootstrap_sequence`, and they record nothing (tested there). Calls 1, 2 and 4 to 14 are unchanged.

**`trust_bootstrap_tests.rs`** now has 17 tests, up from 16:
- **New:** `a_revoked_counted_signer_below_the_threshold_refuses_and_writes_nothing`, covering two cases:
  - The list revokes key 11, one of the catalog's two TR-INDEX signers (`INDEX_SIGNER` is 11 and 12; threshold 2). The result is `PAYLOAD-NOT-ADMISSIBLE` (`catalog`), with the trust tree and `state.v1` unchanged and no confirmed publication.
  - The same with key 14, one of the component manifest's two TR-COMPONENT signers (`COMPONENT_SIGNER` is 14 and 15). The result is `PAYLOAD-NOT-ADMISSIBLE` (`component`).
- **Retargeted:** `a_revoked_document_whose_quorum_survives_is_present_then_revoke_with_revoked_by`, which replaces r1's two-signer case. The catalog is signed by all three TR-INDEX keys (11, 12 and 13), and the list revokes 11. The quorum (two of three) survives, so the catalog is admissible. Its pre-filter signers include 11, so it gets Present then Revoke, `ST-REVOKED`, `revokedBy` naming the `EV-REVOKE`, and the confirming admission refuses `index:revoked`.
- **Changed:** `expired_and_revoked_is_three_events_ending_revoked` uses the same three-signer catalog.
- The bundle and core cases are not new tests: `InitialCore` (463 item 5) already refuses a release whose TR-CORE or TR-BUNDLE quorum fails after exclusion, so no payload reaching `from_initial_core` can exercise them. The exclusion still runs on them in `verify`.

## Subject
**Worktree:** `/Users/sb/code/opensip-ai/opensip-x4ba`, detached at `c2352ae`. Nothing is committed.
- 8 files: 2347 insertions and 47 deletions.
- `git diff`: 104003 bytes, sha256 `4b0df6b75997253aee62bb5d21ecaada3218e7d7f4ac83ddfff4cb3a38372fff`.
- `trust_bootstrap.rs`: 43086 bytes, sha256 `4aaf78e2…9664`.
- `trust_bootstrap_tests.rs`: 36930 bytes, sha256 `229b1589…d7da`.

## Inventory v113 (rebuilt on v117)
Built on the inventory the lock selects at c2352ae: `repository-file-inventory.v117.json`, 414580 bytes, sha256 `0601e3fa93ad00a09197dc199aafe74b8102f7d90c62916881ff90d0bd6f3138` (unit X8a).
- `repository-file-inventory.v113.json`: 418175 bytes, sha256 `cca9d397b042941eee7ac672552e0ed80b0164a3dbb6f5c768518efe41c78f98`. It has 837 files: all 835 v117 rows by value, plus the same two rows.
- `trust-bootstrap-x4ba-inventory-v113/successor.json`: 20193 bytes, sha256 `a8cd24517614615dba2e3b308c2c2f5da8637025f8728bda835dcb8bff0f3c50`. The sixteen overrides are re-projected by path from v117's record.

**Changes in the builder:**
- `evidence/build_v113.py` adds v117's committed successor record to PRIOR, beside v114. It updates the docstring.
- Three phrases in the two row descriptions now state the RF-1 behaviour:
  - the service row says "with the list's keyIds excluded" and names `successor_record_bindings`, which r1's code already ran;
  - the test row covers a revoked signer whose quorum survives;
  - the test row adds "a revoked counted signer that leaves a catalog or component manifest below threshold writes nothing".
- Reruns give identical bytes.

**Other refreshed files:** README "Order" and "Projection", the `verify_projection.py` comment (v117), the `verify_scratch.py` docstring, `verifier-anchor.json` (c2352ae), and `verification.*`.

**Checks:**
- `verify_projection.py` against the real lock: PASS, 16 rows, 83 corruptions refused.
- `evidence/verify_scratch.py` on the worktree: passed, with 79 inventory successors, 72 contract successors, 16 inheritance rows, and v113 selected.
- `check_package_edges --lane host` against v113: passed, 19 declared and 19 resolved.

The files are untracked. X4a's v116 is still in flight.

**Subject manifest:** `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113-subject.json`, 2144 bytes, sha256 `d47b9695001e63b2f91209fb9c147eb2612937a58319e3357400995908ab476c`.

## Lead's runs (on these exact bytes)
- `cargo test --locked --offline -p opensip-security --lib trust_bootstrap`: 17 passed.
- `cargo test --locked --offline --workspace`, run twice: 1511 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: clean.
- `cargo fmt --all --check`: clean, and the two include files were run through `rustfmt --edition 2024`.

## Decide
1. Is RF-1 closed?
2. Is the rebase clean?
3. Is the v117 rebuild correct?
4. Is anything new wrong?

## review.json
review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `d47b9695001e63b2f91209fb9c147eb2612937a58319e3357400995908ab476c`;
- "inventoryCandidateAssessment": an object with:
  - verdict and requiredFindings;
  - path `docs/implementation/m2/repository-file-inventory.v113.json`, bytes 418175, sha256 `cca9d397b042941eee7ac672552e0ed80b0164a3dbb6f5c768518efe41c78f98`;
  - parent: the v117 pin above;
  - successorRecord: path `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113/successor.json`, bytes 20193, sha256 `a8cd24517614615dba2e3b308c2c2f5da8637025f8728bda835dcb8bff0f3c50`.

Write REVIEW.md and review.json. Do not commit.
