# Codex review: SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1, round 2

**Verdict: ACCEPT.** SM-U1-R1-RF-01 is resolved. No required findings or nonblocking observations.

## Exact subject and custody

Independently rehashed subject.json (13241 bytes, SHA-256 `6e5ec0bdb152afeeda3b877bf439eaeba037f9c0ee17bc6969739bae5498e3a5`) and all 53 members in `/tmp/opensip-implementation/sm-u1-r1-stage`. Every size and hash matches. Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `9e3492c05fa3cdf77fbabb594470b37e91f81f40`, with only the existing untracked held E2s tree, whose contents were not read.

Compared the round-1 manifest and retained original stage against this subject. Of the original 49 members, only PLAN-r3.md, make_plan_r3.py and REPORT.md changed. Each plan file changes only the comparison paragraph; REPORT adds only the round-2 disclosure paragraph. The four additions are the exact original subject, exact original plan/script copies and the round-2 freeze script. All experimental sources, controls, images' pin records, collections, executors, runners, measurements, audit and checks retain their round-1 bytes. The original subject's SHA-256 is `65884c39a0de99f8ca30d90cd33bd800d1d51fbc6a28684ebb88821c240eca0c`. The round-1 review was not modified.

## RF-01 and PLAN-r3

Recomputed the comparison from the accepted static-profile samples and the accepted remaining/axum-tokio context samples. Relative to context, ordinals 0–8 differ by **+0.412%, -0.444%, +3.597%, +0.898%, +7.774%, -0.507%, +1.961%, +0.751%, +0.687%**. PLAN-r3 and its authoring script give these nine values, identify the denominator and sources, call the comparison descriptive, disclaim equivalence and explicitly base the choice on the command-data boundary. The request's legacy “check the ~1% agreement” wording therefore does not require retaining the rejected assertion.

Reconstructed PLAN-r3 from accepted PLAN-r2 using the authoring script's literal replacements and splice, without executing it. The result matches exactly. Changes remain the revision heading/change table, D-5 and consequential U-1 wording; other definitions remain unchanged.

The D-5 choice is sound: U-1 uses actual static Cargo command data and the driver reads the prepared map from a file. The measured whole-graph boundary includes child start, hashing, decoding and bookkeeping, with coverage and incomplete units disclosed. The accepted producer's propagated unavailability prevented command construction for build-script-only libraries; the executor inherited that block. The framed whole graph includes repeated map streaming into every child, so its rejection for this chosen SM-4 boundary is justified. Its evidence remains retained.

## Producer, collection and executors

The round-1 independent source and graph checks remain applicable to these exact unchanged bytes and were corroborated by the freshly reproduced audit. The complete producer populations matched (3130 files), with exactly the two declared Rust source changes: build-script-edge filtering/OUT_DIR removal/disclosure, and the additional control. Existing unavailability seeds and other producer files remain unchanged. Cargo prepare_rustc constructs commands without executing build scripts. Accepted producer/image pins remain unchanged; all four retained controls pass.

All nine graphs equal accepted graphs modulo packet roots; previously constructed commands agree modulo packet/image roots. New commands are exactly the difference between the original unavailability closure and the closure excluding build-script edges: **36,19,18,0,9,3,11,9,3**. Their environments omit OUT_DIR and *_OUT_DIR. Build-script units themselves remain unconstructed. Maps retain accepted logical file/content populations, counts and bytes. Neither source trimming nor replacement repairs unavailable expansion.

Both executor variants retain the confined build-script-edge exclusions in argument/dependency/extern/transitive-metadata handling and the disclosure flag. Supported target/mode checks continue to exclude build scripts and proc macros. No new executor change was introduced in round 2.

## Series, incomplete units and history

Read all three archive members in memory, verifying index sizes/hashes and equality to named external originals. Archive SHA-256 remains `3ca1fe4456b72e9f413286ad223d7cbc40e003196fb95da6beb32049f082cebc`. No extraction occurred.

Rechecked all nine static-profile rows: ten runs each, three warmups and seven measured samples; recomputed median and maximum whole-graph spans. The successful series retains **2690 compiler children**, the recorded population/read-audit/metadata repetition, and every previously analysed unit. The detailed round-1 checks of these unchanged raw records remain valid. Recorded read observations do not establish complete runtime/sysroot read sealing.

Incomplete populations remain **5,4,6,0,3,2,0,3,2**. Retained serde_core stderr identifies absent env!("OUT_DIR") at the private.rs include; its dependants remain incomplete. Retained serde_derive_internals stderr refuses src/mod.rs outside the prepared map. No cause was repaired or converted into success. The new first-party successes remain napi_sys and the napi_derive_backend unit instances.

The unchanged metadata evidence supports the disclosed root explanation: old/new Hyper metadata each contains its packet root 54 times; nine additional root bytes explain the 486-byte size difference. Within-series metadata repetition is the control; this is no claim of complete cross-root semantic equivalence.

Framed records, runner and logs remain historical evidence, excluded from the selected SM-4 series. The previously checked r79 commit time falls within retained Napi warmup timestamps and precedes measured samples, supporting the disclosed warmup overlap. Retained attempt-0 evidence still records ten entry-0 graphs followed by the missing analysisElapsedNanos failure; the successful runner treats that unavailable instrumented interval as absent without changing the whole-graph boundary.

## Authorized audit and standing

Ran exactly `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/audit_u1_r1.py`. It exited zero and reproduced u1-checks-r1.json byte for byte: **51860 bytes**, SHA-256 `d194ede2d7346213bacd7526a8d214384aa3866f92667833530565c6479e4c15`, also equal to the staged checks.

No build script or proc macro executed in the reviewed series. No formal SM-4 value, F, T or outcome is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. O7, D3 and D13 are closed; only L-G1 remains open among L's gates. Native admission supplies no additional gate for this outside-product experiment. Exact lead assent and fresh design verification before architecture-only publication remain lead work.

Only read-only reading, hashing, JSON/source parsing, Git queries, in-memory archive inspection and the expressly authorized byte-identical audit rewrite were used. No Cargo/compiler/image/driver/runner/test/lane execution, network, pane or delegation; no private fixture, installation, keys or held-tree content was read. Neither repository, stage nor control files were edited. Only this directory's REVIEW.md and review.json were otherwise written.
