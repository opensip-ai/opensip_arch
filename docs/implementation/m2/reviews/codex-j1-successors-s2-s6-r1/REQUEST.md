Codex review: five M2-law amendments that J1 r5 owes before unit J3a, reviewed as one batch. They are J1's successors S2 to S6:
- **S2, law 468 r6:** existing-root admission. The creator act's route and its value-only `created` record; the backup-status carrier.
- **S3, law X1 r2:** the ordinary platform owner. The durable creator-class entry, the creator-class sequence, and the read receipt with or without a session.
- **S4, law 464 r3:** creation ingress. The lent RequestId, and the prelude's ExecutionId reserved before P0.
- **S5, law X3a r6:** store endpoint admission. Item 2's consequence.
- **S6, law X4B r6:** first trust acceptance. Item 1's rejected bullet and one forbidden substitute. **X4B r6 also carries J-RW r4's RW-S5 record note,** because both accepted laws name X4B r6.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Give **one verdict per law**: **ACCEPT** or **REQUIRED-FINDINGS**, each with its subject sha256.

Write only under `/tmp/opensip-implementation/reviews/codex-j1-successors-s2-s6-r1/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No test, build or matrix run.** Don't run cargo or any lead set. Timing-sensitive lanes may be using this machine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The batch

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/`. Each subject is the law's live `PROPOSAL.md`. Diff each subject against its diff base.

| J1 successor | Law | Subject (sha256, bytes) | Diff base (sha256, bytes) | Diff base accepted by |
|---|---|---|---|---|
| S2 | 468 r6 | `m2/existing-root-admission-468/PROPOSAL.md` (`93f4d014…`, 20,223) | `PROPOSAL-r5.md` (`0959e308…`, 11,373) | Grok, `m2/reviews/grok-existing-root468-r5` |
| S3 | X1 r2 | `m2/ordinary-platform-x1/PROPOSAL.md` (`1d03e1f7…`, 16,772) | `PROPOSAL-r1.md` (`d747adf0…`, 8,796) | Grok, `m2/reviews/grok-ordinary-platform-x1-r1` |
| S4 | 464 r3 | `m2/creation-ingress-464/PROPOSAL.md` (`e0803ad9…`, 12,481) | `PROPOSAL-r2.md` (`a940ba50…`, 6,709) | Grok, `m2/reviews/grok-creation-ingress464-r2` |
| S5 | X3a r6 | `m2/store-admission-x3a/PROPOSAL.md` (`cb213261…`, 19,705) | `PROPOSAL-r5.md` (`310197d3…`, 14,850) | Grok, `m2/reviews/grok-store-admission-x3a-r5` |
| S6 | X4B r6 | `m2/trust-bootstrap-x4b/PROPOSAL.md` (`c8c54154…`, 27,900) | `PROPOSAL-r5.md` (`97c2eef3…`, 21,552) | Grok, `m2/reviews/grok-initial-core-463-r9-trust-bootstrap-x4b-r5` |

**The diff bases.**
- **468 r5, 464 r2 and X3a r5** were snapshotted for this batch. Each is the live file without its acceptance note, and each equals the `subjectSha256` of its accepting `review.json`. Before the amendment, each live file was checked to equal its snapshot plus the note.
- **X4B r5** already existed. It was checked, not rewritten, and it equals `laws.trust-bootstrap-x4b-r5.subjectSha256` of its accepting `review.json`.
- **X1 r1** was snapshotted by the lead before this batch, because J-RW r4 pins it. It is a byte copy of the live r1 file, **with** r1's acceptance sentence, " ACCEPTED by Grok X1 r1 on 2026-09-30.". Without that sentence its bytes are Grok's accepted subject (`e47aff45…`, 8,758 bytes; `m2/reviews/grok-ordinary-platform-x1-r1/review.json`). It was not rewritten.

**The revision numbers.** Each law's highest accepted revision is the one J1 r5 assumed: 468 r5, X1 r1, 464 r2, X3a r5 and X4B r5. None has moved on. So each amendment takes the number J1 names (J1:847-851), and the J1 successor ids are kept.

## Pins

The pins are in `hashes.txt`. Apart from the five subjects and this request, every pin is an accepted snapshot or a review record that accepted one.
- **The source:** J1 r5, `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, = `m3/reviews/codex-host-pipeline-j-r5/review.json`'s `subjectSha256`). Every amendment cites it as J1, by item and line. The parts used:
  - item 13's rows S2 to S6 (J1:847-851) and J3a (J1:881);
  - item 3: the durable entry and its route (J1:246-262), the `created` record (J1:263-267), the creator terminations (J1:273) and the amendments (J1:278-288);
  - item 2: the RequestId and the ExecutionId reservation (J1:190-233);
  - item 6's entry and its absent-I case (J1:442, :453);
  - item 9, J-BS (J1:695-716);
  - item 3's forbidden substitutes and J-C1, J-C6 and J-C6b (J1:185, :304-328), and the law's forbidden substitutes (J1:909).
- **X3d r9**, accepted by Grok: `m2/commit-session-x3d/PROPOSAL-r9.md` (`c727001a…`, = `m2/reviews/grok2-x3d-r9/review.json`'s `subjectSha256`). It is J1's S10. 464 r3 and X3a r6 cite it as X3D9 for S10.1, the ExecutionId reservation at `open` (X3D9:486-493), and S10.8, unit J3a (X3D9:562-565). S4 and S5 must agree with it.
- **M3-PLAN r9**, `m3/M3-PLAN-r9.md` (`72bc7a13…`): M3P:265, which says J-BS still needs its own ACCEPT-DESIGN-UNIT review (468 r6 LD6-2).
- **J-RW r4**, accepted by Codex: `m3/resume-repair-jrw/PROPOSAL-r4.md` (`9c53bce7…`, = `m3/reviews/codex-resume-repair-jrw-r4/review.json`'s `subjectSha256`). X4B r6 cites it as JRW for RW-S5's record note: the RW-S5 row (JRW:683), item 3.2's P-PREFIX and C-SUFFIX (JRW:242-246), item 3.5, C-TRUST (JRW:373-379), item 3.6, C-TDIR (JRW:381-415), and X-RW-4 (JRW:705-708).
- **Not pinned:**
  - X11 r1 (`m2/cli-enablement-x11/PROPOSAL.md`). Its live file carries an acceptance note, and no snapshot exists. 468 r6 LD6-2 cites its item 3 only for the history of item 7's deferral; J1 quotes the parts it needs.
  - X4T (`m2/trust-admission-x4t/`). X4B r6 cites X4T item 7 as the shared protocol's owner, through J-RW r4. RW-S5's X4T r13 is another drafter's and is not written yet.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `d2c00a9`, read-only. J3a is not integrated. J1 read the product at `3e64266`. `git diff --stat 3e64266 d2c00a9` is empty for every product file these amendments cite:
  - `crates/security/src/custody/installation_routing.rs` (`:90-119`, `route`; `:164`, the intent's host-I/O row; `:458-461`, the post-rename refusal's rows);
  - `crates/security/src/custody/installation_publication.rs` (`:277-285`, where the rename is marked done; `:351-382`, the act's results);
  - `crates/security/src/initial_installation.rs` (`:28`, `:96-99`, the attempt allocation; `:591`, `mint_intent`'s draw);
  - `crates/security/src/custody/installation_admission.rs:801` (the one gate);
  - `crates/security/src/custody/read_premise.rs` and `custody/ordinary_writer.rs` (the receipts and `admit_ordinary_writer`);
  - `crates/host/src/request.rs` (`RequestAuthority`; `installation_entry`).

## The shape of each diff

Every amendment has the same form:
- the title's revision number;
- one new header block after the existing header, which keeps every earlier acceptance note: what the revision changes, an "rN changes" table, and its lead decisions;
- the amended text in place, each change marked "(rN)", "(rN, J1 Sk)" or, in X4B, "(r6, record, RW-S5)". A sentence the revision rewrites is replaced where it stands. Everything else in the earlier revision is kept byte for byte.
- in 468, 464, X3a and X4B, the existing header paragraph also differs from the diff base by its earlier acceptance note, which the live file already carried. X1's diff base keeps that note, so its header paragraph does not differ.

With subject line numbers:
- **468 r6:** header block :5-38. Item 1 gains two bullets and a code note (:43-50). Item 2 gains one note (:58). Item 6's continue row is reworded (:95). Item 7's deferral target is reworded and a note is added (:98-100). One forbidden-substitute sentence is appended (:106).
- **X1 r2:** header block :5-36. Item 1: one sentence gains a note (:48), the "at most one" sentence is restated (:52), and a new bullet is added (:53-57). Item 2's last sentence is replaced (:68). Item 7's first bullet and closing sentence are replaced, the read-receipt clause is added, and the creator-class sequence is a new paragraph (:87-98). Item 8 gains J3a (:106).
- **464 r3:** header block :5-30. Item 1's id bullet is replaced, and a P0 sentence is added (:42, :48). Item 5 is restated (:61-66): its ledger sentences and its last sentence are replaced, and its StepId sentences are kept. Item 7 gains a J3a note (:81).
- **X3a r6:** header block :5-30. Item 2's creator paragraph only (:58-67): one sentence of its reasoning, two of its three constraints, its consequence, and one rejected bullet.
- **X4B r6:** header block :19-43. S6: item 1's rejected creator bullet (:90) and one forbidden substitute (:212). RW-S5's record: a note on item 5's rejected bullet (:151) and a new last bullet in item 6 (:157-161).

## What each revision carries

**468 r6 (S2).**
1. **The route (item 1).** The creator act runs on attempt A, ends `Published`, `LostRace` or `NotPristine`, and enters no gate. Attempt A is dropped with its core and platform. The invocation continues through X1's `admit_ordinary_writer` on a fresh attempt B, not through a gate lent by the creator's `InitialPlatform` (J1:259-261, :279).
2. **The `created` record (item 1).** It is value-only: `Option<Created { classification, target }>`. It is `Some` exactly when this act performed the exclusive publication rename. It comes from the act's own result, never from an existence scan or the minted intent. Every later path of the invocation carries it, and no row changes (J1:263-267, :279).
3. **Item 2:** attempt B's `InitialPlatform` lends the unchanged capability. **Item 6:** the continue row names item 1's route.
4. **Item 7:** the backup-status carrier lands with J1's S13, J-BS, and its first emitter is J3d's durable envelope. The owner's deferral stands (J1:697-713).
5. **Lead decisions.**
   - **LD6-1.** A ledger refusal after the rename is `Some`, though it takes the budget row (`installation_routing.rs:458-461`). An indeterminate rename is `None`, because the act's result does not establish the rename (`installation_publication.rs:277-285`, `:377-382`).
   - **LD6-2.** Item 7 names S13 and J3d, and records nothing as landed.

**X1 r2 (S3).**
1. **Item 1: the third producing entry.** J1's durable entry runs the producers on attempt A, then the presence probe. On `Present` it seals them as `PlatformReceipt<Write>` and runs item 2's steps 2 to 4. On `PositivelyAbsent` they serve the creator act unsealed. The Write purpose is fixed after the probe and before any receipt exists (J1:247-262, :280).
2. **Item 7: the creator-class sequence.** One creator act on attempt A, then exactly one `admit_ordinary_writer` on attempt B, only after `Published`, `LostRace` or `NotPristine`. The two-slot allocation, the `CreatorActEnded` token, `Invariant` for any other second allocation and for a third, and one gate per process (J1:281-283, :309, :320).
3. **Item 7: the read receipt** is a lawful use of the process's one attempt with or without a session (J1:284, :442, :453).
4. **Item 8:** J3a carries the code (J1:881).
5. **Lead decisions.**
   - **LD2-1.** A process still produces at most one receipt. On route 3b the intent is minted on attempt A, and item 1 lets no intent be minted through a receipt.
   - **LD2-2.** The `Creator` class enters through J1's durable entry. 468c's M2 composition is no longer an entry, and `run_initial_creator` stays `pub(crate)` and defined once (J-C1).
   - **LD2-3.** Item 2's last sentence ("The creator path keeps 468c's route unchanged") is outside items 1 and 7. It is amended because S2 and S3 make it false.

**464 r3 (S4).**
1. **Item 1.** The intent holds the invocation's lent `RequestIdentity`, and a fresh ExecutionId that it reserves before P0 is staged and holds as `ReservedExecutionId`. P0's writer takes nothing else (J1:194, :209, :288).
2. **Item 5.** The uniqueness ledger before I is process custody: `RequestAuthority` for the RequestId, and `ExecutionIdReservations` for the prelude's ExecutionId. The reservation rule is X3d r9 S10.1's: at most eight draws, the host-I/O row on exhaustion or a failed draw, and no release. The RequestId is the whole invocation's, and the prelude's ExecutionId is never reused or bound to the analysis attempt (J1:190-218, :223, :288, :365).
3. **Item 7:** J3a carries the code (J1:881; X3D9 S10.8).
4. **LD3-1.** r2's "Before I exists there is no ledger … uniqueness is established by construction" conflicts with J1 item 2, which rejects the draw as a reservation (J1:225). J1's wording governs.

**X3a r6 (S5).**
1. **Item 2's creator paragraph.** The creator act, not the creator invocation, produces no endpoint. The constraints read from 468 r6 item 1 and X1 r2 item 7. The consequence takes J1's wording: "a separately admitted ordinary write operation: a later invocation, or this invocation's attempt B (J1 item 3)" (J1:285).
2. **A record sentence.** Attempt B's commit session reserves its own ExecutionId at `open` (X3D9 S10.1), never the creation prelude's (464 r3 item 5; J1:365).
3. **LD6-1.** J1:285 quotes one phrase. r6 also amends each other sentence of the paragraph that J1's route makes false, including the rejected "a second attempt in the same process", which J1 item 3 adopts.

**X4B r6 (S6, with RW-S5's record note).**
1. **Item 1's rejected bullet (S6).** The creator act enters no gate and holds no store. On first use, acceptance runs at attempt B's fenced first read, because attempt B is an ordinary writer.
2. **The forbidden substitute (S6)** "acceptance in the creator invocation" becomes "acceptance in the creator act" (J1:286).
3. **RW-S5's record note, its own row in the changes table.** J-RW r4 says "X4B r6 records that the shared protocol completes such a leaf and such a directory, and deletes nothing (X4B:125-130)" (JRW:683). Item 5's rejected "writing records in place" gains a note: a strict-prefix completion changes no record's content (JRW:705-706). Item 6 gains a record bullet: C-TRUST completes a strict-prefix leaf at a name the publication writes (JRW:373-377); C-TDIR completes a `may_create` directory left without its allow, `trust/objects` among them (JRW:381-405); nothing is deleted (JRW:378). X4B decides nothing. The rule is X4T item 7's, as RW-S5's X4T r13 will amend it, and its code is J-RW unit J4d's.
4. **Lead decisions.**
   - **LD6-1.** Both accepted laws name X4B r6, so one revision carries S6 and RW-S5's note, each in its own row.
   - **LD6-2.** Item 1's first bullet names `admit_ordinary_writer` as the producer of the admission. It is left as written, because the trigger is the admission with the fence held.

## Decide

For each law:
1. **Faithfulness.** Does the revision carry exactly what J1 r5's successor row assigns (J1:847-851), as J1 item 3 states it (J1:278-288)? For X4B r6, does it also carry exactly RW-S5's note (JRW:683)? Does it cite each part by item and line? Does anything go beyond its sources?
2. **The lead decisions.** Is each one needed, limited to a point J1 leaves open or to a conflict with the law's own text, and sound? Are the rejected alternatives right?
3. **Code.** Where J1's text needs a code change, does the revision assign it to J3a (J1:881) and change no product code itself?
4. **Preservation.** Apart from the title, the new header block and the sentences marked "(rN)", is every sentence of the diff base kept byte for byte? Does any accepted outcome of the law, or of another law, change beyond what the revision declares? Does any public code, class, exit, detail, row, subject or remedy change?

In particular:
5. **468 r6, LD6-1.** Is `Some` right for a post-rename ledger refusal on the budget row, and `None` right for an indeterminate rename, against J1:264-266, J-C6b (J1:322-328) and the product's rename marking?
6. **468 r6, LD6-2.** Is "item 7 landed by S13" (J1:847) read rightly? Does item 7 keep the owner's deferral while naming S13 and J3d?
7. **X1 r2, LD2-1 and LD2-2.** Does the restated "at most one receipt" hold on every route of J1 item 3? Is it right to make J1's durable entry the `Creator` class's entry, and to stop listing 468c's `run_initial_creator` composition as one?
8. **X1 r2, item 7.** Does the creator-class sequence keep the purposes of one entry per process: no laundered budget and no reused receipt (J1 reviewer question R2, J1:942)?
9. **464 r3 and X3a r6 against X3d r9.** Does 464 r3's prelude reservation use the same registry and rule as X3D9 S10.1? Is X3a r6's record sentence about attempt B's ExecutionId right? Do both agree with J-C4b's three distinct ExecutionIds (J1:242) and with J1:365's first-use exception?
10. **464 r3, LD3-1.** Is J1 item 2's wording the right one to govern r2's "no ledger before I"?
11. **X3a r6, LD6-1, and X1 r2, LD2-3.** Is it right to amend sentences next to the assigned ones that J1's route makes false? Or should those be left for a later revision?
12. **X4B r6.** Is RW-S5's record note faithful to J-RW r4 (JRW:683, items 3.5 and 3.6, X-RW-4), and limited to a record? Does it decide anything that belongs to X4T r13? Is LD6-1's one revision for both right? Is LD6-2, leaving item 1's first bullet unchanged, right?
13. **Across the batch.** The five revisions cite each other (468 r6, X1 r2, 464 r3, X3a r6). Are those cross-references consistent? Does the batch leave any S2 to S6 content of J1 unassigned?
14. **Anything else wrong.**

## Output

Write REVIEW.md and review.json under `/tmp/opensip-implementation/reviews/codex-j1-successors-s2-s6-r1/`. Do not commit.

review.json carries one verdict per law:

```json
{
  "laws": {
    "existing-root-468-r6": {
      "successor": "S2",
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "93f4d0145104c9b92850cf9f289527f6846aa7b41454febdc43b01b1dff94dca",
      "preservedSnapshot": {"path": "docs/implementation/m2/existing-root-admission-468/PROPOSAL-r5.md", "bytes": 11373, "sha256": "0959e3083f95841783d39d3d299960000b556d95ebbea18b8f237cefc8d5ccf7"}
    },
    "ordinary-platform-x1-r2": {
      "successor": "S3",
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "1d03e1f7b38438b32d821de9235a15704dc5b17945e08d9380f162d47c8f9ef3",
      "preservedSnapshot": {"path": "docs/implementation/m2/ordinary-platform-x1/PROPOSAL-r1.md", "bytes": 8796, "sha256": "d747adf076b698a053748dc52ee1e2e61d4ddbbf6643b6e298a0049bd5dcfd5d"}
    },
    "creation-ingress-464-r3": {
      "successor": "S4",
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "e0803ad9f1cc3b2f8a699f3bb7a739d056ee8df2495b17795e232674a3e9fbf3",
      "preservedSnapshot": {"path": "docs/implementation/m2/creation-ingress-464/PROPOSAL-r2.md", "bytes": 6709, "sha256": "a940ba5015e99507293af73256fda9bfb5ec67b7dc28303cd1cfed64008e19c8"}
    },
    "store-admission-x3a-r6": {
      "successor": "S5",
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "cb2132614b469e9bd3f04f08c6175ba5c13acb0275da410718703d32da866e8a",
      "preservedSnapshot": {"path": "docs/implementation/m2/store-admission-x3a/PROPOSAL-r5.md", "bytes": 14850, "sha256": "310197d33f4851eb0c198073e2516a6ea14192cebde751f64a0861f5f98f8ba3"}
    },
    "trust-bootstrap-x4b-r6": {
      "successor": "S6, with J-RW RW-S5's record note",
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "c8c541544d7e48d8deea4fa7bf3f79c387bda2fd97fb08bc1d479fb402ed4991",
      "preservedSnapshot": {"path": "docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL-r5.md", "bytes": 21552, "sha256": "97c2eef3f0ad374b2004ce31d0c34fc593cba5de321f926cfe2d83aff77229a3"}
    }
  },
  "batchFindings": []
}
```

Each required finding needs an id, its law, a location, the problem or claim, the evidence and the fix. `noAcceptedOutcomeChanged` is judged apart from the revision's declared changes. Put a finding that spans laws in `batchFindings`, and name every law it touches. REVIEW.md gives the same verdicts, one section per law.
