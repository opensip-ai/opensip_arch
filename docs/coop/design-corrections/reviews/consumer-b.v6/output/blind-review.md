# Blind consumer-B reconstruction — OpenSIP DR-011-R10 product-v1 contract set

**Verdict: CHANGES_REQUIRED** — 2 MUST, 2 SHOULD, 2 advisory.

I am a fresh blind consumer. I authored none of this design, read no author
reference model, fixture, golden, report or prior review, and had no expected
results. I read only the 45 files of the supplied kit, implemented the canonical
encoder, the `H` identity frame, the CVE1 capability-manifest encoder and every
admission law I needed **from the prose and the machine-readable registries**,
and then built my own descriptor graphs and computed my own vectors.

Everything below is reproducible from
`output/ref/*.py` (my disposable reference code) and `output/vectors.json`
(78 vector groups, 355 retained content-addressed objects, every value computed
by that code).

---

## 1. Input custody and hash verification

`consumer-input-manifest.json` declares 45 files under
`parentSubjectSha256 = ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9`.

| Check | Result |
|---|---|
| Files declared | 45 |
| SHA-256 **and** byte length match | **45 / 45** |
| Missing | 0 |
| Present on disk but undeclared | 0 |
| Total declared bytes | 2,583,367 |

No input-custody problem. Every normative dependency I needed for the promised
vectors was present: the retained `resolved-inputs.v2#planIdContract.canonicalValueEncoding`
(all eight CVE1 types), the DELIVERY-v4 capability-manifest recipe as carried by
the selected successor registry, the C-2 `executionId` provenance selector, the
inherited `d9-exit-contract.v1.14` for the D9 composition check, `fact-identity-policy.v2`
for the body grammar, `permission-truth-tables.v9` for the effect selections,
`fact-plane.v1` for the inherited relation vocabulary, and all four
foundation/native/workflow/security schema bundles. I did not need — and did not
read — any readiness or review record, and the index is right that none is
required to reconstruct a semantic recipe.

I read the index's distinction as stated: the **normative retained/superseded
selector tables inside the five contracts** determine the applicable recipes; the
correction record and readiness register grant *standing* only and are correctly
absent. Historical review narratives inside the inherited documents (the F1–F12 /
R1–R7 / PR-* / CB-* provenance headers) I treated as provenance and followed no
link out of the kit.

---

## 2. The reconstruction

### 2.1 The spine, end to end

Zero-config discovery → typed config/source → invocation/step/attempt →
Plan → native facts/Coverage/view → proof verification → Evidence/Seal/Run →
durable receipt and current availability reconstructs cleanly, and the
**semantic / operational** split holds at every joint.

| Stage | Owner and selector | What it mints |
|---|---|---|
| Repository boundary, custody, nested-project boundaries | security **S3**, one shared rule `discovery-defaults.py` | `DiscoveryProvenanceV1` → `AdmittedBoundaryInventoryV1` |
| Language units inside that boundary | native **§1.4 U-1…U-8** | `WorkspaceUnitV2`, `UnitMembershipV1`, foundation `scope-descriptor` |
| Configuration resolution | admission **§1.1** + `product-configuration.schema.v2` | resolved `semantic-configuration`, `resolvedConfigDigest` |
| Snapshot | identity **§3** | `snapshot2` over ProjectId + inventory + config/scope/VCS digests |
| Invocation / step / attempt | workflows **§1** | `RequestId` (pre-admission), `ExecutionId` per attempt, `StepId` = position |
| Native context | native **§2.3/§2.4/§1.2**, `admit_native_context` | `native.context.{rust,typescript,syntax}.v2` |
| Semantic universe | native **§2.1/§2.2/§1.2**, `bind_*_universe` | `native.semantic-universe.{rust,typescript,syntax}.v2` |
| Plan | identity **§3** | `plan2` incl. `nativeContextDigests` (bare-hex **set**) and `capabilityManifestId` |
| Scope / fact / Coverage | native **§4.1a/§4.3**, `admit_coverage_result_v3` | `scope2`, `fact2`, `coverage2` |
| View | identity **§3** | `view2` |
| Derivation | identity **§3** | `stage-spec` → `exec-plan2` |
| Proof | identity **§4** | `program-predicate` → `predicate-witness` → `proof2` |
| Evidence / Seal / Run | identity **§3/§5** | `evidence2` → `seal2` → `run2` |
| Custody | identity **§5** | commit receipt, `commit-inventory`, availability generation |

**Semantic identity vs operational authority.** `RequestId`, `ExecutionId`, wall
clocks, PIDs, credentials, authorization nonces, receipts and output destinations
are excluded from every content identity. My vector `ID-1` recomputes the same
`run2:7c1fb0…` under a changed RequestId, ExecutionId and timestamp, and moves
`plan2` on a single semantic field (`budget`). `ID-2` shows every non-constant
Plan field moving the identity individually. The `authorizationRef` /
`securityGrantRef` stay outside the Plan descriptor; the Plan binds only the
semantic-grant *projection*.

**Mutation vs analysis steps.** Only `analysis` and `verify` seal or link a
`run2`. `comparison`, `query`, `render`, `import`, `repair-preview`,
`repair-apply`, `test-execution`, `native-preparation`, `mutation`,
`export-delivery` and `doctor` never mint one. A test-execution step has **no
Plan at all**; its observations enter an analysis only as an `import2` of kind
`test`, and `test-code` is not an analysis semantic-grant operation.

### 2.2 Capability-manifest admission, derived before encoding

The effective ADM-DOMAIN registry is selected **by name, by both owning
contracts** (identity §3 and native §11):
`docs/coop/design-corrections/native/capability-manifest-domains.v2.json`. Its
scope is exactly two relation registries; every other value domain keeps its
inherited membership. I implemented the four inherited gates in their inherited
order and the declared traversal order, then encoded.

Positive vector `CAP-1` (my own minimal manifest, one TypeScript provider
declaring `unresolved-edge@observed`, one absent Rust row):

```
committedBytes (CVE1)  = 761 bytes
capabilityManifestId   = 59e600029dd94f15c1195a6a68cf5892945ea62a497f6567644264f62dbffbaa
recipe                 = SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)
```

`unresolved-edge` is admissible **only** under `RELATION-DOMAIN-V2`; the
inherited twelve-member domain cannot express it, which is exactly why the
successor is selected.

Every named gate exercised, each with its own refusal (`CAP-N1…N12`, `CAP-P2`):

* **ADM-TYPE** — `schemaVersion: true` and `schemaVersion: "1"` both refuse before
  any content comparison. A declared-OPEN position is still typed: `schemaVersion: 2`
  passes and moves the id to `437e791c…`.
* **ADM-CLOSED** — an undeclared key on `ProviderCapability` and a missing required key both refuse; a MAP is not a record and closes nothing.
* **ADM-DOMAIN** — `declares: "resolved-callee"` refuses (a rung of *another*
  relation's ladder is not a live vocabulary token), an unregistered relation key
  refuses, and `coverageState`/`deficiency` outside their one- and five-member
  domains refuse.
* **ADM-ORDER** — unsorted `platformIds`, a **duplicate** `platformIds` member and
  a duplicate `providerId` row all refuse; a duplicate is an ordering violation,
  not merely an unsorted list.
* **CVE1 after the gates** — a non-NFC `providerId` refuses at the encoder;
  `-0`, floats and out-of-range integers refuse; a negative integer encodes under
  tag `07` (`07ffffffffffffffff` for `-1`); map-key **insertion** order does not
  change the identity, because CVE1 sorts map entries by key bytes.

### 2.3 The canonicalizer and the H frame, built from prose

`C`: UTF-8 byte-ordered keys, no whitespace, shortest decimal integers,
`\b\t\n\f\r` plus lowercase `\u00xx` for other C0 controls, no slash escaping,
U+007F and U+2028 unescaped, arrays in admitted order, duplicate keys and
non-scalar Unicode refused. Hand-spelled control:

```
C({"b":1,"a":"xé","é":[1,-1,0],"z":{"k":true}})
  = {"a":"xé","b":1,"z":{"k":true},"é":[1,-1,0]}     (byte order: a < b < z < C3A9)
```

`H`, hand-verified against the literal frame:

```
frame("subject-scope",{"a":1})
  = 6f70656e7369702e70726f647563742e7631 00 7375626a6563742d73636f7065 00
    0000000000000007 7b2261223a317d
H = 31727110bfcd1b633cbf7a4f25db35aa3222ca8fe6ce76fd53f990c78525a476   != SHA256(C(X))
```

I implemented the whole `x-opensip-order` vocabulary (`sequence`,
`canonical-set`, `canonical-order`, `utf8`, `path`, `numeric`, `ordinal`,
`predicate`, `ruleId`/`waiverId`, `{"by":[…]}`) and enforced it on every array I
built.

### 2.4 Complete positive Run graphs — all three universes

| Run | Universe domain | Facts | Seal | RunId |
|---|---|---|---|---|
| **TypeScript** (ordinary project, `node_modules`, bare specifiers) | `native.semantic-universe.typescript.v2` | 9 | indeterminate | `run2:7c1fb084…` |
| **Rust** (mixed-edition workspace) | `native.semantic-universe.rust.v2` | 15 | pass | `run2:b26e3576…` |
| **Syntax, code grammar** (no TS/Rust unit) | `native.semantic-universe.syntax.v2` | 6 | indeterminate | `run2:0ac8b481…` |
| **Syntax, data/document grammar** | `native.semantic-universe.syntax.v2` | 7 | indeterminate | `run2:7a02673f…` |

Each carries a **non-empty** `plan.nativeContextDigests` and its *own*
language-specific universe/fact/Coverage path. The Rust graph is not a Rust
context merely present in a TypeScript Plan: it has its own snapshot, Plan,
scopes, facts and Coverage minted under the Rust universe, with the nested
`DependencySourceSetV1`, `DependencyFileManifestV1`, `UnifiedFeaturesV1`,
`CargoConfigProjectionV2` and `SourceUnitOwnershipV1` records retained as frames
and re-admitted.

The graph is acyclic exactly as stated: proof carries no `evidenceId` and no
`runId`; evidence includes proof; seal includes both; Run includes seal.
`subjectScopeCommitment` is the **identical** digest as `scope2` in
`sha256:` form (`FILE_COMMIT.hex == FILE_SCOPE_ID.hex` — verified true), not a
second commitment.

`view.schemaDigests` names exactly the two registered documents each view
admitted (relation payloads `ef0c244e…`, CoverageResultV3 `2a5fc493…`), and
`JOIN-1` confirms every closure-bearing field carries its declared kind
(`enumeratorClosure`/`producerClosure` = `provider`, `evaluatorClosure` =
`evaluator`) **and** is a member of `plan.semanticClosures`.

### 2.5 TypeScript configuration graphs — all four required shapes

| Vector | Shape | `configOrigin` (**derived**) | `tsconfigGraphHash` |
|---|---|---|---|
| `TS-CFG-1` | ordinary `tsconfig.json`, `extends` = [`base.a`, `base.b`, **`base.a` again**] | `tsconfig` | `1c7802dd…` |
| `TS-CFG-1b` | control: the same three edges **deduplicated** | `tsconfig` | `dd2c5a75…` ≠ above |
| `TS-CFG-2` | explicitly selected **custom-named** `configs/app.build.json`, ordered bases with a repeat | `tsconfig` (entry kind `other`) | `c19e118c…` |
| `TS-CFG-3` | **synthesized** (entry `null`, `nodes` `[]`) | `synthesized` | `432d4a7f…` |
| `TS-CFG-4` | **`jsconfig.json` extending a shared base of another filename** | `jsconfig` | `fbcfa632…` |

`extendsResolved` is `x-opensip-order: sequence`, so the repeated base is
retained and later-wins precedence survives; deduplicating it is a *different*
retained record and a different universe. `configOrigin` is derived from the
retained record's entry node, never asserted — `TS-N9` refuses an asserted
`jsconfig`.

The ordinary project reads `node_modules` through a retained
`ResolvedNodeModulesLayoutV1` (`7f7fca6b…`) joined by **digest**, not by snapshot
membership — correct, because the one shared discovery rule prunes `node_modules`
by path segment so an inventory row could not exist. `nodeModulesInReadSet` is
exactly `nodeModulesLayoutDigest is not null` (`TS-N11` refuses the drift), and
with the layout absent every bare specifier is `unresolved-module-specifier`,
scope `external`, never an implicit install.

### 2.6 Clone body identity

The framed preimage, computed from the prose and hand-checked:

```
body span "{ return 1; }"            (src/util.ts, bytes 24..37)
L0 payload  = 0000000d 7b2072657475726e20313b207d        (raw_byte_len || bytes)
final frame component = 00000011 0000000d 7b…7d          (payload_len = raw + 4)
bodyIdentity = sha256:09e6886969e59edf13b8058ded5b61074d0bf3343bde1e096e98df56aac9e4eb
```

`TS-CLONE-N1` computes the *single*-prefix reading and gets
`sha256:4950da43…` — a different identity. The contract names which of the two
grammatically available readings is admitted, and my independent implementation
reproduces the double prefix.

`languageVersion` is the **raw 32 bytes** of `SHA-256(C(body-language-version))`,
and `body-language-version` is `derived`: I recomputed it from the domain row's
`languageVersionBinding` rather than accepting it.

**Body language vs provider identity.** The same 13 bytes in `src/util.js`, read
by the *same* TypeScript engine universe, mint
`sha256:88db5341…` — because `languageId` comes from
`bodyLanguageByVariant[<suffix variant>]` (`js` → `javascript`), never from the
domain row's own `language` field (which names the engine). `TS-CLONE-N2` refuses
a `rust`-framed body under a TypeScript universe.

**Grammar parse vs compiler parse.** The identical Rust body span read by the
grammar bundle mints `sha256:216ecad0…` against the compiler's
`sha256:74746ea0…` — different `compilerName`
(`opensip-grammar-bundle` vs `rustc`) and a different dialect branch
(`{grammarVariant:"rs"}` vs `{edition:2021}`).

**L0 vs a normalized level.** `RS-CLONE-L1` builds the framed token stream
(`u32be count || (u16be kind_len||kind || u32be val_len||val)*`) at `L1-lexical`
with a retained, re-hashable level specification. At L0 I recomputed the payload
from the fact's own anchor (a real source join); at L1 what is required is
retained-preimage custody plus the framed-identity check — which qualifies no
normalizer, exactly as the contract says.

### 2.7 The mixed-edition Rust workspace

Workspace: `crates/core` (package edition 2021, with a **`bin` target overriding
to 2018**), `crates/legacy` (2015), and **`tool#1`** — a valid `#` marker
directory, which closes a complete Run because `unitId` is
`H(native.compilation-unit.v1, {schemaVersion, markerPath, targetKind, targetName})`
and needs no delimiter.

| Selection | Owner of `crates/core/src/shared.rs` | Dialect | `bodyIdentity` | `sourceUniverse` |
|---|---|---|---|---|
| A: `lib core` | targetEdition `null` → package default | `{edition: 2021}` | `sha256:74746ea0…` | `sha256:bca51ef3…` |
| B: `bin coretool` | targetEdition **2018** | `{edition: 2018}` | `sha256:dfbaf49c…` | `sha256:77016a7c…` |
| C: `lib` + `test` (both defer) | package default | `{edition: 2021}` | **`sha256:74746ea0…` (unchanged)** | `sha256:…` (changed) |

That is the required pair of results: the **same physical file under two
explicitly selected target editions** is two universes and two body identities;
and **only the selection changing without changing the effective dialect** leaves
the body identity stable while moving the universe (and therefore `fact2`). No
relation payload changed to make either possible. The 21-crate map I built is 925
canonical bytes against a `u8` component maximum of 255 — the same order as the
contract's own 723-byte figure, confirming the reasoning independently of the
literal number.

Every branch of the selection law refuses with its own cause
(`RS-OWNERSHIP-NEGATIVES`): ownership missing, `enumeration: partial` **before any
row is read**, path not compiled, path owned only by unselected targets, and
selected owners disagreeing.

**Enumeration completeness ≠ resolution completeness.** I did not invent a
resolved rung for file facts: `file@enumerated` is `not-applicable` for
resolution (RC-1) while carrying its own independent `coverage: complete` over the
examined partition, and it is the **only** relation the registry marks total.

### 2.8 The derived relation/rung applicability table

Computed from the single ladder authority, not restated:

* **13** relations, **17** registered `(relation, rung)` pairs.
* **5** resolved pairs: `imports@resolved-target`, `references@resolved-binding`,
  `calls@resolved-callee`, `types@checked`, `reachability@from-resolved-calls`.
* **12** `not-applicable` pairs, including `unresolved-edge@observed` and every
  weaker rung of a multi-rung relation.
* `reachability` is the case that proves the rule is the **rung**, not ladder
  length: one rung, and that rung *is* resolved.
* **RC-0 runs first and is relation-specific and fact-independent.** I applied it
  to retained scopes and Coverage **with no fact present**:
  `unresolved-edge@enumerated` names two registered tokens and no registered pair,
  and refuses (`TS-N19`).
* State/count/class/attempt rules enforced at both boundaries: a resolution claim
  on a non-resolved rung (`TS-N20`), `not-applicable` on a resolved rung
  (`TS-N21`), and RC-2's "a zero edge count never implies complete" (`TS-N22`).

Anchor law by class, applied in every universe:
`source-text` ≥ 1, `body-identity` = 1, `inventory` = **0** — with `TS-N14`
(inventory fact carrying an anchor), `TS-N15` (unanchored code fact under a
*compiler* universe, not only under the syntax guard) and `TS-N16` (a `package`
fact anchored into an unrelated file) all refusing.

### 2.9 Compiler-free syntax-only Runs, and the code/data distinction

The bundled grammar set is **seven** languages / **fourteen** suffixes. I verified
the `code` subset (`typescript`, `javascript`, `rust`) equals the
`body-language-version.languageId` enum and that the four `data-document`
languages are **absent** from it — in both directions, at bundle admission
(`SY-N5`, `SY-N6`).

* **Data/document Run** (`README.md`, `docs/guide.md`, `data/config.json`,
  `data/values.yaml`, `settings.toml`, plus `tool/main.py` and a non-UTF8
  `assets/logo.bin`): the declared **inventory** capability is served for **every
  inventoried path**, including the two `unsupported-file` rows, because inventory
  capabilities are exempt from grammar gating at *both* boundaries and the
  inventory relations carry zero anchors. `declares@syntactic`,
  `clones@normalized-body-hash`, `references@resolved-binding` and
  `unresolved-edge@observed` are **disclosed as unavailable, not refused**:
  `coverage: unknown`, `deficiency: language-tier-unsupported`,
  `nativeCause: capability-missing`, indeterminate (3) / `VERDICT.INDETERMINATE`.
  A complete **empty** result would conceal unsupported analysis, and `SY-N11`
  refuses it.
* **Code-grammar Run** (`src/one.rs`, `src/two.rs`, `notes.md`,
  `scripts/build.py`, **no `Cargo.toml`, no `tsconfig.json`, no `package.json`**):
  inventory + `declares@syntactic` + `clones@normalized-body-hash` all genuinely
  `complete`, with the two identical bodies sharing one identity. `references`,
  `types` and `unresolved-edge` correctly unavailable —
  `unresolved-edge` because `resolutionAttempted` is the constant `false`.
* **Custody** is exact throughout: context `native.context.syntax.v2` carrying
  *only* the grammar bundle (no toolchain, stdlib, lockfile, `node_modules` or
  config graph), universe `native.semantic-universe.syntax.v2` committing the
  **selected** grammar set, provider a `kind=provider` closure, grammar a
  `kind=grammar` closure whose manifest `semanticVersion` equals `parserVersion`
  (`SY-N8` refuses drift).
* An **unselected** grammar lends no capability (`SY-N4`); a scope naming both a
  supported and an unsupported path cannot hide the unsupported part behind the
  supported one (`SY-N3`); `.py` refuses rather than folding into a neighbour
  (`SY-N9`, `SY-N10`) and stays `unsupported-file / no-bundled-grammar`.

**Every advertised mode has a representable analysis path.** I tested the
unsupported grammar (`.py`) explicitly and never assumed a TypeScript compiler to
do it.

### 2.10 Zero-config selection under an incomplete release

Multi-unit repository (`apps/web` ts-tsconfig, `apps/legacy` js-synthesized,
`services/api` rust-cargo, `docs` syntax-only) with a release declaring
everything **except** `clones-near`, `clones-cross-tsjs` and `unresolved-edge`.

* The **default request is fixed by the matrix**, not by the release: every
  capability whose `(capability, mode)` cell is not `NOT-SELECTED`, including
  `UNSUPPORTED-TYPED` cells. Today's three `NOT-SELECTED` cells are
  `clones-cross-tsjs` under the two Rust modes and `syntax-only`.
* A capability id is **not** a `relation@rung`: `inventory` covers three
  coordinates, `clones-near` and `clones-cross-tsjs` cover **none**.
* Single-step invocation: `{stepCount: 1, totalNoticeCount: 10, steps:[…]}`.
  Named multi-step invocation with a **different selection at step 2**:
  `{stepCount: 2, totalNoticeCount: 15, …}` — composed **per step**, so nothing is
  discarded to fit, and the same ownership tuple lawfully recurs across steps.
  Both validate against `common.schema.json#/$defs/CapabilityAvailabilityV1` with
  zero errors.
* Ownership is carried in **typed fields** (`capabilityId`, `languageMode`,
  `workspaceRoot`), never concatenated — `workspaceRoot` is a 4096-bounded
  `UserInputPath` while `subject` is 1024-bounded.
* Routes: a **fact-producing** capability projects onto its `relation@rung`
  Coverage entry; a **candidate-only** capability has no Coverage entry at all and
  its *only* public route is `CommandEnvelope.availability`. Where both
  unavailability and an unservable universe apply, `language-tier-unsupported`
  outranks `provider-unavailable`.
* Product promise vs installed availability vs explicit override are three
  distinct things, and `capability-availability` is a **declared parity field** of
  all five `requestClass: analysis` commands, so every applicable renderer carries
  it and an omission is a required-delivery fault.

### 2.11 Public failure envelopes and the D9 composition

Four complete envelopes, each built from an internal refusal **plus its
originating boundary**, all schema-valid against `command-envelope.schema.json`:

| Origin | Class / exit | errorCode | `termination.domainDetail` | `errors[0]` |
|---|---|---|---|---|
| External **configuration** | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.INVALID` | the same detail |
| **Retained external** spec | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | absent | route's `native.capability-spec-invalid` |
| **Host-generated invalid internal record** | **operational-failed / 4** | `SYSTEM.OUTCOME.ILLEGAL_STATE`, `faultCause: host-invariant` | absent | `HOST.INVARIANT_VIOLATED` |
| **Producer boundary** | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION`, `faultCause: provider-protocol` | absent | `native.coverage-cause-unsupported` |

Where the termination carries a detail, `errors` **is** that detail, so the two
surfaces cannot disagree; where it does not, the route's own envelope detail
supplies one. Before a Plan or Run exists no run envelope is fabricated.

`bounded_subject` reproduces exactly: a 4142-code-point subject elides to
**exactly 1024** code points, the registered key survives verbatim, and the
SHA-256 is of the untruncated UTF-8 (`c9789ed9…`). Units are code points, not
UTF-8 bytes — I confirmed the two differ for non-ASCII.

**The D9 extension checks out against the inherited contract.**
`d9-exit-contract.v1.14` declares `SYSTEM.OUTCOME.ILLEGAL_STATE` in its **closed**
errorCode vocabulary with **no cause preimage in either inherited map**. Adding
`host-invariant → SYSTEM.OUTCOME.ILLEGAL_STATE` keeps `faultCauseToErrorCode`
injective, adds no class/exit/reason/error code, and respects the inherited
`causeModel.precedence` (`faultCause > rejectionCause > deficiency`) — which is
precisely why routing a host-minted invalid record to `operational-failed`
rather than `request-rejected` is *required* by the inherited precedence rather
than a new choice. `codeMaps.rule`'s totality is over the **declared cause
domain**, so an error code without a preimage was never a violation. It **is** a
vocabulary extension (10 → 11 causes) and the successor says so.

### 2.12 Custody, purge, replay, comparison

* **Pinned-purge refusal**, complete and schema-valid: `evidence.pinned` →
  `request-rejected` / `REQUEST.PRECONDITION_FAILED` / exit 2, `subject` = the
  RunId, `purgeDisclosure` carrying the RunId, the **complete** `activePins`
  inventory sorted uniquely by `pinId`, and the three ordered consequences. No pin
  omitted, truncated or aggregated. `WF-5N` shows a schema-valid **subset** also
  validates — correctly identifying that completeness is a *host* obligation
  against the ledger observed under the exclusive lease, not a schema-decidable
  property.
* **Generic mutation replay scope** vs the **repair-apply key** are genuinely two
  recipes: `H("workflow.mutation-intent", {schemaVersion, requestId, stepId,
  projectId, operation})` = `38a370ad…` (operational, scoped to one host-minted
  request — a different fresh request yields `a1c61faa…`) against raw SHA-256 of
  `C({operation:"repair-apply", projectId, repairPlanId, baseSnapshotId})` =
  `258f41fb…` (content-derived, its own step, excluded from `MutationParams`).
* **Purge/replay/availability**: sealed assurance is immutable; current
  availability is a separate monotonic generation; a retention decision changes no
  identity and never turns expired evidence into `no match`; the three event
  positions (`REQUEST.PRECONDITION_FAILED` before evaluation, `HOST.IO_FAILURE`
  during a selected operation, indeterminate-3 for admitted partial inputs) are
  distinct and not interchangeable. Cache-key **construction** is pure and grants
  nothing; a **hit** is admitted only against the Run's whole closure.
* **Required-output failure**: after commit, `DELIVERY.REQUIRED_FAILED` / exit 4 /
  `faultCause: delivery-required` retains the RunId and rewrites nothing; a
  missing parity field is the same fault, never an empty result.
* **Comparison, scope axis only.** I bound a real `ScopeDocumentV1` through the
  registered `parameter` row (document `policy-document.schema.json`, selector
  `#/$defs/ScopeDocumentV1`, document digest `012505da…`) and built a comparison
  in which **only that scope policy** changes: policy, waiver and detector digests
  equal, `EvaluationContext.scopeDigest` `339fad44…` → `5186a5c7…`, axis E2→E3,
  classification `SCOPE-DELTA`. It is a different record from the foundation
  `scope-descriptor` that `plan.scopeDigest` names, and both may sit in one Plan.
  I also reconstructed the honest boundary: `adopt_baseline` is a pure projection,
  and without the retained analysis spec its scope binding is a **caller
  assertion**, not a join.
* **Audit shapes**: missing detector pivot (`pivot-detector-unavailable`,
  E0 never substituted with B), evidence changed on a gating rule
  (`evidence-availability-changed`; identity comparison, not kind presence), and
  the **empty result on both sides** that is still indeterminate because missing
  evaluation can hide a finding present in neither set. All four comparison
  entries validate against `comparison-result.schema.json#/$defs/Entry`.

### 2.13 Sufficiency and repair

`Atom.minResolution` and `EvidenceRequirement.minResolution` are **rung names**;
the flat enum is exactly the union of the thirteen ladders (verified equal) and is
**necessary only** — membership of *this atom's relation's* ladder is sufficient
and is enforced at admission. Satisfaction is ladder-index comparison inside one
relation; a cross-relation comparison is a **refusal**, never a truth value
(`SUF-N1…N6`).

Qualifying and insufficient pairs at all three levels: `declares@syntactic`
(qualifying) vs `imports` at the weaker `syntactic-specifier` rung;
`references@resolved-binding` under `universal-negative/forbid/forbid` with
`state: complete` and `exportsClosed: closed` — the **only** shape under which an
authoritative no-consumer claim is eligible — vs the same atom with one
`computed-member-access` edge (`resolution-incomplete`, cause carried by
`resolutionCompleteness`, `nativeCause` null **by design**) and vs a
budget-exhausted `partial` stage; `types@checked` with `annotated` derivation
(qualifying) vs `compiler-inferred` under `declared-only`
(`derivation-policy-unmet`, carried by `derivationKinds` and scoped to relation
`types`) vs a fact at the weaker `annotated` rung.

`SUF-2` reproduces the removed early exit: confidence 100000 against a floor of
900000 yields `confidence-floor-unmet` for a one-rung `clones` requirement under
`partial-ok`, and 1000000 satisfies.

The repair evidence requirements, the five-field `closedWorld` projection (with
`dynamicDispatch` and `reasons` **dropped**), the authority boundary (the
projection grants nothing; authority stays the sealed Run named by
`evidenceRunId`, including the two members the descriptor does not carry), the
target-relative reading of `dynamicDispatch`, and the imported-observation
boundary (`observable-unhit` ≠ unused; one window is never universal non-use;
runtime coverage is never OpenSIP Coverage; mandatory source correspondence) all
reconstruct — except for the one field named in MUST-1.

---

## 3. Independent vector inventory

78 vector groups. **83 discriminating negative controls**, every one refusing with
a typed cause, **zero** unexpectedly admitted:

| Group | Negatives | Covers |
|---|---|---|
| `CAP-N*` | 12 | all four ADM gates + CVE1 |
| `TS-NEGATIVES` | 26 | context/universe joins, hidden inputs, frames, anchor law, RC-0/1/2, totality, cross-universe discharge |
| `RS-OWNERSHIP-NEGATIVES` | 6 | every branch of the Rust dialect selection law |
| `RS-NEGATIVES` | 18 | clone disclosure derivation + Rust hidden/mismatched inputs |
| `SY-NEGATIVES` | 12 | grammar class law, capability boundaries, suffix law |
| `SUF-NEGATIVES` | 6 | atom vocabulary and cross-relation comparison |
| `TS-CLONE-N1/N2`, `TS-CFG-1b` | 3 | body framing and record-shape controls |

Highlights I want to name explicitly because they are the ones a permissive
implementation would pass:

* `TS-N13` — a `file@enumerated` fact of **another universe** does **not**
  discharge this scope's totality obligation. The view-level fact/scope join is
  existential, so without the five-coordinate `matchOn` a TypeScript fact would
  pay a syntax-universe scope's debt. Refuses.
* `TS-N23` — a raw canonical payload offered where an `h-identity` **frame** is
  required fails on the prefix; `TS-N24` — a single flipped bit in a retained
  frame fails; `TS-N25` — an unregistered H domain refuses; `TS-N26` — the
  retained context set must equal `plan.nativeContextDigests` **exactly**, in both
  directions.
* `RS-N19`/`RS-N20` — `configProjectionSha256` carrying the raw **file** digest,
  or raw SHA-256 of `C(record)`, both refuse. All three values are distinct in my
  vector (`RS-DIG-1`), as the contract requires.
* `RS-N17` — a retained `PreparedOutputSetV3` that **no universe selected** is
  refused: bytes in custody never enter a resolution by being in custody.
* `RS-N7…N11` — an empty clone view under partial ownership cannot claim
  `complete`; `unknown` with a null deficiency is an undisclosed gap; an unrelated
  but schema-valid `budget-exhausted`, a null cause and a wrong ownership cause
  each refuse separately, so the four faults stay separable.

---

## 4. Issues

### MUST-1 — `EvidenceRequirement.deficiency` cannot express four of the nine outcomes its only producer emits

**Selector:**
`docs/coop/design-corrections/workflows/schemas/repair.schema.json#/$defs/EvidenceRequirement/properties/deficiency`
→ `urn:opensip:product-v1:workflows:common#/$defs/D9Deficiency`.

The field's only defined producer is native §4.6 `sufficiency_v2`, whose outcome
vocabulary is `DeficiencyV2`
(`native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2`, and the §10
precedence list). Four of its nine members are **not** in `D9Deficiency`:

```
derivation-policy-unmet   external-consumers-unknown
input-closure-incomplete  resolution-incomplete
```

`resolution-incomplete` is exactly what §4.6 step 6 mandates for a
`universal-negative` under `unresolvedEdgePolicy: forbid` over an affected target
— the case a destructive unused-code recipe turns on, and the case workflows §6
routes through this record. Three conforming readings exist and they disagree:
write the D9-mapped `verdict-indeterminate` (collapsing all four successor
members and destroying the per-requirement distinction native §10 went to length
to preserve); write the `sufficiency_v2` value (schema-invalid for four of nine);
or omit the optional field (dropping the disclosure). No document states which
vocabulary the field carries, and no mapping is published in either direction.

The `DomainDetailCode` route native §10 names does **not** resolve it: that
vocabulary covers a *different* five members
(`budget-exhausted`, `derivation-policy-unmet`, `external-consumers-unknown`,
`input-closure-incomplete`, `resolution-incomplete` — but not
`confidence-floor-unmet`, `language-tier-unsupported`, `provider-unavailable`,
`required-relation-missing`). The union of the two vocabularies covers all nine;
**neither single field does**, and `EvidenceRequirement.deficiency` is a single
field. Vector `GAP-1`.

**Remedy (one of):** re-type the field to `DeficiencyV2`; or state normatively
that it carries the D9-mapped value and publish `DeficiencyV2 → D9Deficiency`; or
split it into a D9 field plus a native-cause field. Any of the three closes it;
what an implementer must not have to do is choose.

### MUST-2 — `TypeScriptConfigGraphV1.nodes[].kind` has no published derivation, and it is hashed into `RunId`

**Selector:**
`docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1/properties/nodes/items/properties/kind`;
prose at `native-evidence.md` §2.2 line 940.

The prose says *"Node kind agrees with its path as specified by the schema and
native admission."* The schema supplies only the three-member enum
`{tsconfig, jsconfig, other}`. No path→kind rule appears anywhere in this kit,
and no `native admission` rule for it is published.

`kind` sits inside the hashed record: `tsconfigGraphHash` is the raw SHA-256 of
`C(TypeScriptConfigGraphV1)`; `TypeScriptUniverseV2ResolvedInputs` **requires**
it and `bind_typescript_universe` checks equality; the universe H identity is
`fact.sourceUniverse` and `subject-scope.sourceUniverse`, hence `fact2`,
`scope2`, `coverage2`, `view2`, `evidence2`, `seal2` and `run2`.

Two natural readings disagree on real files:

* **basename exactly** — `tsconfig.json` → `tsconfig`, `jsconfig.json` →
  `jsconfig`, everything else → `other` (what I used); or
* **basename prefix** — any `tsconfig*.json` → `tsconfig` (the widespread
  `tsconfig.build.json` / `tsconfig.base.json` convention).

Discriminating file: `tsconfig.build.json` reached as a base of the entry —
`other` under the first reading, `tsconfig` under the second, two different
`tsconfigGraphHash` values and **two different RunIds for one repository**.
The `configOrigin` derivation does not pin it: `other` and `tsconfig` both derive
`tsconfig`, and a **non-entry** node's kind affects no derived value at all yet is
still committed to the identity. Vector `GAP-2`.

This is the contract's own standard. CB4-SHOULD-2 elevated exactly this class of
defect for `analysis-spec.requestedCapabilities[].capabilityId` — *"two conforming
hosts requesting the same analysis of the same unit therefore mint different
`analysisSpecDigest`s, different `PlanId`s and different `RunId`s, which defeats
independent replay across machines"* — and closed it by naming the vocabulary
authority. The same closure is owed here.

**Remedy:** publish the path→kind rule beside the enum (a `x-opensip-vocabulary`
annotation naming the authority would match the pattern already used for
`capabilityId`), and state it for non-entry nodes as well as the entry.

### SHOULD-1 — no published map from the closed command name vocabulary to `MutationOperation`

**Selectors:** `workflows/command-inventory.v1.json#/commands[]` (45 commands, the
declared **sole** command list, whose `Command` record carries **no**
`mutationClass` field) and
`workflows/schemas/repair.schema.json#/$defs/MutationOperation` (24 members).

Three of the ten mutation-class commands have no same-named operation:
`waive`, `policy-init`, `baseline-upgrade`. Their operations
(`waiver-change`, `policy-write`, `baseline-upgrade-apply`) are inferable but
unpublished. `mutationClass` is a **public** envelope field, and workflows §1
makes `MutationReplayScopeV1.operation` equal to it, so it enters the
`H("workflow.mutation-intent", scope)` preimage of the published
`idempotencyKey`. Vector `WF-11` / `GAP-3`.

Bounded impact, which is why this is SHOULD and not MUST: `requestId` is
host-minted and unique per invocation, so a spelling difference cannot cause a
false or missed dedupe *across* hosts, and the key grants no authority. What is
lost is a consumer's ability to derive the expected `mutationClass` from the
contracts alone.

### SHOULD-2 — the Coverage-partition "without omissions" clause has no decidable referent for symbol relations

**Selectors:** `identity-and-evidence.md` §3, *"Coverage scopes partition the
claimed universe without overlaps or omissions"*, against `native-evidence.md`
§1.2, *"Which relations owe totality is stated in the relation registry
(`coverageTotality`), where only `file` has a row, and never inferred."*

The overlap half is decidable (pairwise disjointness of subjects within one
`(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` key). The
omission half is not, for the nine `symbol`-kind relations: native §1.2 itself
states that the enumerator's attribution of symbols to files is **trusted and not
re-derivable from the retained Run**, and no document publishes an enumeration of
the symbol universe. Two conforming readings — "the claimed universe" as the union
of the scopes' own committed subjects (making the clause vacuous and the sentence
an overlap rule) or as what exists (making it unenforceable and inconsistent with
the `coverageTotality` registry). Vector `GAP-4`.

I used the registry reading and enforced overlap-freedom separately. The registry
statement is the more specific successor and does resolve it in practice; what is
missing is the reconciliation in the text, which an implementer must currently
supply.

### Advisory (non-blocking)

* **ADV-1 — `js-synthesized` recognition vs §1.4 U-1.** §1.2's recognition row
  admits a `tsjs` unit for *"`package.json` present **or any** `.js/.mjs/.cjs/.jsx`
  file under the unit"*, while U-1 requires a directory to hold one of the three
  markers to yield a unit at all. Under U-1 the second disjunct is unreachable and
  a directory of bare `.js` files is **not** a unit (its files are `grammar-only`).
  U-1 governs — it is the specific model with the closed `WorkspaceUnitV2` record
  and the exactly-once `FileMembershipRowV1` law — but an implementer reading §1.2
  alone would mint units for bare-`.js` directories, changing both membership and
  the Plan. Vector `GAP-5`; I used U-1.
* **ADV-2 — the scope of `native.confidence.v1`.** §4.8 defines the method as
  *"declared-exact: every admitted checked fact is 1000000 under its universe; **no
  value below 1000000 is produced by a native provider**"*. The second clause is
  unscoped, yet §4.6's own named regression case exercises a `clones` fact at
  `confidenceMillionths` 100000, and sufficiency step 3 compares the field for
  every relation. The clause must be read as scoped to the `types@checked` method
  it defines, or step 3 and that regression case are both unreachable. Vector
  `GAP-6`; I used the types-scoped reading.
* **ADV-3 — the successor D9 artifact is owed, and the contract says so.** Native
  §10 states plainly that `d9-exit-contract.v1.14.json` keeps its bytes and that
  publishing the successor D9 artifact belongs to that unit. A checker reading the
  inherited artifact alone would refuse a lawful `host-invariant` termination. I
  record this because it is a live cross-unit dependency for implementation, not
  because the design is unclear — it is disclosed, bounded, and correctly attributed.

---

## 5. What I had to invent, and what I deliberately did not

**Invented — and I flag each as an assumption, not a reconstruction:**

1. The path→`kind` rule for `TypeScriptConfigGraphV1` nodes (MUST-2). I chose
   exact-basename matching. It changes `RunId`.
2. The value written to `EvidenceRequirement.deficiency` for the four
   inexpressible outcomes (MUST-1). I left the field absent in my vectors rather
   than write a value the schema refuses or a value that loses the distinction.
3. The `waive` → `waiver-change` mapping (SHOULD-1).
4. The referent of "the claimed universe" (SHOULD-2). I used the registry reading.

**Algorithm freedom deliberately left to implementation — not gaps.** I did not
count any of these as findings: the clone `near-v1` shingling, the `tsjs-erasure-v1`
projection details, query planning (explicitly an optimization only, held to
agree with a retained full scan), the choice of which spans a producer cites for a
code fact (a real statement about what it read, with no cross-provider anchor
identity promised), the internal diagnostic key space, and the physical storage
carrier. Each of these is a genuine implementation choice whose *public* boundary
is contracted.

**I did not have to invent** — and want to record it, because these are the places
a weaker contract would have forced me to: the `subjectScopeCommitment` producing
recipe (§4.1a, closed, and it is the *same* digest as `scope2`); the
`unitId` preimage (published four-field record, `derived` retention, not an opaque
digest); the L0 double-length-prefix reading (named explicitly); the `libSelection`
→ component `fold` (named as full non-tailored default lowercase, with the three
discriminating code points and a declared UCD version); which of `projectionSha256`
/ `configProjectionSha256` / `raw(C(record))` each field carries; the dialect
selection order and its per-step causes; the syntax capability law's inventory
exemption at **both** boundaries; and the `(deficiency, nativeCause)` carrier per
row. Every one of those would have been an invention in a less complete kit.

---

## 6. Limitations of this review

* This is a **design reference exercise**. Nothing here qualifies a product,
  authorizes implementation, or awards a readiness grade. Passing my checks is not
  product qualification.
* Every OS, filesystem, compiler, Cargo, provider, cryptographic and SQLite
  observation in my vectors is a **synthetic trusted observation** — an assumption,
  never native enforcement proof. I executed no compiler, no repository code, no
  provider and no ledger. Real fsync/SQLite/process-death, ACL and O_NOFOLLOW
  custody races, concurrent readers and writers, cross-machine replay, hostile
  archive import and renderer parity remain future qualification work, and I
  treated their absence as such rather than as a design defect.
* My closures, trees, manifests and signatures are synthetic; a signature check
  proves only that a signer signed those bytes, and I made no trust claim.
* I did not review the security unit's S4/S5/S6/S7/S9 time, root-chain, revocation
  and lease machinery beyond the joins the reconstruction needed (S3 discovery,
  S10/S10.1/S10.2 authorization, S12/S12.1 refusal projection). A separate pass
  would be needed to reconstruct those.
* Byte-level values in my vectors depend on my synthetic inputs. What is
  independently meaningful is the **recipe** each value was computed by, the
  refusals, and the disagreements between two conforming readings — not the digests
  themselves.
* I verified only the schemas the kit contains. Where a document is named but
  absent from the kit by design (author reference models, fixtures, checkers), I
  reconstructed the law from the prose rather than assuming the repository omitted
  it, and none of those absences blocked a promised vector.

---

## 7. Verdict

**CHANGES_REQUIRED.**

This is a strong contract set. Every promised vector was constructible from these
inputs alone, with one exception (MUST-1, where the schema refuses the value its
own producer emits), and the two identity-critical recipes I most expected to be
under-specified — the `subjectScopeCommitment` producing recipe and the Rust
compilation-unit dialect selection — are closed, precise, and reproduced exactly
by an independent implementation. The design's strongest property is the closing
digest law: **no default**, so a 64-hex field without an annotation refuses. That
law is what let me find MUST-2 mechanically, by asking of every field I had to
populate "what must this value *be*?" — and finding one hashed field where the
contract answers only "as specified by the schema and native admission", and
neither does.

The two MUST issues are narrow, precisely located and independently fixable, and
neither is architectural: one is a field type that must name its vocabulary, the
other is a derivation rule that must be written down beside a field that is
already correctly hashed. Both are the same class of defect the contract set has
already corrected twice by its own initiative (CB3-MUST-1's ladder, CB4-SHOULD-2's
capability vocabulary), and both would defeat exactly the property the set most
insists on: independent replay across machines. That is why they block rather than
advise. The two SHOULD issues are reconciliations the text owes a reader, not
choices the design has failed to make.

I would expect a corrected revision to be reconstructable without invention.
