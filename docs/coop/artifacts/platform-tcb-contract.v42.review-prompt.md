# Independent review — platform-tcb-contract.v42 (DR-126)

Independent, refute not confirm. Did not author v1–v42.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v42.json`
Expected digest: `79a24b5e4224ee59d6da0d8d94822fcfdb2325b6b041bb25c57fa85a02b5ad84`
Predecessor v41 `554de3700ad613dba49cd6d7768b3708233aa2a78502a35b06ca6e4e27ed04a4`.
Frozen Claude v41 ACCEPT `db4da05b5484a44254076b98a0c991022e555219a7d65805c7cb85da8871e11e`.
Frozen Codex v41 REJECT `3ae5e64fcf139612ffffb93f4594687620ae5e9fe78126198261b74ae8ad7994`.
Do not read the other current v42 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v42.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v42.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v41 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: `builderPublicKey` is the exact 32-byte Ed25519 key (64-hex on the wire); SHA-256 of those bytes equals `builderRootDigest`; verify consumes those bytes. IKCONFIG markers: absent = 0+0; present = exactly one ST then one ED; lone/reversed/stray refuse. `actualHeaderKind` MUST equal `preimage.headerKind`. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A).
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
