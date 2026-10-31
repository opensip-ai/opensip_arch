# Independent review: GUARD-AMENDMENT GA-r1 / LD-Q-165-B

GUARD-AMENDMENT: ACCEPT

Reviewed 2026-10-31. This is acceptance of the exact narrow LAW-CLASS amendment, for subsequent coordinator adoption. No BLOCKING findings; two CARRIED observations below.

## Authority, route, and custody

- Request: `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/review/REQUEST-guard-amendment-c2b.md`, SHA-256 `d9cb7faf7dd9b757bdc71b3b95d3ed027bfabc90b8793ed4092dbc69a6e8f490`, matched.
- Canonical architecture: `/Users/sb/code/opensip-ai/opensip_arch`. Read START-HERE for orientation, IMPLEMENTATION-STATUS for bounded M3 standing, current control state and ACTIVE-PLAN top, the delegated live MAP, and AGENT-MODEL-ROUTING. MAP's architecture pin `c4dfdb5f9` is older than the observed architecture HEAD `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`; product main still matches `dd89db11a33e7b67d8ca7dce74368a56c4808231`. This review uses the exact current request and pinned LD-Q-165-B handoff, not an older unit example or MAP checkpoint as amendment authority.
- Before substantive review, `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/tools/agent_model_route.py check --provider codex --route R3-FRONTIER` returned exit 0: `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high`. Reviewer vendor Codex is independent of Claude author w2C.
- All 17 request-listed SHA-256 pins matched, including the eight manifest members and both copies of the C2a patch. Rechecked before writing; all 17 evidence files have no write permission bits. The request itself also matched. No frozen bytes were modified.
- Subject document SHA-256: `b7d6c489824dd3fdb612000e95932bdd11787c28c36e256753bc38da937bb277`. Guard patch: `7e5611d34ebd6fcce7292229035a750b506a4c9b361728afd7873a186adb6768`. Manifest: `5d4e3298fa2f8168a40af610f78cac93511b058292cc4f7a32c608fecd008eec`.
- Reconstructed every patch hunk in memory against H4 `a03407dbf344dc646e50c4b7dff69c8be99ab0b3`, checking context and hunk counts. The two results equal both pinned after-copies and the development worktree files. The separate three-file C2a patch also reconstructs that worktree exactly. Its combined diff SHA-256 is `526ffc7776eda54f8173283495e3d456565e5941791fc926ed774ddc0cd63402`, matching the prefix in validate-r2.out. No patch was applied on disk.

References below: `E/` means `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/evidence/h5/guard-amend/`; `creator` and `doctor` mean its `guard-amend__GA-creator_commands_tests.rs.after` and `guard-amend__GA-doctor_tests.rs.after`. Product sites are at H4 unless stated otherwise.

## Answers to the four requested review questions

1. **Doctor opt-in graph: accepted as narrowly amended.** `doctor:912-924` adds only `"profile-allocations": []` to host's exact expected feature object. `doctor:1026-1042` still rejects any mismatch, including a default key, additional feature, or forwarding element. `doctor:967-980` adds the endpoint to the guarded feature set. The existing all-package forwarding walk (`1116-1147`) follows resolved aliases, including weak `alias?/feature` forwarding; the dependency walk (`1149-1189`) follows resolved package IDs and declaration kinds. `profile-allocations` is absent from the dev exceptions at `1178-1185`, so normal, dev, and build dependencies onto the selected host are all refused. This is stricter than the ruling's outside-host-dev minimum and does not introduce an unnecessary self-dependency exemption. Existing measurement/scenario exceptions remain unchanged. H4 `crates/host/Cargo.toml:35-62` declares an empty, nondefault feature and requires it for the allocation test target. Host `lib.rs:118-122` refuses feature-enabled builds without debug assertions. The exact cfg semantics, rather than an assumption that debug builds imply tests, are the accepted boundary.

2. **Creator guard: accepted as a five-line literal exception.** `creator:497-504` binds the support block to `pub mod typescript_profile_support;` and the controls block to `mod typescript_profile_controls;`, retaining the already permitted `#[allow(dead_code)]`. The strings match H4 `crates/host/src/lib.rs:118-122,128-130` exactly, each once. The substitution removes four support lines and one controls line, and no declaration. `creator:568-577` admits zero or one occurrence of each complete block and refuses duplicates; edits to the module name, attributes, or compile-error text do not match. The pinned prefix, single adapter count, next export, operability identifier refusal, no-`!`/no-`*` rule, four pre-existing attribute spellings, and residual attribute/identifier refusal remain at `583-626`. `has_creator_commit_symbol` still scans the original text after removing only the single logging adapter (`719-728`); the normalized block text is used only to decide eligibility for that adapter exception. No arbitrary macro, hidden module, feature cfg, or creator/commit symbol is erased from the symbol scan.

3. **Other rules and negative controls: preserved within this amendment.** The patch touches only the two test files. It leaves the production scanners, resolved logging-crate binding, selector checks, CLI behavior checks, existing constants, and pre-existing negative assertions intact. The pinned H4 report records exactly the two named guard failures, with candidate workspace exit 101; the corresponding log sites are `candidate-workspace-tests.log:21-29,46-54`. The pinned r2 validation records both amended real-tree guards passing, creator 9/9 and doctor 8/8, with the new control names explicitly present. This is supplied execution evidence, not a fresh reviewer run.

   The new creator cases (`creator:519-565`) are: **a block twice; doc(hidden) on another module; the compile_error! line alone; the block bound to another module; the feature cfg on another module; a line injected inside the block** (`#[macro_use]`); **the controls cfg without its allow line; another feature in the cfg** (`crash-matrix`). Each must make the adapter predicate false. Positives cover both blocks absent and both exact blocks present.

   The new doctor cases (`doctor:1705-1762`) are: **profile-allocations in host's default; profile-allocations forwarding into the metered crate; a cli feature forwarding into profile-allocations; dependency activation for normal, dev, and build kinds**. Each must make feature closure false.

   Retained creator controls (`creator:732-869`) include direct/method/qualified/imported/raw and containing-name finalize symbols; a same-named bridge, renamed binding, alternate logging/host source; wrong host or unbound logging; nested/duplicate adapters; operability shadowing; glob import; alias macro; macro_use; token-separated attributes; compile_error rebinding; changed adapter body and an additional storage finalize call. Retained doctor controls (`doctor:1646-1704,1764-1860`) include defaults and unknown features on all eight selected packages, foreign manifests/sources, retargeted forwarding aliases, direct harness-feature activation in all three dependency kinds, changed forwarding, duplicate selected package, wrong/foreign measurement source and missing resolve data. Their assertions remain unchanged, and the supplied full-suite success includes them.

4. **Rationale and minimality: accepted for the current bytes.** The support file uses host-private `typescript_config` and `typescript_profile_controls` (`crates/host/src/typescript_profile_support.rs:6-9`); host forbids unsafe code (`lib.rs:1`), while the separate allocation test implements an unsafe counting allocator (`tests/typescript_profile_allocations.rs:34-55`). These substantiate the relocation costs described in LD-Q-165-B. The requirement for a 228-mutant re-sweep/funding re-review is the coordinator's pinned process ruling, not a new execution result or a proof that every conceivable alternative is impossible. The document's rationale is a compressed account of that ruling. The guard change admits precisely the existing feature and five lines, with stronger module/block binding than a general per-line whitelist. The separate C2a patch removes its five offending attribute occurrences; it does not alter the C2b-1b blocks. No production API widening or allocator relocation is part of GA-r1.

## Exact H4 byte pins checked independently

All hashes are SHA-256. Block hashes include their terminating LF and include the module declaration (and the controls' existing allow line), exactly as matched by the guard.

| Bytes | Hash |
| --- | --- |
| `crates/host/Cargo.toml` | `0d9cf05ce826c07c29c41dea1da541cc13785272809d0fe2d400b10bcaebcbc9` |
| `crates/host/src/lib.rs` (whole H4 file) | `be1bbad5fb836ccb6ab17314bc2cb1f980ac3a9f1e71dc6dfa0af6151dab8ad0` |
| `profile-allocations = []` plus LF | `b74e86e9733bcf4a7cced886c7f0562fbdae4b6869728d674f9beb8d2e92e86a` |
| Exact `C2B1B_PROFILE_SUPPORT` input block | `b31c5e1ee5019c8f6e3e01bd25563cc28132593d6e2338dcb59348136744f239` |
| Exact `C2B1B_PROFILE_CONTROLS` input block | `24e92a0c6a85c8b4140eb020e2704253dc4d6809866d0056249b7215606f075a` |
| `crates/host/src/typescript_profile_support.rs` | `916a057dd00e9f03a8c9cbd3ee51a35f0e31f591f8dd6d65868b88ff60294b2e` |
| `crates/host/tests/typescript_profile_allocations.rs` | `d4189dd8fc91f7e75730f5a869b70eb5f3d9ae56521d8058a0aabd43c5c36f67` |
| Creator after-copy | `9e73b5d790fd2cf7b85be99d943255fbc792ac0da905f710fea47eca1b919c4f` |
| Doctor after-copy | `f50f76b81b637ed76d348518aca3046451e0917af22d7a9fa8f102e733ca92bc` |

The two admitted blocks remain byte-identical in the composed development candidate. The whole host lib.rs does change for C2a; this review does not mistake block identity for whole-file identity or a completed funding-transfer verification.

## Findings

- **GA-1 — CARRIED — stale forwarding comment.** H4 `crates/host/src/lib.rs:115-117` says the feature forwards `metered-test-support`; the actual manifest has `profile-allocations = []` and enables the observer through host's metered dev-dependency. `E/guard-amend__GUARD-AMENDMENT-GA-r1.md:48-51` explicitly acknowledges this. The assertion and amended guard rely on actual manifest bytes. Keep the frozen bytes unchanged here; correct the comment through a separately authorized successor with its required transfer checks. This does not block the five-line amendment.
- **GA-2 — CARRIED — validation wrapper is not a fail-closed reusable gate.** `E/guard-amend__validate.zsh:5,15-19` uses only `set -u`, reports rustfmt failure without stopping, pipes test output through grep without capturing Cargo's status, and prints the Clippy pipeline status without enforcing it. A failed test or compiler error can therefore leave the wrapper exiting successfully. The present verdict relies on the pinned r2 log's explicit successful test summaries and printed rustfmt/Clippy statuses, plus exact patch/source review; it does not certify the wrapper exit status. Before reusing this script as an acceptance gate, retain complete outputs and require each producer's exit status. The subsequent H5 lane and re-carries remain required by LD-Q-165-B. This limitation does not alter the guard predicates or invalidate the explicit 9/9 and 8/8 results in this receipt.

## Evidence boundary

Reviewer actions were read-only hashes, Git/source inspection, metadata inspection, and in-memory patch reconstruction; the only written artifact is this review. No Cargo/Rust tests, mutation sweep, lane, receipt refresh, private store, real-home fixture, installation, or signing operation was run by the reviewer. Supplied r1 validation remains history; r2 is the pinned developer validation, with the GA-2 limitation above.

Acceptance covers only GA-r1's exact law amendment and two guard diffs under LD-Q-165-B. It precedes and does not perform coordinator adoption. It does not accept C2a's source fix as a separate unit, certify funding/sweep transfer, complete H5 binding or integration, establish production enforcement, or confer unit/product qualification. Future adoption and execution must use the exact reviewed bytes and retain the coordinator's remaining gates.

GUARD-AMENDMENT: ACCEPT
