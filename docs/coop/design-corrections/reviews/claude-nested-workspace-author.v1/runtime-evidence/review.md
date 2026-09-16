# Nested Cargo workspace folding — bounded author correction

**Standing.** Bounded architecture/design/reference correction of nested Cargo workspace folding over a fresh regular-file capture of frozen39. Not independent acceptance, not readiness, not frozen40, not a repin. No product code, commit, push, activation, agents, web or private/session logs; no LIVE, frozen or other-runtime writes; no blind consumer artifact or root replay diagnosis read; the TS/JS unitKind coauthor's work was not read. Root integration, full references and independent review follow. Every number below is recomputed by `tools/build_review.py` from receipts and result files; `review.json` carries the same values and 27 consistency checks (all hold: **True**).

## 1. Custody

- LIVE manifest39 `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json`, sha256 verified; all 12909 members (737605070 bytes) verified, then captured as fresh regular files into `work/source` (`custody/frozen39-capture.json`: no faults, no unlisted, no copy faults).
- End-of-work recheck (`results/final-recheck.json`, receipt `final-recheck`): manifest sha holds, frozen39 snapshot 0 faults / 0 unlisted; `work/source` differs from frozen39 in exactly the 5 delta files at their after-bytes; root's probe directory unchanged in use (hashes recorded) and root's `report.json` rows equal this runtime's pre-fix path-only adaptation rows: **True**.

## 2. Defect, reproduced

Root's observation reproduces in the capture (`probes/root_adapted.py`, a path-only adaptation: model and report paths are arguments; cases and calls are root's): ordinary workspace, nested workspace leaf and explicit inner workspace return; `nested-workspace-with-package` raises `StopIteration`.

Mechanism in frozen39 `discover_units` (lines 3925–3958): two passes disagreed on what a fold target is. Pass 1 marked a `Cargo.toml` directory folded when **any enclosing kept workspace manifest** existed. Pass 2 chose the **deepest enclosing workspace manifest** and looked it up among units with `next(...)`. A workspace manifest below a workspace unit is itself folded by pass 1, so for any `Cargo.toml` directory below such a nested workspace the lookup finds no unit and `StopIteration` escapes. It is not a typed refusal, and it also escapes enumeration admission: the derivation witness (`enumeration_model.v1.py:667`) catches only `AdmissionError`/`ValidationError`.

Measured extent before the correction (`results/prefix/discriminate.json`):

- exhaustive sweep over six directories (`""`, `a`, `a/b`, `a/b/c`, `a-b`, `ab/c`) × {absent, package, workspace}, automatic and every explicit selection of one or two present directories: **918 of 8504 inputs raised `StopIteration`**; every input that returned already matched the law oracle (0 mismatches) and P22 (0 mismatches);
- 12 of 24 named scenarios raised: `nested-workspace-with-package`, `depth-three-workspaces-and-package`, `depth-package-between-workspaces`, `nested-without-root-manifest`, `sibling-outer-workspaces-keep-their-own-subtrees`, `member-roots-strict-utf8-order`, `explicit-outer-root-equals-automatic`, `explicit-outer-and-inner-workspace`, `explicit-outer-and-inner-package`, `boundary-below-nested-workspace-keeps-the-rest-folded`, `explicit-outer-root-with-inner-boundary`, `pruning-under-nested-roots`;
- enumeration admission with nested markers in the derivation witness: `StopIteration` escaped at `native_evidence_model.v2.py:3957`.

## 3. Assessment under published law

U-4b.2 folds "a `Cargo.toml` directory strictly below the root of a `cargo-workspace` **unit** … into the DEEPEST such workspace". "Such workspace" can be read as a unit or as any workspace manifest. Only the unit reading is implementable. `memberPackageRoots` exists only on a `WorkspaceUnitV2`, and a workspace manifest below a workspace unit is not a unit by the same sentence. The manifest reading therefore has no record to receive members and forces either a contradiction or a refusal.

The unit reading is total, so no refusal is needed. Take a kept `Cargo.toml` directory *d* with at least one enclosing kept workspace manifest, and let *w₀* be the shallowest. *w₀* has no enclosing kept workspace manifest (one would also enclose *d* and be shallower), so *w₀* is a unit. A workspace manifest below another kept workspace manifest is folded, so workspace units are pairwise non-nested. Exactly one workspace unit therefore encloses *d*, and "DEEPEST (the longest enclosing `rootPath`)" selects it. The sweep observed this: every one of 6930 folded directories after the correction had exactly one enclosing workspace unit (`oracleEnclosingUnitCounts`).

Consistency with the neighbouring law:

- **P22 / U-2** (explicit roots are unit selection): selection happens before folding and is unchanged. Explicit `.` equals the automatic unit. `.`+`nested` folds `nested` into the root unit, just as frozen39 already folds an explicitly named member package under a named workspace root. `nested` alone is its own workspace unit with `nested/pkg`, and `nested/pkg` alone is a `cargo-package`. Over all 1458 single-workspace explicit selections in the sweep, the explicit unit equals automatic discovery of its own subtree (0 mismatches).
- **U-8** boundaries: marker directories at or below a boundary are removed before folding (item 1); unchanged. A boundary below a nested workspace used to crash; it now folds the rest.
- **U-4a / U-4b.4** pruning: Cargo roots for rows are unit roots plus member roots. With the correction every folded nested root is a member, so `nested/target` and `nested/pkg/target` stay `host-ignore-convention` and `nested/src/target` stays source.
- **U-4b.3** ordering: unchanged (strict UTF-8 member roots; `nested-x` sorts before `nested/pkg`), enforced by the M3 law control.

**A typed refusal was considered and rejected.** No published law makes a workspace manifest below a workspace unit an error. U-4b.2 prescribes folding, and the observations are representable trusted markers. A refusal would need a new code, which is out of scope, and would refuse inputs the contract already decides. No claim is made that Cargo accepts such a layout: this is a standalone reference over marker observations, and applicability is assessed under the published law only.

## 4. Correction (smallest coherent)

| file | before sha256 / bytes | after sha256 / bytes |
| --- | --- | --- |
| `docs/coop/design-corrections/foundation/check-enumeration.v1.py` | `732e0b045157c6d0e14fb0533e9259ba275166856aa734e5c4c22fdc40b021f4` / 40097 | `cf1139cda9f329bc8c86020600ab4e8a78820b71b51ede7f9f6e4498950c5b51` / 43270 |
| `docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` | `caa602935474f6d29b65daca0348eb65c6a86243658d07c387e0e82b8e8eafdc` / 61016 | `d826987aeecd2ed41241cef3d6f9aff70a70ce027b5c27548ad8a4d23a439a90` / 62605 |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `fb1bcc38737ad04c26259bff788c55caac79ab759a1f293ad4a829ce6cdf6d52` / 633768 | `b0f82ca2e35494c34fbf84c7b5195d3f25cc3c28ee54c8dfe597b0d63f4da8d4` / 641457 |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `51bcab333b2f35f4e33cecf6e3581f108c440b9526ca3dbbaa14d7301cc965ca` / 307748 | `f19ecff7fb0959ff513d8e193122507f30a60fa7616d28542c00fcc2e2eb9a57` / 307986 |
| `docs/v2/contracts/product-v1/native-evidence.md` | `efd413891925c25629f1677e05b67c00754c5e9d1135d3f2dd18328289b14037` / 296916 | `87875d1067e72fac37e0c6d465f066353c6483310d0c35e17809d8521885710d` / 297517 |

`correction.patch` sha256 `1c38cd8373c170baf088e8c626d3ef9a1a7cc55e64e9af39460858d09f38e2a8` (20502 bytes), unified diff against frozen39 (a/ b/ repo-relative, 3 lines of context); `delta-manifest.json` sha256 `2222fa2edf61607fa15878e401a196a76a7af4ec79ca7c04fd59c32057e77987`. The system `patch -p1` applied to the frozen39 before-bytes reproduces all five after-images exactly (`results/postfix/patch-apply-check.json`).

- **Model.** One depth-ordered pass. A `Cargo.toml` directory is folded into the deepest already-emitted `rust` `cargo-workspace` unit that strictly encloses it, or else becomes a unit. The former second pass (the `next(...)` lookup) and `cargo_ws_roots` are removed, plus one docstring sentence. There is no new code, schema, registered-schema byte, pin or planning change, and no TS/JS line changed.
- **Behaviour preserved elsewhere.** Every sweep input that returned before the correction returns byte-identical output after it (7586 inputs); every one of the 918 inputs that raised now returns (`results/postfix/sweep-comparison.json`).
- **Contract.** U-4b.2 now says the fold target is a surviving **unit**, that directories left after item 1 and explicit selection are decided shallowest first, that a nested workspace manifest below a workspace unit is a member and receives none, and why a target always exists. It cites the new native case.
- **Checker controls.**
  - `native-cases.v2.json`: fixture `markersCargoNestedWorkspace` and case `units-nested-cargo-workspace-folds-into-the-deepest-surviving-workspace-unit`, placed after the existing P22 Cargo case rather than at the array end. The case covers automatic folding, explicit `.`, `.`+`nested`, `nested` and `nested/pkg`, a nested-project boundary, pruned trees, membership rows and scope prefixes.
  - consumer24 M3: 4 rows — the fold, the law passing, member roots in segment rather than UTF-8 order giving `ENUMERATION_MEMBERSHIP_ORDER`, and a dropped folded member un-pruning its `target` giving `ENUMERATION_MEMBERSHIP_ROW_DERIVATION`.
  - enumeration: the derivation witness over nested markers now decides a typed `REFUSE` [`ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION`] where memberships differ, and a coherent nested-workspace admission `ADMIT`s. The exact refusal and the folded rust unit are asserted.

## 5. Suites (all children finished)

Suites ran in run copies, never in `work/source` (checkers write reports beside themselves). `work/run-prefix` is a copy of the unedited capture. `work/run-postfix` is a copy of the corrected capture with the 25 registered pin entries of the 5 delta files rewritten from before to after sha256, **in the copy only**, across 5 pin files (`results/postfix/run-copy-pin-overlay.json`; no entry was at an unexpected value). The delta itself changes no pin file.

| suite | pre-fix (frozen39 bytes) | post-fix (corrected, pin overlay) |
| --- | --- | --- |
| native | exit 0 — PASS: 380/380 cases; matrix cells 66; open objects 0; uncovered feedback [] | exit 0 — PASS: 381/381 cases; matrix cells 66; open objects 0; uncovered feedback [] |
| consumer24 | exit 0 — 183/183 passed; failed [] | exit 0 — 187/187 passed; failed [] |
| enumeration | exit 0 — mismatches [] | exit 0 — mismatches [] |
| integration | exit 0 — passed 412, failed [] | exit 0 — passed 412, failed [] |
| security | exit 0 — passed True, cases {'total': 464, 'pass': 464, 'fail': 0}, sweeps 11/11 | exit 0 — passed True, cases {'total': 464, 'pass': 464, 'fail': 0}, sweeps 11/11 |
| identity | exit 0 — passed 1596, failed 0 | exit 0 — passed 1596, failed 0 |
| workflow-projection | exit 0 — passed True, failed [], ok rows 838/838 | exit 0 — passed True, failed [], ok rows 838/838 |

The new native case passed in the post-fix report, and the enumeration receipt records {"nested-cargo-workspace-derivation-differs-refused": ["REFUSE", ["ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION"]], "nested-cargo-workspace-derivation-folds-into-surviving-unit": ["ADMIT", []]}. Without the pin overlay, the corrected bytes are refused by pin verification exactly on the 5 delta files: native `PIN-MISMATCH` exit 2 (receipt `postfix-unpinned-suite-native`), security `sourcePinsValid: false` exit 1 (`postfix-unpinned-suite-security.2`). **Root must repin at integration; this delta deliberately does not.**

### Controls discriminate: corrected checkers and cases against the frozen39 model

The used unpinned copy was changed to hold the frozen39 model, with pins for the other 4 delta files overlaid (`results/controls/control-copy-state.json`, 25 pin entries, holds: True).

- native: exit 1, the checker aborts (`TypeError: 'NoneType' object is not subscriptable`). Its step resolver dereferences `$auto.units` after the faulted step, which is the existing harness behaviour for any failed bound step. `probes/native_case_diagnosis.py` runs the case's discovery steps through the checker's own `run_case`: 4 `discover_units` steps fault with `StopIteration` (automatic, `.`, `.`+`nested`, boundary), the explicit `nested` and `nested/pkg` steps return, and 9 expectations are unreachable. Against the corrected model the full case passes.
- consumer24: 183/184; the only failure is M3 `section-crashed` (`StopIteration` at the `next(...)` lookup), and every pre-existing row still passes.
- enumeration: exit 1, `StopIteration` escapes admission from `admit_enumeration` → `discover_units`.

## 6. Failed attempts, preserved

- `edit-native-cases` (exit 1): native-cases.v2.json does not round-trip through json.dumps(indent=1); refusing to rewrite → edit-native-cases-textual: textual insertion keeping every original byte; the dumps round-trip first differs at the offsets it records
- `postfix-unpinned-suite-security` (exit 1): FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/opensip-design-corrections/claude-nested-workspace-author.v1/results/postfix-unpinned/security-report.json' → postfix-unpinned-suite-security.2 with an existing report directory (harness error, not a suite result)
- `control-copy-mutate` (exit 1): FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/opensip-design-corrections/claude-nested-workspace-author.v1/results/controls/control-copy.json' → the copy had already been mutated before the record write failed; control-copy-verify-state reads and records the actual state instead of re-running
- `build-review` (exit 1): FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/opensip-design-corrections/claude-nested-workspace-author.v1/receipts/build-review/exit.txt' → the builder listed its own in-progress receipt (no exit.txt yet); it now skips receipts without exit.txt and names them
- Pre-fix probe, control and checker failures above are intended evidence and are kept as receipts.

## 7. Integration notes for root

- **Model hunks** are near, but do not change, the TS/JS unit block. The third hunk's context includes the tsjs `recognizerId` / `provenance` / `break` lines (frozen39 3950–3952). If the TS/JS unitKind coauthor changed those exact lines, that hunk needs a 3-way merge. That author's work was not read.
- **Checker insertions:** `native-cases.v2.json` after `markersCargoWorkspaceTwoMembers` and after case index 105 (380→381 cases); consumer24 at the end of `m3()`; enumeration after `invalid-boundaries-native-admission-error`, plus 2 `want` entries and one assertion after the internal-root mismatches.
- **Pins, reports, receipts:** registered pins (native, security, foundation, evaluator3, workflows pin files) still name the before-bytes. The frozen `native-evidence-report.v2.json` was not regenerated (post-fix reports live only in the run copies), and enumeration receipts were written to this runtime.

## 8. Scope limitations

- Standalone reference evidence over trusted marker observations. No Cargo, compiler or repository code ran, and no claim is made about Cargo's treatment of nested or `exclude`d workspaces. Markers carry no `exclude` information; whether a product should treat an excluded nested workspace as its own unit is a separate product/Cargo-semantics question that published law does not decide, and it is not decided here.
- The sweep universe is 6 directories, explicit selections of at most 2, rust markers only, no boundaries, custody exclusions or cap interplay; those are covered only by named scenarios. The oracle was written by the same author as the fix, from the contract text, so it is not independent.
- Suites ran on run copies with a pin overlay, not on LIVE or the frozen tree. Identity, workflow projection, integration and security are breadth re-runs whose results are unchanged.
- No acceptance, readiness, frozen40 or repin is claimed. Root full references and independent review follow integration.

## 9. Commands (receipts)

| label | exit | argv (after interpreter flags) |
| --- | --- | --- |
| prefix-root-adapted-probe | 0 | `probes/root_adapted.py work/source results/prefix/root-adapted.json` |
| prefix-make-run-copy | 0 | `tools/make_run_copy.py work/source work/run-prefix results/prefix/run-copy.json` |
| prefix-discriminate-probe | 0 | `probes/discriminate.py results/prefix/discriminate.json work/source` |
| prefix-suite-native | 0 | `work/run-prefix/docs/coop/design-corrections/native/check_native_evidence.v2.py` |
| prefix-suite-enumeration | 0 | `work/run-prefix/docs/coop/design-corrections/foundation/check-enumeration.v1.py --receipt results/prefix/enumeration-receipt.json --hashes results/prefix/enumeration-hashes.json` |
| prefix-suite-security | 0 | `work/run-prefix/docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report results/prefix/security-report.json` |
| prefix-suite-integration | 0 | `work/run-prefix/docs/coop/design-corrections/check-integration.py --report results/prefix/integration-report.json` |
| prefix-suite-consumer24 | 0 | `work/run-prefix/docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` |
| prefix-suite-identity | 0 | `work/run-prefix/docs/coop/design-corrections/foundation/check-identity.py --report results/prefix/identity-report.json` |
| prefix-suite-workflow-projection | 0 | `work/run-prefix/docs/coop/design-corrections/workflows/check-workflow-projection.v3.py` |
| edit-native-cases | 1 | `tools/edit_native_cases.py work/source/docs/coop/design-corrections/native/native-cases.v2.json` |
| postfix-root-adapted-probe | 0 | `probes/root_adapted.py work/source results/postfix/root-adapted.json` |
| postfix-discriminate-probe | 0 | `probes/discriminate.py results/postfix/discriminate.json work/source` |
| edit-native-cases-textual | 0 | `tools/edit_native_cases_textual.py work/source/docs/coop/design-corrections/native/native-cases.v2.json` |
| build-delta-v1 | 0 | `tools/build_delta.py work/source deltas/v1/correction.patch deltas/v1/delta-manifest.json` |
| postfix-make-run-copy-unpinned | 0 | `tools/make_run_copy.py work/source work/run-postfix-unpinned results/postfix/run-copy-unpinned.json` |
| compare-sweeps | 0 | `tools/compare_sweeps.py results/prefix/discriminate.digests.json results/postfix/discriminate.digests.json results/postfix/sweep-comparison.json` |
| postfix-unpinned-suite-native | 2 | `work/run-postfix-unpinned/docs/coop/design-corrections/native/check_native_evidence.v2.py` |
| postfix-unpinned-suite-security | 1 | `work/run-postfix-unpinned/docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report results/postfix-unpinned/security-report.json` |
| postfix-make-run-copy-pin-overlay | 0 | `tools/make_run_copy.py work/source work/run-postfix results/postfix/run-copy-pin-overlay.json --pin-overlay deltas/v1/delta-manifest.json` |
| postfix-unpinned-suite-security.2 | 1 | `work/run-postfix-unpinned/docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report results/postfix/security-report-unpinned.json` |
| postfix-suite-native | 0 | `work/run-postfix/docs/coop/design-corrections/native/check_native_evidence.v2.py` |
| postfix-suite-enumeration | 0 | `work/run-postfix/docs/coop/design-corrections/foundation/check-enumeration.v1.py --receipt results/postfix/enumeration-receipt.json --hashes results/postfix/enumeration-hashes.json` |
| postfix-suite-security | 0 | `work/run-postfix/docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report results/postfix/security-report.json` |
| postfix-suite-integration | 0 | `work/run-postfix/docs/coop/design-corrections/check-integration.py --report results/postfix/integration-report.json` |
| postfix-suite-consumer24 | 0 | `work/run-postfix/docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` |
| control-copy-mutate | 1 | `tools/mutate_run_copy.py work/run-postfix-unpinned deltas/v1/delta-manifest.json results/controls/control-copy.json --revert docs/coop/design-corrections/native/native_evidence_model.v2.py` |
| postfix-suite-identity | 0 | `work/run-postfix/docs/coop/design-corrections/foundation/check-identity.py --report results/postfix/identity-report.json` |
| control-copy-verify-state | 0 | `tools/verify_control_copy.py work/run-postfix-unpinned deltas/v1/delta-manifest.json results/controls/control-copy-state.json docs/coop/design-corrections/native/native_evidence_model.v2.py` |
| patch-apply-prepare | 0 | `tools/patch_apply_check.py prepare deltas/v1/delta-manifest.json work/patch-apply-v1` |
| patch-apply-system-patch | 0 | `/usr/bin/patch -p1 -d work/patch-apply-v1 -i deltas/v1/correction.patch` |
| postfix-suite-workflow-projection | 0 | `work/run-postfix/docs/coop/design-corrections/workflows/check-workflow-projection.v3.py` |
| controls-prefix-model-suite-native | 1 | `work/run-postfix-unpinned/docs/coop/design-corrections/native/check_native_evidence.v2.py` |
| controls-prefix-model-suite-enumeration | 1 | `work/run-postfix-unpinned/docs/coop/design-corrections/foundation/check-enumeration.v1.py --receipt results/controls/enumeration-receipt.json --hashes results/controls/enumeration-hashes.json` |
| patch-apply-verify | 0 | `tools/patch_apply_check.py verify deltas/v1/delta-manifest.json work/patch-apply-v1 results/postfix/patch-apply-check.json` |
| controls-prefix-model-suite-consumer24 | 1 | `work/run-postfix-unpinned/docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` |
| controls-native-case-diagnosis-prefix-model | 0 | `probes/native_case_diagnosis.py work/run-postfix-unpinned results/controls/native-case-diagnosis-prefix-model.json` |
| controls-native-case-diagnosis-corrected-model | 0 | `probes/native_case_diagnosis.py work/run-postfix results/controls/native-case-diagnosis-corrected-model.json` |
| final-recheck | 0 | `tools/final_recheck.py deltas/v1/delta-manifest.json results/final-recheck.json` |
| build-review | 1 | `tools/build_review.py` |

Interpreter for every Python receipt: `/tmp/opensip-architecture-review-env/bin/python -I -B`, with `PYTHONDONTWRITEBYTECODE=1`; each receipt directory holds command, cwd, stdout, stderr, exit and digests. Direct edits made without a receipt: native_evidence_model.v2.py: fold loop + removed second pass (Edit x2) and docstring sentence (Edit x1); native-evidence.md: U-4b.2 clarification (Edit x1); check-native-consumer24-corrections.v1.py: M3 tail rows (Edit x1); check-enumeration.v1.py: two cases (Edit x1) and expectations/assertion (Edit x1); native-cases.v2.json: fixture + case via receipt edit-native-cases-textual.
