# Other-runs independent kit-only review

**Verdict: `OTHER_RUNS_REFUSED`**

Independent kit-only validator of four reconstructed Runs. Same origin as the prior four-Run and foundation reviews. Not whole-consumer ACCEPT. Root admission not performed. Foundation/pilot/workflows/syntax-code outside this recheck.

This is not whole-consumer ACCEPT, not product implementation, and not root admission.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80; expected `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` match=True |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match=True |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | expected `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` match=True |
| `snapshot-manifest.json` | `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` | PASS 343/343; expected `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` match=True |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`

Reproducible command:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/independent/review_four.py
```

Consumer helper PASS, saved evaluator output, completion-review claims, and copied review files inside the snapshot were treated as claims under review, not oracles.

Expected proofs were reconstructed from selected execution inputs. Claimed proof fields were not copied. Positive graph admission precedes semantic comparison. Diagnostics after a first refusal are `diagnostic/notReached` for acceptance, not successful replay.

## Original per-Run property map

| ID | Kind | Observable | In this recheck |
|---|---|---|---|
| `R-RUN-TS` | completeRun | exported store/object table/frames for this Run plus replay export | yes |
| `R-RUN-TS-NODE-MODULES` | completeRunProperty | retained dependency layout / node_modules observation as the kit requires, exhibited on R-RUN-TS | yes |
| `R-RUN-TS-CONFIG-DEPS` | completeRunProperty | retained config-graph and dependency-layout preimages on R-RUN-TS | yes |
| `R-RUN-RUST` | completeRun | exported Rust Run frames plus replay | yes |
| `R-RUN-RUST-MIXED-EDITION` | completeRunProperty | edition map with more than one edition on a claimed Rust complete Run | yes |
| `R-RUN-RUST-TARGET-EDITION` | completeRunProperty | measured target edition ≠ package default on a claimed Rust complete Run | yes |
| `R-RUN-RUST-BODY-DIALECT` | completeRunProperty | clone/body records carrying derived dialect, not a workspace-wide guess | yes |
| `R-RUN-RUST-SAME-FILE-TWO-EDITIONS` | completeRunProperty | ownership/selection exhibiting one path under two selected target editions | yes |
| `R-RUN-RUST-PARTIAL-EMPTY-CLONES` | completeRun | exported graph whose clones Coverage is the published partial/unknown pairing, not complete-empty from partial ownership | yes |
| `R-RUN-RUST-HASH-MARKER` | completeRunProperty | inventoried path containing the published # marker form | yes |
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | completeRunProperty | two retained graphs or an explicit pair vector comparing body identities | yes |
| `R-RUN-RUST-LARGE-EDITION-MAP` | completeRunProperty | retained edition map plus derived version component; may be on a claimed Rust Run or a pair vector that still uses admitted context/body provenance | yes |
| `R-RUN-RUST-VERSION-COMPONENT` | completeRunProperty | measured derivation inputs (admitted context, body provenance) retained | yes |
| `R-RUN-FILE-FACT-INVENTORY` | completeRun | exported Run whose file facts join snapshot inventory path, digest, and length under the registered file law | yes |
| `R-RUN-CLONES-L0-AND-NORMALIZED` | completeRunProperty | L0 and normalized clone facts with retained frames | yes |
| `R-RUN-CLONES-CUSTODY` | completeRunProperty | retained level-specification bytes and language-version derivation inputs | yes |
| `R-RUN-SYNTAX-DATA` | completeRun | exported syntax data Run; clones/unsupported capabilities not complete-empty when unsupported | yes |
| `R-RUN-UNAVAILABLE-SEMANTIC` | completeRunProperty | published deficiency/nativeCause (or equivalent kit pairing) on the unsupported request | yes |
| `R-RUN-NONCEMPTY-CONTEXT` | completeRunProperty | plan.nativeContextDigests nonempty and retained on those Runs | yes |
| `R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC` | completeRunProperty | analysis-spec parameter on a claimed complete Run citing that document/selector | yes |
| `R-IMPORTED-PAYLOAD-IN-GRAPH` | completeRunProperty | imported payload retained and referenced from a claimed complete Run | yes |
| `R-CLONE-DEFICIENCY-PAIRING` | completeRunProperty | Coverage entry pairing measured against the cited kit selectors | yes |
| `R-NATIVE-PREIMAGE-JOINS` | completeRunProperty | retained nested preimages joining the universe/context fields that name them | yes |
| `R-RUN-SYNTAX-CODE` |  | syntax-code store frozen this pass; outside this four-Run recheck | no |

## First-refusal map (existing published law)

| Run | Raw | Schema | Structural | Fullsemantic | First refusal |
|---|---|---|---|---|---|
| `ts` | PASS | PASS | PASS | PASS | none |
| `rust` | PASS | PASS | PASS | PASS | none |
| `syntax-data` | PASS | PASS | PASS | PASS | none |
| `rust-partial-clones` | PASS | PASS | PASS | PASS | none |

Prior v1 first refusals rechecked on these NEW stores (not waived by historical labels):

- `ts`: IMPORT_PAYLOAD_SCHEMA RuntimePayloadV1 format=json / null observationWindow
- `rust`: crateRootPaths #/a not inventoried; TREE_MEMBER_LENGTH proc-macro-srv 13 vs 14; BODY_LANGUAGE_OWNER_AMBIGUOUS dual selectedUnitIds
- `syntax-data`: clones-fact account unsupported-typed vs matrix SUPPORTED-DESIGN
- `rust-partial-clones`: crateRootPaths + tree length + claimed pass vs required partial (composition §5)
- `all`: evaluationInputRefs extras policy/rule-program vs enumeration-contract §7

Classification:

- **Existing-law corrections independently verified on these NEW stores:**
  - `ts.import-payload-RuntimePayloadV1`: istanbul-json format and object observationWindow inhabit payload registry; first refusal gone
  - `rust.crateRootPaths`: crateRootPaths is inventoried `#/a/Cargo.toml`, not `#/a`
  - `rust.tree-member-length`: component-manifest TREE_MEMBER_LENGTH join passed (proc-macro-srv declared length equals retained blob)
  - `rust.body-language-owner`: sealed selectedUnitIds is one edition; BODY_LANGUAGE_OWNER_AMBIGUOUS not raised; pair vector exhibits two selections of `#/a/src/lib.rs`
  - `syntax-data.clones-applicability`: clones-fact account is supported-available (matrix SUPPORTED-DESIGN); Coverage unknown+language-tier-unsupported/capability-missing; required cell partial; seal indeterminate
  - `rust-partial.composition-s5`: required partial cell produces native executionDeficiencies and sealed indeterminate, not a false pass
  - `evaluationInputRefs`: proof.evaluationInputRefs equals selectedRefs plus execution-inputs only (enumeration-contract §7 / composition v3)
  - `whole-run-tamper`: each admitted graph reminted proof+evidence+seal+run; replacement structurally admitted; semantic C/identity refused. Stale-hash C-inequality recorded separately. Foreign proof IDs were not used as that execution.
- **Remaining original accept-blocking property misses (not waived by graph identity inequality or file presence):**
  - `R-RUN-CLONES-L0-AND-NORMALIZED` on ['ts', 'rust']: original observable requires L0 **and** a normalized-level clone fact with retained frames. These graphs retain only `normalisationLevel=L0-verbatim` clones facts (resolution `normalized-body-hash` is the clones ladder rung, not a second normalisation level). Syntax-code is frozen/outside this recheck and is not used as a waiver.
  - `R-RUN-CLONES-CUSTODY` on ['ts', 'rust']: original observable requires L0 **and** a normalized-level clone fact with retained frames. These graphs retain only `normalisationLevel=L0-verbatim` clones facts (resolution `normalized-body-hash` is the clones ladder rung, not a second normalisation level). Syntax-code is frozen/outside this recheck and is not used as a waiver.
- **Absent/contradictory published law:** none used as a waiver. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED; stored-bytes tree join was still executed. Prose identity/execution/composition/atom/native contracts were executed even though they are not stock JSON Schema.
- **Not invented default-profile cells:** these Plans request explicit capability subsets; unselected `calls`/`types`/`references` were not demanded.
- **Not a two-complete-graphs requirement** for `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`: original observable permits two retained graphs or an explicit pair vector. This recheck uses the explicit pair plus independently derived L0/ownership identities.

## Per-Run outcomes

### `ts`

- Store SHA-256 `ca1b44df3f89bc6d6cc63edfe239ce510a60c7fc47f2d531c5bcb10385b99086` (678620 bytes, 115 blobs)
- Run `run3:9fb05cf2f6ead9bec2ca4f4b773ceb2cba38520582a145f52520b23b51386190`
- Plan `plan2:9a6654ad5f4e7c976f826f2c7094fc7c14af853bac8afc8bc096fb9e710e21f7`
- Claimed proof `proof3:6969b09b5f6b0256ff9afb89407a843f3af379a372d206a9eb380e5eb67f8500`
- Independently reconstructed proof `proof3:6969b09b5f6b0256ff9afb89407a843f3af379a372d206a9eb380e5eb67f8500`
- Layers: raw `PASS` / schema `PASS` / structural `PASS` / fullsemantic `PASS`
- Overall: **ADMIT**
- First refusal: none
- Claimed verdict `pass`; independently derived verdict `pass`
- Proof C claimed `f1d4454d185cf01344672fec71daf6c7ccdc2d6037fc8c0342eb31e1e03045be`; expected `f1d4454d185cf01344672fec71daf6c7ccdc2d6037fc8c0342eb31e1e03045be`
- Tamper: stale-hash control `True`; semantic C-differs `True`; whole-Run executed `True` reason `reminted-proof-evidence-seal-run-then-admitted`; replacement admitted `True`; semantic refuse after admit `True`; reminted proof `proof3:fb2cb77f5a2ef64c1f3186e10da30505a335a34ac0c344315b0f7afa218dab37` run `run3:3e301db2782655cb9583b83454d18618b580eb90e0b11f6dc50e4eafa367dd1a`

Original required properties:

- `R-RUN-TS` PASS — overall=ADMIT layers={'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'}
- `R-RUN-TS-NODE-MODULES` PASS — inventoried node_modules paths plus ResolvedNodeModulesLayoutV1 nestedRecord join, not file-presence of a review artifact
- `R-RUN-TS-BARE-SPECIFIER` PASS — imports payload specifier=left-pad on admitted graph member
- `R-RUN-NONCEMPTY-CONTEXT` PASS — ['271a6043c1bf60bb25e814f08ff495bf7bd15b582d5b6cffc3f086ce9986f605']
- `R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC` PASS — analysis-spec parameter ScopeDocumentV1
- `R-IMPORTED-PAYLOAD-IN-GRAPH` PASS — ['import2:98fee8f9a2333a46e2a58a198642cc3cce63d9ca000e535bb86ddb0f614a2c1c']
- `R-RUN-FILE-FACT-INVENTORY` PASS — file facts plus snapshot inventory join
- `R-RUN-CLONES-L0` PASS — L0 frame retained and joined
- `R-RUN-CLONES-L0-AND-NORMALIZED` FAIL — clone normalisationLevel values on this graph=['L0-verbatim']; original observable is L0 and a normalized-level clone fact with retained frames, not only resolution=normalized-body-hash
- `R-RUN-CLONES-CUSTODY` FAIL — L0 span + languageVersion custody executed; normalized-level fact/frame not present so custody of that level is not exhibited
- `R-RUN-TS-CONFIG-DEPS` PASS — ['nestedRecord:nodeModulesLayout', 'nestedRecord:configGraph']
- `R-NATIVE-PREIMAGE-JOINS-TS` PASS — ['nestedRecord:nodeModulesLayout', 'nestedRecord:configGraph']

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

- Store SHA-256 `3b4daf1caa81f11cbaa255feede860c27fc81dd27b92e1f31cb9de634570d791` (541150 bytes, 102 blobs)
- Run `run3:db63563987becdd0079573e16ba47f09fcb3d4b216904a873c29528bf7ddb23a`
- Plan `plan2:25d8e4df72f3c2041966cc9bd0b9afe6d83fbbe5e5bdf9c07699082f49068545`
- Claimed proof `proof3:8c329c54977da78ecdb92e42ae2acb948134fc39e1ca16095166f7ccdf9d8ea2`
- Independently reconstructed proof `proof3:8c329c54977da78ecdb92e42ae2acb948134fc39e1ca16095166f7ccdf9d8ea2`
- Layers: raw `PASS` / schema `PASS` / structural `PASS` / fullsemantic `PASS`
- Overall: **ADMIT**
- First refusal: none
- Claimed verdict `pass`; independently derived verdict `pass`
- Proof C claimed `d7efff1f22134bb1ca00796cfc6865f949a3d37d8b9d5274f7a7e08639e3b62b`; expected `d7efff1f22134bb1ca00796cfc6865f949a3d37d8b9d5274f7a7e08639e3b62b`
- Tamper: stale-hash control `True`; semantic C-differs `True`; whole-Run executed `True` reason `reminted-proof-evidence-seal-run-then-admitted`; replacement admitted `True`; semantic refuse after admit `True`; reminted proof `proof3:68493d8a901e9b8e0419201fb7d972d0d88adade98d05f71166d1b32feb60280` run `run3:db3aa6e25cb30c8f14f8fca5ced5cba80ef5c68db7a9de5760777f267d8623b6`

notReached:

- `imported-payload-in-graph` — this Run has empty plan.importIds

Original required properties:

- `R-RUN-RUST` PASS — overall=ADMIT layers={'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'}
- `R-RUN-NONCEMPTY-CONTEXT` PASS — 
- `R-RUN-RUST-HASH-MARKER` PASS — ['#/Cargo.toml', '#/a/Cargo.toml', '#/a/src/lib.rs']
- `R-RUN-RUST-MIXED-EDITION` PASS — {"a": 2018, "crate00": 2015, "crate01": 2018, "crate02": 2021, "crate03": 2024, "crate04": 2015, "crate05": 2018, "crate06": 2021, "crate07": 2024, "crate08": 2015, "crate09": 2018, "crate10": 2021, "crate11": 2024, "crate12": 2015, "crate13": 2018, "crate14": 2021, "crate15": 2024}
- `R-RUN-RUST-LARGE-EDITION-MAP` PASS — 17
- `R-RUN-FILE-FACT-INVENTORY` PASS — 
- `R-RUN-CLONES-L0` PASS — 
- `R-RUN-CLONES-L0-AND-NORMALIZED` FAIL — clone normalisationLevel values on this graph=['L0-verbatim']; original observable is L0 and a normalized-level clone fact with retained frames, not only resolution=normalized-body-hash
- `R-RUN-CLONES-CUSTODY` FAIL — L0 span + languageVersion custody executed; normalized-level fact/frame not present so custody of that level is not exhibited
- `R-NATIVE-PREIMAGE-JOINS-RUST` PASS — ['nestedIdentity:packages.[].fileManifestSha256:empty', 'nestedIdentity:dependencySourceSetId', 'nestedIdentity:unifiedFeaturesId', 'nestedIdentity:preparedOutputSetId:null', 'nestedIdentity:packages.[].fileManifestSha256:empty', 'nestedIdentity:dependencySourceSetId', 'nestedIdentity:unifiedFeaturesId', 'nestedIdentity:preparedOutputSetId:null', 'nestedIdentity:configProjectionSha256', 'nestedIdentity:sourceUnitOwnershipId']
- `R-RUN-RUST-BODY-DIALECT` PASS — derived from rustc context + selected target edition; ownership does not enter body-language-version
- `R-RUN-RUST-TARGET-EDITION` PASS — packageDefault=2018 measured=('sha256:1e4e1cda7b538b89dc972eea01680dcea67d7ca8ca34e4cc2a22aa7ebc4342b3', 2018, 2021) units=[{'unitId': 'sha256:1e4e1cda7b538b89dc972eea01680dcea67d7ca8ca34e4cc2a22aa7ebc4342b3', 'crateName': 'a', 'targetEdition': 2021, 'kind': 'bin'}, {'unitId': 'sha256:7291519e6b819789a4669bc7f69158790980b844ec917d4493b05ae4120e0b2b', 'crateName': 'a', 'targetEdition': None, 'kind': 'lib'}, {'unitId': 'sha256:dfae73d03e22c5efe812a07df22ac76e321f698694bae30a13cb16d6e8c1e823', 'crateName': 'a', 'targetEdition': None, 'kind': 'test'}]
- `sealed-selectedUnitIds-one-edition` PASS — selectedUnitIds=['sha256:1e4e1cda7b538b89dc972eea01680dcea67d7ca8ca34e4cc2a22aa7ebc4342b3'] selectedEditions=[2021]; kit selectionLaw admits one path at two editions one selection at a time, and refuses BODY_LANGUAGE_OWNER_AMBIGUOUS if both are stuffed into one selectedUnitIds
- `R-RUN-RUST-SAME-FILE-TWO-EDITIONS` PASS — path=#/a/src/lib.rs ownerUnits=3 editionsOnPath=[2018, 2021] sealedSelectedEditions=[2021] independentL0_2018=sha256:321e22ac744dc3e177f066bb8cec042d8ce2159ff7cf090a8ecbee96efc64d1b independentL0_2021=sha256:4cfa4328a9474482a26627a810afe941a6204782be4a9c1f248b71bf51e77fa8 pairVectorMatch=True. Lawful form is two selections / pair vector, not both editions in one selectedUnitIds.
- `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` PASS — explicit pair vector: same span + same edition ⇒ same L0 (ownership maps excluded from body-language-version); different edition ⇒ different L0. Not a two-complete-graphs requirement. independent={"l0_2018": "sha256:321e22ac744dc3e177f066bb8cec042d8ce2159ff7cf090a8ecbee96efc64d1b", "l0_2021": "sha256:4cfa4328a9474482a26627a810afe941a6204782be4a9c1f248b71bf51e77fa8", "distinctWhenDialectChanges": true, "stableSameDialect": true, "compilerVersion": "1.80.0", "compilerBuild": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef", "sealedLanguageVersion": "5507b2ff4fdcf6ac386c97ba3d2f80b0da46e1be74fb71792e36f9bfafc22b55", "spanBytes": 14, "selectionLibH": "sha256:0a1fc805e924acea4f76c06137bf6954e6c383712cd148823726544ff391283d", "selectionBinH": "sha256:e66847b3852e97605c66a2075c7aa9f155ea7e7d1c6aac2895e6752308514a27"}
- `R-RUN-RUST-VERSION-COMPONENT` PASS — compilerVersion=1.80.0 compilerBuild=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef dialectKey=edition; languageVersion is SHA-256(C(body-language-version))
- `pair-vector-l0-preimage-match` PASS — claimed pair 2018=sha256:321e22ac744dc3e177f066bb8cec042d8ce2159ff7cf090a8ecbee96efc64d1b 2021=sha256:4cfa4328a9474482a26627a810afe941a6204782be4a9c1f248b71bf51e77fa8 independent 2018=sha256:321e22ac744dc3e177f066bb8cec042d8ce2159ff7cf090a8ecbee96efc64d1b 2021=sha256:4cfa4328a9474482a26627a810afe941a6204782be4a9c1f248b71bf51e77fa8
- `pair-vector-stable-selections-distinct-identities` PASS — {"selectionA": "sha256:0a1fc805e924acea4f76c06137bf6954e6c383712cd148823726544ff391283d", "selectionB": "sha256:24af01ccd3cf48597bbf899af1a0e43f3071d8396aca3c51a17d08b7dcab38d6", "l0": "sha256:321e22ac744dc3e177f066bb8cec042d8ce2159ff7cf090a8ecbee96efc64d1b", "equal": true}
- `pair-vector-not-two-complete-graphs` PASS — original observable permits two retained graphs OR an explicit pair vector; this check uses the explicit pair plus complete ownership/body preimages

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
      "relation": "clones",
      "resolution": "normalized-body-hash",
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
      "relation": "declares",
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
    },
    {
      "relation": "literal",
      "resolution": "syntactic",
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
    }
  ]
}
```

### `syntax-data`

- Store SHA-256 `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099` (490936 bytes, 65 blobs)
- Run `run3:4ec370fb40972db1f8dffa5e2921328e30df8a6348c6191560273fb817f61488`
- Plan `plan2:09e25c1ec3e3267c252402623391071321a6dc0d2551200dd504c23aabb61cd9`
- Claimed proof `proof3:d0d5b5f16e5bec05f20b724e2a8a40227c6cdea3efec4ecd9ae316c0b4a3bedc`
- Independently reconstructed proof `proof3:d0d5b5f16e5bec05f20b724e2a8a40227c6cdea3efec4ecd9ae316c0b4a3bedc`
- Layers: raw `PASS` / schema `PASS` / structural `PASS` / fullsemantic `PASS`
- Overall: **ADMIT**
- First refusal: none
- Claimed verdict `indeterminate`; independently derived verdict `indeterminate`
- Proof C claimed `490810b751f13a69531c15c012d267c590e2eddd3d45d7e1a098db264be48bcb`; expected `490810b751f13a69531c15c012d267c590e2eddd3d45d7e1a098db264be48bcb`
- Tamper: stale-hash control `True`; semantic C-differs `True`; whole-Run executed `True` reason `reminted-proof-evidence-seal-run-then-admitted`; replacement admitted `True`; semantic refuse after admit `True`; reminted proof `proof3:443f7d4eb88504d34de3010e51ec1209a776cef1413fe83af95a0e25b684b89c` run `run3:8abeb03ae05140b6045633ae3abd7ec06b163e5aa3a0644e44940294408f8dde`

notReached:

- `imported-payload-in-graph` — this Run has empty plan.importIds

Original required properties:

- `R-RUN-SYNTAX-DATA` PASS — overall=ADMIT layers={'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'}
- `inventory-present` PASS — 
- `R-RUN-UNAVAILABLE-SEMANTIC` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "language-tier-unsupported", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:13adc7be85220299600b702d96a900fb64f6691caa8a1e0d2d9e239a0762d29f"}, "nativeCause": "capability-missing", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": true, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `not-complete-empty-concealment` PASS — 
- `syntax-only-no-ts-rust-unit` PASS — native.context.syntax.v2
- `clones-account-applicability-vs-matrix-SUPPORTED-DESIGN` PASS — supported-available
- `clones-fact-cell-not-complete-from-unsupported-typed` PASS — state=partial app=supported-available
- `required-partial-sealed-indeterminate` PASS — derived=indeterminate claimed=indeterminate

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
      "state": "partial",
      "deficiency": "language-tier-unsupported",
      "nativeCause": "capability-missing",
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

- Store SHA-256 `89fd6accbc6181217e6605fbc6b4a058520b7ae8ce0cda3523f4a0a86b1a004c` (501541 bytes, 77 blobs)
- Run `run3:4852e398497daf2c361127a6fd82a59e5c82e01b4b6323ee6cb7750458faaca1`
- Plan `plan2:1539822bf2705d16d3bd57fca3cbd4b3b713622c37f873909e895a0c9c60ea5c`
- Claimed proof `proof3:9406360530804fa453f5b5a2ce7255c370bd004f19608afd4574fbf7aecd8754`
- Independently reconstructed proof `proof3:9406360530804fa453f5b5a2ce7255c370bd004f19608afd4574fbf7aecd8754`
- Layers: raw `PASS` / schema `PASS` / structural `PASS` / fullsemantic `PASS`
- Overall: **ADMIT**
- First refusal: none
- Claimed verdict `indeterminate`; independently derived verdict `indeterminate`
- Proof C claimed `3fd11e8c98c44dfd67e66bacf6545246d64fa6cc64268a0785694d6ca6a2186e`; expected `3fd11e8c98c44dfd67e66bacf6545246d64fa6cc64268a0785694d6ca6a2186e`
- Tamper: stale-hash control `True`; semantic C-differs `True`; whole-Run executed `True` reason `reminted-proof-evidence-seal-run-then-admitted`; replacement admitted `True`; semantic refuse after admit `True`; reminted proof `proof3:ac98d8c3acb8303103f5958b7350743f52d6b27c5de4662cfae562c761faaab9` run `run3:e1f576824c166613fc891ab07ea98fd614853bb0be3388352d82c384f6ce7a1c`

notReached:

- `imported-payload-in-graph` — this Run has empty plan.importIds

Original required properties:

- `R-RUN-RUST-PARTIAL-EMPTY-CLONES` PASS — overall=ADMIT layers={'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'}; complete-Run obligation requires admission, not only exhibited partial Coverage
- `empty-clone-facts` PASS — ['package', 'file']
- `clones-coverage-unknown` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "input-closure-incomplete", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:1b81d57a82b09031f0ad0114f97cdefe306323d60aa711eb02ee062765122efa"}, "nativeCause": "body-language-owner-unenumerated", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": false, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `R-CLONE-DEFICIENCY-PAIRING` PASS — [{"closedWorld": {"deadCodeRepairEligible": false, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown", "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}, "confidenceMillionths": 1000000, "coverage": "unknown", "deficiency": "input-closure-incomplete", "derivationKinds": [], "examinedUniverse": {"subjectCount": 1, "subjectScopeCommitment": "sha256:1b81d57a82b09031f0ad0114f97cdefe306323d60aa711eb02ee062765122efa"}, "nativeCause": "body-language-owner-unenumerated", "relation": "clones", "resolution": "normalized-body-hash", "resolutionCompleteness": {"attempted": false, "examinedExhaustive": false, "stageTerminal": "complete", "state": "not-applicable", "unresolvedEdgeClasses": [], "unresolvedEdgeCount": 0}}]
- `clones-fact-cell-derived-partial` PASS — {"state": "partial", "deficiency": "input-closure-incomplete", "nativeCause": "body-language-owner-unenumerated"}
- `does-not-claim-complete-from-partial-ownership` PASS — partial
- `file-present-inventory-complete` PASS — 
- `seal-not-false-pass-on-required-partial` PASS — derived=indeterminate claimed=indeterminate

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

- lexical/C/H/CVE1 on retained bytes (prose identity-and-evidence §3, not only stock JSON Schema)
- owning-schema stock JSON Schema + x-opensip-order via pinned local $id registry
- custom x-opensip-digest / x-opensip-payload-registry / domainSets annotations
- prose identity-and-evidence, native-evidence, execution-inputs, enumeration-contract §7, evaluator-composition v3, atom-evaluation
- recursive nestedIdentities/nestedRecords/snapshotJoins/blobJoins/closureJoins including native-nested ownership
- relation registry ladder/universe/anchor/rung/snapshotJoins
- file coverageTotality + coveragePartitionLaw
- closureMembership direct/equalToDirect + detector extra selected
- component-manifest stored-bytes join (no v11 inhabitance)
- capabilityManifestId SHA256(UTF8(opensip.capability-manifest.v1)||00||CVE1 bytes)
- execution-inputs selectedRefs totality, view-only stage, hostDerivedRefs
- native coverage account totality vs matrix relations; applicability from matrix cell state + VCS
- derive_account + derive_outcome joined to host CellProgramOutcomeV1
- enumeration inventory one-per-cell-program-kind
- FACT-IDENTITY L0 frame + languageVersion derivation (selectionLaw one-selection-at-a-time)
- scopeCapabilityLaw for clones under closed-suffix-table universes
- complete expected proof from selected program/evidence/scope/Coverage/import/enumeration/execution inputs (no copy of claimed proof fields)
- positive graph admission precedes semantic comparison; post-refusal diagnostics are notReached
- logical-result tamper stale-hash control separately; whole-Run remint of proof+evidence+seal+run then admit replacement then semantic refuse
- composition §5 required executionDeficiencies ⇒ sealed indeterminate
- Rust pair property as explicit pair vector with independently derived L0/ownership identities

## Unexecuted obligations

- ROOT-ADMISSION (outside this validator role; not presumed)
- component-manifest-schemas.v11 stock inhabitance / signature envelopes (CANDIDATE-NOT-APPLIED); stored-bytes tree join was still executed
- real host/compiler/crypto/SQLite execution (synthetic TCB observations used; structural joins still executed)
- L1 token-stream tokenisation where L1 facts are absent
- default-profile remaining matrix cells not requested by these Plans
- incoming-search / target-attribution / sufficiency_v2 incoming completeness (no such selected records on these four graphs)
- whole-consumer ACCEPT / other original requirements outside these four Runs
- foundation phases 0–4 / R-IMPORTED-OBSERVATION-BOUNDARY (retained prior origin; not this recheck)
- pilot / workflow / syntax-code store (frozen this pass; not this recheck)

Diagnostic expected proofs and reminted replacement graphs were constructed only in this validator's output. Consumer snapshot stores were not overwritten.

