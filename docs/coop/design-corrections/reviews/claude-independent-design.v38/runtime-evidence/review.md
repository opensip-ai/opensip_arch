# Independent design review: frozen source38

**Verdict: ACCEPT** (source level only; not blind reconstruction, application, readiness or product qualification).

No MUST or SHOULD issue is unresolved. S37-01/02/03, A37-01..08, R1/R2, RC37-01 and RC37-A1..A3 are closed or accepted as designed on source38 by complete owner reads and independent discriminating probes; RC37-A4 stays optional editorial. Three advisories (ADV38-01..03) and SI-A1 are non-blocking and routed. Required actions ran to completion: subject/archive/member/parent/delta verification, six pinned groups, planning and inventory checks, package15 verification and probes. Source-level acceptance only.

## Subject

- Manifest: `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json`, SHA-256 `2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5`; measured live SHA `2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5`; verifiedManifest=True.
- Archive `571aad4d...`; 12904 files, 737100757 bytes; parent37 `245ef613...` verified=True; delta {"changed": 41, "added": 4, "removed": 0}.
- The source37 review (CHANGES_REQUIRED) and the bounded root-corrections review (PARTIAL, SHA equal to the root-recorded value: True) are preserved unchanged.

## Issues

No new MUST or SHOULD issue.

### ADV38-01 (ADVISORY): Delegated domainDetail and attribution on an analysis termination have no closed admissibility rule in the read owners

The termination owner admits a shape-valid but unrelated registered domainDetail on an analysis indeterminate projection (HOST.INVARIANT_VIOLATED, or a QUERY.* detail) and returns it as owner-validation-required, as its contract says. This review found no closed class-and-reason to detail admissibility table in the owners it read. The obligation is carried to host outcomes/finalization and to the §9 verification scenario.

- Selectors: `docs/coop/design-corrections/foundation/run-termination-contract.v1.md:23-38, 164-179`; `docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189`; `docs/v2/architecture/repository-file-inventory.v1.json crates/host/src/outcomes.rs, finalization.rs`; `implementation-coverage.v1.json workflows-and-surfaces:10 verification.method`
- Receipt: `receipts/probe-run-termination.json#PROJ`
- Disposition: ROUTE-TO-IMPLEMENTATION (host outcomes owner validates delegated detail and attribution); not a source defect because the owner never calls these lawful.

### ADV38-02 (ADVISORY): Read-only route for an association that names a carrier observed unmigrated (no published format row) is prose-only

The open dispatch classifies an unmigrated carrier as carrierFormat1 or carrierFormat2. The reader law sends any association naming a format 1 or 2 generation to unknown-carrier-incompatible, but the machine observation list and dispatch-result map cover only the migrated below-first_generation case. An association naming a carrier that is unmigrated now points to lost migration, rollback or a swap, which could equally be read as custody or quarantine. Both candidate routes are non-confirming operational failures at exit 4, so fail-closed behaviour is preserved.

- Selectors: `docs/coop/design-corrections/security/carrier-dispatch.v3.json:262 (readerLaws)`; `carrier-dispatch.v3.json:641-652 (unknown-carrier-incompatible observations name only grantGeneration below first_generation)`; `carrier-dispatch.v3.json:667-674 (readOnlyStandingOfDispatchResult has no carrierFormat1/carrierFormat2 entry)`; `docs/v2/contracts/product-v1/security-and-lifecycle.md:1307`
- Receipt: `receipts/probe-carrier-sql.json#DISPATCH.format2-with-association`
- Disposition: ROUTE-TO-CARRIER-OWNER: state the route and add the observation or map entry before F46 implementation.

### ADV38-03 (EDITORIAL): commit-recovery-readonly.v3 keeps two stale scope phrases

The plan now holds F00-F53, and S12 extends MIGRATION.CORRUPT to the writer/maintenance carrier footprint. The read-only document's conclusion, that MIGRATION.CORRUPT is not used on a read-only path, is correct; only the scope description is stale.

- Selectors: `docs/v2/architecture/commit-recovery-readonly.v3.md:39 ("F00-F37")`; `commit-recovery-readonly.v3.md:73-75 (MIGRATION.CORRUPT "is the store transition's detail")`; `security-and-lifecycle.md:1300, 1310 (governing scope includes the carrierFormat 3 migration footprint at writer/maintenance open)`
- Receipt: `fresh read`
- Disposition: EDITORIAL at the next successor; security S12 governs.

### Observations (not issues)

- Replay-stack exception coverage: a module-graph walk found exception class objects outside the declared UNAVAILABLE/MISMATCHES/REFUSALS tuples (for example the identity copy's native load NativeRefusal/ScopeRefusal and discovery-defaults errors). Static escape analysis attempt 2 found escapes only from registry-selected inputs (NATIVE_CONTEXT_LANGUAGE), cve1_encode over already-admitted values and a Unicode case-data environment error. No retained-byte path to a misrouted owner refusal was demonstrated. Such an exception would fail closed as host-invariant.
- observe_retained_availability admits a schema-valid record with non-canonical key order. The query contract names identity availability schema admission, not canonical bytes, so this is recorded as an observation only.
- SQLite affinity conversions (integral text, boolean, 1.0 REAL) and an embedded NUL in the free-text body are admitted by the carrier DDL; carrier-format §5.1 assigns closed-record admission to the host.
- The historical workflows common schema admits 33 lawful termination combinations versus 34 for evaluator3 common; the difference is the retained RunId pattern, not the R1/R2 branch law.

## Item dispositions

### S37-01: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v37 (SHOULD).

The analysis projection (class, runId, ordered reasonCodes, coverageId, absence of errorCode/faultCause/signal) is now a deterministic function of the sealed Run. Independent derivation matched the owner on every variant, including foo-budget+bar-unavailable, work budget with native stage carriers, provider-fault/cancelled/complete stage terminals and the complete-empty and policy-failed controls, and was invariant to discovery and object order. Delegated executionId/domainDetail/authority remain owner-validation-required (ADV38-01).

Owner selectors:
- `docs/coop/design-corrections/foundation/run-termination-contract.v1.md:61-84 (§3 condition population), :85-135 (§4 conditions, evaluator-only bridge and total order), :136-163 (§5 coverageId), :164-199 (§6 checking and goldens)`
- `docs/coop/design-corrections/foundation/run_termination_model.v1.py; run-termination-goldens.v1.json`
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189 (§9 selects the owner)`
- `docs/v2/contracts/product-v1/native-evidence.md:2946-2966 (native stage selection stops; the Run termination owner is named)`
- `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:138 (EVALUATION.WORK_BUDGET_EXHAUSTED positioned by run-termination-contract §4)`
- `docs/v2/architecture/implementation-normative-inputs.v6.json and implementation-coverage.v1.json workflows-and-surfaces:10 (incorporated owner pinned)`

### S37-02: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v37 (SHOULD); bounded review CLOSED-BY-OVERLAY-TEXT.

The planning layer no longer selects executable report hooks, so TCB-SCOPE-01 has no report-rendering exception.

Owner selectors:
- `docs/v2/architecture/prototype-report-inventory.md:37 (R02: versioned host-approved data projections only; executable report hooks not admitted under admission §5)`
- `docs/v2/architecture/prototype-report-inventory.md:179 (External tools row: no executable report-hook admission)`
- `docs/v2/contracts/product-v1/admission-and-qualification.md:344-345 (§5 items 4-5: no untrusted native/WASM admission; no imperative contributions or project hooks)`
- `docs/v2/architecture/implementation-coverage.v1.json R02 and R24 valueSha256 rebound`

### S37-03: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v37 (SHOULD); bounded review CLOSED-FOR-SCHEMA-AND-CONTROLS.

Advisory is admitted exactly where the schema law permits; no advisory violation was produced by the enumeration.

Owner selectors:
- `docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json:908-1022, 1180-1194 (advisory law)`
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:152 (advisory is schema-const false for graph.*)`

### A37-01: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v37 (advisory).

In each of the UTF-8, UTF-16le and UTF-16be carriers the probe offered 26 values. All 16 hostile grammar values (uppercase, zero-width, fullwidth, NUL-tail and leading-space hex and prefixes, BLOB, NaN and overflowing sequence, unknown record type) were refused. The 10 admitted values are 2 lawful controls (REV, SEAL), 7 documented SQLite affinity conversions (integral or leading-space integral text sequence, boolean grantGeneration, text record_schema, 1.0 REAL or text first_generation, 1.0 REAL chain_law) and 1 NUL-suffixed free-text body. carrier-format §5.1 leaves closed-record admission of that body to the host; this review treats that as the stated boundary, not a defect.

Owner selectors:
- `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:33, 49-50, 63-65, 89-114 (typeof + length + instr(col, char(0)) = 0 + prefix GLOB + NOT GLOB '*[^0-9a-f]*')`
- `docs/coop/design-corrections/security/carrier-format.v3.md:168-227 (§5.1 exact storage class and whole-value grammar)`
- `docs/v2/architecture/attempt-custody.schema.v1.json:153-155 (proposedPrivateDDL and ddlGrammarCorrection)`

### A37-02: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v37 (advisory).

The publication and first_generation laws are DDL-enforced in the footprint that 37 found unenforced. The superseded-generation law was isolated after attempt 2 showed contiguity firing first.

Owner selectors:
- `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:58-70 (migrated_from/migration_op_ref/first_generation CHECKs), :73-75 (format row immutable), :137-151 (no append before the format row; below first_generation; superseded generation)`
- `docs/coop/design-corrections/security/carrier-format.v3.md:168-227 (publication law)`
- `docs/coop/design-corrections/security/carrier-migration.v1.md`

### A37-03: CLOSED-AT-SOURCE-LEVEL (editorial residual ADV38-03)

Origin: claude-independent-design.v37 (advisory).

A foreign project binding is no longer carried by MIGRATION.CORRUPT on any path.

Owner selectors:
- `docs/v2/contracts/product-v1/security-and-lifecycle.md:1300-1301 (MIGRATION.CORRUPT scope; carrier project binding mismatch with domainDetail omitted), :1310-1312`
- `docs/coop/design-corrections/security/carrier-dispatch.v3.json:568-580 and :597-609 (carrier-project-binding-mismatch routes)`
- `docs/v2/architecture/commit-recovery-readonly.v3.md:58-69`

### A37-04: CLOSED-AT-SOURCE-LEVEL (residual ADV38-02)

Origin: claude-independent-design.v37 (advisory).

F46 and F51 have public projections, and all 9 phase routes in publicProjectionByPhase are schema-valid StepTerminations in the probe (ROUTES 9/9 VALID). Format-1 rows after TERMINAL and a UTF-16 F51 carrier are detected as split-brain (writer MIGRATION.CORRUPT; read-only quarantine requiring stable observations).

Owner selectors:
- `docs/v2/contracts/product-v1/security-and-lifecycle.md:1300 (writer F51), :1305 (read-only quarantine incl. F51), :1307 (F46 unknown-carrier-incompatible)`
- `docs/coop/design-corrections/security/carrier-format.v3.md:361-402 (§8.1 phase-specific routes)`
- `docs/coop/design-corrections/security/carrier-dispatch.v3.json:611-674 (publicProjectionByPhase.readOnlyRecovery and readOnlyStandingOfDispatchResult)`

### A37-05: CLOSED-AT-SOURCE-LEVEL (see RC37-A1)

Origin: claude-independent-design.v37 (advisory); bounded RC37-A1.

An out-of-vocabulary observation is a reference precondition, a product adapter defect with a valid RequestId is host-invariant, and a malformed retained record is evidence.corrupt.

Owner selectors:
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:160-164`
- `query_projection_model.v3.py:1504-1519 host_adapter_refusal, :1522-1546 observe_retained_availability`

### A37-06: CLOSED-AT-SOURCE-LEVEL (see RC37-01)

Origin: claude-independent-design.v37 (advisory); bounded RC37-01 SHOULD.

Complete-replay disagreement is no longer collapsed into corrupt bytes.

Owner selectors:
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:166-173, 186-191`

### A37-07: CLOSED-AT-SOURCE-LEVEL (RC37-A4 editorial retained)

Origin: claude-independent-design.v37 (editorial); bounded CLOSED-FOR-WORDING.

Standing prose names the current v6 layer and preserves dated counts as history.

Owner selectors:
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md:10-22, 1039-1052, 1103-1111 (current v6 binding; historical checkpoints 1083-1101 preserved)`
- `docs/v2/architecture/store-instance-lineage.v1.json:470 and :508 (currentStandingNote F00-F53)`
- `docs/v2/architecture/14-repository-and-module-layout.md:719-731`

### A37-08: ACCEPTED-AS-DESIGNED-UNCHANGED

Origin: claude-independent-design.v37 (advisory).

The registered payload schema bytes and every coverage2 identity minted against them stay unchanged. The superseded annotation remains readable in the schema, and native §10 governs it.

Owner selectors:
- `docs/v2/contracts/product-v1/native-evidence.md:2933-2944 (explicit annotation supersession)`
- `docs/coop/design-corrections/native/native-evidence.schemas.v2.json (registered payload schema bytes)`

### R1: CLOSED-FOR-SCHEMA-LAW

Origin: root termination-boundary assessment; bounded ACCEPTED-FOR-SCHEMA-LAW.

faultCause appears only on operational-failed, and reasonCodes only on indeterminate. Evaluator3 common admits exactly the 34 lawful combinations; the historical common admits 33 because its RunId pattern differs. No unlawful combination is admitted, and the query operation exception terminations remain admissible.

Owner selectors:
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json:739-1140 ($defs/StepTermination branches)`
- `docs/coop/design-corrections/workflows/schemas/common.schema.json (retained predecessor, identical branch law)`
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189`

### R2: CLOSED-FOR-SCHEMA-LAW

Origin: root termination-boundary assessment; bounded ACCEPTED-FOR-SCHEMA-LAW.

Across the 24 routes, an illegal pair is refused at schema admission (132 of 132) and a structurally lawful but owner-inconsistent pair is refused at owner parity (120 of 120). Zero outcomes were unexpected.

Owner selectors:
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json:945-1060 (11 exact faultCause/errorCode pairs incl. host-invariant)`
- `docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py (separate schema and parity controls)`

### RC37-01: CLOSED-AT-SOURCE-LEVEL

Origin: claude-source37-root-corrections-review.v1 (SHOULD).

Missing bytes route to evidence.missing, corrupt structural bytes (including an evidence-level remint refused structurally) to evidence.corrupt, and a fully reminted semantically false Run to evidence.regeneration-mismatch with the refused RunId as subject. An undeclared host exception inside the replay stack routes to SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant / HOST.INVARIANT_VIOLATED. The route is selected by class object, not text: a KeyError, and the query identity copy's own classes raised inside the stack, route by type, and a lawful Run admits again after restore.

Owner selectors:
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:166-173 (four typed close_run outcomes) and :186-191 (table rows)`
- `docs/coop/design-corrections/workflows/query_projection_model.v3.py:565-597 (close_retained_run)`
- `docs/coop/design-corrections/foundation/identity-model.v3.py:613-635 (EvidenceUnavailable, RegenerationMismatch, CompleteReplayMismatch), :654-681 (close_run normalization by exact class object), :1927 (restore maps to RegenerationMismatch)`
- `docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py:18-27 (declared UNAVAILABLE/MISMATCHES/REFUSALS)`
- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md:3, 11, 15`

### RC37-A1: CLOSED-AT-SOURCE-LEVEL

Origin: claude-source37-root-corrections-review.v1 (advisory).

A product adapter's own invalid observation with a valid RequestId terminates host-invariant, and a retained availability record failing identity availability admission is evidence.corrupt. No public code is added.

Owner selectors:
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:162-164`
- `query_projection_model.v3.py:1504-1519, 1522-1546`

### RC37-A2: CLOSED-AT-SOURCE-LEVEL

Origin: claude-source37-root-corrections-review.v1 (routed to integration).

Planning and pins bind current source38 bytes; the pin gates of all six groups pass.

Owner selectors:
- `docs/v2/architecture/implementation-normative-inputs.v6.json (30 inputs incl. run-termination-contract.v1.md)`
- `implementation-coverage.v1.json subjectManifestSha256`
- `implementation-planning-sources.v1.json architecture.manifestSha256`
- `five source-pins ledgers`

### RC37-A3: ACCEPTED-AS-DESIGNED

Origin: claude-source37-root-corrections-review.v1 (advisory).

request-rejected still admits all 19 D9ErrorCode members, which is deliberate. Class-specific error families belong to the D9 successor owner.

Owner selectors:
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json StepTermination request-rejected branch`

### RC37-A4: RETAINED-OPTIONAL-EDITORIAL

Origin: claude-source37-root-corrections-review.v1 (editorial).

This is harmless provenance wording. It could name the current normative layer at the next successor, and has no semantic effect.

Owner selectors:
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md:201 ("not a claim that candidate25 already specifies or implements that private table")`

### SI-1: CONFIRMED-RESOLVED

Origin: claude-source38-seal-integration-assessment.v1.

The typed replay mismatch no longer escapes the SEAL adapter as a host exception.

Owner selectors:
- `docs/coop/design-corrections/security/security_lifecycle_model_v1.py:1547-1550 (except IM.C.AdmissionError -> Reject(SEAL_CLOSE_RUN_REFUSED:...) from e)`
- `docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py`

### SI-2: CONFIRMED-INDEPENDENTLY

Origin: claude-source38-seal-integration-assessment.v1.

The lawful Run admits. The fully reminted false Run is refused with cause type exactly IM.CompleteReplayMismatch, chained to the replay stack's origin-free CompleteReplayMismatch. A structurally refused remint is refused with cause IM.C.AdmissionError. Foreign same-name classes raised by close_run propagate, as does a KeyError inside the comparison, and the lawful Run admits after restore.

Owner selectors:
- `security_lifecycle_model_v1.py:1527-1550`
- `identity-model.v3.py:654-681`

### SI-3: CONFIRMED

Origin: claude-source38-seal-integration-assessment.v1.

The security-local Reject key establishes no public origin; the outer host decides origin.

Owner selectors:
- `security_lifecycle_model_v1.py:175 (Reject carries no termination)`
- `docs/coop/design-corrections/public-detail-registry.v1.json`

### SI-A1: CARRIED-IMPLEMENTATION-BOUNDARY-UNDER-EXISTING-FAULT-OWNER

Origin: claude-source38-seal-integration-assessment.v1 (advisory).

A product outer host must route SEAL refusals by the Reject __cause__ type, not by the embedded diagnostic text. The existing fault owner already forbids text inference, so this is an implementation obligation, not a source defect.

Owner selectors:
- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md:3 (no origin from a prefix in the error text), :15 (retained regeneration versus live host-internal)`
- `docs/v2/architecture/repository-file-inventory.v1.json crates/host/src/finalization.rs and outcomes.rs rows`

### SI-4: CONFIRMED-INDEPENDENTLY

Origin: claude-source38-seal-integration-assessment.v1.

No current caller depends on the changed close_run class names.

Owner selectors:
- `foundation/atom_model.v1.py:897 and security/security_lifecycle_model_v1.py:1481 (the only non-test class-name matches; neither wraps close_run)`
- `workflows/query_projection_model.v3.py:596 (type name used only in host-invariant diagnostic text after typed routing)`

### SI-5: SUPERSEDED-BY-REBIND

Origin: claude-source38-seal-integration-assessment.v1 (limitation).

The pin-gated security owner suite runs and passes on source38.

Owner selectors:
- `docs/coop/design-corrections/security/source-pins.v1.json (rebound)`

### QF-1: CONFIRMED-INDEPENDENTLY

Origin: claude-source38-seal-integration-assessment.v1.

Both protections are retained and discriminated. The earlier failing expectation (root-final38 source37 overlay exit 1) is preserved as history, not reclassified.

Owner selectors:
- `docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py (read complete)`

### AUTHOR-V2-QUALIFICATION: CONFIRMED-ACCURATE; v2 REPORT PRESERVED UNEDITED

Origin: claude-source38-seal-integration-assessment.v1 v2Qualification.

The v2 sentence that class names were unchanged is overbroad for replay disagreement, caller-copy classes, the query route and restore. The qualification is correct and does not rewrite the v2 record.

Owner selectors:
- `identity-model.v3.py:627-635, 678-681, 1927`
- `query-projection-contract.v3.md:169`

### ROOT38-CARRIER-GRAMMAR: CLOSED-AT-SOURCE-LEVEL

Origin: root-source38-dispositions.v4 rootFollowups.

The NUL suffix and ASCII-hex BLOB holes are closed in all three encodings.

Owner selectors:
- `see A37-01`

### ROOT38-HOST-PROJECTION-SCOPE: CLOSED-AT-SOURCE-LEVEL (residual ADV38-01)

Origin: root-source38-dispositions.v4 rootFollowups.

A combined work-budget Run with native stage carriers now names the stage carrier. Arbitrary schema-valid extras are owner-validation-required, never lawful.

Owner selectors:
- `run-termination-contract.v1.md:23-38 (derived versus delegated members), :136-163 (carrier chosen from every condition at the primary rank)`
- `crates/host/src/outcomes.rs and finalization.rs inventory rows`

### ROOT38-FAULT-CHECK-ORDER: CLOSED (see QF-1)

Origin: root-source38-dispositions.v4 rootFollowups.

None beyond QF-1.

Owner selectors:
- `check-evaluator-faults.v3.py`

### QF-I1: CLOSED (see QF-1)

Origin: claude-source37-query-fault-author.v2.

None beyond QF-1.

Owner selectors:
- `check-evaluator-faults.v3.py`

### QF-I2: CLOSED (see RC37-A2)

Origin: claude-source37-query-fault-author.v2.

Pins are rebound.

Owner selectors:
- `five source-pins ledgers`

## Probes and command receipts

- **P38-SUBJECT** `probes/verify_subject.py`: LIVE candidate-subject.v38.json and snapshot verified member by member; parent37 manifest and 37->38 delta measured. Receipts: `receipts/subject-verification.json`, `receipts/manifest38-index.json`
- **P38-ARCHIVE** `probes/verify_archive_extract.py`: Archive 571aad4d... hashed; every member extracted into the two disposable copies and compared by hash and length. Receipts: `receipts/archive-verification.source38-pkg.json`, `receipts/archive-verification.source38.json`
- **P38-DELTA** `probes/make_delta_diffs.py`: Unified 37->38 diffs for all changed files (reading aid; diffs are not whole-file reads). Receipts: `receipts/delta-diffs/`
- **P38-GROUPS** `probes/run_reference_groups.py`: Six pinned reference groups with /tmp/opensip-architecture-review-env/bin/python -I -B on a verified disposable exact copy; copy re-verified before and after. Receipts: `receipts/reference/groups-report.json`
- **P38-PLAN** `probes/run_planning_checks.py`: check_implementation_planning --check and check_repository_file_inventory --check on the exact copy, plus independent v6/coverage/planning-source binding counts. Receipts: `receipts/planning-checks.json`
- **P38-PKG** `claude-author-package-successor.v15/verify-package.py (author verifier, executed on the verified copy)`: Package15 13 Run/control structural and full-replay checks plus 7 query checks against source38. Receipts: `receipts/package-verification/verification.json`
- **P38-TERM** `probes/probe_run_termination.py`: Independent derivation of the whole-Run termination over 11 actual closed Runs versus the owner model; native stage helper; semantically false Run; projection boundary; 47-cause bridge; mixed-owner cases. Receipts: `receipts/probe-run-termination.json`
- **P38-CARRIER** `probes/probe_carrier_sql.py`: Hostile TEXT/hex/NUL/BLOB grammar in three encodings, publication/first_generation/superseded/TERMINAL order laws, and open-dispatch phase routes over real SQLite carriers. Receipts: `receipts/probe-carrier-sql.json`
- **P38-SEALQ** `probes/probe_seal_query_fault.py`: SEAL adapter over lawful, reminted false, structural and foreign same-name exceptions; replay-stack exception-class coverage walk; graph query missing/corrupt/reminted/host-defect/foreign-class routes and retained availability records; fault pair schema-versus-parity discrimination; StepTermination admission enumeration. Receipts: `receipts/probe-seal-query-fault.json`
- **P38-STATIC** `probes/static_raise_reachability.py`: Syntactic escape analysis of owner exceptions from identity-model.v3 call sites that are not locally wrapped (attempt 2 accounts for call-site try blocks). Receipts: `receipts/static-raise-reachability.json`

Reference groups (reference interpreter `-I -B`, verified disposable copy):

| Group | Exit | Seconds | Copy unchanged |
|---|---|---|---|
| evaluator3 | 0 | 294.4 | True |
| foundation | 0 | 126.6 | True |
| integration | 0 | 17.2 | True |
| native | 0 | 3.0 | True |
| security | 0 | 0.9 | True |
| workflows | 0 | 9.7 | True |

Evaluator3 children: analysis-seal {"passed": true, "cases": 16}, atoms {"passed": 101, "failed": 0}, candidate-replay {"passed": true, "count": 4}, comparison-knowledge {"passed": true, "count": 1}, composition {"passed": true, "count": 20}, current-profile {"passed": true, "count": 22}, enumeration {"cases": 44, "mismatches": 0}, execution-inputs {"cases": 75, "mismatches": 0}, execution-replay {"passed": true, "count": 8}, faults {"passed": true, "count": 41}, full-replay {"passed": true, "count": 68}, native-replay {"passed": true, "count": 30}, policy-derivation {"passed": true, "count": 6}, provider-attribution-return {"passed": 47, "failed": 0}, query-projection {"passed": true, "count": 193, "failed": []}, workflow-projection {"passed": true, "count": 493, "failed": []}

Planning: `PASS: 320 source-bound mappings, 54 planned failure cases, private schema, owners and generated plan`; inventory: `PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches`.

Preserved failed probe attempts: `receipts/probe-carrier-sql.attempt2-order-not-isolated.json`, `receipts/probe-seal-query-fault.attempt1-probe-bug.json`, `receipts/probe-seal-query-fault.attempt2-query-structural-uncaught.json`, `receipts/runs/probe_carrier_sql.attempt1-harness-failure.run.json`, `receipts/runs/probe_carrier_sql.attempt1-harness-failure.stderr`, `receipts/runs/probe_carrier_sql.attempt1-harness-failure.stdout`, `receipts/runs/probe_carrier_sql.attempt2-order-not-isolated.run.json`, `receipts/runs/probe_carrier_sql.attempt2-order-not-isolated.stderr`, `receipts/runs/probe_carrier_sql.attempt2-order-not-isolated.stdout`, `receipts/runs/probe_seal_query_fault.attempt1-probe-bug.run.json`, `receipts/runs/probe_seal_query_fault.attempt1-probe-bug.stderr`, `receipts/runs/probe_seal_query_fault.attempt1-probe-bug.stdout`, `receipts/runs/probe_seal_query_fault.attempt2-query-structural-uncaught.run.json`, `receipts/runs/probe_seal_query_fault.attempt2-query-structural-uncaught.stderr`, `receipts/runs/probe_seal_query_fault.attempt2-query-structural-uncaught.stdout`, `receipts/runs/static_raise_reachability.attempt1-call-site-try-ignored.run.json`, `receipts/runs/static_raise_reachability.attempt1-call-site-try-ignored.stderr`, `receipts/runs/static_raise_reachability.attempt1-call-site-try-ignored.stdout`, `receipts/static-raise-reachability.attempt1-call-site-try-ignored.json`.

Root reference `root-final38-reference.v1` failed (analysis-seal child exit 1) and stays a failure; `root-final38-reference.v2` and the bound report `94b54adc...` are evidence only.

## Package15

- Manifest `6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e` (expected equal: True); verification `204742347ae79a5f5d3bbe86a2f7f44e7eba9406b1a32d89f1c71870c334499c` (expected equal: True).
- All 13 Run/control structural and full-replay checks and all 7 query checks passed against source38 on a verified copy.
- Mixed construction provenance: TypeScript-derived groups are source33 constructions and normalized/Rust groups are source30 constructions, bound to source38 without remint.
- A9/A10 partial-helper limits (package README): only the TypeScript checkpoint compares a partial consumer helper with the owner; six positives are owner-derived/replayed self-consistency; the helper exercises exists/none, leaves and/or/not unexercised and count-at-most/all-covered unimplemented; two-binding construction is incomplete with a single explicit binding.
- No identity remint and no consumer artifact repair were performed. Binding alone proves nothing, and author proposals grant no grades.
- No compiler, provider, OS or process-isolation qualification.

## TCB-SCOPE-01 (one shared assumption, 13 dependent rows)

Assumption: Selected authenticated in-process host/evaluator code is trusted; adversarial code sharing that process is outside this product threat model. Untrusted inputs are inert typed data and provider process boundaries still require real qualification.

- Coherent as a scope selection on source38. Admission §5 is byte-identical: item 4 admits no untrusted native/WASM and claims no sandbox; item 5 admits no imperative contributions or project hooks (admission-and-qualification.md:344-345).
- The source37 inconsistency is removed. prototype-report-inventory.md:37 and :179 now select versioned host-approved data projections with no executable report-hook admission, and coverage R02/R24 are rebound.
- What the assumption relies on was re-probed on source38. A fully reminted false Run passes owner closure and is refused only by complete replay (SEAL cause IM.CompleteReplayMismatch; query evidence.regeneration-mismatch; package semantic-controls1 owner ADMIT / semantic REFUSE).
- The typed boundary itself assumes trusted in-process code. close_run normalizes by exact class object, foreign same-name classes propagate, and undeclared exceptions fail closed as host-invariant. Adversarial code in the same process could raise identity classes directly, which is exactly what the assumption excludes.
- It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries (DR-G29/G30 and related gates), and all 32 gates are unperformed.

Consequence: Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING. Adjudication owner: Separate final application review by a fresh other origin excluding all 11 author, design and blind origins; not adjudicated here.

Dependent rows: RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c. The source37 `tcbScopeAccount` is unchanged; field mapping 37->38: {"id": "id", "assessedOnce": "assessedOnceAsOneAssumption", "dependentResidualIds": "dependentRows (+ dependentRowCount)", "assumption": "assumption (text carried verbatim)", "assessment": "substantiveCurrentAssessment (re-assessed on source38, not copied)", "standing": "standing (new) with the 37 value preserved in prior37Standing; consequence and adjudicationOwner made explicit"}.

## Disposition rows (107)

### F

- **F-01** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-02** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-03** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-04** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-05** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-06** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-07** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-08** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-09** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-10** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-11** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-12** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-13** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.
- **F-14** CARRIED-NOT-REGRADED (inherited-unchanged-37): Identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.

### Evaluation residuals

- **RES-EP13-01** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: Plan/derivation joins are recomputed inside complete replay (evaluator_replay_model.v3.py:60-65, 67-89). On source38 a Plan-consistent reminted false Run passes owner closure and is refused only by replay (P38-SEALQ, P38-TERM FALSE; package semantic-controls1). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-02** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01, assessed once on source38. No answer-provenance claim against adversarial in-process route regions is made. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-03** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: The seven-vector measurement stays finite history. The correction text and admission §2-4 are byte-identical to source37, and no delta file changes it. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-04** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Closed input schemas remain the product admission (StepTermination and query request enumerations in P38-SEALQ). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-05** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: This review verified the frozen subject outside every author instrument: live manifest, archive, 12,904 members and parent37 (P38-SUBJECT, P38-ARCHIVE). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-06** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: canonical.py and identity §3 are unchanged. Exact typed admission still refuses float/exponent/negative-zero; carrier SQL affinity conversions are storage behaviour under host record admission, not canonical admission. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-07** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: Seal binds Plan, execution plan, evidence, proof and verdict: a predicate-flip remint with valid new identities is refused as EVALUATOR_COMPLETE_PROOF_REPLAY at SEAL and as evidence.regeneration-mismatch at query (P38-SEALQ). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-08** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Bounded historical measurement; no product proof over all PlanIntents is claimed in source38 either. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-09** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: Provenance stays distinct from correctness: reminted mutants carry valid identities and are refused only by replay (P38-SEALQ; package semantic-controls1 owner ADMIT / semantic REFUSE). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-10** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: Author self-counters did not decide this review: the six groups, planning and package were re-executed here and probes were independent. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-11** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Historical checker failures stay recorded by cause. Likewise the failed root-final38-reference.v1 run is preserved as failed and not relabelled. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-12** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. No sole Python answer-provenance guard is carried into product authority. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-13** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. This review's probes deep-copy fixtures before mutation (fixture isolation only). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-14** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: The differential census is not used as an oracle; unchanged. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-15** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: C-2 v4 self-census not elevated; plan/derivation schemas unchanged in 38. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-16** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Producer flags cannot bypass replay (P38-SEALQ). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-17** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Text-only disclosures remain text-only. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-18** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-19** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING]: Substantive semantic review was performed on source38 with discriminating probes; pins and passing counts were not treated as acceptance. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-01** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-02** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: No name/punctuation scan decides product scope; unchanged. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-03** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The replay-stack module walk confirms that loaded instances are reachable in-process, which is exactly why the boundary is trust rather than containment. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-04** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01; one TCB account is used. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-05** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Contradictory prose requires substantive review; unchanged. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-06** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Historical attacker cost preserved as history. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-07** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-37) [author grade PENDING]: Original environment preserved; this review names its own interpreter and pins. The historical limitation is preserved; no historical guard is claimed repaired.
- **AX6** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.
- **AX9** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.
- **MD5** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.
- **RX2c** ASSESSED-CONSISTENT-GRADE-PENDING (new-38) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The historical limitation is preserved; no historical guard is claimed repaired.

### AR

- **AR-01** NO-NEW-ISSUE (new-38): Admission §1 is unchanged. The R1/R2 StepTermination closure was probed by exhaustive enumeration, with 34 lawful combinations admitted and none unlawful.
- **AR-02** NO-NEW-ISSUE (inherited-unchanged-37): Admission §§2-4 and qualification-gates are unchanged; all 32 gates remain unqualified.
- **AR-03** NO-NEW-ISSUE (inherited-unchanged-37): Security S3 discovery was re-read complete on source38; the security and integration groups pass.
- **AR-04** NO-NEW-ISSUE (inherited-unchanged-37): Security S4 trust time re-read complete on source38; no probe.
- **AR-05** NO-NEW-ISSUE (inherited-unchanged-37): Security S5/S6 re-read complete on source38; no probe.
- **AR-06** NO-NEW-ISSUE (new-38): The carrier DDL platform CHECK names the four S8 machine ids and refuses NUL-bearing platforms (P38-CARRIER); security group pass.
- **AR-07** NO-NEW-ISSUE (inherited-unchanged-37): Native §§3/5/9 re-read complete on source38 (the native delta is the §10 owner pointer); native group passes.
- **AR-08** NO-NEW-ISSUE (inherited-unchanged-37): The workflows-and-surfaces delta is confined to §9; repair per-requirement disclosure is unchanged.
- **AR-09** NO-NEW-ISSUE (new-38): identity-and-evidence.md is unchanged, and the reference close_run boundary now types its outcomes. A37-06 is closed by RC37-01 (P38-SEALQ).
- **AR-10** NO-NEW-ISSUE (inherited-unchanged-37): Baseline/comparison unchanged; comparison-knowledge child passes.
- **AR-11** NO-NEW-ISSUE (inherited-unchanged-37): Import wrapper and history/runtime limits unchanged; no independent import probe.
- **AR-12** NO-NEW-ISSUE (inherited-unchanged-37): Native §4 unchanged; atoms child passes.
- **AR-13** NO-NEW-ISSUE (new-38): Its 37 routing reason, S37-03, is closed at source level.
- **AR-14** ADVISORY-ONLY (new-38): A37-03 closed; ADV38-02 and ADV38-03 remain carrier/read-only advisories.
- **AR-15** NO-NEW-ISSUE (new-38): Its 37 routing reason, S37-02, is closed: report projections are data only.
- **AR-16** ADVISORY-ONLY (new-38): S37-01 closed by run-termination-contract.v1; ADV38-01 on delegated detail validation.

### FW

- **FW-01** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-02** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-03** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-04** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Runtime/test/history stay non-Coverage per workflows §4 (re-read complete on source38); inventory row unchanged.
- **FW-05** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-06** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-38): The finalization row now routes the retained analysis projection through outcomes.rs and separately validates delegated attribution, detail and authority. S37-01 is closed; SI-A1 and ADV38-01 are carried to this owner.
- **FW-07** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-08** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-38): The outcomes row now names run-termination-contract.v1 as the derivation law. A37-05/06 are closed at the query owner (RC37-A1/RC37-01).
- **FW-09** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-10** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-11** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-12** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-13** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-38): S37-03 advisory registry/schema admission is closed.
- **FW-14** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.
- **FW-15** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (inherited-unchanged-37): Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.

### Inherited residuals

- **DR-001** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): current-source-map and residual ledgers are unchanged; this review refreshed the reading path on source38. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-002** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): The identity/evidence/proof chain was re-probed: typed close_run outcomes and complete replay (P38-SEALQ; package 13 closures). The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-003** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): The carrier v3 grammar/publication/route corrections were probed (P38-CARRIER). The 54 recovery cases remain not executed, and real platform demonstration remains a release requirement. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-004** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Native §4 and Phase-1A semantics unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-005** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): Executable custody reference groups pass on source38; native product carrier qualification is still required before release. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-006** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Descriptor graph unchanged; the full-replay child passes. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-007** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): S37-01 closed: the D9 cause reduction and coverageId join have one owner. The D9 published successor artifact remains a carried implementation-unit obligation (native §10:3133-3147; evaluator-fault-contract.v3.md:20), not a new blocker. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-008** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Applied retention posture unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-009** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): The termination projection keeps executionId delegated and outside the derived members, preserving lifetime neutrality. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-010** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): S37-02 closed: bounded first-party composition with no executable report hooks. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R01** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Fact-plane successor schemas unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R02** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Fact identity unchanged; arbitrary imperative plugins remain outside D-371 (admission §5 items 4-5 re-read). The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R03** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): plan2/exec-plan2 unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R04** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): The security carrierFormat axis and format-aware reader staging (S9:736-777) join the core bridge; the security group passes. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R05** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Rust protocol major 3 unchanged; native group passes. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R06** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): Proof mismatch is typed and restore maps it to RegenerationMismatch (identity-model.v3.py:1927). The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R07** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): Retained availability records and graph availability observations have typed routes (query §7:160-164; P38-SEALQ). The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R08** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): S37-01 closed. Branch-specific optional fields are closed by R1/R2, and the D9 published successor artifact remains carried (DR-007). The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R09** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Semantic IDs exclude attempt identity; unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R10** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): OPEN: this nonblind review cannot close the fresh blind implementer litmus. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R11** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): Carrier advisories A37-01..04 are closed at source level, with ADV38-02 residual. Real platform durability is unmeasured, and the 54 cases are not executed. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R12** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): Depends on TCB-SCOPE-01, assessed once on source38. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R13** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Versioning successor unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R14** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): CFG-6/TM unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R15** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-37): Trusted request context unchanged. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.
- **DR-011-R16** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-38): S37-02 closed: no executable report-hook admission, so the bounded first-party product authority is preserved. The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.

### Scoped review owners

- **DR-201** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-37): Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.
- **DR-202** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-37): Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.
- **DR-203** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-37): Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.
- **DR-204** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-37): Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.
- **DR-205** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-37): Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.

Every row: appliedByThisReview=false, finalApplicationOutcomeGranted=false.

## Read scope

Fresh complete reads (source38):
- `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` 7fdaae67ae6f4439 (220 lines): added in 38; complete
- `docs/coop/design-corrections/foundation/run-termination-goldens.v1.json` 9bdde8236ce24b29 (265 lines): added in 38; complete
- `docs/coop/design-corrections/foundation/run_termination_model.v1.py` 2b9dd91782147182 (304 lines): added in 38; complete
- `docs/v2/architecture/implementation-normative-inputs.v6.json` efa3777c6a79ce09 (155 lines): added in 38; complete
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` 857d6bbed265a51c (1469 lines): changed; complete sequential chunks
- `docs/v2/contracts/product-v1/native-evidence.md` cfe6962777fe1e91 (3795 lines): changed; complete sequential chunks (lines 3789 and 3791 verified by tail print)
- `docs/v2/contracts/product-v1/security-and-lifecycle.md` 9ca85de10f4f364b (1523 lines): changed; complete sequential chunks
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md` 6a504eb5657ab9a2 (206 lines): changed; complete
- `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md` 1f8128bb46e2a440 (223 lines): changed; complete
- `docs/coop/design-corrections/security/carrier-format.v3.md` 10608c16c510a4eb (655 lines): changed; complete
- `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql` b82d63c07bc7ca0a (171 lines): changed; complete
- `docs/coop/design-corrections/security/carrier-migration.v1.md` 446c73dc9c95ae29 (259 lines): changed; complete
- `docs/coop/design-corrections/security/carrier-dispatch.v3.json` 62b1958e7e2832ba (676 lines): changed; complete
- `docs/coop/design-corrections/security/check-carrier-v3.py` 4948301df3752c52 (1063 lines): changed; complete in two ranges (440-1063 before context compaction, 1-440 after)
- `docs/v2/architecture/commit-recovery-readonly.v3.md` 3b32d24a3c6e7195 (463 lines): changed; complete
- `docs/v2/architecture/attempt-custody.schema.v1.json` 60a881545e63a9e8 (172 lines): changed; complete
- `docs/v2/architecture/store-instance-lineage.v1.json` 919d1717b53f202b (628 lines): changed; complete
- `docs/v2/architecture/14-repository-and-module-layout.md` 1ea7a5c2b6aa878f (731 lines): changed; complete
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` e207c8db06ff24ef (1131 lines): changed; complete
- `docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py` 26e88580acff3d93 (107 lines): changed; complete
- `docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py` 57e0d9d8e24cd1a1 (73 lines): changed; complete
- `docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py` b0afeb841fe94d13 (267 lines): changed; complete
- `docs/coop/design-corrections/inherited-residuals.proposed.md` 4b2b992b06abd9cd (46 lines): unchanged 37->38; freshly re-read complete

Fresh delta reads (complete 37->38 diff plus ranges; not whole-file):
- `docs/coop/design-corrections/foundation/identity-model.v3.py` 9376aaae10a7fbe6: complete 37->38 diff; ranges 1-70, 600-690, 1412-1439; grep context of every native_admission()/workflow_admission() call site
- `docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py` cceeb42bd2fb2212: complete 37->38 diff
- `docs/coop/design-corrections/security/security_lifecycle_model_v1.py` d0ef9814d27b86f1: complete 37->38 diff; lines 175, 1527-1550 located by grep
- `docs/coop/design-corrections/workflows/query_projection_model.v3.py` bb9de8f7c7fece1b: complete 37->38 diff; ranges 565-597, 1504-1546
- `docs/coop/design-corrections/workflows/check-query-projection.v3.py` 82eddd7487af9863: complete 37->38 diff (executed: 193 checks)
- `docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` bc8a82e08bc3bebc: complete 37->38 diff (executed in evaluator3 group)
- `docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py` 2f51675e4e7e73a5: complete 37->38 diff
- `docs/coop/design-corrections/workflows/schemas/common.schema.json` f73094dd175c44f2: complete 37->38 diff; overlay bytes identical to 38 were reviewed in the bounded root-corrections review
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json` 36124787ace53c9b: complete 37->38 diff; overlay-identical
- `docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json` 33a43bd86ec7bcb1: complete 37->38 diff; overlay-identical
- `docs/coop/design-corrections/workflows/workflow-cases.v1.json` f67d22f1a3358864: complete 37->38 diff; overlay-identical
- `docs/coop/design-corrections/workflows/check_workflows.v1.py` 88edad11d904d1fa: complete 37->38 diff; overlay-identical (executed in workflows group)
- `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py` 4f356745f409b64c: complete 37->38 diff; overlay-identical (executed: 493 checks)
- `docs/coop/design-corrections/workflows/workflows-report.v1.json` f327d25587db1fbd: complete 37->38 diff
- `docs/coop/design-corrections/foundation/source-pins.v1.json` 1cc1c7d4aa1c7be8: complete 37->38 diff (pin gate executed by groups)
- `docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json` dba63a8a26295e5f: complete 37->38 diff
- `docs/coop/design-corrections/native/source-pins.v2.json` b313d9cb2b98a101: complete 37->38 diff
- `docs/coop/design-corrections/security/source-pins.v1.json` dc738371639ca0e9: complete 37->38 diff
- `docs/coop/design-corrections/workflows/source-pins.v1.json` 1cc1c7d4aa1c7be8: complete 37->38 diff
- `docs/v2/architecture/implementation-coverage.v1.json` 8710671d6c7bc26a: complete 37->38 diff (planning checker executed)
- `docs/v2/architecture/implementation-planning-sources.v1.json` e66f6c026827aea7: complete 37->38 diff
- `docs/v2/architecture/repository-file-inventory.v1.json` 4f1d37fa85af910d: complete 37->38 diff plus row-by-row JSON comparison (only finalization.rs and outcomes.rs rows changed)
- `docs/v2/architecture/prototype-report-inventory.md` 3f4d4dd2246a9dd3: complete 37->38 diff; overlay bytes identical to 38 were read completely in the bounded review

Inherited unchanged from the source37 complete read (hash recomputed):
- `docs/v2/contracts/product-v1/README.md` c53633c2c8e056de
- `docs/v2/contracts/product-v1/identity-and-evidence.md` 39b06021d2233825
- `docs/v2/contracts/product-v1/admission-and-qualification.md` 69cd6ba3cb41ed19
- `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` ae4523a224bf6e21
- `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` 8649b8b079ccbd8f
- `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` 4889ab4baef50fa7
- `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` 1640740f71ab5018
- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` 5731b41d191d36f0
- `docs/coop/design-corrections/foundation/target-attribution.schema.v2.json` bd938f11c584be65
- `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` 2d5719b57dc65095
- `docs/coop/design-corrections/native/fact-batch.schema.v3.json` a963abd38fb2cf8a
- `docs/coop/design-corrections/native/occupancy-companion.schema.v1.json` 983864b16ec8ea9c
- `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` 868c3cf241af9ecc
- `docs/coop/design-corrections/hydradb-dispositions.proposed.md` 9a15484c69509257
- `docs/coop/design-corrections/current-source-map.proposed.md` 5229359680be8e36
- `docs/v2/architecture/commit-recovery-plan.v1.json` cbaac9b1651fe02e
- `docs/v2/architecture/report-asset-binding.v1.json` 71363c0637d4405d
- `docs/v2/architecture/implementation-normative-inputs.v5.json` 4b4b35b781928330
- `docs/coop/design-corrections/security/carrier-highwater.schema.v1.json` 1bbfd9135bd9492e
- `docs/operations/check_implementation_planning.py` dc7ac14ab75b0013
- `docs/operations/check_repository_file_inventory.py` ea2e171e03fb7b64

## Retained obligations and authority

- residuals: 30
- authorGradesPending: 30
- condition2Obligations: 28
- condition2Source: docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (unchanged 37->38)
- qualificationGatesUnperformed: 32
- qualificationGatesQualifiedTrue: 0
- recoveryCasesNotExecuted: 54
- d9PublishedSuccessor: Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.
- finalApplication: Must be a fresh other origin excluding all 11 author, design and blind origins.
- Authority: {"gradeGranted": false, "activationGranted": false, "implementationAuthorized": false, "blindReconstructionClaimed": false, "source37AcceptanceInherited": false, "frozenInputsModified": false, "applicationOrReadinessGranted": false}

## Limitations

- Nonblind review. The reviewer read author packages, author and root receipts and prior reviews. No original or current blind consumer artifact, author blind diagnosis or root replay oracle was accessed.
- Reference Python models over synthetic native-admitted inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or crypto is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed.
- Large changed reference code and ledgers (identity-model.v3.py, security_lifecycle_model_v1.py, query_projection_model.v3.py, checkers, pins, coverage, planning sources, inventory) were read as complete 37->38 diffs plus named ranges, and several were executed. They are listed under fresh38DeltaRead and are not claimed as whole-file reads.
- Host-defect and foreign-class cases are in-process monkeypatches, always restored. Carrier probes ran on the reference interpreter's SQLite only.
- Static escape analysis is syntactic; the replay-stack coverage walk demonstrates class objects, not retained-byte reachability.
- Probe attempts with harness or probe defects are preserved beside the reruns (preservedFailures) and were not counted as results.
- F-01..F-14 content lives outside the snapshot and was not re-derived.
- No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.
