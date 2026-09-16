# Independent Grok review: joint10 combined reference

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-grok-joint-review-10/subject`
**Manifest SHA-256:** `4041658cb3b414c0a9311fee2b86768938df94379625212f41cf9c82a4559436`
**Members:** 1558
**Verdict:** **ACCEPT WITHIN STATED COMBINED REFERENCE SCOPE**

This is not product, milestone, release, or source-promotion acceptance. Standalone Grok coverage-binding acceptance remains standalone; it does not approve this combined successor. Grok coverage S1 is a separate checkpoint and is not delta-accepted here.

## Custody

Verified before work and after.

| Check | Result |
| --- | --- |
| Manifest | `4041658c…9436` |
| Files | 1558 listed = 1558 walk |
| Extra / missing / mismatch / symlinks / bytecode | none |
| Source checkpoint | `e36f301c…b5d9` matches |

Work used only `review/copy` and `review/probes`. `save_checkpoint.py` was not run. Neither repository nor the frozen subject was written.

## Verification executed

`verify_candidate.py grok10` in the private copy (5 phases, 19 check processes):

| Phase | Expected | Observed |
| --- | --- | --- |
| `check_frozen_inputs.py` | 0 | 0 (215 members, 182 external sources, 21 parent snapshot members) |
| `reproduce.py grok10` | 0 | 0 |
| `run_checks.py grok10` | 0 | 0 (**19/19** processes) |
| `check_all_parent_cases.py` | **1** | **1** (194 cases, 183 same outcome, **11** differences) |
| `reconcile_parent_cases.py` | 0 | 0 (11 replacement witnesses, **205** executions, all passed) |

Do not collapse this to 194 unchanged passes. Inventory exit 1 is the documented difference set; reconciliation supplies 11 successor witnesses. Logs: `review/copy/verification-grok10-*.std{out,err}` and `review/results/verification-grok10.json`.

Coverage source checks (included in the 19): 7 groups, including actual retained two-row Run joins, identity-consistent forgeries that pass local hashes and fail `J-EVIDENCE-SOURCE-PREFIX`, ephemeral Plan/evidence local joins (not native replay), and native schema-digest succession.

Author `run_checks.py` plus standing/schema probes are **not** the whole review. Independent executable counterexamples were run against the same copy (`review/probes/independent_executable.py`, 24/24 after two preserved failed attempts).

## Independent executable counterexamples

`review/results/independent-executable.json`. These compile copy bytes and drive combined admission, host join, placement, and finalizer APIs. They are not restatements of `check_coverage_source.py`.

**Coverage vs retained source**

- Actual two-row admitted Run hydrates and host-joins.
- Identity-consistent rehash of row 0 (new payload digest and coverageId, source unchanged) **passes local admit** and **fails** `J-EVIDENCE-SOURCE-PREFIX`.
- Well-formed substituted `evidenceId` **passes local admit** and **fails** host prefix join.
- Substituted `runId` fails local `J-EVIDENCE-SOURCE-RUN`.
- Ephemeral `{planId, evidenceId}` on a retained Run fails local source authority.
- Missing evidence object is `EvidenceUnavailable`, not an empty panel.
- An unlinked hash-valid coverage object in the map does not expand `project()`.

**Standalone item-cap vs combined report cap (scope limitation, not a defect)**

`check_projection` requires `item-cap` prefixes to have `embedded == maxEvidenceEntries` (3956). A standalone `project(..., 1)` panel joins the host at cap 1, but **cannot** be admitted as a combined report evidence panel (`J-EVIDENCE-COUNTS`). Combined shorter prefixes must be byte-budget with rejected whole-row delta, not standalone item-cap. Two early probe attempts assumed otherwise and crashed on `J-EVIDENCE-COUNTS`; they are preserved in `independent-executable-attempts.json` as probe-assumption failures, not subject defects.

**Budget reservation/order**

- After catalog `exploration-budget-exceeded`, a later graph builder is not invoked; the slot stays omitted.
- A later present panel after an earlier budget omission refuses (`later existing panel violates priority`).
- Overlapping builder/terminal, reserved states over cap, and an owner exceeding remaining allowance all refuse.

**Fit interruption / output precedence**

- Composite interruption delivers complete with **exit 130**.
- The same envelope with a failing writer is **exit 4** / `OUTPUT.SERIALIZATION_FAILED`, not 130.
- After-commit user-signal / transport-close / optional-delivery-failure keep the output fault.
- Second deliver after commit refuses.
- Dropping `advisoryReport` (still shape-valid) writes **no normal bytes**.
- Aggregate/envelope termination mismatch is output-fault exit 4.

## Combined contract (executable, not prose-only)

**One coverage2 per native payload.** Rows are `{coverageId, descriptor, result}`. Local admission checks canonical unique IDs, descriptor identity, registered full-native-document digest (exactly two pinned files with identical reachable `CoverageResultV3` closures), payload digest, and item arithmetic. Frozen report08 still has the old single-`coverageId` stream; this successor does not rewrite those historical bytes.

**Run versus ephemeral authority.** Retained sources are `{runId, evidenceId}`. Ephemeral sources are `{planId, evidenceId}` and confer no Run/history authority. Inventing a Run on an ephemeral document is `J-EVIDENCE-SOURCE-EPHEMERAL`. Host `verify_source_prefix` replays a complete retained Run only; it is not a maximal shared-byte prefix or a storage lease. Ephemeral native custody/replay remains a host duty; current witnesses are shape/envelope joins. Dense fixtures are shape/join controls, not 3956-row admitted Runs. The real retained positive fixture has two coverage rows.

**Native digest succession.** Historical descriptors keep the original raw document digest `2d37b810…`. The composed new-Plan document is a second registered digest. Relabeling retained rows to the new digest is locally hash-consistent and fails the retained-source join. Final native registry selection is still a gate.

**Shared budget.** Projection keeps reservation, priority, stop, item-cap, byte-budget and rejected whole-row delta (`ItemProjectionV1`, Uint53). Standalone experimental uint64 / item-cap-only schema is not the combined carrier. Independently: a standalone item-cap-1 prefix is not a lawful combined-report panel under profile 6's 3956 item cap. Profile is `opensip.report-projection.development-caps.6`; profile 5 documents are schema-refused. Profile 5/6 is an unreleased development carrier; no released wire-major compatibility is claimed. Frozen report08 remains historical caps.4.

**Owner majors.** Generated models record invocation5, query4, envelope7, common4, inventory6. Embedded query panels keep the original owner codec bound inside the larger report profile.

**L01.** Ledger prose uses invocation5 and does not assume a whole-record codec. Structural ledger bound is not a codec proof. RP-OBL-L01 stays open.

## L02 and promotion blockers

**L02 assessment.** The proposed D9 v1.15 view is complete-required-envelope-or-operational-failure: useful work may already be committed; required-output failure then uses `OUTPUT.SERIALIZATION_FAILED` / exit 4; no truncation, empty account, or invented 130-versus-4 precedence. That is a coherent **replacement** criterion for a report-at-render combined candidate.

It **does not** satisfy the original stronger law (preflight rejection before retained selection, or a complete bounded output profile with required parity). The candidate states this honestly (`RP-OBL-L02` status `open-owner-decision`, `blocksM1FinalIntegration: true`, standing “the original preflight-or-complete-profile criterion is not met”). This review does **not** mark the original criterion satisfied.

**Design/source decisions that prevent promotion** (not defects of the stated combined-reference scope):

- L02 remains an unaccepted alternative.
- Development profile 6 is incompatible with profile-5 readers; no released wire major.
- Two registered native schema documents; no final registry selection.
- Ephemeral native source replay unimplemented.
- Shared maximal-byte prefix and storage lease unimplemented.
- RP-DO feature blockers and L01 still open.
- No product adapters, storage, browser, or release qualification.

## Findings

### Must-fix

None in the stated combined-reference scope. Executable coverage binding, host/local split, 205-execution reconciliation, and L02 honesty hold under independent reading plus `verify_candidate.py grok10`.

### Should-fix

**S1. `REVIEW-GUIDE.md` is still a joint09 guide with 8-replacement arithmetic.**

- File: `REVIEW-GUIDE.md` title and §9 (“186 unchanged outcomes and 8 replacements”).
- Trigger: this freeze asks reviewers to read that file for joint10.
- Observed: guide describes joint09 and 8 replacements. Actual joint10 is 183 unchanged + **11** witnesses = **205** executions (`verify_candidate.py` standing, `README.md`, `coverage-succession.md`, `integration-status.json`, this grok10 run).
- Expected: retitle/update to joint10 11-witness arithmetic, or mark the file as inherited joint09 history (`inherited-joint09-README.md` already exists for that).
- Reason: a reader of the guide alone would collapse the 11 documented differences. The executable verifier does not. Not a must-fix of the combined contract.

### Advisories (kept)

- Early-chunk corruption may already be sent; last chunk is content-bound; receiver publication is an M3 duty (inherited from coverage-binding).
- Relation v2 CanonicalPath path-normalization gap remains another unit’s duty.
- Isolation/clean-staging is source-only reproduction, not a hermetic sandbox.
- Synthetic dense rows are not native-admitted full Runs.

## Independent probes

Standing/schema: `review/probes/independent_joint10.py` → **18/18**. Detection that the review guide is stale is a documentation finding, not a passing product control.

Executable combined boundaries: `review/probes/independent_executable.py` → **24/24** (after two preserved probe-assumption failures on item-cap layering). Forged locally self-consistent coverage rows, source substitution, budget stop/order, and interruption-then-output-failure precedence were exercised on the actual combined APIs.

## Commands

Python `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B`. Private copy only.

1. Manifest + 1558-file hash verify; checkpoint pin; copy
2. `verify_candidate.py grok10` (5 phases, 19 checks)
3. Independent standing/schema probes (18)
4. Independent executable admission/projection/output probes (24; two earlier attempts preserved)
5. Completion re-hash of the frozen subject (match)

## Limitations

- Clean-staging `check_clean_staging.py` was not re-run; frozen `clean-staging-coverage06` evidence was read, not regenerated.
- No live storage lease, browser, or production encoder.
- Independent executable probes did re-drive retained `close_run` plus combined `admit` / `verify_source_prefix` / `joint_placement.append` / `Finalizer.deliver`. They do not implement storage leases, live signals, or a 3956-row admitted Run.
- Combined report item-cap is the profile's `maxEvidenceEntries` (3956). Standalone hydration caps are not interchangeable with that law.
- Ephemeral native source replay was not implemented; only local Plan/evidence joins were executed.
- Not Claude, product, or milestone acceptance.

## Verdict restated

**ACCEPT WITHIN STATED COMBINED REFERENCE SCOPE.** The combined carrier binds one coverage2 per native payload, distinguishes retained Run from ephemeral Plan/evidence, keeps historical native IDs, restores shared byte-budget/rejected-delta, and documents 194+11=205 predecessor executions. L02 is an explicit unaccepted alternative and blocks promotion; it is not a false claim that the old criterion passed. Update `REVIEW-GUIDE.md` when convenient. Do not treat this as final source, profile, or product lock.
