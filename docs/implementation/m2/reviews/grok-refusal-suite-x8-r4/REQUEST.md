Grok review: law X8 r4, a record-only revision of the opaque API refusal suite. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-refusal-suite-x8-r4. This is a law review with no product cargo. Run git only read-only. Never touch the real home (`~/Library/Application Support/OpenSIP` must stay absent), and never read the private 413 UUID fixture.

## What is asked

X8 r4 records one decision that was already accepted elsewhere and makes no new one. Your review of X3d r7 recommended it (`reviews/grok-record-x3d-r7-x7-r6-x9-r3/REVIEW.md`, "X8's own record"), and `EXIT-PLAN.md` notes it as "X8 record note owed (2026-10-04)". The main question: **does any accepted outcome change?** That covers any item, trial result, case, group, code, fragment rule, feature, module, behavioural case, unit scope or dependency, or forbidden substitute of X8 r3, and any accepted outcome of another law. A record that goes beyond its source, or misstates it, is a finding.

## Pins

Pins are in hashes.txt. The accepted predecessor is preserved byte for byte, without its "ACCEPTED" note: `refusal-suite-x8/PROPOSAL-r3.md` is X8 r3, 44288 bytes, sha256 `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385`, equal to `subjectSha256` in `reviews/grok-refusal-suite-x8-r3/review.json`. The snapshot already existed. It was checked, not rewritten.

## The revision (diff PROPOSAL.md against PROPOSAL-r3.md)

Every line of r3 survives verbatim, with two kinds of exception: the title (r3 to r4), and the "r3 ACCEPTED by Grok on 2026-10-02." note that the working law already carried. Two insertions:
- **An r4 header paragraph** after r3's, saying the revision is record-only and naming its sources:
  - the overtaken sentence: "Units after the law" says X8b "Lands before X3d-2, whose storage tests use it (item 4g)". X3d-2 integrated first, at product `adc9081`, before X9-1 (`a36da7c`) and before X8b was built;
  - its source: the X3d-2 review, call 1 (`reviews/grok-commit-facade-x3d2-r1`), EXIT-PLAN's "X3d-2 ordering and follow-ups (2026-10-03)", and X3d r7's "Ordering: X3d-2 before X8b and X9-1";
  - what that ordering means, in X3d r7's words: X3d-2's storage tests take no `ProjectOperation`, and the first test of `prepare_commit` and `publish` with a real `CommitSession` is X8c's B0–B4, then X9-2;
  - what stands: item 4g as the arrangement for any storage test that needs a `ProjectOperation` in the ordinary lane; X8b's dependency list, of which X3d-2 was never part; and X8c's dependencies.
- **One "r4 (record)" note** under the overtaken sentence, pointing at the header. The sentence itself stays.

## Not recorded here

- **X9 r4's cross-reference.** X9 r4 (`reviews/grok-crash-matrix-x9-r4-x6-r4`, pending) says X8's next revision "may restate" items 4b and 4e's "`crash_matrix_support` still returns no authority type" with X9 r4's three-entry exception. X9 r4 is not accepted, so r4 records nothing of it. Please say whether you agree, or whether that belongs in this revision once X9 r4 is accepted.
- **X8b's own judgment calls.** Those are in the X8b code review (`reviews/grok-scenario-fixtures-x8b-r1`), not in this law.

## Date

r4 is dated 2026-10-04, the date of the X3d r7 review that asked for it.

## Decide

- Does r4 change any accepted outcome? See "What is asked" for what that includes.
- Is the record faithful to its named sources, and does it go no further?
- Is the predecessor snapshot exact, and is every accepted sentence preserved?
- Is anything else wrong?

Write REVIEW.md and review.json. review.json must contain:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true or false;
- "subjectSha256": the sha256 of `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`;
- the preserved snapshot's path, bytes and sha256.

Do not commit.
