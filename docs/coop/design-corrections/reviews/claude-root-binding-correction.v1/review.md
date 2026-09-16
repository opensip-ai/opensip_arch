All work is complete and verified. Here is the report.

---

# Authored bounded correction — F-04, Q-2, F-05, F-06

**Standing:** author-assisted reference work by a reviewer acting as author. This is **not** independent acceptance, **not** blind reconstruction, **not** product implementation or readiness authorization. I authored these changes; I do not accept them.

**Bindings (re-verified independently this turn):** candidate25 manifest `fa8cdc79…a536d`, **12869/12869** files hash-matched; author package manifest `c533aa6a…16c4`, **97/97** hash-matched. Re-verified **after** all work: candidate25 **0 modified**, author package **0 modified**. Every write went to `scratch/`.

**Deliverable:** `scratch/output/` — 9 patches, 13 changed full files (`output/files/src25/`), 1 helper successor, `evidence-manifest.json` (158 files, sha256 `51b18f3f076b5b0976af6345bcf9ffbb1d6aa7a51204f2d7cf72244af4bed255`), `REPRODUCE.md`.

## 1. What the CanonicalPath regex actually enforces

I inspected it rather than assuming. `CanonicalPath` is `^(?!/)(?!.*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])` with `minLength: 1`. Executed matrix:

| value | CanonicalPath |
|---|---|
| `''` | reject (minLength) |
| `'.'`, `'..'`, `'a/./b'`, `'/abs'`, `'a\b'`, `'a\x00b'` | reject |
| `'crates/alpha/'` | **ACCEPT** (trailing slash) |
| `'crates//alpha'` | **ACCEPT** (empty interior segment) |

So its escaping does **not** enforce a canonical directory, and it cannot express the project root at all. That is why I added two new selectors rather than reusing it.

## 2. F-04 — the correction

**Schema** (`patch-01`, 42 lines). Two new `$defs` placed beside `CanonicalPath`, and `WorkspaceUnitV2.rootPath` / `memberPackageRoots.items` repointed:

- `CanonicalRelativeDirV1` — `^(?!.*(^|/)\.\.?(/|$))[^\u0000\\/]+(/[^\u0000\\/]+)*(?![\s\S])`. Constructive segment form, so leading/trailing slash and empty segments are impossible by construction; the dot-segment lookahead is reused **verbatim** from `CanonicalPath` so the frozen custody law is restated, not re-invented.
- `InternalUnitRootV1` — same, with an empty alternative for the project root.

`memberPackageRoots` is the *non-empty* selector, and that follows from source: a member is folded only when `w != d and _under_unit(d, w)`, which cannot hold for `d == ""`. Verified: both accept `crates/foo#bar`, `.hidden`, `..a`, `a b`, `deep/a/b/c/d`; both reject `.`, trailing slash, `a//b`.

**Ordering** (`patch-02`, 81 lines). `admit_unit_roots()` reads the two patterns **from the schema document** (house style: `GRAMMAR_CAPABILITY_REGISTRY`, `BODY_LANGUAGE_IDS` are read, not restated), and is called as the first statement of `assign_membership` and `unit_scope_descriptor` — before `_cargo_roots_of_units`, before any `_under_unit` prefix test, before `_rel` slicing, before `DD.spell_root`.

**Attribution** (`patch-03`, 51 lines). `enumeration_model` gains one **internal** fault key `ENUMERATION_MEMBERSHIP_UNIT_ROOT`, decided at line 581 — before `_membership_covers_snapshot` (585) and before every binding join. It delegates to `NV.admit_unit_roots`, so there is one authority, not two.

**Boundary classification.** I used the distinction the source already owns, and decided it by *which boundary the value crossed*, not by any prefix or filename. `ReferenceEnvironmentError` documents itself as "NOT an AdmissionError… the environment cannot produce a conforming answer at all"; it is used once, for a Unicode-data mismatch — a wrong unit root is not that. `units` reaching `assign_membership` is host-generated (`discover_units` output), so a violation is the same class as the existing `AdmissionError("membership must cover every inventory file exactly once")` two lines below, and is raised the same way. The **external** boundary is untouched: Config2/CLI roots keep `normalize_explicit_root` → `native.explicit-root-grammar` (CONFIG.INVALID).

**No public D9 code was invented — and could not be.** `d9_map` raises `"no D9 mapping for {detail}; silent exit 0 is forbidden"` for an unknown detail and refuses any code outside `EXISTING_D9_CODES`. I executed that: `d9_map('native.unit-root-representation')` → `AdmissionError`, identically before and after.

### Executed before/after (same script, both trees)

| case | BEFORE (frozen) | AFTER |
|---|---|---|
| C1 lawful root `""` | schema ok, membership `program-member`, scope `['.']` | **identical** |
| C2 root `"."` | schema **valid**, membership silently **all `syntax-only`**, scope spelled `['.']` indistinguishably, caps accepted | schema invalid; membership/scope refuse `NATIVE_UNIT_ROOT_REPRESENTATION:units[0].rootPath:#/$defs/InternalUnitRootV1:'.'` |
| C3 root `"src/"` | schema **valid**, membership **mixed** — `index.ts` dropped, `src/*.ts` kept: a silently **wrong partition** | refused |
| C4 root `"src//deep"` | schema **valid**, all `syntax-only` | refused |
| C5 `memberPackageRoots:["."]` | schema **valid**, accepted | refused at the `memberPackageRoots[0]` selector |
| C6 co-located TS+Rust at `""` plus nested `src/inner` | works, scope `['.', 'src/inner']` | **identical** — co-location and nesting preserved |
| C7 enum binding, root `"."` | `_unit_for_cell`→None, `_u1_entry`→None ⇒ **`ENUMERATION_BINDING_PROGRAM_ENTRY`** (wrong field) | root guard fires first: `ENUMERATION_MEMBERSHIP_UNIT_ROOT`, admission stops before binding |
| C8 ownership round trip | unitIds re-derive, ownership identity `sha256:2d1a24bc…` | **identical** — untouched |
| C10/C11 external root | `.`→`''`, `a/../b` refused | **identical** |
| C12 discovery | roots `['', 'crates/alpha']`, membership correct | **identical** |

**Contract prose** (`patch-04`): a new normative **U-0** bullet in `native-evidence.md` before U-1, stating the internal form, naming `.` as the external sentinel on both edges (`normalize_explicit_root` in, `spell_root` out), stating that a retained unit is never normalized after retention and why (exact-prefix consumption by U-3, slicing, and the `len(rootPath)` ranking), and recording that `CanonicalPath` is deliberately not this grammar.

## 3. Q-2 — the exact per-universe rule

`patch-05` adds a labelled clause at the end of execution-inputs §5. I derived it from the code, and it claims **no scope beyond what is enforced today**:

- A selected `(cellOrdinal, programOrdinal)` binding carries exactly one universe U. When §5 derives its Coverage accounts it resolves the Coverage of the views **that cell/program returned**, restricted to the binding's own producer closure. Inside that resolution: every resolved envelope's subject-scope `sourceUniverse` and every payload `key.sourceUniverse` **must equal U** (`load_coverage` lines 1094-1096 raise `EXECUTION_INPUTS_COVERAGE_DERIVE` and still return the row, so it is a fault, not a silent skip), and the account's `coverageIds` must equal the complete matching returned partition set (line 1201). §3 separately owns the named-scope `sourceUniverse` vs U check plus view `planId`, enumerator closure, `producerClosure` and receipt `outputDomains`.

The clause states explicitly what it does **not** do: it does not constrain `targetUniverse` (verified — lines 1114-1117 and 1210 key on `relation`/`resolution`/`sourceUniverse` only), so cross-universe relationships and incoming targets stay lawful; it does not ban a multi-universe Run; it does not ban a multi-universe view in general, only one **reached through a selected cell/program binding's account derivation**. It forbids exactly one thing: one view carrying two universes' Coverage, then attributed to a binding fixed at one of them.

**Refusal boundary proved unchanged**, same script both trees:

| tree | unmerged | merged |
|---|---|---|
| baseline25 | ADMIT, runId `bb3f0c9c…` | capture REFUSE `[EXECUTION_INPUTS_COVERAGE_DERIVE]`, semantic `EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_COVERAGE_DERIVE` |
| src25 | ADMIT, runId `f703f20a…` | **identical refusal and identical code** |

The unmerged runId moves because the registered schema document is part of Run identity (see §5). The decision and the code do not move.

## 4. F-05 and F-06 — reference controls on **frozen** candidate25

Built by fresh whole-graph construction (141 objects each, all digests minted from the offending value), **not** by mutating a hashed ancestor. My lawful control reproduces the author's packaged store **byte-for-byte** (runId `run3:541765b2…`, export sha `1b8ec850…`), which validates the harness.

Run through the author package's frozen `check-export.v4.py` against frozen candidate25:

| control | runId | structural | semantic |
|---|---|---|---|
| `ts-lawful-default` (`programEntry: null`, `default-unit`) | `541765b2…` | **ADMIT** | **ADMIT** |
| **F-05** `ts-negative-default-unit-nonnull-entry` | `cead63f5…` | **ADMIT** | **REFUSE — `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY`** |
| **F-06** `ts-lawful-explicit-plan-selection` (`programEntry: "tsconfig.json"`, `explicit-plan-selection`) | `476d7a77…` | **ADMIT** | **ADMIT** |

Three distinct runIds. F-05 reaches the semantic enumeration law exactly as required, not an unrelated hash mismatch. F-06 is lawful because `ENUMERATION_PLAN_DEFAULT_UNIT` (lines 631-633) fires only on *more than one* default-unit binding or a default-unit binding at ordinal ≠ 0 — it does not require one to exist — and the non-null entry then satisfies the `entry == graph['entryConfigPath']` join.

**What F-06 tests and what remains untested — stated precisely.** I tested a *single* binding with non-default provenance and a non-null selected config, admitted end-to-end and distinct from the default case. I did **not** build a two-binding cell (default at ordinal 0 *alongside* an explicit binding at ordinal 1): that needs a second universe H, its own per-`programOrdinal` inventories for every kind, and its own cell outcomes and coverage accounts. That construction remains untested here.

**Helper successor** (`output/files/helpers-successor/ts_pilot.py`). `_binding` → `_default_unit_binding`, the dead `program_entry` parameter removed, the single call site adjusted, zero `_binding(` call sites left, and a docstring stating that this constructor deliberately cannot express an additional-program binding. Predecessor bytes preserved unmodified (`987bade0…`); successor `7801111a…`. **Proof the parameter was dead:** the successor rebuilds the Run byte-identically — sha `1b8ec850…`, runId `541765b2…`.

## 5. Two additional defects I demonstrated rather than papered over

Running the suites surfaced two failures. I established by controlled experiment that **neither is caused by my correction**: a **null-change control tree** (semantically inert `$comment` added to the same schema, identical rebinding) passes **all 16** evaluator3 checks. The failures are content-dependent, and both are the same latent defect class in frozen *harness* code — treating a content-ordered `x-opensip-order: canonical-set` array as if position or element substitution carried meaning.

**D-1 — positional unpack of a canonical-set list.** `check-execution-inputs.v1.py:153,189,235`: `rel_schema, cov_schema = existing_view["schemaDigests"]`. That list is built by `M.canon_str_list([rel_schema, cov_schema])`, so its order is content:

| tree | relation digest | native digest | canonical order | position 0 is relation? |
|---|---|---|---|---|
| baseline | `53380a…` | `d8e9a1…` | `[53380a, d8e9a1]` | yes |
| null-change | `53380a…` | `954d8b…` | `[53380a, 954d8b]` | yes |
| **mine** | `53380a…` | `3f03de…` | `[3f03de, 53380a]` | **no — swapped** |

The swap assigns the relation digest to `cov_schema` → `native.coverage-payload-schema-not-registered`. The unpack was correct only for the accidental digest values of one frozen revision.

**D-2 — element substitution in a canonical-set array.** `check-analysis-seal-adapter.v1.py:79-94`: `remint_first_finding` substitutes a finding id everywhere by string replacement and never re-sorts, so `findingIds` fails `array order canonical-set: strict unique order required` whenever the new digest does not sort into the replaced position.

Both are **reference-harness** defects, not contract defects — consistent with AR-06's rule about not promoting a fixture defect. I fixed them in `patch-07` and `patch-08`, **classified separately as `separable-harness-defect`**, so root can take the normative correction and these independently. `patch-07` selects the coverage document by its registered identity (`H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)`) instead of by position; `patch-08` re-normalises the canonical-set finding arrays after substitution.

## 6. Integration consequence root must weigh

`native/native-evidence.schemas.v2.json` is **payload-registered**, so its raw SHA is checked by `registered_schema_documents()` at `identity-model.v3.py:769`. I measured the blast radius rather than assuming it:

- The old digest `d8e9a1fc…` is retained **6–17 times in every one of the author package's seven Runs**. Adopting this schema change therefore **requires reminting all seven** (and the three controls). This is expected for a pre-implementation schema correction, but it is not free.
- Rebinding is **not one file**. It took three ordered passes across **six** files in four owner areas: the `NATIVE_FIXTURES['coverageView']['schemaDigests']` declaration in `native-cases.v2.json`, then `source-pins` in foundation/native/security/workflows plus `evaluator3-source-pins`, then the cross-pins (the evaluator3 ledger pins the other four ledgers). Full delta retained in `output/evidence/source-pin-rebinding.json` (51 rows).
- By contrast the new internal fault key is **not** identity-bearing: `internalFaults` appears **0 times** in every packaged store.

**One requirement I did not adopt, and why.** I first also guarded `default_capability_selection`. That broke `check-identity.py:3561`, whose fixture is `_units=[{'languageMode':'ts-tsconfig','rootPath':'.','languageFamily':'tsjs'}]`. On inspection that guard was *my* over-reach: the function does no membership, no prefix test and no slicing, it only spells `rootPath or "."` outward, its docstring says it runs before Plan construction, and the stub is intentionally minimal (not a full `WorkspaceUnitV2`) for a check that asserts capability-absence codes and ordering, never the root. The task named membership, slicing and enum binding; that function is none of them, so I reverted it rather than widen the law. I do record the fixture as corroborating evidence that the ambiguity has already been acted on inconsistently inside frozen reference material — `rootPath: '.'` is written there today. I did not change it.

## 7. Suites executed

| suite | baseline25 | src25 |
|---|---|---|
| `run-reference-checks.py` | pins valid, 1224 files, **passed** (122s) | pins valid, 1224 files, **passed** (129s) |
| per-check report digests | — | **all 5 byte-identical to baseline**, `check-identity.py` included (`6de40d1cf1`) |
| `run-evaluator3-checks.py` | **16/16 exit 0** (239s) | **16/16 exit 0** (244s) |
| null-change control | — | **16/16 exit 0** (241s) |

Identical `check-identity.py` report bytes across 1596 checks is the strongest evidence I can give that the correction changes no existing behaviour.

## 8. Changed files (before → after)

| file | before | after |
|---|---|---|
| `native/native-evidence.schemas.v2.json` | `d8e9a1fcaa98` | `3f03ded5fabb` |
| `native/native_evidence_model.v2.py` | `2b57bfc34af4` | `6bf606bf7f7b` |
| `foundation/enumeration_model.v1.py` | `e8a51329b273` | `0724bd310794` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `06f614742a8a` | `3f3c0df4caaa` |
| `foundation/execution-inputs-contract.v1.md` | `12e753ee6ac5` | `3d612dfb3170` |
| `native/native-cases.v2.json` | `6f6ce5f915a1` | `2ff458b4a174` |
| `foundation/check-execution-inputs.v1.py` *(separable)* | `cedae4090f14` | `a7b8e173bca0` |
| `security/check-analysis-seal-adapter.v1.py` *(separable)* | `d790b4c515ef` | `200635edfa71` |
| 5 pin ledgers *(scratch-only rebinding)* | — | see `source-pin-rebinding.json` |

## 9. Separability and scope

The native model patch is based on frozen25 and touches only `admit_unit_roots` plus two call sites; it does not touch `discover_units`' cap logic, so it is cleanly separable from the pending XA-01 three-file patch. I did not duplicate root's parallel work (attachment custody, portable probes, coverage/weighting/citation limits, F-08 effective-edition evidence). No shared live or successor file was modified; no commit, push, implementation or agent use.

**Still open and not touched by this turn:** original blind 123 + 8 standing + 3 future reconstruction, AR-07 application review, and independent review of *this* correction. I authored it; it needs a fresh substantive independent reviewer, and adopting it requires reminting the seven author Runs and the three controls against the new registered schema bytes. No readiness is implied.
