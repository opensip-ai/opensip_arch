# Independent review — Route B preview dispositions v2

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

Do all three subjects. Do not read the other reviewer's files.
Do not edit. Do not commit. Do not adopt. Do not mark SATISFIED.

Measure each subject's sha256 yourself at start and end.

## Subjects, frozen

1. `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.json`
   sha256 `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809`
   Write ONLY:
   - Claude 2: `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.claude2.json`
   - Codex: `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.codex.json`

   Successor to v1: Claude 2 ACCEPT; Codex REJECT RB-DR005-CX-01.
   Verify operational metadata is no longer called rebuildable.

2. `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.json`
   sha256 `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c`
   Write ONLY:
   - Claude 2: `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.claude2.json`
   - Codex: `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.codex.json`

   Successor to v1 ACCEPT-WITH-ADVISORIES. Verify IR-RBD008-A1 and
   RB-DR008-A1 landed.

3. `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.json`
   sha256 `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52`
   Write ONLY:
   - Claude 2: `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.claude2.json`
   - Codex: `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.codex.json`

   Successor to v1 ACCEPT-WITH-ADVISORIES. Verify IR-RBTM003-A1 and
   RB-DR003-A1 landed.

Attack each: silent SATISFIED; wave-through; pretended settled
V10/custody/G19/Phase-1A; coordinator as owner; ACCEPT as owner
recording; implementation authorized; stale COORD pin (must be
current 5229013f…); collapsed state classes (DR-005).

Verdict per subject: ACCEPT | REJECT | ACCEPT-WITH-ADVISORIES.
Final chat: short summary of all three.
