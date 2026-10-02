# X4B-c r1

Verdict: **ACCEPT**. No required findings. No inventory candidate.

The subject is `subject.diff`, 45126 bytes, sha256 `9bfd8e13b6d5f353caefd12343ac7b9ccd927f6fec8021845a400e21f02337e2`. Nine existing files under `crates/security/src/trust/` change, 735 insertions and 59 deletions. The worktree `/Users/sb/code/opensip-ai/opensip-x4bc` is detached at `f097c5b7dbc818c09a9849e815e67787b4548740`. Its lock selects inventory v125 (`1d157eea04974577502cc584b611c1ad77953214ca153eb1e14e514289df2d10`, 506284 bytes; 85 inventory successors, 55 inheritance rows). The worktree adds no file. All 17 pins in `hashes.txt` match.

## Item 9

The diff implements X4B r5 item 9.

On macOS, `generate` tries `produce` and, when that returns `None`, calls `construct`. `construct` is the previous generator. `p0_publication`, `signed_chain`, `anchor`, and `invocation` are the same values in the same order; `signed_chain` changes `expiresAt` only when `produce` asks it to. On any other target the `produce` functions are absent and every store is constructed. Linux is not claimed.

`Knobs::for_roles` judges the whole six-role request. TR-PROFILE and TR-REPAIR must be `Unbootstrapped`. TR-BUNDLE, TR-CORE, and TR-INDEX must be carried. TR-COMPONENT may be `Unbootstrapped`, which means no component manifest. It then walks the eight `(root expired, catalog expired, stale)` combinations in binary order. For each carried role it runs `role_machine::bootstrap_sequence` with `BootstrapEntry::Admissible`, expiry set from the root for every carried role and from the catalog for TR-INDEX, staleness store-wide, and revocation set exactly where the request says `Revoked`. The first combination whose end states match the request wins. `State::Recovery` maps to no `RoleTarget`, and the sequence never emits `QuorumLost`, so those requests miss.

`produce` returns `None` when `chain_end` is anything other than `Head`, when a root or list signer is replaced, when no knobs fit, when `build_over_p0` refuses, or when any stored role state differs from the request. The last clause covers a caller list entry that revokes a document the request still calls `Trusted`: `revokes` matches a `keyId` among that document's signers, the namespace `opensip` on every envelope, `release` equal to `CORE_CLOSURE` on TR-CORE, and `catalogSnapshot` equal to the catalog's snapshot on TR-INDEX. A root key that signed no role document does not move a role, so that store is produced with every role `Trusted`.

The retained records on the produced path are `build_over_p0`'s files at `TrustWrite::path`, de-duplicated against P0, then the producer's `state.v1`. The payload is signed with the public quorum62 seeds: the same root chain, a final-root `expiresAt` of `2026-10-01T12:00:00Z` when the root must be expired, the caller's list entries plus the third signer of each revoked role, issued `2026-07-01` when stale and `2026-10-01` otherwise, a TR-INDEX catalog with the component release row, 463h's component manifest under TR-COMPONENT unless that role is uncarried, a TR-BUNDLE manifest, and a TR-CORE inventory. `BootstrapPayload::from_parts` still receives `CORE_CLOSURE`.

`x4b_produces_every_request_its_sequences_reach` pins ten reachable requests as produced, with each role's events equal to its item 4 sequence (`EV-PRESENT-PAYLOAD`, then `EV-CLOCK` only when expired or stale, then `EV-REVOKE` only when revoked), `accepted.by` on the present event, and `revokedBy` on the revoke event or null. The reference binders accept each store. The default store's `evalHighWater` is W (`2026-10-02T00:00:00Z`) and `lastAccepted` is A (`2026-10-01T00:00:00Z`), which is S4 step 2's L := A. Quorum root 1 is issued at that same A and expires in 2027 unless the knob rewrites the final root.

`a_request_no_acceptance_reaches_is_constructed` pins ten unreachable requests on `construct`, each still in its requested states: all targets, six trusted, quorum lost, a lone expired core, a lone stale component, an uncarried index, another envelope, replaced root signers, replaced list signers, and a list that names `CORE_CLOSURE`.

`no_production_source_reaches_the_constructor` is unchanged. `root_payload.rs` still declares the module under `#[cfg(test)]` only. `only_the_producer_and_the_generator_call_the_store_builder` limits the text `build_over_p0(` to `trust_bootstrap.rs` (the definition and `build_acceptance`'s one call) and `accepted_store_fixture.rs` (one call).

## Producer behaviour

`build_acceptance` now passes `owner.capsule()` and `owner.raw()` into `build_over_p0`. Those are the capsule and the exact bytes the old function read from the owner. The rest of the body is the same function: `is_p0`, the observation, `authenticate`, S4 step 2, `bootstrap_sequence`, and the records. It writes nothing and grants nothing. `accept_bootstrap` and `bootstrapping_first_read` are absent from the diff. The producer's own suite passed on these bytes, including an expired catalog, an expired root, a stale list, a revoked signer whose quorum survives, three events for expired-and-revoked, and no component manifest.

`TrustWrite::path`, the modules `current_trust_admission` and `trust_bootstrap`, `BootstrapAcceptance::files`, and `build_over_p0` are `pub(in crate::trust::root_payload)`. `accepted_store_fixture` is a child of `root_payload`, so it can call them. `trust_bootstrap` stays `cfg(target_os = "macos")`. The diff adds no `cfg` on a production item and no `cfg(test)` re-export. The joint predicate of X8 r3 item 4b and X9 r2 item 6 still has one site for this module, the existing `#[cfg(test)]` declaration. X9-1, which widens that site, is in flight elsewhere. This unit does not add a site outside X9-1's list.

A stored state on the produced path is a state `decide` accepted inside `bootstrap_sequence`. When the producer refuses, or stores some other state, `produce` returns `None` and the test-only constructor remains the only writer of that store. The constructor stays unreachable from production.

## Calls 1 to 8 and 10

1. **No inventory successor.** `verify_design` admits only a strictly additive successor, and this diff adds no file. v125 stays the selected inventory. The v125 row for `accepted_store_fixture.rs` is now false and belongs to a later description batch. It says the module builds the retained publication itself, with one conditioning event per role, and that "It is the only constructor of these kinds and no production path reaches it; X4B owns the real producers." Reachable requests are now the producer's records over the module's signed payload. The module remains `cfg(test)`, and no production path reaches it. The already-listed `trust_bootstrap.rs` sentence "Not wired to the fenced first read (X4B-b)" is unchanged. The rows for the test file, `build_over_p0`, and the two moved pins are understated and still true in what they claim. The rows for `core_authentication.rs`, `current_trust_admission.rs`, `floor_publication.rs`, and `ordinary_targets.rs` are untouched in substance.

2. **Whole-request reachability.** One acceptance has one set of time inputs and one list. Expired is produced through an expired catalog (TR-INDEX only) or an expired root (every carried role). Stale revocation is produced only store-wide. Revoked is produced per role, through a signer the list names, including after a clock when the root is also expired. A lone expired core and a lone stale role stay constructed, as do `QuorumLost`, an accepted TR-PROFILE or TR-REPAIR, and an uncarried TR-INDEX. Deleting `construct` would drop item 12 cases item 9 keeps. `RoleTarget` has no `Recovery` variant.

3. **Below publication.** `generate` calls `build_over_p0` over P0 bytes from `initial_publication::build`. It does not call `accept_bootstrap`. Files are placed by `TrustWrite::path`. `write` remains a plain layout: no barriers and no confirm.

4. **Joint predicate.** See the visibility paragraph above. The fixture's new dependencies are production items, the macOS-only producer, and `core_authentication::tests::{component_body, component_release}`, factored out of `signed_release` with the same bytes. That tests module is a site X9-1 already widens. The inner `cfg(target_os = "macos")` on `produce` sits inside the existing test module. The X9-1 feature simulation was not replayed.

5. **Synthetic inventory.** The inventory body is `embeddedBootstrap` (directory, envelope, manifest, each with bytes, path, and sha256) and `inventorySchema` 3, signed under TR-CORE by keys 8, 9, and 10. `authenticate` verifies that envelope. The record builder pushes the manifest, catalog, revocation, component manifests, and root-chain blobs. It does not push the inventory pair. `from_parts` still takes `CORE_CLOSURE`, and the consumer tests pass that same closure.

6. **Pins.** Produced `Spec::default()` records `lastAccepted` A and keeps `evalHighWater` W. It adds `component-0.json` and its envelope, a catalog release row, and a third signature on the catalog and bootstrap-manifest envelopes. `NATIVE_MEASURED` moves from `(31, 265, 36_008)` to `(33, 291, 40_885)`: 2 objects, 26 edges, 4,877 bytes. `NATIVE_AFTER_FLOOR` moves from `(31, 265, 32_103)` to `(33, 291, 36_979)`: the same objects and edges, 4,876 bytes. Both native tests passed, so the live charges equal those triples. `MEASURED` stays `(23, 46, 35_371)` because its six-role store is constructed. The const assertions `NATIVE_MEASURED` against `TRUST_VIEW_COST` compiled.

7. **macOS only.** The new producer-route test is `cfg(target_os = "macos")`. The constructed-request test is not.

8. **Source pin.** Unchanged, as item 9 requires. X9-1's rebase is that unit's own diff.

10. **Recovery.** `RoleTarget` is `Unbootstrapped`, `Trusted`, `Expired`, `StaleRevocation`, `QuorumLost`, and `Revoked`. Item 9 names Recovery only as a test-only state acceptance cannot reach. This unit does not offer it.

## Call 9

Call 9 is accepted as a reading of the two laws, and it is not a finding against this code.

X4T r11 item 13 defines X4T-0 as the test-only record constructor and rejects "moving X4B before X4T-a, which would lengthen the critical trust chain and couple the reader to acceptance." The same item's X4T-a3 bullet rejects "building X4T-a3's tests on X4B-a's producer or test release, which couples the reader to acceptance (as item 13 already rejects)." That rejection governs how X4T-a3 was built: the reader tests landed before, and independently of, X4B-a's producer.

X4B r5 item 9 is the later, accepted step: "Once X4B's producer exists, X4T-0's test-only constructor is replaced by calls to it, wherever X4B can produce the requested role states." Item 11 names X4B-c as that step. This diff is that step.

After it, X4T-a3's lawful rotated stores (`roots` 2 and 3, `ChainEnd::Head`, default roles) are produced. `a_recorded_rotation_is_admitted_from_its_first_root_at_the_final_roots_epoch` still asserts the reader's split: the closure `rootChain` starts at the accepted root, `heads.root` is the signing root, the epoch and the root-version floor are the final root's version, and the standing is `InstallGateRequiredForNewProcess`. The refusal stores stay on `construct`: other envelopes, short and empty chains (`a_closure_chain_not_ending_on_the_head_is_incomplete`, still `Incomplete` with `FinalIdentity` or `Shape`), and replaced signers (still the S5 rows, including `ROOT.CHAIN_OLD_THRESHOLD` and `ROOT.CHAIN_NEW_THRESHOLD`). The reader's code does not call the producer. Exercising the producer's output from the reader tests is item 10's round trip.

A reading that item 13 forbids this later move would be a finding against the law. This review does not reopen X4T r11 or X4B r5.

## Consumer purpose

The X4T-a assertions are unchanged apart from the two measured pins. They still name the reader's rows.

`each_continuation_refusal_names_its_role_and_state` still expects `TrustRow::Continuation` with the role and state in the subject. Core `Revoked`, index `Revoked`, and component `Unbootstrapped` are requests one acceptance reaches, so those three now run on produced stores. Core `QuorumLost`, core `Expired` alone, index `QuorumLost`, index `Unbootstrapped`, and component `StaleRevocation` alone stay constructed. `an_expired_or_stale_index_is_admitted_as_existing_only` admits index `Expired` from the producer and index `StaleRevocation` alone from `construct`, and still expects `ExistingOnly`.

`a_revoked_closure_component_refuses_by_kind_and_subject` still expects `CONTINUE-CORE-NOT-TRUSTED` with subject `kind:subject` on a fenced read and a reread, for all four entries. The `release` of `CORE_CLOSURE`, the namespace `opensip`, and `catalogSnapshot` `1` make `revokes` end a carried role `Revoked` while the request says `Trusted`, so `produce` returns `None` and `construct` keeps the old store. The `keyId` is root key 2. That key signs the root envelope, not a role document, and the list itself is signed by the final root's first two keys, so the producer accepts every role `Trusted`. The reader's `admit_revocation` then refuses because that key is in the closure's signing keys. The refusal is the reader's closure check.

`entries_naming_no_closure_component_are_admitted_and_carried` names an unrelated release, an unused key, namespace `elsewhere`, `catalogSnapshot` `2`, and `CORE_CLOSURE` under kind `namespace`. None of those match `revokes`, so the store is produced with every role `Trusted`. The test still expects the reader to carry those entries and to refuse `release:` of a different running core. `the_revocation_list_is_verified_under_the_signing_root` admits an unused key on a produced two-root store, and still refuses a list signed only by root 1's keys, which `produce` declines because `revocation_signers` is set.

## Replay

Private `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-x4bc-grok.54pJXQ`, mode 0700, under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` was the `target` directory beside this review, removed after the runs. Toolchain `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`. Cargo was `--locked --offline`.

- `cargo test -p opensip-security --lib`: 945 tests, 907 passed, 36 failed, 2 ignored. Every failure is under `custody::`. Every `trust::` result in that run passed, including `x4b_produces_every_request_its_sequences_reach`, `a_request_no_acceptance_reaches_is_constructed`, `only_the_producer_and_the_generator_call_the_store_builder`, the producer suite, the continuation and closure-revocation cases, the rotation and non-head cases, `the_native_read_admits_the_written_store_and_rechecks_state_v1`, and the floor-publication suite.
- A serial rerun of those 36 names (`--test-threads=1`, same `TMPDIR`) ran 37 tests, because `a_busy_installation_fence_ends_in_the_busy_row` also matches `ordinary_writer`. 16 passed and 21 failed. The failures are `ancestor-acl`, `ChangedDuringRead`, and chain `Capture { component: 6, error: Changed }`. Other worktrees were running cargo against this same user temporary parent during both runs. The failing tests do not read this diff. They are not a finding.
- `cargo fmt --all -- --check` exited 0.
- `python3.14 -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .` passed: v125 selected, 85 inventory successors, 74 contract successors, 55 inheritance rows, 4 supersessions.

Not replayed: the workspace suite, workspace clippy, the crash-matrix clippy, `check_package_edges.py`, and the lead's scratch simulation of X9-1's joint predicate. The removed byte-identity harness was not put back. `~/Library/Application Support/OpenSIP` was absent at the start and at the end.
