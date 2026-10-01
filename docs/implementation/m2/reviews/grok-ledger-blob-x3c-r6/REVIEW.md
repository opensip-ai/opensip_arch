# Review: evidence ledger and blob publication X3c r6

Verdict: ACCEPT.

Subject `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 18392 bytes, sha256 `15f8f9845595c274daae4e7447cb87435784ce7129f057300207b168422ccb8e`, matching hashes.txt. Preserved r5 is 18248 bytes, sha256 `ffa4dc8b032f53698c410be15dc3b56afb01faedb039639e60ffb773a8c0edbd`. Preserved r4 is 18046 bytes, sha256 `66fc8f92bee80915cfaab08f1c3c87e04785622cbcfe8b10cefc298f9d5ee220`. Preserved r3 is 17736 bytes, sha256 `a17b236df38c27f4ff24e3e72c1a35f416a983f174a5c08c952d6a88eab37381`. Preserved r2 is 17037 bytes, sha256 `8344d819e77ff63b40cebfc022305a3d6ccb548af80f5837eda156ab9334d755`. Preserved r1 is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`. The live product HEAD is `8bfc78a741158e961f727dd44f481549ec09225d`. The real OpenSIP support directory is absent. No product cargo.

The diff against r5 is the title, the provenance line, and one parenthetical in item 8. No refusal row changes.

## r5 RF-1

Closed. The stop sentence now names the fresh `REV` acquisition as X3b r6 item 6, the append lock. X3c item 6 remains staging and the prepared commit. The stop order is unchanged: roll back the open ledger transaction, release level 4, then each level-3 transaction, then that fresh level-3-then-level-4 acquisition. Level 3 is never acquired or reacquired under level 4. The forbidden-substitutes line still forbids releasing level 4 before the evidence commit only on a path that continues to `COMMIT`, and it says the stop order is not a substitute. A path that reaches `COMMIT` releases level 4 once that `COMMIT` returns. Each of the three exits releases level 4 once.
