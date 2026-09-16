**Disposition: CLARIFICATION_PROPOSED.** The owners don't conflict and nothing in semantics, identity or admission needs to change. But the enumeration contract's prose makes it easy to copy the config or Cargo marker into `programEntry` on a `default-unit` binding. Frozen41 matched its manifest (12912 members, 0 missing, mismatched or extra), and the five relevant source files match it byte for byte.

## What the owners say, and where
- **Default bindings use null.** This is stated only in the schema description of `AvailableProgramBindingV1.programEntry`: "U-1 default uses null; admission derives the actual U-1 marker/synthesized entry and compares it to retained `TypeScriptConfigGraphV1.entryConfigPath` (the graph entry need not be null)".
- **The actual entry lives on the native side** (`native-evidence.md` §2.2). For a TS/JS default, `entryConfigPath` is the unit's marker path, which is non-null; it is null only for a synthesized config.
- **The contract text invites the mistake.** "`programEntry` path or `null` (U-1 default / synthesized)" (§1 `:24`) reads as "null only when synthesized". Combined with §2.2, a producer would write `"tsconfig.json"` into `programEntry`.
- **The refusal key isn't published.** `ENUMERATION_BINDING_PROGRAM_ENTRY` appears only in the reference model.
- **One sentence is wrong for `syntax-only`.** §1 `:21` calls the default "one `tsjs`/`rust`/`syntax-only` unit per directory by marker precedence". Syntax-only has no marker: it is backed either by the U-9 zero-config fallback unit (`markerPath: ""`) or by no unit at all.

## Each case separately
| Case | `programEntry` | Actual retained entry |
|---|---|---|
| TS/JS default, `tsconfig.json`/`jsconfig.json` marker | null | `entryConfigPath` = marker path (non-null) — highest risk |
| TS/JS default, `package.json` (synthesized) | null | `entryConfigPath` null, no nodes |
| TS/JS explicit program | the selected config path | `entryConfigPath` = that same path |
| Rust default | null (`Cargo.toml` is a unit marker, not an entry) | the universe H |
| Rust explicit | not a complete program key; the universe H distinguishes it | the universe H |
| Syntax-only default | null (no marker exists) | the syntax universe H |
| Unavailable bindings | the schema allows a path or null; no owner states a value | — |

For unavailable bindings I added no rule; that stays open for the owners.

## Proposed patch
The patch is `clarification.patch` (sha256 `2ccef46a…`) and touches only `enumeration-contract.v1.md` §1. The base equals frozen41 bytes (`ae4523a2…`) and the result is `a4b6be3c…`.
- **§1 `:21`:** say accurately which unit backs a default binding, including the syntax-only cases.
- **§1 `:24`:** replace the misleading parenthetical with a pointer to the new rule.
- **New construction rule**, stated as a restatement that adds no rule:
  - `programEntry` identifies which program of the cell a binding is; it is not the compiler entry.
  - Three records must agree for one binding: the binding itself, the retained native inputs, and the native universe and context. Producers never copy the unit's `markerPath` into `programEntry`.
  - The six-row table above.
  - A non-null default binding is refused, never normalised into an admissible one.
  - Unavailable bindings are unaffected.
- **Example:** a `packages/web` cell. The default binding has `programEntry: null` and graph entry `packages/web/tsconfig.json`. An explicit binding has `packages/web/tsconfig.build.json` as both `programEntry` and graph entry. The wrong default encoding is shown with its refusal.

## Consequences and limits
- **Unchanged:** identity and admission. The schema, native documents and model are untouched.
- **Repin needed at integration:** the contract's bytes are pinned by five `source-pins` files. `check-enumeration.v1.py` only hashes the file and checks none of its text.
- **Not run:** no checkers, suites, pin updates, planning work or new controls. Model code is cited as evidence only.
- **Open for owners:**
  - what `programEntry` should be on unavailable bindings;
  - what an explicit Rust `programEntry` path means;
  - the schema says explicit TS/JS programs are non-null, but I read in the model code that it doesn't refuse a null explicit binding. I didn't test that.
- **Hash index scope:** `hash-index.json` also hashed four pre-existing harness files in the runtime (`launch.py`, `process.json`, `prompt.md`, `public-events.jsonl`). I didn't create or read them.

Files are in `/private/tmp/opensip-design-corrections/claude-program-entry-clarification.v1`:
- review.md
- review.json
- clarification.patch
- delta-manifest.json
- hash-index.json
- receipts/
- work/
