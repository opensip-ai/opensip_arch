# OpenSIP product scope and delivery stages

> **Current direction — binding scope selection under D-371:** One complete design for the intended product,
> implemented in stages. The preview is a delivery milestone. Its completed
> design does not establish completion of the whole product design.
> [File 08](08-decision-and-readiness-register.md#unified-product-design-readiness)
> owns the remaining readiness state. The older scope map below remains a
> record of the preview-era dispositions.

## One product design

The design target is one local-first, language-extensible evidence and
assessment platform. Its common host owns discovery and admission, invocation
planning, evidence identity and storage, evaluation, policy, comparison,
authorization, and output. Independently versioned capabilities contribute
native evidence or project host-owned results through those common contracts.

The target includes useful analysis without prerequisite configuration;
single-step and composed invocations; language-native static analysis and
clone evidence; explicit test, runtime, and history evidence intake; durable,
verifiable results; stable findings and baseline/delta assessment; declarative
policy authoring and testing; bounded advisory discovery, inspection and review;
and separately authorized repair with verification. CLI and machine clients
use the same assessment model. Optional Map judgments retain their advisory
status and cannot supply Control verdicts.

These are design obligations now. Shipping a capability later does not defer
its architectural ownership, public contract, compatibility, failure behavior,
or interaction with other capabilities until after implementation. The
[Fallow-informed constraints](13-evidence-workflows-and-product-contracts.md)
apply throughout this product design. Their historical `future` labels
identify capabilities outside the preview, not permission to leave required
product architecture unresolved.

The bounded intended-product selection is:

| Area | Selected design scope |
|---|---|
| Native language depth | TypeScript/JavaScript through the TypeScript role, and Rust through the Rust role. Additional languages require a later explicit support decision. DR-118/119 must still settle each capability/platform cell and its limitations. |
| Platforms | Preserve the preview's macOS and Linux, arm64 and x86_64 target families. Broader historical platform lists are not newly promised by this act. Exact baselines and supported closures require full-product reconciliation at DR-119/126. |
| Evidence and surfaces | Authoritative Control results, custody/retention/replay/purge, baselines, CLI/JSON, applicable SARIF/HTML and agent projections, diagnostic and signed update/recovery workflows. |
| Advisory work | Candidate discovery, inspect/review contracts and optional Map/provider integration boundaries are designed now. A bundled model, embedding engine or conversational Map application is not required for this design's completion. Model judgments remain external/advisory. |
| Repair | Deterministic host-authorized preview/apply/verify lifecycle and native action contracts; no implicit mutation or model-driven autonomous maintenance loop. |
| Existing users | Explicit coexistence and fresh-install posture. Legacy state is not silently adopted as authoritative; any selected import must validate provenance and compatibility. DR-130 must settle and review the transition contract even if it selects no automatic migration. |
| Exclusions | Public marketplace, third-party publisher ecosystem, untrusted executable/WASM contributions, remote execution, credential-requiring features, automatic repository-code execution and TUI. No additional language or platform promise follows from extensibility. |

These choices use the existing delegated product authority. Exact schemas and
support/parity evidence are still required at their owning rows; this scope
selection is not their acceptance. Discovery resolves to host inventory or an
existing language-provider role, not a new contribution kind.

## Language-independent contracts, native implementations

The Fallow lessons are not TypeScript-only. Their placement is:

| Common product contract | Language or ecosystem implementation |
|---|---|
| Repository discovery, defaults, provenance and configuration recommendation | Language/framework/layout recognition and entry-point rules |
| Facts with explicit scope, evidence requirements and visible omissions | Parsers, compiler/checker integrations, symbol and reference resolution |
| Clone candidates, inspection and distinct review judgments | Token/AST normalization, structural matching and language-specific equivalence limits |
| Test/runtime/history evidence identity, freshness and observation coverage | Ecosystem-specific collectors, coverage formats and source/build mapping |
| Stable findings, baselines, regression gating and attribution | Versioned native rule semantics and subject correspondence |
| Invocation steps, host policy, output contracts and action authorization | Capability adapters operating inside the shared host lifecycle |

A provider declares its supported language and role, capability version,
applicable scope, required inputs and produced evidence families. Each result
binds the analyzed source/view and records actual coverage and unavailable
requirements. The host evaluates sufficiency for the particular predicate or
action; the provider cannot assign the product verdict. Installed, applicable,
executed and sufficient are distinct questions.

For example, a TypeScript checker can resolve exports and type references;
a Rust provider needs its own native semantics for traits and conditional
compilation. The same policy surface can consume either provider's declared
evidence, but must return indeterminate when a required relationship cannot
be established. Neither a generic syntax adapter nor another language's
provider silently substitutes for the missing capability.

Fallow's V8/Istanbul imports are JavaScript-ecosystem adapters. OpenSIP's shared
evidence contract must also accommodate other ecosystem adapters without
assuming identical coverage semantics. Untracked code differs from observed
code with no hits; observation in one window is not proof of universal non-use.
Cross-language clone matching similarly does not prove semantic equivalence.

The required acceptance cases include mixed-language repositories, supported
and unsupported capability combinations, partial framework recognition,
stale or unmapped runtime evidence, missing native semantic inputs, and
consistent host policy/output across providers. DR-118/119 and the evidence
owners select exact supported cells and corpora before full design acceptance.

## Delivery stages within that design

The existing preview can remain the first implementation milestone. Subsequent
milestones activate the designed durable evidence, comparison, richer analysis,
advisory review and repair capabilities in dependency order. Milestones do not
create separate architectures or incompatible private tool state models.

Full design acceptance requires resolving the product contracts and their
cross-capability joins. Implementation planning then selects code structure,
algorithms within the accepted contracts and delivery order; qualification
demonstrates the resulting product on its supported targets. A complete design
does not claim that implementation or qualification has already happened.

## Historical preview-era scope map

> **Status:** DRAFT SCOPE MAP — non-binding; product acceptance remains open
> **Authority:** Scope labels do not override V1 authority, apply a successor, or
> close any entry in the [central register](08-decision-and-readiness-register.md).

This document is a human-readable scope view, not a second checklist. Every
readiness state, owner, decision, and acceptance artifact lives in the central
register.

## Design decisions before implementation

[D-370](../../coop/COORDINATOR-DECISIONS.md#d-370--fallow-informed-product-design)
adopts [evidence workflows and product contracts](13-evidence-workflows-and-product-contracts.md)
as constraints for the product's design. It distinguishes clarification of
existing preview obligations from requirements on future discovery, review,
repair, runtime evidence, comparison, and policy-authoring capabilities.
Those requirements are settled before implementation; their adoption does not
admit the future capabilities into the preview or claim their exact schemas
and qualification are complete. The chapter maps each area to its existing
register owners for scope re-entry. D-369's preview contracts, accepted corpora,
required gates, row standing, and pending implementation authorization remain
unchanged.

## MVP commitments

These are preserved V1 constraints or explicit current V2 MVP directions. They
remain subject to their linked register gates.

| MVP scope | Register link and qualification |
|---|---|
| Standard command-oriented CLI with stable human/machine output and non-interactive CI behavior | DR-123; applicable SARIF is DR-122/DR-G17; blocks every first slice |
| Local-first/offline operation, strict configuration/provenance, secret-value exclusion, signed exact-byte delivery, honest security labels | DR-001–011, DR-103/106/112, DR-G06–G09 |
| Host-owned semantic authority for Plan/Snapshot, facts/findings, Coverage, policy, finalization, evidence, D9, and exits | DR-002–009; recipes remain blocked where V1 is unset |
| Small signed distribution-core direction plus at least one signed authoritative offline analysis closure | DR-101/106/115/117 and DR-G01–G06; product successor remains required |
| First-party or explicitly trusted components under one lifecycle/control model | DR-102–107/116; public ecosystem depth is not implied |
| Independent failure containment for every external analyzer/tool | DR-G21; required immediately and explicitly not a sandbox claim |
| Self-contained runtime/tool closure for every product-supported language role | DR-118–120 and DR-G13–G15; exact supported roles remain an open product decision |
| Durable-authoritative storage mechanics, custody, retention posture, recovery and honest purge | DR-002–008/106/109/113 and DR-G11/G18/G19; blocked by inherited V1 successors |
| Common component developer/operability contract and isolated monorepo qualification lanes | DR-121/125 and DR-G16/G20; APIs and CI implementation remain later design |

## Deferred or post-MVP directions

| Direction | Register link and boundary |
|---|---|
| Third-party sandboxed native/WASM components | DR-128: post-MVP; requires explicit product successor and demonstrated confinement, permission, platform, escape, revocation, and incident evidence |
| Public marketplace/catalog/ecosystem governance | DR-010/117/128: excluded by current P-1/P-2/G3 until product successor; not an MVP promise |
| Optional interactive TUI | DR-129: may add host-owned progress/exploration/remediation projection; cannot replace or package the CLI; framework deferred; blocks only a TUI-bearing slice |
| Additional language/tooling roles beyond the product-selected MVP set | DR-118/119: role list and parity thresholds remain open; no list is invented here |
| Remote/customer-owned external-system exceptions | DR-119: narrow product-approved exceptions only; never silently marketed as self-contained support |
| Network-granted analysis, probes, imperative contributions, and broader root commands | DR-117/128: post-MVP unless an explicit successor and enforcement evidence change the boundary |

## Out of scope or rejected shapes

| Shape | Register/source link and reason |
|---|---|
| Components choosing policy, verdict, Run/evidence authority, D9, or exits | DR-002–009/125; violates the closed semantic host boundary |
| Process isolation described as a sandbox without measured enforcement | DR-105/128 and DR-G09/G21; fault containment is not security confinement |
| Ambient/global runtime or implicit download for supported language analysis | DR-119/120 and DR-G14/G15; supported closures are signed and self-contained |
| Lockstep core/component/bundle/provider/state-schema versions | DR-107/111/127 and DR-G18; compatibility is per surface and independently releasable |
| A bundle as hidden promotion gate for otherwise compatible releases | DR-127; bundles qualify selections but do not erase independent compatibility |
| Lowest-common-denominator analysis or silent syntax fallback | DR-118 and DR-G13; capability/parity is corpus-based and language-native |
| Competing lifecycle/RPC/state/recovery models per component | DR-102/107/124/125; one host contract owns cross-cutting behavior |

## Ambiguity rule

If an item is not clearly preserved by exact V1 disposition or accepted in the
central register, it is `OPEN`, not an implied MVP commitment. This scope map is
refreshed only by linking the exact register disposition; prose here cannot make
V2 blueprint-ready or release-qualified.
