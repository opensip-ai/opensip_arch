# TS/JS `unitKind`: author correction of the native U-4b.2 identity law

Coauthor origin f5617310-c7c7-4d85-acdd-31370f220944.

This is an architecture, design and reference correction only. It is not a product change, commit, push, acceptance or readiness claim. Only this runtime was written: LIVE, frozen39, the root successor and every other runtime are untouched. No pins, planning, policy files or reports were regenerated, and no private logs or blind artifacts were read.

## Custody

- **Manifest.** The LIVE manifest `docs/coop/design-corrections/reviews/candidate-subject.v39.json` was read and verified: sha256 `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`, 3188557 bytes.
- **Members.** All 12909 members were verified in `/tmp/opensip-design-corrections/candidate-subject.v39` against manifest hash **and** length, with 0 missing, not-regular, hash, length or extra mismatches. Bytes read equal `totalBytes` (737605070).
- **Capture.** `work/source` is an independent regular-file copy (distinct inode, nlink 1, re-hashed). Receipt: `receipts/frozen39-verify-and-capture.json`.
- **Final custody** (`receipts/final-custody.json`, `ok: true`): the manifest was re-verified; the capture has 12909 files with 0 new, 0 missing and 0 pycache; exactly the 5 touched files differ from frozen39; each before-image equals its frozen39 member; and 12904 members are unchanged.

## Diagnosis (independent)

**Owning text.** `native-evidence.md` §1.4 publishes the closed `WorkspaceUnitV2` with `unitKind: cargo-workspace|cargo-package|ts-program|js-program|syntax-only`.
- U-4b opens: "`UnitMembershipV1` enters `PlanId` through `membershipDigest`, so every choice below is identity and none is left to an implementation".
- U-4b.2 assigns the Rust `unitKind` (and `recognizerId` equal to it).
- For TS/JS it assigns the marker, the mode (U-1's, via the §1.2 mode table) and `recognizerId`, but **never `unitKind`**.
- U-9 assigns the fallback `syntax-only`.

The schema enum admits both TS/JS kinds for any TS/JS unit. The only decision is `native_evidence_model.v2.py:3948`: `ts-program` if the mode is `ts-tsconfig`, else `js-program`. So a reader following the normative text can choose `ts-program` for an allowJs `tsconfig.json` project (its marker is a tsconfig), and the model chooses `js-program`. That yields two `membershipDigest`s, and therefore two `PlanId`s, for one project.

**Enforcement, checked rather than assumed.**
- `admit_unit_roots` (native) explicitly does not look at `unitKind`.
- Enumeration admission, which Run closure reaches through `evaluator_input_model.v3` → `admit_enumeration`, runs `_membership_order_law`. That law re-derives unit order, ordinals, member roots, row projections and row decisions, but no unit field.
- The enumeration-plan schema and the security/discovery-defaults owners never mention `unitKind`.
- No other owner assigns or enforces the kind.

**Actual demonstration on the unmodified capture** (`receipts/probes/pristine.json`). Using the maintained consumer24 real-Run harness (membership mutated before it is hashed into `membershipDigest`, then a full `close_run`):
- complete Runs carrying a discovered `ts-tsconfig`, `js-allowjs` (`tsconfig.json` marker with `allowJs`) or `js-synthesized` unit close;
- **the same Runs with that unit's `unitKind` reminted to the other kind also close**.

The ambiguity is therefore admitted at Run closure, not merely latent in the text.

**Mapping choice.** I follow the current model, with no substantive reason to deviate:
- the kind is a function of the mode alone;
- `ts-tsconfig` means JavaScript files are not program roots (a TS program);
- `js-allowjs` and `js-synthesized` both admit JavaScript roots;
- the existing native cases already assert `js-synthesized` → `js-program`;
- the kind has no other behavioural consumer, so the choice is pure identity, and keeping the model's value leaves every lawful discovered membership byte-identical.

## Exact law

**U-4b.2** (TS/JS clause, added): each TS/JS unit's `unitKind` is `ts-program` exactly when its mode is `ts-tsconfig`, and `js-program` when it is `js-allowjs` or `js-synthesized`. So a `tsconfig.json` marker with effective `allowJs=true` is a `js-program` unit: the kind follows the mode, never the marker file name.

**U-4b.5** (enforcement, extended): the following refuse `ENUMERATION_MEMBERSHIP_ORDER`:
- a `tsjs` unit whose `unitKind` is not that projection of its mode;
- a `ts-program`/`js-program` kind on a unit of another family.

This is the existing internal key U-4b.5 already assigns to "mismatched projections". It is already listed in the enumeration-plan schema's `x-opensip-new-internal-faults`, so no new key and no schema document bytes change. There is no public detail code.

**One normative owner:** `native-evidence.md` §1.4 U-4b. The reference projection `NV.TSJS_UNIT_KIND` is used by `discover_units`, and the closure check `enumeration_model._membership_order_law` reads that same table; the mapping logic is not duplicated.

## Delta (`delta-manifest.json` sha 5a353d68…, `correction.patch` sha ab1826f0…, 202 lines)

| File | before sha256 / bytes | after sha256 / bytes |
|---|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | efd413891925c25629f1677e05b67c00754c5e9d1135d3f2dd18328289b14037 / 296916 | 5f3b0cced53e5e0b71e4a1eadf78c54dbca5355ed5d1011beee510af93414261 / 297359 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | 51bcab333b2f35f4e33cecf6e3581f108c440b9526ca3dbbaa14d7301cc965ca / 307748 | 6128b24a7b71fa7fa74d654ec9518a1962894c85eb51cc9a7e0fb2121ec025db / 308052 |
| `docs/coop/design-corrections/foundation/enumeration_model.v1.py` | 55a23396aefda8d1f243495c0e6acd073783be5fb4e3861b64a18485637dcc28 / 48854 | e54741c6ac46904b1c06ccaf71700611f15cd5c354ef5c2c6384e9c65361ab46 / 49298 |
| `docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` | caa602935474f6d29b65daca0348eb65c6a86243658d07c387e0e82b8e8eafdc / 61016 | 043ef86ed9c555c0f6a045356789e7b6432ac76baceb144fa8af72bdc16f7595 / 66026 |
| `docs/coop/design-corrections/foundation/check-enumeration.v1.py` | 732e0b045157c6d0e14fb0533e9259ba275166856aa734e5c4c22fdc40b021f4 / 40097 | 1356fafe2cf452b84f650b3b86ad0eebeb73d70cd7e237db0387cc9a49b208a1 / 41619 |

- **Content:** the model change is one constant plus one expression replaced by it (discovery output unchanged). The enumeration change is the closure check plus its docstring line. The checker changes are controls only.
- **Unchanged:** schema documents, native cases, the native matrix, pins, native report bytes and policy files are all unchanged.
- **Before-images** are in `work/before/`, and the edit log `receipts/edits.jsonl` has 5 rows.

## Controls and results

**Sequence.** Pristine baseline → controls only (Phase A) → pre-fix run → fix (Phase B) → post-fix run.

**New controls** (all discriminating):
- **consumer24 M3** (`check-native-consumer24-corrections.v1.py`), 25 rows:
  - the owner table equals the published closed table; its modes equal the enumeration `TS_MODES`; its kinds are members of the schema enum;
  - the law sentence is present in the normative owner;
  - `discover_units` outputs mode, kind, marker and recognizer for:
    - **ts-tsconfig**: `ts-tsconfig` / `ts-program` / `tsconfig.json` / `typescript-config`;
    - **js-allowjs via a `tsconfig.json` marker with `allowJs`**: `js-allowjs` / `js-program` / `tsconfig.json` / `typescript-config`;
    - **js-allowjs via `jsconfig.json`**;
    - **js-synthesized**: `js-synthesized` / `js-program` / `package.json` / `node-package`;
  - for each of those four: the law admits the canonical kind and refuses the reminted kind with `[ENUMERATION_MEMBERSHIP_ORDER]`;
  - the rust canonical kind is lawful; a rust unit carrying `js-program`, the fallback carrying `ts-program`, and a TS/JS unit with a non-TS/JS mode are each refused;
  - real complete Runs:
    - a published kind closes for ts-tsconfig, js-allowjs (tsconfig marker) and js-synthesized;
    - a digest-consistent reminted kind refuses at `close_run` with `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_MEMBERSHIP_ORDER`, for each of the three and for the fallback unit reminted to `js-program`.
- **Enumeration** (`check-enumeration.v1.py`): on the ts-tsconfig admission baseline, only `unitKind` is changed and `membershipDigest` is rebound. The published `ts-program` is `ADMIT`ted; a reminted `js-program` refuses with exactly `[ENUMERATION_MEMBERSHIP_ORDER]`.

**Receipts** (`receipts/checks/*`). All children were run with `/tmp/opensip-architecture-review-env/bin/python -I -B`, and every child finished.

| Run | Result |
|---|---|
| `baseline-pristine`: all 17 current evaluator children (the `run-evaluator3-checks.py` job list, run directly) | all exit 0; consumer24 183/183; enumeration 0 mismatches; workflow projection 838; query projection 204; full replay 73; native replay 31 |
| `baseline-pristine-native`: native checker, real pin gate | PASS, 380/380, pins verified |
| `probes/pristine` | canonical kinds close; **reminted kinds also close (defect)** |
| `phaseA-prefix`: consumer24 | **exit 1, 195/208**. The 13 failing rows are exactly: table; law; the 4 remint law rows; rust, fallback and non-TS/JS mode; and 4 real-Run remint rows (the Runs closed). The 12 discovery, canonical and real-Run-close rows pass. |
| `phaseA-prefix`: enumeration | **exit 1**: the reminted `js-program` was `ADMIT`ted with no refusal |
| `postfix`: all 17 evaluator children | all exit 0; consumer24 208/208; enumeration 0 mismatches (reminted refuses with exactly ORDER); every other child's count equals baseline |
| `postfix-native-gated`: native checker, real pin gate | **exit 2, PIN-MISMATCH**: its pin faults name exactly the 5 touched files; pins were not regenerated |
| `postfix-native-unpinned`: native body via the labelled driver (`PIN-GATE-BYPASSED-BY-EXTERNAL-DRIVER`) | PASS, 380/380; actual pin faults recorded |
| `probes/postfix` | canonical kinds close; reminted kinds refuse with `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_MEMBERSHIP_ORDER` |
| `postfix` integration (`check-integration.py`) | 412 passed. The first attempt ran but failed to write its report (receipt directory did not exist); rerun into an existing receipt directory. |
| `postfix-security` (unpinned security body, including `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`) | 464/464 cases, 11/11 sweeps |
| owner launchers `run-evaluator3-checks.py` and `run-reference-checks.py` | pin gates invalid for exactly the 5 touched files; no child executed; not a pass |

## Limitations and nearby observations (not repaired)

- **Pins.** The foundation, evaluator3 and native pin ledgers are stale for the 5 files. Root must rebind them and run the owner launchers and full suites. The in-tree `native-evidence-report.v2.json` was not regenerated; its content would be unchanged (380 cases).
- **Admission narrowed.** Memberships that a divergent reader of the old text would have produced (for example `ts-program` for an allowJs tsconfig project) now refuse at closure. Discovered memberships and lawful plans are byte-identical, so no identity or registered schema digest moves.
- **Key name.** The reused key's name is order-flavoured. U-4b.5 already assigned "mismatched projections" to it, and the text now names this case explicitly. A dedicated key would change the registered enumeration-plan schema bytes and the parameter-registry digest.
- **Closure scope.** Closure still does not re-derive a TS/JS unit's mode from its marker, `recognizerId` or `markerPath` from its marker, or a rust unit's `cargo-workspace`/`cargo-package` choice (which depends on manifest content the unit does not retain). Only the TS/JS kind projection, and the TS/JS kinds' family, are enforced.
- **jsconfig mode discrepancy (observed, not repaired).** The model's `discover_units` maps any `jsconfig.json` marker to `js-allowjs`. The §1.2 mode table says a jsconfig entry that writes `allowJs: false` is `ts-tsconfig`. The new `unitKind` law is keyed on the mode, so it stays consistent whichever mode the owner decides, but that mode question is a separate item for root.
- **Receipt quirk.** `run_checks.py` named its own row receipt `enumeration.receipt.json`, overwriting the checker's `--receipt` file. The checker's full report is retained in `enumeration.stdout` (run with `--stdout`), which is what these results quote.
- **Evidence strength.** The controls use synthetic fixtures and the maintained real-Run harness. They are reference evidence, not product qualification or acceptance.
