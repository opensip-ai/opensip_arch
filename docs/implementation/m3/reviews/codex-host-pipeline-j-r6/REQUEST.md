Codex review: M3-J1 r6, the guarded durable host pipeline. This is a **law and method-soundness** review, round 6. r6 is a **record revision**: it records what accepted laws, bound successors and the lead's rulings have settled since r5, and it pins every cited law at an accepted snapshot. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-host-pipeline-j-r6.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No run.** No product build, test, clippy, generator or `verify_design` run: a timing-sensitive crash-matrix lead set may be using this machine. Reading files and `git show` / `git diff` are fine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`. Every cited law is pinned at its accepted snapshot (`PROPOSAL-rN.md`), never at a live file, which may move to a new draft during your review.
- **The subject:** `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, the r6 law. Its sha256 is `subjectSha256`.
- **The diff base:** `docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`), the r5 bytes Codex accepted, without the acceptance note. r6 is built from these bytes. Diff r5 against r6: every change should appear in r6's "r6 changes" table.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `1799d3d`, read-only, with 99 contract successors and 96 inventory successors (v136 selected). No product file J1 cites changed between `5214350` (r5's base) and `1799d3d`. You can check with `git diff 5214350 1799d3d -- <path>`.
- **Arch history, for the pin claims:** J1 r1 was committed at arch `04e7d2e14` and r5 at `0f35fd485`. `git show 0f35fd485:<path>` gives the live file J1 r5 read.
- **Three directory names are kept from earlier assignments.** Grok reviewed S21 in `reviews/codex2-s21-r2/` and X3d r9 in `m2/reviews/grok2-x3d-r9/`. GROK2 reviewed X7 r7 in `m2/reviews/codex2-x7-r7/`. Each `status.json` names the reviewer.

## What r6 records, and where each item comes from

| # | Item | Source | Where in r6 |
|---|---|---|---|
| 1 | **Row 57 and R1's sentence.** M3-D item 25's request-class route: request-rejected 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`. Decided in M3-D r4 (LD-R4-2), given word for word in M3-D r5 (X-D4-J1-1, `supervisor-d/PROPOSAL-r5.md:1222`), bound in NE by SD-7 (product `d2c00a9`). R1 gains D r5's sentence. | M3-D r5 items 25 and 30; SD-7 README and PASSAGES | item 4's R1 row; item 10's row 57 and its bullet; J-C20; S20 |
| 2 | **X-SD7-J1.** Row 56's basis is NE:3540 as SD-7 supersedes it; row 57's "NE §10 (SD-7)" is NE:3539's override; J-C20 tests both. | SD-7 README, "Cross-law items" | item 10, a bullet; J-C20 |
| 3 | **S21, accepted and bound** at `3f6f9a5`. J1 r5's rule-1 and rule-2 gate for a signal is met. The S21 row takes S21's scope (LD-3) and its per-kind lines WS:229 and WSE:233 (LD-6), as S21's cross-law item 1 asks. | S21 README, PASSAGES, unit record | 8.3; J-C14; item 12; S12, S21; item 14; Open questions 7 |
| 4 | **M3-D r5 re-cited.** M3D moves from r3 to r5, and every line is re-pinned (map in the M3D short name). | D's acceptance note ("J1's next revision re-cites D at r5") | short name M3D; items 4, 6, 13; history tables |
| 5 | **M3-L r5's X14.** Nothing is open: r5 applied it in full. No change. | M3-L r5, X14 | none |
| 6 | **SYN-1's routes** (bound at `682991f`): the `native.syntax-*` keys on row 52; new row 58, the syntax backend fault (operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>`); O-1's two native-context keys on row 52. | SYN-1 README (X-J1, LD-5, LD-12, O-1) and PASSAGES | item 10's rows 52 and 58 and its SYN-1 bullet |
| 7 | **E-3's ephemeral detail (lead ruling).** RTC §7.4 governs: an ephemeral attempt carries no §7.5 detail. Row 27's ephemeral case and item 6's E-3 recommendation drop `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. **Rejected:** a contract successor changing §7.4. | `grok-j2a-r1/REQUEST.md`, "Not settled" item 3 and "Lead rulings" item 3; RTC §7.4 | row 27; item 6's E-3 row; item 10, a bullet; Open questions 3 |
| 8 | **Item 14's derivation owners (lead ruling).** J3d derives a committed Run's ordered D9 deficiencies, coverageId and §7 composition; J2c derives an ephemeral result's. J2a stays pure. | `grok-j2a-r1/REQUEST.md`, "Not settled" item 4 and "Lead rulings" item 4 | item 14's J2a, J2c, J3d rows |
| 9 | **Item 13's successor states.** Accepted: S2 to S6, S7 (with RW-S1), S9, S10, S11 (round 3, adding X4-F3, LD8-9), S12 (section by section; §RC accepted, §S12 reserved), S14 (X3c r8; X3c r9 also accepted). Not yet written: S7b's E-1 and X4T parts, S8, S13, S16. S20 partly owed as SD-5b. | each law's snapshot and review directory, cited in its row | item 13; item 14 (J3a, J3b) |
| 10 | **The SD-5b rule.** Written row by row with each refusal's first consumer. | M3-D r5 item 29 (`:1180`); `grok-j2a-r1/REQUEST.md`, "Lead rulings" item 1 | item 10, a bullet; S20 |

**Items r6 adds beyond the brief, each from an accepted source:**
- **J-RW r4's RW-S8.** Item 11's recommendation is replaced by J-RW's decisions (JRW items 2 and 5), and J-C22 is JRW item 9's. M3-PLAN r10 lists RW-S8 as owed by J1's next revision.
- **X3d r9's LD9-3.** The close's admission bit is `StoppedSession::admitted_at_close()`. X3d r9 notes that J1 8.6 did not say where the bit lives.
- **X4 r8's LD8-9.** J3b depends on X4-F3. M3-PLAN r10 records the same edge.
- **M3-C r8, accepted in review** by CODEX2 while r6 was being drafted (`snapshot-plan-c/PROPOSAL-r8.md`, `578c186e…`). It carries S7b's E-2 (LD8-4) and E-3's C half (LD8-5), the latter under the same §7.4 ruling. Its cross-law item X-8, "for the enumeration owner, with J1", finds that a required cell whose closure is not admitted has no binding the enumeration contract admits. r6 records that dependency for row 27's required cells and J2c's leg, and decides nothing.
- **J1-R5-NB-01**, Codex's own observation on r5, applied in the M3C short name.
- **Snapshot pins.** r5 pinned seventeen laws and plans at live files. r6 pins each at the snapshot J1 was read against. For thirteen (X1, X3A, X3D, X4, X4B, X4T, X5, X7, X9, X10, X11, L464, L468) the live file differed from the snapshot by at most one line, edited in place by its acceptance record, and J1 cites no such line. For M3B, I1, OPP and AQP the live file was the snapshot plus a two-line note after line 1, so 45 citations drop by 2. The drafter checked every moved endpoint against the old live file: 56 line pairs, no mismatch.

## One item recorded, not resolved

NE's excluded-form row (SD-5, as SD-7 supersedes it at NE:3540; see `sd-7/PASSAGES.md`, "Effective NE §10 rows after SD-7") says that a required closure current trust does not admit, "an ephemeral request with no trust view included", "keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`". Under the lead's ruling, RTC §7.4 gives that ephemeral form no detail. r6 amends no NE text and routes the sentence to the lead (r6 Open questions, "Routed to the lead"). Tell us whether J1 r6 can lawfully stand with that sentence unchanged, or whether an NE successor must come first.

## Considered and deliberately not changed

- **M3P stays M3-PLAN r9.** r10 is accepted (Codex). r6 cites it only for the X4-F3 edge. A full re-pin is left to J1's next revision.
- **M3B, I1 and X4T** are pinned at the revisions J1 was read against (M3-B r2, I1 r2, X4T r11), not their later accepted revisions (M3-B r4, I1 r3, X4T r13).
- **X-D4-J1-2's optional J-C10b case.** M3-D r5 says J-C10b "may" add D4-T4's positive case. D4-T4 already runs it on the three paths (`supervisor-d/PROPOSAL-r5.md:818-819`), so r6 adds no control.
- **M3C stays r7**, the snapshot S19 names. M3-C r8 is cited by item and pinned in `hashes.txt` as a source.
- **The lead's scheduling decision that J3a waits for X4-F3 to integrate** is a work-log decision, not law. r6 does not record it in item 14.

## Decide

1. **Fidelity.** Is each recorded item faithful to its source? Does r6 change anything that no source or lead ruling calls for? In particular:
   - Is row 57 M3-D r5's row word for word, and R1's added sentence D r5's?
   - Are rows 52 and 58 what SYN-1's X-J1 and O-1 ask, on the routes SYN-1's NE rows state?
   - Does each item 13 row state its successor's state, snapshot and review directory correctly?
   - Is RW-S8's replacement of item 11's recommendation a faithful summary of JRW items 2 and 5?
   - Is M3-C r8's X-8 recorded as a dependency only, with no row changed?
2. **Re-citations.** Does every re-pinned citation resolve to the same fact at its new snapshot?
   - **M3D r3 → r5:** 717-722 → 764-769; 717-734 → 764-797; 718 → 765; 719 → 766; 720 → 767; 722 → 769; 733 → 796; 743-746 → 812-815; 748-763 → 827-851; 1091 → 1179-1180; 1092 → 1181. Two lines say more in r5 (796 and 769's quotation); r6's table names both.
   - **The thirteen line-identical pins** and **the drop of 2** for M3B, I1, OPP and AQP. Compare against `git show 0f35fd485:<live path>`.
3. **The lead rulings.** Are rows 27 and E-3, and item 14's derivation split, applied as ruled and no wider?
4. **The NE sentence** (above).
5. **Scope.** Does r6 change anything else in r5?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. J-BS, S7b, S8, S13, S16 and SD-5b still need their own reviews. Do not commit.
