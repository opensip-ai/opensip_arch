# X4B-a r1 — REQUIRED-FINDINGS

The producer implements items 3 to 6, the chain authentication, and the record shapes. Item 2's revocation exclusion does not. The catalog and each component manifest are checked with an empty revoked set, and the pinned "revoked signer" test records `ST-REVOKED` for a quorum that item 2 requires to refuse.

Inventory v113 is ACCEPT on v114.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x4ba`, detached at `daa7b0130027937c1de371d4ca6efe7e996deaaf`. Eight files, uncommitted: 2294 insertions, 47 deletions. `git diff` is 101814 bytes, sha256 `04ce6fd0a6aaa83c8d66caf58d35eff162e9a4a4b390fa46bee429e1215efc77`. All 23 `hashes.txt` pins match. The worktree `design-lock.json` is the unmodified file at that commit (180739 bytes). The product checkout has since moved to `c2352ae`; its lock is a later file. This review uses the worktree lock.

Law is X4B r5, `trust-bootstrap-x4b/PROPOSAL.md`, 21587 bytes, sha256 `77b9ab1e27028a50af5d1b49cccdd835a365c8066d6955052f263d87823fc62c`. The reviewed r5 text matches `PROPOSAL-r5.md` plus the acceptance note. Scope is X4B-a: items 2 to 6 and this unit's part of item 10. X4B-b and X4B-c are out of scope.

`~/Library/Application Support/OpenSIP` is absent.

## RF-1. Document quorums ignore the embedded revocation

Item 2 (r5) reverifies the catalog under TR-INDEX and each component manifest under TR-COMPONENT, against the final root, with the embedded revocation's keys excluded, at that role's quorum. A failure is `PAYLOAD-NOT-ADMISSIBLE` and writes nothing. The same item re-filters the index-0 root, every link, and the list's own quorum, and cites law 463 item 5's order. That order's step 3 also requires the TR-CORE and TR-BUNDLE quorums still met after the same key set.

`verify` in `crates/security/src/trust/trust_bootstrap.rs` calls `filter_envelope_revoked` with an empty set. The list's `keyId`s are applied only to the anchor quorum, each link's continuity and possession, and the list itself. The catalog, the component manifests, the bootstrap manifest, and the core inventory all go through `verify`, so a key the list revokes still counts toward those thresholds.

The root in `quorum-roots.json` (schema 1) sets TR-INDEX `threshold` to 2. `INDEX_SIGNER` signs the catalog with keys 11 and 12. `a_revoked_document_is_present_then_revoke_with_revoked_by` revokes key 11 and expects Present then Revoke, a durable `ST-REVOKED` index, and the continuation row `index:revoked`. After exclusion that quorum is one signature. Item 2 requires `PAYLOAD-NOT-ADMISSIBLE` (`catalog`) and an unchanged P0. Item 4's Revoke, which uses the signers from before filtering, applies when the quorum still meets after exclusion. Judgment call 3's "unfiltered" reading contradicts the r5 sentence.

Required: exclude the list's `keyId`s inside `verify`, which is the check for the catalog, the component manifests, the bundle, and the inventory. A quorum that fails after exclusion refuses `PAYLOAD-NOT-ADMISSIBLE` and writes nothing. Retarget the two-signer TR-INDEX case to that refusal. Keep Present then Revoke for a quorum that still meets, with the revoked key among the pre-filter signers.

Replay of `cargo test --locked --offline -p opensip-security --lib trust_bootstrap` passed this test, so the suite currently pins the unlawful outcome. 16 passed, 0 failed.

## Judgment call 12

r9 needs amending. Item 3 of X4T r9 authenticates the view from the installation's accepted root, `heads.root`, through `bind_retained_head` and `authenticate_shared`, and reverifies documents against that root's keys. `current_trust_admission::authenticate` passes the retained head as the accepted root and as the signing root. That is the behaviour the item states, and it is what the accepted X4T-a reader does.

The same item also says a chain N+1..M in the closure is evaluated link by link. `verify_captured_core` requires the closure's first body to equal the accepted root and its last body to equal the signing root, then evaluates `skip(1)` from the accepted root. With both ends set to the head, a chain whose first root differs from the head fails `FirstIdentity` before a link is evaluated. The default test release rotates root 1 to root 2. Acceptance records both bodies, sets `heads.root` and `clock.record.rootVersion` to root 2, and the confirming admission then refuses `FirstIdentity`. `a_multi_link_root_chain_is_authenticated_and_recorded_in_full` pins that, and this replay passed it.

The reader the lead recommends takes the chain's first root as the accepted root and the head as the signing root. That split is what `verify_captured_core` needs for a rotated chain, and it makes the accepted root a document other than `heads.root`. Item 3 has to say so before an X4T-a successor implements it: `heads.root` stays the signing (final) root that document signatures use; the accepted root is the closure `rootChain`'s first body; the links after the first are the N+1..M evaluation under S5. X4B-a already writes that record, because the inventory `RootCount` join requires the closure chain to match the manifest and the documents are signed by the final root. The amendment and the reader successor come before X4B-b. This unit does not own the gap, and it is not a finding here.

## The other calls

1. Accepted. `BootstrapDocuments` retains the revocation pair's stored bytes beside the r9 pairs. `bootstrap_release` lends the embedded binding, the manifest and inventory pairs, and the chain. `InitialCore` still makes no trust decision on the catalog and component manifests.

2. Accepted. The chain starts at the index-0 body, checked against the embedded binding, authenticated with an empty initial set inside `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }`. The list's keyIds then re-filter that anchor, each link, and the list. Chain errors use X4T's `chain_row`.

4. Accepted. A list entry revokes a role when it names a pre-filter signer of that role's documents, a namespace one of those documents is signed for, the running core's `release` for TR-CORE, or the catalog snapshot for TR-INDEX. `newer_and_byte_valid` is true.

5. Accepted. `evaluate_fresh_install` uses the unchanged kernel. An expired final root sets `expired` for every carried role; an expired catalog adds TR-INDEX; a list with `issue + 90 d < tEval` sets `stale` (`evaluation > issued + 90 d`). When both hold, `decide` stores `Expired` before Revoke. The replay's expired, stale, and expired-and-revoked tests match those sequences.

6. Accepted. A is the max of the manifest, catalog, and list issue times and the final root's issue time. Inventory and component-manifest issue times are not inputs. The single-root confirming admission admits and writes nothing.

7. Accepted. Time evidence is `TimeEvidenceV1` (`inputSchema` 1) with `SignedTimeSourceV1` `{ordinary, closure}`. The clock-write event goes `unevaluated` to `evaluated`. Role events cite that clock write. Accepted standings carry the final-root binding, the root admission, the role's root namespaces, `catalog` for TR-INDEX only, and `by` set to that role's `EV-PRESENT-PAYLOAD`.

8. Accepted. Objects are the chain bodies and envelopes and the list, catalog, manifest, and component pairs. The core inventory is verified and is not an object, and no record references it. Closure members are the manifest's `envelopes` and `manifests` slots, sorted by `(slot, path)`. A listed artifact, permission policy, or repair `path` refuses `PAYLOAD-NOT-ADMISSIBLE` because those bytes are not retained.

9. Accepted. `may_create` admits the `trust/objects` directory at parent index 1, through the same private create and both barriers used for `by-predecessor`. `file_cost` still reserves every parent as a create. The accessors on `TrustWrite` are crate-local.

10. Accepted. The test builder signs component manifests before the catalog and lists one release row per signed component. `catalog_expires`, `revocation_issued`, and `root_expires` are the three knobs. 463h's tests are outside this replay.

11. Accepted. A non-P0 capsule returns the host I/O row, cause `acceptance-predecessor`, before authentication. X4B-b is the caller that runs this only on F absent.

13. Accepted as scope. The uncertain pointer replacement stays in `publish`. `CORE.NO_EMBEDDED_RELEASE` stays upstream of `from_initial_core`. Ordering, the monitor, the lease, read-only commands, and a second F-absent are X4B-b.

14. Accepted. Payload copies and built records are charged on the caller's ledger. The binders use `Budget::borrowed`. `publish` reserves writes and the confirmation before the first effect. The short-ledger test leaves P0 current.

## Inventory v113

ACCEPT on v114.

`repository-file-inventory.v113.json` is 397366 bytes, sha256 `057e2944772a64e079754218e7a53cc0204fc2035e88619893326aee77ed5c32`. Parent `repository-file-inventory.v114.json` is 393913 bytes, sha256 `5a6f2b74f549e2e7b8bce26e6df9f3e9b00c01039728f47e68521fc5002fceb4`. 806 files: the 804 v114 rows equal by value, plus `trust_bootstrap.rs` and `trust_bootstrap_tests.rs`. Sorted, no duplicate paths, no removals. Packages, pending decisions, and the other non-file keys match except `standing`, which is the X4B-a proposed-layout sentence. `carriedUnresolvedObligations` matches the v114 successor record. The successor's `addedFiles` are those two paths. Sixteen projection rows; each `before` equals the stored description in v113. Flags `inheritedRowsEqualByValue`, `packageDependencyGraphUnchanged`, and `pendingDecisionsInheritedUnchanged` are true.

`verify_projection.py` against the worktree lock: PASS, 16 rows, 83 corruptions refused, `directParentOverrideIncluded` true. `verify_scratch.py` on the worktree: passed, 78 inventory successors, 72 contract successors, 16 inheritance rows, v113 selected.

The README's D1 notes on `initial_core.rs` and `current_trust_admission.rs` are the inherited understated descriptions. An additive successor keeps those rows by value. The new rows describe the code as it stands, including the unfiltered document check and the pinned `FirstIdentity` gap. The code defect is RF-1; the inventory rows are the right files.

`build_v113.py` was not run. It writes the architecture tree.

## Replay

`cargo test --locked --offline -p opensip-security --lib trust_bootstrap -- --test-threads=1`, with `CARGO_TARGET_DIR` under this review directory: 16 passed, 0 failed, 8.94s. The target was removed. Home is still absent.

The lead's full workspace (1506 passed, twice), clippy `-D warnings`, `cargo fmt --all --check`, and `check_package_edges --lane host` were not replayed.

## Verdict

REQUIRED-FINDINGS. RF-1: document quorums must exclude the embedded list's keys. Judgment call 12: X4T r9 item 3 needs amending before a reader successor treats the chain's first root as accepted and `heads.root` as signing. Inventory v113 is ACCEPT on v114.
