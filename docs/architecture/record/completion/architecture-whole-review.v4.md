# Independent whole-architecture application review — v4 (bounded re-review)

Reviewer: Claude `wH:p3`, D-368 fresh whole-architecture auditor; authored none of the subject
bytes. HEAD at open `b26c9d3`. Companion JSON: `architecture-whole-review.v4.json`.

Subject `architecture-application.v1.json` `ce15dd64d6d3399de66d0e9f5bdb790db12d6e3dd52b5296298d6d57c5922989`;
register-edits manifest `5b2de1384870c478fa640b5657cef53121ae5be600decfab41418539292b258e`; freeze receipt
`b84fab9058c221e9c28a474ca5cfea6baaa9dde63bd1f10376e662b66f020b70`; supplement unchanged.

## Verdict: OBJECT — 1 MUST-FIX, 0 SHOULD-FIX

Everything else is in order: V3-M1 is repaired except one clause, V3-M2 is repaired, the checker
replays at 6185 PASS, 0 FAIL, 2 PENDING with all 47 register checks passing, and every turn-1
merits binding holds on the unchanged units, supplement, D-369 text, documents and handoff.

| ID | Severity | Finding |
|---|---|---|
| V4-M1 | MUST-FIX | The closing paragraph reads "condition 2 is MET and condition 5 remains PENDING; … condition 2 remains 6 of 23 SATISFIED-requiring rows SATISFIED". Only its first line was corrected. Replace the tail clause with "condition 2 is 23 of 23 SATISFIED-requiring rows SATISFIED, with 9 rows on the deferral limb", regenerate the post-image and the row hashes, re-run the checker. Nothing else needs to change. |

## Explicit dispositions of WR-4..WR-6 (as requested)

- **WR-4 disposed as advisory.** The stale standing strings are authoring-time residue in a
  proposal snapshot; every authoritative binding is a pinned accepted receipt, and this review
  records the true standing. No decision, pin, grade or evidence changes.
- **WR-5 disposed as advisory with a recording condition.** The D-369 entry must state its opened
  date (2026-09-04, the completion package) and its adoption date, so the cells' date reads as the
  package date recorded by D-369.
- **WR-6 disposed as advisory.** The superseded v48 members are named in security v8 §0.2, §8.3
  and §8.4, which D-369 item 1 adopts by pin. A DR-126 cross-reference would help readers only.

Other advisories: the bare "29 of 29 required gates are named with owners." line 9 duplicates the
condition-4 cell; the v4 dispatch cites the v2 receipt digest; the manifest is one whole-document
byte edit.

## Next freeze

Fix V4-M1 only. With that, the next dispatch receives ACCEPT 0/0 with all 68 grades, MF-6 hashes,
registerImage, documentationImage, handoffImage, enactmentImage, ownerActGrades and
scopeApplicationGrades in the checker's acceptance shape.
