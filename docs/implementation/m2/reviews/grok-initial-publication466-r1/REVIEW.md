# Review: initial publication 466 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Source review of the in-memory P0 trust publication and inventory 66. No repository edits.

Product `4e0cb7b`. `git status` is the three modified trust files and the new `initial_publication.rs`. All four hashes match.

## Verdict

**ACCEPT-UNIT.** No required findings. Inventory 66 is accepted as a layout candidate.

## Answers

1. **The six records follow the closed shapes and the P0 rules the existing verifiers enforce.** `build` admits each document with `shapes::admit` before it is kept. The marker is schema 1 and the 32-hex store id. Creation input, operation, and event use store generation 0, schema K, sequence 1, and a null previous. The descriptor’s `afterProjection` is the capsule body without `publication`, with one event whose `roleChange` is null, and with `nativeBefore` and `previousCapsule` null. The capsule is revision 1, clock phase `unevaluated`, all six roles `ST-UNBOOTSTRAPPED`, and its publication pin is the descriptor’s sha256 and length. The inputs275 `original-0` row names the same marker (`33ba744a…`, 72 bytes), creation input (`b746c0f7…`, 485), operation (`815b4939…`, 403), and event (`2f8e8e45…`, 315). The passing test checks those four hashes, and an independent hash of the marker JSON matches `33ba744a…`.

2. **The check is the existing verifiers, not a stub.** `verify` parses the built documents and runs `trust_input_bindings::creation`, `capsule_consistency` with no predecessor, and `publication_events::bind_events` from blank roles and a null head. `creation` loads the marker and creation input from the in-memory store and requires the shared store binding, sequence 1, the event head, and the P0 capsule shape. `capsule_consistency` recomputes the descriptor reference and requires that pin, and it requires `afterProjection` to be the capsule with `publication` removed. `bind_events` loads the event and requires the creation chain and a null role change. The swap test builds a second publication at state schema 2, replaces the capsule and then the descriptor, and both calls return an error.

3. **Lengths are refused before any charge.** `check_lengths` returns `Input` with `used` still zero. `BUILD_COST` (32 objects, 32 edges, 64KiB) is charged before `assemble`. The verifier loads go through `Budget::borrowed` on that same scope: `account` calls `work.charge`, and `retain` charges the retained copy before its `Arc`. A ledger one byte short of `BUILD_COST` fails closed. 64KiB is a ceiling over the six small records; the owner allows that overcount.

4. **Paths are the reader locators.** Immutable files use `locator_components`, which returns `Locator::new(...).parents` plus `leaf`, the same `Locator` `capture_with` walks. Records are `trust/records/<sha256>`. The event is `trust/stores/S/events/1-<sha256>`. The initial publication is `trust/publications/initial/S/<sha256>`. `state.v1` is `current_parents(S)` plus `CURRENT_LEAF`, and `capture_head_with` now walks those same helpers (`trust`, `stores`, S, then `state.v1`).

5. **This produces records, not authority and not the missing inputs.** `Inputs` is caller-supplied. The module does not mint S, K, the core closure, the platform, the staging nonce, or the invocation ids. It does not open a path or write a file. `InitialPublication` is `pub(super)` inside `trust::root_payload` and is not re-exported. The type has no create or permit method.

## Inventory 66

One added file, `crates/security/src/trust/initial_publication.rs`, at files index 281, role `builder`. 713 inherited rows are equal by value. `package.json` moves 510 → 511 and `schemas/sources/imported-v1.schema.json` moves 577 → 578. Packages and pending decisions match v65. The projection helper is byte-identical to the v64 and v65 helper (`bb82ef05…`, 2917 bytes). Against product `design-lock.json` (`512270a6…`, the anchor hash) it reports PASS and 28 corruptions refused.

## Replay

Rust is `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

- `rustfmt --edition 2024 --check` on the four pinned `.rs` paths: exit 0.
- `cargo test -p opensip-security --lib -- initial_publication native_current native_record_capture trust_input_bindings`: 37 passed, including all 6 `initial_publication` tests.
- `cargo clippy --workspace --all-targets -- -D warnings`: exit 0.
- `verify_projection.py` for inventory 66: PASS, 28 corruptions refused.

Do not commit.
