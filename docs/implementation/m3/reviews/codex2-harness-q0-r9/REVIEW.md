# CODEX2 — M3-Q0 quality-harness design record r9

**Verdict: REQUIRED-FINDINGS. Four required findings.**

The per-run charged-memory method is a reasonable exploratory replacement. Fresh leaves solve counter carry-over, and same-run elapsed/memory collection removes the split-batch problem. Namespace setup alone does not establish the stated containment guarantee; the metric, baseline and incomplete-result rules also need the corrections below.

## Subjects and scope

- `docs/implementation/m3/harness/DESIGN.md`: **120794 bytes**, SHA-256 `4db107c03d9d65b4c62cc113baf15335810228d3d6328bae961d809ca3d5924b`.
- `exploratory-quality-envelope.schema.v1.json`: **53610 bytes**, SHA-256 `00f6d032c24c886341f27c4bb2befe6104f76daa0ca462c34c8175edb2c47d36`.

Both match REQUEST.md. Retained r8 subjects also match their recorded hashes. The delta fits the announced replacement and its schema, validator, runner, preregistration, history and citation changes; no unrelated substantive change was found.

**Dependency revision:** r9 cites quality-plan r5. During review, live `analysis-quality/PLAN.md` advanced to proposal r6. The retained `PLAN-r5.md` matches the reviewed r5 SHA-256 `c8ceb480718c41a803c83fc170296ed89d1dde59885d61f6589d9a1eed2105d8`. AQP line references below mean that pinned r5 basis. This review does not assess or accept r6.

## C2-Q0-R9-01 — Establish descriptor isolation and continuous control ownership (P2)

Location: [DESIGN:783–798](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:783), calibration :810–818.

Two source-derived counterexamples defeat the unconditional namespace guarantee:

- A writable sibling `cgroup.procs` FD opened outside the leaf namespace and inherited across exec retains its opener's namespace and credentials for migration checks. Writing the workload PID through it can move the workload out despite its current namespace and dropped capabilities. The leaf subsequently becomes empty. Linux 6.1 saves the namespace at :3757–3759 and uses it with file-open credentials at :4833–4836. ([Linux migration implementation](https://raw.githubusercontent.com/torvalds/linux/v6.1/kernel/cgroup/cgroup.c))
- A cgroup namespace does not itself hide the existing mount's writable ancestor controls. The same UID can access the delegated parent's `cgroup.subtree_control`. With the empty parent and leaf topology specified here, a permitted `-memory` then `+memory` cycle destroys and recreates child controller state. After freeing an earlier large allocation, that can lose its high-water while the final read and emptiness checks succeed. See controller transitions :3014–3075 and checks :3161–3166/:3227–3232; the peak reads the current memcg watermark. ([Controller transitions](https://raw.githubusercontent.com/torvalds/linux/v6.1/kernel/cgroup/cgroup.c), [memcg allocation and peak](https://raw.githubusercontent.com/torvalds/linux/v6.1/mm/memcontrol.c))

These are static inferences from pinned kernel source, not executed demonstrations. Dropping capabilities does not remove ordinary control-file access or inherited descriptors.

**Required change:** specify and verify a descriptor allowlist/close-on-exec boundary plus mount/access isolation that denies outside controls and preserves controller identity throughout the run. Include both paths in negative calibration. If that boundary cannot be established, retain `cgroup-escape-unprevented` and a null memory sample. Ordinary namespace-local migration is correctly confined.

## C2-Q0-R9-02 — Remove the universal anonymous-RSS bound (P2)

Location: [DESIGN:790–791](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:790), :799.

The claim that the figure is never smaller than the group's anonymous resident memory repeats the separately required r5 correction. Placement with `CLONE_INTO_CGROUP` also does not charge **every page touched** to the destination. Charges stay with their accounting owner; migration does not relocate existing charges, and memory can be shared across groups. ([Linux memory ownership](https://www.kernel.org/doc/html/v6.1/admin-guide/cgroup-v2.html#memory-ownership))

For example, an outside launcher allocates resident anonymous pages, then creates a child in the leaf. The child reads those inherited pages before exec without copying them. Their resident mappings do not move their external charges. Exec removes the inherited address space; it does not make the blanket first-touch or general RSS-bound claim true.

**Required change:** remove the universal inequality and qualify entry as establishing placement for subsequent accounting. Disclose inherited/shared/external ownership limits, retain the charged-memory label and D13 routing, and align the harness wording with the corrected quality-plan amendment. Live proposal r6 already withdraws this bound; pinned Q0 r9 still contains it.

## C2-Q0-R9-03 — Make leaf validation compatible with unavailable or missing evidence (P2)

Location: [DESIGN:867–880](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:867), :778–786/:803; ENV :5.

The new invariant requires every measured slot's operational record to name a distinct leaf, and its violation makes the envelope invalid. Yet unavailable-cgroup, v1-only, delegation-failure and macOS cases may create no leaf at all. They must still be representable as typed incomplete results with known elapsed values. Coverage also permits `record-missing`, and the accepted measured-slot example at :880 keeps both known samples despite the absent record.

Those cases cannot satisfy an unconditional actual-leaf witness requirement without inventing evidence.

**Required change:** apply actual-leaf identity/uniqueness when a leaf was created, with explicit absent-leaf handling tied to the applicable reason. Define independent driver evidence or a record-present-only check for missing operational records. Preserve QD-27's known values. Add reference cases for unavailable Linux, macOS and measured `record-missing`; retain duplicate-created-leaf rejection.

## C2-Q0-R9-04 — Bind budget ratios to a compatible charged-memory baseline (P2)

Location: [DESIGN:841–844](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:841), :764/:913; [ENV:1381](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:1381), :1518.

Both schema variants retain `baselinePeakRssBytes` while samples and maxima become charged-memory values. The budget rule still applies product ratios against a reviewed baseline, without saying that its denominator must use the new measurement. A reviewed old RSS baseline and a new charge peak are different quantities; their ratio cannot establish the claimed memory `within`/`over` status.

**Required change:** give the baseline explicit charged-memory semantics and an accurate carrier name, and require a reviewed compatible measurement/reset/cache basis. Do not reuse an RSS denominator by implication. Until a compatible baseline exists, use `no-baseline` or an explicitly approved exploratory absolute-charge comparison. Qualification equivalence remains with D13.

## Requested checks and previous findings

- **R8-01–04: moot by withdrawal.** No per-process ptrace inventory, terminal-counter attribution or attach/detach execution rule remains in the active collection method. Historical tables are labelled as history. This does not validate the withdrawn mechanism.
- **R8-05: moot through same-run collection.** There is one physical batch per ordinal; `rssCollection`/`rssBatchId` are removed. Retry/finality and batch joins remain.
- **Fresh leaf and entry:** no lifetime peak is reused or reset. Placement before workload exec is sound for the declared charged quantity, subject to R9-01/02.
- **Drain/read:** reading after `populated 0`, then verifying empty membership, establishes the intended live-member drain once containment/control continuity holds. Failed drain invalidates both samples.
- **Capabilities:** namespace creation followed by dropping all workload capabilities is sound in principle. It does not revoke descriptor or ordinary filesystem authority; R9-01 supplies the missing boundary.
- **Page cache:** the disclosure correctly says existing externally charged cache is not charged again. Cold/warm charge ownership must remain part of comparability.
- **Carrier/nulling:** six cgroup reasons plus two additional memory reasons match the declared table. Among these, only `cgroup-not-empty` nulls elapsed too. Record absence/invalidity keeps known numeric samples, but any reason makes the row incomplete and excludes it from Q6. All 40 object schemas remain closed; no floating-point fields were found.
- **Standing:** RS3 is unchanged. Charged Q6 samples stay in ENV; D13 owns any qualification equivalence. Adoption remains dependent on resolution of the separate quality-plan amendment.

## Non-blocking observations

- **C2-Q0-R9-N01:** ENV :5 retains stale AQP citations `419–425,535`. For the requested r5 basis the intended envelope/D13 targets are `PLAN-r5.md:428–434,544`. DESIGN's sampled remaps are correct for r5. Pin that revision or deliberately remap to the new live proposal.
- **C2-Q0-R9-N02:** clarify descendant settlement and elapsed end after tracing is withdrawn (:762, :794–798, :808). Empty live membership does not prove every descendant was reaped or successful: zombies are omitted from `cgroup.procs` and can remain when the directory is removed. State how daemonized descendants, bounded cleanup and failed settlement satisfy the retained elapsed/reaping definition. No separate concrete false accepted product sample was established for this observation. ([Linux process lifecycle documentation](https://raw.githubusercontent.com/torvalds/linux/v5.19/Documentation/admin-guide/cgroup-v2.rst))

## Verification

Read-only comparison, static JSON/citation checks, independent challenge reviews and primary Linux documentation/source inspection. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run; no runtime home was accessed; no commit was created. Writes for this review are limited to REVIEW.md and review.json in the requested r9 directory.
