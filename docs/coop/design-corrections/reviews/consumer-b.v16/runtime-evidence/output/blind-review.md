# OpenSIP blind consumer design review -- consumer-b.v16

**Verdict: CHANGES_REQUIRED**

| | |
|---|---|
| sessionId | `79569ae1-10f4-4181-972b-334f7ed2f07a` |
| same-origin ancestry | consumer-b.v14 -> consumer-b.v15 -> consumer-b.v16 |
| subject manifest SHA-256 | `6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6` |
| parent digest declared in that manifest | `1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b` |
| kit files verified | 101 / 101 (PASS) |
| changed against the prior disclosed kit | docs/coop/design-corrections/native/native-evidence.schemas.v2.json |
| requirement status | executed 131, futureQualification 3 |
| new MUST / SHOULD / advisories | 0 / 2 / 2 |

> This is NOT a parent whole-candidate verification: only the parent digest declared
> inside the held manifest was compared. No root admission, agreement, expected
> result, author model or checker was supplied, read or inferred; the root outcome
> over these exact bytes is unobserved by this origin. Nothing here qualifies any
> product, compiler, provider or host.

## Why this verdict

ACCEPT-RECONSTRUCTABLE requires every acceptBlocking requirement executed AND no unresolved MUST or SHOULD. Two SHOULD-level design gaps remain, so the verdict is CHANGES_REQUIRED even though all 131 non-future requirements are executed.

- acceptBlocking requirements unexecuted: **0**
- claimed complete positives that passed schema admission, retained closure, fresh-process replay and their controls: **all 5**
- unresolved MUST issues: **0**
- unresolved SHOULD issues: **2**

## Claimed complete positive Runs

| Run | runId | verdict | objects | blobs | closure checks | replay | controls |
|---|---|---|---|---|---|---|---|
| syntax-code | `run3:0f23a723e1789e1c5...` | pass | 51 | 134 | 616 passed / 17 n-a / 0 refused | MATCH | 14 refused |
| typescript | `run3:c8366533d5cf8b8db...` | pass | 60 | 180 | 778 passed / 5 n-a / 0 refused | MATCH | 14 refused |
| rust | `run3:6eae15420e57f168e...` | pass | 79 | 192 | 844 passed / 18 n-a / 0 refused | MATCH | 14 refused |
| rust-partial | `run3:21cdc5a21431d44bf...` | indeterminate | 88 | 191 | 508 passed / 8 n-a / 0 refused | MATCH | 14 refused |
| syntax-data | `run3:89fdb7e9d5f55a2e7...` | indeterminate | 53 | 136 | 549 passed / 19 n-a / 0 refused | MATCH | 14 refused |

Exported bytes, by SHA-256 of the export file itself:

- `runs/syntax-code.store.json` -> cd6877a54fa7a967e7a8e924637b4a10ad8546e19f3e61520495799d286bd59d
- `runs/typescript.store.json` -> 83696323e3947883ed719723b611ea343570685eb2419db467826efe093d955b
- `runs/rust.store.json` -> 867ce1d1035c70bc6995b01c0255400878e88e37e3f8df233713d439250b32e8
- `runs/rust-partial.store.json` -> bd4d00eb99a487a03f0740497f917dcb20837d64bad87cee8bc380f8a2b32f39
- `runs/syntax-data.store.json` -> dd9752c53555823228ac9d56b1e9be1d75736208c840bd3602183bf59e12a45a

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v16/output/lib/verify_all.py
```

28 stages, all passed: True.

## New MUST issues

None. newMustIssues is EMPTY because every observable this origin was required to produce had a published derivation that it could execute: the C/H recipes, the closing digest law and its four representations and retention modes, the capability-manifest gates, the relation/rung registry with its anchor, snapshot, totality and partition laws, the grammar-capability registry and its three enforcement boundaries, the section 1.2 mode table, the config node-kind law, the Rust context projection, the execution-inputs cell and account derivation, the composition section 9 proof/evidence/seal/Run joins, the repair descriptor and its two idempotency recipes, the comparison and baseline identities, the D9 class/exit table, and the graph-query operations with their bounds and mandatory disclosure. Where a value could not be recomputed (L1-L3 normalisation, symbol-to-path attribution, provider occupancy) the kit SAYS so and substitutes custody, which this origin executed rather than worked around.

## New SHOULD issues

### V16-S1 -- the repair descriptor's closedWorld projection names "that same Run's ClosedWorldV2" without saying which Coverage entry owns it when a Run carries several that differ

- class: ambiguous default
- selectors:
  - `docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json#/$defs/RepairPlanDescriptor/properties/closedWorld (description)`
  - `docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/CoverageResultV3 entry.closedWorld`
- attempted: reconstructing RepairPlanDescriptor.closedWorld as "the five-field PROJECTION of the evidence Run's native ClosedWorldV2 ... each taken unchanged from that same Run's ClosedWorldV2". ClosedWorldV2 is a member of EVERY CoverageResultV3 entry, so a Run with N Coverage entries holds N of them.
- the kit says: the clause is written in the singular ("the evidence Run's native ClosedWorldV2") and pins the projection, the seven-member closure, the two dropped members and the authority direction. It does not publish a selection rule over several entries, nor a requirement that they agree.
- why this is a missing contract rather than algorithm freedom: the five projected values enter repairPlanId, and deadCodeRepairEligible gates every unsafe edit. Two conforming hosts that pick different Coverage entries mint DIFFERENT repairplan2 identities for the same plan, and one may gate an unsafe edit that the other admits. That is an outcome the kit treats as normative, not a strategy it left open.
- measured here: the TypeScript Run used as the evidence Run carries several Coverage entries whose ClosedWorldV2 records reduce to ONE distinct canonical value, so this origin could project unambiguously and did NOT have to choose. The ambiguity was found by measuring the count, and is reported rather than worked around: see vectors/repair-descriptor.json evidenceRun.closedWorldNote.
- smallest fix: one sentence naming the owner -- for example "the ClosedWorldV2 of the Coverage entry of the relation@rung each EvidenceRequirement names, which must agree across the requirements of one plan or REPAIR.CLOSED_WORLD_AMBIGUOUS" -- or a requirement that a Run's ClosedWorldV2 records be equal.
- why not MUST: every other input to the gate and to the identity is published, and a host with agreeing entries (the common case, and this origin's case) reconstructs it exactly. Reconstruction is possible; agreement between hosts is not guaranteed.

### V16-S2 -- GlobPattern publishes a whole-segment `**` and one example, which does not decide whether a TRAILING `**` matches the files of that directory

- class: ambiguous default
- selectors:
  - `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/GlobPattern ("literal characters plus '*', '?' and a whole-segment '**'. No brace, class or escape syntax.")`
  - `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:217 ("`**/*.ts` matches root `a.ts`")`
  - `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md:109 (the same sentence, for rule include/exclude)`
- attempted: admitting a RepairPlanDescriptor whose permittedEditScope is `src/**` against an edit to `src/legacy.js`, and selecting rule subjects with include globs.
- the kit says: the alphabet is closed and ONE semantic fact is published: a LEADING `**/` may match zero segments. Nothing states whether `**` as the FINAL segment matches one-or-more segments, zero-or-more segments, or only directories.
- why this is a missing contract rather than algorithm freedom: permittedEditScope decides whether a repair edit is admissible, and policy include/exclude decides subject enumeration and therefore which findings exist. Both are normative outcomes. Under "zero or more segments" `src/**` matches `src/` only; under "one or more" it matches `src/legacy.js`. Two conforming consumers disagree on admission of the same plan.
- measured here: this origin writes a trailing wildcard as `**/*` so the final segment is matched explicitly, and recorded that choice at the site (lib/phase6_repair.py permittedEditScope). No reconstruction depended on the unstated reading.
- smallest fix: one sentence, or a second published example with a trailing `**`.
- why not MUST: a consumer can always avoid the unstated case by spelling the final segment, so reconstruction is possible.

## Advisories

- **V16-A2** (case not stated) the execution-inputs inventory-kind equality rule does not state the case where a cell binding is UNAVAILABLE
  - observation: the rule that a cell's retained inventory KINDS are set-equal to the cell's declared kinds is stated for an available binding. For an unavailable binding there is no inventory to produce, and the clause does not say whether the equality still applies, is vacuous, or is replaced.
  - handled here by: the check is applied only to an available binding, and the unavailable case is recorded as NOT-STATED rather than given an invented refusal or a fictional inventory. See the INVENTORY_KINDS_SET_EQUAL_TO_THE_CELL check and its not-applicable record in runs/*.closure.json.
- **V16-A3** (wording) `traversalCoverage` and native CoverageResult share the word "coverage" while being different obligations
  - observation: the schema already says "Not native CoverageResult" in both places, which is why this is only advisory. The shared noun still invites a consumer to report a COMPLETE traversal over an INCOMPLETE evidence base as evidence completeness.
  - handled here by: the two are carried in different required fields and reported separately, with an explicit statement of why: see query/graph-query-reconstruction.json evidenceLimitationsVersusStoredEdgeCompletion.

## Withdrawn by this origin, or resolved in the new kit bytes

- **V15-S1 (withdrawn by this origin)** -- WITHDRAWN as over-broad. no annotated site of the native document uses `fragment`, so declining to declare it there is correct. Measured: retention counts are preimage-frame 31, preimage 21, owner-retained 11, closure-tree-member 10, derived 3, and ZERO fragment sites (notes/native-annotated-site-audit.json).
- **V15-A1 (resolved in the new kit bytes)** -- RESOLVED at the source. the v16 native schema replaces it with `siteCountLaw`: "Count syntactic x-opensip-digest annotation occurrences in this schema document; the reference checker reports the measured count. No second hand-maintained total is normative." This origin now MEASURES 76 occurrences and asserts the absence of the old key.
- **V15-observation on the `derived` retention recipe** -- RESOLVED at the source. the v16 native schema declares `derived` with the recipe this origin had already derived from the plan/run capabilityManifestId join; the closure now asserts the declared statement rather than this origin's inference (check_native_digest_law_vocabulary).

## Algorithm freedom that is NOT a gap

- **how a host ENUMERATES subjects**: pinned observable -- SubjectInventoryV1 rows, examinedPaths equal to the Plan census, and the locator identity (planId, parameterDigest, cellOrdinal, programOrdinal, kind); left open -- the traversal strategy, parallelism and caching. the retained record is fully specified, so any strategy is checkable
- **how a normalizer computes an L1-L3 body**: pinned observable -- the framed body identity, the retained level specification bytes, and bodyIdentityJoin.recomputableAt = [L0-verbatim] only; left open -- the normalisation algorithm itself. the kit states in terms that it is NOT recomputable above L0 and demands exact retained preimage custody instead -- a deliberate, published limit, not a missing recipe
- **which shortest path a graph.path returns when several tie**: pinned observable -- canonical fact2-id-sequence tie-break; left open -- the search algorithm. the tie-break makes the RESULT total, so the algorithm is free
- **how a host stores and indexes the evidence store**: pinned observable -- the exported object table plus every blob keyed by its digest; left open -- the storage engine, indexes and compaction. a host index is explicitly never authority; resolution goes through digests

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
| V16-A1 | this origin's own v15 SHOULD about the native retention catalogue | self-correction |

Open helper failures on a claimed positive: **0**.

## Limitations and scope

- Every compiler, provider, toolchain, OS and runtime observation in these Runs is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a compiler, a provider, a host or an operating system, and no such qualification is claimed.
- No product code was written, no repository was modified, no commit or push was made, and no product was executed. Every byte produced lives under this origin's own output directory.
- The parent candidate was never held. Only the disclosed 101-file kit and the parent digest declared inside its manifest were verified.
- No root admission, agreement, expected result, author model, checker or golden was supplied, read or inferred. The root outcome over these exact bytes is UNOBSERVED by this origin.
- Three of the six advertised language modes (ts-tsconfig, js-synthesized, rust-cargo-prepared) have an admitted representable path at the (context, universe) record level but were NOT exercised end-to-end on a sealed Run. That distinction is published in vectors/advertised-mode-paths.json and is not merged into the complete-positive claim.
- L1-L3 normalised body identities, symbol-to-path attribution and provider occupancy are not recomputable by a consumer; the kit says so and substitutes retained custody, which is what was executed. No normalizer, parser or provider is qualified by that custody.
- The repair, comparison, baseline, invocation and query records are RECORD reconstructions with their identities recomputed and their admission laws executed. No repair was previewed, applied or authorized; no baseline was adopted; no query engine was run by a product.

## Standing

- **noRootAdmissionClaim**: this origin reports ONLY its own independently executed admission, closure, replay and controls. It does not claim that any root, author or successor admitted, agreed with or validated these bytes.
- **noProductQualificationClaim**: nothing here authorizes a product implementation or qualifies any product, component, compiler, provider or host.
- **kitOnly**: every citation names a path and selector inside the frozen 101-file kit. No original repository, author model, fixture, golden, report, prior review or other /tmp/opensip-design-corrections directory was read.
- **priorGenerationsUnmodified**: PASS. Newest modification time per generation: consumer-b.v14 2026-09-12T09:15:20Z; consumer-b.v15 2026-09-12T09:39:10Z; consumer-b.v16 2026-09-12T11:10:21Z

