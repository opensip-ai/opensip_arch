# Codex review: SM-RUST-SITE-CENSUS-V2-r1 (U-3), round 2

**Verdict: ACCEPT.** No required findings or nonblocking observations. **SM-SITE-V2-R1-RF-01 and SM-SITE-V2-R1-RF-02 are resolved.** Acceptance covers the medium-workload site decomposition and corrected fixed-byte/formula desk record, not actual SM-13/SM-14 values or complete S-M.

## Exact subject and preservation

Stage: `/tmp/opensip-implementation/sm-rust-site-census-v2-r1-stage`.

`subject.json`: 5753 bytes, SHA-256 `22455958a1aca19062de2ca19fddfb1abcdabd3504ee071e698818404c072f2f`. Independently rehashed all **24 members**; every size and digest matches.

The original 4566-byte manifest is retained as history/round1-subject.json, SHA-256 `3329b4f3eae4195411839224e4f4acb843e8ff6a81bbb50cb275a599b91e68e2`. All nineteen original member pins remain represented by unchanged current bytes or exact historical copies. Only REPORT.md, derive_sm13_fixed_bytes.py and sm13-fixed-bytes.json change among original paths. Their exact originals are retained under history/round1-*. The original freeze script remains unchanged; a round-2 freeze script is added. The census, audit, source, image, build records, runner and retained failed attempt are unchanged. The round-1 review was not modified.

Live bases match clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `63cee2f5f49e929ef825fb0b0dd5ad586cdc61dc`. Architecture's existing untracked held E2s directory was not read or changed.

## Round-1 findings

**RF-01:** the occupancy fixed total now includes the required schemaVersion=1 value: map head plus ten encoded keys plus one fixed uint byte = **140**. The derivation, JSON and report agree. Near-clone candidateFixedBytes remains 334 as a partial fixed component, but candidateFixedBytesExcludes explicitly names text(resolution_near), and perCandidate.variable now adds that required unbound term. The owner remains unresolved under A6; no resolution is invented. The spool and payload formulas include the candidate's named variable members, so the value no longer silently contributes zero.

**RF-02:** the general frame formula now uses factBatchFrames_stage from the **unset G3 batch partition**, subject to nonempty batches, the candidate-count cap and frame bounds. The payload formula sums over that same partition. ceil(C/B) is retained only as the explicitly conditional uniform-full-packing case. C4a grouping and the response-frame-scope reading remain unresolved; no packing policy is selected.

## Independent fixed-byte checks

Recomputed sizes from schema-required fields and fixed values using an independent CBOR head/key calculation, without importing the submitted derivation. All seven cited source files match their recorded hashes.

| Component | Independently checked fixed bytes |
|---|---:|
| Candidate common | 290 |
| literal@syntactic | 345 |
| calls@resolved-callee | 349 |
| Source-span anchor | 74 |
| Spool entry wrapper | 35 |
| FactBatch envelope | 78 |
| FactBatch V2 / V3 | 47 / 82 |
| Occupancy companion | 140 |
| Census row / complete container | 61 / 35 |

Also recomputed all eleven relation rows. They match 347, 345, 355, 353, 360, 349, 341, 366, 355, 334 excluding the unresolved near resolution, and 362 respectively.

Checked the other fixed constants: candidate schemaVersion and known relation/layer/resolution strings; producer/language and the fixed-length source-universe encoding; source-span kind and null factId; envelope direction/frameType/protocol-major encoding; FactBatchV3 schemaVersion=3; occupancy schemaVersion=1; and complete-census state=complete. No additional omitted constant was found in these fixed components. Variable text/integer/byte-string/array sizes remain variable. The 74-byte anchor is specifically the source-span variant, not an assertion that every anchor variant has that size.

RPP's exact spool-entry CBOR and 40-byte prefix exclusion remain correctly distinguished. The report names the lead-written reference head counter and its standing, as well as the proposed census schema's standing. A1-A6 remain explicit readings/unresolved terms rather than new binding choices. The added partition term removes the previously unstated packing assumption. The corrected records satisfy the fixed-byte decomposition requirement without establishing candidate volumes or final resource bounds.

## Census, source and run checks

The retained v1 source still equals the accepted r1 walk, SHA-256 `fedaa40df44fd2e76a5cea4abb4d2e6fb8efaf031aaa7bb7a19ec3a591674881`. The reviewed source diffs are unchanged: v2 adds literal expression/pattern counts and the stated control-flow HIR kinds, their rustc categories and the version marker; the driver adds rustc_ast to the r1 instrumentation. The site walk remains after the closed timing event. NE literalKind/edgeKind mapping stays with G3.

The runner still differs from the accepted r1 runner only by v2 names/labels and the v1-source pin. The executor/observer match their closed accepted copies. The original built image equals the staged image: 679416 bytes, SHA-256 `070f92c01685fbe15963444be122216c60393d1cd6d35ec87bb1f29f63390234`. Build records and sources remain at their round-1 reviewed pins; no build or image execution occurred.

Independently recounted 354 launched children across nine entries and two runs each, checked each population against the accepted pilot index/standing/reason map, and compared normalized site events across both runs. Every launched unit has one after_analysis and one site_walk event. Populations repeat and counts are deterministic. The unchanged v1 equality audit reports zero mismatches. The retained priority-error first attempt remains a failure before lane acquisition or compiler work.

The new groups exclude expanded and subtype counters from base totals. First-party subjects and dependencies remain separate. Reachability and near-clones are expressly described as derived, and the compiler-query table continues to match the preserved source. Zero workloads have exact coverage; no SM-11 time/RSS quotient is derived. Site distributions remain site observations, not candidate counts.

## Permitted reproduction

Checked the authorized scripts and their working inputs/outputs against the stage before execution. Ran exactly the two permitted `nice -n 10 python3 -I -B` commands. Both exited zero and reproduced their outputs byte-for-byte:

| Output | Bytes | SHA-256 |
|---|---:|---|
| site-census-checks-v2.json | 111830 | 624b0519aca326f96fbaa2d9da5f6c8677281f6fa9187392d750162788cf462e |
| sm13-fixed-bytes.json | 9940 | 24ed5146289373bef71785bb43510fb346d11e01104f15dd7ce61e2394d8a341 |

## Standing and boundaries

No stage, requested key, emission factor, census kind, batching policy or scratch value is chosen. No SM-13 or SM-14 value is derived, and sites remain labelled sites, not candidates. Large-workload inputs remain U-7's; other measurement and report duties remain owed. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. SMComplete, LG1Met, effectiveL and productQualification remain false. Native admission is not an additional experiment gate.

Only read-only inspection, hashing, JSON/source parsing, Git queries and the two expressly permitted scripts were used. Their authorized output rewrites were byte-identical. No compiler, Cargo, driver, runner, tests, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage, other working files nor control state was edited. Only this REVIEW.md and review.json were otherwise written. Nothing was pushed. Exact lead assent and fresh design verification before publication remain separate lead work.
