Grok re-review: law X3b r8, the grant journal with grant-generation rollover. It answers your X3b r7 RF-1 to RF-3. Claude Opus 5.5 leads, and you are the single reviewer.
- Make no repository edits, commits or pushes, and do not delegate.
- Write only under `/tmp/opensip-implementation/reviews/grok-journal-x3b-r8`.
- This is a law review: no product cargo.

## Subject

The subject is `docs/implementation/m2/journal-x3b/PROPOSAL.md` r8, in the arch repository `~/code/opensip-ai/opensip_arch`. Its pin is in `hashes.txt`: sha256 `82b0c66cb29e17e8fe9a7f558921f52cadafe411ac8621b51f8986b6c2451aa4`, 54686 bytes.

The r7 bytes you reviewed are preserved as `PROPOSAL-r7.md`: sha256 `b9aad8f68fd150ca5245378a7c3925b7f80e8b282fde0a772b35c7d3c948c3c5`, 52076 bytes. That equals your r7 review's subjectSha256. Diff r8 against it. Your r7 review is in `/tmp/opensip-implementation/reviews/grok-journal-x3b-r7`, and a copy is in arch under `reviews/grok-journal-x3b-r7/`.

## What changed (r7 to r8)

- **Title and header.** The title now says r8, and a header note lists the answers below.
- **RF-1 (item 5a, item 11).** `RA`, `REV` and `CLN` are admitted only when t ≤ `9007199254740989`, so the appended `seq` is at most `9007199254740990`. That is carrier-format.v3 §5 and X3b-2's `LAST_ORDINARY_SEQ` check. `GenerationFull` at t = `9007199254740990` stays on the busy row. The `SEAL` ceiling, the `TERMINAL` window and the trigger are unchanged. Item 11's boundary test covers tail `…989` admitted at `seq` `…990`, and tail `…990` as `GenerationFull`.
- **RF-2 (item 13, item 11).** Item 13's decision table has a new row: an open tail t below `provenTailSeq` refuses before any write, whether or not it is inside the window.
  - If the floor is ahead of t, it refuses as floor regression.
  - Otherwise it refuses as `uncertainTailLoss`.

  The `TERMINAL` row now requires t in the window and t ≥ `provenTailSeq`. The table's rows apply in order, first match deciding, and r7's "below the window" row is subsumed, because `provenTailSeq` ≥ `…988`. Item 11 adds the restore test: the tail left at `…988` or `…989` with `provenTailSeq` `…990`, once with the floor ahead of the tail and once behind it.
- **RF-3 (item 13, item 11).** A new row, placed before the `provenTailSeq` and `TERMINAL` rows: when the open generation G is `9223372036854775807`, the observation refuses on item 8's no-successor invariant row before any write, and no `TERMINAL` is appended. The `TERMINAL` row also requires G < `9223372036854775807`. Item 11 adds the test.

Nothing else changed.

## Decide

Are RF-1, RF-2 and RF-3 closed? Is anything new wrong?

`review.json` must contain the top-level members `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` and `subjectSha256`. Write `REVIEW.md` and `review.json`. Do not commit.
