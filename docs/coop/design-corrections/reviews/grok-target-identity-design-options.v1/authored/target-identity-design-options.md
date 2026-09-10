# Target identity design options — coauthor draft proposal

Standing: actual Grok design-coauthor draft for Codex alignment. Not independent
final review. Not acceptance. Not implementation readiness. Not a live
normative edit of source24. No product implementation, git commit/push,
historical-evidence rewrite, or graph remint is authorized by this document.

This turn chooses a coherent successor design and writes a concrete draft
proposal so Codex can align and later author reference corrections. It does
not implement those corrections.

## 1. Custody and source

Input manifest SHA-256 `1fd136a131abd5f1b72348e19df831fec38f1c5cc083f26cc9d18908c1968388` verified over:

| path | sha256 | bytes |
|---|---|---|
| `inputs/root-assessment.md` | `f0e04ef4bd3dc13729ec4526433b245cf595708ebbe08d5797f8f0d97338fcea` | 1310 |
| `inputs/target-representability-review.json` | `3cc3aff198335bcc805e34b6066e8779748a771665c1f651db527a4576511f2f` | 40429 |
| `inputs/target-representability-review.md` | `580e5879243a089163f239ab4984d1ab30eb7ee94e32b7a743d8bd99ebeaa168` | 30141 |

Readonly historical source: `/tmp/opensip-design-corrections/candidate-subject.v24`.
Declared current source manifest SHA-256
`a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb`.
This session did not locate that manifest file inside source24; it verified
the evaluator3 pin inventory
`docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json`
(`79f5ce3cb14d99517263563af5bcb140c73fa4608dfadeeff1b78d3a742dd316`, 1220
files) against the exact owner bytes used below. Those owner bytes matched
their declared pins. Source24 was not mutated.

Owner bytes independently read as coauthor (normative design/schema and
reference code/tests only; no other-session helpers):

- `foundation/target-attribution.schema.v1.json`
- `foundation/subject-inventory.schema.v1.json`
- `foundation/relation-payload-schemas.v2.json`
- `foundation/atom-evaluation-contract.v1.md`
- `foundation/atom_model.v1.py`
- `foundation/check-atoms.v1.py`
- `foundation/evaluator-projection-registry.v1.json`
- `foundation/enumeration-contract.v1.md`
- `foundation/execution-inputs-contract.v1.md`
- `foundation/execution-inputs.schema.v1.json`
- `foundation/incoming-search.schema.v1.json`
- `foundation/identity-schemas.v3.json`
- `foundation/evaluator-composition-contract.v3.md`
- `foundation/shared-profile-decisions.v1.md`
- `workflows/query-projection-contract.v3.md`
- `workflows/query_projection_model.v3.py`
- `workflows/schemas/policy-document.v2.schema.json`
- `docs/v2/contracts/product-v1/identity-and-evidence.md`
- `docs/v2/contracts/product-v1/native-evidence.md` (evaluator3 consumption of target-attribution)
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (profile dispatch)

## 2. Agreed gap, and the limits that survive into the correction

Root and P4 agree: advertised ordinary first-party FILE and PACKAGE import
target occupancy is a genuine existing design gap. Ordinary inventory
identities are path / packageName. `ImportsPayloadV1.resolvedTarget` is
`SubjectIdV1`. Mandatory native-id-first equality cannot occupy those
inventory subjects. External occupancy satisfiability is jointly lawful and
is not functional adequacy for advertised first-party incoming analysis,
target filters, or graph navigation of inventory subjects.

Preserved limits:

1. P4 C14 `incomingNone=true` is a **stipulated** lawful complete-sufficiency
   construction. It is **not** an executed `evaluate_atom` / `close_run`
   fully admitted false-result proof of the authorized TS store. A
   correction must close the representability gap and the conditional
   false-absence *risk*; it must not overstate C14 as a reproduced full-Run
   defect.
2. A **schema-admitted** positive target example establishes
   *representation*. It does not claim real native extraction truth.
3. First-party SYMBOL targets remain representable. Unary FILE/PACKAGE
   *source* occupancy remains representable. Those must stay coherent.
4. Occupancy=external remains lawful for a distinct namespaced vertex.
5. Query empty neighbors are still not “no callers.” Unattested incoming
   search is still unknown, not none.
6. Grammar intersection (`file:src/lib/util.ts` as both LogicalPath and
   SubjectIdV1) is excluded from ordinary positives (P4 C15).

Product intent remains portable file/package incoming analysis and
relationship navigation. Withdrawing advertised FILE/PACKAGE
`imports.targetKinds` is therefore not the preferred answer.

Codex’s initial preference — keep existing portable inventory identities;
do not have the host parse provider namespaces — is a preference, not a
decided solution. The recommendation below coincides with that preference
only after independent comparison.

## 3. Current law that any correction must join

These are source24 owners, not newly invented requirements.

### 3.1 Two lawful identity grammars

| Coordinate | Grammar | Owner |
|---|---|---|
| File inventory / evaluation-subject `nativeSubjectId` | LogicalPath; equals `path` and `qualifiedName` | `subject-inventory.schema.v1.json` InventoryRowV1; `enumeration-contract.v1.md` §8 |
| Package inventory / evaluation-subject `nativeSubjectId` | attested `packageName` (= `qualifiedName`); identity is `(universe, package, packageName, packageManifestPath=row.path)` | same |
| Symbol inventory / evaluation-subject `nativeSubjectId` | opaque `SubjectIdV1` | InventoryRowV1 symbol branch |
| `ImportsPayloadV1.importer` and `resolvedTarget` | `SubjectIdV1` (`^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+$`) | `relation-payload-schemas.v2.json#/$defs/ImportsPayloadV1` |
| `TargetAttributionV1.targetNativeId` | exact copy of the payload field named by `relations[fact.relation].targetNativeIdField` | `target-attribution.schema.v1.json` join law |
| Finding fingerprint `subjectKey.logicalPath` | path-stable logical correspondence; not opaque native IDs | `identity-schemas.v3.json` finding-fingerprint; composition §4 |
| File unary payload `path`; package unary `packageName`+`manifestPath` | LogicalPath / CanonicalText; endpointTarget forbidden | registry relations.file / relations.package |
| Clone body IDs | opaque candidate body IDs; not evaluation-subject authority | `execution-inputs-contract.v1.md` §6 |

`SubjectIdV1` description is explicit: lowercase namespace, colon, **opaque**
NFC identity. Join law `derivation.never`: do not parse `namespace:opaque`
to invent kind or occupancy; do not invent first-party
`packageManifestPath` from `logicalPath`.

### 3.2 Advertised FILE/PACKAGE target surface

- Registry `relations.imports.targetKinds = [file, symbol, package]`;
  `endpointTarget=admitted-at-rung` at `resolved-target`.
- `kindApplicability.endpointTarget` uses **targetKinds**, not
  `sourceSubjectKind`.
- PolicyDocumentV2 `Atom.endpoint` enum `source|target` (default source).
- Composition §2: enabled rules select every admitted program of the
  required primary subject kind; include/exclude apply to logical path,
  never opaque native IDs.
- Query table: `imports@resolved-target` target kinds file, symbol,
  package; target kind from admitted TargetAttributionV1; projected
  target `nativeSubjectId` is `payload.resolvedTarget`.
- Incoming bind: current `E=(U,K,N)` occupies the target native-id field
  after native-id compare.

Unary file/package and calls/references/control-flow/reachability do **not**
advertise file/package targets. Wrong kind is `ATOM_KIND_INCOMPATIBLE`,
never vacuous none.

### 3.3 The unsatisfiable ordinary first-party FILE set

1. File inventory N is ordinary LogicalPath `src/lib/util.ts`.
2. `resolvedTarget` is SubjectIdV1, so ordinary path is not a lawful payload
   value.
3. `targetNativeId` must equal `resolvedTarget`.
4. occupancy=first-party requires `targetNativeId` exact inventory native id.
5. Atom `_native_occupancy` for `endpoint=target` returns NOMATCH when
   `payload[targetNativeIdField] != E.nativeSubjectId`, **before** kind /
   occupancy reconcile.

Replace occupancy=first-party with occupancy=external (or unknown): the
constraints hold, and the evaluation subject remains a **different tuple**
from the projected target. That is P4’s jointly satisfiable external
authoring. It does not occupy `(U, file, src/lib/util.ts)`.

### 3.4 Reference suite currently bypasses payload schema

`foundation/check-atoms.v1.py` `test_source_kind_vs_incoming_target_kind`
uses `resolvedTarget: "src/a.ts"` and expects incoming `exists=true` on
file subject `src/a.ts`. That string is LogicalPath, not SubjectIdV1, so it
is **not** a schema-admitted ImportsPayloadV1 value. Atom matching
string-compares the payload field and does not admit the payload schema.
This local bypass must not be treated as an existing positive
representation. Successor controls must use schema-admitted SubjectIdV1
payloads.

## 4. Independent comparison of P4 options

Any coherent fix must make matchingFacts occupy the **same evaluation
identity** as first-party `E`. Changing occupancy metadata alone
(`logicalPath`, sidecar occupancy) cannot create a known-hit while compare
remains payload SubjectIdV1 versus inventory LogicalPath/packageName.

### 4.1 Option D — withdraw FILE/PACKAGE from `imports.targetKinds` (P4 O1)

`imports.targetKinds` becomes `{symbol}`. File/package
`subjectEnumeration` + `endpoint=target` becomes `ATOM_KIND_INCOMPATIBLE`.

- Smallest **deletion**. Existing external occupancy graphs can remain.
- Contradicts stated product intent: portable file/package incoming
  analysis and relationship navigation.
- Policy rules that already advertise the combination start refusing.
- Does not preserve advertised surface; it withdraws it.

Not preferred. Retained as the explicit unsupported-surface alternative if
product intent were later changed.

### 4.2 Option C — file/package inventory native id becomes attested SubjectIdV1 (P4 O2)

Keep `path` / `manifestPath` as LogicalPath; attest `nativeSubjectId` as
SubjectIdV1 independently (no parse of path). Evaluation-subject N and
query inventory vertices use that SubjectIdV1. Payload already uses
SubjectIdV1, so R7 would match.

- Remints every file/package evaluation-subject, inventory native id,
  query inventory vertex, and subject3.
- Unary file source occupancy today compares `payload.path` to
  `E.nativeSubjectId`. After O2 those strings diverge unless unary law is
  also rewritten.
- Fingerprints still use `subjectKey.logicalPath`; subject3 would no
  longer equal that path for files. Composition §4 file/package
  `qualifiedName` is admitted path/package name — still coherent as a
  *fingerprint* field, but evaluation identity would stop being the
  portable inventory spelling.
- Package uniqueness already needs `packageManifestPath`; namespacing the
  name does not remove that coordinate.
- Breaking for every consumer that treated LogicalPath as file
  `nativeSubjectId`.

Rejected: it “fixes” target occupancy by destroying coherent unary
file/package/body-adjacent source identities. The gap is a **join**
between two lawful grammars, not a defect in inventory identity.

### 4.3 Option A — kind-discriminated payload endpoint identity (P4 O3)

When attribution.kind=file, the payload native-id field used for matching
is LogicalPath (inventory spelling); when kind=package, packageName plus
packageManifestPath; when kind=symbol, SubjectIdV1.

Concrete shape (draft, if this option were chosen):

```json
{
  "importer": "module:src/app.ts",
  "specifier": "./util",
  "resolvedTarget": {
    "kind": "file",
    "nativeId": "src/lib/util.ts"
  }
}
```

or a kind-discriminated `oneOf` on `resolvedTarget` itself. Matching stays
“native-id compare is first” against `E.nativeSubjectId`. Host ephemeral
unique-inventory derivation would then occupy first-party file subjects
without a new mapping record.

Tradeoffs:

| For | Against |
|---|---|
| Compare law stays one-string equality | `ImportsPayloadV1` currently reproduces inherited field **types**; this remints every imports `fact2` (payload is in fact identity) |
| Query vertices collapse (`src/lib/util.ts` vs `file:src/lib/util.ts`) | Opaque native payload IDs are lost for file/package targets |
| Reuses current ephemeral unique-inventory derivation | Native protocol emit grammar changes for the same field |
| C14 structurally impossible for ordinary files once payload equals inventory N | External file targets that today use `file:node_modules/...` change spelling; occupancy becomes the only distinction from first-party paths |
| No new mapping record | Host auto-promotion of path-equal targets to first-party is a positive occupancy fact created from payload/inventory equality, not from an explicit cross-grammar attestation |
| | Old frozen Runs’ namespaced query vertices disappear if a new profile is applied to old payloads — silent reinterpretation unless profile-pinned |

This is a coherent option. It is the smallest change to **matching**, and
the largest change to **payload, fact identity, and native emit grammar**.

### 4.4 Option B — provider-attested typed endpoint-to-evaluation mapping in a versioned sidecar (P4 O4, refined)

Keep `ImportsPayloadV1.resolvedTarget` as opaque `SubjectIdV1`. Keep file
inventory N as LogicalPath and package N as packageName. Add an explicit
**evaluation occupancy identity** on a successor TargetAttribution record.
MatchingFacts compare `E` to that occupancy identity, not to the opaque
payload string. Host does not parse `file:` / `package:` off
`SubjectIdV1`.

P4 O4 as written would reverse `logicalPath MUST be null on first-party`
and reuse `logicalPath` as the compare field. That is the wrong field:

- `logicalPath` is currently an external/unknown hint, forbidden on
  first-party, and is **not** a native-id compare field.
- Reusing it would silently change the meaning of existing V1 records if
  first-party `logicalPath` were later allowed.
- Package occupancy already has a distinct `packageManifestPath`
  coordinate; stuffing a file mapping into `logicalPath` does not give
  packages a typed name+manifest occupancy identity.

Refinement: **new fields**, new schemaVersion. Do not reverse the
`logicalPath` null-on-first-party law. Do not treat `logicalPath` as
occupancy identity.

Tradeoffs:

| For | Against |
|---|---|
| Preserves portable inventory identities (unary file/package, fingerprints, package uniqueness) | Compare law is no longer payload-string-first for file/package targets |
| Preserves opaque native payload IDs | Two identity planes remain (payload native id vs evaluation occupancy id) |
| Host does not parse provider namespaces | Requires a provider emission channel for the mapping; host capture is not authority |
| Mapping has uniquely admitted provider+inventory authority | Successor TargetAttribution schema, atom compare, query projection, native return, and proof-input document pointer |
| fact2 payload identity unchanged | Existing namespaced query vertices on **new** Runs disappear for first-party mapped facts (by occupancy, not by alias) |
| Old V1 Runs keep old interpretation if projection/compare are schemaVersion-dispatched | More join complexity than Option A |
| C14 closed: payload≠N is not occupancy nomatch; absent unique mapping is unknown, not none | Providers that today omit sidecars cannot represent first-party file/package hits until they emit V2 |

This is a coherent option. It is the smallest change that treats the gap
as a **join** rather than as a demand to collapse either grammar.

### 4.5 Forbidden non-options (not current law, not successor law)

- Parsing `file:` / `package:` off SubjectIdV1 to invent occupancy or
  evaluation native id.
- Inventing alias records that equate `(file, src/lib/util.ts)` with
  `(file, file:src/lib/util.ts)` as a general identity.
- Treating `logicalPath` as occupancy identity under current join law.
- Treating empty query neighbors as no callers.
- Treating unattested incoming search as none=true.
- Caches, host guesses, or namespace stripping creating positive
  occupancy facts or proving absence.

### 4.6 Recommendation

**Recommend Option B (refined P4 O4): TargetAttributionV2 explicit
provider-attested evaluation occupancy mapping.**

Independent reasons, not Codex deference:

1. The gap is unsatisfiability of a **join** between two already-lawful
   grammars. Collapsing inventory identity (C) or payload identity (A)
   “fixes” the join by deleting one grammar. Product intent needs both:
   portable file/package evaluation subjects **and** opaque native payload
   IDs.
2. Unary file/package source occupancy, fingerprint `logicalPath`,
   package `(name, manifest)` uniqueness, and clone body opacity are
   coherent today. Option C breaks them. Option A remints every imports
   fact2 and drops payload opacity.
3. Cross-grammar occupancy is a **positive fact**. Positive facts need
   uniquely admitted authority. Exact inventory match of an already-equal
   grammar (symbols today) is inventory authority. Exact inventory match
   after host stripping a namespace is a host guess. Option B makes the
   provider attest the evaluation identity and the host **validate** a
   unique inventory match. That is the existing sidecar architecture,
   extended with typed occupancy fields.
4. `relation-payload-schemas.v2.json` is explicitly not modified by the
   current atom/registry standing (`x-opensip-does-not-modify`; atom
   contract: “Native fact payload `$defs` are not extended”;
   TargetAttribution “MUST NOT be added to relation-payload-schemas”).
   Option A violates that payload-isolation posture. Option B continues
   it.
5. Old frozen Runs must retain old interpretation. Option A changes
   payload bytes/grammar; applying a new compare to old namespaced
   payloads would still miss, but applying a new projection that expected
   inventory spelling would mis-handle old graphs. Option B
   schemaVersion-dispatches: V1 records keep payload-vs-N compare and
   payload-string vertices; V2 records use occupancy identity. No silent
   remint of source24 or of old `run3` fingerprints.

Option A remains the leading **competing** alternative if later alignment
decides that payload opacity for file/package targets is less valuable
than keeping one-string compare. It is not withdrawn; it is not
recommended.

Option D remains available only if product intent is revised to
symbol-only first-party import targets.

## 5. Proposed successor — Option B field shapes and laws

Preimplementation: these are draft successor shapes. They are not applied
to source24 in this turn.

### 5.1 Identity planes (keep both)

**Payload / native-id plane** (unchanged):

- `ImportsPayloadV1.resolvedTarget`: opaque `SubjectIdV1`
- `TargetAttribution.targetNativeId`: exact copy of that field
- Query/atom **replay** of the fact still names this string
- Host never parses it

**Evaluation occupancy plane** (new, V2 only):

- File: `(universe, kind=file, evaluationNativeId=LogicalPath, packageManifestPath empty)`
- Package: `(universe, kind=package, evaluationNativeId=packageName, evaluationPackageManifestPath=LogicalPath)`
- Symbol: `(universe, kind=symbol, evaluationNativeId=SubjectIdV1, packageManifestPath empty)` with `evaluationNativeId == targetNativeId`
- This tuple **is** the evaluation-subject identity used for matchingFacts,
  incoming bind, and first-party graph target vertices

The mapping is directional occupancy of **this fact’s target endpoint**.
It is not a bidirectional alias between the two strings.

### 5.2 TargetAttributionV2 draft shape

New document `foundation/target-attribution.schema.v2.json`.
`$id` `opensip.product.target-attribution.2`. `schemaVersion` const `2`.
Identity remains raw SHA-256 of `C(this record)`; uniqueness remains
`(planId, sourceFactId)`.

Required fields (V1 set plus occupancy-identity fields):

| field | V2 law |
|---|---|
| `schemaVersion` | `2` |
| `planId` | retained Plan |
| `sourceFactId` | fact2 of that Plan |
| `producerClosure` | equals `fact.producerClosure`; closures[pc].kind=`provider` |
| `targetUniverse` | equals `fact.targetUniverse` |
| `targetNativeId` | equals payload field named by registry `targetNativeIdField` at fact.resolution (imports: `resolvedTarget`) |
| `kind` | `file\|symbol\|package\|unknown` |
| `occupancy` | `first-party\|external\|unknown` |
| `exported` | symbol-only tri-state; null otherwise |
| `logicalPath` | **unchanged V1 law**: optional only when occupancy is external or unknown; MUST be null when occupancy=first-party; NEVER an occupancy compare field; NEVER used to invent `evaluationPackageManifestPath` |
| `packageManifestPath` | keep V1 package coordinate as the **inventory join copy** when kind=package; see below |
| `evaluationNativeId` | new; nullable typed evaluation-subject `nativeSubjectId` |
| `evaluationPackageManifestPath` | new; nullable LogicalPath; package occupancy only |

V1 `packageManifestPath` already is the first-party package inventory
path. V2 may keep it as the package occupancy path **or** rename usage to
`evaluationPackageManifestPath` and require V1 `packageManifestPath` to
equal it when both present. Draft choice: **keep `packageManifestPath`
as the package occupancy path** (already the evaluation coordinate) and
add `evaluationNativeId` for the kind-discriminated evaluation native id.
Do not add a third package path. For kind=file/symbol,
`packageManifestPath` remains null.

`evaluationNativeId` admission:

| occupancy | kind | `evaluationNativeId` | `packageManifestPath` |
|---|---|---|---|
| first-party | file | required LogicalPath; unique inventory row `(U, file, evaluationNativeId)` | null |
| first-party | package | required CanonicalText packageName; unique inventory row `(U, package, evaluationNativeId, packageManifestPath)` | required LogicalPath |
| first-party | symbol | required SubjectIdV1; MUST byte-equal `targetNativeId`; unique inventory row `(U, symbol, evaluationNativeId)` | null |
| external | file\|symbol\|package | MUST be null | MUST be null (kind≠package already); kind=package external also null |
| unknown | any | MUST be null | MUST be null except existing V1 unknown-package hints remain unknown, not first-party |

No structural constraint of the form “`evaluationNativeId` is the suffix
of `targetNativeId` after the first colon.” Ordinary file examples will
*happen* to look that way; the join is still attested, not parsed.

`logicalPath` on first-party remains `TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY`.

### 5.3 Producer custody and selected execution-input ownership

Current standing (keep, then tighten):

- TargetAttribution is a **canonical-record blob** domain
  (`identity-schemas.v3.json` `x-opensip-digest-domains.byDomain.target-attribution`).
- Execution-inputs classifies it as a **host-derived typed input** in
  `hostCapture.hostDerivedRefs` / `selectedRefs`. That is **custody of
  captured bytes**, not authority to mint occupancy identity.
- Schema already: “Provider attribution truth is trusted after host join
  validation. Host derivation is an EPHEMERAL projection and MUST NOT be
  written as this record.”

Successor tightening:

1. **Authority** of `evaluationNativeId` / first-party occupancy is the
   Plan-selected **provider** named by `producerClosure`, after host join
   validation against admitted SubjectInventoryV1.
2. Host **captures** provider-emitted V2 records into
   `hostDerivedRefs`. Host does not fill `evaluationNativeId` by parse,
   cache, or suffix strip.
3. Host **ephemeral** unique-inventory derivation remains only for
   **exact native-id equality** of `targetNativeId` to an inventory
   native id (the symbol case, and any accidental C15 colon-path file
   whose inventory N is already SubjectIdV1). Ephemeral derivation MUST
   NOT invent a first-party file occupancy from `file:path` versus
   inventory `path`.
4. If the provider emits no V2 record: occupancy unknown. That is not
   occupancy=external and not a known-hit and not none.
5. Native protocol / native-evidence successor must add an **additive
   typed return** of TargetAttributionV2 (or an equivalent mapping
   record bound 1:1 to `sourceFactId`) from the same provider that minted
   the imports fact. rust-provider-protocol.v2 currently has no such
   record; this is a successor protocol obligation, not a host guess.
   Payload frames for `ImportsPayloadV1` stay unchanged.
6. Do not add TargetAttribution fields to
   `relation-payload-schemas.v2.json`. Do not add them to a view-only
   `derive-inventory-view` stage (`outputDomains: ["view"]`).

### 5.4 Compare / matchingFacts law (atom successor)

Replace, for `Atom.endpoint=target` only, the current first step in
`atom_model.v1.py` `_native_occupancy`:

```
tid = payload[targetNativeIdField]
if tid is None or tid != N or fact.targetUniverse != U: NOMATCH
```

Successor occupancy-identity compare (profile-pinned to V2 attributions):

1. Payload target field must be present at an admitted target rung.
   Absent field at requested rung remains filter/endpoint unavailable.
2. `fact.targetUniverse` must equal `E.universe` else NOMATCH.
3. Admit unique TargetAttributionV2 for `sourceFactId` (global
   `admit_atom_inputs` unchanged). Duplicate `(planId, sourceFactId)`
   still `TARGET_ATTRIBUTION_DUPLICATE_FACT`.
4. `targetNativeId` must equal the payload field (unchanged
   `TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH`). This is a **payload join**,
   not occupancy compare.
5. Occupancy identity I:
   - occupancy=first-party: I = `(targetUniverse, kind, evaluationNativeId, packageManifestPath or empty)`. Host unique-match against admitted inventory identities of this Plan. Size≠1 → `TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY` (admission refuse), not a silent match.
   - occupancy=external: I is not a first-party evaluation subject. Result for any first-party E is NOMATCH.
   - occupancy=unknown, or no V2 sidecar, or `evaluationNativeId` null when first-party required: occupancy unknown → FUNK / unknown, **not NOMATCH**, **not MATCH**.
6. MATCH iff E’s evaluation-subject tuple equals I.
7. Kind mismatch after known kind: NOMATCH (unchanged).
8. Payload string ≠ `E.nativeSubjectId` is **not** occupancy NOMATCH when
   the inventory grammar of `E.kind` is not SubjectIdV1.

Source occupancy (`endpoint=source`) is **unchanged**: file `path`,
package `packageName` **and** `manifestPath`, symbol SubjectIdV1.

Symbol target occupancy is unchanged in effect: `evaluationNativeId ==
targetNativeId == payload field == E.nativeSubjectId`.

Calls/references/control-flow/reachability stay symbol-only; file target
of calls remains `ATOM_KIND_INCOMPATIBLE`.

Registry successor text:

- `owedPartitions.incoming.bind`: current E occupies the **evaluation
  occupancy identity**, not the opaque payload native-id field.
- `owedPartitions.incoming.matchingFacts`: facts whose
  `targetUniverse=U` and occupancy identity = E (kind reconciled).
- Keep: facts with other T do not omit owed S.
- Keep: no Coverage S→U ⇒ `source-target-search-unattested`; never infer
  search of U from producer facts.

### 5.5 Absence law (C14 closed without overclaiming)

Under V2:

| Situation | Incoming `none` |
|---|---|
| Unique first-party occupancy identity equals E | false (known hit), even if payload string ≠ N |
| Unique first-party occupancy identity equals a **different** inventory subject | known nomatch for this E; may contribute to none if completeness holds |
| occupancy=external | known nomatch for first-party E |
| No V2 sidecar, occupancy=unknown, non-unique mapping | **unknown**, not none |
| Complete Coverage S→U (or admitted complete IncomingSearchV1) + stipulated sufficiency_v2 universal-negative + **only** known nomatches and no unknowns | none may be true. This remains a stipulated completeness construction until a fully admitted Run actually evaluates it |
| Same construction with a namespaced payload fact **and no mapping** | unknown (the V2 close of C14’s false-absence *risk*). Not a claim that the authorized TS store was replayed to none=true |

Query §0 is unchanged: zero neighbor rows is not “no callers.” Atom remains
the absence owner.

Unmapped V2-required imports facts are uncertain evidence. They must not
be dropped as known nomatch by payload≠N.

### 5.6 Graph projection / endpoint membership / paths / retained closure / disclosure

Query endpoint tuple shape is unchanged:
`(universe, kind, nativeSubjectId, packageManifestPath or empty)`.
graph-query request `schemaMajor` may remain 3. **Projection law is
successor** (query-projection-contract.v4, or v3 with an explicit
profile pin). Applying V2 projection to V1 attributions is forbidden.

Successor projection of `imports@resolved-target` **target** endpoint:

| occupancy | target vertex `nativeSubjectId` | `packageManifestPath` |
|---|---|---|
| first-party file | `evaluationNativeId` (inventory path) | empty |
| first-party package | `evaluationNativeId` (packageName) | sidecar `packageManifestPath` |
| first-party symbol | `evaluationNativeId` (== payload SubjectIdV1) | empty |
| external | `payload.resolvedTarget` (opaque SubjectIdV1) | empty |
| unknown / missing V2 | fact **unprojectable** (`unprojectable-fact`); not an inventory occupancy; not absence | |

Source endpoint remains `payload.importer` (symbol SubjectIdV1).

Consequences:

- First-party mapped imports occupy the **inventory** file/package
  vertex. Neighbors at `(U, file, src/lib/util.ts)` contain the fact.
- The opaque payload string is **not** a second vertex for that
  occupancy. No alias record is minted.
- A query asking for `(U, file, file:src/lib/util.ts)` on a V2 Run where
  that string is not an inventory native id and not an external projected
  endpoint is `QUERY.ENDPOINT_UNKNOWN`.
- External left-pad remains `(U, file, file:node_modules/left-pad/index.js)`
  (or whatever opaque id the payload carries).
- Isolated inventory vertices with no incident projected facts remain
  lawful; empty neighbors are not absence.
- Paths / reach / retained closure walk occupancy vertices. Disclosure
  still copies Coverage, IncomingSearchV1, deficiencies; it does not
  become a second absence evaluator.
- `host.cache` / `host.targetAttributions` remain non-authority
  (query contract §0/§8).

### 5.7 Admission / uniqueness / ambiguity

Keep existing V1 refusals. Add:

| key | when |
|---|---|
| `TARGET_ATTRIBUTION_EVALUATION_ID_REQUIRED` | occupancy=first-party and `evaluationNativeId` null |
| `TARGET_ATTRIBUTION_EVALUATION_ID_FORBIDDEN` | occupancy≠first-party and `evaluationNativeId` non-null |
| `TARGET_ATTRIBUTION_SYMBOL_EVALUATION_ID_MISMATCH` | kind=symbol first-party and `evaluationNativeId != targetNativeId` |
| `TARGET_ATTRIBUTION_EVALUATION_GRAMMAR` | first-party file `evaluationNativeId` fails LogicalPath, or first-party package name empty, or symbol fails SubjectIdV1 |
| `TARGET_ATTRIBUTION_OPAQUE_ID_AMBIGUOUS_OCCUPANCY` | within one Plan, two first-party V2 records share `(targetUniverse, targetNativeId)` and disagree on occupancy identity |
| `TARGET_ATTRIBUTION_SCHEMA_VERSION_MIXED` | a Run’s selected target-attribution refs mix schemaVersion 1 and 2 |

Keep: first-party size≠1 → `TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`.
Keep: sidecar occupancy=external while ephemeral exact-id occupancy is
first-party → `TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY`
(this continues to fire for **exact** native-id matches, i.e. symbols /
C15, not after a parse).

Ambiguous same packageName at two manifests: occupancy stays unknown
unless `packageManifestPath` selects exactly one row (existing R12).

Include/exclude globs still apply to logical path, never to opaque
payload IDs.

Unknown sidecar fields still cannot override independently known
ephemeral fields. Independently known ephemeral first-party from exact
id match still wins over sidecar unknown. Exact-id ephemeral **cannot**
become first-party for ordinary `file:path` versus inventory `path`.

Caches are not uniqueness authority.

### 5.8 Proof / output / replay / domain identity

- `proof.evaluationInputRefs` continues to include
  `{domain: target-attribution, digest: raw SHA-256 of C(V2)}`.
- identity-schemas.v3 `byDomain.target-attribution.record.document`
  successor-points at `target-attribution.schema.v2.json`. That pointer
  change is a successor identity-schema pin, not a silent rewrite of
  already sealed V1 blobs.
- `close_run` complete replay re-admits V2 joins. It must not interpret
  V1 bytes as V2 occupancy identity.
- subject3 / finding3 / finding-key2 / run3 recipes are unchanged.
  File/package evaluation-subjects keep path/packageName. Fingerprints
  keep `subjectKey.logicalPath`. Old frozen Run fingerprints are not
  reinterpreted.
- Predicate-witness matching/uncertain fact sets follow the successor
  occupancy compare. A V2 known-hit is a knownFactId on the file
  subject even though payload ≠ N.

### 5.9 Policy / config / contract / readiness

- PolicyDocumentV2 Atom.endpoint and subjectEnumeration.subjectKind
  **unchanged**. The advertised surface is kept and made representable.
- policy-document.schema.json v1 still lacks endpoint; that remains a
  schema-generation standing note, not withdrawal of V2 advertisement.
- Product identity §4 incorporation list successor-names the atom and
  query contracts that carry occupancy-identity compare/projection.
- Evaluator **output** profile may remain 3: evaluation-subject,
  finding3, proof3, run3 recipes do not change. Successor atom/query
  contracts are incorporated constituents, not an invented evaluator4,
  unless a later identity-schema major is independently required.
- graph-query request schemaMajor may remain 3; projection contract
  successor is the law change.
- Readiness grades, application, and implementation authorization are
  **not** claimed. Historical source24 design assent is preserved and
  still cannot authorize application/readiness until successor
  correction and reviews exist.

### 5.10 Version dispatch for old Runs

| Artifact | Old frozen Run (TargetAttributionV1) | Successor Run (V2) |
|---|---|---|
| Payload `resolvedTarget` | SubjectIdV1 | SubjectIdV1 (unchanged) |
| File inventory N | LogicalPath | LogicalPath (unchanged) |
| Atom compare | payload vs N (R7); ordinary file known nomatch | occupancy identity vs E |
| Query imports target vertex | payload string | first-party: evaluation identity; external: payload string |
| Incoming none with complete search and only namespaced payload facts | stipulated C14 risk under V1 law | unknown unless mapped; known hit if mapped to E |
| Fingerprints / subject3 | old bytes, old meaning | new Runs mint new subject3 only when subjects actually change (they should not for this correction) |

Never apply V2 compare or V2 projection to V1 records. Never mutate
source24. Never relabel a V1 digest as V2 authority.

Because this is preimplementation design, these are **explicit successor
schema/profile needs**, not invented deployed-compatibility promises. No
on-the-wire migration of already-shipped products is claimed; there is no
authorized implementation.

## 6. Exact ordinary examples and controls

Universe `U0` =
`0000000000000000000000000000000000000000000000000000000000000000`
is schematic. Examples are schema-admitted representation controls, not
native extraction truth, not Run admission.

Ordinary grammars (same as P4; colon-path excluded from ordinary
positives):

| name | value | SubjectIdV1 | LogicalPath |
|---|---|---|---|
| ordinary file path | `src/lib/util.ts` | false | true |
| ordinary package name | `demo-app` | false | true |
| ordinary manifest path | `package.json` | false | true |
| ordinary symbol id | `module:src/lib/util.ts` | true | true |
| namespaced file id | `file:src/lib/util.ts` | true | true |
| namespaced package id | `package:demo-app` | true | true |
| excluded colon path | `file:src/lib/util.ts` used **as file inventory N** | true | true |

### 6.1 Positive FILE — schema-admitted known-hit

Inventory row: `{kind:file, nativeSubjectId:"src/lib/util.ts", path:"src/lib/util.ts", qualifiedName:"src/lib/util.ts"}`

E: `{schemaVersion:3, universe:U0, kind:file, nativeSubjectId:"src/lib/util.ts"}`

Payload (ImportsPayloadV1): 

```json
{
  "importer": "module:src/app.ts",
  "specifier": "./util",
  "resolvedTarget": "file:src/lib/util.ts"
}
```

TargetAttributionV2:

```json
{
  "schemaVersion": 2,
  "kind": "file",
  "occupancy": "first-party",
  "targetNativeId": "file:src/lib/util.ts",
  "evaluationNativeId": "src/lib/util.ts",
  "logicalPath": null,
  "packageManifestPath": null,
  "exported": null
}
```

Required results under successor law:

- payload join: `targetNativeId == resolvedTarget`
- occupancy MATCH on E
- incoming `exists=true`; `none=false`
- query target vertex `(U0, file, src/lib/util.ts)`
- `(U0, file, file:src/lib/util.ts)` is not that vertex
- Host must not derive `evaluationNativeId` by stripping `file:`

### 6.2 Positive PACKAGE — schema-admitted known-hit

Inventory: `{kind:package, nativeSubjectId:"demo-app", path:"package.json", qualifiedName:"demo-app"}`

E: `{schemaVersion:3, universe:U0, kind:package, nativeSubjectId:"demo-app", packageManifestPath:"package.json"}`

Payload: `{importer:"module:src/app.ts", specifier:"demo-app", resolvedTarget:"package:demo-app"}`

V2 sidecar: `kind=package`, `occupancy=first-party`,
`targetNativeId="package:demo-app"`, `evaluationNativeId="demo-app"`,
`packageManifestPath="package.json"`, `logicalPath=null`.

Required: MATCH on that package subject; query vertex includes
`packageManifestPath=package.json`; a second first-party `demo-app` at
`apps/demo/package.json` is a different subject.

### 6.3 Positive SYMBOL — control, must remain representable

Inventory N = payload = targetNativeId = evaluationNativeId =
`module:src/lib/util.ts`. occupancy=first-party. Query vertices equal.
Calls/references/control-flow/reachability unchanged. This does not
substitute for FILE/PACKAGE positives.

### 6.4 External FILE — control, remains lawful and distinct

Payload `resolvedTarget="file:node_modules/left-pad/index.js"`.
V2: occupancy=external, `evaluationNativeId=null`,
`logicalPath="node_modules/left-pad/index.js"` optional hint.
Incoming on first-party `src/lib/util.ts`: NOMATCH.
Query vertex is the opaque payload id, not an inventory subject.
First-party occupancy on that namespaced id still refuses
`TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`.

### 6.5 Unknown / incomplete / unattested — must not become none

- No V2 sidecar on an imports@resolved-target fact whose payload is
  namespaced file id: incoming unknown; query unprojectable-fact; not
  none=true.
- occupancy=unknown, `evaluationNativeId` null: same.
- No Coverage S→U and no IncomingSearchV1: `source-target-search-unattested`
  (C13, unchanged).
- `examinedExhaustive=false` never proves complete search (unchanged).

### 6.6 Negative / refusal controls

| id | attempt | exact refusal / result |
|---|---|---|
| N1 host parse | first-party file sidecar with `evaluationNativeId` omitted; host would strip `file:` | `TARGET_ATTRIBUTION_EVALUATION_ID_REQUIRED`; never MATCH |
| N2 payload sneak | `resolvedTarget="file:src/lib/util.ts"` and `targetNativeId="src/lib/util.ts"` | `TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH` (C11, kept) |
| N3 unlawful payload | `resolvedTarget="src/lib/util.ts"` | ImportsPayloadV1 SubjectIdV1 schema fail; not a positive |
| N4 first-party missing inventory | evaluationNativeId not in inventory | `TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY` (C10, kept) |
| N5 logicalPath on first-party | `logicalPath="src/lib/util.ts"` with occupancy=first-party | `TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY` |
| N6 file target of calls | subjectKind=file, endpoint=target, calls@resolved-callee | `ATOM_KIND_INCOMPATIBLE` (C7) |
| N7 unary endpoint=target | file/package relation | `ATOM_ENDPOINT_UNAVAILABLE` (C9) |
| N8 syntactic-specifier target | imports@syntactic-specifier endpoint=target | `ATOM_ENDPOINT_UNAVAILABLE` / `QUERY.RELATION_UNSUPPORTED` (C8) |
| N9 duplicate package name | two manifests, sidecar lacks distinguishing path | occupancy unknown, not first-party |
| N10 mixed schemaVersion | V1 and V2 attributions selected on one Run | `TARGET_ATTRIBUTION_SCHEMA_VERSION_MIXED` |
| N11 opaque-id occupancy clash | two first-party V2 records, same `(U, targetNativeId)`, different evaluation identity | `TARGET_ATTRIBUTION_OPAQUE_ID_AMBIGUOUS_OCCUPANCY` |
| N12 producer not provider | `kind=evaluator` producerClosure | `TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER` |
| N13 C15 not ordinary positive | inventory N=`file:src/lib/util.ts` | excluded from ordinary positives; lawful only if that path is truly a file inventory native id, still requiring explicit evaluationNativeId, not parse |
| N14 V1 bytes under V2 law | apply occupancy compare to schemaVersion=1 sidecar | forbidden; old Run keeps R7 |

### 6.7 C14 successor restatement (limit preserved)

P4 construction: E file `src/lib/util.ts`; fact.targetNativeId
`file:src/lib/util.ts`; nativeIdEqual false; matchingFacts []; complete
Coverage S→U stipulated; sufficiency_v2 universal-negative **stipulated**;
incomingNone true under **V1** compare.

Successor:

- If a V2 sidecar maps that fact to E: known hit; none false.
  Representation is shown by the schema-admitted positive in §6.1, not by
  replaying the authorized TS store.
- If no V2 sidecar: unknown, not none. This closes the false-absence
  *risk* of payload≠N under complete search.
- This document does **not** claim an executed fully admitted none=true
  (or none=false) proof of
  `run3:8170fc2c58c49759e89b3994ba92cf2d59f27a7721ac88698985628e2d2057db`.

### 6.8 Outgoing targetKind=file on symbol source (C16)

Unchanged and still not FILE target occupancy. FieldFilter `targetKind`
projects `targetAttribution.kind`. Current subject is the source importer.

## 7. Affected owning joins (complete trace)

| Join | Current owner | Successor impact under Option B |
|---|---|---|
| Native payload | `relation-payload-schemas.v2.json` ImportsPayloadV1 | **Unchanged**. resolvedTarget remains SubjectIdV1 |
| Native schema isolation | atom contract; registry `x-opensip-does-not-modify` | **Preserved**. Mapping stays out of payload `$defs` |
| Native protocol | `native-evidence.md`; `rust-provider-protocol.v2.json`; `native/protocol3-transitions.v1.json` | **Additive** typed TargetAttributionV2 return from the fact’s provider. No payload grammar change. No protocol3 phase/frame redesign unless a later native owner requires an extra result channel |
| Native profile / capability | `native-capability-matrix.v2.json`; capability-manifest-domains | imports capability still emits resolved-target facts; attribution becomes an owed typed return for first-party file/package occupancy |
| Target-attribution producer custody | target-attribution.schema.v1 join law; execution-inputs hostDerivedRefs | V2 schema; provider attests evaluationNativeId; host captures/validates; host does not mint |
| Selected execution-input ownership | execution-inputs.schema.v1; execution-inputs-contract §1/§6/§7 | Same domain and custody class; document pointer and admission keys update to V2; still not a view-only stage product |
| Enumeration / inventory | enumeration-contract.v1; subject-inventory.schema.v1 | **Unchanged** file path / package name identities, totality, package uniqueness |
| Evaluation subject | identity-schemas.v3 `evaluation-subject`; composition §1 | **Unchanged** subject3 recipe |
| Atom matching / incoming | atom-evaluation-contract.v1 §2; atom_model `_native_occupancy`; registry incoming.bind / matchingFacts | Successor occupancy-identity compare; payload join retained |
| Target filters | registry filters.targetKind; FieldFilterSuccessorV1 | still `targetAttribution.kind`; unknown kind still indeterminate, not nomatch |
| Completeness / IncomingSearch | incoming-search.schema.v1; atom §4; registry incoming.attestation | **Unchanged** universe-search law. Unmapped facts become unknown evidence, so they **block** none rather than feed it |
| Alias ambiguity | currently no alias records | still no alias records; new uniqueness over `(U, targetNativeId) → occupancy identity` |
| Graph projection | query-projection-contract.v3 §2–3; query_projection_model.v3 `project_fact` | Successor: first-party target vertex = evaluation identity; external = payload id; unknown = unprojectable |
| Endpoint membership | query §2 vertex domain | inventory rows unchanged; projected endpoints follow occupancy |
| Paths / reach / retained closure | query §4–6 | walk occupancy vertices; disclosure unchanged in kind |
| Proof / replay | identity-and-evidence §4; identity-model.v3 close_run; executionInputsDigest | re-admit V2; V1 Runs replay under V1; no silent fingerprint remint |
| Domain identity | identity-schemas.v3 byDomain.target-attribution | successor document pointer to schema v2 |
| Policy / config | policy-document.v2.schema.json; product-configuration | Atom.endpoint unchanged; config/profile pins successor contracts |
| Contract incorporation | identity-and-evidence §4; workflows-and-surfaces.md | name successor atom/query contracts |
| Readiness / application | central register; admission-and-qualification.md | **not authorized** by this draft |
| Public faults | target-attribution `x-opensip-new-internal-faults`; public-detail-registry.v1.json; D9 | new keys listed in §5.7 remain NEW/internal until root public-detail / D9 integration, same standing as current TARGET_ATTRIBUTION_* keys |
| Reference controls | check-atoms.v1.py; check-query-projection.v3.py | replace illegal `resolvedTarget:"src/a.ts"` bypass with §6 schema-admitted positives/negatives |
| Fingerprints | finding-key2 subjectKey.logicalPath; composition §4 | **Unchanged** path-stable correspondence |
| Body identity | clone candidate body ids | **Unchanged** |

## 8. Source impact inventory (draft; not applied)

Do **not** edit these in this turn. Listed so Codex can align a later
reference-correction plan.

### 8.1 Expected successor files (new)

- `foundation/target-attribution.schema.v2.json`
- `foundation/atom-evaluation-contract.v2.md` (or a clearly versioned
  successor of v1 that pins occupancy-identity compare)
- `workflows/query-projection-contract.v4.md` (or v3 successor section
  with explicit V1/V2 dispatch)
- Additive native-evidence / protocol result schema for
  TargetAttributionV2 emission (owner: native contract, not payload
  `$defs`)

### 8.2 Expected successor edits (existing owners)

- `foundation/evaluator-projection-registry.v1.json` (or v2):
  incoming.bind, matchingFacts, compare-law note. Do not change
  `imports.targetKinds`.
- `foundation/atom_model.v1.py` successor: occupancy compare;
  `evaluationNativeId` admission; no namespace parse helper that can
  succeed a match.
- `foundation/check-atoms.v1.py`: schema-admitted FILE/PACKAGE positives;
  N1–N14 negatives; keep symbol/external/unary/C7–C9 controls.
- `workflows/query_projection_model.v3.py` successor `project_fact`
  target nativeSubjectId selection.
- `workflows/check-query-projection.v3.py`: first-party file vertex
  occupancy; external namespaced vertex; ENDPOINT_UNKNOWN at unmapped
  namespaced id; empty neighbors still not absence.
- `foundation/identity-schemas.v3.json` byDomain.target-attribution
  document pointer (successor pin).
- `foundation/execution-inputs-contract.v1.md`: V2 document cite;
  provider-attest vs host-capture distinction.
- `docs/v2/contracts/product-v1/identity-and-evidence.md` §4
  incorporation names.
- `docs/v2/contracts/product-v1/native-evidence.md`: additive
  attribution return; no payload type change.
- `public-detail-registry.v1.json` / fault contract: new keys when root
  integrates (same pending standing as current TARGET_ATTRIBUTION_*).
- evaluator3 / native / workflow source-pins after those bytes exist.

### 8.3 Must not change for this correction

- `relation-payload-schemas.v2.json` ImportsPayloadV1 field types
- `subject-inventory.schema.v1.json` file/package nativeSubjectId grammar
- identity-schemas.v3 `evaluation-subject` required fields
- PolicyDocumentV2 Atom.endpoint
- IncomingSearchV1
- finding-key2 / fingerprint recipe
- clone body identity
- unary file/package endpointTarget=forbidden
- calls/references/control-flow/reachability targetKinds={symbol}
- source24 historical bytes in this turn
- authorized TS store / any retained Run interpretation

### 8.4 Option A impact (if later selected instead)

Would additionally change ImportsPayloadV1, remint imports fact2, change
native emit grammar, collapse query vertices by payload spelling, and
reuse ephemeral exact-id derivation for files. Still would need profile
dispatch so old namespaced payloads are not silently re-read as path
ids. Not recommended.

## 9. Bounded integration / review plan

This is a design-alignment plan, not an implementation schedule and not a
claim that work is ready to merge.

1. **Align (this artifact).** Codex reads this draft, accepts or
   rejects Option B versus Option A, and names any field-shape
   disagreements (`evaluationNativeId` versus reused `logicalPath`;
   package path field naming; native return channel). No source24 edit.
2. **Successor contracts.** Author the schema/contract files in §8.1–8.2
   as isolated successors. Pin schemaVersion dispatch. Do not rewrite
   V1 records or historical preservation reports as if they already
   contained V2 law.
3. **Reference controls.** Implement §6 positives/negatives in atom and
   query checkers. Require schema admission of ImportsPayloadV1 on every
   imports fixture. Forbid a helper that strips `file:` and then
   matches. Keep symbol, external, unary, C7–C9, C13, C15 controls.
4. **Reference replay.** Source-pinned atom + query + execution-input
   checks on synthetic graphs only. A schema-admitted positive is
   representation, not compiler truth. Do not claim close_run of the
   authorized TS store as the FILE positive.
5. **Independent review.** Fresh kit-only review of successor bytes:
   representability of §6.1–6.2, C14 limit preserved, no host parse,
   V1 Runs unchanged, unary/symbol coherence.
6. **Application / readiness.** Separate D-372-style act after
   acceptance. This draft does not move readiness grades.

Stop conditions: disagreement on Option A vs B; any attempt to treat C14
as an executed full-Run false result; any host parse helper that can
create MATCH; any silent V1→V2 reinterpretation.

## 10. What this document does not claim

- Not acceptance of source24 or of this successor.
- Not implementation readiness or product qualification.
- Not a live normative edit.
- Not a reproduced none=true of the authorized TS store.
- Not a claim that occupancy=external is unsatisfiable.
- Not a claim that Option A is incoherent; it is coherent and not
  recommended.
- Not Codex preference treated as a requirement.

## 11. Key decisions (draft, pending Codex alignment)

1. Keep advertised FILE/PACKAGE imports targets; do not choose Option D
   unless product intent is revised.
2. Keep portable inventory identities and opaque payload SubjectIdV1.
3. Choose Option B: TargetAttributionV2 evaluation occupancy mapping
   with unique provider+inventory authority.
4. Do not reuse `logicalPath` as the mapping field; do not reverse
   null-on-first-party.
5. Occupancy-identity compare replaces payload-vs-N compare for
   `endpoint=target` under V2 only.
6. Query first-party target vertices use evaluation identity; no alias
   records; external vertices keep opaque payload ids.
7. Old V1 Runs keep V1 compare/projection. Successor schema/profile
   pins are required; deployed compatibility is not invented.
8. Schema-admitted FILE/PACKAGE positives are required reference
   controls and are not extraction truth.
9. C14 remains a stipulated completeness construction; V2 closes the
   representability/false-absence risk without overclaiming.
