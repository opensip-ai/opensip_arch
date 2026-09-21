# Addendum — 327 Python oracle vs native optional `commandOutcome`

**Standing:** additional finding on the already-written 327 REVIEW. REVIEW.md is **unchanged**. Frozen `native-capsule-projection-checkpoint-327` is **not** edited. Not a 328 review and not optional-outcome coverage.

328 composition setup reported that the 327 Python local prefix inherited original **227** eight-member `PublicationDescriptorV1`, while native shape is current **127** with existing **241** optional `commandOutcome`. Independent check of the frozen 327 extract confirms that split. Native 327 product was **unchanged** for this field. Isolated 328 composition attaches unchanged **265/241** successor `InputWork.shape` (125 profile) to the 327 predicate; 327 original files stay as frozen.

---

## What was verified

Python 327 oracle (`source324/semantic324/trust-capsule-shapes.v1.json`, **64** `$defs`) `PublicationDescriptorV1`:

- **eight** required members: `publicationSchema`, `store`, `revision`, `previousCapsule`, `nativeBefore`, `operation`, `events`, `afterProjection`
- those eight are the **only** properties
- `additionalProperties: false`
- **no** `commandOutcome` property

Native 327 `Definition` enum is **127** names, including `TrustCommandOutcomeV1`. Generated `node_305` (`PublicationDescriptorV1`) keeps the same eight required keys and additionally allows optional `commandOutcome` as `NodeRef` (`node_4`). `check_capsule_projection` calls `shape(Definition::PublicationDescriptorV1, …)` on that native definition. It still performs **no** outcome load (zero I/O), which is correct for this helper.

`capsule-projection327.ndjson` and parent `capsule279.ndjson`: **649** rows, **`commandOutcome` count 0**. Descriptor key union is the eight 227 members plus `extra` on shape-failure rows. Independent replay of a local positive (`original-0`) with a well-formed `commandOutcome` NodeRef, and with a malformed value, both refuse in Python as `additionalProperties` (`'commandOutcome' was unexpected`). The 241 present / malformed-NodeRef distinction is **not** reachable in this oracle.

---

## Limitation, not a 327 native defect

This is a **327 Python-oracle coverage limitation**, not a native `capsule_projection` defect:

1. 327 never claimed to bind `commandOutcome`. 241/265 `InputWork` / `bind_descriptor_raw` remain the outcome owner. Local projection has no store callback.
2. Native 127 already admitted optional `commandOutcome` before 327. 327 did not add or remove that field.
3. The 649/155 Python matches only show that the 227 eight-member prefix agrees with native on **that** corpus. Absence of the key under 227 (property does not exist) is **not** the 241 optional-absent law (property exists, value omitted).
4. A current-127 descriptor with a well-formed optional outcome is **outside** the 327 Python oracle: native shape can accept the extra key; Python cannot. 649 cases therefore **do not** cover present / missing-required-join / malformed / wrong-outcome paths.

328 is the composition that must test those joins. Do not treat 327’s 649 rows as optional-outcome coverage. REVIEW remaining already listed “optional outcomes”; this addendum is the concrete schema/oracle reason.

---

## Verdicts

- [x] **327 oracle-coverage limitation:** Python local prefix is 227 eight-member D; native is 127 with 241 optional `commandOutcome`; 649 corpus has zero outcomes; 649/155 does not cover optional-outcome compositions.
- [ ] **Not** a native 327 product defect, 241/265 outcome-admission review, or 328 approval.
