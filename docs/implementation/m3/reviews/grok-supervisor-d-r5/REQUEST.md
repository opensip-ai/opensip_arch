Grok review: **M3-D r5**, OpenSIP's supervisor and common control law, round 5. It answers your r4 review: one required finding (RF-1) and two non-blocking observations (NBO-1, NBO-2). It changes nothing else. This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-supervisor-d-r5`.

**Rules** (as in r4):
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No product builds or test runs. Run no `cargo`, no tests, no probes, no checkers and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git`, redirect `HOME` to a private 0700 scratch directory under your review directory and turn hooks off.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. Every cited law is pinned at an accepted snapshot, never at another law's live file.
- **The subject** is `docs/implementation/m3/supervisor-d/PROPOSAL.md` (r5). It is the subject of `subjectSha256`.
- **The base** is `docs/implementation/m3/supervisor-d/PROPOSAL-r4.md`, your r4 subject (`114e9e10…`). Diff it against r5. Every change should belong to the "r5 changes" table.
- **Your r4 review** is copied to `docs/implementation/m3/reviews/grok-supervisor-d-r4/`.
- **The product** is `/Users/sb/code/opensip-ai/opensip`, read-only. Main is now `218465f` (91 contract successors). The law still reads the product at `052d3cb`.
  - Every commit since `052d3cb` is a binding-only lock change, except P0's integration (`5e25d04`). That commit adds the `crates/components` and `crates/syntax` scaffolds, their workspace members and host dependency-policy rows.
  - `crates/security/src/component_manifest.rs` is the same blob (`2ece3789…`) at `052d3cb` and `218465f`.

## What r5 changes

- **RF-1 (D4-T4's source pin).** r5 follows your fix and the lead's direction:
  - **(b) and (c):** the security owner refuses them in both `validate` and `validate_inventory` (`component_manifest.rs:178-184`, `:268-270`, both called from `:414`). D4's arm is the DR-G29 backstop for them.
  - **(a):** nothing in those bytes checks it. Until C2a materializes CR-1's role-scoped schema copy, D4's own EE-5a check is the enforcing check for (a). Once C2a lands, RJ-6 refuses (a) first, and D4 becomes the backstop.
  - **The order:** D4 carries its own (a) check from its first integration. It does not land without that check, and it does not rely on C2a.
  - **D4-T4's pins:** (b) and (c) are pinned to the security owner's lines, as your text gives them. (a) is pinned to D4's check, with a second RJ-6 pin once C2a has landed. Your fact that the shape still refuses every closure-only role is kept: no closure-only manifest is yet a validated value.
  - **Also changed:** item 24's "who refuses each form" bullet (it replaces r4's "Agreement" bullet), its forbidden substitutes, the Units gates and D4 row, X-D4-CR1, X-D4-SL, and a marker on the r4 table's first row.
- **NBO-1:** your exact replacements, in item 25's warrant, the r4 table's X-SD5-1 row and row 57's source column. The host-invariant rejection bullet is reworded to match.
- **NBO-2:** J1 r4's matrix ends at row 55. Rows 56 and 57 are now cited as owed via J1's next revision: in item 24, the SD-5 cell, X-D4-J1-1, X-D4-J1-2 and row 57's heading. J1 r5 is in review with Codex. It carries row 56, and r5 does not cite it.
- **Record:** the product line names main `218465f` and the bindings since `052d3cb`.

## Decide

1. **RF-1.** Is it resolved?
   - Does every statement of who refuses (a), (b) and (c) now match the pinned bytes, before and after C2a?
   - Is "no condition has two routes" still true?
   - Are D4-T4's pins demonstrable?
2. **The order.** Is D4 carrying its own (a) check, independent of C2a, stated as a law, a unit gate and a forbidden substitute, and is it consistent with CR-1's D4 join and CR-T8?
3. **NBO-1 and NBO-2.** Are they applied as you gave them, and is "owed via J1's next revision" consistent with J1 r4's S20 (J1:774)?
4. **New errors, and anything else that blocks acceptance.** Section F stays an O7 placeholder.

## Output

Write `review.json` and `REVIEW.md`. `review.json` needs:
- `verdict`;
- `subjectSha256`;
- `priorFindings`: RF-1, NBO-1 and NBO-2;
- `requiredFindings`, each with id, location, problem, evidence and fix;
- `nonBlockingObservations`.

If you would change text, give the exact replacement. Do not commit.
