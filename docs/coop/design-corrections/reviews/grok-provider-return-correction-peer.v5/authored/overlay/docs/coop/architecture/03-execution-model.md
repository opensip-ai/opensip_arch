# 03 — Execution model

**Status:** SEALED unless noted. Resiliency specifics are CANDIDATE (D10).

How a run happens, from a live worktree to a sealed Run.

---

## Canonical flow

```text
live project + resolved intent
  → Snapshotter        [O(changed) content work; read-set recorded]
  → Planner            [typed derivation DAG + capability/resource grants]
  → Extractors         [syntax facts: per file, content-addressed]
     └─ Semantic providers  [one Program per semantic universe
                             → resolved/type facts w/ confidence]
  → Probes             [EXCLUDED FROM V1; ARCH.PROBE-CONTRACT must supply a
                        restricted runtime before this stage can be admitted]
  → Rules              [v1 declarative only; linked bundled algorithms are TCB;
                        third-party/untrusted imperative rules are excluded]
  → Policy             [waivers, baselines, required-Coverage gate]
  → seal RunManifest + EvidenceDigest
  → RepairPlan?        [deterministic, snapshot-bound, non-applying]
  → typed query services → CLI / TUI / MCP / SARIF / HTML / Cloud export
```

Single write authority. Single timing authority. Single scope expansion. Single
graph generation identity per build.

---

## Snapshot capture

**SEALED.** Producers read **host-owned immutable snapshot bytes or a read-only
VFS** — never a live worktree that can mutate mid-run. Enumerating and hashing a
live tree does not make it immutable.

### Cost model

**SEALED.** Snapshot capture must not be O(repo) per invocation, or the agent
loop — the product's stated wedge — becomes its slowest path.

```text
cold embedded:            O(inventory metadata) + O(changed bytes hashed/materialised)
warm engine w/ journal:   ≈ O(changed · log N)
```

Mechanism: a **stat-cache-validated Merkle manifest** with lazy content-addressed
materialisation — the git-index / Bazel model. Content is hashed only on stat
mismatch; blobs enter CAS only when a producer actually reads them.

**O(changed) is a warm-path objective, not an unconditional guarantee.** A cold
one-shot process must still discover inventory unless it has a trustworthy VCS or
fsmonitor journal.

### Validation integrity

**SEALED.** The stat tuple needs racy-timestamp protection: device/inode, ctime,
mtime, size, filesystem timestamp resolution, and conservative re-hash inside the
race window. A final or CI profile may require full content verification. The
`SnapshotManifest` **records its validation method and assurance level**, and
required weak validation can never silently claim an authoritative pass.

### Mid-run mutation

**SEALED.** Under the product's own thesis — agents continuously editing, plus
watch mode and format-on-save — mid-run mutation is the **steady state**, not an
edge case. An honest terminal status that fires constantly is a usability
failure, so:

1. The manifest records the **read-set**; mutation of files the run never read
   does not invalidate it.
2. Bounded automatic **re-snapshot and retry**, then terminal `invalidated`.
3. Retry counts are **execution metadata** — never part of the EvidenceDigest.
4. Exhausted convergence is **`indeterminate`**, not an operational failure:
   nothing malfunctioned, the input was unstable.

---

## Planning and derivation keys

**SEALED.** The planner builds a typed derivation DAG from the workflow plus each
rule's declared requirements, and allocates capability and resource grants.

Cache identity must be **provenance-complete**. Content hashes alone are
necessary but insufficient:

```text
DerivationKey = H(snapshot partitions, producer + schema + config,
                  semantic-universe roots, required coverage)
RuleKey       = H(rule + config, required fact-partition roots,
                  graph/index algorithm versions, coverage)
```

**The subtle case is negative queries.** A dead-code rule depends on the *absence*
of references, so hashing only the rows a rule consumed would fail to invalidate
when a new reference appears. Cache against declared relation and scope Merkle
roots plus Coverage — not just positive rows. Dynamically discovered dependencies
may be recorded for diagnostics, but the sound pre-run key is the declared
partition root.

This is the difference between content-addressed caching and unsound memoization.

---

**CANDIDATE (RESOLVED-INPUTS).** ~~Contract-complete, unreviewed.~~ Binding artifact:
[`resolved-inputs.v2.json`](../artifacts/resolved-inputs.v2.json).

**Corrected 2026-08-04 — "unreviewed" is withdrawn.** These bytes have been
independently reviewed; as recorded on that date, blueprint §1.1 carries
RESOLVED-INPUTS as **PASSED with changes**. The binding-artifact pointer above is
unaffected and still current. Do not copy the verdict out of this sentence: review
state is not maintained in this file, and freeze §3 and blueprint §1.1 are the
authorities for it.

## The ambient-input closure

Determinism does not follow from recording the environment. **Recording is not
neutralising** — and an earlier draft recorded an environment identity and stopped
there, which left locale, collation, filesystem enumeration order, path form, clock
and entropy free to reach a result.

Recording an input buys *reproducibility by identity*: a different locale yields a
different PlanId, so at least there is no false cache hit. It costs *portability*:
two machines can then never share a cache entry. And recording the inputs nobody
thought of buys nothing at all.

So every ambient input the process can observe is assigned to exactly one of three
classes. **Neutralise when you can, key when you must, forbid when neither.**

| Class | Rule | Examples |
|---|---|---|
| **Neutralised** | host forces a canonical value; **must not** enter PlanId — keying a constant is churn carrying no information | locale → `C`, TZ → `UTC`, collation → byte-wise, enumeration → sorted, paths → normalised NFC, fixed hash seed |
| **Keyed** | genuinely analysis-affecting; **always** enters PlanId with per-field provenance | semantic universe keys, allowlisted env, the execution-capable grant, the ChangeSpec |
| **Forbidden** | must never be read on the analysis path; a read is a host defect | wall clock, entropy, network state, hostname/uid, unallowlisted env, anything under `$HOME` outside the declared config path |

Keying locale would make every cache entry machine-local and every cross-machine
comparison a false miss — while still doing nothing to stop a rule folding a hash map
in a nondeterministic order. **Keying records that machines differ; it does not make
them agree.**

The classification must be **total**: an input in none of the three classes is a
defect, not a default. The declared inventory is necessarily incomplete, and the
checker is honest about that bound — it verifies every *listed* input is classified
exactly once, and cannot discover one nobody listed.

Two consequences worth naming. Collation and enumeration order are neutralised
because **subject-set ordering is load-bearing**: the no-match commitment in
[06](06-evidence-and-persistence.md) is a *sorted*-leaf Merkle root, so a machine
that sorts differently computes a different root over identical facts. And actually
*denying* a forbidden read is unimplementable today — it needs the same capability
substrate `ARCH.PROBE-CONTRACT` is reopened over. The closure specifies intent that
nothing yet enforces, and says so.

---

## Resiliency

**CANDIDATE (D10).** Sealed fragments plus a candidate structure:

- **Cancellation:** one cancellation tree per `ExecutionId`. A whole-Run deadline
  bounds stage deadlines; cancellation propagates into extractors, semantic
  providers, scanners, WASM, and process groups. Graceful deadline, then hard
  kill. Orphan reaping is mandatory.
- **Retry:** only operations declared idempotent for the same Snapshot and Plan.
  Snapshot convergence retry is bounded. **Probes are never implicitly retried.**
- **Partial output:** admitted only when a complete, checksummed partition
  manifest was sealed. **A truncated stream is a fault, not partial evidence** —
  this is the discriminator between `indeterminate` and `operational-failed`.
- **Storage faults:** SQLite busy, CAS write failure, disk-full — **fail closed**
  with a typed error. Never a partially corrupt Run.
- **Chaos gates** prove the above in the vertical prototype.

## Concurrency

**SEALED.** Multiple concurrent processes in one checkout is the normal case —
two agent sessions, a watch, and CI can share a working tree.

- **Any** host that writes evidence must be multi-process safe on its own: WAL,
  busy-timeout, idempotent run insertion, CAS write-then-atomically-link, and
  defined stale-lease recovery. This obligation is on the storage protocol, not
  on a particular deployment.
- **Warm state is an acceleration, never an evidence authority.** A host holding
  cached inventory, semantic state, or indexes may not produce a Run that a cold
  host could not produce identically from the same Snapshot and Plan.
- All hosts use the **same transaction and CAS protocol**. There is no
  "engine-only" write path.

**CANDIDATE FOR FREEZE (R-1 SEAL-WITH-CHANGES recommendation).** The v1 process
topology is one-shot orchestration host plus a pure, data-only evaluation core.
Resident execution, autostart, resident-default UX, and per-project or
multi-project residency are parked outside v1. They may be reconsidered only
after workload measurement and an explicit product scope change; they are not
alternate implementation paths. The storage-protocol obligation above is
independent of that future decision. See [08](08-surfaces-and-topology.md) and
the coordinator closure artifact.

---

## Invariants shipped from commit one

**SEALED.**

1. Required partial coverage cannot yield `pass`.
2. Analyzers cannot mutate the source tree; apply is a separate capability
   followed by a verification Run.
3. Network is denied unless the workflow grants it.
4. Every result is bound to snapshot, config, and rule/provider identities.
5. The EvidenceDigest is deterministic given identical Coverage and declared
   determinism classes; nondeterministic edges are documented, not hidden.
6. Plugins cannot invent CLI or persistence surfaces.
7. A process boundary is never described as a security sandbox.
8. Cached facts are reusable only on full input-identity match.
9. MCP and reports use the application query API, never raw persistence.
10. The analysis kernel never imports Cloud.
11. One Run identity; `latest` returns a resolved ID.
