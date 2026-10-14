# Review: SM-REPORT-U6-r1

**Verdict: REQUIRED-FINDINGS.** Two required findings on complete figure assembly and source custody. No nonblocking observations. The timing sources, F/T arithmetic, outcomes and sensitivities independently check out.

## Required findings

**SM-U6-R1-RF-01 — Other-figure sources are absent from the report's pin set.** The report says sm-report-data.json carries every number with its source and SHA-256 pin. Its24 pins cover only timing-component assembly. render_sm_report.py reads U-4a,U-4b,SM-6 and rust-scope outside that mechanism. Sui scope,census-v2 fixed bytes and U-7's matrix are literal summaries without pins in the report data, which has no other-figure records. The claim of a complete pinned figure closure is false.

Add exact records/pins for all other figures, S_eff inputs and the large-workload matrix. Materialize their values or explicitly reference pinned complete records in report data and generate summaries from them. Preserve existing timing/outcome data and accepted sources; no measurement rerun is needed.

**SM-U6-R1-RF-02 — Required SM-5 populations and SM-12 peak-memory statistics are not assembled.** Item9's SM-5 includes rows,total bytes and canonical descriptor bytes against sourced bounds; the assembled component records contain only times. The S_eff prose provides selected examples rather than per-row repository and dependency-part populations/bound standings. SM-12's table has median times but no maximum times or numeric peak-memory values, despite the figure requiring time and memory and the accepted actor records providing both. For example Napi host-a's accepted maxNanos is3014958 and measuredPeakProcessRssBytes is25935872; neither value is carried into the report.

Carry the accepted SM-5 population/byte/descriptor/bound records for each reported row, keeping dependency parts beside repository rows and no invented dependency-descriptor bound. Carry SM-12 actor medians,maxima and native/converted whole-process peak RSS, including Sui and the correct prototype/synthetic labels. Preserve pending actual-worker, bound-domain and scratch fields. The missing records already exist; no rerun or new parameter choice is necessary.

`everyFigureAtItsStanding=false` records this incomplete figure assembly. It does not reject the accepted component measurements or upgrade any later-owned field.

## Exact subject and boundaries

Rehashed subject.json in `/tmp/opensip-implementation/sm-report-u6-r1-stage`:1382 bytes, SHA-256 `9510da111f7f4ae37db6e42f489826bf5ad5b2e9444cb13a9463549cd3d9b365`. All **6 members** match sizes and hashes. Rehashed all24 report-data source pins, including the index-pinned U-1 and U-5b working copies.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `8bc2250dadbf70a0f230ddf0d4bdd42815236a9d`. Its existing untracked held E2s tree was not read or changed.

Only read-only file reads, hashing, JSON parsing, source inspection and Git queries were used. No assembler, renderer, runner, image, Cargo, tests, lane, network, other panes or delegation. No private413 fixture, installation, signing keys or held-tree contents were read. Neither repository, stage, working directories nor control files were edited. Only this directory's REVIEW.md and review.json were written.

## Timing figures, F/T and outcomes

Independently selected the correct accepted source runs and recomputed **all140 component records**: ten runs each, ordinals0–9,three warmups and seven measured, median and maximum. Values and report rounding match.

D-1's source counts and synthetic replay label are preserved, with no real-workload bound. D-2 uses accepted U-2c two-part sealing and r3 transfer. D-3 uses two-entry sums for R8 SM-4/5/7,two SM-3 starts and one SM-9. D-4 selects synthesized Express and discloses TS start over-count. D-5 uses U-1 changed rows and original static-profile Hyper. D-7 keeps accepted warm labels and U-5a/U-5b cold labels without a flush claim.

Recomputed every row's F/T as sums of component medians and sums of maxima. The selected sources are correct. Verified edit target2s warm and medium budgets8s warm/30s cold against AQP and item9. Every holding outcome is recorded: **4 A rows,10 B rows,8 C rows**, with B and C both retained where they hold. A appears only where neither does.

Recomputed sensitivities without SM-9, without the double-counted TS start, and using sums of maxima. They match the JSON/report and are not substituted for the primary results. TS Napi remains A on medians but differs under maxima; only Rust Lambda's B survives removal of SM-9. D-1 conditionality and lead-macOS/not-D12 standing are explicit.

## Other-figure accuracy and large workloads

The rendered SM-6 repository-only counts/bytes/descriptors and SM-8 call medians/maxima match their accepted records. SM-10's152 current entries and labelled largest-child/larger-of-two conventions match accepted U-4b. SM-11's no-quotient standing matches medium dependency-inclusive populations and U-7's partial/absent large coverage.

The reported SM-12 median tables reproduce accepted actor run medians. Sui's host medians39.993334/67.583958ms correctly round to40.0/67.6ms. Its missing memory/max records are RF-02; later actual-worker/domain work remains pending as disclosed.

SM-13 fixed-byte literals match accepted census-v2 decomposition, including occupancy companion140, frame prefix40,census row61/container35; site counts remain sites, not candidates, and G3/C4a inputs remain unset. SM-14 remains a formula. S_eff remains first-term-only rather than a recorded ceiling.

The large matrix agrees with U-7 and U-4a: Smithy10 of25 entries analysed/15 unavailable, Deno2 analysed/root over descriptor bound, Rspack2 unavailable due stable-compiler nightly flags,and Sui3 unavailable for offline Git/excluded symlink reasons. Subject counts1084/1384/1052/3318 and snapshot population/descriptor figures match accepted records. This accuracy does not cure the absent machine-record pins in RF-01.

## Scope

No L placeholder is filled and L is unchanged. The report computes conditional F/T and outcomes as U-6 input; it leaves raising O3/O4 to the delta round. Full S-M,L-G1,effective L,native admission/worker,K1 and qualification remain open. O7,D3 and D13 stay closed. No owned G3/C4a parameter or completion-round value is chosen. Nothing was pushed. Lead assent and fresh design verification remain separate work after correction.
