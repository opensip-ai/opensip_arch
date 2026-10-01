# Review: live guards X4 r3

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 23266 bytes, sha256 `d075505c98371d3167668818e58b2f6901c165176d6158799a5a0dd31a53de00`, matching hashes.txt. `PROPOSAL-r2.md` is the r2 subject: 21270 bytes, sha256 `ec7408a79c82e898b6f3a12daeba9f308936b8acb24db6081e0a0281d502f279`. Product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. The real OpenSIP support directory is absent. No product cargo. X2 r5 and X4T r2 are the on-disk texts this proposal cites. This review does not accept them.

## r2 findings

RF-1 is closed. Item 5 runs both attempts inside one `FreshnessMonitor::read`. The single callback performs steps 1 to 4 and, when step 4's identity differs, performs steps 1 to 4 once more. It returns the coherent admitted view when either attempt's reopened identity matches its own step 1. It returns the latching error only for a still-mixed second view, an unreadable record, a failed authentication, or a floor or rollback rejection. The clock bracket covers both attempts and any wait. Both attempts charge the one per-observation ledger. A second `read` call, and unbounded retries, are rejected. The product `read` takes one `FnOnce` callback and latches on any error (`revocation.rs`), so the retry cannot be a second call. The required tests name the absorbed atomic replacement and the still-mixed latch.

RF-2 is closed. Item 8 keeps a receipt failure on its 468c row. A replaced lease file, root, `.opensip`, marker, namespace, or endpoint (identity or full sample changed) is `CONFIG.CUSTODY_REFUSED`, subject `required-files-changed`. A lease whose admitted descriptor is unchanged and whose lock is no longer held is S7's busy row: operational-failed, exit 4, `LEDGER.BUSY_TIMEOUT`, fault cause `ledger-busy`, detail `PROJECT.BUSY`, and that row is never `required-files-changed`. Those codes are the registered rows (`diagnostic-routes.json`, `public-detail-registry.json`). Item 10's RF-4 tests require both the replaced-file row and the lost-lock row.

## Ledger

The per-observation ledger matches the ceiling X4T r2 item 11 asks X4 to adopt: 2 × `TRUST_VIEW_COST` is 128 objects, 2048 edges, and 240 MiB, from 64 objects, 1024 edges, and 120 MiB. 120 MiB is 2 × (11 × 4 MiB + 16 MiB). 240 MiB is 251658240 bytes, inside the owner byte cap `BYTE_LIMIT` of 268435456 (`work_ledger.rs`). The ledger covers both attempts of one read, is not charged to the operation ledgers, and does not reset the monitor history or the latch. Item 9 still charges that first admission to the gate ledger while the fence is held, which is the charge X4T r2 item 11 states.

The header and the r3 note still say X4T r1. The body uses X4T r2's ceiling. That citation lag does not change the bound. X4T r2 item 11 still says this proposal states the old 2048-object, 16384-edge, 64 MiB ledger. The current item 5 does not. That sentence is X4T's, and it is not a finding against this law.

## The rest of the law

The observer never takes the installation fence. `state.v1` is published by atomic replacement. `observe_revocation` runs against the immutable start epoch: a revoking match or a dropped required grant revokes; an unrelated revocation update or a policy change that keeps every required grant continues and is recorded as drift; the start epoch is never replaced; a newly named revocation record is opened and authenticated. A lower counter stays X4T's floor rejection.

The checkpoint sequence under a `JournalAppendLock` borrow is unchanged and still sound: guard rechecks, then the monitored observation, `StopObserver::observe` must be `Preparing`, then one no-I/O clock sample within 10 s of the earliest instant of that read, then immediately `FinalGate::admit` or the effect intent append. X3b and X3d repeat that sequence after blocking SEAL, witness, or association work. A latch after a lawful admission is `1 → 3` and does not relabel the admitted commit. A latch before admission is `0 → 2` and admits no `RA`, intent, commit, or `SEAL`. A confirmed commit stays committed. The abstract lock exists only under `cfg(test)`. Provenance is not a live obligation. Effect-admitting guards are complete or absent. X4 depends on X4T and does not fold it in. The refusal rows use the existing vocabulary.

The ordering of the first read is not closed. See the finding below.

## Required findings

### RF-1 — The first monitor read is still the handoff's admission

Item 2 creates the one `FreshnessMonitor` and `FinalGate` at X2 r5 item 7's lease-free point: after R is current, before any lease, the same point as X4T r2's fenced admission, and it says trust state is never written under a lease. It then says item 7a only moves them into `ProjectOperation`, and that the handoff's fenced X4T admission then runs as the monitor's first `read`. X2 r5 item 7 takes the lease before item 7a. Item 7a holds that lease for the join, the transfer, and X3b's carrier start, and only then releases the fence. X4T's first read performs items 2 to 7, including the write-ahead floor. X4T r2 item 9 says that read is not part of item 7a, and it rejects running the admission there because the lease is held and S7 forbids the floor write under a lease.

Failure scenario: an implementer follows the sentence that item 7a only moves the monitor, and then runs the handoff's X4T admission as the first `read`. That call writes the floor inside item 7a, after the lease is taken. Item 6 builds `OperationGuard` inside that handoff, item 9 charges "the X4T admission at handoff", item 10 times the bound from "the handoff capture", and X4a creates the guard inside the handoff. The floor write lands under the lease.

The first `read` is the X4T admission at the lease-free point, before any lease, and that call is the monitor's first read, so the clock brackets it. Item 7a only moves the already-run monitor, the admitted view, and the gate into `ProjectOperation`, and it publishes no trust state. Items 6 and 9, the handoff-capture test, and X4a's creation step place the guard's assembly on that already-run view. They do not place the admission inside item 7a.
