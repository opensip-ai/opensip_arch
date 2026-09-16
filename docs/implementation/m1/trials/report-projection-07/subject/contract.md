# Report projection and fit successor contract (author-07)

## 0. Standing

This is an **author-07 correction candidate** answering the resumed independent review `m1-report-projection-review-06` of frozen `m1-report-projection-subject-06` (outer manifest `3b3153ce…3131c`). It covers RPR6-1..3, advisories A1–A5, root direction on analyze `--baseline` and optional delivery, and the accepted K01 unit. It is not approval; independent review and root assent are still required.

History is preserved unchanged: subject-06, its first wrong-cwd root run (which failed on `shutil.rmtree`'s dir_fd-relative open) and review-06.

**Readiness:**

| Scope | State |
|---|---|
| Carrier unit | Candidate for review |
| Report design | **Blocked**: all 11 feature blockers (RP-DO-01, 03..12) stay open until the final selected carrier integration |
| M1 final integration | **Blocked** by RP-OBL-C01 and RP-OBL-C02. RP-OBL-K01 is closed by the accepted unit. |
| M5 workflow delivery | Also **blocked** by RP-OBL-P01 (analyze import) and RP-OBL-X01 (optional delivery selection) |
| AUDIT-G10 | Open |
| Whole project | **Not complete** while any of these are open |

**Separate work, referenced but not adopted or duplicated:**
- evidence candidate `m1-report-evidence-design-subject-01` (`0af84231…`) for RP-DO-03/05/09/10;
- timing candidate `m1-workflow-timing-subject-01` (`be0d1062…`) for RP-DO-11;
- presentation catalog `m1-presentation-catalog-subject-01` (`22479d58…`) for RP-DO-01/06/07/08;
- root security work (RP-DO-04) and history work (RP-DO-12), both ongoing.

**Parents:**
- envelope5 is unchanged (`45de2b0a…789d`).
- Interruption correction05 (`m1-interruption-envelope-subject-05`, `34556f3f…530f`; envelope6 schema `fd2663c2…` unchanged) is under review and **not adopted**.
- The pending references now point to correction05 instead of 01/03/04.
- **inventory5 bytes change this round** (analyze grammar, flag and golden text; §2 RPR6-3). That is recorded for root's rebase of any record that pinned the earlier inventory5.

**Not claimed:** no runtime, browser, generator, performance, product installation or general process confinement.

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists 19 files and excludes only itself.

**Run from a copy of exactly the listed files, from any cwd:**

`TMPDIR=<existing absolute dir> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B <copy>/check.py --architecture ARCH --subject-strict --out <absolute result path>`

**Closure (trusted reference only).**

| Aspect | Rule |
|---|---|
| Pins | 85 files and 3 listings, verified before import, re-hashed at every governed open, listings recomputed at use. New pins: the accepted `coverage-prerequisite-unit.v1.json`, its `subject-manifest.json` and `implementation-coverage.v3.json`. |
| Unattributable events (RPR6-1) | CPython's open/listing audit events carry no `dir_fd`. **Every open, listdir or scandir event whose path is not absolute (relative names, dir_fd-relative names, fds) is refused `UNATTRIBUTABLE-PATH-EVENT` before any byte is read**, whatever the cwd or target. Relative events are never cwd-normalized and never exempted, in trace mode as well. |
| Cwd independence | Declared paths (`--architecture`, `--out`, `--trace-closure`) are resolved to absolute paths once, before the hook, so the result does not depend on the invocation cwd. |
| Scratch | Removed by `remove_owned_tree`: absolute scandir, lstat-based kind, unlink/rmdir, no symlink following and no dir_fd-relative open. `shutil` is no longer imported. |
| In-process probes (`unattributablePathProbe`) | Every probe is refused `UNATTRIBUTABLE-PATH-EVENT` and cwd is restored:<br>• review-06 PoC (a): an fd on the non-governed architecture parent with cwd `/`, then `os.open("opensip_arch/docs/implementation/README.md", dir_fd=…)`;<br>• PoC (b): cwd = architecture, `os.open("etc", dir_fd=fd("/"))`;<br>• an fd listing, a relative `open` and a relative `scandir` under the architecture cwd. |
| Other controls kept | alias probe (exact, case-variant, `..`), bytecode demonstration, fresh-source loader, refusal of child processes, declared out path write-only (observed-writes line) |
| Explicit limits | trusted host and interpreter; hard links planted outside the roots; native extensions; concurrent-writer TOCTOU; no general process confinement |

## 2. Finding-by-finding disposition (review06)

### RPR6-1: hook misattributes dir_fd-relative opens; cwd scope unstated — corrected

The unattributable-event refusal, owned scratch removal, absolute argument resolution and in-process probes are described in §1.

The strict check runs from the exact frozen copy with three cwds: the copy, the architecture checkout, and `/`. All three give identical outcomes; see `scratch/closure-evidence.json`.

### RPR6-2: fabricated skipped detail laundered into interruption errors — corrected

**Detail list.** `recorded_failure_details` excludes **skipped and cancelled** steps. It keeps optional-step failures, matching correction05's filter.

**Exact skip termination.** `J-LEDGER-SKIPPED` (ledger) and `J-ENV-INTERRUPTION-DETAIL` (envelope join) require every skipped step's termination to be exactly the owner skip record `{class: request-rejected, errorCode: REQUEST.PRECONDITION_FAILED}`, with no domainDetail. Actual owner skips carry none (`workflows_model.v1.py:306`), and the owner `run_invocation` runs in §2 RPR6-3 re-assert this for every skip they produce.

**Deterministic error rule on every before-settle interrupted carrier** (aligned with correction05's selected proposal; not an adoption of it):

| Carrier | Recorded detail list | `errors` |
|---|---|---|
| any | nonempty | exactly that list |
| failure | empty | `[]` (envelope5 refuses: pending envelope6, RP-OBL-C01) |
| run | empty | absent (envelope schema forbids empty errors there) |

**Cases:**

| Case | Outcome |
|---|---|
| proper real error only | accept |
| review-06 probe E (fabricated skipped detail carried) | refused |
| fabricated skipped detail not carried | refused (fabricated skip termination) |
| cancelled-step detail not carried | accept |
| cancelled-step detail carried | refused |
| run carrier with no details and errors absent | accept |
| run carrier with `errors []` | `SCHEMA-ENV` |
| run carrier with the real pivot detail | accept |
| run carrier with that detail omitted | refused |
| run carrier with an invented detail | refused |
| ledger: fabricated skip detail, or another class on a skipped step | `J-LEDGER-SKIPPED` |

**New delivered golden** (4 formats): audit with pivot rejected, primary committed, comparison skipped and SIGINT during render. The `kind=run` interrupted carrier, with `runId`, carries `errors = [pivot detail]`.

**Host duty (C01 closure criterion):** record every composed route detail when each step is recorded, not only when an interruption occurs.

**C02.** The optional-Run one-line owner successor stays unaccepted and pending. The settled D9 aggregate is unchanged (required-only).

### RPR6-3: planning omits conditional expansions and mis-binds a param — resolved concretely

**analyze `--baseline PATH`** (root direction; bounded owner choices recorded in `owner/builtin-step-planning.v1.json#/analyzeBaselineDecision`).

*Grammar* (owner: workflow):
- `owner/command-inventory.v5.json` `/commands[name=analyze]/cli` changes from `opensip analyze [--ephemeral]` to `opensip analyze [--ephemeral | --baseline PATH]`.
- Flag `--baseline` (owner workflow, class selection, value exactly one UserInputPath) is inserted after `--ephemeral`.
- Passage overrides: workflows-and-surfaces line 1097 (`analyze [--ephemeral | --baseline PATH]`) and line 1103 (compares against the admitted baseline and never adopts one; refused with `--ephemeral` before planning).
- The audit-only flags `--audit-profile`, `--closure-bundle` and `--accept-origin` are not added. An unmapped project stays `BASELINE.PROJECT_UNMAPPED` indeterminacy.

*Variants:*
- `baseline-no-pivot`: delegated authoritative primary analysis → comparison[0] (`currentStep` 0, `baseline` PATH, `auditProfile` **code-regression**, the existing default audit profile) → render[0,1].
- `baseline-with-pivot`: pivot analysis (profile `pivot`, `pivotOfStep` 1, `pivotClosureIds`) → delegated primary → comparison[0,1] (`pivotStep` 0) → render[0,1,2]. It applies under the existing pivot condition.
- Ordinary analyze keeps `verdictGate` self.
- Retained baseline admission, custody, current trust, pivot resolution, project correspondence and no-latest-fallback are the existing §2/§3 laws.

*Ephemeral with baseline.* `--ephemeral` with `--baseline` is refused **before planning**: `REQUEST.UNSATISFIABLE` / `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`, exit 2. That is the inventory golden route, verified. Evidence for the pre-planning placement: if planned anyway, the owner `validate_dag` gives `WORKFLOW.VERDICT_GATE_UNBOUND` (no-pivot) or `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` (pivot). The report ledger refuses an ephemeral baseline plan as `J-LEDGER-MODE`.

*Contradiction resolved explicitly.*
- Inventory golden `analyze-ephemeral-required-authority` said "--ephemeral combined with --baseline adopt…".
- Analyze has `writesTrackedIntent=false`, and §8 limits tracked-intent writes to `policy init`, `waive` and `baseline adopt|export|upgrade`, so analyze `--baseline` cannot adopt.
- Exact before/after in `owner/command-inventory.v5.json` `/goldens[id=analyze-ephemeral-required-authority]/situation`: "--ephemeral combined with --baseline adopt or a repair prerequisite" becomes "--ephemeral combined with --baseline PATH (the comparison needs an authoritative current Run) or a repair prerequisite; baseline adoption is the separate baseline adopt mutation". Class, code and exit are unchanged.

*Report reachability.* The analyze comparison panel is reachable exactly for baseline variants (new base `analyze-baseline-run`). Ordinary analyze keeps it not-selected; a present panel there is refused `J-COMPARISON-ID`.

**Optional delivery.**
- **Owner-bound variant.** Owner goldens `analyze-optional-export-failed` and `interrupted-after-settle` bind an optional export sink to analyze, which challenges an "exact 8 builtin" claim that excluded it. Analyze therefore gets `primary-with-optional-export`: analysis → render[0] (required) → export-delivery[0] (optional, terminal, `sourceStep` 0, required false). New base `analyze-with-optional-export`; the export step stays unrecorded during render projection.
- **Sink selection.** The source is undeclared (no grammar or configuration owner), so it is tracked as **RP-OBL-X01**. X01 is not an M1 blocker but is required before M5, and appears on the coverage rows `commands:analyze`, `workflowGoldens:analyze-optional-export-failed` and `workflowGoldens:interrupted-after-settle`.
- **Generic compositions.** The optional-**render** delivery goldens (8 of 68 rows) are now labelled `planningOrigin: generic-profile-d9-composition`. They claim no builtin plan admission, and the core CLI has no generic profile surface (X01). The primary requested output stays required.

**repair-preview.**
- The binding is now schema form: `evidenceSource` is an object requiring `runId` and forbidding `step`. The representative value is `{runId: <bound Run>}`.
- The `{step}` form needs an earlier analysis step, so it belongs to a profile, not this builtin.
- Controls: the `{step}` form is refused by the binding; subject-06's string `"runId"` is refused by the owner `RepairPreviewParams` schema.

**Full schema-valid representative StepSpecs (A3).** Every plannable variant's representative params are validated against:
- invocation:3 `StepSpec`;
- the variant's params-binding schema;
- the whole `InvocationRecord` (schemaMajor 3).

They pass the owner `validate_dag` with the same mutant codes as the report DAG law.

**Actual pure owner model.** `workflows_model.v1.py run_invocation` is executed on every plannable variant: all-completed, first step rejected, SIGINT before the required render, and an optional export fault. Its aggregate and exit equal `report_model.invocation_aggregate` on the projected results. For example, analyze `baseline-with-pivot` with the pivot rejected gives outcomes rejected, completed, skipped, completed and aggregate request-rejected. The optional export fault gives success.

**P01 M1 scope (root decision).** Unplannable analyze import is **not an M1 exit blocker** (M1 is build/contracts/bootstrap metadata). It is required before M5 workflow delivery and is not a waiver of import features.

### A2: query fixture visitedNodes — corrected

`owner/query-fixture-correction.v1.json` adds `query_surface_projection.v3.py:512` `"visitedNodes": 4,` → `"visitedNodes": 1,`. `graph_ctx` builds neighbors contexts, and the owner neighbors walk enters only the endpoint; the corrected `ctx_lb` inherits 1. Executed owner neighbors pages report `visitedNodes` 1. The closed query prefix law is not reopened.

### K01: now accepted — rebased, workaround removed

- **Base:** the coverage overlay is built on `docs/implementation/m1/trials/coverage-prerequisite-01/subject/implementation-coverage.v3.json` (`1388fd68…`).
- **Unit checks:** `coverage-prerequisite-unit.v1.json` must be ACCEPTED-DESIGN-CORRECTION with root assent and subject manifest `48035089…bf7ff9`; that manifest pins the v3 bytes; v3 must equal historical v2 plus exactly `assets.rs = M1`.
- **Validation:** the owned validator returns **valid** on v3 and on the overlay with **no workaround**, over 323 rows.
- **Negative controls kept:** historical v2 still gives "Missing/extra module milestone prerequisite", and `assets.rs = M6` is refused.
- RP-OBL-K01 is closed by the accepted unit. Product source-lock integration is future.

### Advisories

| Advisory | Disposition |
|---|---|
| A1 superseded parents | Rebased pointers to correction05 in the register, `successor.json` and C01/C02. |
| A2 | Corrected (above). |
| A3 StepSpec | Full representative StepSpec and record validation plus `run_invocation` (above). |
| A4 | K01 closed; L01 unchanged. |
| A5 | All 11 feature blockers kept. |

## 3. Carrier law changes this round

- **Ledger plan roles:** gain `export-delivery`. Plan variants gain `primary-with-optional-export`, `baseline-no-pivot` and `baseline-with-pivot`.
- **`J-LEDGER-MODE`:** also refuses ephemeral with comparison or pivot roles.
- **`J-LEDGER-SKIPPED`:** requires the exact owner skip termination.
- **`J-ENV-INTERRUPTION-DETAIL`:** now covers failure and run carriers.
- **Derived bounds:** computed over plannable variants (render and later steps unrecorded). `documentMaxBytes` is **27,828,517**; the ledger maximum is 19,436,467. Structural bounds only (RP-OBL-L01).
- **Unchanged:** envelope5 host admission, graph page law, byte law, history, provenance and static parity.

## 4. Obligation register (`owner/design-obligations.v1.json`)

| Id | Standing |
|---|---|
| RP-DO-01, 03..12 | report design blockers (proposals; separate candidates referenced) |
| RP-DO-02 | conditional, not selected |
| RP-OBL-C01 | pending integration (correction05), M1 blocker |
| RP-OBL-C02 | pending integration (optional-Run successor), M1 blocker |
| RP-OBL-P01 | pending owner decision; not M1, M5 blocker |
| RP-OBL-X01 | pending owner decision; not M1, M5 blocker |
| RP-OBL-L01 | pending owner statement, non-blocking |
| RP-OBL-K01 | closed by accepted unit |

## 5. Evidence and limits

**`check.py` verifies:**
- closure, alias, unattributable-path and bytecode probes;
- regeneration of 10 owner outputs and fixtures;
- restorations (inventory5 undoes the fit additions, the analyze cli/flag/golden text and the steps description), the 43 metadata cases and the in-process accepted checker;
- coverage on the accepted v3, overrides (9) and the register;
- builtin planning (schema, `validate_dag`, `run_invocation`), owner query paging and fixture correction;
- 22 aggregate cases, 68 delivery goldens (17 scenarios), 8 pending goldens and 19 static-parity goldens;
- **40 envelope cases:** 12 accept, 10 schema, 18 host;
- **193 report cases on 19 bases, each with its exact code:** 30 accept, 29 schema, 15 codec/boundary, 16 envelope host, 49 ledger, 29 graph, 25 other;
- graph controls, byte law, worst case and codec reachability.

**Limits:**
- Representative StepSpecs are schema-valid constructions. Unbound members (format, destination, snapshotSource, sink) are chosen per invocation.
- `run_invocation` uses synthetic owner-shaped results, not retained Run replay.
- The planning, grammar and fixture records are proposals.
- The mock graph owner and fixtures are constructions.
- No product installation, runtime, browser, generator or performance qualification.
