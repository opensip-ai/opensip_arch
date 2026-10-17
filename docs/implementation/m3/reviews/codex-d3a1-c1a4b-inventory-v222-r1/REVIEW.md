# D3A1-C1A4B inventory v222 review

**Verdict: REQUIRED-FINDINGS — one required finding, no non-blocking observations.** Inventory only; the accepted code was not re-reviewed.

## Required finding

**D3A1-C1A4B-V222-RF-1 — Correct the inherited discovery census description’s obsolete held-out state.** P2; candidate inventory line 4765.

The row for `crates/security/src/custody/discovery_census.json` says **“held-out entries outstanding.”** At the exact integrated product commit, the accepted blind run has populated ten `blind-census` entries and `heldOutMargin` is `holds (blind census)`. That explicit state assertion is now false. This differs from a role description that simply omits additional functionality. The successor preserves it unchanged while judging the inherited descriptions still true.

Override this one description to describe receipt-derived held-out rows and their freshness-dependent classification without fixing them at “outstanding.” Keep the parent bytes and unrelated inherited values unchanged. Re-pin the candidate, update the successor record’s inherited-row/description-override accounting, and re-pin the subject. No code change, lane or blind run is needed. The current candidate cannot be accepted until this metadata is corrected.

## Pins and integration

The staged subject is 701 bytes and hashes to `f23877bf32aa40be8190bd87723969e90b9a428833bdd33f611a02b8683a0c65`. All three manifest members match their lengths and hashes:

- Candidate v222: 739,385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`.
- Integration source census: 749 bytes, `b3cb200a474a603798781c3d32b2f8242e6b236d08df360a0996b7d7751d43dd`.
- Successor record: 7,667 bytes, `d1472ee9e999941b2d865cee07f4f85725b5e7135621c607a4064c680bf999d7`.

The unchanged v221 parent is 735,596 bytes, `ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55`. The candidate and record correctly name v222 as the successor path.

Live product HEAD is `72e078799b201709b2545ba58cdce3fcd62a933e`, clean; architecture HEAD is `0b84657f6ecc1ba5445fdcaac4bdb9bd61087c0c`. Each of the three accepted reviews and subject manifests matches the successor’s pin, and each review binds its corresponding subject and says ACCEPT-UNIT. The product maps themselves match their subject pins. Their 19-path union equals the product diff from the v221 lock base `b7538549b727e13013f36d3b7c2e2917e767f3f2`. Integrated candidate bytes match those maps, accounting for the accepted blind run superseding the gate’s snapshot census record. No other product path changed.

## Inventory assessment

The candidate has 1,331 unique sorted rows versus the parent’s 1,327. It is a strict path superset. All 1,327 inherited rows are equal by value; all other top-level fields, including 20 packages and nine pending decisions, are unchanged. This proves inheritance mechanically; RF-1 identifies the one inherited description that should instead be corrected.

The four added rows have the requested packages, roles and generated flags:

- `supervisor_tests.rs`: opensip-components / test / false. Its description stays within the accepted D3a-1 controls, fixture participant and settlement/readiness work.
- `supervisor_fixture.rs`: opensip-components / test / false. Cargo declares it as a harness-free test target, not a product binary; the row explicitly preserves test-only status.
- `snapshot_ledger_census_held_out.json`: opensip-security / fixture / true. It describes the accepted closed receipt, input bindings, conditional composition and lack of qualification.
- `test_snapshot_ledger_census_blind.py`: tooling / test / false. It describes the accepted hermetic blind controls and their synthetic inputs, consistent with discovery’s precedent.

The inherited supervisor.rs planned role remains accurate as the module’s intended role. D3a-1 partly realizes it; resource bounds and cancellation remain later work. No completed implementation of those later responsibilities is inferred from the unchanged planned description.

The other inherited changed-path descriptions remain accurate role descriptions, including descriptions scoped to earlier test units. In particular, snapshot_ledger_census.py’s row expressly describes its **lead-readable census** role; “never a held-out entry” is read within that ordinary-mode scope, consistent with discovery’s retained lead-readable wording. Reusing discovery’s gated join adds no independent store-access mechanism. The separate new blind-control and receipt rows, and the accepted gate SCOPE, supply the additional behavior. This wording is incomplete as a whole-module feature list but does not change the stated ordinary-mode behavior. RF-1 concerns a different, explicit output-state assertion.

All 1,238 tracked product paths are covered. The 93 still-absent planned paths equal `inheritedPlannedFilesRetained` exactly. The sole newly realized planned path is supervisor.rs; the parent had 94 absent planned paths. The per-unit added/changed lists, four inventory additions and realized-planned list match the accepted maps and actual Git trees. Planned rows retain proposed standing and confer no implementation or qualification claim.

## Census and disposition

Parsing discovery_census.py’s pinned 19-file CLOSURE and intersecting it with both units’ integrated path union yields no changed closure file, matching the record.

The expressly permitted live operability source check exited 0: **114 rows, passed, no findings**. Its checker and exceptions-file pins match the archived integration census. The lexical mint audit has **439 rows**, identical by value to the v221 lock base; its standing explicitly grants no mint authority. No new mint authority or product qualification is claimed.

One combined successor is appropriate for the integrated paths, including LD-C1A4B-5’s controls and receipt. After RF-1 is corrected and the revised candidate accepted, lead assent/publication and the separate product lock commit remain required. The lock must re-point inherited passage rows to the accepted v222 artifact and run fresh verify_design. Those future actions were not performed or claimed here.

Only permitted read-only operations and the expressly authorized source check were used. No compiler, Cargo, tests, lane/lock, network, private fixture, installation directory, signing key, held tree/store, T2 store/cache/material, other pane or delegation was accessed. Neither repository, the stage nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
