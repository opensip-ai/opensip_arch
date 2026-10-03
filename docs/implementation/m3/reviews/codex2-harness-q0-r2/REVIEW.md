# CODEX2 review — M3-Q0 r2

**Verdict: REQUIRED-FINDINGS.** Six r1 findings are resolved and two are partially resolved. Three required findings remain, including one new schedule arithmetic error.

Reviewed subjects:

- `docs/implementation/m3/harness/DESIGN.md`: 91,319 bytes; SHA-256 `4225ca34728ba1494a087110c5b92664f7d3f1560dc5ce3dd70fa24cf91e63c4`.
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`: 50,098 bytes; SHA-256 `df67c65128065c33867ad3317a1cf25f870a0b4670c06a8af4336ab00de9548f`.

Both match REQUEST.md. The retained r1 subjects also match their recorded hashes. Locations below refer to these reviewed files; ENV means the schema.

## R1 finding resolution

| R1 finding | Resolution | Evidence and remaining work |
|---|---|---|
| C2-Q0-R1-01 — TRI soundness | **RESOLVED** | DESIGN:242–260 includes the full path/mode/content snapshot and resolution inputs, including added/deleted candidates. No narrower closure is admitted without independently reviewed soundness. Input triggers are separate from detector outputs. |
| C2-Q0-R1-02 — advisory allocation | **RESOLVED** | DESIGN:490–495 reaches the per-stratum, per-evidence-set floor by water-filling. The former counterexample now draws 72 + 28 = 100. Uniform selection and sampled denominators are explicit. |
| C2-Q0-R1-03 — sample versus census guard | **RESOLVED** | DESIGN:264–274,453–471 distinguishes populations and uses verified true/corpus count for admission. Unlabelled findings cannot produce PASS from a sample ratio. OI-17 is not adopted. |
| C2-Q0-R1-04 — repository-controlled execution | **RESOLVED** | DESIGN:533,555–560 enforces M3's prohibition, verifies non-executing modes and defers executing tools to explicit M5 authorization. Confinement supplies no permission. |
| C2-Q0-R1-05 — lifetime RSS accounting | **PARTIALLY RESOLVED** | DESIGN:681–709 identifies a Linux own-address-space counter and conservatively marks missing/platform-unavailable counters incomplete. Historical inventory completeness and terminal thread-group selection still need R2-01. |
| C2-Q0-R1-06 — missing denominators | **RESOLVED** | ENV:845–929,947–999,1233–1256,1555–1573 carries repository populations/line counts, yield denominators and per-rule Q7 populations/histograms/dispositions. Measured Q7 requires nonempty rows at ENV:1637–1657. |
| C2-Q0-R1-07 — incomplete results and retry identity | **PARTIALLY RESOLVED** | DESIGN:729–743 and ENV's complete/incomplete variants supply nullable samples, typed reasons, non-Q6 status, batch identity and final selection. Batch-scoped record/observation joins remain missing: R2-02. |
| C2-Q0-R1-08 — oracle freeze scheduling | **RESOLVED** | DESIGN:839–865 supplies reviewed, enforced freezes before T1 producer runs, ten pre-day-zero days and TS completion at day six. OI-12 lists pending plan edits. The new slip calculation is a separate error: R2-03. |

The five r1 non-blocking observations were also checked. N01's estimand and CP premise, N03's withdrawn simulation claim, and N05's citations/restricted Rust domain are resolved. N02's numerical references and all-success qualification are corrected, but its error wording needs R2-N01. N04's trigger separation, rater slots and permanent exposure tracking are supplied; runner fields exist, but their batch scope needs R2-02.

## Required findings

### C2-Q0-R2-01 — Complete lifetime RSS needs a loss-aware terminal protocol (P1)

**Location:** DESIGN:689–696. **Relation:** remaining part of C2-Q0-R1-05.

At line 694, completeness follows from `populated 0` and collected exits for every **registered** lifetime. That does not establish that every historical descendant was registered. A short-lived child can allocate a peak and disappear between inventory reads while its connector and accounting messages are lost. All known exits can then be collected and the cgroup empty, with the missing child absent from the sum.

This is a real property of the chosen interfaces: `cgroup.procs` excludes zombies and `populated` describes live processes; taskstats documents CPU-scoped subscriptions and receive-buffer loss. Connector sends can fail. Empty snapshots cannot recover lost history. [Cgroup documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html), [taskstats documentation](https://docs.kernel.org/accounting/taskstats.html), [Linux connector source](https://raw.githubusercontent.com/torvalds/linux/v6.18/drivers/connector/cn_proc.c).

There is also no explicit process-terminal selection rule. Taskstats emits per-task records on individual thread exits, whereas DESIGN deduplicates lifetimes by tgid. An early-exiting leader can report a smaller peak before a worker raises the shared address-space peak. Keeping the first record for that tgid is insufficient; summing thread counters duplicates an address space. The pinned Linux source marks the final per-task record with `AGROUP` and carries `ac_tgid`; the design should specify the chosen terminal record and its identity join. [Linux taskstats source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/taskstats.c).

**Required change:** specify acknowledged pre-launch subscriptions covering every permitted CPU, loss/continuity checks, stable identity acquisition and terminal draining/completion. Overflow, sequence gaps, subscription failures, unknown/unjoinable identities or missing terminal counters must force `incomplete`. Define final thread-group record selection and deduplication for the pinned kernel. Extend the planned K1c calibration/rejection cases to include short-lived processes, a leader exiting before a worker, and event loss. No calibration was run during this review.

The counter itself is credible: Linux `hiwater_rss` reads the task's own address-space high-water mark and reports KiB. The remaining defect concerns complete collection and selection, not absence of a counter. [Linux extended-accounting source](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/tsacct.c).

### C2-Q0-R2-02 — Operational records and runner observations need a batch join (P1)

**Location:** DESIGN:740–742,761; ENV:459–501,573–601. **Relation:** remaining part of C2-Q0-R1-07, also affecting r1 N04.

Both initial and retry batches must live in one envelope. Q6 rows now have batch IDs, but `operationalRecords` still identifies only `workloadId` and `runIndex`, plus a digest and disclosure flag. Those indexes recur across workflow/reset/control cells and retries. A record digest identifies bytes; no declared lookup binds those bytes to the corresponding Q6 batch.

Likewise, DESIGN:761 requires observations for **each batch**, while `runner.observations` is a single closed object. Two retained batches with different pre-batch load averages cannot carry both observations through that field.

For example, both batches contain run index 0 of the same workload, with different phase/reuse records and load averages. The envelope has distinct Q6 batch IDs but no explicit association for either supporting carrier. Reviewers cannot reconstruct first/final batch evidence or validate quiet-run admission.

**Required change:** add a required batch-ID join to operational-record rows with explicit run-slot semantics, or ordered record references within each batch. Carry runner observations as batch-keyed rows or required batch references. Assign canonical-ID, join, duplicate/orphan and required-coverage checks to the envelope validator. Missing evidence must use the defined incomplete/absence state.

### C2-Q0-R2-03 — K2 slip slack omits F1 → H → J2 (P2)

**Location:** DESIGN:856–857,859–865; M3-PLAN:213,218–227. **Relation:** new r2 error; the original baseline freeze defect is resolved.

The four-day slack assertion compares F2's day-14 finish with the original J3 day-18 start while holding H and J2 fixed. H also depends on F1. Under the design's stated model that delaying first T1 activity shifts the F branch, let `d` be the actual F1 delay:

```text
F1 = 10 + d; F2 = 14 + d; F3 = 17 + d
H  = max(12, 10 + d) + 3
J2 = H + 3
J3 = max(J2, 14 + d, 15) + 3
```

Applying the remaining plan dependencies gives:

| Actual F1 delay | F1 | H | J2 | J3 | M3-M | M3-X |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 10 | 15 | 18 | 21 | 24 | 26 |
| 2 | 12 | 15 | 18 | 21 | 24 | 26 |
| 3 | 13 | 16 | 19 | 22 | 25 | 27 |
| 4 | 14 | 17 | 20 | 23 | 26 | 28 |

Other stated branch/day-zero assumptions hold, including `O2_selected ≤ 24`. Thus `M3-X = 26 + max(0, d - 2)`: only two days of actual F1 delay fit. If oracle slip `s` is measured from the planned day-six freeze, the stated one-day margin gives `d = max(0, s - 1)`; three days of oracle slip fit, and the fourth extends the chain.

**Required change:** replace the four-day assertion with dependency-aware formulas and incorporate the corrected consequences into OI-12. If authoring can proceed independently of delayed T1 execution, explicitly model that schedule and recalculate its dependencies. The current prose already asserts whole-branch shifts, so its slack must be computed consistently with that model.

## Non-blocking observations

1. **C2-Q0-R2-N01 — Error wording is too strong (DESIGN:451,501).** An error need not increase the family count under the product method. At 299 families, 298 precisions of 1 and one of 999999/1000000 yield `L ≥ 0.990030 × 0.999999 = 0.99002900997 > 0.99`. With full adjudication, the pooled guard also passes. Restrict the error-free requirement and the one-error/473-family statement to the single-finding CP branch. The formal product decision is correct.

2. **C2-Q0-R2-N02 — OI-17 does not guarantee the stated cost reduction (DESIGN:469,503).** Current water-filling draws all 116 findings from 29 families of four. Even a forced 100-finding sample need not establish the proposed α/29 hypergeometric guard: for an incompletely sampled four-finding family, all sampled labels can be true with probability at least 1/4 despite one hidden false label, far above 0.05/29. Approval alone does not establish sufficiency. Keep the current approximately 260-vote estimate and qualify or withdraw the prospective 224-vote estimate. OI-17 remains unadopted, so this does not invalidate the current guard.

3. **C2-Q0-R2-N03 — “Exactly when” should be “guaranteed when” (DESIGN:380).** At least 100 families guarantees one sampled finding per family; fewer than 100 singleton families also receive one each. The formal branch condition at lines 375–376 is correct.

4. **C2-Q0-R2-N04 — Specify sample/reason consistency (ENV:1495–1526; DESIGN:729–742).** Null sample slots with seven empty reason lists are structurally admissible. Assign unavailable-slot/reason consistency and phase/aggregate availability checks to the schema or envelope validator. This does not admit a within-budget result: incomplete status and `q6Labelled: false` are enforced.

## Requested method checks and open items

- **Water-filling:** sound. The smallest cap reaches `min(100, ΣN_j)`; any overshoot is less than the family count. Uniform within-family sampling and recorded `N_j/a_j` preserve the stated product-bound argument.
- **Two-sided guard:** sound. `T/N` is a deterministic lower bound and `(T+U)/N` an upper bound on pooled precision. FAIL uses the upper bound; PASS requires the lower bound and confidence bound. No unverified finding can improve the lower bound.
- **Linux mechanism:** a credible counter source with incomplete-platform/missing-counter handling, but R2-01 is required before complete accounting can be claimed.
- **Schema rejection cases:** static inspection confirms rejection of missing required denominators, measured Q7 without nonempty rule rows, within results with null RSS samples, incomplete results marked Q6-labelled, and unknown run reasons. Batch evidence remains R2-02; absence consistency is N04. Cross-row final selection/population arithmetic is explicitly assigned to the semantic validator. No validator was run.
- **K2 schedule:** the baseline freeze ordering is coherent and resolves r1; slip arithmetic needs R2-03.

OI-17's pending inference rule and OI-18's explicit macOS incomplete boundary are appropriately disclosed. Neither open status alone requires a finding. A macOS qualification lane still needs an own-counter source. OI-12 clearly lists pending M3-PLAN edits; those edits must include the corrected slack, but the plan need not be edited before this design review is accepted.

Review method: static reading of the r2 subjects, retained r1 subjects/review, governing local design references and primary Linux documentation/source, with analytic allocation/bound/schedule checks. No product code, tests, builds, corpus fetches, benchmarks or runtime-home access; no commits. Only the requested two review artifacts were written.
