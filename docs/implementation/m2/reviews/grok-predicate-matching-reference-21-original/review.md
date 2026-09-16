# Predicate-matching reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not Rust, runtime, schema-wire, identity-recipe, full Run, replay, or live install. Activation still needs root assent after this review. Local helper evidence is not complete-graph qualification.

**subjectManifestSha256** `04bf748e2796592f2691a5eff76bfd59e0828de192fcaae67b6ff2e1ce6ac463`  
`docs/implementation/m2/predicate-matching-reference-selection-v1-subject.json` **1842** bytes, **8/8** files, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/predicate-matching-reference-selection-v1/successor.json` **5363** / `006c225d8fa17b3fd9cf4bd71b4e55b45cb5162a642c71986a91b22f99ae1fc6`. Candidates (7) equal the subject minus that record.

## What this unit is

Two new reference changes on selected parents, plus three exact passage overrides that clarify existing generated-address alphabet and glob-contract attribution. Physical `identity-schemas.v3.json` bytes and identity hashing recipes are unchanged.

1. Selected workflows v1 `glob_match` (1296–1321) previously consumed a pattern `*` as a literal when the candidate scalar was also `*`, before recording the wildcard backtrack. Candidate excludes `*` from the equality branch: `p[i] == '?' or (p[i] != '*' and p[i] == s[j])`. Ordinary segments, whole-segment `**`, slashes, case, brackets, braces, and admission otherwise remain the same.
2. Selected identity `619d6e3c…41e6` `predicate_node_at` used `str.isdigit()` plus `int()`, which accepted Unicode decimal aliases (including non-ASCII leading zero) and let superscripts escape as uncaught `ValueError`. Candidate requires ASCII ordinal `0|[1-9][0-9]*` (`any(c<'0' or c>'9')` plus the existing ASCII leading-zero rule) and names `PREDICATE_ADDRESS` before conversion.

The workflow candidate also carries the already-accepted source-selection-v2 line-380 interruption override (`required` → `results` for committed Run ids). AST remainder is compared against that **effective** predecessor, not a raw rollback of historical v1. Deterministic first-kind fallback in unchanged workflows-v3 is retained.

## Pins

Parents (6), sorted unique, disk-exact:

| Parent | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md` | 3946 | `9b12ef44aa84f597427c27a9d2bf94fd487fd7f96893971cd902f71fb1d68ba0` |
| `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | 196987 | `a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21` |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | 142811 | `be37023f173f339edcd49b2019a2c6f3d424360a2c9cdcbf95bd382fa72066dc` |
| `docs/implementation/m1/source-selection-v2/successor.json` | 34488 | `8bd78b833ab84b719947080911e7ad358c00ac94242465492adee2343dac2819` |
| `docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py` | 158555 | `619d6e3cf49d0cd58967688e35c1598c92eaeb32b95fd30bb67f634271c141e6` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135448 | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` |

Unit directory has exactly the eight subject members; no extras.

Archived advisory `docs/implementation/m2/reviews/grok-policy-predicate-boundary-21/` (advisory + three follow-ups + root-disposition) matches `evidence/advisory-pins.json`. JSON copies equal this reviewer’s prior private tree.

## Passage overrides (clarification only)

All three `before` strings are unique and exact on the parent bytes; physical files are not rewritten.

- `identity-schemas.v3.json` `/$defs/program-predicate/description`: “shortest decimal” → “shortest ASCII decimal 0 or [1-9][0-9]*; non-ASCII digits are refused, never normalized”.
- `identity-and-evidence.md` line 1272: “shortest decimal without a leading zero” → “shortest ASCII decimal (`0` or `[1-9][0-9]*`), refusing non-ASCII digit spellings without normalization”.
- `glob-pattern-contract.v1.md` line 79: attributes the predicate to this unit’s `reference/workflows_model.v1.py::glob_match` and records the historical literal-star mismatch. Matching law and required examples are unchanged.

`program-predicate.predicateId` remains `$ref: Text` (`string`, minLength 1, maxLength **4096**, no digit pattern). Proof-bundle `predicateId` is the same 1–4096 string. Schema description now names the generated alphabet the helper already emits (`str(i)` / `.0`); lookup refuses other spellings. Direct helper inputs longer than 4096 stay outside this correction, as the README states. At the bound, `p.`+`9`×4094 (length 4096) is well-formed ASCII and still `PREDICATE_ADDRESS_RANGE` on the control tree.

## AST remainder and composition

- Identity remainder excluding `predicate_node_at`: **identical** to `619d6e3c…`. Byte delta +52 (docstring + one condition). `predicate_child_addresses` and `identifier` unchanged.
- Workflow remainder excluding `glob_match`, after applying source-selection-v2 line 380 to historical v1: **identical** to the candidate. Remainder versus **raw** historical v1 is **not** identical (the interruption line differs). Candidate line 380 uses `results`, not `required`. Net bytes 142811 − 1 + 18 = 142828.
- `workflows_model.v3.py` is **not** a candidate and remains **22494** / `60f28dc97114cf918a92f5c8bb99a3b3e5d73a2608a7b9d289b7a9f652a36123`. It loads `HERE/'workflows_model.v1.py'`, re-exports public names, and overrides `rule_program_digest` / `admit_atom` / `admit_policy_rule`. `glob_match` / `in_scope` therefore come from the overlaid v1. First-kind fallback `next((k for k in kinds if k), None)` is still present. Future composed environments must place both replacement files at those HERE-relative import locations together with this unchanged v3; historical relative imports are not rewritten.

## Independent reproduction (Python 3.12.13 / UCD 15.0.0)

Frozen `evidence/check-matching.py --architecture $ARCH` and a separate declarative checker in this work tree (`independent_check.py`; star decided before literal equality; ASCII ordinal `0|[1-9][0-9]*`) agree with `evidence/result.json` on every frozen field:

| Gate | Result |
| --- | --- |
| Glob pairs vs independent law | **609978** cases, **0** mismatches, **1732** changed |
| Original four literal-star counterexamples | old helper false / law true; candidate true |
| Contract required examples + `?` vs candidate `*` + fullwidth `＊` | candidate = law |
| ASCII address controls | **23**, all unchanged vs selected identity (including `p.01` ADDRESS, `p.3` RANGE, `p.0.0` LEAF, bound RANGE) |
| Unicode address controls | **805** (`798` `isdigit()` scalars from U+0080 plus 7 mixed extras); **804** changed; all candidate `PREDICATE_ADDRESS`; sole unchanged extra `p.0١` (already ASCII leading-zero ADDRESS) |
| Emitted child-address round-trips | **7**, ASCII `str(i)`, child helper identical |
| AST remainder vs effective predecessor | true; inherited interruption preserved |

Superscripts that previously raised `ValueError` now name `PREDICATE_ADDRESS`. Arabic-Indic / fullwidth digits that previously navigated or hit RANGE now ADDRESS. No full Run or replay was executed.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, not Rust glob selection, not policy.rs / predicate-owner implementation, not caller ADMIT, not `open_run_closure` / replay, not a schema pattern added to `Text`, and not a live overlay. Root portable counts are local helper evidence only.
