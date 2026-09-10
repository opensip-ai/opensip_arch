# Self-audit of workflow-review.v1

**Successor outcome: `WORKFLOW_SCOPE_REFUSED`**

This is a bounded self-audit of the just-completed workflow-review.v1. It is not a new fresh origin, not a pilot admission review, and not whole-consumer ACCEPT. Historical v1 reports, diagnostics, and consumer bytes were **not edited**. Consumer vectors were **not reminted**. Probe counts are not conformance counts.

## Custody (reverified)

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| snapshot-manifest.json | `9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c` | **224/224 PASS**, 0 extras |

Frozen Run stores still match `frozen-run-hashes.json`. Those hashes were verified; the Runs were **not** admitted here.

Independent expected behavior was derived from the kit. Consumer evaluators were not oracles. `scope_reconstruct.py` was not executed (it writes).

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output/diagnostics/self_audit_probes.py
```

Self-audit probes: 169 checks, 143 pass, 26 fail. Those are diagnostic probe counts, not 134-ID conformance counts. Historical v1 114/101/13 likewise.

D-CORR-SA-1: first detector-compat kit-substring fail was markdown backticks around `closure.manifestDigest`. Original fail preserved at `diagnostics/self_audit_probes.original-detector-backtick-fail.json`. Kit text does contain the listing-vs-manifest split.

## Withdrawals of v1 reconstructed admits

v1 admitted 39 reconstructed rows. Six of those admits are withdrawn. The historical v1 review is left unchanged; the correction lives only here.

| ID | v1 grade | Why withdrawn | Evidence class |
|---|---|---|---|
| `R-REPAIR-APPLY-KEY` | admitted-schema-or-digest | `applyKey` is `{kind, repairPlanId, snapshotId, requestId, stepId}`, not `C({operation, projectId, repairPlanId, baseSnapshotId})`. v1 accepted SHA-256 inequality of two arbitrary records. | invalid produced key |
| `R-PIVOT-ONLY-FINGERPRINTS` | admitted-schema-inhabitance | Schema pass. Entry `presence.B=true` and `E0=true` — not a fingerprint present only in a pivot. `counts.DETECTION-DELTA=0` against classification `DETECTION-DELTA`. | invalid produced example |
| `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` | admitted-as-cited-standing-vector | Original verb forbids a checklist sentence. Artifact is a four-arrow checklist. | checklist, not exhibition |
| `R-MULTI-UNIT-MISSING-CAPS` | admitted-as-cited-standing-vector | Kind is `standaloneConfigVector`. Named lists of units/caps are not an executed zero-config selection. | citation, not reconstruction |
| `R-CANDIDATE-ONLY-CLONES` | admitted-as-cited-standing-vector | Kind is `standaloneConfigVector`. `cellKindsMustBeEmpty=true` is not `kinds=[]` plus `candidateSourcePaths`. | citation, not reconstruction |
| `R-HOST-CAPTURED-VS-CANDIDATE` | admitted-as-required-kind | Two gloss strings are not host-captured vs candidate-only returns from retained observations. Cited kit law exists. | citation, not reconstruction |

## Nine v1 refusals, rechecked

Unexercised declared `firstRefusal` is distinct from an invalid produced value.

| ID | Keep? | Class | Notes |
|---|---|---|---|
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | keep refused | insufficient produced pair | Two selection labels on one L0 (edition 2018). No retained `SourceUnitOwnershipV1` preimages. Equality is tautological because ownership never enters BLV. |
| `R-RUN-UNSUPPORTED-GRAMMAR` | keep refused | **unexercised** | Declared `unsupported-file` flag. Suffix/grammar-bundle admission not run. |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | keep refused | **unexercised** | Declared firstRefusal dicts. Native context/universe admission not run. |
| `R-CLONES-NEGATIVE-VECTORS` | keep refused | **unexercised** | Hand-raised `AdmissionError` wrappers / assigned dicts. |
| `R-REPAIR-AUTHORITY-PER-TARGET` | keep refused | **unexercised** | Constructed firstRefusal; not an executed correspondence join. |
| `R-MIN-RESOLUTION-THREE-LEVELS` | keep refused | incomplete existing law + invalid expected | Type level has no qualifying case. Measured resolved insufficient `false` agrees with kit complete-absence; `insufficientExpected=indeterminate` does not. |
| `R-MIN-RESOLUTION-REPAIR-EVIDENCE` | keep refused | incomplete existing law | Prose `tiedTo` min-resolution.json, not repair-evidence records. |
| `R-SCOPE-POLICY-ONLY-COMPARISON` | keep refused | **invalid produced value** | Schema pass. Identical `scopeDigest` `5abc279f…` with `contextDelta.scopeChanged=true`. |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | keep refused | **invalid produced value** | All four ops request `file@enumerated` (graph-projectable no) and were answered as success. Failure envelope is `QUERY.VIEW_UNKNOWN`, not `QUERY.RELATION_UNSUPPORTED`. |

### Withdrawn v1 refusal *grounds* (row still refused)

For `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` only:

- **Cursor `"c1"`.** The artifact `query/graph-query-bundle.json` has `"nextCursor": null`. Section 5 allows empty `nextCursor` on a complete page. The v1 MD overstated the token. The v1 probe `gq-cursor-is-reference-form` passed via `else True` when `nextCursor` is missing.
- **Empty `coverageIds` as an independent defect.** Section 6 derives `coverageIds` / `scopeIds` from selected views and other retained Coverage whose key relation is the declared query relation. That is not a universal nonempty rule. v1 probe `gq-evidence-coverageIds-from-selected-views` used `bool(coverageIds)`.

`underlyingRunAdmissionUnverified` remains correctly labelled and does not license answering an unsupported relation.

## Identity recipes vs arbitrary digests

| Claimed identity | Selected kit recipe | Observed |
|---|---|---|
| repair-apply key | raw SHA-256 of `C({operation, projectId, repairPlanId, baseSnapshotId})` | **not that preimage** → refused |
| mutation replay scope | `MutationReplayScopeV1` with generic `operation` (not `repair-apply`); receipt key is `H("workflow.mutation-intent", scope)` | schema-valid `operation=purge` → admitted as the reconstructed record, not as a digest pair |
| `repairPlanId` | `repairplan2:` + `H("workflow.repair-plan", descriptor)` | claimed `b4ab1ea5…`, selected `d1c17ff9…` → schema inhabitance retained, identity not the recipe |
| comparison2 / baseline2 | `H("workflow.comparison"\|"workflow.baseline", descriptor)` | none of the four measured CASE ids match → CASE distinguishing fields still hold for missing / evidence-changed / empty / E0-vs-E1-E3 / baseline-audit |

## Comparison descriptors and standing content

Missing vs evidence-changed is substantiated (`comparisonPerformed` false vs true; `wholeIndeterminateReason` `required-evidence-unavailable` vs `evidence-availability-changed`). Empty-result has `entries=[]` and `zeroFindings=true`. E0 vs E1–E3 is substantiated by `pivotsAvailable` and `presence` (E0-available vs E1–E3-available). Pivot-only is **not** substantiated (see withdrawal).

Standing documents were read, not merely listed as present:

- Promise vs availability: `native-evidence.md` advertised cells vs capability-manifest / release declaration.
- Four empty/partial/unavailable/missing states: `enumeration-contract.v1.md` (complete-empty is not candidate-only `kinds=[]`; missing retained bytes are structural).
- Detector listing vs manifest: `workflows-and-surfaces.md` §2 `.opensip/detector-compatibility.json` vs `closure.manifestDigest`.
- Mutation vs analysis / semantic vs operational / subsystem owners: cited kit owners match.

## v1 aggregate correction

v1 markdown listed frozen out-of-scope as **39** *and* futureQualification as **3**, and claimed total 134. Those rows sum to 137. `validatorDisposition: out-of-scope` already included the three futureQualification ids (24 frozen-run + 12 frozen-replay + 3 future = 39). The 3 were double-counted in the table. Per-ID rows were 134 and overlap with the charter (8 standing + 123 requirements + 3 future) is exact.

Corrected reviewedScope: reconstructed 48 + continuation standing 24 + notReached 23 + frozen-run 24 + frozen-replay 12 + future 3 = **134**.

## Laws

Genuinely absent or contradictory published laws: **none** (`newMustIssues` / `newShouldIssues` empty).

Incomplete consumer implementation of existing laws: the 15 refused reconstructed IDs.

## 134 original IDs after audit

| reviewedScope | Count |
|---|---:|
| in-scope reconstructed, independently **refused** | 15 |
| in-scope reconstructed, admitted as published kind | 33 |
| standing of consumer continuation (not re-executed here) | 24 |
| historical vector notReached this pass | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Full rows: `review-self-audit.json`, successor `workflow-review.json#/originalRequirementIds`, `diagnostics/id-dispositions.json`.
