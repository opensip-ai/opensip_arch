I'll close the remaining authority holes in the four execution-inputs files: retained member locators, Plan-rooted candidate extent, and independent coverage census. Reports go only to a new v4 folder.Plan-rooted `candidateSourcePaths` on enumeration bindings, then retained `sourceBodies` in the candidate envelope so locators are not a free caller map.Root v3 is not treated as accepted. These six holes are closed in isolated source. Reports are only in **v4**; v1/v2/v3 receipt paths refuse.

## Exact files

**Execution-inputs (38 cases, mismatches `[]`)**

| file | bytes | sha256 |
|---|---|---|
| `execution-inputs.schema.v1.json` | 25130 | `664287ee496f94046c915df82350dc54cf77bbc938834c1070e21b6283eae2b9` |
| `execution-inputs-contract.v1.md` | 11095 | `7b8352801376d75cbb3b9af86ff4061766e0ef8f37530dc93f1bbc7517ae215c` |
| `execution_inputs_model.v1.py` | 59672 | `0b0ad476495327fd8ab652d8eabdcc1c190673c04f256ee1a3440af2475a92b3` |
| `check-execution-inputs.v1.py` | 50656 | `bd161fdd962daba2ec981334b6946a62c500328fd3a491526cf40b069027f24b` |

**Enumeration (Plan-rooted candidate census; 44 cases, mismatches `[]`)**

| file | bytes | sha256 |
|---|---|---|
| `enumeration-plan.schema.v1.json` | 19890 | `62ff499e024b83150fee7ce62c449553a3bc2021e0476975f922cdceef806237` |
| `enumeration-contract.v1.md` | 19341 | `f977cad6d34b5d8d0f409a69eafb9249fa7b1b23f6f83add9488b30072cbbbf3` |
| `enumeration_model.v1.py` | 43873 | `e8a51329b273245895bcb330cbf52b13667423fcd2d6137b887940fd9cff83ff` |
| `check-enumeration.v1.py` | 37224 | `d547707649b8410ee9a627472934c0613120ddc6ea17f320ab9ec009372cdaac` |

Receipts: `/tmp/opensip-design-corrections/grok-execution-inputs.v4/check-receipt.json` and `enumeration-check-receipt.json`. Checker default is stdout. `--receipt` into v1/v2/v3 is refused.

Owner-graph file positive remains **ADMIT / row `partial` / `native-work-incomplete` on package**. Not a Run.

## What closed

1. **No free `member_locators`.** Coordinates live on retained `CandidateProducerResultV1.sourceBodies` `{id, path, contentSha256, byteLength, universe}`. Group members must be those opaque ids. Path, U, and snapshot `sha256`/`bytes` must match **this** binding’s Plan census and snapshot row. Wrong-U and unbound ids refuse.

2. **Plan-rooted candidate extent.** `kinds=[]` / empty extents are not complete-empty work. Available `clones-near` / `clones-cross-tsjs` bindings require `candidateSourcePaths` (subset of first-party scoped snapshot members). Two programs with disjoint sets ADMIT at enumeration; examining the union as one program’s complete extent refuses.

3. **Independent coverage census.** Expected subjects come from inventory/extent and the relation’s subject-kind (`source-path` / `package-name` / `symbol`), not from returned scopes. A complete Coverage over a subset of expected file paths leaves the file account **incomplete**. Account complete is extraction completeness, not fully-resolved semantics (RC-1 / RC-3 unchanged).

4. **Original causes.** Partial inventory `budget-exhausted` is not rewritten as `provider-unavailable` (`OUTCOME_DERIVE`). Required partial inventory still emits `required-cell-unsatisfied` with the inventory digest. All originating causes/inputRefs stay on `derivedOutcomes`.

5. **Host-derived sidecars.** `hostCapture.hostDerivedRefs` is the custody set for inventory / candidate / target / incoming. A target-attribution may be selected without being a view-stage output. Complete-empty candidate requires the retained envelope **and** `examinedPaths` equal the Plan census.

## Root adapter (precise)

- Emit `candidateSourcePaths` on each available clones-near/cross-tsjs binding (do not omit the field; `[]` is an explicit zero census).
- Put `sourceBodies` on every `CandidateProducerResultV1`; drop any caller locator map.
- Fill `hostDerivedRefs` with every selected inventory, candidate, target-attribution, and incoming-search digest.
- Reconstruct: compare candidate `examinedPaths` to **that binding’s** `candidateSourcePaths`; bind group members only through retained `sourceBodies`; join coverage accounts to inventory/extent census, not only returned views.
- Still needed for later registration (unchanged): ProofInputRef `candidate-producer-result`; do not add inventory/candidate/target/incoming to a view-only stage’s `outputDomains`.
