# Advisory: E39 schema-failure tracking totality

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded independent advisory of selected E39 `admit_enumeration` schema-failure tracking. **Not design-unit selection. Not product, kernel, reader, source, or M2 approval.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-totality-42/`. Probes and this review only. No live/frozen/history/product/architecture writes.  
**Preserved prior work:** reader41 advisory remains frozen at `m2-grok-enumeration-reader-41/review/advisory.md` **7297** / `990a0eddc4c0eaff917160859a87bda769fd4b05d8953249d402de6f6d141619` and `advisory.json` **1696** / `6572c319004fbcddc5835e344e5f47893890dd9e8f496c64c3e531dc69e7f736`. Not reopened. wH independently checks the kernel; this review is reference totality and locator type semantics.

## Verdict

**PRESERVE-DEFINED-OUTPUTS; CANDIDATE-SOUND-AS-TOTALITY-CORRECTION-NOT-SELECTED.**

Selected E39 is not total: 18 schema-invalid subject-inventory locators whose `cellOrdinal` / `programOrdinal` / `kind` is JSON-C array or object raise raw `TypeError` while hashing `schema_failed`. The required correction is totality **without** a silent switch of already-defined refusal outputs.

Root’s private candidate **50678** / `a02960c631df0f0342f039fcef395dbba402d67453dbc9aba760fad0e6719d5c` is the minimal sound totality patch: wrap failed-locator membership/`set.add` in a narrow `TypeError` catch, treat unhashable locators as non-occupying, keep SCHEMA then MISSING, and keep Python scalar locator equality (`False==0` / `True==1`) on the schema-failed path. Independent replay: all **1423** previously defined mutation outputs unchanged; all **45** boolean diagnostic outputs unchanged; the 18 former exceptions become `ENUMERATION_INVENTORY_SCHEMA` then `ENUMERATION_INVENTORY_MISSING_RECORD`.

This advisory does **not** select that candidate as a reference unit. Formal selection is a later named review. Tightening `schema_failed` to `C.equal_typed` / `type is int` / Rust `JsonValue` distinctness is a **second, named law** that would change False occupancy from SCHEMA-only to SCHEMA+MISSING. Do not fold it into this totality patch.

## Scope

| In | Out |
| --- | --- |
| Selected E39 `schema_failed` hashing vs arbitrary JSON-C locator fields | Product / architecture / frozen evidence edits |
| Exact refusal order SCHEMA then MISSING | Kernel join approval (wH) |
| Python bool/int locator equality vs typed locator | Reader41 reopen |
| Preserve defined E39 outputs vs typed tightening | Design-unit selection of the candidate |
| Independent reproduction in this directory | Parser-38, reconstruct, full M2 |

## Pins

Selected E39 (trial41 overlay, same bytes as integer-profile selection):  
`/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/archroot/docs/coop/design-corrections/foundation/enumeration_model.v1.py`  
**50447** / `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992`.

Private candidate (not selected):  
`/tmp/opensip-implementation/m2-enumeration-totality-candidate-42/enumeration_model.v1.py` and the overlay copy under that tree’s `reference/archroot/.../enumeration_model.v1.py` — identical **50678** / `a02960c6…719d5c`. Predecessor copy is byte-identical to selected E39. Account: **620** / `b0bf7720d63c83512f3f5095e103f9da3a823e486f32bad51dbbe80b6c774eeb`. Comparison: **402** / `55b382a6ae7385e58ac9a22b071dbcbac0324e9759574b6d93bcbb06deb7df5e` (`1537` cases, `1519` unchanged defined, `18` former TypeErrors now refuse, `0` mismatches).

Mutation corpus: `cases.ndjson` **13081472** / `d3153ccd18edddab9bb5792fb8435b07041646641cb0704dc30c09f7fec9d2ab` — **1423** cases, **16 ADMIT / 1407 REFUSE**. The 18 array/object locator labels are **absent** (oracle could not compute). `oracle-exceptions.json` **2394** / `49457f37acfa34bcc8a4a8dd11fcbeed236a69dd5cb8eb0afba57b804906c8f3`. Kernel mutation result **993** / `0d31d2a1d1b1ee44ff951c68dcde177f14bbe749236b77259d96817b046d8529` records those 18 as preserved oracle exceptions.

Boolean diagnostic corpus: **45** cases, **590293** / `c5e06c21d7905e788a03fb66bf45e1b408a309c35ef6379146aa4aac88049d6e`. Initial typed-kernel difference exit 101; later boolean-check result **161** / `a2a8ee01f87961c0687a9895324e3f15cf9e52d230255ec521cf8e2f3eccfbc8` (45 pass after schema-failed Bool alias). Used here as type-semantics evidence, not kernel approval.

`canonical.py` `equal_typed` **8995** / `ad88e58fe90fe66531dbe39f4694f20ad3bc6ce2099ae4fc762c0251468496f7`.  
`subject-inventory.schema.v1.json` **16861** / `6ab46925853d26c1a5f7ae1fbd69db5dcc9052fdefdb1b265e53481b4e1cee33` — `cellOrdinal` / `programOrdinal` exact integer `minimum` 0; `kind` enum string.

Reference supplement (trial41): **950** / `1d4794a14e87c0b71738dce23d94720c3027673a3484d2d47fe4fa2413ddede7`. Overlay files present and matching: `target-attribution.schema.v1.json` **13480** / `788bd9d000fb1da830ef368d14c119f441f7b60e8a56f8da3467ef0fbf0ed90e`; `v2` **23086** / `bd938f11c584be65e914bc1446193fdf3dd4a15f7b78630cc3eb628c5bca1d53`. Source32/38 unchanged. Probes loaded E from the trial41 overlay (selected) and candidate overlay (candidate) so `HERE`-relative schemas resolve.

Integer-profile gate remains at import: both `sys.flags.int_max_str_digits==0` and `get()==0`, else `ReferenceEnvironmentError`. Confirmed: same interpreter without `-X` raises that error (`flags=4300`). All probes used:

```
/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0
```

CPython 3.12.13. `python` → `cpython-3.12-macos-aarch64-none`.

## Commands (this directory only)

```
/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0 \
  /tmp/opensip-implementation/m2-grok-enumeration-totality-42/probes/probe_totality.py

/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B -X int_max_str_digits=0 \
  /tmp/opensip-implementation/m2-grok-enumeration-totality-42/probes/repro_schema_failed.py
```

Probe outputs: `probes/totality-result.json` **63517** / `6a550e3a36527b496ded9cb2dca2fb212a191d0a05a4e787941a4969668337f0`; cleaned `probes/repro-result.json` **30566** / `2e33bd12f656d8c717d325479155329a1a9de0a33c2d99cd4f1e477ac698d3b8` (18 TypeErrors on selected E39). Scripts: `probe_totality.py` **5bc20c4c…eed67**; `repro_schema_failed.py` **3196f012…922dd**.

Independent probe totals: oracle 18/18 TypeError message match; candidate 18/18 `REFUSE` `[SCHEMA, MISSING]`; defined mutation replay 1423/1423 selected and 1423/1423 candidate; boolean 45/45 both; candidate `formerly-unhashable-*` 18/18.

## Selected-E39 hole

After `INV_SCHEMA` failure, E39 **878–883** does:

```python
loc = (inv.get("cellOrdinal"), inv.get("programOrdinal"), inv.get("kind"))
if loc in binding_by:
    schema_failed.add(loc)
```

`binding_by` / `expected_keys` are tuples `(cell_index:int, program_ordinal:int, kind:str)` from admitted plan cells (**863–864**). Later (**1022–1024**):

```python
for key in expected_keys:
    if key not in seen_inv and key not in schema_failed:
        _add(faults, "ENUMERATION_INVENTORY_MISSING_RECORD")
```

`_add` appends first-seen order (**226–228**). SCHEMA is recorded in the `except` before this loop, so defined dual refusals are always SCHEMA then MISSING.

Purpose of `schema_failed`: a schema-invalid inventory that **still names** an expected slot must not also emit MISSING. That is why `inventories[0].schemaVersion` array/object/True is **SCHEMA-only** — locators remain `(0, 0, "file")` and occupy the slot. Confirmed on baseline-0 for both selected and candidate.

JSON-C array/object locator fields make `loc` unhashable. `loc in binding_by` raises `TypeError: unhashable type: 'list'|'dict'`. Matrix: baselines 0/14/48 × `{cellOrdinal, programOrdinal, kind}` × `{array, object}` = the 18 oracle rows. Independently reproduced, messages identical to `oracle-exceptions.json`. Those labels are not in `cases.ndjson`.

Other inventory array/object mutations (schemaVersion, planId, …) stay in the corpus as REFUSE because locators remain hashable.

Valid-schema locators never take this path: `key = (inv["cellOrdinal"], inv["programOrdinal"], inv["kind"])` runs only after `C.validate(INV_SCHEMA, inv)`. INV_SCHEMA rejects bool/float/array/object for those fields. Bool/float occupancy is therefore **schema-failed tracking only**, never ADMIT.

## Python equality versus typed locator

On this interpreter:

| Comparison | Result |
| --- | --- |
| `False == 0` / `True == 1` | True |
| `hash(False) == hash(0)` | True |
| `(False, 0, "file") == (0, 0, "file")` | True |
| `(True, 0, "file") == (0, 0, "file")` | False |
| `(True, 0, "file") == (1, 0, "file")` | True |
| `0.0 == 0` / `1.0 == 1` | True |
| `C.equal_typed(False, 0)` / `(True, 1)` / `(0.0, 0)` | False |
| `type(False) is int` | False |
| `isinstance(False, int)` | True |

`C.equal_typed` (**canonical.py 86–93**) requires `type(a) is type(b)`. Rust `JsonValue` distinguishes Bool / Integer / Float. Kernel `number()` accepts `V::Integer` only. Valid inventory parsing therefore never treats bool as int.

Mutation corpus `bool` on locator fields is JSON `true` (`True`), not `False`. Defined True outputs are SCHEMA+MISSING because True occupies slot 1, not expected 0 — **the same refusals typed law would produce for True**. False is **not** in the 1423 defined mutation cases.

False **is** now explicit in the 45-case boolean diagnostic: `cellOrdinal:False` and `programOrdinal:False` on baselines 0/9/14 are SCHEMA-only (Python occupancy of slot 0). `kind:False` is SCHEMA+MISSING (`False != "file"`). Selected E39 and the TypeError-catch candidate both produce those outputs. A typed `schema_failed` (require `type is int` / `C.equal_typed` / no Bool alias) would change the six False numeric cases to SCHEMA+MISSING. That is a semantic switch, not totality.

Initial kernel boolean diagnostic failed exactly there: typed locators emitted SCHEMA+MISSING where the Python oracle expected SCHEMA-only (cases 0, 5, 15, 20, 30, 35). Later kernel `failed_locator` aliases `Bool(false)→0` and `Bool(true)→1` **only** on schema-failed rows. That matches selected E39 Python membership. It is cited as type-semantics evidence; wH owns kernel review.

## Candidate evaluation (not selection)

Delta versus selected E39 is only **878–888**:

```python
try:
    if loc in binding_by:
        schema_failed.add(loc)
except TypeError:
    # JSON-C array/object locator fields cannot name a binding.
    # Keep the schema refusal and allow missing-record accounting.
    pass
```

No other AST change. Consequences:

1. **Totality:** array/object locators no longer throw. They cannot name a binding, so they do not enter `schema_failed`. Expected slots stay missing → SCHEMA then MISSING. Same order as defined True/null/string/negative locator refusals.
2. **Defined outputs preserved:** independent replay of all 1423 mutation cases matches expected `result` and `refusals` on both selected E39 and the candidate. schemaVersion-array SCHEMA-only preserved. True SCHEMA+MISSING preserved. Ordinal `127` remains UNEXPECTED+MISSING (schema-valid integer, success path, not `schema_failed`).
3. **False occupancy preserved:** SCHEMA-only on numeric False locators. No silent typed switch.
4. **Candidate corpus extras** (not previously defined mutation labels): 51 `original-*` rows plus 18 `formerly-unhashable-*` rows plus 45 boolean rows = 114 extras on 1537. The 18 formerly-unhashable rows independently match SCHEMA+MISSING.

This is the minimal correction that makes tracking total **and** preserves previously defined reference outputs. Alternatives that type-narrow occupancy (`type(x) is int and type(k) is str`, or `C.equal_typed` against `expected_keys`) would also stop the TypeError, but they would change False (and `0.0`) occupancy relative to selected E39. Reject those as *this* totality patch.

## Recommendation

**Keep previously defined reference outputs. Apply the narrow TypeError totality wrap. Do not silently adopt typed locator occupancy.**

Law for a successor reference unit, if later selected:

1. `admit_enumeration` must return a defined REFUSE for every JSON-C locator field value. Raw `TypeError` / `ValueError` is not a reference answer.
2. Unhashable locator fields (array/object) do not occupy `schema_failed`. Refusal is SCHEMA then MISSING when that inventory was the occupant of an expected slot.
3. Hashable schema-invalid locators keep selected E39 Python tuple membership: `False` occupies `0`, `True` occupies `1`, intact integer/string locators occupy their slot (schemaVersion-array SCHEMA-only). Valid rows still use INV_SCHEMA exact types; bool never ADMITs.
4. Refusal order remains first-seen `_add`: SCHEMA recorded at schema failure, MISSING appended later if the expected key is in neither `seen_inv` nor `schema_failed`.
5. Typed tightening (`C.equal_typed` / `type is int` / no Bool alias) is **not** this correction. If wanted, name a new unit, publish the six False numeric output changes, and select that unit separately. Combined later acceptance must not waive the original defined outputs.

Residual JSON-C number alias, not a TypeError hole: Python `0.0 == 0` so `cellOrdinal: 0.0` is SCHEMA-only on both selected E39 and the candidate (hashable). `C.equal_typed(0.0, 0)` is False; kernel `number()` rejects Float. Float locators are absent from the 1423 and 45 corpora. If Python membership remains the selected schema-failed law, kernel matching cannot alias Bool while leaving integral floats typed — that split would recreate the initial False diagnostic on `0.0`. Either extend schema-failed occupancy to Python’s remaining hashable numeric aliases, or change False and `0.0` together in a named typed successor. Do not treat the split as an accidental side effect of totality.

## Not claimed

- Design-unit selection or installation of candidate `a02960c6…719d5c`.
- Product, kernel, reader, reconstruct, parser-38, or M2 approval.
- Reopening reader41.
- Approval of unprovided corrections other than the evaluated private candidate.
- That typed locator occupancy is already selected law. It is not: selected E39 and the 45 boolean diagnostics encode Python equality on `schema_failed` only.
