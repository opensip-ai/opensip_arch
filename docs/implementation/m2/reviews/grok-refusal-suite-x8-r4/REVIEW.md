# X8 r4

Claude Opus 5.5 leads. Grok is the single reviewer. Law review only. No product cargo. Git was read-only. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Verdict: **ACCEPT**. `noAcceptedOutcomeChanged` is true. r4 records the X3d-2-first ordering and changes no accepted outcome of X8 r3 or of any other law.

| | |
|---|---|
| Subject | `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`, 46639 bytes, `3b0ead97b2e925ad1eef2456ad0f47b4fd5b963ffd0bfaea960faa7e83c85b00` |
| Preserved snapshot | `docs/implementation/m2/refusal-suite-x8/PROPOSAL-r3.md`, 44288 bytes, `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385` |

The snapshot equals `subjectSha256` in `reviews/grok-refusal-suite-x8-r3/review.json`, whose verdict is ACCEPT. r3 is 365 lines and r4 is 377. Every r3 line survives in order. The two lines that are not byte-identical are the title (`r3` to `r4`) and the r3 header, which gains `r3 ACCEPTED by Grok on 2026-10-02.` The insertions are the r4 header and one `r4 (record)` note under the overtaken sentence. The sentence itself stays: X8b "Lands before X3d-2, whose storage tests use it (item 4g)."

## The record matches its sources

The header says the revision is record-only, dated 2026-10-04, and names the sources the X3d r7 review and EXIT-PLAN name.

The overtaken sentence is the unit-list bullet. X3d-2's review, call 1, accepted integrating X3d-2 before X8b and X9-1, and said that unit's storage tests take no `ProjectOperation`: they run the functions `prepare_commit` and `publish` compose, on a scratch `I/stores/S`, with a real replay and no session. X3d r7's "Ordering: X3d-2 before X8b and X9-1" records the same fact, and says `prepare_commit` and `publish` with a real `CommitSession` are first tested together by X8c's B0–B4, then by X9-2's matrix, and that no X3d requirement of the unit is left unmet. The X3d r7 review's "X8's own record" asks for this note on X8 and leaves X8's accepted text in place. EXIT-PLAN's "X3d-2 ordering and follow-ups (2026-10-03)" and "X8 record note owed (2026-10-04)" say the same.

Product history matches the commits the header names. `adc9081` (`adc9081a0408f9cdac50b87c791f36d30f29e965`, the storage facade) is an ancestor of `a36da7c` (`a36da7ce495b49c2d82ad31a9ecef707e6de9909`, the crash-matrix surface). At `a36da7c`, `scenario-fixtures` is an empty feature so the joint predicate can name it, and the manifest comment says X8b gives it its module. There is no `scenario` module. X8b was not built at either commit.

What the header says still stands is the text r3 already has:

- Item 4g stays the arrangement for a storage test that needs a `ProjectOperation` in the ordinary lane: `scenario-fixtures` as a dev-dependency, not a crate-private `cfg(test)` fixture and not a production seam. The item's own sentence is unchanged.
- X8b's dependency line stays X9-1, X2e, X3a-1, X3b-3, X4a, X4T-0, and X3c-2. X3d-2 is not on it.
- X8c's dependency line stays X8b, X3d-2 (and so X3d-1, X4a, and X3c-2), and X5a, with the B6 and B7 needs on the following bullet.

The `r4 (record)` note under the unit bullet points at that header and restates only the overtaken ordering and that item 4g stands. No item, trial result, case, group, code, fragment rule, feature, module, behavioural case, unit scope, dependency, or forbidden substitute is edited.

## X9 r4's cross-reference stays out of this revision

X9 r4 is accepted. Arch commit `5733fc9fd` records that acceptance, and the r4 review verdict is ACCEPT. Its cross-reference still reads, in the current X9 law: items 4b and 4e say `crash_matrix_support` "still returns no authority type"; from r4 on that sentence is read with X9's three-entry exception; X8 is not edited there; a later X8 revision may restate it. "May" is permission. The sources of this revision are the ordering note X3d r7 and EXIT-PLAN asked for, and they do not include that sentence. Leaving it unrecorded changes no X8 outcome. A later X8 revision may restate items 4b and 4e. This one does not.

`hashes.txt` pins EXIT-PLAN and X9's `PROPOSAL.md` at the bytes of arch `6e16b026d` and of the X9 r4 subject. The tree has since added EXIT-PLAN's closure-binding blocker and accepted X9 through r6. The two EXIT-PLAN paragraphs this header cites are unchanged, and the X9 cross-reference sentence is the accepted r4 sentence.

Nothing else is wrong. The worktree was not committed.
