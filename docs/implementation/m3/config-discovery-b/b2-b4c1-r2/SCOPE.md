# B2-b4c1 r2: what the candidate delivers (M3-B unit B2-b4, sub-unit B2-b4c1: the blind held-out census mode)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements the code half of section 2.5 of the accepted B2-b4 plan r6 (Codex `codex-b2b4-plan-r6`; architecture `a5b3fc88`). Section 2.5 follows the owner's decision of 2026-10-16 (`owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`, the option "Mechanical blind run").

The base is product `d33df45`:
- B2-b4b3 is bound;
- inventory is v198;
- there are 164 contract successors.

**This unit opens no held-out store, and no check or control in it does.** The run itself is B2-b4c2, which follows this review.

## r2 changes (Codex `codex-b2b4c1-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2B4C1-R1-RF-1:** the Rust margin test counted held-out rows but did not check their ids. | **The test binds the record's identities to the reviewed manifest.** The record's manifest pin must equal `MANIFEST_SHA256`. The SHA-256 of the entry ids in record order, of the workspace ids, and of the ids carrying a held-out status (each list joined by newlines) must equal three constants, which are computed from the manifest's ids and flags. So a duplicated, foreign or substituted id fails, as does an omitted row or a held-out status on a lead-readable entry. A workspace row can no longer carry a held-out status. **New census-record controls:** same-count duplicate id, foreign id, lead-readable row substituted by a passing composed row, lead-readable row omitted. |
| **B2B4C1-R1-RF-2:** a `SystemExit` passed both handlers, and an abbreviated flag could enter the blind mode unredacted. | **The parser refuses abbreviations** (`allow_abbrev=False`). **Redaction comes from the parsed arguments:** `main` parses, then runs the blind mode inside one `except BaseException` boundary, so an exit, an interrupt or any exception prints only the generic line and exits 1. Parser exits (usage, help) come first and echo only the command line. `blind_row` also reduces a `SystemExit` to its class. **New controls:** a measurement raising `SystemExit` with a planted path (`MODEL`); in-process `main` runs whose `costs` raises `SystemExit`, `KeyboardInterrupt` or `ValueError` carrying the canary (only the generic line); abbreviated spellings refused with exit 2, no canary and no receipt. |
| **B2B4C1-R1-RF-3:** the receipt did not bind the code the population check runs. | **The bindings gain `reference`:** the pins of `tools/security/discovery_walk_vectors.py` and `tools/contracts/generator-closure.json` (which pins the provisioned packages), and the architecture pins of the bound reference, the SLM and rule it pins, and the foundation `canonical.py` SLM imports by path. `load_reference` refuses unless the files actually loaded are exactly those (`REFERENCE_ARCH`). **New drift controls:** each of the six reference inputs makes the receipt stale. |

**New guard mutations, each caught:** `abbreviation-allowed`, `exit-not-reduced`, `boundary-narrowed` and `reference-unbound`. The r1 mutations follow the moved code.

## What changes

| Path | Change |
| --- | --- |
| `tools/security/discovery_census.py` | **The blind mode, `--held-out-blind`.** It is mutually exclusive with `--check` and `--write` and needs `--t2-cache`. `run_blind` writes only `crates/security/src/custody/discovery_census_held_out.json` and prints one line of counts.<br>**The held-out join.** `held_out_store_path` is the only join of a held-out digest to the store. It refuses without the mode's private token and for any entry that is not held out. `store_path` is unchanged and still refuses every held-out entry.<br>**Each row.** `blind_row` runs, in order: `verified_tree` (the same integrity check); the same model and reference population, through `measure`; the population comparison; and the per-mille margins against the caps the code holds (bytes at the largest root length). Failures map to classes: an `OSError` is `IO`; any other exception is `INTEGRITY` during verification and `MODEL` during measurement; a population difference is `POPULATION`. The exception is discarded.<br>**The receipt.** `receipt_bindings` builds the bindings: the manifest pin, the tool's own pin, every closure pin, the sizes, the caps, the root lengths and the reference-loading pins (r2). `receipt_state` derives the state.<br>**The ordinary mode.** `validated_receipt` checks the closed format and unique ids, and that the state equals the one derived from the rows. `compose_held_out` returns the census record's held-out rows and `heldOutMargin`: outstanding when there is no receipt, stale on any binding drift, otherwise composed after an exact coverage check. `census_output` takes its held-out rows from `compose_held_out` (status `blind-census`, the receipt row without its id as `result`). A failing composed row enters `failingEntries`, in manifest order, and so returns the caps.<br>**Output.** In the blind mode, `main` prints only `Discovery census blind run failed.` for any failure (r2). The ordinary mode's error output is unchanged.<br>The module docstring describes the third output. |
| `tools/tests/test_discovery_census_blind.py` | **New.** The synthetic controls: 19 tests, in four classes (Canary, Receipts, Lifecycle, Access) over a shared Fixture. Below. |
| `crates/security/src/custody/discovery_census_tests.rs` | **The margin test reads composed held-out rows.**<br>• It accepts `outstanding: held-out`, `outstanding: held-out (blind receipt stale)` and `blind-census` held-out rows.<br>• `blind_result` checks each composed row's closed format, and that `passes2x` agrees with its margins at 2000.<br>• **Identity (r2):** the manifest pin and the entry, workspace and held-out id lists must equal reviewed digests.<br>• All ten held-out rows must be in one state: outstanding, stale or composed.<br>• `failingEntries` equals the failing lead-readable and blind rows, in record order. No lead-readable entry fails (the r7 full claim, as before).<br>• `caps` is `returned-to-law` exactly when something fails.<br>• `heldOutMargin` equals the state derived from the rows. Only `holds (blind census)` (all ten measured and passing) meets the gate.<br>The header comment names the new scope. |

**Unchanged.** `discovery_census.json` and `discovery_census_vectors.json` are unchanged: the record pins the closure, not the tool, and no receipt exists, so the census `--check` passes on the base record.

## One reading of section 2.5, made explicit

Section 2.5 says the ordinary mode "validates its format and coverage", then checks the bindings, and that "any drift" makes the receipt stale. A manifest drift can change the held-out id set itself. The ids are then checked against a manifest the receipt is not bound to, and the two sentences disagree. This candidate:
- checks format and unique ids on every receipt;
- checks exact coverage against the current manifest only when every binding (the manifest pin included) matches;
- treats a drifted manifest as stale, never as a coverage refusal.

Either way, a drifted receipt never composes.

## The controls (synthetic stores, receipts and models only)

| Plan r6 control | Tests |
| --- | --- |
| **Leakage.** A canary in a held-out tree's names and content is absent from the receipt, stdout and stderr; an allow-list checks the closed formats. | `Canary.test_a_measured_run_emits_only_the_closed_rows`; every other Canary test runs the same silence and allow-list checks. The canary is also absent from the temporary path. |
| **Errors,** each reduced to its class. | `MODEL` (a raising model, the canary in its message; an unexpected exception type); `IO` (a raising `PermissionError` naming a canary path; a removed store; an unreadable store directory); `POPULATION` (a population differing by a canary path); `INTEGRITY` (a planted canary file). |
| **The command line.** | A subprocess in the blind mode whose input paths carry the canary prints only the generic line. The same failure in the ordinary mode still names the path. **r2:** abbreviated spellings are refused (exit 2); in-process `main` runs with an exit, an interrupt or an exception carrying the canary print only the generic line. |
| **Invalid receipts.** | Missing, unknown (a lead-readable id; a foreign id) and duplicated ids. An error row with margins, or with a non-class `errorClass`. A measured row without margins, with a string margin, with `integrity: false` or with an extra key. A `passes2x` disagreeing either way. An unknown status. A disagreeing state, an extra top-level key, empty rows. |
| **Lifecycle.** | A blind run, then the census record built twice: equal bytes (`--check` after `--write`), state `holds`. A failing run: `fails`, the ids in `failingEntries`, `returned-to-law`. An erroring run: `incomplete`, nothing failing. No receipt: outstanding. Drift in each binding (tool bytes, a closure file, each of the six reference-loading inputs, a size, a cap, a root length, the manifest bytes, the held-out id set) is stale, and the receipt composes again once the inputs are restored. |
| **Access.** | A spy on `lstat`, `stat`, `scandir`, `listdir`, `readlink` and `open` during the ordinary census record: the lead-readable store is touched, and neither held-out store is. The lead-readable model is stubbed; only access is under test. The blind join refuses without the token and for a lead-readable entry; `store_path` still refuses a held-out one. A held-out workspace refuses the blind mode. |

**Lane mutations.** Each must make the blind controls fail:
- `exception-text-kept`;
- `generic-message-dropped`;
- `abbreviation-allowed`, `exit-not-reduced`, `boundary-narrowed` and `reference-unbound` (r2);
- `blind-join-unguarded`;
- `stale-binding-ignored`;
- `coverage-unchecked`;
- `passes2x-unchecked`;
- `ordinary-opens-held-out`.

**Census-record controls for the Rust margin test.** Each temporarily replaces the census record with a synthetic composed one, with invented margins, then restores it:
- **Four valid records must pass:** holds, fails, incomplete, stale.
- **Eleven invalid records must fail:**
  - holds with a failing margin;
  - holds with an error row;
  - a `passes2x` disagreeing with its margins;
  - partial coverage;
  - failing with the caps holding;
  - failing but not listed;
  - an error row in an open format;
  - (r2) a same-count duplicate id, a foreign id, a lead-readable row substituted by a passing composed row, and an omitted lead-readable row.

## Inventory

`tools/tests/test_discovery_census_blind.py` is a new path, so an inventory successor (v199) follows this unit's code commit, as in earlier units. It also carries the description-correction row recorded at B2-b4b3 (`discovery_census.json` and `discovery_census.py`). The receipt, a new path of B2-b4c2, gets its own successor after that run.

## Checks

See `evidence/checks.json`. The rows are:
- the security suite at base and candidate, with equal failure sets;
- warning-denied all-targets Clippy on host and security;
- rustfmt;
- the environment and FW-01 pins;
- the scan, upward and walk vector checks;
- the walker storage check;
- the census-tool controls, old and new, and the census `--check` (lead-readable stores; no receipt);
- the configuration tables, the operability census and verify_design;
- the guard mutations and the census-record controls.

The platform crate is unchanged, so its suite is not run.

## Not claimed

- No held-out store opened, no receipt, no held-out margin. The run is B2-b4c2's.
- No production caller and no qualification.
- No law change.

B2-b is not complete.
