# Independent source + formal review — native runtime42 / source postchecked-reader-439

Actual Claude Opus 5, 2026-09-21. Bounded, independent. No repo edits, selection, commits, push or
delegation. I owned the serial native lane. Detailed commands, logs and hashes are in `evidence/` and
`hashes.txt`; no compiled binaries archived, no native account details printed.

I wrote the 429 advice this primitive implements, so I reviewed it against the source and by
execution rather than against my own recollection of what I recommended.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Three non-blocking observations.

## Formal, archive, staging

All three pins match (subject `78359b48…` 2480 B, archive `95d89ba8…`, manifest `5abd61ed…`).
12 members verify; 11 candidates = subject minus record, pin-identical; 3 sorted parents (owner-406,
runtime-41, inventory-62), all accepted, none overwritten; no path reuse; no overrides; unit not in
the lock; `stage.py` byte-identical to the accepted v41 helper.

All **618** members hashed in memory — regular files only, none unsafe or duplicated, membership
equals manifest. **596** product − 1 lock = **595** non-lock = **592** unchanged + **3** mapped, all
three **existing** platform paths, zero new files, no dependency or layout change, and the archive
product set equals the live 596-file tracked set. The archive lock equals the live **37/63** lock
with its five inherited meanings and is excluded from materialization by exact path. Map, baseline,
and the recorded stage stdout all verify; my own staging reproduced 618 / 595 / 3 / 592 with the live
product untouched.

## The sequencing primitive

`read_bounded_reserved_with_postchecks<R: Read, E: From<ReadFailure>>` implements the shape my 429
advice described, and the implementation is more careful than the sketch in two respects.

**Budget partition.** The read share is carved with the accepted 41 `with_allowance`, so the read
cannot consume postcheck space — the failure root demonstrated at 431. The doc states the trap
explicitly: the parent must already hold read **plus** postcheck allowance, and for
`WorkLedger::effect` that total goes in the *second* argument because the first is charged but not
spendable. Documenting the counterexample at the callsite is the right response to it.

**Type-level provisionality.** The inner closure returns `Result<Result<Vec<u8>, ReadFailure>, WorkFailure<E>>`:
the outer arm carries terminal failures, the inner arm carries the provisional outcome. Budget failure
and `InvalidLimit` propagate out through `?` and skip the callback; ordinary `Io`, `Reserve` and
semantic `Bound` become `Ok(Err(..))` and are held in one private local. That is the distinction my
advice argued should be type-level rather than conventional, and here it is exactly that.

**No early escape.** The callback signature is `FnOnce(&R, &mut ReservedPostchecks<'_>) -> Result<(), WorkFailure<E>>`.
It receives a *shared* borrow of the same original reader and the parent's protected remainder — never
the accumulated `Vec`, never the pending outcome — and it returns `()` on success, so it has no channel
to emit anything. `read_charged(&mut reader, …)` borrows mutably only inside the `with_allowance`
closure, so the later `&reader` borrow is conflict-free; that is the callsite-usability fix root
describes, and it works because `&mut R: Read`.

**Precedence and finalization.** A postcheck error returns through `?` and discards `pending`, so it
outranks a pending read error — matching `read_one`'s existing order. Only after the callback succeeds
is a pending read error converted into `E` and returned as `Operation`, closing the owner. Bytes are
returned only when both the read and the callback succeeded.

I verified the ordering by execution with explicit traces rather than inferring it:

| Probe | Observed |
| --- | --- |
| P1 success | `used` equals the whole allowance exactly; postcheck ran; bytes returned after it |
| P2 ordinary IO error | **postchecks RAN**, then `PermissionDenied` preserved, owner closed |
| P3 postcheck error + pending read error | postcheck error won |
| P4 budget exhaustion in the read share | **postchecks SKIPPED**, owner closed |
| P5 postcheck budget failure caught and swallowed | bytes withheld, owner closed |
| P6 oversize | postchecks RAN, then semantic `Bound`, no prefix |
| P7 panic inside the callback | propagated, owner closed, no bytes released |
| P8 invalid limit | converted into `E` before the reader; postchecks skipped |

That is the complete disposition table from the 429 advice, now measured: terminal work failure stops
immediately; ordinary read failure keeps the required checks; postcheck failure outranks it.

The `actual File` fixture proves what it claims and no more — `ptr::from_ref` equality plus
`dev/ino/len` at callback time show the **same** object, and the test comment says plainly that this
is usable borrow, not custody.

## Replay

**20** reader integration tests (8 inherited + 12 new), **13** ledger integration tests, and
`check --workspace --all-targets` clean with **zero** warnings. No full security suite was needed. The
438 evidence is root's; 439 makes no fresh native claim and the 595 non-lock bytes are exactly 438's
with only the lock rebased, which my archive comparison confirms.

## Root's qualifications on my 41 review

Both are fair and I accept them. My "the callback form is sounder" claim was under-argued — a correct
returnable split could also enforce an exclusive parent borrow, and I showed only that *this* form
does, not that the alternative cannot. And my counting-fixture suggestion would not catch a future
internal OS API addition either, so it pins today's shape rather than guaranteeing future accuracy.
The frozen name observer's one-call/one-buffer reading stands, with future cost changes needing review.

## Limits

This is a sequencing primitive for an **arbitrary** callback. It orders read, checks and finalization;
it does not establish that any actual native check occurred, and I draw no such inference. Existing
native adapters are not rewired and complete 429 native composition remains open: the owner still owes
real descriptor, directory, name, account and custody checks and properly derived costs, with ACL and
descriptor costs still unresolved. Standalone `read_bounded_accounted` and `read_bounded_reserved` are
unchanged and still latch ordinary I/O before returning; the header now names them explicitly rather
than saying "both entry points", which is the right correction now that a third function exists. EOF is
relative to the `Read` contract; arbitrary reader, callback and drop internals, OS, service and
allocator costs, RSS and latency are outside the claim. The typed `Reserve` branch is not an injected
allocator fault. No new authority, creator, P0 or current authority; no Linux, release, power-loss,
full M2 or M2–M6 qualification; existing law unchanged. Root substantive assent and guarded
private/live integration remain required.

## Observations (non-blocking)

1. **The callback cannot return data.** `Result<(), _>` is the safe choice — no channel to leak a
   provisional outcome — but a real postcheck that produces an observation (the `after` metadata in
   `read_one`, say) must capture it into a closure local. Ergonomic friction worth knowing before the
   native adapter is written.
2. **`InvalidLimit` remains terminal and latching**, now converted into the caller's `E`. My runtime40
   note stands unchanged: a caller parameter error still closes the shared operation. Validating `max`
   before the bracket would keep a misuse from poisoning a healthy operation.
3. **`read_allowance` is unvalidated against the parent's remainder by design** — an over-large value
   simply refuses through `with_allowance` and is terminal, which is correct, but it means a sizing
   mistake presents as budget exhaustion rather than as a distinguishable misuse. That is acceptable
   while costs are underived; it will matter more once real postcheck costs exist.
