# Enumeration locator-totality reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Frozen **proposal**, **not selected** until root assent and lock activation. Not enumeration-join-41 / product / parser-38 / source / runtime acceptance. Not complete enumeration, reconstruct, replay, release, or M2. Selection, if later activated, is **lock-only** and must not rewrite runtime-18’s 257 non-lock product sources.

**subjectManifestSha256** `5b0151423ca2e6b92c8186c474091fbc996ee203f82e7dd878e929b251e40077`  
`docs/implementation/m2/enumeration-locator-totality-reference-selection-v1-subject.json` **2854** bytes, **12/12** files, paths sorted unique, **0** pin mismatches. Successor candidates (11) equal the subject minus `successor.json`. `passageOverrides` is `[]`.

Prior totality-42 advisory is preserved byte-identical (`advisory.md` **14380** / `7a4f5583…131c2`; `advisory.json` **6087** / `6c45791a…1e54`). Precision addendum withdrew the residual float-alias as **outside JSON-C**; this unit does not add float support.

## What this unit is

Reference-only successor to selected enumeration integer-profile E **50447** / `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992`. Candidate `enumeration_model.v1.py` **50678** / `a02960c631df0f0342f039fcef395dbba402d67453dbc9aba760fad0e6719d5c` equals `evidence/candidate.py` (normative reference = candidate).

Independently, the AST delta is exactly one membership/`set.add` wrap:

```python
try:
    if loc in binding_by:
        schema_failed.add(loc)
except TypeError:
    # JSON-C array/object locator fields cannot name a binding.
    # Keep the schema refusal and allow missing-record accounting.
    pass
```

Predecessor contains that unwrapped block once; `old.replace(old_block, new_block) == new`. Bare `except TypeError` count 0 → 1. Integer-profile gate, INV_SCHEMA path, `_add` first-seen order, refusal vocabulary, hashing, package projection, and successful ADMIT behavior are unchanged. No malformed inventory becomes ADMIT. Unhashable JSON-C array/object locators cannot occupy `schema_failed`, so the expected slot still yields `ENUMERATION_INVENTORY_MISSING_RECORD` after `ENUMERATION_INVENTORY_SCHEMA`.

Python scalar equality on the schema-failed path is retained (`False` occupies ordinal 0, `True` occupies 1). Those booleans remain schema-invalid and never enter accepted row processing. Tightening that diagnostic to `C.equal_typed` / Rust Bool≠Integer is **not** this unit.

JSON-C has no float: selected `canonical.py` `typed`/`canonical` raise `EXACT_JSON_TYPE_REQUIRED`; `parse` raises `FLOAT_OR_NONFINITE_FORBIDDEN`; Rust `JsonValue` (`Value`) is Null/Bool/Integer/String/Array/Object only. Do not add float alias.

## Parents (live lock independently **25 inventory / 36 contract**)

Live `design-lock.json` **74089** / `4df2bd504524bbb95bf18bca92ef545de3a1d0b480b676958a63b9125d8af99b`. Last contract is already **native-runtime-selection-v18**. Both parents are accepted **contract records** (path/bytes/sha256 match lock + architecture disk). Sorted unique. None are lock `inputs`. This locator-totality successor is **not** in the lock.

Request text said 24/36 with inventory-27 pending. Independently, inventory-27 is now lock inventory 25 (`ACCEPTED-UNIT`). That concurrent inventory activation does not change these parents.

| Parent | Live class |
| --- | --- |
| enumeration-integer-profile-v1 successor `536754c6…0265` / 4354 | contract record (`ACCEPTED-DESIGN-UNIT`) |
| native-runtime-v18 successor `7824be20…8ad1` / 22076 | contract record (`ACCEPTED-DESIGN-UNIT`) |

## Evidence (independent reproduction)

Portable `check-reference.py` **4388** / `8ca24d6ef68ebc0be36abdcbdeab4a4296d0406b3dbb4c5aa5789fb44441def1` rerun with pinned CPython **3.12.13** UCD **15.0.0**:

```
/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0 \
  …/evidence/check-reference.py \
  --output /tmp/opensip-implementation/m2-grok-enumeration-locator-totality-reference-v1-review/review/reproduce-check
```

Checker uses only `Path(__file__).parent` (no `/tmp` ambient fixture). Exit 0. `result.json` byte-identical to pinned `expected-result.json` / `comparison.json` **402** / `55b382a6ae7385e58ac9a22b071dbcbac0324e9759574b6d93bcbb06deb7df5e`.

| Claim | Independent |
| --- | --- |
| 159 fixture pins + tar census, regular members only | yes; before-tree 159, after-tree 159 |
| 157 members = frozen source32 reference except accepted integer-profile E | yes; 156 non-E sha match source32; E is `d32883fd…26992` |
| 2 extra files = accepted application-subject.v46 target-attribution v1/v2 | yes; **13480** / `788bd9d0…ed90e` and **23086** / `bd938f11…1d53`; v46 **126405** / `dab6e00f…743f7` |
| Uncompressed corpus pin **18215825** / `f8a3fe77…4faf8b`, 1537 cases | yes (`cases-pin.json`) |
| Exact narrow source patch | yes |
| Every recorded before/after output | yes; 0 mismatches |
| 1519 defined results unchanged | yes |
| 18 former TypeError → SCHEMA then MISSING | yes |
| Normative `reference/enumeration_model.v1.py` == `evidence/candidate.py` | yes |
| After overlay E == candidate; before E == predecessor | yes |

Corroboration from private totality-42 replay (selected vs candidate, same interpreter): mutation 1423/1423, boolean 45/45, 18 unhashable TypeErrors on predecessor, 18 SCHEMA+MISSING on candidate.

Self-contained fixture. Historical source32/38 archives, manifests, and evidence were not rewritten.

## requiredFindings

None.

## Limits / not claimed

Not selected until root assent and lock activation. Not private enumeration implementation 41, reader41, reconstruct, replay, or custody. Not parser-38 / dependency / source re-acceptance. Not runtime-18 product re-verification (parent pin only). Not inventory-27 re-acceptance. Not complete enumeration, resource/security qualification, or M2–M6. Bounded 1537 development controls are not a proof of totality for every input. Combined later acceptance must not waive this unit’s defined-output preservation or the JSON-C no-float law.
