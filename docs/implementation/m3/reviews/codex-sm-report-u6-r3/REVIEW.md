# SM-REPORT-U6-r3 review

Verdict: **ACCEPT**

Subject manifest: `1f9fabce06364250f85a7a9e1cc51d5ac6d01efb58d6fd3974d5b0fc8b4d6334` (3818 bytes; 18 members).

Required findings: none. Non-blocking observations: none.

## Round-3 corrections

SM-U6-R2-RF-01 is resolved. `otherFigures.SM14.S` contains all 12 workloads, including rspack (1384) and Sui (3318). Its counts match the accepted SM-12 subject-count records and every applicable medium and large census count. Source inspection confirms that the assembler constructs the map from SM-12 records and asserts complete coverage and census equality. Sui retains the item-9 condition, “if S-P permits”; SM-14 remains a formula with no derived value.

SM-U6-R2-NBO-01 is resolved. The large-workload table renders analysed-entry counts (Smithy 10 and Deno 2) rather than entry-list objects.

All other `otherFigures` values, timing components, F, T, targets, rules and outcomes equal round 2 by value. The round-2 report, data and scripts are preserved byte-for-byte under `history/`, together with the matching round-2 subject manifest. Round-1 history is also retained, and timing components, F, T and outcomes remain equal to round 1.

## Independent verification

Rehashed the subject manifest and all 18 members, and verified all 33 source pins. Verified the requested product and architecture base hashes; the product checkout is clean. The architecture checkout's held untracked tree was not inspected or changed.

Recomputed all 140 timing component statistics from their raw run records: the first three runs are warmups, and the median and maximum use the seven measured runs. Recomputed F and T for all 14 medium rows and both reset states, including sums of maxima and the numerical sensitivities. Source selection follows D-5: U-1 for changed warm Rust rows, the original static-profile series for warm hyper, and U-5b for cold Rust. The other components use their pinned accepted warm or cold records.

F and T follow item 9 and D-3/D-4. R8 sums the two entry statistics, counts SM-3 twice and SM-9 once. Express uses the synthesized analysis record. The TypeScript start over-count is stated and its sensitivity is carried. Outcome rules use warm F > 2 seconds for B, cold T > 30 seconds or warm T > 8 seconds for C, and neither for A. All holding outcomes are recorded: four A, ten B and eight C. D-1 synthetic replay conditionality, preliminary standing, and sensitivities without SM-9, without the duplicated start, and using sums of maxima are retained rather than substituted for the declared outcomes.

The prior round-1 corrections remain consistent. The data materializes the other figures from pinned sources, and source inspection confirms the renderer reads only `sm-report-data.json`. SM-5 carries all 15 per-row populations, with repository and dependency parts separated and their sourced bounds stated; no dependency-descriptor bound is invented. SM-12 carries all 12 workloads, including Sui, with actor medians, maxima and peak RSS. Its scope, process-memory interpretation, prototype actors and pending fields remain explicit.

SM-6, SM-8 and SM-10 match their accepted records and labels. SM-11 retains its two parts without deriving a quotient. SM-13 remains a fixed-byte decomposition with unset operational parameters. SM-14 remains a formula with the complete subject map. S_eff supplies only the measured first term with dependency populations alongside. The large-workload matrix accurately preserves partial compiler coverage, unavailable entries and the absence of outcomes dependent on those workloads. D-1 through D-9 and plan §3a are applied at their accepted standing.

## Scope and boundaries

No placeholder is filled, L is unchanged, and no owner question is raised in this report. Full S-M, L-G1, effective L and product qualification remain open; this acceptance is for the report unit. O7, D3 and D13 retain their closed standing.

Verification used read-only file/source inspection, hashing, JSON parsing and Git queries. No supplied assembler, renderer, runner, image, Cargo command, test or lane was executed. Neither repository nor the stage, working directories or control files was edited. Only this directory's `REVIEW.md` and `review.json` were written.
