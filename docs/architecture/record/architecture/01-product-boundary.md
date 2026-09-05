# 01 — Product boundary

**Status:** SEALED unless noted.

What opensip-cli is, what it refuses to be, and the constraints every other
document inherits.

---

## The product

A **local-first, deterministic evidence-and-enforcement control plane for
codebases** — especially AI-edited ones. Four pillars:

| Pillar | Meaning |
|--------|---------|
| **Intent** | Rules, scopes, and gates are declared, not implied |
| **Executable rules** | Deterministic analysis yields pass/fail plus ranked findings |
| **Durable evidence** | Runs are addressable, queryable, reproducible, exportable |
| **Capability control** | Scope is explicit; automation must leave proof |

## The central inversion

**SEALED.** The product is *not* "a CLI that hosts five peer tools." It is an
**evidence compiler over a project snapshot**.

- Tools, packs, and scanners are **producers**.
- CLI, MCP, SARIF, HTML, and Cloud export are **projections**.
- The host is the **only** writer of durable state.

Designing around "Commander plus plugins" yields a tool dispatcher. Designing
around `intent → analysis → evidence → surfaces` yields the product. This single
inversion is the parent of nearly every other decision in this set.

---

## Hard constraints

These are product boundaries, not implementation preferences. Violating one is a
product change requiring explicit sign-off.

| Constraint | Consequence for architecture |
|------------|------------------------------|
| **No model calls in the product path** | The analysis kernel is deterministic. Model-driven fix generation belongs to the platform, never the CLI. |
| **Local-first and fully useful offline** | Network is default-deny. No feature may require Cloud to produce a verdict. |
| **First value before `init`** | The CLI composes validated in-memory defaults and keeps state in a user-scoped location with **separately labelled** authoritative ledger/evidence and rebuildable cache partitions; nothing lands in the customer repo until they ask. |
| **Agents and CI are first-class clients** | Machine surfaces are designed, not retrofitted. MCP is not CLI-string scraping. Exit codes and JSON are frozen harder than TTY output. |
| **Cloud is a consumer of evidence** | The analysis kernel has zero Cloud imports. Cloud failure can never change a local verdict. |
| **Polyglot analysis with strategic depth in two languages** | One shared extraction substrate. Depth is expressed as a **semantic provider**, and P-4 is decided: **TypeScript and Rust** get one; all other supported languages ship at the syntax/reference tier. The tier difference is surfaced **loudly** at the point of use — see [04](04-fact-plane.md#provider-coverage-and-the-capability-tier). |
| **The v1 provider spine is closed** | The only deep provider processes are the bundled TypeScript worker and bundled pinned-`rustc_driver` sidecar, named canonically `typescript-semantic` and `rust-semantic` in C-2, RI and DELIVERY. C-2 retains `external-scanner` in the general ontology, but v1 rejects its frozen pre-admission `PlanIntent` with `FEATURE.EXTERNAL_SCANNER_NOT_IN_V1` before allocating an attempt; D9 projects the existing `EXTENSION.ADMISSION_REJECTED` code. Non-bundled or unknown semantic-provider identities reject as `FEATURE.SEMANTIC_PROVIDER_NOT_IN_V1`. |
| **Finite initial platform promise** | The supported domain is Linux x86_64/aarch64 GNU (kernel 5.4, glibc 2.28), macOS arm64/x86_64 13+, and Windows x86_64 MSVC (Windows 10 22H2 / Server 2022). Each supported row defaults to the full TypeScript+Rust profile and must pass the offline release lane. Other targets are best-effort, not silently included. |
| **Unselected authority is absent, not aspirational** | Until `ARCH.PROBE-CONTRACT` selects a restricted runtime, imperative contributions, Probes, untrusted native/WASM code, scenario effects, and network-granted analysis are rejected at admission. |
| **Product scope is a total admission overlay** | `delivery.v4.json#initialProductScope.v1PlanIntentOverlay` assigns every live C-2 exclusion-bearing enum value `ALLOW`, `ALLOW_IF`, or `DENY`. It covers topology, workflow, network/remote computation, all repository-execution switches, contribution origin/authority, capability kind, stage kind, fact-derivation operator, and the TypeScript semantic-stage budget unit. TypeScript accepts absent or `work-units`; `milliseconds`, `bytes`, and `items` reject before attempt admission. A new C-2 value fails the retained DELIVERY checker until product classifies it. |

## Why the CLI/platform split is load-bearing

**SEALED.** opensip-cli is the open-source guardrail layer producing deterministic
evidence; the platform is the autonomous maintenance loop built on top. The
entire trust story depends on the CLI calling no models: a human or an agent can
believe a claim because the evidence behind it is addressable and reproducible.
Softening this boundary removes the reason the product is credible.

---

## What is deliberately rejected as the architectural center

| Temptation | Why rejected |
|------------|--------------|
| Generic Tool-plugin platform as the ontology | Optimises plugin symmetry over product coherence; forces product invariants to be reconstructed with seams, guardrails, and ADRs |
| Graph as a peer tool silo | Forces lateral dependencies and duplicate inventories between tools |
| Tool-private persistence | Fractures agent query and gate semantics |
| 50+ micro-packages on day one | Release tax without install customers |
| Datalog and DataFusion as day-one requirements | Unvalidated complexity; both are implementation selections deferred behind a logical `FactQuery` |
| All rules out-of-process, uniformly | Security purity at the cost of agent-loop latency; tiered execution instead |
| Ambient scope / service locator as primary DI | Explicit context in-process; a wire protocol out-of-process |
| UI-driven architecture | The TTY is a projection, never the source of truth |
| Making Cloud a required plane | Breaks the local-first thesis |

---

## Non-goals

**SEALED.** Explicitly out of scope; do not design for these without a product
decision:

- Multi-tenant SaaS behaviour inside the CLI
- IDE extensions as the primary surface
- In-CLI LLM inference of any kind
- Replacing git
- Billing or entitlement logic inside the analysis kernel
- Custom database backends on day one
- A public extension marketplace before the threat model, capability matrix, and
  supply-chain governance are sealed

## Honest limits the product must not overstate

**SEALED.** Two claims that must never appear in documentation or marketing:

1. **A process boundary is not a security sandbox** unless an OS-level confinement
   profile is active. Process isolation buys fault containment and compatibility.
2. **No extension mechanism can promise source confidentiality** from a producer
   that reads source and returns text. The finding stream is an exfiltration
   channel. The honest promise is capability-scoped ambient I/O — no network, no
   unexpected filesystem, no inherited secrets — not "your source cannot leak."

A related engineering corollary appears in
[05-rules-and-extensions](05-rules-and-extensions.md): in a language with ambient
module resolution, **no in-language signature is a capability boundary**.
