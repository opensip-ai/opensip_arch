# Independent adjudication — storage D2 generation-handling proposal

Reviewer: Claude (actual independent reviewer; Codex remains owner). Date 2026-09-18.
Request: `/tmp/opensip-implementation/reviews/storage-D2-20260918-REQUEST.md`.
Standing: **design adjudication only.** Not code acceptance, not selection, no whole-project or
operational authority. Nothing in the repository, frozen subjects or product was edited; no commit,
push or delegation. All reviewer output is under this directory.

## 1. What was reviewed (exact bytes)

| Item | SHA-256 |
|---|---|
| Proposal, copied to `claude-out/proposal-as-reviewed.md` (4,574 bytes) | `7d50474337601b02b70b7dc3630d75b7119dd7cb9cdce8030ef58f77c5a1de45` |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` (read: §1 precedence, Step 3, Step 4, §3) | `7bcc8f8e23da91e87d36e7c1a1c913f05a634be058e4a4c5c0c73ac4faec1d80` |
| `docs/coop/design-corrections/security/carrier-format.v3.md` (§4, §5 laws, §7, §8, §10–§12) | `2c3e465d90140228225790fec5eeac00c767d7f0ed06842be5e855fdb6145a7f` |
| `…/security/carrier-migration.v1.md` (§3, §4) | `446c73dc9c95ae293c97660ac8dac41d1d969f518ddb0deb80c08e4e628e5da6` |
| `docs/coop/completion/security-completion.v8.md` (§5.4, §5.5) | `54f3a6901d4192c5b6af82d4aad4414a84ee3b7748aa67cae06272a481e38c2d` |
| `docs/coop/completion/security-completion.v2.md` (§5.4 write-ahead protocol, high-water) | `fca2a4b615a3261f61e2e2d7a685b1b747678dedc54f9f87d7adcd643ffd3b78` |
| `docs/coop/completion/security_unit_lib_v8.py` (`reconcile_witness`) | `3e28bc7ba34e3a5964ca5c611a1735ee6771b7084256893d648a15d8ddf56d40` |
| `…/security/grant-journal.carrier.v3.sql` (`carrier_quarantine`) | `b82d63c07bc7ca0a735fb0ce07e5b9410a31b78d152e4a7dd9dcb61553944c91` |
| `…/security/carrier-highwater.schema.v1.json` | `1bbfd9135bd9492ef5b1df328aacdb959b0440a9e21312763f88609f4b966f82` |
| `…/security/check-carrier-v3.py` | `834e337a18b1f6320463b3cd6d3132b7e809d5c32acc976c12a8f6238872b977` |
| `docs/v2/architecture/carrier-fault-cases.v1.json` | `d510662ce455b851d8180954a023b875667c2386be0991253337cb7118f347da` |
| `security-and-lifecycle.md` lines 775–800 at repository HEAD `e185d7e91` | (read in place) |

Full list: `claude-out/owners-read.txt`. Evidence hashes: `claude-out/hashes.txt`.

**Existing bounded schedules.** I looked for one that already covers the question. There is none:
`check-carrier-v3.py` models the witness only as "names admitted / other project" (`_s37_open`,
lines 751–790) and has no witness generation, no floor and no capture interleaving;
`carrier-fault-cases.v1.json` has 16 cases, none with a witness or floor naming a generation other
than the association's. The C11 drift model the read-only owner cites is not in the selected tree
("no operative rule may be recovered from … any reference model"). So the proposal's last sentence
("re-run existing … bounded schedule model") cannot be satisfied by what exists; a new one is needed.
I therefore wrote my own (§3). It is reviewer evidence, not a normative model.

## 2. Verdict

**The direction is right and I found no lawful counterexample to item 4 — but the proposal is not
yet freezable.** Items 1, 3 and 5 I agree with. Item 4 is sound under one premise no owner states.
Item 2 is weaker than the proposal claims ("same retained-custody assurance bound") and needs two
further conditions, both free to evaluate. Four owner decisions are still missing.

Findings, most severe first.

### F-1 (must fix before freezing) — the historical-floor row loses tail anchoring, and ignores the durable per-generation quarantine marker

Proposal item 2 calls the new row "under the same retained-custody assurance bound" as Case C.
It is not. In Case C the witness `PENDING t+1` still pins the tail of the requested generation; in
the same-generation table a truncated tail is caught by `COMMITTED n > tail`. Once the witness has
moved to a later generation, **nothing pins the old generation's tail above its floor**, and with
item 3's honest admission that the closing operation's floor copy names the *new* generation, the
old floor is normally *below* the old tail.

Reproduced (`d2-model-r1`, X3): generation 1 closed at seq 3, floor at 1, rows 2..3 then removed.
Every later read of `(1,1)` is `confirm:hist-floor`; no read ever reports a condition. The same
bytes observed one step earlier (witness still `COMMITTED(1,3)`) are `unknown-quarantine-condition`.
So the answer becomes *more permissive* purely because the writer moved on.

Two owner facts close most of this at no cost:

1. **A lawfully superseded generation ends in `TERMINAL`.** WA-13 and carrier-format §5/§7: all
   three closure causes append `TERMINAL/grantGenerationClosure`, and the superseded-generation
   trigger forbids later appends. Require, in the same journal snapshot, that the requested
   generation's tail row is that `TERMINAL` (schema 1, cause `grantGenerationClosure`). A superseded
   generation without it is a quarantine *candidate* (Step 4 applies). With this rule X3 becomes
   `superseded-generation-without-TERMINAL` and **no lawful schedule is affected** (r2: L1–L3, L5
   still 0 reports), because the witness cannot name `g+1` before `TERMINAL(g)` is durable and `J`
   is captured after `W1`.
2. **The one lawful supersession without `TERMINAL` has a durable marker.** v2 §5.4:
   `uncertainTailLoss` → `carrier_quarantine` row, `failClosedNoAppend`, "continuation only on a new
   grant generation". `carrier_quarantine` is keyed `grantGeneration INTEGER PRIMARY KEY`
   (`grant-journal.carrier.v3.sql:161`). The read-only owner never reads it. For a historical
   generation it is the *only* surviving record that the writer itself found that generation
   damaged. The floor row must read it in the same snapshot; a row for `A.grantGeneration` →
   `unknown-custody` (my recommendation; it is the writer's own finding, not a reader diagnosis, so
   Step 4 need not gate it) — never `confirm`. Model case Q1 shows the behaviour.

What remains after both: substitution of rows strictly between the floor and `TERMINAL` (X5 — caught
only when it hits the joined `k`), i.e. exactly the selected `interior-bodies-not-authenticated`
limit. That *is* the same bound. State it that way.

### F-2 (must state) — item 4 rests on an unowned premise: how the witness crosses a generation boundary

Item 4's argument is "a later-generation SEAL cannot have committed while the witness remained in an
older generation". I agree **if** the first append of generation `g+1` is an ordinary write-ahead
append. No owner says so. What the owners actually say:

- v8 §5.4 table: "witness names another carrier (digest **or generation**) → QUARANTINE";
  `reconcile_witness(…, grant_generation, terminal=False)` compares `witness['grantGeneration'] !=
  grant_generation` first. The `terminal` parameter is accepted and never used.
- Nothing states which generation the opener passes between `TERMINAL(g)` durable and the first row
  of `g+1`, nor whether the witness is re-initialised (`COMMITTED (g+1, 0)`, which the closed shape
  permits) or goes straight to `PENDING (g+1, 1)`.
- `carrier-migration.v1.md` §3 act A is "single INSERT under the inherited append triggers" — no
  witness step is mentioned for that `TERMINAL`.

Consequences, measured:

- L1/L3 (witnessed `TERMINAL`, with or without the `COMMITTED(g+1,0)` step): 0 lawful reports in
  777,548 / 561,688 reader interleavings. Item 4 never fires lawfully.
- **L4 (unwitnessed `TERMINAL`): 42 lawful `unknown-quarantine-condition` reports** out of 399,960,
  all through the *existing* row "tail > witness seq", all with stable brackets and two agreeing
  tails — Step 4 does not save it, because the state is stable, not skewed. This is not caused by
  the proposal, and for carrierFormat 1/2 generations it is unreachable (F46 and the `{A}` prefix are
  decided first). It is reachable for any future closure of a carrierFormat 3 generation performed
  the way act A is written.

Required owner sentence (one): *every `TERMINAL` append and the first append of a new generation
follow the v2 §5.4 five-step protocol; the witness generation never decreases; the generation passed
to reconciliation is the highest generation with a row, or the witness generation when that
generation is closed.* With that sentence item 4 is a theorem, not a judgment:

> `A` exists ⇒ `SEAL(A.g,k)` committed ⇒ witness was `PENDING(A.g,k)` before that commit ⇒ (monotone)
> every later witness read names a generation ≥ `A.g`. The ledger snapshot precedes `W1`.

Note this holds **whether or not the SEAL is present in `J`**. The extra condition in item 4 is
therefore not needed for soundness; what it does is choose the *diagnosis*: SEAL present + lower
witness = witness rolled back alone (X1, reported as `lower-witness-with-seal`); SEAL absent = the
namespace rolled back together (X2), which the existing F22 rule already owns. I support keeping the
condition for that reason — do not describe it as the thing that makes the rule safe.

### F-3 (must define) — "`t`" and "the two agreeing tails" are ambiguous once generations differ

Step 3 says "`t` = captured tail seq" and Step 4 "two journal snapshots agreeing on tail sequence and
tail digest". With one generation these are unambiguous. With a historical `A` they are not: carrier
tail or tail of `A.grantGeneration`? It matters:

- X2 is detected (`F22-lower-tail`) only if `t` is the tail **of the requested generation** (0 when
  that generation has no row) and `H` is that generation's floor.
- If the Step 4 tails are the *carrier* tail, a busy current generation makes every historical
  diagnosis `unavailable-busy` forever, though the closed generation cannot move. If they are the
  requested generation's tail, a closed generation is trivially stable — correct, and it also means
  Step 4's protection is vacuous there, which is one more reason F-1's `TERMINAL` rule matters.

Recommendation: both are per requested generation; say so, and say that an absent generation is
`t = 0`, not "generation absent → unknown".

### F-4 (decision) — per-generation floor keying is a new storage law, not a clarification

The read-only owner says "`H` = the SC-TRUST floor for that carrier **and generation**"; the only
shape (`carrier-highwater.schema.v1.json`) is titled "per-**carrier** floor", has one
`grantGeneration` *member*, and is still `PROPOSED-NOT-SELF-ACCEPTED`. v2 copies "at operation start
and end". No owner says floors are retained per generation, so today a generation advance plausibly
*overwrites* the only floor. Item 3 is therefore a new retention law and needs: the key
(`projectKeyDigest`, `grantGeneration`); that a copy never lowers or replaces another generation's
record; bounded growth (one small record per closed generation — state it; generations are rare);
the rule that a floor whose `grantGeneration` member disagrees with its key is malformed, not
foreign; and the migration/rollback copy-forward the contract already promises for other floors.
Also fix the schema's standing before anything depends on it.

### F-5 (disclose as a selected limit) — the last operation of every generation is permanently `unknown-custody`

Measured, L1: `(1,2)` — committed in the operation that closes the generation — is
`unknown-custody:hist-floor-insufficient` in 99,495 reads and `confirm:hist-floor` in **0**, for
ever. Item 3 says this honestly. It should be listed with §3's selected limits, with its size: every
SEAL after the closing operation's *start* copy. For a whole-generation REV that is small; for a
long-running operation that ends in rollover or migration it is not.

On the "closure handoff": L2 (end copy covers every generation) recovers it (38,466 confirms) and is
lawful **as an end-of-operation act**, because the v8 end sequence already holds fence + re-acquired
lease with no writer able to append to a closed generation. It needs no fence acquisition under the
lease. I recommend selecting it now rather than deferring: it is the existing end copy applied to
"every generation this operation appended to", not a new mechanism. Its one condition: if the lease
is not re-acquired the v8 rule "skip the copy (that writer's start recorded a tail at or above
ours)" is **false for a closed generation** — the other writer's start copy names the new
generation. State that the skipped closed-generation copy is simply lost (→ F-5 limit), never
assumed covered.

### F-6 (agree) — item 1 (my C2a) and item 5

Item 1 is what I asked for. One addition: "retain exact raw-byte SHA-256 + bounded reason" must name
the reason vocabulary as closed (the D1 codec's refusal kinds), or P-1-style reflection reappears.
Item 5's precedence is right: carrier format → project binding → floor shape → generation. Add
explicitly: a floor record for the requested key that is malformed is `witnessMalformed`-class
(candidate, Step 4), while *absent* is `unknown-custody` and *unreadable* is unavailable — three
different outcomes, all three needed as cases.

### F-7 (minor) — higher-generation witness: also refuse the impossible direction

Item 2 handles `W.g > A.g`. Add the mirror sanity check that costs nothing: `W.g` above the highest
generation with a row **and** `W.state == COMMITTED` with `seq ≥ 1` is `COMMITTED n > tail` for that
generation (tail 0) — an existing v8 row, reportable for the *current* generation, and irrelevant to
a historical `A`. Say which: my recommendation is that it must not block a historical floor-anchored
confirm (it says nothing about generation `A.g`) but must be carried as a diagnostic.

## 3. Reviewer model (evidence, not law)

`claude-out/probes/d2_model.py` (r1) and `d2_model_r2.py` (r2 = r1 + the two F-1 rules). Writer =
atomic durable steps of the v2 §5.4 protocol, floor copies at operation boundaries, closure by
`TERMINAL`, first SEALs of generation 2. Reader = association fixed at ledger-snapshot time, then two
captures `(W1,H1) J (W2,H2)` at every non-decreasing placement over the timeline (so every crash-stop
prefix is included); decision = Step 3/4 as written plus proposal items 2 and 4.

| Schedule | Interleavings | Lawful quarantine reports |
|---|---|---|
| L1 witnessed TERMINAL, `COMMITTED(g+1,0)`, current-generation floor copy | 777,548 | 0 |
| L2 as L1, end copy covers closed generation | 777,548 | 0 |
| L3 no `COMMITTED(g+1,0)` step | 561,688 | 0 |
| L4 **unwitnessed TERMINAL** | 399,960 | **42** (existing v8 row; F-2) |
| L5 crash + REVERT before closure | 1,432,665 | 0 |

Adverse origins (applied at the end of L1): X1 witness-only rollback → `lower-witness-with-seal`
(item 4) and `v8-row`; X2 namespace rollback → `F22-lower-tail`; X3 closed-generation truncation →
**never reported in r1**, `superseded-generation-without-TERMINAL` in r2; X4 floor-row substitution →
`floor-hash`; X5 interior substitution → `unknown-custody:join` only at the joined `k` (selected
limit); Q1 quarantine-continuation → `unknown-custody:generation-has-quarantine-row` in r2.
Outputs: `claude-out/d2-model-r1.{json,log}`, `d2-model-r2.{json,log}`.

Limits of this model, stated: two generations, ≤ 3 rows each, one writer, W/H read at one instant per
bracket half, no SQLite/WAL visibility effects, no declared-restore (§5.5) path, adverse counts mix
reads before and after the mutation (only presence/absence of an outcome is meaningful there). It
does not model migration 1/2→3 because F46 and the prefix rows pre-empt the witness table there.

## 4. Decisions still missing (owner, not reviewer)

1. F-2 sentence: witness protocol across `TERMINAL` and first new-generation append; meaning of the
   unused `terminal` parameter; whether `COMMITTED(g+1,0)` is a lawful witness state.
2. F-1: outcome for a generation with a `carrier_quarantine` row (I recommend `unknown-custody`), and
   whether the `TERMINAL` tail requirement is a candidate (Step 4) or a plain `unknown-custody`.
3. F-3: per-generation `t`, `H` and Step 4 tails.
4. F-4/F-5: floor keying and retention law; select or defer the end-of-operation closed-generation
   copy; list the last-operation limit among the selected limits.
5. Declared restore (§5.5) with a ledger that outlives the namespace: confirm that the association
   ledger is outside the restored set, since X2's detection depends on `A` surviving.

## 5. Required cases — additions to the proposal's list

Closed generation truncated above its floor with and without `TERMINAL` surviving; quarantined
generation followed by continuation; reader capture straddling `TERMINAL` commit, straddling
`COMMITTED(g+1,0)`, and straddling `PENDING(g+1,1)`; floor key/member generation disagreement;
skipped end copy because another writer holds the lease; `k` equal to the `TERMINAL` seq (must be
`unknown-custody` at the join — `TERMINAL` is not a `SEAL`); busy current generation must not turn a
closed-generation answer into `unavailable-busy`.

## 6. Bounded verdict

**Proposal D2: sound in direction, CHANGES REQUIRED before a normative successor is frozen**
(F-1, F-2, F-3 substantive; F-4, F-5 decisions; F-6, F-7 minor). No lawful counterexample to item 4
was found in the owners or in 3.9 M modelled interleavings, conditional on the F-2 premise. This is
not approval of any text, model or code, and implies nothing about D3–D6.
