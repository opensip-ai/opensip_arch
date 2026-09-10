# Enumerator v12 coauthor integration review

**Standing.** Coauthor review of isolated successor evaluator3 joins. Not fresh-blind independent acceptance. Not product implementation. Synthetic admitted inputs; `check-replay.v3.py` does not qualify a compiler, provider, or real repository. Sidecar/incoming admission remains root-owned atom v6 work — not rediscovered here.

Enumeration unit checks (this coauthor, five owned files) are join-admission only and do **not** qualify a Run.

## A. Enumeration (owned files; implemented this turn)

Optional-unselected enumerator is now coherent:

- Schema: `SelectedEnumeratorRef` vs `UnselectedEnumeratorRef`; available bindings selected-only; unavailable may be either.
- `required=true` + unselected → `ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`.
- Non-null universe + unselected → plan schema refusal (available cannot express unselected).
- Selected missing `closureId` → structural schema refusal, not optional-unselected.
- Optional `required=false` unavailable + `reason=optional-unselected` + lawful `provider-unavailable`/`nativeCause` null + empty unavailable inventories + host extents → ADMIT.
- Host extents still compared on unselected bindings (`optional-unselected-wrong-extents` → `ENUMERATION_BINDING_EXTENT_PATHS`).
- Retired `ENUMERATION_SCOPE_EXCLUDE_ALL` removed from the live `INTERNAL_FAULTS` list (no emission). Historical v7–v11 receipts untouched.
- Checker receipt is `--receipt` / `--hashes` / `--stdout`; default `/tmp/opensip-enumeration-check-scratch/`; refuses write into historical `grok-subject-assessment.v7`–`v11`.

39 enumeration-join cases, 0 mismatches, 13/20 historical bounded. Python 3.12.13.

## B. Root integration (read-only)

Read: `evaluator_input_model.v3.py`, `evaluator_composition_model.v3.py`, `evaluator_replay_model.v3.py`, `workflows/workflows_model.v3.py`, `evaluator-composition-contract.v3.md`, actual `check-replay.v3.py`. Live run: **25 checks, passed**, standing synthetic admitted inputs / no real extraction qualification. Cases: file positive; 4 reminted same-count mutants (severity/message/parameter/citation); `two-universes-six-full-findings` (two syntax U on one inventory cell → 6 distinct subject3 findings); none/count/all-covered/nongating/disabled/budget/empty-path/glob; runtime×5; history×3; test×3. Default fixture is one syntax-only **inventory** cell (`kinds=['file','package']`) plus view(s). The suite does **not** exercise candidate-only `kinds=[]` cells, optional-unselected enumerators, omitted views, or ScopeDocument selection. Completeness cannot be inferred from it.

### Blockers (concrete disagreements / missing joins)

1. **Required candidate-only cells can look satisfied.**  
   Contract: clone producers (`clones-near`, `clones-cross-tsjs`, `kinds=[]`) retain a **separate** contract; enumeration emits **zero** inventories for those cells.  
   `reconstruct` required-execution accounting is only:
   - `cell.required and binding.universe is None` → `required-cell-unsatisfied`
   - `cell.required and inv.state != 'complete'` over **existing** inventories  
   A required `kinds=[]` cell with a non-null universe has **no inventory locators**, so neither arm fires. `executionDeficiencies` stays empty and a pass verdict treats required execution as satisfied. That is a false satisfied required execution cell. The 24 replay checks never construct such a cell.

2. **Required-execution loop still owns clone cells at all.**  
   The same loop will mark `required and universe is None` on a candidate-only cell as *this evaluator's* `required-cell-unsatisfied`. If clone execution is out of evaluator3's contract, that is false ownership (indeterminate/fail in the declarative evaluator for a producer it does not inventory). Complementary to (1).

3. **No view input totality.**  
   Imports: `input_refs` domain=import must equal `plan.importIds` (`EVALUATOR_IMPORT_INPUT_TOTALITY`).  
   Views: taken only from `input_refs` domain=view; facts/scopes/coverages are the union of those views. There is no join that the selected views equal owner-admitted / execution-plan view outputs. Replay then rebuilds `semantic-evidence.viewIds` from the **proof's** `evaluationInputRefs`, so an omitted view is stable under replay. Missing inventory pointer is structural; missing view is silent empty native evidence.

4. **`no-covering-program` is inventory-shaped, not available-binding-shaped.**  
   Contract complete-empty needs a covering **available** binding. Reconstruct `relevant` is every inventory locator whose kind is the rule primary and whose **cell languageMode** maps to the rule's portable domain — including **unavailable** inventories (`universe=null`). Those yield `incomplete-inventory`, not `no-covering-program`. A domain/kind that exists only as `kinds=[]` never appears in `relevant`, so a file/symbol rule against a Plan that only requested candidate-only clones reports `no-covering-program` while the required clone cell may still false-satisfy (1). Applicability is not resolved here (contract: policy construction); an already enabled rule with no covering **available** program is incomplete, but unavailable vs absent are collapsed inconsistently.

5. **Duplicate `required-cell-unsatisfied` for one required unavailable inventory cell.**  
   First loop (U=null, no inventory ref) and second loop (inv not complete, with inventory ref) both append. `cset` does not collapse them (`inputRefs` differ). Two execution deficiencies for one cell.

### Same-Plan selected U

Available binding U is joined: enumeration requires the U record in the caller map and `native.semantic-universe.<engine>.v2` via `universe_domains`; reconstruct repeats domain vs `MODE_DOMAIN[cell.languageMode]` (`EVALUATOR_CELL_UNIVERSE_DOMAIN`). Bindings with U not in owner `nativeUniverses` fail that domain get. This is the Plan-selected U join for **available** bindings. It does not by itself fix (1) or (3). Rule covering uses cell `languageMode` domain; two programs of that domain both cover. `two-universes-six-full-findings` is that path for two syntax U on one inventory cell (6 findings). It is not a candidate-only or view-totality control.

### Not new discovery (root-owned / pending)

- Target-attribution sidecar and incoming-search admission: reconstruct copies refs into `atom_inputs` with planId/sourceFactId duplicate checks only; atom v6 owns occupancy/unknown. Not restated as a new finding.
- Package `packageManifestPath` on subject3: M3 + reconstruct + compose already add the field for kind=package.
- `source-syntax-invalid` is forwarded from partial inventory into enumeration deficiencies.

### Other concrete notes (not claimed complete from tests)

- Reconstruct mints population only from inventory rows; unavailable/optional-unselected empty inventories mint no subjects (agrees with enumeration). Optional-unselected is not in the replay fixture.
- ScopeDocument parameter key `workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1` matches the registry row; `parameter_row_of` hashes **document** bytes (one row today). Replay fixture selects no ScopeDocument. `glob_match` / `in_scope` come from workflows v3 re-export of v1.
- Compose verdict: any `executionDeficiencies` (including the duplicates in (5) or false-satisfy absence in (1)) drives indeterminate if no fail. Budget-exhausted appends another execution deficiency; replay covers that path only for the inventory fixture.
- Actual `check-replay.v3.py`: 25/25 passed on this machine. Synthetic admitted graphs with fully reminted mutants. They do not contain candidate-only required cells, omitted views, or optional-unselected enumerators. Completeness cannot be inferred from that suite.

## C. Disposition

| Item | Status |
|---|---|
| Optional-unselected enumerator (schema+model+controls) | Settled in the five owned files |
| Live `ENUMERATION_SCOPE_EXCLUDE_ALL` | Removed from internal fault list |
| Checker historical-folder overwrite | Default scratch; v7–v11 refused; this receipt explicit `--receipt` v12 |
| False-satisfied required `kinds=[]` cells | **Blocker, root-owned reconstruct** |
| View input totality | **Blocker, root-owned reconstruct/replay evidence join** |
| no-covering-program vs available covering / candidate-only | **Blocker, root-owned** |
| Duplicate required-cell-unsatisfied | **Defect, root-owned** |
| Sidecar/incoming | Pending atom v6 (known) |
| Full Run qualification from enum unit checks | **Not claimed** |
| Independent acceptance of evaluator3 | **Not claimed** |
