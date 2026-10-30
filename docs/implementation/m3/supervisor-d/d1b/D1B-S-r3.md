# D1B-S r3: SD-5b's `confinement-refused` row (J1 item 10 row 60), by value (D1b author, 2026-10-30)

**Status: PROPOSED.** Under R3 different-vendor review (`REQUEST-r3.md`, Codex gpt-6-astra/high, codex-l5-r3). It takes
effect only when the coordinator records its adoption, owner-delegated under OD-AUTO-1 (LD-Q-35), in a separate
adoption receipt that pins this file's sha256. This file is never edited after review; a revision is a new file.

**r3 answers R3 review r2** (`REVIEW-r2.md`, `D1B-S: REQUIRED-FINDINGS`; r2 is kept unchanged as `D1B-S-r2.md`):
- **D1BS-R2-RF-1:** row 60 now follows LD-D1B-A **r2** (`LD-D1B-A-r2.md`), which withdraws r1's exec witness and keeps
  F-1's success row: `A` then EOF continues. Row 60's domain is the completed refusal statuses and the one pending state
  reaching item 14's bound (whatever was read); the exec-event rows are removed; observation-source failures are named
  in their host-I/O route (§2.3).
- **D1BS-R2-RF-2:** fd 5's `EPIPE` is excluded from the terminal channel failures and deferred to fd 6 (§2.3), with
  controls and a mutation (§5.1, §6).

**r2 answered R3 review r1** (`REVIEW-r1.md`, `D1B-S: REQUIRED-FINDINGS`; r1 is kept unchanged as `D1B-S-r1.md`):
- **D1BS-R1-RF-1:** row 60 now states what the host observed (the confined launch could not be established under the
  adopted classifier), and claims "before the target ran" only for the statuses that establish it. The status-to-step
  table is conditional on the refusal classification, and the non-refusal statuses are excluded by name (§2.1, §2.3).
  It followed LD-D1B-A r1, since replaced by r2 (above). **Adoption of this
  text requires LD-D1B-A's adoption first; if LD-D1B-A changes the refusal domain or the step mapping, this row is
  reconciled before adoption.**
- **D1BS-R1-RF-2:** §5 separates what D1b-3 establishes (the projection, J-C20) from the envelope composition and
  remedy, which stay owed by the envelope owners (J3d, J2c) with named negative controls (§5.2).
- **D1BS-R1-NBO-1:** §5.1 adds the interruption-precedence control.

**What it amends, by value (no accepted bytes are edited):**
- **M3-D r5**, `opensip_arch/docs/implementation/m3/supervisor-d/PROPOSAL.md` (sha256 `36c26161…44db0`; equal to
  `PROPOSAL-r5.md`, `224b9228…6d`, plus its acceptance note): item 22's `confinement-refused` row, and item 29's SD-5b
  row for this one refusal.
- **J law r7**, `opensip_arch/docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (sha256 `5d03aaca…40a0`): item 10's
  outcome matrix (a new row 60), and the SD-5b sentences at :50, :837 and :916 for this one refusal.

**Why now.** J law :50 and :916 place each SD-5b refusal "with its first consumer … `confinement-refused` with D1b, and
only if O7 is decided as recommended. Each adds one item 10 row and one J-C20 test in its consuming unit." O7 was
adopted as recommended on 2026-10-09 (`O7-OWNER-DECISION-2026-10-09.json`). D1b (plan r1, `../plan/PLAN-r1.md`) is the
consuming unit; its sub-unit D1b-3 writes the product row and waits only on this text.

**What is already fixed, and not reopened here.** M3-D item 22: `confinement-refused` (observer: the launcher) routes
to `operational-failed` 4, `HOST.IO_FAILURE`, faultCause `host-io`; "its detail and J1 row are SD-5b's". F-4: the
settlement arises only when availability probed positive and an apply step then failed (F-1's status table). D adds no
public code (item 22; MJ item 10).

## 1. The questions SD-5b leaves open, and the answers

| Question | Answer |
|---|---|
| **Q1. The detail** (SD-5 LD-S3's existing-code test) | `DELIVERY.CLOSURE_UNSPAWNABLE`, with subject `confinement-refused:<step>` (§2) |
| **Q2. The remedy** | WS:1375's, unchanged: `opensip doctor` |
| **Q3. Is a contract (NE or WS) row also owed?** (item 29: "Whether a contract row is also owed, as SD-5 found for `ExcludedForm`, is SD-5b's question") | **No.** The route and detail are WS:1375's existing contract route ("installed closure … unspawnable", `operational-failed` 4, `HOST.IO_FAILURE`, `DELIVERY.CLOSURE_UNSPAWNABLE` → `opensip doctor`), used with that meaning (§3). No WS, NE, SL, schema, registry or D9 byte changes |
| **Q4. Reachability** | Under O7 only, and only on a platform with a CF-1 measured row. Until CF-1 supplies one, D1b's table is empty and every launch is `unavailable` (disclosed), so row 60 is **not reachable** in production; it is recorded like row 53 |

## 2. The new text

### 2.1 J law item 10: row 60 (new)

| # | Observation | Class / exit | Code / faultCause | Detail | runId | Basis |
|---|---|---|---|---|---|---|
| 60 | **(D1B-S; SD-5b, O7)** Confinement refused: availability probed positive (F-4: a CF-1 measured row **and** the probe), and the launch phase did not establish the required confined launch under the adopted classifier (M3-D F-1; LD-D1B-A r2): a launcher failure code before `A`, nothing then EOF, a completed sequence outside the classifier's table, or item 14's handshake deadline reached before fd 6's EOF, whatever was read. For a failure code before `A` and for nothing then EOF (F-1's own rows) the target did not run; for the others the required launch was not established, and the host refuses rather than continuing. Never a provider fault and never an unconfined fallback. Not reachable until CF-1 supplies a measured row (D1b LD-D1B-4) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `DELIVERY.CLOSURE_UNSPAWNABLE`, subject `confinement-refused:<step>` (§2.3); remedy as row 28's (WS:1375, `opensip doctor`); the settlement key goes to the operational record | none | M3-D item 22, F-1, F-4; WS:1375 |

### 2.3 The step, given the refusal classification, and what is not row 60

Only a launch phase that LD-D1B-A classifies `confinement-refused` reaches row 60. Its `<step>`:

| Observed (fd 6 to EOF, unless stated) | `<step>` | Did the target run? |
|---|---|---|
| `r` / `n` / `d` / `c` / `u` / `p` / `k` alone | `record` / `noncanonical` / `descriptors` / `core-limit` / `symbol` / `apply` / `check` | no (F-1: failed before the profile applied) |
| nothing | `no-status` | no (F-1: the launcher died before `A`) |
| a completed sequence that is none of F-1's rows with LD-D1B-A's codes (for example `AA`, `Ap`, `pA`, three or more bytes) | `malformed` | not established |
| item 14's handshake deadline reached before fd 6's EOF, whatever was read (nothing, `A`, a code, a malformed prefix) | `unsettled` | not established |

**Not row 60**, by the same classifier (LD-D1B-A r2):
- `A` then EOF: supervision continues (F-1's row); a later exit is item 13's `unexpected-exit`, as for any provider.
- `Ae`, `Aa`, `Af` then EOF: `spawn-failed`, row 28's `DELIVERY.CLOSURE_UNSPAWNABLE`, with its own subject, never
  `confinement-refused:`.
- `Ax` then EOF: `spawn-failed`, item 22's host-I/O route.
- A **terminal** observation-source failure: a read error on fd 6, or a write error on fd 5 **other than `EPIPE`**
  (`EAGAIN` and `EINTR` are retried): `host-fault`, item 22's host-I/O route.
- **`EPIPE` on fd 5 is not a terminal failure (RF-2).** The host stops writing and fd 6 decides under the same bound, so
  `EPIPE` then `r` then EOF is `confinement-refused:record`; `EPIPE` then the bound is `confinement-refused:unsettled`.
  `EPIPE` alone is never taken as the launcher's death.
- A first cause that already won (user cancellation, revocation, observer fail-stop) keeps its own route.

The detail row 60 shares with row 28 does not merge their causes or subjects.

The subject is at most 32 characters, inside `BoundedText`. One refusal per settlement, so no choice among several is
needed (contrast SD-5 LD-S4).

### 2.2 Superseded sentences (for `confinement-refused` only; the other three SD-5b refusals stay owed)
1. **M3-D item 22, the `confinement-refused` row's route cell**, "its detail and J1 row are SD-5b's (r4)", is replaced
   by: "detail `DELIVERY.CLOSURE_UNSPAWNABLE`, subject `confinement-refused:<step>`; J1 row 60 (D1B-S)".
2. **M3-D item 29, the SD-5b row:** `confinement-refused` is removed from "**Not written.**"; the row reads "written for
   `confinement-refused` by D1B-S (J1 row 60)" for that member.
3. **J law :50, :916 ("Still owed, as SD-5b: …")** and **:837 ("SD-5b's refusals have no row yet")**: `confinement-refused`
   is removed from the owed list and cited as row 60. `MemoryBudgetBelowCeiling`, `ToolOutputBound` and
   `ToolScratchBound` stay owed, each with its own first consumer, unchanged.
4. **J law item 13's S20 row** records row 60 as met for `confinement-refused`.

## 3. Why this detail (SD-5 LD-S3's existing-code test)

- **A registered detail is owed.** A `kind=failure` envelope needs a nonempty `errors` array (WS:1340-1344). MD item 22
  and MJ item 10 forbid a new public code.
- **`DELIVERY.CLOSURE_UNSPAWNABLE` is true here.** Under O7 the launch law (M3-D F-1, F-4) makes the confined launch the
  only lawful way to start a provider on a platform whose availability probed positive: "Available but an apply step
  fails means refuse the launch", never run unconfined. The provider closure therefore cannot be spawned on this host
  in the form its law requires, which is what "unspawnable" says. It is also the same owner, class, code and fault as
  item 22's `spawn-failed` row and J1 row 28, so the route table stays one route.
- **The remedy is true.** `opensip doctor` is the right next step for a host whose platform probe passed but whose
  apply then failed, which F-4 calls "an unknown state". It does not tell the user to reinstall or to disable
  anything (there is no switch, F-4).
- **The subject separates it.** `confinement-refused:` distinguishes it from row 28's spawn errors in the envelope and
  the operational record, as SD-5's subject prefix did (LD-S5); the product selects nothing new by it.

**Rejected:**
- **`DELIVERY.CLOSURE_BYTES_CORRUPT`.** The bytes were not observed to differ; its remedy implies repair of the bytes.
- **Detail absent (row 23's shape).** The envelope still needs a detail, and the two surfaces would differ (SD-5
  LD-S3's own rejection).
- **`PROVIDER.PROTOCOL_VIOLATION`.** Item 22 forbids routing a refusal the provider never spoke as a provider fault.
- **`OBSERVER.FAIL_STOP` or `HOST.INVARIANT_VIOLATED`.** The first is the trust observer's (X4:121); the second asserts
  a host bug, but a platform apply failure is not one.
- **A dedicated code** (for example `CONFINEMENT.REFUSED`). Forbidden by MD item 22 and MJ item 10; new public codes
  are the owner's.
- **A new NE §10 row (SD-5 LD-S1's form).** SD-5 needed one because no contract table routed an `ExcludedForm`. Here
  WS:1375 already routes "unspawnable" to exactly this class, code, detail and remedy, so a second statement would be a
  second copy that can drift (SD-5 LD-S1's own "both NE and WS" rejection).

## 4. Consequences, stated
- **The public surface:** one more observation reaches an existing route; no code, detail, remedy, schema or golden
  changes. WS:1375's golden keeps its meaning and gains a second cause with a distinguishing subject.
- **The product (D1b-3):** `outcomes.rs` gains one observation variant `ConfinementRefused { step }` projected to
  `Termination::failed(Code::HostIoFailure, Fault::HostIo, Some(Detail::DeliveryClosureUnspawnable))` with the subject,
  in the exhaustive match; the comment near :420 drops `confinement-refused` from SD-5b's unwritten list.
  `supervisor_records.rs`' `OwnerRoute::ConfinementRefused` (D1b-2) joins it.
- **Not reachable before CF-1:** the row is law now; its first production occurrence needs a CF-1 measured row.
- **O7 record:** unchanged by this text (`d1bImplemented` moves only when the coordinator records D1b's integration).

## 5. Controls

### 5.1 What D1b-3 establishes (the projection; J-C20)
- **Row 60's projection:** each of the ten `<step>` values projects to exactly class 4, `HOST.IO_FAILURE`, `host-io`,
  `DELIVERY.CLOSURE_UNSPAWNABLE`, subject `confinement-refused:<step>`, no runId, and **the same remedy field row 28's
  projection carries** (the projection selects no remedy of its own: `outcomes.rs` leaves remedy selection to the
  envelope owners except where a bound successor selects one). The existing field-by-field table is extended.
- **Route join:** `Cause::ConfinementRefused` → `OwnerRoute::ConfinementRefused` → row 60, never `ProviderProtocol`
  (a `supervisor_records` test over every cause).
- **Interruption precedence (NBO-1):** a `confinement-refused` settlement that is also `userInterrupted` before
  FinalGate routes `Interrupted` (130) through `settlement_route`, not row 60.
- **Classifier boundary (r2 RF-1, r3):** every non-refusal case in §2.3's "Not row 60" list yields no
  `confinement-refused:` subject; each refusal status yields exactly its step (D1b-2's classifier test over the whole
  table), including the bound reached with nothing, with `A`, and with a malformed prefix read.
- **`EPIPE` (r3 RF-2):** fd 5 `EPIPE` then `r` then EOF yields `confinement-refused:record`; a non-`EPIPE` write error on
  fd 5 and a read error on fd 6 yield `host-fault`, never row 60.
- **Totality:** the projection's match has no wildcard arm (item 10), so a missing row fails to compile.

### 5.2 What stays owed by the envelope owners (RF-2)
D1b-3 does **not** establish the failure envelope. WS:1340-1344's composition (a nonempty `errors` equal to the
termination's `domainDetail`) and the remedy text are J3d's and J2c's (`outcomes.rs`: "the envelope's `errors`
composition … and every remedy but the two successor-selected ones below are the envelope's (J3d, J2c)"). **Owed with
that owner, at its gate:** for row 60, the real composition path's full `DomainDetail` (code, subject, remedy) equals the
singleton `errors` value; no Run envelope is fabricated; and two negative controls: a wrong remedy, and an empty or
mismatched `errors`, each failing. No test-only reconstruction or the schema helper's placeholder remedy counts as that
evidence. D1b reports row 60's public surface as **projected, not composed** until then.

## 6. Mutations (D1b-3, on its frozen commit)
`detail-bytes-corrupt` (row 60 projects `DELIVERY.CLOSURE_BYTES_CORRUPT`), `fault-provider-protocol`,
`route-as-provider` (cause routed to `ProviderProtocol`), `subject-dropped`, `step-swapped` (`apply`↔`check`),
`exit-3`, `accepted-as-malformed` (the classifier refuses `A` then EOF), `interrupt-precedence-lost` (the refusal
outranks `userInterrupted`), `epipe-as-host-fault` (every fd 5 write error routed to `host-fault`), `pending-a-continues`
(the bound reached with `A` read settles `handshake-deadline`). Each must fail a §5.1 control. The envelope mutations are §5.2's owner's.

## 7. Questions for the reviewer
1. Does §2.1–§2.3 now match LD-D1B-A r2 exactly, including the `EPIPE` exception (r2 RF-1, RF-2)?
