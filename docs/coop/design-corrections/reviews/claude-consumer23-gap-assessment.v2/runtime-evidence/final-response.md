All three source findings are real, SHOULD-level issues, so my source36 ACCEPT must reopen. I've written one successor patch covering all three, and it passed every affected suite in a disposable copy. This is a nonblind source assessment only: not blind consumer B, not the final application review, and no acceptance of the successor. The frozen candidate36 bytes are unchanged.

**Files:**
- `claude-consumer23-gap-assessment.v1/assessment.json` (`3d66396c…`)
- `claude-consumer23-gap-assessment.v1/assessment.md` (`5c7e3a64…`)
- Patch: `claude-consumer23-gap-assessment.v2/successor-patch/successor-v23-gaps.v2.patch` (`cd16d3ab…`)

A final check of both files against the retained receipts passes 39/39.

## The three findings
- **V23-S1: real inconsistency.** A package endpoint without `packageManifestPath` is refused `QUERY.PARAMS_MALFORMED` by both the schema and the public query entry point. §2 of the query contract and the model's parser say `QUERY.ENDPOINT_AMBIGUOUS`.
  - The model can never mark a fully specified endpoint ambiguous, so this missing-path case is the only way that code could ever occur.
  - **Fix:** a request-only endpoint definition that lets the missing path through closed-schema admission, so §2 refuses it as `ENDPOINT_AMBIGUOUS`. Response rows keep the strict definition. Contract wording, parser and new controls are aligned.
  - **Alternative:** keep the schema and publish `PARAMS_MALFORMED`. `ENDPOINT_AMBIGUOUS` would then have no reachable query route.
- **V23-S2: real inconsistency, not a scope distinction.** Native §10 gives `VERDICT.INDETERMINATE` for `required-relation-missing`, `language-tier-unsupported` and `confidence-floor-unmet`. The D9 exit contract, which §10 says it inherits unchanged, gives the matching `COVERAGE.*` codes. The owner texts leave no room for a per-requirement exception: a single requirement's outcome carries no D9 code at all.
  - **Budget mismatch:** the native model's `run_termination` also maps `budget-exhausted` to `VERDICT.INDETERMINATE`, contradicting §10 itself and D9.
  - **Fix:** change the three §10 cells, add a paragraph stating the single mapping, derive `run_termination` from the D9 map, and add a regression case. No D9 vocabulary changes.
- **V23-S3: real but narrow gap.** Over a real admitted Run, `unavailable` evidence is refused with `evidence.missing`, but only model code says so; no contract text or control names it. The identity owner's own termination for unsuppliable evidence also uses `evidence.missing`.
  - **Fix:** publish the full state-to-detail mapping in query §7 (`retained` and `partial` don't refuse on their own) and add controls. No new detail code.

## My first patch was wrong on one point
My original patch also edited the `publicD9Termination` text inside `native-evidence.schemas.v2.json`. Changing those bytes breaks retained evidence:
- A foundation check failed, because a native test fixture still declares the old digest.
- All 13 retained package13 Runs embed that schema's digest. Replaying them against the edited owners refuses every positive Run with `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`.

The corrected patch leaves the schema bytes alone. §10 now says that annotation is incomplete and that §10 governs.

## Corrected patch in the disposable copy
- All seven suites exit 0 with pins valid:
  - query 131/131, including all 8 new controls;
  - native 376/376, including the new case;
  - foundation, integration (412), security and workflows;
  - evaluator3 launcher 16/16.
- The 13 package13 Runs behave exactly as on frozen36 through both `open_run_closure` and `close_run`.
- The implementation-planning check exits 1 ("Planning source changed: query"). That is expected, not a patch defect: `native-evidence.md` and `graph-query.schema.json` are pinned planning inputs, so the current planning layer can't be kept.

A real successor still needs the pin ledgers re-sealed, the regenerated workflows and native reports committed, a new planning input layer, and a fresh review of its exact bytes. Fifteen of the 107 rows own `native-evidence.md` and must be re-read then.

## Reopening source36
My ACCEPT reported no new MUST or SHOULD, and these three consumer-visible defects were missed. It stays on record unedited but can't stand as final acceptance of these areas. I raise no MUST: class, exit code, errorCode, soundness and D9 vocabulary are unaffected.

## Still open, and how this run went
- **Model limits (not fixed here):** `run_termination` emits one reason code where D9 derives an ordered list including secondary deficiencies. It also emits no Run or coverage IDs. How evaluator proof causes pick a whole-Run deficiency is not decided here.
- **Carried unchanged:** TCB-SCOPE-01 as one shared assumption over 13 dependent rows, 28 condition-2 obligations, 32 product gates unperformed (condition 5 NOT MET), 54 recovery cases unexecuted, and 30 residual proposals pending. No application, readiness or implementation authority is granted.
- **Provenance:** root states the report I assessed (`77cfab1f…`) is the completed consumer23 final report, even though the original dispatch labelled it interim. I verified only my copy's digest.
- **Run record:**
  - My first rehearsal was stopped mid-run when the earlier process ended; a bounded poll confirmed it was not active.
  - The original builder then failed on the missing rehearsal summary, and a gate of my own was wrong at first. All of these receipts are kept.
  - In an earlier progress note I misstated the report's verdict as ACCEPT; it is CHANGES_REQUIRED.
