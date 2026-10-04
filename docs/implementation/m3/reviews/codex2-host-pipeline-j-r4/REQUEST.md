CODEX2 review: M3-J1 r4, the guarded durable host pipeline. This is a **law and method-soundness** review, round 4. It is a narrow amendment. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-host-pipeline-j-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, the r4 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r3.md` (`ad887c90…`), the r3 bytes you accepted, without the acceptance note.
- **The source of the amendment:** M3-D r3, the supervisor law, accepted by GROK2 (`docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, `9679dbc4…`). Read:
  - item 24 (lines 708-746): R10a's placement, what it admits, the ephemeral path, the first-use exception, the route and D4-T1;
  - item 25 (lines 748-762): the R1 checks, which stay before any draw at all;
  - successors SD-5 and SD-6 (lines 1091-1092), cross-law finding F11 (line 1111) and the D4 gate (line 1133).

  M3-D cites J1 by r3's snapshot lines (`J1:NNN`). The r4 file is longer, so the line numbers differ.
- **The companion:** M3-C r7 (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`), reviewed separately under `codex2-snapshot-plan-c-r7`. It narrows M3-C item 16's row 8, which r4 records as S19.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (F8b), read-only. J1 was read at `3e64266`. `e093e90` is the next commit, and it changes no product path J1 cites: it touches only generator, lane, registry and design-lock files.

**Scope.** r4 applies exactly M3-D's SD-6 and one record correction, and changes nothing else. Diff r3 against r4: every change should belong to SD-6 or to the item 11 correction, or to the header, the "r4 changes" table and the new short name M3D.

## What r4 changes

1. **Row R10a (item 4).** It sits between R10 and R11 in the order table, with a bullet after the first-use clause.
   - After R10's fenced first read yields the trust view, and before R11's handoff and R12's draw, D4's `components/manifest.rs` admits every component manifest that the trust view admits and that the analysis step can select.
   - It refuses EE-1, EE-3b, EE-4's manifest part and EE-5a as `ExcludedForm`. No analysis-attempt ExecutionId is drawn or reserved.
   - The route is M3-D item 24's: J1 projects it with existing codes under M3-D's SD-5. M3-D recommends request-rejected 2 with `EXTENSION.ADMISSION_REJECTED`.
   - A refusal there ends before any handoff, lease or session, so neither `refused()` nor `finish` runs.
   - J-β's range becomes R4-R10a (5.2).
2. **ER10a (item 6).** R10a's ephemeral counterpart is the last step under the read session's fence, after X4T's report-only trust admission. The ephemeral attempt starts, and so draws and reserves its ExecutionId, only after ER10a returns. With no trust view (E-3, E-4), ER10a admits nothing and refuses nothing.
3. **The first-use exception.** It is quoted from M3-D:722, then restated in J1's terms. On route 3b, whatever the creator act's result, the prelude's reservation from `mint_intent` may already exist at R10a. It is never bound to the analysis attempt.
4. **Control J-C10b.** This is the placement half of M3-D's D4-T1.
   - The registry is sampled **when R10a returns its refusal**: empty on 3a and on the ephemeral path, and the prelude's alone on 3b.
   - R11 and R12 never run, and `x3d.session.execution-draw` is never reached.
   - Step 1's render draw is the only reservation added afterwards.
5. **Successors S19 and S20, and one forbidden substitute.**
   - S19 is M3-C r7, row 8's narrowing.
   - S20 records the SD-5 projections that R10a's route needs. It gates J2a's projection of those refusals, and J3d's and J2c's R10a wiring, each with D4.
6. **Record correction (item 11).** r3's "A `repair recover` command is M5 (BP:973)" is withdrawn. `repair-recover` is the source-repair journal recovery command (CINV:988-989; WS:1024; SL:673; BP:973). J-RW r1's drafter found it (X-RW-8, `resume-repair-jrw/PROPOSAL.md`, a draft).

## Decide

1. **Placement.** Is R10a faithful to M3-D r3 item 24 and SD-6: after R10's trust read, before R11 and R12, with no analysis-attempt ExecutionId? Does J1 only place the row, and leave its content to M3-D?
2. **The ephemeral draw.** J1 r3 put the ephemeral draw "at the attempt's start" (item 2) without fixing that start in item 6. r4 fixes only that the start follows ER10a. Is that enough for SD-6, and is ER10a's place under the read session's fence sound?
3. **The first-use exception and J-C10b.** Is the exception stated as M3-D r3 states it?
   - J-C10b reads "the first-use route" as route 3b whatever the act's result, so `LostRace` and `NotPristine` also hold the prelude's reservation.
   - It samples the registry before step 1's render draw, because a render draw follows every refusal (item 2, 5.2, J-C4b).

   Are both readings right?
4. **The route.** Is it lawful to leave R10a's public projection to M3-D's SD-5 (S20), with item 10's totality incomplete for `ExcludedForm` until S20 lands?
5. **The record correction.** Is `repair-recover` the source-repair journal command, and is r3's sentence rightly withdrawn?
6. **Scope.** Does r4 change anything else in r3?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. J-BS, S18 and the inventory units J2a to J3d still need reviews of their own. D4's integration also waits for this amendment (SD-6). Do not commit.
