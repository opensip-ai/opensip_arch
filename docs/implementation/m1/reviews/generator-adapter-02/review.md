# M1 generator adapter review 02 (corrections)

**Verdict: changes-required.** R1–R4 are resolved. There are two new small
required findings, NR1 and NR2. This is still a development-trusted-host
adapter: **not hermetic**, not product integration, not M1 acceptance. The A1
and A2 items remain open; fixing the four required findings does not close them.

## Pins

- Manifest `40c3c4a7…f2701ab` verified before and after all probing. All 79
  files match, with none unlisted.
- Candidate-02's generator (`ec6bb9d8…`, links only libSystem), node, rustfmt,
  python, four dylibs and the 140-file TS tree all match the closure. `.pnpm`
  holds only typescript@6.0.3.
- All 28 `source-map.json` architecture pins hash-match the architecture
  checkout and equal the implementation bytes.

## Independent checks

- **Baseline:** `validate-schemas` checked 586 original refs, and the 8
  outputs show no drift. `test_generation` passes 18 tests and
  `test_dependencies` passes 9.
- **Dependency fixture:** it equals real `cargo metadata --locked --offline`
  for root dependencies, targets and features, all resolve nodes, packages
  and lock.
- **Round-01 harness, ported:** 46 probes plus an M25c redo. All expectations
  are met; M23 is informational.
- **New probes:** 12 adapter P-series probes, 21 real-cargo guard probes, and
  a consumer-workspace feature probe.
- **Binaries:** candidate-01 and candidate-02 generators were built from
  identical pinned sources and lock. They have different hashes but produce
  identical outputs.

## Inherited findings

| ID | Disposition | Evidence |
|---|---|---|
| R1 | resolved | M03a–d and P1 (nested) are refused. P2 (nested `$id`) is refused by the runtime before the generator runs. P9 (reformatted runtime declaration) and P11 (tampered validator) are refused. No writes. |
| R2 | resolved | M09 is refused. |
| R3 | resolved as an invocation guard | M28 and M28b are refused, and no asserts remain. P4 (`sitecustomize` replacing `sys.flags`) gets past it; that is classified under A1 as entrypoint trust. |
| R4 | resolved | D03 dev-dependency is refused. Inactive target, `cfg(any())` and optional declarations are refused, as are default-features and root feature changes. See NR2. |
| A1 | open | N1 (library list self-declared), S1 (entrypoint self-verification), P4. Native libraries are verified then loaded later; no confinement. |
| A2 | open, new evidence | Non-reproducible rebuild from identical sources. There is still no binary/source provenance join. |
| A3 | partial | The exact deniedRefs set is bound (M07 refused). Subpaths are not; see NR1. |
| A4 | resolved internally | The source map is pinned and cross-checked (M05, P6, P7 and M08 refused). A consistent three-way rebind (P8) is still accepted; see NA3. |
| A5 | resolved | M10 is refused. |
| A6 | partial | Direct declarations are bound on every target. NR2 is open. Transitive edges are checked for one target per run, and dependency build scripts have no recorded review. |
| A7 | open | Child stdout still precedes the summary. |
| A8 | partial | New tests were added. There are still no stub-executable `generate()` refusal tests. |
| A9 | resolved | Only TS 6.0.3 is materialized (140 files). |
| A10, A11 | open | Single recipe; Homebrew toolchain identified by hash. |

## New required findings

**NR1 — supersession is exact-ref only.** P5 adds the entry point
`native…:v2#/$defs/HelloV3/properties/protocolMajor` and rebinds only the
options digest. `--write` accepts it, and `…ReviewerHelloV3ProtocolMajor` is
generated into `report.ts` and `evidence.rs`.

*Correction:* in `validate_options` and `flatten`, refuse entry point refs and
`$ref` targets that equal a denied ref or start with that ref plus `/`. Add a
test.

**NR2 — declared root feature table is unbound.** D14 adds
`[features] reviewer-rc = ["serde/rc"]`, which is inactive in this workspace,
and the guard passes. A consumer workspace enabling that feature resolves
`serde` and `serde_core` with `rc`.

*Correction:* add a `subjectDeclaredFeatures: {}` policy row, require
`root['features']` to equal it, and add fixture and real-metadata negative
tests.

## Advisories

- **NA1:** Python `convert()` strips nested `$id`/`$schema` without
  comparing them. P12 shows that with the runtime check neutered, a rebase is
  accepted. Add the owner and dialect equality check for defense in depth.
- **NA2:** `report.ts` embeds the raw schemas, and `SchemaRegistry.matches(ref)`
  accepts any ref, including unselected ones (P3) and superseded HelloV3.
  Route to the TS runtime/report owner to restrict it to selected entry
  points.
- **NA3:** A consistent registry + options + source-map rebind (P8) is a
  review-only control. Add an `--architecture` verification of the
  source-map pins.
- **NA4:** Extending the runtime `known` set with an applicator that neither
  visitor descends (P10) opens a hole. Add a test that every known applicator
  is traversed.
- **NA5:** `validate-schemas.cjs` writes `schema-runtime.cjs` into the
  generator input directory. Use a separate scratch directory.
- **NA6:** Owner-mapping data (`source-map.json`) is pinned in the tool
  closure, which mixes tool identity with data ownership.

## Remaining before a hermetic selected recipe or product integration

1. Fix NR1 and NR2 with tests.
2. **A1:** eliminate or snapshot the native formatter closure. Anchor
   entrypoint and interpreter trust outside the closure they verify, and add
   effect confinement.
3. **A2:** establish generator build provenance through a recorded build
   identity or a verified reproducible rebuild.
4. Make the offline provisioning lane explicit and verified.
5. Add stub-executable `generate()` tests (A8) and clean machine-readable
   output (A7).
6. Close the protocol obligations, plus the separately pending inventory
   successor and design-lock decisions. No authority is inferred from lock3.

Evidence is in `logs/`, with the probe scripts in `work/`. All mutations ran on
copies inside this directory.
