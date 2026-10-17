# D3A1-C1A4B inventory v222 round-2 review

**Verdict: ACCEPT-UNIT.** Inventory candidate assessment: ACCEPT. No required findings or non-blocking observations. D3A1-C1A4B-V222-RF-1 is resolved by the verified existing effective-description mechanism. No code or product qualification is accepted by this inventory review.

## Correction to round 1

Round 1 incorrectly treated the raw discovery_census.json inventory description as its effective meaning and requested an inherited-row edit. I missed its already-bound passage override. verify_design.py requires inherited inventory rows to remain equal by value and the successor record to assert that preservation; descriptions change through contract passage overrides and their inventory inheritance, not by rewriting an inherited row in an additive successor.

Contract successor 165 already supplies the required wording. Its record is exactly 5,201 bytes, SHA-256 `ce2a7f7ca44b99e547f19668909c8b013fe3a6e537ed87a95efbe24f4ae2ea33`. I verified its binding at contractSuccessors index 164, all four record/subject/review/assent pins, the ACCEPT-DESIGN-UNIT review and substantive assent, and the exact originating before/after text. The current lock carries the override on v221 at `/files/584/description`.

Its effective description explicitly allows held-out rows to be outstanding, stale, or composed from a current B2-b4c receipt, with the held-out state. It is true for the accepted product at 72e07879 and its ten composed blind-census rows. It does not assert that the current rows remain outstanding. The raw inherited row must therefore stay unchanged. No new override or supersession is necessary.

## Complete override projection

All **113** projection entries were checked independently against design-lock.json’s inventoryPassageInheritance, not just the disputed row. Each lock entry binds the exact v221 parent pin. Every projected before text equals its v221 row’s raw description, every inherited row remains equal by value in v222, and every effectiveDescription equals the lock’s after text. Both parent and candidate JSON-pointer indices resolve to the same stable file path. There are no duplicate paths, missing overrides or extra overrides.

For discovery_census.json the candidate selector is exactly `/files/586/description`. The effectiveDescriptionAnswersFinding origin and priorRound pins are exact. The projection is a record of existing bound meaning; it creates no new authority. The later bind must actually carry all 113 overrides to these v222 selectors and pass fresh verify_design.

## Subject and unchanged evidence

The 717-byte subject manifest hashes to `1ad03edb1356b1c4b6ada342526f916dfa86f4e09d3ba88f919ccae9f9dad889`. All three members match:

- Candidate v222: 739,385 bytes, `9992d0830b81c5c38c1813ba0db3a2f1615467813e94d613be0d26c53d3c8f0c`.
- Source census: 749 bytes, `b3cb200a474a603798781c3d32b2f8242e6b236d08df360a0996b7d7751d43dd`.
- Round-2 successor record: 328,609 bytes, `817b595de5288ae1bf9cd8640c9ab060b14b2cecdd6484a54f4eccd7d0f0290c`.

The v221 parent remains 735,596 bytes, `ed52500e89ac124b8250b9df9cedf69fc8eedfd3e5f7f4df2472b722bd1cec55`. The candidate correctly names v222. Candidate and census bytes are unchanged from round 1. The archived round-1 manifest and record match their prior pins; every old successor-record value is unchanged. Only round metadata, prior-round references, the projection/rule and the finding explanation were added to the record, with the corresponding manifest update.

Live product main remains clean at `72e078799b201709b2545ba58cdce3fcd62a933e`. Architecture is `7a7e87a0e7295d47135d298438815c68dbdc3356`; its only commit since round 1 publishes CI-PLAN-r3/CI-A1. The inventory parent and the three accepted unit review/subject pins are unchanged across that publication.

Rechecked candidate structure: 1,327 inherited rows remain equal by value; four additions give 1,331 sorted unique rows. All 1,238 tracked product paths are covered, all 93 still-absent planned paths are retained, and the 20 packages and nine pending decisions are unchanged. The four additions, partly realized supervisor planned row, per-unit map lists, integrated candidate hashes and empty discovery-closure intersection retain round 1’s conclusions on unchanged bytes. No later D3a/D3b responsibilities or qualification are inferred.

The same archived integration census records a passing source check with 114 rows and no findings; its checker and exceptions pins still match current product bytes. The mint audit remains 439 rows. The successful live source check from round 1 was not repeated because its product inputs and recorded evidence are unchanged. No new mint authority follows.

## Other descriptions and outcome

The discovery blind receipt description states a derived state, not a fixed success/outstanding state. Its public-binding list omits memberModel, an existing unchanged binding. The list is incomplete rather than false: it names actual bound inputs without asserting that no others exist. No description successor is required for that omission.

The workspace-ledger description makes no held-out-state assertion and remains accurate; neither accepted unit changed that artifact. The snapshot census description’s attribution of held-out entries to the blind validation run is accurate. These three rows have no carried override, as asserted, so their raw descriptions were assessed directly.

The combined successor is accepted on these exact bytes. Lead assent and architecture publication, followed by the separate inventory lock commit and fresh verify_design, remain pending actions. Nothing was bound, committed or pushed by this review.

Only read-only reading, hashing, JSON parsing and Git queries were used in this round. No compiler, Cargo, tests, lane, network, private fixture, installation directory, signing key, held tree/store, T2 store/cache, other pane or delegation was accessed. Neither repository, the stage nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
