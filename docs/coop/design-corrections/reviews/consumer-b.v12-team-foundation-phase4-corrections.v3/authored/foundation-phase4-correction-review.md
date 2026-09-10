# Foundation Phase 4 correction

**Verdict: `READY_FOR_INDEPENDENT_RECHECK`**

Same original B12 kit-only author. Other-runs-corrections.v6 is complete. P6 withdrew two prior Phase 4 passing grades because the original observables were unexecuted. Those two standaloneCanonicalVectors are corrected here. This is not whole-consumer ACCEPT, not product qualification, and not a new complete Run.

team-inputs.json `61e4b2391cb7fce9cb42ac3e4bad933d31dec6cf59151abb552d90c6dde6e170` match. Four P6 reports PASS. Kit 80/80. Trace successor `TRACE_DATA_ADMITS` remains historical; already-corrected traces were frozen.

## From-scratch command (exit 0, second produce hash-identical)

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/output/scripts/phase4_count_class_and_matrix.py
```

Derivation re-reads the exported count-class store and re-applies RC-0/RC-1/RC-2/RC-6. Saved `ok` flags are not the source of truth.

## R-COUNT-CLASS-ATTEMPT (was withdrawn)

Original clause: apply state-dependent count/class/attempt rules to **retained scopes and Coverage even when no fact is present**. Scalar `{factsPresent:false}` was not that observable.

The vector now retains snapshot, enumerator closure, universe preimage, subject-scope H-frames, coverage2 envelopes, CoverageResultV3 payloads, and fact2 records (`foundation/count-class-attempt.store.json`).

| Case | Retained records | Derived |
|---|---|---|
| file@enumerated with fact | scope `src/a.ts` + file fact + complete Coverage | RC-1 `not-applicable` / `attempted=false` |
| file@enumerated fact-absent | scope `absent.ts` (not in snapshot) + no file fact + complete Coverage | same RC-1; fact-free examined partition |
| file@enumerated empty scope | subjects `[]` + no facts + complete Coverage | RC-1 + RC-6 (complete ⇒ exhaustive) |
| imports@resolved-target complete | import fact, zero unresolved-edge facts in examined set | RC-2 `complete` |
| imports@resolved-target incomplete | unresolved-edge fact whose referrer is in the examined set | RC-2 `incomplete` |
| imports skipped | `attempted=false`, count 0 | RC-2 `not-attempted` (zero count is not complete) |

Negatives: RC-6 refuses `coverage=complete` with `examinedExhaustive=false`; RC-0 refuses `unresolved-edge@enumerated`. Coverage is not labeled complete without owner inputs, counters, and classes.

New: `75fc228b…e846` (was `990d598e…6fcbc3`). Store `7b68f4a2…7d58`.

## R-CODE-VS-DATA-MATRIX (was withdrawn)

Original clause: published **matrix** and **body/normalizer** laws, with measured fields from cited syntax Runs. A path plus boolean is not matrix application.

Measured:

- Matrix cell `clones-fact × syntax-only` = `SUPPORTED-DESIGN`, note **grammar-bearing languages only**.
- `body-language-version.languageId` enum `{typescript, javascript, rust}`; `json` is not a member.
- Grammar registry: typescript bears `clones@normalized-body-hash`; json does not.
- **syntax-code** (raw property check, not full Run admission): two `clones@normalized-body-hash` facts; bodyIdentity `languageId` in the BLV enum; SyntaxGrammarBundleV1 + normalizer specification digest retained.
- **syntax-data**: zero clones facts; clones Coverage `unknown` / `language-tier-unsupported` / `capability-missing` — unavailable disclosure, not a complete empty clone result.

New: `c7fc60d1…c4cb` (was `82f85d23…c6bd`). Limit: these are raw retained-frame checks, not full Run admission of the cited stores.

## Unchanged Phase 4 artifacts

| Artifact | SHA-256 | Status |
|---|---|---|
| relation-rung-table.json | `e00260e4…0f0d` | unchanged, still valid |
| advertised-mode-paths.json | `55f38387…f3fb` | unchanged, still valid |
| enum-vs-resolution.json | `956a753f…bbc1` | **previous bytes preserved** |

Citation census: current frozen stores still have only `file@enumerated` facts (no invented resolved file rung). Cited IDs from an earlier freeze differ for rebuilt TS/Rust/syntax-data/partial stores; syntax-code `fact2:852404c1…` still matches. Refresh **not applied** so previous bytes stay. Census: `foundation/enum-vs-resolution-citation-census.json`.

## Frozen

All five Run stores, query/workflows/output-traces, and other foundation artifacts including corrected protocol3 traces: freeze `frozen-this-pass.foundation-phase4.v3.json`, **0 mismatches**. Predecessors: `preserved-failures/phase4-v3-pre-withdrawn-vectors/`.

No new language mode, extra Run, or per-language L1 demand.
