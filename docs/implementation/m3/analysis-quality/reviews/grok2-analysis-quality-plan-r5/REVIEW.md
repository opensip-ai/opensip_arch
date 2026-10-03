# GROK2 fact review — M3 analysis-quality plan r5

Verdict: **ACCEPT**.

Subject: `docs/implementation/m3/analysis-quality/PLAN.md`, 64603 bytes, sha256 `c8ceb480718c41a803c83fc170296ed89d1dde59885d61f6589d9a1eed2105d8`. That matches the request pin. The previous subject is `PLAN-r4.md`, 62802 bytes, sha256 `52895ef271b6301fdec96e8b13abd58a25ae772293d6cd1648d09b6d5e2495b0`, the accepted r4. Read-only. No product code was run. `~/Library/Application Support/OpenSIP` was absent.

## What changed

The diff against `PLAN-r4.md` is three hunks: the title, the new r5 changes section (PLAN.md:41-43), and the §5.1 peak-memory bullet (PLAN.md:331-338). The r4 RSS bullet is gone. Neither file contains an acceptance note, so the diff does not remove one.

## Facts

The new citations match the sources.

- AQ §3 is `admission-and-qualification.md:225`. AQ:268-272 requires positive integer elapsed nanoseconds and peak RSS bytes, then median elapsed time and maximum RSS, with limits 1.20× and 1.25×. Those lines do not say how peak RSS bytes are measured. PLAN.md:113, PLAN.md:329, and the r5 qualification sentence restate that regime and send the measurement question to D13.
- QG items[12] is DR-G13 (`qualification-gates.applied.v1.json:263`). The owner string at QG:264 is "Language quality + Product + Release engineering". QG:268-269 still requires cold/warm p95 and process-tree RSS, with thresholds decided by D-369. D1 (PLAN.md:531) remains the proposed record successor for that text. r5 does not edit D1.
- AQC:142-145 is the preview's high-water resident sum over the supervised process tree, with NON-PASS when descendants cannot be measured. LQM:925 is the larger of the 10 ms sampled concurrent sum and the sum of per-process high-water counters, with a missing child counter as NON-PASS. LQM:923-924 is the cold and warm definitions the cold-fixture bullet cites. The r5 parenthetical describes r4's larger-of-two rule in those words; LQM:925 is the line that states the larger-of-two, and AQC:142-145 is the resident-sum half.
- D13 (PLAN.md:544) is still the exploratory envelope now and a DR-G13/report/harness successor before any Q2–Q8 target qualifies. PLAN.md:434 says that envelope is never a G13 input and is never promoted. PLAN.md:7-9 still says this plan changes no accepted contract, gate, threshold, or register row.

CODEX2's M3-Q0 r8 review is REQUIRED-FINDINGS. Its findings are ptrace attribution gaps (CLONE_UNTRACED children, exec-entry VmHWM, CLONE_VM/vfork sharing, SEIZE/seccomp side effects, and split-batch identity). That review does not adopt `memory.peak`. r5's "follows" sentence is the lead's response to those still-open per-process gaps. r2 through r6 and r8 are all REQUIRED-FINDINGS; r7 was not reviewed. Per-process attribution had not closed.

r5 does not contradict AQ §3, QG items[12], or LQM without a successor. It leaves AQ's peak-RSS statistic and QG's process-tree RSS evidence in place for qualification, names D13 as the G13 successor that must decide whether `memory.peak` satisfies AQ:268-272, and leaves LQM:925 as the preview method (PLAN.md:340). The plan's own exploratory figure is a different quantity, labelled `cgroupMemoryPeak`.

## Method

`memory.peak` is a sound exploratory budget figure for charged memory of a workload that stays in one cgroup. The kernel file is the maximum memory usage of that cgroup and its descendants since the cgroup was created, or since the last reset on the same file descriptor. The counter moves when memory is charged, so a short-lived child that remains in the cgroup is included without the event-channel or ptrace join that Q0 could not close. A 10 ms sampled sum can miss a peak between samples; this mark does not.

The stated limits match the counter. The charge includes userland page cache and anonymous memory, plus kernel objects and socket buffers the controller tracks. That is wider than resident set size. It is at least the group's anonymous charge, because anonymous memory is part of the charge, so the high-water of the total is at least the high-water of the anonymous part. Reports are told to say `cgroupMemoryPeak`. `wait4` maxima are information only, which keeps the unclosed per-process counters out of the budget. macOS has no group high-water, and `incomplete` cannot pass. Swap has its own `memory.swap.peak` and is outside this charged-memory figure.

The figure is conservative against the group's anonymous charge and against a sampled sum. A physical page is charged once, while a sum of per-process RSS counts a shared mapping in each process, so `memory.peak` can sit below r4's larger-of-two. The plan does not claim otherwise. Qualification still has to go through D13 before this figure can stand in for AQ:268-272 or for QG's process-tree RSS.

## Anything else

Nothing outside the title, the r5 section, and that §5.1 bullet changed.
