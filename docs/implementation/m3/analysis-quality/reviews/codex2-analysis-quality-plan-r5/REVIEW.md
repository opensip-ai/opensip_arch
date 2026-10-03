# CODEX2 — M3 analysis-quality plan r5

**Verdict: REQUIRED-FINDINGS. One required factual correction.**

Choosing a separately labelled cgroup charge peak for exploratory measurement is reasonable, and qualification is routed to D13. The unconditional resident-memory bound at PLAN:332 is false.

## Subject and scope

- Subject: `docs/implementation/m3/analysis-quality/PLAN.md`, **64603 bytes**, SHA-256 `c8ceb480718c41a803c83fc170296ed89d1dde59885d61f6589d9a1eed2105d8`.
- Accepted r4 snapshot: `PLAN-r4.md`, **62802 bytes**, SHA-256 `52895ef271b6301fdec96e8b13abd58a25ae772293d6cd1648d09b6d5e2495b0`.

Hashes match REQUEST.md. The diff has exactly three hunks: title, r5 changes section, and §5.1's peak-memory rule. No unrelated change was found. There is no separate acceptance-note deletion hunk in this retained-r4 comparison; r5 remains a proposal.

## C2-AQ-R5-01 — Remove the unconditional anonymous-RSS upper bound (P2)

Location: [PLAN:331–332](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:331).

The statement that `memory.peak` is never smaller than the group's anonymous resident memory is not generally true. Charge ownership follows the memory's accounting owner; migration does not move existing charges. A workload can map inherited anonymous pages whose charges remain outside the measured subtree. ([Linux cgroup memory ownership](https://www.kernel.org/doc/html/v6.18/admin-guide/cgroup-v2.html#memory-ownership))

For example, an outside parent allocates resident anonymous pages, forks a child, and places it in the dedicated workload group. The child can use those inherited pages without their charges moving into the group. Its mapped anonymous resident memory can exceed the group's peak charges. Within one group, shared pages also do not reproduce summed per-process RSS.

This is a counterexample inferred from the documented accounting rules, not an executed test. The counter remains useful for **peak charges to that subtree**; adding page-cache/kernel charges does not turn it into an unconditional bound on process resident memory.

**Required correction:** remove the unconditional inequality and unqualified RSS-conservatism claim. State the inherited/shared/external charge-ownership limit and define completeness for the kernel-reported charged quantity. Preserve the separate `cgroupMemoryPeak` label and D13 routing. An exploratory charge-budget result must not be presented as proof of the accepted RSS budget or compatibility with an RSS baseline.

## Facts and authority

The cited AQ:268–272 lines accurately require 3 + 7 runs, positive integer elapsed/RSS values, median elapsed/max RSS, the 1.20×/1.25× limits and reviewed absolute bounds. They do not specify a process-aggregation mechanism. QG items[12] still names process-tree RSS and the DR-G13 owners. LQM:925 accurately supplies the preview's larger-of-two method; AQC:142–146 supplies its process-tree RSS target.

The amendment does not silently change those accepted qualification requirements: PLAN:335 routes the new metric to D13, §7:428–442 forbids exploratory G13 input/promotion, and D13 at :544 names Language quality, Product and Release engineering. D1 remains a record correction toward current AQ; D13 must carry any substantive charged-memory qualification decision.

## Non-blocking observations

- **C2-AQ-R5-N01:** pin each run's interval in the harness. Use a fresh cgroup or a supported reset with the retained FD; reusing the lifetime mark would mix warmups and measured runs. Also establish availability, containment, collection-failure handling and comparable cache/charge ownership, swap and effective limits. ([Linux memory interfaces](https://www.kernel.org/doc/html/v6.18/admin-guide/cgroup-v2.html#memory-interface-files))
- **C2-AQ-R5-N02:** label informational `wait4` values as reported resource usage. Linux includes reaped-child maxima, so they are not necessarily independent own-process peaks. Keeping them out of budgets is sound. ([wait accounting](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/exit.c), [resource-usage calculation](https://raw.githubusercontent.com/torvalds/linux/v6.18/kernel/sys.c))

## Verification

Read-only diff, citation/authority checks and primary-source inspection only. No product code, tests, builds, validators, corpus fetches or benchmarks were run; no runtime home was accessed; no commit was created. Writes for this review are limited to REVIEW.md and review.json in the requested amendment directory.
