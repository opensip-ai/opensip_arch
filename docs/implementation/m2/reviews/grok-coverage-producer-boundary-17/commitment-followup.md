# Follow-up: producer commitment call trace (advisory 17 obligation 2)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Correction of advisory-17 producer obligation 2. Original advisory and carrier follow-up bytes **unchanged**.
**Work:** existing private review tree only. No live/frozen edits. Root implements the **selected** boundary, not descriptor-construction conflation.

## Disposition

Advisory 17 obligation 2 **over-attributed** `subject_scope_descriptor` (1499–1522) to producer-local `subject_scope_commitment` (1530–1542). Root’s call-trace is confirmed on selected functions.

`admit_coverage_result_v3` (1557) calls **only** `subject_scope_commitment`. That helper calls `subject_scope_identity` (1537) → `IM.identifier` (1527). It does **not** call `subject_scope_descriptor`. Ladder/duplicate **construction** refusals are therefore **not** producer-local commitment behavior. Unregistered `(relation, rung)` at the producer is **RC-0** via `coverage_bijection` on the **entry** (1573, 1408–1409).

## Exact call trace

```
admit_coverage_result_v3(payload, scope_descriptor, unresolved_facts, …)   # 1545
  validate_native("CoverageResultV3", payload)                             # 1556
  subject_scope_commitment(scope_descriptor)                               # 1557 → 1530
    subject_scope_identity(descriptor)                                     # 1537 → 1525
      IM.identifier("subject-scope", descriptor)                           # 1527
        C.validate(schema #/$defs/subject-scope)                           # identity 218–221
        ordered(value)   # collection order / uniqueItems; NOT _rung_index
        return "scope2:" + C.identity(...)
    out.scopeId = that prefix form
    out.subjectScopeCommitment = "sha256:" + hex
    out.subjectCount = len(descriptor["subjects"])                         # 1538–1540
    validate_native("SubjectScopeCommitmentV1", out)                       # 1541
  … key/entry/examined joins against that commitment …
  coverage_bijection([dict(entry, examinedSubjects=scope.subjects)], …)    # 1573
    _rung_index(entry.relation, entry.resolution) is None → RC-0           # 1408–1409
```

`subject_scope_descriptor` (1499) **is** the helper that:

- `_rung_index` else `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER` (1513–1514)
- sorts subjects by `C.canonical` (1515)
- duplicate → `SUBJECT_SCOPE_DUPLICATE_SUBJECT` (1516–1517)
- then `validate_foundation("subject-scope")` (1521)

Producer never enters that function.

Identity Run closure **1913–1916** still checks retained-scope ladder via `_rung_index` **before** 1934 admit. That is identity walk, not commitment recompute.

## Probe (selected native, overlay `__file__` for HERE schemas)

`unresolved-edge` ladder is `['observed']`. `_rung_index(..., "enumerated")` is `None`.

| Call | Result |
| --- | --- |
| `subject_scope_descriptor(..., relation=unresolved-edge, rung=enumerated, subjects=["a.ts"])` | `AdmissionError SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:unresolved-edge@enumerated` |
| `subject_scope_identity` / `subject_scope_commitment` on the same schema-valid descriptor | **ok** `scope2:0277ed98…ddea` / `sha256:0277ed98…ddea` / count 1 |
| `admit_coverage_result_v3` with matching CoverageResultV3 (`unknown`, RC `not-applicable`, commitments aligned) | `result=REFUSE`, **`refusals=[]`**, `faults=[{entry: unresolved-edge@enumerated, fault: RC-0: rung is not a member of this relation's own ladder}]` |

Duplicates `["a.ts","a.ts"]`: identity/`commitment` fail schema `uniqueItems` (`ValidationError`), **not** the descriptor ladder string. Descriptor ctor still hits **ladder first** (1513 before 1516). Unordered `["b.ts","a.ts"]`: identity fails `x-opensip-order: canonical-set`; ctor again ladder-first.

So: **rung** construction ≠ producer commitment. **Duplicate/order** may still fail `identifier` schema/order if a host passed a non-admitted descriptor; a retained identity-admitted scope is already unique and ordered. Do not conflate ctor sorting/ladder with commitment.

## Correction to advisory 17 obligation 2

**Replace** the bullet that listed `_rung_index` 1513–1514 and duplicate 1516–1517 under `subject_scope_commitment`.

**Selected producer commitment is:**

- `identifier` schema + collection order (identity 218–221)
- `scope2:` / `sha256:` respelling of the same hex (1537–1539)
- `subjectCount = len(descriptor["subjects"])` (1540)

**Selected producer ladder check is:** `coverage_bijection` RC-0 on the **entry** (1573 / 1408–1409), after commitment joins. Empty-ladder fallback remains forbidden there.

Do **not** implement producer-local `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER` by calling `subject_scope_descriptor`. Root implements the selected boundary.

## Original bytes (unchanged)

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `advisory.md` | 14107 | `30ea10dc0f3708ce0ba975072d31f595e1f018f50a752562bf29e7e7ba209ac4` |
| `advisory.json` | 3439 | `236f88e236a15ce275891af813a78a0f3542e350610137c337a5e5b2b557f758` |
| `followup.md` | 6660 | `601f73da05d9c0e11e53910fc24ee0abd58a9e7aa23bffc23bfff6c0cba29e20` |
| `followup.json` | 2135 | `c21e0b880b9937087d9369721019d021b2925fe29da89265944dcad3be9d436f` |
