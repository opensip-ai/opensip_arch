# Blind consumer-B reconstruction — OpenSIP DR-011-R10 (consumer-b.v9)

**Verdict: CHANGES_REQUIRED**

Four MUST-class and three SHOULD-class design gaps remain, all of them in one
place: the **pure evaluator's own inputs**. Everything else in this kit
reconstructed cleanly and mechanically. I built an independent encoder, identity
helper, native-admission model, closure checker, provider state machine and
evaluator from the prose alone, and closed **15 complete positive Runs**, each of
which additionally passed **semantic proof replay** against its retained claim,
plus 48 retained-closure negatives, 142 admission/native/workflow vectors and 9
provider traces, with **0 required-control failures**.

The verdict is CHANGES_REQUIRED and not ACCEPT-RECONSTRUCTABLE because the
declarative policy DSL is admissible in shapes the retained Run cannot decide:
I could not derive the subject enumeration, the field-filter projection, an
imported-evidence atom's witness, or the waiver's effect on the sealed verdict
without inventing public semantics. Those inventions change `proof2`, `seal2`
and `run2` — the product's own independent-replay property — so they are not
implementation freedom.

---

## 1. Input custody

All 46 files in `consumer-input-manifest.json` verified by SHA-256 and byte
length; no extra file under `docs/`, none missing.
Manifest bytes: `d7af863160ac0d5175db566a127337d40f062a155e9bb3844404793c784fc031`.

The manifest declares `parentSubjectSha256` =
`360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`. **That value
is not verifiable from this kit** — the kit is a declared subset, and no
composition rule for the parent digest is supplied. I record the claim and do
not assert it.

No file outside `consumer-b.v9/subject` was read. No author model, fixture,
golden, case file, review or other `/tmp/opensip-design-corrections` directory
was opened. All code and output is under `consumer-b.v9/output`.

`docs/v2/contracts/product-v1/README.md` is explicit that the readiness register
and correction record grant standing and are deliberately excluded; I needed
neither, and I treated every historical review narrative inside the inherited
documents (post-reset MUST-3, CB3-MUST-*, CB4-*, CB8-*, PR2-*) as provenance
only, never as acceptance.

---

## 2. What I built, and what is executed versus assumed

`ref/` (~3,000 lines, all written here from prose):

| Module | Reconstructs |
|---|---|
| `canon.py` | raw lexical admission, `C`, `H` + frame, `x-opensip-order`, CVE1, the FACT-IDENTITY body frame |
| `kit.py` | pinned document loader, `$ref` closure, the normative registries |
| `store.py` | the one content-addressed store and the typed object table |
| `native.py` | `admit_native_context`, `bind_*_universe`, `body-language-version` derivation, `lib_name_fold` |
| `closure.py` | retained Run closure: identities, schemas, joins, relation registry, Coverage laws, body-identity join |
| `evaluator.py` | the published predicate table, node addressing, witnesses, verdict |
| `protocol.py` | the Rust major-3 state law from `protocol3-transitions.v1.json` |
| `workflow.py` | default capability selection, public route derivation, bounded subjects, envelopes, mutation keys, pinned purge |
| `build/scenarios/assemble` + `run_*.py` | the synthetic repositories and Run graphs |

**Executed here** (real computation over real bytes): every canonical encoding,
every `H`/CVE1/body-identity digest, every schema validation against the pinned
documents, the whole retained closure, every negative refusal, the complete
evaluator replay of every positive Run, and every provider trace.

**Assumptions about a future host** (stated, never executed): every OS, ACL,
filesystem, compiler, Cargo, provider, SQLite, fsync, signature and clock
observation is a *synthetic trusted observation* supplied by my builders. Closure
tree contents, stdlib inventories, `node_modules` layouts, edition ownership,
grammar bundles and dependency manifests are declarations, not measurements. None
of this is native enforcement proof, and nothing here qualifies a platform, a
compiler, a normalizer, a renderer or a ledger.

Re-run everything from scratch:

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v9/output/ref/run_all.py
```

It re-verifies the manifest, recomputes every identity, re-closes and re-replays
every Run, writes `vectors/` and **exits non-zero if any required control fails**.
Current run: `requiredControlFailures: 0`.

---

## 3. Reconstruction 1 — discovery to durable receipt

### The chain, with its owner at each link

```
repository + explicit inputs
  └─ security S3 discovery (custody, walk rule, nested-config boundary)   [security]
      └─ AdmittedBoundaryInventoryV1 ──> native S1.4 U-1..U-8 unit discovery [native]
          └─ Config2 resolution, all five sections present                 [admission S1.1]
              └─ snapshot2 = H(snapshot, {ProjectId, sourceInventory,
                                 resolvedConfigDigest, scopeDigest, vcsDigest}) [identity]
                  └─ closures ─> native context ─> semantic universe       [native S2, S11]
                      └─ plan2 (capability manifest, spec, contexts, policy,
                                waivers, scope, budget, semantic grant)     [identity S3]
                          └─ subject-scope ─> commitment ─> CoverageResultV3
                              ─> coverage2 ─> view2                        [native S4.1a]
                              └─ fact2 (relation payload + anchors)        [identity S3]
                                  └─ proof2 (predicate proofs + witnesses) [identity S4]
                                      └─ evidence2 ─> seal2 ─> run2        [identity S3]
                                          └─ commit receipt + availability [identity S5]
```

**Semantic identity versus operational authority.** `snapshot2 … run2` are
`H(domain, C(descriptor))` over closed records. `RequestId`, `ExecutionId`, wall
clocks, PIDs, credentials, nonces, receipts and output destinations are
operational and are *not fields of any semantic descriptor* — I verified this by
schema: adding `requestId`, `executionId`, `committedAt` or `pid` to a
`snapshot` descriptor refuses on `additionalProperties: false`
(vectors `A3-V2-*`). Two attempts over identical semantic inputs mint the same
`run2` and remain separately auditable through their own `ExecutionId`.

**Mutation versus analysis steps.** Only `analysis` and `verify` seal or link a
`run2`; the other eleven step kinds never mint one, and the schema enforces
`retryPolicy: none` on the seven effecting kinds. I validated complete
`InvocationRecordV1` + `CommandEnvelope` documents for each trace.

### The derivation is acyclic — checked by construction

`native-evidence` §4.1a asserts *closures → context → universe → scope2 →
commitment → Coverage payload → coverage2 → view2*, and identity §3 asserts
proof excludes EvidenceId and RunId. I did not take either on trust: my builders
mint in exactly that order with no back-reference, and the schemas confirm that
`plan` names no execution-plan, `proof-bundle` names no evidence or run, and
`policy-derivation`/`execution-plan` point *at* the Plan. No cycle exists.

### Provider message sequencing, derived independently

I implemented the 34-row table, the `*ANY`/`*PRE_COMPLETE`/`*PROCESS_FAULT`
wildcards, the pre-match law (FAULT absorbing → post-terminal → process fault),
first-match-wins, the guard law, the four state updates, the stage-dependent
`ANALYZING_OR_READY_COMPLETE` resolution and the terminal law. I also
**independently checked the published pairwise-disjointness claim** — it holds,
so first-match resolves no ambiguity today.

| Trace | Result |
|---|---|
| T1 complete, one stage | `DONE`, terminal `complete`, `P3-01 02 03 04 05 06 07 10 20 22 23 24 27 31 32` |
| T2 complete, dependency custody, **two stages** | `DONE`, `stagesCompleted=2`, `…08 11 12 13 15 20 22 23 24 23 24 27 31 32` |
| T3 `Unavailable` before Analyze | `DONE`, terminal `unavailable`, `…P3-21 31 32` |
| T4 cancellation mid-analysis | `DONE`, terminal `cancelled`, `…P3-29 30 31 32` |
| T5 **OpenUniverse before identity negotiation** | `FAULT` at `P3-34`, **`sourceBytesSent=false`** |
| T6 process death mid-stage | `FAULT` at `P3-33` |
| T7 post-terminal frame after `Complete` | `FAULT`, trace `post-terminal-frame`, terminal `complete` retained |
| T8 `BudgetExhausted` | `DONE`, terminal `budget-exhausted` |
| T9 `ProviderFault` mid-custody | `DONE`, terminal `provider-fault` |

**Identity negotiation before source disclosure is enforced structurally, not by
convention.** T5 is the discriminating trace: `P3-03`'s guard requires
`identityNegotiated: true`, which `HelloAck` sets only when all four identity
tokens are present, so `OpenUniverse` — the frame that carries `snapshot2` and
`plan2` — matches no row and the exchange faults with **no source byte sent**.
**Terminal process handling** is separate from the terminal frame: reaching a
terminal does not end the exchange; `zero-exit` then `eof` are still required to
reach `DONE`, and any other frame in between is `post-terminal-frame → FAULT`.
This is why identity §1's "complete protocol transaction **plus** successful
process exit and EOF before facts are admitted" is one law and not two.

Invocation-level traces (schema-validated envelopes, `D2-T1..T5`): complete
(`success`/0), unavailable (`indeterminate`/3, Run still authoritative),
cancellation before settle (`interrupted`/130 with the earlier step's RunId
retained), provider fault (`operational-failed`/4, **no facts, no Coverage, no
Run**, dependent render `skipped` with a typed `skipReason`), and a named
multi-step `audit` with different unit selections at different analysis steps.

---

## 4. Reconstruction 2 — capability manifest, native evidence, syntax modes

### Capability manifest: gates before encoding

I derived the record shape from `capability-manifest-domains.v2` `recordShape`
and the declared sort keys from `delivery.v4` `declaredSortKeys`, then applied
the four inherited gates **in order** and only then encoded:

`ADM-TYPE → ADM-CLOSED → ADM-DOMAIN → ADM-ORDER → CVE1 → SHA256("opensip.capability-manifest.v1" ‖ 00 ‖ committedBytes)`

Positive `A4-POS`: a manifest carrying the thirteenth relation
`unresolved-edge@observed` (only expressible because `RELATION-DOMAIN-V2`
extends the inherited twelve) plus an `AbsentCapability` row.
`capabilityManifestId = 093eb011c21385ff…`, recomputed from the committed bytes.

Eleven discriminating negatives, each flipping one thing:
boolean-as-integer and numeric-string (`ADM-TYPE`), an undeclared key
(`ADM-CLOSED`), an unregistered relation, **a rung of another relation**, an
unregistered platform (`ADM-DOMAIN`), unsorted providers and a **duplicate
treated as an ordering violation** (`RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL`),
non-NFC text, a float and a byte string (CVE1).

Three separations I checked rather than assumed: **CVE1 ≠ C** over the same
value; **`capabilityManifestId` ≠ `H("capability-manifest", X)`**; and CVE1's
NFC admission does not leak into `C`'s no-normalization profile.

I also independently confirmed the **declared mirror** claim: every ladder in
`RELATION-LADDER-DOMAIN-V2` equals the single authority
`relation-payload-schemas.v2#/x-opensip-relation-registry` **exactly and in
order** (this is the inversion the subject says was harmless only for
membership).

### Canonical raw-input admission, separate from encoding

Demonstrated separately, because an encoder cannot see a lexical fault. Thirteen
raw-byte refusals (`A1-N1..N13`): duplicate key, `1.0`, `1e0`, `NaN`, `-0`,
lone surrogate, `2^64`, `−2^63−1`, malformed UTF-8, raw C0 control, depth 33
(depth 32 admits — root counts as 1), and a descriptor over 4 MiB. Canonical
vectors cover UTF-8 byte key order across BMP and non-BMP, the escape set with
`/`, U+007F and U+2028 **unescaped**, shortest integers at both bounds, and
arrays kept in admitted order.

Frame admission: prefix, unregistered domain, wrong declared length, and a body
that is not `C` of its own parse each refuse; a raw payload offered where a frame
is required fails on the prefix, in both a unit vector and a full Run.

### The complete relation/rung applicability table, applied

Derived from the single ladder authority: **17 registered `(relation, rung)`
pairs**, of which exactly **5 are resolved** (`imports@resolved-target`,
`references@resolved-binding`, `calls@resolved-callee`, `types@checked`,
`reachability@from-resolved-calls`) and **12 are not**. RC-1 is decided by
*rung membership in the closed resolved set*, never by ladder length — which is
why one-rung `reachability` is never `not-applicable`.

Applied to retained scopes and Coverage **even where no fact is present**: the
`RUN-SYN-DATA` and `RUN-SYN-NONE` Runs carry fact-free `declares` and `clones`
scopes and are judged by RC-0/RC-1/RC-6 and the capability law regardless.

State-dependent count/class/attempt rules exercised as negatives: a
`not-applicable` entry claiming `attempted`, carrying edge classes, or carrying a
resolution state; RC-6 `complete` with `examinedExhaustive: false`; and the whole
deficiency/cause registry (`cause without deficiency`, `cause required`, `cause
must be null`, `relation not in scope`, `carrier unsupported`).

**Enumeration completeness is not resolution completeness.** Every `file`,
`package`, `vcs-change`, `declares`, `clones` entry in every positive Run carries
`coverage: complete` **and** `resolutionCompleteness.state: not-applicable`. No
resolved rung is invented for a file fact anywhere.

### Complete positive Run descriptor graphs — both languages, and syntax

15 Runs, each closed and replayed. Selected:

| Run | verdict | facts | body identity |
|---|---|---|---|
| `RUN-TS-1` | fail | 11 | L0 `a80f6ef7…`, L1 `9a273e0c…` |
| `RUN-RS-1-lib` | pass | 8 | `2aaf0fa7…` (edition 2018) |
| `RUN-RS-2-test` | pass | 8 | `f13b743d…` (edition 2021) |
| `RUN-SYN-CODE` | fail | 5 | `f1892d05…` (grammar variant `js`) |
| `RUN-TSV-jsbody` | pass | 5 | `427d1f04…` (source variant `js`) |

**`RUN-TS-1`** is the ordinary TypeScript project the contract asks for: it
**reads `node_modules` and resolves bare specifiers**, with a retained
`ResolvedNodeModulesLayoutV1` (rows joined by digest, *not* snapshot inventory
rows, because the shared discovery rule prunes `node_modules` by segment), a
retained `TypeScriptConfigGraphV1` whose entry `tsconfig.json` extends
`configs/base.json`, a `package-lock` lockfile joined to the inventory, eleven
`file@enumerated` facts satisfying the inventory-totality obligation, a
`references@resolved-binding` fact, and two clone bodies.

A **Rust context merely present in a TypeScript graph would not exercise the
Rust universe path**, so the Rust Runs are separate graphs with their own
`NativeContextV2`, `DependencySourceSetV1`, `UnifiedFeaturesV1`,
`CargoConfigProjectionV2`, `SourceUnitOwnershipV1` and Rust universe/fact/
Coverage. In `vec_native` the Rust dependency chain runs **down to raw bytes**:
`fileManifestSha256` is re-derived as
`H("native.dependency-file-manifest.v1", rows)`, every row's blob is retained at
exactly its declared length, and `fileCount`/`totalBytes` are recomputed.

### Configuration graphs

| Variant | `configOrigin` | Exercised |
|---|---|---|
| `RUN-TS-1` | `tsconfig` | entry + one base, digests joined to the snapshot |
| `RUN-TSV-synth` | `synthesized` | null entry, empty node set, every `SynthesizedCompilerOptionsV1` value equal to the honored option, `jsx` absent because no `.jsx/.tsx` root exists |
| `RUN-TSV-custom` | **`tsconfig`** | `tsconfig.build.json` — kind **`other`** by the exact basename table, yet `configOrigin` still `tsconfig`; `extendsResolved = [base, override, base]` with the **repeated base retained in precedence order** |
| `RUN-TSV-jsconfig` | `jsconfig` | `jsconfig.json` extending `configs/shared.base.json` (a shared base under **another filename**, kind `other`) |

Negative: relabelling `tsconfig.build.json` as kind `tsconfig` refuses
`native.config-graph-kind-contradicts-path`. This matters because `kind` is
*inside* the hashed `TypeScriptConfigGraphV1`, so it reaches `tsconfigGraphHash`
→ universe → `fact2` → `run2`.

### Clone bodies: L0, a normalized level, and the custody chain

`RUN-TS-1` carries both:

* **L0-verbatim** — the payload is `u32be raw_len ‖ span bytes`, itself under the
  frame's own `u32be payload_len`, so the span is length-prefixed twice. Closure
  **recomputes it from the enclosing fact's own anchor**: a real source join.
  Independently computed, a 4-byte span `a=1\n` yields payload
  `00000004 613d310a` and frame component `00000008 00000004 613d310a`.
* **L1-lexical** — a framed token stream
  (`u32be count ‖ (u16be kindLen‖kind ‖ u32be valLen‖val)*`) which no host can
  recompute, so what is required is exact retained preimage custody plus framing.

Custody negatives, all refusing with distinct causes: `levelId` disagreeing with
the payload's level; `levelVersion` that is not the raw 32 digest bytes of the
retained level specification; `languageId` that is not the derived body language;
`languageVersion` that is not the derived `body-language-version`; a truncated
token stream; trailing bytes; an L0 payload that is not the anchor span; an
anchor range outside the blob.

`body-language-version` is **derived, never accepted**. Reconstructed from the
registry row's `languageVersionBinding` and hashed to 32 raw bytes:

```
TS engine, .js body : {"compilerBuild":"3d17e68a…","compilerName":"typescript",
                       "compilerVersion":"5.6.2","dialect":{"sourceVariant":"js"},
                       "languageId":"javascript","schemaVersion":1}
grammar,   .js body : {"compilerBuild":"f015a74b…","compilerName":"opensip-grammars",
                       "compilerVersion":"0.9.1","dialect":{"grammarVariant":"js"},
                       "languageId":"javascript","schemaVersion":1}
rustc,   shared.rs  : {"compilerBuild":"bbbb…","compilerName":"rustc",
                       "compilerVersion":"1.83.0","dialect":{"edition":2018},
                       "languageId":"rust","schemaVersion":1}
```

**A JavaScript clone body through the TypeScript analyzer universe** carries
`languageId: javascript`, not `typescript`: the body language comes from the
suffix selector, not from the provider. The *same `.js` bytes* read by the
grammar bundle mint a **different** identity (`f1892d05…` vs `427d1f04…`) —
required, because a grammar parse and a compiler parse are different
interpretations.

The bounded version component is derived from **the exact admitted compiler
context and body provenance**: `compilerVersion` is joined to the tool closure
manifest's `semanticVersion` at context admission
(`native.native-context-compiler-version-not-from-manifest` refuses otherwise),
and `compilerBuild` is `rustCommitHash` / `compilerPackageDigest` / the grammar
bundle digest. Nothing operational (platform, paths, resolution inputs, build
tooling, option synthesis) enters.

### Mixed-edition Rust workspace

Workspace with a **`#` marker directory** (`crates/#alpha/Cargo.toml` — admissible
under the canonical path contract, which is exactly why `unitId` is
`H(native.compilation-unit.v1, {schemaVersion, markerPath, targetKind,
targetName})` rather than a `#`-delimited label). `crates/beta` declares package
edition 2018 with a **`[[test]]` target whose own edition is 2021** — a
target-specific edition differing from its package default. `crates/beta/src/shared.rs`
is owned by both.

| Selection | Effective dialect | Body identity |
|---|---|---|
| `{alpha lib, beta lib}` | 2018 | `2aaf0fa7…` |
| `{beta_it test}` | 2021 | `f13b743d…` |
| `{alpha lib, beta lib, beta bin}` | 2018 | `2aaf0fa7…` — **stable**, selection changed, dialect did not |
| 21-crate edition map | 2018 | `2aaf0fa7…` — **stable**, universe identity moved |
| `{beta lib, beta_it test}` | — | **refuses `BODY_LANGUAGE_OWNER_AMBIGUOUS`** |

So the same physical file **is** validly analysed under each explicitly selected
target edition, one selection at a time, each a different `sourceUniverse`; and
the ambiguous unselected request refuses. The large edition map confirms
`editionMapKeys` is excluded from the body record: unrelated crates move the
universe identity and leave the body identity untouched.

**Ambiguity and partial enumeration are different claims.** Partial enumeration
refuses **before any row is read**, so incomplete discovery can never act as an
implicit edition selection. The empty clone view then **must not claim complete
Coverage**: I re-derive the owed pair from the committed ownership record and
this scope's subjects, and four separate refusals hold it —
`COVERAGE_DIALECT_PREREQUISITE` (false `complete`),
`…_PREREQUISITE_UNDISCLOSED` (null deficiency),
`COVERAGE_DIALECT_DEFICIENCY_MISMATCH`, `COVERAGE_DIALECT_CAUSE_MISMATCH`.
`RUN-RS-5` and `RUN-RS-6` seal `indeterminate`, which is the correct outcome —
not a false finding of "no clones".

### Compiler-free syntax-only Runs, and the code/data distinction

Independently verified against the published matrix and body/normalizer laws
rather than taken from prose:

* the `code` subset of the grammar registry (`rust`, `typescript`, `javascript`)
  **equals** the `body-language-version.languageId` enum;
* **no** `data-document` language (`json`, `toml`, `markdown`, `yaml`) is in that
  enum, and no data suffix appears in the syntax dialect table;
* the bundle's `languageId` enum equals the seven bundled languages.

`RUN-SYN-CODE` — a supported **code** grammar with inventory, `declares@syntactic`
and a grammar-parsed clone body: closes with genuine `complete`, no deficiency.

`RUN-SYN-DATA` — an **already bundled data/document** grammar set: the declared
**inventory** capability is served with a genuine `complete` over every path,
while `declares@syntactic` and `clones@normalized-body-hash` are **disclosed
unavailable** (`coverage: unknown`, `language-tier-unsupported`,
`capability-missing`) and never refused outright. **A complete empty result does
not conceal unsupported analysis**: a false `complete` refuses
`SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, a wrong deficiency and a wrong cause each
refuse by their own name.

`RUN-SYN-NONE` — a repository with **no TypeScript and no Rust compilation unit**
(`tool/main.py`, `README.md`, `data.yaml`). `tool/main.py` has no bundled
grammar; it is still **inventoried** with a `file@enumerated` fact, because the
three inventory capabilities are exempt from grammar ownership at *both*
boundaries. Semantic capabilities are correctly unavailable. Exact custody:
context `native.context.syntax.v2` (grammar closure kind `grammar`, `parserVersion`
joined to the closure manifest), universe `native.semantic-universe.syntax.v2`
with the **selected** grammar set committed and `resolutionAttempted: false`.

**Every advertised mode has a representable analysis path** — I built one for
each of `ts-tsconfig`, `js-allowjs`, `js-synthesized`, `rust-cargo` and
`syntax-only`; `rust-cargo-prepared` is representable through
`preparedResolution ∈ {host-prepared, imported-inert}` with `preparedOutputSetId`
non-null, which I exercised in the context/universe binding but not as a further
sealed Run. **An unsupported grammar is tested without assuming a TypeScript
compiler**: `.py` is `unsupported-file / no-bundled-grammar` under the
syntax-only universe, with no compiler anywhere in `RUN-SYN-NONE`.

Chosen grammars are stated in each universe: `RUN-SYN-CODE` selects
`{g-javascript, g-markdown, g-typescript}`, `RUN-SYN-DATA` selects
`{g-json, g-markdown, g-toml, g-yaml}`, `RUN-SYN-NONE` selects
`{g-markdown, g-yaml}`. An **unselected** grammar lends no capability
(`native.syntax-grammar-not-in-bundle` for an unbundled selection).

**Deficiency/`nativeCause` pairing for incomplete or ambiguous clone ownership**
is derived, not copied: `BODY_LANGUAGE_OWNERSHIP_REQUIRED →
body-language-ownership-missing`, `BODY_LANGUAGE_OWNER_UNENUMERATED →
body-language-owner-unenumerated`, `BODY_LANGUAGE_OWNER_AMBIGUOUS →
body-language-owner-ambiguous`, each with `input-closure-incomplete`, projecting
outward as `VERDICT.INDETERMINATE` / exit 3 with the cause as typed detail in the
`coverage2` record the termination names.

### Minimum-resolution predicates at syntactic, resolved and type levels

Seven executed cases (`A5-1..7`), each with qualifying and insufficient inputs,
plus the cross-relation refusal:

| Atom | Fact | Coverage | Result |
|---|---|---|---|
| `exists references@≥syntactic-name-match` | `resolved-binding` | complete | **true** |
| `exists references@≥resolved-binding` | `syntactic-name-match` | complete | **false** |
| `exists references@≥resolved-binding` | `resolved-binding` | complete | **true** |
| `exists types@≥checked` | `annotated` | complete | **false** |
| `exists types@≥checked` | `checked` | complete | **true** |
| `exists references@≥resolved-binding` | none | **unknown** | **indeterminate** |
| `exists references@≥resolved-binding` | none | complete | **false** |
| `exists clones@≥resolved-callee` | — | — | **refuses `RUNG_NOT_IN_RELATION_LADDER`** |

**Missing relation Coverage with no match follows the published three-valued
law**: with no Coverage at all, `exists`, `none`, `all-covered` and
`count-at-most 0` are each **indeterminate** — never a false universal negative.

**Repair evidence requirements and the imported-observation boundary**: the two
planes are disjoint and admission decides the plane from the relation's registry
membership, never from the value — I verified `resolution-incomplete` is a
`NativeSufficiencyDeficiency` and **not** an `ImportedRequirementDeficiency`, and
that the two enums share no member. `RepairPlanDescriptor.closedWorld` is the
**five-field** projection (`dynamicDispatch` and `reasons` dropped); the
authority stays the sealed evidence Run's own full record, and any edit to the
projection mints a different `repairPlanId` that no authorization names.

### Mutation replay scope, repair-apply key, pinned purge

* Generic mutation: `MutationReplayScopeV1 = {schemaVersion, requestId, stepId,
  projectId, operation}`; key = **bare 64-hex `H("workflow.mutation-intent", scope)`**
  = `91d935ef…`. Scoped to one host-minted request and one admitted step — a
  different `RequestId` yields a different key, so fresh requests never
  deduplicate each other's mutations. `repair-apply` is refused in the generic
  field by schema.
* Repair apply: a **different recipe** — raw SHA-256 of
  `C({operation, projectId, repairPlanId, baseSnapshotId})` = `7bab3f95…`,
  which is not the `H` over the same record.
* **Complete pinned-purge refusal**: `request-rejected` / exit 2 /
  `REQUEST.PRECONDITION_FAILED`, detail `evidence.pinned`, `subject` = the RunId,
  and the closed `PinnedPurgeDisclosure` carrying the RunId, the **complete**
  `activePins` inventory sorted uniquely by `pinId`, and the three ordered
  consequences. Validated against `CommandEnvelope`; a duplicate pin id and an
  over-bound inventory each refuse. Neither the disclosure nor any flag confers
  authority.

### Refused hidden/mismatched inputs, per language

TypeScript (13): compiler version not from the manifest, tool digest outside the
closure, incomplete stdlib inventory, component digest disagreeing with the tree,
`lib` not retained, `libSelection` disagreeing with honored `lib`,
`moduleResolutionMode` disagreement, config path outside the snapshot, lockfile
digest mismatch, a Rust context offered as the TypeScript one, a context-free
bind, context bytes that are not the admitted ones, a universe field
contradicting the context.

Rust (8): `rustcVersion` not from the manifest, `rustcDevLlvmDigest` naming a
closure of the wrong kind, replaced config outside the snapshot, linker outside
the closure, dependency `totalBytes` mismatch, the **raw projection file digest
offered as the H suffix**, a `cfgSet` dropping a base cfg, a crate root outside
the snapshot.

Syntax (5): grammar not in the bundle, `parserVersion` not from the manifest, a
data grammar claiming `code`, a code grammar demoted to `data-document`, a row
claiming another language's suffix.

`lib_name_fold` is the **full, non-tailored, context-sensitive default lowercase**
— I verified all four published discriminators (`İ`→`i̇` two code points,
final/non-final sigma, `ß` unchanged) under UCD **15.0.0**, the declared version.

---

## 5. Reconstruction 3 — audit, scope policy, authorization, purge, output

**`ScopeDocumentV1` bound into the retained analysis-spec.** Using its exact
registered `parameter` row (`workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1`),
I built two analysis specs differing **only** in the parameter's `payloadDigest`:

```
registered document digest 012505da4791…
scope policy A  (include src/**)                          d6…  → analysisSpecDigest X
scope policy B  (include src/**, exclude src/generated/**) 3f…  → analysisSpecDigest Y ≠ X
plan.scopeDigest (foundation scope-descriptor)             UNCHANGED in both
```

The two scope records stay distinct throughout: `plan.scopeDigest` is the
repository **extent actually walked**; `ScopeDocumentV1` is the policy's
include/exclude glob **selection over** that extent. With detector, policy and
waivers held fixed, every moved entry is attributed to the **first** axis at
which it changes — `E2 → E3` = **SCOPE-DELTA**; `E0`, `E1`, `E2` and `E4` are
`not-needed`. The binding verifier's two refusals are deliberately not merged
(`BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER` vs
`BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`), and an **ambiguous** selection
refuses earlier on `CONFIG.INVALID` with no third spelling — I confirmed all
three details are registered members of the closed public registry.

I also reproduced the selection-cardinality defect: a spec with **two distinct**
`ScopeDocumentV1` payloads under the one registered row is admitted by the
schema (`uniqueItems` sees two distinct items) and must be refused by the
selection law — my closure refuses it
(`ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS`).

**Zero-config selection with multiple workspace units and a partial release.**
Three units (`.` ts-tsconfig, `crates/core` rust-cargo, `docs` syntax-only)
against a release declaring only four capabilities. Derived independently from
the matrix, not from prose: **11 capabilities per TypeScript unit, 10 per Rust
unit** (`clones-cross-tsjs` is the only `NOT-SELECTED` cell, in three modes),
**31 requested rows**, and **21 disclosed absences** — every one still requested,
none dropped. I independently reproduced the published bound arithmetic:
93 × 11 = 1023 admits, 94 × 11 = 1034 refuses `PROJECT.SCOPE_LIMIT` with subject
`requestedCapabilities:1034>1024`, without truncation.

**Candidate-only clone capabilities**: `clones-near` and `clones-cross-tsjs` have
**empty** matrix `relations`, so no Coverage entry could carry a pair; their only
public route is the advisory selection account
(`projection: selection-account-only`). Fact-producing capabilities carry
`projection: coverage-entry` with their exact `relation@rung` coordinates.

**What the ORIGINAL invocation discloses** (from `command-inventory.v1.json`, 45
commands): for `default` — `requestClass: analysis`, `authority:
authoritative-default`, steps `[analysis, render]`, formats
`[human, json, sarif, html, agent]`, and eight declared `parityFields` including
`capability-availability`. Ownership fields are typed and never concatenated:
each notice carries `capabilityId`, `languageMode` and `workspaceRoot`
separately, because `workspaceRoot` is a `UserInputPath` bounded at 4096 while
`BoundedText` is 1024. Cardinality is bounded per step (≤1024) and per
invocation (≤64 steps), **composed per step** so 2×1023 notices survive rather
than being flattened into one 1024 array; order is the selection's own
(`sequence`). A step that made no selection contributes no entry; one that
selected and found nothing absent contributes an **empty** entry — a positive
statement that it checked.

Single-step (`default`) and named multi-step (`audit`, four steps, two analysis
steps with **different unit selections**, a delegated verdict gate and a
`terminal`-gated render) both validated end to end.

**Product promise vs installed availability vs override vs prerequisite** are
four different things and I kept them apart: the matrix fixes the *request*; the
authenticated release declaration states *availability* and never scope; explicit
`analysis.capabilities` narrows the *request* with its own provenance; and a
semantic prerequisite the admitted universe cannot serve keeps the more specific
`language-tier-unsupported`, which outranks `provider-unavailable`.

**Public responses built from an actual internal refusal plus originating boundary.**
`public_termination_for(key, origin)` normalizes the colon-suffixed guard output
by longest registered key, refuses an unregistered key and refuses an origin a
key cannot have. Complete `kind=failure` envelopes, all schema-valid, with a
**nonempty `errors` array** in every case:

| Origin | class / exit | errorCode | domainDetail | errors[0] |
|---|---|---|---|---|
| external configuration | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.INVALID` | `CONFIG.INVALID` |
| retained external input | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | *absent* | `native.capability-spec-invalid` |
| host-generated internal record | **operational-failed / 4** | `SYSTEM.OUTCOME.ILLEGAL_STATE` (`faultCause: host-invariant`) | *absent* | `HOST.INVARIANT_VIOLATED` |
| producer boundary | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` | *absent* | `native.coverage-cause-unsupported` |
| authenticated release declaration | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | *absent* | `native.release-declaration-invalid` |
| `NOT-SELECTED` cell (origin-independent) | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED` | `PROVIDER.NOT_SELECTED` |

These are complete envelopes, not termination fragments. The bounded-subject
encoding is exact: a 4096-character refused value composes to **exactly 1024
Unicode code points**, preserving the registered key verbatim and eliding only
the value with `...#sha256:` plus the digest of the untruncated UTF-8 bytes.

**The selected D9 extension, checked against the inherited contract.** I read
`d9-exit-contract.v1.14` directly. Its `faultCause` enum has 11 members and does
**not** contain `host-invariant`; `faultCauseToErrorCode` has 10 entries and
`SYSTEM.OUTCOME.ILLEGAL_STATE` has **no** preimage in it, and the map is
injective today. So the extension adds exactly one member, maps it to an existing
code, and **preserves both totality and injectivity** — the subject's precision
claims are correct, and its disclosure that a checker reading v1.14 alone would
refuse a lawful `host-invariant` termination is also correct. `causeModel.precedence
= [faultCause, rejectionCause, deficiency]` confirms the operational-fault
dominance my aggregate ordering implements.

**Purge / replay / required-output failure.** Six schema-validated termination
examples. Three *different event positions* kept apart: a query requiring proof
after purge refuses `REQUEST.PRECONDITION_FAILED` / `evidence.purged` **before**
evaluation (exit 2); an inability *during* a selected operation is
`HOST.IO_FAILURE` (exit 4); successfully admitted **partial** native inputs
instead yield an *authoritative* indeterminate Run (exit 3). Regeneration
mismatch is `HOST.IO_FAILURE` / `evidence.regeneration-mismatch` and cannot
replace the sealed Run. A required renderer failing after commit is
`DELIVERY.REQUIRED_FAILED` (exit 4, `faultCause: delivery-required`) retaining
the RunId and rewriting nothing; an optional export sink leaves `success`.

**Which subsystem owns every decision** (this is the whole point of the split):

| Decision | Owner |
|---|---|
| repository boundary, custody, trust time, revocation, leases, platform admission | security S3–S9 |
| unit discovery inside that boundary, membership, capability cells, contexts, universes, Coverage production | native §1–§9 |
| canonical encoding, every semantic identity, closure, replay, retention, purge, availability | identity §3–§5 |
| invocation/step/attempt lifecycle, comparison, imports, policy, repair, output parity, D9 projection | workflows §1–§9 |
| exact numeric admission, Config2 resolution, qualification reports | admission §1–§3 |
| **finding construction, policy evaluation, verdict, persistence, finalization, rendering, termination** | **the host, always** |

---

## 6. Required semantic proof replay

This is a separate step after identity/schema/closure admission and it is the
reason several graphs that *close* are still not complete positives.

For **every** positive Run I re-ran my own evaluator over the **retained**
policy, compiled rule program, views, facts, Coverage, scopes and waivers, and
compared the complete recomputed bundle to the retained claim. Exported per Run
in `vectors/<RUN-ID>.json` as `replayedInputs`, `computedProof`, `retainedProof`
and `comparison`. All 15 report `comparison: "MATCH"`.

The replay derives, from the inputs alone: the complete subject enumeration; the
exact `matchingFactIds` and `coverageIds` per predicate; predicate **addresses**
(`p`, `p.0`, `p.1`, …) and child values; the `program-predicate` record and its
`nodeDigest` over the addressed node; the witness record and its digest; every
finding emission; and the final verdict. No caller-authored truth, no empty-match
flag and no literal pass/fail was accepted anywhere: `verify_replay` never reads
`proof.verdict` or `predicateProofs[].value` except to *compare*.

**Tampered-result control.** Two controls preserve valid record identities and
citation membership and change only the claimed logical result:

| Control | Linkage closure | Replay |
|---|---|---|
| `CTRL-tamper-verdict` | **admitted** (every identity, join and citation valid) | **REFUSED**: `verdict: recomputed fail != retained pass` |
| `CTRL-tamper-predicate-value` | **admitted** | **REFUSED**: `('cb9.clone-present','src/a.ts','p') value: recomputed true != retained false` |

This is the discriminating result: **a linkage-valid graph that has not passed
replay is not a complete positive.** Both tampered Runs pass every structural
check and are caught only by recomputation. Kept strictly separate from future
authentication and host qualification: the replay proves reproducibility of the
result, not soundness of the evaluator, and it authenticates nothing.

---

## 7. Validation discipline actually applied

* **Every record validated against its owning normative schema**, resolved
  through the pinned local `$ref` closure with no network retrieval: identity
  records against `identity-schemas.v2`, relation payloads against the row's own
  selector in `relation-payload-schemas.v2`, `CoverageResultV3` and every native
  record against `native-evidence.schemas.v2`, policy/waivers/rule program/scope
  document against `policy-document.schema.json`, invocations and envelopes
  against their workflow schemas.
* **Retained closure independently executed**, not asserted: identity
  recomputation from retained frames, frame prefix/domain/length/canonicality,
  preimage retention and re-hashing, `admit_native_context` and
  `bind_*_universe` re-run over retained bytes, relation registry ladders,
  rung field rules, `universeRule`, `anchorLaw`, `snapshotJoins`,
  `coveragePartitionLaw`, `coverageTotalityLaw`, RC-0/1/2/6, the
  deficiency/cause registry, the scope capability laws, the body-identity join,
  view/evidence/proof/seal/Run joins, closure kind and membership, the
  analysis-spec ownership tuple and parameter cardinality, and the Plan-budget
  agreement.
* **Machine-readable object table** — `vectors/<RUN-ID>.json` carries every typed
  identity with its **domain and full descriptor**, plus **all blob and frame
  bytes keyed by digest** as a base64 export. Schema documents, the committed
  capability-manifest artifact, closure trees, level specifications and body
  frames are part of that closure wherever the retention law requires them.
* **Each language/grammar uses its own actual selected provider and capability
  context** — the Rust Runs have Rust contexts, universes, facts and Coverage;
  the syntax Runs have a grammar bundle and no compiler.
* **Valid controls, invalid mutations and explanatory calculations are separate
  categories** in the report (`positiveRuns`, `closureNegatives`,
  `tamperControls`, `*Vectors`, `designGaps`), and the runner **exits non-zero**
  on any required-control failure. Counts below are measured results, not labels.

| | count |
|---|---|
| complete positive Runs closed **and** replayed | 15 / 15 |
| retained-closure negatives refused | 48 / 48 |
| identity / admission / evaluator vectors | 62 |
| native context / universe / nested-record vectors | 37 |
| workflow / surface / termination vectors | 43 |
| provider protocol traces | 9 |
| required control failures | **0** |

### First observed refusal boundary, and what it masks

Every negative records `firstObservedBoundary`. Four maskings are real and I
state them rather than claiming each law was reached:

1. `N-anchor-borrowed-package` stops at `FACT_ANCHOR_CARDINALITY`, masking the
   `file` row's `anchorPathField` — which is exactly what the registry says
   ("subsumed rather than reached").
2. A *wrong deficiency* on a Rust dialect disclosure stops at
   `native.coverage-cause-carrier-unsupported` (the substituted
   `budget-exhausted` fails its own carrier test first), masking
   `COVERAGE_DIALECT_DEFICIENCY_MISMATCH`; that name is reached by the
   syntax-universe variant instead.
3. `N-syntax-wrong-cause` stops at `native.coverage-cause-not-for-deficiency`,
   masking `SYNTAX_CAPABILITY_UNSUPPORTED_CAUSE_MISMATCH`.
4. A view whose producer closure is not Plan-selected stops at
   `CLOSURE_NOT_SELECTED`, masking `FACT_PRODUCER_NOT_VIEW_PRODUCER`; that law is
   reached directly by `N-fact-producer`.

### Distinctions kept apart

**Schema validation** (shape, enums, bounds, `additionalProperties`) ≠ **helper
predicates** (my `check_order`, `registered_pair`, `lib_name_fold`) ≠ **full
retained closure** (recomputation and joins over retained bytes) ≠ **future host
enforcement** (custody races, fsync, ACLs, process confinement, signature
verification, ledger durability — none of which is claimed or executed).

### Two bugs in my own code, with their corrections

Recorded as required, with the original failure preserved:

1. `run_tsvariants` `synth` first failed
   `native.universe-context-field-mismatch: synth:strict` because my TypeScript
   context helper hard-coded `strict: true` while `SynthesizedCompilerOptionsV1`
   fixes `strict: false`. **A helper bug with a precise existing normative
   answer**, not a design gap: native §2.4 states "in synthesized mode every
   value in `synthesizedOptions` equals the corresponding honored option".
   Corrected by parameterising the helper.
2. `parse_token_stream` let a raw `struct.error` escape on a truncated L1 stream
   instead of a typed refusal, which would have reported a well-formed refusal as
   a crash. Corrected to raise `TOKEN_STREAM_FRAMING` with the offending token
   index; the framing grammar itself is unchanged.

---

## 8. Findings

### MUST

**CB9-MUST-1 — the evaluator's subject enumeration has no published binding to a
retained Run.**
`policy-document.schema.json#/$defs/Rule/properties/subjectEnumeration` carries
`universe` as a bare `common#/$defs/CanonicalIdentifier` (`^[a-z][a-z0-9]*…`) and
`subjectKind` as a bare enum `{file, symbol, export, package}`. Every fact and
`subject-scope` carries `sourceUniverse`/`targetUniverse` as a **64-hex
`h-identity`** of a `native-semantic-universe` domain, and the relation registry's
`subjectKindLaw` uses `{source-path, package-name, symbol}`. Nothing joins the
two universe forms, the two subject-kind vocabularies overlap in exactly one
member (`symbol`), and **no document says where the candidate subject population
comes from in a real Run** — the only statement is
`policy-test.schema.json#/$defs/Subject` ("the complete enumerated subject
inventory for the **fixture**"), which is the fixture plane.
identity §4 nevertheless requires the verifier to "recompute scope membership,
matches, completeness and each result", and `predicateProofs` are keyed by
`subjectId`. Two conforming hosts enumerating different subjects therefore mint
different `proof2`, `seal2` and `run2` from one admitted Plan — the exact
independent-replay defect the contracts already closed for
`analysis-spec.requestedCapabilities[].capabilityId` (CB4-SHOULD-2) and
`Atom.minResolution` (CB3-MUST-2). *I had to invent all three bindings.*

**CB9-MUST-2 — `FieldFilter` has no published projection onto `fact2` + relation
payload.**
`policy-document.schema.json#/$defs/FieldFilter/properties/field` admits
`{subject, target, resolution, universe, confidenceMillionths, subjectKind,
targetKind, observability}`. Of these, only `resolution` and
`confidenceMillionths` are fields of `identity-schemas.v2#/$defs/fact`; the other
six have no home. The only place all eight are defined together is
`policy-test.schema.json#/$defs/FactRecordCandidate`, explicitly "a host-schema
fact supplied as **test input**", and it is *type-incompatible* with the product
plane: its `universe` is a `CanonicalIdentifier`, which cannot represent a 64-hex
identity beginning with a decimal digit, and its `subject` is a `LogicalPath`,
while nine relations' subjects are opaque `SubjectIdV1` values the record
associates with no path. `filters` enters `emitWhen`, hence `programDigest`,
`ruleProgramDigest`, every `program-predicate.nodeDigest` and the whole proof.
*My evaluator refuses a filtered atom (`FILTER_PROJECTION_UNPUBLISHED`) rather
than inventing semantics; the field cannot be used at all.*

**CB9-MUST-3 — an imported-evidence atom has no representable witness and no
published matching law.**
`imported-evidence.schema.json#/x-opensip-evidence-relation-registry` explicitly
admits policy atoms over `runtime-observation` and `history-change`, and native
§4.6 states those relations "mint no `fact2`, carry no
`sourceUniverse`/`targetUniverse` and have no Coverage entry". But
`identity-schemas.v2#/$defs/predicate-witness` closes `matchingFactIds` to
`^fact2:…` and `coverageIds` to `^coverage2:…`. So `exists` / `none` /
`count-at-most` over an imported relation has **no representable witness
content**, and there is no published projection from an atom to import payload
subjects (the one that exists,
`x-opensip-imported-requirement-law/targetSubjectProjection`, is keyed by a
finding fingerprint and is explicitly the **repair** requirement law). The value
would be producer-asserted — precisely what identity §4 forbids
("Neither a provider nor a witness supplies its own expected result").

**CB9-MUST-4 — the waiver's effect on the sealed verdict is unspecified, and
three verdict-bearing records have no stated relation.**
identity §3 says waiver resolution "selects the active admitted waiver set
before pure evaluation and retains that resolved set", and §4 says the verifier
"recomputes … rule outcomes and aggregate verdict" — but **nothing states what a
waiver does**. `identity-schemas.v2#/$defs/finding` has **no `waived` field**
(the only `waived` flag in the kit is on `policy-test.schema.json#/$defs/CaseResult`,
the fixture plane), so a retained Run cannot record waived status; nothing says
whether a waived finding is emitted, whether it enters `proof.findingIds` /
`evidence.findingIds`, or how it changes the verdict. And `proof-bundle.verdict`,
`evaluation-seal.verdict` and `policy-derivation.verdict` all exist with **no
published relation among them** — a search of `identity-and-evidence.md` for
"verdict" returns only the domain table rows and the replay sentence. Over one
admitted Plan whose gating rule emits on a waived target, one reading seals
`fail` and the other seals `pass`. *I assumed emission-then-gating and
`seal.verdict == proof.verdict`; both are inventions.*

### SHOULD

**CB9-SHOULD-1 — `all-covered` has no stated value on the twelve non-resolved
registered pairs.** RC-1 forces `resolutionCompleteness.state: not-applicable`
there, and identity §4 says `all-covered` is "true **only** with admitted
resolution-complete coverage". Strictly read, `all-covered` over any of the
twelve is permanently indeterminate, so a gating rule using it can never pass.
The strict reading is what the text supports and is what I implemented, but the
consequence is severe enough to deserve one explicit sentence.

**CB9-SHOULD-2 — `finding-fingerprint.subjectKey.discriminator` for
signature-less subject kinds.** It is `required` with `minLength: 1` on every
fingerprint, and identity §3 explicitly admits "a finding over a zero-anchor
inventory fact". But the token source is "declaration-signature tokens … in
grammar order", which a `file`, `package` or `vcs-change` subject does not have.
The *authority* is placed (the selected detector closure defines the token
projection), so replay is stable across installations sharing that closure; what
is missing is the contract-level statement for those subject kinds, and
`finding-key2` reaches baseline membership and comparison attribution. *I invented
a two-token projection for my vectors.*

**CB9-SHOULD-3 — `subjectEnumeration.include`/`exclude` over non-path subjects.**
`GlobPattern` is defined as a "closed glob over **LogicalPath**", but a `symbol`-
or `package`-kind enumeration ranges over subjects the registry says are not
paths (`SubjectIdV1`, `ns:opaque`). Either state what a path glob means against
an opaque subject id, or state that include/exclude apply only to source-path
subject kinds.

### Advisory (non-blocking)

* **CB9-ADV-1** — the D9 `host-invariant` extension is correctly disclosed and
  its properties hold (see §5). The successor D9 artifact remains an owed
  cross-unit deliverable; the subject already carries it as such, so this is a
  confirmation, not a new finding.
* **CB9-ADV-2** — every declared mirror in the kit holds under independent check:
  the ladder mirror (exactly and in order), `policy-document Rung` = the union of
  the ladders, `native Relation`/`Rung`, `NativeSufficiencyDeficiency` =
  `DeficiencyV2`, the disjointness of the two requirement planes, `LanguageMode`
  = the language-mode map, the grammar `code` subset = the `languageId` enum,
  `DomainDetailCode` = the 289-record public registry **exactly**, every route
  registry detail a registry member, and the matrix's 66 cells = the complete
  11 × 6 product. Nothing drifted.
* **CB9-ADV-3** — `PROJECT.SCOPE_LIMIT` is reachable by an *ordinary* repository:
  94 TypeScript units under the matrix-fixed default produce 1034 rows against a
  1024 bound. The contract states this and I confirmed the arithmetic. It is a
  real product limit disclosed as such, not a defect.

### What did *not* require invention

Worth recording, because the list is long: the canonical encoder and every
digest law; `H` and its frame; CVE1 and the four capability gates; the relation
registry including ladders, `anchorLaw`, `snapshotJoins`, `coverageTotality` and
`coveragePartitionLaw`; RC-0/1/2/6 and the deficiency/cause registry; the
subject-scope commitment recipe; native context admission and universe binding
for all three languages, down to nested dependency manifests and raw bytes; the
`body-language-version` derivation and all three dialect axes; the grammar
capability law at both boundaries; the provider state machine; the public route
derivation and bounded-subject encoding; the default capability selection and its
availability disclosure; the mutation and repair-apply keys; the pinned-purge
disclosure. All of these were reconstructible from the kit alone, and in several
places the kit is *more* precise than it needed to be (the double length prefix at
L0, the `fold` discriminator table, the two cargo-projection digests, the
traversal order for ADM-ORDER).

---

## 9. Limitations

* Everything a real host would **measure** is a synthetic trusted observation
  here. No compiler, Cargo, provider, filesystem, ACL, SQLite, signature, clock
  or renderer was executed. Real OS/compiler/crypto/SQLite measurements are
  future qualification and I do not demand the product already exists.
* My closure checker is thorough but not exhaustive over the kit: I did not
  implement cache/regeneration-key admission, the `import2` staleness table end
  to end, `SourceMappingV1` per-file verification, baseline adoption/pivot
  resolution, the `PreparedOutputSetV3` PO-0..PO-4 consumption rules, or the
  security unit's trust-time, revocation and lease machinery. Those were read and
  are reflected in the narrative, not in executed code.
* `rust-cargo-prepared` is exercised at the context/universe binding level, not as
  a further sealed Run.
* The `parentSubjectSha256` in the manifest is unverifiable from a declared
  subset.
* Passing everything here is **not** product qualification, **not** a readiness
  grade and **not** implementation authorization. It is a design-reference
  reconstruction over one blind kit.

---

## 10. Verdict

**CHANGES_REQUIRED.**

The identity, native-evidence, capability-manifest, protocol, retention and
surface layers of this design are, in my independent reconstruction, unusually
complete: I rebuilt them from the prose without an oracle, closed fifteen Runs
across TypeScript, JavaScript, Rust and three compiler-free syntax modes, replayed
every one of them, and could not find a way to make a tampered result, a hidden
input, a borrowed anchor, a false `complete`, a fabricated dialect or a mismatched
native input survive. The closing digest law, the `anchorLaw`, the ownership
selection law and the grammar capability law in particular do real work — several
of my first attempts at a "reasonable" graph were refused for reasons I had to go
back to the text to understand, which is the behaviour a design contract should
have.

The gap is that the **declarative policy DSL is admissible in shapes the retained
Run cannot decide**. `subjectEnumeration` and `FieldFilter` are the last two
fields in this design that enter a content identity while carrying no published
vocabulary or join — the same condition the design itself already diagnosed and
closed twice, for `capabilityId` and for `minResolution`. Imported-evidence atoms
are admissible with no representable witness. And the waiver, which is committed
into `PlanId` and named by three separate verdict-bearing records, has no stated
effect on any of them.

Those four are not algorithm freedom. Query planning, chunk sizes, caching,
normalizer internals and physical layout are freedom, and the contracts say so.
These four change the public semantic result — the emitted findings and the sealed
verdict — so two conforming hosts would disagree on the product's own answer from
one admitted Plan. That defeats independent replay across machines, which is the
property the whole identity graph exists to provide.

Closing them looks small relative to what is already here: a subject-enumeration
join (universe form, subject-kind map, population source), a per-relation field
projection, either a witness member for imported observations or an explicit
empty-witness rule with a published matching law, and a paragraph on waiver
application and the three verdicts. With those four written down, I would expect a
blind consumer to reach ACCEPT-RECONSTRUCTABLE on this kit.

*No claim of full product qualification or implementation authorization is made.*
