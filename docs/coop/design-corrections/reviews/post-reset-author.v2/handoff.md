# Post-reset author handoff v2 (Claude, new author session) — N-1/P3, N-4/P9, N-5/P10, A-3/P22, owned A-4/A-5

Standing: proposed design/reference corrections in the working tree `/Users/sb/code/opensip-ai/opensip_arch`, NOT
committed, NOT pushed, NOT self-accepted, no product implementation. Frozen `candidate-subject.v2` re-verified
byte-identical after this session. Owned scope only: `security/`, `native/`, `discovery-defaults.py`,
`security-and-lifecycle.md`, `native-evidence.md`. Untouched: source pins, retained reports, foundation/, workflows/,
integration files, public-detail registry, crosswalks, D-372, readiness. Every owned file started from bytes equal to
frozen v2 (`owned-file-deltas.json`: 14 changed, 2 new, 18 unchanged incl. both pin files and both retained reports).
Prior author + Codex corrections and the exact-input `(?![\s\S])` patterns are preserved.

Inputs: the reviewer's final `post-reset-review.v2/review.md` (CHANGES_REQUIRED, N-1..N-5, A-1..A-5; arrived
mid-session) and probes P3/P9/P10/P22. Codex-side API/record examples are in `handoff-interface.json` (generated from
the corrected bytes: exact records, references and admission outputs).

## 1. Repair RECOVERY authorization (N-4 / P9) — security S10.2

- Record `RepairRecoveryAuthorizationV1` (product data, closed): project, plan, base snapshot, recipe closure;
  `journalRef` (exact journal identity); `journalState` + `observedJournalStateDigest`; finite `recoveryAction`;
  `originalRequestId`, fresh `recoveryRequestId`/`recoveryExecutionId`; `consent`; `issuedAt`/`expiresAt`;
  `leaseMode: EXCLUSIVE`, `mutationBoundary: host-broker`, `repositoryExecution: false`, `newEdits: false` (schema
  constants). Reference = `security.repair-recovery-authorization.v1:<H>` (full, never `auth:<16hex>`).
- `admit_recovery_authorization(authz, ctx)` → `RecoveryAuthorizationAdmissionV1`. Trusted context inputs (13, each
  named in the output): projectId, repairPlanId, baseSnapshotId, journal (as read under the EXCLUSIVE lease before any
  write), recoveryRequestId, recoveryExecutionId, ci, admittedTime (S4), custodyAdmitted (S3 re-run), policyAdmitsRepair,
  recipeClosureId, revokedClosures, admittedClosures.
- Noncircular journal identity `repair_journal_identity`: `H('security.repair-apply-journal-identity.v1', {schemaFamily,
  schemaMajor, requestId, stepId, executionId, repairPlanId, baseSnapshotId, authorizationRef})` — never state, paths,
  blobs or the recoveryAuthorizationRef the journal later carries; one journal has one identity in every state.
- Replay/crash: `repair_journal_state_digest` = sha256(canonical {state, stagedPaths, appliedPaths, preimageBlobs}) as
  read. A successful mutation changes state → replay refuses `AUTHZ.JOURNAL_STATE_MOVED`; a crash / requires-broker
  before the first write leaves it unchanged → same authorization resumes within the 24 h lifetime with a fresh attempt.
- Inspection is read-only, no record. Terminal states admit no mutation (`AUTHZ.RECOVERY_NOT_MUTATING:<state>`).
  Action table mirrors the workflow `RECOVERY_TABLE` mutating rows (equality verified in `probes-v2.py`; Codex retains
  the check). Safe rollback/cleanup (`discard-temps`, `roll-back-renamed`) never consults recipe trust (a revoked recipe
  must still roll back); `verify-postimages-and-commit` re-consults it (revoked → `AUTHZ.RECIPE_CLOSURE_REVOKED`,
  EXTENSION.ADMISSION_REJECTED; not admitted → `AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED`). Preimage/postimage law mandatory.
- Cases: NEW `repair-recovery-authorization-cases.v1.json` (32: valid rollback; rollback under revoked recipe admits;
  staged discard-temps; commit revoked refuses first / admitted admits / not-admitted refuses; action mismatch; COMMITTED
  and RECOVERY_BLOCKED not authorizable; journal mismatch; replay after rollback; crash resume; expired / not-yet-valid /
  lifetime bound / expiry≤issue; no admitted time; not-fresh / mismatched / original-request mismatch; repositoryExecution
  true, newEdits true (schema-invalid + refuse); CI interactive / CI policy; custody; plan mismatch; journal of other
  plan; lease mode; boundary; policy; shape; ci=0).

## 2. Installation transition intent + JOURNAL (N-5 / P10) — security S9.2, S7, S15

- `InstallationTransitionIntentV1` = required field/operation contract for the workflow `CoreTransitionIntentV1`
  successor: 11 fields (adds `fromStoreGeneration`, `toStoreGeneration`), 5 operations (adds `store-migrate`,
  `store-rollback`). `admit_transition_intent` is total: repair keeps closure/schema/store; update changes closure, never
  lowers schema, schema change ⇔ new store; rollback changes closure, never raises schema, needs the host deadline;
  store-migrate keeps core, advances schema, new store; store-rollback keeps core, retreats schema, re-selects retained
  store, needs deadline. `transition_intent_digest` = raw sha256 canonical intent (= inputDescriptorDigest).
- `InstallationTransitionJournalV1` (`transition_journal_record`, `admit_transition_journal` →
  `TransitionJournalAdmissionV1`, ref `security.installation-transition-journal.v1:<H>`): intentDigest + every intent
  field; frozen `registry` + `registryDigest`; `affects` + exact `leaseSet` = `core_transition_affected_namespaces`
  over the frozen registry (caller-chosen smaller set → `TRANSITION.SCOPE_MISMATCH`); state `LEASED`; schema constants
  `fenceHeld`, `writtenAfterAllLeasesHeld`. ctx (host observations under the fence): intent, intentDigest,
  namespaceRegistry, fenceHeld, leasesHeld, currentStateSchema, currentStoreGeneration, currentCoreGeneration,
  admittedTime. Busy namespace ⇒ `LEASE_SET_NOT_HELD` (no journal written). Rollback window checked against S4 time.
- `recover_transition_journal` → `TransitionRecoveryV1`: no fence → refuse; registry differs → QUARANTINE
  MIGRATION.CORRUPT; lease set not re-acquired exactly → PROJECT.BUSY; LEASED/PREPARING → ABORT; PREPARED → store op via
  S9 `migration_recover` footprint (RESUME-COMMIT step 3 / ABORT / QUARANTINE without footprint), core op → ABORT;
  COMMITTED → RESUME-COMMIT (never reversed); DONE/ABORTED → RELEASE-ONLY.
- `lease_schedule` new op `transition-journal {actor, namespaces}`: JOURNALED only under the fence after
  `core-transition-acquire` of exactly that set (`LeaseTraceV1` op enum extended); 5 new lease cases.
  `core_transition_affected_namespaces` also re-selects when the store generation changes.
- Cases: NEW `transition-journal-cases.v1.json` (42: 20 journal admissions incl. all five operations, empty registry,
  smaller set, busy, no fence, digest/field/registry/schema/store/generation mismatch, not-LEASED, shape; 11 intent
  semantics incl. the nine-field legacy intent refusing shape with the required-field list; 11 crash recoveries).
- Contract: S7 item 4 rewritten; new S9.2; S12 rows; S14 lock-set wording (A-4); S15 five operations + journal.

## 3. Admitted boundary inventory (N-1 / P3) and explicit Cargo root (A-3 / P22) — shared, security S3, native §1.4

- `discovery-defaults.py` v2: `relative_locator`, `boundary_inventory_from_provenance` (absolute custody locators →
  relative scope paths: nestedRepositories, nestedProjects, custodyExcludedUnits verbatim, prunedTrees),
  `classify_boundary` (ONE prefix rule, now also used by security `_in_nested_repo/_in_nested_project`),
  `classify_custody_exclusion`, `boundary_excluded_prefixes`.
- Security: `boundary_inventory(result)` → `AdmittedBoundaryInventoryV1` (Reject unless ACCEPT); model
  `boundary-inventory` cases (P3 fixture; launch inside nested config → no boundary; custody rows verbatim; refused
  discovery exports nothing); sweep `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`
  runs the P3 fixture through BOTH instruments (unit sets equal, excluded reasons equal, pruned trees equal,
  memberships outside, scope prefixes, join refusals in both, standalone source=none, mismatch refusal).
- Native: `discover_units(markers, explicit_roots, boundaries)`, `assign_membership(..., boundaries)`,
  `unit_scope_descriptor(..., boundaries)`; `UnitDiscoveryV1.boundaries` (`UnitBoundariesV1`: source
  `security.discovery|none`, lists, `excludedUnits {path, marker, reason, anchor}`, disclosure); membership
  `outside-project-boundary` + reasons; `outsideBoundaryFiles`; refusals `native.explicit-root-crosses-boundary`
  (CONFIG.INVALID) and `native.boundary-inventory-mismatch` (REQUEST.PRECONDITION_FAILED: inventory prunedTrees must
  equal the native-derived ones — caller ignores are never proof of completeness). `boundaries=None` retained for the
  standalone pure instrument only, disclosed as `source: none`.
- P22: explicit roots keep the semantic member packages of a SELECTED Cargo workspace root folded (only their
  `Cargo.toml`), so member `target` stays pruned; naming a member alone selects it as its own `cargo-package` unit.
- Cases (native, `PR2-P3`/`PR2-P22`): nested repo+project excluded (full unit array, memberships, scope prefixes);
  explicit root crossing (project, sub-dir, repo with trailing slash; `.` admits); launch inside nested config; standalone
  source=none; pruned-tree mismatch + non-security source schema-invalid; custody-excluded dir + marker; explicit Cargo
  workspace root == automatic rows, member alone.
- Contract: S3 "Admitted boundary inventory" + A-5 read-set sentence + Config2 trailing-slash correction (fixture
  re-labelled `cli-workspace-root-with-trailing-slash-...-config2-refuses-it-earlier`); native §1.4 U-2 (explicit roots),
  U-4a (A-5), NEW U-8, Config2 join, scope paragraph; §10 rows; §12 counts (100 cases: 35/65; 86 defs); §13 H-1, NEW H-8;
  header provenance now cites `reviews/post-reset-*` repository paths.

## Checks (all UNPINNED: pin gate bypassed by `run-security-unpinned.py` / `run-native-unpinned.py`; retained here)

- `security-run4.json`: 444/444 (baseline 361), 9/9 sweeps (baseline 8), 36 output schemas validated; per file:
  discovery 68, execution 46, transition-journal 42, platform 38, lease 34, clock 33, repair-recovery 32, revocation 30,
  root-schema 30, trust-recovery 29, root-chain 16, repair 15, migration 14, offline 9, storage 8.
- `native-run5.json`: 100/100 (35 positive, 65 negative; baseline 93), 60 matrix cells, 0 open objects, 86 defs,
  PR2-P3 ×6, PR2-P22 ×1.
- `probes-v2.json`: P3, P9, P10, P22 all OK against the corrected tree; workflow RECOVERY_TABLE mutating rows ==
  security RECOVERY_ACTION_FOR_STATE; workflow still mints `auth:` (Codex join pending); workflow intent enum still 3.
- Contract hygiene: no duplicate heading numbers, 0 `/tmp` citations in the two contracts and two READMEs; count claims
  match (444 / nine; 100 / 86-def).
- Pinned runs fail at the pin gate as expected (Codex re-pins). Retained reports and pin files unchanged.
- Edit scripts retained: `edit-native-schemas.py`, `edit-native-cases.py`, `edit-security-schemas.py`,
  `edit-security-cases.py`, `fix-trailing-slash-case.py`, `make-handoff-interface.py`, `make-handoff-json.py`.

## Remaining joins (Codex; details and examples in `handoff-interface.json`, spellings in `handoff.json`)

1. Workflow `RepairApplyJournalV1.recoveryAuthorizationRef` → closed grammar; `repair_recover` consumes the host
   projection of `admit_recovery_authorization` (drop the caller dict / `auth:` mint); integration-host-model
   recovery projection; retain the action-table equality check.
2. Workflow `CoreTransitionIntentV1`: +`store-migrate`/`store-rollback`, +`fromStoreGeneration`/`toStoreGeneration`;
   `core_transition_scope` → `admit_transition_intent` + journal admission with the registry read under the fence;
   store commands bind the intent.
3. `check-integration.py`: compose `S.boundary_inventory(sd)` into `N.discover_units` on a nested fixture.
4. Registry: register the new `AUTHZ.*`, `TRANSITION.*`, `native.explicit-root-crosses-boundary`,
   `native.boundary-inventory-mismatch` spellings (N-2 consolidation is Codex's).
5. Re-pin both units (security pins gain `native_evidence_model.v2.py` for the new sweep; native pins drop the empty
   handoff), regenerate reports, freeze a new subject, fresh independent review. Top-level README/crosswalk dispositions.

Not addressed (not mine): N-2, N-3, A-1 (foundation semantic-grant `analysisOperations`; a security-side check could be
added next round), A-2. Not claimed: acceptance, product qualification, OS/crypto measurement; expectations are
same-author.
