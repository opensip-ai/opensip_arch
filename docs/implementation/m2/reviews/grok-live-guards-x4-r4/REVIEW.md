# Review: live guards X4 r4

Verdict: ACCEPT.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 23968 bytes, sha256 `43174456e723ce7c529df3c68ba33952841d84c147cadc2a1478971685210ddc`, matching hashes.txt. `PROPOSAL-r3.md` is the r3 subject: 23266 bytes, sha256 `d075505c98371d3167668818e58b2f6901c165176d6158799a5a0dd31a53de00`. Product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. The real OpenSIP support directory is absent. No product cargo. X2 r5 and X4T r2 remain the on-disk texts this proposal cites. This review does not accept them.

## r3 RF-1

RF-1 is closed. Item 2 creates the one `FreshnessMonitor` and `FinalGate` at X2 r5 item 7's lease-free point, after R is current and before any lease. At that same point X4T's fenced admission is the monitor's first `read`, and that call includes the write-ahead floor publication. S7 allows that publication only there: under the fence, with no lease. The monitor brackets the call with the clock. Item 7a later only moves the already-run monitor, the admitted view, and the gate into `ProjectOperation`, and it publishes no trust state.

Item 6 builds `OperationGuard` in that handoff from those already-created values. The guard runs no X4T admission and writes no trust state in the handoff. Item 8 reports a missing current trust at the lease-free point, on X4T's own rows. Item 9 charges that admission to the gate ledger while the fence is held, before any lease, and charges nothing for it inside 7a. The bound test times the pause from the lease-free capture. X4a creates the monitor and runs its first read at the lease-free point, and creates the guard inside the handoff from that completed read.

No remaining sentence places the X4T admission or a trust write inside item 7a. Item 5's "at handoff" sentence is the move of the directory handles whose identity was judged at the lease-free capture. The observations that follow run after the fence is released. They reject on the floor and they append nothing. The header's "single fence hold" names X3b's floor step and carrier start under the fence X2 already holds across both points. It does not put X4T's publication in 7a.

## Unchanged and still closed

r2 RF-1 and RF-2 are unchanged and stay closed. Both mixed-read attempts stay inside one `FreshnessMonitor::read`. A replaced required file stays `CONFIG.CUSTODY_REFUSED` subject `required-files-changed`. A lost lock on an unchanged lease descriptor stays `LEDGER.BUSY_TIMEOUT`, fault cause `ledger-busy`, detail `PROJECT.BUSY`. The per-observation ledger stays 2 × X4T r2's ceiling: 128 objects, 2048 edges, and 240 MiB. The header and the r3 history sentence still name X4T r1. The body uses X4T r2's ceiling and charge. That citation lag does not change the bound or the placement. X4T r2's sentence that this law still states the old 64 MiB ledger remains X4T's text.

The checkpoint sequence, the immutable start epoch, the drift continue path, the latch states, the complete-or-absent effect guard, and the `cfg(test)` abstract lock are unchanged and still sound.
