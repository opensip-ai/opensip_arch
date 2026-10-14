# Review: SM-DESK-U4B-r1

**Verdict: REQUIRED-FINDINGS.** One required finding, SM-U4B-R1-RF-01, for duplicate Express SM-2 source records. No nonblocking observations. All recorded RSS statistics independently reproduce, and SM-11 coverage/quotient decisions pass.

## Required finding: SM-U4B-R1-RF-01

PLAN-r3 D-4 selects the synthesized program's whole-process span for Express SM-2. derive_u4b.py nevertheless includes Express from the cohort loop, then appends its synthesized-program record for the same row/component/reset.

The resulting JSON has two current entries for each `(tsjs, js-medium-express, SM-2, reset)` key:

| Reset | Cohort median bytes | Synthesized median bytes |
|---|---:|---:|
| Warm | 129941504 | 269156352 |
| Cold | 129810432 | 269418496 |

All four are labelled SM-2, rather than marking the cohort pair informational and outside the selected component. The report generator constructs a reset-keyed dictionary and silently keeps the last entry, so Markdown shows the selected synthesized values while the machine record remains ambiguous. A first-match consumer can choose the wrong component peak. sourcesCorrect=false records this source-selection defect; numerical recomputation itself passes.

**Required correction:** exclude Express from current cohort SM-2 rows, retain synthesized results for both resets, and either remove the cohort pair or preserve it in a separately labelled informational collection. Update the current-entry count (152 instead of154 if the two surplus entries are removed), report and manifest; check uniqueness by language/row/component/reset/entry identity. No measurement rerun is needed.

## Exact subject and sources

Rehashed subject.json:1100 bytes, SHA-256 `4fb0f1dd1ad2cac67bd79c455cbf67a715fe7e814abb411d2c4dc3dcf8806cf0`. All **4 members** match declared sizes and hashes.

Rehashed all22 recorded source pins. U-1's working series and source-map index match their committed large-records index pins; each graph matches its recorded hash. The U-5b working result copies match their recorded source pins. Sources are the accepted warm components and U-5a/U-5b cold records, with U-2c supplying Rust SM-5/SM-7 and replay retaining its synthetic source-count label.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `9dd254013a7b5c68f300ce67df84f3d657523c69`. Its existing untracked held E2s tree was not read or changed.

## SM-10 recomputation and labels

Independently recomputed all **154 stored entries**, including the two surplus cohort Express entries and six R8 larger-of-two summaries. Every median/maximum matches its recorded source over seven measured samples from ten-run series. Recorded rssNative values are integers in byte-labelled macOS runs and fit uint64. Compiler observations use rss_native from the accepted Darwin observation path; conversion to bytes is identity.

SM-4 is correctly labelled as the largest single compiler child's peak in each run; child counts reproduce. It is not executor-parent RSS or summed process memory. Hyper correctly selects the accepted static-profile warm source under D-5, because U-1 changes no Hyper unit; cold uses the U-1 runner over the same population.

SM-7 is correctly identified as receiver-child RSS. Shared language-start figures and synthetic SM-9 source counts are labelled. R8 retains per-entry records, and each summary uses the larger entry median and maximum rather than adding sequential peaks. The report identifies this lead convention. Other row/component/reset selections reproduce their expected accepted sources.

## SM-11 coverage and statistics

Independently joined U-1's first measured unit standings to each pinned Cargo graph, classifying first-party units by path+ pkg_id. Analysed names, unavailable kinds/standings/reasons and dependency counts match the desk record. Counts `(first-party analysed, first-party not analysed, dependency analysed)` by ordinal are:

`(4,38,93), (0,8,63), (1,3,43), (1,0,6), (0,12,8), (0,3,3), (1,8,26), (0,12,8), (0,6,3)`.

Subject counts match the accepted census recipe:239,192,301,98,208,71,808,279,279. The overlay's279 is the census's derived whole-overlay count; its earlier rust3LimRecordedS field is null, not an invented original recorded pin.

SM-4 warm/cold times and the joined SM-10 child peaks reproduce their selected series. Every row includes dependency crates, and all except Hyper also miss first-party units. Under item9's exact-coverage rule, all nine rows correctly record **no quotient**; worker scratch is not claimed measured.

R8's warm SM-4 median sum is2170.015ms and cold sum2216.123584ms, matching the report's2170.0/2216.1ms. RSS summaries remain larger-of-two values rather than these time sums.

## Scope and boundaries

This remains a desk-only derivation. It fills no placeholder, computes no F or T, records no outcome and grants no admission or gate effect. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Full S-M, L-G1, effective L and product qualification remain false.

Only read-only file reading, hashing, JSON parsing, source inspection and Git queries were used. No derivation script, runner, image, Cargo, tests, lane, network, panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Lead assent and fresh design verification remain separate work after correction.
