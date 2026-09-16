# Asset-channel selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Scoped follow-up of the archived asset-channel addendum. Not a pristine-blind claim. Archived 185-file `review.md`/`review.json`/`asset-channel-addendum.md` and frozen/live product were not edited. This does **not** complete whole M1 on staged bytes and does **not** integrate the unit into the live design lock.

Design subject `docs/implementation/m1/asset-channel-selection-v1-subject.json` SHA-256 `f35eea25dbc210bb962d72f0ea81e6d0bae9da4ffb559ac577d5e54c14f6943b` (22 files). Implementation subject `docs/implementation/m1/trials/asset-channel-01/subject.json` SHA-256 `51b3ae02757f9a094c48c92b20202f845cf6a6052df641dd104c0d7825e13699` (200 files). Archive `subject.tar.gz` SHA-256 `312a6be20b538c145c1778de9137856952819db478e2910be61bf2b956174e36`. All pins matched.

## Custody

Successor parents are the last prior contract unit (`rust-provider-workspace-selection-v1/successor.json`) and inventory v10; both pins match. `passageOverrides` is empty. Materialization map names only the two inventory-preexisting owners: `crates/reporting/src/assets.rs` and `crates/reporting/tests/projection_tests.rs`. Product delta versus the 185-file tree is exactly those: one content change and one added named test file. Host and rust-provider `Cargo.lock` bytes are unchanged. Staged `design-lock.json` is unchanged (live integration still required).

## What the code actually does

Private `HostAssetPinV1` and `CompiledBuildSelection` live only in `assets.rs`. They are not `pub`. `lib.rs` still exports only `development_metadata` / renderers. There is no public pin constructor, no env/config input, no runtime asset open.

One `BUILD_CHANNEL = Development`. Production `BUILD_SELECTION = CompiledBuildSelection::new(BUILD_CHANNEL, None)` — explicit **no bundle**, no invented path/digest. `development_metadata` reads `BUILD_SELECTION.channel()`, which for `None` is that same compiled channel.

`CompiledBuildSelection::new` is `const fn`. When `Some(pin)` is supplied it checks private shape (schemaVersion 1, POSIX relative paths, manifest-under-root prefix + `/`, 64 lowercase hex digest, length in `[1, 9007199254740990]`) and **channel equality** with the compiled metadata channel. Failure is `assert!` → const-eval **E0080** with a specific guard string. Comments in-source state that assembly must still prove real manifest/member bytes and that the later renderer rechecks bounded reads.

`projection_tests.rs` `include!`s the **production** `src/assets.rs` into a disposable package (not a stub). A labelled development fixture (actual `fixture.js` / `manifest.json` bytes) is used as `Some(TEST_PIN)`:

| Case | Result (reproduced) |
|---|---|
| matching real fixture + `BUILD_CHANNEL` | compiles |
| pin `Release` vs compiled Development | E0080 `asset pin build channel differs from compiled metadata` |
| manifest not under root | E0080 `manifest must be under asset root` |
| zero length | E0080 `invalid manifest byte length` |
| invalid raw digest | E0080 `invalid raw manifest digest` |

First disposable `cargo check` creates a local lock; later cases `--locked` and assert lock bytes unchanged. Production locks are not that lock.

Independent hashes: fixture script 79 bytes SHA-256 `2669f5ae…1d49`; manifest 266 bytes `d8870ab5…99ef`; selected `report-v1.schema.json` `bbb5ca92…cc97`. Private JSON Schema shape of the required pin fields and of the manifest validate. Manifest does not list itself; the one asset path is under `fixture-assets`. Extra keys on `fixture-pin.json` (`standing`, `projectionSource`, `projectionSha256`) are test metadata stripped before schema validate.

## Does this discharge the M1 sentence?

Selected clause remains coverage v4 `/groups/commands/30/verification/method`:

> BuildMetadataV1.buildChannel and HostAssetPinV1.buildChannel derive from one compiled build selection; disagreement refuses at build time. crates/reporting/tests/projection_tests.rs owns the compiled producer/channel-agreement negatives

**`None` alone does not prove agreement.** The production constant is an honest non-selection. Agreement is the `new()` law, exercised by compiling `Some(pin)` through **that same function** on the production source: matching fixture passes; `Release` vs `Development` fails E0080. That is not a fake production pin and not a vacuous skip.

This matches the addendum’s allowed path: handwritten private type, one `BUILD_CHANNEL`, named negatives, no dummy digest in production.

Load-time open/read/digest, complete member inventory, HTML, and signed release are **not** done here and are **not** waived. They remain M4/M6 as in report-asset-binding `loadTimeValidation` / `buildTimeValidation` and `html_renderer` milestone.

**M1-clause-disposition:** compiled pin/channel admission **satisfied** for this unit. Assembly, custody, raw member digest, projection join, HTML, and release remain mandatory later.

## Independent execution

Adapted `run-checks.py` to the private copy (`m1-asset-channel-candidate-01` is not this tree). Python 3.14 metadata-reference-env; Cargo 1.95.

- Workspace `cargo test --locked --offline --all-targets`: **32** passed (including both projection tests; compile-probe ~17s).
- `clippy --locked --offline --all-targets -- -D warnings`: pass.
- `cargo fmt --all --check`: pass.

Additional private const probes (not in the named matrix) against production `assets.rs` also failed compile with E0080 and the intended guard: `.` root, `..` path, backslash, uppercase digest, `schema_version: 2`, oversize length, trailing-slash root.

No public authority escape: pin types stay crate-private; tests only `include!` them in an unpublished disposable package.

## requiredFindings

None.

## shouldFix

1. Named `projection_tests.rs` matrix does not itself fire schemaVersion / POSIX / uppercase / max-length guards. Constructor has them; extra probes passed. Expanding the named matrix would reduce reliance on out-of-band probes.
2. `evidence/run-checks.py` hardcodes another candidate path; reviewers must retarget it.

## Limits

Const admission does not read the filesystem or prove inventory completeness. Staged product lock is not updated. No whole-M1 or M6 claim. Root still must integrate privately/live before treating the 185-file tree as containing this unit.
