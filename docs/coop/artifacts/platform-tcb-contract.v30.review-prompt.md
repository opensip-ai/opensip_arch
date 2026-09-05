# Independent review — platform-tcb-contract.v30 (DR-126)

Independent, refute not confirm. Did not author v1–v30.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v30.json`
Expected digest: `9be8deeb44e4185736ea77d61c6fb3169796bb4b3abd4bfd0d4eacc43f5c6986`
Predecessor v29 `8ad68c0aa65a113199ebdc80ff3dc1a9ccdb24e6b49113acd94e57b78b33bb4a`.
Frozen Claude v29 REJECT `1e15d77dca4c8e61feaffa351c4288f3bacc53444eaf116c9bfcd664a9197cd4`.
Frozen Codex v29 REJECT `1c4e6ec5ed6f55a9d6901a82001d6ec9ab1893e299d61f150cfbab0e3cacbf93` (end-state after post-COMPLETE rewrite from `a4fba8c6…`).
Do not read the other current v30 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v30.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v30.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v29 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: subject kind is `firmware-launched-kernel-package` (post-boot kexec out of scope, disclosed); signed `measuredBootTranscript` binds type+order+digest through the first PCR-4 EV_SEPARATOR; `recomputeDigest` once (no double-hash); post-transition RPM stages use `roFd` only; replay skips `EV_NO_ACTION`. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A).
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
