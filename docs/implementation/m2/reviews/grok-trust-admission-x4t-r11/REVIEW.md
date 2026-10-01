# X4T r11 — revocation against the signing root

ACCEPT. r10's RF-1 is closed. The diff from `PROPOSAL-r10.md` is the title, one header sentence, and item 4. The two-root split, the closure join, and X4T-a3 are unchanged, and r10 raised no other required finding.

## Subject

`docs/implementation/m2/trust-admission-x4t/PROPOSAL.md`, r11, 53342 bytes, sha256 `7fe098fd30de298cf1e09ca6514d8a50eef6a328cb25bda6ebcf4398353cd384`. r10 is `PROPOSAL-r10.md`, 53028 bytes, sha256 `3484dc5d966ffd41cc6c8f50d2caab29fa3bf8cd3cc3eba322038fdd016b30a8`, the text r10 reviewed. Both pins match `hashes.txt`. No product cargo. `~/Library/Application Support/OpenSIP` is absent.

The unified diff is two hunks. The title says r11. The header adds: r11 answers Grok X4T r10 RF-1, and r10 bytes are preserved in `PROPOSAL-r10.md`. Item 4 is the only decision sentence that changed.

## RF-1

r10 required item 4 to verify `heads.revocation` against the signing root, `heads.root`, root M, with the keys revoked before it. N is not that key set.

Item 4 now says `admitted_revocations::verify_revocation` verifies exactly the stored body and envelope that load supplied against the signing root, `heads.root` (root M), with the keys revoked before it. The parenthetical records that r9 and r10 named the accepted root, which r10 redefined as root N, and that a list signed by M need not meet N's quorum. That is the same root item 3's Signatures sentence already uses for every accepted document, the root S5 advances the counter to, and the root `open_heads` passes to `verify_revocation`. A one-root chain is unchanged, because N and M are the same document. A rotated release signed by root 2 is verified against root 2. A quorum failure stays item 10's existing `PAYLOAD-NOT-ADMISSIBLE` row, which is registered in `public-detail-registry.json`. r11 adds no public code and no diagnostic route.

## What r10 already accepted

The rest of the file is byte-for-byte r10. Item 3 still passes N, the first `rootChain` document, to `authenticate_shared` as the accepted root and `heads.root` as the signing root, so `verify_captured_core` admits a rotated chain and a one-root chain keeps r9's result. Item 7 still reads every floor from `clock.record`, equal to the signing root's counters, and compares none of them to N. The closure join is still that the last `rootChain` document equals `heads.root.document`. Item 13 still places X4T-a3 as the reader successor, with X4B-b depending on it. r10's review recorded those as accepted and named only RF-1.

## Verdict

ACCEPT. RF-1 is closed. No new finding.
