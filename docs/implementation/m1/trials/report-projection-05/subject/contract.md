# Report projection and fit successor contract (author-05)

## 0. Standing

This is an **author-05 correction candidate** answering the fresh independent review `m1-report-projection-review-04` of frozen `m1-report-projection-subject-04` (manifest `5e43e1a1…7b20e`): RPR4-1..3 and advisories A1–A9. It is not approval. An actual separate review and root acceptance are still required.

**Readiness:**

| Scope | State |
|---|---|
| Carrier unit | Candidate for review. It covers the shape and admission of delivered carriers: the envelope5 fit carrier; the report-projection:1 ledger, panels, codec, derived bounds and byte law; and delivery goldens. |
| Report design | **Blocked** by RP-DO-01 and RP-DO-03..12 in `owner/design-obligations.v1.json`. Those entries are proposals to other owners, not completed features. |
| M1 final integration | **Blocked** by RP-OBL-C01 (pre-Run interruption envelope form) and RP-OBL-K01 (coverage module-milestone key). |
| AUDIT-G10 | Open. |

**Envelope parent dependency (explicit).**
- **envelope5 bytes are unchanged** from subject-04: `owner/command-envelope.v5.schema.json`, sha256 `45de2b0a12fc2f1f41f3a4f50b22b5e177fad58b19e5cc5072ff808c737e789d`, 36,852 B. `check.py` asserts this.
- Those are exactly the parent bytes of the root-authored, **unselected, conditional** envelope6 candidate `m1-interruption-envelope-subject-01` (manifest `76897423…71bf`). Its review, `m1-interruption-envelope-review-01`, is accept-conditional pending F1 (owner prose), F2 (a named host ledger join) and F3 (a post-commit query-command carrier). Root is correcting those.
- **This candidate does not adopt envelope6 and claims no integration of it.**
  - No file here references `command-envelope:6`; `check.py` asserts this.
  - No envelope6 file is opened or pinned.
  - If an envelope successor is accepted, this candidate must rebind (RP-OBL-C01 closure criterion).

**Unchanged:**
- Earlier subjects, reviews, source45, application46, the accepted metadata-v2 unit, the foundation directory and the historical coverage bytes are untouched.
- The mutable `docs/implementation/README.md` is never read; the alias probe shows the hook refuses it.

**Not claimed:** no browser, HTML, human renderer, generator, product code, host signal handling or performance measurement.

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists 17 files and excludes only itself:
- `check.py`, `report_model.py`, `build_owner.py`, `build_fixtures.py`, `seal.py`;
- `report-projection.schema.json`, plus under `owner/`: `command-envelope.v5.schema.json`, `command-inventory.v5.schema.json`, `command-inventory.v5.json`, `implementation-coverage-successor.v1.json`, `passage-overrides.v1.json`, `design-obligations.v1.json`, `budget-derivations.v1.json`;
- `fixtures.json`, `source-pins.json`, `successor.json`, `contract.md`.

`check.py` never runs `seal.py`, and no file hashes itself.

**Run it from a copy of exactly the listed files:**

`TMPDIR=<existing absolute scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture ARCH --subject-strict [--out RESULT]`

**Trusted-reference closure.** The claim is narrow: a trusted host and interpreter, not a sandbox against malicious natives.

| Mechanism | What it does |
|---|---|
| Pins | `source-pins.json` holds 79 files and 2 listings, verified before any external import. |
| Audit hook | Governed read-opens are refused unless pinned, and are re-hashed at open. Listings are recomputed at use. |
| Alias handling (A1) | Membership uses the given path and its realpath, compared case-folded; pins are also matched by `(st_dev, st_ino)`. **Alias probe:** exact, case-variant and `..` spellings of the unpinned README are all refused `UNPINNED-LOAD` before a byte is read. Hard links planted outside the roots and hostile native code are outside this claim. |
| Fresh-source loader | Compiles the verified bytes; bytecode is never consulted. The bytecode demonstration is kept. |
| No child processes | The accepted metadata checker runs in-process. |
| Writes | Only the declared `--out` may be written, and it may not be read. |
| TMPDIR (A2) | `tempfile.gettempdir()` is not called, so there is no pre-hook probe write. The declared `TMPDIR` must already exist; after the hook only a fresh `mkdtemp` child is used and then removed. |
| Out-write counter (A2) | A result cannot count its own write. The result file says so; after the write, the run asserts and prints `declared-out writes observed: 1`. |

## 2. Finding-by-finding disposition (review04)

| Finding | Disposition | Evidence (exact outcome) |
|---|---|---|
| **RPR4-1 page law (blocking)** | **Corrected.** `report_model.page_law(context, items, size, bounds, position)` implements the owner law for any page of a logical operation (query-projection-contract.v3 :136, :140, :146):<br>• `totalItems == producedItems` on every page (exact: all units produced; lower-bound: the produced prefix);<br>• a page is `[position, position+items)` of the produced prefix and must not exceed it;<br>• a cursor ⇒ full page, rows remain, and it continues at `position+items` (reference form checked);<br>• no cursor ⇒ `position+items == producedItems` (the page set ends and embeds every produced row), and not truncated-page;<br>• complete ⇒ exact and no cursor;<br>• lower-bound ⇒ a produced or visited cap was reached;<br>• truncated ⇔ truncated-bound;<br>• counts within the caps.<br>The mock owner now answers continuation pages (`page.cursor`). The verified graph provenance label is renamed `owner-page-law-total-equals-produced-prefix-coverage-continuation` (A4 of review03). | G4 → `J-GRAPH-COUNT`; G5 → `J-GRAPH-COUNT`; G6 → `J-GRAPH-COUNT`; total = produced at the cap but sliced without a cursor → `J-GRAPH-COUNT`; G1/G2/G3, S2 still refused.<br>Positive controls (`graphPageLawControls`): exact multi-page set 50/50/7 whose concatenation equals the unbounded answer; capped multi-page set under test bound 60 (25/25/10, last truncated-bound lower-bound, equals the produced prefix, refused under public bounds); **public item cap reached** over 100,001 facts (first page truncated-page with cursor, last page at position 99,900 is truncated-bound with no cursor and equals the produced suffix); smaller re-issued first page is a prefix of the larger; public-cap document slot → accept.<br>Model negatives: continuation dropped mid-set, total ≠ produced, page beyond the prefix, last page at the wrong position. |
| **RPR4-2 skipped steps (required)** | **Corrected** to the pinned owner reference model (`workflows_model.v1.py` run_invocation aggregate):<br>• skipped required steps stay in the ledger with their recorded termination but are excluded from D9 ordering, picking and tie matching;<br>• if no non-skipped required termination exists, the aggregate is `success`;<br>• skipped counts as settled for cancellation;<br>• before-settle `runId` is taken from committed **required** steps, as in the owner model.<br>The ledger preserves skipped records: `skipReason` is required iff skipped (schema), and `J-LEDGER-SKIPPED` requires no attempts and a `skipReason` supported by recorded dependency outcomes (the owner dependency gate). Erasure of a skipped record is caught by missing-children recomputation. | Aggregate: reviewer probe (skipped request-rejected) → `success`; skipped indeterminate → `success`; all skipped → `success`; required rejection plus skipped → the rejection; required success + optional failed + required skipped → `success`; optional skipped + policy-failed → policy-failed; before-settle over skipped-settled → refused; after-settle → not reclassified.<br>Documents: 2 new owner-valid skipped bases accept (fit analysis rejected/query skipped; audit baseline rejected/comparison skipped); skipped termination promoted → `J-LEDGER-AGGREGATE` (fit and audit); skipped with attempt → `J-LEDGER-SKIPPED`; skipped with a completed dependency (reviewer shape in a document) → `J-LEDGER-SKIPPED`; unsupported reason → `J-LEDGER-SKIPPED`; missing or misplaced `skipReason` → `SCHEMA`; erased record → `J-LEDGER-MISSING`.<br>Goldens: 5 skipped mixtures × human/json/agent/html (written, required render failed, optional render failed; audit written and required render failed after commit). |
| **RPR4-3 RP-OBL-C01 (required)** | **Tracked as pending integration; not closed, and no detail invented.**<br>• **Register:** `integrationObligations[RP-OBL-C01]` records owner, gap, affected rows, the envelope6 parent dependency (not adopted), closure criteria (accepted successor with F1 prose, F2 host ledger join with refusal goldens, F3 post-commit query-command carrier, rebind of this candidate), and `blocksM1FinalIntegration: true`.<br>• **Coverage:** open review issue RP-OBL-C01 on all 8 html command rows, the human/json/agent/html renderer rows and workflowGolden `interrupted-before-settle` (analyze, interrupted, 130). Each row's method states it cannot be verified for that situation. The golden already exists, so inventory5 is not changed.<br>• **Carrier:** host rule `J-ENV-INTERRUPTION-DETAIL` refuses any error detail beside an interrupted `kind=failure` termination.<br>• **Goldens:** 8 pending expected-refusal goldens (analyze and candidates, signal before commit, × 4 formats), all `countsAsDeliveredBehavior: false`. | Pending goldens: owned aggregate `{interrupted, SIGINT}` with no runId; envelope5 outcomes are errors-empty → `SCHEMA-ENV`, errors-omitted → `SCHEMA-ENV`, invented `evidence.purged` → `J-ENV-INTERRUPTION-DETAIL`.<br>Report cases: interrupted failure with an invented detail → `J-ENV-INTERRUPTION-DETAIL`; without detail → `SCHEMA`.<br>Coverage: C01 on 13 rows; the scoped validator is still valid. |
| **A1 alias bypass** | Corrected within the trusted-reference claim (§1). | `aliasProbe`: exact / case-variant / dot-dot → `UNPINNED-LOAD` |
| **A2 pre-hook probe and counter** | Corrected (§1). | stdout `declared-out writes observed: 1` |
| **A3 codec vs structural bound** | The distinction is stated, and a new obligation RP-OBL-L01 asks the invocation-record owner for the bound. | `codecReachability`: a schema-valid 4096-pin termination of 6,382,004 B is refused by the exact codec parse (`BYTE_LIMIT_OR_TYPE`) and lies within the structural bound 6,476,835 B. The structural bound is kept; M01 must measure the maximal document. |
| **A4 disclosure label** | The key is renamed `graphDescriptorNotRetainedSubjectsHostAsserted` (static format `labelled-canonical-lines.3`). The schema description says browser admission is shape, codec and internal joins only and never semantic proof. | `J-DISCLOSURES` hidden-count case; derived cap now 27,827,987 B (+23 B from the key) |
| **A5 R05 / conditional RP-DO-02** | Corrected: only blocking obligations hold report-feature rows open. RP-DO-02 remains a review issue with `affects: []` and a conditional standing. | `conditionalRpDo02HoldsNoRowOpen` |
| **A6 workaround value and owner** | Recorded, not closed: the key alone is proven. `valueDerivation` and owner are in the overlay; closure belongs to the coverage owner (RP-OBL-K01, blocks M1 final integration). | Only delivery row owning `assets.rs` is `commands/version` M1; M0 → valid, M1 → valid, M6 → "Delivery precedes module prerequisite: version" |
| **A7 register standing** | Every design obligation carries `standing: proposal to the owning design unit; not accepted by that owner…`. RP-DO-11 notes the invocation:3 successor and ledger successor it implies after M1. | register check |
| **A8 explicit Run selection** | Open: RP-DO-12 notes that history stays recent-only and explicit older Run selection is not delivered. | register |
| **A9 generator** | Open: not run (RP-OBL-G01). | — |

## 3. Fit successor

Unchanged from author-04: envelope5 (bytes identical), inventory5, host admission `J-ENV-FIT-*`, and the restorations with 43 metadata cases through envelope5 plus the in-process accepted checker. Additions this round:
- `J-ENV-INTERRUPTION-DETAIL`;
- the stated envelope6 dependency (§0).

The audit `comparisonResultId` join remains, except on interrupted terminations.

## 4. Report document

The root members, views and panels are as in author-04. `disclosures` now carries `graphPlannedSubjects`, `graphDescriptorNotRetainedSubjectsHostAsserted` and `historyPriorRunsInSnapshotHostAsserted`. Feature states and their obligations are unchanged: 12 features, RP-DO-01..12; they are disclosure only.

## 5. Invocation ledger, D9, cancellation and skipped steps

**Shape:** `{requestId, workflow, mode, cancellation, steps ≤ 64, missingChildren, provenance}`. When recorded, a step carries `outcome`, `attempts`, `termination`, and `skipReason` iff skipped.

**Joins:**
- `J-LEDGER-REQUEST`, `-COMMAND`, `-STEPS`, `-RENDER`, `-MISSING`, `-ATTEMPTS`;
- `J-LEDGER-SKIPPED`;
- `J-LEDGER-RUN`, `-MODE`;
- `J-LEDGER-CANCELLATION` (a delivered document needs `requested false, phase none`; cancelled ⇔ interrupted; model-law refusals);
- `J-LEDGER-AGGREGATE`;
- `J-LEDGER-BOUND`.

**Aggregate law** (`invocation_aggregate`, equal to the owner reference model):
- **before-settle** (some required step unrecorded or cancelled; skipped counts as settled): `{interrupted, signal, runId of the last committed required analysis}`.
- **otherwise:** D9 over recorded, required, **non-skipped** steps, with ties to the first carrying detail; none gives `success`.
- after-settle requires every required step recorded.
- a cancelled step without before-settle is refused.

**Delivery goldens:** 12 scenarios × 4 formats = 48 rows. The 7 author-04 scenarios are unchanged; the 5 skipped mixtures are new (§2). Each row preserves prior terminations, keeps an identical aggregate across formats, and has an envelope admitted by envelope5 host admission.

## 6. Graph policy, owner page law and subject index

- The slot plan, pointers and table laws are unchanged. `J-GRAPH-COUNT` applies the §2 page law at position 0 against `budgetProfile.graphPublicBounds` (graph-query:3 Bounds).
- Report documents embed first pages only; continuation behavior is exercised by the owner-level positive controls.
- `host.testBounds` controls are lawful only under their own bounds.

## 7. History policy

Unchanged: baseline source first, excluded from prior Runs; recent prior Runs by commit sequence; the snapshot count is host-asserted and disclosed. Explicit older Run selection is RP-DO-12.

## 8. Provenance

Every `verifiedInDocument` label names an enforced join, and host assertions are listed. The static disclosure names every host-asserted count.

## 9. Codec, derived bounds, byte law and delivery

**Codec:** `documentMaxBytes` **27,827,987** = 246 + 4,194,304 + 19,435,937 + 4,194,304 + 3,196 root members. Iterative depth ≤ 38, canonical lexical laws.

**Bounds:** the ledger bound is structural per command (audit 19,435,937 B). Under the exact codec a single record over 4 MiB is unreachable, pending the owner statement (RP-OBL-L01). The effective exploration budget and the byte law are unchanged; delivery failures follow D9.

## 10. Obligation register

| Id | Kind | Standing |
|---|---|---|
| RP-DO-01, 03..12 | report design blockers | proposals to owners; M4 |
| RP-DO-02 | conditional, not selected | holds no row open |
| RP-OBL-C01 | integration: envelope/workflow owner | pending integration; blocks M1 final integration; envelope6 parent dependency, not adopted |
| RP-OBL-K01 | integration: coverage owner | pending successor; blocks M1 final integration |
| RP-OBL-L01 | integration: invocation record codec bound | pending owner statement |

Other obligations in `fixtures.json#/obligations`: RP-OBL-B01 (browser), B02 (accessibility), H01 (host delivery), M01 (measurement, including the 27.8 MB document), G01 (generator), E01 (integration record).

## 11. Passage overrides and coverage

There are seven conditional overrides; the condition text names author-05. The coverage overlay has 38 row changes, 1 addition and 13 review issues:
- the 12 design issues;
- RP-OBL-C01.

The full owned validator gives unscoped (base and overlay) "Missing/extra module milestone prerequisite", and scoped valid/valid.

## 12. Check evidence and limits

**`check.py` verifies:**
- closure, alias probe and bytecode demonstration;
- regeneration;
- restorations, the 43 metadata cases and the in-process accepted checker;
- coverage (C01 rows, R05, workaround controls);
- the register (standing, integration obligations, envelope5 sha = envelope6 parent, no envelope6 reference);
- subject3 agreement;
- 22 aggregate cases, 48 delivery goldens, 8 pending goldens and 16 static-parity goldens;
- codec reachability and derived bounds;
- **22 envelope cases:** 7 accept, 8 schema, 7 host admission;
- **162 report cases on 16 bases, each with its exact code:** 27 accept, 29 schema, 15 codec/boundary, 16 envelope host admission, 22 ledger/D9/cancellation/skipped, 29 graph/slot/index, 24 other joins;
- graph page-law controls, the byte-law scenario and the worst-case table.

**Limits:**
- Fixtures and the mock graph owner are constructions following the cited laws, not the product engine or ledger store.
- Owner-model agreement is by rule implementation, not by executing `workflows_model.v1.py`.
- Skipped-step divergence from author-04 appears only for ledgers where the skipped root is not a required failure. Owner-valid DAGs (a required step may not depend on an optional step) mostly give the same class. Both are aggregated exactly as the owner model does.
- Pending goldens document a gap and are not delivered behavior.
- This is not browser, renderer, generator, performance or product qualification.
