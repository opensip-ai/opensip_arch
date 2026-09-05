# D-044 turn 2 — Perform the D-033 property-pin rewrite

> **Status:** DRAFT — under review.
> **Date:** 2026-08-13
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Performs the file-08 rewrite
> D-033 authorized and refused to perform in the same commit
> (D-001 MF-6). Adds no file-08 status token. Does not amend
> D-001's five conditions.
> **Subject:** file 08 citation form and DR-001 live scope clause
> only. Not live-versus-history. Not DESIGN-READY. Not MEASURED
> regeneration. Not SATISFIED re-record. Not condition 5.

Turn-1 subject `coordinator-decisions.D-044.draft.md`
`6eb6f8692aa9225155c5877d34864968d32f814d469c79ec4142774d679c9865`.

Turn-1 findings:

| ID | Sev | Disposition |
|---|---|---|
| C2-D044-01 | SHOULD-FIX | ACCEPTED. The claim-matrix Key sealed laws pin is named below as outside this entry's file-08 scope and outside D-033 clause 1. Routed to a later file-09 D-000 act. Left whole-document until then. |
| NOTE-C2-D044-01 | NOTE | RECORDED. "A baseline refresh re-opens it" occurs twice in the DR-001 cell. Clause 2 already retires the sentence; the performing commit must retire both occurrences. |
| NOTE-D044-01 | NOTE | ADOPTION INSTRUCTION. Not a merits condition. Carried at adoption. |

Measured inputs:

| Path | sha256 |
|---|---|
| file 08 | `877e36d3b597fb9b51c1c91fb6b6c6f27eabdcb8b2b1a941ade2b34850a0f58f` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| blueprint | `909394c54dbd3588b9e455391f0fb2c5b1d2af51c9ca03b6802b1db47e44b7ad` |
| COORD | `726b472e75c2b8744a340fa17b751ead9180014696f2ab2c39cddab4b8265f61` |
| Claude 2 turn 1 | `0e6ee95d40297856ec70cb7d0accfca5e41f3f20cdaed6d9d0706d37cc01dac8` OBJECT, 0 MUST-FIX, 1 SHOULD-FIX |
| Codex turn 1 | `db0452a361fa00637ca7fe228008bb75eec0d75ad804821bb8f03f80beb09cd6` CONSENT, 0 MUST-FIX, 0 SHOULD-FIX |
| D-033 | adopted `ac48808`; clause 2 authorizes this rewrite and does not perform it |
| D-043 | adopted `a5d3719`; Lane R instrument recorded; not this subject |

## Extraction rule

Same rule D-033 recorded for freeze §7.10, generalized:

- Start: the heading line that names the cited section, or the
  first line of a numbered law / table row when that is the
  cited property.
- End: last line before the next heading of the same or higher
  level, or before the next numbered law, or the end of that
  single table row. Intervening blanks included. Next heading
  / next law / next row excluded.
- Hash: sha256 of those bytes with newlines preserved, including
  the trailing newline `sed -n 'START,ENDp'` emits.
- Line ranges below are convenience at the pinned freeze /
  blueprint whole-file digests. The delimiters are the pin.
- Wrong reading (heading through next heading inclusive) is
  not the pin. For §7.10 that wrong reading is `32da6d14…`;
  the pin remains `7bfa72c40b08381ceb0e9a815f6e0746f7c9c47f14b6b08496ef03980495c1ca`.

## Decision

1. **Perform the citation conversion.** In file 08, whole-document
   freeze and blueprint pins used as standing citations on
   DR-001 / DR-004 / DR-005 / DR-006 / DR-011 / DR-012 convert
   to the property pins in the table below. A later edit that
   does not change a cited property does not re-open that row.
2. **Perform the scope rewrite.** DR-001's live scope clause
   becomes: this row re-opens only when a cited property pin in
   its source-pin cell changes (path missing, named
   section/selector/law/row unresolvable, or segment hash
   mismatch). A whole-document motion of the freeze, blueprint,
   baseline, or this register that does not change a cited
   property does not re-open the row. The sentences "A baseline
   refresh re-opens it" and turn-3 R5 "any pinned-source motion
   re-opens the row" cease to be live scope. They remain
   history. Both occurrences of "A baseline refresh re-opens it"
   in the DR-001 cell cease to be live scope.
3. **Expected re-open.** This rewrite re-opens DR-001 by today's
   (pre-rewrite) scope clause. That is the one last lawful
   re-open D-033 clause 3 predicted. Live standing stays `OPEN`.
   The 2026-08-13 SATISFIED disposition stays history.
   SATISFIED re-record remains the D-001 two-stage act
   (MEASURED regeneration now; SATISFIED only after independent
   review). This entry is not that re-record.
4. **Does not edit** `v1-authority-baseline.json` or
   `v1-status-evidence.json`. Those files stay whole-document
   until a later MEASURED regeneration. This entry is not that
   regeneration.
5. **No new status token.** File 08 status vocabulary stays
   closed (D-006 turn-2 NOTE-03).
6. **No implementation authorization.** Condition 5 is unchanged.
   No freeze motion. No blueprint. No `docs/v2/implementation/`.
   No row becomes `SATISFIED`.
7. **Snapshot.** The dated current-position block's condition-1
   clause is updated so its leading label still matches the
   DR-001 cell (OPEN, now by D-044). Rows remain authoritative.

## Property pins to write

| Row | Cited property | Start delimiter | Convenience lines | segment sha256 |
|---|---|---|---|---|
| DR-004 | freeze §3.1 | `### 3.1 Phase-1A insertion — mandatory` | 580-603 | `19c6a3eb2664478a4fb340451bcd1878a0ee57bcbdb7ccafd5362c86fb02b490` |
| DR-005 | freeze §3 EVIDENCE row | line beginning `\| EVIDENCE \|` | 388 | `fe85576b57dec53c49dc36214dda66f4a85d4c8c9b1b230bb434a5cfb2c4e381` |
| DR-005 | freeze §3 TM row | line beginning `\| TM \|` | 391 | `dcbfb191f84643d9c1b315e8e0d8d30404ca4ecde0079c2d1f16ff75a76d2824` |
| DR-005 | freeze §3 OPERABILITY row | line beginning `\| OPERABILITY \|` | 383 | `dc1f8ef8c6d38c09448b1d31ad0106c40dfc4e9fad2c43b929f42e1d537aab75` |
| DR-006 | freeze §3 FACT-PLANE row | line beginning `\| FACT-PLANE / C-1 \|` | 379 | `d5891fa5cd7c0f5d0dfb36ff24ff742474f855185ba4ab71d2232a69bc41170c` |
| DR-006 | freeze §7.1 | `### 7.1 Parked identity recipes` | 1675-2267 | `30a2ff0af2deed4b35db0898be370436438da8e2855b6a79d4272f7643a4dced` |
| DR-006 | freeze §9 | `## 9. Phase-4 verification record` | 4674-5287 | `01e36920a0efb5c4555eba9c99a772bdd7cc61b79031b780369d802d5287bc1c` |
| DR-006 | freeze §6 law 6 | line beginning `6. \`RequestId\`` inside §6 | 1442-1463 | `0e3d3c69f77d8208bdf78b812d30154b0c494d600e24a80ca885cec13cef29ed` |
| DR-006 | freeze §6 law 19 | line beginning `19. **An identity namespace` | 1531-1580 | `671e2247806bcf8fb871740e5bdb3b7bf3aae38c5279d202b451fe1ef790c183` |
| DR-011 | blueprint §1.1 | `### 1.1 Normative byte set` | 121-836 | `39843bda8d29c4fafa9d078681332e3b5628be0ec51c78a55bd87dbc484fb358` |
| DR-011 | freeze §3 ledger | `## 3. Surface disposition ledger` | 285-691 | `9bb9765b2c9f17ed2ec5834434a98d0c7aad9d417c3c8c5cec816e85b45558f1` |
| DR-011 | freeze §7 | `## 7. Named non-blocking residuals and parks` | 1581-4609 | `9eeb80c0943436467b13964f77411d7af8992dc779a5904f5fe11dbb1eda578e` |
| DR-011 | freeze §7.8 | `### 7.8 Companion instruments` | 3884-4174 | `f305c6881a6572c02ec87bfc55b551a7073d07c51c4c17b75f7afded0ac84dd8` |
| DR-011 | freeze §7.9 | `### 7.9 Structural: applying a successor` | 4311-4448 | `a8db5cc13300802b7b68840a90d964197f995285fce91a4196e276e335973903` |
| DR-012 | freeze §6 law 17 | line beginning `17. \`implementable: true\`` | 1497-1498 | `cb2331f231f3ea04ab6e8388ed1996de75ec81530d277c7e7a605116e59dbe16` |

DR-001's source-pin cell already names the three manifests, not a
freeze whole-file digest. Those three remain cited. This entry
does not convert them. `R2-FINAL-03` stays the named residual
already routed at DR-011-R10; it is not given a new section pin
here. The claim-matrix **Key sealed laws** pin
(`docs/v2/architecture/09-v1-to-v2-claim-matrix.md`, the sixth
whole-document freeze pin in file 08's D-014 pin-accounting
note) is outside this entry's file-08 scope and outside D-033
clause 1's DR-row list. This entry does not convert it. It is
routed to a later file-09 D-000 act and stays whole-document
until then.

DR-005 keeps `operability.v10` `9bacbbf43dfb941a0d87330f79844d395b3ac838ae5bf54026ef4d69681696be` G19
as the already-specific instrument pin. DR-004 keeps the product
`CD-RT-5.whatThisDecisionDoesNOTDo.phase1A` selector.

## Alternatives

- Keep whole-document pins. Rejected: recorded DR-001 treadmill;
  D-033 already decided.
- Also convert the baseline JSON in this commit. Rejected: that
  is MEASURED regeneration (D-001 C3 / MF-8), a later act.
- Also convert the claim-matrix Key sealed laws pin in this
  commit. Rejected: file 09 is a separate register-content act.
- SATISFIED re-record in this commit. Rejected: D-001 two-stage.
- Coin DESIGN-READY. Rejected: D-033 clause 4; D-006 NOTE-03.
- Perform only the scope rewrite and leave citations. Rejected:
  D-033 clause 1 is the citation conversion.

## Readiness effect

Zero SATISFIED. DR-001 stays OPEN (expected re-open). Conditions
1–5 unchanged in text. Condition 1 still 0/11 SATISFIED.

## Reversibility

Compound after the rewrite lands: overturn requires reverting or
superseding this commit (C-D044) and restoring the prior scope
clause. Overturn: C-D044.
