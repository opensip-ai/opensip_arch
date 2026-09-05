# Security v3 independent review assistance

**OBJECT within assigned scope — 3 MUST, 0 SHOULD.** This assists the consolidated parent verdict; it is not an application or row-closure decision. Reviewer authored none of the65 frozen security subjects.

Freeze SHA-256: `9486f6c4f3d8196a1489541dd5bff7d3b7869e15d0b9d88b5a2011a46c761f81`. All65 pins match before/after review. The retained full report has230 checks/0 failures; the parent owns its replay. This assist ran22 targeted probes, retaining exact inputs/results and reproducer source.

- **SV3A-1 — Complete root admission.** A schema-valid root with a nonempty `kernelAttestationKeys` list passes semantic admission and manifest verification, contrary to the preview's explicit empty-list rule. Direct verification also admits repeated recovery keys because it bypasses root-schema validation. Enforce closed shape and the complete semantic policy before signature use.
- **SV3A-2 — Traversal is not scope narrowing.** Schema-valid project prefixes `src/../private` and `src/../../outside` merge under global `src` without refusals. Validate canonical policy path syntax and compare normalized path components; lexical prefix matching is insufficient. A later effect boundary may refuse, but that does not make this merge's proof correct.
- **SV3A-3 — Validate witness records before recovery.** Boolean sequence produces OK; missing PENDING hash produces REVERT; PENDING0 on an empty journal produces ADVANCE. Validate a closed state-specific witness shape and strict ranges before comparison. Malformed records must quarantine.

Positive controls support signature quorum distinctness, raw-policy deny-by-absence and deny precedence, effective-domain separation, legal witness transitions, and fresh-SQLite replacement/update/delete refusal. Frozen SQLite bytes were never opened writable.

A separate ungraded observation is retained for the parent: adding a project stateClass when the global token scope omits it is accepted. The underlying omitted-scope law must decide whether that is narrowing; this assist does not invent a rule.

All repairs are bounded admission/reconciliation predicates and can be tested with synthetic inputs. No production qualification, subject mutation, register edit or SATISFIED claim is made.
