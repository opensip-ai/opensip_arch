# Law X3d r4 — CommitSession capacity threshold

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `commit-session-x3d/PROPOSAL.md` is 23757 bytes, sha256 `bd6b56d17f84a90ba464c470778da59c8f57136ca41d73b4e7d175a99a043744`, matching `hashes.txt`. Preserved r3 is `PROPOSAL-r3.md`, 23334 bytes, sha256 `2524b77adc123c1804b7794a84de58a2290afe719646f36d90f2068c2b4a8d5b`, equal to the accepted r3 `subjectSha256`. The diff is two hunks: the title and the r4 header note, and item 3's capacity step. Accepted X3b r8 is `journal-x3b/PROPOSAL-r8.md`, 54686 bytes, sha256 `82b0c66cb29e17e8fe9a7f558921f52cadafe411ac8621b51f8986b6c2451aa4`.

## Item 3

`seal_fits(provenTail)` is false when the proven tail is `9007199254740988` or higher, and a SEAL fits only at a proven tail of at most `9007199254740987`. That is X3b r8 item 5a's ceiling: a SEAL at tail `9007199254740987` takes seq `9007199254740988` and leaves `9007199254740989` and `9007199254740990` for its `REV` and `CLN`. The exhaustion trigger there is an open effective tail `≥ 9007199254740988`, which is exactly when `prepare_commit` returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` before any write. X7 r3 item 6 routes that outcome, and it still describes an attempt that has written nothing. The reserved terminal slot remains `9007199254740991`. X3d-1 calls `seal_fits` and writes no literal threshold.

## The rest of X3d

Item 4 publishes a SEAL only after `prepare_commit` has returned a `PreparedCommit`, so it does not apply the old `≥ 9007199254740990` test. Item 8 charges the same reserves and does not name a tail. Item 9 still gives `CarrierCapacityExhausted` no row of its own. The X3d-1 unit list and the tests name no threshold. r3's only occurrence of the decision literal `9007199254740990` was item 3, and r4 replaces that comparison.

## Verdict

ACCEPT. No required findings.
