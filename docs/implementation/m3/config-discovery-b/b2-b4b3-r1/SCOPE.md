# B2-b4b3 r1: what the candidate delivers (M3-B unit B2-b4, sub-unit B2-b4b3: the caps and the full margin test)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements section 2.3 of the accepted B2-b4 plan r4. The caps are those law M3-B r7 item 12 records (Codex `codex-m3b-r7-r1`; architecture `8d2f4557`): 2^22 objects, 2^21 edges and 2^30 bytes. They come from the redesigned walker's census (unit B2-b3d) by r6's rule. The base is product `79c8160`: B2-b3d is bound, inventory is v198, and there are 164 contract successors.

## What changes

| Path | Change |
| --- | --- |
| `crates/platform/src/work_ledger.rs` | `DISCOVERY_OBJECT_LIMIT` goes from `1 << 20` to `1 << 22`. Its comment cites M3-B r7 item 12 and the rule. The edge and byte caps are unchanged. |
| `crates/platform/tests/work_ledger_tests.rs` | B2-b1's two cap controls use the recorded object cap. Each discovery cap is admitted exactly and refused one beyond, and the profile is still the only way above the global caps. |
| `tools/security/discovery_census.py` | **The full margin claim:**<br>• `passes2x` now covers bytes too, at the largest root spelling (R = 4,096, the code's bound);<br>• the record's `caps` is `recorded-margin-holds` when no entry fails (otherwise `returned-to-law`), with `capsRecordedBy` naming r7;<br>• each workspace row carries `fullLedgerMargin: outstanding …` until B3-b's member-observation bound (r6);<br>• the closure pin of `work_ledger.rs` is refreshed. |
| `crates/security/src/custody/discovery_census.json` | Regenerated. Its limits are 4,194,304, 2,097,152 and 1,073,741,824; `failingEntries` is empty, and `caps` is `recorded-margin-holds`. |
| `crates/security/src/custody/discovery_census_vectors.json` | Regenerated; only the closure pin changes. |
| `crates/security/src/custody/discovery_census_tests.rs` | **The margin test makes the full claim:**<br>• each censused row's `passes2x` equals whether a fresh discovery ledger admits twice its objects, edges and bytes at the largest root length;<br>• no lead-readable entry fails;<br>• `caps` is `recorded-margin-holds`;<br>• workspace rows stay `outstanding` for the full ledger;<br>• the ten held-out rows stay outstanding;<br>• the record's limits are exactly the profile's.<br>The unused `fits_twice` helper is removed. |

## The margin, now claimed (lead-readable repository entries)

| Entry | Objects (cap 2^22) | Edges (cap 2^21) | Bytes at R = 4,096 (cap 2^30) |
| --- | --- | --- | --- |
| `rs-very-large-aws-sdk-rust` | 1,476,438 (2.84×) | 1,007,224 (2.08×) | 358,480,897 (2.99×) |

Every other lead-readable entry has a wider margin in each dimension; the census record lists each row's per-mille margins.

**What stays outstanding:**
- **Workspace rows:** walker-only until B3-b's reviewed member-observation bound.
- **The ten held-out entries:** their margin waits for an authorized harness or an accepted law change. That is an owner decision when B2-b reaches it.

**B2-b is complete only when the all-entry margin holds (LD-B2B-4).**

## Inventory

No path is added, so no inventory successor is owed by this unit.

**Recorded follow-up.** Two inherited inventory descriptions are now stale:
- `crates/security/src/custody/discovery_census.json` (its row says "the caps returned to the law");
- `tools/security/discovery_census.py` (its row predates the byte census and the redesign).

They are corrected in the next inventory successor. That successor needs a reviewed description-correction row, not the additive-only form.

## Checks

The evidence is lane r2. Lane r1 (kept in the work directory) failed two rows:
- **The census controls:** the constants test still expected the 2^20 object cap. It now expects 2^22.
- **The platform suite comparison:** run in parallel, the platform library tests race on shared descriptors and the shared temp directory. At base, an IO-safety abort; at the candidate, two retention races. Neither is in `work_ledger.rs`, and the platform library suite had not been in a lane before. Lane r2 runs the platform suite with one test thread, at both base and candidate.

See `evidence/checks.json`. The rows are:
- the security and platform suites (platform single-threaded) at base and candidate, with equal failure sets;
- warning-denied all-targets Clippy (host, security, platform);
- rustfmt;
- the environment and FW-01 pins;
- the scan, upward and walk vector checks;
- the walker storage check;
- the platform size test, the census controls and the census `--check`;
- the configuration tables, the operability census and verify_design.

**Mutations:**
- `cap-not-raised` (the object cap back at 2^20): the full-claim margin test must fail;
- the five census-model mutations, as regression.

## Not claimed

- No held-out or workspace full-ledger margin.
- No production caller and no qualification.
- No law change: r7 recorded the caps.

B2-b is not complete.
