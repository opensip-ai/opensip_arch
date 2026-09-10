# Other-runs independent kit-only review

**Verdict: `OTHER_RUNS_REFUSED`**

Independent kit-only validator of four reconstructed Runs. Not whole-consumer ACCEPT. Root admission not performed.

This is not whole-consumer ACCEPT, not product implementation, and not root admission.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80 |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | match |
| `snapshot-manifest.json` | `385cacdedbca83701acc14afbe9342dfe8d4c4867453888e391fc1f2c2e4be33` | PASS 275/275 |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`

Reproducible command:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/output/independent/review_four.py
```

Consumer helper PASS, saved evaluator output, and copied review files inside the snapshot were treated as claims under review, not oracles.

## First-refusal map (existing published law, not invented profile)

| Run | Raw | Schema | Structural first refusal | Fullsemantic first refusal |
|---|---|---|---|---|
| `ts` | PASS | PASS | `structural:import-payload` | `proof-C-compare` |
| `rust` | PASS | PASS | `structural:domainSet-joins` | `proof-C-compare` |
| `syntax-data` | PASS | PASS | `structural:execution-inputs-laws` | `proof-C-compare` |
| `rust-partial-clones` | PASS | PASS | `structural:domainSet-joins` | `proof-C-compare` |

Classification of refusals:

- **Existing law, missing consumer implementation:** TypeScript imported `runtime` payload does not inhabit `RuntimePayloadV1` (`format=json` / null `observationWindow`). Rust `crateRootPaths` `#/a` is not an inventoried snapshot path (native-evidence crateRootPaths join). Rust toolchain tree `bin/proc-macro-srv` declared 13 bytes, retained blob is 14 (`b'proc-macro-srv'`). Rust clones fact is minted under one universe whose `selectedUnitIds` own `#/a/src/lib.rs` at editions 2018 and 2021 (`BODY_LANGUAGE_OWNER_AMBIGUOUS`; lawful form is one selection at a time). syntax-data `clones-fact` account is `unsupported-typed` while matrix cell `clones-fact × syntax-only` is `SUPPORTED-DESIGN`; Coverage unknown + `language-tier-unsupported`/`capability-missing` is the scopeCapabilityLaw disclosure, which makes a supported-available account incomplete and the required cell **partial**, not complete. rust-partial required `clones-fact` cell is correctly host-`partial`, but claimed proof `executionDeficiencies=[]` and `verdict=pass` contrary to composition §5 (required execution deficiency ⇒ sealed indeterminate). `evaluationInputRefs` adds `policy` and `rule-program` beyond enumeration-contract §7 `selectedRefs + execution-inputs`.
- **Absent/contradictory published law:** none used as a waiver. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; stored-bytes tree join was still executed.
- **Not invented default-profile cells:** these Plans request explicit capability subsets; unselected `calls`/`types`/`references` were not demanded.

## Per-Run outcomes

### `ts`

- Store SHA-256 `af2238a65afb0b7d82c5dd5ab1278436d55c4bc3087631d407563346593eb4ca` (678780 bytes, 115 blobs)
- Run `run3:97651646098ed5ff74bbafa5546898d9a96e77fa352beb209c622bd321276adc`
- Plan `plan2:2d723a9a8f88e00bbd81af2ee4a262bcf24c73e9cca9514facf24060cd3514dc`
- Claimed proof `proof3:ab7796b647e93608b36dbae713977d088f41882682bff889dfaed39a6f86e0c7`
- Independently reconstructed proof `proof3:e0b5cbc14dd872beceef9ab7a3e13d10b61dc45515d26be4347c70f471372de6`
- Layers: raw `PASS` / schema `PASS` / structural `REFUSED` / fullsemantic `REFUSED`
- Overall: **REFUSED**
- First refusal: `structural:import-payload` — IMPORT_PAYLOAD_SCHEMA: IMPORT_PAYLOAD_SCHEMA: [{'path': ['format'], 'message': "'json' is not one of ['v8-json', 'istanbul-json', 'lcov', 'llvm-cov-json']", 'validator': 'enum'}, {'path': ['observationWindow'], 'message': "None is not of type 'object'", 'validator': 'type'}]
- Claimed verdict `pass`; independently derived verdict `pass`
- Proof C claimed `afc54dc5d0cd73208c9de95363cf2590c3c7b1c854d9dc73e103a6c092820f36`; expected `74bfbe399a9e98d2d9175c362ffb4c1945cdde247a91722d84f48e4aa6038fe0`
- Tamper: stale-hash control `True`; semantic refuse `True`; tampered `proof3:0925ffba1773128a227920a24b4bc514e2970b50467251477fdece4756a2a0e1`

Failed joins:

- `structural:import-payload` — IMPORT_PAYLOAD_SCHEMA: IMPORT_PAYLOAD_SCHEMA: [{'path': ['format'], 'message': "'json' is not one of ['v8-json', 'istanbul-json', 'lcov', 'llvm-cov-json']", 'validator': 'enum'}, {'path': ['observationWindow'], 'message': "None is not of type 'object'", 'validator': 'type'}]
- `fullsemantic:proof-C-compare-kit-evaluationInputRefs` — expected proof3:e0b5cbc14dd872beceef9ab7a3e13d10b61dc45515d26be4347c70f471372de6 claimed proof3:ab7796b647e93608b36dbae713977d088f41882682bff889dfaed39a6f86e0c7
- `fullsemantic:proof-C-compare` — expected proof3:e0b5cbc14dd872beceef9ab7a3e13d10b61dc45515d26be4347c70f471372de6 claimed proof3:ab7796b647e93608b36dbae713977d088f41882682bff889dfaed39a6f86e0c7
- `fullsemantic:proof-identity-compare` — proof3:e0b5cbc14dd872beceef9ab7a3e13d10b61dc45515d26be4347c70f471372de6
- `fullsemantic:proof-field-diffs` — evaluationInputRefs

Original required properties:

- `R-RUN-TS` FAIL — REFUSED
- `R-RUN-TS-NODE-MODULES` PASS — ['node_modules/left-pad/index.js', 'node_modules/left-pad/package.json']
- `R-RUN-TS-BARE-SPECIFIER` PASS — 
- `R-RUN-NONCEMPTY-CONTEXT` PASS — ['271a6043c1bf60bb25e814f08ff495bf7bd15b582d5b6cffc3f086ce9986f605']
- `R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC` PASS — {"exclude": ["node_modules/**"], "include": ["src/**/*.ts"], "schemaFamily": "opensip.product.scope", "schemaMajor": 1}
- `R-IMPORTED-PAYLOAD-IN-GRAPH` FAIL — ['import2:1bdd740b9ce2b4639c7c12b5abbce5d95937bebd6ba70981d58dc4eafcc70eaa']; payload does not inhabit payload-registry RuntimePayloadV1
- `R-RUN-FILE-FACT-INVENTORY` PASS — 
- `R-RUN-CLONES-L0` PASS — 
- `R-NATIVE-PREIMAGE-JOINS-TS` PASS — ['nestedRecord:nodeModulesLayout', 'nestedRecord:configGraph']
- `config-graph-and-node-modules` PASS — 

Requested capabilities / cell outcomes:

```json
{
  "requested": [
    {
      "capabilityId": "clones-fact",
      "languageMode": "ts-tsconfig",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "imports",
      "languageMode": "ts-tsconfig",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "inventory",
      "languageMode": "ts-tsconfig",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "syntax",
      "languageMode": "ts-tsconfig",
      "required": true,
      "workspaceRoot": "."
    }
  ],
  "cells": [
    {
      "ordinal": 0,
      "capabilityId": "clones-fact",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 1,
      "capabilityId": "imports",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 2,
      "capabilityId": "inventory",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 3,
      "capabilityId": "syntax",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    }
  ],
  "coverages": [
    {
      "relation": "clones",
      "resolution": "normalized-body-hash",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "declares",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "file",
      "resolution": "enumerated",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "literal",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "imports",
      "resolution": "resolved-target",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "control-flow",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "package",
      "resolution": "manifest-declared",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    }
  ]
}
```

### `rust`

- Store SHA-256 `e6457494c46b2c8cefc7f6c0779da08de820b26890bc250defe1361b6e29fd4a` (536279 bytes, 100 blobs)
- Run `run3:02f31e575e6841316fe34f4f9a95fcb572c528b66f9793aad948078ec59a7949`
- Plan `plan2:12445233b2b92fdd2df79c7189f5a7b4a13a1402331d6bb8e075c25620575380`
- Claimed proof `proof3:026843f105a1bdc931091b8224eec091fb5cd2aa0961efef1efa1dd2c5e4e86c`
- Independently reconstructed proof `proof3:cd4f5169252288709b6d7b7c58bb49cec123660ddf56dd0a788bb5688d559429`
- Layers: raw `PASS` / schema `PASS` / structural `REFUSED` / fullsemantic `REFUSED`
- Overall: **REFUSED**
- First refusal: `structural:domainSet-joins` — SNAPSHOT_JOIN_PATH: SNAPSHOT_JOIN_PATH: uni.crateRootPaths #/a
- Claimed verdict `pass`; independently derived verdict `pass`
- Proof C claimed `00d293ea4e699c61d66058598a58c8bd69cb6be96fe44122b385b6b6bd54b2ce`; expected `ae39db0ef28ec17f997c477d5d395cad258a1bc4f2d05e151544a3ddcc7712aa`
- Tamper: stale-hash control `True`; semantic refuse `True`; tampered `proof3:55a7ae5ffed5b37360d993a5e77d841dc98be053d5e9cd97c1e0e8420197668b`

Failed joins:

- `structural:domainSet-joins` — SNAPSHOT_JOIN_PATH: SNAPSHOT_JOIN_PATH: uni.crateRootPaths #/a
- `structural:component-manifest` — TREE_MEMBER_LENGTH: TREE_MEMBER_LENGTH: bin/proc-macro-srv
- `structural:clones-body-and-scope-capability` — BODY_LANGUAGE_OWNER_AMBIGUOUS: BODY_LANGUAGE_OWNER_AMBIGUOUS: {2018, 2021}
- `fullsemantic:proof-C-compare-kit-evaluationInputRefs` — expected proof3:cd4f5169252288709b6d7b7c58bb49cec123660ddf56dd0a788bb5688d559429 claimed proof3:026843f105a1bdc931091b8224eec091fb5cd2aa0961efef1efa1dd2c5e4e86c
- `fullsemantic:proof-C-compare` — expected proof3:cd4f5169252288709b6d7b7c58bb49cec123660ddf56dd0a788bb5688d559429 claimed proof3:026843f105a1bdc931091b8224eec091fb5cd2aa0961efef1efa1dd2c5e4e86c
- `fullsemantic:proof-identity-compare` — proof3:cd4f5169252288709b6d7b7c58bb49cec123660ddf56dd0a788bb5688d559429
- `fullsemantic:proof-field-diffs` — evaluationInputRefs

Original required properties:

- `R-RUN-RUST` FAIL — REFUSED
- `R-RUN-NONCEMPTY-CONTEXT` PASS — 
- `R-RUN-RUST-HASH-MARKER` PASS — ['#/Cargo.toml', '#/a/Cargo.toml', '#/a/src/lib.rs', 'Cargo.lock']
- `R-RUN-RUST-MIXED-EDITION` PASS — {"a": 2018, "crate00": 2015, "crate01": 2018, "crate02": 2021, "crate03": 2024, "crate04": 2015, "crate05": 2018, "crate06": 2021, "crate07": 2024, "crate08": 2015, "crate09": 2018, "crate10": 2021, "crate11": 2024, "crate12": 2015, "crate13": 2018, "crate14": 2021, "crate15": 2024}
- `R-RUN-RUST-LARGE-EDITION-MAP` PASS — 17
- `R-RUN-FILE-FACT-INVENTORY` PASS — 
- `R-RUN-CLONES-L0` PASS — 
- `R-NATIVE-PREIMAGE-JOINS-RUST` PASS — ['nestedIdentity:packages.[].fileManifestSha256:empty', 'nestedIdentity:dependencySourceSetId', 'nestedIdentity:unifiedFeaturesId', 'nestedIdentity:preparedOutputSetId:null', 'nestedIdentity:packages.[].fileManifestSha256:empty', 'nestedIdentity:dependencySourceSetId', 'nestedIdentity:unifiedFeaturesId', 'nestedIdentity:preparedOutputSetId:null', 'nestedIdentity:configProjectionSha256', 'nestedIdentity:sourceUnitOwnershipId']
- `ownership-units` PASS — [{"crateName": "a", "markerPath": "#/a/Cargo.toml", "targetEdition": 2021, "targetKind": "bin", "targetName": "tool", "unitId": "sha256:1e4e1cda7b538b89dc972eea01680dcea67d7ca8ca34e4cc2a22aa7ebc4342b3"}, {"crateName": "a", "markerPath": "#/a/Cargo.toml", "targetEdition": null, "targetKind": "lib", "targetName": "a", "unitId": "sha256:7291519e6b819789a4669bc7f69158790980b844ec917d4493b05ae4120e0b2b"}]
- `R-RUN-RUST-TARGET-EDITION` PASS — crate a default 2018 target sha256:1e4e1cda7b538b89dc972eea01680dcea67d7ca8ca34e4cc2a22aa7ebc4342b3=2021
- `R-RUN-RUST-SAME-FILE-TWO-EDITIONS` FAIL — #/a/src/lib.rs editions=[2018, 2021] both appear in one selectedUnitIds set; dialect law refuses BODY_LANGUAGE_OWNER_AMBIGUOUS. Lawful form is one selection/universe at a time.
- `R-RUN-RUST-BODY-DIALECT` FAIL — 
- `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` FAIL — consumer pair artifact is a claim, not a second retained graph; this validator did not independently mint a lib-only selection universe. Claimed L0 2018 vs 2021 distinct=True
- `R-RUN-RUST-VERSION-COMPONENT` FAIL — derived from rustc context + selected target edition

Requested capabilities / cell outcomes:

```json
{
  "requested": [
    {
      "capabilityId": "clones-fact",
      "languageMode": "rust-cargo",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "inventory",
      "languageMode": "rust-cargo",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "syntax",
      "languageMode": "rust-cargo",
      "required": true,
      "workspaceRoot": "."
    }
  ],
  "cells": [
    {
      "ordinal": 0,
      "capabilityId": "clones-fact",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 1,
      "capabilityId": "inventory",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 2,
      "capabilityId": "syntax",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    }
  ],
  "coverages": [
    {
      "relation": "package",
      "resolution": "manifest-declared",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "control-flow",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "declares",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "file",
      "resolution": "enumerated",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "clones",
      "resolution": "normalized-body-hash",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "literal",
      "resolution": "syntactic",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    }
  ]
}
```

### `syntax-data`

- Store SHA-256 `e050875685a7a4f706c98982baeafbce3b15f9c6c4c2ff97c2800a820645ec87` (490576 bytes, 65 blobs)
- Run `run3:a803341435a3a360d96c535261d3e45a32942a5db4c445764d102d1810ffccbc`
- Plan `plan2:09e25c1ec3e3267c252402623391071321a6dc0d2551200dd504c23aabb61cd9`
- Claimed proof `proof3:22e08d2fa0618444910aff48ea7bc8d862cde7c837cc6473024f095681ff6337`
- Independently reconstructed proof `proof3:d61754bcf6024256a1e5ced071f5a8062a5da1f5842aeb5ea15823f5d5faebbe`
- Layers: raw `PASS` / schema `PASS` / structural `REFUSED` / fullsemantic `REFUSED`
- Overall: **REFUSED**
- First refusal: `structural:execution-inputs-laws` — EXECUTION_INPUTS_APPLICABILITY: EXECUTION_INPUTS_APPLICABILITY: clones-fact/clones: host unsupported-typed != derived supported-available (matrix syntax-only)
- Claimed verdict `pass`; independently derived verdict `pass`
- Proof C claimed `7d791f7c7eeb94a0519bcb9fe3426f9cd331badf1a4fc67a8c5572de4028950f`; expected `8b41aba5c1f8ddb6bee39ba9808b2316381f11adc855cf0664ca51e85117a76c`
- Tamper: stale-hash control `True`; semantic refuse `True`; tampered `proof3:c09833ece4b29e9bbf5a6bc11e99fb264f8a4e3f2910fded9d9454b670bf8580`

Failed joins:

- `structural:execution-inputs-laws` — EXECUTION_INPUTS_APPLICABILITY: EXECUTION_INPUTS_APPLICABILITY: clones-fact/clones: host unsupported-typed != derived supported-available (matrix syntax-only)
- `fullsemantic:proof-C-compare-kit-evaluationInputRefs` — expected proof3:d61754bcf6024256a1e5ced071f5a8062a5da1f5842aeb5ea15823f5d5faebbe claimed proof3:22e08d2fa0618444910aff48ea7bc8d862cde7c837cc6473024f095681ff6337
- `fullsemantic:proof-C-compare` — expected proof3:d61754bcf6024256a1e5ced071f5a8062a5da1f5842aeb5ea15823f5d5faebbe claimed proof3:22e08d2fa0618444910aff48ea7bc8d862cde7c837cc6473024f095681ff6337
- `fullsemantic:proof-identity-compare` — proof3:d61754bcf6024256a1e5ced071f5a8062a5da1f5842aeb5ea15823f5d5faebbe
- `fullsemantic:proof-field-diffs` — evaluationInputRefs

Original required properties:

- `R-RUN-SYNTAX-DATA` FAIL — REFUSED
- `inventory-present` PASS — 
- `R-RUN-UNAVAILABLE-SEMANTIC` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "language-tier-unsupported", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:13adc7be85220299600b702d96a900fb64f6691caa8a1e0d2d9e239a0762d29f"}, "nativeCause": "capability-missing", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": true, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `not-complete-empty-concealment` PASS — 
- `syntax-only-no-ts-rust-unit` PASS — native.context.syntax.v2
- `clones-account-applicability-vs-matrix-SUPPORTED-DESIGN` FAIL — unsupported-typed
- `clones-fact-cell-not-complete-from-unsupported-typed` FAIL — state=complete app=unsupported-typed

Requested capabilities / cell outcomes:

```json
{
  "requested": [
    {
      "capabilityId": "clones-fact",
      "languageMode": "syntax-only",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "inventory",
      "languageMode": "syntax-only",
      "required": true,
      "workspaceRoot": "."
    }
  ],
  "cells": [
    {
      "ordinal": 0,
      "capabilityId": "clones-fact",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    },
    {
      "ordinal": 1,
      "capabilityId": "inventory",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    }
  ],
  "coverages": [
    {
      "relation": "package",
      "resolution": "manifest-declared",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "clones",
      "resolution": "normalized-body-hash",
      "coverage": "unknown",
      "deficiency": "language-tier-unsupported",
      "nativeCause": "capability-missing"
    },
    {
      "relation": "file",
      "resolution": "enumerated",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    }
  ]
}
```

### `rust-partial-clones`

- Store SHA-256 `227856b1dec3c4d051677e156b9b3883613a90dee7e1c8db46670bb95a4e1141` (501289 bytes, 77 blobs)
- Run `run3:679b3d194b062fa3b113a453b9c45c01da530fa0d553570f8d98d44a50832737`
- Plan `plan2:a98f5aab0dfe84694a41f36aa5aa33bc2a152e46f33fe6e02c577d74d45fd8c5`
- Claimed proof `proof3:607fbbdb8b74c939ac42e6506c8b0c3f09dfc4c186b7c458f3eb3f8f8cc9ba5a`
- Independently reconstructed proof `proof3:00d38df253fcf1f3d8bdf6fc3749276e987adbd21d7533efc62fc9a9c0f259f9`
- Layers: raw `PASS` / schema `PASS` / structural `REFUSED` / fullsemantic `REFUSED`
- Overall: **REFUSED**
- First refusal: `structural:domainSet-joins` — SNAPSHOT_JOIN_PATH: SNAPSHOT_JOIN_PATH: uni.crateRootPaths #/a
- Claimed verdict `pass`; independently derived verdict `indeterminate`
- Proof C claimed `3ecd8de773be3907f46e698d5d4a10ddf9c70b091249f4be699bdf2835aa8ca4`; expected `32e26f582810195185369412179e2da5c63742d797ef402c67b338243caee842`
- Tamper: stale-hash control `True`; semantic refuse `True`; tampered `proof3:a1c0fcc48b9410c89848b8d1677edd04044b877a46cecad80b703424403b786b`

Failed joins:

- `structural:domainSet-joins` — SNAPSHOT_JOIN_PATH: SNAPSHOT_JOIN_PATH: uni.crateRootPaths #/a
- `structural:component-manifest` — TREE_MEMBER_LENGTH: TREE_MEMBER_LENGTH: bin/proc-macro-srv
- `fullsemantic:proof-C-compare-kit-evaluationInputRefs` — expected proof3:00d38df253fcf1f3d8bdf6fc3749276e987adbd21d7533efc62fc9a9c0f259f9 claimed proof3:607fbbdb8b74c939ac42e6506c8b0c3f09dfc4c186b7c458f3eb3f8f8cc9ba5a
- `fullsemantic:proof-C-compare-if-policy-and-rule-program-added-to-evaluationInputRefs` — enumeration-contract.v1.md §7 names selectedRefs + execution-inputs only; policy/rule-program extras are recorded, not used to waive the kit field
- `fullsemantic:proof-C-compare` — expected proof3:00d38df253fcf1f3d8bdf6fc3749276e987adbd21d7533efc62fc9a9c0f259f9 claimed proof3:607fbbdb8b74c939ac42e6506c8b0c3f09dfc4c186b7c458f3eb3f8f8cc9ba5a
- `fullsemantic:proof-identity-compare` — proof3:00d38df253fcf1f3d8bdf6fc3749276e987adbd21d7533efc62fc9a9c0f259f9
- `fullsemantic:proof-field-diffs` — evaluationInputRefs,executionDeficiencies,verdict

Original required properties:

- `R-RUN-RUST-PARTIAL-EMPTY-CLONES` PASS — graph present
- `empty-clone-facts` PASS — ['package', 'file']
- `clones-coverage-unknown` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "input-closure-incomplete", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:bbe0bcb7be86f8ed0dcbcd9bf5ace64d05fff041ae5832dd1059521bb4c44413"}, "nativeCause": "body-language-owner-unenumerated", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": false, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `R-CLONE-DEFICIENCY-PAIRING` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "input-closure-incomplete", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:bbe0bcb7be86f8ed0dcbcd9bf5ace64d05fff041ae5832dd1059521bb4c44413"}, "nativeCause": "body-language-owner-unenumerated", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": false, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `clones-fact-cell-derived-partial` PASS — {"state": "partial", "deficiency": "input-closure-incomplete", "nativeCause": "body-language-owner-unenumerated"}
- `does-not-claim-complete-from-partial-ownership` PASS — partial
- `file-present-inventory-complete` PASS — 
- `seal-not-false-pass-on-required-partial` PASS — derived=indeterminate claimed=pass

Requested capabilities / cell outcomes:

```json
{
  "requested": [
    {
      "capabilityId": "clones-fact",
      "languageMode": "rust-cargo",
      "required": true,
      "workspaceRoot": "."
    },
    {
      "capabilityId": "inventory",
      "languageMode": "rust-cargo",
      "required": true,
      "workspaceRoot": "."
    }
  ],
  "cells": [
    {
      "ordinal": 0,
      "capabilityId": "clones-fact",
      "state": "partial",
      "deficiency": "input-closure-incomplete",
      "nativeCause": "body-language-owner-unenumerated",
      "required": true
    },
    {
      "ordinal": 1,
      "capabilityId": "inventory",
      "state": "complete",
      "deficiency": null,
      "nativeCause": null,
      "required": true
    }
  ],
  "coverages": [
    {
      "relation": "clones",
      "resolution": "normalized-body-hash",
      "coverage": "unknown",
      "deficiency": "input-closure-incomplete",
      "nativeCause": "body-language-owner-unenumerated"
    },
    {
      "relation": "file",
      "resolution": "enumerated",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    },
    {
      "relation": "package",
      "resolution": "manifest-declared",
      "coverage": "complete",
      "deficiency": null,
      "nativeCause": null
    }
  ]
}
```

## Applicable-law inventory (executed)

- lexical/C/H/CVE1 on retained bytes
- owning-schema stock JSON Schema + x-opensip-order via pinned local $id registry
- x-opensip-digest annotations on graph records
- x-opensip-payload-registry for relation/coverage/import/parameter
- relation registry ladder/universe/anchor/rung/snapshotJoins
- file coverageTotality + coveragePartitionLaw
- identity-schemas.v3 domainSets nestedIdentities/nestedRecords/snapshotJoins/blobJoins/closureJoins
- closureMembership direct/equalToDirect + detector extra selected
- component-manifest stored-bytes join (no v11 inhabitance)
- capabilityManifestId SHA256(UTF8(opensip.capability-manifest.v1)||00||CVE1 bytes)
- execution-inputs selectedRefs totality, view-only stage, hostDerivedRefs
- native coverage account totality vs matrix relations; applicability from matrix cell state + VCS
- derive_account + derive_outcome joined to host CellProgramOutcomeV1
- enumeration inventory one-per-cell-program-kind
- FACT-IDENTITY L0 frame + languageVersion derivation
- scopeCapabilityLaw for clones under closed-suffix-table universes
- complete expected proof from selected program/evidence/scope/Coverage/import/enumeration/execution inputs
- logical-result tamper vs stale-hash separately; whole-replacement identity join separately
- composition §5 required executionDeficiencies → sealed indeterminate

## Unexecuted obligations

- ROOT-ADMISSION (outside this validator role; not presumed)
- component-manifest-schemas.v11 stock inhabitance / signature envelopes (CANDIDATE-NOT-APPLIED)
- real host/compiler/crypto/SQLite execution (synthetic TCB observations used; structural joins still executed)
- L1 token-stream tokenisation where L1 facts are absent
- default-profile remaining matrix cells not requested by these Plans
- incoming-search / target-attribution / sufficiency_v2 incoming completeness (no such selected records on these four graphs)
- whole-consumer ACCEPT / other original requirements outside these four Runs

## Whole-replacement graph

{
  "kind": "whole-replacement-graph-admission",
  "note": "A foreign proof3 identity cannot join this Run's evaluation-seal.proofBundleId. Independently reminting a replacement proof is not treated as the consumer's accepted graph.",
  "executed": true,
  "tsProof": "proof3:ab7796b647e93608b36dbae713977d088f41882682bff889dfaed39a6f86e0c7",
  "rustProof": "proof3:026843f105a1bdc931091b8224eec091fb5cd2aa0961efef1efa1dd2c5e4e86c",
  "distinct": true,
  "result": "foreign-proof-would-fail-seal-join"
}

Diagnostic expected proofs were constructed only in this validator's output. Consumer stores were not reminted.

