# X4T r10 — REQUIRED-FINDINGS

Item 3's split is the amendment judgment call 12 asked for, and it matches `verify_captured_core` and S5. Item 4 still verifies the revocation list against the accepted root. After r10, that word means root N, and a rotated release's list is signed by root M. The confirming admission of X4B-a's default release would fail the list quorum instead of `FirstIdentity`.

## Subject

`trust-admission-x4t/PROPOSAL.md`, r10, 53028 bytes, sha256 `3484dc5d966ffd41cc6c8f50d2caab29fa3bf8cd3cc3eba322038fdd016b30a8`. All 11 `hashes.txt` pins match. `PROPOSAL-r9.md` is the accepted r9 text without the acceptance sentence, 45488 bytes, sha256 `c8c1bdc4a4330225558c3df829ec930fc6ac38e25ce891270b2ca130c4dd1367`. Product main is `c2352ae1a9aec1f569a501623a989aa4e095cf05`, and `crates/security/src` is clean there. No product cargo. `~/Library/Application Support/OpenSIP` is absent.

The decision diff against r9 is the round header plus the items the request lists: item 1's epoch `rootVersion`, item 2 step 3, item 3, the signatures sentence, item 7's one sentence, item 10, item 11, item 12, item 13 (X4T-0's one-root note and unit X4T-a3), the forbidden-substitutes clause, and the r10 note. The r9 acceptance sentence appears because `PROPOSAL-r9.md` omits it. Item 4 is byte-for-byte the r9 sentence.

No new public code. The incomplete row stays `CONFIG.CUSTODY_REFUSED` / `installation-incomplete`, and a list that fails its quorum stays `PAYLOAD-NOT-ADMISSIBLE`. Both are already in the public detail registry.

## RF-1. Item 4 still verifies the revocation against the accepted root

Item 3 defines the accepted root as N, the first `rootChain` document, and the signing root as `heads.root`, root M. Its signatures bullet reverifies every accepted document against M. S5 evaluates the chain from N and, on success, advances the root counter to M. X4B r5 item 2 verifies the revocation list under the final root. `open_heads` at product `c2352ae` passes `input.head.root()` into `verify_revocation`, and that head is M.

Item 4 still says the loaded body and envelope are verified against the accepted root. Under r10 that is N. X4B-a writes `heads.root.document`, the root admission's `root`, and the last `rootChain` document as the final root (`trust_bootstrap.rs`, the `final_doc` binding), and the default release rotates root 1 to root 2. A list signed by root 2 does not meet root 1's quorum. Implementing item 4 as written refuses that store at revocation, so the `FirstIdentity` gap moves rather than closes.

One-root stores hide it: N and M are the same document, which is why r9's sentence was true then.

Required: item 4 verifies `heads.revocation` against the signing root, `heads.root`, root M, with the keys revoked before it. N is not that key set. The one-root result stays r9's.

## The split, the floors, and the join

Item 3 closes the `verify_captured_core` half of call 12. The caller passes N's document reference and validated payload as the accepted root and `heads.root` as the signing root. The function, unchanged at lines 177–237 of `trust_ordinary_roots.rs`, requires the first `rootChain` body to equal N and the last to equal M, verifies N's envelope at N's threshold with revoked keys excluded, and authenticates `skip(1)` from N. A one-document chain has no links and both ends are the head, which is r9. `authenticate_shared` is the pre-time proof; intermediate expiry stays unconsulted, and M's expiry is `clock.record.rootExpiresAt` at tEval, as S5 states. The rejected alternatives match the ones call 12 named.

Item 7's comparisons are unchanged. `Floors::of_clock` reads all five floors from `clock.record` on a retained clock. `Floors::below` compares those fields. `admit_bound` sets the epoch `rootVersion` from `input.head.root()`, which is M. `check_capsule_projection` requires `clock.record.rootVersion` to equal `heads.root.binding.rootVersion`. Check 3 in `fenced_first_read` compares `view.floors()` with the hold's prior floors. N is not a floor and is not an operand. X4B-a sets both the binding and `clock.record.rootVersion` from the final root.

The closure join is lawful for both writers. X4B-a sets the last `rootChain` document, `heads.root.document`, and the root admission's `root` to the same reference. X4T-0's fixture sets `rootChain` to `[root_doc]` at `rootVersion` 1, and that document is the head. An empty chain or a chain that ends on another reference is the incomplete row, which is the right row for a misbound closure. A value-only match would allow two envelopes for one root; reference equality is the join `verify_captured_core` does not perform by itself (`ordinary_inventory::prepare` only requires that the signing-root reference occur somewhere in the chain, and that the manifest's count match).

N needs no further record. It is the first `rootChain` document of the `PayloadMetadataClosureV1` named by the root admission's `parent`. `admit_original` checks that reference's body against the validated payload, and `verify_captured_core` checks first identity, N's own quorum, and the links through M. That is the same shape r9 used for a one-root head, with the link proofs covering the steps r9 did not have. The embedded release root stays out of this role, as item 3 rejects.

Item 11 adds N's body and envelope to the count only when N is not the head. `ChainBudget` already counts N as the anchor, `Budget` dedupes a digest already retained, and the objects ceiling's margin absorbs the two files. The stated ceilings stay 128 objects, 2048 edges, and 112 MiB.

X4T-a3 is the reader successor: the two roots in `authenticate`, the closure join, item 12's rotation tests, and a test-only rotation knob on X4T-0. It depends on X4T-a2 and X4T-b. Building those tests on X4B-a's producer is rejected, which keeps the reader and the acceptance uncoupled. X4B-b's dependency on X4T-a3 is stated in item 13, and the r10 note correctly leaves the X4B r5 text change (that dependency, and the `FirstIdentity` test expecting admission at `rootVersion` 2 once X4T-a3 is on main) to an X4B amendment. What X4B-a writes is already the record r10 reads.

## Verdict

REQUIRED-FINDINGS. RF-1: item 4 must verify the revocation against the signing root M. The rest of r10 is the call 12 amendment.
