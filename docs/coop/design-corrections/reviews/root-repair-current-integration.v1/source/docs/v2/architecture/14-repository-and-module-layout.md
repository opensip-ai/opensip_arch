# Repository and module layout

Recorded 2026-09-10 from the user's agreement on repository organization, CLI
naming and the browser report. This chapter is the single current home for
those structural decisions and the remaining crate/package design. Its companion
file inventory owns the proposed target filenames and generates the tables below. It records
user-agreed direction; technical integration and independent review remain
pending. It grants no implementation readiness or authorization. The
[central register](08-decision-and-readiness-register.md#unified-product-design-readiness)
continues to own readiness.

The [implementation boundaries and build plan](implementation-boundaries-and-build-plan.md)
owns the concrete API handoff, private recovery record/failure matrix,
generation/build rules, tooling decision matrix and source-bound milestone coverage.
The [prototype report inventory](prototype-report-inventory.md) owns its 24
feature dispositions. These focused companions extend this layout without
creating alternate readiness records; both are author proposals pending Claude.

## Agreed organization

Settle the major package boundaries before implementation. Each package needs a
clear responsibility, public interface, permitted dependencies and build output.
Individual source files and small internal module divisions can evolve within
those boundaries during implementation.

The proposed product source tree is:

```text
apps/
  cli/                  Command-line application and host assembly
  report/               Browser report interface, styles and assets
crates/
  reporting/            Host-owned report projection and HTML assembly
  contracts/            Shared inert contract types (proposed)
  identity/             Pure canonical admission and identities (proposed)
  evaluator/            Pure evaluation and semantic replay (proposed)
  syntax/               Pure grammar parsing and clone candidates (proposed)
  platform/             OS mechanisms (proposed)
  security/             Trust, custody and grants (proposed)
  storage/              Retained evidence mechanics (proposed)
  components/           Component supervision and protocols (proposed)
  lifecycle/            Install/update/recovery coordination (proposed)
  host/                 Host authority and workflows (proposed)
providers/
  typescript/           TypeScript/JavaScript provider
  rust/                 Rust provider and its toolchain boundary
schemas/                Owned wire contracts and binding generation
tests/
  conformance/          Shared contract and compatibility checks
  integration/          Complete workflows across component boundaries
  qualification/        Platform and performance evidence requirements
tools/                  Build, release and repository maintenance
docs/                   Current product and developer documentation
```

This is the target organization for implementation. These directories have not
been scaffolded by this decision. It does not move the existing architecture
record or its pinned schema and evidence files. The initial inventory below
proposes crate boundaries and direct dependencies for review. Complete API,
workspace and build configuration decisions remain open.

### CLI names

Directory, Cargo package and installed executable have distinct purposes:

| Item | Agreed name |
|---|---|
| Source directory | `apps/cli/` |
| Cargo package | `opensip-cli` |
| Installed executable | `opensip` |

The CLI assembles and invokes host services. Its directory name does not move
semantic authority into argument parsing or presentation code.

### Report ownership and delivery

The browser report has its own source home at `apps/report/`. Report-specific
components, styles and browser assets stay together there. A generic
`packages/ui/` is reserved for a future demonstrated need to share visual
components between applications; it is not part of the initial package list.

`crates/reporting/` owns preparation of host-approved report data and assembly
of the HTML output with its built assets. The inventory now proposes the Cargo
package name `opensip-reporting` and one renderer module per applicable output
format in that crate. Those refinements require technical review; only the
directory and report responsibility were agreed in the initial discussion.

The responsibilities follow the existing
[workflow output contract](../contracts/product-v1/workflows-and-surfaces.md#8-command-inventory-outputs-and-parity-ar-13-surfaces-ar-16):

1. The admitted analysis and host evaluation produce findings, evidence and
   assessments under their existing authority rules.
2. The host prepares the declared report projection. Reporting code preserves
   those values and assembles the deliverable.
3. The browser interface presents the embedded data. Any agreed filtering or
   navigation changes presentation, without recomputing policy or changing the
   underlying findings, evidence, verdict or completeness disclosures.

The selected HTML deliverable remains a self-contained, offline file with its
data embedded and no script-fetched data. It requires no separately running
web server. Building `apps/report/` produces assets for that deliverable;
placing its source under `apps/` does not select a hosted service, server-side
rendering or a separate installation. The companion build plan now specifies exact asset-manifest and signed host
release-artifact joins under the offline delivery contracts; those corrected
bytes require review. No frontend framework or bundler is selected
by this directory decision.

The prototype's source has now been inventoried at its pinned commit in the
[report inventory](prototype-report-inventory.md), with 24 proposed preservation,
or change dispositions and reasons. HTML output is selected; executed
feature parity and independent acceptance have not yet been established. Any
change to the current offline or data-access contract needs explicit review.

## Rules for a maintainable repository

- Give every contract and shared type one source owner. Generate language
  bindings or enforce explicit drift checks; do not maintain competing copies
  by hand.
- Document the allowed dependency direction and enforce it in repository
  checks. Preserve the pure evaluator's lack of effects and the host's
  authority over admission, lifecycle, persistence and outcomes.
- Create a crate when it establishes a useful dependency boundary, isolates
  substantial dependencies, or supports independent testing or delivery.
  Smaller responsibilities may remain internal modules. A directory does not
  imply a process, separately installed component or independent release.
- Define provider workspaces and toolchain requirements explicitly so unrelated
  provider dependencies do not become mandatory CLI build dependencies.
  Independent releases continue to use the common compatibility and packaging
  contracts; directory layout does not introduce lockstep versions.
- Keep unit tests near their implementation. Give shared fixtures,
  conformance checks, integration tests and qualification workloads explicit
  homes and owners. Reference fixtures do not become product qualification
  merely by being copied into a test directory.
- Maintain one current documentation reading path. Update the owning document
  as decisions evolve and use version control for its history. Keep retained
  audit/review evidence clearly identified and linked without duplicating the
  current design across successive status documents.
- Keep build outputs and temporary agent work out of the normal source tree.
  Generated bindings have the explicit locations below; the build plan proposes
  checking them in with byte-for-byte regeneration checks. Asset bundles remain
  build outputs. Generator/tool selection still requires review.
  Retain required review evidence deliberately with its own custody;
  existing frozen evidence is not deleted or reorganized by this decision.

## File inventory and naming conventions

The user requested an explicit directory/filename list with a description of
what belongs in each file, including consistent names for similar
implementations. The [machine-readable inventory](repository-file-inventory.v1.json)
is the source for the generated tables below. Edit its entries and regenerate
this section; do not maintain a second handwritten list. Proposed files become
real as their implementation is needed, with the inventory updated whenever a
reviewed split, merge or rename changes their responsibilities.

These are initial structural proposals. A listed filename does not establish
that its API, algorithm, dependency selection or product qualification is done.
This inventory deliberately leaves tool-specific build configuration and the
full schema migration map open until their owning decisions are made. Shared
platform behavior remains host-owned even when its code is in a support crate.

### Naming rules

| Category | Rust | TypeScript | Meaning |
|---|---|---|---|
| Ordinary source module | `snake_case.rs` | `kebab-case.ts` | Name the concrete responsibility; exported Rust types and TypeScript classes/types may use `PascalCase` |
| Factory | `<subject>_factory.rs` | `<subject>-factory.ts` | Select and construct an implementation from explicit inputs; do not hide workflow execution, discovery or permission grants in construction |
| Incremental builder | `<subject>_builder.rs` when a dedicated builder implementation exists | `<subject>-builder.ts` on the same rule | Incrementally construct a value; a function that constructs a descriptor can remain in its domain module |
| Named boundary adapter | `<boundary>_adapter.rs` | `<boundary>-adapter.ts` | Translate one named external boundary into owned structures; concrete platform mechanisms may retain names such as `filesystem.rs` |
| Renderer | `<format>_renderer.rs` | `<format>-renderer.ts` if one is needed | Produce a presentation of admitted data, without acquiring semantic authority |
| Persistent store implementation | `<subject>_store.rs` | `<subject>-store.ts` if one is needed | Own persistence mechanics; do not call browser view state a store of authoritative evidence |
| Generated bindings | `src/generated/<domain>.rs` | `src/generated/<domain>.ts` | Generated from the selected schema owner; never edited by hand |
| Separate behavioral test file | `<subject>_tests.rs` | `<subject>.test.ts` | Name the behavior or module under test; small Rust unit tests may remain inline |

Standard ecosystem entrypoints keep their standard spelling: `Cargo.toml`,
`Cargo.lock`, `lib.rs`, `main.rs`, `mod.rs`, `package.json`, `tsconfig.json` and
`index.ts`. New JSON data filenames use kebab-case; schema documents use the
selected owner's schema/version spelling. Existing frozen artifacts are not
renamed to fit these implementation conventions. Folder names use kebab-case;
Rust source-module filenames use Rust's underscore convention.

The three currently proposed factories are
`crates/components/src/session_factory.rs`,
`crates/reporting/src/renderer_factory.rs` and
`providers/typescript/src/program-factory.ts`. Their descriptions below state
which construction each owns. This convention does not require converting
ordinary constructors into factory abstractions.

Use concrete domain names in preference to catch-all files such as `utils`,
`helpers`, `misc` or `manager`. If one of those names seems necessary, first
identify the actual responsibility and its owning package. Put browser-only
state in `view-state.ts`; transport types come from generated contracts rather
than a second handwritten `types.ts` containing unrelated records.

### Ownership and dependency constraints

Within the pure layers, `contracts` has no internal dependencies, `identity`
may depend on `contracts`, and `evaluator` may depend on `identity` and
`contracts`. Reversing those edges is forbidden even if the graph is acyclic.
These crates may also use explicitly reviewed pure external libraries.
They have no OS, provider, store or report UI dependency. Platform code supplies
mechanisms; security, lifecycle and host code decide whether an operation is
lawful. Host finalization coordinates the authoritative application boundary.
The [commit API proposal](implementation-boundaries-and-build-plan.md#admission-and-authoritative-commit)
requires storage's facade to consume opaque evaluator `ReplayedRun` and security
`CommitSession` prerequisites bound to the exact target; raw ledger mutation and
receipt constructors stay private to storage. Storage therefore gains direct
evaluator and security dependencies. An ordinary DTO or success flag cannot
substitute for those prerequisites. The exact carrier/recovery join is proposed
there for Claude review; no implemented type-level or durability guarantee is
claimed by this inventory.

Components owns framing, negotiated protocol shape and session supervision.
Host fact admission owns the returned evidence's joins to the selected source,
context and Plan. Replay independently checks the semantic obligations over
explicitly supplied data. This keeps lifecycle's use of component management
from assigning it responsibility for analysis admission.

The Rust provider is a separately pinned workspace. Its shared contract/identity
source dependencies must be resolved reproducibly without pulling its compiler
integration into the host workspace. The TypeScript provider and report are
separate packages. Both consume their selected generated bindings; neither
imports the other's runtime code. Report assets are supplied by build/release
assembly to host reporting, not by a runtime dependency on a web server.

The source dependency graph alone does not describe these integration edges:

| Relationship | Required boundary |
|---|---|
| Schemas → Rust contracts, TS provider and report bindings | Registry records exact source IDs/digests, profiles, generator version/options, generated targets and semantic validator owners; generated types alone do not perform runtime admission |
| Host components ↔ separately released providers | Negotiated process protocols and authenticated release closures; no source imports of compiler implementations into the host |
| Rust provider → shared Rust contract/identity libraries | Reproducible pinned dependency resolution within its separate workspace, explicit compatible toolchains and selected wire surfaces; a path dependency must not inherit incompatible root workspace settings |
| Report build → host reporting → CLI release | Versioned asset bundle matches the embedded projection and is included in the signed offline release closure; provider-only builds need no report toolchain |
| Shared fixtures → package tests and executable integration harnesses | Each scenario has an executable owner and an independent expected result; qualification evidence retains its separate standing |

Root TypeScript scripts coordinate packages without making a combined frontend
build a prerequisite for provider development. A provider-side SDK is not yet
selected: compare shared transport obligations before adding a package. Common
host supervision, authorization and outcome behavior remains host-owned either
way. CLI bootstrap initializes only the services required by the admitted command;
static linkage does not justify opening stores or providers for help/version.

Derived indexes belong to storage mechanics and have a lifecycle separate from
retained evidence. Host query owns exact Run/view selection, bounded traversal
and truthful completeness. Loss or interruption of an index leads to rebuilding,
a supported retained-evidence fallback or an explicit unavailable result under
the selected contract, never an invented empty answer. No graph engine is chosen.

Current product semantics remain in the five product contracts. This inventory
maps those responsibilities onto prospective code; it does not change their
wire majors, typed outcomes or authority boundaries. In particular, the new
`schemas/` home needs an exact source/ID/generation mapping before migration;
this document does not silently replace the existing pinned schema files.

The [inventory checker](../../operations/check_repository_file_inventory.py)
validates unique canonical paths, ownership, Rust/TypeScript naming, factory, store and
renderer suffixes, test names, generated-file locations, the pure-crate
dependency direction and an acyclic declared package graph. It also checks that this chapter matches the inventory. It does
not inspect an implemented dependency graph or prove semantic correctness.
Actual source/dependency enforcement belongs to the implementation's repository
checks once those files exist.

```sh
python3 -I -B docs/operations/check_repository_file_inventory.py --write
python3 -I -B docs/operations/check_repository_file_inventory.py --check
```

<!-- BEGIN GENERATED FILE INVENTORY -->

### Proposed package boundaries

Package names and dependency edges below are proposals except for the agreed
`opensip-cli` name. Non-Rust group IDs are inventory labels, not selected npm
package names. Dependencies list proposed direct Rust source edges;
generated-schema inputs, process protocols and asset delivery are separate
build/runtime relationships. This table grants no component authority.

| Package/group | Directory | Responsibility | Proposed direct dependencies |
|---|---|---|---|
| `repository` | `./` | Workspace, contributor guidance and shared checks. | None declared |
| `opensip-cli` | `apps/cli/` | CLI parsing and application assembly. | `opensip-contracts`, `opensip-host` |
| `opensip-contracts` | `crates/contracts/` | Shared inert contract types and protocol declarations. | None declared |
| `opensip-identity` | `crates/identity/` | Pure canonical admission and content identity. | `opensip-contracts` |
| `opensip-evaluator` | `crates/evaluator/` | Pure policy evaluation and complete semantic reconstruction. | `opensip-contracts`, `opensip-identity` |
| `opensip-syntax` | `crates/syntax/` | Pure compiler-free parsing and normalized clone candidates over admitted source and grammar bytes. | `opensip-contracts`, `opensip-identity` |
| `opensip-platform` | `crates/platform/` | OS mechanisms behind explicit interfaces, without policy authority. | `opensip-contracts` |
| `opensip-security` | `crates/security/` | Host trust, custody and authorization decisions. | `opensip-contracts`, `opensip-evaluator`, `opensip-identity`, `opensip-platform` |
| `opensip-storage` | `crates/storage/` | Host-internal retained evidence mechanics. | `opensip-contracts`, `opensip-identity`, `opensip-evaluator`, `opensip-platform`, `opensip-security` |
| `opensip-components` | `crates/components/` | Common component negotiation and supervision. | `opensip-contracts`, `opensip-identity`, `opensip-platform` |
| `opensip-lifecycle` | `crates/lifecycle/` | Host installation and component generation lifecycle. | `opensip-contracts`, `opensip-identity`, `opensip-platform`, `opensip-security`, `opensip-components`, `opensip-storage` |
| `opensip-reporting` | `crates/reporting/` | Host-owned projections and output assembly. | `opensip-contracts`, `opensip-identity` |
| `opensip-host` | `crates/host/` | Application authority and complete workflow orchestration. | `opensip-contracts`, `opensip-identity`, `opensip-evaluator`, `opensip-platform`, `opensip-security`, `opensip-storage`, `opensip-components`, `opensip-lifecycle`, `opensip-reporting`, `opensip-syntax` |
| `typescript-provider` | `providers/typescript/` | Sealed-input TypeScript/JavaScript analysis; no host policy, storage or presentation authority. | None declared |
| `opensip-rust-provider` | `providers/rust/` | Independently pinned Rust compiler/provider integration. | `opensip-contracts`, `opensip-identity` |
| `report` | `apps/report/` | Build offline browser report assets; no provider or host runtime import. | None declared |
| `shared-assets` | `schemas/` | Own implementation schema sources and binding generation mapping. | None declared |
| `verification` | `tests/` | Cross-package conformance, workflow integration and implementation measurements. | None declared |
| `tooling` | `tools/` | Repository validation and build/release adapter tooling. | None declared |
| `product-docs` | `docs/` | One current implementation reading path with linked historical evidence. | None declared |

### Proposed filenames and responsibilities

The inventory currently contains **198 proposed files**. Each
row names one target file. Generated rows are owned outputs of schema
generation; their schemas and semantic validators remain distinct owners.
This is a planning inventory, not an instruction to create empty files.

#### repository

| Target path | Role | Contents/responsibility |
|---|---|---|
| `.gitignore` | configuration | Exclude build outputs, local state and scratch work while retaining intentional evidence. |
| `AGENTS.md` | documentation | State repository ownership, dependency, generated-file and verification rules for coding agents. |
| `Cargo.lock` | lockfile | Pin the host workspace dependency resolution for reproducible executable builds. |
| `Cargo.toml` | manifest | Declare the host workspace and shared build policy; exclude the independently pinned Rust provider workspace. |
| `README.md` | documentation | Give the shortest path to understanding, building and using the product. |
| `package.json` | manifest | Declare TypeScript workspace membership and common script names; package manager and its lockfile remain to be selected. |
| `rust-toolchain.toml` | configuration | Pin the host development toolchain; exact version remains to be selected. |

#### opensip-cli

| Target path | Role | Contents/responsibility |
|---|---|---|
| `apps/cli/Cargo.toml` | manifest | Declare Cargo package opensip-cli with explicit [[bin]] name = "opensip", dependency edges and build targets. |
| `apps/cli/src/arguments.rs` | parser | Parse the selected command inventory and flags into typed host requests; do not discover projects or execute providers. |
| `apps/cli/src/bootstrap.rs` | composition | Assemble command-scoped host services lazily; help/version must not open a project, store or component session or access the network. For version metadata, read the build-embedded signed release descriptor and its exact declared closure IDs without opening a component/project/store session; do not claim these are currently loaded closures. |
| `apps/cli/src/main.rs` | entrypoint | Assemble the executable and delegate to its application boundary. |
| `apps/cli/src/terminal.rs` | adapter | Adapt terminal capabilities and presentation preferences; do not derive verdicts or exit-code policy. |
| `apps/cli/tests/startup_tests.rs` | test | Exercise help/version with unavailable project/store/provider resources and verify no resource initialization or network effects. |

#### opensip-contracts

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/contracts/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/contracts/src/generated/evidence.rs` | model; generated | Generated facts, Coverage, proofs and retained evidence carriers. |
| `crates/contracts/src/generated/identity.rs` | model; generated | Generated identity and typed descriptor carriers; no hashing or custody authority. |
| `crates/contracts/src/generated/invocation.rs` | model; generated | Generated request, step, attempt and outcome carriers. |
| `crates/contracts/src/generated/mod.rs` | public-api; generated | Expose generated modules from the selected schema registry. |
| `crates/contracts/src/generated/output.rs` | model; generated | Generated command envelope and report projection carriers. |
| `crates/contracts/src/generated/protocol.rs` | model; generated | Generated negotiated control/provider frame carriers; preserve each protocol owner. |
| `crates/contracts/src/lib.rs` | public-api | Expose inert versioned contract modules; provider consumers select only their required wire/identity surface, without host effects or lockstep protocol upgrades. |

#### opensip-identity

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/identity/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/identity/src/canonical.rs` | codec | Implement exact lexical admission and canonical encoding; preserve profile and integer distinctions. |
| `crates/identity/src/closure.rs` | validator | Check object/blob identity and ownership joins over explicitly supplied bytes; this is not complete evaluator replay. |
| `crates/identity/src/descriptors.rs` | validator | Validate identity descriptors and declared collection ordering. |
| `crates/identity/src/digests.rs` | algorithm | Implement registered digest framing and domain dispatch without a second serializer. |
| `crates/identity/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |

#### opensip-evaluator

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/evaluator/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/evaluator/src/atoms.rs` | algorithm | Evaluate atomic predicates with native/import evidence and explicit uncertainty. |
| `crates/evaluator/src/budgets.rs` | algorithm | Account for deterministic analysis work and output bounds; never truncate into a substitute successful Run. |
| `crates/evaluator/src/composition.rs` | algorithm | Compose predicate truth, findings, waivers and required execution deficiencies. |
| `crates/evaluator/src/enumeration.rs` | algorithm | Derive selected subject populations from admitted Plan inputs and retained inventories. |
| `crates/evaluator/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/evaluator/src/policy.rs` | compiler | Admit and compile the closed declarative policy language; own the pure portable glob predicate used by evaluator filters and host policy/repair scope checks, following glob-pattern-contract.v1.md. |
| `crates/evaluator/src/proofs.rs` | builder | Construct complete proof outputs and their references from evaluation results. |
| `crates/evaluator/src/replay.rs` | validator | Independently reconstruct complete semantic outputs and mint opaque ReplayedRun only after full replay/closure checks over immutable supplied inputs; no I/O or callbacks. |

#### opensip-syntax

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/syntax/Cargo.toml` | manifest | Declare the pure syntax crate and explicit dependencies; no filesystem, process or compiler discovery. |
| `crates/syntax/src/lib.rs` | public-api | Expose pure parsing/normalization over immutable admitted inputs; no unchecked Coverage or authoritative finding constructors. |
| `crates/syntax/src/grammar.rs` | validator | Validate the retained SyntaxGrammarBundle, signed grammar closure identity/version, closed language/suffix registry and selected grammar-set joins. |
| `crates/syntax/src/parser.rs` | parser | Parse supplied code/data bytes with the selected retained grammar; preserve exact anchors and code/data distinctions without resolving imports. |
| `crates/syntax/src/normalization.rs` | algorithm | Apply the selected grammar normalizers to code bodies; preserve dialect/variant identity and closed relation-at-rung eligibility. |
| `crates/syntax/src/candidates.rs` | builder | Produce inert syntax and normalized-clone candidates with source ranges and explicit limitations; host admits facts, Coverage and occupancy. |
| `crates/syntax/tests/grammar_tests.rs` | test | Check exact closure/version/suffix joins, unbundled grammar refusal and all seven selected language families/fourteen suffixes. |
| `crates/syntax/tests/normalization_tests.rs` | test | Check code/data separation, body grammar identity, deterministic normalization and unsupported semantic relation refusal. |

#### opensip-platform

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/platform/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/platform/src/clock.rs` | adapter | Expose wall and sleep-inclusive monotonic observations; do not decide trust time. |
| `crates/platform/src/filesystem.rs` | adapter | Provide safe-handle reads, atomic publication and durability primitives; callers decide admission. |
| `crates/platform/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/platform/src/linux.rs` | adapter | Implement selected Linux-specific mechanism bindings. |
| `crates/platform/src/locks.rs` | adapter | Provide filesystem lease/fence mechanisms with explicit nonblocking or bounded behavior. |
| `crates/platform/src/macos.rs` | adapter | Implement selected macOS-specific mechanism bindings. |
| `crates/platform/src/process.rs` | adapter | Provide process launch, cancellation and reap mechanisms for already authorized operations. |

#### opensip-security

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/security/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/security/src/commit_authority.rs` | service | Mint opaque live CommitSession from actual project/store custody, operational grants and writer guard; bind exact operation/generation and perform final S6 checkpoint under the journal lock. Own the session-consuming JournalWriteTxn, opaque JournalSealBinding and atomic final commit-admission gate; accept only evaluator-minted ReplayedRun for SEAL targets. |
| `crates/security/src/custody.rs` | validator | Decide path/owner/ACL and source/storage custody from explicit platform observations. |
| `crates/security/src/grants.rs` | validator | Bind and verify exact execution, mutation and recovery permissions. |
| `crates/security/src/journal_store.rs` | store | Own grant journal append/witness/high-water admission and versioned SEAL carrier mapping; preserve append-only sequence/cap/restore rules and keep this carrier distinct from lifecycle transition journals. |
| `crates/security/src/lib.rs` | public-api | Expose admitted security services and opaque authority-session types with private constructors; never expose an unchecked operational grant or journal checkpoint. |
| `crates/security/src/revocation.rs` | service | Observe trust epochs and enforce effect/SEAL checkpoints under the required journal ordering. |
| `crates/security/src/trust.rs` | validator | Admit signed trust metadata, root chains and closure associations. |
| `crates/security/src/trust_time.rs` | algorithm | Apply clock plausibility, monotonic floors and authorized floor recovery. |

#### opensip-storage

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/storage/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/storage/src/availability.rs` | model | Manage versioned evidence availability independently of immutable sealed assurance and disposable index readiness; index loss must not mark retained evidence purged. |
| `crates/storage/src/backup.rs` | service | Export and restore bounded evidence bundles without restoring trust floors or granting local authority. |
| `crates/storage/src/blob_store.rs` | store | Publish and read immutable digest-bound objects with verified length and bytes. |
| `crates/storage/src/commit.rs` | service | Require evaluator ReplayedRun and security CommitSession; bind immutable target/inventory, publish verified objects, then coordinate SEAL/ledger barriers and private recovery association before producing PublishedCommit. Privately stage the exact receipt/association, supply the single-use ledger commit adapter, and mint PublishedCommit only from its own confirmed barrier result. |
| `crates/storage/src/gc.rs` | service | Perform host-authorized reachability cleanup under the exclusive lease and reader census. |
| `crates/storage/src/index_store.rs` | store | Own disposable derived-index publication, generation binding, interruption cleanup and rebuild state; bind entries to exact retained Run/fact views and keep backend row IDs private. |
| `crates/storage/src/ledger_store.rs` | store | Implement private ledger transactions, exact receipts and recovery associations used only by the guarded commit/authorized maintenance paths; expose no raw writable connection. |
| `crates/storage/src/lib.rs` | public-api | Expose read/maintenance APIs and the guarded commit facade; keep SQL handles, raw ledger mutation and receipt constructors private. |
| `crates/storage/src/pins.rs` | service | Maintain explicit retention roots and enumerate affected pins for host-authorized operations. |
| `crates/storage/src/recovery.rs` | service | Reconcile ledger receipts, private journal associations and exact objects in a fresh read-only recovery path; uncertain reads never establish absence, and recovery never repeats repository mutations. |
| `crates/storage/src/retention.rs` | algorithm | Calculate expiry and retention decisions from admitted policy and pins. |
| `crates/storage/tests/commit_tests.rs` | test | Exercise the actual carrier at each object/journal/ledger/acknowledgement fault point, lock order, revoked sessions and fresh-process recovery; API compile-fail fixtures require the selected harness. |

#### opensip-components

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/components/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/components/src/control_protocol.rs` | codec | Encode and validate common control frames without translating provider semantics. |
| `crates/components/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/components/src/manifest.rs` | validator | Admit selected component capabilities and manifest shape after authenticated closure association. |
| `crates/components/src/provider_protocol.rs` | codec | Dispatch the selected provider wire protocol and validate its transaction boundaries. |
| `crates/components/src/session_factory.rs` | factory | Construct a role-specific session from an already admitted selection; leave spawning and effects to supervision. |
| `crates/components/src/supervisor.rs` | service | Supervise component lifetime, EOF/exit, cancellation and resource failures. |

#### opensip-lifecycle

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/lifecycle/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/lifecycle/src/catalog.rs` | validator | Resolve authenticated component releases and compatibility declarations. |
| `crates/lifecycle/src/doctor.rs` | service | Inspect lifecycle/trust/store state and return typed diagnostics; read-only inspection performs no repairs. |
| `crates/lifecycle/src/installation.rs` | service | Stage and publish authorized immutable component generations. |
| `crates/lifecycle/src/journal_store.rs` | store | Retain lifecycle intent and transition records using the required ordering and durability barriers. |
| `crates/lifecycle/src/leases.rs` | service | Compose install fences and project lease modes in the specified lock order. |
| `crates/lifecycle/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/lifecycle/src/transitions.rs` | service | Apply authorized update, rollback and migration state machines. |

#### opensip-reporting

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/reporting/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/reporting/src/agent_renderer.rs` | renderer | Project the common envelope with advisory agent hints that cannot alter parity fields. |
| `crates/reporting/src/assets.rs` | model | Validate exact report asset manifest, compatibility and bytes verified against the exact asset-manifest digest and length embedded in the trusted host binary; report assets are not a new closure2 producer kind. |
| `crates/reporting/src/html_embedding.rs` | codec | Embed data and assets safely, preserving untrusted repository text as data rather than executable markup. |
| `crates/reporting/src/html_renderer.rs` | renderer | Assemble the self-contained HTML report from the selected projection and supplied built assets. |
| `crates/reporting/src/human_renderer.rs` | renderer | Render the human-readable projection with required parity fields. |
| `crates/reporting/src/json_renderer.rs` | renderer | Serialize the selected typed command envelope without changing semantic values. |
| `crates/reporting/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/reporting/src/projection.rs` | adapter | Construct total command-specific presentation data and bounded optional exploration data from host-approved results; preserve required parity fields and route missing required data to host delivery failure. |
| `crates/reporting/src/renderer_factory.rs` | factory | Select a registered renderer for an already admitted format and command; never choose policy or public termination. |
| `crates/reporting/src/sarif_renderer.rs` | renderer | Render applicable analysis results through the declared SARIF projection. |
| `crates/reporting/tests/html_renderer_tests.rs` | test | Check single-file offline assembly, hostile repository text escaping and embedded-payload preservation; browser execution belongs to the report integration lane. |
| `crates/reporting/tests/projection_tests.rs` | test | Check applicable renderer parity and required-field failures against shared output cases, including advisory and ephemeral results. |

#### opensip-host

| Target path | Role | Contents/responsibility |
|---|---|---|
| `crates/host/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `crates/host/src/agent_server.rs` | service | Adapt agent serve requests to the same admitted host operations, cancellation and typed outcomes; expose no alternate admission or mutation authority. |
| `crates/host/src/analysis.rs` | service | Compose provider work, admission, evaluation and complete replay into an analysis attempt. |
| `crates/host/src/baselines.rs` | service | Adopt, export and upgrade portable baselines and their retained executable closure pins. |
| `crates/host/src/comparison.rs` | service | Compose the required counterfactual Runs and attribution/gating rules for delta assessment. |
| `crates/host/src/configuration.rs` | service | Resolve admitted configuration layers, registry selections and provenance. |
| `crates/host/src/delivery.rs` | service | Publish selected rendered artifacts atomically, bind them to the exact projection/Run and handle optional browser launch; account for post-commit failures without changing the Run. |
| `crates/host/src/discovery.rs` | service | Compose safe project discovery, technical recognition and explicit workspace selection. |
| `crates/host/src/execution.rs` | service | Coordinate explicitly authorized tests/native preparation and their evidence-import handoff. |
| `crates/host/src/fact_admission.rs` | validator | Own host admission of provider candidates, Coverage and occupancy joins against the selected source/context before evaluation; protocol framing alone grants no fact authority. |
| `crates/host/src/finalization.rs` | service | Coordinate full evaluator replay and live security admission, then pass opaque ReplayedRun and CommitSession to guarded storage publication; project success only after PublishedCommit. Route typed CarrierCapacityExhausted through cleanup and operation-lease release to lifecycle rollover under its fence; storage never calls lifecycle. After publication, use outcomes.rs for the retained analysis projection and separately validate delegated attempt attribution, detail and authority under their owners. |
| `crates/host/src/imports.rs` | service | Admit and retain typed imported evidence with correspondence and explicit mutation receipts. |
| `crates/host/src/invocation.rs` | service | Execute the bounded step/attempt DAG and apply dependency, retry and cancellation rules. |
| `crates/host/src/lib.rs` | public-api | Expose the intentionally public API; keep internal modules private. |
| `crates/host/src/maintenance.rs` | service | Coordinate store status, authorized purge/backup/recovery and pin-impact decisions through lifecycle/security/storage owners; never use cache deletion as evidence deletion. |
| `crates/host/src/outcomes.rs` | adapter | Derive the admitted Run analysis projection, including ordered D9 reasons and deterministic coverage attribution, under run-termination-contract.v1; map typed host boundary observations and aggregate step outcomes under their existing owners. Shape-valid attempt attribution and explanatory details still require host validation. |
| `crates/host/src/plan.rs` | builder | Construct Plan inputs and the derivation DAG with all semantic dependencies bound. |
| `crates/host/src/policy.rs` | service | Coordinate policy show/test/init and waiver commands, using the pure compiler/evaluator and explicit authorization for tracked-intent changes. |
| `crates/host/src/query.rs` | service | Admit retained selections and perform deterministic graph/artifact queries with bounded completeness disclosures. |
| `crates/host/src/repair.rs` | service | Coordinate separately authorized repair preview/apply/recovery and fresh verification; derive relevant program ownership and native closed-world eligibility from retained admitted evidence, keeping the descriptor summary distinct from authorization. |
| `crates/host/src/request.rs` | service | Reserve RequestId and orchestrate typed request admission before effects. |
| `crates/host/src/review.rs` | service | Handle candidate inspection, bounded review briefs and content-bound advisory dispositions. |
| `crates/host/src/snapshot.rs` | service | Capture exact admitted source/read-set bytes through the selected custody boundary. |
| `crates/host/src/syntax.rs` | service | Dispatch pure opensip-syntax over exact admitted source/grammar closure, including no-compiler-unit repositories; retain grammar inputs and route candidates through ordinary host fact/Coverage admission. |
| `crates/host/tests/admission_tests.rs` | test | Verify malformed provider joins, identity-valid but replay-invalid Runs, revoked authority and stale fences cannot produce acknowledged authoritative commits. |
| `crates/host/tests/discovery_tests.rs` | test | Execute explicit/default workspace and custody-boundary behavior, including the current audit counterexamples. |
| `crates/host/tests/retention_tests.rs` | test | Exercise commit/recovery, pin-aware purge, missing evidence and historical selection. |
| `crates/host/tests/workflow_tests.rs` | test | Execute complete analysis, baseline, import, repair and cancellation flows through the public host boundary. |

#### typescript-provider

| Target path | Role | Contents/responsibility |
|---|---|---|
| `providers/typescript/package.json` | manifest | Declare the provider package and pinned runtime/compiler/build requirements. |
| `providers/typescript/src/analysis/calls.ts` | algorithm | Produce call candidates and unresolved-target observations. |
| `providers/typescript/src/analysis/clones.ts` | algorithm | Produce native clone facts and separately identified near/cross-language candidates. |
| `providers/typescript/src/analysis/coverage.ts` | builder | Produce examined partitions and resolution-completeness observations without deciding host sufficiency. |
| `providers/typescript/src/analysis/imports.ts` | algorithm | Produce import candidates and exact occupancy observations. |
| `providers/typescript/src/analysis/reachability.ts` | algorithm | Produce bounded reachability from resolved calls and admitted origins with explicit unresolved/entry-point limitations; never infer universal absence from incomplete discovery. |
| `providers/typescript/src/analysis/references.ts` | algorithm | Produce symbol reference candidates and relevant search observations. |
| `providers/typescript/src/analysis/symbols.ts` | algorithm | Produce the required symbol census including symbols with no emitted relation facts. |
| `providers/typescript/src/analysis/syntax.ts` | algorithm | Produce selected declares/literal/control-flow syntax facts from sealed compiler inputs; exclude data-document code constructs and preserve provenance. |
| `providers/typescript/src/analysis/types.ts` | algorithm | Produce declared/inferred type evidence with derivation provenance. |
| `providers/typescript/src/compiler-adapter.ts` | adapter | Isolate the selected TypeScript compiler API and translate compiler observations into provider-owned structures. |
| `providers/typescript/src/framework-recognition.ts` | algorithm | Produce technical recognizer evidence and unresolved choices; host configuration and permission authority remain separate. |
| `providers/typescript/src/generated/protocol.ts` | model; generated | Generate selected wire carriers from the owned schema registry; transport encoders remain explicit implementations. |
| `providers/typescript/src/index.ts` | entrypoint | Start the provider protocol session using the host-supplied closure and input channels. |
| `providers/typescript/src/program-factory.test.ts` | test | Check sealed-input/context construction and refusal of ambient or mismatched compiler inputs. |
| `providers/typescript/src/program-factory.ts` | factory | Construct the selected compiler program from the admitted native context and sealed VFS; no ambient compiler discovery. |
| `providers/typescript/src/protocol.ts` | codec | Encode/decode the selected provider/control channels without owning public outcomes. |
| `providers/typescript/src/sealed-vfs.ts` | adapter | Expose only the source and dependency bytes admitted into the provider read set. |
| `providers/typescript/src/session.ts` | service | Own one negotiated provider transaction and discard incomplete output. |
| `providers/typescript/tsconfig.json` | configuration | Define the provider compilation boundary and explicit generated binding inputs. |

#### opensip-rust-provider

| Target path | Role | Contents/responsibility |
|---|---|---|
| `providers/rust/Cargo.lock` | lockfile | Pin the separate provider workspace dependency resolution. |
| `providers/rust/Cargo.toml` | manifest | Declare this package, explicit dependencies and build targets. |
| `providers/rust/rust-toolchain.toml` | configuration | Pin the provider compiler toolchain independently of the host toolchain. |
| `providers/rust/src/clones.rs` | algorithm | Produce selected Rust clone evidence while preserving dialect and normalization identity. |
| `providers/rust/src/compiler_adapter.rs` | adapter | Isolate the pinned Rust compiler integration and its observation boundary. |
| `providers/rust/src/context.rs` | validator | Bind target, edition, features, toolchain and prepared-input context before extraction. |
| `providers/rust/src/coverage.rs` | builder | Produce examined partitions and resolution-completeness observations. |
| `providers/rust/src/facts.rs` | builder | Produce native relation candidates and explicit unknown edges. |
| `providers/rust/src/inventory.rs` | builder | Produce the complete required subject census and selected program observations. |
| `providers/rust/src/main.rs` | entrypoint | Assemble the executable and delegate to its application boundary. |
| `providers/rust/src/protocol.rs` | codec | Implement the selected Rust provider wire transaction without host outcome authority. |
| `providers/rust/src/sealed_vfs.rs` | adapter | Expose only admitted Rust source, dependency and prepared-input bytes. |
| `providers/rust/src/session.rs` | service | Run one negotiated provider transaction over explicit host inputs. |

#### report

| Target path | Role | Contents/responsibility |
|---|---|---|
| `apps/report/index.html` | template | Provide the self-contained report shell and defined embedded-data location; no remote asset requirement. |
| `apps/report/package.json` | manifest | Declare report build dependencies and scripts; frontend framework and bundler remain undecided. |
| `apps/report/src/catalog-view.ts` | view | Display searchable admitted rule/capability/recipe catalogs and provenance with explicit availability; descriptors grant no execution permission. |
| `apps/report/src/comparison-view.ts` | view | Display baseline/delta classifications and gate attribution when present. |
| `apps/report/src/evidence-view.ts` | view | Display coverage, provenance, limitations and retained availability. |
| `apps/report/src/exports.ts` | service | Produce optional local exports of displayed admitted data with Run/view/completeness context and safe CSV text; never mint an authoritative evidence bundle. |
| `apps/report/src/findings-view.ts` | view | Display findings, locations and retained evidence citations. |
| `apps/report/src/generated/report.ts` | model; generated | Generate projection carriers and runtime shape-validation support from the same selected output schema as Rust; exact generator remains pending, and shape validity grants no semantic authority. |
| `apps/report/src/graph-view.ts` | view | Display bounded host graph/path/coupling projections with exact universe/symbol identities, presentation controls and completeness disclosures; local layout/filtering cannot create semantic authority. |
| `apps/report/src/help-view.ts` | view | Present view-specific explanations of controls, evidence scope and unknown states with accessible opening/closing behavior. |
| `apps/report/src/history-view.ts` | view | Select among exactly embedded Run projections and disclose history limits and observation age; never substitute latest for a missing explicit Run or fetch live evidence. |
| `apps/report/src/index.ts` | entrypoint | Initialize presentation using the embedded, versioned report payload. |
| `apps/report/src/navigation.ts` | service | Own safe embedded-view routes, keyboard navigation and focus transitions; validate local editor-link schemes and provide relative-path fallback without ambient source access. |
| `apps/report/src/overview-view.ts` | view | Display admitted invocation/step/attempt summaries and outcomes without deriving verdicts or concealing missing child evidence. |
| `apps/report/src/report-data.test.ts` | test | Check payload compatibility and explicit failure display. |
| `apps/report/src/report-data.ts` | validator | Use generated runtime validation for the embedded projection and explicit version/profile compatibility checks; incompatible data produces a display error, with no hand-maintained duplicate schema or recomputed verdict. |
| `apps/report/src/report-view.test.ts` | test | Check required disclosures, safe repository-text rendering and presentation-only interactions. |
| `apps/report/src/report-view.ts` | view | Compose overview, historical selection, findings, evidence, comparison, catalog and graph presentation with required disclosures and independent optional-panel failures. |
| `apps/report/src/report.css` | style | Define report-specific styling and accessible presentation states. |
| `apps/report/src/symbol-detail-view.ts` | view | Present an exact occurrence, source locations, callers/callees and evidence links across report views; never identify distinct symbols solely by body hash. |
| `apps/report/src/view-state.ts` | model | Hold presentation-only selection and filtering state without altering the embedded assessment. |
| `apps/report/tsconfig.json` | configuration | Define browser compilation and generated projection binding inputs. |

#### shared-assets

| Target path | Role | Contents/responsibility |
|---|---|---|
| `schemas/README.md` | documentation | Map each selected immutable contract to its implementation source owner; exact schema-file migration remains pending. |
| `schemas/registry.json` | registry | Declare exact complete schema sources, multi-source hermetic generation recipes and globally unique generated outputs with role sets; include generated module indexes and distinguish handwritten semantic admission owners. |

#### verification

| Target path | Role | Contents/responsibility |
|---|---|---|
| `tests/conformance/README.md` | documentation | Describe shared contract fixtures, independent oracles and their product/reference standing. |
| `tests/conformance/identity-cases.json` | fixture | Carry canonical admission, digest-domain and complete closure positive/negative vectors. |
| `tests/conformance/output-cases.json` | fixture | Carry cross-renderer parity and unavailable/partial/failure expectations. |
| `tests/conformance/protocol-cases.json` | fixture | Carry negotiation, framing, ordering, omission and process-completion cases. |
| `tests/integration/README.md` | documentation | Own cross-process/offline/end-to-end scenario definitions and link their executable package targets. |
| `tests/qualification/README.md` | documentation | Map required platform, performance, security and native measurement lanes to retained implementation evidence. |

#### tooling

| Target path | Role | Contents/responsibility |
|---|---|---|
| `tools/README.md` | documentation | Publish supported maintenance/build commands, their inputs, outputs and ownership; select concrete adapter/tool filenames after choosing the tooling. |

#### product-docs

| Target path | Role | Contents/responsibility |
|---|---|---|
| `docs/README.md` | documentation | Link current product/developer guidance and keep review history out of the first-reading path. |
| `docs/architecture.md` | documentation | Summarize the accepted component/dependency model with links to exact owned contracts. |
| `docs/development.md` | documentation | Describe workspaces, toolchains, build/test commands and contribution workflow. |
| `docs/report.md` | documentation | Describe report generation, offline behavior and the explicit prototype-feature dispositions. |

### Explicit gaps in this first inventory

- Obtain actual Claude review of the corrected topology and implementation-boundaries-and-build-plan.md, including storage dependencies and opaque replay/security prerequisites.
- Review the closed private recovery record, explicit operation/store-generation bindings, witness-aware two-transaction ordering and F00–F53 cases and the selected versioned physical carrier migration; obtain final independent design review and qualify the product migration before release.
- Bind exact schemas, profiles, pinned generator/runtime validator and checked-in generated targets to the accepted successor; preserve historical bytes and IDs and enforce byte-for-byte regeneration.
- Select supported toolchain versions, TS package manager/lock layout, frontend/bundler, dependency checker, release adapter and executable test harnesses before their implementation milestones.
- Review all R01-R24 prototype report dispositions, including the five explicit tab mappings and local editor path disclosure; source inspection does not establish executed feature parity.
- Use existing shared identity tokens/HelloV3 contracts and generated bindings; no extra shared provider SDK is selected for the distinct TS2/Rust3 protocols. Reconsider only with demonstrated reuse.
- Refine private helper signatures during implementation inside accepted public API/authority boundaries; expand milestones into all selected commands, capabilities and standing gates.
- Review the pure crates/syntax backend, retained signed grammar inventory and host dispatch/admission joins; this selects no new provider protocol.
- Resolve the four inherited run2 CLI examples and the SEAL/current-platform journal carrier migration in the successor review; preserve frozen source bytes.

<!-- END GENERATED FILE INVENTORY -->

## Complete this blueprint before implementation

This chapter owns layout; its implementation-plan and report-inventory companions
own the focused decisions linked above. Remaining review/tool choices are:

| Remaining decision | Required result |
|---|---|
| Rust crate inventory | Review the proposed package/file list and settle public API boundaries, dependencies and build outputs; assess which services should remain modules |
| Dependency graph | Review the declared edges above and define enforcement over actual source and external dependencies |
| TypeScript package/module layout | Review the proposed provider/report files and generated binding locations; settle tool-specific configuration and any justified sharing |
| Workspace and release boundaries | Review the concrete independent build lanes, checked-in binding policy and explicit report asset inputs in the implementation plan; select tool versions/adapters |
| Schema and fixture ownership | One owner per contract and fixture, generation/drift rules, and locations for produced artifacts |
| Report feature inventory | Review all R01–R24 source-based dispositions and establish executed parity during implementation |
| Documentation organization | A concise implementation reading path and explicit locations for current design, developer guidance and retained evidence |

## Author review and pending Claude review

Codex completed a focused author review on 2026-09-10 of this chapter, the file
inventory and its checker against the frozen candidate25 identity/evidence,
security/lifecycle and workflow contracts. This is a review of the proposed code
organization, not another complete architecture audit or independent acceptance.
That review expanded the initial 167-file proposal to 175 paths across 19 groups.
The 2026-09-11 implementation planning first expanded it to 186 paths;
the subsequent coverage pass brings the current inventory to 190.
No proposed product source files were created.

| Review finding | Correction or explicit disposition |
|---|---|
| Component protocol handling also owned evidence admission | Move fact admission into host; distinguish framing checks from source/context joins and independent semantic replay |
| A promise of verified storage inputs did not specify an enforceable handoff | Assign authoritative commit to private host finalization, clarify storage mechanics, and require API/constructor/visibility review before implementation; exact handoff remains open |
| Acyclic pure dependencies could still point in the wrong direction | Define and check contracts → no internal dependencies; identity → contracts; evaluator → identity/contracts |
| Source edges omitted generation, process and asset dependencies | Add the integration relationship table, independent build constraints and exact schema/generator mapping requirements |
| Runtime report validation and generated types were conflated | Require schema-derived runtime shape checks, explicit compatibility handling and separate semantic authority; preserve total projection and delivery-failure behavior |
| Policy commands, agent serving and store maintenance had no explicit host module | Add owning modules using the same host admission, authorization and outcomes |
| Derived indexes had no explicit storage owner | Add an index store separate from evidence availability; retain exact historical selection and honest failure/completeness behavior |
| Startup and critical boundary checks lacked concrete test locations | Add CLI startup, host admission and reporting parity/HTML test files; executable cross-process/browser/OS harness selection remains pending |
| Generated source locations conflicted with the generic output exclusion rule | Distinguish generated bindings from build artifacts; defer check-in/drift policy to generator selection |

The three factory names remain consistent. No extra factory abstraction or new
crate is justified by this review. The proposed crate count still needs assessment
against actual public interfaces, dependency weight and independent testing.
Prototype report parity and tool-specific build files remain explicit unfinished
work, not implied by the filename list. Checker results establish internal
inventory consistency only; proposed tests have not been implemented or run.

The 2026-09-10 author validation passed: all 175 inventory paths and generated tables, ten
negative checker controls (including reversed acyclic pure dependencies and
incorrect nested ownership), 43 local documentation links and whitespace checks.

### Additional author planning, 2026-09-11

The implementation plan now proposes an enforceable two-prerequisite commit API,
private recovery association, independent build lanes, checked-in generated
bindings with drift checks, and M0–M6 milestones. The source-based prototype
inventory records 24 feature dispositions. Eleven additional target modules/tests
bring the inventory to 186 paths; no additional crate or product source file was
created. The subsequent coverage pass adds four modules (compiler-free host
syntax, TS syntax/reachability and the security grant-journal owner), bringing
the current total to 190. Its 320 source-bound mappings and 36 planned recovery
cases are owned by the implementation plan and its machine-readable companions.
These decisions supersede the earlier open handoff/generated-output
choices in the dated author review above, while actual Claude acceptance, precise
carrier integration and tool selection remain pending.

### Claude task — repository structure and file responsibilities

**Status: first actual Claude reviews completed; corrections and changed-byte review pending.** The user
explicitly requested this additional review on 2026-09-10. Another model's review
cannot mark this Claude item complete. It adds to the existing design-correction
reviews, blind-consumer obligations and final application review.

Give Claude this chapter, its canonical JSON inventory, the checker, both
focused companions and planning-source manifest, plus the final successor
contracts/source map selected for review. Freeze or otherwise
record the exact input bytes/digests at dispatch; candidate25 acceptance does not
cover this later structural proposal. Ask Claude to:

1. Assess every proposed package's responsibility, public interface, permitted
   dependencies and build output; identify missing owners, cycles, unnecessary
   crates, overly broad modules and inconsistent filenames or role suffixes.
2. Review the proposed opaque replay/security prerequisites, added storage
   dependencies and SEAL/ledger crash join; check API visibility, component versus
   host authority, pure layers and command-scoped startup.
3. Check all 321 ownership mappings, COV-01/02/03 and the corrected XA-03 graph/finding.show
   scope; assess the private 13-field recovery record and all F00–F53 cases,
   including witness recovery and both database transaction orderings.
4. Check independent provider releases/toolchains, shared contract surfaces,
   schema/runtime-binding generation, SDK reuse and build/asset closure joins.
5. Check report ownership, offline assembly, runtime validation, renderer parity,
   browser safety/accessibility and the 24 proposed prototype feature dispositions.
6. Check tooling trial criteria, test/harness ownership, disposable index recovery, current documentation
   ownership and the remaining tool-specific configuration decisions.

Require substantive findings with paths and reasons, explicit dispositions for
open decisions, and a verdict scoped to the exact reviewed bytes. Correct and
re-review any material changes before marking the topology accepted. Record the
actual response and unresolved findings in the existing review process, then
reconcile successor/application bindings and the central readiness register.
Do not mark readiness complete just because this layout review passes.

### Corrections following actual Claude review, 2026-09-11

Actual Claude’s complete layout and focused prototype reports are retained in
`docs/coop/design-corrections/reviews/claude-return-review.v1/` and
`claude-return-followup.v1/`. They required corrections; their completion is not
acceptance of new bytes. The current proposal has 198 target paths/20 groups,
including the pure syntax crate, and 54 planned recovery cases. Security owns
its session/SEAL adapter types and depends on the pure evaluator; host keeps
dispatch, fact admission and lifecycle coordination. Report migration now maps
all five legacy tab groups and removes hidden test exclusion. The companion
plan specifies retained grammar/release joins and generation/asset row shapes.
Carrier and lineage corrections are integrated as author work. Final source rebinding and independent changed-byte review remain open.
Historical dated counts above describe their earlier checkpoints.
