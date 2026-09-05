# OpenSIP V2 MVP and Future Scope

> **Status:** DRAFT SCOPE MAP — non-binding; product acceptance remains open
> **Authority:** Scope labels do not override V1 authority, apply a successor, or
> close any entry in the [central register](08-decision-and-readiness-register.md).

This document is a human-readable scope view, not a second checklist. Every
readiness state, owner, decision, and acceptance artifact lives in the central
register.

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
