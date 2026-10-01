Grok review: unit X4B-a r2, the first trust acceptance producer, after your r1 RF-1. This round also rebases onto product a34dc6b and rebuilds inventory v113 on v116. Claude Opus 5.5 leads, and you are the single reviewer.

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
X8a and then X4a integrated after r1. Product main is now `a34dc6b`, and the lock selects inventory116 (unit X4a).

The worktree `/Users/sb/code/opensip-ai/opensip-x4ba` was moved in two steps:
1. **daa7b01 → c2352ae (X8a):**
   - reset the intent-to-add entries, stash with untracked, detached checkout, stash pop;
   - no conflict: none of the eight X4B-a paths differ between the two commits;
   - before the RF-1 edit, `git diff` was byte-identical to r1's (sha256 `04ce6fd0…fc77`).
2. **c2352ae → a34dc6b (X4a), after the RF-1 edit,** by the same procedure:
   - X4a touches two X4B-a paths: `current_trust_admission.rs` (+50 lines) and `floor_publication.rs` (one header comment);
   - `floor_publication.rs` auto-merged, because X4a's comment and X4B-a's `may_create` and `TrustWrite` hunks are disjoint;
   - the two new files were made intent-to-add again.

**One conflict, in `current_trust_admission.rs`.** X4a declares its `live_observation` child module and re-exports, and X4B-a declares its `trust_bootstrap` child module, at the same point: after the `floor_publication` re-exports and before `mod tests`.
- **Resolution:** keep both, X4a's block first, then X4B-a's block unchanged, separated by a blank line.
- Neither module refers to the other.
- X4a's other hunks in this file (the `ViewClosure` and `AdmittedRevocation` fields on the view) do not overlap X4B-a, which only declares the module here.

**Check:** the `+` and `-` lines of `git diff` at a34dc6b are identical, line for line, to those of the diff at c2352ae. Only context and index lines moved, so the RF-1 hunks reviewed below are what is on a34dc6b.

## RF-1 fix (code)
Only `trust_bootstrap.rs` and `trust_bootstrap_tests.rs` change against r1. Of the other six files, four are byte-identical to r1. `current_trust_admission.rs` and `floor_publication.rs` differ from r1 only by X4a's hunks, carried by the rebase (see `hashes.txt`).

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
**Worktree:** `/Users/sb/code/opensip-ai/opensip-x4ba`, detached at `a34dc6b`. Nothing is committed.
- 8 files: 2347 insertions and 47 deletions.
- `git diff`: 103910 bytes, sha256 `daa7a2a666c7481b02396232df4ddd60dfe54c972937a1ca9411778edff70c79`.
- `trust_bootstrap.rs`: 43086 bytes, sha256 `4aaf78e2…9664`.
- `trust_bootstrap_tests.rs`: 36930 bytes, sha256 `229b1589…d7da`.

## Inventory v113 (rebuilt on v116)
Built on the inventory the lock selects at a34dc6b: `repository-file-inventory.v116.json`, 425975 bytes, sha256 `f087978d92e5e27c7f9e01fbda904ccc7f0ed75400e921fefdf7cc6290789554` (unit X4a). v116 is v117's 835 rows plus X4a's eight; no row X4B-a touches changed.
- `repository-file-inventory.v113.json`: 429574 bytes, sha256 `c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`. It has 845 files: all 843 v116 rows by value, plus the same two rows.
- `trust-bootstrap-x4ba-inventory-v113/successor.json`: 20193 bytes, sha256 `2b40d9fad8941c83ccd662d13b4ee5415e79ba1fcdad0632477b2ef589c1298e`. The sixteen overrides are re-projected by path from v116's record.

**Changes in the builder:**
- `evidence/build_v113.py` adds the committed successor records of v117 and v116 to PRIOR, beside v114. It updates the docstring.
- Three phrases in the two row descriptions now state the RF-1 behaviour:
  - the service row says "with the list's keyIds excluded" and names `successor_record_bindings`, which r1's code already ran;
  - the test row covers a revoked signer whose quorum survives;
  - the test row adds "a revoked counted signer that leaves a catalog or component manifest below threshold writes nothing".
- Reruns give identical bytes.

**Other refreshed files:** README "Order" and "Projection", the `verify_projection.py` comment (v116), the `verify_scratch.py` docstring, `verifier-anchor.json` (a34dc6b), and `verification.*`.

**Checks:**
- `verify_projection.py` against the real lock: PASS, 16 rows, 83 corruptions refused.
- `evidence/verify_scratch.py` on the worktree: passed, with 80 inventory successors, 72 contract successors, 16 inheritance rows, and v113 selected.
- `check_package_edges --lane host` against v113: passed, 19 declared and 19 resolved.

The files are untracked.

**Subject manifest:** `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113-subject.json`, 2144 bytes, sha256 `4db04f22c98e1330f81e62409d5789fec7bd5274bb8bdc425e8443a9808fc7a4`.

## Lead's runs (on these exact bytes)
- `cargo test --locked --offline -p opensip-security --lib trust_bootstrap`: 17 passed.
- `cargo test --locked --offline --workspace`, run twice: 1543 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: clean.
- `cargo fmt --all --check`: clean, and the two include files were run through `rustfmt --edition 2024`.

## Decide
1. Is RF-1 closed?
2. Is the rebase clean, and is the conflict resolution right?
3. Is the v116 rebuild correct?
4. Is anything new wrong?

## review.json
review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `4db04f22c98e1330f81e62409d5789fec7bd5274bb8bdc425e8443a9808fc7a4`;
- "inventoryCandidateAssessment": an object with:
  - verdict and requiredFindings;
  - path `docs/implementation/m2/repository-file-inventory.v113.json`, bytes 429574, sha256 `c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`;
  - parent: the v116 pin above;
  - successorRecord: path `docs/implementation/m2/trust-bootstrap-x4ba-inventory-v113/successor.json`, bytes 20193, sha256 `2b40d9fad8941c83ccd662d13b4ee5415e79ba1fcdad0632477b2ef589c1298e`.

Write REVIEW.md and review.json. Do not commit.
