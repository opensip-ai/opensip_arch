# Codex review: SM-RUST-SITE-CENSUS-V2-r1 (U-3)

**Verdict: REQUIRED-FINDINGS.** Two required findings in the desk byte/formula decomposition; no nonblocking observations. The census variant, retained runs and reproduced audit otherwise check out. Preserve those measurements while correcting the accounting record.

## Exact subject and boundaries

Stage: `/tmp/opensip-implementation/sm-rust-site-census-v2-r1-stage`.

`subject.json`: 4566 bytes, SHA-256 `3329b4f3eae4195411839224e4f4acb843e8ff6a81bbb50cb275a599b91e68e2`. All **19 members** independently rehashed and match their declared sizes and digests. Bases match clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `63cee2f5f49e929ef825fb0b0dd5ad586cdc61dc`. The architecture's pre-existing untracked held E2s directory was not read or changed.

Only read-only inspection, hashing, JSON/source parsing, Git queries and the two expressly permitted scripts were used. No compiler, Cargo, driver, runner, tests, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage nor control files were edited. The two authorized working-output rewrites reproduced their staged bytes exactly. Only REVIEW.md and review.json were otherwise written.

## Required findings

### SM-SITE-V2-R1-RF-01 — Required wire values are missing from the byte decomposition

At derive_sm13_fixed_bytes.py:42-43, `occ_fixed = 1 + keys(*occ_keys)` counts the ten-key occupancy map's head and key encodings, yielding 139. The cited product occupancy-v1.schema.json also requires `schemaVersion` with **const 1**. That fixed unsigned value occupies one additional CBOR byte. The exact fixed portion is therefore **140**, not the 139 claimed in REPORT.md:90 and sm13-fixed-bytes.json. The companion formula has no named variable term that accounts for this missing constant.

There is a second omitted-value case in the candidate decomposition. At :32-35, the near-clone row deliberately leaves resolution unset and excludes its text encoding, yielding 334 bytes. That is a valid partial fixed component, but :50-54 lists the variable members and defines candidateBytes as fixed plus those members without adding the encoded resolution. Merely naming A6 does not insert the missing bytes into the spool/payload formula. FactCandidateV1 still has a required resolution member; an unset value must remain an explicit term rather than contribute zero.

**Required correction:** include the schemaVersion=1 byte in the occupancy fixed total, or accurately label 139 as head-and-keys only and include the constant separately. Add `text(resolution_near)` as an explicitly unset, owner-bound A6 term and label 334 as excluding that required value. Propagate the corrections through the derivation, output and report. Preserve the census observations and all unbound parameters.

Actual review value: `fixedBytesCorrect=false`.

### SM-SITE-V2-R1-RF-02 — The frame formula assumes a packing rule not supplied by G3

At derive_sm13_fixed_bytes.py:59, the general formula uses `ceil(candidates_stage / batchSize)` as the FactBatch frame count. The source contracts constrain nonempty candidate arrays and their maximum count, and RPP separately bounds frame payload bytes. They do not require all nonfinal batches to fill one uniform count-based size. M3-L r6:589 expressly leaves batching to G3.

For example, four candidates under a count cap of two may be partitioned into batches of sizes **1, 2, 1**: three frames, while the expression produces two. Variable byte sizes and owner-selected flush rules can also require nonuniform batches. No concrete batchSize has been assigned here, but the formula still silently assumes a relationship between count and batch partition. The report calls it a closed formula and says no reading is chosen without stating this condition.

**Required correction:** use an explicit G3-owned, unset actual batch partition or batch-frame count in the general formula, retaining unset C4a grouping and the response-frame-scope reading. Keep the ceiling expression only as an expressly conditional uniform-full-packing case if useful. Do not choose a packing policy or rerun the compiler census.

Actual review value: `ambiguitiesStatedNotChosen=false`, because the general frame formula contains an unstated packing assumption. `ownedParametersChosen=false` remains appropriate for concrete binding: no stage, key, emission factor, census kind, batchSize value or worker scratch count has actually been assigned. That absence does not make the assumed frame formula valid.

## Variant, build and retained runs

The retained site_walk-v1.rs equals the accepted r1 walk byte-for-byte, SHA-256 `fedaa40df44fd2e76a5cea4abb4d2e6fb8efaf031aaa7bb7a19ec3a591674881`. The diff adds expression literals, pattern literals, rustc LitKind labels and the stated control-flow HIR variants; it also records siteWalkVersion=2. The driver retains the r1 instrumentation and adds only `extern crate rustc_ast`. The walk still follows the closed after_analysis timing event.

The source matches the query table: literal expressions use ExprKind::Lit; pattern literals use visit_pat_expr/PatExprKind::Lit; match and loop have rustc source-category subsets; short-circuit counts use BinOpKind::And/Or. NE literalKind and edgeKind mapping remains with G3. Derived reachability and near-clone relationships are expressly stated without claiming independent candidate counts.

Build sources and linked-artifact pins match their retained bytes. The original built image equals the staged image: 679416 bytes, SHA-256 `070f92c01685fbe15963444be122216c60393d1cd6d35ec87bb1f29f63390234`. The retained recipe is bare rustc against the pinned 1.95 rustc-dev sysroot, not Cargo. Empty build logs are retained; the image was not executed in this review.

The runner diff from r1 is confined to v2 names/labels and the v1-source pin. The executor and observer equal the accepted closed files, respectively SHA-256 `721572db3859afd9d72ac1dacba495803c320135036ff5414474b571b4f37e85` and `b55cf3e457e17042d01a1a1184f53ff124708d183bbe29e03243d418a356cb6b`.

Independently counted **354** launched children over nine entries and two runs each. Every launched unit has one after_analysis event and one site_walk event and completes analysis. Every population matches the accepted pilot index/standing/reason map. Per-unit events excluding elapsed time are identical across runs, and every old v1 per-file kind count matches in both v2 runs. The retained first-attempt log fails at the runner's initial setpriority call, before output creation, lane acquisition or compiler launch; it is not upgraded to a successful run.

## Audit reproduction and independent arithmetic

Before rerunning, checked both scripts and their working inputs/outputs against the stage. Ran exactly the two permitted commands with `nice -n 10 python3 -I -B`. Both exited zero and reproduced their outputs byte-for-byte:

| Output | Bytes | SHA-256 |
|---|---:|---|
| site-census-checks-v2.json | 111830 | 624b0519aca326f96fbaa2d9da5f6c8677281f6fa9187392d750162788cf462e |
| sm13-fixed-bytes.json | 8899 | 0c210aaefd135830217319a67a6e76abd340e82d16be6edc712ca737bdee6dae |

Reproduction confirms the submitted arithmetic and observations, including the accounting defects above. The audit verifies the permitted T2-store subjects and maps first-party site files to store-identical bytes. Dependencies remain separate. Macro-expanded and literal/control-flow subtype counters are not added again to the base groups. Zero workloads have exact coverage; no SM-11 time/RSS quotient is derived. Covered-subject site distributions remain labelled site statistics, not candidate or complete-workload resource statistics.

Independently recomputed CBOR head/key/value sizes from the cited required fields, without importing the derivation:

| Component | Checked fixed bytes |
|---|---:|
| Candidate common | 290 |
| literal@syntactic candidate | 345 |
| calls@resolved-callee candidate | 349 |
| Source-span anchor | 74 |
| Candidate spool entry wrapper | 35 |
| FactBatch envelope | 78 |
| FactBatch V2 / V3 | 47 / 82 |
| Occupancy companion, including const schemaVersion=1 | **140** |
| Census row / complete container | 61 / 35 |

All seven cited fixed-byte source pins match. RPP confirms the spool's exact semantic-value CBOR and the 40-byte framing prefix exclusion. FA-2 census exported is a text enum, correctly treated as variable text; its rows and paths arrays and token sequence remain variable. The encoder is named and disclosed as lead-written; the proposed census schema's standing is also disclosed. Ambiguities A1-A6 are listed, but the omission of A6's variable bytes and the unstated packing assumption must be corrected before the decomposition is complete.

## Standing

Sites remain labelled **sites, not candidates**. No SM-13 or SM-14 value is derived, and no final S_eff, F, T or outcome is recorded. Large-workload inputs remain U-7's; coverage changes and other report units remain owed. O7, D3 and D13 remain closed; L-G1 remains open. SMComplete, LG1Met, effectiveL and productQualification remain false. Native admission is not an extra experiment gate. Nothing was pushed; exact lead assent and fresh design verification before publication remain separate lead work.
