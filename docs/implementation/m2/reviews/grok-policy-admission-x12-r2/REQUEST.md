Grok review: law X12 r2, configuration and policy-pack admission (DR-G24). It answers your X12 r1 RF-1 (a bundled imperative key is the caller's refusal) and RF-2 (`CONFIG.INVALID`'s published remedy is the capability-selection string). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-policy-admission-x12-r2. Law review; no product cargo.

Subject: docs/implementation/m2/policy-admission-x12/PROPOSAL.md r2 (pin in hashes.txt). r1 bytes are preserved in PROPOSAL-r1.md (pinned too). Your r1 review is under docs/implementation/m2/reviews/grok-policy-admission-x12-r1 (output at /tmp/opensip-implementation/reviews/grok-policy-admission-x12-r1).

What changed:
- **Item 6 and item 7 rows 3 and 4 (RF-1).**
  - For a `Named` source, a failure at step 1, 2, 3, 5, 6 or 7 is a signed-core defect. Only a step 4 failure (an unregistered ID) is the caller's.
  - Row 3 (`POLICY.IMPERATIVE_KEY_REFUSED`, request-rejected 2) now covers only a `Supplied` document.
  - Row 4 (operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / `host-invariant` / `HOST.INVARIANT_VIOLATED`, subject `pack:<packId>`) now includes a bundled item 6.2 failure. The release self-check still refuses to ship such a row.
  - Item 10 adds a bundled `exec`-key test expecting row 4, and the Forbidden substitutes add a bundled imperative member surfacing as row 3.
- **Item 7 and Units (RF-2).**
  - The claim that the registered `CONFIG.INVALID` detail already states the pack condition is deleted. The law now quotes the published `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` capability string and the remedy-keying constraint.
  - A new remedy-text contract successor, X12-0, widens that one string so it stays true for the three existing capability keys and for rows 1, 2 and 3a. The law states the three things the widened text must say in substance and leaves the exact bytes to X12-0's own review.
  - X12-0 precedes X12b, which now depends on X12a and X12-0. No row 1, 2 or 3a is emitted before it lands. The public code stays `CONFIG.INVALID`.
  - Item 10 adds a byte-equality test against the X12-0 string, and the Forbidden substitutes add emitting those rows before X12-0. The rejected alternative (minting a pack detail) is restated on the reuse-with-widening basis.
- **Other updates.** The header note and the EXIT-PLAN row text now list the units X12-0, X12a, X12b, X12c and X12d.

Context: as for r1, in particular `docs/coop/design-corrections/native/native_evidence_model.v2.py` (`PUBLIC_ROUTE_REMEDIES`), native-evidence's `remedyKeyingConstraint` in `native/native-evidence.schemas.v2.json`, admission-and-qualification §1, and workflows-and-surfaces §5 and its D9 table.

## Decide

Do RF-1 and RF-2 close? Is every bundled failure, including item 6.2, now the host-invariant row, with row 3 left to caller documents? Is X12-0 the right shape for the remedy successor, with the right predecessor relation to X12b and the code unchanged? Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the PROPOSAL.md sha256 in hashes.txt). Write REVIEW.md and review.json. Do not commit.
