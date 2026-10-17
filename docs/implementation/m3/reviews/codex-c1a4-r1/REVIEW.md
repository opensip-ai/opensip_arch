# C1A4-r1 review

**Verdict: ACCEPT-UNIT.** No required findings; two non-blocking observations below. This accepts the constructor, classification remedies and lead-readable census work. The separate blind validation and receipts remain owed; no held-out margin or whole-C1a completion is accepted here.

Subject manifest SHA-256: `65124de040d5b858e7f6f289ed2afc5bbd6ac1c60ca6f2b01e9b77b6db70b90a` (23,182 bytes). All 99 members match their pins. Verified the 14 product-map candidates, archives and parent pins, authority pins and candidate base `4ece8495b3a599dbd1f14009458c94b60d1836c8`. Two product paths are new.

## Classification remedies

**(a) is sound.** The anchor scan performs the shared classification once for each .opensip name. An exact custody anchor is removed before observation; otherwise Level retains only the child's index and the boolean needed by the exclusion predicate. A directory listing can contain at most one such name, so a removed anchor cannot shift a different retained .opensip index. The subsequent walk takes paths in place without removing earlier slots. The retained field is inline in the already charged frame; it adds no heap allocation or retained PrunedAnchor string.

The reuse argument holds: member roots are fixed; the only intervening Cargo-root addition is the current directory, while any Cargo prefix tested before a target segment of x/.opensip is a strict ancestor of x. Descendant Cargo roots are removed on stack unwind. The cached boolean therefore preserves precisely the is_some result used by the walk. Ignore and boundary judgments remain separate and unchanged.

**(b-prime) is equivalent.** Counting each nonempty base's segments and comparing the borrowed path prefix with base.split('/') has the same segment equality as the former collected vector, including multi-segment/shared-prefix roots and the empty internal root. The shortest matching custody anchor is still selected. No per-member allocation remains; the one resulting anchor is constructed after the search. Removing the snapshot classification's member allocation term is justified. Discovery's existing charge needs no change: the uncharged member lists identified by r9 section 7 no longer exist. LD-C1A4-2 supplies the M3-B owner's acceptance through this reviewed unit; no behavior or cap amendment to M3-B is needed. Its closure pin must change, as it does here.

## Profile, model and census

snapshot_profile uses exactly r9's 2^21 objects, 2^24 edges and 2^33 bytes, preserving failure latching, no Clone/Default and the existing stricter with_limits policy. C1-T27 tests literal caps, equality, one-over refusal before action, no charge on refusal and subsequent closure. The payload controls use this profile; the recorded 4 GiB probe passes in 122.98 seconds and measures buffer/read/write attempts rather than charging payload storage as ledger allocation.

The model anchors track the revised classification, recorded/reused result and exclusion predicate; caps are read from the constructor's constants. The permitted live model --check passes for both vector files. Independent JSON comparison confirms only opensip-anchors-root-and-member's prediction changes: minus 12 objects, zero edges and minus 1,726 bytes. The other 34 cases, exact flags and openers remain unchanged. Session vectors are byte-identical.

The companion census's method follows r9: conservative no-boundary pricing, new-blob session branches, sealing at its bounded envelope, and separate eligibility on an admitted-extent lower bound after marker/depth exclusions. Item-5 and sealing terms are anchored. Store access uses the discovery tool's verified lead-readable path, filters held-out entries before store access, and uses the same workspace verification/composition path. No census was rerun for this review.

The recorded census covers 39 lead-readable repository entries and five workspaces exactly, matching the published discovery record's lead-readable IDs and order. Thirty-nine rows are measured; five are over item 5 with the same lower-bound evidence as r9. All measured full-ledger costs independently satisfy the three 2x inequalities. Maxima are 529,529 objects, 1,488,056 edges and 220,027,344 bytes, as accepted in r9. The Rust margin test judges recorded full-ledger charges against the compiled profile and distinguishes over-item-5 rows from claimed margins.

LD-C1A4-3 is a reasonable reading of the companion-tool-byte obligation: those bytes may be pinned in the companion record and bound by its own receipt, without adding an unrelated tool to discovery's native CLOSURE. This is subject to defining a complete companion receipt binding in the next reviewed unit; the six current tool pins alone are not that complete binding (NBO-1).

## Closure, history and lane

The discovery tool changes only its work_ledger.rs and discovery_rule.rs closure rows; both new pins are correct. Structural comparison confirms the generated discovery census changes only those closure pins and the ten held-out rows becoming stale/outstanding. Discovery vectors change only those pins. The workspace ledger changes those pins and the census tool pin; lead-readable charges/margins do not change. The recorded unchanged receipt is intentionally stale; a separate pre-reviewed blind validation run, followed by post-review, must refresh discovery and write the companion snapshot receipt against frozen caps. Failure within item 5 returns the caps to law. No held-out success is inferred.

The displacement list answers M3CR9-R2-NBO-1: it includes the old formal-bound passages at PLAN-r6:165–166, the historical changes-table formula, constructor/constants, changed implementation/tests, regenerated census/vector records and both receipt obligations. r9 and earlier packages remain history.

The lane's 24 checks pass as recorded. Host has the same eight failures and 407 passes; security has the same 14 failures with 1,184 to 1,187 passes; serial platform has zero failures and 321 to 322 passes. No differing/flaky tests are recorded. Formatting is restricted to the six base-clean Rust files. Warning-denied all-targets Clippy, focused tests, the probe, model/vector checks, three lead-readable census checks, FW-01 (8), environment exceptions (10), operability and verify_design pass. All eight mutations fail their named focused tests without compilation failure. Attempt 1's parallel platform abort is disclosed history, not the accepted lane.

Git confirms the lane-to-package base difference is exactly D2b-0's code plus its two lock commits, disjoint from this unit's paths, model pins and census closure. The new schemas do not change the snapshot descriptor's selected schema or its encoding. Recorded package-base model, operability and verify_design checks pass. Carrying the lane across this base difference is adequate for this scope.

## Non-blocking observations

**C1A4-R1-NBO-1 — Complete the future companion receipt's input binding** (`tools/security/snapshot_ledger_census.py:261`). The current six pins identify the companion tool and selected inputs, but omit the snapshot walk/source pins returned by snapshot_costs, the session source set and identity bound/encoding sources. The next blind unit should bind the full native cost-source closure, directly or through pinned vector/model records, and check freshness. No companion receipt is claimed here, so this is a downstream binding obligation rather than a blocker to the current exact lead-readable result.

**C1A4-R1-NBO-2 — Enforce census ID coverage in the Rust test** (`crates/security/src/snapshot_walk_tests.rs:946`). Matching manifest hashes and internally supplied counts does not prove all IDs are present once. A truncated/duplicated record with adjusted counts could pass. The current record's complete coverage was independently verified. Comparing unique lead-readable ID sets with the compiled discovery record would make this stated test property durable.

The permitted live operability check passes: 114 rows, no findings. No new mint authority, ambient environment read or prohibited discard is introduced. No Cargo, rustc, builds, lane lock or census runs were invoked. No private fixture, installation, signing keys, held trees, T2 stores/cache or held-out entries were accessed. Neither repository, worktree nor control files was edited. Only the requested REVIEW.md and review.json were written.
