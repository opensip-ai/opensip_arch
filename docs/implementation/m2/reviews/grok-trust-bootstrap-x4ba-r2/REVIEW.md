# X4B-a r2 — ACCEPT-UNIT

RF-1 is closed. The rebase onto `a34dc6b` keeps both modules, and inventory v113 is ACCEPT on v116.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x4ba`, detached at `a34dc6b41216285a2ceb1a4338f897ced2665c11`. Nothing is committed. Eight files: 2347 insertions, 47 deletions. `git diff` is 103910 bytes, sha256 `daa7a2a666c7481b02396232df4ddd60dfe54c972937a1ca9411778edff70c79`. All 23 `hashes.txt` pins match, including `trust_bootstrap.rs` (43086 bytes, `4aaf78e24577b7c4c7d9811023009e9541f8e6182b9408b37f2ca431ad4c9664`) and `trust_bootstrap_tests.rs` (36930 bytes, `229b158953067a304aaa2cb9288ee6a0a8b90c47e2d93ed7ce9f528bbdfbd7da`). The worktree `design-lock.json` is the file at that commit (182961 bytes, sha256 `541898d9c4a67258886eaa175b5774058c4472dad13c979198ac99d1aeb60060`), the same lock as the product checkout, and it selects inventory v116.

Law is unchanged: X4B r5, `trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e27028a50af5d1b49cccdd835a365c8066d6955052f263d87823fc62c`. Scope is the producer for items 2 to 6. Judgment call 12 stays outside this unit.

`~/Library/Application Support/OpenSIP` is absent.

## RF-1

Closed. `verify` takes the embedded list's keyId set and passes it to `filter_envelope_revoked`. The same call checks the revocation list, the bootstrap manifest (TR-BUNDLE), the core inventory (TR-CORE), the catalog (TR-INDEX) and each component manifest (TR-COMPONENT). `filter_revoked` drops those keys and compares the survivors with the role threshold already on the quorum (`required`). A state other than `Met` returns `PAYLOAD-NOT-ADMISSIBLE` with that document's subject. `authenticate` runs inside `build_acceptance`, and `accept_bootstrap` publishes only after that returns, so the refusal writes nothing.

`Document.signers` is still `valid_before_revocation`, cloned before the exclusion. `revokes` reads that set, so Revoke runs only for a document whose quorum survived.

The suite has 17 tests. `a_revoked_counted_signer_below_the_threshold_refuses_and_writes_nothing` revokes key 11 of the catalog's two TR-INDEX signers (threshold 2) and expects `PAYLOAD-NOT-ADMISSIBLE` (`catalog`), then revokes key 14 of the component manifest's two TR-COMPONENT signers and expects `PAYLOAD-NOT-ADMISSIBLE` (`component`). Both cases leave the trust tree, `state.v1` and the confirmed publication unchanged. `a_revoked_document_whose_quorum_survives_is_present_then_revoke_with_revoked_by` signs the catalog with TR-INDEX keys 11, 12 and 13, revokes 11, and expects Present then Revoke, `ST-REVOKED`, `revokedBy` naming `EV-REVOKE`, and the confirming admission's `index:revoked`. `expired_and_revoked_is_three_events_ending_revoked` uses that same three-signer catalog. The bundle and core documents go through the same `verify`; a release whose TR-BUNDLE or TR-CORE quorum fails after exclusion never reaches `from_initial_core`.

Judgment call 3, as revised, matches the code. A document that `verify` returns has a met quorum, and the producer dispatches `PresentOrdinary` with `Admissible`. `Inactive` and `Rejected` are reached only through `bootstrap_sequence`, and that test still expects an empty record. Calls 1, 2 and 4 to 14 are unchanged. The two-root test still pins the reader's `FirstIdentity` refusal. That remains the X4T amendment and the reader successor, before X4B-b.

## Rebase

Clean. `daa7b01..c2352ae` does not touch any of the eight paths. `c2352ae..a34dc6b` touches two: `current_trust_admission.rs` gains 50 lines (the `ViewClosure` and `AdmittedRevocation` fields, their construction, and the `live_observation` module), and `floor_publication.rs` changes one header comment. The comment and the X4B-a `may_create` and `TrustWrite` hunks are disjoint, and the uncommitted diff against `a34dc6b` is those X4B-a hunks.

The one overlap is the child-module point after the `floor_publication` re-exports. The worktree keeps X4a's `live_observation` block, then a blank line, then X4B-a's `trust_bootstrap` block. The uncommitted diff adds only the `trust_bootstrap` lines. Neither file mentions the other module. There are no conflict markers. The other four modified files are the X4B-a diff against a base those two commits left unchanged, and the two new files are intent-to-add.

## Inventory v113

ACCEPT on v116.

`repository-file-inventory.v116.json` is 425975 bytes, sha256 `f087978d92e5e27c7f9e01fbda904ccc7f0ed75400e921fefdf7cc6290789554`, 843 files. That is v117's 835 rows plus X4a's eight. `repository-file-inventory.v113.json` is 429574 bytes, sha256 `c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`, 845 files: every v116 row equal by value, plus `trust_bootstrap.rs` and `trust_bootstrap_tests.rs`. Sorted, no duplicate paths, no removals. Packages, pending decisions, and the other non-file keys match. `standing` is the X4B-a proposed-layout sentence. `carriedUnresolvedObligations` matches the v116 successor record.

The successor is 20193 bytes, sha256 `2b40d9fad8941c83ccd662d13b4ee5415e79ba1fcdad0632477b2ef589c1298e`. Its parent and candidate pins match. Sixteen projection rows: each `before` and `effectiveDescription` is the v116 row's text, `parentSelector` is that row's candidate selector, and `candidateSelector` is the path's index in v113. The stored descriptions of those inherited rows stay the parent text. Flags `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged`, and `pendingDecisionsInheritedUnchanged` are true.

The service row says each document is checked at its role's threshold with the list's keyIds excluded, and it names `successor_record_bindings`, which the publisher calls. The test row names a revoked signer whose quorum survives, and a revoked counted signer that leaves a catalog or component manifest below threshold and writes nothing. `build_v113.py` lists v114, v117 and v116 in `PRIOR` and was not run.

`verify_projection.py` against the worktree lock: PASS, 16 rows, 83 corruptions refused, `directParentOverrideIncluded` true. `verify_scratch.py` on the worktree: passed, 80 inventory successors, 72 contract successors, 16 inheritance rows, v113 selected. `check_package_edges --lane host` against v113: passed, 19 declared and 19 resolved.

The subject manifest is 2144 bytes, sha256 `4db04f22c98e1330f81e62409d5789fec7bd5274bb8bdc425e8443a9808fc7a4`, and its ten pins match.

## Replay

`cargo test --locked --offline -p opensip-security --lib trust_bootstrap -- --test-threads=1`, with `CARGO_TARGET_DIR` under this review directory: 17 passed, 0 failed, 8.35s. The target was removed. Home is still absent.

The lead's workspace suite (1543 passed, twice), clippy `-D warnings`, and `cargo fmt --all --check` were not replayed.

## Verdict

ACCEPT-UNIT. RF-1 is closed. The rebase resolution is the two modules in order, X4a's block first. Inventory v113 is ACCEPT on v116.
