Grok review: law X3d r4, a narrow amendment required by X3b r8. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-commit-session-x3d-r4.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, r4, sha256 bd6b56d17f84a90ba464c470778da59c8f57136ca41d73b4e7d175a99a043744. r3, which you accepted, is preserved as PROPOSAL-r3.md. Pins are in hashes.txt.

Why: you accepted X3b r8 (`journal-x3b/PROPOSAL.md`, sha256 82b0c66c…; snapshot PROPOSAL-r8.md). Its item 5a reserves two ordinary slots after every SEAL for its REV and CLN, and exports `seal_fits`. Its item 5a/13 text says that X3d's next revision cites this.

Change: in item 3 only, the literal threshold "proven tail ≥ 9007199254740990" becomes "`seal_fits(provenTail)` is false (proven tail 9007199254740988 or higher)". X3d-1 calls `seal_fits` and writes no literal. The title and header gain the r4 note. Diff r3 to r4 and confirm nothing else changed.

Decide: is item 3 consistent with X3b r8 item 5a and with X7 r3's trigger? Does anything else in X3d (items 4, 8, the X3d-1 unit, the tests) still assume the old threshold?

review.json fields: "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings", "subjectSha256". Write REVIEW.md and review.json. Do not commit.
