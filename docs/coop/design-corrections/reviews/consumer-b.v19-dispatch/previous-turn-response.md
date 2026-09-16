Area 3 is written; execution is blocked. Status:

## What I completed this turn (no interpreter needed)

**Read the actual Area‑3 clauses** rather than working from my draft's assumptions: `execution-inputs-contract.v1.md` §§1–8 in full, and `execution-inputs.schema.v1.json` `StageReceiptV1` / `HostCaptureV1` / `CellProgramOutcomeV1` / `NativeCoverageAccountV1` / `CandidateProducerResultV1` allOf branches.

**`output/lib/indep_execution_inputs.py`** — rewritten as the third independent derivation, clause‑mapped X1–X10, reading only the Plan, execution‑plan, enumeration plan, inventories, receipts, views/scopes/Coverage payloads, the vcs observation and the registries; it never reads the seal, the verdict, or any "capability is available" notion. Two readings the text leaves open are declared in the docstring (I‑1 row‑2 scope, I‑2 expected‑subject local vs global) instead of silently picked. My earlier draft had invented a `targetUniverse` requirement — §5 says explicitly that it does *not* constrain `targetUniverse`, so that is now recorded as deliberate silence.

**`output/notes/v18-area3-clause-map.md`** — the clause→old‑helper comparison. Clauses the retained closure does not represent at all: §3's binding joins (no cell outcome is ever joined to a receipt; no scope `sourceUniverse` is compared to its binding's U), `viewDigests` receipt attribution, receipt↔stage totality, `EXECUTION_INPUTS_SELECTED_COVER`, the typed null‑stage‑reason derivation, §5's subject‑scope universe half and expected‑subject join, and all of §6's candidate custody.

**Findings recorded** (`helper_corrections.py`, which had *no* generation‑18 rows at all — D1–D5 existed only as comments at the correction sites):
- **V18‑D6** *(new, corrected)*: the rebind rewrote generation‑labelled **content** in the corrections record — all eight `V17-D*` rows read generation `v18`, and V17‑D1's sentence had been made self‑contradictory. Settled against a disclosed input (`previous-review.source31.md` lists them as generation‑17 rows). Labels are now split literals; `consumerId` was still `v16`; the open‑failures list is now derived from row status instead of a hardcoded `[]`.
- **V18‑D7** *(open)*: my closure adds a derived‑state branch the §4 table does not contain ("all accounts unsupported ⇒ unavailable"), which would **refuse a lawful graph**. Dormant on the five positives — which is exactly why passing counts never exposed it.
- **V18‑D8** *(open, predicted not measured)*: the `clones-fact` cells claim `complete` while their own complete file inventory names expected file subjects no returned clones partition covers (§5 + `relations.clones.sourceSubjectKind = file`). Widening the scope is not the fix — `scopeCapabilityLaw` turns unreadable paths into an unsupported scope, i.e. "mixed ⇒ not complete" and `partial` again.

**Phase 10**: V16‑S2 now separates what the lone example *logically forces* (a leading `**/` may consume zero segments) from the segment‑group account that merely explains it; V16‑S1 gained an explicit generation‑18 status stating it was **not** closed by a recipe‑selected ClosedWorld record. Both stay OPEN.

**`verify_all.py`**: the three audit‑area modules plus the carrier controls are wired in after the Run stage.

## What is blocked, and on what

Every `Bash` call that invokes `/tmp/opensip-architecture-review-env/bin/python` is denied in this session (`ls`/`wc`/`grep` are allowed). So **nothing was executed**: no re-export, no fresh‑process replay, no controls, no reconciliation. Consequences I am not going to paper over:

- `output/blind-review.md`, `blind-review.json`, `verify-all.json`, `requirement-status.json` and `helper-corrections.json` still describe the **pre‑Area‑3** state and now disagree with `lib/`. The final reconciliation the instruction requires (kit digest/ancestry, stage count, artifact hashes, write‑history standing agreeing across human report, machine report and receipt) has not happened.
- V18‑D8 is a reading of clause + fixture, not a measurement; V18‑D7's removal and the Area‑3 port into the sealed closure are unapplied.
- I deliberately did **not** write the Area‑3 discriminating controls: the charter requires each to report its *actual* first refusal, and the laws they target are not yet in the closure. Shipping guessed first‑refusals would be fabricated evidence, so that work waits with the port.
- §6 candidate custody, a selected‑but‑unavailable binding, and multi‑stage receipts remain **unexercised** by the positives; those are logged as exercise gaps, not passes.

Verdict stays **CHANGES_REQUIRED** (S1/S2 open, V18‑D7/D8 open).

To finish, I need permission to run the reference interpreter — then the sequence is: run `indep_execution_inputs.py` over the five exported stores to measure V18‑D8, remove the V18‑D7 branch, port the missing Area‑3 laws, re‑derive and re‑seal the affected Runs, add the Area‑3 controls, and re‑run `verify_all.py` end to end before reconciling the report.
