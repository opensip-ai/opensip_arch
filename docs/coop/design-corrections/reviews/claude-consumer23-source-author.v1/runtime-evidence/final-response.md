I fixed all three source issues in the isolated assembly and wrote the author report. This is authorship only: not acceptance, blind B or readiness, and nothing was committed or pushed. All four checkers pass on the final assembly: query 138/138, native cases 377/377, identity 1596/1596 and integration 412/412.

**What changed**
- **V23-S1:** A package endpoint without a `packageManifestPath` is now a schema refusal (`QUERY.PARAMS_MALFORMED`). "Ambiguous" is kept for a complete tuple that matches more than one vertex, and the model helper was brought into line. Public behaviour is unchanged. The reference public wrapper can never actually return "ambiguous", so only a helper-level control covers that code.
- **V23-S2:** Native deficiencies now follow the existing D9 codes.
  - The section 10 table rows for language tier, confidence floor and missing relation now use their `COVERAGE.*` codes.
  - The model gained a complete mapping for all nine deficiencies, checked against the D9 contract.
  - `run_termination` now picks the code by section 10 precedence. It used to return `VERDICT.INDETERMINATE` for budget and the other three `COVERAGE.*` deficiencies on a successful stage. It also ignored a higher-precedence entry deficiency on budget or unavailable stages.
  - 11 of 24 stage × entry combinations change. One gets a less specific code: a budget stage with an input-closure deficiency goes from `COVERAGE.BUDGET_EXHAUSTED` to `VERDICT.INDETERMINATE`, because input-closure ranks higher.
  - The helper returns only the primary code, not D9's list of secondary reasons.
- **V23-S3:** The graph query contract now states `purged`, `expired`, `corrupt` and `unavailable` → exit 4 with `evidence.purged`, `evidence.expired`, `evidence.corrupt` and `evidence.missing`. `retained` and `partial` neither refuse nor grant; `close_run` decides. No new enums or details were added.
- **V16-A3 and V23-A1:** kept as advisories with no source change; the reasons are in the report. The consumer said the "Not native CoverageResult" wording appears in both schemas, but only the graph-query schema has it.

**Tests**
- 15 new query controls and 2 new native cases.
- Against the frozen36 models, only one of the new query controls fails; the other 14 lock in behaviour frozen36 already had but never published. Both new native cases fail there, on wrong codes and not just missing functions.
- No existing expectation was changed.

**Things I didn't finish or change**
- **Schema annotation:** my edit to the native schema's D9 wording broke an identity check. That file's hash is a registered schema digest, so I restored the exact frozen36 bytes. The exact replacement text is in the JSON report, to apply only with a deliberate re-registration.
- **Failed runs:** a failed identity run and a failed probe from that edit are kept as receipts.
- **Citation fix:** reviewing my own diff, I found a wrong case reference in native-evidence.md, fixed it, and reran the four checks and the after-snapshot.
- **Not run:** the native checker's `main()` (it writes into the tree), the six groups, planning checks and pin validation. The frozen36 manifest file wasn't readable, so custody rests on a file-by-file hash comparison. S2 evidence comes from calling helpers directly, with no complete Run.
- **Carried over:** the one TCB-SCOPE-01 assumption with 13 residual accounts, plus 32 product gates and 54 recovery cases, none performed.

**For root**
- Reseal 30 stale pin rows: 6 in each of the five source-pin ledgers.
- The same frozen36 hashes also appear in three planning-layer files and in `workflows-report.v1.json`; I left them alone.
- `native-evidence-report.v2.json` still records 375 cases; the assembly now has 377.

Six files differ from frozen36, and nothing outside them. The before-images, after-images and diffs are saved, and every command and its output is under `probes/receipts/`.

Files are in `/private/tmp/opensip-design-corrections/claude-consumer23-source-author.v1`:
- author-report.md
- author-report.json (SHA-256 `de5f2fd2…`)
- before-manifest.json
- after-manifest.json
