# Review: trust floor publication X4T-a2 and X4T-b r1

Verdict: REQUIRED-FINDINGS.

Worktree `/Users/sb/code/opensip-ai/opensip-x4tb` is detached at `0206ce8673ade3689331fe22801458a03646f502`. `product.diff` is 101126 bytes, sha256 `02ad321f99a370dc33f7d49f875e856637ec38d3671fa0ee89ba036d55c8fa90`, 13 files, 1974 insertions and 84 deletions. Subject manifest `docs/implementation/m2/trust-floor-x4tb-inventory-v106-subject.json` is 2108 bytes, sha256 `a53cb8a6f565d0bddc5bde149a4018ac38f8ec75851f109582a6b2285a05c11b`. Inventory v106 is 362790 bytes, sha256 `82edcbd6fd65f636fc44f0987f24836de4bd1bb104fc5c3673f2a0cda7117dcd`, parent v105 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08` (359222 bytes). Successor record is 20201 bytes, sha256 `a178d9d31c9dc37571038c22aae84e317960a62e802a2e43b8be5d4280f8e180`. `~/Library/Application Support/OpenSIP` is absent.

## RF-1

`capped_read` is the byte allowance for every exact reread in the publication protocol, and it is below the charge `read_bounded_accounted` makes for a file whose length is the cap. `decode` admits a capsule up to the trust record parser's 131072-byte cap before any effect, and the confirmation then rereads that exact length. For a full read of an exact-length file the charged bytes are the platform's `read_bounded_cost` growth sum. `capped_read` allows `2 * len + 8192`. That is short on these lengths:

- 16384 through 20480, short by 4097 bytes down to 1
- 32768 through 53248, short by 20481 bytes down to 1
- 65536 through 118784, short by 53249 bytes down to 1
- 131072, short by 118785 bytes

`publish` carves the confirmation as its own `prepaid` allowance after `publish_private_file` has already renamed `state.v1`. Unused write allowance is not returned to that carve. The confirmation spends one judged sample and the reopen, then the reread. The bytes still in the allowance are one judged sample plus `capped_read`. The reread is short by the amounts above, so either the reread or the second sample fails closed with `ReservedPostcheck`. A larger outer ledger does not pay it: the carve is the estimate. `publish` then returns the budget row, and the owner is left on the predecessor, while the pointer already names the new capsule.

The same formula is what `file_cost` reserves for an existing content-addressed record. That read shares the writes allowance, which also holds the unspent read term of every sibling that took the create path, so a lone equal record can fail where a record beside new siblings still fits. The confirmation has no such sibling term.

Required: reserve the platform's `read_bounded_cost(len, attempts)` for both rereads, with the attempt bound the read session already uses (one edge per growth, the EOF read, and the four spare attempts). The reservation has to cover the confirmation that runs after the rename, so a lawful capsule inside the 131072-byte parser cap completes when the ledger can pay that cost, and a short ledger still fails before the first effect.

## What holds

`check_accepted_by` checks an in-chain `accepted.by` in place and requires an accepted `role-event` of that role. An event outside the chain is one `Budget::load_at` on `Events`, at most `MAX_ACCEPTED_BY_READS` (6). It must be an accepted role event of that role, in this store, at the reference's sequence, and lower than the current descriptor's first listed event. An empty event list uses `eventHead.sequence + 1`, or 1 when the head is null, so the event is no higher than `eventHead`. `previous` and `history` are not walked. A missing, foreign, refused, or non-role event is the incomplete row. A ledger limit is the budget row.

Checks 1 and 2 run on every admission and only for `kind == s4-evaluation`. A retained before-clock compares all five floors, an evaluated before-clock compares F and L, and an unevaluated before-clock compares nothing. F is compared with `observation.wall` through `Floors::below` on a one-field floor. The refusal is `TrustRow::Rollback` (`CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`).

`RetainedCurrentTrust::bind` decodes the supplied bytes, opens `trust/stores/S` through I, and rechecks `state.v1` with `observe_private_file`. A sample mismatch is `RequiredFilesChanged`. `fenced_first_read` rechecks the fence and the owner, admits the retained capsule, applies check 3 against `owner.prior`, and publishes before the view is returned when `needs_write` is set. Check 3 pushes a predecessor's floors only when `Floors::of_clock` is not the default, so an unevaluated P0 adds nothing. Report-only, a time refusal, and a missing floor write publish nothing.

`build_floor_publication` writes the before image, the `S4EvaluationInputV2` from `proposed_time_input::assemble`, the `TrustAdmissionInputV1` (`continue`, `installed-component`, the running core closure), the `host-trust-admission` operation, the clock-write event, the descriptor under `trust/publications/by-predecessor/<sha256(before)>`, and the successor capsule. In the capsule, F becomes tEval, the anchor is replaced when S4 rewrote it, and L and `clock.timeEvidence` change only when L advances. Revision, `previous`, `eventHead`, and `publication` advance with that write. `successor_record_bindings::bind` and `current_record_bindings::bind` run on those bytes before `publish`.

`publish` rechecks the fence and the owner, reserves writes and the confirmation in one `effect` before the first dependency, creates only `publications/by-predecessor` and its bucket, probes absence before an exclusive create, admits a present private file only when the capped reread equals the bytes, and replaces `state.v1` last through `journal_store`'s re-export of `carrier_floor::publish_private_file`. The owner advances from the confirming reread and its post-rename sample. `ConfirmedCurrent.predecessor` is the sample reconfirmed before that effect. Nothing in the module retries or deletes. A `state.v1.<32 hex>` temporary left by the file protocol is not adopted. The census names `trust/stores/S/state.v1` and does not scan the store directory.

`DurableInstallation::advance_current` is the only change of the retained `state.v1` sample. It requires the same relative path, a decoded `(S, G, K)` equal to the endpoint, and a retained sample equal to `confirmed.predecessor()`. `advance_registry` still moves only `project-registry.v2`. The two required files are disjoint. Both methods sit side by side on `DurableInstallation`.

## Judgment calls

1. Accepted. The operation is `host-trust-admission` with `TrustAdmissionInputV1 { purpose: continue, surface: installed-component, closure: the running core closure }`. The action is already a closed `OperationInputV1` string. `current_record_bindings::bind` reaches `trust_input_bindings::descriptor`, and the same-store shell stops at the operation input, so this clock-write publication carries no role event and does not enter the install/continue role-event contract.
2. Accepted. `journal_store.rs` re-exports `carrier_floor::publish_private_file` under `cfg(target_os = "macos")`. The pointer and the carrier floor share that protocol. The leftover temporary is not deleted or adopted.
3. Accepted. `proposed_time_input::assemble` is the single producer. `prepare` calls it. Authority is `heads.root.admission`, `beforeClock` is the capsule clock, `beforeImage` is the owner's record reference, and `source` is `ordinary` with the closure the evaluation used.
4. Accepted. The event's `timeEvidence` is `{kind: kept}` and the capsule's evidence is left in place, unless `last_write` is set. Then the event evidence is `{kind: new, proof: the evaluation}` and the capsule's evidence is that evaluation reference. `writes` lists `anchor` when the anchor is rewritten, `evalHighWater` always, and `lastAccepted` when L advances.
5. Accepted. `needs_write` is false for report-only, a refusal, or no floor write. Otherwise it is true when stored F is absent or tEval exceeds it, when L advances, or when `anchor_write` is set and the stored anchor differs from the observation. S4's `evaluation` is `floor.max(wall).max(admitted)`, so a write sets F to a value at least the stored F. A confirming admission on the same sample writes nothing.
6. Accepted. Both binders run in `build_floor_publication` on the bytes that will be written, charged through `Budget::borrowed`, and `publish` is called only after they return.
7. Accepted. `may_create` is true only at and below `trust/publications/by-predecessor`. `write_dependency` observes absence first. A present private file is admitted when its bytes match and refused as incomplete when they differ or the file is not a private regular file. Any other missing parent is incomplete.
8. Accepted. `TrustRow::Rollback` and `TrustRow::RequiredFilesChanged` are both `CONFIG.CUSTODY_REFUSED`, subjects `trust-rollback` and `required-files-changed`.
9. Accepted. `CurrentStore.raw` keeps the gate's one read. `current_trust` lends those bytes and the `RequiredFile`. Only `advance_current` replaces them, and only from the reconfirmed predecessor. `ConfirmedCurrent` is a single slot, so a hold with two publications advances the gate after each one, in order. The gate test covers one publication, the second-advance refusal, and an unchanged registry sample.
10. Accepted. `fenced_first_read` and `publish` take `&dyn HeldFence`. The owner and `publish` leave the module only under `cfg(all(test, macos))`. `ConfirmedCurrent` is crate-visible so the gate can apply it. No adapter over `DurableInstallation` is built here.
11. Required finding. The one-effect reservation, the create path and the existing path both counted, and `prepaid` failing closed are the right shape. The capped-reread term is not an upper bound. See RF-1.
12. Accepted. An in-chain `accepted.by` must be an accepted `role-event` of that role. The out-of-chain path checks the same shape.
13. Accepted. v106 carries all 785 v105 rows by value, including the three descriptions the request defers to the D1 description-only successor.

## Inventory v106

v106 adds `crates/security/src/trust/floor_publication.rs` (service) and `floor_publication_tests.rs` (test) in path order, 787 files. Packages, pending decisions, and every inherited file row are unchanged. The standing text names this unit. The sixteen description overrides stay bound by path to the v105 rows. The rebase keeps X2c's `installation_directory`, `home_spelling`, `uid`, and `advance_registry` beside `current_trust` and `advance_current`.

## Replay

`cargo test --locked --offline -p opensip-security --lib` with the floor-publication, current-trust-admission, accepted-store-fixture, and `a_confirmed_trust_publication_is_the_only_advance_of_the_state_v1_owner` filters: 39 passed, 0 failed (12 floor-publication, 19 current-trust admission, 7 accepted-store fixture, 1 gate advance). `verify_scratch`: passed, 71 inventory successors, 72 contract successors, 16 inheritance rows, v106 selected. `verify_projection`: 16 rows, 83 corruptions refused. `check_package_edges --lane host` against v106 passed. `rustfmt --check` on the touched files reports wrap diffs; the parent revisions of the edited files report the same class of diff, so formatting is not a finding. The workspace suite and workspace clippy were not replayed. The X4T-0 fixture used by the passing tests sits outside the lengths in RF-1.
