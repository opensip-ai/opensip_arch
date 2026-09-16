# OpenSIP blind consumer design review -- consumer-b.v19

**Verdict: ACCEPT-RECONSTRUCTABLE**

| | |
|---|---|
| sessionId | `79569ae1-10f4-4181-972b-334f7ed2f07a` |
| same-origin ancestry | consumer-b.v14 -> consumer-b.v15 -> consumer-b.v16 -> consumer-b.v17 -> consumer-b.v18 -> consumer-b.v19 |
| subject manifest SHA-256 | `124835865d78de77198d3fe741e8d27495d87cb0236cd064316ebdd38065dc8b` |
| parent digest declared in that manifest | `3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2` |
| kit files verified | 102 / 102 (PASS) |
| measured normative delta | 93 unchanged, 8 changed, 1 added, 0 withdrawn |
| changed owners | `atom-evaluation-contract.v1.md`, `common.schema.json`, `common.schema.json`, `repair.schema.json`, `repair.schema.json`, `workflow-projection-contract.v3.md`, `native-evidence.md`, `workflows-and-surfaces.md` |
| added owner | `glob-pattern-contract.v1.md` |
| history standing | CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE |
| requirement status | executed 131, futureQualification 3 |
| new MUST / SHOULD / advisories | 0 / 0 / 1 |

> This is NOT a parent whole-candidate verification: only the parent digest declared
> inside the held manifest was compared. No root admission, agreement, expected
> result, author model or checker was supplied, read or inferred; the root outcome
> over these exact bytes is unobserved by this origin. Nothing here qualifies any
> product, compiler, provider or host.

## Why this verdict

ACCEPT-RECONSTRUCTABLE requires every acceptBlocking requirement executed, no unresolved MUST or SHOULD, no open helper failure on a claimed positive, and every claimed positive through schema admission, retained closure, fresh-process replay and its controls. MEASURED: 0 acceptBlocking requirement unexecuted, 0 MUST, 0 SHOULD, 0 open helper failure, all five positives passed = True.

- acceptBlocking requirements unexecuted: **0**
- claimed complete positives that passed schema admission, retained closure, fresh-process replay and their controls: **all 5**
- unresolved MUST issues: **0**
- unresolved SHOULD issues: **0**

## Claimed complete positive Runs

| Run | runId | verdict | objects | blobs | closure checks | replay | controls |
|---|---|---|---|---|---|---|---|
| syntax-code | `run3:570febcca6629d32e...` | indeterminate | 51 | 135 | 854 passed / 17 n-a / 0 refused | MATCH | 14 refused |
| typescript | `run3:1b4f6a3c01445325b...` | indeterminate | 60 | 180 | 1042 passed / 10 n-a / 0 refused | MATCH | 14 refused |
| rust | `run3:75a9e57791f4ff92f...` | indeterminate | 73 | 188 | 1137 passed / 19 n-a / 0 refused | MATCH | 14 refused |
| rust-partial | `run3:1e3ff99abf5caccd1...` | indeterminate | 88 | 192 | 730 passed / 9 n-a / 0 refused | MATCH | 14 refused |
| syntax-data | `run3:e18eaf7c7710629d2...` | indeterminate | 53 | 136 | 780 passed / 20 n-a / 0 refused | MATCH | 14 refused |

Exported bytes, by SHA-256 of the export file itself:

- `runs/syntax-code.store.json` -> 58be25439d6ada794006d56e8633fc36a390455072b464db095b183e9db793a9
- `runs/typescript.store.json` -> 7ef028e8cababd65e4dd9c54fe6e7be9112cb6bd54570cba82d769cda5a57efa
- `runs/rust.store.json` -> 98f7d21df74b45322899677a4718af5968186ff0cc3a585f269e15d2cffe78cc
- `runs/rust-partial.store.json` -> f57dfe243c1a0cce9a58150afb304fdc3f71c0617a49bb7bc5982966114ba778
- `runs/syntax-data.store.json` -> fa815695ba887b48c8555cf74100628dd02553310bf3d31f089b91fa513b630d

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v19/output/lib/verify_all.py
```

The command declares **46** stages. When this final reconciliation stage ran, **45** preceding stages of this same run were recorded and all passed: **True**. this deliverable is written by the FINAL stage of that command. verify-all.json is rewritten after every stage, so the row count above is every preceding stage of the SAME run; the only row it cannot contain is this reconciliation stage's own exit, which the command appends after it returns. No number here is inherited from an earlier run.

## New MUST issues

None. newMustIssues is EMPTY because every observable this origin was required to produce had a published derivation that it could execute: the C/H recipes, the closing digest law and its four representations and retention modes, the capability-manifest gates, the relation/rung registry with its anchor, snapshot, totality and partition laws, the grammar-capability registry and its three enforcement boundaries, the section 1.2 mode table, the config node-kind law, the Rust context projection, the execution-inputs cell and account derivation, the composition section 9 proof/evidence/seal/Run joins, the repair descriptor and its two idempotency recipes, the comparison and baseline identities, the D9 class/exit table, and the graph-query operations with their bounds and mandatory disclosure. Where a value could not be recomputed (L1-L3 normalisation, symbol-to-path attribution, provider occupancy) the kit SAYS so and substitutes custody, which this origin executed rather than worked around.

## New SHOULD issues

None open. The two that generation 16 raised are RESOLVED by the normative successor
this generation received, on published law rather than by invention:

### V16-S1 -- the repair descriptor's closedWorld projection names "that same Run's ClosedWorldV2" without saying which Coverage entry owns it when a Run carries several that differ

- disposition: **RESOLVED BY THE NORMATIVE SUCCESSOR, at generation 19**
- what the new bytes say: workflows-and-surfaces.md section 6 now states the problem and then the answer: "A Run holds one ClosedWorldV2 per Coverage entry, not one per Run, so the gate states which entries it reads", and "An earlier revision of this section said the prerequisite was decided against the evidence Run's own native ClosedWorldV2, as though a Run held one. It does not, and with several retained records that phrase did not denote." The three published steps are relevant universes (target occurrences UNION the retained selected-program census of the EnumerationPlan, with a selected-but-unavailable binding contributing typed unresolved ownership), selected records (every retained coverage2 whose scope sourceUniverse is relevant, independent of evidenceRequirements, totally ordered on six members), and a NON-VACUOUS conjunction gate. repair.schema.json closedWorld carries the same law and adds the five-field least-closed DISPLAY SUMMARY with absence folded in, the display sentinel, and "NO MEMBER OF IT IS AUTHORITATIVE, the boolean included".
- how this origin closed it: lib/repair_selection_v19.py reconstructs the three steps and the reduction; lib/phase6_repair.py now derives the descriptor member from that selection and gates unsafe edits on the selected records. Measured: the TypeScript Run selects 5 records over 1 relevant universe, the Rust Run 5 over 2 (the census join makes a second universe relevant for one unsafe path) and rust-partial 8 over 3; every one dissents, so no unsafe edit is eligible in any of them. Nine law-branch controls measure the branches no Run contains, including the selected-but-unavailable binding whose unresolved ownership "does not vanish because some other owner of the same path is closed". Two new descriptor controls refuse a summary copied from one recipe-selected favourable Coverage entry and a literal seven-field copy.
- whatThisOriginDidNOTDo: it did not keep its earlier workaround. The v16-v18 reconstruction projected ONE Coverage entry and relied on the measured accident that this subject's entries agreed; that is exactly the recipe-selected record the published law forbids, and it is gone.

### V16-S2 -- GlobPattern publishes a whole-segment `**` and one example, which does not decide whether a TRAILING `**` matches the files of that directory

- disposition: **RESOLVED BY THE NORMATIVE SUCCESSOR, at generation 19**
- what the new bytes say: foundation/glob-pattern-contract.v1.md is NEW in this input and is the normative owner of the predicate: "A pattern segment that is exactly `**` instead matches zero or more whole candidate segments. This rule applies at the beginning, middle, and end, and may consume the final filename segment. It does not require a directory." Its required-example table settles the exact case this origin reported as unstated: `src/**` matches `src`, `src/legacy.js` AND `src/nested/legacy.js`, while `src/**/*` does NOT match `src`. workflow-projection-contract section 14 and the atom contract both link to it, and common.schema.json GlobPattern repeats the rule in its description.
- how this origin closed it: lib/opensip_eval.py glob_match is reconstructed from the published equivalence and lib/glob_law_v19.py measures all 23 required-table rows, 22 further properties the prose states (anchoring, case sensitivity, dotfiles, scalar-counting `?`, literal braces/brackets, no escape syntax, trailing slash as an empty segment, no `.`/`..` resolution) and 5 composition cases: 0 failures. The generation-18 predicate is kept in that module so the delta is MEASURED: for every glob this origin actually uses the two readings agree, because this origin had deliberately written terminal wildcards as `**/*`, so no Run needed reminting for the glob law.
- whichReadingWon: the "any remaining suffix" reading, NOT the segment-group-followed-by-a-separator account this origin had written up as one possible interpretation. The generation-18 write-up was careful to present that as possible rather than forced, which is why the correction here is a measurement rather than a retraction of a claim.

## Advisories

- **V16-A3** (wording) `traversalCoverage` and native CoverageResult share the word "coverage" while being different obligations
  - observation: the schema already says "Not native CoverageResult" in both places, which is why this is only advisory. The shared noun still invites a consumer to report a COMPLETE traversal over an INCOMPLETE evidence base as evidence completeness.
  - handled here by: the two are carried in different required fields and reported separately, with an explicit statement of why: see query/graph-query-reconstruction.json evidenceLimitationsVersusStoredEdgeCompletion.

## Withdrawn by this origin, or resolved in the new kit bytes

- **V16-A2 (WITHDRAWN by this origin as factually wrong about the kit)** -- WITHDRAWN -- the clauses do state it, and they state the opposite. three published clauses, read this generation: (1) enumeration-contract section 1, UNAVAILABLE binding -- "`extents` still populated from host membership so expected file/package paths are not lost", and the enumerator row requires "inventories empty `unavailable` matching that pair"; (2) enumeration-contract sections 3/4 -- EXACTLY ONE SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind) of cell.kinds, with the `unavailable` shape given explicitly (rows=[], examinedPaths=[], deficiency non-null) and ENUMERATION_INVENTORY_MISSING_RECORD named for a whole missing expected inventory; (3) execution-inputs section 6 -- "Inventory digests: exactly one per kind, kinds set-equal to the cell" with NO available-only qualifier, plus "Unselected or `universe=null` DOES NOT DISCARD same-cell inventory items." A MISSING record is not a retained `unavailable` record.
- **V15-S1 (withdrawn by this origin)** -- WITHDRAWN as over-broad. no annotated site of the native document uses `fragment`, so declining to declare it there is correct. Measured: retention counts are preimage-frame 31, preimage 21, owner-retained 11, closure-tree-member 10, derived 3, and ZERO fragment sites (notes/native-annotated-site-audit.json).
- **V15-A1 (resolved in the new kit bytes)** -- RESOLVED at the source. the v16 native schema replaces it with `siteCountLaw`: "Count syntactic x-opensip-digest annotation occurrences in this schema document; the reference checker reports the measured count. No second hand-maintained total is normative." This origin now MEASURES 76 occurrences and asserts the absence of the old key.
- **V15-observation on the `derived` retention recipe** -- RESOLVED at the source. the v16 native schema declares `derived` with the recipe this origin had already derived from the plan/run capabilityManifestId join; the closure now asserts the declared statement rather than this origin's inference (check_native_digest_law_vocabulary).

## Algorithm freedom that is NOT a gap

- **how a host ENUMERATES subjects**: pinned observable -- SubjectInventoryV1 rows, examinedPaths equal to the Plan census, and the locator identity (planId, parameterDigest, cellOrdinal, programOrdinal, kind); left open -- the traversal strategy, parallelism and caching. the retained record is fully specified, so any strategy is checkable
- **how a normalizer computes an L1-L3 body**: pinned observable -- the framed body identity, the retained level specification bytes, and bodyIdentityJoin.recomputableAt = [L0-verbatim] only; left open -- the normalisation algorithm itself. the kit states in terms that it is NOT recomputable above L0 and demands exact retained preimage custody instead -- a deliberate, published limit, not a missing recipe
- **which shortest path a graph.path returns when several tie**: pinned observable -- canonical fact2-id-sequence tie-break; left open -- the search algorithm. the tie-break makes the RESULT total, so the algorithm is free
- **how a host stores and indexes the evidence store**: pinned observable -- the exported object table plus every blob keyed by its digest; left open -- the storage engine, indexes and compaction. a host index is explicitly never authority; resolution goes through digests

## What this generation added to the audit

### area1_enumerationProgramBinding

- instrument: lib/indep_enumeration_binding.py, lib/programentry_law_v19.py
- checksPassedPerRun: {'syntax-code': 60, 'typescript': 67, 'rust': 57, 'rust-partial': 48, 'syntax-data': 60}
- programEntryProvenances: default, explicit and SYNTHESIZED: 8 cases, 0 failures (vectors/program-entry-law.json)

### area2_subjectInventoryCarrier

- instrument: lib/indep_subject_inventory.py, lib/negatives_carrier.py
- checksPassedPerRun: {'syntax-code': 95, 'typescript': 132, 'rust': 204, 'rust-partial': 146, 'syntax-data': 91}
- clauseOwners: subject-inventory.schema.v1.json properties.deficiency / properties.nativeCause / allOf and $defs.EnumerationDeficiencyV1 -- the actual selected schema

### area3_executionInputs

- instrument: lib/indep_execution_inputs.py (new independent derivation) plus 11 discriminating controls
- refusalsAgainstTheFivePositives: 0
- clausesPortedIntoTheRetainedClosureThisGeneration:
  - section 1 receipt totality over the admitted execution-plan stages
  - section 1 EXECUTION_INPUTS_SELECTED_COVER, both directions
  - section 3 binding joins: receipt producer, receipt outputDomains vs the stage, attributed view planId and producer, every named scope sourceUniverse vs the binding universe, and selected-U-cannot-become-complete-by-omitting-the-stage-and-views
  - viewDigests attributed to the captured receipt
  - the typed null-stage reason derived from the binding shape
  - section 5 subject-scope half of the per-universe attribution
  - section 5 expected-source-subject membership (the omission that let V18-D8 stand)
  - section 5 unsupported-typed requires a MATRIX cell deficiency and is contradicted by a returned partition (V19-D3)
  - section 6 candidate custody (implemented; unexercised by these Runs)
- lawRemovedBecauseThePublishedTableDoesNotContainIt: the all-accounts-unsupported => unavailable branch (V18-D7)

## Coverage limitations (disclosed, not design gaps)

- section 6 CANDIDATE-ONLY custody (group bytes, sourceBodies id/path/universe/snapshot joins, complete examinedPaths, complete-empty envelope) is IMPLEMENTED in the retained closure and in the independent Area-3 instrument, but no positive Run declares a clones-near / clones-cross-tsjs cell, so no CandidateProducerResultV1 exists to exercise it
  - why not a gap: the kit publishes the law completely; this is a limit of this origin's own fixture set, recorded as an exercise gap. The equality law passes VACUOUSLY on all five Runs and is reported that way, and a cell whose capability is candidate-only is refused when it owes an envelope and has none
  - measured where: `vectors/indep-execution-inputs.json SECTION_6_CANDIDATE_CUSTODY_IS_UNEXERCISED_BY_THIS_RUN`
- a SELECTED-but-UNAVAILABLE enumerator binding (status selected, universe null) appears in no positive Run: the only unavailable binding is the optional-unselected shape, so the `unavailable-binding` typed null-stage reason and the `provider-unavailable` unavailable RECEIPT are reached by controls and by law-branch measurements rather than by a Run
  - why not a gap: both shapes are published and both are implemented and measured
  - measured where: `vectors/execution-inputs-negative-controls.json null-stage-reason-swapped; vectors/repair-closed-world-selection.json lawBranchControls`
- every positive Run declares exactly ONE execution-plan stage, so receipt totality over several stages is exercised by a control rather than by a positive
  - why not a gap: the totality law is implemented and measured
  - measured where: `vectors/execution-inputs-negative-controls.json execution-plan-stage-without-a-receipt`
- a js-synthesized CELL appears in no positive Run, so the SYNTHESIZED programEntry provenance is measured at the law level over synthetic parameters
  - why not a gap: the clause is published and all three provenances are measured
  - measured where: `vectors/program-entry-law.json`

## Helper corrections (helper bug != design gap)

| id | where | corrected |
|---|---|---|
| V15-D1 | lib/rebind_v15.py, lib/verify_kit.py | corrected |
| V15-D2 | lib/run_ts.py language mode of record | corrected |
| V15-D3 | lib/opensip_schema.py _resolve_local | corrected |
| V15-D4 | lib/run_*.py VCS observation kind | corrected |
| V16-D1 | lib/opensip_schema.py walk_keywords / _resolve_local | corrected |
| V16-D2 | lib/opensip_build.py component-manifest description | corrected |
| V16-R1 | lib/run_ts.py, lib/run_ts_full.py -- the TypeScript subject and Run | reconstruction-strengthening (NOT a helper bug and NOT a kit defect) |
| V17-D1 | lib/phase0.py ANCESTRY table, after the v16->v17 path rebind | corrected |
| V17-D2 | lib/opensip_closure.py check_policy_admission filter admissibility | corrected |
| V17-D3 | lib/opensip_closure.py (no kind law at all) + run_syntax_code_full.py and run_rust_full.py disabled probe rules | corrected |
| V17-D4 | lib/opensip_closure.py (no enumeration checker) + all four non-data Run fixtures | corrected |
| V17-D5 | lib/opensip_closure.py execution-inputs derivation + run_syntax_code.py unavailable binding | corrected (and withdraws the v16 advisory V16-A2) |
| V17-D6 | lib/phase7.py multi-step invocation + lib/envelopes.py (no join checker) | corrected |
| V17-D7 | lib/phase6_repair.py FileEdit admission | corrected |
| V17-D8 | lib/rebind_v17.py SELF_EXCLUDE, lib/check_siblings_untouched.py, lib/helper_corrections.py | corrected, with an irreversible side effect reported in full |
| V16-A1 | this origin's own v15 SHOULD about the native retention catalogue | self-correction |
| V18-D1 | lib/rebind_v18.py + lib/phase0.py ANCESTRY table and its historical note | corrected |
| V18-D2 | lib/run_syntax_code.py and lib/run_syntax_data.py UnitMembershipV1 records, plus lib/opensip_closure.py (which had no U-1..U-4 law at all) | corrected |
| V18-D3 | lib/run_ts_full.py default-unit program binding + lib/opensip_closure.py check_enumeration_plan (no programEntry provenance law) | corrected |
| V18-D4 | lib/run_ts_full.py, lib/run_rust_full.py, lib/run_rust_partial.py membership rows | corrected |
| V18-D5 | lib/run_syntax_code.py unavailable binding AND its retained inventory, plus lib/opensip_closure.py check_enumeration_carrier_pair (new) | corrected |
| V18-D6 | lib/helper_corrections.py ROWS (the generation field of V17-D1..V17-D8) and the V17-D1 narrative sentence, plus the stale consumerId in main() | corrected |
| V18-D7 | lib/opensip_closure.py check_execution_inputs_derivation, the all-accounts-unsupported branch of the derived-state ladder | corrected at generation 19 (identified at 18, measured and removed at 19) |
| V18-D8 | lib/run_syntax_code.py / run_ts_full.py / run_rust_full.py / run_rust_partial.py clones-fact cell outcomes, and lib/opensip_closure.py (the clause is absent there entirely) | corrected at generation 19 (PREDICTED at 18, MEASURED and repaired at 19) |
| V19-D1 | lib/opensip_capmanifest.py, lib/opensip_schema.py (four helper-correction narratives) and lib/deliver.py sameOriginAncestry | corrected |
| V19-D2 | lib/rebind_v19.py own docstring | corrected |
| V19-D3 | lib/run_ts_full.py, lib/run_rust_full.py, lib/run_rust_partial.py, lib/run_syntax_data.py accounts + lib/opensip_closure.py (no matrix requirement) | corrected |
| V19-D5 | lib/phase7.py multi_unit_missing_caps (vectors/multi-unit-missing-caps.json) | corrected |
| V19-D4 | lib/phase6_repair.py schema_admit and four control inputs | corrected |

Open helper failures on a claimed positive: **0**.

## Limitations and scope

- Every compiler, provider, toolchain, OS and runtime observation in these Runs is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a compiler, a provider, a host or an operating system, and no such qualification is claimed.
- No product code was written, no repository was modified, no commit or push was made, and no product was executed. Every byte produced lives under this origin's own output directory.
- The parent subject was never held. Only the disclosed 102-file kit and the parent digest declared inside its manifest were verified.
- Three branches of the execution-inputs and enumeration law are IMPLEMENTED and measured but are not exercised by a positive Run: section 6 candidate-only custody (no clones-near / clones-cross-tsjs cell exists), a SELECTED-but-UNAVAILABLE enumerator binding, and a multi-stage execution plan. A js-synthesized CELL is likewise absent, so the synthesized programEntry provenance is measured at the law level. Each is disclosed with the artifact that measures it in vectors/phase10-design-gaps.json coverageLimitationsDisclosedNotDesignGaps, and none is merged into the complete-positive claim.
- No root admission, agreement, expected result, author model, checker or golden was supplied, read or inferred. The root outcome over these exact bytes is UNOBSERVED by this origin.
- 3 of the 6 advertised language modes (js-synthesized, rust-cargo-prepared, ts-tsconfig) have an admitted representable path at the (context, universe) record level but were NOT exercised end-to-end on a sealed Run. Measured in vectors/advertised-mode-paths.json and not merged into the complete-positive claim.
- L1-L3 normalised body identities, symbol-to-path attribution and provider occupancy are not recomputable by a consumer; the kit says so and substitutes retained custody, which is what was executed. No normalizer, parser or provider is qualified by that custody.
- The repair, comparison, baseline, invocation and query records are RECORD reconstructions with their identities recomputed and their admission laws executed. No repair was previewed, applied or authorized; no baseline was adopted; no query engine was run by a product.

## Standing

- **noRootAdmissionClaim**: this origin reports ONLY its own independently executed admission, closure, replay and controls. It does not claim that any root, author or successor admitted, agreed with or validated these bytes.
- **noProductQualificationClaim**: nothing here authorizes a product implementation or qualifies any product, component, compiler, provider or host.
- **kitOnly**: every citation names a path and selector inside the frozen 102-file kit. No original repository, author model, fixture, golden, expected output, root outcome or other review was supplied or read. The disclosed PRIOR-OWN inputs are named in notes/v19-input-custody.json disclosedPriorInputs: this origin's own generation-17 review, its own generation-18 closing response, and a copy of its own generation-18 output including the unreconciled reports it has now corrected.
- **priorGenerationsUnmodified**: generations modified during this session: []. Newest modification time per generation: consumer-b.v14 2026-09-12T09:15:20Z; consumer-b.v15 2026-09-12T09:39:10Z; consumer-b.v16 2026-09-12T11:54:34Z; consumer-b.v17 2026-09-12T11:52:40Z; consumer-b.v18 2026-09-12T12:47:41Z. this measures WHETHER this session wrote into them. It does not and cannot certify that their earlier content is otherwise intact, and it is not a restoration verdict for the two generation-16 files.
- **historyStanding**: CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
- **generationLabelProvenance**: {'verdict': 'NO HISTORICAL LABEL DRIFT', 'method': "the earliest before-image containing the SAME sentence (with the label masked) carries that sentence's true generation; a later copy that disagrees was rewritten by a mechanical rebind", 'standing': 'the label corruption class that produced V18-D6 was audited again this generation against the retained before-images; four historical helper-correction sentences and one ancestry list were restored (V19-D1) and the rebind now rewrites PATH FORM ONLY.'}
- **writesMadeUnderAPriorGeneration**: this session: ZERO. Measured in notes/v19-history-standing.json measuredC: the newest modification time of every earlier generation tree predates this session's first write, so generation 19 wrote into none of them.
  - still open from generation 17: the GENERATION-17 session overwrote TWO files under the generation-16 output before its own control caught the defect: helper-corrections.json and notes/siblings-untouched.json. Generations 14 and 15 had zero writes, and no prior Run export, review file, checkpoint or vector was touched. The prior bytes were not retained by this origin and are NOT claimed to be restorable; root supplies no restoration verdict to this continuation. The item stays OPEN and is carried forward rather than marked clean. See helper-corrections.json row V17-D8.

