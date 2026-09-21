# Addendum — extract `edge_limit=0` comparison

**Standing:** correction of the independent Python extract comparison in 313 REVIEW §3 / remaining-table note. Does **not** edit `REVIEW.md`. Does **not** reopen the native 313 verdict. Not a 312 helper or native codec defect.

---

## What was wrong

REVIEW stated that 36 extract rows with native `limit=0` (`edge-budget`) were accepted by the 312 Python `extract` helper, and treated that as “Python successor extract does not latch `edge_limit=0`.”

That comparison used:

```python
int(r.get("limit") or 131072)
```

In Python, `0 or 131072` is `131072`. The helper was therefore invoked with the **default** budget, not `0`. Frozen 312 `extract` takes keyword `edge_limit` and requires `0 <= edge_limit <= 131072` and `len(rows) < edge_limit` (`Refusal: edge-budget`). Passing `edge_limit=0` refuses the first edge.

This was a **review-call error**, not missing enforcement in the helper.

---

## Corrected replay

Reproducible script (review-local only; frozen fixtures not overwritten):

`/tmp/opensip-implementation/reviews/grok-native-provenance313-20260920-r1/replay_extract_limits.py`

It sets `edge_limit = int(row["limit"])` when the key is present, including `0`.

| Check | Result |
|---|---|
| Extract rows | 415 |
| Replayed (hex body) | **414** |
| Repeat-only skipped | 1 |
| Matched fixture `valid` | **414 / 414** |
| Mismatch | **0** |
| First `limit=0` row | Python **refused** `edge-budget` (fixture `valid: false`) |

Evidence: `grok-out/io/extract-limit-replay.json`. The earlier `fixture-replay.json` (36 mismatches) is the buggy-call receipt; it is not a helper result.

Independent decode **566/566** and owned-root record extract **212/212** from that earlier run are unaffected (they do not use `limit`).

---

## What still stands

Native 313 verdict, 253/2 ignored, 16 mutants, host 8/8 schema-2 assembly, and “locator is not admission” stand. Do **not** claim the 312 Python helper ignores `edge_limit`.

No code, schema, or frozen-source edits.
