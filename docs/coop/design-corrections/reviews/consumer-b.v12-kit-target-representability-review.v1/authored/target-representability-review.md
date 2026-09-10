# Target representability independent architecture review

Same P4 original kit-only reviewer origin. Bounded follow-through on this origin's query-attribution-review.v1 COMPLETE13 conclusion about distinct namespaced file targets vs file/package inventory identity. Functional representability of advertised first-party FILE/PACKAGE target filtering, incoming analysis/absence, and graph navigation. Not whole-consumer ACCEPT. Not query execution. Not graph remint.

**Verdict:** genuine architectural gap for advertised first-party FILE and PACKAGE import TARGET occupancy on ordinary identities. First-party SYMBOL targets remain representable. occupancy=external remains lawful for a distinct namespaced vertex. That last fact is not a substitute for first-party file/package target representability.

Query interpretation of the authorized TS store remains **diagnostic / not acceptance** (prior scoped MUST `ts.compilerPackageDigest-is-toolchain-tree-member`). Reasoning examples below are **not Run admission**.

## Custody

- new-inputs manifest `7ca1f3c9e8a68acecf23584998a90bd04ebac4c97f1310a6f076bb29c830003d` match=True
- `query-run-completion-review.md` `5aad9ebbfd9776e197a729b07da1ae83d98a544b452ddf0b20d9aca014b08d2b` match=True
- `query-run-completion-review.json` `59bcab77c5d10b57445bc00d17c8f3e11d0df9a912d8bb2ffd253a71b5b90dfe` match=True
- `query-run-graph-inventory.json` `6b525741231b3258c9e36b40241e803dc28d07223c619197aee5bc2a6b07635c` match=True
- `runs/ts.store.json` `59b7d384f886899083d356a4db41cec3a5cd87b3584027ec3e71cc0adddce062` match=True
- kit `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` match=True
- requirements `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` match=True
- charter `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` match=True
- prior query-attribution-review.md `65a15c505c2162552531b09e1c24f5a0233f90320cd87b4492bf3fdbdbc6d3ba` match=True
- prior query-attribution-review.json `6633c11f204c7792f7c62f449fd77dc860415abdd6701de49fe88d5d27ddba38` match=True
- this store `59b7d384f886899083d356a4db41cec3a5cd87b3584027ec3e71cc0adddce062`

Command: `/tmp/opensip-architecture-review-env/bin/python -I -B /private/tmp/opensip-design-corrections/consumer-b.v12-kit-target-representability-review.v1/output/independent/target_representability_review.py`

Author helpers, root checkers, expected values, reference implementations, fixtures, and goldens were not read.

## Advertised-surface proof

This is not a newly invented product requirement. The following current owners already advertise first-party FILE and PACKAGE as import targets of incoming analysis and as graph target kinds.

- Incorporated: identity-and-evidence.md §4 incorporates atom-evaluation-contract.v1.md as constituent intended-design semantics. Plan commits PolicyDocumentV2.
- Endpoint applicability: `foundation/evaluator-projection-registry.v1.json#/kindApplicability/endpointTarget` — Uses relation.targetKinds, NOT sourceSubjectKind. Rule kind file|symbol|package must be a member of targetKinds.
- Policy: workflows/schemas/policy-document.v2.schema.json Atom.endpoint enum source|target (default source) and subjectEnumeration.subjectKind file|symbol|export|package. policy-document.schema.json v1 Atom has no endpoint field. PolicyDocumentV2 is the committed profile. AtomSuccessorV1 describes the same endpoint extension.
- Imports: `evaluator-projection-registry.v1.json#/relations/imports` targetKinds=['file', 'symbol', 'package'], endpointTarget=admitted-at-rung at ['resolved-target']. endpoint=target admission uses TARGET kinds {file,symbol,package}, not source subjectKind symbol.
- Other binary native targetKinds: calls=['symbol'], references=['symbol'], control-flow=['symbol'], reachability=['symbol'].
- Unary relations: forbidden / ATOM_ENDPOINT_UNAVAILABLE.
- Query: `workflows/query-projection-contract.v3.md §3` — resolved-target; target kinds file, symbol, package; target kind from admitted TargetAttributionV1.
- Incoming bind: `evaluator-projection-registry.v1.json#/owedPartitions/incoming/bind` — current E=(U,K,N) occupies the target native-id field after native-id compare; fact.targetUniverse must equal U for a MATCH.
- Enumeration: `evaluator-composition-contract.v3.md §2` — Enabled rules select every admitted program of the required primary subject kind. Include/exclude apply to logical path, never opaque native IDs.

The current design advertises first-party FILE and PACKAGE inventory subjects as lawful current evaluation subjects for imports@resolved-target endpoint=target, and advertises graph navigation to file/package import targets. It does not advertise file/package as calls/references/control-flow/reachability targets.

File and package as SOURCE of unary inventory relations are a different advertised surface (endpointTarget forbidden) and remain representable. Outgoing `targetKind=file` filters on a symbol source are also a different surface (attribution.kind, not file-inventory occupancy).

## Constraint map

### Required

- **R1** (`subject-inventory.schema.v1.json InventoryRowV1.path / enumeration-contract.v1.md`): File nativeSubjectId is the snapshot LogicalPath (equals path; qualifiedName equals path).
- **R2** (`enumeration-contract.v1.md / subject-inventory package rows`): Package nativeSubjectId is the attested packageName (equals qualifiedName). Identity is (universe, package, packageName, packageManifestPath=row.path).
- **R3** (`subject-inventory.schema.v1.json symbol nativeSubjectId`): Symbol nativeSubjectId is owner SubjectIdV1.
- **R4** (`relation-payload-schemas.v2.json#/$defs/ImportsPayloadV1`): importer and resolvedTarget are SubjectIdV1. specifier is CanonicalText, not a native id.
- **R5** (`target-attribution.schema.v1.json x-opensip-join-law.joins`): targetNativeId equals the payload field named by relations[fact.relation].targetNativeIdField at fact.resolution (imports: resolvedTarget).
- **R6** (`target-attribution occupancy / derivation.never`): occupancy=first-party iff targetNativeId is a first-party inventory subject of targetUniverse (exact native id). Never parse SubjectIdV1 spelling to invent kind or occupancy. Never invent first-party packageManifestPath from logicalPath.
- **R7** (`atom-evaluation-contract.v1.md §2`): Native-id compare is first: payload target field != N => known nonmatch even if kind unknown.
- **R8** (`owedPartitions.incoming.matchingFacts`): matchingFacts are facts whose actual targetUniverse=U and target nativeId=N (and kind reconciled).
- **R9** (`owedPartitions.incoming.attestation / incoming-search.schema.v1.json`): If no CoverageResultV3 with key.targetUniverse=U, incoming none/count-at-most-true/all-covered MUST NOT infer that S searched U. Require IncomingSearchV1 or source-target-search-unattested. Attestation is not inferred from producer facts. examinedExhaustive=false never proves complete search.
- **R10** (`query-projection-contract.v3.md §0 and §2–3`): Zero neighbor rows is not no callers. Endpoint tuple is (universe, kind, nativeSubjectId, packageManifestPath or empty). Projected imports target nativeSubjectId is payload.resolvedTarget; no invented or stripped namespaces.
- **R11** (`atom-evaluation-contract.v1.md §4`): Wrong subject.kind for the relation/endpoint is ATOM_KIND_INCOMPATIBLE, never vacuous none.
- **R12** (`target-attribution first-party package`): occupancy=first-party and kind=package requires non-null packageManifestPath exact-matching inventory (packageName=targetNativeId, path=packageManifestPath). Ambiguity stays occupancy unknown.

### Permitted

- occupancy external|unknown when ephemeral first-party identity set is empty
- external resolved targets that are not first-party inventory remain lawful query vertices
- logicalPath non-null only when occupancy is external or unknown; MUST be null on first-party
- targetKind FieldFilter on attribution.kind for imports@resolved-target
- outgoing known-hit on a first-party symbol importer whose payload.importer equals symbol inventory nativeSubjectId

### Ordinary grammars used in cases (independently chosen)

These names were not chosen to intersect SubjectIdV1 with LogicalPath or packageName.

| name | value | SubjectIdV1 | LogicalPath | CanonicalText |
|---|---|---|---|---|
| ordinary file path | `src/lib/util.ts` | False | True | True |
| ordinary package name | `demo-app` | False | True | True |
| ordinary manifest path | `package.json` | False | True | True |
| ordinary symbol id | `module:src/lib/util.ts` | True | True | True |
| namespaced file SubjectIdV1 | `file:src/lib/util.ts` | True | True | True |
| namespaced package SubjectIdV1 | `package:demo-app` | True | True | True |
| colon path (excluded from ordinary cases) | `file:src/lib/util.ts` | True | True | True |

Unsatisfiable set for ordinary first-party FILE import target occupancy:
- R1 file inventory nativeSubjectId is ordinary LogicalPath src/lib/util.ts
- R4 resolvedTarget is SubjectIdV1
- R5 targetNativeId equals resolvedTarget
- R6 occupancy=first-party requires targetNativeId exact inventory native id
- R7 native-id compare is first and does not parse namespaces

Replace occupancy=first-party with occupancy=external (or unknown). Constraints hold. The evaluation subject and the projected target remain distinct tuples.

## Discriminating cases

All cases are kit-derived reasoning examples, **not replacement graph admission** and not `evaluate_atom` / `execute_graph_query` execution.

### C1-ordinary-first-party-file-import-target

- Advertised combination: **True**
- Classification: **architectural-gap**
- Surface: PolicyDocumentV2 rule subjectEnumeration.subjectKind=file, Atom.endpoint=target, relation=imports, minResolution=resolved-target. Registry relations.imports.targetKinds includes file; kindApplicability.endpointTarget requires the rule kind to be a member of targetKinds.
- Reason: The combination is advertised and admitted (not ATOM_KIND_INCOMPATIBLE). Ordinary first-party file N cannot equal SubjectIdV1 resolvedTarget without parsing. Known-hit on that exact inventory subject is unreachable. External occupancy is a different subject.
- Provider can lawfully represent a known positive to that exact first-party evaluation subject: **False**
- How the host preserves the relationship: As occupancy=external (or unknown) projected query vertex (U, file, file:src/lib/util.ts). Not as the first-party evaluation subject (U, file, src/lib/util.ts). logicalPath is not a native-id compare field and MUST be null on first-party occupancy.

### C2-ordinary-first-party-package-import-target

- Advertised combination: **True**
- Classification: **architectural-gap**
- Surface: subjectEnumeration.subjectKind=package, Atom.endpoint=target, imports@resolved-target. Registry imports.targetKinds includes package. First-party package occupancy additionally requires non-null packageManifestPath exact-matching inventory (packageName, path).
- Reason: Package is an advertised imports target kind and a first-party evaluation-subject kind, but ordinary packageName is not SubjectIdV1. Native-id compare cannot occupy the inventory package subject.
- Provider can lawfully represent a known positive to that exact first-party evaluation subject: **False**
- How the host preserves the relationship: As occupancy=external/unknown projected imports target whose nativeSubjectId is the SubjectIdV1 payload, not (package, demo-app, package.json).

### C3-ordinary-first-party-symbol-import-or-calls-target

- Advertised combination: **True**
- Classification: **representable**
- Surface: subjectEnumeration.subjectKind=symbol|export, endpoint=target, imports@resolved-target or calls@resolved-callee or references@resolved-binding or control-flow/reachability. Symbol inventory nativeSubjectId is SubjectIdV1; payload target fields are SubjectIdV1.
- Reason: Symbol is the identity kind whose inventory grammar is already SubjectIdV1. This is the lawful positive first-party TARGET example. It does not substitute for advertised file/package target occupancy.
- Provider can lawfully represent a known positive to that exact first-party evaluation subject: **True**
- How the host preserves the relationship: Payload native id, inventory nativeSubjectId, targetNativeId, evaluation-subject N, and query tuple nativeSubjectId are the same SubjectIdV1. Host ephemeral first-party projection size=1. Query and incoming occupy the same vertex.

### C4-external-file-import-target

- Advertised combination: **True**
- Classification: **representable**
- Surface: Query vertex domain includes projected-fact endpoints that are not first-party inventory. occupancy=external is consistent when ephemeral size=0.
- Reason: External occupancy plus projected query vertex is the jointly satisfiable authoring already established. It does not represent a known-hit on a first-party file/package evaluation subject.
- Provider can lawfully represent a known positive to that exact first-party evaluation subject: **False**
- How the host preserves the relationship: Query vertex (U, file, file:node_modules/left-pad/index.js). Not an inventory subject. First-party occupancy would refuse.

### C5-first-party-file-as-source-not-target

- Advertised combination: **True**
- Classification: **representable**
- Surface: relations.file / vcs-change / clones: sourceField is path (LogicalPath / CanonicalPath). endpointTarget=forbidden.
- Reason: First-party FILE SOURCE occupancy is representable. Unary file/package relations do not advertise endpoint=target.

### C6-first-party-package-as-source-not-target

- Advertised combination: **True**
- Classification: **representable**
- Surface: relations.package sourceOccupancy: payload.packageName AND payload.manifestPath must equal evaluation-subject nativeSubjectId and packageManifestPath. endpointTarget=forbidden.
- Reason: First-party PACKAGE SOURCE occupancy is representable. The package relation is not a target endpoint.

### C7-file-endpoint-target-on-calls

- Advertised combination: **False**
- Classification: **explicitlyunsupported**
- Surface: calls.targetKinds={symbol}. kindApplicability.endpointTarget: rule kind must be a member of targetKinds. Wrong kind is ATOM_KIND_INCOMPATIBLE, never vacuous none.
- Reason: File is not an advertised calls target kind. This is not the imports file-target gap.
- Exact refusal: `ATOM_KIND_INCOMPATIBLE`

### C8-imports-syntactic-specifier-endpoint-target

- Advertised combination: **False**
- Classification: **explicitlyunsupported**
- Surface: imports.endpointTargetRungs=[resolved-target]. specifier is not a native id. Query table: imports@syntactic-specifier is not graph-projectable.
- Reason: Deliberate rung unavailability, not identity inequality.
- Exact refusal: `ATOM_ENDPOINT_UNAVAILABLE (atom) / QUERY.RELATION_UNSUPPORTED (graph request)`

### C9-unary-file-or-package-endpoint-target

- Advertised combination: **False**
- Classification: **explicitlyunsupported**
- Surface: file/package/declares/literal/types/clones/vcs-change/unresolved-edge: targetKinds=[], endpointTarget=forbidden.
- Reason: Unary relations do not advertise target occupancy.
- Exact refusal: `ATOM_ENDPOINT_UNAVAILABLE`

### C10-first-party-occupancy-on-namespaced-file-native-id

- Advertised combination: **True**
- Classification: **explicitlyunsupported**
- Surface: Join law sizeZero: sidecar occupancy=first-party while no exact inventory identity refuses TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY.
- Reason: This is an explicit join refusal of first-party occupancy, not unknown and not a silent match. It does not withdraw the advertised file target kind.
- Exact refusal: `TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`

### C11-first-party-occupancy-forcing-inventory-spelling-into-targetNativeId

- Advertised combination: **True**
- Classification: **explicitlyunsupported**
- Surface: targetNativeId MUST equal the payload field named by relations[fact.relation].targetNativeIdField. Mismatch refuses TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH. ImportsPayloadV1.resolvedTarget is SubjectIdV1, so ordinary LogicalPath is not a lawful payload value either.
- Reason: Cannot sneak the inventory spelling into targetNativeId while the payload remains namespaced, and cannot lawfully write the inventory spelling as resolvedTarget.
- Exact refusal: `TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH (and payload.resolvedTarget=src/lib/util.ts would fail SubjectIdV1 schema)`

### C12-query-neighbors-at-unequal-file-identities

- Advertised combination: **True**
- Classification: **representable**
- Surface: query-projection-contract.v3.md §0 zero neighbor rows is not no callers; §2 vertex domain is inventory rows UNION projected endpoints; no namespace stripping.
- Reason: Query preserves the edge at the namespaced file vertex and admits the inventory file as an isolated vertex. Empty neighbors is not an absence claim. This guard is query-only.

### C13-incoming-none-without-coverage-S-to-U

- Advertised combination: **True**
- Classification: **unknown**
- Surface: owedPartitions.incoming.attestation and atom contract Search of U: if no CoverageResultV3 with key.targetUniverse=U, incoming none/count-at-most-true/all-covered MUST NOT infer that S searched U. Require IncomingSearchV1 or report source-target-search-unattested.
- Reason: This is the normative guard that prevents converting unattested search into proven absence. It does not fire when complete Coverage S→U exists.

### C14-incoming-none-with-complete-search-and-unequal-native-ids

- Advertised combination: **True**
- Classification: **architectural-gap**
- Surface: matchingFacts require target nativeId=N after native-id compare. Different targetNativeId is known nomatch even if kind/occupancy unknown. Complete Coverage S→U (or admitted complete IncomingSearchV1) plus sufficiency_v2 universal-negative at resolved rungs can make incoming none true.
- Reason: Known incoming evidence exists at a distinct namespaced file identity. The advertised first-party file evaluation subject sees known nomatch. Complete search of U is about universes, not about equating those identities. Query §0 does not apply to atom none.
- False-result class: **proved-construction** — not a potential-risk-only claim and not an unreachable input
- Construction: `{"E": {"universe": "0000000000000000000000000000000000000000000000000000000000000000", "kind": "file", "nativeSubjectId": "src/lib/util.ts", "packageManifestPath": ""}, "fact.targetNativeId": "file:src/lib/util.ts", "nativeIdEqual": false, "matchingFacts": [], "coverage": "complete at (imports, resolved-target, S=U, T=U)", "sufficiency_v2": "universal-negative success stipulated as a lawful reachable provider emission", "incomingNone": true}`

### C15-specially-chosen-colon-path-excluded

- Advertised combination: **False**
- Classification: **unreachable-as-ordinary-input**
- Surface: LogicalPath grammar permits a colon in a segment, so file:src/lib/util.ts can be both LogicalPath and SubjectIdV1. This review forbids using such a name as an ordinary first-party example.
- Reason: Satisfiability via grammar intersection is not ordinary first-party file identity and is not a substitute for a general representability proof.

### C16-outgoing-targetKind-file-filter-on-symbol-source

- Advertised combination: **True**
- Classification: **representable**
- Surface: FieldFilter targetKind on imports@resolved-target projects targetAttribution.kind. Current subject is the SOURCE importer (symbol inventory). endpoint defaults to source.
- Reason: Outgoing targetKind filtering does not require the current subject to be a file inventory row. It is not first-party FILE target occupancy.

### C17-occupancy-unknown-is-not-false-when-native-ids-match

- Advertised combination: **True**
- Classification: **unknown**
- Surface: Join law absence: no sidecar and no unique first-party identity => kind/occupancy unknown, not nomatch, not false. This clause applies after native-id compare already matched.
- Reason: Guards unknown occupancy from becoming false. It never runs for ordinary file/package import targets because native-id compare already failed.

## Authorized TS store diagnostic (not admission)

Standing: diagnostic observation of already-authorized TS store bytes; not whole-Run admission. run `run3:8170fc2c58c49759e89b3994ba92cf2d59f27a7721ac88698985628e2d2057db` universe `2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8`.

- File inventory nativeSubjectId values: ['src/index.ts']
- Package inventory rows: `[{"kind": "package", "nativeSubjectId": "app", "path": "package.json", "qualifiedName": "app"}]`
- Projected imports@resolved-target facts:
  - `fact2:a5570c5ea598e6292b20fec608e160a06b29c1dc4ac052ee21922b929b0fa6bd` module:src/index.ts → file:node_modules/left-pad/index.js kind=file occupancy=external targetNativeId=file:node_modules/left-pad/index.js logicalPath=node_modules/left-pad/index.js
  - `fact2:ddc3eeb902d147e7bdacb0b09d0b745b9f0998def6b70df21e15e7ebb63e3cf8` module:src/app.ts → file:src/index.ts kind=file occupancy=external targetNativeId=file:src/index.ts logicalPath=src/index.ts
- Native-id equalities vs inventory: `[{"resolvedTarget": "file:node_modules/left-pad/index.js", "equalsAnyFileInventoryNativeId": false, "equalsAnyPackageNativeId": false}, {"resolvedTarget": "file:src/index.ts", "equalsAnyFileInventoryNativeId": false, "equalsAnyPackageNativeId": false}]`
- Imports Coverage records: `[{"id": "coverage2:5d75f2485651e70b4a71c3f362084220b7c152b71f9e626618b8166c01777a4e", "coverage": "complete", "examinedExhaustive": true, "key": {"relation": "imports", "resolution": "resolved-target", "sourceUniverse": "2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8", "subjectScopeCommitment": "sha256:cc4b83a92efa6d06c73f65016d3137768b57473456390c4620aa0e02de64a261", "targetUniverse": "2c475675b3b873ebf07ff153339460c55ab8770f266cf8f8f9f0bc0a19de89a8"}, "closedWorldKeys": ["deadCodeRepairEligible", "dynamicDispatch", "entryPointsRecognized", "exportsClosed", "externalConsumers", "nonliteralLoading", "reasons"], "resolutionCompletenessState": "complete"}]`

Observed: every projected file target native id is a SubjectIdV1 (`file:src/index.ts`, `file:node_modules/left-pad/index.js`) and none equals file inventory `src/index.ts` or package inventory `app`. One attributed fact has occupancy=external and logicalPath=`src/index.ts`. Native-id compare against the first-party file evaluation subject is known nonmatch. Query neighbors at `(file, src/index.ts)` are empty; neighbors at `(file, file:src/index.ts)` contain the attributed fact (prior tuple-law observation, not re-executed here as a query). Coverage of imports@resolved-target is `complete` with sourceUniverse=targetUniverse=this U and resolutionCompleteness.state complete, so the C13 unattested-search guard does **not** fire on this retained Coverage key. sufficiency_v2 closed-world polarity is not independently replayed here; C14 therefore uses a stipulated lawful complete sufficiency as a reachable construction, and treats this store as a live illustration of the native-id miss plus a represented S→U Coverage key, not as a verified none=true replay of this Run.

## False absence versus guards

| Situation | Result | Class |
|---|---|---|
| Query empty neighbors at inventory file | not “no callers” (query §0) | guarded; not absence |
| Incoming none without Coverage S→U and without IncomingSearchV1 | `source-target-search-unattested` / unknown | guarded |
| Occupancy unknown after a native-id **match** | unknown, not false | guarded; unreachable for ordinary file/package import targets |
| Wrong kind for endpoint (file target of calls) | ATOM_KIND_INCOMPATIBLE | explicit unsupported; never vacuous none |
| occupancy=first-party on namespaced id not in inventory | TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY | explicit join refusal |
| Complete Coverage S→U + sufficiency_v2 universal-negative + native-id inequality on advertised first-party file/package E | incoming none=true while a namespaced-id fact exists | **proved construction**, not merely a potential risk, not an unreachable input |

Absence of representation at the inventory subject cannot silently become proven absence in query. It **can** become incoming none=true in atom evaluation once search of U is represented as complete, because matchingFacts use exact native-id equality and the namespaced fact is a known nomatch, not uncertain evidence.

## Reconsideration of prior “not a gap”

- Prior: query-attribution-review G1: existing-law identity inequality; not a missing/contradictory law because occupancy=external is jointly satisfiable; first-party occupancy on namespaced file SubjectIdV1 is the unsatisfiable set if first-party is demanded
- Retained: Still not a pairwise schema contradiction. External occupancy remains lawful. That statement is not withdrawn.
- Insufficient for: Advertised first-party FILE and PACKAGE target filtering, incoming analysis/absence, and graph identity of inventory subjects.
- Revised: **genuine architectural gap for advertised first-party FILE and PACKAGE import TARGET occupancy on ordinary identities**
- Not a newly invented product requirement: registry targetKinds, kindApplicability.endpointTarget, PolicyDocumentV2 endpoint, composition subject-kind enumeration, query table, and incoming bind already advertise the combination
- C7–C9/C10–C11 are explicit refusals. C1/C2/C14 are advertised combinations whose known-hit is unreachable and whose incoming none can be true under complete search.

## Smallest coherent design-level correction options

Design-level options only. No kit edit, no graph remint, no claimed implemented fix.

Atom matchingFacts / native-id compare must occupy the same native string as the first-party evaluation subject N. Changing occupancy metadata alone (logicalPath, sidecar occupancy) cannot create a known-hit while R7 compares payload SubjectIdV1 to inventory LogicalPath/packageName.

### O1-withdraw-file-package-from-imports-target-kinds

imports.targetKinds becomes {symbol} for first-party evaluation; file/package subjectEnumeration + endpoint=target becomes ATOM_KIND_INCOMPATIBLE. Query may still project occupancy=external file/package vertices as non-inventory endpoints, or the query table may drop those target kinds in the same revision.

Compatibility: Policy rules that enumerate file/package incoming imports start refusing. Existing external occupancy graphs remain lawful. Smallest if product intent is symbol-only first-party import targets.

### O2-file-package-inventory-native-id-becomes-attested-SubjectIdV1

File/package inventory keep path/manifestPath as LogicalPath and attest nativeSubjectId as SubjectIdV1 independently (no parse of path). Evaluation subject N and query inventory vertices use that SubjectIdV1. Payload already uses SubjectIdV1.

Compatibility: Remints every file/package evaluation-subject, inventory native id, and query inventory vertex. Fingerprints still use path. Breaking for consumers that treated LogicalPath as file nativeSubjectId.

### O3-kind-discriminated-payload-target-native-id

When attribution.kind=file, the native-id field used for matching is LogicalPath (inventory spelling); when kind=package, packageName plus packageManifestPath; when kind=symbol, SubjectIdV1. Requires payload and/or targetNativeIdField law change.

Compatibility: Remints imports facts and collapses today's two file vertices (src/lib/util.ts vs file:src/lib/util.ts) into one. Existing namespaced query vertices disappear.

### O4-kind-discriminated-compare-using-typed-sidecar-fields-not-namespace-parse

Keep payload SubjectIdV1. For kind=file, matchingFacts compare E.nativeSubjectId to a typed LogicalPath sidecar field that is allowed on first-party occupancy; for kind=package, compare (packageName, packageManifestPath). This is a new compare law, not a parse of namespace:opaque.

Compatibility: Requires reversing logicalPath MUST be null on first-party occupancy and reversing native-id-compare-is-first against payload. Existing external graphs would need a published migration for which vertex is the first-party subject.

Not current law (must not be treated as already published):
- Parsing file: off SubjectIdV1
- Inventing alias records that equate (file, src/lib/util.ts) with (file, file:src/lib/util.ts)
- Treating logicalPath as occupancy identity under current join law
- Treating empty query neighbors as no callers
- Treating unattested incoming search as none=true

No accepted candidate bytes were edited or replaced. No implemented fix is claimed.

## Limitations

- Not whole-Run close_run admission of the authorized TS store. Prior scoped identity-closure observation compilerPackageDigest-is-toolchain-tree-member remains. Query/atom interpretation of that store is diagnostic/not acceptance.
- Not execution of graph.neighbors/path/reach or evaluate_atom. Cases are kit-derived reasoning examples labeled not Run admission.
- Not a claim that occupancy=external is unsatisfiable. That authoring remains lawful for external vertices.
- Closed-world/sufficiency_v2 on the retained TS coverage entry is observed at Coverage key, coverage=complete, resolutionCompleteness.state, and examinedExhaustive when present on that record. C14's none=true construction stipulates lawful complete sufficiency as a reachable provider emission, not as a verified sufficiency_v2 replay of this store.
- policy-document.schema.json v1 Atom lacks endpoint; the committed profile is PolicyDocumentV2. If a consumer presented only v1 atoms, endpoint would default to source and file incoming imports would not be expressible in that older schema. That is a schema-generation standing note, not withdrawal of registry/atom/query advertisement.
- No reference implementation, fixtures, goldens, root reports, or other origins were read.
- No normative kit bytes or graph bytes were edited.

No normative design edit. No graph remint.
