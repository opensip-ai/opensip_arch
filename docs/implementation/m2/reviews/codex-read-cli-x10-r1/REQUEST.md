Codex review: law X10 r1, read-only CLI enablement (`opensip doctor`). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-read-cli-x10-r1. Law review; no product cargo. Product HEAD is d1b5eda; you may read it.

Subject: docs/implementation/m2/read-cli-x10/PROPOSAL.md r1 (pin in hashes.txt). Context: EXIT-PLAN.md row X10, law 464 item 7, 468 items 6 to 8, 458c r6 items 1, 7 and 12, owner.md §1a, §5 and §6, and the command-envelope v7 schema.

## Decide

- **Item 1.** Is the scope right: `doctor` only, with the installation check as its only check, and everything else keeping its present refusal?
- **Items 2 and 3.** Do the ingress and envelope mapping match the schema and 468 item 6? Look at `kind` doctor versus failure, `errors` for the host I/O row, and the remedies.
- **Item 4.** Is human rendering with JSON parity right, including the exact note label?
- **Item 5.** Is the test seam sound? It is in-process `run_with` with the real producers swapped, plus binary tests of the dev-build behavior, plus a source pin against env, `home_dir` and cfg selection. Does any path to a scratch-home or profile override exist in a release binary?
- **Items 6 to 8.** Help and completion, schema validation, the unit split, and the golden remedy mismatch.
- Check the lead decisions, each with its rejected alternative.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
