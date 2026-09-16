# CLI metadata correction review (review02)

**Verdict: ACCEPT-UNIT.** This accepts the concrete CLI metadata unit on these frozen bytes and nothing else. It does not accept the generator or adapter01, integration, design-lock binding, the HostAssetPinV1 channel check, build or release qualification, or M1. The generator stays partial, the 45-command goal is unchanged, and the CLI advertises only its 3 implemented commands.

- **Subject:** `/tmp/opensip-implementation/m1-cli-metadata-subject-02`
- **Manifest:** sha256 `9180e2a8a3abd5dd14934b5b735eb74646dea017960c8d11030049a07c0e4c44`
- **Pins:** checked before and after the review. 96 of 96 files match, with nothing extra or missing.

## What changed since subject-01
- **Changed:** `CLI-UNIT.md`, `startup_tests.rs` (one test added, the existing ones untouched), `crates/platform/src/lib.rs` and `crates/reporting/src/human_renderer.rs`.
- **Removed:** `crates/platform/src/entropy.rs` and `check-cli-metadata-reference.py`.
- **Added:** `broken-pipe-result.json`.
- **Unchanged:** the manifests, the lock, the host code, the JSON renderer and the generated contracts.

## How the review01 findings were resolved
- **RF-1: closed.** The 16-byte getrandom wrapper is unchanged and now lives in `crates/platform/src/lib.rs`, which is already in inventory v3. No file is outside the inventory, and neither the lock nor any manifest changed.
- **RF-2: closed.** Human failure output now prints these lines, then the diagnostic:
  - `Termination:`
  - `Error:`
  - `Detail:` and `Remedy:` for each error
  - `Request:`

  Successful help and version output ends with `Termination: success`. Completion scripts end with the comment `# Termination: success`. The "never omits termination-class" rule now holds everywhere, so the A-10 owner question no longer arises.

Earlier advisories:

| ID | Status | Note |
|---|---|---|
| A-01 | Disclosed | CLI-UNIT now documents the closed-stdout /dev/null behavior |
| A-02 | Open, non-blocking | No bootstrap-level entropy/collision failure test |
| A-03 | Open, separate | Build-lane backend cfg guard, platform dependency policy, uncached r-efi |
| A-04 | Open, non-blocking | Parser edge limits; no caller text is echoed in human output |
| A-05 | Open, non-blocking | Usage spelling differs from inventory4 |
| A-06 | Open, separate | `projection_tests.rs` and the HostAssetPin channel check |
| A-07 | Open, non-blocking | Don't reuse the process-only host for M2 |
| A-08 | Superseded | Reference checker removed; I re-ran the validation myself |
| A-09 | Open, non-blocking | Delivery-failure envelope drops `clientCorrelationId` |
| A-10 | Moot | No exemption needed now |

## New advisories (non-blocking)
- **B-01:** The new test checks the error codes but not the labels. Replacing `"Detail: {}\nRemedy: {}"` with `"{}{}"` still passed all 6 tests, and nothing checks the remedy text. The other 4 mutants were caught. Assert the labels, the remedy text and the line order for one refusal and one delivery failure.
- **B-02:** fish isn't installed on this machine. The fish script (a `complete` line plus a `#` comment) is valid syntax only by inspection.
- **B-03:** The platform code now sits in the public-API `lib.rs`. That's fine at 10 lines, and it can move later if platform grows.
- **B-04:** The human reason sentence now comes after the Request line. Order isn't owner-specified, so this is a note only.

## Independent checks I ran
- **Build and lint:** in a private copy with its own target directory, `cargo build`, `test` and `clippy -D warnings`, all `--locked --offline`, pass. `cargo fmt --check` exits 0. Tests: 6 startup, 2 authority, 1 metadata and 10 identity, all passing.
- **JSON unchanged:** 27 JSON cases (the 17 author reference cases plus 10 adversarial ones) and 3 read-only-stdout delivery cases produce output identical to the review01 binary once RequestIds are masked.
- **Schema:** those cases plus one broken-pipe case, 31 envelopes in all, are valid against the original envelope4 schema using the accepted ExactValidator adapter.
- **Human output:** I captured 14 cases, including both delivery failures on stderr. I put escape sequences in the help topic and correlation IDs, and none of them show up in the output.
- **Completion scripts:**
  - `bash -n` passes, and sourcing the script registers `complete -W 'completion help version' opensip`.
  - `zsh -n` passes. With `_opensip` on the fpath, `compinit` binds `_comps[opensip]` and autoloads `_arguments '1:command:(completion help version)'`. `#compdef` is still the first line.
- **Existing tests preserved:** the five earlier startup tests, including the `errors=[]` refusal test and the JSON delivery test, are unchanged and pass.
- **No side effects:** under a sandbox that blocks network, writes, and reads of the fixture directory, `/Users` and `/private/etc` (each block confirmed first), 7 cases give the same output as without it.
- **Mutation testing:** 4 of 5 renderer mutants were caught (B-01).

Probe outputs are in `work/probes/`, and the mutation results are in `work/mutants.txt` and `work/mut-*.log`.

## Limits
- Everything ran on macOS arm64 in a debug build. Nothing ran on Linux, and there was no release build or startup, size or memory measurement.
- fish wasn't run, and a CSPRNG failure couldn't be triggered in the binary.
- The sandbox evidence rests on those denial checks, not a syscall trace.
- No frozen, product or architecture files were edited, and nothing was committed or pushed. Everything I wrote is inside `m1-cli-metadata-review-02`.
