# Independent adjudication — proposed 169: recovery admission vs the S7 lease boundary

Reviewer: Claude (actual independent reviewer; Codex remains owner and will author any correction). 2026-09-19.
Subject: owner proposal `/tmp/opensip-implementation/recovery-admission169-proposal.md`, SHA-256
`8b7ea989de86f1193cc4b35226169ad00fedffb2ef6b6e971abd4242da97df73` (bytes as read: `claude-out/proposal-as-read.md`).
This is an assessment of a proposal, not a review of frozen bytes and not an acceptance: no candidate 169 exists, I
edited nothing, and nothing here is cumulative approval.

Owner bytes I read (my verified extraction of frozen reference **167**, archive `48608156…fc6f`):
| Owner | SHA-256 | Passages |
|---|---|---|
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | `2b3443e7…f4e62f` | S7 lock table ll. 730–736; modes and laws ll. 738–748; namespaces ll. 763–767; core-transition lock set ll. 769 ff.; lease-by-command table ll. 812–818; "required delivery is a separate phase" ll. 690–696; operation start/end l. 852 |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` | `42fc1917…22679d` | §2 preamble ll. 130–135; Step 0 ll. 137–143; sweep §4 ll. 406–464; delivery handoff ll. 522–526 |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `acf5a5b0…acc46` | "Read-only recovery selectors" l. 1685 ff. |
| product 168 `crates/lifecycle/src/leases.rs` (my verified extraction) | — | `try_fence` → `FenceHeld::project_lease`; `FENCE_WAIT_BOUND = 5 s`; `PROJECT_RETRY_BOUND = 30 s`; no fence-free acquisition |

## 1. Is the conflict real, and does an existing owner already resolve it?
**It is real, and no selected owner resolves it.**

- S7 (l. 744–746): "Laws: **no lease without the fence**; no waiting for a lease; no waiting for the fence while holding
  a lease (operation end releases the lease first); no upgrade". The fence itself is "bounded wait 5 s, then
  `PROJECT.BUSY`" (l. 732). Namespaces (l. 763–766): a lease names a registered namespace; "a lease on an unregistered
  namespace is a violation".
- Recovery §2 (l. 130–135): "Read-only throughout. **Prohibited for the whole algorithm: the install fence** … **any
  wait on any lock** or on the writer". Step 0, *inside* that algorithm (l. 139): "**Take** the `SHARED-READ` project
  lease **per S7** and obtain the custody-admitted store binding through an admitted handle and the registry".
- Identity (l. 1685): "`recover(ExecutionId)` **takes** the `SHARED-READ` lease and reads one consistent committed
  ledger snapshot" — it restates the lease, not how it is obtained.

"Per S7" imports "no lease without the fence" and a wait of up to 5 s into a step of an algorithm that forbids both.
Read literally, Step 0 cannot be executed lawfully. I looked for a sentence that separates admission from the
algorithm and found none for recovery. The **nearest precedent** is the delivery phase (contract ll. 690–696; recovery
ll. 522–526): "release the lease; **ordinary S7 end handoff; then a new `SHARED-READ` phase** over the committed
snapshot". That shows the owners' intended *pattern* — a read phase is entered through the ordinary S7 start — but it
speaks about delivery, not about `recover`, and does not say what §2's prohibition covers. The lease-by-command table
(l. 815–817) lists "`repair recover` … inspection alone is SHARED-READ" and is equally silent on acquisition. The
implementation already follows S7 and offers no fence-free constructor; I agree it must not grow one.

## 2. Assessment of the recommended boundary
**I agree with the recommendation.** It is the only one of the three possible shapes that keeps every existing law:

| Shape | Verdict |
|---|---|
| (a) fence-free `SHARED-READ` acquisition for recovery | Rejected, as the proposal says. Without the fence, registry validation and lease acquisition are not atomic with respect to a core transition (which holds the fence for its whole duration, ll. 769 ff.); the reader could take a lease on a namespace being unregistered or migrated — exactly the "lease on an unregistered namespace" violation. |
| (b) hold the fence through the whole read | Rejected. It breaks "readers never block a writer", blocks every admission install-wide for the duration of a read, and contradicts §2 in the other direction. |
| (c) **ordinary S7 admission first; the algorithm consumes the held context** | Preserves "no lease without the fence" (acquired under it), "no waiting for a lease" (non-blocking, once), "no waiting for the fence while holding a lease" (the algorithm never needs the fence again — including its second capture), "no upgrade", and §2's whole list from the moment the algorithm starts. |

Why retaining the binding after the fence is released is sound — the argument the correction should state, because it
is what makes (c) more than a convention: while `readers.lease` is held `LOCK_SH`, no `EXCLUSIVE` (`LOCK_EX|LOCK_NB`
on the same file) can be taken on that namespace, so purge, GC, repair-apply, migration and every core transition that
enumerates it get a busy probe and **retain/skip**. The registry entry and store binding validated under the fence
therefore cannot lawfully change for the lifetime of the lease. `APPEND-WRITE` still coexists — by design; that is why
§2 insists on exactly one ledger snapshot.

## 3. What the correction must also say (gaps in the proposal as written)
1. **Retry budget.** S7's 30 s backoff (l. 743–744) is written for "a second writer or an EXCLUSIVE request", but the
   implementation offers the same retry for `SharedRead`. The proposal says "acquire SHARED-READ once, nonblocking" —
   make that normative: recovery admission performs **no** project-lease retry, so the invocation's total lock wait is
   bounded by the 5 s fence wait and nothing else. Whichever is chosen, the number belongs in the wait disclosure of
   point 3; "the read itself waits on nothing" is only honest if the admission bound is printed next to it.
2. **Public projection of an admission failure.** Say which existing row it is: fence or project busy →
   `PROJECT.BUSY` with the `unavailable-busy` projection (operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` /
   `ledger-busy`), **with zero ledger/journal/file reads performed**; unregistered namespace → the refusal Step 0
   already prescribes ("An unregistered namespace refuses"), unchanged, just relocated before the algorithm. No new
   vocabulary is needed; none should appear.
3. **Step 0 keeps two of its sentences.** "**No liveness probe** of any kind is taken, and no in-memory active set is
   consulted" must survive the rewrite, with one clarification: the *outcome* of lease admission (busy because an
   `EXCLUSIVE` holder exists) is an admission failure, never evidence about the attempt — it must not be read as
   "attempt live" or feed `unknown-attempt-open`.
4. **The held context must be a sealed proof, not a convention.** Every boundary in this series that mattered became a
   private-field type (`AnchorAssessment`, `CapturedLedger`, `AdmittedCarrierConnection`). "Receive and validate the
   already-held admitted `SHARED-READ` context" should mean: a value obtainable only from `FenceHeld::project_lease`
   in mode `SharedRead`, carrying the namespace and the binding validated under that fence, borrowed for the whole
   read. "Validate" then means *mode and namespace match the request* — not re-reading the registry outside the fence,
   which would reopen the race the fence closed. The security crate must not gain a dependency on the lease owner for
   this; the host composes them (as 157's README already plans for ledger + anchor).
5. **Lifetime, in both directions.** The lease outlives the read *and the projection of its result* (your "consuming
   observation"); the owned evidence (150/157/168: SQL already released) may outlive the lease, and is then historical
   — say so, or a later reader will treat retained evidence as still covered by the lease.
6. **Three owners, not two.** `identity-and-evidence.md` l. 1685 says `recover` "takes the `SHARED-READ` lease"; after
   the correction it should say the lease is held from ordinary S7 admission, or the same ambiguity survives in the
   third document. Its manifest hash changes with it.
7. **Scope of §2's prohibition.** State that it governs the §2 reader only. The §4 settlement sweep lawfully holds the
   fence and `EXCLUSIVE` (ll. 453–464) while honouring "the same one-snapshot rule"; without a scope sentence, §2's
   "prohibited: the install fence" reads as contradicting §4 too.
8. **Nested reuse (point 4) — tighten one case.** Reuse by a caller already holding the right `SHARED-READ` context is
   fine. For an `APPEND-WRITE` or `EXCLUSIVE` holder, "release/re-admit at the outer operation boundary" is right and
   should cite the existing end handoff (l. 852: release the lease **before** acquiring the fence, then reacquire
   non-blocking) so nobody implements "drop writer, grab reader" without the fence in between. A latched committing
   session starts no such phase (l. 695–696) — keep that sentence adjacent.

## 4. Guarantees checked against the proposal
| Guarantee | Preserved? |
|---|---|
| S7: no lease without the fence; no fence wait while holding a lease; no upgrade; non-blocking leases | yes (with §3.8's citation) |
| Registry consistency / no lease on an unregistered namespace | yes — validated under the fence; pinned afterwards by `LOCK_SH` excluding `EXCLUSIVE` (§2 above) |
| §2: no fence, writer lease, write, wait, repair or grant *during the read*; 1 ledger + ≤ 2 journal snapshots, ≤ 4 + 4 file reads | yes, unchanged |
| Invocation-level honesty about waiting | yes **if** §3.1's bound is stated; otherwise the "no wait" claim is only locally true |
| No settlement, registration, authority, vocabulary or flock change; Python models untouched | yes — and correct that the lanes cannot prove a physical admission owner exists |

## 5. Verdict
**The conflict is genuine and unresolved by any selected owner; the nearest text (the delivery-phase handoff) shows the
intended pattern but does not cover `recover`. The recommended boundary — ordinary S7 admission (bounded fence wait,
registry validation, one non-blocking `SHARED-READ`), fence released, then a read-only algorithm that *consumes* the
held admitted context and never re-acquires — is the right resolution and the only one that keeps both S7 and §2
intact. Before it is frozen it should additionally: fix the retry budget and print the invocation's wait bound; name
the existing `unavailable-busy` / refusal projections for admission failures with zero reads; keep "no liveness probe"
and forbid reading lease busyness as attempt liveness; make the held context a sealed, host-composed proof validated
by mode and namespace only; state both lifetimes; correct the third owner (`identity-and-evidence.md`); and scope §2's
prohibition so it does not collide with the §4 sweep.** This is an opinion on a proposal: not acceptance, not a review
of any 169 bytes, and no approval of host integration.
