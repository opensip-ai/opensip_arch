# 02 — Domain model

**Status:** SEALED unless noted.

The kernel vocabulary. Everything else in the system speaks this language; the
kernel itself is deliberately small — domain types, identities, errors, and wire
shapes, not a junk drawer.

---

## Core types

| Concept | Role |
|---------|------|
| `ProjectSnapshot` | Immutable manifest over content-addressed blobs: paths, hashes, VCS state, config digest, scope, environment inputs, validation method, recorded read-set |
| `FactSet` | Closed admitted `FactRecordV1` observations about a snapshot, content-addressed by host-only FACT-ID-V1 and carrying typed relation payload, universe, anchor, producer/schema/resolution/confidence provenance |
| `Finding` | A rule's evidence-backed claim, with a stable fingerprint and typed proof anchors |
| `Coverage` | What was analyzed, what was omitted, and why — per required capability |
| `Verdict` | Policy decision over findings, waivers, baselines, and required Coverage |
| `RepairPlan` | Deterministic, snapshot-bound proposed change. Non-applying by default |
| `Run` | The immutable sealed manifest linking all of the above |
| `Probe observation` | Output of an effectful stage, carrying a determinism class |

## Plane separation

**SEALED.** These are different kinds of thing and must never collapse:

```
facts  ≠  findings  ≠  verdict  ≠  telemetry
```

- **Facts** — imports, declarations, calls, manifests, test relationships.
- **Findings** — "UI depends on persistence," "this function is unreachable."
- **Verdict** — pass / fail / indeterminate under project policy.
- **Telemetry** — logs, progress, profiling. **Never evidence**, never in the digest.

The purpose of the separation is that "analysis did not complete" can never be
represented as a clean run or as a fake finding.

---

## The Run is multi-axis

*(How these axes become a process outcome is **D9**, a **candidate** contract.)*

**SEALED.** A Run outcome is not one status field. Four orthogonal axes:

| Axis | Values |
|------|--------|
| **Lifecycle** | running / completed / failed / cancelled / invalidated / abandoned |
| **Coverage** | complete / partial / unavailable, per required capability |
| **Policy verdict** | pass / fail / indeterminate |
| **Durability** | recorded / explicitly ephemeral |

Consequences:

- `advisory` belongs to finding severity, not lifecycle.
- `unavailable` belongs to Coverage, not verdict.
- **Required partial coverage can never yield `pass`.**
- A passing analysis whose authoritative commit failed is **not** a success — the
  termination contract (**D9**, **candidate**) fixes how that is reported — see
  [07-outcomes-and-failure](07-outcomes-and-failure.md).
- Read-only queries and projections do **not** create recursive Runs.

---

## Identity model

**BINDING CANDIDATE; recent identity-recipe repairs await independent
rereview.** One Run model with several identities, not competing "session" and
"execution run" APIs. The recipes below are `IMPLEMENTABLE_UNEXECUTED`; they do
not claim a built product or qualification evidence.

| Identity | Purpose | Stability |
|----------|---------|-----------|
| `RequestId` | Host-owned operational correlation for every invocation, including rejected and stored-view requests | Random per request; non-semantic |
| `ProjectId` | Host-owned logical project/storage-tenant identity, persisted outside source inputs | Random allocation preserved across an explicit move; clones fork by default |
| `ExecutionId` | Attempt/lifecycle anchor, allocated at admission before work begins | Per attempt |
| `SnapshotId` | Content identity of source and config-relevant inputs | Content-derived |
| `PlanId` | Workflow, rule/provider versions, resolved config, capability grants, budgets | Derived |
| `FactViewId` | Snapshot + derivation roots + Coverage + schema identities | Derived |
| `EvidenceDigest` | Canonical semantic output, excluding clocks and log ordering | Deterministic |

**`latest` is a resolver, never an authority.** Any resolver must return the
resolved ID it selected.

### RequestId allocation and exclusion

**BINDING, IMPLEMENTABLE; not yet qualified or demonstrated.** The host ingress
adapter allocates `RequestId` before parsing or validating any CLI/API request and
before a stored-Run lookup. Public callers do not supply it; an optional caller
token is a separate untrusted `clientCorrelationId`. The canonical form is
`req1_` plus 32 lowercase hexadecimal characters encoding 16 OS-CSPRNG bytes.
The host atomically reserves a candidate, retries a collision with a fresh
candidate, and fails operationally after eight collisions without admitting an
attempt or emitting an ordinary event under a fabricated ID.

A transport retry, new CLI invocation, or stored view is a new request and gets
a new ID. An internal retry inside one accepted host request retains its immutable
`RequestContext`. `RequestId` may correlate operational and host-audit records,
but it is excluded from `SnapshotId`, `PlanId`, fact/finding identity,
`FactViewId`, `EvidenceDigest`, evaluation proofs, `RunId`, the sealed Run
semantic manifest, Coverage, verdict, termination, cache keys, and regeneration
keys. It can therefore never turn operational correlation into evidence
authority. The retained checker mechanically joins this exclusion to the six
live closed Snapshot/Plan/C-2/fact/pure-core/D9 semantic inputs. `FactEnvelope`,
`SealedStageInput`, and `AttemptMetadata` now reject unknown fields and include
retained `RequestId` counterexamples. Generic FACT-ID-V1 is computed from the
closed admitted envelope+payload record under an exact host-only recipe; its
two-RequestId vector is recomputed rather than asserted as equal strings. Normalized
body identity remains a distinct typed payload identity. `EvidenceBundle` unknown-field closure is
still owned by the concurrent Phase-1A evidence/retention lane; an exact deferred
patch is binding as pending work, so that surface is not counted as mechanically
proven yet. Finding fingerprints, `FactViewId`, `EvidenceDigest`, `RunId`,
sealed-Run identity, and cache/regeneration keys remain normative exclusions
explicitly parked until their exact byte recipes exist; checker success does not
pretend otherwise.

CSPRNG failure, reservation I/O failure, and eight-collision exhaustion all
project through D9's existing `pre-admission-host-io-failure` context:
`faultCause=host-io`, `operational-failed`, `HOST.IO_FAILURE`, exit 4. The
internal `REQUEST_ID_ALLOCATION_FAILED` diagnostic does not extend D9's public
vocabulary. The complete lifecycle, D9, exclusion, and collision fixtures are binding in
[`operability.v10.json`](../artifacts/operability.v10.json), whose independent
pre-freeze review of exactly those bytes is PASS at zero blocking findings. v10
self-declares `CANDIDATE-NOT-APPLIED`; a passing review is not an applied
artifact. The parked-exclusion sentence above is unchanged at v10 — it is a
standing gap, not version drift.

### ProjectId allocation and custody

**BINDING, IMPLEMENTABLE_UNEXECUTED.** The host project resolver allocates 32
OS-CSPRNG bytes and persists `prj1-` plus 64 lowercase hexadecimal characters
in the exact no-follow marker `.opensip/project-id.v1`. The marker is
host-owned, untracked, excluded from snapshot enumeration, and paired with a
unique host-registry reservation. Request validation requires marker/registry
agreement before PlanIntent, storage admission, snapshot capture, or a
user-derived durable write.

A supported root move preserves identity through one atomic registry rebind
after proving the old root absent. An ordinary clone has no marker and receives
a new identity. A copied marker at two live roots is a collision, never an
implicit alias; the user must select an explicit fork or move/adopt operation.
Offline cross-machine duplication cannot be proven absent, so the host makes no
global-uniqueness claim. Exact marker bytes, lifecycle vectors, and storage/C-2
joins are binding in
[`resolved-inputs.v2.json`](../artifacts/resolved-inputs.v2.json).

Project identity diagnostics do not invent public exits. Caller/config
invalidity projects to `CONFIG.INVALID`/exit 2; malformed, unsafe, or colliding
host-owned marker/registry custody projects as `LEDGER.CORRUPT`/exit 4; entropy,
reservation, publication-I/O, or collision-exhaustion allocation failure
projects as `HOST.IO_FAILURE`/exit 4. The provenance is selected before the
internal `PROJECT_ID_*` detail.

### SnapshotId recipe

**BINDING, IMPLEMENTABLE_UNEXECUTED.** `SNAPSHOT-ID-V1` is derived only after
the host has captured and sealed the declared read set. Its text form is
`snap1:sha256:` plus 64 lowercase hexadecimal characters, and its preimage is:

```text
UTF8("opensip.snapshot-id") || 0x00 || u16be(1) || CVE1(SnapshotDescriptorV1)
```

The closed descriptor contains `schemaVersion`, verified `ProjectId`, sorted
file/symlink entries, VCS state, resolved configuration, scope, and capture
policy. Files commit exact byte length and SHA-256; symlinks commit raw target
bytes and are not followed. Paths are NFC project-relative forward-slash paths
sorted uniquely by UTF-8 bytes. The ProjectId marker is forbidden from entries,
requested paths, and the read set. Store/cache/replay/provider boundaries must
recompute both sealed bytes and `SnapshotId` before authority use; `PlanId`
field 1 is exactly that verified value.

Snapshot identity termination is likewise provenance-sensitive. Malformed
request/mutation material is `CONFIG.INVALID`; a well-formed mutation snapshot
mismatch is `REQUEST.PRECONDITION_FAILED`; persisted ledger/CAS/cache bytes that
read successfully but fail schema, digest, or equality verification are
`LEDGER.CORRUPT`; provider echoes are `PROVIDER.PROTOCOL_VIOLATION`. Failure to
read the bytes is `HOST.IO_FAILURE`, never content corruption. These reuse D9's
live causes, classes, codes, exits, and goldens without new public vocabulary.

### PlanId recipe

**BINDING, IMPLEMENTABLE_UNEXECUTED.** `PlanId` is allocated by the host Plan
builder at C-2 snapshot binding: after `ExecutionId`/AttemptRecord admission,
after the Snapshot is sealed and every keyed input is resolved, and before a
public stage executes. The host never trusts a supplied value. It recomputes the
pre-admission `planIntentCommitment`, requires that the AttemptRecord,
`ExecutionPlan.planIntentCommitment`,
`ExecutionPlan.planIdentityInputs.planIntentCommitment`, and Plan descriptor
carry the same commitment, reconstructs the
closed Plan descriptor, and verifies the supplied `PlanId` before cache lookup,
provider dispatch, or stage execution.

The recipe is exactly:

```text
SHA-256(
  UTF8("opensip.plan-id") || 0x00 || u16be(1) || u16be(13) ||
  frame(1, snapshotId) ||
  frame(2, planSchemaMajor) ||
  frame(3, release) ||
  frame(4, invocationProfile) ||
  frame(5, resolvedConfiguration) ||
  frame(6, scope) ||
  frame(7, changeSpec) ||
  frame(8, contributions) ||
  frame(9, semanticUniverses) ||
  frame(10, capabilityGrants) ||
  frame(11, workflow) ||
  frame(12, budgets) ||
  frame(13, planIntentCommitment)
)
```

Each frame is an 8-bit tag, a 32-bit big-endian value length, and one CVE1
value. CVE1 has a closed byte grammar for null, booleans, signed/unsigned
64-bit integers, NFC UTF-8 strings, arrays, and UTF-8-key-sorted maps. The text
form is `plan1:sha256:` plus 64 lowercase hexadecimal characters. Missing,
unknown, duplicate, reordered, noncanonical, or mismatched inputs are rejected;
empty collections and explicit nulls are never omitted.

The `semanticUniverses` field has provider-specific closed schemas. Its
TypeScript record independently commits the signed release/capability manifests,
the exact bundled Node/provider artifacts and identity descriptors, protocol and
provider build, Node/V8/modules ABI, TypeScript compiler/stdlib, platform, and
the resolved tsconfig/package universe. These identities name a provider
universe; they do not establish a global fact tier. Fact sufficiency remains
predicate- and relation-relative under C-1.

The Rust record independently commits the signed release/capability manifests,
exact bundled sidecar and toolchain artifacts, protocol/provider build, pinned
rustc commit and versions, host/target triples, sysroot/rustc-dev/LLVM/stdlib
digests, provider binary and notices, platform, and the exact edition/cfg/package/
feature/rustflags/crate-root universe. Execution-capable build-script and
procedural-macro outputs are present only with the exact per-project grant.
No system `rustc`, Cargo, sysroot, or `PATH` lookup may substitute for the
bundled universe. A retained full-profile vector contains both TypeScript and
Rust universes and exercises omission, substitution, and order failures.

The pre-admission `AdmissionDescriptorV1` is also closed: contributions carry
their complete versioned provenance, origin, authority, verification evidence,
parameters, and admission grant; capability grants carry their version and
project binding. AttemptRecord stores the full frozen descriptor, and
ExecutionPlan fields 3–8 and 10–12 plus the thirteen-field Plan descriptor must
equal it exactly. Snapshot binding may add the verified SnapshotId and semantic
universes; it cannot default, omit, or replace admitted authority.

In CI/non-interactive mode, layer 4 is not loaded or resolved and mere file
presence is not an admission failure. In local-interactive mode every resolved
analysis-affecting layer-4 value and its provenance enters `PlanId`. The exact
field schemas, PlanIntent recipe join, byte oracle, positive vectors, and
negative controls are binding in
[`resolved-inputs.v2.json`](../artifacts/resolved-inputs.v2.json).

### Extension identity has three layers

**SEALED.** One overloaded UUID is insufficient:

| Identity | Meaning | Stability |
|----------|---------|-----------|
| `BundleId` + artifact digest | Publisher/distribution and exact installed bytes | Publisher-stable + revision digest |
| `ContributionId` | Stable ID for a rule pack, rule, provider, scanner, probe, or profile | Rename-stable forever |
| `ActivationId` | One configured instance with parameters and grants in a project Plan | Config-generation scoped |

Human-readable slugs are **aliases, not durable keys**. Runs, baselines, waivers,
and fingerprints store stable IDs plus the observed slug for explanation. Package
coordinates are not identities.

---

## Fingerprints

**SEALED.** A finding's identity derives from a **rule-versioned recipe** over
typed subject and proof anchors, computed **host-side**:

```
fingerprint = recipe(rule-id, rule-major, subject-id, canonical-proof-anchor)
```

- Rules supply typed subjects and anchors; they never mint their own identities.
- Each fingerprint records its **stability class**: rename-stable, path-stable,
  or span-fallback.
- The recipe is versioned **independently of the fact schema**. This is the single
  most consequential versioning decision in the system, because baselines are the
  artifact whose content is **producer-derived** rather than user-authored, which
  is what makes it uniquely fragile among the several that live in user
  repositories — see
  [06-evidence-and-persistence](06-evidence-and-persistence.md).

---

## Determinism, stated precisely

**SEALED.** The naive invariant "concurrency cannot change fingerprints or
verdicts" is **false** once resource budgets exist: timeouts are load-dependent,
budget exhaustion changes Coverage, and Coverage feeds the verdict.

The correct statement:

> The `EvidenceDigest` is always a deterministic hash of a canonical sealed
> manifest. **Cross-run equality** is promised only for producers declared
> deterministic, under identical snapshot, plan, toolchain, and environment
> identities, **and an exact Coverage manifest** — not a Coverage summary enum.
> Budget or timeout exhaustion is a declared nondeterministic edge that is
> recorded with a reason code and never silently absorbed.

Canonical ordering is mandatory before hashing or projection.

---

## Kernel sizing

**SEALED (as a target).** The kernel holds domain types, identities, errors, and
wire shapes only. A "kernel" that grows to tens of thousands of lines has stopped
being one — the name asserts a role the size contradicts. Mass belongs in the
extract, fact, rule, and policy layers, not in the kernel and not in the
composition root.
