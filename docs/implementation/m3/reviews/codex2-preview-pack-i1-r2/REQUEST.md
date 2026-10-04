CODEX2 re-review: M3-I1 **r2**, the X12c preview policy pack, after your r1 findings. This is a **law and contract-soundness** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-preview-pack-i1-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: crash-matrix work may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The files are untracked in arch until acceptance.
- `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` (r2) is the subject of `subjectSha256`.
- `docs/implementation/m3/preview-pack-i1/UNITS.md` (r2).

**Previous round.** The r1 bytes are preserved as `PROPOSAL-r1.md` (`2226b14f…`, the sha you reviewed) and `UNITS-r1.md` (`8fc877d4…`). Your r1 review is `/tmp/opensip-implementation/reviews/codex2-preview-pack-i1-r1/`, with three required findings and three non-blocking observations. r2's "r2 changes" table maps each finding to its change. Diff r1 against r2 and confirm nothing else changed in substance.

## What r2 changes

1. **I1-RF-1: the source census.** Item 2.5(b) now requires positive coverage of the expected `imports` source census in each universe U of V. It uses the expected-source law that incoming accounting already uses (ATOM:257, ATOM:259, ATOM:210-212):
   - **The census** is the union by U of the `imports`-cell symbol inventories (EPLAN:96-98), drawn from inventory rows only. A partial, unavailable or absent inventory gives `population-unknown`.
   - **Coverage** is exact-id membership of every expected source in the subjects of some retained exact (`imports`, `resolved-target`) scope of U. A known uncovered source gives `uncovered-expected-source-subject`, as does a universe with no scope at all.
   - **Pairing and sufficiency** stay as in r1.
   - **The law holds whatever the cell's `required` flag is**, and no `provider-unavailable` is manufactured (EXI:169, EXI:190, EXI:198-211).
   - Your counterexample is UNITS case 15. Cases 16 to 18 are your other three.
2. **I1-RF-2: identity law.** The lead decided to add an explicit identity-contract passage successor to I1's successor set (item 3, and item 4's IE:213-214 and IDS:4978 rows). The passage:
   - authorizes exactly one additive `operation` member under the existing proof3 and program-predicate majors;
   - states the admission behaviour;
   - states why no existing record, H identity (IE:168-170) or `finding-key2` changes.

   r1's "unchanged IE already permits it" is withdrawn. The major bump is rejected, with its blast radius listed in item 3. The lead found no rule in the identity contract that forbids an in-place additive widening by a reviewed successor. **Confirm or refute that reading.**
3. **I1-RF-3: population-only incompleteness.** r1's condition 2.5(d) is removed. File population is composition's alone (COMP:28, COMP:56, COMP:161-166). Item 2.4 adds the argument that the atom's false stays sound without (d). The rule that every indeterminate answer carries a cause now holds by construction. UNITS case 19 covers a partial file inventory with otherwise complete imports evidence. New LD-13.
4. **The NB items.**
   - NB-1: item 2.4's representative is relative to this Run, and non-monotone.
   - NB-2: the short unit order now includes I1-b1 → I1-b2.
   - NB-3: LD-10 states the C2 and C4 obligations (IE:272-278), and is a recommendation only.

**Unchanged:** the pack bytes and the three provisional digests, which you recomputed. Also the units' number, order and sizes.

## Decide

1. Is I1-RF-1 resolved? Does 2.5(b) close the expected-source census for lawful optional cells without manufacturing a carrier? Are the cause choices and the complete-empty rule (ATOM:242-245) right?
2. Is I1-RF-2 resolved?
   - Is the IE and IDS passage text in item 4 narrow enough?
   - Is its compatibility and admission behaviour sound?
   - Is anything in the identity contract a bar to an additive exception by successor? If something is, item 3's fallback is the major bump.
3. Is I1-RF-3 resolved? Is item 2.4's soundness argument for the third row's false, without a file-population condition, correct?
4. Does r2 introduce anything new that is wrong?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. I1-L and I1-P will need `ACCEPT-DESIGN-UNIT` reviews of their own. Do not commit.
