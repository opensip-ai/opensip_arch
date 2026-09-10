# Review-quality self-audit of v3 `PILOT_ADMITS`

**Successor outcome of the scoped recheck: `PILOT_REFUSED`.**  
This document audits the v3 review, not the consumer authoring. The v3 report is preserved unedited.

v3 path: `/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-recheck.v3/output/pilot-review.md` SHA-256 `8ad475d831bedcbf6eeb5da5198b16437494a2b8eb1c5b9fde0c71fc0781fdec`.  
v3 JSON SHA-256 `a63d5de08d8ef403a4cad46a3de215c1cc0f52c927b16ee6a1a50472c5dcc642`, outcome still `PILOT_ADMITS`.

Snapshot-manifest `33507ddb3d006027834dd4c3552ec33193717b97cfc37e19644dd274e01cad1d` **264/264 PASS**. Kit 80/80 `ea2fa750…`. Requirements `855a1464…`. Snapshot bytes were not reminted. No root diagnostic, author fixture, or peer diagnosis was used.

## What v3 treated as authority (withdrawn)

Prior positive grades and independently reproduced C-equality were hypotheses. The following v3 grades are **withdrawn** as authority. The v3 files themselves are not edited.

| Withdrawn grade | Defect |
|---|---|
| Joint `PILOT_ADMITS` | Tamper replacement graph was not a complete admitted graph. Semantic C-unequal was reported anyway. |
| “Independently reconstructed expected proof” | `reconstruct_expected_proof` copied claimed `proof.executionPlanId`, `proof.ruleProgramDigest`, and `proof.predicateProofs[0].scopeIds[0]` into the expected record. Equality to the consumer claim cannot prove a shared selected-input derivation. |
| `evidence-proof-join` PASS | Checked object-table typedId self-identity, not `evidence.proofBundleId` ↔ `H(proof-bundle)` ↔ `seal.proofBundleId` ↔ `run.evidenceId`. |
| `coverage-payload-*` / `ruleProgram-retained` / `policyDigest-retained` PASS | Equated blob-key presence with the payload-registry document-byte join, C remainder, and selector inhabitance. |
| 129/129 executed applicable laws; `existingLawImplementationMissesOnTheseExports: []` | Probe count is not a charter-conformance count. Stock schema plus H-frame plus C-equality of a claimed-field reconstruction is not the complete join set. |
| Tamper `structuralAdmission: PASS` then first refused boundary `tamper-complete-proof-C-unequal` | Distinct reminted identities and equal selected-input bytes are not complete graph admission. |

## Missed existing laws (now executed)

These laws already existed in the selected current owners. v3 did not pair them with actual operands. They are not new requirements.

- `identity-schemas.v3.json#/x-opensip-payload-registry` relation class: `fact.payloadSchemaDigest` = SHA-256 of the **exact full bytes** of `relation-payload-schemas.v2.json` (`53380a24…`); payload blob = `C(payload)`; validation by the relation-row selector, never `json.loads` and never whole-bundle inhabitance.
- Coverage class: envelope `schemaVersion` 2; payload `schemaVersion` 3; `payloadSchemaDigest` = SHA-256 of exact full `native-evidence.schemas.v2.json` (`a87331bc…`); `CoverageResultV3` selector.
- `coverageTotalityLaw` for `file@enumerated` complete Coverage over inventoried subjects, discharged only by same-universe facts (`matchOn` includes both universes and snapshotId).
- `coveragePartitionLaw` disjoint `subjects` per `(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` within one view.
- File `snapshotJoins` inventoried-file: path ∈ `snapshot.sourceInventory` **and** `contentSha256` **and** `byteLength` **and** retained-bytes rehash. Blob presence is not that join.
- `anchorLaw` cardinalities: inventory exactly 0, clones exactly 1, source-text minimum 1.
- `languageVersionBindingLaw`: L0 `languageVersion` is the raw 32 bytes of `SHA-256(C(body-language-version))` rebuilt from the syntax native-context grammar bundle plus longest-suffix dialect. An opaque claimed `bodyIdentity` hash is not the join.
- `closureMembership.equalToDirect`: `fact.producerClosure` equals enclosing `view.producerClosure` (kind=provider); `proof.evaluatorClosure` equals `seal.evaluatorClosure` equals `exec.evaluatorClosure` (kind=evaluator).
- Grammar artifacts via `plan.nativeContextDigests` and registered `closureJoins` (`kind=grammar` tree members include `bundleDigest`, each `grammarDigest`, and `normalizer.specificationDigest`). Flattening into `semanticClosures` is not the law.
- `execution-inputs-contract.v1.md` §1 `selectedRefs` **exact totality** (complete receipt `outputRefs` ∪ captured view `coverageIds` ∪ cell-outcome inventories ∪ Plan `importIds`), not a subset and not `n==4`.
- `seal.policyDigest == plan.policyDigest` with C remainder; v3 checked blob presence.
- `evidence.coverageIds` equals the union of selected views’ `coverageIds`; `evidence.importIds` equals `plan.importIds` (`IMPORT_JOIN`); `evidence.findingIds` equals `proof.findingIds`.
- Composition §7 reconstructs evidence, seal, and Run preimages, not only proof C.
- Composition §3 claimed predicate value must agree with retained witness `matchingFactIds` (none with known match is false).
- Composition §4 `emitWhen=true` emits exactly one `finding3`.
- `nativeCoverageAccounts` `supported-available` `coverageIds` **equals** matching returned partitions, not a subset.
- Rule program is the Plan-selected policy projection; copying `proof.ruleProgramDigest` into the expected proof is not that join.
- Universe `nativeContextId` equals `sha256:` + Plan native-context digest.

## Checker-logic defects corrected

| Equivocation | Required join |
|---|---|
| Blob key present | Document-byte SHA-256, C remainder, selector inhabitance, tree membership |
| Field present / typedId self-identity | Cross-record H/C equality of the named owners |
| Equal generated bytes of a reconstruction that read claimed proof fields | Derivation from Plan, ExecutionInputs, enumeration, policy, view/facts/coverage/inventories only |
| Distinct reminted run/proof/evidence/seal identities | Complete admitted replacement graph, then semantic C compare |

The expected proof on this audit used **zero** claimed proof fields. Derived `executionPlanId` came from `ExecutionInputsV1.executionPlanId`. Derived `ruleProgramDigest` came from `C({schemaVersion:2, policyDigest:plan.policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]})`. Derived `scopeIds` came from the view’s `file@enumerated` scope whose `subjects` contain the enumerated native id.

After that correction, positive complete proof/evidence/seal/run C still equal the claimed records (proof C SHA-256 `8764a0ac…`, proof `proof3:0388fb97…`). That equality is now a comparison operand, not the construction method. It does not authorize the tamper graph.

## Measured boundaries

### Positive export

**First refused boundary: none** among executed applicable laws. Structural admission passed. Independent semantic replay passed (proof, witness, evidence, seal, Run).

### Tamper export

**First refused boundary (structural, before semantic replay):** `tamper-claimed-predicate-value-agrees-with-retained-witness-matches-0`.

- Selector: composition §3; none with known match is false.
- Operands: claimed `predicateProofs[0].value` = `true`; retained witness `matchingFactIds` = [`fact2:852404c1…` file fact]; derived from those matches = `false`; operation = `none`.
- The tamper proof reminted H identity (`proof3:94c13996…`) while keeping the positive witness digest `111728e6…`. Distinct proof identity is not the complete join.

**Later structural refusal on the same graph:** `tamper-claimed-emitWhen-true-has-finding3-0` — claimed value `true`, `findingIds` `[]`. Composition §4 requires one `finding3` per true `emitWhen`.

**Semantic replay: `notReached`.** Complete admitted graph must precede any semantic-tamper claim. v3’s `tamper-complete-proof-C-unequal` semantic refuse is withdrawn as a reached boundary.

### notReached (both graphs; not refusals)

| Item | Why |
|---|---|
| L1 token-stream tokenisation judgment | Frame/custody and outer/token-count prefixes were parsed. Tokenisation judgment is level-spec freedom. |
| `component-manifest-schemas.v11` stock inhabitance | Prose field contract, not an executable stock JSON Schema. No invented validator. Stored-bytes/tree join remains the check. |
| Tamper semantic replay | notReached because structural admission of the replacement graph failed. |

## Executable inventory

`diagnostics/pilot_selfaudit_probes.py` — 240 probes, 237 pass, 3 fail (the two tamper composition joins and the gated `tamper-structural-before-semantic` marker). 142 laws that v3 missed now execute and pass on the **positive** graph and on tamper **input** joins. Probe counts are still not whole-charter conformance counts.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-selfaudit.v4/output/diagnostics/pilot_selfaudit_probes.py
```
