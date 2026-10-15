# B1-b: carriers, invocation mode and the environment check (M3-B unit B1-b)

**Product unit, r4; for Codex review (ACCEPT-UNIT).** r4 answers Codex round 3 (`codex-b1b-r3`), RF-01 (integration-test files under production inclusion); see "Round 4". Round 3 accepted round 2's RF-02.

Earlier, **(r3)** r3 answers Codex round 2 (`codex-b1b-r2`): its RF-01 (the pin's include confinement) and RF-02 (a zero-lookup count, and the refused-pack composition). See "Round 3" below. Round 1's RF-01 and RF-02 were accepted in round 2.

Earlier,  r2 answers Codex round 1 (`codex-b1b-r1`, REQUIRED-FINDINGS). Each finding's resolution is stated where it lands below and under "Round 2":
- **RF-01:** capture binds to the custody judgment's sample.
- **RF-02:** optional absence is observed under judged parents and rechecked against their original samples.
- **RF-03:** the exception pin resolves constants and finds test scope by brace matching, with negative controls.
- **RF-04:** the controls are completed.
- **NBO-01:** rustfmt is classified over every edited file.

r2 also shares one settlement between `capture_with` and `capture_optional` (`settle_capture`), so the audited `swallowed` count in `installation_read.rs` stays 1. The operability source check passes with no exception row added beyond r1's `stdio` row. This implements the accepted plan r3 (`config-discovery-b/b1-b/PLAN-r3.md`) and M3-B r5's item 9 list. Both were accepted together in `codex-b1b-plan-r3` and published at arch `b9893272`. The product base is `c0151bc` (B1-a code and inventory v188 bound).

## What it delivers

### Security: the analysis path's carriers (X2 r9 item 3a)

**Selection with retention (`project_admission.rs`).**
- `select` takes a `retain` flag. With `retain`, it returns the judged `opensip.json` descriptor from the directory that selected it. This applies to both the explicit path and the walk.
- `select_project_root` stays the legacy entry. It calls `select` with `retain = false` and is otherwise byte-for-byte the old selection: the same opens, charges and refusals, with the descriptor dropped where it always was.

**Carriers (`project_admission.rs`), after the chain walk, incarnation and marker:**
- **`opensip.json`:** captured from the retained descriptor. **(r2, RF-01)** Selection retains the descriptor *and* the full sample its custody judgment passed on (`judge_project_object_sampled`; the legacy `judge_project_object` wraps it with identical charges). Capture requires a sample equal to that judged one, then reads once within the existing 4 MiB custody bound, charged to the ledger, then requires a second sample equal to it. The full sample includes the change time, so a write, mode, owner or ACL change after the judgment refuses; nothing is re-baselined. When selection found none, its absence is observed by a charged no-follow lookup in the chain's retained root.
- **Interactive only, `.opensip/local.json`:**
  - `.opensip` is opened and judged by project-directory custody;
  - `local.json` is judged by configuration custody (`judge_local`) and captured bound to that judgment, the same way;
  - otherwise the absence of `.opensip`, or of `local.json` under it, is recorded.
- **In CI:** no lookup at all.
- **The recheck.** `ConfigCarriers::recheck` joins `ProjectRootAdmission::recheck` under the held fence:
  - a captured carrier is reopened by name and must have the same full sample;
  - each recorded absence must still hold.
- **The legacy path's admission** carries `carriers: None` and rechecks nothing new.

**The two phases (LD-B1B-1).**
- `admit_project_root_for_analysis` → `CarrierAdmission`: selection with retention, chain, incarnation, marker and carriers. It reads no registry.
- `CarrierAdmission::capture_registry` → `ProjectRootAdmission`: item 5, then classification.
- `ReadSession::admit_project_carriers` and `complete_project_admission` (`installation_read.rs`), and the write gate's `admit_carriers_on_gate` and `complete_on_gate` with `OrdinaryWriter`'s wrappers (`first_registration.rs`, `ordinary_writer.rs`), mirror the legacy wrappers: the same ledger scope, latching and session or gate recheck.
- The legacy `admit_project_root` and its wrappers are unchanged.

**Refusals.** There is no new code. A new `ProjectAdmissionRefusal::Carrier(subject)` maps to the existing `CONFIG.CUSTODY_REFUSED` row, with these subjects:
- `local-symlink`, `local-not-a-regular-file`, `local-custody` and `local-directory-custody`;
- `opensip.json:appeared`, `.opensip:appeared` and `local.json:appeared`.

A carrier that changed is the existing `Changed` row. Host I/O stays the host I/O row. `opensip.json`'s own custody refusals keep their legacy subjects.

### Security: the user-global carrier (LD-B1B-2)

`ReadSession::capture_optional(prefixes, leaf, cap)` (`installation_read.rs`), **r2, RF-02**:
- **One walk.** It runs `read_capture`'s own walk with `optional` set. Each existing prefix is judged exactly as a capture judges it: private custody, exact name and H's filesystem. A charged no-follow absence lookup runs under each judged parent before its child is opened.
- **Absence.** The first absent component is recorded as an `AbsentObservation`, holding the judged parents with the full samples of their judgments and the absent path. A parent that fails a judgment refuses and latches, as in a capture.
- **The recheck.** In the session's full recheck, `recheck_absent` reopens each parent by its exact name, judges it again by private custody, and requires its original full sample. The absent component must still be absent. A vanished, replaced or re-permissioned parent is a change.
- **Presence.** With every component present, it is exactly `capture`. With `optional` unset, `read_capture` is the legacy capture.
- **Never created.** Nothing is created. `I/host/settings.json` is read this way. J1 wires the call.

### Host: invocation mode (MB item 3; B1A-FU-1 resolved)

- **One type.** B1-a's duplicate `InvocationModeV1` in `configuration.rs` is removed, and the resolver imports `invocation.rs`'s. The purity pin's `crate::` count moves from 3 to 4 accordingly.
- **The module.** `invocation_mode.rs` (new):
  - `invocation_mode(stdin_terminal, stderr_terminal)` is the rule: both must be terminals;
  - `observe_invocation_mode()` is the one observation, `std::io::IsTerminal` on stdin and stderr.
  - It reads no environment, and has no caller before J1.
- **Operability.** `tools/operability/exceptions.json` gains one `stdio` row for `invocation_mode.rs`, count 1, under the closed owner "output and terminal". The source check passes with 114 rows; the mint census is unchanged.

### The environment structural check (M3-B r5 item 9)

- `crates/host/clippy.toml` and `crates/security/clippy.toml` are byte-identical. Each refuses `std::env::{var, var_os, vars, vars_os}`.
- There is no workspace `clippy.toml`, so platform (`crash_barrier.rs`) is outside the check.
- Thirteen item-level `#[allow(clippy::disallowed_methods, reason = "...")]` attributes cover r5's seventeen call sites exactly, on their enclosing functions.
- `tools/tests/test_environment_exceptions.py` pins:
  - every call site by file, function and **actual variable name**: **(r2, RF-03)** the constant-backed names `HELPER_INPUT`, `x8c::HELPER` and `MARKER` resolve to `OPENSIP_X8_INPUT`, `OPENSIP_X8_HELPER` and `OPENSIP_TEST_RETAINED_PATH_130`;
  - the allows on exactly those functions;
  - every exception but `git_tracking::process_environment` inside a test target. **(r2, RF-03)** A test target is a `tests/` file, a test-gated module found by brace matching on the code with comments and literals blanked, or a file `include!`d from inside one. Each allow must be attached to its function (only attributes between them). Two negative controls run on a copy: changing a constant's value, and moving an allowed helper out of its test module. Each must be caught without relying on Clippy;
  - no unqualified import;
  - the two identical configurations.

## Lead decisions taken in implementation

**LD-B1B-4, no public facade.**
- Project admission is `pub(crate)` in security, and making it reachable from the host is J1's wiring.
- So the plan's single hostile-environment child is split by crate, with the same coverage:
  - a security child runs the analysis admission (both phases) and the optional global capture over a fixture, and prints each carrier's path and SHA-256;
  - a host child runs `resolve_analysis_configuration` over all 52 PCM vectors, and prints each digest and provenance.
- Each runs clean and with hostile `HOME`, `PATH`, `CI`, `TERM`, `NO_COLOR` and `XDG_*`; the outputs must be byte-identical. Neither runs X2's tracking step.

**LD-B1B-5, no child-marker variable.**
- The hostile-environment, pipe and pseudo-terminal children are `#[ignore]`d tests that their parents run explicitly with `--ignored --exact`. Their result is their own assertion or their printed lines.
- So no child-marker environment variable is needed, and r5's allowance for "the child marker of B1-b's hostile-environment control" goes unused. The code's exception list is r5's list without it: strictly narrower.

## Round 4 (Codex `codex-b1b-r3`)

**R3-RF-01: integration-test files.** The pin test no longer exempts `tests/` files from production reachability. It computes reachability directly:
- **Roots.** The production roots are the files outside `tests/` that nothing includes: crate roots and `mod` files.
- **Flow.** Production flows along every include edge that is not inside a test-gated module.
- **Classification.** Any file it reaches is production, a `tests/` file included; every other file is wholly test code. So one production-reachable inclusion makes any file production, and an integration-test entry point stays test code only while nothing in production includes it.
- **The new negative control.** It includes the host's `tests/admission_tests.rs` from `crates/host/src/lib.rs` in a copy. `rustc_path`'s `RUSTC` exception then classifies production, and the pin rejects it; unchanged, it is test code.
- **Kept.** The src-file mixed-inclusion, comment and literal, constant-change and moved-helper controls stay.
- **Conservative direction.** An out-of-line `#[cfg(test)] mod x;` file would classify production, which can only cause a false rejection; none exists today.

## Round 3 (Codex `codex-b1b-r2`)

- **R2-RF-01, include confinement.**
  - The pin test now records every real `include!` edge, found on the blanked code so include-like text in comments and literals is no edge. The path is read from the raw text at the same offset.
  - Each edge carries whether it sits inside a test-gated module. A file is wholly test code when it is a `tests/` file, or when it is included and every inclusion is test-scoped or comes from a wholly-test file, resolved to a fixed point.
  - One production-reachable inclusion makes the file production.
  - New negative controls: a production inclusion of an allowed test file, added while its test inclusion stays, is caught; include text in a comment and in a literal creates no edge. The constant-change and moved-helper controls stay.
- **R2-RF-02, the zero CI lookup count.**
  - A test-only per-thread counter, `LOCAL_LOOKUPS`, counts `local_directory`, the only entry to the local carrier.
  - A CI admission (both phases) with `.opensip/local.json` present makes 0 lookups; an interactive one makes 2, the capture and the recheck.
  - A new lane mutation, `ci-ignored-local-lookup`, performs a charged local lookup in CI and ignores it. It is caught.
- **R2-RF-02, the refused-pack composition.** `ScenarioHome::compose_analysis_carriers` composes the real pieces. It sits in security's existing test-only `scenario` seam: `scenario-fixtures` feature, `#[doc(hidden)]`, enabled only by storage's and host's `[dev-dependencies]` (law X8 r3 item 4), so there is no production facade or caller. The steps:
  1. it opens an ordinary writer's gate and runs the analysis first phase;
  2. it hands the captured carrier bytes to the caller's decision;
  3. it runs item 5 only on an admitting decision;
  4. it drops the writer and reports what reached the registry and I.

  The host test `a_refused_project_pack_stops_before_the_registry_composed_across_crates` decides with the real `resolve_analysis_configuration` (the resolver and X12 pack admission).
  - **A project-layer `other.pack:1`:** not admitted, the registry not captured, `project-registry.v2` byte-identical (no RESERVED row), every member of I and of the project the same path and size (no lease, journal or marker), and the writer and fence released.
  - **The bundled pack:** admitted, the registry captured, and still nothing registered or written.

## Round 2: the controls Codex required (RF-04)

- **Judgment to read (RF-01).** Selection's retained judgment and `judge_local`'s are each followed by an interposed rewrite, or by a mode change, before the read. Each refuses `Changed`. The unchanged path captures the judged bytes.
- **Optional parents (RF-02).**
  - A wrong-custody existing `I/host` refuses.
  - After an absence under a judged `I/host`, each of these refuses on recheck: a mode change, a replacement (rename, and a fresh private `host`), and a detachment.
  - The absent `host` appearing and the leaf appearing (r1) also still refuse.
- **No registry read in phase 1 (MB item 10).**
  - Phase 1's ledger charges are equal with an empty registry and a 40-row registry, so phase 1 reads no registry.
  - After phase 1 and a drop (what a refused pack leaves), no member of I is created, removed or resized except the fence carrier's own, and a new session opens: the fence was released.
  - The pack refusal itself is the host's `resolve_analysis_configuration` (B1-a's X12 order control). Composing the two crates is J1's.
- **CI makes no local lookup (a ledger counter).** Every lookup is charged. In CI, phase 1's charges are equal with and without `.opensip/local.json` present. Interactively they differ.
- **The legacy path against the base product.** The lane copies the base product (`git archive HEAD`), adds the same probe file (`project_admission_legacy_probe_tests.rs`, which uses only base APIs), and runs it there and here, with the same private TMPDIR. The legacy admission's printed charges and classification must be equal line for line, in five states:
  - no config;
  - a small config;
  - a 1 MiB config;
  - `.opensip` present;
  - `local.json` present.

  The legacy read-session and write-gate wrappers are unchanged in source. The session's recheck adds `recheck_absent` over an empty list on that path.
- **Hostile environment (MB item 9).** Each child now runs with a cleared environment (only the private TMPDIR kept), then with hostile values.
  - The security child prints each carrier's path, length and SHA-256, the global carrier's, and the classification.
  - The host child prints, for all 52 PCM vectors, the canonical semantic and operational records, the digest, and every provenance entry: layer, canonical winning value and source.
  - The two runs must be byte-identical.
- **The permitted Git refusal, asserted separately.** A child runs X2's tracking on an admitted fixture project. With the cleared environment it proceeds (`ok`). With the hostile one it refuses, and the refusal names `environment-` (X2's refusal-only check reads `HOME` and `XDG_CONFIG_HOME` before any repository discovery).

## Controls

The lane is `checks-r1`:
- **Suites.** Security and host on the base and the candidate, `--no-fail-fast`, with equal failure sets (the pre-existing base failures).
- **Lint and format.** All-targets Clippy with warnings denied on both crates. **(r2, NBO-01)** rustfmt runs on every edited or new Rust file that was rustfmt-clean at base, or is new. The lane classifies every edited Rust file (`evidence/rustfmt-classification.json`). Files dirty at base are listed and not reformatted. Four base-clean files were formatted after the allow attributes went in: rustfmt only splits those attributes over lines.
- **Tools and census.** The two tools tests, the operability census and verify_design.
- **Seven code mutations,** each caught: **(r3)** an ignored charged local lookup in CI, CI probing local, the absence recheck disabled, the carrier recheck disabled, **(r2)** capture re-baselining instead of binding to the judgment, **(r2)** the optional-parent sample comparison disabled, and the mode's "either stream".
- **Two planted `std::env` reads,** one in host production code and one in security production code. Each makes Clippy fail with `disallowed_methods`, which proves each crate-local configuration is read.

The new security tests cover:
- capture and provenance;
- CI never looking up local, with hostile local bytes refusing only interactively;
- each appearance after an absence;
- a custody-valid `.opensip` appearing in CI never being a local refusal, with marker custody refusing in contrast;
- changed carriers;
- local custody subjects;
- phase 1 reading no registry;
- **legacy compatibility:** identical ledger charges for a 2-byte and a 1 MiB `opensip.json`, and with and without `local.json` present;
- the optional global capture's absence and its recheck;
- FW-01: the project tree is unchanged and I's member set does not grow;
- the hostile-environment capture child.

## Not claimed

- No CLI wiring or public API (J1).
- No discovery (B2), member carriers (B3) or S-OP-5.
- No inventory successor yet: v189 follows the accepted code.
- No product qualification.
