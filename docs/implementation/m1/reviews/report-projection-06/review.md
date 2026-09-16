# RESUMED INDEPENDENT DELTA REVIEW: report projection author-06 (`m1-report-projection-subject-06`)

This review continues the review-05 reviewer; it is not a fresh session. Review-05's "root run pending" note is historical and was not edited.

**Verdict: CHANGES REQUIRED** — three required findings, none blocking.

**Scope.** Proposed carrier, semantic joins and owner clarifications only. No report design, browser UI, assets, M1, performance or release acceptance. All 11 report-feature design blockers, AUDIT-G10, RP-OBL-C01/C02/K01/P01/L01 and RP-DO-12 stay open, and the planning and query-fixture records remain proposals.

## Custody

**Subject identity:**

| Item | Value |
|---|---|
| Outer manifest | `3b3153ced5c08fa0e8e858bc1ffc0c58278302fd5a63b3fafb59c97e7fc3131c` (20 files, exact set) |
| Inner manifest | `3b7bdc8b…708fd5` (lists 19) |
| envelope5 | `45de2b0a…` (unchanged) |

**Before review:** 82/82 pins and 3/3 listings re-hashed with no drift. Three pins were added since subject-05 (query model, query contract, evaluator projection registry); none changed or were removed. The after-verification is in `work/after-verification.json`.

**Root's retained validation** in `docs/implementation/m1/trials/report-projection-06/root-validation` equals the mutable origin byte for byte, including the wrong-cwd stderr.

**Strict run** from the exact copy (`work/closure`, cwd = copy, own `TMPDIR`, `-I -B`, fresh prefix): exit **0**, `declared-out writes observed: 1`.

| Item | Count |
|---|---|
| Report cases (accepts) | 184 (28) |
| Envelope cases | 31 |
| Metadata cases | 43 |
| Aggregate cases | 22 |
| Delivery goldens (scenarios) | 64 (16) |
| Pending goldens | 8 |
| Static parity goldens | 17 |
| Coverage rows | 323 |
| Pins / listings | 82 / 3 |
| Child processes | 0 |
| `documentMaxBytes` | 27,828,318 |

## Root run

- **Initial run: did not pass.** From the architecture cwd, `bytecode_demo`'s `shutil.rmtree` issued `os.open('__pycache__', dir_fd=…)`. The hook resolved that name against cwd, producing `UNPINNED-LOAD <arch>/__pycache__`.
- **Rerun:** passed from the documented copy cwd.
- **My reproduction:**
  - from a governed cwd, the check **fails** the same way and leaves its scratch directory behind;
  - from `/`, it **passes**.

So the supported scope is a cwd that is the subject copy or non-governed, and the contract does not say so (RPR6-1).

## Review05 dispositions

### RPR5-1: closed, with residual RPR6-3

**Regenerated switches:** S1 gives `J-LEDGER-DAG` in 6/6 bases, and S2 gives `J-LEDGER-PLAN` in 6/6.

**New mutants, all refused:**

| Mutant | Code |
|---|---|
| fit render `dependsOn [1]` | `J-LEDGER-PLAN` |
| fit render gate `completed` | `J-LEDGER-PLAN` |
| query `planRole` import | `J-LEDGER-PLAN` |
| no-pivot labelled with-pivot | `J-LEDGER-PLAN` |
| swapped pivot/primary roles | `J-LEDGER-PLAN` |
| comparison drops pivot dependency | `J-LEDGER-PLAN` |
| envelope names the pivot Run | `J-LEDGER-RUN` |
| default ledger ephemeral | `J-LEDGER-MODE` |

The analyze ephemeral control is accepted.

**Owner shapes.** The bound default and audit no-pivot shapes equal the owner `workflow-cases.v1.json` invocation cases.

**Stated limitation.** `validate_dag` ran on role-bound params only. Probe B lists the unbound required StepSpec params. No full workflow replay is claimed.

### RPR5-2: closed

The owner `finish_operation` computes units, applies caps, then slices, and refuses out-of-prefix or foreign cursors.

**I executed the owner model independently:**
- **Neighbors over 100,001 facts at page size 100:**
  - pages 1 and 2 are 100000/100000 lower-bound truncated-page with contiguous rows;
  - the page at position 99,900 is truncated-bound with no cursor;
  - there is no count reset across pages.
- **Cursor faults:** a cursor at position 100000, a cursor bound to other params, and a malformed cursor are all refused.
- **Other walks:** a reach with a visited cap of 5 and an exact 7-by-3 neighbors walk are lawful.
- **Report page law:** every owner page is lawful at its position.

The correction's before-texts match the pinned lines. Residual: A2.

### RPR5-3: closed, with residual RPR6-2

**Probes on the pinned join:**
- the audit pivot golden with 2 details is accepted exactly;
- omitting the second detail, duplicating and reversing are refused;
- the fit golden is accepted; an earlier indeterminate detail is excluded; a missing ledger join is refused.

**Consistency with root.** The rule matches root interruption04's exact in-step-order join. The empty form stays pending (`SCHEMA-ENV`).

### Advisories A1–A7

| Advisory | Disposition |
|---|---|
| A1 | Fixed; verified by code inspection only (the scratch exemption uses the realpath only). |
| A2 | Kept as host assertion. |
| A3 | Kept. |
| A4 | Kept. |
| A5 | Recorded as RP-OBL-C02. |
| A6 | Outside the claim. |
| A7 | Open. |

## Required findings

### RPR6-1: the hook misattributes dir_fd-relative opens, and the cwd scope is unstated

**The cause.** CPython's "open" audit event carries no `dir_fd`, and `norm()` resolves relative names against cwd.

**Evidence** (`fd_relative_poc.out`, with the subject hook and loader installed):

| Probe | Setup | Result |
|---|---|---|
| (a) false admission | fd on the non-governed parent `/Users/sb/code/opensip-ai`, cwd `/`; `os.open('opensip_arch/docs/implementation/README.md', dir_fd=parent)` | **Reads the unpinned mutable README (8,763 B)**; the absolute spelling is refused |
| (b) false refusal | governed cwd; `os.open('etc', dir_fd=fd('/'))` | Refused `UNPINNED-LOAD …/work/poc/etc` |

The root and governed-cwd failures above are the same defect.

**Correction:**
- Refuse (or treat as unattributable) non-absolute path events under the hook.
- Remove scratch without relying on dir_fd-relative events.
- State the supported cwd, or make the result independent of it.
- Add probes for governed cwd and dir_fd-relative access, or list dir_fd access as an explicit exclusion.

### RPR6-2: a fabricated skipped-step detail is laundered into interruption errors

**The gap.** `recorded_failure_details` does not exclude skipped outcomes, and `J-LEDGER-SKIPPED` does not constrain the skipped termination. The owner skip termination has no detail (`workflows_model.v1.py:306`).

**Probe E.** I placed a fabricated `evidence.purged` detail on the skipped query of the fit golden:
- `errors = [CONFIG.INVALID, fabricated]` is **accepted**;
- `errors = [CONFIG.INVALID]` is refused.

The author's "skipped termination is not a detail" case only covers the omission.

Interruption04's filter (`outcome != cancelled`) shares this gap.

**Correction:**
- Exclude skipped steps.
- Require the skipped termination to equal the owner skip termination exactly.
- Add cases for both.

### RPR6-3: the planning record omits conditional expansions and mis-binds a param

**analyze `--baseline`.**
- Workflows `:1097` lists `analyze [--ephemeral] [--baseline]`, but the inventory has no `--baseline` flag.
- The report schema *requires* a comparison panel and view for analyze, yet the only plannable analyze variant has no comparison step, so that panel is always not-selected.
- This conflict is not recorded as an obligation (P01 covers import only).

**Optional steps.**
- The owner exercises an optional `export-delivery` step (case `optional-export-failure-keeps-success`; prose `:1145`).
- The subject's own goldens use optional renders.
- The record claims "exact expansions" but has no optional render or export variant.

**repair-preview.** The binding `evidenceSource` is the string label `"runId"`, while the schema requires `oneOf {step}|{runId}` objects. The `{step}` exclusion matches the inventory but is not stated.

**P01.** Its non-blocking standing is supported: the only owner import case is a fully optional profile chain. Whether analyze import is in M1 scope still needs an explicit root decision.

**Correction:**
- Record the analyze `--baseline` decision or obligation, and state comparison-panel reachability.
- Add optional render/export variants, or mark those goldens as non-builtin.
- Express bindings in schema form and state the `{step}` exclusion.

## Advisories

- **A1:** C01 and C02 cite superseded parents (envelope subject-01 / review-01 text; successor03). Root's current correction is interruption04 (`0cfda57a…`). Standing is honestly pending; update the pointers at rebase.
- **A2:** the corrected fixture keeps `visitedNodes 4` on neighbor rows, but the owner model gives 1 for neighbors. It is count-lawful, not owner-reachable.
- **A3:** planning `validate_dag` evidence is binding-param only; do not present it as StepSpec admission.
- **A4:** K01 is pending (root coverage correction01 is under review, not selected) and L01 is unchanged. No premature completion was found.
- **A5:** RP-DO-03/05/09/10 and 11 are authored separately; all 11 remain blockers here.

## Limits

- No full retained-Run `execute_graph_query` replay; the controls used `traverse_projected_graph`, which shares `finish_operation`.
- No full StepSpec or `run_invocation` replay of the bound variants.
- The A1 fix was not re-probed.
- Hard links, native modules and TOCTOU remain outside the claim.
- Interruption04 was read for its join rule only, not reviewed or adopted.
- No private sessions or author responses were inspected.

## After-verification

See `work/after-verification.json`: outer, inner and envelope5 SHAs, 20/20 exact set, 82 pins and 3 listings, closure copy unchanged, and no `__pycache__`. No commit or push was made.
