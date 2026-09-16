Root's two SQLite holes are real, and the gap was wider. I've fixed it for every column in the v2 disposable copy. Root's DDL is byte-identical to my v1 final DDL. These are DDL admission counterexamples; host record admission remains separate. This is not acceptance: all 54 product recovery cases (F00–F53) remain not executed, and these are in-memory SQLite reference checks only.

**What was actually admitted.** In SQLite, `length()` and `GLOB` stop at an embedded NUL, and a TEXT column keeps a BLOB as a BLOB. I probed 28 columns with 341 variants: every lawful value must be admitted, and no admitted row may store a value outside its column's grammar.

| Tree | Holes | Lawful values refused | Root's counterexamples |
|---|---|---|---|
| frozen37 | 105 | 0 | admitted |
| v1 final | 49 | 0 | admitted |
| **v2** | **0** | **0** | **refused** |

The 49 v1 holes break down as:
- **All 10 hex columns**, not just the three root named: NUL suffixes, and ASCII-hex BLOBs.
- **Five free TEXT columns** accept BLOBs: `request_ref`, `token`, `install_generation_id`, `body`, `namespace_id`.
- **`first_generation` and `grantGeneration`** accept a non-integer REAL such as 2.5.

**The remedy.** Every column in the v3 carrier DDL and the private attempt-custody DDL now declares its storage class with `typeof()`. Every hex column must additionally satisfy `length(c) = N` and `length(CAST(c AS BLOB)) = N`, then its prefix and hex check. Character length stops at a NUL and byte length doesn't, so the two agree only for a NUL-free ASCII value.
- **Why no lawful row breaks:** CHECKs see values after SQLite's type conversion, so an integer supplied as text `'5'` is still admitted.
- **Enumerated columns (`record_type`, `platform`, `phase`, `settled_outcome`) are unchanged:** they were already exact.
- **Encoding:** byte lengths assume UTF-8, the SQLite default. A UTF-16 database refuses every hex row, which fails closed.
- **STRICT tables were rejected:** they don't catch an embedded NUL. Per SQLite's documentation (not tested here), older SQLite libraries can't read a database containing one, which would break the rule that a format-unaware core still reads history.
- **Historical carriers:** the frozen v1/v2 carrier bytes are untouched and still admit these values. That is disclosed, not repaired: historical rows can never satisfy a schema-3 SEAL join.

**Wording correction.** Reference SQLite instances were created from the earlier v3 bytes, so the claim that they were "never instantiated" was wrong, as was calling the v1 grammar exact. Both claims are corrected in the DDL, carrier-format §5.1, the dispatch record and the attempt-custody note. The claim is now scoped to product: no product implementation or deployed carrier was created from the earlier bytes, and those reference instances and receipts stay as history. A carrier built from earlier bytes is refused `MIGRATION.CORRUPT` by the definition check. The v1 report is left as-is; the new report states exactly which of its claims are superseded.

**Routes are unchanged.** No contradiction came up. S12, the read-only doc, carrier-migration, store lineage and the route table are byte-identical to v1. All nine routes still pass the current and the R1/R2 StepTermination schemas and are D9-legal.

**Checks:**
- **Owner validator:** 247/0 on v2, including 62 new storage checks; v1 final still reproduces 201/0.
- **Discrimination** (v2 checker over mixed trees):
  - v1 DDL restored: 226/21, and only storage checks fail;
  - frozen37 DDL restored: 211/36, storage, publication and scenario checks fail;
  - frozen37 routes restored: 242/5, only route-row checks fail.

**Failures along the way (all receipts kept):**
- **First matrix run on frozen37:** crashed reading back an admitted invalid-UTF-8 value.
- **Byte-safe rerun on v2:** crashed because the new DDL correctly refused the UTF-16 setup row.
- **Next version (three runs):** failed on a missing import.
- **First discrimination run:** failed because my new invalid-definition check anchored on text that only exists in the v2 DDL. I fixed the checker so it works on every DDL revision; the rerun meets every expectation.

**Changes and bindings for root:**
- **Changed since v1:** 5 of the nine files, namely the v3 SQL, carrier-format, carrier-dispatch, check-carrier-v3 and the attempt-custody schema.
- **Bindings awaiting rebind:** the same set as v1: manifest pins on all 9, normative-inputs v5 on 8, 8 coverage sources, 5 pin ledgers. v2 adds no new planning drift.
- **Custody:** frozen37, the v1 runtime and the retained v1 copy are unchanged.

**Limits not stated above:**
- **Pre-existing UTF-16 carriers:** one could not be migrated without a reviewed successor. None is known.
- **Namespace length:** `namespace_id`'s length check counts characters only up to a NUL, so the record's own length rule governs.
- **Oracle:** the grammar oracle is my reading of the owner patterns.
- **Suites not run:** no reference groups, pin verification, planning checker or package verification; drift was computed, not executed.

All subprocesses ran in the foreground and have finished.

Files are in `/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/`:
- review.md (`7482c5cd…`)
- review.json (`557da06d…`, full before/after hashes)
- proposed-edits.diff (frozen37 → v2, `21654ca7…`, 1360 lines)
- v1-to-v2.diff (`b7c628d1…`, 556 lines)
