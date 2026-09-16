# Advisory: native universe binding (syntax first, then compiler)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded owner/API note for `bind_*_universe`. **Not acceptance. Not full Run. Not frozen09 review. Not runtime02.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-universe-binding-boundary-01/review`. Live, frozen, and private product were not edited.

Live lock **10 inventory / 15 contract** (inventory v12 selected). Selected native `e6784aa1…e2b9`, identity `619d6e3c…41e6`, current identity-v3 `311c1feb…b68f`, current native-v2 schema `e5834d37…7773`. Overlay still must not load historical `native_evidence_model.v2.py` or historical native schema `2d37b810…` by filename.

## Local universe-owner vs Plan/Run/execution

| Layer | What it decides | What it is not |
| --- | --- | --- |
| `bind_syntax_universe` / `bind_typescript_universe` / `bind_rust_universe` | Universe record agrees with **already-admitted context bytes**, named retained nested records, and (TS/Rust) snapshot inventory | Plan membership, grant/`prepare-code`, pruned-tree law, fact/coverage, compiler execution |
| Identity `admit_frame` + Plan loop (`identity_model.py` 1588–1743) | H-frame, nested fetch, `NATIVE_CONTEXT_SET_JOIN`, languageMode request, grant prepared-resolution, `sourceUniverse` identity | `ReplayedRun` |
| `close_run` | Complete evaluator replay | This slice |

`bind_*` docstrings: **before PlanId**; nothing executes cargo/tsc/parser/filesystem. `SourceUnitOwnershipV1` is a trusted producer observation: passing `source_unit_ownership_faults` “still proves nothing about the real repository.”

Do not mint ADMIT from a caller flag, a matching `nativeContextId` string alone, or a `FramedCandidate` shape.

## Closed obligations

### Common (all three `bind_*`)

Inputs: `universe`, `admission`, `context` (`retained` / `snapshot_inventory` required for TS/Rust; **accepted but unused** for syntax).

1. `validate_native` on the universe def (`SyntaxUniverseV2ResolvedInputs` / `TypeScript…` / `Rust…`).
2. Copy `admission["refusals"]` into the result (a refused context cannot bind as ADMIT).
3. `admission.language` and `admission.domain` match the universe language (`native.native-context-language-mismatch:…`).
4. `universe.nativeContextId == admission.nativeContextId` else `native.universe-context-binding-mismatch`.
5. `context is None` → `native.universe-context-not-supplied` (never ADMIT).
6. **Recompute** `native_identity(contextDomain, contextDef, context)` and require equality with `admission.nativeContextId` else `…context-bytes-are-not-the-admitted-ones`. Identity is `H(domain, C(record))` (`native_identity` line 276), not raw SHA of JSON, except TS nested **records** below.
7. Result `sourceUniverse` is that H digest **without** `sha256:` (`identity_model.py` 1737 compares it to the frame digest).

**Root minimum syntax (correct):** resolve the named context **frame**, **re-run** `admit_native_context` on retained descriptor + closure trees, **forbid caller ADMIT**, then `selectedGrammarIds`.

`SyntaxUniverseV2ResolvedInputs` required: `nativeContextId`, `resolutionAttempted` **const false**, `schemaVersion` const 2, `selectedGrammarIds` (**minItems 1**, unique, utf8 order). Empty selection is not expressible.

After context bytes match: `selectedGrammarIds ⊆ {g.grammarId for g in context.grammarBundle.grammars}` else `native.syntax-grammar-not-in-bundle:<id>`. Subset, not equality. No nested records, no snapshot paths. `retained`/`snapshot_inventory` omission is **not** a syntax refusal (signature parity only).

### TypeScript (after syntax; needs nested owners)

Identity-v3 universe row `nestedRecords`: `tsconfigGraphHash` → `retainedAs: configGraph` (canonical-record blob, **raw SHA-256 of C(graph)**, not H). Context row `nestedRecords`: `nodeModulesLayoutDigest` → `retainedAs: nodeModulesLayout` (nullable, same raw-SHA rule).

Identity merge at bind: `{**context_retained, **universe_retained}` (`identity_model.py` 1733–1735). Helper keys **match** those `retainedAs` names (`configGraph`, `nodeModulesLayout`).

`typescript_universe_retained_input_faults`:

- missing `configGraph` → `native.universe-retained-input-missing:configGraph` (**no skip**)
- `typescript_config_graph_digest(graph) == universe.tsconfigGraphHash`
- graph node paths == `context.configProjection.configGraphPaths`
- each node path+sha in snapshot inventory (`native.universe-source-mismatch`)
- `typescript_config_graph_faults`: kind from **exact basename** (`config_node_kind`; `tsconfig.build.json` is `other`; no case fold); extends edges; reachability; cycle; synthesized-with-nodes
- `configOrigin` **derived** from entry node kind (`typescript_config_origin`); asserted universe value must match (`native.universe-context-field-mismatch:configOrigin`)
- layout vs `context.nodeModulesLayoutDigest`: digest None ⇒ no layout and not `nodeModulesInReadSet` (else `unselected` / field-mismatch); digest set ⇒ layout required, identity match, `nodeModulesInReadSet` true
- `programRootFiles` / `jsRootFiles` inventoried

`universe_context_field_faults` additionally ties languageMode / allowJs / lockfileKind / synthesized flags to context bytes. Exact tsconfig vs jsconfig spelling is **not** decided there; it needs the retained graph.

Omitted `retained` or `snapshot_inventory` → `native.universe-retained-inputs-not-supplied`, never ADMIT.

### Rust (after nested H-owners present)

`retainedAs` that the helper reads: `dependencySourceSet`, `unifiedFeatures`, `preparedOutputSet`, `sourceUnitOwnership`. Those names **match** universe (and overlapping context) `nestedIdentities`. Required vs optional:

| Key | If universe id is None | If universe id is set |
| --- | --- | --- |
| dependencySourceSet, unifiedFeatures | n/a (ids required on universe) | missing → `…-missing:…` |
| preparedOutputSet | extra retained → `…-unselected:preparedOutputSet` | missing → `…-missing:` |
| sourceUnitOwnership | extra → `…-unreferenced` | missing → `…-missing:` |

No blanket skip. Identities are **H** (`sha256:` + `C.identity(domain, record)`), not raw SHA.

Also: lockfile/crate roots inventoried; `contextAgreementFields` on the identity row (`dependencySourceSetId`, `unifiedFeaturesId`, `preparedOutputSetId`); rustflags; `configProjectionSha256` vs `cargo_config_projection_identity(context["configProjection"])` (H of the **record**, not `projectionSha256` file digest); `executionCapableResolution == (preparedResolution != "none")`; cfg sets **add** to `context.baseCfg`; prepared toolchain/cfgSetId/kind.

**Grant** `prepare-code` / `read-import` is **Plan** `preparedResolutionGrantOperations` after bind (`identity_model.py` 1741). Local bind must not require a grant. Body-dialect / `BODY_LANGUAGE_OWNERSHIP_*` is **fact** law, not bind: a universe can bind without ownership; clones later refuse.

## retainedAs vs helper (mismatches)

**Aligned:** TS `configGraph` / `nodeModulesLayout`; Rust `dependencySourceSet` / `unifiedFeatures` / `preparedOutputSet` / `sourceUnitOwnership`.

**Do not invent `retainedAs` for `configProjectionSha256`.** The rust universe nested identity has `form: bare-hex`, `domainSet: native-nested`, **no `retainedAs`**. `bind_rust_universe` never reads `retained["configProjection"]`; it hashes `context["configProjection"]`. Local diagnostics should pass the **context descriptor**, not a extra retained key.

**Full `open_run_closure` still `admit_frame`s that nested H-frame** (CargoConfigProjectionV2 + file `projectionSha256` blob). Local bind ADMIT does **not** prove that walk. Don’t skip it in Plan closure; don’t demand it in the bind `retained` map.

**TS vs Rust digest kinds:** `tsconfigGraphHash` / `nodeModulesLayoutDigest` are raw SHA of canonical JSON (`CONFIG_GRAPH_DOMAIN_NOTE`). Rust nested ids are H-identities. Do not feed one into the other.

**Duplicate rust nested ids on context and universe:** same `retainedAs` names; merge prefers universe. Safe if `contextAgreementFields` hold; still re-run identity on the retained record, don’t trust the id string.

## Interface (evaluator → identity primitives)

Keep bind in **evaluator** (port `bind_*` + helpers). Identity stays `RetainedInputs` / `FramedCandidate` / blob/get. No identity→evaluator.

```text
bind_named_universe(inputs, universe_digest, budget)
  -> Result<BoundUniverse, Unavailable | Invalid { causes } | Limit>
```

- Load universe H-frame (identity).
- Resolve `nativeContextId` (`sha256:` + 64 hex) to a **context frame**; missing → **Unavailable**.
- Rebuild closure trees from retained `closure2:` objects; **re-run** `admit_native_context`. Do not accept a caller `admission` struct as authority.
- If context refusals nonempty → **Invalid** with those causes (not skip, not Unavailable).
- Syntax: `bind_syntax_universe(universe, admission, context)` (pass dummy retained/snapshot only if keeping Python arity).
- TS/Rust: build `retained` **only** from `retainedAs` keys after fetching nested canonical/H records; missing required key → Invalid `…-missing:`; extra unselected → `…-unselected:`.
- Snapshot inventory from the **fact/plan snapshot object** only when this function is used inside Plan closure; for local diagnostics the caller supplies the inventory list explicitly (same as Python). Do not implicit-trust “any retained snapshot.”
- Preserve **Limit** from traversal budget; do not fold into Invalid.

Compiler branches **after** nested owners exist (configGraph layout fetch, rust H-nested). Syntax must not wait on those.

## Compact vectors (syntax now; TS/Rust once nested fetch exists)

**Syntax +**

- Context bundle grammars `{ts, rs}`, universe `selectedGrammarIds: ["rs"]` (utf8-sorted if more), `resolutionAttempted: false`, context bytes recompute to `admission.nativeContextId`, language `syntax`. Expect ADMIT.

**Syntax −**

| Recipe | Expect |
| --- | --- |
| Caller `admission` with `refusals: []` but context recompute differs | `…context-bytes-are-not-the-admitted-ones` (ignore caller ADMIT) |
| `selectedGrammarIds: ["nope"]` | `native.syntax-grammar-not-in-bundle:nope` |
| Empty `selectedGrammarIds` | schema/validate refuse (`minItems: 1`) |
| Typescript admission bound to syntax universe | `native.native-context-language-mismatch:syntax-universe-bound-to-…` |
| `context is None` | `native.universe-context-not-supplied` |
| Context frame blob missing | Unavailable |
| Unsorted `selectedGrammarIds` | native `x-opensip-order` / validate refuse |

**TS − (nested)** missing `configGraph`; graph hash ≠ `tsconfigGraphHash`; `configOrigin: tsconfig` while entry basename is `jsconfig.json`; layout blob present while `nodeModulesLayoutDigest` is null (`unselected`); digest set, layout missing; `DOM` path kind must not use `lib_name_fold` (kind is exact basename, not case-fold).

**Rust − (nested)** missing `dependencySourceSet`; `preparedOutputSetId` null but retained prepared present (`unselected`); ownership id set, `unitId` ≠ `H(native.compilation-unit.v1, UnitIdentityV1)`; `configProjectionSha256` ≠ H(context projection **record**); cfg row drops a `baseCfg` atom.

Do not run old 26931/375k corpora here.

## Traps

1. Overlay: `identity_model.py:41` still names `native_evidence_model.v2.py`; `validate_native` needs **current** native schema `e5834d37…`, not coop historical `2d37b810…`.
2. Don’t put bind inside identity.
3. Don’t treat Plan `nativeContextDigests` membership as context ADMIT (id set join is later).
4. Don’t skip missing nested keys because “syntax doesn’t need them.”
5. Don’t use `char::to_lowercase` / rustc 17 for config **kind** (kind is not `lib_name_fold`).
6. Don’t equate `projectionSha256` (file) with `configProjectionSha256` (H of projection record).
7. Don’t require grant or body-ownership at bind.
8. `bind_*` copies context refusals: a failed context owner is universe Invalid, not a silent ADMIT.

## Verdict

**NOT ACCEPTANCE.** Syntax bind is the coherent next evaluator slice: named context frame, re-run context owner, no caller ADMIT, `selectedGrammarIds` subset of the bundle. Compiler binds wait on nested retained owners with explicit missing/unselected/mismatch causes.
