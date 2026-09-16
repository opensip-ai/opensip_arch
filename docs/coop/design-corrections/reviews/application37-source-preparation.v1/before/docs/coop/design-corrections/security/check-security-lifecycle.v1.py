"""Reference checker for the security/lifecycle unit (PROPOSED, not self-accepted).

Run:  python -I -B check-security-lifecycle.v1.py --report security-lifecycle-report.v1.json
(Python 3.12, jsonschema 4.25.1; from this directory or with repository-relative paths.)

What it does:
  1. verifies every pinned external source in source-pins.v1.json (exact SHA-256);
  2. admits every case file through the foundation exact lexical canonicalizer (product data profile);
  3. runs every case through security_lifecycle_model_v1 and compares dotted-path expectations;
  4. validates every model output against the closed schemas in security-lifecycle.schemas.v1.json;
  5. runs invariant sweeps (floor monotonicity/no-clamp, recovery replay, brokered linearization,
     profile-separation vectors, discovery pruning/cap, platform vocabulary join, admitted-boundary join with the
     native unit instrument) that are not tied to a single hand-authored case;
  6. writes a report that discloses TCB assumptions and that this is design evidence only.
Exit 0 iff all pins verify, all cases pass, all outputs validate and all sweeps hold. It never claims
product qualification, OS measurement or cryptographic verification.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FOUNDATION = HERE.parent / 'foundation' / 'canonical.py'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


canonical = load('canonical', FOUNDATION)
model = load('security_lifecycle_model_v1', HERE / 'security_lifecycle_model_v1.py')

CASE_FILES = [
    ('discovery-cases.v1.json', 'DiscoveryResultV1'),
    ('trust-clock-cases.v1.json', 'ClockDecisionV1'),
    ('trust-recovery-cases.v1.json', None),   # per-case schema (challenge vs apply)
    ('root-chain-cases.v1.json', 'RootChainResultV1'),
    ('revocation-live-cases.v1.json', None),  # observe / observer / linearize
    ('lease-cases.v1.json', 'LeaseTraceV1'),
    ('platform-admission-cases.v1.json', 'PlatformAdmissionV1'),
    ('migration-cases.v1.json', None),        # recover / migrate / rollback
    ('execution-principal-cases.v1.json', 'RepoExecutionAdmissionV1'),
    ('repair-authorization-cases.v1.json', 'RepairAuthorizationAdmissionV1'),
    ('repair-recovery-authorization-cases.v1.json', 'RecoveryAuthorizationAdmissionV1'),   # S10.2 (post-reset v2 P9)
    ('transition-journal-cases.v1.json', None),   # S9.2 intent / journal / recovery (post-reset v2 P10)
    ('root-schema-cases.v1.json', None),      # root-document / profile-set-envelope
    ('public-detail-cases.v1.json', 'PublicDetailProjectionV1'),   # S12 public DomainDetail projection (M-5)
    ('storage-write-cases.v1.json', 'StorageWriteAdmissionV1'),
    ('offline-guidance-cases.v1.json', 'OfflineGuidanceV1'),
]
MODEL_SCHEMA = {
    'discovery': 'DiscoveryResultV1', 'clock': 'ClockDecisionV1', 'recovery-challenge': 'RecoveryChallengeResultV1',
    'recovery-apply': 'RecoveryApplyResultV1', 'root-chain': 'RootChainResultV1', 'revocation-observe': 'RevocationObservationV1',
    'observer': 'ObserverTickV1', 'linearize': 'LinearizationV1', 'lease': 'LeaseTraceV1', 'platform': 'PlatformAdmissionV1',
    'migration-recover': 'MigrationRecoveryV1', 'migrate-floors': 'FloorMigrationV1', 'rollback-floors': 'FloorRollbackV1',
    'repo-exec-grant': 'RepoExecutionAdmissionV1', 'offline-guidance': 'OfflineGuidanceV1',
    'repair-authorization': 'RepairAuthorizationAdmissionV1', 'root-document': 'RootAdmissionV1', 'profile-set-envelope': 'ProfileSetAdmissionV1',
    'storage-write': 'StorageWriteAdmissionV1',
    'execution-projection': 'ExecutionProjectionAdmissionV1', 'semantic-projection': 'SemanticProjectionV1',
    'core-transition-scope': 'CoreTransitionScopeV1', 'public-detail': 'PublicDetailProjectionV1',
    'recovery-authorization': 'RecoveryAuthorizationAdmissionV1', 'boundary-inventory': 'AdmittedBoundaryInventoryV1',
    'transition-intent': 'TransitionIntentAdmissionV1', 'transition-journal': 'TransitionJournalAdmissionV1',
    'transition-recovery': 'TransitionRecoveryV1',
}


def get_path(obj, path):
    cur = obj
    for part in path.split('.'):
        if part == 'length':
            return len(cur)
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            if part not in cur:
                raise KeyError(path)
            cur = cur[part]
        else:
            raise KeyError(path)
    return cur


def substitute(value, subs):
    if isinstance(value, str) and value.startswith('$') and value[1:] in subs:
        return subs[value[1:]]
    if isinstance(value, list):
        return [substitute(v, subs) for v in value]
    if isinstance(value, dict):
        return {k: substitute(v, subs) for k, v in value.items()}
    return value


def iter_cases(doc):
    """Case files carry `cases` or several `*Cases` lists; each case names its `model` or inherits the file's."""
    default_model = doc.get('model')
    for key, val in doc.items():
        if key == 'cases' or key.endswith('Cases'):
            for c in val:
                yield dict(c, model=c.get('model', default_model))


ALIASES = {'baseRecord': 'base', 'ctxBase': 'ctx', 'grantBase': 'grant', 'authorizationBase': 'authorization'}


def build_subs(doc):
    """`$name` substitutions: top-level fixture objects (aliased for the legacy names) and the children of
    `computed`, `keys`, `roots` and `records`, resolved in file order so later entries may use `$from`."""
    subs = {}
    for key in ('computed', 'keys'):          # leaf values first, whatever their position in the file
        for k, v in doc.get(key, {}).items():
            subs[k] = v
    for key, val in doc.items():
        if key in ('roots', 'records', 'observations'):
            for k, v in val.items():
                subs[k] = resolve_input(v, subs)
        elif isinstance(val, dict) and key not in ('conventions', 'computed', 'keys'):
            subs[ALIASES.get(key, key)] = resolve_input(val, subs)
    return subs


def deep_merge(base, over):
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def resolve_input(inp, subs):
    inp = substitute(inp, subs)
    # `$base+` style overrides: {"record": {"$from": "base", "evalHighWater": ...}}
    def walk(v):
        if isinstance(v, dict):
            if '$from' in v:
                base = subs[v['$from']]
                over = {k: walk(x) for k, x in v.items() if k != '$from'}
                return deep_merge(base, over)
            return {k: walk(x) for k, x in v.items()}
        if isinstance(v, list):
            return [walk(x) for x in v]
        return v
    return walk(inp)


def compare(expect, out):
    failures = []
    for path, want in expect.items():
        try:
            got = get_path(out, path)
        except (KeyError, IndexError, TypeError):
            failures.append({'path': path, 'want': want, 'got': '<absent>'})
            continue
        if not canonical.equal_typed(want, got):
            failures.append({'path': path, 'want': want, 'got': got})
    return failures


def run_cases(schemas, validator_for):
    results = []
    for fname, default_schema in CASE_FILES:
        raw = (HERE / fname).read_bytes()
        doc = canonical.parse(raw)   # exact lexical admission of the case file as product data
        subs = build_subs(doc)
        for case in iter_cases(doc):
            entry = {'file': fname, 'id': case['id'], 'model': case['model'], 'status': None, 'failures': [], 'schemaErrors': []}
            try:
                inp = resolve_input(case['input'], subs)
                # optional closed-schema validation of an INPUT document (e.g. a presented recovery epoch)
                for field, sname in case.get('inputSchemas', {}).items():
                    errs = list(validator_for(sname).iter_errors(get_path(inp, field)))
                    if bool(errs) == case.get('inputValid', True):
                        entry['failures'].append({'path': 'inputSchemas.' + field, 'want': 'valid=%s' % case.get('inputValid', True), 'got': [e.message for e in errs][:3] or 'valid'})
                if case.get('expectReject'):
                    try:
                        model.run_case(case['model'], inp)
                        entry['failures'].append({'path': 'expectReject', 'want': case['expectReject'], 'got': 'no rejection'})
                    except model.Reject as e:
                        if not str(e).startswith(case['expectReject']):
                            entry['failures'].append({'path': 'expectReject', 'want': case['expectReject'], 'got': str(e)})
                else:
                    out = model.run_case(case['model'], inp)
                    canonical.typed(out)   # model output is product data: exact JSON types only
                    entry['failures'] = compare(substitute(case['expect'], subs), out)
                    sname = case.get('outputSchema') or MODEL_SCHEMA[case['model']]
                    for err in validator_for(sname).iter_errors(out):
                        entry['schemaErrors'].append('/'.join(str(p) for p in err.absolute_path) + ': ' + err.message)
            except Exception as e:  # a modelling error is a failed case, never a skipped one
                entry['failures'].append({'path': '<exception>', 'want': 'no exception', 'got': '%s: %s' % (type(e).__name__, e)})
            entry['status'] = 'PASS' if not entry['failures'] and not entry['schemaErrors'] else 'FAIL'
            results.append(entry)
    return results


# ---------------------------------------------------------------------------------------------
# Invariant sweeps
# ---------------------------------------------------------------------------------------------
def sweep_clock_monotone():
    """Every PROCEED decision writes floor == evaluationTime >= recorded floor; every REFUSE writes nothing;
    the wall never exceeds admittedTime + 90 d on PROCEED. Grid over walls, floors and payload ages."""
    base_last = '2026-12-20T00:00:00Z'
    checked = 0
    for floor in ('2026-12-21T10:00:00Z', '2027-03-19T00:00:00Z', '2028-06-01T00:00:00Z'):
        for wall_days in (-400, -10, -1, 0, 1, 30, 89, 90, 91, 365, 800):
            for boot in ('boot-A', 'boot-Z'):
                for payload_age in (None, 0, 10, 100):
                    wall = model.iso(model.ts('2026-12-21T10:00:00Z') + wall_days * model.DAY)
                    rec = {'evalHighWater': floor, 'lastAccepted': base_last,
                           'anchor': {'bootId': 'boot-A', 'mono': 1000, 'wall': '2026-12-21T10:00:00Z'},
                           'revocationIssuedAt': base_last, 'catalogExpiresAt': '2027-03-20T00:00:00Z', 'rootExpiresAt': '2027-10-01T00:00:00Z'}
                    obs = {'wall': wall, 'mono': 1000 + max(0, wall_days) * model.DAY, 'bootId': boot}
                    payload = None if payload_age is None else {'newestIssuedAt': model.iso(model.ts(wall) - payload_age * model.DAY), 'presentedRootIssuedAt': None}
                    out = model.clock_decision(rec, obs, payload)
                    checked += 1
                    if out['decision'] == 'PROCEED':
                        assert out['floorWrite'] == out['evaluationTime'], (out, rec, obs, payload)
                        assert model.ts(out['floorWrite']) >= model.ts(floor)
                        assert model.ts(wall) <= model.ts(out['admittedTimeReference']) + model.UNATTESTED_FORWARD_HORIZON_S
                        assert 'evalHighWater' in out['writes']
                    else:
                        assert out['writes'] == [] and out['floorWrite'] is None and out['anchorWrite'] is None and out['lastAcceptedWrite'] is None
                        assert out['floorAdvance'] == 'WITHHELD'
                    ro = model.clock_decision(rec, obs, payload, report_only=True)
                    assert ro['writes'] == [] and ro['floorWrite'] is None and ro['anchorWrite'] is None and ro['lastAcceptedWrite'] is None
                    assert ro['decision'] == out['decision'] and ro['evaluationTime'] == out['evaluationTime'] and ro['states'] == out['states']
    return {'name': 'clock-floor-monotone-no-clamp-report-only-writes-nothing', 'checked': checked, 'holds': True}


def sweep_recovery_replay():
    """A recovery epoch applies once; the same bytes replay-refuse; a counter that differs in either direction
    refuses; a reboot or an expired monotonic window refuses; the floor after recovery is the signed time, never
    below lastAccepted; counters unchanged. Signers are the recovery authority, never root keys."""
    ra = ['r%d' % i * 32 for i in range(5)]
    ra = [('%02d' % i) * 32 for i in range(5)]
    root = {'rootVersion': 3, 'rootKeys': ['k1' * 32, 'k2' * 32, 'k3' * 32], 'rootThreshold': 2, 'recoveryAuthority': {'keys': ra, 'threshold': 3}}
    rec = {'evalHighWater': '2031-01-01T00:00:00Z', 'lastAccepted': '2026-12-20T00:00:00Z', 'anchor': None,
           'rootVersion': 3, 'revocationVersion': 4, 'indexSnapshotVersion': 9, 'recoveryEpochSerial': 0, 'pendingRecoveryChallenge': None}
    obs = {'wall': '2026-12-23T08:00:00Z', 'mono': 6000, 'bootId': 'boot-A'}
    ch = model.recovery_challenge(rec, 'ab' * 32, {'wall': '2026-12-23T07:00:00Z', 'mono': 5000, 'bootId': 'boot-A'})
    rec2 = dict(rec, pendingRecoveryChallenge=ch['pendingWrite'])
    epoch = {'recoverySchema': 1, 'kind': 'trust-recovery-epoch', 'epochSerial': 1, 'issuedAt': '2026-12-23T00:00:00Z',
             'challenge': {'nonce': ch['pendingWrite']['nonce'], 'recordDigest': ch['pendingWrite']['recordDigest']},
             'counters': {'rootVersion': 3, 'revocationVersion': 4, 'indexSnapshotVersion': 9}, 'installBinding': 'challenge'}
    checked = 0
    assert model.recovery_apply(rec2, epoch, ['k1' * 32, 'k2' * 32, 'k3' * 32], obs, root)['detail'] == 'SIGNATURE_THRESHOLD'
    ok = model.recovery_apply(rec2, epoch, ra[:3], obs, root)
    assert ok['result'] == 'APPLIED' and ok['floorLowered'] and ok['writes']['evalHighWater'] == '2026-12-23T00:00:00Z'
    rec3 = dict(rec2, evalHighWater=ok['writes']['evalHighWater'], lastAccepted=ok['writes']['lastAccepted'],
                recoveryEpochSerial=1, pendingRecoveryChallenge=None)
    replay = model.recovery_apply(rec3, epoch, ra[:3], obs, root)
    assert replay['result'] == 'REFUSE' and replay['detail'] == 'NO_PENDING_CHALLENGE'
    ch2 = model.recovery_challenge(rec3, 'cd' * 32, obs)
    rec4 = dict(rec3, pendingRecoveryChallenge=ch2['pendingWrite'])
    replay2 = model.recovery_apply(rec4, epoch, ra[:3], obs, root)
    assert replay2['result'] == 'REFUSE' and replay2['detail'] == 'CHALLENGE_MISMATCH'
    checked += 4
    for k in ('rootVersion', 'revocationVersion', 'indexSnapshotVersion'):
        for delta in (-1, 1):
            ctr = {'rootVersion': 3, 'revocationVersion': 4, 'indexSnapshotVersion': 9}
            ctr[k] += delta
            e2 = dict(epoch, challenge={'nonce': ch2['pendingWrite']['nonce'], 'recordDigest': ch2['pendingWrite']['recordDigest']}, epochSerial=2, counters=ctr)
            out = model.recovery_apply(rec4, e2, ra[:3], obs, root)
            assert out['result'] == 'REFUSE' and out['detail'] == 'COUNTER_MISMATCH:' + k, (k, delta, out)
            checked += 1
    e3 = dict(epoch, challenge={'nonce': ch2['pendingWrite']['nonce'], 'recordDigest': ch2['pendingWrite']['recordDigest']}, epochSerial=2)
    for bad_obs, detail in ((dict(obs, bootId='boot-B'), 'CHALLENGE_BOOT_CHANGED'), (dict(obs, mono=6000 + model.RECOVERY_CHALLENGE_TTL_S + 1), 'CHALLENGE_EXPIRED'),
                            (dict(obs, mono=5999), 'CHALLENGE_CONTINUITY_MALFORMED')):
        assert model.recovery_apply(rec4, e3, ra[:3], bad_obs, root)['detail'] == detail
        checked += 1
    assert model.recovery_apply(rec4, dict(e3, issuedAt='2026-12-24T08:00:01Z'), ra[:3], obs, root)['detail'] == 'ISSUED_IN_FUTURE'
    late_obs = dict(obs, wall='2026-12-24T00:00:01Z', mono=6000 + model.RECOVERY_CHALLENGE_TTL_S)   # still inside the window; issue = lastAccepted but > 24 h behind the wall
    assert model.recovery_apply(rec4, dict(e3, issuedAt='2026-12-23T00:00:00Z'), ra[:3], late_obs, root)['detail'] == 'ISSUED_TOO_OLD_FOR_WALL'
    assert model.recovery_apply(rec4, dict(e3, issuedAt='2026-12-22T23:59:59Z'), ra[:3], obs, root)['detail'] == 'TIME_BEFORE_LAST_ACCEPTED'
    checked += 3
    # exact-typed constants: true is never 1 in epoch fields
    for field, val in (('recoverySchema', True), ('epochSerial', True)):
        assert model.recovery_apply(rec4, dict(e3, **{field: val}), ra[:3], obs, root)['detail'].startswith('SHAPE:')
        checked += 1
    # the next ordinary evaluation after recovery proceeds at the real wall and the floor advances normally
    after = model.clock_decision(dict(rec3, revocationIssuedAt='2026-12-23T00:00:00Z', catalogExpiresAt='2027-03-23T00:00:00Z', rootExpiresAt='2027-10-01T00:00:00Z'),
                                 {'wall': '2026-12-23T08:00:00Z', 'mono': 10, 'bootId': 'boot-R'})
    assert after['decision'] == 'PROCEED' and after['floorWrite'] == '2026-12-23T08:00:00Z' and after['states'] == {'rootExpired': False, 'catalogExpired': False, 'revocationStale': False}
    checked += 1
    return {'name': 'recovery-epoch-applies-once-replay-counter-mismatch-reboot-and-window-refuse', 'checked': checked, 'holds': True}


def sweep_linearization():
    """For every interleaving of one brokered request with REV, no brokered effect commits after REV, and
    a user edit after commit is never overwritten by rollback."""
    import itertools
    checked = 0
    for order in itertools.permutations(['REV trust-revoked', 'COMMIT r1', 'EDIT r1']):
        # EDIT needs COMMIT first; skip impossible orders
        if order.index('EDIT r1') < order.index('COMMIT r1'):
            continue
        sched = ['GRANT g1', 'RA r1', 'RCI r1'] + list(order)
        try:
            out = model.linearize(sched)
        except model.Reject as e:
            # COMMIT after REV never took effect, so a later EDIT of that target is a fixture error, not a model gap
            assert str(e) == 'EDIT_WITHOUT_EFFECT:r1' and order.index('REV trust-revoked') < order.index('COMMIT r1')
            checked += 1
            continue
        checked += 1
        rev = out['revocationSeq']
        for rec in out['journal']:
            if rec['recordType'] in ('ICO', 'RCO'):
                assert rec['seq'] < rev, order
        edit_before_rev = order.index('EDIT r1') < order.index('REV trust-revoked')
        if edit_before_rev:
            # the user's change is present at REV: rollback is blocked and the edit survives
            assert 'r1' in out['disclosure']['rollbackBlocked'] and out['finalTargets']['r1'] == 'edited:r1', order
        else:
            # rollback happened first (exact postimage), then the user's later edit stands
            assert 'r1' in out['disclosure']['reverted'] and out['finalTargets']['r1'] == 'edited:r1', order
    return {'name': 'brokered-linearization-and-no-overwrite-of-user-edits', 'checked': checked, 'holds': True}


def sweep_profile_separation():
    """The metadata profile (NFC required) and the product profile (no normalization) are distinct and
    neither is applied to the other's data: a decomposed string is refused by `canon` and preserved by
    foundation canonical()."""
    decomposed = 'é'
    try:
        model.canon(decomposed)
        raise AssertionError('metadata canon accepted a non-NFC string')
    except model.Reject as e:
        assert str(e) == 'NON_NFC_STRING'
    raw = canonical.canonical({'k': decomposed})
    assert raw == b'{"k":"e\xcc\x81"}'
    # product integers above i64 are admitted by the product profile and refused by the metadata profile
    canonical.canonical({'n': 2**64 - 1})
    try:
        model.canon(2**64 - 1)
        raise AssertionError('metadata canon accepted an integer above i64')
    except model.Reject as e:
        assert str(e) == 'INTEGER_OUT_OF_RANGE'
    return {'name': 'metadata-nfc-profile-and-product-profile-never-mixed', 'checked': 4, 'holds': True}


def sweep_lease_modes():
    """Readers never block an APPEND-WRITE; EXCLUSIVE never coexists with anything; no mode is blocking."""
    checked = 0
    for first in model.LEASE_MODES:
        for second in model.LEASE_MODES:
            out = model.lease_schedule([
                {'actor': 'a', 'op': 'fence-acquire'}, {'actor': 'a', 'op': 'lease', 'mode': first}, {'actor': 'a', 'op': 'fence-release'},
                {'actor': 'b', 'op': 'fence-acquire'}, {'actor': 'b', 'op': 'lease', 'mode': second}, {'actor': 'b', 'op': 'fence-release'}])
            checked += 1
            r = out['trace'][4]['result']
            coexist = {('SHARED-READ', 'SHARED-READ'), ('SHARED-READ', 'APPEND-WRITE'), ('APPEND-WRITE', 'SHARED-READ')}
            assert (r == 'ACQUIRED') == ((first, second) in coexist), (first, second, r)
            assert out['deadlockFree']
    return {'name': 'lease-mode-compatibility-matrix', 'checked': checked, 'holds': True}


def sweep_public_detail_closure():
    """S12 / blind consumer M-5. Run every case and sweep fixture and project each refusing outcome onto the
    public DomainDetail vocabulary. Invariants: (a) every emitted code is a member of the unit's closed
    SECURITY_PUBLIC_DETAIL_CODES, so there is no wildcard family; (b) every emitted code is registered,
    with no remaining drafting allowance, and every internal alias agrees with the shared registry; (c) no sub-detail after the first colon becomes a code;
    (d) the D9 branch is decided by the refusal, never by naming the defect more precisely."""
    registry = json.loads((HERE.parent / 'public-detail-registry.v1.json').read_text())
    registered = {r['code'] for r in registry['records']}
    aliased = {r['internalCode']:r['publicCode'] for r in registry['internalAliases']}
    emitted, pending, subjects, checked = set(), set(), set(), 0
    for fname, _ in CASE_FILES:
        doc = canonical.parse((HERE / fname).read_bytes())
        subs = build_subs(doc)
        for case in iter_cases(doc):
            if case['model'] == 'public-detail':
                continue
            try:
                out = model.run_case(case['model'], resolve_input(case['input'], subs))
            except Exception:
                continue
            key = 'TRANSITION.REFUSED' if case['model'].startswith('transition') else (
                  'GRANT.REFUSED' if case['model'] in ('repo-exec-grant', 'repair-authorization', 'recovery-authorization') else (
                  'PLAN.EXECUTION_PROJECTION_REFUSED' if case['model'] == 'execution-projection' else None))
            for item in model.public_details(out, key):
                checked += 1
                emitted.add(item['code'])
                if item['subject'] is not None:
                    subjects.add(item['subject'])
                if item['pendingRegistration']:
                    pending.add(item['code'])
    outside = sorted(emitted - model.SECURITY_PUBLIC_DETAIL_CODES)
    unregistered = sorted(emitted - registered)
    over_pending = sorted(set(unregistered) - model.PENDING_PUBLIC_DETAIL_REGISTRATIONS)
    subject_as_code = sorted(s for s in subjects if s.partition(':')[0] in model.SECURITY_PUBLIC_DETAIL_CODES)
    alias_drift = sorted(k for k,v in model.SECURITY_INTERNAL_DETAIL_ALIASES.items() if aliased.get(k)!=v)
    holds = not outside and not unregistered and not subject_as_code and not alias_drift
    return {'name': 'public-domain-details-are-a-closed-fully-registered-set',
            'checked': checked, 'holds': holds, 'emitted': len(emitted),
            'outsideClosedSet': outside, 'notYetRegistered': unregistered,
            'beyondDeclaredPending': over_pending, 'subjectTextThatIsAlsoACode': subject_as_code,
            'declaredPending': sorted(model.PENDING_PUBLIC_DETAIL_REGISTRATIONS),
            'internalAliasDrift': alias_drift,
            'note': 'the registry and the typed workflow enum are owned elsewhere; this sweep never edits them'}


def sweep_root_schema_readers():
    """Every schema-2 root fixture is typed-unsupported under a {1}-only reader and never reported as corruption; every
    schema-1 fixture admits identically under {1} and {1,2}; a boolean rootSchema is never admitted by any reader."""
    doc = canonical.parse((HERE / 'root-schema-cases.v1.json').read_bytes())
    subs = build_subs(doc)
    checked = 0
    for case in doc['rootCases']:
        root = resolve_input(case['input'], subs)['root']
        for readers in ((1,), (1, 2), (2,)):
            out = model.admit_root_document(root, readers)
            checked += 1
            if isinstance(root.get('rootSchema'), bool):
                assert out['result'] == 'REFUSE' and out['detail'] == 'ROOT.SCHEMA_CONSTANT_TYPE'
            elif out['detail'] == 'ROOT.SHAPE':
                pass   # closed shape is checked before the reader set
            elif root.get('rootSchema') in (1, 2) and root['rootSchema'] not in readers:
                assert out['refusal'] == 'ROOT.SCHEMA_UNSUPPORTED' and out['d9']['code'] == 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED'
            assert out['refusal'] != 'MIGRATION.CORRUPT'
    return {'name': 'root-schema-reader-sets-typed-unsupported-never-corruption', 'checked': checked, 'holds': True}


def _synthetic_repo(first_party_units, installed_packages):
    """Generated lstat map: one VCS root with a root package.json, N first-party `pkgNNNN/package.json` directories and
    M installed `node_modules/<pkg>/package.json` manifests (each with its own directory entry)."""
    R = '/home/alice/big'
    fs = {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1},
          '/home/alice': {'kind': 'dir', 'uid': 1000, 'mode': '0700', 'dev': 1}, R: {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1, 'vcs': True},
          R + '/package.json': {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 100}}
    d = lambda: {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}
    f = lambda: {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 100}
    for i in range(first_party_units):
        fs[R + '/pkg%04d' % i] = d()
        fs[R + '/pkg%04d/package.json' % i] = f()
    if installed_packages:
        fs[R + '/node_modules'] = d()
        for i in range(installed_packages):
            fs[R + '/node_modules/dep%04d' % i] = d()
            fs[R + '/node_modules/dep%04d/package.json' % i] = f()
    return {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs}


def sweep_discovery_pruning_and_cap():
    """MUST-3: 4200 installed package manifests are one pruned tree, not units and not a cap refusal; 4200 first-party
    marker directories are a typed PROJECT.WORKSPACE_UNIT_LIMIT refusal (D9 REQUEST.UNSATISFIABLE) with no truncation and
    no exception; exactly 4096 first-party units still admit. The shared rule and the security instrument agree on counts."""
    checked = 0
    out = model.discovery(_synthetic_repo(0, 4200))
    assert out['status'] == 'ACCEPT', out.get('refusal')
    assert [u['path'] for u in out['provenance']['units']] == ['/home/alice/big']
    assert out['provenance']['prunedTrees'] == [{'path': '/home/alice/big/node_modules', 'reason': 'dependency-tree', 'markerCount': 4200}]
    checked += 1
    out = model.discovery(_synthetic_repo(4200, 4200))
    assert out['status'] == 'REFUSE' and out['refusal'] == 'PROJECT.WORKSPACE_UNIT_LIMIT', out.get('refusal')
    assert out['detail'] == 'WORKSPACE_UNIT_LIMIT:4201>4096' and out['d9'] == {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.UNSATISFIABLE'}
    assert out['provenance']['units'] == [] and out['provenance']['prunedTrees'][0]['markerCount'] == 4200
    checked += 1
    out = model.discovery(_synthetic_repo(4095, 10))   # root + 4095 = exactly the cap
    assert out['status'] == 'ACCEPT' and len(out['provenance']['units']) == 4096
    checked += 1
    enum = model.DD.enumerate_units(['package.json'] + ['pkg%04d/package.json' % i for i in range(4095)] + ['node_modules/dep%d/package.json' % i for i in range(10)])
    assert len(enum['unitDirs']) == 4096 and enum['refusal'] is None and enum['prunedTrees'][0]['markerCount'] == 10
    for legal, pruned in (('packages/target/index.ts', None), ('src/target/x.ts', None), ('target/debug/x.rs', ('target', 'cargo-build-output')),
                          ('node_modules/a/node_modules/b/index.js', ('node_modules', 'dependency-tree')), ('.git/hooks/package.json', ('.git', 'vcs-tree')),
                          ('crates/core/target/out.rs', ('crates/core/target', 'cargo-build-output')), ('crates/core/src/target/mod.rs', None)):
        assert model.DD.classify_path(legal, {'', 'crates/core'}) == pruned, legal
        checked += 1
    assert model.DD.normalize_explicit_root('.') == '' and model.DD.normalize_explicit_root('a/b/') == 'a/b'
    for bad in ('', '/abs', 'a//b', 'a/../b', './a', 'a\\b', 'a\x00'):
        try:
            model.DD.normalize_explicit_root(bad)
            raise AssertionError('accepted ' + repr(bad))
        except model.DD.RootGrammarError:
            checked += 1
    return {'name': 'discovery-prunes-installed-dependencies-and-refuses-real-cap-typed', 'checked': checked, 'holds': True}


def sweep_platform_vocabulary_join():
    """MUST-2: the ONE machine platform vocabulary keys the profile set, admits every platform, keys the grant truth table,
    equals the native matrix platformFamilies and the workflow test-execution platformId enum; every display alias refuses
    in platform admission and in grant admission."""
    checked = 0
    pdoc = canonical.parse((HERE / 'platform-admission-cases.v1.json').read_bytes())
    psubs = build_subs(pdoc)
    edoc = canonical.parse((HERE / 'execution-principal-cases.v1.json').read_bytes())
    esubs = build_subs(edoc)
    schemas = canonical.parse((HERE / 'security-lifecycle.schemas.v1.json').read_bytes())
    assert tuple(sorted(schemas['schemas']['PlatformProfileSetV1']['properties']['platforms']['properties'])) == model.PLATFORM_IDS
    assert tuple(sorted(schemas['schemas']['RepoExecutionGrantV2']['properties']['platformId']['enum'])) == model.PLATFORM_IDS
    assert tuple(sorted(model.PLATFORM_TRUTH_TABLE)) == model.PLATFORM_IDS and tuple(sorted(psubs['profileSet']['platforms'])) == model.PLATFORM_IDS
    native = json.loads((HERE.parent / 'native' / 'native-capability-matrix.v2.json').read_text())
    assert tuple(sorted(native['platformFamilies'])) == model.PLATFORM_IDS, native['platformFamilies']
    wf = json.loads((HERE.parent / 'workflows' / 'schemas' / 'test-execution.schema.json').read_text())
    wf_ids = wf['$defs']['TestExecutionStepParams']['properties']['platformId']['enum'] if 'TestExecutionStepParams' in wf.get('$defs', {}) else None
    if wf_ids is None:   # locate any platformId enum in the document
        def find(x):
            if isinstance(x, dict):
                if 'platformId' in x and isinstance(x['platformId'], dict) and 'enum' in x['platformId']:
                    return x['platformId']['enum']
                for v in x.values():
                    r = find(v)
                    if r: return r
            if isinstance(x, list):
                for v in x:
                    r = find(v)
                    if r: return r
        wf_ids = find(wf)
    assert tuple(sorted(wf_ids)) == model.PLATFORM_IDS, wf_ids
    checked += 5
    obs = {'macos-aarch64': psubs['macos'], 'macos-x86_64': psubs['macosIntel'], 'linux-x86_64-gnu': psubs['linux'], 'linux-aarch64-gnu': psubs['linuxArm']}
    for pid in model.PLATFORM_IDS:
        adm = model.platform_admit(psubs['profileSet'], obs[pid])
        assert adm['result'] == 'ADMIT' and adm['platform'] == pid and adm['displayAlias'] == model.PLATFORM_DISPLAY_ALIASES[pid], (pid, adm['refusals'])
        grant = dict(esubs['grant'], platformId=adm['platform'])   # the admitted id IS the grant id: one vocabulary
        g = model.admit_repo_execution_grant(grant, esubs['ctx'])
        assert g['result'] == 'ADMIT', (pid, g['refusals'])
        checked += 2
        alias = model.PLATFORM_DISPLAY_ALIASES[pid]
        if alias != pid:
            a = model.platform_admit(psubs['profileSet'], dict(obs[pid], platform=alias))
            assert a['result'] == 'REFUSE' and a['refusals'][0].startswith('NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:')
            ga = model.admit_repo_execution_grant(dict(esubs['grant'], platformId=alias), esubs['ctx'])
            assert ga['result'] == 'REFUSE' and 'GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID:' + pid in ga['refusals']
            checked += 2
    return {'name': 'one-machine-platform-vocabulary-joins-profile-set-admission-grant-native-matrix-and-workflow-schema', 'checked': checked, 'holds': True}


def _p3_repo():
    """The post-reset v2 P3 counterexample fixture: a VCS root holding a nested repository (vendor/lib, its own VCS marker
    and an installed dependency tree) and a nested project (apps/site with its own opensip.json and a sub crate)."""
    R = '/home/alice/repo'
    d = lambda **kw: dict({'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}, **kw)
    f = lambda: {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    fs = {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1},
          '/home/alice': d(mode='0700'), R: d(vcs=True), R + '/package.json': f(),
          R + '/vendor': d(), R + '/vendor/lib': d(vcs=True), R + '/vendor/lib/package.json': f(), R + '/vendor/lib/src': d(),
          R + '/vendor/lib/node_modules': d(), R + '/vendor/lib/node_modules/x': d(), R + '/vendor/lib/node_modules/x/package.json': f(),
          R + '/apps': d(), R + '/apps/site': d(), R + '/apps/site/opensip.json': f(), R + '/apps/site/package.json': f(),
          R + '/apps/site/sub': d(), R + '/apps/site/sub/Cargo.toml': f()}
    return R, fs


def sweep_boundary_join_native():
    """Post-reset v2 P3: over ONE marker inventory, the security instrument's admitted boundary inventory, passed to the
    native unit instrument, yields exactly the security unit set; every security-excluded nested unit directory is a
    native excluded unit with the same reason; memberships below a boundary are outside the project; the Plan scope
    descriptor names every boundary anchor; an explicit root crossing a boundary refuses in both instruments; and the
    standalone native instrument (no inventory) discloses source=none instead of claiming completeness."""
    native = load('native_evidence_model_v2', HERE.parent / 'native' / 'native_evidence_model.v2.py')
    R, fs = _p3_repo()
    sd = model.discovery({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs})
    assert sd['status'] == 'ACCEPT', sd
    inv = model.boundary_inventory(sd)
    assert inv == {'schemaVersion': 1, 'source': 'security.discovery', 'selectedRoot': R, 'nestedRepositories': ['vendor/lib'],
                   'nestedProjects': ['apps/site'], 'custodyExcludedUnits': [],
                   'prunedTrees': [{'path': 'vendor/lib/node_modules', 'reason': 'dependency-tree', 'markerCount': 1}]}, inv
    markers = {p[len(R) + 1:]: {'sha256': '1' * 64} for p, e in fs.items() if p.startswith(R + '/') and e['kind'] == 'file' and p.rpartition('/')[2] in model.WORKSPACE_MARKERS}
    nd = native.discover_units(markers, None, inv)
    assert nd['refused'] is None
    sroots = sorted(model.DD.relative_locator(R, u['path']) for u in sd['provenance']['units'])
    assert sroots == sorted({u['rootPath'] for u in nd['units']}) == [''], (sroots, nd['units'])
    sexcl = sorted((model.DD.relative_locator(R, x['path']), x['reason']) for x in sd['provenance']['excludedUnits'])
    nexcl = sorted((x['path'], {'nested-repository': 'INSIDE_NESTED_REPOSITORY', 'nested-project': 'INSIDE_NESTED_PROJECT'}[x['reason']]) for x in nd['boundaries']['excludedUnits'])
    assert sexcl == nexcl == [('apps/site', 'INSIDE_NESTED_PROJECT'), ('apps/site/sub', 'INSIDE_NESTED_PROJECT'), ('vendor/lib', 'INSIDE_NESTED_REPOSITORY')], (sexcl, nexcl)
    assert [dict(t, path=model.DD.relative_locator(R, t['path'])) for t in sd['provenance']['prunedTrees']] == nd['prunedTrees'] == inv['prunedTrees']
    mem = native.assign_membership(nd['units'], ['index.js', 'vendor/lib/src/x.js', 'apps/site/sub/src/lib.rs'], inv)
    assert mem['outsideBoundaryFiles'] == ['apps/site/sub/src/lib.rs', 'vendor/lib/src/x.js'] and mem['erasedFiles'] == []
    scope = native.unit_scope_descriptor(nd['units'], [], None, nd['prunedTrees'], inv)
    assert {'apps/site', 'vendor/lib'} <= set(scope['scopeDescriptor']['excludedPathPrefixes']) and scope['boundaries']['source'] == 'security.discovery'
    checked = 6
    for join, detail in (('apps/site/sub', 'JOIN_CROSSES_NESTED_PROJECT'), ('vendor/lib', 'JOIN_CROSSES_NESTED_REPOSITORY')):
        sj = model.discovery({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs, 'explicitJoins': [join]})
        assert sj['status'] == 'REFUSE' and sj['detail'] == detail, sj
        nj = native.discover_units(markers, [join], inv)
        assert nj['refused'] is not None and nj['refused']['detail'] == 'native.explicit-root-crosses-boundary', nj['refused']
        checked += 2
    alone = native.discover_units(markers)
    assert alone['boundaries']['source'] == 'none' and sorted(u['rootPath'] for u in alone['units']) == ['', 'apps/site', 'apps/site/sub', 'vendor/lib']
    bad = native.discover_units(markers, None, dict(inv, prunedTrees=[]))
    assert bad['refused']['detail'] == 'native.boundary-inventory-mismatch'
    checked += 2
    return {'name': 'admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery', 'checked': checked, 'holds': True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', required=True)
    a = ap.parse_args()
    from jsonschema import Draft202012Validator
    pins = json.loads((HERE / 'source-pins.v1.json').read_text())
    changed = []
    for item in pins['pins']:
        p = ROOT / item['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            changed.append(item['path'])
    report = {'artifact': 'opensip.security-lifecycle.reference-report', 'version': 1, 'status': 'PROPOSED-NOT-SELF-ACCEPTED',
              'standing': 'design evidence over SYNTHETIC fixtures; not product qualification, OS measurement or cryptographic verification',
              'interpreter': sys.version.split()[0], 'sourcePinsValid': not changed, 'changedOrMissing': changed,
              'tcbAssumptions': {'clock': model.CLOCK_TCB, 'recovery': model.RECOVERY_TCB, 'rootChain': model.ROOT_TCB, 'platform': model.PLATFORM_TCB,
                                 'boundaryInventory': model.BOUNDARY_INVENTORY_TCB, 'repairRecovery': model.REPAIR_RECOVERY_TCB, 'transition': model.TRANSITION_TCB},
              'cases': [], 'sweeps': [], 'passed': False, 'productQualification': False}
    if changed:
        Path(a.report).write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'sourcePinsValid': False, 'changedOrMissing': changed}))
        return 1
    schemas = canonical.parse((HERE / 'security-lifecycle.schemas.v1.json').read_bytes())
    validators = {}

    def validator_for(name):
        if name not in validators:
            if name not in schemas['schemas']:
                raise KeyError('UNKNOWN_SCHEMA:' + name)
            # the bundle is the root document so `#/$defs/...` and `#/schemas/...` references resolve
            s = {'$ref': '#/schemas/' + name, '$defs': schemas['$defs'], 'schemas': schemas['schemas']}
            Draft202012Validator.check_schema(s)
            validators[name] = canonical.ExactValidator(s)
        return validators[name]

    report['cases'] = run_cases(schemas, validator_for)
    for sweep in (sweep_clock_monotone, sweep_recovery_replay, sweep_linearization, sweep_profile_separation, sweep_lease_modes, sweep_root_schema_readers,
                  sweep_discovery_pruning_and_cap, sweep_platform_vocabulary_join, sweep_boundary_join_native,
                  sweep_public_detail_closure):
        try:
            report['sweeps'].append(sweep())
        except Exception as e:  # any failure inside a sweep is a failed sweep, never a skipped one
            report['sweeps'].append({'name': sweep.__name__, 'holds': False, 'detail': ('%s: %s' % (type(e).__name__, e))[:500]})
    counts = {'total': len(report['cases']), 'pass': sum(c['status'] == 'PASS' for c in report['cases'])}
    counts['fail'] = counts['total'] - counts['pass']
    report['counts'] = counts
    report['passed'] = counts['fail'] == 0 and all(s['holds'] for s in report['sweeps'])
    report['schemasValidated'] = sorted(validators)
    Path(a.report).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'counts': counts, 'sweeps': [(s['name'], s['holds']) for s in report['sweeps']]}))
    for c in report['cases']:
        if c['status'] != 'PASS':
            print('FAIL', c['file'], c['id'], json.dumps(c['failures'])[:600], json.dumps(c['schemaErrors'])[:600])
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
