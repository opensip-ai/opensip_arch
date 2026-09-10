"""Reference model for docs/v2/contracts/product-v1/security-and-lifecycle.md (PROPOSED, not self-accepted).

Design evidence only. Pure functions over JSON-shaped inputs; no filesystem, clock, process, network or
cryptography access. Nothing here is a product implementation, an OS measurement or a qualification
result. Every fixture consumed by this model is SYNTHETIC unless its record says otherwise.

TCB ASSUMPTIONS (inputs this model takes as already established by the trusted computing base):
  * `signers` / `signers` sets: key ids whose envelope signatures verify_envelope (security_unit_lib_v8)
    already accepted. The model decides thresholds, ordering and floors over asserted sets; it does not
    verify a signature.
  * `payload.newestIssuedAt`, `presentedRootIssuedAt`, `epoch.issuedAt`: issue times read from documents
    whose signatures were already verified. They are "admitted time evidence" only because of that.
  * `observation.{wall, mono, bootId}` and every platform observation (`sip`, `secureBoot`, `kernUuid`,
    `fsType`, `nsUnchanged` ...): values the host read from the OS. The model treats them as given.
  * fixture `fs` maps: lstat/ACL results the host would obtain with O_NOFOLLOW handles.
None of these is measured here. A boolean in a case file is a modelled assumption, not evidence.

Sections (numbers refer to the contract):
  S3  discovery(...)                 AR-03 custody-bounded discovery; VCS-root default; explicit joins
  S4  clock_decision(...)            AR-04 refusal of unattested forward excursion BEFORE evaluation/write
      recovery_challenge(...)        AR-04 challenge for a signed recovery epoch (poisoned floor)
      recovery_apply(...)            AR-04 authenticated floor recovery preserving counters/custody
  S5  verify_root_chain(...)         AR-05 expired-root chaining, old+new thresholds, final freshness
  S6  revocation_observe(...)        AR-05 live revocation: counter observation predicate
      observer_tick(...)             AR-05 fail-stop observer under OS scheduling assumptions
      linearize(...)                 AR-05 abstract brokered-commit linearization (fixture SEAL id)
      admit_seal_run_id_prefix(...)  run3 pattern only; not close_run
      admit_analysis_seal(...)       JournalRecord fields + identity-model.v3.close_run + RunId compare
  S7  lease_schedule(...)            AR-14 SHARED-READ / APPEND-WRITE / EXCLUSIVE lease modes, lock order,
                                     multi-namespace registry and the core-transition lock set (fence + EXCLUSIVE
                                     on every affected registered namespace, all-or-nothing, non-blocking)
  S8  platform_admit(...)            AR-06 two-tier admission over a four-platform profile population keyed by the
                                     ONE machine platform vocabulary (PLATFORM_IDS); display aliases never admit
  S9  migration_recover(...)         AR-14 crash recovery decision table
      migrate_floors(...)            AR-14 floors forward-only into the new store
      rollback_floors(...)           AR-14 floors forward-only back into the old store
  S3  boundary_inventory(...)        P3 export of the admitted authority boundaries (nested repositories/projects, custody
                                     exclusions) as the closed AdmittedBoundaryInventoryV1 the native unit instrument consumes
  S9.2 admit_transition_intent       installation transition (core update|repair|rollback, store migrate|rollback) intent semantics
      admit_transition_journal       closed InstallationTransitionJournalV1: admitted-intent digest, current/target schema, store
                                     and generation bindings, frozen registry, affected set and exact lease set held under the fence
      recover_transition_journal     crash recovery as the first act under the next fence: re-acquire the journaled set, fail closed
  S10 admit_repo_execution_grant     execution principal `repository-code` (grant V2: snapshot + sealed dependency-closure owners);
                                     OPERATIONAL admission, before any Plan exists (no Plan projection is an admission input)
      semantic_projection_for_grants the principals a consuming analysis must project into its Plan (preparation grants only)
      admit_plan_execution_projection Plan-time check that the projection equals the consumed preparation grants
      admit_repair_authorization     repair apply = brokered source mutation authorization, not a repo-execution grant
  S10.2 admit_recovery_authorization repair RECOVERY = separately authorized mutation within the original plan's authority,
                                     bound to the exact journal identity and observed journal state (single use, crash-safe);
                                     rollback/cleanup never consults recipe trust, commit re-consults it
  S9.1 admit_root_document           root schema 1 (v8 bytes) and schema 2 (exact extension recipe); reader sets
      admit_profile_set_envelope     signed PlatformProfileSetV1 under TR-PROFILE (schema 2) or core-embedded only
  S3.1 storage_write_admission       backup-custody choice before the first source-derived write (TM V17)
  S11 offline_guidance(...)          AR-16 offline windows and doctor outcome guidance

Two canonical profiles are used and never mixed:
  * `canon` below is `opensip-metadata-canonical.1` (NFC-required strings, i64 integers), the profile of
    signed security metadata (root, catalog, revocation, journal records, recovery challenge/epoch).
  * Product data (discovery provenance, grants, decision records) uses the foundation canonicalizer
    (`foundation/canonical.py`, no normalization, integers to 2^64-1). The checker applies it; this
    module serializes product data only through that imported canonicalizer (`_C.identity` / `_C.canonical`
    for the journal identity, journal-state and intent digests of S9.2 and S10.2), never through `canon`.

Uses the foundation exact validator and jsonschema. Python 3.12 is the reference interpreter; `-I -B` are required.
"""
import datetime
import hashlib
import re
import unicodedata
import copy,json,importlib.util
from pathlib import Path
_SCHEMA_BUNDLE=json.loads((Path(__file__).resolve().parent/'security-lifecycle.schemas.v1.json').read_text())
_cs=importlib.util.spec_from_file_location('security_exact',Path(__file__).resolve().parent.parent/'foundation/canonical.py')
_C=importlib.util.module_from_spec(_cs);_cs.loader.exec_module(_C)
# ONE shared zero-config discovery rule (pruned trees by path segment, unit cap, root sentinel), consumed here
# and by the native unit instrument; see ../discovery-defaults.py (post-reset review MUST-3).
_ds=importlib.util.spec_from_file_location('discovery_defaults',Path(__file__).resolve().parent.parent/'discovery-defaults.py')
DD=importlib.util.module_from_spec(_ds);_ds.loader.exec_module(DD)
def validate_input(name,value):
    schema=copy.deepcopy(_SCHEMA_BUNDLE);schema['$ref']='#/schemas/'+name
    _C.validate(schema,value)
    return value


# ---------------------------------------------------------------------------------------------
# Constants selected by the contract (numeric bounds are design selections, not measurements)
# ---------------------------------------------------------------------------------------------
DAY = 86400
FUTURE_TOLERANCE_S = 1 * DAY            # existing OD-112-2 value, unchanged (FC-FUTURE)
REVOCATION_FRESH_DAYS = 90              # existing OD-112-2 value, unchanged
CATALOG_EXPIRY_DAYS = 90                # existing
ROOT_EXPIRY_DAYS = 365                  # existing
UNATTESTED_FORWARD_HORIZON_S = REVOCATION_FRESH_DAYS * DAY   # S4: wall > admittedTime + 90 d is refused
SESSION_DEVIATION_TOLERANCE_S = 1 * DAY # S4: in-boot wall vs sleep-inclusive monotonic elapsed
TRUST_WARNING_WINDOW_DAYS = 14          # S11: pre-cliff warning
MAX_CONFIG_BYTES = 4 * 1024 * 1024      # foundation carrier ceiling, reused
MAX_WALK_DEPTH = 256                    # S3: bounded ancestor walk
MAX_EXPLICIT_JOINS = DD.MAX_WORKSPACE_UNITS   # S3: 4096; also the automatic first-party unit ceiling (shared rule)
WORKSPACE_MARKERS = DD.WORKSPACE_MARKERS   # S3: language workspace units (data only); shared with native discovery
RECOVERY_CHALLENGE_TTL_S = 1 * DAY      # S4.5: pending challenge lives one boot and 24 h of sleep-inclusive monotonic time
RECOVERY_ISSUE_SKEW_S = 1 * DAY         # S4.5: epoch issuedAt must lie within +/- 24 h of the wall at import
REVOCATION_POLL_INTERVAL_S = 5          # S6 (qualification obligation, see observer_tick)
REVOCATION_OBSERVATION_BOUND_S = 10     # S6: 2 x poll interval; a stall beyond it is fail-stop
CANCEL_GRACE_S = 2                      # S6: protocol Cancel wait
TERM_GRACE_S = 3                        # S6: SIGTERM wait
CANCELLATION_TOTAL_BOUND_S = 10         # S6: Cancel + TERM + KILL + reap + scratch cleanup
LEASE_RETRY_BUDGET_S = 30               # S7: CLI retry budget outside the fence
LEASE_RETRY_BACKOFF_S = (1, 2, 4, 8, 15)
FENCE_WAIT_BOUND_S = 5                  # S7: the fence is the only blocking lock; bounded wait
MIGRATION_ROLLBACK_WINDOW_DAYS = 30     # S9
HEX64 = re.compile(r'^[0-9a-f]{64}$')
PROJECT_ID_RE = re.compile(r'^prj1-[0-9a-f]{64}$')
SNAPSHOT_ID_RE = re.compile(r'^snapshot2:[0-9a-f]{64}$')
MACOS_BUILD_RE = re.compile(r'^(\d{2})([A-Z])(\d{1,5})([a-z])?$')
LINUX_OSRELEASE_RE = re.compile(r'^(\d+\.\d+\.\d+)-(\d+)-([a-z0-9]+)$')
TS_RE = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')

# D9 v1.14 joins (no class, code or exit is minted; every mapping below names an existing code)
D9 = {
    'CONFIG.CUSTODY_REFUSED':          ('request-rejected', 2, 'CONFIG.INVALID'),
    'PROJECT.ROOT_CUSTODY_REFUSED':    ('request-rejected', 2, 'CONFIG.INVALID'),
    'PROJECT.EXPLICIT_PATH_INVALID':   ('request-rejected', 2, 'CONFIG.INVALID'),
    'PROJECT.WORKSPACE_UNIT_LIMIT':    ('request-rejected', 2, 'REQUEST.UNSATISFIABLE'),   # S3: > 4096 first-party units, no truncation
    'CLOCK-EXCURSION-FORWARD':         ('request-rejected', 2, 'REQUEST.PRECONDITION_FAILED'),
    'TRUST.NO_ADMITTED_TIME_CONTEXT':  ('request-rejected', 2, 'REQUEST.PRECONDITION_FAILED'),
    'PAYLOAD-NOT-ADMISSIBLE':          ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'RECOVERY.REFUSED':                ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'CONTINUE-CORE-NOT-TRUSTED':       ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'TRUST.COMPONENT_REVOKED_DURING_OPERATION': ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'OBSERVER.FAIL_STOP':              ('operational-failed', 4, 'HOST.IO_FAILURE'),
    'PROJECT.BUSY':                    ('operational-failed', 4, 'LEDGER.BUSY_TIMEOUT'),
    'ROOT.SCHEMA_UNSUPPORTED':         ('request-rejected', 2, 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED'),
    'STATE.SCHEMA_UNSUPPORTED':        ('request-rejected', 2, 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED'),
    'ROOT.FLOOR_ABOVE_CORE':           ('request-rejected', 2, 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED'),
    'MIGRATION.CORRUPT':               ('operational-failed', 4, 'LEDGER.CORRUPT'),
    'HOST.IO_FAILURE':                 ('operational-failed', 4, 'HOST.IO_FAILURE'),
    'NT-TCB-BOOT':                     ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'NT-TCB-PROFILE-UNQUALIFIED':      ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'NT-TCB-IDENTITY':                 ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED'),
    'GRANT.REFUSED':                   ('request-rejected', 2, 'REQUEST.PRECONDITION_FAILED'),
    'PLAN.EXECUTION_PROJECTION_REFUSED': ('request-rejected', 2, 'REQUEST.PRECONDITION_FAILED'),   # S10: Plan projection vs consumed grants
    'TRANSITION.REFUSED':              ('request-rejected', 2, 'REQUEST.PRECONDITION_FAILED'),   # S9.2: installation transition intent/journal admission (all TRANSITION.* details)
}


def d9(code):
    cls, ex, c = D9[code]
    return {'class': cls, 'exit': ex, 'code': c}


class Reject(Exception):
    pass



# ---------------------------------------------------------------------------------------------
# S12 - projecting a security outcome onto the ONE closed public DomainDetail  (blind consumer M-5)
# ---------------------------------------------------------------------------------------------
# A public termination carries exactly one `domainDetail` = {code, remedy, subject?} where `code` is a
# member of the single closed registry (`../public-detail-registry.v1.json`, mirrored by
# workflows/schemas/common.schema.json#/$defs/DomainDetailCode). This unit therefore states its OWN
# closed vocabulary here and refuses to emit anything outside it; there is no wildcard family and no
# open `PROFILE_SET.*` prefix rule.
#
# The projection rule, which is the rule these bytes already follow:
#   1. The BASE CODE is everything before the first ':'; everything after it is subject data.
#      ('ROOT.ROLE_SET:1' -> code ROOT.ROLE_SET, subject '1'.)
#   2. If a `detail` is present and its base code is in this closed set, that is the public code and
#      the rest of the detail is the subject. This is why the 38 ROOT.* document defects are public
#      codes rather than collapsing into one PAYLOAD-NOT-ADMISSIBLE, and it is exactly why the
#      ENVELOPE.* / PROFILE_SET.* defects of `admit_profile_set_envelope` must be registered too:
#      they occupy the same position for the same reason (S9.1 names them as `detail`).
#   3. Otherwise the `refusal` supplies the public code and the whole `detail` travels as subject.
#      This is the reading S12 already uses for RECOVERY.REFUSED (CHALLENGE_EXPIRED, COUNTER_MISMATCH,
#      ...), for CONFIG.CUSTODY_REFUSED (SYMLINK, WRITABLE_BY_OTHERS, ...) and for
#      PROJECT.EXPLICIT_PATH_INVALID (JOIN_PATH_GRAMMAR, ...). Those sub-details are NOT registry
#      members and must not become a second public vocabulary.
#   4. Anything else refuses. An unknown internal key never reaches a public envelope.
# The D9 class/exit/code always comes from the `refusal`, never from the detail: naming a defect more
# precisely never changes its termination branch.
SECURITY_PUBLIC_DETAIL_CODES = frozenset({
    'AUTHZ.BASE_SNAPSHOT_MISMATCH', 'AUTHZ.CI_FLAG_MISMATCH', 'AUTHZ.CI_REQUIRES_POLICY_RECORD',
    'AUTHZ.CONSENT_MODE', 'AUTHZ.CONSENT_SHAPE', 'AUTHZ.CUSTODY_NOT_ADMITTED',
    'AUTHZ.EXPIRED', 'AUTHZ.EXPIRY', 'AUTHZ.JOURNAL_CONTEXT',
    'AUTHZ.JOURNAL_MISMATCH', 'AUTHZ.JOURNAL_NOT_OF_THIS_PLAN', 'AUTHZ.JOURNAL_STATE_MISMATCH',
    'AUTHZ.JOURNAL_STATE_MOVED', 'AUTHZ.JOURNAL_STATE_UNKNOWN', 'AUTHZ.LEASE_MODE',
    'AUTHZ.LIFETIME_BOUND', 'AUTHZ.MUTATION_BOUNDARY', 'AUTHZ.NEW_EDITS_NOT_GRANTABLE_HERE',
    'AUTHZ.NOT_YET_VALID', 'AUTHZ.NO_ADMITTED_TIME_CONTEXT', 'AUTHZ.ORIGINAL_REQUEST_MISMATCH',
    'AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR', 'AUTHZ.POLICY_RECORD_ID', 'AUTHZ.PROJECT_ID_MISMATCH',
    'AUTHZ.RECIPE_CLOSURE_MISMATCH', 'AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED', 'AUTHZ.RECIPE_CLOSURE_REVOKED',
    'AUTHZ.RECIPE_CLOSURE_SHAPE', 'AUTHZ.RECOVERY_ACTION_MISMATCH', 'AUTHZ.RECOVERY_ACTION_UNKNOWN',
    'AUTHZ.RECOVERY_EXECUTION_NOT_FRESH', 'AUTHZ.RECOVERY_NOT_MUTATING', 'AUTHZ.RECOVERY_REQUEST_MISMATCH',
    'AUTHZ.RECOVERY_REQUEST_NOT_FRESH', 'AUTHZ.REPAIR_PLAN_MISMATCH', 'AUTHZ.REPOSITORY_EXECUTION_NOT_GRANTABLE_HERE',
    'AUTHZ.REQUEST_ID_SHAPE', 'AUTHZ.SHAPE', 'AUTHZ.SOURCE_MOVED',
    'AUTHZ.TIME_GRAMMAR', 'CLOCK-EXCURSION-FORWARD', 'CONFIG.CUSTODY_REFUSED',
    'CONFIG.INVALID', 'CONTINUE-CORE-NOT-TRUSTED', 'ENVELOPE.BODY_DIGEST',
    'ENVELOPE.KIND', 'ENVELOPE.SHAPE', 'GRANT.ARGV_MISMATCH',
    'GRANT.AUTHORIZATION_MODE', 'GRANT.AUTHORIZATION_SHAPE', 'GRANT.CI_FLAG_MISMATCH',
    'GRANT.CI_REQUIRES_POLICY_RECORD', 'GRANT.DEPENDENCY_SET_MISMATCH', 'GRANT.DEPENDENCY_SET_SHAPE',
    'GRANT.EFFECTS_SHAPE', 'GRANT.ENFORCEMENT_CLAIM_NOT_IN_TRUTH_TABLE', 'GRANT.ENFORCEMENT_VOCABULARY',
    'GRANT.EXECUTION_CLASS', 'GRANT.EXPIRY', 'GRANT.INHERITED',
    'GRANT.OWNERS_SHAPE', 'GRANT.OWNER_DUPLICATE', 'GRANT.OWNER_MANIFEST_MISMATCH',
    'GRANT.OWNER_NOT_IN_SEALED_SET', 'GRANT.OWNER_SOURCE_DIGEST_MISMATCH', 'GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID',
    'GRANT.PLATFORM_NOT_IN_TRUTH_TABLE', 'GRANT.POLICY_DOES_NOT_ADMIT_PRINCIPAL', 'GRANT.POLICY_RECORD_ID',
    'GRANT.PRINCIPAL_NOT_REPOSITORY_CODE', 'GRANT.PROJECT_ID_MISMATCH', 'GRANT.REFUSED',
    'GRANT.RUNNER_MUST_BE_TOOL_CLOSURE', 'GRANT.RUNNER_NOT_IN_TOOL_CLOSURE', 'GRANT.RUNNER_NOT_SEALED_MEMBER',
    'GRANT.RUNNER_SHAPE', 'GRANT.SCHEMA', 'GRANT.SEMANTIC_PRINCIPAL_KIND',
    'GRANT.SHAPE', 'GRANT.SNAPSHOT_MISMATCH', 'GRANT.TOOL_CLOSURE_MISMATCH',
    'HOST.IO_FAILURE', 'MIGRATION.CORRUPT', 'NT-TCB-BOOT',
    'NT-TCB-IDENTITY', 'NT-TCB-PROFILE-UNQUALIFIED', 'OBSERVER.FAIL_STOP',
    'PAYLOAD-NOT-ADMISSIBLE', 'PLAN.CONSUMED_GRANT_SHAPE', 'PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED',
    'PLAN.EXECUTION_PROJECTION_REFUSED', 'PLAN.GRANT_CONSUMED_WITHOUT_HOST_PREPARED', 'PLAN.HOST_PREPARED_WITHOUT_GRANT',
    'PLAN.PREPARED_RESOLUTION_UNKNOWN', 'PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT', 'PLAN.TEST_RUNNER_HAS_NO_PLAN',
    'PROFILE_SET.CANON', 'PROFILE_SET.CORE_PIN_MISMATCH', 'PROFILE_SET.NO_TR_PROFILE_ROLE',
    'PROFILE_SET.SCHEMA', 'PROFILE_SET.SCHEMA_SHAPE', 'PROFILE_SET.SIGNATURE_THRESHOLD',
    'PROJECT.BUSY', 'PROJECT.EXPLICIT_PATH_INVALID', 'PROJECT.ROOT_CUSTODY_REFUSED',
    'PROJECT.WORKSPACE_UNIT_LIMIT', 'RECOVERY.REFUSED', 'ROOT.CHAIN_BACKDATED',
    'ROOT.CHAIN_GAP', 'ROOT.CHAIN_NEW_THRESHOLD', 'ROOT.CHAIN_OLD_THRESHOLD',
    'ROOT.CHAIN_ORIGIN_INCONSISTENT', 'ROOT.EXPIRED_NO_CHAIN', 'ROOT.EXPIRY_NOT_AFTER_ISSUE',
    'ROOT.FINAL_EXPIRED', 'ROOT.FINAL_FUTURE', 'ROOT.FLOOR_ABOVE_CORE',
    'ROOT.ISSUE_NOT_BEFORE_EXPIRY', 'ROOT.KERNEL_ATTESTATION_KEYS', 'ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY',
    'ROOT.KERNEL_ATTESTATION_KEYS_POLICY', 'ROOT.KEYS_SHAPE', 'ROOT.KEY_ID',
    'ROOT.KEY_REUSE', 'ROOT.KEY_REUSED_ACROSS_ROLES', 'ROOT.PREVIOUS_VERSION',
    'ROOT.RECOVERY_AUTHORITY', 'ROOT.ROLE_SET', 'ROOT.ROLE_SHAPE',
    'ROOT.ROLE_THRESHOLD', 'ROOT.ROLE_THRESHOLD_POLICY', 'ROOT.ROOT_KEYS',
    'ROOT.ROOT_THRESHOLD_POLICY', 'ROOT.SCHEMA_CONSTANT_TYPE', 'ROOT.SCHEMA_SHAPE',
    'ROOT.SCHEMA_UNSUPPORTED', 'ROOT.SHAPE', 'ROOT.STATE_INCONSISTENT',
    'ROOT.TIMESTAMP_GRAMMAR', 'ROOT.TR_REPAIR_ACTIVE_UNDER_SCHEMA_1', 'ROOT.TR_REPAIR_MUST_BE_TYPED_ABSENCE',
    'ROOT.TR_PROFILE_THRESHOLD_POLICY', 'ROOT.TR_REPAIR_STANDING', 'ROOT.TR_REPAIR_THRESHOLD_POLICY',
    'ROOT.UNKNOWN_KEY', 'ROOT.VERSION_RANGE',
    'ROOT.VERSION_TYPE', 'STATE.SCHEMA_UNSUPPORTED', 'TRANSITION.CLOSURE_SHAPE',
    'TRANSITION.CONTEXT_INTENT', 'TRANSITION.CURRENT_SCHEMA_MISMATCH', 'TRANSITION.CURRENT_STORE_MISMATCH',
    'TRANSITION.DEADLINE_ONLY_FOR_ROLLBACK', 'TRANSITION.FENCE_NOT_HELD', 'TRANSITION.GENERATION_SHAPE',
    'TRANSITION.INITIAL_STATE', 'TRANSITION.INTENT_DIGEST_MISMATCH', 'TRANSITION.INTENT_FIELD_MISMATCH',
    'TRANSITION.INTENT_SCHEMA', 'TRANSITION.INTENT_SHAPE', 'TRANSITION.JOURNAL_LAW_CONSTANTS',
    'TRANSITION.JOURNAL_SHAPE', 'TRANSITION.LEASE_SET_NOT_HELD', 'TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE',
    'TRANSITION.NO_ADMITTED_TIME_CONTEXT', 'TRANSITION.OPERATION', 'TRANSITION.PRECONDITION_GENERATION_MISMATCH',
    'TRANSITION.PROFILE_DIGEST_SHAPE', 'TRANSITION.REFUSED', 'TRANSITION.REGISTRY_DIGEST_MISMATCH',
    'TRANSITION.REGISTRY_MISMATCH', 'TRANSITION.REPAIR_MUST_KEEP_CLOSURE', 'TRANSITION.REPAIR_MUST_KEEP_SCHEMA',
    'TRANSITION.REPAIR_MUST_KEEP_STORE', 'TRANSITION.ROLLBACK_CANNOT_RAISE_SCHEMA', 'TRANSITION.ROLLBACK_DEADLINE_SHAPE',
    'TRANSITION.ROLLBACK_MUST_CHANGE_CLOSURE', 'TRANSITION.ROLLBACK_REQUIRES_DEADLINE', 'TRANSITION.ROLLBACK_WINDOW_EXPIRED',
    'TRANSITION.SAME_SCHEMA_KEEPS_STORE', 'TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE', 'TRANSITION.SCOPE_MISMATCH',
    'TRANSITION.STATE_SCHEMA', 'TRANSITION.STORE_OPERATION_KEEPS_CORE', 'TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT',
    'TRANSITION.UPDATE_CANNOT_LOWER_SCHEMA', 'TRANSITION.UPDATE_MUST_CHANGE_CLOSURE', 'TRUST.COMPONENT_REVOKED_DURING_OPERATION',
    'TRUST.FLOOR_AHEAD_OF_WALL', 'TRUST.NO_ADMITTED_TIME_CONTEXT', 'storage.backup-choice-required'
})

# The declared BOUND on the gap between this closed set and the shared registry: codes this unit emits
# that the registry did not carry when they were authored. It is a bound the checker asserts, not the live
# answer: `pendingRegistration` below is computed against the registry file itself, so the flag clears by
# itself as soon as the registry owner lands the records and no stale `true` survives integration.
PENDING_PUBLIC_DETAIL_REGISTRATIONS = frozenset({
    'ENVELOPE.BODY_DIGEST', 'ENVELOPE.KIND', 'ENVELOPE.SHAPE',
    'PROFILE_SET.CANON', 'PROFILE_SET.CORE_PIN_MISMATCH', 'PROFILE_SET.NO_TR_PROFILE_ROLE',
    'PROFILE_SET.SCHEMA', 'PROFILE_SET.SCHEMA_SHAPE', 'PROFILE_SET.SIGNATURE_THRESHOLD',
    # Found by the sweep below, not by inspection: S9.1's schema-2 rule emits a per-ROLE threshold-policy
    # code ('ROOT.%s_THRESHOLD_POLICY' % role), so TR-REPAIR and TR-PROFILE each have one. The registry
    # carries ROOT.ROLE_THRESHOLD_POLICY and ROOT.ROOT_THRESHOLD_POLICY but neither of these two.
    'ROOT.TR_PROFILE_THRESHOLD_POLICY', 'ROOT.TR_REPAIR_THRESHOLD_POLICY',
})

# Internal decision keys this unit produces that are NOT public codes; the host normalizes them at the
# boundary exactly as it normalizes the native aliases. `PROFILE_SET_KEY_NOT_MACHINE_ID` is deliberately
# absent: it is not an alias but a SUBJECT sub-detail of the registered NT-TCB-PROFILE-UNQUALIFIED (S8).
SECURITY_INTERNAL_DETAIL_ALIASES = {
    'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT': 'TRUST.COMPONENT_REVOKED_DURING_OPERATION',
}

# The eight dotted families whose members this unit publishes as public codes. A detail whose base code
# is inside one of them but outside the closed set above is a REFUSAL, not a silently degraded subject:
# that is what keeps `PROFILE_SET.*` and `ENVELOPE.*` from becoming an unbounded wildcard vocabulary.
# Sub-details outside these families (CHALLENGE_EXPIRED, SYMLINK, JOIN_PATH_GRAMMAR, ...) are ordinary
# subject text and are deliberately NOT registry members.
SECURITY_PUBLIC_DETAIL_FAMILIES = ('AUTHZ.', 'ENVELOPE.', 'GRANT.', 'NT-TCB-', 'PLAN.', 'PROFILE_SET.',
                                   'ROOT.', 'TRANSITION.')

# The one detail whose D9 branch differs from its enclosing refusal (S12): a revoked recipe closure is an
# admission rejection, while every other AUTHZ.* detail of the same admission is a precondition failure.
SECURITY_DETAIL_D9_OVERRIDE = {
    'AUTHZ.RECIPE_CLOSURE_REVOKED': {'class': 'request-rejected', 'exit': 2, 'code': 'EXTENSION.ADMISSION_REJECTED'},
}

# S12 row `PAYLOAD-NOT-ADMISSIBLE (incl. ROOT.*, ENVELOPE.*, PROFILE_SET.* details)`, stated as a rule
# rather than left to a silent default: a member of the three DOCUMENT-ADMISSION families that the D9 map
# does not name explicitly (the ROOT.CHAIN_* / ROOT.FINAL_* / ROOT.*_SHAPE defects, every ENVELOPE.* and
# every PROFILE_SET.*) is a payload that is not admissible. The three schema-major refusals
# (ROOT.SCHEMA_UNSUPPORTED, STATE.SCHEMA_UNSUPPORTED, ROOT.FLOOR_ABOVE_CORE) keep their own D9 row, so
# this rule never reassigns a branch the map already decided.
SECURITY_DOCUMENT_ADMISSION_FAMILIES = ('ENVELOPE.', 'PROFILE_SET.', 'ROOT.')


_PUBLIC_DETAIL_REGISTRY = Path(__file__).resolve().parent.parent / 'public-detail-registry.v1.json'
_registered_public_detail_codes = None


def registered_public_detail_codes():
    """The shared closed registry, READ ONLY. This unit never edits it; it reads it so that
    `pendingRegistration` is the live answer rather than a drafting constant. If the file is unreadable the
    declared bound is used, which can only over-report a gap, never hide one."""
    global _registered_public_detail_codes
    if _registered_public_detail_codes is None:
        try:
            _registered_public_detail_codes = frozenset(
                r['code'] for r in json.loads(_PUBLIC_DETAIL_REGISTRY.read_text())['records'])
        except Exception:
            _registered_public_detail_codes = SECURITY_PUBLIC_DETAIL_CODES - PENDING_PUBLIC_DETAIL_REGISTRATIONS
    return _registered_public_detail_codes


def public_detail_split(text):
    """(base code, subject or None). The subject is everything after the FIRST colon."""
    if not isinstance(text, str) or not text:
        raise Reject('PUBLIC_DETAIL_EMPTY')
    base, sep, subject = text.partition(':')
    return base, (subject if sep else None)


def public_detail(refusal, detail=None, remedy=None, d9_branch=None):
    """Project one security refusal onto the closed public DomainDetail plus its D9 branch.

    `d9_branch` is the branch the emitting function already decided (some outcomes carry the D9 error
    code, not a D9 map key, in their `refusal` field); when absent it is derived from the refusal.
    """
    alias = SECURITY_INTERNAL_DETAIL_ALIASES.get(refusal)
    if alias is not None:
        refusal, detail = alias, (detail if detail is not None else refusal)
    refusal_base, refusal_subject = public_detail_split(refusal)
    if detail is not None:
        detail_base, detail_subject = public_detail_split(detail)
        if detail_base in SECURITY_PUBLIC_DETAIL_CODES:
            code, subject = detail_base, detail_subject
        elif detail_base.startswith(SECURITY_PUBLIC_DETAIL_FAMILIES):
            raise Reject('PUBLIC_DETAIL_UNREGISTERED:' + detail_base)
        elif refusal_base in SECURITY_PUBLIC_DETAIL_CODES:
            code, subject = refusal_base, detail
        else:
            raise Reject('PUBLIC_DETAIL_UNREGISTERED:' + detail_base)
    elif refusal_base in SECURITY_PUBLIC_DETAIL_CODES:
        code, subject = refusal_base, refusal_subject
    else:
        raise Reject('PUBLIC_DETAIL_UNREGISTERED_REFUSAL:' + refusal_base)
    if code in SECURITY_DETAIL_D9_OVERRIDE:
        branch = dict(SECURITY_DETAIL_D9_OVERRIDE[code])
    elif d9_branch is not None:
        branch = d9_branch
    elif refusal_base in D9:
        branch = d9(refusal_base)
    elif (refusal_base in SECURITY_PUBLIC_DETAIL_CODES
          and refusal_base.startswith(SECURITY_DOCUMENT_ADMISSION_FAMILIES)):
        branch = d9('PAYLOAD-NOT-ADMISSIBLE')
    else:
        raise Reject('PUBLIC_DETAIL_NO_D9_BRANCH:' + refusal_base)
    out = {'code': code, 'subject': subject, 'd9': branch,
           'pendingRegistration': code not in registered_public_detail_codes()}
    if remedy is not None:
        out['remedy'] = remedy
    return out


def public_details(outcome, refusal_key=None):
    """Every public DomainDetail a model outcome projects to.

    Two emitted shapes are covered: `{refusal, detail}` records (root/profile-set/envelope/storage
    admission, clock decisions) and `{refusals: [...]}` lists (grant, plan-projection, repair,
    recovery and transition admission), whose entries already carry their own base code and whose D9
    branch comes from the enclosing `refusal_key`.
    """
    if not isinstance(outcome, dict):
        raise Reject('PUBLIC_DETAIL_OUTCOME_SHAPE')
    branch = outcome.get('d9')
    items = []
    for entry in outcome.get('refusals') or ():
        items.append(public_detail(refusal_key or entry, None if refusal_key is None else entry,
                                   d9_branch=branch if refusal_key else None))
    if outcome.get('refusal') is not None:
        items.append(public_detail(outcome['refusal'], outcome.get('detail'), d9_branch=branch))
    return items

# ---------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------
def ts(s):
    """ISO-8601 `YYYY-MM-DDTHH:MM:SSZ` -> epoch seconds (int). The Z grammar is the schema's."""
    if s is None:
        return None
    if not isinstance(s, str) or not TS_RE.fullmatch(s):
        raise Reject('TIMESTAMP_GRAMMAR:%r' % (s,))
    dt = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp())


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def canon(v):
    """opensip-metadata-canonical.1 as in security_unit_lib_v8.canon (copied discipline for signed
    security metadata only; NOT the product serializer, which lives in foundation/canonical.py)."""
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if v is None:
        return 'null'
    if isinstance(v, int):
        if v < -2**63 or v > 2**63 - 1:
            raise Reject('INTEGER_OUT_OF_RANGE')
        return str(v)
    if isinstance(v, float):
        raise Reject('FLOAT_FORBIDDEN')
    if isinstance(v, str):
        v.encode('utf-8')
        if unicodedata.normalize('NFC', v) != v:
            raise Reject('NON_NFC_STRING')
        out = ['"']
        for ch in v:
            o = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == '\\':
                out.append('\\\\')
            elif ch == '\b':
                out.append('\\b')
            elif ch == '\t':
                out.append('\\t')
            elif ch == '\n':
                out.append('\\n')
            elif ch == '\f':
                out.append('\\f')
            elif ch == '\r':
                out.append('\\r')
            elif o < 0x20:
                out.append('\\u%04x' % o)
            else:
                out.append(ch)
        out.append('"')
        return ''.join(out)
    if isinstance(v, list):
        return '[' + ','.join(canon(x) for x in v) + ']'
    if isinstance(v, dict):
        ks = sorted(v.keys(), key=lambda k: [ord(c) for c in k])
        return '{' + ','.join(canon(k) + ':' + canon(v[k]) for k in ks) + '}'
    raise Reject('OUTSIDE_DATA_MODEL')


def journal_body_sha(body):
    return hashlib.sha256(b'opensip.metadata.journal.1\x00' + canon(body).encode('utf-8')).hexdigest()


def metadata_sha(domain, body):
    """Domain-framed digest under the metadata profile (signed security metadata family)."""
    return hashlib.sha256(domain.encode('ascii') + b'\x00' + canon(body).encode('utf-8')).hexdigest()


# =============================================================================================
# S3 - Discovery (AR-03)
# =============================================================================================
def _parent(path):
    if path == '/':
        return None
    p = path.rsplit('/', 1)[0]
    return p if p else '/'


def _join(d, name):
    return '/' + name if d == '/' else d + '/' + name


def _mode(entry):
    """Fixture modes are octal strings ("1777") or integers; symlink/absent entries have no mode."""
    m = entry.get('mode', 0)
    if isinstance(m, str):
        return int(m, 8)
    if not _int(m):
        raise Reject('MODE_MALFORMED')
    return m


def _acl_write_custody(entry, uid, groups):
    """POSIX ACL / macOS ACL write grants are custody facts. Fixture: aclWrite = ['uid:1001', 'group:50'].
    `aclUnreadable: true` models EACCES/ENOTSUP-unknown on the ACL read: custody cannot be established."""
    if entry.get('aclUnreadable'):
        return 'ACL_UNREADABLE'
    for p in entry.get('aclWrite', []):
        if p in ('uid:%d' % uid, 'uid:0'):
            continue
        if p.startswith('group:') and _int_or_none(p[6:]) in groups:
            continue
        return 'WRITABLE_BY_ACL'
    return None


def _int_or_none(s):
    try:
        return int(s)
    except ValueError:
        return None


def _dir_custody(entry, uid, waive_owner, groups):
    if entry is None:
        return 'ABSENT'
    kind = entry.get('kind')
    if kind == 'symlink':
        return 'SYMLINK'
    if kind != 'dir':
        return 'NOT_A_DIRECTORY'
    if not waive_owner and entry.get('uid') not in (uid, 0):
        return 'FOREIGN_OWNER'
    mode = _mode(entry)
    if mode & 0o002:
        return 'WRITABLE_BY_OTHERS'
    if mode & 0o020 and entry.get('gid') not in groups:
        return 'WRITABLE_BY_GROUP'
    return _acl_write_custody(entry, uid, groups)


def _file_custody(entry, uid, waive_owner, groups):
    kind = entry.get('kind')
    if kind == 'symlink':
        return 'SYMLINK'
    if kind != 'file':
        return 'NOT_A_REGULAR_FILE'
    if not waive_owner and entry.get('uid') not in (uid, 0):
        return 'FOREIGN_OWNER'
    mode = _mode(entry)
    if mode & 0o002:
        return 'WRITABLE_BY_OTHERS'
    if mode & 0o020 and entry.get('gid') not in groups:
        return 'WRITABLE_BY_GROUP'
    acl = _acl_write_custody(entry, uid, groups)
    if acl:
        return acl
    if entry.get('nlink', 1) != 1:
        return 'HARD_LINKED'
    if entry.get('size', 0) > MAX_CONFIG_BYTES:
        return 'TOO_LARGE'
    return None


def _vcs_info(entry):
    v = entry.get('vcs')
    if not v:
        return None
    if v is True:
        return {'kind': 'directory', 'target': None, 'followed': False}
    if isinstance(v, dict) and v.get('kind') == 'indirection':
        # `.git` file with `gitdir: <path>`: data, never followed by discovery
        return {'kind': 'indirection', 'target': v.get('target'), 'followed': False}
    raise Reject('VCS_FIXTURE_MALFORMED')


def discovery(inp):
    """DISCOVERY-V1. Input is a synthetic lstat/ACL map plus invocation facts; output is the closed
    DiscoveryProvenanceV1 record or a typed refusal. Deterministic: no environment variable, no PATH,
    no HOME variable (the account home comes from the account database), fixed walk order.
    `authorizedGroupIds` come only from an explicit `--trust-group <gid>` invocation argument."""
    # Closed synthetic host-observation vocabulary, not a public request carrier.
    # A misspelled fixture/host projection is an instrument error, never an ignored option.
    allowed = {'invokingUid','accountHome','cwd','fs','ci','trustProjectOwner',
               'authorizedGroupIds','explicitProject','explicitResolved','explicitJoins','configWorkspaceRoots'}
    required = {'invokingUid','accountHome','cwd','fs'}
    if not isinstance(inp, dict) or not required <= set(inp) or set(inp) - allowed:
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    if not _int(inp['invokingUid']) or inp['invokingUid'] < 0 or not isinstance(inp['fs'], dict):
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    if any(k in inp and type(inp[k]) is not bool for k in ('ci','trustProjectOwner')):
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    if any(not isinstance(inp[k], str) for k in ('accountHome','cwd')):
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    if any(k in inp and inp[k] is not None and not isinstance(inp[k], str) for k in ('explicitProject','explicitResolved')):
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    for key in ('authorizedGroupIds','explicitJoins','configWorkspaceRoots'):
        if key in inp and not isinstance(inp[key], list):
            raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    if any(not _int(g) or g < 0 for g in inp.get('authorizedGroupIds', [])):
        raise Reject('DISCOVERY_OBSERVATION_SHAPE')
    uid = inp['invokingUid']
    home = inp['accountHome']
    fs = inp['fs']
    ci = bool(inp.get('ci', False))
    waive = bool(inp.get('trustProjectOwner', False))
    groups = set(g for g in inp.get('authorizedGroupIds', []) if _int(g))
    explicit = inp.get('explicitProject')
    joins = inp.get('explicitJoins', [])
    config_roots = inp.get('configWorkspaceRoots', [])   # admitted Config2 `discovery.workspaceRoots` (after foundation admission)
    prov = {'schemaVersion': 1, 'mode': None, 'ci': ci, 'selectedRoot': None, 'configPath': None,
            'walked': [], 'stopReason': None, 'custodyWaiver': 'trustProjectOwner' if waive else None,
            'authorizedGroupIds': sorted(groups), 'vcs': None, 'nestedRepositories': [], 'nestedProjects': [], 'unitSource': None, 'units': [],
            'excludedUnits': [], 'prunedTrees': [], 'explicitPathWasSymlink': None, 'warnings': []}

    def refuse(code, path, detail):
        return {'status': 'REFUSE', 'refusal': code, 'path': path, 'detail': detail, 'd9': d9(code), 'provenance': prov}

    def examine_config(directory, rec):
        cfg = _join(directory, 'opensip.json')
        centry = fs.get(cfg)
        if centry is None:
            return None, None
        fwhy = _file_custody(centry, uid, waive if prov['mode'] == 'explicit' else False, groups)
        if fwhy is not None:
            rec['candidate'] = 'REFUSED'
            return cfg, fwhy
        rec['candidate'] = 'PRESENT'
        return cfg, None

    def _in_nested_repo(p):
        """ONE boundary prefix rule shared with the native instrument (`DD.classify_boundary`, P3)."""
        hit = DD.classify_boundary(p, prov['nestedRepositories'], ())
        return hit is not None

    def _in_nested_project(p):
        """A nested `opensip.json` is a DELIBERATE project boundary (post-reset review ADV-3): from inside it, the
        walk selects it (nearest config wins, S3); from the enclosing project it is another authority root, recorded
        as `nestedProjects`, never entered by automatic discovery, and reachable only by its own launch/--project.
        Same shared prefix rule as `_in_nested_repo`."""
        hit = DD.classify_boundary(p, (), prov['nestedProjects'])
        return hit is not None

    def _markers(directory):
        """Manifest markers present in `directory` and passing file custody. Parsing a manifest is DATA
        only: no script, hook, plugin or workspace member globs are executed or followed; no source is
        written. A marker failing file custody is not a marker (recorded in `excludedUnits`)."""
        found, bad = [], []
        for m in WORKSPACE_MARKERS:
            e = fs.get(_join(directory, m))
            if e is None:
                continue
            why = _file_custody(e, uid, False, groups)
            (found if why is None else bad).append(m if why is None else m + ':' + why)
        return found, bad

    def _unit_custody(rel):
        """Every directory from the root to the unit must pass directory custody; returns (subpath, why) or None."""
        if rel == '.':
            why = _dir_custody(fs.get(prov['selectedRoot']), uid, waive, groups)
            return (prov['selectedRoot'], why) if why is not None else None
        parts = rel.split('/')
        for i in range(1, len(parts) + 1):
            sub = _join(prov['selectedRoot'], '/'.join(parts[:i]))
            why = _dir_custody(fs.get(sub), uid, waive, groups)
            if why is not None:
                return sub, why
        return None

    def _explicit_units(paths, kind, too_many):
        """Explicit roots are EXACT roots (never scan roots). The sentinel `.` and the path grammar come from the
        shared discovery rule (`DD.normalize_explicit_root`), so a Config2 `workspaceRoots` value has the same
        meaning here and in the native unit instrument. An explicit root inside a pruned tree (node_modules,
        VCS tree, Cargo target) is refused: the user named a dependency/output tree, not first-party source."""
        if len(paths) > MAX_EXPLICIT_JOINS:
            return refuse('PROJECT.EXPLICIT_PATH_INVALID', None, too_many)
        cargo_roots = DD.cargo_roots_from_markers(_relative_marker_paths(prov['selectedRoot']))
        for j in paths:
            try:
                rel = DD.normalize_explicit_root(j)
            except (DD.RootGrammarError, TypeError):
                return refuse('PROJECT.EXPLICIT_PATH_INVALID', j if isinstance(j, str) else None, 'JOIN_PATH_GRAMMAR')
            jp = prov['selectedRoot'] if rel == DD.INTERNAL_ROOT else _join(prov['selectedRoot'], rel)
            if _in_nested_repo(jp):
                # crossing into a nested repository (another custody root) needs its own --project, not a join
                return refuse('PROJECT.EXPLICIT_PATH_INVALID', jp, 'JOIN_CROSSES_NESTED_REPOSITORY')
            if _in_nested_project(jp):
                return refuse('PROJECT.EXPLICIT_PATH_INVALID', jp, 'JOIN_CROSSES_NESTED_PROJECT')
            hit = DD.classify_path(rel, cargo_roots) if rel else None
            if hit is not None:
                return refuse('PROJECT.EXPLICIT_PATH_INVALID', jp, 'JOIN_INSIDE_PRUNED_TREE:' + hit[1] + ':' + hit[0])
            bad = _unit_custody(rel or '.')
            if bad is not None:
                sub, why = bad
                if why in ('ABSENT', 'NOT_A_DIRECTORY'):
                    return refuse('PROJECT.EXPLICIT_PATH_INVALID', sub, why)
                return refuse('PROJECT.ROOT_CUSTODY_REFUSED', sub, why)
            markers, bad_markers = _markers(jp)
            prov['units'].append({'path': jp, 'kind': kind, 'markers': markers})
            for b in bad_markers:
                prov['excludedUnits'].append({'path': jp, 'reason': 'MARKER_CUSTODY:' + b})
            if not markers:
                # custody is admitted here; the language-unit layer (native section 1.4) refuses an explicit root
                # without a language marker as CONFIG.INVALID `native.explicit-root-without-marker`
                prov['warnings'].append('EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER:' + jp)
        return None

    def _relative_marker_paths(root):
        """Relative paths (internal form, root = ``) of every marker FILE entry under the selected root."""
        base = root.rstrip('/') + '/'
        return sorted(p[len(base):] for p, e in fs.items()
                      if e.get('kind') == 'file' and p.rsplit('/', 1)[-1] in WORKSPACE_MARKERS and p.startswith(base))

    def finish(root):
        prov['selectedRoot'] = root
        # nested repositories under the selected root are other authority/custody roots: recorded, never
        # examined or entered; crossing into one needs an explicit --project of its own
        for p, e in sorted(fs.items()):
            if p != root and p.startswith(root.rstrip('/') + '/') and e.get('kind') == 'dir' and e.get('vcs'):
                prov['nestedRepositories'].append(p)
        # nested `opensip.json` files under the selected root are deliberate project boundaries (ADV-3): recorded,
        # never entered. Ones inside pruned trees (a dependency's own opensip.json) or nested repositories are not projects
        # of this tree at all and are ignored here.
        base_rel = root.rstrip('/') + '/'
        cargo_roots = DD.cargo_roots_from_markers(_relative_marker_paths(root))
        for p, e in sorted(fs.items()):
            if p != _join(root, 'opensip.json') and p.startswith(base_rel) and p.rsplit('/', 1)[-1] == 'opensip.json' and e.get('kind') == 'file':
                d = _parent(p)
                if _in_nested_repo(d) or DD.classify_path(p[len(base_rel):], cargo_roots) is not None:
                    continue
                prov['nestedProjects'].append(d)
        # Unit source precedence: explicit CLI joins > admitted Config2 discovery.workspaceRoots > automatic
        # marker discovery inside the admitted root. Explicit sources are custody-checked like joins and
        # refuse on failure (explicit intent); automatic units failing custody are excluded, not refused.
        if joins:
            prov['unitSource'] = 'explicit-joins'
            r = _explicit_units(joins, 'explicit-join', 'TOO_MANY_JOINS')
            if r is not None:
                return r
        elif config_roots:
            prov['unitSource'] = 'config-workspace-roots'
            r = _explicit_units(config_roots, 'config-workspace-root', 'TOO_MANY_WORKSPACE_ROOTS')
            if r is not None:
                return r
        else:
            prov['unitSource'] = 'automatic'
            # ONE shared rule (../discovery-defaults.py): dependency trees (node_modules), VCS trees and Cargo build
            # output (`target` directly under a directory holding Cargo.toml) are pruned by exact path segment BEFORE
            # any custody walk; each pruned tree is recorded once. Installed package manifests therefore never become
            # units and never count toward the cap. The cap counts first-party marker directories and refuses typed.
            enum = DD.enumerate_units(_relative_marker_paths(root), enforce_limit=False)
            prov['prunedTrees'] = [{'path': _join(root, t['path']), 'reason': t['reason'], 'markerCount': t['markerCount']} for t in enum['prunedTrees']]
            for rel in enum['unitDirs']:
                d = root if rel == DD.INTERNAL_ROOT else _join(root, rel)
                if _in_nested_repo(d):
                    prov['excludedUnits'].append({'path': d, 'reason': 'INSIDE_NESTED_REPOSITORY'})
                    continue
                if _in_nested_project(d):
                    prov['excludedUnits'].append({'path': d, 'reason': 'INSIDE_NESTED_PROJECT'})
                    continue
                if d != root:
                    if len(rel.split('/')) > MAX_WALK_DEPTH:
                        prov['excludedUnits'].append({'path': d, 'reason': 'DEPTH'})
                        continue
                    bad = _unit_custody(rel)
                    if bad is not None:
                        prov['excludedUnits'].append({'path': bad[0], 'reason': 'DIRECTORY_CUSTODY:' + bad[1]})
                        continue
                markers, bad_markers = _markers(d)
                for b in bad_markers:
                    prov['excludedUnits'].append({'path': d, 'reason': 'MARKER_CUSTODY:' + b})
                if not markers:
                    continue
                prov['units'].append({'path': d, 'kind': 'workspace-auto', 'markers': markers})
            # Count admitted project units after authority/custody exclusions.
            unit_count = len(prov['units'])
            if unit_count > DD.MAX_WORKSPACE_UNITS:
                prov['units'] = []
                return refuse('PROJECT.WORKSPACE_UNIT_LIMIT', root,
                              'WORKSPACE_UNIT_LIMIT:%d>%d' % (unit_count, DD.MAX_WORKSPACE_UNITS))
        return {'status': 'ACCEPT', 'provenance': prov}

    if waive and explicit is None:
        return refuse('PROJECT.EXPLICIT_PATH_INVALID', None, 'trustProjectOwner requires an explicit --project path')

    if explicit is not None:
        prov['mode'] = 'explicit'
        target = inp.get('explicitResolved', explicit)   # realpath result supplied by the harness
        prov['explicitPathWasSymlink'] = (target != explicit)
        entry = fs.get(target)
        why = _dir_custody(entry, uid, waive, groups)
        if why is not None:
            if why == 'ABSENT' or why == 'NOT_A_DIRECTORY':
                return refuse('PROJECT.EXPLICIT_PATH_INVALID', target, why)
            return refuse('PROJECT.ROOT_CUSTODY_REFUSED', target, why)
        rec = {'path': target, 'custody': 'PASS', 'candidate': 'ABSENT', 'boundary': 'EXPLICIT'}
        prov['walked'].append(rec)
        cfg, fwhy = examine_config(target, rec)
        if fwhy is not None:
            return refuse('CONFIG.CUSTODY_REFUSED', cfg, fwhy)
        prov['configPath'] = cfg
        prov['vcs'] = _vcs_info(entry)
        prov['stopReason'] = 'EXPLICIT'
        return finish(target)

    prov['mode'] = 'walk'
    cwd = inp['cwd']
    cur = cwd
    depth = 0
    while True:
        depth += 1
        if depth > MAX_WALK_DEPTH:
            return refuse('PROJECT.ROOT_CUSTODY_REFUSED', cur, 'WALK_DEPTH_EXCEEDED')
        entry = fs.get(cur)
        why = _dir_custody(entry, uid, False, groups)
        if why is not None:
            if cur == cwd:
                return refuse('PROJECT.ROOT_CUSTODY_REFUSED', cur, why)
            prov['walked'].append({'path': cur, 'custody': why, 'candidate': 'NOT_EXAMINED', 'boundary': why})
            prov['stopReason'] = 'CUSTODY:' + why
            break
        rec = {'path': cur, 'custody': 'PASS', 'candidate': 'ABSENT', 'boundary': None}
        prov['walked'].append(rec)
        cfg, fwhy = examine_config(cur, rec)
        if fwhy is not None:
            return refuse('CONFIG.CUSTODY_REFUSED', cfg, fwhy)
        if cfg is not None:
            prov['configPath'] = cfg
            prov['stopReason'] = 'CANDIDATE'
            prov['vcs'] = _vcs_info(entry)
            prov['mode'] = 'config'
            return finish(cur)
        # boundaries after examining this directory, in fixed precedence
        vcs = _vcs_info(entry)
        if vcs is not None:
            rec['boundary'] = 'VCS'
            prov['stopReason'] = 'VCS'
            prov['vcs'] = vcs
            prov['mode'] = 'vcs-default'   # the repository root is the project, not the launch directory
            return finish(cur)
        if cur == home:
            rec['boundary'] = 'HOME'
            prov['stopReason'] = 'HOME'
            break
        if cur == '/':
            rec['boundary'] = 'FS_ROOT'
            prov['stopReason'] = 'FS_ROOT'
            break
        par = _parent(cur)
        pentry = fs.get(par)
        if pentry is not None and pentry.get('kind') == 'dir' and pentry.get('dev') != entry.get('dev'):
            rec['boundary'] = 'MOUNT'
            prov['stopReason'] = 'MOUNT'
            break
        cur = par
    prov['mode'] = 'cwd-default'
    return finish(cwd)


BOUNDARY_INVENTORY_TCB = ['the inventory is derived only from an ACCEPTed DiscoveryProvenanceV1 of this instrument over the same '
                          'marker inventory the native unit instrument receives; a caller-authored ignore list is not an inventory']


def boundary_inventory(result):
    """S3 export for the native language-unit instrument (post-reset review v2, P3). Converts an ACCEPTed discovery
    result's absolute custody locators (`nestedRepositories`, `nestedProjects`, custody/depth `excludedUnits`,
    `prunedTrees`) into the closed `AdmittedBoundaryInventoryV1` of relative scope paths under the selected root, via
    the shared `DD.boundary_inventory_from_provenance`. A REFUSE result exports nothing (Reject): an operational host
    composition passes this record, unchanged, to native `discover_units(markers, explicit_roots, boundaries)`,
    `assign_membership(..., boundaries)` and `unit_scope_descriptor(..., boundaries)`; the native instrument never
    re-derives a boundary from caller input."""
    if not isinstance(result, dict) or result.get('status') != 'ACCEPT':
        raise Reject('BOUNDARY_INVENTORY_REQUIRES_ACCEPT')
    try:
        return DD.boundary_inventory_from_provenance(result['provenance'])
    except DD.BoundaryError as e:
        raise Reject('BOUNDARY_INVENTORY:' + str(e))


# =============================================================================================
# S4 - Evaluation clock: refuse unattested excursion before evaluation and before any write (AR-04)
# =============================================================================================
CLOCK_TCB = ['payload times are issue times of signature-verified documents (asserted)',
             'observation.wall/mono/bootId are OS reads (asserted); mono is sleep-inclusive by qualification']
EXPIRY_FIELDS = ('revocationIssuedAt', 'catalogExpiresAt', 'rootExpiresAt')


def _clock_out(report_only, wall_s):
    return {'schemaVersion': 1, 'evaluationMode': 'report-only' if report_only else 'decision',
            'rawWallClock': wall_s, 'decision': None, 'refusal': None, 'refusalKind': None, 'evaluationTime': None,
            'floorWrite': None, 'floorAdvance': None, 'anchorWrite': None, 'lastAcceptedWrite': None,
            'writes': [], 'admittedTimeReference': None, 'plausibilityLimit': None, 'witness': None,
            'continuity': {'available': False}, 'findings': [], 'states': None, 'trustFreshness': None,
            'd9': None, 'remedy': None, 'tcbAssumptions': list(CLOCK_TCB)}


def clock_decision(record, observation, payload=None, report_only=False):
    """One decision evaluation (or a report-only evaluation when report_only=True).

    record (SC-TRUST clock fields; fresh install when evalHighWater is None):
      evalHighWater: ISO|None, lastAccepted: ISO|None (required whenever evalHighWater is set),
      anchor: None|{bootId, mono, wall}, revocationIssuedAt, catalogExpiresAt, rootExpiresAt: ISO|None
    observation: {wall: ISO, mono: int seconds (sleep-inclusive monotonic), bootId: str}
    payload: None | {newestIssuedAt: ISO, presentedRootIssuedAt: ISO|None, [expiry fields of the presented docs]}

    Rule (contract S4):
      admittedTime A = max(lastAccepted, accepted witness time, presented root issue time)
      the wall is plausible iff wall <= A + 90 d; an implausible wall is REFUSED before any evaluation and
      before any write (no floor, anchor or lastAccepted change). A plausible wall evaluates at
      tEval = max(evalHighWater, wall, A) and the floor written is exactly tEval (write-ahead), so the
      persisted floor and the evaluated instant never differ and evaluated time never goes backwards.
      Nothing ever lowers evalHighWater except recovery_apply (S4.5).
    """
    wall = ts(observation['wall'])
    mono = observation['mono']
    boot = observation['bootId']
    if not _int(mono) or mono < 0:
        raise Reject('MONOTONIC_MALFORMED')
    floor = ts(record.get('evalHighWater'))
    last = ts(record.get('lastAccepted'))
    if floor is not None and last is None:
        raise Reject('RECORD_LAST_ACCEPTED_REQUIRED')
    anchor = record.get('anchor')
    out = _clock_out(report_only, observation['wall'])
    findings = out['findings']

    def refuse(code, kind, remedy):
        out['decision'] = 'REFUSE'
        out['refusal'] = code
        out['refusalKind'] = kind
        out['remedy'] = remedy
        out['d9'] = d9(code)
        out['floorAdvance'] = 'WITHHELD'
        out['writes'] = []
        return out

    def finish_writes(t_eval, floor_write, advance, anchor_write, last_write):
        if report_only:
            out['floorAdvance'] = 'NOT-APPLICABLE'
            out['writes'] = []
            return
        out['floorWrite'] = iso(floor_write)
        out['floorAdvance'] = advance
        out['writes'].append('evalHighWater')
        if anchor_write is not None:
            out['anchorWrite'] = anchor_write
            out['writes'].append('anchor')
        if last_write is not None:
            out['lastAcceptedWrite'] = iso(last_write)
            out['writes'].append('lastAccepted')

    # --- witness (payload): admitted time evidence -------------------------------------------------
    witness_time = None
    root_time = None
    if payload is not None:
        wt = ts(payload['newestIssuedAt'])
        if wt > wall + FUTURE_TOLERANCE_S:
            # existing OD-112-2 future-time rule (FC-FUTURE): the payload refuses, state unchanged
            out['witness'] = {'newestIssuedAt': payload['newestIssuedAt'], 'accepted': False, 'reason': 'issued-in-future'}
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'payload-future',
                          'presented document is issued more than 24 h after the wall clock (FC-FUTURE); state unchanged')
        if last is not None and wt < last:
            out['witness'] = {'newestIssuedAt': payload['newestIssuedAt'], 'accepted': False, 'reason': 'older-than-lastAccepted'}
        else:
            witness_time = wt
            out['witness'] = {'newestIssuedAt': payload['newestIssuedAt'], 'accepted': True, 'reason': None}
        if payload.get('presentedRootIssuedAt'):
            root_time = ts(payload['presentedRootIssuedAt'])
            if root_time > wall + FUTURE_TOLERANCE_S:
                return refuse('PAYLOAD-NOT-ADMISSIBLE', 'payload-future', 'presented root is issued more than 24 h after the wall clock; state unchanged')

    cands = [x for x in (last, witness_time, root_time) if x is not None]
    admitted = max(cands) if cands else None

    # --- fresh install: no floor, no admitted time context without a payload ------------------------
    if floor is None:
        if admitted is None:
            return refuse('TRUST.NO_ADMITTED_TIME_CONTEXT', 'fresh-no-context',
                          'first trust evaluation needs the embedded bootstrap payload or an ordinary payload; nothing is written')
        out['admittedTimeReference'] = iso(admitted)
        out['plausibilityLimit'] = iso(admitted + UNATTESTED_FORWARD_HORIZON_S)
        if wall > admitted + UNATTESTED_FORWARD_HORIZON_S:
            findings.append({'check': 'clock', 'status': 'CLOCK-EXCURSION-FORWARD', 'kind': 'fresh-beyond-horizon', 'wouldRefuse': True})
            return refuse('CLOCK-EXCURSION-FORWARD', 'fresh-beyond-horizon',
                          'wall clock is more than 90 d beyond the newest signed time; correct the clock or present a newer payload; no floor is initialised')
        t_eval = max(wall, admitted)
        out['decision'] = 'PROCEED'
        out['evaluationTime'] = iso(t_eval)
        finish_writes(t_eval, t_eval, 'INIT', {'bootId': boot, 'mono': mono, 'wall': observation['wall']}, admitted)
        _states(out, record, payload, t_eval)
        return out

    # --- ordinary evaluation --------------------------------------------------------------------------
    out['admittedTimeReference'] = iso(admitted)
    out['plausibilityLimit'] = iso(admitted + UNATTESTED_FORWARD_HORIZON_S)

    # in-boot continuity check (sleep-inclusive monotonic elapsed vs wall)
    continuity = {'available': False}
    excused = False
    if anchor is not None and anchor.get('bootId') == boot:
        if not _int(anchor.get('mono')) or mono < anchor['mono']:
            findings.append({'check': 'clockContinuity', 'status': 'CLOCK-CONTINUITY-MALFORMED', 'wouldRefuse': False})
        else:
            expected = ts(anchor['wall']) + (mono - anchor['mono'])
            dev = wall - expected
            continuity = {'available': True, 'expectedWall': iso(expected), 'deviationSeconds': dev}
            if dev > SESSION_DEVIATION_TOLERANCE_S:
                # a witness excuses the deviation only if it proves the expectation itself was behind
                excused = witness_time is not None and witness_time >= expected
                if not excused:
                    findings.append({'check': 'clockContinuity', 'status': 'CLOCK-EXCURSION-FORWARD', 'kind': 'in-session', 'wouldRefuse': True})
                    out['continuity'] = continuity
                    return refuse('CLOCK-EXCURSION-FORWARD', 'in-session',
                                  'wall clock advanced more than 24 h beyond monotonic elapsed time in this boot session: correct the clock or present a payload issued after the expected time')
            if dev < -SESSION_DEVIATION_TOLERANCE_S:
                findings.append({'check': 'clockContinuity', 'status': 'CLOCK-REGRESSION-IN-SESSION', 'wouldRefuse': False})
    out['continuity'] = continuity

    # plausibility against admitted time evidence: refuse BEFORE evaluation and before any write
    if wall > admitted + UNATTESTED_FORWARD_HORIZON_S:
        findings.append({'check': 'clock', 'status': 'CLOCK-EXCURSION-FORWARD', 'kind': 'beyond-horizon', 'wouldRefuse': True})
        return refuse('CLOCK-EXCURSION-FORWARD', 'beyond-horizon',
                      'wall clock is more than 90 d beyond the newest signed time: correct the clock or present a payload issued within 90 d of the wall; no floor is written')

    if wall < floor:
        findings.append({'check': 'clock', 'status': 'CLOCK-REGRESSION', 'wouldRefuse': False})
    if floor > wall + UNATTESTED_FORWARD_HORIZON_S:
        findings.append({'check': 'clock', 'status': 'TRUST.FLOOR_AHEAD_OF_WALL', 'wouldRefuse': False,
                         'remedy': 'recorded evalHighWater is more than 90 d ahead of the wall; ordinary payloads cannot lower it; obtain a signed recovery epoch (S4.5)'})

    t_eval = max(floor, wall, admitted)
    out['decision'] = 'PROCEED'
    out['evaluationTime'] = iso(t_eval)
    anchor_write = None
    if not continuity.get('available') or abs(continuity['deviationSeconds']) <= SESSION_DEVIATION_TOLERANCE_S or excused:
        anchor_write = {'bootId': boot, 'mono': mono, 'wall': observation['wall']}
    last_write = admitted if admitted > last else None
    finish_writes(t_eval, t_eval, 'ADVANCE' if t_eval > floor else 'NONE', anchor_write, last_write)
    _states(out, record, payload, t_eval)
    return out


def _states(out, record, payload, t_eval):
    eff = {k: (payload or {}).get(k, record.get(k)) for k in EXPIRY_FIELDS}
    root_exp = ts(eff['rootExpiresAt'])
    cat_exp = ts(eff['catalogExpiresAt'])
    rev_iss = ts(eff['revocationIssuedAt'])
    out['states'] = {
        'rootExpired': (root_exp is None) or t_eval >= root_exp,
        'catalogExpired': (cat_exp is None) or t_eval >= cat_exp,
        'revocationStale': (rev_iss is None) or t_eval > rev_iss + REVOCATION_FRESH_DAYS * DAY,
    }
    if rev_iss is not None:
        remaining = (rev_iss + REVOCATION_FRESH_DAYS * DAY) - t_eval
        out['trustFreshness'] = {'daysRemaining': remaining // DAY if remaining > 0 else 0,
                                 'warning': 0 < remaining <= TRUST_WARNING_WINDOW_DAYS * DAY}


# --- S4.5 signed recovery epoch for an already-poisoned floor -------------------------------------
RECOVERY_BOUND_FIELDS = ('evalHighWater', 'lastAccepted', 'rootVersion', 'revocationVersion', 'indexSnapshotVersion', 'recoveryEpochSerial')
RECOVERY_TCB = ['`signers` are key ids whose envelope signature verify_envelope already accepted (asserted)',
                '`nonce` is 32 host-CSPRNG bytes supplied by the harness (asserted)']


def _record_digest(record):
    body = {k: record.get(k) for k in RECOVERY_BOUND_FIELDS}
    return metadata_sha('opensip.metadata.recovery-challenge.1', body)


def _observation(obs):
    """Strict observation shape {wall, mono, bootId}: mono is a non-negative i64 (never a bool), bootId a
    non-empty string, wall the schema timestamp grammar."""
    if not isinstance(obs, dict) or set(obs) != {'wall', 'mono', 'bootId'}:
        raise Reject('OBSERVATION_SHAPE')
    if not (_int(obs['mono']) and 0 <= obs['mono'] <= 2**63 - 1) or not isinstance(obs['bootId'], str) or not (1 <= len(obs['bootId']) <= 256):
        raise Reject('OBSERVATION_SHAPE')
    return ts(obs['wall']), obs['mono'], obs['bootId']


def recovery_challenge(record, nonce, observation, report_only=False):
    """`opensip trust recovery-challenge` exports TrustRecoveryChallengeV1 and persists it as the one
    pending challenge (replacing any earlier pending challenge). The pending challenge is bound to the
    current boot and to a sleep-inclusive monotonic expiry window (24 h): a response can only be imported
    in the same boot, before the window closes. Doctor (report-only) cannot create one."""
    if not isinstance(nonce, str) or not HEX64.match(nonce):
        raise Reject('NONCE_GRAMMAR')
    wall, mono, boot = _observation(observation)
    if report_only:
        return {'result': 'REFUSE', 'refusal': 'RECOVERY.REFUSED', 'detail': 'REPORT_ONLY_CANNOT_CHALLENGE', 'd9': d9('RECOVERY.REFUSED'),
                'challenge': None, 'pendingWrite': None, 'tcbAssumptions': list(RECOVERY_TCB)}
    ch = {'challengeSchema': 1, 'kind': 'trust-recovery-challenge', 'nonce': nonce,
          'recordDigest': _record_digest(record), 'createdWall': iso(wall),
          'boundRecord': {k: record.get(k) for k in RECOVERY_BOUND_FIELDS}}
    pending = {'nonce': nonce, 'recordDigest': ch['recordDigest'], 'bootId': boot, 'createdMono': mono,
               'expiresMono': mono + RECOVERY_CHALLENGE_TTL_S, 'createdWall': iso(wall)}
    return {'result': 'ISSUED', 'refusal': None, 'detail': None, 'd9': None, 'challenge': ch,
            'pendingWrite': pending, 'tcbAssumptions': list(RECOVERY_TCB)}


EPOCH_KEYS = {'recoverySchema', 'kind', 'epochSerial', 'issuedAt', 'challenge', 'counters', 'installBinding'}
COUNTER_KEYS = ('rootVersion', 'revocationVersion', 'indexSnapshotVersion')
PENDING_KEYS = {'nonce', 'recordDigest', 'bootId', 'createdMono', 'expiresMono', 'createdWall'}


def _epoch_shape(epoch):
    """Strict closed shape of TrustRecoveryEpochV1 BEFORE any comparison with the record. Integers are
    exact (a bool is never an integer; 1 is never true); constants are compared by type and value."""
    if not isinstance(epoch, dict) or set(epoch) != EPOCH_KEYS:
        return 'SHAPE'
    if not (_int(epoch['recoverySchema']) and epoch['recoverySchema'] == 1):
        return 'SHAPE:recoverySchema'
    if not (isinstance(epoch['kind'], str) and epoch['kind'] == 'trust-recovery-epoch'):
        return 'SHAPE:kind'
    if not (_int(epoch['epochSerial']) and 1 <= epoch['epochSerial'] <= 2**63 - 1):
        return 'SHAPE:epochSerial'
    if not isinstance(epoch['issuedAt'], str) or not TS_RE.fullmatch(epoch['issuedAt']):
        return 'SHAPE:issuedAt'
    ch = epoch['challenge']
    if not isinstance(ch, dict) or set(ch) != {'nonce', 'recordDigest'} or \
            not all(isinstance(ch[k], str) and HEX64.match(ch[k]) for k in ('nonce', 'recordDigest')):
        return 'SHAPE:challenge'
    ctr = epoch['counters']
    if not isinstance(ctr, dict) or set(ctr) != set(COUNTER_KEYS) or \
            not all(_int(ctr[k]) and 1 <= ctr[k] <= 2**63 - 1 for k in COUNTER_KEYS):
        return 'SHAPE:counters'
    if not (isinstance(epoch['installBinding'], str) and epoch['installBinding'] == 'challenge'):
        return 'SHAPE:installBinding'
    return None


def _pending_shape(pending):
    if not isinstance(pending, dict) or set(pending) != PENDING_KEYS:
        return 'PENDING_SHAPE'
    if not all(isinstance(pending[k], str) and HEX64.match(pending[k]) for k in ('nonce', 'recordDigest')):
        return 'PENDING_SHAPE'
    if not isinstance(pending['bootId'], str) or not pending['bootId']:
        return 'PENDING_SHAPE'
    if not all(_int(pending[k]) and 0 <= pending[k] <= 2**63 - 1 for k in ('createdMono', 'expiresMono')) or pending['expiresMono'] < pending['createdMono']:
        return 'PENDING_SHAPE'
    if not isinstance(pending['createdWall'], str) or not TS_RE.fullmatch(pending['createdWall']):
        return 'PENDING_SHAPE'
    return None


def recovery_apply(record, epoch, signers, observation, accepted_root, revoked_keys=()):
    """`opensip trust recovery-import` applies TrustRecoveryEpochV1.

    Authority: the accepted root's `recoveryAuthority.keys` at `recoveryAuthority.threshold` (the existing
    root schema-1 field, disjoint from rootKeys), revoked keys excluded; the accepted root's expiry is NOT
    consulted here (the poisoned floor is what is being repaired; anti-rollback counters, not time, protect
    the root). Root keys do not count: recovery never exercises root keys and root-key compromise alone
    cannot lower a floor.

    Counters: the epoch's counters must EQUAL the challenged record's counters (design selection: exact
    equality, the simplest rule). A higher signed counter is refused with a typed detail and the remedy is
    to import the ordinary payload carrying it first and then re-challenge; nothing is silently discarded
    and nothing is silently advanced.

    Freshness: the pending challenge is single-boot (bootId equal) and single-window (createdMono <= mono
    <= expiresMono, sleep-inclusive monotonic); `issuedAt` must lie within +/- 24 h of the wall at import
    and never before lastAccepted. A response to an old challenge cannot be imported after a reboot or after
    the window, so no indefinitely pending response can later lower the floor to stale real time.

    Threat statement: the wall is untrusted. The freshness rule bounds how far a signed epoch can move the
    floor relative to the wall; it does not prove the wall. A recovery authority that signs a false time is a
    malicious publisher and is outside this protocol's promise; the protocol promises install binding,
    single use, counter preservation and no floor below lastAccepted, not detection of a lying signer.

    Effect on success: evalHighWater := lastAccepted := epoch.issuedAt; anchor cleared;
    recoveryEpochSerial := epoch.epochSerial; pending challenge consumed. Counters, revocation entries,
    role states, journals and namespaces are untouched. Refusals leave the record unchanged."""
    out = {'result': None, 'refusal': None, 'detail': None, 'd9': None, 'writes': None,
           'floorLowered': None, 'countersUnchanged': True, 'revocationEntriesUnchanged': True,
           'revivesRevokedTrust': False, 'custody': 'SC-TRUST under the global lifecycle fence; no project lease; no namespace deletion',
           'tcbAssumptions': list(RECOVERY_TCB)}

    def refuse(detail):
        out['result'] = 'REFUSE'
        out['refusal'] = 'RECOVERY.REFUSED'
        out['detail'] = detail
        out['d9'] = d9('RECOVERY.REFUSED')
        out['writes'] = []
        out['floorLowered'] = False
        return out

    # 1. strict shapes first: epoch, observation, pending challenge (before any comparison)
    why = _epoch_shape(epoch)
    if why is not None:
        return refuse(why)
    wall, mono, boot = _observation(observation)
    issued = ts(epoch['issuedAt'])
    ch = epoch['challenge']
    ctr = epoch['counters']
    # 2. authority: recovery authority quorum of the accepted root, revoked keys excluded
    ra = accepted_root.get('recoveryAuthority') or {}
    ok = (set(signers) & set(ra.get('keys', ()))) - set(revoked_keys)
    if not _int(ra.get('threshold')) or ra['threshold'] < 3 or len(ok) < ra['threshold']:
        return refuse('SIGNATURE_THRESHOLD')
    # 3. a fresh pending challenge of this boot and window
    pending = record.get('pendingRecoveryChallenge')
    if pending is None:
        return refuse('NO_PENDING_CHALLENGE')
    why = _pending_shape(pending)
    if why is not None:
        return refuse(why)
    if pending['bootId'] != boot:
        return refuse('CHALLENGE_BOOT_CHANGED')
    if mono < pending['createdMono']:
        return refuse('CHALLENGE_CONTINUITY_MALFORMED')
    if mono > pending['expiresMono']:
        return refuse('CHALLENGE_EXPIRED')
    # 4. install and record binding
    if ch['nonce'] != pending['nonce']:
        return refuse('CHALLENGE_MISMATCH')
    if ch['recordDigest'] != pending['recordDigest'] or ch['recordDigest'] != _record_digest(record):
        return refuse('RECORD_CHANGED_SINCE_CHALLENGE')
    if epoch['epochSerial'] <= (record.get('recoveryEpochSerial') or 0):
        return refuse('SERIAL_NOT_ADVANCING')
    for k in COUNTER_KEYS:
        if not _int(record.get(k)) or ctr[k] != record[k]:
            return refuse('COUNTER_MISMATCH:' + k)
    # 5. signed time bounds
    last = ts(record.get('lastAccepted'))
    if last is not None and issued < last:
        return refuse('TIME_BEFORE_LAST_ACCEPTED')
    if issued > wall + RECOVERY_ISSUE_SKEW_S:
        return refuse('ISSUED_IN_FUTURE')
    if issued < wall - RECOVERY_ISSUE_SKEW_S:
        return refuse('ISSUED_TOO_OLD_FOR_WALL')
    floor = ts(record.get('evalHighWater'))
    out['result'] = 'APPLIED'
    out['writes'] = {'evalHighWater': iso(issued), 'lastAccepted': iso(issued), 'anchor': None,
                     'recoveryEpochSerial': epoch['epochSerial'], 'pendingRecoveryChallenge': None,
                     'audit': {'recordType': 'RECOVERY-EPOCH', 'epochSerial': epoch['epochSerial'], 'previousEvalHighWater': record.get('evalHighWater')}}
    out['floorLowered'] = floor is not None and issued < floor
    out['revivesRevokedTrust'] = False   # counters and entries unchanged; expiry is re-evaluated at signed real time only
    return out


# =============================================================================================
# S5 - Root chain verification through expired roots (AR-05)
# =============================================================================================
def _admit_root_semantic(root, reader_schemas):
    """Reduced semantic admission (the complete v8 rule set stands; this model checks the members
    that the chain rule depends on plus the schema-dependent TR-REPAIR / kernelAttestationKeys rule)."""
    r = []
    schema = root.get('rootSchema')
    if not _int(schema) or schema not in reader_schemas:
        return ['ROOT.SCHEMA_UNSUPPORTED']
    rk = root.get('rootKeys', [])
    if len(set(rk)) != len(rk) or len(rk) < 3 or not (2 <= root.get('rootThreshold', 0) <= len(rk)):
        r.append('ROOT.ROOT_THRESHOLD_POLICY')
    rv, pv = root.get('rootVersion'), root.get('previousRootVersion')
    if not (_int(rv) and 1 <= rv <= 2**63 - 1):
        r.append('ROOT.VERSION_RANGE')
    if (rv == 1) != (pv is None):
        r.append('ROOT.CHAIN_ORIGIN_INCONSISTENT')
    try:
        if not (ts(root.get('issuedAt')) < ts(root.get('expiresAt'))):
            r.append('ROOT.EXPIRY_NOT_AFTER_ISSUE')
    except Reject:
        r.append('ROOT.TIMESTAMP_GRAMMAR')
    rep = (root.get('roles') or {}).get('TR-REPAIR', {})
    kak = root.get('kernelAttestationKeys', None)
    if schema == 1:
        if not (rep.get('standing') == 'typed-absence-DR-110' and rep.get('keys') == [] and rep.get('threshold') == 0):
            r.append('ROOT.TR_REPAIR_MUST_BE_TYPED_ABSENCE')
        if kak != []:
            r.append('ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY')
    else:  # schema 2: active TR-REPAIR and kernelAttestationKeys are admissible under the stated key policy
        if rep.get('standing') == 'active':
            ks = rep.get('keys', [])
            if not (rep.get('threshold', 0) >= 2 and len(ks) >= rep.get('threshold', 0) + 1 and rep.get('namespaces')):
                r.append('ROOT.ROLE_THRESHOLD_POLICY:TR-REPAIR')
            if set(ks) & set(rk):
                r.append('ROOT.KEY_REUSED_ACROSS_ROLES:TR-REPAIR')
        elif not (rep.get('standing') == 'typed-absence-DR-110' and rep.get('keys') == [] and rep.get('threshold') == 0):
            r.append('ROOT.TR_REPAIR_STANDING')
        if not isinstance(kak, list) or len(set(kak)) != len(kak) or len(kak) > 8 or any(not HEX64.match(k) for k in kak):
            r.append('ROOT.KERNEL_ATTESTATION_KEYS_POLICY')
        elif set(kak) & set(rk):
            r.append('ROOT.KEY_REUSED_ACROSS_ROLES:kernelAttestation')
    return r


ROOT_TCB = ['`signers` are key ids whose envelope signature verify_envelope already accepted (asserted)']


def verify_root_chain(state, chain, t_eval, wall, revoked_keys=(), reader_schemas=(1,)):
    """ROOT-CHAIN-V1. state = {acceptedVersion, acceptedRoot}. chain = [{root, signers}] for
    versions N+1..M in order. Every link needs BOTH the previous root's threshold (continuity) and the
    new root's threshold (possession). Intermediate root expiry is never consulted; the final root must
    be unexpired at t_eval and not issued in the future. Refusals leave state unchanged."""
    t_eval = ts(t_eval)
    wall = ts(wall)
    revoked = set(revoked_keys)
    prev = state['acceptedRoot']
    n = state['acceptedVersion']
    base = {'result': None, 'refusal': None, 'acceptedVersion': n, 'links': [], 'stateUnchanged': True,
            'lastAcceptedIssuedAt': None, 'antiRollback': None, 'remedy': None, 'tcbAssumptions': list(ROOT_TCB)}
    if prev.get('rootVersion') != n:
        return dict(base, result='REFUSE', refusal='ROOT.STATE_INCONSISTENT')
    links = base['links']
    if not chain:
        if t_eval >= ts(prev['expiresAt']):
            return dict(base, result='REFUSE', refusal='ROOT.EXPIRED_NO_CHAIN',
                        remedy='present an ordinary payload carrying every root version from %d+1 to the newest' % n)
        return dict(base, result='ACCEPT', lastAcceptedIssuedAt=prev['issuedAt'], antiRollback='counters unchanged at %d' % n)
    for link in chain:
        root = link['root']
        signers = set(link.get('signers', []))
        rec = {'from': prev.get('rootVersion'), 'to': root.get('rootVersion'), 'prevExpiryConsulted': False,
               'oldThresholdMet': None, 'newThresholdMet': None, 'refusal': None}
        links.append(rec)
        sem = _admit_root_semantic(root, set(reader_schemas))
        if sem:
            rec['refusal'] = sem[0]
            return dict(base, result='REFUSE', refusal=sem[0])
        if root.get('previousRootVersion') != prev['rootVersion'] or root['rootVersion'] != prev['rootVersion'] + 1:
            rec['refusal'] = 'ROOT.CHAIN_GAP'
            return dict(base, result='REFUSE', refusal='ROOT.CHAIN_GAP')
        if ts(root['issuedAt']) < ts(prev['issuedAt']):
            rec['refusal'] = 'ROOT.CHAIN_BACKDATED'
            return dict(base, result='REFUSE', refusal='ROOT.CHAIN_BACKDATED')
        old_ok = len((signers & set(prev['rootKeys'])) - revoked)
        new_ok = len((signers & set(root['rootKeys'])) - revoked)
        rec['oldThresholdMet'] = old_ok >= prev['rootThreshold']
        rec['newThresholdMet'] = new_ok >= root['rootThreshold']
        if not rec['oldThresholdMet']:
            rec['refusal'] = 'ROOT.CHAIN_OLD_THRESHOLD'
            return dict(base, result='REFUSE', refusal='ROOT.CHAIN_OLD_THRESHOLD')
        if not rec['newThresholdMet']:
            rec['refusal'] = 'ROOT.CHAIN_NEW_THRESHOLD'
            return dict(base, result='REFUSE', refusal='ROOT.CHAIN_NEW_THRESHOLD')
        prev = root
    final = prev
    if t_eval >= ts(final['expiresAt']):
        return dict(base, result='REFUSE', refusal='ROOT.FINAL_EXPIRED',
                    remedy='the newest presented root is itself expired at the evaluation instant; obtain a newer chain')
    if ts(final['issuedAt']) > wall + FUTURE_TOLERANCE_S:
        return dict(base, result='REFUSE', refusal='ROOT.FINAL_FUTURE')
    return dict(base, result='ACCEPT', acceptedVersion=final['rootVersion'], stateUnchanged=False,
                lastAcceptedIssuedAt=final['issuedAt'], antiRollback='counters advance to %d' % final['rootVersion'])


# =============================================================================================
# S6 - Live trust revocation: observation, fail-stop observer and journal linearization (AR-05)
# =============================================================================================
def revocation_observe(epoch_at_start, current_epoch, closure, revocation_entries, effective_policy_grants=None, required_grants=None):
    """Pure predicate run by the operation's own host at every authority checkpoint (each effectRequest
    before its journal append) and at every observer tick. Returns {'action', 'reason', 'matches'}."""
    if current_epoch['revocationVersion'] < epoch_at_start['revocationVersion']:
        return {'action': 'CONTINUE', 'reason': 'counter-below-start (rollback is detected elsewhere; never revoke on a lower counter)', 'matches': []}
    matches = []
    if current_epoch['revocationVersion'] > epoch_at_start['revocationVersion']:
        for e in revocation_entries:
            k, s = e['subjectKind'], e['subject']
            if k == 'release' and s in closure.get('releases', []):
                matches.append(e)
            elif k == 'keyId' and s in closure.get('signingKeyIds', []):
                matches.append(e)
            elif k == 'namespace' and s in closure.get('namespaces', []):
                matches.append(e)
            elif k == 'catalogSnapshot' and s == str(closure.get('catalogSnapshotVersion')):
                matches.append(e)
        if matches:
            return {'action': 'REVOKE', 'reason': 'trust-revoked', 'matches': matches}
    if current_epoch['permissionPolicyDigest'] != epoch_at_start['permissionPolicyDigest'] and required_grants is not None:
        allowed = set((g['stableId'], g['token']) for g in (effective_policy_grants or []))
        lost = [g for g in required_grants if (g['stableId'], g['token']) not in allowed]
        if lost:
            return {'action': 'REVOKE', 'reason': 'policy', 'matches': lost}
    drift = []
    if current_epoch['revocationVersion'] != epoch_at_start['revocationVersion']:
        drift.append('revocation-unrelated')
    if current_epoch['permissionPolicyDigest'] != epoch_at_start['permissionPolicyDigest']:
        drift.append('policy-unrelated')
    return {'action': 'CONTINUE', 'reason': ','.join(drift) if drift else 'no-change', 'matches': []}


OBSERVER_OBLIGATION = {
    'standing': 'implementation qualification obligation under OS scheduling assumptions; not a wall-clock guarantee in a stopped process',
    'monotonicTimer': {'linux': 'CLOCK_BOOTTIME', 'macos': 'mach_continuous_time'},
    'pollIntervalSeconds': REVOCATION_POLL_INTERVAL_S,
    'stallBoundSeconds': REVOCATION_OBSERVATION_BOUND_S,
    'authorityCheckpoint': 'every effectRequest re-reads trustEpoch under the journal append lock before its intent/commit record',
    'failStop': 'a tick that finds the last successful counter read older than the stall bound, or that cannot read the counter, appends REV(observer-fail-stop) and cancels',
    'stoppedProcess': 'a SIGSTOPped or descheduled host emits no effects while stopped; on resume the first checkpoint or tick observes the stall and fail-stops before any further effect',
}


def observer_tick(last_read_mono, now_mono, counter_read_ok):
    """Fail-stop observer. All times are sleep-inclusive monotonic seconds (asserted OS reads)."""
    if not (_int(last_read_mono) and _int(now_mono)) or now_mono < last_read_mono:
        raise Reject('MONOTONIC_MALFORMED')
    if not counter_read_ok:
        return {'action': 'REV', 'reason': 'observer-fail-stop', 'detail': 'counter-unreadable', 'd9': d9('OBSERVER.FAIL_STOP'), 'obligation': OBSERVER_OBLIGATION}
    if now_mono - last_read_mono > REVOCATION_OBSERVATION_BOUND_S:
        return {'action': 'REV', 'reason': 'observer-fail-stop', 'detail': 'stalled:%ds' % (now_mono - last_read_mono), 'd9': d9('OBSERVER.FAIL_STOP'), 'obligation': OBSERVER_OBLIGATION}
    return {'action': 'CONTINUE', 'reason': 'within-bound', 'detail': None, 'd9': None, 'obligation': OBSERVER_OBLIGATION}


CURRENT_JOURNAL_RECORD_SCHEMA = 3
HISTORICAL_JOURNAL_RECORD_SCHEMA = 2
# Linearization fixture only. Not a native fact, not evaluator authority, not a close_run identity.
FIXTURE_SEAL_RUN_ID = 'run3:' + '0' * 64
_RUN3 = re.compile(r'^run3:[0-9a-f]{64}$')
_RUN2 = re.compile(r'^run2:[0-9a-f]{64}$')


def _validate_current_journal_record(rec):
    """Exact current JournalRecord fields (recordSchema 3). Not a mixed run[23] parser."""
    schema = copy.deepcopy(_SCHEMA_BUNDLE)
    schema['$ref'] = '#/$defs/JournalRecord'
    _C.validate(schema, rec)


def admit_journal_record(rec):
    """Current selected journal record is recordSchema 3 and the closed JournalRecord fields.
    Schema-2 journals are frozen historical bytes and are not read as 3. Mixed run2/run3
    prefixes refuse. Grant/root schema-2 documents are a different version axis."""
    if type(rec) is not dict:
        raise Reject('JOURNAL_RECORD_SHAPE')
    schema = rec.get('recordSchema')
    run_id = rec.get('runId')
    if schema == CURRENT_JOURNAL_RECORD_SCHEMA:
        if type(run_id) is str and (run_id.startswith('run2:') or _RUN2.match(run_id)):
            raise Reject('JOURNAL_RECORD_MIXED_PREFIX')
        try:
            _validate_current_journal_record(rec)
        except Exception as e:
            if type(e).__name__ in ('AdmissionError', 'ValidationError'):
                raise Reject('JOURNAL_RECORD_SCHEMA_INVALID') from e
            raise
        return {'result': 'CURRENT', 'recordSchema': 3, 'runId': rec.get('runId')}
    if schema == HISTORICAL_JOURNAL_RECORD_SCHEMA:
        if type(run_id) is str and (run_id.startswith('run3:') or _RUN3.match(run_id)):
            raise Reject('JOURNAL_RECORD_MIXED_PREFIX')
        raise Reject('JOURNAL_RECORD_SCHEMA_HISTORICAL')
    raise Reject('JOURNAL_RECORD_SCHEMA_UNSUPPORTED')


def admit_seal_run_id_prefix(run_id):
    """Narrow run3 prefix dispatch. Not identity-model.v3.close_run. Not analysis-Run authority.
    Linearization uses FIXTURE_SEAL_RUN_ID through this helper only as a schedule token."""
    if type(run_id) is not str:
        raise Reject('SEAL_RUN_ID_INVALID')
    if _RUN2.match(run_id) or run_id.startswith('run2:'):
        raise Reject('JOURNAL_RECORD_MIXED_PREFIX')
    if not _RUN3.fullmatch(run_id):
        raise Reject('SEAL_RUN_ID_INVALID')
    if run_id == FIXTURE_SEAL_RUN_ID:
        raise Reject('SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY')
    return {'result': 'ADMIT', 'standing': 'prefix-dispatch', 'authority': 'run3-pattern',
            'runId': run_id, 'fixture': False}


def admit_host_seal_run_id(run_id):
    """Alias of admit_seal_run_id_prefix. Does not perform close_run."""
    return admit_seal_run_id_prefix(run_id)


_IDENTITY_V3 = None


def _identity_model_v3():
    """Lazy M3 load. Linearize never calls this. Not a product host."""
    global _IDENTITY_V3
    if _IDENTITY_V3 is None:
        path = Path(__file__).resolve().parent.parent / 'foundation' / 'identity-model.v3.py'
        spec = importlib.util.spec_from_file_location('security_identity_model_v3', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _IDENTITY_V3 = module
    return _IDENTITY_V3


def admit_analysis_seal(record, run, objects, blobs):
    """Public reference SEAL of an analysis Run.

    Requires identity-model.v3.close_run on the supplied retained graph and
    compares the returned RunId to the journal SEAL runId. Prefix dispatch is
    not this boundary. Linearize is an abstract brokered-effect schedule, not
    product analysis SEAL. Root-required proof.executionInputsDigest is enforced
    inside close_run/reconstruct; this adapter does not mint that digest.
    """
    admitted = admit_journal_record(record)
    if record.get('recordType') != 'SEAL':
        raise Reject('SEAL_RECORD_TYPE')
    claimed = record.get('runId')
    if claimed is None:
        raise Reject('SEAL_RUN_ID_REQUIRED')
    if claimed == FIXTURE_SEAL_RUN_ID:
        raise Reject('SEAL_RUN_ID_FIXTURE_NOT_AUTHORITY')
    IM = _identity_model_v3()
    try:
        actual = IM.close_run(run, objects, blobs)
    except Exception as e:
        if type(e).__name__ in ('AdmissionError', 'EvidenceUnavailable', 'RegenerationMismatch'):
            raise Reject('SEAL_CLOSE_RUN_REFUSED:' + str(e).split('\n')[0][:240]) from e
        raise
    if actual != claimed:
        raise Reject('SEAL_RUN_ID_MISMATCH')
    return {'result': 'ADMIT', 'standing': 'current-host', 'authority': 'identity-model.v3.close_run',
            'runId': actual, 'journalRecordSchema': admitted['recordSchema'], 'fixture': False}


def linearize(schedule, grant_generation=1, operation_ref='op-' + '0' * 32):
    """Journal linearization model. `schedule` is the order in which actors acquire the journal
    append lock L. Each step is one of:
      GRANT <g>            append GRANT g
      RA <r>               request accepted for r (refused RF-6 GRANT_NOT_CURRENT after REV)
      ICI <r> | RCI <r>    intent appended (skipped -> not-begun if REV already present)
      COMMIT <r>           atomic under L: if no REV -> brokered effect committed + ICO/RCO COMPLETED (postimage
                           digest retained); else no effect
      EDIT <r>             the user (or anything outside the broker) changes the target after COMMIT
      INDET <r>            the target's current state cannot be read (rollback would be indeterminate)
      CHILD <name>         an unconfined child (trusted repository code) is running; not a brokered effect
      REV <reason>         append REV under L, then postimage-checked rollback, cleanup (CLN) and bounded cancellation
      SEAL                 append SEAL (recordSchema 3, fixture run3 id) under L; refused after REV
      POLL                 observer tick (no journal effect)
    Linearization covers BROKERED effects only: no brokered effect commits after REV. Unconfined children
    are cancelled within the bound but their external effects before the kill are not enumerable.
    Current records are recordSchema 3. Schema-2 journals remain frozen historical bytes."""
    journal = []
    seq = 0
    state = {'rev': None, 'requests': {}, 'sealed': False, 'refused': [], 'grants': set(), 'children': {}}

    def append(rec):
        nonlocal seq
        seq += 1
        body = dict(rec)
        body.update({'recordSchema': CURRENT_JOURNAL_RECORD_SCHEMA, 'grantGeneration': grant_generation, 'seq': seq, 'operationRef': operation_ref})
        body['bodySha256'] = journal_body_sha({k: v for k, v in body.items() if k != 'bodySha256'})
        journal.append(body)
        return seq

    for step in schedule:
        parts = step.split()
        op = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        if op == 'GRANT':
            state['grants'].add(arg)
            append({'recordType': 'GRANT', 'grant': arg})
        elif op == 'RA':
            if state['rev'] is not None:
                state['refused'].append({'request': arg, 'refusal': 'RF-6:AUTHORIZATION.GRANT_NOT_CURRENT', 'atSeq': seq})
                continue
            s = append({'recordType': 'RA', 'requestRef': arg})
            state['requests'][arg] = {'ra': s, 'intent': None, 'class': None, 'outcome': None, 'effect': False,
                                      'preimage': 'pre:' + arg, 'postimage': None, 'current': 'pre:' + arg, 'readable': True}
        elif op in ('ICI', 'RCI'):
            req = state['requests'].get(arg)
            if req is None:
                raise Reject('INTENT_WITHOUT_RA:' + arg)
            if state['rev'] is not None:
                req['blockedAfterRev'] = True
                continue
            s = append({'recordType': op, 'requestRef': arg})
            req['intent'] = s
            req['class'] = 'IRREVERSIBLE' if op == 'ICI' else 'REVERSIBLE'
        elif op == 'COMMIT':
            req = state['requests'].get(arg)
            if req is None or req['intent'] is None:
                raise Reject('COMMIT_WITHOUT_INTENT:' + arg)
            if state['rev'] is not None:
                req['blockedAfterRev'] = True
                continue
            req['effect'] = True
            req['postimage'] = 'post:' + arg
            req['current'] = req['postimage']
            s = append({'recordType': 'ICO' if req['class'] == 'IRREVERSIBLE' else 'RCO', 'requestRef': arg, 'outcome': 'COMPLETED',
                        'postimageSha256': hashlib.sha256(req['postimage'].encode()).hexdigest()})
            req['outcome'] = s
        elif op == 'EDIT':
            req = state['requests'].get(arg)
            if req is None or not req['effect']:
                raise Reject('EDIT_WITHOUT_EFFECT:' + arg)
            req['current'] = 'edited:' + arg
        elif op == 'INDET':
            req = state['requests'].get(arg)
            if req is None or not req['effect']:
                raise Reject('INDET_WITHOUT_EFFECT:' + arg)
            req['readable'] = False
        elif op == 'CHILD':
            state['children'][arg] = {'running': True, 'startedAtSeq': seq}
        elif op == 'REV':
            if state['rev'] is not None:
                continue
            reason = arg or 'trust-revoked'
            rs = append({'recordType': 'REV', 'reason': reason, 'trustEpochObserved': {'revocationVersion': 'observed'}})
            state['rev'] = rs
            residuals = []
            disclosure = {'revocationSeq': rs, 'completedBeforeRevocation': [], 'reverted': [], 'rollbackBlocked': [],
                          'indeterminate': [], 'notBegun': [], 'unconfinedChildren': []}
            for r, req in state['requests'].items():
                if req['outcome'] is not None:
                    if req['class'] == 'REVERSIBLE' and reason == 'trust-revoked':
                        if not req['readable']:
                            residuals.append('%s:rollback-indeterminate' % r)
                            disclosure['indeterminate'].append(r)
                        elif req['current'] == req['postimage']:
                            req['current'] = req['preimage']
                            residuals.append('%s:reverted' % r)
                            disclosure['reverted'].append(r)
                        else:
                            residuals.append('%s:rollback-blocked-modified-since-commit' % r)
                            disclosure['rollbackBlocked'].append(r)
                    else:
                        residuals.append('%s:completed-irreversible' % r if req['class'] == 'IRREVERSIBLE' else '%s:completed-reversible-retained' % r)
                        disclosure['completedBeforeRevocation'].append(r)
                else:
                    residuals.append('%s:not-begun' % r)
                    disclosure['notBegun'].append(r)
            for c, ch in state['children'].items():
                ch['running'] = False
                residuals.append('%s:child-cancelled-external-effects-not-enumerable' % c)
                disclosure['unconfinedChildren'].append({'name': c, 'standing': 'cancelled within bound; effects before kill not enumerable; not a brokered effect'})
            append({'recordType': 'CLN', 'residuals': residuals})
            state['disclosure'] = disclosure
            state['cancellation'] = {
                'steps': [
                    {'step': 1, 'action': 'refuse further effectRequests (GRANT_NOT_CURRENT)', 'boundSeconds': 0},
                    {'step': 2, 'action': 'protocol Cancel', 'boundSeconds': CANCEL_GRACE_S},
                    {'step': 3, 'action': 'SIGTERM', 'boundSeconds': TERM_GRACE_S},
                    {'step': 4, 'action': 'SIGKILL process group, reap, EOF', 'boundSeconds': CANCELLATION_TOTAL_BOUND_S - CANCEL_GRACE_S - TERM_GRACE_S},
                    {'step': 5, 'action': 'clear connection map, remove spawn scratch under lease', 'boundSeconds': 0},
                ],
                'totalBoundSeconds': CANCELLATION_TOTAL_BOUND_S,
                'requestDriven': False,
                'standing': OBSERVER_OBLIGATION['standing'],
            }
        elif op == 'SEAL':
            if state['rev'] is not None:
                state['sealRefused'] = 'SEAL_AFTER_REV'
                continue
            s = append({'recordType': 'SEAL', 'runId': FIXTURE_SEAL_RUN_ID})
            state['sealed'] = True
            state['sealSeq'] = s
        elif op == 'POLL':
            pass
        else:
            raise Reject('UNKNOWN_STEP:' + step)
    out = {'journal': [{k: v for k, v in r.items() if k != 'bodySha256'} for r in journal],
           'journalTypes': [r['recordType'] for r in journal],
           'refused': state['refused'], 'sealed': state['sealed'], 'sealSeq': state.get('sealSeq'),
           'sealRefused': state.get('sealRefused'), 'revocationSeq': state['rev'],
           'disclosure': state.get('disclosure'), 'cancellation': state.get('cancellation'),
           'effectsCommitted': sorted(r for r, q in state['requests'].items() if q['effect']),
           'finalTargets': {r: q['current'] for r, q in sorted(state['requests'].items())},
           'sealedBeforeRevocation': None,
           'linearizationScope': 'brokered effects only; unconfined child effects are disclosed, not linearized'}
    if state['rev'] is not None:
        out['sealedBeforeRevocation'] = state['sealed'] and state['sealSeq'] < state['rev']
        # invariant: no brokered effect committed after REV
        assert all(q['outcome'] is None or q['outcome'] < state['rev'] for q in state['requests'].values())
    return out


# =============================================================================================
# S7 - Lease modes and lock order (AR-14)
# =============================================================================================
LOCK_ORDER = [
    {'level': 0, 'name': 'lifecycle fence', 'carrier': '<installRoot>/lifecycle.fence flock(LOCK_EX)', 'blocking': 'bounded wait (%d s) then PROJECT.BUSY' % FENCE_WAIT_BOUND_S},
    {'level': 1, 'name': 'project writer lease', 'carrier': '<namespace>/writer.lease flock(LOCK_EX|LOCK_NB)', 'blocking': 'never'},
    {'level': 2, 'name': 'project reader lease', 'carrier': '<namespace>/readers.lease flock(LOCK_SH|LOCK_NB) for readers; flock(LOCK_EX|LOCK_NB) for EXCLUSIVE', 'blocking': 'never'},
    {'level': 3, 'name': 'ledger transaction', 'carrier': 'SQLite WAL; writers BEGIN IMMEDIATE with busy_timeout 0; readers read a committed snapshot', 'blocking': 'never for readers'},
    {'level': 4, 'name': 'journal append lock', 'carrier': 'in-process mutex', 'blocking': 'bounded, in-process'},
]
LEASE_MODES = ('SHARED-READ', 'APPEND-WRITE', 'EXCLUSIVE')
DEFAULT_NAMESPACE = 'ns-default'
# S7 core-transition lock set (post-reset review SHOULD-6). A core transition (`core update|repair|rollback`,
# `store migrate|rollback`) is install-level state, and EXCLUSIVE is a per-namespace project lease, so the
# mechanism is a COMPOSITION, not a new flock mode:
#   1. hold the install-wide lifecycle fence (level 0) for the WHOLE transition, not only for lease acquisition;
#   2. enumerate the affected namespaces from the host namespace registry (ProjectId <-> namespace locator), never
#      from a directory listing and never from user input: ALL registered namespaces when the from/to state schema
#      differ or the operation is a rollback/store re-selection (`affects: all-registered`); NO namespace when the
#      selected core closure changes but the state schema is unchanged and no store is re-selected
#      (`affects: none`; running project operations keep their pinned immutable generation and re-check trust at
#      their S6 checkpoints);
#   3. take EXCLUSIVE on each affected namespace in namespace-locator byte order, non-blocking; the first busy
#      namespace aborts: every acquired lease is released in reverse order, the fence is released, PROJECT.BUSY names
#      the busy namespace and its holders, and the retry happens outside the fence with the S7 backoff;
#   4. write the CoreTransitionIntentV1 / migrating-root journal record naming the exact lease set only after all
#      leases are held; crash recovery (S9 table) runs as the first act under the next fence acquisition, before any
#      project admission, and re-acquires exactly the journaled lease set (a namespace registered after the intent
#      cannot exist, because registration itself needs the fence; if one is found the footprint is MIGRATION.CORRUPT);
#   5. release leases in reverse order, then the fence.
# Ordinary component `install`/`update` publish new immutable generations under the fence alone and take no project
# lease; they never revoke a generation a live operation pins (GC census governs removal).
CORE_TRANSITION_AFFECTS = ('all-registered', 'none')


def core_transition_affected_namespaces(intent, registry):
    """Decide the required project lease set of a core transition from its intent and the host namespace registry.
    intent: {operation: core-update|core-repair|core-rollback|store-migrate|store-rollback, fromStateSchema,
    toStateSchema, fromStoreGeneration, toStoreGeneration}. Returns {'affects', 'namespaces'} with namespaces in locator byte order."""
    op = intent.get('operation')
    if op not in ('core-update', 'core-repair', 'core-rollback', 'store-migrate', 'store-rollback'):
        raise Reject('CORE_TRANSITION_OPERATION:' + str(op))
    schema_change = intent.get('fromStateSchema') != intent.get('toStateSchema')
    reselect = op in ('core-rollback', 'store-rollback', 'store-migrate') \
        or ('fromStoreGeneration' in intent and intent.get('fromStoreGeneration') != intent.get('toStoreGeneration'))
    if schema_change or reselect:
        return {'affects': 'all-registered', 'namespaces': sorted(registry, key=lambda s: s.encode('utf-8'))}
    return {'affects': 'none', 'namespaces': []}


def lease_schedule(actions, registry=None):
    """Actors perform lock actions; the model records results and checks the ordering laws:
      fence (level 0, the only blocking lock, bounded) -> project lease (always non-blocking) -> ledger/journal.
      SHARED-READ: any number; coexists with one APPEND-WRITE; excluded by EXCLUSIVE.
      APPEND-WRITE: at most one; append-only publication (never deletes or rewrites bytes a reader may
        reference); coexists with readers.
      EXCLUSIVE: GC, purge, migration, repair-apply; requires no reader and no writer.
    No actor may attempt a lease without the fence, wait for a lease, hold the fence while waiting for
    anything else, upgrade a lease, or write trust state under a project lease.
    Namespaces: every lease names a registered project namespace (`namespace`, default DEFAULT_NAMESPACE); the
    registry is the host namespace registry (`registry` argument; when None, DEFAULT_NAMESPACE only). A lease on an
    unregistered namespace is a violation (no arbitrary namespace).
    Core transitions: `core-transition-acquire` {actor, namespaces: [...]} takes EXCLUSIVE on every named registered
    namespace in locator order under the held fence, all-or-nothing and non-blocking; `core-transition-release`
    releases them in reverse order. The fence stays held by the transition actor throughout. `transition-journal`
    {actor, namespaces} is the write of the InstallationTransitionJournalV1 (S9.2): lawful only under the fence, only
    after the actor's whole lease set is held, and only naming exactly that held set (the journal names the exact
    lease set, never a requested or smaller one).
    action: {actor, op: fence-acquire|fence-release|lease|lease-release|gc-census|trust-write|
             core-transition-acquire|core-transition-release|transition-journal, mode?, namespace?, namespaces?}"""
    registered = sorted(registry, key=lambda s: s.encode('utf-8')) if registry is not None else [DEFAULT_NAMESPACE]
    fence = None
    ns_state = {ns: {'readers': set(), 'writer': None, 'exclusive': None} for ns in registered}
    transition = {}   # actor -> [namespaces held by a core transition]
    trace = []
    violations = []

    def holds(actor):
        return any(actor in s['readers'] or actor == s['writer'] or actor == s['exclusive'] for s in ns_state.values()) or actor in transition

    def holders(s):
        return s['exclusive'] or s['writer'] or ','.join(sorted(s['readers']))

    for a in actions:
        actor, op = a['actor'], a['op']
        ns = a.get('namespace', DEFAULT_NAMESPACE)
        res = None
        if op == 'fence-acquire':
            if fence is None:
                fence = actor
                res = 'ACQUIRED'
            else:
                res = 'BLOCKED-BY:' + fence
                if holds(actor):
                    violations.append('%s waits for the fence while holding a lease' % actor)
        elif op == 'fence-release':
            if fence != actor:
                violations.append('%s releases a fence it does not hold' % actor)
                res = 'NOOP'
            elif actor in transition:
                violations.append('%s releases the fence while its core transition still holds leases' % actor)
                res = 'REFUSED-TRANSITION-HOLDS-LEASES'
            else:
                fence = None
                res = 'RELEASED'
        elif op == 'lease':
            mode = a['mode']
            if mode not in LEASE_MODES:
                raise Reject('LEASE_MODE:' + str(mode))
            if ns not in ns_state:
                violations.append('%s attempts a lease on unregistered namespace %s' % (actor, ns))
                res = 'REFUSED-UNREGISTERED-NAMESPACE'
            elif fence != actor:
                violations.append('%s attempts a lease without the fence' % actor)
                res = 'REFUSED-NO-FENCE'
            elif holds(actor):
                violations.append('%s attempts an upgrade/second lease' % actor)
                res = 'REFUSED-NO-UPGRADE'
            else:
                s = ns_state[ns]
                if mode == 'SHARED-READ':
                    if s['exclusive'] is None:
                        s['readers'].add(actor)
                        res = 'ACQUIRED'
                    else:
                        res = 'BUSY:' + s['exclusive']
                elif mode == 'APPEND-WRITE':
                    if s['exclusive'] is None and s['writer'] is None:
                        s['writer'] = actor
                        res = 'ACQUIRED'
                    else:
                        res = 'BUSY:' + (s['exclusive'] or s['writer'])
                else:
                    if s['exclusive'] is None and s['writer'] is None and not s['readers']:
                        s['exclusive'] = actor
                        res = 'ACQUIRED'
                    else:
                        res = 'BUSY:' + holders(s)
                if res.startswith('BUSY'):
                    res += ' (non-blocking; report PROJECT.BUSY, release the fence, retry outside the fence)'
        elif op == 'lease-release':
            res = 'NOOP'
            for s in ns_state.values():
                if actor == s['exclusive']:
                    s['exclusive'] = None
                    res = 'RELEASED'
                elif actor == s['writer']:
                    s['writer'] = None
                    res = 'RELEASED'
                elif actor in s['readers']:
                    s['readers'].discard(actor)
                    res = 'RELEASED'
        elif op == 'core-transition-acquire':
            wanted = list(a.get('namespaces', []))
            if fence != actor:
                violations.append('%s starts a core transition without the fence' % actor)
                res = 'REFUSED-NO-FENCE'
            elif holds(actor):
                violations.append('%s starts a core transition while holding a lease' % actor)
                res = 'REFUSED-NO-UPGRADE'
            elif any(n not in ns_state for n in wanted):
                bad = sorted(n for n in wanted if n not in ns_state)
                violations.append('%s names unregistered namespace(s) %s in a core transition' % (actor, ','.join(bad)))
                res = 'REFUSED-UNREGISTERED-NAMESPACE:' + ','.join(bad)
            elif wanted != sorted(wanted, key=lambda s: s.encode('utf-8')) or len(set(wanted)) != len(wanted):
                violations.append('%s core transition lease set is not in locator order or has duplicates' % actor)
                res = 'REFUSED-LOCK-ORDER'
            else:
                acquired = []
                busy = None
                for n in wanted:
                    s = ns_state[n]
                    if s['exclusive'] is None and s['writer'] is None and not s['readers']:
                        s['exclusive'] = actor
                        acquired.append(n)
                    else:
                        busy = (n, holders(s))
                        break
                if busy is None:
                    transition[actor] = acquired
                    res = 'ACQUIRED-ALL:' + (','.join(acquired) if acquired else 'no-namespace-affected')
                else:
                    for n in reversed(acquired):   # all-or-nothing: release in reverse order, keep nothing
                        ns_state[n]['exclusive'] = None
                    res = 'BUSY:%s:%s (non-blocking; released %s; report PROJECT.BUSY, release the fence, retry outside the fence)' % (
                        busy[0], busy[1], ','.join(reversed(acquired)) if acquired else 'nothing')
        elif op == 'transition-journal':
            wanted = list(a.get('namespaces', []))
            if fence != actor:
                violations.append('%s journals a transition without the fence' % actor)
                res = 'REFUSED-NO-FENCE'
            elif actor not in transition:
                violations.append('%s journals a transition before its lease set is held' % actor)
                res = 'REFUSED-LEASE-SET-NOT-HELD'
            elif transition[actor] != wanted:
                violations.append('%s journals a lease set (%s) that differs from the held set (%s)' % (actor, ','.join(wanted), ','.join(transition[actor])))
                res = 'REFUSED-LEASE-SET-MISMATCH'
            else:
                res = 'JOURNALED:' + (','.join(wanted) if wanted else 'no-namespace-affected')
        elif op == 'core-transition-release':
            held = transition.pop(actor, None)
            if held is None:
                res = 'NOOP'
            else:
                for n in reversed(held):
                    ns_state[n]['exclusive'] = None
                res = 'RELEASED-ALL:' + (','.join(reversed(held)) if held else 'no-namespace-affected')
        elif op == 'gc-census':
            if fence != actor:
                violations.append('%s runs GC census without the fence' % actor)
                res = 'REFUSED-NO-FENCE'
            elif ns not in ns_state:
                violations.append('%s runs GC census on unregistered namespace %s' % (actor, ns))
                res = 'REFUSED-UNREGISTERED-NAMESPACE'
            else:
                s = ns_state[ns]
                live = sorted(s['readers'] | ({s['writer']} if s['writer'] else set()) | ({s['exclusive']} if s['exclusive'] else set()))
                res = 'CENSUS:' + ('live=' + ','.join(live) if live else 'all-released') + ' (LOCK_EX|LOCK_NB probe; busy means retain)'
        elif op == 'trust-write':
            if fence != actor:
                violations.append('%s writes trust state without the fence' % actor)
                res = 'REFUSED-NO-FENCE'
            elif holds(actor) and actor not in transition:
                violations.append('%s writes trust state while holding a project lease' % actor)
                res = 'REFUSED-ORDER'
            else:
                res = 'COMMITTED (readers see it via WAL snapshot; no reader is blocked)'
        else:
            raise Reject('UNKNOWN_OP:' + op)
        trace.append({'actor': actor, 'op': op, 'mode': a.get('mode'), 'namespace': ns if op in ('lease', 'gc-census') else None, 'result': res})
    d = ns_state.get(DEFAULT_NAMESPACE, {'readers': set(), 'writer': None, 'exclusive': None})
    return {'trace': trace, 'violations': violations, 'deadlockFree': not violations,
            'final': {'fence': fence, 'readers': sorted(d['readers']), 'writer': d['writer'], 'exclusive': d['exclusive'],
                      'namespaces': {n: {'readers': sorted(s['readers']), 'writer': s['writer'], 'exclusive': s['exclusive']} for n, s in ns_state.items()},
                      'coreTransitions': {actor: list(held) for actor, held in sorted(transition.items())}},
            'lockOrder': LOCK_ORDER}


# =============================================================================================
# S8 - Platform admission over a signed profile population (AR-06)
# =============================================================================================
PLATFORM_TCB = ['every observed value (sip, authenticatedRoot, kernUuid, dyldCdhash, secureBoot, lockdown, dpkg, fsType, nsUnchanged ...) is an asserted OS read; admission over it is modelled, not measured']
# ONE machine platform vocabulary (post-reset review MUST-2). These four ids are the delivery release inventory's
# `platformId` values and are used, unchanged, by: the signed PlatformProfileSetV1 keys, platform_admit output,
# RepoExecutionGrantV2.platformId / PLATFORM_TRUTH_TABLE, the native capability matrix `platformFamilies`, the workflow
# test-execution schema and the qualification gates. The historical short spellings are DISPLAY ALIASES only: they
# appear in human renderings and historical documents, are never a profile-set key, never an admitted platform and
# never a grant platformId (an alias presented as a machine id refuses typed).
PLATFORM_IDS = ('linux-aarch64-gnu', 'linux-x86_64-gnu', 'macos-aarch64', 'macos-x86_64')
PLATFORM_DISPLAY_ALIASES = {
    'macos-aarch64':     'macos-arm64',
    'macos-x86_64':      'macos-x86_64',
    'linux-x86_64-gnu':  'linux-x86_64',
    'linux-aarch64-gnu': 'linux-arm64',
}
_ALIAS_TO_PLATFORM = {alias: pid for pid, alias in PLATFORM_DISPLAY_ALIASES.items() if alias != pid}
SUPPORTED_POPULATION = {
    # Selected support population (design selection under D-367; the lane column is the qualification runner class
    # from security v8 section 8.7 and keeps its historical spelling). EXACT-MEASURED tier requires a release-measured
    # identity from a lane; BASELINE-ATTESTED tier admits unmeasured identities inside the population with identical
    # security predicates and records identity drift. Nothing outside the population is admitted.
    'macos-aarch64':     {'lanes': ['macos-15'],        'population': 'macOS 15 and 26 on Apple silicon, sealed system volume, SIP on, APFS install root'},
    'macos-x86_64':      {'lanes': ['macos-15-intel'],  'population': 'macOS 15 and 26 on Intel, sealed system volume, SIP on, APFS install root'},
    'linux-x86_64-gnu':  {'lanes': ['ubuntu-24.04'],    'population': 'Ubuntu 24.04 LTS, Canonical-signed kernels on the supported lines/flavors, ext4/xfs/btrfs install root'},
    'linux-aarch64-gnu': {'lanes': ['ubuntu-24.04-arm'], 'population': 'Ubuntu 24.04 LTS on arm64, Canonical-signed kernels on the supported lines/flavors, ext4/xfs/btrfs install root'},
}
assert tuple(sorted(SUPPORTED_POPULATION)) == PLATFORM_IDS
ENFORCEMENT_LIMITS = [
    'BASELINE-ATTESTED admits an identity no lane ever measured; the tier records drift, it does not detect a hostile kernel',
    'Linux bootAttestation=package-db-declared provides no boot attestation; only secure-boot-lockdown observes Secure Boot state',
    'macOS Full vs Reduced Security is not distinguished at launch; boot policy is virtualized-not-observable on hosted lanes',
    'platforms outside the population (other distributions, self-built kernels, non-APFS/ext4/xfs/btrfs roots, Windows) refuse',
]


def _macos_build_key(b):
    m = MACOS_BUILD_RE.match(b or '')
    if not m:
        raise Reject('MACOS_BUILD_GRAMMAR:%r' % (b,))
    return (int(m.group(1)), m.group(2), int(m.group(3)))


def platform_admit(profile_set, observed):
    """Two-tier admission. Security predicates are identical at both tiers; the tiers differ only
    in whether the exact measured identity of the platform TCB is required (EXACT-MEASURED) or
    recorded as drift within a supported population (BASELINE-ATTESTED)."""
    plat = observed['platform']
    base = {'result': None, 'platform': plat, 'displayAlias': PLATFORM_DISPLAY_ALIASES.get(plat), 'tier': None, 'lane': None,
            'refusals': [], 'drift': {}, 'disclosure': None, 'remedy': None,
            'd9': None, 'enforcementLimits': list(ENFORCEMENT_LIMITS), 'tcbAssumptions': list(PLATFORM_TCB)}

    def refuse(refusals, tier=None, remedy=None, drift=None):
        code = refusals[0].split(':')[0]
        return dict(base, result='REFUSE', tier=tier, refusals=refusals, remedy=remedy, drift=drift or {}, d9=d9(code))

    # the profile set is keyed by machine ids only; a display alias or any foreign key is not a population entry
    foreign = sorted(k for k in (profile_set.get('platforms') or {}) if k not in PLATFORM_IDS)
    if foreign:
        return refuse(['NT-TCB-PROFILE-UNQUALIFIED:PROFILE_SET_KEY_NOT_MACHINE_ID:' + ','.join(foreign)],
                      remedy='the signed profile set must be keyed by the four machine platform ids; display aliases never key it')
    if plat in _ALIAS_TO_PLATFORM:
        return refuse(['NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:' + _ALIAS_TO_PLATFORM[plat]],
                      remedy='present the machine platform id (%s); %r is a display alias' % (_ALIAS_TO_PLATFORM[plat], plat))
    ps = profile_set['platforms'].get(plat)
    if ps is None or plat not in SUPPORTED_POPULATION:
        return refuse(['NT-TCB-PROFILE-UNQUALIFIED:platform-not-in-population'], remedy='platform is outside the selected support population')
    lanes = SUPPORTED_POPULATION[plat]['lanes']
    refusals = []
    if observed.get('fsType') not in ps['installRootFilesystems']:
        refusals.append('NT-TCB-BOOT:INSTALL_ROOT_FS_%s' % observed.get('fsType'))
    if plat.startswith('macos'):
        if observed.get('authenticatedRoot') != 'enabled':
            refusals.append('NT-TCB-BOOT:AUTHENTICATED_ROOT_DISABLED')
        if observed.get('sip') is not True:
            refusals.append('NT-TCB-BOOT:SIP_DISABLED')
        if refusals:
            return refuse(refusals)
        build = observed.get('osversion')
        try:
            bk = _macos_build_key(build)
        except Reject:
            return refuse(['NT-TCB-IDENTITY:BUILD_GRAMMAR'])
        measured = {m['build']: m for m in ps['measuredProfiles']}
        if build in measured:
            m = measured[build]
            if m.get('lane') not in lanes:
                return refuse(['NT-TCB-PROFILE-UNQUALIFIED:MEASURED_ON_UNLISTED_LANE_%s' % m.get('lane')])
            for k in ('kernUuid', 'dyldCdhash'):
                if observed.get(k) != m[k]:
                    refusals.append('NT-TCB-IDENTITY:%s' % k)
            if refusals:
                return refuse(refusals, tier='EXACT-MEASURED')
            return dict(base, result='ADMIT', tier='EXACT-MEASURED', lane=m['lane'])
        major = str(bk[0])
        sup = ps['supportedMajors'].get(major)
        if sup is None:
            return refuse(['NT-TCB-PROFILE-UNQUALIFIED:MACOS_MAJOR_%s' % major], remedy='this macOS major is outside the signed profile population; a later release must measure it')
        if bk < _macos_build_key(sup['minBuild']):
            return refuse(['NT-TCB-PROFILE-UNQUALIFIED:BUILD_BELOW_FLOOR_%s' % sup['minBuild']])
        drift = {'kernUuid': observed.get('kernUuid'), 'dyldCdhash': observed.get('dyldCdhash'), 'osversion': build, 'standing': 'recorded-never-allow-refuse'}
        return dict(base, result='ADMIT', tier='BASELINE-ATTESTED', lane=None, drift=drift,
                    disclosure='build %s is within supported major %s but not release-measured; identity recorded as drift' % (build, major))
    # linux
    if observed.get('osReleaseId') != ps['distro'] or observed.get('versionId') not in ps['series']:
        return refuse(['NT-TCB-PROFILE-UNQUALIFIED:DISTRO_SERIES'], remedy='only the distribution/series in the population is supported')
    if not observed.get('procVersionUbuntu'):
        refusals.append('NT-TCB-BOOT:PROC_VERSION_NOT_UBUNTU')
    if not (observed.get('dpkgInstalled') and observed.get('dpkgMaintainerUbuntu')):
        refusals.append('NT-TCB-BOOT:KERNEL_PACKAGE_NOT_INSTALLED_BY_UBUNTU')
    if observed.get('archiveKeyDigest') != ps['archiveSigningKeyDigest']:
        refusals.append('NT-TCB-BOOT:ARCHIVE_KEY_DIGEST')
    if ps['bootAttestation'] == 'secure-boot-lockdown':
        if observed.get('secureBoot') != 1:
            refusals.append('NT-TCB-BOOT:SECURE_BOOT_OFF')
        if observed.get('lockdown') not in ('integrity', 'confidentiality'):
            refusals.append('NT-TCB-BOOT:LOCKDOWN_NONE')
        if observed.get('uefiSignerPresent') is not True:
            refusals.append('NT-TCB-BOOT:UEFI_SIGNER_ABSENT')
    elif ps['bootAttestation'] != 'package-db-declared':
        refusals.append('NT-TCB-BOOT:BOOT_ATTESTATION_UNKNOWN')
    if observed.get('nsUnchanged') is not True:
        refusals.append('NT-TCB-BOOT:MOUNT_NAMESPACE_CHANGED_DURING_READ')
    if refusals:
        return refuse(refusals)
    m = LINUX_OSRELEASE_RE.match(observed.get('osrelease') or '')
    if not m:
        return refuse(['NT-TCB-IDENTITY:OSRELEASE_GRAMMAR'])
    line, abi, flavor = m.group(1), m.group(2), m.group(3)
    for mp in ps['measuredProfiles']:
        if mp['line'] == line and mp['flavor'] == flavor:
            if mp.get('lane') not in lanes:
                return refuse(['NT-TCB-PROFILE-UNQUALIFIED:MEASURED_ON_UNLISTED_LANE_%s' % mp.get('lane')])
            return dict(base, result='ADMIT', tier='EXACT-MEASURED', lane=mp['lane'], drift={'abi': abi})
    if line in ps['supportedKernelLines'] and flavor in ps['baselineFlavors']:
        return dict(base, result='ADMIT', tier='BASELINE-ATTESTED', drift={'line': line, 'flavor': flavor, 'abi': abi},
                    disclosure='Canonical-signed %s kernel on supported line %s is not release-measured; identity recorded as drift' % (flavor, line))
    return refuse(['NT-TCB-PROFILE-UNQUALIFIED:KERNEL_LINE_OR_FLAVOR_%s-%s' % (line, flavor)],
                  remedy='kernel line/flavor outside the signed profile population; the core refuses rather than degrading')


# =============================================================================================
# S9 - Stage transition: crash recovery decision table, floor continuity, schema bridge (AR-14)
# =============================================================================================
SCHEMA_BRIDGE = {
    'stage1': {'rootReaders': [1], 'stateDecoder': 'state-decoder.v1', 'stateWriter': 1, 'trRepair': 'typed-absence-DR-110 only', 'kernelAttestationKeys': '[] only'},
    'stage2': {'rootReaders': [1, 2], 'stateDecoders': ['state-decoder.v1 (read-only migration source)', 'state-decoder.v2 (writer)'], 'stateWriter': 2,
               'trRepair': 'active admissible under schema 2 key policy', 'kernelAttestationKeys': 'nonempty admissible under schema 2 policy'},
    'orderedRelease': ['1. stage-2 core released under the schema-1 catalog (TR-CORE of root N): every stage-1 install can update to it by its ordinary path',
                       '2. root N+1 with rootSchema 2 released, signed by root-N keys (old threshold) and its own keys (new threshold)',
                       '3. stage-1 cores refuse N+1 typed (ROOT.SCHEMA_UNSUPPORTED, state unchanged) and keep root N until it expires; stage-2 cores accept N+1 by the dual reader',
                       '4. state migration 1->2 runs under EXCLUSIVE lease with floors copied forward; old store retained read-only for the rollback window'],
    'metadataProfile': 'opensip-metadata-canonical.1 (NFC) for root/catalog/revocation/journal/recovery documents at both stages; product data uses foundation/canonical.py; never mixed',
}


def migration_recover(footprint):
    """Decides from the durable footprint only. footprint = {
        old: {present: bool, unbootstrappedReason: None|'RESTORED'|..., ...},
        new: {dir: 'absent'|'migrating'|'final'|'both', state: None|'PREPARING'|'PREPARED'|'COMMITTED'}}"""
    old = footprint['old']
    new = footprint['new']
    base = {'action': None, 'refusal': None, 'd9': None, 'fromStep': None, 'oldRootRetainedDays': None, 'rationale': None}
    if new['dir'] == 'absent':
        return dict(base, action='NO-MIGRATION-IN-PROGRESS', rationale='nothing to recover; a state-using operation may begin prepare')
    if new['dir'] == 'both':
        return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'),
                    rationale='a final root and a migrating root coexist; the footprint is ambiguous and nothing is chosen')
    if new['dir'] == 'final':
        return dict(base, action='DONE', rationale='commit completed; old root retained read-only for the rollback window', oldRootRetainedDays=MIGRATION_ROLLBACK_WINDOW_DAYS)
    st = new.get('state')
    if st in (None, 'PREPARING'):
        return dict(base, action='ABORT', rationale='prepare did not complete; delete the migrating root; old state untouched')
    if st == 'PREPARED':
        if old.get('unbootstrappedReason') == 'RESTORED':
            return dict(base, action='RESUME-COMMIT', fromStep=3, rationale='old store already fenced (step 2 durable); finish steps 3-4')
        return dict(base, action='ABORT', rationale='prepared but commit not begun (old store not fenced); abort is exact')
    if st == 'COMMITTED':
        return dict(base, action='RESUME-COMMIT', fromStep=4, rationale='commit marker durable; only the final rename remains')
    return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'), rationale='unknown migration state')


FLOOR_KEYS = ('rootVersion', 'indexSnapshotVersion', 'revocationVersion', 'evalHighWater', 'lastAccepted', 'recoveryEpochSerial')


def migrate_floors(old_trust, core_embedded_chain_max, core_readers=(1, 2)):
    """Floors move forward only. The new core's embedded chain must reach the old accepted root."""
    n = old_trust['rootVersion']
    base = {'result': None, 'refusal': None, 'd9': None, 'rationale': None, 'newTrust': None, 'oldStoreMark': None, 'floorsLowered': None, 'downgradeNoReturn': None, 'bridge': SCHEMA_BRIDGE}
    if n > core_embedded_chain_max:
        return dict(base, result='REFUSE', refusal='ROOT.FLOOR_ABOVE_CORE', d9=d9('ROOT.FLOOR_ABOVE_CORE'),
                    rationale='the old install accepted root %d; this core knows only up to %d; a newer core is required' % (n, core_embedded_chain_max))
    new = {k: old_trust.get(k) for k in FLOOR_KEYS}
    new['anchor'] = None  # a migration never carries a boot anchor
    new['pendingRecoveryChallenge'] = None  # a pending challenge is bound to the old record digest and does not survive
    new['roles'] = 'ST-UNBOOTSTRAPPED:MIGRATED (re-established by the PRESENT event over the embedded chain)'
    return dict(base, result='COPIED', newTrust=new, oldStoreMark='RESTORED', floorsLowered=False,
                downgradeNoReturn='after commit the stage-1 core observes RESTORED and refuses until a schema-1-verifiable payload at or above the floors')


def rollback_floors(new_trust, old_trust, old_core_chain_max, old_core_readers=(1,)):
    """Rollback inside the window re-selects the old store; floors are copied BACK forward-only. If the new
    store accepted a root the old core cannot verify (schema or chain reach), rollback refuses typed."""
    base = {'result': None, 'refusal': None, 'd9': None, 'rationale': None, 'oldTrustAfter': None, 'floorsLowered': None}
    if new_trust['rootVersion'] > old_core_chain_max or new_trust.get('acceptedRootSchema', 1) not in old_core_readers:
        return dict(base, result='REFUSE', refusal='ROOT.FLOOR_ABOVE_CORE', d9=d9('ROOT.FLOOR_ABOVE_CORE'),
                    rationale='the new store accepted root %d (schema %d); the old core cannot verify it; rollback would lower a floor' % (new_trust['rootVersion'], new_trust.get('acceptedRootSchema', 1)))
    after = {}
    for k in FLOOR_KEYS:
        a, b = old_trust.get(k), new_trust.get(k)
        if a is None:
            after[k] = b
        elif b is None:
            after[k] = a
        else:
            after[k] = max(a, b)
    after['anchor'] = None
    after['pendingRecoveryChallenge'] = None
    after['roles'] = 'ST-UNBOOTSTRAPPED:RESTORED'
    return dict(base, result='ROLLED-BACK', oldTrustAfter=after, floorsLowered=False,
                rationale='old store re-selected; floors are the maximum of both stores; roles re-established by the next PRESENT event')


# =============================================================================================
# S9.2 - Installation transition intent and JOURNAL (post-reset review v2, P10): one closed record for
#        core update|repair|rollback and store migrate|rollback under the S7 core-transition lock set
# =============================================================================================
TRANSITION_OPERATIONS = ('core-update', 'core-repair', 'core-rollback', 'store-migrate', 'store-rollback')
CORE_OPERATIONS = ('core-update', 'core-repair', 'core-rollback')
STORE_OPERATIONS = ('store-migrate', 'store-rollback')
ROLLBACK_OPERATIONS = ('core-rollback', 'store-rollback')
STATE_SCHEMAS = (1, 2)
# Required operation/field contract of the host-projected intent (workflow CoreTransitionIntentV1 successor; Codex owns
# the workflow schema and projection). The same eleven fields serve core and store operations; a store operation keeps
# the core closure, a same-schema core operation keeps the store.
TRANSITION_INTENT_KEYS = {'schemaVersion', 'operation', 'fromCoreClosure', 'toCoreClosure', 'fromStateSchema', 'toStateSchema',
                          'fromStoreGeneration', 'toStoreGeneration', 'platformProfileSetBodyDigest', 'preconditionGeneration',
                          'rollbackDeadline'}
INTENT_BOUND_FIELDS = ('operation', 'fromCoreClosure', 'toCoreClosure', 'fromStateSchema', 'toStateSchema', 'fromStoreGeneration',
                       'toStoreGeneration', 'platformProfileSetBodyDigest', 'preconditionGeneration', 'rollbackDeadline')
TRANSITION_JOURNAL_KEYS = {'journalSchema', 'kind', 'intentDigest', 'registryDigest', 'registry', 'affects', 'leaseSet', 'state',
                           'fenceHeld', 'writtenAfterAllLeasesHeld'} | set(INTENT_BOUND_FIELDS)
TRANSITION_STATES = ('LEASED', 'PREPARING', 'PREPARED', 'COMMITTED', 'DONE', 'ABORTED')
TRANSITION_JOURNAL_DOMAIN = 'security.installation-transition-journal.v1'
# Crash recovery decision table (first act under the next fence, before any project admission). `store-footprint`
# defers to the S9 migrating-root table (`migration_recover`) for the durable store footprint.
TRANSITION_RECOVERY_TABLE = {
    'LEASED':    ('ABORT', 'ABORTED', 'intent journaled, nothing prepared: release the journaled lease set; installation unchanged'),
    'PREPARING': ('ABORT', 'ABORTED', 'preparation incomplete: discard the unpublished generation / migrating root; installation unchanged'),
    'PREPARED':  ('store-footprint', None, 'prepared: a store operation follows the S9 footprint table (RESUME-COMMIT only when the old store is fenced); '
                                            'a core operation aborts because the published generation was never selected (GC census reclaims it)'),
    'COMMITTED': ('RESUME-COMMIT', 'DONE', 'commit marker durable: finish the selection switch / final rename; a committed transition is never reversed'),
    'DONE':      ('RELEASE-ONLY', 'DONE', 'transition complete; only the lease set and fence remain to release'),
    'ABORTED':   ('RELEASE-ONLY', 'ABORTED', 'transition aborted; only the lease set and fence remain to release'),
}
TRANSITION_TCB = ['`fenceHeld`, `leasesHeld`/`leasesReacquired`, the namespace registry, current schema/store/core generation and the store '
                  'footprint are host observations made under the fence (asserted); the model decides, it does not lock or read']


def transition_intent_digest(intent):
    """Raw SHA-256 of the canonical admitted intent (product data). Equals the workflow mutation step's
    inputDescriptorDigest (S15); the journal binds it as `intentDigest`."""
    return hashlib.sha256(_C.canonical(intent)).hexdigest()


def admit_transition_intent(intent):
    """Total admission of the host-projected installation transition intent. Returns the closed refusal list (empty =
    admitted). Shape first, then per-operation semantics:
      core-update    closure changes; the state schema never lowers; a schema change selects a new store, a same-schema
                     update keeps the store (immutable generations stay pinned, S7 `affects: none`)
      core-repair    closure, schema and store all unchanged (replaces damaged bytes of the selected closure)
      core-rollback  closure changes; schema never rises; needs the host-observed rollback deadline
      store-migrate  core closure unchanged; schema advances; a new store generation is selected
      store-rollback core closure unchanged; schema retreats; the retained old store generation is re-selected; needs the deadline"""
    if not isinstance(intent, dict) or set(intent) != TRANSITION_INTENT_KEYS:
        return ['TRANSITION.INTENT_SHAPE']
    r = []
    if not (_int(intent['schemaVersion']) and intent['schemaVersion'] == 1):
        r.append('TRANSITION.INTENT_SCHEMA')
    op = intent['operation']
    if op not in TRANSITION_OPERATIONS:
        return r + ['TRANSITION.OPERATION:' + str(op)]
    for k in ('fromCoreClosure', 'toCoreClosure'):
        if not isinstance(intent[k], str) or not CLOSURE_ID_RE.match(intent[k]):
            r.append('TRANSITION.CLOSURE_SHAPE:' + k)
    for k in ('fromStateSchema', 'toStateSchema'):
        if not _int(intent[k]) or intent[k] not in STATE_SCHEMAS:
            r.append('TRANSITION.STATE_SCHEMA:' + k)
    for k in ('fromStoreGeneration', 'toStoreGeneration', 'preconditionGeneration'):
        if not _int(intent[k]) or intent[k] < 0:
            r.append('TRANSITION.GENERATION_SHAPE:' + k)
    if not isinstance(intent['platformProfileSetBodyDigest'], str) or not HEX64.match(intent['platformProfileSetBodyDigest']):
        r.append('TRANSITION.PROFILE_DIGEST_SHAPE')
    dl = intent['rollbackDeadline']
    if dl is not None and (not isinstance(dl, str) or not TS_RE.fullmatch(dl)):
        r.append('TRANSITION.ROLLBACK_DEADLINE_SHAPE')
    if r:
        return r
    same_closure = intent['fromCoreClosure'] == intent['toCoreClosure']
    same_schema = intent['fromStateSchema'] == intent['toStateSchema']
    same_store = intent['fromStoreGeneration'] == intent['toStoreGeneration']
    if op == 'core-repair':
        if not same_closure:
            r.append('TRANSITION.REPAIR_MUST_KEEP_CLOSURE')
        if not same_schema:
            r.append('TRANSITION.REPAIR_MUST_KEEP_SCHEMA')
        if not same_store:
            r.append('TRANSITION.REPAIR_MUST_KEEP_STORE')
    elif op == 'core-update':
        if same_closure:
            r.append('TRANSITION.UPDATE_MUST_CHANGE_CLOSURE')
        if intent['toStateSchema'] < intent['fromStateSchema']:
            r.append('TRANSITION.UPDATE_CANNOT_LOWER_SCHEMA')
        if same_schema and not same_store:
            r.append('TRANSITION.SAME_SCHEMA_KEEPS_STORE')
        if not same_schema and same_store:
            r.append('TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE')
    elif op == 'core-rollback':
        if same_closure:
            r.append('TRANSITION.ROLLBACK_MUST_CHANGE_CLOSURE')
        if intent['toStateSchema'] > intent['fromStateSchema']:
            r.append('TRANSITION.ROLLBACK_CANNOT_RAISE_SCHEMA')
        if same_schema and not same_store:
            r.append('TRANSITION.SAME_SCHEMA_KEEPS_STORE')
        if not same_schema and same_store:
            r.append('TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE')
    elif op == 'store-migrate':
        if not same_closure:
            r.append('TRANSITION.STORE_OPERATION_KEEPS_CORE')
        if intent['toStateSchema'] <= intent['fromStateSchema']:
            r.append('TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE')
        if same_store:
            r.append('TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE')
    elif op == 'store-rollback':
        if not same_closure:
            r.append('TRANSITION.STORE_OPERATION_KEEPS_CORE')
        if intent['toStateSchema'] >= intent['fromStateSchema']:
            r.append('TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT')
        if same_store:
            r.append('TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE')
    if op in ROLLBACK_OPERATIONS and dl is None:
        r.append('TRANSITION.ROLLBACK_REQUIRES_DEADLINE')
    if op not in ROLLBACK_OPERATIONS and dl is not None:
        r.append('TRANSITION.DEADLINE_ONLY_FOR_ROLLBACK')
    return r


def _registry_sorted(registry):
    return sorted(set(registry), key=lambda s: s.encode('utf-8'))


def registry_digest(registry):
    """Raw SHA-256 of the canonical sorted namespace-locator list frozen under the fence."""
    return hashlib.sha256(_C.canonical(_registry_sorted(registry))).hexdigest()


def transition_journal_record(intent, registry):
    """Constructor of the InstallationTransitionJournalV1 a host writes AFTER every lease of the affected set is held
    (state LEASED). Reference only: the admission function re-derives every binding from the trusted context and
    never trusts this record's own claims."""
    r = admit_transition_intent(intent)
    if r:
        raise Reject('TRANSITION_INTENT:' + ','.join(r))
    scope = core_transition_affected_namespaces(intent, _registry_sorted(registry))
    j = {'journalSchema': 1, 'kind': 'installation-transition', 'intentDigest': transition_intent_digest(intent),
         'registryDigest': registry_digest(registry), 'registry': _registry_sorted(registry), 'affects': scope['affects'],
         'leaseSet': scope['namespaces'], 'state': 'LEASED', 'fenceHeld': True, 'writtenAfterAllLeasesHeld': True}
    for k in INTENT_BOUND_FIELDS:
        j[k] = intent[k]
    return j


def admit_transition_journal(journal, ctx):
    """InstallationTransitionJournalV1 admission (S9.2). Identity H('security.installation-transition-journal.v1',
    journal) is the retained journal reference. Total over the trusted context:
      ctx = {intent                  -- the host-admitted intent record (workflow CoreTransitionIntentV1 successor)
             intentDigest            -- host-computed raw SHA-256 of the canonical admitted intent (= inputDescriptorDigest)
             namespaceRegistry       -- the host namespace registry read under the held fence
             fenceHeld               -- the install-wide lifecycle fence is held by this operation (bool)
             leasesHeld              -- the EXCLUSIVE lease set the S7 composition actually acquired, locator order
             currentStateSchema, currentStoreGeneration, currentCoreGeneration  -- observed under the fence
             admittedTime}           -- S4 PROCEED evaluation time (None when no admitted time context exists)
    Laws: the journal binds the exact admitted intent (digest and every bound field); it freezes the registry observed
    under the fence; its affected set and lease set are exactly `core_transition_affected_namespaces` over that frozen
    registry (a caller cannot choose a smaller or different set: any mismatch is TRANSITION.SCOPE_MISMATCH); it may be
    written only while the fence is held and only after every lease of that set is held; it binds the current schema,
    store generation and core generation it starts from; a rollback needs an admitted time inside the host-observed
    window. Every refusal is D9 REQUEST.PRECONDITION_FAILED (request-rejected, 2)."""
    base = {'result': None, 'refusals': [], 'd9': None, 'journalRef': None, 'affects': None, 'leaseSet': None,
            'identityDomain': TRANSITION_JOURNAL_DOMAIN, 'fenceHeldThroughout': True,
            'recovery': 'first act under the next fence acquisition, before any project admission (recover_transition_journal)',
            'trustedContextInputs': ['intent', 'intentDigest', 'namespaceRegistry', 'fenceHeld', 'leasesHeld', 'currentStateSchema',
                                     'currentStoreGeneration', 'currentCoreGeneration', 'admittedTime']}
    if not isinstance(journal, dict) or set(journal) != TRANSITION_JOURNAL_KEYS:
        return dict(base, result='REFUSE', refusals=['TRANSITION.JOURNAL_SHAPE'], d9=d9('TRANSITION.REFUSED'))
    r = []
    if not (_int(journal['journalSchema']) and journal['journalSchema'] == 1) or journal['kind'] != 'installation-transition':
        r.append('TRANSITION.JOURNAL_SHAPE')
    if journal['fenceHeld'] is not True or journal['writtenAfterAllLeasesHeld'] is not True:
        r.append('TRANSITION.JOURNAL_LAW_CONSTANTS')
    if journal['state'] != 'LEASED':
        r.append('TRANSITION.INITIAL_STATE:' + str(journal['state']))
    intent = ctx.get('intent')
    ir = admit_transition_intent(intent)
    if ir:
        r.extend('TRANSITION.CONTEXT_INTENT:' + x for x in ir)
    else:
        expected_digest = transition_intent_digest(intent)
        if journal['intentDigest'] != expected_digest or ctx.get('intentDigest') != expected_digest:
            r.append('TRANSITION.INTENT_DIGEST_MISMATCH')
        for k in INTENT_BOUND_FIELDS:
            if not _C.equal_typed(journal[k], intent[k]):
                r.append('TRANSITION.INTENT_FIELD_MISMATCH:' + k)
    registry = _registry_sorted(ctx.get('namespaceRegistry', []))
    if not isinstance(journal['registry'], list) or journal['registry'] != registry:
        r.append('TRANSITION.REGISTRY_MISMATCH')
    if journal['registryDigest'] != registry_digest(registry):
        r.append('TRANSITION.REGISTRY_DIGEST_MISMATCH')
    if not ir:
        scope = core_transition_affected_namespaces(intent, registry)
        if journal['affects'] != scope['affects'] or journal['leaseSet'] != scope['namespaces']:
            r.append('TRANSITION.SCOPE_MISMATCH')
        held = list(ctx.get('leasesHeld', []))
        if held != scope['namespaces']:
            r.append('TRANSITION.LEASE_SET_NOT_HELD')
    if ctx.get('fenceHeld') is not True:
        r.append('TRANSITION.FENCE_NOT_HELD')
    if not ir:
        if ctx.get('currentStateSchema') != intent['fromStateSchema']:
            r.append('TRANSITION.CURRENT_SCHEMA_MISMATCH')
        if ctx.get('currentStoreGeneration') != intent['fromStoreGeneration']:
            r.append('TRANSITION.CURRENT_STORE_MISMATCH')
        if ctx.get('currentCoreGeneration') != intent['preconditionGeneration']:
            r.append('TRANSITION.PRECONDITION_GENERATION_MISMATCH')
        if intent['operation'] in ROLLBACK_OPERATIONS:
            now = ctx.get('admittedTime')
            if now is None:
                r.append('TRANSITION.NO_ADMITTED_TIME_CONTEXT')
            elif ts(now) > ts(intent['rollbackDeadline']):
                r.append('TRANSITION.ROLLBACK_WINDOW_EXPIRED')
    if r:
        return dict(base, result='REFUSE', refusals=r, d9=d9('TRANSITION.REFUSED'))
    return dict(base, result='ADMIT', journalRef=TRANSITION_JOURNAL_DOMAIN + ':' + _C.identity(TRANSITION_JOURNAL_DOMAIN, journal),
                affects=journal['affects'], leaseSet=list(journal['leaseSet']))


def recover_transition_journal(journal, ctx):
    """Crash recovery for a journaled installation transition: the FIRST act under the next fence acquisition, before
    any project admission. ctx = {namespaceRegistry (read under the new fence), fenceHeld, leasesReacquired (the set
    the S7 composition re-acquired, locator order), storeFootprint (S9 footprint for store operations; optional)}.
    Fail-closed laws: the fence must be held; the registry must equal the frozen one (a namespace registered or
    deregistered while a transition was journaled is impossible without the fence, so a difference is
    MIGRATION.CORRUPT and nothing is chosen); exactly the journaled lease set must be re-acquired (anything else is
    PROJECT.BUSY, retried outside the fence); then the closed table decides. A COMMITTED transition is finished, never
    reversed; an expired rollback window does not undo a committed rollback."""
    base = {'action': None, 'journalStateAfter': None, 'refusal': None, 'd9': None, 'reacquire': None, 'fromStep': None, 'rationale': None,
            'trustedContextInputs': ['namespaceRegistry', 'fenceHeld', 'leasesReacquired', 'storeFootprint']}
    if not isinstance(journal, dict) or set(journal) != TRANSITION_JOURNAL_KEYS or journal['state'] not in TRANSITION_STATES:
        return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'), rationale='journal shape or state unknown; nothing is chosen')
    lease_set = list(journal['leaseSet'])
    if ctx.get('fenceHeld') is not True:
        return dict(base, action='REFUSE', refusal='TRANSITION.FENCE_NOT_HELD', d9=d9('TRANSITION.REFUSED'), reacquire=lease_set,
                    rationale='recovery runs only under the fence')
    registry = _registry_sorted(ctx.get('namespaceRegistry', []))
    if registry != journal['registry'] or registry_digest(registry) != journal['registryDigest']:
        return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'), reacquire=lease_set,
                    rationale='namespace registry differs from the frozen journal registry; registration needs the fence, so the footprint is ambiguous')
    held = list(ctx.get('leasesReacquired', []))
    if held != lease_set:
        return dict(base, action='BUSY', refusal='PROJECT.BUSY', d9=d9('PROJECT.BUSY'), reacquire=lease_set,
                    rationale='the journaled lease set was not re-acquired exactly (%s); release, drop the fence, retry outside it' %
                    (','.join(sorted(set(lease_set) ^ set(held), key=lambda s: s.encode('utf-8'))) or 'order'))
    action, after, why = TRANSITION_RECOVERY_TABLE[journal['state']]
    if action == 'store-footprint':
        if journal['operation'] in STORE_OPERATIONS:
            fp = ctx.get('storeFootprint')
            if not isinstance(fp, dict):
                return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'), reacquire=lease_set,
                            rationale='PREPARED store transition without a durable footprint; nothing is chosen')
            m = migration_recover(fp)
            if m['action'] == 'RESUME-COMMIT':
                return dict(base, action='RESUME-COMMIT', journalStateAfter='DONE', reacquire=lease_set, fromStep=m['fromStep'], rationale=m['rationale'])
            if m['action'] == 'ABORT':
                return dict(base, action='ABORT', journalStateAfter='ABORTED', reacquire=lease_set, rationale=m['rationale'])
            if m['action'] == 'DONE':
                return dict(base, action='RELEASE-ONLY', journalStateAfter='DONE', reacquire=lease_set, rationale=m['rationale'])
            return dict(base, action='QUARANTINE', refusal='MIGRATION.CORRUPT', d9=d9('MIGRATION.CORRUPT'), reacquire=lease_set, rationale=m['rationale'])
        return dict(base, action='ABORT', journalStateAfter='ABORTED', reacquire=lease_set, rationale=why)
    return dict(base, action=action, journalStateAfter=after, reacquire=lease_set, rationale=why)


# =============================================================================================
# S10 - Execution principal `repository-code` (joined to native AuthorizedExecutionV2 and workflow securityGrantRef)
# =============================================================================================
PRINCIPAL_CLASSES = ('first-party', 'repository-code', 'imported-artifact')
EXEC_CLASSES = ('build-script', 'proc-macro', 'test-runner')
EFFECTS = ('subprocess', 'filesystemWrite', 'network', 'environment')
ENFORCEMENT_V1 = ('DISCLOSURE-ONLY', 'ENFORCED-BY-CONSTRUCTION', 'ENFORCED-AT-HOST-BROKER')  # or ENFORCED-PLATFORM:<primitiveId>
# Security owner's platform truth table for the repository-code principal (child-process mode). Values
# are DESIGN SELECTIONS joined from permission-truth-tables.v9 semantics; no platform primitive is measured here.
PLATFORM_TRUTH_TABLE = {
    p: {'subprocess': 'DISCLOSURE-ONLY', 'filesystemWrite': 'DISCLOSURE-ONLY', 'network': 'DISCLOSURE-ONLY', 'environment': 'ENFORCED-BY-CONSTRUCTION'}
    for p in PLATFORM_IDS   # the same four machine ids that key the S8 population; a display alias has no row
}
PRINCIPAL_ALIASES = {
    # display / contract-local names -> the one foundation semantic-grant principal kind (identity-schemas.v2 `semantic-grant`)
    'P-TRUSTED-REPO': 'trusted-repository-code',     # workflows-and-surfaces section 7 / test-execution schema
    'repository-code': 'trusted-repository-code',    # native-evidence section 5 AuthorizedExecutionV2.principalClass
}
GRANT2_KEYS = {'grantSchema', 'principalClass', 'semanticPrincipalKind', 'projectId', 'snapshotId', 'argvDigest', 'executionClass',
               'owners', 'ownerSourceDigest', 'runner', 'dependencySourceSetId', 'toolClosureId', 'platformId', 'effects',
               'authorization', 'expiry', 'inherited'}
OWNER_KEYS = {'ownerKey', 'source', 'ownerFileManifestSha256'}
OWNER_SOURCES = ('snapshot-member', 'dependency-closure-member')
RUNNER_KINDS = ('toolchain-closure', 'snapshot-member')
CLOSURE_ID_RE = re.compile(r'^closure2:[0-9a-f]{64}$')
REPAIR_PLAN_ID_RE = re.compile(r'^repairplan2:[0-9a-f]{64}$')


def admit_repo_execution_grant(grant, ctx):
    """RepoExecutionGrantV2 admission (supersedes the V1 draft record, which is retained in the schema bundle
    as superseded and admitted by nothing).

    ctx = {ci, projectId, snapshotId, argvDigest, policyAdmitsRepositoryCode,
           snapshotOwners: {ownerKey: ownerFileManifestSha256}     -- sealed snapshot members that may own execution
           dependencyClosure: {dependencySourceSetId, owners: {ownerKey: ownerFileManifestSha256}}  -- SEALED DependencySourceSetV1
           toolClosure: {closureId, members: [...]},              -- sealed first-party toolchain closure (bundled cargo, rustc, linker, test runner)
           ownerSourceDigest,                                     -- host-computed raw SHA-256 of canonical sorted closed owner rows (retained blob)
           truthTable}

    OPERATIONAL admission, before any Plan exists (post-reset review SHOULD-2). A grant authorizes one operational
    step: native preparation (build-script / proc-macro owners) or a workflow test-execution step (test-runner).
    Preparation precedes analysis and a test-execution step has no Plan at all, so NO Plan semantic-grant projection
    is an admission input here; a ctx `semanticGrantPrincipals` entry is ignored, never consulted (it would be a
    fabricated authority condition). The Plan-time join is the separate `admit_plan_execution_projection`: when a
    later analysis consumes prepared outputs produced under grants, its plan2 semantic-grant must project exactly
    the `trusted-repository-code` principals of those consumed preparation grants (`semantic_projection_for_grants`).
    A test-runner grant is projected by nothing: its evidence enters a Plan only as an import2 payload whose
    wrapper and step receipt retain the operational securityGrantRef.

    Bindings that DO hold a test-runner grant: projectId, snapshotId, argvDigest, executionClass, the runner
    (sealed tool-closure member or sealed snapshot member), toolClosureId, platformId + truth-table effects, consent
    (interactive-explicit outside CI or a policy record), the ci flag, expiry and non-inheritance, plus the S6 live
    boundaries during the step. `owners` is `[]` for test-runner and `ownerSourceDigest` is then the digest of the
    canonical empty owner array: canonical empty-set bookkeeping that keeps the record shape uniform; it binds no
    program. The runner binding is `runner` + `toolClosureId`/snapshot membership + `argvDigest`.

    Two identities are kept apart: the foundation `semanticGrantDigest` (semantic projection inside plan2, no
    nonce/expiry/consent) and the operational `securityGrantRef` = H('security.repo-execution-grant.v2', grant)
    under the product canonicalizer (computed by the host, not here). Owners may come from the sealed snapshot
    OR from the sealed dependency closure (external crates' build scripts and proc-macros); the runner is always a
    member of the sealed tool closure for build-script/proc-macro, and a tool-closure member or a snapshot member
    for test-runner. There is no system fallback: a program outside both sealed sets is refused."""
    r = []
    base = {'result': None, 'refusals': [], 'd9': None, 'principalClass': None, 'semanticPrincipalKind': None, 'execution': None,
            'confinementClaimed': False, 'effects': None, 'ownerBinding': None,
            'revocationPath': 'journal REV (reason policy|operator|trust-revoked) via S6; process group killed in cancellation; effects before kill not enumerable',
            'identityDomain': 'security.repo-execution-grant.v2', 'semanticGrantIdentity': 'foundation semantic-grant (identity-and-evidence section 3), projected into plan2; distinct from securityGrantRef'}
    if not isinstance(grant, dict) or set(grant) != GRANT2_KEYS:
        return dict(base, result='REFUSE', refusals=['GRANT.SHAPE'], d9=d9('GRANT.REFUSED'))
    table = ctx.get('truthTable', PLATFORM_TRUTH_TABLE)
    if not (_int(grant['grantSchema']) and grant['grantSchema'] == 2):
        r.append('GRANT.SCHEMA')
    if grant['principalClass'] != 'repository-code':
        r.append('GRANT.PRINCIPAL_NOT_REPOSITORY_CODE')
    if grant['semanticPrincipalKind'] != PRINCIPAL_ALIASES['repository-code']:
        r.append('GRANT.SEMANTIC_PRINCIPAL_KIND')
    if not isinstance(grant['projectId'], str) or not PROJECT_ID_RE.match(grant['projectId']) or grant['projectId'] != ctx['projectId']:
        r.append('GRANT.PROJECT_ID_MISMATCH')
    if not isinstance(grant['snapshotId'], str) or not SNAPSHOT_ID_RE.match(grant['snapshotId']) or grant['snapshotId'] != ctx['snapshotId']:
        r.append('GRANT.SNAPSHOT_MISMATCH')
    if not isinstance(grant['argvDigest'], str) or not HEX64.match(grant['argvDigest']) or grant['argvDigest'] != ctx['argvDigest']:
        r.append('GRANT.ARGV_MISMATCH')
    cls = grant['executionClass']
    if cls not in EXEC_CLASSES:
        r.append('GRANT.EXECUTION_CLASS')
    # owners: exact validated binding to the sealed snapshot or the sealed dependency closure
    dep = ctx.get('dependencyClosure') or {}
    owners = grant['owners']
    if not isinstance(owners, list) or len(owners) > 64 or (cls in ('build-script', 'proc-macro') and not owners) or (cls == 'test-runner' and owners):
        r.append('GRANT.OWNERS_SHAPE')
    else:
        seen = set()
        for o in owners:
            if not isinstance(o, dict) or set(o) != OWNER_KEYS or o['source'] not in OWNER_SOURCES or \
                    not isinstance(o['ownerKey'], str) or not o['ownerKey'] or not isinstance(o['ownerFileManifestSha256'], str) or not HEX64.match(o['ownerFileManifestSha256']):
                r.append('GRANT.OWNERS_SHAPE')
                break
            if o['ownerKey'] in seen:
                r.append('GRANT.OWNER_DUPLICATE:' + o['ownerKey'])
                break
            seen.add(o['ownerKey'])
            pool = ctx.get('snapshotOwners', {}) if o['source'] == 'snapshot-member' else dep.get('owners', {})
            if o['ownerKey'] not in pool:
                r.append('GRANT.OWNER_NOT_IN_SEALED_SET:' + o['ownerKey'])
            elif pool[o['ownerKey']] != o['ownerFileManifestSha256']:
                r.append('GRANT.OWNER_MANIFEST_MISMATCH:' + o['ownerKey'])
    if grant['dependencySourceSetId'] is not None and (not isinstance(grant['dependencySourceSetId'], str) or not HEX64.match(grant['dependencySourceSetId'])):
        r.append('GRANT.DEPENDENCY_SET_SHAPE')
    elif any(isinstance(o, dict) and o.get('source') == 'dependency-closure-member' for o in owners if isinstance(owners, list)):
        if grant['dependencySourceSetId'] is None or grant['dependencySourceSetId'] != dep.get('dependencySourceSetId'):
            r.append('GRANT.DEPENDENCY_SET_MISMATCH')
    if not isinstance(grant['ownerSourceDigest'], str) or not HEX64.match(grant['ownerSourceDigest']) or grant['ownerSourceDigest'] != ctx.get('ownerSourceDigest'):
        r.append('GRANT.OWNER_SOURCE_DIGEST_MISMATCH')
    # runner: sealed tool closure (no system cargo/rustc/linker/shell), or a snapshot member for test-runner only
    tool = ctx.get('toolClosure') or {}
    if not isinstance(grant['toolClosureId'], str) or not CLOSURE_ID_RE.match(grant['toolClosureId']) or grant['toolClosureId'] != tool.get('closureId'):
        r.append('GRANT.TOOL_CLOSURE_MISMATCH')
    run = grant['runner']
    if not isinstance(run, dict) or set(run) != {'kind', 'member'} or run['kind'] not in RUNNER_KINDS or not isinstance(run['member'], str) or not run['member']:
        r.append('GRANT.RUNNER_SHAPE')
    elif run['kind'] == 'toolchain-closure':
        if run['member'] not in tool.get('members', ()):
            r.append('GRANT.RUNNER_NOT_IN_TOOL_CLOSURE')
    else:
        if cls != 'test-runner':
            r.append('GRANT.RUNNER_MUST_BE_TOOL_CLOSURE')
        elif run['member'] not in ctx.get('snapshotMembers', ()):
            r.append('GRANT.RUNNER_NOT_SEALED_MEMBER')
    # no Plan projection is checked here (operational admission precedes any Plan; see docstring and
    # admit_plan_execution_projection for the Plan-time join)
    plat = grant['platformId']
    row = table.get(plat)
    if plat in _ALIAS_TO_PLATFORM:
        r.append('GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID:' + _ALIAS_TO_PLATFORM[plat])
    elif row is None:
        r.append('GRANT.PLATFORM_NOT_IN_TRUTH_TABLE')
    eff = grant['effects']
    if not isinstance(eff, dict) or set(eff) != set(EFFECTS):
        r.append('GRANT.EFFECTS_SHAPE')
    elif row is not None:
        for k in EFFECTS:
            v = eff[k]
            if not isinstance(v, str) or not (v in ENFORCEMENT_V1 or v.startswith('ENFORCED-PLATFORM:')):
                r.append('GRANT.ENFORCEMENT_VOCABULARY:' + k)
            elif v != row[k]:
                r.append('GRANT.ENFORCEMENT_CLAIM_NOT_IN_TRUTH_TABLE:' + k)
    auth = grant['authorization']
    if not isinstance(auth, dict) or set(auth) != {'mode', 'policyRecordId', 'ci'} or not isinstance(auth['ci'], bool):
        r.append('GRANT.AUTHORIZATION_SHAPE')
    else:
        if auth['ci'] is not ctx['ci']:
            r.append('GRANT.CI_FLAG_MISMATCH')
        if auth['mode'] not in ('interactive-explicit', 'policy-record'):
            r.append('GRANT.AUTHORIZATION_MODE')
        elif auth['mode'] == 'policy-record':
            if not (isinstance(auth['policyRecordId'], str) and HEX64.match(auth['policyRecordId'])):
                r.append('GRANT.POLICY_RECORD_ID')
        else:
            if auth['policyRecordId'] is not None:
                r.append('GRANT.POLICY_RECORD_ID')
            if ctx['ci']:
                r.append('GRANT.CI_REQUIRES_POLICY_RECORD')
    if not ctx.get('policyAdmitsRepositoryCode', False):
        r.append('GRANT.POLICY_DOES_NOT_ADMIT_PRINCIPAL')
    if grant['expiry'] != 'operation-end':
        r.append('GRANT.EXPIRY')
    if grant['inherited'] is not False:
        r.append('GRANT.INHERITED')
    if r:
        return dict(base, result='REFUSE', refusals=r, d9=d9('GRANT.REFUSED'))
    binding = {'snapshotOwners': sorted(o['ownerKey'] for o in owners if o['source'] == 'snapshot-member'),
               'dependencyClosureOwners': sorted(o['ownerKey'] for o in owners if o['source'] == 'dependency-closure-member'),
               'runner': dict(run), 'toolClosureId': grant['toolClosureId']}
    # confinement is never claimed: the truth table holds no ENFORCED-PLATFORM/ENFORCED-AT-HOST-BROKER value for
    # this principal; an environment allowlist is construction, not confinement of the child's reach
    return dict(base, result='ADMIT', principalClass='repository-code', semanticPrincipalKind='trusted-repository-code',
                execution='disclosed-trusted-code', confinementClaimed=False, effects=dict(eff), ownerBinding=binding)


PROJECTED_EXEC_CLASSES = ('build-script', 'proc-macro')   # preparation grants: their outputs enter a later Plan


def semantic_projection_for_grants(admitted_grants):
    """The foundation semantic-grant principals a consuming analysis MUST project into its plan2 for the preparation
    grants whose outputs it consumes (`preparedResolution = host-prepared`). Input: the admitted RepoExecutionGrantV2
    records (already ADMITted by admit_repo_execution_grant; shape re-checked, decision not re-made). Output: sorted,
    duplicate-free `[{kind: 'trusted-repository-code', closureId, ownerSourceDigest}]`. Test-runner grants contribute
    nothing: a test-execution step has no Plan and its evidence is bound by the import wrapper and step receipt."""
    out = {}
    for g in admitted_grants:
        if not isinstance(g, dict) or set(g) != GRANT2_KEYS:
            raise Reject('GRANT.SHAPE')
        if g['executionClass'] not in PROJECTED_EXEC_CLASSES:
            continue
        key = (g['toolClosureId'], g['ownerSourceDigest'])
        out[key] = {'kind': PRINCIPAL_ALIASES['repository-code'], 'closureId': key[0], 'ownerSourceDigest': key[1]}
    return [out[k] for k in sorted(out)]


def admit_plan_execution_projection(plan_principals, consumed_grants, prepared_resolution):
    """Plan-time join (analysis admission, AFTER preparation). `plan_principals` is the plan2 semantic-grant
    `principals[]` (foundation record); `consumed_grants` are the admitted preparation grants whose prepared outputs
    this Plan consumes; `prepared_resolution` is the universe's `preparedResolution` (`none` | `imported-inert` |
    `host-prepared`). Rules: `host-prepared` requires the projection to carry exactly the principals of the consumed
    grants (missing -> PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED; extra trusted-repository-code principals no grant
    backs -> PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT); `imported-inert` and `none` consume no grant, so any
    trusted-repository-code principal in the projection is refused (prepared availability never implies that this
    host held a grant); a test-runner grant offered as a consumed grant refuses (PLAN.TEST_RUNNER_HAS_NO_PLAN).
    Never a projection fabricated from the grant: the projection comes from the Plan, the grants from the step
    receipts, and they must agree."""
    r = []
    if prepared_resolution not in ('none', 'imported-inert', 'host-prepared'):
        r.append('PLAN.PREPARED_RESOLUTION_UNKNOWN')
    if any(isinstance(g, dict) and g.get('executionClass') == 'test-runner' for g in consumed_grants):
        r.append('PLAN.TEST_RUNNER_HAS_NO_PLAN')
    preparation = [g for g in consumed_grants if not (isinstance(g, dict) and g.get('executionClass') == 'test-runner')]
    try:
        required = semantic_projection_for_grants(preparation)
    except Reject as e:
        r.append('PLAN.CONSUMED_GRANT_SHAPE:' + str(e))
        required = []
    projected = [p for p in plan_principals if isinstance(p, dict) and p.get('kind') == PRINCIPAL_ALIASES['repository-code']]
    proj_keys = {(p.get('closureId'), p.get('ownerSourceDigest')) for p in projected}
    req_keys = {(p['closureId'], p['ownerSourceDigest']) for p in required}
    if prepared_resolution == 'host-prepared':
        if not preparation:
            r.append('PLAN.HOST_PREPARED_WITHOUT_GRANT')
        for k in sorted(req_keys - proj_keys):
            r.append('PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED:' + k[1])
        for k in sorted(proj_keys - req_keys, key=lambda x: (x[0] or '', x[1] or '')):
            r.append('PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT:' + str(k[1]))
    else:
        if preparation:
            r.append('PLAN.GRANT_CONSUMED_WITHOUT_HOST_PREPARED')
        for k in sorted(proj_keys, key=lambda x: (x[0] or '', x[1] or '')):
            r.append('PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT:' + str(k[1]))
    base = {'result': None, 'refusals': [], 'd9': None, 'preparedResolution': prepared_resolution,
            'requiredPrincipals': required, 'projectionSource': 'plan2 semantic-grant (foundation); never derived from the grant',
            'testRunnerProjected': False}
    if r:
        return dict(base, result='REFUSE', refusals=r, d9=d9('PLAN.EXECUTION_PROJECTION_REFUSED'))
    return dict(base, result='ADMIT')


# =============================================================================================
# S10.1 - Repair apply authorization: host-brokered source mutation, NOT a repository-execution grant
# =============================================================================================
REPAIR_AUTHZ_KEYS = {'authorizationSchema', 'kind', 'projectId', 'repairPlanId', 'baseSnapshotId', 'recipeClosureId',
                     'consent', 'expiry', 'leaseMode', 'repositoryExecution'}


def admit_repair_authorization(authz, ctx):
    """RepairApplyAuthorizationV1 admission. Identity H('security.repair-apply-authorization.v1', authz) is the
    workflow `RepairApplyParams.authorizationRef`. It binds one repair plan, one base snapshot, the recipe's
    signed closure and an explicit consent; it grants brokered first-party source mutation under the EXCLUSIVE
    lease and never repository execution. Live revocation: every brokered write re-reads the trust epoch (S6
    authority checkpoint); a revoked recipe closure at any checkpoint is REV(trust-revoked) with postimage-
    checked rollback. ctx = {projectId, repairPlanId, baseSnapshotId, ci, liveTreeEqualsBase, revokedClosures,
    policyAdmitsRepair, recipeClosureId, admittedClosures}. The expected recipe
    comes from the rehashed repair plan, and admittedClosures from current signed
    closure admission; absence from revocations alone is insufficient."""
    r = []
    base = {'result': None, 'refusals': [], 'd9': None, 'grantsRepositoryExecution': False, 'leaseMode': None,
            'identityDomain': 'security.repair-apply-authorization.v1',
            'revocationPath': 'authority checkpoint before every brokered write; REV(trust-revoked) with postimage-checked rollback (S6)'}
    if not isinstance(authz, dict) or set(authz) != REPAIR_AUTHZ_KEYS:
        return dict(base, result='REFUSE', refusals=['AUTHZ.SHAPE'], d9=d9('GRANT.REFUSED'))
    if not (_int(authz['authorizationSchema']) and authz['authorizationSchema'] == 1) or authz['kind'] != 'repair-apply':
        r.append('AUTHZ.SHAPE')
    if not isinstance(authz['projectId'], str) or not PROJECT_ID_RE.match(authz['projectId']) or authz['projectId'] != ctx['projectId']:
        r.append('AUTHZ.PROJECT_ID_MISMATCH')
    if not isinstance(authz['repairPlanId'], str) or not REPAIR_PLAN_ID_RE.match(authz['repairPlanId']) or authz['repairPlanId'] != ctx['repairPlanId']:
        r.append('AUTHZ.REPAIR_PLAN_MISMATCH')
    if not isinstance(authz['baseSnapshotId'], str) or not SNAPSHOT_ID_RE.match(authz['baseSnapshotId']) or authz['baseSnapshotId'] != ctx['baseSnapshotId']:
        r.append('AUTHZ.BASE_SNAPSHOT_MISMATCH')
    if not isinstance(authz['recipeClosureId'], str) or not CLOSURE_ID_RE.match(authz['recipeClosureId']):
        r.append('AUTHZ.RECIPE_CLOSURE_SHAPE')
    elif authz['recipeClosureId'] in ctx.get('revokedClosures', ()):
        r.append('AUTHZ.RECIPE_CLOSURE_REVOKED')
    elif authz['recipeClosureId'] != ctx.get('recipeClosureId'):
        r.append('AUTHZ.RECIPE_CLOSURE_MISMATCH')
    elif authz['recipeClosureId'] not in ctx.get('admittedClosures', ()):
        r.append('AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED')
    c = authz['consent']
    if not isinstance(c, dict) or set(c) != {'mode', 'policyRecordId', 'ci'} or not isinstance(c['ci'], bool):
        r.append('AUTHZ.CONSENT_SHAPE')
    else:
        if c['ci'] is not ctx['ci']:
            r.append('AUTHZ.CI_FLAG_MISMATCH')
        if c['mode'] not in ('interactive-explicit', 'policy-record'):
            r.append('AUTHZ.CONSENT_MODE')
        elif c['mode'] == 'policy-record':
            if not (isinstance(c['policyRecordId'], str) and HEX64.match(c['policyRecordId'])):
                r.append('AUTHZ.POLICY_RECORD_ID')
        else:
            if c['policyRecordId'] is not None:
                r.append('AUTHZ.POLICY_RECORD_ID')
            if ctx['ci']:
                r.append('AUTHZ.CI_REQUIRES_POLICY_RECORD')
    if authz['expiry'] != 'operation-end':
        r.append('AUTHZ.EXPIRY')
    if authz['leaseMode'] != 'EXCLUSIVE':
        r.append('AUTHZ.LEASE_MODE')
    if authz['repositoryExecution'] is not False:
        r.append('AUTHZ.REPOSITORY_EXECUTION_NOT_GRANTABLE_HERE')
    if not ctx.get('policyAdmitsRepair', False):
        r.append('AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR')
    if ctx.get('liveTreeEqualsBase') is not True:
        r.append('AUTHZ.SOURCE_MOVED')
    if r:
        code = 'TRUST.COMPONENT_REVOKED_DURING_OPERATION' if 'AUTHZ.RECIPE_CLOSURE_REVOKED' in r else 'GRANT.REFUSED'
        return dict(base, result='REFUSE', refusals=r, d9=d9(code))
    return dict(base, result='ADMIT', leaseMode='EXCLUSIVE')


# =============================================================================================
# S10.2 - Repair RECOVERY authorization (post-reset review v2, P9): a separately authorized mutation within the
#         ORIGINAL plan's authority; never repository execution, never a new edit, never a broader plan
# =============================================================================================
RECOVERY_AUTHZ_DOMAIN = 'security.repair-recovery-authorization.v1'
JOURNAL_IDENTITY_DOMAIN = 'security.repair-apply-journal-identity.v1'
RECOVERY_AUTHZ_KEYS = {'authorizationSchema', 'kind', 'projectId', 'repairPlanId', 'baseSnapshotId', 'recipeClosureId',
                       'journalRef', 'journalState', 'observedJournalStateDigest', 'recoveryAction', 'originalRequestId',
                       'recoveryRequestId', 'recoveryExecutionId', 'consent', 'issuedAt', 'expiresAt', 'leaseMode',
                       'mutationBoundary', 'repositoryExecution', 'newEdits'}
JOURNAL_STATES = ('PREPARING', 'STAGED', 'APPLYING', 'APPLIED', 'COMMITTED', 'FAILED_CLEAN', 'FAILED_ROLLED_BACK', 'RECOVERY_BLOCKED', 'INDETERMINATE')
# The finite recovery actions a journal state admits (mirror of the workflow repair recovery table's MUTATING rows;
# the integration check asserts the two tables agree). Terminal states admit no mutation: inspection only.
RECOVERY_ACTION_FOR_STATE = {'PREPARING': 'discard-temps', 'STAGED': 'discard-temps', 'APPLYING': 'roll-back-renamed',
                             'APPLIED': 'verify-postimages-and-commit', 'INDETERMINATE': 'verify-postimages-and-commit'}
RECOVERY_ACTIONS = ('discard-temps', 'roll-back-renamed', 'verify-postimages-and-commit')
# Safe rollback/cleanup restores retained preimages or discards temps: it must be possible AFTER the recipe was revoked
# (that is what revocation rollback is). Commit re-executes the revoked-or-not recipe's postimages: it re-consults trust.
RECOVERY_COMMIT_ACTIONS = ('verify-postimages-and-commit',)
RECOVERY_AUTHZ_MAX_LIFETIME_S = 1 * DAY
# Noncircular journal identity: only the fields fixed when the apply journal was created (never `state`, paths, blobs,
# blocked/restore lists or any recoveryAuthorizationRef the journal later carries).
JOURNAL_IDENTITY_KEYS = ('schemaFamily', 'schemaMajor', 'requestId', 'stepId', 'executionId', 'repairPlanId', 'baseSnapshotId', 'authorizationRef')
# Observed journal state: the mutable recovery-relevant fields as READ under the EXCLUSIVE lease before any recovery
# write. Every successful recovery mutation changes `state`, so a retained authorization cannot be replayed after one;
# An unchanged digest permits continuation only inside the same admitted execution/lifetime. A process crash requires a fresh execution and authorization.
JOURNAL_STATE_KEYS = ('state', 'stagedPaths', 'appliedPaths', 'preimageBlobs')
REQUEST_ID_RE = re.compile(r'^req1_[0-9a-f]{32}$')
EXECUTION_ID_RE = re.compile(r'^exec1_[0-9a-f]{32}$')
REPAIR_RECOVERY_TCB = ['`ctx.journal` is the RepairApplyJournalV1 the host read under the EXCLUSIVE lease before any recovery write (asserted)',
                '`ctx.admittedTime` is an S4 PROCEED evaluation time (asserted); `ctx.custodyAdmitted` is the S3 re-run for this invocation',
                '`ctx.recipeClosureId` comes from the rehashed repair plan; `ctx.admittedClosures`/`revokedClosures` from current signed-closure admission']


def repair_journal_identity(journal):
    """`security.repair-apply-journal-identity.v1:<hex>` over the closed identity preimage (JOURNAL_IDENTITY_KEYS).
    Noncircular by construction: the preimage excludes every field recovery may write."""
    if not isinstance(journal, dict):
        raise Reject('JOURNAL_SHAPE')
    missing = [k for k in JOURNAL_IDENTITY_KEYS if k not in journal]
    if missing:
        raise Reject('JOURNAL_IDENTITY_KEYS:' + ','.join(missing))
    return JOURNAL_IDENTITY_DOMAIN + ':' + _C.identity(JOURNAL_IDENTITY_DOMAIN, {k: journal[k] for k in JOURNAL_IDENTITY_KEYS})


def repair_journal_state_digest(journal):
    """Raw SHA-256 of the canonical observed journal state {state, stagedPaths, appliedPaths, preimageBlobs} (product data)."""
    if not isinstance(journal, dict) or 'state' not in journal:
        raise Reject('JOURNAL_SHAPE')
    pre = {'state': journal['state'], 'stagedPaths': journal.get('stagedPaths', []), 'appliedPaths': journal.get('appliedPaths', []),
           'preimageBlobs': journal.get('preimageBlobs', [])}
    return hashlib.sha256(_C.canonical(pre)).hexdigest()


def admit_recovery_authorization(authz, ctx):
    """RepairRecoveryAuthorizationV1 admission (S10.2). Identity H('security.repair-recovery-authorization.v1', authz) is
    the workflow `RepairApplyJournalV1.recoveryAuthorizationRef` (full reference, never a truncated prefix).

    TRUSTED CONTEXT INPUTS (each a host observation, none supplied by the caller of `repair recover`):
      projectId, repairPlanId, baseSnapshotId  -- the admitted project and the rehashed original repair plan
      journal                                  -- RepairApplyJournalV1 as read under the EXCLUSIVE lease before any write
      recoveryRequestId, recoveryExecutionId   -- the FRESH recovery invocation (its own RequestId/ExecutionId)
      ci                                       -- the invocation's real CI flag
      admittedTime                             -- S4 PROCEED evaluation time; None = no admitted time context
      custodyAdmitted                          -- S3 discovery re-run on this invocation admitted the project root and targets
      policyAdmitsRepair                       -- project policy admits repair (recovery is inside the repair policy)
      recipeClosureId, revokedClosures, admittedClosures -- current signed-closure trust for the plan's recipe

    Bindings (all must hold): project, exact original plan and base snapshot; exact journal identity (noncircular
    preimage) and the observed journal state digest (single use / crash-safe resume); the finite requested action equals
    the one the journal state admits (terminal states admit none: inspection is read-only and needs no authorization);
    the original request id equals the journal's and the recovery request/attempt is the fresh one; consent
    (interactive-explicit outside CI, policy-record in CI); an admitted time inside [issuedAt, expiresAt] with the lifetime
    bounded (24 h); EXCLUSIVE lease and the host-broker mutation boundary; `repositoryExecution`, `newEdits` constant
    false (recovery cannot grant repository code execution, new edits or a broader plan). Rollback/cleanup never consults
    recipe trust (a revoked recipe must still be rolled back); commit re-consults it and a revoked recipe refuses first.
    The workflow recovery table's guarded preimage/postimage law is mandatory and is never waived by this record."""
    r = []
    base = {'result': None, 'refusals': [], 'd9': None, 'grantsRepositoryExecution': False, 'grantsNewEdits': False,
            'planScope': 'original-plan-only', 'leaseMode': None, 'mutationBoundary': None, 'action': None,
            'recipeTrustConsulted': None, 'journalRef': None, 'journalStateDigest': None, 'identityDomain': RECOVERY_AUTHZ_DOMAIN,
            'inspection': 'read-only; needs no authorization',
            'preimagePostimageLaw': 'mandatory: every target must be at its plan preimage or postimage before any restore/commit (workflow recovery table); never waived here',
            'replaySemantics': 'single use: successful recovery changes the observed state digest; unchanged state may continue only in the same admitted execution/lifetime; a fresh execution requires a fresh authorization',
            'revocationPath': 'authority checkpoint before every brokered write; rollback/cleanup proceeds under a revoked recipe; commit refuses AUTHZ.RECIPE_CLOSURE_REVOKED (S6)',
            'trustedContextInputs': ['projectId', 'repairPlanId', 'baseSnapshotId', 'journal', 'recoveryRequestId', 'recoveryExecutionId', 'ci',
                                     'admittedTime', 'custodyAdmitted', 'policyAdmitsRepair', 'recipeClosureId', 'revokedClosures', 'admittedClosures']}
    if not isinstance(authz, dict) or set(authz) != RECOVERY_AUTHZ_KEYS:
        return dict(base, result='REFUSE', refusals=['AUTHZ.SHAPE'], d9=d9('GRANT.REFUSED'))
    if not (_int(authz['authorizationSchema']) and authz['authorizationSchema'] == 1) or authz['kind'] != 'repair-recover':
        r.append('AUTHZ.SHAPE')
    if not isinstance(authz['projectId'], str) or not PROJECT_ID_RE.match(authz['projectId']) or authz['projectId'] != ctx['projectId']:
        r.append('AUTHZ.PROJECT_ID_MISMATCH')
    if not isinstance(authz['repairPlanId'], str) or not REPAIR_PLAN_ID_RE.match(authz['repairPlanId']) or authz['repairPlanId'] != ctx['repairPlanId']:
        r.append('AUTHZ.REPAIR_PLAN_MISMATCH')
    if not isinstance(authz['baseSnapshotId'], str) or not SNAPSHOT_ID_RE.match(authz['baseSnapshotId']) or authz['baseSnapshotId'] != ctx['baseSnapshotId']:
        r.append('AUTHZ.BASE_SNAPSHOT_MISMATCH')
    if not isinstance(authz['recipeClosureId'], str) or not CLOSURE_ID_RE.match(authz['recipeClosureId']):
        r.append('AUTHZ.RECIPE_CLOSURE_SHAPE')
    elif authz['recipeClosureId'] != ctx.get('recipeClosureId'):
        r.append('AUTHZ.RECIPE_CLOSURE_MISMATCH')
    # exact journal binding: identity (noncircular) + observed state (single use)
    journal = ctx.get('journal')
    journal_ref = state_digest = None
    try:
        journal_ref = repair_journal_identity(journal)
        state_digest = repair_journal_state_digest(journal)
    except Reject as e:
        r.append('AUTHZ.JOURNAL_CONTEXT:' + str(e))
    if journal_ref is not None:
        if journal.get('repairPlanId') != ctx['repairPlanId'] or journal.get('baseSnapshotId') != ctx['baseSnapshotId']:
            r.append('AUTHZ.JOURNAL_NOT_OF_THIS_PLAN')
        if authz['journalRef'] != journal_ref:
            r.append('AUTHZ.JOURNAL_MISMATCH')
        if authz['journalState'] not in JOURNAL_STATES:
            r.append('AUTHZ.JOURNAL_STATE_UNKNOWN')
        elif authz['journalState'] != journal['state']:
            r.append('AUTHZ.JOURNAL_STATE_MISMATCH')
        if authz['observedJournalStateDigest'] != state_digest:
            r.append('AUTHZ.JOURNAL_STATE_MOVED')
        admitted_action = RECOVERY_ACTION_FOR_STATE.get(journal['state'])
        if admitted_action is None:
            r.append('AUTHZ.RECOVERY_NOT_MUTATING:' + str(journal['state']))
        elif authz['recoveryAction'] not in RECOVERY_ACTIONS:
            r.append('AUTHZ.RECOVERY_ACTION_UNKNOWN')
        elif authz['recoveryAction'] != admitted_action:
            r.append('AUTHZ.RECOVERY_ACTION_MISMATCH')
        if authz['originalRequestId'] != journal.get('requestId'):
            r.append('AUTHZ.ORIGINAL_REQUEST_MISMATCH')
    # the recovery attempt is a fresh request, never the original apply request
    for k, rx in (('originalRequestId', REQUEST_ID_RE), ('recoveryRequestId', REQUEST_ID_RE), ('recoveryExecutionId', EXECUTION_ID_RE)):
        if not isinstance(authz[k], str) or not rx.match(authz[k]):
            r.append('AUTHZ.REQUEST_ID_SHAPE:' + k)
    if authz['recoveryRequestId'] != ctx.get('recoveryRequestId') or authz['recoveryExecutionId'] != ctx.get('recoveryExecutionId'):
        r.append('AUTHZ.RECOVERY_REQUEST_MISMATCH')
    if authz['recoveryRequestId'] == authz['originalRequestId']:
        r.append('AUTHZ.RECOVERY_REQUEST_NOT_FRESH')
    if isinstance(journal, dict) and authz['recoveryExecutionId'] == journal.get('executionId'):
        r.append('AUTHZ.RECOVERY_EXECUTION_NOT_FRESH')
    c = authz['consent']
    if not isinstance(c, dict) or set(c) != {'mode', 'policyRecordId', 'ci'} or not isinstance(c['ci'], bool):
        r.append('AUTHZ.CONSENT_SHAPE')
    else:
        if c['ci'] is not ctx['ci']:
            r.append('AUTHZ.CI_FLAG_MISMATCH')
        if c['mode'] not in ('interactive-explicit', 'policy-record'):
            r.append('AUTHZ.CONSENT_MODE')
        elif c['mode'] == 'policy-record':
            if not (isinstance(c['policyRecordId'], str) and HEX64.match(c['policyRecordId'])):
                r.append('AUTHZ.POLICY_RECORD_ID')
        else:
            if c['policyRecordId'] is not None:
                r.append('AUTHZ.POLICY_RECORD_ID')
            if ctx['ci']:
                r.append('AUTHZ.CI_REQUIRES_POLICY_RECORD')
    # time: admitted time inside a bounded, finite lifetime
    now = ctx.get('admittedTime')
    try:
        issued, expires = ts(authz['issuedAt']), ts(authz['expiresAt'])
    except Reject:
        issued = expires = None
        r.append('AUTHZ.TIME_GRAMMAR')
    if issued is not None:
        if expires <= issued or expires - issued > RECOVERY_AUTHZ_MAX_LIFETIME_S:
            r.append('AUTHZ.LIFETIME_BOUND')
        if now is None:
            r.append('AUTHZ.NO_ADMITTED_TIME_CONTEXT')
        else:
            t = ts(now)
            if t < issued:
                r.append('AUTHZ.NOT_YET_VALID')
            elif t > expires:
                r.append('AUTHZ.EXPIRED')
    if authz['leaseMode'] != 'EXCLUSIVE':
        r.append('AUTHZ.LEASE_MODE')
    if authz['mutationBoundary'] != 'host-broker':
        r.append('AUTHZ.MUTATION_BOUNDARY')
    if authz['repositoryExecution'] is not False:
        r.append('AUTHZ.REPOSITORY_EXECUTION_NOT_GRANTABLE_HERE')
    if authz['newEdits'] is not False:
        r.append('AUTHZ.NEW_EDITS_NOT_GRANTABLE_HERE')
    if not ctx.get('policyAdmitsRepair', False):
        r.append('AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR')
    if ctx.get('custodyAdmitted') is not True:
        r.append('AUTHZ.CUSTODY_NOT_ADMITTED')
    # recipe trust: consulted only when recovery would COMMIT the recipe's postimages
    consult = authz['recoveryAction'] in RECOVERY_COMMIT_ACTIONS
    if consult and 'AUTHZ.RECIPE_CLOSURE_SHAPE' not in r:
        if authz['recipeClosureId'] in ctx.get('revokedClosures', ()):
            r.append('AUTHZ.RECIPE_CLOSURE_REVOKED')
        elif authz['recipeClosureId'] not in ctx.get('admittedClosures', ()):
            r.append('AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED')
    if r:
        code = 'TRUST.COMPONENT_REVOKED_DURING_OPERATION' if 'AUTHZ.RECIPE_CLOSURE_REVOKED' in r else 'GRANT.REFUSED'
        return dict(base, result='REFUSE', refusals=r, d9=d9(code), recipeTrustConsulted=consult, journalRef=journal_ref, journalStateDigest=state_digest)
    return dict(base, result='ADMIT', leaseMode='EXCLUSIVE', mutationBoundary='host-broker', action=authz['recoveryAction'],
                recipeTrustConsulted=consult, journalRef=journal_ref, journalStateDigest=state_digest)


# =============================================================================================
# S9.1 - Root schema 2 and the signed profile-set envelope (input admission; design, not release qualification)
# =============================================================================================
ROLE_NAMES_1 = ('TR-CORE', 'TR-INDEX', 'TR-COMPONENT', 'TR-BUNDLE', 'TR-REPAIR')
ROLE_NAMES_2 = ROLE_NAMES_1 + ('TR-PROFILE',)
ROOT2_KEYS = {'rootSchema', 'rootVersion', 'previousRootVersion', 'issuedAt', 'expiresAt', 'keys', 'rootKeys', 'rootThreshold',
              'roles', 'recoveryAuthority', 'kernelAttestationKeys', 'indexOrigin'}
ENVELOPE_KINDS = {  # opensip-signature-envelope.2 `kind` -> (body schema, digest domain, signing authority)
    'root': ('RootV1|RootV2', 'opensip.metadata.root.<rootSchema>', 'previous rootKeys@rootThreshold AND own rootKeys@rootThreshold (S5)'),
    'catalog': ('catalog v8', 'opensip.metadata.catalog.1', 'TR-INDEX keys@threshold'),
    'revocation': ('revocation v8', 'opensip.metadata.revocation.1', 'TR-INDEX keys@threshold'),
    'trust-recovery-epoch': ('TrustRecoveryEpochV1', 'opensip.metadata.recovery-epoch.1', 'recoveryAuthority.keys@threshold (S4.5)'),
    'platform-profile-set': ('PlatformProfileSetV1', 'opensip.metadata.platform-profile-set.1', 'schema-2 TR-PROFILE keys@threshold; under a schema-1 root only as a TR-CORE-namespace member of the signed core release'),
}


def _key_list(v, lo, hi):
    return isinstance(v, list) and lo <= len(v) <= hi and all(isinstance(k, str) and HEX64.match(k) for k in v) and len(set(v)) == len(v)


def admit_root_document(root, reader_schemas=(1,)):
    """Closed shape + semantic rules for root schema 1 (byte-identical to security-schemas.v8/root.schema.json) and
    schema 2 (the exact extension recipe of S9.1). Returns a typed refusal; a schema-2 root under a {1}-only reader
    is ROOT.SCHEMA_UNSUPPORTED (typed, state unchanged), not corruption. Constants are exact-typed (true is not 1)."""
    out = {'result': None, 'refusal': None, 'detail': None, 'd9': None, 'rootSchema': None, 'roles': None, 'recoveryAuthority': None,
           'kernelAttestationKeys': None, 'profileSetAuthority': None}

    def refuse(refusal, detail):
        out.update(result='REFUSE', refusal=refusal, detail=detail, d9=d9(refusal) if refusal in D9 else d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out

    if not isinstance(root, dict) or set(root) != ROOT2_KEYS:
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.SHAPE')
    sch = root['rootSchema']
    if not _int(sch) or sch not in (1, 2):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.SCHEMA_CONSTANT_TYPE')
    if sch not in reader_schemas:
        return refuse('ROOT.SCHEMA_UNSUPPORTED', 'rootSchema %d not in reader set %s' % (sch, sorted(reader_schemas)))
    out['rootSchema'] = sch
    try:validate_input('RootV'+str(sch),root);canon(root)
    except (ValueError,Reject,_C.ValidationError):return refuse('PAYLOAD-NOT-ADMISSIBLE','ROOT.SCHEMA_SHAPE')
    for k in ('rootVersion',):
        if not (_int(root[k]) and 1 <= root[k] <= 2**63 - 1):
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.VERSION_TYPE')
    if root['previousRootVersion'] is not None and not (_int(root['previousRootVersion']) and 1 <= root['previousRootVersion'] < root['rootVersion']):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.PREVIOUS_VERSION')
    try:
        if ts(root['issuedAt']) >= ts(root['expiresAt']):
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ISSUE_NOT_BEFORE_EXPIRY')
    except Reject:
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.TIMESTAMP_GRAMMAR')
    keys = root['keys']
    if not isinstance(keys, list) or not (1 <= len(keys) <= 64) or any(not isinstance(k, dict) or set(k) != {'keyId', 'publicKey', 'label'} for k in keys):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.KEYS_SHAPE')
    known = [k['keyId'] for k in keys]
    if len(set(known)) != len(known) or any(not (isinstance(i, str) and HEX64.match(i)) for i in known):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.KEY_ID')
    if not _key_list(root['rootKeys'], 3, 8) or not (_int(root['rootThreshold']) and 2 <= root['rootThreshold'] <= len(root['rootKeys'])):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ROOT_KEYS')
    ra = root['recoveryAuthority']
    if not isinstance(ra, dict) or set(ra) != {'keys', 'threshold'} or not _key_list(ra['keys'], 5, 16) or \
            not (_int(ra['threshold']) and 3 <= ra['threshold'] <= len(ra['keys'])):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.RECOVERY_AUTHORITY')
    roles = root['roles']
    expected_roles = ROLE_NAMES_1 if sch == 1 else ROLE_NAMES_2
    if not isinstance(roles, dict) or set(roles) != set(expected_roles):
        return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ROLE_SET:%s' % sch)
    used = [('rootKeys', list(root['rootKeys'])), ('recoveryAuthority', list(ra['keys']))]
    for name, role in roles.items():
        if not isinstance(role, dict) or set(role) - {'standing'} != {'keys', 'threshold', 'namespaces'} or not _key_list(role['keys'], 0, 8) or \
                not (_int(role['threshold']) and 0 <= role['threshold'] <= 8) or not isinstance(role['namespaces'], list):
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ROLE_SHAPE:' + name)
        if role['keys'] and role['threshold'] < 1:
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ROLE_THRESHOLD:' + name)
        if role['threshold'] > len(role['keys']):
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.ROLE_THRESHOLD:' + name)
        used.append((name, list(role['keys'])))
    if sch == 1:
        if roles['TR-REPAIR']['keys'] or roles['TR-REPAIR']['threshold'] != 0 or roles['TR-REPAIR'].get('standing') == 'active':
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.TR_REPAIR_ACTIVE_UNDER_SCHEMA_1')
        if root['kernelAttestationKeys'] != []:
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.KERNEL_ATTESTATION_KEYS_NOT_EMPTY')
    else:
        for name in ('TR-REPAIR', 'TR-PROFILE'):
            role = roles[name]
            if role['keys']:
                if role['threshold'] < 2 or len(role['keys']) < role['threshold'] + 1 or not role['namespaces']:
                    return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.%s_THRESHOLD_POLICY' % name.replace('-', '_'))
        if not _key_list(root['kernelAttestationKeys'], 0, 8):
            return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.KERNEL_ATTESTATION_KEYS')
        used.append(('kernelAttestationKeys', list(root['kernelAttestationKeys'])))
    seen = {}
    for where, lst in used:
        for k in lst:
            if k not in known:
                return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.UNKNOWN_KEY:%s' % where)
            if k in seen and seen[k] != where:
                return refuse('PAYLOAD-NOT-ADMISSIBLE', 'ROOT.KEY_REUSE:%s:%s' % (seen[k], where))
            seen[k] = where
    out.update(result='ACCEPT', roles=sorted(roles), recoveryAuthority={'keys': len(ra['keys']), 'threshold': ra['threshold']},
               kernelAttestationKeys=len(root['kernelAttestationKeys']),
               profileSetAuthority=('TR-PROFILE' if sch == 2 and roles['TR-PROFILE']['keys'] else 'core-release-embedded-only'))
    return out


def admit_profile_set_envelope(envelope, accepted_root, signers, revoked_keys=(), selected_profile_digest=None):
    """Standalone signed PlatformProfileSetV1 admission under opensip-signature-envelope.2 kind
    `platform-profile-set`. Under a schema-2 root with an active TR-PROFILE role the signers must reach that
    role's threshold (revoked keys excluded); under a schema-1 root (no TR-PROFILE) a standalone document is
    refused typed and only the copy embedded in the signed core release is used. Body digest domain
    `opensip.metadata.platform-profile-set.1` under the metadata profile."""
    out = {'result': None, 'refusal': None, 'detail': None, 'd9': None, 'authority': None, 'bodyDigest': None}
    if not isinstance(envelope, dict) or set(envelope) != {'envelopeSchema', 'kind', 'body', 'bodyDigest'}:
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='ENVELOPE.SHAPE', d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    if not (_int(envelope['envelopeSchema']) and envelope['envelopeSchema'] == 2) or envelope['kind'] != 'platform-profile-set':
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='ENVELOPE.KIND', d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    body = envelope['body']
    try:validate_input('PlatformProfileSetEnvelopeV1',envelope);canon(body)
    except (ValueError,Reject,_C.ValidationError):
        out.update(result='REFUSE',refusal='PAYLOAD-NOT-ADMISSIBLE',detail='PROFILE_SET.SCHEMA_SHAPE',d9=d9('PAYLOAD-NOT-ADMISSIBLE'));return out
    if not isinstance(body, dict) or body.get('profileSetSchema') != 1 or not _int(body.get('profileSetSchema')):
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='PROFILE_SET.SCHEMA', d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    try:
        digest = metadata_sha('opensip.metadata.platform-profile-set.1', body)
    except Reject as e:
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='PROFILE_SET.CANON:' + str(e), d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    out['bodyDigest'] = digest
    if envelope['bodyDigest'] != digest:
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='ENVELOPE.BODY_DIGEST', d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    if selected_profile_digest is None or digest != selected_profile_digest:
        out.update(result='REFUSE',refusal='PAYLOAD-NOT-ADMISSIBLE',detail='PROFILE_SET.CORE_PIN_MISMATCH',d9=d9('PAYLOAD-NOT-ADMISSIBLE'));return out
    role = (accepted_root.get('roles') or {}).get('TR-PROFILE')
    if accepted_root.get('rootSchema') != 2 or not role or not role.get('keys'):
        out.update(result='REFUSE', refusal='ROOT.SCHEMA_UNSUPPORTED', detail='PROFILE_SET.NO_TR_PROFILE_ROLE:core-release-embedded-copy-only', d9=d9('ROOT.SCHEMA_UNSUPPORTED'))
        return out
    ok = (set(signers) & set(role['keys'])) - set(revoked_keys)
    if len(ok) < role['threshold']:
        out.update(result='REFUSE', refusal='PAYLOAD-NOT-ADMISSIBLE', detail='PROFILE_SET.SIGNATURE_THRESHOLD', d9=d9('PAYLOAD-NOT-ADMISSIBLE'))
        return out
    out.update(result='ACCEPT', authority='TR-PROFILE@%d' % role['threshold'])
    return out


# =============================================================================================
# S3.1 - Backup-custody choice before the first source-derived write (identity-and-evidence section 5, TM V17)
# =============================================================================================
def storage_write_admission(backup_status, allow_backup_custody, admitted_policy_record, ci, ephemeral):
    """First source-derived write into a project store. `backup_status` is the host's classification of the
    storage root (BACKED_UP | NOT_BACKED_UP | UNKNOWN, an asserted OS read). A detected backed-up root needs an
    explicit choice: --allow-backup-custody for this invocation, or an already-admitted storage-policy record;
    ephemeral mode needs none. Nothing here writes a policy file or changes any root identity."""
    if backup_status not in ('BACKED_UP', 'NOT_BACKED_UP', 'UNKNOWN'):
        raise Reject('BACKUP_STATUS_VOCABULARY')
    out = {'result': None, 'refusal': None, 'detail': None, 'd9': None, 'choice': None, 'policyFileWritten': False, 'rootIdentityChanged': False,
           'disclosure': 'UNKNOWN is disclosed as unknown, never as not-backed-up; an acknowledgement is not a network-export or shared-storage grant'}
    if ephemeral:
        out.update(result='ADMIT', choice='ephemeral')
        return out
    if backup_status in ('NOT_BACKED_UP','UNKNOWN'):
        out.update(result='ADMIT', choice='unknown-disclosed' if backup_status=='UNKNOWN' else 'not-required')
        return out
    if allow_backup_custody is True:
        out.update(result='ADMIT', choice='invocation-flag')
        return out
    if isinstance(admitted_policy_record, str) and HEX64.match(admitted_policy_record):
        out.update(result='ADMIT', choice='admitted-policy-record:' + admitted_policy_record)
        return out
    out.update(result='REFUSE', refusal='REQUEST.PRECONDITION_FAILED', detail='storage.backup-choice-required',
               d9={'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.PRECONDITION_FAILED'},
               choice='interactive-prompt-unavailable' if ci else 'interactive-choice-required')
    return out


# =============================================================================================
# S11 - Offline windows and doctor guidance (AR-16)
# =============================================================================================
OFFLINE_WINDOWS = {
    'revocationFreshDays': REVOCATION_FRESH_DAYS, 'catalogExpiryDays': CATALOG_EXPIRY_DAYS, 'rootExpiryDays': ROOT_EXPIRY_DAYS,
    'warningWindowDays': TRUST_WARNING_WINDOW_DAYS,
    'continuationStops': 'when the revocation list is stale (tEval > issuedAt + 90 d) or the root is expired (tEval >= expiresAt)',
    'installStops': 'when the catalog is expired (tEval >= expiresAt) or continuation stops',
    'rootHealing': 'an expired accepted root is healed only by a chain (S5); an expired root alone refuses every operation',
}


def offline_guidance(record, t_eval):
    t = ts(t_eval)
    rev = ts(record['revocationIssuedAt'])
    cat = ts(record['catalogExpiresAt'])
    root = ts(record['rootExpiresAt'])
    rev_until = rev + REVOCATION_FRESH_DAYS * DAY
    out = {'evaluationTime': t_eval, 'windows': OFFLINE_WINDOWS,
           'revocationFreshUntil': iso(rev_until), 'catalogExpiresAt': record['catalogExpiresAt'], 'rootExpiresAt': record['rootExpiresAt'],
           'daysUntilContinuationStops': max(0, (min(rev_until, root) - t) // DAY), 'daysUntilInstallStops': max(0, (min(rev_until, cat, root) - t) // DAY),
           'daysUntilRootExpires': max(0, (root - t) // DAY), 'posture': None, 'remedy': None, 'warning': None, 'userWaiver': None, 'doctor': None}
    if t > rev_until or t >= root:
        out['posture'] = 'REFUSES-ALL-OPERATIONS'
        out['remedy'] = 'present an ordinary payload (consented online refresh or air-gap import); an expired root is healed by the chain rule (S5); a floor ahead of the wall needs a recovery epoch (S4.5)'
    elif t >= cat:
        out['posture'] = 'CONTINUATION-ONLY'
        out['remedy'] = 'already-verified components run; install/update refuse until a payload with a fresh catalog'
    else:
        out['posture'] = 'NORMAL'
    out['warning'] = out['posture'] == 'NORMAL' and out['daysUntilContinuationStops'] <= TRUST_WARNING_WINDOW_DAYS
    out['userWaiver'] = 'NONE: the OD-112-4 G08 waiver is a release-gate waiver held by product and release authority; it never extends an install\'s freshness floor'
    out['doctor'] = {'outcomeWhenDefectFound': 'OC-2', 'exit': 0, 'writes': [],
                     'ciGate': 'select .outcome == "OC-1" on the machine report; exit 0 is not a pass signal',
                     'rationale': 'doctor is not an analysis; D9 policy-failed is unavailable; no exit code is changed by this contract'}
    return out


# ---------------------------------------------------------------------------------------------
# Dispatch for the checker
# ---------------------------------------------------------------------------------------------
def run_case(model, inp):
    if model == 'discovery':
        return discovery(inp)
    if model == 'clock':
        return clock_decision(inp['record'], inp['observation'], inp.get('payload'), inp.get('reportOnly', False))
    if model == 'recovery-challenge':
        return recovery_challenge(inp['record'], inp['nonce'], inp['observation'], inp.get('reportOnly', False))
    if model == 'recovery-apply':
        return recovery_apply(inp['record'], inp['epoch'], inp['signers'], inp['observation'], inp['acceptedRoot'], inp.get('revokedKeys', ()))
    if model == 'repair-authorization':
        return admit_repair_authorization(inp['authorization'], inp['ctx'])
    if model == 'recovery-authorization':
        return admit_recovery_authorization(inp['authorization'], inp['ctx'])
    if model == 'boundary-inventory':
        return boundary_inventory(discovery(inp))
    if model == 'transition-intent':
        refusals = admit_transition_intent(inp['intent'])
        return {'result': 'REFUSE' if refusals else 'ADMIT', 'refusals': refusals, 'd9': d9('TRANSITION.REFUSED') if refusals else None,
                'requiredFields': sorted(TRANSITION_INTENT_KEYS), 'operations': list(TRANSITION_OPERATIONS)}
    if model == 'transition-journal':
        return admit_transition_journal(inp['journal'], inp['ctx'])
    if model == 'transition-recovery':
        return recover_transition_journal(inp['journal'], inp['ctx'])
    if model == 'root-document':
        return admit_root_document(inp['root'], tuple(inp.get('readerSchemas', [1])))
    if model == 'profile-set-envelope':
        return admit_profile_set_envelope(inp['envelope'], inp['acceptedRoot'], inp['signers'], inp.get('revokedKeys', ()), inp.get('selected_profile_digest'))
    if model == 'storage-write':
        return storage_write_admission(inp['backupStatus'], inp.get('allowBackupCustody', False), inp.get('admittedPolicyRecord'), bool(inp.get('ci', False)), bool(inp.get('ephemeral', False)))
    if model == 'root-chain':
        return verify_root_chain(inp['state'], inp['chain'], inp['tEval'], inp['wall'], inp.get('revokedKeys', ()), tuple(inp.get('readerSchemas', [1])))
    if model == 'revocation-observe':
        return revocation_observe(inp['epochAtStart'], inp['currentEpoch'], inp['closure'], inp['revocationEntries'], inp.get('effectivePolicyGrants'), inp.get('requiredGrants'))
    if model == 'observer':
        return observer_tick(inp['lastReadMono'], inp['nowMono'], inp['counterReadOk'])
    if model == 'linearize':
        return linearize(inp['schedule'])
    if model == 'journal-record':
        return admit_journal_record(inp['record'])
    if model == 'host-seal-run' or model == 'seal-run-prefix':
        return admit_seal_run_id_prefix(inp['runId'])
    if model == 'analysis-seal':
        return admit_analysis_seal(inp['record'], inp['run'], inp['objects'], inp['blobs'])
    if model == 'lease':
        return lease_schedule(inp['actions'], inp.get('namespaceRegistry'))
    if model == 'core-transition-scope':
        return core_transition_affected_namespaces(inp['intent'], inp['namespaceRegistry'])
    if model == 'platform':
        return platform_admit(inp['profileSet'], inp['observed'])
    if model == 'migration-recover':
        return migration_recover(inp['footprint'])
    if model == 'migrate-floors':
        return migrate_floors(inp['oldTrust'], inp['coreEmbeddedChainMax'])
    if model == 'rollback-floors':
        return rollback_floors(inp['newTrust'], inp['oldTrust'], inp['oldCoreChainMax'], tuple(inp.get('oldCoreReaders', [1])))
    if model == 'repo-exec-grant':
        return admit_repo_execution_grant(inp['grant'], inp['ctx'])
    if model == 'execution-projection':
        return admit_plan_execution_projection(inp['planPrincipals'], inp['consumedGrants'], inp['preparedResolution'])
    if model == 'semantic-projection':
        return {'principals': semantic_projection_for_grants(inp['grants'])}
    if model == 'offline-guidance':
        return offline_guidance(inp['record'], inp['tEval'])
    if model == 'public-detail':
        # The outcome is produced by the named inner model, never hand-written, so the projection is
        # always over bytes this unit actually emits (S12, blind consumer M-5).
        source = run_case(inp['source']['model'], inp['source']['input']) if 'source' in inp else inp['outcome']
        items = public_details(source, inp.get('refusalKey'))
        return {'items': items, 'codes': sorted({i['code'] for i in items}),
                'pendingRegistrationCodes': sorted({i['code'] for i in items if i['pendingRegistration']})}
    raise Reject('UNKNOWN_MODEL:' + model)


def admit_root_chain(state,chain,t_eval,wall,revoked_keys=(),reader_schemas=(1,2)):
    """Public composition boundary. Old verify_root_chain is a projected-fixture primitive only."""
    for root in [state['acceptedRoot']]+[v['root'] for v in chain]:
        result=admit_root_document(root,reader_schemas)
        if result['result']!='ACCEPT':return {'result':'REFUSE','detail':result['detail'],'stateUnchanged':True}
    return verify_root_chain(state,chain,t_eval,wall,revoked_keys,reader_schemas)
