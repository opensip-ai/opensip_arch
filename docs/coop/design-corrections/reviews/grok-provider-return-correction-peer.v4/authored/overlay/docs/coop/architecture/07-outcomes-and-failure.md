# 07 — Outcomes and failure

**Status:** CANDIDATE, independently reviewed at head, not applied.
`d9-exit-contract.v1.14.json` is the **binding** artifact: the demotion recorded
here previously was correct for a reference document and wrong for an
implementation target, because goldens and vocabularies are exactly what a team
needs in week one. The independent pre-freeze review of exactly those bytes is
PASS at zero blocking findings, with two advisories (`R-V114-F1`, `R-V114-F2`)
tabled as verifier residuals. v1.14 carries 45 goldens exercising every declared
cause value, a stated cause model, and cross-axis invariants verified against
every golden before adoption; its own delta over the prior version is API and
coherence only — cause values are enum-closed and `hostTerminationUnion.details`
carries an explicit no-authority disposition, and every golden, core-completion
row and reduction rederives identically.

`check-d9-v1.14.py` is a gate, not a coherence note: it verifies 25 pins before
retained execution, and `--selftest` rejects a mutation suite in isolated child
interpreters. It is also where the total axes-to-class function actually lives —
the head JSON names a `referenceDerivation` rather than stating the function, so
the oracle is obtained by **executing** the checker, never by reading a lower
version of the contract.

It is **not sealed and not applied.** v1.14 self-declares
`CANDIDATE-NOT-APPLIED`; a passing review is not an applied artifact. Three
contract gaps remain carried by the checker's `referenceDerivation` rather than
by the JSON — observation-to-`faultCause` selection, optional-field presence
policy, and the `success`/`policy-failed`/`interrupted` branch — and closing them
in the D9 JSON is a successor's job. One live divergence is recorded rather than
papered over: `rust-provider-protocol.v4#d9JoinV4` and `evidence.v10` both pin the
prior version `d9-exit-contract.v1.13`, one behind this head. The v1.14 review
re-derived all 45 goldens identically under both, so the divergence is in the pin
and not in the semantics — but a join pinned one version back does not carry
v1.14's closed cause enums. Implement the join against this head and escalate the
stale pin; do not repair it by editing a reviewed artifact.

How a command terminates, what the machine sees, and what may never be confused
with what.

---

## Why this needs its own contract

Termination is the **only output with no redundancy**. A wrong finding is visible
in the report; a wrong exit code is invisible in every projection — the JSON
looks right, the report looks right, and CI silently does the wrong thing. It is
also the output CI depends on most and inspects least.

It is additionally the natural sink for **axis conflation**. Analyzer faults,
missing coverage, advisory findings, and policy failure all want to become "the
command failed," and once they share one representation the distinctions are
unrecoverable. The multi-axis Run model ([02](02-domain-model.md)) exists to keep
them apart; this contract is where that separation either holds or collapses.

*Empirical support from the shipping product — how expensive this gets without a
single owner — is recorded in `../steering/01-current-state-evidence.md`.*

---

## Public output is a discriminated envelope

**CANDIDATE.** One run-shaped document cannot represent reads, mutations,
long-lived servers, or failures that occur before Run admission.

```text
CommandEnvelope =
  RunResult       { kind: "run",      run: RunProjection }
| QueryResult     { kind: "query",    query, data, page?, coverage? }
| MutationReceipt { kind: "mutation", operation, before?, after?, verificationRunId? }
| FailureResult   { kind: "failure",  executionId?, errors[] }
```

Rules:

- Common header: schema **family and major**, command/request ID, project
  identity when resolved, bounded diagnostics.
- `FailureResult` is the **most stable member** — it is what CI and agents hit
  when everything else is broken — and must be **constructible before project
  resolution**, so it cannot require project identity.
- Consumers must be able to **pin a schema major** and receive a typed refusal
  rather than a silently reshaped document. A silent reshape is the same hazard
  class as baseline invalidation, on a different contract.
- Exact Coverage and large artifacts are **content-addressed references**;
  projections carry summaries and IDs.
- Filtering, pagination, and `top` are projection metadata and never alter the
  sealed Run.
- stdout carries exactly one machine document (or a declared JSONL protocol).
  Progress and logs never go to stdout.
- The agent surface reuses the same **domain bodies**, not a CLI JSON string wrapper.
- SARIF preserves the canonical OpenSIP Run/Finding IDs, Coverage, verdict,
  truncation, and artifact references in typed SARIF fields or namespaced property
  bags. A viewer may hide extension properties, but the serialized interchange is
  not permitted to discard them; human/agent projections provide the visible
  fallback.
- The envelope declares a **schema family and major**; consumers negotiate.
  A version number alone, without a family, is ambiguous.

---

## Termination is one total union

**CANDIDATE.** The naive formula `exit = f(lifecycle, coverage,
verdict)` is **not total**: those axes do not exist before admission, or for
queries, mutations, and servers — and it omits the **durability** axis.

The input is a six-variant `HostTermination` union. Admitted analysis *derives*
it from lifecycle + required Coverage + verdict + durability + interruption +
required postconditions; other command kinds derive the same union from their
domain result. Only then does one table map it to a numeric code.

| Class | Code | Meaning |
|-------|------|---------|
| `success` | 0 | Operation completed; analysis passed or was advisory |
| `policy-failed` | 1 | Valid, sufficiently covered analysis; project policy failed |
| `request-rejected` | 2 | Usage, config, admission, compatibility, addressed-identity, or mutation-precondition rejection |
| `indeterminate` | 3 | Honest terminal result, but required evidence or convergence was unavailable |
| `operational-failed` | 4 | Host, provider, protocol, integrity, durability, required-delivery, or serialization failure |
| `interrupted` | 130 | User interrupted; cooperative cleanup ran where possible |

### Settled classifications

| Case | Class | Rationale |
|------|-------|-----------|
| Snapshot convergence exhausted | `indeterminate` (3) | Nothing malfunctioned; the input was unstable. Under agent editing this fires routinely, and 4 would page a human every time |
| Addressed identity missing | `request-rejected` (2) | 404, not a failure |
| Empty collection query | `success` (0) | Absence is data when the query is set-valued |
| Unsupported fingerprint recipe | `indeterminate` (3) | Encodes the baseline safety property — never mass net-new |
| Optional egress failed | `success` (0) | Export can never change a local verdict |
| Explicitly required delivery failed | `operational-failed` (4) | Requiredness is a project decision |
| Ephemeral run where caller required authority | `request-rejected` (2) | Unsatisfiable by construction |
| Cooperative `serve` stop | `success` (0) | Ctrl-C is the normal way to stop a daemon; 130 reads as failure to supervisors |
| `latest` resolver on empty domain | `request-rejected` (2) | An addressed identity that cannot be resolved |
| Ledger busy past retry budget | `operational-failed` (4) | Distinguish contention from corruption — the remedy differs |

### The hardest boundary

`indeterminate` vs `operational-failed` turns on **whether the host can seal a
coherent Run**. A required provider that is unavailable but whose absence the host
can record as Coverage is `indeterminate`; a **truncated or invalid provider
stream** that prevents sealing is `operational-failed`.

---

## Invariants

**CANDIDATE.**

1. Only the host finalizer constructs a termination. Producers return domain
   results, Coverage reasons, observations, or typed faults — **never numeric
   exits**.
2. One process-boundary map and **one controllable exit write site**.
3. A successfully emitted envelope carries the **same** termination class and code
   as the process.
4. `FailureResult` is constructible without project or Run identity.
5. **A policy verdict never becomes an Error; an operational failure never becomes
   a Finding.**
6. Optional export failure cannot alter a local verdict.
7. **A durability failure cannot report success** for an authoritative Run, even
   when the analysis verdict is pass.
8. Signal handlers request cancellation; they contain no independent exit mapper.
9. Interruption during authoritative publication must leave the ledger
   **recoverable** — recovery marks the orphan `abandoned`, never sealed.
10. Finalization is linearized: a signal arriving after semantic completion cannot
    nondeterministically replace a settled outcome.
11. SIGKILL and failures preventing all finalization are outside the controllable
    contract.

## Diagnostics that must not become findings

**SEALED.** Reason codes distinguish remedies, and conflating them destroys the
agent's next action:

- `indeterminate` reason codes must separate **convergence-exhausted** from
  **required-coverage-missing** — the remedies are retry versus widen scope or
  install a provider.
- Addressed-identity errors must separate **expired/retention-collected** from
  **never-existed**, and claiming expiry requires tombstone evidence.
- A run that exits 4 with `verdict: pass` must render legibly, or required-delivery
  failure reads as a false failure. Verdict and termination are **distinct
  fields**, never one status line.

## Remaining work before seal

1. ~~Goldens are owed for `COVERAGE.LANGUAGE_TIER_UNSUPPORTED`,
   `COVERAGE.BUDGET_EXHAUSTED` and `CAS.LINK_FAILED`.~~ **Discharged at the
   head**: `d9-exit-contract.v1.14.json` exercises all three across
   `analysis-language-tier-unsupported`, `analysis-budget-exhausted`,
   `analysis-multiple-deficiencies` and `analysis-cas-link-failed`. What is
   genuinely still owed is the three contract gaps the head leaves to the
   checker's `referenceDerivation` rather than to the JSON, named above.
2. The baseline case must encode the **prohibited effect** — exit 3 alone does not
   prevent an implementation emitting mass comparison-derived findings. Required:
   zero derived findings, no comparison performed, repair metadata present.
3. Executable mapper goldens, not table lookups.
4. `sealedPropertiesCovered` traceability — see
   [10-method](10-method.md).
