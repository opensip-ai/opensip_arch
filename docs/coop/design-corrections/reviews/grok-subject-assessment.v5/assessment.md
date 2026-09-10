I'll pull the exact membership, workspace-root, and provider-route selectors first, then rewrite GR3–GR5 so the cycle, digest, partial, and cardinality blockers are actually fixed.# GR3–GR5 corrected construction (v5)

**Standing.** Bounded coauthor correction of v4. Root blockers accepted. SUBJECT-D1–D6 stand. No source assent. Not G3–G9/GR6/GR8. Examples conceptual.

**Retract.** Parent `analysisSpecDigest`/`planId` inside the parameter; comparing `extentDigest` to `examinedPathsDigest`; `partial ⇒` strict path subset; excluding partial inventories from evaluation; required `enumeratorClosure` plus a null branch; using `PROVIDER.NOT_SELECTED` for “no enumerator”; `disabled rule ⇒ no obligation deficiency`; outcome introducing a context absent from `plan.nativeContextDigests`; one context = one universe; `grammar-only` as a membership value; `workspaceRoot` as `LogicalPath`; file complete-empty over a nonempty extent; data-only extent ⇒ symbol `unavailable`; host-recomputed symbol rows; unit-family language on every file; `maxItems: 1024` as a kind-obligation proof; `canonical-set` as a uniqueness-by-key annotation.

## 1. Pre-Plan parameter (no cycle)

New **separate** schema document (parameter registry keys by **full document bytes**, not a selector into identity-schemas):

`docs/coop/design-corrections/workflows/schemas/enumeration-obligation.schema.json`

`analysis-spec.parameters[]` already uses `payloadDigest` = raw SHA-256 of `C(payload)` with `schemaDigest` = raw SHA-256 of that document (`identity-schemas.v2.json#/$defs/analysis-spec/properties/parameters`). **Representation: raw canonical-record digest, not an H frame.** Do not mint `eobset2:` for the parameter.

**`EnumerationObligationSetV1`** (no parent ids):

```
{ schemaVersion: 1,          // const 1
  snapshotId,                // snapshot2:
  scopeDigest,               // raw C(scope-descriptor), same recipe as plan.scopeDigest
  membershipDigest,          // raw C(UnitMembershipV1)
  cells: [ CellObligationV1, ... ] }
```

`cells`: `maxItems: 1024`, `uniqueItems: true`, `x-opensip-order: {"by":["capabilityId","languageMode","workspaceRoot"]}`. One cell record **per** `requestedCapabilities` row (ownership tuple). That is the cardinality proof: `len(cells) = len(requestedCapabilities) ≤ 1024`. Kinds live **inside** the cell (`kinds` derived from that capability’s matrix relations + `subjectKindLaw`). An `inventory` cell has `kinds: ["file","package"]`; a `syntax` cell has `kinds: ["symbol"]`. Do **not** explode to 3072 top-level rows.

**`CellObligationV1`** (identity = raw SHA-256 `C(row)`; **no self-id field**):

```
{ capabilityId, languageMode, workspaceRoot,
  required,                    // copied from the matching requestedCapabilities row
  kinds: ["file"|"package"|"symbol", ...],   // 1..3, x-opensip-order {"by":[""]} wait: array of enums
  enumerator: EnumeratorRef,
  nativeContextDigest,         // 64-hex | null
  programEntry,                // Text | null  (see §5)
  extent }                     // SourceExtentV1 inlined; also extentDigest = raw C(extent)
```

`kinds` order: `x-opensip-order: {"by":[]}` is wrong. Use `x-opensip-order: "canonical-set"` **on the kinds array only** (whole-item UTF-8 of each enum string). Cell array uses `{"by":[...]}` as above.

**`EnumeratorRef`** (closed):

```
oneOf:
  { "selected": true,  "closureId": "closure2:<64 hex>" }
  { "selected": false, "reason": "optional-unselected" }
```

`required=true` ∧ `selected=false` → **Plan admission refusal**, not unknown evidence. Optional cell with `selected=false` is well-formed unavailable (disclose). `selected=true` ⇒ `closureId` ∈ `plan.semanticClosures` and `closureKinds` `provider` (`identity-schemas.v2.json#/x-opensip-digest-domains/closureKinds/byField` subject-scope.enumeratorClosure). Extra closures do not enumerate.

**Do not** route missing enumerator as `PROVIDER.NOT_SELECTED`. That public detail is only `native-evidence.schemas.v2.json#/x-opensip-public-route-registry/keys/native.requested-capability-mode-not-selected`: well-formed request for a matrix **NOT-SELECTED** cell; class `request-rejected`, `REQUEST.UNSATISFIABLE`, `domainDetail: PROVIDER.NOT_SELECTED`. A NOT-SELECTED cell is refused at `admit_requested_capabilities` and **mints no obligation**. A SUPPORTED-DESIGN required cell with no selected provider is a host planning fault (existing host-invariant / `REQUEST.PRECONDITION_FAILED` family — exact GR8 row still open). Interpreter/protocol crash after spawn remains operational (`PROVIDER.PROTOCOL_VIOLATION`); it is **not** rewritten as enumeration unknown.

**`workspaceRoot`:** same `#/$defs/Text` as `analysis-spec.requestedCapabilities[].workspaceRoot`. May be `.` (`native-evidence.md` §1.4 `normalize_explicit_root`). Not `LogicalPath` (which forbids `.`).

**`SourceExtentV1`:** `{ workspaceRoot, languageMode, programEntry, paths }` with `paths` `maxItems: 100000`, `x-opensip-order: "canonical-set"`. Paths are snapshot `LogicalPath`s except the root token `.` is not in `paths`.

Membership filter uses **exact** `FileMembershipRowV1` (`native-evidence.schemas.v2.json#/$defs/FileMembershipRowV1`):

- `membership ∈ {program-member, syntax-only, unsupported-file, outside-project-boundary}`
- `reason ∈ {deepest-unit-in-language, no-program-unit-for-language, grammar-only, no-bundled-grammar, host-ignore-convention, nested-repository, nested-project, custody-excluded}`

Compiler-mode file/package/symbol extents: `membership=program-member`. Syntax inventory: include `syntax-only` (reasons `grammar-only` **or** `no-program-unit-for-language`) plus `unsupported-file` (`no-bundled-grammar`) — inventory is not grammar-gated. `host-ignore-convention` is a **reason** on `syntax-only` rows, not a membership. `outside-project-boundary` never enters extent.

**Closure equality (not hashed into the parameter):** `snapshotId = plan.snapshotId`; `scopeDigest = plan.scopeDigest`; `membershipDigest = C(retained UnitMembershipV1)`; each cell ownership tuple equals exactly one `requestedCapabilities` row including `required`; selected `closureId` ∈ `plan.semanticClosures`; if `nativeContextDigest ≠ null` it ∈ `plan.nativeContextDigests`.

## 2. Context, program key, universes

U-1 yields **one `tsjs` unit per directory** (marker precedence `tsconfig.json` > `jsconfig.json` > `package.json`). It does **not** enumerate `tsconfig.build.json` or extra solution projects.

**Program key (explicit, limited):** `(languageMode, workspaceRoot, programEntry)` where `programEntry` is `null` for U-1 default (synthesized or the precedence marker) or an inventoried config path **only if a requested cell names it**. Extra configs without a cell are out of scope, not silently expected.

One context may still back several universes. Outcome universe must join **this cell’s** selected context (if non-null) **and** this `programEntry`+extent. Sharing `nativeContextId` is not identity.

**Context lifecycle:** `nativeContextDigest` is fixed at Plan. `null` means the unavailable-only path (context admission failed **before** Plan, obligation still records null). Outcome **must not** introduce a context absent from `plan.nativeContextDigests`. A different context is a new Plan. `expectedUniverse` may be null until bind succeeds; a complete outcome’s `universe` must re-bind against the **selected** context + planned program/extent, or refuse.

## 3. Outcome, partials, file totality

**`EnumerationOutcomeV1`** (Run output, not Plan): raw `C` digest cited from `ProofInputRef` (new domain; GR8 majors open).

```
{ schemaVersion: 1,
  cellDigest,                  // raw C(CellObligationV1)
  enumerator,                  // must equal cell.enumerator
  nativeContextDigest,         // equal cell; no late introduce
  universe,                    // 64-hex | null
  state: complete | partial | unavailable,
  unavailableCause,            // null | typed native cause already in DeficiencyV2 / NativeCause
  inventories: [{ kind, inventoryDigest }],  // 0..len(kinds)
  examinedPaths }              // LogicalPath[], same grammar as extent.paths, canonical-set
```

**Compare path sets, not mixed digests.** Host parses `extent.paths` and `examinedPaths`. Every examined path must be ∈ extent. **Do not** require `examined ⊂ extent` for `partial` (timeout inside the last visited file can leave `examined == extent`). `partial` is a **provider attestation**, not a set-inequality.

**SUBJECT-D4:** rows in a **partial** inventory **still evaluate**. Unseen population stays unknown on the GR2 enumeration record. Do not drop partial inventories from the candidate set.

**Complete file:** `state=complete` for `kind=file` is lawful empty **only if `extent.paths` is empty**. Nonempty extent ⇒ inventory has a row for **every** extent path (host-checkable totality, same spirit as `coverageTotality` for `file@enumerated`). Omission ⇒ refuse exhaustive claim, not complete-empty.

**Complete package/symbol:** empty rows may be legitimate. **Data-only** program-member extent (JSON/Markdown under a code grammar request for `syntax`/`declares`): zero applicable symbols ⇒ **complete-empty symbol enumeration**. A requested **semantic** cell (`references`, `calls`, …) keeps its **own** sufficiency (`language-tier-unsupported` / `capability-missing` per grammar registry). Do not force symbol-enum `unavailable` merely because data has no declarations.

**Unavailable vs operational:** `state=unavailable` is well-formed unsupported/incomplete **evidence** (typed cause). Provider protocol/crash/invalid bytes: existing operational/admission law; **no** authoritative Run where that law already says so. Do not erase into unknown.

Pointer/bytes: SUBJECT-D6 unchanged (omitted required pointer structural; lost bytes retention; bad hash admission).

## 4. Trust / what host recomputes

| Host recomputes (no compiler) | Provider-attested (trusted, retained) |
|---|---|
| Obligation set, extents, membership, Plan joins, GR2 rule enumeration | Inventory **rows** (symbols/packages/export tri-state, attributed paths, tokens) |
| File exhaustive claim vs extent path set; package `manifestPath` ∈ snapshot; language/suffix table; enumerator/context equality | `examinedPaths` as the actual examined set; `partial`/`complete` for **symbol extraction** |

Host **cannot** recompute native extraction or the true examined set. Do not call symbol inventories host-verified. Complete claims bind whole `kinds`+program+extent; file totality is independently checked; symbol completeness is attested against that bound, not re-derived.

## 5. Language, packages, tokens

**Subject language = language of `logicalPath` via closed suffix tables**, never “Rust unit ⇒ rust on Cargo.toml”.

1. Longest suffix in `x-opensip-grammar-capability-registry.languages` → that `languageId` (`Cargo.toml` → `toml`; `.rs` → `rust`; `.js` → `javascript` even in a TS engine universe).
2. Else suffix in a closed **unbundled-extension** table in that **same** document (known language, `unsupported-file`) → that token.
3. Else `unspecified`.

Adding a suffix is a registry change. Engine language stays on the universe domain, not the fingerprint.

**Package fingerprint language:** manifest **format** language (same table: `package.json` → `json`, `Cargo.toml` → `toml`), not ecosystem (`javascript`/`rust`). Unit `languageFamily` is not `finding-fingerprint.subjectKey.language`.

No fake snapshot paths for `node_modules` / dependency-source-set packages.

**Tokens:** inventory stores enumerator tokens only. Fingerprint discriminator uses the **finding’s** `ruleClosure` projection (`identity-schemas.v2.json#/$defs/finding/properties/ruleClosure`; identity §3). Multiple detectors over one inventory ⇒ each finding names its own `ruleClosure`; reconstruction must not pick “the inventory’s detector.” File/package `signatureTokens=[]` only for those kinds (GR6 still owns anonymous symbols).

## 6. Selection → output cardinality

`requestedCapabilities` n ≤ 1024 → n cell obligations. Each cell produces **one** outcome. Each `kind` on a complete/partial outcome produces **one** inventory (empty inventory still a record). `required` follows the **capability cell**, independent of whether any policy rule is disabled (retract v4 G6 sentence). Probe “disabled rule has no enumeration deficiency” applies only to **that rule’s** GR2 row; `required` execution/coverage on the cell remains.

`U(rule)` = inventories whose cell mode maps to the selector domain **and** whose outcome is `complete` **or `partial`**. Required `unavailable` / missing outcome stays in the expected set as unknown (does not shrink).

## 7. Four conceptual examples

**C1 — cycle gone.** Parameter omits `analysisSpecDigest`; closure still checks equality to the parent spec. Hashing the set cannot require the spec that hashes the set.

**C2 — partial last-file timeout.** `examined == extent`, `state=partial`, 3 known symbols. Those three evaluate; GR2 keeps unknown remainder. Excluding the inventory would hide true findings (SUBJECT-D4/D5).

**C3 — two TS programs, one context.** U-1 default: one cell, `programEntry=null`. A second `tsconfig.build.json` is **not** expected unless a second requested cell names it. An outcome universe for the unselected entry is refused even if `nativeContextId` matches.

**C4 — data files + `syntax` + `references`.** Symbol enum **complete-empty**. `references` cell remains `language-tier-unsupported`. File inventory complete over those paths (nonempty ⇒ not file-empty). Markdown language `markdown`, not `syntax`.

Atom/import/majors/public routes remain separate. Stop.
