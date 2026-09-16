# source42 kit — law reading log and the helper checks it implies (working record)

**Custody.** Kit `consumer-input-manifest.json` SHA-256 `9c90a1e8…`, parent `f602fc7e…`, 104 members, all verified; no unlisted file.

Against my own source41 custody rows (`preserved/source41-v1/vectors/phase0-custody.json`), exactly two documents changed, and none was added or removed:
- `docs/coop/design-corrections/foundation/enumeration-contract.v1.md`
- `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md`

`charter.md` and `requirements.json` are byte-identical to source41 apart from runtime paths and kit hashes. Both changed documents were read in full. The source41 kit bytes were not read; a change is identified by reading the current text against the laws my helpers implement.

## Laws to check against the ported helpers

1. **Enumeration contract §1: `programEntry` construction rule** (lines 24-47).
   - An available `default-unit` binding has `programEntry: null`; a non-null value refuses `ENUMERATION_BINDING_PROGRAM_ENTRY`, never normalised.
   - The retained native entry is derived and compared:
     - TS/JS `tsconfig.json`/`jsconfig.json` marker: `TypeScriptConfigGraphV1.entryConfigPath` equals the unit's `markerPath`;
     - `package.json` (`js-synthesized`): `entryConfigPath` null with `nodes` `[]`;
     - TS/JS `explicit-plan-selection`: `entryConfigPath` equals `programEntry`;
     - Rust and syntax-only defaults: `programEntry` null, and the universe H is the entry.
   - The contract says this restates the schema: `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description` (line 389) reads "U-1 default uses null; admission derives the actual U-1 marker/synthesized entry and compares it to retained TypeScriptConfigGraphV1.entryConfigPath". That schema file is unchanged since source41.
   - **Own source41 defect.** My source41 TS and Rust builders set `programEntry` to `"tsconfig.json"` / `"Cargo.toml"` on `default-unit` bindings (`preserved/source41-v1/builders/ts_runs.py` line 257, `rust_runs.py` line 194), and my source41 enumeration admission implemented neither the null rule nor the entry comparison. Every source41 TS, cmp-* and Rust export carried it; to be measured on this kit before correction.
2. **Enumeration contract §1 lines 20-21: `default-unit` means at most one binding per cell, at `ordinal=0`.** A `syntax-only` cell's default binding is backed by the U-9 fallback unit. My syntax builder labels that binding `explicit-plan-selection` (`builders/syntax_runs.py` line 191), and my admission checks neither rule.
3. **Execution-inputs §3 view attribution** (line 53), in two parts:
   - (a) The candidate views are the `view` `outputRefs` of complete receipts, which §1 makes exactly the `view` members of `selectedRefs`. A `view` on `selectedRefs` but on no complete receipt refuses `EXECUTION_INPUTS_SELECTED_COVER`. My source41 HC-42 helper also drew candidates from the claimed `selectedRefs` (`ref/execinputs.py` `candidate_views`).
   - (b) Relation-column membership: the pair's resolution plays no part, so a scope at another rung of the relation's ladder is attributed. The helper already compares relation names only; to be confirmed by a vector.
### Measured before any correction (unchanged ported helpers on this kit)

- `logs/s42-original.7.from_scratch.log`: all 27 claimed positives ADMIT; the designed negative refuses.
- The rebuilt stores carry run ids identical to all 27 run ids exported by my source41 review (`preserved/source41-v1/blind-review.json#/claimedCompletePositives`). The source41 exports are therefore these exact bytes.
- Retained enumeration plans:
  - `ts-pass` and every cell: `provenance: default-unit`, `programEntry: "tsconfig.json"` (same builder for the 14 cmp-* and 3 ts-* Runs);
  - `rust-mixed` and the other Rust Runs: `default-unit`, `programEntry: "Cargo.toml"`;
  - `syntax-code` and the other syntax Runs: `explicit-plan-selection`, `programEntry: null` for the U-9 default.
- The unchanged admission refused none of these.

4. **Execution-inputs §8 `build_manifest`.** Receipt `outputRefs` capture the explicit returned views on the view stage whose `producerClosure` each carries. Row `viewDigests` are the attributed subset; a returned view no row owns stays captured. My builders follow this after HC-42; to be re-measured.
