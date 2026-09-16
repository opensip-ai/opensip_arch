# Independent design review: frozen source39

**Verdict: CHANGES_REQUIRED** (source level only; not blind reconstruction, application, readiness or product qualification).

Two SHOULD issues are unresolved, both in the policy test command: the facts verifier loses a known native hit when a required evidence kind is unavailable (S39-01), and admission does not apply the closed policy universe token map (S39-02). Both were measured by discriminating probes against the production composition owner. No MUST issue. ADV38-01/02/03 are closed at source level; ADV39-01 is a non-blocking native advisory. Subject, archive, members, parent38, delta, six pinned groups (all pass), 17 evaluator3 children, planning and inventory checks, package16 content agreement and eight reviewer probes ran to completion. Source-level result only.

## Subject

- Manifest `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json`: SHA-256 `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`; measured `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`; verifiedManifest=True.
- Archive `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-source.v39.tar.gz`: `5ae67eaacbe878a81c2a997b6b73480ecb846eeb4bf9110779f8e86b62a229ed` (measured equal: True); 12909 files, 737605070 bytes.
- Parent38 `2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5` unchanged and verified: True; delta {"changed": 67, "added": 5, "removed": 0}.
- The source38 review (ACCEPT) is preserved unchanged, and its acceptance is not inherited.

## Issues

No MUST issue.

### S39-01 (SHOULD): The policy-test facts verifier drops a known native hit when a required evidence kind is unavailable, so the authoring test reports a different gating outcome than production for the same facts

One gating rule `or(exists native hit, ...)` over src/a.ts declares a required import kind that the fixture lists as unavailable. Production composition (E.compose through the check-composition harness) returns rule outcome fail, verdict fail, 1 finding, root value true. The facts verifier returns verdict indeterminate, no finding, indeterminateRules [known-hit-rule]; the suite's finding expectation becomes indeterminate and its verdict=fail expectation unmet, so the suite outcome is failed. With the required kind available, or the kind optional, both agree on fail with the finding. With an `and` whose known conjunct is false, both agree on indeterminate. The disagreement is exactly the fail-dominance case the composition owner controls (a9). Consequence: a policy author's suite can report a production gate failure as indeterminate and unmet; section 5 promises the opposite.

- Required change: Evaluate the predicate for every selected subject even when a required kind is unavailable. Keep known true results as findings and gating failures (fail dominates). Mark only subjects without a known deciding value as unknown, with the missing-required cause retained. Add a policy-test control mirroring check-composition a9 (known hit plus missing required kind gives verdict fail with the finding).
- Owner: workflows policy test (policy_test_model.v3.py; check-workflow-projection pt2 controls)
- Selectors: `docs/coop/design-corrections/workflows/policy_test_model.v3.py:214-218 (evaluate: `if required - available` marks every selected subject unknown and `continue`s before any predicate is evaluated)`; `docs/v2/contracts/product-v1/workflows-and-surfaces.md:641-647 (facts cases are evaluated under the current atom law; unknown leaves an expectation indeterminate "unless a known finding decides it; known findings, strong Kleene and gating are unchanged")`; `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:34-36 (known matches are preserved despite incomplete coverage; deficiency provenance is retained when a known value dominates) and :319 (fail still dominates)`; `docs/coop/design-corrections/foundation/check-composition.v3.py:95 (a9-known-live-failure-dominates-missing-required-import) and check-replay.v3.py:210`; `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py oc2/pt2 policy-test controls (ranges 3540-3800 read): no control for a known hit under a missing required kind`
- Measured: `{"composition": {"verdict": "fail", "ruleOutcome": "fail", "findings": 1, "rootValue": "true"}, "fixture": {"outcome": "failed", "observedVerdict": "indeterminate", "findings": [], "indeterminateRules": ["known-hit-rule"], "expectationOutcomes": ["indeterminate", "unmet"]}, "controlsThatAgree": {"control-or-required-present-agrees": true, "control-or-optional-missing-agrees": true}, "andFalseRequiredMissing": {"composition": {"verdict": "indeterminate", "ruleOutcome": "indeterminate", "findings": 0, "rootValue": "false"}, "fixture": {"outcome": "indeterminate", "observedVerdict": "indeterminate", "findings": [], "indeterminateRules": ["known-hit-rule"], "expectationOutcomes": ["indeterminate", "met"]}}}`
- Receipt: `receipts/probes/policy-test.json#P1`

### S39-02 (SHOULD): policy test admits and evaluates candidate rule universe tokens that the evaluator3 profile refuses, including the authored suite's own typescript-v2

The authored suite uses typescript-v2, which is not in the profile token map, and PolicyTestSuiteV2 admission plus the resolver accept it (ADMITTED, resolverAccepted true, summary 5 passed / 0 failed / 3 indeterminate / 1 not-executable). Replacing the token with no-such-universe yields the same admission and the same summary; the registered token typescript yields the same summary too. So the universe token is neither admitted nor consulted by the facts verifier. Consequence: a candidate policy that analysis refuses at evaluator admission passes its authoring test with met expectations, and the checked-in reference suite exercises only a refused spelling.

- Required change: Admit every candidate rule universe through the same closed policyUniverseMap before evaluation, refusing an unknown token with a typed registered detail under the section 5 precedence. Change the authored suite to registered tokens, and add a negative control (typescript-v2 and an arbitrary token refuse) beside pt2.
- Owner: workflows policy test admission (workflows_model.v3.py policy.test profile; policy-test-cases.v3.json; check-workflow-projection pt2)
- Selectors: `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:26 (closed policy universe token map typescript/rust/syntax; "Unknown tokens refuse admission; historical illustrative tokens such as typescript-v2 are not additional implicit aliases")`; `docs/coop/design-corrections/foundation/evaluator_input_model.v3.py:16 (UNIVERSES from identity-schemas x-opensip-evaluator-profile.policyUniverseMap)`; `docs/v2/contracts/product-v1/workflows-and-surfaces.md:638-641 and 653-668 (facts cases under the current policy resolver and atom law; admission precedes evaluation)`; `docs/coop/design-corrections/workflows/policy-test-cases.v3.json:23, 63, 87, 122, 179, 226, 265, 308, 317, 355, 573, 608 (every authored universe is typescript-v2)`; `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py:3651 (pt2-current-candidate-resolver-admitted asserts the resolver accepts that suite)`
- Measured: `{"profileTokenMap": {"typescript": "native.semantic-universe.typescript.v2", "rust": "native.semantic-universe.rust.v2", "syntax": "native.semantic-universe.syntax.v2"}, "authoredTokens": ["typescript-v2"], "authoredSuite": {"route": ["ADMITTED", true, null], "tokensRegistered": {"typescript-v2": false}, "summary": {"passed": 5, "failed": 0, "indeterminate": 3, "notExecutable": 1}}, "noSuchUniverse": {"route": ["ADMITTED", true, null], "summary": {"passed": 5, "failed": 0, "indeterminate": 3, "notExecutable": 1}}, "registeredTokenControl": {"route": ["ADMITTED", true, null], "summary": {"passed": 5, "failed": 0, "indeterminate": 3, "notExecutable": 1}}}`
- Receipt: `receipts/probes/policy-test.json#P2`

### ADV39-01 (ADVISORY): The registered native payload schema document was edited in place, contrary to the native section 10 statement that its bytes are deliberately unchanged and that an edit is a schema-document successor

The document changed 3e37c7b7... to 2d37b810... under the same v2 name; the only JSON difference is one description string. The identity registry now registers only the source39 digest, the rebuild consumed that digest, and 17 of 17 package exports carry new RunIds. The new digest is propagated consistently and every executed suite passes, so nothing is inconsistent inside source39. But the section 10 sentence ("the annotation's bytes are deliberately unchanged ... editing ... is a schema-document successor with its own re-registration") no longer describes what was done, and a source38 payloadSchemaDigest is not resolvable against the source39 registry.

- Selectors: `docs/v2/contracts/product-v1/native-evidence.md:3093-3096`; `docs/coop/design-corrections/native/native-evidence.schemas.v2.json (only difference: #/$defs/ResolvedNodeModulesLayoutV1/description)`; `docs/coop/design-corrections/foundation/identity-model.v3.py registered_schema_documents()`; `root-author-package-final39-rebuild.v1/rebuild-report.json inputs.registeredNativeSchemaSha256`
- Receipt: `receipts/probes/schema-digest-effect.json`
- Disposition: ROUTE-TO-NATIVE-OWNER: either record this document revision (and the historical digest's standing) in section 10, or restore the registered bytes and carry the description in a successor. Non-blocking.

### Observations (not issues)

- Pruned-tree custody: one ResolvedNodeModulesLayoutV1 row with installPath node_modules authorizes reads of every top-level package ([]). A nested installed package still refuses. Security S3 (security-and-lifecycle.md:266-279) states which files were read is a host TCB observation, so this is within TCB-SCOPE-01.
- Exact-case segment rule: Node_Modules/a/index.js is not a pruned-tree read and stays first-party custody ([]). This is consistent with exact segment matching; a case-insensitive filesystem host must not fold it.
- U-9 fallback: when the only marker is in a custody-excluded directory, discovery yields the syntax-only fallback unit and its scope excludes that directory ({"refused": null, "units": [{"rootPath": "", "languageFamily": "none", "languageMode": "syntax-only", "unitKind": "syntax-only", "markerPath": "", "markerSha256": null, "recognizerId": "syntax-only-fallback", "recognizerVersion": 1, "provenance": "DEFAULTED", "memberPackageRoots": [], "unitOrdinal":). An explicit empty root list gives {"refused": null, "units": []}. Neither is claimed as a defect; U-9 names only "no language unit survives".
- A hidden candidates listing's suppressedCount mutated from 1 to 0 still projects ADMIT ({"originalSuppressedCount": 1, "mutatedTo": 0, "outcome": {"schemaValid": true, "projection": "ADMIT", "why": null}}): the count is not joinable from the query record alone, so it rests on the producing step.
- repair:2: a trusted retained view that declares KeyError as its UNAVAILABLE class gets KeyError mapped to REPAIR.EVIDENCE_RUN_UNAVAILABLE (["REFUSE", "REQUEST.PRECONDITION_FAILED", "REPAIR.EVIDENCE_RUN_UNAVAILABLE", 0]); a subclass of the declared class propagates. admit_repair_plan_v2 admits a reminted descriptor with applicable flipped ("ADMIT"): it is schema and identity admission, and semantic authority stays with the constructor and apply authorization. Both are inside TCB-SCOPE-01.
- PolicyTestSuiteV2 admission: a candidatePolicy with integer schemaMajor 1 but no schemaFamily routes CONFIG.INVALID rather than the major refusal (["REFUSED", "request-rejected", "CONFIG.INVALID", "CONFIG.INVALID"]). The x-opensip-admission-precedence text reads "a policy document candidatePolicy whose integer schemaMajor is not 2"; a family-less object is read as not a policy document. A one-line clarification would remove the ambiguity.
- Author checker hygiene: check-carrier-v3.py binds _S37_CF to the carrier_format INSERT and later rebinds the same global to carrier-format prose for a text check. The checker is correct in its own order, but reusing its publish helper after a full module run needs the SQL restored (done in P39-CARRIER-RO).
- identity-schemas.v3.json now names workflows/schemas/policy-document.v2.schema.json as the policy Predicate digest document (exists in source39: True).

## Item dispositions

### ADV38-01: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v38 (ADVISORY).

Delegated members now have a closed admission. The host observation {stepId, durability, attempts, commitReceipt, requiredClosureNotInstalled} is joined to the sealed Run, receipt, inventory, plan and stage; the detail is admitted only from the ordered allowlist (WORK_BUDGET, then REQUIRED_CLOSURE_NOT_INSTALLED, then the native entry deficiency of the coverageId carrier). An unrelated registered detail, a reminted receipt and mismatched joins refuse in P39-TERM7.

Owner selectors:
- `docs/coop/design-corrections/foundation/run-termination-contract.v1.md:205-342 (section 7 host composition of the whole analysis StepTermination; detail allowlist row 2 at :298)`
- `docs/coop/design-corrections/foundation/run_termination_model.v1.py:299 (CLOSURE_DETAIL), :374 (admit_analysis_step_termination)`

### ADV38-02: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v38 (ADVISORY).

The unmigrated-carrier association route is now machine-mapped, and a bound carrier observed absent is custody (host-io), never not-committed. Every one of the 99 reviewer-tabulated scenarios matched the owner dispatch, no read-only open changed a schema object, and every reached public projection is a valid StepTermination. The reference model has no stability observation, so quarantine standings assume stable observations.

Owner selectors:
- `docs/coop/design-corrections/security/carrier-dispatch.v3.json:684-693 (readOnlyStandingOfDispatchResult: carrierFormat1/2 -> unknown-carrier-incompatible; fresh-install -> unknown-custody)`
- `docs/v2/architecture/commit-recovery-readonly.v3.md section 1 (precedence rows 1-4)`
- `docs/coop/design-corrections/security/carrier-format.v3.md section 8.1`
- `docs/v2/contracts/product-v1/security-and-lifecycle.md:1315-1316 (bound carrier observed absent; association naming an unmigrated carrier)`

### ADV38-03: CLOSED-AT-SOURCE-LEVEL

Origin: claude-independent-design.v38 (EDITORIAL).

Measured on whitespace-normalized text: source38 carried the unqualified F00-F37 sentence and the store-transition-only scope; source39 carries neither, and instead states the F00-F53 plan and cites the security S12 scope. The read-only conclusion is unchanged and now agrees with S12.

Owner selectors:
- `docs/v2/architecture/commit-recovery-readonly.v3.md:39-40 (F00-F37 now qualified as the range when the document was authored; the current plan holds F00-F53)`
- `commit-recovery-readonly.v3.md:74-75 (the MIGRATION.CORRUPT scope now cites security S12)`
- `commit-recovery-readonly.v3.md:30, 121 (not used on a read-only path)`
- `docs/v2/contracts/product-v1/security-and-lifecycle.md:1319 (MIGRATION.CORRUPT: store transition footprint and carrierFormat 3 migration footprint at a writer or maintenance open)`

### ROOT39-FOUNDATION-DETAIL-CENSUS: CONFIRMED

Origin: root-foundation-detail-census-correction.v1.

The three root v1 failures were stale census assertions. The correction names exactly the four new workflow details, keeps the historical substrate closed, and does not absorb arbitrary future additions. The registry diff adds exactly those four codes and removes none.

Owner selectors:
- `docs/coop/design-corrections/foundation/check-identity.py (_WORKFLOW3_PUBLIC_DETAILS; historical 289-code substrate kept closed)`
- `docs/coop/design-corrections/public-detail-registry.v1.json (four workflow rows added)`

### ROOT39-FINAL-REFERENCE: V1-PRESERVED-AS-FAILURE; V2-IS-THE-ONLY-CURRENT-ALL-PASS-RECEIPT; THIS-REVIEW-RE-EXECUTED

Origin: root-source39-final-reference.v1 and .v2.

v1 stays a failure (foundation exit 1; check-identity 1593 passed, 3 failed), and nothing relabels it. v2 is evidence only; this review's own six pinned groups on the verified copy are the acceptance input.

Owner selectors:
- `root-source39-final-reference.v1/reference-checks.json`
- `root-source39-final-reference.v2/reference-checks.json`

### TOPIC-POLICY-TEST: CHANGES-REQUIRED (S39-01, S39-02); remainder confirmed

Origin: source39 charter.

Confirmed independently: the admission precedence (suite major, candidate major, imperative key via the grammar, other schema failures CONFIG.INVALID, then resolver refusals with the resolver detail) over 25 routes; suiteDigest = H("workflow.policy-test-suite", suite), not the raw bytes; result id policytest2 = H over the result without its id; candidate digest over raw bytes; same suite, same result bytes. Strong Kleene in the verifier matches composition for and/or/not when evidence is available (P1 controls). Not confirmed: known-hit dominance under a missing required kind (S39-01) and universe-token admission (S39-02). argvDigest (workflows-and-surfaces.md:1056-1062; security S10 now defines it identically) was checked by reading and by the executed author control, not by an independent probe.

Owner selectors:
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:631-668`
- `docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json`
- `docs/coop/design-corrections/workflows/policy_test_model.v3.py`
- `docs/coop/design-corrections/workflows/workflows_model.v3.py:181-311`

### TOPIC-QUERY-CARRIERS: CONFIRMED-INDEPENDENTLY

Origin: source39 charter.

Exactly nine commands dispatch through query carriers; the query command exposes the 20 public graph-query-3 operations, 17 of them non-graph, with graph-query-3 bytes unchanged from source38; host-only operations are not public. Each command's parity paths equal its parity fields. Cross-kind envelopes, failure envelopes with carriers, graph selectors over records and wrong exits refuse. Reminted join negatives refuse. DELIVERY.REQUIRED_PROJECTION_FAILED is valid only without runId, and RENDERER_FAILED_AFTER_COMMIT only with runId.

Owner selectors:
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:1130-1139, 1208-1243, 1371-1372`
- `docs/coop/design-corrections/workflows/query_surface_projection.v3.py:310-388`
- `docs/coop/design-corrections/workflows/command-inventory.v3.json`
- `docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json and invocation-record.schema.json (delta read)`

### TOPIC-REPAIR2: CONFIRMED-INDEPENDENTLY (observations only)

Origin: source39 charter.

Authority refuses first, then a missing retained closure, then a non-run3 id, then Plan and exact run identity joins, then target correspondence, each before any descriptor is built. Only the exact declared unavailability class maps typed. The owner plan is repair:2 and admits; a major-1 descriptor refuses typed.

Owner selectors:
- `docs/coop/design-corrections/workflows/workflows_model.v3.py:119-179`
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:714`
- `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:37`
- `docs/coop/design-corrections/workflows/workflows_model.v1.py (historical constructor keeps keyword-only descriptor_major=1)`

### TOPIC-COMPARISON-PRESENCE-KNOWLEDGE: CONFIRMED-AT-HELPER-LEVEL

Origin: source39 charter.

Presence knowledge is true only for a baseline entry, false only for non-selection or complete-hit-set without a same-rule same-path barrier, and otherwise null, never coerced to false. First attribution unknown selects the baseline first. Full-Run comparison controls are the author's executed child, not an independent reconstruction.

Owner selectors:
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md:382-400 (evaluated absence; same-rule/same-path barrier; B absence only under RuleCoverage.absenceKnowledge complete-hit-set; INDETERMINATE current/baseline-absence-unknown), :402-411 (closed indeterminate reason order)`
- `docs/coop/design-corrections/workflows/workflow_projection_model.v3.py (delta read)`
- `docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json (delta read)`

### TOPIC-NATIVE-IDENTITY: CONFIRMED-WITH-ADVISORY (ADV39-01)

Origin: source39 charter.

VCS trees refuse at any depth; a nested installed package needs its own row; a store realPath authorizes its own files; first-party Cargo output is never a read. The syntax-only fallback appears only when no language unit survives, its default selection is the complete syntax-only product at root, and zero units refuse NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT. Stage-output schema registration, the normalization map and body eligibility were read (diff and contract) and exercised by the executed consumer24 child, not independently probed.

Owner selectors:
- `docs/v2/contracts/product-v1/native-evidence.md:782 (U-4b ENUMERATION_MEMBERSHIP_ORDER), :851 (U-9 zero-config syntax-only fallback), :749 and :778 (U-9 in discovery and membership), :877 (NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT)`
- `docs/coop/design-corrections/foundation/identity-model.v3.py:124 (FOUNDATION_DIGEST_UNANNOTATED), :683 (snapshot_pruned_tree_faults)`
- `docs/coop/design-corrections/foundation/identity-schemas.v3.json (normalizationSpecificationLaw, bodyEligibilityLaw, stage-output registeredBy law)`
- `docs/v2/contracts/product-v1/security-and-lifecycle.md:266-279 (A-5 pruned trees and the read set), :288-299 (U-9 counterpart in the admitted boundary inventory)`

### TOPIC-TERMINATION-IMPORT-EVALUATOR-NATIVE-BRIDGES: CONFIRMED (termination independently; import/evaluator/native by read and executed controls)

Origin: source39 charter.

The bridges join through one owner each. No independent import-bridge probe was run; that is a limitation, not a finding.

Owner selectors:
- `run-termination-contract.v1.md section 7`
- `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md (read complete; account targetUniverse typed null; body-eligible census)`
- `evaluator-composition-contract.v3.md (read complete)`

### TOPIC-V7-PLANNING: CONFIRMED (newly bound selectors partly line-read)

Origin: source39 charter.

v7 binds 31 inputs with no mismatch and no self-binding; coverage and planning sources name v7; the mapping population is preserved and the checker passes. The coverage diff was line-read for its first 260 of 1014 lines (source rebinding and golden selector shifts); the rest rests on the executed checker.

Owner selectors:
- `docs/v2/architecture/implementation-normative-inputs.v7.json (read complete)`
- `docs/v2/architecture/implementation-coverage.v1.json`
- `docs/v2/architecture/implementation-planning-sources.v1.json`

### TOPIC-PACKAGE16: VERIFIED-AS-AUTHOR-EVIDENCE (reconstructed, not relabelled)

Origin: source39 charter.

See packageAssessment. The formal manifest and the files-only projection are different objects with equal file lists. The package was rebuilt from package15 plus the migration overlay against source39, and the exports and membership probes agree in content, not only in a passed flag.

Owner selectors:
- `/tmp/opensip-design-corrections/claude-author-package-successor.v16/artifact-manifest.json`
- `/tmp/opensip-design-corrections/claude-author-package-successor.v16/source-binding.v39.json`
- `/tmp/opensip-design-corrections/root-author-package-final39-rebuild.v1/rebuild-report.json`

## Probes and command receipts

- **P39-SUBJECT** `probes/verify_subject.py`: Formal manifest f71a5992... and snapshot verified member by member (12,909 members, hash and length); parent38 manifest and snapshot re-verified; 38->39 delta measured (67 changed, 5 added, 0 removed). Receipts: `receipts/subject-verification.json`, `receipts/manifest39-index.json`
- **P39-ARCHIVE** `probes/verify_archive_extract.py`: Archive 5ae67eaa... hashed; every member extracted into two disposable copies and compared by hash and length; no extra, duplicate or non-regular members. Receipts: `receipts/archive-verification.source39-pkg.json`, `receipts/archive-verification.source39.json`
- **P39-DELTA** `probes/make_delta_diffs.py`: Unified 38->39 diffs for all 72 delta files (reading aid; a diff is not a whole-file read). Receipts: `receipts/delta-diff-summary.json`, `receipts/delta-diffs/`
- **P39-GROUPS** `probes/run_reference_groups.py`: Six pinned reference groups with /tmp/opensip-architecture-review-env/bin/python -I -B on a verified disposable exact copy, re-verified before and after. Receipts: `receipts/reference/groups-report.all.json`
- **P39-PLAN** `probes/run_planning_checks.py`: check_implementation_planning --check and check_repository_file_inventory --check on the exact copy plus independent v7/coverage/planning-source binding counts. Receipts: `receipts/planning-checks.json`
- **P39-PKG** `claude-author-package-successor.v16/verify-package.py and probe-native-v2.py (author tools, run by probes/run_env.py on this review's verified copy)`: Package16 7 groups (17 exports across 6 Run/control groups plus 7 queries) and 9 native-v2 membership probes re-executed against source39 and compared in content with the root receipts. Receipts: `receipts/runs/package-v16-verify.run.json`, `receipts/runs/package-v16-probe-native-v2.run.json`
- **P39-POLICY** `probes/probe_policy_test.py`: P1 fixture verifier versus production composition over the same facts (known native hit; required/optional evidence present/missing; or/and); P2 universe tokens; P3 25 PolicyTestSuiteV2 admission routes; P4 identity preimages recomputed with the reviewer's own C() and H(). Result: {"rows": 50, "failed": ["known-native-hit-under-missing-required-evidence-agrees-with-composition"], "observations": ["observation-candidate-major-1-without-family"]} Receipts: `receipts/probes/policy-test.json`
- **P39-TERM7** `probes/probe_run_termination_s7.py`: run-termination-contract section 7 host composition admission over golden Runs with receipts minted by the evidence store: detail allowlist order, receipt/inventory/plan/stage joins and reminted negatives. Result: {"rows": 24, "failed": [], "observations": ["observation-extra-member", "observation-missing-member", "observation-cannot-bless-a-non-derived-projection"]} Receipts: `receipts/probes/run-termination-s7.json`
- **P39-QUERY** `probes/probe_query_carriers.py`: Nine query-dispatch commands, 20 public graph-query-3 operations, 17 non-graph operations, host-only operations, per-command lawful controls plus four cross-kind/exit negatives, reminted join negatives and the delivery failure laws. Result: {"rows": 98, "failed": [], "observations": ["observation-hidden-listing-suppressedCount-is-not-joinable-from-the-record"]} Receipts: `receipts/probes/query-carriers.json`
- **P39-CARRIER-RO** `probes/probe_carrier_readonly.py`: 11 real in-memory SQLite carriers x 3 associations x 3 witnesses against the reviewer's own table of commit-recovery-readonly section 1 precedence; schema objects unchanged; public projections schema-valid. Result: {"rows": 108, "failed": [], "observations": []} Receipts: `receipts/probes/carrier-readonly.json`
- **P39-SCHEMA-DIGEST** `probes/probe_schema_digest_effect.py`: Registry effect of the in-place native-evidence.schemas.v2.json edit (JSON difference paths; source38/39 digests registered or not). Receipts: `receipts/probes/schema-digest-effect.json`
- **P39-NATIVE-CUSTODY** `probes/probe_native_custody_fallback.py`: Helper-level identity section 3 pruned-tree read custody and native U-9 syntax-only fallback boundaries (owner functions, not full Runs). Result: {"rows": 20, "failed": [], "observations": ["observation-a-single-broad-installPath-row-authorizes-every-top-level-package", "observation-a-file-at-the-listed-directory-path-itself-is-not-authorized", "observation-exact-case-segment-rule-leaves-a-case-variant-directory-in-first-party-custody", "observation-only-marker-in-a-custody-excluded-directory-yields-the-fallback", "observation-explicit-roots-empty-explicit-root-list", "observation-explicit-roots-explicit-dot-root"]} Receipts: `receipts/probes/native-custody-fallback.json`
- **P39-COMPARISON** `probes/probe_comparison_knowledge.py`: Pure-function presence-knowledge helpers (first attribution unknown, correspondence barrier, selection exclusion, baseline presence knowledge, fingerprint absence). Result: {"rows": 28, "failed": [], "observations": []} Receipts: `receipts/probes/comparison-knowledge.json`
- **P39-REPAIR2** `probes/probe_repair2.py`: repair:2 constructor over the owner checker's close_run-admitted Runs with a spied shared builder: refusal order before any descriptor, exact-class unavailability mapping (subclass propagates), plan admission and major-1 refusal. Result: {"rows": 16, "failed": [], "observations": ["observation-a-trusted-view-declaring-a-builtin-class-maps-that-exact-class", "observation-admit-repair-plan-v2-is-schema-and-identity-admission-not-semantic-rederivation"]} Receipts: `receipts/probes/repair2.json`

Reference groups (reference interpreter `-I -B`, verified disposable copy):

| Group | Exit | Seconds | Script matches manifest | Copy unchanged |
|---|---|---|---|---|
| evaluator3 | 0 | 456.2 | True | True |
| foundation | 0 | 127.2 | True | True |
| integration | 0 | 16.2 | True | True |
| native | 0 | 2.9 | True | True |
| security | 0 | 0.9 | True | True |
| workflows | 0 | 9.5 | True | True |

Evaluator3 children (all exit 0: True): current-profile {"exitCode": 0, "passed": true, "count": 38, "checksCount": 38}, enumeration {"exitCode": 0, "casesCount": 44, "mismatchesCount": 0}, atoms {"exitCode": 0, "passed": 101}, execution-inputs {"exitCode": 0, "casesCount": 76, "mismatchesCount": 0}, composition {"exitCode": 0, "passed": true, "count": 30}, full-replay {"exitCode": 0, "passed": true, "count": 73, "checksCount": 73}, native-replay {"exitCode": 0, "passed": true, "count": 31, "checksCount": 31}, execution-replay {"exitCode": 0, "passed": true, "count": 8, "checksCount": 8}, candidate-replay {"exitCode": 0, "passed": true, "count": 4, "checksCount": 4}, policy-derivation {"exitCode": 0, "passed": true, "count": 6, "checksCount": 6}, faults {"exitCode": 0, "passed": true, "count": 41, "checksCount": 41}, provider-attribution-return {"exitCode": 0, "passed": 47}, workflow-projection {"exitCode": 0, "passed": true, "count": 838, "failedCount": 0}, query-projection {"exitCode": 0, "passed": true, "count": 204, "failedCount": 0, "checksCount": 204}, comparison-knowledge {"exitCode": 0, "passed": true, "count": 1}, analysis-seal {"exitCode": 0, "passed": true, "casesCount": 16}, native-consumer24-corrections {"exitCode": 0, "passed": 183, "total": 183, "failedCount": 0}

Planning: `PASS: 322 source-bound mappings, 54 planned failure cases, private schema, owners and generated plan`; inventory: `PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches`; v7 `8543d29f7047b7228f98eef12b2ae1f2d5738ec7447c8cd9605b259da029900f`, 31 inputs, mappings 322 (source38 320).

Root reference: v1 passed=False ({"passed": 1593, "failed": 3, "productQualification": false}; failures ["retained-scope-details-and-explicit-evaluator3-additions-are-closed", "retained-four-native-route-details-remain-named-with-current-evaluator-additions", "scope-boundary-still-reuses-existing-public-detail-with-current-evaluator-additions"]) stays a failure; v2 passed=True is the only current all-pass root receipt and is evidence only.

## Package16

- Artifact manifest `a88697c1bb82b4f4ad9abf05b22f01f3a0ddfd53fdbfa4b7dd6bfbbdb9ea2f6e` (expected equal: True); 387 files listed, mismatched 0, unlisted 0.
- Formal manifest versus files-only projection: `{"formalManifestSha256": "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009", "artifactManifestFormalSubject": "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009", "artifactManifestFilesOnlySource": "2c1c779f812ba17e4f7f7a1939dfcff453ebf1c0301f68692f1337602ed48a64", "formalSourceManifestCopySha256": "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009", "packageSourceManifestSha256": "2c1c779f812ba17e4f7f7a1939dfcff453ebf1c0301f68692f1337602ed48a64", "packageSourceManifestFilesEqualFormalFiles": true, "formalFileCount": 12909, "formalAndFilesOnlyAreDifferentObjects": true, "bindingProjectionEqualsFormalFiles": true}`.
- Reconstruction: `{"rebuildReport": "/tmp/opensip-design-corrections/root-author-package-final39-rebuild.v1/rebuild-report.json", "sha256": "b5a7824455a4625cab50c64d1818699fbba1aea73f12eba5be8ebfecd8c10009", "equalsBindingRebuildReportSha256": true, "script": "/private/tmp/opensip-design-corrections/claude-author-package-migration.v1/overlay/rebuild-author-package.v2.py", "scriptSha256": "53f75a074487fe9f01c16764c941ed4ac629a0aad0a9abe91f96a80f406a993c", "rebuiltPackageBeforeMetadataBinding": "0842174fc124de225ccaf04ca8e1999a94c9eb53096e4701547d4de17a057f20", "equalsArtifactPredecessor": true, "overlayManifestSha256Measured": "07c3185f0fca2d191fda26e584293b409ca43a9f081ad620e906388f5e36e7a1", "overlayManifestInPackageSha256": "07c3185f0fca2d191fda26e584293b409ca43a9f081ad620e906388f5e36e7a1", "overlayFilesByteEqualInPackage": 10, "overlayFilesNotEqualInPackage": ["README.md", "verify-package.py"], "overlayDifferencesExplained": {"verify-package.py: only the __SOURCE_MANIFEST_SHA256__ placeholder is instantiated with the files-only projection sha": true, "README.md: the package README is a formal-binding header followed by the overlay README": true}, "preFormalBindingCopies": {"readmeSha256": "205f7aada9190e4d72259310e6444834ae0fcb665a3e01cb5ed092c8d2f96e63", "artifactManifestSha256": "0842174fc124de225ccaf04ca8e1999a94c9eb53096e4701547d4de17a057f20", "readmeEqualsOverlayReadme": true, "artifactManifestEqualsRebuiltPackage": true}, "exportComparisonRows": 17, "exportsWithNewRunId": 17, "exportsWithNewBytes": 17, "exportsMarkedNew": 4, "exportBytesFoundInPackage": 17}`.
- Verification: `{"mineSha256": "b5a3fe83b3aeb12771df0de12cf866560037bb94bab9d5339f0cdb04b89dc55b", "rootSha256": "b5a3fe83b3aeb12771df0de12cf866560037bb94bab9d5339f0cdb04b89dc55b", "contentEqualToRoot": true, "passed": true, "groupCounts": {"checkpoint3": 1, "normalized-examples6": 4, "rust-selection-examples1": 2, "semantic-controls1": 3, "binding-controls": 3, "normalization-map-controls1": 4, "query": 7}, "exportCount": 17, "queryCount": 7, "filesComparedWithRootVerificationDirectory": 55, "filesDifferingInContent": [], "exactInputStoresCompared": 17}`; native probe `{"mineSha256": "e7e0ad1da71e45850ca235071e903472509411a7bfb0cbb29ceed565e7e9bc40", "contentEqualToRootRebuildProbe": true, "runs": 9, "passed": true, "unitsVsDiscoveryDisagreements": []}`.
- All 7 verifier groups (17 exports: checkpoint3 1, normalized-examples6 4, rust-selection-examples1 2, semantic-controls1 3, binding-controls 3, normalization-map-controls1 4; plus 7 queries) passed on this review's verified copy. The verification and every compared output file are content-equal to the root run, and the 9 native-v2 membership probes are content-equal to the root rebuild probe.
- Author construction and self-consistency evidence; the verifier and native probe are author tools re-executed here, not an independent reconstruction.
- Reconstructed by root from package15 plus the migration overlay against source39. That is a rebuild, not a relabel: 17 of 17 exports carry new RunIds.
- Preserved package limitations: the TypeScript checkpoint compares a partial consumer helper with the owner; owner-derived positives are self-consistency; the helper leaves and/or/not unexercised and count-at-most/all-covered unimplemented; two-binding construction is incomplete with a single explicit binding.
- No compiler, provider, OS or process-isolation qualification; independent grades granted: 0.

## TCB-SCOPE-01 (one shared assumption, 13 dependent rows)

Assumption: Selected authenticated in-process host/evaluator code is trusted; adversarial code sharing that process is outside this product threat model. Untrusted inputs are inert typed data and provider process boundaries still require real qualification.

- It stays coherent as a scope selection on source39. Admission section 5 (no untrusted native/WASM, no imperative contributions or project hooks) is byte-identical 38->39: True. prototype-report-inventory still admits no executable report hooks: True.
- The new in-process trust surfaces are consistent with the assumption and are stated as trust. The repair:2 retained view is a trusted host adapter whose declared class is authority, and it maps even KeyError (P39-REPAIR2). The section 7 termination admission takes host validate callbacks. Pruned-tree read custody names which files were read as a host TCB observation (security S3), and one broad installPath row authorizes every top-level package (P39-NATIVE-CUSTODY).
- Untrusted inputs remain inert typed data. PolicyTestSuiteV2 refuses imperative keys and string expressions through the grammar (P39-POLICY P3). Query carriers refuse cross-kind and failure envelopes (P39-QUERY). Read-only carrier opens refuse without changing a schema object in all 99 scenarios (P39-CARRIER-RO).
- S39-01 and S39-02 are fidelity defects of the reference authoring-test verifier and admission. Neither is a trust-boundary violation, and neither changes the assumption.
- It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries, and all 32 gates are unperformed (qualified=true count 0).

Reviewer position: NOT REJECTED. Consequence: Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING. Adjudication owner: The separate final application review, by a NEW other actual Claude origin that is not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin; not adjudicated here.

Dependent rows: RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c.

## Disposition rows (107)

### F

- **F-01** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-01: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-02** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-02: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-03** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-03: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-04** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-04: identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-05** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-05: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-06** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-06: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-07** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-07: identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-08** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-08: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-09** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-09: identifier and prior root standing INHERITED recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-10** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-10: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-11** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-11: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-12** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-12: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-13** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-13: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.
- **F-14** CARRIED-NOT-REGRADED (inherited-unchanged-38; prior38 CARRIED-NOT-REGRADED): F-14: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 recorded from root-independent36-completion-assessment.v1. The F content lives outside the snapshot, is not re-derived, and no 38->39 delta file is an F record. The prior standing is not source39 acceptance.

### Evaluation residuals

- **RES-EP13-01** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Plan and derivation joins are still recomputed inside complete replay; source39 adds golden Runs (check-semantic-replay.v3 +138) that the full-replay and candidate-replay children use, and P39-TERM7 refuses a reminted receipt and mismatched plan/stage joins against those Runs. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-02** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The source39 section 7 termination admission takes validate_shape/validate_attempt/validate_receipt from the host, so no answer-provenance claim against adversarial in-process regions is made. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-03** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: The seven-vector measurement stays finite history; admission-and-qualification.md and the residual ledger are byte-identical 38->39. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-04** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Closed input schemas remain the product admission; PolicyTestSuiteV2 refuses imperative keys and string expressions through the grammar (P39-POLICY P3), with the S39-02 universe-token gap recorded separately. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-05** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: The frozen subject was verified outside every author instrument: formal manifest, archive, 12,909 members and parent38 (P39-SUBJECT, P39-ARCHIVE). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-06** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: canonical.py is outside the delta. The reviewer's own C()/H() reproduced the owner canonical bytes (6,459 bytes) and the policy-test digests (P39-POLICY P4). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-07** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Seal and replay owners (security_lifecycle_model_v1.py, evaluator_replay_model.v3.py) are outside the delta; the analysis-seal child re-executed and passed on source39. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-08** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Bounded historical measurement; source39 claims no product proof over all PlanIntents. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-09** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Provenance stays distinct from correctness: package semantic-controls1 still has owner ADMIT and semantic REFUSE on source39 (content-equal to the root receipt), and admit_repair_plan_v2 admits a reminted flipped descriptor by identity alone (P39-REPAIR2 observation). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-10** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Author self-counters did not decide this review. The author control pt2 asserts that the typescript-v2 suite is accepted, and no author control covers S39-01; both SHOULDs came from independent discriminating probes. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-11** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Historical failures stay recorded by cause: root-source39-final-reference.v1 (3 stale census assertions) stays a failure; v2 is the only all-pass receipt and is evidence only. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-12** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The repair:2 retained view's declared class is authority by trust, not containment (P39-REPAIR2); no sole Python guard enters product authority. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-13** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. This review's probes deep-copy fixtures, restore the spied builder and the checker's _S37_CF global, and verify the copy after each run (fixture isolation only). The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-14** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: The differential census is not used as an oracle; unchanged. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-15** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: The C-2 v4 self-census is not elevated. The enumeration-plan schema change (membership order law, +7/-5) was diff-read and is exercised by the enumeration child, not by a census. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-16** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Producer flags still cannot bypass replay; the section 7 admission derives class and reasons from the sealed Run, not from the host candidate. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-17** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Text-only disclosures remain text-only. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-18** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Pruned-tree read custody relies on a host observation of which files a context read (security S3), stated as a TCB observation. The historical limitation is preserved; no historical guard is claimed repaired.
- **RES-EP13-19** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Substantive semantic review on source39 with discriminating probes; pins and passing counts were not treated as acceptance, and two SHOULDs were found despite all six groups passing. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-01** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. Each executed probe ran in-process with owner modules; containment is not claimed. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-02** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: No name or punctuation scan decides scope: repair:2 matches unavailability by exact class identity (a subclass propagates, P39-REPAIR2), and the census correction names four codes explicitly instead of matching a prefix. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-03** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. A trusted view can declare any exception class, even KeyError, as its unavailability class, and it maps. That is exactly why the boundary is trust rather than containment. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-04** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01; one TCB account is used for all thirteen rows. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-05** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Contradictory prose still needs substantive review: S39-01 is a section 5 sentence contradicted by the fixture, and ADV39-01 a section 10 sentence contradicted by the bytes. Neither was caught by a passing suite. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-06** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: Historical attacker cost preserved as history. The historical limitation is preserved; no historical guard is claimed repaired.
- **IR-EP13-NB-07** ASSESSED-CONSISTENT-GRADE-PENDING (inherited-unchanged-38; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING]: The original environment is preserved; this review names its interpreter (-I -B) and pins. The historical limitation is preserved; no historical guard is claimed repaired.
- **AX6** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The AX6 escape (evaluation-proof.v13) stays history; no 38->39 delta file claims same-process route-region protection, and replayed comparison remains reproducibility. The historical limitation is preserved; no historical guard is claimed repaired.
- **AX9** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The AX9 escape stays history; the source39 additions (section 7 admission, repair:2 view) are typed data admission under a trusted evaluator, the correction's stated boundary. The historical limitation is preserved; no historical guard is claimed repaired.
- **MD5** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The MD5 escape stays history; source39 adds no Python-containment mechanism and none enters product authority. The historical limitation is preserved; no historical guard is claimed repaired.
- **RX2c** ASSESSED-CONSISTENT-GRADE-PENDING (new-39; prior38 ASSESSED-CONSISTENT-GRADE-PENDING) [author grade PENDING] [depends on TCB-SCOPE-01]: Depends on TCB-SCOPE-01. The RX2c escape stays history; complete replay and the new golden Runs are reproducibility evidence, not containment. The historical limitation is preserved; no historical guard is claimed repaired.

### AR

- **AR-01** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Admission section 1 is byte-identical. The StepTermination law gains the delivery branches (common.schema +75, delta read), and P39-QUERY confirmed both runId directions.
- **AR-02** NO-NEW-ISSUE (inherited-unchanged-38; prior38 NO-NEW-ISSUE): Admission sections 2-4 and qualification-gates are byte-identical 38->39; all 32 gates stay unperformed.
- **AR-03** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Security S3 was re-read complete and its A-5 pruned-tree paragraph is new. P39-NATIVE-CUSTODY confirmed VCS refusal at any depth and nested-package rows; the broad-row observation is a stated host TCB observation.
- **AR-04** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Security re-read complete on source39; the 38->39 diff (read) does not touch trust time. No probe.
- **AR-05** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Security re-read complete on source39; the 38->39 diff (read) does not touch root chain or revocation. No probe.
- **AR-06** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): The platform admission text and carrier DDL are unchanged (grant-journal.carrier.v3.sql outside the delta); the security group passes.
- **AR-07** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Native re-read complete. U-4b membership order and the allowJs derivation were read and exercised by the executed consumer24 child; the native group passes 380/380.
- **AR-08** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): The repair:2 constructor is new and confirmed by P39-REPAIR2 16/16. argvDigest is defined once (workflows-and-surfaces.md:1056-1062), and security S10 restates it with a cross-reference (security-and-lifecycle.md:1074).
- **AR-09** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): identity-and-evidence.md changed (+114) and was re-read complete: stage-output registration, normalization map, body eligibility, foundation digest law, program predicate node. The foundation group passes; only pruned-tree custody was independently probed.
- **AR-10** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Presence knowledge is new; P39-COMPARISON 28/28 at helper level, and the comparison-knowledge child passes.
- **AR-11** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): The import bridge types account targetUniverse null (execution-inputs contract read complete; schema diff read); the execution-inputs child passes. No independent import probe.
- **AR-12** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): Native section 4 atom semantics are unchanged in substance; the atoms child passes. The policy-test verifier's divergence from the atom law under missing required evidence is S39-01, owned by workflows section 5.
- **AR-13** NO-NEW-ISSUE (new-39; prior38 NO-NEW-ISSUE): The U-9 syntax-only fallback and its security S3 counterpart were probed (P39-NATIVE-CUSTODY); observations only.
- **AR-14** NO-NEW-ISSUE (new-39; prior38 ADVISORY-ONLY): ADV38-02 and ADV38-03 are closed at source level (P39-CARRIER-RO; commit-recovery-readonly text measured).
- **AR-15** NO-NEW-ISSUE (inherited-unchanged-38; prior38 NO-NEW-ISSUE): The contract index README is byte-identical 38->39.
- **AR-16** CHANGES-REQUIRED (S39-01, S39-02) (new-39; prior38 ADVISORY-ONLY): ADV38-01 is closed by run-termination section 7 and the command carriers are confirmed. The policy test command has two SHOULD issues in its facts verifier and admission.

### FW

- **FW-01** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): discovery.rs must implement the security S3 pruned-tree read-set join and U-9 fallback; the source39 laws are confirmed at helper level (P39-NATIVE-CUSTODY). The observations on broad rows and case-variant segments are host obligations. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-02** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): review.rs carries the review-brief command through query carriers; P39-QUERY confirmed the lawful control, truncated variant and another-run refusal. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-03** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): analysis.rs hands the host observation to run-termination section 7; P39-TERM7 confirmed the admission order and joins. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-04** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): imports.rs implements the typed-null targetUniverse account; confirmed by read and the execution-inputs child only. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-05** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): comparison.rs implements presence knowledge true/false/null; confirmed at helper level (P39-COMPARISON). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-06** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): finalization.rs projects the delivery laws (REQUIRED_PROJECTION_FAILED without runId, RENDERER_FAILED_AFTER_COMMIT with runId), confirmed by P39-QUERY. The ADV38-01 obligation is now a closed section 7 admission. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-07** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): invocation.rs computes argvDigest over C(argv) (workflows section 7, security S10); read-confirmed and covered by an executed author control, not independently probed. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-08** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): outcomes.rs implements the section 7 detail allowlist order; P39-TERM7 confirmed that unrelated registered details refuse. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-09** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): review.rs candidates/inspect carriers were confirmed by P39-QUERY. The suppressedCount observation means the host must derive the count from the producing step. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-10** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): repair.rs is the repair:2 constructor owner; P39-REPAIR2 confirmed refusal before descriptor and the exact-class unavailability mapping. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-11** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): comparison.rs baseline.show carriers and pivot closure availability were confirmed by P39-QUERY controls. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-12** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): review.rs review.produce-brief is a host query operation, and P39-QUERY confirmed host-only operations are not public. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-13** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): configuration.rs recommend config2 proposals and CONFIG.INVALID policy-test admission routes were confirmed (P39-QUERY recommend joins; P39-POLICY P3). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-14** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): discovery.rs recommend discovery units and the NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT refusal were confirmed (P39-QUERY, P39-NATIVE-CUSTODY). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.
- **FW-15** OWNER-ROUTING-ASSESSED-NOT-EXECUTED (new-39; prior38 OWNER-ROUTING-ASSESSED-NOT-EXECUTED): policy.rs owns policy show/test. S39-01 and S39-02 route here and to the workflows section 5 reference verifier; the policy-show waiver resolution join refuses (P39-QUERY). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 38->39: True); implementation not executed.

### Inherited residuals

- **DR-001** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): current-source-map and the residual ledgers are byte-identical 38->39; this review refreshed the reading path on source39. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-002** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The identity/evidence/proof chain gained section 7 host composition joins (receipt, inventory, plan, stage), confirmed by P39-TERM7, and identity-and-evidence was re-read complete. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-003** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Read-only carrier routes are now machine-mapped (ADV38-02 closed, P39-CARRIER-RO). The 54 recovery cases remain unexecuted and real platform demonstration remains a release requirement. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-004** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The native contract changed (U-4b, U-9, allowJs) and was re-read complete; the native group passes. ADV39-01 records the in-place registered schema edit. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-005** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Executable custody reference groups pass on source39, and pruned-tree read custody was probed; native product carrier qualification is still required before release. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-006** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The descriptor graph is unchanged: graph-query-3 bytes equal source38 (P39-QUERY) and the full-replay child passes. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-007** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): ADV38-01 is closed by section 7. The D9 published successor artifact remains a carried implementation-unit obligation, not a new blocker. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-008** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The applied retention posture is unchanged. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-009** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The section 7 host observation is separate from the sealed Run record and does not alter it; attempt facts are validated by host callbacks, preserving lifetime neutrality. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-010** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Bounded first-party composition is unchanged (prototype-report-inventory byte-identical). The policy-test verifier is reference evidence only; S39-01/02 concern authoring-test fidelity, not composition authority. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R01** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Fact-plane successor schemas grew (identity-schemas +142: normalization-specification-map, stage-output registeredBy, bodyEligibility), diff-read and exercised by the consumer24 child. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R02** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Imperative plugins stay outside D-371: PolicyTestSuiteV2 refuses undeclared members and string expressions with POLICY.IMPERATIVE_KEY_REFUSED (P39-POLICY P3). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R03** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): plan2/exec-plan2 gained the membership order law (enumeration-plan schema and model diffs read); the enumeration child passes. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R04** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The carrierFormat axis now maps carrierFormat1/2 and fresh-install for read-only recovery (carrier-dispatch.v3.json:684-693). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R05** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The Rust protocol major 3 is unchanged; the native group passes. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R06** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The identity-model diff (read complete) is additive admission law (+232/-9); typed close_run outcomes were re-exercised by the executed analysis-seal and query-projection children. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R07** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Query retained availability routes are unchanged in substance (query-projection-contract +2/-1); the query-projection child passes. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R08** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): ADV38-01 closed; the D9 published successor artifact remains carried (DR-007). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R09** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Semantic IDs still exclude attempt identity: the section 7 observation carries attempts outside the Run, and policytest2 identity is a function of the suite alone (P39-POLICY P4). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R10** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): OPEN: this nonblind review cannot close the fresh blind implementer litmus. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R11** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): ADV38-02/03 are closed at source level. Real platform durability is unmeasured and the 54 cases are not executed. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R12** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Depends on TCB-SCOPE-01, assessed once on source39. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R13** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): Versioning successors are breaking majors, not relabels: PolicyTestSuiteV2 and repair:2 refuse major 1 typed (P39-POLICY P3, P39-REPAIR2). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R14** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): CFG-6/TM is unchanged. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R15** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (new-39; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): The trusted request context stays host-only: HostQueryParams operations are not public operations (P39-QUERY). The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.
- **DR-011-R16** CONDITION-1-OBLIGATION-RETAINED-ASSESSED (inherited-unchanged-38; prior38 CONDITION-1-OBLIGATION-RETAINED-ASSESSED): No executable report-hook admission: prototype-report-inventory and admission section 5 are byte-identical 38->39. The successor routing in inherited-residuals.proposed.md (byte-identical 38->39) is consistent with source39; original custody and standing preserved.

### Scoped review owners

- **DR-201** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-38; prior38 ROUTING-ASSESSED-ONLY-NOT-APPLIED): The semantic-correctness owner row (Run versus command finalization, post-commit output failure) is byte-identical. Source39 adds the delivery failure laws in that area, confirmed by P39-QUERY. Register 08 is byte-identical (True). This review is an input to the integrated review and is not applied.
- **DR-202** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-38; prior38 ROUTING-ASSESSED-ONLY-NOT-APPLIED): The delivery/operations owner row (recovery, repair, loader TCB) is byte-identical. The source39 read-only carrier routes and repair:2 fall under it and are confirmed at source level. Register 08 is byte-identical (True). This review is an input to the integrated review and is not applied.
- **DR-203** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-38; prior38 ROUTING-ASSESSED-ONLY-NOT-APPLIED): The prototype-lessons owner row (PARTIAL-SCOPED) is byte-identical. No source39 delta file touches the prototype reference or its pin. Register 08 is byte-identical (True). This review is an input to the integrated review and is not applied.
- **DR-204** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-38; prior38 ROUTING-ASSESSED-ONLY-NOT-APPLIED): The V1/coop invariant owner row (exact selector/digest posture) is byte-identical. This review validated exact selectors and digests independently, and ADV39-01 is a digest-posture advisory in its spirit. Register 08 is byte-identical (True). This review is an input to the integrated review and is not applied.
- **DR-205** ROUTING-ASSESSED-ONLY-NOT-APPLIED (inherited-unchanged-38; prior38 ROUTING-ASSESSED-ONLY-NOT-APPLIED): The small-core/components owner row (core/TCB boundaries) is byte-identical. TCB-SCOPE-01 remains coherent on source39. Register 08 is byte-identical (True). This review is an input to the integrated review and is not applied.

Every row: appliedByThisReview=false, finalApplicationOutcomeGranted=false.

## Read map

Whole-file claims are made only for fresh39Read (every line read this charter) and inheritedUnchanged38Read (read completely under the source38 review and byte-identical now). complete38ReadPlusComplete39Diff is a complete predecessor read plus the exact complete diff, listed separately. delta39Read and fresh39RangeRead are not whole-file reads. Hashes were recomputed at build time against the frozen snapshot.

Fresh complete reads (source39):
- `docs/coop/design-corrections/foundation/check-composition.v3.py` aeb17e1d4937fc4d (98 lines): targeted ranges
- `docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py` caa602935474f6d2 (914 lines): complete read (1-730, 731-914); new file
- `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` 30d4d9d2e7cb78c2 (334 lines): complete single read
- `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` e953dedee6ef76fe (298 lines): complete single read
- `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` f9eb575219cd4815 (372 lines): complete sequential read
- `docs/coop/design-corrections/security/carrier-dispatch.v3.json` f5c4ce7779f71bbb (696 lines): complete single read
- `docs/coop/design-corrections/security/carrier-format.v3.md` 2c3e465d90140228 (679 lines): complete single read
- `docs/coop/design-corrections/security/check-integrated-carrier.v1.py` acbdfed35ca4ae67 (28 lines): targeted ranges
- `docs/coop/design-corrections/workflows/policy-test-cases.v3.json` d1e94da920a28a13 (621 lines): complete single read; new file
- `docs/coop/design-corrections/workflows/policy_test_model.v3.py` 8138e2e8a4c4c008 (272 lines): complete single read
- `docs/coop/design-corrections/workflows/query-projection-contract.v3.md` 923ff32fc9e063f8 (207 lines): complete single read
- `docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json` 963d5bb1977991b2 (93 lines): complete single read
- `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md` 6b660fc36fe11d5b (226 lines): complete single read
- `docs/v2/architecture/commit-recovery-readonly.v3.md` 7bcc8f8e23da91e8 (497 lines): complete single read
- `docs/v2/architecture/implementation-normative-inputs.v7.json` 8543d29f7047b722 (160 lines): complete single read; new file
- `docs/v2/contracts/product-v1/identity-and-evidence.md` c82404f3a0cf56fa (1846 lines): complete: lines 1-859 earlier chunk plus 860-1846
- `docs/v2/contracts/product-v1/native-evidence.md` efd413891925c256 (3947 lines): complete sequential read 1-3947 (chunks 1-619,620-1079,1080-1539,1540-1999,2000-2499,2500-2999,3000-3479,3480-3947)
- `docs/v2/contracts/product-v1/security-and-lifecycle.md` a319da39b9f90aff (1532 lines): complete sequential read (1-420,420-979,980-1532)
- `docs/v2/contracts/product-v1/workflows-and-surfaces.md` 707d8147fc1c9532 (1694 lines): complete sequential read (1-299,300-599,600-899,900-1199,1200-1459,1460-1694)

Fresh range reads (not whole-file):
- `docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` 2bef052db5dacf53: 410-764
- `docs/coop/design-corrections/foundation/evaluator_input_model.v3.py` 021cc9ac7351f20b: 40-84
- `docs/coop/design-corrections/foundation/run-termination-goldens.v1.json` feefb64cd4707cb9: 262-443
- `docs/coop/design-corrections/security/check-carrier-v3.py` 834e337a18b1f632: 1-60,740-879
- `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py` 1284605f8fa10be0: 3540-3800,4100-4229,4340-4424
- `docs/coop/design-corrections/workflows/query_surface_projection.v3.py` 26106f4e523d6def: 270-469
- `docs/coop/design-corrections/workflows/workflows_model.v3.py` 130eb41c203ac19d: 1-52

Delta reads (38->39 diffs; not whole-file):
- `docs/coop/design-corrections/foundation/check-enumeration.v1.py` 732e0b045157c6d0: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/check-execution-inputs.v1.py` 5cbe6053f4d98b87: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/check-identity.py` 8e7100c5df596d1f: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/check-replay.v3.py` b1dd20521a7c8c68: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` 2bef052db5dacf53: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` 10627cb6a22a9ff1: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/enumeration_model.v1.py` 55a23396aefda8d1: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py` 510ef2960960eae3: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py` 567498c30830a49e: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json` 604bd94175584128: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py` b8ba152cdcd1783a: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/execution_inputs_model.v1.py` 7c6f7c5cb8f9db5f: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/identity-model.v3.py` a6dc5f997b5b9502: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/identity-schemas.v3.json` a76c9e2f07e8f8e5: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/incoming-search.schema.v1.json` accb597a95969109: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/run-evaluator3-checks.py` 152b280a21c35028: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/run-termination-goldens.v1.json` feefb64cd4707cb9: PARTIAL 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/run_termination_model.v1.py` cedf74a4ced223e9: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json` 6ab46925853d26c1: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/native/README.md` 277f7f4adae1ab88: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/native/native-cases.v2.json` fb1bcc38737ad04c: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/native/native-evidence-report.v2.json` 652d519dbc0a9106: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` 2d37b810bd9ffed7: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/native/native_evidence_model.v2.py` 51bcab333b2f35f4: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/public-detail-registry.v1.json` 2702e6ca97b6d809: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/security/check-carrier-v3.py` 834e337a18b1f632: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/README.md` 1fca693c5e50c8d4: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/check-query-projection.v3.py` 8e2c2b6b4b202cb6: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/check-workflow-projection.v3.py` 1284605f8fa10be0: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/command-inventory.v3.json` d303cc640154ff2b: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/query_surface_projection.v3.py` 26106f4e523d6def: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py` 08fb9b72a5de0e06: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/common.schema.json` b7b25d5e7c2bf2c8: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/README.md` 66c8cc1e83a62832: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json` d5126989a8d96ba9: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json` 09292fc108f223c9: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/command-inventory.schema.json` 34e4b2c01476e606: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json` ce45b9ff712fa0ea: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json` f82a30702180ed15: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json` 65980226dc5f879c: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/schemas/test-execution.schema.json` a6f7c2d85cdc4c4b: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/workflow_projection_model.v3.py` 6dea10d01f4a8991: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/workflows-report.v1.json` 8237d701c872c6bf: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/workflows_model.v1.py` be37023f173f339e: complete 38->39 diff (not a whole-file read)
- `docs/coop/design-corrections/workflows/workflows_model.v3.py` 130eb41c203ac19d: complete 38->39 diff (not a whole-file read)
- `docs/v2/architecture/14-repository-and-module-layout.md` 0e615869b76acba0: complete 38->39 diff (not a whole-file read)
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` 8313318630c55add: complete 38->39 diff (not a whole-file read)
- `docs/v2/architecture/implementation-coverage.v1.json` 5d324a3a0ffeda9d: PARTIAL 38->39 diff (not a whole-file read)
- `docs/v2/architecture/implementation-planning-sources.v1.json` 9f795ea5e2c8632f: complete 38->39 diff (not a whole-file read)
- `docs/v2/contracts/product-v1/security-and-lifecycle.md` a319da39b9f90aff: complete 38->39 diff (not a whole-file read)

Complete source38 read plus complete 38->39 diff:
- `docs/coop/design-corrections/foundation/run_termination_model.v1.py` cedf74a4ced223e9
- `docs/coop/design-corrections/security/check-carrier-v3.py` 834e337a18b1f632
- `docs/v2/architecture/14-repository-and-module-layout.md` 0e615869b76acba0
- `docs/v2/architecture/implementation-boundaries-and-build-plan.md` 8313318630c55add

Inherited unchanged from source38 complete reads (hash recomputed):
- `docs/v2/architecture/implementation-normative-inputs.v6.json` efa3777c6a79ce09
- `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql` b82d63c07bc7ca0a
- `docs/coop/design-corrections/security/carrier-migration.v1.md` 446c73dc9c95ae29
- `docs/v2/architecture/attempt-custody.schema.v1.json` 60a881545e63a9e8
- `docs/v2/architecture/store-instance-lineage.v1.json` 919d1717b53f202b
- `docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py` 26e88580acff3d93
- `docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py` 57e0d9d8e24cd1a1
- `docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py` b0afeb841fe94d13
- `docs/coop/design-corrections/inherited-residuals.proposed.md` 4b2b992b06abd9cd
- `docs/v2/contracts/product-v1/README.md` c53633c2c8e056de
- `docs/v2/contracts/product-v1/admission-and-qualification.md` 69cd6ba3cb41ed19
- `docs/coop/design-corrections/foundation/enumeration-contract.v1.md` ae4523a224bf6e21
- `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` 8649b8b079ccbd8f
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

Scope residue: {"changed38ReadNotFullyReread": [{"path": "docs/coop/design-corrections/foundation/run-termination-goldens.v1.json", "sha38": "9bdde8236ce24b299b36100325df4a6874bbba4e86d4abf308b653da457f4fcc", "sha39": "feefb64cd4707cb9b43223aaf0ba3c3192e6b5425fd05070ab84f2f9a4fd7d59", "delta39Read": true, "partialDiff": true, "rangeRead": ["262-443"]}], "deltaFilesWithoutReadEntry": ["docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json", "docs/coop/design-corrections/foundation/source-pins.v1.json", "docs/coop/design-corrections/native/source-pins.v2.json", "docs/coop/design-corrections/security/source-pins.v1.json", "docs/coop/design-corrections/workflows/source-pins.v1.json"], "pinLedgersVerifiedByPinGatesOnly": ["docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json", "docs/coop/design-corrections/foundation/source-pins.v1.json", "docs/coop/design-corrections/native/source-pins.v2.json", "docs/coop/design-corrections/security/source-pins.v1.json", "docs/coop/design-corrections/workflows/source-pins.v1.json"]}

## Retained obligations and authority

- residuals: 30
- authorGradesPending: 30
- condition2Obligations: 28
- condition2Source: docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 38->39: True)
- qualificationGatesUnperformed: 32
- qualificationGatesQualifiedTrue: 0
- recoveryCasesNotExecuted: 54
- condition5: NOT MET (not a design defect)
- d9PublishedSuccessor: Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.
- finalApplication: Must be performed by a NEW other actual Claude origin, not this origin and not any author, design or blind origin.
- Authority: {"gradeGranted": false, "activationGranted": false, "implementationAuthorized": false, "blindReconstructionClaimed": false, "source38AcceptanceInherited": false, "frozenInputsModified": false, "applicationOrReadinessGranted": false, "consumerArtifactsAccessedOrRepaired": false}
- Child completion: `{"referenceGroups": [{"name": "evaluator3", "exitCode": 0, "timedOut": false}, {"name": "foundation", "exitCode": 0, "timedOut": false}, {"name": "integration", "exitCode": 0, "timedOut": false}, {"name": "native", "exitCode": 0, "timedOut": false}, {"name": "security", "exitCode": 0, "timedOut": false}, {"name": "workflows", "exitCode": 0, "timedOut": false}], "evaluator3Children": {"current-profile": 0, "enumeration": 0, "atoms": 0, "execution-inputs": 0, "composition": 0, "full-replay": 0, "native-replay": 0, "execution-replay": 0, "candidate-replay": 0, "policy-derivation": 0, "faults": 0, "provider-attribution-return": 0, "workflow-projection": 0, "query-projection": 0, "comparison-knowledge": 0, "analysis-seal": 0, "native-consumer24-corrections": 0}, "planning": {"check_implementation_planning": 0, "check_repository_file_inventory": 0}, "probeRuns": {"P39-PKG": {"verify": 0, "nativeProbe": 0}, "P39-POLICY": 0, "P39-TERM7": 0, "P39-QUERY": 0, "P39-CARRIER-RO": 0, "P39-SCHEMA-DIGEST": 0, "P39-NATIVE-CUSTODY": 0, "P39-COMPARISON": 0, "P39-REPAIR2": 0}, "stdoutOnlyHelpers": ["probes/summarize_receipts.py", "probes/summarize_evidence.py", "probes/ledger.py"], "backgroundProcessesOutstanding": 0}`

## Limitations

- Nonblind review. The reviewer read the author package, author and root receipts and the source38 review. No blind consumer artifact, its implementation, or root replay diagnoses or oracles were accessed, used or repaired.
- Reference Python models over synthetic inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or crypto is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed (condition 5 NOT MET).
- Large changed reference code, schemas and ledgers were read as complete 38->39 diffs (delta39Read), not as whole files. Two diff reads are partial: implementation-coverage.v1.json (first 260 of 1014 diff lines, the rest resting on the executed planning checker) and run-termination-goldens.v1.json (diff lines 1-200 plus file lines 262-443, exercised by P39-TERM7 and the executed children). The five source-pins ledgers were not line-read; they are verified by the six executed pin gates.
- Several probes are helper-level, not full Runs: comparison presence knowledge (pure functions), native custody/fallback (owner functions), and the P1 composition side (a replica of the check-composition harness). The query and repair probes reuse the owner checker's module globals and admitted Runs. The carrier probe runs on the reference interpreter's in-memory SQLite with no stability observation.
- In-process monkeypatches (a spied shared builder; restoring the checker's rebound _S37_CF global) were always restored and verified.
- Probe attempts with harness defects were fixed and rerun, and their receipts were overwritten, so the failing outputs are not preserved as files. They were: policy-test (a duplicate-waiver negative broke waiverId order, reminted as w-zdup; a P4 row call missing its observed argument); carrier-readonly (IndexError importing check-carrier-v3 without argv; publish refused-by-ddl because the checker rebinds _S37_CF to prose); native-custody-fallback (custodyExcludedUnits rows must be {path, reason} objects). None was counted as a result.
- argvDigest, stage-output schema registration, the normalization specification map, body eligibility and the import bridge were confirmed by reading and executed author controls, not by independent probes.
- F-01..F-14 content lives outside the snapshot and was not re-derived.
- No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.
