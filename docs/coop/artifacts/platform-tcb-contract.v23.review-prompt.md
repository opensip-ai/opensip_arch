# Independent review — platform-tcb-contract.v23 (DR-126)

Independent, refute not confirm. Did not author v1–v23.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v23.json`
Expected digest: `c93175e6577daed190bb33af12973e42ad5bba88be36df07307e99f54053289d`
Predecessor v22 `62cba1c1ce548a93565326ec1b9a80518841033cd3ea3846045f77de0879da6d`.
Frozen Codex v22 REJECT `9a603e8c693a7b2fae70fdaaaa48556db38fbe5ea461ff0669175d3b85b601c5`.
Claude v22 did not land COMPLETE; do not require it.
Do not read the other current v23 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v23.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v23.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v22 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: linux-file-backed join is path+hash on the same manifest member; linux-pathless is a trusted kernel-image sha-256 (ima-kernel-image or efi-boot-kernel-digest), not NT_GNU_BUILD_ID; objectAuthenticityBindRecord is OS-discriminated; rpm/apt acquire one archive, bind digest, then checksig/extract those bytes.
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
