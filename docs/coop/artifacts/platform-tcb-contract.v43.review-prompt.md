# Independent review — platform-tcb-contract.v43 (DR-126)

Independent, refute not confirm. Did not author v1–v43.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v43.json`
Expected digest: `0aab8564a57857de467645f003ab60991e3cbfe5f197ce64ea456edf9961f2a3`
Predecessor v42 `79a24b5e4224ee59d6da0d8d94822fcfdb2325b6b041bb25c57fa85a02b5ad84`.
Frozen Claude v42 ACCEPT `2866b5b550017296d315d6d3d5287e77c578adb981d0cbb2d43efa4f7ef4394e`.
Frozen Codex v42 REJECT `6fdc216d72326cdc1bad8a3660384f91aafaf696b4b754dc163596763cadd09a`.
Do not read the other current v43 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v43.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v43.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v42 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs of Codex PTCB-V42-S1/S2: `hexEncodingRule` is GOVERNING. Every digest string in builderAttestation.preimage, result, builderRootDigest, later, and signedObject is exactly 64 lowercase hex `[0-9a-f]{64}`. Uppercase, mixed-case, or other spellings refuse. `builderSignature` on signed/later records is 128 lowercase hex of the 64 signature bytes; verify consumes those decoded 64 bytes. G22 required vectors now enumerate zero/zero accept; lone ST; lone ED; extra ST; extra ED; pair+stray ST; pair+stray ED; reversed; nested; overlapping; all three correct headerKind mappings; all six ordered headerKind mismatches; signed/later builderPublicKey mismatch; root/key/signature cross-event composition; uppercase/mixed-case digest refuse; signature encoding refuse. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A).
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
