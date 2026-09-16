I've adopted your encoding-independent grammar exactly, and none of my controls found a counterexample. The v2 UTF-8-only restriction was an unnecessary narrowing and is withdrawn. My v2 argument against a NUL guard was wrong: it judged `instr` on its own and ignored the hex check that stays in the conjunction, which already refuses multibyte and malformed characters. This is still not acceptance: all 54 product recovery cases (F00–F53) remain not-executed, and these are in-memory SQLite checks only.

**The confirmed problem with v2.** Your captured files are byte-identical to my final v2 DDL and attempt-custody schema. Those bytes admit no hostile value in any encoding, but they refuse every lawful row in UTF-16le and UTF-16be databases: 42 over-refusals in each.

**Full-conjunction check.** I ran the v2 matrix (28 columns, 341 variants) in all three encodings. On top of that I added UTF-8 and UTF-16 specific hostile values on the hex columns: overlong NUL, surrogates, a NUL code unit, and fullwidth or Arabic-Indic digits. Values are read back as raw bytes and decoded in the database's actual encoding.

| DDL | UTF-8 | UTF-16le | UTF-16be |
|---|---|---|---|
| frozen37 | 165 holes | 121 holes | 121 holes |
| v2 | exact | 42 lawful rows refused | 42 lawful rows refused |
| your alternative | exact | exact | exact |
| **v3** | **exact** | **exact** | **exact** |

"Exact" means no hostile value admitted, no lawful value refused, and your counterexamples refused. Valid affinity conversions, such as text `'5'` stored as integer 5, are admitted as lawful.

**Every part of the conjunction is necessary.** On synthetic single-column tables:
- only the complete conjunction is exact in all three encodings;
- the v2 byte-length form and BLOB-instr are exact in UTF-8 but refuse every lawful UTF-16 value;
- `instr` with only `typeof` admits uppercase and non-hex values;
- removing `typeof`, length, `instr`, the hex check or the prefix check each admits hostile values.

**What changed.** Each `length(CAST(c AS BLOB)) = N` became `instr(c, char(0)) = 0`: seven in the carrier DDL, three in the attempt-custody DDL. The DDL statements are identical to your substitution applied to v2 (comment lines aside), and the attempt-custody DDL matches it exactly. In the prose, dispatch record and private DDL note:
- the UTF-8 assumption, the "fails closed" justification, the `encodingAssumption` dispatch key and "no lawful row is refused" are removed;
- storage class is now described accurately: explicit `typeof()` on integer, free-text and hex columns, and exact enumeration on `record_type`, `platform`, `phase` and `settled_outcome`;
- carrier-format §5.1 records the v1 → v2 → v3 history.

The storage-class, publication and `first_generation` laws, the object names and the historical scope are unchanged. v1 and v2 are left intact, with their failures kept.

**Recovery routes are unchanged.** Only the dispatch grammar record changed. S12, the read-only doc, migration, lineage and the route table are byte-identical to v2. All nine routes still pass both StepTermination schemas and are D9-legal.

**Checks:**
- **Owner validator:** frozen37 87/0, v2 247/0, v3 362/0 (177 storage checks).
- **New checker controls:** every column in all three encodings; UTF-16le and UTF-16be carrierFormat 2 carriers migrate, publish, admit a lawful SEAL, and still refuse NUL and BLOB values.
- **Discrimination** (v3 checker over mixed trees; all 12 expectations met):
  - v2 DDL restored: 301/61, failing only on UTF-16 lawful admission, the UTF-16 migration and the byte-length structural check, with no UTF-8 failure;
  - frozen37 DDL restored: 289/73;
  - frozen37 routes restored: 357/5.
- **Kept failure:** my first routes/drift/wording receipt exited 1 because its wording scan flagged the checker's own assertion that `encodingAssumption` is absent. I reran it with only that line reclassified, and everything else had already passed. Separately, before any run, I removed a stray tab-indented line from the ablation probe that would have raised `TabError`.

**Changes and bindings:**
- **Changed since v2:** 5 of the nine files: DDL, carrier-format, dispatch, checker, attempt-custody.
- **Bindings awaiting rebind:** the same set as v1/v2: manifest pins on all 9, normative-inputs v5 on 8, 8 coverage sources, 5 pin ledgers. There is no new planning drift.
- **Custody:** frozen37, the v2 runtime and your review files are unchanged.

**Limits:**
- **SQLite version:** encoding independence was observed on SQLite 3.50.4 only. That `instr()` and `char()` exist since 3.7.15/3.7.16 comes from release history, not testing.
- **UTF-16 migration:** the control covers one inherited carrier shape per encoding.
- **Oracle:** the oracle is my reading of the owner patterns, and the hostile set is finite.
- **Enumerated columns:** they rely on whole-value comparison, with no explicit `typeof`.
- **Suites not run:** no reference groups, pins, planning checker or package verification; drift was computed.

All subprocesses ran in the foreground and have finished.

Files are in `/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3/`:
- review.md (`da06472e…`)
- review.json (`74e75a14…`, full before/after hashes)
- proposed-edits.diff (frozen37 → v3, `f7ff95c4…`, 1426 lines)
- v2-to-v3.diff (`8495dadb…`, 446 lines)
