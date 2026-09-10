# Blind consumer-B reconstruction — OpenSIP DR-011-R10

**Verdict: CHANGES_REQUIRED**

Two MUST-class and two SHOULD-class design gaps remain unresolved. Everything else
in the promised scope reconstructed cleanly from the supplied bytes alone: I built
a working canonicalizer, `H` helper and Run-closure checker from prose, and closed
complete positive Run graphs for TypeScript, JavaScript-through-the-TypeScript-engine,
Rust (mixed edition, per-target selection), and all three compiler-free syntax-only
classes, plus 57 negative vectors that every refuse with a typed cause.

This is a design-reference reconstruction only. It is **not** product qualification,
**not** implementation authorization, and every filesystem, compiler, provider,
enumerator and OS observation in my vectors is a synthetic assumption, never native
enforcement proof.

---

## 1. Input custody and hash verification

| Item | Result |
|---|---|
| Manifest | `consumer-input-manifest.json`, 45 files |
| Declared parent subject | `8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023` |
| Files verified byte-exact (SHA-256 **and** declared length) | **45 / 45** |
| Mismatched | none |
| Missing | none |
| Files present but not in the manifest | none |

The verification is re-run mechanically by `src/run_all.py` and recorded in
`vectors/summary.json#inputVerification`. I did not read the original repository,
any author Python/TypeScript model, any fixture/case/golden/report, any prior review,
or any other `/tmp/opensip-design-corrections` directory. Historical and review links
inside the inherited normative documents were treated as provenance only and not
followed.

**One input-custody observation, not a design defect.** Two contracts name an
"authenticated release declaration registry" as the authority for the default
profile and the applicable capability set
(`native-evidence.md` §1.4, `admission-and-qualification.md` §1.1). That document is
not among the 45 supplied files. I did **not** treat this as a repository omission:
the capability matrix in the kit carries capability ids and the contracts describe
the registry's role well enough to reconstruct everything that depends on it. It
does, however, leave one field without a named vocabulary authority — see
**CB4-SHOULD-2**, which I raise against the *contract text*, not against the kit.

---

## 2. What I reconstructed, and who owns each decision

### 2.1 The pipeline, end to end

**Zero-config discovery → typed config/source.**
Discovery is the **security unit's** decision (`security-and-lifecycle.md` §S3):
deterministic over `lstat`/ACL results through `O_NOFOLLOW` handles, no environment,
no `PATH`, no `HOME`; the walk selects `mode: config` / `vcs-default` / `cwd-default`,
and a config below a VCS root is a deliberate project boundary (ADV-3). After an
`ACCEPT`, `boundary_inventory(result)` produces the closed
`AdmittedBoundaryInventoryV1`, which the host passes **unchanged** to the **native
unit's** `discover_units` / `assign_membership` / `unit_scope_descriptor`
(`native-evidence.md` §1.4 U-8). One shared discovery rule prunes `node_modules`,
VCS trees and Cargo `target` **by exact path segment**; the native instrument may
never re-derive a boundary from caller input, and an inventory whose pruned trees
disagree refuses `PROJECT.DISCOVERY_INVENTORY_MISMATCH`.

Typed configuration is the **foundation's**: lexical admission before JSON decoding
can round a number (`admission-and-qualification.md` §1), then
`product-configuration.schema.v2.json#discovery` layered resolution into the closed
`identity-schemas.v2.json#/$defs/semantic-configuration` — all five sections always
present, an unselected section exactly `{}`. `resolvedConfigDigest` is
`raw SHA-256(C(that record))`.

Snapshot capture consumes **the same** admitted boundary inventory
(`identity-and-evidence.md` §5, "Snapshot capture consumes the same admitted boundary
inventory as native discovery"), removes nested-repository / nested-project /
custody-excluded paths **before opening or hashing bytes**, and mints
`snapshot2 = H("snapshot", {projectId, sourceInventory, resolvedConfigDigest,
scopeDigest, vcsDigest})`.

**Invocation / step / attempt lifecycle** is the **workflow unit's**
(`workflows-and-surfaces.md` §1): `RequestId` minted before admission and retained for
refusal as well as success, an ordered acyclic list of at most 64 steps with
zero-based `StepId`, a fresh `ExecutionId` per admitted attempt and at most 3
attempts. Only `analysis` and `verify` seal or link a `run2`. The step DAG and the
derivation DAG never reference each other.

**Semantic identity versus operational authority.** `RequestId`, `ExecutionId`, wall
clocks, PIDs, credentials, authorization nonces, receipts and output destinations are
*operational* and excluded from Run identity (`identity-and-evidence.md` §2). I
verified this constructively: two independent attempts over identical semantic inputs
minted the **same** `run2` (vector `P-operational-exclusion`), while one changed
source byte moved `snapshot2` and therefore `plan2` and `run2`
(`P-semantic-field-change`).

**Mutation versus analysis steps.** A generic `mutation` step's replay key is the
bare 64-hex `H("workflow.mutation-intent", MutationReplayScopeV1)` over exactly
`{schemaVersion, requestId, stepId, projectId, operation}` — operational, scoped to
one host-minted request, and explicitly **excluding** `repair-apply`. Repair apply is
the content-derived exception: `raw SHA-256(C({operation:"repair-apply", projectId,
repairPlanId, baseSnapshotId}))`. I built both and confirmed they are different
recipes over different preimages (`W1`, `W2`), and that
`invocation-record.schema.json#/$defs/MutationReplayScopeV1` refuses `repair-apply`
in the generic scope.

**Plan.** `plan2` (`identity-schemas.v2.json#/$defs/plan`) binds snapshot,
`capabilityManifestId` **and** `capabilityManifestBytesDigest`, semantic closures,
`analysisSpecDigest`, `resolvedConfigDigest`, the `nativeContextDigests` **set** of
bare 64-hex suffixes, import IDs, policy/waiver digests, the foundation
`scope-descriptor` digest, the deterministic budget and `semanticGrantDigest`. I
enforced identity §3's budget join: a Plan whose inline `budget` contradicts the
`analysis.budget` of the resolved configuration it names is refused before evaluation.

**Native facts / Coverage / view.** A universe is bound to its admitted context
*before* PlanId (`native-evidence.md` §2.1/§2.4/§1.2); the context bytes are a
**required** argument, so there is no context-free admit path. `subjectScopeCommitment`
is `"sha256:" +` the 64-hex suffix of the *identical* `scope2` the host mints from its
**own** enumeration (§4.1a) — one preimage, one digest, two spellings. The host builds
the Coverage key from its own enumeration and a provider-supplied commitment is never
an input to that step.

**Proof verification.** The evaluator is pure and consumes only Plan-bound,
schema-admitted inputs (`identity-and-evidence.md` §4). Predicate proofs address
exact nodes of the admitted `RuleProgramV1` through the `program-predicate` record,
whose `predicateId` is the *total, deterministic* node address (`p`, `p.0`, `p.1`, …).
Before sealing, the host independently replays the admitted program against the
retained closure and compares the **complete normalized result**, not a checksum.

**Evidence / Seal / Run.** The graph is acyclic by construction: proof includes
neither `evidenceId` nor `runId`; evidence may include proof; seal includes both; Run
includes seal. I enforced this in my closure and it holds for every positive graph.

**Durable receipt and current availability.** `identity-and-evidence.md` §5: default
`opensip`/`analyze` is `DURABLE_AUTHORITATIVE` under CD-RT-5 with retention origin
`DEFAULTED` disclosed before the first write and no implicit policy file. The commit
order is closure-validate-and-replay → blobs → one synchronous ledger transaction
(Run manifest, object refs, availability generation, pins, commit receipt) →
acknowledge. Sealed assurance (`verified` / `verifiable` / `replayable`) is immutable;
**current availability** is a separate monotonic-generation record and a query reports
both.

### 2.2 Subsystem ownership of every decision

| Decision | Owner | Selector |
|---|---|---|
| Repository root, custody, trust time, revocation, leases, platform profiles | security | `security-and-lifecycle.md` S3–S9 |
| Boundary inventory handed to native | security | S3 "Admitted boundary inventory"; native §1.4 U-8 |
| Repository-code / test-runner grants; repair apply & recovery authorization | security | S10, S10.1, S10.2 |
| Language units, membership, universes, contexts, facts, Coverage payloads, protocol | native | `native-evidence.md` §1–§9 |
| Deficiency + `nativeCause` typed detail (inside `coverage2`, no new D9 enum) | native | §10, H-3 |
| Canonical encoder `C`, `H`, the closing digest law, the payload registry, the Plan/Run graph, retention/purge | foundation/identity | `identity-and-evidence.md` §3–§5 |
| Pure evaluation and predicate semantics | evaluator (in the TCB) | §4 |
| Invocation/step/attempt, baseline, comparison, imports wrapper, policy DSL, review, repair, command inventory, output parity | workflow | `workflows-and-surfaces.md` §1–§12 |
| D9 class / code / exit assignment and the closed public detail vocabulary | host | §9; `public-detail-registry.v1.json` |
| Numeric and schema admission, qualification reports | foundation | `admission-and-qualification.md` |

---

## 3. Independent vectors and results

All code is mine, written from the prose and the kit's normative schemas. No author
model, checker, fixture or golden was read, and no expected value was copied from
anywhere: every digest below is computed by `src/osip.py`, whose canonicalizer and
`H` frame I wrote from `identity-and-evidence.md` §3 alone.

**Totals: 126 vectors — 56 positive, 57 negative (all 57 refuse), 11 mechanical
verifications of the contracts' own claims, 2 advisories — plus 8 gap records.**
Sources in `src/`, machine-readable results in `vectors/`.

### 3.1 Canonicalization, admission and identity (`vectors/v1-admission.json`, 43)

Exact integer admission (`1.0`, `1e0`, `-0`, `NaN`, `2^64`, `-2^63-1` all refuse;
`-2^63` and `2^64-1` admit); duplicate keys refuse at both the top level and nested;
booleans stay distinct from integers; lone surrogates and malformed UTF-8 refuse;
depth 32 admits and 33 refuses without truncation; the 4 MiB cap refuses.
`C` orders keys by **UTF-8 bytes** (`"a" < "z" < "é" < "😀"`), escapes only
`"`/`\`/`\b\t\n\f\r` and lowercase `\u00xx` for other C0, leaves `/`, U+007F and
U+2028 unescaped, performs **no** Unicode normalization (NFC and NFD are different
descriptors with different digests), and never sorts or dedupes an array.

`H(D,X)` is demonstrably not `raw SHA-256(C(X))`, and the same descriptor under two
domains gives two identities — which is what lets one CAS keyed by raw SHA-256 hold
raw artifacts, canonical records and `H` preimage frames without collision. Frame
admission is exact: a raw payload offered where a frame is required fails the prefix,
an unregistered domain refuses, a length lie refuses, and a frame body that is not
`C` of its own parse refuses.

The whole closed `x-opensip-order` vocabulary is exercised, including
`canonical-order` admitting equal repeats, duplicate inventory paths refusing with no
tie-break, `sequence` retaining repeated declaration-signature tokens, and an
annotation outside the vocabulary refusing rather than passing silently.

All eight CVE1 types encode with their exact tags; map entries sort by unsigned
key bytes so `{"a","b"}` and `{"b","a"}` encode identically; a non-NFC string is
rejected rather than normalised; floats are forbidden. CVE1's already-NFC admission
is confined to the capability manifest and leaves `C`'s no-normalization profile
intact.

### 3.2 Complete Run graphs (`vectors/v2-runs.json`, 44)

**TypeScript, three configuration shapes, all closing.**

* *Ordinary project*: reads `node_modules` through a retained
  `ResolvedNodeModulesLayoutV1` (two installed packages, rows joined by digest and
  **not** snapshot inventory rows, because the shared discovery rule prunes
  `node_modules` by segment), with an explicitly selected **custom-named** project
  config `configs/app.build.json` (node `kind: other`, deriving `configOrigin:
  tsconfig`) inheriting from **multiple ordered bases including a repeated base**
  — `["configs/base.strict.json", "configs/base.node.json",
  "configs/base.strict.json"]` — whose later-wins precedence is retained because
  `extendsResolved` is a `sequence`, not a set.
* *jsconfig*: `jsconfig.json` extending a shared base under **another filename**
  (`shared/base.common.json`, kind `other`); the entry node kind decides
  `configOrigin: jsconfig`, so a jsconfig program stays a jsconfig program.
* *Synthesized*: null entry, empty node set, `SynthesizedCompilerOptionsV1` equal to
  every honored option, `lockfileKind: none`, `nodeModulesInReadSet: false`.

**JavaScript body through the TypeScript analyzer universe.** One `typescript-v2`
engine universe produced both a `typescript` body (`src/app.ts`) and a `javascript`
body (`src/legacy.js`) over **byte-identical** spans, with different identities:

```
ts  L0-verbatim  sha256:c5ebedb8c271c9de54ce4f436f1e17ec32f89231b5c19ac7dccdb14c5eb15d38
ts  L1-lexical   sha256:5eb62234c5fd5b3d57d92d2ed98e569677cffccd35cff54b5ad72a82bb0f1a92
js  L0-verbatim  sha256:801612ea90992f312e883e4c39055c906924ff17497dfde1cfb9daf69a2e2a7f
```

The `body-language-version` record is **derived**, not accepted: `compilerName`,
`compilerVersion` and `compilerBuild` are copied from the named paths of the admitted
retained context and the dialect is `{sourceVariant}` from the closed longest-suffix
table. The actual **body language** is the language of the body, not of the provider.
An unlisted suffix (`.vue`) refuses `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN` rather
than being folded into a neighbour.

**File-fact Run with the full inventoried join.** `file@enumerated` payloads were
joined to the snapshot inventory on `path`, `contentSha256` **and** `byteLength`,
with the bytes retained and re-hashed and every anchor required to lie in the very
file the payload claims. Negative vectors: a foreign content hash and a path in no
snapshot (a pruned `node_modules` path) both refuse.

**Clone body identities at L0 and at a normalized level.** At `L0-verbatim` the host
**recomputes** the payload from the enclosing fact's own anchor span — a real source
join, which my closure performs. At `L1-lexical` it verifies retained preimage custody
plus the framed-identity check and well-formed `u32be count || (u16be kind || u32be
value)*` stream framing, and judges no tokenisation. Level-specification custody is
real: `normalisationVersion` is the raw SHA-256 of the **retained** level-specification
bytes and `levelVersion` enters the frame as the **raw 32 digest bytes**, never the
hex text; `languageVersion` is the raw 32 bytes of `SHA-256(C(body-language-version))`,
which is what keeps every component inside the inherited `u8` length.

**Rust: a mixed-edition workspace with a target-specific override.** 21 crates, three
editions (2015 / 2018 / 2021), a valid `#` marker directory
(`crates/v#1/Cargo.toml`, whose `unitId` is `H` over the published four-field
`UnitIdentityV1` preimage and therefore needs no delimiter and no path restriction),
and a `bin` target carrying `targetEdition: 2018` while its package `core_lib`
defaults to 2021 — so a package map whose values all agree still does not determine a
body's dialect, and there is no fast path.

| Selection | `crates/core_lib/src/shared.rs` dialect | body identity |
|---|---|---|
| `lib-only` | `{edition: 2021}` | `sha256:12d721d6…` |
| `lib-plus-test` | `{edition: 2021}` | `sha256:12d721d6…` (**stable**) |
| `bin-only` | `{edition: 2018}` | `sha256:7851a9b3…` |
| `both-targets` | — | `BODY_LANGUAGE_OWNER_AMBIGUOUS` |

All four selections mint **four different `sourceUniverse` identities**, which is
exactly what makes the same physical file under two explicitly selected target
editions representable: two analyses, one selection at a time, and the ambiguous
*unselected* request refuses. No relation payload changed. Bodies of 2015, 2018 and
2021 all close **in the same universe** — the ordinary mixed-edition workspace has a
representable valid form. Under `bin-only`, `crates/core_lib/src/lib.rs` refuses
per-body as `BODY_LANGUAGE_OWNER_NOT_SELECTED` while the clones Coverage stays
**`complete`**, exactly as §10 says a deliberately excluded selection should.

**Enumeration completeness is not resolution completeness, and neither invents a
resolved rung for file facts.** `file@enumerated` is a one-rung relation and its
Coverage carries `resolutionCompleteness.state: not-applicable`, which RC-1 says is
*not* `complete` — it makes no resolution claim at all. I did not mint a resolved rung
for any inventory relation.

**Ambiguity and partial enumeration.** With `enumeration: partial` the dialect refuses
**before any row is read**, so incomplete discovery can never act as an implicit
edition selection. The result is an **empty clone view that does not claim complete
Coverage**: zero clone facts, `coverage: unknown`,
`deficiency: input-closure-incomplete`, `nativeCause: body-language-owner-unenumerated`,
and the Run still closes as authoritative-indeterminate rather than voiding. My
closure **re-derives** that pair independently and refuses a false `complete`
(`COVERAGE_DIALECT_PREREQUISITE`), an undisclosed null, a wrong deficiency and a wrong
cause — the four separable refusals §10 requires. The three ownership states map
exactly:

| Selection-law refusal | deficiency | nativeCause |
|---|---|---|
| `BODY_LANGUAGE_OWNERSHIP_REQUIRED` | `input-closure-incomplete` | `body-language-ownership-missing` |
| `BODY_LANGUAGE_OWNER_UNENUMERATED` | `input-closure-incomplete` | `body-language-owner-unenumerated` |
| `BODY_LANGUAGE_OWNER_AMBIGUOUS` | `input-closure-incomplete` | `body-language-owner-ambiguous` |
| `BODY_LANGUAGE_OWNER_NOT_COMPILED` / `_NOT_SELECTED` | *(none — per-body, compatible with `complete`)* | *(none)* |

**Compiler-free syntax-only Runs, all three classes.**

* *Supported code grammar*: a repository with `.rs` files and **no `Cargo.toml`
  anywhere**. The bundled Rust grammar is selected; inventory facts, `declares@syntactic`
  and `clones@normalized-body-hash` all admit; `body-language-version` binds
  `compilerName: opensip-grammar-parser`, `parserVersion` joined to the grammar
  closure manifest's `semanticVersion`, dialect `{grammarVariant: "rs"}`. The two
  `.rs` bodies with identical spans group. Crucially, the grammar-parsed identity
  (`sha256:43c6ed9b…`) is **not** the compiler-parsed one — a grammar parse and a
  compiler parse are different interpretations and never equate.
* *Already-bundled data/document grammars* (`json`, `toml`, `markdown`, `yaml`): the
  declared **inventory** capability is available and never grammar-gated, so the
  `file@enumerated` Coverage is genuinely `complete`; `clones@normalized-body-hash`
  and `declares@syntactic` are **disclosed unavailable** —
  `coverage: unknown`, `deficiency: language-tier-unsupported`,
  `nativeCause: capability-missing` — never answered and never refused outright. A
  **complete empty clones Coverage over a data-only repository refuses**
  (`SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`), so a complete empty result cannot conceal
  unsupported analysis.
* *Unsupported grammar*: a `.py` file has no bundled grammar, stays
  `unsupported-file / no-bundled-grammar`, and no TypeScript compiler is silently
  assumed. This is the vector that exposed **CB4-MUST-1**.

I verified the code-versus-data distinction against the published matrix and the
body/normalizer laws rather than assuming it: `x-opensip-grammar-capability-registry`'s
`code` subset is exactly the `body-language-version.languageId` enum, the four
`data-document` languages are disjoint from it, one suffix maps to one grammar across
14 suffixes, and every semantic rung is `UNSUPPORTED-TYPED` for `syntax-only` in the
matrix (verification `L7`, `L6`). An **unselected** grammar lends no capability: a
bundle shipping a Rust grammar the universe did not select cannot make
`clones@normalized-body-hash` available for `.rs` files, and a Markdown-anchored code
fact refuses in a *mixed* repository exactly as in a data-only one.

**Negative vectors, per language, all 23 refusing with a typed cause.** TypeScript: a
stdlib merkle root naming no retained closure; a compiler version not from the manifest;
a config-graph path outside the snapshot; a partial declaration inventory for the same
retained library; a universe field contradicting the admitted context; a Rust-minted
context offered as the TypeScript one; a file fact with a foreign hash; a file fact
naming a path in no snapshot. Rust: a `rustcDevLlvmDigest` naming no retained
`kind=rust-dev-llvm` closure; a tool digest outside the named signed closure tree; a
replaced `.cargo` config outside the snapshot. Graph-wide: a **hidden** hash-valid
native context reached by no Plan; a Plan naming an unretained context; a `declares`
fact carrying `resolved-callee` (a rung of `calls` — schema vocabulary is not relation
membership, and there is no empty-ladder fallback); a `same-only` universe violation;
a `clones` fact with two anchors; an import cited but not Plan-selected.

**Imports.** One real `import2` wrapper over the workflow-owned canonical
`RuntimePayloadV1`, with `payloadSchemaDigest` = the raw SHA-256 of the **entire**
`imported-evidence.schema.json` document, every auxiliary digest the raw SHA-256 of a
retained closed record, `blobs: []` (lawful — the payload and the registered schema
document are retained independently), and the Plan carrying `read-import`. The
observation boundary is preserved: `observed-hit` is positive evidence,
`observable-unhit` is **bounded negative** evidence within its window and population,
`unobservable` and `unmapped` are never unhit signals, one window never establishes
universal non-use, and runtime coverage is never OpenSIP Coverage. A clean commit name
plus a declared build string alone never map (`IMPORT.SOURCE_MAPPING_REQUIRED`).

**Native dependency/configuration `H` preimages, rebuilt from the recipes.**
`native.dependency-file-manifest.v1` over the sorted `[{path, contentSha256,
byteLength}]` rows; `native.dependency-source-set.v1` over the closed set, with a
vendored registry package correctly recorded `self-consistent` / `declared` rather
than `registry-authenticated` (DS-1: a self-asserted `.cargo-checksum.json` proves
nothing about the files); `native.unified-features.rust.v1`;
`native.compilation-unit.v1`; and — the one that is easy to conflate — the **three
distinct** digests of one `CargoConfigProjectionV2`: its own `projectionSha256` (the
raw bytes of the projected `.cargo/config.toml` file), the universe's
`configProjectionSha256` (the 64-hex suffix of
`H("native.cargo-config-projection.v2", record)`), and the raw SHA-256 of the
canonical record, which is **neither**.

### 3.3 Workflows, audit and authorization (`vectors/v3-workflows.json`, `v4-audit.json`)

**Baseline audit and comparison.** A genuine `CODE-NET-NEW` gating under
`code-regression`; a regression hidden by a same-change policy edit staying
`CODE-NET-NEW` with `subsequentDeltas: [policy]` and `gateReason:
code-net-new-policy-hidden`; a removed detector forcing `INDETERMINATE` with
`pivot-detector-unavailable`, because `E0` is never substituted with `B`; an
evidence-availability change on a gating rule forcing `INDETERMINATE`; and an
**empty-result** comparison — zero entries, both observed finding sets empty — that is
still `indeterminate` because a required policy re-evaluation was unbound and a gating
rule's coverage is unknown. Every descriptor validates against
`comparison-result.schema.json#/$defs/ComparisonDescriptor`.

**A real `ScopeDocumentV1` bound into the retained analysis spec.** Using the exact
registered `parameter` row
(`identity-schemas.v2.json#/x-opensip-payload-registry/classes/parameter/rows/
"workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"`), the
parameter's `schemaDigest` is the raw SHA-256 of the **full** policy-document
document bytes and its `payloadDigest` is `raw SHA-256(C(ScopeDocumentV1))`. I then
built a comparison in which **only that scope policy changed**: `policyDigest`,
`waiverSetDigest` and `detectorClosureIds` are equal on both sides, so the first
axis at which the fingerprint changes is **scope (E2 → E3)**. Both Plans carry the
**identical** `plan.scopeDigest` — the foundation `scope-descriptor`, the repository
extent actually walked by discovery — while their `analysisSpecDigest`s and therefore
their PlanIds differ. The two scope records stay different things throughout, which
is the whole point of the row. A real but unregistered parameter document refuses.

**Complete pinned-purge refusal.** `request-rejected` / `REQUEST.PRECONDITION_FAILED`
/ exit 2, carrying the closed `common.schema.json#/$defs/PinnedPurgeDisclosure` with
the **complete** three-pin inventory sorted uniquely by `pinId` and the three ordered
consequences, validated end to end through `StepTermination`. A `purgeDisclosure` on
any other detail code refuses. I also recorded the honest boundary the contract itself
draws: a **truncated** pin set is schema-valid, so schema validity is not inventory
completeness — the host must compare against the complete set observed under the
exclusive purge lease, and that obligation cannot be discharged by the schema.

**Thirteen public termination examples**, each validated against `StepTermination`
with its `DomainDetail` code checked for membership of the single closed
`public-detail-registry.v1.json` (283 records, mirrored exactly by the common-schema `DomainDetailCode` enum, plus 7 internal aliases that are never public enum values), covering success, both
`policy-failed` branches (authoritative with `runId`, ephemeral with
`authority=ephemeral` and **no** `runId`), the four `evidence.*` details at their two
distinct event positions (pre-evaluation `request-rejected` exit 2 versus
during-operation `HOST.IO_FAILURE` exit 4), authoritative-indeterminate exit 3 with a
`coverageId`, **required output failure after commit**
(`DELIVERY.REQUIRED_FAILED` / `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` / exit 4, RunId
retained, Run never rewritten), `PROVIDER.PROTOCOL_VIOLATION`,
`storage.backup-choice-required` in CI, doctor-with-defects at exit 0, and interrupt
after commit. Five negative terminations confirm the branch contract is
schema-enforced, including an internal alias (`native.too-many-units`) refusing as a
public code.

**Cache key versus cache hit.** Key construction is pure — exact schema admission and
canonical order over the `cache-key` record, no bytes read, no reference resolved —
and the same record under the `regeneration-key` domain gives a different identity.
Admitting a *hit* requires the Run's whole closure, and a bare
`coverage-payload`/`import-payload`/`fact-payload` reference is refused as an
authoritative root rather than resolved by guesswork. A regeneration mismatch is the
operational `evidence.regeneration-mismatch` refusal, never a replacement for the
sealed Run.

**Explicit test / preparation / repair authorization.** A `test-runner` grant with
`owners: []` and `ownerSourceDigest` = the digest of the canonical empty owner array,
bound to project, snapshot and the exact argv digest, `policy-record` consent in CI,
effects **disclosed** and equal to the pinned truth table. A test-execution step has
**no Plan**; `test-code` is not a semantic-grant operation and a test-runner grant is
projected by nothing. Preparation: `AuthorizedExecutionV2` is a preflight descriptor,
the authority is the operational `authorizationRef` excluded from Plan and every
content identity, `host-prepared` projects `prepare-code` while `imported-inert`
projects only `read-import`, and inert row kinds are closed to three with a media type
that is a label and never a trust proof. Repair apply is host-brokered **first-party**
mutation with `repositoryExecution` constant `false`, a separate authorization record,
a closed journal and a closed recovery table in which rollback never consults recipe
trust while commit does.

**Minimum-resolution predicates at syntactic, resolved and type levels.** Satisfaction
is ladder-index comparison **inside one relation**: `declares@syntactic` qualifies for
`minResolution: syntactic`; `references@syntactic-name-match` is insufficient for
`resolved-binding`; `calls@syntactic-callee-name` is insufficient for
`resolved-callee`; `types@annotated` is insufficient for `checked`. A cross-relation
comparison (`declares` fact against `minResolution: resolved-binding`) is an
**admission refusal**, never a true or false predicate — the withdrawn abstract
tiers and the global rank table are not used anywhere in my model. RC-2 is exercised
across all five states, confirming a **zero** unresolved-edge count never implies
`complete`. The corresponding repair `EvidenceRequirement` rows and the
`deadCodeRepairEligible` prerequisites are constructed and validated.

### 3.4 Mechanical re-checks of the contracts' own claims (`vectors/v5-law-checks.json`)

Nine of eleven hold; the two that fail are the evidence for CB4-MUST-2 and CB4-ADV-1.

| Check | Result |
|---|---|
| **L1** closing digest law: all 58 64-hex occurrences in `identity-schemas.v2` annotated | **holds** |
| **L2** relation document annotation law; joins name existing selector fields; `not-joined` exemptions declared | **holds** (`vcs-change.previousPath` is the one declared exemption) |
| **L3** ladder mirror drift, exactly and **in order**, 13 relations | **holds** |
| **L4** `Rung` enum == union of the ladders; imports introduce no new rung token | **holds** (15 rungs, symmetric difference empty) |
| **L5** every §10 Cause-column value representable in `NativeCause` | **FAILS** → CB4-MUST-2 |
| **L6** matrix cell count matches the prose | **FAILS** (66 vs 60) → CB4-ADV-1 |
| **L7** grammar `code` subset == `body-language-version` enum; data disjoint; one suffix one grammar | **holds** |
| **L8** import wrapper mirror differential over order annotations, blob min/max, path grammar and byte bound, with a discriminating negative floor | **holds** — both documents now agree at every boundary (`0..4096` blobs, `canonical-set` omissions, `path`-ordered blobs) |
| **L9** `ExecutionId` non-equivalence: retained C-2 pattern really does end in a bare `$`; both successor spellings identical | **holds** |
| **L10** the four repository-code effect values against the pinned v9 table | **holds** (values correct; see ADV-3 on the mapping) |
| **L11** domain-set registry completeness: three universes, three contexts, every one with a binding, a context domain and a `languageVersionBinding` | **holds** |

---

## 4. Issues

### MUST

**CB4-MUST-1 — anchor cardinality for inventory and symbol facts is undecided, and
under a syntax universe the two lawful readings differ in admissibility.**

Selectors:
`identity-schemas.v2.json#/$defs/fact/properties/anchors` (no `minItems`, no
per-relation cardinality);
`relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/clones/
bodyIdentityJoin.anchorCardinality` = 1 (**the only** relation given one);
`.../relations/file/snapshotJoins[0].anchorPathField`;
`native-evidence.md` §1.2 "Every admitted fact" and "Every requested scope";
`native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry.
enforcementBoundaries` (2) and (3).

Boundary (3) says inventory capabilities are **always available and deliberately not
grammar-gated**, so a `file@enumerated` Coverage over a snapshot containing
`tool/main.py` is genuinely `complete`. Boundary (2) says every anchor path of an
admitted fact must be read by a **selected** grammar, with no inventory exemption. A
whole-file-anchored `file` fact for that path therefore refuses
(`SYNTAX_CAPABILITY_UNSUPPORTED_FACT`), while an unanchored one admits — vacuously
satisfying both boundary (2) and the `file` row's own `anchorPathField` note. The
carve-out sentence "an unanchored **code** fact is not vacuously supported" is scoped
to code facts and leaves inventory facts undecided.

If reading A is intended, an inventoried file exists in a `complete` extent for which
no fact can be minted, so `exists file where path=tool/main.py` is authoritatively
**false**. If reading B is intended, every inventory and symbol fact in **every**
language mode has two lawful spellings with different `fact2` — and therefore
`view2`, `evidence2`, `seal2`, `run2` — identities, which contradicts the stated
property that identical semantic inputs produce the same Run and that independent
replay across machines is checkable. Demonstrated in `vectors/v6-gaps.json#CB4-MUST-1`
with both fact identities computed.

Smallest conformant fix: state the anchor cardinality per relation in the registry
(as the `clones` row already does), **or** exempt the three inventory capabilities
from enforcement boundary (2) exactly as boundary (3) already exempts them.

**CB4-MUST-2 — three of §10's own Cause-column values cannot be expressed by the
closed `NativeCause` enum the `coverage2` record carries.**

Selectors:
`native-evidence.md` §10 deficiency table, rows `resolution-incomplete` (Cause = "the
unresolved edge classes; `partial`/`not-attempted` stage"), `external-consumers-unknown`
(Cause = `exports-open`, `exports-unknown`) and `derivation-policy-unmet` (Cause =
`compiler-inferred` present);
`native-evidence.schemas.v2.json#/$defs/NativeCause` (closed, 14 members);
`.../$defs/ViewEntryV3/properties/nativeCause` (`NativeCause | null`);
`.../$defs/UnresolvedEdgeKindV1` (closed, 16 members, **disjoint** from `NativeCause`).

The intersection of `UnresolvedEdgeKindV1` and `NativeCause` is empty, and neither
`exports-open`, `exports-unknown` nor `compiler-inferred` is a member. The only
representable value for the most common deficiency in real JavaScript and
non-prepared Rust is therefore `null` — which the enum's **own description** says
"records that a disclosure was owed and not made". That is the identical argument the
three `body-language-*` members were added to answer (CB3-MUST-5), applied to three
further rows and not carried through. The deficiency itself *is* publicly nameable —
`resolution-incomplete`, `external-consumers-unknown` and `derivation-policy-unmet`
are all members of the closed `DomainDetailCode` registry — so it is precisely and
only the cause that is unrepresentable.

Smallest conformant fix: add the members, **or** state in §10 that these rows' causes
travel in `resolutionCompleteness.unresolvedEdgeClasses` and `closedWorld` and that
`nativeCause` is `null` for them by design. Either closes it; leaving the table naming
values the schema refuses does not.

### SHOULD

**CB4-SHOULD-1 — the clones registry's `languageIdSource` contradicts the derived
body-language law and is unrepresentable for the syntax universe.**

Selectors:
`relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/clones/
bodyIdentityJoin.languageIdSource` ("the language of the fact `sourceUniverse` domain
registry row");
`identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/
native-semantic-universe/*/language` (`typescript`, `rust`, **`syntax`**);
`.../languageVersionBinding.bodyLanguageByVariant` and `.bodyLanguageLaw`;
`identity-and-evidence.md` §3 ("the language of the **body**, not of the provider");
`identity-schemas.v2.json#/$defs/body-language-version/properties/languageId`
(enum: `javascript`, `rust`, `typescript`).

Read literally, a `.js` body under a TypeScript universe gets `typescript` — which
identity §3 explicitly forbids — and **any** body under the syntax universe gets
`syntax`, which the closed enum refuses outright. The correct answer is determinate:
the domain row's own `bodyLanguageLaw` and identity §3 agree that it is derived from
the selected variant, and that is what I implemented. This is a one-sentence wording
defect in a **normative registry**, but a literal implementer produces a different
clone identity for every JavaScript body and no admissible identity at all in
syntax-only mode.

**CB4-SHOULD-2 — `analysis-spec.requestedCapabilities[].capabilityId` is
identity-bearing with no named vocabulary authority.**

Selectors:
`identity-schemas.v2.json#/$defs/analysis-spec/properties/requestedCapabilities/items/
properties/capabilityId` (`$ref: #/$defs/Text`, free text);
`native-evidence.md` §1.4 ("the authenticated release declaration registry rows");
`admission-and-qualification.md` §1.1;
`native-capability-matrix.v2.json#/capabilities[].id`.

The field enters `analysisSpecDigest` and therefore PlanId and RunId, but nothing says
whether its value is a matrix capability id (`clones-fact`) or a `relation@rung`
string (`clones@normalized-body-hash`) — both are schema-valid and the §1.3 table and
the Coverage key use the latter. Two conforming hosts requesting the same capability
for the same unit mint different PlanIds, which defeats the stated independent-replay
property. This is a SHOULD rather than a MUST because a single implementation is
self-consistent; it becomes a MUST the moment two must agree on one PlanId. Naming the
release declaration registry with its selector, or constraining the field to the
matrix ids, closes it.

### Non-blocking advisories

* **CB4-ADV-1** — `native-evidence.md` §1.1 says the matrix has 60 cells; it has 66
  (11 capabilities × 6 modes). The matrix is authoritative; the count is stale
  decoration and affects no admission.
* **CB4-ADV-2** — the two prose enumerations of registered identity domains
  (`identity-and-evidence.md` §3 "Both universe domains…"; `native-evidence.md` §11
  "Identity domains authored here") predate the syntax-only universe and omit
  `native.semantic-universe.syntax.v2` / `native.context.syntax.v2`, although §1.2
  registers them and the machine-readable `x-opensip-digest-domains` registry — which
  is what admission dispatches on — carries all three universes with bindings,
  context domains and `languageVersionBinding`s. I dispatched on the registry.
* **CB4-ADV-3** — the four repository-code effect **names** are said to be copied from
  `permission-truth-tables.v9.json`, but that table is over seven closed permission
  **tokens** and the name-to-token mapping is published nowhere. It is determinate by
  elimination and every claimed value verifies (L10); `PT-HOST-EFFECT-BROKERED`
  (`ENFORCED-AT-HOST-BROKER`) is a table value that `EnforcementV1` admits but no
  effect name projects.
* **CB4-ADV-4** — the `parameter` payload-registry class is keyed by the cited
  **document** digest, not the `(document, selector)` pair. The two rows are
  distinguishable today, but the registry law itself has to add an explicit ambiguity
  refusal for a case that keying by the pair would make impossible.

---

## 5. What I had to invent

Only two things, both recorded above as MUST/SHOULD rather than silently absorbed:

1. **Anchor cardinality for inventory facts (CB4-MUST-1).** To build the promised
   "repository with no TypeScript or Rust compilation unit" vector I chose unanchored
   inventory facts for `unsupported-file` paths and whole-file anchors elsewhere.
   Neither is derivable from the kit and the choice moves fact identities.
2. **A `capabilityId` spelling (CB4-SHOULD-2).** I used `relation@rung`. Nothing in
   the kit selects between that and the matrix ids.

Everything else came out of the supplied bytes. Where a choice existed but the
contracts explicitly leave it to implementation, I recorded it as **algorithm freedom
rather than a missing contract** and did not raise it: the concrete normalizer that
produces an `L1`–`L3` token stream (the contracts require only retained preimage
custody plus framing and explicitly qualify no tokenisation); the near-clone shingling
and grouping algorithm (candidate-only, with `matchedEdges` and
`scoreMeaning=minimum-member-best-neighbor` published); query planning (an
optimization only, with a retained full-scan reference that must agree on selected
facts); and the concrete `SubjectIdV1` minting inside a provider (opaque by
construction, with the enumerator's symbol-to-file attribution a **stated** trust
limit rather than an oversight).

I did **not** need to invent: the canonical encoder, the `H` frame, the digest law,
any domain, the `subjectScopeCommitment` recipe, the body-identity frame, the
`body-language-version` derivation for any of the three universes, the Rust ownership
selection order, the syntax capability law, the payload registry, the mutation or
repair keys, the pinned-purge disclosure, or any termination projection.

---

## 6. Limitations

* No product exists to measure and none was assumed. Real OS custody, `fsync`/SQLite
  durability, process death, compiler behaviour, cryptographic verification and
  confinement are **future qualification work** and I did not demand them.
* Every filesystem byte, installed package manifest, compiler/stdlib/grammar tree,
  Cargo target table, provider enumeration and protocol outcome in my vectors is a
  **synthetic TCB observation** — an assumption, never native enforcement proof. In
  particular, `SourceUnitOwnershipV1` states what a producer *claims* it enumerated;
  its truth is not established here, and the contract says so.
* My `close_run` is my own reconstruction of the closure the contracts describe. It
  exercises the joins I could derive; passing it establishes that a lawful graph is
  *constructible*, not that any implementation is correct.
* The finite policy interpreter behind my predicate vectors evaluates a single-atom
  subset. It qualifies neither the declarative language nor any native Coverage or
  relation payload registry.
* I read the five contracts, their normative schemas and registries, and the retained
  inherited artifacts named as normative dependencies. I did not read governance
  records (correction record, readiness register), reviews, author models, fixtures or
  goldens, so I make **no** statement about this design's acceptance standing, grade
  or prior verdicts — only about whether an implementer can reconstruct it.
* Passing this reconstruction is not product qualification and confers no
  implementation authorization.

---

## 7. Verdict

The design is very close to reconstructable end to end, and materially more so than
the surface area would suggest: the closing digest law, the single ladder authority,
the `subjectScopeCommitment`/`scope2` unification, the per-selection Rust dialect
record and the syntax-only universe are all genuinely closed, and I could exercise
each of them adversarially without inventing a recipe. The two mirror pairs that a
differential could have caught now agree at every boundary I tested.

It is **CHANGES_REQUIRED** because two gaps force invention at the exact points the
contracts stake their strongest claims. CB4-MUST-2 leaves a *mandated* disclosure
unrepresentable for the most common deficiency the product will emit, by the same
argument the contracts already accepted once for a neighbouring case. CB4-MUST-1
leaves the fact set of an ordinary repository — and therefore its `run2` — undecided
between two lawful readings, one of which makes an advertised capability
unrepresentable and the other of which breaks the determinism property the whole
identity graph exists to provide. Both are small, local and closable by a sentence
each; neither is a structural problem with the design.

**newMustIssues:** `CB4-MUST-1`, `CB4-MUST-2`
**newShouldIssues:** `CB4-SHOULD-1`, `CB4-SHOULD-2`
**Advisories (non-blocking):** `CB4-ADV-1` … `CB4-ADV-4`
