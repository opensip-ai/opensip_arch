# D2 r1 — contract successor

ACCEPT-DESIGN-UNIT. Four `passageSupersessions` on inventory v122, at product `96dd1145b3da207e83479dc0f50d9d62cb1b7e04`. `passageOverrides` is empty. There is no inventory successor.

## Pins

All seven `hashes.txt` rows match. The subject manifest is `docs/implementation/m2/description-batch-d2-subject.json`, 1034 bytes, sha256 `5eb1e332609874db0f06f5b9518c4f46728574fbd2e9ad7724590d10a3fb2260`. `successor.json` is 14785 bytes, sha256 `21e1ce5141834b8df62f73ffd84b59ccbf9262c1ed58828112929315ed6d048a`.

`evidence/build_d2.py` was not executed against the architecture tree. A read-only reconstruction, with `Path.write_text` captured in memory, produced those same two byte strings. The architecture files were left as pinned.

## Record

`successor.json` is schemaVersion 1. Its one parent is `repository-file-inventory.v122.json`, 485705 bytes, sha256 `69cf90db0ade09fc0f9536b3ef293d7de6aff68c7d3ae9a2aabfab4f6c244c7a`, the inventory the product lock selects. The four supersessions, in inventory order:

| v122 | File | `supersedes` |
|---|---|---|
| `/files/273/description` | `crates/identity/src/store_lineage.rs` | 468a `successor.json` `dae42833b0f6a204836762b273a42e36433b968a5edb81018b0825277ae17d5c` (15663 bytes), v74 `90ccda7e0b199ad4705661e5303581f4b6b4ab220b560a8ec93d9809dd982279`, `/files/158/description` |
| `/files/372/description` | `crates/security/src/custody/installation_session.rs` | 461b `successor.json` `2c8a4de79e156b0f0c47e579c2121adae07f804a505e3d19d3bb2b787596fad6` (11909), v80 `838a7f4072b408e8c4011249c89e0974d38616031cda110267c92ab762d0d1e7`, `/files/247/description` |
| `/files/388/description` | `crates/security/src/custody/read_premise.rs` | same 461b record and v80 parent, `/files/250/description` |
| `/files/398/description` | `crates/security/src/initial_installation.rs` | same 468a record and v74 parent, `/files/242/description` |

Each `before` equals that row's one `inventoryPassageInheritance` `after`, and equals the named root override's `after`. `descriptions.json` and `successor.json` carry the same `before` and `after` text. Every `after` is non-empty, different from `before`, and contains no newline.

D1's 39 paths are disjoint from these four. Each of the four still has exactly one inheritance entry, from 468a or 461b, and the lock has no earlier supersession of that path. The link each entry names is that root override. Law VD1 item 6 names this same quartet: `read_premise.rs` and `installation_session.rs` name 461b; `store_lineage.rs` and `initial_installation.rs` name 468a.

The supersessions sit on the selected inventory, so verify_design checks them and leaves them unprojected. Inheritance stays at 55 rows.

## Scratch verify

`python3.14 -I -B evidence/verify_scratch.py` ran the product's verify_design over the real lock with D2 appended and the review and assent held in memory. It passed: 74 contract successors, v122 still selected, `inventoryPassageSupersessions` 4, 55 inheritance rows unchanged, each `before` equal to that row's current meaning, `passageOverrides` empty, 40 generation sources, 48 admission sources, and 15 aliases. `executedGeneratorCode` and `executedRuntimeCode` are false. Nothing was written.

## The four texts

Sentence split on `. ` : `store_lineage.rs` and `initial_installation.rs` keep every old sentence. `installation_session.rs` drops only `Library only: no CLI command is wired.` `read_premise.rs` drops that same sentence, and edits `The receipt is private …` to `The read receipt is private …` with the remainder of that sentence kept word for word.

Checked against the product at `96dd114`:

- `SuppliedChain::into_nodes` (`store_lineage.rs` 194) returns the chain. The write gate's one read takes it at `installation_admission.rs` 1449. The observation session's member reads take it at `installation_session.rs` 755.
- The session latches at `observe_with` (303) so one observation is per session. Receipt rechecks run at 357 and again at 392. The core finding is `pair.core_closure() != core` at 664, from `receipt.selected_core().0` (305). The current record is read once under `CURRENT_STATE_CAP` (678–690); over-cap, decode, and `current_matches` are `IncompleteRefusal::CurrentStore`. `lineage_bound` (395–404) and `lineage_limit` (408–413) make the session limit the budget row and a generation-bound stop the `Chain` finding (759–762). `endpoint` (454–463) keeps the pair, the marker, the nodes, and the current record when findings and failure are empty. `retain` (277–290) requires `complete()` and keeps the ledger, the receipt, and the observation.
- `PlatformReceipt<Read>` qualification (135–136) is `ReadPremiseQualification`. `PlatformReceipt<Write>` qualification (161–162) is `DurableBarrierQualification`. `bootstrap_source` (168) is on Write; its only production caller is `ordinary_writer.rs` 332, inside `gate_step`, for the monitor's first read. `charge` (176), `charge_guarded` (191), `reserve_end_path_settlement` (209), and `settle_end_path` (218) are the write receipt's lendings. `selected_core` (117–118) is on both purposes. A foreign actor, core, or platform is `T::Invariant` (350–354). `produce_write_platform` (302) is called from production only at `ordinary_writer.rs` 494.
- `opensip doctor` is `Request::Doctor` (`apps/cli/src/bootstrap.rs` 34), `doctor()` (72–77) calls `host.doctor`, `doctor_ingress.rs` 39 calls `observe_installation_for_doctor`, and `installation_doctor.rs` 57 calls `produce_read_platform`. That is the one wired CLI path, and it uses the read receipt.
- `InitialInstallationAttempt::begin` (98–100) is one attempt per process, refused on a second call even after drop. `recheck_actor_in` (284) rechecks the actor on a borrowed scope. `recheck_storage_in` (299) rebuilds I through `installation_target` (512–517) and re-classifies storage; `recheck_handoff_storage` (660) refuses a foreign actor or handoff and then calls it. `reserve_end_path_settlement` (170–177) and `settle_end_path` (183–188) are the only production callers of `WorkLedger::reserve_settlement` and `WorkLedger::settle`. `ordinary_writer.rs`'s `settle` is that writer's own method.

## Judgment calls

1. **The edited sentence.** Accept. With `Read` and `Write`, "the receipt" did not say which purpose holds `ReadPremiseQualification`. The sentence now says "The read receipt", and that lending is `qualification` on `PlatformReceipt<Read>` only. Every other old sentence of each text is kept word for word, apart from the two "Library only" sentences in call 2.

2. **"Library only" is replaced.** Accept. Those sentences in `read_premise.rs` and `installation_session.rs` are false since X10a wired `opensip doctor`. The replacement names doctor as the one wired CLI path. `read_premise.rs` also says no CLI command reaches a write receipt, which matches the single production caller of `produce_write_platform`.

3. **The creator sentences stay, and the attempt also stands behind the receipts.** Accept. "the initial creator's pre-installation attempt" and "the only work ledger for the whole act" remain true of the creator. The new sentence is this module's one attempt type: `begin` is once per process, and the read and write receipts are `InitialInstallationAttempt` values produced by that `begin`. The closing sentence, that this module opens no installation path, creates nothing, and does not enable the creator, is kept and still true. Settlement spends a reserve; it does not open an installation path.

4. **The other 12 of the original 16.** They may wait. None of their effective sentences is now false. The twelve are `apps/cli/src/bootstrap.rs`, `apps/report/package.json`, `package.json`, `crates/host/src/installation_lineage.rs`, `crates/security/src/custody/installation_fence.rs`, `crates/security/src/custody/installation_publication_tests.rs`, `crates/security/src/installation_observation.rs`, `crates/security/src/private_access.rs`, `crates/security/src/trust/native_census.rs`, `crates/security/src/trust/native_read_session.rs`, `crates/security/src/trust/native_record_capture.rs`, and `schemas/sources/imported-v1.schema.json`. Spot checks at `96dd114`: root `package.json` engines are Node 24.16.0 and npm 11.13.0; `apps/report/package.json` pins TypeScript 6.0.3 and esbuild 0.28.2, and `tsconfig.json` lib includes DOM; `BARRIER_SLOTS` is asserted 44; `InstallationReadFence` still documents no selected store and its public API is acquire, recheck, and capture; supplied and native fence acquires used from production files sit in test fixtures; the trust readers borrow a held-fence view or `InstallationReadFence`; private-file and private-directory helpers still use modes 0600 and 0700; `import_joins.rs` still owns retained correspondence and parameter selection. `bootstrap.rs` omits doctor, and `crates/host/src/imports.rs` remains a proposed inventory path. Those are incomplete assignments, and no sentence of the twelve is false. They do not join D2.

5. **After selection.** Accept the obligation as stated. The next inventory successor carries these four rows by value and folds each supersession into that row's one inheritance entry: `before` stays the raw text, and `after` becomes D2's `after`. The projection helper's count stays 55. `commit-facade-x3d2-inventory-v122/verify_projection.py` reads `inventoryPassageInheritance` and `passageOverrides` (lines 28–31) and does not read `passageSupersessions`, so the next helper has to read them. If another inventory is selected before D2, `build_d2.py` rebuilds by path and that rebuild needs a new review.

## Disclosure

Source comments still say "Library only" at `read_premise.rs` 19, `installation_doctor.rs` 11, and `ordinary_writer.rs` 13, and `read_premise.rs` 6–7 still says "The receipt is private". D2 updates inventory descriptions. Those comments are outside this successor.

`~/Library/Application Support/OpenSIP` is absent. No product cargo.
