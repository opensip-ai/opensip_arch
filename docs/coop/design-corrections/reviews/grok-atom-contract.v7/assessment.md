I'll pick up the six owned files at the remaining v6 gaps: history ordinals, observation/payload joins, global admission keys, and typed NativeCause.I’ll apply the history-ordinal, observation-join, and closed-input-key fixes in the model first.v6 of the six owned atom files is finished. Bounded unit checks ran and passed; this is not Run acceptance.

`/tmp/opensip-architecture-review-env/bin/python -I -B …/check-atoms.v1.py` → **44/44 ok**. Draft 2020-12 metaschema-ok on the three JSON schemas. Registry `NativeCause` enum is an exact copy of `native-evidence.schemas.v2.json#/$defs/NativeCause` (14 owner strings). Helpers/report/hashes are under `/tmp/opensip-design-corrections/grok-atom-contract.v6/`. Frozen21, live, and root files were not edited.

### Additional concrete checks (this round)

- **History sequence.** `HistoryPayloadV1.subjects` is a sequence; duplicate paths are lawful. `_eval_imported` keeps **every** matching `history-subject` ordinal (not the last `hit`). Count uses the full address set.
- **Observation/payload join.** Non-null runtime `window`/`population`, test `selection`, and history `revisionRange` `{from,to}` must equal payload owner fields. Contrary adapters refuse `ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN`. Completeness reads payload fields; an observation-only window is not treated as owner-admitted. Missing payload window/population → `observation-window-insufficient`.
- **`admit_atom_inputs(inputs)`** is callable with **no atom**. It admits closed keys, all sidecars, all incoming searches, every `planSelectedImportIds` wrapper/scope/flag, and observation joins. Missing selected wrappers refuse even on an empty policy.
- **Closed input keys** (exact): `facts`, `scopes`, `coverages`, `enumerationPlan`, `inventories`, `targetAttributions`, `closures`, `universeDomains`, `imports`, `importPayloads`, `importObservations`, `importScopes`, `importScopeAdapter`, `planSelectedImportIds`, `evaluationInputRefs`, `incomingSearchAttestations`, `planId`, `blobs`, `coverageScopes`, `importFlagsAdapter`.
  - `coverageScopes`: `coverage2:<hex>` → `scope2:<hex>` (root derives from coverage envelope `scopeId`).
  - `importFlagsAdapter`: `import2:<hex>` → `{consumable, staleness}` only (root M3 owner maps). No default `true`/`current`. Extra inner keys refuse.

View/candidate execution totality remains the separate root input contract (main v12). Not this unit.

### Cause / API receipt

Every retained `AtomCauseV1` has typed `evidenceKind` and `nativeCause`. `nativeCause` is an owner NativeCause string or `null`; untyped strings refuse `ATOM_NATIVE_CAUSE_UNTYPED`. Native `sufficiency_v2` DeficiencyV2 values stay on `nativeDeficiencies`.

**NativeCause owner strings (14):**  
`body-language-owner-ambiguous`, `body-language-owner-unenumerated`, `body-language-ownership-missing`, `capability-missing`, `config-flag-stripped`, `generated-file-missing`, `generated-file-out-of-bounds`, `generated-output-unavailable`, `linker-unavailable`, `lockfile-missing`, `missing-dependency-source`, `no-program-unit`, `node-modules-outside-read-set`, `source-replacement-outside-snapshot`

**identity-schemas.v3 native deficiency codes** (`evidenceKind` null):  
`budget-exhausted`, `confidence-floor-unmet`, `coverage-unknown`, `derivation-policy-unmet`, `enumeration-unknown`, `external-consumers-unknown`, `input-closure-incomplete`, `language-tier-unsupported`, `missing-relation-coverage`, `provider-unavailable`, `required-relation-missing`, `resolution-incomplete`, `selector-unbound`, `source-target-search-unattested`, `target-kind-unknown`, `target-metadata-unknown`, `unavailable-program-binding`, `uncovered-expected-source-subject`

**identity-schemas.v3 import deficiency codes** (`evidenceKind` required):  
`evidence-kind-unavailable`, `incomplete-observation`, `unobservable-subject`, `unmapped-subject`, `no-consumable-row`, `import-unmapped-only`, `target-metadata-unknown`, `test-completeness-not-established`, `wrapper-partial`, `null-exit-status`, `history-outside-collection-scope`, `history-truncated`, `observation-window-insufficient`, `zero-owed-wrappers`

**Non-blocking disclosure:** `cross-family-edge-not-owed`  
**Structural, not semantic:** `omitted-selected-wrapper`, `missing-expected-inventory`

**New AtomCauseCodeV1 members not in that registry** (root owns schema3):  
native-side — `scope-without-coverage`, `population-unknown`, `target-export-unknown`, `unresolved-edge-target-unattributed`  
import-side — `overload-ambiguous`  
atom-local — `optional-absent`, `required-absent`

API: `evaluate_atom(atom, subject, inputs) -> AtomResult`; `admit_atom_inputs(inputs)` for global admission. Returns `value`, fact/observation arrays, `coverageIds`, `scopeIds`, `evaluationInputRefs`, `causes`, `nativeDeficiencies`, `disclosures`. No gating boolean.

### Owned-file SHA-256

| file | sha256 | bytes |
|---|---|---|
| `evaluator-projection-registry.v1.json` | `9c456f68c539c74b9d888ccdb0bfbfbef17db45da0c7e0adcdd533d552ffa502` | 58617 |
| `target-attribution.schema.v1.json` | `788bd9d000fb1da830ef368d14c119f441f7b60e8a56f8da3467ef0fbf0ed90e` | 13480 |
| `atom-evaluation-contract.v1.md` | `3564f5891c3c473e9565141b8f960f2764129ffe80474f157a50466660eab153` | 16257 |
| `atom_model.v1.py` | `52a057c74a11c89ceb0100423f5d2be2526a529b036b8a1dc1d2f400b9c478c0` | 77602 |
| `check-atoms.v1.py` | `d03c406325462d98936d2e10e85b2717c2f9e3eccd1fa2b7be2e6e1f3841d7c5` | 60950 |
| `incoming-search.schema.v1.json` | `8de1e688dacffa48a5a5dd4b0c72eb054901cb086bed97335c3c98dfa14e545f` | 11594 |

These 44 cases are discriminating unit scans of admitted maps. They are not a full independent Run, not compiler qualification, and not the root’s ~25 synthetic reference checks.
