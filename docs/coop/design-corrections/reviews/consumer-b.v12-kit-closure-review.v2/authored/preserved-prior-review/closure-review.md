# Structural closure review — corrected syntax-code Run

**Verdict: `SCOPED_CLOSURE_REFUSED`**

This is a bounded independent structural admission of the corrected syntax-code Run. It is **not** whole-consumer acceptance, product/host implementation, semantic-proof evaluation, or root admission. A selection of successful checks is not full admission.

The graph was not repaired or reminted. Consumer closure helpers were not used as an expected-value oracle. Laws were walked from the published kit registries.

## Input hashes

| Item | Value |
|---|---|
| Kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` (match) |
| Parent subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| Snapshot manifest | `f0339fa8345a5c7ce929a6a7ccd54239469d9862ce7d7e76700ded7a4ba65511` (match) |
| Snapshot files | **147/147** path/sha256/bytes PASS |
| Syntax-code store | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` (867956 bytes) |
| Independently reminted run | `run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918` (equals meta.runId) |

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v1/output/probes/structural_admit.py
```

Results: `probes/structural_admit.results.json`. Checker source is retained next to it.

## Applicability inventory (from published schemas, not consumer join names)

Keyword counts walked on identity v3, relation-payload v2, native-evidence v2, execution-inputs, enumeration-plan, emission-plan, subject-inventory, policy-document v1/v2:

`x-opensip-digest`, `x-opensip-order`, `x-opensip-digest-domains`, `x-opensip-relation-registry`, `x-opensip-payload-registry`, `x-opensip-deficiency-cause-registry`, plus uniqueness/parameter-registry/kind-derivation/file-membership/new-internal-faults on enumeration/execution owners.

**Digest domains** (identity-schemas.v3 `byDomain`): analysis-spec, blob, cache-key, capability-manifest, closure, configuration, coverage, coverage-payload, evaluation-seal, execution-plan, fact, fact-payload, finding, finding-fingerprint, finding-parameters, import, import-payload, native-context, plan, policy, policy-derivation, predicate-witness, proof-bundle, regeneration-key, rule-program, run, schema, semantic-evidence, snapshot, subject-scope, view, waiver, enumeration-plan, subject-inventory, evaluation-subject, evaluator-emission-plan, target-attribution, incoming-search, execution-inputs, candidate-producer-result.

**Relation registry** (13): calls, clones, control-flow, declares, file, imports, literal, package, reachability, references, types, unresolved-edge, vcs-change.

**This graph’s relations:** `clones`, `declares`, `file` only.

**Not applicable here (evaluated as N/A, not skipped silently):** TypeScript/Rust native-context snapshotJoins and nested identities; import payload registry; finding-fingerprint order; TS config-graph nested record; Rust ownership/edition dialect.

## Measured refusal (existing law, not a new design gap)

**`CLOSURE-MEMBERSHIP-SEAL-EVALUATOR-IN-PLAN` REFUSED**

Selector: `identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership`

- Direct member: `evaluation-seal.evaluatorClosure` — “Selected for the evaluation seal.”
- Selection law: “Direct members must be in `plan.semanticClosures`.” Extra closures may be selected; omitting a **direct** member is not permitted.

Measured:

| Field | Value |
|---|---|
| `plan.semanticClosures` | provider `closure2:00ec14d1…da01`, grammar `closure2:2951220e…cdc0` |
| `view.producerClosure` | `closure2:00ec14d1…da01` (in the set) **PASS** |
| `fact.producerClosure` = view producer | **PASS** |
| `proof.evaluatorClosure` = `seal.evaluatorClosure` | `closure2:2a9cfd92…ccec` **PASS** |
| evaluator closure retained (`kind=evaluator`) | yes |
| evaluator in `plan.semanticClosures` | **no** |

The evaluator frame is in the CAS. It is not a Plan-selected semantic closure. That is a reconstruction miss of an existing membership law, not a missing recipe.

Exact boundary: `UNSELECTED_EVALUATOR_CLOSURE` — `evaluation-seal.evaluatorClosure` / `proof-bundle.evaluatorClosure` `closure2:2a9cfd9286fa5f4fb752a8f8d8e42792fe471d9c71e0abcd69ce27e59129ccec` ∉ `plan.semanticClosures`.

## What did pass (not admission)

63 PASS rows including, independently reminted from kit C/H:

- Store blob keys = SHA-256 of exact bytes; H frames remint (prefix, domain, length, C equality, SHA-256(frame)=digest); typed prefixes.
- Acyclic graph: proof has no evidenceId/runId; seal includes evidence and proof; run includes seal.
- Run/plan/snapshot/proof/evidence/seal identity equality joins; projectId; capabilityManifestId derived `SHA256(UTF8("opensip.capability-manifest.v1")\|\|00\|\|committedBytes)` = `8bc78baa…e234`.
- Relation ladder membership; inventory/body-identity/source-text anchor cardinalities; same-only universes; payload `SHA256(C)` and `payloadSchemaDigest` = SHA-256 of exact `relation-payload-schemas.v2.json` bytes.
- File inventoried-file join (path, digest, length, retained blob); file@enumerated coverage totality; coverage partition disjointness; RC-6 complete ⇒ `examinedExhaustive`; deficiency-cause registry join.
- Clones L0 recomputed from syntax-universe languageVersionBinding (parserName/parserVersion/bundleDigest, `grammarVariant` from longest suffix, body language rust for `.rs`); L1 level-spec preimage retained.
- Syntax context: grammar-only (no toolchain); grammar closure join; bundle/normalizer/grammar-definition preimages; selectedGrammarIds subset; `resolutionAttempted=false`; universe `nativeContextId` binds context; plan native-context set contains the syntax context.
- `x-opensip-order` canonical-set on plan closures/contexts, view facts/scopes/coverage, scope subjects.
- Digest-field preimage retention for `*Digest`/`*Sha256` 64-hex fields (derived capabilityManifestId excluded).

## NOT_REACHED (remain open)

| Law | Why |
|---|---|
| `SEMANTIC-PROOF-EVALUATION` | Another review. Predicate witnesses, atom values, verdict derivation not evaluated. |
| `ROOT-ADMISSION` | No root result assumed or performed. |
| `EXECUTION-INPUTS-OUTCOME-DERIVE` | execution-inputs preimage and planId join **were** checked; full `derive_outcome` aggregate was not. |
| L1 token-stream framing parse | Level-spec bytes retained; tokenisation judgment not executed (level-specification freedom). |

Stock Draft 2020-12 `$defs` inhabitance of every record is not claimed here. This walk is the cross-record / custom-annotation set stock JSON Schema does not execute.

## Status counts

PASS 63 · REFUSED 1 · NOT_APPLICABLE 6 · NOT_REACHED 3 · **73 laws**.

Because an applicable structural law refused, the scoped verdict is **`SCOPED_CLOSURE_REFUSED`**. PASS rows do not override that. NOT_REACHED boundaries remain listed and are not treated as passes.

Machine-readable companion: `closure-review.json`.
