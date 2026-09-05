# Adversarial review — g30-fixture-corpus.v2

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g30-fixture-corpus.v2.json`
Expected sha256:
`c8ab0b08913c3889c72ab9fb62ac5158f980856d7a15bea5096d47595dcdc714`
Mode 0444. If the subject moves, OBJECT.

Frozen predecessor:
- `docs/coop/artifacts/g30-fixture-corpus.v1.json` `0e86bd1690d92a6f33ca263f78aa0d3d582f9b1b5da1d0e0c682e397af1f6f0f`
  Claude REJECT CLAUDE-G30FX-V1-S1 (`557bcb724ddb1b8e6d7a9148650786f45fadd3bd3fe3f17ad831f0115c90380e`); Codex REJECT 0 MUST-FIX, 1 unlabeled SHOULD-FIX (`45d740fc830ec52e8c78ce910a80523b8cedb73986ae608c91786a1e04a0a394`).
If v1 moved, OBJECT.

Frozen fixtures under `docs/coop/artifacts/fixtures/g30.v1/` (seven files, mode 0444). If any fixture moves, OBJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g30-fixture-corpus.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g30-fixture-corpus.v2.review-independent.codex.json`

Do not edit the subject. Do not edit v1. Do not edit fixtures. Do not commit. Do not edit file 08 or COORD.
Do not SATISFY DR-117, DR-131, or DR-133. Do not remasure g30 leftover-join.v4.
Do not invent a PlanIntent schema, a DR-131 pack, Rust-as-core, a D9 code, or a section 7.1 recipe.
Do not close leftover-design of OBL-G30-FX-AUTHORING. Do not invent identifiers.
Do not read the other reviewer's current-turn review.

HEAD is `76cc272426e13a874b65d62bc2f2ed9771fe7f8f`. Last heading is D-316. Required-now is 28.
Live COORD sha256 is `717552ce18c429e779d1674be1af1554957da7afa86607ce627d9c14051caad1`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-30.

Check CLAUDE-G30FX-V1-S1 is landed: basedOn.d086.role no longer asserts that D-086 named DR-G30; naming parent remains D-158.
Check the unlabeled Codex SHOULD-FIX is landed: basedOn roles lineage-qualify leftover-join tokens as g30 leftover-join.v3 / g30 leftover-join.v4.
Purpose attributes both findings to g30-fixture-corpus.v1 Stage A, not to a nonexistent v2 Stage A. Fixtures remain at fixtures/g30.v1/. Speaker is g30-fixture-corpus.v2. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded is empty.

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
