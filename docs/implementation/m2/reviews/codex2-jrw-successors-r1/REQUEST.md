Codex review: the five successors that law J-RW r4 owes, with J1 r5's S7, reviewed as one batch. They are:
- **RW-S1 and J1's S7, law X2 r10:** project-root custody and first registration. Item 4's reservation join on the write gate only, new item 6c (reservation completion), and the creator branch withdrawn from item 6.
- **RW-S2, registry owner selection v3 (a record):** four line overrides on the selected registry owner v2. J-RW is the operation owner for ordinary, random-kind reservation completion, and a strict-prefix marker is completed in place only with the complete namespace present.
- **RW-S3, law X3c r9:** the evidence ledger. C-ACL for the store directories, and two resumable creation states: the ACL-omitted empty ledger file, and L-UNC with its schema cookie and bound k = 26. It also discharges X3c r8's CL-4.
- **RW-S4, law X3b r11:** the grant journal. C-ACL for `trust/carrier-floors/` at the floor step, under the fence.
- **RW-S5, law X4T r13 (its X4T part):** current-trust admission. Item 7's publication protocol completes a torn leaf at a name it writes (C-TRUST) and a `may_create` parent directory left without its allow (C-TDIR), on both ends of the fenced read.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Give **one verdict per law**, each with its subject sha256: **ACCEPT** or **REQUIRED-FINDINGS** for the four laws, and **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS** for the registry record (see "The registry record's verdict").

Write only under `/tmp/opensip-implementation/reviews/codex2-jrw-successors-r1/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No test, build or matrix run.** Don't run cargo, `verify_design.py` or any lead set. Timing-sensitive lanes may be using this machine. Read `verify_design.py` from git; don't execute it.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- Read-only scratch scripts under your review directory are fine, at low priority (`nice -n 19`, Python `-I -B`), as in earlier rounds.

## The batch

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/`. Each law's subject is its live `PROPOSAL.md`. Diff each against its diff base, the accepted snapshot.

| J-RW successor | Law | Subject (sha256, bytes) | Diff base (sha256, bytes) | Diff base accepted by |
|---|---|---|---|---|
| RW-S1, with J1's S7 | X2 r10 | `m2/project-root-x2/PROPOSAL.md` (`a0d43d99…`, 71,310) | `PROPOSAL-r9.md` (`0d68e3a5…`, 55,434) | Grok, `m2/reviews/grok-project-root-x2-r9` |
| RW-S2 | registry owner selection v3 | the subject manifest `m2/project-registry-owner-selection-v3-subject.json` (`0bd640d3…`, 454): `project-registry-owner-selection-v3/README.md` (`4ec39357…`, 7,654) and `successor.json` (`c6d860cf…`, 12,684) | its parent `m2/project-registry-owner-selection-v2/owner.md` (`2d4b65c9…`, 32,488) | Grok, `m2/reviews/grok-registry-owner-v2-20260921-r1` (ACCEPT-DESIGN-UNIT), with root assent in `project-registry-owner-selection-v2-unit.json` |
| RW-S3 | X3c r9 | `m2/ledger-blob-x3c/PROPOSAL.md` (`46156e8e…`, 81,248) | `PROPOSAL-r8.md` (`ba638efb…`, 66,778) | GROK2, `m2/reviews/grok2-ledger-blob-x3c-r8` |
| RW-S4 | X3b r11 | `m2/journal-x3b/PROPOSAL.md` (`27ed0aaf…`, 73,641) | `PROPOSAL-r10.md` (`25a60824…`, 69,171) | Grok, `m2/reviews/grok-journal-x3b-r10-commit-session-x3d-r6` (`x3b/review.json`) |
| RW-S5, X4T part | X4T r13 | `m2/trust-admission-x4t/PROPOSAL.md` (`f7b18730…`, 94,708) | `PROPOSAL-r12.md` (`cf566db7…`, 79,182) | Codex, `m2/reviews/grok2-x4t-f2-r1` |

**The diff bases.** Each existed and was checked, not rewritten. Each equals the `subjectSha256` of its accepting `review.json`. Each law's live file was checked, before r10, r9, r11 and r13 were written, to equal its snapshot plus an acceptance note, and nothing else. The four laws' highest accepted revisions are X2 r9, X3c r8, X3b r10 and X4T r12, so each new revision takes the number J-RW names (JRW:679-683).

**The revision header.** X2, X3c and X4T kept their acceptance note as a separate paragraph, so their new revisions start from the snapshot and record that acceptance in the new header. X3b records acceptances inline, so X3b r11 keeps r10's sentence "r10 ACCEPTED by Grok on 2026-10-02." on its own line (the line-20 hunk).

## Pins

The pins are in `hashes.txt`. Apart from the subjects and this request, every pin is an accepted snapshot, or a review record or unit that accepted one.
- **J-RW r4**, the source, cited as JRW: `m3/resume-repair-jrw/PROPOSAL-r4.md` (`9c53bce7…`, = `m3/reviews/codex-resume-repair-jrw-r4/review.json`'s `subjectSha256`). The parts used:
  - item 12's rows RW-S1 to RW-S5 (JRW:679-683);
  - item 2's writer, its authorization for family R, and its clocked-path authorization for family T (JRW:165-193);
  - item 3's completions: C-ACL (:219-240), C-SUFFIX (:242-250), C-LEDGER (:252-344), C-REG (:346-371), C-TRUST (:373-379) and C-TDIR (:381-415);
  - items 4, 5, 6 and 8: the states, the neighbours, the crash rules, and the rows and budget (:417-514);
  - item 9's controls (:519-575) and item 11's units J4a to J4d (:662-665);
  - item 13's cross-law items X-RW-1 to X-RW-5, X-RW-9 and X-RW-13 (:696-734), the forbidden substitutes (:744-761) and the lead decisions (:767-784).
- **JRW-R4-NB-01** (Codex's r4 observation): `current_trust_admission.rs`'s row mapping is cited at `d2c00a9`'s lines, `:89-114` (`:100`, `:101`, `:107`), in X4T r13's item 10.
- **J1 r5**, the source of S7: `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, = `m3/reviews/codex-host-pipeline-j-r5/review.json`'s `subjectSha256`). Row S7 (J1:852), item 3's route 3b (J1:257-262) and its X2 r10 bullet (J1:287), and unit J3a (J1:881).
- **The registry record's parents and model:** v2's `owner.md`, `successor.json`, subject manifest, unit and review; and S21's `successor.json` (`m3/host-pipeline-j/s21/successor.json`), the lean M3 form of a passage-only contract successor that v3 follows (README V3-1).
- **Other accepted snapshots cited:** X3d r9 (`m2/commit-session-x3d/PROPOSAL-r9.md`, `c727001a…`, with `m2/reviews/grok2-x3d-r9/review.json`), which already records X3c r8's CL-1; X4B r5 (`m2/trust-bootstrap-x4b/PROPOSAL-r5.md`, `97c2eef3…`), items 5 and 6; X4B r6 (`m2/trust-bootstrap-x4b/PROPOSAL-r6.md`, `c8c54154…`, = `m2/reviews/codex-j1-successors-s2-s6-r1/review.json`'s X4B `subjectSha256`), whose items 5 and 6 carry RW-S5's record note (X4B r6:151, :157-161); and law 465 (`m2/initial-parent-preparation-465/PROPOSAL.md`, `b34eae39…`, its only revision), item 5.
- **Not pinned:** every other law's live `PROPOSAL.md`. Several are being amended in parallel.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `d2c00a9`, read-only. Read each file with `git show d2c00a9:<path>`. The product lines the subjects cite are JRW's, which Codex checked at `d2c00a9` in round 4, plus these:
  - `crates/security/src/custody/first_registration.rs:2183` (`register_on_gate`, the only registration entry; X2 r10's S7 note);
  - `crates/security/src/custody/project_admission.rs:602-603`, `:616`, `:678-719` (the marker observation and the classification; X2 r10 item 4);
  - `crates/security/src/journal_store/carrier_floor.rs:237`, `:826-848` (the floor step's probe, its judgment of `trust/carrier-floors/`, and its row; X3b r11 LD11-1);
  - `crates/security/src/trust/floor_publication.rs:158-172`, `:406-452`, `:455-490`, `:973-1000`, and `crates/security/src/trust/current_trust_admission.rs:89-114` (X4T r13 items 7 and 10);
  - `crates/storage/src/commit.rs:370-375`, `crates/storage/src/ledger_store/project_ledger.rs:255-262`, `:346-356`, `:535-566`, and `crates/storage/src/ledger_store.rs:123-134` (X3c r9 items 1, 2 and 10);
  - `tools/verify_design.py:155-495` (`selected_passage`, `contract_successor` and `successor_chain`) and `design-lock.json`'s `contractSuccessors` (the registry record's form and binding).

## The shape of each diff

Each law revision has the same form: the title's revision number; one new header block that says what changes and records the earlier acceptance; a changes table; its lead decisions; and the amended text in place, each change marked "(rN, …)". Everything else in the diff base is kept byte for byte. Subject line numbers:
- **X2 r10:** title (:1); header block, changes table and LD10-1 to LD10-4 (:92-127); item 4's grant, tracking sentence and write-gate join (:221, :227, :229-233); item 6's S7 sentence (:244) and leftover sentence (:298); new item 6c (:370-411); item 8 (:451); item 10 (:484); one forbidden substitute (:507); "Not claimed" (:519).
- **X3c r9:** title and status line (:1-2); r9 basis, changes table and R9-1 (:47-76); item 1's C-ACL (:107-116); item 2's step-2 note (:120), "Crash states" sentence and the resumable creation states (:125-150); item 10 (:281, :291); item 12a's tests (:300-302); item 13's units (:331-334); CL-4 and CL-5 discharged (:429-430); forbidden substitutes (:435, :447-449); "Not claimed" (:458).
- **X3b r11:** title (:1); r10's inline acceptance sentence (:20); the r11 block with LD11-1 (:30-37); item 2's C-ACL (:61-68); item 12's J4a (:364).
- **X4T r13:** title (:1); the history line, with r12's acceptance and what r13 changes (:3); the r13 changes table and LD13-1 (:5-20); item 7's dependency rule and its two completions (:192-207); item 10 (:266); item 12's tests (:331-336); item 13's J4d (:421-423); forbidden substitutes (:427); the r13 note (:471-477).
- **Registry owner selection v3:** a new directory beside v2's, in v2's form. `successor.json` has four `passageOverrides` on v2's `owner.md`, lines 9, 60, 74 and 76. Each `after` equals its `before`, one space, then the appended text that the README lists. Its parents are v2's `owner.md` and `successor.json`; its one candidate is the README; `inheritedSelectedRegistryRecord` names v2's record, as v2's named v1's.

## Lead decisions in this batch

| Where | Decision | Rejected |
|---|---|---|
| X2 r10 LD10-1 | One revision carries S7 and RW-S1, which both name X2 r10 and agree. | RW-S1 in a later revision. |
| X2 r10 LD10-2 | In item 6c, R is item 5's capture R0, which already holds RESERVED, and R0 plays R1's role as ACTIVE's predecessor. | Publishing RESERVED again; a second registry read. |
| X2 r10 LD10-3 | No new classification: on the write gate, a root that meets the join is RecoveryNeeded and gets item 6c. | A new classification value. |
| X2 r10 LD10-4 | Item 6's leftover sentence (X2:256) is amended, because X-RW-5 names it. | Leaving a sentence that contradicts item 6c. |
| REG v3 V3-1 | v3 takes v2's form: a contract-successor record with line overrides, a subject manifest and a design-unit review. | Editing `owner.md` in place; a full new copy of `owner.md`. |
| REG v3 V3-2 | Each override appends to its v2 line and rewrites no accepted word. | Rewriting REG:76's exact-marker sentence. |
| REG v3 V3-3 | The observation table and the reference model are unchanged. | Extending `registry_model.py` and its results. |
| REG v3 V3-4 | REG:1 is not retitled; the carrier stays `project-registry.v2`. | Retitling REG as v3. |
| X3c r9 R9-1 | "Not claimed" drops only X3c's own resumable-creation text, which r9 makes false. | Leaving it. |
| X3b r11 LD11-1 | The completion runs at the floor step's judgment of the existing directory, after the busy probe. | Before the probe; only at a floor write. |
| X4T r13 LD13-1 | P-ACL's bounded emptiness check at the parent step is not "a directory scan to find trust records". | Treating it as that scan; probing a fixed list of names. |

**The registry record's verdict (a lead decision of this request).** v2 is a bound contract successor in the product's `design-lock.json`. `verify_design.py` binds such a unit only through its own review: `verdict` `ACCEPT-DESIGN-UNIT`, `requiredFindings` empty, and `subjectManifestSha256` equal to that unit's manifest (`verify_design.py:186-201` at `d2c00a9`). One review cannot bind several subjects. So the record's verdict is `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`, and it goes in two places: its entry in the batch `review.json`, and its own design-unit `review.json` (see "Output"). **Rejected:** a plain `ACCEPT` in the batch file only, which would need a second review before J4b can bind v3.

**No conflict needing an owner decision was found.** S7 and RW-S1 agree (JRW:174, :190; J1:287). X3c r8's re-commit clauses and RW-S3 are disjoint (JRW X-RW-9). X4T r12's clock and write-ahead rules are kept unchanged (JRW X-RW-13).

## Not in this batch

- **RW-S5's other part,** a record note in X4B r6, shared with J1's S6. It has landed: Codex accepted X4B r6 on 2026-10-04, in the S2 to S6 batch below. X4T r13's r13 note records it.
- **RW-S6,** X9 r17's `RW-` section, in a later round.
- **RW-S7 and RW-S8,** records that have already landed (JRW:685-686).
- **J1's S2 to S6,** accepted by Codex on 2026-10-04 (`m2/reviews/codex-j1-successors-s2-s6-r1`).
- **J1's S7b** (J1:853): "M3-B and X2 successor (E-1)", which gates J2c. It names an X2 successor, not X2 r10, and X2 r10 does not carry it. It stays owed.
- **Code.** No product code changes. The code is J-RW's units J4a to J4d and J1's unit J3a. Binding v3 into `design-lock.json` is J4b's.

## Decide

For each law:
1. **Faithfulness.** Does the revision carry exactly what its successor row assigns (JRW:679-683; for X2 also J1:852 and J1:287), as JRW's items state it? Does it cite each part by item and line? Does anything go beyond the row?
2. **The lead decisions.** Is each one needed, limited to a point the row leaves open or to a conflict with the law's own text, and sound? Are the rejected alternatives right?
3. **Code.** Is every code consequence assigned to a named unit (J4a to J4d, or J3a), with no product code changed here?
4. **Preservation.** Apart from the declared hunks, is every line of the diff base kept byte for byte? Does any accepted outcome of the law, or of another law, change beyond what the revision declares? Does any public code, class, exit, detail, row, subject or remedy change?

In particular:
5. **X2 r10, the join.** Does item 4's join run on the write gate only, with every other path keeping r9's observation, classification and row byte for byte (JRW:175, :371)? Does item 6c's join equal JRW item 3.4 exactly, including clause 3: a present marker of any form, with N absent, is never the join?
6. **X2 r10, LD10-2.** Is R0 a sound predecessor for item 6c's ACTIVE replacement under item 6's replacement primitive and its retained-evidence rule, given the forbidden substitute "reconfirming R0 after RESERVED is confirmed"?
7. **X2 r10, S7.** Is "under X1's `OrdinaryWriteAdmission` only" right against J1 item 3's route (J1:257-262, :287), and is it right that no code change follows at `d2c00a9` (`register_on_gate` only)?
8. **Registry owner selection v3.** Does each override's `before` equal v2's line exactly, and each `after` equal `before` plus one space and the README's text? Do the overrides record RW-S2 (JRW:680) and no more? Are V3-1 to V3-4 right, and are the record's parents, candidates and manifest well formed for `verify_design.py`'s `contract_successor` (`:186-276`) and `successor_chain` (`:278-495`)? Judge this by reading, not by running.
9. **X3c r9.** Does item 2's L-UNC text match JRW item 3.3: the predicate, the bound k = 26 (7 tables, 1 index, 18 triggers), the guarantee and its threat model, and the stop rule and fallback? Is CL-3 kept? Is every re-commit clause of r8 unchanged? Is R9-1 right?
10. **X3b r11.** Is LD11-1's placement right against `carrier_floor.rs:826-848`, the busy probe's "write nothing" skip, and S7's rule that trust state is written only under the fence and never under a lease?
11. **X4T r13.** Are r12's clock and write-ahead rules kept unchanged (r12:170-175, :205)? Does item 7's both-ends text compose with JRW item 2 and LD-16 exactly: completion on the authenticated closure and pending write, then r12's unchanged clocked refusal, with no view and no lease? Does item 10 cite the row mapping at `d2c00a9`'s `:89-114` (JRW-R4-NB-01)? Is LD13-1 right?
12. **Across the batch.** Are the cross-references consistent: X2 r10 and the registry record; X3c r9 and X3d r9's CL-1; X4T r13, X4B's shared protocol and accepted X4B r6's RW-S5 note? Is any content of RW-S1 to RW-S4, RW-S5's X4T part, or S7 left unassigned?
13. **Anything else wrong.**

## Output

Write REVIEW.md and review.json under `/tmp/opensip-implementation/reviews/codex2-jrw-successors-r1/`. Do not commit.

review.json carries one verdict per law:

```json
{
  "laws": {
    "project-root-x2-r10": {
      "successors": ["RW-S1", "J1 S7"],
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "a0d43d9943d881e86cdff9cfe8c564b28bf1dcb2a10c49812e9efb40489bacd0",
      "preservedSnapshot": {"path": "docs/implementation/m2/project-root-x2/PROPOSAL-r9.md", "bytes": 55434, "sha256": "0d68e3a5e70578d43f95c107adc803abacf98cc84b16e4171af1d0bc27003065"}
    },
    "project-registry-owner-selection-v3": {
      "successors": ["RW-S2"],
      "verdict": "ACCEPT-DESIGN-UNIT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectManifestSha256": "0bd640d3f0c210dfa70a5fb9c167f92f2870162ae6882e5aefffde0adb4f44e2",
      "parent": {"path": "docs/implementation/m2/project-registry-owner-selection-v2/owner.md", "bytes": 32488, "sha256": "2d4b65c9b0bc088b2667c35e75bf82d1702d13703be6effb1df975e7c67c179f"},
      "designUnitReview": "registry-owner-selection-v3/review.json"
    },
    "ledger-blob-x3c-r9": {
      "successors": ["RW-S3", "X3c r8 CL-4"],
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "46156e8e6c7c59cea686a221b2044155eea6ef21b05cd66faa6e8b8180461748",
      "preservedSnapshot": {"path": "docs/implementation/m2/ledger-blob-x3c/PROPOSAL-r8.md", "bytes": 66778, "sha256": "ba638efbacda47fdddb32bfe5c4e035752c772812cf62fd63bf5766bf38760b7"}
    },
    "journal-x3b-r11": {
      "successors": ["RW-S4"],
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "27ed0aaf92cf66f53e3fdd6f7d66bfee83f077ffbe01dd69fc5245644965c1e9",
      "preservedSnapshot": {"path": "docs/implementation/m2/journal-x3b/PROPOSAL-r10.md", "bytes": 69171, "sha256": "25a60824598b9ef749e594649a8bed7129c6ccc29a493d749e8cd3956063ecb9"}
    },
    "trust-admission-x4t-r13": {
      "successors": ["RW-S5 (X4T part)"],
      "verdict": "ACCEPT|REQUIRED-FINDINGS",
      "requiredFindings": [],
      "nonBlockingObservations": [],
      "noAcceptedOutcomeChanged": true,
      "subjectSha256": "f7b187307aae0fe3174b2b8affc42ae8cdbefdb37ad53d6c9f56047c5864cdc7",
      "preservedSnapshot": {"path": "docs/implementation/m2/trust-admission-x4t/PROPOSAL-r12.md", "bytes": 79182, "sha256": "cf566db721c0dd3b24aabdbf4613062c59ecbf52d7f64ebed507016f9f9643fb"}
    }
  },
  "batchFindings": []
}
```

The registry record also gets its own design-unit review, at `/tmp/opensip-implementation/reviews/codex2-jrw-successors-r1/registry-owner-selection-v3/review.json`, with the same verdict:

```json
{
  "schemaVersion": 1,
  "reviewKind": "independent-codex-project-registry-owner-selection-v3-design-unit-review",
  "reviewer": "Codex (CODEX2)",
  "subjectManifest": "docs/implementation/m2/project-registry-owner-selection-v3-subject.json",
  "subjectManifestBytes": 454,
  "subjectManifestSha256": "0bd640d3f0c210dfa70a5fb9c167f92f2870162ae6882e5aefffde0adb4f44e2",
  "verdict": "ACCEPT-DESIGN-UNIT|REQUIRED-FINDINGS",
  "requiredFindings": [],
  "nonBlockingObservations": []
}
```

Each required finding needs an id, its law, a location, the problem or claim, the evidence and the fix. `noAcceptedOutcomeChanged` is judged apart from each revision's declared changes. Put a finding that spans laws in `batchFindings`, and name every law it touches. REVIEW.md gives the same verdicts, one section per law.
