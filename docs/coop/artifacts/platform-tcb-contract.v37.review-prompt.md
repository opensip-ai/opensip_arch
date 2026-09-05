# Independent review — platform-tcb-contract.v37 (DR-126)

Independent, refute not confirm. Did not author v1–v37.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v37.json`
Expected digest: `7d38d6cac7342274812adaa310ae9a87ec03fc627bd02ace85ce0b50fef8d42a`
Predecessor v36 `9d4779b693de35b7ba3bf7f0f5f1dd152a5deb3934346e9fcf5872debed3d8d1`.
Frozen Claude v36 ACCEPT `a676996bc19b3794a2921bce406c1bf4f8eb8bd874da9557617e34c1962684fd`.
Frozen Codex v36 REJECT `3bfa9b04e1b39be315d44350233b5d0cec5c56135ad5115dc81e541d233ea1e1`.
Do not read the other current v37 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v37.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v37.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v36 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: IKCONFIG is taken only from the unique pair inside the architecture-selected decompressed payload (never the raw PE); requiredN symbols must appear as explicit disabled forms; signed `ikconfigDigest` attests that text; x86 setup_header and arm64 zboot parsers are pinned; compression is gzip/xz/zstd/lz4/none. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A). Does not add DRTM/IMA as an or-choice.
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.
