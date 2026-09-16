Diagnosis complete. `diagnosis.md` and `diagnosis.json` are in the new runtime.

## Custody
Frozen33 manifest matches `1cf3db70…`; **all 12 899 rows verified byte-exact** (736 764 309 bytes, 0 mismatched/missing). One untracked `__pycache__` `.pyc` compiled by cpython-**3.14** — my interpreter is 3.12.13 with `-B`, so not mine.

## Where the disagreement moved
Transport and structural admission ADMIT on all five. `executionDeficiencies`, `evaluationInputRefs`, `executionInputsDigest` **equal on all five**, and predicate-proof counts agree — the blind19 execution-account layer is clean. First refusal is `compare_complete_replay` at `evaluator_replay_model.v3.py:59`, which **masks** the proofBundleId, evidence, seal and run replay joins: unestablished for all five.

**One counting correction to root's path list:** rust-partial's 36 deficiency field differences are, at set level, **one substitution of 4 records** plus re-sorting (8 of 12 shared verbatim). And the 33 `witnessDigest` differences reduce to exactly two witness fields — `coverageIds` and `deficiencies`; nine other fields never differ.

## Six root causes
| | Finding | Class |
|---|---|---|
| RC-1 | Sufficiency view omits `clones→declares@syntactic`; loses `coverage-unknown` | **Consumer violated explicit law** (atom contract L88) |
| RC-2 | Outgoing scope pairing finds nothing → 19 spurious `uncovered-expected-source-subject` | Consumer deviation (L74; **all inputs were in its own export**) |
| RC-3 | `missing-relation-coverage` where bindings exist | Consumer deviation, **settled on its own retained plan** |
| RC-4 | Composite `scopeIds` empty, not union of children | **Consumer violated explicit law** (composition L121) |
| RC-5 | `count-at-most` indeterminate → **4 findings suppressed** | Downstream of RC-2/RC-3 |
| RC-6 | `matchingImportCount` 0 vs 1 | Independent consumer deviation |

RC-4's decisive detail: the reference's value equals the union of the **consumer's own** children's scopeIds on all 6 nodes — they agree on every leaf.

## Surface
**S-1** I re-ran the token control on final20's own bytes rather than inheriting root's v19 result: the aliases persist, the frozen machine FAULTs at index 2 (`P3-34`, OpenUniverse, no disclosure) while final20 claims DONE/complete; changing only the token list completes. **S-2** is narrower than "still `req-7f3a1c`" — the consumer *did* correct the surface in its new probe (ADMITs), but left the old vector retained, and the two publish **different** generic keys. **S-3** multistep availability/aggregate termination: absent from retention, undischarged. **S-4** schema-only ≠ semantic joins. **S-5** query execution blocked; I did not remint.

## Source33
**No design change is demonstrated as required.** One clarity candidate only (outgoing `selector-unbound` vs `missing-relation-coverage` predicate, stated for incoming at L76) — not the cause of anything here. No stage-count conformance claim.

**Honest gaps:** I did not read consumer20's implementation (classifications rest on outputs vs published law); the charter was not read in full; root's other three blind19 controls remain **unconfirmed for final20**; my p8 commitment column is a probe artifact proving nothing; and **`consumer-b.v20/final-public-artifact-manifest.json` does not exist** at the path named — I used `output/**` and hashed everything I read.
