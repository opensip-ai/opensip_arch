# GROK2 review: M3-D r3, supervisor and common control

**Verdict: ACCEPT.**

Subject: `docs/implementation/m3/supervisor-d/PROPOSAL.md`, 169430 bytes, sha256 `9679dbc4eec3081cce37f4e2333d4f1f6aecc4df19f0540b157439bd158a8771`. Base: `PROPOSAL-r2.md`, 167305 bytes, sha256 `1f5367dc8fffe9410338fce5dcabd41f7b3b331e39cfd0ad3ef8ced4c964bab8`. Single reviewer. Law review. No product cargo, tests, probes, or lead sets. `~/Library/Application Support/OpenSIP` was absent.

The r2-to-r3 diff is the round label, the r3 history and table, and the five edits that table names. CF-P remains met. Section F stays an O7 placeholder. Overnight line 9 is still B1. Accepting r3 accepts the D law.

## Prior findings

**r2 RF-1, resolved.** The prohibition is an analysis-attempt ExecutionId in the four places r2 named.

- The preamble refuses excluded forms before any analysis-attempt ExecutionId is drawn or reserved. The same bullet says item 25's R1 checks run before any draw, and that on first use the creation prelude's reservation may already exist at R10a and names the creation act only (PROPOSAL.md:9).
- Item 24's heading is "Manifest-class refusals before any analysis-attempt ExecutionId is drawn" (PROPOSAL.md:708).
- Item 24's forbidden substitutes forbid an analysis-attempt ExecutionId drawn or reserved before the checks, and forbid binding the prelude's ExecutionId to the analysis attempt (PROPOSAL.md:742).
- The global admission substitute forbids a refusal after an analysis-attempt ExecutionId is drawn or reserved (PROPOSAL.md:1180).

Item 24's decision paragraph is unchanged. R10a is still after R10 and before R11 and R12, a refusal there draws no analysis-attempt id, and the prelude id is not the analysis attempt's (PROPOSAL.md:717, :722). Item 25 stays at R1, before any ExecutionId draw, with its own absolute forbidden substitute (PROPOSAL.md:750, :761). The diff does not move R10a.

## Observations

- **NBO-1.** D5-T2c now records `exit: unreaped` for a root held alive past the reap ceiling, and it records that the group is not signalled again (PROPOSAL.md:576). That matches the escalation sentence and the r3 table.
- **NBO-2.** Item 6 now marks "`/var/tmp` is on disk on both distributions" as desk-checked and not measured by CF-P (PROPOSAL.md:257). LX-5 still says `/var/tmp` is not in CF-P.
- **NBO-3.** D4-T1's census bullet is the durable session draw, `x3d.session.execution-draw` right after the handoff (J1:179, J1:428). The ephemeral and render draws are not that point. The registry bullet remains the proof on every path (PROPOSAL.md:744-745).
- **NBO-4.** The r3 request pins the live overnight log: 20259 bytes, sha256 `dcdaeabe3ff0c9530043e638137f09780620eedc7977127b4f2ed63d6773555a`. Line 9 is B1. The law cites that entry.

## Non-blocking

The r3 history sentence says r2 found r1 RF-1 through RF-5 resolved (PROPOSAL.md:18). The r2 review records r1 RF-4 as partly resolved; the remainder was r2 RF-1, which this round closes. The clause does not change a rule.
