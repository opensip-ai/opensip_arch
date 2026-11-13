# Erratum X5-E1: replay's retained-byte cap is re-sized; a proposed re-routing of a cap crossing (author draft, 2026-11-13)

Status: **PROPOSED.** Part A implements lead decision LD-DEC-7 items 2 and 3 (`LC/decisions/LD-DEC-7-durable-shapes/DECISION.md`,
`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). Part B is **not decided**: it is a question put to the
reviewers (LD-DEC-7 item 4). The erratum is **additive**: the accepted bytes stay frozen.

Corrects one accepted text: law X5 r4 (the replay-to-commit join), accepted 2026-10-04 by GROK2:
`docs/implementation/m2/replay-join-x5/PROPOSAL-r4.md`, 28,966 bytes, sha256 `2734f74b629a0fc27d80e90c38d07a901e21ac625e830b7715897c3151f88b71`.
The live `PROPOSAL.md` (29,175 bytes, sha256 `da0676d2…`) is r4 plus a two-line acceptance note, so its line numbers are r4's plus 2.

Model and form: `../errata-2026-11-11/ERRATUM-I1-E1.md` and `../fact-admission-h/ERRATUM-H-E1.md` (branch `errata-2026-11-11-r1`):
an additive erratum, adopted by the lead with a receipt.

**Which record form applies (checked against the product's `design-lock.json` at product main `1bd328f3`).** No path under
`docs/implementation/m2/replay-join-x5/` appears in the design lock. So no passage successor applies, and the form is an
erratum with an adoption receipt (`ADOPTION-X5-E1.md`, not yet written).

## X5-E1.1 Part A: the value (decided, LD-DEC-7 item 2)

**The accepted sentences.** Live `PROPOSAL.md:130` (r4 `:128`):

> 5e. **`REPLAY_LIMITS` and the bounds test (r3).** No design source fixes the values. `REPLAY_LIMITS` takes the values the host's replay corpus test (`crates/host/src/native_owner_tests.rs`) and X3d-2's storage tests already replay under:

and live `PROPOSAL.md:134` (r4 `:132`):

> - 33 554 432 retained bytes (32 MiB).

**Corrected.** Line 134's bullet is read as:

> - 268 435 456 retained bytes (256 MiB). This is a local development bound, not a product limit. It is sized from the measured real closure trees, which every commit copies into memory and counts (erratum X5-E1). The corpus value of r3 refused a Run on those trees.

**Why.** Replay reads every tree file of every closure it reaches and copies each one into the Run's retained set. All of it
counts against this one cap.
- Bytes are checked at the end of `replay_run`, over every read frame and blob, with no exemption for closures
  (`evaluator/src/replay.rs:324`, as read in `LC/decisions/LD-DEC-7-durable-shapes/PROVIDER-TREE-VS-REPLAY-CAP.md` §2).
- Capture copies every marked blob (`identity/src/closure.rs:1602-1640`, same file §1).
- The code already calls these bounds local development bounds (`evaluator/src/replay.rs:10-11`, as quoted in `REDTEAM.md`
  finding 1).

The real closures, measured (`PROVIDER-TREE-VS-REPLAY-CAP.md` §3, from `LC/f4/f4a/evidence/freeze-probe/package-022`):

| tree | files | bytes |
|---|---|---|
| T (toolchain) | 128 | 133,732,818 (`bin/node` 120,573,328; `lib/typescript.js` 9,144,216) |
| S (standard library) | 115 | 3,804,937 |
| P (provider) | 54 | 1,027,509 |
| total | 297 | 138,565,264, 4.13 times the old cap |

The REPLAY-CAP-1 unit's run (`LC/replay-cap-1/commit1-before.txt:1-2`; product branch `replay-cap-1-r1`, tests commit
`322fb984`) measured what capture actually holds, counted by distinct blob:
- T alone: 133,729,613 bytes in 118 blobs, refused at 33,554,432 with `Limit`;
- T, S and P together: 134,756,890 bytes in 168 blobs, captured at 268,435,456.

The two counts differ (138,565,264 by file, 134,756,890 by blob). I did not establish why. Both are below 256 MiB, with
about 130 MB to spare.

**Memory cost (disclosed, LD-DEC-7 item 3).** Each commit copies the closure trees into memory: about 140 MB, held two or
three times during a commit (capture's arena, then `DeclaredObject`; `REDTEAM.md` finding 1, `commit.rs:279-286`). The
probe above peaked at 283,394,600 bytes (`commit1-before.txt`, "peak memory footprint"). The cap bounds encoded bytes,
not total heap (`closure.rs:1601`).

**The bounds test.** 5e's test (live `:136-141`) is unchanged. It measures the corpus and varies one dimension at a time.
At 256 MiB the constant is still at least the corpus's need. The new real-tree controls are REPLAY-CAP-1's (LD-DEC-7,
"Controls that follow").

**What Part A does not change.** The other eight values of 5e (walk and owner budgets, owner invocations, capture entries).
Items 4, 5, 5a to 5d and 5f. Every row and remedy. Custody: closure trees stay inside the Run's inventory and stay counted
(LD-DEC-7 item 2). The bounded-memory replay reader is a later unit, before the first real Run (LD-DEC-7 item 5), and is
not designed here.

**Product.** Branch `replay-cap-1-r1` at `7c020dc9` sets `retained_bytes: 256 * 1024 * 1024` and marks it "at risk until
that binds", naming this erratum (`crates/host/src/fact_admission.rs`, the `REPLAY_LIMITS` comment). When this erratum is
adopted, the mark's reference resolves to this file.

## X5-E1.2 Part B: which row a cap crossing takes (PROPOSED, NOT DECIDED; a question for the reviewers)

Until the reviewers rule, the route stays as it is (LD-DEC-7 item 4).

**What happens today.** At commit-time replay, `ReplayError::Capture(Limit)` (and `Structure(Limit)`, and an owner
traversal `Evaluation(Limit)`) takes the structural row: operational-failed, exit 4, `PROVIDER.PROTOCOL_VIOLATION`,
`provider-protocol`, detail `EVALUATION.INPUT_REFUSED` (live `PROPOSAL.md:79`, item 5's table). Its remedy is
"Correct the provider output and rerun the stage; retain its admission diagnostic." (live `:123`). Code:
`host/src/fact_admission.rs:125-128` (`Capture(..)` → `Route::InputRefused`) and `:153-156`
(`Code::ProviderProtocolViolation`, `Detail::EvaluationInputRefused`).

**The texts for keeping the row.**
- X5 chose it on purpose. Live `PROPOSAL.md:87`: "During replay, an `EvaluationError` (including `Limit`, the owner
  traversal bound of `REPLAY_LIMITS`) is the evaluator refusing to re-derive the retained closure. That is the structural
  row, the same row `Structure(Limit)` and `Capture(Limit)` already take."
- 5b (live `:111-113`): "The candidate is retained producer data, and the contract says 'Re-admitting retained producer
  data preserves the producer-contract meaning of a structural violation' … So the route is `provider-return`".
- X5 rejects a row per variant (live `:89`): "a borrowed detail would carry a remedy its owner did not fix."

**The texts for the host-fault row.**
- The class follows the boundary the input came from. Native-evidence `native-evidence.md:3560-3563`: "The originating
  boundary decides the class and code, and it is the existing law. Admission §1 fixes the actor/layer split — 'Invalid
  external input is an admission rejection …; an invalid host-generated internal layer is a host invariant fault'".
- The lead's reading of it, LD-DEC-5 item 1 (`LC/decisions/LD-DEC-5-user-caused-host-fault/DECISION.md:51-55`): "the
  class of a refusal follows the boundary the offending input came from … A budget or limit crossing on a lawful input is
  a host defect and stays on the host-fault route until the budget is re-sized or an upstream bound refuses the input
  earlier."
- A retained-byte crossing is not a structural fault of what the provider returned. The bytes that cross are the host's
  own installed closure trees (the toolchain's `bin/node` alone is 120,573,328 bytes). No provider output can fix it, so
  the remedy names the wrong party.
- The nearest accepted precedent: fact-admission law M3-H, live `fact-admission-h/PROPOSAL.md:741` (r3 `:739`): the
  admission work bound is "host-internal", `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `WORK.BUDGET_EXHAUSTED`
  ("MJ rows 11 and 21's codes"), and `:754`: "A crossing on a return D3 accepted is a host invariant".

**The proposal.** A `Limit` crossing at replay (`Capture(Limit)`, `Structure(Limit)` and the owner traversal
`Evaluation(Limit)`) takes the host-invariant row that M3-H item 23 uses for its own admission bound:
operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `faultCause: host-invariant`, `WORK.BUDGET_EXHAUSTED`.
Every other `Structure`, `Capture`, `Law`, `Input` and `Evaluation` leaf keeps the structural row.

**Questions for the reviewers.**
1. Does 5b's "re-admitting retained producer data" reason cover a cap crossing, or only a structural fault in that data?
2. Is M3-H's row the right host-fault row here, and does `WORK.BUDGET_EXHAUSTED` have a published remedy for this route?
   I did not find a remedy text for it in X5 or M3-H.
3. Does splitting `Limit` out conflict with X5's "Rejected: a separate row per `EvaluationError` variant" (live `:89`)?
   The split is by condition (a host bound), not by variant.
4. Do `Structure(Limit)` and `Evaluation(Limit)` belong in the same move? Each is also a host bound of `REPLAY_LIMITS`.

**What would move if Part B is accepted** (by reading; nothing has been changed or run):
- law: a new bullet in X5 item 5's table and in 5d's remedies, and the amendment of `:87`;
- product: `crates/host/src/fact_admission.rs`: the `Route` match at `:125-128` needs a `Limit` arm before the structural
  one, a new route in `replay_termination` (`:137-157`) and its remedy in `replay_remedy` (`:171-173`). Whether the host
  can see `Limit` without matching the evaluator's error tree itself is open: X5 5a rejects the host matching that tree
  (live `:107`), so the evaluator's accessor (`evaluator/src/unavailable_evidence.rs`) would likely need a second
  classifier. Not established;
- tests: the "every `ReplayError` variant maps to its row and remedy" test and the bounds test, which expects "refused, on
  the structural row" at one below each need (live `:138`), and REPLAY-CAP-1's old-cap refusal test if it asserts the
  route. The design lock's X5a control text ("refuses one below on the structural row", product `design-lock.json:11751`
  and `:11752`) states the same and would need a lock passage change too.

## X5-E1.3 What this does not change

- No contract text (IE, NE, the fault contract) and no schema, digest or fixture.
- No row, detail or remedy (Part A). Part B changes nothing until a reviewer accepts it and the lead adopts it.
- No custody or inventory rule. The "replayable" label and its new control are LD-DEC-7 item 1's, not this erratum's.

## X5-E1.4 Review and binding owed

- **Review: two independent reviewers** (LD-DEC-7 item 2: "amended by an erratum with two reviewers"; resource
  accounting, OD-REVIEW-1 item 4). Part B needs the cross-vendor reviewer's ruling.
- **Binding owed:** the lead's adoption receipt `ADOPTION-X5-E1.md` pinning this file's sha256, as `../snapshot-plan-c/c2b1a/own-funding-r3/ADOPTION-E1.md` did for
  funding-r3. No design-lock entry (X5 is not a lock input). If Part B is accepted, its law change and the lock's X5a
  control text change are separate work, listed above.
