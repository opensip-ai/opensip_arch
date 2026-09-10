#!/usr/bin/env python3
"""Emit review-selfaudit.md/json and successor workflow-review.md/json from probe results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output")
RES = json.loads((OUT / "probes/workflow_selfaudit.results.json").read_text())
PROBE = OUT / "probes/workflow_selfaudit.py"
PROBE_SHA = hashlib.sha256(PROBE.read_bytes()).hexdigest()
RES_SHA = hashlib.sha256((OUT / "probes/workflow_selfaudit.results.json").read_bytes()).hexdigest()

by = {r["id"]: r for r in RES["scope48"]}
c = RES["custody"]


def sha_later(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


selfaudit = {
    "standing": "Same independently fresh kit-only review origin, not a new origin. Review-quality self-audit of consumer-b.v12-kit-workflow-recheck.v3 WORKFLOW_SCOPE_ADMITS. Not authoring. Not product qualification. Not whole-consumer ACCEPT. Frozen Run admission remains unverified and outside this workflow scope.",
    "selfAuditVerdict": "REVIEW_QUALITY_CORRECTIONS_APPLIED",
    "successorVerdict": "WORKFLOW_SCOPE_REFUSED",
    "reasonSuccessorChanged": "Six v3 PASS grades on the 48 in-scope IDs do not survive original kind/verb plus complete owning contract. Five are REFUSED; R-CHAIN-ZERO-CONFIG-TO-RECEIPT is WORKFLOW_SCOPE_INCOMPLETE because frozen Run arrows were silently claimed. First actual refusal: R-CONFIG-CUSTOM-MULTI-BASE.",
    "originalReviewPath": "/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v3/output/workflow-review.json",
    "originalReviewVerdict": "WORKFLOW_SCOPE_ADMITS",
    "didNotChangeConsumerBytes": True,
    "didNotImportConsumerHelperForExpectedValues": True,
    "python": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "writeRoot": str(OUT),
    "reproductionCommand": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output/probes/workflow_selfaudit.py",
    "inputHashes": {
        "snapshotManifestSha256": c["snapshotManifestSha256"],
        "snapshotManifestMatch": c["snapshotManifestMatch"],
        "snapshotFiles": f"PASS {c['independentFilePass']}/{c['listedCount']}",
        "kitManifestSha256": c["kitManifestSha256"],
        "kitManifestMatch": c["kitManifestMatch"],
        "requirementsSha256": c["requirementsSha256"],
        "requirementsMatch": c["requirementsMatch"],
        "checkerSha256": PROBE_SHA,
        "resultsSha256": RES_SHA,
        "v3ReviewMdSha256": "7286cd9b6d5a5874150a0ef949317448ec01ee011574ffbe8247d1222a8f6b3f",
        "v3ReviewJsonSha256": "791f136393510c9f0509109f8aeab0e4a4b0e820b43b0b9c0f082d3ba090d2bf",
        "v3CheckerSha256": "324c8a9115135205be09f17793edf708f3edfa895fe6eac1e221b706759c5f80",
    },
    "v3DispositionCounts": {"PASS": 48},
    "successorDispositionCounts": RES["scope48Counts"],
    "original134Counts": RES["original134Counts"],
    "nOriginal134": 134,
    "firstActualRefusal": RES["firstActualRefusal"],
    "frozenRunAdmission": "unverified",
    "wholeConsumerAccept": False,
    "priorProbeImportedConsumerHelper": True,
    "overbroadRefusalsCorrected": [
        {
            "id": "R-RUN-UNSUPPORTED-GRAMMAR",
            "action": "kept PASS",
            "reason": "Original verb is unsupported-grammar refusal without assuming a TypeScript compiler. Kit dialect.table onUnknown and selectionLaw name both BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN and unsupported-file/no-bundled-grammar. Consumer .rs→rust-syntax vs kit .rs→rs is an existing-law spelling miss, not the required observable.",
        },
        {
            "id": "R-JS-CLONE-BODY-THROUGH-TS",
            "action": "kept PASS on languageId vs provider; did not refuse for unreminted L0",
            "reason": "Original observable is vectors/js-body-through-ts.json with languageId vs provider language. Claimed L0 hashes are not that observable.",
        },
    ],
    "withdrawnPassingGrades": RES["withdrawals"],
    "qualityBoundaries": [
        {
            "id": "QB-INDEPENDENCE",
            "title": "Expected derivation must not use consumer helper output as oracle",
            "finding": "v3 probes/workflow_admit.py imported helper.canonical, helper.identity, helper.evaluator, helper.schema_admit, helper.body_identity. Those are claims under test. Successor reminted C/H from identity-and-evidence.md §3 and did not import consumer helper.",
        },
        {
            "id": "QB-VACUOUS-STOCK",
            "title": "Stock schema / file presence / or-True do not establish original verbs",
            "finding": "v3 R-CONFIG-SYNTHESIZED PASSed via `or True`. v3 custom-multi-base and js-shared PASSed on load() truthiness. Successor reminted raw SHA-256 of C(TypeScriptConfigGraphV1), derived node kind from basename, and checked x-opensip-order path sequence. Synthesized and js-shared hold. Custom-multi-base identity/kind/order hold but repeated-base sequence does not.",
        },
        {
            "id": "QB-QUERY-PARITY",
            "title": "Full response parity is the complete published parity contract, not aggregate counts",
            "finding": "workflows-and-surfaces.md §8: query-response is the complete owner-admitted GraphQueryResponseV1 (full context, items, optional termination). v3 compared runId/availability/truncated/totalItems/nItems. Retained json query-response is {operation, nItems}. Agent omits query-response and termination-class. neighborsPaged sets truncated=true with traversalCoverage=truncated-page (contract: page fullness is truncated-page, truncated=false). nextCursor is retained but page-2 continuation is not. Independently projected neighbors/path/reach item bytes still match.",
        },
        {
            "id": "QB-IDENTITY-RECIPE",
            "title": "Source-record identity derivations are not waived by one pairwise property",
            "finding": "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE is completeRunProperty. Pair vector compares claimed L0 hashes with no retained span/compilerBuild/BLV. identity-schemas.v3: BLV is DERIVED; rust dialect.edition is integer enum. v3 implementation notes recorded string-edition and unretained span and still PASSed. Successor withdraws PASS.",
        },
        {
            "id": "QB-FACTS-NOT-LABELS",
            "title": "Helper agreement tables are not facts/Coverage",
            "finding": "R-MIN-RESOLUTION-THREE-LEVELS original requires qualifying and insufficient facts/Coverage at syntactic, resolved, and type. Retained vector is helper.evaluator.eval_atom value labels plus qualifyingAgrees flags. Independent three-valued law still holds as a synthetic observation; the retained vector does not contain the required facts/Coverage.",
        },
        {
            "id": "QB-CHAIN-AND-FOUR-STATES",
            "title": "Standing exhibition is not a checklist sentence or four labels",
            "finding": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT requires traces, envelopes, and complete Runs together. v3 PASSed a four-arrow workflow checklist with notAChecklistSentence:true. Frozen Run admission is outside this scope and must not be silently claimed → INCOMPLETE. R-EMPTY-PARTIAL-UNAVAILABLE-MISSING requires exhibition across syntax/availability/Coverage artifacts; retained vector is four narrative strings.",
        },
        {
            "id": "QB-NO-INVENTED-CASES",
            "title": "Did not invent fault cases the original verbs do not require",
            "finding": "Did not refuse for missing QUERY.ENDPOINT_AMBIGUOUS/UNKNOWN/PARAMS_MALFORMED, maxVisitedNodes truncated-bound, native-evidence-unavailable, or includeStart default-false as extra cases. Retained neighborsPaged cursor and §8 renderer/summary joins are required by the original observable and owners.",
        },
    ],
    "notes": RES["notes"],
    "scope48": RES["scope48"],
}

selfaudit_md = f"""# Review-quality self-audit of v3 workflow-scope review

**Self-audit verdict: `REVIEW_QUALITY_CORRECTIONS_APPLIED`**

**Successor workflow-scope verdict: `WORKFLOW_SCOPE_REFUSED`**

This is the same independently fresh kit-only review origin, not a new origin. It audits the v3 `WORKFLOW_SCOPE_ADMITS` (48/48 PASS) against original requirement kinds/verbs and complete owning contracts. It is not authoring, not product qualification, and not whole-consumer `ACCEPT`. Frozen Run `close_run` remains **unverified** and outside this workflow scope.

v3 `workflow-review.md` / `workflow-review.json` / probes are preserved. Consumer snapshot bytes were not modified.

First actual refusal on the 48 in-scope IDs: **`R-CONFIG-CUSTOM-MULTI-BASE`**.

## Input hashes (snapshot bytes unchanged)

| Item | Value |
|---|---|
| Snapshot manifest | `{c["snapshotManifestSha256"]}` **MATCH** |
| Snapshot files | **PASS {c["independentFilePass"]}/{c["listedCount"]}**, 0 fail |
| Kit manifest | `{c["kitManifestSha256"]}` **MATCH** |
| `requirements.json` | `{c["requirementsSha256"]}` **MATCH** |
| Independent checker | `probes/workflow_selfaudit.py` `{PROBE_SHA}` |
| Results | `probes/workflow_selfaudit.results.json` `{RES_SHA}` |
| v3 review.md (preserved) | `7286cd9b6d5a5874150a0ef949317448ec01ee011574ffbe8247d1222a8f6b3f` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. No consumer helper import for expected values. C/H reminted from `identity-and-evidence.md` §3.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \\
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output/probes/workflow_selfaudit.py
```

## What v3 got right (confirmed, not authority)

Independently reminted without consumer helper:

- Repair-apply key = raw SHA-256 of `C({{operation, projectId, repairPlanId, baseSnapshotId}})` `206733ee…`, unequal to mutation-intent H `6a2921ca…`.
- `repairplan2:` / `comparison2:` / `baseline2:` identities remint from published H domains; comparison counts from entries.
- Pivot-only first-axis: B=false, E0=true, E4=false → `CODE-NET-NEW`, not live.
- Scope-only comparison: two scope digests unequal, policy digest equal.
- Synthesized config graph `C` digest `432d4a7f…`; js-shared base identity `b4249ca9…`; node `kind` derived from basename; nodes path-ordered.
- Unknown suffix refuses; clones negatives execute firstRefusal codes; JS body languageId `javascript` ≠ provider `typescript`.
- Candidate-only `kinds=[]`; hostCapture labeled synthetic.
- Command inventory join commandCount 45; query parity field *names* match kit; six StepTermination examples inhabit the closed class vocabulary.
- Graph projection: 3 `calls@resolved-callee` edges; neighbors/path/reach item bytes equal claimed; hopCount 1 is shortest; `file@enumerated` → `QUERY.RELATION_UNSUPPORTED`; cursor *form* `q3.<64hex>.<64hex>.<position>`; `underlyingRunAdmissionUnverified` retained.
- Multi-step envelope: two analysis steps with profiles `default` vs `fit`.

Those confirmations do **not** restore v3’s 48-PASS verdict.

## Quality boundary 1 — independence of expected derivation

v3 `probes/workflow_admit.py` imported consumer `helper.canonical` / `identity` / `evaluator` / `schema_admit` / `body_identity`. Artifact metadata and helper output are **claims under test**, not expected-value authority.

Successor implements C (UTF-8 key order, no whitespace) and `H(D,X)` from `identity-and-evidence.md` §3, exists three-valued from the published atom law, graph projection from `query-projection-contract.v3.md` §3, and config node-kind from `native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law`.

## Quality boundary 2 — vacuous and file-presence PASS

v3 `R-CONFIG-SYNTHESIZED` used `or True`. v3 custom-multi-base and js-shared PASSed if the file loaded.

Successor reminted `tsconfigGraphHash = SHA-256(C(graph))`. Synthesized and js-shared **hold**. Custom-multi-base identity, derived `kind=other` for `tsconfig.app.json`, and path order **hold**, but the original verb requires **repeated bases with retained precedence**. `extendsResolved` is `[strict, base]` then `[base]` — a diamond, not a repeated edge in one sequence (`x-opensip-order: sequence`, later-wins). **PASS withdrawn → REFUSED.**

## Quality boundary 3 — query complete owner vs aggregate counts

Original `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` observable: independently derived complete typed responses, failure envelopes, bound/cursor cases, renderer and summary joins. Owners: `query-projection-contract.v3.md` §§1–8, `graph-query.schema.json`, `workflows-and-surfaces.md` §8.

§8: `query-response` is the **complete owner-admitted GraphQueryResponseV1** (full context, items, optional termination). Host projection must be total over `parityFields`. Aggregate/count comparisons cannot substitute.

Measured on retained `query/parity.json` / `rendererParity`:

| Renderer | Required | Actual |
|---|---|---|
| json `query-response` | complete GraphQueryResponseV1 | `{{operation, nItems: 2}}` |
| agent | all six parity fields | `resolvedView` / `availability` / `truncated` / `totalItems` / `items`; **no** `query-response`, **no** `termination-class` |
| human | typed content of the response | scalar `view=… avail=… truncated=False total=2 items=2` |

Further retained-cursor law (not invented):

- `neighborsPaged`: `traversalCoverage=truncated-page` with `truncated=true`. Contract §5 / schema: page fullness is `truncated-page`, **`truncated=false`**. `truncated` is true iff `truncated-bound`.
- `nextCursor` `q3.1908c594….2aabcead….1` form-ok; page-2 continuation **not retained**. Independent remaining neighbor is `fact2:ae187938…`.
- SelectionHash C-domain is unpublished; this audit did **not** invent a hash recipe.
- Did **not** invent `QUERY.ENDPOINT_*`, `maxVisitedNodes` truncated-bound, or `native-evidence-unavailable` as extra required cases.

**PASS withdrawn → REFUSED.** Item-byte equality of neighbors/path/reach remains true and is not the complete owner.

## Quality boundary 4 — identity recipe vs pairwise claimed hashes

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` is `completeRunProperty`. Observable: two retained graphs or an explicit pair vector comparing body identities. Kit: BLV is **derived**; rust `dialect.edition` is integer `{{2015,2018,2021,2024}}`; ownership never enters BLV.

Pair vector: two ownership maps, derived edition 2018, claimed L0 equal; 2021 map moves claimed L0; `SourceUnitOwnershipV1` required fields present. **No** retained span, `compilerBuild`, or BLV record. v3 guessed `pub fn x() {{}}` / `"0"*64` and still PASSed because pairwise claimed-hash equality held, recording string-edition as an implementation note.

Original record-kind and identity obligations are not waived because one isolated property held. Claimed L0 `sha256:aa8162f8…` is not independently remintable from retained preimages. **PASS withdrawn → REFUSED.**

## Quality boundary 5 — facts/Coverage vs helper agreement labels

`R-MIN-RESOLUTION-THREE-LEVELS` original: syntactic, resolved, and type, **each with qualifying and insufficient facts/Coverage**.

Retained `vectors/min-resolution.json` is `helper.evaluator.eval_atom` value labels (`qualifyingAgrees: true`). No facts, no Coverage. Independent synthetic exists law (match→true; no coverage→indeterminate; complete coverage no match→false) agrees with the stored *values*. Helper agreement flags are claims, not expected-value authority. **PASS withdrawn → REFUSED.**

`R-MIN-RESOLUTION-REPAIR-EVIDENCE` independently remints `repairplan2:90fbc873…` and binds three rungs — **PASS retained**.

## Quality boundary 6 — standing exhibition vs checklist / labels

`R-CHAIN-ZERO-CONFIG-TO-RECEIPT` (`standingRule`): exhibited by executed traces, envelopes, **and complete Runs** together, not a checklist sentence. v3 PASSed four workflow-file arrows plus `notAChecklistSentence: true`. No Run arrow, no trace arrow. Frozen Run admission is **outside this workflow scope** and must not be silently claimed. **PASS withdrawn → `WORKFLOW_SCOPE_INCOMPLETE`.**

`R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` (`standingRule`): exhibited across syntax/availability/Coverage artifacts; a single label for all four is failure. Retained vector is four narrative strings + `distinct: true`. **PASS withdrawn → REFUSED.**

Standing owner-map / cited-distinction IDs (`R-SUBSYSTEM-OWNERS`, `R-SEMANTIC-VS-OPERATIONAL-AUTHORITY`, `R-MUTATION-VS-ANALYSIS-STEPS`, `R-PROMISE-VS-AVAILABILITY`) remain PASS: those original observables *are* cited reconstruction maps.

## Overbroad refusals corrected

v3 issued **no** refusals on the 48 (all PASS). This audit does **not** refuse:

- `R-RUN-UNSUPPORTED-GRAMMAR` for `.rs` → `rust-syntax` vs kit `rs` (unknown-suffix refusal is the verb).
- `R-JS-CLONE-BODY-THROUGH-TS` for unreminted L0 (languageId vs provider is the verb).

No new schema or requirement was invented.

## Disposition vs v3

| | v3 | successor |
|---|---:|---:|
| PASS | 48 | **42** |
| REFUSED | 0 | **5** |
| WORKFLOW_SCOPE_INCOMPLETE | 0 | **1** |
| **in-scope assessed** | **48** | **48** |

Withdrawn PASSes: `R-CONFIG-CUSTOM-MULTI-BASE`, `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`, `R-MIN-RESOLUTION-THREE-LEVELS`, `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` (REFUSED); `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` (INCOMPLETE).

## 134-ID mapping (outside-scope retained)

| thisReview | Count |
|---|---:|
| in-scope-executed-PASS | 42 |
| in-scope-executed-REFUSED | 5 |
| in-scope-INCOMPLETE | 1 |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| notReached-historical-vector | 23 |
| out-of-scope-frozen-run | 24 |
| out-of-scope-frozen-run-replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Frozen Run stores remain byte-identical and **unverified** for `close_run`. Whole-consumer `ACCEPT` is **not** issued.

Successor machine-readable review: `workflow-review.json`. Self-audit machine-readable: `review-selfaudit.json`.
"""

(OUT / "review-selfaudit.json").write_text(json.dumps(selfaudit, indent=2) + "\n")
(OUT / "review-selfaudit.md").write_text(selfaudit_md)

# successor workflow-review.json
wf = {
    "reviewer": RES["reviewer"],
    "verdict": "WORKFLOW_SCOPE_REFUSED",
    "standing": "Successor bounded independent kit-only review after self-audit of v3 WORKFLOW_SCOPE_ADMITS. Same fresh origin. Frozen Run/replay IDs remain out of scope and unverified. Not whole-consumer ACCEPT. Not product qualification. Not root admission. Prior positive grades were hypotheses, not authority.",
    "structuralOutcome": "WORKFLOW_SCOPE_REFUSED",
    "semanticOutcome": "independent C/H/query/atoms/config reminted from kit; consumer helper not oracle",
    "python": RES["python"],
    "writeRoot": RES["writeRoot"],
    "inputHashes": selfaudit["inputHashes"],
    "frozenRunStoresVerifiedByteIdentical": RES["frozenRunStoresVerifiedByteIdentical"],
    "frozenRunAdmission": "unverified",
    "reproductionCommand": selfaudit["reproductionCommand"],
    "firstActualRefusal": RES["firstActualRefusal"],
    "scope48Counts": RES["scope48Counts"],
    "scope48": RES["scope48"],
    "withdrawnFromV3Pass": [w["id"] for w in RES["withdrawals"]],
    "original134Counts": RES["original134Counts"],
    "original134": RES["original134"],
    "nOriginal134": 134,
    "absentOrContradictoryLaws": [],
    "implementationMissesVsAbsentLaw": [
        "Consumer helper SYNTAX_SUFFIX_TABLE maps .rs to 'rust-syntax'; kit languageVersionBinding dialect table maps .rs to 'rs'. Unknown-suffix refusal is the required behavior for R-RUN-UNSUPPORTED-GRAMMAR and was independently executed. Token spelling is not that requirement's observable.",
        "Consumer rust_body_l0 / pair-vector claimed L0 cannot be reminted from retained BLV/span. That is an unmet identity-recipe obligation of R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE (completeRunProperty), not an absent kit law.",
    ],
    "wholeConsumerAccept": False,
}

(OUT / "workflow-review.json").write_text(json.dumps(wf, indent=2) + "\n")

gq = by["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"]["detail"]
cmb = by["R-CONFIG-CUSTOM-MULTI-BASE"]["detail"]

wf_md = f"""# Workflow-scope independent review (successor after self-audit)

**Verdict: `WORKFLOW_SCOPE_REFUSED`**

This is a bounded independent kit-only review of another actor’s authored workflow snapshot, after a review-quality self-audit of the v3 `WORKFLOW_SCOPE_ADMITS`. Same fresh origin, not a new origin, and **not** independent acceptance of this reviewer’s own prior authoring. Frozen Run stores were hash-verified only; their `close_run` admission is **unverified**. This is **not** whole-consumer `ACCEPT`.

First actual refusal on the 48 in-scope IDs: **`R-CONFIG-CUSTOM-MULTI-BASE`**.

## Input hashes

| Item | Value |
|---|---|
| Snapshot manifest | `{c["snapshotManifestSha256"]}` **MATCH** |
| Snapshot files | **PASS {c["independentFilePass"]}/{c["listedCount"]}**, 0 fail |
| Kit manifest | `{c["kitManifestSha256"]}` |
| `requirements.json` | `{c["requirementsSha256"]}` |
| Independent checker | `probes/workflow_selfaudit.py` `{PROBE_SHA}` |
| Results | `probes/workflow_selfaudit.results.json` `{RES_SHA}` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Source metadata names `/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output` — that actor directory was **not** read. Snapshot bytes were not reminted. Consumer helper was **not** used as expected-value oracle.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \\
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output/probes/workflow_selfaudit.py
```

## 134-ID mapping (outside-scope retained)

| thisReview | Count |
|---|---:|
| in-scope-executed-PASS | **42** |
| in-scope-executed-REFUSED | **5** |
| in-scope-INCOMPLETE | **1** |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| historical vector notReached | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Full rows: `workflow-review.json#/original134`. Copied historical claims are not accepted by copy.

## First actual refusal

**`R-CONFIG-CUSTOM-MULTI-BASE`** (`standaloneConfigVector`).

Original: custom-named project config inheriting from multiple ordered bases, **including repeated bases with retained precedence**. Owner: `TypeScriptConfigGraphV1.nodes[].extendsResolved` is a **sequence** (later entry wins); repeated edges are retained.

Independently reminted `C(graph)` digest `{cmb["digest"]}` **matches** claimed `{cmb["digest"]}`. Node kinds derive from basename (`tsconfig.app.json` → `other`). Nodes are path-ordered. Entry extends `[tsconfig.strict.json, tsconfig.base.json]` — multiple ordered distinct bases. **No node’s `extendsResolved` contains a repeated edge.** A diamond in which `tsconfig.base.json` is reached from two parents is not the required repeated-base sequence.

v3 PASSed on file presence. That grade is withdrawn.

## Other in-scope refusals

### `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`

Independently projected **3** `calls@resolved-callee` edges; neighbors/path/reach **item bytes equal** claimed; hopCount **1** is shortest; `file@enumerated` refuses `QUERY.RELATION_UNSUPPORTED`; failure envelope is CommandEnvelope `kind=failure` with no `run` field; cursor form ok; `underlyingRunAdmissionUnverified` retained.

Unmet complete owner (`query-projection-contract.v3.md` §§1–8 + `workflows-and-surfaces.md` §8):

- json `query-response` is `{{operation: graph.neighbors, nItems: 2}}`, not complete GraphQueryResponseV1.
- agent renderer omits `query-response` and `termination-class`.
- human renderer is aggregate counts, not typed response content.
- `neighborsPaged`: `traversalCoverage=truncated-page` with `truncated=true` (law: page fullness ⇒ `truncated=false`).
- `nextCursor` retained; page-2 continuation **not** retained. Independent remaining neighbor: `{gq["page2ExpectedFactId"]}`.

v3 aggregate runId/availability/truncated/totalItems/nItems comparison is withdrawn as a substitute for full parity.

Did **not** invent `QUERY.ENDPOINT_*`, visited-node cap, or `native-evidence-unavailable` cases.

### `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`

`completeRunProperty`. Two ownership maps, derived edition 2018, claimed L0 equal; 2021 moves claimed L0. **No retained span / compilerBuild / BLV.** Kit identity recipe is not remintable from this pair vector. Pairwise claimed-hash stability of a non-kit encoding does not satisfy the property. v3 implementation-note waiver is withdrawn.

### `R-MIN-RESOLUTION-THREE-LEVELS`

Retained vector is helper `eval_atom` value labels, not qualifying/insufficient facts/Coverage at three levels. Independent synthetic exists law still yields indeterminate / false / true as published. Helper `qualifyingAgrees` flags are claims under test.

### `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING`

`standingRule`. Four narrative strings are not exhibition across syntax/availability/Coverage artifacts.

## In-scope incomplete (not a silent Run claim)

**`R-CHAIN-ZERO-CONFIG-TO-RECEIPT`** (`standingRule`): original exhibition is traces, envelopes, **and complete Runs** together, not a checklist sentence. Retained four arrows are workflow files only (`notAChecklistSentence: true` is itself a flag). Frozen Run admission stays **out of scope / unverified**. This ID is `WORKFLOW_SCOPE_INCOMPLETE`, not a `close_run` claim.

## In-scope PASS (42) — selected current owners

Repair/comparison/baseline H remints, mutation-intent inequality, pivot/scope/E0–E3 classifications, synthesized and js-shared config identities, candidate-only cells, host-capture synthetic label, clones negatives with firstRefusal, JS languageId vs provider, unknown-suffix refusal, multi-unit missing advertised clones, inventory join (45), six StepTermination examples, CommandEnvelope failure shapes + D9 exit join, single-step and multi-step (default vs fit) InvocationRecords, durable receipt/availability nested records, detector listing-file vs manifest-body, three-valued exists vector `indeterminate`, repair-evidence plan identity bound to three rungs, test/prep/repair authorization envelopes, cited standing owner maps.

Per-ID selectors: `workflow-review.json#/scope48`.

## Frozen Runs

Five stores match `frozen-run-hashes.json` byte-for-byte. That is **not** Run admission.

## Limitations (not waivers)

1. Frozen Run `close_run` / other-Run replay remain out of scope.
2. `ROOT-ADMISSION` of exported frames was not performed.
3. Real host/OS/compiler/crypto is future qualification.
4. SelectionHash C-domain is unpublished; form was checked; a hash recipe was not invented.
5. Whole-consumer `ACCEPT` is **not** issued.

Genuinely absent/contradictory kit laws: **none**. Existing-law implementation misses are listed in `workflow-review.json#/implementationMissesVsAbsentLaw` and are not treated as missing design.
"""

(OUT / "workflow-review.md").write_text(wf_md)

for name in ("review-selfaudit.md", "review-selfaudit.json", "workflow-review.md", "workflow-review.json"):
    p = OUT / name
    print(name, hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size)
print("n134", len(wf["original134"]), "verdict", wf["verdict"])
print("selfaudit keys ok", "withdrawnPassingGrades" in selfaudit)
