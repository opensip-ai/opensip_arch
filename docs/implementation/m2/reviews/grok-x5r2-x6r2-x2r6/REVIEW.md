# X5 r2, X6 r2, and X2 r6

Grok. Three laws. No product cargo. Product HEAD `859089a74a6fecf8137471ff49b555e20e1f9887`. The OpenSIP support directory is absent. `hashes.txt` recomputed 3/3.

## X5 r2 — ACCEPT

`replay-join-x5/PROPOSAL.md` is 9800 bytes, sha256 `d2a1f585517b19a6c07b5a6267875dd2d728c05ffa1a7c49bd62cf4a33454365`. Preserved `PROPOSAL-r1.md` is the reviewed r1: 8969 bytes, sha256 `140c6338b1809ac83db8ca45997fc4842eacf21808532a8f10df48087d574428`. The diff is the title, the r2 provenance sentence, item 5's two input rows, and item 8's two tests.

**RF-1 is closed.** `Input(MissingObject(key))` and `Input(MissingBlob(digest))` take the promised-bytes-lost route: operational-failed, exit 4, `HOST.IO_FAILURE`, `host-io`, detail `evidence.missing`, with the missing key or digest as the reference. That is the evaluator-fault contract's `promised-bytes-lost:evidence-store` row and the host-io exit. `RetainedInputError` is `closure::Error`. Its other variants are domain, identity, digest, length, canonical, candidate, and role failures, and they stay on `EVALUATION.INPUT_REFUSED` with `Structure`, `Capture`, and `Law`. `Mismatch` stays `evidence.regeneration-mismatch`. `Evaluation(e)` stays the evaluator's own mapping. Item 8 expects `evidence.missing` for a missing object and a missing blob, and `EVALUATION.INPUT_REFUSED` for a schema or identity failure inside `Input`.

## X6 r2 — ACCEPT

`carrier-recovery-x6/PROPOSAL.md` is 15834 bytes, sha256 `c81b939bc4f633265eb124df8c3445c3cb6fa0508515bae49ad114e6d175ddf4`. Preserved `PROPOSAL-r1.md` is the reviewed r1: 15035 bytes, sha256 `2c26332929bffac38cd19cb2faa227f0ecb136351d6cc43b006053fbce6201bd`. The diff is the title, the r2 provenance sentence, the X2 r6 citation, item 3's lease sentence, item 8's degraded row, and the X6b dependency.

**RF-1 is closed.** Item 3 step 4 takes `readers.lease` `LOCK_SH|LOCK_NB` without the fence and cites X2 r6 item 7 as the one exception. It takes no `writer.lease` and is never upgraded. The walk still skips 458c's fence attempt. The sweep still takes both EXCLUSIVE leases under the fence held by `admit_ordinary_writer`, and releases the fence last. The forbidden list still bars a fence acquisition or a writer-lease wait in `recover`.

**RF-2 is closed.** `committed-availability-degraded` now states both §1 projections. History is success. A selected operation that requires an unavailable object is operational-failed, `HOST.IO_FAILURE`, `host-io`, with `evidence.missing`, `evidence.corrupt`, `evidence.purged`, or `evidence.expired`. Those four details are in the public-detail registry. `recover` reports the standing and the per-object availability, and the sentence says a required unavailable object is never success. The selected operation's owner applies the second projection.

## X2 r6 — ACCEPT

`project-root-x2/PROPOSAL.md` is 37143 bytes, sha256 `898eb0a07ed1f751aae0a1b767a6d33233cce1e63a9d3954962421d51272fa6e`. Preserved `PROPOSAL-r5.md` is the accepted r5: 35787 bytes, sha256 `98d502659a07580066b3a83eea15b6e583ceafa8c484af431a2fb0ba4ffa834f`. The diff is the title, the r6 provenance sentence, item 7's exception, and one forbidden-list clause.

The exception is `recover(ExecutionId)` only. It takes SHARED-READ, `readers.lease` `LOCK_SH|LOCK_NB`, without the fence and without waiting. It takes no `writer.lease`, writes nothing, and the lease cannot be upgraded or promoted into a writer or into `FencedNamespace`. Every other lease, including the sweep's EXCLUSIVE pair, stays under the fence. The forbidden list names that exception and still bars a waiting lease and a lease upgrade. The rejected alternatives are taking the fence for recovery, and a general fence-free shared read.

That matches identity-and-evidence §5, which gives `recover(ExecutionId)` the SHARED-READ lease with no fence acquisition and no wait on a writer, and owner §5, which excludes that selector from the fenced binding path. The rest of accepted r5 is unchanged.

## Verdicts

X5 r2 ACCEPT. X6 r2 ACCEPT. X2 r6 ACCEPT.
