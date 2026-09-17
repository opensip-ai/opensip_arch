# Addendum: process-startup integer-conversion profile

**Separate from** original `advisory.md` **8474** / `3e2c8365…c56d` and numeric-totality addendum **7147** / `157150ddbfa20d409f42eaba15bf146e3dbecdabba9dfe3236b80ecc0e0f7742` (also `preserved/`). This note does **not** rewrite those texts.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Suitability of an explicit CPython **process-startup** profile (`python -I -B -X int_max_str_digits=0`) for the next enumeration reference unit. **Not a candidate. Not source/dependency acceptance. Did not modify reference or product.**

Root favors Option A, but **not** `sys.set_int_max_str_digits` around `tomllib.load` (process-global mutation, races, restoration is not a profile). Proposed: selected enumeration module imports `sys`, at **module initialization** requires `get_int_max_str_digits()==0`, else a clear `RuntimeError` demanding `python -I -B -X int_max_str_digits=0`. New harnesses pass `-X0`. Invalid interpreter profile is a **tooling precondition**, never enumeration syntax/semantic refusal. Rust adds no decimal-digit Limit. Historical old E/harnesses stay unchanged; old defined outcomes are compared under explicit 0, and old default-`ValueError` cases are recorded separately.

## Verdict

**The process-startup boundary is the right Option A. No more suitable selected convention exists than “environment gate, never admission.” Two adjustments avoid material holes; they do not reject the boundary.**

1. Pin **startup** with `sys.flags.int_max_str_digits == 0`, not only `get_int_max_str_digits()==0`.
2. Put the gate on **`project_named_packages` (and any other `tomllib.load` entry)**, not solely module import. Optionally also at import for fail-fast.
3. Raise a **reference-environment** error (same class as selected native `ReferenceEnvironmentError`), not `AdmissionError`, and not a package `syntax` / `parseFailed` reason. Bare `RuntimeError` is acceptable only if harnesses already treat any uncaught exception as tooling failure and never map it to classification.

Rust: no decimal Limit. That remains a **CPython/OpenSIP profile** choice (see the separate precision note), not a TOML 1.0 unbounded-integer mandate.

## Existing selected convention (use this, do not invent a third class)

Standing Python invocation is already **`python -I -B`** (isolated, no bytecode). Selected native (`capability-totality-reference-selection-v1` `native_evidence_model.py` **702–751**) is the profile pattern:

- `ReferenceEnvironmentError` is **not** `AdmissionError`.
- Unicode case-data mismatch refuses **the operation** (`lib_name_fold`), never a typed refusal about caller input.
- “The binding is effective, not advertised.”
- Environment fault: host cannot produce a conforming answer.

Integer conversion belongs in that class: wrong `int_max_str_digits` is an interpreter that cannot reproduce the published tomllib classification, not a malformed `Cargo.toml`.

There is **no** existing selected check of `int_max_str_digits`. Do not reuse `AdmissionError`, `TOMLDecodeError`, or `parseFailed` `syntax`.

## Why `-X` and not `PYTHONINTMAXSTRDIGITS`

Measured on the pinned 3.12.13 binary:

| Invocation | `get_int_max_str_digits()` | `sys.flags.int_max_str_digits` |
| --- | ---: | ---: |
| `python -I -B` | 4300 | 4300 |
| `PYTHONINTMAXSTRDIGITS=0 python -I -B` | **4300** (env ignored) | 4300 |
| `python -I -B -X int_max_str_digits=0` | **0** | **0** |
| `PYTHONINTMAXSTRDIGITS=0 python -B` (no `-I`) | 0 | 0 |
| `python -I -B` then `set_int_max_str_digits(0)` | 0 | **4300** (flags stay startup) |

`-I` implies `-E`: all `PYTHON*` environment variables are ignored. The numeric addendum’s env-var alternative is **inoperative** under the standing `-I -B` convention. **`-X int_max_str_digits=0` is the flag that actually sets the process profile.** CPython documents that `-X` wins over the env var when both are set; with `-I` only `-X` remains.

CPython itself moved this limit to a **process-wide global** (gh-95778). Call-site `set_int_max_str_digits` is not a safe restoration story. Reject that path.

## Material holes if implemented exactly as first proposed

**A. `get()==0` accepts mid-process mutation.** After a default startup, `set_int_max_str_digits(0)` makes `get()` 0 while `sys.flags.int_max_str_digits` remains 4300. That is the race/restoration surface root wants to close. Require:

```text
sys.flags.int_max_str_digits == 0 and sys.get_int_max_str_digits() == 0
```

Startup `-X int_max_str_digits=0` satisfies both. Mutation after a wrong start fails the flags check. Mutation away from 0 after a good start fails `get()`.

**B. Module-init-only is skipped by overlay harnesses.** `check_packages38.py` loads foundation `enumeration_model.v1.py` then `exec`s a single `FunctionDef` (`project_named_packages`) from the selected file into that namespace. Top-level init of the **new** module never runs. Unicode already gates **in the function that needs the environment**, not only at import. Put the same check at the start of `project_named_packages` (before `tomllib.load`). An additional module-level check is fine for `import enumeration_model` fail-fast; it is not sufficient alone.

**C. `RuntimeError` vs `ReferenceEnvironmentError`.** Not fatal if harnesses never catch it as syntax. Closer selected law is a dedicated environment exception whose docstring says it is not `AdmissionError` and must not become `parseFailed`. Native already has the name. Enumeration may define a local sibling rather than importing native’s class (owner split). Message should name the required argv: `python -I -B -X int_max_str_digits=0`.

None of these reject the process-profile boundary. They are how to implement it without a silent bypass.

## What is not a flaw

- Invalid profile is not `syntax` / not `Limit` / not `parseFailed`. Agreed.
- New harnesses all pass `-X int_max_str_digits=0`. Agreed. Keep `-I -B`.
- Historical old E unchanged. Agreed.
- Compare old defined outcomes **under explicit 0** (those cases never needed 4301 decimal digits). Agreed.
- Record old **default-4300 `ValueError`** cases as a **separate historical ambient artifact**, not as selected law and not as syntax. Agreed.
- Rust adds no decimal-digit Limit. Agreed for this profile (lazy `DeInteger` already does not convert). Identity `MAX_BYTES` (4 MiB) still bounds the blob; that is unrelated.

## Suggested gate (illustrative, not product text)

At the start of `project_named_packages` (and at module import if desired):

- If `sys.flags.int_max_str_digits != 0` or `sys.get_int_max_str_digits() != 0`: raise the environment error naming `-X int_max_str_digits=0`.
- Do not call `sys.set_int_max_str_digits`.
- Do not catch that error in the TOML `except` that maps `TOMLDecodeError` / `UnicodeDecodeError` to `syntax`.

Harness argv: pinned CPython 3.12.13  
`…/python -I -B -X int_max_str_digits=0`.

## Unqualified

Not a selected unit. Not an edit of `E689620`. Original incomplete-radix report and numeric-totality addendum stay as written, including the numeric note’s env-var wording; this addendum is the operational correction for `-I`.
