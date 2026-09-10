# Independent whole-architecture application review — v2 (bounded re-review)

Reviewer: Claude `wH:p3`, D-368 fresh whole-architecture auditor; authored none of the subject
bytes. HEAD at open `4e40abe`. Companion JSON: `architecture-whole-review.v2.json`.

Subject `architecture-application.v1.json`
`e8906a952435c6b8b1de963197c856a0c7bd84edb4ad169b8277db05b6d53610`; register-edits manifest
`dd5836f4d0a966c04f17a1906daf79d52c8c41323a1dc783a8f39740f3339e09`; freeze receipt
`8e57992a86733324d8aa88af470be6fddcf8fe7761b093c0dbb335825c4eef46`; supplement unchanged
`be569fb0…`.

## Verdict: OBJECT — 4 MUST-FIX, 3 SHOULD-FIX (carried)

WR-1 and WR-3 are repaired and verified. WR-2 was answered in the wrong place, and the
successor broke custody that held at turn 1. All turn-1 merits bindings hold on the unchanged
bytes (units, supplement, handoff, twelve documents, D-369 text, images).

| ID | Severity | Finding |
|---|---|---|
| V2-M1 | MUST-FIX | `inputs[2].pin` still names the superseded edits manifest (`8ce9a7bb…`); the checker fails `application-pin/inputs/2` and `register/manifest` and skips every register check. The receipt's "fail 0" does not replay (2 FAIL). |
| V2-M2 | MUST-FIX | The 18 byte edits are the 17 rows plus G13 only. The header, blueprint-readiness paragraph, snapshot date, condition-2 and condition-4 cells and the closing paragraph are gone, so the replayed post-image `772f6db3…` says "6 of 23 NOT MET", "28 of 28" and "not blueprint-ready" beside 17 SATISFIED rows. The on-disk post-image was not regenerated (`3c920108…`). |
| V2-M3 | MUST-FIX | Eight rows still embed the turn-1 `MF6.after` text while the manifest row edits carry the corrected text: DR-101, 111, 114, 118, 124, 125, 131, 133. MF-6 hashes cannot be attested. |
| V2-M4 | MUST-FIX | The same eight rows had `qualificationRemainderProposed` emptied instead of reconciled; gate 3 now has no manifest-named remainder for them. DR-124's corrected text also reads "G09/G09". |
| WR-4 | SHOULD-FIX | Unchanged: stale "pending/not frozen" standing text and ten stale `observedSha256`. |
| WR-5 | SHOULD-FIX | Unchanged: rows dated 2026-09-04; the new post-image also reverts the snapshot line to 2026-08-15. |
| WR-6 | SHOULD-FIX | Unchanged: v48 member supersessions not named in D-369 or the DR-126 row. |

## Verified repairs

- **WR-1.** S.JOURNAL clause, `ACT-SC-TRUST-CONCURRENCE`, the OBL-GRANT-JOURNAL and OBL-BLK-4
  clauses and the corrected DR-124 row text now place the journal bytes in SC-OPS with SC-TRUST
  holding witnesses, floors, `evalHighWater` and `trustEpoch`, matching state v11 and security v8.
- **WR-3.** `completedLeadCorrectionReviews` is 3; lead review 2, its dispatch and freeze v7 are
  pinned and the pins verify.
- Corrected row texts for DR-131 (G24–G28) and DR-133 (G10/G21/G23) now agree with the gate table.

## Exact repair for the next freeze

1. `inputs[2].pin` = the frozen manifest digest.
2. Put the non-row edits back into the manifest, regenerate `readiness-register.proposed.v1.md`
   to the manifest's `proposedSha256`, update every row's `draftWholeRegisterAfterSha256`.
3. Copy each `rowEdits[].after` into `rows[].MF6.after` byte-for-byte.
4. Restore `qualificationRemainderProposed` for the eight rows as exactly the set the row text
   names (owner and pinned gate-row source; no duplicate DR-G13), and fix "G09/G09".
5. Re-run the checker with the snapshot to 0 FAIL / 2 PENDING before freezing; freeze only a
   receipt whose counts replay.
6. WR-4..WR-6 remain SHOULD-FIX. The checker requires `shouldFix: 0` for acceptance, so they must
   be repaired or explicitly disposed by a reviewed act before an ACCEPT 0/0 review can exist.
