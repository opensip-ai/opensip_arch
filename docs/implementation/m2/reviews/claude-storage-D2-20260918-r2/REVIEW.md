# Independent adjudication r2 — storage D2 owner decisions and addendum

Reviewer: Claude (actual independent reviewer; Codex owns the decisions). 2026-09-18.
Standing: **design adjudication of unselected choices.** Not code, model or text acceptance; no
selection, no current authority. Nothing frozen, selected or installed was touched; no commit, push
or delegation. My r1 review and its evidence are unchanged.

## 1. Exact bytes reviewed

| Item | Bytes | SHA-256 |
|---|---|---|
| `storage-D2-owner-decisions-r2-20260918.md` → `claude-out/decisions-r2-as-reviewed.md` | 8,115 | `ed101e67e878d32f633cde1c4fa42ae7cef06f49e74ccfc8b2b59179138b02e9` |
| `storage-D2-r2-addendum-20260918.md` → `claude-out/addendum-as-reviewed.md` | 1,716 | `c834b6768456d33b4b8cfea916fe4c39d4f6376d61402486a0a11da94d440e27` |

Owners are those pinned in r1 `claude-out/owners-read.txt` (unchanged at repository HEAD
`e185d7e91`); for this round I re-read v8 §5.4 (fence/lease handoff, reconcile table), v2 §5.4
(quarantine continuation, high-water), `carrier-migration.v1.md` §3 and the `carrier_quarantine` DDL.

## 2. Verdict

**r2 resolves r1 F-1 to F-7 in substance, and the addendum's two choices are both right.** I found
no lawful false diagnosis and no unlawful confirmation beyond the already-selected interior limit.
**Not yet freezable:** item 5's open dispatch has undefined and no-progress cells (G-1, G-2), one
existing rule misreports a superseded generation as busy for ever (G-3), and item 4's scope is tied to
in-process memory with an undefined later authority (G-4). All four are wording-level decisions, not
redesigns.

### Resolution of r1 findings

| r1 | r2 disposition | My assessment |
|---|---|---|
| F-1 tail anchoring / quarantine marker | item 1: TERMINAL tail required; marker (even malformed) → `unknown-custody`; missing TERMINAL → `unknown-custody`, not a new diagnosis | **Resolved.** Choosing `unknown-custody` over my "candidate" is the more conservative option and I agree: it never confirms (X3 → `unknown-custody:no-terminal`) and adds no corruption class that Step 4 would have to justify. X6 (tail removed, TERMINAL re-appended) still confirms rows at or below the floor — that is exactly `interior-bodies-not-authenticated`, and item 1 says so. |
| F-2 witness across generations | item 5 + addendum ¶1 | **Resolved in principle**; see G-1/G-2. |
| F-3 per-generation `t`, `H`, tails | item 2 | **Resolved**; see G-3 for one consequence. |
| F-4 floor keying | item 3 | **Resolved.** The lock-order correction is right: v8 (the later owner) copies at start with fence **and** non-blocking lease held, and at end after re-acquiring both; "never under a project lease" was the v2 handoff v8 replaced. "Lower sequence or equal-seq/different-digest is a condition, never an overwrite" is the right monotonic law. Disclosing unbounded-but-small growth is honest. |
| F-5 last-operation limit / end copy | item 4 | **Resolved with G-4.** |
| F-6 closed reason vocabulary | item 6 | **Resolved** (four private classes, no raw text, D1 codes advisory — consistent with my 109 N-1/N-2 being advisory). |
| F-7 current-generation anomaly | item 7 | **Resolved**, as I recommended. |

## 3. Challenge results

### G-1 (must fix) — open dispatch after a quarantine marker: 8 no-progress cells, 6 open questions

`claude-out/dispatch-cells.json` enumerates the writer dispatcher exactly as item 5 + addendum state
it: 5 journal states × 14 witness states = 70 cells.

Quarantine continuation is "separately authorized existing behaviour, never produced by this pure
dispatch". Fine — but it has a crash prefix the dispatch must still classify: **marker(G) durable, new
witness not yet written.** In that state the witness is whatever caused the quarantine (absent for
`witnesslessRestore`; `COMMITTED n > tail`, `COMMITTED < tail` or malformed otherwise). The text gives
"existing refusal" again for all of them. `carrier_quarantine.grantGeneration` is the PRIMARY KEY, so
a second marker insert fails, and nothing in the text ever reaches "G is closed by quarantine → next
generation may start". 8 cells.

Needed, one sentence each: (a) marker(G) present ⇒ G is *already quarantined*: no second marker,
idempotent; (b) which witness contents are tolerated beside marker(G) — I recommend: any **same-project**
witness naming G, or absent **iff** `reason = witnesslessRestore`; foreign project still refuses; (c) the
separately authorized continuation then publishes `PENDING(G+1,1)` by the normal first-append rule.

The 6 "question" cells are the mirror: marker(G) present and the witness reconciles `OK` / `ADVANCE` /
`REVERT` against G. May a quarantined generation still be ADVANCEd or REVERTed (a witness *write*)?
I recommend no: `failClosedNoAppend` should also mean no witness repair in G.

### G-2 (must fix) — "highest journal generation" is undefined for an empty journal, and must include the inherited table

11 cells: every non-absent witness over a journal with no row. Two are lawful and common —
`COMMITTED(first_generation, 0)` (the INIT result) and `PENDING(first_generation, 1)` (crash before the
first ever commit) — and the addendum's rule "can name only the immediately next generation after
witnessed closure or quarantine continuation" refuses both, because there is no predecessor. Define
the base case: with no row in any admitted table, the only lawful witness generation is
`carrier_format.first_generation`, states `COMMITTED 0` or `PENDING 1`.

Same root: on a migrated carrier the predecessor generation lives in the **inherited**
`grant_journal`, not `grant_journal_v3`. "All admitted journal generation boundaries" must say so, or
the first v3 append after migration (`W = PENDING(first_generation,1)`, v3 empty, inherited G closed by
the act-A TERMINAL) falls into the undefined cells. Corollary worth adding to
`carrier-migration.v1.md` act C, which today checks only that the witness names the project: with a
witnessed act A, act C can also require `W == COMMITTED(G, seq(TERMINAL))`. And state explicitly that
no carrier exists that was migrated with the old *unwitnessed* act A (migration is prospective); if one
could exist, it needs its own row, because the dispatcher would quarantine it (`tail > witness`).

### G-3 (should fix) — a superseded generation with `k > t` is reported `unavailable-busy` for ever

Model X3, association `(1,2)` after the closed generation lost rows 2..3 and the floor is below `k`:
the existing ordering-hazard rule fires first ("`k > t` still … otherwise `unavailable-busy`"). For
the current generation "busy" is a fair guess — a writer may be in flight. For a generation both
witnesses place in the past, nothing can ever append (superseded-generation trigger), so the state is
permanent and "busy" invites unbounded retry. Item 1 already says "a superseded generation … has no
historical anchor: select `unknown-custody`"; make the hazard rule yield to it: *when both witnesses
are valid, same-project and later than `A.g`, `k > t` without the F22 floor condition is
`unknown-custody`, not `unavailable-busy`.* (With `H.lastSeq ≥ k` it stays F22 — X2 shows that working,
and shows the item-4 end copy *improving* detection: after R1 all three associations report
`F22-lower-tail`.)

### G-4 (decision) — item 4 scope: derive it from durable state, and delete or define the "later authorized observation"

I agree with selecting the end copy now, with "skipped re-acquisition promises nothing", and with
"only current admitted rows under both locks". Two problems:

1. **"Every generation this operation appended to" is process memory.** A crash between closure and
   the end copy loses it, and the next operation's start copy names only the generation the witness
   names. The set is derivable instead: under fence + lease, *the generation the witness names, plus
   the generation being closed in this operation*. More generally the honest rule is: a closed
   generation's floor may be raised **only while the witness still names that generation and
   reconciles OK against its TERMINAL tail** — that is the one moment a closed tail has an anchor.
   That covers the ordinary end copy, and it covers crash recovery when the crash came before the
   first new-generation append (witness still `COMMITTED(G, TERMINAL)`), with no remembered state.
2. **"…until a later separately authorized observation can raise that floor"** names an authority no
   owner defines. Once the witness has moved to `G+1` there is *no* anchor for G's tail above its
   floor; any later raise would bless whatever bytes are there, for a window far longer than the v8
   detection bound contemplates for the current generation. I recommend deleting the clause: after the
   witness leaves a generation its floor is final. "Do not claim permanent unknown in all cases" then
   becomes simply false-free: it *is* permanent for SEALs above that final floor, and R2 measures it
   (`(1,2)`: 11,334 `hist-floor-insufficient`, 0 confirms).

### G-5 (agree, tested) — addendum ¶2: historical confirmation without `stableW`

Sound. In the historical row the witness is not the anchor; it only *selects the row*, and witness
generation is monotone, so two individually valid same-project witnesses both later than `A.g` carry
all the information the row needs. Measured on R4 (closed generation, busy current generation,
4.46 M separately-timed interleavings of the 10 reads): `unavailable-busy` **489,905 with the addendum
vs 3,374,558 with strict `stableW`**; historical confirms 3,463,395 vs 578,742; across R1–R4
**0 lawful quarantine reports under either variant**, and every confirm is of a SEAL that lawfully
exists. Diagnosis keeps byte-identical W and H plus two requested-generation tails, as the addendum
says. One unspecified sub-case: W1 later, W2 valid and same-project but **not** later (generation
went down between reads — impossible lawfully). Say: retry; then `lowerWitnessGeneration` candidate
under Step 4, else `unavailable-busy`. My model treats any one-sided result as retry.

### G-6 (agree) — item 5's other choices

No proactive `COMMITTED(G+1,0)`: agreed; it still arises as the REVERT of `PENDING(G+1,1)`, and R3
(that exact crash, then retry) has 0 lawful reports. "Reconcile against the tail of the generation the
witness names, never a caller-selected generation" plus addendum ¶1 (a journal row in a generation
later than the witness is quarantine; do not let W.g's tail hide newer rows) closes the hole I would
otherwise have raised. The unused `terminal` parameter "is not authority": agreed.

### G-7 (minor) — items 6 and 8

Item 6: the proof sentence is now the right one (monotone witnessed appends + association precedes
W1). Item 8 is appropriately modest; in each restore test state which of {ledger association,
journal, witness, floors} survives — floors are excluded from lifecycle backup (v8 §5.5), so the
"namespace-only rollback" family always has floors ≥ the rolled-back tail, which is what makes X2
detectable.

## 4. Reviewer evidence

`claude-out/probes/d2_model_r3.py` → `d2-model-r3.json`: five separately timed reads per capture (item
2), r2 item-1 historical row, both addendum variants evaluated on identical interleavings.

| Schedule | States | Lawful quarantine (relaxed / strict) |
|---|---|---|
| R1 closure, end copy of gens 1+2 | 16 | 0 / 0 |
| R2 closure, end copy skipped | 15 | 0 / 0 |
| R3 crash before first new-generation commit → `COMMITTED(2,0)` → retry | 18 | 0 / 0 |
| R4 closed gen 1, busy gen 2 | 18 | 0 / 0 |

Adverse final states: X1 witness-only rollback → `lowerWitnessGeneration` for the newer association,
`v8-row` for the older; X2 namespace rollback → `F22-lower-tail` ×3; X3 → `unknown-custody:no-terminal`
and the G-3 `busy`; X6 → confirm at/below floor, `unknown-custody:join` above (selected limit).
`probes/dispatch_cells.py` → `dispatch-cells.json`: 70 cells, 11 undefined, 8 no-progress, 6 questions.

Limits: two generations, ≤ 3 rows, one writer, no SQLite/WAL visibility, no migration tables, no
declared-restore path; the dispatch table encodes *my reading* of the text — a cell I mark undefined
may be intended to fall under "existing refusals", in which case the fix is to say so. This is
bounded evidence, not a concurrency proof, and not the owner reference model item "required
evidence" calls for.

## 5. Additions to the required-evidence list

Marker-present open for each quarantine reason with the pre-continuation witness; empty-journal base
case (fresh and migrated); first v3 append after migration with the predecessor in the inherited
table; crash between TERMINAL commit and end copy, then next operation start; W2 lower than W1;
superseded generation with `k > t` and floor below `k` (must not be `busy`); end copy finding a
lower-or-different floor for the closed key (condition, no overwrite).

## 6. Bounded verdict

**D2 owner decisions r2 + addendum: direction and all seven r1 resolutions accepted as sound design
choices; CHANGES REQUIRED before a normative successor is frozen — G-1 and G-2 (dispatch
completeness), G-3 (superseded `k > t`), G-4 (end-copy scope and the undefined later authority).**
G-5/G-6 tested and agreed. This approves no text, model or code and says nothing about D3–D6.
