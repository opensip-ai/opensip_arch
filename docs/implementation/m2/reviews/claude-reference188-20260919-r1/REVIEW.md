# Independent review — frozen `immutable-carrier-reference-checkpoint-188`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 188 reference bytes — the `cf_no_replace` carrier guard and eight-object dispatch, the immutable-ledger mutation law, and the Phase A active-transition binding (my 186 `NOTES-W2` correction, adopted by the owner). My inventory, notes and proposals were assistance, not acceptance. The 189 product draft is outside this review and was not inspected. No production, host-qualification, custody or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `7a02a5831ea1bb2e5bb6819117cc49b91e24dfb3a4a30682482034430638c5ab`, 2,301,224 B = request = `archive-pin.json` |
| Members | 1,485, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,299/1,299; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 186 extraction** (1,298); 24 modified + 1 added (`ledger-mutation-immutability.v1.md`) = 25 |
| Python | 91: 86 byte-identical to 186, 5 changed, 0 new. `transition-journal-cases.v1.json` and the inherited format-1/2 DDL byte-identical |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs: **all seven lanes exit 0** — from my own run: integration 1,646 checks / 0 failed; carrier 479 passed / 0 failed. The two focused modules alone through the host-model loader: 1,220 checks, 0 failed. No bytecode left.

## 3. Phase A binding — what I checked and found

As read: for changed-store journals only, after the fence check and **before** registry, leases and footprint, the model requires `activeTransitionBinding` (closed private `ActiveTransitionBindingV1`: `executionId`, `journalRef`), schema-validates it, and requires `journalRef ==` the canonical identity of the *current* journal revision and `executionId ==` the projected `transitionExecutionId`; otherwise `Unavailable`. Same-store journals never read it.

**My 186 sweep, ported** (`probes/sweep.py` → `io/sweep.txt`; only change: each context carries a coherent binding): 4,320 states, **0 disagreements**, 0 post-fence ABORT; every targeted counterexample line is byte-identical to my 186 output. The binding gate changed nothing for correct inputs.

**My W-2 wrong-id sweep under three conditions** (`probes/binding.py` → `io/binding.txt`, 864 states, physical truth fixed):

| Condition | Result |
|---|---|
| binding carries the **true** id, supplied id wrong | **864/864 `Unavailable`** — the hole I measured in `NOTES-W2` is closed whenever the binding is truthful |
| binding **and** supplied id both wrong (a consistent false assertion) | 830 same as truth, 22 safe-direction QUARANTINE, **9 DANGEROUS ABORT + 3 DANGEROUS RELEASE-ONLY** — exactly the 12 I measured before. The limitation is preserved, and the owner says so: "does not authenticate arbitrary caller assertions" |
| both true (control) | 864 same as truth |

That is the honest shape: the prerequisite converts *inconsistency* into unknown-custody; it cannot, and does not claim to, detect a coherent lie.

**Precedence, including terminal and same-store** (context reads recorded by a spy): binding missing → `Unavailable` having read only `fenceHeld, activeTransitionBinding`; the same for a `DONE` and an `ABORTED` journal, for a binding naming a *different revision of the same journal*, and when registry or leases are *also* wrong (binding wins, as stated). Fence-not-held still wins over a missing binding (`REFUSE`, only `fenceHeld` read). With a good binding and missing leases → `BUSY`. Malformed binding (extra member; upper-case hex in `journalRef`) → schema `ValidationError`. Same-store `core-repair` / same-schema `core-update` at `COMMITTED` with **no** binding → RESUME-COMMIT, reads `fenceHeld, namespaceRegistry, leasesReacquired` only.

**Phase C** (`probes/phasec.py`): through the real `sequence`, for `PREPARED`, `DONE` and `ABORTED` journals, five binding faults each (missing, `None`, execution differs, stale revision, malformed) → `stop=unknown-custody`, `retired=False`, `newAdmission=not-attempted`, Phase C inputs never read; each healthy control reaches Phase C. The terminal coverage I asked for in `NOTES-W2` §3.5 is there: a bad binding cannot release or retire.

## 4. SQL side (`probes/sql_probe.py` → `io/sql_probe.txt`, SQLite 3.51.0)

- 188 carrier SQL instantiates **8** carrierFormat-3 objects (adds `cf_no_replace`); 186's instantiates 7.
- 188 `carrier_format`: `REPLACE`, `INSERT OR REPLACE`, `INSERT OR IGNORE`, plain `INSERT` of the singleton all **refused** with `recursive_triggers` OFF and ON. Control on the 186 seven-object SQL with triggers OFF: `REPLACE` **accepted and the row changed** — the hole my inventory listed, now closed in the reference.
- Owner's carrier checker additionally runs this under UTF-8/UTF-16le/UTF-16be and asserts that a carrier with `cf_no_replace` dropped dispatches to `migration-footprint-corrupt` in both open phases (read; it is in the 479).
- **Attempt DDL "exact 187": confirmed.** The reference `proposedPrivateDDL` is **byte-equal** to `ATTEMPT_DDL` in my verified 187 product (`sha ee45313f51a0…` both), and the instantiated `sqlite_schema` rows are equal.

## 5. Mutation (`probes/mutation.{py,json,log}`, `mutation2.{py,log}`, `stale_revision.py`)

Eight mutants of the binding block, scratch copy, judged by the owner's focused checks through the loader (not the pinned lane). Baseline 1,220/1,220.
- **6 killed**: block removed; `journalRef` not compared; `executionId` not compared; binding not required for terminal journals; missing binding tolerated; binding checked after registry/leases. All die on the owner's spy assertion "binding gate read later input" — a good control. *(My first version of the "after registry" mutant crashed with `UnboundLocalError`; that is a broken mutant, not a kill. It is preserved in `mutation.log`; the proper one in `mutation2.log` is killed behaviourally.)*
- **2 survive the owner's checks:**

| Mutant | Evidence | Assessment |
|---|---|---|
| binding required for **same-store** too | my probe: same-store `COMMITTED` without a binding → `Unavailable` instead of RESUME-COMMIT | real gap: the "same-store stays journal-only" control is asserted in prose; no owner check runs a same-store journal *without* a binding |
| `journalRef` accepted for **any revision of the same journal** (state ignored) | `stale_revision.py`: binding names the `LEASED` revision while the journal is `PREPARED`, healthy fenced footprint → original `Unavailable`, mutant **RESUME-COMMIT** | real gap: owner checks use a wholly different ref, never a stale revision of the *same* journal. This is the case "exact **current** journalRef" exists for |

(My binding probe flagged the second only through a changed read order, because that case used an unavailable footprint; I added the behavioural confirmation rather than count a side effect.)

## 6. Findings

No finding against the recovery or guard logic.

### T-1 (test strength) — the two survivors above
Add: same-store journals at every state with `activeTransitionBinding` absent (must behave exactly as before); a binding whose `journalRef` is an earlier revision of the same journal, with an otherwise healthy observation (must be `Unavailable`).

### W-1 (low-medium, liveness) — "exact current journalRef" makes (journal revision, binding) atomicity load-bearing
Journal identity includes `state`, so every journal state write changes the ref the binding must carry. The protocol says they are "one coherent carrier revision" and lists publishing it as host work. The consequence is not spelled out: if a host ever makes the two durable separately, a crash between them leaves a binding that names the previous revision, and by this law every executor then stops `unknown-custody` — for all states, terminal included, with no reference route out. That is the correct *safe* answer; it is also a permanent wedge needing custody/restore intervention. One sentence should say so, so the host author treats single-record atomicity as a requirement rather than an optimisation.

### W-2 (low) — the in-tree pinned report does not carry the new "historical" labels
`check-security-lifecycle.v1.py` now emits `historical: true` / `qualificationScope: historical-migration-v1-only` for the eight `migration-recover` cases — my regenerated report has exactly 8 such entries, all from `migration-cases.v1.json`. The pinned `security-lifecycle-report.v1.json` in the candidate is unchanged from 186 and has **0**. So 186 W-1 is closed in the generator and open in the artefact a reader would actually open. Either regenerate and re-pin it, or mark that file as a stale historical output.

### W-3 (low) — the ledger law is checkable against the product for one table of six
`ledger-mutation-immutability.v1.md` correctly states the rule ("every collision with every PRIMARY KEY or UNIQUE constraint"; statement-level refusal; `OR IGNORE` is not idempotence; extended `CONSTRAINT_TRIGGER`; unordered pin diffs; projection loss is custody loss; `first_publication` unverified) and names all six tables. Only `attempt_custody` has reference DDL; the key tuples of the other five appear nowhere in the reference, so reference↔product agreement for them rests on the 187 product review, not on anything a reference lane can compare. Listing the six key sets in the law (they are in my 187 review §3) would make drift visible.

### N-1 — reference and product carrier DDL now differ by one object until 189
The verified 187 product's `CURRENT_CARRIER_DDL` has seven objects; the reference now requires eight and refuses seven. Disclosed ("later product adoption"); worth a line in the build plan so nobody runs the product dispatch against a reference-built carrier in the interval.

### N-2 — source-fence slot law answers my 186 N-1
One attribution slot per store; initialised observed-none at admitted creation; survives DONE, retirement and PRESENT; superseded only by the next admitted source fence at the same recoverable boundary; an older carrier without the representation is *unknown*, never observed-none; no on-read initialisation. Coherent with the selector's `fence = other` handling. Same-store `jCOMMITTED`-before-pair-publication is now stated (186 N-2).

## 7. Closure of earlier findings

| Finding | Status |
|---|---|
| 186 W-2 / `NOTES-W2` (unbound execution id) | **Addressed as far as a reference can**: coherent binding prerequisite before later observations, terminal included; limitation vectors retained; no authentication claim. Truthful-binding case measured closed (864/864); consistent-lie case measured unchanged (12) and disclosed |
| 186 T-1 (foreign carrier; missing ancestor target) | **Closed, verified**: my two 186 survivors re-applied to the 188 selector are now killed by `footprint186.foreign-carrier.*` and `footprint186.absent-ancestor.*` (`probes/t1_186_closure.py` → `io/t1_186_closure.txt`) |
| 186 W-1 (historical labelling) | closed in the generator; **open in the pinned report** (W-2 above) |
| 186 N-1 / N-2 | closed in the protocol text |
| 185 F-1 for `carrier_format` | **closed at reference level** (guard + eight-object dispatch + seven-object refusal); product adoption owed |
| 187 reference counterparts | attempt DDL byte-equal to product 187; ledger law added (W-3) |
| Inherited format 1/2 and marker tables | unchanged, as they must be; still unguardable, still disclosed |

## 8. Limits

Pure reference over asserted observations; nothing here shows a host builds the binding from a sealed carrier, keeps it atomic with the journal, or publishes fence/pair/floors correctly. My sweep's oracle is the protocol's stated write order. SQL probes ran on system SQLite 3.51.0. I did not rebuild the owner's six behavioural or two SQLite mutants, and did not look at 189.

## 9. Verdict (bounded)

**188 does what it says: the carrier singleton is guarded at the schema level and seven-object drafts are refused; the attempt DDL is byte-equal to product 187; the Phase A binding stops every inconsistent identity before registry, leases, footprint, retirement and Phase C — terminal journals included — while leaving same-store journals and all 4,320 correct-input outcomes unchanged; and the consistent-false-assertion limitation is preserved and disclosed rather than argued away. T-1 names two untested protections; W-1 is a liveness consequence the host author must be told; W-2 is a stale pinned report.** No cumulative, product or host approval.
