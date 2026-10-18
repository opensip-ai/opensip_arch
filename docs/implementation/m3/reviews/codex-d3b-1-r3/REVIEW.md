# D3b-1 r3 independent unit review

**Verdict: ACCEPT-UNIT**

**Subject manifest SHA-256:** `cc3f83ab29b68d7b8ae80e8e83528c08e5e4e0fb940b898e750638fbed317f93`

The manifest and all 278 members rehash exactly. All fifteen parent rows match product commit `d154eb002fc536855b9c831d0d6484bfaf5335d3`; all archived candidate bytes match the product map, final candidate pins, and final proof pins. The eight authority files match architecture commit `853d3f08edc90f22abfb11c635eec8b4168094fc`, and `design-lock.json` matches the product base.

Round 3 closes `D3B1-R2-RF-1`. In `a_failed_listing_or_group_kill_leaves_the_tree_incomplete`, the group-kill-failure case now samples the root identity while it is alive, kills it out of band, verifies that its identity is gone, asserts `ExitClass::Unreaped`, rejects `ExitObserved`, and requires `ConfirmOutcome::MembersListed`. It also retains zero by-pid sends, the explicit prohibition on a by-pid request for the root, the group-call/evidence equality, and the no-signal-after-reap-ceiling check. The common tool harness still snapshots the native-call recorder at settlement, drives three additional turns, drops supervision, and requires that no later native tree call occurred.

The correction and its evidence are coherently bound. Comparing the two fifteen-row product maps shows that only `crates/components/src/supervisor_tests.rs` changed from unit round 2, with no production-source change. The frozen source diff consists only of the alive-root assertion and cleanup block. I independently reproduced every observer hash in `mutation-reuse-proof.json`: the eight named mutation-observing test bodies are byte-identical, and the snapshot-failure portion of the combined test is byte-identical. The embedded round-2 manifest has its expected SHA-256, all 134 of its members rehash, and the preserved request, subject, review, and verdict bytes match the original failed review.

Fresh evidence runs the six affected controls successfully and records the full component result as 193 passed, zero failed, zero ignored. The final component source pins match the reviewed archive. The fresh Clippy, 95-test operability run, conservative no-cgroup scan, design verification, source check, formatting, and closure proof all report success. The eight preserved mutations show runtime test failures with no compile-failure markers; their production source and observing assertions are unchanged by round 3. The retained platform result is 292 passed with one inherited ignore, and the corrected-CARGO refusal evidence records three passes on each side. The standalone catalog evidence records all five controls passing; the earlier nested-lock attempt remains disclosed as superseded.

The equal baseline/candidate owner-label expectation failure remains an inherited open obligation and is correctly excluded from any whole-repository pass claim. This verdict accepts only D3b-1. D3b-2 and gate removal, D3b-L/Linux work, D5 codec reruns, CF/production wiring, qualification, and project completion remain outside the unit.

## Required findings

None.

## Non-blocking observations

### D3B1-R3-NBO-1 — The failed round and mutation reuse are auditable

Round 2 and its independent `REQUIRED-FINDINGS` review are preserved byte for byte. The round-3 delta is one test file, production source is unchanged, and the mutation observers needed to reuse all eight runtime controls are exactly reproduced by hash.

### D3B1-R3-NBO-2 — Final validation is properly scoped

The fresh affected and complete component runs substantiate the correction, while the package accurately preserves the inherited owner-label mismatch and makes no whole-repository or qualification claim.

No builds, tests, cargo commands, lanes, network access, private data access, panes, or delegation were used during this review.
