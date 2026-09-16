# Bounded review of root corrections overlay — source37

**Outcome: PARTIAL.**

- **Substantively corrected:** S37-02, S37-03, R1 and R2.
- **Addressed with advisories:** A37-05 and A37-07.
- **Not closed:** A37-06 (RC37-01, SHOULD).
- **Integration:** a planning and pin rebind is required (RC37-A2).

No final design, application, readiness or grade is granted. My original source37 review stays immutable and CHANGES_REQUIRED.

## Subject and verification

- **Overlay manifest:** `subject-manifest.json`, SHA-256 `db9b7b3f3fbec833229fbd6e0c37cdc7bfed35ffabf3b6baabf709d35b380e52`, matching dispatch.
- **Base:** source37 manifest `245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680`.
- **Overlay rows:** all 12 match their `sha256`/`bytes`, and each base file equals its `beforeSha256`.
- **Disposable copy:** 12,900 source files verified and overlay applied; post-overlay verification shows no mismatch (`receipts/overlay-copy.json`).
- **Probes and checkers:** every run proves no copy file changed.

## Item dispositions

### S37-02 — CLOSED-BY-OVERLAY-TEXT (subject to integration rebind RC37-A2)

R02 (line 37) now reads "Presentation consumes versioned host-approved data projections only. Executable report hooks are not admitted under admission-and-qualification §5; trusted built-in projection and rendering code remain host-owned." R24 External tools (line 179) reads "Versioned host-approved data projections from selected admitted first-party capabilities ... host-owned validation, keys and rendering; no executable report-hook admission". This agrees with admission §5 items 1, 3, 4 and 5. Searching the overlay inventory case-insensitively for hook/worker/isolat/sandbox finds only these two negations (lines 37 and 179); no worker-lane or isolation claim remains. R01-R23 are unchanged. The coverage owners (report-view.ts, reporting/projection.rs) now fit the text.

### S37-03 — CLOSED-FOR-SCHEMA-AND-CONTROLS (subject to integration rebind RC37-A2)

The added else branch (graph-query.schema.json:1190-1200) makes admission equal the "true exactly for four operations" law across all 20 operations x advisory {true, false} (probe S3: overlayEqualsLaw=true; base violated 13 non-advisory operations). Graph operations keep their existing const false. Consumers: no retained query-response JSON fixture exists (0 scanned); query_surface_projection emits advisory False only for graph and coverage.show responses; command-inventory names query-response only as a parity field. No consumer admission changes. The overlay controls passed (check-query-projection 162/162, including 6 non-advisory and 9 advisory rows). graph-query.schema.json is not a registered payload document and not in registered_schema_documents before or after; it is a v5 normative input (see RC37-A2).

### A37-05 — SUBSTANTIVELY-ADDRESSED-WITH-ADVISORY (RC37-A1)

See RC37-A1.

### A37-06 — NOT-CLOSED (RC37-01 SHOULD)

A deliberate evidence.corrupt route with the replay subject and an actual fully reminted mutant through the strong public query was added and passes. It conflicts with the evaluator fault owner route for complete-replay-mismatch and separates structural, semantic and host-defect causes only by subject text. My original A37-06 remedy accepted evidence.corrupt "if chosen deliberately"; that remedy overlooked evaluator-fault-contract.v3.md:15 and is corrected here.

### A37-07 — CLOSED-FOR-WORDING (RC37-A2 integration consequence; RC37-A4 editorial)

The build-plan lines 10-22 and 1043-1052 now name the v5 normative-input binding and the coverage subjectManifest instead of candidate25 ownership. Historical receipts at 1083-1099 are preserved. The claimed binding (planning-sources architecture.manifestSha256 = coverage subjectManifestSha256 = 4b4b35b7...) holds for source37 bytes.

### A37-08 — UNCHANGED-AS-INTENDED

Native §10 supersession of the registered schema annotation is unchanged; native-evidence.schemas.v2.json bytes are unchanged in the overlay (not an overlay row).

### R1 — ACCEPTED-FOR-SCHEMA-LAW (reference; producers unchanged)

Both common StepTermination definitions are identical before and after (probe R12.defsEqual). faultCause is now refused on success, policy-failed, request-rejected, indeterminate and interrupted; reasonCodes on every class except indeterminate. An exhaustive class x {absent + 12 faultCause} x {reasonCodes absent/present} x {absent + 19 errorCode} enumeration (3120 combinations) gives: base 990 admitted, overlay 34; 956 removed; 0 newly admitted; 0 removed combinations lawful under the D9 predicate; 0 overlay admissions unlawful. The union had no faultCause field and the successor (workflows-and-surfaces §0:66, §9:1140-1148) declares it only for operational-failed. So refusing faultCause "none" on other classes follows the successor field closure, not a stale union rule. D9 v1.14 scenarioAxes faultCause "none" values are axes, not carriers. Producers: 24 evaluator fault routes and 24 native public routes validate identically before and after. The 25th native key (release-capability-undeclared) returns None by design (notATermination), a probe artifact. Of 90 termination-shaped JSON fixture objects, exactly the 12 new reject vectors (workflow-cases terminationVectors/reject/12-23) change admission.

### R2 — ACCEPTED-FOR-SCHEMA-LAW

operational-failed now requires one of exactly 11 faultCause/errorCode pairs equal to workflows_model.FAULT_TO_ERROR, including host-invariant -> SYSTEM.OUTCOME.ILLEGAL_STATE (probe R12.operationalPairsEqualHostMap=true). The existing required [errorCode, faultCause] and faultCause != none remain. Maintained controls ran and passed on the overlay copy: check_workflows.v1 1816 passed / 0 failed (legacy common profile, including termination.fault-pairs-equal-host-fault-map and the 12 reject vectors), check-workflow-projection.v3 493 / 0 failed (current common:3 profile, including current-termination-fault-pairs-equal-host-map and all shared vectors).

## New SHOULD finding

### RC37-01 (A37-06) — The new graph-query route for complete-replay disagreement conflicts with the existing evaluator fault owner route for the same condition and selects by exception text

**Owner selectors**

- overlay query-projection-contract.v3.md:164 and §7 table row at line 181 (structurally admitted retained Run whose complete proof replay disagrees -> HOST.IO_FAILURE / evidence.corrupt; subject preserves the diagnostic)
- foundation/evaluator-fault-contract.v3.md:15 ("Complete semantic replay disagrees with an otherwise admitted sealed result | evidence.regeneration-mismatch under the retained regeneration boundary; a live first-party evaluator contradicting its own reconstruction is a host invariant fault") and :72-75
- foundation/evaluator-fault-observation.schema.v3.json x-opensip-routes "complete-replay-mismatch:retained-regeneration" (HOST.IO_FAILURE, host-io, evidence.regeneration-mismatch) and "complete-replay-mismatch:host-internal" (SYSTEM.OUTCOME.ILLEGAL_STATE, host-invariant, HOST.INVARIANT_VIOLATED)
- foundation/evaluator-fault-contract.v3.md:3 (the host applies the route for the boundary and "does not infer origin from ... a prefix in the error text"); overlay query contract :160 ("never by a filename, exception prefix or caller-supplied fault origin")
- overlay query_projection_model.v3.py close_retained_run (unchanged catch-all Exception -> evidence.corrupt)

**Observed** (`receipts/probe-overlay-semantics.json#A6`)

- `root-severity-mutant`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `EVALUATOR_COMPLETE_PROOF_REPLAY`; structural closure ADMIT.
- `fail-to-pass`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `EVALUATOR_COMPLETE_PROOF_REPLAY`; structural closure ADMIT.
- `indeterminate-laundered`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `EVALUATOR_COMPLETE_PROOF_REPLAY`; structural closure ADMIT.
- `execution-deficiency-erased`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `EVALUATOR_COMPLETE_PROOF_REPLAY`; structural closure ADMIT.
- `structural-reference-identity`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `REFERENCE_IDENTITY`; structural closure REFUSE:REFERENCE_IDENTITY.
- `missing-proof-object`: REFUSE HOST.IO_FAILURE/evidence.missing, exit 4; subject `proof3:d9d486652843d68156ea050923cfcecb3b475352fad8e0ed90e50ab61e5b928`; structural closure REFUSE:EVIDENCE_UNAVAILABLE:proof3:d9d486652843d68156ea050923cfcecb3b475352fad8e0ed90e50ab61e5b928e.
- `host-defect-in-close_run`: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4; subject `simulated host evaluator defect`; structural closure None.
- `positive-control-after-restore`: ADMIT None/None, exit None; subject ``; structural closure None.

**Owner routes**

- `promised-bytes-lost:evidence-store` → {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"} / evidence.missing.
- `complete-replay-mismatch:retained-regeneration` → {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"} / evidence.regeneration-mismatch.
- `complete-replay-mismatch:host-internal` → {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE", "faultCause": "host-invariant"} / HOST.INVARIANT_VIOLATED.

**Consequence.** Two owners now publish different public details for the same named condition: the query owner gives evidence.corrupt, and the evaluator fault registry gives evidence.regeneration-mismatch (retained) or HOST.INVARIANT_VIOLATED (host-internal). The structural refusal (REFERENCE_IDENTITY), all four semantic mutants and a simulated host defect inside close_run all project to the same class, code and detail. They differ only in subject text, which is the exception-prefix selection both contracts forbid. Operators get the corrupt-bytes remedy for a semantically false Run and for a host bug. The overlay control proves the refusal but cannot detect the owner conflict. The public fail-closed outcome (exit 4, no items, no Run) is correct, so this is SHOULD, not MUST.

**Minimal remedy.** Route this row through the evaluator fault registry rather than a query-local choice: retained complete-replay mismatch -> evidence.regeneration-mismatch, and a live/host defect -> host-invariant. Type the replay-mismatch observation (for example identity RegenerationMismatch or a typed fault observation) instead of catching every Exception. If root prefers evidence.corrupt, amend the evaluator fault contract, registry and routes in the same successor with a stated remedy distinction. Add a control proving that the structural, semantic and host-defect refusals are distinguishable by typed route, not by subject text.

## Advisories

### RC37-A1 (A37-05) — The closed availability vocabulary and ReferenceCallPrecondition are honest reference-harness law; the product-host outcome should cite the existing host-invariant route

The overlay closes the vocabulary (retained, partial, purged, expired, corrupt, unavailable, plus the direct missing alias). Every present null, wrong type, unknown token, case or whitespace variant, bytes or container value raises ReferenceCallPrecondition(host.availability); omitted stays allowed (probe A5, 17 rows). Request-schema refusal precedes it, as does missing-Run refusal. This is not a hidden new public code, and it removes the silent grant-by-omission the original advisory named. The RequestId analogy is only partial. Without a RequestId no failure envelope can be built, but with a valid RequestId an out-of-vocabulary observation leaves a representable public outcome. The existing evaluator fault law already routes an "Invalid host-generated internal layer" to operational-failed / SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant / HOST.INVARIANT_VIOLATED (evaluator-fault-contract.v3.md:11), and that termination and envelope validate (A5.hostInvariantRouteRepresentable). The overlay text names only what the observation must not become and leaves the product host outcome to be invented. A malformed availability record read from retained store bytes is a different cause (identity availability admission / corruption) from an adapter bug.

- **Remedy:** Add one sentence: a product host adapter that produces an out-of-vocabulary observation terminates by the existing host-invariant route; unreadable or invalid retained availability record bytes follow identity availability admission. No new code is needed.
- **Disposition:** SUBSTANTIVELY-ADDRESSED-FOR-REFERENCE; product-host pointer advisory

### RC37-A2 (integration) — The overlay invalidates the current planning binding that A37-07 wording names; a rebind is required before integration

check_implementation_planning --check on the verified overlay copy exits 1 with "Planning source changed: query" and stops at the first failure (preserved failure, receipts/runs/check_implementation_planning.*). The full stale-binding list is in receipts/probe-planning-binding.json. implementation-normative-inputs.v5.json still pins the pre-overlay bytes of ['docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md']; implementation-coverage sources ['query', 'report', 'workflows-and-surfaces'] are stale; the five source-pins files and workflows-report still pin changed files. The new build-plan sentence ("Current planning is bound by the architecture.manifestPath and manifestSha256 in that record") is accurate for source37, but it is not true of any candidate that includes this overlay until v5, coverage and pins are rebound. The instruction forbade regeneration here, so this is not a defect of the correction text.

- **Remedy:** At integration, rebind a successor normative-input manifest, regenerate coverage selectors (R02/R24 values and workflows-and-surfaces §9 onward shift) and source pins, then re-run the planning checkers. The A07 wording should then name that successor.
- **Disposition:** ROUTED-TO-INTEGRATION

### RC37-A3 (R1/R2) — request-rejected still admits fault-family errorCodes (no global partition, deliberately); union field placements not imported

All 19 D9ErrorCode members remain admitted on request-rejected, including the 11 fault-map codes, so request-rejected+HOST.IO_FAILURE still validates. This matches root's deliberate choice and ce3 A1; no legitimate operation-specific request-rejected route is excluded (the request-rejected errorCode set is identical base versus overlay). The superseded D9 v1.14 hostTerminationUnion also placed runId/coverageId/executionId/details per class (for example no runId on request-rejected, coverageId only on indeterminate). The successor StepTermination owns that closure (workflows-and-surfaces §0:66), and the overlay imports none of those placement rules; this review did not assess them.

- **Remedy:** None required for R1/R2. If class-specific error families or field placement are wanted, decide them in the D9 successor owner, not by importing the superseded union.
- **Disposition:** ACCEPTED-AS-DESIGNED; placement outside R1/R2 scope

### RC37-A4 (A37-07) — Remaining candidate25 mentions are provenance or historical, apart from one proposal sentence

Overlay build plan lines 10 and 15 are the new provenance wording. Lines 1089 and 1098 sit under "Historical author verification checkpoints" and are preserved receipts. Lines 777 and 926 are provenance. Line 201 still says "not a claim that candidate25 already specifies or implements that private table", which is harmless provenance but could name the current normative layer instead.

- **Remedy:** Optional editorial change at the next rebind.
- **Disposition:** ACCEPTED-WITH-EDITORIAL-NOTE

## Registered payload and retained-identity consequence

- **registeredPayloadIdentity.** No change. payloadSchemaDigest is the raw SHA-256 of the registered document named by x-opensip-payload-registry, and no registered or digest-domain document is an overlay row. None $refs StepTermination, GraphQueryResponseV1, evaluator3 common or graph-query. imported-evidence, test-execution and policy-document(.v2) $ref other workflows common definitions (Blob, LogicalPath, Sha256Hex, ...), which the overlay does not change (the common-schema diff touches only StepTermination). No overlay file is in registered_schema_documents before or after.
- **retainedIdentities.** No reminting required for source37 fixtures. Four actual closed Runs rebuilt on the overlay copy have RunIds identical to the retained source37 review receipts (declares-exists, incoming-incomplete, missing-inventory, owner graph). No retained Run closure, import payload or H-domain record carries a StepTermination or query response.
- **pinsAndPlanning.** Raw digests of all 12 files change; the five source-pins files, workflows-report, normative-inputs v5, coverage sources and planning-sources architecture record still carry pre-overlay digests (RC37-A2). These are review pins, not payload identities.
- **notAssessed.** A future signed product release closure that ships these schema documents would get new closure bytes; no such retained closure exists in source37.

## Probes

- **P-COPY:** `probes/make_overlay_copy.py` (sha256 `78e50cabc4057772…`), receipt `receipts/overlay-copy.json`.
- **P-DIFF:** `probes/make_diffs.py` (sha256 `396bfa63619215a8…`), receipt `receipts/diff-summary.json`.
- **P-SEM:** `probes/probe_overlay_semantics.py` (sha256 `843220923dc4d8ea…`), receipt `receipts/probe-overlay-semantics.json`.
- **P-PLAN:** `probes/probe_planning_binding.py` (sha256 `61b6b7a889721737…`), receipt `receipts/probe-planning-binding.json`.

Key probe results:

- **S3:** overlay equals law = True. The base violated it for 13 non-advisory operations. Consumer admission changes: [].
- **A5:** {"omitted": "ADMIT", "retained": "ADMIT", "partial": "ADMIT", "purged": "REFUSE", "expired": "REFUSE", "corrupt": "REFUSE", "unavailable": "REFUSE", "missing": "REFUSE", "unknown-token": "REFERENCE-CALL-PRECONDITION", "case-variant": "REFERENCE-CALL-PRECONDITION", "trailing-space": "REFERENCE-CALL-PRECONDITION", "null": "REFERENCE-CALL-PRECONDITION", "false": "REFERENCE-CALL-PRECONDITION", "zero": "REFERENCE-CALL-PRECONDITION", "list": "REFERENCE-CALL-PRECONDITION", "dict": "REFERENCE-CALL-PRECONDITION", "bytes": "REFERENCE-CALL-PRECONDITION"}.
- **A5, host-invariant route representable:** {"termination": true, "envelope": true}.
- **R12 exhaustive:** {"combinations": 3120, "admittedBase": 990, "admittedOverlay": 34, "newlyAdmitted": [], "newlyAdmittedCount": 0, "removedCount": 956}.
  - Removed but lawful: [].
  - Admitted but unlawful: [].
  - Request-rejected error codes: {"base": 19, "overlay": 19, "equal": true}.
  - Operational pairs equal host map: True.
- **R12 fixtures:** 90 termination-shaped objects. Changed only: ['/terminationVectors/reject/23', '/terminationVectors/reject/22', '/terminationVectors/reject/21', '/terminationVectors/reject/20', '/terminationVectors/reject/19', '/terminationVectors/reject/18', '/terminationVectors/reject/17', '/terminationVectors/reject/16', '/terminationVectors/reject/15', '/terminationVectors/reject/14', '/terminationVectors/reject/13', '/terminationVectors/reject/12'].
- **Run identity stability:** {"declares-exists": true, "incoming-incomplete": true, "missing-inventory": true, "owner-graph": true}.
- **Planning binding:** v5 stale: ['docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md']. Coverage sources stale: ['query', 'report', 'workflows-and-surfaces'].

## Focused checks (verified overlay copy; failures preserved)

- `check-query-projection.v3`: exit 0, 52.2s, copy unchanged = True; 162 checks, 0 failed.
- `check_workflows.v1`: exit 0, 10.4s, copy unchanged = True; 1816 passed, 0 failed.
- `check-workflow-projection.v3`: exit 0, 97.5s, copy unchanged = True; 493 checks, 0 failed.
- `check_implementation_planning`: exit 1, 0.0s, copy unchanged = True; EXIT 1 (preserved): ValueError "Planning source changed: query" (stops at first stale binding).
- `check_repository_file_inventory`: exit 0, 0.0s, copy unchanged = True; PASS: 198 unique paths.

## Out of scope and retained

- **S37-01:** host finalizer: separate coauthor work, NOT closed here
- **A37-01..04:** carrier corrections: separate coauthor work, NOT closed here
- **grades:** 30 residual author grades remain PENDING
- **gates:** 32 product qualification gates remain unperformed
- **recovery:** 54 product recovery cases remain not executed

## Reads (exact hashes)

### Overlay files

- `docs/coop/design-corrections/workflows/check-query-projection.v3.py`: 2beb8a7d1a70507b → cfe85f887ccd4e4130f7977d5836755ae63eedb863a05e46e765da9070695b7a. Read: complete base-to-overlay unified diff (86 diff lines, +56/-0) plus changed-region context.
- `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py`: ce3cc3519353b9d6 → 4f356745f409b64ccf967070125c0ef6cc5fc64915975bc3a4298ccf08180821. Read: complete base-to-overlay unified diff (32 diff lines, +23/-0) plus changed-region context.
- `docs/coop/design-corrections/workflows/check_workflows.v1.py`: d1286edb50e0446e → 88edad11d904d1fabaf6bcd3bc41cd7f833a9944cdc9d1ec992b173453fde0a0. Read: complete base-to-overlay unified diff (16 diff lines, +7/-0) plus changed-region context.
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md`: 04a5e31179317ff6 → f7b2e7ca031d7605993446272328cccd51c665a2b3cb86e875fbdf2e135d93e7. Read: complete file.
- `docs/coop/design-corrections/workflows/query_projection_model.v3.py`: 0c7150b9b573459d → 0d4433aef51f7cace5e00c5329ea8520a3e9c42eeaf2545179d268bbfa344545. Read: complete base-to-overlay unified diff (18 diff lines, +8/-1) plus changed-region context.
- `docs/coop/design-corrections/workflows/schemas/common.schema.json`: 965474dc1b3697cb → f73094dd175c44f2ca474c654d00c4a9cc6eada823ca8bbdae7766f0bd2138fe. Read: complete base-to-overlay unified diff (226 diff lines, +170/-5) plus changed-region context.
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json`: 4a6e577545e9c877 → 36124787ace53c9b7e1ce1b98cf92ab914a03532a4adbec24710e95532e1bc27. Read: complete base-to-overlay unified diff (226 diff lines, +170/-5) plus changed-region context.
- `docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json`: ca1e2baed58df6dd → 33a43bd86ec7bcb18e5d4ac3d65f5543f57b7d22168a004edd4f1dad285febe9. Read: complete base-to-overlay unified diff (20 diff lines, +11/-0) plus changed-region context.
- `docs/coop/design-corrections/workflows/workflow-cases.v1.json`: 22b7443048ea5aef → f67d22f1a33588643b20b8f4001036d32c25b531741869b966a9e5c7d46d234e. Read: complete base-to-overlay unified diff (78 diff lines, +69/-0) plus changed-region context.
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md`: 666461f0c53dd871 → e207c8db06ff24ef53d709de741c3af6e5676ed1b1570ab41ec9fc3edcfd40e8. Read: complete base-to-overlay unified diff (51 diff lines, +18/-14) plus changed-region context.
- `docs/v2/architecture/prototype-report-inventory.md`: 3c9901d1071dae5a → 3f4d4dd2246a9dd373172267b0a40e9f4105b0bcd52625506c84412be379c3a0. Read: complete file.
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md`: b2530a314a7653eb → b71cdd6ee978fe3badae91a197fb663e4c7842413e6d827c97257624e7daeb2c. Read: complete base-to-overlay unified diff (14 diff lines, +4/-1) plus changed-region context.

### Context files

- `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` `5731b41d191d36f0b7c64ddbf46bcf0a66e93c302b8cfca854ec4dd0f4b311ab` (unchanged source37 byte (manifest-verified)): lines 1-90.
- `docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json` `b9a74548277c882a36bb30b412b994495dcd8f0141d67981cb57927c0660da3d` (unchanged source37 byte (manifest-verified)): complete-replay-mismatch condition/origin rows and x-opensip-routes (grep with context).
- `docs/coop/design-corrections/foundation/identity-schemas.v3.json` `099745ab0b9ea22b96b525e343e53c88a1a1953f4f79ad71f149e747371ba7f6` (unchanged source37 byte (manifest-verified)): $defs/availability (1641-1691); x-opensip-payload-registry (4692-4811); digest-domain records (grep).
- `docs/coop/design-corrections/public-detail-registry.v1.json` `39ec20cd9d1ead85ddbf9a21650765a4e3f45ae421efdd10a759f24fe012b580` (unchanged source37 byte (manifest-verified)): evidence.corrupt/missing/regeneration-mismatch and HOST.INVARIANT_VIOLATED records (grep).
- `docs/coop/artifacts/d9-exit-contract.v1.14.json` `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31` (unchanged source37 byte (manifest-verified)): hostTerminationUnion 824-953; codeVocabulary 954-982.
- `docs/coop/artifacts/resolved-inputs.v2.json` `0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43` (unchanged source37 byte (manifest-verified)): lines 220-259.
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` `b71cdd6ee978fe3badae91a197fb663e4c7842413e6d827c97257624e7daeb2c` (overlay): overlay §0 lines 54-72 and §9 lines 1134-1177.
- `docs/v2/architecture/implementation-normative-inputs.v5.json` `4b4b35b78192833027a26f0936c31c8b4523e228c03ccac7e1fc20d8ab0d091a` (unchanged source37 byte (manifest-verified)): complete (150 lines).
- `docs/v2/architecture/implementation-coverage.v1.json` `a818b71453ecf6c05f0ec8693036b99cd5d3672ba0af52d32dfacd707eaecd8f` (unchanged source37 byte (manifest-verified)): lines 1-72 (subject/sources).
- `docs/v2/architecture/implementation-planning-sources.v1.json` `b66a060bf260dae7b9d9ceeb10e7c3960236c5645b377043e491a42c371437e3` (unchanged source37 byte (manifest-verified)): lines 1-40, 225-244 and path/sha grep.
- `docs/coop/design-corrections/native/native_evidence_model.v2.py` `eba8628f02a0c49657aff61a7d0f5b713a602b585910bb7d7d4d69b09d9e3809` (unchanged source37 byte (manifest-verified)): public_termination_for 1038-1097.
- `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` `3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0` (unchanged source37 byte (manifest-verified)): StepTermination mentions (grep with context).
- `docs/coop/design-corrections/workflows/query_surface_projection.v3.py` `e23c3d0b1037603e5bab16998d0d4c02df4e022498325bc8d1c56b1cb9f804ec` (unchanged source37 byte (manifest-verified)): lines 85-114 and 260-354.
- `docs/coop/design-corrections/workflows/workflows_model.v1.py` `1d89bd285b77f0b3b8f852965320ed5447038196640a55b99b3c790752bdcdd3` (unchanged source37 byte (manifest-verified)): FAULT_TO_ERROR and terminate headers (grep).
- `docs/coop/design-corrections/workflows/command-inventory.v3.json` `c12ca4e8859d3815327490018e8db0a947d862a7c09e5cf9b2ae8db429b50d5b` (unchanged source37 byte (manifest-verified)): query-response parity field (grep).
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json` `36124787ace53c9b7e1ce1b98cf92ab914a03532a4adbec24710e95532e1bc27` (overlay): overlay StepTermination 738-1147.
- `docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json` `33a43bd86ec7bcb18e5d4ac3d65f5543f57b7d22168a004edd4f1dad285febe9` (overlay): overlay 1140-1205.
- `docs/coop/design-corrections/workflows/query_projection_model.v3.py` `0d4433aef51f7cace5e00c5329ea8520a3e9c42eeaf2545179d268bbfa344545` (overlay): overlay 1420-1464.
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` `e207c8db06ff24ef53d709de741c3af6e5676ed1b1570ab41ec9fc3edcfd40e8` (overlay): overlay 1-40, 195-206, 770-781, 1025-1099.

### Termination-boundary assessment

- `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/claude-source37-termination-boundary-assessment.v1/runtime-evidence/assessment.md` `7ad6095a73bdfe2d7d46e8d4a61f8ae3c80725be37cd918d29562ee93bd7087b`: complete (138 lines); public assessment only.

## Limitations

- Only the three changed owning checkers and the two planning checkers were run, individually. No group runner or global suite was run, and no pins were regenerated. The planning checker stops at its first failure.
- Overlay files were read as complete base-to-overlay diffs with changed-region context; the query contract and prototype inventory were read completely. Unchanged regions of large overlay files were not re-read, relying on the retained source37 complete-read record.
- The D9 legality predicate in P-SEM is this reviewer's transcription (faultCause only on operational-failed, reasonCodes only on indeterminate, operational pair = host fault map). Actual schema outcomes are recorded beside it.
- The exhaustive enumeration uses one reasonCode value, minimal required fields per class, and no runId/coverageId/executionId/domainDetail placement variants.
- The host-defect case monkeypatches close_run inside the probe process only, to show routing of a non-admission exception; it is not a product fault model.
- Producer coverage: native public_termination_for over every registered key/origin and the 24 evaluator fault routes. workflows_model.terminate and integration public_termination were covered only through the maintained checkers.
- Reference Python models over synthetic native-admitted inputs; no product implementation, compiler, provider or platform qualification.
- check_workflows.v1 reports only counts (1816 passed, 0 failed). Execution of its termination.fault-pairs-equal-host-fault-map control and the 12 new reject vectors is inferred from source reading (module-level check calls at lines 124-133) plus the empty failed list, not from named check ids. check-workflow-projection.v3 and check-query-projection.v3 report the new controls by id.
