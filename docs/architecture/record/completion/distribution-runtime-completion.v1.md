# Distribution, runtime and developer contract completion

Author: Codex. Status: PROPOSED, awaiting independent review and application.
Scope: DR-101, DR-103, DR-107, DR-111, DR-120, DR-121, DR-125.

## 1. Incorporation and explicit supersessions

This is a V2 preview design successor, not a V1 freeze. On application it
incorporates the design sections of these recorded contracts: distribution-core-
inventory-contract.v16 (D-114), component-manifest-schemas.v11 (D-104), lifecycle-
generation-contract.v2 (D-107), compatibility-matrices-contract.v5 (D-103),
component-packaging-contract.v14 (D-108), monorepo-ci-contract.v16 (D-124), and
component-sdk-contract.v4 (D-110). The application manifest pins exact paths,
digests and selectors. Historical status, reviewGuidance, repair logs and
pre-recording authority disclaimers are provenance, not fresh decisions.

Only the reservations and rules expressly replaced below change. All inherited
requirements, refusal classes, positive behavior and named test classes remain.
This contract replaces the core-language, installed-tree accounting, adapter,
CI encoding, SDK API, compatibility window, lifecycle mechanism and manifest-cap
reservations. Trust/signature choices are supplied by the paired security
completion contract, not implicitly accepted here. No new control/provider wire,
sealed identity, evidence storage, self-update or extra analyzer role is added.

### Named reference-design reservation successors

Under D-367, the accepted recording of this contract expressly supersedes:

- D-108 **Decision**, “Adapter implementations remain reserved”, and
  component-packaging-contract.v14 **namedOpenDecisions OD-P1**, “Concrete
  packager, build tool, language toolchain, and command line”, owner
  “docs/v2/implementation/ after DR-120 is accepted and condition 5 authorizes
  blueprint work”: the reference adapter DESIGN is selected in §6. Production
  implementation remains the subsequent phase.
  The incorporated `adapterTemplate.doesNotChoose` list and `notAPackager`
  disclaimer remain historical descriptions of v14; this successor selects
  those reference interfaces/tools in §§6–7.
- D-110 **Decision**, “Exact SDK APIs/frameworks remain reserved”, and
  component-sdk-contract.v4 **reserved**, “exact SDK APIs and frameworks”:
  §8 selects the reference SDK interface and its schema bindings.
- D-310 **Decision**, “No concrete encoding is chosen. The six members remain
  explicit named open decisions” and “No concrete encoding becomes
  post-Condition-5 work without that further successor”: §7 decides CI
  provider, ownership-file encoding, selector command, cache keys, command
  invocations and toolchain. YAML implements this accepted interface later.
- D-311 **Decision**, “No concrete mechanism is chosen. The seven members remain
  explicit named open decisions” and “No concrete encoding becomes
  post-Condition-5 work without that further successor”: §3/§5 and the paired
  security schema decide journal, lock grammar, lease mechanism, solver,
  filesystem layout, publication and quarantine. Atomic same-filesystem rename
  is selected; no unreviewed equivalent is authorized.
- D-114's incorporated distribution-core-inventory-contract.v16
  **namedOpenDecisions OD-101-1**, “RESERVED ... This artifact does not mint
  Rust-as-core”: §2 selects Rust. **OD-101-2**, “Ceremony/thresholds/notarization
  remain a DR-101 decision”: the paired security-completion contract selects
  them explicitly as a DR-101 successor; this distribution document alone
  does not clear that obligation.
- D-314 **Adopted text item 7, Q3**, “Leave the DR-111 numeric windows RESERVED” is superseded by the full independent surface windows in §3; **item 12, Q8**, and D-315 **item 2, Q8**, “supply no cap values” are superseded by §4's bounded metadata measurements. D-314 **item 15, Q11**, “name no implementation language in this recommendation and do not treat Rust-as-core as decided” remains historical for that recommendation; this independently reviewed successor chooses Rust in §2. **Item 17, Q13** continues to route ceremony to a DR-101 successor: the paired security unit explicitly acts in that capacity.
- D-314 **Adopted text item 21, G3-G15**, “Leave the adapter implementation reserved and name no adapter”; **item 22, G3-G16**, “Leave G16 blocked”; and **item 23, G3-G18**, confirmed by D-315 **item 3**, “Leave G18 blocked, specify no quarantine format now” are superseded by the independently reviewed reference adapter, authoritative ownership carrier and lifecycle/quarantine design in §§5–7. Authoring and reviewing reference schemas/examples is design work; production implementation still requires condition 5.
- D-314 **Adopted text** Q12 and Q15's preference/authority classifications stand. Their reference-design decisions are now taken by the delegated pair through this scoped successor. The reference-design
  choices exist before condition 5; executable product construction does not.

The old historical entries remain accurate at their dates. This is the scoped
successor D-310/D-311 required, not a claim that their classification alone
closed design. D-056 gates 1–3 remain substantive: all schemas and fixtures
must be authored before acceptance. D-368 only joins recording steps.

A substitute must preserve these property classes and rerun their gates:

| Reference choice | Invariants a substitute must preserve | Execution owner |
|---|---|---|
| Rust core / bundled Node TypeScript | Pure evaluator boundary, no ambient runtime, immutable closure, same support matrix, installed/startup budgets | G01–G05, G14, G24–G28; release + host |
| SQLite journal / OS lease locks / rename | P-1..P-8; one durable selection; no use-after-GC; trust floors never roll back | G18; lifecycle + security |
| Deterministic solver and metadata encoding | Exact complete dependency closure, independent windows, byte-stable total order, all RJ/TC cases | G07/G08/G15/G18; distribution + compatibility |
| Rust packaging adapter | All OC-1..OC-9 and AT-* byte/profile/hermeticity obligations, no ambient tools | G15; release engineering |
| GitHub Actions / strict ownership JSON | Exact v16 selection fixed point, complete axis, independent releases, all SL slots | G16; CI + release engineering |
| TypeScript SDK / Rust host bindings | Host authority, exact provider/control wire, cancellation/teardown, no findings or exit setters | G20/G21/G24–G28; SDK + host |

Choosing a new reference architecture requires independent successor review;
patching its implementation within these contracts requires ordinary code review
and the same gate evidence. No substitute inherits qualification by name.

## 2. Core implementation and inventory (DR-101)

The reference implementation is a Rust 2024 workspace. G01 scores every offered compressed core download container independently on each platform: both macOS `.pkg` and `.tar.zst`, and Linux `.tar.zst`. Each must meet the existing ceiling; publishing a larger alternate container cannot bypass the gate. The distribution core
and semantic host initially share one native executable; the pure evaluator is
a separate library with data-only inputs and outputs. It receives no filesystem,
clock, process, environment, callback or network capability. The TypeScript
provider remains an independently versioned external process with its own
bundled runtime. Selecting Rust for the host does not activate the rustc_driver
analyzer role. A later language substitution requires equivalent contract and
budget evidence and a reviewed architecture successor.

Linux core targets are `x86_64-unknown-linux-musl` and
`aarch64-unknown-linux-musl`, linked static-PIE without PT_INTERP. macOS targets
are `x86_64-apple-darwin` and `aarch64-apple-darwin`; the core links libSystem
only. Required TCB verification helpers are separate processes with their own
signed closure. The bundled Node component's OS dependencies are declared
under DR-119. These reference build choices do not assert that a platform has
passed G22; the security completion contract supplies the selected profiles.

The implementation pins the exact Rust compiler distribution and Cargo.lock in
its tool-closure manifest, vendors dependencies, and builds with Cargo's
`--frozen` behavior. A floating `stable` or unpinned registry lookup is not a
release input. Compiler patch selection is release inventory data, not an
undecided architectural choice. No claim of bit reproducibility follows from a
lockfile alone: independent builds must compare the unsigned payload tuple.

Every mandatory file is classified as routing/configuration, trust, admission,
supervision, lifecycle, host semantics, evaluation or output. Runtime bytes,
license/notice material and mandatory data cannot be omitted from the inventory.
Platform TCB dependencies are listed separately under DR-126. Help/version and
metadata-only management cannot load the TypeScript component or project state.

### G02 installed-tree accounting (D-006 threshold-family successor)

The ceiling remains 80,000,000 bytes, inclusive, for each supported platform.
Measure a fresh immutable core installation with no previous generations and
before first-use cache creation. Include every mandatory core path, licenses,
runtime and data; exclude optional component closures and declared OS TCB bytes
only. Report component and aggregate sizes separately as already required.

Collect a no-follow inventory of every inode and path, including directories and
symlinks. A mandatory path not measurable is NON-PASS. Compute:

- `logical`: regular-file lengths, symlink-target UTF-8 byte lengths, plus exact
  extended-attribute name and value byte lengths. Count logical payload for
  every path, including hard-linked aliases; a shared digest is not a deduction.
- `allocated`: `st_blocks * 512` for each distinct `(device,inode)` plus each
  inode's extended-attribute name/value bytes once. Include directory blocks.
  Attribute allocation may already be reflected in blocks; this deliberately
  conservative extra charge is retained rather than platform-specific guessing.
- `budgetBytes = max(logical, allocated)`. Equality passes; one byte over fails.
  Report both inputs, all link relationships and the path-to-inventory join.

Deduplicated inventory nodes cannot omit paths. Reflink/compression savings
cannot lower `logical`. Filesystem directory/allocation differences remain
visible in `allocated` and every platform must pass. Metadata such as inode
tables not attributable through these measurements is reported as filesystem
overhead, not silently claimed included. Modes/owners/timestamps are validated
metadata, not added as invented byte charges. Unexpected/unreadable xattrs fail
the inventory, rather than being dropped. Integer arithmetic is checked u64.

## 3. Compatibility and lock resolution (DR-111, DR-103)

Versions belong to independent surfaces. Initial preview writers are core
release `0.1.0`, root/index/manifest/lock schema major 1, common control major 1,
TypeScript provider major 1, and preview component-state major 1. The Rust
provider's existing major 2 is recorded as unshipped; no role API is invented.
Evidence formats are deferred under D-002. A schema version coincidence does not
require releases to share a version.

For each shipped schema/protocol/state surface, the writer emits its declared
major and the reader accepts exactly that major: `[1,1]` initially. S-CORE
contains two separate values: release SemVer `0.1.0` and core-state schema
major 1. The initial component release constraint admits host `[0.1.0,0.2.0)` with
inclusive lower/exclusive upper bound. All 0.1.x host patches preserve the
accepted API and coreState1; a breaking change requires an explicit compatibility
successor. Thus a core-only 0.1.1 update can retain the same component release.
The `[1,1]` reader
range applies to core state, never to release SemVer major 0. Both are pinned
in each resolved tuple, separately from component state S-STATE. A future-major
message is explicitly refused using the frozen refusal envelope; no permissive
parse or downgrade. Protocol compatibility requires BOTH independently
declared ranges to intersect; select the highest mutually supported integer
already permitted by the lock. No intersection refuses before role dispatch.

Reader support is guaranteed for 90 days after a same-major preview minor is
superseded, and at least one subsequent host minor release, whichever is later.
That duration is a support policy, not a promise that a new major reads old
state. Cross-major automatic migration and upgrade continuity remain absent
(D-018/D-010). Each replacement writer must either retain the required reader
or retain the previous signed executable as a selectable generation. It cannot
delete a supported reader while calling the window satisfied. Security
revocation overrides availability: a revoked reader is refused and the support
exception is reported. Alias windows remain D-012's existing 90-day/one-minor
rule, independently of these per-surface windows.

The supported `versionConstraint` grammar is a SemVer 2.0 exact version or a
closed lower/upper interval object `{min,max,includeMin,includeMax}`. Wildcards,
caret, tilde, OR expressions and implicit prerelease inclusion are refused.
Prereleases are selectable only by an exact version or a constraint explicitly
naming a prerelease bound with the same core version. Build metadata never
alters SemVer precedence but distinguishes exact release bytes.

Resolve against one authenticated index snapshot, platform, host version,
project/global scope and input request. Evaluate complete dependency constraints
before publishing. Search candidates in descending SemVer precedence, then
ascending full UTF-8 version bytes, the provenance tuple `(publisher UTF-8 bytes, sourceClass UTF-8 bytes)`
and manifest digest for ties. Project candidates precede same-ID/provenance
global candidates; that selection preference is separate from output order. Backtrack deterministically; never select an unsatisfiable highest-only
partial closure. Reject cyclic required dependencies. Limit candidate visits to
100,000 and dependency depth to 64; exhaustion is a named resolution refusal,
never a partial lock. Prefer project scope where D-012 permits shadowing; global
fallback is permitted only for an admitted identical identity/provenance with
all constraints satisfied. Untrusted or missing dependencies refuse; no network
acquisition occurs implicitly during resolution.

`versionConstraint` in the inherited manifest dependency and lock request
fields explicitly changes from string-only to the closed string-or-interval
grammar in `version-constraint-schema.completed.v2.json`. Version integer
components compare as arbitrary nonnegative decimal integers, never lossy JSON
numbers; leading zeros are invalid. `min > max` or an empty interval refuses.

The resolved tuples extend the DR-103 lock shape as concretized in
`component-lock-schema.completed.v3.json`. Each tuple adds closed
`selectedCompatibility` fields for the active surface majors; resolutionInputs
adds the current public `permissionPolicyDigest`, which identifies policy
bytes, never consent or a grant. It additionally pins `registryViewDigest`, the domain-separated digest of the immutable scoped registry view, while `indexDigest` pins exactly one signed release catalog snapshot; the view scopeContext must equal the lock scopeContext. A local admitted registry is host custody, never release-signed authority. Catalog `hostCoreConstraint` must structurally equal the manifest `compatibility.hostCore`; any inequality refuses at the signed catalog/manifest join before selection (COMPATIBILITY-CATALOG-JOIN), even if both ranges happen to admit the current host. The v5 signed selector executes this condition. It also pins hostCoreStateMajor,
compatibilityPolicyDigest, canonicalProfileId, and scopeContext with the
projectKey plus the ordered allowed scopes. A null projectKey permits global
only; a projectKey admits project-before-global resolution. The preview fixes
requestedProfile to `preview-typescript` and requestedCapabilities to the five
sorted host capability IDs; these are provider admission requirements, not
permission for the pack to require unrelated analysis rungs. Explicit pins and
holds contain exact stableId/version pairs, sorted by stableId then version;
duplicate/conflicting pairs refuse. They constrain already-requested dependency
closure members and do not add roots. A dangling pin/hold refuses. Request
arrays are similarly sorted and duplicate IDs refuse, so logically identical
requests have identical declared bytes. All these resolution-affecting inputs
are serialized, rather than read from ambient local state. The old `exclusionsRecorded` statement is now
the exact fixed literal in that schema. Metadata-schema validation does not
replace dependency closure, signed admission, tuple sorting or current trust
checks. `compatibility-matrix.completed.v4.json` retains all eight inherited
surfaces, adds the independent S-DOCTOR machine-output surface, and fills all six cells; unshipped/deferred surfaces have explicit
dispositions, not invented writers. Sort by canonical lowercase
UUID bytes, SemVer precedence, full version UTF-8 bytes, scope (`global` before
`project`), the provenance tuple `(publisher UTF-8 bytes, sourceClass UTF-8 bytes)` and
manifest digest. String comparison is unsigned UTF-8 byte order, never locale
or JSON-escape order. Duplicate tuple
keys with different digests refuse. Canonical serialization uses the paired
security contract's metadata profile. Locks now pin exact schema/control/state
majors and permission-policy references; a live handshake only confirms the
pin. These are selected-input custody records, not authority grants or sealed
Run identities. Lock production becomes active only when both this contract
and the security metadata profile are applied.

## 4. Metadata limits and portable paths (DR-103)

Adopt the following inclusive limits, under DR-115's product/release ownership:
manifest UTF-8 bytes 4,194,304; tree entries 100,000; path UTF-8 bytes 1,024;
aliases per component 64; commands 4,096; command nesting 32; JSON nesting 64.
Bytes are counted before parsing; aliases include every element, before any
deduplication. Reject duplicates rather than reducing the count. Apply all
limits together. No automatic truncation or oversized-input waiver is allowed
at admission. An explicit future threshold successor may revise a limit.
The same byte/nesting limits apply to one lock and one signed index document;
larger index inventories require a future explicit pagination schema.

These limits bound metadata admission, not payload sizes. Archive-profile.1's
100-byte ustar path and link-target capacity remains a separate stricter
packaging constraint. A 101-byte manifest path can be structurally admissible
but cannot be emitted under that archive profile. The adapter reports that
specific refusal; it cannot silently use PAX, GNU extensions or a different
archive format. The 100,000-node ceiling bounds the abstract tree even when the
manifest byte ceiling is reached first.

Apply the inherited no-absolute/no-dot/no-parent/no-backslash/no-NUL/no-empty-
segment path rule. Require NFC; never normalize a supplied path and thereby
change signed bytes. Compare paths for collision using NFC of Unicode full
case-folded NFC segments. Reject both members of a collision before extraction.
Freeze the collision table at Unicode 15.1; the implementation vendors it as a
declared core data dependency. A later Unicode revision is an explicit schema
successor, not a library-update side effect.

For portable archive safety, reject a segment ending in dot or space, or whose
basename before the first dot, case-insensitively, is `CON`, `PRN`, `AUX`, `NUL`,
`COM1`..`COM9` or `LPT1`..`LPT9`. Apply these lexical rules on all four platforms;
the retained Windows examples do not claim Windows support. Reject any symlink
chain that escapes the tree, forms a cycle, or resolves through an undeclared
entry. Extraction uses directory-relative no-follow operations into private
staging; verification opens the same immutable objects later used for launch.

The Unicode duplicate case is explicitly constructible: two individually NFC
names whose full case folds coincide, such as `Straße.ts` and `STRASSE.ts`, are
refused as a collision. A decomposed `e\u0301.ts` separately tests non-NFC
refusal. This replaces the earlier claim that Unicode-normalization collision
evidence must remain unauthorable until a schema successor exists.
For the inherited TC-PATH.11 normalization pair, the metadata path preflight
collects both non-NFC and normalization-collision diagnostics before returning
RJ-3. This is an explicit diagnostic-collection successor; it never normalizes
or admits the supplied bytes. The separate NFC case-fold pair above isolates
collision checking without requiring a non-NFC input to pass an earlier check.

OD-2 remains the recorded do-not-fold decision; existing conditional evidence
shapes stay readable. Signature ENVELOPE_MISMATCH activates with the security
profile, and its concrete mismatched-preimage case must be retained. No
signature acceptance is inferred merely from a matching digest.

## 5. Generations, publication and recovery (DR-107)

`host-foundation-completion.v1.md` concretizes the separate immutable core payload and per-user operational install root, ownership/discovery, project-filesystem support and configuration/policy carriers. Its exact paths and scoped refusals supplement the carrier rules here; a system package never requires shared mutable per-user trust.

Use a host-owned SQLite lifecycle database with WAL, full synchronous commits,
and foreign keys enabled. Each install root also has a permanent host-owned
advisory-lock file. All lifecycle writers and garbage collection take the same
exclusive lock; readers acquire a generation lease before releasing that lock.
SQLite is operational metadata, not an evidence backend. Its exact library
version is a pinned core dependency and counts toward the core budget.

The database schema consists of `generation(id, manifestDigest, lockDigest,
platform, state, trustEpoch)`, `project_selection(projectKey,generationId)`,
`operation_lease(leaseId,generationId,supervisorBootId,processStartToken)`,
`transition(txId,oldGeneration,newGeneration,phase)`, and
`quarantine(generationId,reason,observedDigest)`. IDs here are random local
operational keys; none is a PlanId, RunId or evidence identity. Integer IDs and
phases are schema-checked; foreign keys prohibit dangling selected generations.
Selected manifest/lock digests commit exact bytes under the metadata profile.
The exact carrier is `lifecycle-carrier.schema.v2.sql` with the accompanying
`lifecycle-carrier.contract.v2.json`, including a sixth `project_registry`
table for host-owned project-root/namespace binding. The registry verifies the
opened root object's device, inode and birth identity; a caller-supplied known
key cannot select another root's namespace. Project-scoped locks must match
that project; only a global-only lock can be shared across projects.
`trustEpoch` carries the SC-TRUST versions used at verification; it is not a
grant generation or a permission grant. A changed trust state always requires
current-trust re-verification, including revocation changes even when root and
index versions remain equal. The security successor owns the complete epoch
tuple and the durable grant-journal/witness protocol. `lifecycle.sqlite` and
`trust.sqlite` are separate files; per-project journals live in the host-owned
project state namespace. No multi-database SQLite atomicity is assumed.

Publication sequence, under the lifecycle lock:

1. Record PREPARING for a fresh private staging directory; write and verify
   every declared object, close writable handles, fsync files and directories.
2. Record VERIFIED with the exact lock and manifest digests. Recheck current
   trust and permission policy. The generation remains invisible to projects.
3. Rename the staged directory to an unused immutable generation path on the
   same filesystem, then durably sync its parent. Never overwrite an existing
   generation. Record READY only after durable publication of all tree bytes.
4. In one SQLite transaction, compare the project's old selected generation,
   replace that selection with the READY generation and mark the matching
   transition COMMITTED (the immutable generation remains READY).
   Readers obtain the whole closure through this one selection. There is no
   separately mutable 'current' symlink that could disagree with the database.
5. Acknowledge success only after the durable database commit. Failed
   compare-and-swap retries from resolution; it never mixes old permissions
   with new executables. The previous generation becomes a rollback root.

Startup recovery holds the lock. PREPARING/VERIFIED entries without a durable
READY tree are quarantined, never selected. An orphan complete tree may be
verified and retained for retry; it cannot become selected by directory name.
A committed selection is used only after exact verification under current
trust. An unreadable database, torn/corrupt tree or ambiguous state refuses
analysis and enables read-only doctor reporting. Trust floors are stored
separately and never restored from a lifecycle rollback.

Each running supervisor owns a dedicated lease-lock descriptor for the entire
operation. Process death releases the OS lock; persisted lease rows are reaped
only after proving that lock is no longer held. PID alone is not proof because
of reuse. A child cannot inherit the lease capability. Garbage collection holds
the lifecycle lock while checking project locks, operation leases, prepared
migrations, rollback slots and operational records; any unresolved reference
prevents deletion. Quarantine is a database state and isolated directory, never
a fallback executable source. Cross-filesystem staging is refused.
Lease/root census uses nonblocking lock inspection while holding the lifecycle
lock. A busy operation remains a retention root; collection never waits for it
while preventing that operation from acquiring the lifecycle lock to finish.

Cache migrations rebuild into a new generation and never mutate the old cache.
Operational schema migration is copy-on-write before READY; a failed prepare
discards the candidate. The preview has no irreversible authoritative-state
migration. Generation rollback selects a previously verified compatible tree
under current trust and acquires fresh leases. Core self-update and repair-media
rollback remain the existing DR-110 deferral; fresh signed core installation is
the preview update path. The DR-101 'updates' inventory slot is explicit
unexercised metadata/status support, not a self-updater.

## 6. Concrete packaging adapter (DR-120)

Select a Rust implementation of `opensip-build-adapter` and a TypeScript adapter
profile that bundles a normal Node.js 24 LTS runtime, the pinned TypeScript
compiler/library closure and provider JavaScript. The initial reference compiler
line is TypeScript 6.0.3, matching the pinned prototype Program service; the
retained native corpus uses that exact version. Future compiler changes must
pass the same G13 corpus and explicit capability matrix without silent regression. No user-managed Node, npm,
compiler or network download is required at runtime. The host invokes the
bundled absolute executable path with a fixed argument vector and cleaned
environment. Node single-executable packaging is not selected because the
Node 24 documentation excludes macOS x64 from that feature's tested support.

Build-time acquisition is a separate explicit job. It verifies signed/digested
tool inputs and produces the offline tool-closure manifest. The adapter consumes
that closure with network disabled and no ambient PATH resolution. Its stages
remain S-1-COLLECT, S-2-NORMALIZE, S-3-EMIT, S-4-VALIDATE. Runtime/TypeScript
patch releases are pinned by digest per release, with no shared version coupling
to the host, SDK, protocol or component. Supported patches must remain within
the security-supported Node 24 line; moving the major needs compatibility and
quality evidence, not a user runtime prerequisite.

The command interface is `opensip-build-adapter build --inputs <manifest>
--target <platform> --out <empty-directory>` and `validate --inputs <manifest>
--out <directory>`. Paths are explicit inputs, not shell fragments. Production
build never invokes the hostile-fixture generator. The reference archive encoder
implements the inherited exact profile. No general system `tar` defaults are
assumed equivalent. Native code signing/notarization occurs in the security
release phase before final payload digests and archives are committed; signed
timestamp-dependent bytes are not falsely described as build-reproducible.

The `--inputs` document is a closed build-only record with exactly
`inputsSchema: 1`, `componentManifest: {path, sha256}`,
`sourceInventory: {path, sha256}`, `toolInventory: {path, sha256}`,
`declarationInventory: {path, sha256}`, and `target`. Every inventory is a
closed array of `{path, sha256, length}` regular-file entries, with unique
relative paths and the same no-traversal/byte-bound rules as §4. All paths
resolve below the explicitly mounted read-only input directory; no symbolic
link or implicit parent traversal is allowed in build inventories. The full
component manifest supplies the intended output tree and declaration members;
the adapter must reproduce their bytes and digest values, never silently
rewrite an input identity or bless a mismatched build. A publisher preparing
a new release first computes that proposed manifest from its own build; the
hermetic adapter reproduces it as the release qualification step. This does
not require a pre-existing release signature.

The selected TypeScript build tool is the pinned compiler's `lib/tsc.js`,
invoked by the pinned bundled Node tool with literal arguments `--project
provider/tsconfig.json --outDir staging/lib`, from the declared source root.
The config and all transitive compiler inputs must appear in source/tool
inventories; a read outside them refuses the build. Runtime Node and required
compiler/library files are copied from the tool inventory into the manifest's
declared closure. Build inventory bytes use the security metadata canonical
encoding with ordinary SHA-256 file custody, not a signed release-inventory
envelope or its authority. They contain no signing secrets. Build-only `target` must equal the
CLI target and a manifest platform alternative. Target mismatch, missing
input, content mismatch, unknown input member or incomplete declaration
inventory is a build refusal before emission.

The build invocation's proposed manifest commits the unsigned build tuple and
is build evidence only, never an install-admission artifact. The subsequent
security signing phase produces a separate final manifest over signed Mach-O
bytes and final declarations, preserving component identity/version and
retaining the unsigned-to-signed custody join. `validate` of the final release
uses that final manifest as its input expectation. It checks exact signed
bytes and signatures; it does not demand timestamp-dependent signed-byte
equality from a second compiler run. Reproducibility is measured before this
explicit signing transformation, as §2 and the security ceremony require.

Admission consumes the same OC-1..OC-9 tuple and conformance-report fields on
every platform. Extend DR-103's signed index release artifact list to include
`archiveProfileId` and `archiveDigest` for each platform; the detached signature
binds that list. This activates ID-DEP-P9 without inventing a Merkle tree root.
The existing treeDigest/report binding point is a plain digest of the profile's
exact serialized tree manifest, named as packaging custody only, not a sealed
TypeScript stdlib or Plan identity.

## 7. CI encoding and release independence (DR-121)

Select GitHub Actions as orchestration. Actual action revisions and runner
images are digest/commit pinned release inputs; no mutable action tag can sign
a release. Untrusted pull-request jobs receive no release signing authority.
CI YAML invokes `opensip-ci-select --ownership <json> --base <git-tree>
--head <git-tree> --out <result.json>` and the §6 adapter, identical to local
validation. Selector success writes all selected/skipped slots; missing data
writes REFUSE and exits nonzero. These are build-tool exit statuses, never D9
product codes. YAML
path filters are only scheduling hints; they may never skip the selector.

The compiled authoritative ownership carrier is strict JSON, schema major 1, containing
previous/current tree IDs, an explicit component-identity set, each tracked
source path's exact owner list, DR-103 dependency edges, shared-surface consumer
sets, role applicability, validated platform sets and the fixed multi-component
predicate. Source units are normalized repository-relative POSIX paths from Git
trees, including deleted paths from the comparison baseline. No glob's order or
'last match wins' determines ownership. Every path must be classified, including
build and workflow files. Documentation-only paths have an explicit shared-core
owner; they may cost a core check but cannot silently disappear.

The exact carrier is `ci-ownership-schema.v1.json`; `ci-carrier-contract.v1.md` defines its source record `.opensip-ci-ownership.json` and nonrecursive source-blob digest calculation. `baseTree`/`headTree` are
resolved Git tree object IDs; the selector independently reads the complete
tracked unit and component sets from those trees and compares them with the
carrier. Independently read ownership records are pinned by
`previousRecordDigest` and `currentRecordDigest`; a changed record expands the
source change set to all previous/current owned units. The complete
pre-mutation corpus basis is pinned by `fixtureDomainBasisDigest` and checked
against the independently retained basis. `dependencyManifestDigests` bind independently verified manifest
dependencies; a self-declared `complete` or signature boolean is not an input.
The previous/current union must equal the key set for dependencies, roles,
platforms and manifest custody. Roleless build components carry an empty role
list, mapped exactly to the inherited ROLELESS-NA sentinel; active analyzer components carry `analyzer`, with all selected platform
members explicitly enumerated. Shared owner tokens are the six closed shared
surfaces. Every other owner and consumer is a stable UUID from the union.
Missing/unknown owners, incomplete maps or mismatched custody refuse before
the complete-conflict branch can select all. The fixed example binds the two
fixture display names to stable UUIDs; display labels never replace identities.
`check_ci_carrier_design.py` retains 24 concrete admission/ambiguity cases;
the existing 26 selector scenarios exercise the subsequent selection algorithm.

Preserve monorepo-ci-contract.v16's algorithm exactly: complete universe from
previous/current union; missing data REFUSE; complete ownership conflict selects
the whole universe; reverse-dependency/shared-consumer/predicate expansion to a
fixed point; two or more selected components also select SL-2/SL-3/SL-4.
SL-1..SL-6 result slots always exist. SL-5/SL-6 retain the existing authoritative
closure deferrals. The preview's offline install is independently tested in
G08/G15 and cannot vanish with SL-5. Every skipped lane has a reason.

Caches are acceleration only, keyed by tool-closure digest, target, lockfile and
source input digest. Every restored output is verified; a cache miss rebuilds
from the offline inputs, and unavailable inputs refuse. No cache key is a
semantic cache/regeneration identity. The compare baseline is the pinned merge
base for the complete candidate, never merely its last commit's parent.

The positive corpus has two independently versioned synthetic component IDs
with a declared dependency, plus a roleless CI build sentinel. The sentinel is not an installable component manifest; v11 still permits only role analyzer. Synthetic test
IDs do not add shipped roles. All four D-002 platforms are present. Tests also
delete a component, change ownership, omit a dependency, remove a platform axis,
remove the role axis, and mutate the fixed predicate. The pre-mutation domain
and complete expected selected/skipped sets are retained.

## 8. SDK contract (DR-125)

Select a TypeScript provider SDK plus Rust host bindings, with generated types
from the pinned existing control and TypeScript provider schemas. Generated type files are committed source-inventory members, accompanied by a manifest pinning their exact source schema digests; release builds verify that join and do not run an undeclared generator. A generator used to refresh them is a separately pinned development tool, never an implicit release input. The SDK is a
library within the component closure, independently versioned from its wire
major. It is not a general plugin execution framework. Expose these typed
operations; the argument/result types are existing protocol schema types:

```typescript
interface ProviderSession {
  readonly effects: BrokerEffects;
  requests(): AsyncIterable<HostRequest>;
  respond(response: ProviderResponse): Promise<void>;
  emitFacts(batch: FactBatch): Promise<void>;
  emitCoverage(coverage: Coverage): Promise<void>;
  reportFault(fault: ControlFault): Promise<void>;
  reportResources(resources: ControlResourceReport): Promise<void>;
  complete(completion: ProviderComplete): Promise<void>;
  cancellation: AbortSignal;
}
```

`BrokerEffects` supplies two disjoint SDK-owned opaque handle lists and two
methods: `writeHostState(HostStateWriteHandle, Uint8Array)` and
`readProject(ProjectReadHandle)`. The precise local outcome unions and handle
brands are the paired broker SDK contract's `broker-sdk-api.v1.ts`; write
completion exposes the validated commit class, read completion exposes a fresh
byte array, and both preserve REFUSED/FAILED/INDETERMINATE distinctions. The
SDK's raw `requestEffect` is private. A provider gets no scratch path, resultRef,
sequence setter, operation target or grant-scope setter. The write input is
copied before asynchronous dispatch; a read yields bytes only after successful
response correlation and the security courier's length/digest/custody checks.

The inherited `broker-bootstrap.contract.v2.md` fixes per-grant/per-spawn maps,
both required permission tokens, exact argv/environment and startup failure.
The security §7.4/§7.5 successor and the paired broker SDK completion add only
the bounded scratch-root/commit-class bootstrap metadata and typed byte courier;
they preserve the existing control/provider wire and shipped empty descriptor.
A handle from another SDK instance or of the wrong effect class refuses locally
before dispatch. The shipped TypeScript profile receives no handles. The final
application must pin the independently reviewed broker SDK schema/model/courier
unit alongside this API; this paragraph alone supplies no execution evidence.

These local names are SDK aliases, not new wire message tokens. `HostRequest`,
`FactBatch`, `Coverage`, and `ProviderComplete` bind respectively to delivery.v2
`typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas`
the discriminated union of `OpenUniverseV1`, `SnapshotManifestV1`,
`SnapshotFileChunkV1`, `SnapshotSealV1`, `AnalyzeV1`, `CancelV1`, then
`FactBatchV1`, `CoverageV1`, and `CompleteV1`. `ProviderResponse` is the closed
union of `UniverseAcceptedV1`, `SnapshotAcceptedV1`, `FactBatchV1`, `CoverageV1`,
`UnavailableV1`, `BudgetExhaustedV1`, `CompleteV1`, and `CancelledV1`. Its
discriminator and exact field grammar come from those schemas; it is not an
open arbitrary message. Convenience methods encode precisely the corresponding
response member and share one serializer. The SDK owns HelloV1/HelloAckV1
exchange before yielding requests, and owns common-control selection, liveness
and shutdown; caller code cannot send those frames directly. Caller responses
are admitted against the existing stage machine before serialization. The
sealed snapshot messages expose their declared byte payloads, not a raw project
filesystem handle. ControlFault and
ControlResourceReport bind to `fault` and `resourceReport` bodies in the
control-protocol completion schema. No generic progress frame is introduced;
the host derives progress from admitted stage/counter observations. Non-authoritative
diagnostics may use the existing bounded stderr channel and carry no protocol
meaning. The SDK owns framing,
backpressure and cancellation delivery; the host validates every received
message independently. Write calls serialize, enforce the negotiated bounds,
reject after terminal completion/cancellation and never hide dropped messages.

No SDK method sets a finding, verdict, policy outcome, host exit, admission,
trust decision or sealed identity. No public raw filesystem/network/process
capability is handed to provider code by this SDK. The bundled TypeScript worker
uses only the declared, host-authorized inputs and runtime closure. Secret
handles remain deferred with DR-108. The SDK capability declaration uses a
host-owned registry; DR-118 freezes the initial supported capability entries.

DR-103 ID-DEP-12's configuration classification vocabulary is now closed to
`host.analysis.semantic` and `host.operability.nonsemantic`. The former feeds
the existing resolved Plan input semantics; the latter is permitted only for
an explicitly host-reviewed operability field and cannot hide an analysis
input. The initial shipped TypeScript configuration field map is empty: the
worker receives its analysis request and sealed snapshot through the existing
protocol and admits no additional private settings. A manifest cannot approve
its own classification or introduce another precedence layer. Adding a
configuration field requires a reviewed host-owned mapping. Optional future
configuration declarations retain a bounded, closed JSON-Schema subset with
no code hooks or arbitrary regular expressions; synthetic mapping fixtures
exercise that structural contract without adding a shipped setting. This is
a vocabulary/validation successor, not activation of deferred DR-106 state or
an identity digest recipe.

### 8.1 Doctor mode and budget successor (DR-114 ID-DEP-3/8)

The file-02 falsifiable-small publication sentence “evidence that
help/version/config/status/doctor load no project or component” is superseded
only for doctor: **core mode reads no project; project mode reads strict
configuration and the selected lock, but neither mode loads component code,
reads project source for analysis, constructs analysis inputs, or executes a
provider**. File-04 project-mode behavior and doctor v4's no-silent-downgrade
rule stand. An unreadable selected project remains project mode with explicit
UNDETERMINED checks. This settles doctor v4 tensionsObserved T-2; it does not
reinterpret the no-project guarantee for help/version.

Both read-only doctor modes carry D-006/D-293's existing steady RSS ≤60 MB
and peak RSS ≤100 MB, where MB = 1,000,000 bytes. G04 measures **each** of core
(no project), explicitly requested core (hostile project present), healthy
project, and unresolved project separately: 21 launches per mode per D-102
platform, existing 10 ms sampling, steady median at/after 20 ms (median of all samples if the process exits before 20 ms), each sample
scored, no warm pair. G12 process/read traces verify the mode boundary and
that limits cause explicit incomplete checks rather than omitted work. G03's
startup thresholds continue to apply to help/version; doctor startup is
retained telemetry under G12, with no invented inherited latency bound.
Consented-probe runs remain outside the read-only G04 RSS budget and retain
their declared probe/resource constraints.

The budget owner remains Product + Release engineering. The reason for keeping
the same RSS limit on both read-only modes is that bounded metadata parsing
does not need a language runtime or project graph. Falsification is a retained
G04 trace over the four mode fixtures exceeding either threshold; change then
requires an explicit reviewed D-006 successor, never a silent mode exemption.

`compatibility-matrix.completed.v4.json` adds S-DOCTOR: writer schema major 1,
reader major 1, the independent 90-day **and** one-subsequent-host-minor support
window, no cross-major downgrade or bridge. Unknown report major is refused
as an unsupported doctor report by its reader before rendering any member;
it never becomes a healthy report. G12/G20/G32 run current-major, malformed,
future-major, and support-window cases. Doctor's output major is independent
of core, control and component-state versions.

### 8.2 Preview cache regeneration decision (DR-124)

The preview does **not reuse analysis results from durable cache**. Every
analysis invocation obtains a fresh sealed input and recomputes provider facts,
Coverage and host evaluation. SC-CACHE remains active for verified downloads,
compiler/runtime scratch and disposable operational acceleration; neither its
bytes nor a cache hit is accepted as analysis evidence or a policy result.
Download reuse is admitted only after checking exact stored artifact digest,
current signed catalog/manifest binding and current trust, using the same
byte admission as a newly received archive. Within one live analysis process,
ephemeral working memory may be reused only under that invocation's existing
input binding. It is never restored from prior durable state.

This expressly disposes SC-CACHE-REGENERATION-KEY for the current preview:
no active durable analysis-result producer or consumer requires the deferred
DR-006 recipe. It does not defer the cache class or invent a replacement
Snapshot/Plan/Run identity. Re-entry of durable analysis-result reuse must
supply the reviewed key and equal-recompute evidence before activation.
G18 tests absent, stale, corrupted and attacker-populated cache directories
against one fixed admitted analysis input: all semantic outputs equal fresh
recomputation; G08/G15 reject an artifact-cache hit with mismatched digest or
revoked trust. Owners: Lifecycle + Semantic host + Security. The class matrix
contains five classes total: SC-EVIDENCE/SC-ANALYSIS deferred, SC-CACHE/SC-OPS/
SC-TRUST active.

## 9. Evidence and qualification boundary

Before application, retain concrete acceptance cases and independent expected
results for metadata limits, path collisions, version selection, incompatible
lock rejection, archive bytes/capacity, CI selection and lifecycle crash states.
Reference models may run as design evidence; they are not the production
implementation and cannot qualify a platform. The application manifest maps
every prior leftover obligation to a decided clause, authored case or existing
scope disposition. Any unmapped obligation keeps its row open.

The remaining release work is production harness implementation and execution,
OS filesystem and process fault injection, actual signed inventories, performance
measurement and four-platform end-to-end qualification. No QUALIFIED or shipping
claim is made by this contract. Future package/tool hashes are measured release
inputs with a defined schema and rejection rule, not missing architecture.

## 10. External design references

Primary documentation checked 2026-09-04. These support implementation choices;
they do not assert that OpenSIP has executed or qualified them.

- Cargo's frozen dependency behavior: https://doc.rust-lang.org/cargo/commands/cargo-build.html
- Node 24 support lifecycle: https://github.com/nodejs/Release
- Node 24 single-executable platform limits: https://r2.nodejs.org/docs/latest-v24.x/api/single-executable-applications.html
- GitHub Actions immutable action pinning: https://docs.github.com/en/actions/reference/security/secure-use

- SemVer grammar and precedence: https://semver.org/spec/v2.0.0.html
- SQLite commit synchronization: https://www.sqlite.org/pragma.html#pragma_synchronous

The compatibility evidence combines `compatibility-design-cases.v2.json` and
`check_compatibility_design_v2.py` with the independently authored
`compatibility-selection-cases.v3.json` / `compatibility-selection-model.v3.py` for the preserved solver core, plus the separately reviewed signed catalog/registry-view v5 integration unit (`g15-conditional-contract.v2.md`).
The latter includes an actual multi-component reference lock and artifact-byte
mutation cases. Both remain reference design models; final admitted metadata
byte serialization and signature preimage examples join the paired security
profile before DR-103/DR-111 closure.

`compatibility-matrix.completed.v3.json` supersedes only v2's illustrative
exact initial host constraint with the patch-compatible interval above; v2's
separation of release and state remains. Exact-version constraints remain a
valid grammar choice for other explicitly constrained requests and fixtures,
not the initial preview provider's release policy.
