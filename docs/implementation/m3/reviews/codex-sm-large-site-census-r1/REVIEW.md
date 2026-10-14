# Codex review: SM-LARGE-SITE-CENSUS-r1 (U-7)

**Verdict: ACCEPT.** No required findings or nonblocking observations. The 33-entry coverage record accurately distinguishes 12 entries with partial analysis from 21 unavailable entries. The accepted v2 image produces reproducible site observations over those twelve prepared entries without claiming full workload coverage or candidate volumes.

## Exact subject and baselines

Stage: `/tmp/opensip-implementation/sm-large-site-census-r1-stage`.

`subject.json`: 2095 bytes, SHA-256 `8b1421184a1e5ddd7bd84bd2c8bdefde1c5eb1dead0b886270af1d63c737ee8a`. Independently rehashed all **eight members**; every size and digest matches. The frozen report, coverage table, runner, audit, run log, raw census, derived checks and freeze script are the reviewed subject.

Live product HEAD matches `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean; architecture HEAD matches `4b3dca62b741d56d1cad89ea841fe06e6cbe2cfd`. Architecture's existing untracked held E2s directory was not read or changed.

## Declared-entry coverage

Checked the coverage table against original-workspace-entries-r1.json: ordinals 0 through 32, with 25 Smithy, three Deno, two Rspack and three Sui entries. The analysed ordinals are exactly **0, 9, 12, 16, 18–23, 26 and 27**. The remaining 21 entries are accounted for. “Analysed” denotes eligible units within an entry, not complete entry/root or workload coverage.

Checked each reason class against cited receipts or accepted report passages:

- Smithy's seven missing generated/path inputs at ordinals 1, 2, 3, 4, 5, 6 and 11 match S1's no-such-file diagnostics. The omitted generated paths are not supplied or repaired.
- Its five lock refusals are ordinals 8, 10, 13, 15 and 17. The cited S7/S11/S5 receipts preserve --locked refusals, including the stale aws-smithy-fuzz lock.
- Ordinal14's original local package-name mismatch matches the accepted classification: the fuzz manifest requests aws-smithy-http from the aws-smithy-legacy-http path. Public acquisition cannot repair that mismatch.
- Smithy ordinal7's 5115131-byte descriptor and Deno ordinal25's 22825382-byte descriptor match r8 REPORT.md:7. Smithy ordinal24's 6596209-byte canary-runner descriptor matches H9 REPORT.md:3. All exceed the unchanged 4194304-byte prototype driver bound and are unavailable before launch. These experimental absolute-path descriptors are not native canonical snapshot-bound outcomes.

Checked **every Rspack and Sui entry**. Rspack ordinals28 and29 both retain the original nightly-only -Z refusal on the pinned stable compiler, respectively in L1 results[3] and Hy1 results[7]. Neither becomes an analysed entry. Sui ordinal30 retains the offline async-graphql Git-checkout failure; ordinal31 retains the offline sui-data-ingestion-core Git failure. Ordinal32 retains Move's target-resolution failure, with r7 REPORT.md:7 supplying the accepted symlink/no-follow cause. The coverage table correctly distinguishes that report's explanation from the receipt's generic target-resolution message.

The twelve analysed entries match the five accepted framed series. All five external pilot files equal their published receipt copies byte-for-byte. The newer accepted short-path SQLite success is used; its earlier zero-analysis history is not upgraded. The canary-runner bound refusal is correctly added to PLAN-r2's summary from H9, without changing a bound or repairing a source.

## Runner and raw observations

The runner selects the accepted U-3 site-walk v2 image and uses the unchanged closed framed-bin executor. The live wrapper equals the published accepted image: SHA-256 `070f92c01685fbe15963444be122216c60393d1cd6d35ec87bb1f29f63390234`. The executor/source pins equal the accepted controls-stage pin list and rehash successfully, including the framed-bin executor, root observer and inherited execution helpers. The runner rechecks those sources, wrapper, source map, command data and graph before every graph.

Independently counted **976 compiler children**, two runs per prepared entry. Per-run child counts for ordinals9,16,12,0,18,19,20,21,22,23,26,27 are respectively 21,18,29,58,66,24,73,73,62,56,1,7, summing to 488 per pass. Each run's unit index/standing/reason sequence exactly matches its accepted pilot. Every launched unit has one after_analysis event and one site_walk event, siteWalkVersion=2 and sitesAreNotCandidates=true. Normalized site observations excluding elapsed time match between both runs. No timing statistic is claimed.

## Audit and independent aggregation

Inspected the audit and checked its working script, raw input and output against the stage before execution. Ran exactly the permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-large-site-census-2026-10-13/audit_sm_large_site_census_r1.py`

It exited zero and reproduced large-site-census-checks-r1.json byte-for-byte: **10311 bytes**, SHA-256 `76c06ab8b4cdbc6d9ab3850ae8b1ffb3067b180f67a27ee6bf9fb9355f1ce4a0`.

The audit derives S from nonempty regular .rs files in verified public T2 store trees. Smithy's **1084** and Deno's **1052** subjects match RUST3-LIM. First-party site paths map to store-identical source bytes; neither workload has sites outside its subjects. Distinct covered subjects are 13 and 1 respectively. Dependency crates remain separate from workload subjects.

Independently regrouped raw run0 kind counts across the entries. All report aggregates match. Smithy's literal/control-flow totals are 99/178; Deno's are 10/7. Expanded/subtype annotations are not added again to base counts. These totals are observations across entry analyses, not deduplicated production candidates. The grouping is explicitly label-only, and the inherited derived-relation/query descriptions preserve G3's emission authority.

Zero workloads have exact coverage. The reported unit totals are Smithy three first-party analyses, 46 unavailable first-party unit occurrences and 477 dependency analyses; Deno one first-party analysis, one unavailable first-party unit occurrence and seven dependency analyses. Rspack and Sui have no analysed entry. No SM-11 quotient or SM-13/SM-14 value is derived.

## Scope and boundaries

No stage, requested key, emission factor, census kind or batching is chosen. Unavailable coverage remains recorded without invented results. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. SMComplete, LG1Met, effectiveL and productQualification remain false. The evidence is outside-product, preliminary and partial; native admission is not an extra experiment gate, and report assembly and remaining S-M work remain owed.

Only read-only inspection, hashing, JSON/source parsing, Git queries and the expressly permitted audit were used. Its authorized output rewrite was byte-identical. No compiler, Cargo, driver, runner, tests, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage, other working files nor control state was edited. Only this REVIEW.md and review.json were otherwise written. Nothing was pushed. Exact lead assent and fresh design verification before publication remain separate lead work.
