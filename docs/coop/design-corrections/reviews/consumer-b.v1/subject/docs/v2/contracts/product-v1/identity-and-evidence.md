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
The grammar is the C-2 owner selector `c2-plan-stage-schema.v4.json`
`planIntent.wireTypes.executionId` (the unique EXECUTION-ID-V1 declaration).
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
lowercase `\u00xx` for other U+0000–001F controls; do not escape slash. Arrays
whose semantics are sets are sorted and unique by canonical item bytes.
Ordinal dependency arrays instead sort numerically; priority arrays such as
configuration `allowedScopes` preserve their declared order. Text maxLength
counts Unicode scalar values, while the descriptor byte cap remains independent.
U+007F and U+2028 remain unescaped.
Inventories instead sort by UTF-8 logical path; predicate proofs by
(ruleId, subjectId, predicateId); stage arrays by contiguous ordinal. Logical
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
canonical JSON string array. The selected detector closure defines the token
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
schema: it is 64 lowercase hex characters without a prefix. Plan carries
`capabilityManifestBytesDigest` (raw SHA256) as well as capabilityManifestId.
The host validates the committed CVE1 artifact under the effective
`delivery.v4.json` schema and recomputes capabilityManifestId as
SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes). `typescriptStdlibMerkleRoot` and
`rustcDevLlvmDigest` in native-context schema 2 are the 64-hex suffixes of
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

Auxiliary raw digests have producing rules, not caller-defined meanings:
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
analysis specification, semantic grant, VCS observation and predicate witnesses.
The grant ProjectId/scope must join the Run/Plan. Witness program bytes must be
retained; matching facts and coverage must come from its explicitly named input
views. Predicate input refs are a subset of evaluationInputRefs; evidence view
roots equal the named views and coverage roots equal their coverage union.
Every visited fact/scope and view/proof/execution/evidence/seal joins the current
source or Plan, including objects reached through typed Ref fields. Proof/finding
Ref domains exclude Run, evidence, seal and proof outputs. The native and workflow
registered payload adapters are separate trusted admission stages, not assumed
validated merely because an opaque digest exists. The finite reference fixture
uses a specifically declared small rule/coverage adapter, not the product DSL.

Native-context, import mapping/observation, policy, rule-program, waiver-set and
witness digests are raw SHA256 of canonical bytes under their specifically
registered native/workflow/predicate-witness schema. Blob bytes and source
inventories use raw SHA256 directly. Schema digests cover the exact complete
registered schema document bytes; transitive references are resolved through
the pinned registry closure without network retrieval. Native semantic universe
keys use the native contract's own versioned producing recipe; the descriptor
retains its raw payload digest separately where needed. A digest from one of
these encodings is never silently treated as a digest from another.

Waiver resolution selects the active admitted waiver set before pure evaluation
and retains that resolved set and its authority provenance; the evaluator does
not consult today's wall clock. Replay evaluates the historical sealed set;
new analysis and repair authorization resolve current expiry and revocation
again. A historical waiver result is never a fresh grant.

The complete closure includes bytes for each policy, waiver, rule program,
configuration, analysis specification, native context, capability manifest,
registered schema, import payload/mapping, fact payload, Coverage payload,
finding parameters and predicate witness referenced anywhere in this graph.
The host recomputes all blob hashes and all semantic identities, validates each
payload with the exact admitted schema and its semantic admission rules, and
rejects missing, extra authoritative roots, wrong-kind, cross-Plan/cross-source
or unresolved references. Unreferenced CAS blobs are not evaluation inputs.
Snapshot config/scope, Plan config/scope and native-context source correspondence
must agree. Every view's facts/scopes/Coverage agree on Plan source, universes,
relation/rung and producer; every source anchor must name an inventoried blob.
Coverage scopes partition the claimed universe without overlaps or omissions.
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
An atomic witness names no children; boolean witnesses name only earlier nodes
in the same subject/rule DAG. Predicate IDs are unique and the DAG is bounded
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
mismatch is `regeneration-mismatch`; it cannot replace the sealed Run. New
source or policy creates a new Plan/Run. Cache reuse requires equal cache2 key,
current admission of its closure and independent object validation. Expired or
revoked permission cannot be resurrected by a matching hash. A miss recomputes
normally; a corrupt hit is quarantined and disclosed before any permitted retry.

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
also revokes the named pins after disclosing consequences. Purge retains the
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
retention/purge invariance and crash acknowledgement states. Their source pins
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
