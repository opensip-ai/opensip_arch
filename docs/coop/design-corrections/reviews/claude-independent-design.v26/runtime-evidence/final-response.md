Review complete and delivered.

## Assessment

**Verdict: CHANGES_REQUIRED** — 1 MUST, 3 SHOULDs, 3 advisories.

**Manifest verified by measurement**: 12,892 files / 736,277,340 bytes, 0 missing, 0 hash or length mismatches, 0 extras — re-confirmed byte-unchanged after every run.

**Read completely**: 37 documents, 21,365 lines, in 120–180 line chunks with preserved offset coverage — the five contracts (incl. native-evidence 3,693 and identity-and-evidence 1,729), all five incorporated evaluator3 contracts with composition §9 in full, both projection contracts, TargetAttributionV2 and the three negotiated native schemas, the planning layer, and every named companion. Seven large JSON files were traversed record-by-record programmatically.

**Pinned execution**: the source-pinned evaluator3 launcher ran with 1,242 pins valid and 16/16 checks at exit 0; sixteen further checkers pass. Pin gates were satisfied with frozen bytes, never bypassed; report-writing checkers ran only in a 1,350-file copy verified against the manifest first.

### The one MUST
`logicalPath` is admissible on `kind=unknown` in both TargetAttributionV2 and OccupancyCompanionV1, contradicting the field's own "**ONLY** … AND kind is file or symbol". The host projection copies it mechanically and no internal key covers the position. Measured consequence: the two lawful spellings of one provider claim produce different record digests (`4337e66e…` vs `2acc198d…`), and that digest reaches `selectedRefs` → `executionInputsDigest` → **run3**. No answer or verdict changes — only the sealed Run identity. It is the same determinacy class this design closed three times (anchor cardinality, capabilityId spelling, config node kind). Remedy is one schema branch plus one internal key, or withdrawing the word ONLY.

### What held up
The required demonstration worked exactly as intended: three fully reminted, internally hash-consistent false-result graphs all **ADMIT** under `open_run_closure` and all **REFUSE** under `close_run`, and the graph-query entry refuses them too because it calls `close_run`. `admit_cache_entry` calls `close_run` first, so there is no cached-payload bypass. Closure-kind rules refuse every referenced field; the three that admitted had zero references. The graph boundary behaved correctly at the exact visited-node cap, on cursor binding, endpoint membership, the availability selector (exit 4, distinct from `finding.show`'s exit 2), and full-response renderer parity including `completenessMet ⇔ countBasis=exact`.

### Standing
All four disposition maps are keyed by id with per-row basis and scope (16 AR / 15 FW / 27 DR / 5 owner rows), every row `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`. The 30 evaluation residuals, 28 condition-2 obligations and all 32 gates (measured `qualified:false`) are retained open. Two of my own probes produced false positives; both are corrected and recorded rather than hidden. I did not perform a blind consumer reconstruction — that session follows separately.

Deliverables: `review.md` (`d3863e78…`), `review.json` (`1ce1812b…`), plus 111 indexed probe and receipt files.
