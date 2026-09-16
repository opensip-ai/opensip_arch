# Report projection and fit successor contract (author-04)

## 0. Standing

This is an **author-04 correction candidate** answering the fresh independent review `m1-report-projection-review-03` (RPR3-1..6, A1–A9) and the root decisions of this round. It is not approval.

**Readiness is split (RPR3-6):**
- **Carrier unit:** candidate for review. This covers the shape and admission of what this carrier actually delivers: the envelope5 fit carrier; the report-projection:1 ledger, panels, codec, derived bounds and byte law; and delivery goldens.
- **Report design:** **blocked** by eleven design blockers in `owner/design-obligations.v1.json` (RP-DO-01, 03–12). RP-DO-02 is a conditional requirement that is not selected.
- **AUDIT-G10:** stays **open**.

**Unchanged:**
- Earlier author/subject/review bytes, source45, application46 and the accepted metadata-v2 unit are historical and untouched.
- Historical coverage bytes are unchanged.
- The mutable `docs/implementation/README.md` is not opened or pinned. The metadata-v2 unit's own `README.md` is pinned because its accepted checker reads it.

**Not claimed:** no browser, HTML, human renderer, generator, product code or performance measurement was built or run. Sizes are structural or constructed, never measured performance.

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists 17 files and excludes only itself:

| Kind | Files |
|---|---|
| Executable | `check.py`, `report_model.py`, `build_owner.py`, `build_fixtures.py`, `seal.py` |
| Owner data | `report-projection.schema.json`, `owner/command-envelope.v5.schema.json`, `owner/command-inventory.v5.schema.json`, `owner/command-inventory.v5.json`, `owner/implementation-coverage-successor.v1.json`, `owner/passage-overrides.v1.json`, `owner/design-obligations.v1.json`, `owner/budget-derivations.v1.json` |
| Other | `fixtures.json`, `source-pins.json`, `successor.json`, `contract.md` |

`check.py` never runs `seal.py`, and no file hashes itself. The freeze anchor is the SHA-256 of `subject-files.json`.

**Run it from a copy of exactly the listed files:**

`TMPDIR=<own scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture ARCH --subject-strict [--out RESULT]`

**Enforced closure (RPR3-4, A6, A8, A3).** `source-pins.json` pins every external file and directory listing that a traced run reads or executes. The roots are the architecture checkout and `/tmp/opensip-implementation`, excluding the subject and the reference environment.

| Mechanism | Rule |
|---|---|
| Pins | Verified before any external import. |
| Audit hook | Every governed read-open re-hashes the file against its pin (`CLOSURE-PIN-DRIFT-AT-OPEN`). Every listing recomputes its digest (`CLOSURE-LISTING-DRIFT-AT-LISTING`). Unpinned opens and listings are refused. |
| Fresh-source loader | `SourceFileLoader.get_code` compiles exactly the bytes it read, after checking them against the pin (`SOURCE-PIN-DRIFT`). Bytecode is never consulted. A bytecode-only governed module is refused. `pycache_prefix` also points to a nonexistent directory. |
| No child process | The audit hook refuses `subprocess`/`exec`/`spawn`/`fork` (`CHILD-PROCESS-REFUSED`). The accepted `check_metadata.py` runs **in-process** under the same hook and loader: argv and stdout are swapped and restored, and its printed result must be `passed: true`. Its whole closure is pinned: metadata-v2 files, the listing, successor parents, the build plan, historical coverage and inventories, and `canonical.py` source. |
| `--out` | The declared result path may be written (and not read), inside or outside a governed root. Any other governed write is refused (`UNDECLARED-WRITE`). The only scratch area is a fresh `mkdtemp` child of `TMPDIR`, removed after use. |
| Bytecode demonstration | In that scratch child, a header-valid stale pyc sits next to a source. The stock loader executes `stale-bytecode`; the enforced loader executes `verified-source`. |

**Trusted-host limits.** The filesystem, interpreter, reference environment and the start-time `source-pins.json`/`subject-files.json` bytes are trusted. Re-hashing at open narrows but does not exclude a concurrent writer between verification and the consuming read. Writes outside the governed roots (other than the out path) are not policed.

## 2. Outcome-by-outcome closure (review03)

| Finding | Correction | Evidence (exact outcome) |
|---|---|---|
| **RPR3-1 graph count law** | Owner page law `report_model.page_law` (§6). Its six rules, all enforced:<br>• complete ⇒ `countBasis` exact, no cursor, and `totalItems` = embedded rows;<br>• lower-bound ⇒ a public produced or visited cap (graph-query:3 `Bounds`) was reached;<br>• truncated-bound ⇒ lower-bound;<br>• truncated-page ⇒ cursor, full page and more counted rows;<br>• truncated-bound without cursor ⇒ every produced row embedded;<br>• rows ≤ page, total and produced.<br>Continuation is derived, not chosen: `complete-page-set` only for exact complete, `not-embedded` with a cursor, `operation-truncated-no-continuation` otherwise. | G1 complete/lower-bound slice → `J-GRAPH-COUNT`; G1 truncated-page variant → `J-GRAPH-COUNT`; G2 truncated-bound relabel → `J-GRAPH-COUNT`; G3 exact slice → `J-GRAPH-COUNT`; positive lower-bound page at the public 100000 item cap → accept; relabelled complete → `J-GRAPH-COUNT`; continuation mislabels → `J-GRAPH-CONTINUATION`; test-bound controls lawful under their bounds and refused under public bounds (`graphPageLawControls`) |
| **RPR3-2 mandatory root bounds** | The placeholder allowance is gone. `owner/budget-derivations.v1.json` derives structural maxima from the 28 pinned owner schemas: StepTermination 6,476,835 B, including the full 4096-pin PinnedPurgeDisclosure (6,463,688 B). No owner bounds the invocation record by the envelope codec, so terminations are never truncated or codec-capped. Per command, the ledger bound is structural over the finite inventory step count (render never recorded): audit 3 recorded steps → 19,435,937 B. `documentMaxBytes` = 246 root-key overhead + 4,194,304 envelope + 19,435,937 ledger + 4,194,304 exploration + 3,173 root members = **27,827,964 B** (development cap, proven finite, not measured). The effective exploration budget is `min(4 MiB, documentMax − overhead − C(envelope) − C(ledger) − rootMemberMax)` and is used by projector and admission alike. Delivery when a valid owner result exceeds a cap: §9. | B1 (audit failure, envelope at 4 MiB, three pinned steps) → accept; B1 control → accept; maximal legal step terminations (steps 2–3 at 4096 pins with 6-byte characters) → accept; oversize → `CODEC-BYTES`; altered cap → `SCHEMA` |
| **RPR3-3 D9 and cancellation** | **Explicit root correction:** the earlier rule "renderer failure cannot replace query failure" is withdrawn. The owned D9 aggregate applies unchanged to a subsequent required render step:<br>• operational-failed dominates request-rejected;<br>• ties keep the first termination with detail;<br>• optional failures never change the aggregate.<br>Recorded step terminations are never rewritten. The ledger carries the exact invocation:3 `Cancellation`. The model law gives before-settle → interrupted 130, naming the committed Run, and after-settle → not reclassified. Interrupted-without-before-settle, signal mismatch and phase mismatch are typed refusals, never `ValueError`. A delivered report is projected inside the required render step, so a signal then is before-settle, cancels that render and yields no document (`J-LEDGER-CANCELLATION`). The interrupted outcome is delivered as a `kind=run` envelope with `runId`, which envelope5 admits. | D1 aggregate → operational-failed `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`; 28 delivery goldens (7 scenarios × human/json/agent/html, §5); D1 inside a delivered report → `J-LEDGER-AGGREGATE`; D2 → `J-LEDGER-CANCELLATION`; 14 aggregate cases |
| **RPR3-4 closure** | §1: in-process historical checker, fresh-source loader, re-hash at open, listing recompute, child refusal, declared `--out`. | 79 pinned files + 2 listings; run-result `closure` counts; `bytecodeDemo` |
| **RPR3-5 coverage** | The fit row now carries all nine `parityFields`, and reportFeatures rows carry review issues. The full owned `validate_coverage` runs on base and overlay:<br>• unscoped, both stop at the pre-existing "Missing/extra module milestone prerequisite";<br>• with the one recorded scoped workaround (in memory, applied identically to both: `moduleFirstMilestone["crates/reporting/src/assets.rs"]="M1"`), both return `valid`.<br>The checker proves the gap is exactly that key. Historical bytes are unchanged. | scoped base/overlay `valid`; C2 control (fit parityFields reverted) → "Command metadata drift"; 28 row changes, 1 addition, 12 review issues |
| **RPR3-6 obligations** | `owner/design-obligations.v1.json` (§10) gives each F01–F10 feature, step duration and explicit older Run selection:<br>• owning design unit, status, gap kind, milestone and gate;<br>• closure criterion and carrier successor;<br>• whether it blocks report-design readiness.<br>F03 and F05 are existing-owner design gaps. Duration is `owner-carrier-field-absent`; the checker finds no duration/elapsed member in invocation:3 or common:3. Blocked report-feature rows require delivered behavior: "an unavailable feature-state disclosure does not satisfy this row". | register checks; `ownerEvidence` all true |
| **A1 slot steering** | New join `J-SLOT-RESOLUTION-CONTRADICTED`: a subject stated `descriptor-not-retained` must not appear in any embedded owner row. An uncontradicted steering remains a host assertion but is counted in the static section (`disclosures.graphUnresolvedSubjects`). | S1 → `J-SLOT-RESOLUTION-CONTRADICTED`; uncontradicted variant → accept (disclosed); hidden count → `J-DISCLOSURES` |
| **A2 history count** | `priorRunsInSnapshot` is host-asserted in provenance (`prior-runs-in-snapshot-count`); the verified label is `prior-run-count-arithmetic-given-host-snapshot-count`. The count is exposed in the static section. | H1 → accept (host-asserted, disclosed); hidden → `J-DISCLOSURES`; claiming it verified → `SCHEMA` |
| **A3 `--out`** | Declared write path (§1). | pinned run writes `--out` under a governed root |
| **A4 graph provenance** | Verified label `owner-page-law-count-basis-coverage-produced-items-continuation` now matches enforced joins; delta measurement is host-asserted. | provenance const |
| **A5 baseline exclusion** | §7 states it; `J-HISTORY-BASELINE` refuses a baseline source listed as prior. | `history-baseline-source-listed-as-prior` → `J-HISTORY-BASELINE` |
| **A6 listing drift** | Recomputed at each listing event. | hook |
| **A7 R14** | Recent selection stays. Explicit older Run selection is RP-DO-12: `run.show`/`run.list` exist in graph-query:3 but items are untyped, and html commands have no Run-id selector. | register; `R14-run-show-operation-exists` |
| **A8 stale pyc** | Fresh-source loader; demonstration. | `bytecodeDemo` |
| **A9 generator** | Not run by this author; remains RP-OBL-G01. | — |

## 3. Fit successor (unchanged from author-03 except coverage)

- **Envelope5** adds only `advisoryReport`. `sealed-run-first-page` carries the exact first `candidate.list` request (page 100, `includeSuppressed` false, no cursor), a CandidateListRecordV1 and FitSealedParityV1. `unavailable-ephemeral-analysis` carries all-null parity.
- **Inventory5** `advisoryDispatch.parityPaths` holds nine fields: run-id, candidates, evidence-levels, termination-class, capability-availability and candidates-truncated/-total-items/-next-cursor/-availability. The coverage fit row now carries all nine.
- **Host admission:** `J-ENV-FIT-RUN`, `-PAGE`, `-CURSOR`, `-PARITY`, `-CARRIER`, `J-ENV-QUERY_SURFACE_*`, `J-ENV-CAPABILITY-AVAILABILITY`, `J-ENV-TERMINATION-RUN`, `J-ENV-EXIT`.
- **Audit:** `comparisonResultId` is required except on an interrupted termination, where the comparison step was cancelled.
- **Failure law:**
  - Query-step refusals or failures after commit are `kind=failure` carrying that step's termination.
  - A later required renderer failure dominates by D9 (§2 RPR3-3) with `RENDERER_FAILED_AFTER_COMMIT`, or with `REQUIRED_PROJECTION_FAILED` when no Run was committed.
  - An interrupted invocation with no committed Run has no admissible envelope5 `kind=failure` form. `errors` must be non-empty and no DomainDetailCode names an interruption. This is recorded as envelope-owner gap RP-OBL-C01, not invented here.
- **Compatibility:** envelope5, inventory schema5 and inventory5 restore exactly. All 43 metadata cases behave identically. The accepted checker passes in-process. The `--ephemeral` join is byte-identical.

## 4. Report document

**Root members:** `schemaFamily`, `schemaMajor 1`, `command`, `renderer {html,1}`, `envelope`, `invocationLedger`, `staticParity`, `disclosures`, `supportedReportViews`, `featureStates`, `budgetProfile`, `documentProvenance`, `reportObservedAt`, `pathDisclosure`, `panels`.

**Views and panels per command** are as in author-03: 8 html commands and 12 view ids; audit comparison is never `not-selected`.

**Feature states** are exact per command. Each carries `reason` and `obligationId`, and is disclosure only:

| Feature | Row | Reason | Obligation |
|---|---|---|---|
| capability-descriptions | R05 | no-admitted-owner | RP-DO-01 |
| catalog-run-statistics | R05 | no-admitted-owner | RP-DO-02 (conditional, not selected) |
| coupling-importer-package-membership | R08 | no-query-carrier | RP-DO-03 |
| declared-configuration | R23 | no-redaction-owner | RP-DO-04 |
| entry-point-recognition | R12 | owner-data-not-retained | RP-DO-05 |
| recipe-descriptions / recipe-parameters | R06 | no-admitted-owner | RP-DO-06 / 07 |
| rule-descriptions | R05 | no-admitted-owner | RP-DO-08 |
| symbol-metrics / test-reachability | R07 | no-admitted-owner | RP-DO-09 / 10 |
| step-duration | R03 | owner-carrier-field-absent | RP-DO-11 |
| explicit-older-run-selection | R14 | no-selection-interface | RP-DO-12 |

**Disclosures** (`J-DISCLOSURES`, recomputed from panels):
- `graphPlannedSubjects`;
- `graphUnresolvedSubjects` (descriptor-not-retained, host-asserted);
- `historyPriorRunsInSnapshotHostAsserted`.

They are shown as counts, never as verified completeness.

## 5. Invocation ledger, D9 and cancellation (R03)

**Shape:** `{requestId, workflow, mode, cancellation (invocation:3 Cancellation), steps ≤ 64, missingChildren, provenance}`.

**Joins:** `J-LEDGER-REQUEST`, `-COMMAND`, `-STEPS`, `-RENDER` (render unrecorded), `-MISSING`, `-ATTEMPTS`, `-RUN`, `-MODE`, plus:
- `J-LEDGER-CANCELLATION`:
  - cancelled outcome ⇔ interrupted termination;
  - the delivered document requires `requested false, phase none`;
  - model-law refusals.
- `J-LEDGER-AGGREGATE`: `invocation_aggregate(steps, cancellation)` must equal the envelope termination exactly.
- `J-LEDGER-BOUND`: canonical ledger ≤ derived per-command bound.

**Aggregate law** (`report_model.invocation_aggregate`):
- requested ⇔ phase ≠ none.
- **before-settle:**
  - some required step, render included, is unrecorded or cancelled;
  - cancelled terminations equal `{interrupted, signal}`;
  - the aggregate is `{interrupted, signal, runId of the last committed analysis}`.
- **after-settle:** requires every required step recorded; the D9 aggregate stands.
- Any cancelled step without before-settle is refused.
- **D9:** operational-failed > request-rejected > policy-failed > indeterminate > success over required recorded steps; ties keep the first termination with domain detail.

**Delivery goldens** (`fixtures.json#/deliveryGoldens`). The prior step terminations are unchanged in every row, and the aggregate, exit and delivery result are identical across human/json/agent/html:

| Scenario | Aggregate | Exit | Render attempts | Delivered |
|---|---|---|---|---|
| fit query refused, render written | request-rejected QUERY.VIEW_UNKNOWN | 2 | 1 | yes (envelope digest; html static parity digest) |
| fit query refused, required render failed | operational-failed DELIVERY.RENDERER_FAILED_AFTER_COMMIT (runId) | 4 | 1 | no |
| fit query refused, optional render failed | request-rejected | 2 | 1 | no |
| fit query refused, no render selected | request-rejected | 2 | 0 | no |
| fit query I/O failed, required render failed (tie) | operational-failed evidence.purged (first detail) | 4 | 1 | no |
| candidates, no Run, query refused, required render failed | operational-failed DELIVERY.REQUIRED_PROJECTION_FAILED (no runId) | 4 | 1 | no |
| fit, signal during required render (before-settle) | interrupted SIGINT runId=R, `kind=run` envelope | 130 | 1 (cancelled) | no |

Every golden envelope passes envelope5 host admission, and every aggregate validates as StepTermination.

## 6. Graph policy, owner page law and subject index

- **Slot plan** (`finding-subject-slot-plan.1`) and the governed endpoint pointers are unchanged from author-03: at most 6 slots over at most 64 policy subjects.
- **Joins:** `J-SLOT-SUBJECTS`/`-POLICY`; `J-GRAPH-RUN`/`-PROJECT`/`-OPERATION`; `J-GRAPH-COUNT` (the §2 page law against `budgetProfile.graphPublicBounds` = graph-query:3 Bounds); `J-GRAPH-CURSOR`; `J-GRAPH-CONTINUATION` (derived); `J-GRAPH-PAGE-CAUSE`; table relation/resolution/kinds/endpoint/coupling/order/reach/path laws; subject index recomputation; and `J-SLOT-RESOLUTION-CONTRADICTED`.
- **Reference controls:** `host.testBounds` may only lower caps. Test-bound pages (truncated-bound last page, lower-bound truncated page) are lawful under their bounds and refused under public bounds. Report documents embed product pages, never reference controls.

## 7. History policy

`baseline-source-then-prior-commit-sequence.1` reads one consistent committed ledger snapshot:
1. The comparison's baseline source Run comes first, when present.
2. Then prior authoritative analysis Runs, by strictly descending `commitSequence` below the current receipt, up to `maxHistoryRuns` (4). **The baseline source Run is excluded from the prior Runs** (`J-HISTORY-BASELINE`).
3. Unavailable rows stay unavailable.

`J-HISTORY-COUNT` is arithmetic given the host-asserted `priorRunsInSnapshot`; it is not document-provable. Only recent Runs are selected. Explicit older Runs are RP-DO-12.

## 8. Provenance

Every `verifiedInDocument` label names an enforced join. Everything else is `hostAsserted`:
- the ledger being this invocation's record;
- descriptor-not-retained states;
- owner response admission;
- re-issued page size and measured byte deltas;
- snapshot receipts and snapshot count;
- the baseline descriptor Run;
- the findings' Run;
- the plan-bound policy;
- the release registry.

The exact labels are consts in the schema; moving a label is `SCHEMA`.

## 9. Codec, derived bounds, byte law and delivery

**Codec:**
1. bytes ≤ `documentMaxBytes` 27,827,964;
2. iterative depth ≤ 38;
3. canonical lexical laws;
4. canonical bytes.

**Owner codecs.** Each embedded owner record passes the exact codec from its native offset (`CODEC-OWNER-DEPTH`). The envelope must be ≤ 4 MiB (`ENVELOPE-SERIALIZATION-BOUNDARY`). Panel owner records must be ≤ 4 MiB (`CODEC-OWNER-BYTES`). Ledger terminations are bounded only structurally.

**Derivation** (`owner/budget-derivations.v1.json`, regenerated byte-identically and asserted against the budget profile):

| Command | Steps (render) | Recorded max | Ledger max bytes |
|---|---|---|---|
| default, candidates, inspect, review-brief, repair-preview | 2 (1) | 1 | 6,480,779 |
| analyze, fit | 3 (1) | 2 | 12,958,358 |
| audit | 4 (1) | 3 | 19,435,937 |

**Byte law.** Priority is comparison → catalog → evidence → graph → history.
- **Atomic panels:** included whole or omitted.
- **Evidence and history findings:** largest fitting prefix.
- **Graph slots:** each slot is re-issued down the ladder [100, 50, 25, 12, 6, 3, 1]. A page that is not full is never shrunk. The first unfittable slot stops the plan.
- **Budget causes:** each byte-budget cause carries a host-measured `rejectedByteDelta`, checked against the **effective** budget (`J-BUDGET-CAUSE`, `J-BUDGET-BYTES`, `J-BUDGET-ORDER`).
- **Per-panel caps:** 3956 evidence entries, 6 slots with 100 rows each, 1034 index rows, 4 history Runs, 5526 findings per Run, 512 rules, 128 capability declarations.

The effective budget equals 4 MiB for every admissible envelope and ledger by construction; this is asserted for every base and exercised by the scenario. Mandatory envelope, ledger and parity metadata are never truncated.

**Delivery when a cap is exceeded:**
- **Envelope over 4 MiB:** the owned `OUTPUT.SERIALIZATION_FAILED` boundary, as for JSON.
- **Required document refused by host admission:** the required render step fails. The aggregate follows D9 (§5): `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` with the Run, or `DELIVERY.REQUIRED_PROJECTION_FAILED` without one. The invocation record and every recorded step termination are retained unchanged.
- **Browser-side refusal:** keeps the static section and shows a typed notice.

**Static parity section** (`labelled-canonical-lines.2`): declared parity pointer lines, then `disclosure.<name>: <json>` lines, then `envelope: <json>`.

## 10. Design-obligation register (report design blocked)

| Id | Feature | Owning design unit | Status / gap | Closure criterion → carrier successor |
|---|---|---|---|---|
| RP-DO-01 | capability-descriptions | native-evidence §1.3 ReleaseCapabilityDeclarationV1 | blocker: no description field | admitted description member → CapabilityCatalogV1 members |
| RP-DO-02 | catalog-run-statistics | query contract §1 (run.list) | conditional, not selected | no statistics shown, or an owned statistic with history scope |
| RP-DO-03 | coupling-importer-package-membership (F03 package coupling; not history) | native-evidence §1.4 UnitMembershipV1/WorkspaceUnitV2 + query contract §§3–4 | blocker: existing-owner design gap | reviewed coupling projection with membership join and counts → package-coupling slot rows |
| RP-DO-04 | declared-configuration | security-and-lifecycle redaction policy | blocker: no redaction selector | selected redaction projection → redacted carrier |
| RP-DO-05 | entry-point-recognition (F05) | native-evidence §8 FrameworkRecognitionV1.entryPoints + identity retention + query §4 | blocker: existing-owner design gap | retained entry points admitted as path starts → entry-point path slots |
| RP-DO-06/07 | recipe descriptions/parameters | workflows §6 RecipeRef/RepairPlanDescriptor | blocker | admitted recipe descriptor/catalogue → carried record |
| RP-DO-08 | rule-descriptions | workflows §5 policy Rule | blocker | admitted description with provenance → RuleCatalogV1 members |
| RP-DO-09 | symbol-metrics | foundation relation registry | blocker | registered metric relations → metric columns keyed by subjectIndex |
| RP-DO-10 | test-reachability | workflows §4 imported evidence + native reachability | blocker | owned fact with completeness/provenance → symbol-detail carrier |
| RP-DO-11 | step-duration (R03) | workflows §1; invocation:3 Attempt | blocker: owner carrier field absent | Attempt observed-duration successor (excluded from Run identity) → ledger attempt member |
| RP-DO-12 | explicit-older-run-selection (R14) | query contract §1 run.show/run.list; workflows §8 | blocker: no typed item or html selector | typed run.show item + explicit Run-id selector → `explicit-run-ids` history source |

**Common to every row:**
- milestone M4;
- gate: the build-plan M4 exit criteria (RP-DO-04 and RP-DO-11 also name DR-G20);
- each has a finite carrier successor that removes the matching feature state.

Blocked coverage rows list the id in `reviewIssues`, and their verification method demands delivered behavior.

## 11. Passage overrides and coverage

There are seven conditional overrides (chapter 14 lines 339, 459, 463, 556, 562, 564; workflows line 1106), updated for disclosures, cancellation and the duration blocker. Parents are never edited. The coverage overlay recomputes post-override section hashes (§2 RPR3-5).

## 12. Check evidence and remaining qualification

**`check.py` verifies:**
- closure and manifest;
- byte-identical regeneration (owners, derivations, register, fixtures);
- schema meta-checks;
- restorations, the 43 metadata cases and the in-process historical checker;
- coverage with the full owned validator;
- overrides and gating;
- the feature map and design register with owner evidence;
- subject3 agreement across three implementations;
- 14 aggregate cases, 28 delivery goldens and 14 static-parity goldens;
- embedding gains and the derived bounds;
- **22 envelope cases:** 7 accept, 8 schema, 7 host admission;
- **146 report cases on 14 bases, each with its exact code:** 25 accept, 26 schema, 15 codec/boundary, 15 envelope host admission, 16 ledger/D9/cancellation, 25 graph/slot/index, 24 other joins;
- graph page-law controls, the byte-law scenario and the worst-case table.

**Remaining (not executed):**
- the design blockers in §10;
- RP-OBL-B01 (browser lane) and B02 (accessibility);
- RP-OBL-H01 (host delivery);
- RP-OBL-M01 (measurement: the scale points of author-03 plus a 27.8 MB maximal document);
- RP-OBL-G01 (generator compatibility, A9);
- RP-OBL-E01 (integration record);
- RP-OBL-C01 (envelope owner: no admissible `kind=failure` detail for an interruption before any committed Run).

**Limits:**
- Fixtures are constructed. The mock owner follows the cited query laws, but it is not the product engine.
- Structural byte maxima are upper bounds (6 bytes per bounded character), not tight.
- This is not browser, renderer, generator, performance or product qualification.
