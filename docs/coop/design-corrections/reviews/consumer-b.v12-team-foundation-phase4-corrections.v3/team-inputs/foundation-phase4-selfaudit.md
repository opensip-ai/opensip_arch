# Phase 4 self-audit

**Verdict: `PHASE4_DATA_INCOMPLETE`**

Same-origin follow-through on this reviewer's five Phase 4 `executed-pass` grades. Original charter paragraph and requirement kinds only. Not a complete Run, not whole-foundation ACCEPT, not product qualification. The bounded trace successor recheck remains historical.

Two of five prior grades are **withdrawn** because they exceeded the retained evidence. Three stand on measured fields.

## Charter clause map

> Derive the complete registered relation/rung applicability table. Derive state-dependent count/class/attempt rules and apply them to retained scopes and Coverage even when no fact is present. Verify code-versus-data capability distinction against the published matrix and body/normalizer laws. Enumeration completeness is distinct from resolution completeness; do not invent a resolved rung for file facts. Every advertised mode must have a representable analysis path; document the chosen grammar.

| Clause | ID | Kind | Prior grade | Now |
|---|---|---|---|---|
| complete registered relation/rung applicability table | R-RELATION-RUNG-TABLE | standaloneCanonicalVector | executed-pass | **stands** |
| apply count/class/attempt rules to retained scopes and Coverage even when no fact is present | R-COUNT-CLASS-ATTEMPT | standaloneCanonicalVector | executed-pass | **withdrawn** |
| code-versus-data against published matrix and body/normalizer laws | R-CODE-VS-DATA-MATRIX | standaloneCanonicalVector | executed-pass | **withdrawn** |
| do not invent a resolved rung for file facts | R-ENUM-VS-RESOLUTION | standingRule | executed-pass | **stands** |
| every advertised mode has a representable analysis path; document chosen grammar | R-ADVERTISED-MODE-PATHS | standingRule | executed-pass | **stands** |

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-phase4-selfaudit.v1/output/phase4_selfaudit.py
```

Comparisons: `phase4-selfaudit-results.json`. Source map: `phase4-source-map.json`.

## What the prior checker actually tested

From `independent-checker.py`, not from ID labels:

- **Relation table:** exhibit `ladder` / `subjectKind` / `universeRule` / `anchorClass` vs kit registry; `nRelations==13`; `fileLadder==[enumerated]`.
- **Count/class/attempt:** `rc_derive` on `vectors[].input` scalars `{relation, resolution, factsPresent, unresolvedEdgeCount, stageTerminal, examinedExhaustive}` compared to claimed `derived`/`expected`/`observed`. No subject-scope or Coverage record required.
- **Code vs data:** grammar-registry `classLaw` string equality, language lists, `clones@normalized-body-hash` membership vs two booleans. Matrix cells and body-language-version unused. Syntax Run fields unused.
- **Enum vs resolution:** five cited fact H-frames, `relation` and `resolution` only.
- **Mode paths:** mode list equals `matrix.languageModes`; `analysisPath` string equality to a hardcoded map; `representable` must be true.

## Grades in detail

### R-RELATION-RUNG-TABLE — stands

Kit `x-opensip-relation-registry` has 13 relations and 17 `(relation, rung)` pairs. Five pairs are RC-1 resolved rungs (`calls@resolved-callee`, `imports@resolved-target`, `reachability@from-resolved-calls`, `references@resolved-binding`, `types@checked`); the other twelve are not-applicable rungs.

Exact exhibit fields compared: `ladder`, `subjectKind`, `universeRule`, `anchorClass` for every relation. All match. `file.ladder` is `[enumerated]` only.

Not treated as missing original observables: exploded pair rows, `coverageTotality`, `snapshotJoins`. Those are extra columns, not a new Run.

### R-COUNT-CLASS-ATTEMPT — withdrawn

**Unexecuted original clause:** apply the rules to **retained scopes and Coverage** even when no fact is present.

Observable: vectors applying the rules to scopes/Coverage with and without facts.

What the artifact actually retains, keys only:

- `vectors[].input.relation`
- `vectors[].input.resolution`
- `vectors[].input.factsPresent` (boolean)
- `vectors[].input.unresolvedEdgeCount`
- `vectors[].input.stageTerminal`
- `vectors[].input.examinedExhaustive`
- claimed `derived` / `expected` / `observed` / `ok`

No `subject-scope` record (kit required fields include `snapshotId`, `relation`, `resolution`, `subjects`, …). No `CoverageResultV3` / `ViewEntryV3` (kit required fields include `coverage`, `resolutionCompleteness`, `examinedUniverse`, `closedWorld`, …). Artifact key walk found **zero** scope-like or coverage-like keys.

Current-law on those scalars still holds: `file@enumerated` is `not-applicable` / `attempted=false` with `factsPresent` true or false; `imports@resolved-target` with zero unresolved edges, complete terminal, exhaustive examination is `complete` / `attempted=true`; one unresolved edge is `incomplete`. That is measured correctness of a **different** object than the original clause named.

The fact-absent case is only `factsPresent: false`, not a Coverage entry over an empty examined scope.

Prior `executed-pass` inferred sufficiency from scalar equality and the boolean. That exceeded evidence.

Not invented: testing every registered pair, RC-6 as a new case, or a sealed Run. A standaloneCanonicalVector could retain Coverage/scope records without being a Run; this one does not.

### R-CODE-VS-DATA-MATRIX — withdrawn

**Unexecuted original clause:** verify against the **published matrix** and **body/normalizer laws**. Observable: **matrix application cited on syntax Runs** and a table vector.

What the artifact retains:

- selector `native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry` (not `native-capability-matrix.v2.json`)
- copied `classLaw` text
- `codeLanguages` / `dataLanguages` lists
- booleans `jsonHasNoBodyIdentity`, `typescriptHasClones`
- frozen store **paths** plus a prose note

Current-law on the grammar table still holds: code languages `{javascript, rust, typescript}`, data-document `{json, markdown, toml, yaml}`; json capabilities do not include `clones@normalized-body-hash`; typescript capabilities do. `body-language-version.languageId` enum is `{typescript, javascript, rust}` and does not contain `json`. The exhibit never names that enum.

The published matrix `clones-fact` × `syntax-only` cell is `SUPPORTED-DESIGN` with note “grammar-bearing languages only”. That cell is **not in the vector**. Syntax Run stores are cited by path; the vector retains no measured `relation` / `deficiency` / `nativeCause` / payload fields from those stores. `jsonHasNoBodyIdentity` is a boolean.

Prior `executed-pass` treated grammar-registry string equality plus two booleans as matrix and body/normalizer verification. That exceeded evidence.

Not invented: a new language mode, data-format syntax facts the kit says do not exist, or full Run admission of the cited stores.

### R-ENUM-VS-RESOLUTION — stands

Standing rule: do not invent a resolved file rung; file facts stay on `enumerated`.

Tested fields on each cited H-frame: `domain`, `relation`, `resolution`.

| Store | cited fact2 | Independent relation | Independent resolution |
|---|---|---|---|
| syntax-code | `852404c1…a717` | file | enumerated |
| ts | `af864a7d…f4a3` | file | enumerated |
| rust | `61b48e7d…f853` | file | enumerated |
| syntax-data | `97e82756…95ac` | file | enumerated |
| rust-partial-clones | `8376fa81…d863` | file | enumerated |

Membership census of **all** fact H-frames in those five stores (not Run admission): each store has exactly one `relation=file` frame, all `enumerated`, zero non-enumerated. The five cited IDs are those five file facts, not a cherry-pick among many.

Kit `file.ladder` remains `[enumerated]`. No resolved file rung invented.

Limitation: stores stay unverified for full Run admission. Coverage totality is not demanded here.

### R-ADVERTISED-MODE-PATHS — stands

Advertised modes from `native-capability-matrix.v2.json languageModes` are exactly the six rows in the table. `representable: true` was **not** used as proof.

Each `analysisPath` was checked for registered domain names:

| Mode | Context domain registered | Universe domain registered | Path contains both |
|---|---|---|---|
| ts-tsconfig | `native.context.typescript.v2` | `native.semantic-universe.typescript.v2` | yes |
| js-allowjs | same | same | yes |
| js-synthesized | same | same | yes |
| rust-cargo | `native.context.rust.v2` | `native.semantic-universe.rust.v2` | yes |
| rust-cargo-prepared | same | same | yes |
| syntax-only | `native.context.syntax.v2` | `native.semantic-universe.syntax.v2` | yes |

Chosen grammar names `SyntaxGrammarBundleV1`, `TypeScriptNativeContextV2`, `NativeContextV2` exist as `$defs` in `native-evidence.schemas.v2.json`. No new language mode.

## Missing vs contradictory norm

No missing or contradictory kit recipe for these clauses. The incompleteness is **unexecuted original observables** in the retained standalone vectors, plus this origin's over-grade, not a gap in current law.

## Limitations

- Frozen stores unverified for Run admission/replay.
- Phases 0–3 and the trace successor recheck were not reopened.
- S-\* author-process custody remains external from the prior review.
- Consumer input records were not repaired or reminted.
