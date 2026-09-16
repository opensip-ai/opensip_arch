# Bounded carrier correction, pass 4 — coauthor report

**Standing.** Non-blind actual Claude coauthor output. Not an acceptance, not a readiness
statement, not a blind-consumer acceptance, not a final application acceptance, not a
self-acceptance, and not product implementation. Root assesses, merges with the separately
authored PS01 and PS04 work, runs the integrated suites, and obtains fresh independent review on
the merged frozen successor.

**Bindings.** Root's latest planning inputs at the runtime root:
`commit-recovery-plan.v1.json` `fffb820d…` (25639 B) and
`implementation-boundaries-and-build-plan.md` `b0fbe313…` (82112 B). Frozen Source25 manifest
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` re-verified, and the v3
four-file input manifest re-verified. C10 asserts the before-bytes of both patched candidate25
owner files match the frozen manifest, and that all eight historical or frozen-schema members
still match it. All v3 output is retained unchanged in `scratch/v3-evidence/`, including the
superseded recovery draft and the pre-renumbering case bytes.

## 1. The two schedules root supplied — both were real defects in my v1 algorithm

I accept both. v1 read the tail, witness and floor once each and treated the tuple as coherent. It
is not, and root's diagnosis of each consequence was exact.

**Race 1 — false corruption from independently timed reads.** With a receipt at `k=9`, a tail
read of `t=10`, and a lawful concurrent `APPEND-WRITE` completing append 11 and witness
`COMMITTED 11` before the reader reads the witness, v1's tuple is `(t=10, W=COMMITTED 11, H<=10)`.
`k > t` is false so the reopen never fires, and v1's witness classification lands on
`COMMITTED n > tail`, producing `unknown-quarantine-condition` for an entirely ordinary later
append. The floor variant is the same shape: `H` advancing after the journal snapshot yields
`H.lastSeq > t` and a false rollback diagnosis.

**Fix: bracketed capture plus a conservative attribution rule.** Each capture takes
witness-before, floor-before, journal snapshot, witness-after, floor-after, and computes byte
stability of each bracket. An anchor is usable only if its own bracket was stable. An owner
quarantine condition is reportable **only** when all five conditions in
`commit-recovery-readonly.v2.md` §4 hold — stable witness bracket, stable floor bracket, two
journal snapshots agreeing on tail sequence *and* tail digest, the closed witness shape validated
before any comparison, and matching carrier naming. Otherwise the mismatch is attributed to
temporal skew and reported `unavailable-busy`. **Read-only never invents a corruption diagnosis
from independently timed observations.** No writer wait, no append-lock, no mutation, no
high-water raise, no witness repair; bounded to one ledger snapshot, at most two journal
snapshots, at most four witness and four floor reads.

I state the stability argument as an **assumption, not a proof**: byte-identical brackets imply
coherence only because the append protocol never lowers the witness sequence or returns to
`PENDING` at the same sequence within an attempt, and `REVERT`/`ADVANCE` need an authorized
lifecycle open holding the fence. If a future writer breaks that monotonicity, the reasoning fails
and the protocol must be revisited.

**Race 2 — false terminal conclusion from a stale snapshot.** v1 checked liveness after the ledger
snapshot, so a writer that committed and exited in between produced a permanent
"uncommitted" answer. Root is right that absence from an in-memory active set is not terminal
proof.

**Fix: a coherent ledger-owned attempt phase, and no liveness probe at all.** I traced the
existing owners first. Identity §2 **already** requires that RequestId and ExecutionId are
"reserved with uniqueness checked in the corresponding operational ledger before use", so the
durable reservation — the admitted phase — is already law. What is genuinely missing is any
durable record that a particular ExecutionId reached a terminal state when it did **not** commit:
the `executionId ↔ operationRef` map is private host state whose only durable home is the
association row, which exists only on success, and identity §6 speaks only of inspecting a
committed receipt. So the minimal contract adds a monotone phase to the *existing* reservation
rather than a second record: `AttemptCustodyV1 {phase: admitted|settled, settledOutcome,
operationRef}`, with the settle write ordered **after** the receipt write, read in the **same**
snapshot as the receipt. `settled` with no receipt is the failed answer; `admitted` is
`unknown-attempt-open`; no row is `unknown-attempt-unobserved`. It authorizes nothing, so the
settled-ExecutionId-is-terminal law is preserved. The in-memory active set is removed from the
algorithm entirely.

**The crash case stays unknown, deliberately.** A writer that dies before settling leaves
`admitted` forever and recovery reports `unknown-attempt-open` indefinitely. Settling it needs an
**authorized sweep** that may take the fence and the S7 lease census. That is not read-only work,
it is **not specified here**, and it is listed as an undischarged obligation. Unknown remains
unknown until actual absence is established.

**Both races are now covered by schedule controls, not fixed tuples.** `c6-schedules.py` runs the
reader as a coroutine yielding after every observation and releases a lawful writer's steps into
those yield slots, enumerating every monotone assignment: **78653 schedules over 14
configurations, 0 violations**, with **7/7 coverage assertions** holding — including that witness
instability and floor instability actually occurred, that skew actually suppressed a corruption
claim, that confirmation on the single retry actually happened, and that all five quiescent
genuinely-corrupt carriers are **still** diagnosable, so the stability gate did not silently
disable the diagnosis.

## 2. Owner patches against candidate25

Root is right that v3 supplied companions without selecting them. Two candidate25 owner files are
patched, and no historical file is:

| Owner file | Change | Before → after |
|---|---|---|
| `identity-and-evidence.md` | §2 attempt-custody phase on the existing reservation; §5 read-only recovery selectors and the narrow assurance limit; §6 the absent-receipt case | `afded6d3…` → `911fa151…`, +35/−1 |
| `security-and-lifecycle.md` | S1 selects carrierFormat 3; S6 the PS05 gate, the `REV`-after-`SEAL` reader rule and the delivery phase; S9 the carrier reader bridge and the third generation-closure cause; S12 three projection rows | `12dcebea…` → `e2ae8e6b…`, +54/−0 |

Deliberately **not** touched: `security-completion.v1.md`, `security-completion.v8.md`,
`grant-journal.sql`, both `journal-record.schema.json` files, both `security_unit_lib` files, and
`security-lifecycle.schemas.v1.json` — all asserted still matching the frozen manifest. `WA-13`
occurs **only** in the immutable historical v8, so the third generation-closure cause is stated in
the current owner (S9) and the historical text is left exactly as it is.

Planning patches: `commit-recovery-plan.v1.json` +110/−2 (cases **F38–F49**, sequential, no
`F39b`), `implementation-boundaries-and-build-plan.md` +29/−2. All 38 inherited cases are asserted
byte-identical, and **root's F32 typed-route fix is asserted preserved verbatim**, including its
move to `crates/host/tests/retention_tests.rs`.

**D9 namespaces pinned exactly, nothing minted.** The three new S12 rows use only existing
`errorCodes` (`LEDGER.BUSY_TIMEOUT`, `LEDGER.CORRUPT`, `EXTENSION.ADMISSION_REJECTED`) and only
existing `DomainDetailCode` members (`PROJECT.BUSY`, `RECOVERY.REFUSED`). The internal standings
are spelled so they cannot be read as a D9 class — in particular none is spelled
`indeterminate`, which is the public class at exit 3. **One decision is left open rather than
minted:** a journal-carrier quarantine has no fitting member in the closed 191-member detail
registry, and reusing `MIGRATION.CORRUPT` would put two remedies behind one code, which the D9
contract itself calls a defect. Both options are costed in the recovery document §1.1; the choice
is the owner's.

## 3. PS05 gate, and the delivery question

I adopted root's PS05 wording rather than my older tri-state sketch: one atomic bit state,
`ADMITTED=1`, `LATCHED=2`, states 0–3, compare-exchange `0→1`, observer always fetch-ORs `2`
including `1→3`, no resets, one single-use permit, state 3 records the latch without revoking or
relabelling the admitted attempt. Executed: **132 schedules, 0 violations**, all four states
observed, permit single-use, fetch-OR idempotent and never clearing `ADMITTED`, CAS from state 2
fails.

**Can a successful commit returning a stopped cleanup-only session still complete required
rendering/delivery? Yes, as a separate phase, and it needs no authority from that session.**
Required delivery is a read-and-materialise activity, which S7 places in `SHARED-READ` alongside
queries and rendering; it is not a brokered effect, so it draws nothing from the closed session
and the closed session grants nothing. The explicit handoff is: commit confirmed → stopped session
returned → cleanup `REV`/`CLN` through a fresh lawful L3→L4 append while that session still holds
the operation lease → release the lease → S7 end handoff → **then** a new `SHARED-READ` phase over
the committed snapshot. A latched attempt (state 2 or 3) starts no delivery phase and cannot
reacquire authority that way; a new effect needs a fresh attempt with a fresh ExecutionId.

**For state 3 I selected the conservative reading and flagged the alternative.** No delivery phase
is started; the commit stays committed with its RunId observable and the required delivery is
reported through the existing `DELIVERY.REQUIRED_FAILED` / operational-failed / exit 4 path. S6
cancellation "refuse[s] further requests", which is why. An owner could instead permit delivery
for state 3 on the reading that disclosing an already committed Run is an obligation rather than a
new effect. That is recorded, not settled.

## 4. Corrections root asked for, and one I had to make to myself

- **Overclaim withdrawn.** My v3 text said the current journal "cannot be written to any inherited
  physical carrier at all". C8 measured it: the frozen carrier admits **8 of the 9** schema-3
  operational record types, and the incompatible cases are exactly `SEAL` plus the three
  alias-only machine platform ids on a `GRANT` (`macos-x86_64` is admitted, being its own alias).
  §2.1 of the carrier document now says that.
- **Attribution separated.** The weak-chain / tail-body limitation was already in root's original
  prompt and the followup §4.2; my control adds the *measurement*, not the limitation. The
  distinct new finding is a **wording contradiction between two frozen documents**: carrierFormat
  1 §5.4 says "the chain head is in the witness" and the v8 closed witness shape has no chain-head
  member. §11 now states that separation explicitly.
- **TERMINAL segregation** kept as the reviewable mechanism: one CHECK makes `record_schema 3`
  exclude `TERMINAL` and `TERMINAL` always the frozen recordSchema-1 body.
- **No `runId` on `REV`.** Not selected; the private association plus the
  `executionId ↔ operationRef` mapping plus the reader rule suffice, and no case in C6 or C7
  needed more.
- **PS01 and PS04 not duplicated.** Both named as dependencies and nothing more; C10 asserts no
  `storeInstanceId` allocation or lineage law and no report-asset or closure-kind requirement is
  authored here.

## 5. Executed scope

Reference environment: CPython 3.12.13, SQLite 3.50.4, jsonschema 4.25.1, invoked as a `python3`
subprocess. Every SQLite database is `:memory:`.

| Control | Result |
|---|---|
| C1 inherited carrier laws | 16 DDL probes, 14/14 witness-reconciliation rows reproduced |
| C2 proposed carrier | 35 DDL probes, migration m1–m12, dispatch on 5 databases |
| C6 schedule controls | 78653 schedules, 0 violations, 7/7 coverage assertions |
| C7 PS05 gate | 132 schedules, 0 violations, all four states |
| C8 incompatibility inventory | exact two-case incompatibility measured |
| C9 patches | 2 owner + 2 planning, F32 preserved |
| C4b carrier validation | 74 passed, 0 failed |
| C10 v4 validation | 84 passed, 0 failed |
| C11 negative controls | 14 drifts, 13 detected |

**The negative controls found real weaknesses again, and I am reporting them rather than hiding
them.** Two model drifts I wrote initially failed to detect anything because the drift itself was
badly constructed; two artifact drifts "detected" only by crashing my validator instead of failing
a check. Both classes are fixed: the validator now fails cleanly, and the sandboxes carry the model
reports the validator reads. **One drift remains undetected and is reported as such:** A2, which
keeps the stability brackets but drops the two-agreeing-tails requirement, produces no violation.
The reason is that in a lawful append the tail only moves together with the witness, so any
schedule moving the tail between captures also moves the witness and the second capture lands on a
usable anchor rather than an adverse one. **These controls therefore do not show the
two-agreeing-tails clause to be independently load-bearing.** I retained it as defence in depth
against a path that moves the tail without moving the witness, which the current protocol does not
contain. Root may drop it; my controls do not justify keeping it.

## 6. Remaining actual design gaps

Separate from unperformed qualification (§7) and from already-selected honest limits (§8).

1. **The witness authenticates no interior prefix**, under either chain law. Real, unfixed;
   fixing needs a new `witnessSchema` carrying a chain head **and** a recursive chain, which
   touches a frozen security boundary. Four options costed in the carrier document §11; none
   adopted.
2. **Two frozen documents contradict each other** about where the chain head lives. Needs an owner
   disposition; both documents are immutable so neither can be edited.
3. **The authorized settle-sweep is unspecified.** Without it, a crashed attempt stays
   `unknown-attempt-open` forever. Named, not discharged.
4. **The carrier-quarantine public detail code is undecided** (§2). Two costed options.
5. **`prev_sha256` byte encoding is unpinned in the inherited corpus** — one DDL comment, zero
   call sites, zero fixtures. Pinned prospectively for carrierFormat 3 only; historical
   verification can only report `chain-unverifiable`.
6. **carrierFormat 1 cannot physically enforce TERMINAL closure** (no trigger). Handled by a
   reader rule; a stronger fix would require touching an immutable carrier.
7. **`indeterminate` remains overloaded in F00–F37**, which I deliberately did not touch. Root
   should decide whether to rename there.
8. **The state-3 delivery reading is a selection, not a settled law** (§3).
9. **The two-agreeing-tails clause is unjustified by my controls** (§5).
10. **The generated matrix block** contains rows I produced in the generator's format; the
    project's own generator must be re-run at integration for byte consistency.
11. **`AttemptCustodyV1` has no DDL here.** The private association table and its accessor are
    storage-owned and root is merging separate sessions in that area, so I specified the record
    and its laws but authored no SQL for it.

## 7. Unperformed product qualification

No OS durability, `fsync`/`F_FULLFSYNC`, or real crash behaviour. No real SQLite crash or lock
contention. **No real concurrent processes: C6 interleaves a model, not two OS processes.** No
process isolation or process control, so F42 has no feasible model here. No Rust compiled or
borrow-checked — the ownership reasoning about E0505/E0451 is an argument about root's design, not
a compiler result. No qualification gate; all twelve added fault cases are `not-executed`.

## 8. Already-selected honest limits

The custody-only anchor boundary (`confirmed-under-retained-custody`, never cryptographic proof,
`unknown` rather than invalidation); the undetectability of a coherent whole-carrier rewrite
performed while no operation was running; and the absence of any interior-prefix authentication.
These are selected positions, not open gaps.
