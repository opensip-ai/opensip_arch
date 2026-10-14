# Codex review: SM-RUST-SITE-CENSUS-r1, round 2

**Verdict: ACCEPT.** No required findings or new nonblocking observations. **SM-SITE-R1-RF-01 and SM-SITE-R1-NBO-01 are resolved.** Acceptance is for the supporting outside-product site census, not complete SM-11/SM-13/SM-14, full S-M, effective L or product qualification.

## Exact subject

Stage: `/tmp/opensip-implementation/sm-rust-site-census-r2-stage`.

Manifest: `subject.json`, 3,832 bytes, SHA-256 `c08a29106c1b8e223c22b8e7a8f88f32751456285b95911d0beb541c6b9fe612`. All **16 members** independently rehashed; no missing file, size mismatch or digest mismatch.

Product HEAD is clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `4bb9e62e39ce99d21cc629369e3c04179e6529c1`. Product lock remains 630,770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`, selecting inventory187 with 147 inventory successors and 161 contract successors.

## Finding resolution and round-2 scope

The audit's base predicate now rejects every key ending `.expanded` before applying the relation's prefix/kind rule. Its separate subset predicate strips that suffix and applies the base predicate. Both first-party and dependency relation totals use these separate predicates; per-covered-subject distributions use only the base predicate.

Independently recomputed all seven label groups for all nine entries from the retained raw site events. Every first-party/dependency base total and expanded-subset total matches the corrected audit output. Every subset is bounded by its base. Every per-covered-subject distribution's population, total, mean, median and maximum matches the corrected base-only computation.

The previously faulty examples now read:

| Entry | Base first-party declarations | Expanded subset, separate |
|---|---:|---:|
| napi-rs | 69 | 2 |
| axum | 3,268 | 2,411 |
| hyper | 759 | 102 |
| tokio | 3 | 2 |

Dependency declaration totals are corrected too: napi's base is 54,433, with 17,777 expanded observations reported separately. No expanded subset is added to a base total or distribution. Raw by-kind counters retain both total and subset as originally observed.

The report now explicitly states these subset semantics. It also correctly distinguishes use-item resolution categories from extern-crate item counts, resolving NBO-01.

Of the 14 file paths shared with round 1, **11 are byte-identical**. Only REPORT.md, the audit script and its derived output change. The round-1 freeze script is replaced by the round-2 freeze script, as permitted; the only other new member is `history/site-census-checks-r1-round1.json`, byte-identical to the original 22,761-byte round-1 audit output (`4aa7068c0c7b31e3faa8aecf196f8f39903cfce603a64a27e73fa5d135ffcef1`). The driver, site-walk module, image, build records/logs, runner, run log and raw census remain unchanged. No extra compiler or corpus run was introduced.

## Permitted audit reproduction

Ran exactly the permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-rust-site-decomposition-2026-10-13/audit_sm_rust_site_census_r1.py`

It exited 0 and reproduced the frozen round-2 output **byte-for-byte**: 28,008 bytes, SHA-256 `8afb57bca57c5f40642e4264d2ade58c5bd8a31b72bf7cf0fbeb52b7cb433ef2`. The external audit script and raw census match the staged members.

The unchanged subject recipe verifies the selected public T2 trees and counts nonempty regular `.rs` files; symlink files are excluded. All seven repository counts agree with RUST3-LIM: 239,192,301,98,208,71,808. The two overlay entries both give S=279 from the separate mounted 208/71-subject members; no missing historical count row is fabricated. Every mapped first-party site file passes store-byte equality. No first-party site is outside the workload subject set, and dependency counts remain separate.

## Variant, walk, build and runner

The closed driver source matches the committed framed-series copy. The variant still differs only in the rustc_hir/module additions, the named TyCtxt and the single site-walk call after the closed timing event. The walk's query meanings and outer source-callsite attribution remain unchanged; observations remain sites, not candidates. `.expanded` remains a subset annotation.

The image matches the unchanged build/receipt pin and original executable: 677,768 bytes, SHA-256 `d04be840c611ec01b65ff2fcb4c41bd0ec953150ace142ed2925880b89d14b9f`. The linked input pins also match. The unchanged build source/records use the closed bare-rustc recipe and the same pinned 1.95 rustc-dev sysroot path. No build was rerun or new sysroot qualification inferred.

The actual executor/observer bytes match their recorded pins and committed closed copies: executor `721572db3859afd9d72ac1dacba495803c320135036ff5414474b571b4f37e85`; observer `b55cf3e457e17042d01a1a1184f53ff124708d183bbe29e03243d418a356cb6b`. The unchanged runner rechecks these inputs, holds its owned lane for the run set, runs exactly twice per entry, compares accepted pilot populations and compares event contents excluding elapsed time.

Independently checked the raw two-run populations again. Each unit's index/standing/reason equals the accepted pilot. Per-run child counts are 66,48,32,7,2,2,16,2,2, yielding **354 compiler children** across both runs. Every launched unit records one after-analysis and one site-walk event, completed analysis/metadata standing and `sitesAreNotCandidates=true`. All raw site event contents excluding elapsed time repeat exactly.

## Scope and remaining work

The NE:590–601 relation grouping remains label-only. It supplies no stage, requested key, emission factor, census symbol kind or batching policy. Fixed byte overheads are explicitly not supplied. The corrected partial site summaries are not semantic candidate volumes or SM-13 per-stage values.

No workload has exact subject coverage: covered-subject counts remain 4,0,19,18,0,0,1,0,0. **workloadsWithExactCoverage=0.** No SM-11 analysis/RSS quotient is derived; covered-subject site distributions are diagnostic summaries. No SM-13 or SM-14 value, scratch measurement, full S-M completion, L-G1 satisfaction, effective L or product qualification is claimed. Native admission remains a separate product obligation and is not imposed as an extra gate on this outside-product experiment.

## Boundaries

Only read-only hashing, JSON/source inspection, Git queries and the expressly permitted audit were performed. The audit's allowed external output rewrite was byte-identical. No compiler, Cargo, driver, runner, tests, lane, network, other panes or delegation were used. No private 413 fixture, installation directory, signing keys or held-tree content was read. No repository, stage, producer or control file was edited. Only the requested REVIEW.md and review.json were otherwise written. Nothing was pushed. Exact lead assent and fresh design/implementation verification before publication remain separate lead work.
