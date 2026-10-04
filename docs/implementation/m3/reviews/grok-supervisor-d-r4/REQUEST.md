Grok review: **M3-D r4**, OpenSIP's supervisor and common control law, round 4. GROK2 accepted r3 with no required findings. r4 is a narrow amendment plus a record revision. It states the exact predicate D4 applies to the excluded forms EE-3b and EE-5a, decides the public route of item 25's request-class refusal, and records what has landed since r3. This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-supervisor-d-r4`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No product builds or test runs. Run no `cargo`, no tests, no probes, no checkers and no lead sets: other lanes may be using this machine.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git`, redirect `HOME` to a private 0700 scratch directory under your review directory and turn hooks off.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`.
- **The subject** is `docs/implementation/m3/supervisor-d/PROPOSAL.md` (r4). It is the subject of `subjectSha256`.
- **The base** is `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, the accepted r3 bytes (`9679dbc4…`). Diff it against r4. Every change should belong to the "r4 changes" table. Most of the diff is re-citation:
  - J1 lines are mapped from r3's bytes to r4's (both pinned);
  - M3P lines are 2 lower, because r4 cites the r6 snapshot where r3 cited r6's live file;
  - L's line numbers are removed, because L is cited by item and role only.

  The "r3 changes" and "r2 changes" tables are history and keep their original citations.
- **GROK2's r3 acceptance** is in `docs/implementation/m3/reviews/grok2-supervisor-d-r3/`.
- **The product** is `/Users/sb/code/opensip-ai/opensip` at main `052d3cb` (85 contract successors), read-only. Read it with `git show 052d3cb:<path>`. Every product file D cites is byte-identical between `3e64266`, r3's base, and `052d3cb`.
  - Main has since moved on: `8ca420f` (FA-2), `7347614` (RUST3-LIM), `5e25d04` (P0), `5214350` (S18) and `3fe7eb5` (CR-1).
  - None of these changes `crates/platform`, `crates/contracts`, `crates/security`, `crates/identity` or `schemas/`.
  - r4 records S18's WS overrides and CR-1's acceptance, but does not re-read the product past `052d3cb`.

## What r4 decides

- **LD-R4-1, the root-command predicate** (item 24). r3's EE-3b row counted "a `commands` entry for role `analyzer`" as an authority claim, and its EE-5a row refused "a root command". DR-103 requires every `analyzer` manifest to declare a non-empty tree whose one parentless entry is its mounted root (DR103:899-904). So, read literally, D4 refused every analyzer. CR-1's drafter found this (CR-1 README, cross-law item 3). r4 reads the sources as excluding a claim on the **host-owned root namespace**. Its sources are PPBS:719-720, AQ:343 and AQ:345, D-012 clauses 2 and 3 (CD:1076-1088), and DR103:902-926. The predicate:
  - **(a)** a closure-only manifest that declares `commands`, which is CR-1's D4 join;
  - **(b)** an `analyzer` tree outside the mounted-root model: not exactly one parentless entry, or that entry's name differing from `manifest.name`;
  - **(c)** a reserved root name among the manifest's root-namespace keys: its name, its aliases and its root's aliases.

  EE-3b keeps only its capability form. Live-name and in-tree collisions stay RJ-2's. The security owner's RJ-2 and RJ-6 refuse every form in (a) to (c) before D4 sees a value (`component_manifest.rs:178-184`, `:268-270`, `:395-414` at `052d3cb`). So D4's arm is DR-G29's backstop, and no condition has two routes.
- **LD-R4-2, item 25's route** (SD-5's X-SD5-1). The route is `request-rejected` 2, `REQUEST.UNSATISFIABLE`, detail `PROVIDER.NOT_SELECTED` with subject `excluded-form:<class>`, and no runId or executionId. Its basis is NE:3577-3579's rule for a well-formed request the product does not serve. The detail's code-keyed remedy (NEM:1159) is widened by a new contract successor, SD-7, under NE's remedy-keying constraint (NES:523). J1's row 57 is a cross-law item.
- **LD-R4-3, SD-5's remainder.** SD-5 is accepted and bound. Its four other projections become the named owed successor SD-5b, which lands with each refusal's first consumer.
- **SD-7** (new) conforms SD-5's bound NE row, which restates r3's EE-3b and EE-5a wording, and adds item 25's row. Until it binds, r4 reads SD-5's row through item 24's predicate.

## Decide

1. **LD-R4-1 (the main question).** Read PPBS's EE-3b and EE-5a, AQ §5 items 3 and 5, D-012 clauses 2 and 3, and DR-103's `commands` field, reserved list and RJ-2.
   - Is a claim on the host-owned root namespace what EE-5a's "root command" excludes?
   - Is the predicate exact and complete for a closed manifest schema?
   - Does it admit every lawful `analyzer` manifest?
   - Is EE-3b right to carry no command form?
2. **The joins.** Does the predicate agree with CR-1? You accepted CR-1 at its r4, and it is bound at `3fe7eb5`; its subject is pinned.
   - Check its D4 join, CR-T8, and CR-T9's name and alias admission for every role, with RJ-2 keeping its routes. That includes CR-1 r4's correction: live-name refusal runs in `validate` only.
   - Is "no condition has two routes" true, given that the security owner's validation precedes R10a?
   - Is D4-T4 the right control?
3. **LD-R4-2.** Is `REQUEST.UNSATISFIABLE` with `PROVIDER.NOT_SELECTED` an honest existing route for a request-class excluded form, once SD-7 widens the remedy?
   - Weigh the rejected alternatives: host-invariant, SD-5's route, `CONFIG.INVALID`, an absent detail, and a dedicated code.
   - Or does the detail's provider-specific name make it a defect that needs a dedicated code, and so an owner decision against item 24?
4. **LD-R4-3 and SD-7.** Is the split of SD-5 right, with SD-5b's timing by first consumer?
   - Is it lawful for a law to read a bound contract row's descriptive parentheticals through its own predicate until SD-7 binds?
   - Is SD-7's stated form constraint correct? NE:3540 already carries SD-5's override, and `verify_design` refuses a second one.
5. **The record items** (M3P9:323). Check that each is applied:
   - D4-T1 and D4-T2 sample at the refusal's return (J1:344, J1:347);
   - first use covers `Published`, `LostRace` and `NotPristine` (J1:233-243);
   - SD-6 is recorded as landed, with MC r7;
   - SD-5 is accepted and split;
   - F7 is answered by FA-1 and MH item 4.
6. **Re-citations.** Spot-check them:
   - the J1 r3 to r4 line map (for example J1:175-195, :308-328, :455-459, :638-709 and the matrix rows);
   - the M3P lines against `M3-PLAN-r6.md`;
   - MC r7's items 7, 12 and 16;
   - L r5's item numbers, including item 12.1's count-only rule, which r4 says closes item 17's departure.
7. **New errors, and anything else that blocks acceptance.** Section F stays an O7 placeholder.

## Output

Write `review.json` and `REVIEW.md`. `review.json` needs:
- `verdict`;
- `subjectSha256`;
- `priorFindings`: none were required at r3, so record GROK2's one r3 observation, the history sentence;
- `requiredFindings`, each with id, location, problem, evidence and fix;
- `nonBlockingObservations`.

If you would change text, give the exact replacement. Do not commit.
