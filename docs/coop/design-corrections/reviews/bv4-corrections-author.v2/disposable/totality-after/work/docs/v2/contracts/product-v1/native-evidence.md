# Native evidence contract — TypeScript/JavaScript and Rust cells, sealed inputs, resolution completeness

**Standing:** PROPOSED. Authored by actual Claude (native owner) under D-367 delegated
design authority for the D-371 intended product. Not adopted, NOT SELF-ACCEPTED.
Codex reviews these bytes; a fresh Claude session reviews the integrated package.
A prospective D-372 act names replacement selectors and applicability. Nothing
here edits a frozen source, awards a grade, authorizes implementation, or claims
platform qualification. Reference checks in
[`docs/coop/design-corrections/native/`](../../../coop/design-corrections/native/README.md)
are design evidence, not product measurement. This revision answers the twelve
items retained in `reviews/native-author-feedback.v1.md` (F1–F12) and seven
further CHANGES_REQUIRED items, R1–R7 (co-located per-language units, inert
generated-file inputs, single canonical import payloads, closed joins H-1…H-5,
import-only clone exclusion, Config2/backup custody join, fault law). The only
retained record of R1–R7 is their statement in
`native/native-cases.v2.json#feedbackMap` and the README table; no separate
Codex review document for them is retained in the repository, and none is
claimed. The post-reset independent Claude review of the frozen
`candidate-subject.v1` (retained in the repository at
`docs/coop/design-corrections/reviews/post-reset-review.v1/review.md` with
executable probes) returned MUST-3, SHOULD-4 and SHOULD-7 against this unit; the
new author session's corrections and handoff are retained at
`docs/coop/design-corrections/reviews/post-reset-author.v1/handoff.md` (items
`PR-MUST-3`, `PR-SHOULD-4` in the feedback map). The second independent review,
of the frozen `candidate-subject.v2`, returned N-1 (nested repository/project
boundaries not carried into unit discovery or the Plan scope) and advisory A-3
(an explicit Cargo workspace root lost member folding) against this unit; a
further Claude author session corrected them here (items `PR2-P3`, `PR2-P22`:
§1.4 U-2, U-8, §10, §13 H-8). The earlier author handoff file
`reviews/native-fix-handoff.v3.md` is empty (the authoring session was
interrupted), is cited nowhere as evidence and is no longer a consumed source
of the checker. A third independent session — a fresh blind consumer
reconstruction of the accepted `candidate-subject.v5` subset — returned M-1 (no producing
recipe for `subjectScopeCommitment`), M-2 (no TypeScript native-context record) and
advisories A-1/A-2 against this unit; a further Claude author session corrected them here
(§0, §2.2, §2.3, §2.4, §4.1a, §9.4, §10, §11, §12, §13; items `CB-M1`, `CB-M2`, `CB-A1`,
`CB-A2` in the feedback map) and swept §13/§14 for obligations already discharged in current
bytes. These are successor edits: the acceptance of `candidate-subject.v5` does not cover
them, and they require a fresh independent review of a newly frozen subject.

**Resolves:** AR-07 (sealed Rust dependency inputs and an honest execution
boundary), AR-12 (examination completeness is not resolution completeness),
AR-13 native cells (exact TypeScript/JavaScript/Rust cells, mixed repositories,
clone equivalence modes, zero-config recognition, import evidence payloads).
Owner rows: DR-118/119 (cells, inputs, execution limits), DR-004 (resolution
completeness law), DR-118 (import payload semantics).

**Joint interfaces honored.** Product source identity is `snapshot2`, Plan is
`plan2`, product fact records are `fact2`, coverage is `coverage2` over a
`CoverageResultV3` payload, and every import is one `import2` wrapper from
`foundation/identity-schemas.v2.json`. This contract authors typed payloads and
native records only; it does not define another serializer or another import
recipe. The reference model imports `foundation/canonical.py` for exact typed
admission, canonical bytes and `H(domain, descriptor)`, and
`foundation/identity-model.py` for the `import2` identifier. Operational
admission, retention, CLI spelling and step ordering are the workflow owner's;
D9 class assignment is host-owned and every new typed detail maps explicitly in
§10.

---

## 0. Superseded selectors (exact) and what replaces them

Historical bytes are unchanged. A D-372 act would apply these replacements.

| Source (pinned in `native/source-pins.v2.json`) | Selector | Disposition |
|---|---|---|
| `docs/coop/artifacts/delivery.v2.json` | `$.rustSemanticSubstrate.repositoryExecution.withGrant` ("with network disabled") | **Superseded** by §5: preparation is *disclosed trusted-code execution* under `AuthorizedExecutionV2`; a network bound is `DISCLOSURE-ONLY` unless the security owner's platform truth table asserts an enforced primitive. |
| `docs/coop/artifacts/delivery.v2.json` | `$.rustSemanticSubstrate.offlineAssets` | **Extended** by §3: sealed `DependencySourceSetV1` is a Plan-bound input class, never an offline asset. |
| `docs/coop/artifacts/delivery.v2.json` | `$.typescriptSemanticSubstrate.wireSchema.definitions.CoverageResultV1.completenessRule` | **Superseded** by `CoverageResultV3` (§4.3): the exhaustive examined partition remains; a five-state `resolutionCompleteness` record is mandatory. |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` (same selectors retained verbatim in the v3/v4 candidates) | `$.repositoryExecution.preparedOwner` ("network-disabled"), `$.repositoryExecution.forbidden` | **Relabeled**: "no network fetch" is a first-party design invariant verified by conformance, not an enforced confinement (§5.5). The semantic worker executes no repository code in any mode (§5.3). |
| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.definitions.RepositoryResolutionV2`, `$.wireSchema.definitions.CoverageResultV2`, `$.wireSchema.payloadSchemas.UnavailableV2.fields.reason`, `$.limits`, `$.orderingAndStateMachine.stateRecord.phaseValues` | **Superseded** by protocol major 3 frames, identity negotiation, limits and phases (§9). |
| `docs/coop/artifacts/resolved-inputs.v2.json` | `$.planIdContract.semanticUniverseSchemas.rust-v1.resolvedInputs`, `...typescript-v1.resolvedInputs` | **Superseded** by `rust-v2` and `typescript-v2` universes (§2). |
| `docs/coop/artifacts/resolved-inputs.v2.json` | `$.projectModel.semanticUniverse.perProvider.rust.ifIncomplete`, `...typescript.ifIncomplete` ("provider-unavailable") | **Superseded**: an incomplete *input closure* with an installed provider is `input-closure-incomplete` (§10), never `provider-unavailable`. |
| `docs/coop/artifacts/fact-plane.v1.json` | `$.sufficiency.rule`, `$.sufficiency.completenessRule`, `$.deficiencyVocabulary.values`, `$.requirementSchema.fields.completeness`, `$.knownLimitations[5]` (R1-FP-03) | **Superseded** by §4 (requirement v2, view entry v3, sufficiency v2, four new deficiencies). |
| `docs/coop/artifacts/fact-plane.v1.json` | `$.relationRegistry.relations`, `$.factRecordContractV1.relationPayloadSchemaRegistryV1.schemas` | **Extended** with relation `unresolved-edge` (§4.4). Existing relation payload grammars are reused by exact `payloadSchemaDigest` inside `fact2`. |
| `docs/coop/artifacts/check-fact-plane.py` | `sufficiency` (lines 571–612) | **Superseded** by `sufficiency_v2` in `native/native_evidence_model.v2.py`; v1 semantics retained there as the counterexample oracle (`sufficiency_v1`). |
| `docs/coop/completion/analysis-quality-completion.v2.md` §3; `docs/coop/completion/language-quality-matrix.completed.v2.json` `$.rows` | TypeScript-only capability registry and 24 cells | **Extended** by `native/native-capability-matrix.v2.json` (§1): TypeScript cells retained, JavaScript, Rust and cross-TS/JS clone cells added. |
| `docs/coop/artifacts/c2-plan-stage-schema.v4.json` | `$.coverageKey.key[subjectScopeCommitment]` | **Retained (shape) and extended (§4.1a)**. The field keeps its retained meaning — it proves membership of the examined set and nothing more (§4.1). The retained selector's own deferral, `"SHAPE ONLY; computation and verification stay deferred (R1-C2-03)"`, and its `EXAMPLE ENCODING for the fixtures only` note are historical bytes that stay unchanged and remain a non-recipe; §4.1a supplies the successor producing recipe the deferral left open. |
| `docs/coop/artifacts/fact-identity-policy.v2.json` | `$.normalisationLadder`, `$.canonicalisationSchema` | **Retained**. Clone fact modes (§6) reference these levels; `near` and `cross-tsjs` are candidate algorithms and never fact identities. |
| `docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json`, `common.schema.json`, `test-execution.schema.json` (current bytes, pinned) | `#/$defs/PayloadRegistryV1`, `#/$defs/ImportWrapperV2`, `#/$defs/RuntimePayloadV1`, `#/$defs/HistoryPayloadV1`, `test-execution#/$defs/TestPayloadV1`, `common#/$defs/SourceCorrespondence`, `#/$defs/SourceMappingV1` | **Joined** (§7, H-5 closed): these are the single canonical runtime/test/history payload schema documents, the wrapper digest recipes and the shared correspondence/mapping records. Native normalizes its adapter shapes into them before `import2`. The earlier `H('import-<kind>')`/`snap1:` bytes are gone from the workflow unit. |

Not touched by this unit: root discovery rule and trust boundary (DR-103, foundation
owner), platform OS baseline population (DR-126, security owner), HTML/agent
projections (DR-122, workflow owner), D9 reason-code vocabulary bytes (host owner).

---

## 1. Supported native cells (AR-13)

### 1.1 Cell coordinates

A cell is `capability × languageMode × platformFamily`. The machine-readable
matrix is `native/native-capability-matrix.v2.json`, validated by
`NativeCapabilityMatrixV2`; its `cells` array is the **complete product** of its
own `capabilities` and `languageModes`, and the reference checks hold it to
exactly that product rather than to a number written here. (A literal count in
this prose said `60` while the matrix held 66; a second hand-maintained counter
would only go stale again, so the count is derived from the two arrays and
reported by the checks instead of restated.) Platform families are exactly the
four `platformId`
values in the delivery release inventory: `linux-x86_64-gnu`,
`linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64`. The OS/kernel/libc/filesystem
*baseline* that qualifies a machine into a family is owned by the security unit
(AR-06); this contract states only that native capabilities are platform-invariant
by design (`platformInvariantDesign: true`) and that no cell is `QUALIFIED` here.

Cell states (closed): `SUPPORTED-DESIGN` (contracted behavior, corpus named,
qualification pending), `UNSUPPORTED-TYPED` (refuses with the named deficiency;
never silently narrows), `NOT-SELECTED` (outside D-371; no promise).

### 1.2 Language modes (closed)

| Mode id | Recognition | Universe | Notes |
|---|---|---|---|
| `ts-tsconfig` | `tsconfig.json` at the unit root (or named by discovery), `allowJs` absent/false | `typescript-v2`, `configOrigin=tsconfig` | JavaScript files are not program roots; a JS import target is `unresolved-module-specifier`. |
| `js-allowjs` | `tsconfig.json`/`jsconfig.json` with effective `allowJs=true` (jsconfig defaults `allowJs=true`) | `typescript-v2`, `allowJs=true` | `.js/.mjs/.cjs/.jsx` are program roots. |
| `js-synthesized` | No `tsconfig.json`/`jsconfig.json` at the unit root; `package.json` present or any `.js/.mjs/.cjs/.jsx` file under the unit | `typescript-v2`, `configOrigin=synthesized`, `synthesizerVersion=1` | Host synthesizes `SynthesizedCompilerOptionsV1` (§2.2); Plan-bound with `DEFAULTED` provenance, disclosed in output. |
| `rust-cargo` | `Cargo.toml` at the unit root (package or workspace) | `rust-v2` | Requires a sealed `DependencySourceSetV1` when the lock lists any non-path package (§3). |
| `rust-cargo-prepared` | as above, plus an admitted `PreparedOutputSetV3` of inert rows | `rust-v2` with `preparedOutputSetId` non-null | Expansions and directives are consumed as data; a site without a row is an unresolved edge (§3.6). |
| `syntax-only` | any file whose extension maps to a bundled grammar | `syntax-v2` (grammar-only; no compiler) | Inventory/syntax/clones only; semantic rungs `language-tier-unsupported`. |

**The syntax-only universe (CB3-MUST-3).** This column previously read
"none (syntax-all provider)", and that made the mode's own advertised cells
unrepresentable. `fact2` and `subject-scope` both **require** a
`native-semantic-universe` h-identity, that domain set held exactly the
TypeScript and Rust universes, and there is no null branch — so a
`declares@syntactic` or `clones@normalized-body-hash` fact in `syntax-only`
mode, and every `file`/`package`/`vcs-change` fact in a repository containing
no TypeScript and no Rust unit at all, could mint no fact and no scope. An
implementer had to invent a third domain, invent a null branch on a required
identity field, or quietly narrow this table.

The registered answer is a third universe, `native.semantic-universe.syntax.v2`,
over a third native context, `native.context.syntax.v2`. Making the universe
fields nullable was rejected: it would delete the invariant that every fact
states what produced it, and would leave "which grammar read this body"
unanswerable for exactly the facts that depend on the answer.

- **What it carries.** The context holds one thing: the installed
  `SyntaxGrammarBundleV1`, pinned the way a toolchain is — an admitted
  `kind=grammar` closure, a `parserVersion` that must equal that closure
  manifest's `semanticVersion`
  (`native.syntax-grammar-version-not-from-manifest`), and every grammar
  definition, the bundle manifest and the normalizer specification present in
  the retained tree. It has no toolchain, no stdlib, no lockfile, no
  `node_modules` layout and no config graph, because a grammar-only analysis
  reads none of them. A syntax-only context that named a compiler would assert
  semantics the mode never computes.
- **What the universe commits.** The admitted context plus the **selected**
  grammar set. Selecting a different set is a different universe, exactly as
  selecting different compilation targets is for Rust, so what was parsed is
  visible to every consumer instead of being an invisible default. A selection
  naming a grammar the bundle does not contain refuses
  (`native.syntax-grammar-not-in-bundle`). The constant
  `resolutionAttempted=false` is carried so no consumer can read the universe
  as a resolution claim.
- **The body dialect axis.** `body-language-version.dialect` gains a third
  branch, `{grammarVariant}`. A syntax-only analysis has no compilation unit, so
  it has no edition to select and no program to join; claiming `{edition: 2021}`
  for a `.rs` body read without Cargo would fabricate compiler semantics. One
  suffix must map to one grammar
  (`native.syntax-grammar-suffix-ambiguous`), longest match wins, and a suffix
  with no bundled grammar refuses rather than being folded into a neighbour —
  which is what keeps `unsupported-file / no-bundled-grammar` an honest
  classification. Because it is a distinct branch, **a grammar-parsed body never
  mints the same identity as a compiler-parsed one over the same bytes.** That
  is required: a grammar parse and a compiler parse are different
  interpretations, and equating them would be a false clone claim.
- **Capability is not widened.** A `syntax-only` universe carries only the
  inventory rungs, the `syntactic` rungs and `clones@normalized-body-hash`.
  `imports`/`references`/`calls`/`types`/`reachability` remain
  `language-tier-unsupported` under it, `unresolved-edge` stays unavailable
  because no resolution was attempted, and a universal-negative predicate still
  requires its own complete `CoverageResultV3`. Nothing here lets a syntax-only
  Run claim a resolved or type fact.
- **The bundled grammar set is closed, and it has SEVEN languages.** The host
  bundles grammars for `rust`, `typescript`, `javascript`, `json`, `toml`,
  `markdown` and `yaml`; the shared discovery rule routes all fourteen of their
  suffixes to membership `syntax-only`, reason `grammar-only`. An earlier
  revision of this section let the grammar descriptor name only the three code
  languages and asserted equality with the `body-language-version` `languageId`
  enum as a drift check. That check proved the enum matched itself: it could not
  express the four data/document grammars the host has always shipped, so the
  promise directly above — *any* file whose extension maps to a bundled grammar —
  was unrepresentable for them. The descriptor now covers exactly the bundled
  set, and each row declares its **`syntaxClass`**.

**`code` versus `data-document`: the distinction the contracts already draw.**
This is not a new narrowing; it is an existing law made machine-readable.

- **`code`** — `rust`, `typescript`, `javascript`. §6.3 defines body spans as
  function, method, closure/lambda, `impl` item and block bodies, publishes the
  L2/L3 normalisation tables for exactly these languages, and puts
  `languageId ∈ {typescript, javascript, rust}` in the clone preimage. These
  grammars bear clone body identity and the code-construct syntax relations, and
  their `languageId` **must** be a member of the `body-language-version` enum.
- **`data-document`** — `json`, `toml`, `markdown`, `yaml`. These formats have no
  such body spans, and this kit publishes **no** tokenisation, `literalKind`
  mapping or normalisation law for them anywhere. Their files are grammar-only
  members — accounted, inventoried, and never `unsupported-file` — bearing
  `file`/`package`/`vcs-change` inventory evidence under the syntax universe.
  They mint **no** body identity, no suffix of theirs appears in the grammar
  dialect table, and their `languageId` **must not** be in the
  `body-language-version` enum, since it could never appear in a clone preimage.

Both directions are enforced at grammar-bundle admission: a data grammar
claiming `code`, a code grammar demoted to `data-document`, and a row claiming a
suffix the discovery table routes to another language each refuse with their own
typed cause. What is held equal to the `body-language-version` enum is therefore
the **`code` subset**, not the whole bundle — which accounts for all seven
languages instead of ignoring four.

Claiming `declares`/`literal`/`control-flow` facts for a data format would
require a tokenisation law this kit does not publish, and inventing one would be
precisely the fabricated-semantics failure the syntax-only universe exists to
prevent. If the product later wants data-format syntax facts, it needs a
published tokenisation and `literalKind` law first; that is a bounded future
capability and this matrix does not promise it today.

An unbundled language stays unrepresentable: `.py` has no bundled grammar, is
not in the descriptor vocabulary, and its files remain `unsupported-file` with
reason `no-bundled-grammar`.

**The capability law binds facts and Coverage, not just descriptors.** Validating
a grammar bundle's declared `syntaxClass` constrains what a bundle may say about
itself; it does not constrain what a Run may claim. An earlier revision enforced
the registry only there, and full Runs consequently admitted a Markdown-anchored
`declares` fact, a **complete** empty `declares`/`clones` Coverage over a
data-only repository, and `references@resolved-binding` under a universe whose
own record declares `resolutionAttempted: false`. The registry is therefore
consulted at the two boundaries that decide what a Run asserts, and at neither
does it consult the claimed coverage value, the caller-declared class, or
whether facts happen to exist:

- **Every admitted fact.** A `fact2` under a syntax universe is admissible only
  if **every one of its anchor paths** is read by a **selected** grammar whose
  registry capability set contains that `relation@rung`. The anchor is the file
  the body was actually read from, so a Markdown-anchored code fact refuses in a
  mixed repository exactly as it does in a data-only one
  (`SYNTAX_CAPABILITY_UNSUPPORTED_FACT`). **Inventory capabilities are exempt
  here as well as at the scope boundary below** — the exemption belongs to the
  *relation*, not to the boundary. An earlier revision wrote this bullet as an
  unconditional every-anchor rule and stated the exemption only in the scope
  bullet, so the two bullets contradicted each other: a literal implementer
  refused a `file@enumerated` fact for `tool/main.py` while the scope bullet had
  just promised that the same path's inventory Coverage was unconditionally
  `complete` — an inventoried file that is authoritatively absent. An inventory
  fact is not read by a grammar at all; it *is* the inventory row, the manifest
  declaration or the VCS observation, so there is no grammar for it to be gated
  on. (The relation registry's `anchorLaw` independently gives the inventory
  class **zero** anchors, so such a fact names no anchor path for this bullet to
  test either; the two laws agree and neither leans on the other.) The exemption
  is from grammar ownership **only**: the relation's snapshot joins, own-scope
  attribution and the anchor law all still bind, and no code fact becomes
  admissible because some other anchor in the Run sits on a supported path.
- **Every requested scope, including an empty view.** A `subject-scope` under a
  syntax universe is judged on its committed **examined extent** — the source
  inventory of the snapshot it names. **Inventory** capabilities
  (`file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported`) are
  **always** available and are deliberately **not** grammar-gated: a snapshot
  inventories every file it contains, including ones no bundled grammar reads,
  and requiring a grammar per inventory row would silently narrow that promise.
  A **code** capability requires at least one path in that extent to be read by a
  selected `code` grammar. A capability no selected grammar bears is unavailable —
  which is every semantic rung and `unresolved-edge` under a syntax universe,
  exactly as the matrix already says.

**A promised inventory capability represents every inventoried path, and a
`complete` inventory result may not hide an omitted one.** These are two halves
of one promise and the second was missing. `file@enumerated` is **total** over
the snapshot inventory: a snapshot inventories exactly the files it contains, so
every inventoried path has exactly one `file` fact, and over a **complete**
`file@enumerated` Coverage the predicate `exists file where path=P` is
authoritative. A complete result that retains no fact for an inventoried subject
therefore asserts that an inventoried file is absent, and that graph closed —
nothing derived the obligation, so nothing compared it. A `complete`
`file@enumerated` Coverage must now carry an admitted `file@enumerated` fact for
every one of its subjects that the snapshot inventory contains
(`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`), derived at Run closure from the
retained view's own facts and the retained inventory. Two things it deliberately
does not require: a subject the snapshot does **not** contain is owed nothing —
the host examined the question and the file is genuinely absent, which is the
one case a universal negative over inventory exists to serve — and an `unknown`
result carrying its disclosed deficiency is owed nothing, which keeps a
partially examined inventory representable rather than forcing a false
`complete`. `package@manifest-declared` and `vcs-change@vcs-reported` are **not**
total and owe nothing: most paths declare no package and most were not changed,
so their empty results are ordinary findings. Which relations owe totality is
stated in the relation registry (`coverageTotality`), where only `file` has a
row, and never inferred.

**How many spans a fact cites is a registry law, not an implementer's choice.**
`fact.anchors` carried no `minItems`, and only `clones` ever stated a
cardinality, so every published predicate over the array — the `file` row's
`anchorPathField`, and the every-anchor rule above — was universally quantified
and therefore *vacuously true* at zero anchors. It neither permitted nor forbade
the unanchored spelling, and both spellings of one `file@enumerated` claim closed
a Run with different `fact2` identities. The relation registry now carries a
closed `anchorLaw` on every relation, in three classes: `source-text` (the nine
code relations) needs **at least one** span, because a code fact is read from
source text and an unanchored one names no file that could have been read;
`body-identity` (`clones`) is **exactly one**, unchanged; and `inventory`
(`file`, `package`, `vcs-change`) is **exactly zero**, because such a fact's
whole semantic input is its payload, which the relation's own snapshot joins
already bind. Zero is also the only cardinality *every* inventoried path can
satisfy — including a `vcs-change` whose `changeKind` is `deleted`, whose path is
by construction not in the snapshot and can carry no anchor at all. The
`source-text` class has deliberately **no** upper bound and no canonical extent:
which spans a producer cites is a real statement about what it read, so two
producers citing different spans have produced different semantic descriptors
and legitimately mint different identities. Nothing here promises cross-provider
anchor identity for code facts. Two things this also closes that the previous
wording did not: an unanchored *code* fact was refused only inside this
syntax-universe guard and closed a Run under a TypeScript or Rust universe, and
`anchorPathField` existed only on the `file` row, so a `package` fact anchored
into an unrelated file closed a Run. One law now covers every relation in every
universe (`FACT_ANCHOR_CARDINALITY`).

An **unselected** grammar lends no capability: selection is committed in the
universe identity, so a bundle that ships a Rust grammar the universe did not
select cannot make `declares@syntactic` available for `.rs` files.

**An unavailable request is disclosed, not answered, and never refused outright.**
The capability is retained and representable: the scope closes a Run and carries
`coverage: unknown` with `deficiency: language-tier-unsupported` and
`nativeCause: capability-missing` — both already in the existing vocabulary, and
mapped in §10. A **false `complete`** for an unavailable capability, a wrong or
null cause, and a wrong deficiency each refuse with their own reason
(`SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, `…_CAUSE_MISMATCH`,
`…_DEFICIENCY_MISMATCH`). No syntax Run is made blanket-indeterminate to achieve
this: a data-grammar inventory Run and a code-grammar `declares`/`clones` Run
both still close with a genuine `complete` and no deficiency.

The guard is **syntax-universe specific**. Every capability of the TypeScript and
Rust universes is unchanged, including all five semantic relations, and the Rust
compilation-ownership guards are untouched — see the ownership disclosure law in
§10, whose prerequisite is now derived from the actual universe kind so that a
grammar-only clone scope, which has no compilation unit at all, owes no
compiler-ownership obligation.

**A scope is judged on ITS OWN extent where the published law supplies one.** The
relation registry states, per relation, what `subject-scope.subjects` identify
(`subjectKindLaw`). For a **`source-path`** relation — `clones`, `file`,
`vcs-change`, which bind their subject to a snapshot path through their registry
`snapshotJoins` `pathField` or, for `clones`, through the single `bodyIdentityJoin`
anchor — the subjects **are** the extent, and **every** named path must be
supported. So a `README.md`-scoped clone request is unavailable even in a mixed
snapshot that also contains `src/plain.rs`: an unrelated code file elsewhere does
not serve it, and a scope naming both cannot hide its unsupported part behind its
supported one.

For a **`symbol`** relation the subjects are opaque `SubjectIdV1` values that the
retained record associates with **no** path. The enumerator's attribution of
symbols to files is **trusted** and is not re-derivable from the retained Run, so
the only answerable question is the coarser one — can this universe produce this
capability anywhere in the committed extent — and that is what is asked. Treating
a symbol identifier as a path would reject lawful code scopes, and inventing
symbol-to-path parsing would be fabricated evidence. This is a stated
trust-boundary limit, not an oversight, and a mixed-repository empty `declares`
scope therefore remains admissible.

**Path support is decided by the SELECTED grammar ROWS and their own suffixes**,
not by the set of selected languages. The descriptor permits a row to own a
**subset** of its language's bundled suffixes, and two rows of one language may
own disjoint suffixes; admission requires only that a claimed suffix belong to
that language and that no suffix be claimed twice. A selected TypeScript row
owning `.ts` therefore establishes nothing about a `.tsx` path when no selected
row owns `.tsx`, and longest match runs over the union of the selected rows' own
suffixes so `.d.ts` still resolves through a row owning `.ts`. An unanchored code
fact is **not** vacuously supported: it names no file that could have been read.

**`allowJs` and `checkJs` are not completeness claims** (feedback 11; primary
sources `typescriptlang.org/tsconfig/allowJs` and `/checkJs`, read 2026-09-06).
`allowJs` is a *program-membership* option: it admits JavaScript roots. `checkJs`
is a *diagnostics* option: it reports errors in JavaScript files and changes
nothing about what is resolved. Both are universe keys (they change PlanId);
neither gates a capability, and neither implies that resolution was attempted or
complete. Resolution completeness is asserted only by `CoverageResultV3` (§4.3).
The universe carries `jsAdmittedToProgram`, `jsDiagnosticsEnabled` and the
constant `resolutionCompletenessImplied=false` so no consumer can confuse them.

Module systems inside `typescript-v2` are observed, not chosen: `import`/`export`
and `require()`/`module.exports` are both resolved by the pinned compiler under
`module=node16` semantics keyed by `package.json` `type`. A non-literal specifier
is an unresolved edge (§4.4), never a silent drop.

### 1.3 Capability × mode table

`✓` = SUPPORTED-DESIGN; `◐` = SUPPORTED-DESIGN with the named limitation;
`✗` = UNSUPPORTED-TYPED with the named deficiency; `–` = NOT-SELECTED. All four
platform families carry the same value in every row.

| Capability (relation@rung) | ts-tsconfig | js-allowjs | js-synthesized | rust-cargo | rust-cargo-prepared | syntax-only |
|---|---|---|---|---|---|---|
| `declares@syntactic`, `literal@syntactic`, `control-flow@syntactic` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (`syntaxClass: code` grammars; a `data-document` grammar member is inventoried, never erased, and produces no code-construct fact; no bundled grammar at all is `language-tier-unsupported`) |
| `imports@resolved-target` | ✓ | ✓ | ◐ L-JS1 | ◐ L-RS1 | ◐ L-RS1 | ✗ `language-tier-unsupported` |
| `references@resolved-binding` | ◐ L-JS2 | ◐ L-JS2 | ◐ L-JS1, L-JS2 | ◐ L-RS2, L-RS3 | ◐ L-RS2, L-RS4 | ✗ |
| `calls@resolved-callee` | ◐ L-JS2 | ◐ L-JS2 | ◐ L-JS1, L-JS2 | ◐ L-RS2, L-RS3 | ◐ L-RS2, L-RS4 | ✗ |
| `types@checked` | ✓ | ◐ L-JS3 | ◐ L-JS3 | ◐ L-RS3 | ◐ L-RS4 | ✗ |
| `reachability@from-resolved-calls` | ◐ L-JS2, L-FW1 | ◐ L-JS2, L-FW1 | ◐ L-JS2, L-FW1 | ◐ L-RS2, L-RS3, L-FW1 | ◐ L-RS2, L-RS4, L-FW1 | ✗ |
| `clones@normalized-body-hash` (modes exact/normalized/structural) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (`syntaxClass: code` grammars only — §6.3 body spans and the L2/L3 tables exist for TS/JS/Rust; a `data-document` grammar mints no body identity) |
| `clones` mode `near` (candidate only) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (`syntaxClass: code` grammars only — `near` shingles the L3 token stream of a clone BODY, so it needs the same §6.3 body spans the fact modes need; a `data-document` grammar bears no body and produces no candidate) |
| `clones` mode `cross-tsjs` (candidate only, §6.4) | ◐ L-CL1 | ◐ L-CL1 | ◐ L-CL1 | – | – | – |
| `unresolved-edge@observed` (§4.4) | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ (no resolution attempted) |

TypeScript `references`/`calls` carry L-JS2 as well: computed member access,
`any`-typed calls and structural dispatch exist in TypeScript programs, not only
in JavaScript. The v1 draft's `✓` for those cells was wrong.

Limitations (closed ids; each is disclosed in Coverage, never hidden):

- **L-JS1** synthesized options: `paths`/`baseUrl`/`rootDirs`/custom `types` are unknown; a specifier resolvable only through them is `unresolved-module-specifier`.
- **L-JS2** dynamic forms: computed member access, non-literal `require`/`import()`, indirect `eval`, reflective access and `any`-typed calls produce unresolved edges; resolution completeness for universal negatives is then `incomplete` (§4).
- **L-JS3** JavaScript types without annotation or JSDoc are `compiler-inferred` (§4.8). They are exact under the admitted universe and carry no probabilistic confidence; a rule pack that wants declared types uses `derivationPolicy=declared-only`.
- **L-RS1** external crates: every non-path package in `Cargo.lock` that unified feature resolution activates for the target must be present in the sealed dependency source set; otherwise the dependent crate's semantic rungs are `input-closure-incomplete` (§3.5). Syntax rungs remain complete.
- **L-RS2** dynamic dispatch and generics: `dyn Trait` calls resolve to the trait method declaration and are recorded as `trait-object-dynamic-dispatch` unresolved edges; generic bound calls as `generic-bound-dispatch`. Both count against resolution completeness for universal negatives.
- **L-RS3** non-prepared generated code: procedural-macro and build-script outputs are absent; each external proc-macro invocation site is a `macro-expansion-unavailable` edge and each package with a build script contributes `build-script-generated-unavailable`. `types@checked` on items whose type depends on such generated code is `unknown` with `input-closure-incomplete` (cause `generated-output-unavailable`). Declarative `macro_rules!` expansion is compiler-native and fully supported.
- **L-RS4** prepared mode: only inert `macro-expansion`, `build-script-directives` and `generated-file` rows are consumed (the last through the read-only virtual `OUT_DIR`, §3.6 PO-4); a site or owner without a matching, non-stale row falls back to L-RS3 behavior for that site.
- **L-FW1** entry points: `reachability` universal negatives need an origin set; without a recognized framework or explicit origins they are `resolution-incomplete` with class `entry-point-unrecognized` (§8).
- **L-CL1** cross-TS/JS candidates use the `tsjs-erasure-v1` syntax projection; bodies with runtime-significant TypeScript tokens are excluded; a candidate is never a fact, never semantic equivalence and never a deletion prerequisite (§6.4).

### 1.4 Mixed repositories and workspace units (R1)

The v1 rule ("deepest root, then `Cargo.toml` > `tsconfig.json`") was wrong: in a
repository whose root holds both `Cargo.toml` and `package.json`/`tsconfig.json`
every TypeScript file fell into the Rust unit and silently left the TypeScript
program. Units are now **per language family and program membership**, and may
share a root.

**Reference discovery model** (`discover_units`, `assign_membership` in the model;
records `WorkspaceUnitV2`, `FileMembershipRowV1`, `UnitMembershipV1`). The root
discovery boundary and trust decision remain the security/foundation owners'
(DR-103); this contract defines what happens inside that boundary.

`WorkspaceUnitV2` (closed): `{unitOrdinal, rootPath, languageFamily: rust|tsjs|none,
languageMode, unitKind: cargo-workspace|cargo-package|ts-program|js-program|syntax-only,
markerPath, markerSha256, recognizerId, recognizerVersion, provenance:
EXPLICIT|DISCOVERED|DEFAULTED, memberPackageRoots[]}`.

- **U-1 (one unit per directory and language family)** A directory holding
  `Cargo.toml` yields a `rust` unit; a directory holding `tsconfig.json`,
  `jsconfig.json` or `package.json` yields exactly one `tsjs` unit whose mode is
  chosen by precedence `tsconfig.json` (→ `ts-tsconfig`/`js-allowjs`) >
  `jsconfig.json` (→ `js-allowjs`) > `package.json` (→ `js-synthesized`). The
  precedence selects the mode **within** `tsjs`; it never removes the co-located
  `rust` unit. A root with both markers has two units with the same `rootPath`
  (`units-colocated-cargo-and-package-json-root-keeps-both-languages`).
- **U-2 (Cargo workspace folding)** A `Cargo.toml` package inside a Cargo
  workspace root's tree is folded into the workspace unit as a member package
  (Cargo resolves the workspace as one program); it is listed in
  `memberPackageRoots`, not as a separate unit. A standalone package outside any
  workspace is its own `cargo-package` unit. **Explicit roots are unit
  selection, never loss of Cargo workspace semantics (post-reset v2 A-3/P22):**
  naming a Cargo workspace root explicitly yields exactly the automatic result
  for that unit (members folded, member `target` output pruned, a member's
  `src/target` still source); naming a member package alone selects that package
  as its own `cargo-package` unit, and files of the unselected root or siblings
  are honest `no-program-unit-for-language` rows, neither claimed nor
  over-ignored (`units-explicit-cargo-workspace-root-keeps-member-folding-and-member-target-pruning`).
- **U-3 (deterministic membership within a language)** A file's family is fixed
  by extension (`.rs` → `rust`; `.ts/.tsx/.mts/.cts/.js/.mjs/.cjs/.jsx` → `tsjs`).
  It belongs to the **deepest unit of its own family** whose root prefixes its
  path. Units of another family never claim it. Nested monorepo packages
  (`packages/web/tsconfig.json` under a root `tsconfig.json`) are therefore
  distinct `tsjs` units and the deeper one wins for its subtree
  (`units-nested-monorepo-deepest-within-language-and-workspace-folding`).
- **U-4 (no source erasure; honest unsupported files)** Every snapshot inventory
  file appears in exactly one `FileMembershipRowV1`: `program-member`;
  `syntax-only` with reason `no-program-unit-for-language` (a `.rs` file with no
  enclosing Rust unit: semantic rungs `unknown`, cause `no-program-unit`),
  `grammar-only` (bundled grammar, no program) or `host-ignore-convention`
  (the file lies inside a pruned tree of the shared rule below); or
  `unsupported-file` with reason `no-bundled-grammar`, listed in
  `unsupportedFiles`. `erasedFiles` is a schema-constant empty array
  (`maxItems 0`) and the model refuses a membership that does not cover the
  inventory exactly once.
- **U-4a (one shared discovery rule; post-reset MUST-3)** The host ignore
  conventions and unit enumeration are stated once, in
  `docs/coop/design-corrections/discovery-defaults.py`, and consumed by both
  `discover_units`/`assign_membership`/`unit_scope_descriptor`/`typescript_mode`
  here and by the security discovery instrument (security S3). Pruned trees,
  by **exact path segment** (never substring): dependency trees (`node_modules`),
  VCS trees (`.git`, `.hg`, `.svn`, `.jj`) and Cargo build output (a `target`
  segment whose parent directory holds `Cargo.toml`, an actual Cargo root known
  from the units: workspace root or folded member package). `packages/target/index.ts`
  and `src/target/x.ts` are ordinary program members; `target/debug/x.rs` under
  a root `Cargo.toml` is `host-ignore-convention`. A marker inside a pruned tree
  (every `node_modules/<pkg>/package.json`, a `Cargo.toml` under `node_modules`)
  is never a unit and never a Cargo root; each pruned tree is reported once in
  `UnitDiscoveryV1.prunedTrees` (`PrunedTreeV1 {path, reason, markerCount}`) and
  its anchor enters `excludedPathPrefixes`. Pruning is a discovery rule, not a
  read-set exemption: bytes a program later reads from a pruned tree
  (`node_modules` in the TypeScript read set, §2.2/§9.4) enter the snapshot read
  set under the identity unit's snapshot custody and are Plan-bound (security
  S3 "Pruned trees and the read set"). Cases
  `units-installed-dependencies-are-pruned-by-segment-*`,
  `units-4200-installed-package-manifests-are-one-pruned-tree-not-a-cap-refusal`.
- **U-8 (admitted boundary inventory; post-reset v2 N-1/P3)** The project's
  **authority boundaries** are decided only by the security discovery instrument
  (S3): nested repositories (other custody roots), nested `opensip.json`
  projects (deliberate boundaries, ADV-3) and custody/depth-excluded unit
  directories. This instrument never re-derives them from caller-supplied
  ignores. An operational host composition obtains the closed
  `AdmittedBoundaryInventoryV1` from security (`boundary_inventory(result)`;
  relative scope paths under the selected root: `nestedRepositories`,
  `nestedProjects`, `custodyExcludedUnits`, `prunedTrees`) and passes it
  unchanged to `discover_units(markers, explicit_roots, boundaries)`,
  `assign_membership(units, files, boundaries)` and
  `unit_scope_descriptor(..., boundaries)`. Under it: a marker directory at or
  below a boundary is no unit and is never folded into a workspace
  (`UnitDiscoveryV1.boundaries.excludedUnits {path, marker, reason:
  nested-repository | nested-project | custody-excluded, anchor}`); a file at or
  below one is `outside-project-boundary` with that reason and listed in
  `outsideBoundaryFiles` (another project's or uncustodied source, never scanned,
  never erased); an explicit root at or below one refuses
  `native.explicit-root-crosses-boundary` (`CONFIG.INVALID`, the counterpart of
  security's `JOIN_CROSSES_NESTED_*`); every nested anchor and
  directory-custody exclusion enters `excludedPathPrefixes`, so the Plan scope
  names the boundaries. The inventory's `prunedTrees` must equal the ones this
  instrument derives from the same marker inventory
  (`native.boundary-inventory-mismatch`, `REQUEST.PRECONDITION_FAILED`): an
  ignore list is never proof of boundary completeness. `boundaries=None` is
  retained only for the **standalone pure instrument** (fixtures, callers with
  no project); its output says so (`boundaries.source = "none"` with a
  disclosure) and is not an operational host composition. From inside a nested
  config the nested project is the whole project and its inventory names no
  boundary. Cases `units-nested-repository-and-nested-project-are-excluded-*`,
  `units-explicit-root-crossing-into-a-nested-project-or-repository-refuses-typed`,
  `units-launch-inside-a-deliberate-nested-config-*`,
  `units-standalone-instrument-without-boundary-inventory-*`,
  `units-boundary-inventory-whose-pruned-trees-disagree-*`,
  `units-custody-excluded-directory-and-marker-*`; the security checker sweep
  `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`
  runs the P3 fixture through both instruments.
- **U-5 (per-unit evaluation and joining)** A predicate over a scope spanning
  units is evaluated per unit and joined by the host: `complete` only if every
  unit's relevant Coverage is complete; otherwise the aggregate carries the most
  specific deficiency by §10 precedence. Silent narrowing to the supported units is
  forbidden (`narrowed=false` is a checked invariant).
- **U-6** Cross-unit edges are `external-module-boundary` unresolved edges on the
  importing side. No cross-language resolution is claimed.
- **U-7** `maxWorkspaceUnits = 4096` **first-party** unit directories (the
  shared rule's cap; pruned dependency manifests never count). Exceeding it is
  the typed refusal `PROJECT.WORKSPACE_UNIT_LIMIT` (`REQUEST.UNSATISFIABLE`, exit 2)
  returned as `UnitDiscoveryV1.refused` with `unitCount`/`limit`, never
  truncation and never an exception (`too-many-units-rejected`: 4200 first-party
  package directories refuse; 4200 installed manifests admit with one unit).
  The security instrument refuses the same population as
  `PROJECT.WORKSPACE_UNIT_LIMIT` → `REQUEST.UNSATISFIABLE`.

**Config2 join (R6; explicit roots are exact roots).**
`product-configuration.schema.v2.json#discovery` (`entryPoints`,
`workspaceRoots`, `ignorePaths`) is consumed as follows. Explicit
`workspaceRoots` (and CLI `--workspace-root`) are normalized by the shared
`normalize_explicit_root`: `.` alone is the admitted project root (identity §3
sentinel) and becomes the internal root `""`, exactly as the security instrument
maps it to the selected root; one trailing `/` is dropped from a CLI value (a
Config2 value spelled with a trailing `/` is refused earlier by the foundation
resolver's logical-path grammar and never reaches this instrument; post-reset v2
A-4); an empty, `.`, `..`,
absolute, backslash or NUL segment is `CONFIG.INVALID`
(`PROJECT.EXPLICIT_PATH_INVALID`). Discovery is then restricted to exactly those
roots with `provenance=EXPLICIT`; an explicit root without a language marker is
`CONFIG.INVALID` (detail `native.explicit-root-without-marker`, exit 2), never
silently dropped and never widened into a scan
(`units-explicit-config2-workspace-root-without-marker-is-config-invalid`,
`units-explicit-root-dot-is-the-project-root-under-the-shared-sentinel-normalization`).
Security admits the custody of such a root and records the warning
`EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER`; this layer decides language-unit
existence; the invocation terminates typed. A root inside a pruned tree has no
first-party marker and refuses the same way (security refuses it as
`JOIN_INSIDE_PRUNED_TREE`). `ignorePaths` remove whole path segments and enter
`excludedPathPrefixes`; `entryPoints` set `entryPoints.source=explicit` (§8,
FR-2). No discovery output executes code, imports ambient evidence or grants
permission.

**Unit scopes feed the shared scope descriptor.** `unit_scope_descriptor` emits
the foundation `identity-schemas.v2.json#/$defs/scope-descriptor`
(`{schemaVersion:2, workspaceRoots, pathPrefixes, excludedPathPrefixes}`; the
project root is spelled `.`); `excludedPathPrefixes` = Config2 `ignorePaths` ∪
the anchors of the pruned trees discovery observed (`prunedTrees`) ∪ the
conventional anchors of the shared rule (`.git`, `node_modules` under every unit
root; `target` under every Cargo root only) ∪ the admitted boundary anchors
(U-8: nested repositories, nested projects, directory-custody exclusions; the
boundary provenance travels beside the closed foundation record as
`boundaries`). `scopeDigest` is its raw SHA-256 of
canonical bytes under the foundation rule, and the same record is what an import
wrapper's `scopeDigest` names (§7). There is no native scope domain. The
foundation scope descriptor admits at most 1024 workspace roots; discovery's
4096 cap is the diagnostic population, and a project with more than 1024 unit
roots refuses at scope admission without truncation and asks for a narrower
explicit scope (§14).

**Default discovery selects the full registered TS/JS/Rust capability set.**
`default_capability_selection` takes the authenticated release declaration
registry rows (capability × applicable language modes) and requests every
registered capability for every unit whose mode it applies to, `required=true`,
`provenance=DEFAULTED`, emitted as the foundation `analysis-spec` record. There
is no `preview-typescript` constant and no TypeScript-only default; a registry row
spelled `preview-*` is refused
(`units-default-capabilities-full-tsjs-rust-registry-no-preview`).

**The capability vocabulary, its authority and its spelling (CB4-SHOULD-2).**
`analysis-spec.requestedCapabilities[].capabilityId` was `$ref: Text` and enters
`PlanId` through `analysisSpecDigest`, and no document named the vocabulary it is
drawn from. Three spellings were consequently in live use in one release: the
reference default-selection corpus emitted `relation@rung`
(`clones@normalized-body-hash`), the foundation reference fixture emitted a bare
relation name (`references`), and the capability matrix publishes `inventory`,
`syntax`, `clones-fact`, `clones-near`, `clones-cross-tsjs`, `unresolved-edge`.
Two conforming hosts requesting the same analysis of the same unit therefore mint
different `analysisSpecDigest`s, different `PlanId`s and different `RunId`s, which
defeats independent replay across machines. The `languageMode` sibling was
already closed against a registered map at Run closure; the capability was not.

- **Authority.** `native/native-capability-matrix.v2.json#/capabilities[].id`,
  closed at eleven members, with the law published beside it at
  `#/capabilityIdLaw`. The same vocabulary serves
  `product-configuration.analysis.capabilities`, whose item pattern
  `^[a-z][a-z0-9._:-]*$` already contained no `@` — so the `relation@rung`
  spelling was never admissible at the configuration layer and is now refused by
  shape at the analysis-spec layer too, before membership is consulted.
- **A capability id is not a `relation@rung`.** They are different concepts and
  are not equated. A capability is a *requestable unit of work* and may cover
  several relations (`inventory` covers `file@enumerated`,
  `package@manifest-declared` and `vcs-change@vcs-reported`; `syntax` covers the
  three syntactic rungs) or none at all (`clones-near` and `clones-cross-tsjs`
  are candidate-only and bear no fact relation). A `relation@rung` is a
  *fact/Coverage coordinate*: it is what `CoverageKeyV2`, the §1.3 table, the
  grammar-capability registry and the relation ladders speak. The bridge in both
  directions is the matrix's own `capabilities[].relations`, so an implementer
  never has to guess one from the other.
- **Mode applicability.** A request names a capability *and* a `languageMode`.
  The `(capability, mode)` cell must exist — the table is the complete product of
  the eleven capabilities and the six modes, so it always does for registered
  members — and its state must not be `NOT-SELECTED`, which means "outside D-371;
  no promise" and is an *unsatisfiable* request rather than a disclosable one.
  An `UNSUPPORTED-TYPED` cell is a different thing entirely: it **is**
  requestable and is answered with `unknown` plus its own named deficiency and
  cause, never refused. Today's three `NOT-SELECTED` cells are
  `clones-cross-tsjs` under `rust-cargo`, `rust-cargo-prepared` and `syntax-only`.
- **The release declaration registry.** Its *content* stays an authenticated
  input — which rows a release ships is not a contract constant — but its schema
  (`native-evidence.schemas.v2.json#/$defs/ReleaseCapabilityRegistryV1`, rows
  `{capabilityId, languageModes[]}`), its membership authority (`capabilityId` ∈
  the matrix ids; every mode registered with a cell that is not `NOT-SELECTED`),
  its canonical spelling and its binding to the Plan are normative. A duplicate
  `capabilityId` refuses rather than merging, because two rows declaring
  different applicable modes for one capability would leave default selection
  ambiguous.
- **Closed at admission, not only in the helper.** The default helper is one
  producer of an `analysis-spec`, not the authority. The same vocabulary is
  closed again at Plan/Run closure over the **retained** `analysis-spec`
  (`ANALYSIS_SPEC_CAPABILITY:native.requested-capability-*`), so an explicitly
  configured or hand-built spec is judged by exactly the rule a defaulted one is,
  and the default and explicit paths agree on one spelling by construction. The
  foundation keeps its own fault for an unregistered *mode*; native owns which
  capabilities exist and which cells this product promises anything for.

No capability is added, removed or renamed, no cell state changes, and all six
advertised modes, the three native contexts and the full default-selected
product stay exactly as representable as before. What is new is the authority
for a field that had none.

**Backup custody join.** Dependency-source files, inert prepared rows and
generated-file blobs are host CAS objects under the one host storage root; they
inherit the identity-and-evidence §5 backup-managed-storage choice
(`--allow-backup-custody` or an admitted storage-policy record; CI without a
choice refuses `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`).
Native adds no second store and no custody rule of its own.

`mixed-native-partial` fixes the meaning: TypeScript unit complete, co-located Rust
unit missing an external crate → TypeScript-scoped predicates evaluate;
repository-scoped semantic predicates are indeterminate with
`input-closure-incomplete` naming the crate; syntax and clone predicates complete
for both.

---

## 2. Semantic universe successors

Every array in the current native schema bundle declares `x-opensip-order`
under identity §3. `sequence` preserves order and repeated items unless a separate
uniqueness constraint applies. It is intentional for compiler flags, signature
tokens, substitution precedence and ordered observations. Stricter orders are
machine-checked at schema admission: declaration components by `component`,
dependency packages by `(name, version, sourceId)`, owner records by `ownerKey`,
file-manifest rows by `path`, and the explicitly sorted path/name/enum collections
by raw UTF-8 bytes. These keys must be unique; a second row with the same key and
different payload also refuses. The canonical encoder never sorts a collection.
Input-adapter observation sequences retain their own declared order; a producer
must construct any stricter output collection before admitting it.

### 2.1 `rust-v2` (replaces `rust-v1.resolvedInputs`)

All `rust-v1` release/toolchain identity fields are retained unchanged.
`resolvedInputs` becomes `RustUniverseV2ResolvedInputs`:

| Field | Type | Rule |
|---|---|---|
| `schemaVersion` | `2` | exact integer |
| `edition` | per-package map `{packageKey: 2015\|2018\|2021\|2024}` | keys sorted; every workspace member present |
| `lockfileIdentity` | `{path:"Cargo.lock", contentSha256, lockfileVersion∈{3,4}}` | absence is `input-closure-incomplete` (`lockfile-missing`), never an implicit `cargo generate-lockfile` |
| `dependencySourceSetId` | `Sha256Text` | identity of the admitted `DependencySourceSetV1` (§3) |
| `unifiedFeaturesId` | `Sha256Text` | identity of `UnifiedFeaturesV1` (§3.4) |
| `nativeContextId` | `Sha256Text` | identity of `NativeContextV2` (§2.3) |
| `cfgSets` | array of `{cfgSetId, cfg}` length 1..4 | default `[primary, primary+test]`; extra sets are Plan-bound. Every set's `cfg` **contains every member of the context's `baseCfg`**: sets differ from the base only by additions, and `cfgSetId` is unique within the universe. A set that dropped a base cfg would analyse a configuration nothing selected |
| `rustflags` | `RustflagsProjectionV1` | the *honored* and *stripped* flag lists after the exact allowlist (§3.3); equal to the bound context's `configProjection.rustflags` |
| `crateRootPaths` | sorted unique canonical paths | unchanged; every path must be in the analysed snapshot inventory |
| `configProjectionSha256` | `DigestHex` | the 64-hex suffix of `H("native.cargo-config-projection.v2", CargoConfigProjectionV2)` over the bound context's `configProjection` (§3.3). It is **not** the raw SHA-256 of the canonical projection bytes, and **not** `CargoConfigProjectionV2.projectionSha256`, which is the raw digest of the projected config *file*. Raw file digests are also in the snapshot |
| `preparedResolution` | `none \| host-prepared \| imported-inert` | how prepared products entered the universe (R4) |
| `executionCapableResolution` | boolean | `preparedResolution ≠ none`. It names the **meaning** of the universe (resolution consumed inert products of some execution). It is **never** a host execution grant: the grant is the operational `RepoExecutionGrantV2` reference outside Plan (§5.1). `imported-inert` needs only `read-import` in the semantic grant; only `host-prepared` projects `prepare-code` |
| `preparedOutputSetId` | `Sha256Text \| null` | identity of the admitted `PreparedOutputSetV3`; `null` when `preparedResolution=none` |

Change rule: any field change changes PlanId. Missing, unknown, float-spelled,
unordered or handshake-mismatched values fail before provider execution.

**Binding a `rust-v2` universe (`bind_rust_universe`).** A universe is bound to its
admitted context before PlanId, exactly as `typescript-v2` is bound by
`bind_typescript_universe` (§2.4), and for the same reason: an identity commits to
the context bytes, not to the universe's copy of them. The binding is pure — it
executes no cargo, rustc, build script, proc macro or filesystem read — and takes
the admitted context descriptor, the retained nested input records
(`DependencySourceSetV1`, `UnifiedFeaturesV1`, `PreparedOutputSetV3` when one is
selected) and the analysed snapshot inventory. All three are **required**: there is
no context-free or input-free admit path, because an optional join is not a rule,
and omission is the typed refusal `native.universe-retained-inputs-not-supplied`,
never an ADMIT. It refuses when

- the admission is not a Rust context admission, or the universe names a context
  this host did not mint, or the supplied context bytes are not the admitted ones;
- any overlapping field disagrees:
  `dependencySourceSetId`, `unifiedFeaturesId`, `preparedOutputSetId`, `rustflags`,
  `configProjectionSha256`, `executionCapableResolution`, `preparedResolution`, or a
  `cfgSets` entry that drops a base cfg or repeats a `cfgSetId`;
- a nested semantic identity is not the exact H identity of the retained record of
  its registered domain, or that record contradicts the universe or context —
  a dependency set whose `lockfileIdentity` differs, unified features computed for
  another `targetTriple` or resolver version, or a prepared set bound to another
  dependency set, toolchain, cfg set or preparation kind;
- a prepared output set is retained but **no** universe selected it
  (`preparedOutputSetId = null`): optional absent preparation stays absent, and
  bytes in custody never enter a resolution by being in custody;
- the snapshot does not contain what the universe names: `Cargo.lock` missing or
  with different bytes, a `crateRootPaths` entry not inventoried, or a
  `replacedSnapshotConfigs` entry not inventoried.

`executionCapableResolution` remains a statement about what the resolution
consumed, never an execution grant; retained inert prepared bytes cannot imply one,
and the operational `RepoExecutionGrantV2` reference stays outside Plan (§5.1).

### 2.2 `typescript-v2` (replaces `typescript-v1.resolvedInputs`)

Retained **in the universe**: `tsconfigGraphHash`, `programRootFiles`,
`executionCapableResolution` (constant `false`: no TypeScript-side repository
execution is selected).

**Relocated to the context** (§2.4), and therefore *not* fields of the closed
`TypeScriptUniverseV2ResolvedInputs`, which is `additionalProperties: false`:
`compilerOptions` — now `TypeScriptConfigProjectionV2.honoredOptions` and
`strippedOptions`; `packageLockIdentity` — now
`TypeScriptNativeContextV2.lockfileIdentity`, with `lockfileKind` retained in the
universe as its kind projection; and `resolvedNodeModulesLayout` — now the
retained `ResolvedNodeModulesLayoutV1` record that
`TypeScriptNativeContextV2.nodeModulesLayoutDigest` names. An implementer building
a universe record from the older "Retained:" list produced a record that fails
admission; these three moved, they were not dropped.

`tsconfigGraphHash` is the **raw SHA-256 of `C(TypeScriptConfigGraphV1)`** — a
retained canonical record, not an H identity and not an opaque id. That record is
`{schemaVersion: 1, entryConfigPath, nodes}`, where `nodes` is the strictly ascending
unique-by-`path` array of every config file actually read, each
`{path, contentSha256, kind, extendsResolved}`: `contentSha256` is that file's
inventoried snapshot digest and `extendsResolved` is the ordered array of
project-relative paths its `extends` entries resolved to. Later entries take
precedence; repetitions are retained, and an empty array means no base config.
`entryConfigPath` selects the root config, or is null for synthesized configuration.
The record is a **required** binding input, and the binding
checks that `nodes[].path` is exactly the context's
`configProjection.configGraphPaths` set, that every node's digest is the snapshot's,
and that every edge names another node. Every node must be reachable from the
selected entry and the graph must be acyclic, so the universe key and the context
cannot describe two different config graphs.

`configOrigin` is **derived from that retained record, never asserted**:
`synthesized` exactly when the entry is null and `nodes` is empty; otherwise it
comes from the selected entry's kind (`jsconfig` for a jsconfig entry, otherwise
`tsconfig`). Node kind agrees with its path as specified by the schema and native
admission. A jsconfig entry extending a shared base remains a jsconfig program.
The universe's `configOrigin` must equal the derived value. This is the input
§2.4's agreement check needs; without the record the `tsconfig`/`jsconfig`
distinction was not derivable and two spellings minted two universe identities for
one admitted context.

Added: `schemaVersion=2`, `languageMode`, `configOrigin`,
`synthesizerVersion`, `synthesizedOptions`, `packageModuleType`, `allowJs`,
`checkJs`, `jsAdmittedToProgram`, `jsDiagnosticsEnabled`,
`resolutionCompletenessImplied=false`, `jsRootFiles`, `lockfileKind`,
`nodeModulesInReadSet` (`false` means bare specifiers are
`unresolved-module-specifier`, scope `external`; never an implicit install) and
`nativeContextId` — the identity of the **`TypeScriptNativeContextV2`** record of §2.4,
under the domain `native.context.typescript.v2`. It is never a `NativeContextV2`
(that record is the Rust context, §2.3), and a `typescript-v2` universe that names a
Rust-minted context refuses before PlanId (§2.4).

**`ResolvedNodeModulesLayoutV1`** is the record that digest names, and it is what
makes the ordinary TypeScript project — the one with dependencies — representable.
It is `{schemaVersion: 1, entries}`, where `entries` is strictly ascending and
unique by `installPath`, one row per installed package directory the resolver may
read: `{packageName, packageVersion, installPath, realPath, contentSha256}`.
`installPath` is the project-relative directory as the resolver walks it,
`realPath` is that directory after symlink or workspace-link resolution (equal to
`installPath` when there is no link, and otherwise itself an `installPath` of this
layout), and `contentSha256` is the raw SHA-256 of that package's manifest file
bytes, retained in the closure.

These rows are **not** snapshot inventory rows and must not be: the one shared
discovery rule prunes `node_modules` by path segment, so the layout is a retained
resolution observation of bytes the analysis read, joined by digest rather than by
snapshot membership. `nodeModulesInReadSet` is exactly
`nodeModulesLayoutDigest is not null`, the layout is a **required** binding input
whenever it is non-null, and a retained layout that no context selected is refused
rather than drifting into the resolution. With the layout present, bare specifiers
resolve normally; with it absent, `nodeModulesInReadSet=false` and every bare
specifier is an `unresolved-module-specifier` edge with scope `external` — never an
implicit install. Both branches are now constructible; before this record existed
only the second one was.

`SynthesizedCompilerOptionsV1` (deterministic function of the unit listing and
`package.json`; version 1 pinned): `allowJs=true`, `checkJs=false`,
`module=node16`, `moduleResolution=node16`, `target=es2022`, `jsx=preserve` iff any
`.jsx/.tsx` root exists else absent, `strict=false`, `skipLibCheck=true`,
`types=[]`, `noEmit=true`, roots = every `.ts/.tsx/.js/.mjs/.cjs/.jsx` file under
the unit excluding `node_modules`, `.git` and host ignore conventions. No option is
read from the environment. A synthesizer change is a universe change.

### 2.3 `NativeContextV2` (Rust)

**There is exactly one native-context record and one `H` domain per language.**
`NativeContextV2` is the **Rust** context; `TypeScriptNativeContextV2` (§2.4) is the
TypeScript one. Neither is a general "native context": a universe binds the record of its
own language and refuses the other.

Descriptor (domain `native.context.rust.v2`): `{schemaVersion:2, targetTriple,
hostTriple, toolchain: ToolchainIdentityV1, toolClosure: ToolClosureV1, baseCfg,
resolverVersion, dependencySourceSetId, unifiedFeaturesId, preparedOutputSetId|null,
configProjection: CargoConfigProjectionV2}`.

`rustcDevLlvmDigest` is at **`NativeContextV2.toolchain.rustcDevLlvmDigest`**, inside
`ToolchainIdentityV1` — not a top-level field of the context (a citation that says only "in
native-context schema 2" is reachable but under-specified). Its value is the 64-hex suffix
of the `closure2` identity of the admitted `kind=rust-dev-llvm` closure, so `"closure2:" +`
the field must name a retained closure of that kind whose recomputed identity equals it;
`admit_native_context('rust', …)` performs exactly that join against the retained closure
descriptor and tree.

`ToolClosureV1` = `{rustc, cargo, linker|null, ar|null, procMacroServer, closureId}`
— the raw digests of every executable the adapter may select, all members of the
signed `closure2` named by `closureId`. **Every tool that runs is in this
closure**: `rustc`, `cargo`, the linker rustc spawns when a build script or
proc-macro crate is linked, `ar`, and the proc-macro server. No `PATH` lookup, no
system `cc`, no `RUSTC`/`CARGO`/`RUSTUP_*`/`CARGO_HOME` from the environment. If a
platform family has no bundled linker in the closure, in-host preparation is
`UNSUPPORTED-TYPED` there (`native.execution-not-authorized`, cause
`linker-unavailable`); it never falls back to a system linker.

The host resolved-inputs adapter computes the context before PlanId; the worker
recomputes it after sealed inputs are received and refuses with
`Unavailable(native-context-mismatch)` before Analyze if any byte differs (§9.5).

### 2.4 `TypeScriptNativeContextV2` (TypeScript/JavaScript)

Descriptor (domain `native.context.typescript.v2`): `{schemaVersion:2, languageMode,
toolchain: TypeScriptToolchainIdentityV1, toolClosure: TypeScriptToolClosureV1,
configProjection: TypeScriptConfigProjectionV2, moduleResolutionMode, packageModuleType,
nodeModulesLayoutDigest|null, lockfileIdentity|null}`.

`TypeScriptToolchainIdentityV1` = `{compilerName:"typescript", compilerVersion,
compilerPackageDigest, typescriptStdlibMerkleRoot, standardLibraryComponentDigests[],
libSelection[]}`. `TypeScriptToolClosureV1` = `{compiler, runtime, closureId}`.

**Exact field locations and producing recipe.** Every value is computed by the host
resolved-inputs adapter before PlanId from **admitted, retained** bytes; none is read from a
worker claim, a `tsc --version` string or the environment.

| Field | Produced from |
|---|---|
| `toolchain.compilerVersion` | the `semanticVersion` of the **admitted signed compiler closure manifest** named by `toolClosure.closureId`; admission refuses when the two differ, so a version string and the bytes it labels cannot drift apart |
| `toolchain.compilerPackageDigest` | a member digest of that retained `kind=toolchain` closure tree |
| `toolchain.typescriptStdlibMerkleRoot` | identity §3's existing recipe: the **64-hex suffix** of the `closure2` identity of the admitted `kind=stdlib` closure. `"closure2:" +` the value must name a retained closure of that kind whose recomputed identity equals it |
| `toolchain.standardLibraryComponentDigests` | the **complete** declaration-file inventory of that retained stdlib tree — one row per `.d.ts` member, selected or not, `component` = the member basename, sorted by `component`. A missing row refuses `native.native-context-stdlib-inventory-incomplete:<name>`, because an alternate partial declaration inventory for the same retained library is not the required complete record. A tree in which two paths share a basename refuses `native.native-context-stdlib-tree-ambiguous-basename:<name>` rather than resolving the join arbitrarily |
| `toolchain.libSelection` | the effective `lib` names the resolved `compilerOptions` select after `target` defaulting, sorted; each must be covered by a retained component |
| `toolClosure.compiler`, `toolClosure.runtime` | raw digests of the bundled compiler and of the bundled JavaScript runtime that executes it, both members of the signed closure named by `closureId`. No `PATH` lookup, no system `node`, no `NODE_OPTIONS`/`NODE_PATH`/`TS_NODE_*` from the environment |
| `configProjection.honoredOptions` | the closed subset of the **effective** resolved `compilerOptions` (or of `SynthesizedCompilerOptionsV1` under `js-synthesized`) that changes program membership, module resolution or checking |
| `configProjection.strippedOptions` | every option removed, with a typed reason (`selects-an-executable`, `emits-output`, `reads-the-environment`, `acquires-types-from-the-network`, `not-a-resolution-or-membership-option`). Stripping is disclosed here and is never a reason to read the option from anywhere else. `typeAcquisitionEnabled` and `executableSelected` are schema constants `false` |
| `configProjection.configGraphPaths` | every `tsconfig`/`jsconfig` file of the resolved `extends` graph, in the snapshot, sorted by logical path; empty under `configOrigin=synthesized` |
| `nodeModulesLayoutDigest` | raw SHA-256 of `C(ResolvedNodeModulesLayoutV1)` — the retained resolution read-set layout — or `null` exactly when `nodeModulesInReadSet=false` |
| `lockfileIdentity` | `{kind, path, contentSha256}` of the admitted lockfile, or `null` when `lockfileKind=none` |

**Retained trees.** The stdlib closure and the compiler closure are retained **whole** —
complete foundation `closure` descriptor and complete file tree — and joined to the selected
compiler. `admit_native_context` recomputes each closure identity from its retained record
and refuses `native.native-context-closure-unretained`,
`native.native-context-closure-identity-mismatch` or
`native.native-context-closure-kind-mismatch` before any digest comparison. The stdlib merkle
root is therefore never a bare number a caller can assert.

**No platform *field*, and the identity is still platform-specific.** Unlike the Rust context there
is no `targetTriple`/`hostTriple`, because TypeScript *resolution semantics* — which specifiers
resolve, which subjects are examined, what is checked — are platform-invariant by design (§1.1).
That is a design selection of this contract, not a measurement, and it is **not** a claim that the
identity is platform-invariant: `toolClosure.closureId` names a signed closure whose foundation
`closure` descriptor includes `platform`, so the same source analysed with the platform-specific
executables of two families mints two `nativeContextId`s — as it must, because different bytes ran
(`typescript-context-identity-is-platform-specific-through-its-signed-tool-closure`).

**Universe and Plan binding.** `typescript-v2.nativeContextId` is
`H("native.context.typescript.v2", descriptor)` in the `Sha256Text` form. `PlanId` binds the
same digest through `plan.nativeContextDigests`, which takes the **bare 64 hex** (§11, the
foundation `plan` record's spelling) and is a canonical **set**: several units of one language
legitimately share one context, and identical admitted contexts collapse to one member — that is
deduplication of an identical descriptor, never of two different ones.

`bind_typescript_universe(universe, admission, context)` refuses a universe whose `nativeContextId`
this host did not mint (`native.universe-context-binding-mismatch`) and refuses a Rust-minted context
outright (`native.native-context-language-mismatch`). The **retained context bytes are a required
argument**: there is no context-free admit path, because an optional field-agreement check is not a
rule — a caller that omitted it would obtain exactly the bypass this join exists to close. Omission
is the typed refusal `native.universe-context-not-supplied`
(`typescript-universe-bound-without-the-retained-context-refuses`); context bytes that do not hash to
the admitted id refuse
`native.universe-context-binding-mismatch:context-bytes-are-not-the-admitted-ones`.

Given those bytes the two records must **agree where they overlap**: a matching `nativeContextId`
commits to the context bytes, not to the universe's copy of them, so `languageMode`,
`packageModuleType`, `allowJs`, `checkJs`, `lockfileKind`, `nodeModulesInReadSet`,
`jsDiagnosticsEnabled`, `jsAdmittedToProgram`, `configOrigin`, the `extends`-graph emptiness and the
synthesized-options presence are each checked against the context and refuse
`native.universe-context-field-mismatch:<field>`.

The context itself also has mandatory agreement rules. `moduleResolutionMode`
equals `configProjection.honoredOptions.moduleResolution`. `libSelection` is
strictly sorted by UTF-8 name bytes, contains no case-insensitive duplicate names,
and selects the same case-insensitive name set as the honored `lib` list;
each record retains its specified order for hashing. The closed resolved context
always materializes that nonempty list. When source configuration omits `lib`,
the resolver supplies the pinned compiler's target-default library selection
in both records; `null` is not an alternate resolved spelling.
`standardLibraryComponentDigests`
has strictly unique component keys in UTF-8 order. Context admission refuses any
contradiction before its digest may enter Plan. In synthesized mode every value
in `synthesizedOptions` equals the corresponding honored option, and an absent
optional `jsx` means honored `jsx` is null. Presence alone is insufficient.
These are semantic agreement checks in addition to closed schema validation;
internal diagnostic suffixes remain operational refusal evidence, not new public
DomainDetail codes.

**Independent derivation (§9.5) applies to TypeScript exactly as to Rust.** The worker
recomputes the context from its own sealed inputs; a differing byte is
`Unavailable(native-context-mismatch)` before Analyze.

Cases: `typescript-native-context-admits-against-retained-stdlib-and-compiler-closures`,
`typescript-standard-library-change-alone-changes-the-context-and-the-universe`,
`typescript-compiler-change-alone-changes-the-context-and-the-universe`,
`typescript-stdlib-merkle-root-that-names-no-retained-closure-refuses`,
`typescript-tool-digest-outside-the-named-closure-tree-refuses`,
`typescript-stdlib-component-digest-disagreeing-with-the-retained-tree-refuses`,
`typescript-stdlib-inventory-missing-an-unselected-declaration-library-refuses`,
`typescript-stdlib-tree-with-two-paths-sharing-a-basename-refuses`,
`rust-native-context-offered-as-the-typescript-context-refuses`,
`typescript-universe-bound-to-a-context-this-host-did-not-mint-refuses`,
`typescript-universe-bound-without-the-retained-context-refuses`,
`typescript-universe-field-contradicting-the-admitted-context-refuses`,
`typescript-universe-agreeing-with-the-admitted-context-admits`,
`typescript-context-bytes-that-are-not-the-admitted-ones-refuse`,
`typescript-context-identity-is-platform-specific-through-its-signed-tool-closure`,
`worker-recomputed-typescript-context-mismatch-is-unavailable-before-analyze`,
`plan-native-context-digests-are-bare-hex-while-native-records-use-sha256-text`.

This is a reference design for the context record and its joins. Measuring a real TypeScript
compiler, its standard library tree or its resolution behaviour on any platform remains
qualification work (§12).

---

## 3. Sealed dependency inputs (AR-07)

### 3.1 `DependencySourceSetV1`

Identity domain `native.dependency-source-set.v1`. Closed descriptor:
`{schemaVersion:1, language:"rust", lockfileIdentity, packages:
[DependencyPackageSourceV1…] sorted by (name, version, sourceId) UTF-8 bytes,
completeness:{state, missing[]}}`.

`DependencyPackageSourceV1`:

| Field | Rule |
|---|---|
| `name`, `version` | exact `[[package]]` values from `Cargo.lock` |
| `sourceKind` | `registry \| git \| path \| vendored` |
| `sourceId` | exact `source` string from `Cargo.lock`, or `""` for path packages |
| `lockChecksum` | 64-hex from the lock `checksum`, or `null` for git/path |
| `fileManifestSha256` | H(`native.dependency-file-manifest.v1`, sorted `[{path, contentSha256, byteLength}]`) |
| `fileCount`, `totalBytes` | exact uint64 |
| `acquisition` | `{mode: in-snapshot-path \| in-snapshot-vendored \| imported-descriptor, descriptorId: ImportId\|null, vendorPath\|null}` |
| `checksumVerification` | `tarball-matched \| self-consistent \| not-applicable \| mismatch` — `mismatch` refuses the whole set |
| `provenanceAssurance` | `registry-authenticated \| declared` |

Verification rules (feedback 3 corrected):

- **DS-1 (registry, vendored tree)** A vendored directory carries a self-asserted
  `.cargo-checksum.json`. Its `package` field equalling `lockChecksum` proves
  nothing about the files: an attacker rewrites file contents and every `files`
  entry while preserving `package`. The host therefore checks internal
  consistency only (`package == lockChecksum`, every listed file's SHA-256
  matches, no extra or missing files) and records `checksumVerification =
  self-consistent`, `provenanceAssurance = declared`. Inconsistency is `mismatch`
  and refuses the set. The reference model contains the mutation
  (`ds1-mutation-preserving-package-checksum-stays-declared`): the mutated tree is
  still admitted, and it is still *declared*, never authenticated.
- **DS-2 (registry, tarball)** Only the exact `.crate` tarball whose SHA-256
  equals `lockChecksum` yields `tarball-matched` / `registry-authenticated`. The
  host extracts it deterministically into the CAS and computes the file manifest
  itself. An extracted tree plus `.cargo-checksum.json` is DS-1.
- **DS-3 (git)** The import supplies the checked-out tree for the exact `#rev`;
  `not-applicable` / `declared`; the file manifest identity is the binding.
- **DS-4 (path)** Path dependencies live in the snapshot; nothing is imported.
- **DS-5 (no ambient reads)** `$CARGO_HOME/registry`, `~/.cargo`, `vendor/`
  outside the snapshot, or any host path is read **only** as the explicit,
  user-named source path of an import step (§7). Any acquisition mode outside the
  closed set, or any fetch URL, refuses. No network fetch exists in any first-party
  code path (design invariant, conformance-checked; not a confinement claim).
- **DS-6 (completeness)** The set is complete for a target when every package
  activated by `UnifiedFeaturesV1` is present with `checksumVerification ≠
  mismatch`. An incomplete set is admitted with `completeness.incomplete` and
  typed `input-closure-incomplete` Coverage for dependent crates; it never blocks
  syntax analysis.

`declared` provenance is disclosed wherever the package matters: in the Plan
(through the set descriptor), in `AuthorizedExecutionV2.owners[].provenanceAssurance`,
and in the pre-execution sentence (§5.2). Facts derived from declared sources are
still Plan-bound Coverage inputs; the disclosure is what changes.

### 3.2 Custody and transport

The host stores admitted dependency sources in its content-addressed store keyed
by `fileManifestSha256`; Plan-bound by `dependencySourceSetId`. Transport uses
protocol-3 frames `DependencySourceManifest / DependencySourceChunk /
DependencySourceSeal / DependencySourceAccepted` (§9.2) with the same byte-exact,
digest-verified, reject-before-use discipline as the snapshot. The worker mounts
the accepted files read-only at `.opensip/deps/v1/<name>-<version>/…` in its
private scratch materialization. Nothing is fetched lazily.

### 3.3 Cargo configuration: verified carrier, exact flags (feedback 5, 10)

Primary source (`doc.rust-lang.org/cargo/reference/config.html`, read 2026-09-06):
Cargo reads `.cargo/config.toml` (and legacy `.cargo/config`) from the current
directory and **every ancestor**, plus `$CARGO_HOME/config.toml`, merging arrays;
it also honors `CARGO_*` environment overrides and knobs that select executables
(`build.rustc`, `build.rustc-wrapper`, `target.*.linker`, `target.*.runner`),
credentials and network. Stock Cargo has no switch that disables ancestor
discovery, and this contract does not claim `--config` replaces the stack.

The first-party `opensip-cargo-adapter` therefore establishes a **verified
ancestor carrier** (`CargoConfigProjectionV2`, all checked by
`cargo_config_admission` in the model):

- **CC-1** Before every Cargo invocation, every ancestor directory of the private
  scratch root is checked for `.cargo/config.toml` and `.cargo/config`. Presence
  is a refusal (`native.ambient-cargo-config`, exit 4), never a merge and never a
  silent skip. `ancestorCarrierVerified=true` is recorded in the context.
- **CC-2** `CARGO_HOME` is a fresh private empty directory created for the
  invocation; its `config.toml` is absent by construction.
- **CC-3** The constructed environment contains no `PATH`, `CARGO_*`, `RUSTFLAGS`,
  `RUSTC*`, `RUSTDOC*`, `RUSTUP_*`, `CC`/`CXX`/`LD`/`AR`/`TARGET_*` variables;
  presence of any is a refusal. Tool locations are passed as absolute closure
  paths on the command line, not via environment.
- **CC-4** Every selected tool digest equals its entry in `ToolClosureV1`.
- **CC-5** Every `.cargo/config(.toml)` inside the snapshot (any directory, not
  only the root) is replaced in the materialization by the single projected file;
  the originals remain snapshot bytes for identity but are never read by Cargo.

Projected (honored) keys: `build.target`, `build.rustflags`,
`target.<triple>.rustflags` (both through the flag allowlist below),
`source.<name>.directory` pointing inside the snapshot with `replace-with`,
`resolver`, and `[patch]` in `Cargo.toml`. Stripped and recorded: `alias`,
`build.rustc`, `build.rustc-wrapper`, `build.rustc-workspace-wrapper`,
`build.rustdoc`, `build.target-dir`, `build.build-dir`, `build.incremental`,
`build.dep-info-basedir`, `cargo-new`, `credential-alias`, `doc`, `env`,
`future-incompat-report`, `http`, `install`, `net`, `patch` (config-level),
`profile`, `registries`, `registry`, `target.*.linker`, `target.*.runner`,
`target.*.<links>`, `term`, `unstable`. A `[source]` replacement pointing outside
the snapshot is `input-closure-incomplete` (`source-replacement-outside-snapshot`).

**Two distinct digests, both now named.** `CargoConfigProjectionV2.projectionSha256`
is the raw SHA-256 of the exact bytes of the **single projected `.cargo/config.toml`
file** the adapter materializes under CC-5 — a raw artifact digest of a file.
`rust-v2.configProjectionSha256` (§2.1) is the 64-hex suffix of
`H("native.cargo-config-projection.v2", CargoConfigProjectionV2)` over the whole
projection record. Neither is the raw SHA-256 of the canonical projection bytes, and
neither substitutes for the other. Every `replacedSnapshotConfigs` entry names a
path that must be in the analysed snapshot inventory: the originals remain snapshot
bytes for identity even though Cargo never reads them.

**Rustflags allowlist** (`RustflagsProjectionV1`; primary source
`doc.rust-lang.org/rustc/command-line-arguments.html`, read 2026-09-06). Honored,
exactly:

| Flag | Constraint |
|---|---|
| `--cfg <ident>` / `--cfg <ident>="<value>"` / `--cfg=<…>` | identifier syntax; no spaces |
| `-A/-W/-D/-F <lint>`, `-A<lint>`… and long forms; `--cap-lints <allow\|warn\|deny\|forbid>` | lint name syntax `[a-z0-9_:]+` |
| `-C target-feature=…`, `-C target-cpu=…`, `-C opt-level=…`, `-C debuginfo=…`, `-C panic=…`, `-C overflow-checks=…`, `-C debug-assertions=…`, `-C strip=…` | value matches `[A-Za-z0-9_+,.=-]+` |
| `--remap-path-prefix <from>=<to>` | only when `<from>` is a verified in-snapshot or in-closure path |

Everything else is stripped and disclosed with a typed reason: `@file` response
files, `-C linker`, `-C link-arg(s)`, `-C link-self-contained`, `-C codegen-backend`,
`-C llvm-args`, `-C extra-filename`, `-L`, `--sysroot`, `--extern`, `-Z…`, `-o`,
`--out-dir`, `--emit`, unknown `-C` options, malformed `--cfg`. The projection
carries the constant `executableSelected=false`. Stripping a flag is disclosed in
the universe; it is never a reason to read the flag from anywhere else.

### 3.4 `UnifiedFeaturesV1`

Domain `native.unified-features.rust.v1`. Computed by the bundled Cargo through
the adapter (`cargo metadata --offline --frozen --locked --format-version 1
--filter-platform <target>`) over the sealed materialization under the verified
carrier. `cargo metadata` executes no build script and no proc macro; it does
invoke the bundled `rustc` (first-party, in the closure). A required package
absent from the materialization makes Cargo fail; the adapter maps that to
`completeness.incomplete` (DS-6) rather than attempting resolution.

### 3.5 Coverage semantics for missing external crates (`missing-external-crate`)

Given crate C depending (directly or transitively via activated edges) on
activated external package P absent from the set: `declares/literal/control-flow/
clones` for C: `complete`. `imports/references/calls/types` at resolved rungs for
C: `unknown`, deficiency `input-closure-incomplete`, cause
`missing-dependency-source`, detail `[P]`. Crates not depending on P: unaffected.
Remedy text: "vendor or import the sealed source for P"; never "install or enable
the provider".

### 3.6 `PreparedOutputSetV3`: inert rows only (feedback 4, R2)

Domain `native.prepared-output-set.v3` (revised in place; v3 was never accepted).
`{schemaVersion:3, preparation: {kind: authorized-execution|imported-descriptor,
authorizationId|null, importId|null, toolchain, dependencySourceSetId, cfgSetId,
producer}, rows: [PreparedOutputRowV3…]}`.

`PreparedOutputRowV3`: `{kind, ownerKey, configuration, site|null, generated|null,
inputBinding: {ownerFileManifestSha256, dependencySourceSetId, toolchainDigest,
cfgSetId}, blob: {sha256, byteLength, mediaType}, status: ok|failed,
failureDetail|null}`.

- **PO-0 (inert by kind and consumption channel; a media type is a label, never a
  trust proof)** Admissible row kinds are exactly three:
  `build-script-directives` (`text/x-cargo-directives`: the captured `cargo:`
  lines, including `rustc-cfg`/`rustc-env` consumed by `cfg`/`env!`),
  `macro-expansion` (`text/x-rust-expansion`: the fully expanded token text for one
  invocation `site` = `{path, startByte, endByte, inputTokenDigest}`), and
  `generated-file` (`generated = {logicalPath, blob}` with media type
  `text/x-rust-source`, `text/plain` or `application/octet-stream`: one data file
  a build script wrote under `OUT_DIR`). Row kinds `proc-macro-dylib` and
  `build-script-binary` are refused **regardless of the media type they claim**
  (a dylib relabelled `text/x-rust-expansion` is still a dylib row), and a media
  type outside the kind's set is refused; either is
  `native.prepared-output-not-inert` (exit 2), from an import *and* from the
  in-host step alike (`generated-file-media-type-is-not-trust-proof-kind-decides`).
  **No prepared artifact is ever loaded, linked or executed by the semantic
  worker.** Expansions are looked up by exact
  `(path, span, inputTokenDigest, macro crate manifest)`; a miss is a
  `macro-expansion-unavailable` edge (L-RS4).
- **PO-4 (generated-file input closure and the read-only virtual `OUT_DIR`)**
  The worker resolves `env!("OUT_DIR")` for owner *O* to the read-only virtual
  path `.opensip/out/v1/<ownerKey>/` in its sealed VFS. A site
  `include!(concat!(env!("OUT_DIR"), "/generated.rs"))` (likewise
  `include_str!`/`include_bytes!`) reads the `generated-file` row bound to
  `(ownerKey, logicalPath="generated.rs")` whose `inputBinding` equals the current
  context, and consumes its bytes **only** as Rust source text, a string literal or
  a byte literal respectively. A miss (no row, stale binding, failed owner) is a
  typed unknown: `build-script-generated-unavailable` edge, cause
  `generated-file-missing`; it is never a hard failure and never a fallback to a
  host path (`generated-file-include-out-dir-resolves-inert`,
  `generated-file-missing-is-typed-unknown-not-failure`). Strict bounds
  (`GeneratedInputBoundsV1`): `logicalPath` is a strict relative path (no `/`
  prefix, no `.`/`..` segment, no NUL or backslash, ≤ 1024 bytes; an escaping path
  fails exact typed admission and the worker lookup independently refuses it with
  cause `generated-file-out-of-bounds`), `maxGeneratedFilesPerOwner 4096`,
  `maxGeneratedFileBytes 67108864`, `maxGeneratedTotalBytes 1073741824`,
  `maxGeneratedFileRows 1000000` (protocol limit). Imported blobs are bound to
  archive members by exact `blobs[]` digest; an archive member outside the
  wrapper's `blobs` is never read (`generated-file-path-escape-and-bounds-refused`).
- **PO-1 (staleness)** A row is usable only if `inputBinding` equals the current
  context (owner manifest, dependency set, toolchain digest, cfg set). A stale row
  is refused before Plan construction (`REQUEST.PRECONDITION_FAILED`, detail
  `native.stale-prepared-output`, listing the differing fields) when prepared mode
  was selected explicitly, or is ignored with a disclosed `staleRows` list and
  non-prepared fallback when prepared mode was defaulted. It never uses a stale blob.
- **PO-2 (failed rows)** A `failed` build script is retained as a row so the same
  inputs need not be re-run; the owner is analyzed non-prepared
  (`build-script-generated-unavailable`).
- **PO-3 (imported)** An imported set carries the same binding fields and
  `provenanceAssurance: declared`; the host cannot verify that an external
  preparer produced the expansions faithfully. Facts derived from them are
  Plan-bound and disclosed with the import identity and producer.

Where do the expansions and generated files come from? From the **preparation
step** (§5.3), which is the only place proc-macro dylibs are built and loaded and
build scripts run, inside the authorized `repository-code` principal with live
boundaries. The step captures the required generated **data** and discards every
executable product; its output is the inert row set, and the worker consumes only
that.

---

## 4. Resolution completeness (AR-12)

### 4.1 Two different completeness claims

A Coverage entry commits two things that were previously conflated:

1. **Examined universe** — the exhaustive examined subject/target partition
   (`subjectScopeCommitment`, retained). "Did we look at every subject?"
2. **Resolution completeness** — whether every reference/import/call edge
   originating in the examined subjects was resolved to a binding at the requested
   rung, *after resolution was actually attempted over the whole partition*.
   "Could we see every consumer?"

### 4.1a Producing recipe for `subjectScopeCommitment` (closed)

The retained C-2 selector deferred computation and verification. This is the successor
recipe; nothing about the historical artifact changes.

**Recipe.** `subjectScopeCommitment` is the foundation **subject-scope** identity of the
examined partition, re-spelled in the native `Sha256Text` text form:

```
scope2      = identity-and-evidence H("subject-scope", D)          -> "scope2:"  + hex
commitment  = "sha256:" + the same 64 hex                          -> Sha256Text
```

where `D` is the closed foundation record
`identity-schemas.v2.json#/$defs/subject-scope`
`{schemaVersion: 2, snapshotId, sourceUniverse, targetUniverse, relation, resolution,
enumeratorClosure, subjects}`.

**Inputs, exactly, and where each comes from.** `snapshotId` is the admitted `snapshot2`.
`relation`/`resolution` are the Coverage key's own relation and rung. `sourceUniverse` and
`targetUniverse` are the bare 64-hex universe digests of the same key (§2, §11).
`enumeratorClosure` is the `closure2` of the Plan-bound enumerator that produced the
partition. `subjects` is the **complete** examined subject inventory that enumerator
enumerated over that snapshot, a canonical set (foundation ordering, duplicates refuse
rather than dedupe). **Encoding**: the foundation canonical encoder and `H` frame, imported,
not restated. There is **no native `H` domain for this field**: one preimage, one digest,
two admitted textual spellings (§11).

**Join with `scope2`.** The commitment is the *identical* digest to the `scope2` the host
binds into the `coverage2` descriptor (`coverage.scopeId`). It is therefore not a second
commitment and cannot drift from the scope it names. Its purpose is that the Coverage
*payload* — the bytes whose `payloadDigest` mints `coverage2` — carries the provider's
in-band commitment to the partition it claims to have examined, which the host then checks
against a value the provider never supplied.

**Where it is produced and checked (`admit_coverage_result_v3`, the admitted native producer
boundary).** For every `CoverageResultV3` a provider sends, before any `coverage2` exists:

1. The host builds `D` from **its own** enumeration and mints `scope2`. A provider-supplied
   commitment is never an input to this step.
2. `key.relation`, `key.resolution`, `key.sourceUniverse`, `key.targetUniverse` must equal
   `D`'s (`native.coverage-key-scope-mismatch:<field>`).
3. `key.subjectScopeCommitment` must equal the computed commitment
   (`native.subject-scope-commitment-mismatch`).
4. `entry.examinedUniverse.subjectScopeCommitment` must equal the key's
   (`native.examined-universe-commitment-mismatch`) and
   `entry.examinedUniverse.subjectCount` must equal `len(D.subjects)`
   (`native.examined-universe-subject-count-mismatch`). A provider that examined a narrower
   partition than the host enumerated is detected here, and by nothing else.
5. RC-2 (§4.3) is rechecked over the same partition.
6. Only then is `coverage2` minted from `{schemaVersion: 2, scopeId, payloadSchemaDigest,
   payloadDigest}`. `payloadSchemaDigest` is the raw SHA-256 of the **exact registered schema
   DOCUMENT bytes** (§7.2). A caller may restate it but never choose it: a value that is not the
   registered document's digest refuses `native.coverage-payload-schema-not-registered`
   (`coverage-payload-schema-digest-a-caller-chose-is-refused`).

Every refusal above is `PROVIDER.PROTOCOL_VIOLATION` (`operational-failed` 4) under the §10
fault law: a worker that lies about its partition contributes no facts, no Coverage and no
Run. This is not a Coverage deficiency; an admitted-but-incomplete input is (§10).

**Coverage use (`coverage_view_use`).** A `view2` may name a `coverage2` only if that
`coverage2` was admitted at the boundary above and its `scope2` is one of the view's own
`scopeIds`. A hash-valid `coverage2` whose subject scope sits outside the evaluated view is
refused exactly as hidden finding evidence is (identity §3), rather than joined silently.

**No circularity.** `D` names the snapshot, the universes and the enumerator closure. A
universe descriptor (§2) names its native context, tools and config projection; a native
context names closures; none of them names a scope, a Coverage, a view, an evidence record
or a Run. The derivation order is therefore total and acyclic: closures → native context →
universe → `scope2` → commitment → Coverage payload → `coverage2` → `view2`. The foundation
scope *descriptor* whose raw digest is `scopeDigest` (§1.4, workspace roots and path
prefixes) is a different record with a different job and is not this commitment.

Cases: `subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form`,
`subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list`,
`coverage-admission-mints-coverage2-from-the-host-subject-scope`,
`coverage-commitment-chosen-by-the-claimant-is-refused`,
`coverage-producer-chosen-narrower-examined-partition-is-refused`,
`coverage-examined-subject-count-that-disagrees-with-the-enumeration-is-refused`,
`coverage-key-naming-a-universe-outside-the-host-scope-is-refused`,
`coverage-complete-claimed-over-an-admitted-unresolved-edge-is-refused-at-the-boundary`,
`coverage-incomplete-over-an-exhaustive-partition-admits-with-the-same-commitment`,
`coverage-use-requires-the-subject-scope-to-be-in-the-evaluated-view`,
`coverage2-whose-subject-scope-is-outside-the-view-is-refused`,
`coverage2-never-admitted-at-the-producer-boundary-is-refused-in-a-view`,
`subject-scope-duplicate-subject-refuses-rather-than-silently-deduping`,
`coverage-payload-schema-digest-a-caller-chose-is-refused`. The two positive coverage cases
recompute the expected `coverage2` with `hashlib` from the scope, the registered schema-document
digest and the canonical payload rather than pinning a literal, so a schema-document edit moves the
identity visibly instead of silently invalidating a frozen value.

**Coordination (identity owner).** Identity §3 now states the same recipe in its own words —
`subjectScopeCommitment` is `"sha256:"` plus the 64-hex suffix of the admitted `scope2` identity,
"another textual form of the **same** digest, not a separate hash of the subjects or of the scope
identifier string" — and names the same descriptor fields and the same `subjectCount` rule. The two
statements agree; this section is the native-side normative detail (the producer boundary, the
refusal vocabulary and the coverage-use join) and adds no second recipe. Any future divergence
between them is a defect in whichever document moved.

Claim 1 never implies claim 2. The counterexample: module A exports `foo`; module
B does `import * as m from './a'` then `m[k]()` with `k` a runtime string. Every
subject is examined, `m` resolves, `m[k]` has no admissible fact at any rung of
`references`, so the v1 view reads `coverage=complete` and a "no consumer of `foo`"
predicate is *satisfied*. Under this contract the provider must emit an
`unresolved-edge` fact for `m[k]` with `targetScope=module` and report
`resolutionCompleteness.state=incomplete`; the predicate reports
`resolution-incomplete` and `foo`/`bar` are both marked affected (§4.5). Both
behaviors are executable in the reference model (`computed-access-m-k`, v1 oracle
versus v2).

### 4.2 Requirement v2

`RequirementV2` (closed): `{relation, minResolution, minConfidenceMillionths
(default 0), completeness: complete|partial-ok, quantifier:
existential|universal-negative, unresolvedEdgePolicy: forbid|disclose,
externalConsumerPolicy: forbid|assume-closed, derivationPolicy: any|declared-only
(relation `types` only), scope?}`.

- `quantifier=universal-negative` requires `completeness=complete`.
- A repair prerequisite, a `no-consumer`/`cold-code`/`unreachable` authoritative
  finding, and any predicate whose truth is a negative over consumers **must** use
  `universal-negative` with `forbid`/`forbid`. `disclose` and `assume-closed` are
  advisory postures; a rule pack declaring them for an authoritative Control
  verdict is refused at pack admission (`advisory-posture-in-control-rule`).

### 4.3 View entry v3 and `CoverageResultV3`

Per `(relation, rung, sourceUniverse, targetUniverse)` the view entry is
`ViewEntryV3`:

```
{ "relation", "resolution": rung, "coverage": "complete"|"unknown",
  "examinedUniverse": {"subjectScopeCommitment", "subjectCount"},
  "resolutionCompleteness": {
     "state": "complete"|"incomplete"|"partial"|"not-attempted"|"not-applicable",
     "attempted": bool, "examinedExhaustive": bool,
     "stageTerminal": "complete"|"unavailable"|"budget-exhausted"|"provider-fault"|"cancelled"|"crash"|null,
     "unresolvedEdgeCount": uint64, "unresolvedEdgeClasses": sorted unique UnresolvedEdgeKindV1 },
  "closedWorld": ClosedWorldV2 (§4.5),
  "derivationKinds": sorted subset of {annotated, jsdoc-declared, compiler-inferred},
  "confidenceMillionths": uint64, "deficiency": null|DeficiencyV2, "nativeCause": null|NativeCause }
```

`CoverageResultV3` on the wire = `{schemaVersion:3, key: CoverageKeyV2, entry}`;
the host wraps it in `coverage2` by exact `payloadSchemaDigest`/`payloadDigest`.

- **RC-1** `state=not-applicable` for one-rung relations (`file`, `package`,
  `vcs-change`, `declares`, `literal`, `control-flow`, `clones`) and syntactic
  rungs. A resolved rung (`resolved-target`, `resolved-binding`,
  `resolved-callee`, `checked`, `from-resolved-calls`) must never claim
  `not-applicable`. A `not-applicable` entry is *not* `complete`: it makes no
  resolution claim at all.
- **RC-2 (corrected, feedback 6)** `state=complete` requires **all** of:
  `attempted=true`, `examinedExhaustive=true`, `stageTerminal=complete`, and zero
  admitted `unresolved-edge` facts whose relation matches and whose referrer is in
  the examined set. `incomplete` requires ≥1 such fact with a complete stage over an
  exhaustive partition. `partial` is any attempted resolution whose stage ended
  `unavailable`/`budget-exhausted`/`provider-fault`/`cancelled`/`crash` or whose
  examined partition is not exhaustive — regardless of edge count. `not-attempted`
  is a skipped stage: `attempted=false`, count 0. A zero count therefore never
  implies `complete`. The host rechecks these relations after admission
  (`coverage_bijection`); any disagreement is `PROVIDER.PROTOCOL_VIOLATION`.
  Fixtures: `rc2-stage-unavailable-zero-edges-is-partial`,
  `rc2-skipped-stage-zero-edges-is-not-attempted`,
  `rc2-partial-examination-zero-edges-is-partial`,
  `rc2-not-applicable-zero-count-is-not-complete`, `protocol3-crash-mid-stage-is-not-complete`.
- **RC-3** `coverage=complete` with `state=incomplete` is a valid, honest entry:
  the examined partition is exhaustive and resolution is not. It is the expected
  result for most real JavaScript and for non-prepared Rust. Such an entry owes
  **no** deficiency and therefore no cause; when a host *does* declare
  `resolution-incomplete`, `resolutionCompleteness` is the field that carries the
  reason — the `state`, and `unresolvedEdgeClasses` for *all* applicable classes
  at once — and `nativeCause` is `null` by design. §10 closes which field carries
  which deficiency's cause and enforces it.
- **RC-4** Derived relations inherit: `reachability` counts `calls` edges over the
  same examined set; classes propagate.
- **RC-5** `maxUnresolvedEdgesPerStage = 1000000`; exceeding it is
  `BudgetExhausted` (unit `items`), which makes the stage `partial`.

### 4.4 Relation `unresolved-edge` (new registry entry)

`schemaId opensip.relation.unresolved-edge.v1`, layer `semantic`, ladder
`[observed]`, `universeRule same-only`. Payload (closed): `{referrer, relation:
imports|references|calls|types|reachability, edgeKind: UnresolvedEdgeKindV1,
targetScope: module|universe|external|unknown, targetModule|null, detail ≤ 512 bytes}`.

`UnresolvedEdgeKindV1` (closed, 16): `computed-member-access`,
`dynamic-import-nonliteral`, `require-nonliteral`, `indirect-eval`,
`reflective-access`, `untyped-any-call`, `unresolved-module-specifier`,
`external-module-boundary`, `structural-dispatch`, `trait-object-dynamic-dispatch`,
`generic-bound-dispatch`, `macro-expansion-unavailable`,
`build-script-generated-unavailable`, `cfg-excluded-region`, `ffi-extern`,
`entry-point-unrecognized`.

Each fact anchors the originating span. It is a product fact like any other: a
`fact2` record (FACT-ID-V2) minted by the host that wraps this payload by exact
`payloadSchemaDigest`, bound to `snapshot2` and the source/target universes. It is
never a finding. It does not appear in `resolutionCompleteness` for relations
where the provider attempted no resolution (those are `not-attempted`).

### 4.5 Closed-world assumptions (feedback 7)

`ClosedWorldV2` = `{exportsClosed: closed|open|unknown, entryPointsRecognized:
all|partial|none, nonliteralLoading: none|present, externalConsumers:
none-declared|possible|unknown, dynamicDispatch: resolved|present|not-applicable,
reasons[], deadCodeRepairEligible}`. `exportsClosed=closed` requires **every**
ingredient:

1. the manifest publishes nothing (`package.json` without `exports`, `main`,
   `module`, `types`, `bin`, `browser`, `files` or `workspaces`, with
   `private:true`; or a Cargo package with `[[bin]]` targets only);
2. `entryPointsRecognized=all` (explicit origins or a recognizer with no
   `unresolvedChoices`);
3. `nonliteralLoading=none` (no `require-nonliteral`, `dynamic-import-nonliteral`,
   `reflective-access`, `indirect-eval` edges in the universe);
4. `externalConsumers=none-declared` (the user/policy declares no non-repository
   consumers: no published subpath, no sibling deployment reading the tree).

`private:true` alone is `unknown` (`private-true-alone-is-not-closed`). A
universal-negative predicate on an exported subject of an `open`/`unknown`
universe with `externalConsumerPolicy=forbid` reports `external-consumers-unknown`.

**Dynamic edges propagate.** `affected_targets` marks every subject a dynamic
edge could reach: `targetScope=module` marks all exports of `targetModule`;
`universe` marks all subjects of the universe; `external`/`unknown` marks every
exported subject. A universal negative about an affected subject is
`resolution-incomplete` even when the entry's own count is zero for that relation
(`dynamic-edge-propagates-to-universe-and-external`).

**No missing entry point permits dead-code repair.** `deadCodeRepairEligible` is
true only with `exportsClosed=closed`, `entryPointsRecognized=all` and no
nonliteral loading; the workflow owner's repair prerequisites consume this flag
(H-5). Unrecognized frameworks yield `entryPointsRecognized=none`
(`framework-unrecognized-entry-points-none`); a config that would need evaluation
yields `partial`.

### 4.6 Sufficiency v2 (replaces `$.sufficiency`)

Evaluated in this order; every applicable cause is collected and the most specific
by §10 precedence is reported. `satisfied=true` may carry `disclosures`.

1. Relation absent from the view → `required-relation-missing`.
2. Rung below `minResolution` → the rung-unavailable cause (`language-tier-unsupported`, `provider-unavailable`, `input-closure-incomplete`, `budget-exhausted`) else `required-relation-missing`.
3. `confidenceMillionths < minConfidenceMillionths` → `confidence-floor-unmet`.
4. Relation `types` with `derivationPolicy=declared-only` and any `compiler-inferred` derivation in the view → `derivation-policy-unmet`.
5. `completeness=complete` and `coverage≠complete` → the entry's own deficiency.
6. `quantifier=universal-negative`: state `partial` or `not-attempted` → `resolution-incomplete` regardless of policy; state `incomplete` or target affected by a dynamic edge → `forbid`: `resolution-incomplete`; `disclose`: disclosure `{unresolved-edges, count, classes}`.
7. `quantifier=universal-negative`, target exported and `exportsClosed≠closed` → `forbid`: `external-consumers-unknown`; `assume-closed`: disclosure.
8. Dependencies (`dependsOn`) recursively (depth ≤ 4) with `partial-ok` for existential requirements and the parent's quantifier/policies for universal negatives.

There is no early exit. A one-rung relation under `existential` with
`partial-ok` passes step 5 vacuously but still runs steps 1–4 and 8: the former
step 9 shortcut ("satisfied outright") returned before the confidence floor and
let confidence 100000 pass a floor of 900000; it was removed (post-reset
SHOULD-4) and the regression case
`sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut`
checks that v2 and the retained v1 oracle both yield `confidence-floor-unmet`
for `clones` at 100000 under floor 900000, and `satisfied` at 1000000.

### 4.7 Positive coverage case (`positive-static-consumer`)

Module A exports `foo` and `bar`; module B does `import {foo} from './a'; foo();`
No computed access, no dynamic import, `package.json private:true` without
published entries, explicit entry points, no external consumers declared.
Provider emits `references@resolved-binding` for `foo`, zero `unresolved-edge`
facts, the stage completes, `resolutionCompleteness.complete`,
`exportsClosed=closed`. Then "no consumer of `foo`" → satisfied=false by evidence;
"no consumer of `bar`" under `universal-negative/forbid/forbid` → satisfied=true
with no deficiency. That is the only shape under which an authoritative
no-consumer claim is eligible. No provider verdict exists.

### 4.8 Type derivation provenance (feedback 12)

The v1 draft capped JSDoc-free JavaScript type facts at `confidenceMillionths ≤
900000`. That number had no evidence rationale: a compiler-inferred type is exact
under the admitted universe, and JSDoc presence is not a calibrated probability.
Replacement: every `types@checked` fact carries `TypeDerivationV1` =
`{derivationKind: annotated|jsdoc-declared|compiler-inferred, confidenceMillionths:
1000000, confidenceMethod: "native.confidence.v1", checkJs, limitations}`.
`native.confidence.v1` is the versioned, conformance-bound method
"declared-exact: every admitted checked fact is 1000000 under its universe; no
value below 1000000 is produced by a native provider". Rule authors express
"declared types only" through `derivationPolicy=declared-only` (§4.2), which
yields the typed `derivation-policy-unmet` deficiency, not a fake percentage.
`checkJs` is recorded because it changes diagnostics, not derivation.

---

## 5. Native execution boundary (AR-07)

### 5.1 Principal class `repository-code` and its joins (R4)

The security contract S10 registers principal class `repository-code`
(`RepoExecutionGrantV2`, execution classes `build-script | proc-macro |
test-runner`). One principal, three current spellings, joined explicitly and
checked by schema constants:

| Where | Spelling | Role |
|---|---|---|
| security S10 / `AuthorizedExecutionV2.principalClass` | `repository-code` | principal class of the admitted grant |
| foundation `identity-schemas.v2#semantic-grant.principals[].kind` / `AuthorizedExecutionV2.semanticGrantPrincipalKind` | `trusted-repository-code` | Plan-bound semantic projection `{kind, closureId (tool closure), ownerSourceDigest (owner file manifest)}` with `analysisOperations ∋ prepare-code` |
| workflow test-execution / `AuthorizedExecutionV2.workflowPrincipalSpelling` | `P-TRUSTED-REPO` | the workflow step's constant for the same principal (class `test-runner`) |

The **authority grant** is the operational `authorizationRef`
(`H("security.repo-execution-grant.v2", grant)`, the workflow's `securityGrantRef`):
it is excluded from the Plan descriptor and from every content identity
(`authorized-execution-interactive-with-declared-owner-disclosed` checks
`authorizationRefInPlan=false`). The **semantic grant projection** is what the Plan
binds. A universe with `preparedResolution=imported-inert` projects only
`read-import`; only `host-prepared` projects `prepare-code`. Prepared semantic
availability therefore never implies that this host holds or held an execution
grant (`prepared-imported-inert-implies-no-host-execution-grant`).

The principal, identified by `{projectId, snapshotId, ownerKey,
ownerFileManifestSha256, toolchainDigest}`, is **outside** the first-party TCB.
Executing it in-host is a disclosed trusted-code execution of code the user chose
to analyze; OpenSIP does not vouch for it and does not confine it unless a
platform primitive is enforced. The security owner supplies the revocation clock
and cancellation carrier (H-2).

### 5.2 `AuthorizedExecutionV2`

Domain `native.authorized-execution.v2`. Closed descriptor bound into
`rust-v2.executionCapableResolution` via `preparedOutputSetId`: `{schemaVersion:2,
operation:"native.prepare", principalClass:"repository-code", projectId,
snapshotId (snapshot2), dependencySourceSetId, toolchain, toolClosure, cfgSetId,
owners: [{ownerKey, kind: build-script|proc-macro, ownerFileManifestSha256,
provenanceAssurance: registry-authenticated|declared|in-snapshot}], effects:
{subprocess, filesystemWrite, network, environment: {requested, enforcement}},
authorization: {mode: interactive-explicit|policy-record, policyRecordId|null, ci},
liveBoundaries: {revocationCheck: before-each-owner, cancellation:
process-group-kill, trustClockRequired: true}, bounds}`.

`EnforcementV1` values are **copied from the security owner's platform truth
table**; this contract never asserts an `ENFORCED-PLATFORM` value itself, and the
model refuses a record that claims more than the pinned table (`permission-truth-tables.v9.json`:
`network`/`subprocess`/`filesystemWrite` `DISCLOSURE-ONLY`; `environment`
`ENFORCED-BY-CONSTRUCTION`).

**Which token each effect name is copied from (CB4-ADV-3).** The four effect
names here are `effects` field names; the pinned table is over seven closed
permission **tokens**, and the correspondence was determinate by elimination but
published nowhere, so an implementer had to infer it. It is stated:

| `effects` field | Permission token | `ENFORCED` in v9 (child-process) | What the value means |
|---|---|---|---|
| `subprocess` | `PT-PROC-EXEC-DECLARED` | `DISCLOSURE-ONLY` | No mechanism prevents the effect; the record states what was asked and answered. |
| `filesystemWrite` | `PT-FS-WRITE-HOST-STATE` | `DISCLOSURE-ONLY` | Same. See the scope note below. |
| `network` | `PT-NET-EGRESS` | `DISCLOSURE-ONLY` | Same. |
| `environment` | `PT-ENV-READ` | `ENFORCED-BY-CONSTRUCTION` | The child's environment is constructed by the host, so the capability is never conferred *in this execution mode*. |

Three scope facts travel with that table and none of them may be dropped:

1. **The values are per execution mode.** `native.prepare` runs owners as child
   processes, so the `child-process` column is the applicable one. In v9's
   `in-host-process` mode *every* token including `PT-ENV-READ` is
   `DISCLOSURE-ONLY`, because a component sharing the host's address space shares
   its environment. Quoting `ENFORCED-BY-CONSTRUCTION` without its mode would
   over-claim.
2. **`PT-FS-WRITE-HOST-STATE` is not repository filesystem authority.** The token
   names the *host's own state store*. Neither it nor any grant over it confers
   authority over the repository tree, and its `DISCLOSURE-ONLY` value says
   precisely that nothing prevents writes anywhere: the executing code holds the
   invoking user's ambient authority throughout. `filesystemWrite` here is a
   disclosure of that fact, never a scoping of it.
3. **`PT-HOST-EFFECT-BROKERED` is deliberately unprojected.** It is the one token
   whose v9 value is `ENFORCED-AT-HOST-BROKER`, and no `effects` field carries
   it, because repository code under `native.prepare` is not routed through a
   host broker. `EnforcementV1` admits the value, so the vocabulary is not
   narrowed; nothing in this contract claims it. The two read-only tokens
   (`PT-FS-READ-PROJECT`, `PT-FS-READ-COMPONENT`) are likewise unprojected: they
   are not effects this record authorizes.

Confinement is never claimed, and every value above remains the security owner's
to change: if a primitive is later measured on a platform, only that cell moves.

The mandatory pre-execution sentence, in human and
JSON output: "Build scripts and procedural macros from N packages will run with
your user's authority. OpenSIP does not prevent network access or other effects on
this platform." followed, when applicable, by "Packages with declared
(unauthenticated) provenance: …".

Authorization: interactive → explicit per-invocation confirmation naming the
owners; CI (`ci=true`) → never prompts; requires a pre-existing `policy-record`
bound to the same `dependencySourceSetId` and toolchain, else
`REQUEST.PRECONDITION_FAILED` / `native.execution-not-authorized`. Missing live
boundaries, an unavailable bundled linker, or an over-claimed enforcement value
refuse the same way. Authorization is never inherited by another ProjectId,
snapshot with a different owner manifest, or toolchain.

### 5.3 What the preparation step does (feedback 4)

Owned by the host resolved-inputs adapter (never the semantic worker), after
snapshot seal and dependency-source admission, before PlanId:

1. Verify the carrier (§3.3 CC-1..CC-5); materialize snapshot and dependency
   sources read-only in private scratch; write the single projected
   `.cargo/config.toml`; construct the environment.
2. Check current trust and revocation state (security owner's clock), then for
   each owner in order: re-check revocation (`before-each-owner`), run the bundled
   Cargo to compile and execute the build script or to build the proc-macro crate
   for the selected cfg set (`cargo check --offline --frozen --locked --target
   <triple>` restricted to the owners; the linker used is the closure linker;
   nothing is installed).
3. **Inside this same authorized step**, drive the bundled compiler's expansion
   through the closure proc-macro server for every invocation site in the
   workspace and dependency crates that names one of the built proc-macro crates,
   and capture the expanded token text per site as `macro-expansion` rows; capture
   `cargo:` directive output as `build-script-directives` rows. Loading the
   proc-macro dylib *is* executing repository code; it happens here, under the
   principal, with the live boundaries, and nowhere else.
4. **Capture required generated data, discard executable products** (R2). For
   each build-script owner: capture the `cargo:` directive lines as a
   `build-script-directives` row; capture as `generated-file` rows the regular
   data files under `OUT_DIR` named by the crate's
   `include!/include_str!/include_bytes!(concat!(env!("OUT_DIR"), …))` sites when
   those are statically determinable, else every regular data file under
   `OUT_DIR` within the PO-4 bounds; discard the build-script binary, every
   dylib/object/archive/executable product and unreferenced scratch files; discard
   the proc-macro dylibs. Referenced paths the script did not produce are recorded
   (`missingReferencedPaths`) and become typed unknowns at analysis. Nothing of
   `OUT_DIR` survives except the captured data rows
   (`preparation-capture-keeps-referenced-data-discards-executable-products`).
   The result is `PreparedOutputSetV3` (`kind: authorized-execution`).

The semantic worker then consumes the inert set through the protocol
(`PreparedOutputManifest/Chunk/Seal`), looks up expansions by exact site key, and
executes nothing. `RepositoryResolutionV3.workerExecutesRepositoryCode` is the
constant `false`. An external preparer may supply the same inert shape
(`kind: imported-descriptor`, `declared` provenance, §3.6 PO-3); it can never
supply a dylib.

### 5.4 Failure, retry, cancellation, recovery

| Event | Outcome |
|---|---|
| Owner build script exits non-zero | row `failed`; other owners continue; owner analyzed non-prepared |
| Revocation observed before an owner | step stops; no further owner runs; rows already captured are discarded; `request-rejected` (`native.execution-not-authorized`) |
| Wall or byte bound exceeded | whole step `operational-failed` (4); no row admitted. Existing `HOST.IO_FAILURE` with detail `native.prepare-bound-exceeded`. Not `BudgetExhausted`: a preparation bound is a safety bound of the adapter |
| Cancellation | kill the process group, discard partial OUT_DIR and captured rows, `interrupted` (130) |
| Retry | idempotent by `(dependencySourceSetId, toolchainDigest, cfgSetId, owners manifest)`; an identical inert set already in custody is reused without re-execution and without re-prompt when a policy record covers it |
| Host crash mid-step | scratch reclaimed by ordinary crash reconciliation; no partial set is visible to Plan construction |
| Ambient Cargo config found | `operational-failed` (4), `native.ambient-cargo-config`; never merged |
| Imported set replaces in-host preparation | allowed; PO-0/PO-1/PO-3 apply |

### 5.5 Where this stops

No sandbox is claimed. No DR-128 scope opens. No general test runner is defined
here (AR-08, workflow owner). The TypeScript side selects no repository execution
(`executionCapableResolution=false`); `postinstall` scripts, bundler plugins and
`ts-node` transforms are never run. "No network fetch" is a design invariant of
first-party code, not an enforced bound on repository code.

---

## 6. Clone equivalence modes (AR-13)

### 6.1 Modes and evidence levels

| Mode | Level/algorithm | Evidence level (closed) | Authority |
|---|---|---|---|
| `exact` | `L0-verbatim` | `byte-identical` | fact |
| `normalized` | `L1-lexical` (default) or `L2-comment-insensitive` (opt-in) | `lexically-identical` / `comment-insensitive-identical` | fact |
| `structural` | `L3-identifier-insensitive` | `identifier-insensitive-identical` | fact |
| `near` | `near-v1`: Jaccard over 5-gram shingles of the L3 token stream | `similar-candidate` | candidate only |
| `cross-tsjs` | `tsjs-erasure-v1` projection, then L3 | `cross-language-syntax-candidate` / `excluded` | candidate only |

No semantic equivalence is inferred by any mode.

### 6.2 Parameters (selected)

`minOccurrences 2`; `minBodyBytes 64` (exact); `minTokens 20` (L1–L3,
cross-tsjs); `minTokens 50` (near); `nearThreshold 800000` millionths;
`maxCandidatesPerGroup 4096`; `maxGroupsPerUniverse 1000000`.

### 6.3 Bodies and language-specific exclusions

Body spans are function, method, closure/lambda, `impl` item and block bodies.
**Import exclusion means candidate exclusion, not byte editing** (R5): a span that
consists solely of import/`use`/`extern crate`/top-level `require` declarations,
module/file headers, shebangs, license headers, `#![...]` inner attributes or
`declare`-only TypeScript declarations is an *import-only body* and is excluded
as a clone candidate in every mode. A body that is kept is hashed over its
**exact verbatim bytes**: an internal `use`, `import()`, `require` or directive
inside a function body is part of the preimage and is never stripped, rewritten
or normalized away at L0 (`clone-import-only-body-excluded-and-kept-bodies-hash-verbatim`:
two bodies differing only by an internal `use` line are not exact clones).

| Language | Kept significant at every level | L2 removes | L3 renames |
|---|---|---|---|
| TypeScript/JavaScript | string/template literal contents, regex literals, JSX text, `'use strict'`/`'use client'` directives, `/// <reference>` and `// @ts-*` directives, decorators | non-directive comments | local `let/const/var`, parameters, local function names, destructured locals; **not** properties, imports, exports, globals, `this` members |
| Rust | macro invocation token trees verbatim, attributes including `#[cfg]`, string/byte/raw literals, lifetimes | non-doc comments | local `let` bindings, parameters, closure parameters, pattern bindings; **not** fields, paths, generics, trait names, macro-introduced names |

Fact identity is same-language: `languageId ∈ {typescript, javascript, rust}` is
in the preimage, so a TypeScript body never groups with a JavaScript or Rust body
in `exact`/`normalized`/`structural`, even with identical bytes.

### 6.4 TS/JS cross-language decision (feedback 9)

Decision: `languageId` **stays** in exact fact identities (a `.ts` and a `.js`
body are different facts). Cross-TS/JS matching is a separate **candidate-only**
mode `cross-tsjs` under the named deterministic syntax projection
`tsjs-erasure-v1`:

- Removed before L3 normalization: type annotations, `type`/`interface`
  declarations, type parameter lists, `as` assertions, `satisfies`, non-null `!`,
  definite-assignment `!`, `declare`/`readonly`/`abstract`/access modifiers,
  `implements` clauses, `import type`/`export type`.
- **Never removed**: tokens that TypeScript compiles into runtime behavior —
  `enum`/`const enum`, parameter properties (`constructor(private x)`),
  value-bearing `namespace`, decorators, `import =`. A body containing any of them
  is **excluded** from cross matching with reason
  `runtime-significant-ts-tokens` and the token list; it is not projected.
- Output rows carry `projectionId=tsjs-erasure-v1`, `authority=candidate-only`,
  `semanticEquivalenceClaimed=false`, `automaticDeletionEligible=false` as schema
  constants. A cross candidate is never a baseline member, never a Control input,
  never a repair prerequisite.

Cases: `clone-cross-tsjs-candidate-only`, `clone-cross-tsjs-runtime-significant-excluded`.

### 6.5 Reviewed suppressions and false-positive boundary

`CloneSuppressionV1` is a superseded draft transport shape, admitted by no product
command. The single current review/suppression record is workflow ReviewDisposition.
Its stable candidate key, mandatory finite expiry and advisory-only semantics are
defined in workflow §12. Suppressed groups remain queryable with rationale and
expired suppressions resurface. Fixed by
`clone-false-positive-boundary`: trivial getters below thresholds → no candidate;
bodies identical except a string literal → not clones at L0–L3; identical except
comments → L1 not clones, L2 clones; identical bytes in two languages → never a
fact group.

---

## 7. Imported evidence: one `import2` wrapper, one canonical payload per kind (feedback 2, R3)

Every import is exactly one foundation `import2` descriptor
(`identity-schemas.v2.json#/$defs/import`, `schemaVersion=2`):
`{kind ∈ runtime|test|history|dependency|prepared, payloadSchemaDigest,
payloadDigest, sourceCorrespondenceDigest, buildDigest, producerClosure,
adapterClosure, blobs[], scopeDigest, observationDigest, completeness, omissions}`.
`ImportId = "import2:" + H("import", wrapper)` — computed by
`identity-model.identifier('import', …)`, never by this unit. It is the only
H-domain identity in an import.

### 7.1 Registry: kind → one schema document, selector, payload domain

Joint decision (workflows finished): the runtime/test/history payloads are the
workflow owner's single canonical schemas; native owns dependency/prepared. The
registry (`ImportRegistryRowV1`, mirrored from the workflow `PayloadRegistryV1`,
checked by `import2-registry-one-schema-document-per-kind`):

| `kind` | Schema document (path under `docs/coop/design-corrections/`) | Selector | `payloadDomain` | Owner |
|---|---|---|---|---|
| `runtime` | `workflows/schemas/imported-evidence.schema.json` | `#/$defs/RuntimePayloadV1` | `workflow.import-payload.runtime.v1` | workflow |
| `test` | `workflows/schemas/test-execution.schema.json` | `#/$defs/TestPayloadV1` | `workflow.import-payload.test.v1` | workflow |
| `history` | `workflows/schemas/imported-evidence.schema.json` | `#/$defs/HistoryPayloadV1` | `workflow.import-payload.history.v1` | workflow |
| `dependency` | `native/native-evidence.schemas.v2.json` | `#/$defs/DependencySourcePayloadV1` = `{payloadDomain, set: DependencySourceSetV1, acquisitionSourcePath, tarballDigests[]}` | `native.import-payload.dependency-source.v1` | native |
| `prepared` | `native/native-evidence.schemas.v2.json` | `#/$defs/PreparedOutputPayloadV1` = `{payloadDomain, set: PreparedOutputSetV3}` | `native.import-payload.prepared-output.v1` | native |

There are **no alternate admitted payload domains**. The native
`RuntimeCoverageAdapterInputV1`, `TestResultsAdapterInputV1` and
`HistoryAdapterInputV1` records remain **input adapter shapes only**: the native
adapter normalizes them into the canonical workflow payload *before* `import2`
(`normalize_runtime_coverage`, `normalize_test_results`, `normalize_history`),
and `import2_wrap` refuses an un-normalized adapter shape
(`UNNORMALIZED_ADAPTER_SHAPE`) and a payload whose `payloadDomain` is not the
registry row's (`IMPORT.KIND_PAYLOAD_MISMATCH`). Normalization is lossless where
the canonical schema has a field and **honest** where it does not: a test result
imported without captured output or argv lists `stdout-not-captured` /
`stderr-not-captured` / `argv-not-recorded` as wrapper omissions instead of
inventing an empty capture; a truncated history lists `history-truncated`.

Semantics that survive normalization: runtime subject states `observed-hit`,
`observable-unhit`, `unobservable`, `unmapped` (`observable-unhit` ≠ unused;
`unobservable`/`unmapped` ≠ unhit; unmapped correspondence turns every subject
`unmapped`; one window is never universal non-use; runtime coverage is never
OpenSIP Coverage); an impact-selected test list with
`completenessEstablished=false` is a bounded recommendation, never proof of
selection completeness; history is an advisory priority input.

### 7.2 Digests (joined to the workflow `ImportWrapperV2` recipe)

Every auxiliary digest is the **raw SHA-256 of the canonical bytes of an exact
closed record retained as a blob** (identity-and-evidence §2); none is an
`H(domain)` identity:

| Field | Preimage |
|---|---|
| `payloadSchemaDigest` | the **exact full schema DOCUMENT file bytes** of the registry row (never a canonicalization of a selected `$def`) |
| `payloadDigest` | canonical payload bytes |
| `sourceCorrespondenceDigest` | canonical `common#/$defs/SourceCorrespondence` |
| `buildDigest` | canonical `BuildIdentityV1 {schemaVersion:1, buildIdentity|null}` |
| `scopeDigest` | canonical foundation `scope-descriptor` (§1.4; the workflow `ImportScopeDescriptor` is its exact mirror) |
| `observationDigest` | canonical `ImportObservationV1 {schemaVersion:1, kind, window|null, population|null, selection|null, revisionRange|null}` |

`import2-raw-digest-differs-from-semantic-identity` pins the raw digests against
hand-spelled preimages and pins an `H(domain, record)` identity separately so the
two encodings are never confused. `completeness ≠ complete` requires non-empty
`omissions`.

### 7.3 Correspondence and mapping (workflow shared `SourceCorrespondence`)

`SourceCorrespondence` = `{kind: exact-snapshot, snapshotId}` or `{kind:
vcs-revision, vcsRevision{system, commit, dirty}, buildIdentity|null,
sourceMappingDigest|null}`. There is no `declared-build` kind. Mapping law
(`import_correspondence`):

- `exact-snapshot` naming an admitted `snapshot2` → **mapped**.
- `vcs-revision` → mapped **only** through an admitted workflow `SourceMappingV1`
  (`{snapshotId, producerClosure, entries[{generatedPath, generatedSha256,
  sourcePath, sourceSha256}]}`) whose raw digest equals `sourceMappingDigest`,
  whose `snapshot2` is admitted, whose commit is clean, and whose **every**
  `sourceSha256` equals the admitted snapshot's inventory digest at `sourcePath`
  (`correspondence-verified-per-file-vcs-mapping-maps-to-snapshot2`).
- A commit name alone (even clean), a declared build string alone, a mapping with
  one mismatched file, or a mapping whose digest differs → **unmapped**
  (`IMPORT.SOURCE_MAPPING_REQUIRED`); such evidence is listable but never feeds a
  predicate (`correspondence-commit-name-or-build-string-alone-never-maps`).

### 7.4 Former workflow conflict: resolved in the current workflow bytes

An earlier revision recorded that `workflows/workflows_model.v1.py#build_import`
computed the auxiliary digests as `H('workflow.…')` identities and that
`workflows-and-surfaces.md` §4/§10 listed dual payload domains. The current
workflow bytes resolve both: `doc_digest` is the raw SHA-256 of the canonical
closed record (retained as a blob, explicitly "NOT an H(domain) identity"),
`buildDigest` hashes the closed `BuildIdentityV1` record, and the registry lists
one payload domain per kind (`workflow.import-payload.{runtime,test,history}.v1`,
`native.import-payload.{dependency-source,prepared-output}.v1`). The integration
checker's `native-workflow-wrapper-equality.*` checks compare this unit's
`import2_wrap` with the workflow `build_import` wrapper byte for byte. Nothing
remains open here; no conflict is carried in §13.

---

## 8. Zero-config framework recognition

`FrameworkRecognitionV1` (domain `native.framework-recognition.v1`):
`{schemaVersion:1, recognized: [{recognizerId, recognizerVersion:1, evidence:
[{path, contentSha256, field}], assurance: declared|inferred, effects:
{entryPoints, testGlobs, ignoreConventions}, unresolvedChoices}], observedHints:
[{dependencyName}], entryPoints: {state: all|partial|none, source}}`.

Recognizers (exactly nine, version 1): `node-package`, `typescript-config`,
`npm-workspaces`, `pnpm-workspace`, `cargo-package`, `cargo-workspace`, `nextjs`,
`vite`, `vitest-jest`.

- **FR-1** Recognition reads manifests as data through the exact parser; it
  executes nothing. A config requiring evaluation yields
  `unresolvedChoices: ["config-requires-evaluation"]` and `entryPoints.state=partial`.
- **FR-2** Every effect enters the declared-input path with provenance
  `DISCOVERED:<recognizerId>@<version>`; explicit configuration wins and sets
  `entryPoints.source=explicit`.
- **FR-3** Unrecognized frameworks: `observedHints` lists manifest dependencies
  naming a framework outside the registry; `entryPoints.state=none`; analysis
  proceeds; `reachability` universal negatives are `resolution-incomplete`
  (`entry-point-unrecognized`); closed-world is `unknown`; no refusal.
- **FR-4** `maxRecognizersPerUnit 32`, `maxEvidenceFilesPerRecognizer 64`,
  `maxEntryPointsPerUnit 65536`.
- **FR-5** A recognizer version change is a Plan-visible change.

Closed-world facts (`exportsClosed`) are no longer decided by a recognizer alone;
they are composed in §4.5 from manifest, entry points, edges and declared consumers.

---

## 9. Provider protocol successors (wire)

### 9.1 Versions and identity negotiation (feedback 1)

`rust-semantic` protocol major **3**; `typescript-semantic` protocol major **2**.
Capability tokens (closed, `CapabilityToken`): identity tokens
`source-identity-snapshot2`, `plan-identity-plan2`, `fact-identity-fact2`,
`coverage-v3`; plus `sealed-vfs-v1`, `multi-stage-analyze-v1`,
`<lang>-semantic-facts-v1`, `resolution-completeness-v2`, `unresolved-edge-v1`,
`dependency-source-v1` (Rust), `prepared-output-v3` (Rust), `native-context-v2`.
`HelloV3` also carries `identityVersions: {snapshot:2, plan:2, fact:2, coverage:3}`
and `HelloAckV3` must echo it exactly.

Reject-before-disclosure ordering:

1. **Plan time (no spawn).** The host reads the signed capability row. The four
   identity tokens are required for every worker; a row lacking any of them, or
   any token the Plan needs, is never spawned: affected Coverage keys are
   `unknown / provider-unavailable` (cause `capability-missing`). No raw
   `snapshot2`, `plan2` or source byte reaches a worker that cannot name them
   (`negotiation-v1-only-worker-never-spawned`).
2. **Hello → HelloAck (no source bytes).** Exact recursive equality of the token
   array and identity versions; mismatch → `FAULT`, `PROVIDER.PROTOCOL_VIOLATION`,
   no snapshot, dependency or prepared byte is ever written.
3. **OpenUniverse** carries `snapshot2`, `plan2`, the universe descriptor
   including `nativeContext`, and `RepositoryResolutionV3`. The host state
   machine admits it only when `identityNegotiated=true`; otherwise the run faults
   with `sourceBytesSent=false` (`protocol3-open-universe-without-identity-faults`).
4. Snapshot custody, dependency-source custody, prepared custody,
   `NativeContextVerified`, then Analyze.

Existing V1 relation payload grammars are reused unchanged inside `fact2` by
exact `payloadSchemaDigest`; legacy FACT-ID-V1 identities remain historical and
are never relabeled.

### 9.2 Frames (Rust major 3)

| Frame | Direction | Payload | Terminal |
|---|---|---|---|
| `DependencySourceManifest` | host→worker | `{dependencySourceSetId, manifestSha256, entries[{packageKey, path, byteLength, contentSha256}]}` | no |
| `DependencySourceChunk` | host→worker | `{dependencySourceSetId, packageKey, path, chunkIndex, byteOffset, bytes}` | no |
| `DependencySourceSeal` | host→worker | `{dependencySourceSetId, manifestSha256, entryCount, totalBytes, totalChunkCount}` | no |
| `DependencySourceAccepted` | worker→host | exact seal echo after digest/VFS validation | no |
| `PreparedOutputManifest/Chunk/Seal/Accepted` | as above for inert rows only | row kinds restricted to the three inert kinds (§3.6 PO-0); generated-file rows are mounted read-only under the virtual `OUT_DIR` | no |
| `NativeContextVerified` | worker→host | `{nativeContextId, recomputedNativeContextId, equal:true}` — a mismatch is sent as `Unavailable(native-context-mismatch)` | no |
| `CoverageV3` | worker→host | `CoverageResultV3` entries, exact bijection with the requested domain | no |

`RepositoryResolutionV3` = `{dependencySourceSetId, preparedOutputSetId|null,
authorizationId|null, workerExecutesRepositoryCode:false, effects|null}` (the
old `network` boolean is replaced by the disclosed effects copied from
`AuthorizedExecutionV2`). `UnavailableReasonV3` adds `native-context-mismatch`,
`dependency-source-incomplete`, `prepared-output-stale`,
`prepared-output-not-inert`, `capability-missing`, `identity-version-mismatch`.

State machine phases (host side, 22): `START, WAIT_HELLO_ACK, READY_OPEN_UNIVERSE,
WAIT_UNIVERSE_ACCEPTED, READY_SNAPSHOT_MANIFEST, RECEIVING_SNAPSHOT,
WAIT_SNAPSHOT_ACCEPTED, READY_DEPENDENCY_MANIFEST, RECEIVING_DEPENDENCY,
WAIT_DEPENDENCY_ACCEPTED, READY_PREPARED_MANIFEST, RECEIVING_PREPARED,
WAIT_PREPARED_ACCEPTED, WAIT_NATIVE_CONTEXT_VERIFIED, READY_ANALYZE, ANALYZING,
READY_COMPLETE, WAIT_CANCELLED, WAIT_ZERO_EXIT, WAIT_EOF, DONE, FAULT`. The
34-rule first-match/total-fallback table is `PROTOCOL3_RULES` in the model;
`dependencyMode`/`preparedMode` are set at OpenUniverse, `identityNegotiated` at
HelloAck. A process fault, post-terminal frame or unmatched frame is `FAULT`. A
stage that ends in `FAULT`, `Unavailable` or `BudgetExhausted` yields
`stageTerminal ≠ complete` for every entry of that stage (§4.3 RC-2).

### 9.3 Limits (`ProtocolLimitsV3`, exact equality in Hello)

`maxDependencySourcePackages 4096`, `maxDependencySourceEntries 1000000`,
`maxDependencySourceTotalBytes 8589934592`, `maxDependencySourceChunkBytes 1048576`,
`maxUnresolvedEdgesPerStage 1000000`, `maxCfgSets 4`, `maxExpansionRows 1000000`,
`maxGeneratedFileRows 1000000`. All 24 v2 limits are retained with identical values.

### 9.4 TypeScript major 2

Adds identity negotiation, `nativeContext` (`typescript-v2`, the
`TypeScriptNativeContextV2` of §2.4), `CoverageV3`, `resolution-completeness-v2`,
`unresolved-edge-v1`, `native-context-v2`. No dependency-source or prepared frames
(`node_modules` is in the snapshot read set). The `NativeContextVerified` frame and the
`native-context-mismatch` unavailable reason apply here too: the TypeScript worker
recomputes `TypeScriptNativeContextV2` after custody and refuses before Analyze on any
differing byte. `Unavailable.reason` adds `capability-missing`,
`identity-version-mismatch`, `node-modules-outside-read-set`.

### 9.5 Independent derivation

The worker recomputes `NativeContextV2` and every `resolutionCompleteness` record
from its own admitted facts and stage outcome; the host recomputes the bijection
and the RC-2 preconditions. Equal inputs must yield byte-identical descriptors.

---

## 10. Deficiencies, precedence and D9 mapping

`DeficiencyV2` = fact-plane v1 values + `input-closure-incomplete`,
`derivation-policy-unmet`, `resolution-incomplete`, `external-consumers-unknown`.
Precedence (most specific first): `language-tier-unsupported`,
`provider-unavailable`, `input-closure-incomplete`, `budget-exhausted`,
`confidence-floor-unmet`, `derivation-policy-unmet`, `resolution-incomplete`,
`external-consumers-unknown`, `required-relation-missing`.

**Existing D9 codes only (R7).** No successor, interim or competing code exists in
this contract; `d9_successor_codes()` is the empty list and `d9_map` refuses a row
that names one. The native `deficiency` and `nativeCause` travel as **typed
detail** inside the `coverage2` record (`CoverageResultV3.entry.deficiency` /
`nativeCause`) that the host termination names by its `coverageId`; no D9 enum
changes anywhere.

**The Cause column is not one field.** This column previously read `Cause
(nativeCause)` throughout, and three of its rows then named values the closed
`NativeCause` enum cannot express: `computed-member-access`, `exports-open` and
`compiler-inferred` each fail schema validation as a `nativeCause`. The only
representable value for those rows was `null` — which that enum's own
description defines as *a disclosure was owed and not made*, the exact argument
that added the three `body-language-*` members. Worse, nothing compared the pair
to anything, so a `resolution-incomplete` entry carrying the unrelated but
schema-valid `lockfile-missing`, or relabelled `capability-missing`, or a
`derivation-policy-unmet` over an empty `derivationKinds`, each closed a Run.

The correction names the carrier per row rather than adding enum members, and
that is a decision on the merits, not on compatibility: `resolution-incomplete`
has a genuinely **set-valued** cause — an entry can exhibit up to all sixteen
`UnresolvedEdgeKindV1` classes at once — so a scalar could only lose information
or force an arbitrary pick, which is the multi-cause defect itself. All three
rows already have closed, structured, independently derived carriers **in the
same entry**: `resolutionCompleteness` (whose `unresolvedEdgeClasses` RC-2
already forces to equal the admitted `unresolved-edge` facts of the view),
`closedWorld.exportsClosed`, and `derivationKinds`. **No enum changes anywhere** —
not `NativeCause`, not `DeficiencyV2`, not `UnresolvedEdgeKindV1`, not the public
`DomainDetailCode` registry, and no D9 class, code or exit.

Where the Carrier column says a field other than `nativeCause`, `nativeCause` is
`null` **by design** and that null is no longer an escape: admission refuses
unless the named field actually carries the cause. The pairing is closed in
`native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry`, derived
at the producer boundary in `admit_coverage_result_v3` and therefore re-derived
at retained Run closure, which re-runs that exact admission over the retained
payload (`native.coverage-cause-*`, `PROVIDER.PROTOCOL_VIOLATION`).

| Native detail | Cause carrier and lawful value | `nativeCause` | D9 class (host-owned) | Existing code | Typed detail carrier |
|---|---|---|---|---|---|
| `input-closure-incomplete` | `entry.nativeCause` — one of `missing-dependency-source`, `lockfile-missing`, `source-replacement-outside-snapshot`, `generated-output-unavailable`, `generated-file-missing`, `generated-file-out-of-bounds`, `no-program-unit`, `node-modules-outside-read-set`, `config-flag-stripped`, `body-language-ownership-missing`, `body-language-owner-unenumerated`, `body-language-owner-ambiguous` | **required** | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `resolution-incomplete` | `entry.resolutionCompleteness` — `state` ∈ {`incomplete`, `partial`, `not-attempted`} names the stage condition, and `unresolvedEdgeClasses` carries **every** applicable class at once | `null` | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `external-consumers-unknown` | `entry.closedWorld.exportsClosed` ∈ {`open`, `unknown`} — the values the old cell spelled `exports-open`, `exports-unknown` | `null` | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `derivation-policy-unmet` | `entry.derivationKinds` must contain `compiler-inferred` | `null` | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `provider-unavailable` | `entry.nativeCause` — `capability-missing` or `linker-unavailable` where one applies; the row is otherwise self-describing (incl. missing identity tokens) | optional | `indeterminate` (3) | `COVERAGE.PROVIDER_UNAVAILABLE` | coverage2 record |
| `language-tier-unsupported` | `entry.nativeCause` = `capability-missing` — the admitted universe's selected grammars do not bear the requested `relation@rung` (§1.2 syntax-only capability law); **no other cause is lawful here** | **required** | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `budget-exhausted` | `entry.resolutionCompleteness.stageTerminal` = `budget-exhausted` — the stage terminal the old cell referred to parenthetically | `null` | `indeterminate` (3) | `COVERAGE.BUDGET_EXHAUSTED` | coverage2 record |
| `confidence-floor-unmet` | **none in the entry** — the floor is `RequirementV2.minConfidenceMillionths` and the entry carries only its own `confidenceMillionths`, so the comparison is the sufficiency evaluation's. Stated as a limit rather than given an invented entry-level predicate | `null` | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |
| `required-relation-missing` | **none in the entry** — a sufficiency verdict about a relation the view carries *no* entry for, so an entry can never be its own evidence | `null` | `indeterminate` (3) | `VERDICT.INDETERMINATE` | coverage2 record |

A `null` deficiency requires a `null` cause: a cause without a deficiency names
why nothing went wrong.

**Multiple simultaneous causes, and precedence.** An entry carries **one**
deficiency and **every** carrier at the same time. The carriers are structurally
independent — `unresolvedEdgeClasses` is an array holding all applicable classes
at once, and `closedWorld` and `derivationKinds` are separate fields — so the
scalar deficiency loses nothing: the other simultaneous conditions stay fully
disclosed in their own fields. Which single member is declared when several
apply is the precedence order above, applied by the owning sufficiency
evaluation against a **Requirement**. That selection is deliberately **not**
re-derived from the entry alone, and the limit is stated rather than worked
around: several conditions are requirement-relative (external-consumer state
matters only for a universal negative about an exported target; the confidence
floor lives in the Requirement), and **RC-3** makes `coverage: complete` with
`state: incomplete` and *no* deficiency a valid honest entry. Forcing a
deficiency out of exhibited entry evidence would refuse lawful Runs. What is
decidable from the entry, and what is therefore enforced, is the other
direction: a **declared** deficiency must be **supported** by the entry's own
committed evidence.

**Retained and public routes are different, and both are named.** *Retained*:
the whole `ViewEntryV3` lives inside the `coverage2` record whose payload and
schema digests the Run commits, so every carrier above is retained evidence a
verifier re-derives. *Public*: the **deficiency** projects outward as its own
closed `DomainDetailCode` — `resolution-incomplete`, `external-consumers-unknown`
and `derivation-policy-unmet` are already members — and the **cause** travels as
typed detail in the `coverage2` record the host termination names by its
`coverageId`, exactly as this section has always said for the
`nativeCause`-carried rows. No new public code is added and none is needed.
| stale prepared/import row selected explicitly; non-inert prepared row | | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | details `native.stale-prepared-output` / `native.stale-import` / `native.prepared-output-not-inert` |
| execution not authorized (CI without policy; missing live boundaries; no bundled linker; over-claimed enforcement; revocation mid-step) | `linker-unavailable` where applicable | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | `native.execution-not-authorized` |
| explicit Config2/CLI workspace root without a language marker; explicit root violating the shared path grammar; explicit root at or below an admitted boundary (nested repository/project, custody-excluded directory) | | `request-rejected` (2) | `CONFIG.INVALID` | `native.explicit-root-without-marker` (missing marker); `PROJECT.EXPLICIT_PATH_INVALID` (grammar or boundary crossing) |
| admitted boundary inventory whose pruned trees do not equal the ones derived from the marker inventory (not produced by security over this inventory) | | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | `PROJECT.DISCOVERY_INVENTORY_MISMATCH` |
| capability/identity mismatch at HelloAck; OpenUniverse before negotiation; coverage bijection or RC-2 precondition mismatch; **subject-scope commitment, coverage key or examined-partition mismatch at the producer boundary** (§4.1a: `native.subject-scope-commitment-mismatch`, `native.coverage-key-scope-mismatch:<field>`, `native.examined-universe-commitment-mismatch`, `native.examined-universe-subject-count-mismatch`, `native.coverage-entry-key-mismatch`); a `view2` naming a `coverage2` that was never admitted at that boundary or whose subject scope is outside the view (`native.coverage-not-admitted-at-producer-boundary`, `native.coverage-subject-scope-outside-view`); **worker fault** (process fault, ProviderFault, crash) | | `operational-failed` (4) | `PROVIDER.PROTOCOL_VIOLATION` | operational record |
| native context whose stdlib/rust-dev-llvm/tool closure is unretained, recomputes to a different identity, has the wrong kind, or whose suffix, component, `libSelection`, tool-member or compiler-version join fails (§2.3, §2.4: `native.native-context-closure-unretained`, `native.native-context-closure-identity-mismatch`, `native.native-context-closure-kind-mismatch`, `native.native-context-stdlib-tree-mismatch`, `native.native-context-lib-not-retained`, `native.native-context-tool-not-in-closure`, `native.native-context-compiler-version-not-from-manifest`); a universe bound to a context this host did not mint or to the other language's record (`native.universe-context-binding-mismatch`, `native.native-context-language-mismatch`) | | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | request detail (before PlanId; no worker is spawned) |
| preparation bound exceeded | | `operational-failed` (4) | `HOST.IO_FAILURE` | `native.prepare-bound-exceeded` |
| ambient Cargo config in an ancestor; environment override present | | `operational-failed` (4) | `HOST.IO_FAILURE` | `native.ambient-cargo-config` |
| more than 4096 first-party workspace unit directories (`PROJECT.WORKSPACE_UNIT_LIMIT`, with `unitCount`/`limit`; installed dependencies never count) / too many recognizers | | `request-rejected` (2) | `REQUEST.UNSATISFIABLE` | request detail |
| shared scope array exceeds its bound (workspaceRoots1024, pathPrefixes/excludedPathPrefixes65536), without truncation | | `request-rejected` (2) | `REQUEST.UNSATISFIABLE` | `PROJECT.SCOPE_LIMIT`, subject `field:count>limit` |
| unrecognized framework | | none (disclosure) | none | disclosure |

Exit 0 is never used for any row above; an unmapped detail is a model error, not
a silent success (`d9-unknown-detail-never-exit-zero`). Cancellation follows D9.

**Clones ownership disclosure is typed, not null (CB3-MUST-5).** §11's
`scopeVersusEnumeration` requires that a clones scope which cannot determine a
body dialect mint no body identity, report the incompleteness in its Coverage,
and leave the predicate and seal indeterminate. `NativeCause` had no member for
any of the three ownership states the `languageVersionBinding` selection law
refuses on, so that mandated disclosure had no expressible value and every
implementation would have invented its own pairing — or emitted
`nativeCause: null`, which records that a disclosure was owed and not made
rather than making it. The closed pairing is now:
`BODY_LANGUAGE_OWNERSHIP_REQUIRED` → `body-language-ownership-missing`;
`BODY_LANGUAGE_OWNER_UNENUMERATED` → `body-language-owner-unenumerated`;
`BODY_LANGUAGE_OWNER_AMBIGUOUS` → `body-language-owner-ambiguous`; each with
deficiency `input-closure-incomplete` and the `indeterminate` class above, so
the CLI/JSON/SARIF/HTML/agent parity fields carry one vocabulary.

**The vocabulary alone did not close this, and an earlier revision wrongly said
it did.** A retained-Run counterexample showed the concrete bypass: the Coverage
prerequisite asked only whether `coverage` was `complete` and whether
`deficiency` was non-null, so under partial ownership a Coverage carrying an
*unrelated* `budget-exhausted` with `nativeCause: null` was admitted, as was
`input-closure-incomplete` with a null cause. A cause vocabulary that nothing
derives and nothing compares leaves the disclosure optional in practice.

The pair is therefore **derived and enforced**, not merely expressible. The
owning native unit derives the owed `(deficiency, nativeCause)` from the
**committed ownership record** and **this scope's subjects**, in the selection
law's own order: no committed ownership; then `enumeration: partial`, decided
before any row is read so incomplete discovery can never act as an implicit
edition selection; then a subject of this scope whose *selected* owners disagree
on effective edition. Run closure re-derives the same pair independently and
refuses a mismatch, so the claim cannot define its own correctness. Four
distinct refusals keep the faults separable — a false `complete`
(`COVERAGE_DIALECT_PREREQUISITE`), an undisclosed null deficiency
(`…_UNDISCLOSED`), a wrong deficiency (`COVERAGE_DIALECT_DEFICIENCY_MISMATCH`)
and a wrong or null cause (`COVERAGE_DIALECT_CAUSE_MISMATCH`).

`examinedExhaustive` and `resolutionCompleteness.state` stay **different
claims**: a host may have examined its committed partition exhaustively while
resolution is `not-applicable` entirely, and neither implies the other or the
ownership disclosure.

A **deliberately excluded** selection is not an unfinished enumeration and owes
no disclosure. The owner exists, enumeration is complete, and the path is
compiled only by targets outside the selection: the host examined that subject
and correctly produced no fact, so `complete` remains lawful. A selection is
committed in the universe identity and visible to every consumer; unfinished
enumeration leaves no such trace. Collapsing the two would either hide a real
gap or slander a lawful selection. The remaining
selection-law refusals get no cause and that is deliberate:
`BODY_LANGUAGE_OWNER_NOT_COMPILED` and `BODY_LANGUAGE_OWNER_NOT_SELECTED` are
per-body refusals §11 states are compatible with `coverage: complete`, and
`BODY_LANGUAGE_DIALECT_ABSENT`/`BODY_LANGUAGE_DIALECT_AMBIGUOUS` refuse at the
universe before any Coverage entry exists. The body refusal itself is unchanged:
a producer that cannot mint a body identity still must not pretend to, and an
empty clones Coverage remains indeterminate rather than a finding of no clones.

**Fault law (R7; `stage_authority`, `run_termination`, `StageAuthorityV1`).**
A worker that faults — process fault, protocol violation, `ProviderFault` frame,
crash — contributes **no facts, no Coverage entries and no Run**: its diagnostics
(stderr, fault detail) are an operational record only and can never mint an
authoritative fact; the invocation is `operational-failed` (4)
`PROVIDER.PROTOCOL_VIOLATION`; cancellation is `interrupted` (130) with the same
no-facts rule (`fault-worker-diagnostics-never-mint-facts-or-run`). By contrast a
stage that terminates cleanly over **successfully admitted but incomplete inputs**
(missing crate, generated file unavailable, unresolved edges) yields admitted
facts and typed Coverage, seals an **authoritative** Run, and terminates
`indeterminate` (3) with the deficiency as typed detail in the coverage2 record
(`admitted-incomplete-inputs-yield-authoritative-indeterminate-3`).
`BudgetExhausted` and `Unavailable` are clean typed terminals: facts before the
terminal are admitted and the Run is authoritative with the stage `partial`.

---

## 11. Identity domains authored here

All are `H(domain, descriptor)` under the foundation recipe, hex-encoded as
`sha256:<64 hex>` where a `Sha256Text` is required:
`native.semantic-universe.rust.v2`, `native.semantic-universe.typescript.v2`,
**`native.semantic-universe.syntax.v2`**, `native.context.rust.v2`,
`native.context.typescript.v2`, **`native.context.syntax.v2`**,
`native.dependency-source-set.v1`,
`native.dependency-file-manifest.v1`, `native.unified-features.rust.v1`,
`native.cargo-config-projection.v2` (over `CargoConfigProjectionV2`, §3.3 — the
domain `rust-v2.configProjectionSha256` carries the suffix of),
`native.prepared-output-set.v3`, `native.authorized-execution.v2`,
`native.clone-suppression.v1`, `native.framework-recognition.v1`,
`native.workspace-unit.v1`, `native.entry-points.v1`,
`native.source-unit-ownership.v1` (over `SourceUnitOwnershipV1`, §2.1 — the
committed source-path to compilation-target relation, its closed target table and
its explicit selection), `native.compilation-unit.v1` (over `UnitIdentityV1`, the
published four-field preimage a `unitId` is `H` of), and the two native import
payload domains `native.import-payload.{dependency-source,prepared-output}.v1`
(registry spelling, §7.1). Runtime/test/history payload domains are the workflow
owner's; the former native `runtime-coverage`/`test-results`/`history` payload
domains are withdrawn (their records are adapter input shapes, never payloads).
Import identity itself is the foundation `import` domain (`import2:`), not a
native domain; the import wrapper's auxiliary digests are raw SHA-256 records,
not domains. `subjectScopeCommitment` adds **no** native domain: it is the foundation
`subject-scope` identity in a different textual form (§4.1a).

**Three admitted textual forms of one digest, and when each is required.** They are not
alternative recipes; the preimage and the `H` frame are always the foundation's.

| Form | Where it is required | Example |
|---|---|---|
| foundation typed prefix `<prefix>:<64 hex>` | any foundation identity field: `snapshot2:`, `plan2:`, `closure2:`, `scope2:`, `coverage2:`, `import2:` | `scope2:2c5f…` |
| native `Sha256Text` `sha256:<64 hex>` | any native record field typed `Sha256Text`, where the foundation domain is not carried in-band: `nativeContextId`, `dependencySourceSetId`, `unifiedFeaturesId`, `preparedOutputSetId`, `CoverageKeyV2.subjectScopeCommitment` | `sha256:2c5f…` |
| bare `DigestHex` (64 hex, no prefix) | raw SHA-256 digests and 64-hex **suffixes of a typed foundation identity**: `plan.nativeContextDigests`, `sourceUniverse`/`targetUniverse`, `configProjectionSha256`, `typescriptStdlibMerkleRoot`, `rustcDevLlvmDigest` | `2c5f…` |

A suffix field is bare precisely because its typed prefix belongs to the foundation identity
it was taken from; admission recovers that identity by re-prefixing and requires a retained
closure to match (§2.3, §2.4). The textual form is a spelling, not an annotation:
which recipe a field carries is what that field's own `x-opensip-digest`
annotation says, and no prefix implies one.

**Language-version binding for FACT-IDENTITY body frames.** A `clones` relation
payload's `bodyIdentity` is framed with a `languageId` and a `languageVersion`
that the inherited `fact-identity-policy.v2` requires to be "canonical identity
bytes supplied by ResolvedInputs/PlanId, not a human display string", for "the
provider interpreting the body span". The identity that satisfies it is the
**compiler**, and it is already committed: a universe's own `nativeContextId` —
a reference Run closure already requires to be Plan-selected — reaches the
admitted retained context, whose `toolchain` carries `rustcVersion` and
`rustCommitHash` here, and `compilerName`, `compilerVersion` and
`compilerPackageDigest` for TypeScript. §2.3's admission already refuses
`native.native-context-compiler-version-not-from-manifest` unless that version
equals the admitted tool closure's `semanticVersion`, for both languages, so the
binding inherits a real chain from a retained closure manifest rather than
copying a display string. **Following an existing admitted reference needs no new
universe field**, and none was added.

The binding lives in the universe domain rows at
`foundation/identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/*/languageVersionBinding`,
and it names, per language, the exact source path of every field of the closed
`body-language-version` record plus each **excluded** field with its reason. The
boundary is: what identifies the component that **interprets the body span**, and
the selected source **dialect**. Not the operational platform (`targetTriple`,
`hostTriple`), not the resolution environment (`sysrootDigest`,
`standardLibraryComponentDigests`, `libSelection`), not the code-generation
backend (`rustcDevLlvmDigest`), not build or dependency tooling (`cargoVersion`,
`resolverVersion`), not paths (`crateRootPaths`), and not option synthesis
(`languageMode`, `synthesizerVersion`), which describes how a program was
assembled rather than which language read the body.

`edition` is a map from crate **name** to year, so it is the *selected value*
that is the dialect, never the map: a body identity that varied with unrelated
crates would be neither meaningful nor representable. When the map's distinct
value set has exactly one member — the ordinary case, including a large
single-edition workspace — that member is the dialect of every body and no owner
selection arises. When it has more than one, the **owning compilation unit
decides**.

More precisely, the **compilation target** decides, not the package. Cargo
documents an `edition` on a target that **defaults to** `package.edition` when
absent — `cargo metadata` lists `targets[].edition` and states the package value
is a default individual targets may differ from, and the `[[bin]]`/`[lib]`
`edition` field, though deprecated, is still documented. So *source → package →
package edition* misses a supported override, and a universe whose package
defaults **all agree** can still contain a target that does not. There is
therefore **no single-edition fast path**: a `clones` fact over a Rust universe
requires the committed ownership relation whatever the package map looks like,
and a null `sourceUnitOwnershipId` admits no clone.

`SourceUnitOwnershipV1` is that relation **and the explicit selection**, and
`RustUniverseV2ResolvedInputs.sourceUnitOwnershipId` is the `h-identity` of
`native.source-unit-ownership.v1` that carries it — required and nullable,
exactly as `preparedOutputSetId` is. It holds three things:

- `units` — the **closed table of compilation targets**:
  `{unitId, markerPath, crateName, targetKind, targetName, targetEdition}`.
  `targetEdition` is the target's own edition when it sets one and `null` when it
  takes the package default, so the two committed places can never contradict.
- `selectedUnitIds` — the **explicit analysis scope**, non-empty, every member a
  declared `unitId`.
- `ownership` — the pure relation `{path, unitId}`, carrying no edition and no
  metadata, so it cannot contradict the table.

`unitId` is **derived, never declared**:

```
unitId = H(native.compilation-unit.v1,
           UnitIdentityV1{schemaVersion: 1, markerPath, targetKind, targetName})
```

carried as `sha256:<64 hex>`, with **`derived` retention**: nothing separate is
retained, because the preimage *is* the unit row, and admission re-derives and
compares (`sourceUnitOwnership.unitId`). **This is not an opaque digest** — the
preimage record, its domain, its codec and its selector are all published here,
so any consumer rebuilds it from the row that carries it.

An earlier draft joined the fields with delimiters,
`markerPath#targetKind:targetName`. **That is withdrawn.** It was injective only
by excluding `#` from `markerPath`, and a `#` in a repository directory is
admissible under the canonical repository-path contract — so the recipe narrowed
admitted paths in order to make a delimiter work, which is the wrong trade. `H`
needs no such restriction, is fixed width for every admitted path and name
length, and a marker under a `#`-containing directory closes a complete Run.

`units` is strictly unique by `unitId`, and `unitId` is a function of the
metadata, so **two contradictory rows for one purported unit are a refusal, never
two units that differ by accident**, and a selection or ownership row naming an
undeclared `unitId` is an unbound caller label and inadmissible.

`markerPath` is the inventoried manifest that declares the target — the same
vocabulary `WorkspaceUnitV2` already uses, under the ordinary canonical
repository-path admission with no added restriction. **`WorkspaceUnitV2` and
`UnitMembershipV1` cannot supply this binding**, and that is a granularity
statement rather than an oversight: they identify *workspace* units
(`cargo-package`, `cargo-workspace`), while one package holds several targets
that may carry different editions. Naming the marker joins my targets to that
existing discovery vocabulary instead of competing with it.

**Because the selection is committed inside the record whose `h-identity` the
universe names, a different selection is a different record, a different identity
and therefore a different `sourceUniverse`.** That is what makes the required case
representable: one physical source path compiled by two targets at two editions is
validly analysed **under each selection, one at a time**, each with its own
correct dialect and its own body identity, and **no relation payload changed** to
make it so.

Selection is exact and total, and the order of decision is fixed so each step has
its own cause. No committed ownership refuses. `enumeration: partial` refuses
**before any row is read**. Rows are those whose `path` **equals** the enclosing
fact's anchor path — never a prefix, never a nearest directory, never a first
match — and no row at all refuses as not-compiled. Rows are then restricted to
`selectedUnitIds`, and a path compiled only by **unselected** targets refuses as
not-selected rather than borrowing an out-of-scope edition. Selected owners whose
effective editions **agree** are admissible — the ordinary shared-file and
lib-plus-test-target case. Selected owners that **disagree** are an ambiguous
unselected request and refuse. §2.1's retained-input admission independently
requires every marker and owned path to be a source of the same snapshot, every
selection and ownership row to name a declared unit, and every deferring unit to
name a crate the same `edition` map declares.

**Selected scope is not incomplete enumeration.** A selection says these targets
*are* the analysis, so an owner outside them is deliberately out of scope; it is
committed in the identity, so every consumer sees it and it changes the universe.
`partial` says the producer did not finish, so an owner *inside* the selected
scope may exist that is not listed and could contradict a listed one — a gap in
knowledge, invisible as a selection, admitting no dialect at all. Silently
omitting a conflicting owner from the table is not a selection either: an
omission leaves no trace, whereas a selection is part of the universe identity.
Partial evidence stays useful under the existing law rather than voiding a Run —
the clones scope mints no body identity, its Coverage carries the incompleteness,
and the predicate and seal are indeterminate.

The consequence is the one that matters: an **ordinary mixed-edition workspace
has a representable valid form**. Each path is owned by units of one edition, so
bodies of *both* editions are admissible in the *same* universe, each carrying
its own dialect. Only a path genuinely compiled under two different editions
refuses, which is a real ambiguity in the input rather than a gap in the law.
This record states what a producer claims it enumerated; it admits no compiler,
measures no build and qualifies no enumerator.

Exact typed admission precedes every schema check and is imported, not
reimplemented: `canonical.parse` refuses `1.0`, `1e0`, `-0`, non-finite tokens,
duplicate keys and lone surrogates; `canonical.validate` uses the exact-const /
exact-enum / exact-integer validator so `true` is never an integer and `1.0` is
never `1` (`float-spelled-integer-refused`). Every native record schema is closed
(`additionalProperties:false`, checked by the report's `openObjects=[]`).

---

## 12. Reference evidence

`native/native-cases.v2.json` (132 cases) carries hand-authored expected outcomes; every
observation a provider, adapter or OS would make is marked as a trusted observation input.
`native/check_native_evidence.v2.py` verifies every consumed source pin in
`native/source-pins.v2.json` (including the foundation serializer and schemas and the three
workflow schema documents), validates fixtures under exact typed admission (native records
against the closed bundle, 100 definitions; workflow payloads and wrapper records against
the pinned workflow documents through a registry closure, no network), runs the model,
validates the matrix, and writes `native/native-evidence-report.v2.json`.
The identity vectors pin a hand-spelled canonical preimage and use `hashlib` as
the independent oracle; `foundationIdentityVector` does the same for a foundation-domain
identity, so the `subjectScopeCommitment` recipe (§4.1a) is checked against `hashlib`
rather than against the model that produced it. Coverage is reported per item F1–F12,
R1–R7, the post-reset items `PR-MUST-3`, `PR-SHOULD-4`, `PR2-P3`, `PR2-P22`, and the
blind-consumer items `CB-M1`, `CB-M2`, `CB-A1`, `CB-A2`.

Nothing here executes a compiler, a provider, Cargo, or a repository. Product
behavior on any platform remains qualification work.

---

## 13. Joins (closed; current spellings, no future owner choices)

- **H-1 (foundation, DR-103) — closed.** The security/foundation owners decide the
  repository boundary (`vcs-default`/`cwd-default`/`config`, nested config as a
  deliberate boundary) and trust; inside it this
  contract's `discover_units`/`assign_membership` (§1.4) produce `WorkspaceUnitV2`
  and `UnitMembershipV1`, and `unit_scope_descriptor` emits the foundation
  `scope-descriptor` whose raw digest is the shared `scopeDigest`. Config2
  `discovery` fields are consumed exactly as §1.4 states. Both instruments
  consume the one shared discovery rule
  (`docs/coop/design-corrections/discovery-defaults.py`: pruned trees by
  segment, first-party cap, `.` sentinel normalization, the boundary prefix
  rule `classify_boundary` and the inventory conversion
  `boundary_inventory_from_provenance`); a host composition
  calls `enumerate_units(markerRelPaths)` and `classify_path(relPath,
  cargoRoots)` from it rather than restating either, and obtains the boundary
  inventory only from security (U-8).
- **H-8 (security S3, post-reset v2 N-1) — closed.** The authority boundary is
  security's decision; this instrument consumes its `AdmittedBoundaryInventoryV1`
  exactly as U-8 states, yields security's unit set over the same marker
  inventory, and refuses an inventory that was not produced over that inventory.
  **The integration join is implemented, not owed.** `integration-host-model.py`
  `admit_repository_discovery` runs security `discovery` → `DD.boundary_inventory_from_provenance`
  → `N.discover_units(markers, explicit, boundaries)` → `assign_membership` →
  `unit_scope_descriptor`, and `check-integration.py` asserts it on a
  nested-repository/nested-project fixture (`host-nested-boundaries-admitted-once`,
  `-no-native-units`, `-no-source-capture`, `-plan-visible`,
  `host-native-inventory-substitution-refused`,
  `host-launch-inside-nested-config-selects-that-project`), beside the equal-unit-roots and
  equal-pruned-trees checks (`security-native-shared-unit-roots`,
  `security-native-shared-pruned-trees`) and the security sweep
  `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`. Nothing
  is open here. Those files are Codex-owned, so this unit records the join and does not
  restate it.
- **H-2 (security S10) — closed.** Principal class `repository-code` is registered
  by S10 with execution classes `build-script | proc-macro | test-runner`; its
  semantic-grant kind is `trusted-repository-code` and its workflow spelling is
  `P-TRUSTED-REPO` (§5.1, schema constants). Enforcement values in
  `AuthorizedExecutionV2.effects` are copied from the pinned
  `permission-truth-tables.v9.json` and must equal S10's entries; the revocation
  clock is consulted `before-each-owner`; cancellation is `process-group-kill`.
  If an enforced primitive is later measured on a platform, only that value changes.
- **H-3 (host D9) — closed.** No new deficiency enum members and no new reason
  codes are requested. Native deficiencies are typed detail inside the coverage2
  record named by the termination's `coverageId`; the D9 codes used are exactly
  the existing `VERDICT.INDETERMINATE`, `COVERAGE.PROVIDER_UNAVAILABLE`,
  `COVERAGE.BUDGET_EXHAUSTED`, `REQUEST.PRECONDITION_FAILED`, `CONFIG.INVALID`,
  `REQUEST.UNSATISFIABLE`, `PROVIDER.PROTOCOL_VIOLATION`, `HOST.IO_FAILURE` (§10).
- **H-4 (host error codes) — closed.** Withdrawn: preparation bounds and ambient
  config are `HOST.IO_FAILURE` with the native detail strings; no
  `NATIVE.*` codes exist.
- **H-5 (workflow) — closed.** Import payloads: one canonical schema document per
  kind (§7.1); wrapper digests: the workflow `ImportWrapperV2` raw-SHA recipe
  (§7.2); correspondence/mapping: the workflow `SourceCorrespondence` +
  `SourceMappingV1` (§7.3). `native.prepare` and import are workflow operational
  steps with the workflow's CLI spelling and receipts; inert prepared/imported
  blobs are host CAS objects under the storage custody rules (§1.4). The workflow
  repair prerequisites consume `ClosedWorldV2.deadCodeRepairEligible` and
  `affected_targets` as stated in §4.5; HTML/agent projections render
  `resolutionCompleteness` and disclosures verbatim.
- **H-6 (Codex identity) — unchanged.** The reference model imports Codex's
  serializer and `import2` identifier by file; if those bytes change, this unit
  re-pins and re-runs; no native serializer exists to diverge.
- **Formerly recorded conflicts — both resolved in current bytes:** (a) §7.4 —
  the workflow `build_import` now uses raw SHA-256 auxiliary digests and one
  payload domain per kind (verified by the integration wrapper-equality checks);
  (b) the security S10 text and the security model's S10 section comment now
  name `AuthorizedExecutionV2` (same effect values). No conflict is open.
- **H-7 (security S10, post-reset SHOULD-2) — closed.** Grant admission is
  operational and precedes any Plan; the principals a consuming analysis must
  project for `preparedResolution=host-prepared` are exactly
  `semantic_projection_for_grants(consumed preparation grants)`, checked at
  Plan admission by `admit_plan_execution_projection`; `imported-inert`
  projects none (§5.1 unchanged); a test-runner grant is projected by nothing.
- **Disagreement statement:** none with the coordinating proposals. One
  retained refinement: the joint text says an incomplete Rust universe "produces
  Coverage provider-unavailable"; this contract types it
  `input-closure-incomplete` (the remedy differs) and carries it as typed detail
  under the existing `VERDICT.INDETERMINATE`, which changes no vocabulary owned by
  another unit.

## 14. Host composition corrections (mixed authorship; independent Claude review pending)

`AuthorizedExecutionV2` is a preparation preflight descriptor, not a security
admission result. `opensip native prepare --authorization PATH --grant-set PATH`
selects its retained canonical bytes and operational grant set. PATH inputs receive
ordinary user-input custody checks. The invocation contains a `native-preparation`
step with `authorizationDescriptorDigest` (raw SHA-256) and `securityGrantSetRef`.
The host verifies those preimages before admission. A completed step returns an
execution receipt and one admitted prepared import, never a Run. Execution is never
an automatic retry; cancellation kills the admitted process group and retains an
indeterminate journal if completion cannot be established. A new explicit request
is required to repeat interrupted execution. Inspection of the journal executes
nothing. Publication of prepared evidence requires complete output admission and
current source correspondence; an execution receipt alone does not supply evidence.

Each preparation owner has an explicit `source` (snapshot-member or
dependency-closure-member) and receives one class-specific RepoExecutionGrantV2.
The preparation bound is 4096 owners; this composes as up to 4096 single-owner
grants and does not enlarge security's 64-owner per-grant bound. Each grant binds
the actual host-selected argv/runner, class, project, snapshot, platform, tool and
dependency closures, consent and effect disclosure. Every grant is admitted through
security's complete schema and decision model before any spawn, with live boundaries
rechecked during execution. Native preflight success alone cannot authorize a spawn.

An owner's semantic source preimage is the canonical singleton array of the closed
security row `{ownerKey,source,ownerFileManifestSha256}`. Its raw SHA-256 is
ownerSourceDigest in both the semantic principal and that owner's operational
grant. The preimage is retained. Multi-owner security grants use the same record
array sorted by unique ownerKey. `securityGrantSetRef` is
`security.repo-execution-grants.v2:` plus H over
`{schemaVersion:2,grantRefs:sortedUniqueV2GrantRefs}`. The actual per-grant reference
is `security.repo-execution-grant.v2:` plus H of the admitted grant. These operational
references and consent are excluded from the semantic Plan.

Native-context schema 2's `typescriptStdlibMerkleRoot` and `rustcDevLlvmDigest`
join foundation's exact stdlib/rust-dev-llvm closure2 suffix recipes, with complete
admitted descriptors and trees retained. Their exact locations are
`TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot` (§2.4) and
`NativeContextV2.toolchain.rustcDevLlvmDigest` (§2.3), each inside its language's
toolchain-identity record; `admit_native_context` performs the re-prefix-and-recompute join
against the retained closure. Manifest digests hash the security metadata
body encoding, excluding its signature envelope. Subject discriminators use the
canonical declaration-signature string-array preimage from identity §3; bodies,
positions and encounter-order suffixes are excluded, and duplicate signatures in a
collision class refuse correspondence. The reference adapter exercises this hash
join; actual compiler token projection remains a named native qualification task.

The discovery instrument can enumerate 4096 first-party units (installed
dependency manifests are pruned first and never count, §1.4 U-4a/U-7), while an
admitted foundation scope permits at most 1024 selected workspace roots. The
effective scope limit is 1024; overflow refuses without truncation and asks for a
narrower explicit scope. Discovery's larger diagnostic population does not bypass
the analysis input bound. A workspace root `.` names the already admitted project
root under the shared `normalize_explicit_root` (§1.4).

Near-clone groups are connected components of threshold-passing edges.
`matchedEdges` exposes the actual endpoint IDs and each Jaccard score;
`scoreMeaning=minimum-member-best-neighbor` describes the group summary score.
It does not claim that every pair in the component passes the threshold. Normal
canonical record-size and work budgets still apply; exceeding them is explicit
incomplete analysis, never an undisclosed truncation. Reviewed candidate identities
follow a stable source fingerprint within a project, separately from the current
Run, under the workflow review contract.

Cross-unit reference evidence: `docs/coop/design-corrections/integration-host-model.py`
and `check-integration.py`. The model composes actual reference admissions over
synthetic TCB inputs; it does not execute repository code or measure confinement.

Public details for the shared cap and explicit-root grammar are PROJECT.WORKSPACE_UNIT_LIMIT and PROJECT.EXPLICIT_PATH_INVALID. The pure instrument retains native.too-many-units and native.explicit-root-grammar only as internal aliases; the host normalizes them through public-detail-registry.v1.json, and the public schema rejects those aliases. The internal capability table key provider-unavailable/capability-missing emits native.capability-unavailable publicly.

The four repository-code child-process effect selections in §5 are consistent with the accepted permission-truth-tables.v9 head. The v7→v9 changes concern metadata/recording and the host-under-instruction network recital; the permission table rows supplying the four selections are unchanged. The product still declares these as its own supported-platform design selections, not measured confinement or an extension of preview qualification.


A scope array that exceeds the shared foundation schema bound refuses REQUEST.UNSATISFIABLE (request-rejected, exit2), public detail PROJECT.SCOPE_LIMIT and subject `field:count>limit`; it is never truncated. workspaceRoots has limit1024 (distinct roots after co-located unit deduplication), and pathPrefixes/excludedPathPrefixes each65536. Thus1025..4096 valid discovered unit roots produce this typed scope refusal, while more than4096 first-party unit directories produce PROJECT.WORKSPACE_UNIT_LIMIT earlier. The public code is shared across host/native scope admission; callers must narrow explicit selection. Native ScopeRefusal retains detail, D9 and observed bound fields for the host's closed termination projection.

The standalone boundary-crossing key native.explicit-root-crosses-boundary is an internal alias of PROJECT.EXPLICIT_PATH_INVALID, the code security emits before native on the operational path. native.boundary-inventory-mismatch is an internal alias of PROJECT.DISCOVERY_INVENTORY_MISMATCH. The latter public condition is emitted by the actual host when its native marker/file inventory disagrees with the security discovery inventory (REQUEST.PRECONDITION_FAILED, exit2), including before native is invoked. Neither internal spelling is a public enum value.
