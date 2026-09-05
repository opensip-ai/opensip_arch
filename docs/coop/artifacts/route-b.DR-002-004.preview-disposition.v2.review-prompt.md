# Independent review — Route B preview dispositions DR-002 and DR-004 v2

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**TWO FROZEN SUBJECTS. Review both. Write one verdict file per subject.**

1. `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json`
   Expected: `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06`
2. `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json`
   Expected: `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76`

Measure each sha256 at start and end. Do not edit either. Do not commit.

**WRITE ONLY:**
- Claude 2:
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.claude2.json`
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.claude2.json`
- Codex:
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.codex.json`
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.codex.json`

Do not read the other reviewer's files.

These are D-047 / D-048 disposition drafts, v2 successors of independently ACCEPT-WITH-ADVISORIES v1s (0 blockers). They are not owner recording.

v1 verdicts (read only to verify the claimed repairs; do not treat v1 ACCEPT as this review):
- DR-002 Claude 2 `c0e6951468f800b54d80647b4630d5fcc6b379bb8f23d1443aaaac6fcdfb4abf` C2-RB002-A1
- DR-002 Codex `c32ac143b86acf83a0aa12f90c17ee3184452e5aa703c2fec0ffbf801a4eff23` RB-DR002-CX-A1
- DR-004 Claude 2 `c313b625e80f50a1450a01b45feaa768759a9103f45b41b5ccff02aaeb59f32b` C2-RB004-A1
- DR-004 Codex `75fe8aa7c82659338f442e9d0eb7388976a76df34c0cf9ae6fb91cf8b274e2f9` RB-DR004-CX-A1

Claimed repairs: two DR-124 classes split; CD-RT-5 lifecycle fenced off preview state; §3.1 UNBOUND items quoted verbatim.

Verdict vocabulary: ACCEPT / ACCEPT-WITH-ADVISORIES / REJECT.
Blockers are MUST-FIX.

Attack:
- claimed repairs not actually landed
- silent SATISFIED or condition-1 discharge
- treats evidence.v15 application as AC-1 / AC-3 / AC-4
- treats section31 v4 as the Phase-1A packet
- pretends any UNBOUND §3.1 item is settled
- applies CD-RT-5 write/retention lifecycle to preview state
- coordinator becomes recording authority
- authorizes docs/v2/implementation/
- file 08 edited
- cited digests do not match live bytes

Final chat: short summary plus both verdict words.
