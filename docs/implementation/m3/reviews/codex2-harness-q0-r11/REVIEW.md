# CODEX2 — M3-Q0 r11

**Verdict: REQUIRED-FINDINGS.** One required finding and one non-blocking observation.

Reviewed the requested current subjects against the retained r10 snapshots:

| Subject | Bytes | SHA-256 |
|---|---:|---|
| DESIGN.md (r11) | 143572 | `c003a06a8d5eaa0ceb414f9458dc52d1fc644b304cf3aa73db6ef00317fac933` |
| exploratory-quality-envelope.schema.v1.json (r11) | 59433 | `8769ed0c156d5496d9df6640eab29c1a219303768ede9c417b59dc638d4f6975` |
| DESIGN-r10.md | 133762 | `c926077ce4403005360339d1dfab85240fb6506a3811d03d2a4c2a5d4717fee1` |
| exploratory-quality-envelope.schema.v1-r10.json | 59031 | `6558bd39ce60f788b78c55c18e8925bee5e02823956b4a25e3f9f61e711e12a9` |

## Decisions requested

1. **R10-01 is resolved.** [QD-33 item 2](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:825) now removes inherited cgroup mounts and aliases before creating the fresh view. Moving cwd outside cgroupfs, closing inherited descriptors, and checking exactly one remaining read-only, leaf-rooted cgroup mount resolve the overmount contradiction. The ordinary inherited mount is now an explicit success case.
2. **R10-02 is partially resolved.** [Creation ordering](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:806), [conditional settlement](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:851), [QD-27](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:939), and [leaf evidence](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:962) agree with the schema. Linux no-leaf runs can settle through subreaping; `settlement-failed` nulls both values. The added macOS known-elapsed promise introduces the required correction below.
3. **No unrelated substantive change found.** The full DESIGN/schema deltas fit the response table. All four prior non-blocking items are resolved: sustained non-dumpability/no outside exec, the temporary audit FD, the retained AQP6 pin, and the complete-row baseline predicate. The endpoint checks are correctly described as consistency checks rather than controller-cycle detection.

## Required finding

### C2-Q0-R11-01 — P2 — Establish macOS tree settlement before retaining elapsed

**Locations:** [elapsed definition](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:790), [settlement](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:851), [new calibration case](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:874), [new reference cases](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1034).

The new macOS no-leaf cases promise known elapsed after the workload root has been reaped and `waitpid` returns `ECHILD`. The adoption mechanism specified in step 5 is Linux `PR_SET_CHILD_SUBREAPER`. That mechanism reparents orphaned descendants to the supervising process and is Linux-specific. [Linux subreaper documentation](https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html)

Apple documents `waitpid` over the caller's children and orphan reparenting to PID 1. Its kernel implements this by moving ordinary children to `initproc` when their parent exits; `wait4_nocancel` scans the caller's children and returns `ECHILD` when none match. [Apple wait documentation](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/waitpid.2.html), [pinned XNU source, lines 2247–2248, 2674 and 2821–2823](https://raw.githubusercontent.com/apple-oss-distributions/xnu/xnu-11215.1.10/bsd/kern/kern_exit.c)

**Static counterexample:** the harness launches root R; R forks child C, then exits while C continues running. On macOS C becomes init's child. The harness reaps R and receives `ECHILD`, satisfying the stated no-leaf predicate while C is still alive. A double-forked daemon has the same problem. The drain limit never triggers because the design already reports settlement.

This records elapsed before the endpoint defined at line 790. The row's memory-platform reason makes it incomplete, but its retained elapsed value and any resulting elapsed median still claim a measurement that has not been established.

**Required correction:** specify positive macOS whole-tree settlement evidence, including orphaned and daemonized descendants, or mark elapsed unavailable with a typed reason that nulls it when settlement cannot be established. Memory-only failures may preserve elapsed only when elapsed is actually known. Align QD-27, the schema if the reason vocabulary changes, and the calibration/reference cases. Include a macOS root-exits-before-descendant case that cannot pass through `ECHILD` alone.

## Non-blocking observation

### C2-Q0-R11-N01 — P3 — Place calibration cases under their expected status

The unavailable Linux/macOS case is under the [complete heading](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:871), although its memory reason makes the row incomplete. The ordinary inherited writable mount is explicitly expected complete but appears under the [incomplete heading](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:881). Move these cases or distinguish a successful calibration check from the resulting row status. This is editorial; the operative status/nulling rules are clear.

## Review limits

Static review only: full subject comparison, hashes and sizes, schema structure/nulling inspection, citation checks, three independent review slices, and primary operating-system documentation/source inspection. No product code, tests, builds, validators, reference implementations, corpus fetches or benchmarks were run. No runtime home was accessed and no commit was created. All writes are confined to the requested r11 review directory.
