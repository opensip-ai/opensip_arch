I’ll finish the remaining v10 joins in the same five files: require partial inventories to keep every known named package when a sibling manifest is malformed, catch native `AdmissionError` on bad boundaries, and put receipts in v11.I’ll add the named-row retention join, catch native `AdmissionError` on bad boundaries, and extend the v11 checker with those controls.v11 finishes the remaining v10 joins in the same five isolated files. Enumeration-join checks only; this is not Run qualification.

**Checker:** `/tmp/opensip-architecture-review-env/bin/python -I -B check-enumeration.v1.py` (3.12.13) — **34 cases, 0 mismatches, 13/20 historical bounded.** Receipts are under v11; v10 evidence was not rewritten.

### Remaining v10 gaps that are now law

Partial package parse now **requires** every `project_named_packages` named path to appear as a row **and** in `examinedPaths` when a sibling manifest is malformed. Dropping the known `rs-app` row while keeping `source-syntax-invalid` is `ENUMERATION_PACKAGE_PARSE`. Mixed positive (bad `package.json` + named `Cargo.toml`) still ADMITs with that named subject retained.

Operational `boundaries` now catch **native** `AdmissionError` (`NV.AdmissionError`). That class is not the enumeration module’s `AdmissionError` (canonical.py is loaded twice). A float `schemaVersion` is `ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION`, not an uncaught typed fault.

### Actual controls

| Control | Result |
|---|---|
| excluded `.` empty complete inventories | ADMIT |
| two `foo` manifests, different paths, distinct subject3 | ADMIT |
| partial drops known named sibling | REFUSE `ENUMERATION_PACKAGE_PARSE` |
| unavailable binding, host-matching extents, empty inventories | ADMIT |
| unavailable binding, caller extents ≠ host file/package | REFUSE `ENUMERATION_BINDING_EXTENT_PATHS` |
| membership rows do not cover snapshot paths | REFUSE `ENUMERATION_ADMISSION_PRECONDITION` |
| full snapshot inventory sha/bytes ≠ used manifest bytes | REFUSE `ENUMERATION_ADMISSION_PRECONDITION` |
| invalid operational boundaries (native typed) | REFUSE `ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION` |

### Owned files (plan schema unchanged from v9)

| File | SHA-256 |
|---|---|
| `enumeration-plan.schema.v1.json` | `89669b0b075439b3cff56f798d035a2ac2aa479c50a0710a29724e5db2e23c1a` |
| `subject-inventory.schema.v1.json` | `6052614acdf337c8e2fe70299df162702f7844f9acb9ef591260953948fde44d` |
| `enumeration-contract.v1.md` | `70cfe3bbc95058c2e746979332a30ca6a3069811d6faa460bef1e3777b6978f3` |
| `enumeration_model.v1.py` | `de897b1f45bf714c522a1de3c60e4f58d436f870ba0769eba8a5c5ce8201f43f` |
| `check-enumeration.v1.py` | `f069033feab52011103634298d64d4dfcde3e70dcb85352e47283363f833e745` |

v11 receipt: `/tmp/opensip-design-corrections/grok-subject-assessment.v11/check-receipt.json`. Root’s three-file fullRun replay is outside this unit; these checks do not qualify a Run.
