# Proof-output derivation peer

**Verdict: `CORRECTIONS_REQUIRED`**

Not blind. Not whole-design acceptance. Not source application or readiness.

Proposed four files are byte-identical to `/tmp/opensip-design-corrections/target-proof-successor.v1`. Frozen24 was used only as beforeimage. Independent §9 verification is against admitted owning laws and the successor reference callgraph, not against the already-applied inventory-digest / binding-carrier / refuse / future-profile edits.

A passing checker or a passing isolated `compose` is not acceptance. Isolated adapter injection is not a Run.

## Standing

| Layer | What it is | What it is not |
|---|---|---|
| `execution_inputs_model.v1.admit_execution_inputs` | Internal `requiredCellDeficiencies` / `derivedAccounts` | Not `evaluation-deficiency`. Not a Run |
| `evaluator_input_model.v3.execution_input_account` | §9.6 proof bridge (`row.deficiency` → cause; `{XI} ∪ row.inputRefs`) | Not a Run |
| `evaluator_replay_model.v3.scanner` | Atom → witness/deficiency mapping; unregistered/wrong-plane refuse; Coverage-entry `inputRefs` overwrite | Not a Run |
| `evaluator_composition_model.v3.compose` | Proof/witness/finding dicts from normalized inputs + substituted scanner | Not owner admission. Not atom replay. Not a Run |
| `evaluator_replay_model.v3.derive` | reconstruct + actual atom scanner + compose | Proof preimages only |
| `identity-model.v3.close_run` | Public complete replay on a minted Run | Synthetic fixture here; not compiler qualification |

`compose` copies `scan_atom.inputRefs` and does not itself assign `EI`. The production adapter (`evaluator_replay_model.v3.scanner`) does. Schema `identifier` validation also refuses an unregistered `cause` enum at proof mint, which is not the §9.5 `EVALUATOR_ATOM_CAUSE_UNREGISTERED` admission key.

## MUST findings

### MUST-1 — §9.7 does not publish Seal3 / Run3 field value sources

§9 opens as the normative mapping to proof, witness, finding, evidence, seal, Run and policy-derivation bytes. Evidence3 and policy-derivation3 receive field lists. Seal3 / Run3 receive “existing identity recipes” plus `identifier` plus `verdict = proof.verdict`.

Schema required fields name the keys. They do not assign the values. Identity-and-evidence §3 gives `H(D,X)`, not the join from proof/Plan/snapshot into those keys. A normative-only consumer cannot reproduce seal/run bytes from the four files without reading `evaluator_replay_model.v3.replay` / `seal_derived`.

**Correction.** Replace the Seal3/Run3 sentence with the same table style as Evidence3:

Seal3 `{schemaVersion:3, planId, executionPlanId, evidenceId, evaluatorClosure, policyDigest, proofBundleId, verdict}`:

| Field | Bytes |
|---|---|
| `planId` | `proof.planId` |
| `executionPlanId` | `proof.executionPlanId` |
| `evidenceId` | `H(semantic-evidence, evidence3)` |
| `evaluatorClosure` | `proof.evaluatorClosure` |
| `policyDigest` | admitted Plan `policyDigest` |
| `proofBundleId` | `H(proof-bundle, proof)` |
| `verdict` | `proof.verdict` |

Run3 `{schemaVersion:3, projectId, snapshotId, planId, evidenceId, evaluationSealId, capabilityManifestId}`:

| Field | Bytes |
|---|---|
| `projectId` | admitted snapshot `projectId` |
| `snapshotId` | admitted Plan `snapshotId` |
| `planId` | `proof.planId` |
| `evidenceId` | seal `evidenceId` |
| `evaluationSealId` | `H(evaluation-seal, seal3)` |
| `capabilityManifestId` | admitted Plan `capabilityManifestId` (schema `capability-manifest-id` recipe) |

Do not name `identifier`, `seal_derived`, or `replay`.

### MUST-2 — `identifier` is a reference helper name, not field law

§9.7: “Evidence, seal and Run H ids are `identifier` of those descriptors.” `identifier` is `identity-model.v3.identifier`. Identity-and-evidence §3 already owns `H(D,X)`.

**Correction.** For every minted output id (`finding3`, `proof3`, `evidence3`, `seal3`, `run3`, `policy-derivation3`, `subject3`, `finding-key2`):

`H(D,X) = prefix(D) + ':' + lowercase-hex(SHA256(ASCII("opensip.product.v1") ‖ 00 ‖ ASCII(D) ‖ 00 ‖ uint64BE(len(C(X))) ‖ C(X)))`

with `prefix` from `x-opensip-prefix` and `C` from identity-and-evidence §3. `proof.findingIds` / `waivedFindingIds` are `Cset` of those `finding3` ids.

### MUST-3 — `program-predicate` description names RuleProgramV1

`identity-schemas.v3.json#/$defs/program-predicate` description: “admitted RuleProgramV1”. Its `ruleProgramDigest` annotation and composition §9.1 / §9.3 use `RuleProgramV2`. Every witness hashes this record.

**Correction.** Replace `RuleProgramV1` with `RuleProgramV2` in that description. Do not add a second program identity.

## Independently verified (no new fields invented)

Root-already-corrected items re-checked and they hold:

- Inventory originating digest is `SHA-256(C(inventory))`, not a helper name.
- Required unavailable binding / null universe keeps the binding carrier with `inputRefs=[]` (proof: `{XI}` only). Each non-complete same-cell inventory is a separate item with its own inventory ref. Actual `admit_execution_inputs` on the unavailable-binding+partial-inventory fixture: 4 internal binding rows with empty refs (full cell/relation coordinates) + 1 inventory row; §9.6 bridge `Cset`s to 2 proof items. Two partial inventories keep two distinct inventory refs.
- Unregistered / wrong-plane atom causes refuse in the replay adapter (`EVALUATOR_ATOM_CAUSE_UNREGISTERED` / `EVALUATOR_ATOM_CAUSE_PLANE_JOIN`). Native diagnostic codes such as `uncovered-expected-source-subject` are native-registry, not execution-bridge `cause`. Internal tokens `native-work-incomplete` / `unsupported-typed` are not proof causes; bridge reads `row.deficiency`.

Remaining §9 formulas vs owning schema / emission:

| Topic | Law | Emission |
|---|---|---|
| Proof required keys | §9.1–§9.7 name all 14 schema-required proof fields | `compose` emits exactly those keys |
| `evaluationInputRefs` | `Cset(selectedRefs ∪ {XI})`; no output domains | derive: one `execution-inputs` member; Plan imports present as suffixes |
| `executionInputsDigest` | raw SHA-256 of `C(ExecutionInputsV1)` named by `XI` | equals `XI.digest` on derive |
| Atomic `predicateProofs[].inputRefs` | `EI`, not atom consumed subset | production adapter and derive emit `EI`; isolated empty-refs scanner does not (`compose` helper boundary) |
| Boolean `inputRefs` | `Cset` union of immediate children | equals `EI` when children emit `EI` |
| Witness has no `inputRefs` | schema `additionalProperties: false` | held |
| Consulted Coverage/scope | may be narrower than `EI` | derive witnesses were a strict subset of EI coverage (`ei_coverage_n=2`) |
| Boolean matches empty | §9.3 | held |
| `childPredicateIds` | `Cset` of grammar addresses | 11-child `or`: stored `p.0,p.1,p.10,p.2,…` not grammar index order |
| Predicate array order | UTF-8 `(ruleId, subjectId, predicateId)` | held |
| Atom cause mapping | subject/predicate of that node; `atomEI` except Coverage-entry overwrite | adapter Coverage item `inputRefs=[{domain:coverage,digest:suffix}]` while atomic `inputRefs` stay `EI` |
| Boolean does not invent causes | union children | held |
| Required-import | enabled only; `inputRefs=[]`; `evidenceKind` = declared kind | held |
| Disabled | no predicate proofs; empty rule deficiencies; required execution retained | held |
| Budget | `predicateProofs=[]`, `findingIds=[]`, `evaluationState=budget-exhausted`; proof item `inputRefs=EI`; ruleResult copy `[]` | held |
| Correspondence | unmatched + `projection-unavailable` for empty symbol tokens; `anonymous-subject` not emitted; deficiency on ruleResult with enumeration inventory refs, not on witness | held |
| File/package discriminator | `SHA-256(C([]))`; no correspondence deficiency | held |
| Finding `evidenceRefs` | root witness + descendant facts/Coverage + observation importIds + every EI `domain=import`; no inventory | held on compose with EI scanner |
| Identical projected execution records | internal uniqueness includes cell/relation coordinates; proof uniqueness is bridged evaluation-deficiency `C` | two unsupported-typed internal rows with empty refs → one proof item |
| Nullable universe/carriers | binding `universe=null` → proof `universe=null`; `nativeCause` travels with its row | held on actual admit+bridge |
| `source=execution` is assessment layer | not a claim the provider is “execution” | bridge always sets `source=execution`; `subjectId`/`predicateId`/`evidenceKind` null |
| Evidence3 `viewIds`/`coverageIds`/`importIds` | EI views; views’ coverage ∪ EI coverage; Plan import set (schema canonical-set) | derive mint matched fixture views/coverage; Plan `importIds` already canonical-set |
| Policy-derivation3 | copies `planId`, `proofBundleId`, `policyDigest`, `waiverDigest`, `verdict` from replayed Run | held on synthetic `derive_policy_result` |
| Verdict | nonempty `executionDeficiencies` ⇒ at least indeterminate; fail dominates | disabled+execution and budget cases |

Synthetic `close_run` after `derive` + minted evidence/seal/run: replay ADMIT; `close_run` runId equals replay; same-count finding severity mutation reminted through proof/evidence/seal refuses `EVALUATOR_COMPLETE_PROOF_REPLAY`. That is a synthetic fixture Run, not product extraction qualification. Isolated `compose` of the same graphs never minted seal/run.

## Wording (not MUST)

§9.7 `importIds`: “Plan array order then … schema canonical-set”. Admitted `plan.importIds` is already `x-opensip-order: canonical-set`, so both readings agree. Prefer one sentence: stored array is `Cset(plan.importIds)`.

§9 notation cites `canonical.py`. The algorithm (sorted keys, compact separators, exact typed JSON) is already identity-and-evidence §3.

## Probes

Source: `probes/independent-proof-fields.v1.py`  
Results: `probes/independent-proof-fields.v1.json`  
Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`  
96/96 cases recorded. Passing probes do not clear MUST-1–MUST-3.

## Inputs

| Path | SHA-256 |
|---|---|
| `evaluator-composition-contract.v3.md` | `a762dd610870e27d8f64c84e098593c84d9c6a258a9f827f81e9a6b54a3ee026` |
| `execution-inputs-contract.v1.md` | `4a155e1565fe31c62917b2a4e7b6943a44a82fa550dc165050a6852cb22c46b6` |
| `identity-schemas.v3.json` | `cc60e9a51b3c71a300b9d28195bc1bc3716bda529b50059b2203645e8bd3b4da` |
| `identity-and-evidence.md` | `f9340e14b6b21218fc89c441a7cd7ce505373d9425fd9e9b0062a2282da4812b` |
