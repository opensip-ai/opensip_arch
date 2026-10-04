# I1-a — schemas, pins and generated enums (product unit with its contract successor)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **PROPOSED frozen candidate.** It needs CODEX2's review (ACCEPT-UNIT for the product change, ACCEPT-DESIGN-UNIT for this record) and root assent before selection.

I1-a is the first product unit of the accepted law M3-I1 r2 (`../PROPOSAL-r2.md`, `1eb47d1e…`), row I1-a of `../UNITS-r2.md`. Its design parent is I1-L (`../i1-l/`), bound at product main. Base: product main `5e25d04` (P0 integrated; 87 contract successors, 95 inventory successors, v135 selected). Its other dependencies, X9-6 and F8b, are integrated.

**The rule it holds to.** The two product schema sources become I1-L's accepted copies byte for byte. Everything else in the unit follows mechanically from those bytes: the registries and source maps that pin them, the generator closure, the native and atom-registry pins, the regenerated contracts, and the dependency-policy pins of the changed sources. No design choice is made here; where I1-L or UNITS is inexact, the deviation is listed below.

## What changes

`materialization-map.json` maps 15 product files on `5e25d04`. Every other tracked file is unchanged, apart from the staged `design-lock.json` row (see "Binding"). The two schema sources map to I1-L's own copies; the other 13 are copied under `product/`.

| Product file | Before | After |
|---|---|---|
| `schemas/sources/identity-v3.schema.json` | 197480, `311c1feb…` | 198423, `eb6ec957…` (I1-L's copy) |
| `schemas/sources/policy-v2.schema.json` | 26534, `b221b5ed…` | 26677, `0ff24ae6…` (I1-L's copy) |
| `schemas/source-map.json` | 28547, `6796d7ec…` | 28565, `76409db5…` |
| `schemas/admission-source-map.json` | 20049, `9ed543dd…` | 20057, `fcd0f34e…` |
| `schemas/admission-registry.json` | 17170, `595fc28d…` | 17170, `15457b75…` |
| `schemas/registry.json` | 20211, `eecde992…` | 20211, `ca65e1b2…` |
| `tools/contracts/generator-closure.json` | 68280, `bb093a9c…` | 68280, `9dc40660…` |
| `crates/identity/src/schema_registry.rs` | 26806, `82ae11b3…` | 26808, `ea3cc09e…` |
| `crates/evaluator/src/atom-registry.json` | 30466, `8f37ed00…` | 30488, `9aabc999…` |
| `crates/contracts/src/generated/identity.rs` | 283889, `af42ad22…` | 284396, `ee275003…` |
| `crates/contracts/src/generated/evidence.rs` | 1570438, `9fcce094…` | 1570759, `510cbc79…` |
| `apps/report/src/generated/report.ts` | 2167115, `90d643db…` | 2168287, `dfe3001e…` |
| `tools/contracts/dependency-policy.json` | 5199, `353c2af7…` | 5199, `f283f3a1…` |
| `tools/identity/dependency-policy.json` | 56471, `ae739105…` | 56471, `03deeac6…` |
| `crates/host/src/schema_sources.rs` | 52054, `4c0f2d36…` | 57322, `6181bcd5…` |

What changes inside them:
- **The schema sources.** I1-L's edits only: `cycle-representative` appended last to policy `Atom.op` (now `:296-304`) and to the identity `predicateProofs[].operation` and `program-predicate.operation` enums (now `:1221-1232` and `:2782-2793`); the r2 `majorLaw` sentence (now `:4986`); policy `description` (line 5); and the two lock-bound overrides that I1-L's copy carries for PIDS (predicate-matching-v2's `program-predicate` description and stage-meta's registration `law`).
- **Generation source map:** both rows' `architectureSource` now names I1-L's product copies (`../i1-l/product/schemas/sources/…`).
- **Admission source map:** the same two rows, and `registryArchitectureSource` now names this record's `schemas/admission-registry.json`.
- **Admission registry:** the identity-v3 and policy-v2 source rows and the policy-v2 alias row (`workflows/schemas/policy-document.v2.schema.json`) carry the new bytes and sha256. Byte counts keep their digit counts, so the length is unchanged.
- **Generation registry:** both `sourceSha256` values, the recipe's sorted `sourceSha256s`, and `generatorClosureSha256`.
- **Generator closure:** three of 349 rows (`schemas/source-map.json` and the two sources). The toolchain is unchanged.
- **Native pins** (`schema_registry.rs`): both `SourcePin` lengths and digests, in rustfmt's layout.
- **Atom registry:** `fieldFilterSchema` moves to I1-L's design copy `../i1-l/design/workflows/schemas/policy-document.v2.schema.json` (path, 28042, `45581464…`); `scannerIdentitySchema` takes the product identity copy's bytes and sha256.
- **Generated outputs** (`run_generation_i1a.py` with the selected rebuild-02 generator): `Policy2AtomOp`, `Identity3ProgramPredicateOperation` and `Identity3ProofBundlePredicateProofsItemOperation` each gain `CycleRepresentative` with its `Display` and `FromStr` arms; two doc comments follow the schema descriptions (`Policy2Root`, `Identity3ProgramPredicate`). `report.ts` gains the member in three unions, its embedded schema bytes and its two provenance header lines. The other five outputs are byte-identical.
- **Dependency policies:** the contracts policy's `src/generated/evidence.rs` and `identity.rs` rows, and the identity policy's `src/schema_registry.rs` row.
- **Test:** `crates/host/src/schema_sources.rs` gains `cycle_representative_is_admitted_by_current_policy_and_identity_schemas_only`. It admits the member through policy-document:2 `/$defs/Atom`, identity:v3 `/$defs/program-predicate` and `/$defs/proof-bundle`, and the three generated enums; it refuses it through policy-document:1 and `Policy1AtomOp`; four near spellings are refused everywhere; and an existing member is the control on each selector.

**No behaviour change at evaluation.** The evaluator still refuses the op at `atoms.rs:3262-3268` (`ATOM_OP`), and no pack row, policy document or fixture uses it. No hand-written code matches on the three enums.

## Parents

The twelve parents, sorted by path, are the selected architecture copies of the changed files' base bytes, plus I1-L's three copies whose bytes or paths I1-a pins:
- 468a's `evidence.rs`, `schema_sources.rs`, `schema_registry.rs`, `admission-source-map.json`, `source-map.json` and `schemas/admission-registry.json` (the copy the admission map named);
- F8b's `report.ts`, `registry.json` and `generator-closure.json`;
- I1-L's design policy-document copy and its two product schema copies.

`identity.rs`, `atom-registry.json` and the two dependency policies have no selected architecture copy of their base bytes, so they have no parent. `freeze_i1a.py` asserts each listed parent equals its file's base bytes.

## Deviations from UNITS r2 and I1-L's list

None of these is a design choice. Each is what the accepted bytes and `verify_design` require.

1. **No inventory successor.** UNITS r2 says "Inventory successor." I1-a adds no file and changes no row's meaning: every changed file is a planned row of v135, and each row's description stays true. So v135 stays selected and v136 is unused.
2. **The generator closure is a member.** UNITS and I1-L's list omit it. The closure pins `schemas/source-map.json` and both sources, and `generate_contracts.py` requires the closure's exact bytes to be an input of an accepted design unit. Its copy is `product/tools/contracts/generator-closure.json`, as in 468a and F8b. `report.ts`'s provenance header follows.
3. **The dependency policies.** `tools/contracts/dependency-policy.json` pins the generated `evidence.rs` and `identity.rs`, and `tools/identity/dependency-policy.json` pins `schema_registry.rs`. Both checkers refuse stale pins, so both are re-pinned here. (Earlier schema units, 468a among them, left these rows stale until F8a refreshed them.)
4. **One wrong line reference in UNITS r2.** `evidence.rs:38891` is the `count-at-most` arm of `Policy1AtomOp`, which does not change. The widened enum is `Policy2AtomOp` (`evidence.rs:40075` on base). UNITS's identity references (`identity.rs:4190`, `:4417`) are the `count-at-most` arms of the two widened enums, as intended.
5. **`scannerIdentitySchema.fixturePath` is kept.** I1-L says only that this pin "moves to the PIDS copy's bytes". Its `fixturePath` names a file in the reconstruction-48 reference tree, which no product code or tool reads. It is left unchanged; the reviewer is asked about it.

## Observation: policy admission between I1-a and I1-b1

Before I1-a, the policy-document:2 schema refused `cycle-representative`. After I1-a, the schema admits it, and the policy pass's `atom_law` (`policy.rs:229-331`) checks relation, rung, endpoint, evidence, subject kind and filters but not the op name. So a document whose rule uses the op with subject kind `symbol` over `imports` would pass policy admission and then refuse at evaluation (`ATOM_OP`). The law's own pack form (subject kind `file`) still refuses at the source-kind check (`policy.rs:260-289`), as UNITS says.

No path reaches this today: the release registry has zero rows, `PackSource::Supplied` always refuses, and no product source writes a policy document that uses the op (the only occurrences are the schemas, the generated enums and the new test). I1-b1, next in the law's order (I1-a → I1-b1 → I1-c), adds the op law of 2.2. This is recorded, not changed.

## Evidence

All scripts are in `evidence/` and run with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`.
- **`apply_i1a.py WORKTREE pins|policies`** applies the edits. It refuses unless every value it changes still holds its `5e25d04` value, and every JSON file round-trips through `json.dumps(indent=2)` at base. Its reports are `pins-report.json` and `policies-report.json`.
- **`run_generation_i1a.py WORKTREE OUT --write`** runs the selected pipeline with rebuild-02 after checking every closure pin, the registry joins and the build receipt, then writes the three changed outputs. Its summary is `generation-summary.json`. The public entry point cannot run before this record is selected, because the closure and the admission registry are its candidates.
- **`freeze_i1a.py WORKTREE SCRATCH`** writes the product copies, the admission-registry copy, the map, this record, the subject and the draft unit record.
- **`stage_lock_i1a.py`** appends this record's `contractSuccessors` entry to the worktree's `design-lock.json`, with `SCRATCH-I1A/` review and assent placeholders.
- **`verify_scratch_i1a.py`** runs the worktree's real `verify_design` with the placeholders served in memory. Besides passing, it asserts that HEAD's lock refuses this tree at the admission registry, that the closure and admission registry are I1-a inputs, and that the inventory chain and inheritance are unchanged.
- **`drift_scratch_i1a.py`** runs the real public `generate_contracts.generate` (write false) with the same in-memory placeholders. It must report `changed: []`.

The lane results are in the review request (`docs/implementation/m3/reviews/codex2-i1a-r1/`).

## Binding

The uncommitted worktree `/Users/sb/code/opensip-ai/opensip-i1a` carries the staged lock. At acceptance, the lead will:
1. copy the reviews in;
2. complete `i1-a-unit.json` (`ACCEPTED-DESIGN-UNIT`, the `review-contract.json` pin);
3. replace exactly the two placeholder pins;
4. run plain `verify_design` and the public `generate_contracts.py` (it must report `changed: []`);
5. commit the product and then this record.

I1-a shares the generator with X4T-c (P5-3); only one of them may be in flight against a given closure.

## Limits

- No evaluator semantics, admission law, pack row or fixture: those are I1-b1, I1-b2 and I1-c.
- No X9 harness source, crash-matrix row or required-runs file is touched.
- Development builds on macOS arm64 only. No product or release qualification.
