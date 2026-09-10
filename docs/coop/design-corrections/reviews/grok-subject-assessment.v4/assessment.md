I'll start from the v3 root assessment and the frozen Plan/native/capability definitions, then settle GR3–GR5 as exact obligations rather than inferred from retained scopes.Root left GR3–GR5 open. Next I’ll read Plan-bound context, capability-cell ownership, and the language/ownership tables that have to pin expected population.# GR3/GR4/GR5 — Plan-bound enumeration obligations and source language

**Standing.** Bounded coauthor law/schema sketch. Frozen21 pin unchanged (manifest `360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`). SUBJECT-D1–D6 stand. This does **not** close GR6/GR8 or G3–G9. Examples conceptual. No source edit.

**Defect.** Defining `U(rule)` from retained scopes/universe frames lets omitted work shrink the expected set. `plan.nativeContextDigests` pins **contexts**, not universes: one TypeScript context can back several `TypeScriptConfigGraphV1` entry programs; one Rust universe can carry 1–4 `cfgSets`. Universe H is a **successful bind** of resolved inputs (`bind_typescript_universe` / `bind_rust_universe` / `bind_syntax_universe`). Compiler/provider failure must not mint a fake H, and a producer `complete` flag or `expectedFindings` list is not a replay oracle.

## 1. Planning record (no native symbols)

Do **not** overload `stage-spec` (exec-plan derivation; `operation` is producer-defined). Add a Plan-bound parameter payload, using existing `analysis-spec.parameters[]` (`schemaDigest` + `payloadDigest`, identity-schemas `#/$defs/analysis-spec`). Register the document in `x-opensip-payload-registry.classes.parameter`. It enters `plan.analysisSpecDigest` and therefore PlanId. Replay re-derives it from retained snapshot + membership + spec + named closures; **no compiler**.

**`EnumerationObligationSetV1`** — H domain `enumeration-obligation-set` (prefix `eobset2:`), max 1024 obligations (same cap as `requestedCapabilities`).

```
{ schemaVersion: 1,
  snapshotId,
  analysisSpecDigest,          // must equal plan.analysisSpecDigest
  scopeDigest,                 // plan.scopeDigest (scope-descriptor)
  membershipDigest,            // raw SHA-256 of C(UnitMembershipV1) retained
  obligations: [ ... ] }       // canonical-set by obligationId
```

**`EnumerationObligationV1`** (row):

| Field | Cardinality / type | Rule |
|---|---|---|
| `obligationId` | `eob1:` + H(this row without id) | unique in the set |
| `ownership` | `{languageMode, workspaceRoot}` | `workspaceRoot` is a `LogicalPath`; mode ∈ languageModes map |
| `capabilityIds` | 1..16 CanonicalIds, canonical-set | subset of `requestedCapabilities` with this ownership pair |
| `required` | bool | **OR** of those rows’ `required` (ownership-tuple uniqueness already forbids split requiredness per cell; this OR is across *different* capabilityIds on the same unit) |
| `kind` | `file \| package \| symbol` | see kind map |
| `enumeratorClosure` | `closure2:` | **named at planning**; `kind=provider`; **must** be ∈ `plan.semanticClosures`. Extra closures do not enumerate. |
| `nativeContextDigest` | 64-hex \| `null` | member of `plan.nativeContextDigests` if context admitted; `null` if context admission failed (still an obligation) |
| `extentDigest` | 64-hex | raw SHA-256 of `C(SourceExtentV1)` |
| `expectedUniverse` | 64-hex \| `null` | universe H **only** if `bind_*` succeeded on retained inputs; **never** synthesized on failure |

**Kind map** (matrix `native-capability-matrix.v2.json#/capabilities[].relations` + `subjectKindLaw`):

- any `inventory` relation (`file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported`) → obligations `file` and `package`
- any relation with registry `subjectKind: symbol` (`syntax`, `imports`, `references`, `calls`, `types`, `reachability`, unresolved-edge, …) → `symbol`
- `clones-fact` is `source-path`; covered by `file` extent (bodies), not a fourth kind
- policy `export` is a **filter** on the symbol inventory, not a Plan obligation

Collapse: one obligation per `(languageMode, workspaceRoot, enumeratorClosure, kind)` even if several capabilityIds contribute.

**`SourceExtentV1`** (host-only; no symbols):

```
{ workspaceRoot, languageMode,
  membershipClass: program-member | syntax-grammar | inventory-all,
  paths: LogicalPath[] }   // max 100000, canonical-set, unique
```

Construction (pure over retained bytes):

1. Re-run `discover_units` / `assign_membership` on snapshot inventory + admitted boundaries + `scope-descriptor` (native §1.4 U-1–U-8). Compiler is not run.
2. Take `FileMembershipRowV1` rows for this `workspaceRoot` / mode:
   - compiler modes (`ts-tsconfig`, `js-allowjs`, `js-synthesized`, `rust-cargo`, `rust-cargo-prepared`): `membership=program-member`, `reason=deepest-unit-in-language`
   - `syntax-only` **symbol/code**: `syntax-only`/`grammar-only` paths whose suffix is a **selected** `syntaxClass=code` grammar
   - `file` kind, all modes: inventory-exempt — every snapshot path in the unit/scope including unsupported, data-document, extensionless (`inventoryIsNotGrammarGated`)
3. Intersect `plan.scopeDigest` prefixes / excludes.

**Package extent** is not `node_modules`. First-party manifests only: inventoried `package.json` / `Cargo.toml` (and workspace `memberPackageRoots`) under the unit. Pruned trees (U-4a) and `ResolvedNodeModulesLayoutV1` / `DependencySourceSetV1` rows are **resolution observations**, never snapshot policy subjects. No fake snapshot path for an imported crate.

**Provider selection (GR5).** For each `(languageMode, workspaceRoot)` the host picks **exactly one** `provider` closure that implements that mode (same act as choosing `stage-spec.producerClosure`, but recorded here). Zero providers + `required=true` → pre-Plan `REQUEST.UNSATISFIABLE` / `PROVIDER.NOT_SELECTED` (existing cell law). Zero providers + `required=false` → obligation still minted, `enumeratorClosure` names the intended provider id only if selected; else outcome `unavailable` / `provider-unavailable`. Several `plan.semanticClosures` do **not** race: only the named enumerator is the expected binding. Expected binding **does not** read producer inventories, scopes, or facts.

## 2. Producer outcome (every obligation)

**`EnumerationOutcomeV1`** — H domain `enumeration-outcome` (`enumout2:`). One per obligation. **Not** a Plan field (compiler may fail after PlanId).

```
{ schemaVersion: 1,
  obligationDigest,                 // eobset row / obligationId preimage
  enumeratorClosure,                // must equal obligation.enumeratorClosure
  state: complete | partial | unavailable,
  unavailableCause: null | provider-unavailable | language-tier-unsupported
    | input-closure-incomplete | budget-exhausted | native-context-mismatch
    | bind-failed | provider-fault | capability-missing,
  universe: DigestHex | null,
  inventoryId: subjinv2: | null,
  examinedPathsDigest,              // SHA-256 C(canonical-set of examined LogicalPaths)
  examinedPathCount }               // 0..100000
```

**Checks (Run closure, still no compiler):**

- Every obligation has exactly one outcome pointer in the proof inputs. **Missing pointer** on a listed obligation: **structural refusal** (SUBJECT-D6).
- Pointer present, bytes missing: **retention loss**. Corrupt/schema-invalid bytes: **admission/hash fault**. Not one `HOST.IO_FAILURE`.
- `enumeratorClosure` mismatch vs obligation: refuse (`ENUMERATOR_BINDING_MISMATCH`).
- `state=unavailable`: `universe` **null**, `inventoryId` **null**. Do not mint universe H. `required=true` → required-unknown (SUBJECT-D5). `required=false` → disclose.
- `state=complete`: `examinedPathsDigest` **equals** obligation `extentDigest` paths. `inventoryId` **required** even if zero rows (complete-empty). If `expectedUniverse ≠ null`, outcome `universe` must equal it; if expected was null and producer now supplies an H, it must re-bind from retained context+inputs (`bind_*`) or refuse.
- `state=partial`: examined ⊂ extent, not equal; inventory present; population **unestablished**. Not complete-empty.
- `complete` + inventory omitted: structural refusal.
- Empty rows + `complete` + examined=extent: **complete-empty** (lawful zero symbols/files/packages).
- Empty rows + no outcome / `unavailable` / `partial`: **not** complete-empty.

**Inventory** (`EnumeratedSubjectInventoryV2`, prior sketch): bound to `obligationDigest` + `enumeratorClosure` + `snapshotId` + `universe` (null forbidden here; unavailable has no inventory). No `scopeId`. Scopes list `subjects ⊆` inventory native ids; inventory does not name scopes. **Acyclic.**

Same `(universe, nativeSubjectId)` from a **non-named** provider: ignored as unselected. Same pair from the named provider twice: refuse duplicate occurrence `(kind, universe, nativeSubjectId)` (SUBJECT-D1 occurrence key). Distinct declarations remain GR6/identity §3.

## 3. Language and keys (GR4)

Engine language (`x-opensip-digest-domains.languageModes.map`: ts-* → `typescript`, rust-* → `rust`, `syntax-only` → `syntax`) is **not** fingerprint/subject language.

| Kind | `subjectLanguage` | `logicalPath` | `qualifiedName` | `signatureTokens` |
|---|---|---|---|---|
| file | suffix table: TS universe `bodyLanguageByVariant` (`.js` → `javascript` even under TS engine); Rust → `rust`; syntax **code** grammar `languageId`; syntax **data-document** (`json`/`toml`/`markdown`/`yaml`) → that `languageId`; `unsupported-file` / no grammar → `unspecified` | the snapshot path (= native id) | = path | **must be `[]`** |
| package | unit family: `tsjs` → `javascript` (manifest ecosystem), rust unit → `rust`; not `syntax` | **first-party** `manifestPath` (inventoried) | `packageName` | **must be `[]`** |
| symbol | language of **attributed** first-party path via the same suffix table, not engine | trusted attributed snapshot path ∈ extent | native binding name | native tokens; empty **does not** correspond (identity §3 anonymous unmatched). Detector **projection** is `finding.ruleClosure` (identity §3); enumerator stores tokens, does not choose the fingerprint hash |

File/package empty-token discriminators (`SHA-256(C([]))`) apply **only** when `kind ∈ {file,package}`. They must not make `kind=symbol` with `[]` match. Data-document / unsupported files: inventory-only; a symbol/clone request is `language-tier-unsupported` / `capability-missing` (grammar registry `unavailableRequestDisclosure`), **not** complete-empty `declares`.

External/imported: no inventory row with a fake snapshot path. Targets that resolve into `DependencySourceSet` / `node_modules` layout are **not** policy file/symbol/package candidates. Explicit `attribution=external` is a fact/target concern (G4), not an expected Plan subject.

## 4. Acyclic dependency

```
snapshot + boundaries + scope-descriptor
        │  (pure discover_units / assign_membership)
        ▼
UnitMembershipV1
        │
requestedCapabilities (capabilityId, languageMode, workspaceRoot, required)
plan.semanticClosures ── named enumerator (planning)
        │
        ▼
EnumerationObligationSetV1 + SourceExtentV1     ← Plan-bound; expectedUniverse maybe null
        │
native context admit (optional) → bind_universe (optional) → universe H
        │
provider run (optional fail)
        ▼
EnumerationOutcomeV1  ──complete/partial──► inventory (universe required)
                      ──unavailable──────► no inventory, universe=null
        │
        ▼
subject-scope.subjects ⊆ inventory ids → coverage → view → proofs
RuleEnumeration (GR2) reads obligations+outcomes+inventories, not “scopes that happened”
evaluation-subject = H("evaluation-subject", {universe, nativeSubjectId})  [derived]
```

Proof `evaluationInputRefs`: obligation-set, each outcome, each inventory, membership blob, extents. `proof-bundle.enumerationIds` remain GR2 rule-level results **derived** from these. Verifier recomputes extents and obligation set, then full outcome/inventory/enumeration records. No `expectedFindings`. No replay-by-row-absence.

## 5. Selection / enumeration algorithm

1. Admit analysis-spec ownership tuples (existing duplicate-tuple refusal).
2. Build `UnitMembershipV1`; digest it.
3. For each distinct `(languageMode, workspaceRoot)` among requested rows: name one provider; derive kinds; mint obligations + extents.
4. Admit contexts into `plan.nativeContextDigests` where possible; bind universes where possible; fill `expectedUniverse` only then.
5. Mint Plan (obligations in `analysis-spec.parameters`).
6. For each obligation, retain an outcome. Required + unavailable/partial/unestablished → SUBJECT-D5 `reqUnknown` (not advisory-operator promotion).
7. Policy `U(rule)` = outcomes of obligations whose mode maps to selector domain (`typescript`/`rust`/`syntax`) **and** `state=complete` with a universe. Missing required outcomes do **not** drop out of the expected set; they stay as unknown.
8. Candidates: inventory rows of matching kind in those complete inventories, then globs/export filter (GR2). Zero facts is normal. File totality remains Coverage law, not enumerator substitute.

## 6. Five conceptual cases (not executed)

**E1 — nested two `tsjs` units, one toolchain.** Two `workspaceRoot`s, two obligations, possibly one context and two universe Hs (`entryConfigPath` differs). Omitting the nested unit’s `enumout2:` cannot make `U(rule)` look like a single complete program.

**E2 — required `syntax` cell, compiler crash.** Obligation present, `expectedUniverse=null`, outcome `unavailable`/`provider-fault`, no H. Required → indeterminate. Parallel `inventory` complete-empty or complete files still retain their own outcome. No synthetic symbol predicates.

**E3 — syntax-only Markdown/JSON.** File/package obligations complete (inventory-exempt). Symbol obligation `unavailable`/`language-tier-unsupported` (`syntaxClass=data-document`). Not complete-empty `declares`.

**E4 — `js-allowjs` `.js` file.** Engine `typescript`; `subjectLanguage=javascript`; fingerprint language `javascript`. Treating it as `typescript` is a false key.

**E5 — `node_modules/foo` vs first-party `package.json`.** Layout row is not a package candidate. First-party manifest is. A glob `**/node_modules/**` matches no first-party extent path (pruned). External attribution stays unavailable, not a fabricated snapshot path.

## 7. Schema / major implications (not GR8-complete)

New `$defs` + H domains: `enumeration-obligation-set`, `enumeration-outcome`, `source-extent` (or nested), existing inventory / evaluation-subject. `ProofInputRef.domain` adds those names + `byDomain` rows. Parameter-class registry row for the obligation document. `analysis-spec` **shape unchanged** if carried as a parameter; PlanId still moves because parameter bytes change. `proof-bundle` gains input refs (and GR2 `enumerationIds`). Strict majors: proof-bundle 2→3; new domains at 1. Historical frozen subjects unmigrated.

**Open:** GR6 detector token projection vs enumerator tokens; GR8 public routes for new refusal keys; G3 subjectField; G6 disabled rules (disabled ⇒ no obligation deficiency, as probe assumed); G7 per-universe Coverage; G9 profile gating. Stop.
