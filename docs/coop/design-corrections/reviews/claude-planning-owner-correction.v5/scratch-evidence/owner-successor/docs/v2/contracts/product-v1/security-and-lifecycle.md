# Security and lifecycle: boundaries, time, trust, platforms, migration, concurrency

Standing: product successor authored and corrected by actual Claude, Codex and
actual Grok. Review and D-372 application standing is governed by the
[correction record](../../../coop/design-corrections/README.md) and central
readiness register. Historical acceptance applies only to its frozen bytes. It
addresses AR-03, AR-04, AR-05, AR-06, AR-14 and the offline/doctor part of
AR-16, the nine items of Codex's intermediate review of the earlier draft, and
the CHANGES_REQUIRED items of Codex's review of the final chapter (handoff
`reviews/security-fix-handoff.v2.md`: S3 units, S4.5 counters and freshness,
S9.1 root schema 2 / profile-set binding, S10 grant V2 and S10.1 repair
authorization, S7 one-writer refinement and backup custody).
Reference evidence: [security/](../../../coop/design-corrections/security/)
(model, closed schemas, cases, checker, report, source pins). Reference checks
are design evidence over synthetic fixtures; they are not OS measurement,
cryptographic verification or product qualification. Every boolean signature or
OS observation consumed by the model is a stated TCB assumption.

## S1. Authority, applicability and superseded selectors

The first-party host is the only authority for discovery, trust time, root
chain acceptance, revocation, platform admission, migration and leases. Content
identity never proves custody. A signed document proves only that its signer
signed those bytes; whether the document is admitted is decided by the rules
below, evaluated at the host's trust instant. Detector compatibility listings
inherit tree, platform and protocol from the already-admitted `closure2`, not
from fields on the listing body. Identity §3 hashes `closure2` over `{kind,
manifestDigest, tree, semanticVersion, protocolMajor, platform}` and states that
a component manifest for a different tree, platform or selected component is
refused by delivery admission. That delivery selector is DR-103
`component-manifest-schemas.v11` `manifestSchema.platforms[]` (`os`, `arch`,
`tree` TreeCommitment, `entrypoint`) together with RJ-3, not `DetectorManifestV1`.
Authenticated association of those component-manifest bytes is the existing
envelope (`opensip-signature-envelope.2` subject `kind=manifest`, domain
`opensip.metadata.manifest.1`, `storedSha256` equal to identity
`closure.manifestDigest` raw-artifact) plus catalog `opensip-catalog.1`
`releases[]` `{manifestDigest, manifestPreimageSha256, envelopeDigest,
artifacts[{platform, archiveProfileId, archiveDigest, sha256}]}` signed TR-INDEX.
Workflows-and-surfaces §2 then admits **that** `closure2` from a retained
generation, an installed signed release with the same `closure2`, or a signed
`closureBundle`. Identity `closure.tree` projects that selected platform
TreeCommitment onto regular files only: each `type=file` entry maps to one
identity `Blob` `{path, sha256, bytes}` with the same path string,
`sha256=entry.sha256`, `bytes=entry.length`, and retained blob length matching
(`BLOB_LENGTH`); `type=dir` and `type=symlink` stay delivery rows, are not
identity Blob members, and are never followed into a listing (RJ-3 keeps
symlink targets inside the tree). Mode bits remain on the TreeCommitment row
and are not identity members; listing bytes are never executed. `DetectorManifestV1`
is only `{schemaFamily, schemaMajor, compatibleClosures}` (`additionalProperties`
false); it cannot be the component-manifest preimage and must not occupy
`closure.manifestDigest`. The listing is the optional unique reserved regular-file
path `.opensip/detector-compatibility.json` in that already-admitted same
`closure2` tree (exact NFC path; not the project-host `.opensip/project-id.v1`
custody marker). Path absent is no declaration; empty `compatibleClosures` is a
complete declaration; a present path that is not `type=file`, whose
Blob/length/digest disagrees with the TreeCommitment file row, or whose retained
bytes fail the existing W listing schema, refuses and does not downgrade. Tree,
path or digest swap fails closure or delivery admission; catalog digest match
alone never admits. After that association the host projects a closed receipt
`{closureId, componentManifestDigest, listing, trustOrigin, compatibleClosures,
tree, platform, protocolMajor}` only when the reserved file is present and
valid. `listing` is its exact Blob `{path, sha256, bytes}`;
`componentManifestDigest` is the admitted closure's `manifestDigest`, and
`trustOrigin` is `retained-generation` | `installed-signed-release` |
`signed-closure-bundle`. The other fields copy the same admitted closure and
listing. Path absence produces no compatibility projection; an empty listing
produces a projection with `compatibleClosures: []`. This is not a second
signature verifier, listing schema or `signatureVerified` flag. Workflow
`host.closures[].trust='admitted'` is a TCB fixture assumption, the same class
as `verify_envelope` already-accepted signers, not that delivery selector.

Prospectively replaced selectors (historical bytes stay immutable):

| Reviewed source | Selector | Disposition |
|---|---|---|
| security v8 §4.2 and `security_unit_lib_v8.evaluation_time` | write-ahead `evalHighWater = max(recorded, wall, lastAccepted)` before evaluation | replaced by S4 (plausibility refusal before evaluation; floor written equals evaluated instant) |
| security v8 §4.8 `doctor_trust_report` | report-only evaluation | retained; S4 adds that report-only returns no actionable write fields and no challenge |
| security v8 §5.5 | restore keeps floors; no floor recovery | retained; S4.5 adds the only lawful floor-lowering act |
| security v8 §5.4 fence/lease handoff | one operation lease, non-blocking | refined by S7 (three lease modes, five-level lock order) |
| security v8 §8.3–8.7 | one measured profile per platform class | replaced by S8 (population with two tiers, four lanes) |
| host foundation v2 §§1–3 discovery | nearest-ancestor `opensip.json` walk to `/` | replaced by S3 |
| compatibility matrix v5 S-STATE/S-CTRL/S-SCHEMA | closed major one, no bridge | retained for stage 1; S9 is the explicit stage-2 successor |
| journal-record.schema v8 | GRANT/RA/ICI/RCI/ICO/RCO/REV/CLN/AUD | retained as historical bytes; schema-2 records added SEAL and `postimageSha256` (S6). **Current** product journal records are `recordSchema` 3 with `run3`. Schema-2 journals remain frozen historical bytes and are not read as 3. The bundle filename `security-lifecycle.schemas.v1.json` is not the record version. Grant tokens and root compatibility schema 2 are a different axis and stay. |

Unchanged inherited constants: 24 h future tolerance, 90 d revocation freshness
and catalog expiry, 365 d root expiry, expiry boundaries (`expired iff tEval >=
expiresAt`; `stale iff tEval > issuedAt + 90 d`). No D9 class, code or exit is
minted; every refusal maps to an existing D9 v1.14 code (table in S12).

## S2. Two canonical profiles, never mixed

Signed security metadata (root, catalog, revocation, journal records, recovery
challenge and epoch, platform profile population) stays under
`opensip-metadata-canonical.1`: NFC-required strings, i64 integers, its own
domain-framed digests. Product data (discovery provenance, decision records,
execution grants, everything with a `schemaVersion`) uses the foundation
canonicalizer of identity-and-evidence §3: no normalization, integers to
2^64-1, `H(domain, descriptor)`. A decoder for one profile never admits the
other's documents. The reference checker demonstrates the separation with a
decomposed string and an integer above i64 (sweep `metadata-nfc-profile-and-
product-profile-never-mixed`).

## S3. Discovery and custody (AR-03)

Discovery is deterministic over lstat/ACL results obtained through O_NOFOLLOW
handles: no environment variable, no `PATH`, no `HOME` (the account home comes
from the account database). Output is the closed `DiscoveryProvenanceV1`.

The disposable discovery instrument accepts only its named host-observation keys:
required `invokingUid`, `accountHome`, `cwd`, `fs`; optional `ci`,
`trustProjectOwner`, `authorizedGroupIds`, `explicitProject`, `explicitResolved`,
`explicitJoins`, `configWorkspaceRoots`. Unknown/missing keys or wrong outer
scalar/container types are `DISCOVERY_OBSERVATION_SHAPE` instrument errors,
not public D9 input refusals. Boolean observations are exact booleans and uid/gid
observations are nonnegative integers, never coerced strings or booleans. The
lstat/ACL map remains a synthetic trusted observation, not proof of native custody.
Public invocation/configuration admission still precedes this host-only seam.

**Custody of a directory** passes only if: it is a real directory (no symlink);
owner is the invoking uid or root; mode has no other-write bit; mode has no
group-write bit unless the directory's gid is in the explicitly authorized set;
no ACL write grant (POSIX ACL on Linux, `acl_get_fd_np` on macOS) to any
principal other than the invoker, root, or an authorized group; and the ACL was
readable. Mode bits alone never establish exclusion. **Custody of a config
file** adds: regular file, link count 1, at most 4 MiB. Group authorization
exists only through an explicit `--trust-group <gid>` invocation argument and
is recorded in provenance; configuration cannot grant it. `--trust-project-owner`
waives only the owner check and only with an explicit `--project` path.

**Walk rule.** With `--project`, the resolved path is examined exactly once
(symlink resolution recorded). Otherwise, from the launch directory upward, at
most 256 levels: a custody failure at the launch directory refuses
(`PROJECT.ROOT_CUSTODY_REFUSED`); a custody failure at an ancestor is a
boundary and that ancestor is never examined for a config. At each passing
directory the config, if present, is custody-checked (failure refuses
`CONFIG.CUSTODY_REFUSED`; it is never skipped) and selects that directory
(`mode: config`). Boundaries after a directory without config, in precedence:
VCS marker (`.git`, `.hg`, `.svn`, `.jj`), account home, filesystem root, mount
change. A VCS boundary selects **that repository root** (`mode: vcs-default`),
never the launch directory, so default scope does not change with launch
directory. Home, root, mount and custody boundaries without any candidate
select the launch directory (`mode: cwd-default`).

**Nested config is a deliberate project boundary (decided; ADV-3).** A config
file found below a VCS root is an author-declared project root and wins for
launches inside it; the walk never continues above a config. The enclosing
VCS-root project treats that directory exactly like a nested repository: it is
recorded in `nestedProjects`, automatic discovery never enters it (excluded
unit reason `INSIDE_NESTED_PROJECT`), and an explicit join crossing into it
refuses `PROJECT.EXPLICIT_PATH_INVALID` (`JOIN_CROSSES_NESTED_PROJECT`). Scope
therefore depends only on which project a launch is inside, never on which
directory of one project. The alternative (VCS root always wins) was rejected
because it would silently ignore a config the repository author placed. Cases
`nested-config-inside-a-vcs-root-*` and
`explicit-join-crossing-into-a-nested-project-refuses`.

**VCS data.** A `.git` indirection file (`gitdir:`) is data: its target is
recorded and never followed by discovery; VCS digests for the snapshot are the
identity unit's concern and read only inside custody.

**Authority roots versus workspace units.** Two different things are
distinguished. A *project authority/custody root* is the selected root: one
custody domain, one ProjectId, one lease namespace. Repositories nested under
it are other custody roots: they are recorded as `nestedRepositories`, never
entered, and reachable only by their own `--project`; a join that crosses into
one refuses `PROJECT.EXPLICIT_PATH_INVALID` (`JOIN_CROSSES_NESTED_REPOSITORY`).
A *language workspace unit* is a directory inside the admitted root that
carries a manifest marker: `Cargo.toml`, `package.json`, `tsconfig.json` or
`jsconfig.json` (markers may co-locate; a unit lists all its markers). Units are
discovered **automatically** for the zero-config full product, with precedence:

| Source | Provenance `unitSource` | Custody failure |
|---|---|---|
| repeatable CLI `--workspace-root PATH` overrides | `explicit-joins` | refuses (explicit intent) |
| admitted Config2 `discovery.workspaceRoots` (foundation product-configuration schema v2) | `config-workspace-roots` | refuses |
| marker scan of the admitted root | `automatic` | unit excluded, recorded in `excludedUnits` with the reason |

An explicit source suppresses automatic discovery. Every directory from the
root to a unit must pass directory custody and stay inside the root (no
absolute, `.`, `..`, backslash or NUL segments); every marker file must pass
file custody. A manifest is **data**: discovery records its presence and later
readers parse it as data only, never running scripts, hooks, plugins or
workspace globs and never writing source.

**One shared discovery rule (MUST-3).** The zero-config rule is stated once, in
`docs/coop/design-corrections/discovery-defaults.py`, and consumed by this
instrument and by the native unit instrument (native §1.4); neither restates
it. Before any custody walk, automatic discovery prunes, by **exact path
segment** (never substring): dependency trees (a segment `node_modules`), VCS
trees (`.git`, `.hg`, `.svn`, `.jj`) and Cargo build output (a segment
`target` whose parent directory holds `Cargo.toml`, an actual Cargo root; a
source directory merely called `target`, such as `packages/target` or
`src/target`, is ordinary source). A pruned tree yields no unit, no marker,
no custody walk and no program member; its anchor is recorded **once** in
`prunedTrees` with the number of markers it hid, so 4200 installed package
manifests are one record, never 4200 units. A `Cargo.toml` inside a pruned
tree does not create a Cargo root. First-party unit directories are capped at
4096; exceeding the cap refuses typed `PROJECT.WORKSPACE_UNIT_LIMIT` (D9
`REQUEST.UNSATISFIABLE`, detail `WORKSPACE_UNIT_LIMIT:<n>><cap>`) with no
truncation; installed dependencies never count toward it (checker sweep
`discovery-prunes-installed-dependencies-and-refuses-real-cap-typed`: 4200
installed manifests admit with one unit; 4200 first-party directories refuse;
exactly 4096 admit).

**Explicit roots are exact roots.** CLI `--workspace-root` and Config2
`discovery.workspaceRoots` values are normalized by the shared
`normalize_explicit_root`: `.` alone denotes the admitted project root
(identity-and-evidence §3 sentinel; internal root ``, the same value the native
instrument uses), one trailing `/` is dropped from a CLI value (a Config2 value
spelled with a trailing `/` is refused earlier by the foundation
product-configuration resolver's logical-path grammar and never reaches either
instrument; case
`cli-workspace-root-with-trailing-slash-normalizes-like-the-native-instrument-config2-refuses-it-earlier`),
and any other empty, `.`, `..`,
absolute, backslash or NUL segment is `JOIN_PATH_GRAMMAR`. An explicit root
inside a pruned tree refuses `JOIN_INSIDE_PRUNED_TREE:<reason>:<anchor>`. An
explicit root **without a language marker** is admitted here for custody (unit
recorded with `markers: []`, warning
`EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER:<path>`) and refused by the language-unit
layer as `CONFIG.INVALID` / `native.explicit-root-without-marker` (native
§1.4); the invocation terminates typed with this provenance retained. That is
the selected behaviour: custody admission and language-unit existence are two
different facts, and neither instrument normalizes the same value differently.
Custody-excluded units are explicit unknown required scope, not a successful
empty scope; later syntax scanners cannot read their uncustodied source. There is
no config "project list" and no duplicate `--project` implicit multi-project
mode: `discovery.workspaceRoots` is the only configuration carrier. Cases
`installed-dependencies-and-cargo-build-output-are-pruned-by-segment-*`,
`config2-workspace-root-dot-*`, `explicit-root-*`.

**Pruned trees and the read set (A-5).** "No custody walk" for a pruned tree
means discovery neither enumerates units in it nor walks its directories for
custody. Bytes a language program later reads from such a tree (a TypeScript
resolution reading `node_modules`, native §2.2/§9.4) enter the snapshot read
set through the identity unit's snapshot custody, are Plan-bound like every
other read-set byte, and are never a discovery unit; they are not exempt from
custody, they are custody-checked by the snapshot reader instead of the
discovery walk.

**Admitted boundary inventory for the language-unit instrument (decided; post-reset
v2 N-1/P3).** The native unit instrument (native §1.4 U-8) never re-derives a
project boundary from caller input. After an `ACCEPT`, the host calls
`boundary_inventory(result)`, which converts this instrument's absolute custody
locators (`nestedRepositories`, `nestedProjects`, custody/depth `excludedUnits`,
`prunedTrees`) into the closed `AdmittedBoundaryInventoryV1` of relative scope
paths under the selected root (shared implementation
`discovery-defaults.boundary_inventory_from_provenance`; one boundary prefix
rule `classify_boundary` is used by both instruments). The host passes that
record unchanged to native `discover_units`, `assign_membership` and
`unit_scope_descriptor`; the native instrument then yields exactly this
instrument's unit set, excludes every marker directory and file at or below a
boundary, refuses an explicit root crossing one (`native.explicit-root-crosses-boundary`,
the counterpart of `JOIN_CROSSES_NESTED_*`) and enters every boundary anchor
into the Plan scope descriptor's `excludedPathPrefixes`. An inventory whose
pruned trees do not equal the ones the native instrument derives from the same
marker inventory is refused (`native.boundary-inventory-mismatch`): a
caller-supplied ignore list is never proof of boundary completeness. A `REFUSE`
result exports nothing. Cases `boundary-inventory-*`; checker sweep
`admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`
runs the P3 fixture through both instruments. **The integration join is implemented, not owed:**
`integration-host-model.py` `admit_repository_discovery` composes `discovery` →
`boundary_inventory_from_provenance` → native `discover_units`/`assign_membership`/
`unit_scope_descriptor`, and `check-integration.py` asserts it
(`host-nested-boundaries-admitted-once`, `-no-native-units`, `-no-source-capture`,
`-plan-visible`, `host-native-inventory-substitution-refused`,
`host-launch-inside-nested-config-selects-that-project`, plus
`security-native-shared-unit-roots` and `security-native-shared-pruned-trees`).

Native custody obligation (qualification, not modelled): ACL reads, O_NOFOLLOW
handle reuse for the later read, and re-check of `st_dev/st_ino` between lstat
and open. A change between them is a refusal, not a retry.

### S3.1 Backup custody before the first source-derived write

Identity-and-evidence §5 (TM V17) is joined here as an admission step, not a
prose promise: when the storage root is classified **detected backup-managed**
(`BACKED_UP`), the first source-derived write needs an explicit choice, in this
order: `--ephemeral`; `--allow-backup-custody` for this invocation; or an
already-admitted host storage-policy record. CI never prompts and refuses
`REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`. **UNKNOWN
admits** with a mandatory disclosure (`unknown-disclosed`): it is never
rendered as not-backed-up and it never requires the choice (fixture
`unknown-backup-status-is-not-not-backed-up`, identity §5, the inventory flag
joins and the S13 addendum agree). The choice writes no policy file and changes
no root identity (ProjectId, namespace locator). Sync/shared/upload storage
classifications are independent checks. Reference `storage_write_admission`;
fixture `storage-write-cases.v1.json`.

## S4. Trust time (AR-04)

Definitions. `evalHighWater` (floor F): highest instant at which a decision
evaluation was made. `lastAccepted` (L): issue time of the newest accepted
signed document; required whenever F exists. **Admitted time evidence** A =
max(L, accepted witness time, presented root issue time), where a witness is
the newest issue time of a presented payload whose signature already verified
and which is not older than L. The wall clock is untrusted.

Decision evaluation, in order, for record R, observation (wall W, sleep-
inclusive monotonic M, bootId B), optional payload P:

1. Payload future check (unchanged FC-FUTURE): an issue time > W + 24 h refuses
   `PAYLOAD-NOT-ADMISSIBLE`; nothing is written.
2. Fresh install (F absent): without admitted time evidence the evaluation
   refuses `TRUST.NO_ADMITTED_TIME_CONTEXT` (the core's embedded bootstrap
   payload or an ordinary payload is required); nothing is written. With it,
   W > A + 90 d refuses `CLOCK-EXCURSION-FORWARD` and initialises nothing.
   Otherwise tEval = max(W, A); F := tEval, L := A, anchor := (B, M, W); expiry
   states are evaluated from the presented documents, never set to false.
3. In-session continuity: if the anchor has the same bootId, expected =
   anchorWall + (M − anchorMono). A forward deviation over 24 h refuses
   `CLOCK-EXCURSION-FORWARD` (`in-session`) unless a witness proves the
   expectation itself was behind (witness ≥ expected). A backward deviation is
   the finding `CLOCK-REGRESSION-IN-SESSION`; a monotonic value below the
   anchor's is `CLOCK-CONTINUITY-MALFORMED` (finding, anchor not rewritten).
4. Plausibility: W > A + 90 d refuses `CLOCK-EXCURSION-FORWARD`
   (`beyond-horizon`) **before any evaluation and before any write**. Remedy:
   correct the clock, or present a payload issued within 90 d of W.
5. Evaluation: tEval = max(F, W, A). The floor written is exactly tEval
   (write-ahead, §5.6 durability), so the persisted floor and the evaluated
   instant never differ and no later evaluation runs earlier than an earlier
   one. `CLOCK-REGRESSION` (W < F) and `TRUST.FLOOR_AHEAD_OF_WALL`
   (F > W + 90 d) are findings with remedies. L advances to A when A > L. The
   anchor is rewritten when continuity is unavailable, within tolerance, or
   excused by a witness.

Consequences. An accidental forward wall is accepted only up to 90 d beyond
signed evidence, so a wrong write is bounded and heals as signed time catches
up; a larger jump writes nothing. Expiry, staleness and future checks still
fail closed at tEval. Repeated reboots cannot lower F or freeze payload
freshness: F only rises, and freshness is evaluated at tEval ≥ F. Report-only
evaluation (doctor) computes the same decision, states and findings, labels
`evaluationMode: report-only`, and returns `writes: []` with every write field
null; it cannot create a recovery challenge.

### S4.5 Recovery of an already poisoned floor

A floor years ahead of real time (written by the superseded rule, or by a
restore) cannot be lowered by ordinary payloads: tEval ≥ F keeps every document
expired. Recovery is an authenticated, install-bound, single-use act:

1. `opensip trust recovery-challenge` (decision mode only; global fence, no
   project lease) writes one pending challenge and exports
   `trust-recovery-challenge.v1.json` (`TrustRecoveryChallengeV1`): a fresh
   32-byte host-CSPRNG nonce, `createdWall`, and `recordDigest` =
   metadata-profile digest, domain `opensip.metadata.recovery-challenge.1`,
   over the six bound fields `{evalHighWater, lastAccepted, rootVersion,
   revocationVersion, indexSnapshotVersion, recoveryEpochSerial}`. The
   pending record additionally binds `{bootId, createdMono, expiresMono =
   createdMono + 24 h, createdWall}` with sleep-inclusive monotonic time. A
   new challenge replaces the pending one; a reboot invalidates it.
2. The publisher's recovery service (consented online) or the air-gap ceremony
   returns `trust-recovery-epoch.v1.json`: an `opensip-signature-envelope.2`
   of kind `trust-recovery-epoch` (digest domain
   `opensip.metadata.recovery-epoch.1`) with body `TrustRecoveryEpochV1`
   `{recoverySchema:1, kind, epochSerial, issuedAt, challenge{nonce,
   recordDigest}, counters{rootVersion, revocationVersion,
   indexSnapshotVersion}, installBinding:"challenge"}`. Authority is the
   **accepted root's `recoveryAuthority.keys` at `recoveryAuthority.threshold`**
   (the existing schema-1 field: 5–16 keys, threshold ≥ 3, disjoint from
   `rootKeys`), revoked keys excluded. Root keys never count, so routine
   recovery never exercises root keys and root-key compromise alone cannot
   lower a floor. The accepted root's expiry is not consulted for this one
   document because the floor under repair is what expired it. This is the
   only external artifact needed.
3. `opensip trust recovery-import` verifies, under the global fence and no
   project lease, in this order: (a) **strict closed shape of the epoch and of
   the pending record before any comparison** (exact-typed constants: `true`
   is never `1`, integers are never booleans, timestamps by grammar, hex by
   grammar); (b) recovery-authority threshold; (c) a pending challenge exists,
   its `bootId` equals the current boot, and `createdMono ≤ mono ≤
   expiresMono` (`CHALLENGE_BOOT_CHANGED`, `CHALLENGE_EXPIRED`,
   `CHALLENGE_CONTINUITY_MALFORMED`); (d) nonce equals the pending nonce;
   `recordDigest` equals both the pending value and a fresh digest of the
   current record; `epochSerial` > `recoveryEpochSerial`; (e) **every counter
   equals the challenged record's counter exactly** (`COUNTER_MISMATCH:<k>`).
   A higher signed counter is refused with that typed detail; the remedy is to
   import the ordinary payload that carries it and re-challenge. Nothing is
   silently discarded and nothing is silently advanced. (f) `issuedAt` ≥ L and
   |`issuedAt` − W| ≤ 24 h (`ISSUED_IN_FUTURE`, `ISSUED_TOO_OLD_FOR_WALL`).
   Any failure refuses `RECOVERY.REFUSED` with the typed detail and changes
   nothing.
4. On success: F := L := `issuedAt`; anchor cleared; `recoveryEpochSerial` :=
   `epochSerial`; pending challenge consumed; audit record `RECOVERY-EPOCH`
   with the previous floor. Counters, revocation entries, role states,
   journals and namespaces are untouched; no namespace is deleted.

Threat statement. The wall is untrusted. The single-boot, 24 h monotonic
challenge window plus the ±24 h issue skew mean that no response to an old
challenge, held indefinitely, can later lower the floor to a stale real time:
after a reboot or after the window the response is dead, and inside the window
the signed time must sit within a day of the wall the operator is looking at.
This bounds a signed epoch relative to the wall; it does not prove the wall.
The protocol promises install binding (nonce + record digest), single use,
serial monotonicity, exact counter preservation and no floor below L. It makes
**no promise against a malicious publisher**: a recovery authority that signs a
false time is outside the protocol, exactly as it is for every other signed
time in this contract. Why this cannot revive revoked trust: revocation is by
counter and entries, which the epoch may not change; a key revoked before the
epoch cannot sign it; expiry is re-evaluated at signed real time, which is ≥
every earlier signed time, so a document genuinely expired at real time stays
expired. If the recovery authority is unavailable, recovery is impossible and
the install must be re-established by fresh install or authenticated adoption.
Migration and rollback (S9) never carry a pending challenge; the serial moves
forward with the other floors.

## S5. Root chain through expired roots (AR-05)

An install holding accepted root N evaluates a chain N+1..M link by link. Each
link needs the previous root's threshold from that root's keys (continuity)
**and** the new root's threshold from its own keys (possession), revoked keys
excluded from both. Semantic admission per link: reader supports the schema;
version and previous-version contiguity; not issued before its predecessor;
issue before expiry; root key policy. Intermediate expiry is never consulted;
the final root must be unexpired at tEval and not issued more than 24 h after
the wall. Any refusal leaves state unchanged and names the link. Success
advances the root counter to M and L to the final root's issue time. An expired
root with no chain refuses `ROOT.EXPIRED_NO_CHAIN` with the remedy of presenting
a payload carrying N+1..newest. Schema-1 readers refuse a schema-2 root as
`ROOT.SCHEMA_UNSUPPORTED` (typed, not corruption, state unchanged).

## S6. Live revocation (AR-05)

Trust epoch `{rootVersion, indexSnapshotVersion, revocationVersion,
permissionPolicyDigest}` is captured at operation start. **Authority
checkpoint:** every brokered effect request re-reads the epoch under the
journal append lock before its intent record. **Observer:** a tick every 5 s
reads the counter; if the last successful read is older than 10 s or the read
fails, the observer appends `REV(observer-fail-stop)` and cancels. These bounds
are implementation qualification obligations under OS scheduling assumptions
using `CLOCK_BOOTTIME` (Linux) / `mach_continuous_time` (macOS); they are not a
wall-clock guarantee inside a stopped process. A stopped process emits no
effects; on resume its first checkpoint or tick observes the stall and fail-
stops before any further effect.

The observation predicate revokes on a higher counter whose entries name the
closure (release, signing key, namespace, catalog snapshot) or on a policy
digest change that removes a required grant; unrelated changes are recorded as
drift; a lower counter never revokes (rollback is detected by the floor rules).

**Linearization** is under the single journal append lock: after `REV` no
`RA`, intent, commit or `SEAL` is appended, and no brokered effect commits.
Commit records carry `postimageSha256`. At `REV(trust-revoked)` the host
attempts rollback of reversible completed effects **only where the current
bytes equal the committed postimage**; a mismatch is `rollbackBlocked`
(user-modified since commit, never overwritten), an unreadable target is
`indeterminate`. Irreversible completed effects and effects under
`REV(policy|operator)` are disclosed as completed. The `CLN` record lists every
residual. Cancellation is bounded: refuse further requests (0 s), protocol
Cancel (2 s), SIGTERM (3 s), SIGKILL of the process group and reap (5 s),
scratch cleanup under the lease; total 10 s under the same qualification
standing. **Unconfined children** (repository code under S10) are not brokered
effects: they are cancelled within the bound and disclosed, and their external
effects before the kill are not enumerable. No confinement is claimed.

**Three different SEAL boundaries, not one.** (1) `linearize` is an abstract
brokered-effect schedule over a grant journal. Its all-zero `run3:` SEAL id is
a **fixture** token for that schedule. It is not a product host, not native
fact authority, and not `identity-model.v3.close_run`. (2)
`admit_seal_run_id_prefix` is narrow `run3` pattern dispatch. It admits a
well-formed non-fixture prefix and refuses `run2` and the fixture id. It does
not replay a graph. (3) `admit_analysis_seal` is the public reference SEAL of
an analysis Run: current `JournalRecord` fields (`recordSchema` 3, closed
required members), then `identity-model.v3.close_run` on the supplied retained
graph, then byte-equal RunId comparison. Owner-only `open_run_closure` is not
that boundary. A well-formed `run3:` that is not the replayed identity refuses
`SEAL_RUN_ID_MISMATCH`. Schema-2 journals remain frozen historical bytes and
are not read as 3. Mixed prefixes refuse. There is no `run[23]` alternation.
Revocation still blocks schedule-SEAL after `REV`. Grant/root schema-2
documents are a different axis. This dispatch does not change lease modes,
lock order, or permission-truth-table effect values. Proof
`executionInputsDigest` is required by identity reconstruct; this unit does
not mint it.

## S7. Leases and lock order (AR-14)

The current security schema bundle declares every array's `x-opensip-order`
under identity §3. Namespace lists use strictly unique raw UTF-8 locator order;
execution-grant owner records use strictly unique `ownerKey` order. Public code
sets use strictly unique UTF-8 order. Other arrays are explicit sequences unless
their owning schema states a stricter order: journal revisions, lock traces,
release steps, signature entries and observations are never silently sorted.
This collection-admission law does not change the security metadata canonical
profile or its immutable historical schemas.

| Level | Lock | Carrier | Blocking |
|---|---|---|---|
| 0 | lifecycle fence | `<installRoot>/lifecycle.fence`, flock LOCK_EX | bounded wait 5 s, then `PROJECT.BUSY` |
| 1 | project writer lease | `<namespace>/writer.lease`, LOCK_EX\|LOCK_NB | never |
| 2 | project reader lease | `<namespace>/readers.lease`, LOCK_SH\|LOCK_NB (readers); LOCK_EX\|LOCK_NB (EXCLUSIVE) | never |
| 3 | ledger transaction | SQLite WAL; writers BEGIN IMMEDIATE, busy_timeout 0; readers read a committed snapshot | never for readers |
| 4 | journal append lock | in-process mutex | bounded, in-process |

Modes: `SHARED-READ` (any number; queries, rendering, doctor, read-only
agents), `APPEND-WRITE` (one; analysis, import, baseline pin; publishes only
new immutable objects and ledger rows, never deletes or rewrites bytes a reader
may reference), `EXCLUSIVE` (GC, purge, migration, repair apply; nothing else
held). Readers never block a writer; a second writer or an EXCLUSIVE request
gets `PROJECT.BUSY` at once, releases the fence, and may retry outside the
fence with backoff 1/2/4/8/15 s within a 30 s budget. Laws: no lease without
the fence; no waiting for a lease; no waiting for the fence while holding a
lease (operation end releases the lease first); no upgrade; trust state is
written only under the fence and never under a lease; GC census is a
LOCK_EX|LOCK_NB probe under the fence and a busy probe means retain.

**One-writer refinement (identity-and-evidence §5).** "Exactly one per-project
writer holds the lifecycle lease through admission, evaluation and commit" is
the APPEND-WRITE mode: exactly one append writer, coexisting with any number of
immutable-snapshot readers that never wait on it. The EXCLUSIVE mode is the
refinement for migration, purge, GC and repair apply, which need a reader
census (the LOCK_EX|LOCK_NB probe) because they may remove or rewrite bytes a
reader could reference. There is no contradiction with the identity contract:
readers are invisible to the writer's commit order and the writer is invisible
to readers' snapshots. Exact selectors: `<namespace>/writer.lease` LOCK_EX|NB
is the identity contract's "lifecycle lease"; `<namespace>/readers.lease`
LOCK_SH|NB is its "consistent committed snapshot"; `<installRoot>/lifecycle.fence`
is its "global trust admission and revocation lock order".

**Namespaces.** Every project lease names a namespace from the host namespace
registry (ProjectId ↔ namespace locator, identity §5); a lease on an
unregistered namespace is a violation, never an implicit registration
(`lease-on-an-unregistered-namespace-is-refused-negative`). Namespaces are
independent: a writer in one never blocks a writer in another.

**Core-transition lock set (decided; SHOULD-6).** `core update|repair|rollback`
and `store migrate|rollback` change install-level state, while EXCLUSIVE is a
per-namespace lease. The mechanism is a composition, not a new flock mode:

1. The install-wide fence (level 0) is held for the **whole** transition, not
   only for lease acquisition; no project operation can be admitted meanwhile.
2. The affected namespace set is enumerated from the registry by
   `core_transition_affected_namespaces` (never from user input or a directory
   listing): **all registered namespaces** when the from/to state schema differ
   or a store is re-selected (`core rollback`, `store migrate|rollback`);
   **no namespace** for a same-schema `core update` or `core repair`, because
   the selected core closure is an immutable generation, running project
   operations keep their pinned generation and re-check trust at their S6
   checkpoints, and nothing they reference is rewritten.
3. EXCLUSIVE is taken on each affected namespace in namespace-locator byte
   order, non-blocking and all-or-nothing: the first busy namespace releases
   every acquired lease in reverse order, releases the fence, reports
   `PROJECT.BUSY` naming that namespace and its holders, and the retry is the
   ordinary backoff outside the fence.
4. The `InstallationTransitionJournalV1` (S9.2) names the exact lease set and is
   written only after every lease is held: in the lock model the
   `transition-journal` action is lawful only under the fence, only after
   `core-transition-acquire` succeeded, and only naming exactly the held set
   (`transition-journal-*` cases). Crash
   recovery runs as the first act under the next fence acquisition, before any
   admission, over the S9.2 recovery table (which defers to the S9 footprint
   table for store operations), and re-acquires exactly the journaled
   set; flock leases die with the process, so no stale lease survives. A
   namespace registered after the intent cannot exist (registration needs the
   fence); finding one is `MIGRATION.CORRUPT`.
5. Leases are released in reverse order, then the fence. The fence cannot be
   released while transition leases are held.

Ordinary component `install`/`update` publish new immutable generations under
the fence alone and never revoke a generation a live operation pins (removal
is GC census only). GC iterates registered namespaces and treats a busy
namespace as retain, never as refusal. Reference `lease_schedule` (registry,
`core-transition-acquire|release`, `transition-journal`),
`core_transition_affected_namespaces`; cases `core-transition-*`,
`transition-journal-*`, `two-namespaces-are-independent-*`.

Command → lease map (workflows command inventory):

| Lease | Commands |
|---|---|
| none (fence only, no project lock) | `install`, `update` (component generations), `trust refresh|import|recovery-challenge|recovery-import`, ordinary payload import, `doctor` / `trust doctor` / `store status` (report-only, no write) |
| SHARED-READ | `query`, `recommend`, `baseline show`, `policy show|test`, `candidates`, `inspect`, `review brief`, `repair preview`, `agent serve` reads, `doctor` project checks |
| APPEND-WRITE | `opensip` default, `analyze`, `fit`, `audit`, `import`, `baseline adopt|export|upgrade`, `policy init`, `waive`, `review join`, `test run`, `native prepare`, `repair verify` |
| EXCLUSIVE (one namespace) | `repair apply` (S10.1 authorization), `repair recover --apply-recovery` (S10.2 authorization; inspection alone is SHARED-READ), `purge`, `store gc` per namespace (busy = retain) |
| core-transition lock set (fence held + EXCLUSIVE on every affected registered namespace) | `core update`, `core repair`, `core rollback`, `store migrate`, `store rollback` |

Trust recovery deliberately takes no project lease: it mutates SC-TRUST only,
under the fence, and a project operation that starts afterwards observes the
new floor at its trust instant.

## S8. Platform population and admission (AR-06)

Selected support population (D-367 design selection) and its qualification
lanes (security v8 §8.7 classes). **One machine platform vocabulary (MUST-2):**
the `Platform id` column is the only machine identity, used unchanged as the
signed `PlatformProfileSetV1` key, the `platform` of every admission record,
`RepoExecutionGrantV2.platformId` and its truth-table key, the native matrix
`platformFamilies` (native §1.1), the workflow test-execution `platformId` and
the qualification-gate `platformFamilies`. The `Display alias` column is human
rendering only: an alias presented as a platform refuses
`NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:<id>`, a
profile set keyed by one is schema-invalid and refuses
`NT-TCB-PROFILE-UNQUALIFIED:PROFILE_SET_KEY_NOT_MACHINE_ID:<id>`, and a grant carrying one
refuses `GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID:<id>`.
`PROFILE_SET_KEY_NOT_MACHINE_ID` is **not** a public `DomainDetailCode` and must not be
registered as one: it is a **subject sub-detail** of the registered
`NT-TCB-PROFILE-UNQUALIFIED`, in the same position as
`platform-display-alias-not-machine-id`, `MACOS_MAJOR_26` and `DISTRO_SERIES` (S12). Lane names keep their
historical spelling; historical documents that use the aliases are unchanged.
The checker sweep
`one-machine-platform-vocabulary-joins-profile-set-admission-grant-native-matrix-and-workflow-schema`
admits every id through `platform_admit` and then a grant carrying that same
id, and checks the four id sets are equal across the units.

| Platform id | Display alias | Population | Lane |
|---|---|---|---|
| `macos-aarch64` | macos-arm64 | macOS 15 and 26, Apple silicon, sealed system volume, SIP on, APFS install root | `macos-15` |
| `macos-x86_64` | macos-x86_64 | macOS 15 and 26, Intel, same predicates | `macos-15-intel` |
| `linux-x86_64-gnu` | linux-x86_64 | Ubuntu 24.04 LTS, Canonical-signed kernels on supported lines/flavors, ext4/xfs/btrfs install root | `ubuntu-24.04` |
| `linux-aarch64-gnu` | linux-arm64 | Ubuntu 24.04 LTS on arm64, same | `ubuntu-24.04-arm` |

The signed `PlatformProfileSetV1` carries, per platform, the release-measured
identities from its lane (`EXACT-MEASURED` tier) and the supported baseline:
macOS supported majors with minimum builds; Linux supported kernel lines and
flavors. An identity inside the baseline but not measured is admitted at the
`BASELINE-ATTESTED` tier with its identity recorded as drift (never allow/
refuse). Security predicates are identical at both tiers: sealed root and SIP
(macOS); Ubuntu build string, kernel package installed by the Ubuntu maintainer,
archive key digest, mount-namespace stability, install-root filesystem; under
`secure-boot-lockdown`, Secure Boot on, lockdown not `none`, UEFI signer
present. A measured profile labelled with a lane outside its platform's lane
list is unqualified. Outside the population (other distributions, self-built
kernels, unsupported lines/flavors, non-listed filesystems, Windows) the core
refuses rather than degrades.

Honest limits, disclosed in every admission record: the baseline tier admits
identities no lane measured and does not detect a hostile kernel;
`package-db-declared` provides no boot attestation; macOS Full vs Reduced
Security is not distinguished at launch and boot policy is unobservable on
hosted lanes. Case values in the reference are placeholders, not measurements.

## S9. Stage transition, schema bridge and floor continuity (AR-14)

Bridge. Stage 1: root readers {1}, state decoder v1, TR-REPAIR typed absence,
`kernelAttestationKeys` empty. Stage 2: root readers {1, 2}, state decoders
`state-decoder.v1` (read-only migration source) and `state-decoder.v2`
(writer); schema-2 roots may carry an active TR-REPAIR (threshold ≥ 2, keys ≥
threshold + 1, namespaces present, no reuse of root keys) and up to 8 kernel
attestation keys (no reuse of root keys). Ordered release: (1) the stage-2 core
ships under the schema-1 catalog, so every stage-1 install updates by its
ordinary path; (2) root N+1 with schema 2 is signed by root-N keys and its own
keys; (3) stage-1 cores refuse N+1 typed and keep N until it expires; stage-2
cores accept it by the dual reader; (4) state migration 1→2 runs under
EXCLUSIVE. Both stages keep the metadata profile of S2.

Migration writes a `migrating` root: PREPARING → PREPARED → (old store fenced
`RESTORED`) → COMMITTED → final rename. Recovery from the durable footprint
only: absent = nothing to do; PREPARING or PREPARED with the old store unfenced
= abort; PREPARED with the old store fenced = resume from step 3; COMMITTED =
resume the final rename; final and migrating coexisting, or unknown state =
quarantine `MIGRATION.CORRUPT`. Floors (`rootVersion`, `indexSnapshotVersion`,
`revocationVersion`, `evalHighWater`, `lastAccepted`, `recoveryEpochSerial`)
copy forward into the new store; the boot anchor and any pending challenge do
not; roles re-establish by the PRESENT event over the embedded chain. A new core
whose embedded chain does not reach the accepted root refuses
`ROOT.FLOOR_ABOVE_CORE`. Rollback inside the 30 d window re-selects the retained
old store with floors set to the maximum of both stores; it refuses when the
new store accepted a root the old core cannot verify (schema or chain reach). A
poisoned floor is not lowered by migration or rollback; only S4.5 lowers it.

### S9.1 Root schema 2 and signed profile-set binding (design, closed)

**The product admission boundary is `security/security-lifecycle.schemas.v1.json $.schemas.RootV1`
and `$.schemas.RootV2`, reached only through `admit_root_document`.** No other document admits a
root. Root **schema 1** *preserves the rule set* of the historical
`docs/coop/completion/security-schemas.v8/root.schema.json`, which remains the immutable
**rule source** and is not a second gate. The successor is not byte-equivalent to it and is not
meant to be: every successor pattern ends with the strict `(?![\s\S])` assertion, where the
retained v8 patterns end with a bare `$`. Under Draft 2020-12 a bare `$` matches before a final
newline, so a root whose `indexOrigin.url` or whose role `namespaces` item carries a trailing
newline is admitted by the historical bytes and **refused** by the product boundary
(`PAYLOAD-NOT-ADMISSIBLE`, detail `ROOT.SCHEMA_SHAPE`, exit 2). That is the intended successor
semantics — the discipline is universal across the product-successor schema documents — and it is
regressed through the actual host gate, not through the schema alone, by
`root-schema-cases.v1.json` cases
`schema-1-root-with-a-trailing-newline-index-origin-url-refuses-at-the-product-boundary` and
`...-role-namespace-...`. Preserved semantic rules of schema 1 (`RootV1`: TR-REPAIR typed absence,
`kernelAttestationKeys` exactly `[]`, `recoveryAuthority` 5–16 keys at
threshold ≥ 3, disjoint from `rootKeys`). Root **schema 2** (`RootV2`) is the
exact extension recipe, and nothing else changes:

| Field | Schema 1 | Schema 2 |
|---|---|---|
| `rootSchema` | const 1 | const 2 (exact integer; `true` refuses `ROOT.SCHEMA_CONSTANT_TYPE`) |
| `roles` | exactly TR-CORE, TR-INDEX, TR-COMPONENT, TR-BUNDLE, TR-REPAIR | those plus **required** `TR-PROFILE` |
| TR-REPAIR / TR-PROFILE | keys `[]`, threshold 0, typed absence | may be active: threshold ≥ 2, keys ≥ threshold + 1, namespaces non-empty |
| `kernelAttestationKeys` | `[]` | 0..8 Hex64 key ids |
| key reuse | none across rootKeys / recoveryAuthority / roles | none across rootKeys / recoveryAuthority / roles / kernelAttestationKeys |
| digest domain | `opensip.metadata.root.1` | `opensip.metadata.root.2` |
| signers | previous root's `rootKeys@rootThreshold` and own | same (S5) |
| readers | stage-1 {1}; stage-2 {1, 2} | stage-1 refuses `ROOT.SCHEMA_UNSUPPORTED` (typed, state unchanged); stage-2 admits |

Signature envelope kinds (`opensip-signature-envelope.2`) and their preimages
are closed: `root` (body RootV1|RootV2, domain by `rootSchema`), `catalog` and
`revocation` (v8 bodies, TR-INDEX), `trust-recovery-epoch` (S4.5,
`recoveryAuthority`), `platform-profile-set` (body `PlatformProfileSetV1`,
domain `opensip.metadata.platform-profile-set.1`, signed by `TR-PROFILE` at
its threshold). Every preimage is the metadata-profile digest of the canonical
body under its domain; the envelope's `bodyDigest` must equal it before any
authority check. Publish/reader compatibility for the profile set: under a
schema-1 root there is no TR-PROFILE, so a **standalone** profile-set document
is refused typed (`ROOT.SCHEMA_UNSUPPORTED`, detail
`PROFILE_SET.NO_TR_PROFILE_ROLE`) and only the copy embedded in the signed
core release (TR-CORE namespace) is used; under a schema-2 root with an active
TR-PROFILE, standalone profile sets are admitted only as a transport for the exact set
pinned by the current admitted core release. The prospective signed core release
manifest schema2 carries required `platformProfileBinding: CoreProfileBindingV2`
with `platformProfileSetBodyDigest` equal to the metadata-profile body digest.
A stage2 reader ships under the old schema1 release first; only then can schema2
release manifests publish this required binding. The embedded and standalone
forms must match that same pin. A different or older set refuses
`PROFILE_SET.CORE_PIN_MISMATCH` even with a valid quorum. Updating the profile
set requires an ordinary signed core release update; it has no independently
mutable lifecycle or additional rollback floor. Reference
`admit_root_document` / `admit_profile_set_envelope` exactly validate the entire
closed input schema before semantic admission. `admit_root_chain` composes that
admission with chain verification; the older projected chain fixture primitive
is not a public admission boundary. Reference; fixture
`root-schema-cases.v1.json` (root and envelope input admission, positive and
negative). Release-side implementation qualification of the signing ceremony
stays future; the design is closed here.

### S9.2 Installation transition intent and journal (decided; post-reset v2 N-5/P10)

`core update|repair|rollback` and `store migrate|rollback` are five operations
of **one** installation transition protocol (S7 lock set, S9 store footprint,
S15 command grammar). One closed intent contract and one closed journal record
serve all five; the reference is `admit_transition_intent`,
`transition_journal_record`, `admit_transition_journal`,
`recover_transition_journal` (fixture `transition-journal-cases.v1.json`).

**Intent (`InstallationTransitionIntentV1`, the required field contract of the
workflow `CoreTransitionIntentV1` successor).** Eleven fields, host-projected,
never caller-authored: `schemaVersion` 1; `operation` (the five above);
`fromCoreClosure`/`toCoreClosure` (`closure2:`); `fromStateSchema`/`toStateSchema`
(1 | 2); `fromStoreGeneration`/`toStoreGeneration` (the selected state-store
generation); `platformProfileSetBodyDigest`; `preconditionGeneration` (the
observed core generation); `rollbackDeadline` (host-observed, or `null`). The
raw SHA-256 of the canonical intent is the mutation step's
`inputDescriptorDigest` (S15) and the journal's `intentDigest`. Semantics,
total over the shape: `core-repair` keeps closure, schema and store; `core-update`
changes the closure, never lowers the schema, selects a new store generation
exactly when the schema changes; `core-rollback` changes the closure, never raises
the schema, needs the deadline; `store-migrate` keeps the core closure, advances
the schema and selects a new store generation; `store-rollback` keeps the core
closure, retreats the schema, re-selects the retained generation, needs the
deadline. An earlier revision recorded that "the current nine-field, three-operation workflow
schema cannot express a store operation" and owed the workflow owner an enum extension. **That is
discharged in current bytes:** `workflows/schemas/invocation-record.schema.json#/$defs/
CoreTransitionIntentV1` now requires all eleven fields, including `fromStoreGeneration` and
`toStoreGeneration`, and its `operation` enum is the five operations above. The successor field
contract and the workflow schema agree, and `integration-host-model.py` validates one intent against
both (`CoreTransitionIntentV1` then `InstallationTransitionIntentV1`) before
`admit_transition_intent`. The retained `nine-field-legacy-intent-*` case keeps its meaning: a
nine-field intent is refused, which is now a regression against a schema that no longer produces one.

**The schema/store pair, stated here so no reader needs the reference model.**
For `core-update` and `core-rollback` alike, an unchanged state schema keeps the
store generation (`TRANSITION.SAME_SCHEMA_KEEPS_STORE`) and a changed state
schema selects a different one (`TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE`).
`core-repair` keeps closure, schema and store together. `store-migrate` requires
an advanced schema **and** a different generation; `store-rollback` requires a
retreated schema **and** a different generation. No admitted intent changes the
store generation with an unchanged schema, and the S9 footprint above already
owns the re-selection of a retained store. This restates exactly what
`admit_transition_intent` enforces; it adds no rule and changes no refusal.

**Journal (`InstallationTransitionJournalV1`; identity
`H("security.installation-transition-journal.v1", record)`).** Written under the
held fence, only after every lease of the affected set is held (`fenceHeld` and
`writtenAfterAllLeasesHeld` are schema constants), in state `LEASED`. It binds:
the `intentDigest` and every intent field; the namespace registry frozen under
the fence (`registry`, `registryDigest`); `affects` and the exact `leaseSet`,
which must equal `core_transition_affected_namespaces` over that frozen
registry (a caller cannot choose a smaller or different set: `TRANSITION.SCOPE_MISMATCH`);
and, through admission, the current state schema, store generation and core
generation the transition starts from. Admission context (all host observations
under the fence): `intent`, `intentDigest`, `namespaceRegistry`, `fenceHeld`,
`leasesHeld` (what the S7 composition actually acquired), `currentStateSchema`,
`currentStoreGeneration`, `currentCoreGeneration`, `admittedTime`. Refusals
`TRANSITION.*` (D9 `REQUEST.PRECONDITION_FAILED`): among them
`LEASE_SET_NOT_HELD` (a busy namespace means no journal is written),
`FENCE_NOT_HELD`, `INTENT_DIGEST_MISMATCH`, `INTENT_FIELD_MISMATCH:<f>`,
`REGISTRY_MISMATCH`, `CURRENT_SCHEMA_MISMATCH`, `CURRENT_STORE_MISMATCH`,
`PRECONDITION_GENERATION_MISMATCH`, `ROLLBACK_WINDOW_EXPIRED`,
`NO_ADMITTED_TIME_CONTEXT` (rollbacks need an S4 admitted time inside the
host-observed window; user arguments cannot extend it). States: `LEASED →
PREPARING → PREPARED → COMMITTED → DONE`, or `ABORTED`.

**Crash recovery (`recover_transition_journal`), the first act under the next
fence, before any project admission.** Fail closed: no fence → refuse; a
registry that differs from the frozen one → `QUARANTINE` / `MIGRATION.CORRUPT`
(registration needs the fence, so the footprint is ambiguous); the journaled
lease set not re-acquired exactly → `PROJECT.BUSY` (retry outside the fence);
then by state: `LEASED`/`PREPARING` → `ABORT` (nothing selected; installation
unchanged); `PREPARED` → a store operation follows the S9 footprint table
(`RESUME-COMMIT` from step 3 only when the old store is fenced `RESTORED`,
otherwise `ABORT`; no footprint → `QUARANTINE`), a core operation aborts (the
published generation was never selected; GC census reclaims it); `COMMITTED` →
`RESUME-COMMIT` (a committed transition is finished, never reversed, even after
the rollback window); `DONE`/`ABORTED` → release only. Cases `crash-at-*`,
`registry-changed-*`, `journaled-lease-set-not-exactly-reacquired-*`.

### S9.3 Private store-instance lineage (successor; proposed, not accepted)

A numeric store generation is not unique over time: `store-rollback` re-selects a
retained generation and `core-rollback` never raises the schema, so two physically
distinct stores can present the same `(storeGeneration, stateSchema)` pair. A
private **store instance identity** disambiguates them for local operational
records. It adds no member to `InstallationTransitionIntentV1`,
`InstallationTransitionJournalV1`, the namespace registry or any signed document,
introduces no envelope kind and no public major, and mints no D9 class, code or
exit; its refusals are the existing `TRANSITION.*` set and the existing
`MIGRATION.CORRUPT` quarantine. It is never a wire field, an authority token or a
semantic input, and it never enters the pure evaluator or a Run hash.

**Instance identity.** Each physical store instance carries one `storeInstanceId`:
32 lowercase hexadecimal characters from 128 bits of OS CSPRNG, allocated once
when that store is created, persisted in that store's own root before the store is
first published, and never rewritten. It has no ordering and no arithmetic, and
reading it grants nothing.

**Lineage nodes, identified by the full triple.** A private append-only table
holds one node per admitted binding triple
`(storeInstanceId, storeGeneration, stateSchema)`, carrying its predecessor triple
and the `intentDigest` of the transition that created it; both are `null` exactly
at a **lineage root**. Every lookup uses the whole triple, whose instance component
is read from the store-root **marker** of the store concerned: a numeric pair alone
never identifies a node, because a retained branch may lawfully present the same
pair as a fresh target. `intentDigest` is evidence validated *on* the selected node
and is never a search key, since it may lawfully repeat. This section asserts no
global uniqueness of a store generation beyond what the rules above already impose.

**Marker observation is three-way and phase-bound.** Reading a store root yields
exactly one of: a **readable** identity; **absent**, meaning no store root is
present; or **unreadable**, meaning a root was observed but its marker is missing
or malformed. An unreadable marker is never treated as absence, and an absence must
be observed, never inferred from a missing observation. The store a transition
comes from always exists, so its marker is always required. The **selected**
store's marker is required only where the transition is settled as committed: at
`LEASED` and `PREPARING` a forward selection's target has not been materialised,
and after an abort an unpublished target may already have been reclaimed by the GC
census, so an absent target there is expected and must never be read as corruption.

**One admission law.** A node is admitted only if its shape is admitted by the
private record's own closed schema, its predecessor and origin digest are null
together or present together, it does not name its own triple, its non-null
predecessor already exists as a node at that exact triple, no existing node shares
its primary key with disagreeing contents, and the chain from it is acyclic and
reaches exactly **one** lineage root. That root rule is scoped to the chain, not to
the whole table: an authorized restore or adoption starts its own lineage, so
several lineages may coexist. Publication and recovery apply this same law, and an
exact byte-identical match at the target key is idempotent but **not** a short
circuit — it is validated the same way and simply writes nothing. A refusal writes
nothing.

**Selection case, derived from the admitted intent alone.** By the pair law in
S9.2 the case is decidable without reading any stored node: equal `to`/`from`
generation and schema is a **same-store** selection; an advanced schema is a
**forward selection**; a retreated schema is an **ancestor re-selection**. Only a
forward selection materialises a new store, allocates a fresh `storeInstanceId`
and writes one node, after the journal record is durably `COMMITTED` and never
inside a level-4 grant-journal append lock. A same-store or ancestor re-selection
writes no node: the store it selects already has one, created by an earlier act.

**Recovery applies the same case, and only after the owner decides.**
`recover_transition_journal` keeps every decision it already makes; this adds no
state, code or recovery action, and in particular a core operation at `PREPARED`
still aborts and a store operation still follows the S9 footprint. Where that
function refuses, reports the project busy or quarantines, the companion makes **no
decision at all**, inspects nothing and reads no marker. Where its action settles
the transition as committed — `RESUME-COMMIT` or `RELEASE-ONLY` reaching `DONE` —
then: a **forward selection** node must be present at its own full triple, or else
reconstructed from the journal record's own from/to generation and schema members
together with the predecessor and selected store-root markers, and admitted by the
law above. A **same-store or ancestor** re-selection validates the retained node at
its own full triple and **never rewrites its predecessor or origin digest**; an
ancestor must additionally lie on the verified chain from the current node, so a
store at a merely equal numeric pair off that chain never qualifies. That node was
created by an earlier, unrelated act whose origin the current intent does not carry,
so a missing one cannot be repaired from it and is `QUARANTINE` /
`MIGRATION.CORRUPT`. No atomicity is claimed between the journal record and a node.

**Before the owner settles a transition**, pre-existing ancestry is expected and
untouched, including a retained branch at the same numeric generation, and an
absent target is expected as above. Where a target *is* observable, what must not
exist is a *new* node for that transition at **its own full triple**: a node there,
or a node there already claiming that transition as its origin, is a premature-node
contradiction and quarantines.

**Lineage roots.** A root is created by an authorized local act that materialises a
new physical store outside any transition: installation, or an authorized evidence
restore or portable adoption. Such an act allocates a fresh `storeInstanceId`,
**replaces** any marker present in copied bytes before first publication so a
restored store never impersonates its source, imports no node from the source, and
imports no floor, grant or local commit authority. No transition is invented to
give it an `intentDigest`.

**Floors and authority are unchanged by this section.** An authorized transition
keeps the S9 floor rules exactly: migration copies the floors forward into the new
store, rollback inside the window sets them to the maximum of both stores, and a
poisoned floor is lowered only by S4.5. An instance identity records which physical
store is selected; it never lowers a floor and never confers local commit authority.

## S10. Execution principal `repository-code`

Principal classes: `first-party`, `repository-code`, `imported-artifact`.
Repository execution is disabled by default. The display names are aliases of
one foundation semantic-grant principal kind: workflow `P-TRUSTED-REPO` and
native `repository-code` both map to `trusted-repository-code`
(identity-schemas.v3 `semantic-grant`). Two identities are kept apart: the
foundation `semanticGrantDigest` (semantic projection inside plan2: principal
kind, closure, owner-source digest, operations, scope; no nonce, expiry or
consent) and the operational `securityGrantRef` =
`H("security.repo-execution-grant.v2", grant)` under the product canonicalizer
(this record). The workflow `TestExecutionStepParams.authorizationRef` and the
native `AuthorizedExecutionV2.authorization` both reference the operational
identity.

A `RepoExecutionGrantV2` (supersedes the never-accepted V1 draft, retained in
the bundle as superseded) is admitted only when: schema 2; principal
`repository-code`, `semanticPrincipalKind` `trusted-repository-code`;
projectId, snapshotId (`snapshot2:`) and argv digest equal the invocation's;
execution class in {build-script, proc-macro, test-runner}; **owners** (≤ 64,
unique) each bind `{ownerKey, source, ownerFileManifestSha256}` where `source`
is `snapshot-member` (validated against the sealed snapshot's owner manifests)
or `dependency-closure-member` (validated against the **sealed
`DependencySourceSetV1`**, whose id must equal `dependencySourceSetId`) — so
build scripts and proc-macros of external crates are grantable exactly when
they are in the sealed closure, never from an ambient registry or vendor
directory; `ownerSourceDigest` equals the host-computed owner-set digest; the
**runner** is a
member of the sealed first-party tool closure (`toolClosureId`, `closure2:`;
bundled cargo/rustc/linker/test runner) for build-script and proc-macro, or a
tool-closure member or sealed snapshot member for test-runner — there is no
system cargo, rustc, linker or shell fallback; `platformId` is one of the four
S8 machine platform ids (a display alias refuses); every effect value (`subprocess`, `filesystemWrite`,
`network`, `environment`) **equals** the security owner's platform truth
table entry (currently `DISCLOSURE-ONLY`, `DISCLOSURE-ONLY`, `DISCLOSURE-ONLY`,
`ENFORCED-BY-CONSTRUCTION` on all four platforms; a stronger or weaker claim
refuses). Those four effect *names* are copied from four of the seven closed
permission **tokens** in `permission-truth-tables.v9.json`, and the
correspondence — `subprocess`→`PT-PROC-EXEC-DECLARED`,
`filesystemWrite`→`PT-FS-WRITE-HOST-STATE`, `network`→`PT-NET-EGRESS`,
`environment`→`PT-ENV-READ`, with the values read from the `child-process`
execution mode these owners run in — is tabulated in native §5.2. Two limits
carry with it: `PT-FS-WRITE-HOST-STATE` names the **host's own state store**, so
neither the token nor a grant over it confers authority over the repository
filesystem — its `DISCLOSURE-ONLY` value states that nothing prevents writes
anywhere, since the code holds the invoking user's ambient authority; and
`PT-HOST-EFFECT-BROKERED`, the one token whose value is
`ENFORCED-AT-HOST-BROKER`, is deliberately projected by no effect name, because
repository code here is not routed through a host broker. Confinement remains
never claimed; authorization is `interactive-explicit` (never in CI) or
`policy-record` with a record id; the grant's `ci` flag is a real boolean equal
to the invocation's; the project policy admits the principal; expiry is
operation-end; not inherited. The native contract copies these effect values
into `AuthorizedExecutionV2.effects` and its `owners[]` are this grant's
owners; the workflow contract's `consentSource` (`pre-existing-policy` |
`interactive-consent`) maps to `policy-record` | `interactive-explicit`, and
its `argv0Source` maps to `runner`. Revocation of a running grant is the S6
path; confinement is never claimed.

**Operational admission precedes any Plan (decided; SHOULD-2).** A grant
authorizes one *operational* step: native preparation (build-script /
proc-macro owners, workflow `native prepare`) or a workflow test-execution step
(test-runner). Preparation runs before the analysis Plan that will consume its
outputs exists, and a test-execution step has no Plan at all (workflows §1/§7),
so **no Plan semantic-grant projection is an admission input** of
`admit_repo_execution_grant`; a ctx projection supplied beside the grant is not
read (`a-ctx-projection-is-never-consulted-not-an-authority-condition`), and a
host must not fabricate one from the grant. The bindings that hold every grant
are the ones listed above: project, snapshot, argv digest, execution class,
owners (preparation classes), runner, tool closure, platform and truth-table
effects, consent, `ci`, expiry, non-inheritance, and the S6 live boundaries
during the step. For a test-runner grant `owners` is `[]` and
`ownerSourceDigest` is the digest of the canonical empty owner array
(`4f53cda1…2b945`): canonical empty-set bookkeeping that keeps the record
shape uniform and binds nothing; the runner is bound by `runner` +
`toolClosureId`/snapshot membership + `argvDigest`
(`test-runner-grant-admits-with-no-plan-*`,
`test-runner-runner-outside-both-sealed-sets-refuses-although-the-empty-owner-digest-matches`).

The Plan-time join is separate and later. `semantic_projection_for_grants`
lists the `trusted-repository-code` principals (`{kind, closureId,
ownerSourceDigest}`) of the **preparation** grants whose prepared outputs an
analysis consumes; a test-runner grant contributes nothing, because its
evidence enters a Plan only as an `import2` payload whose wrapper and
test-execution step receipt retain the operational `securityGrantRef`. When the
analysis is admitted, `admit_plan_execution_projection(planPrincipals,
consumedGrants, preparedResolution)` requires, under `host-prepared`, that the
plan2 semantic-grant projects exactly those principals
(`PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED:<digest>` /
`PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT:<digest>`), refuses any
`trusted-repository-code` principal under `imported-inert` or `none` (prepared
availability never implies this host held a grant), and refuses a test-runner
grant offered as a consumed grant (`PLAN.TEST_RUNNER_HAS_NO_PLAN`). The
projection comes from the Plan and the grants from the step receipts; they must
agree, and neither is derived from the other. D9: `REQUEST.PRECONDITION_FAILED`
(request-rejected 2). Records `SemanticProjectionV1`,
`ExecutionProjectionAdmissionV1`; cases `plan-*`,
`semantic-projection-for-grants-*`. **Implemented, not owed:**
`integration-host-model.py` derives the Plan requirement through
`semantic_projection_for_grants(grants)` and `check-integration.py` drops
`ctx.semanticGrantPrincipals` before operational admission and then checks the Plan-time join
(`consuming-plan-preparation-principal-join`, `consuming-plan-missing-principal-refused`,
`imported-inert-does-not-infer-local-grant`, `test-runner-is-operational-not-a-plan-principal`,
`test-runner-cannot-be-consumed-as-preparation`).

### S10.1 Repair apply authorization (not a repository-execution grant)

Repair apply is host-brokered **first-party** source mutation: the host writes
postimages it computed from a signed recipe closure under the EXCLUSIVE lease.
No repository code runs. Its authorization is therefore a separate record,
`RepairApplyAuthorizationV1` (product data; identity
`H("security.repair-apply-authorization.v1", record)` is the workflow
`RepairApplyParams.authorizationRef`), admitted only when: projectId,
`repairPlanId` (`repairplan2:`) and `baseSnapshotId` (`snapshot2:`) equal the
invocation's; the live tree still equals the base snapshot
(`AUTHZ.SOURCE_MOVED`); `recipeClosureId` (`closure2:`) equals the recipe in
the rehashed repair plan (`AUTHZ.RECIPE_CLOSURE_MISMATCH`) and is positively
admitted under current signed-closure trust (`AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED`).
Absence from the revocation set is insufficient. Revocation refuses first
(`AUTHZ.RECIPE_CLOSURE_REVOKED`, D9
`EXTENSION.ADMISSION_REJECTED`); consent is `interactive-explicit` (never in
CI) or `policy-record`, with a real boolean `ci` equal to the invocation's;
expiry operation-end; `leaseMode` `EXCLUSIVE`; `repositoryExecution` is the
constant `false` and cannot be set. Live revocation: every brokered write
passes the S6 authority checkpoint; a revoked recipe closure at any checkpoint
is `REV(trust-revoked)` with postimage-checked rollback and the workflow's
`FAILED_ROLLED_BACK` / `RECOVERY_BLOCKED` states. Reference
`admit_repair_authorization`; fixture `repair-authorization-cases.v1.json`.

Fingerprint-targeted repair consumes `finding-key2` fingerprints of **finding3**
occurrences on a **run3** evidence Run (workflow evaluator3 repair descriptor
`evidenceRunId`). The fingerprint domain stays `finding-key2`; that is
correspondence identity, not a finding2 occurrence and not a run2 graph.
A historical `finding2` / `run2` export remains inspectable by its original
tools. It cannot become current repair, baseline, import or installation
authority by changing an id or schema label. Unmatched finding3 occurrences
remain findings of the current Run and may fail ordinary current-Run gates;
they cannot satisfy a fingerprint-targeted repair or waiver. EXCLUSIVE lease,
host-brokered mutation, `repositoryExecution=false` and original-plan-only
recovery scope are unchanged.

### S10.2 Repair recovery authorization (decided; post-reset v2 N-4/P9)

Recovery inspection (`repair recover` without `--apply-recovery`, workflows §6
`repair_inspect`) is read-only and needs no authorization. Every recovery
**mutation** (`discard-temps`, `roll-back-renamed`,
`verify-postimages-and-commit`) is a separately authorized host-brokered
write within the **original** plan's authority, under the EXCLUSIVE lease, and
its authorization is the closed security record `RepairRecoveryAuthorizationV1`
(product data; identity `H("security.repair-recovery-authorization.v1", record)`
is the workflow `RepairApplyJournalV1.recoveryAuthorizationRef`, always the full
reference, never a truncated prefix). It is admitted by
`admit_recovery_authorization(authz, ctx)` only when every binding holds:

- **Project, plan, snapshot, recipe.** `projectId`, `repairPlanId`,
  `baseSnapshotId` and `recipeClosureId` equal the admitted project and the
  rehashed original plan (`AUTHZ.*_MISMATCH`).
- **Exact journal identity (noncircular).** `journalRef` =
  `security.repair-apply-journal-identity.v1:` + `H` over the closed identity
  preimage `{schemaFamily, schemaMajor, requestId, stepId, executionId,
  repairPlanId, baseSnapshotId, authorizationRef}`: only fields fixed when the
  apply journal was created, never `state`, paths, blobs, blocked/restore lists
  or any `recoveryAuthorizationRef` the journal later carries, so one journal
  has one identity in every state and the reference written into the journal
  never enters its own preimage (`journal-identity-mismatch-*`,
  `journal-of-a-different-plan-*`).
- **Observed journal state and replay/crash semantics.** `journalState` and
  `observedJournalStateDigest` (raw SHA-256 of canonical `{state, stagedPaths,
  appliedPaths, preimageBlobs}`) equal the journal **as read under the EXCLUSIVE
  lease before any recovery write**. Every successful recovery mutation changes
  `state`, so a retained authorization cannot be replayed after one
  (`AUTHZ.JOURNAL_STATE_MOVED`; `replay-after-a-successful-rollback-*`); a crash
  or a `requires-broker` return before the first write leaves the digest
  unchanged. The same authorization may continue only within the same still-admitted
  recovery execution and lifetime. A process crash ends that execution; a fresh
  attempt requires a newly admitted authorization bound to its new execution id (`crash-before-the-first-recovery-write-*`).
- **Finite action.** `recoveryAction` equals the one the journal state admits
  (`PREPARING`/`STAGED` → `discard-temps`; `APPLYING` → `roll-back-renamed`;
  `APPLIED`/`INDETERMINATE` → `verify-postimages-and-commit`;
  `AUTHZ.RECOVERY_ACTION_MISMATCH` otherwise). Terminal states (`COMMITTED`,
  `FAILED_*`, `RECOVERY_BLOCKED`) admit no mutation
  (`AUTHZ.RECOVERY_NOT_MUTATING:<state>`); the table mirrors the workflow
  recovery table's mutating rows, and the integration checker asserts that equality today
  (`security-workflow-recovery-action-table-identical`, comparing the mutating rows of
  `W.RECOVERY_TABLE` with `S.RECOVERY_ACTION_FOR_STATE`).
- **Fresh attempt.** `originalRequestId` equals the journal's `requestId`;
  `recoveryRequestId`/`recoveryExecutionId` equal the recovery invocation's own
  ids and differ from the original (`AUTHZ.RECOVERY_REQUEST_NOT_FRESH`).
- **Consent and policy.** Consent is `interactive-explicit` (never in CI) or
  `policy-record`, with a real boolean `ci` equal to the invocation's; the project
  policy admits repair.
- **Time.** `issuedAt` ≤ S4 admitted evaluation time ≤ `expiresAt`, lifetime at
  most 24 h; no admitted time context refuses (`AUTHZ.NO_ADMITTED_TIME_CONTEXT`).
- **Boundary.** `leaseMode` `EXCLUSIVE`, `mutationBoundary` `host-broker`,
  `repositoryExecution` and `newEdits` are the constant `false`: recovery can
  never grant repository code execution, write a byte the original plan did not
  name, or broaden the plan (`planScope: original-plan-only`).
- **Current host custody.** The S3 custody rule is re-run on the recovery
  invocation (`AUTHZ.CUSTODY_NOT_ADMITTED`); an old admission does not carry over.

**Safe rollback versus re-executing a revoked recipe.** `discard-temps` and
`roll-back-renamed` restore retained preimages or discard temps and **never
consult recipe trust**: rolling back after the recipe was revoked is exactly what
revocation rollback is (`rollback-recovery-admits-although-the-recipe-closure-is-revoked-*`).
`verify-postimages-and-commit` would commit the recipe's postimages, so it
re-consults current signed-closure trust: a revoked recipe refuses first
(`AUTHZ.RECIPE_CLOSURE_REVOKED`, D9 `EXTENSION.ADMISSION_REJECTED`) and a recipe
not positively admitted refuses (`AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED`). The
workflow recovery table's guarded preimage/postimage law (every target at its
plan preimage or postimage before any restore or commit; otherwise
`RECOVERY_BLOCKED`) is mandatory and never waived by this record.

**Trusted context inputs**, each a host observation and none supplied by the
caller of `repair recover`: `projectId`, `repairPlanId`, `baseSnapshotId`,
`journal` (as read under the lease), `recoveryRequestId`, `recoveryExecutionId`,
`ci`, `admittedTime`, `custodyAdmitted`, `policyAdmitsRepair`, `recipeClosureId`,
`revokedClosures`, `admittedClosures`. Output `RecoveryAuthorizationAdmissionV1`;
fixture `repair-recovery-authorization-cases.v1.json`. **Implemented, not owed:** the workflow
journal's `recoveryAuthorizationRef` takes the closed grammar above,
`integration-host-model.py` `recovery_authorization_projection` composes
`admit_recovery_authorization` exactly as it composes `admit_repair_authorization`, and
`repair_recover` consumes that host-created projection rather than a caller dictionary — the
caller-dictionary path is a checked refusal
(`recovery-caller-projection-refused`), beside
`security-workflow-journal-preimages-identical`, `security-to-recovery-full-reference-commits`,
`recovery-moved-journal-refused`, `recovery-revoked-commit-refused`,
`recovery-original-execution-not-fresh` and `recovery-revoked-recipe-still-rolls-back`.

## S11. Offline windows and doctor (AR-16)

Windows: revocation fresh 90 d after its issue; catalog expires 90 d after
issue; root expires 365 d after issue; warning from 14 d before the earliest
cliff. Continuation (already-verified components run) stops when the revocation
list is stale or the root expired; install/update stops when the catalog
expired or continuation stopped. Remedies: an ordinary payload (consented
online refresh or air-gap import); an expired root heals only by S5; a floor
ahead of the wall heals only by S4.5. The OD-112-4 G08 waiver is a release-gate
waiver held by product and release authority; no user waiver extends an
install's freshness. Doctor is report-only: a found defect is outcome `OC-2`
with exit 0 and `writes: []`; CI gates on `.outcome == "OC-1"` in the machine
report, never on the exit code. No exit code is changed by this contract.

## S12. D9 joins and refusal vocabulary

| Refusal | D9 class / exit / code |
|---|---|
| `CONFIG.CUSTODY_REFUSED`, `PROJECT.ROOT_CUSTODY_REFUSED`, `PROJECT.EXPLICIT_PATH_INVALID` (incl. `JOIN_PATH_GRAMMAR`, `JOIN_INSIDE_PRUNED_TREE`, `JOIN_CROSSES_NESTED_PROJECT`) | request-rejected / 2 / `CONFIG.INVALID` |
| `PROJECT.WORKSPACE_UNIT_LIMIT` (detail `WORKSPACE_UNIT_LIMIT:<n>><cap>`) | request-rejected / 2 / `REQUEST.UNSATISFIABLE` |
| `CLOCK-EXCURSION-FORWARD`, `TRUST.NO_ADMITTED_TIME_CONTEXT`, `GRANT.REFUSED` (all `GRANT.*` details), `PLAN.EXECUTION_PROJECTION_REFUSED` (all `PLAN.*` details), `AUTHZ.*` details except revoked closure (apply S10.1 and recovery S10.2), `TRANSITION.REFUSED` (all `TRANSITION.*` details, S9.2), `PROJECT.DISCOVERY_INVENTORY_MISMATCH` (host security/native inventory join), `storage.backup-choice-required` | request-rejected / 2 / `REQUEST.PRECONDITION_FAILED` |
| `PROJECT.EXPLICIT_PATH_INVALID` (nested boundary crossing; native aliases are internal) | request-rejected / 2 / `CONFIG.INVALID` |
| `PAYLOAD-NOT-ADMISSIBLE` (incl. `ROOT.*`, `ENVELOPE.*`, `PROFILE_SET.*` details), `RECOVERY.REFUSED` (all typed details), `NT-TCB-*`, revoked-during-operation, `AUTHZ.RECIPE_CLOSURE_REVOKED` | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` |
| `ROOT.SCHEMA_UNSUPPORTED`, `STATE.SCHEMA_UNSUPPORTED`, `ROOT.FLOOR_ABOVE_CORE` | request-rejected / 2 / `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` |
| `PROJECT.BUSY` (incl. a journaled transition lease set not re-acquired exactly, S9.2) | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` |
| `MIGRATION.CORRUPT` (incl. a registry differing from the frozen transition journal, S9.2) | operational-failed / 4 / `LEDGER.CORRUPT` |
| `OBSERVER.FAIL_STOP`, I/O failure | operational-failed / 4 / `HOST.IO_FAILURE` |

The common scope stage additionally refuses PROJECT.SCOPE_LIMIT with REQUEST.UNSATISFIABLE (exit2) when its distinct workspaceRoots exceed1024 or pathPrefixes/excludedPathPrefixes exceed65536, even if discovery's4096-unit limit admitted the repository. Public subject `field:count>limit` states the observed bound. PROJECT.DISCOVERY_INVENTORY_MISMATCH is REQUEST.PRECONDITION_FAILED (exit2) at the host's security/native inventory join. Boundary crossing still uses PROJECT.EXPLICIT_PATH_INVALID; native internal aliases do not create a second public code.

### S12.1 Projecting a refusal onto the one closed public detail vocabulary

A public termination carries exactly one `domainDetail` = `{code, remedy, subject?}`, and `code` is a
member of the single closed registry (`design-corrections/public-detail-registry.v1.json`, mirrored by
`workflows/schemas/common.schema.json#/$defs/DomainDetailCode`). This section states the projection
this unit's refusals take, so that "detail" in the prose above is never ambiguous between a registry
member and free subject text. Reference `public_detail` / `public_details`, record
`PublicDetailProjectionV1`, fixture `public-detail-cases.v1.json`, sweep
`public-domain-details-are-a-closed-set-with-a-bounded-pending-registration-gap`.

1. **Base code, then subject.** The base code is everything before the **first** colon; everything
   after it is subject data. `ROOT.ROLE_SET:1` is code `ROOT.ROLE_SET`, subject `1`.
2. **A registered detail wins over the enclosing refusal.** When a refusal carries a `detail` whose
   base code is a registry member, that is the public code. This is why the 38 `ROOT.*` document
   defects are public codes instead of collapsing into one `PAYLOAD-NOT-ADMISSIBLE`, and it is
   exactly why `ENVELOPE.*` and `PROFILE_SET.*` belong in the registry: they occupy the same position
   in `admit_profile_set_envelope` that `ROOT.*` occupies in `admit_root_document`, and S9.1 names
   them normatively as `detail`.
3. **Otherwise the refusal supplies the code and the whole detail is subject text.** This is the
   existing reading for `RECOVERY.REFUSED` (`CHALLENGE_EXPIRED`, `COUNTER_MISMATCH:<k>`,
   `ISSUED_TOO_OLD_FOR_WALL`, …), for `CONFIG.CUSTODY_REFUSED` (`SYMLINK`, `WRITABLE_BY_OTHERS`, …)
   and for `PROJECT.EXPLICIT_PATH_INVALID` (`JOIN_PATH_GRAMMAR`, `JOIN_INSIDE_PRUNED_TREE`, …). Those
   sub-details are deliberately **not** registry members; registering them would create a second
   public vocabulary for the same events.
4. **The vocabulary is closed, not a prefix rule.** The unit declares the exact set it may emit
   (`SECURITY_PUBLIC_DETAIL_CODES`, 191 members). A detail whose base code lies inside one of the
   eight families this unit publishes (`AUTHZ.`, `ENVELOPE.`, `GRANT.`, `NT-TCB-`, `PLAN.`,
   `PROFILE_SET.`, `ROOT.`, `TRANSITION.`) but outside that set **refuses**; there is no open
   `PROFILE_SET.*` wildcard.
5. **The D9 branch comes from the refusal, never from the detail.** Naming a defect more precisely
   never changes its termination branch. `PROFILE_SET.NO_TR_PROFILE_ROLE` therefore travels under
   `ROOT.SCHEMA_UNSUPPORTED` → `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` exactly as S9.1 says, while every
   other `PROFILE_SET.*`/`ENVELOPE.*` defect travels under `PAYLOAD-NOT-ADMISSIBLE` →
   `EXTENSION.ADMISSION_REJECTED`. Members of the three document-admission families
   (`ROOT.`, `ENVELOPE.`, `PROFILE_SET.`) that the D9 table does not name individually take that same
   `PAYLOAD-NOT-ADMISSIBLE` row; the three schema-major refusals keep their own. The single
   exception is `AUTHZ.RECIPE_CLOSURE_REVOKED`, which is an admission rejection while every other
   `AUTHZ.*` detail of the same admission is a precondition failure.
6. **Internal decision keys are aliased, never published.**
   `RF-6:AUTHORIZATION.GRANT_NOT_CURRENT`, the S6 linearization trace's spelling for a request
   refused after revocation, is an internal alias of the registered
   `TRUST.COMPONENT_REVOKED_DURING_OPERATION`.

**The eleven formerly missing codes are now registered** in the shared
`public-detail-registry.v1.json` and the identical workflow `DomainDetailCode`
enum: `ENVELOPE.SHAPE`, `ENVELOPE.KIND`, `ENVELOPE.BODY_DIGEST`,
`PROFILE_SET.SCHEMA_SHAPE`, `PROFILE_SET.SCHEMA`, `PROFILE_SET.CANON`,
`PROFILE_SET.CORE_PIN_MISMATCH`, `PROFILE_SET.NO_TR_PROFILE_ROLE`,
`PROFILE_SET.SIGNATURE_THRESHOLD`, `ROOT.TR_REPAIR_THRESHOLD_POLICY` and
`ROOT.TR_PROFILE_THRESHOLD_POLICY`. The last two are the exact per-role
schema-2 threshold refusals. The RF-6 internal alias is registered as well.
The reference sweep requires every emitted code to be registered and every
internal alias to match the shared mapping; no drafting gap is permitted.
`PENDING_PUBLIC_DETAIL_REGISTRATIONS` preserves the old coordination list as
provenance, while `pendingRegistration` is computed from the actual registry
and is false for these current registered outcomes. The host's common
termination projection validates every final public shape.

## S13. Reference evidence and implementation conformance

`security/check-security-lifecycle.v1.py` verifies the pinned sources, admits
every case file through the foundation canonicalizer, runs 456 cases across
sixteen fixtures (positive, negative, crash, replay, downgrade, reboot,
window-expiry, exact-typed-constant, report-only, strict end-anchor regression,
public-detail projection) and ten invariant sweeps
(floor monotonicity with no clamp and no report-only write; recovery
single-use with replay, counter-mismatch in both directions, reboot and window
refusal; brokered linearization with no overwrite of user edits; profile
separation; lease-mode matrix; root schema reader sets typed-unsupported never
corruption; discovery pruning of 4200 installed manifests and the typed
first-party cap refusal; the one-platform-vocabulary join across profile set,
admission, grant, native matrix and workflow schema; the admitted-boundary
join that runs the nested-repository/nested-project fixture through this
instrument and the native unit instrument; the closed, fully registered public-detail projection and exact shared aliases, S12.1), validates every output against the closed schemas, and writes
`security-lifecycle-report.v1.json`. Every signer set, nonce and OS observation
in the fixtures is an asserted model input (TCB assumption), not a measurement. Before shipping, the implementation must
additionally demonstrate on every lane: O_NOFOLLOW/ACL custody races;
sleep-inclusive monotonic behaviour across suspend; fsync-ordered floor writes
and crash points around each write; flock semantics of the three modes;
process-group kill within the bound; observer stall under SIGSTOP; migration
crash points at every step; and end-to-end recovery-epoch signing with the
publisher ceremony. Those are qualification criteria under the existing gates,
not open design alternatives.

### Joint correction provenance

Actual Claude authored the security unit; Codex's independent v2 probes exposed
additional schema and cross-contract defects. Codex supplied the v3 integration
corrections. The post-reset independent Claude review of the frozen
`candidate-subject.v1` (retained in the repository at
`docs/coop/design-corrections/reviews/post-reset-review.v1/review.md` with its
executable probes) returned MUST-2, MUST-3, SHOULD-2/3/4/6/7 and ADV-3 against
this unit; a new Claude author session corrected them in the working tree
(handoff `docs/coop/design-corrections/reviews/post-reset-author.v1/handoff.md`) while
Codex concurrently corrected foundation/workflows/integration (S14/S15 headings,
repair authorization binding, strict end assertions). The second independent
Claude review, of the frozen `candidate-subject.v2`, returned N-1 (nested
boundaries not carried into native discovery), N-4 (no owning repair recovery
authorization), N-5 (transition intent/journal not representable) and
advisories A-3/A-4/A-5 against this unit; a further Claude author session
corrected them here (S3 boundary inventory, S9.2, S10.2, the `transition-journal`
lock action, the A-4/A-5 wording). A third independent session — a fresh blind consumer
reconstruction of the accepted `candidate-subject.v5` subset — returned M-5 (this contract
normatively names typed public details the closed registry cannot express), S-2 (two schema-1 root
documents disagree on admission) and S-6 (discharged obligations still written as open) against this
unit; a further Claude author session corrected them here (S8, S9.1, S12.1, and the S3/S9.2/S10/S10.2
obligation sweep). These mixed bytes require
a fresh independent review of a newly frozen subject; neither a passing
reference checker nor any author handoff accepts them. Codex completed the shared registry/typed-enum integration in S12.1 and strengthened
the sweep to require a zero registration gap. The original coauthor handoff and
its exact source bytes remain retained as evidence of that earlier coordination state.
UNKNOWN backup status permits admission with mandatory unknown disclosure, matching
identity-and-evidence. Detected backup status requires the explicit custody choice;
sync/shared/upload storage checks remain independent.

## S14. Candidate lifecycle command grammar (Codex integration correction)

These are the exact candidate spellings joined by the workflow inventory:
`opensip trust refresh`, `opensip trust import PATH`, `opensip trust doctor`,
`opensip trust recovery-challenge`, `opensip trust recovery-import PATH`,
`opensip store migrate --to 2`, `opensip store rollback --to 1`,
`opensip store gc`, and `opensip store status`. PATH is a user input path admitted
under the existing custody rules. Refresh is the explicit online consent boundary;
import uses an already obtained signed payload. Neither bypasses root, expiry,
revocation or current-core profile-set admission. Recovery import consumes the
signed response for the exact pending challenge.

Migration and rollback use S9's admitted source/target schema sets, the S9.2
transition journal, forward-only trust floors and rollback window; they run under
S7's core-transition lock set (fence held throughout plus EXCLUSIVE on every
affected registered namespace), not a single-namespace EXCLUSIVE lease.
GC follows the admitted retention policy, pins and availability generations rather
than inferring permission to purge all data. Status and both doctor commands are
read-only. `--project` selects at most one authority root; repeatable
`--workspace-root` supplies the internal `explicitJoins` projection from S3.
These grammar corrections are mixed-author bytes awaiting independent Claude review.

## S15. Execution and core-transition host composition (Codex correction)

The product host first validates the complete RepoExecutionGrantV2 record, verifies
its canonical sorted owner-set preimage and raw ownerSourceDigest against sealed
host inventories, then calls `admit_repo_execution_grant`. The workflow test input
is a host-created projection of that actual admitted grant; it is not a submitted
`ADMIT` flag. Native preparation uses one class-specific grant per owner as described
in native §14. All machine grant/test platform IDs are the S8 machine platform ids;
display aliases never enter those records. Grant admission is operational and
precedes any Plan (S10); the Plan-time projection join is
`admit_plan_execution_projection`. The reference composition is
`integration-host-model.py`; its contexts explicitly stand in for real TCB
observations. The public root-chain path similarly calls `admit_root_document` on
every full root before the continuity primitive. Reduced root fixtures are not a
public admission grammar.

`opensip core update VERSION`, `opensip core repair`, and
`opensip core rollback --to VERSION` are exact candidate grammars. Repair selects the
currently selected signed core closure and replaces damaged bytes; it does not
select a different release. Update and rollback resolve VERSION to one signed core
closure under current trust, platform and reader compatibility. Every operation,
core and store alike, binds a retained transition intent (workflow
`CoreTransitionIntentV1`, whose required successor field contract is S9.2
`InstallationTransitionIntentV1`): operation, from/to closure, from/to state
schema, from/to store generation, the target core's exact platform-profile body
digest, observed generation and rollback deadline. Its raw canonical digest is
the mutation step inputDescriptorDigest and the journal's `intentDigest`. The
host supplies the observed preconditions; user arguments cannot lower floors or
invent a rollback window.

All five use the S7 core-transition lock set (fence held throughout plus
EXCLUSIVE on every affected registered namespace, decided by
`core_transition_affected_namespaces` from the intent's from/to state schema and
store re-selection; a same-schema update or repair affects no namespace and
running project operations keep their pinned generation), the S9.2
`InstallationTransitionJournalV1`, which records that exact lease set and the
frozen registry after every lease is held and drives crash recovery, and
immutable receipts. Commit rechecks generation and current target trust. Schema transition
requires the reader-first stage and profile binding from S9; rollback preserves
maximum observed trust/revocation floors and refuses an expired rollback window.
An incompatible or revoked target refuses before replacement. Neither repair nor
rollback imports old credential/authorization state. A later delivery failure
retains the transition receipt and does not reverse a committed transition.

Installation recovery is entered through the host admission described in workflow §12: verify the current durable revision reference, reconstruct and admit its intent, recompute intentDigest and derive the exact lease set over the frozen registry before calling the pure recovery table. A hash alone cannot authenticate a lawful scope. Each durable state revision has a new full H reference; the fenced journal location, not a caller argument, selects the current revision.

Shared discovery helper WORKSPACE_UNIT_LIMIT is an internal decision key only. Every public cap refusal uses PROJECT.WORKSPACE_UNIT_LIMIT, and malformed explicit roots use PROJECT.EXPLICIT_PATH_INVALID. The host applies the closed registry alias map; subreason/counts are diagnostic subject data, never alternate public codes.

## S16. Existing prototype users and local-state transition (DR-130)

The baseline is the separate `opensip-cli` prototype at commit `a62509d623173155d0946e9f5d5ca90c839893e0`, as scoped by architecture `prototype-evidence-reference.md`. Its files and output are historical user custody, not this product's schema-one state. S9's signed product stage/schema bridge must never be applied to a prototype database merely because it contains a version number of one.

The complete transition policy is **immutable coexistence with explicit adoption**, not automatic state conversion. Installing or selecting the new product does not replace the prototype package, mutate its Node/npm installation, take over its launcher/PATH alias, import its database, adopt its baselines or run it. Both installations may remain usable through their explicitly selected launchers/absolute paths. New product state is admitted only under its own validated root/profile/namespace; an occupied root with a foreign/prototype marker/schema is refused by the existing root/schema admission before a write. A user chooses a distinct admitted location or project checkout; the host never guesses that overwriting foreign state is migration. Removal targets the selected product installation and its own references. It does not uninstall the prototype or purge either product's evidence by implication.

A legacy configuration is accepted only by admission §1.1's exact supported legacy schema and in-memory provenance-preserving projection. Unsupported fields/versions refuse rather than being ignored. An explicit configuration migration is a reviewable authorized data patch; analysis never rewrites a tracked config. If the prototype and new product need incompatible project configurations, coexistence uses separate explicitly selected checkouts/configurations rather than silently changing the prototype's tracked intent. There is no prototype Run/baseline/state importer in this product. Historical exports remain inspectable by their original tools; a separately admitted current-format observation may enter only through the ordinary closed import registry with truthful producer/source correspondence. It cannot acquire historical Run authority or become a baseline merely by changing an id or schema label. This is a settled compatibility boundary for the full product, not a deferred delivery-stage decision.

The transition preserves all five obligations in architecture file05 §Migration constraints:

1. **Tracked intent:** original tracked config/locks and their version-control history remain intact; any requested new-format patch is explicit and reviewable, never a migration side effect.
2. **The same no-write pre-initialization value:** installing/selecting the new distribution does not initialize a project or write source-derived state. The prototype's no-write workflow remains available unchanged. The new product's explicit `--ephemeral` analysis and metadata-only surfaces provide pre-initialization value without a project marker, private registry entry, authoritative store, adoption or persistent cache write; temporary scratch custody and stdout are operational, never a durable initialization. The new product's default authoritative analysis remains the explicitly invoked, disclosed first-write operation of identity §5. Distribution migration never invokes that operation implicitly.
3. **Per-value provenance:** supported legacy projection records sourceSchemaVersion=1 and the original carrier/value origin; explicit new choices retain their own provenance. A default or migration cannot be reported as a tracked user choice.
4. **Historical identities/custody:** original ids, bytes, evidence meaning, retention and ownership remain in the original custody account. No new product identity replaces, upgrades or retroactively authenticates a historical one; new source/Plan/Run identities are explicitly new-major identities. Coexistence does not erase historical review standing.
5. **Promised offline behavior:** already installed prototype assets remain usable under their original promise. The new product's authoritative offline promise applies only to its separately admitted complete signed closure, including verified storage. Missing current assets cause typed unavailability/refusal, never an automatic download or fallback.

All five distinctions remain explicit: (1) distribution migration selects executable generations; user-custody state migration is a separately authorized operation, and no prototype-state conversion is provided; (2) management-only adoption supplies management functions, while an authoritative closure additionally supplies every admitted executable/data/storage dependency; (3) immutable coexistence retains separately selected generations/installations, while in-place package mutation is forbidden; (4) removal drops installation/reference selection, while explicit purge alone changes retained evidence availability under identity §5; (5) replay pinning retains the exact runnable detector/evidence closure, while contract-approved typed degradation reports missing/expired/purged evidence without rewriting assurance or fabricating replay.

Authoritative cache and regeneration hits inherit identity §4. Admission against a current Run is `identity-model.v3.close_run` complete evaluator3 semantic replay, then `admit_cache_entry` through that Run's own closure. Constructing `cache2` / `regen2` or matching a hash is not authority. `identity-model.py.close_run` of a `run2` graph is historical owner-closure admission (exact schema, identity, and native owner joins). It is not merely a hash compare, and it is not evaluator3 semantic replay. Expired or revoked permission cannot be resurrected by a matching hash. Installation recovery already requires reconstructing and admitting the retained transition intent over the frozen registry; a hash alone cannot authenticate a lawful scope. Retained historical `run2` custody stays those bytes.

The six “No migration silently…” prohibitions are retained individually: no silent **download**, **index refresh**, **lock mutation**, **replacement historical identity**, **evidence-meaning rewrite**, or **telemetry/network requirement**. Explicit commands retain their separate consent, signed-input, expiry/revocation, custody, recovery and output laws. No migration authority is inferred from the mere presence of old data.

Release owners must exercise the coexistence/foreign-root/legacy-config/no-write/offline/removal-versus-purge/replay-degradation positive and negative corpus at G06/G07/G11/G12/G18/G19/G21, with prototype baseline provenance and actual current product measurements. These are required implementation/release tests, not a claim that this design reference has executed the prototype or converted a database.
