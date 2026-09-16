Done. The corrected design/reference successor is applied, controlled, and checked.

## What changed — 3 files in `/tmp/opensip-design-corrections/atom-cause-successor.v1/source`

Custody re-verified after every edit: 12 899 files both sides, nothing added or removed, exactly these three differ from frozen33.

| path | before → after sha256 |
|---|---|
| `foundation/atom-evaluation-contract.v1.md` | `681c3da7…` → `0a3fe11d…` |
| `foundation/atom_model.v1.py` | `2023f8d8…` → `b05642b2…` |
| `foundation/check-atoms.v1.py` | `b7ae967e…` → `77786e88…` |

**Contract §4** gained five blocks, placed as directed (cause derivation beside the partition law, shared sufficiency beside its dependency paragraph): completeness-result independence from truth; ascending `scope2`/`coverage2` selection order; the six-step outgoing derivation with each cause's `universe` and the exact refs each return carries; the incoming derivation and its absence of any early return; and the deterministic `DEPENDS_ON` view with the `coverage-unknown` carrier rule. No `[DECISION]` placeholders, no new cause tokens, no new public fields.

**`atom_model.v1.py`** got two `return sorted(...)` lines. Root's suspicion about `_depends_chain`/`_conservative_entry`/`_build_sufficiency_view`/`_build_attestation_view` was correct: `reconstruct` builds the maps from Python *set* comprehensions, `-I` ignores `PYTHONHASHSEED`, and two folds are first-wins over that order. Before: 24 processes gave two deficiencies and two nativeCauses; after: 20/20 identical while the input dict order still varied 6 and 5 ways.

## Controls — 70 → 76 cases, 76/76 pass

The 70 pre-existing results are byte-identical to frozen33's. Run against **both** models, the split is:

- **`test_dep_fold_carrier_is_first_partition_in_selection_order` — discriminating.** Fails on frozen33 (`no-program-unit` where the evidence says `lockfile-missing`), passes corrected, at both endpoints.
- The other five pass on both models. They are publication controls, and I want that stated plainly rather than dressed up: they find no defect and were not meant to — they stop the prose and the reference drifting apart.

## Checks and Run evidence

Seven focused affected checks, all exit 0. Re-run from the frozen33 tree read-only: **all six non-atom checks produce byte-identical stdout across the two models**; only `check-atoms` differs, by exactly the six added cases.

The retained reference Run replayed 8× before and 8× after the correction — same `run3:ecb44874…`, same proof `c18f225f…`, 3 findings, 3 predicates. **I am not claiming complete Run parity:** one retained Run plus the Runs those six checks build internally; the full corpus and the six broad groups were not run.

## Things you should see

1. **15 pin entries go stale** across 5 ledgers (`pins/files` indices 1069, 1070, 1073). No ledger edited — enumerated in `changed-file-handoff.json`.
2. **`ViewEntryV3.coverage` is a two-member enum** (`complete`, `unknown`), and the native model says the producer boundary schema-validates first. Yet `_conservative_entry` ranks an intermediate `partial`, and several pre-existing checks build `coverage: "partial"` entries. Unreachable on admitted input and no conclusion turns on it, so I reported it and left it alone rather than touching unrelated retained checks. I did fix the *contract* prose to cite the published enums.
3. The defect is **latent** — shown by controlled multi-process probes, not a Run diff.
4. Every token the amendment relies on is in the 169-file normative-only kit outside this contract (`tokensOnlyInThisContract: []`). The looser first attempt at that probe is retained.

Deliverables: `assessment.md`, `assessment.json` (`cc4cece5…`), `changed-file-handoff.json` (`e2027822…`), before/after images, and 25 receipts including the failed attempts. No acceptance claimed.
