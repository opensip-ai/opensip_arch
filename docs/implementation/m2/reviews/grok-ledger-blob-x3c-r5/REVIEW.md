# Review: evidence ledger and blob publication X3c r5

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 18248 bytes, sha256 `ffa4dc8b032f53698c410be15dc3b56afb01faedb039639e60ffb773a8c0edbd`, matching hashes.txt. Preserved r4 is 18046 bytes, sha256 `66fc8f92bee80915cfaab08f1c3c87e04785622cbcfe8b10cefc298f9d5ee220`. Preserved r3 is 17736 bytes, sha256 `a17b236df38c27f4ff24e3e72c1a35f416a983f174a5c08c952d6a88eab37381`. Preserved r2 is 17037 bytes, sha256 `8344d819e77ff63b40cebfc022305a3d6ccb548af80f5837eda156ab9334d755`. Preserved r1 is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`. The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The real OpenSIP support directory is absent. No product cargo.

The diff against r4 is the title, the provenance line, and the forbidden-substitutes line. No refusal row changes.

## r4 RF-1, the ban

The forbidden-substitutes line now forbids releasing level 4 before the evidence commit only on a path that continues to `COMMIT`, and it says item 8's stop order is not a substitute. Item 8's rejection says the same thing. Item 5 still acquires neither level-3 transaction under level 4 and never reacquires level 3 under level 4. The stop order is unchanged: roll back the open ledger transaction, release level 4, then each level-3 transaction, then append F19's `REV` through a fresh level-3-then-level-4 acquisition. A path that reaches `COMMIT` holds level 4 until that `COMMIT` returns and then releases it once. The three exits still release level 4 once each.

## Required finding

### RF-1 — The fresh REV acquisition is still cited as this proposal's item 6

The stop sentence still says that acquisition is "(item 6)". Item 6 of this proposal is staging and the prepared commit. It does not acquire `JournalAppendLock` and it does not append `REV`. The fresh level-3-then-level-4 acquisition is X3b item 6.

Required: the parenthetical names X3b item 6. The stop order and the forbidden-substitutes line stay as they are.
