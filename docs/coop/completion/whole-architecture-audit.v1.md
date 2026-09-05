# Whole-architecture implementability audit — v1

Auditor: fresh independent reviewer (Claude, this session), no authorship of any subject.
Status: AUDIT FINDINGS, binds nothing, edits no design bytes and no file 08.
Measured at HEAD `1eea066` (working tree at audit time); file 08
`872f0929926f996ee475642426c6ba33bec7bd6aa3eec6b6a927f2b197618bd6`.
Subjects and exact digests are pinned in `whole-architecture-audit.v1.json`.

Scope: actual implementability across every boundary of the integrated preview and every
inherited active obligation. Not re-reported here, because the lead named them as repairs in
progress: security v3's stock signed OS baseline (SEC2-M1), root semantic admission (SEC2-M4),
the witness/lease lock handoff (SEC2-M2), rollback claim bounding (SEC2-M3), name alignment
(SEC2-M5), the real G15 signed catalog/registry-view/multi-lock joins, and the doctor/cache mode
fixtures. Where a finding below touches one of those, it says what the repair must additionally
decide, and why the repair as named does not already cover it.

Reference models under `docs/coop/completion` are treated as design evidence only. Nothing here
claims or denies product qualification. The affected-row set of 23 and the nine deferrals are
preserved by the obligation map and by every finding below; no finding proposes a scope ride.

## 0. Summary

| Priority | Count | Character |
|---|---|---|
| P1 | 6 | A boundary cannot be built as written: missing decision, privilege the host lacks, or two accepted texts that contradict each other |
| P2 | 7 | Cross-unit inconsistency or omitted failure/fixture class that an implementer would have to invent |
| P3 | 4 | Bounded evidence-quality or specification gaps; cheap to close (WA-16 already resolved by a post-pin edit) |

The two largest structural problems are (1) the brokered-effect path has no lawful way for a
component to obtain the references it must send, and (2) the Linux runtime attestation the
accepted platform contract requires cannot be performed by an unprivileged process. Neither is
closed by the repairs in progress as they were described to me.

Rows affected by at least one P1: DR-101, DR-105, DR-107, DR-112, DR-114, DR-124, DR-125, DR-126.
Gates affected: G03, G04, G07, G09, G12, G18, G21, G22.

## 1. P1 findings

### WA-1 — No implementable acquisition path for `authorizationRef` / `operationRef` (DR-105, DR-124, DR-125, DR-102 boundary)

Traced through the accepted contracts:

- `control-protocol-contract.v2.json` `onTheWire`: `effectRequest` (component → host) "names an
  effect class token and an authorizationRef"; the channel is a courier and grants nothing. The
  sixteen message types, five descriptors (fd0–fd4) and the closed `hello`/`helloAck`/`select`/
  `selectAck` bodies carry no operation or grant handle. `control-completion.schema.v3.json`
  makes every unknown member RF-2 and bounds `authorizationRef`, `operationRef`, `resultRef` at
  1,024 UTF-8 bytes.
- `permission-truth-tables.v9.json` `PT-HOST-EFFECT-BROKERED`: "Every individual request still
  names one of the other tokens above as the effect it asks the host to perform", and "A request
  naming a denied token, an unknown token, or a scope wider than the grant is refused before any
  host effect is initiated." The accepted request semantics are request-carries-token-and-scope;
  the host decides and records request acceptance (RA) afterwards.
- `security-completion.v2.md` §7.1 (as v1): "`authorizationRef` names the `GRANT` record; the
  grant binds token, scope, operation, expiry and platform, so the request carries nothing else",
  with the §5.4 locator `gj:<base64url(projectKey)>:<grantGeneration>:<seq>`.
- `distribution-runtime-completion.v1.md` §8 `ProviderSession` exposes requests/respond/
  emitFacts/emitCoverage/reportFault/reportResources/complete and no effect-request operation,
  although `component-sdk-contract.v4` requires components to "use host brokers" and the control
  contract's fifth function is live.
- The TypeScript provider wire (`delivery.v2` HelloV1/HelloAckV1) is frozen and carries no such
  field; §6 fixes the worker's argument vector; the environment is host-constructed.

Consequence: under §7.1 a component must present a host-private journal locator that it has no
channel to learn, that embeds the opaque host-owned `projectKey` the lifecycle contract keeps
off every path and away from every caller, and that cannot exist before the request when the
journal's RA record is the acceptance of that very request. As written the brokered-effect
boundary is unbuildable, and the only fixture that could show it (FX-6/FX-8 effect flows,
G09/G21) would have to invent the delivery.

Independent challenge to the lead's proposal (authorizationRef-only 2,048-byte cap plus a
"bounded bootstrap handle delivery"):

1. The cap fixes a symptom. `gj:` + base64url of a 1,024-byte key + two counters is 1,406 bytes,
   so 2,048 admits it, but the defect is that `projectKey` bytes are on the wire at all. Nothing
   in v9, v25, control v2 or the lifecycle contract requires or permits the component to see the
   project key or the journal position; the lifecycle contract's own rule is that a caller
   supplying a key never acquires a namespace, so the value carries zero authority and pure
   leakage.
2. Any bootstrap delivery must use a channel the accepted contracts already permit. Permitted:
   the host-constructed child environment (v9 `PT-ENV-READ` is exactly "a named environment
   variable that the host places in the component process's own environment block", and FX-3
   already reserves "the host's declared structural allowlist"). Not permitted without reopening
   an accepted or SATISFIED row: a new member in `hello`/`helloAck`/`selectAck` (RF-2, DR-102
   SATISFIED at D-085), a seventeenth message type, a sixth descriptor, a per-operation value in
   the §6 fixed argument vector, or a provider-wire field.
3. Recommended shape (for the pair to decide, not this audit): `operationRef` is a host-issued
   opaque per-spawn value delivered in the constructed environment under a declared structural
   variable name, since control v2 fixes one `select` per child so one spawn is one operation;
   `authorizationRef` is either the accepted v9 request shape (permission token plus bounded
   scope, host maps to the grant) or a host-issued opaque grant handle bound to that spawn; the
   `gj:` locator stays host-internal and appears only in audit, doctor output and `effectResult`
   sequence numbers. That removes the bound problem, removes the key leak, and adds no wire
   member. Whichever shape is chosen, `control-completion` needs a v6 with at-bound and
   one-over-bound cases for the changed field, FX-3 needs the structural-variable case, and the
   SDK needs a typed `requestEffect` returning `effectResult` or an RF-6 refusal.

### WA-2 — Linux runtime attestation needs privileges the host does not have (DR-126, DR-114, G22, G12)

`platform-tcb-contract.v48.json` `filesystemMeasurementTarget.linux`: "The only lawful Linux
mountinfo reader is a dedicated helper that (1) receives the held ns fd, (2) enters that namespace
with `setns(nsfd, CLONE_NEWNS)`, (3) reads `/proc/self/mountinfo`, (4) exits ... setns failure
... refuses." `resolutionPredicate` step 1 requires this observation before any profile
selection, and `security-completion.v1.md` §3.3 places the DR-126 resolution predicate "at
launch". `security-completion.v2.md` §6.4 admits "the mount table via the v48 setns helper" as a
doctor read.

`setns(2)` with `CLONE_NEWNS` requires `CAP_SYS_ADMIN` in the user namespace that owns the target
mount namespace, including the caller's own current namespace. An unprivileged host therefore
gets `EPERM` and refuses on every launch. The Linux measured-boot bind (`measuredBootBind`,
`fromBootLockdown` reading authenticated `Boot####` data from the TCG2 event log) likewise reads
`/sys/kernel/security/tpm0/binary_bios_measurements`, which is root-readable only.

No contract decides a privilege model: no setuid or privileged helper, no requirement to run as
root, no privileged daemon, no split between qualification-time and launch-time observation. As
written, the Linux preview refuses for every non-root user.

Relation to the v3 repair: replacing the custom kernel with a stock signed baseline may change or
drop the measured-boot half. It does not touch `filesystemMeasurementTarget.linux`, which is the
install-root filesystem observation and is independent of the OS-ABI scheme. v3 must either
supersede the setns interface (for example an unprivileged `/proc/self/mountinfo` read with the
namespace inode retained as identity) or decide the privilege model explicitly.

### WA-3 — macOS attestation helper contradicts "framework absent" and is in the launch path (DR-126, DR-101, G02, G22)

v48 `platformAttestationOperation.macosCodesign` prescribes `SecCodeCopyGuestWithAttributes`,
`SecCodeCheckValidity` and `SecCodeCopySigningInformation` for the loader (`/usr/lib/dyld`)
member, evaluated at runtime resolution ("Any runtime resolution whose authenticity
identityEvidence ... is not an exact allowlist match" is drift). `distribution-runtime-completion.v1.md`
§2: the core "links libSystem only" and "Required TCB verification helpers are separate processes
with their own signed closure". `security-completion.v1.md` §8.2: "the qualification verifier (a
separate process) may use Security.framework"; v2 §8.3 declares the framework class "absent with
inapplicability proofs" for both macOS profiles.

These cannot all hold. If the helper runs at launch it is a mandatory closure member (counted in
G02's 80,000,000 bytes) that links Security.framework, so the framework class is not absent and
needs a PLATFORM-ATTESTED member of its own. If the helper is qualification-only, v48's runtime
drift refusal for the loader is not implemented on macOS and G22's "hostile loader" claim is
qualification-time only. Decide which, and record the helper's own closure and profile members.

The v49 `macos-sealed-boot` scheme adds `bputil -d` and `system_profiler SPiBridgeDataType` as
acquisition interfaces. Both are unverified on the adopted fleet (WA-7): hosted macOS runners are
virtual machines, `bputil` boot-policy display inside a VM is not measured anywhere in the unit,
and `system_profiler` costs seconds per invocation, which no launch-path budget admits.

### WA-4 — Install root location, ownership, discovery and multi-user model are undecided (DR-101, DR-107, DR-112, DR-114, DR-124, G02, G03, G04, G18)

Neither file 02, file 04, `lifecycle-generation-contract.v2`, `state-class-contract.v11`, nor any
completion unit states where the install root is, whether it is per-user or system-wide, how the
core executable locates it, or who owns `lifecycle.sqlite`, `trust.sqlite`, the "permanent
host-owned advisory-lock file" (distribution §5) and the project state namespace. The designs
require write access on every operation: the writer fence for every lifecycle mutation,
`evalHighWater` write-ahead on every trust evaluation (security v2 §4.2), lease rows, the journal
witness. The `.pkg` channel (security v1 §3.2 step 5) installs with administrator rights into a
system location; a second OS user on that machine then cannot analyze, cannot run doctor without
`UNDETERMINED` on every trust check, and (under WA-5) cannot run `--version` if it evaluates
trust.

G02 measures "a fresh immutable core installation with no previous generations", G04 measures four
doctor modes, and G18 injects death around durability boundaries; none of them can be authored
without the root's location and ownership. This is a missing decision, not a qualification
remainder.

### WA-5 — Read-only surfaces versus write-ahead trust evaluation and reconciliation-on-open (DR-112, DR-114, DR-124, G04, G12)

`security-completion.v2.md` §4.2: "Whenever the trust machine evaluates any expiry, staleness or
future-time predicate it first computes `t` ... durably writes `evalHighWater = t` (its own SQLite
transaction, `synchronous=FULL`) and only then evaluates." §5.4: reconciliation on open of a
journal reverts, advances or quarantines the witness. Doctor's default is read-only (file 04;
`security-dependency-inventory.v1` ID-DEP-6 "Do not mutate trust high-water during default
read-only doctor"; ID-DEP-7 actor-scoped FC-RO). The in-progress `doctor-cache-check.v1.py`
`mode()` trace asserts `writes: []` for every mode. So the fixture and the trust design contradict
each other by construction: a doctor that reports trust state either writes, or evaluates with an
unpersisted `t` that §4.2 forbids, or reports recorded state without evaluating and cannot say
whether the catalog is expired.

Decide a non-persisting report-only evaluation (no decision is taken, so the write-ahead
invariant is not needed) or a doctor that reports recorded counters plus the recorded
`evalHighWater` without evaluating, and state which one the FC-RO and FC-MODE fixtures assert.
The same decision must say whether journal open in doctor performs reconciliation (a write) or
reports a would-reconcile state as a check.

### WA-6 — What `--help`/`--version` verify at launch is undecided, and the G03 budget cannot absorb the default reading (DR-101, G03, G07)

`security-completion.v1.md` §3.3: "At launch: the DR-G07 open-then-verify of the same immutable
objects, plus the DR-126 resolution predicate." `reference-handoff.draft.md`: "Help/version and
admission use authenticated metadata." D-006 G03: cold p50 ≤ 100 ms for `--help`/`--version`,
"loads no components and no project". Nothing exempts help/version from launch verification.
Hashing an inventory of up to 80,000,000 bytes on a cold cache, spawning the WA-3 helper, opening
`trust.sqlite` and (under §4.2) performing one durable write per launch cannot meet 100 ms p50,
and on macOS a durable write is `F_FULLFSYNC`, not `fsync` (WA-9).

Decide the launch-verification scope per command class (metadata-only commands verify what,
against which envelope, with or without trust evaluation), record it as the G03 fixture's
falsification condition, and make G07's "at launch" claim match.

## 2. P2 findings

### WA-7 — Profile OS selectors and G13 runner class contradict the adopted D-102 fleet (DR-126, DR-118, G03, G04, G13, G22)

`coordinator-decisions.D-102.turn2.draft.md` (adopted) names `macos-15` (3-core M1, 7 GB),
`macos-15-intel` (4 CPU, 14 GB) and `ubuntu-24.04` (4 CPU, 16 GB) hosted images as the G03/G04
fleet. `security-completion.v2.md` §8.3 pins both macOS profiles to build `25G83` (macOS 26.6.2)
with "Runner requirements: Full Security boot policy, sealed root, SIP, build 25G83"; §8.4 pins
Linux to the OpenSIP kernel image (being replaced by v3, but still an image D-102 did not name).
`analysis-quality-completion.v2.md` §3 requires "a dedicated four-vCPU/eight-GiB worker for each
target", which `macos-15` cannot supply.

On the D-102 fleet no complete macOS profile matches, so the core refuses (NT-TCB-1/3) and the G04
doctor-mode fixtures measure a refusing host. D-006 MF-2 binds every number to one named runner
class chosen with product sign-off. Either re-measure the profiles on the D-102 images or record a
D-102 successor; G13 must name its runner from the same table.

### WA-8 — The worker's "fixed argument vector and cleaned environment" have no content (DR-120, DR-125, DR-105, G14, G09)

`distribution-runtime-completion.v1.md` §6 says the host invokes the bundled Node with "a fixed
argument vector and cleaned environment"; v9 FX-3 asserts "no variable outside the grant plus the
host's declared structural allowlist appears". Neither the vector nor the structural allowlist is
enumerated in any unit. Node 24 reads ambient inputs unless neutralised on the command line:
`NODE_OPTIONS`, `NODE_EXTRA_CA_CERTS`, `--icu-data-dir`, `--env-file`, `UV_THREADPOOL_SIZE`, `TZ`
and locale variables, and an OpenSSL configuration file from OpenSSL's compiled-in default
directory (`--openssl-config` / `OPENSSL_CONF`; verify against the pinned Node 24 documentation
before relying on the exact flag). G14's "hostile PATH/loader/system-tool substitutions" and FX-3
cannot be authored without the declared set. WA-1's bootstrap variable belongs in this same
allowlist.

### WA-9 — Durability primitives are assumed equal across platforms; I/O failure classes are absent (DR-107, DR-124, G18)

Distribution §5, security v2 §5.4 and `lifecycle-carrier.contract.v2.json` treat "fsync file,
rename, fsync directory" and `synchronous=FULL` as durable. On macOS `fsync(2)` does not flush the
device; durability needs `F_FULLFSYNC` (`PRAGMA fullfsync` for SQLite), which costs tens of
milliseconds on APFS and interacts with WA-5/WA-6. Every unit disclaims power-loss qualification,
but no unit decides the primitive per platform, so an implementer chooses.
`lifecycle-carrier.cases.v2.json` has zero cases for ENOSPC, EIO, short write, or a failing fsync,
and security FX-4 enumerates crash points, not I/O errors. Add the failure class per durability
boundary (publication, selection commit, witness, `evalHighWater`, quarantine) with the expected
typed refusal and no partial state.

### WA-10 — Doctor OC→D9 and permission PR→exit joins remain unmapped (DR-114, DR-105, G12, G09)

`security-dependency-inventory.v1` leaves ID-DEP-1 (doctor OC-1..OC-5 → D9/exit) and ID-DEP-P1
(PR decision → exit) ACTIVE-JOIN-UNVERIFIED. `security-behavior-model.v3.py` derives OC-1..OC-5
but no unit cites the D9 v1.14 class and exit for each, nor for an RF-6/PR-n refusal during
`analyze`. FC-D9 (OBL-DOCTOR-FX-AUTHORING) cannot be authored until this mapping exists. Not in
the named repairs. Two inventory items are now answered and should be closed there: ID-DEP-3
(S-DOCTOR is present in `compatibility-matrix.completed.v4.json`) and ID-DEP-8 (distribution §8.1).

### WA-11 — Project and host configuration carrier is undecided (DR-103, DR-114, DR-105, G12)

Distribution §8.1 has doctor project mode read "strict configuration and the selected lock"; §3
requires every resolution-affecting input (requested profile, capabilities, pins/holds, allowed
scopes, `permissionPolicyDigest`) to be "serialized, rather than read from ambient local state";
security §6.3 needs a "pre-existing policy carrier" for CI. No accepted contract or unit defines
the configuration document: schema major, location (project and host), precedence, or who writes
the permission policy file. DR-103 ID-DEP-12 closed only the classification vocabulary. The
in-progress `doctor-cache-check.v1.py` reads `host/settings.json`, `project/opensip.json` and an
interactive-only `project/local.json`, which is a precedence rule that exists in a fixture and
nowhere else. Decide the carrier before the doctor, lock and permission fixtures bind to it.

### WA-12 — Project-root identity refuses common developer filesystems (DR-107, DR-124, G18)

`lifecycle-carrier.contract.v2.json` `projectRegistry`: Linux binding requires `STATX_BTIME`;
"Production Linux roots without STATX_BTIME refuse binding." Bind mounts inside containers
(overlayfs), NFS, 9p/virtiofs shares used by Docker Desktop and VMs, and older tmpfs do not
return a birth time. The preview would refuse analysis in those environments with no decided
refusal class or D9 mapping. Decide the supported project-root filesystem set (distinct from the
DR-126 install-root profile member) and the typed refusal, and add the fixture class.

### WA-13 — Project purge/retirement crosses three carriers with no ordering (DR-124, DR-107)

Security v2 §5.4 advances `grantGeneration` at "project purge"; the lifecycle registry retains
retired tombstones and forbids reuse; the admitted registry (`registry.schema.json`) carries
`projectKey` on every project-scoped entry. DR-113 purge is deferred. Either project retirement is
in the preview, in which case the order across registry entries, selection, journal namespace and
tombstone must be specified with crash points, or it is not, in which case §5.4's purge cause is
unreachable and should say so.

## 3. P3 findings

### WA-14 — SDK "generated types" need a pinned generator or a committed-output rule (DR-125, DR-120)

Distribution §8 generates SDK types from the pinned schemas; §6 names only `lib/tsc.js` in the
tool closure and forbids reads outside the inventories. Either the generator is a tool-inventory
member or generated types are source-inventory members with a digest join to the schemas.

### WA-15 — Catalog `hostCoreConstraint` duplicates manifest `compatibility.hostCore` with no mismatch rule (DR-103, DR-111)

**Verified after delivery:** `compatibility-selection-model.v5.py` line 137 requires
`release['hostCoreConstraint'] == m['compatibility']['hostCore']` (`COMPATIBILITY-CATALOG-JOIN`); the
lead reports the distribution text now states it. No action remains beyond that text landing.

Both are signed under different roles (TR-INDEX, TR-COMPONENT). `g15-conditional-author.v1.py`
copies one from the other, so the fixture cannot show a mismatch. State which one admission
evaluates and that inequality refuses. May already be inside the in-progress G15 joins; verify.

### WA-16 — G01 measured container must be named now that two containers exist (DR-101, G01)

**Resolved in current bytes after this audit's pin.** `distribution-runtime-completion.v1.md` §2 now
reads "G01 scores every offered compressed core download container independently on each platform:
both macOS `.pkg` and `.tar.zst`, and Linux `.tar.zst`" (on-disk digest `a2adbbac…`, pinned digest
`f4ec12c7…`). Retained for the record; no action remains.

Security v1 §3.2 step 5 ships a `.pkg` and a `.tar.zst` per macOS platform. `harness.DR-G01.core-download.v11`
measures "exact signed compressed closure" per platform. State whether both, or which, is the
G01 subject.

### WA-17 — Performance workload does not exercise the rule it budgets (DR-118, G13)

`quality-corpus-manifest.v1.json` `performance.seed` is `linear-chain-0-through-999` with
`expectedCycles: []`. The pack's only rule is strongly-connected-component detection; the
budgeted workload contains no cycle and 999 edges. Keep the chain as one workload and add a
cyclic one, or record that latency thresholds bind to the chain only.

## 4. Checked and found consistent

- Control v5 bodies match security §7.1/§7.2 shapes (effect classes, outcome enums, sequence
  semantics) except for the locator problem in WA-1.
- `compatibility-matrix.completed.v4.json` carries S-DOCTOR with the dual window; ID-DEP-3 holds.
- Distribution §8.1 settles doctor v4 T-2 for the G04 mode budgets; ID-DEP-8 holds.
- Scope rides SD-1..SD-8 are a closed set with trigger and owner each; none removes a row.
- The obligation map preserves the 23-row affected set and the nine deferrals; all 47 prior
  obligations are PENDING-INTEGRATION with empty evidence, which is expected before application.
- Lifecycle v2 SQL enforces the state machine and collision rules the notes claim.

## 5. Limits of this audit

Read-only. I executed none of the retained checkers. I did not measure any platform. Each
finding cites the bytes it rests on; a finding is withdrawn if those bytes are shown to say
otherwise. The per-row application-grade and SATISFIED-grade reviews of the frozen integration
remain separate later acts.
