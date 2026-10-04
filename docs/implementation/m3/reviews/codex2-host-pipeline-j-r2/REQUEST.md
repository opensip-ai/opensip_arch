CODEX2 review: M3-J1 r2, the guarded durable host pipeline. This is a **law and method-soundness** review, round 2. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-host-pipeline-j-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs, and no lead set.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, law M3-J1 r2. It is the subject of `subjectSha256`.
- `docs/implementation/m3/host-pipeline-j/PROPOSAL-r1.md` holds the r1 bytes you reviewed (`ff5cb156…`), for diffing.

**Your r1 review** is `docs/implementation/m3/reviews/codex2-host-pipeline-j-r1/` (REQUIRED-FINDINGS, J1-R1 to R7 required, J1-N1 and N2 non-blocking). r2's "r2 changes and review responses" table maps each finding to its change.

**The unit.** M3-J1 is the law row of M3-J in the accepted M3 plan r6 (`docs/implementation/m3/M3-PLAN-r6.md:217`, the r6 bytes `a6956e88…`).

**What changed in the records since r1:**
- **M3-PLAN r6 is accepted.** J1 now cites r6's bytes. The live `M3-PLAN.md` adds only the acceptance note.
- **M3-C r5 is accepted in review** (`snapshot-plan-c/PROPOSAL-r5.md`, `7f76052d…`). It takes effect once M3-L and X12 r4 are accepted. J1 now cites r5's lines.
- **X12 r4 and X2 r9 are accepted by Grok.** J1 cites their accepted bytes, `PROPOSAL-r4.md` and `PROPOSAL-r9.md`, whose lines equal r1's citations.
- **S-OP-2:** Codex returned required findings on r4, and r5 is in progress. J1 cites r4's bytes (`s-op-2/PROPOSAL-r4.md`) and gains it no acceptance.
- **M2 is complete:** Grok's crash-matrix rerun on `3d2d5b5` was accepted (`m2/M2-COMPLETE.md`).
- **M3-L is unchanged** (r1 draft).

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only.

## The r2 answers to check

1. **J1-R1 (item 8.3; 8.2's phase C; matrix rows 38 and 42; J-C14; S12-U).** The precedence now matches the outcome first:
   - `CommitUndetermined`, whatever the gate's state;
   - then `Committed(PublishedCommit)` with `latchedAfterAdmission`;
   - then phase D;
   - then `interrupted`.

   State 3 alone selects nothing.
2. **J1-R2 (5.3; 8.2's phases D and O; 8.4; S18; S12-D and S12-O).**
   - Step 1 is terminal only when its required output returns, and that moment is the settlement point.
   - An output decision point ends phase D.
   - The final output section (phase O) defers a signal. It is routed as an explicit exception through successor S18, owned by the WS and OPP owners, and J3d's output code is gated on S18.
   - S12-D now holds at `x3d.finish.end-step.after`, a D point. The new S12-O holds at `x7.delivery.required.before`, inside O.
3. **J1-R3 (item 3's `EntryRefusal { termination, created }`; item 9's presence rule; J-C6b; J-C19).**
   - `created` comes from the act's own result: `Published`, or a refusal after the rename.
   - Presence starts at publication, on every envelope except the empty-errors `interrupted` branch.
   - `LostRace` and `NotPristine` keep `firstUse: false`.
4. **J1-R4 (item 2; S4, S10; J3a; J-C4b).**
   - A platform-owned, process-custody `ExecutionIdReservations` reserves every ExecutionId, uniqueness-checked, before P0, a frame, the session or a record uses it (IE:77-81).
   - It is distinct from the durable attempt row (IE:83-101; X3D:130-134), and the security-owned draw is kept.
5. **J1-R5 (item 14).** J3d depends on F2 and G3 again, and the conditional critical path is restated against M3P:309-322.
6. **J1-R6 (matrix rows 52 to 55; J-C20b).** These cover NE:3530, :3531, :3532 and :3540 with :3574, with their classes, codes, fault causes, origins and detail-carrier rules (NE:3546-3555).
7. **J1-R7 (item 1).** The M4 CLI unit replaces the `opensip`, `analyze` and `fit` refusals. `audit`'s stays until its M5 comparison step exists.
8. **J1-N1 (8.1).** `take_cancellation_latch` is minted once per operation. The window is two bits of the gate's own atomic word, closed on every return of `prepare_commit` and `publish`, with one total order. **J1-N2:** J3d depends on O1.

## Decide

1. Does each answer close its finding without opening a new defect?
2. **S18 (J1-R2).** Is it a sound reconciliation of single-envelope delivery with WS:224-228 and OPP:337-338?
   - Is phase O's interval the right one: from the output decision point, which precedes SOP2:623's finalization, to the output's return?
   - Is the renderer failure's route inside O right: F16 before any byte?
   - Is the write failure's route right: exit 4 with no replacement envelope (`bootstrap.rs:55-60`)?
3. **The post-rename case (J1-R3).** Is extending `created` to a refusal after the publication rename (L468:48) lawful and truthful against OWN §6? The installation is visible, but its durability is unconfirmed.
4. **The window bits (8.1).** Is putting them in `FinalGate`'s word, which needs X4 r8 as an amendment, sound against X4 item 7, F41 and the gate's state law? This includes masking in `admit`, `observe` and `state`.
5. **The ExecutionId registry (J1-R4).** Is a platform-owned registry the right owner, given that both security and the host draw ExecutionIds? Is the refusal on each drawing owner's existing host-I/O row lawful?
6. **Pins and citations.** Are r2's citations right against the renewed pins: M3P r6, M3-C r5, X12 r4, X2 r9 and SOP2 r4?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. J-BS, S18 and the inventory units J2a to J3d each need reviews of their own; a contract successor's verdict must be `ACCEPT-DESIGN-UNIT`. Do not commit.
