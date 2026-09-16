# A5 review: root-consumer24-js-options.v1 (JavaScript option and universe-flag derivation)

**Standing.** Substantive review by the same actual Claude coauthor. This is not independent acceptance, integration or qualification. Root's A5 directory was only read; the patch was not copied into or applied to my source38 tree. Any amendment is proposed separately in `a5-review/`.

**Verdict: CORRECTIONS REQUIRED.** The direct-option default and the two flag formulas are right, and I accept them. Two substantive defects and one editorial one need an amendment before integration.

## Inputs verified (p00)

- `README.md`, `changes.diff`, `changes.json`, `check_reference.py`, `probe.cjs`, `compiler-observations.json` and `compiler-custody.json` were hashed at the start and are unchanged at the end (p04).
- **Compiler custody.** `compiler/lib/typescript.js` (`f3165207…`), `package.json` and `LICENSE.txt` match `compiler-custody.json`.
- **Changed files.** The two after-files match `changes.json` after-hashes, and both before-hashes equal the source38 manifest.
- **Not repeated.** No download and no rerun of the 32 direct-option checks. The 20 new cases below run the retained compiler bytes offline, on in-memory files.

## Accepted

- **Direct default.** A `tsconfig` with `checkJs: true` and no `allowJs` has effective `allowJs=true`. This matches TypeScript 5.6.3 `getAllowJSCompilerOption` and root's 32 direct rows; the model change at `native_evidence_model.v2.py:2219-2220` implements it.
- **Flag formulas are consistent at every boundary I checked.**
  - `jsAdmittedToProgram = honoredOptions.allowJs AND len(jsRootFiles) > 0` and `jsDiagnosticsEnabled = honoredOptions.checkJs`.
  - These are the formulas already in `typescript_mode` (`:2239`) and in the context/universe agreement `universe_context_field_faults` (`:2488-2489`).
  - The resolved-input and typed-context schemas require both options as booleans: `TypeScriptUniverseV2ResolvedInputs` (`native-evidence.schemas.v2.json:3370-3375`) and `TypeScriptHonoredOptionsV1` (`:6154-6158`). So "effective, materialized booleans" matches the closed records.
  - A field disagreement refuses `native.universe-context-field-mismatch:<field>`, as the prose says.
- **Zero JS roots.** `checkJs`-only with no JS file gives `allowJs=true`, `jsAdmittedToProgram=false`, `jsDiagnosticsEnabled=true` (compiler row 2; root's model gives the same, `receipts/a5-cases.json` extra `tsconfig-checkJs-only-no-js`).
- **Explicit `allowJs=false` with `checkJs=true`.** The effective values stay `false`/`true`, and the compiler reports option diagnostic 5052 (root rows 3, 11, 19 and 27). Refusing to rewrite `false` to `true` is right.
- **Standing claims.** The compiler is supporting evidence rather than a toolchain pin, completeness is not implied, and no payload schema bytes change.

## Corrections

### A5-C1 (substantive): configuration inheritance is applied in the wrong order relative to the jsconfig default

Root's law is:

> an explicit `allowJs` value wins, including `false`. A jsconfig entry defaults it to `true` … Apply configuration inheritance before these defaults.

TypeScript 5.6.3 applies the jsconfig default **per configuration file, beneath that file's own options, before inheritance**:
- `convertCompilerOptionsFromJsonWorker` starts each file's options from `getDefaultCompilerOptions(configFileName)`, which is `{allowJs: true, …}` for a basename `jsconfig.json` (`typescript.js:42796-42802`);
- `extends` then merges with the file's own options winning: `ownConfig.options = assign(result.options, ownConfig.options)` (`:42581`).

So an inherited `false` does not beat a jsconfig node's default, and a base named `jsconfig.json` passes `true` down. Existing native law makes this reachable: "A jsconfig entry extending a shared base remains a jsconfig program" (`native-evidence.md` §2, line 1197). The retained graph's node `kind` uses the same exact basename rule.

**Counterexamples** run with the retained compiler (`receipts/a5-extends.json`; node 24.16.0, TypeScript 5.6.3, custody re-verified):

| Entry | Base | tsc `allowJs` / `checkJs` | Root law |
|---|---|---|---|
| `jsconfig.json` `{}` | `base.json` `{allowJs:false}` | **true** / false | false |
| `jsconfig.json` `{checkJs:true}` | `base.json` `{allowJs:false}` | **true** / true | false |
| `jsconfig.json` `{}` | `base.json` `{allowJs:false, checkJs:true}` | **true** / true | false |
| `tsconfig.json` `{}` | `shared/jsconfig.json` `{}` | **true** / false | false |

Each row was run with and without a JS file, and when `true` the JS file is a program root. Controls that agree with both laws:
- a jsconfig entry writing `allowJs:false` over a base writing `true`;
- a tsconfig entry over a base named `jsconfig.json` that writes `false`;
- inherited `checkJs:true`, and an entry that overrides it with `false`;
- inherited `allowJs:false` with an entry's `checkJs:true` (diagnostic 5052);
- an entry's `allowJs:true` over a base writing `false`.

**Result over all 52 retained compiler rows** (root's 32 plus these 20): root's law disagrees on 8, and the amended law disagrees on 0 (`receipts/a5-amendment.r2.json`).

### A5-C2 (substantive): a retained native case still encodes the old default

`native-cases.v2.json` case `ts-tsconfig-without-allowjs-excludes-js` (line 9313, feedback F11) is unchanged by the two-file patch. It expects `tsconfig {checkJs: true}` to give:
- `languageMode=ts-tsconfig`;
- `jsAdmittedToProgram=false`;
- `programRootFiles=["src/b.ts"]`.

Root's corrected model returns `js-allowjs`, `true` and `["src/a.js", "src/b.ts"]` (`receipts/a5-cases.json`; source38's model agrees with the stale case). The native checker was not run here, but that case can no longer pass against the corrected model. Dependent selectors are `native/README.md:101` (F11 row) and the retained `native-evidence-report.v2.json:403,1183`, which root or the native coauthor regenerates.

### A5-C3 (editorial, pre-existing, in the row A5 rewrote): the `ts-tsconfig` mode row omits jsconfig

The row recognizes only `tsconfig.json` and states `configOrigin=tsconfig`. A `jsconfig.json` entry that writes `allowJs: false` selects `ts-tsconfig` with `configOrigin=jsconfig`, both in the model (`receipts/a5-cases.json` extra `jsconfig-explicit-allowJs-false`) and under the §2 `configOrigin` derivation.

## Proposed amendment (not applied anywhere)

**Diff:** `a5-review/proposed-amendment.r2.diff` (sha256 `e86be974a3add6b5d209969ad78d0959ba6390c1f35423016400956a453df31a`, 184 lines), against root's A5 after-bytes. The amended copies are in `a5-review/amended.r2/`.

| File | Root A5 after | Amended |
|---|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | `e4319c64…` | `68184d04f6465c42e6841d57bbf00671dee14452c3b56d09ae675561435568d2` |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `1194d905…` (= source38) | `f382d81abdbe4ebd495d1a699cb6ad188b323f67893e9bcd1b3466baa0f81c36` |

**Changes:**
1. **Law.** Every graph node of kind `jsconfig` supplies `allowJs=true` as if written in that node unless it writes `allowJs`. Inheritance then applies, with a node's own options over its bases and later `extends` entries over earlier ones. Only after that does an `allowJs` value win (including `false`); otherwise `allowJs` derives from effective `checkJs`. The two reachable consequences are stated.
2. **Mode row.** `ts-tsconfig` covers `tsconfig.json` and `jsconfig.json` entries with effective `false` (a jsconfig entry only when it writes `false`), and `configOrigin` is derived from the entry.
3. **F11 cases.**
   - The stale case becomes `ts-tsconfig-explicit-allowjs-false-excludes-js`, with explicit `false` + `checkJs:true`.
   - Three cases are added: `tsconfig-checkjs-only-admits-js`, `tsconfig-checkjs-only-without-js-roots` and `jsconfig-explicit-allowjs-false-excludes-js`.
   - The edit is a byte-preserving splice: every other byte is kept, and the parsed document equals the intended one.

**Checks** (`receipts/a5-amendment.r2.json`):
- The amended law agrees with all 52 compiler rows.
- All five `typescript_mode` cases of the amended file agree with root's A5 model.
- Against source38's model, both `checkJs`-only cases fail, so the new cases distinguish the old default from the new one.

The model needs no change: it has no `extends` input, and root's README already disclaims inheritance.

**Merge note.** The native coauthor edits other sections of the same two files; root merges. If the stale case is renamed, `native/README.md:101` also changes and the native report must be regenerated.

## Observation (not a correction)

The prose says existing configuration and input admission remain required for explicit `false` with `checkJs=true`. I found no existing owner that routes compiler option diagnostic 5052, or option diagnostics in general, to an admission refusal or a deficiency. As written, such a universe is admitted with its effective values. That is not wrong for the flags law, but "existing admission" names nothing specific for this diagnostic. Root may want to name the owner or record it as a limit.

## Failed attempt preserved

`receipts/a5-amendment.*` (exit 1) re-serialized `native-cases.v2.json`, which does not round-trip through `json.dumps(indent=1)`. Its output (`a5-review/amended/`, `proposed-amendment.diff`) is kept but superseded. `a5_amendment_b` reran the exact source with a byte-preserving splice.

## Limits

- A bounded set of 20 in-memory `extends` shapes, each with one base, no `extends` arrays, no `compilerOptions` inheritance beyond these two options, and no `files`/`include` interaction.
- The TypeScript version is supporting evidence, not an OpenSIP pin.
- The native checker and global groups were not run.
