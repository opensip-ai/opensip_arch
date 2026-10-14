# Review request: M3-L r6, a delta round on M3-L r5

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-provider-protocol-l-r6/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory (`~/Library/Application Support/OpenSIP`), signing keys or held trees. Do not use other panes and do not delegate. Permitted: read-only hashing, JSON parsing, reading sources, and read-only Git queries. You may re-run control L-C1 in the stage: `python3 -I -B /tmp/opensip-implementation/provider-protocol-l-r6-stage/docs/implementation/m3/provider-protocol-l/evidence/wire_identities.py --check`. It reads only the staged mirror.

## Lead note: why you

M3-L r5 was accepted in review by GROK2 on 2026-10-04 (`docs/implementation/m3/reviews/grok-provider-protocol-l-r5/`), and Grok reviewed r2 to r4. "Review and effect" sends a delta round to the same reviewer. Neither GROK2 nor Grok is available any longer, and the owner directed on 2026-10-13 that Codex review from now on. r6 records the substitution (r6 changes, row 7). Judge whether its wording is lawful. You have not reviewed this law before, so read r5's "Review and effect", item 9 and the gate in full as context. Your review is still on the diff. A Grok request for this round was prepared but never answered. Ignore it.

## Subject

- Stage: `/tmp/opensip-implementation/provider-protocol-l-r6-stage`
- `subject.json`: 3328 bytes, SHA-256 `837c25f18a4621e91bb03f81c2dd66efa3dfaee8cd34f8c3a163c6831f007b47`, 6 members plus 10 architecture context pins. Rehash every member, and the context pins in the architecture repo at HEAD `4229df9e73b604fd1c5c02d12f811ed0e0f4f272`.
- **The law:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, which is r6 and byte-identical to `PROPOSAL-r6.md`. **The diff:** `r5-to-r6.diff` (`diff PROPOSAL-r5.md PROPOSAL.md`). Review it on the diff only, as "Review and effect" requires, while reading enough of r5 to judge each change in context.

## What to review

r6 answers a lead finding: a cycle in L's gate.
- L-G1 and "Before L takes effect" need the S-M delta round to fill every `⟨SM-n⟩`, including r5's SM-11 to SM-14.
- Their values need inputs that only units after day 0 bind: C4a's Rust stage list and requested keys; G3's emission recipe, census symbol kinds and batching; and the worker (G1a and G2).
- Day 0 is L in effect.

r6 fills those four figures in two parts. The S-M delta round fills a decomposition. A **fifth delta round**, owed after effect and not a condition of it, completes them.

1. **The cycle.** Check each claimed dependency against its cited source:
   - `M3-PLAN-r10.md:79`, `:80`, `:306`, `:311`, `:481`, `:497`, `:525`, `:538-540`;
   - MC8:1185;
   - MD5:546 and :551;
   - RL README:140, and "What S-M must measure" and "Cascade and cross-law items";
   - RPP:118, :137-150, :152 and :600-606;
   - NE:591-598.

   Is every value r6 defers dependent on an input that a unit after day 0 binds? Is anything deferred that S-M could measure lawfully now?
2. **The S-M round's part** (item 9, "When SM-11 to SM-14 are filled"). Is it exact, and free of any invented stage, key, emission factor, batching, census kind or scratch count? Are the SM-11 quotient rule (only where coverage is exact), SM-12's host part, SM-13's decomposition (site counts labelled as not candidates, exact fixed overheads, closed formulas with owned parameters unset), SM-14's formula and S_eff's first term coherent with item 9's other rules and forbidden substitutes?
3. **The fifth round.** Is a round owed after effect, outside "L in effect", lawful under "Review and effect" and against "What dependents may rely on"? Is its change set closed: only SM-11 to SM-14 values and the records item 9 says they set, with no protocol constant, item or outcome (A) to (C)? Is the interim F-4 fault statement right?
4. **Scope.** Does r6 change anything beyond these:
   - item 9's SM-11 to SM-14;
   - the text that states the rounds and L in effect, which is the header, "Review and effect", the gate's L-G1 cell and "Before L takes effect", the S-M rows of "What depends", and "Not claimed";
   - the r6 table, history, short names and standing direction;
   - X17, R16 and the r6 reversal flag?

   Item 13 and L-C1 must be unchanged; `l-c1-check.log` must show a pass.
5. **X17.** Does it route the sequence correctly to M3-PLAN, M3-C (X-RL-C2), M3-G (X-RL-G2) and RUST3-LIM's X-RL-L3, deciding none of them?
6. **The reviewer substitution** (row 7, and "Review and effect").

Product, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native admission is not an extra gate on outside-product S-M experiments. This is law text only: no S-M figure is filled, L-G1 is not met, and L is not in effect.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), `nonBlockingObservations` (array), and exactly these expected fields with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "837c25f18a4621e91bb03f81c2dd66efa3dfaee8cd34f8c3a163c6831f007b47",
  "gateCycleReal": true,
  "sMRoundPartInventsNoOwnedInput": true,
  "completionRoundAfterEffectLawful": true,
  "completionRoundChangeSetClosed": true,
  "onlyItem9SM11to14AndRoundTextChanged": true,
  "item13AndLC1Unchanged": true,
  "protocolConstantsUnchanged": true,
  "outcomesAtoCUnchanged": true,
  "reviewerSubstitutionLawful": true,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
