# OpenSIP DR-011-R10 — blind consumer-B reconstruction review

**Verdict: CHANGES_REQUIRED** — 2 unresolved MUST issues, 2 unresolved SHOULD issues,
4 nonblocking advisories. Everything else in the brief reconstructed and closed.

This is a design-reference reconstruction only. It is **not** product qualification and
**not** implementation authorization. Every OS, compiler, provider, filesystem and
cryptographic observation below is a **synthetic trusted observation** — an assumption,
never native enforcement proof. No compiler, cargo, provider, repository, ledger or
renderer was executed.

---

## 1. Input custody and hash verification

`consumer-input-manifest.json` declares 45 files as an exact subset of the accepted parent
subject `5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f`.

| Check | Result |
|---|---|
| Files declared | 45 |
| SHA-256 + byte length verified | **45 / 45 OK** |
| Files on disk not in the manifest | none |
| Manifest entries missing on disk | none |

Retained at `output/vectors/input-verification.json` (per-file digests).

I read **only** the kit. I did not open the original repository, any author Python/TypeScript
reference model, fixtures, cases, goldens, reports, prior reviews, or any other
`/tmp/opensip-design-corrections` directory. Historical/review links inside inherited
normative documents were treated as provenance and not followed.

**Method.** I wrote my own canonical encoder `C`, the `H` frame, the CVE1 encoder, the
FACT-IDENTITY body frame and a `close_run` admission from the contract **prose plus the
machine-readable registries in the kit**, then built descriptor graphs and computed every
identity myself. Schema validation uses the kit's own schemas through a pinned local
closure (no network). Sources: `output/ref/`; outputs: `output/vectors/`.

One consistency observation, clearly separated from my own vectors: after implementing
CVE1 from `resolved-inputs.v2.json#planIdContract.canonicalValueEncoding` I recomputed
`capabilityManifestId` from the *embedded* `delivery.v4.json` DCM-1 committed byte string
and got the embedded value. That tests my reading of the prose; the embedded example is
**not** used as an oracle for any vector I designed — every designed vector's expected
value is computed by my own helper from my own inputs.

---

## 2. Reconstruction of the chain

### 2.1 Zero-config discovery → typed config/source

* **Discovery boundary and custody** are the security unit's
  (`security-and-lifecycle.md` §S3): `O_NOFOLLOW` handles, directory/file custody, the
  walk rule, and **nested config as a deliberate project boundary** (ADV-3). The selected
  root yields one ProjectId, one custody domain, one lease namespace.
* **One shared discovery rule** (`security` §S3 "One shared discovery rule"; native §1.4
  U-4a) prunes by **exact path segment**: `node_modules`, `.git/.hg/.svn/.jj`, and a
  `target` segment whose parent holds `Cargo.toml`. Security exports
  `AdmittedBoundaryInventoryV1` and native **consumes** it (native §1.4 U-8); native never
  re-derives a boundary from caller input.
* **Units are per language family and program membership** (native §1.4 U-1…U-8). A root
  holding both `Cargo.toml` and `package.json` yields **two** units at one `rootPath`.
* **Typed configuration** is `foundation/product-configuration.schema.v2.json` resolved by
  `admission-and-qualification` §1.1 into the closed
  `identity-schemas.v2#/$defs/semantic-configuration` — all five sections always present,
  an empty section exactly `{}`. `resolvedConfigDigest` = raw SHA-256 of `C` of that record.
* **Source** becomes `snapshot2` = `H("snapshot", {projectId, sourceInventory,
  resolvedConfigDigest, scopeDigest, vcsDigest})`. `node_modules` rows are **not** inventory
  rows; the resolver read set is the retained `ResolvedNodeModulesLayoutV1` joined by
  digest (native §2.2).

### 2.2 Invocation / step / attempt lifecycle

`workflows-and-surfaces.md` §1. Invocation = one host request, `RequestId` minted before
admission and retained for refusal; ≤ 64 ordered acyclic steps; `StepId` = zero-based
position; ≤ 3 attempts, each a fresh `ExecutionId`. Only `analysis` and `verify` seal or
link a `run2`. The **step DAG and the derivation DAG are distinct** — each analysis/verify
attempt owns exactly one `exec-plan2` (≤ 1024 stages) through `DerivationBinding`; a step
never depends on a stage.

**Semantic identity vs operational authority.** `RequestId`, `ExecutionId`, receipts, wall
clocks, PIDs, credentials, nonces and output destinations are operational and appear in
**no** semantic descriptor — I verified this mechanically across the ten identity-bearing
records (`vectors/identity-mutation.json`). Identical semantic inputs on two attempts
produce the same Run; attempts stay separately auditable.

**Mutation vs analysis steps.** `comparison`, `query`, `render`, `import`,
`repair-preview`, `repair-apply`, `test-execution`, `native-preparation`, `mutation`,
`export-delivery`, `doctor` mint no Run.

### 2.3 Analysis Plan

`plan2` binds snapshot, capability manifest (id **and** bytes digest), semantic closures,
analysis-spec digest, resolved-config digest, `nativeContextDigests` (a **canonical set** of
bare 64-hex `h-identity` suffixes), imports, policy, waivers, scope, budget and semantic
grant. Verified joins in my closure: `plan.budget` must equal
`config.analysis.budget` exactly and by type; the analysis spec's capability vocabulary is
re-closed against `native-capability-matrix.v2.json#/capabilities[].id` over the **retained**
spec; every analysis-spec parameter must cite a document on the closed
`x-opensip-payload-registry.classes.parameter` list.

### 2.4 Native facts / Coverage / view

* A universe binds a context **of its own language**, and Run closure **re-runs the owning
  contract's own admission** over the retained bytes (`admit_native_context`,
  `bind_typescript_universe` / `bind_rust_universe` / `bind_syntax_universe`). A frame proves
  retention, never admission.
* `plan.nativeContextDigests` must equal the retained context frame set **exactly**; every
  universe's `nativeContextId` must be a member.
* Facts: relation registered; `payloadSchemaDigest` = the relation document's own file
  digest; rung a member of **that relation's** ladder; the rung's required/forbidden fields;
  `universeRule: same-only`; the closed `anchorLaw` (source-text ≥ 1, body-identity = 1,
  inventory = 0); the per-relation `snapshotJoins`.
* Coverage: minted only at the producer boundary (`admit_coverage_result_v3`) from the
  **host's own** enumeration — `subjectScopeCommitment` is the identical digest to the
  `scope2` the host mints, re-spelled `sha256:`; the provider never supplies it. RC-1/RC-2
  and the `x-opensip-deficiency-cause-registry` are enforced, and re-enforced at closure.
* Views: fact/scope join is **existential**; `coverageTotality` for `file@enumerated`
  matches on **all five** coordinates including both universes.

### 2.5 Proof verification → Evidence / Seal / Run

The graph is acyclic: proof carries no evidence/seal/Run identity; evidence may include
proof; seal includes both; Run includes seal. I verified: the compiled `RuleProgramV1` is
exactly the projection of the Plan-selected policy's rules in `ruleId` order; every atom's
`minResolution` is a member of *that atom's relation's* ladder, checked over **both** the
policy and the compiled program; `program-predicate` node addressing (`p`, `a.i`, `a.0`) is
total and deterministic and the witness's `childPredicateIds` are exactly the addressed
node's operand addresses; `countLimit` is the node's `n` for `count-at-most` and null
otherwise; predicate input refs ⊆ `evaluationInputRefs`; evidence view roots equal the named
views and coverage roots equal their union; `coverage-payload`/`import-payload`/`fact-payload`
are refused as authoritative proof roots.

### 2.6 Durable receipt and current availability

Sealed assurance (`verified` / `verifiable` / `replayable`) is immutable; **current
availability** is a separate monotonic-generation record (retained / partial / expired /
purged / corrupt / unavailable). A query reports both. Commit order is 4-phase; a failure
before step 3 publishes no authoritative Run; a crash after ledger commit but before
acknowledgement is `durability-undetermined`, exit 4. Regeneration mismatch is
`HOST.IO_FAILURE` / `evidence.regeneration-mismatch` and **cannot replace the sealed Run**
(vector emitted and schema-validated).

### 2.7 Who owns every decision

| Decision | Owner |
|---|---|
| Repository root, custody, boundary inventory, trust time, revocation, platform admission, leases | security (`security-and-lifecycle.md` S3/S4/S6/S7/S8) |
| Exact numeric/lexical admission, configuration resolution, report custody | admission-and-qualification §1/§2/§3 |
| `C`, `H`, the digest law, payload registry, retention, purge, replay | identity-and-evidence §3/§5 |
| Language units, universes, contexts, facts, Coverage, deficiency/cause, grammar capability | native-evidence §1/§2/§4/§10/§11 |
| Invocation, steps, attempts, comparison, imports, policy DSL, repair, output/parity, D9 projection | workflows-and-surfaces §1–§12 |
| D9 class / code / exit legality | host-owned, `d9-exit-contract.v1.14.json` retained unchanged |
| Capability id vocabulary | `native-capability-matrix.v2.json#/capabilityIdLaw` |
| Relation ladders (single authority) | `relation-payload-schemas.v2.json#/x-opensip-relation-registry` |
| Public detail vocabulary | `public-detail-registry.v1.json` (mirrored by `common#/$defs/DomainDetailCode`) |

---

## 3. Vectors and results

29 scenario groups, 8 fully closed Run graphs through my own `close_run`, 58 negative
probes. All outputs in `output/vectors/`; `_summary.json` reports zero scenario errors.

### 3.1 Canonicalization and identity (`canonicalization`, `digest-law`, `identity-mutation`)

Independently authored `C` vectors with byte strings and digests: UTF-8 byte key order
(including a non-BMP key), integer boundaries `[-2^63, 2^64-1]`, booleans distinct from
integers, the exact escape set (`\b\t\n\f\r`, lowercase `\u00xx`, slash **not** escaped,
U+007F and U+2028 unescaped), no Unicode normalization, arrays in admitted order.

Refusals (all fired): duplicate key, `1.0`, `1e0`, `-0`, `NaN`, integer above `2^64-1`,
integer below `-2^63`, lone surrogate, malformed UTF-8, depth 33 (depth 32 admits — the root
container counts as 1).

`H` frames emitted with full hex for three domains, showing `H(D,X) ≠ SHA256(C(X))` and the
three admitted spellings (typed prefix / `sha256:` / bare suffix) of **one** digest.

Digest law asserted mechanically: **no** 64-hex field of `identity-schemas.v2.json` lacks an
`x-opensip-digest` annotation (the two hits are the terminal scalar *definitions* `Hash` and
`DigestHex`, which the relation document's law explicitly says must not carry a blanket
default). Every `Ref`/`ProofInputRef`/`FindingEvidenceRef` `domain` enum member is registered
in `byDomain`.

Identity mutation: every semantic field of `subject-scope` moves the identity; no operational
field appears in any of the ten semantic records.

### 3.2 Capability manifest (`capability-manifest`, `native-h-preimages`)

Own `CapabilityManifestV1`, own CVE1 committed bytes (length + digest emitted), own
`capabilityManifestId` under
`SHA-256(UTF8("opensip.capability-manifest.v1") ‖ 0x00 ‖ committedBytes)`; a single-field
mutation moves it. CVE1 refuses floats and non-NFC text; it is **total** on booleans and
strings, which is exactly why ADM-TYPE is a gate *before* encoding — a respelled
`schemaVersion` mints a different, well-formed id rather than failing.

Native H preimages reconstructed from the recipes for
`native.dependency-source-set.v1`, `native.dependency-file-manifest.v1`,
`native.unified-features.rust.v1`, `native.cargo-config-projection.v2`,
`native.source-unit-ownership.v1` and `native.compilation-unit.v1`, each with frame length,
frame prefix bytes and both spellings. The three Cargo digests are shown **pairwise
distinct**: `CargoConfigProjectionV2.projectionSha256` (raw digest of the projected *file*),
`rust-v2.configProjectionSha256` (bare suffix of `H` over the whole *record*), and raw
`SHA-256(C(record))` — none substitutes for another.

### 3.3 TypeScript / JavaScript (5 closed Runs, 18 negatives)

| Vector | What it exercises |
|---|---|
| `ts-ordinary` | An ordinary TS project that reads `node_modules` and resolves bare specifiers: retained `TypeScriptConfigGraphV1`, retained `ResolvedNodeModulesLayoutV1` (**not** inventory rows), lockfile join, zero-anchor inventory facts for every path, an RC-3 honest `references` entry (`coverage: complete`, `state: incomplete`, no deficiency, `nativeCause: null` by design) with its admitted `unresolved-edge` fact, and **three** clone facts |
| `ts-synthesized` | `js-synthesized`: `configOrigin` **derived** (entry null and nodes empty), `nodeModulesInReadSet=false` so every bare specifier is an `unresolved-module-specifier` edge — never an implicit install |
| `ts-custom-named-multi-base` | An explicitly selected **custom-named** config (`tsconfig.build.json`, entry kind `other` → derived `configOrigin: tsconfig`) extending **three ordered bases including a repeated one**; dropping the repetition changes `tsconfigGraphHash` **and** the universe identity |
| `ts-jsconfig-shared-base` | `jsconfig.json` extending `shared/common.settings.json` (kind `other`): a jsconfig entry extending a shared base under another filename **remains a jsconfig program**; asserting `configOrigin: tsconfig` refuses |
| `ts-two-contexts-one-plan` | **Two TypeScript contexts under one Plan** (ordinary, not exceptional). Nothing elects one by position: a fact's `sourceUniverse` names its own `nativeContextId`. Negative: dropping the second universe's own `file` fact refuses `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` even though the remaining fact satisfies the *existential* view join — totality matches on all five coordinates |

**Body language vs provider identity.** In `ts-ordinary` the identical byte span in
`src/a.ts` and `src/legacy.js` under **one** TypeScript engine universe mints **different**
`bodyIdentity` values, because `languageId` is derived from
`languageVersionBinding.bodyLanguageByVariant[<longest suffix match>]`
(`ts → typescript`, `js → javascript`) and **never** from the universe row's `language`
field. The same body at `L1-lexical` mints a third identity.

**Custody at L0 vs L1.** At `L0-verbatim` I recompute the payload from the fact's own anchor
span — a real source join. At `L1` I check retained preimage custody plus the framed-identity
check and well-formed token-stream framing, and grade no tokenisation.

Negatives (all fired): compiler version not from the manifest; tool digest outside the named
closure tree; incomplete stdlib declaration inventory; stdlib merkle root naming no retained
closure; config-graph path outside the snapshot; a Rust context offered as the TypeScript
context; a universe bound **without** the retained config graph; context bytes that are not
the admitted ones; a retained layout no context selected; a raw canonical payload offered
where an `h-identity` frame is required (`FRAME_PREFIX`); an unregistered H domain in a frame;
a missing preimage; a hidden context frame no Plan reached; an **unanchored code fact under a
TypeScript universe**; an **inventory fact carrying an anchor**; a `file` payload claiming a
wrong content hash; a rung of another relation; an unlisted source-variant suffix.

### 3.4 Rust (1 closed Run + 6 constructed universes, 14 + 15 negatives)

Workspace: `crates/core` (package edition 2021) with a **test target overriding to 2018**,
`crates/legacy` (2015), and `tools/#gen` (2024) — a **valid `#` marker directory**, admitted
without narrowing the canonical path grammar. `SourceUnitOwnershipV1` commits the units table,
the explicit `selectedUnitIds` and the pure `{path, unitId}` relation; every `unitId` is
**re-derived** at admission from `H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion,
markerPath, targetKind, targetName})`.

* **Mixed edition in ONE universe:** bodies at 2021, 2015 and 2024 all admissible, each with
  its own dialect. The bounded version component is derived from the **admitted compiler
  context**: `compilerName` const `rustc`, `compilerVersion` ← `toolchain.rustcVersion`,
  `compilerBuild` ← `toolchain.rustCommitHash`, and the dialect from the selected target's
  effective edition. `languageVersion` is the **raw 32 bytes** of `SHA-256(C(body-language-version))`.
* **Representative large edition map:** 21 crates, `C(edition)` = 650 bytes — well past the
  inherited `u8` component length of 255, which is exactly why the map is hashed rather than
  embedded and why the fixed-width treatment is not a convenience.
* **Same physical path, two selections:** `crates/core/src/shared.rs` under selection
  `{lib@2021, legacy, gen}` and under selection `{test@2018}` gives two **different
  universes** and two **different body identities** — two analyses, not two readings of one.
* **Stable body identity when only the selection changes:** dropping `gen` from the selection
  changes the `sourceUniverse` but **not** `crates/core/src/lib.rs`'s `bodyIdentity`, because
  its effective dialect is unchanged.
* **Ownership deficiencies, derived and enforced.** For each of no committed ownership,
  `enumeration: partial` (refused **before any row is read**) and disagreeing selected owners,
  the selection law refuses per body and the clones Coverage carries the **derived** pair
  `input-closure-incomplete` + `body-language-ownership-missing` /
  `body-language-owner-unenumerated` / `body-language-owner-ambiguous`. The empty clone view
  is `unknown`, never a `complete` finding of no clones. Four distinct refusals keep the faults
  separable: `COVERAGE_DIALECT_PREREQUISITE` (false `complete`),
  `COVERAGE_DIALECT_UNDISCLOSED` (null deficiency),
  `COVERAGE_DIALECT_DEFICIENCY_MISMATCH` (unrelated deficiency),
  `COVERAGE_DIALECT_CAUSE_MISMATCH` (a schema-valid but wrong cause — the cause registry alone
  admits it; only the **derived** pair refuses it).
* **Public projection:** indeterminate (3), `VERDICT.INDETERMINATE`, cause as typed detail in
  the `coverage2` record the termination names by `coverageId`; the deficiency
  `input-closure-incomplete` is itself a registered `DomainDetailCode`.

Rust negatives (all fired): rustc version not from the manifest; `rustcDevLlvmDigest` naming no
retained closure; replaced config path outside the snapshot; crate root outside the snapshot;
lockfile bytes differing; a `cfgSet` dropping a base cfg; `configProjectionSha256` mismatch;
`executionCapableResolution` without prepared products; unified features for another target
triple; a prepared set retained but unselected; a `unitId` not derived from its own row; a
selection naming an undeclared unit; an ownership path outside the snapshot; and a
**nearest-directory ownership inference** (`BODY_LANGUAGE_OWNER_NOT_COMPILED` — rows must match
the anchor path by **equality**).

### 3.5 Compiler-free syntax-only (2 closed Runs, 13 negatives)

* **Code grammar Run** (`javascript` + `markdown` selected): inventory facts for every path
  including `tool/main.py`, plus `declares@syntactic` and `clones@normalized-body-hash` facts
  anchored in `src/app.js`. The context carries **exactly** `{schemaVersion, grammarBundle}` —
  no toolchain, no stdlib, no lockfile, no config graph — and `parserVersion` is joined to the
  `kind=grammar` closure manifest's `semanticVersion` exactly as a compiler version is.
  `references@resolved-binding` is **disclosed unavailable**: `coverage: unknown`,
  `language-tier-unsupported`, `capability-missing`.
* **Data/document-only repository with no TypeScript and no Rust compilation unit**
  (`json`/`toml`/`markdown`/`yaml` selected): inventory and `package@manifest-declared` are
  available and **not grammar-gated** — `tool/main.py`, which has no bundled grammar, is still
  inventoried. Every code capability and every semantic rung is unavailable-and-disclosed with
  the same pair. A **complete empty clones result refuses**
  (`SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`) rather than reading as a finding of no clones.
* **Code-vs-data verified against the published matrix**: I read
  `native-capability-matrix.v2.json` cells for `syntax-only` (inventory/syntax/clones-fact/
  clones-near `SUPPORTED-DESIGN`; imports/references/calls/types/reachability/unresolved-edge
  `UNSUPPORTED-TYPED` with `language-tier-unsupported`; `clones-cross-tsjs` `NOT-SELECTED`) and
  against the body/normalizer laws: the syntax dialect table contains **no** data-format suffix,
  so a data grammar can mint no body identity
  (`BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN` on `data/records.json`).
* **Unsupported grammar without assuming a TypeScript compiler:** `.py` has no bundled
  grammar; a code fact anchored there refuses, and `body_language_version` refuses. The path is
  still inventoried — `unsupported-file / no-bundled-grammar` is an honest classification, not
  an erasure.
* **Grammar parse ≠ compiler parse:** the identical `src/app.js` body bytes mint different
  identities under `native.semantic-universe.syntax.v2` (`grammarVariant`) and under a
  TypeScript engine universe (`sourceVariant`). Required, not incidental.
* Negatives: a Markdown-anchored code fact; an unbundled-grammar-anchored code fact; a false
  `complete` for an unavailable capability; a wrong cause; an unselected grammar lending a
  capability; a selection naming a grammar outside the bundle; a data grammar declaring `code`;
  a code grammar demoted to `data-document`; a grammar claiming another language's suffix; a
  parser version not from the grammar closure manifest.

### 3.6 Minimum-resolution predicates and the imported-observation boundary

Per-relation ladder-index comparison at **syntactic**, **resolved** and **type** levels, with
qualifying and insufficient facts for `declares`, `imports`, `references`, `calls`, `types`.
There is **no global rank**: `resolved` names a different rung in each of `imports`,
`references`, `calls` and `reachability`. A rung of another relation is a **refusal**, not a
weaker value.

`sufficiency_v2` reproduced in order with **no early exit**: a universal negative over an
`incomplete` resolution state yields `resolution-incomplete`; over `exportsClosed ≠ closed`
yields `external-consumers-unknown`; the **confidence floor precedes** the one-rung existential
shortcut (`clones` at 100000 under a floor of 900000 → `confidence-floor-unmet`); a
`declared-only` derivation policy over `compiler-inferred` yields `derivation-policy-unmet`; a
relation absent from the view yields `required-relation-missing`.

Repair evidence requirements built and validated both satisfied and unsatisfied. The imported
boundary: the two closed evidence relations (`runtime-observation`, `history-change`), each with
the one-rung ladder `[observed]` and **no new rung token**; an evidence atom must declare its
kind and a native-fact atom must not; a runtime payload validated **through the registry row**,
with a hit count on an `unobservable` subject refused.

### 3.7 Imports

One `import2` wrapper with every auxiliary digest computed as raw SHA-256 of the canonical
closed record; `importId = "import2:" + H("import", wrapper)` is the **only** H-domain identity
in an import. `blobs: []` demonstrated lawful (0..4096). The foundation record and its workflow
mirror agree in both directions on an instance sitting on a boundary they once disagreed about
— but **only once `x-opensip-order` is enforced**: a stock JSON-Schema validator admits both,
because the order is an annotation an admission implementation must apply. I implemented the
full closed order vocabulary to make that differential discriminating. The staleness table and
the `IMPORT.STALE_FOR_PLAN` / `IMPORT.MAPPING_REQUIRED` terminations are emitted.

### 3.8 Zero-config selection with an incomplete release

Three discovered units (`.` ts-tsconfig, `services/api` rust-cargo, `docs` syntax-only). The
default profile is **fixed by the matrix, not by the release**: 11 requests per TypeScript
unit, 10 per Rust unit, 10 per syntax-only unit — 31 rows for all three, including every
`UNSUPPORTED-TYPED` cell, excluding only `NOT-SELECTED`. An installed release declaring a
subset (no `reachability`, no `unresolved-edge`, no `clones-near`, no `clones-cross-tsjs`)
does **not** narrow the request.

The **original invocation** discloses the absences on `CommandEnvelope.availability`:

* record `CapabilityAvailabilityV1 = {stepCount, totalNoticeCount, steps[≤64]}`, each step
  `{stepId, noticeCount, notices[≤1024]}`;
* each notice carries the **complete ownership tuple in typed fields** — `capabilityId`,
  `languageMode`, `workspaceRoot` — never concatenated into `subject`;
* `code` is the **const** `native.capability-unavailable`;
* order is the selection's own (`x-opensip-order: sequence`);
* a step that made no selection contributes **no entry**; a step that selected and found
  nothing absent contributes an **empty** entry.

I emitted a **single-step** command (`opensip`, steps `analysis` + `render`) and a **named
multi-step** invocation with different selections at different analysis steps (step 0: the root
TypeScript unit → 4 notices; step 2: all three units → 17 notices; 21 total across 2 entries,
which one flat 1024 array would still admit but which the per-step composition makes exact).
`capability-availability` is a **declared parity field of every `requestClass: analysis`
command** — verified against `command-inventory.v1.json` for `default`, `analyze`, `fit`,
`audit`, `repair-verify` — so every applicable renderer (human/JSON/SARIF/HTML/agent, per each
command's declared `formats`) carries it.

**Product promise vs installed availability vs override vs prerequisite.** A capability can be
undeclared **and** unservable at once (`references` under `syntax-only`); §10's precedence ranks
`language-tier-unsupported` ahead of `provider-unavailable`, so the more specific pair wins and
the release-absence account never overrides it. **Candidate-only** capabilities
(`clones-near`, `clones-cross-tsjs`) have empty matrix `relations`, mint no fact and **no
Coverage entry at all** — the advisory notice is their *only* public route. An explicit
`analysis.capabilities` override changes the **request**, not the obligation, and carries its
own provenance against the default's `DEFAULTED`.

**Bounded cardinality arithmetic verified exactly as native §14 claims:** 11 capabilities per
TypeScript unit, 10 per Rust unit; 93 units → 1023 rows (fits), 94 → 1034 (refuses
`PROJECT.SCOPE_LIMIT` / `REQUEST.UNSATISFIABLE`, exit 2, subject `field:count>limit`, without
truncation). The scope-descriptor `workspaceRoots` bound of 1024 is the effective scope limit
against discovery's 4096 first-party unit cap.

### 3.9 Public terminations and failure envelopes

Six **complete** `kind=failure` `CommandEnvelope` documents, each schema-validated against
`command-envelope.schema.json` (not a termination fragment), derived from a real internal
decision key **plus its originating boundary**:

| Origin | Class / exit | errorCode | `termination.domainDetail` | `errors[0].code` |
|---|---|---|---|---|
| External configuration | request-rejected 2 | `CONFIG.INVALID` | `CONFIG.INVALID` | `CONFIG.INVALID` |
| Retained externally-supplied spec | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | absent (lawful) | `native.capability-spec-invalid` |
| Host-generated invalid internal record | **operational-failed 4** | `SYSTEM.OUTCOME.ILLEGAL_STATE` (`faultCause: host-invariant`) | absent | `HOST.INVARIANT_VIOLATED` |
| Producer boundary | operational-failed 4 | `PROVIDER.PROTOCOL_VIOLATION` (`provider-protocol`) | absent | `native.coverage-cause-unsupported` |
| `NOT-SELECTED` cell (origin-independent) | request-rejected 2 | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED` | `PROVIDER.NOT_SELECTED` |
| Authenticated release declaration | request-rejected 2 | `REQUEST.PRECONDITION_FAILED` | absent | `native.release-declaration-invalid` |

`normalize_internal_key` matches the **longest registered key followed by a colon**; an
unregistered key refuses (`native.public-route-key-unregistered`) and an origin a key cannot
have refuses (`native.public-route-origin-not-possible`). `bounded_subject` elides in **Unicode
code points** with a UTF-8 SHA-256 digest: a 4142-code-point subject becomes exactly 1024 with
the registered key preserved verbatim and class/code/origin unchanged.

**D9 extension checked against the inherited contract.** The inherited
`d9-exit-contract.v1.14.json` declares 11 `faultCause` members; the product declares 12. The
single added member `host-invariant` maps to `SYSTEM.OUTCOME.ILLEGAL_STATE`, which is already in
the inherited **closed** `codeVocabulary.errorCodes` and has **no** preimage in the inherited
`faultCauseToErrorCode`, so `codeMaps.rule`'s "total and injective" over the declared cause
domain is preserved. `classToExitCode` and the error-code set are byte-identical. The declared
precedence `["faultCause", "rejectionCause", "deficiency"]` matches the product's "a required
operational fault dominates a committed failing Run". The product's own statement — that this
*is* a vocabulary extension and that the inherited artifact keeps its bytes — is accurate.

Also emitted and validated: the pinned-purge refusal (complete `PinnedPurgeDisclosure`, three
ordered consequences, three pins sorted by `pinId`, `evidence.pinned` /
`REQUEST.PRECONDITION_FAILED` / exit 2, detail in **both** `termination` and `errors`); the
required-output failure after commit (`DELIVERY.REQUIRED_FAILED`, `delivery-required`, exit 4,
`runId` retained); a **missing parity field** producing the same fault rather than an empty
result; `evidence.regeneration-mismatch`; `evidence.purged` on a query after purge;
`WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`.

Negative controls I ran on the disclosure: truncating the three consequences refuses; carrying
`purgeDisclosure` on another code refuses; a **subset** of pins is schema-valid — completeness is
a host obligation the schema cannot decide, which is exactly what the contract says.

### 3.10 Mutation replay, repair-apply key

`H("workflow.mutation-intent", {schemaVersion:1, requestId, stepId, projectId, operation})` as
a bare 64-hex key; a different fresh request, a different step and a different operation each
give a different key, so different fresh requests never deduplicate. `repair-apply` is
**excluded by schema** from `MutationReplayScopeV1.operation` and `MutationParams.mutationClass`
and uses the distinct **raw SHA-256 of canonical
`{operation:"repair-apply", projectId, repairPlanId, baseSnapshotId}`**. Two different recipes;
neither substitutes for the other.

### 3.11 Scope-policy parameter and comparison

A real `ScopeDocumentV1` bound into the retained analysis spec through the exact registered row
`workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1`, keyed by the **whole
document** digest. A bounded verifier proves selection membership from the retained spec;
a document that is not selected, a spec selecting no scope parameter, and an unregistered
parameter document each refuse with their own reason.

The two scope records stay distinct throughout: `plan.scopeDigest` names the foundation
`scope-descriptor` (the repository extent actually walked) and `EvaluationContext.scopeDigest`
names `ScopeDocumentV1` (the operator's glob policy over that extent). I built a comparison in
which **only** the scope policy changes — `contextDelta.scopeChanged: true`, everything else
false, `plan.scopeDigest` and the snapshot unchanged — classified `SCOPE-DELTA` at the E2→E3
axis.

Also emitted and validated: a **missing required detector pivot** (`indeterminate`, exit 3,
`BASELINE.RECIPE_UNSUPPORTED`, `BASELINE.PIVOT_DETECTOR_UNAVAILABLE`); an **evidence-availability
change** where the same-kind import identity changed under a gating rule with required runtime
evidence (`INDETERMINATE` / `evidence-availability-changed`,
`COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE`); and an **empty-result comparison that is still
indeterminate** — zero entries, one gating rule deficiency, verdict `indeterminate`, because
missing evaluation can hide a finding that appears in neither set and entry counts cannot prove
absence.

### 3.12 Explicitly authorized test / preparation / repair

`TestExecutionStepParams` admitted with `argv0Source` bound to a toolchain-closure member, an
allowlisted environment, and the four effect values **copied** from the pinned truth table; an
over-claimed `ENFORCED-PLATFORM` refuses. The four effect *field names* project four of the seven
closed permission **tokens** (`PT-PROC-EXEC-DECLARED`, `PT-FS-WRITE-HOST-STATE`, `PT-NET-EGRESS`,
`PT-ENV-READ`), all present in the pinned table; `PT-HOST-EFFECT-BROKERED` and the two read
tokens are deliberately projected by no effect field. A `RepairPlanDescriptor` was built and its
`repairplan2` identity computed, with `RepairApplyParams` and the consent mapping
(`interactive-explicit → interactive-consent` / `interactive`,
`policy-record → pre-existing-policy` / `policy`).

Authority boundaries reconstructed: the authority grant is the **operational**
`authorizationRef`, excluded from the Plan and from every content identity; the Plan binds only
the **semantic projection**; `imported-inert` projects only `read-import` while `host-prepared`
projects `prepare-code`; a test-execution step has **no Plan** and `test-code` is not an analysis
semantic-grant operation; confinement is never claimed.

### 3.13 Cache key vs cache hit

The `cache-key` record admits and mints an identity; the **same record** under the
`regeneration-key` domain mints a different one. Construction is pure — it reads no bytes and
resolves no reference — while admitting a **hit** requires the Run's whole closure, and a bare
`coverage-payload` / `import-payload` / `fact-payload` reference is refused as an authoritative
root rather than resolved by guesswork.

---

## 4. Issues

### MUST-1 — the capability-manifest value-domain successor is not selected by any contract selector

**Selectors.**
`docs/v2/contracts/product-v1/identity-and-evidence.md` §3, the sentence
*"The host validates the committed CVE1 artifact under the effective `delivery.v4.json` schema
and recomputes capabilityManifestId as …"*;
`docs/coop/design-corrections/native/capability-manifest-domains.v2.json#/standing`;
`docs/v2/contracts/product-v1/native-evidence.md` §11.

**What I found.** `capability-manifest-domains.v2.json` declares itself the *"Normative CURRENT
successor of delivery.v4 capabilityManifestIdentity valueDomains, **named by native-evidence
section 11 and identity-and-evidence section 3**"*, and its `RELATION-DOMAIN-V2` extends the
bound relation domain to **13** members by adding `unresolved-edge`, with the stated reason:
*"A provider declaring the new relation as a capability could not previously be expressed in a
capability manifest at all, which made it unrepresentable in a PlanId input."*

Both naming claims are false in the kit:

* identity-and-evidence.md mentions `capability-manifest-domains.v2` **once** (§3, the ladder
  paragraph) and only as a *declared mirror* of `RELATION-LADDER-DOMAIN-V2.ladders` that is
  drift-checked against the relation registry. It is **not** named as the ADM-DOMAIN /
  value-domain successor, and the sentence that actually selects the admission document names
  `delivery.v4.json`.
* native-evidence.md mentions `capability-manifest-domains` **zero** times (verified by full-text
  search of the kit).

**Consequence.** An implementer following the contract text applies `delivery.v4`'s ADM-DOMAIN,
whose `fact-plane.v1#relationRegistry.relations` domain has **12** members (verified against the
live `fact-plane.v1.json` bytes in the kit: 12). A release capability manifest declaring
`unresolved-edge` — a capability the matrix advertises as `unresolved-edge@observed`,
`SUPPORTED-DESIGN` in five of six language modes, requested by the **matrix-fixed default
profile** for every non-syntax unit — is then refused at ADM-DOMAIN under DL-DOM-1's
*"no third state"*. The implementer must either refuse the product's own thirteenth relation or
invent the selection of a document no contract selector names. Both are invention.

**Fix (one sentence plus one list entry).** identity-and-evidence §3 must name
`native/capability-manifest-domains.v2.json` as the effective value-domain/ADM-DOMAIN registry
for the committed CVE1 artifact, superseding `delivery.v4.json`'s `valueDomains` within its
declared scope; and native §11 must actually list it, as its standing claims.

### MUST-2 — `libSelection` → `standardLibraryComponentDigests` is an enforced join with no published name mapping

**Selectors.**
`docs/v2/contracts/product-v1/native-evidence.md` §2.4, the `toolchain.libSelection` row
(*"each must be covered by a retained component"*) and the paragraph
*"`libSelection` … selects the same case-insensitive name set as the honored `lib` list"*;
`native/native-evidence.schemas.v2.json#/$defs/TypeScriptToolchainIdentityV1/properties/libSelection`
(*"each must name a retained component"*) and
`#/$defs/TypeScriptLibComponentV1/properties/component`
(*"declaration file name inside the admitted stdlib closure tree, e.g. lib.es2022.d.ts"*);
native §10's refusal row `native.native-context-lib-not-retained`.

**What I found.** `libSelection` holds the effective TypeScript `lib` **names** (`es2022`,
`dom`), forced by the equality rule against `configProjection.honoredOptions.lib`, whose values
are `compilerOptions.lib` values. `component` holds declaration **file** names
(`lib.es2022.d.ts`). *"Each must name a retained component"* therefore cannot hold literally,
and no document in the kit publishes the name → component mapping. The join is not optional: it
is enforced at context admission with its own typed refusal and its own §10 route
(`request-rejected` 2, `REQUEST.PRECONDITION_FAILED`, before PlanId).

I could not build the TypeScript context vectors without inventing the TypeScript-ecosystem
convention `lib.<name>.d.ts` (recorded in `output/ref/closure.py` at the point of use). Two
conforming hosts that invent different mappings **admit and refuse the same retained context
bytes differently**, which is a public admission divergence, not algorithm freedom.

**Fix.** Publish the mapping in §2.4 (either `component == "lib." + lowercase(name) + ".d.ts"`,
or make `libSelection` carry component names and drop the `honoredOptions.lib` equality rule —
but not both readings).

### SHOULD-1 — RC-1 does not determine `resolutionCompleteness.state` for `unresolved-edge@observed`

**Selectors.** `docs/v2/contracts/product-v1/native-evidence.md` §4.3 **RC-1**;
`native/native-evidence.schemas.v2.json#/$defs/ResolutionCompletenessState`;
`native/native-capability-matrix.v2.json` capability `unresolved-edge`.

RC-1 names `not-applicable` for seven one-rung relations and for syntactic rungs, and forbids it
on a **resolved** rung. `unresolved-edge@observed` is in **neither** list and `observed` is not a
resolved rung. `resolutionCompleteness` is a **required** member of `ViewEntryV3`, and the
capability is `SUPPORTED-DESIGN` in five modes, so an entry is owed for an ordinary Run.

My vector (`vectors/rc1-unresolved-edge-state-gap.json`) shows **two** states admissible under
RC-1/RC-2 and the cause registry (`complete` and `not-attempted`), producing **two distinct
`coverage2` payload digests** for the same observation of the same universe — a divergence in a
content-derived identity.

**Fix.** Add `unresolved-edge` to RC-1's `not-applicable` list, or state the required state for
the `observed` rung explicitly.

### SHOULD-2 — the repair plan's `closedWorld` is described as "copied from" a record it cannot hold

**Selectors.**
`workflows/schemas/repair.schema.json#/$defs/RepairPlanDescriptor/properties/closedWorld`
(*"Copied from the evidence Run's native ClosedWorldV2 (native-evidence.md §4.5)"*, closed at
five properties);
`native/native-evidence.schemas.v2.json#/$defs/ClosedWorldV2` (closed at **seven** required
properties);
`workflows-and-surfaces.md` §12 (*"the workflow repair prerequisites consume
`ClosedWorldV2.deadCodeRepairEligible` and `affected_targets`"*).

A literal copy of `ClosedWorldV2` is **refused** by the repair schema (I hit exactly this:
*"Additional properties are not allowed ('dynamicDispatch', 'reasons' were unexpected)"*). The
projection — drop `dynamicDispatch` and `reasons` — is determinate by elimination, so no semantic
invention is forced, but it is published nowhere, and `dynamicDispatch` is a genuine closed-world
ingredient that a destructive-repair prerequisite silently discards.

**Fix.** Replace "Copied from" with the explicit projection, or widen the record to the seven
`ClosedWorldV2` members.

### Advisories (nonblocking)

* **ADV-1 — the "four closed representations" are five tokens in practice.**
  identity §3 states *"The four representations are closed"*, but
  `identity-schemas.v2.json#/$defs/{Ref,ProofInputRef,FindingEvidenceRef}/properties/digest`
  carry `representation: "by-domain"`, a fifth token that indirects into the four through
  `x-opensip-digest-domains.byDomain`. The adjacent paragraph explains the indirection, so a
  careful reader recovers; a strict implementer enforcing the four-member vocabulary refuses
  three real fields. One sentence closes it.
* **ADV-2 — the `LogicalPath` description overstates its adoption.**
  `identity-schemas.v2.json#/$defs/LogicalPath` says *"every identity-bearing path field now
  carries it in the schema"*. In fact only `Blob.path` and `import-blob.path` reference it;
  `fact.anchors[].path` and `finding-fingerprint.subjectKey.logicalPath` are plain bounded
  strings. (The three `scope-descriptor` arrays legitimately cannot use it — `.` is the project-
  root sentinel and `LogicalPath` forbids a dot segment.) No invention is forced, because an
  anchor path must be an inventoried snapshot path and inventory rows **are** `Blob`, so the join
  restores the grammar; the sentence is simply not true as written.
* **ADV-3 — the L0 body payload carries two length prefixes.**
  `fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar` gives
  `payloadEncodingByLevel["L0-verbatim"] = "u32be raw_byte_len || exact body-span bytes"` and
  `domainSeparatedPreimage` ends with `"u32be payload_len || payload_bytes"`. Read together the
  L0 payload is length-prefixed **twice** (`payload_len == raw_byte_len + 4`). The reading is
  decided by symmetry with `streamFraming` for L1–L3 (`u32be token_count || token*` under the
  same outer `u32be payload_len`), and I implemented it that way, but the alternative reading is
  grammatically available and yields a different `bodyIdentity`. One explicit byte vector or one
  sentence would close it.
* **ADV-4 — `PLATFORM-ID-DOMAIN-V1` admits platforms the product does not select.**
  Both `delivery.v4.json` and `capability-manifest-domains.v2.json` bind
  `ProviderCapability.platformIds[]` to a domain containing `windows-x86_64-msvc`,
  `windows-aarch64-msvc` and `linux-x86_64-musl`, while security S8 and the native matrix select
  exactly four machine ids and admission §5 item 1 states *"Windows is not selected."* A manifest
  can therefore declare a capability for a platform the selected product does not promise.
  `delivery.v4` discloses this as `DUD-V4-9`, so it is an accounted open item rather than a
  hidden inconsistency — but the product contracts do not repeat the accounting.

### Related but **not** an issue (checked and cleared)

`capability-manifest-domains.v2`'s `DEFICIENCY-DOMAIN-V1` remains the inherited **five** members
while the product's `DeficiencyV2` has **nine**. I initially recorded this alongside MUST-1, then
withdrew it: the four added members (`input-closure-incomplete`, `resolution-incomplete`,
`external-consumers-unknown`, `derivation-policy-unmet`) are all **per-Run or
requirement-relative** conditions, whereas `AbsentCapability.deficiency` is a **release-level**
capability-absence declaration for which `provider-unavailable` and `language-tier-unsupported`
suffice. The rule is closed and implementable; only the rationale is unpublished. Noted here so
the distinction between a missing contract and a missing explanation is explicit.

---

## 5. What required invention

| # | What I had to invent | Blocking? |
|---|---|---|
| 1 | The `lib` name → stdlib `component` file-name mapping (`lib.<name>.d.ts`) | **Yes — MUST-2** |
| 2 | Whether the effective ADM-DOMAIN registry for the committed CVE1 artifact is `delivery.v4`'s or the unnamed successor's | **Yes — MUST-1** |
| 3 | The `resolutionCompleteness.state` of an `unresolved-edge@observed` Coverage entry | **Yes — SHOULD-1** |
| 4 | The 7 → 5 projection of `ClosedWorldV2` into the repair descriptor | **Yes — SHOULD-2** |
| 5 | The L0 double-length-prefix reading (decided by L1–L3 symmetry) | No — ADV-3 |
| 6 | Synthetic repository contents, closure trees, tool digests, level-specification bytes, grammar bundle bytes, ProjectId, RequestId/ExecutionId values | No — these are **inputs I am supposed to choose**, not design gaps |

Everything else in the brief was reconstructable from the kit **without** inventing design:
`C`, `H`, the frame, the digest law, CVE1, the capability-manifest recipe, the body-identity
frame and both dialect axes, the ownership selection law and its six ordered causes, the
Coverage producer boundary, the deficiency/cause registry, the syntax capability law at all
three boundaries, the array law and its ten-member order vocabulary, the payload registry
including the `ScopeDocumentV1` parameter row, the predicate node addressing, the comparison
axis chain, the availability disclosure, the public route registry with origin dependence, the
bounded-subject elision, the D9 composition, the mutation and repair-apply keys, and the pinned
purge refusal.

---

## 6. Limitations

* **Nothing here is qualification.** No compiler, cargo, provider, repository, filesystem,
  ledger, renderer or cryptographic primitive was executed. Real OS/compiler/crypto/SQLite
  measurements are future qualification work and I do not demand the product already exist.
* **Every provider/OS/security observation in my vectors is a synthetic trusted input** — an
  assumption. Synthetic TCB observations are never native enforcement proof. In particular my
  closure trees, stdlib inventories, grammar bundles, `SourceUnitOwnershipV1` enumerations and
  `permission-truth-table` copies are asserted, not measured.
* **My `close_run` is not the product's.** It implements the joins the contracts name that are
  decidable over retained descriptors; it does not implement the evaluator, the ledger, retention
  GC, lease mechanics, trust time, root-chain admission, migration, the protocol-3 state machine,
  or renderer conformance. Where I say a refusal "fired", that is my reconstruction of the stated
  rule, not evidence about any implementation.
* **`x-opensip-order` is not a JSON-Schema keyword.** A stock validator ignores it; I implemented
  the closed vocabulary separately. Any statement I make about mirror agreement holds only with
  that enforcement in place, and I have said so where it matters.
* **The reference-fixture and checker claims in the contracts are untested here.** I deliberately
  did not read them; assertions such as "the checker exercises N cases" are outside what I can
  confirm from this kit.
* **Governance standing is out of scope by construction.** The correction record and central
  readiness register are excluded from this kit, as the contract index states; nothing above
  grants readiness, acceptance or implementation permission, and passing a design-reference check
  is not product qualification.
* I did not exercise `agent serve`, HTML/SARIF renderers, `policy test` suites, baseline
  export/adopt round trips, trust recovery, store migration or the installation transition
  journal beyond reading their contracts; they were not in the brief's vector list.

---

## 7. Verdict

The design is **substantially reconstructable**. Eight complete Run descriptor graphs — five
TypeScript (including two contexts under one Plan), one Rust mixed-edition workspace, and two
compiler-free syntax-only Runs over both a code grammar and a data-document-only repository —
close end to end against my independently written encoder, identity helper and admission, with
58 negative probes all refusing for the stated reason and with public terminations and failure
envelopes that validate against the kit's own schemas. The parts of the design that are hardest
to get right — the body-identity dialect axes, the ownership selection law and its derived
disclosure, the coverage totality `matchOn` law, the syntax capability guard at fact and scope
boundaries, the origin-dependent public route table, and the per-step availability composition —
are specified precisely enough that I reconstructed them from prose and the machine-readable
registries alone, and my independent constructions agreed with the laws in every case I tested.

It is nonetheless **CHANGES_REQUIRED**. MUST-1 is the serious one: the document that repairs the
capability-manifest relation domain exists in the kit, asserts that two contracts name it, and
neither does — while the contract sentence that *does* select an admission document points at the
superseded one. The effect is that the product's own thirteenth relation is unrepresentable in a
Plan input for any implementer who follows the text, which is precisely the defect the successor
was written to fix. MUST-2 is smaller in blast radius but is a genuine enforced admission join
with no published mapping, and it made me import outside-the-kit knowledge to build an ordinary
TypeScript context. Both are one-or-two-sentence corrections; neither is a structural problem.

No claim of full product qualification or implementation authorization is made or implied.
