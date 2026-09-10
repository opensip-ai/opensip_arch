# Distribution and Component Architecture

> **Preview application:** D-369 applies the independently reviewed [reference architecture](../../coop/completion/reference-architecture.v2.md) and [exact successor manifest](../../coop/completion/architecture-application.v1.json). Older reservations and broader authoritative-product directions below retain their historical scope; the manifest names the sentences replaced for the preview. V1 claim/freeze status is unchanged. [File 08](08-decision-and-readiness-register.md) remains the only readiness checklist.

> **Status:** DRAFT — proposed V2 product/distribution delta
> **Authority:** V1 P-1/P-2/G3 exclusions remain until explicit product successor.
> **Readiness:** [DR-010, DR-101 through DR-107, DR-116 through DR-128, DR-205](08-decision-and-readiness-register.md)

## Three different meanings of core

V2 uses three terms and does not collapse them:

| Term | Meaning | Boundary |
|---|---|---|
| **Signed distribution core** | Proposed small native executable plus its mandatory runtime/data closure | Packaging, install, update, trust, management/recovery footprint |
| **Semantic host** | Host authority for admission, Snapshot/Plan, findings/facts, Coverage, policy, finalization, durable authority, D9, and output | May share a process with the distribution core, but authority is non-delegable |
| **Pure evaluation core** | R-1 data-only deterministic evaluation function returning `CoreCompletion` | No effects, callbacks, ports, entropy, filesystem, network, process, store, or resident state |

The distribution core and semantic host may initially be one executable. That
does not permit semantic work to migrate into components or effects into the
pure evaluation core.

## Proposed small signed distribution core

The default install is proposed to contain routing, strict configuration,
authentication, trust, updates, host semantic authority, output, component
protocol/supervision, lifecycle/recovery, and essential lock/journal/audit state.
It excludes language runtimes, analyzers, graph engines, report generators,
evidence databases, and telemetry backends from the default dependency closure.

“Small” is falsifiable, not aesthetic. Every release must publish:

- the complete mandatory file/dependency/TCB inventory and layer assignment;
- exact signed compressed and installed closure size;
- cold help/version startup and baseline/peak memory;
- evidence that help/version/config/status/doctor load no project or component;
- each component's incremental cost; and
- the aggregate authoritative offline closure cost.

Named gates DR-G01 through DR-G05 own the method, platform matrix, regression
policy, evidence, and waiver expiry. Numeric thresholds remain open at DR-115;
until decided and measured, V2 may say “small-core direction,” not “qualified
small core.”

## Management core versus authoritative offline analysis

Core-only is management and recovery: help, version, completion, configuration,
component inventory/lifecycle, status, doctor, and repair. It is not the current
full analysis product and cannot claim absent capabilities.

Every supported **authoritative** offline analysis closure must be a signed,
locally installable exact selection containing:

- the compatible distribution core/semantic host;
- required analyzers/providers and negotiated subprotocols;
- mandatory verified storage mechanics, or an explicitly inventoried minimal
  backend inside the signed core closure;
- the exact evidence/custody/recovery capability required by the current durable
  retention posture; and
- all offline trust/index/revocation/manifests/payloads needed on a clean machine.

Missing, unverified, or failed storage yields typed non-success; it cannot
silently downgrade an authoritative request or report success. Exact result/exit
is blocked by DR-007 and DR-113. Persistence remains optional only for the
management-only core distribution, never for a supported authoritative analysis
closure.

## One component architecture

**Proposed V2 direction.** All optional roles share stable opaque identity,
manifest-first discovery, one catalog/lock, one lifecycle, one supervisor, one
host result model, and independently signed releases. A manifest eventually
binds commands, capabilities, dependencies/prerequisites, compatibility, exact
immutable tree and entrypoint, publisher/provenance, SBOM/attestations,
permissions, configuration classification, state/migration, and update data.
Concrete schemas remain DR-103.

Help, completion, and inventory read authenticated metadata only. They do not
execute component code, load a runtime, resolve a project, open evidence, probe
customer tools, or use network. The host owns root grammar, flags, collisions,
dispatch, output, policy, finalization, and exits.

There is no required same-version coupling among distribution core, component
release, bundle revision, control protocol, TypeScript/Rust provider major,
state schema, evidence format, or index schema. Compatibility is expressed by
separate per-surface matrices under DR-111.

## Common component packaging and language build adapters

**Proposed V2 architecture model.** Every OpenSIP component release, regardless
of implementation language, emits one common packaging/admission contract:

- a canonical closed manifest and stable component/release identity;
- immutable archive and full-tree path/type/mode/length/digest commitment,
  including entrypoint and required runtime/tool bytes;
- signed publisher provenance plus bound SBOM, attestation, license, and notice
  inventory;
- explicit supported-platform alternatives and per-surface compatibility;
- declared capabilities, prerequisites, permissions, state/migration, and
  capability/performance parity evidence;
- static validation, health, and role/subprotocol conformance results;
- signed offline/air-gap installation inputs;
- deterministic update, rollback, repair, and revocation metadata; and
- download/install/startup/memory and role-quality gate evidence.

Language runtimes and ecosystems differ, so per-language **build adapters** may
use different internal build mechanisms. Each adapter is responsible for
collecting and normalizing its language's runtime/parser/compiler/language-server
closure into the same OpenSIP output contract. Variation ends at the adapter
boundary: admission, signing, exact-byte verification, lifecycle, offline use,
and measurement consume the common contract rather than language-specific
package-manager semantics.

DR-120 must define the adapter template and developer ergonomics: deterministic
and hermetic CI inputs, reproducible local validation, actionable missing-field
diagnostics, fixture generation, platform fan-out, and one conformance report
shape. Acceptance tests cover clean install, no ambient dependencies, hostile
paths, health/subprotocol negotiation, offline/air-gap use, update/rollback, and
all relevant size/quality/performance gates.

This architecture does not choose a concrete packager, build tool, language
toolchain, or command line. Those choices belong in `docs/v2/implementation/`
after DR-120 is accepted and blueprint work is authorized.

## Monorepo CI and independent component releases

**Proposed V2 architecture requirement.** OpenSIP may remain a monorepo while
components release independently. Declared component ownership and dependency
metadata select isolated language/component CI lanes; an unrelated change does
not force every language closure to build. The selector must fail safe when
ownership or dependency impact is ambiguous.

Each selected component lane builds, tests, packages, signs, attests, emits an
SBOM/license inventory, and qualifies its self-contained closure on the relevant
manifest-declared platforms. It also runs its language-native capability/parity,
behavior, performance, runtime-UX, packaging-adapter, and conformance gates.

Separate lanes cover:

- the shared distribution core/semantic host/pure-core contracts;
- common control protocol and unchanged opaque provider data planes;
- semantic-authority and D9/fate integration;
- deterministic lock/dependency/compatibility resolution;
- clean-machine authoritative offline closure; and
- aggregate convenience/air-gap bundle qualification.

Independent releases do not require separate repositories and do not create
lockstep versions. A release selects independently qualified compatible bytes
through signed metadata and per-surface matrices.

DR-121 and DR-G16 require acceptance tests for correct lane selection, omitted
dependency/owner detection, per-lane exact release evidence, and cross-component
integration. CI provider, YAML, repository path filters, caches, commands, and
implementation tooling remain reserved for the later blueprint.

## Exact control/data-plane demarcation

The proposed common control plane may only:

- discover authenticated manifest capabilities;
- start/stop/supervise a component;
- negotiate an opaque named role subprotocol and version;
- carry cancellation/health/resource/fault control; and
- broker separately authorized host effects.

It must not wrap, translate, normalize, reorder, reinterpret, merge, or assign
new fates to semantic frames of an existing provider protocol.

Host control events and opaque provider data may race, but precedence remains
host-owned and deterministic. The host defines joins for cancellation versus
result, control fault versus provider fault, EOF/process death, duplicate or
late frames, and teardown. Hostile dual-channel conformance exercises every
ordering while comparing provider semantic frames byte-for-byte: the control
plane may decide supervision/fate only under the owning contract and cannot
translate provider meaning to resolve a race.

## Common component developer and operability contract

Language analyzers and tools do not reimplement cross-cutting product behavior.
The host plus common component SDK/control contract provides standardized:

- structured candidate/result/fault envelopes and host-owned human, JSON, and
  applicable SARIF projection;
- diagnostic taxonomy, redaction, bounds, structured logging/audit correlation,
  progress, and status;
- schema-checked configuration with provenance and brokered secret handles;
- artifact/state brokers, cancellation, deadlines, resource reporting, trust,
  lifecycle, and doctor integration; and
- consistent host verdict/finalization/D9/exit mapping.

Components may emit domain candidates, events, progress, and bounded structured
diagnostics. They must not render product UI directly, choose verdicts/exits,
seal evidence, write unstructured host logs, or bypass host brokers. Common
look-and-feel and operability across components are DR-125/DR-G20 acceptance
properties; exact SDK APIs and frameworks remain implementation design.

## Independent failure containment

Every external analyzer/tool is supervised as an independently failing
component. Crash, panic, malformed/truncated stream, timeout, resource breach,
or unexpected exit is detected by the host, which cancels and reaps the process
tree, discards uncommitted candidates, emits bounded/redacted structured
diagnostics and audit correlation, preserves already sealed evidence, and maps
the event through host Coverage/D9 rules. The core process must not crash; the
host continues or terminates the command gracefully as the exact contract
requires, and components never choose UI or exit behavior.

DR-G21 covers crash/panic, timeout, malformed/truncated/duplicate output,
resource breach, process-tree cleanup, core-survival, recovery, Coverage fate,
and host output/exit goldens. This is fault containment, not automatically a
security sandbox: an unconstrained same-user component remains trusted code in
the TCB unless effective confinement is enforced and measured.

### TypeScript provider

The effective DELIVERY contract is the applied `delivery.v4` derivation
(`3cffe…121`) over `delivery.v2` (`47b6cf…bf3`). Selector
`$.typescriptSemanticSubstrate.providerProtocol.major` is **1**. Its closed
canonical-CBOR frames, identity, sealed-VFS, commitments, Coverage, D9/fault
joins, conformance goldens, one child per
`(ExecutionId, SnapshotId, TypeScriptSemanticUniverseKey)`, and no reuse remain
unchanged. R-1 one-shot/lifetime-neutral constraints also apply.

### Language runtime and toolchain UX

**Proposed V2 product rule, binding only if accepted through DR-119.** Every
supported programming-language analyzer/tool component supplies the non-system
dependencies it requires—language runtime, parser, compiler, language server, or
analogous tooling—inside its signed, verified, platform-qualified component
closure. The end user does not separately install, select, update, or manage
them. There is no ambient `PATH`/system-runtime lookup, project package-manager
resolution, or implicit download.

The component manifest declares every bundled runtime/tool byte and exact tree,
entrypoint/loader binding, license/notice, SBOM and attestation, supported
platform/compatibility matrix, and capability/performance parity evidence. If
the closure is missing or incompatible, the host returns a typed unavailable
result with explicit local/offline remediation. It never silently substitutes a
system tool or weakens semantics.

A narrow exception is possible only for a customer-owned external system that
cannot lawfully or technically be bundled, such as a remote service or privileged
platform facility. The exception requires explicit product approval, names
ownership/trust/network/prerequisites, appears in manifest and doctor output, and
has typed absence/failure behavior. It must never be marketed or silently treated
as a supported self-contained language analyzer.

The prototype's Node installation friction is the motivating concrete case:
supported TypeScript analysis must package/provision compatible Node as verified
signed bytes and reject ambient/global Node. Exact packaging, signing,
notarization, exception, and platform mechanics remain owned decisions under
DR-119 and gate DR-G14. This rule joins authoritative offline closure DR-106,
exact-byte gate DR-G07, manifest DR-103, and quality/parity DR-118.

### Rust provider

The normative Rust contract is **major 2** and exists only as the merge of:

- v4 overlay `3e349…2909`;
- v2 base `6308…93b` as merge input, never standalone;
- delivery join `02d7…6146`; and
- resolved-inputs join `4ce77…763e`.

Resolve `v4#$.retainedV2SemanticProjection.mergeAlgorithm`. The base's two
blockers were discharged by v4 deletion; building the rejected base alone is
forbidden. The merged ordering/state/fates, conformance goldens, D9/fault joins,
one supervised sidecar per semantic universe, and no reuse are preserved.

Any semantic frame/fate or lifetime change to either protocol needs an explicit
successor from the owning V1 surface. The common control protocol cannot make
the change by negotiation.

## Current V1 product boundary and required successors

V1 product authority currently says:

- P-1: no marketplace, public lifecycle parity, discovery service, or ecosystem
  governance depth;
- P-2: contributions are narrow producers or data-only rules/profiles, with no
  root commands, policy, persistence, rendering, termination, or host lifecycle;
- G3: full-default Rust host/core plus bundled TypeScript and pinned Rust
  sidecar/offline assets is the V1 substrate.

An independently released public catalog/lifecycle may exceed all three. Before
acceptance, product owner DR-117 must explicitly disposition:

1. marketplace/catalog and governance depth;
2. external lifecycle parity and discovery;
3. contribution roles beyond narrow/data-only;
4. untrusted native or WASM admission and required enforcement evidence;
5. imperative contributions, probes, project hooks, and root commands;
6. network-granted analysis and egress defaults; and
7. replacement of the full-default G3 physical substrate.

Until then, V1 exclusions remain: no ecosystem-depth promise, untrusted
native/WASM, imperative contributions, probes, or network-granted analysis by
default. V2 may define a future-safe boundary but cannot ship those policies by
architecture prose.

## Prototype constraints retained

The pinned prototype reference is
[`a62509d6…`](prototype-evidence-reference.md). V2 carries forward stable IDs,
manifest-first discovery, exact-byte admission,
supervision/cancellation/recovery, host-mediated effects, and uniform outcomes.
It rejects the prototype's lockstep Node/npm train, default runtime burden,
split lifecycle/RPC models, duplicate recovery machinery, and process-as-sandbox
claims. These dispositions are recorded at DR-203.

## Language-native product quality

**Proposed V2 product-quality requirement.** A native/Rust distribution core does
not require every analyzer to be implemented in Rust. Implementation language is
chosen per role to preserve or improve the target language's semantics,
ecosystem fidelity, and operational quality—not to force all roles through a
lowest-common-denominator abstraction.

For every language/tooling role the product elects to support, DR-118 and
DR-G13 require:

- an explicit capability/parity matrix against a future product-approved,
  digest-pinned role corpus, fixtures, measured baseline behavior/performance,
  and accepted current path; the prototype commit supplies source navigation,
  not that acceptance manifest;
- language-specific semantic, identity, Coverage, graph, and failure goldens;
- behavior and performance baselines on supported platforms/corpora;
- documented known limitations and unsupported tiers;
- typed unavailability or refusal when required semantics are absent; and
- tests proving there is no silent fallback to a weaker syntactic, semantic, or
  graph answer.

TypeScript analysis must meet product-approved parity/improvement thresholds
against the future accepted corpus for the selected scope. Rust analysis must
meet its product-approved Rust-native corpus/capability thresholds. No such
digest-pinned quality corpus or accepted measurement manifest exists in this V2
snapshot, so these are OPEN evidence requirements rather than current quality
claims. The exact languages, tools, tiers, and parity thresholds are product
decisions; V2 does not invent a support list or choose analyzer implementation
languages. This requirement is a blueprint-readiness and review gate, not a
binding implementation choice.

Every matrix also records the self-contained runtime/tool user experience and
proves the signed closure produces accepted quality on clean offline machines.
For TypeScript that includes no ambient/global Node; see DR-119 and DR-G14.
