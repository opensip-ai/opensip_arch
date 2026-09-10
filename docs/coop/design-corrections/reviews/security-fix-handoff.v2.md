# Security unit fix handoff v2 — answer to Codex CHANGES_REQUIRED (NOT self-accepted)

Author: actual Claude (security unit, joint design author). Date: 2026-09-05.
Scope of bytes touched: `docs/coop/design-corrections/security/` and
`docs/v2/contracts/product-v1/security-and-lifecycle.md` only. No
implementation, no commit, no history edit. Foundation bytes are frozen under
independent review and were only re-pinned; native is being revised
independently and the S10 join names the fields it must confirm. This handoff
is for Codex's independent re-review; the author does not accept it.

Checker run (Python 3.12.13, jsonschema 4.25.1):

```
/tmp/opensip-architecture-review-env/bin/python -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json
{"passed": true, "counts": {"total": 312, "pass": 312, "fail": 0}, "sweeps": [... 6 hold ...]}
```

Previous run: 234 cases, 5 sweeps. Added: 78 cases (all but 9 negative) and
one sweep; the recovery sweep was rewritten. All 25 source pins verify.

## Item-by-item disposition

### MUST S3 — monorepo units, authority roots vs workspace units

Chosen design (contract S3, table "Authority roots versus workspace units"):

- A *project authority/custody root* is the selected root (one ProjectId, one
  lease namespace). Nested repositories are other custody roots: recorded,
  never entered, and a join crossing into one refuses
  `PROJECT.EXPLICIT_PATH_INVALID` / `JOIN_CROSSES_NESTED_REPOSITORY`.
- A *language workspace unit* is any directory inside the admitted root with
  a `Cargo.toml`, `package.json`, `tsconfig.json` or `jsconfig.json` marker
  (markers may co-locate; the unit lists them). Units are discovered
  automatically for zero-config; precedence: CLI `--project` joins >
  admitted Config2 `discovery.workspaceRoots` > automatic. Explicit sources
  refuse on custody failure; automatic units failing custody are excluded and
  recorded in `excludedUnits` with the reason (never silently dropped).
- Manifests are data: presence only at discovery; no script/hook/plugin/
  workspace-glob execution and no source write anywhere.
- The nonexistent "config project list" and the duplicate `--project`
  implicit multi-project wording are removed; `discovery.workspaceRoots` is
  the only configuration carrier and is admitted with identical custody.

Evidence: `discovery()` (unit source precedence, `_markers`, `_unit_custody`),
`DiscoveryProvenanceV1` gains `unitSource`, `units[].markers`,
`excludedUnits`. Cases: 7 new (`zero-config-monorepo-…`, `trust-group-admits-…`,
`config2-workspace-roots-override-…`, two Config2 refusals, precedence,
backslash grammar).

Join to confirm: Codex (Config2 owner) — `discovery.workspaceRoots` items are
root-relative logical paths with the S3 grammar; native (U1) — units feed the
per-language program membership, not the custody root.

### MUST S4.5 — counters and freshness

- **Counters: exact equality** to the challenged record (design selection:
  simplest). A higher signed counter refuses `COUNTER_MISMATCH:<k>` with the
  remedy "import the ordinary payload carrying it, then re-challenge". Nothing
  is silently discarded or advanced. Model and contract agree; the sweep
  checks ±1 on every counter.
- **Freshness**: pending challenge is single-boot (`bootId`) with
  `createdMono`/`expiresMono = +24 h` (sleep-inclusive monotonic). Import
  requires same boot, `createdMono ≤ mono ≤ expiresMono`, `issuedAt ≥ L`, and
  `|issuedAt − wall| ≤ 24 h` (both directions). A reboot invalidates the
  challenge. An old pending response can no longer lower the floor to stale
  real time.
- **Threat statement** is explicit in S4.5: wall distrust, what the protocol
  bounds, and no promise against a malicious recovery signer.
- **Strict schemas before comparisons**: `_epoch_shape` and `_pending_shape`
  run first; integers are exact (`_int` rejects bool); constants compared by
  type and value; the checker's foundation exact validator rejects `true` for
  `const 1`. Cases: boolean `epochSerial`, boolean counter, `recoverySchema:
  true`, bad `issuedAt` grammar, pending record without boot binding.
- **Authority changed to `recoveryAuthority`** (see "Design choice that Codex
  may object to" below).

Cases: 11 new apply cases; sweep
`recovery-epoch-applies-once-replay-counter-mismatch-reboot-and-window-refuse`
(19 checks).

### MUST S9/S4/S8 — root schema 2, profile-set binding

Authored in S9.1 and the schema bundle:

- `RootV1` reproduces the v8 `root.schema.json` rule set unchanged.
- `RootV2` is the exact extension recipe: `rootSchema` const 2; `roles` gains
  required `TR-PROFILE`; TR-REPAIR/TR-PROFILE may be active with threshold ≥ 2,
  keys ≥ threshold + 1, namespaces non-empty; `kernelAttestationKeys` 0..8;
  no key reuse across rootKeys/recoveryAuthority/roles/kernel keys; digest
  domain `opensip.metadata.root.2`; signers as S5.
- Envelope kinds and preimages are a closed table (root, catalog, revocation,
  trust-recovery-epoch, platform-profile-set), each a metadata-profile digest
  under its domain; `bodyDigest` must match before authority.
- Publish/reader compatibility: schema-1 readers refuse schema-2 roots typed
  (`ROOT.SCHEMA_UNSUPPORTED`, never corruption; sweep over all fixtures ×
  reader sets); a standalone profile set under a schema-1 root is refused
  typed and only the core-embedded copy is used; under schema 2 the
  TR-PROFILE threshold admits standalone sets.
- Machine-readable input admission: `admit_root_document`,
  `admit_profile_set_envelope`; `root-schema-cases.v1.json` (16 root cases,
  8 envelope cases, including `rootSchema: true`, `envelopeSchema: true`,
  key reuse in three directions, 9 kernel keys, TR-PROFILE threshold policy).

Release-side qualification of the signing ceremony remains future; the design
is closed.

### MUST S10 — grant join

`RepoExecutionGrantV2` replaces the never-accepted V1 (retained in the bundle
as superseded, admitted by nothing):

- Principal mapping table in the model: `P-TRUSTED-REPO` (workflow display)
  and `repository-code` (native class) → foundation semantic-grant kind
  `trusted-repository-code`. `semanticGrantDigest` (plan2 projection) and
  `securityGrantRef = H("security.repo-execution-grant.v2", grant)` are
  separate identities; admission requires the projection to carry the same
  principal, `toolClosureId` and `ownerSourceDigest`.
- Owners bind `{ownerKey, source, ownerFileManifestSha256}` from the sealed
  snapshot **or** the sealed `DependencySourceSetV1` (external crates' build
  scripts / proc-macros), with exact manifest-digest validation and
  `dependencySourceSetId` equality. Runner is a sealed tool-closure member
  (bundled cargo/rustc/linker/test runner); test-runner may also use a sealed
  snapshot member. No system fallback: `/usr/bin/cargo` refuses.
- Workflow test fields aligned concretely: `authorizationRef` = securityGrantRef,
  `consentSource` ↔ authorization mode, `argv0Source` ↔ `runner`; `ci` must be
  a real boolean (`ci: 1` is a shape refusal).
- **S10.1 `RepairApplyAuthorizationV1`**: repair apply is host-brokered
  first-party source mutation, not a repo-execution grant. Binds project,
  `repairPlanId`, `baseSnapshotId`, `recipeClosureId`, consent, expiry
  operation-end, `leaseMode: EXCLUSIVE`, `repositoryExecution: false`
  (constant; `true` refuses). Live revocation via S6 authority checkpoint;
  revoked recipe closure → `EXTENSION.ADMISSION_REJECTED`. Identity is the
  workflow `RepairApplyParams.authorizationRef`.

Cases: 36 grant cases, 13 repair cases.

Joins to confirm: native (being revised) — `AuthorizedExecutionV2.owners[]`
must carry `source` and match this grant's owners; `toolClosure` must expose a
`closureId` (`closure2:`) and member list. Workflow — none blocking; the
`test-execution.schema.json` description should say V2.

### SHOULD S7 — one-writer refinement, backup custody

S7 now states the identity-§5 refinement with exact selectors (writer.lease =
"lifecycle lease", readers.lease = "consistent committed snapshot", fence =
"trust admission lock order"), why EXCLUSIVE needs a reader census, and a
command → lease map in which `trust recovery-challenge|import`, install/update
and doctor take no project lock. S3.1 joins TM V17 as an admission step
(`storage_write_admission`, 8 cases): `--ephemeral`, `--allow-backup-custody`,
or an admitted policy record; CI refuses `storage.backup-choice-required`; no
policy file written, no root identity changed.

### D9

No new class, code or exit. New typed details (`COUNTER_MISMATCH`,
`CHALLENGE_*`, `ROOT.*`, `ENVELOPE.*`, `PROFILE_SET.*`, `GRANT.*`, `AUTHZ.*`,
`storage.backup-choice-required`) map to the existing classes 2/3/4 exactly as
before; S12 table updated. Doctor remains report-only, `writes: []`, no clock
write, no challenge creation (unchanged cases).

## Design choice that Codex may object to

The v1 chapter said the recovery epoch is signed by the accepted root's
`rootKeys` at `rootThreshold` and "there is no other quorum". The preserved
schema-1 root already carries `recoveryAuthority` (5–16 keys, threshold ≥ 3,
disjoint from rootKeys) with no consumer in v8. v2 makes `recoveryAuthority`
the epoch signer and excludes root keys entirely: routine floor recovery never
exercises root keys, and root-key compromise alone cannot lower a floor. If
Codex prefers root quorum, the change is one line in `recovery_apply` and the
fixtures' signer lists; the rest of S4.5 is unaffected. This is flagged, not
hidden.

## Candid limits (unchanged in kind)

- All signer sets, nonces, boot ids, monotonic values and OS custody reads are
  asserted model inputs; nothing is measured or cryptographically verified.
- Expectations are same-author; no independent oracle.
- OS qualification (O_NOFOLLOW/ACL races, sleep-inclusive monotonic across
  suspend, fsync-ordered floor writes, flock semantics, process-group kill,
  migration crash points, signing ceremony) stays under the existing gates.
- `RootV2` is the design schema; the release successor of
  `security-schemas.v8/root.schema.json` must be byte-derived from it.
- Foundation `canonical.py`, `identity-and-evidence.md` and
  `test-execution.schema.json` changed since the v1 pins (foundation is under
  independent review); pins were refreshed to the bytes present at this
  handoff and the checker exits 2 if they move again.

## Files changed in this handoff

- `security-and-lifecycle.md`: S3 (units, S3.1), S4.5, S7, S9.1, S10, S10.1,
  S12, S13, standing.
- `security/security_lifecycle_model_v1.py`, `security-lifecycle.schemas.v1.json`
  (bundle v2), `check-security-lifecycle.v1.py`, `source-pins.v1.json`,
  `security-lifecycle-report.v1.json`, `README.md`,
  `initial-author-response.json` (v3).
- Cases: `discovery-cases.v1.json`, `trust-recovery-cases.v1.json`,
  `execution-principal-cases.v1.json` (rewritten for V2); new
  `repair-authorization-cases.v1.json`, `root-schema-cases.v1.json`,
  `storage-write-cases.v1.json`.

NOT SELF-ACCEPTED. Codex re-reviews these bytes; a fresh Claude session
reviews the integrated package.
