Grok review: **law X12 r4**, configuration and policy-pack admission, an amendment that the accepted M3 law **M3-B r2** requires (its successor S2), plus one lead decision. Claude Opus 5.5 leads. You reviewed X12 r1 to r3. This is a **law** review. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-policy-admission-x12-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix run may be using this machine, so run no `cargo`, no tests and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- The product is at main `3e64266`; r4 changes no product code.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until acceptance.
- **Subject:** `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` (r4), the subject of `subjectSha256`.
- **Previous accepted:** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r3.md` (`11628912…`, 26,705 bytes). It equals the r3 subject you accepted in `reviews/grok-policy-admission-x12-r3`. The live file also keeps r3's "r3 ACCEPTED" note in its header paragraph.
- **The law that requires it:** `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, M3-B r2. GROK2 accepted it on 2026-10-04 (`docs/implementation/m3/reviews/grok2-config-discovery-b-r2`). Its accepted bytes are `PROPOSAL-r2.md` (`92e65825…`); the live file adds only the acceptance note.
  - **M3-B item 10** gives S2's exact text, the reading of X12:136, and what stands. Item 25's S2 row names the successor.
  - GROK2's r1 finding RF-2 (`…/grok2-config-discovery-b-r1`) is the source of the withdrawal record. Its r2 review confirmed the X12:136 reading.
- **M3-I1 r2** (`docs/implementation/m3/preview-pack-i1/PROPOSAL.md`, accepted by CODEX2). Its item 7 (I1:381-388) amends X12 r3 for M3 by statement.
- **X2 r9** (`docs/implementation/m2/project-root-x2/PROPOSAL.md`), assigned to you in parallel as `reviews/grok-project-root-x2-r9`. Its item 3a sets the order that r4's reconciliation cites.

Diff r3 against r4. Check that every change is in the r4 header, in item 8's replaced opening, or in the "r4" note after X12:136.

## What r4 changes

1. **Item 8's opening paragraph and five bullets (X12:125-130) are replaced by S2's text**, placed where they stood.
   - Pack admission stays pure: no I/O, no lock and no ledger charge.
   - It now runs immediately after configuration resolution, which runs immediately after S3's selection walk and the carrier captures.
   - It runs before X2's registry capture and every later step of project admission, before any effect, and before every analysis step r3 listed.
   - It may follow the fence acquisition of the 458c read session or of the 468/X1 write gate, the selection walk and the carrier reads.
2. **The "Withdrawal recorded" paragraph**, part of S2's text, supersedes X12:126 and the ordering sense of X12:136. It withdraws the clause "the order" from I1:388.
3. **X12:136 keeps its words**, followed by an r4 note. "Runs before any custody" now means that admission itself performs no custody. The correction that X12 does not depend on X1 stands.
4. **One lead decision, added inside S2's text.** Its two passages are marked "r4, lead decision", and the header records it with its gap, rejected alternative and control.
   - **The gap.** On first use, 468 r5 item 1 has the creator publish the installation before the 468 gate takes a fresh fence. The project carrier can be read only after that fence and the selection walk. So S2's "before any effect" cannot be met on the first-use creator route.
   - **The first-use clause.** On that route, "before any effect" reads "before any project-scoped effect":
     - the creator's installation effects come first, then pack admission, then every project-scoped effect (registration, any lease, the project ledger and journal);
     - a refused pack leaves an empty, valid installation and no project effect, which the refusal discloses and never hides.
   - **Rejected:** reading the project configuration before its custody judgment. That would break X2 r9 item 3a.
   - **Dependents named in the withdrawal record**, which S2 supersedes:
     - X11 r1 item 1a, which rejected "creating I first" on r3's order. That conflict is routed to the X11 successor that M3-J1 owns. X11's M2 decision stands on its other reasons, which X11 calls "each sufficient on its own".
     - I1:404, "J2 calls `admit_policy_selection` first".
   - **Not law, so only noted:** row 1 of the order table in M3-C's draft carries r3's order. It is updated in M3-C's next revision.

The header carries M3-B item 10's basis, rejected alternatives, what stands, and its control for B1-a.

## Reconciliations (the r4 header states each)

- **Format.** S2 puts the item number inside its bold heading. r4 writes it as the list marker (`8. **Order: …**`), so item 8 stays item 8. Apart from the two passages marked "r4, lead decision", the words are byte-identical to M3-B item 10's two quoted paragraphs; the lead checked this mechanically.
- **Names in S2's text.** "S3" is the security contract's S3. In "(registration, item 6; any lease, item 7)", the items are X2's.
- **X12:132** now follows S2's last sentence, which says the same thing in short. M3-B keeps both.
- **I1's amendments** (X12:67, :160 and :169, by I1:383-386) live in I1. r4 does not restate them, and they read on r4's identical text. I1's file is not edited.
- **X12:170's source pin** ("no … custody call" on the refusal paths) stays true.
- **Forbidden substitutes.** The "Order" bullets stand and stay true. r4 adds no bullet. On the first-use route, M3-B's "effect" means a project-scoped effect.
- **X2 r9's order.** X2 r9 item 3a, a lead decision, runs X2 item 2's placement check and item 3's chain walk after the selection walk and before the carrier reads. So S2's "immediately after S3's selection walk and the configuration carrier captures" means immediately after the captures.
- **Line citations.** X12:NNN citations are r3's lines, preserved in `PROPOSAL-r3.md`.

## Decide

1. Is item 8's new opening S2's text, placed correctly, apart from the two marked lead-decision passages? Is the rest of item 8 (X12:132-138) intact?
2. Is the first-use clause sound?
   - Is "project-scoped effect" bounded tightly enough?
   - Is "nothing to clean up" still true at project scope when a refused pack leaves a created installation?
   - Does the clause conflict with 464 or 468, or with DR-G24's record?
3. Are the dependents handled correctly? Is it acceptable to route X11 item 1a to the X11 successor, and to supersede I1:404 from here?
4. Are the X12:136 note and the reconciliations faithful to M3-B item 10, to r3 and to X2 r9? In particular, is the I1 reading right?
5. Does r4 change anything else in r3?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"subject"`: path, bytes and sha256;
- `"preservedR3"`: `PROPOSAL-r3.md`'s path, bytes and sha256.

This is a law review, not a `verify_design` unit. Do not commit.
