# Host roots and preview configuration

Author: Codex lead. PROPOSED; no register edit or implementation authorization.
This unit closes whole-architecture findings WA-4, WA-11 and WA-12 and states
the preview interpretation of WA-13. It supplements distribution-runtime §5/§8
and inherits lifecycle-carrier v2's identity, lease and publication rules.

## 1. Installation and ownership

There are two different roots. **Core payload root** is the immutable installed
release containing `bin/opensip` and its signed inventory. The host obtains its
actual executable path from the OS, retains the opened executable identity, and
resolves the payload root as the parent of `bin`, without consulting argv[0],
PATH, current directory, project configuration or an environment override.
An executable lacking that layout is a required-delivery failure for commands
that need the payload. Help/version use the embedded data and command-specific
verification rule in the paired security successor. They do not initialize state.

The macOS `.pkg` installs core payloads under
`/Library/OpenSIP/core/<release-version>/<platform>/`, owned by root with
directories 0755 and regular data 0644/executables 0755. The installer may
create `/usr/local/bin/opensip` as a launcher symlink to that immutable binary;
discovery resolves the executable, not that symlink's parent. The tar channel
extracts the identical payload layout into an explicitly chosen empty directory.
It does not install into PATH or change user configuration implicitly. Its
payload must be owned by the invoking user or root, with no group/other write
permission; admission checks the complete immutable path chain. A new core
release is a separately installed payload; preview does not implement self-update.

**Operational install root**, called `installRoot` by lifecycle and trust
contracts, is private to the invoking OS account. Resolve its home directory
through the OS account database (`getpwuid_r` for the effective UID); never use
the inherited HOME/XDG variables. The fixed locations are:

| Platform | Operational install root |
|---|---|
| macOS | `<account-home>/Library/Application Support/OpenSIP/preview-v1` |
| Linux | `<account-home>/.local/state/opensip/preview-v1` |

No initial-preview override selects a different operational root. Test harnesses
may inject a root into a reference model; that is not a CLI or environment
authority. This root is local APFS on macOS or local ext4 on Linux, independently
of the core payload's location and the source project's filesystem observation.
Every created directory is 0700, every mutable regular file 0600; executable
generation members retain their declared executable mode, with no group/other
access. Verify the root and owned descendants no-follow, effective-UID ownership,
and absence of group/other writes before opening writable state. Verify each
existing ancestor is a directory owned by root or the account and not writable
by other principals. A symlink or unsafe ancestor refuses; no repair/chmod of
an existing unsafe tree is implicit. A missing writable root may be created only
by an explicit state-using operation, with create-new, durable publication and
the same checks. Read-only commands report absence without creating it.

The root contains `lifecycle.sqlite`, `trust.sqlite`, `lifecycle.lock`,
`generations/`, `staging/`, `quarantine/`, `projects/<namespaceId>/`,
`settings.json`, `policies/permission-policy.json`, and `cache/`. NamespaceId is
the immutable lifecycle UUID, never projectKey bytes. A project namespace owns
its `grant-journal.sqlite`, operation-lock files, local permission policy and
registry-view exports. All lifecycle publication paths and SQLite sidecars are
on this root's one filesystem. SC-OPS/SC-TRUST are not in `cache/`. Cache deletion
cannot delete a journal, witness, selected generation, permission or registry.

The lifecycle `project_registry` binds the opaque projectKey to its immutable
namespaceId and the derived projectKeyDigest = SHA-256(projectKey UTF-8 bytes).
The digest may be computed from the retained key rather than redundantly stored.
Both `grant-journal.sqlite` and `grant-journal.witness.json` live under
`projects/<namespaceId>/`; journal locators and witness carrier identities use
projectKeyDigest plus grant generation. Neither projectKey bytes nor its digest
is a filesystem path component. Restoring that binding is a verified lifecycle
operation, never inference from a directory name.

Each provider spawn with broker handles gets the private transport directory
`projects/<namespaceId>/spawns/<spawnId>/`, where spawnId is the host's fresh
opaque UUID (not a provider input or operationRef). The host creates it under
the held project operation lease, mode0700, and binds its held directory fd to
that spawn and current project. This is the security courier's resultScratchRoot;
its `stage/` child is also0700. It is ephemeral SC-OPS transport state, not a
retained generation or analysis/cache artifact. A preview component with nonempty
handles always belongs to an admitted project operation; global/core commands
have no provider spawn. The SDK gets the path only in its structural bootstrap
and never exposes it to provider callbacks.

The host cleans this spawn directory after the child has exited and all courier
readers/writers have stopped, while retaining the operation lease. The normal
terminal path, refusal, cancellation and crash cleanup use the same ownership
rule. After supervisor death, recovery/GC may delete an orphan only after the
lifecycle fence's nonblocking census proves its operation lease released; an
uncertain or live lease preserves the directory. No generic cache cleanup may
cross into spawns. These bytes are outside G02's immutable core payload, but count
against the explicit courier's per-result/per-spawn caps and any operational
state measurement that names them. G18/G21 own cleanup, no-use-after-reap and
size/custody cases; actual OS/process qualification remains required.

The permanent lifecycle fence guards concurrent first creation as well as later
mutation. Its create-new/open-no-follow protocol accepts an already existing
correct owner/mode file; it never replaces its inode. Before initial databases
are published, one fence holder validates or finishes their exact recorded
initialization; partial/mismatched state refuses for recovery. Root/bootstrap
metadata comes from the signed core payload, with the pinned non-TOFU root;
initial permission policy denies everything unless a separate authorized operator
policy exists. No package installer creates per-user grants or mutable trust.

Two OS users can run the same system core; each has independent installId,
trust high-water, component generations, selections and grants. There is no
shared writable service, setuid executable, privileged daemon or cross-user
grant reuse. A different core release for the same user reads the same supported
state-major root subject to the independent compatibility contract. Actual core
and component sizes remain separately visible; writable state is not silently
excluded from an installed-generation measurement that names it.

## 2. Project binding and lifecycle boundary

`analyze --project <directory>` selects that explicit directory; without it,
the host walks from the opened current directory to the nearest ancestor with
a regular `opensip.json`, stopping at filesystem root. No match selects the
opened current directory with compiled defaults. The path is resolved once and
the canonical directory handle is retained. Help/version and explicit doctor
core mode never perform this search. Doctor's existing explicit/implicit project
mode selection stands; failure after selecting a project never falls back to core.

Supported preview project roots are local APFS or ext4 with an observable,
stable device/inode/birth-time tuple. The host observes the selected root's own
filesystem, independently of the operational root. A container or bind mount
is admitted only if its actual observation satisfies this contract; no container
brand is assumed to provide a birth time. NFS, SMB, overlay, 9p, virtiofs, tmpfs
and an absent/unsupported birth-time result are not admitted by this profile.
There is no timestamp-from-mtime fallback and no weaker inode-only identity.

An unsupported user-selected project root is pre-admission `config-invalid`,
using the existing D9 request-rejected/exit-2 mapping with diagnostic
`project-root-identity-unavailable`; no namespace, selection, grant or analysis
attempt is created. In doctor project mode it is an explicit UNDETERMINED
identity check and uses the existing doctor OC/D9 mapping. An I/O failure while
observing an otherwise supported root uses the existing host-I/O operational
failure, not a fabricated unsupported-filesystem observation. A persisted
registry/root mismatch follows lifecycle corruption/quarantine rules.

This is a declared preview filesystem support boundary, not evidence that all
four platforms have been tested. G18 retains same-root/moved-root/replaced-root,
unsupported-filesystem/missing-birth-time, separate-user and read-only-absence
fixtures; G12 verifies mode and refusal projection. Lifecycle + security own it.

User-visible project retirement, purge, adopt/import, or fork is not activated
by this unit: DR-113 and the existing identity re-entry dispositions remain.
Lifecycle tombstones remain a defensive storage shape, not a new command.
Security's project-purge grant-generation rollover cause is unreachable until
that re-entry is reviewed. Active quarantine, counter-exhaustion rollover and
detected-restore refusal remain active and do not purge a project implicitly.

## 3. Configuration carrier and resolution

The exact bounded JSON carrier is `preview-configuration.schema.v1.json`.
All input documents are strict UTF-8, duplicate-key-free JSON objects, at most
4 MiB, depth 32, with no non-finite number, surrogate, trailing data or unknown
member. Absent files supply no layer; an existing unreadable or invalid file
is an error. Inputs are data only; no executable config, include, interpolation,
secret value, projectKey, installId or implicit extension key is permitted.

The preserved six-layer order is defaults, global, tracked project, interactive
local, allowlisted environment, flags. Locations and initial preview fields:

| Layer | Carrier | Admitted fields |
|---|---|---|
| 1 | Compiled defaults pinned with core | Fixed preview profile/capabilities and signed-profile component request; absent stage budget; empty pins/holds |
| 2 | `<installRoot>/settings.json` | `analysis.budget` only on the semantic path; `ui.color` only on presentation |
| 3 | `<project-root>/opensip.json` | `analysis.budget`, `components.request`, `components.pins`, `components.holds`, `components.allowedScopes` |
| 4 | `<project-root>/.opensip/local.json` | Same fields as layer 3, only in local-interactive mode |
| 5 | Constructed input from declared environment keys | Empty semantic allowlist in this preview |
| 6 | Parsed command flags | `--budget-work-units <positive-decimal>` maps to `analysis.budget`; project/mode/output flags are host selectors, not private provider fields |

Each file has required `schemaVersion: 1`. `ui.color` is one of `auto`, `always`, `never`. The budget flag is canonical positive ASCII decimal `[1-9][0-9]*`, without leading zero or sign, checked against the uint53 ceiling. `analysis.budget` is exactly
`{unit:"work-units",limit:<integer 1..9007199254740991>}` and supplies the existing
admitted C-2 stage budget, whose six-dimensional TypeScript projection remains
delivery.v2's `stageRequestProjection.budgetProjection`. Absence uses the signed
provider's existing default profile; elapsed time never changes this budget.
This chooses a bounded preview configuration domain within the existing uint64
protocol domain, not a new wire number or a default performance promise.

Component request/pin/hold item grammars are exact copies of the corresponding
`component-lock-schema.completed.v3.json` resolutionInputs members, capped at
128 items each. Requests cannot be empty; duplicates/conflicts and dangling
pins/holds refuse through the existing resolver. `allowedScopes` is exactly
`["global"]` or `["project","global"]`. Initial signed install-profile defaults
provide the TypeScript request; no unknown UUID or example release is hard-coded
as a shipped artifact. Profile `preview-typescript` and the five declared
capabilities are fixed defaults, not user-overridable quality reductions.

Resolve by leaf: a present higher-layer scalar or whole array replaces that
field; absence preserves the lower layer. `analysis.budget` is one atomic value,
never a merge of unit from one layer and limit from another. Empty pins/holds
explicitly clear earlier lists. No `null` reset is accepted. Winning array values/order remain unchanged in resolved configuration and provenance; a separate canonical sorted resolutionInputs projection supplies the existing resolver. Reject duplicate/conflicting IDs before projection, so sorting cannot erase a conflict. Preserve per-field
`decidingLayer` and exact value in the existing resolved-input path; only semantic
fields reach the analysis request. The preview does not create a sealed PlanId
or alternative identity recipe by recording this provenance.

CI/non-interactive mode does not stat, open, parse or resolve layer 4; malformed
or hostile local bytes do not reject it. Local-interactive requires both a TTY
invocation and no `--ci`; otherwise the invocation is non-interactive. Existing
mode semantics for explicit automation stand. An unlisted ambient variable is
not a config field. Unknown tracked/local keys or authored invalid values use
config-invalid/request-rejected; invalid compiled defaults or an impossible
host-created environment/flag projection are host invariant failures. Global
keys outside this closed schema refuse at config validation and never enter
analysis. This does not weaken CFG-9's broader V1 allowlist: other V1 keys are
not exposed by this narrower fixed-profile preview, and cannot introduce an
ambient toolchain, disabled required provider, lower floor or execution grant.

Doctor reads and validates these same carriers and shows their provenance but
does not allocate a namespace, mutate selection, build an analysis snapshot or
spawn a provider. The doctor/cache v1 fixture's `host/settings.json`,
`project/opensip.json`, `project/local.json` and `project/lock.json` are fixture
mount aliases for the paths here and the already selected host-owned lock; they
are not four additional production paths or a separate configuration resolver.

## 4. Operator permission carrier

Permission is separate from semantic configuration. Global policy lives at
`<installRoot>/policies/permission-policy.json`; project policy, if present, lives
at `<installRoot>/projects/<namespaceId>/permission-policy.json`. Each uses the
security unit's closed policy schema and the matching `policyScope`. A repository
file is never a policy source. Missing policy is the explicit empty deny-by-
absence policy; its canonical bytes and digest are still well-defined. A
missing project namespace supplies no project policy and must not be created
merely to check permissions in doctor.

The OS-account operator or that account's deployment automation authors these
files out of band, using atomic replacement with private ownership/mode. This
does not require a new preview policy-editor command. The host reads no-follow,
validates exact bytes under the lifecycle fence and retains its parsed immutable
snapshot; malformed/unsafe policy refuses affected operations. On a new operation
it re-reads and binds the current policy digest, rather than trusting mtime.
Replacing a policy file does not itself authorize an effect. Global/project
combination retains the permission truth table's deny-wins and scope rules;
the host alone creates a GRANT bound to concrete current operation/component/
generation/platform, and CI requires a matching pre-existing policy. Interactive
consent uses the existing recorded consent path. A layer-3/4 config document,
lock, manifest or component cannot write or nominate this carrier.

## 5. Evidence, numeric ownership and substitution

The 4 MiB cap reuses the completed metadata bound; depth 32 reuses bounded host
report/config traversal. The 128-item request/pin/hold cap supports independently
released dependency closures while bounding user-authored constraint work below
the existing solver visit/depth limits. Equality passes, one over refuses before
allocation or resolution. Product + host own these D-006-form choices; retained
representative project/constraint fixtures and the at/over boundary cases are
their design evidence. A legitimate supported project needing more entries is
the falsification signal for an explicit reviewed cap successor, never silent
truncation. The work-unit limit is a user choice with no automatic increase.

G12/G18 execute configuration precedence and exact no-layer-4-read, private root,
filesystem identity/refusal and policy-custody cases. G09 validates no repository
grant and current host policy binding. G03/G04 retain no-project help/core-doctor
and bounded metadata-only behavior. Reference tests here are design evidence;
actual OS ownership, race, filesystem and process checks remain qualification.
A substitute root/config mechanism must preserve all these properties, the six
layer law, independent per-user trust and the same gates; it requires a reviewed
architecture successor. No placeholder location or implementation choice remains.
