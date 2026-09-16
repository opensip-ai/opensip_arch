# Closure-discipline self-audit (begun source39.v2, completed source39.v3)

What was asked: an independent self-audit of the existing reconstruction against the unchanged source39 kit. It covers:
- output construction separated from closure validation;
- a complete retained graph derived from owning schemas and registries, not from what the emitter retained;
- replay only after that closure admits;
- one independent negative per applicable retention/reference class, with exact first refusal and masking.

All numbers below are from source39.v3 executions (`logs/v3-closure.*`) unless marked v2.

## 1. Own prior bytes preserved and self-checked first (v2)

- The source39.v1 output tree was copied byte-exact (636 files) to `preserved/source39-v1/`, with its manifest. The original `consumer-b.v24` output is recorded as a hash manifest.
- `tools/selfcheck_prior.py` → `selfcheck/pre-summary.json`, covering 63 seeded stores:
  - custody equals the v1 manifest for all 63;
  - the unchanged ported code, in fresh processes, reproduced v1's recorded closure/replay result for all 62 stores that have a v1 record;
  - the one store without a record is `ts-pass.pre-builder-extension`.

## 2. Reference vocabulary from the kit (`tools/reference_census.py` → `vectors/reference-census.json`)

- **Typed-prefix identity positions.** 231, taken from schema patterns `^<prefix>:[0-9a-f]{64}`.
- **`x-opensip-digest` annotations.** 232, in 14 representation/retention pairs:

  | Representation | Retention | Count |
  |---|---|---|
  | by-domain | preimage | 7 |
  | canonical-record | preimage | 80 |
  | canonical-record | fragment | 2 |
  | canonical-record | owner-retained | 2 |
  | capability-manifest-id | derived | 4 |
  | framed-body-identity | provider-output-retained | 1 |
  | h-identity | preimage | 25 |
  | h-identity | preimage-frame | 31 |
  | h-identity | derived | 3 |
  | raw-artifact | preimage | 52 |
  | raw-artifact | closure-tree-member | 10 |
  | raw-artifact | owner-retained | 11 |
  | snapshot-path | snapshot-inventoried | 3 |
  | snapshot-path | not-joined | 1 |

- **Registry join forms** from `x-opensip-digest-domains.domainSets`: `closureJoins` (closure2-identity / closure2-suffix), `nestedIdentities`, `nestedRecords` (+ `blobJoins`), `blobJoins`, `snapshotJoins` (inventoried-paths / inventoried-path-and-digest), `contextAgreementFields`, and `languageVersionBinding` (derived).
- **Closure law.** `closureMembership` (direct / equalToDirect / selectedThroughOtherInput) and `closureKinds.byField`.

## 3. The independent retained-closure validator (`ref/retained_graph.py`)

- **Separate from the emitter.**
  - It reads only the exported content-addressed blobs (re-hashing every fetch) and the kit.
  - It imports no builder, evaluator, closure, digestlaw, native, import or membership module, and never reads the export `objectTable`.
  - `canonical.py` is used only for the section-3 C codec, and `schemas.py` only for kit-document Draft 2020-12 plus `x-opensip-order` admission.
- **Walk.**
  - It starts at `run3` and admits every resolved record under its owning selector.
  - Every typed-prefix field resolves a frame in the prefix-selected identity domain. The prefix table is from identity s3 and composition s9.7; a historical prefix refuses.
  - Every annotation is executed per its representation/retention, with the registry joins, closure membership/kinds and the Plan/snapshot joins of identity s3 lines 616-617.
  - Reachable descriptors, required preimages and unreachable retained frames are all reported.
- **Obligations are reported separately:** LEXICAL, SCHEMA, IDENTITY, RETENTION, JOIN.
- **Explicitly delegated to owner graph admission**, which runs as its own stage:
  - `languageVersionBinding` derivation;
  - clones body-identity parse joins;
  - native context/universe admission and binding;
  - enumeration and execution-input derivation.

  Workflow-owned Plan input documents' typed values are recorded as owner-scoped keys (HC-36; advisory A-v2-1).
- **`ref/closure.py close_run` stage order.**
  1. Owner graph admission.
  2. Retained closure. Stages 1 and 2 always both run.
  3. Semantic replay, only if 1 and 2 both admit.
  4. Reachable output-set equality (HC-34).

  First refusal, masked stages and stage-ordered faults are reported.

## 4. Helper defects found and corrected from the kit (`tools/hc_v2.py`)

| HC | Defect | Selector | Original failure retained |
|---|---|---|---|
| HC-33 | typed-prefix output references (proof findingIds, predicate subjectIds, enumerations, finding subject/fingerprint/ruleClosure, evidence arrays) were never resolved before replay; replay compared only the emitter's own object subset | composition s7 line 74; identity s3 lines 435-439, 616-617 | `selfcheck/pre-summary.json`: v1 code ADMITs all 27 positives, walker refuses all 63 stores |
| HC-34 | no exact reachable output-set equality | composition s7 lines 76, 328 | — |
| HC-35 | evaluator emitted subject3 descriptors only for subjects with findings | composition s7 line 72 | all v1 stores lack those frames |
| HC-36 | walker treated typed values in workflow-owned Plan inputs as retention references | composition s7 line 74, s5 line 54; identity s3 lines 597-600, 627-631 | `logs/v2-build.4.from_scratch.log` (cmp-empty, cmp-budget) |
| HC-37 | walker required plan selection only for typed-prefix import2 refs, not by-domain import refs | identity-schemas.v3 `closureMembership.selectedThroughOtherInput` | `preserved/v3-pre-hc37/vectors/retention-negatives.json` (walker admitted `ts-pass~hidden-import`) |
| HC-38 | walker delegated SourceUnitOwnershipV1 `unitId` derivation although the native law publishes it | native-evidence.schemas.v2 `x-opensip-digest-law.retention.derived`; `$defs/UnitIdentityV1` | same file (walker admitted `rust-mixed~unit-id-not-derived`) |

Tool-construction defects in my new test tools were fixed with their failed attempts kept; they are not helper corrections:
- `retention_negatives.py` first remint did not re-order generic canonical records (`logs/v2-negatives.0.retention_negatives.log`);
- `v3_preserve_and_rebind.py` rewrote its own constants (`notes/12-v3-completion.md`).

## 5. Pre/post correction matrix (`selfcheck/prepost-matrix.json`; every cell a fresh-process closure over exact bytes)

| Code \ bytes | v1 stores | v2/v3 stores |
|---|---|---|
| pre (source39.v1 helpers, `preserved/pre-hc33`) | 27/27 positives ADMIT | 27/27 ADMIT |
| post (HC-33..HC-38) | 26/27 REFUSE at retained-closure (`PREIMAGE_MISSING typed-prefix:evaluation-subject`); `cmp-empty` ADMITs because it references no subject and its bytes are unchanged | 27/27 ADMIT |

- Run, proof, evidence and seal identities are unchanged for all 27 positives.
- The only byte delta is added `evaluation-subject` frames; nothing was removed.

## 6. Claimed complete positives under the corrected closure (v3)

- **From-scratch** (`runs/from-scratch.summary.json`, `logs/v3-closure.1`): all 27 ADMIT through owner admission, retained closure, replay and reachable-set equality. The designed negative `syntax-mixed-falsecomplete` refuses at owner admission.
- **Per positive:**
  - required preimages: 109–210;
  - reachable semantic outputs: 4–28, equal to the recomputed set;
  - unreachable retained frames: `policy-derivation3` in every Run; unselected closures (syntax Runs); the import omitted by `cmp-gmissing`.
- **Replay export** (`logs/v3-closure.5`): 27/27 exported after a fresh `close_run` ADMIT. C(recomputed proof) is byte-equal, evidence/seal/Run identities are equal, and every witness is byte-equal (520 predicate proofs).
- **Admission log** (`logs/v3-closure.6`): 27 positives, 0 failures.

## 7. Replay-all and tamper (v3)

- **`runs/replay-all.summary.json`:** 62 stores; 29 ADMIT (27 positives + 2 lawful controls); 33 REFUSE, all first at owner graph admission.
  - The independent retained closure also refuses 10 of those 33.
  - The other 23 are owner-semantic laws the walker explicitly delegates. They are listed by name in `vectors/retention-negatives.json` / `runs/*.replay.json#/retainedClosure`:
    - native context admission (compiler/grammar version, stdlib inventory, config node kind, universe↔context allowJs / configProjectionSha256);
    - body-language ownership (ambiguous / unenumerated);
    - normalization specification;
    - enumeration (membership order, inventory file totality, partition overlap), selected cover;
    - import grant / staleness / window;
    - scope-document cardinality;
    - pruned-tree reads;
    - edition map;
    - scope capability.
- **Tamper** (`runs/{syntax-code,ts-pass,rust-mixed}.tamper-outputs.json`, `logs/v3-closure.2-4`):
  - Every constructed semantic control (9, 10, 9; imported-address exists only in ts-pass) is admitted by owner admission and by the retained closure, then refused by replay (`SEMANTIC_REPLAY_PROOF_MISMATCH`).
  - Every identity control refuses before replay.

## 8. Retention/reference-class negatives (`vectors/retention-negatives.json`, `logs/v3-closure.7`)

**Construction.**
- 32 negatives were constructed from corrected positives by an exact mutation plus an independent remint.
- The remint rewrites every enclosing record or frame, re-orders it under the registered selector its original bytes admitted under, and re-hashes to fixpoint, so no stale hash remains.
- Each is closed by post code (in-process) and by pre code (`preserved/pre-hc33`, fresh process).
- **All 32 pass** the structural criterion:
  - refusal negatives REFUSE, replay does not run, and the retained closure refuses;
  - the unreachable-output control ADMITs, with the extra frame listed unreachable;
  - the unrecomputed-output control REFUSEs in replay.
- No refusal code was asserted in advance; all are measured.

**Classes first refused by the independent retained closure, which owner admission does not see.** The last column is what the pre-correction helpers did.

| Negative | Retained-closure first refusal | Pre code |
|---|---|---|
| subject3 descriptor missing | RETENTION PREIMAGE_MISSING (`predicateProofs[1].subjectId`) | **ADMIT** |
| finding3 frame missing | RETENTION PREIMAGE_MISSING | replay OUTPUT_OBJECT_MISSING |
| finding-key2 descriptor missing | RETENTION PREIMAGE_MISSING | replay OUTPUT_OBJECT_MISSING |
| finding3 prefix carries a subject frame | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| finding3 frame outside `$defs/finding` | SCHEMA FRAME_RECORD_REFUSED | replay PROOF_MISMATCH |
| canonical record where an H frame is required | LEXICAL FRAME_PREFIX | replay PROOF_MISMATCH |
| subject universe names a native-context frame | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| finding-parameters preimage missing | RETENTION PREIMAGE_MISSING | replay OUTPUT_PREIMAGE_MISSING |
| FindingEvidenceRef by-domain fact names a coverage frame | IDENTITY FRAME_DOMAIN_NOT_ALLOWED | replay PROOF_MISMATCH |
| finding.ruleClosure not Plan-selected | JOIN CLOSURE_MEMBERSHIP_DIRECT | replay PROOF_MISMATCH |
| finding.ruleClosure names the evaluator closure | JOIN CLOSURE_KIND_MISMATCH | replay PROOF_MISMATCH |

**Classes first refused by owner graph admission.** Owner admission's named cause is first; the retained closure also refuses, and its refusal is masked. Retained-closure codes by negative:
- historical `finding2` prefix: SCHEMA FRAME_RECORD_REFUSED;
- scope2 input missing: RETENTION PREIMAGE_MISSING;
- native-nested preimage-frame missing: RETENTION;
- witness not canonical: LEXICAL RECORD_NOT_CANONICAL;
- witness selector refused: SCHEMA RECORD_REFUSED;
- payload-class schema digest: JOIN PAYLOAD_SCHEMA_DIGEST_JOIN;
- program-predicate fragment: JOIN FRAGMENT_MISMATCH;
- closure tree bytes missing: RETENTION;
- tree length: RETENTION ARTIFACT_LENGTH_MISMATCH;
- unregistered schema document: JOIN SCHEMA_DOCUMENT_UNREGISTERED;
- closure-tree-member: JOIN CLOSURE_TREE_MEMBER_ABSENT;
- capability-manifest-id: JOIN DERIVED_MISMATCH;
- snapshot-path: JOIN SNAPSHOT_PATH_NOT_INVENTORIED;
- clones body frame missing: RETENTION;
- nestedRecords blobJoins: every layout entry is also a snapshot row, so source retention is reached first (RETENTION);
- lockfile path-and-digest: the new digest has no bytes, so RETENTION first;
- closureJoins kind: JOIN CLOSURE_KIND_MISMATCH;
- contextAgreementFields: JOIN UNIVERSE_CONTEXT_AGREEMENT;
- equalToDirect: JOIN FACT_PRODUCER_VIEW_JOIN.

**Builder input mutations used where the class lives in native owner inputs:**
- `ts-pass~hidden-import`: the walker refuses JOIN UNSELECTED_EVALUATION_IMPORT (HC-37);
- `rust-mixed~unit-id-not-derived`: JOIN DERIVED_UNBOUND (HC-38);
- `ts-pass~config-graph-path-outside-snapshot`: RETENTION;
- `rust-mixed~config-projection-mismatch`: refused only by owner binding, because the universe `configProjectionSha256` ↔ context join is not a `domainSets` registry join.

**Not reached.** `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` occur in no constructed positive graph. They have no negative and are not claimed.

## 9. What this audit changes in the review

- **Helper defects corrected; no kit issue.** HC-33..HC-38 were real helper defects with precise kit answers.
- **Carried forward.** s39-M1 stays unresolved.
- **New advisories.** A-v2-1, A-v2-2 and A-v2-3 are wording and scoping items with deterministic readings (`notes/10-gaps.md`).
- **The exported positives now differ from v1's**: they retain the subject descriptors composition s7 requires. v1's bytes would be refused by a closure that enforces s7.
