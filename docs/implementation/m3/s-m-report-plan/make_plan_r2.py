from pathlib import Path
# Derive PLAN-r2.md from the reviewed PLAN-r1.md for Codex SM-REPORT-PLAN-R1-RF-01, -RF-02 and -NBO-01.
H = Path(__file__).resolve().parent; s = (H / 'PLAN-r1.md').read_text()
def rep(a, b):
    global s; assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
rep("# S-M report plan r1: definitions S-M's report fixes, and the units left before it\n\n**Lead plan record, 2026-10-13. Not law, not code, and no S-M figure.**",
    "# S-M report plan r2: definitions S-M's report fixes, and the units left before it\n\n**Lead plan record, 2026-10-13. Revision r2. Not law, not code, and no S-M figure.**")
rep("## 1. Where S-M stands", """**Changes from r1** (Codex `codex-s-m-report-plan-r1`, REQUIRED-FINDINGS; r1 is retained unchanged beside this file):

| # | Change | Finding |
|---|---|---|
| 1 | D-9 records SM-5's measured snapshot2-equivalent population per workload (rows, descriptor bytes, total bytes, bound standing) as the admitted-rows term. Any average-based ceiling is informational and estimated, outside the term. | SM-REPORT-PLAN-R1-RF-01 |
| 2 | §3a adds a coverage matrix for the large workloads smithy-rs, rspack, deno and sui (the last if S-P permits), and unit U-7 owes their pre-effect inputs before U-6. | SM-REPORT-PLAN-R1-RF-02 |
| 3 | D-1 calls its sizes workload source-count scenarios, carries the actual SM-2/SM-4 coverage beside them, and keeps any F, T or outcome conditional on the D-1 convention. | SM-REPORT-PLAN-R1-NBO-01 |

## 1. Where S-M stands""")
rep("  - **Graph:** the closed generator's synthetic graph with one fact, one finding and one finding fingerprint per **analysed source**. For a TS row, the analysed sources are SM-2's distinct configured files (express: the synthesized program's 141 roots). For a Rust row, they are the workload's RUST3-LIM subjects S.",
    "  - **Graph:** the closed generator's synthetic graph with one fact, one finding and one finding fingerprint per **counted source**: a workload source-count scenario. For a TS row, the count is SM-2's distinct configured files (express: the synthesized program's 141 roots). For a Rust row, it is the workload's RUST3-LIM input subjects S. These are input counts, not analysed coverage: Rust SM-4 analyses only part of S (census `subjectCoverage`, `s-m-rust-site-census-2026-10-13/REPORT.md:35-43`). The S-M report carries each row's actual SM-2/SM-4 coverage beside its SM-9.")
rep("One fact and one finding per analysed source is the smallest graph in which every source the analysis covers appears in the replayed Run. It chooses no G3 emission factor or other owned parameter (PROPOSAL-r6:627), and it is the accepted 193-source precedent (`s-m-full-replay-partial-2026-10-09`).",
    "D-1 fixes it as an explicit benchmark convention: one fact and one finding per counted source, as in the accepted 193-source precedent (`s-m-full-replay-partial-2026-10-09`). It chooses no G3 emission factor or other owned parameter (PROPOSAL-r6:627).")
rep("Any outcome the delta round records from an F containing it carries that label.", "Any F, T or outcome the S-M report or delta round records from it is conditional on the D-1 convention and says so.")
i = s.index("### D-9. S_eff's first term"); j = s.index("## 3. Units owed before S-M's report")
s = s[:i] + """### D-9. S_eff's first term

- **Decision.** "snapshot2's admitted rows, from SM-5" (PROPOSAL-r6:591) is recorded per workload as SM-5 measured it: the exact snapshot2-equivalent inventory population (its rows), its canonical descriptor bytes and total bytes, and its standing against each bound (100,000 rows, 4 MiB descriptor, 8 GiB; PROPOSAL-r6:559). For the medium rows this is `s-m-sealing-typed-2026-10-09/REPORT.md:7-23`; for the large workloads, `s-m-sealing-typed-remaining-2026-10-11/REPORT.md:9-29`. Under D-2 a Rust row's dependency-source part is reported beside it, not added to snapshot2's rows.
- **Not the term.** No ceiling is extrapolated from average bytes per row: row encoding varies with paths and content, and descriptor overhead is not a per-row constant. If the S-M report shows such a number, it is labelled "estimated, informational" and kept outside S_eff. S_eff itself is not filled; its other terms stay formulas (PROPOSAL-r6:591).

""" + s[j:]
rep("| U-4 | **Desk records.** SM-8 under D-6; SM-10 per F/T component; SM-11's labelled SM-4/SM-10 by covered units; S_eff's first term under D-9. | D-6, D-9 | Codex |",
    "| U-4 | **Desk records.** SM-8 under D-6; SM-10 per F/T component; SM-11's labelled SM-4/SM-10 by covered units for the medium rows; S_eff's first term under D-9 for all 12 Rust workloads. | D-6, D-9 | Codex |")
rep("| U-6 | **S-M report assembly.** Every figure under D-1..D-9, labels, per-row F and T as item 9 defines them, and every outcome that holds, ready for the S-M delta round on L. | U-1..U-5 | Codex |",
    "| U-7 | **Large-workload pre-effect inputs** under §3a: site census over the accepted Smithy and Deno prepared entries; SM-11's labelled SM-4/SM-10 by covered units where analysis exists; exact substantiated unavailability for every entry with no analysis (rspack, sui, Smithy `rust-runtime`, the Deno root). | U-3 | Codex |\n| U-6 | **S-M report assembly.** Every figure under D-1..D-9, labels, per-row F and T as item 9 defines them (conditional on D-1), and every outcome that holds, ready for the S-M delta round on L. | U-1..U-5, U-7 | Codex |")
i = s.index("Large-workload SM-11/SM-13 inputs (Smithy and Deno graphs) follow U-3 as information; no outcome depends on them (PROPOSAL-r6:577).")
j = s.index("## 4. What this plan does not do")
s = s[:i] + """### 3a. Large workloads (SM-11 to SM-14, S-M part)

Item 9 adds smithy-rs, rspack and deno, and sui if S-P permits, for SM-11 to SM-14 (PROPOSAL-r6:571), and the S-M round's part applies to each (:586-591). No outcome depends on them (:577), but that does not make them optional.

| Workload | Exact S | SM-12 host derivations | SM-4 / SM-10 coverage | SM-13 sites | S_eff first term (SM-5) | Owed |
|---|---|---|---|---|---|---|
| smithy-rs | 1,084 (`s-m-rust-scope-2026-10-09`) | accepted, 3+7 | partial: 10 of 25 declared entries analysed (`s-m-actual-smithy-fuzz-framed-series-2026-10-10`, `s-m-actual-smithy-http-fuzz-framed-series-2026-10-10`, `s-m-actual-smithy-r11-hierarchy-r9-framed-series-2026-10-11`, the last informational because review work ran concurrently); `rust-runtime` unavailable before launch (descriptor 5,115,131 bytes over the closed driver's 4,194,304-byte bound, `s-m-actual-large-workspace-data-r8-2026-10-10/REPORT.md:7`); `aws-smithy-fuzz` refuses under `--locked` (`…-r7-2026-10-10/REPORT.md:7`) | none | 3,632 rows; 647,602 descriptor bytes; within bounds | U-7: census over the analysed entries; labelled coverage; each other entry's unavailability exact |
| rspack | 1,384 | accepted, 3+7 | none: no graph in any accepted series (`…-r1-2026-10-10`; r2 observed only Smithy, Deno and Sui, `…-r2-2026-10-10/REPORT.md:7`) | none | 23,980 rows; 4,085,164 descriptor bytes; within bounds | U-7: the exact per-entry reason from the retained r1 outcomes, desk only |
| deno | 1,052 | accepted, 3+7 | partial: the binary subworkspace and the SQLite entry analysed (`s-m-actual-deno-framed-bin-series-2026-10-10`, `s-m-actual-deno-sqlite-short-paths-framed-series-2026-10-10`); the root unavailable before launch (descriptor 22,825,382 bytes, r8 REPORT:7) | none | 14,920 rows; 2,227,549 descriptor bytes; within bounds | U-7: census over the two analysed entries; labelled coverage |
| sui (if S-P permits) | 3,318 (`s-m-sui-scope-series-2026-10-10`) | accepted, 3+7 | none: Move resolves, but its bin source is a symlink the no-follow copy excludes (r7 REPORT:7) | none | 19,063 rows; 3,509,292 descriptor bytes; within bounds | U-7: unavailability recorded exactly; no analysis claimed |

Quotients by S are recorded only where coverage is exact (:587), which holds for none of these. Unavailable or partial coverage is preserved as it is. U-7 executes no repository code, admits nothing natively and measures no worker figure.

""" + s[j:]
(H / 'PLAN-r2.md').write_text(s)
