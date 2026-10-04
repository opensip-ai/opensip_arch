# S18 r1 — REQUIRED-FINDINGS

Reviewer: GROK2. The request directory keeps the name `codex2-s18-r1` because the unit builder emits that review path. This review judges the unit.

Subject manifest `docs/implementation/m3/host-pipeline-j/s18-subject.json`: 1621 bytes, sha256 `9d184011d659d7cffe154280c3325aa3844f9625f24d20e71463f6ab00904ffc`.

Successor `docs/implementation/m3/host-pipeline-j/s18/successor.json`: 13062 bytes, sha256 `5407ce5170cfb7f5ae611c542f13a06297172e3afa36180f603ebcc14064f17f`.

Product HEAD `cd5958b3608f44a0035566c9d4500e5005c62e91`. `~/Library/Application Support/OpenSIP` is absent. No cargo, and no repository write.

Verdict: **REQUIRED-FINDINGS**. One required finding, RF-1. Two non-blocking observations.

## RF-1

WS:227-228 and WSE:229-230 still define `*after-settle*` as every required step already being terminal. S18 does not override those lines.

The new paragraph, appended at WS:231 and WSE:235, marks the render step `cancelled` at the output decision point when the signal is no later than that check. `cancelled` is one of the closed step outcomes (WS:99-102). The sentence that delays terminality until the output returns applies to "a render step that was not cancelled". README cross-law item 1d states the consequence the authors want J1 to record: for a cancelled step 1, terminality is earlier than the output's return. During that gap every required step is already terminal, so the unamended parenthetical classifies the interval as after-settle. The same paragraph says the invocation settles when the output returns and `*after-settle*` begins only then.

The plan copy already has the missing conjunct. Row E (copy line 337) reads "Every required step terminal and the required output returned". Line 225 was amended in place so the section is not before-settle. The after-settle parenthetical needs the same in-place amendment.

**Fix.** Two further line overrides:

- WS:228 before: `already terminal): the aggregate is **not reclassified**; the settled class stands.`
- WS:228 after: `already terminal, and, where the final output section below applies, only once that section's required output has returned): the aggregate is **not reclassified**; the settled class stands.`
- WSE:230 before: `already terminal): the aggregate is **not reclassified**; the settled class stands. Settled aggregates retain the required-step D9`
- WSE:230 after: `already terminal, and, where the final output section below applies, only once that section's required output has returned): the aggregate is **not reclassified**; the settled class stands. Settled aggregates retain the required-step D9`

Regenerate `PASSAGES.md` from those overrides. The inserted clause is the same on both parents; the WSE line keeps its trailing D9 sentence, so the full lines differ.

## Rulings

1. **The six existing overrides and the plan copy are exact.** Each `before` is the parent line. The three WS/WSE pairs are byte-identical in `before` and `after`. `build_s18.py --check` reported identical bytes. `check_s18.py` reports the copy differs from `PLAN-r3.md` only at r3 lines 293, 328, 335, 336 and 433, plus the one inserted row O. The live plan is r3 plus its two-line acceptance note.

2. **J1's S18 row is carried, including both observations.** The paragraph and row O carry terminality at output return, the decision point, deferral for durable and ephemeral alike, the committed-evidence renderer split (`DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the `runId` when a Run committed, otherwise `DELIVERY.REQUIRED_PROJECTION_FAILED`), the aggregate under WS:233-240, and exit 4 with no replacement. NB-01 cites X3d r8 items 6 and 9 and X7 r6 items 3 and 5, returns the fault to those owners through §9 (WS:1412-1413), keeps it out of verdict and closed-Run composition, and keeps the ExecutionId and namespace whichever termination is primary. Those citations match X3D:176 and :283 and X7:101 and :120. NB-02 classifies and defers every O signal, then splits the operational record by S-OP-2 r6's cutoff (step 1, r6:657), freeze reads (step 4, r6:664-682) and post-freeze tally (r6:682, :704). The withdrawn readings, "O follows the freeze" and the WS:1409 composition citation, are absent from the new text. `CancelPhase` `O` is an ordinary registration at r6:226-230.

3. **LD-1, LD-2, LD-3 and LD-10 stand.** WS and WSE are lock inputs, and the six selectors are free at `cd5958b`. The operability plan is not a `verify_design` input, so a complete copy of the accepted r3 bytes, selected by the record, is the sound successor. WSE takes the same three texts; its cancellation paragraph is longer, so the lines are 225, 235 and 1466. CINV has 45 commands; 44 end in `render`; `agent-serve` is `query` only. The copy's scope, rows D, O and E plus the §5.2 and §10 rows, is what the section touches. Rows A to C, the r3:338 note and §9's S-OP-12 row stay with OPP's next revision under J1's S15.

4. **LD-4, LD-5, LD-8 and LD-9 stand, and LD-4 is what makes RF-1 necessary.** The termination output is written in the section, and settlement is that output's return. A renderer failure of a cancelled termination output fails the render step (J1 row 44, J1:690). INV5's `Cancellation.phase` is `none`, `before-settle`, `after-settle`. An O signal stays out of the envelope and out of an invocation record the envelope carries. `deliver_required` at `cd5958b` is `write_all` then `flush` (`crates/host/src/delivery.rs:17-21`); the caller sees no byte count. `bootstrap.rs:55-60` already ends that failure at exit 4 with no replacement. Row O keeps the decided termination's drain (OPP r3:195 normal, r3:196 cancellation). NBO-2 is the S-OP-2 sentence that does not yet say this.

5. **The other consequential passages hold.** No remaining accepted sentence says every signal before the output returns is `interrupted` 130. WS:1393 / WSE:1466 now defer a final-output signal and keep the decided class. CINV's `interrupted-before-settle` and `interrupted-after-settle` goldens are the before-settle case and optional export after settlement; a final-output golden is the M4 unit's (LD-11). WSE:1389-1395 remains the before-settle interruption ledger: it requires a recorded before-settle cancellation and does not classify a signal in the section. LD-12 correctly leaves J1 8.3's commit-phase precedence to a later WS successor. WS:226 still gives `interrupted` for a before-settle signal, and the new paragraph points at "the termination the rule above gives" without restating rules 1 and 2. INV5's after-settle description is NBO-1.

6. **Selection is well-formed.** `verify_scratch.py --rev cd5958b` passes: 82 to 83 successors, six overrides, no supersession, inventory `v134`, inheritance 55, and a later override of WS:231 refused as conflicting. `check_s18.py` passed 121 checks. It scanned 25 unbound successor records, and none shares an S18 selector. The request's figure of 23 is the count when the request was written.

## Evidence

- `build_s18.py --check` exited 0, `identical`.
- `check_s18.py --rev cd5958b` exited 0, 121 checks, no failures.
- `verify_scratch.py /Users/sb/code/opensip-ai/opensip --rev cd5958b` exited 0, as in ruling 6.
- CINV recount: 45 commands, 44 whose last step is `render`, `agent-serve` steps `['query']`.

## Non-blocking observations

**NBO-1.** INV5's `Cancellation.phase` description still defines after-settle as every required step having reached a terminal outcome. LD-5 does not store an O signal there. M4's invocation successor should carry RF-1's output-returned conjunct when it restates that description.

**NBO-2.** S-OP-2 r6:653 still sets 100 ms "on cancellation" and 200 ms on normal exit. Row O applies the cancellation drain only when the decided envelope is `interrupted`. O1 should carry that qualifier.
