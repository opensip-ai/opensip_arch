# Claude security/lifecycle correction evidence

Proposed, NOT self-accepted; mixed Claude/Codex corrections pending fresh independent Claude review
of a newly frozen subject. These are design reference instruments for
`docs/v2/contracts/product-v1/security-and-lifecycle.md`, not product implementation, OS
measurement, cryptographic verification or release qualification.

Provenance of the current bytes: actual Claude authored the unit; Codex supplied the v3
integration corrections (repair authorization binds the expected recipe and positive admitted
closures; strict end assertions `(?![\s\S])` in place of `$` anchors; S14/S15 headings). The
post-reset independent Claude review of frozen `candidate-subject.v1` (retained at
`../reviews/post-reset-review.v1/`) returned MUST-2, MUST-3, SHOULD-2/3/4/6/7
and ADV-3 against this unit; a new Claude author session corrected them here (handoff
`../reviews/post-reset-author.v1/handoff.md`). The second independent Claude review, of frozen
`candidate-subject.v2` (Codex retains it under `../reviews/`), returned N-1 (nested boundaries not
carried into native discovery), N-4 (no owning repair recovery authorization), N-5 (transition
intent/journal not representable) and advisories A-3/A-4/A-5; a further Claude author session
corrected them here (S3 `boundary_inventory`, S9.2 transition intent/journal/recovery, S10.2 repair
recovery authorization, the `transition-journal` lock action). A third independent session, a fresh
blind consumer reconstruction of the accepted `candidate-subject.v5` subset, returned M-5 (the
contract names typed public details the closed registry cannot express), S-2 (two schema-1 root
documents disagree on admission) and S-6 (discharged obligations still written as open); a further
Claude author session corrected them here (S12.1 public-detail projection with its closed vocabulary
and bounded pending-registration gap, S9.1 naming `RootV1` in this bundle as the product admission
boundary with strict end-anchor regressions, S8 correcting `PROFILE_SET_KEY_NOT_MACHINE_ID` to a
subject sub-detail, and the S3/S9.2/S10/S10.2 obligation sweep). No retained review covers the
corrected bytes.

- `security_lifecycle_model_v1.py`: pure reference model (foundation exact validator plus jsonschema). Sections
  S3–S11 of the contract: discovery custody with automatic workspace units under the ONE shared
  discovery rule (`../discovery-defaults.py`: dependency/VCS/Cargo-output trees pruned by exact
  path segment, first-party cap 4096 refusing typed `PROJECT.WORKSPACE_UNIT_LIMIT`, `.` sentinel
  normalization shared with the native instrument, nested `opensip.json` as a deliberate project
  boundary, the shared boundary prefix rule) and the `boundary_inventory` export of the admitted
  authority boundaries for the native unit instrument (`AdmittedBoundaryInventoryV1`), Config2
  `workspaceRoots` override, backup-custody write admission (UNKNOWN admits
  with disclosure; detected backup-managed needs the explicit choice), trust clock with
  refusal-before-write, boot-bound signed recovery epoch (exact counters, recovery authority),
  root chain, root schema 1/2 and profile-set envelope admission, live revocation (observer,
  linearization, postimage-checked rollback), lease modes, namespace registry and lock order,
  the core-transition lock set (`core_transition_affected_namespaces`, `core-transition-acquire|release`,
  `transition-journal`), the S9.2 installation transition intent/journal/crash-recovery
  (`admit_transition_intent`, `transition_journal_record`, `admit_transition_journal`,
  `recover_transition_journal`: one closed journal for core update|repair|rollback and store
  migrate|rollback binding the admitted-intent digest, from/to schema/store/generation, the frozen
  registry and the exact held lease set),
  platform population admission keyed by the ONE machine platform vocabulary (`PLATFORM_IDS`;
  `PLATFORM_DISPLAY_ALIASES` are output-only), migration/rollback floor continuity,
  `repository-code` grant V2 (operational admission before any Plan; no Plan projection input)
  plus the Plan-time join `semantic_projection_for_grants` / `admit_plan_execution_projection`,
  repair-apply authorization (S10.1), repair RECOVERY authorization (S10.2:
  `admit_recovery_authorization` over the closed `RepairRecoveryAuthorizationV1`, bound to the
  noncircular journal identity `repair_journal_identity` and the observed journal state
  `repair_journal_state_digest`; rollback/cleanup never consults recipe trust, commit does),
  offline guidance, and the S12.1 public-detail projection (`public_detail` / `public_details` over
  the closed `SECURITY_PUBLIC_DETAIL_CODES`, the declared
  `PENDING_PUBLIC_DETAIL_REGISTRATIONS` gap and `SECURITY_INTERNAL_DETAIL_ALIASES`; base code before
  the first colon, subject after it, D9 branch from the refusal, no wildcard family).
  Its docstring lists every TCB assumption (asserted signers and OS reads).
- `security-lifecycle.schemas.v1.json` (bundle version 2, 43 records): closed Draft 2020-12
  records for every model input document and output, including
  `TrustClockRecordV1`, `TrustRecoveryChallengeV1`, `TrustRecoveryEpochV1`,
  `RootV1`, `RootV2`, `PlatformProfileSetV1` (keys = the four machine ids), `PlatformProfileSetEnvelopeV1`,
  `RepoExecutionGrantV2` (V1 retained as superseded), `RepairApplyAuthorizationV1`,
  `RepairRecoveryAuthorizationV1` / `RecoveryAuthorizationAdmissionV1`,
  `SemanticProjectionV1`, `ExecutionProjectionAdmissionV1`, `CoreTransitionScopeV1`,
  `InstallationTransitionIntentV1` / `InstallationTransitionJournalV1` / `TransitionIntentAdmissionV1` /
  `TransitionJournalAdmissionV1` / `TransitionRecoveryV1`, `AdmittedBoundaryInventoryV1`,
  `PublicDetailProjectionV1`.
  Records marked `metadata` are signed security metadata under
  `opensip-metadata-canonical.1`; all others are product data under
  `../foundation/canonical.py`. The checker's exact validator treats `true` and
  `1` as different values everywhere.
- `*-cases.v1.json`: SYNTHETIC fixtures with hand-authored expectations (same
  author, not an independent oracle). `$name` references and `{"$from": ...}`
  overrides are resolved by the checker; `computed` values (journal identities, state digests,
  intent and registry digests) are produced by the model's own functions and the recipe is named
  in each file's standing. 453 cases across sixteen files, including `public-detail-cases.v1.json`,
  whose cases project the outcome of an inner model run rather than a hand-written outcome.
- `check-security-lifecycle.v1.py`: verifies `source-pins.v1.json`, admits the
  case files through the foundation canonicalizer, runs the cases, validates
  outputs against the schemas, runs the ten invariant sweeps (including the generated
  4200-installed-manifest / 4200-first-party-unit discovery sweep, the four-platform
  vocabulary join across profile set, admission, grant, native matrix and workflow schema, and the
  admitted-boundary join that runs the nested-repository/nested-project fixture through this
  instrument and `../native/native_evidence_model.v2.py`, and the public-detail closure sweep that
  projects every refusing case outcome and asserts the emitted vocabulary is inside the unit's closed
  set and that the not-yet-registered gap stays within the declared pending list)
  and writes the report.
- `security-lifecycle-report.v1.json`: the retained report of the last pinned run (pre-correction
  bytes; the pinned run is re-generated only after Codex re-pins). Unpinned runs of the corrected
  bytes are retained in the author handoff directories.
- `source-pins.v1.json`: exact SHA-256 of every external source read while
  authoring; the unit's own files are authenticated by the reviewer, not by
  themselves.
- `initial-author-response.json`: handoff record (files, checks, open joins).

Run with Python 3.12 and jsonschema 4.25.1 from this directory:

```
/tmp/opensip-architecture-review-env/bin/python -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json
```

Exit 0 means all pins verify, all cases pass, all outputs validate and all
sweeps hold. It does not qualify a native carrier, a platform lane or a signing
ceremony.
