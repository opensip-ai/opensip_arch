# Configuration and Security

> **Status:** DRAFT — V1 laws separated from proposed V2 mechanisms
> **Authority:** Resolve RESOLVED-INPUTS, DELIVERY, TM, and product selectors in
> the [claim matrix](09-v1-to-v2-claim-matrix.md).
> **Readiness:** [DR-003, DR-103, DR-105, DR-108, DR-112, DR-116](08-decision-and-readiness-register.md)

## Preserved V1 configuration law

Effective configuration resolves in this order:

1. compiled defaults;
2. user-global settings;
3. tracked project intent;
4. untracked local override;
5. allowlisted environment; and
6. command flags.

CI/non-interactive does not load or resolve layer 4 and does not reject merely
because a layer-4 file exists. Local-interactive may resolve layer 4; every
analysis-affecting winning value and `decidingLayer=4` provenance enters the
existing Plan path. Unknown tracked keys fail closed.

CFG-9 is exact: **only allowlisted analysis-affecting user-global keys enter
analysis resolution; every other user-global key is forbidden from analysis
resolution entirely.** Excluding a UI/theme/TTY preference from PlanId is not
enough if analysis can still observe it.

## Proposed V2 component configuration

Component configuration is proposed to be namespaced and schema-closed. The host
reviews every field's analysis classification and maps admitted values into the
existing resolution/Plan semantics. A component cannot add a private precedence
layer, classify its own hidden semantic input, or read non-allowlisted global
configuration.

The project component lock records selected signed inputs and deterministic
resolution, not secret values, user trust decisions, or self-granted authority.
Its concrete schema is DR-103.

## Preserved V1 secret-value scope

The V1 rule applies to **resolved configuration secret values and credentials**.
They are referenced by handles; the handle participates where the exact contract
requires it, while the value is excluded from PlanId, evidence digest,
diagnostics, and support bundles. RESOLVED-INPUTS v2 contains a stale CFG-6 note
about the then-current TM v2. The pinned TM v3 restores finding V11 and records
`A1-TM2-01` resolved, so CFG-6 has a live threat root. TM remains
`UNSET — BLOCKS FREEZE` for V10/custody/G19, not for CFG-6; the stale
cross-artifact note is a DR-011 reconciliation residual.

This rule does not classify arbitrary analyzed source text as a configuration
secret and does not promise that code authorized to read source cannot observe
credentials embedded in that source. Source confidentiality requires actual
read-set and confinement enforcement, not handle terminology.

## Proposed credential storage and brokering

OS keychain storage and a verified-permission user-file fallback are proposed,
not inherited settled V1 mechanics. Platform behavior, migration, recovery, and
threat evidence are open at DR-108. A future broker may resolve an admitted
secret handle for one bound operation without logging the value; exact API and
platform guarantees await that decision.

## Preserved signed-delivery laws

V2 must retain the applied DELIVERY properties for pinned non-TOFU bootstrap,
threshold signing, root rotation, revocation, expiry, snapshot consistency,
anti-rollback, exact digest/size closure, offline verification bundles, staged
admission, and no implicit network dependency.

Architecture status is not release qualification. Current V1 evidence remains
`IMPLEMENTABLE` where stated and the product remains not `QUALIFIED` and not
`DEMONSTRATED`; V2 uses those words exactly.

## Proposed independent-release trust

Component/index/core/repair trust needs explicit, separate roles and recovery:

- core, index, component, offline bundle, and repair-media signatures;
- delegated publisher/component namespaces and threshold policy;
- SBOM and attestation digests inside the signed closure;
- last-known revocation and metadata expiry for air-gapped/removable media;
- root recovery, quorum loss, emergency running-component, and break-glass;
- monotonic trust/revocation/anti-rollback state that executable rollback cannot
  reverse; and
- clean-machine no-network verification tests.

These are readiness blockers DR-103 and DR-112, not claimed settled mechanisms.

## Proposed permissions with honest outcomes

Per-operation permission resolution has two distinct records:

- authorization: `requested`, then resolved to `granted` or `denied`; and
- execution: `enforced`, `disclosed-trusted-code`, or `refused`.

Deny wins; absence denies. A manifest, repository, or publisher cannot grant
authority to itself. Every platform needs a truth table for filesystem, network,
subprocess, state, secret-handle, artifact, and other effects. Required
confinement refuses when unenforceable. Trusted-code fallback requires explicit
consent bound to exact component bytes, operation, scope, and platform; CI never
prompts and needs pre-existing policy.

Broker grants bind Request/Execution attempt, component/generation, process
instance, operation, grant, project, scope, and expiry. Revocation blocks new
broker requests, invalidates later use by the component and every descendant,
and triggers bounded cancellation/cleanup.

The host must define one durable, monotonic **revocation linearization point**
per grant generation. A broker request whose acceptance is not durably ordered
before that point is denied. An accepted but still reversible/in-flight request
is canceled and may not commit an effect after the revocation point. An
irreversible external effect whose host-owned effect-commit was durably ordered
before revocation is recorded and disclosed as completed-before-revocation; it
is not falsely reported undone. An irreversible effect not yet committed at the
point is forbidden. Components, wall-clock races, and delayed messages cannot
choose this ordering. Audit binds acceptance, effect-commit, revocation, cleanup,
and residual outcome to the grant generation, process descendant, Run/operation,
and broker request IDs.

Conformance exercises revocation before acceptance, after acceptance but before
reversible commit, racing an irreversible effect-commit, and between successive
broker calls; it proves deterministic ordering, no post-revocation commit, and
bounded cancellation/cleanup. Process death, cancellation, and teardown close
grants and handles. This is a proposed V2 mechanism at DR-105, not evidence that
any current platform enforces it.

## Preserved confinement honesty

A child process is fault containment, not a sandbox. An OS/WASM sandbox claim is
permitted only when alternate ambient access is prevented and the effective
grant is measured. Otherwise the component is disclosed trusted code in the
TCB. Host brokers used voluntarily by an unconstrained same-user process do not
create confinement.

V1 currently excludes untrusted native/WASM, probes, and network-granted
analysis by default under P-1/P-2/G3. Changing that is product decision DR-117
plus enforcement evidence, not an implication of the component model.

For MVP, OpenSIP supports first-party or explicitly trusted components with
required fault containment; third-party sandboxing is a future/post-MVP
direction, not an assumed capability or MVP gate. A process boundary is never
called a sandbox. Public marketplace, untrusted native/WASM, imperative, probe,
or network-granted components remain excluded by default. A later sandbox needs
DR-117/DR-128 product approval plus demonstrated OS/WASM confinement, permission
enforcement and platform truth tables, escape tests, revocation/incident
ownership, and honest failure/refusal behavior.

## Preserved repository-code execution default

Freeze law 11 remains in force: repository build scripts, compiler plugins/proc
macros, and analogous project-controlled execution are disabled by default.
Rust resolution may receive only the narrow reviewed grant needed for the
declared semantic tier, bound to sealed inputs and the operation; it is not a
general permission to run repository code, fetch dependencies, or widen the
read/effect set. Any successor needs explicit product/security disposition and
negative conformance evidence.
