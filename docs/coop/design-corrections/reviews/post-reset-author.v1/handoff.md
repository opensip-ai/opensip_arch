# Post-reset author handoff (Claude, new author session) — security + native corrections

Standing: corrections in the working tree `/Users/sb/code/opensip-ai/opensip_arch`, NOT committed,
NOT pushed, NOT self-accepted. Design reference only; no product implementation. Frozen
`candidate-subject.v1` is untouched. Codex's concurrent corrections (repair authorization
binding, two new security cases, strict `(?![\s\S])` end assertions, S14/S15 headings,
removal of the sufficiency shortcut) are preserved; no frozen bytes were restored over them.

Inputs: `/tmp/opensip-design-corrections/post-reset-review.v1/review.md` and
`probes/independent-probes.json` (P2–P7, P11, P14). Owned scope only (security/, native/,
the two contracts, one shared artifact); nothing under foundation/, workflows/, integration
files, D-372, pins, ledger, navigation or readiness register was edited.

## Findings → what changed

### MUST-2 (P2): one machine platform vocabulary
- `security_lifecycle_model_v1.py`: `PLATFORM_IDS = (linux-aarch64-gnu, linux-x86_64-gnu, macos-aarch64, macos-x86_64)`;
  `SUPPORTED_POPULATION` re-keyed to it; `PLATFORM_DISPLAY_ALIASES` (output only); `PLATFORM_TRUTH_TABLE` built over
  `PLATFORM_IDS`; `platform_admit` outputs `displayAlias`, refuses an alias presented as platform
  (`NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:<id>`) and a profile set keyed by a non-machine id
  (`PROFILE_SET_KEY_NOT_MACHINE_ID:<keys>`); grant admission refuses `GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID:<id>`.
- Schema: `PlatformProfileSetV1.platforms` keys = the four ids; `PlatformAdmissionV1.displayAlias` (required).
- Cases: `platform-admission-cases.v1.json` re-keyed (three `linux-arm64-*` ids renamed `linux-aarch64-gnu-*`); 6 new cases
  (machine id admits with alias output; alias refuses ×2; alias-keyed profile set schema-invalid + refuses; macos-x86_64 and
  linux-x86_64-gnu admit). `root-schema-cases.v1.json` profile-set bodies re-keyed; body digest recomputed with the model's
  metadata canonicalizer (`d3bb8500…` → `df98424c…`). `execution-principal-cases.v1.json`: alias-in-grant refuses;
  macos-x86_64 grant admits (all four ids now have a positive grant case).
- Sweep `one-machine-platform-vocabulary-joins-…`: for each id `platform_admit` ADMIT, then a grant with that same id ADMIT; the
  alias refuses in both; asserts equality of the id sets across the security schema, the truth table, the native matrix
  `platformFamilies` and the workflow `test-execution.schema.json` `platformId` enum.
- Contract S8: table now `Platform id | Display alias | Population | Lane`, with the alias law; S10 references S8 ids; S15 wording.
- Native: matrix and §1.1 already used the four ids; README/contract now state the S8 join.

### MUST-3 (P3, P4, P5): ONE shared discovery rule
- NEW `docs/coop/design-corrections/discovery-defaults.py` (shared artifact; see interface below).
- Security `discovery`: automatic branch calls `DD.enumerate_units` over relative marker paths BEFORE custody walks;
  pruned trees recorded once in provenance `prunedTrees` (`{path, reason, markerCount}`); cap refusal is typed
  `PROJECT.WORKSPACE_UNIT_LIMIT` (new D9 row → `REQUEST.UNSATISFIABLE`, detail `WORKSPACE_UNIT_LIMIT:<n>><cap>`), no
  KeyError; explicit joins / Config2 roots go through `DD.normalize_explicit_root` (`.` → selected root, trailing `/`
  dropped, grammar → `JOIN_PATH_GRAMMAR`), refuse inside a pruned tree (`JOIN_INSIDE_PRUNED_TREE:<reason>:<anchor>`), and an
  explicit root without a marker is admitted for custody with warning `EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER:<path>`.
- Native `discover_units`: consumes `DD.enumerate_units` / `classify_path`; returns `UnitDiscoveryV1 {units, prunedTrees,
  refused}` (new closed schema + `PrunedTreeV1`); cap is the typed `native.too-many-units` refusal record with
  `unitCount`/`limit` (was an `AdmissionError`); explicit roots normalized by the shared function (`.` → ``; new typed detail
  `native.explicit-root-grammar` → CONFIG.INVALID); `assign_membership` uses `classify_path` with Cargo roots derived from the
  rust units (workspace root + folded members) instead of substring matching; `unit_scope_descriptor` takes
  `pruned_trees` and lists `.git`/`node_modules` per unit root and `target` per Cargo root only; `typescript_mode` uses the
  segment rule. `synthetic_marker_set` is a documented fixture generator for the 4200-manifest cases.
- Cases (security): `installed-dependencies-and-cargo-build-output-are-pruned-by-segment-legal-target-directories-stay-units`
  (root Cargo.toml+package.json, node_modules ×3 incl. a Cargo.toml, `packages/target`, `packages/web` + its node_modules,
  `src/target`, real `target/`), `config2-workspace-root-dot-…`, `…-trailing-slash-…`, `explicit-root-without-a-language-marker-…`,
  `explicit-root-inside-an-installed-dependency-tree-refuses`, `…-inside-cargo-build-output-refuses…`,
  `explicit-root-source-directory-called-target-is-admitted`, `…-grammar-refusals`. Sweep
  `discovery-prunes-installed-dependencies-and-refuses-real-cap-typed`: 4200 installed → ACCEPT (1 unit, one pruned tree with
  markerCount 4200); 4200 first-party → REFUSE `PROJECT.WORKSPACE_UNIT_LIMIT` / `REQUEST.UNSATISFIABLE` (detail `4201>4096`,
  units `[]`); 4095+root = 4096 → ACCEPT; `classify_path` table incl. `packages/target/index.ts`, `src/target/x.ts` (not pruned),
  `crates/core/target/out.rs` (pruned), `crates/core/src/target/mod.rs` (not pruned); grammar refusals.
- Cases (native): `units-installed-dependencies-are-pruned-by-segment-and-legal-target-directories-are-program-members`,
  `units-4200-installed-package-manifests-are-one-pruned-tree-not-a-cap-refusal`, `units-explicit-root-dot-is-the-project-root-…`
  (`.`, `packages/web/`, `packages/./web` grammar refusal, `node_modules/left-pad` without-marker refusal), `too-many-units-rejected`
  extended with the real 4200-unit refusal; `units-nested-monorepo-…` scope expectation updated (`target` only under Cargo roots).
- Contracts: security S3 (shared rule, explicit-root normalization, custody-vs-language-unit split), S12 rows; native §1.4
  (U-4 reworded, new U-4a, U-7, Config2 join, scope descriptor), §10 rows, §13 H-1, §14 (1024 vs 4096 wording).

### ADV-3: nested config vs VCS root — decided
Nested `opensip.json` is a deliberate project boundary in both directions: nearest config wins for launches inside it (unchanged
walk); the enclosing project records it as `nestedProjects` (new provenance field), excludes its units
(`INSIDE_NESTED_PROJECT`) and refuses joins into it (`JOIN_CROSSES_NESTED_PROJECT`). Cases
`nested-config-inside-a-vcs-root-is-a-deliberate-project-boundary-launch-inside-selects-it`,
`…-launch-elsewhere-selects-the-vcs-root-and-never-enters-the-nested-project`, `explicit-join-crossing-into-a-nested-project-refuses`.
Contract S3 states the decision and the rejected alternative.

### SHOULD-2 (P11): test-runner grant has no Plan; preparation precedes analysis
- `admit_repo_execution_grant` no longer reads `ctx.semanticGrantPrincipals` (removed refusal
  `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED`); admission is operational for every class. Docstring states the retained bindings and
  that the empty-owner digest is bookkeeping, not the runner binding.
- NEW `semantic_projection_for_grants(grants)` (preparation classes only → `[{kind, closureId, ownerSourceDigest}]`) and
  `admit_plan_execution_projection(planPrincipals, consumedGrants, preparedResolution)` (Plan-time; refusals
  `PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED:<d>`, `PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT:<d>`, `PLAN.TEST_RUNNER_HAS_NO_PLAN`,
  `PLAN.HOST_PREPARED_WITHOUT_GRANT`, `PLAN.GRANT_CONSUMED_WITHOUT_HOST_PREPARED`; D9 row `PLAN.EXECUTION_PROJECTION_REFUSED` →
  `REQUEST.PRECONDITION_FAILED`). Schemas `SemanticProjectionV1`, `ExecutionProjectionAdmissionV1`; checker models
  `semantic-projection`, `execution-projection`.
- Cases: `ctxBase.semanticGrantPrincipals` removed; `operational-grant-admits-without-any-plan-projection-…` (replaces the
  former projection-missing refusal case); `test-runner-grant-admits-with-no-plan-empty-owner-digest-is-bookkeeping-…`
  (ownerSourceDigest = sha256(canonical `[]`) = `4f53cda1…2b945`); `test-runner-runner-outside-both-sealed-sets-refuses-although-the-empty-owner-digest-matches`;
  `a-ctx-projection-is-never-consulted-not-an-authority-condition`; `semantic-projection-for-grants-projects-preparation-grants-only-…`;
  `plan-projection-equal-…-admits`, `plan-missing-…-refuses`, `plan-projecting-…-without-grant-refuses`, `test-runner-grant-is-never-a-consumed-plan-grant`.
- Contract S10: new "Operational admission precedes any Plan" section; S15 wording; native §13 H-7.

### SHOULD-3 (P6): S3.1 corrected — UNKNOWN admits with mandatory disclosure; detected backup-managed needs the explicit choice.

### SHOULD-4 (P7): confirmed Codex removed the one-rung existential shortcut (diff vs frozen: the two-line early return before
the confidence check is gone). Added regression `sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut`
(clones, floor 900000, confidence 100000 → `confidence-floor-unmet` in v2 and in the v1 oracle; 1000000 → satisfied). Model
docstring/comment and contract §4.6 (step 9 removed; "no early exit") updated. All earlier checks preserved.

### SHOULD-6 (P14): core transition lock scope — decided
Composition, not a new flock mode: fence held for the whole transition; affected namespace set from the host registry via
`core_transition_affected_namespaces(intent, registry)` — ALL registered when from/to state schema differ or a store is
re-selected (`core rollback`, `store migrate|rollback`), NONE for same-schema `core update`/`core repair` (immutable generations
stay pinned; ordinary component `install`/`update` publish generations under the fence alone and never revoke a pinned one);
EXCLUSIVE taken per namespace in locator byte order, non-blocking, all-or-nothing with reverse-order release and `PROJECT.BUSY`
naming the busy namespace; journal names the exact lease set after acquisition; crash recovery is the first act under the next
fence and re-acquires the journaled set; no arbitrary namespace (unregistered → violation). `lease_schedule(actions, registry)`
now multi-namespace with `core-transition-acquire|release`; schema `LeaseTraceV1` (trace `namespace`, final `namespaces`,
`coreTransitions`), `CoreTransitionScopeV1`. 8 lease cases + 6 scope cases. Contract S7 (namespaces, protocol, command map),
S15 aligned; S9 journal records the lease set.

### SHOULD-7 (owned parts)
- Native: second `## 11.` → `## 14.`; header no longer cites the empty `native-fix-handoff.v3.md` as a handoff or claims a retained
  Codex review v2 (states that R1–R7's only retained record is the feedbackMap/README table); §7.4 rewritten as resolved (verified:
  workflow `doc_digest` is raw SHA-256, one payload domain per kind); §13 conflicts (a)/(b) marked resolved; model comment line
  "AuthorizedExecutionV1" → V2; counts (93 cases, 82 defs).
- Security: S13 count 312 → 361, six → eight sweeps; provenance paragraph names the actual retained review and this handoff;
  S14/S15 headings preserved; S15 cross-reference "native §11" → "native §14".

## Checks run (pin gate bypassed; retained here)
- `run-security-unpinned.py` → `security-run3.json`: 361/361 cases (discovery 64, execution 46, platform 38, clock 33,
  revocation 30, root-schema 30, recovery 29, lease 29, root-chain 16, repair 15, migration 14, offline 9, storage 8),
  8/8 sweeps hold, 30 output schemas validated. Frozen baseline was 318 cases / 6 sweeps.
- `run-native-unpinned.py` → `native-run3.json`: 93/93 (32 positive, 61 negative), 60 matrix cells, 0 open objects, all
  F1–F12/R1–R7 covered. Frozen baseline 89/89.
- Pinned runs still fail at the pin gate (expected): security pins name Codex-changed `identity-and-evidence.md`,
  `common.schema.json`, `workflows-and-surfaces.md`; native pins likewise. Retained reports in the repo are the frozen bytes
  (my first baseline run had overwritten `native-evidence-report.v2.json` with a pin-mismatch stub; restored byte-for-byte).
- `owned-file-deltas.json`: sha256 before/after for every owned file. Edit scripts retained: `edit-security-schemas.py`,
  `edit-security-cases.py`, `edit-native-cases.py`.

## Shared discovery interface for Codex (integration)
`docs/coop/design-corrections/discovery-defaults.py` (pure, no I/O; load like the other reference modules):
- `enumerate_units(marker_relpaths: Iterable[str]) -> {'unitDirs': [rel dirs, '' = root], 'prunedTrees': [{path, reason, markerCount}], 'refusal': None | {'detail': 'WORKSPACE_UNIT_LIMIT', 'unitCount', 'limit': 4096}}`
- `classify_path(relpath, cargo_roots) -> None | (anchor, reason)` with reason ∈ `dependency-tree | vcs-tree | cargo-build-output`
- `cargo_roots_from_markers(marker_relpaths) -> set[str]`; `normalize_explicit_root(spec) -> internal root ('' for '.')`, raises
  `RootGrammarError('ROOT_GRAMMAR')`; `spell_root(internal)`; `conventional_excluded_prefixes(unit_roots, cargo_roots)`.
- Constants: `WORKSPACE_MARKERS`, `MAX_WORKSPACE_UNITS`, `DEPENDENCY_TREE_SEGMENTS`, `VCS_TREE_SEGMENTS`, `CARGO_BUILD_OUTPUT_SEGMENT`.
Security exposes it as `model.DD`; native as `native_evidence_model.DD`. Suggested integration check: feed one marker inventory to
`S.discovery` (as an fs fixture) and `N.discover_units`; assert the security unit paths (relative to the selected root) equal
`N` unit `rootPath`s and both `prunedTrees` lists agree.

## Remaining obligations (not in my scope)
1. Re-pin `security/source-pins.v1.json` and `native/source-pins.v2.json` (add `discovery-defaults.py` to both; the native pin
   of the empty `reviews/native-fix-handoff.v3.md` may be dropped); regenerate both retained reports; freeze a new subject
   including `discovery-defaults.py`.
2. `check-integration.py bind()` and `integration-host-model.py`: stop seeding `ctx.semanticGrantPrincipals`; derive the Plan
   requirement via `S.semantic_projection_for_grants(grants)` and check with `S.admit_plan_execution_projection(...)` at Plan
   admission (`admit_preparation`'s `semanticGrantProjection` should equal it under `host-prepared`).
3. `foundation/product-configuration-model.py` still refuses `.` in `workspaceRoots` (`CONFIG_LOGICAL_PATH`); Codex said it will
   allow the sentinel (share `normalize_explicit_root`).
4. `workflows-and-surfaces.md` §12 says "Native §11 and security S13"; should read native §14 / security S15. Command inventory
   `core-*` `authorizationClass: exclusive-lease` may be relabelled to the S7 core-transition lock set (or documented as such).
5. `foundation/g13-result-schema.v5.json` still enumerates `macos-arm64`/`linux-x86_64`/`linux-arm64`; foundation owner to
   decide whether that historical schema stays alias-spelled (display) or moves to the machine ids.
6. MUST-1 (detail-code registry) is Codex's; the security/native detail spellings used here are unchanged
   (`storage.backup-choice-required`, `native.*`, `GRANT.*`, `PLAN.*`) and should be registered there.
7. Top-level `design-corrections/README.md` / crosswalk should list `discovery-defaults.py`.

Not claimed: no product qualification, no OS/crypto measurement, no acceptance of these bytes; expectations are same-author.
