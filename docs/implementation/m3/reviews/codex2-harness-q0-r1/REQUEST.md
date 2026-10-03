CODEX2 review: the M3-Q0 quality-harness design record, r1, **method**. Focus on the soundness of the method, especially the statistics, and on consistency with the accepted plans. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r1.

**Rules:**
- Read-only. No commits, no product builds or test runs.
- Never touch the real home.
- Never read the 413 fixture.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md`, 65990 bytes, sha256 `22df1afb5b97f419a04e7c7cd5ffcb519f0a7311b8b4cddd7a1d90764aa831b3`.
- `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json`, 23190 bytes, sha256 `4cdfbb60b70ffaf74ddcf64c8757c6adbebe5f64cf1a0e9e3c7a915149064877`. This is the draft for D13.

The record is unit M3-Q0 (`docs/implementation/m3/M3-PLAN.md:157`). It sits under:
- the accepted analysis-quality plan (`docs/implementation/m3/analysis-quality/PLAN.md`, r4), especially §2, §4.3–§4.5, §5.1, §7 and §11 D12/D13;
- the accepted M3 unit plan (`M3-PLAN.md`, r4);
- the accepted operability plan (`docs/implementation/m3/operability/PLAN.md`, r3), §4.1;
- RS3 (`docs/coop/design-corrections/foundation/product-quality-report.schema.v3.json`) and its validator, and QG items[12] (`qualification-gates.applied.v1.json:262-275`).

Your r2 and r3 reviews of the analysis-quality plan (`docs/implementation/m3/analysis-quality/reviews/codex2-analysis-quality-plan-r{2,3}/`) set the confidence-rule obligation this record answers.

## Decide

1. **The confidence rule (§5).** Check each of these:
   - **The estimand** (QD-11): repository-weighted conservative precision, with a census guard on AQP's pooled ratio (QD-15).
   - **Method selection** (§5.2): chosen from the stratum's structure before any label is read. Exact Clopper–Pearson applies only when every family contributes one finding.
   - **The chosen cluster method** (QD-13): *L* = α^{1/k} × the geometric mean of the per-family precisions. Is the validity argument (product e-value, Markov's inequality, AM–GM over family means) correct? Does it handle the zero-error boundary without a degenerate pass? Are the rejected alternatives fairly treated?
   - **The minimum counts** (*k*_min 29 and 299), the status order, held-out-only acceptance, the downgrade path, and the per-stratum rather than family-wise confidence (OI-5).
   - **§5.8's practical consequence**, that gating Q2 is INSUFFICIENT-EVIDENCE without about 299 held-out families. Is it stated correctly?
2. **The ledger and adjudication (§3, §4).**
   - Does the hard/soft label key and the detector-independent truth-input digest meet AQP:249-263? In particular, can a stale label be carried?
   - Are the calibration bar, the agreement triggers (including the κ prevalence handling) and the model-family rule (QD-10) operational and sound?
3. **Recall and honesty (§1.3, §6, §7).** Check:
   - the outcome table and the classification of misses by cause;
   - mutant accounting and validator audits;
   - the differential's repository-code execution boundary (QD-17) against `M3-PLAN.md:355`.
4. **Stability and performance (§8, §9).** Check:
   - the independence of the mapping oracle;
   - the determinism variants and comparison rule;
   - cold/warm resets against LQM:923-924;
   - the RSS method against LQM:925 and AQP:329, including QD-19's counter source;
   - phase timings against OPP §4.1;
   - the CI retry rule (QD-20, your earlier N02);
   - the D12 requirements.
5. **The envelope (§11, ENV).** Does it meet AQP:419-425 without touching RS3? Is it closed and float-free, and does it carry every denominator?
6. **Consistency and citations.** Does any statement contradict an accepted plan or contract? Do the `FILE:line` citations support their claims? Is anything Q0 owes (`M3-PLAN.md:157`, `:222`) missing, including the K2 sizing in §13?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256": an object keyed by subject path.

Do not commit.
