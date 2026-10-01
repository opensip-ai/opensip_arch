# X4T-a3 r1 — ACCEPT

The reader admits a recorded rotation from accepted root N and signs under root M. The closure join compares the last `rootChain` document with `heads.root.document`, body and envelope, before `ordinary_inventory::prepare` can classify that mismatch as `SigningRoot`. `verify_captured_core` is unchanged. There is no inventory successor.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x4ta3`, detached at `0fc8ea21a5d2881624d0cb296ff7cae5981c5a64`. Nothing is committed. Seven modified files, no additions: 624 insertions, 49 deletions. `subject.diff` is 38998 bytes, sha256 `ddd2e27ef0ebbf2f0ac214d4681988b37a93d7c7119a7a69e39f23881177ecb0`. All 13 `hashes.txt` pins match, including the seven product files and that diff. The worktree lock selects inventory v113 (`c35788a82f5b2561e6fb0df9b920def2c978790555190a9dc0f5a9105e7f5874`, 429574 bytes).

Law is X4T r11. `PROPOSAL-r11.md` is 53342 bytes, sha256 `7fe098fd30de298cf1e09ca6514d8a50eef6a328cb25bda6ebcf4398353cd384`. The live `PROPOSAL.md` is 53378 bytes, sha256 `8116f487a852675627bd61f6ccac7d8e7dab360e49dce80d683b78795c2c1db5`.

`~/Library/Application Support/OpenSIP` is absent.

## Law

Item 3 is implemented in `current_trust_admission::authenticate`. After the root admission's `root` matches `head.document()`, `bind_chain_anchor` loads the admission's `parent` as `PayloadMetadataClosureV1`, requires the last `rootChain` document to equal that head document, and admits `rootChain[0].body` as root N. `authenticate` passes `anchor.authentication_context(VIEW_CHAIN)` as the accepted root and `head.root()` / `head.document()` as the signing root into `prepare_authenticated_times`, which calls `authenticate_shared` and then `verify_captured_core`.

The diff of `trust_ordinary_roots.rs` adds `Error::EmptyChain` and `bind_chain_anchor` after `bind_retained_head`. `verify_captured_core`, `authenticate_shared`, `bind_retained_head`, and `RetainedHead::authentication_context` are unchanged. `verify_captured_core` still compares the first body value with the accepted root, the last body value with the signing root, verifies N's envelope after revoked-key exclusion, and authenticates the links after the first from N.

Item 4 (r11) needed no new reader branch. `open_heads` sets `root = input.head.root()` and passes that value to the catalog's `verify_envelope` and to `verify_revocation`. `the_revocation_list_is_verified_under_the_signing_root` admits a 1→2 list signed by root 2, carries the entry, and refuses a list signed only by seeds 0 and 1 as `PAYLOAD-NOT-ADMISSIBLE`.

Item 7 is unchanged. `admit_bound` sets the epoch `rootVersion` from `input.head.root()` and the floors from `Floors::of_clock` on the capsule clock. The rotation tests observe epoch and floor `n` on the fenced read, the report-only read, and the reread. N is visible on the proof (`original_accepted_ref`, `chain().links()`, `accepted_version`) and is not a floor.

Item 10's incomplete row is the existing `roots_row` catch-all. `EmptyChain`, `FinalIdentity`, `FirstIdentity`, and `Shape` map to `TrustRow::Incomplete` (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`). Chain errors still go through `chain_row`. `Envelope` and `FirstQuorum` stay `PAYLOAD-NOT-ADMISSIBLE` (`root`).

Item 11 counts N with the chain. `chain_bytes` sums the unresolved roots' bodies and envelopes and drops the head's two digests. `a_recorded_rotation_is_admitted_from_its_first_root_at_the_final_roots_epoch` expects that sum to equal N..M−1. For n = 1 the sum is empty, which is the existing one-root pin. The head stays in the closure total.

Item 12's r10 bullet is the five admission tests, the rotated floor-publication test, and the one-root case inside the rotation test. Item 13's X4T-a3 is this reader. The fixture is X4T-0's `quorum_root` and `sign`. It does not call X4B-a's producer.

## Join before SigningRoot

`bind_chain_anchor` compares `last != head.document()` and returns `FinalIdentity` before `prepare_authenticated_times`. `ordinary_inventory::prepare` then requires `chain.contains(signing_root_ref)` and a body-value match, and a miss is `SigningRoot`. `roots_row` sends a shared `SigningRoot` through `quorum_row`.

`OtherEnvelope` stores a second envelope over the head body and puts that document last. The body matches M and the document reference does not, so the join returns `FinalIdentity` on the incomplete row. `Short` drops the last document and takes the same row. Both are pinned at n = 1 and 2 (`OtherEnvelope`) and n = 2 and 3 (`Short`), on the fenced path and the reread. A join that ran after `prepare` would let `SigningRoot` classify those stores.

`PayloadMetadataClosureV1.rootChain` is `minItems` 1 and `maxItems` 64 (`tools/security/inputs/trust-record-schema.json`). An admitted closure cannot reach `EmptyChain`. `ChainEnd::Empty` writes the closure with `unshaped_record`, and the test expects cause `Shape`. `EmptyChain` remains the explicit join and maps to the same incomplete row. The test pins `roots_row` for all four join errors.

One root is the same function. `rootChain[0]` is the head document, already retained by `bind_retained_head`, and there are no links. The rotation test includes n = 1, and `MEASURED` bytes stay 35371.

## Revoked keys inside authenticate

`prepare_shared` verifies the closure's revocation list against the signing root and copies its `keyId` subjects into the union before `verify_captured_core`. N's envelope and the links are filtered with that union. The first-root case that revokes seeds 1 and 2 under root 2 refuses `Times(Rooted(Roots(FirstQuorum)))`. The 1→3 list that revokes seeds 20 and 21 refuses `ROOT.CHAIN_NEW_THRESHOLD` / `link:0`. `admit_revocation` still re-filters the catalog and the list and still refuses a named closure component on the continuation row. The existing component test passed in this replay.

## Fixture

`Spec.roots` defaults to 1 and `ChainEnd` defaults to `Head`. Root 1 is `quorum_root(1)`. Root k+1 clones it, sets `rootVersion` k+1 and `previousRootVersion` k, and moves `rootKeys` through `[0,1,2]`, `[20,21,22]`, `[23,24,25]`. Later roots keep root 1's `keys` array, so `sign` against `&first` resolves seeds 20–25. Root 1's envelope uses three signatures. Each link uses the previous set and the new set, six signatures. The list and the catalog are signed against root n. Default revocation signers are the first two of root n's ROOT keys, which for n = 1 is `[0,1]`. Catalog `rootVersionRequired`, clock `rootVersion`, and the list's `rootVersion` follow n. At the defaults those values are 1, and the manifest envelope order is `catalog.sig`, `revocation.sig`, `root-0.sig`.

`a_recorded_rotation_lists_the_chain_with_the_head_last` checks n = 2 and 3: the closure lists n documents ending on the head, the root admission's `root` is the head, each body is version k+1, root 1 has three signatures and each link six, the list is at version n, and `current_record_bindings::bind` and `bind_retained_head` accept the store.

## X4B-a

`a_multi_link_root_chain_is_authenticated_and_recorded_in_full` still records the default 1→2 release: `heads.root` binding `rootVersion` 2, `clock.record` `rootVersion` 2, closure `rootChain` length 2. `confirm()` now expects the view to admit with epoch `rootVersion` 2 and `rootVersion` floor 2. That is the r10 note on X4B and the close of judgment call 12. The test passed in this replay.

`a_floor_publication_on_a_rotated_store_is_followed_by_an_admitted_read` uses `Spec { roots: 2 }`. The first fenced read admits at epoch and floor 2, the published `state.v1` differs from the bytes read before publication, and `heads` text is unchanged. A later invocation's fenced read admits with `InstallGateRequiredForNewProcess` at epoch and floor 2. The native reread admits at epoch 2.

## Pins

`MEASURED` is `(23, 46, 35_371)`. `NATIVE_MEASURED` is `(31, 265, 36_008)`, asserted at compile time to be within `TRUST_VIEW_COST`. `NATIVE_AFTER_FLOOR` is `(31, 265, 32_103)`.

`Budget::load_at` charges one edge, then returns a retained `(collection, digest)` when `refresh_cached` is false. The in-memory digest store returns false, so the anchor's reload of a body `bind_retained_head` already holds, and `prepare`'s reload of the closure the anchor just retained, are two edges and no new object or byte. The closure's retaining load is the one `prepare` used to make. Objects stay 23 and bytes stay 35371.

A native store returns `refresh_cached` true, so each of those two loads reads again. `capture_with` charges one edge per parent, and `directory` charges one edge on every visit and one object only for a new device/inode. The parents are `trust/` and the collection. With the `load_at` edge and the file edge, a revisit is six edges. Two revisits are twelve. Objects stay 31 and bytes stay 36008, and 32103 after the floor publication. `the_view_cost_is_measured_and_within_the_ceiling` and the post-floor native assertion passed.

Passing the admitted closure into `prepare` would change the ordinary-inventory and ordinary-targets signatures. Item 3 does not ask for that.

## Judgment calls

1. No inventory successor. No file is added. `verify_design.inventory_successor` admits a strict sorted superset, requires every inherited row equal by value, and requires review verdict `ACCEPT-UNIT` with an inventory assessment `ACCEPT`. A description-only edit cannot be selected. v113's `trust_bootstrap_tests.rs` row still ends "with the reader's current FirstIdentity refusal pinned as a stated gap." That sentence is now false, and it belongs in the description-only batch, with the descriptions v116's README already marked out of date. `current_trust_admission.rs` still "authenticates the accepted state from the accepted root," which is now N. `trust_ordinary_roots.rs` stays generic. This review is `ACCEPT` and carries no `inventoryCandidateAssessment`.

2. An empty `rootChain` is refused by the closed shape. The test drives that with the one unshaped record and expects `Shape`. `EmptyChain` stays in the join and on the incomplete row.

3. The closure is loaded in `bind_chain_anchor` and again in `prepare`. The in-memory second load is an edge. The native second load is the six-edge revisit above.

4. A first `rootChain` body that does not admit as a root is `FirstIdentity` on the incomplete row. `PAYLOAD-NOT-ADMISSIBLE` stays the signature and quorum rows. The below-threshold tests expect `FirstQuorum`.

5. `bind_chain_anchor` always loads `rootChain[0].body`. The one-root store is that path.

6. `AdmittedCurrentTrust` gains no field. Epoch and floors stay M. Tests read N from the authentication proof.

7. r11 needed no reader change. `open_heads` already passed `input.head.root()` to both verifiers, and the new test pins admission under M and refusal under N's keys.

8. The rotation follows `signed_release`'s shape: `rootKeys` move to unused seeds, links are signed by both sets, and the list is signed under the final root. The generator is `quorum_root` and `sign`.

9. The older "root chain through expired intermediates" case is outside the r10 bullet assigned to X4T-a3. `authenticate_root_chain` takes no evaluation time.

The catalog comment in `open_heads` still says the envelope is reverified against the accepted root. The value passed is `input.head.root()`, root M. The r11 test pins both directions. The comment does not change the call.

`ordinary_targets::prepare_clock_input` still builds its accepted context from the retained head. `current_trust_admission::authenticate` does not call it. Item 13 assigns the two-root split to `authenticate`. The ordinary-targets tests in this replay passed, including the existing real-host clock test remaining ignored.

The lead's first full workspace run failed `custody::operation_handoff::tests::live::a_revoking_update_is_seen_by_the_checkpoints_own_final_observation` in scratch setup with `Custody { subject: "ancestor-acl" }`, then passed three times in isolation. The test uses the default one-root store. This diff does not reach that setup. Runs 2 and 3, as reported by the lead, were 1550 passed, 0 failed, 3 ignored. I did not replay the workspace, clippy, rustfmt, package edges, or `verify_design`.

## Replay

`cargo test --locked --offline -p opensip-security --lib -- current_trust_admission accepted_store_fixture floor_publication live_observation ordinary_roots ordinary_targets trust_bootstrap`, with `CARGO_TARGET_DIR` under this review directory: 79 passed, 0 failed, 1 ignored, 808 filtered out, 32.52s. The ignored test is `actual_current_samples_feed_owned_s4_with_authenticated_inputs`. The target directory was removed after the run.
