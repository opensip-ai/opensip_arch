# Review: evidence ledger and blob publication X3c r4

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 18046 bytes, sha256 `66fc8f92bee80915cfaab08f1c3c87e04785622cbcfe8b10cefc298f9d5ee220`, matching hashes.txt. Preserved r3 is 17736 bytes, sha256 `a17b236df38c27f4ff24e3e72c1a35f416a983f174a5c08c952d6a88eab37381`. Preserved r2 is 17037 bytes, sha256 `8344d819e77ff63b40cebfc022305a3d6ccb548af80f5837eda156ab9334d755`. Preserved r1 is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`. The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The real OpenSIP support directory is absent. No product cargo.

The diff against r3 is the title, the provenance line, and item 8's rejection sentence. No refusal row changes.

## r3 RF-1, the rejection

Item 8 now rejects releasing level 4 before the evidence commit only on a path that continues to `COMMIT`. That release would let a `REV` slip between `SEAL` and the commit. A path that stops before `COMMIT` releases level 4 by the stop order and does not commit. The stop order is unchanged: roll back the open ledger transaction, release level 4, then each level-3 transaction, then append F19's `REV` through a fresh level-3-then-level-4 acquisition. Level 3 is never acquired or reacquired under level 4. Each `SEAL` exit releases level 4 once.

## Required finding

### RF-1 — The forbidden-substitutes line still bans the stop's release

The forbidden-substitutes line is unchanged. It still bans "releasing level 4 before the evidence commit", with no stop named. Item 8 requires that release when the evidence `COMMIT` will not be called. The checklist and item 8 assign opposite permissions to the same release.

The stop sentence still points the fresh acquisition at "(item 6)". In this proposal item 6 is staging. The acquisition is X3b item 6, the append lock.

Required: the forbidden-substitutes entry bans releasing level 4 and then still performing the evidence `COMMIT`, and it allows the stop's release. The parenthetical names X3b item 6. The stop order already in item 8 stays.
