# V1-to-V2 Relationship and Migration

> **Status:** DRAFT — non-binding relationship guide
> **Authority:** `docs/coop` remains the untouched V1 history/evidence/status corpus.
> **Readiness:** [DR-001 through DR-011, DR-203, DR-204; DR-012 is release-only](08-decision-and-readiness-register.md)

## Documentation relationship

| Location | Role |
|---|---|
| [`docs/coop`](../../coop/) | V1 exact artifacts, reviews, adjudications, checkers, product decisions, and status evidence |
| [`docs/v2/architecture`](README.md) | Readable non-binding V2 working surface and design delta |
| [`v1-authority-baseline.json`](v1-authority-baseline.json) | Reproducible V1 review snapshot; verifies inputs but creates no authority |
| [`v1-status-evidence.json`](v1-status-evidence.json) | Pinned independent review/adjudication/closure/checker evidence for matrix standing |
| [Prototype evidence reference](prototype-evidence-reference.md) | Clean source commit and role/capability navigation only; no authority and no accepted quality corpus/measurement baseline yet |
| [V1-to-V2 claim matrix](09-v1-to-v2-claim-matrix.md) | Exact selector/status/disposition mapping into V2 sections |
| [Decision/readiness register](08-decision-and-readiness-register.md) | Single active blocker/decision/review/gate checklist |
| `docs/v2/implementation/` | Reserved and absent until the register's blueprint gate is satisfied |

V2 does not relocate, rewrite, or retroactively relabel V1. It also does not
assume a later filename supersedes a pinned head. Baseline refresh follows the
stop-on-conflict rule in [Status and authority](00-status-and-authority.md).

## Preserved structural laws

V2 carries forward, subject to exact matrix standing:

- host authority over admission, Snapshot/Plan, facts/findings, Coverage,
  policy/verdict, finalization, durable state, D9, and output;
- facts/FACT-ID, Coverage, Plan/PlanId, Run/evidence separation, and D9 semantic
  boundaries;
- RequestId-before-validation, ExecutionId-at-admission, frozen pre-attempt
  PlanIntent, and exact-type admission before identity derivation;
- six-layer configuration, CFG-9, CI layer-4 exclusion, per-value provenance,
  and secret-value exclusion at its exact scope;
- local-first/no-write first value, explicit adoption, and offline analysis;
- pinned-root signed delivery, exact bytes, revocation/expiry/anti-rollback;
- honest fault-containment versus confinement; and
- TypeScript major 1 and merged Rust major 2 provider subprotocols with R-1
  one-shot/no-reuse constraints.

## Inherited conditions, not preserved recipes

V2 does not convert accepted-but-unapplied or unset V1 material into law.
EVIDENCE and TM remain `UNSET — BLOCKS FREEZE`; Phase-1A and V10/G19 are absent;
freeze §7.1 identity recipes remain parked. `RunId`, `EvidenceDigest`, sealed-Run,
replay, verification, inspection, purge degradation, and typed result/exit are
therefore architectural constraints or open integration work, not settled V2
recipes. See DR-002 through DR-009.

## Proposed physical/product delta

V2 proposes:

1. a small signed distribution core and semantic host;
2. optional independently released components under one lifecycle/control plane;
3. a signed deterministic index/lock and immutable multi-version generations;
4. a management-only core profile; and
5. a signed authoritative offline analysis closure that includes verified
   durable storage mechanics.

This exceeds V1's P-1/P-2/G3 product boundary in possible catalog/ecosystem
depth. Product-owner successor DR-117 is mandatory before acceptance. Until
then, V1 marketplace, untrusted native/WASM, imperative contribution, probe,
and network-grant exclusions remain.

## Migration constraints

A future reviewed transition must preserve tracked intent, the same no-write
pre-initialization value, per-value provenance, historical identities/custody,
and promised offline behavior. It must distinguish:

- distribution migration from user-custody state migration;
- management-only core adoption from installation of an authoritative closure;
- immutable coexistence from in-place package mutation;
- removal from explicit purge; and
- replay pinning from contract-approved typed degradation.

No migration silently downloads, refreshes an index, mutates a lock, creates
replacement historical identities, rewrites evidence meaning, or treats
telemetry/network as required.

## Confirmed prototype lessons and owners

The [clean pinned prototype](prototype-evidence-reference.md) is evidence, not a
package template. Each lesson has one V2 owner and test target:

| Prototype lesson | V2 owner / decision | Acceptance target |
|---|---|---|
| No-write first value and identity-preserving adoption | CLI/product, DR-123 | clean-project no-write/adopt/upgrade corpus; historical IDs unchanged |
| Manifest-first discovery | Component architecture, DR-103/104 | metadata-only help/list/completion; hostile manifest/collision tests |
| Stable IDs distinct from aliases/versions | Product/CLI, DR-104 | rename/alias/version/coexistence goldens |
| Exact-byte, deny-by-default explainable admission | Delivery/security, DR-103/105/126 | DR-G07/G09/G22 hostile bytes, loader, permission/refusal corpus |
| Uniform outcomes and output projections | Semantic/output, DR-122/123 | D9 plus human/JSON/SARIF parity/loss goldens DR-G17 |
| Strict config, provenance, and secret handles | Configuration/security, DR-108 | CFG-9/layer/provenance/redaction/broker tests |
| Verifiable releases and offline indexes | Release/security, DR-103/112 | DR-G06–G08 signed clean-machine/air-gap/update/rollback corpus |
| Doctor, diagnostics, and redaction | Operability/security, DR-114/125 | DR-G12/G20 stable schema, no-code/no-network, redaction and consent tests |
| Supervision, cancellation, recovery, and host-mediated effects | Supervisor/protocol, DR-102/105/107/125 | DR-G09/G18/G21 crash, timeout, broker, cleanup and recovery corpus |
| Durable evidence, state ownership, migration, retention, purge | Evidence/storage/lifecycle, DR-002–008/109/113/124 | DR-G11/G18/G19 custody, state-class, replay/removal/purge tests |
| Language capability and baseline quality | Product/language owners, DR-118 | OPEN: future digest-pinned role/corpus capability matrix and DR-G13 behavior/performance measurements/thresholds; the prototype commit alone is insufficient |

Rejected prototype shapes remain lockstep Node/npm versions, Node as default
core burden, split lifecycle/RPC, duplicate recovery, implicit update egress,
managed/hash-matched as complete trust, or a process boundary called a sandbox.
DR-203 records the review disposition.

## Blueprint transition

The later implementation directory may be created only when the single
[blueprint-readiness decision](08-decision-and-readiness-register.md#blueprint-readiness-decision)
is satisfied and product/architecture authorities explicitly authorize it.
Architecture prose, review completion, or a green checker alone is insufficient.
DR-012 release qualification is deliberately not circular: it does not block
authoring a lawfully authorized blueprint after DR-001–011 and applicable V2
architecture decisions receive exact dispositions. It still blocks release and
authoritative launch, and the blueprint cannot claim qualification.
