# Pilot admission review — completed syntax-code Run

**Verdict: `PILOT_REFUSED`**

This is a bounded independent admission of the **new** completed syntax-code pilot. It is **not** a new origin, **not** whole-consumer `ACCEPT`, **not** `ACCEPT-RECONSTRUCTABLE`, and **not** product qualification. Consumer `PILOT_READY_FOR_VALIDATOR_RECHECK` is a claim, not admission.

Structural admission and semantic replay are reported separately. The graph was not reminted or repaired. Replacement inputs are not labeled as the consumer’s accepted case. Consumer evaluator/replay scripts and saved truth flags were not used as an expected-output oracle.

## Separate outcomes

| Axis | Outcome | First actual refusal / boundary |
|---|---|---|
| Structural admission | **`STRUCTURAL_REFUSED`** | `EVALUATION-INPUT-REFS-EQUALS-SELECTED-PLUS-MANIFEST` |
| Semantic replay | **`SEMANTIC_REFUSED`** | complete expected proof C and H identity ≠ claimed (sole differing field: `evaluationInputRefs`) |
| Prior structural finding on **this** graph | **PASS** | predecessor `UNSELECTED_EVALUATOR_CLOSURE` is not present on the new Plan |
| This pass | **`PILOT_REFUSED`** | existing incorporated law, consumer correction |

`NOT_REACHED` that remain listed and are **not** treated as passes: `ROOT-ADMISSION`, `CLONES-L1-TOKEN-STREAM-FRAMING-JUDGMENT`.

## Input hashes

| Item | Value |
|---|---|
| Kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` **MATCH** |
| Kit files | **PASS 80/80** |
| Parent subject (declared on kit manifest) | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| Snapshot manifest | `0a953ef9d710bf6457aab58eaed4fb8f41c9daade252738f5d37704476c11ed0` **MATCH** |
| Snapshot files | **PASS 245/245**, 0 undeclared |
| Syntax-code store | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` (889618 bytes, 90 blobs, 32 H frames) |
| Independently reminted run | `run3:1ee613d2fd191b215e2f7ab56662ab70616ce303a55bd29f596299f481690081` |
| Independently reminted plan | `plan2:61407daf2c6f656c5258e1616907ae949fed63a1f4f6511572c395cfc6326471` |
| Independently reminted claimed proof identity | `proof3:e88715da47e0c07c715c580a8061c3c7df888ed82d1e08d17b3bc8582577e86b` |
| Snapshot | `snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd` |
| Checker | `probes/pilot_admit.py` SHA-256 `a564d60bac1eb1aa8465dcb48d082ba9bf2192820e3688e5865351c843ce33b1` |
| Results | `probes/pilot_admit.results.json` SHA-256 `afd1fce570602fa11c526bddbb28282dc975e53219b70d3aaf8b624c25a6ca3b` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v2/output/probes/pilot_admit.py
```

Consumer scripts under the snapshot `source` metadata path were **not** executed. Original failure stores were **not** rewritten.

## Prior first actual refusal — rechecked on the new graph

Selector: `identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership`  
Selection law: “Direct members must be in `plan.semanticClosures`.” Extra closures may be selected; omitting a **direct** member is not permitted.

| Graph | Evaluator | In `plan.semanticClosures` |
|---|---|---|
| Predecessor (preserved) `run3:f2542b3a…` store `2e74a6b2…` | `closure2:2a9cfd92…ccec` | **no** — `UNSELECTED_EVALUATOR_CLOSURE` |
| **This** graph `run3:1ee613d2…` | `closure2:a8a0903d…4b0a` kind=evaluator | **yes** — **PASS** |

Equal-to-direct `proof.evaluatorClosure = seal.evaluatorClosure` **PASS**. View/stage/scope producer/enumerator `closure2:62ad924a…e783` kind=provider is selected **PASS**. Extra detector `closure2:fba23342…32c9` (emission-plan binding) and extra grammar `closure2:841800c0…df99` are selected; grammar is also `selectedThroughOtherInput` via `plan.nativeContextDigests`. The predecessor first-refusal code is **not** the first refusal of this graph.

Preserved evidence (unchanged, not relabeled accepted):

- original store `preserved-failures/syntax-code-original/runs/syntax-code.store.json` `8b0f6d82…` (862544 bytes)
- structurally refused store `preserved-failures/syntax-code-structural-refused/runs/syntax-code.store.json` `2e74a6b2…` (867956 bytes)

Prior reviewer outputs are copied at `preserved-prior-review/`.

## First actual refusal on this graph (existing law)

**`EVALUATION-INPUT-REFS-EQUALS-SELECTED-PLUS-MANIFEST` REFUSED** — consumer correction, not a missing recipe.

Owning selectors:

- `evaluator-composition-contract.v3.md` §1: “`evaluationInputRefs` equals its selected references plus that one manifest reference.”
- `execution-inputs-contract.v1.md` §7: `evaluationInputRefs = selectedRefs + {domain:execution-inputs, digest}`.

Measured:

| Set | N | Content |
|---|---:|---|
| Independently recomputed `selectedRefs` | 11 | 1 complete-receipt view ∪ 6 view `coverageIds` ∪ 4 cell-outcome inventory digests |
| Kit-expected `evaluationInputRefs` | 12 | those 11 plus execution-inputs `d72fb03c…` |
| Claimed `proof.evaluationInputRefs` | 14 | expected 12 **plus** `rule-program` `77b07390…` **plus** `policy` `f7532ddc…` |

No expected member is missing. The two extras are **not** `selectedRefs`. `ruleProgramDigest` and `plan.policyDigest` already exist as their own proof/Plan fields. Extra members change C and therefore proof identity.

This is not absent or contradictory law. Current incorporated law states equality.

## Semantic replay (independent fresh process)

Admitted selected inputs were used to reconstruct: file subjects from complete file inventories; RuleProgramV2 as the published projection of Plan policy; postorder atom evaluation (strong Kleene); predicate-witness; ruleResults; sealed verdict; full proof-bundle record; then C bytes and H identity.

| Field | Independent expected | Claimed |
|---|---|---|
| Verdict | `pass` | `pass` |
| Atom `none` of `file@enumerated` filter `subject=hello.rs` | `false` (known file fact) | `false` |
| Findings | 0 | 0 |
| Predicate proofs | 1, witness digest equal | 1 |
| Subject | `subject3:8bf8bec7…a3ab` | same |
| Proof C SHA-256 | `8764a0ac48eb8b3bb26a423606f271c8f6e7ac906b37223d44825558d1bcb85a` | `2c735b764b6728a7d832841071324c4c8fadf658eb999fe4db5afeb47f876357` |
| Proof identity | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` | `proof3:e88715da47e0c07c715c580a8061c3c7df888ed82d1e08d17b3bc8582577e86b` |

**C equality: false. Identity equality: false.** The only field that differs is `evaluationInputRefs`.

Diagnostic (not an accepted expected-output): adding the two extra refs to the independently reconstructed proof yields **byte-identical** C and the claimed identity `proof3:e88715da…`. That shows every other complete proof field remints; it does **not** waive the equality law. The kit-law expected identity `proof3:0388fb97…` is **not** written into the consumer store and is **not** called the consumer’s accepted case.

Consumer `freshProcessReplay.proofCompareEqual=true` used the consumer composer (which injects policy and rule-program). That composer was not the oracle.

## Logical-result tamper vs stale-hash vs replacement graph

Same selected inputs, same Plan, same `executionInputsDigest`. Not a reconstructed replacement graph.

| Mutation | Independently reminted identity | vs claimed | vs kit-expected |
|---|---|---|---|
| Stale-hash control (flip `executionInputsDigest` only; citations preserved) | `proof3:5b95c8aa…` | C ≠ | C ≠ |
| Verdict-only (`verdict=fail`, atom/ruleResults unchanged) | `proof3:0d648fda…` | C ≠ | C ≠ |
| Logical result (`verdict=fail`, atom `true`, rule outcome `fail`) | `proof3:3a69570de5fd6a6d12827c31b7d100b28768c5f805791906ef8c103c536dd2ff` | C ≠ | C ≠ |

The full logical-result remint **equals** the consumer-claimed tamper identity `proof3:3a69570d…`. Independently reconstructed expected remains `verdict=pass` / atom=`false`. Semantic replay refuses the tampered claim. A stale-hash C inequality is recorded separately and is not that semantic refusal.

## Structural laws re-established on this graph (not inherited)

Prior 63 PASS rows were **not** carried forward by label. They were re-executed on the new graph together with the previously `NOT_REACHED` execution-input and proof-field laws this pass owns.

Measured PASS includes (non-exhaustive; full table in `probes/pilot_admit.results.json`):

- Store blob keys = SHA-256 of exact bytes; H-frame remint (prefix, domain, length, C remainder, SHA-256(frame)=digest); typed prefixes.
- Acyclic graph; run/plan/snapshot/proof/evidence/seal identity joins; capability-manifest-id derived `8bc78baa…e234`.
- Relation ladder, anchors, same-only universes, payload `SHA256(C)` and `payloadSchemaDigest` = SHA-256 of exact `relation-payload-schemas.v2.json`.
- File inventoried-file join; file@enumerated coverage totality; coverage partition disjointness; RC-6 complete ⇒ `examinedExhaustive`.
- Clones L0 recomputed from **published** `languageVersionBinding` (parserName/parserVersion/bundleDigest; dialect `grammarVariant` from the syntax-universe closed-suffix table, longest match; `bodyLanguageByVariant`). Not a local suffix heuristic used as law.
- Syntax context grammar-only; grammar closure join; selectedGrammarIds subset; `resolutionAttempted=false`.
- `x-opensip-order` canonical-set on plan closures/contexts, view facts/scopes/coverage, proof `evaluationInputRefs` **shape** (the extra members still form a canonical set; equality still refuses).
- Annotated `x-opensip-digest` owner walk on records this graph contains: **114 hits, 0 failures**. A `*Digest`/`*Sha256` suffix walk is retained only as an audit contrast and was **not** the law used.
- `selectedRefs` exact totality **11**; stage `outputDomains` `["view"]`; inventories are `hostDerivedRefs`; forbidden proof/finding/seal/run/evidence/execution-inputs domains absent from `selectedRefs`.
- `derive_outcome` join: clones-fact / inventory / syntax all `all-complete:complete`.
- Native coverage accounts cover every matrix pair of the **requested** cells (7 accounts), including VCS `kind=none` → `vcs-change` `inapplicable-vcs`.
- Component-manifest stored-bytes SHA-256 join as synthetic observation. `component-manifest-schemas.v11` stock inhabitance **not claimed** (`CANDIDATE-NOT-APPLIED`).

Status counts: **PASS 114 · REFUSED 2 · NOT_APPLICABLE 8 · NOT_REACHED 2 · 126 laws.**

## Applicability resolved from current kit (not consumer scope labels)

An unexecuted applicable law is not waived by a consumer scope label or by a historical candidate/application label.

| Law | Applicability | Result |
|---|---|---|
| Direct evaluator in `plan.semanticClosures` | applicable | PASS (this graph) |
| `evaluationInputRefs` = `selectedRefs` + execution-inputs | applicable | **REFUSED** |
| Complete expected proof C/H | applicable | **REFUSED** (follows the extra refs) |
| `selectedRefs` totality / `derive_outcome` | applicable | PASS |
| Requested-cell native account pairs | applicable (explicit selection) | PASS (7) |
| Default-profile remaining matrix cells | **not this Plan** (`explicitOverride`) | NOT_APPLICABLE |
| TypeScript/Rust native-context snapshotJoins | not on this graph | NOT_APPLICABLE |
| Import payloads / finding-fingerprint | no imports, no findings | NOT_APPLICABLE |
| `component-manifest-schemas.v11` stock inhabitance | CANDIDATE-NOT-APPLIED | NOT_APPLICABLE |
| L1 token-stream tokenisation judgment | level-spec freedom | NOT_REACHED |
| ROOT-ADMISSION | not demanded this pass | NOT_REACHED |
| Real host/OS/compiler/crypto implementation | future qualification | NOT_APPLICABLE |

`native-capability-matrix.v2.json` document `status` is `PROPOSED`. Execution-inputs contract §5 still joins requested cells to that matrix’s `capabilities[].relations`. That standing is recorded; it is **not** used to invent a default-profile obligation this explicit Plan does not carry, and it is **not** treated as absent law for the seven requested pairs.

`all-covered` → `sufficiency_v2` was **not** executed: the committed atom is `none`, not `all-covered`.

## Assumptions audited in the prior checker

1. **Suffix-name `*Digest` walk is not `x-opensip-digest` execution.** This pass walks published annotations on records the graph actually contains (114 owner hits). The suffix walk is audit-only.
2. **Keyword inventory is not annotation execution.** `x-opensip-*` counts are inventory only.
3. **`grammarVariant` is not a local heuristic used as law.** Variant/languageId come from `identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.syntax.v2/languageVersionBinding`.
4. Previously claimed successful checks were **re-run** on this new graph; they were not inherited.

## Limitations (not waivers)

1. Independent validator/root admission of exact exported frames was **not** performed (`ROOT-ADMISSION` NOT_REACHED).
2. L1 token-stream framing parse was not executed; level-specification bytes are retained.
3. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; signature envelopes are not verified (real crypto is not demanded).
4. Stock Draft 2020-12 inhabitance of every record is not claimed; this walk is the cross-record / custom-annotation / complete-proof set stock JSON Schema does not execute.
5. Other four Run stores, scope-v2 envelopes/vectors/query, and unexecuted original requirements outside this pilot remain visible and unverified by this pass.
6. Whole-consumer `ACCEPT` / `ACCEPT-RECONSTRUCTABLE` is **not** issued.

## Read coverage (normative + this consumer snapshot)

Normative: original 80-file kit under `/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject` and `requirements.json` beside it. Especially `identity-schemas.v3.json` (digest domains, closureMembership, proof-bundle, predicate-witness, languageVersionBinding), `relation-payload-schemas.v2.json`, `native-evidence.schemas.v2.json`, `native-capability-matrix.v2.json`, `execution-inputs.schema.v1.json` + contract v1, `evaluator-composition-contract.v3.md`, `atom-evaluation-contract.v1.md`, `enumeration-plan.schema.v1.json`, `evaluator-emission-plan.schema.v1.json`, `subject-inventory.schema.v1.json`, `identity-and-evidence.md`, policy-document v2.

Consumer (read-only snapshot): `snapshot-manifest.json`; `pilot-completion-review.md/json`; `runs/syntax-code.store.json` exact bytes; meta/closure/replay/tamper/reconstruction JSON; `helper/*.py` and `scripts/pilot_syntax_run.py` / `replay_from_export.py` as changed producer/admission/evaluator **code under review**, not oracles; preserved-failure stores hashed only. Source metadata names `/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output` — that original author directory was **not** read.

Own prior outputs: `consumer-b.v12-kit-closure-review.v1/output/closure-review.md/json` and `probes/structural_admit.py` (copied to `preserved-prior-review/`).

Measured commands: the independent checker above only.
