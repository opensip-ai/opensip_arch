# Independent whole-architecture application review — v1

Reviewer: Claude `wH:p3`, the D-368 fresh whole-architecture auditor; authored none of the
application, supplement, units, register edits, documents, handoff or D-369 text. HEAD at open
`94baf02`; HEAD at verdict `2606256`. Companion JSON: `architecture-whole-review.v1.json`.

Subject `architecture-application.v1.json`
`f2abb73d868c314819ce9a767505b1884df007e2934b9150e72836f45973238a`; supplement
`be569fb045b96a94f35c111faadab7806b77e717a15f811dab7461e9ad0e7480`; freeze receipt
`432bce71a4dd6aa6f603cd87edd362b301f31a6c8de92831b35cd2998eba170c` (the dispatch's earlier
`a6bb1033…` citation is superseded custody text per commit `2606256`, not a subject defect).

## Verdict: OBJECT — 3 MUST-FIX, 3 SHOULD-FIX

The design content is complete and coherent. Every count, pointer, patch and image replays. The
objections are record contradictions and custody defects inside the frozen bytes that D-369 would
cite as authority; they are bounded repairs that change no reviewed design unit.

| ID | Severity | Finding | Rows |
|---|---|---|---|
| WR-1 | MUST-FIX | Grant-journal class: the OBL-GRANT-JOURNAL clause, the S.JOURNAL clause, `ACT-SC-TRUST-CONCURRENCE` and the DR-124 row text say SC-TRUST; accepted state v11 SUP-124 and security v8 §5.3 (via v1) say SC-OPS, with SC-TRUST holding only witnesses, floors, `evalHighWater` and the epoch | DR-124; act rows DR-105/107/112/114 |
| WR-2 | MUST-FIX | Proposed register rows name remainder gates that differ from the manifest's `qualificationRemainderProposed` each row cites; DR-131 (row: G23/G24/G26/G27; manifest: G24–G28) and DR-133 (row: G21/G25/G28; manifest: G10/G21/G23) contradict the register's own gate table; DR-118 lists DR-G13 twice | DR-101, 111, 114, 118, 124, 125, 131, 133 |
| WR-3 | MUST-FIX | `units.security.reviewHistoryCounts.completedLeadCorrectionReviews` is 0; three were completed (OBJECT 2/1, OBJECT 0/1, ACCEPT 0/0) and lead review 2, its dispatch and freeze v7 are not pinned in the receipt | security receipt |
| WR-4 | SHOULD-FIX | Stale standing text in frozen subjects: application `status` "NOT-FROZEN"; supplement `integrationStanding` says security v6 pending and broker/G15 pending; BROKER.FINAL, G15.FINAL, S.POLICY and S.JOURNAL clauses say "pending"; ten `observedSha256` annotations match no file | record accuracy |
| WR-5 | SHOULD-FIX | Seventeen "SATISFIED 2026-09-04 (D-369)" cells and the snapshot line predate the earliest possible recording date | all 17 |
| WR-6 | SHOULD-FIX | Supersessions of accepted platform-tcb-contract.v48 members (setns mount helper, macOS pathless codesign scope, kexec-absent/KB-1 members) live only inside security v8 and are not named in D-369 or the DR-126 row | DR-126 |

Exact evidence pointers and required repairs are in the JSON `findings`.

## What passed

- **Sets and counts.** 23 affected = 17 target + 6 already SATISFIED; 9 deferrals unchanged; 47
  obligations by (row, id) against the pinned obligation map; 86 + 8 = 94 definitions with unique
  source-qualified keys; 11 named conditions; 38 claim rides each citing D-002/D-018 and, where
  split, D-077/D-078 bytes; 5 custody edges; all 148 pointers resolve against pinned bytes.
- **Independent enumeration.** Definition-shaped entries across all 31 catalogue sources equal the
  declared selectors; no undeclared definition exists; lineage carries manifest 12/12 and
  permission 13/13 plus ID-DEP-P14. Delivery v4 authoring conditions are provenance.
- **Register and documents.** The 17 byte edits reproduce `3c920108…` exactly; each MF-6 before
  string occurs once; roster 28→29 with G13 owner and SPECIFIED, not QUALIFIED; condition 2 reads
  23 of 23, condition 4 reads 29 of 29, condition 5 stays the next act. All twelve document
  before images equal the 14-path snapshot; the after bodies are banners with no shipping,
  implementation-permission or V1-authority claim. The handoff v2 was read in full.
- **Checker.** With the historical snapshot: 6184 PASS, 0 FAIL, 2 PENDING (both the absent
  external verdict); selftest 71/71. Without the snapshot the 159 FAILs are all live decision-book
  drift, as the dispatch describes.
- **WA-1..WA-17.** Every original finding is resolved in the final bytes (security v8 §3.3, §4.8,
  §5.4, §5.6, §6.9, §7.4–7.5, §8.3–8.7; foundation v2 §1–§4; broker bootstrap v2; performance
  successor v2; distribution v2 §2, §3, §8). WR-6 only concerns how one of them is recorded.
- **Security chain.** Three ordinary exchanges, UPHOLD, two FAILED bounded confirmations (v4, v5),
  the D-367 owner-case exception (CONSENT, recorded `5e1160a`) exhausted by the second failure,
  the lead-correction v2 procedure (CONSENT 0/0, recorded `f68bef7`, notification quoted), then
  LEAD-CORRECTION-REVIEW 1 OBJECT 2/1, 2 OBJECT 0/1, 3 ACCEPT 0/0 on v8 (864 checks). No reset,
  no fourth ordinary exchange. The chain is sound; only the receipt count is wrong (WR-3).
- **Boundaries by example.** Cross-connection handle replay refused at PR-4; non-member target
  refused versus sealed member admitted; weak-threshold root cannot verify; wrong kernel series
  refused; doctor report-only with no writes; post-visibility durability UNDETERMINED; fifth
  broker grant is a startup failure; positive signed locks admitted across platforms and states.

## Rows

Nine rows would receive all four grades now: DR-103, DR-105, DR-107, DR-112, DR-120, DR-121,
DR-122, DR-126, DR-127 (DR-105/107/112 only through the corrected act text). Eight are blocked by
WR-2 on gate 3 and MF-6: DR-101, DR-111, DR-114, DR-118, DR-124, DR-125, DR-131, DR-133; DR-124
is additionally blocked by WR-1. Six of seven owner acts and all eight scope applications would be
accepted as prospective proposals; `ACT-SC-TRUST-CONCURRENCE` is blocked by WR-1.

## Limits and next step

Read-only review of frozen bytes; checkers replayed, nothing measured or executed as product.
A re-freeze that changes only the members named in WR-1..WR-6 and the regenerated register patch
may reuse the merits findings above; I will re-verify every digest and each changed member and
then supply the 68 grades, the MF-6 hashes and the bound images in the acceptance shape.
