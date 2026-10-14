# S-M large-workload site census and declared-entry coverage (U-7)

This is an outside-product experiment and desk record, unit U-7 of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`, §3a). It supplies the S-M round's SM-11 and SM-13 inputs for the large Rust workloads of M3-L r6 item 9 (PROPOSAL-r6:571, :586-591): smithy-rs, rspack and deno, and sui if S-P permits. It produces no SM-11, SM-13 or SM-14 value.

## Declared-entry coverage (desk)

`large-workload-entry-coverage.md` gives, for every one of the 33 original declared Cargo workspace entries, its final accepted outcome with citations: **12 analysed** (smithy-rs 10, deno 2) and **21 unavailable** (smithy-rs 15, deno 1, rspack 2, sui 3). Reasons, verbatim from the accepted records:
- smithy-rs: 7 generated or path inputs absent from the pinned tree, 5 lock refusals under `--locked`, 2 descriptors over the closed driver's 4 MiB bound (`rust-runtime` 5,115,131 bytes; `canary-runner` 6,596,209 bytes), 1 local package-name mismatch;
- deno: the root descriptor 22,825,382 bytes over the bound;
- rspack: both entries refused by the pinned stable compiler because the original configuration passes nightly-only `-Z` flags;
- sui: two Git dependencies that cannot be checked out offline, and a bin target whose source is a symlink the no-follow copy excludes.

No lock, bound, flag or tree was changed to make an entry available. PLAN-r2 §3a listed `rust-runtime` but not `canary-runner` among the over-bound entries; this record adds it from H9 REPORT:3.

## Census of the analysed entries

- **What ran.** The accepted site-walk v2 image (U-3, `codex-sm-rust-site-census-v2-r2`) as the wrapper, through the unchanged closed framed-bin executor (pins from `sm-framed-bin-profile-controls-r1-stage/source.json`, checked before every graph), over the prepared entries of the five accepted large-workload framed series (Smithy fuzz, Smithy http-fuzz, Smithy r11 hierarchy, Deno bin, Deno SQLite short paths): 12 entries, twice each, 976 compiler children. The series' own driver source is the closed framed driver (`43315ea6…`) of which v2 is the accepted variant.
- **Checks.** Every run repeated its accepted pilot's unit population (`allPopulationsRepeated` True), and site counts were identical across runs (`allSiteCountsDeterministic` True). No timing statistic is claimed.
- **Audit.** `audit_sm_large_site_census_r1.py` (derived from the accepted U-3 audit) computes S by RUST3-LIM's recipe over the verified T2 store, maps first-party site files to store-identical subjects across all of a workload's entries, keeps dependency crates apart, and groups site kinds by relation@rung as a label only.

| Workload | Entries | S | Subjects with sites | First-party units analysed / unavailable | Dependency units analysed | declares | imports | references | calls | types | unresolved-edge | clones body | literal | control-flow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rs-large-smithy-rs | 10 | 1084 | 13 | 3 / 46 | 477 | 1268 | 132 | 2474 | 449 | 2254 | 36 | 213 | 99 | 178 |
| poly-very-large-deno | 2 | 1052 | 1 | 1 / 1 | 7 | 8 | 5 | 25 | 8 | 81 | 6 | 2 | 10 | 7 |

Coverage is far from exact: smithy-rs 13 of 1084 subjects, deno 1 of 1052. Almost all analysed units are dependency crates. rspack and sui have no analysed entry. So no SM-11 quotient is recorded for any large workload, as item 9 requires (:587).

## Standing

Sites are not candidates. No stage, key, emission factor, census kind or batching is chosen; no SM-11, SM-13 or SM-14 value. No native admission or product change. L-G1 is open, and L is not in effect.
