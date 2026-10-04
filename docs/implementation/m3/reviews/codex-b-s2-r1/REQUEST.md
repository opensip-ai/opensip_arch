Codex review: **B-S2**, round 1. B-S2 is the contract successor that accepted law M3-B r2 names as S4: identity `vcs-observation` schema 3, with per-member VCS rows for D15 multi-repository workspaces. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex-b-s2-r1`.

(Lead note: this request was first written for GROK2. Codex reviews it because Codex was free; the unit README's line 120 still names `grok2-b-s2-r1` as the review path, and that guidance text is superseded by this directory.)

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. A timing-sensitive crash-matrix lead set may be using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.


**M3-C citations (lead note).** `MC:n` line citations refer to M3-C r6 **with its acceptance note**, the bytes at arch commit `3590205a9`. Read them with `git show 3590205a9:docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (sha256 `a2f16b7b…`). Run git read-only with a private `HOME`. The live path now holds the M3-C r7 draft, a narrow row-8 amendment in review with CODEX2, which doesn't touch SX-1 or the D15 rows. `PROPOSAL-r6.md` is the same text without the two-line note, so its lines are two lower.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/config-discovery-b/b-s2-subject.json` (1,469 bytes, `9c17e1f674f64135111c3923a6dce7e847b75749a51af2416c4bd50bb5558d0a`). Its members, all under `docs/implementation/m3/config-discovery-b/b-s2/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record, with 2 passage overrides on IE.
- `PASSAGES.md`: both overrides, rendered.
- `schemas/identity-schemas.v3.b-s2-additions.json`: the identity-bundle fragment.
- `evidence/build_b_s2.py`, `evidence/check_b_s2.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `b-s2-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`. It is not part of the subject.

**The law it serves.** `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, M3-B r2, which you accepted:
- item 22's snapshot paragraph (MB:685-689);
- the forbidden "version-3 VCS observation for a single-root project" (MB:700);
- the S4 row (MB:775);
- B-S2's unit row (MB:842).

The consumer is M3-C r6, accepted by CODEX2 (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`). Read its item 4 (MC:274-296: VCS reads, `dirty`, and the D15 workspace shape at MC:281-285) and its successor VCS-1 (MC:1046), which also targets IE:542-546.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (the F8b binding; 77 contract successors), read-only. The consumers named in LD-1 are `crates/evaluator/src/run_links.rs:364-373`, `crates/evaluator/src/import_joins.rs:205` and `tools/contracts/options.json:758`.

## What it does

1. **IE:542** now says that B-S2 adds schema 3. The sentence otherwise reads as before.
2. **IE:547**, the blank line after the `vcsDigest` paragraph, is replaced by a schema-3 paragraph. A blank line is kept on each side. The paragraph sets out:
   - the record `{schemaVersion: 3, kind: "none", commitId: null, dirty: false, sourceInventoryDigest, members}`;
   - `members`: 1 to 64 rows `{path, kind: "git", commitId, dirty}` in strict `path` order, with `commitId` as 40 lowercase hex;
   - schema 3 exactly when the project has an admitted member, and otherwise schema 2 with unchanged bytes;
   - no `vcs-revision` correspondence through schema 3;
   - the record name and selector, unchanged.
3. **The IDS fragment.** `#/$defs/vcs-observation` becomes `oneOf [vcs-observation-v2, vcs-observation-v3]`. `vcs-observation-v2` is the accepted record copied unchanged; the build asserts that it equals both IDS copies. `vcs-observation-v3` and `vcs-member-observation` are added.

IE:543-546 are deliberately untouched and left to VCS-1 (README LD-7).

**The lead's runs:**
- `build_b_s2.py` reproduces identical bytes twice.
- `check_b_s2.py` passes:
  - schema-2 samples admit under both the accepted and the new record, with identical canonical bytes;
  - a two-member schema-3 sample admits;
  - 13 negatives refuse;
  - it prints canonical-byte vectors, which are in the README.
- `verify_scratch.py` passes at `--rev e093e90` and on the main checkout. The lock goes from 77 to 78 contract successors, with 40 generation sources verified on the checkout. The selected inventory and inheritance are unchanged, and no bound successor overrides IE:542 or IE:547.
- A scratch check outside the subject appended B-S1, B-S2 and B-S9 together to the `e093e90` lock. It passes with 80 successors.

B-S2 has overrides only, so it binds on the verify_design at `e093e90` with no prerequisite.

## Decide

1. **Faithfulness.**
   - Is schema 3 exactly MB item 22's shape, with M3-C item 4's top-level and member rules?
   - Is every single-root `snapshot2` byte-identical: does `vcs-observation-v2` equal the accepted record, and is schema 3 emitted only with a member?
2. **Judgment calls.** Rule on the README's R1 to R4:
   - **R1:** replacing the record in place under the same name and selector (LD-1).
   - **R2:** the fixed top level, the 40-hex `commitId`, and the 1-to-64 members in `path` order (LD-2 to LD-5).
   - **R3:** failing closed on `vcs-revision` correspondence (LD-6).
   - **R4:** the IE line allocation with VCS-1 (LD-7).
3. **Closure.**
   - Is the merged `vcs-observation` closed, bounded and exclusive between versions?
   - Does Run closure's `VCS_KIND_JOIN` still hold?
   - Does anything that reads `vcs-observation` need a change C1b would miss (README BS2-F2)?
   - Is the ordering note with the I1-L draft's IDS copies right (README BS2-F3)?
4. **Conflicts.** Are the README's reconciliations with M3-B r2, M3-C r6, X2 r9, X12 r4 and B-S1 complete?
5. **Form.** Is the successor well formed for selection? Is anything else wrong?

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `b-s2-subject.json`. The lead's value is `9c17e1f674f64135111c3923a6dce7e847b75749a51af2416c4bd50bb5558d0a`;
- `"successor"`: `{path, bytes, sha256}` of `b-s2/successor.json`. The lead's value is 4,600 bytes, `1f089c83f8c80751145dde78623e79c8298bb2ac094e576f52b1791cc61467ad`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change any passage, give the exact replacement text. Do not commit.
