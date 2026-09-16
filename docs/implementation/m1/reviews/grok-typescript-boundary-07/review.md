# Independent Grok review: TypeScript boundary07

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-subject-07`
**Manifest SHA-256:** `34170796e4d0807e5186d6fccc90725a3c296475b7901c7c9667e072490f678d`
**Entries:** 2047 (1694 files, 335 directories, 18 symlinks)
**Verdict:** **ACCEPT WITHIN STATED DELTA SCOPE**

Mechanism-only successor to Grok-accepted boundary06. No production compiler/sys.require policy, bootstrap, inventory installation, M1, or source-selection-v2 is selected. Original04 remains CHANGES REQUIRED. Original06 bytes and Grok06 ACCEPT are unchanged.

## Custody

Verified before and after. Every listed path’s type, mode, file digest and symlink target matched. Frozen subject was not executed against.

| Check | Result |
| --- | --- |
| Manifest | `34170796…678d` matches declared |
| Walk | 2047 = 2047; extra/missing/mismatch/mode/symlink 0 |
| After | frozen hash unchanged |

## Delta vs accepted06

| Path | Standing |
| --- | --- |
| `checker/src/usages.mjs`, `resolve.mjs`, `browser-scanner.mjs`, `browser-options.mjs` | byte-identical to 06 |
| `checker/src/tool-policy.mjs` | new |
| `checker/src/lane.mjs` | inventory chain + tools/ subpackage bind |
| `checker/src/check.mjs` | `--tool-policy`, bound caller exceptions refused, report pin/limitations |
| `checker/test/root07.test.mjs` | 21 new checks |

Bound tooling exceptions must come from a contract-successor candidate **and** manifest member (exactly once), an exception-free lane record equal to the checked record, and sorted pins of declared inputs, manifest, tsconfig, lock and exception files. Empty-target `dynamic-loader` sites require `unfollowedDynamicLoaders` with limitation `reviewed-tool-code-outside-statically-enumerated-closure` and a path under that package’s `node_modules/`. That is not a proof of unreachability. `dependencyClosureQualified` and `sourcePurityQualified` stay false. Finite targets remain ordinary ownership/declared-input checks. Report and typescript-provider `policyId`s cannot use this reader. Caller `trustedUsages` on a bound lane are refused.

`tools/` nested packages become bound only when the selected inventory lists their `package.json` as tooling/manifest. Uninventoried nested trials stay unbound.

Inventory binder now walks every five-pin successor and requires the first parent in `lock.inputs` and each later parent equal to the immediate predecessor candidate. Parent06 still refuses an inventory4-shaped chain (`inventory parent is not a selected design-lock input`). That is the first-only hole this delta closes at the pin layer.

## Precondition: pins, not semantic acceptance

`bindToolPolicy` and `bindInventory` hash/length-check review and assent documents and do not read verdicts. Independently, a fixture `review.json` with `verdict: CHANGES REQUIRED` still binds. That matches 06 and `root07-policy.md`: orchestration must run owned `tools/verify_design.py` first. A passing checker call is not design approval. Synthetic test approval documents are fixtures and must not be copied into a product lock. The mechanism does not silently give caller-owned exemptions authority.

## Reproduction (private copy)

Node v24.16.0 `--experimental-import-meta-resolve --test checker/test/*.test.mjs`: **224/224** (203 inherited + 21 new). Writes `copy/work/`. Frozen `root07-full-tests02` is the final source run; `full-tests01` (222) is intermediate chain-edit evidence only. 32 inherited mutants, 11 review03 mutants and 8 manifest controls were not rerun (same skip as 06; AMD/browser sources unchanged).

## Independent probes (20/20)

Empty-target external disclosed binds; local empty-target refused; caller/browser/provider/unbound policy refused; undisclosed empty target and invented “proven-unreachable” refused; bound without policy still `unsupported-loader`; finite target cross-package `lane-escape`; finite target not a declared input refused; two-successor inventory chain verifies; 06 binder refuses that shape; broken predecessor join refused; uninventoried `tools/contracts` unbound; inventoried nested manifest bound; stale site refused.

## Must-fix / should-fix

None in this delta scope.

## Remaining

Actual compiler invocation, environmental inputs, source-generator confinement, RuntimeClosure and source purity remain unqualified. Policy file contents for real tool closures are not selected. Inventory/bootstrap/tool installation and source-selection-v2 are separate. Not product, M1, or Claude agreement.
