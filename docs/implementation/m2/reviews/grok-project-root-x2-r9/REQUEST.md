Grok review: **law X2 r9**, project-root custody, an amendment that the accepted M3 law **M3-B r2** requires (its successor S1), plus one lead decision. Claude Opus 5.5 leads. You reviewed X2 r3 to r8. This is a **law** review. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok-project-root-x2-r9.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix run may be using this machine, so run no `cargo`, no tests and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- The product is read at main `3e64266`. Every product file M3-B cites is byte-identical at `30c5db1`, where M3-B read it. Read files or use `git show`; change nothing.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until acceptance.
- **Subject:** `docs/implementation/m2/project-root-x2/PROPOSAL.md` (r9), the subject of `subjectSha256`.
- **Previous accepted:** `docs/implementation/m2/project-root-x2/PROPOSAL-r8.md` (`c31d9a02…`, 39,036 bytes). It equals the r8 subject you accepted in `reviews/grok-project-root-x2-r8`. The live file also keeps r8's "r8 ACCEPTED" note in its first paragraph.
- **The law that requires it:** `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, M3-B r2. GROK2 accepted it on 2026-10-04 (`docs/implementation/m3/reviews/grok2-config-discovery-b-r2`). Its accepted bytes are `PROPOSAL-r2.md` (`92e65825…`); the live file adds only the acceptance note. Read **M3-B item 21**, which is r9's content, and items 2, 3, 12, 19, 20, 24 and 25, which r9 cites. GROK2's r1 review (`…/grok2-config-discovery-b-r1`) confirmed item 21's eight safety points (its R7) and the ledger reading (its R3).
- **X12 r4** (`docs/implementation/m2/policy-admission-x12/PROPOSAL.md`), assigned to you in parallel as `reviews/grok-policy-admission-x12-r4`. Its pack admission is the step that item 3a's order places.

Diff r8 against r9. Check that every change is in the r9 header or is marked "(r9)" or "r9".

## What r9 changes

r9 carries M3-B item 21, plus one lead decision (item 7 below):
1. **Item 1, premise scope.** The objects the premise may admit gain:
   - `<root>/.opensip/local.json`, a custody-checked configuration file;
   - the directories the downward discovery walk custody-judges, from the root to each unit;
   - for each admitted D15 member M, exactly `M/.git`, `M/.git/config` and `M/.git/index`, and nothing else under `M/.git`.
2. **New item 3a, carrier capture.** S3's selection keeps the descriptor of the `opensip.json` it judged. `.opensip/local.json` is judged the same way when the invocation is interactive. The resolver reads both from those descriptors, at most 4 MiB, and their metadata samples join item 3's held-fence recheck set.
3. **New item 6b, the member observation.** It runs after the fence is released, on M3-B's discovery ledger, only when item 6a's observation of W is "no repository". For each declared member it checks placement (M3-B's M1 to M3, quoted), then item 6a's layout and index decoder, unchanged. The member evidence is not in the fenced recheck set.
4. **Item 8.** No new code. There are four new subjects: `member-vcs-unsupported:<reason>`, `member-outside-volume` and `workspace-root-inside-repository` under `PROJECT.ROOT_CUSTODY_REFUSED`, and `members:<n>>64` under `PROJECT.SCOPE_LIMIT`.
5. **Item 10.** M3-B's unit B1-b owns 3a, and its unit B3-b owns 6b.
6. **Forbidden substitutes.** All of them apply to members. Four are added: 6b without its precondition, a member admitted from the environment, any member Git object beyond the three, and any write under a member.
7. **Lead decision: item 3a's order.** Neither M3-B nor r8 ordered item 3a's reads, resolution and X12 r4's pack admission against item 2's placement check and item 3's chain walk. All are reads under the fence, so either order was lawful, but the refusal differed: a root outside H that also has a refused pack ID got either `outside-home` or X12's row 1.
   - **Decided order:** S3's selection walk, then item 2's placement check and item 3's chain walk, then item 3a's carrier reads, configuration resolution and pack admission, then item 5's registry capture.
   - **Effect:** a misplaced root, or one whose chain fails, is refused before any configuration byte is read. The selection walk still judges `opensip.json` and keeps its descriptor; only the bytes wait.
   - **Rejected:** reading, resolving and admitting packs straight after the selection walk; and leaving the order to B1-b, so that a public refusal depends on the implementation.

The header also carries item 21's safety argument, basis, rejected alternatives and controls.

## Reconciliations (the r9 header states each)

- **Names.** In r9's text, "M3-B item N" is M3-B's and a bare "item N" is X2's. M3-B's W and M clauses, units and short names are glossed.
- **`local.json` is not an operational file.** It sits under `.opensip/`, but item 1's "never covers" bullet stays about operational files such as the marker. `local.json` is a configuration carrier, and its custody refusal is item 8's `CONFIG.CUSTODY_REFUSED` row.
- **Item 9's one ledger.** Item 3a runs inside admission and is charged there. Item 6b and the downward walk run after item 7a's handoff, on M3-B item 12's discovery ledger.
- **The `PROJECT.SCOPE_LIMIT` remedy.** Item 8's registry-capacity remedy stays the three registry subjects' remedy only. M3-B gives `members:<n>>64` no remedy text. Its item 24 rows are successor S3's content, so r9 states none.
- **Where the subjects apply.** M3-B item 24 decides it. A member that a reader declared, and that fails 6b, is excluded and disclosed, not refused.
- **Line citations.** X2:NNN citations, in M3-B and in r9's own text, are r8's lines, preserved in `PROPOSAL-r8.md`.

## Disclosed for you to judge

- **The remedy gap** (left open by lead decision). `members:<n>>64` has no remedy text anywhere yet. The native model keys `PROJECT.SCOPE_LIMIT`'s remedy per field (`SCOPE_LIMIT_REMEDY`, `docs/coop/design-corrections/native/native_evidence_model.v2.py:4080`), and X7 r2 (answering your X7 r1 RF-1) records that X2 item 8 and S12 fix this code's subjects and registry remedy. r9 leaves the members remedy to S3 (B-S1), and the r9 header says so. Is that acceptable for this law, or must r9 state it?

## Decide

1. Does r9 carry M3-B item 21 faithfully: item 1's three additions, 3a, 6b, the four subjects, the units and the four forbidden substitutes? Is anything of item 21 missing, or anything added beyond it other than the marked lead decision?
2. Are the reconciliations faithful to both M3-B and r8? In particular, check the `local.json` reading against item 1's "never covers" list, and the item 9 ledger reading.
3. Does 6b reuse item 6a's closed layout exactly, with no new Git semantics? Check it against `git_tracking.rs:295-317`, `:429`, `:697-713` and `:807`.
4. Is the lead decision on item 3a's order sound? Is it consistent with item 5's "placement check runs first", and with X12 r4's "immediately after S3's selection walk and the configuration carrier captures"?
5. The disclosed remedy gap.
6. Does r9 change anything else in r8?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"subject"`: path, bytes and sha256;
- `"preservedR8"`: `PROPOSAL-r8.md`'s path, bytes and sha256.

This is a law review, not a `verify_design` unit. Do not commit.
