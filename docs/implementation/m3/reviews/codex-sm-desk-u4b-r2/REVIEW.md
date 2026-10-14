# Review: SM-DESK-U4B-r2

**Verdict: ACCEPT.** SM-U4B-R1-RF-01 is resolved. No required findings or nonblocking observations.

## Exact subject and correction

Rehashed subject.json in `/tmp/opensip-implementation/sm-desk-u4b-r2-stage`:2209 bytes, SHA-256 `db41044d9f990ba17bdc3236a7bc885af4182774bb531c03fa03725f7e1bf81d`. All **9 members** match declared sizes and hashes.

Express's current SM-2 records now use only the synthesized program under D-4, for both resets. The cohort pair is retained separately in SM10Informational, explicitly labelled “NOT D-4 SM-2.” Its source data and statistics remain unchanged.

Verified all **152 current entries** are unique by language,row,component,reset,entryChild. The derivation asserts uniqueness and the correct count:60 TS entries,80 Rust base entries,6 additional R8 entry-child records and6 larger-of-two summaries. The report's current/informational counts and source explanation agree.

Compared against round1: current SM10 equals the original sequence with exactly the two cohort Express entries removed. Every other entry and the complete SM11 collection are unchanged by value. The original report, derivation, subject and records are retained byte for byte in history; the earlier review was not modified. Source pins and standing flags are unchanged. The derivation delta is confined to the corrected source selection, separate informational collection, uniqueness/count assertions and revision metadata.

## SM-10 independent verification

Rehashed all22 recorded source pins. Verified U-1's working series and source-map record against their committed archive index and each graph against its individual pin. U-5b copies retain their recorded source hashes.

Independently recomputed the seven-sample medians and maxima for all152 current entries and both informational entries from the accepted source run records. All reproduce exactly. Native rssNative values are byte-labelled macOS integers within uint64; compiler rss_native values are from the accepted Darwin observation path. Conversion to bytes is identity.

The selected sources cover all14 language/workload rows and both resets: accepted warm series, U-5a/U-5b cold records, U-2c Rust sealing/transfer, synthetic D-1 replay, and the now-unambiguous Express synthesized program. All source selections are correct.

SM-4 values remain the largest single compiler child's process peak per measured run, with child counts verified and executor-parent RSS explicitly unrecorded. Hyper correctly uses the accepted static-profile warm series under D-5, while cold uses the U-1 runner's same population. SM-7 labels receiver-child RSS. Shared start figures and synthetic replay sizes retain their labels.

R8 records each entry child and then the larger entry median/maximum. Recomputed all six larger-of-two summaries; none sums sequential RSS peaks. The lead convention and its limitation remain disclosed.

## SM-11 independent verification

Rejoined all nine pinned U-1 Cargo graphs to the first measured unit standings using path+ pkg_id for first-party classification. Analysed names, not-analysed kinds/standings/reasons, dependency counts and graph populations match exactly.

Counts `(first-party analysed, first-party not analysed, dependency analysed)` by ordinal are:

`(4,38,93), (0,8,63), (1,3,43), (1,0,6), (0,12,8), (0,3,3), (1,8,26), (0,12,8), (0,6,3)`.

S matches accepted census subject counts239,192,301,98,208,71,808,279,279. Overlay279 is the census's derived whole-overlay count, not a fabricated earlier recorded inventory value.

The unchanged selected SM-4 warm/cold times and SM-10 peaks retain round1's independently checked source values. Every row includes dependency crates; all except Hyper also miss first-party units. Item9's exact-coverage rule therefore correctly yields no quotient for every row. Worker scratch is not claimed measured.

R8 SM-4 median sums reproduce **2170.015ms warm** and **2216.123584ms cold**, matching report rounding2170.0/2216.1ms. These time sums do not alter the larger-of-two RSS convention.

## Scope and boundaries

Live product HEAD remains clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD remains `9dd254013a7b5c68f300ce67df84f3d657523c69`. Its existing untracked held E2s tree was not read or changed.

This is desk-only. No placeholder, F, T, outcome, admission or gate effect is recorded. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Full S-M, L-G1, effective L and product qualification remain false.

Only read-only file reading, hashing, JSON parsing, source comparison and Git queries were used. No derivation script, runner, image, Cargo, tests, lane, network, panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Exact lead assent and fresh design verification before architecture-only publication remain lead work.
