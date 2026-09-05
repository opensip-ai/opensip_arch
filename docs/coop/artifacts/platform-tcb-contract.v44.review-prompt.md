# Independent review — platform-tcb-contract.v44 (DR-126)

Independent, refute not confirm. Did not author v1–v44.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v44.json`
Expected digest: `c2166fa1640310772981a84c886681b3806068add72632b583a645450c6cbfe2`
Predecessor v43 `0aab8564a57857de467645f003ab60991e3cbfe5f197ce64ea456edf9961f2a3`.
Frozen Claude v43 ACCEPT `ec79de27734cc9d896dfb6fbe82173219bdade62691fcc4ce0225787085e9e4a`.
Frozen Codex v43 REJECT `df391482bdbd6c0a9cbc7838bf515fa827d5c6d0487c402dc0fa9e884c253483`.
Do not read the other current v44 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v44.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v44.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v43 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repair of Codex PTCB-V43-S1: `g22.vectorRosterRule` is GOVERNING (successor rosters are cumulative; replacing the JSON string is not withdrawal). `g22.ikconfigParserVectors` is the explicit union of every v42 required vector and every v43 addition, including distinct vectors for wrong memberSha256, altered kexecCapability, payloadDigest mismatch versus P, absent/duplicate builderRoot, multiple linux_banner, present non-32-byte key, correctly encoded invalid signature under the correct key, loaded-section payload accept, and zero-marker absent branch with a valid builderAttestation. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A).
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
