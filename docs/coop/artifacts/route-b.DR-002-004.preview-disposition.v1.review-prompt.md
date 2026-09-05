# Independent review — Route B preview dispositions DR-002 and DR-004

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**TWO FROZEN SUBJECTS. Review both. Write one verdict file per subject.**

1. `docs/coop/artifacts/route-b.DR-002.preview-disposition.v1.json`
   Expected: `92949689a29d95e8dc5f2d0da2d05b4ea939a85517440caf19b10198507bb0c6`
2. `docs/coop/artifacts/route-b.DR-004.preview-disposition.v1.json`
   Expected: `36ad7df03c3019ce06daf75d800082fba566510afa1cd19def3d2e987869c61f`

Measure each sha256 at start and end. Do not edit either. Do not commit.

**WRITE ONLY:**
- Claude 2:
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v1.review-independent.claude2.json`
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v1.review-independent.claude2.json`
- Codex:
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v1.review-independent.codex.json`
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v1.review-independent.codex.json`

Do not read the other reviewer's files.

These are D-047 / D-048 disposition drafts. They are not owner recording.
Verdict vocabulary: ACCEPT / ACCEPT-WITH-ADVISORIES / REJECT.
Blockers are MUST-FIX.

Attack:
- silent SATISFIED or condition-1 discharge
- treats evidence.v15 application as AC-1 / AC-3 / AC-4
- treats section31 v4 as the Phase-1A packet
- pretends any UNBOUND §3.1 item is settled
- coordinator becomes recording authority
- authorizes docs/v2/implementation/
- file 08 edited
- cited digests do not match live bytes

Final chat: short summary plus both verdict words.
