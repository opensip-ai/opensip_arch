I'll recheck the two corrected Phase 4 vectors against current law and the actual retained records, including scopes/Coverage without facts and measured syntax-run fields.Successor vectors now retain scopes, Coverage, and claimed syntax-run measurements. I’ll hash-verify the bundle, then recompute joins and RC/matrix fields from those records.I’ll write an independent recheck that recomputes C/H/joins and RC/matrix fields from the retained records, without treating claimed `ok` values as evidence.I'll pick up the Phase 4 recheck from the existing checker, run it against the retained records, and write the deliverables from measured results rather than claimed grades.The checker is in place. Next I’ll read it against the successor vectors, original clauses, and prior self-audit so the run is independent rather than a replay of claimed grades.I’ll inspect the corrected vectors, original RC/matrix laws, and identity joins next so the checker is driven by retained records rather than claimed `ok` flags.I’ll extract remaining vector structure, RC-2/Coverage schema, and store identity joins so the checker can be run against actual retained bytes.I’ll tighten identity, payload, and RC-2 joins so a missing body-language parse cannot pass as an empty `all()`, then run the checker.The checker admitted both IDs. I’ll inspect the measured joins, hashes, and body-identity fields so the write-up doesn’t rest on claimed `ok` flags.Measured joins hold. I’ll write the recheck report, owner mapping, and JSON from those results, treating the typescript/rust prose mismatch as a should-issue rather than a clause failure.**Verdict: `PHASE4_DATA_ADMITS`**

Same-origin recheck after the Phase 4 self-audit withdrawals. The two corrected standalone vectors now retain the original observables. This is not a new origin, not a whole-Run test, and not whole-foundation ACCEPT.

## Prior withdrawals

| ID | Self-audit | Now |
|---|---|---|
| `R-COUNT-CLASS-ATTEMPT` | withdrawn | **executed-pass, closed** |
| `R-CODE-VS-DATA-MATRIX` | withdrawn | **executed-pass, closed** |

Both close as existing-law reconstructions of successor retained records. Neither was a missing or contradictory kit recipe. Other Phase 4 grades (`R-RELATION-RUNG-TABLE`, `R-ENUM-VS-RESOLUTION`, `R-ADVERTISED-MODE-PATHS`) keep prior scoped standing only.

## What was independently re-derived

**Count/class/attempt.** Snapshot `snapshot2:3547d9e93bf52f7900e712df6b96ec6658c57aba848bab68a8ebd2ec1e87a97e`. All six vectors have subject-scope + CoverageResultV3. C/H, payload digest, schema stock, store membership, and RC-0/1/2/6 were recomputed; claimed `ok` was not used.

- Fact-absent Coverage: `absent.ts` not in snapshot, and empty subjects/`subjectCount=0`, both still RC-1 `not-applicable`
- RC-2 on `imports@resolved-target`: complete (0 unresolved), incomplete (`unresolved-module-specifier` count 1), not-attempted (`stageTerminal=null`)

Negative RC-0/RC-6 controls have no retained scope/Coverage records and stay **notReached**, not executed refusals.

**Code vs data.** Kit matrix cells, grammar `classLaw`, and BLV enum `{typescript,javascript,rust}` were applied to measured syntax-Run fields.

- syntax-code: `selectedGrammarIds=["rust"]`, `syntaxClass=code`, BLV member, two clones facts at `normalized-body-hash`, framed body-identity `languageId=rust`, clones Coverage complete
- syntax-data: `["json"]`, `data-document`, json not in BLV, zero clones facts, clones Coverage `unknown` / `language-tier-unsupported` / `capability-missing` (unavailable disclosure, not a complete empty clone result)

**Should-issue (does not refuse):** exhibit prose says “selected typescript code grammar”; measured grammar is rust. Finding `FD-SHOULD-CVD-APPLICATION-PROSE-TYPESCRIPT-VS-MEASURED-RUST`. Evaluated on measured fields.

## Input hashes

Successor manifest SHA `0db360733a100cc56161de13389aa801f74d111b7b94b2c45a8925ce79c5017f` matches. Kit manifest `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8`. All five successor files match the manifest. syntax-code is unchanged vs this origin’s original store; syntax-data changed (`00fce98f…` → `2c4f1950…`).

Reproduction:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-phase4-recheck.v1/output/phase4_recheck.py
```

Written only under that `output/` directory: `foundation-phase4-recheck.md`, `foundation-phase4-recheck.json`, `phase4-recheck-results.json`, `phase4-owner-mapping.json`. Inputs were not mutated. Cited stores remain raw property checks, not whole-Run admission.
