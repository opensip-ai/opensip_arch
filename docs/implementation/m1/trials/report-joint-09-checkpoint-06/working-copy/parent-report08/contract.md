# Report projection and fit successor contract (author-08)

## 0. Standing

This is an **author-08 correction candidate** prepared for **one combined independent review** covering both:

1. the **review-06 fixes** first delivered as author-07 (frozen `m1-report-projection-subject-07`, outer manifest `cee1eb24…e6c8`, 20 files). Their independent review is still pending, so their full scope and evidence are carried unchanged in §4;
2. the **interruption integration**: root has accepted `docs/implementation/m1/interruption-envelope-unit.v1.json` conditionally, at design/reference scope only (status `ACCEPTED-DESIGN-CORRECTION-CONDITIONAL-PARENT`, `integrationApproved: false`). Its frozen subject-07 is `bcc63f22…a1a1` (51 files), with trial copy `docs/implementation/m1/trials/interruption-envelope-07`. The integration also includes the new capacity obligation RP-OBL-L02.

It is not approval, and it is not a runtime, browser, M1 or whole-project claim. History is unchanged: subject-01..07, reviews 01..06, the interruption subjects and reviews, and the capacity audit.

**Readiness:**

| Scope | State |
|---|---|
| Carrier unit | Candidate for joint review (envelope5 fit carrier with its envelope6 interruption successor, report-projection:1) |
| Report design | **Blocked**: all 11 feature blockers (RP-DO-01, 03..12) stay open |
| M1 final integration | **Blocked** by RP-OBL-C01 and RP-OBL-C02 (implemented in this candidate, pending joint review and root source selection, not closed) and by **RP-OBL-L02** (open capacity decision). RP-OBL-K01 stays closed by its accepted unit. |
| M5 workflow delivery | Also **blocked** by RP-OBL-P01 (analyze import; workflows lines 148-151 name the import step, so the feature is kept) and RP-OBL-X01 (optional delivery selection) |
| AUDIT-G10 | Open |
| Whole project | **Not complete** |

**Separate owners (referenced, not adopted, no bytes taken, no feature marked delivered).**
- The 11 feature owners remain separate.
- Evidence author-02 and root's presentation, timing, configuration and history proposals are under review `m1-report-presentation-owners-review-01`.
- Evidence subject-01 (`0af84231…`), timing subject-01 (`be0d1062…`), presentation catalog subject-01 (`22479d58…`), and root security (RP-DO-04) and history (RP-DO-12) work remain separate.

**Parents.**
- **envelope5:** bytes unchanged (`45de2b0a…789d`, 36852 B). It is the conditional parent and is **still unaccepted**.
- **envelope6:** `command-envelope.v6.schema.json` (`bdd5d270…3ada`, 39969 B), from the trial copy. It is now the report envelope `$ref`. `check.py` restores it exactly to envelope5 by reversing its only delta (`/allOf/19/then`).
- inventory5 changes only the json renderer row (version 6; its parity rule says major 6).

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists **20 files** and excludes only itself. The one new file is `owner/interruption-binding.v1.json`.

**Run from a copy of exactly the listed files, from any cwd:**

`TMPDIR=<existing absolute dir> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B <copy>/check.py --architecture ARCH --subject-strict --out <absolute result path>`

**Closure (trusted reference only).**

| Aspect | Rule |
|---|---|
| Pins | **96 files and 3 listings**, verified before import, re-hashed at every governed open, listings recomputed at use. |
| New pins (11) | the unit record; the trial `subject-manifest.json`; the trial `command-envelope.v6.schema.json`, `passage-overrides.json`, `model-successor.json`, `successor.json` and `ledger_join.py`; `native/native_evidence_model.v2.py`; `workflow-projection-contract.v3.md`; `audits/envelope-capacity-01/issue.json`; `/tmp/opensip-implementation/m1-envelope-capacity-audit-01/result.json`. No pin was dropped. |
| Executed owner code | Compiled from the verified bytes with no import shim: workflows model pure functions (historical form, plus the successor with exactly line 380 replaced); native `release_absence_notices`, `invocation_availability`, `admit_requested_capabilities` and `PUBLIC_ROUTE_REMEDIES`; the whole `ledger_join.py`; foundation `canonical.py` |
| Unattributable events (RPR6-1) | Every open, listdir or scandir event whose path is not absolute is refused with `UNATTRIBUTABLE-PATH-EVENT` before any byte is read (§4) |
| Other controls kept | alias probe; bytecode demonstration; fresh-source loader; child processes refused; owned scratch removal; absolute argument resolution; declared out path is write-only |
| Explicit limits | trusted host and interpreter; hard links planted outside the roots; native extensions; concurrent-writer TOCTOU; no general process confinement |

## 2. Interruption integration (the conditionally accepted unit)

### 2.1 Exact bindings (`owner/interruption-binding.v1.json`)

| Bound item | Selector / evidence |
|---|---|
| Unit | `interruption-envelope-unit.v1.json`: status, `integrationApproved false`, conditional parent sha = envelope5 sha, open finding list exactly `[RP-OBL-L02]` |
| Manifest | trial `subject-manifest.json` = `bcc63f22…a1a1`, 51 files; the five selected files are re-hashed against it |
| Schema6 | report schema `/properties/envelope` = `{$ref: command-envelope:6}`. envelope6 minus `/allOf/19/then` (restored to its before value), with `$id`, title, description and schemaMajor 5 restored, equals envelope5. |
| Prose (3 overrides on `workflows-and-surfaces.md`, source sha `1ee203e3…`) | **224-228** cancellation: an optional Run is retained, after-sha `678eddc7…`. **1302-1338** availability section: entry points, attempt prerequisite, custody, presence law, empty account before planning; after-sha `1dbdff59…`. **1340-1349** failure envelopes: the two `errors=[]` exceptions and the recorded-error rule; after-sha `7bb16efc…`. |
| Prose checks | For each override, the before-text equals the current lines and before and after sha256 are bound. `overridden_text` applies them together with the 9 single-line report overrides, which must be disjoint. The selected duty phrases must be present. |
| Model | `workflows_model.v1.py` (`be37023f…`) line 380: `for r in required if` becomes `for r in results if`. Both forms are executed. |
| Joins | recorded-error, payload/Run-carrier, result-kind and skipped-step joins, through the pinned `ledger_join.py` |
| Mandatory composite entry points | `validate_interruption_delivery` on every post-planning interruption golden; `validate_preplanning_delivery` on every preplanning golden. The narrower helpers are never used alone. |

### 2.2 Report host admission (`J-ENV-*`, shared by human/json/agent/html)

Applied to any before-settle interrupted `failure` or `run` carrier joined to its recorded steps:

- **Recorded-error rule (kept).** The exact in-step-order `domainDetail`s of recorded request-rejected/operational-failed steps (optional included; skipped and cancelled excluded) are carried. When the list is empty, a failure carrier has `errors: []` (now admitted by envelope6) and a run carrier omits `errors`. Code `J-ENV-INTERRUPTION-DETAIL`.
- **Run carrier (new, model line 380).** If any completed analysis/verify step committed a Run (any requirement), the carrier must be `kind=run` naming and carrying exactly the last such Run. Otherwise it must be `kind=failure` with no `runId`. Code `J-ENV-INTERRUPTION-RUN-CARRIER`.
- **Availability (new).** A command whose inventory parity includes `capability-availability` must carry `availability` on every interrupted carrier, even before a Run exists (the explicit empty account when nothing was selected). Code `J-ENV-CAPABILITY-AVAILABILITY`. The exact account, the per-step selections and the started-attempt prerequisite can be judged only by the composite entry point against the host selection context. Report host admission cannot see them (negative controls below).
- **Fit (open joint-review question Q-FIT-1).** An interrupted fit run carrier carries no `advisoryReport` the host did not seal (the prose forbids invented results). If one is carried, it is admitted in full. No owner text requires or forbids the sealed page on an interrupted fit run carrier.
- The settled D9 aggregate and every settled golden are unchanged. `report_model.invocation_aggregate` applies line 380 only on before-settle interruption.
- **Output kinds.** `owner/builtin-step-planning.v1.json#/outputKinds` binds one actual carrier per builtin/variant and situation: settled with Run `run`; settled without Run `failure`; query success `query`; interrupted with committed Run `run`; interrupted without Run `failure`; preplanning `failure`; invocation carrier `not-selected`. The binding also records the availability duty.
- A report document is still never delivered for a before-settle interruption: `J-LEDGER-CANCELLATION`, unchanged.

### 2.3 Delivered goldens (status `delivered-in-candidate-pending-joint-review`)

Each golden is produced and re-derived by `check.py` as follows:

1. The pinned owner model runs a scripted schema-valid invocation.
2. The InvocationRecord schema is checked.
3. The historical and successor models are both executed.
4. `report_model.interruption_envelope` builds the carrier.
5. The carrier is admitted by the envelope6 shape, then by the actual composite entry point with the native `invocation_availability`, then by report host admission.

| Set | Count | Content |
|---|---|---|
| Builtin interruption scenarios | **36** (12 plannable variants × 3) = **144 renderer rows** | signal before the first step (SIGINT); signal before the required render after every earlier step completed (SIGTERM); first step rejected, then a signal before render (SIGHUP) |
| Carriers observed | 36 | failure `errors=[]` with empty account: 8. run, no errors, with selection: 8. failure with recorded errors and selection: 6. run with recorded errors and selection: 2 (pivot rejected, primary committed). failure `errors=[]` without availability (query commands): 8. failure with recorded errors without availability: 4. |
| Preplanning carriers | **9** (8 resolved commands × 4 renderers = 32 rows, plus an unresolved command) | failure `errors=[]` with exit 130; resolved analysis commands carry the explicit empty account; query commands and the unresolved command omit it |
| Profile optional commit (C02) | **3** (one per signal) | optional analysis committed, then a signal before the required render. The successor names the optional Run (run carrier accepted). The historical model's termination omits it. |
| Converted former pending goldens | **8** (`pending-C01-{analyze,candidates}-signal-before-commit/{human,json,agent,html}`) | now delivered by `analyze/primary/signal-before-first-step` and `candidates/primary/signal-before-first-step`. The author-07 analyze rows used an unplannable import step (RP-OBL-P01); the plannable primary expansion is used instead. |

**Owner model.**
- All 36 builtin scenarios are identical under the historical and successor models: no builtin html variant plans an optional analysis step.
- The 3 profile cases differ only in the Run choice.
- In every case, `report_model.invocation_aggregate` over the projected steps equals the successor termination.

**Negative controls on the builtin scenarios** (composite entry point / report host admission):

| Control | Count | Composite | Host |
|---|---|---|---|
| availability omitted | 24 | `J-AVAILABILITY-PROJECTION` | `J-ENV-CAPABILITY-AVAILABILITY` |
| empty account invented (no duty, no selection) | 12 | `J-AVAILABILITY-PROJECTION` | accept (not visible without context) |
| committed Run erased into a failure | 10 | `J-INTERRUPTION-AGGREGATE` | `J-ENV-INTERRUPTION-RUN-CARRIER` |
| detail invented | 36 | `J-INTERRUPTION-INVENTED-DETAIL` | `J-ENV-INTERRUPTION-DETAIL` |
| recorded detail omitted | 12 | `J-INTERRUPTION-INVENTED-DETAIL` | `J-ENV-INTERRUPTION-DETAIL` |
| selection on an unstarted (cancelled) step | 8 | `J-AVAILABILITY-SELECTION` | accept (not visible without context) |
| retained selection dropped (empty account) | 16 | `J-AVAILABILITY-PROJECTION` | accept (not visible without context) |
| envelope major 5 | 36 | schema | `SCHEMA-ENV` |

The three "not visible without context" rows show why the composite entry point is mandatory.

**Other negative controls:**
- **Preplanning** (per carrier): an invented selection is refused with `J-AVAILABILITY-PROJECTION`; an invented detail or a changed signal with `J-INTERRUPTION-PREPLANNING-CARRIER`; an availability-duty mismatch with `J-AVAILABILITY-PROJECTION`. Report host admission refuses omitted availability for analysis commands.
- **Profile:** the historical-choice carrier and the historical record itself are each refused with `J-INTERRUPTION-AGGREGATE`; omitted availability with `J-AVAILABILITY-PROJECTION`.
- **Converted goldens:** errors-empty accept/accept; errors omitted `SCHEMA-ENV`/schema; unrelated detail invented `J-ENV-INTERRUPTION-DETAIL`/`J-INTERRUPTION-INVENTED-DETAIL`; major 5 `SCHEMA-ENV`/schema; analyze availability omitted `J-ENV-CAPABILITY-AVAILABILITY`/`J-AVAILABILITY-PROJECTION`.

**Host custody and nothing invented.**
- Selection contexts are synthetic trusted host inputs: one retained selection per started, unskipped analysis/verify step, with one absence on the first. Their completeness is a host custody duty, not proved here.
- Nothing is fabricated: no findings, advisoryReport or query/doctor completion. Earlier optional commits are never erased.

### 2.4 Integration duties that remain explicit

- Rebase metadata/CLI carriers, generated sources, the generator registry and product closure to envelope6 with its envelope5 parent (RP-OBL-G01/E01).
- Host RequestContext custody and complete immutable retained selections.
- Composite entry points at every actual delivery boundary.
- Renderer parity for interrupted carriers in every applicable renderer (SARIF included).
- Q-FIT-1.
- RP-OBL-L02.

## 3. RP-OBL-L02: required output capacity (open)

**Regression** (`check.py` `capacity_regression`, actual native functions):

1. `admit_requested_capabilities` admits 995 `calls@js-synthesized` rows with distinct 4096-character workspace roots.
2. The analysis-spec validates and is **4,167,140 B** canonical.
3. `invocation_availability` over that selection validates as `CapabilityAvailabilityV1`.

| Case | Account | Envelope | envelope6 shape | Composite join | Report host | Exact codec (4,194,304) |
|---|---|---|---|---|---|---|
| analyze, 1 selection (first step rejected, signal before render; failure carrier) | **4,231,826 B** (`28d8de2e…`, equal to the audit) | 4,232,205 B | valid | accept | accept | account and envelope refused `BYTE_LIMIT` |
| audit with pivot, 2 selections (signal before render; run carrier) | **8,463,605 B** (`b7830c73…`) | 8,464,317 B | valid | accept | accept | refused `BYTE_LIMIT` |

A truncated notice, an empty account or omitted availability is refused by the composite join with `J-AVAILABILITY-PROJECTION`. **No silent truncation, false empty account or invented precedence exists in this candidate.**

**What the owners say (exact lines, checked against the effective text):**
- `workflows-and-surfaces.md:226` (override 224-228): before-settle cancellation gives aggregate `interrupted`, exit **130**, naming an earlier committed Run.
- `workflows-and-surfaces.md:238`: the settled D9 order ranks operational-failed > request-rejected > policy-failed > indeterminate > success. Interruption is decided by the cancellation law and is not ranked.
- `workflows-and-surfaces.md:1135`: the projection must be total over parity fields; a missing field is a required-delivery operational fault (**4**, `DELIVERY.REQUIRED_FAILED`).
- `workflows-and-surfaces.md:1147`: a required renderer failure after commit is `DELIVERY.REQUIRED_FAILED` (**4**).
- `workflow-projection-contract.v3.md:123`: output overflow is `OUTPUT.SERIALIZATION_FAILED`, faultCause `output-serialization` (operational-failed, **4**).

**Disposition.**
- No owner text orders interrupted/130 against required-delivery/4 or serialization/4 for the interruption carrier's own output, and no bounded owner correction follows directly from existing text. The choice between preflight rejection before retained selection and a complete bounded output profile belongs to the capacity owner.
- RP-OBL-L02 is registered `open-owner-decision`, `blocksM1FinalIntegration` and `blocksRequiredOutputCapacityClaim`, with the issue's closure criteria. It is also a coverage review issue on `commands:{default,analyze,fit,audit}` and `renderers:{human,json,agent,html}`.
- No global codec redesign.
- **Not proved:** complete native unit/filesystem selection, parameter admission, preflight and final serializers.

## 4. Review-06 fixes (author-07 scope, preserved for the combined review)

### RPR6-1: hook misattributes dir_fd-relative opens; cwd scope unstated — corrected (unchanged)

- **Refusal.** Every non-absolute open, listdir or scandir event is refused with `UNATTRIBUTABLE-PATH-EVENT` before content, in trace mode as well; nothing is cwd-normalized.
- **Paths and scratch.** Declared paths are resolved once, before the hook. Scratch is removed by `remove_owned_tree` (absolute scandir, lstat-based kind, unlink/rmdir); `shutil` is not imported.
- **In-process probes** (`unattributablePathProbe`):
  - review-06 PoC (a): an fd on the non-governed architecture parent with cwd `/`, then a dir_fd-relative open of the unpinned README;
  - PoC (b): cwd = architecture, `os.open("etc", dir_fd=fd("/"))`;
  - an fd listing, a relative `open` and a relative `scandir`.

  All are refused, and cwd is restored.
- **Strict runs.** The strict check runs from the exact frozen copy with three cwds (the copy, the architecture checkout and `/`). The outcomes are compared in `scratch/closure-evidence.json`, outside the subject.

### RPR6-2: fabricated skipped detail laundered into interruption errors — corrected (now joined to envelope6)

- **Detail list.** `recorded_failure_details` excludes skipped and cancelled steps and keeps optional-step failures. `J-LEDGER-SKIPPED` and `J-ENV-INTERRUPTION-DETAIL` require every skipped step's termination to be exactly `{class: request-rejected, errorCode: REQUEST.PRECONDITION_FAILED}`, as in the owner skip record.
- **Error rule.** The deterministic rule of §2.2 applies. The pending "failure with empty list" row is now delivered by envelope6.
- **Cases kept, with outcomes:** real error only accept; review-06 probe E refused; fabricated skip not carried refused; cancelled-step detail not carried accept; cancelled-step detail carried refused; run carrier with no details and errors absent accept; run carrier with `errors []` `SCHEMA-ENV`; run carrier with the real pivot detail accept; that detail omitted refused; invented detail refused; ledger fabricated skip `J-LEDGER-SKIPPED`.
- **Delivered golden.** Audit with pivot rejected, primary committed, comparison skipped and SIGINT during render: a run carrier with `errors = [pivot detail]`.

### RPR6-3: planning omits conditional expansions and mis-binds a param — resolved (unchanged)

- **analyze `--baseline PATH`.** Grammar `opensip analyze [--ephemeral | --baseline PATH]` and the `--baseline` flag (workflow, selection, one UserInputPath). Passage overrides at workflows lines 1097 and 1103. Variants `baseline-no-pivot` (delegated primary → comparison code-regression → render) and `baseline-with-pivot` (pivot → delegated primary → comparison → render).
- **Ephemeral with baseline.** Refused before planning: `REQUEST.UNSATISFIABLE` / `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY`, exit 2. Golden `analyze-ephemeral-required-authority` situation text is corrected (analyze never adopts).
- **Optional delivery.** `primary-with-optional-export` (optional terminal export on [0]). The sink selection source is RP-OBL-X01 (M5). The optional-render delivery goldens (8 of 68) are labelled `generic-profile-d9-composition`.
- **repair-preview.** `evidenceSource` is `{runId}` only; the `{step}` form and subject-06's string form are both refused.
- **Representative StepSpecs.** Validated against `StepSpec`, the params binding and the whole InvocationRecord. The owner `validate_dag` gives the same mutant codes as the report DAG law. The owner `run_invocation` aggregate equals `report_model` for all-completed, first step rejected, SIGINT before render, and the optional export fault.
- **P01 scope.** Not an M1 exit blocker; required before M5.

### Advisories and K01 (unchanged)

- **A2.** The query fixture's `visitedNodes` 4 becomes 1; executed owner neighbors pages report 1.
- **A3.** Full StepSpec and record validation.
- **A5.** All 11 feature blockers kept.
- **K01.** The coverage overlay is built on the accepted v3 (`implementation-coverage.v3.json`, unit manifest `48035089…`). The owned validator returns valid on v3 and on the overlay with no workaround. The historical v2 negative control ("Missing/extra module milestone prerequisite") and the `assets.rs = M6` control are kept.

## 5. Carrier law changes this round

- **Envelope.** The report envelope `$ref` becomes command-envelope:6. Host admission adds `J-ENV-INTERRUPTION-RUN-CARRIER` and interrupted-carrier availability (`J-ENV-CAPABILITY-AVAILABILITY`), and relaxes the fit carrier as Q-FIT-1 (§2.2).
- **Model.** `report_model` adds `interruption_envelope` and `preplanning_envelope`. `failure_envelope` carries the template's availability on interrupted failures. Cancellation Run selection follows model line 380.
- **Inventory5.** The json renderer is version 6.
- **Overrides.** The report's 9 single-line overrides now name command-envelope:6 over its envelope5 parent, applied together with the 3 interruption spans.
- **Coverage.** 323 rows re-derived from the effective (overridden) text: 52 row changes, 1 addition, 16 review-issue additions (L02 added). The owned validator returns valid on the v3 base and on the overlay.
- **Unchanged:** graph page law, byte law, history, provenance, static parity and derived bounds (`documentMaxBytes` 27,828,517; ledger 19,436,467; structural, RP-OBL-L01).

**Renamed case ids.** The meaning of these author-07 ids depended on envelope5. Each control is kept; the envelope5 outcome is still reproduced by the major-5 cases.

| author-07 id (outcome) | author-08 id (outcome) |
|---|---|
| `interruption-empty-errors-envelope5` (`SCHEMA-ENV`) | `interruption-empty-errors-no-recorded-detail` (accept), and `interruption-empty-errors-envelope-major-5` (`SCHEMA-ENV`) |
| `interrupted-failure-without-detail-envelope5` (`SCHEMA`) | `interrupted-failure-empty-errors-with-recorded-detail` (`J-ENV-INTERRUPTION-DETAIL`) |
| `interrupted-failure-with-real-recorded-detail-passes-join-then-ledger` (`J-LEDGER-AGGREGATE`) | `interrupted-failure-carrier-erases-committed-run` (`J-ENV-INTERRUPTION-RUN-CARRIER`): the failure carrier erased the committed Run, which is now refused first |

**New cases:**
- `envelope-major-5-refused` and `json-fit-major-5`;
- `interruption-empty-errors-with-recorded-detail`;
- `interruption-failure-availability-omitted`;
- `interruption-query-command-no-availability`;
- `interruption-failure-carrier-erases-committed-run`;
- `interruption-run-carrier-names-other-run`.

No other expectation changed.

## 6. Obligation register (`owner/design-obligations.v1.json`)

| Id | Standing |
|---|---|
| RP-DO-01, 03..12 | report design blockers (proposals; separate owners) |
| RP-DO-02 | conditional, not selected |
| RP-OBL-C01 | implemented in candidate, pending joint review (subject-07 unit + envelope5); M1 blocker |
| RP-OBL-C02 | implemented in candidate, pending joint review (model line 380); M1 blocker |
| RP-OBL-P01 | pending owner decision; not M1, M5 blocker |
| RP-OBL-X01 | pending owner decision; not M1, M5 blocker |
| RP-OBL-L01 | pending owner statement, non-blocking |
| **RP-OBL-L02** | **open owner decision; M1 blocker; blocks any required-output capacity claim** |
| RP-OBL-K01 | closed by accepted unit, bound |

Order: C01, C02, P01, X01, L01, L02, K01. M1 blockers are C01, C02 and L02; M5 blockers are P01 and X01.

## 7. Evidence and limits

**`check.py` verifies:**
- closure, alias, unattributable-path and bytecode probes;
- regeneration of 11 owner outputs and fixtures;
- restorations: envelope5 → envelope4, **envelope6 → envelope5**, inventory schema5 and inventory5;
- **43 metadata cases through envelope5 and through envelope6** with identical outcomes, and the in-process accepted metadata checker (43 cases, 28 schemas);
- coverage on the accepted v3 (323 rows), overrides (9 single-line + 3 interruption spans) and the register;
- builtin planning (schema, `validate_dag`, `run_invocation`), owner query paging and the fixture correction;
- **interruption integration** (§2) and the **L02 regression** (§3);
- 22 aggregate cases, 68 delivery goldens (17 scenarios) and 19 static-parity goldens;
- **47 envelope cases:** 14 accept, 11 schema, 22 host;
- **194 report cases on 19 bases, each with its exact code:** 30 accept, 29 schema, 15 codec/boundary, 18 envelope host, 48 ledger, 29 graph, 25 other;
- graph controls, byte law, worst case and codec reachability.

**Limits:**
- Scripted owner results and selection contexts are synthetic trusted inputs. There is no retained Run replay, RequestContext custody, signal handling, renderer or serializer execution.
- Envelope6, the prose and model line 380 are bound for joint review and root source selection, not selected. The envelope5 parent stays unaccepted.
- The planning, grammar and fixture records are proposals.
- The mock graph owner and fixtures are constructions.
- No product installation, runtime, browser, generator, performance, M1 or project qualification.
