# M3-Q0 quality-harness design record — r11

Draft r11. Claude Opus 5.5, implementation lead. Unit **M3-Q0** of the accepted M3 unit plan (`M3-PLAN.md:157`).

r1 (`DESIGN-r1.md`, sha256 `22df1afb…`, 65,990 bytes; schema `exploratory-quality-envelope.schema.v1-r1.json`, `4cdfbb60…`, 23,190 bytes) was reviewed by CODEX2 (method; `/tmp/opensip-implementation/reviews/codex2-harness-q0-r1/`), with 8 required findings and 5 non-blocking observations. r2 answers all of them. CODEX2 confirmed the cluster-product bound and the 29/299 floors as sound, so they are unchanged.

r2 (`DESIGN-r2.md`, sha256 `4225ca34…`, 91,319 bytes; schema `exploratory-quality-envelope.schema.v1-r2.json`, `df67c651…`, 50,098 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r2/`). Six r1 findings were resolved and two partly resolved, with 3 required findings and 4 non-blocking observations. r3 answers all of them and changes nothing else of substance.

r3 (`DESIGN-r3.md`, sha256 `b69c918f…`, 101,902 bytes; schema `exploratory-quality-envelope.schema.v1-r3.json`, `f38b3f20…`, 52,882 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r3/`), with 2 required findings and 2 non-blocking observations. r4 answers them and changes nothing else.

r4 (`DESIGN-r4.md`, sha256 `f7afe275…`, 107,617 bytes; schema `exploratory-quality-envelope.schema.v1-r4.json`, `b6c7d8ae…`, 53,642 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r4/`), with one required finding. r5 answers it and changes nothing else.

r5 (`DESIGN-r5.md`, sha256 `d922f5bd…`, 111,807 bytes; schema `exploratory-quality-envelope.schema.v1-r5.json`, `3f79b979…`, 53,696 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r5/`), with one required finding and one non-blocking observation. r6 answers both and changes nothing else.

r6 (`DESIGN-r6.md`, sha256 `3a17a943…`, 118,963 bytes; schema `exploratory-quality-envelope.schema.v1-r6.json`, `da73a476…`, 53,696 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r6/`), with one required finding and two non-blocking observations. r7 answers them, and records a simpler alternative as OI-19.

r7 (`DESIGN-r7.md`, sha256 `c72f71ba…`, 124,649 bytes; schema `exploratory-quality-envelope.schema.v1-r7.json`, `1afd2709…`, 53,752 bytes) closed C2-Q0-R6-01 and proposed OI-19. The lead then **decided to adopt OI-19**. r8 implements that decision and changes nothing else.

r8 (`DESIGN-r8.md`, sha256 `c958fdab…`, 120,918 bytes; schema `exploratory-quality-envelope.schema.v1-r8.json`, `cc6f3cb8…`, 57,369 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r8/`), with 5 required findings (R8-01 to R8-05). The lead then **decided to stop per-process attribution** and amended the quality plan to r5 (§5.1, AQP:331-338). r9 implements that decision.

r9 (`DESIGN-r9.md`, sha256 `4db107c0…`, 120,794 bytes; schema `exploratory-quality-envelope.schema.v1-r9.json`, `00f6d032…`, 53,610 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r9/`), with 4 required findings and 2 non-blocking observations. r10 answers all of them and changes nothing else.

r10 (`DESIGN-r10.md`, sha256 `c926077c…`, 133,762 bytes; schema `exploratory-quality-envelope.schema.v1-r10.json`, `6558bd39…`, 59,031 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r10/`), with 2 required findings and 4 non-blocking observations. r11 answers all of them and changes nothing else.

## Standing

**This is a design record, not law and not a contract successor.** It changes no accepted contract, schema, gate, threshold or register row. It fixes the harness mechanisms that the accepted analysis-quality plan leaves to "the harness design" (AQP:237, AQP:489), so that K1, K2, I2, S-M and M3-M can be implemented from it directly. No product measurement, corpus fetch, adjudication or product run was performed for it. The numbers in §5 are arithmetic.

**What Q0 owes.** The M3-Q0 row (`M3-PLAN.md:157`) names the case model (AQP:132-137), the label ledger (AQP:251-265), the confidence rule (AQP:235-239), the exploratory envelope (AQP:428-434), the D12 runner, and the rule-catalog draft specs (AQP:169-193). Q0 also has to size K2, which the critical path leaves "unbounded until Q0 sizes it" (`M3-PLAN.md:222`, `M3-PLAN.md:241`).

**Who depends on it.**
- **M3-L's acceptance gate** includes Q0, D13 and the D2 draft (`M3-PLAN.md:160`).
- **S-M**'s report waits for the Q0 envelope and D13; its Q6-labelled samples wait for D12 (`M3-PLAN.md:158`).
- **K1 and K2** depend on Q0 (`M3-PLAN.md:172`), and so does **I2** (`M3-PLAN.md:171`).
- **M3-M** runs the measurement this record defines (`M3-PLAN.md:173`).

**Authority.** The mechanisms below are lead decisions (AQP:527), numbered **QD-n** so that reviewers can cite them. Three items need sign-off that this record cannot give: D12 (AQP:543), D13 (AQP:544) and the D4 revisit (AQP:534). §14 lists them.

Short names, as in the accepted plans:
- **AQP:** `docs/implementation/m3/analysis-quality/PLAN-r5.md` (r5, pinned, sha256 `c8ceb480…`). Every plain `AQP:` citation refers to this file. r9 remapped citations from r4 to r5, and r10 pins them so that later plan revisions cannot move them. References to r4's removed RSS rule cite `PLAN-r4.md`.
- **AQP6:** `docs/implementation/m3/analysis-quality/PLAN-r6.md` (the r6 snapshot, sha256 `8aed6eb8…`; C2-Q0-R10-N03). Cited only for its corrected §5.1 peak-memory wording (AQP6:335-346), which supersedes r5's §5.1 bullet.
- **M3-PLAN:** `docs/implementation/m3/M3-PLAN.md` (r4, accepted)
- **OPP:** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; lines of the live file, which carries the acceptance note)
- **AQ / IE / NE / WS:** `docs/v2/contracts/product-v1/{admission-and-qualification,identity-and-evidence,native-evidence,workflows-and-surfaces}.md`
- **RS3:** `docs/coop/design-corrections/foundation/product-quality-report.schema.v3.json`
- **PQV:** `docs/coop/design-corrections/foundation/product-quality-validator.py`
- **CAN:** `docs/coop/design-corrections/foundation/canonical.py`
- **QG:** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **AQC:** `docs/coop/completion/analysis-quality-completion.v2.md`
- **LQM:** `docs/coop/completion/language-quality-matrix.completed.v2.json`
- **SMAP:** `docs/coop/design-corrections/current-source-map.proposed.md`
- **ENV:** `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json` (drafted with this record)

---

## r11 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R10-01 (mount invariant) | §9.3 QD-33 item 2, calibration, §9.5 cases | The fresh view is installed by **removal, not overmount**. Inside the private mount namespace, the launcher moves its working directory out of cgroupfs, then detaches (`umount2` with `MNT_DETACH`) every inherited `cgroup2` and `cgroup` v1 mount and alias, then mounts a fresh read-only `cgroup2` at `/sys/fs/cgroup`. The invariant is stated over the mounts that remain: exactly one cgroup-type entry, which is read-only, leaf-rooted and at `/sys/fs/cgroup`. A failed setup is `cgroup-isolation-unverified`. The ordinary inherited writable mount is a success calibration case. |
| C2-Q0-R10-02 (before-creation reasons; no-leaf settlement) | §9.3 steps 1 and 5, Elapsed, §9.5, QD-27, ENV | The batch checks run before any run leaf exists, and a failure creates no leaves. Absent rows may carry `cgroup-escape-unprevented` (no `nsdelegate`) and `cgroup-isolation-unverified` (the batch-start outside-process check). The same reasons after creation carry a created leaf. Elapsed settlement is conditional: with a leaf, the root reaped, `ECHILD` and `populated 0`; with no leaf, the root reaped and `ECHILD`. A no-leaf drain timeout kills the process group and records the new `settlement-failed`, which nulls both values. |
| N01 (continuous non-dumpability) | §9.3 QD-33 item 4 | The outside set is the harness and its driver. Each is non-dumpable from its start, and they never exec during a batch. The check is repeated after every run, and a violation is `cgroup-isolation-unverified`. |
| N02 (audit descriptor) | §9.3 QD-33 item 3 | The audit expects {0, 1, 2, *a*}, then closes *a*, so exec carries exactly {0, 1, 2}. |
| N03 (AQP6 pin) | Short names | AQP6 now points at `PLAN-r6.md` (`8aed6eb8…`). |
| N04 (baseline predicate) | §9.5 QD-34 | Compatibility is checked on the measurement, the reset and cache policy with charge ownership, the kernel release, the runner class and the entry method. "Otherwise `no-baseline`" applies only to complete rows; `incomplete` takes precedence. |
| (review note) | §9.3 Continuous ownership, calibration | The endpoint inode and controller checks are explicitly **not** claimed to detect a disable and re-enable cycle. The test-hook case exercises the sole-writer guard instead. |

## r10 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R9-01 (descriptors and control ownership) | §9.3 (QD-33), calibration, QD-27, ENV | Before exec, the launcher: unshares the cgroup and mount namespaces from inside the leaf; mounts a fresh **read-only** `cgroup2` that shows only the leaf; checks `mountinfo`; closes every non-allowlisted descriptor with `close_range` (all harness fds are also `O_CLOEXEC`) and checks `/proc/self/fd`; and requires every other same-uid process to be non-dumpable. The harness holds the leaf by an `O_PATH` directory fd, is the only writer, and checks the inode and controllers at the read. Anything unverifiable is `cgroup-isolation-unverified`, which nulls memory only. Both reviewed attack paths are calibration cases. |
| C2-Q0-R9-02 (anonymous-RSS bound) | §9.3 steps 3 and 6, the peak-memory paragraph | The universal bound is withdrawn, matching quality-plan r6 §5.1 (AQP6:336-340). Entry establishes placement for later accounting only. First-touch charging means pages charged elsewhere, inherited before exec or shared are not counted, and shared pages are charged once. A calibration case shows that inherited pages are not counted. |
| C2-Q0-R9-03 (leaf validation) | §9.5, ENV `cgroupLeaves` | Leaf evidence now comes from the driver, independent of the operational record. Each slot's row holds either a created leaf, or `leafName: null` with an `absentReason` tied to the same reason in `slotReasons` (`cgroup-unavailable`, `cgroup-v1-only`, `cgroup-no-delegation` or `memory-peak-unavailable-platform`). Distinctness is checked only among created leaves. |
| C2-Q0-R9-04 (baseline compatibility) | §9.5 (QD-34), ENV | `baselinePeakRssBytes` is replaced by `baselineCgroupMemoryPeakBytes` plus `baselineBasisDigest`, a reviewed basis declaring the measurement, reset, cache policy, runner class and entry method. The 1.25× ratio applies only against a compatible charged baseline; otherwise the status is `no-baseline`, an initial measurement. Comparing against the §5.2 absolute budgets is informational only (`absoluteChargeComparison`) until D13. |
| N01 (stale ENV citations) | ENV `description`, Short names | AQP citations are pinned to `PLAN-r5.md`, and the ENV description cites `PLAN-r5.md:428-434,544`. |
| N02 (settlement) | §9.3 steps 5, Elapsed | The harness is a child subreaper. Settlement means the root has been reaped, `waitpid` reports `ECHILD`, and `populated 0`. A drain timeout kills the leaf, gives `cgroup-not-empty`, and nulls both values. |

## r9 changes: lead decision to stop per-process RSS attribution

| Item | Section | Change |
|---|---|---|
| **Lead decision (QD-32)**, following the amended quality plan r5 (AQP:331-338) | §9.3 | Linux peak memory is cgroup v2 `memory.peak` of a fresh dedicated leaf per measured run, labelled `cgroupMemoryPeak` and never called RSS. Per-process `wait4` `ru_maxrss` values from the host's operational record are informational only. macOS stays `incomplete`. Equivalence to AQ's "peak RSS bytes" goes to D13 (OI-2). |
| Rejected alternatives, recorded | §9.3 | **More ptrace rounds:** R8-01 to R8-04 (untraced clone paths, exec-entry reads that are not final, `CLONE_VM` and `vfork` sharing, attach and detach consistency) showed each needs more design. **r4's larger-of-two rule:** its per-process half failed in r2–r8, and its sampled concurrent sum can miss short peaks (AQP:337-338). |
| R8-01 to R8-04 | §9.3 | Moot: the ptrace mechanism is withdrawn. |
| R8-05 (batch identity) | §9.5 | **Moot.** There is no separate traced RSS batch any more: elapsed time and memory come from the same runs, and there is no split mode. Batch identity stays (round, workload, workflow, reset, control, ordinal), with one physical batch per ordinal, and the retry and final rules are unchanged. `rssCollection` and `rssBatchId` are removed. |
| The cgroup method | §9.3 steps 1–6 | Host checks (cgroup v2, `memory.peak` on 5.19 or later, with AL2023 at 6.1; delegation and permissions); escape prevention through a cgroup namespace on an `nsdelegate` mount; a fresh leaf per run, with no reset, because writable `memory.peak` needs a later kernel; entry before exec (`clone3` `CLONE_INTO_CGROUP`, or verified migration before exec); a drain to `populated 0` before the read; and empty verification. Charged page cache is disclosed. |
| Reasons | §9.5 QD-27, ENV | Removed: every tracer and own-counter reason, `untraced-process` and `host-join-unresolved`. Added: `cgroup-unavailable`, `cgroup-v1-only`, `cgroup-no-delegation`, `cgroup-escape-unprevented` (beyond the decision's list, because emptiness alone cannot exclude a same-uid self-migration), `cgroup-read-failed`, `cgroup-not-empty`, `memory-peak-unverified` and `memory-peak-unavailable-platform`. |
| Schema | ENV | Q6 samples are now elapsed and `cgroupMemoryPeakBytes`, with `maxCgroupMemoryPeakBytes`. `runner.calibration` holds kernel release, `memoryPeakVerified`, `nsdelegate`, `cgroupEntry` and `leafOverheadPpm`. Operational-record rows carry `carriesProcessMaxRss`. |
| Withdrawn | QD-29, QD-30, QD-31; the host-join part of QD-28 | Kept as history in the change tables and `DESIGN-r7.md` and `DESIGN-r8.md`. |
| Citations | Short names | AQP is now the live r5 file. Every earlier AQP citation was remapped mechanically, and references to the removed r4 RSS rule cite `PLAN-r4.md:327`. |
| Tests | §9.3 calibration, §9.5 | Cgroup calibration cases, both complete and incomplete; schema and validator cases; a reference model of the per-run procedure. |

## r8 changes: lead decision to adopt OI-19

| Item | Section | Change |
|---|---|---|
| **Lead decision (QD-30)** | §9.3 | Figure (b) on Linux is collected by ptrace: `PTRACE_SEIZE` with the TRACEFORK, VFORK, CLONE, EXEC, EXIT, SECCOMP and EXITKILL options. The exiting thread's `VmHWM` is read at each `PTRACE_EVENT_EXIT` stop, and the group's final value is the last thread's read. A seccomp `SECCOMP_RET_TRACE` exec stop reads each image before exec, and `PTRACE_GETEVENTMSG` re-keys a non-leader exec. Group-stops are held with `PTRACE_LISTEN`, and signals are reinjected unchanged. On harness death the tree is killed (`tracer-died`); on a controlled failure every tracee is detached (`tracer-failed`). |
| Withdrawn | §9.3, QD-19, QD-29 | The process-event connector, taskstats records, the census, the K/L/S fences, the per-CPU sequence proofs and post-S probes, and `pre-exec-image-unmeasured`. |
| Rejected alternatives, recorded | §9.3 | Keeping r7's mechanism: four rounds of gaps, and unproven until calibration. Budgeting on the concurrent sum alone: it needs an AQP/LQM successor (`PLAN-r4.md:327`; LQM:925). |
| Completeness proof | §9.3 step 7 | Now structural: every task is attached before it runs; every thread ends in an observed exit stop with a read, or an observed termination without one (`own-counter-missing`); every exec is read; and the harness survives the run. |
| Interactions | §9.3 steps 8–10 | Yama: scope 3 or a failed attach is `tracer-unavailable`. O7: seccomp stacks most-restrictive-wins, Landlock permits tracing from outside the domain, the tracer never changes a tracee's state, and K1c checks that confinement denials survive tracing. Overhead: K1c measures it, and the preregistered QD-31 rule chooses combined or split (`rssBatchId`) RSS collection. macOS is unchanged (`incomplete`). |
| Host join | §9.3 | Kept as an exact-equality join on (tgid, field-22 ticks). The harness key is now read race-free at the attach stop. PID and time namespaces must match. |
| Deviation from the decision text | §9.3 step 3 | `VmHWM` is read from the exiting thread's `/proc/<tgid>/task/<tid>/status`, not the leader's, because an early-exiting leader has already released its address space. The value is group-wide, and K1c verifies this. |
| Schema | ENV | Withdrawn reasons removed (unused; nothing depends on them): `pre-exec-image-unmeasured`, `inventory-incomplete`, `unregistered-process`, `subscription-unverified`, `event-loss`, `unjoinable-identity`, `terminal-record-missing`, `terminal-record-duplicate`, `drain-timeout`, `cpu-coverage-unproven`. Added: `tracer-unavailable`, `tracer-died`, `tracer-failed`, `untraced-process`. Q6 rows carry `rssCollection` and `rssBatchId`. `runner.calibration` gains `yamaPtraceScope`, `tracingOverheadPpm` and `rssCollectionMode`, and drops `spawnIsCloneVm`. |
| Tests | §9.3 calibration, §9.5 | New calibration success and incomplete cases, schema and validator cases, and a structural-proof reference model. |

## r7 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R6-01 (per-CPU coverage through S) | §9.3 steps 3 and 4, calibration, QD-27, ENV `runReason` | Once S's connector exit has been received, a post-S probe runs pinned to every online CPU. Each CPU's sequence-gap proof runs from its pre-launch sentinel through its post-S probe, and S stays the attribution cutoff. Coverage that cannot be proven (a CPU offline, pinning failed, or a probe missing) is `incomplete` with the new reason `cpu-coverage-unproven`, which nulls (b) and the peak only. Calibration adds the reviewed lost-late-birth sequence, which must give `event-loss`, and three unproven-coverage cases. |
| N01 | §9.3 step 4 | The sufficiency argument is reworded around single-socket enqueue order and pre-reap ordering only. |
| N02 | §9.3 calibration | The pre-launch-exit case is qualified: a census or window-birth predecessor gives `unjoinable-identity`. |
| (lead) | OI-19 | A simpler synchronous alternative is recorded for the coordinator's decision: ptrace exit-stop collection of `VmHWM`. |

## r6 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R5-01 (terminal-record generation) | §9.3 steps 4–6, calibration, §9.5 reference cases | QD-29 adds generation safety with three queue-position fences: K (census), L (launch) and S (close, on S's connector **exit** event). A window-open census of every live tgid is taken from `/proc` with field-22 ticks. A subtree tgid that is in the census, or has any other window birth, is `unjoinable-identity`. An `AGROUP` record is attributed only within the L–S range, and only to a subtree lifetime whose tgid has exactly one known generation. Taskstats has no start field in field 22's representation, so none is used, and there is no clock conversion. Terminal selection no longer relies on `ac_tgid` alone. Calibration adds the reviewed predecessor sequence and three related cases. |
| C2-Q0-R5-N01 (PID namespace) | §9.3 step 4 | Initial-PID-namespace tgids and `/proc` view are required. The PID-namespace identities of the harness, the host and pid 1 must all be equal; otherwise the run is unresolved. |

## r5 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R4-01 (host-join bridge) | §9.3 steps 4 and the host join, QD-27, ENV `runReason` | The interval test is withdrawn. On each fork or exec event, the harness reads `/proc/<tgid>/stat` field 22 (clock ticks) and keys the lifetime by (tgid, `starttimeTicks`), the same field the host's parent reads before reaping. The join is exact integer equality, with no clock conversion and equal time namespaces required. A failed read, an inconsistent key, a reused tgid, a missing match or a namespace mismatch is `host-join-unresolved`, and the run is `incomplete`; the host value is kept, never discarded. Fork-timestamp ordering is replaced by a run-window tgid-uniqueness rule. Calibration and validator cases are added. |

## r4 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R3-01 (warmup reason carrier) | §9.5, ENV `q6` | The untyped seven-position `runReasons` is replaced by `slotReasons[]`: one row per affected slot, keyed by the typed run slot (priming, warmup 0–2 or measured 0–6). Coverage consults it for every required slot. A warmup-only evidence failure keeps the batch `incomplete` and retained, with all measured samples intact. |
| C2-Q0-R3-02 (reasons must not erase known values) | §9.5 (QD-27), ENV `description` | A fixed mapping says which quantities each reason invalidates. A value is null exactly when a reason concerning that quantity exists, and all other known values and aggregates are kept. `record-missing` and `record-invalid` null no numeric sample. Any reason still makes the row `incomplete`. |
| N01, N02 | §9.3 | Per-tgid buffering and conservative rejection of reuse ambiguity; the host-key reconciliation and retained lifetime history; the sentinel as a birth-history fence only; calibration success cases separated from expected-incomplete cases. |

## r3 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R2-01 (complete lifetime RSS) | §9.3, §9.5, ENV `runReason` | Linux figure (b) is complete only by a positive proof:<br>- an acknowledged pre-launch subscription on every online CPU, proven live by per-CPU sentinels;<br>- loss detection (receive errors and overruns, per-CPU connector sequence gaps, CPU-set changes);<br>- lifetimes keyed by (tgid, fork timestamp);<br>- one terminal record per thread group, selected by `ac_tgid` with `AGROUP`; per-thread records are never summed;<br>- draining that ends only when every lifetime has its terminal record and every per-CPU post-run sentinel has arrived;<br>- a two-channel cross-join.<br>Any failure, or anything that cannot be evaluated, is `incomplete` with a new typed reason. Completeness is never inferred from absence. K1c's calibration adds short-lived children, an early-exiting leader, induced loss and pid reuse. |
| C2-Q0-R2-02 (batch join) | §9.5, §9.6, §11, ENV | `operationalRecords[]` rows carry `batchId` and a typed run slot. Runner observations move to `batchObservations[]`, one row per batch. Per-runner calibration stays in `runner.calibration`. The validator's identity, coverage, uniqueness, orphan and sample-consistency checks are listed. |
| C2-Q0-R2-03 (slip slack) | §13 | The slip is recomputed through F1 → H → J2 with every dependency: M3-X = 26 + max(0, *s* − 3). That is 3 days of oracle slip, not 4. The split authoring/run alternative is named, and OI-12's list gains the slip rule. |
| N01–N04 | §5.2, §5.6, §5.8, §9.5 | The error wording is restricted to the Clopper–Pearson branch, with the product-branch example. The OI-17 cost estimate is withdrawn. "Exactly when" becomes "guaranteed when". Sample and reason consistency is assigned to the validator. |

## r2 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R1-01 (truth-input closure) | §3.3 | The truth-input digest is now the full selected-universe and resolution-input closure: the whole snapshot inventory, including additions and deletions, so a newly present resolution candidate changes it. Narrower rule-specific closures are allowed only through a reviewed soundness argument (none is admitted in r2). The unexplained-output trigger compares input components separately from output fields. |
| C2-Q0-R1-02 (advisory allocation) | §5.7, §5.8 | Water-filling allocation reaches the 100-finding floor whenever enough findings exist. Unused slots are redistributed, selection within each family stays uniform, and the floor applies per stratum and per evidence set. Population and sample are recorded separately, and the bound uses each family's sampled denominator. The cost estimate is redone with two votes and calibration. |
| C2-Q0-R1-03 (advisory census guard) | §3.4, §5.6, ENV `q2` | The guard is now two-sided and conservative. Unlabelled findings count as not true for the guard's lower value and as true for its upper value. FAIL needs the upper value below the target; a lower value below the target is INSUFFICIENT-EVIDENCE. Corpus, sampled, settled, pending and unlabelled counts are carried separately. A sample ratio is never called census precision. A sharper pooled inference rule is routed for approval as OI-17. |
| C2-Q0-R1-04 (repository execution) | §6.2, §7, OI-6 | At M3 only tool modes whose pin verifies, with a canary fixture, that no repository code executes. Executing differentials and Rust compile validation are deferred to the M5 authorized execution path (`M3-PLAN.md:347-352`). Confinement is an additional condition, never the authorization. |
| C2-Q0-R1-05 (lifetime RSS) | §9.3, QD-19 | Named counter sources and units. Every supervised descendant is registered, and its own counter is collected at exit. Lifetimes are keyed by (tgid, start time). Host values can only raise a figure, never replace one. Incomplete inventory or collection is an explicit NON-PASS, never filled from sampled peaks. macOS has no harness-readable own lifetime counter, so macOS runs are `incomplete` for RSS; this is open item OI-18. |
| C2-Q0-R1-06 (denominators) | §11, §12, ENV | Per-repository Q2 rows with line counts by class; Q3 and Q6 yield numerators and denominators; per-rule Q7 rows with populations, a score histogram and disposition counts. Measured sections must carry these fields; not-measured stays explicit. |
| C2-Q0-R1-07 (incomplete performance) | §9.3–§9.5, ENV `q6` | A closed `incomplete` variant with typed per-run reasons and null where a sample is unavailable; it can never be `within`. Batch identity and ordering: the first run is batch 1, the retry is batch 2, and the final verdict is the last batch. |
| C2-Q0-R1-08 (K2 schedule) | §13 | Each lane's oracle is frozen and reviewed before any producer output in that lane. K2 moves into the pre-day-0 window, and the M3-PLAN bounds to update under OI-12 are listed. |
| N01–N05 | §5, §4.4, §1.4, §2.1, §8.3, §9.6 | "Family-weighted" naming; the IID premise of the Clopper–Pearson branch; correct rounded-down reference values; the simulation claim removed in favour of the proof; κ rater slots; persistent held-out exposure; runner observations carried; AQP:170-176 field citations; the restricted Rust refactor domain. |

---

## 0. Ground rules the harness inherits

These come from accepted law. The design keeps every one of them.

- **Expected answers are independent.** A report cannot supply or alter its own expected subject, answers, runner or baseline (AQ:196-198). The gate computes counts and correctness itself and reads no PASS flag (AQ:263-266; PQV:24-27). K2 is authored before the producers for this reason (`M3-PLAN.md:172`).
- **RS3 is closed.** It has `additionalProperties: false` and a fixed required set (RS3:4-18), so it carries no `standing` member (AQP:428). The harness never adds a field to it.
- **The product statistic** is 3 warmups, then 7 measured runs; the median of the elapsed times and the maximum of the peak-RSS samples; 1.20× and 1.25× against a reviewed baseline; plus reviewed absolute bounds (AQ:268-276; RS3:78-101). The reference gate takes `sorted(elapsed)[3]` and `max(peakRss)` (PQV:28). Since r9, the harness's per-run memory figure is `cgroupMemoryPeak` (§9.3; AQP:331). Whether that satisfies "peak RSS bytes" for qualification is D13's question (AQP:335).
- **Offline runs.** Ordinary analysis and discovery are offline (AQ:346). Corpus acquisition is a separate, explicit, networked harness step, and runs read only pinned local bytes (AQP:209).
- **No repository code executes at M3** (`M3-PLAN.md:355`). S-P and S-M execute no build script, proc-macro or package script (`M3-PLAN.md:158`).
- **Freeze before measuring.** Metric definitions, denominators, rubrics and held-out sets are frozen and digest-pinned before any acceptance measurement (AQP:161).
- **Exploration is never promoted.** A G13 qualification run re-executes from scratch on the D12 lanes against the held-out set (AQP:442).

**Canonical bytes.** Every harness record digested below is serialized with the foundation canonicalization: sorted keys, compact separators, UTF-8, no floats, at most 4 MiB (CAN:67-74; floats are refused at CAN:61). **QD-1:** proportions and bounds are therefore stored as integer millionths (`…Ppm`). A lower bound is rounded down and an upper bound up, so rounding never helps a pass. Every pass/fail decision is computed in exact rational arithmetic (§5.6), never from the rounded value.

---

## 1. The case model

### 1.1 Case kinds

One record type, with a `caseKind` discriminator. Each kind maps to one accepted measurement.

| `caseKind` | Measures | Source of the expected answer |
|---|---|---|
| `cell-observation` | Q1, and Q4 on T1 | T1 oracle fixture: exact atoms and exit (AQ:240-246, AQ:256-266) |
| `finding` | Q3, Q4, and Q2 calibration items | the corpus oracle: T1, a validated seed, a fix reversal, a lookalike or a curated differential case (AQP:269-291) |
| `refactor-pair` | Q5 survival | the independently reviewed mapping oracle (AQP:308) |
| `determinism` | Q5 determinism | equality of canonical results (AQP:318-321) |
| `workload` | Q6 | the pinned workload manifest (AQP:342-347) |
| `config-shape` | Q8 | the pinned shape with its manual-correction count (AQP:148; SMAP:67) |

Q2 itself is not case-scored. It is measured on adjudicated T2 findings (AQP:142, AQP:230); §3 to §5 cover that.

### 1.2 The scoring unit and expected answers

A `finding` case is the scoring unit (rule, subject, required relation@rung, universe, configuration). Configuration means the mode, target, features, cfg and prepared-input set (AQP:132). Each case pins exactly one expected answer, independently of any candidate run (AQP:132-137):

| `expectedAnswer.kind` | Meaning | Required extra fields |
|---|---|---|
| `determinate-positive` | a finding is required | `expectedFinding`: rule, subject, correspondence expectation |
| `determinate-negative` | a retained no-match is required | none |
| `must-abstain` | required evidence is insufficient (NE:2260), with propagation applied (NE:2230) | `expectedDeficiency`: the deficiency class the case must surface (AQP:293-298); `positiveSoundUnderDeficiency`: boolean |

`positiveSoundUnderDeficiency` records whether a finding would still be sound under the deficiency. A sound positive under incomplete Coverage is a correct determinate fail, not a Q4 failure (AQP:300; WS:600-604). The oracle decides this when the case is authored, never the candidate run.

"Answerable" means `determinate-positive` or `determinate-negative`. The candidate's Coverage never chooses which cases are scored (AQP:137).

### 1.3 Outcome classification

The candidate result for a case is one of: `found`, `no-match`, `indeterminate(deficiency)`, `refused(code)` or `error`. Scoring is a fixed table (**QD-2**):

| Expected | `found` | `no-match` | `indeterminate` | `refused` / `error` |
|---|---|---|---|---|
| positive | Q3 hit | Q3 miss; cause classified (below) | Q3 miss, and a yield loss (AQP:143, AQP:159) | Q3 miss; defect |
| negative | case false positive (reported beside Q2, never inside it) | correct | yield loss, dispositioned (AQP:154) | defect |
| must-abstain | correct if `positiveSoundUnderDeficiency`, else a false positive | **Q4 failure**: an unsupported determinate negative (AQP:144) | correct if the deficiency matches; otherwise `deficiency-mismatch`, dispositioned | correct only if the case pins that typed refusal |

**Miss causes** (AQP:302-304). The oracle records whether the required evidence was complete:
- complete, but the detector or predicate erred: a **Q3 miss**;
- the candidate's Coverage claimed complete, but the oracle shows the evidence was missing: a **false completeness claim**, which is a **Q4 failure** and release-blocking.

On T1 a deficiency mismatch also fails Q1, because Coverage atoms are compared by exact set equality (AQC:127-130).

### 1.4 Case fields

| Field | Content |
|---|---|
| `caseId` | stable human-readable ID, unique in the case set |
| `caseKind` | §1.1 |
| `tier` | `T1`, `T2` or `T3` (AQP:203-207) |
| `origin` | `oracle-fixture`, `validated-seed`, `fix-reversal`, `negative-lookalike`, `curated-differential`, `curated-adjudication` |
| `family` | the independence family (§5.3), for T2 and T3 |
| `heldOut` | boolean: a member of the held-out repository set or a held-out mutation family (AQP:221, AQP:280). Held-out standing is **reserved and never exposed** (**QD-23**, N04). The ledger keeps a permanent `exposure` history (§3.2). Once a case, repository or family has been inspected outside an acceptance round (its findings viewed during development, its labels read, or used as a curated differential source during development), it loses held-out standing permanently. Rotating a freeze seed, or curating it again, never restores it. The acceptance gate checks this history, not the flag alone. |
| `inputs` | `fixtureManifestDigest` (T1) or `{repository, commit, treeDigest}` (T2, §10); for a seed, `controlTreeDigest` and `mutantPatchDigest` |
| `rule` | `ruleId` and `ruleSpecDigest` (§2) |
| `subject` | universe, subject kind, logical subject key |
| `requirement` | relation@rung and universe |
| `configuration` | mode, targets, features, cfg set, `dependencySourceSetId`, `preparedOutputSetId` (NE:1265, NE:1274) |
| `expectedAnswer` | §1.2 |
| `cell` | for `cell-observation` only: the CellId coordinates, expected atoms `{kind, subject, value}`, expected exit, and work and stress bounds (AQ:240-246, AQ:259-262) |
| `provenance` | the author or generator, plus the ledger records that settled the expected answer (§3) |
| `caseDigest` | SHA-256 of the canonical bytes of the record without `caseDigest` |

### 1.5 Pinning and digests

- **The case set** is a JSON Lines file. There is one canonical record per line, the lines are sorted by `caseId`, and the file ends with a newline. `caseSetDigest` is the SHA-256 of the file bytes.
- **T1 fixtures** live under `tests/qualification/fixtures/` in the product repository, with per-file SHA-256 and a manifest digest, like the preview corpus (AQP:205). A T1 case references the fixture manifest digest.
- **The freeze record.** Each measurement round is opened by one `freeze` record in the ledger (§3.4). It pins: `caseSetDigest`, `ruleSpecSetDigest`, `rubricSetDigest`, `familyMapDigest`, `heldOutSetDigest`, `metricDefinitionsDigest` and `preregistrationDigest` (§5.7). A case added after the freeze enters the next round, never the current one (AQP:161).
- **Change control.** A changed expected answer is a new case revision with a new digest. The old revision is kept, and the change must cite a ledger record. A candidate run can never change a case (AQP:154).

---

## 2. Rule-catalog draft specs

The draft catalog is a prerequisite for Q2 and Q3 scoring (AQP:169). I2 evaluates it non-authoritatively in the harness (`M3-PLAN.md:171`). Each rule is a `PolicyDocumentV2` rule (AQP:167; WS:593-597), evaluated under strong Kleene: under incomplete Coverage `none` is false on a match and otherwise indeterminate (WS:600-604). A universal negative therefore abstains by construction when its Coverage is incomplete.

### 2.1 The spec record

The fields follow AQP:170-177. Q0 adds one field, `propositionClass` (**QD-3**), because label carry-forward (§3.3) needs it.

| Field | Content |
|---|---|
| `ruleId`, `specRevision`, `specDigest` | identity |
| `propositionClass` | `existential`: true because a witness exists (a cycle, an unresolved specifier, a crossing edge). `universal-negative`: true because nothing in a universe refers to the subject (the unused and unreferenced rules). |
| `subjectPopulation` | universe, subject kind, include/exclude (AQP:170) |
| `predicate` | the exact proposition in words, plus an `emitWhen` sketch (AQP:171). I2 binds the relation IDs. |
| `configurations` | mode, targets, features, cfg and dev/build/test scope (AQP:172) |
| `closedWorld` | the `ClosedWorldV2` fields the rule needs (AQP:173; NE:2210-2224) |
| `minimumSufficiency` | the relation@rung and Coverage that must be complete for a determinate negative (AQP:174) |
| `lookalikes` | legitimate cases that must not fire (AQP:175) |
| `default` | gating, advisory, or gating only after declared policy (AQP:176) |
| `explanationTemplate`, `limitations` | (AQP:177) |
| `mutationFamilies` | §6.1, with the held-out family marked |
| `rubricDigest` | the frozen adjudication rubric (§4.1) |

### 2.2 The draft rules

The rules and defaults are AQP's (AQP:181-193); Q0 adds the proposition class, the minimum sufficiency and the lookalike set. Every dead-code rule also carries AQP:195's required truth fixtures: outside-workspace consumers, re-exports, `pub(crate)`, multi-crate workspaces, feature and cfg variants, test and build dependencies, and framework or generated entry points.

| Rule | Class | Minimum sufficiency for a negative | Required lookalikes | Default |
|---|---|---|---|---|
| `ws-unreferenced-export` (TS/JS) | universal-negative | complete in-universe reference Coverage at the semantic rung; no dynamic edge whose possible targets include the subject (NE:2230) | re-exported, `import *` namespace use, type-only use, use from a test or config file inside the universe | advisory (AQP:183) |
| `unused-export` (TS/JS) | universal-negative | as above, plus `exportsClosed=closed` and `externalConsumers=none-declared` (NE:2213-2224) | `private:true` alone (NE:2226), published subpath, `bin` entry | gating (AQP:184) |
| `unimported-file` (TS/JS) | universal-negative | `entryPointsRecognized=all`; complete import Coverage | convention-loaded framework file (L-FW1), side-effect import, config-referenced file | gating, otherwise indeterminate (AQP:185) |
| `rs-workspace-unreferenced-pub` | universal-negative | complete cross-crate reference Coverage over the selected targets and features | used only under a non-selected cfg; used only in tests; used through a re-export; used from a macro expansion | advisory (AQP:186) |
| `rs-unused-pub-item` | universal-negative | as above, plus closed world: not reachable from the published API and `externalConsumers=none-declared` | a library crate's public API; `pub(crate)` | gating (AQP:187) |
| `unused-dependency` | universal-negative | complete use Coverage across every selected target that declares it, counting build scripts, proc-macros, tests and features (AQP:189) | used only in `build.rs`; used only by a proc-macro; used only behind a feature; renamed dependency | gating per declared scope |
| `module-import-cycle` | existential | the witness edges are resolved | type-only import cycle, if the policy excludes it | gating only by declared policy (AQP:190) |
| `unresolved-import` | existential | the specifier and the resolution attempt are disclosed | an ambient module declaration; a path alias | advisory (AQP:191) |
| `clone-*` | existential | facts only; near clones are candidates (L-CL1) | generated code | advisory, never gating (AQP:192) |
| `boundary-violation` | existential | the crossing edge is resolved | an allowed exception in the declared layering | gating once declared (AQP:193) |

Repair eligibility is never a catalog rule. It stays per finding, through `deadCodeRepairEligible` (AQP:188; NE:2237-2242).

---

## 3. The label ledger

### 3.1 Storage format (QD-4)

- **One append-only JSON Lines file per round:** `ledger/<roundId>.jsonl`. Every line is one canonical record (CAN:67-74).
- **Chaining.** Each record carries `prevRecordDigest`, the digest of the previous line (`null` on the first), and `recordDigest`, the SHA-256 of its own canonical bytes with `recordDigest` removed.
- **Pinning.** `ledgerDigest` is the SHA-256 of the whole file. The exploratory envelope pins both it and the head record's digest (ENV `ledger`).
- **History.** Nothing is rewritten or deleted. A correction is a new `supersede` record that names the record it replaces and why (AQP:264).
- **T3 labels** stay in a separate local ledger. Only aggregate metrics and labels leave the machine, never source (AQP:207), so a T3 rationale cites `path:line` and contains no source text.

### 3.2 Record kinds

| `recordKind` | Content |
|---|---|
| `adjudicator` | voter registration: `voterId`; `kind` (`human` or `agent`); for an agent: `modelFamily`, `modelId` and `contextClass`; designated-expert flag; rules on which the voter is conflicted (§4.5) |
| `freeze` | the round's pinned digests (§1.5) |
| `item` | an adjudication item: the label key (§3.3), the queue, whether it is a calibration item (the flag is hidden from adjudicators), and the presentation digest (§4.2) |
| `vote` | one blind label: `itemId`, `voterId`, `label` (`true`, `false` or `unclear`), a rationale citing `path:line` at the pinned tree, `triageMillis`, and a `rubricDigest` |
| `escalation` | an item sent to the expert, with its reason: `disagreement` or `unclear-gating` |
| `resolution` | the settled label: `label`, `method` (`agreement` or `expert`), the vote records it rests on, and the expert's rationale when there is one |
| `carry` | a carry-forward decision: the source resolution, the new label key, the per-component compatibility result (§3.3), and `carried` (boolean) |
| `calibration-result` | per voter and round: items, correct answers, known-false items labelled true, and pass/fail against the bar (§4.3) |
| `agreement` | per rule and round: n, raw agreement, Cohen's κ, prevalence, and whether a trigger fired (§4.4) |
| `drift-audit` | per rule and round: the sample, its seed, the results, and whether drift fired (§3.5) |
| `exposure` | a held-out case, repository or family that was inspected outside acceptance: who, when and what was seen. It is permanent (QD-23). |
| `supersede` | the record replaced, and why |

### 3.3 The label key, and what each component binds

A label is bound to a **label key** (AQP:252-257). Q0 splits its components into two groups (**QD-5**).

**Hard components must be identical for a label to carry:**

| Component | Bound to |
|---|---|
| `propositionId`, `rubricDigest` | the adjudicated proposition and the rubric revision (AQP:253) |
| `ruleSpecDigest`, `ruleProgramDigest`, `detectorSemanticsMajor` | the rule definition, program digest and semantics major (AQP:254) |
| `configurationDigest` | mode, target, features and cfg (AQP:255) |
| `dependencySourceSetId`, `preparedOutputSetId` | NE:1265, NE:1274 (AQP:256) |

**The input component that may differ in form only:**

| Component | Bound to |
|---|---|
| `truthInputDigest` (TRI) | the truth-relevant input closure, defined next. It replaces r1's narrower lexical digest. |
| `treeDigest` | the repository tree (AQP:255). It is recorded, and it is covered by the TRI below. |

**Recorded outputs, which are never input components:**

| Output | Content |
|---|---|
| `evidenceRefs`, `messageParameters` | the finding's evidence references and message parameters (`finding3`, IE:190; AQP:257). These are detector output. They never justify reuse; they feed only the unexplained-output trigger. |

**The truth-input closure (QD-5, revised for C2-Q0-R1-01).** The TRI covers the subject, its incoming references and the proof's evidence references (AQP:259). It must not depend on the detector, and it must be **conservative**: any input change that could change the label's truth must change the TRI. r1's lexical, witness-based digest failed that test. In CODEX2's counterexample, adding `missing.ts` resolves `import './missing'` without touching any file in the old digest, and edits through aliases or re-exports need not contain the subject's name. The default TRI is therefore the **full selected-universe and resolution-input closure**, which is the SHA-256 of the canonical record of:
1. the **complete snapshot inventory**: every path in the analysed snapshot, with its mode and content digest, in the §10 tree-digest form. Additions and deletions anywhere in the snapshot change it. That includes previously absent resolution candidates (a new `missing.ts`, a new `index.ts`, a new crate directory) and generated inputs present in the snapshot.
2. the **resolution inputs outside the tree**: `configurationDigest`, `dependencySourceSetId` and `preparedOutputSetId` (already hard components), plus the digest of the harness's resolution environment (the pinned toolchain and closure identities in the freeze).

In practice the default TRI is unchanged exactly when the snapshot and the resolution inputs are byte-identical. A label then carries across product rebuilds that keep the detector semantics major, and across rounds on the same pinned commit, but never across a corpus commit bump.

**Narrower closures.** A rule-specific closure smaller than the default (for example, the files that can reach the subject through resolution) is permitted only when **all** of these hold:
- a written soundness argument covers aliases, re-exports, barrel files, configuration (path mappings, `exports` maps, cfg and features), generated inputs, and the negative searches that universal negatives depend on;
- that argument is reviewed independently of the rule's author;
- it is pinned by digest in the rule spec as `truthClosureSpecDigest`.

r2 admits none, so every rule uses the default.

**The carry rule** (AQP:259). A label carries only if every hard component is identical and the TRI is identical. The check is mechanical, and its per-component result is written as a `carry` record.

**Re-adjudication triggers** (AQP:260-263). Each trigger maps to a mechanical test, and the tests compare inputs and outputs separately (N04):
- a change to the rule, rubric, configuration, dependency set or prepared outputs: a hard component differs;
- a change to the subject or its incoming references, or to anything that could resolve to it: the TRI differs;
- a change in detector output that no input change explains: every hard component and the TRI are identical, but the recorded outputs (`evidenceRefs` or `messageParameters`) differ. This both re-queues the item and files a determinism defect (§8.4).

`finding-key2` is used only to *propose* which earlier label might apply. It is never a reason to carry one (AQP:258; IE:199-213).

### 3.4 Evidence counts

Following CODEX2's r2 observation N02 (`docs/implementation/m3/analysis-quality/reviews/codex2-analysis-quality-plan-r2/review.json`, C2-AQ-R2-N02), the populations are kept apart (**QD-6**, extended for C2-Q0-R1-03). Each count is carried per stratum and per repository (ENV `q2`):
- **corpus:** every finding the candidate emitted in a stratum;
- **sampled:** the findings drawn for adjudication. That is all of them for gating and repair-eligible rules (AQP:230), and the §5.7 allocation for advisory rules;
- **settled:** sampled findings with a resolution (true, false or unclear);
- **pending:** sampled findings without a resolution yet;
- **unlabelled:** corpus minus sampled. These findings were never drawn, so they are never labelled.
- **independent evidence units:** what the confidence rule counts (§5): families, with each family's sampled denominator.

**Naming rule.** "Census precision" is used only when unlabelled = 0 and pending = 0. A ratio computed from a sample is called the *sample ratio*, and it is descriptive only. It is never used for the census guard (§5.6).

Calibration items are never in any of these populations. A finding that appears in two rounds through a carried label counts once per round, not twice. Carried labels count as evidence only in the round that carried them.

### 3.5 Drift audit

Each round, for each rule, the harness samples carried labels: at least 5% and at least 20, or all of them when fewer than 20 were carried (AQP:265). The sample is drawn with a seed equal to `SHA-256(roundId ‖ ruleId ‖ head recordDigest at the freeze)`, so it is fixed by the freeze and can be recomputed. Each sampled item is re-adjudicated blind under §4.

**Drift** means one or more sampled items whose new settled label differs from the carried one. It triggers full re-adjudication of every carried label for that rule in that round (AQP:265).

---

## 4. The adjudication protocol

### 4.1 The rubric

There is one digest-pinned rubric per rule revision (AQP:244). Each rubric contains:
1. the exact proposition from the spec (§2.1), not "is this code good" (AQP:233);
2. a decision checklist ending in `true`, `false` or `unclear`;
3. the lookalike list, with the correct label for each one;
4. what a rationale must cite: `path:line` at the pinned tree, plus the configuration consulted;
5. a **time box**, default 20 minutes (**QD-7**). `unclear` is allowed only with a written reason: the time box ran out, the evidence is outside the pinned bytes, or the proposition is ambiguous for this case. Triage time is recorded on every vote, for Q7's triage-cost report (AQP:156).

### 4.2 Blind presentation

An adjudicator receives a **presentation** for each item: the rule's proposition and rubric, the subject (universe, kind, logical key, and declaration location), the selected configuration, and read access to the pinned tree. The presentation's digest is recorded on the `item` record.

The presentation withholds:
- the other label and its rationale;
- the detector's evidence path, its rationale and its message parameters (AQP:245);
- whether the item is a calibration item.

Calibration items are built in the same format from real T2 code (§4.3), so they cannot be told apart by their shape. Queue order is shuffled with a seed recorded in the freeze.

### 4.3 Calibration items

Known-true and known-false items are planted blind in each queue (AQP:246). **QD-8** sets the numbers:
- **Source.** Known-true items are validated seeds placed in real T2 code (§6). Known-false items are validated negative lookalikes, the hard cases of AQP:279. Both carry expected answers settled before the round.
- **Rate.** At least 10% of each queue, at least 5 items per voter per round, at least 2 of them known-false.
- **The bar.** Calibration accuracy of at least 0.90, and **no** known-false item labelled `true`.
- **Below the bar.** That voter's votes are excluded for the round, and their items are re-queued to other voters (AQP:246).
- **Counts.** Calibration items are excluded from every evidence count and from the agreement statistics (§3.4).

### 4.4 The agreement statistic

The harness records raw agreement and Cohen's κ per rule and round (AQP:249). With precision near 0.99, κ suffers the prevalence paradox: two voters can agree on 99% of items and still get a low κ. So **QD-9** fixes the trigger as follows:
- **Recorded every round:** n, raw agreement, κ, and the prevalence of `true`.
- **Rubric review triggers.** Any one of these sends the rule's definition back for review (AQP:249):
  - raw agreement below 0.90;
  - κ below 0.60, applied only when the minority label class has at least 10 items in the round;
  - `unclear` above 5% of the rule's settled labels.
- **Small rounds.** Below the κ applicability floor, κ is still recorded, labelled `kappa-unstable`. Calibration (§4.3) does the work there.
- **Rater populations (N04).** Each item has two ordered vote slots. Slot A holds the human vote, or the vote of the earlier-registered human when both votes are human. Slot B holds the other vote. The rule-level κ is Cohen's κ over the (A, B) pairs, so it measures agreement between the human slot and the independent second slot. Votes are mapped to slots only after the round closes, and voters never see their slot. The harness also records a pair-specific κ for each voter pair sharing at least 20 items. That is diagnostic only and does not trigger review. `unclear` is a third category in both calculations.

### 4.5 Votes, independence and the model-family rule

**The author rule.** The author of a rule does not adjudicate it (AQP:247).

**Voters.** A voter is a registered person or agent configuration (§3.2). For agents, **QD-10** makes AQP:247 operational:
- **Model family** means the vendor's model lineage: every Anthropic Claude model is one family, every OpenAI GPT or Codex model is one, every xAI Grok model is one, and so on. The `adjudicator` record pins `modelFamily` and `modelId`.
- **Same family, one vote.** Agents from the same family count as **one** vote. If they disagree among themselves, that family's vote is `unclear`.
- **Implementation context.** An agent has implementation context for a rule if it has seen the rule's source, the detector's code, the detector's output for the item, or implementation discussion of the rule. Such an agent counts as the rule's author and does not vote on that rule.
- **This lead's rules.** The draft catalog is authored by the lead, a Claude model. So for these rules, every Claude-family agent is treated as sharing implementation context and does not vote. Agents of other families may vote if they are given only the presentation (§4.2).
- **Agents never stand alone.** Agents assist; they are never independent ground truth on their own (AQP:247). So a settled label needs at least one human vote.

**Settling a label.**
1. Every item receives two votes from two different vote groups (AQP:245). At least one of the two is human.
2. If both are `true`, or both are `false`, the item resolves with method `agreement`.
3. A disagreement goes to the designated human domain expert, and so does every `unclear` on a gating or repair-eligible finding (AQP:248). A third procedural vote does not settle it (AQP:248).
4. If two votes on an advisory finding agree on `unclear`, the label resolves as `unclear` and counts as not true (AQP:234).

### 4.6 Escalation to the expert

**Who.** The expert is the owner or a named delegate (AQP:248), registered with the expert flag (§3.2). The roster is an owner action (`M3-PLAN.md:368`).

**What the expert sees.** The presentation and both rationales. The detector's evidence stays withheld, as in §4.2, so the expert is not anchored to the tool.

**The decision.** It is final for that label key and is recorded with a rationale. If the expert answers `unclear`, the label counts as not true (AQP:234).

**Pending items.** An exploratory report may close while gating or repair-eligible items are still pending. Those strata are reported as `not-yet-adjudicated` (`M3-PLAN.md:173`). Any later Q2 use requires every such item to be resolved (AQP:230, AQP:248).

---

## 5. The confidence rule

### 5.1 The estimand

AQP sets the target on a one-sided 95% lower bound of conservative precision, per stratum. Conservative precision counts unclear as not true (AQP:234). A stratum is rule × language × mode, and strata are never pooled (AQP:235).

The target generalizes beyond the corpus. The 95% statement is about repositories like those in the corpus, and the unit that is sampled from that population is the repository family (§5.3), not the finding.

**QD-11.** The bound is placed on the **family-weighted conservative precision** (N01: named for its actual weighting): the average, over independence families in which the rule fires, of each family's expected conservative precision. Two reasons:
- A finding-weighted bound over correlated findings invents independent evidence. This is the counterexample in the CODEX2 review that produced AQP:237 (the same review file, C2-AQ-R2-01 `analyticIllustration`).
- The family-weighted quantity is close to what a single team sees on its own repository.

**What it does not claim.** It is not a lower bound on the population's finding-weighted precision. The pooled guard in §5.6 does not make it one; the guard only stops a large, poor repository from being averaged away. Each Q2 result names its estimand (ENV `q2.strata[].estimand`). Whether qualification wants a finding-weighted estimand is OI-4, and family-wise confidence is OI-5. Both stay open for the DR-G13 successor.

### 5.2 Which bound applies

The method is chosen from the **structure** of the stratum's evidence before any label is read, so the choice cannot follow the labels. Let *k* be the number of families with at least one finding in the stratum, and let *a_j* be the number of **sampled** findings from family *j* (§5.7). *a_j* equals family *j*'s corpus count for gating rules.

- **Single-finding families** (AQP:236): every *a_j* = 1. **Method: exact Clopper–Pearson** (§5.4).
- **Clustered** (AQP:237): some *a_j* > 1. **Method: the cluster-level product bound** (§5.5).

**The Clopper–Pearson premise, stated (N01).** One finding per family gives distinct evidence units. That alone does not make them IID Bernoulli draws with a common success probability. The Clopper–Pearson branch adds the premise that the *k* families are independent draws from one population of families, with the finding drawn uniformly within each. Each sampled finding is then Bernoulli with the population's family-weighted mean. If that premise is doubted, the product bound remains valid without it, since it allows heterogeneous independent family means (§5.5). The two branches therefore rest on different premises, and each result records which one applied (ENV `method`).

**Where the single-finding design comes from.** The §5.7 allocation is guaranteed to give one finding per family when the stratum has at least 100 families with findings. Smaller strata of single-finding families also get one each, and the formal condition in the branch rule above decides. Gating strata are adjudicated in full (AQP:230), so they take the Clopper–Pearson branch only when every family has a single finding.

### 5.3 Independence families

The independence unit is a **family** of repositories, not a single repository (**QD-12**). Repositories go in one family if any of these hold:
- one is a fork, mirror, vendored copy or split of another;
- they share generated code from the same generator;
- they are parts of one multi-checkout workspace assembly (the D15 approximation is **one** family; AQP:219);
- they share an upstream project, for example a repository and its examples repository.

Sharing an organization alone does not merge two repositories.

Families are assigned in the T2 manifest by M3-T2, reviewed, and pinned by `familyMapDigest` at the freeze. Families with no finding in a stratum do not count toward that stratum's *k*. T3 repositories form their own families, labelled `T3-local` (AQP:207). Per-repository results are reported as well as per-family ones (§12), because a family may hold several repositories (AQP:240).

**The assumption every method needs.** Each bound treats the families as independent draws from the population of repositories the claim is about. T2 is purposely selected (AQP:215-221), not randomly sampled. The held-out discipline (§5.6) guards against tuning on the corpus, but not against unrepresentative selection. The envelope states this assumption on every Q2 result (ENV `q2.strata[].assumption`).

### 5.4 Exact Clopper–Pearson (single-finding strata)

Let *x* be the true count out of *k* single-finding families. The one-sided 95% lower bound *L* is the *p* that solves P(Bin(*k*, *p*) ≥ *x*) = α, with α = 0.05; *L* = 0 when *x* = 0. Equivalently, *L* is the α quantile of Beta(*x*, *k* − *x* + 1).

**Exact decision.** *L* ≥ *t* holds exactly when Σ_{i=x}^{k} C(*k*, *i*) *t*^i (1 − *t*)^{k−i} ≤ α. The harness evaluates this in exact rational arithmetic, with *t* = 99/100 or 9/10 and α = 1/20. It stores *L* rounded down to millionths: the largest *q*/10⁶ for which the tail at *q*/10⁶ is ≤ α.

**Reference values for K1b's self-test (N02).** These are stored integers, rounded down and computed exactly for this record:

| Case | `lowerBoundPpm` |
|---|---|
| *x* = *k* = 299 | 990030 |
| *x* = *k* = 29 | 901855 |
| *x* = 472, *k* = 473 (one error) | 990010 |
| *x* = 45, *k* = 46 (one error) | 900975 |

With one error, *k* = 473 is the smallest count reaching 0.99, and *k* = 46 the smallest reaching 0.90 (AQP:236 gives the zero-error examples).

### 5.5 The cluster-level product bound (clustered strata)

**Chosen method (QD-13), unchanged from r1.** For each family *j*, let *X_j* = *t_j* / *a_j* ∈ [0, 1] be that family's conservative precision **on its sampled findings**: its census value for gating rules, or its uniform within-family sample estimate for advisory rules (§5.7). The denominator is always the family's sampled count *a_j*, never its corpus count. Then

> *L* = α^{1/k} · (Π_j *X_j*)^{1/k}, that is, α^{1/k} times the geometric mean of the per-family precisions; *L* = 0 if any *X_j* = 0.

**Exact decision.** Pass iff Π_j *X_j* ≥ *t*^k / α, as an exact rational comparison.

**Why it is valid.** Fix any *m* in (0, 1]. Suppose the families are independent and the average of their expected precisions is at most *m*. For a sampled family, uniform selection within the family makes *E[X_j]* equal that family's precision. The product of the expectations of *X_j*/*m* is then at most 1 (AM–GM over the family means), so the product is an e-value. Markov's inequality gives P(Π *X_j* / *m^k* ≥ 1/α) ≤ α. Taking *m* to be the true mean, P(*L* ≥ true mean) ≤ α. CODEX2 verified this derivation (review §"Method assessment").

This needs no model of how findings correlate inside a repository, no prior, no asymptotics and no resampling. It also does not need the families to be identically distributed: it bounds the average of their means. It is the fixed-bet, all-in case of the betting confidence bounds for bounded means (Waudby-Smith and Ramdas, *JRSS-B*, 2024; Vovk and Wang, *Ann. Statist.*, 2021). The analytic proof is the evidence for validity. r1's simulation sentence is withdrawn (N03), because nothing about it was retained.

**The zero-error boundary.** If every family is all-true, *L* = α^{1/k}. That is exactly the Clopper–Pearson bound for *k* single observations. **At that all-success boundary**, it is also the most any method can claim without a within-repository model. If each repository were all-true or all-false with mean *μ*, the chance of *k* all-true repositories would be *μ*^k. So 300 findings from 3 perfect repositories give `lowerBoundPpm` 368403, as CODEX2's illustration requires. Identical all-true repositories are never resampled into a pass (AQP:237). Away from that boundary no optimality is claimed (N02).

**It uses partial information.** Unlike reducing each family to a single clean/unclean bit, a family at 0.995 contributes 0.995, not 0. Reference values, stored and rounded down:
- 30 families at 1.0: 904966;
- 29 at 1.0 and one at 0.90: 901793, a pass at 0.90;
- 29 at 1.0 and one at 0.50: 884296, not a pass.

**What it costs.** When findings inside a repository really are independent, the bound is more conservative than a model-based one. That is the price of assuming nothing about correlation within a repository.

**One harsh property, accepted.** A single family whose sampled findings in the stratum are all false or unclear sets *L* = 0. For a gating rule, a repository where every finding is wrong is a defect worth failing. Gating unclear labels go to the expert first (§4.5), so this happens only when the expert also cannot confirm a single finding in that repository.

**Rejected alternatives:**
- **Repository bootstrap.** It is degenerate at zero errors (AQP:237).
- **Beta-binomial or Bayesian hierarchical model.** At zero errors the data cannot identify the within-repository correlation, so the bound would be set by the prior on that correlation. A credible bound is also not the 95% confidence statement Q2 asks for.
- **Design-effect correction with an assumed intraclass correlation.** It is asymptotic, and it needs an assumed correlation that cannot be checked when there are no errors.
- **Reducing each family to a clean/unclean indicator, then Clopper–Pearson.** It is valid, but it throws away partial information.

### 5.6 Status rules, minimum counts, the pooled guard and INSUFFICIENT-EVIDENCE

**Minimum independent families.** At zero errors both methods give α^{1/k}, so a pass needs *k* ≥ *k*_min(*t*) = ⌈ln α / ln *t*⌉ (**QD-14**). These are stored values, rounded down:

| Target | *k*_min | Check |
|---|---|---|
| advisory 0.90 | **29** | *k* = 29 gives 901855; *k* = 28 gives 898534 |
| gating and repair-eligible 0.99 | **299** | *k* = 299 gives 990030; *k* = 298 gives 989997 |

The exact checks are 20·(9/10)^29 ≤ 1 < 20·(9/10)^28, and the same form for 99/100. These are floors: no stratum with fewer families can pass. In the single-finding (Clopper–Pearson) branch, any error raises the requirement (§5.4). In the product branch, an error raises it only if it lowers a family's precision enough. For example, 299 families with 298 at 1 and one at 999999/1000000 give *L* ≥ 0.990030 × 0.999999 > 0.99, which passes (C2-Q0-R2-N01).

**The pooled guard (QD-15, revised for C2-Q0-R1-03).** Let *N* be the stratum's corpus count, *T* and *F* its settled true and settled not-true counts (unclear counts as not true, AQP:234), and *U* = *N* − *T* − *F* the findings that are unlabelled or pending. The guard has two conservative values, computed exactly:
- **verified lower value:** *T* / *N*, which treats every unlabelled finding as not true;
- **optimistic upper value:** (*T* + *U*) / *N*, which treats every unlabelled finding as true.

When *U* = 0, the two coincide and equal the **census precision**. That is the only case in which that name is used. For gating strata, *U* = 0 once adjudication is complete (AQP:230). An unweighted sample ratio is never used for the guard. In CODEX2's counterexample (one family of 10,000 findings at 0.80, plus 99 single true findings, sampled one per family), *T* ≤ 8,099 and *N* = 10,099. The verified value is at most 0.802, so the stratum cannot pass. The upper value depends on the sampled labels, and it is FAIL only if the sample shows enough errors.

**Status, per stratum, evidence set and target, decided in this order:**
1. `NOT-YET-ADJUDICATED`: some **sampled** finding is pending (`M3-PLAN.md:173`). Exploratory only; it is never a Q2 result.
2. `INSUFFICIENT-EVIDENCE`: zero findings, or *k* < *k*_min(*t*) (AQP:238). The bound is still reported.
3. `FAIL`: the optimistic upper value is below *t*. Even if every unlabelled finding were true, pooled precision would miss the target.
4. `INSUFFICIENT-EVIDENCE`: the verified lower value is below *t*. The guard cannot be established without more labels.
5. `PASS`: *L* ≥ *t* by the exact decision in §5.4 or §5.5.
6. `INSUFFICIENT-EVIDENCE`: otherwise. The guard holds, but the bound does not.

If any guard input is unavailable (for example, the corpus count is missing), the stratum is `INSUFFICIENT-EVIDENCE` with the reason `guard-unavailable`, and PASS is prohibited. Neither non-pass status is ever a pass (AQP:238).

**A consequence for advisory rules.** Under this guard, an advisory PASS needs at least 0.90·*N* findings verified true, so in practice nearly the whole stratum must be adjudicated. A sharper rule would bound pooled precision from the sample: a per-family exact hypergeometric lower bound on true counts, at level α/*k* (Bonferroni), summed over families and divided by *N*. Unsampled families would contribute zero, and fully adjudicated families their exact count. That is a new inference rule, so r2 does not adopt it. It is routed for approval as OI-17, and until it is approved the conservative guard above is in force.

**Which families count for acceptance.** The acceptance computation counts only **held-out** families, whose findings and labels were never exposed during rule development (AQP:221, AQP:442; QD-23). Development families give exploratory numbers only, labelled `development`. Both are reported, and every count and status is computed separately for each evidence set.

**Downgrading** (AQP:239).
- A gating stratum that does not PASS at 0.99 is evaluated at 0.90. If it passes, the rule may ship as a qualified advisory rule.
- If it does not pass at 0.90 either, it may ship only as a declared-unqualified exploratory advisory rule. It gets no Q2 pass and no waiver, and it is listed in the envelope's `unqualifiedAdvisoryRules`.
- Both targets are fixed before measurement, so the downgrade involves no tuning.

**Confidence is per stratum.** 95% applies to each stratum, as AQP:235 states. With *S* strata, a release could hold false passes on up to about 0.05·*S* of them in expectation. The plan sets no family-wise correction, and this record does not invent one. §14 OI-5 routes the question to the DR-G13 successor.

### 5.7 Preregistration and advisory allocation

Before any acceptance measurement, the freeze record (§1.5) pins a **preregistration document** (`preregistrationDigest`). It fixes:
- α = 1/20, and the targets 99/100 and 9/10;
- the estimand (§5.1), and the method-selection rule (§5.2);
- the family map and the held-out set, with its exposure history (QD-23);
- the advisory allocation, below;
- the pooled guard and the status order (§5.6);
- the rounding rule (QD-1);
- the cgroup drain limit (§9.3 step 5).

**Advisory allocation (QD-24, revised for C2-Q0-R1-02).**
- **Unit and floor.** The floor applies to each stratum (rule × language × mode), which satisfies AQP:230's "at least 100 per rule per language". It applies separately to the held-out and the development evidence sets. Let *N_j* be family *j*'s corpus count in the stratum and evidence set, and *T* = min(100, Σ*N_j*).
- **Water-filling.** Find the smallest integer *c* ≥ 1 such that Σ_j min(*N_j*, *c*) ≥ *T*, and set *a_j* = min(*N_j*, *c*). Families too small for their share give their unused slots to the others, so the total reaches *T* whenever enough findings exist, and is all of them when Σ*N_j* ≤ 100. The total may exceed 100 by less than *k*.
- **Effects.** With *k* ≥ 100 families, *c* = 1, which gives one per family and the Clopper–Pearson branch. In CODEX2's counterexample (*k* = 29, one family of 100 and 28 of 1), *c* = 72, so the allocation is 72 + 28 = 100.
- **Selection.** Within each family, *a_j* findings are drawn uniformly without replacement, with the seed `SHA-256(roundId ‖ stratumId ‖ evidenceSet ‖ family)`.
- **Recording.** *N_j* and *a_j* are both recorded per family and per repository. The bound uses *a_j* as the denominator (§5.5), and the guard uses *N* (§5.6).

None of these may change after the freeze for that round (AQP:161).

### 5.8 What this means in practice, reported to the owner

**Gating.** A **gating 0.99 PASS needs at least 299 held-out families with findings for that rule, language and mode**, and 299 error-free families suffice at that minimum. In the single-finding branch, one error raises the need to 473 (§5.4). In the product branch, an error costs extra families only to the extent that it lowers a family's precision (§5.6). Every gating finding in them must be adjudicated (AQP:230).

**Advisory.** A 0.90 PASS needs at least 29 held-out families. Under the in-force pooled guard, it also needs at least 0.90·*N* of the stratum's findings verified true. Example: 29 held-out families with 4 findings each give *N* = 116. All 116 are adjudicated: 232 votes, plus calibration of at least 10% of each of the two vote queues (about 13 items each), so about 260 votes, at least half of them human (§4.5). r2's lower estimate for OI-17 is withdrawn (C2-Q0-R2-N02). A sample from small families need not establish the proposed per-family hypergeometric bound, so approving OI-17 would not by itself reduce this cost.

**Scale.** T2 plans at least two repositories per language per size class, with one held out per class (AQP:220-221). Gating strata will therefore be INSUFFICIENT-EVIDENCE unless T2 grows by an order of magnitude. At the all-success boundary this is not a defect of the method: without a within-repository model, no valid 95% method can do better (§5.5). The choice is the D4 revisit (AQP:150, AQP:534) and D3 sizing (AQP:533); see OI-3.

---

## 6. Mutation and seeding (Q3, Q4)

### 6.1 Mutation families

A mutant is a candidate case only (AQP:271). Each family is a deterministic generator over sites chosen by a harness-owned syntactic enumerator. It is independent of the product's providers.

| Rule | Families (the **held-out** family is chosen by the freeze seed) | Expected answer |
|---|---|---|
| `ws-unreferenced-export` / `unused-export` | `EXP-ADD` (add an export with a fresh, lexically unique name); `REF-DEL` (delete the last in-universe reference); `REEXP-DEL` (remove one link of a re-export chain); `IMPORT-RETARGET` (move an import to a sibling export) | positive |
| `unimported-file` | `FILE-ADD`; `IMPORT-DEL` (remove a file's only import) | positive, or must-abstain under L-FW1 |
| `rs-workspace-unreferenced-pub` / `rs-unused-pub-item` | `PUB-ADD`; `USE-DEL` (remove the only cross-crate use); `CFG-HIDE` (move the only use under a non-selected cfg) | positive in the selected configuration |
| `unused-dependency` | `DEP-ADD`; `DEP-USE-DEL` | positive |
| `module-import-cycle` | `CYCLE-CLOSE`; `CYCLE-BREAK` | positive / negative |
| `unresolved-import` | `SPEC-BREAK` | positive |
| `boundary-violation` | `LAYER-CROSS` | positive once declared |

**Fix reversals** are documented dead-code, unused-dependency and cycle fixes from the pinned repositories' history, reverted. **Negative lookalikes** are the §2.2 lookalikes placed in real code (AQP:279). Both are case origins of their own, not mutation families.

At least one family per rule is held out for acceptance with the held-out repositories (AQP:280). It is named in the freeze, and its instances are generated only for the acceptance round.

### 6.2 Validation steps

Each mutant records its subject, the unmutated control, the expected introduced difference, the selected configuration and its expected answer (AQP:271-276). It is then validated:
1. **Applicability.** The site lies in a selected target, under the selected cfg and features, and inside the analyzed universe.
2. **Well-formedness.** The mutant parses with the pinned grammar. For TS/JS, the pinned TypeScript compiler type-checks it without emitting; this executes no repository code. For Rust, nothing that would run build scripts or proc-macros is used (`M3-PLAN.md:355`), so a Rust mutant has no compile check at M3. Compile validation waits for the authorized execution path in QD-17. Any tool used here carries the same non-execution canary pin as QD-17.
3. **Independent proposition check** (AQP:278). Simple families (`EXP-ADD`, `PUB-ADD`, `FILE-ADD`, `DEP-ADD`, `SPEC-BREAK`) have a mechanical validator: the name is lexically unique in the universe, the module is not star-re-exported into a published entry point, the crate is not a library's public surface (for gating rules), and so on. Every other family is adjudicated under §4, and its label settles the expected answer.
4. **Validator audit.** For each mechanical validator, the harness audits a sample (10% and at least 20 per family and round) by adjudication. One disagreement suspends the validator for that family until it is fixed. Mutants it validated in that round are then adjudicated individually.

### 6.3 Accounting

Every generated mutant ends in exactly one state (**QD-16**):
- `valid-positive`, `valid-negative`, `valid-abstain`;
- `invalid` (fails the proposition);
- `equivalent` (no semantic change);
- `not-enumerated` (outside the selected configuration);
- `ill-formed` (fails step 2);
- `unvalidatable` (would need repository-code execution).

All counts are reported per family (AQP:278). Only the three `valid-*` states become cases. Invalid states never become misses and never disappear from the totals.

---

## 7. The cross-tool differential (discovery only)

**Tools.** Knip and ts-prune for TS/JS; rustc `dead_code`/`unused`, cargo-udeps and cargo-machete for Rust (AQP:283). Each is pinned by version, executable-closure digest, compiler, configuration and adapter digest (AQP:283), and recorded in the envelope's `tools` list with role `differential`.

**Repository-code execution (QD-17, revised for C2-Q0-R1-04).**
- **The M3 rule.** At M3 no repository code executes (`M3-PLAN.md:355`; prepared mode imports, `M3-PLAN.md:301`). The harness is bound by the same rule.
- **What runs at M3.** Only a tool **mode** whose pin verifies that no repository code executes. The pin records the mode, its flags, and a **non-execution canary check**. The tool is run, in that mode, on a harness-owned canary fixture whose `build.rs`, proc-macro, package scripts and JS/TS configuration files would each write a distinct marker file, and whose formatter and linter plugins would do the same. The pin is accepted only if no marker appears. The canary fixture is harness-authored, not repository code, and it is re-run whenever the pin changes. A tool with no verified non-executing mode does not run at M3. `executesRepositoryCode` is recorded as `false` for every tool used at M3 (ENV `tools`).
- **Expected outcome, to be confirmed at pin time.** cargo-machete (lexical) and ts-prune are candidates for a verified mode. rustc's `dead_code`/`unused` lints through a build, and cargo-udeps, build the crate, which runs build scripts and proc-macros, so they have no M3 mode. Knip qualifies only if a mode without configuration or plugin loading passes the canary.
- **Deferred, not conditional.** Executing differentials and Rust compile validation (§6.2) are deferred to the later explicit authorized execution path: M5's `execution.rs` under the `RepoExecutionGrantV2` and the M5-EX successors (`M3-PLAN.md:319`, `M3-PLAN.md:347-352`), on public T2 bytes only, never T3. O7 confinement or a disposable container is an **additional** condition on that later execution. It is never the authorization or the milestone gate.
- See OI-6.

**Why a tool is not an oracle.**
- The tools answer different propositions. rustc's `dead_code` is crate-local and does not see cross-crate `pub` use, which is where OpenSIP adds value (AQP:186). cargo-machete is lexical. Knip uses its own entry-point heuristics.
- They have their own false positives, and their answers depend on configuration.

A tool's output is therefore never an oracle and never G13 evidence (AQP:290-291). The tools run only inside the harness, never as a product dependency or fallback (AQP:291).

**From disagreement to curated case:**
1. **Normalize.** Each tool's finding is mapped to a catalog proposition through that tool's published proposition mapping, or marked non-overlapping (AQP:284).
2. **Compare** against OpenSIP's result on the same case key (§1.2).
3. **Adjudicate** every normalized disagreement under §4 into one of four classes (AQP:285-289): `confirmed-comparable-defect`, `other-tool-false-positive`, `semantic-non-overlap` or `unresolved`.
4. **Curate.** Only a confirmed comparable defect becomes a case: `origin=curated-differential`, with its expected answer taken from the settled label and a ledger reference (AQP:290). It joins the **next** frozen round (§1.5). It is held out only if its repository is held out and unexposed (QD-23). Adjudicating a held-out repository's differential during development exposes it.

---

## 8. Refactor and determinism suites (Q5)

### 8.1 Transformations

Each transformation is a pinned generator (AQP:308). The formatters run with harness-owned configuration, so no repository formatter plugin is loaded.

| ID | Transformation | Expected mapping |
|---|---|---|
| `R-FMT` | Reformat with the pinned rustfmt or Prettier | all subjects unchanged |
| `R-ORDER` | Reorder top-level declarations that have no initializer side effects | unchanged |
| `R-MOVE` | Move a module and rewrite every specifier or `mod` path | subjects moved |
| `R-RENAME-UNRELATED` | Rename a symbol that is not a finding's subject or in its evidence. TS uses the pinned TypeScript language service's rename. Rust is limited to private items with a lexically unique name in their file. | renamed symbol changed; all others unchanged |
| `R-ADD-UNRELATED` | Add a self-contained module | expected new findings, which are correct CODE-NET-NEW; all others unchanged |
| `R-SPLIT` | Split a file, re-exporting from the original | subjects moved |

### 8.2 The independent mapping oracle

For each pair, the generator emits a mapping: unchanged, changed, moved or renamed subjects, and the expected differences in facts, findings and Coverage (AQP:308). A second, independent derivation must agree with it. That derivation is a harness-owned declaration matcher over the before and after trees, comparing declaration signature tokens and the path-move map, and it shares no code with the generator. Any disagreement goes to human review. The reviewed mapping is digested into the `refactor-pair` case.

### 8.3 Validation and comparison

**Validation** (AQP:309). Before scoring, the pair must preserve, modulo the mapping:
- import resolution, read from the pinned TypeScript compiler's program file list and resolved modules for TS, and from the harness's syntactic `mod` tree with an unchanged Cargo manifest for Rust;
- recognized entry points;
- prepared-output freshness. In prepared mode, the harness recipe regenerates the imported set (`M3-PLAN.md:163`).

A pair that fails is recorded with its reason and discarded, never scored.

**The restricted Rust domain (N05).** A syntactic `mod` tree plus an unchanged manifest does not establish that `use` resolution, cfg selection or macro expansion is preserved. A Rust pair is therefore eligible only when the transformation cannot affect them:
- formatting;
- reordering items with no attributes and no macro invocations;
- renaming a private item that is not referenced from any macro body, cfg-gated item or `use` path.

Any other Rust pair whose independent resolution invariant cannot be established is recorded as `unvalidated` and discarded, never scored. Expanding the semantic oracle is part of the full Q5 suite at M5 (AQP:493).

**Comparison** is against the oracle, not `finding-key2` alone (AQP:310-314):
- finding content: message parameters, severity, and evidence references mapped through the oracle;
- relevant proofs and Coverage;
- zero spurious CODE-NET-NEW and zero spurious CODE-FIXED (WS:352-353);
- ambiguous and unmatched findings counted explicitly (IE:1563-1567).

**Survival** is the share of oracle-unaffected findings that survive with matching correspondence, reported per rule × transformation (AQP:315). A pair with fewer than 20 unaffected findings is `insufficient`, never passing (AQP:315).

**Moved and renamed subjects** are reported but not scored for survival until D7's declaration mechanism exists (AQP:316, AQP:538). The full suite runs at M5 (AQP:493); at M3, K1 builds the driver and §8.4 runs.

### 8.4 Determinism checks

These run at M3 (AQP:490). They use identical semantic input closures, run repeatedly (AQP:319), with these variants (**QD-18**):

| Variant | What changes |
|---|---|
| V0 | baseline, 5 repeats |
| V1 | fresh corpus copies written in reverse path order |
| V2 | concurrency 1 against automatic |
| V3 | different scratch root, `TMPDIR` and harness `HOME` |
| V4 | different locale, `TZ` and umask |
| V5 | compatible runner lanes. Deferred while M3 claims only this host's platform family (`M3-PLAN.md:306`). |

**Comparison:**
- When the PlanIds are equal, every identity the contract derives from Plan-bound inputs must be byte-equal: scope, fact, Coverage, view and finding (IE:183-190).
- When an identical input closure gives a different PlanId within one lane, that is itself a determinism failure.
- Across lanes, only canonical semantic payloads and correspondence are compared. IDs are not expected to match across different Plans (AQP:320).
- Per-invocation identifiers (RequestId, ExecutionId) and timings are excluded.

Any difference fails; Q5 determinism is exact (AQP:145). This tests the obligation of independent replay across machines (IE:1806).

---

## 9. Performance (Q6)

### 9.1 Workloads

The T2 manifest pins one **workload manifest** per repository (AQP:342-347). It records:
- source counts by class: hand-written, generated, vendored and excluded;
- shape: files, packages, import and reference edges, and dependencies;
- the selected rules, cells and configuration;
- the exact cold and warm reset and priming steps (§9.2);
- the start and end events of each run.

**Workflows** (AQP:351-354):
- `core-analyze`, with inputs prepared;
- `first-use`, from a clean checkout with no OpenSIP state, including OpenSIP-driven preparation;
- `prep-invalidating-edit`.

The edit taxonomy follows INC-4's sequences (AQP:391): body-only, exported signature, import, feature/config, generated input, insert/delete, missing input, and a newly introduced dynamic edge.

**Controls:** clean, missing input, stale prepared output, and broken or partial build. Each control reports how far the unaffected units progressed, and yield always appears beside time (AQP:358). The user's own `cargo build` is reported separately and never counted (AQP:356).

### 9.2 Cold and warm resets

**Cold** (LQM:923; AQP:330). Before **every** run, warmups included, the harness:
- deletes the project's OpenSIP state and the disposable analyzer caches;
- starts a new process;
- records the OS page-cache state.

Warmups therefore never turn cold samples warm. The page cache is never claimed flushed unless that is verified (LQM:923), so the label is "cold OpenSIP state, page cache recorded".

**Warm, with retained evidence** (LQM:924). The harness runs one priming invocation on the same inputs. Each later run is a new process with the declared caches retained and no reused provider process. Cold and warm are separate fixtures (AQ:279-280).

**Order.** reset → 3 warmups → 7 measured runs, as RS3 requires (`warmupRuns` const 3, seven samples; RS3:78-101).

### 9.3 Elapsed time and peak memory

**Elapsed** is measured on a monotonic clock, from spawn to the **settlement** of the workload tree (step 5). Settlement always means that the top process has exited and every descendant has been reaped. When a run leaf exists, it also means that the leaf reports `populated 0`. A slot with no leaf settles by reaping alone (C2-Q0-R10-02). It is recorded as positive integer nanoseconds (AQ:268-269). The cell statistic is the median, `sorted[3]` (PQV:28).

**Peak memory (QD-32, lead decision, following the amended quality plan, r5 §5.1 as corrected in r6).** On Linux, each run's peak-memory figure is **`cgroupMemoryPeak`**: the kernel's high-water mark of memory **charged to the run's dedicated cgroup v2 leaf**, read from `memory.peak` (AQP6:335-336). It includes page cache and kernel memory charged there. It is not resident set size, and it is neither a superset nor a sum of per-process RSS (AQP6:336-340). It is **never** called RSS. The cell statistic is the maximum of the seven run values (AQ:270; PQV:28). A run whose figure cannot be established is `incomplete` (§9.5), and nothing is ever filled in.

**The decision, and what it replaces.** r2–r8 tried to deliver r4's larger-of-two RSS rule: the concurrent summed RSS, and the sum of per-process own high-water counters (`PLAN-r4.md:327`; LQM:925). The per-process half needed complete, correctly attributed counters for every process.
- r2–r7 used kernel event channels: the process-event connector and taskstats, with a census, fences and per-CPU sequence proofs.
- r8 used ptrace exit stops.

Every round still had loss or attribution gaps (C2-Q0-R2-01, R4-01, R5-01, R6-01, and R8-01 to R8-04). The lead amended the quality plan instead (AQP r5 §5.1, AQP:331-338; corrected in AQP6:335-346). Two alternatives were rejected (AQP6:344-346):
- **More ptrace rounds.** R8-01 to R8-04 showed that tracing still has to handle untraced clone paths, exec-entry reads that are not final counters, and shared address spaces after `CLONE_VM` or `vfork`, each of which needs further design.
- **r4's larger-of-two rule**, with a sampled concurrent sum, which can miss short peaks.

The kernel maintains `memory.peak` for everything charged to the group, so it needs no tracing, event channels or per-process attribution. Whether it satisfies AQ's "peak RSS bytes" (AQ:268-272) for G13 qualification is D13's question (AQP6:343; OI-2).

*Linux, the D12 reference platform (AQP:543).* For each **measured run**, warmups included:

1. **Host checks, once per batch, before any run leaf is created.** If any check fails, every run in the batch is `incomplete` with the stated reason. **No run leaf is created** for that batch: each run proceeds without one, its elapsed value is kept, and its `cgroupLeaves` row is absent with the failing reason (§9.5). The checks that can fail here are:
   - cgroup v2 present;
   - `memory.peak` supported;
   - delegation;
   - `nsdelegate` on the mount (`cgroup-escape-unprevented`);
   - the batch-start check that the measurement uid has no outside process except the harness and its driver (`cgroup-isolation-unverified`).

   The `memory.peak` probe uses a separate test cgroup, which is not a run leaf and is removed before the batch.
   - **cgroup v2.** The harness finds a `cgroup2` mount in `/proc/self/mountinfo` and the `memory` controller in the delegated parent's `cgroup.controllers`. A host with only cgroup v1 (or a hybrid with `memory` on v1) is `cgroup-v1-only`. No `cgroup2` mount at all is `cgroup-unavailable`.
   - **Kernel support.** `memory.peak` exists for cgroup v2 from Linux 5.19. The harness checks that the file exists in a test leaf, and if it does not, the result is `cgroup-unavailable`. AL2023's kernel (6.1) has it, but writing `memory.peak` to reset it needs a later kernel, so r9 never resets: it **recreates** the leaf for every run (step 2). `clone3` with `CLONE_INTO_CGROUP` (Linux 5.7) and `cgroup.kill` (5.14) are also available on 6.1. The kernel release is recorded in `runner.calibration`.
   - **Delegation and permissions.**
     - The harness runs inside a delegated subtree. Under systemd that is a scope or service with `Delegate=yes`.
     - The harness's own processes sit in a sibling leaf, not in the parent, because of cgroup v2's no-internal-process rule.
     - The harness must be able to: write `+memory` to the parent's `cgroup.subtree_control`; `mkdir` and `rmdir` a child; and write the child's `cgroup.procs`. Moving the root also needs write access to `cgroup.procs` of the common ancestor of the source and destination cgroups.

     Any failure is `cgroup-no-delegation`.
   - **Escape prevention: the namespace.** A process with the same uid as the delegated subtree could write its own pid into another cgroup's `cgroup.procs`, and the leaf would then become empty without showing the escape. So the workload root starts in a new **cgroup namespace** rooted at the leaf (`CLONE_NEWCGROUP`), on a `cgroup2` mount with the `nsdelegate` option (checked in `mountinfo`). Under `nsdelegate`, a cgroup namespace is a delegation boundary for migrations made from inside it. A mount without `nsdelegate` is detected by the batch checks, before any leaf exists, and gives an absent leaf. A namespace that fails to be created in a launcher is detected **after** that run's leaf exists, and gives a created leaf with the same reason, `cgroup-escape-unprevented`.
   - **Isolation and control ownership (QD-33, for C2-Q0-R9-01).** A namespace alone does not hold. A descriptor opened outside the namespace keeps its opener's namespace and credentials, and the existing mount still exposes the delegated parent's writable `cgroup.subtree_control`. A `-memory` then `+memory` cycle there would recreate the leaf's controller state and lose its high-water. So the launcher, a harness-owned child that becomes the workload root at exec, establishes all four of these before exec:
     1. **The launcher's position.** It is created in the leaf with `clone3(CLONE_INTO_CGROUP)`. It then calls `unshare(CLONE_NEWCGROUP | CLONE_NEWNS)`, so the namespace root is the leaf, and makes every mount private.
     2. **A read-only, leaf-only cgroup view, by removal and not overmount (C2-Q0-R10-01).** Mounting over the inherited `cgroup2` mount would leave it in the stack, and `mountinfo` would still list it. So, inside its private mount namespace, the launcher:
        - first changes its working directory to the workload's directory, which is outside cgroupfs;
        - then **detaches every inherited cgroup mount**, every `cgroup2` and any `cgroup` (v1) entry, including aliases and bind mounts wherever they are mounted. It works from its `mountinfo`, innermost first, with `umount2(…, MNT_DETACH)`. A detached mount leaves the namespace's mount tree. Its only remaining references would be open descriptors or working directories inside it, and item 3 closes the descriptors;
        - then mounts a fresh `cgroup2` at `/sys/fs/cgroup` with `MS_RDONLY`, which inside the cgroup namespace shows only the leaf.

        **The invariant over the remaining mounts.** The launcher re-reads `/proc/self/mountinfo` and requires exactly one cgroup-type entry: the new `cgroup2` mount at `/sys/fs/cgroup`, read-only, with root `/` (the leaf), and no `cgroup` v1 entry. A detach that fails, a mount that fails, or any other cgroup entry still present gives `cgroup-isolation-unverified`, so the run is incomplete. On the ordinary delegated D12 layout this setup leaves exactly one entry, and the check passes. The workload therefore cannot write any control file, including the leaf's own and any ancestor's.
     3. **A descriptor allowlist.** The allowlist is the three standard streams, which are pipes to the harness, and nothing else. The launcher closes every other descriptor with `close_range(3, ~0U, 0)`, and every harness descriptor is opened `O_CLOEXEC` as a second line of defence.
        - **The audit.** The launcher opens `/proc/self/fd` as descriptor *a*, which is `O_CLOEXEC`, and requires the listed set to be exactly {0, 1, 2, *a*}. It then closes *a*, so the set carried into exec is exactly {0, 1, 2} (C2-Q0-R10-N02).
     4. **No path back through other processes (refined for C2-Q0-R10-N01).**
        - **The outside set** is exactly two processes, the harness and its batch driver. Each sets `PR_SET_DUMPABLE` 0 at its own start, before any batch, so its `/proc/<pid>/root` and `/proc/<pid>/fd` are closed to the workload.
        - **They never call exec during a batch.** An exec would reset dumpability before the new image runs, and would open a window. They create other processes only as launchers, which leave the outside set and become workload roots in a leaf.
        - **The check.** The batch-start check requires that no other process of the measurement uid exists. The harness repeats it after every run's settlement. A same-uid process outside the leaf found then, or any outside-set exec recorded during the batch, gives `cgroup-isolation-unverified` for that run.

     After these checks the launcher drops every capability (the effective, permitted, inheritable, ambient and bounding sets, with locked securebits) and executes the workload.

     **Continuous ownership.** The harness opens the leaf's directory with `O_PATH | O_DIRECTORY` when it creates the leaf, and holds that descriptor for the whole run. Every control operation it makes (entry, `cgroup.events`, `memory.peak`, `cgroup.kill`) goes through `openat` on that descriptor. The harness is the **only writer**: it enables `+memory` on the parent once per batch, before any run, and makes no other `subtree_control` change while a run is live. Controller continuity rests on that rule plus the isolation in items 1–4. **The endpoint checks below cannot detect a disable and re-enable cycle,** and are not claimed to (C2-Q0-R10 review). At the read, as consistency checks only, it verifies through the held descriptor that:
     - the leaf's inode equals the one recorded at creation;
     - `memory` is still listed in the leaf's `cgroup.controllers` and in the parent's `cgroup.subtree_control`.

     **Unverifiable means incomplete.** If any of items 1–4 or the ownership checks fails or cannot be evaluated, the run is `incomplete` with the reason `cgroup-isolation-unverified`, and its memory sample is null (§9.5). The workload's environment otherwise stays the same: only its view of cgroupfs and its inherited descriptors change. K1c's determinism comparison checks that results are unchanged.
2. **A fresh leaf per run.** The harness creates `run-<batchId>-<slot>` with `mkdir`. A new cgroup's `memory.peak` starts from its own charges, so no peak carries over between runs. A leaf is never reused.
3. **Into the leaf before exec.**
   - **Preferred.** The launcher, which becomes the root, is created directly in the leaf with `clone3(CLONE_INTO_CGROUP)`. That **places** it in the leaf for all later accounting. It does not move charges that already exist (C2-Q0-R9-02). Pages inherited from the harness before exec stay charged to their owner, and `exec` then drops that inherited address space.
   - **Fallback.** The child blocks on a pipe. The parent writes its pid to the leaf's `cgroup.procs` through the held leaf descriptor, and verifies the leaf path in `/proc/<pid>/cgroup` before releasing it. Charges made before the migration stay with their owner. The QD-33 steps then follow, and then `exec`.
   - The method used is recorded (`cgroupEntry: clone-into | migrate-before-exec`).
4. **Containment during the run.** Every descendant inherits the leaf. The namespace, the read-only leaf-only mount, the descriptor allowlist and the non-dumpable outside processes (QD-33) together prevent leaving it, and prevent changing its controllers. No per-process tracking is needed.
5. **Settlement, after the tree exits (C2-Q0-R9-N02; no-leaf case for C2-Q0-R10-02).** Before forking the launcher, the harness sets `PR_SET_CHILD_SUBREAPER`, so every orphaned descendant, including a daemonized one, is reparented to the harness and reaped by it. Zombies are not listed in `cgroup.procs`, so emptiness alone does not prove settlement. The workload root is also placed in its own process group and session at launch.
   - **Settled, with a run leaf,** means both:
     - the harness has reaped the root, and `waitpid` reports no remaining children (`ECHILD`);
     - `cgroup.events` shows `populated 0`.
   - **Settled, without a run leaf** (absent-leaf slots, §9.5), means the first condition alone: the root has been reaped and `waitpid` reports `ECHILD`. No cgroup interface is consulted.
   - **Drain, with a leaf.** The harness waits for settlement up to a preregistered drain limit (default 10 s). If the tree has not settled by then, it kills the leaf with `cgroup.kill`, reaps everything, and records `cgroup-not-empty`. The run did not end within the elapsed definition, so its elapsed value is invalid too (§9.5).
   - **Drain, without a leaf.** The same limit applies. At the limit, the harness signals the root's process group with `SIGKILL`, reaps what it can, and records **`settlement-failed`**, which nulls both values. A descendant that left the process group cannot be guaranteed killed, and that is disclosed in the reason's definition.
   - **Read.** The harness then reads `memory.peak` once through the held leaf descriptor, as an integer number of bytes. A failed or malformed read is `cgroup-read-failed`.
   - **Verify empty.** `cgroup.procs` must be empty, and `populated` must still be 0.
   - **Remove.** The leaf is then removed with `rmdir`. A failed `rmdir` is recorded as a defect, and the run is still complete if steps 1–5 passed.
6. **What the figure includes, disclosed (aligned with AQP6:336-340, C2-Q0-R9-02).** It is the peak of memory charged to the leaf: anonymous memory the workload allocates there, page cache it faults in first, and kernel memory charged there. Memory is charged to the cgroup that first touched it.
   - **Pages charged elsewhere are not counted,** even when the workload maps them. That includes cache populated by an earlier run or outside the leaf, memory first touched outside the leaf, and pages inherited before exec.
   - **Shared pages are charged once.**

   So the figure is not a bound on any RSS definition, and r9's claim that it is never smaller than anonymous resident memory is withdrawn. Cold and warm runs can differ in charged page cache. The cold reset records the page-cache state, and never claims it was flushed unless that is verified (LQM:923, §9.2). Charge ownership is part of a baseline's basis (§9.5).

*Per-process maxima, informational only (AQP:333).* When the host reaps a supervised child, it records `wait4` `ru_maxrss` (KiB on Linux, bytes on macOS) in its operational record (OPP:249), with the child's pid and role. The value covers that child and any descendants it has reaped, so it is labelled `hostReapedMaxRss`. It is never summed, never joined to the cgroup figure, and **never a budget input**. It is reported in the envelope as an operational-record digest (`operationalRecords[].carriesProcessMaxRss`). The r5–r8 host-join machinery (start-identity keys, namespace checks, `host-join-unresolved`) is withdrawn, because nothing is joined any more.

*macOS (lead workstation, and the later macOS lanes)* has no equivalent group high-water mark (AQP:334). Every macOS run records `cgroupMemoryPeakBytes` as null, with the reason `memory-peak-unavailable-platform`. Its memory figure is `incomplete`, and it can never be within budget. The informational `ru_maxrss` values are still recorded. A macOS group-peak source is needed before any macOS G13 lane can qualify memory (OI-18).

**Calibration (K1c), on the D12 image.** These cases are expected to be **complete**, with the right value:
- **A known allocation.** A fixture touches a known number of anonymous bytes **after entering the leaf** and exits; `memory.peak` must be at least that.
- **Inherited pages not counted.** The harness touches a large buffer before forking the launcher. The figure must not include it, which shows that the disclosure (step 6) is accurate.
- **Unavailable Linux and macOS:** absent leaves, known elapsed values (settled by reaping), and memory null with the platform or host reason.
- **A short-lived grandchild.** It allocates a peak and exits within 1 ms, and the peak is still captured. The mark is kernel-maintained, so no sampling is involved.
- **A daemonizing grandchild.** It double-forks and is reparented, stays inside the leaf, and is drained or killed as in step 5.
- **A fresh leaf per run.** Two consecutive runs with different peaks each report their own peak; no peak carries over.
- **Unchanged confinement.** Under the confinement profile, a child's denials still hold in the leaf.
- **Determinism.** Results are equal with and without the cgroup namespace (§8.4).

These cases are expected to be **`incomplete`**, with the stated reason:
- a host with cgroup v1 only: `cgroup-v1-only`;
- `memory.peak` removed or unmounted (simulated): `cgroup-unavailable`;
- a parent without write access to `cgroup.subtree_control`: `cgroup-no-delegation`;
- a `cgroup2` mount without `nsdelegate`, or a failed namespace creation: `cgroup-escape-unprevented`;
- a deliberate self-migration attempt under `nsdelegate`, which must be **refused** by the kernel; the run itself must then be unaffected;
- an **inherited descriptor**: a writable sibling `cgroup.procs` descriptor, opened outside the namespace and left open. `close_range` must close it, and the `/proc/self/fd` check must pass. With the close disabled in test mode, the check must fail with `cgroup-isolation-unverified`, and the run must never be complete;
- **the ordinary inherited writable mount (C2-Q0-R10-01, expected complete):** the D12 layout's writable `cgroup2` mount at `/sys/fs/cgroup` is detached in the launcher's namespace. The re-read `mountinfo` shows exactly one read-only, leaf-rooted `cgroup2` entry, and the run completes;
- **a writable alias bind-mounted elsewhere** (for example `/mnt/cg`): it is detached too. With detaching disabled in test mode, the invariant must fail with `cgroup-isolation-unverified`;
- **a missing `nsdelegate` at batch start (C2-Q0-R10-02):** no leaf is created. Each row is absent with `cgroup-escape-unprevented`, elapsed is kept, and settlement is by reaping;
- **a dumpable same-uid process at batch start:** no leaf is created. Each row is absent with `cgroup-isolation-unverified`, and elapsed is kept;
- **a no-leaf run with a stuck descendant:** `settlement-failed`, and both values are null;
- an **ancestor control write**: the workload attempts to write `-memory` to the parent's `cgroup.subtree_control`. It must be unreachable (`ENOENT` or `EROFS` in its view). With the read-only remount disabled in test mode, the mountinfo check must give `cgroup-isolation-unverified`;
- a **controller cycle forced by a harness test hook mid-run**: the hook is a write by the harness itself. The harness's sole-writer guard must record the violation and give `cgroup-isolation-unverified`, never a complete run with a lost high-water. The endpoint checks are not relied on to detect the cycle;
- a **same-uid outside process left dumpable**: the batch-start check must give `cgroup-isolation-unverified`;
- a **daemonized grandchild left as a zombie**: it is reparented to the harness and reaped, and settlement waits for `ECHILD`;
- a process left running past the drain limit: `cgroup-not-empty`;
- an injected read failure: `cgroup-read-failed`;
- a macOS run: `memory-peak-unavailable-platform`.

**Overhead.** The memory controller's accounting is active for every process on a cgroup v2 host, so moving into a leaf adds no measurement mode of its own, and QD-31's overhead rule is withdrawn. K1c still checks it by comparing elapsed time in the leaf with elapsed time in the harness's own cgroup on the calibration fixtures. It records the result in `runner.calibration.leafOverheadPpm`, for disclosure only.

### 9.4 Phase timings from the operational record

The harness reads each run's operational record (OPP:249). The record holds:
- phase spans: discovery, snapshot and sealing, Plan, each provider (start, analysis, teardown), admission and replay, evaluation, commit and delivery, and cache and reuse decisions (OPP:248);
- wall time, CPU time and peak RSS per process (OPP:249);
- the INC-8 reuse disclosure: which results were recomputed and which reused (AQP:399; OPP:249).

At M3 the record reaches the harness as internal instrumentation and the exploratory envelope (OPP:250). The harness checks that:
- every phase is present or marked not applicable;
- the spans nest correctly and are monotonic;
- the **unattributed** time, elapsed minus the sum of the top-level phases, is non-negative. It is reported, never dropped, because no OpenSIP work is excluded (AQP:349).

Reuse disclosure is stored only in the envelope's `operationalRecords`, never in a semantic result (AQP:399). A run with no record, or with a record that fails these checks, has null phase fields and a typed reason (`record-missing`, `record-invalid`, `phase-missing`, `negative-unattributed`); nothing is synthesized (ENV `q6`). Instrumentation stays at the same preregistered setting for every sample (OPP:251).

### 9.5 Statistics, budgets, incomplete measurements and continuous integration

**Budgets.** The §5.2 budgets apply per size class (AQP:362-369), with the product ratios against a reviewed baseline. A null baseline never qualifies a cell (AQ:272-276). The seven samples and their maximum are diagnostics only (AQP:339).

**Memory baselines must be charged-memory baselines (QD-34, for C2-Q0-R9-04).** The memory ratio, 1.25× (AQ:270), compares like with like. Its denominator is `baselineCgroupMemoryPeakBytes`: a reviewed baseline of the **same** quantity, `cgroupMemoryPeak`. Its **basis** is pinned by `baselineBasisDigest`, the digest of the reviewed baseline-advance record (AQP:500). That record must state:
- the measurement (`cgroupMemoryPeak`);
- the reset and cache policy (§9.2, and charge ownership, §9.3 step 6);
- the runner class and kernel release;
- the cgroup entry method.

An RSS baseline (`baselinePeakRssBytes`, r9 and earlier) is never used as a denominator, and the field is removed.

Without a compatible charged-memory baseline, a **complete** row's status is `no-baseline`: an **initial measurement**, never `within`. Any slot reason keeps the row `incomplete`, and that takes precedence. The validator checks the basis record against the row for compatibility on every field above: the measurement, the reset and cache policy with charge ownership, the kernel release, the runner class and the entry method (C2-Q0-R10-N04). The §5.2 absolute byte budgets are written for process-tree RSS (AQP:364-369). Comparing `cgroupMemoryPeak` against them is reported only as an informational, exploratory **absolute-charge comparison** (`absoluteChargeComparison`). It never sets the row's status until D13 decides equivalence (OI-2). Elapsed time keeps its own `baselineMedianNanos`.

**Complete and incomplete results (QD-25, for C2-Q0-R1-07).** Each workload, workflow, reset, control and batch result is either complete or incomplete.
- **Complete:** 3 warmups and 7 measured runs, with every elapsed value and every `cgroupMemoryPeakBytes` value present. Status is `within`, `over` or `no-baseline`.
- **Incomplete:** at least one slot (priming, warmup 0–2 or measured 0–6) has at least one typed reason. Reasons are carried in `slotReasons[]`, one row per affected slot, keyed by the typed run slot (`{slot, reasons}`; C2-Q0-R3-01). A warmup or priming failure therefore has its own carrier, and is never attributed to a measured position. The two measured series (elapsed and `cgroupMemoryPeakBytes`) keep their seven positions, with `null` where a value is unavailable.

**Reasons and the quantities they invalidate (QD-27, for C2-Q0-R3-02).** A reason makes a numeric sample null only if it concerns that quantity, and every known value is kept. The fixed mapping:

| Reasons | Quantities that are null in that measured slot | Quantities kept |
|---|---|---|
| `run-failed`, `timeout`, `cgroup-not-empty`, `settlement-failed` | elapsed and `cgroupMemoryPeakBytes` | none. A failed run's numbers are not samples. A run with processes left behind did not end within the elapsed definition (§9.3 step 5). |
| `cgroup-unavailable`, `cgroup-v1-only`, `cgroup-no-delegation`, `cgroup-escape-unprevented`, `cgroup-isolation-unverified`, `cgroup-read-failed`, `memory-peak-unverified`, `memory-peak-unavailable-platform` | `cgroupMemoryPeakBytes` | elapsed |
| `record-missing`, `record-invalid` | none | both. Only the operational evidence (phases, reuse disclosure and the informational per-process maxima) is missing, which shows as `phaseTimingsPresent: false` with a `phaseAbsenceReason` (§9.4). |

For warmup and priming slots no numeric samples are carried, so their reasons, typically `run-failed`, `timeout`, `record-missing` or `record-invalid`, affect only the batch's status.

A row is `incomplete` whenever **any** slot has a reason, **including a row in which every numeric sample is known**, such as one whose only defect is a missing warmup record. Status `incomplete` is never `within` and never counts toward Q6. The aggregates are kept when their inputs exist: the median when all seven elapsed values are present, and the maximum when all seven `cgroupMemoryPeakBytes` values are. Failed runs are kept, never dropped and never re-run to fill the slot.

**Batches (QD-20, revised for C2-Q0-R1-07).** Every result carries a `batchId` (SHA-256 of the canonical tuple of round, workload, workflow, reset, control and ordinal) and a `batchOrdinal`: 1 for the first batch, 2 for the CI retry. Both batches of a retry live in the same envelope.
- **The retry.** On a threshold failure or an incomplete result, CI runs one more full batch, as AQP:499 allows.
- **The final verdict** is the batch with the highest ordinal, whichever way it goes, and is marked `final: true`. Exactly one batch per key is final. A schema cannot express that cross-row rule, so the envelope validator checks it, together with the population sums (ENV `description`). The better batch is never kept by choice, and both batches are kept in the record.
- **The batch join (C2-Q0-R2-02).** Every piece of supporting evidence names its batch:
  - each `operationalRecords[]` row carries its `batchId` and a **run slot** (`priming`, `warmup` 0–2, or `measured` 0–6);
  - each batch has exactly one `batchObservations[]` row (§9.6), keyed by `batchId`.
- **What the envelope validator checks.** These are cross-row rules a schema cannot express:
  - **Identity.** Each `batchId` equals the SHA-256 of its canonical key tuple.
  - **Coverage.** Every Q6 row's batch has one observation row. Every warmup and measured slot (and the priming slot for a warm reset) has exactly one operational record, or the row is `incomplete` and its `slotReasons[]` row for that slot lists `record-missing`. A record that is present but fails §9.4's checks needs `record-invalid` on its slot.
  - **Uniqueness.** No two records share (`batchId`, slot), and no two `slotReasons[]` rows in a row share a slot.
  - **No orphans.** No record or observation row names a batch absent from `q6`.
  - **Sample consistency (revised for C2-Q0-R3-02).** For each measured slot and each quantity, the value is null **if and only if** that slot has a reason that the QD-27 table maps to that quantity. A reason that does not concern a quantity never nulls it.
  - **Aggregates.** The median is non-null exactly when all seven elapsed values are, and `maxCgroupMemoryPeakBytes` exactly when all seven peaks are.
  - **Leaf evidence (revised for C2-Q0-R9-03).** Leaf evidence comes from the **driver**, not from the product's operational record, so a missing operational record (`record-missing`) never removes it. The envelope carries one `cgroupLeaves[]` row per (`batchId`, slot) for every warmup, measured and priming slot. Each row has either:
    - a created leaf: `leafName` (`run-<batchId>-<slot>`) and `leafInode`, with `absentReason` null; or
    - no leaf: `leafName` null, and `absentReason` naming why. That reason must be one of the **batch-level, before-creation** reasons (§9.3 step 1; C2-Q0-R10-02): `cgroup-unavailable`, `cgroup-v1-only`, `cgroup-no-delegation`, `memory-peak-unavailable-platform`, `cgroup-escape-unprevented` (no `nsdelegate`) or `cgroup-isolation-unverified` (the batch-start outside-process check). The same reason must appear in that slot's `slotReasons`.

    The last two reasons can also arise **after** a leaf is created (a failed namespace creation, a failed mount invariant or descriptor audit, an outside exec). Those rows carry a `leafName`. The evidence records which case happened, and the validator never infers it. `cgroup-read-failed` and `cgroup-not-empty` exist only after creation and never appear in an absent row. A slot with no leaf settles by reaping (§9.3 step 5), and its elapsed value is kept unless a reason in the QD-27 table nulls it.

    Distinctness is checked **only among created leaves**: two rows naming the same leaf make the envelope invalid. A slot with no `cgroupLeaves[]` row also makes it invalid.
  - **Baselines.** A complete row whose status is `within` or `over` must carry non-null `baselineMedianNanos`, `baselineCgroupMemoryPeakBytes` and `baselineBasisDigest`. The referenced basis must match the row on the measurement (`cgroupMemoryPeak`), the reset and cache policy with charge ownership, the kernel release, the runner class and the entry method. Otherwise a complete row's status must be `no-baseline`, and an incomplete row stays `incomplete`.

  A violation makes the envelope invalid, not merely the row incomplete.
  - **Phase evidence.** `phaseTimingsPresent` is true exactly when every measured slot has a valid record. `phaseAbsenceReason` is null exactly when `phaseTimingsPresent` is true; otherwise it names the first applicable reason, in the order `record-missing`, `record-invalid`, `phase-missing`, `negative-unattributed`.
  - **Status.** A row with any slot reason has status `incomplete`, and a complete-variant row has no reasons.
- **Reference cases for K1c's validator (r4).** These were checked against ENV, plus a reference implementation of the QD-27 rule, while this record was drafted. That was a design check, not a product run.
  - **Accepted:**
    - a warmup-0 `record-missing` with all 14 measured values known;
    - a measured-0 `record-missing` that keeps both values;
    - `cgroup-read-failed` that nulls only the memory value and keeps elapsed and the median (re-expressed in r9 from r4's `event-loss` and r8's `own-counter-missing` examples);
    - `run-failed` that nulls both values in its slot.
  - **Rejected by the schema:**
    - empty `slotReasons`;
    - a slot row with no reasons;
    - warmup index 3;
    - the legacy `runReasons`;
    - a complete row that carries reasons;
    - a reasoned row that claims `within`.
  - **Rejected by the validator:**
    - `record-missing` that nulls a known elapsed value;
    - `cgroup-read-failed` that also nulls elapsed;
    - `cgroup-read-failed` that leaves the memory value present;
    - a null measured value with only a warmup reason;
    - duplicate slot rows.
- **Reference cases from r5 to r8 (superseded in r9).** The host-join, attribution, per-CPU and ptrace cases tested withdrawn mechanisms and are retained only in `DESIGN-r8.md`.
- **Reference cases added in r9 (QD-32).**
  - **Accepted by the schema:** each new reason, and a complete row carrying `cgroupMemoryPeakBytes` and `maxCgroupMemoryPeakBytes`.
  - **Rejected by the schema:**
    - each withdrawn reason (for example `tracer-died`, `own-counter-missing`, `host-join-unresolved` and `event-loss`);
    - the withdrawn fields `ownHighWaterSumBytes`, `concurrentSumPeakRssBytes`, `peakRssBytes`, `rssCollection` and `rssBatchId`;
    - a calibration block carrying `yamaPtraceScope`.
  - **Accepted by the validator:** `cgroup-not-empty` that nulls both values, and `cgroup-escape-unprevented` that nulls the memory value only.
  - **Rejected by the validator:** `cgroup-escape-unprevented` that nulls elapsed, and two slots naming the same created leaf.
  - **A reference model of the per-run cgroup procedure (step order 1–5).** It gives:
    - complete, on a clean run;
    - `cgroup-v1-only`, `cgroup-no-delegation` and `cgroup-escape-unprevented`, from the host checks;
    - `cgroup-not-empty`, on a drain timeout;
    - `cgroup-read-failed`, on a read error;
    - and it reads the peak only after `populated 0`.
- **Reference cases added in r10.**
  - **Leaf evidence (R9-03):**
    - accepted: an unavailable Linux host whose seven measured rows are `leafName: null` with `absentReason: cgroup-unavailable` matching `slotReasons`;
    - accepted: a macOS batch with `absentReason: memory-peak-unavailable-platform`;
    - accepted: measured `record-missing` with a created leaf still present, keeping both values;
    - rejected: a duplicate created leaf;
    - rejected: an absent leaf whose `absentReason` is not in the slot's reasons;
    - rejected: an absent leaf with a post-creation reason (`cgroup-read-failed`);
    - rejected: a missing leaf row.
  - **Baselines (R9-04):**
    - accepted: `no-baseline` with null charged baseline values;
    - accepted: `within` with a compatible charged baseline and basis;
    - rejected by the schema: the removed `baselinePeakRssBytes`;
    - rejected by the validator: `within` with a null charged baseline, and `within` with a basis declaring RSS or a different entry method.
  - **Isolation (R9-01):**
    - accepted: `cgroup-isolation-unverified` nulling memory only;
    - rejected: it also nulling elapsed.
  - **A reference model of the isolation checks:** the launcher passes only with fds equal to the allowlist, every `cgroup2` mount read-only and rooted at the namespace root, no dumpable same-uid outside process, and an unchanged inode and controllers at the read. Each injected violation gives `cgroup-isolation-unverified`.

- **Reference cases added in r11.**
  - **Mount setup (R10-01).** A model of the launcher's `mountinfo`:
    - the inherited writable `cgroup2` plus the fresh read-only mount after detaching gives exactly one entry, so the check passes;
    - overmounting without detaching leaves two entries and gives `cgroup-isolation-unverified`;
    - a writable alias that was not detached gives `cgroup-isolation-unverified`;
    - a cgroup v1 entry that was not detached gives `cgroup-isolation-unverified`;
    - a failed detach gives `cgroup-isolation-unverified`.
  - **Before-creation reasons (R10-02).**
    - accepted: absent rows with `cgroup-escape-unprevented` or `cgroup-isolation-unverified` that match `slotReasons`;
    - accepted: unavailable Linux and macOS with absent leaves and every elapsed value known;
    - rejected: an absent row with `cgroup-read-failed`, and an absent row whose reason is not in `slotReasons`.
  - **No-leaf settlement.**
    - a model gives `settled` once the root is reaped and `ECHILD`, without consulting the cgroup;
    - a stuck descendant at the limit gives `settlement-failed`.
  - **`settlement-failed` in the validator:** accepted when it nulls both values, rejected when it keeps elapsed.
  - **Baselines (N04):** a basis that differs in kernel release, or in cache policy, is rejected for `within`.
  - **The descriptor audit (N02):** the listed set {0, 1, 2, *a*} passes. After *a* is closed, the exec set is {0, 1, 2}.

- **Flips.** A non-pass followed by a pass is counted as a `flip`. Three flips in any ten consecutive CI runs of a workload send that workload to noise review.

**Baselines** advance only through a reviewed baseline-advance record (AQP:500).

### 9.6 The D12 reference runner

The requirements, for D12 (AQP:543):
- a dedicated 4 vCPU / 8 GiB worker, at concurrency 1 (AQC:138-141);
- one selected, signed platform-profile lane per report (AQ:228-230, AQ:238-239);
- no network.

It records the fields in `runnerRequired` (LQM:926-937): CPU model, OS version and build, kernel, filesystem, host and provider-closure digests, compiler and runtime digests, cache state and measurement-tool digest.

**Q0 adds (QD-21):**
- **Quiet.** No other lead run set (`M3-PLAN.md:270`), and a one-minute load average below 0.2 before each batch.
- **Fixed CPU frequency policy,** with swap and power state recorded.
- **Storage.** The corpus store is on the runner's local disk.
- **Kernel interfaces.** On Linux, kernel 5.19 or later for `memory.peak`; AL2023's 6.1 qualifies. It also needs a `cgroup2` mount with `nsdelegate`, a delegated subtree with the `memory` controller, and `CAP_SYS_ADMIN` for the launcher, held only to create the cgroup namespace (§9.3). The §9.3 calibration must have passed.
- **Carrier (N04; batch-scoped for C2-Q0-R2-02).** Each batch records its observations in its own `batchObservations[]` row, keyed by `batchId`. That row holds: load average before the batch (milli-units), CPU frequency policy, swap bytes in use, power state, whether the corpus store is on local disk, and the online-CPU set before and after. The §9.3 calibration results are per runner and toolchain, so they stay in `runner.calibration`: kernel release, `memoryPeakVerified`, `nsdelegate`, `cgroupEntry` and the disclosure-only `leafOverheadPpm`.

**Labelling.** Samples from any other machine are labelled `lead-workstation` or `ci` (ENV `runner.runnerClass`) and are never Q6-labelled (`M3-PLAN.md:158`). For qualification at M6, the runner's identity and keys are authenticated under AQ:191-198; exploratory runs don't need that.

---

## 10. The corpus fetch and store

`corpus fetch` is a harness command, never a product command (AQP:209). It is the only networked step.

**Steps.** For each manifest entry `{repository URL, commit, treeDigest, licence, family, heldOut, submodulePolicy}`, the harness:
1. fetches exactly that commit, shallow;
2. materializes it into the content-addressed store at `store/<treeDigest>/`;
3. verifies the digest, then makes the tree read-only.

**The tree digest (QD-22)** is the SHA-256 of the canonical JSON array of `[path, mode, sha256(content)]`, sorted by path bytes. It is independent of Git's object hash. The manifest also records the Git tree ID, for cross-checking.

**Submodules and LFS** are either pinned explicitly in the manifest or excluded explicitly. A missing pinned object fails the fetch.

**At run time:**
- Every exploratory and qualification run takes the store as a read-only input. It re-verifies the tree digests of the repositories it uses before starting, and refuses on a mismatch (AQP:209).
- Runs set `HOME`, the XDG directories, `CARGO_HOME` and the npm cache to per-run scratch directories, so that no tool reads the user's configuration or real home.
- No run path contains network code.

**T3** has its own local manifest and fetches from local paths. Its source never leaves the machine (AQP:207).

---

## 11. The exploratory envelope (D13)

The schema is drafted as ENV, `exploratory-quality-envelope.schema.v1.json`, beside this record. It is a **separate** carrier, because RS3 stays closed and unchanged (AQP:428).

| Requirement | Where ENV meets it |
|---|---|
| It references unchanged RS3-shaped observations by digest (AQP:429) | `rs3Observations[]`: `reportSha256`, `schemaId` const `opensip.qualification.product-report.3`, `signed` |
| It records the product commit, corpus and ledger digests, the scoring-harness digest, the runner and the tool versions (AQP:430) | `product`, `harness`, `corpus`, `ledger`, `runner`, `tools` |
| It pins every metric definition and denominator (AQP:431) | `definitions` pins the metric-definition, preregistration, rule-spec and rubric digests. Each measured section carries its own numerators and denominators: Q2 per stratum and per repository, with corpus, sampled, settled, pending and unlabelled counts and line counts by class; Q3 and Q6 yield counts; Q7 per-rule populations and score histograms. A measured section must carry them, enforced by the schema's `if`/`then`; not-measured stays explicit. (C2-Q0-R1-06) |
| It declares itself non-qualifying (AQP:432) | `standing` const `exploratory-never-promoted`; `qualificationEvidence` const `false` |
| D13's exploratory class for unqualified advisory rules (AQP:239) | `unqualifiedAdvisoryRules[]` |
| INC-8 provenance and phase timings, outside semantic Coverage (AQP:399; OPP:249) | `operationalRecords[]`, by digest, each joined to a Q6 batch and run slot (§9.5) |
| Incomplete performance results and retry batches (§9.5) | `q6.workloads[]` is a closed `oneOf` of complete and incomplete variants, with per-run nullable samples, typed `slotReasons`, `batchId`, `batchOrdinal` and `final` |
| Runner observations (§9.6) | `batchObservations[]` per batch; `runner.calibration` per runner |

**What a valid envelope does not do.** It is never a G13 input and is never promoted (AQP:434, AQP:442). Validating against ENV says nothing about whether the claims inside are true. Envelopes are signed only in the sense that their digests are pinned. They need no authenticated runner, because they claim nothing that requires one.

---

## 12. Report outputs and Q1–Q8

| Q | Envelope section | Reported values | Status values |
|---|---|---|---|
| Q1 | `q1.cells[]` | per cell: expected, actual, missing and extra counts and exit match, computed by the gate (PQV:24-27); the RS3 report digest | `exact`, `mismatch` |
| Q2 | `q2.strata[]`, `q2.repositories[]` | **Per stratum** (rule × language × mode × target × evidence set): estimand (`family-weighted`); method; *k*; corpus, sampled, settled, pending and unlabelled counts; true, false and unclear counts; the guard's verified and optimistic values; `censusPrecisionPpm` (null unless nothing is unlabelled or pending); the sample ratio (descriptive); resolved-label precision (descriptive, AQP:234); *L*; concentration (AQP:240); per-family *N_j*, *a_j* and true counts. **Per repository** (AQP:240, AQP:153): repository, commit, tree digest, family, evidence set, the same label and population counts, and analysed lines by class (hand-written, generated, vendored, excluded), with false positives split between hand-written and generated or vendored code, so that FP/KLOC and findings/KLOC can be recomputed from counts. False-positive cost (AQP:241) is carried as median triage time. | §5.6 |
| Q3 | `q3.strata[]` | answerable positives, hits, misses by cause (§1.3), abstentions on answerable cases, answerable negatives and determinate negatives, so that yield is determinate ÷ answerable (AQP:154), and mutant accounting by family (§6.3) | `measured`, `insufficient` (no answerable positives) |
| Q4 | `q4` | unsupported determinate negatives and false completeness claims (each must be 0; AQP:144), deficiency mismatches | `zero`, `nonzero` |
| Q5 | `q5.survival[]`, `q5.determinism[]` | survival per rule × transformation, with counts; spurious CODE-NET-NEW and CODE-FIXED; discarded and unvalidated pairs; determinism variant results | `measured`, `insufficient` (< 20); `exact`, `differs` |
| Q6 | `q6.workloads[]` | per workload × workflow × reset × control × batch: 7 elapsed samples and 7 `cgroupMemoryPeakBytes` samples (nullable only in the incomplete variant); the median elapsed and `maxCgroupMemoryPeakBytes`; `baselineMedianNanos`, `baselineCgroupMemoryPeakBytes` and `baselineBasisDigest` (QD-34); the informational `absoluteChargeComparison`; phase-timing state with a typed absence reason; unattributed time; yield as `determinateCases` ÷ `answerableCases`; runner class; `batchId`, `batchOrdinal` and `final`. Driver leaf evidence is carried in `cgroupLeaves[]` (§9.5). The informational per-process `ru_maxrss` values live in the digest-linked operational records. Q6 memory values are carried **only** in the envelope: no RS3-shaped Q6 report is produced until D13 decides whether `memory.peak` may fill RS3's `peakRssBytes` (AQP:335). | `within`, `over`, `no-baseline`, `incomplete` |
| Q7 | `q7.rules[]` (M4, D8) | per rule: finding population; sample size (50, or all findings if fewer, labelled `small-population`); fields required and present; proof joins checked and failed; score histogram for 1 to 5 and the score sum; items scoring ≤ 2 and their dispositions; gating or repair-eligible items in the sample and their dispositions; median triage time; accepted and dismissed counts (AQP:417-420) | `measured`, `not-measured` |
| Q8 | `q8.shapes[]` | manual corrections per pinned shape (SMAP:67; AQP:148) | `measured`, `not-measured` |

Time to first trustworthy result is reported under Q6 (AQP:155). Before D13's DR-G13 successor is accepted, Q2–Q8 are never qualification evidence (AQP:436-440).

---

## 13. Implementation units and K2 sizing

| Sub-unit | Contents | Size (`M3-PLAN.md:146-150`) |
|---|---|---|
| K1a | case and ledger libraries, canonical digests, the freeze, `corpus fetch` and the store (§1, §3, §10) | M |
| K1b | the confidence module: exact rational Clopper–Pearson, the product bound, status rules, and a self-test against §5.4 and §5.5's reference values | S |
| K1c | the run driver: resets, the per-run cgroup leaf procedure and `memory.peak` read (§9.3), operational-record ingestion, the determinism driver (§8.4, §9), and envelope emission | M |
| K2a | T1, TS/JS lane: 33 cells | XL part, 5 days |
| K2b | T1, Rust lane: 22 cells | XL part, 5 days |
| K2c | T1, syntax-only lane: 11 cells, per grammar (AQ:233-234) | 3 days |
| K2a-r, K2b-r, K2c-r | each lane's independence review and oracle freeze | 1 day each |

The cell counts are `M3-PLAN.md:58`. The T1 obligation is all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3 (AQP:490).

**K2 estimate: 16 days of serialized lane work** (5 + 5 + 3, plus 3 one-day lane reviews), using the plan's planning durations (`M3-PLAN.md:197-200`). This is a planning assumption, not a measurement. r1 counted 2 review days for all three lanes; r2 reviews and freezes each lane separately, so it costs one more day.

**The independence gate (QD-26, for C2-Q0-R1-08).** K2 is authored before the producers so that expected answers are independent (`M3-PLAN.md:172`). Finishing by day 21 does not by itself secure that, so the gate is per lane:
- **The freeze.** A lane's oracle is **frozen** by a ledger `freeze` record pinning its fixture-manifest and case-set digests, after its lane review. The review checks that no expected answer was derived from producer output.
- **The ordering.** The freeze must precede, in the ledger chain, the **first producer run on that lane's T1 fixtures**, and K2 authors never see producer output for those cells before it.
- **Enforcement.** The T1 runner refuses a lane that has no freeze. A producer may be *authored* earlier, and may be tested on its own unit fixtures, but it is not run on T1 fixtures before the freeze.

**The schedule against the M3 table (`M3-PLAN.md:202-227`).** The earliest producer activity in each lane sets that lane's deadline:

| Lane | Earliest producer activity on its inputs | Oracle frozen by | Placement |
|---|---|---|---|
| Rust (K2b) | G2-v, launch and validation from day 2 to day 3, after D1 (`M3-PLAN.md:210`, `M3-PLAN.md:215`) | before day 0 | **pre-day-0**: K2b + K2b-r, 6 days |
| syntax-only (K2c) | E2 parser work from day 3, after C2 (`M3-PLAN.md:206`, `M3-PLAN.md:212`) | before day 0 | **pre-day-0**: K2c + K2c-r, 4 days |
| TS/JS (K2a) | F1 from day 7, after C1, C2 and D3 (`M3-PLAN.md:213`) | end of day 6 | **days 0–6**: K2a + K2a-r, 6 days |

**Consequences.**
- **Pre-day-0.** 10 days of K2 join the pre-day-0 work, after Q0 is accepted, in parallel with S-M, T2b, S-P with G2 authoring, CF-P and L acceptance (`M3-PLAN.md:243-248`). If the other pre-day-0 items finish sooner, K2 becomes the latest pre-day-0 item, at Q0 + 10 days.
- **Days 0–6.** K2a has one day of margin before F1's day-7 start. If K2a-r slips, F1 may still be authored, but its first run on TS T1 fixtures waits.
- **Slip, computed through every dependency (C2-Q0-R2-03).** This record does not split F1's completion from its first T1 run, so conservatively a delay to that run delays F1's finish, and with it the whole F branch. Let *s* be the K2a freeze's slip past day 6, and *d* = max(0, *s* − 1) the resulting delay to F1. From the plan's rows (`M3-PLAN.md:208`, `M3-PLAN.md:213`, `M3-PLAN.md:217-227`):
  - F1 = 10 + *d*; F2 = 14 + *d*; F3 = 17 + *d*;
  - H = max(C4 = 12, F1) + 3; J2 = H + 3; J3 = max(J2, F2, G3 = 15) + 3; I2 = H + 2;
  - M3-M = max(J3, G4 = 18, F3, I2, K2 = 6 + *s*, …) + 3; M3-X = max(M3-M, R, J4 = J3 + 2, 23, O2_selected) + 2.

  r2 checked F2 against J3 alone and missed the path F1 → H → J2. With every other day-0 and branch assumption held (including O2_selected ≤ 24), the result is:

  | *s* (oracle slip) | *d* (F1 delay) | F1 | H | J2 | J3 | M3-M | M3-X |
  |---:|---:|---:|---:|---:|---:|---:|---:|
  | 0–1 | 0 | 10 | 15 | 18 | 21 | 24 | 26 |
  | 2 | 1 | 11 | 15 | 18 | 21 | 24 | 26 |
  | 3 | 2 | 12 | 15 | 18 | 21 | 24 | 26 |
  | 4 | 3 | 13 | 16 | 19 | 22 | 25 | 27 |
  | 5 | 4 | 14 | 17 | 20 | 23 | 26 | 28 |

  So **M3-X = 26 + max(0, *d* − 2) = 26 + max(0, *s* − 3)**. H's slack against F1 is 2 days (C4 finishes at 12 and F1 at 10), so 3 days of oracle slip fit (the 1-day margin plus 2), and every further day moves the host chain by a day. r2's "up to 4 days" is withdrawn.
- **If authoring and first T1 run are later split.** Should F1's law allow F1 to finish and feed H while only its T1 conformance run waits, H would no longer depend on the freeze. The slip would then reach M3-X only through F2, F3 and K2. That schedule is not assumed here, and OI-12 recomputes it if it is adopted.
- **Formulas with no slip.** K2 finishes by day 6. R = max(15, 6) + 2 = 17, and M3-M = max(21, 6) + 3 = 24, so the day-21 K2 condition (`M3-PLAN.md:233`) holds by construction.

**The M3-PLAN bounds to update under OI-12:**
- the K2 row (`M3-PLAN.md:222`): 16 days, 10 before day 0 and 6 by day 6;
- the R and M3-M rows (`M3-PLAN.md:225-226`): K2 = 6;
- the K2 clause of the condition (`M3-PLAN.md:233`, `M3-PLAN.md:239`);
- "K2's size" in the unbounded list (`M3-PLAN.md:241`): it is now bounded;
- the pre-day-0 list (`M3-PLAN.md:243-248`): add K2b and K2c, 10 days after Q0;
- F1's row (`M3-PLAN.md:213`): its first T1 run waits for K2a's freeze;
- the slip rule: M3-X = 26 + max(0, *s* − 3), for K2a freeze slip *s* past day 6, through F1 → H → J2 (C2-Q0-R2-03).

The rejected alternative was to delay every producer behind all three lane oracles. That would delay G2-v and E2 and lengthen the host chain.

---

## 14. Open items, with owners

| ID | Item | Owner | Blocks |
|---|---|---|---|
| OI-1 | **D13**: accept the exploratory envelope (ENV) | lead, owner sign-off (AQP:544) | S-M's report, M3-M (`M3-PLAN.md:158`) |
| OI-2 | **D13 successor**: the DR-G13/report/harness successor that carries this record's case model, ledger, confidence rule and oracles into qualification (AQP:436-440). Since r9 it also decides whether cgroup `memory.peak` satisfies AQ's "peak RSS bytes" (AQ:268-272; AQP:335). | Language quality + Product + Release engineering (QG:264) | Q2–Q8 qualification at M6 |
| OI-3 | **Q2 achievability** (§5.8): grow T2 held-out families toward *k*_min, or revisit D4 | owner (D4, AQP:534); lead (D3 sizing, AQP:533) | any Q2 PASS |
| OI-4 | The estimand: family-weighted, with the pooled guard (QD-11, QD-15), against finding-weighted | DR-G13 successor owners | Q2 qualification |
| OI-5 | Per-stratum against family-wise confidence across strata (§5.6) | DR-G13 successor owners | Q2 qualification |
| OI-6 | Differential tools and Rust compile validation that execute repository code (QD-17, §6.2) are outside M3. They wait for the authorized execution path: M5 `execution.rs`, `RepoExecutionGrantV2` and the M5-EX successors (`M3-PLAN.md:319`, `M3-PLAN.md:347-352`). Confinement is an additional condition, not the authorization. | M5-EX successor owners (`M3-PLAN.md:347-350`); lead | the Rust differential; Rust mutant compile checks (M5 or later) |
| OI-7 | **D12**: select the reference runner (§9.6) | release engineering; lead with owner sign-off (AQP:543) | Q6-labelled samples |
| OI-8 | Q3 and Q5 confidence statements. AQP sets point targets and a population floor of 20 (AQP:143, AQP:315); this record adds no bound. | DR-G13 successor owners | Q3/Q5 qualification |
| OI-9 | **D7**: declared correspondence for moved and renamed subjects (§8.3) | lead + identity owner (AQP:538) | Q5 at M5 |
| OI-10 | **D8**: explanation fields (Q7) | lead + reporting owner (AQP:539) | Q7 at M4 |
| OI-11 | The operational-record carrier after M3: S-OP-1 and S-OP-6 (OPP:250) | OPP §9 owners | M4 `--timings` |
| OI-12 | Fold K2's estimate and lane gates (§13) into M3-PLAN's bounds, as listed in §13 | lead | the M3 total |
| OI-13 | **D1**: QG items[12] still says "cold/warm p95" (QG:268). The harness follows AQ:268-282 and PQV:28. | lead (AQP:531) | record hygiene only |
| OI-14 | The expert roster and capacity (§4.6) | owner (`M3-PLAN.md:368`) | resolving gating labels |
| OI-15 | **D2**: where the catalog lives (§2) | lead + evaluator owner, owner sign-off (AQP:532) | the M5 product pack |
| OI-16 | Family assignment for each T2 entry (§5.3) | M3-T2 (lead), D3 sign-off | the freeze |
| OI-17 | A sample-based pooled-precision guard: per-family exact hypergeometric lower bounds at α/*k* (§5.6). Until it is approved, the conservative verified-true guard is in force. | DR-G13 successor owners (QG:264); lead proposes | advisory Q2 PASS without near-complete adjudication |
| OI-19 | Synchronous tracer collection of per-process counters. Decided in r8 (QD-30), then **withdrawn in r9**: the amended quality plan stops per-process attribution (AQP:331-338). Closed. | lead | — |
| OI-18 | A macOS group peak-memory source (§9.3; AQP:334). Until one exists, the macOS memory figure is `incomplete`. | release engineering (D12); lead | any macOS G13 memory qualification |

## Lead decisions in this record

QD-1 integer millionths and directional rounding · QD-2 outcome table · QD-3 proposition class · QD-4 JSON Lines ledger with a hash chain · QD-5 hard components and the full truth-input closure · QD-6 the separated populations · QD-7 the 20-minute time box · QD-8 calibration numbers · QD-9 agreement triggers · QD-10 the model-family rule · QD-11 family-weighted estimand · QD-12 independence families · QD-13 the cluster product bound · QD-14 *k*_min · QD-15 the two-sided pooled guard · QD-16 mutant states · QD-17 differential execution boundary · QD-18 determinism variants · QD-19 process inventory and own RSS counters (its mechanism replaced by QD-30) · QD-20 CI retry, batches and batch joins · QD-21 runner additions · QD-22 tree digest · QD-23 held-out exposure · QD-24 advisory water-filling allocation · QD-25 complete and incomplete performance results · QD-26 the K2 lane-freeze gate · QD-27 reason-to-quantity nulling · QD-28 the start-identity key and exact-equality host join · QD-29 generation safety (withdrawn in r8) · QD-30 ptrace exit-stop collection (withdrawn in r9) · QD-31 the tracing-overhead rule (withdrawn in r9) · QD-32 cgroup v2 `memory.peak` per fresh leaf, with cgroup-namespace escape prevention · QD-33 descriptor, mount (detach-then-mount) and control-ownership isolation · QD-34 charged-memory baselines.

## Not claimed

- No product measurement, corpus fetch, adjudication or product run was performed for this record. The values in §5 are exact arithmetic, computed for this record. Validity rests on the analytic proof in §5.5.
- No contract, schema, gate, threshold or register row is changed. RS3 is unchanged.
- ENV is a draft for D13, not an accepted carrier.
- The differential tools' execution behaviour is to be confirmed by each pin's canary check (QD-17).
- The cgroup method (§9.3) is to be confirmed by K1c's calibration on the D12 image. Until then, the Linux memory figure is `incomplete` with the reason `memory-peak-unverified`.
- The K2 estimate and its lane schedule are planning assumptions.
