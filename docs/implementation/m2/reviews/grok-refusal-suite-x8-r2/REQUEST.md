Grok review: law X8 r2, the opaque API refusal suite (`crates/host/tests/admission_tests.rs`). Claude Opus 5.5 leads, and you are the single reviewer.

**Ground rules.**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-refusal-suite-x8-r2`.
- This is a law review. Run no cargo in the product checkout.
- The product baseline pin is `f1b8321`. The arch repo is `/Users/sb/code/opensip-ai/opensip_arch`.

**Subject.** `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md` r2. The first row of `hashes.txt` pins it: sha256 `829a70e547ef766317893a0ddf479289846b6004fcf9a1ec814aa35221b2bafd`, 39753 bytes.
- r1 is preserved as `PROPOSAL-r1.md` (sha256 `1fa3fa80…c125`, the bytes you reviewed).
- Your r1 review is in `docs/implementation/m2/reviews/grok-refusal-suite-x8-r1/` (REVIEW.md and review.json, also pinned in `hashes.txt`).
- The r1 trial evidence under `/tmp/opensip-x8-trial` is unchanged; r1's `hashes.txt` pins it.

## What r2 changes

The header's r2 note lists the changes. r2 changes only these parts:
- **RF-1:**
  - item 4b, rewritten: one shared site list, the joint predicate, and the wording change to X9 r1 item 6 and to its forbidden substitute;
  - item 4c: `operation` uses only the shared sites;
  - item 4f: the shared sites without either feature;
  - item 4g: the X3d r7 fixture sentence names the list;
  - the units: X8b depends on X9-1 and extends its pin; the record-only X3d r7 and X9 notes;
  - the forbidden substitutes.
- **RF-2:**
  - r1's `publish_revocation` is withdrawn (item 4c);
  - new item 5a, the helper process;
  - the B6 and B7 rows;
  - X8c's dependency on X9-1's publisher;
  - a forbidden substitute.

Everything else is unchanged from r1.

## Context

- Accepted X9 r1, `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`: items 2, 3, 6 and 11, unit X9-1 in item 12, gap G1, and the forbidden substitutes.
- Accepted X4 r7 item 2 (no trust write under a lease).
- Accepted X2 r8 item 7a (the handoff releases the fence and keeps the lease).
- Accepted X3d r6 items 11 to 13.

## Decide

1. **RF-1.** Does item 4b close the finding?
   - There is one list (X9-1's pin, extended by name) and one joint predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` on exactly the sites both surfaces call. AppendStep, ObjectStep and the ledger commit hook stay `cfg(test)`.
   - The features and the modules stay separate, and X9 item 2 is unchanged.
   - Is the record-only wording change to X9 item 6 and to X9's forbidden substitute correct, and does it leave X9's accepted outcome in place?
   - Does X3d r7's fixture sentence (item 4g) name the same list?
2. **RF-2.** Does item 5a close the finding?
   - B6 and B7 publish through X9 item 6's fenced helper, in a re-executed helper process that never ran `operation` and holds no lease.
   - The test thread waits for that process to exit, then calls `prepare_commit` and `publish`, with no sleep.
   - B3, B4 and B5 stay on the test thread and take no fence.
   - Is the observer-tick reasoning right?
3. Did r2 introduce anything inconsistent with r1's unchanged items or with X9?
4. Is anything else wrong?

## Output

Write `REVIEW.md` and `review.json`. `review.json` must contain these top-level keys:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on ACCEPT;
- `"subjectSha256"`: `829a70e547ef766317893a0ddf479289846b6004fcf9a1ec814aa35221b2bafd`, the PROPOSAL.md sha256 in `hashes.txt`.

Do not commit.
