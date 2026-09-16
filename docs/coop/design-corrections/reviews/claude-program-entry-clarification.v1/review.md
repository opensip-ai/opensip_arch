# `programEntry` (enumeration binding) vs the actual selected compiler entry (native), frozen41

**Author:** bounded AUTHOR f5617310-c7c7-4d85-acdd-31370f220944. This is architecture and documentation clarity work only. It is **a proposal**, not independent source or application assent. Nothing was written to LIVE, frozen41 or the root successor. No consumer implementation, results or artifacts were accessed.

**Base.** `candidate-subject.v41`, manifest sha256 `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236`. All 12912 members verified (`receipts/frozen41-verify.json`: 737732367 bytes, 0 missing, 0 mismatched, 0 extra). The relevant source files match the manifest (`receipts/source-bytes.json`):

| File | sha256 |
|---|---|
| `enumeration-contract.v1.md` | `ae4523a2…` |
| `enumeration-plan.schema.v1.json` | `10627cb6…` |
| `native-evidence.md` | `66c6b82b…` |
| `native-evidence.schemas.v2.json` | `2d37b810…` |
| `enumeration_model.v1.py` | `e54741c6…` |

## Disposition: **CLARIFICATION_PROPOSED**

The owners do not conflict. The construction law is complete, but it is spread across one schema description, a native section and model behaviour. The enumeration contract's own prose is ambiguous enough that an implementer could copy the U-1 config marker into `programEntry` on a `default-unit` binding. One sentence (§1 `:21`) is also inaccurate about `syntax-only`. This is not a new semantic defect.

## 1. Owners and exact selectors

**The binding field (enumeration)**

| Selector | What it says |
|---|---|
| `enumeration-plan.schema.v1.json` `#/$defs/AvailableProgramBindingV1/properties/programEntry.description` | "TS/JS extra program: non-null LogicalPath of the selected inventoried config … **U-1 default uses null**; admission derives the actual U-1 marker/synthesized entry and compares it to retained `TypeScriptConfigGraphV1.entryConfigPath` (**the graph entry need not be null**). Rust extra programs are distinct universe H values …; programEntry is not a complete program key." This is the only explicit statement of the null-for-default encoding. |
| `…/UnavailableProgramBindingV1/properties/programEntry` | `LogicalPath` or `null`, **no description**. |
| `enumeration-contract.v1.md:21` (§1) | `default-unit` = "the U-1 default: one `tsjs`/`rust`/`syntax-only` unit per directory by marker precedence". |
| `enumeration-contract.v1.md:22`, `:58` (§1) | Explicit programs are Plan-selected bindings: "admitted universe H + context + `programEntry`". |
| `enumeration-contract.v1.md:24` (§1) | "`programEntry` path or `null` (U-1 default / synthesized)". |
| `enumeration-contract.v1.md:163` (§9) | "`programEntry` is not a complete program key (Rust cfg/features live in universe H)". |

**The actual entry (native)**

| Selector | What it says |
|---|---|
| `native-evidence.md:1319-1342` (§2.2) | `TypeScriptConfigGraphV1.entryConfigPath` "selects the root config, or is null for synthesized configuration"; `configOrigin` is `synthesized` exactly when the entry is null and `nodes` is empty. |
| `native-evidence.md:1354-1359` (§2.2) | An explicitly selected custom-named config such as `tsconfig.build.json` is an `other` entry that derives `configOrigin=tsconfig`. |
| `native-evidence.schemas.v2.json` `#/$defs/TypeScriptConfigGraphV1.description` | The same: "entryConfigPath is the SELECTED root config … null exactly when the configuration was synthesized". |
| `native-evidence.md:652-662` (§1.4 U-1) | Marker precedence: `tsconfig.json` > `jsconfig.json` > `package.json` (→ `js-synthesized`); `Cargo.toml` → `rust`. |
| `native-evidence.schemas.v2.json` `#/$defs/WorkspaceUnitV2` | `markerPath`, `unitKind` including `syntax-only`, `languageFamily` including `none`, nullable `markerSha256`. |
| `native-evidence.md:868-894` (§1.4 U-9) | The zero-config `syntax-only` fallback unit has `markerPath: ""` and `markerSha256: null`. "Mixed repositories get no fallback": a `syntax-only` cell may then be requested at an explicit root with no unit. |
| `native-evidence.md:172-179`, `:231` | `syntax-only` "has no compilation unit". |
| `native-evidence.md:206-229` | The syntax universe commits a context plus the selected grammar set, with no config graph. |

**Reference evidence only (not normative)**
- `enumeration_model.v1.py:797-812`, available bindings:
  - a non-null `programEntry` with `provenance=default-unit` refuses `ENUMERATION_BINDING_PROGRAM_ENTRY`;
  - for TS modes, `expected = programEntry if non-null else _u1_entry(unit)`, compared to `graph.entryConfigPath`.
- `:435-440` `_u1_entry` returns the unit `markerPath` for `ts-tsconfig`/`js-allowjs`, and `None` for `js-synthesized`, Rust and `syntax-only`.
- `:817-819`, unavailable bindings: a non-null entry must only be a snapshot path; there is no default-unit null check.
- `check-enumeration.v1.py:146-163, 251, 327, 409-410, 721-722`: maintained bindings use `default-unit` with `programEntry=None` (available and unavailable), and `explicit-plan-selection` with `"tsconfig.build.json"`.

## 2. Could a reader copy the marker into `programEntry` with `provenance=default-unit`?

Yes, from the contract prose alone.
- **Wording.** "`programEntry` path or `null` (U-1 default / synthesized)" (`:24`) can be read as *null only for synthesized*. Native §2.2 then says the TS default graph entry *is* the marker path, so a producer mapping `programEntry ≡ entryConfigPath` would write `"tsconfig.json"`.
- **Where the rule lives.** The null-for-default encoding is stated only in a schema description. The refusal key is published nowhere in owner prose.
- **Vocabulary.** Unit `provenance` (`DISCOVERED`/`EXPLICIT`/`DEFAULTED`, and "Plan-bound with `DEFAULTED` provenance" for `js-synthesized`) is a different vocabulary from binding `provenance` (`default-unit`/`explicit-plan-selection`), which adds to the confusion.

Per case:

| Case | Law (owners) | Risk before clarification |
|---|---|---|
| TS/JS `default-unit`, `tsconfig.json`/`jsconfig.json` marker | `programEntry` null (schema). The graph entry is the marker path, non-null (native §2.2, model `_u1_entry`). | **High**: the two fields hold different values for the same program. |
| TS/JS `default-unit`, `package.json` (`js-synthesized`) | `programEntry` null. Graph entry null, `nodes` `[]`. | Low: both are null, but "synthesized" in `:24` wrongly suggests null applies only here. |
| TS/JS `explicit-plan-selection` | non-null selected config path (schema), equal to the graph entry (model). | Low. |
| Rust `default-unit` | `programEntry` null (schema "U-1 default uses null"). No config graph; universe H is authority. `Cargo.toml` is a unit marker, not an entry. | Medium: `markerPath` is `Cargo.toml` and could be copied. |
| Rust `explicit-plan-selection` | Distinct universe H; `programEntry` is not a complete program key (schema, §9). **No owner defines what an explicit Rust `programEntry` path denotes.** | Not clarified beyond restating; no rule invented. |
| `syntax-only` default | `programEntry` null (schema). No marker: U-9 `markerPath` is `""`, or there is no unit at all. | Contract `:21` wrongly calls it a unit "per directory by marker precedence". |
| Unavailable bindings (any provenance) | Schema allows `LogicalPath` or `null` with no description. No owner prose states a value, and the model does not refuse non-null default-unit entries there. | **Not decided by owners.** This clarification adds no rule. It is reported for owners, and I did not invent a universal null rule. |

## 3. Proposed clarification (exact delta)

`clarification.patch` has sha256 `2ccef46a25b8bd4a3905352107eb9f01b9bcbd761723b3178d91f8710e4d8381` (5787 bytes). `delta-manifest.json` lists the file below; the base is byte-identical to frozen41.

| File | Base sha256 (21273 bytes) | After sha256 (24325 bytes) |
|---|---|---|
| `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` | `ae4523a224bf6e21371c5575381f661e5feda634488b692513117c236d6ee689` | `a4b6be3c69b8df89f56cf079bfe6ff8d273ec44d559c1237e7671ac8c7d52408` |

The schema, native documents and model are unchanged.

**The three edits, all in §1:**
1. **`:21`.** `default-unit` is the `tsjs`/`rust` unit U-1 yields by marker precedence. A `syntax-only` default is backed by the U-9 fallback unit (`markerPath: ""`) or by no unit.
2. **`:24`.** The parenthetical "(U-1 default / synthesized)" becomes "(see the construction rule below)".
3. **New construction rule.**
   - **Principle:** `programEntry` is the binding discriminator, not the compiler entry. The actual entry is retained natively (TS/JS `entryConfigPath`; Rust and syntax universe H) and derived and compared by admission.
   - **Obligation:** a producer builds the binding, the retained native inputs and the universe/context consistently, and never copies `WorkspaceUnitV2.markerPath` into `programEntry`.
   - **Table:** six rows (TS/JS default config marker, TS/JS synthesized default, TS/JS explicit, Rust default, Rust explicit, syntax default) with their retained entries.
   - **Non-normalisation:** a non-null `programEntry` on a default-unit available binding is not a U-1 default; reference admission refuses it (`ENUMERATION_BINDING_PROGRAM_ENTRY`) rather than normalising it.
   - **Scope:** unavailable bindings keep the schema shape, and the table adds no rule for them.
   - **Example:** a `packages/web` cell with default `programEntry: null` (graph entry `packages/web/tsconfig.json`), an explicit binding `packages/web/tsconfig.build.json` (graph entry the same path, kind `other`, `configOrigin` tsconfig), and the WRONG default encoding with its refusal.

The text explicitly restates `AvailableProgramBindingV1.programEntry` and §9 and "adds no rule". No semantics, schema, identity or admission changes are proposed, and non-null default bindings are never normalised into admissible ones.

## 4. Cross-document construction obligation (surfaced)

For one available binding, three independently owned records must agree:
1. the enumeration binding (`programEntry`, `provenance`, `nativeContextDigest`, `universe`);
2. the retained native inputs (TS/JS `TypeScriptConfigGraphV1`, whose raw hash is the universe's `tsconfigGraphHash`; Rust `DependencySourceSetV1`/`UnifiedFeaturesV1`/`PreparedOutputSetV3`; syntax grammar selection);
3. the native universe/context (`bind_*_universe`).

Today this obligation is spread across `enumeration-contract.v1.md` §1 `:24`, `:58`, the schema description, and `native-evidence.md` §2.2/§2.4/U-1/U-9. The patch states it once in §1.

## 5. Consequences and limitations
- **Identity and admission:** no change. No `EnumerationPlanV1` digest, universe H or refusal changes. The only change is contract bytes.
- **Integration:** the contract is pinned by `foundation/source-pins.v1.json`, `foundation/evaluator3-source-pins.v1.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json` and `workflows/source-pins.v1.json`, and listed in `check-enumeration.v1.py` `owned_hashes`, which only hashes it and asserts on no text. Root integration would repin; no pins were changed here.
- **References kept valid:** other documents cite `enumeration-contract.v1.md §1` for the unselected-enumerator law, which is untouched, and section numbering is unchanged.
- **Not run:** no checker, suite, pin, planning or new control. The model lines are cited as evidence only.
- **Open for owners, not decided here:**
  - the `programEntry` value on unavailable bindings;
  - what path, if any, an explicit Rust `programEntry` denotes;
  - that the schema says explicit TS/JS programs are non-null while the reference model does not refuse a null explicit binding (observed in model code, not measured).
- **Not read:** anything under `reviews/` beyond the formal manifest file.
