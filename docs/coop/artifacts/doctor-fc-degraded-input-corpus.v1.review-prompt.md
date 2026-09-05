# Independent review — doctor-fc-degraded-input-corpus.v1

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/doctor-fc-degraded-input-corpus.v1.json`
Expected sha256:
`4864760c06d1ebbfe5e4fb96f5b22618b4af72eca2d4283abc295a66ea62895b`
Mode 0444. If the subject moves, OBJECT / REJECT.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/doctor-fc-degraded-input-corpus.v1.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/doctor-fc-degraded-input-corpus.v1.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark any row SATISFIED. Do not execute fixtures.
Do not author pre-image or post-image bytes. Do not author report bytes.
Do not invent last-known revocation bytes or timestamps. Do not acquire a lease, refcount, or lock.
Do not design purge. Do not invent a D9 code or a §7.1 recipe.
Do not authorize implementation. Do not read the other reviewer.

HEAD is `5d5d778` (D-166 ADOPTED). Required-now is 26.

Attack:
- leftover-design of OBL-DOCTOR-FX-AUTHORING is claimed closed
- pre-image, post-image, report, revocation-state, or timestamp bytes are treated as authored
- a lease, refcount, or lock is acquired
- the named images are not the v4 FC-DEGRADED set (DEG-1; DEG-2 truncated/duplicate-key/absent lock; DEG-3; DEG-4; DEG-5 prepare/commit/abort/post-crash-ambiguous; DEG-6 forward and backward skew; DEG-7)
- a cartesian product of DEG × consent is invented as required
- QUALIFIED or SATISFIED is recorded
- required-now changes
- cited digests do not match
- subject moved

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: ACCEPT or REJECT.
