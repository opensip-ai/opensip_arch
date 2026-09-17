# Enumeration integer-profile reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Frozen **proposal**, **not selected**. Not parser-38 / dependency / source / runtime acceptance. Not complete enumeration, replay, release, or M2–M6. Root assent and private activation remain required.

**subjectManifestSha256** `1b83d3175f1fd945062666f9761327199dfe2411a8dfa483e26ceabd05db4bcc`  
`docs/implementation/m2/enumeration-integer-profile-reference-selection-v1-subject.json` **3773** bytes, **16/16** files, paths sorted unique, **0** pin mismatches. Successor candidates (15) equal the subject minus that record. `passageOverrides` is `[]`.

## What this unit is

Reference-only process profile for the CPython tomllib oracle. Candidate `enumeration_model.v1.py` **50447** / `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992` (E50447B) vs selected totality E **49833** / `689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072`.

Independently, the AST delta is exactly:

- `import sys`
- `class ReferenceEnvironmentError(RuntimeError)` (docstring: never an input `AdmissionError` or syntax finding)
- `_require_reference_integer_profile()` requiring **both** `sys.flags.int_max_str_digits == 0` and `sys.get_int_max_str_digits() == 0`
- that helper at **module import** and at the start of `project_named_packages`
- no other function body changes; Cargo `except` remains `(TOMLDecodeError, UnicodeDecodeError)` only
- **no** `sys.set_int_max_str_digits` in the model

Pinned interpreter: CPython **3.12.13** `-I -B -X int_max_str_digits=0`. Incompatible startup is `ReferenceEnvironmentError`, a tooling/environment failure, never `parseFailed` `syntax` or a resource Limit. This matches the semantic-38 process-profile addendum (startup flags **and** effective value; gate on package entry, not import-only; `-X` because isolated `-I` ignores `PYTHONINTMAXSTRDIGITS`). Arbitrary literal retention is the **oracle profile**, not a TOML 1.0 unbounded-integer mandate (precision addendum). Rust is not this unit.

Future AST-overlay harnesses must load the complete new module or carry the helper/class **and** the function-entry gate. This checker overlays the whole file. Historical totality E and old harnesses are unchanged.

## Parents (live lock independently **24 inventory / 34 contract**)

Live `design-lock.json` **71077** / `e903cf3459085a1d0487538a104f9c8a496da9729a95ef33d694d72b14c03462`. Last contract is already **enumeration-totality-v1**. All **three** parents are accepted **contract records** (path/bytes/sha256 match lock + architecture disk). Sorted unique. None are lock `inputs`.

| Parent | Live class |
| --- | --- |
| capability-totality-v1 successor `6421e727…f064` / 3596 | contract record |
| enumeration-totality-v1 successor `342afdbd…0b69` / 2610 | contract record |
| native-runtime-v17 successor `d41ff9c8…4853` / 11769 | contract record |

## Evidence (independent reproduction)

Portable `check-profile.py` **5840** / `449c22e801139d471b042b871e16d938b9aecb587e12cb5e2bcbac267f47fd44` rerun with:

`--source32 /tmp/opensip-implementation/m2-full-walk-subject-32`  
`--source32-manifest` full-walk-32 subject **97191** / `c52cf367757970cb072e8ae72e6c29fe8b60741719709eafda2cd5a6f464ec96`  
`--python` native-case15 3.12.13  
`--output` `review/reproduce-check` (fresh)

Checker hashed **157** `reference/` members of SOURCE-32 (508 files in that subject) before overlaying separately pinned old/new E. Child processes use `-I -B` plus the explicit `-X` flag where required. Exit 0.

Frozen evidence **byte-identical** to this run: `result.json`, `exceptions.json`, `before-default.json`, `before-zero.json`, `after-zero.json`, `after-default.json`, `after-640.json`, `after-mutated-zero.json`.

| Claim | Independent |
| --- | --- |
| 1940 comparisons, 144 numeric | yes |
| 1922 defined default outcomes unchanged | yes |
| 18 old default `ValueError` (4301/5000 decimal, signed/underscore, three placements) become named `p` under zero-profile | yes |
| all 1940 old/new **zero-profile** outcomes match | yes, 0 mismatches |
| 3 bad-startup import controls (default, 640, default-then-`set(0)` fake zero) | `ReferenceEnvironmentError`; mutated control has flags 4300 / get 0 |
| post-import mutation 0→4300 refused at package entry | same message, then restored |

## requiredFindings

None.

## Limits / not claimed

Not selected until root assent. Not parser-38, its dependency graph, or package-projection install. Not SOURCE-34/35 re-acceptance. Not runtime-17 product re-verification (parent pin only). Not complete enumeration, replay, resource/security qualification, or M2–M6. The Python oracle still converts integers (CPU cost). Historical default-profile `ValueError` rows remain separate evidence, not selected syntax law.
