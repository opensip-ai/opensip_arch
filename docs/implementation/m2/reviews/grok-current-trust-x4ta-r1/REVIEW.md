# Review: current-trust admission X4T-a r1

Verdict: REQUIRED-FINDINGS. Inventory v90: REQUIRED-FINDINGS.

Worktree `/Users/sb/code/opensip-ai/opensip-x4ta` at `5b5f04cf3132d4aa91ced618d4b40544f2aaf2f5`. `product.diff` is `git diff` of the eight product paths: 56800 bytes, sha256 `12755083a01eab0b1cf6fb8ee7222445b23faf57c1197535c4f400c7ae630bf9`. The nineteen hashes.txt pins match. The real OpenSIP support directory is absent. Subject manifest sha256 `e0dcf982c1495fb1d03b5792cc1854d071dbc1f8711a783b193c8d331d6101ee`.

Law is accepted X4T r5. This unit is items 1–6 and 8–11. Time is report-only. Item 7, the floor write-ahead, is X4T-b.

Replay, Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib -- current_trust_admission accepted_store_fixture`, `CARGO_TARGET_DIR` under this review directory, then removed: 21 passed, 0 failed. Fourteen are the current-trust admission tests and seven are the accepted-store fixture tests. Workspace suite, clippy, fmt, `check_package_edges`, and verify_scratch were not replayed. Passing tests leave the rows below open.

## What matches

`admit_current_trust` takes the supplied capsule and loads the descriptor, then `current_record_bindings::bind` and `check_accepted_by`. `admit_native` calls `capture_p2`, runs the same admission, and `recheck`s `state.v1`. The fenced first read does not recapture `state.v1`. `accepted.by` must name an event `bind_trace` loaded for that role. A miss is the incomplete row. History is left unwalked.

X4T-a opens the root admission, the catalog and revocation bodies, envelopes and admissions, `history`, and `timeEvidence` with `Budget::load` in the collection the typed reference names. Bodies and envelopes are `Objects`. The catalog envelope is reverified, and `verify_revocation` runs on the loaded revocation bytes. The root chain is `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }`. `policy::merge(Source::Missing, …)` supplies the epoch digest through `Effective::digest()`. S4 runs on the fenced read only, through `evaluate_retained_ordinary`. `TimeRange` is `PAYLOAD-NOT-ADMISSIBLE` subject `time`. A reread carries no time. This unit writes nothing. `standing(core, index, component)` is the join for the three roles once Recovery has been passed (RF-5). The view is private. Nothing here is wired to a session.

## Judgment calls

1. The three envelope rows in the generator's payload closure are acceptable. The inventory owner binds each manifest envelope slot to its stored blob. The production path does not reach the `cfg(test)` constructor.
2. The source pin may admit `current_trust_admission_tests.rs` after checking that its `include!` sits under `#[cfg(test)] mod tests`. The inherited description of that pin is the inventory finding below.
3. Unit checks are an acceptable substitute for the documents the generator cannot mint: a 33-event descriptor through `check_event_bound`, `ChainError::Limit` through `chain_row`, a short object ledger through `Budget::new`, and the existing envelope, quorum, and chain-error arms for a bad signature, a wrong quorum, and an expired final root. Those arms already name `PAYLOAD-NOT-ADMISSIBLE` and the S5 `ROOT.*` rows. The positive revoked component is RF-4. The full-size cost pin is RF-2.
4. Adding the 16 MiB chain allowance to the 40 MiB closure total is RF-2.
5. An empty set of keys revoked before this list is acceptable. Item 11 forbids walking history to fill it. That empty set is the prior-list set only. The current list's `keyId`s are RF-4.
6. Role states from the capsule, with S4 expiry carried on `TimeAdmission` and left off the role tokens, are acceptable. An `Expired` or `StaleRevocation` index is `ExistingOnly`. Clock expiry is never an S5 row.
7. Classifying nested owner errors by Debug text is RF-3.
8. `TimeRange` as `PAYLOAD-NOT-ADMISSIBLE` subject `time` is acceptable. `ContinuityExpectedWall` is a calendar failure of the expected wall; `InSession` already maps to `CLOCK-EXCURSION-FORWARD` subject `in-session`. A native digest or absence as the incomplete row, and I/O or the fence as host I/O, are acceptable. The Recovery subject is RF-5.
9. Leaving the view unwired is acceptable. Consumption is X4a's.

## RF-1

`pre_acceptance` is true when `heads` is null or `history` is null. `admit_current_trust` returns `TRUST.NO_ADMITTED_TIME_CONTEXT` before any read in that case, and `preamble` returns the same row again. Item 1's P0 shape is `heads` and `history` both null and every role `ST-UNBOOTSTRAPPED`. `check_capsule_projection` already requires that conjunction for a non-retained phase, and that a pre-acceptance capsule has no accepted role. Item 10 uses F absent for nothing else. A retained capsule missing only `history`, or a pre-acceptance capsule with an accepted role, takes F absent today and never reaches that projection.

Required: F absent only for that P0 shape. The early return before any read may stay for that exact shape. Any other null head, null history, or accepted role on a pre-acceptance capsule is the incomplete row.

## RF-2

The closure check is `b.counters().2 - start_bytes > 40 MiB + 16 MiB`, after `authenticate` has retained the chain on the same counter. `ChainBudget` already refuses a chain over 16 links or 16 MiB. A closure of 50 MiB with a small chain is under 56 MiB and is admitted. `budget_row` maps `Error::Cap` to the budget row. `retain` returns `Cap` when the bytes are empty or longer than the owners' 4 MiB cap. Item 10 puts oversize with the incomplete row. `ObjectLimit`, `ByteLimit`, `EdgeLimit`, and a closed scope are the view ceiling and stay the budget row.

Item 11's acceptance condition is a pin of the real cost of a view whose closure is at its 40 MiB total with 32 events and whose chain is at its 16-link, 16 MiB budget, and that this cost is at most `TRUST_VIEW_COST`. The test pins the six-role store at 23 objects, 44 edges, and 35,371 bytes. `bounds_refuse_on_the_budget_row` covers the 33-event list, `ChainError::Limit`, and an 8-object ledger.

Required: refuse when the closure's retained bytes, excluding the chain's own `ChainBudget` accounting, exceed 40 MiB. `Cap` takes the incomplete row. `ObjectLimit`, `ByteLimit`, `EdgeLimit`, and `Closed` stay the budget row. Pin the charged cost of a view at the 40 MiB closure with 32 events and a 16-link, 16 MiB chain, and that this cost is at most `TRUST_VIEW_COST`. The six-role pin may remain as the ordinary-store measurement.

## RF-3

`nested_input` scans the Debug text of `ordinary_roots::Error::Shared` and `ScopeError::Inventory` for the last `Input(`, then prefix-matches `ObjectLimit`, `ByteLimit`, `EdgeLimit`, `Closed`, `Cap)`, `Capture)`, `Missing)`, `Digest)`, and `Reference)`. A cause the text misses becomes `PAYLOAD-NOT-ADMISSIBLE`. `trust_ordinary_quorums::Error`, `trust_ordinary_metadata::Error`, and `retained_metadata_index::Error` already expose those causes as typed variants. A budget or missing cause published as `PAYLOAD-NOT-ADMISSIBLE` is request-rejected, where item 10's budget row is operational-failed.

Required: match the typed `Input` and nested causes. `ObjectLimit`, `ByteLimit`, `EdgeLimit`, and `Closed` are the budget row. `Cap`, `Capture`, `Missing`, `Digest`, and `Reference` are the incomplete row. A failed document or quorum stays `PAYLOAD-NOT-ADMISSIBLE`.

## RF-4

Item 4 refuses a revoked component in the closure: the running core, the release, the signing keys, and the namespace's catalog snapshot. The loaded list's closed subject kinds are `keyId`, `namespace`, `release`, and `catalogSnapshot`. `observe_revocation` already matches those kinds to closure subjects. `admit_bound` compares an optional `core_closure` string to subjects only, ignores `subjectKind`, and skips the check when the option is absent. `a_revoked_running_core_closure_refuses` supplies `closure2:cccc` and admits, because the fixture list revokes nothing. The catalog envelope is reverified with `filter_envelope_revoked` over an empty set, and `prepare_authenticated_times` receives an empty revoked-key set, both before the current list's `keyId`s exist.

Required: after `verify_revocation`, an entry whose `subjectKind` and subject name the admitted closure's release, signing key, namespace, or catalog snapshot refuses as `CONTINUE-CORE-NOT-TRUSTED`, subject that component. Reverify the other envelopes this unit checks with those current `keyId`s excluded. The set of keys revoked before this list stays empty. Item 2's read set has no embedded 463 revocation document. `InitialCore` already refuses a release entry that names the closure.

## RF-5

`authenticate` returns `Continuation("recovery")` when any of the six roles is `State::Recovery`, before `standing()`. The subject is the single word `recovery`. `continuation` takes core, index, and component. A Recovery bundle, profile, or repair is outside that join, and item 1 rejects a stricter join.

Required: Recovery goes through `standing()`, with subjects `core:recovery`, `index:recovery`, and `component:recovery`. A Recovery bundle, profile, or repair follows the role machine.

## Inventory v90

Parent v87 is 324832 bytes, sha256 `f4240a79718874c8d8e323750b918b11a86ec0b22f7e050f30b53f2472a8d209`, matching the successor parent and the file on disk. v90 is 327561 bytes, sha256 `a75b551f74c92a90cbfad70f28a5ecb95861d6f8655055f22a0a2e8f9f932c3d`. Against v87 the file rows add exactly `current_trust_admission.rs` and `current_trust_admission_tests.rs`. No row is removed. Every inherited file row is equal by value. Packages and pending decisions are unchanged. Standing differs, which a new unit requires. Successor `current-trust-inventory-v90/successor.json` is 20194 bytes, sha256 `891b6dc126c52190a4e553df3462a50a7403f9d0fa8082b4a1d0a08e007cbd2a`.

The v90 description of `accepted_store_fixture_tests.rs` says the source pin shows the constructor is named by no other source file. `current_trust_admission_tests.rs` names `accepted_store_fixture`, and the pin admits that file after the `cfg(test)` check in judgment 2. That sentence is false. Carrying the row by value leaves it false. Required: the description says the source pin admits that `cfg(test)` test file. The two new descriptions describe this unit's behavior, including the F-absent return the code performs, and stay as written.
