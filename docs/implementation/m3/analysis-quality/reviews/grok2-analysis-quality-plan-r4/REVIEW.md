# GROK2 fact review — M3 analysis-quality plan r4

Verdict: **ACCEPT**.

Subject: `docs/implementation/m3/analysis-quality/PLAN.md`, 62802 bytes, sha256 `52895ef271b6301fdec96e8b13abd58a25ae772293d6cd1648d09b6d5e2495b0`. That matches the request pin. The previous subject is `PLAN-r3.md`, sha256 `8f5b3547322940f2ad3003ddda95a9245591644330fee98e70fc07648c14c2b9`. Read-only. No product code was run. `~/Library/Application Support/OpenSIP` was absent.

## RF-1

Resolved. The r3 finding was that §2 still stated an unqualified exact Clopper–Pearson bound, and that 0.99 needed about 299 error-free findings in every stratum, while §4.3 had withdrawn both claims.

PLAN:138 now says the Q2 target is a one-sided 95% lower bound under §4.3's rule: the exact Clopper–Pearson bound only for established independent samples, and otherwise a preregistered cluster-aware bound. Too little evidence is INSUFFICIENT-EVIDENCE. PLAN:146 says the same thing about 0.99. The 299 count is an example for established independent samples, and a correlated stratum needs a cluster-aware bound or is INSUFFICIENT-EVIDENCE.

That is the rule at PLAN:231-234. Section 4.3 still holds the minimum repository count, the zero-error boundary, and the 29 example for 0.90. Section 2 points at that rule and no longer contradicts it.

## What changed

The diff against `PLAN-r3.md` is the title, the Q2 definition cell, the D4 note, and one row in the r3 response table (GROK2 RF-1). Nothing else changed.
