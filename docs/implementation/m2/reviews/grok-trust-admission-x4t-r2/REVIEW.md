# Review: native current-trust admission X4T r2

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` is 24424 bytes, sha256 `d4c30645b79b2a58577b63f07effbbd93f3996a12fe1abb62f8f5c793ce3437a`, matching hashes.txt. Preserved r1 is 17029 bytes, sha256 `131c59273fd48670c7174f4e33c8e43d8dc6d949fab92f3453c249dcf60baf91`. The request names product HEAD `f7acb6d`. The live product HEAD is `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c`. No `AdmittedCurrentTrust` exists there. The real OpenSIP support directory is absent. No product cargo.

r1 RF-1 through RF-6 are closed. One new row is unnamed.

## Closed findings

RF-1. Item 9 runs the fenced admission, including the write-ahead, under the installation fence with no project lock, at X2 r5 item 7's lease-free point, after R is current and before any lease. The `FreshnessMonitor` is created there and this admission is its first `read`. Item 7a moves the view and the monitor and publishes no trust state. That matches accepted X4 r4 item 2. S7's rule is stated on the writer.

RF-2. While the fence is held, only this admission's confirmed publication replaces the retained `state.v1` and its full sample. Any other change before release is `required-files-changed`. After release the capture is provenance. A newer pointer is a new view, and X4's S6 predicate decides revoke, drift, or rollback. A lower F, L, root version, revocation version, or index snapshot version than SC-TRUST's own retained floors is `trust-rollback` on the fenced first read. The same comparison on an unfenced reread is `OBSERVER.FAIL_STOP`. The journal carrier floor stays `{highWaterSchema, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`.

RF-3. The unfenced reread is one attempt. It does not retry and does not call `FreshnessMonitor::read`. X4's single callback opens, calls, reopens, and repeats that attempt once. A second mixed view, a rollback, an unreadable record, or a failed authentication returns to that callback, and X4 latches `OBSERVER.FAIL_STOP` (operational-failed, exit 4, `HOST.IO_FAILURE`). Item 10 does not publish those errors.

RF-4. F absent is only `TRUST.NO_ADMITTED_TIME_CONTEXT` (request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`), before the role join. The view then runs `role_machine::continuation(core, index, component)`. `ExistingOnly` is core and component `Trusted` with index `Expired` or `StaleRevocation`, and it is admitted and carried. `InstallGateRequiredForNewProcess` is admitted and carried the same way. A continuation refusal uses the continuation class, request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, with a subject that names the role and the state. An `Expired` core is `core:expired`. Clock expiry of an index or component is never an S5 `ROOT.*` row. S5 `ROOT.*` remains the chain evaluation and names the link. `CLOCK-EXCURSION-FORWARD` keeps `beyond-horizon` and `in-session`.

RF-5. The closure is eleven files plus chain N+1..M. The verifier is called with `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }`. `TRUST_VIEW_COST` is 64 objects, 1024 edges, and 120 MiB, which is 2 × (11 × 4 MiB + 16 MiB). Retention charges one object and the raw length per record, and `check_value` bounds decoded-tree work by the same byte count. X4T-a pins a view with every file at its cap and the chain at this budget, and raises the ceiling before acceptance if the measured factor exceeds two. The per-observation ledger at twice that ceiling is 128 objects, 2048 edges, and 240 MiB, inside the owner's 256 MiB byte cap. Accepted X4 r4 item 5 already uses those figures. The sentence that X4 r3 still states 2048 objects, 16384 edges, and 64 MiB describes r3.

RF-6. `permissionPolicyDigest` is `Effective::digest()`, the domain-separated hash `opensip.metadata.policy-effective.1` over the merged policy's canonical bytes. `merge` returns that digest. Both reads use it. The raw SHA-256 is not stored.

## Lead decision on the two continuation codes

Sound, including the class. `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED` are the role machine's index and component refusals, and neither is in the public detail registry. `CONTINUE-CORE-NOT-TRUSTED` is registered as request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`. The successor X4T-c adds exactly those two codes with that same class, by the 468a path: common4, the public detail registry, D9 routes, generation, and the drift check. Until that successor lands, item 10 publishes them under `CONTINUE-CORE-NOT-TRUSTED` with the role-naming subject. Permanently folding them into the core code is rejected.

## Required finding

### RF-1 — A chain past the named budget has no row

Item 11 calls the root verifier with `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }` and says a recorded chain beyond either bound refuses as its S5 chain-limit row. S5's refusals are the registered `ROOT.*` details, and each of those names a link. `ChainError::Limit` is the verifier result when `max_links` or `max_stored_bytes` is exceeded, and the chain-test projection publishes no `ROOT` code for it. The public registry has no chain-limit detail. The verifier also counts `check_value` traversal against `max_stored_bytes`, so `Limit` is that whole budget, not only a stored-byte total. Item 10 forbids a new public code and does not list this refusal.

Failure scenario: a recorded chain has 17 links, or its stored bytes and traversal work exceed 16 MiB. Item 11 requires an S5 chain-limit row. No such code exists. The projection either invents one, which item 10 forbids, or places the refusal on a link-named `ROOT.*` detail whose remedy is a chain defect.

Required: exceeding this `ChainBudget` uses the existing budget row, `WORK.BUDGET_EXHAUSTED`, operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, host-invariant, the same row as a view over `TRUST_VIEW_COST`. The chain is not truncated. A distinct public code is an owner decision scheduled the way the two continuation codes are scheduled.
