**The gap is real: CORRECTION_REQUIRED.** I tested it with owner graphs at admission and in closed Runs, rather than relying on the earlier code reading. Frozen41 matched its manifest before and after (12912 members, 0 missing, mismatched or extra), and all relevant source files match it byte for byte. All subprocesses have finished.

## Does changing only provenance to explicit (keeping null) admit?
Yes, and no existing check refuses it.
- **Admission** (the maintained `check-enumeration` harness):
  - the default `ts-tsconfig` binding with only provenance changed to `explicit-plan-selection` admits;
  - `js-synthesized` explicit null also admits, given a matching context.
- **Full Run:** I used the semantic fixture, executed from its own bytes with two asserted changes: a real `tsconfig.json` default unit from `discover_units`, and the binding's provenance and `programEntry`.
  - R3 (default control with only provenance changed) closes on the exact manifest.
  - Controls: R2 (default null) and R1 (explicit `"tsconfig.json"`) close.
  - Refused: R4 (default with non-null entry) refuses `ENUMERATION_BINDING_PROGRAM_ENTRY`.
- **Why nothing catches it:** the model refuses a non-null entry on a default binding. It also compares the retained graph entry against either the given path or, when null, the path it derives from the default unit's marker. It never checks provenance when the entry is null. An explicit null is refused only by accident, when that derived path differs from the retained graph entry (R5, or a graph entry of `tsconfig.build.json`).
- **My first `js-synthesized` world failed** because the harness hardcodes a `ts-tsconfig` context. I preserved it and retried directly.

## Proposed correction
The patch is `correction.patch` (sha256 `89097b0c…`); base and after hashes are in `delta-manifest.json`.
- **Model** (`enumeration_model.v1.py`): an available binding with `explicit-plan-selection` in a TS/JS mode and a null `programEntry` now refuses the existing `ENUMERATION_BINDING_PROGRAM_ENTRY`.
  - Unchanged: defaults, non-null entries, Rust, syntax-only, candidate cells, unavailable bindings, schema and identity.
  - `js-synthesized` is included because the published text says "TS/JS", so a synthesized program is encoded only as a default binding. Excluding that mode is a one-token change but would need owner wording.
- **Checker** (`check-enumeration.v1.py`): the harness can now take a `native_contexts` override. There are 8 new cases:
  - **new refusals:** TS explicit null and `js-synthesized` explicit null;
  - **existing behaviour guarded:** default binding with a non-null entry is refused;
  - **preservation, all admit:** explicit TS naming the marker config, `js-synthesized` default null, Rust explicit null, syntax explicit null, unavailable explicit null.
  - The three refusal cases must produce exactly `ENUMERATION_BINDING_PROGRAM_ENTRY`.

**Receipts:**

| Run | Cases | Mismatches |
|---|---|---|
| Unpatched copy | 46 | 0 |
| Patched copy | 54 | 0 |
| Patched checker on unpatched model | 54 | 4, exactly the two new refusals and their exact-refusal checks |

- The 46 shared cases are identical between base and patched.
- **Patched Run:** R3 is now refused, while R0, R1 and R2 still close on the exact manifest.
- **Patched admission:** Rust, syntax and every unavailable variant are unchanged.

**Maintained explicit-null shapes that would stop admitting.** Some explicit-null `ts-tsconfig` bindings in `check-atoms.v1.py` (and a mode-less workflow projection helper) never reach enumeration admission, so they're unaffected at runtime. I report them and did not change them.

## The two other open notes
- **Unavailable bindings (path or null): no change needed.** It is Plan-selection input the owners intentionally leave free, not a missing rule.
  - With a null universe there is no native entry to compare, and admission only checks that a non-null value is a snapshot path. All four variants admit.
  - No evaluator, execution-input or native model reads `programEntry`, and no owner claims a canonical encoding.
  - Different values are different Plans, not nondeterminism.
- **Explicit Rust path: no change needed.** It is a Plan label; the universe identity is the program key.
  - Native `bind_rust_universe` takes no `programEntry`, and the schema and §9 say it isn't a complete program key.
  - Duplicate universes in a cell are already refused. Default null, explicit null and explicit `Cargo.toml` all admit.
  - Contract §1 `:24` slightly overstates `programEntry` as a Rust/syntax bind input. That is prose imprecision with no behavioural effect.

## Root's scope correction
Replacing "It never copies the U-1 marker …" with "For an available default-unit binding, it never copies …" is **correct and necessary**:
- **It protects lawful explicit selection.** Explicit bindings naming the marker config are maintained lawful shapes: the semantic fixture (its Run closes), `check-atoms`, and my admitted probe case. The unscoped sentence would forbid them.
- **It matches the enforced rule.** The scoped sentence matches exactly what admission refuses, and doesn't reach unavailable bindings.

## Limits
- **Standing:** admission results are the enumeration owner join. Run results come from the maintained semantic sequence on a probe variant; no fixture file was written.
- **Not run:** broad suites, pins, planning, `check-atoms`, workflow or other Run checkers. "No other admission-reaching explicit TS/JS null bindings" rests on source search, not execution.
- **Hash index scope:** `hash-index.json` also hashed pre-existing harness files in the runtime (`launch.py`, `process.json`, `prompt.md`, `public-events.jsonl`). I didn't create or read them.

Files are in `/private/tmp/opensip-design-corrections/claude-program-entry-enforcement.v1`:
- review.md
- review.json
- correction.patch
- delta-manifest.json
- hash-index.json
- receipts/
- tools/
