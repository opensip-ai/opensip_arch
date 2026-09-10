# Identity, authoritative evidence, and retention

Standing: product successor authored by Codex, with review and application
standing governed by the [correction record](../../../coop/design-corrections/README.md)
and central readiness register. This is the Phase-1A packet for the intended
product, not a repair of the historical preview's acceptance record. The
machine-readable descriptors and reference semantics are in
[foundation](../../../coop/design-corrections/foundation/). Every `schemaVersion`
in the new semantic identity graph is 2. Old identifiers remain old identifiers.

## 1. Authority and applicability

The host admits inputs, mints identities, evaluates policy through the pure
evaluator, verifies its result, and commits evidence. Native providers, imported
observations, model suggestions and stored caller-supplied identifiers do not
have evaluation or custody authority. Signed software provenance does not prove
that an algorithm is correct; the selected, authenticated first-party host and
pure evaluator remain in the TCB. No Python introspection guard or caller's
`verified=true` is an authority mechanism.

This contract prospectively replaces the Run/evidence/Plan/source/view/finding/
proof/cache/regeneration recipes and their parks in freeze §7.1,
`evidence-identity-recipes.v5.json`, `evaluation-proof.v8.json`'s claim-shape
lineage and `evaluation-proof.v13.json`'s provenance lineage. Neither evaluation
candidate becomes retrospectively applied. It replaces the Phase-1A and
retention-result join missing from `evidence.v15.json`, and consumes the
CD-RT-5 posture implemented by `retention-tiers.v28.json`. It supplies the
identity-dependent parts of R-1, trusted-request context and OPERABILITY G19.
Precise residual dispositions and source pins are in the integration record.

Unchanged inherited constraints: no ambient provider reads; sealed snapshot;
complete protocol transaction plus successful process exit and EOF before facts
are admitted; pure deterministic evaluation; one host writer; deny-by-absence
permissions; lifetime-neutral semantics. Existing relation payload schemas can
be referenced by exact digest. Their historical FactRecord1 wrapper cannot bind
a snapshot2 identifier; product FactRecord2 is an explicit successor.

## 2. Tenant and operational identity

ProjectId retains PROJECT-ID-V1: `prj1-` followed by 64 lower-case hex digits,
32 host-CSPRNG bytes. The untracked `.opensip/project-id.v1` marker and the
private host registry must agree exactly. A private namespace UUID is an
operational storage locator, bound one-to-one to ProjectId; it does not enter
semantic identities. The host verifies marker, root identity, owner, no-follow
handles and registry binding before any project writer. Missing marker and
registry is first use; agreement is reuse; either unilateral or contradictory
presence is an admission refusal requiring explicit recovery/adoption. It never
silently chooses one identity. Discovery and admission use the security unit's
root boundary.

An ordinary fresh clone gets a fresh ProjectId. Explicit adoption from an
admitted portable project bundle preserves a ProjectId after showing its source
and target; it never imports another machine's local authorization, credentials,
leases or execution receipts. A fork gets a new ProjectId and explicit origin
metadata. A root move preserves ProjectId only through an authenticated registry
move with no live writer; duplicate simultaneous roots for one local namespace
refuse. Read-only comparison of two tenants does not merge their stores.

Invocation identity is RequestId (`req1_` plus 32 lower-case hex digits), minted
before admission and retained for refusal as well as success. Each admitted
attempt receives a fresh ExecutionId (`exec1_` plus 32 lowercase hex digits).
`c2-plan-stage-schema.v4.json` `planIntent.wireTypes.executionId` is the C-2
owner selector for EXECUTION-ID-V1 **provenance** — where the identifier and its
uniqueness discipline come from — and it is not byte-equivalent to the product
successor grammar. Its pattern ends in a bare `$`, so it admits
`exec1_<32 hex>\n`, which `admission-and-qualification` §1 declares malformed and
which `common.schema.json#/$defs/ExecutionId` refuses. The **product successor
grammar is end-anchored**: `^exec1_[0-9a-f]{32}(?![\s\S])`, exactly as
`identity-schemas.v2.json#/$defs/commit-receipt/properties/executionId` and the
workflow `ExecutionId` spell it, and a trailing newline, carriage return or space
is refused rather than trimmed. RequestId is `^req1_[0-9a-f]{32}(?![\s\S])` on the
same rule. This is the same deliberate non-equivalence security §S9.1 states for
`RootV1`: the retained selector remains the immutable provenance record, the
successor is what admits.
Both RequestId and ExecutionId use independent 16-byte host-CSPRNG draws, reserved
with uniqueness checked in the corresponding operational ledger before use.
Caller-supplied IDs and reuse are refused; neither is derived from a content hash.
This prospectively settles RES-C2V4-01 ownership in the shared identity contract.
StepId is the zero-based integer position in the invocation's ordered DAG.
Retry always receives a new ExecutionId. These identities, wall clocks, PIDs,
credentials, authorization nonces, receipts and output destinations are
operational and excluded from Run identity. Identical semantic inputs can
produce the same Run on two attempts; attempts remain separately auditable.

## 3. Exact canonical encoding and identity preimages

The authoritative schema is `foundation/identity-schemas.v2.json` (closed
Draft 2020-12 records); semantic joins below are equally mandatory. JSON Schema
alone does not establish exact numeric admission. Before deserialization loses
lexical information, reject duplicate keys, floating/exponent tokens, `-0`,
nonfinite tokens, malformed UTF-8 and non-scalar Unicode. Integer range is
[-2^63, 2^64-1], booleans are distinct, and every field has its narrower schema
bound. Maximum descriptor is 4 MiB and nesting depth 32: the root container
counts as 1; scalar leaves and object keys add no container depth. Byte inventories may
name larger independently bounded blobs. A descriptor exceeding a bound is
rejected; it is never truncated into a different identity.

Canonical JSON has UTF-8 byte-ordered keys, no whitespace or trailing newline,
no Unicode normalization, shortest ordinary decimal integers, and unescaped
Unicode scalar characters. Escape quote and backslash, use `\b\t\n\f\r`, and
lowercase `\u00xx` for other U+0000–001F controls; do not escape slash. Arrays are encoded **in their admitted order**: C never sorts, deduplicates or
infers semantics from a field name or `uniqueItems`. The closing default for
any array in a registered payload is an **ordered sequence**, including nested
arrays and raw token arrays. A schema/owning contract may prescribe a stricter
order; its producer constructs that order and admission refuses deviations
before hashing. This separation applies to every auxiliary digest as well as H.

`x-opensip-order` is the machine-readable schema annotation for these orders, and
the closed vocabulary is exactly the one the `x-opensip-order` validator keyword in
`foundation/canonical.py` implements: `sequence` (default); `canonical-set` (strict
ascending canonical item bytes); `canonical-order` (nondecreasing canonical item
bytes, repeats allowed); `utf8` (strict ascending UTF-8 bytes of a scalar string
item); `path` (strict ascending UTF-8 `path`); `numeric` (strict ascending
integers); `ordinal` (contiguous zero-based `ordinal`); `predicate` (strict
ascending UTF-8 `ruleId,subjectId,predicateId` tuple); `ruleId` and `waiverId`
(strict ascending UTF-8 value of that key); and the generic object form
`{"by": [key, ...]}` (strict ascending UTF-8 tuple of those item keys, in the
listed order). All except `sequence` and `canonical-order` also require unique sort
keys; `uniqueItems` alone neither selects nor overrides an order. An annotation
outside this vocabulary refuses rather than passing silently. Explicit owning
schema/contract order takes precedence over the sequence default and must agree
with any annotation. No caller may elect a different order for one schema.

Every array in identity-schemas.v2 carries this annotation: semantic collections
use `canonical-set`, inventories use `path`, dependencies use `numeric`, stages
use `ordinal` and predicate proofs use `predicate`. Inventory paths must be
unique even when two rows have different byte digests or lengths; there is no
tie-break, and duplicate paths refuse before an identity is minted. Configuration
`allowedScopes` preserves declared priority; declaration-signature tokens
preserve grammar order, including repeated tokens. PolicyDocumentV1 and
RuleProgramV1 `rules` preserve their schema's `ruleId` order, never canonical
rule-object order; WaiverSetV1 uses `waiverId`. Other native/workflow arrays
preserve their admitted sequence subject to their explicitly declared ordering
rules. This settles all arrays without an implicit set heuristic.

Text maxLength counts Unicode scalar values, while the descriptor byte cap
remains independent. U+007F and U+2028 remain unescaped. Logical
paths are relative slash-separated scalar strings, without empty, dot, dot-dot,
NUL or backslash segments. Source spans are half-open byte offsets, bounded by
the exact named source blob; they never split UTF-8 characters in text anchors.
Native language identifiers may have their own explicit normalization; that is
a payload property, never an implicit change to this canonical encoder.

For domain D and descriptor X:

`H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(length(C(X))) || C(X))`.

The identifier is the prefix below, a colon, and lowercase H hex. A raw blob
reference uses SHA256 of its exact bytes and its byte length. A semantic
reference must name its domain, not just an untyped hash. No path, display
version or claimed digest substitutes for verified bytes.

| Domain / prefix | Exact semantic content (schema contains field types) |
|---|---|
| snapshot / snapshot2 | ProjectId, sorted source inventory, resolved config, scope and VCS digests |
| closure / closure2 | role kind, signed manifest digest, exact executable/data tree, semantic version, protocol major and platform |
| import / import2 | typed payload/schema, source and build correspondence, producer/adapter closures, blobs, scope, observation and completeness |
| plan / plan2 | snapshot, capability manifest, semantic closures, analysis spec, resolved config, native contexts, imports, policy, waivers, scope, deterministic budget and semantic grant |
| subject-scope / scope2 | snapshot, relation/rung, source/target universes, enumerator closure and complete sorted subject inventory |
| fact / fact2 | snapshot, relation/rung, universes, producer closure, exact relation payload/schema, anchors and confidence millionths |
| coverage / coverage2 | scope, CoverageResultV3 payload and exact schema digest |
| view / view2 | Plan, scopes, facts, Coverage, producer and schema closure |
| execution-plan / exec-plan2 | Plan and ordered acyclic derivation stages, each with exact stage spec, dependencies and output domains |
| finding-fingerprint / finding-key2 | stable rule name, detector semantics major, logical subject key and related subject keys |
| finding / finding2 | fingerprint, exact rule closure, subject, message code/parameters, severity and evidence references |
| proof-bundle / proof2 | Plan, derivation plan, evaluator closure, rule program, admitted evaluation input references, predicate proofs, findings and verdict |
| semantic-evidence / evidence2 | Plan, views, Coverage, imports, findings and proof |
| evaluation-seal / seal2 | Plan, derivation plan, evidence, evaluator, policy, proof and verdict |
| run / run2 | ProjectId, snapshot, Plan, evidence, evaluation seal and capability manifest |
| cache-key / cache2; regeneration-key / regen2 | Plan, exact producer, stage spec, scopes, inputs and output schema |
| policy-derivation / policy-derivation2 | Plan, proof, policy, waivers and verdict |
| quality-difference (unprefixed operational digest) | G13 independently recomputed expected/actual observation difference; never Run authority |

The graph is acyclic: proof does not include EvidenceId or RunId; evidence may
include proof; seal includes both; Run includes seal. A finding fingerprint
excludes line offsets, messages, timestamps and concrete evidence, but includes
a discriminator for otherwise indistinguishable logical subjects. The host
refuses an ambiguous key; it does not suffix it by encounter order. The native
subject adapter supplies declaration-signature tokens in grammar order, preserving
language/kind, qualified binding name, generic arity and parameter/type signature
syntax, excluding body and positions. `discriminator` is raw SHA256 of their
canonical JSON **ordered** string array (grammar order, repeated tokens retained). The selected detector closure defines the token
projection. Identical signatures within one logical-name collision class are
ambiguous and refuse correspondence; anonymous subjects without a unique enclosing
name/signature remain unmatched. A changed signature may change the key. This is
syntactic correspondence, never semantic equivalence. Renames
require explicit subject correspondence; a stable fingerprint is not proof of
unchanged detector semantics. Schema/domain changes require a new identifier
major and reviewed migration, not a permissive parser.

Finding citations cannot introduce extra authoritative input roots. Fact and
Coverage citations must belong to an evaluated view; import citations must be
both selected by Plan and listed in evaluationInputRefs; predicate-witness
citations must name a witness of this proof; raw blob citations must be explicit
blob inputs to this evaluation. Every evaluated import must belong to Plan even
when no finding cites it. A well-formed, hash-valid object outside this closure
is refused, rather than admitted as hidden finding evidence.

CapabilityManifestId uses the inherited applied producing recipe and exact
schema: it is 64 lowercase hex characters without a prefix. Its separate
CVE1 producing encoder is fully defined by
`docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`
(eight closed types and exact tags/lengths); that normative dependency must be
provided to a release-builder or blind consumer. CVE1's already-NFC string
admission applies to the capability manifest only and does not change C's
no-normalization product descriptor profile. Plan carries
`capabilityManifestBytesDigest` (raw SHA256) as well as capabilityManifestId.
The host validates the committed CVE1 artifact under the effective
value-domain registry and recomputes capabilityManifestId as
SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes).

**The effective registry is selected here, by name.** It is
`docs/coop/design-corrections/native/capability-manifest-domains.v2.json`, the
current successor of `delivery.v4.json`'s
`capabilityManifestIdentity.valueDomains`, and it supersedes those `valueDomains`
**within its own declared scope and nowhere else**. Native-evidence §11 lists the
same document, so the selection is stated by both owning contracts rather than
asserted by the registry about itself. That scope is exactly two relation
registries: `RELATION-DOMAIN-V2`, which carries the thirteenth relation
`unresolved-edge` (native §4.4) that the inherited twelve-member relation domain
of `fact-plane.v1` cannot express at all; and `RELATION-LADDER-DOMAIN-V2`, a
declared mirror of the single ladder authority
(`foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry`,
drift-checked exactly and in order, below), so a rung of another relation is
refused rather than admitted as a live vocabulary token. **No other
value domain is widened by this selection** — platform ids, deficiencies,
coverage state and every position declared OPEN keep the inherited membership
they already had. Everything the successor reproduces verbatim stays the
inherited artifact's and is not restated here: the CVE1 encoder and its
`resolved-inputs.v2#planIdContract.canonicalValueEncoding` selector, this
identity recipe and its `opensip.capability-manifest.v1` domain, and all four
admission gates in their inherited order — **ADM-TYPE** (exact JSON type before
any content comparison), **ADM-CLOSED** (every reachable record closed; a map is
not a record), **ADM-DOMAIN** (every scalar either bound to a named registry or
declared open, with no third state) and **ADM-ORDER** (every ordered collection
already in its declared canonical order). The inherited `delivery.v4.json` and
`fact-plane.v1.json` **bytes are unchanged** and remain the historical record;
selecting a successor registry is not a rewrite of the artifact it succeeds.

`TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot` and
`NativeContextV2.toolchain.rustcDevLlvmDigest` (inside the Rust
`ToolchainIdentityV1`) are the 64-hex suffixes of
`closure2` identities for `kind=stdlib` and `kind=rust-dev-llvm`, respectively.
Both complete descriptors and trees are retained and joined to the selected
compiler/toolchain; these are explicit successor recipes despite the retained
field names, never reinterpretations of a historical Plan. They are never read
from an unverified worker claim. `closure.manifestDigest` is raw SHA256 of the
admitted component manifest body bytes encoded with the security metadata
profile, excluding the signature envelope; the signed envelope and verified
role/namespace join are retained as operational provenance. A manifest for a
different tree, platform or selected component is refused by delivery admission. They enter the native-context
payload, hence Plan. Closure tree hashing includes relative path, byte length
and digest for every selected file. A semantic version alone is not a closure.

The native `subjectScopeCommitment` is `"sha256:"` plus the 64-hex suffix
of the exact admitted `scope2` identity, using H("subject-scope", descriptor).
It is another textual form of the **same** digest, not a separate hash of the
subjects or of the scope identifier string. Its retained descriptor includes
snapshot, relation/rung, source/target universes, enumerator closure and sorted
unique subjects. `subjectCount` is exactly that inventory's length. The native
Coverage admission boundary joins both key/entry commitments and count to this
host-owned scope descriptor and mints `coverage2.scopeId` from that same scope;
a mismatched provider claim mints neither Coverage nor Run (native §4).

Native contexts have explicit H domains: `native.context.typescript.v2` over
TypeScriptNativeContextV2, `native.context.rust.v2` over NativeContextV2, and
`native.context.syntax.v2` over the installed grammar bundle (native §1.2).
Native records carry `sha256:<H hex>`; `plan.nativeContextDigests` carries the
sorted unique bare 64-hex suffixes for selected, admitted contexts. These are
**H digests**, not raw SHA256 of context JSON. Native universe identities follow
native §11's own H domains — for example `native.semantic-universe.typescript.v2`
over TypeScriptUniverseV2ResolvedInputs — and `fact` and `subject-scope`
`sourceUniverse`/`targetUniverse` carry its bare 64-hex suffix. A native
`sha256:` text form is never a foundation typed Ref domain.
When a field specifically names a raw payload digest, raw SHA256(C(payload))
is retained separately and cannot substitute for either H identity.

Both of these are `h-identity` fields, so the object retained under each is the
exact H preimage frame, and Run closure admits it by parsing that frame rather
than by trusting a producer's claim or an ADMIT flag. **A frame proves retention,
never admission.** Frame parsing alone would let a claimant re-frame a context
the native boundary refuses and still mint a Run, so Run closure additionally
**re-runs the owning contract's own admission over the retained bytes**: the
native context admission of native §2.3/§2.4/§3/§14 (reference entry point
`admit_native_context`) against the Run's own retained `closure2` descriptors and
trees, and the universe binding of native §11 (reference entry point
`bind_typescript_universe`) against that admission and those exact context bytes.
Any refusal either returns is a Run admission refusal, reported with the native
contract's own typed refusal string. The registry rows in
`x-opensip-digest-domains.domainSets` name the language, the admission entry
point and the joins for each domain. Nothing is re-executed: no compiler, cargo,
provider, repository or filesystem operation runs at Run closure; the admission
is re-decided over retained descriptors alone.

Beyond that, the closure re-derives the joins this contract names, from the
retained frame: `toolClosure.closureId` must be a retained `closure2` of kind
`toolchain`; `TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot` and
`NativeContextV2.toolchain.rustcDevLlvmDigest` must, prefixed with `closure2:`,
name retained closures of kind `stdlib` and `rust-dev-llvm` respectively, whose
recomputed identities equal them and whose complete trees are retained; the
recomputed context identity must equal the Plan's bare-hex member and the
recomputed universe identity must equal the field that named it; the set of
retained context frames must equal `plan.nativeContextDigests` exactly, so a
context reached by no Plan is refused and a Plan naming an unretained context
cannot close; and every retained universe frame's `nativeContextId` must be
`sha256:` plus a member of `plan.nativeContextDigests`, so a universe cannot bind
a context this Plan did not select.

The native-context and native-universe source correspondence that this section
already requires to agree with the snapshot is discharged here rather than
assumed: every repository path a context or universe names must be an inventoried
snapshot path (`TypeScriptConfigProjectionV2.configGraphPaths`,
`CargoConfigProjectionV2.replacedSnapshotConfigs`,
`RustUniverseV2ResolvedInputs.crateRootPaths`), and a named lockfile
(`TypeScriptNativeContextV2.lockfileIdentity`,
`RustUniverseV2ResolvedInputs.lockfileIdentity`) must name an inventoried path
whose inventory digest equals its `contentSha256`. A context or universe
describing configuration, crate roots or a lockfile that is not in the analysed
snapshot cannot enter a Plan.

**All three** universe domains native §11 registers are registered here:
`native.semantic-universe.typescript.v2` over TypeScriptUniverseV2ResolvedInputs,
`native.semantic-universe.rust.v2` over RustUniverseV2ResolvedInputs, and
`native.semantic-universe.syntax.v2` over the grammar-only universe of native
§1.2. This sentence and native §11's list both predated the syntax-only universe
and named two; the machine-readable `domainSets` registry — which is what
admission and the closure checker actually dispatch on, complete with each
domain's binding and `languageVersionBinding` — has carried three throughout, and
these lists are now that registry. A
universe must bind a context of **its own language** — the bound context's H
domain must be the one its registry row names, in either direction — and every
identifier the two records both carry must be equal; for Rust that is
`dependencySourceSetId`, `unifiedFeaturesId` and `preparedOutputSetId`. Each
domain names its owning binding — `bind_typescript_universe` (native §11),
`bind_rust_universe` (native §2.1/§11) and `bind_syntax_universe` (native §1.2) —
and Run closure re-runs it over the
retained universe, the retained context bytes, the retained nested input records
and the snapshot inventory, exactly as it re-runs `admit_native_context`. Where
the owning contract registers a domain but supplies no binding for it, a universe
of that domain is **refused with a typed named cause**
(`NATIVE_UNIVERSE_BINDING_UNAVAILABLE`), never admitted unbound: an unfinished
owner obligation must not become a weaker admission.

**Nested native semantic identities are records, not opaque strings.** A native
context or universe names further H identities, and each is admitted the same way:
retained as its own frame, parsed, validated under the record its domain
registers, and re-hashed. `native.dependency-source-set.v1`,
`native.unified-features.rust.v1`, `native.prepared-output-set.v3` and
`native.cargo-config-projection.v2` are registered here for that purpose, and the
chain continues to raw bytes: a dependency package's `fileManifestSha256` is a
`native.dependency-file-manifest.v1` identity whose every row's `contentSha256`
must be retained with exactly its declared `byteLength`, and every inert
prepared-output row's blob must be retained with exactly its declared length.
A semantically required dependency identity is never admitted merely because an
outer frame hashes.

`CargoConfigProjectionV2` carries **two** digests that are not interchangeable:
its own `projectionSha256` is the raw SHA-256 of the projected `.cargo/config.toml`
file bytes, while `rust-v2.configProjectionSha256` is the 64-hex suffix of
`H("native.cargo-config-projection.v2", CargoConfigProjectionV2)` over the whole
record. Both are retained; neither substitutes for the other, and neither is the
raw SHA-256 of the canonical projection bytes.

**Prepared products are inert data; execution authority stays operational.** A
universe's `preparedResolution` projects the grant operation the native contract
names — `host-prepared` requires `prepare-code` and `imported-inert` requires
`read-import` in the Plan's semantic grant — and a universe that consumed prepared
products without it refuses. Retained prepared bytes never imply an execution
grant, `executionCapableResolution` is a statement about what the resolution
consumed rather than a permission, and an unselected prepared set stays absent:
bytes in custody do not enter a resolution by being in custody.

### The closing digest law

Arrays have a closing default; so do digests. **Every 64-hex field in
identity-schemas.v2 has exactly one representation and one retention mode**,
declared field-by-field by the machine-readable `x-opensip-digest` schema
annotation. There is no residue: a 64-hex field carrying no annotation is
inadmissible, and a producer may not choose a representation for it. Nothing in
this graph infers a digest's meaning from a **field name**: a `Digest` spelling,
a `sha256` key or a bare hex string carries no meaning by itself, and two fields
with the same name have the same recipe only because the annotation says so.
The array law closes by naming a default; this law closes by admitting **no**
default, which is stronger: a new 64-hex field added without an annotation
refuses at admission instead of silently inheriting a plausible rule, so the
omission that produced this paragraph cannot recur unnoticed.

The four representations are closed. They are the closed set of **terminal**
representations: what a digest field's value actually *is*. A reference field
(`Ref`, `ProofInputRef`, `FindingEvidenceRef`) instead annotates
`representation: "by-domain"`, which is a **selector, not a fifth terminal
representation** — it says the value's representation is whatever the sibling
`domain` resolves to through the normative `x-opensip-digest-domains.byDomain`
registry, and every registered domain resolves to exactly one of the four below.
`by-domain` is therefore not admissible as a terminal value, no `byDomain` row may
name it, and an implementer enforcing the four-member terminal vocabulary must
resolve those three fields through the registry rather than refuse them.


| Representation | Meaning |
|---|---|
| `raw-artifact` | raw SHA256 of the **exact retained artifact bytes** — a source or closure-tree file, a committed capability-manifest artifact, a component manifest body, or a complete registered schema document. Not of a canonicalization of anything. |
| `canonical-record` | raw SHA256 of `C(record)` for a **named registered record**. The annotation names it: a `#/$defs/…` record of this bundle, a `{document, selector}` record registered by another unit's pinned schema, a record `registeredBy` a sibling schema-document digest, or the workflow `PayloadRegistryV1` row keyed by an import's `kind` and `payloadDomain`. |
| `h-identity` | the lowercase hex of `H(D, X)` — either a typed object of a domain in the table above, carried with its prefix, or the **bare 64-hex suffix** of a domain in a named domain set. Never raw SHA256 of the payload. |
| `capability-manifest-id` | the inherited CVE1 recipe `SHA256(UTF8("opensip.capability-manifest.v1") ‖ 00 ‖ committedBytes)`, closed to `plan.capabilityManifestId`, `run.capabilityManifestId` and the `capability-manifest` reference domain. |

The four retention modes are closed:

| Retention | Meaning |
|---|---|
| `preimage` (default) | the exact preimage bytes are retained in the content-addressed store **under this digest**; the closure checker fetches them and re-hashes. |
| `fragment` | the preimage is a canonical sub-object of an already retained record; the annotation's `locatedBy` states which record and which addressing rule, and the closure checker recomputes it there rather than storing it twice. Closed to `program-predicate.nodeDigest`. |
| `derived` | recomputed from another retained artifact by the stated recipe. Closed to `capabilityManifestId`, derived from the `capabilityManifestBytesDigest` artifact. |
| `owner-retained` | the named owning contract retains and admits the bytes; this closure joins by digest equality only. Closed to `owner-source-set[].ownerFileManifestSha256`, owned by security's `RepoExecutionGrantV2` owner admission. |

Because `H(D, X)` is `SHA256` of the framed preimage, **one** content-addressed
store keyed by raw SHA256 retains all three of raw artifacts, canonical records
and H identities: the object retained under a bare-hex `h-identity` digest is the
exact H preimage frame
`ASCII("opensip.product.v1") ‖ 00 ‖ ASCII(D) ‖ 00 ‖ uint64BE(length(C(X))) ‖ C(X)`.
Frame admission is exact and is not a blob escape: the literal prefix must match,
the domain must be a member of the annotation's named domain set, the declared
length must equal the remaining byte count, the remainder must be byte-identical
to `C` of its own parse, and the parsed payload must validate under the record
that the domain set registers for that domain. A frame is admissible **only**
where the annotation says `h-identity`; conversely a raw canonical payload is
never admissible there, because `C(X)` does not begin with the framing prefix and
`SHA256(C(X))` is not `H(D, X)`. A native `sha256:`-prefixed identity and a Plan's
bare-hex suffix are two spellings of one H digest and can never become a raw
payload SHA256, in either direction. Offering a frame where a `canonical-record`
is required fails parsing; offering a payload where a frame is required fails the
prefix.

Two things are easy to conflate here, so they are separated explicitly. The
**annotation** is what closes a field: it says which representation and retention
that one field has. A **spelling** — a bare 64-hex string, a `sha256:` prefix, a
`fact2:`/`plan2:` typed prefix — is not an annotation and never implies one. This
contract does not claim that every prefixed identity in the graph carries the same
annotation, and no reader should infer that from the prefix: a typed prefix tells
you which domain *table* interprets the value, while the field's own annotation
tells you what the value *is*. Where a field carries the bare 64-hex suffix of an
`h-identity`, the annotation must name the **domain set** that resolves it,
because the suffix alone does not.

`plan.nativeContextDigests` is exactly this case, and it is a **set**. A Plan may
name several admitted native contexts, including **several of the same language** —
two TypeScript projects under one Plan is ordinary, not exceptional. Nothing
elects one of them by position, by display order or by any other scalar. A fact's
`sourceUniverse` is an `h-identity` of a semantic-universe domain, and that
universe record names **its own** `nativeContextId`; that is what selects the
corresponding context, and the closure requires the selected context to be one the
Plan committed to. There is no arbitrary scalar display anywhere in that
selection.

Reference `digest` fields (`Ref`, `ProofInputRef`, `FindingEvidenceRef`) take
their representation from their sibling `domain` through the normative
`x-opensip-digest-domains.byDomain` registry in identity-schemas.v2. Every member
of every `domain` enum is registered; an unregistered domain refuses. The
`coverage-payload`, `import-payload` and `fact-payload` reference domains are
resolved through the owning Coverage, import or fact object's
`payloadSchemaDigest`; they are not authoritative roots and the proof input
vocabulary excludes them.

Auxiliary digests therefore have producing rules, not caller-defined meanings:
`resolvedConfigDigest` is SHA256 of the configuration resolver's canonical
semantic value (§1.1 of admission-and-qualification). `scopeDigest` hashes the
closed scope-descriptor record in identity-schemas.v2 (workspace roots, requested
path prefixes and excluded path prefixes, canonical sets of admitted relative
paths; `.` alone denotes the admitted project root, and every other path
is a strict logical path with no dot/parent/empty segment). `analysisSpecDigest` hashes the closed analysis-spec record (exact
registered capability/language-mode/workspace/required selections, policy pack
IDs and schema-bound parameter payloads). `semanticGrantDigest` hashes the
closed semantic-grant record: ProjectId, selected first-party or explicitly
trusted-repository principals and their exact closure/owner-source binding,
analysis operation set and scope. First-party principals have null owner source;
repository principals require the admitted owner-source digest. The projection
includes only read-source/read-import/native-analysis/prepare-code operations
actually needed by the analysis. Operational preparation grants are admitted
before a Plan exists; when analysis consumes their host-prepared outputs, its
projection must match the exact admitted preparation records retained with those
outputs under security's Plan-time join. A test-execution step has no Plan:
its runner/argv/snapshot authorization stays operational, and its observations
enter an analysis only through an admitted import2 with its execution provenance.
`test-code` is not an analysis semantic-grant operation. Storage, rendering and repair effect authority stays in the
operational request; it cannot be fabricated by this projection. Any absent
required permission refuses before Plan construction. Nonces, expiry, signing
receipts and local executable paths are not fields in the semantic projection.

`vcsDigest` hashes the closed `vcs-observation` record: schemaVersion 2,
kind none/git/hg/svn/jj, commitId (null exactly for none), dirty, and
sourceInventoryDigest (raw SHA256 of the canonical source inventory, retained
as a blob). This is source provenance; it alone never authenticates imported
runtime-to-source correspondence.

The closure checker parses and exactly validates scope, semantic configuration,
analysis specification, semantic grant, owner-source set, source inventory, VCS
observation, stage specs, finding parameters, predicate witnesses and program
predicates, and admits the policy document, resolved waiver set, compiled rule
program, import correspondence, build identity and observation through their
owning unit's schema admission. It dispatches on the `x-opensip-digest`
annotation of the field it is walking, never on that field's name, and refuses a
64-hex field the schema does not annotate.
The grant ProjectId/scope must join the Run/Plan. Witness program bytes must be
retained; matching facts and coverage must come from its explicitly named input
views. Predicate input refs are a subset of evaluationInputRefs; evidence view
roots equal the named views and coverage roots equal their coverage union.
Every visited fact/scope and view/proof/execution/evidence/seal joins the current
source or Plan, including objects reached through typed Ref fields. Proof/finding
Ref domains exclude Run, evidence, seal and proof outputs. The native and workflow
registered payload adapters are separate trusted admission stages, not assumed
validated merely because an opaque digest exists. The finite reference fixture
carries a real PolicyDocumentV1 and its compiled RuleProgramV1 in the product DSL,
so the record shapes, digests and joins above are exercised as specified; only its
*interpreter* is small, evaluating a single-atom subset, and it qualifies neither
the declarative language nor a native Coverage or relation payload registry.

Import mapping/observation, correspondence, build identity, policy, rule-program
and waiver-set digests are `canonical-record` digests under their owning
workflow schema, named exactly by the annotation and admitted by that unit's own
schema admission, so there is one implementation of each record law and no second
policy or compiler language in this contract. `plan.policyDigest` and
`policy-derivation.policyDigest` name `PolicyDocumentV1`; `plan.waiverDigest` and
`policy-derivation.waiverDigest` name the resolved effective `WaiverSetV1`;
`proof.ruleProgramDigest` names `RuleProgramV1`. The compiled program is not a
free artifact: its `policyDigest` must equal the Plan's, and it must be exactly
the projection of the Plan-selected policy's rules
(`{schemaVersion:1, policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]}`,
in the policy's own `ruleId` order). Blob bytes are `raw-artifact`. The source
inventory is the registered `source-inventory` record, and
`vcs-observation.sourceInventoryDigest` must equal the digest of the snapshot's
own inventory. Schema digests cover the exact complete registered schema document
bytes; transitive references are resolved through the pinned registry closure
without network retrieval.

### The payload registry

An earlier draft of this section additionally required "a document offered as a
*payload* schema must constrain the payload directly, so a multi-record bundle
cannot pass vacuously". **That requirement is withdrawn.** It contradicted the
native and workflow registries, which correctly hash the *exact full schema
document bytes* and validate through a registered **selector**; under the
withdrawn rule their own bundles were non-conforming, and no registry row named
a single-record document to replace them. The bundles were right and the sentence
was wrong.

What replaces it is the thing that was actually missing: a closed registry saying,
for each payload, exactly which document bytes are hashed and which selector
validates. `identity-schemas.v2.json#/x-opensip-payload-registry` is that
registry. For every class in it:

- `payloadSchemaDigest` is the **raw SHA-256 of the exact full bytes of the
  document the row names** — never a canonicalization of a selected `$def`;
- admission validates the payload against the row's **selector**, resolved through
  the pinned local closure with no network retrieval, so a multi-record bundle is
  admitted through its row and never needs a root type;
- the codec is `C`;
- a key with no row **refuses**. There is no default row, no caller-selected
  schema and no inferred one. A key name prefixed `payload.` is read from the
  parsed payload; every other name is read from the naming record.

| Class | Keyed by | Document and selector |
|---|---|---|
| `relation` | `fact.relation` | `foundation/relation-payload-schemas.v2.json`, selector from that document's own `x-opensip-relation-registry` row |
| `coverage` | `payload.schemaVersion` | `native/native-evidence.schemas.v2.json#/$defs/CoverageResultV3` |
| `import` | `import.kind` + `payload.payloadDomain` | the workflow `PayloadRegistryV1` / native §7.1 rows, mirrored; Run closure re-derives them from the workflow registry and refuses on drift, so the two cannot diverge |
| `parameter` | the cited `schemaDigest` | a document on the closed list: `foundation/import-source-context.schema.json`, and `workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1` |

`view.schemaDigests` names the registered documents a view admitted, and each
member must be one of them.

**The `ScopeDocumentV1` parameter row (CB3-MUST-4).** The comparison contract
states that `EvaluationContext.scopeDigest` is the workflow glob scope-policy
document "bound as an analysis-spec parameter", and the `parameter` class was
closed to a single document. A key with no row refuses — there is no default row
and no caller-selected schema — so that binding refused at Plan admission and
the comparison scope axis (E2 to E3) could not be populated at all: one contract
required a binding a sibling contract's closed registry forbade. The row is
registered rather than the mechanism abandoned, because the scope policy is a
genuine Plan input and the parameter class is where Plan inputs are admitted.

It is deliberately a **different record** from the foundation `scope-descriptor`
that `plan.scopeDigest` names, and neither substitutes for the other:
`scope-descriptor` is the repository extent actually walked (workspace roots and
path prefixes), `ScopeDocumentV1` is the policy's include/exclude glob selection
over that extent. Both may appear in one Plan. Because the class is keyed by the
cited **document** digest, two rows selecting different records out of one
document would be indistinguishable and the first listed would silently win;
that is the arbitrary selection the registry law forbids, so an ambiguous key
refuses. The class remains closed: a real but unregistered document, and a
caller-chosen permissive one, both still refuse.

The bounded limitation is **accounted rather than lifted**. Today's two rows are
distinguishable — `import-source-context.schema.json` and
`policy-document.schema.json` are different documents with different digests — so
nothing is ambiguous in this release, and the same `policy-document.schema.json`
bytes named by `plan.policyDigest` and `plan.waiverDigest` sit under the
`canonical-record` representation in a *different* payload class, outside this
key space entirely. What the key forbids is a **future** second `parameter` row
selecting another `$def` out of a document an existing row already cites; that is
a refusal (`PAYLOAD_PARAMETER_AMBIGUOUS_ROW`), not a defect, and it is the
registry declining to choose arbitrarily. Re-keying the class by
`(document, selector)` would remove the restriction and would change no identity
today — and is deliberately not done, because no requirement needs such a row,
and widening a closed key space and retiring an explicit refusal for a case that
does not exist buys flexibility nothing asked for. If that requirement ever
arises it is an explicit versioned correction with its own controls, never a
silent widening and never something an implementer may assume.

**Where the binding is actually decided, and where it is only asserted.**
Registering the row makes a lawful scope parameter admissible at Plan closure;
it does not by itself bind the *comparison* context to it. `adopt_baseline`
assigns `context.scopeDigest` from the scope document it is **passed**, and its
`plan` argument is a PlanId **string** — so that assignment records the digest
of whatever document the caller supplied and is **not** evidence that the
document was the Run's selected analysis-spec parameter. The same holds for
`policyDigest` and `waiverSetDigest`. Calling that assignment a binding would be
false, and this contract does not.

The honest boundary is therefore stated rather than implied. `adopt_baseline` is
a **pure projection over documents the caller must already have admitted**, and
its precondition is exactly that `policy`, `scope` and `waivers` are the
documents the Plan selected. Selection membership is decidable only with the
retained analysis-spec record in hand, so a bounded verifier takes that record
and proves it: the scope document's canonical digest must be the `payloadDigest`
of a selected parameter row citing the registered `ScopeDocumentV1` **document**
digest. A document that is not selected, a spec that selects no scope parameter,
and a row cited under another schema each refuse with their own typed reason.
When the analysis spec is supplied, `adopt_baseline` performs that verification;
when it is not, the scope binding is a **caller assertion** and this contract
says so rather than implying a join. Neither path changes the baseline
descriptor or its identity, and no product host is implied here.

The two scope records remain different things throughout: the foundation
`scope-descriptor` that `plan.scopeDigest` names is the repository extent
actually walked, while `ScopeDocumentV1` is the operator's include/exclude glob
policy over that extent.

### `fact2` payload encoding: one explicit successor law

The inherited `fact-plane.v1.json`
`$.factRecordContractV1.relationPayloadSchemaRegistryV1.canonicalPayloadEncoding`
is a deterministic-CBOR profile that forbids negative integers and non-NFC text,
while `fact2.payloadDigest` is a `canonical-record` digest under `C`, which admits
both. Two owning statements in direct contradiction is a design defect, so this
contract settles it in one direction and says exactly what changes.

**`fact2` payloads are `C`.** There is one product encoder and no second codec in
the trusted computing base. Every *logical* restriction the CBOR profile carried
survives, as an admission rule expressed in the registered schema rather than
implied by a codec: NFC-only text, no negative integers, `uint64` range, the
closed field set, the enums, the per-rung required/forbidden fields and the
`universeRule`. `foundation/relation-payload-schemas.v2.json` carries all
thirteen relations — the twelve inherited from fact-plane plus native §4.4's
`unresolved-edge` — reproducing each inherited `required`, `optional`, field type
and enum exactly, and its `x-opensip-relation-registry` carries each relation's
selector, universe rule and rung ladder.

**The ladder is an explicit array, and `rungs` is not it (CB3-MUST-1).** That
registry had no `ladder` key at all. Its `rungs` member is a per-rung
required/forbidden **field-rule** table, and it is legitimately the empty object
for a relation with no per-rung field variance — which is every single-rung
relation: `file`, `package`, `vcs-change`, `declares`, `literal`,
`control-flow`, `reachability` and `clones`. Reading `rungs` as the ladder gives
two conforming readings and both are wrong: read strictly, those eight relations
admit no `resolution` at all and no Run of the kind these contracts require
could close; read leniently — as the reference closure did, via an
`and row['rungs']` guard — the ladder check is skipped entirely for them, and a
`declares` fact carrying `resolved-callee`, a rung of `calls`, closes a Run.
The rung vocabulary is shared across relations, so such a value is perfectly
well-formed; **schema vocabulary is not relation membership.**

Each row therefore carries an explicit ordered **`ladder`**, weakest-first,
inherited verbatim from `fact-plane.v1 relationRegistry.relations[].ladder` plus
`[observed]` for `unresolved-edge`. This registry is the **single authority**;
`native_evidence_model.v2.LADDERS` and
`capability-manifest-domains.v2 RELATION-LADDER-DOMAIN-V2.ladders` are declared
mirrors of it and are drift-checked **exactly and in order**. Order is not
decoration: the capability registry's arrays had been alphabetised while still
naming the inherited ladder as their source, which reversed `calls`, `imports`
and `references` — harmless only because that registry is consulted for
membership alone, and an inversion for anything that read it as an order.

Membership is decided against `ladder`, always, with **no empty-ladder
fallback**: a relation with no ladder is a registry defect and refuses rather
than admitting anything. Order comparison is the index within one relation's
own ladder. Nothing orders a rung of one relation against a rung of another,
and there is no global rank; a cross-relation comparison is an admission
refusal, never a true or false predicate.

**One rung vocabulary, named directly (CB3-MUST-2).** The policy DSL previously
carried its own abstract tier vocabulary — `syntax`, `resolved`, `type`,
`external` — reached from `PolicyDocumentV1` `Atom.minResolution` and reused by
repair's `EvidenceRequirement`. It shared **zero** members with the fifteen rung
names every fact, Coverage entry and native `RequirementV2` actually carries, no
document mapped one onto the other, and the evaluator compared them through a
single global rank table (`{syntax:0, resolved:1, type:2, external:1}`) shared by
every relation. Whether `minResolution: resolved` was satisfied by
`resolved-target`, by `resolved-binding`, by `checked` or by all three is a
public semantic decision, so two conforming implementations emitted different
findings from the same Plan.

Preserving the abstract syntax with a published mapping was considered and
rejected. Such a mapping must be **per relation** — `resolved` names a different
rung in each of `imports`, `references`, `calls` and `reachability`, `type`
names a rung only for `types`, and `external` names no native rung at all — so
it is a partial, lossy renaming with no expressive power, and it does not even
preserve the one-word-one-meaning property that motivates an abstract syntax. It
also cannot survive C-1: `syntax < resolved < type` **is** a global ladder, and
making it relation-relative dissolves it into the rung names. The smaller and
coherent correction is to name the rung: `Atom.minResolution` and
`EvidenceRequirement.minResolution` are rung names, the abstract `Resolution`
enum and the global `RES_ORDER` rank are **withdrawn**, and satisfaction is
ladder-index comparison inside one relation.

Two admission conditions follow, because no schema keyword can express the
second without restating the ladders and creating another independent source.
The schema constrains `minResolution` to the flat rung vocabulary — exactly the
union of the registry's ladders, drift-checked — which is **necessary**.
Membership of *this atom's relation's* ladder is **sufficient** and is enforced
at admission: in the workflow policy resolver, and at the **Run closure**, over
both the Plan's `PolicyDocumentV1` and the proof's compiled `RuleProgramV1`. An
evaluator-only check would let a sealed Run assert a predicate that was never
admissible. Atom relations are closed too: an atom names either one of the
thirteen native fact relations or one of the imported-evidence relations closed
by `imported-evidence.schema.json#/x-opensip-evidence-relation-registry`
(`runtime-observation`, `history-change`, each with the one-rung ladder
`[observed]` — no new rung token), and an evidence relation must declare its
`evidence` kind while a native fact relation must not.

**What does not change:** historical `FactRecord1` records, their CBOR wire bytes
and their provenance are untouched and remain valid history. They are never a
`fact2` preimage, and this contract has always said the historical wrapper cannot
bind a `snapshot2` identifier. **The conversion is stated, not delegated:** a
provider that emits deterministic CBOR has its payload decoded under the selected
registered schema and re-encoded to `C` by the trusted first-party host adapter
before `fact2` is minted; the adapter refuses rather than repairs a payload that
violates any retained restriction, and persistence stores the `C` bytes that
`payloadDigest` names. No unspecified adapter invents a schema.

Joined at Run closure for every fact: the relation must be registered;
`payloadSchemaDigest` must be the relation document's own file digest;
`resolution` must be a rung of that relation's ladder; that rung's required and
forbidden fields must hold; and `universeRule: same-only` requires
`sourceUniverse == targetUniverse`.

#### Relation payloads: the digest law, and what a payload's claim is joined to

The closing digest law above governs identity-schemas.v2, and the native contract
extends it to its own bundle. `foundation/relation-payload-schemas.v2.json` was
governed by **neither**, so its digest-bearing and path-bearing fields carried no
annotation and a `file` payload's `path`, `contentSha256` and `byteLength` were
joined to nothing at all: a schema-valid fact could claim any content hash for
any path, including a path in no snapshot, and close a Run. That was a real
defect and this is its closure, as a class rather than as one field.

That document now carries its own `x-opensip-digest-law`, and **every**
`DigestHex`, `Sha256Text` and `CanonicalPath` field in it is annotated with its
representation, producing preimage or codec, retention and owning authority. The
law is **consumed, not declared**: every annotated field must be reachable from
its relation's registry joins or must declare `retention: not-joined` with its
reason, and every field a join names must exist in the selector. A newly
annotated field with no join refuses, so this omission cannot recur silently.

The relation document's annotation law also governs schema structure. A governed
occurrence is a reference to `DigestHex`, `Sha256Text` or `CanonicalPath`, including
an intermediate local `$defs` alias, or an inline pattern exactly equal to one of
those definitions' patterns. Follow local references, nested `properties`,
`items`, `additionalProperties` and `oneOf`/`anyOf`/`allOf` branches when checking
these occurrences. Following local references must terminate even when a local
definition is cyclic. An annotation on the occurrence, its enclosing schema
path, or an intermediate alias applies to that occurrence. An annotation on
the terminal governed scalar definition does **not** provide a blanket default
for all references to that type. Directly annotated top-level selector
properties remain subject to retention and join checks even when their scalar
form is not one of these three.

Every governed occurrence must have an effective annotation. An annotated
alternative does not cover an unannotated alternative; a parent annotation may
cover each alternative it encloses. When multiple schema paths reach the same
location, any occurrence lacking an effective annotation makes that location
inadmissible. Later annotated occurrences cannot undo that absence. Object-key
order and the order in which these paths are visited must not change admission.

There is no precedence rule between disagreeing effective annotations at one
location: distinct annotations conflict and the document refuses; repeated
annotations that are equal under typed canonical equality do not conflict.
Every effective annotation must use the declared retention vocabulary. These
same effective annotations govern coverage, retention and join/exemption checks;
none of those checks may silently revert to inspecting only direct properties.

The current registry's join fields address top-level selector properties.
Taking a scalar alternative of such a property preserves that address; entering
an object member, array element or map value does not. A governed occurrence at
one of those nested locations must explicitly declare `retention: not-joined`.
As elsewhere in this law, the reason for an exemption is stated on the field
for a reader; admission checks the declared retention, not the presence or
content of that prose. It cannot claim a joinable retention that the current
join vocabulary cannot address. An addressable annotated property requires its
registry join unless it declares that exemption, and every named join field
must exist in the selector. Missing annotations, conflicting annotations,
undeclared retention values, unaddressable claimed joins, missing joins and
joins naming absent fields all refuse at schema-law admission. This check
establishes coherence of the registered schema; the owning-fact snapshot and
retained-byte joins below still establish the truth of each admitted payload.

`x-opensip-relation-registry` carries a normative per-relation **`snapshotJoins`**
table, and Run closure applies it to **every owning fact** — after the registered
selector validation, and **independently of the payload decode memo**, because
the truth of a claim about a snapshot is a property of the *owner*, not of the
bytes. A payload alone cannot decide it, so the closure requires owner context:
the enclosing fact, the snapshot **that fact names**, the retained blobs and the
bound native context. The four relations that make such a claim:

| Relation | Join |
|---|---|
| `file` | `path` must be in the enclosing fact's snapshot source inventory; `contentSha256` must equal that inventory row's digest; `byteLength` must equal its length; the bytes must be **retained** under that digest and re-hash to it; and every anchor of the fact must lie in the very file the payload claims. |
| `package` | `manifestPath` must be in that inventory. |
| `vcs-change` | `path` must be in that inventory **unless** `changeKind` is `deleted`, where the path is by definition absent from the analysed snapshot. |
| `clones` | the framed body-identity join below. |

**How many anchors a fact carries is decided per relation, and the inventory
class carries none.** `fact.anchors` has no `minItems`, and only `clones` ever
stated a cardinality, so both the `file` row's every-anchor clause above and
native §1.2's every-anchor-path rule are universally quantified over an array of
unstated length — *vacuously true* at zero anchors, permitting and forbidding
nothing. Both spellings of one `file@enumerated` claim consequently closed a Run
with different `fact2` identities. The relation registry now carries a closed
`anchorLaw` on every relation:

| Class | Relations | Anchors | Why |
|---|---|---|---|
| `source-text` | `declares`, `literal`, `control-flow`, `imports`, `references`, `calls`, `types`, `reachability`, `unresolved-edge` | **≥ 1** | The fact was read from source text; an unanchored one names no file that could have been read. No *additional relation-specific* maximum and no canonical extent beyond the common schema bounds (`fact.anchors` keeps its `maxItems: 100000` and `uniqueItems`): which spans a producer cites is a real statement about what it read, so differing citations are *different* semantic descriptors and no cross-provider identity is promised. |
| `body-identity` | `clones` | **= 1** | Exactly the body span the identity is over (unchanged). |
| `inventory` | `file`, `package`, `vcs-change` | **= 0** | The claim's whole semantic input is the payload, already bound to the snapshot by the joins in this table. An anchor could only restate part of an already-joined claim on an axis nothing derives — one semantic input, several spellings, several identities. |

Zero is also the only cardinality *every* inventoried path can satisfy: a path
no bundled grammar reads, an extensionless path, and a `vcs-change` on a
`deleted` path, which the row above places outside the snapshot entirely and
which therefore cannot bear an anchor at all.

**The raw-byte boundary.** An inventory claim retains its path, content digest
and byte length **without anyone decoding the bytes**. With the class at zero
anchors the `ANCHOR_SOURCE` / `ANCHOR_RANGE` / `ANCHOR_UTF8` checks never run for
such a fact — they iterate the anchors — while the `inventoried-file` join above
still does, and it only hashes and measures. An **empty** file and a **non-UTF8
binary** file are therefore ordinary inventory, at an extensionless path as
readily as any other, and requiring bytes to parse as code or as UTF-8 merely to
record their path and hash would be a narrowing this contract never intended.
The code-span laws keep exactly the scope they had: the *same* non-UTF8 bytes
still refuse as a `source-text` anchor (`ANCHOR_UTF8`), and the digest, length
and path joins still refuse a wrong claim about those bytes.

**Where a location comes from, now that inventory facts carry no anchors.**
Nothing reads `fact.anchors` as a finding location, so removing them removes no
route and no new flexibility is added. A finding locates through
`finding-fingerprint.subjectKey.logicalPath`; an inventory claim's own location
is its payload `path`, joined to the snapshot inventory by the table above; and
`finding`, `finding-fingerprint`, `proof-bundle` and `predicate-witness` carry no
anchor field at all. A finding over a zero-anchor inventory fact closes a Run and
is located by exactly those existing records. It closes two live gaps as well as
the spelling one: the "unanchored code fact" rule was enforced only inside the
syntax-universe guard, so such a fact closed a Run under a TypeScript or Rust
universe; and `anchorPathField` sat only on the `file` row, so a `package`
payload anchored into an unrelated file closed a Run. The `file` row's clause is
retained as the narrower statement it always was — under this cardinality it is
subsumed rather than reached (`FACT_ANCHOR_CARDINALITY`).

`vcs-change.previousPath` is the one declared exemption. A pre-rename path names
a state **before** the analysed snapshot; it is a historical observation, not a
current source claim, and joining it to this snapshot's inventory would refuse
every honest rename. The exemption is recorded as `retention: not-joined` with
that reason rather than left as residue, so the distinction between a current
source claim and a historical path observation is explicit in both directions.

An inventory row is a claim *about* bytes; retention is custody *of* them. A
`file` fact whose inventory row agrees but whose bytes are not retained is
**evidence unavailable** — retention loss under §5 — not a false claim.

#### `clones`: the inherited body recipe, reused and not restated

`bodyIdentity` and `normalisationVersion` are pinned by
`docs/coop/artifacts/fact-identity-policy.v2.json`, at
`#/canonicalisationSchema`, `#/normalisationLadder` and
`#/factRecordIdentityBoundaryV1`. Those are **normative inputs to this
contract**, named here by exact path and selector; this section reuses that
grammar and does not replace a pinned body recipe with a restatement.

- `normalisationVersion` is the raw SHA-256 of the **exact retained canonical
  level-specification bytes** — the per-language lexical boundary rules, canonical
  token-kind registry, directive classification, transform order and replacement
  byte rules. A human version label is insufficient and an opaque caller hash is
  inadmissible; the specification is retained and re-hashed at closure.
- `bodyIdentity` is `sha256:` followed by SHA-256 of the **fully framed,
  domain-separated preimage**: `u8 len‖"opensip.fact-identity.v1"`,
  `u8 len‖levelId`, `u8 len‖levelVersion` as the **raw 32 digest bytes and never
  the hexadecimal display text**, `u8 len‖languageId`, `u8 len‖languageVersion`,
  then `u32be len‖payload`. Unframed concatenation is forbidden. At
  `L0-verbatim` the payload is `u32be raw_byte_len ‖ the exact body-span bytes`
  with tokenisation forbidden; at `L1`–`L3` it is the level's framed token stream.
- **The outer frame length and the L0 payload length are both present and both
  meant.** The trailing `u32be len‖payload` component is the frame's, and the L0
  payload is *itself* length-prefixed, so at `L0-verbatim`
  `payload_len == raw_byte_len + 4` — the payload is length-prefixed twice and
  neither prefix is dropped. This is not an accident of two grammars meeting: it
  is the same shape `L1`–`L3` already have, where the payload is
  `u32be token_count ‖ token*` under the same outer `u32be payload_len`, so every
  level presents one uniform framed component to the preimage. Worked example —
  a four-byte body span `a=1\n` (`61 3d 31 0a`) has L0 payload
  `00 00 00 04 61 3d 31 0a` (8 bytes) and contributes the final frame component
  `00 00 00 08 00 00 00 04 61 3d 31 0a` (12 bytes). Reading the span bytes as the
  payload directly would yield `00 00 00 04 61 3d 31 0a` there and a **different**
  `bodyIdentity`; that reading is not the one this contract uses. The inherited
  `fact-identity-policy.v2` `byteGrammar` bytes are unchanged and this states
  which of its two grammatically available readings is the admitted one.
- The frame itself is **retained** under that 64-hex suffix, so closure fetches
  it, re-hashes it, parses it and joins each component to something the Run has
  already admitted: the domain tag to the policy, `levelId` to the payload's own
  `normalisationLevel`, `levelVersion` to the retained specification, and
  `languageId`/`languageVersion` to the fact's own semantic universe.
- `languageVersion` is the **raw 32 bytes of `SHA-256(C(body-language-version))`**
  — the same fixed-width treatment the inherited grammar already gives
  `levelVersion`, so the inherited frame bytes and field grammar are unchanged.
  Fixed width is not a convenience: the inherited frame gives each component a
  **`u8` length**, and any component built by embedding per-crate or per-package
  data is not representable for ordinary valid inputs. A Rust workspace of
  twenty-one crates already produces 723 bytes of raw map, against a maximum of
  255.

`body-language-version` is defined in identity-schemas.v2 and its retention is
**`derived`**: no field of it is a free input, every field is copied from a named
path in a record this Run already retains and the owning contract already
admitted, and closure **recomputes** it rather than accepting it. What it carries
is the identity of the component that **interprets the body span** — the
compiler — plus the selected source **dialect**. That identity is not missing and
never needed a new universe field: the universe's own `nativeContextId`, which
this closure already requires to be Plan-selected, reaches the admitted retained
native context whose `toolchain` carries it, and native §2.3 already refuses a
context whose compiler version is not the admitted tool closure's own. Each
language's binding names the exact source path of every field and lists each
**excluded** field with its reason; operational platform, paths, resolution
inputs, build tooling and option synthesis are all out, because none of them
reads the body.

Dialect is **body specific**, per language, closed, and always **selected** —
never collected and never defaulted. There is no `null` branch: a language with
no declared dialect axis would be exactly the unexamined default this law
refuses, so every language states its axis and its selection rule, and every
branch that cannot select refuses with its own cause.

- **Rust**: the **effective** edition of the **selected** compilation **target**
  that owns this body's path, from native §2.1's committed
  `SourceUnitOwnershipV1` — a stated relation with a closed target table and an
  **explicit selection**, not a directory inference. Cargo lets a target override
  its package's edition, so a package map whose values all agree still does not
  determine a body's dialect: there is **no fast path**, the ownership relation is
  required for every Rust `clones` fact, and a universe that committed none admits
  no clone. Selected owners whose effective editions agree are admissible;
  selected owners that disagree, a path owned only by unselected targets, an
  unowned path, and a missing relation all refuse, each with its own cause. A
  unit's identity is `H` over a **published** four-field preimage
  (`native.compilation-unit.v1`), re-derived at admission — not an opaque digest,
  and not a delimiter label, which could stay injective only by forbidding a `#`
  in a repository directory that the canonical path contract admits.

  **The same physical source path compiled by two targets at two editions has a
  valid form under each.** The selection lives inside the record whose identity
  the universe names, so choosing a different target is a different
  `sourceUniverse` — two analyses, not two readings of one — and the ambiguous
  *unselected* request, which asks for both at once, refuses. No relation payload
  changed to make that possible, and none needed to.
- **TypeScript**: the source **variant** its own file suffix denotes, by a closed
  longest-suffix table (`.d.ts` is never read as `.ts`). An unlisted suffix
  refuses rather than being folded into a neighbour, so no normal variant is
  silently mis-assigned and a new one must be registered deliberately. This is
  deliberately conservative: distinct variants stay distinct even where a parser
  would treat two alike, so it can fail to equate two equivalent bodies and can
  never equate two the language reads differently.

Paths, crate names, unit ids and the selection itself **establish** these
selections and then do not enter the record; what enters is `{edition: year}` or
`{sourceVariant: token}`.

**Selected scope and incomplete enumeration are different claims**, and the
closure enforces the difference rather than letting one stand in for the other. A
selection says the named targets *are* the analysis: an owner outside them is
deliberately out of scope, and because the selection is part of the universe
identity every consumer can see it. `partial` enumeration says the producer did
not finish: an owner *inside* the selected scope may exist that was never listed
and could contradict a listed one, so **no body dialect is admissible at all**,
checked before any row is read — incomplete discovery can never act as an
implicit edition selection by hiding a conflicting owner, and silently omitting
one is not a selection because an omission leaves no trace. Partial evidence
still counts under the existing law rather than voiding a Run: the clones scope
mints no body identity, its Coverage reports the incompleteness, and the
predicate and seal are **indeterminate** rather than a false pass. Schema
validity is never a completeness claim about a real repository; what a producer
enumerated remains a trusted observation and its truth remains future
qualification work.

The body's `languageId` comes from the **same selector over the same anchor**,
and it is the language of the **body**, not of the provider. Native §6.3 puts
`languageId ∈ {typescript, javascript, rust}` in the normalized-body preimage
precisely so a TypeScript body never groups with a JavaScript one even with
identical bytes, and one TypeScript **engine** universe lawfully produces both: a
`.js` body read by that engine is a `javascript` body and carries that
identifier. The frame's `languageId` and the record's are taken from one
derivation, so they cannot disagree; the frame's must also be a language the
universe's binding declares that engine produces, so a `rust` frame under a
TypeScript universe refuses.

Spelled exactly, so the relation registry, the domain registry and this section
are one sentence: the `languageId` is
`languageVersionBinding.bodyLanguageByVariant[<the variant the dialect suffix
table selects from this anchor's path, longest match>]` where the row's
`dialect.form` is `closed-suffix-table`, and `languageVersionBinding.bodyLanguage`
for any other dialect form. It is **never** the universe domain row's own
`language` field, which names the engine: that reading yields `typescript` for
every `.js` body, and `syntax` — a value the closed `languageId` enum does not
contain — for every body under `native.semantic-universe.syntax.v2`, so a
TS-hosted JavaScript body would get the wrong clone identity and a compiler-free
syntax Run would have no admissible body identity at all. The clones registry's
`bodyIdentityJoin.languageIdSource` previously carried that engine reading; it
now carries this one, and each domain row's own `bodyLanguageLaw` has always
said the same. No JavaScript body is rewritten as TypeScript, and
§6.4's `cross-tsjs` candidate-only projection is untouched — it remains a
separate candidate mode, never a shared identity.

Two bodies sharing a `bodyIdentity` is evidence that their **normalized bodies
agree under one language version at one level**. It is not evidence of semantic
equivalence, not a cross-language or cross-variant claim, and not a statement
about any normalizer's correctness. The remaining obligation is placed rather
than dropped: **a level specification whose transform depends on an axis the body
language version does not carry is inadmissible for that language**, and level
specifications are FACT-IDENTITY's to write.
- A `clones` fact carries **exactly one** anchor: the body span the identity is
  over. Zero would leave the claim unattached, and several would make the L0
  recomputation a choice — the arbitrary-anchor defect in another form. This is
  the `body-identity` row of the registry `anchorLaw` above, which is the single
  enforcing statement; `bodyIdentityJoin.anchorCardinality` is a declared mirror
  of it and the join checks that the two **agree** rather than refusing the same
  fault twice under two names (`RELATION_ANCHOR_LAW_DRIFT`).

The split is honest and stated rather than blurred. At `L0-verbatim` the
canonical payload **is** the raw body-span bytes, so the host **recomputes** it
from the enclosing fact's own anchor: a real source join. At `L1`–`L3` it is a
versioned normalizer's output that no host can recompute, so what is required is
exact **retained preimage custody** plus the framed-identity check and
well-formed stream framing. That is evidence about custody and framing. It
qualifies no parser, grades no tokenisation and certifies no normalizer.

**FACT-ID-V1 and `bodyIdentity` are never equated.** The fact identity wraps the
complete clone fact; `bodyIdentity` is over one normalized body span. They differ
by type and by domain, and neither may substitute for the other — as
`#/factRecordIdentityBoundaryV1/clonePayloadJoin` already says.

Native contexts and native semantic universes are `h-identity` under the native
contract's own versioned domains, retained as frames and re-admitted at Run
closure by that contract's own admission. A digest under one representation is
never silently treated as a digest under another.

Five records this graph digests are defined here because nothing else defines
them, and every field of every one of them is required:

`program-predicate` is the record digested by
`predicate-witness.programPredicateDigest`:
`{schemaVersion: 2, ruleProgramDigest, ruleId, predicateId, operation, nodeDigest}`.
It **addresses** one predicate node of the admitted `RuleProgramV1`; it does not
restate the node. `ruleProgramDigest` equals the proof bundle's; `ruleId` names a
rule of that program; `operation` is one of the seven evaluator predicates and
equals both the addressed node's `op` and the predicate proof's `operation`; and
`nodeDigest` is raw SHA256 of the canonical bytes of the addressed node, whose
schema is the workflow contract's own `Predicate`. **Node addressing** is total
and deterministic: the rule's `emitWhen` root has address `p`; the *i*-th operand
of an `and`/`or` node at address `a` has address `a.i` with *i* zero-based in
shortest decimal without a leading zero; the single operand of a `not` node at
address `a` has address `a.0`. `predicateProofs[].predicateId` and
`predicate-witness.childPredicateIds` are these addresses, not free labels. The
witness's `childPredicateIds` are exactly the addressed node's operand addresses,
each of which must itself be proven for the same rule and subject; `countLimit` is
the node's `n` for `count-at-most` and null otherwise. Two conforming
implementations therefore mint one `programPredicateDigest` for one source and
one policy, and a witness cannot name a predicate the admitted program does not
contain.

`finding-parameters` is the record digested by `finding.parameterDigest`:
`{schemaVersion: 2, messageCode, parameters}`, where `parameters` is an object map
from a parameter name to a string, integer or boolean. It is a map, not an array,
so parameter names are unique and ordered by the canonical encoder itself with no
ordering annotation to elect. `messageCode` must equal the finding's.

`stage-spec` is the record digested by `stageSpecDigest`:
`{schemaVersion: 2, planId, producerClosure, operation, parameters, outputDomains,
outputSchemaDigest}`. `execution-plan.stages[].stageSpecDigest` and
`cache-key.stageSpecDigest` carry the same field name because they are the same
digest of the same record under the same recipe; there are never two recipes for
one spelling. The stage spec's `planId` is the Plan, its `producerClosure` is a
Plan-selected semantic closure, its `outputDomains` equal the stage's, its
`outputSchemaDigest` is the exact complete registered stage output schema document
bytes, and every one of its `parameters` rows (`{schemaDigest, payloadDigest}`,
the same shape the analysis spec uses) must also be a row of the Plan's analysis
spec: a stage takes no hidden input. A cache or regeneration key must repeat the
same `producerClosure` and `outputSchemaDigest` as its stage spec, so a caller
cannot invent an output schema for a reused stage. `cache-key` and
`regeneration-key` continue to share one schema and differ only by H domain.

`commit-inventory` is the record digested by `commit-receipt.inventoryDigest`:
`{schemaVersion: 2, runId, objects, blobDigests}` — the exact set of typed object
identities and retained raw blob digests the commit published for that Run. The
receipt authenticates RunId and this inventory and remains operational custody
evidence excluded from semantic IDs.

`owner-source-set` is the record digested by
`semantic-grant.principals[].ownerSourceDigest`: the security contract's
`RepoExecutionGrantV2` owner projection, an array of
`{ownerKey, source, ownerFileManifestSha256}` strictly ascending and unique by
`ownerKey`. The manifest bytes themselves stay `owner-retained` by security; this
closure joins the projection by digest equality and re-checks its order and
uniqueness.

Waiver resolution selects the active admitted waiver set before pure evaluation
and retains that resolved set and its authority provenance; the evaluator does
not consult today's wall clock. Replay evaluates the historical sealed set;
new analysis and repair authorization resolve current expiry and revocation
again. A historical waiver result is never a fresh grant.

The complete closure includes bytes for each policy, waiver, rule program,
configuration, analysis specification, scope descriptor, semantic grant, owner
source set, source inventory, VCS observation, stage spec, native context frame,
native universe frame, capability manifest, registered schema, import
payload/mapping/correspondence/build/observation, fact payload, Coverage payload,
finding parameters, program predicate and predicate witness referenced anywhere in
this graph — that is, the preimage of every digest whose retention mode is
`preimage`, with the three named exceptions recomputed or owner-retained as §3
states. For a native context or universe this reaches the nested semantic records
it names and their raw members: the dependency source set, its packages' file
manifests and every manifest member's bytes at exactly its declared length; the
unified features; the cargo config projection and the projected config file bytes;
and every inert prepared-output row's bytes. A replayable Run retains them all.
The host recomputes all blob hashes and all semantic identities, validates each
payload with the exact admitted schema and its semantic admission rules, and
rejects missing, extra authoritative roots, wrong-kind, cross-Plan/cross-source
or unresolved references. Unreferenced CAS blobs are not evaluation inputs.
Snapshot config/scope, Plan config/scope and native-context source correspondence
must agree. **The Plan's deterministic `budget` must equal, exactly and by type,
the `analysis.budget` of the committed resolved semantic configuration the same
Plan names.** The value is committed in two places and neither silently wins: a
legitimate budget override enters the **resolved semantic configuration first**
(admission-and-qualification §1.1's layered resolution), and the Plan then
carries that same `{unit, limit}`. A Plan whose inline budget contradicts its own
configuration is refused before any evaluation. Both values already enter PlanId,
so this changes no identity, replay or determinism property; what it fixes is
that two conforming implementations would otherwise disagree on *admission*.
Every view's facts/scopes/Coverage agree on Plan source, universes,
relation/rung and producer; every source anchor must name an inventoried blob,
and the number of anchors must be the one the relation registry's `anchorLaw`
states for that relation.

**Coverage scopes partition, and the two halves of that word have different
owners.** *Disjointness* is the general rule, applies to every relation, and is
**decided at retained Run closure**: two Coverage scopes of one view that share
the **full owning tuple** — the same
`(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` — must carry
disjoint subject sets, so no subject is claimed twice under one interpretation and
no count, completeness claim or universal negative over that view double-counts it.
The key is published as the relation registry's `coveragePartitionLaw.partitionKey`
and is the same tuple `coverageTotality` matches facts on; a Run whose view
violates it refuses with `SUBJECT_SCOPE_PARTITION_OVERLAP` naming the relation,
rung and offending subject. A **differing tuple is a different claim, not an
overlap**, which is why the same subject may lawfully appear under two relations,
two rungs or two universes.

Three boundaries of that rule matter and are held by controls. It is **per view**:
two views of one Run may reference the same scope, because a view is one
producer's interpretation. It covers **every scope the view references, including
scopes with no Coverage entry** — those bypass the per-Coverage *producer* guard,
though they still reach the retained-scope ladder check. And it is decided
**here, not by the producer**: Coverage admission sees one scope and its one
entry, so it cannot decide a property that holds between two scopes; a law nothing
compares is the defect this closes.

*Omission* is **not** a general rule and is never inferred. A scope owes a
complete enumeration only where the relation registry gives its rung a
`coverageTotality` row, which today is `file@enumerated` alone: a snapshot
inventories exactly the files it contains, so a `complete` result there must carry
a fact for every inventoried subject it claims to have examined — a fact that
agrees with **that scope** on its own snapshot, relation, rung and *both*
universes. `package@manifest-declared` and `vcs-change@vcs-reported` have no row
and owe nothing, because most paths declare no package and most were not changed.
Neither do the nine `symbol`-kind relations, and that is a **stated trust
boundary rather than an omission**: native §1.2 records that the enumerator's
attribution of symbols to files is trusted and **not re-derivable from the
retained Run**, no enumeration of the symbol universe is published, and inventing
one would be fabricated evidence. Reading "without omissions" as a universal
obligation would therefore make the clause either unenforceable or a demand for
evidence the design deliberately does not claim.

This does **not** make `complete` vacuous where no totality row exists. It remains
a claim about the **examined** partition, and it is held to that claim by the
entry's own committed evidence: RC-0 decides the relation's registered
`(relation, rung)` pair before any fact is read, RC-1 keeps enumeration
completeness separate from resolution completeness, RC-2 forces
`unresolvedEdgeClasses` to equal the admitted `unresolved-edge` facts of the view
and never lets a zero edge count imply `complete`, `examinedUniverse` carries the
counts, and `partial`/`not-attempted`/`unknown` with a disclosed deficiency stay
representable so nothing is forced into a false `complete`. The fact/scope join
above is existential, so in a view carrying two universes a fact of one lawfully
sits beside a scope of the other and must not discharge its obligation.
No arbitrary payload schema supplied by an import becomes an admitted schema.

## 4. Evaluation and proof verification

The deterministic evaluator consumes only the Plan-bound, schema-admitted
finite fact views, Coverage, imported evidence, declarative program, policy and
waivers. The declarative rule program defines the exact subject enumeration,
relation/rung, typed field filter, quantifier, deterministic work bound and
emission condition for each predicate. Query planning is an optimization only:
a retained full-scan reference must agree on selected facts. Neither a provider
nor a witness supplies its own expected result or filter. All consumed data are
listed in the proof's evaluationInputRefs; no hidden lookup is allowed.

A predicate proof binds rule, subject, predicate, operation, admitted inputs,
scopes, value and a retained witness digest. The closed witness record contains
schemaVersion=2, program predicate digest, sorted matching fact IDs, sorted
Coverage IDs, optional integer count limit and sorted child-predicate IDs.
The program predicate digest is the §3 `program-predicate` record, which addresses
the exact node of the admitted rule program this proof discharges; the predicate
ID and the child predicate IDs are that section's node addresses, not free
labels. An atomic witness names no children; boolean witnesses name only earlier
nodes in the same subject/rule DAG, and each named child must itself be proven
for the same rule and subject. Predicate IDs are unique and the DAG is bounded
by the rule program's admitted work bound. Witness facts must be exactly those
selected by the program over the complete admitted view, not merely a subset
chosen by the producer. Counts count distinct selected fact IDs. The verifier
recomputes scope membership, matches, completeness and each result, and then
recomputes finding fingerprints, findings, rule outcomes and aggregate verdict.
Missing witness bytes is retention loss, not a false predicate.

| Predicate | Positive/complete case | Incomplete case |
|---|---|---|
| exists | true on a matching fact; false only on complete absence | true on a known match, otherwise indeterminate |
| none | false on a known match; true only on complete absence | false on a known match, otherwise indeterminate |
| count-at-most N | false once more than N distinct matches exist; true when complete count ≤ N | false above N, otherwise indeterminate |
| all-covered | true only with admitted resolution-complete coverage for the requested universe/rung | indeterminate |
| and / or / not | strong Kleene three-valued logic; false dominates and, true dominates or | unresolved value propagates unless dominated |

Completeness means the native contract's examined partition **and** resolution
and closed-world requirements. An unresolved `m[k]()` can never establish
no-consumer merely because the enumerator visited all subjects. Runtime unhit
observations never supply universal static completeness. A rule expression that
is true produces its declared outcome; findings arise only from the program's
emission condition. A false condition is a retained no-match proof. An
indeterminate required predicate is retained with typed deficiency. A schema,
identity or interpreter fault is an operational failure, not a fourth logical
truth value and not an authoritative Run. Aggregate policy fail dominates
indeterminate, which dominates pass; a required operational fault has D9's
operational precedence even if other steps have committed failing Runs.

Before sealing, the host independently replays the admitted deterministic
program against the retained closure and compares the complete normalized
result (all predicate outcomes, omissions, findings and verdict), not just a
checksum supplied by the producer. This verifier is first-party trusted code;
this is reproducible verification, not a proof of mathematical soundness or a
sandbox against a malicious host. Semantic conformance uses independent
oracles and mutation cases. The exact evaluator executable, declarative program,
input closure and witness bytes are retained, so an independent installation
can replay without trusting the original result flags. No old Python route
region is executed to decide product authority.

Verification reads retained objects and creates an operational verification
receipt. Regeneration executes the exact retained producer and Plan input
closure into a candidate namespace, verifies each expected semantic identity,
and publishes recovered availability only if all required bytes agree. A
mismatch is an operational regeneration verification refusal: `HOST.IO_FAILURE`
(class `operational-failed`, faultCause `host-io`, exit4), domain detail
`evidence.regeneration-mismatch`. It cannot replace the sealed Run. New
source or policy creates a new Plan/Run. Expired or
revoked permission cannot be resurrected by a matching hash. A miss recomputes
normally; a corrupt hit is quarantined and disclosed before any permitted retry.

**Constructing a cache key and admitting a hit are two different acts, and only
the second is an admission.** Key construction is pure and deterministic: exact
schema admission and canonical order over the `cache-key` record, nothing more. It
reads no bytes and resolves no reference, so a host may compute it before loading
anything and miss cheaply; it is a lookup key and grants nothing. **Finding bytes
under a matching key is not authority.** An entry may be consumed only against
exactly the closure the Run itself requires: the stage spec retained and joined to
this Plan, the producing closure retained and Plan-selected, every `scopeIds`
member a retained `subject-scope` of this snapshot, the output schema document
retained, and every `inputRefs` entry resolved through the same
`x-opensip-digest-domains` registry the Run uses — so a consumed native context
must be one this Plan selected, a consumed import must be one this Plan selected,
and nothing is admitted under a guessed payload-domain schema. A bare
`coverage-payload`, `import-payload` or `fact-payload` reference is refused as an
authoritative root rather than resolved by guesswork; those are reached only
through their owning object. A hit that clears all of this is reusable producer
output, never evidence authority, and it never replaces or re-seals a Run. The
same record and the same admission apply to a regeneration key; only the H domain
differs, and a regeneration whose result disagrees remains the
`evidence.regeneration-mismatch` refusal above.

## 5. Durable custody and failure protocol

Default `opensip`/`analyze` is DURABLE_AUTHORITATIVE under CD-RT-5. The host
reports retention origin DEFAULTED and durable-unbounded posture before first
write; the command's documented effect is admission of the project marker and
private registry/store, followed by an authoritative Run. No implicit policy
file is written. Explicit retention overrides have independent byte/time/count
bounds with provenance; failure to satisfy an authoritative request never
silently demotes it to ephemeral. `--ephemeral` is explicitly non-authoritative,
uses temporary custody, mints no authoritative commit receipt and cannot satisfy
baseline adoption, repair or authoritative replay prerequisites.

The storage-root admission still applies the inherited sync, backup and private
custody classifications separately. A detected backup-managed root requires an
explicit storage-policy choice before the first source-derived write (TM V17):
select another admitted root, choose explicit ephemeral mode, or acknowledge
backup custody for this invocation with `--allow-backup-custody` (or the
corresponding already-admitted host storage-policy record). CI never prompts;
without that explicit choice it refuses REQUEST.PRECONDITION_FAILED with detail
`storage.backup-choice-required`, before creating evidence. The acknowledgement
is retained as operational custody metadata; it does not alter semantic Run
identity or silently write a policy file. UNKNOWN backup status is disclosed as
unknown, never as not-backed-up. Purge never claims deletion of external copies.
Sync/upload roots and group/ACL exposure retain their separate admission rules;
a backup acknowledgement is not a network-export or shared-storage grant.

Exactly one per-project writer holds the lifecycle lease/fence through source
admission, evaluation and atomic commit. Read-only clients use a consistent
committed ledger snapshot and never wait while holding a lock needed by the
writer. Global trust admission and revocation use the security contract's lock
order. SQLite WAL, transaction settings, fsync/atomic-rename carrier and crash
reconciliation retain the reviewed lifecycle carrier's native obligations;
the reference model here tests the semantic transition, not OS durability.

Commit order:

1. Validate closure and independently replay proof; compute all final IDs.
2. Write immutable blobs and descriptors to private temporary files, verify
   digest/length, fsync files, atomically publish under digest, fsync directories.
3. In one synchronous ledger transaction insert Run manifest, object references,
   retained availability generation, baseline/other authorized pins and a commit
   receipt with ExecutionId, namespace, monotonic sequence, inventory digest,
   signer and immutable assurance; commit and satisfy the carrier's barriers.
4. Only then acknowledge commitment. Required rendering/delivery is later and
   cannot rewrite the Run. Receipt signing is operational custody evidence and
   excluded from semantic IDs; the receipt authenticates RunId and inventory.

A failure before step 3 publishes no authoritative Run. Orphan blobs are
unreferenced and eligible for GC after reconciliation. A crash after ledger
commit but before acknowledgement is `durability-undetermined` to the caller,
exit 4, with an ExecutionId for read-only recovery. Recovery checks the ledger
and actual objects; it returns committed or failed, never repeats a repository
mutation. Duplicate retry can share a Run but has a separate attempt receipt.
An acknowledged Run with missing/corrupt objects becomes partially available or
corrupt; the host does not pretend it was never sealed.

Sealed assurance is immutable: verified means exact identity+proof checks at
seal; verifiable also commits the verification closure; replayable also commits
all exact admitted producer executables and source/input closure. The default
authoritative profile requires replayable retention at seal. Current
availability is a separate monotonic-generation record: retained, partial,
expired, purged, corrupt or unavailable, with exact missing references and
cause. Availability may improve through verified restoration or regeneration;
sealed assurance and historical verdict never change. A query reports both.

Retention roots include every live Run's required closure, active baseline,
authorized repair prerequisite and backup/export operation pin. Automatic
expiry respects these pins and all independent policy bounds; it refuses a
new durable admission if the required closure cannot be retained within bounds.
A direct purge of a pinned Run refuses unless the explicit destructive purge
also revokes the named pins after disclosing consequences. That refusal has a
registered public projection and this contract does not restate it: the
foundation-owned detail `evidence.pinned` projects as `request-rejected`,
`REQUEST.PRECONDITION_FAILED`, exit 2, carrying the closed
`common.schema.json#/$defs/PinnedPurgeDisclosure` — the RunId, the complete
current `activePins` inventory sorted uniquely by `pinId`, and the three ordered
consequences `named-pins-revoked`,
`dependent-evidence-replay-unavailable`, `sealed-history-retained` — exactly as
**workflows-and-surfaces §12** specifies. No pin is omitted, truncated or
aggregated into a count. Neither that disclosure nor any flag confers authority:
a later destructive attempt still requires the explicit lifecycle authorization
and disclosure of its then-current complete pin set, and a changed pin inventory
requires renewed disclosure before destruction. Purge retains the
minimal sealed manifest, provenance and tombstone but deletes unshared evidence
bytes by reachability GC; shared bytes survive until the final reference is
removed. Purged is not deleted-history. The user may separately destroy the
whole project store/marker under lifecycle authorization; no indefinite privacy
claim is made for backups or exports already outside that store.

A retention decision never changes a fact, Coverage, finding or Run identity.
It never turns expired evidence into `no match`. Query of retained manifest is
allowed after purge and states evidence unavailable. Query requiring actual
proof, comparison baseline or repair input refuses with
REQUEST.PRECONDITION_FAILED and `evidence.{expired,purged,missing,corrupt}`
before evaluation (exit 2); inability during a selected operation is HOST.IO_FAILURE
with evidence detail (exit 4). Successfully admitted partial native inputs may
instead produce an indeterminate Run (exit 3) under the native and D9 contracts.
These are different event positions, not interchangeable error spellings.

Backup/export holds a read snapshot plus short-lived object pins, writes a
bounded relative-path inventory, hashes and verifies every object, then seals
the bundle. Import checks path traversal, symlinks, sizes, duplicate paths,
cryptographic identities and all referenced schemas before publishing anything.
Source provenance/authenticity is reported separately from hash integrity.
Trust floors, current authorization and local custody receipts are never
restored backwards from an evidence backup. Portable baseline details are in
the workflow contract. An import cannot silently claim a remote Run was locally
evaluated: its imported-custody receipt names origin and local verification.

## 6. Required implementation conformance

Reference checks cover exact numeric and canonical encodings, wrong-source and
wrong-Plan joins, identity changes for each semantic input, operational identity
exclusion, universal negatives under incomplete resolution, proof tampering,
retention/purge invariance and crash acknowledgement states. They additionally
assert the digest law mechanically: that every 64-hex field carries a registered
representation, that each new closed record reproduces an independently computed
canonical digest vector and moves under every single-field mutation, and that a
complete Run with a non-empty native context set closes while an altered frame, a
missing preimage, a wrong preimage, an unregistered H domain, a raw payload
offered as an H identity and a hidden input each refuse with a typed cause. They
also assert that a fully re-framed and re-keyed Run built around a context the
native boundary refuses — contradicting honored options, a compiler or runtime
digest outside the tool closure, an incomplete stdlib inventory, a component
digest that is not the retained tree's, a compiler version not from the manifest,
a universe contradicting its context, or a config graph or lockfile path outside
the snapshot — is refused with that boundary's own typed refusal string. They
exercise a complete Rust universe/fact/Coverage Run alongside the TypeScript one,
with the nested dependency, features, config-projection and prepared-output
records retained and joined; and they separate cache key construction from cache
hit admission, showing that a key needs no bytes while a hit needs the Run's whole
closure. Their source pins
and independent review are part of D-372. They do not qualify a native carrier.

Before shipping, the exact implementation must additionally demonstrate:
all supported platform fsync/SQLite/process-death cases; concurrent readers and
writers plus trust revocation; independent replay across machines; missing,
corrupt, stale and wrong-tenant closure rejection; hostile archive import; GC
with shared references; backup restoration preserving trust floors; and public
D9/CLI/JSON/SARIF/HTML/agent parity. Those are implementation acceptance criteria
under existing G gates, not unresolved design alternatives.

### Reference lifecycle joins

The reference store instantiates closed commit-receipt and availability records.
An availability transition increments generation and never rewrites a sealed Run
or its original assurance. Read-only `recover(ExecutionId)` inspects the committed
receipt after a lost acknowledgement and never repeats effects. Verified restoration
requires the same complete identity closure and replay result before availability
returns to retained; a regeneration mismatch refuses. Physical fsync, authenticated
receipt signing, shared-blob deletion and OS crash recovery remain implementation
qualification obligations; the reference transitions do not claim to execute them.

The security chapter's three lease modes refine the inherited single-writer rule:
immutable readers coexist with the append writer; exclusive migration/purge acquires
the writer lease and reader exclusion. No second writer is permitted.

At Run closure, every Plan-selected import re-admits its retained canonical SourceCorrespondence. An exact-snapshot import must name the Plan snapshot. VCS-revision imports require a retained, canonical admitted SourceMappingV1 to that snapshot, with inventory-matching source digests and the current clean revision; an unmapped/stale intake artifact may remain available for inspection but cannot be selected as an analyzed Plan input. Intake storage does not establish this source join. The authenticated importer/evaluator still owns payload-schema, observation-scope and polarity admission; rehashing an opaque import is insufficient. The reference closure reuses the same workflow import/mapping schema admission functions so the source law has one implementation.

The semantic grant's `prepare-code` operation is present exactly when it projects trusted-repository-code preparation principals. Their provenance comes from consumed admitted host-prepared inputs; no test-runner operation or principal is added. Verification/replay checks these immutable bindings without reusing expired operational grants.

The expected VCS build context is explicit, never inferred from the imported claim. The host may select one analysis-spec parameter whose schemaDigest is the raw SHA-256 of `foundation/import-source-context.schema.json` and whose payloadDigest binds canonical ImportSourceContextV1 `{schemaVersion:1, declaredBuildIds:[...]}`. These expected labels come from the separately admitted analysis request/build configuration; the importer cannot nominate its own expected labels. No parameter means an empty set; more than one is refused. Labels are declarations, not proof: source mapping remains mandatory. Run closure reconstructs workflow §4's binding from this retained parameter and the snapshot's VCS observation, then applies the same staleness function (both dirty flags, revision, expected build label and admitted mapping). A label not in the expected set is wrong-build and cannot become a Plan-selected import. The schema bytes and payload are retained with the Plan parameters for independent replay.

Snapshot capture consumes the same admitted boundary inventory as native discovery. The host obtains it from successful security discovery, passes it unchanged to native discovery/membership and the shared scope descriptor, and removes nested-repository, nested-project and directory-custody-excluded paths before opening or hashing snapshot source bytes. The remaining paths are only capture candidates: per-file custody, safe handles and exact hashing still precede source admission. Boundary exclusion anchors enter the Plan's scope descriptor and their operational provenance is retained beside it. The host reference join admits one inventory; caller-supplied alternative boundary lists or substituted marker sets are refused. Discovery's dependency-tree pruning is an analysis-unit rule; explicitly required native dependency read-set bytes require separate custody/closure admission and cannot cross a nested authority boundary.

Every Plan with selected import2 inputs also requires read-import in its semantic grant. This includes imported-inert preparation. Close_run enforces this operation/input join as well as prepare-code/principal equality; the later consuming-Plan admission separately validates the actual preparedResolution provenance.


The reference closure entry point reports a missing promised object/blob as EvidenceUnavailable carrying the closed operational-failed/HOST.IO_FAILURE/host-io termination with evidence.missing and the missing reference. It never emits a bare lookup error or turns missing witness bytes into a false predicate or admission rejection. This models the host's retained-byte/custody observation boundary. Untrusted malformed records still receive exact schema/identity admission refusal; an inventory of available retained bytes does not authorize rewriting the assurance of a sealed Run.
