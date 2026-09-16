# Bounded correction and integration consistency pass — author report (v6)

**Standing.** Actual Claude, same carrier author origin. Not an acceptance, readiness statement,
blind-consumer acceptance, final application acceptance or self-acceptance. Not product
implementation. Private design/reference work, not OS qualification. All v5 output is retained
immutable in `scratch/v5-evidence/`, with the nested v4 and v3 evidence inside it. Root's supplied
`ddl-atomicity.py`, `ddl-atomicity.json` and `root-F00-F37-proposed.json` are **unmodified** and
hashed in the manifest. Native schemas and PS-01 / PS-04 untouched. No new carrier architecture and
no new options.

## 1. Confirmed correction 1 — act B was never atomic, and root proved it

Accepted without qualification. Root's `ddl-atomicity.py` AST-extracted my v5 `act_B` unchanged,
injected one SQL error before the first trigger, and recorded
`tablesSurvivingFailure: ["carrier_format"]` with the transaction closed. The cause is exact:
`executescript` issues an implicit `COMMIT` first and then runs statements one at a time, so
`c.executescript(DDL3)` followed by `c.commit()` is **not** one transaction. My v5 C13 asserted
atomicity and never tested a failure inside it — the claim was unfalsifiable as written.

**Normative B stays atomic; the mechanism is now stated and the helper performs it.** Explicit
`BEGIN` on the same connection, every statement in order, `COMMIT`, and `ROLLBACK` on failure. A
bulk-script execution is now explicitly **not** an acceptable implementation of act B. Writing the
splitter surfaced a second defect of my own: my first trigger-boundary rule treated the `END;` of a
trigger *body clause* as the trigger terminator and truncated `gj3_append_laws`; it now tracks
`BEGIN`/`CASE`/`END` depth.

Added controls:

- **C13** mid-DDL failure: raises, **no** surviving object, no open transaction, recovery reports
  the prefix-A standing, and the retry then completes. Plus the success path and every legal
  durable prefix.
- **C13** malformed partial object set: `MIGRATION.CORRUPT`, refused rather than resumed. The
  partial check now runs *before* any read of the format row, because a malformed stub table
  previously crashed recovery — found by writing the probe.
- **C15** replays root's own extraction method against the corrected helper: `v5 ["carrier_format"]
  → v6 []`.
- **C11 A13** reintroduces the v5 bulk-script helper and is detected, with the diagnostic
  `table carrier_format already exists` — root's surviving-object defect, visible in the failure
  message.

All of this is **in-memory transaction evidence only**. It establishes nothing about `fsync`,
OS durability or real crashes.

## 2. Confirmed correction 2 — selected documents reconciled, not just companions

You were right that I patched companions and left the selected document contradicting them.

- **§8 detection** now keys on the published format **row**, with an explicit partial-object
  branch, matching `carrier-migration.v1.md` §3. The table-existence predicate is gone.
- **§9 reader staging** no longer claims a format-unaware core "refuses typed". It cannot: such a
  core never looks for `carrier_format`. The section now separates a **carrierFormat-aware** {1,2}
  core, which does refuse typed, from a **format-unaware** core, which is detectable-not-preventable
  — and labels that a **selected disclosed limitation** with release ordering as an implementation
  and release obligation, not an open architectural question.
- **Header and change set** now point at `commit-recovery-readonly.v3.md`, and a new
  selected-companion table names the stable normative path for each concern and states that v1 and
  v2 are superseded and must never be linked as current owners. Both older drafts remain only in
  the retained evidence trees; the v2 draft was moved out of the current proposal set in v5 and is
  not reintroduced.

## 3. Confirmed correction 3 — the receipt has no store binding

`foundation/identity-schemas.v3.json $defs/commit-receipt` is closed with exactly eight members:
`schemaVersion`, `runId`, `executionId`, `namespaceId`, `commitSequence`, `inventoryDigest`,
`sealedAssurance`, `signerKeyId`. **No `storeGenerationDigest`.** My `joins.toReceipt` implied one;
that is corrected with no member widening.

The corrected law: join the receipt on the members it actually has — `executionId` and
`namespaceId` by binary equality, and `runId`, `commitSequence`, `inventoryDigest` against the
association's copies. The store binding comes from the **admitted handle and registry** and is
carried by `CommitRecoveryAssociationV1.storeGenerationDigest`; a mismatch is caught at that
**owning** join and reported `binding-unusable`.

**C16** builds real instances of both records and validates them against their real schemas — no
`{x:1}`/`{y:1}` stand-ins. It asserts a receipt carrying `storeGenerationDigest` is refused, and
runs eight join cases including "wrong store generation for an otherwise perfect receipt", where
the receipt join succeeds and the binding join is the one that fails. Building it surfaced a third
version axis worth recording: the receipt's `schemaVersion` is **const 2**, distinct from the
association's `recordSchema` 1 and the journal's `recordSchema` 3.

## 4. Confirmed correction 4 — the identity §2 companion is now scoped

The v5 patch attached `AttemptCustodyV1` to the RequestId/ExecutionId reservation generically, which
would have pulled read-only requests and `--ephemeral` into persistent evidence writes. Corrected:

- The **uniqueness reservation is restated separately and unweakened**, applying to every RequestId
  and ExecutionId in every request mode, as the pre-use uniqueness rule only.
- The durable record is scoped to **durable-authoritative commit-capable attempts** using the
  evidence ledger — exactly those that can publish an authoritative receipt through the guarded
  facade.
- **Read-only requests and `--ephemeral` are explicitly excluded**: no persistent evidence-ledger
  write and no security operation reference. §5 owns `--ephemeral` as non-authoritative with
  temporary custody, minting no authoritative receipt, and that is cited rather than reinterpreted.

C10 asserts all four properties against the patched bytes.

## 5. Confirmed correction 5 — uncertainty stops the attempt

The v5 migration text read as though the same operation could re-read and then retry A or proceed
to B. Corrected to match the commit-path law it should always have mirrored: the uncertain
maintenance attempt **stops**, performs cleanup only, releases `EXCLUSIVE` then the fence, and
writes nothing further. Further progress requires a **separately admitted fresh maintenance
attempt** with its own `migrationOpRef`, re-acquiring fence and `EXCLUSIVE` before any write; it
resumes from the durable prefix, and a `TERMINAL` naming the previous attempt's ref is lawful
history to resume past rather than something to redo. `operationRef` attribution is preserved, the
footprint stays self-describing, and **no new durable or public intent is introduced**.

**`store-gc` is now stated as a SELECTED prospective expansion.** The inherited row establishes
only a negative — that `store-gc` is not intent-writing — not that this mutation was previously
authorized. The selection is written out explicitly, with what it does and does not change, in both
`carrier-migration.v1.md` §1 and the S9 patch. `store-status`'s existing `migration-state` field is
reused; no surface is added.

## 6. Root dispositions applied

- **Two-tail clause**: selected conservative diagnostic policy. "Root may drop it" is removed from
  the selected law; the honest non-necessity evidence (C11 A2) is retained as the stated reason it
  is conservatism rather than necessity. No stronger cryptographic prefix mechanism anywhere.
- **Receipt-present + `admitted` contradiction: dropped.** It is a **lawful interval** under the
  receipt-before-settle order, and §4.2's own committed-but-unsettled sweep case presupposes it. A
  valid joined receipt establishes historical commitment and continues the carrier capture;
  `pendingSettlement` is disclosed operationally; no authority is revived and **no writer may
  reopen a stopped session merely to settle it**. Corrected together in C6, C14, the recovery
  document §2.1, the attempt-custody record, and the stale phase-only **E3** owner-patch wording,
  which had said a settled phase alone establishes no commitment — contradicting the
  settled+refused law. The composed **commit → reader → later sweep** positive case is now executed
  in C14, and C6 gained a coverage assertion that the interval is actually exercised. Effect: C6's
  77 spurious `unknown-custody` results became `committed-historically`.
- **DDL placement: selected** storage-owned evidence ledger inside the inventoried
  `crates/storage/src/ledger_store.rs`, `commit.rs`, `recovery.rs`. The sweep uses that same ledger
  and table; no separate DDL. Unexecuted SQLite/process/OS behaviour is product qualification, and
  C14 is reference execution, not sweep qualification — both stated in the record and the manifest.
- **Old-core limitation**: selected and disclosed, release ordering an implementation obligation,
  and no longer listed as an unresolved gap.
- **Output schema owner**: explicit, not inferred. C12 asserts `workflows-and-surfaces.md` line 33
  ("Its closed schemas live under `workflows/schemas/evaluator3/`"), the incorporated
  `workflow-projection-contract.v3.md` line 7, and line 38 ("Historical output schemas remain
  retained evidence and are not an alternative parser for this profile"). Recovery §1 prose now
  names `evaluator3/common.schema.json` as the owner. **The alleged run2-vs-run3 gap is withdrawn.**
- **F38–F53 identities and meanings preserved; F32's typed route preserved and asserted.** Root
  owns the generated matrix.

## 7. Awareness comments on `root-F00-F37-proposed.json`

In `scratch/comments-on-root-F00-F37-proposed.md`; root's file is not touched. The proposal closes
the `indeterminate` overload I had carried as a gap. Three consistency observations, none a change
request: `snapshot-dependent` (F29) has no projection row in my §1 table, so it needs either a row
or a decomposition; F36's `unknown-attempt-open` is a pre-sweep standing that could read as
permanent when the sweep will later settle it `refused`; and F14 is correct as `committed` but does
not mention the `pendingSettlement` disclosure.

## 8. Remaining REAL architecture contradictions

**None found in this pass.** Every item I previously listed under "remaining gaps" is now either
corrected above, a selected limitation (§9), or product qualification (§10). The three open items
are *root's to settle*, not contradictions: the `snapshot-dependent` projection row, and the two
optional clarifications in §7.

One item I want to name precisely rather than bury: the two-agreeing-tails clause is selected
policy whose necessity my controls **cannot** demonstrate (C11 A2 remains undetected by design).
That is a known limit of the evidence, not a contradiction.

## 9. Selected limitations, with dispositions recorded

Retained-custody-only confirmation (`confirmed-under-retained-custody`, never cryptographic proof,
`unknown` rather than invalidation); no interior-prefix authentication under any chain law, because
the witness names the tail body digest; the historical chain-head wording contradiction, disposed in
S1/S6 with both documents' bytes preserved; prospective `chain_law` 1 with `chain-unverifiable` for
historical generations; carrierFormat 1 TERMINAL closure enforced by the admitted reader;
format-unaware old-core split-brain detectable but not preventable, mitigated by release ordering;
and the two-agreeing-tails conservative diagnostic policy.

## 10. Unperformed product qualification

No OS durability, `fsync`/`F_FULLFSYNC`, or real crash behaviour. No real SQLite crashes or lock
contention. No real concurrent processes — C6 interleaves a model. No process control, so F42 has no
feasible model. No Rust compiled or borrow-checked. No qualification gate; **all sixteen** added
fault cases F38–F53 are `not-executed`. The settlement sweep is specified and its decision matrix is
reference-executed; its execution remains qualification. Every database in every control is
`:memory:`.

Two stale v5 metadata claims are corrected in the manifest's `standingCorrections`: it said twelve
additions (correct: sixteen, F38–F53) and listed the sweep as an unspecified remaining obligation.
