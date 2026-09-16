Only one thing remains before the assessment files: the successor rehearsal (p04), which is still running in the background. Everything after it depends on its receipt. That means running the builder, writing `assessment.md` from both results, and a final invariant check, so I'm waiting for it to finish.

Already confirmed on the frozen candidate36 bytes (receipts p01–p03):
- **V23-S1 is a real inconsistency.** A package endpoint without `packageManifestPath` gets `QUERY.PARAMS_MALFORMED` from the schema and the public wrapper, while §2 and the parse helper say `QUERY.ENDPOINT_AMBIGUOUS`. No other route to ENDPOINT_AMBIGUOUS is reachable.
- **V23-S2 is a real inconsistency.** Native §10 gives `VERDICT.INDETERMINATE` for required-relation-missing, language-tier-unsupported and confidence-floor-unmet, but the D9 exit contract §10 claims to inherit gives specific COVERAGE codes. No published per-requirement exception exists. The native model also diverges on budget-exhausted.
- **V23-S3 is a real but narrow gap.** Unavailable evidence maps to `evidence.missing` only in model code; no contract text or control names it.
