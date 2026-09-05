# Independent review — permission v2 and §3.1 supplier coverage

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

Do both subjects. Do not read the other reviewer's files.
Do not edit. Do not commit. Do not adopt.

Measure each subject's sha256 yourself at start and end.

## Subjects, frozen

1. `docs/coop/artifacts/permission-truth-tables.v2.json`
   sha256 `cce3afcaee90bbca388825a474751d6ebb17b30722b35dadcf6c631b34a8731a`
   Write ONLY:
   - Claude 2: `docs/coop/artifacts/permission-truth-tables.v2.review-independent.claude2.json`
   - Codex: `docs/coop/artifacts/permission-truth-tables.v2.review-independent.codex.json`

   Successor to v1 REJECT (B-1, B-2, B-3). Verify those three
   landed. Verify T-3 / ID-DEP-P3 / PT-NET-EGRESS rebased onto
   adopted D-032. Attack: recited counts; GRANTED tuple still
   missing Request/Execution attempt; FX-6 still forces
   'completed' over FAILED; host egress claimed as PT-NET-EGRESS
   slice-1 exerciser; silent SATISFIED.

2. `docs/coop/artifacts/section31-supplier-coverage.v1.json`
   sha256 `2ceb0365fd6bf068d9871aa028a7be05312b3ea638d1345b2182366f355048bb`
   and `docs/coop/artifacts/check-section31-supplier-coverage-v1.py`
   (measure yourself)
   Write ONLY:
   - Claude 2: `docs/coop/artifacts/section31-supplier-coverage.v1.review-independent.claude2.json`
   - Codex: `docs/coop/artifacts/section31-supplier-coverage.v1.review-independent.codex.json`

   Lane R instrument. Not the Phase-1A packet. Attack: claims
   SATISFIED; binds a selector that does not resolve; pretends
   v28 still carries partB_purgeSemantics; checker passes when a
   bound supplier is deleted.

Verdict: ACCEPT | REJECT | ACCEPT-WITH-ADVISORIES.
Final chat: short summary of both.
