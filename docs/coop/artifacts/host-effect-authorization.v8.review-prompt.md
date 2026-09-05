# Independent review — host-effect-authorization.v8

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/host-effect-authorization.v8.json`
sha256 `2cbad5612e546d3bf915074a8ad3fc4cae444122c997e2ddb3fe067d3cd022dc`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/host-effect-authorization.v8.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/host-effect-authorization.v8.review-independent.codex.json`

Do not read the other reviewer's files. Do not edit. Do not commit.

Successor to v7: Claude 2 ACCEPT 0 blockers; Codex REJECT HAE7-CX-01
(mixed CA-4-HOST vs CA-4 predicates). Verify one discriminator
domain: doctor-v4 CA-1..CA-4, with an explicit translation from
authorization-record labels.

Attack: mixed predicate domains remain; CA-4 send/receive still
unselected; deadline/byteCap shapes regress; silent SATISFIED;
minted PT token; waived join blocker; preview-denial regression.

Verdict: ACCEPT | REJECT | ACCEPT-WITH-ADVISORIES.
Final chat: short summary.
