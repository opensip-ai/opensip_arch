# Security, trust and platform-TCB completion — lead-owned corrective integration v6

Author of corrective integration: Codex lead. Inherited design and reference evidence:
Claude v5, retained with attribution in the predecessor freeze. Status: PROPOSED;
no technical acceptance, register edit, implementation authorization or platform
qualification is asserted. Authority: security-lead-correction.v2.md and its
independent procedural CONSENT and recorded addendum. The complete unit requires
fresh independent LEAD-CORRECTION-REVIEW by a reviewer who authored none of its bytes.

Cumulative history: three ordinary exchanges; one UPHOLD adjudication; two failed
bounded confirmations (v4 and v5); zero completed LEAD-CORRECTION-REVIEW exchanges.
This is not a reset or another confirmation under the exhausted first exception.
All earlier frozen units and failure probes remain unchanged. M1/M3/M4/M5 and
inseparable regressions are repaired here; M2/M6, N1 and caps remain governed by
their accepted dispositions. The exact per-file diff against v5 accompanies the
freeze. Every failed lead review is reported to the user before any further round.
Date: 2026-09-04. Scope and qualification standing are unchanged.

## 0. Pins, retained files, repair map

### 0.1 Pins

HEAD at corrective authoring `5e1160a`; file 08 `872f0929926f996ee475642426c6ba33bec7bd6aa3eec6b6a927f2b197618bd6`.
Incorporated recorded contracts and their digests are exactly the table in `security-completion.v1.md`
§0; the v1 and v2 §0 lists stand. Paired units: the operative normative pack is `distribution-foundation-reference-freeze.v2.json`
(`bad1e956…`); its distribution and foundation v2 supersede the historical v1 reads, `scope-rides-completion.v2.md` `d22d7cc3…` (rides SD-1..SD-8), `analysis-quality-completion.v2.md`
`08fb0806…`, `security-dependency-inventory.v1.md`, `d9-exit-contract.v1.14.json`
`8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31`, `operability.v10.json` `9bacbbf4…`,
`control-completion.schema.v3.json` `2929de62…` (effect bodies; `authorizationRef`, `operationRef`,
`resultRef` at 1,024 UTF-8 bytes, unchanged by this unit), `broker-bootstrap-impact.v1.json`, the
lead's bootstrap v2 unit (independent NO-OBJECTION, 150 checks), `whole-architecture-audit.v1.md`
`f3c8620c…` (WA-1, 2, 3, 5, 6, 7, 9, 10, 13 answered below), `legacy-corpus-checker-audit.v1.md`
(G07 and G22 crosswalk, §8.8), `coordinator-decisions.D-102.turn2.draft.md` (runner classes, §8.7),
and the lead's foundation decisions (per-user operational root, project purge deferred to DR-113,
global plus project-private policy files).

Retained with this document, all under `docs/coop/completion/`: `security-schemas.v6/` (eleven closed
JSON Schemas plus `grant-journal.sql`, byte-identical to v4), `security-fixtures.v6/` (54 files),
`security-vectors.v6.json`, `security_unit_lib_v6.py`, `check-security-unit.v6.py`, and the frozen report
`security-unit.v6.report.json` (751 checks, 0 failures; cross-validated through the review
environment's `jsonschema` 4.25.1). Every fixture under §7, §8.7 and §8.8 is SYNTHETIC: it demonstrates
that the design is authorable and that its admission logic is executable; genuine OS execution on the
named runner classes is qualification and is not claimed anywhere in this unit.

### 0.2 Repair map

| Finding | Landed at |
|---|---|
| SEC2-M1 stock Linux platform | §8.4 v49 `publisher-signed-boot`; kexec-absent kernel, `builderAttestation`, KB-1 withdrawn; honest no-hostile-kernel-detection in §1 |
| SEC2-M2 lock handoff and witness | §5.4 race-free fence→lease handoff; full reconciliation table, executable (`reconcile_witness`), fourteen retained cases plus simulated crash points |
| SEC2-M3 rollback claims | §1 and §5.5 bounded to detected or declared restores |
| SEC2-M4 root semantic admission | §3.1 `admit_root` before any signature; twelve retained negatives; the weak-threshold probe cannot verify |
| SEC2-M5 names | §2.1 registry-view domain in the table; §5.1 `trustEpoch` quadruple with `indexSnapshotVersion`; §5.4 uint53 `seq` vs i64 metadata counters |
| WA-1 acquisition path | §7.4 per-grant opaque handles `ah:<32 hex>` on the wire, delivered in the bootstrap descriptor; the `gj:` locator is host-internal only and now a fixed digest form (§5.4); both the broker grant and the underlying token grant re-verified on every request; no control schema change, no 2,048-byte cap; §7.5 result courier |
| WA-2 Linux privileges | §8.4 unprivileged launch predicate; v48 setns helper superseded by a same-namespace `mountinfo` read bracketed by `/proc/self/ns/mnt` equality; TPM event log qualification-only; explicit privilege model |
| WA-3 macOS helper | §8.3 the Security.framework helper is qualification-only and not a launch-closure member; launch computes the loader cdhash in-core and reads sysctl/`csr_check`; boot policy is qualification-only and `virtualized-not-observable` on hosted images |
| WA-5 read-only doctor | §4.8 report-only evaluation at `max(evalHighWater, wall clock, lastAccepted)` with no write; would-reconcile journal state reported, never written |
| WA-6 launch verification | §3.3 per-command-class table; `--help`/`--version` verify nothing beyond exec and open nothing; operations verify executed members on their opened fd |
| WA-7 fleet | §8.7 runner table over the four D-102 classes; the 25G83 templates are development measurements; release profiles are measured on their class; G13 thresholds apply per class on all four |
| WA-9 durability | §5.6 per-platform primitives (`F_FULLFSYNC` on macOS), seven boundaries × eight error classes, post-visibility failures UNDETERMINED with reconcile-before-use |
| WA-10 joins | §6.9 |
| WA-13 purge | §5.4 project purge is not in the preview (DR-113 deferred); `grantGenerationClosure` reachable only by whole-generation REV and the uint53 rollover |
| Legacy-corpus audit G07/G22 | §8.8 observed-event admission probes (38 retained cases over the four templates) and the exact crosswalk of the seven loader and five TOCTOU G07 states |
| Bootstrap v2 MUST (broker token alone) | §7.4 `EFFECT_UNDERLYING_TOKEN`: HE-2 needs PT-FS-READ-PROJECT and HE-1 needs PT-FS-WRITE-HOST-STATE in addition to PT-HOST-EFFECT-BROKERED, checked at every request under the existing precedence |
| Lead pre-freeze advisories | §5.6 UNDETERMINED post-visibility durability; §4.2 evaluation time and exact expiry/freshness boundaries; §6.11 effective policy digest identifying both files |

**Turn-4 repairs (each UPHELD by the adjudicator; every counterexample retained as a negative):**

| Finding | Landed at |
|---|---|
| SEC3-M1 root closed/semantic boundary | §3.1 `kernelAttestationKeys` must be exactly `[]` (schema `maxItems 0` and refusal `ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY`); duplication checked on every key list including `recoveryAuthority`; one boundary `admit_root_document` = parse → schema → semantic rules returning an `AdmittedRoot`, the only root value `verify_envelope` accepts (a raw dictionary is `ROOT-NOT-ADMITTED` before any step); negatives `M1-kernel-attestation-key-present`, `M1-recovery-repeated-key` |
| SEC3-M2 policy traversal | §6.11 every `pathPrefixes` member of a raw policy must be a normalized member path at source admission (`POLICY.PATH_PREFIX_NOT_NORMALIZED`), narrowing compares whole segments; negatives `src/../private`, `src/../../outside`, `src/./x`; controls `src/a` (legal descendant) and `srcx` (sibling, refused) |
| SEC3-M3 malformed witness | §5.4 closed witness shape validated before any comparison; any violation quarantines `witnessMalformed`; negatives: bool `seq`, hashless PENDING, PENDING 0 on an empty carrier, unknown member, missing schema member, bool generation; the string sentinel is itself a malformed witness |
| SEC3-M4 mandatory broker/courier context and exact grammar | §7.4 `verify_effect_request(body, ctx)` refuses `AUTHORIZATION.CONTEXT_ABSENT` unless the connection map, current binding, journal state and the sealed snapshot manifest are all present; both the broker grant scope and the underlying grant scope must be non-empty (`GRANT_SCOPE_EMPTY`) and contain the exact prebound target; the underlying HE-2 scope must name the sealed snapshot (`SNAPSHOT_BINDING_MISSING_OR_MISMATCH`); membership is always checked (`TARGET_NOT_SEALED_MEMBER`); §7.5 `resolve_result(ref, reader, ctx)` takes one required context record (`RESULT.CONTEXT_ABSENT`); every wire grammar is a full match (a trailing newline is refused); pure helpers are named `_target_within_scope` and are not the enforcing boundary |
| SEC3-M5 HE-1 order | §7.5 explicit ordered algorithm RA → RCI or ICI → effect from the immutable buffer → RCO or ICO → unlink stage → result; `he1_recover` retained with twelve crash cases: the footprint decides, never the missing record; irreversible intent with an undeterminable footprint is INDETERMINATE |
| SEC3-M6 Linux profile identity | §8.4 and §8.7 the kernel flavor and series are RELEASE-MEASURED per D-102 class (the `ubuntu-24.04` image 20260823.283.1 boots `6.17.0-1022-azure`, primary source cited); release templates carry placeholders for flavor, series and package pattern; two ILLUSTRATIVE filled examples (`azure-6.17`, `generic-6.8`) admit nothing; `linux_os_abi_predicate` retained with twelve cases including the wrong-series negative; the four-class fleet is unchanged |
| SEC-POLICY-N1 (lead, separate) | §6.11 a raw policy with a repeated `(stableId, token)` among its grants refuses `POLICY.DUPLICATE_GRANT_PAIR`, among its denies `POLICY.DUPLICATE_DENY_PAIR`; a grant and a deny of the same pair is lawful and the deny wins; same-scope and conflicting-scope duplicates retained |
| Lead's cap interpretation | §7.5 the 64 MiB per-spawn cap counts retained HE-2 results; HE-1 staging is separately bounded by at most four single-use handles × 16 MiB; conservative scratch maximum 128 MiB with the D-006 rationale |

**Historical v5 repair claims (the second confirmation found the remaining gaps listed in §10), bounded to the four unresolved IDs; every failed probe retained as a
negative with its positive control:**

| Unresolved finding | Systemic corrective landed at |
|---|---|
| SEC3-M1 (mutable public carrier; verify without shape recheck) | §3.1 `AdmittedRoot` is an immutable carrier (canonical copy, fresh copies only, no setter); `verify_envelope` re-runs the complete parse → schema → semantic boundary on the value it receives and re-derives the digest before any use; a directly constructed carrier over an invalid root or with a wrong digest is `ROOT-NOT-ADMITTED`; a mutated copy never reaches the held state; exceptions inside the boundary are refusals. Retained: `root-boundary-cases.json` (the three exact probes and three controls) |
| SEC3-M3 (absent hash member conflated with null; KeyError) | §5.4 the witness shape requires the `bodySha256` member to be present (null only at COMMITTED 0); the journal tail is validated; `reconcile_witness` is an exception-free boundary (any exception quarantines). Retained: `M3-genesis-missing-hash`, `M3-tail-malformed`, `M3-witness-is-a-list` |
| SEC3-M4 (shallow presence checks; string sequence; mode 0; `[{}]` members) | §7.4/§7.5 closed-shape strict-type validation of every consumed record before any comparison: bindings are exactly four typed non-empty members; snapshot members are validated element by element before any set is built; connection entries and journal grants are typed; `requestSeq`/`expectedRequestSeq` are strict integers; stat records are typed and the scratch directory mode is exactly 0700; the new refusal is `CONTEXT_MALFORMED`; exceptions inside either boundary are refusals. Retained: the four exact probes (`M4-empty-identity-bindings`, `M4-malformed-request-correlation`, `M4-scratch-mode-zero`, `M4-snapshot-member-not-a-string`) plus partial-binding, traversal-member, bool-sequence, mode-0710 and unknown-stat-member negatives and the adjudicator's valid controls |
| SEC3-M5 + SEC4-REG-M5-OUTCOME (REVERTED outside the closed vocabulary; no REV cases; receipt text) | §7.5 recovery emits only the closed journal vocabulary (RCO COMPLETED/FAILED; ICO COMPLETED/FAILED/INDETERMINATE); a reversible effect is reverted by executing the recorded `inverseRef` and proven by the footprint (INVERSE-FIRST), never asserted; an undeterminable reversible footprint appends nothing (RETRY-LATER); after REV the request closes through the CLN residual string; unlawful record order quarantines; the receipt id derives from the outcome record's position (`receipt_id`). Retained: thirty recovery cases including ten with REV inputs, the `RCO REVERTED` schema rejection with its FAILED control, and the order-violation set |

## 1. Threat model boundary

File 03's laws are carried whole (v1 §1). **Assumed trusted computing base:** the operating-system
kernel and its distribution signing chain, the platform loader and libc, and first-party trusted code
running with the invoking user's ambient authority; the host itself runs unprivileged (§8.4 privilege
model). Adversaries in scope: tampered or substituted release artifacts; replayed stale catalogs and
revocation lists; a rolled-back trust store that is detected or declared; ambient library, loader or
tool substitution observable from the process; a manifest that grants itself authority; a component
that smuggles a verdict through free text or presents an authorization it was not issued; a metadata
document whose parsed identity differs between admitter and consumer. Out of scope: a compromised
kernel or distribution signing chain, local root, a hostile kernel reached by kexec, and a coherent
unmarked rollback of the whole install root (§5.5). Nothing below claims confinement of first-party
code, hostile-kernel detection, or filesystem-wide rollback detection.

## 2. Metadata canonicalization and signature profile

### 2.1 `opensip-metadata-canonical.1`, parse refusals, domain registry, wire grammars

Rules, undetermined-point decisions and parse refusals as v2 §2.1. **Closed domain-tag registry:**

| Tag | Document | Enveloped |
|---|---|---|
| `opensip.metadata.manifest.1` | component manifest | yes, TR-COMPONENT |
| `opensip.metadata.catalog.1` | release catalog | yes, TR-INDEX |
| `opensip.metadata.root.1` | trust root document | yes, ROOT |
| `opensip.metadata.revocation.1` | revocation list | yes, ROOT |
| `opensip.metadata.inventory.1` | signed-closure inventory (DR-126 carrier) | yes, TR-CORE |
| `opensip.metadata.payload.1` | air-gap payload manifest | yes, TR-BUNDLE |
| `opensip.metadata.registry.1` | local admission store | never |
| `opensip.metadata.registry-view.1` | scoped registry view consumed by a lock | never; digest-pinned in the lock as `registryViewDigest` |
| `opensip.metadata.lock.1` | component lock | never |
| `opensip.metadata.policy.1` | raw permission policy files: the global file and the project-private file (schema `permission-policy`) | never |
| `opensip.metadata.policy-effective.1` | the effective policy document, the merge of the two raw files (schema `permission-policy-effective`, §6.11) | never; its digest is the lock's `permissionPolicyDigest` and is on every GRANT record |
| `opensip.metadata.journal.1` | grant-journal record bodies | never |
| `opensip.metadata.envelope.2` | the signed subject of an envelope | is the signature message |
| `opensip.metadata.test.1` | vectors only | never |

**Numeric ranges.** Metadata counters (`rootVersion`, `previousRootVersion`, `snapshotVersion`,
`revocationVersion`, `grantGeneration`, epoch members) are signed-i64 `1 .. 9223372036854775807`. The
grant-journal `seq` alone is uint53 `1 .. 9007199254740991` because the control contract carries it in
`effectResult.decisionSeq / outcomeSeq`.

**Closed wire grammars (security-owned; the control schema stays a 1,024-byte courier and never
parses them):** `authorizationRef` `^ah:[0-9a-f]{32}$`; `operationRef` `^op-[0-9a-f]{32}$`; `resultRef`
`^rr:[0-9a-f]{32}:[0-9a-f]{64}:(0|[1-9][0-9]{0,7})$` (at most 108 bytes). A schema-valid string outside
its grammar is an `RF-6` host-authorization refusal (§7.4), never `RF-2`; the channel/refusal
precedence of the control contract is untouched.

### 2.2 `opensip-signature-envelope.2` — as v2 §2.2, with the admission step added

Step 0, before any of the seven verification steps: the root document in force is admitted by §3.1's
semantic rules; a root that fails admission yields `ROOT-NOT-ADMITTED` and no signature is consulted.

## 3. DR-101 OD-101-2: signing ceremony, notarization, launch verification

### 3.1 Key hierarchy and root semantic admission (SEC2-M4)

Thresholds, custody and rotation as v2 §3.1, minus the kernel attestation key (`kernelAttestationKeys`
is an empty list in the preview). A root document is **admitted** only when every rule below holds;
shape validity never admits a root:

1. `keys[]` has unique `keyId` and unique `publicKey`; every `keyId` equals `SHA-256(publicKey)`.
2. Every key reference resolves to a member of `keys[]`; no list repeats a key.
3. `rootKeys` has at least three members and `2 <= rootThreshold <= |rootKeys|`.
4. `recoveryAuthority` has at least five members, `3 <= threshold <= |keys|`, disjoint from `rootKeys`.
5. The role set is exactly `TR-CORE, TR-INDEX, TR-COMPONENT, TR-BUNDLE, TR-REPAIR`; every active role has
   `standing: active`, `threshold >= 2`, `|keys| >= threshold + 1` and at least one namespace; `TR-REPAIR`
   is the typed absence (no keys, threshold 0, no namespace, `standing: typed-absence-DR-110`).
6. Role key sets are pairwise disjoint and disjoint from root and recovery keys.
7. `1 <= rootVersion <= 2^63-1`; `previousRootVersion` is null exactly when `rootVersion` is 1 and
   otherwise `1 <= previousRootVersion < rootVersion`; `issuedAt < expiresAt`.

8. `kernelAttestationKeys` is exactly `[]` (the preview's typed absence; the schema pins `maxItems 0`
   and the semantic rule refuses `ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY`).
9. No key list repeats a key: `rootKeys`, `recoveryAuthority.keys` and every role list
   (`ROOT.DUPLICATE_KEY_IN_LIST`).

**One admission boundary (SEC3-M1, corrected in v5).** `admit_root_document(encoded bytes or parsed JSON value)` = parse → closed
shape (`root.schema.json`) → the semantic rules above, and returns an `AdmittedRoot` or the refusal
list; an exception anywhere inside is a refusal. `AdmittedRoot` is an immutable carrier, not a trust
anchor: it holds a canonical copy and the claimed digest, exposes only fresh copies, and refuses
attribute assignment. `verify_envelope` accepts only an `AdmittedRoot` and, before any verification
step, **re-runs the complete boundary on the copy it receives and re-derives the digest**
(`recheck_admitted_root`); a raw dictionary, a directly constructed carrier over an invalid document, a
carrier whose claimed digest differs, or any exception during the recheck is `ROOT-NOT-ADMITTED`. A
mutation of a returned copy never reaches the held state, and a directly constructed carrier over a
valid document with the correct digest verifies only because the recheck admits it.
Fourteen retained negatives (each refused by the boundary), including a non-empty
`kernelAttestationKeys` and repeated recovery keys; the turn-2 probe (TR-COMPONENT threshold 1, one
signature) returns `ROOT-NOT-ADMITTED`.

### 3.2 Entitlements and notarization — as v2 §3.2 (Gatekeeper claim withdrawn).

### 3.3 Verification at install and launch, by command class (WA-6)

Retained as `launch-verification-classes.json`. DR-G07's "at launch" claim is scoped to the operation
class; the G03 fixture's falsification condition is any read outside the first row.

| Command class | Verifies | Trust evaluation | Durable writes | Must not open |
|---|---|---|---|---|
| metadata-only (`--help`, `--version`) | nothing beyond the OS exec of the core; prints compile-time embedded release metadata | none | none | `trust.sqlite`, registry, lock, inventory members, grant journals, any helper process, any project path |
| doctor (both read-only modes) | reads trust, registry, lock, journals and the profile observations | report-only, non-persisting (§4.8) | none | any file for writing under the install root; any helper process |
| operation (`analyze`, `install`, `remove`, `update-index`, trust refresh) | open-then-verify of every executed or loaded closure member on its opened fd (the core itself and the component binaries about to run), not an eager hash of the whole inventory | decision evaluation with write-ahead `evalHighWater` (§4.2) | yes, under §5.6 | — |

The install-time verification of a payload (every member on its opened fd against the signed
inventory before publication) is unchanged from v2 §3.3.

## 4. DR-112 trust machine

As v2 §4, with `trustEpoch` member `indexSnapshotVersion` equal to the release catalog document's
`snapshotVersion`, and these two precisions.

### 4.2 Evaluation instant and exact boundaries

Every expiry, staleness or future-time predicate evaluates at `tEval = max(evalHighWater, wall clock,
lastAccepted)` where `lastAccepted` is the issue time of the last accepted trust document. A decision
evaluation writes `evalHighWater = tEval` durably first (write-ahead, §5.6) and then evaluates; a
report-only evaluation (§4.8) evaluates at the same instant without writing. The raw wall clock is
recorded separately in the audit and in doctor output, and a raw clock below `evalHighWater` is the
`CLOCK-REGRESSION` finding. Boundaries: a catalog or root is **expired iff `tEval >= expiresAt`**; a
revocation list is **stale iff `tEval > revocationFreshUntil`** (an age of exactly 90 days is fresh;
90 days plus one second is stale). §4.7's worked transitions stand under these boundaries.

### 4.8 Doctor evaluates report-only (WA-5)

Doctor never persists. It computes `tEval`, evaluates the predicates above against the recorded
counters, and labels the output `evaluationMode: report-only` with `rawWallClock`, `evaluationTime`,
`recordedEvalHighWater` and `lastAccepted`. Journal open in doctor runs the pure `reconcile_witness`
and reports the would-reconcile state (`OK | WOULD-REVERT | WOULD-ADVANCE | WOULD-QUARANTINE`); the
write happens at the next operation open under the lease. FC-RO and FC-MODE assert `writes: []` and the
mode label. Retained: `doctor-trust-report.example.json` (normal, clock regression, expired, the
90-day boundary on both sides, and a recorded high-water above the wall clock).

## 5. DR-124: trust state, index custody, grant journal, durability

### 5.1 SC-TRUST — as v2 §5.1 with `trustEpoch = {rootVersion, indexSnapshotVersion,
revocationVersion, permissionPolicyDigest}`; `permissionPolicyDigest` is the effective document's
digest (§6.11).

### 5.2, 5.3 — as v2.

### 5.4 Grant-journal carrier, lock handoff and witness (SEC2-M2, WA-1, WA-13)

Encoding, DDL, sequence rule, uint53 cap with the reserved terminal slot, hash chain: as v2 §5.4.
Replaced or added:

**Locator (host-internal only).** `gj:<projectKeyDigest>:<grantGeneration>:<seq>` with
`projectKeyDigest = SHA-256(projectKey UTF-8 bytes)` in lowercase hex; grammar
`^gj:[0-9a-f]{64}:[1-9][0-9]{0,18}:[1-9][0-9]{0,15}$`, 71 to 104 bytes. It appears in journal
records, audit and doctor output and in the host's handle map; it is never a control-plane body member
and never discloses `projectKey` bytes. The v2 base64url form (up to 1,409 bytes) is withdrawn.
Retained: `locator-bounds.json` (minimum, maximum, ten refused spellings). The witness names its carrier
by `projectKeyDigest` and `grantGeneration`.

**Fence and lease handoff (race-free).** Operation start: acquire the global lifecycle fence; attempt
the project's operation lease **non-blocking** (if held, release the fence and report the project busy;
never wait for a lease under the fence); read the carrier tail and witness; compare with the SC-TRUST
high-water for that carrier and quarantine on a lower tail or an equal sequence with a different body
hash; copy the observed tail into SC-TRUST; capture `trustEpoch`; publish the lifecycle lease row;
release the fence. Under the lease the writer never acquires or waits for the fence. Operation end:
release the lease; acquire the fence; re-acquire the lease non-blocking; if acquired, re-read the tail,
copy it into SC-TRUST and release both; if another writer holds the lease, skip the copy (that writer's
start recorded a tail at or above ours) and release the fence. Garbage collection: under the fence, a
**non-blocking census** of lease locks; any lease that cannot be proven released is treated as live and
its carrier skipped; GC never waits on a lease.

**Witness shape (SEC3-M3), validated before any comparison.** `{witnessSchema: 1, projectKeyDigest:
hex64, grantGeneration: 1..2^63-1, seq: integer (never a boolean) 0..2^53-1, state: PENDING | COMMITTED,
bodySha256: hex64 when seq >= 1 and null only at COMMITTED 0}`; the `bodySha256` **member must be
present** (an absent member is not a null); PENDING requires `seq >= 1`; no other member. The journal
tail passed in is validated as well. Any violation, including a string or list where an object is
expected, quarantines `witnessMalformed`; the boundary never raises (an exception inside it quarantines);
only a valid witness can authorize REVERT or ADVANCE.

**Witness reconciliation on open** (executable as `reconcile_witness`, twenty-four retained cases
including nine malformed-shape negatives, and a simulated writer crashed after each protocol step
reconciling to OK, REVERT, ADVANCE, OK):

| Journal tail vs witness | Action |
|---|---|
| empty carrier, no witness | INIT: witness created at COMMITTED 0 |
| COMMITTED n = tail n, same body hash (or n = 0) | OK |
| PENDING n+1 with tail n | REVERT: the append never became durable; witness → COMMITTED n |
| PENDING n = tail n, same hash | ADVANCE: commit landed before the witness update; witness → COMMITTED n |
| COMMITTED n > tail | QUARANTINE `uncertainTailLoss` |
| COMMITTED n = tail n, different hash | QUARANTINE `uncertainTailLoss` (equal sequence, unequal bytes) |
| PENDING n = tail n, different hash | QUARANTINE |
| tail > witness seq (either state) | QUARANTINE: protocol violation |
| PENDING not adjacent to the tail | QUARANTINE |
| witness absent with a non-empty journal | QUARANTINE `witnesslessRestore` |
| witness fails the closed shape (bool sequence, missing hash, PENDING 0, unknown member, string) | QUARANTINE `witnessMalformed` |
| witness names another carrier (digest or generation) | QUARANTINE |

**Grant-generation closure (WA-13).** `grantGeneration` advances only on whole-generation REV and on
the uint53 rollover (TERMINAL with cause `grantGenerationClosure`). Project purge and retirement are
user operations deferred with DR-113 by the lead's foundation decisions; the v2 "project purge" cause is
unreachable in the preview and is retained as a typed reserved cause for that slice, whose ordering
across registry entries, selection, journal namespace and tombstone is that slice's design. Runtime
rollback, quarantine and the rollover stay active.

**Detection bound (honest).** The witness detects torn restores, lost tails and hash substitution within
a carrier; the SC-TRUST high-water detects a project-namespace rollback below the last **observed**
operation boundary. A rollback to a state above the last observed floor, performed while no operation
was running, is not detected until an operation observes a tail lower than a later floor.

### 5.5 Backup, restore and rollback (SEC2-M3)

Trust floors are excluded from lifecycle backups and generation rollback; any declared restore marks
every role `ST-UNBOOTSTRAPPED` with reason `RESTORED` and keeps the restored counters and
`evalHighWater` as floors; only an ordinary payload at or above the floors re-establishes trust.
Detected: declared restores, torn or partial journal restores (§5.4), a project rollback below an
observed floor, a trust store restored below any document still on disk. Not detected, stated: a
coherent rollback of the entire install root with the marker suppressed, which may reuse the authority
it validly held at its own time (verified components keep running; already-catalogued releases stay
admissible) until the catalog or revocation floors age out or a consented refresh compares counters
with the origin. No origin check is performed before offline operations. Rollback therefore yields
denial where it is detected or declared, and at most formerly valid authority, aging into denial,
where it is not.

### 5.6 Durability primitives and I/O failure classes (WA-9)

Retained as `durability-io-failures.json`. **Primitives:** macOS `fcntl(F_FULLFSYNC)` on files and on
the directory fd (falling back to `fsync(2)` only where the directory refuses it), SQLite
`synchronous=FULL; fullfsync=ON; checkpoint_fullfsync=ON`; Linux `fsync(2)` on file and directory,
SQLite `synchronous=FULL`. These costs are paid only at operation boundaries and decisions (§3.3),
never by metadata-only commands or doctor. **Boundaries:** witness write, `evalHighWater` write,
journal append, quarantine marker, SC-TRUST high-water copy, lifecycle publication, selection commit.
**Error classes and dispositions** (every one a typed refusal, D9 `operational-failed` / 4 /
`HOST.IO_FAILURE`):

- Before visibility (`ENOSPC`, `EDQUOT`, `EIO`, `EROFS`, short write, failed rename): no partial state;
  the previous durable state is retained by the temp-then-rename pattern; `ENOSPC`/`EDQUOT` retryable.
- After visibility (`FSYNC_FAILED`, `COMMIT_FAILED`): durability is **UNDETERMINED**, because a
  visible rename or SQLite commit may precede the failed sync. The writer refuses every further effect
  of the operation, reopens the carrier, reconciles the exact state (witness reconciliation for the
  witness and journal boundaries; re-read and re-sync for the others) and only then decides. It never
  assumes either the old or the new state. Three post-visibility cases are retained with their reopen
  rule.

## 6. DR-105 and DR-114

§6.1–§6.8 as v2, with rides named by scope-rides identifier: BLK-1 (CA-2) → SD-2; CA-3 KEYCHAIN → SD-3;
DR-124 SC-EVIDENCE/SC-ANALYSIS → SD-4; DR-122 `committed-run-preserved` → SD-5; DR-127 AL-3 → SD-1.
Each is a ride under the five-condition property of `scope-rides-completion.v2.md`, adopted in the
same integrated act; nothing here creates a ride by prose. The not-admitted probe subtypes and CA-4
paths are admission decisions (§6.4, §6.5), not rides.

### 6.9 Joins to the accepted D9/exit vocabulary (WA-10; inventory items ID-DEP-1 and ID-DEP-P1)

Source `d9-exit-contract.v1.14.json` projected through `operability.v10` `projectionParity` (the exit
surface carries termination only). No class, code or exit is minted; retained as `d9-joins.example.json`
and checked against the closed vocabulary.

| OC | D9 class | exit | codes | reduction |
|---|---|---|---|---|
| OC-1 allChecksSatisfied | success | 0 | — | none |
| OC-2 environmentDefectFound | success | 0 | — | doctor is not an analysis, so `policy-failed` is unavailable; the verdict is `report.outcome` on the machine surface; CI gates on it |
| OC-3 reportIncomplete | indeterminate | 3 | `QUERY.COMPLETENESS_UNMET` | nearest closed reason to unreached checks |
| OC-4 invocationRefused | request-rejected | 2 | `REQUEST.UNKNOWN_OPTION`, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, `CONFIG.INVALID`, `REQUEST.PRECONDITION_FAILED` | one per sub-cause |
| OC-5 doctorFault | operational-failed | 4 | `OUTPUT.SERIALIZATION_FAILED`, `HOST.IO_FAILURE`, `SYSTEM.OUTCOME.ILLEGAL_STATE` | sink, consent-record write, report construction |

Permission: at admission PR-1, PR-3 and PR-6 reach D9 as `request-rejected` / 2 /
`EXTENSION.ADMISSION_REJECTED`; at request time every PR family is an `RF-6` refusal on the wire and the
Run's termination follows only the component's subsequent protocol-visible response. State-class
matrix: five total, three active in the preview (SC-CACHE, SC-OPS, SC-TRUST), the other two retained by
SD-4. ID-DEP-3 and ID-DEP-8 are answered by `compatibility-matrix.completed.v5.json` and distribution
§8.1 and should close in the inventory.

### 6.11 Effective permission policy (lead's final policy join)

The foundation keeps two raw policy files under the per-user operational root: the global file and the
project-private file (both schema `permission-policy`, domain `opensip.metadata.policy.1`); the
repository can grant nothing. The lock and every GRANT record pin one `permissionPolicyDigest`: the
domain digest, under its own tag `opensip.metadata.policy-effective.1`, of the **effective document**
(its own closed schema `permission-policy-effective`, so a consumer can recompute the merge and compare
the exact body and both source pins) computed by the pure `merge_policy(global, project)`: a deny in
either layer denies; a grant is effective only when the global layer grants the same `(stableId,
token)` and the project layer grants it with a scope inside the global scope (path prefixes within,
list members subset, state class equal); the project layer can only narrow; an unknown token or a
widening project scope refuses the whole policy; consents are the intersection; ordering is stable by
`(stableId, token)`. The effective document embeds both raw-file digests, so the pin identifies both
files and the merge, never "whichever was last", and never equals a raw file's digest.

**Source admission (SEC3-M2, SEC-POLICY-N1).** Before any merge, every `pathPrefixes` member of every
grant in either raw file must be a normalized member path (relative, NFC, `/`-separated, no empty, `.`
or `..` segment, no backslash or NUL, at most 1,024 bytes) or the whole policy refuses
`POLICY.PATH_PREFIX_NOT_NORMALIZED`; narrowing then compares whole path segments, so `src/../private`
and `src/../../outside` never earn a narrowing proof and `srcx` is not under `src`. A raw file that
repeats a `(stableId, token)` pair among its grants refuses `POLICY.DUPLICATE_GRANT_PAIR`, among its
denies `POLICY.DUPLICATE_DENY_PAIR`, whether the repeated scopes agree or conflict; a grant and a deny
of the same pair is lawful and the deny wins. Retained: three traversal negatives, two controls, four
duplicate cases.

**Absence (the foundation author's rule, deny by absence).** A selected-project operation whose
private project policy file is missing evaluates `merge(global, EMPTY_PROJECT_POLICY)` (an explicit
empty project layer: no grants, no denies, no consents), never `merge(global, None)`; its effective
grants are therefore empty and its `sources.project` is the empty layer's digest.
`merge(global, None)` is exclusively the global/core operation without a selected project namespace
(`sources.project` null). Doctor reports the absence and never creates the project namespace to
represent an empty policy. Retained: `permission-policy.effective.example.json` (global, project,
effective, digest, the global-only branch, the deny-by-absence branch, and three negatives), reproduced
and schema-validated by the checker.

## 7. Control-plane effect bodies

§7.1–§7.3 as v2 (RF-5 locally unreachable; CC-8 opaque detail), with the v1 §7 locator-on-the-wire
sentence withdrawn: the request carries a handle, and the journal locator never leaves the host.

### 7.4 Authorization handles and bootstrap consumption (WA-1; bootstrap v2 MUST)

**Minting.** At spawn the host mints **one handle per GRANT record** the spawn may exercise:
`ah:<32 lowercase hex>` from 16 CSPRNG bytes, held in a connection-local map
`{handle → {operationRef, effectClass, brokerLocator, underlyingLocator, grantGeneration, seq, binding,
target}}`. Several handles share the spawn's single `operationRef` (`op-<32 hex>`, one `select` per
child). The map is keyed by the connection, so a handle presented on any other connection is unknown
(PR-4: the caller is the spawn the map was minted for). Handles carry no authority and are never
persisted as authority.

**Delivery.** The handles reach the component only through the protocol author's bootstrap descriptor
(`OPENSIP_BROKER_CONTEXT`, `bootstrapVersion` 1, at most four handles, base64url of strict closed JSON,
encoded ≤ 16,384 and decoded ≤ 12,288 bytes, depth ≤ 8; consumed once and unset by the SDK; a missing or
malformed descriptor is a startup error on the existing provider-operability path). Each entry carries
`{effectClass, operationRef, authorizationRef}`, the frozen bootstrap schema's shape
(`broker-bootstrap.schema.v1.json`, pinned in the fixture; the retained descriptor example validates
against it). The shipped TypeScript worker receives the empty descriptor `{bootstrapVersion: 1,
handles: []}`, which stays as frozen. **One bootstrap successor is required by §7.5 and is recorded,
not implied:** when `handles` is non-empty the descriptor carries the single new top-level member
`resultScratchRoot` (absolute path, ≤ 4,096 UTF-8 bytes, no empty, `.` or `..` segment, under the
per-user operational root) and may carry `commitClass` on every entry as SDK-facing information (the
host's connection map stays authoritative and the SDK never sends it); entry grammar, bounds and error
path are unchanged. The bootstrap author authors and numbers that successor after this freeze; the
frozen bootstrap bytes are not edited. The entry grammar and the courier are this unit's;
the envelope and its error path are the bootstrap unit's. The public SDK surface the broker author is
preparing (`readProject(handle)`, `writeHostState(handle, bytes)`, with `requestEffect` internal and
refs and scratch private) consumes exactly §7.4 and §7.5.

**Verification at every `effectRequest`** (after `RF-2`..`RF-5`; the enforcing boundary is
`verify_effect_request(body, ctx)`, thirty-one retained cases), refusing with `RF-6` and the closed
reasons, in this order: **context absent** (SEC3-M4: the connection map, the current binding, the
journal state and the sealed snapshot manifest must all be present; absence never admits); **context
malformed** (v5: the current binding is exactly `{installGenerationId, manifestDigest, platform,
stableId}` with strict non-empty types, so an empty or partial binding never compares equal to anything;
every snapshot member is a normalized member-path string, validated element by element before any set is
built, with no duplicates; every connection-map entry and journal grant record has its closed shape and
strict types; an exception anywhere inside the boundary is `CONTEXT_MALFORMED`); handle grammar and
operationRef grammar (full match; a trailing byte refuses); unknown handle; operation
mismatch; effect-class mismatch; binding drift (the connection's `{installGenerationId,
manifestDigest, platform, stableId}` differs from the map's); locator integrity; then for **both** the
broker grant (`PT-HOST-EFFECT-BROKERED`) and the underlying token grant (`HE-1` →
`PT-FS-WRITE-HOST-STATE`, `HE-2` → `PT-FS-READ-PROJECT`): grant not current (revoked, or its generation
closed), token mismatch, grant binding mismatch; then for **both** grants the scope must be non-empty
(`GRANT_SCOPE_EMPTY`) and contain the exact prebound target: for HE-2 the target path normalized, the
grant scope naming the sealed snapshot and the target the same one
(`SNAPSHOT_BINDING_MISSING_OR_MISMATCH`), exact membership in that snapshot's manifest
(`TARGET_NOT_SEALED_MEMBER`), then whole-segment prefix containment (`TARGET_OUTSIDE_SCOPE`); for HE-1
the state class equal and `0 < byteCap <= 16 MiB`. `PT-HOST-EFFECT-BROKERED` alone never admits an
effect, and an empty broker scope admits nothing. A 1,025-byte reference is `RF-2` by the control
schema and never reaches this verifier. `_target_within_scope` is a named pure helper, not the boundary,
and is never scored as admission. Only after all of this does the host append RA and proceed as §7.5.

### 7.5 Result courier and the two effect classes

Neither effect has a preview consumer (the host owns projections; the TypeScript worker reads the
sealed VFS directly); both are demonstrated byte paths with synthetic fixtures, not product features.

- **Target order (HE-2).** The prebound target `{snapshotDigest, memberPath}` is admitted in this
  order, each step refusing before the next: the member path is a normalized snapshot member path
  (relative, NFC, `/`-separated, no empty, `.` or `..` segment, no backslash, ≤ 1,024 bytes); the
  target names the grant's sealed snapshot; the path is an exact member of that snapshot's manifest;
  and only then the whole-segment prefix relation to the granted prefixes. `src/../private` never
  reaches the prefix check. HE-1's target `{stateClass, byteCap}` must equal the grant's state class
  with `0 < byteCap ≤ 16 MiB`.
- **HE-2 PROJECT-READ-RETURNED.** The host copies the member's bytes from the sealed snapshot store
  into `<resultScratchRoot>/<resultId>.bin` (written via `openat` on the held directory fd with
  `O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0400, `fsync`, rename, directory `fsync`) and **only then** sends
  `effectResult.resultRef = rr:<resultId>:<sha256>:<length>` (publish before result). Because the
  bytes are a member of the snapshot the Run already sealed, **no additional semantic input enters the
  Run**; delivery.v2's source-only sealed VFS is preserved. A handle may be exercised more than once;
  each exercise is a new result.
- **HE-1 HOST-STAGED-STATE-WRITE (ordered algorithm, SEC3-M5).** The SDK writes
  `<resultScratchRoot>/stage/<handle hex>.bin` through the held directory fd with
  `O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`, `fsync`s, closes, records its own digest and sends the request.
  The host then, in this order and never otherwise: (1) verifies the request (§7.4), opens the stage file
  through its own held fd with `O_RDONLY|O_NOFOLLOW|O_CLOEXEC`, admits it by `fstat`
  (`stage_file_admission`: regular, `nlink` 1, host uid, size ≤ `byteCap`; seven retained cases), reads
  exactly that size **once** into a buffer allocated at that size and digests it; (2) appends **RA**
  durably; (3) appends the intent record durably, **RCI** for `REVERSIBLE` or **ICI** for
  `IRREVERSIBLE`, carrying the request reference (and, for RCI, the `inverseRef`); (4) commits **from the
  buffer** by temp-then-rename into the staged host-state class; (5) appends **RCO** or **ICO** durably
  with the actual outcome: RCO permits only `COMPLETED | FAILED`; ICO additionally permits
  `INDETERMINATE`; (6) unlinks the stage file (the handle is single-use for HE-1); (7) sends `effectResult` with
  the receipt whose `rid` derives from that outcome record's position. No effect precedes its durable
  authorization and intent. **Recovery** (`he1_recover`, thirty retained cases, ten with REV inputs; v5 corrected): the
  records for one request must be a lawful prefix of RA → intent → outcome, with REV allowed only after
  RA and nothing but CLN after REV; a duplicate, a wrong-class intent or outcome, an intent without RA,
  an outcome without its intent, or REV before RA **quarantines** the carrier under the existing reason
  `uncertainTailLoss` and appends nothing. RA without intent first appends REV with reason `process-death` (REVOKE-FIRST),
  then re-runs the existing post-REV cleanup to append CLN `not-begun` and report
  `FAILED`. It never appends an outcome lacking its intent. REV applies to the dead
  operation and its in-flight requests, not an invented request-local revocation.
  Reversible intent without outcome: the recorded `inverseRef` is executed first when the footprint is
  present (INVERSE-FIRST) and recovery re-runs; an absent footprint appends `RCO FAILED`; an
  undeterminable footprint appends **nothing** and reports `HOST.IO_FAILURE` (RETRY-LATER), so a revert
  is proven by the footprint, never by the missing record. Irreversible intent without outcome is decided
  by the durable footprint: present with the recorded digest → `ICO COMPLETED`, absent → `ICO FAILED`,
  undeterminable → `ICO INDETERMINATE`. After REV the in-flight request closes through the CLN residual
  string `<requestRef>:<not-begun | reverted | completed-irreversible | indeterminate>`, never through a
  post-REV RCO/ICO. **Only the closed journal vocabulary is ever emitted** (RCO `COMPLETED | FAILED`,
  ICO `COMPLETED | FAILED | INDETERMINATE`); `REVERTED` is not an outcome and the schema keeps rejecting
  it. A recorded outcome is never re-derived. The receipt's 32-hex `rid` derives from the outcome
  record's position (`receipt_id` over the carrier digest, grant generation and the RCO or ICO sequence),
  so the receipt is tied to that record without any new journal member. **The HE-1 `rr:` is a receipt only:** it authenticates the
  committed input bytes (digest and length of what the host committed from its buffer; `rid` is the
  32-hex id derived from the RCO or ICO record position by `receipt_id`) and names no file; the host publishes no receipt
  file and the SDK's `writeHostState` never opens one, returning the receipt after comparing its digest
  with the bytes it staged (`RESULT.RECEIPT_MISMATCH`, SDK-local). A stage file mutated after the read
  changes nothing committed. A missing or inadmissible stage file is an effect outcome `FAILED` with
  opaque detail, not an authorization refusal.
- **Scratch root and lifetime.** Host-created per spawn by `mkdirat` under the held operational-root
  fd at `projects/<namespaceId>/spawns/<spawnId>/` (the foundation's layout), mode 0700, a fresh name
  per spawn, held open by the host for the spawn's lifetime, named to the SDK by the bootstrap successor
  member; the SDK opens it once at startup with `O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`, checks owner and
  mode 0700, and uses that held fd for every later `openat`, never re-resolving the path. Files live
  until spawn end; the host removes the whole root after the child has exited and courier activity has
  stopped, while holding the operation lease; the SDK never deletes. It is never part of the sealed VFS
  and never a semantic input.
- **Caps (the lead's D-006-form decision).** 16 MiB per HE-2 result and **64 MiB of retained
  host-published HE-2 results per spawn**, charged before publication; a result that would exceed the
  aggregate is `FAILED` without publication. HE-1 staging is bounded **separately**: at most four
  single-use handles per spawn, each stage file at most 16 MiB and never above its prebound `byteCap`.
  A spawn's scratch root therefore holds at most 128 MiB in the conservative mixed budget (an actual
  four-handle mix is never larger). No combined 64 MiB claim is made, because that would require a
  distributed reservation between the SDK writer and the host publisher. Rationale in D-006 form:
  these are transport ceilings for an ephemeral SC-OPS directory owned by Product and host, not
  analysis budgets; equality passes and one byte over refuses before allocation; a legitimate component
  needing more is the falsification signal for a reviewed cap successor, never silent truncation.
- **SDK resolution** (`resolve_result(ref, reader, ctx)`, nineteen retained cases; SEC3-M4): `ctx` is
  one required record `{effectResult, expectedRequestSeq, scratchDirStat, selfUid, fileStat,
  spawnBytesSoFar}` and any absent member refuses `RESULT.CONTEXT_ABSENT` first; then in order: the
  carrying `effectResult` is `COMPLETED`, its `requestSeq` is the SDK's own request and its `resultRef`
  is the one being resolved; the held scratch directory is a directory owned by this uid at mode 0700;
  ref grammar as a full match and the per-result cap; the aggregate cap; the file opened by
  `openat(held, "<rid>.bin", O_RDONLY|O_NOFOLLOW|O_CLOEXEC)` is regular, `nlink` 1, owned by this uid,
  with size equal to the ref length (the buffer is allocated only now, at that size); then length and
  digest equality before any byte is returned. Every failure is an SDK-local typed error
  (`RESULT.CONTEXT_ABSENT | CONTEXT_MALFORMED | EFFECT_NOT_COMPLETED | REQUEST_SEQ_MISMATCH |
  REF_NOT_FROM_RESULT | SCRATCH_NOT_OWNED | REF_GRAMMAR | OVER_CAP | SPAWN_CAP_EXCEEDED |
  FILE_NOT_ADMITTED | ABSENT | INTEGRITY`) and nothing is sent on the wire. **v5 shape rule:** before any
  comparison the effect result is a closed record with `effectOutcome` in its enum and `requestSeq` a
  strict integer in `1..2^53-1` (a string or boolean is `CONTEXT_MALFORMED`), `expectedRequestSeq` and
  `spawnBytesSoFar` are strict integers, the stat records are typed with no unknown member, and the
  scratch directory mode is **exactly 0700** (mode 0, 0710 or 0750 refuse); an exception inside the
  boundary is `CONTEXT_MALFORMED`. No new provider frame, no
  new control member and no new file descriptor is introduced; the one descriptor member the courier
  needs is the recorded bootstrap successor above.

## 8. DR-126 profiles

### 8.1, 8.2 — as v2 (value-source legend; static-PIE musl core; libSystem-only macOS core).

### 8.3 macOS (WA-3)

Measured facts as v2 §8.3 (no SecCode guest for the kernel; kernel bytes unsigned per file; `kern.uuid`
equals the kernel's `LC_UUID`). v49 scheme `macos-sealed-boot` as v2, with the acquisition split
decided:

- **Launch (unprivileged, no helper, no Security.framework):** `sysctlbyname(kern.uuid)` and
  `kern.osversion` equal to the profile; `csr_check(CSR_ALLOW_UNAUTHENTICATED_ROOT)` and
  `csr_check(CSR_ALLOW_UNRESTRICTED_FS)` from libsystem_kernel (the calls `csrutil` makes) proving
  authenticated root and SIP; the loader cdhash computed **in-core** by parsing `LC_CODE_SIGNATURE` of
  `/usr/lib/dyld` and hashing its CodeDirectory with CommonCrypto (libSystem), the sealed volume
  guaranteeing file bytes equal loaded bytes; `fstatfs` of the install root equal to `apfs`.
- **Qualification only:** the Security.framework helper (`SecCodeCopyGuestWithAttributes`,
  `SecCodeCheckValidity`, `SecCodeCopySigningInformation`) confirming the in-core cdhash; it is a
  separate signed process with its own closure, **not a launch-closure member and not counted in G02**;
  the boot policy (`bputil -d`, `system_profiler SPiBridgeDataType`), recorded as
  `virtualized-not-observable` on hosted images and never refusing at launch; the boot kernel collection
  digest. The framework class therefore stays absent for the core with its inapplicability proof.
- **Honest limitation:** at launch an unsealed root is refused; Full versus Reduced Security is not
  distinguished at launch.

### 8.4 Linux — v49 scheme `publisher-signed-boot` (SEC2-M1, WA-2)

Withdrawn from v2: the OpenSIP-built kexec-absent kernel, `builderAttestation`, KB-1, the required
measured-boot transcript, the AK certificate member, and v48's setns mount helper. **Privilege model:**
the host runs unprivileged; no setuid helper, daemon or root requirement; every launch-time refusal
predicate uses only unprivileged observations; privileged observations are qualification-only.

- **Identity (SEC3-M6):** `{publisher: ubuntu, packageDbScheme: apt-secure, kernelFlavor, kernelSeries,
  kernelPackageNamePattern, archiveSigningKeyDigest, uefiSignerDigest, bootAttestation,
  lockdownExpected: integrity}`. The publisher members are fixed; **`kernelFlavor` and `kernelSeries`
  are RELEASE-MEASURED on the D-102 class image**, never assumed: the `ubuntu-24.04` hosted image
  20260823.283.1 boots `6.17.0-1022-azure` (primary source: the runner-images Ubuntu 24.04 readme), a
  Canonical-signed `linux-azure` archive kernel, so its measured series is `6.17.0-azure` with flavor
  `azure`; a stock GA install would measure `6.8.0-generic`. The series is `<major.minor.patch>-<flavor>`;
  the ABI number, the exact `kernelPackageVersion` and `uname -r` are drift metadata, retained on every
  run and never allow/refuse. The release templates carry placeholders for flavor, series and package
  pattern; two ILLUSTRATIVE filled examples (`profile.example.linux-x86_64.azure-6.17.json`,
  `profile.example.linux-x86_64.generic-6.8.json`) validate and admit nothing.
- **`bootAttestation`** is measured once on the D-102 image and recorded in the release profile:
  `secure-boot-lockdown` when the image boots UEFI Secure Boot under the Canonical chain (efivars
  `SecureBoot` = 1 and `/sys/kernel/security/lockdown` not `none`); otherwise `package-db-declared`,
  in which case the OS ABI member is a declared baseline that doctor reports as **declared, never
  attested**. Both forms detect drift and unsupported kernels; neither detects a hostile kernel (§1).
- **Launch observations (all unprivileged; retained in the templates' `acquisition.launch`):** efivars
  `SecureBoot-8be4df61-…` data byte; `/sys/kernel/security/lockdown`; `/proc/sys/kernel/osrelease` and
  `/proc/version` in the declared series; `/var/lib/dpkg/status` showing `linux-image-<osrelease>`
  installed with the Ubuntu maintainer; SHA-256 of `/etc/apt/trusted.gpg.d/ubuntu-keyring-2018-archive.gpg`;
  the Canonical UEFI CA present in the efivars `db`; the install-root filesystem observed by reading
  `/proc/self/ns/mnt`, then `/proc/self/mountinfo` in the process's **own** namespace, then
  `/proc/self/ns/mnt` again and requiring equality, plus `fstatfs(install-root fd).f_type ==
  EXT4_SUPER_MAGIC`. That read supersedes v48 `filesystemMeasurementTarget.linux`'s setns helper, which
  needs `CAP_SYS_ADMIN` and returns `EPERM` for every unprivileged host.
- **Qualification only:** `/boot/vmlinuz-<osrelease>` (mode 0600) Authenticode chain and apt-secure
  InRelease verification; the TPM event log (`binary_bios_measurements`, root-readable), hardening
  evidence only.
- **Refuses (NT-TCB-BOOT; executable as `linux_os_abi_predicate`, twelve retained cases):** under
  `secure-boot-lockdown`, Secure Boot off, lockdown `none`, or the UEFI signer absent; under either
  form, `/proc/sys/kernel/osrelease` whose line or flavor differs from the measured series (the
  wrong-series negative: `6.8.0-45-generic` on the azure profile; `6.14.0-1010-azure` on the `6.17.0`
  line), a `/proc/version` without the Ubuntu build string, the package absent or not installed by the
  Ubuntu maintainer, an archive-key digest mismatch, an `/etc/os-release` selector mismatch, a namespace
  change during the read, or an install root not on ext4. A release template still carrying a
  placeholder is `undetermined` and admits nothing. An ABI bump within the measured series
  (`6.17.0-1030-azure`) is drift only.

### 8.5 Carrier and `verifiedInstallRoot` — as v2 §8.5.

### 8.6 Product consequence

A host on a Canonical-signed Ubuntu 24.04 kernel of the flavor and series measured for its class
selects a qualified profile without privilege, and distribution kernel updates within the series do not
break it. Hosts
with self-built kernels or kernels outside the series select no qualified profile and the core refuses,
never degrading. Linux remains in D-002's slice 1; no custom kernel and no root privilege is required.

### 8.7 Qualification runner table (WA-7; the quality unit's G13 binding)

Retained as `qualification-runners.json`, pinned to `coordinator-decisions.D-102.turn2.draft.md`. Rule:
one named hosted class per platform; every release profile is measured on its class; a profile named
for a build the class does not run is never qualified; G13 thresholds apply on every class with a
separate per-class baseline.

| D-102 class | Platform | Release profile | Development template | Launch attestation |
|---|---|---|---|---|
| `macos-15` (3-core M1, 7 GB, VM) | macos-arm64 | `P-MACOS-ARM64-<image build>-APFS` (RELEASE-MEASURED) | `profile.P-MACOS-ARM64-25G83-APFS.json` | §8.3 launch list; boot policy `virtualized-not-observable` |
| `macos-15-intel` (4 CPU, 14 GB, VM) | macos-x86_64 | `P-MACOS-X86_64-<image build>-APFS` | `profile.P-MACOS-X86_64-25G83-APFS.json` | same |
| `ubuntu-24.04` (4 CPU, 16 GB) | linux-x86_64 | `P-LINUX-X86_64-UBUNTU2404-EXT4` | `profile.P-LINUX-X86_64-UBUNTU2404-EXT4.json` | §8.4 launch list; `kernelFlavor`/`kernelSeries` (image 20260823.283.1 boots `6.17.0-1022-azure`) and `bootAttestation` RELEASE-MEASURED |
| `ubuntu-24.04-arm` (4 CPU, 16 GB) | linux-arm64 | `P-LINUX-ARM64-UBUNTU2404-EXT4` | `profile.P-LINUX-ARM64-UBUNTU2404-EXT4.json` | same |

G13 (the quality owner's decision): the absolute thresholds (10 s / 5 s / 1 GiB) and the per-class 10 %
regression rule apply on **all four** named classes; different hardware means separate per-class
baselines and no cross-class comparison, never a missing threshold; the floating four-vCPU/eight-GiB
worker requirement is replaced by the named class plus the actual CPU/RAM observation validated against
the class capacity. G03/G04 run on all four classes, measuring the metadata-only launch class of §3.3.
The four templates carry `measurementStanding: DEVELOPMENT-MEASUREMENT` and name their class; the
core-gate reference unit's scorers bind to this table.

### 8.8 Observed-event admission and the G07/G22 crosswalk (legacy-corpus audit)

Template validity does not prove hostile-event admission, so admission is executable:
`admit_observed_events(profile, observed)` over a retained observation `{trace, environment, osAbi}`
returns the closed refusals `NT-TCB-IDENTITY` (a declared member's identity differs, or a declared
external member never loaded), `NT-TCB-UNDECLARED` (an image of a class the profile neither declares
nor proves inapplicable, including a shell), `NT-TCB-ALT-LOADER` (origin outside
`allowedLoaderOrSearchOrder`), `NT-TCB-ENV-INFLUENCE` (a FORBIDDEN variable present),
`NT-TCB-TRACE-MISSING` (absent or partial trace: no profile match is ever asserted without a complete
observation), `NT-TCB-BOOT` (§8.3/§8.4 predicate failed or undetermined) and
`NT-TCB-PROFILE-UNQUALIFIED` (a compared member is still a release-measured placeholder: a development
template admits nothing). Thirty-eight retained cases over the four templates
(`g22-observed-events.json`) cover the four legacy `G22.<platform>.hostile-loader-system-library-tool`
states and map the seven `G07.loader.*` states to these refusals or to open-then-verify. The five
`G07.toctou.*` states are crosswalked to the rules that close them: extraction into a fresh directory
with verification on opened fds and rename into the generation slot; `openat` chains with `O_NOFOLLOW`
from a pinned root fd; verify-to-spawn, which differs by platform: on Linux the verified fd itself is
executed (`fexecve`) with no path re-resolution; on macOS `execve` of `/dev/fd/N` fails with `EACCES`
(measured by the lead, evidence retained separately) and no `fexecve` is exposed, so the guarantee is
scoped rather than an fd exec: the generation directory is immutable and the host mutates nothing under
the held generation lease, the exec path is canonical and absolute inside the per-user 0700 root,
`fstat` of the verified fd equals `stat` of the path (device and inode) immediately before
`posix_spawn`, and after spawn the child's text-image vnode (libproc `PROC_PIDREGIONPATHINFO`) must
equal the verified device and inode before the hello or the child is killed; the residual window can
be raced only by same-UID code, which is inside the explicitly trusted first-party boundary of §1;
immutable generations removed only by the fence-held census; and pinned root fd with
device/inode/birth comparison after every step (the lead's project-root identity rule). `G07.archive.*` and `G07.path.*`
are archive and path admission states owned by the distribution and lifecycle units. Genuine OS
execution, loader traces and build identities on the runner classes are qualification.

## 9. Evidence and checker report

`check-security-unit.v6.py --report security-unit.v6.report.json` (751 checks) reproduces every vector,
validates every example against its schema and cross-validates through `jsonschema` 4.25.1, runs the
envelope positive and five negatives, manifest admission, the root admission boundary with fourteen
negatives, the seven carrier boundary cases (immutability, recheck, direct construction), the
raw-dictionary refusal and the weak-threshold probe, twenty-four witness cases plus simulated crash
points and the never-raises set, the journal chain, binding,
digest-form locator with bounds and ten refused spellings, and the SQLite guards on a fresh database,
the thirty-seven broker-handle cases (including absent and malformed context, empty and partial
bindings, non-string and traversal snapshot members, malformed grant and entry records, empty and
narrowed broker scopes, missing snapshot binding, traversal, dot-segment, sealed-membership and
trailing-newline targets), the twenty-five result-courier cases with required and strictly typed context,
the seven stage-admission cases, the HE-1 order and thirty recovery cases with the journal vocabulary
and order-violation checks, the stated caps, the descriptor's validation against
the pinned frozen bootstrap schema and the recorded successor member, the durability matrix with its
post-visibility rule, the doctor report-only evaluations and both boundary edges, the launch-class
table, the runner table against the D-102 pin, the effective-policy reproduction under its own schema
and domain tag with digest sensitivity to either file, the deny-by-absence branch, the traversal and
duplicate-pair negatives with their controls, the twelve Linux OS-ABI predicate cases and the two
illustrative Linux examples, the thirty-eight
observed-event cases and the G07 crosswalk completeness, the D9 join vocabulary, and the four profile
templates (asserting no kexec-absent, KB-1
or builder-attestation residue, every launch observation unprivileged and outside the launch closure,
no privileged or slow interface at launch, and a development-measurement standing on a D-102 class).
Environment and the Unicode-table disclosure as v2.

## 10. Leftover obligation mapping — as v2 §10, with rides cited as SD-1..SD-5; the doctor and
permission D9 joins under DR-114 ID-DEP-1 and DR-105 ID-DEP-P1; the handle and courier design under
DR-105 (PT-HOST-EFFECT-BROKERED request semantics) and DR-125 (SDK `requestEffect`, to be authored by
the SDK unit over §7.4/§7.5); the effective policy under DR-124 `permissionPolicyDigest`; the runner
table under DR-126 and DR-118.

## 11. External references — as v2 §11, plus `apt-secure(8)`, the Canonical UEFI CA, the Linux
kernel lockdown LSM documentation, `fcntl(2)` `F_FULLFSYNC` and SQLite `PRAGMA fullfsync` documentation,
and `csr_check` as exported by libsystem_kernel (an SPI; its use is a RELEASE-MEASURED interface choice).

## 12. What this contract does not do

As v2 §12 and as the turn-3 and turn-4 texts; additionally it does not build, sign or require a custom kernel or root privilege; does not
adopt the v49 successor, the scope-rides amendment, the bootstrap unit or the foundation unit (it
specifies the first and consumes the others); does not claim detection of a coherent unmarked rollback,
of a hostile kernel, or of Full versus Reduced Security at launch; does not claim any runner class has
been measured; and does not make HE-1 or HE-2 a preview product feature.

## 10. Lead correction boundary requirements and retained challenges

The v6 boundaries `admit_root_document`, `verify_envelope`, `reconcile_witness`,
`verify_effect_request`, `stage_file_admission`, `resolve_result` and `he1_recover`
validate all consumed record shapes and strict scalar types before comparisons.
Any exception inside an admission boundary becomes its refusal, never admission.
Root canonicalization is inside that boundary, including free-text `keys[].label`.
`witnessSchema` is an integer exactly 1, never float 1.0 or boolean true. Pure
constructors (`receipt_id`, `make_result_ref`, `AdmittedRoot`) may reject misuse by
exception; they are not admission or recovery boundaries, and their constructed
values are revalidated at the use boundary.

The host connection entry is closed over operationRef, effectClass, brokerLocator,
underlyingLocator, grantGeneration, seq, binding and target; its binding has the
exact four existing identity members. Grant-state projections are closed over
status, token, binding and scope. Scope admits only the existing journal scope
members (pathPrefixes, variables, programs, endpoints, stateClass), plus the
host-attached snapshotDigest. That digest is derived from the held operation's
sealed snapshot; it is not an added journal GRANT member. Lists retain their
journal-schema bounds, are actual lists of NFC strings with no duplicates, and
pathPrefixes elements are normalized member paths. Unknown fields refuse. HE-2
requires snapshot binding and sealed membership in both relevant grant scopes;
HE-1 has exact target {stateClass, byteCap}, with cap 1..16 MiB. Grant policy cannot
create a new state class through this projection.

The request body is exactly {effectClass, authorizationRef, operationRef}. Both
context records have exactly their documented members. `effectResult` is the full
frozen control body, requiring requestSeq, decisionSeq, outcomeSeq, commitClass,
effectOutcome, and permitting only optional resultRef; numeric sequences are strict
uint53 and all enums and bounds remain unchanged. The former three-member fixture
projections are replaced with full bodies; removing optional resultRef still passes
shape validation but supplies no file to resolve. Malformed input releases no bytes.
Stage admission itself validates its stat, uid and positive cap, irrespective of
prior authorization. Recovery malformed class, footprint or sequence quarantines;
no outcome or receipt is fabricated to absorb a malformed record.

`security_boundary_mutations_v6.py` applies type-changing mutations at every
nested member of the retained root, witness, broker, courier, stage and recovery
controls, unknown fields at closed records, strict float/bool integer mutations,
required-member deletion, and exact v5 failure probes. Each has positive controls
and asserts a typed refusal with no exception. This is systematic design evidence,
not an exhaustive proof over all inputs or platform qualification. The original
332 checks are retained; four RA-without-intent expectations and the zero-cap
stage expectation change explicitly to the lawful refusal/cleanup described here.
The report records the exact count and every input digest. Retired outcome and
receipt prose is checked separately from executable behavior.
