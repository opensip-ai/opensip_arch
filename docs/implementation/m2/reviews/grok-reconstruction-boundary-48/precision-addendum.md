# Addendum: reconstruct advisory precision (closures, duplicates, causes)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Precision addendum to reconstruction-boundary-48. **Does not rewrite** `advisory.md` / `advisory.json`. **Not** formal reference-49 review. **Not** SOURCE47 or runtime-23 findings.

**Preserved originals:** `advisory.md` **8270** / `fdf5c8391d02cb6e424f9b4893156815054269d23c420381696dafb162a064cf`; `advisory.json` **1859** / `a4fd19d0ef90e4953019543d37fa2478094ecd2ca1ae2f2dc756067b76a73b40`. Re-hashed after this file was written.

Candidate 49 (unselected): one-line `closures={key:objects[key][1] for key in plan['semanticClosures']}` vs selected I line 94. Predecessor **17578** / `021cc9ac…ba8b` = selected I. Candidate **17561** / `4b2999ca478cdf8959ab031b6cff951aeebe2af0fd659fc529d00a0f2584c769`. Corpus `cases.ndjson.xz` uncompressed **63336841** / `8fb1ff9a0afb6d6a8b81f255c7124763dad2e6ed8cdfd91291814ec96a04b7af` (**73** cases).

## Independently verified

**1. Closure-map-only difference on admitted originals.**  
73 cases: **52 ADMIT / 21 REFUSE**. **35** before≠expected, **38** unchanged. All 35 diffs are **only** `normalized.closures` and `evidence.closures`. The **17** `*-original` ADMIT packets (all except `candidate-forbidden-fact-authority-original`) differ solely on those maps. Independent recompute of `packet-0-original`: selected I ADMIT with 4 closure keys; candidate ADMIT with 3 keys equal to `plan.semanticClosures`; `pred==before`, `cand==expected`. Named-only packets are unchanged (already Plan-selected). Ambient-extra packets change only by dropping the extra closure.

**2. Duplicate inventory is not a reachable ADMIT / doubled `inventoryRowCount`.**  
All **18** `*-duplicate-inventory` variants refuse **before** population/counting:

`EVALUATOR_ENUMERATION_JOIN:ENUMERATION_INVENTORY_DUPLICATE`

I **103–104** calls `ENUM.admit_enumeration` first. ENUM **892–893** (`enumeration_model.v1.py`): after schema, `key=(cellOrdinal,programOrdinal,kind)`; `if key in seen_inv: _add(ENUMERATION_INVENTORY_DUPLICATE)`. Independent recompute of `packet-0-duplicate-inventory` matches that string on both predecessor and candidate. The advisory’s ADMIT/doubled-count prediction is **not reachable** on these valid inputs (duplicate locator rows, not merely duplicate ref list after unique locators). **Still do not silently dedup** the occurrence list: hiding duplicates would skip this ENUM refusal. Incoming-search duplicates are a **separate** case: `incoming-duplicate-incoming` **ADMIT**s with two attestations (`incoming_n=2`); independent recompute matches.

**3. Execution-cause projection.**  
Selected I **50–52**:

```python
if cause not in M.SCHEMA[...]['sources']['execution']:
    if cause not in (None,'source-syntax-invalid'):
        raise C.AdmissionError('EVALUATOR_EXECUTION_CAUSE_UNREGISTERED')
    cause='required-cell-unsatisfied'
```

**Only** unregistered `None` / `source-syntax-invalid` map to `required-cell-unsatisfied`. Any **other** unregistered cause raises `EVALUATOR_EXECUTION_CAUSE_UNREGISTERED`. The original table’s “unregistered (except None / source-syntax-invalid) → required-cell-unsatisfied” **inverts** that `except`.

## What stands from the original advisory

- Invoke 47 first; named maps; no store census in **Rust**.
- Candidate 49 **is** the I closures correction (Plan `semanticClosures`); not selected by this addendum.
- Preserve inventory occurrence lists so ENUM duplicate remains visible.
- `atom_inputs.blobs` wholesale remains inert for current atom_model.
- Remaining reconstruct obligations (population, rule enumerations, causes, observation joins, evidence absence, target uniqueness, counts) still beyond 47.

## Limits

Not formal 49 selection. Not 47/runtime-23 findings. Root may package reference-49 separately.
