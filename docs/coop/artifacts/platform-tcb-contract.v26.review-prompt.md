# Independent review — platform-tcb-contract.v26 (DR-126)

Independent, refute not confirm. Did not author v1–v26.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v26.json`
Expected digest: `5128f40120f10796d3f974e82422820aed7b18e6454f2198c20cb1a89796238a`
Predecessor v25 `aa1542bad713b9eba6d1015f539857dfeae59690e79263ce719a914680471b07`.
Frozen Codex v25 REJECT `4aa0e0271fdbfb741b473e5fd131a9cc0b167273c891b5d9161c87a891ceda66`.
Frozen Claude v25 REJECT `60b9c67627784943541cb589f34564336e19956e9204e6268765bdbce6928900`.
Do not read the other current v26 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v26.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v26.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v25 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: RPM preferredApi holds one librpm FD across digest/verify/extract; CLI path uses openat+inode revalidation; linux-pathless restored as TCG2+TPM2_Quote PCR 4 (Linux stays slice 1; no TPM fails the machine); manifest uniqueness is relativePath only; EXTERNAL parent-of-canonicalOrigin; rpmHeaderIdentity gated to rpm-checksig and bound to queryArgv/NEVRA. Does not mint a Linux deferral or D-096 (A).
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
