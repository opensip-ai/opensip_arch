# Law X4B r3 — first trust acceptance

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `trust-bootstrap-x4b/PROPOSAL.md` is 17231 bytes, sha256 `926f5277b7002b7de9535d48f15456782a66b52579c26167beaa43da391d19d1`, matching `hashes.txt`. Preserved r2 is `PROPOSAL-r2.md`, 15149 bytes, sha256 `5734a6514e70b7cf480c456a8260c8501b1ffb8270c1a39b270af5906c12e09e`. Preserved r1 is `PROPOSAL-r1.md`, 9132 bytes, sha256 `6615176f35649568087e55cea5dae7e60f5a444dbccc8317f09ae1af9fb26e3f`. Live product HEAD is `46b1d60faef4ca004170ae3cbcff7c9b29ad3f7c`.

Judged against accepted X4 r7, X4T r7, X2 r6, X1 r1, X3a r5, S4 steps 2 and 5, S7, and `FreshnessMonitor::read_with` at that HEAD.

## What holds

r2 RF-1 is closed on the bracket. The operation's `FreshnessMonitor` and `FinalGate` are created first, on the fence already held, before any project lease. Their one first `read` runs the retained-capsule admission. On F absent, and only then, the same counter callback runs the acceptance and the one confirming admission on the confirmed retained `state.v1`, then returns that view. `read_with` samples the start clock before it calls the counter, and on success it stores that start as the earliest instant. A slow acceptance stays inside the bracket, and the next read's bound runs from that earliest instant. X2e receives the monitor, the gate, and the view, and publishes no trust state.

The acceptance uses that read's clock sample for W, M, and B. It sets F to max(W, A) and L to A, and the anchor to (B, M, W). The confirming admission uses the same sample, so its tEval is max(F, W, A) = F. L does not advance, because A is not greater than L. The proposed anchor equals the anchor just stored, so the anchor does not advance. X4T item 7 publishes when tEval exceeds the stored F, or when L or the anchor advances. Those triggers are idle, and the confirming write-ahead publishes nothing. A second F absent stays the existing host-invariant row. The charge stays on the gate ledger, inside that read, as X4T item 11 charges the fenced first read. Item 10's ordering bullet and item 11's X4a dependency match that sequence. The r1 holdings on the payload, the `decide` sequence, the rows, and the creator path stay in force.

## RF-1

Item 5 says: "Item 1 step 3's re-admission reads that retained owner."

Item 1 step 3 is the start epoch. It takes the view the callback already returned. The read of the confirmed retained owner is the confirming admission, item 1 step 2.3, which item 4 already cites. Under the numbering this round introduced, a reader who follows item 5 places that read at the start epoch, after the callback has returned.

Item 5 names item 1 step 2.3, the confirming admission, as the reader of the retained owner. The capsule still comes from the publication's confirming reopen. Step 3 stays the start epoch.

## Verdict

REQUIRED-FINDINGS. r2 RF-1 is closed. RF-1: item 5 cites step 3 for the confirming admission.
