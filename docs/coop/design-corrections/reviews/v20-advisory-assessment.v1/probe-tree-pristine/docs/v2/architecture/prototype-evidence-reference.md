# OpenSIP CLI Prototype Evidence Reference

> **Status:** PINNED REVIEW INPUT — non-binding
> **Authority:** Prototype evidence and migration baseline only; it creates no V1
> or V2 semantic/product authority.

The reviewed prototype is the separate `opensip-cli` repository at clean commit
`a62509d623173155d0946e9f5d5ca90c839893e0`. Every path below is interpreted at
that commit. A later prototype head does not silently replace this baseline.

## Role and capability inventory

| Prototype role/capability | Pinned evidence path | Acceptance semantics carried into V2 |
|---|---|---|
| Host CLI grammar and mounted tool commands | `AGENTS.md` “CLI bootstrap flow”; `packages/cli/src/bootstrap/register-tools.ts` | Host owns grammar/dispatch; manifest discovery never hands a component raw root parser authority |
| Language adapters and analysis tools | `AGENTS.md` bundled language/tool registry inventory; package manifests under `packages/languages/`, `packages/tool-*`, `packages/graph/`, `packages/yagni/` | Product-selected roles must receive a pinned capability/parity matrix; this inventory is a baseline, not an invented V2 support promise |
| Stable findings/outcomes and machine views | `packages/contracts/src/signal-envelope.ts`; `packages/output/src/format/`; output formatter tests | Same semantic outcome across applicable human/JSON/SARIF views; no renderer owns policy, evidence, or exits |
| SARIF 2.1.0 | `packages/output/src/format/signal-sarif.ts`; `packages/contracts/src/command-presets.ts`; graph/yagni CLI tests | Optional for commands that advertise it; parity/loss requirements are DR-122/DR-G17 |
| Baseline/ratchet | `AGENTS.md` baseline section; `packages/contracts/src/baseline-export.ts`; datastore baseline schema/tests | Corpus records existing findings; comparison gates net-new findings using stable fingerprints; export does not become semantic authority |
| Component/tool discovery and admission | package `opensipTools` manifests; `packages/cli/src/bootstrap/register-tools.ts`; compatibility/admission tests | Manifest-first, deny-by-default, stable IDs distinct from versions/aliases; no implicit execution during discovery |
| Local state, sessions, purge, doctor/redaction | datastore/session/tool lifecycle packages and their tests; command inventory in `AGENTS.md` | Durable local evidence and explicit purge; doctor/redaction and lifecycle requirements must be host-owned and typed |
| Verification and release UX | root `package.json`, release checks, action/SARIF fixtures | Verifiable artifacts and CI behavior are retained as product lessons, without inheriting npm/Node lockstep packaging |

## Corpus, baselines, and quality use

The commit pin above makes the prototype source inventory reproducible. It does
**not** establish a digest-pinned language-quality corpus, accepted capability
matrix, behavior/performance measurements, or parity threshold. Those artifacts
do not exist in this V2 snapshot and remain OPEN future acceptance evidence at
DR-118 and DR-G13.

Before any supported role can claim language-native quality, its owner must pin
the exact corpus/fixtures/goldens and their digests, record measured current and
target behavior/performance, known limitations, and product-approved parity or
improvement thresholds. A missing or inapplicable prototype baseline must be
stated explicitly and replaced only by a product-approved language-native
corpus. No role may silently fall back to a weaker parser, syntactic tier,
graph, or finding model.

## Limits of this reference

This pin confirms inspectable prototype lessons and source locations; it does
not itself confirm measured quality or acceptance behavior, freeze the
prototype package topology, claim that every prototype capability ships in V2,
or make the Node/npm lockstep train a V2 distribution model. Exact product
support remains DR-118. V1 authority and status still resolve through the V1
baseline, status-evidence manifest, claim matrix, and central register.
