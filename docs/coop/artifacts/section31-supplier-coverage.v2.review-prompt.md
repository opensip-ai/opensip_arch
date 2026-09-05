# Independent review — section31-supplier-coverage.v2

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECTS:**
- `docs/coop/artifacts/section31-supplier-coverage.v2.json`
  sha256 `553b740a556a570bb5aa08b309c0cce1fec6a02375c18009ad5baf74a97d6bfd`
- `docs/coop/artifacts/check-section31-supplier-coverage-v2.py`
  sha256 `c8f6dc6d7a9a67697246c49f77996175417ce1a7b2511de9edd929d62dfa20af`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/section31-supplier-coverage.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/section31-supplier-coverage.v2.review-independent.codex.json`

Do not read the other reviewer's files. Do not edit. Do not commit.

Successor to v1 REJECT (Claude S31-B1; Codex S31-CX-B1/B2).
Verify digest binding exists and is enforced, and that S31-3
binds CD-RT-5.defaultPosture rather than a delta-equivalence
object.

Attack: no supplier sha256; checker still passes on same-path
byte change; S31-3 still not the default/implicit values;
claims SATISFIED; partB_purgeSemantics pretended present.

Verdict: ACCEPT | REJECT | ACCEPT-WITH-ADVISORIES.
Final chat: short summary.
