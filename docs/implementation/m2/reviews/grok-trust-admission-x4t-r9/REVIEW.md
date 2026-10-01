# Law X4T r9 — check 3 admits an unevaluated predecessor

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `trust-admission-x4t/PROPOSAL.md` is 45488 bytes, sha256 `c8c1bdc4a4330225558c3df829ec930fc6ac38e25ce891270b2ca130c4dd1367`, matching the request pin. Preserved r8 is `PROPOSAL-r8.md`, 45076 bytes, sha256 `4a333c8660ea3f548d2fe3d8fc36ef570f53c1f6fe3666396b39c641de03fe81`, equal to the r8 review's subjectSha256. Live product HEAD is `9dbefb918aa2fb10848e6203fb0cb79338c7ce2f`.

The diff from r8 is two hunks: the title and the r9 header sentence, and item 7 check 3. The reference load, checks 1 and 2, the stated whole-restore limit, the four rejected alternatives, the retained owner, item 10, and unit X4T-a2 stay the r8 text.

## What holds

r8 RF-1 required that a predecessor whose clock is unevaluated has nothing to compare, and that check 3 admits X4B's acceptance. Check 3 now says that. The capsule this fence hold retains before the acceptance is the P0 `state.v1`. X4B records that clock as the unevaluated phase, and the initial publication writes it as `phase` alone. X4B's confirming admission runs X4T items 2 to 7 on the new capsule after that advance, inside the same hold. Check 3 skips the P0 predecessor, and the admission succeeds.

The admitted capsule's floors remain its `clock.record` values: `evalHighWater`, `lastAccepted`, `rootVersion`, `revocationVersion`, and `indexSnapshotVersion`. A floor publication writes a new capsule record with F, L, and the anchor set, and every other field unchanged, so the capsule it replaces already carries those five fields on its record. That record is the retained phase. X4B's acceptance is one publication of a retained-phase capsule; until the pointer is confirmed, `state.v1` remains P0. The confirming admission's tEval equals F, so that admission publishes no further capsule. An evaluated clock is check 1's before-clock, where F and L are compared with the projection. The advances check 3 names retain the unevaluated P0, which the new sentence skips, and a retained record, which has the five floors.

The rest of r8 stands on the unchanged text. The `accepted.by` load is one `Budget::load_at` in `Collection::Events` per role, at most six; `previous` is never followed and `history` is never walked; the count is 53 under the same ceiling. Checks 1 and 2 match `TimeEvidenceV1`. The whole-file restore limit is the selected bound, and the four rejected alternatives remain sound. The retained owner matches item 8, X2 r5, and X4B item 5. X4T-a2 is that reference-load unit. Item 10 still refuses a rollback as `CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`, and adds no public detail.

## Verdict

ACCEPT. RF-1 is closed. No required finding.
