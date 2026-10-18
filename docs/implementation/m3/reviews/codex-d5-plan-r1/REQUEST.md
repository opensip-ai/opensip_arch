# Review request: D5-PLAN-r1 (the DR-G21 controls, the fake providers and the escape controls; M3-D r5 items 18 and 27, F-7), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d5-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d5-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 378 bytes, SHA-256 `6c234d73f395d2f905806abcb1ae8b89213a41290d01bb205177d3c200e4af99`. It has 1 member, `d5/PLAN-r1.md` (26,668 bytes). Rehash it.
- **Bases:** product main `7a4be0b0402341481ae388c0cd46877f328de6c2`; architecture `cc96a35786bade24c25e9e594d8fd54973a22dd5`. Read product files at that commit with `git show 7a4be0b:<path>` if main moves. D3a-4 r2 (`d3a-4-r2-subject.json`, `454d5eeb…`, your `codex-d3a-4-r2` ACCEPT-UNIT) is integrating, and the plan cites its test file's lines.
- **Pinned sources:** the plan's opening table gives each one's SHA-256 prefix. Check them.

## Authority

- **M3-D r5:**
  - item 27 (`supervisor-d/PROPOSAL-r5.md`:880-918);
  - item 18's controls (:619-625);
  - the structural controls D5-S1 to D5-S3 (:202, :222, :239), D5-C5 (:262), D5-C1 (:415), D5-T6 (:679), D5-T7 (:703) and D5-T8 (:750);
  - F-7 (:1080-1094);
  - the units, gates and order (:1244-1287).
- **The O7 owner decision** (`owner-decisions/2026-10-09/O7-OWNER-DECISION-2026-10-09.json`): section F is binding, and CF-1 and D1b are not done.
- **The D3b plan r3** (accepted, `codex-d3b-plan-r3`), whose §0 places D5's re-runs. **The D4 plan r2** (accepted, `codex-d4-plan-r2`).
- **D3a-3 r2's carried obligation** `D3A3-D5-codecs-and-timing`.
- **QG:423-441 (DR-G21); REG:366; OPP §10 (OPP:422-437) and S-OP-11 (OPP:418); SOP2's C-4, C-7 and C-12 (:941, :944, :949); M3P:85, :421, :509; HD:909-910.**

## What to review

1. **The split and its gates (§1).** Are the seven sub-units right? Is each gate stated correctly against main and the records:
   - D3b-1 and D3b-2 for D5-3;
   - D4 for D5-4 only;
   - D2b-4b for D5-2;
   - D1b and CF-1 for D5-5;
   - Linux lanes and K1c for D5-L.
2. **Item 27's coverage.** Does the plan give every QG:428 group, every REG:366 corpus class and every OPP §10 area that touches supervision at least one named control or a cited owner? Is LD-D5-7's machine-checked table, with its pinned-source equality, a sound way to keep MD:918's table?
3. **The codec re-run and the margin (LD-D5-4, LD-D5-5).** Do they discharge `D3A3-D5-codecs-and-timing`? Are the margin's evidence and the "release waits except the one exercised" rule free of invented constants?
4. **The fakes (LD-D5-3).** Are they first-party `TestFixture` binaries that never read repository bytes and misbehave on cue across REG:366's corpus? Does the fake's self-check rule out fake defects?
5. **The structural checks (LD-D5-6).** Do they extend the right existing censuses?
6. **F-7 (LD-D5-9).** Is the outcome rule faithful to MD:1093, and is the denial test (errno cleared per call, only the denial class passes) right?
7. **The Self-review (§8)** against the lead's checklist. Are the mutation lists in §5 runtime-caught and adequate?
8. **Answer Q1 to Q5 of §9** with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `D5PLAN-R1-RF-n` / `D5PLAN-R1-NBO-n`.
