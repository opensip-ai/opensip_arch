# Independent review — platform-tcb-contract.v14 (DR-126)

Independent, refute not confirm. Did not author v1–v14.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v14.json`
Expected digest: `c90757221d4235d67e4758b197d90e29fa80c9c7d1ee4e3308528ed53f7f3b6a`
Predecessor v13 `9c12b6b5a5e5067d9d9f1f2bca5ec399c8bd0ff0407b4d629d241e10e04172f4`.
Frozen Claude v12 REJECT `3aae79790575c312642572d91a77808e281d5b154a43b6fbf9be8ee54bd6c532` (reproducing; v13's fa2c04a6 pin did not).
Frozen Codex v12 REJECT `1851a2871c6a2ca5b53a43d4be29408e0e57d5dea3428bb72d41306ff664106e` (reproducing; v13's ee785134 pin did not).
Frozen Codex v13 REJECT `5f468845e0496db643586659fed2e2d38acfdf2bd339dd18446829cfc01eec76`.
Claude v13 did not land COMPLETE; do not require it.
Do not read the other current v14 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v14.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v14.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12/v13 verdict (0444 — STOP).
HEAD is `498cd8d` (D-118 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `b38bd9007da65f0d1f3bc3cb48b34cb7f757a811bd9a9c5159190c975b70f34f`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: v12 pins reproduce; volume rules are tag-dispatched; volumeConstraint is a closed tagged union; run-level preselection forbids completePlatformProfileKey; Linux observation uses held /proc descriptors (not non-preemption); PATHLESS is only-if OS ABI; remasured at D-118 HEAD `498cd8d` / COORD `b38bd900`.
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
