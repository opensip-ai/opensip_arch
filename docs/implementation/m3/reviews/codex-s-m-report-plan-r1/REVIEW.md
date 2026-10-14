# Codex review: S-M-REPORT-PLAN-r1

**Verdict: REQUIRED-FINDINGS.** Two required findings and one nonblocking observation. D-1's explicitly synthetic convention is permissible without a real-workload bound; D-2 matches the dependency-source contracts. D-9 and the remaining-work coverage need correction before this plan can be accepted.

## Exact subject and boundaries

Reviewed `/tmp/opensip-implementation/s-m-report-plan-r1-stage/subject.json`: 852 bytes, SHA-256 `8b061e6d84ed46e7950f3016f642d1f48ee65e9d8ad484b8debf8a14117128b3`. All three members were independently rehashed and match:

| Member under docs/implementation/m3/s-m-report-plan | Bytes | SHA-256 |
|---|---:|---|
| PLAN-r1.md | 16828 | 372d3d8d97898c4c7cb08b5dd902f317a288e3ccf2b21ad67569705f1a3977e9 |
| gap-inventory-2026-10-13.md | 46306 | 8ca97e6ecea09ff316ef9f7a11d17c0a4c63463713f958ecdaa8e9c149d82e12 |
| runners/freeze_s_m_report_plan_r1.py | 6403 | c5778b08123e16b58237c73de4c928c6b6c9ce9fa9d62eb2e8885e6bd7fa8920 |

Product HEAD is `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean. Architecture HEAD is `5d474f97f9d41564999e6ccc6247f6bc487a23e3`; its pre-existing untracked held E2s directory was not read or changed. The gap inventory was used to locate questions, not to accept its derived numbers. Conclusions below rely on the law, contracts and accepted records.

Only read-only file inspection, hashing, JSON parsing and Git queries were used. No compiler, Cargo, tests, driver, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Only this REVIEW.md and review.json were written; neither repository, stage nor control state was edited. The freezer was inspected, not executed.

## Required findings

### SM-REPORT-PLAN-R1-RF-01 — D-9 substitutes an estimated capacity for admitted rows

PLAN-r1.md:98-99 defines the required first term as `min(100000, floor(4 MiB / measured descriptor bytes per row))`, with the actual workload row count merely beside it. U-4 at :108 would then record that result.

M3-L r6 :559 asks for measured inventory rows, total bytes and canonical descriptor bytes against their separate bounds. At :591, the S-M part is “snapshot2's admitted rows, from SM-5”; :620 rejects invented or estimated figures. The descriptor's average byte cost does not establish an exact ceiling for a larger, unspecified population. Row encoding depends on paths and other row content, and the descriptor also has overhead that is not a constant per-row charge. An exact measurement of one descriptor does not make an extrapolated capacity exact.

**Required correction:** record each required workload's measured snapshot2-equivalent population, exact row count, descriptor bytes, total bytes and standing against the bounds from SM-5. Any average-based extrapolation must be labelled estimated/informational and kept outside the required admitted-row term. An alternative exact capacity derivation would need an explicitly fixed population and independently reviewable admission/encoding evidence. Do not fill final S_eff or choose later-owned parameters.

This makes `definitionsWithinItem9Authority=false`: the report may fix a benchmark convention, but cannot turn this estimate into the required measured admission term under the cited authority.

### SM-REPORT-PLAN-R1-RF-02 — Large-workload pre-effect coverage is incomplete in the unit list

U-3 at :107 reruns the nine medium prepared entries. The follow-up at :112 names only Smithy and Deno graphs “as information,” justified by the absence of an outcome dependency. U-4 does not explicitly account for the remaining large-workload coverage and census inputs.

M3-L r6 :571 includes smithy-rs, rspack, deno and sui if S-P permits. At :586-591, the S-M round owes its part **for each workload above**: exact S, labelled analysis/RSS coverage, independent host scope derivations, site decomposition and formulas. At :577, “No outcome (A) to (C) depends on them” separates their use from medium-budget outcomes; it does not waive those pre-effect inputs. Thus completing the listed units need not supply all required large-workload records.

**Required correction:** add an explicit workload/figure coverage matrix and unit assignments for all these workloads, including sui's S-P condition. Identify accepted exact S and host derivations; labelled analysis/RSS coverage or substantiated unavailability; and outstanding site observations, query mappings and formulas. Put the necessary large-workload census/coverage work before U-6. Honest partial/unavailable coverage is acceptable where supported: this finding does not demand repository execution, native admission, unsupported per-subject quotients or post-effect worker measurements.

## Definition and citation checks

**D-1:** the synthetic graph convention can be adopted as a labelled SM-9 benchmark under :563 without asserting that it bounds real compiler output or real replay cost. It selects fixture behavior rather than binding G3's production emission factor. The explicit no-bound disclosure at :34 preserves the substance of SM-REPLAY-SIZED-R1-RF-01. The accepted round-2 replay review accepted the measurements as scenarios and established no real-workload inference; this plan cannot retroactively change that acceptance. The control correction's “real SM-9” consequence remains valid for claims about real replay cost; it need not prohibit an explicitly defined synthetic benchmark. No real graph wait or new native-admission gate is required for that benchmark.

**Nonblocking SM-REPORT-PLAN-R1-NBO-01:** :31 calls all Rust S subjects “analysed sources,” whereas the accepted site census REPORT.md:35-43 and :47 records partial or zero first-party coverage. Prefer workload input/source-count scenarios and carry actual coverage beside them. The “smallest graph” language is not a proof of a minimum real replay graph. Any eventual F/T or outcome using D-1 must retain its synthetic convention, not acquire an unproved real-workload bound.

**D-2:** NE:612, :1687, :1693-1697, :1706-1707 and :2863-2864, DS4-P1 CONTRACT.md:5 and M3-C r7:600 support activated admitted non-path membership, path custody in the snapshot, separate acquisition population and snapshot-before-dependency transport. The accepted dependency-fragment REPORT.md:2 records axum's 187 packages/7338 files; the map-transfer REPORT.md:11 records 6403 files for its different map population. The accepted map transfer does not complete normative SM-7. U-2 is appropriately new work over that population; outside-product experiments do not require completed native admission.

**D-3 to D-6:** the overlay's separate children, repeated startup and expanded whole-process/whole-graph analysis spans are disclosed rather than silently treated as start-free spans. The context-series REPORT.md:7 supports the hashing/decoding/bookkeeping disclosure. U-1 is explicitly a new variant and leaves the closed executor unchanged. Its measured coverage must accompany the result. D-6 chooses the observable single public compiler API call; the accepted TS records retain those timings and expressly distinguish them from whole uninterrupted event-loop blocks. The per-file/program granularity warning must accompany the D-law use. Overlay statistics should be formed from corresponding per-run sums before taking the median/maximum.

**D-7:** harness DESIGN.md:798-807 confirms fresh processes, priming, declared cache treatment, separate reset fixtures and page-cache recording before every cold run including warmups. The warm convention with no declared persistent analyzer caches is permissible as stated. U-5 must preserve that absence or clear any disposable state/caches it introduces, in addition to the recorded page-cache state; page-cache flushing is not required or claimed.

**D-8:** the accepted Rust-scope REPORT.md:7 discloses whole-process wait4 RSS rather than incremental heap. The accepted T2-manifest interpretation is consistent with the outside-product subject recipe and does not add native admission as a gate. Later worker/domain-key inputs remain deferred.

Cited source passages and retained numbers checked above are accurate; the D-9 interpretation and missing coverage are substantive defects rather than incorrect quotation. No G3/C4a-owned parameter is chosen.

## Standing

No placeholder, F, T or outcome is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. O7, D3 and D13 remain closed; L-G1 remains open. Accepted experiments and prior findings remain closed in their exact scopes. Exact lead assent and fresh verification before any architecture publication remain the lead's separate work.
