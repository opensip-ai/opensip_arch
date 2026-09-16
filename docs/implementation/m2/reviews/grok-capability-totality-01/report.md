# Independent Grok advisory: capability-manifest total-refusal correction

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Bounded reference-only patch of `admit_capability_manifest`. **Not formal selection. Not CVE1 codec selection. Not Unicode/NFC. Not live/frozen/history edit.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-capability-totality-01/review`.

## Standing

Original selected native `native_evidence_model.v2.py` `7d1c0acf…b8be` / 319376 bytes is identical in architecture and in the recognition-derived overlay actually loaded at `/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01/archroot/docs/coop/design-corrections/native`. Candidate `e6784aa1…e2b9` / 319944 bytes. Account predecessor/candidate hashes match.

Root is implementing a separate pure CVE1 codec and full Unicode 16 conformance. This review does not select those.

## Verdict

**NOT SELECTION.** The proposed fix is **sound for the stated crash totality** in this one function.

Independently: the recorded 19 cases are real. Golden ADMIT. The other 18 are AttributeError/TypeError, **not** typed REFUSE. Candidate turns those 18 into closed/type REFUSE, keeps golden ADMIT and the same `capabilityManifestId`, and does not invent a language/provider/schemaVersion registry. AST of every other top-level function is identical (143 unchanged; only `admit_capability_manifest` changed). CVE1 encode/decode/read, capability-manifest identity recipe, and gate-vector helper are byte-identical as functions.

Remaining diagnostic (not a crash): a mixed-type ordered collection that also duplicates strings reports **only** the type refusal; `strict_unique` skips order when any element is not `str`. That matches the candidate comment. It is not a reason to reject the crash fix.

## Original faults (independent)

Re-ran the overlay model through CVE1 encode of the same 19 values as `original-probe.py`. All 19 match `original-reference-faults.json` (`8b07990b…7d84`) exactly, including exception type and message. Faults were **not** relabelled.

| Class | Count | Actual original |
| --- | ---: | --- |
| golden DCM-1-core | 1 | ADMIT, id `508f24c7…8881b` |
| non-map root (`None`/`False`/`True`/`0`/`'text'`/`[]`) | 6 | `AttributeError`: `*.get` |
| `platformIds` mixed with non-str (`False`/`0`/`[]`/`{}`/`None`/`['file']`) | 6 | `TypeError` from `sorted` (`<` across types) |
| `AbsentCapability.relationIds[]` non-str | 6 | `TypeError`: `sorted` or unhashable `set` element |

Cause in the original function:

1. `value.get("schemaVersion")` before a map check.
2. `strict_unique` does `sorted(values)` / `set(values)` after element type faults are recorded.
3. `relations.add(relation)` on absent ids **before** a string type gate.

## Proposed fix

Three local changes inside `admit_capability_manifest` only:

1. Non-dict root: `closed(value, "CapabilityManifestV1")` then REFUSE (`capability.adm-closed:CapabilityManifestV1`) before `.get`.
2. `strict_unique`: return without sort/hash if any element is not `str` (type already recorded at `platformIds[]` / filtered provider keys).
3. Absent `relationIds[]`: `type is str` **before** `relations.add` and membership.

Candidate 19: 1 ADMIT + 18 REFUSE, **0 exceptions**. Refusals are the existing ADM-CLOSED / ADM-TYPE codes, not a new vocabulary.

Widened cases (not in the original 19):

| Case | Original | Candidate |
| --- | --- | --- |
| language `cobol` (OPEN) | ADMIT | ADMIT |
| providerId arbitrary (OPEN) | ADMIT | ADMIT |
| schemaVersion `2` (OPEN value; type still int) | ADMIT | ADMIT |
| profile `not-core` (OPEN as registry; custody separate) | ADMIT | ADMIT |
| `schemaVersion=True` | REFUSE type | REFUSE type |
| mixed `platformIds` `[all-supported, False]` | TypeError | REFUSE `platformIds[]` |
| mixed duplicate `[all-supported, False, all-supported]` | TypeError | REFUSE type only (no `adm-order`) |
| empty `platformIds` | ADMIT | ADMIT |
| mixed absent `[file, 0]` / `[file, ['file']]` | TypeError | REFUSE `relationIds[]` |
| duplicate absent `['file','file']` | REFUSE order | REFUSE order |
| extra root key | REFUSE closed | REFUSE closed |
| `platformIds` not a list | REFUSE type | REFUSE type |

`declaredOPEN` still lists schemaVersion, profile, providerId, language (provider and absent). Candidate does **not** add membership checks on those positions. Profile custody (DL-CUST-3) remains outside this function.

## What did not change

- CVE1 encode/decode/read AST identical (root is implementing a separate codec; this patch does not touch it).
- `capability_manifest_identity` recipe identical (`opensip.capability-manifest.v1` + NUL + bytes).
- Gate-vector helper identical.
- 143 other top-level functions identical; no added/removed names.
- Closed record shapes, relation/platform/deficiency/coverage registries, and all-string order law still fire when types are strings.

## Reproduction

```
/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B \
  /tmp/opensip-implementation/m2-grok-capability-totality-01/review/probes/run_review.py
```

Results: `review/results/probes.json`.

## Coordination

Did not edit frozen native, live product, architecture history, graph06, or commits. Unicode NFC advisory remains in its tree; a tinyvec_macros crate-kind correction was **appended** there without rewriting the original Unicode report text.
