# Law X3b r8 — grant-generation rollover

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `journal-x3b/PROPOSAL.md` is 54686 bytes, sha256 `82b0c66cb29e17e8fe9a7f558921f52cadafe411ac8621b51f8986b6c2451aa4`, matching `hashes.txt`. Preserved r7 is `PROPOSAL-r7.md`, 52076 bytes, sha256 `b9aad8f68fd150ca5245378a7c3925b7f80e8b282fde0a772b35c7d3c948c3c5`, equal to the r7 review's `subjectSha256`. The diff is six hunks: the title, the r8 header, item 5a's `RA`/`REV`/`CLN` cell, item 11's boundary test, item 11's two rollover tests, and item 13's decision table.

## RF-1

The admission cell now admits `RA`, `REV`, and `CLN` when `t ≤ 9007199254740989`, so the appended seq is at most `9007199254740990`. That is the reserved slot in carrier-format.v3 §5 and X3b-2's `LAST_ORDINARY_SEQ` check. `GenerationFull` at `t = 9007199254740990` stays the busy row. The `SEAL` ceiling, the `TERMINAL` window, and the trigger are the r7 text. Item 11 covers both sides: tail `…989` admitted at seq `…990`, and tail `…990` as `GenerationFull`.

## RF-2

The decision rows apply in order and the first match decides. An open tail `t < provenTailSeq` refuses before any write, inside the window or below it. The floor being ahead of that tail is floor regression, which the first row already refuses; otherwise the refusal is `uncertainTailLoss`, with no witness change and no `TERMINAL`. The append row requires `t` in the window and `t ≥ provenTailSeq`. Because a rollover's `provenTailSeq` is at least `9007199254740988`, a tail below the window takes this row. Item 11 plants the restore at `…988` or `…989` with `provenTailSeq` `…990`, once with the floor ahead and once behind.

## RF-3

An open generation `9223372036854775807` is its own row, before the proof check and the append row. It refuses on item 8's no-successor invariant row and appends no `TERMINAL`. The append row also requires `G < 9223372036854775807`. A generation already closed by a `TERMINAL` at that maximum still takes item 4a's OPEN refusal, which writes nothing. Item 11 covers the open in-window case.

## Verdict

ACCEPT. RF-1, RF-2, and RF-3 are closed. The r7 rollover, the successor rule, S7, and the `op-` token stand as accepted.
