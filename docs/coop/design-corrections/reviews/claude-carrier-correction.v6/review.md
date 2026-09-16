Done. Source25 pristine, root's three supplied files unmodified, v5 immutable, all writes in v6 `scratch/`.

## Your confirmed corrections

**1. Act B was never atomic — accepted without qualification.** Your `ddl-atomicity.py` was right: `executescript` issues an implicit `COMMIT` and then runs statements one at a time, so `executescript(DDL3)` + `commit()` is not one transaction, and my v5 C13 asserted atomicity while never testing failure inside it. B stays normatively atomic, but the mechanism is now explicit — `BEGIN`, every statement, `COMMIT`, `ROLLBACK` on failure — and the helper performs it. The decisive number: `v5 ["carrier_format"] → v6 []`. C15 replays *your* extraction method to show it; C11 A13 reintroduces the v5 helper and is caught with the diagnostic `table carrier_format already exists` — your surviving-object defect visible in the failure text. Writing the splitter exposed a second bug of mine: the trigger-body `END;` truncated `gj3_append_laws`, now fixed with BEGIN/CASE/END depth. Added mid-DDL failure, success, every legal prefix, and partial-object refusal — and the partial probe showed recovery *crashed* on a malformed stub, so that check now precedes any row read.

**2. Selected documents reconciled.** §8 now keys detection on the published **row** with a partial-object branch; §9 no longer claims a format-unaware core "refuses typed" — it separates the aware {1,2} core (which does) from the unaware one (which cannot), labelled a selected disclosed limitation. Header and change set point at v3, plus a selected-companion table naming stable paths and stating v1/v2 are superseded and never competing owners.

**3. The receipt has no store binding.** Confirmed closed, 8 members, no `storeGenerationDigest`. Joins corrected to the members it actually has; binding flows through the admitted handle + association and mismatches are caught at that owning join. C16 uses real instances of both records — no `{x:1}` stand-ins — and found a third version axis: the receipt's `schemaVersion` is **const 2**, distinct from association `recordSchema` 1 and journal `recordSchema` 3.

**4. Identity §2 scoped.** Uniqueness reservation restated separately and unweakened for all modes; the durable record scoped to durable-authoritative commit-capable attempts; read-only and `--ephemeral` explicitly excluded, citing §5.

**5. Uncertainty stops the attempt** — cleanup, release, then a separately admitted fresh maintenance attempt with its own `migrationOpRef`. And `store-gc` is now written out as a **selected prospective expansion**: the inherited row proves only the negative, not prior authorization.

## Dispositions

Two-tail clause settled as selected policy with the non-necessity evidence retained and the "may drop" wording gone. **Receipt-present + `admitted` dropped as a contradiction** — it's the lawful interval, fixed together across C6, C14, recovery §2.1, the record, and the stale E3 wording; the composed commit → reader → sweep case now executes; C6's 77 spurious contradictions became `committed-historically`. DDL placement selected in the inventoried ledger modules. Schema owner cited explicitly from both selectors plus line 38's "not an alternative parser" — **the run2-vs-run3 gap is withdrawn**.

Counts: C12 39→42, C13 41→50, C14 51→57, C10 84→90, C11 19/17→21/20, plus C15 7/7 and C16 22/22. A2 remains the one undetected drift, by design.

**§8 reports no remaining real architecture contradictions.** Three items are yours to settle, none a contradiction — chiefly that `snapshot-dependent` (F29) in your proposal has no projection row in my §1 table, so it needs a row or a decomposition. Comments are in `comments-on-root-F00-F37-proposed.md`; your file is untouched. The manifest's `standingCorrections` names both stale v5 claims (twelve→sixteen; sweep now specified, only execution outstanding).
