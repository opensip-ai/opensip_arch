# CODEX2 — M3-Q0 quality-harness design record r10

**Verdict: REQUIRED-FINDINGS. Two required findings.**

R10 resolves the RSS/accounting statement and the RSS-baseline mismatch. Its descriptor boundary, driver leaf evidence and subreaper settlement are substantial corrections. The prescribed mount setup cannot satisfy its own check, and absent-leaf outcomes still lack consistent evidence and elapsed settlement.

## Subjects and scope

- `docs/implementation/m3/harness/DESIGN.md`: **133762 bytes**, SHA-256 `c926077ce4403005360339d1dfab85240fb6506a3811d03d2a4c2a5d4717fee1`.
- `exploratory-quality-envelope.schema.v1.json`: **59031 bytes**, SHA-256 `6558bd39ce60f788b78c55c18e8925bee5e02823956b4a25e3f9f61e711e12a9`.

Both match REQUEST.md. Retained r9 DESIGN/schema hashes match `4db107c0…`/`00f6d032…`. The complete delta fits the r10 response table; no unrelated substantive change was found.

## C2-Q0-R10-01 — Make the mount setup satisfy its own invariant (P2)

Location: [DESIGN:803–804](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:803), calibration :855 and reference model :983.

The launcher mounts a fresh read-only leaf view **over** the inherited cgroup mount, then requires **every** `cgroup2` entry in its `mountinfo` to be read-only and leaf-rooted. Overmounting retains the covered mount as a stack parent; `mountinfo` includes stacked mounts. ([Linux mountinfo semantics](https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html))

On the ordinary delegated D12 layout, the old writable full-hierarchy mount therefore remains an entry and fails the predicate. Making mounts private prevents propagation; it does not remove that entry. This is a source-derived setup counterexample, not an executed test. The check fails closed, but the clean setup cannot produce the promised complete calibration or memory samples.

**Required change:** explicitly remove inherited cgroup mounts and aliases inside the private namespace before installing the new view, or specify and validate a sound check of reachable mount topology. The documented cgroup-namespace setup unmounts the old view before mounting the new one. ([Linux namespace setup](https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html))

Include the normal inherited writable mount as a successful setup case, while preserving rejection of reachable writable aliases and outside controls.

## C2-Q0-R10-02 — Make pre-creation failures and no-leaf settlement representable (P2)

Location: [DESIGN:792–815](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:792), :776/:822–824/:902/:922–924/:960–974; [ENV:1948–1956](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:1948) and description :5.

Two parts of the new absence/lifecycle rules conflict:

- Host checks run before step 2 creates leaves. Missing `nsdelegate` can produce `cgroup-escape-unprevented` there; the reference model expressly gives that reason “from the host checks.” The batch-start same-uid check can similarly produce `cgroup-isolation-unverified` before creation. Yet :924 declares both post-creation and ENV excludes them from `absentReason`. There is no explicit rule guaranteeing a real leaf for these failed checks.
- Elapsed now ends only when a leaf reports `populated 0` (:776/:824). Legitimate unavailable Linux and macOS slots carry absent leaves and memory-only reasons, retaining elapsed (:902/:924). A nonexistent leaf cannot satisfy that end condition.

**Required change:** define actual creation/failure ordering and truthful created-versus-absent evidence. Either ensure creation before the relevant checks when possible, or permit the applicable pre-creation absence reasons. Define no-leaf elapsed settlement through root/descendant reaping independently of cgroup interfaces, retaining bounded failure handling.

Update ENV, validator and reference cases together. Cover missing `nsdelegate` and batch-start isolation failure before creation, plus unavailable Linux and macOS with known elapsed values and absent leaves. Preserve QD-27's known samples; do not invent a leaf or erase valid elapsed to satisfy the invariant.

## R9 findings and requested checks

| Prior item | Assessment |
|---|---|
| **R9-01** descriptors/control ownership | **Partly resolved.** Closure and audit address inherited control descriptors. Read-only leaf isolation, non-dumpable outside roles and the sole-writer rule address outside access in principle. R10-01 blocks the specified clean setup. |
| **R9-02** universal RSS bound | **Resolved.** :778/:817–818/:829–833 distinguish placement from charge transfer, disclose inherited/shared/external ownership, and withdraw the RSS bound. |
| **R9-03** leaf evidence | **Partly resolved.** Driver-owned `cgroupLeaves` fixes missing operational records and the four declared absence reasons. R10-02 remains. |
| **R9-04** baseline compatibility | **Resolved.** :883–891 removes the RSS denominator, pins a reviewed charged-memory basis, and keeps absolute RSS-budget comparison informational pending D13. |
| **R9-N01** ENV citations | **Resolved.** Plain AQP and ENV correctly pin r5. The new AQP6 pointer needs N03 below. |
| **R9-N02** settlement | **Resolved for created-leaf runs.** Subreaper + reaped root + `ECHILD` + `populated 0` establishes settlement; elapsed ends there and failed settlement nulls both values. R10-02 covers the newly introduced no-leaf condition. |

The non-dumpable rule is an appropriate kernel guard **while effective**: proc descriptor access is ptrace-gated. Under ordinary credentials and a continuously non-dumpable outside process set, it blocks the stated proc path. No additional concrete false-complete case was established under that prerequisite. ([Linux proc descriptor access](https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html))

Holding the leaf directory and using relative opens preserves leaf targeting. Controller continuity also depends on sustained isolation and the stated sole-writer rule; unchanged inode/controller names alone would not detect a disable/re-enable cycle. The test-hook case can enforce the sole-writer violation rather than claim endpoint checks detect it.

Static schema inspection found **41 closed object schemas**, integer-only numeric fields and no unresolved local references. The created/absent `oneOf` is internally consistent. New `cgroup-isolation-unverified` nulls memory only; failed run/timeout/settlement null both; missing operational evidence keeps known values. Any reason remains `incomplete` and excluded from Q6. RS3 is unchanged, and qualification equivalence remains with D13.

## Non-blocking observations

- **C2-Q0-R10-N01 — Continuous non-dumpability (:806/:820).** Define the outside harness/driver process set and preserve the prerequisite throughout the run. Ordinary exec resets dumpability before the new image runs; restoring it afterward or polling leaves a window. Prohibit such outside transitions during measurement or use independent access isolation. This clarifies the stated invariant; no permitted outside exec was identified as another required counterexample. ([Linux 6.1 exec implementation, :1271–1276](https://raw.githubusercontent.com/torvalds/linux/v6.1/fs/exec.c))
- **C2-Q0-R10-N02 — Audit descriptor (:805).** Listing `/proc/self/fd` opens its own directory FD. Exclude only that identified temporary FD and close it before exec, or audit from the parent. The final inherited set remains exactly the three pipes. ([Linux close_range example](https://man7.org/linux/man-pages/man2/close_range.2.html))
- **C2-Q0-R10-N03 — AQP6 pin (:39).** Live accepted `PLAN.md` now has SHA-256 `1611014d4b8b71e3c3ce28274d6423114d0a2f54ae3a72990f7476c2ca043480` and a two-line acceptance-note shift. `PLAN-r6.md` matches the stated `8aed6eb8…` hash and intended line numbers. Point AQP6 at that snapshot.
- **C2-Q0-R10-N04 — Complete-row baseline predicate (:883–891/:927).** Explicitly compare reset/cache/charge-ownership policy and kernel as well as metric, runner class and entry method. Qualify “otherwise no-baseline” to complete rows; any slot reason retains `incomplete` precedence (:907/:931 and the fixed schema variant).

## Verification

Read-only full DESIGN/schema comparison, hash/size and citation checks, static carrier/validator inspection, three independent challenge slices and primary Linux documentation/source inspection. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run; no runtime home was accessed; no commit was created. Writes are limited to REVIEW.md and review.json in the requested r10 directory.
