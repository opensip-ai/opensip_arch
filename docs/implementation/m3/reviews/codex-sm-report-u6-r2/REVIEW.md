# Review: SM-REPORT-U6-r2

**Verdict: REQUIRED-FINDINGS.** Both round-1 findings are resolved. One new required finding remains on SM-14's incomplete subject-count map, plus one nonblocking rendering observation.

## Required finding: SM-U6-R2-RF-01

otherFigures.SM14.S is constructed from census-v2's medium rows and U-7's analysed large-workload rows. It contains the eight medium workloads, Smithy1084 and Deno1052, but omits **poly-large-rspack=1384** and **rs-very-large-sui=3318**. Those accepted independent subject counts already appear in the newly pinned SM-12 records. Compiler non-analysis does not make their subject counts unavailable.

The report states S is exact per workload and points to this map, so its machine SM-14 input is incomplete for two item9/section3a workloads. Add the missing counts from the complete accepted subject-count records, preserve Sui's conditional standing, cross-check census agreement and assert expected workload coverage. Keep K_stage, stage grouping and other owned inputs unset. Regenerate the exact data/report/manifest; no measurement rerun or stage-budget derivation is needed.

`everyFigureAtItsStanding=false` reflects this incomplete exact-count input. It does not reject the formula or require completion-round values.

## Round-1 resolution and subject custody

Rehashed subject.json in `/tmp/opensip-implementation/sm-report-u6-r2-stage`:2607 bytes, SHA-256 `1e2a2520b142fdcfda16d4c9ffe98e03c8fa2c908ddd8fa67628c3ba75ab6839`. All **12 members** match declared sizes and hashes.

Original report,data,assembler,renderer and subject are retained byte for byte in history. The historical subject hash remains `9510da111f7f4ae37db6e42f489826bf5ad5b2e9444cb13a9463549cd3d9b365`. Components, F/T rows, targets,rules,standing and sensitivities equal round1 by value. The earlier review was not modified.

**RF-01 resolved:** all33 report-data pins match current source bytes. Nine new pins bind SM-6,U-4a,U-4b,rust-scope,Sui source,census-v2,fixed-byte decomposition,U-7 checks and the per-entry coverage record. otherFigures materializes the additional figure records. The renderer reads only sm-report-data.json; its source records are no longer independent unpinned inputs.

**RF-02 resolved:** all15 SM-5 population records (six TS and nine Rust entries) reproduce accepted repository and dependency shapes. Rows/entries,total bytes,descriptor bytes,set identities and sourced bounds match; dependency parts remain beside snapshot rows with no dependency-descriptor bound. All12 SM-12 workloads carry actor medians,maxima and whole-process peak RSS, Sui included. Verified37 actor summaries against accepted records, including the additional closed Rust helper. Process/prototype labels and later-owned fields remain pending.

## Statistics, definitions and outcomes

Independently recomputed all **140 timing components** from ten-run source records (three warmups,seven measured), checking median and maximum. All match. Recomputed all14 F/T rows and outcomes; counts remain **4 A,10 B,8 C**.

D-1 synthetic source-count conditionality,no lower-bound inference,D-2's accepted dependency sets,D-3's R8 entry sums/two starts/one replay,D-4's synthesized Express and TS-start over-count,and D-5's U-1 changed rows/original static-profile Hyper remain correct. D-7 reset labels remain preliminary with page cache recorded rather than flushed.

Targets remain2s warm edit,8s warm medium and30s cold medium. Every holding B/C is retained and A applies only where neither holds. Sensitivities without SM-9,without duplicate TS start and under sums of maxima are unchanged from the independently verified round1 data; they remain alongside rather than replacing the primary results.

## Other figures and large workloads

SM-6 rows/bytes/descriptors reproduce accepted read-set records. SM-8 medians,maxima and call labels match U-4a. SM-10's152 current entries and informational Express cohort records equal accepted U-4b. SM-11 medium coverage and no-quotient standing also equal U-4b; large coverage matches U-7 exactly.

SM-12 time/RSS rows reproduce accepted rust-scope actors and Sui source statistics. SM-13 materializes accepted medium/large site groupings, exact fixed-byte structures,ambiguities and unset parameters; it remains a decomposition with sites labelled as not candidates. SM-14's formula matches the accepted fixed record and remains uncomputed; its incomplete S map is the finding above.

S_eff's12 first-term population records equal U-4a, with dependency populations beside them and no filled ceiling. The large matrix and pinned entry-coverage record preserve Smithy10 analysed/15 unavailable,Deno2 analysed/root over bound,Rspack2 unavailable and Sui3 unavailable, with the accepted reasons. The numeric large-workload records are accurate.

**Nonblocking observation SM-U6-R2-NBO-01:** the table's Analysed entries cells print full Python-style object lists for Smithy and Deno, including cwd paths/control fields. Show10 and2 counts in the summary and leave detailed entries in pinned JSON. This is a presentation issue; the underlying populations are correct.

## Scope and boundaries

Live product HEAD remains clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD remains `8bc2250dadbf70a0f230ddf0d4bdd42815236a9d`. Its existing untracked held E2s tree was not read or changed.

No L placeholder is filled or L changed. Conditional F/T and outcomes are report inputs; raising owner questions remains the delta round's work. Full S-M,L-G1,effective L,native admission/worker,K1 and qualification stay open. O7,D3 and D13 stay closed. No G3/C4a parameter is chosen.

Only read-only file reads,hashing,JSON parsing,source comparison and Git queries were used. No assembler,renderer,runner,image,Cargo,tests,lane,network,panes or delegation. No private413,installation,signing keys or held-tree contents were read. Neither repository,stage,working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Lead assent and fresh design verification remain separate work after correction.
