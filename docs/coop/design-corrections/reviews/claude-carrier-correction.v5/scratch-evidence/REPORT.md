# Bounded carrier correction, pass 5 — author report

**Standing.** Actual Claude as author, same origin. Not an acceptance, readiness statement,
blind-consumer acceptance, final application acceptance or self-acceptance, and not product
implementation. Private design/reference work, not OS qualification. Original blind 1/2/3, gate 8/3
and final application remain root obligations. All v4 output is retained immutable in
`scratch/v4-evidence/`, with the nested v3 evidence inside it.

**Bindings.** This runtime did not re-supply the planning inputs, so the latest root bytes are the
immutable v4 copies, read read-only: `commit-recovery-plan.v1.json` `fffb820d…` (25639 B) and
`implementation-boundaries-and-build-plan.md` `b0fbe313…` (82112 B). Frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`. Root's supplied counterexample
is hashed in the manifest and reproduced in C13.

## 1. Root's four new findings

### 1.1 Carrier migration cannot borrow the logical store-migrate protocol

Accepted in full; the v4 dispatch was wrong. C13 reproduces root's counterexample against the
frozen owner: reusing `store-migrate` with an unchanged state schema and store generation refuses
`TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE` and `TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE`, and
an invented `carrier-migrate` refuses `TRANSITION.OPERATION`. C13 also asserts the shapes: the
intent is a closed **11**-member record, the journal a closed **20**-member record, and **neither
has a carrier field**. The v4 phrase "`InstallationTransitionJournalV1`-shaped intent" conflated an
intent with a journal and is withdrawn.

New document `carrier-migration.v1.md`. Authorization is traced, not invented:

| Question | Existing owner |
|---|---|
| command | `store-gc` — `owner: security`, `authorizationClass: exclusive-lease`, **`writesTrackedIntent: false`** |
| locks | S7 install fence, then non-blocking `EXCLUSIVE` on the affected project namespace; busy = skip and retain, S7's existing GC law |
| reporting | `store-status`, whose parity fields already include `migration-state` |
| generation closure | the existing typed `TERMINAL` cause `grantGenerationClosure` |

`writesTrackedIntent: false` is the decisive property: `store-gc` is already a security-owned
exclusive-lease mutation that writes no tracked intent, which is exactly why it does not drag in
the S9.2 protocol. No new command, flag, authorization class, public operation or enum value.

**Durability order and total recovery.** Three atomic acts: **A** `TERMINAL` append, **B** object
creation (one DDL transaction), **C** format-row insert. The format **row** is the commit point and
**detection is keyed on that row**, not on the tables — that single change is what makes prefix
`{A,B}` recoverable rather than merely idempotent. `first_generation` is recomputed at C. Every
prefix has an exact resume action, verified by C13:

| Prefix | Standing | Resume |
|---|---|---|
| ∅ | inherited format, generation open | start at A |
| **{A}** | inherited format, generation **closed** | resume at B — this is root's failure-after-TERMINAL-before-final-metadata case |
| **{A,B}** | still inherited by detection | verify object definitions byte-equal, then resume at C, else `MIGRATION.CORRUPT` |
| {A,B,C} | carrierFormat 3 | none |

Commit uncertainty on A is resolved from the **frozen TERMINAL body's own `operationRef`**, adding
no field anywhere; a retry cannot double-apply because the inherited trigger refuses any append to
a TERMINAL generation. C13 also exercises the benign interleaving where a format-unaware core rolls
to a new generation in place, and confirms `first_generation` skips it. "Second migration aborts
because the table exists" is explicitly **not** the recovery mechanism.

**One honest limit, stated rather than engineered away.** A core predating `carrierFormat` cannot
be made to refuse a migrated carrier, so prevention is impossible within the inherited format.
Detection is exact — any generation at or above `first_generation` in the inherited table is a
split-brain custody condition, never valid history — and the mitigation is the existing
ordered-release pattern, not a new mechanism. carrierFormat 1 is worse, having no TERMINAL trigger
at all. Recorded as F51.

### 1.2 AttemptCustodyV1 — and a flaw C14 found in my own v5 draft

Root is right that v4's Step 1 read `phase` alone. The settlement matrix is now normative and
verified by C14 across eleven combinations, with **exactly one** cell yielding the negative:
`phase = settled` **and** `settledOutcome = refused` **and** both receipt and association confirmed
absent, all in one coherent snapshot. `settled+committed` with no receipt is a contradiction and
unavailable history, never a negative. A purged historical receipt can never become
never-committed, because a purge cannot produce `refused` and the retained sealed manifest,
provenance and tombstone still name the Run — absence of receipt *bytes* is not absence of a
receipt.

**Then C14 exposed a flaw I had introduced.** My draft carried a third `undetermined` outcome.
Because the row is immutable once settled, `settled+undetermined` would have been **unresolvable** —
nothing could ever move it to a real outcome, which is precisely the "cannot prove absence without
durable reconciliation" problem root named. It is removed. The correct separation:
`durability-undetermined` is the **D9 response to the caller**; the **custody row stays `admitted`**,
because `admitted` *is* the honest unknown; and the sweep is the durable reconciliation. The record
now has exactly two settled outcomes, because those are the only two an observer can prove.

The record also states its **canonical profile** explicitly — the product/foundation canonicalizer
of identity §3, **not** `opensip-metadata-canonical.1`, since it is neither signed security
metadata nor a journal record — and names the contrast at every join, because the journal
`body_sha256` it joins against *is* domain-framed. Proposed private DDL included and executed
(C14: monotone trigger, no delete, no identity change, no unknown phase).

### 1.3 The authorized settlement sweep

Specified in `commit-recovery-readonly.v3.md` §4 and verified by C14's proof matrix. Authorization
is the same `store-gc` owner; custody is fence plus non-blocking `EXCLUSIVE`, which is **what makes
proof possible** and why read-only recovery — holding neither — cannot produce it. It reads one
coherent snapshot, writes only `committed` or `refused`, at most one transition per attempt, and
writes **nothing** when the lease is busy, the ledger is unreadable, the ledger is one-sided, or
the row is already settled. It reuses no dead-attempt authority, obtains no grant and never retries
the commit. Permissible cleanup is the existing reachability GC of unreferenced orphans only. A
failed, latching or durability-uncertain attempt must never open another write transaction with its
stopped session; it releases and leaves the row `admitted` for the sweep.

### 1.4 chain_law, and two unsupported claims withdrawn

- The DDL now **refuses** `chain_law` 2 (`CHECK (chain_law = 1)`), verified by C13. It no longer
  advertises an alternative that is not implemented and that root is not requesting.
- **Withdrawn as false:** the claim that the pinned `prev_sha256` encoding was "the only consistent
  reading" because "both operands are TEXT". `seq` is an **INTEGER** column. The encoding choice is
  **prospective**, and that is now all it claims.
- **Withdrawn as unsupported:** the argument that a signing key inherently requires networking or
  breaks offline operation. It does not, and the stronger-authentication option table no longer
  says so.

## 2. Root's dispositions of my 11 items, applied

- **1/2/5/6 reclassified as selected limits, not gaps.** Retained-custody-only confirmation is
  selected; no stronger prefix authentication is proposed. The historical chain-head contradiction
  now has an explicit **current-owner disposition** patched into S1 (as a superseded-selector row)
  and S6: the v8 closed witness shape governs, the v1 sentence is retained historical prose and not
  a current claim, and no current owner asserts interior-prefix authentication. Old bytes preserved.
  The same limit is no longer listed as both an open gap and a selected non-gap.
- **4 settled, not deferred.** C12 establishes against the real schema that `StepTermination`
  requires only `class` and that `domainDetail` is **optional**, so a carrier quarantine publishes
  `operational-failed` / `LEDGER.CORRUPT` / `faultCause ledger-corrupt` with **no detail**. No
  registry member is minted; `MIGRATION.CORRUPT` is **not** misused. Negative controls confirm an
  unregistered code or a missing `faultCause` is refused.
- **8 selected as law.** No new delivery phase after a latch; state 3 keeps the commit committed
  with the RunId observable and reports through `DELIVERY.REQUIRED_FAILED`. The "owner choice not
  settled" wording is gone. C12 additionally demonstrates that **`policy-failed` (exit 1) and
  `indeterminate` (exit 3) survive publication** carrying `runId` and `reasonCodes`, and that
  `success` can carry neither an `errorCode` nor `reasonCodes` — so **no lawful reset to success
  exists** and an optional surface failure cannot manufacture one.
- **9 kept as explicit conservative diagnostic policy**, with the statement that the controls do not
  prove independent necessity, no correctness or cryptographic claim, and no manufactured attack.
- **10 and F00–F37 naming:** root owns the generator and integration; recorded, not treated as a
  blocker. F32's route and the sequential F38–F49 ids are preserved and asserted.
- **3 and 11** are completed above.

## 3. Deliverables

10 added files under `scratch/proposal/`, hashed in `scratch/output-manifest.json`. New this pass:
`docs/coop/design-corrections/security/carrier-migration.v1.md` and
`docs/v2/architecture/commit-recovery-readonly.v3.md`. Changed: the carrier DDL (`chain_law`),
`carrier-format.v3.md`, `attempt-custody.schema.v1.json` (rewritten) and
`carrier-fault-cases.v1.json` (F50–F53 added; F38–F49 unchanged).

Minimal patches, **two** candidate25 owner files and **two** planning inputs:

| File | Before → after | Δ |
|---|---|---|
| `identity-and-evidence.md` | `afded6d3…` → `a8ea1a52…` | +43/−1 |
| `security-and-lifecycle.md` | `12dcebea…` → `5c71be5c…` | +96/−0 |
| `commit-recovery-plan.v1.json` | `fffb820d…` → `44d321ca…` | +146/−2 |
| `implementation-boundaries-and-build-plan.md` | `b0fbe313…` → `01c3a95f…` | +33/−2 |

No historical or frozen-schema file is patched: `security-completion.v1.md`,
`security-completion.v8.md`, `grant-journal.sql`, both `journal-record.schema.json` files, both
`security_unit_lib` files and `security-lifecycle.schemas.v1.json` are all asserted still matching
the frozen manifest. Native-evidence schemas are untouched, so the seven reminted Runs on their
exact new digest are unaffected. **PS-01** lineage stays in `owner-correction.v3` — its binding
tuple and digest shape are consumed as inputs and no allocation is duplicated. **PS-04** untouched.

## 4. Executed scope

| Control | Result |
|---|---|
| C1 / C2 inherited and proposed carrier | 16 + 35 DDL probes, 0 failures |
| C6 schedule controls | 78653 schedules, 0 violations, 7/7 coverage |
| C7 PS05 gate | 132 schedules, 0 violations, all four states |
| C8 incompatibility inventory | 8 of 9 types admitted; exactly `SEAL` + 3 alias-only ids refused |
| C12 D9 projections | 39 passed, 0 failed |
| C13 migration prefixes | 41 passed, 0 failed |
| C14 settlement and sweep | 51 passed, 0 failed |
| C4b / C10 reference validation | 74 and 84 passed, 0 failed |
| C11 negative controls | 19 drifts, **17** detected |

**Two drifts remain undetected and are reported, not removed.** A2 (dropping the two-agreeing-tails
clause) and A8 (dropping the receipt-present-but-unsettled contradiction) both produce no violation.
The reason in each case is that the removed rule is **conservative policy, not correctness**: in a
lawful append the tail moves only with the witness, and a present receipt is itself the authority.
Both are retained as policy and labelled as such in the recovery document; root may drop either. I
also mis-constructed three drifts before arriving at these, and fixed them rather than counting
safe drifts as detections.

## 5. Remaining actual design gaps

Separate from §6 unperformed qualification and §7 selected limits.

1. **The authorized sweep is specified but unexecuted**; it has no DDL of its own and depends on
   storage's private ledger placement, which root is merging from another session.
2. **`AttemptCustodyV1` has proposed private DDL only.** If root's storage session prefers a
   different physical placement, the record shape and laws are what must survive, not the SQL.
3. **Split-brain after migration is detectable but not preventable** (F51). The mitigation is a
   release-ordering discipline, which is a process property this correction cannot enforce.
4. **The generated failure-matrix block** contains rows I produced in the generator's format; root's
   generator must be re-run at integration for byte consistency.
5. **Two conservative policies are unjustified by my controls** (§4), awaiting root's keep-or-drop.
6. **The `common.schema.json` / `evaluator3/common.schema.json` `RunId` split** (`run2` vs `run3`)
   is asserted in C12 as the retained-predecessor pattern rather than investigated. If the
   non-evaluator3 document is still a live projection owner anywhere, my projections would not
   validate against it.

## 6. Unperformed product qualification

No OS durability, `fsync`/`F_FULLFSYNC`, or real crash behaviour. No real SQLite crash or lock
contention. **No real concurrent processes: C6 interleaves a model, not two OS processes.** No
process control, so F42 has no feasible model. No Rust compiled or borrow-checked. No qualification
gate; all sixteen added fault cases are `not-executed`. Every database in every control is
`:memory:`.

## 7. Selected limits, with dispositions recorded

Not gaps. Retained-custody-only confirmation (`confirmed-under-retained-custody`, never
cryptographic proof, `unknown` rather than invalidation); no interior-prefix authentication under
any chain law, because the witness names the tail body digest; the historical chain-head wording
contradiction, disposed in S1/S6 with both documents' bytes preserved; prospective `chain_law` 1
with `chain-unverifiable` for historical generations; carrierFormat 1 TERMINAL closure enforced by
the admitted reader rather than a trigger; and the undetectability of a coherent whole-carrier
rewrite performed while no operation was running.
