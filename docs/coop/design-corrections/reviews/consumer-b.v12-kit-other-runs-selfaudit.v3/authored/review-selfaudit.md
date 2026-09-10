# Review-quality self-audit (other-runs v2)

**Successor four-Run verdict: `OTHER_RUNS_REFUSED`**

Same kit-only four-Run origin. This is not a new origin, not authoring, not whole-consumer ACCEPT, not product/real-host/compiler/crypto qualification. Stores were not modified.

The original charter (verbatim) is the quantifier/kind authority. Structured `requirements.json` organizes that charter; it does not replace it.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | expected match=True |
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS 80/80 |
| parent frozen | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | match=True |
| v2 snapshot-manifest | `feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c` | PASS 343/343 |
| preserved v2 other-runs-review.md | `782d91e34d48b6a1fb5f870ec8d1c295c7a0073456a11fe712150ad3c3c1300c` | match=True |
| preserved v2 other-runs-review.json | `ae7e81b8e2627d0fde27cf42dbc7bb7a67afc3188ecaa5a868c5a6d8068733ce` | match=True |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/independent/selfaudit.py
```

## Withdrawn grades

- **v2 OTHER_RUNS_REFUSED on R-RUN-CLONES-L0-AND-NORMALIZED / R-RUN-CLONES-CUSTODY as a per-TS-and-Rust demand** — Charter Phase 5 and requirements mayBeSatisfiedTogetherWith = TS|Rust|syntax-code. At-least-one-set. Syntax-code is pending global integration. Not a failure of each scoped graph.
- **v2 structural/fullsemantic PASS on ts** — Did not execute compilerPackageDigest closure-tree-member join (blob presence is not tree membership).
- **v2 structural/fullsemantic PASS on rust and rust-partial-clones** — Did not execute rustcVersion == tool-closure semanticVersion (native-context-compiler-version-not-from-manifest). Fullsemantic PASS after that miss is withdrawn; successor marks fullsemantic NOT_REACHED.
- **v2 fullsemantic PASS as successful replay on graphs whose native producing recipes were unexecuted** — Positive graph admission (including native re-admission) precedes semantic comparison. C equality of compose_proof is not native admission.

## Charter quantifiers (full charter, not the v2 condensed map)

Charter Phase 5: complete TS Run and complete Rust Run (and their Include properties); a separate Rust partial-enumeration complete Run; **at least one** complete file-fact Run (may be the same export as a TS, Rust, or syntax-code Run if those properties are actually present) carrying L0 **and** a normalized-level clone identity; syntax-code and syntax-data complete Runs; imported payload on **at least one** claimed complete graph.

v2 treated `R-RUN-CLONES-L0-AND-NORMALIZED` / `R-RUN-CLONES-CUSTODY` as a per-TS-and-Rust demand and used that as the four-Run refusal. That silently upgraded an at-least-one-set property. The unreviewed syntax-code member of that set is **pending global integration**, not a blanket waiver and not a failure of each scoped graph.

| ID | Kind | Quantifier | This recheck |
|---|---|---|---|
| `R-RUN-TS` | completeRun | exactly-the-named-complete-Run | in-scope: ts graph |
| `R-RUN-TS-NODE-MODULES` | completeRunProperty | property-of-R-RUN-TS | in-scope: ts graph |
| `R-RUN-TS-CONFIG-DEPS` | completeRunProperty | property-of-R-RUN-TS | in-scope: ts graph |
| `R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC` | completeRunProperty | property-of-R-RUN-TS | in-scope: ts graph |
| `R-RUN-RUST` | completeRun | exactly-the-named-complete-Run | in-scope: rust graph |
| `R-RUN-RUST-MIXED-EDITION` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph |
| `R-RUN-RUST-TARGET-EDITION` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph |
| `R-RUN-RUST-BODY-DIALECT` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph |
| `R-RUN-RUST-SAME-FILE-TWO-EDITIONS` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph + pair vector |
| `R-RUN-RUST-HASH-MARKER` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph |
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph + explicit pair vector |
| `R-RUN-RUST-LARGE-EDITION-MAP` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph or pair vector |
| `R-RUN-RUST-VERSION-COMPONENT` | completeRunProperty | property-of-R-RUN-RUST | in-scope: rust graph |
| `R-RUN-RUST-PARTIAL-EMPTY-CLONES` | completeRun | exactly-the-named-complete-Run | in-scope: rust-partial-clones graph |
| `R-CLONE-DEFICIENCY-PAIRING` | completeRunProperty | property-of-R-RUN-RUST-PARTIAL-EMPTY-CLONES | in-scope: rust-partial-clones graph |
| `R-RUN-SYNTAX-DATA` | completeRun | exactly-the-named-complete-Run | in-scope: syntax-data graph |
| `R-RUN-UNAVAILABLE-SEMANTIC` | completeRunProperty | property-of-R-RUN-SYNTAX-DATA | in-scope: syntax-data graph |
| `R-RUN-NONCEMPTY-CONTEXT` | completeRunProperty | both-named-parents | in-scope: ts and rust graphs |
| `R-IMPORTED-PAYLOAD-IN-GRAPH` | completeRunProperty | at-least-one-claimed-complete-positive | in-scope: satisfied if ts graph admits with import member |
| `R-NATIVE-PREIMAGE-JOINS` | completeRunProperty | on-the-language-Runs-that-name-them | in-scope: ts and rust nested preimages |
| `R-RUN-FILE-FACT-INVENTORY` | completeRun | at-least-one-of-TS-Rust-syntax-code | pending-global: may be ts or rust if file facts actually present; syntax-code outside |
| `R-RUN-CLONES-L0-AND-NORMALIZED` | completeRunProperty | property-of-that-at-least-one-file-fact-Run | pending-global: NOT a per-language/per-Run demand on every TS and Rust graph |
| `R-RUN-CLONES-CUSTODY` | completeRunProperty | property-of-R-RUN-CLONES-L0-AND-NORMALIZED | pending-global: same at-least-one set; not a per-Run demand |
| `R-RUN-SYNTAX-CODE` | completeRun | exactly-the-named-complete-Run | pending-global: outside this four-Run recheck |
| `R-RUN-NO-COMPILER-UNIT` | completeRunProperty | property-of-R-RUN-SYNTAX-CODE | pending-global: outside |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | standaloneCanonicalVector | standalone-vector | pending-global: outside |
| `R-RUN-UNSUPPORTED-GRAMMAR` | standaloneCanonicalVector | standalone-vector | pending-global: outside |

## v2 PASS claims vs producing/join laws

v2 structural/fullsemantic PASS executed stock schema, annotated digest *presence*, nested H frames, snapshot path joins, execution-inputs derive, and C(expected proof)==C(claimed). Identity-and-evidence §3 requires Run closure to **re-run owning native admission** over retained bytes (`admit_native_context` / `bind_*_universe`). Native-evidence §2 names field-producing recipes. Blob presence or H-frame parse is not those recipes.

Expected-proof C equality of a shared `compose_proof` (including predicate `inputRefs` citing `rule-program`) does not establish identity §3 subset/totality. Diagnostics after a first structural refusal are notReached, not successful replay.

### `ts`

- v2 layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall `ADMIT` first `None`
- successor layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal (acceptance-grade): `structural:ts.compilerPackageDigest-is-toolchain-tree-member` — compilerPackageDigest retention is closure-tree-member of toolClosure.closureId
- Law: native-evidence.schemas.v2.json TypeScriptToolchainIdentityV1.compilerPackageDigest x-opensip-digest retention=closure-tree-member; native-evidence.md §2.4
- Semantic: `NOT_REACHED`

Producing/join assertions (operands in JSON):

- `plan.nativeContextDigests-set-equals-retained-context` **PASS** — set of retained context frames must equal plan.nativeContextDigests
- `universe.nativeContextId-is-plan-selected` **PASS** — universe nativeContextId must be sha256: plus a Plan-selected context suffix
- `vcs.sourceInventoryDigest-equals-snapshot-inventory-C` **PASS** — vcs-observation.sourceInventoryDigest is raw SHA-256 of the snapshot inventory
- `evidence.importIds-equals-plan.importIds` **PASS** — semantic-evidence.importIds repeats the Plan-selected import set exactly
- `evidence.proofBundleId-equals-seal.proofBundleId` **PASS** — acyclic: evidence and seal name the same proof
- `seal.verdict-equals-proof.verdict` **PASS** — seal carries the proof verdict
- `evaluationInputRefs-contains-every-plan-import` **PASS** — evaluator3 proof names every Plan-selected import in evaluationInputRefs
- `predicate-inputRefs-subset-of-evaluationInputRefs` **DIAG** — claimed predicate inputRefs cite [{"digest": "bfc392674a431ed3b5e4ce966011236950fbab873273e86ef9a1319dddbeb615", "domain": "rule-program"}] not in evaluationInputRefs. ProofInputRef.domain enum includes rule-program; enumeration-contract §7 / composition v3 keep evaluationInputRefs = selectedRefs + execution-inputs. v2 compose_proof shared this citation. C equality of that shared derivation does not establish the subset sentence as written.
- `ts.toolClosure.kind-toolchain` **PASS** — toolClosure.closureId names retained kind=toolchain
- `ts.compilerVersion-equals-tool-closure-semanticVersion` **PASS** — compilerVersion is the semanticVersion of the admitted signed compiler closure manifest
- `ts.toolClosure.compiler-in-closure-tree` **PASS** — compiler raw digest is a member of the signed toolchain tree
- `ts.toolClosure.runtime-in-closure-tree` **PASS** — runtime raw digest is a member of the signed toolchain tree
- `ts.compilerPackageDigest-is-toolchain-tree-member` **FAIL** — compilerPackageDigest retention is closure-tree-member of toolClosure.closureId
- `ts.stdlib-closure-kind` **PASS** — typescriptStdlibMerkleRoot is the bare suffix of kind=stdlib closure2
- `ts.stdlib-inventory-complete-vs-tree-d.ts` **PASS** — standardLibraryComponentDigests is the complete .d.ts inventory of the retained stdlib tree
- `ts.libSelection-fold-equals-honored-lib` **PASS** — folded libSelection equals folded honoredOptions.lib
- `ts.libSelection-maps-to-retained-component` **PASS** — component(n)=lib.{fold(n)}.d.ts is in the declared component set
- `ts.moduleResolutionMode-equals-honored-moduleResolution` **PASS** — context moduleResolutionMode equals honoredOptions.moduleResolution
- `ts.nodeModulesInReadSet-iff-layout-digest-non-null` **PASS** — nodeModulesInReadSet is exactly (nodeModulesLayoutDigest is not null)
- `ts.executionCapableResolution-false` **PASS** — TypeScript universe executionCapableResolution is constant false
- `ts.tsconfigGraphHash-is-C-of-TypeScriptConfigGraphV1` **PASS** — tsconfigGraphHash is raw SHA-256 of C(TypeScriptConfigGraphV1)
- `ts.config-graph-nodes-equal-configGraphPaths` **PASS** — graph nodes[].path is exactly the context configGraphPaths set
- `ts.config-node-kind-derived-from-basename-table` **PASS** — every node's kind is the closed basename table, never asserted
- `ts.configOrigin-derived-from-entry-kind` **PASS** — configOrigin is derived from the retained graph, never asserted
- `ts.universe-languageMode-agrees-context` **PASS** — overlapping languageMode must agree

### `rust`

- v2 layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall `ADMIT` first `None`
- successor layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal (acceptance-grade): `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- Law: native-evidence.md §2.3/§11; identity-and-evidence.md §3 language-version binding chain
- Semantic: `NOT_REACHED`

Producing/join assertions (operands in JSON):

- `plan.nativeContextDigests-set-equals-retained-context` **PASS** — set of retained context frames must equal plan.nativeContextDigests
- `universe.nativeContextId-is-plan-selected` **PASS** — universe nativeContextId must be sha256: plus a Plan-selected context suffix
- `vcs.sourceInventoryDigest-equals-snapshot-inventory-C` **PASS** — vcs-observation.sourceInventoryDigest is raw SHA-256 of the snapshot inventory
- `evidence.importIds-equals-plan.importIds` **PASS** — semantic-evidence.importIds repeats the Plan-selected import set exactly
- `evidence.proofBundleId-equals-seal.proofBundleId` **PASS** — acyclic: evidence and seal name the same proof
- `seal.verdict-equals-proof.verdict` **PASS** — seal carries the proof verdict
- `evaluationInputRefs-contains-every-plan-import` **PASS** — evaluator3 proof names every Plan-selected import in evaluationInputRefs
- `predicate-inputRefs-subset-of-evaluationInputRefs` **DIAG** — claimed predicate inputRefs cite [{"digest": "67416e803513efd33d5a80aaef8fb4505da71895add95f763e976950be919e7b", "domain": "rule-program"}] not in evaluationInputRefs. ProofInputRef.domain enum includes rule-program; enumeration-contract §7 / composition v3 keep evaluationInputRefs = selectedRefs + execution-inputs. v2 compose_proof shared this citation. C equality of that shared derivation does not establish the subset sentence as written.
- `rust.toolClosure.kind-toolchain` **PASS** — toolClosure.closureId names retained kind=toolchain
- `rust.rustcVersion-equals-tool-closure-semanticVersion` **FAIL** — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- `rust.toolClosure.rustc-in-closure-tree` **PASS** — rustc raw digest is a member of the signed toolchain tree
- `rust.toolClosure.cargo-in-closure-tree` **PASS** — cargo raw digest is a member of the signed toolchain tree
- `rust.toolClosure.procMacroServer-in-closure-tree` **PASS** — procMacroServer raw digest is a member of the signed toolchain tree
- `rust.rustcDevLlvmDigest-kind` **PASS** — rustcDevLlvmDigest is the bare suffix of kind=rust-dev-llvm closure2
- `rust.executionCapableResolution-equals-prepared-not-none` **PASS** — executionCapableResolution is preparedResolution ≠ none; never a grant
- `rust.rustflags-equal-context-configProjection.rustflags` **PASS** — universe rustflags equals bound context configProjection.rustflags
- `rust.configProjectionSha256-is-H-of-context-configProjection` **PASS** — configProjectionSha256 is the 64-hex suffix of H(native.cargo-config-projection.v2, context.configProjection), not projectionSha256
- `rust.overlapping-nested-ids-agree` **PASS** — Rust overlapping nested identities must equal the bound context
- `rust.cfgSets-contain-every-baseCfg-member` **PASS** — every cfg set contains every member of the context baseCfg
- `rust.sourceUnitOwnership-required-for-clones-universe` **PASS** — a clones fact over any Rust universe requires committed SourceUnitOwnershipV1; null admits no clone
- `rust.unitId-derived-from-UnitIdentityV1` **PASS** — unitId is H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion,markerPath,targetKind,targetName}), derived retention

### `syntax-data`

- v2 layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall `ADMIT` first `None`
- successor layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall **ADMIT**
- First refusal: none
- Semantic: `PASS`

Producing/join assertions (operands in JSON):

- `plan.nativeContextDigests-set-equals-retained-context` **PASS** — set of retained context frames must equal plan.nativeContextDigests
- `universe.nativeContextId-is-plan-selected` **PASS** — universe nativeContextId must be sha256: plus a Plan-selected context suffix
- `vcs.sourceInventoryDigest-equals-snapshot-inventory-C` **PASS** — vcs-observation.sourceInventoryDigest is raw SHA-256 of the snapshot inventory
- `evidence.importIds-equals-plan.importIds` **PASS** — semantic-evidence.importIds repeats the Plan-selected import set exactly
- `evidence.proofBundleId-equals-seal.proofBundleId` **PASS** — acyclic: evidence and seal name the same proof
- `seal.verdict-equals-proof.verdict` **PASS** — seal carries the proof verdict
- `evaluationInputRefs-contains-every-plan-import` **PASS** — evaluator3 proof names every Plan-selected import in evaluationInputRefs
- `predicate-inputRefs-subset-of-evaluationInputRefs` **DIAG** — claimed predicate inputRefs cite [{"digest": "71aaef89749857b54552f394b368a64df5a3c70df079daf7109ee1bcc9381b40", "domain": "rule-program"}] not in evaluationInputRefs. ProofInputRef.domain enum includes rule-program; enumeration-contract §7 / composition v3 keep evaluationInputRefs = selectedRefs + execution-inputs. v2 compose_proof shared this citation. C equality of that shared derivation does not establish the subset sentence as written.
- `syntax.grammar-closure-kind` **PASS** — grammarBundle.closureId names kind=grammar
- `syntax.parserVersion-equals-closure-semanticVersion` **PASS** — parserVersion equals grammar closure semanticVersion
- `syntax.resolutionAttempted-false` **PASS** — syntax universe resolutionAttempted is false

### `rust-partial-clones`

- v2 layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'PASS', 'fullsemantic': 'PASS'} overall `ADMIT` first `None`
- successor layers {'raw': 'PASS', 'schema': 'PASS', 'structural': 'REFUSED', 'fullsemantic': 'NOT_REACHED'} overall **REFUSED**
- First refusal (acceptance-grade): `structural:rust.rustcVersion-equals-tool-closure-semanticVersion` — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- Law: native-evidence.md §2.3/§11; identity-and-evidence.md §3 language-version binding chain
- Semantic: `NOT_REACHED`

Producing/join assertions (operands in JSON):

- `plan.nativeContextDigests-set-equals-retained-context` **PASS** — set of retained context frames must equal plan.nativeContextDigests
- `universe.nativeContextId-is-plan-selected` **PASS** — universe nativeContextId must be sha256: plus a Plan-selected context suffix
- `vcs.sourceInventoryDigest-equals-snapshot-inventory-C` **PASS** — vcs-observation.sourceInventoryDigest is raw SHA-256 of the snapshot inventory
- `evidence.importIds-equals-plan.importIds` **PASS** — semantic-evidence.importIds repeats the Plan-selected import set exactly
- `evidence.proofBundleId-equals-seal.proofBundleId` **PASS** — acyclic: evidence and seal name the same proof
- `seal.verdict-equals-proof.verdict` **PASS** — seal carries the proof verdict
- `evaluationInputRefs-contains-every-plan-import` **PASS** — evaluator3 proof names every Plan-selected import in evaluationInputRefs
- `predicate-inputRefs-subset-of-evaluationInputRefs` **DIAG** — claimed predicate inputRefs cite [{"digest": "224cfc675965fb19212f7f84c7b293f0201212aa1f25fac5b03d19a6316e944d", "domain": "rule-program"}] not in evaluationInputRefs. ProofInputRef.domain enum includes rule-program; enumeration-contract §7 / composition v3 keep evaluationInputRefs = selectedRefs + execution-inputs. v2 compose_proof shared this citation. C equality of that shared derivation does not establish the subset sentence as written.
- `rust.toolClosure.kind-toolchain` **PASS** — toolClosure.closureId names retained kind=toolchain
- `rust.rustcVersion-equals-tool-closure-semanticVersion` **FAIL** — §2.3/§11 refuse native-context-compiler-version-not-from-manifest unless rustcVersion equals admitted tool closure semanticVersion
- `rust.toolClosure.rustc-in-closure-tree` **PASS** — rustc raw digest is a member of the signed toolchain tree
- `rust.toolClosure.cargo-in-closure-tree` **PASS** — cargo raw digest is a member of the signed toolchain tree
- `rust.toolClosure.procMacroServer-in-closure-tree` **PASS** — procMacroServer raw digest is a member of the signed toolchain tree
- `rust.rustcDevLlvmDigest-kind` **PASS** — rustcDevLlvmDigest is the bare suffix of kind=rust-dev-llvm closure2
- `rust.executionCapableResolution-equals-prepared-not-none` **PASS** — executionCapableResolution is preparedResolution ≠ none; never a grant
- `rust.rustflags-equal-context-configProjection.rustflags` **PASS** — universe rustflags equals bound context configProjection.rustflags
- `rust.configProjectionSha256-is-H-of-context-configProjection` **PASS** — configProjectionSha256 is the 64-hex suffix of H(native.cargo-config-projection.v2, context.configProjection), not projectionSha256
- `rust.overlapping-nested-ids-agree` **PASS** — Rust overlapping nested identities must equal the bound context
- `rust.cfgSets-contain-every-baseCfg-member` **PASS** — every cfg set contains every member of the context baseCfg
- `rust.sourceUnitOwnership-required-for-clones-universe` **PASS** — a clones fact over any Rust universe requires committed SourceUnitOwnershipV1; null admits no clone
- `rust.unitId-derived-from-UnitIdentityV1` **PASS** — unitId is H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion,markerPath,targetKind,targetName}), derived retention

## Checker exception/branch audit

- v2 admit_digest_field raw-artifact: rehash blob only; no closure-tree-member check for compilerPackageDigest (schema retention=closure-tree-member).
- v2 never compared NativeContextV2.toolchain.rustcVersion to closure.semanticVersion; no native-context-compiler-version-not-from-manifest.
- v2 never derived unitId from H(native.compilation-unit.v1, UnitIdentityV1) (this audit did; rust unitIds matched).
- v2 never derived TypeScript config node kind / configOrigin (this audit: tsconfig.json -> tsconfig, configOrigin=tsconfig matched).
- v2 never checked cfgSets ⊇ baseCfg, rustflags equality, configProjectionSha256 = H(cargo-config-projection) (this audit: those rust overlapping fields matched).
- v2 compose_proof always inserts domain=rule-program into predicate inputRefs; claimed proofs match that shared derivation; identity §3 subset sentence is not established by that C equality.
- v2 walk_digest_anns does not re-run admit_native_context / bind_rust_universe / bind_typescript_universe field-producing recipes; nested H parse + stock schema is not that admission.
- v2 first-refusal JoinLog continued proof-C-compare after structural refuse in earlier versions; current finish() marks later layers NOT_REACHED only from acceptance-grade joins — producing-rule misses were never those joins.

## Unexecuted / pending

- ROOT-ADMISSION outside this role
- component-manifest-schemas.v11 inhabitance (CANDIDATE-NOT-APPLIED); stored-bytes tree join still executed in v2
- real host/compiler/crypto/SQLite
- syntax-code / foundation / pilot / workflow / standalone vectors (pending global integration)
- Unicode Default Case Conversion beyond ASCII lib names (current libSelection is ASCII ES2022)
- L1–L3 clone token-stream recomputation (no such facts on these four graphs; at-least-one set pending syntax-code)

