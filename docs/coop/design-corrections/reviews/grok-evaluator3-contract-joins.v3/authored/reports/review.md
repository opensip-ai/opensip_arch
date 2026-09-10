# Evaluator3 native/security joins v2 — bounded coauthor handoff

**Standing.** Actual Grok read-only handoff after the v2 authoring turn. Isolated source `/tmp/opensip-design-corrections/evaluator-successor.v1`. Not independent or blind acceptance. Not a Run. Not producer, platform, or pin qualification. v1 report and v2 process/public cancel standing are retained unmodified. This packet writes only these two files.

**Verdict.** `OWNED_SOURCE_AUTHORED_OFFICIAL_CHECKS_UNPERFORMED`. R2/R3/R4 source and the three normative chapters are present on disk with the semantics below. Official checkers have not validated those bytes. Do not treat this as a closed integration.

## Checks performed and unperformed

**Performed (v2 turn, retained).** Official security checker:

```
/tmp/opensip-architecture-review-env/bin/python -I -B check-security-lifecycle.v1.py --report .../grok-evaluator3-contract-joins.v2/security-official-pin-gate.json
```

Exit 1. `sourcePinsValid: false`. `cases: []`, `sweeps: []`, `passed: false`, `productQualification: false`. The checker refused to run cases because historical pins differ. It did **not** exercise journal dispatch, linearize, or native helpers.

Pin mismatches named by that official run (12 paths):

| path | this Grok v2 authorship | other |
|---|---|---|
| `native/native-capability-matrix.v2.json` | yes | |
| `native/native-cases.v2.json` | yes | |
| `native/native-evidence.schemas.v2.json` | yes | |
| `native/native_evidence_model.v2.py` | yes | |
| `security/check-security-lifecycle.v1.py` | yes | |
| `security/security-lifecycle.schemas.v1.json` | yes | |
| `security/security_lifecycle_model_v1.py` | yes | |
| `docs/v2/contracts/product-v1/native-evidence.md` | yes | |
| `public-detail-registry.v1.json` | no | root (already stale vs frozen pins) |
| `workflows/schemas/common.schema.json` | no | root |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | no | root |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | no | root |

`revocation-live-cases.v1.json` is not in `security/source-pins.v1.json`. Historical pin files were not edited.

**Cancelled, not rerun.** A follow-on manual pin-bypass that would have run cases/sweeps anyway was cancelled. No case or sweep output exists from it. **No semantic PASS is claimed.**

**Unperformed.** Native `check_native_evidence.v2.py` was not invoked this v2/v3 turn. Security cases and sweeps after the pin gate were not invoked. Root will seal new pins and run official checks.

This v3 turn hashes files and inspects source only.

## Required semantics now on disk

### 1. Native helper is complete capability REQUEST, not a complete evaluator3 spec

`default_capability_selection` still emits

```
{"schemaVersion": 2, "requestedCapabilities": requested, "policyPackIds": [], "parameters": []}
```

The return flag is `defaultIsCompleteCapabilitySelection: True`. Docstring states the empty parameter list is **intentional** pre-Plan capability request. EnumerationPlanV1 / EvaluatorEmissionPlanV1 stay a later host Plan-construction stage. This helper does not mint them.

Native-cases expectations (exactly two):

- `units-default-capabilities-full-tsjs-rust-registry-no-preview`
- `units-default-capabilities-staged-release-subset-discloses-absence`

both expect `$c.defaultIsCompleteCapabilitySelection: true` and `$c.analysisSpec.parameters: []`.

Chapters `native-evidence.md` and `admission-and-qualification.md` use the same name and the same pre-Plan / later-Plan split.

### 2. Journal record dispatch is recordSchema 3 / run3, not a mixed prefix

Current selected `$defs/JournalRecord`: `recordSchema` **const 3**, `runId` `^run3:[0-9a-f]{64}(?![\s\S])`. No `run[23]` alternation.

Frozen `$defs/JournalRecordV2`: `recordSchema` const 2, `runId` `^run2:…`. Not the LinearizationV1 item schema. Historical schema-2 journals are not read as 3.

`linearize` appends `recordSchema = CURRENT_JOURNAL_RECORD_SCHEMA` (3). SEAL writes `FIXTURE_SEAL_RUN_ID = 'run3:' + '0'*64`, labeled fixture, not close_run identity.

`admit_journal_record`: schema 3 + run3 → `CURRENT`; schema 2 + run2 → `JOURNAL_RECORD_SCHEMA_HISTORICAL`; schema 3 + run2 or schema 2 + run3 → `JOURNAL_RECORD_MIXED_PREFIX`.

`admit_host_seal_run_id`: run3 pattern, refuse run2, refuse the all-zero fixture as `SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY`, otherwise declare `authority: identity-model.v3.close_run`. It does **not** call `close_run`. Discriminating cases exist in `revocation-live-cases.v1.json` (`journalRecordCases`, `hostSealRunCases`) plus `seal-before-revocation-stands` expects recordSchema 3 and the fixture runId, and `seal-after-revocation-refused` remains. Grant/root schema-2 documents are a different axis.

### 3. Current native identity-chain annotations are evidence3/seal3/run3

Schema `movesIdentity` and `identityConsequence`, model `source_variant_capability_support` docstring, matrix `enforcedAt`, and the config-node-kind case note now name `fact2 / scope2 / coverage2 / view2 / evidence3 / seal3 / run3`. Native owner admission is `identity-model.v3.open_run_closure`; complete replay is `identity-model.v3.close_run`. Historical evaluator2 `evidence2/seal2/run2` is retained as the historical counterexample, not a current qualified claim.

## Stale R6 (v1 report)

v1 R6 said `identity-schemas.v3.json` `#/$defs/Domain` lacked `candidate-producer-result`. That observation was already stale against the **same bytes the v1 report hashed**: `4ed626ec932ffd480585e67c0044091b3ebda53f18447a8746a5ae377fa341de` (183663). Those bytes contain `candidate-producer-result` in Domain, Ref.domain, and `x-opensip-digest-domains.byDomain` → `execution-inputs.schema.v1.json#/$defs/CandidateProducerResultV1`. v1 R6 is not restated as live. Root: reconstruction function added, not yet called while execution v5 builds the fixture helper; no acceptance.

## Remaining design gaps (exact)

1. **Official native and security suites unrun** on these authored bytes. Pin files still name pre-v2 hashes. Root seals pins, then runs official checkers. This handoff cannot substitute.

2. **`foundation/check-identity.py:4425`** still asserts `_DEFAULT_FULL['defaultIsCompleteSelectedProduct'] is True`. Native helper no longer emits that key. This file was out of v2 ownership. After pin seal, that check will KeyError unless root updates it to `defaultIsCompleteCapabilitySelection`.

3. **`admit_host_seal_run_id` does not invoke `identity-model.v3.close_run`.** It admits any well-formed non-zero `run3:` string and *names* close_run as authority. A current host SEAL still needs the caller to pass an actually replayed RunId. Pattern dispatch is not replay.

4. **`admit_journal_record` is prefix/schema-number dispatch, not full JournalRecord schema admission.** A schema-3 object missing `recordType`/`seq` still returns `CURRENT` if `runId` is absent or run3. LinearizationV1 → JournalRecord full validation is the official checker’s job and was not executed.

5. **R1** (requiredForEvaluatorMajors at Plan/spec admission) and **R5** (workflows `policy-derivation2` leftover) remain root, as assigned. Not re-opened here.

6. **`identity-model.v3.py` moved under root** since v1 (`e4b8b2c0…` / 137395 → `e3fe8e5a…` / 137882). Not edited in the v2 Grok ownership set.

## Owned source hashes (sha256)

| file | bytes | sha256 |
|---|---|---|
| `native/native_evidence_model.v2.py` | 286278 | `ae1112db3f9951dcfb59635b6ed896e21dd9ee323422011d96a698deecce0d37` |
| `native/native-evidence.schemas.v2.json` | 230178 | `a87331bca7545468a266d74776d785a9903f93563220ac7f6267b6d749b82257` |
| `native/native-capability-matrix.v2.json` | 36595 | `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14` |
| `native/native-cases.v2.json` | 623693 | `a160be1718fc133151e9e4007743fb5243db5f8359f7a884afd4bc59153d6f71` |
| `security/security-lifecycle.schemas.v1.json` | 120764 | `b876e58df66d38af0d178c85559d726a1b95b6fcdc08591923db58a05b3fd32d` |
| `security/security_lifecycle_model_v1.py` | 200551 | `bb9b64c3ea612bbceeb94e4a82380748a743dc26ba08d383924137802ad33344` |
| `security/revocation-live-cases.v1.json` | 22608 | `15bc3740fa6476123eb5cfaa8fbf62eb3b2f0b16d6e5cd919629731b8b2f2160` |
| `security/check-security-lifecycle.v1.py` | 44024 | `4701d3b9d38703ffcc776e57fbe27b15710a3caccf3b469bdc5f184c9e24d8fc` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 262614 | `62202cd4ecd397e21219b4ed06cdb72ac7a4dd8ff000591f8f7d98e3ac347d4d` |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | 90072 | `0ec670021068ab25f072208f1777fc6c4077bce71b16b49ad66ef170688ebddd` |
| `docs/v2/contracts/product-v1/admission-and-qualification.md` | 26595 | `884d218040697bc5314f40b2646c7828fb415d90c5c71756e45f49d241c0d5cf` |

Counterpart (not owned this v2 turn): `identity-schemas.v3.json` still `4ed626ec932ffd480585e67c0044091b3ebda53f18447a8746a5ae377fa341de` (183663); `check-identity.py` still `fd7a9b945e745160fb6f764061ec1d937a796046e814c7c3b3d546396aec0e63` (578303); `identity-model.v3.py` now `e3fe8e5a103d68c90c21904a0a4ed1d557c02d10fb066c82854cd092896076fd` (137882).

v1 reports remain at `grok-evaluator3-contract-joins.v1/`. v2 retains `security-official-pin-gate.json` and cancelled-turn public files. Historical source-pins were not regenerated.
