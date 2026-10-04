Codex review: J-RW r1, the resume/repair writer law. This is a **law and contract-soundness** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine. Do not run any lead set.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them (for example, to recompute digests or tabulate the X9 evidence runs).

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until it is accepted.
- **The subject:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, law J-RW r1. It is the subject of `subjectSha256`.
- **The unit.** J-RW is the law that the accepted M3 plan gives to M3-J by lead decision P5-1 (`docs/implementation/m3/M3-PLAN-r6.md:217, :236, :251, :572-575`). It is the resume/repair writer's successor to X2 item 8, X3c item 10 and the X4T dependency-publication rule, with its X9 coverage rows. Its code unit is J4, which does not wait for J3. J-RW must be accepted before M3 day 0.
- **The gap it closes:** M2's limit L11, the permanently refused crash states (`m2/EXIT-PLAN.md:186-191`; `m2/M2-COMPLETE.md:349-356`; X9 r16 at `PROPOSAL-r16.md:136-168` and `:1162`). The 57 F00 kill points behind it are in the X9 evidence record's storage runs.
- **Governing records and their status:**
  - **Accepted:** X2 r9; X3c r7; X3b r10; X4T r11; X4B r5; X3d r8; X6 r4; X1 r1; X9 r16; law 465; the registry owner selection v2 (REG); the root-binding owner selection (OWN); M3-PLAN r6; M3-J1 r3; the operability plan r3; S-OP-2 r6. M2 is complete (M2C).
  - **In draft, not pinned:** X3c r8, the re-commit successor (P5-2). Another agent is writing it tonight. J-RW deliberately does not read it. Judge J-RW's item 13, X-RW-9, against X3c r7 and P5-2 only.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only. Main has since moved to `e093e90` (F8b). `git diff --name-only 3e64266 e093e90 -- crates/` is empty, so every cited product line is the same at both.

## What the law decides

1. **Scope (item 1).** Exactly L11's three families, plus X3b's `carrier-floors` directory, which P5-1's owner list omits. The families are an interrupted first registration (R), a created owner not yet private (P), a partial ledger WAL (L), and an X4T dependency at a re-written name (T). Undetermined commits, `admitted` attempts, adopt-kind or moved reservations, migrations and power-loss variants are out of scope.
2. **The writer (item 2).**
   - **Where.** Each family is completed inside the next admitted durable write, at its owner's own step and under its owner's lock: R at R9, P3 and T at R10, and P1, P2 and L at `prepare_commit`'s `admit_layout`.
   - **Never** on a read path, and never in the crashed process.
   - **Authorization.** An `OrdinaryWriteAdmission` on the same root, with agreeing locator and incarnation, authorizes completion of a random-kind reservation (REG:9, :74).
   - **No new surface:** no command, entry or flag.
3. **Completion is the owner's interrupted step, finished in place (item 3).** It never deletes, renames away, rewrites a byte or adopts a temporary name. There are five procedures:
   - **C-ACL:** the one zero-rights owner allow on an empty, exact-private-shape, ACL-omitted object. This generalizes L465 item 5.
   - **C-SUFFIX:** the suffix written to a strict-prefix marker or trust leaf.
   - **C-LEDGER:** X3c item 2's schema transaction, over L-UNC: no committed schema object and no page beyond the header.
   - **C-REG:** X2 item 6's remaining steps under REG's reservation join.
   - **C-TRUST:** C-ACL and C-SUFFIX at `write_dependency`.
4. **The crash-state table (item 4).** Thirteen states, RW-R1 to RW-T2, account for all 57 sampled kill points (46 R, 6 P, 2 L, 3 T). Each has today's row, the writer's action and its terminal state.
5. **The neighbours it keeps refusing (item 5),** each on today's row and subject.
6. **Idempotence, crash during repair, cancellation, concurrency and stacking (item 6):** rules CR-1 to CR-7.
7. **Disclosure (item 7).** No public change. One operational-record event, `host.repair.completed`, added by S-OP-2's ordinary registration.
8. **Controls, X9 r17 rows, units and successors (items 9 to 12):**
   - controls RW-C1 to RW-C14, plus J-C22, which J1 left for this law to define;
   - rows RW-F00 (F00's L11 cells re-transcribed), RW-K1 to K9 (a three-child crash-during-repair ladder), RW-N1 to N9 (mutation neighbours) and RW-B, with a census rule and `.repair` scope names. L11 is retired;
   - units J4a to J4e;
   - successors RW-S1 to RW-S8: X2 r10, REG v3, X3c r9, X3b r11, X4T r12 with an X4B record, X9 r17, and the M3-PLAN and J1 records.
9. **Cross-law items (item 13),** X-RW-1 to X-RW-11, X3c r8's sequencing and boundary among them, and two record corrections (item 14).

## Decide

1. **Scope.** Is item 4 complete for L11? Does any census occurrence in these windows leave a state that is in neither item 4 nor item 5 (review question R6)? Check the 57 runs against the evidence record.
2. **Authority.** Does item 2's authorization meet REG:9 and REG:74? Is IE:47-50's "explicit recovery" met without an identity-contract passage successor (X-RW-1, R1)? Do the J1 constraints at `host-pipeline-j/PROPOSAL-r3.md:689` hold: an X1 ordinary writer through J1 item 3, no public code, no deletion, no foreign artifact adopted?
3. **Each predicate and action.** Check each against its owner's law and the product:
   - **P-ACL and C-ACL** against L465 item 5 and OWN §6 (R4);
   - **P-PREFIX and C-SUFFIX** against X2 item 6 step 5, REG:60, X4T item 7, X4B:125 and X4B:130 (R3);
   - **L-UNC and C-LEDGER** against X3c item 2 and X3b item 3a (R2). Is L-UNC exactly the committed view at `x3c.ledger-create.wal` and `ddl.commit.before`, and nothing that ever held evidence?
   - **C-REG's join** against REG:70-76 (R5).
4. **The safety bias.** Can any completion manufacture a committed Run, an attempt row, a receipt or a RunId, or widen custody? Does every ambiguous state refuse on its existing row?
5. **The rows.** Do RW-F00, RW-K, RW-N and RW-B, the census rule and the retirement of L11 cover CR-1 to CR-3 under X9's driver, ladder and evidence rules (X9 r16 at `:170`, `:920`, `:1079`, `:1089`, `:1233`, `:1236`) (R7)? Is the RW-F00 change to R4 (back to F00 r5's UAU) right?
6. **Cross-law items.** Is each conflict named against the law that must change? Is X-RW-9 enough to keep J-RW and the unread X3c r8 disjoint (R8)?
7. **Units and plan.** Do J4a to J4e and RW-S1 to RW-S8 keep P5-1's DAG (no J4 edge on J3 or X3c-3) and the plan's J4 bounds (M3P:311, :340)?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. J4's sub-units each need their own inventory-unit review, and RW-S1 to RW-S6 each need their own review. Do not commit.
