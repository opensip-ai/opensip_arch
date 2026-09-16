# evaluator3 repair:2 preview owner: exact evidence-Run join and declared retained unavailability

**Standing.** A bounded author correction by the actual Claude coauthor `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`. It covers architecture, design and reference only.
- **Not:** source acceptance, readiness, product qualification, global pins, planning, a commit or a push.
- **Further review:** a later independent final-source review is required.
- **Merge:** root will three-way merge this bounded delta with the separate f561 final grammar correction.
- **Out of scope:** the known unrelated policy-test grammar failure is not fixed and not relabelled here.

**Runtimes.**
- **Original:** `/tmp/opensip-design-corrections/claude-repair-join-author.v1`. Everything written there is preserved unchanged, including the status-only record files.
- **Continuation (this runtime):** `/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1`.

## 1. Captured inputs and custody

**Root probe directory** `/tmp/opensip-design-corrections/root-repair-owner-probe.v2` (read only; hashes in `receipts/p00-copy.json`):

| File | sha256 |
|---|---|
| `report.json` | `444c1ab5faadb04db92f4a101379689ed214eda8cd47afe75d76773b64e08ceb` |
| `probe.py` | `d96b22650f9dccffe05fe7b32cf650d8c2fedb706d9658e42ed874e1dd650c11` |
| `capture.json` | `e3d9d4300f5bb60adb7926fcb9b810bfee311a0bdc918dd2bb90bcc0df9598f3` |
| `checker-stdout.json` | `fbeafa10407d103717b657ae325e5aa757be8ba833469a6aa013aa6e7ed96eab` |
| `checker-stderr.txt` | empty |

**Root's captured source.** All 1360 files matched `capture.json` by path, sha256 and size, with no extra files and no symlinks. The report's before/after hashes of the three probed files are stable.
- `capture.json` names the active f561 tree as its origin. That tree was **not read**.
- At the final summary, root's inputs and captured source were re-verified as unchanged.

**Copies:**
- **Original runtime.** A regular per-file copy became `work/source`: distinct inodes, `st_nlink == 1`, byte-equal.
- **Frozen baseline tree** `work/baseline`.
- **Hybrid tree** `work/hybrid-baseline-owner`: baseline owner files plus the edited checker only.

**Continuation carry** (`receipts/c00-carry.json`). Every carried file is a regular copy with a per-file hash and its source path.
- **Original runtime manifest:** 4141 files, sha `92ee845d…`.
- **Carried content:** 32 completed original receipts, the 8 original probes (verbatim), the delta, the baseline root-probe directory, and both authored trees.
  - `work/source` and `work/hybrid-baseline-owner` are byte-equal to their expected hashes.
  - `work/baseline` was verified in place.
- **Continuation probes** (`run`, `p02_battery`, `p03_rootprobe`, `p04_semantic`, `p06_compare`) differ from the originals only by one replaced BASE path literal each.

### Interruption account

In the original runtime, four jobs were launched in the background:
- `p02_battery source`
- `p02_battery hybrid-baseline-owner`
- `p03_rootprobe source`
- `p04_semantic source`

The original main process then exited with a status-only response while they ran. **They never completed:**
- no receipt or result exists;
- nothing was still running when the continuation began;
- the only leftovers are zero-byte checker stdout/stderr files, plus the root-probe `probe.py` copy and its `source` symlink.

Those leftovers are preserved under `interrupted/`, with hashes in `c00-carry.json`. The four jobs were then **re-executed as new, distinct continuation executions** on the carried trees; these are not the original jobs completing. Their receipts in this runtime record continuation start and finish times, all after the status-only main turn.

## 2. Defects demonstrated at baseline (actual fixture)

The fixture is the checker's own fully closed `cw_pos` Run, `run3:77cbc8c2…724d`. A separate `identity-model.v3.close_run` re-admits it to that exact ID, and `identifier('run', run)` agrees.

1. **The wrong Run ID is admitted.**
   - **Root's report (`444c1ab5…`).** It showed the same retained closure and Plan with `runId run3:aaaa…` being admitted, producing `evidenceRunId run3:aaaa…`.
   - **Reproduction.** Root's `probe.py`, run byte-for-byte against my baseline copy, returns exactly root's calls. Its checker stdout is byte-identical (`fbeafa10…`).
   - **Beyond an arbitrary ID.** Two further Runs, **`cw_dyn` (`run3:1915ed30…`) and `cw_neg` (`run3:1384f41e…`)**, are admitted by the checker's `close_run`, re-admitted here, and share `cw_pos`'s Plan with different evidence.
   - **Result at baseline.** Naming `cw_dyn`'s ID over `cw_pos`'s closure, and the reverse, both **ADMIT**. The dyn-named plan over `cw_pos` evidence minted `repairplan2:85e90242…`, identical to `cw_dyn`'s own lawful plan.
2. **A foreign exception with the same name is misrouted.** An unrelated class named `RetainedEvidenceUnavailable`, raised from `matched_findings`, was turned into `REQUEST.PRECONDITION_FAILED` / `REPAIR.EVIDENCE_RUN_UNAVAILABLE` because the owner compared class names.
3. **Same defect class, found while testing:**
   - A declared missing record read by the closed-world selector through the checker's **separate selection-module instance** view escaped as a raw exception instead of the typed route. The selector matched only the owner instance's own class.
   - An undeclared duck-typed view was normalized by class name.

## 3. Correction

- **Delta:** `delta-vs-captured-source.diff`, sha256 `b7c04ff851d1912df37cd91f8e911f6c8c133adf6dee6a4c0ec2a4b31ed41495`, 218 lines, against root's captured source.
- **Scope of change:** exactly four owned files, none added or removed.
- **Check:** the continuation re-derives this diff and compares it byte-for-byte with the carried original (`receipts/c05-summary.final.json`).

| File (`docs/coop/design-corrections/workflows/`) | Before | After |
|---|---|---|
| `workflows_model.v3.py` | `3ba50985fc82ea5dbcc6b5a1487a8373a59938a4d1a310d8e41736fd1ad7f504` | `ae7fc67313daa7eb81e6740cf17432eca572951717eb63708b5b8d682506c95c` |
| `repair_closed_world_selection.v1.py` | `c92ea49d3d488809f3137493d8adc16051bdc7e8d9ce37c30018eda32389da5d` | `08fb9b72a5de0e06d5c8e194c020eb3b62db3dae57d5bcd7e441fdd77bd43bc5` |
| `workflow-projection-contract.v3.md` | `3bdb5c1e6e03033f093c7c096e61b6205781967e8a7d3810489bef4775cfd60d` | `1650e55257bc6d9e4bdb4e7ba03473cb7156189190915c4a14231addc94530df` |
| `check-workflow-projection.v3.py` | `56647271dbd7b288f2b3274ac4d4e394b6ba503147f5c39cedc7887b9d5fddc2` | `a34824d02ede6bd26bc514531ecc2bf146b0e35722d0420eae1676a5d5db7e25` |

`docs/v2/contracts/product-v1/workflows-and-surfaces.md` is unchanged (`27fe512a…`). Its §6 already requires targets present in that Run, with authority in the sealed Run named by `evidenceRunId`, so no paragraph was needed.

### Owner selectors

**`workflows_model.v3.repair_preview`**
- **Identity join.** After the existing authority → retained → run3 → `planId` checks, it refuses `REQUEST.PRECONDITION_FAILED` / `REPAIR.EVIDENCE_RUN_UNAVAILABLE` unless `run['runId'] == identity_owner().identifier('run', retained.run)`. This happens before `matched_findings` and before the shared builder, so no descriptor exists.
- **Delegation.** The Run identifier is delegated to identity-model.v3's own `identifier` (the one `open_run_closure` uses), loaded as this profile's private instance. There is no new hashing recipe, and the closure is not re-admitted: it was already admitted under the adapter precondition.
- **Target join.** The target-join `except` catches only `retained_unavailable(retained)`, re-raises unless `type(exc)` is exactly one of those classes, and otherwise propagates.
- **Docstring** updated to match.

**`workflows_model.v3.evaluator3_closed_world`**: the selector `except` uses the same declared exact classes.

**New `workflows_model.v3.retained_unavailable(retained)`** returns:
- the owner selection instance's `RetainedEvidenceUnavailable`;
- plus `type(retained).UNAVAILABLE`, if that attribute is an `Exception` subclass class.

It consults no names, no message text and no blanket catch.

**New `workflows_model.v3.identity_owner()`**: a lazy file loader in the pattern of the existing `atom_owner`/`projection_owner`.

**`repair_closed_world_selection.v1.RetainedRunView.UNAVAILABLE = RetainedEvidenceUnavailable`**: the declared class of each module instance. This solves the separate-instance problem without names.

**`workflow-projection-contract.v3.md` §5, "Preview constructor" bullet** gains three sentences:
- "Another Run" is exact identity: `planId` must be the retained Run's, and `runId` must equal `identifier('run', …)` of the retained Run record.
- Unavailability maps only for the declared owner class, by exact class identity.
- Other exceptions, including a same-named class, propagate; the trusted-adapter scope qualifies no host, snapshot or trust.

**`check-workflow-projection.v3.py`**: 19 new `oc1-*` controls, inserted after `oc1-current-constructor-keeps-authority-first`.

### Preserved

- **Historical major-1:** `workflows_model.v1.py` is untouched (`be37023f…`). The constructor/API, the keyword-only `descriptor_major=1` and the historical-profile oc1 checks all still pass.
- **repair:2:** schema and recipe unchanged; no schema, registry or D9 code added.
- **Refusal order unchanged:** authority first; run2 → `EVALUATION.MIXED_OUTPUT_MAJOR`; another `planId` → unavailable.
- **Other laws:** source38 host, termination, native and query laws are untouched.

### Design choice

The declared attribute on the trusted retained adapter is the smallest explicit interface that works across separate module instances. Alternatives rejected:
- **Name matching** is the defect itself.
- **Catching only the owner instance's class** loses the reference view's lawful route.
- **An owner-created replacement view** would bypass the host adapter's own reads, so host faults would never surface.

## 4. Results, kept in three separate categories

### A. Known unrelated baseline failure (not fixed, not relabelled)

`oc2-owner-string-expression-case-is-policy-imperative-key-refused` (`CONFIG.INVALID/CONFIG.INVALID`) fails in **every** checker run here:
- root's captured run;
- the baseline battery (795 checks);
- root probe on the baseline copy;
- the edited battery (814 checks);
- the hybrid;
- root probe on the edited tree.

The whole-checker exit is therefore **1** in every run. **The whole workflow checker does not pass**, and this correction makes no whole-checker pass claim.

### B. Bounded repair-join controls

**Actual checker, edited tree** (`receipts/p02-source.json`; checker stdout `4ef61c79…`, identical in the root-probe run):
- 814 checks; the only failure is the unrelated oc2.
- **All 19 new controls pass**, and all 794 previously passing controls still pass.

**Hybrid: baseline owner files plus edited checker** (`p02-hybrid-baseline-owner.json`). It fails exactly oc2 plus these **9** new negative controls:

| Control | Baseline outcome |
|---|---|
| `…same-retained-closure-and-plan-with-another-run3-id-refuses-before-descriptor` | ADMIT |
| `…admitted-dyn-run-id-over-the-positive-run-closure…` | ADMIT |
| `…positive-run-id-over-the-admitted-dyn-run-closure…` | ADMIT |
| `…admitted-neg-run-id-over-the-positive-run-closure…` | ADMIT |
| `…positive-run-id-over-the-admitted-neg-run-closure…` | ADMIT |
| `…each-selection-instance-view-declares-its-own-unavailability-class` | no declaration |
| `…declared-missing-retained-subject-maps-typed-for-a-reference-instance-view` | PROPAGATE raw |
| `…foreign-same-name-exception-from-matched-findings-propagates-as-the-same-object` | REFUSE (misroute) |
| `…an-undeclared-view-raising-a-separate-owner-instance-class-is-not-normalized` | REFUSE by name |

The other 10 new controls pass on both owners:
- the lawful preview;
- the shared-Plan fact;
- both admitted Runs' own previews;
- the missing finding, for both instances;
- the missing subject, for the owner instance;
- the foreign exception from `coverage_records`;
- the host fault;
- the builder-restoration check.

**Battery on the edited tree** (same actual fixture; a spy on the shared builder counts calls, and zero calls means the refusal came before any descriptor):

| Case | Baseline | Edited |
|---|---|---|
| lawful `cw_pos` preview | ADMIT `repairplan2:ccb3795c…`, `evidenceRunId` = actual Run | **ADMIT**, identical plan |
| same closure and Plan, `runId run3:aaaa…` | ADMIT with the wrong `evidenceRunId` | **REFUSE** unavailable, builder calls 0 |
| `cw_dyn` own preview (second admitted Run, shared Plan) | ADMIT `…85e90242…` | **ADMIT**, identical |
| `cw_dyn` ID over `cw_pos` closure / `cw_pos` ID over `cw_dyn` closure | ADMIT / ADMIT | **REFUSE / REFUSE**, builder calls 0 |
| another `planId` | REFUSE | REFUSE, builder calls 0 |
| declared missing finding record: reference-instance view / owner-instance view | REFUSE / REFUSE | **REFUSE / REFUSE**; the `__cause__` class is exactly that instance's class; builder calls 0 |
| declared missing `evaluation-subject` records, read in the selector: reference / owner view | PROPAGATE raw / REFUSE | **REFUSE / REFUSE**; cause is exactly that instance's class; refused inside the selector, before the descriptor |
| probe-local `RetainedEvidenceUnavailable` from `matched_findings` | REFUSE (misroute) | **PROPAGATE, exact same object** |
| same, from `coverage_records` | PROPAGATE | PROPAGATE, exact same object |
| `OSError` host fault from `matched_findings` | PROPAGATE | PROPAGATE, exact same object |
| undeclared duck-typed view raising the reference class | REFUSE (by name) | **PROPAGATE, exact same object** |

**Root's `probe.py`, byte-for-byte, on the edited tree** (`p03-rootprobe-source.json`, report sha `c5285ad6…`):
- `lawful` is ADMIT, byte-equal to the baseline row.
- `same-retained-closure-and-plan-but-wrong-run-id` is REFUSE, `REQUEST.PRECONDITION_FAILED` / `REPAIR.EVIDENCE_RUN_UNAVAILABLE`.
- `foreign-same-name-host-exception` records class `RetainedEvidenceUnavailable` with `errorCode` null. Root's probe files every non-Refusal exception under the label "REFUSE" with its class name, so this is the foreign exception propagating out of `repair_preview`, not a Refusal. Exact-object identity is shown by the battery and checker controls above.

`receipts/p06-compare.json` checks every expectation above: **allOk**.

### C. Semantic and full-Run checks that genuinely pass

- **Full Runs.** `cw_pos` is fully admitted, and a separate `identity-model.v3.close_run` re-admits it to `run3:77cbc8c2…`. `cw_dyn` is likewise re-admitted to its own ID. Both hold on the baseline and edited trees.
- **Complete semantic golden replay** (`foundation/check-semantic-replay.v3.py`, unmodified):
  - **passed, 31 goldens, `blocked []`** on both baseline and edited trees;
  - byte-identical stdout (`590532fb…`), which is expected because this delta touches no foundation file.

## 5. Commands executed

- **Original runtime, completed and carried:**
  - `p00_copy`, `p01_tree baseline`, `p01_tree hybrid-baseline-owner hybrid-checker`
  - `p02_battery baseline`, `p03_rootprobe baseline`, `p04_semantic baseline`
  - `p05_summary` (non-final)
- **Original runtime, interrupted** (no receipt; §1): `p02_battery source`, `p02_battery hybrid-baseline-owner`, `p03_rootprobe source`, `p04_semantic source`.
- **Continuation:**
  - `c00_carry`
  - `p02_battery source`, `p02_battery hybrid-baseline-owner`, `p03_rootprobe source`, `p04_semantic source`: each exit 0, polled to completion in the same turn.
  - `p06_compare` (exit 0)
  - `c05_summary final`

All receipts, with digests and the execution origin of each, are in `receipts/c05-summary.final.json`. No child process remains running.

## 6. Limits

- **Trusted declaration.** The adapter's `UNAVAILABLE` declaration is trusted exactly like the rest of the adapter, within the existing already-admitted host-adapter scope. An adapter declaring an overly broad class (for example `Exception`) would widen normalization. That lies outside the trusted scope and is not defended here; only `Exception` subclass classes are accepted, and anything else is ignored.
- **Undeclared views.** Duck-typed views without a declaration now get only the owner's own class normalized. This is an intentional behaviour change from the name-based baseline.
- **Synthetic fixture.** The adapters are synthetic fixture adapters over real admitted Runs. Nothing here qualifies a host, snapshot, storage read, trust or product.
- **What the identity join does and doesn't prove.** It proves that the request names the retained Run record's exact identity. It does not re-admit or authenticate the closure; that remains the host precondition.
- **Checker scope.** Only the focused workflow checker, root's probe, the batteries and semantic replay were run; the six global groups were not. The whole workflow checker still exits 1 because of the unrelated oc2 failure.
- **No acceptance claimed.** This is not final-source independent review and not aggregate design acceptance.
