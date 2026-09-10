# Normative law audit — identity-and-evidence.md §3 (entire)

This inventory covers **every paragraph** of `docs/v2/contracts/product-v1/identity-and-evidence.md` §3 (lines **87–1349**). It is a completeness check, **not** a substitute for execution. Each EXECUTED/KIT row names the checker function and measured operands in `normative-law-audit.json#/positiveLaws` (and `#/tamperLaws`).

Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` (ORIGINAL TASK REQUIREMENTS). Checker: `helper/s3_closure.py` `execute_s3_laws` / `execute_kit_s3_schema_laws`, invoked from `admit_graph` and `probes/normative_s3_audit.py`.

**Paragraphs:** 115. Unmapped: 0. Applicable-without-assertion: 0.

| disposition | count |
|---|---:|
| EXECUTED | 75 |
| KIT (kit-document law executed on frozen schemas) | 9 |
| N/A (not fields of this syntax-only graph) | 21 |
| META (heading / lead-in) | 9 |
| WITHDRAWN (replaced by payload registry) | 1 |

## Graphs

| Graph | Store | Structural §3 | Independent expected proof | Semantic C |
|---|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | PASS firstRefusal none | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` `usedClaimedProofFields=[]` | equal |
| Tamper | `f6e79d735620f0f5366e08e80375c3adfc443f84e1be6c9e6828b4509e165985` `run3:c624c90f491ea0175393b9431ac7f5331a23a62daaef7e1fecfc7d403fa7e7e3` | PASS firstRefusal none | same expected `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` | **unequal** (claimed fail vs derived pass) |

Expected proof is reconstructed from Plan, ExecutionInputs, policy projection, view/facts/coverage/inventories. Claimed proof fields are comparison operands only.

## What was missing before this pass (existing-law checker gaps, not new design)

Prior v2 admission walked annotated digests and payload-registry relation bytes, but did **not** execute as named assertions: lexical raw admission; H-frame native-context parse; plan.nativeContextDigests set equality; universe.nativeContextId bind; Coverage payloadSchemaDigest = exact full native-evidence document bytes + CoverageResultV3 + subjectScopeCommitment; file snapshotJoins (path/digest/length/rehash); anchorLaw per relation; clones body frame; rule-program exact policy projection; VCS inventory digest; Plan budget = analysis.budget; evidence.importIds; predicate inputRefs subset; program-predicate nodeDigest/address `p`; coverage partition and file@enumerated totality; stage-spec parameter subset; capabilityManifestId from retained bytes; acyclic proof. Those are now executed. **The retained graph bytes already satisfied them**; no identity remint was required.

N/A (not invented, not demanded): TS stdlib/rustc LLVM closures, nested rust dependency/cargo/prepared-output identities, ScopeDocumentV1 comparison binding, vcs-change.previousPath, commit-receipt, owner-source-set.

notReached (charter): L1 tokenisation judgment (level-spec freedom; frame/custody executed); component-manifest-schemas.v11 stock schema (prose field contract); ROOT-ADMISSION.

## Paragraph inventory

| lines | first sentence | disposition | graphs | checker lawIds | note |
|---|---|---|---|---|---|
| 87–87 | ## 3. Exact canonical encoding and identity preimages | META | both | — | section heading |
| 89–98 | The authoritative schema is `foundation/identity-schemas.v3.json` (closed | EXECUTED | both | S3-LEXICAL-BEFORE-DESERIALIZE | lexical admission before deserialize + bounds |
| 100–108 | Canonical JSON has UTF-8 byte-ordered keys, no whitespace or trailing newline, | EXECUTED | both | S3-C-REMAINDER-CONFIG, S3-ORDER-PREDICATE | C encoder; arrays admitted order |
| 110–124 | `x-opensip-order` is the machine-readable schema annotation for these orders, and | EXECUTED | both | S3-ORDER-PREDICATE | x-opensip-order vocabulary; predicate order on proof |
| 126–136 | Every array in identity-schemas.v3 carries this annotation: semantic collections | EXECUTED | both | S3-ORDER-PREDICATE, S3-RULE-PROGRAM-PROJECTION | identity-schemas array orders; policy ruleId order |
| 138–144 | Text maxLength counts Unicode scalar values, while the descriptor byte cap | EXECUTED | both | S3-LEXICAL-BEFORE-DESERIALIZE | text/path/span bounds via lexical+C remainder |
| 146–146 | For domain D and descriptor X: | META | both | — | lead-in to H recipe |
| 148–148 | `H(D,X) = SHA256(ASCII("opensip.product.v1") // 00 // ASCII(D) // 00 // uint64BE(length(C( | EXECUTED | both | S3-H-RECIPE-RUN, S3-H-RECIPE-PROOF | H(D,X) formula |
| 150–153 | The identifier is the prefix below, a colon, and lowercase H hex. A raw blob | EXECUTED | both | S3-H-RECIPE-RUN, S3-CAP-MANIFEST-ID | prefix + hex; raw blob vs semantic domain |
| 155–175 | / Domain / prefix / Exact semantic content (schema contains field types) / | EXECUTED | both | S3-H-RECIPE-RUN, S3-H-RECIPE-PROOF, S3-ACYCLIC-SEAL-HAS-BOTH | domain/prefix table for records in this graph |
| 177–192 | The graph is acyclic: proof does not include EvidenceId or RunId; evidence may | EXECUTED | both | S3-ACYCLIC-PROOF, S3-ACYCLIC-EVIDENCE-HAS-PROOF, S3-ACYCLIC-SEAL-HAS-BOTH | acyclic graph; fingerprint correspondence unused on unmatched tamper finding |
| 194–200 | Finding citations cannot introduce extra authoritative input roots. Fact and | EXECUTED | both | S3-FINDING-CITE-WITNESS, S3-PRED-INPUTREF-SUBSET, S3-EVIDENCE-IMPORT-IDS | finding citations; import unused still selected |
| 202–213 | CapabilityManifestId uses the inherited applied producing recipe and exact | EXECUTED | both | S3-CAP-MANIFEST-ID | capabilityManifestId recipe from committed bytes |
| 215–241 | **The effective registry is selected here, by name.** It is | KIT | kit | S3-KIT-DIGEST-DOMAINS, S3-KIT-PAYLOAD-REGISTRY | effective capability-manifest-domains.v2 selection; ADM gates in cap_manifest |
| 243–263 | `TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot` and | N/A | neither | S3-NA-TS-RUST-TOOLCHAIN | TS stdlib / rustc LLVM — syntax context has no those fields |
| 265–273 | The native `subjectScopeCommitment` is `"sha256:"` plus the 64-hex suffix | EXECUTED | both | S3-SCOPE-COMMITMENT, S3-COVERAGE-SCOPE-COMMIT | subjectScopeCommitment = sha256:+scope2 suffix |
| 275–286 | Native contexts have explicit H domains: `native.context.typescript.v2` over | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT, S3-PLAN-CONTEXT-SET | native.context.syntax.v2 H domain; plan.nativeContextDigests bare hex |
| 288–303 | Both of these are `h-identity` fields, so the object retained under each is the | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT, S3-GRAMMAR-TREE, S3-UNIVERSE-BIND-CONTEXT | frame proves retention never admission; re-run bind_syntax_universe / grammar tr |
| 305–317 | Beyond that, the closure re-derives the joins this contract names, from the | EXECUTED | both | S3-PLAN-CONTEXT-SET, S3-UNIVERSE-BIND-CONTEXT | re-derived context/universe joins; TS/Rust nested toolchain N/A |
| 319–329 | The native-context and native-universe source correspondence that this section | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE | repository paths in snapshot inventory (file payload path) |
| 331–352 | **All three** universe domains native §11 registers are registered here: | EXECUTED | both | S3-UNIVERSE-OWN-LANGUAGE-SYNTAX, S3-NA-NESTED-RUST-IDENTITIES | three universe domains; syntax bind; rust nested N/A |
| 354–365 | **Nested native semantic identities are records, not opaque strings.** A native | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | nested rust dependency/file-manifest identities |
| 367–372 | `CargoConfigProjectionV2` carries **two** digests that are not interchangeable: | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | CargoConfigProjectionV2 two digests |
| 374–381 | **Prepared products are inert data; execution authority stays operational.** A | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | prepared products / prepare-code grant |
| 383–383 | ### The closing digest law | META | both | — | ### The closing digest law |
| 385–396 | Arrays have a closing default; so do digests. **Every 64-hex field in | KIT | kit | S3-KIT-DIGEST-DOMAINS | closing digest law: every 64-hex field annotated; no field-name inference |
| 398–407 | The four representations are closed. They are the closed set of **terminal** | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT, S3-C-REMAINDER-CONFIG, S3-CAP-MANIFEST-ID | four terminal representations + by-domain selector |
| 410–415 | / Representation / Meaning / | EXECUTED | both | S3-CAP-MANIFEST-ID, S3-H-FRAME-NATIVE-CONTEXT, S3-PAYLOAD-REGISTRY-RELATION, S3-C-REMAINDER-CONFIG | representation table measured on present fields |
| 417–417 | The four retention modes are closed: | META | both | — | The four retention modes are closed: |
| 419–424 | / Retention / Meaning / | EXECUTED | both | S3-C-REMAINDER-CONFIG, S3-CAP-MANIFEST-ID | retention table |
| 426–442 | Because `H(D, X)` is `SHA256` of the framed preimage, **one** content-addressed | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT | H frame parse: prefix, domain, length, C remainder |
| 444–453 | Two things are easy to conflate here, so they are separated explicitly. The | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT, S3-PLAN-CONTEXT-SET | annotation vs spelling; bare-hex needs domain set |
| 455–463 | `plan.nativeContextDigests` is exactly this case, and it is a **set**. A Plan may | EXECUTED | both | S3-PLAN-CONTEXT-SET, S3-UNIVERSE-BIND-CONTEXT | plan.nativeContextDigests is a set; universe selects context |
| 465–472 | Reference `digest` fields (`Ref`, `ProofInputRef`, `FindingEvidenceRef`) take | EXECUTED | both | S3-PRED-INPUTREF-SUBSET, S3-PAYLOAD-REGISTRY-RELATION | Ref digest representation by-domain |
| 474–497 | Auxiliary digests therefore have producing rules, not caller-defined meanings: | EXECUTED | both | S3-BUDGET-EQUAL, S3-C-REMAINDER-CONFIG, S3-STAGE-SPEC-PARAMS | auxiliary digests: resolvedConfig, analysisSpec, semanticGrant, budget |
| 499–503 | `vcsDigest` hashes the closed `vcs-observation` record: schemaVersion 2, | EXECUTED | both | S3-VCS-INVENTORY | vcs-observation |
| 505–524 | The closure checker parses and exactly validates scope, semantic configuration, | EXECUTED | both | S3-PRED-INPUTREF-SUBSET, S3-EVIDENCE-COVERAGE-UNION, S3-EVIDENCE-IMPORT-IDS, S3-PROOF-IMPORTS-IN-EIREFS, S3-RULE-PROGRAM-PROJECTION | closure checker dispatch on annotation; witness/view/import joins |
| 526–535 | Every visited fact/scope and view/proof/execution/evidence/seal joins the current | EXECUTED | both | S3-H-RECIPE-RUN, S3-EXPECTED-PROOF-NO-CLAIMED-FIELDS | visited objects join Plan; profile3 reconstructs predicate tree |
| 537–553 | Import mapping/observation, correspondence, build identity, policy, rule-program | EXECUTED | both | S3-RULE-PROGRAM-PROJECTION, S3-VCS-INVENTORY, S3-PAYLOAD-REGISTRY-RELATION | policy/rule-program/waiver canonical-record; schema document bytes |
| 555–555 | ### The payload registry | META | both | — | ### The payload registry |
| 557–564 | An earlier draft of this section additionally required "a document offered as a | WITHDRAWN | kit | S3-KIT-PAYLOAD-REGISTRY | withdrawn vacuous-bundle sentence; replaced by payload registry |
| 566–569 | What replaces it is the thing that was actually missing: a closed registry saying, | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-PAYLOAD-REGISTRY-COVERAGE, S3-KIT-PAYLOAD-REGISTRY | payload registry law: full document bytes + selector + C |
| 571–579 | - `payloadSchemaDigest` is the **raw SHA-256 of the exact full bytes of the | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-PAYLOAD-REGISTRY-COVERAGE | payloadSchemaDigest raw SHA-256 of exact full document bytes |
| 581–586 | / Class / Keyed by / Document and selector / | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-PAYLOAD-REGISTRY-COVERAGE | registry class table |
| 588–588 | `view.schemaDigests` is the producer's own **declaration** of the schema documents its vie | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION | view.schemaDigests selected not derived; fact pins document |
| 590–598 | **The `ScopeDocumentV1` parameter row (CB3-MUST-4).** The comparison contract | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | ScopeDocumentV1 parameter row; this Plan selects none (zero legal) |
| 600–609 | It is deliberately a **different record** from the foundation `scope-descriptor` | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | scope-descriptor vs ScopeDocumentV1 |
| 611–626 | The bounded limitation is **accounted rather than lifted**. Today's two rows are | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | parameter class keying limitation |
| 628–638 | **How many entries may cite one row (CB8-MUST-1).** The paragraph above answers | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | at most one parameter per registered row |
| 640–651 | The rule is therefore stated for the class as a whole: **one Plan selects at most | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | zero legal; uniqueItems on parameters |
| 653–662 | It is enforced at three places, and the first two call one function so they cannot | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | enforced at pre-Plan and Run closure |
| 664–672 | **Where the binding is actually decided, and where it is only asserted.** | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | adopt_baseline is not this graph |
| 674–681 | The honest boundary is therefore stated rather than implied. `adopt_baseline` is | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | baseline scope binding verifier |
| 683–701 | Each way of failing that proof has its own **named and publicly carriable** | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | BASELINE.SCOPE_* public details |
| 703–713 | An **ambiguous** selection — more than one row citing the registered document — is | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | ambiguous selection / caller assertion |
| 715–718 | The two scope records remain different things throughout: the foundation | N/A | neither | S3-NA-SCOPE-DOCUMENT-V1 | two scope records remain different |
| 720–720 | ### `fact2` payload encoding: one explicit successor law | META | both | — | ### fact2 payload encoding heading |
| 722–727 | The inherited `fact-plane.v1.json` | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION | inherited CBOR vs C settled: fact2 payloads are C |
| 729–738 | **`fact2` payloads are `C`.** There is one product encoder and no second codec in | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-KIT-RELATION-LADDER | fact2 payloads are C; 13 relations; ladder authority |
| 740–752 | **The ladder is an explicit array, and `rungs` is not it (CB3-MUST-1).** That | KIT | kit | S3-KIT-RELATION-LADDER | ladder is explicit array; rungs is not the ladder |
| 754–763 | Each row therefore carries an explicit ordered **`ladder`**, weakest-first, | KIT | kit | S3-KIT-RELATION-LADDER | ladder weakest-first; mirrors drift-checked |
| 765–770 | Membership is decided against `ladder`, always, with **no empty-ladder | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-KIT-RELATION-LADDER | membership against ladder; no empty-ladder fallback |
| 772–782 | **One rung vocabulary, named directly (CB3-MUST-2).** The policy DSL previously | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION | minResolution is rung names; this atom uses none over file@enumerated |
| 784–795 | Preserving the abstract syntax with a published mapping was considered and | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION | abstract Resolution enum withdrawn; satisfaction is ladder-index |
| 797–810 | Two admission conditions follow, because no schema keyword can express the | EXECUTED | both | S3-RULE-PROGRAM-PROJECTION, S3-PROGRAM-PREDICATE | Run closure enforces atom relation/rung on Plan policy and compiled program |
| 812–820 | **What does not change:** historical `FactRecord1` records, their CBOR wire bytes | META | both | — | historical FactRecord1 untouched; not a fact2 preimage |
| 822–826 | Joined at Run closure for every fact: the relation must be registered; | EXECUTED | both | S3-PAYLOAD-REGISTRY-RELATION, S3-UNIVERSE-RULE | joined at Run closure for every fact |
| 828–828 | #### Relation payloads: the digest law, and what a payload's claim is joined to | META | both | — | #### Relation payloads heading |
| 830–836 | The closing digest law above governs identity-schemas.v3, and the native contract | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE, S3-ANCHOR-LAW | relation-payload digest law / snapshotJoins class |
| 838–844 | That document now carries its own `x-opensip-digest-law`, and **every** | KIT | kit | S3-KIT-ANCHOR-LAW-EVERY-RELATION | x-opensip-digest-law on relation document |
| 846–857 | The relation document's annotation law also governs schema structure. A governed | KIT | kit | S3-KIT-ANCHOR-LAW-EVERY-RELATION | governed occurrences of DigestHex/CanonicalPath |
| 859–864 | Every governed occurrence must have an effective annotation. An annotated | KIT | kit | S3-KIT-DIGEST-DOMAINS | every governed occurrence must have annotation |
| 866–871 | There is no precedence rule between disagreeing effective annotations at one | KIT | kit | S3-KIT-DIGEST-DOMAINS | no precedence between disagreeing annotations |
| 873–886 | The current registry's join fields address top-level selector properties. | KIT | kit | S3-KIT-ANCHOR-LAW-EVERY-RELATION | schema-law admission of registered schema coherence |
| 888–894 | `x-opensip-relation-registry` carries a normative per-relation **`snapshotJoins`** | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE, S3-CLONES-BODY-FRAME, S3-ANCHOR-LAW | snapshotJoins table applied to every owning fact |
| 896–901 | / Relation / Join / | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE | snapshotJoins relation table |
| 903–910 | **How many anchors a fact carries is decided per relation, and the inventory | EXECUTED | both | S3-ANCHOR-LAW, S3-KIT-ANCHOR-LAW-EVERY-RELATION | anchorLaw classes inventory/body-identity/source-text |
| 912–916 | / Class / Relations / Anchors / Why / | EXECUTED | both | S3-ANCHOR-LAW | anchorLaw class table |
| 918–921 | Zero is also the only cardinality *every* inventoried path can satisfy: a path | EXECUTED | both | S3-ANCHOR-LAW | zero is only cardinality every inventoried path can satisfy |
| 923–933 | **The raw-byte boundary.** An inventory claim retains its path, content digest | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE, S3-ANCHOR-LAW | raw-byte boundary: inventory hashes/measures without decoding |
| 935–948 | **Where a location comes from, now that inventory facts carry no anchors.** | EXECUTED | both | S3-ANCHOR-LAW | finding location not via inventory anchors |
| 950–955 | `vcs-change.previousPath` is the one declared exemption. A pre-rename path names | N/A | neither | — | vcs-change.previousPath exemption; no vcs-change fact |
| 957–959 | An inventory row is a claim *about* bytes; retention is custody *of* them. A | EXECUTED | both | S3-SNAPSHOT-JOINS-FILE | inventory row vs retention of bytes |
| 961–961 | #### `clones`: the inherited body recipe, reused and not restated | META | both | — | #### clones heading |
| 963–968 | `bodyIdentity` and `normalisationVersion` are pinned by | EXECUTED | both | S3-CLONES-BODY-FRAME | clones body recipe pinned to fact-identity-policy.v2 |
| 970–1009 | - `normalisationVersion` is the raw SHA-256 of the **exact retained canonical | EXECUTED | both | S3-CLONES-BODY-FRAME | normalisationVersion = SHA-256 of retained level-spec bytes |
| 1011–1024 | `body-language-version` is defined in identity-schemas.v3 and its retention is | EXECUTED | both | S3-UNIVERSE-BIND-CONTEXT, S3-CLONES-BODY-FRAME | BLV derived from retained syntax native context grammar interpreter |
| 1026–1030 | Dialect is **body specific**, per language, closed, and always **selected** — | EXECUTED | both | S3-CLONES-BODY-FRAME | dialect body-specific, selected, no null branch |
| 1032–1045 | - **Rust**: the **effective** edition of the **selected** compilation **target** | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | Rust edition from SourceUnitOwnershipV1 — this graph is syntax-only |
| 1047–1059 | **The same physical source path compiled by two targets at two editions has a | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | two targets two editions |
| 1061–1063 | Paths, crate names, unit ids and the selection itself **establish** these | EXECUTED | both | S3-CLONES-BODY-FRAME | paths establish selection then do not enter BLV |
| 1065–1080 | **Selected scope and incomplete enumeration are different claims**, and the | N/A | neither | S3-NA-NESTED-RUST-IDENTITIES | partial enumeration vs selection for Rust clones dialect |
| 1082–1091 | The body's `languageId` comes from the **same selector over the same anchor**, | EXECUTED | both | S3-CLONES-BODY-FRAME | languageId is language of the BODY |
| 1093–1108 | Spelled exactly, so the relation registry, the domain registry and this section | EXECUTED | both | S3-CLONES-BODY-FRAME | languageId from dialect suffix table / bodyLanguageLaw; never universe engine fi |
| 1110–1123 | Two bodies sharing a `bodyIdentity` is evidence that their **normalized bodies | EXECUTED | both | S3-CLONES-BODY-FRAME | shared bodyIdentity is normalized-body agreement not semantic equivalence |
| 1125–1131 | The split is honest and stated rather than blurred. At `L0-verbatim` the | EXECUTED | both | S3-CLONES-BODY-FRAME | L0 recomputed from anchor; L1+ custody/framing not tokenisation judgment |
| 1133–1136 | **FACT-ID-V1 and `bodyIdentity` are never equated.** The fact identity wraps the | EXECUTED | both | S3-H-RECIPE-PROOF, S3-CLONES-BODY-FRAME | FACT-ID-V1 and bodyIdentity never equated |
| 1138–1141 | Native contexts and native semantic universes are `h-identity` under the native | EXECUTED | both | S3-H-FRAME-NATIVE-CONTEXT | native contexts/universes h-identity; no silent representation swap |
| 1143–1144 | Five records this graph digests are defined here because nothing else defines | EXECUTED | both | S3-PROGRAM-PREDICATE | program-predicate record; addressing p / p.i |
| 1146–1165 | `program-predicate` is the record digested by | EXECUTED | both | S3-PROGRAM-PREDICATE | program-predicate record body |
| 1167–1171 | `finding-parameters` is the record digested by `finding.parameterDigest`: | EXECUTED | tamper | S3-FINDING-CITE-WITNESS | finding-parameters; positive has no findings |
| 1173–1186 | `stage-spec` is the record digested by `stageSpecDigest`: | EXECUTED | both | S3-STAGE-SPEC-PARAMS, S3-STAGE-OUTPUT-DOMAINS-REGISTERED | stage-spec record |
| 1188–1207 | `stage-spec.operation` is owned by the selected producer closure's semantic | EXECUTED | both | S3-STAGE-SPEC-PARAMS | stage-spec.operation owned by producer interface |
| 1209–1219 | Both `outputDomains` arrays use the existing domain vocabulary in | EXECUTED | both | S3-STAGE-OUTPUT-DOMAINS-REGISTERED | outputDomains registered byDomain; empty permitted |
| 1221–1229 | `plan.semanticClosures` records the Plan's explicit selection, with a required | EXECUTED | both | S3-GRAMMAR-TREE | plan.semanticClosures; view producer; evaluator equalToDirect (via admit_full_pi |
| 1231–1238 | An import's producer and adapter are retained through the selected `import2` | EXECUTED | both | S3-GRAMMAR-TREE, S3-NA-TS-RUST-TOOLCHAIN | grammar closures via native context; need not flatten into semanticClosures |
| 1240–1244 | `commit-inventory` is the record digested by `commit-receipt.inventoryDigest`: | N/A | neither | — | commit-inventory / commit-receipt operational |
| 1246–1252 | `owner-source-set` is the record digested by | N/A | neither | — | owner-source-set RepoExecutionGrantV2 |
| 1254–1258 | Waiver resolution selects the active admitted waiver set before pure evaluation | EXECUTED | both | S3-RULE-PROGRAM-PROJECTION | waiver resolution historical sealed set; this graph waivedFindingIds=[] |
| 1260–1290 | The complete closure includes bytes for each policy, waiver, rule program, | EXECUTED | both | S3-C-REMAINDER-CONFIG, S3-H-FRAME-NATIVE-CONTEXT, S3-PAYLOAD-REGISTRY-RELATION, S3-ANCHOR-LAW, S3-BUDGET-EQUAL, S3-GRAMMAR-TREE | complete preimage retention; budget equality; anchorLaw; Plan/source agreement |
| 1292–1304 | **Coverage scopes partition, and the two halves of that word have different | EXECUTED | both | S3-COVERAGE-PARTITION | Coverage scopes partition disjointness |
| 1306–1313 | Three boundaries of that rule matter and are held by controls. It is **per view**: | EXECUTED | both | S3-COVERAGE-PARTITION | per view; includes scopes with no Coverage |
| 1315–1321 | Fact totality and the population available for evaluation are separate | EXECUTED | both | S3-COVERAGE-TOTALITY-FILE | file@enumerated totality only |
| 1323–1335 | Evaluator3 additionally requires the independently selected subject census in | EXECUTED | both | S3-COVERAGE-TOTALITY-FILE, S3-EXPECTED-PROOF-NO-CLAIMED-FIELDS | enumeration contract subject census; execution-inputs cells |
| 1337–1348 | This does **not** make `complete` vacuous where no totality row exists. It remains | EXECUTED | both | S3-COVERAGE-TOTALITY-FILE, S3-COVERAGE-PARTITION | complete is examined-partition claim; RC-0/1/2 not vacuous |

Machine-readable operands: `normative-law-audit.json`.
