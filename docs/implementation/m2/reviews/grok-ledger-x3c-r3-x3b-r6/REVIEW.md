# Review: evidence ledger X3c r3 and grant journal X3b r6

Verdict: REQUIRED-FINDINGS for X3c r3. ACCEPT for X3b r6.

X3c r3 `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 17736 bytes, sha256 `a17b236df38c27f4ff24e3e72c1a35f416a983f174a5c08c952d6a88eab37381`, matching hashes.txt. Preserved r2 is 17037 bytes, sha256 `8344d819e77ff63b40cebfc022305a3d6ccb548af80f5837eda156ab9334d755`. Preserved r1 is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`.

X3b r6 `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 25772 bytes, sha256 `4ee7e465e790fa3bc04ddd40c6e07e96e00e08a1487e0f10049b57dec4a72765`, matching hashes.txt. Preserved r5 is 25025 bytes, sha256 `51e927000d76488428784a626c01c0afe5a6a7da84d0a316b1bcd838392da2dd`. Preserved r4 is 24340 bytes, sha256 `296c05673cb535aec3d363f6ff908ef3d7011b2351d6322b67c47fa492c4a156`, the accepted X3b r4 subject.

The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The real OpenSIP support directory is absent. No product cargo.

The X3c diff against r2 is the title, the provenance line, and item 8's stop paragraph. The X3b diff against r5 is the title, the provenance line, and item 5 step 7's stop paragraph. No new public detail is introduced.

## X3b r5 RF-1

Closed. On a `SEAL` whose evidence `COMMIT` is called, level 4 stays held through staging, the repeated checkpoint, and `AdmissionPermit` until that `COMMIT` returns, then is released. Level 3 is never acquired under level 4. The ledger transaction is acquired before level 4.

When that path stops before the evidence `COMMIT` — a staging failure, a failed repeated checkpoint, no `AdmissionPermit`, an observer latch, or any other error after the durable `SEAL` — both laws now use one order. Roll back the open ledger transaction, which writes nothing. Release level 4, then each level-3 transaction. Append F19's `REV` through a fresh level-3-then-level-4 acquisition. Level 3 is never reacquired under level 4. Each `SEAL` exit releases level 4 once: the commit return, `CommitUndetermined`, or this stop.

That stop matches X4 r4 item 3 and the build plan's F19 and F38: abort the uncommitted evidence transaction, release the locks, then record `REV` by a new lawful journal call. X3b item 10's journal half is the same release: level 4, then level 3, then a fresh level-3-then-level-4 `REV`, and never reacquire level 3 under level 4. After a durable `SEAL` the journal transaction is already closed, so item 10's "abort the open journal transaction if any" is empty and the ledger rollback is the evidence abort.

An uncertain journal barrier stays on item 5's own rule. The journal transaction is not already closed, no evidence commit proceeds, the writer refuses every further effect, and reconciliation does not append that `REV`.

## X3b r5 RF-2

Closed. `PROPOSAL-r4.md` is the accepted r4 subject. `PROPOSAL-r5.md` is the r5 subject.

## Required finding (X3c)

### RF-1 — The stop's level-4 release is still forbidden

Item 8 now requires the stop above, including its release of level 4 before any evidence `COMMIT`, and then F19's `REV`. The same paragraph still rejects "releasing level 4 before the evidence commit, which would let a `REV` slip between `SEAL` and commit." The forbidden-substitutes line still bans "releasing level 4 before the evidence commit" with no stop named. The stop's own release is that banned sentence. The `REV` that follows it is the F19 `REV`, which the rejection names as the reason for the ban.

Required: the rejection and the forbidden-substitutes entry ban releasing level 4 and then still performing the evidence `COMMIT`. They allow the stop's release, which runs because that `COMMIT` will not be called and which is followed by the fresh `REV`. The stop order already in item 8 stays. In that sentence, the fresh acquisition is X3b item 6; X3c item 6 is staging.
