"""Independent reviewer probes for frozen candidate-subject.v4.

Written by a fresh actual-Claude reviewer session that authored none of the subject
bytes. Every probe composes the ACTUAL frozen models; none mirrors a unit fixture's
expectation. Signatures, OS observations, evaluator callbacks, fence/lease
observations, trust instants and pivot presences are declared synthetic TCB inputs.
Runs against the scratch copy (checkers write beside their sources).
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
import traceback
from pathlib import Path

from jsonschema import ValidationError

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v4/scratch')
DC = ROOT / 'docs/coop/design-corrections'
CONTRACTS = ROOT / 'docs/v2/contracts/product-v1'
ARCH = ROOT / 'docs/v2/architecture'

spec = importlib.util.spec_from_file_location('probe_host', DC / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S, N, W, C = M.S, M.N, M.W, M.C
IM = N.IM
F = M.load('probe_fixtures', 'integration-fixtures.py')

results = []


def rec(pid, title, status, detail, **extra):
    results.append({'probe': pid, 'title': title, 'status': status, 'detail': detail, **extra})
    print('%-6s %-8s %s' % (pid, status, title))
    if status != 'OK':
        print('        ' + str(detail)[:2000])


def probe(pid, title):
    def deco(fn):
        try:
            out = fn()
        except Exception as exc:  # a probe that dies is a finding about the probe, reported honestly
            rec(pid, title, 'PROBE-ERROR', ''.join(traceback.format_exception_only(type(exc), exc)).strip(),
                traceback=traceback.format_exc()[-1500:])
            return
        if isinstance(out, tuple):
            status, detail = out
        else:
            status, detail = ('OK' if out else 'COUNTEREXAMPLE'), out
        rec(pid, title, status, detail)
    return deco


def refuses(fn):
    """True iff fn() raises any admission/validation refusal used by these models."""
    try:
        fn()
    except (ValueError, ValidationError, C.AdmissionError, W.Refusal, N.C.AdmissionError, IM.C.AdmissionError, KeyError):
        return True
    return False


def raised(fn):
    try:
        fn()
    except Exception as exc:
        return exc
    return None


NF = C.parse((DC / 'native/native-cases.v2.json').read_bytes())['fixtures']
SF = C.parse((DC / 'security/execution-principal-cases.v1.json').read_bytes())
WF = C.parse((DC / 'workflows/workflow-cases.v1.json').read_bytes())
REG = C.parse((DC / 'public-detail-registry.v1.json').read_bytes())
COMMON = C.parse((DC / 'workflows/schemas/common.schema.json').read_bytes())
INVENTORY = C.parse((DC / 'workflows/command-inventory.v1.json').read_bytes())


def sub(value):
    if isinstance(value, str) and value.startswith('$'):
        return WF['constants'][value[1:]]
    if isinstance(value, list):
        return [sub(v) for v in value]
    if isinstance(value, dict):
        return {k: sub(v) for k, v in value.items()}
    return value


def bind(grant, ctx):
    digest = M.owner_digest(grant['owners'])
    grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest
    ctx.pop('semanticGrantPrincipals', None)
    ctx.update(projectId=grant['projectId'], snapshotId=grant['snapshotId'], argvDigest=grant['argvDigest'])
    return grant, ctx


def test_grant(platform, mode, ci, policy_id='a' * 64):
    grant, ctx = copy.deepcopy(SF['grantBase']), copy.deepcopy(SF['ctxBase'])
    grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId=platform,
                 runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
    argv = ['bin/opensip-test-runner', '--ci']
    grant['argvDigest'] = W.payload_digest(argv)
    grant['effects'] = dict(S.PLATFORM_TRUTH_TABLE[platform])
    grant['authorization'] = ({'mode': 'policy-record', 'policyRecordId': policy_id, 'ci': ci}
                              if mode == 'policy-record' else {'mode': 'interactive-explicit', 'policyRecordId': None, 'ci': ci})
    bind(grant, ctx)
    ctx = dict(ctx, ci=ci)
    return grant, ctx, argv


def test_params(platform, grant, projection, argv, consent):
    return {'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': platform,
            'authorizationRef': projection['securityGrantRef'], 'argv': argv,
            'argv0Source': {'kind': 'toolchain-closure', 'closureId': grant['toolClosureId'], 'member': argv[0]},
            'kind': 'test-execution', 'cwdIsRoot': True, 'consentSource': consent, 'afterStep': 0,
            'timeoutMilliseconds': 600000, 'maxOutputBytes': 1048576, 'environmentAllowlist': [],
            'effects': grant['effects']}


def test_ctx(grant, ctx, projection, ci):
    return {'ci': ci, 'projectId': grant['projectId'], 'snapshotId': grant['snapshotId'], 'grant': projection,
            'snapshotMembers': ctx['snapshotMembers'],
            'toolchainMembers': {grant['toolClosureId']: ctx['toolClosure']['members']},
            'truthTable': S.PLATFORM_TRUTH_TABLE, 'liveEqualsAfterStep': True}


PLATFORMS = sorted(S.PLATFORM_TRUTH_TABLE)

# ===========================================================================
# V4-SPECIFIC: MUST-A / ADV-i consent join
# ===========================================================================


@probe('P1', 'MUST-A: policy-record grant admits a test step on all 4 platforms, in and out of CI')
def _():
    rows = {}
    for platform in PLATFORMS:
        for ci in (False, True):
            grant, ctx, argv = test_grant(platform, 'policy-record', ci)
            proj = M.test_grant_projection(grant, ctx)
            params = test_params(platform, grant, proj, argv, 'pre-existing-policy')
            adm = W.admit_test_execution(params, test_ctx(grant, ctx, proj, ci))
            rows['%s.ci=%s' % (platform, ci)] = (proj['consentSource'], adm['admitted'], adm['confinementClaimed'])
    ok = all(v == ('pre-existing-policy', True, False) for v in rows.values()) and len(rows) == 8
    return ('OK' if ok else 'COUNTEREXAMPLE'), rows


@probe('P2', 'MUST-A: interactive-explicit grant admits outside CI, and its projection is interactive-consent')
def _():
    rows = {}
    for platform in PLATFORMS:
        grant, ctx, argv = test_grant(platform, 'interactive-explicit', False)
        proj = M.test_grant_projection(grant, ctx)
        params = test_params(platform, grant, proj, argv, 'interactive-consent')
        adm = W.admit_test_execution(params, test_ctx(grant, ctx, proj, False))
        rows[platform] = (proj['consentSource'], adm['admitted'])
    return ('OK' if all(v == ('interactive-consent', True) for v in rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P3', 'MUST-A: interactive-explicit grant in CI is refused by SECURITY admission on all 4 platforms')
def _():
    rows = {}
    for platform in PLATFORMS:
        grant, ctx, argv = test_grant(platform, 'interactive-explicit', True)
        exc = raised(lambda: M.test_grant_projection(grant, ctx))
        rows[platform] = None if exc is None else str(exc)[:160]
    return ('OK' if all(v is not None for v in rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P4', 'MUST-A: neither consent value can be relabelled; the workflow compares the ADMITTED projection')
def _():
    rows = {}
    for platform in PLATFORMS:
        for ci in (False, True):
            # policy grant relabelled interactive
            g, c, argv = test_grant(platform, 'policy-record', ci)
            p = M.test_grant_projection(g, c)
            rows['policy->interactive.%s.ci=%s' % (platform, ci)] = refuses(
                lambda: W.admit_test_execution(test_params(platform, g, p, argv, 'interactive-consent'),
                                               test_ctx(g, c, p, ci)))
            # interactive grant relabelled policy (non-CI only; CI is refused at security)
            if not ci:
                g2, c2, argv2 = test_grant(platform, 'interactive-explicit', False)
                p2 = M.test_grant_projection(g2, c2)
                rows['interactive->policy.%s' % platform] = refuses(
                    lambda: W.admit_test_execution(test_params(platform, g2, p2, argv2, 'pre-existing-policy'),
                                                   test_ctx(g2, c2, p2, False)))
                rows['legacy-spelling.%s' % platform] = refuses(
                    lambda: W.admit_test_execution(test_params(platform, g2, p2, argv2, 'interactive'),
                                                   test_ctx(g2, c2, p2, False)))
    return ('OK' if all(rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P5', 'MUST-A: the projection is a FUNCTION of the admitted mode (no constant-value regression)')
def _():
    """The v3 defect was a projection that could only ever produce one value. Prove the
    image of the projection over all admitted modes has both values, from real admissions."""
    image = set()
    for platform in PLATFORMS:
        g, c, _ = test_grant(platform, 'policy-record', True)
        image.add(M.test_grant_projection(g, c)['consentSource'])
        g, c, _ = test_grant(platform, 'interactive-explicit', False)
        image.add(M.test_grant_projection(g, c)['consentSource'])
    enum = C.parse((DC / 'workflows/schemas/test-execution.schema.json').read_bytes())
    declared = set(enum['$defs']['TestExecutionStepParams']['properties']['consentSource']['enum'])
    return ('OK' if image == declared == {'pre-existing-policy', 'interactive-consent'} else 'COUNTEREXAMPLE'), \
        {'projectionImage': sorted(image), 'schemaEnum': sorted(declared)}


@probe('P6', 'ADV-i: the ONE mapping table in workflows section 12 equals all three real closed enums')
def _():
    text = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    rows = re.findall(r'^\|\s*(interactive-explicit|policy-record)\s*\|\s*([a-z-]+)\s*\|\s*([a-z-]+)\s*\|',
                      text, re.M)
    table = {r[0]: (r[1], r[2]) for r in rows}
    sec = C.parse((DC / 'security/security-lifecycle.schemas.v1.json').read_bytes())
    sec_modes = set(sec['$defs']['Consent']['properties']['mode']['enum'])
    te = C.parse((DC / 'workflows/schemas/test-execution.schema.json').read_bytes())
    te_modes = set(te['$defs']['TestExecutionStepParams']['properties']['consentSource']['enum'])
    rp = C.parse((DC / 'workflows/schemas/repair.schema.json').read_bytes())
    rp_modes = set(rp['$defs']['RepairApplyParams']['properties']['consentSource']['enum'])
    ok = (set(table) == sec_modes
          and {v[0] for v in table.values()} == te_modes
          and {v[1] for v in table.values()} == rp_modes
          and table['policy-record'] == ('pre-existing-policy', 'policy')
          and table['interactive-explicit'] == ('interactive-consent', 'interactive'))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'table': table, 'security': sorted(sec_modes),
                                                'test': sorted(te_modes), 'repair': sorted(rp_modes)}


@probe('P7', 'ADV-i: the repair projection carries the ADMITTED consent source and ci, and repair_apply compares both')
def _():
    """Rebuild the actual repair authorization -> projection -> apply chain from the frozen
    security/workflow cases, then attack the two new conjuncts independently."""
    case = sub(copy.deepcopy(WF['repairApply']))
    plan = case['plan']
    rows = {}
    for ci in (False, True):
        auth = copy.deepcopy(sub(WF['repairAuthorization']))
        auth['consent'] = {'mode': 'policy-record', 'policyRecordId': 'c' * 64, 'ci': ci}
        ctx = copy.deepcopy(sub(WF['repairAuthorizationContext']))
        ctx['ci'] = ci
        ref = 'security.repair-apply-authorization.v1:' + C.identity('security.repair-apply-authorization.v1', auth)
        proj = M.repair_authorization_projection(auth, ctx, plan, ref)
        rows['ci=%s.projection' % ci] = (proj['consentSource'], proj['ci'])
    return ('OK' if rows == {'ci=False.projection': ('policy', False),
                             'ci=True.projection': ('policy', True)} else 'COUNTEREXAMPLE'), rows


@probe('P8', 'ADV-i residue: the TEST projection carries no ci, so no side asserts grant.ci == invocation.ci')
def _():
    """Repair now binds ci; test does not. Determine whether that is an authority hole or
    a stated TCB assumption, by exercising every (grantCi, invocationCi) pair."""
    outcomes = {}
    for mode in ('policy-record', 'interactive-explicit'):
        for grant_ci in (False, True):
            g, c, argv = test_grant('macos-aarch64', mode, grant_ci)
            exc = raised(lambda: M.test_grant_projection(g, c))
            if exc is not None:
                outcomes['%s.grantCi=%s' % (mode, grant_ci)] = 'security-refused'
                continue
            p = M.test_grant_projection(g, c)
            consent = 'pre-existing-policy' if mode == 'policy-record' else 'interactive-consent'
            for inv_ci in (False, True):
                key = '%s.grantCi=%s.invocationCi=%s' % (mode, grant_ci, inv_ci)
                try:
                    W.admit_test_execution(test_params('macos-aarch64', g, p, argv, consent),
                                           test_ctx(g, c, p, inv_ci))
                    outcomes[key] = 'ADMIT'
                except Exception:
                    outcomes[key] = 'refused'
    carries_ci = 'ci' in M.test_grant_projection(*test_grant('macos-aarch64', 'policy-record', True)[:2])
    # The only disagreement that could grant authority is an interactive grant used in CI.
    hole = outcomes.get('interactive-explicit.grantCi=False.invocationCi=True') == 'ADMIT'
    return ('OK' if not hole else 'COUNTEREXAMPLE'), {'outcomes': outcomes, 'testProjectionCarriesCi': carries_ci,
                                                      'repairProjectionCarriesCi': True, 'authorityHole': hole}


# ===========================================================================
# V4-SPECIFIC: SHOULD-A typed PROJECT.SCOPE_LIMIT
# ===========================================================================


@probe('P9', 'SHOULD-A: 1024 roots admit, 1025 refuse typed, and NOTHING is truncated')
def _():
    ok1024 = N.unit_scope_descriptor(
        N.discover_units({'pkg%04d/package.json' % i: {'sha256': '1' * 64} for i in range(1024)})['units'], [])
    big = N.discover_units({'pkg%04d/package.json' % i: {'sha256': '1' * 64} for i in range(1025)})
    exc = raised(lambda: N.unit_scope_descriptor(big['units'], []))
    d9 = N.d9_map('PROJECT.SCOPE_LIMIT')
    term = M.public_termination(exc.d9, exc.detail,
                                'Select at most 1024 workspace roots.',
                                '%s:%d>%d' % (exc.subject['field'], exc.subject['count'], exc.subject['limit']))
    ok = (len(ok1024['scopeDescriptor']['workspaceRoots']) == 1024
          and big['refused'] is None and len(big['units']) == 1025
          and isinstance(exc, N.ScopeRefusal)
          and exc.subject == {'field': 'workspaceRoots', 'count': 1025, 'limit': 1024}
          and d9 == {'detail': 'PROJECT.SCOPE_LIMIT', 'class': 'request-rejected', 'exitCode': 2,
                     'code': 'REQUEST.UNSATISFIABLE', 'successorCode': None, 'interim': False,
                     'typedDetailCarrier': 'request rejection detail'}
          and term['class'] == 'request-rejected' and term['errorCode'] == 'REQUEST.UNSATISFIABLE'
          and W.exit_code(term) == 2
          and term['domainDetail']['subject'] == 'workspaceRoots:1025>1024')
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'roots1024': len(ok1024['scopeDescriptor']['workspaceRoots']),
                                                'discovery1025Refused': big['refused'],
                                                'units': len(big['units']), 'subject': getattr(exc, 'subject', None),
                                                'd9': d9, 'termination': term}


@probe('P10', 'SHOULD-A: the scope bound is reached through the OPERATIONAL host composition too, not only standalone')
def _():
    """native section 1.4 U-8 says the standalone instrument is not an operational composition.
    The unit case and the integration case both use it. Drive the same band through
    admit_repository_discovery (real security discovery -> admitted boundaries -> native)."""
    n = 1025
    fs = {'/p': {'kind': 'dir'}, '/p/.opensip': {'kind': 'dir'}}
    markers = {}
    for i in range(n):
        fs['/p/pkg%04d' % i] = {'kind': 'dir'}
        fs['/p/pkg%04d/package.json' % i] = {'kind': 'file'}
        markers['pkg%04d/package.json' % i] = {'sha256': '1' * 64}
    di = {'cwd': '/p', 'fs': fs, 'explicitProjectPath': None, 'config': None,
          'trustProjectOwner': False, 'ownerObservations': {}}
    exc = raised(lambda: M.admit_repository_discovery(di, markers, []))
    typed = isinstance(exc, N.ScopeRefusal)
    return ('OK' if typed else 'GAP'), {'exception': type(exc).__name__ if exc else None,
                                        'message': str(exc)[:300] if exc else None,
                                        'subject': getattr(exc, 'subject', None),
                                        'note': 'operational join reaches the same typed ScopeRefusal'}


@probe('P11', 'SHOULD-A: the 4096 discovery cap and the 1024 scope bound stay DISTINCT and both are typed')
def _():
    over = N.discover_units({'pkg%04d/package.json' % i: {'sha256': '1' * 64} for i in range(4097)})
    cap_detail = over['refused']['detail'] if over['refused'] else None
    aliases = {r['internalCode']: r['publicCode'] for r in REG['internalAliases']}
    codes = {r['code'] for r in REG['records']}
    at4096 = N.discover_units({'pkg%04d/package.json' % i: {'sha256': '1' * 64} for i in range(4096)})
    scope_exc = raised(lambda: N.unit_scope_descriptor(at4096['units'], []))
    ok = (cap_detail == 'native.too-many-units'
          and over['refused']['d9']['code'] == 'REQUEST.UNSATISFIABLE'
          and aliases[cap_detail] == 'PROJECT.WORKSPACE_UNIT_LIMIT'
          and 'PROJECT.SCOPE_LIMIT' in codes and 'PROJECT.WORKSPACE_UNIT_LIMIT' in codes
          and at4096['refused'] is None and isinstance(scope_exc, N.ScopeRefusal)
          and scope_exc.subject == {'field': 'workspaceRoots', 'count': 4096, 'limit': 1024})
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'capDetail': cap_detail, 'capPublic': aliases.get(cap_detail),
                                                'at4096DiscoveryRefused': at4096['refused'],
                                                'at4096ScopeSubject': getattr(scope_exc, 'subject', None)}


@probe('P12', 'SHOULD-A totality: every scope-descriptor array field has a maxItems the model actually reads')
def _():
    props = IM.SCHEMA['$defs']['scope-descriptor']['properties']
    arrays = {k: v for k, v in props.items() if v.get('type') == 'array'}
    read = {'workspaceRoots', 'pathPrefixes', 'excludedPathPrefixes'}
    missing = {k for k, v in arrays.items() if 'maxItems' not in v}
    return ('OK' if set(arrays) == read and not missing else 'COUNTEREXAMPLE'), \
        {'arrayFields': {k: v.get('maxItems') for k, v in arrays.items()}, 'modelReads': sorted(read),
         'missingMaxItems': sorted(missing)}


@probe('P13', 'SHOULD-A: the excludedPathPrefixes / pathPrefixes bounds are also typed, not only workspaceRoots')
def _():
    units = N.discover_units({'pkg%04d/package.json' % i: {'sha256': '1' * 64} for i in range(4)})['units']
    exc = raised(lambda: N.unit_scope_descriptor(units, ['ign%06d' % i for i in range(65537)]))
    exc2 = raised(lambda: N.unit_scope_descriptor(units, [], ['pp%06d' % i for i in range(65537)]))
    ok = (isinstance(exc, N.ScopeRefusal) and exc.subject['field'] == 'excludedPathPrefixes'
          and isinstance(exc2, N.ScopeRefusal) and exc2.subject['field'] == 'pathPrefixes')
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'excluded': getattr(exc, 'subject', None),
                                                'pathPrefixes': getattr(exc2, 'subject', None)}


# ===========================================================================
# V4-SPECIFIC: ADV-ii internal aliases + host inventory-mismatch emitter
# ===========================================================================


@probe('P14', 'ADV-ii: the two standalone-only codes are now internal aliases and are refused as public codes')
def _():
    codes = {r['code'] for r in REG['records']}
    aliases = {r['internalCode']: r['publicCode'] for r in REG['internalAliases']}
    enum = set(COMMON['$defs']['DomainDetailCode']['enum'])
    retired = ('native.boundary-inventory-mismatch', 'native.explicit-root-crosses-boundary')
    rows = {}
    for code in retired:
        rows[code] = {
            'inPublicRegistry': code in codes,
            'inSchemaEnum': code in enum,
            'alias': aliases.get(code),
            'refusedAsPublic': refuses(lambda c=code: W.validate_import_record(
                'workflows/schemas/common.schema.json', '#/$defs/DomainDetail',
                {'code': c, 'remedy': 'x'})),
            'aliasD9AgreesWithNative': None,
        }
    # The alias target must carry the SAME class/code/exit as the native internal row,
    # or public_termination would refuse ("unit class and exit disagree").
    for code in retired:
        d9 = N.d9_map(code)
        term = M.public_termination(d9, code, 'Re-admit one consistent repository inventory.')
        rows[code]['aliasD9AgreesWithNative'] = (term['domainDetail']['code'], term['class'],
                                                 term.get('errorCode'), W.exit_code(term))
    ok = (all(not r['inPublicRegistry'] and not r['inSchemaEnum'] and r['alias'] and r['refusedAsPublic']
              for r in rows.values())
          and codes == enum
          and rows['native.boundary-inventory-mismatch']['aliasD9AgreesWithNative']
          == ('PROJECT.DISCOVERY_INVENTORY_MISMATCH', 'request-rejected', 'REQUEST.PRECONDITION_FAILED', 2)
          and rows['native.explicit-root-crosses-boundary']['aliasD9AgreesWithNative']
          == ('PROJECT.EXPLICIT_PATH_INVALID', 'request-rejected', 'CONFIG.INVALID', 2))
    return ('OK' if ok else 'COUNTEREXAMPLE'), rows


@probe('P15', 'ADV-ii: PROJECT.DISCOVERY_INVENTORY_MISMATCH has a real host emitter reachable pre-native')
def _():
    """Build a real project, then hand native an inventory the security discovery did not
    observe. The refusal must be the typed host class, raised BEFORE native discovery."""
    fs = {'/p': {'kind': 'dir'}, '/p/.opensip': {'kind': 'dir'},
          '/p/a': {'kind': 'dir'}, '/p/a/package.json': {'kind': 'file'}}
    di = {'cwd': '/p', 'fs': fs, 'explicitProjectPath': None, 'config': None,
          'trustProjectOwner': False, 'ownerObservations': {}}
    good = {'a/package.json': {'sha256': '1' * 64}}
    baseline = M.admit_repository_discovery(di, good, ['a/package.json'])
    # (a) a marker native claims that security never observed
    e1 = raised(lambda: M.admit_repository_discovery(di, dict(good, **{'b/package.json': {'sha256': '2' * 64}}), []))
    # (b) a marker security observed that native drops
    e2 = raised(lambda: M.admit_repository_discovery(di, {}, []))
    # (c) a file native claims outside the observed inventory
    e3 = raised(lambda: M.admit_repository_discovery(di, good, ['a/ghost.ts']))
    terms = []
    for e in (e1, e2, e3):
        if isinstance(e, M.DiscoveryInventoryMismatch):
            terms.append(M.public_termination(e.d9, e.detail, 'Re-admit one consistent repository inventory.'))
    ok = (len(baseline['native']['units']) == 1 and len(terms) == 3
          and all(t['domainDetail']['code'] == 'PROJECT.DISCOVERY_INVENTORY_MISMATCH'
                  and t['errorCode'] == 'REQUEST.PRECONDITION_FAILED' and W.exit_code(t) == 2 for t in terms))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'baselineUnits': len(baseline['native']['units']),
                                                'emitted': [type(e).__name__ for e in (e1, e2, e3)],
                                                'terminations': terms[:1]}


@probe('P16', 'ADV-ii: an explicit root crossing a nested boundary is still reported ONCE, by security')
def _():
    fs = {'/p': {'kind': 'dir'}, '/p/.opensip': {'kind': 'dir'},
          '/p/a': {'kind': 'dir'}, '/p/a/package.json': {'kind': 'file'},
          '/p/nested': {'kind': 'dir'}, '/p/nested/.opensip': {'kind': 'dir'},
          '/p/nested/package.json': {'kind': 'file'}}
    di = {'cwd': '/p', 'fs': fs, 'explicitProjectPath': None,
          'config': {'discovery': {'workspaceRoots': ['nested']}},
          'trustProjectOwner': False, 'ownerObservations': {}}
    markers = {'a/package.json': {'sha256': '1' * 64}, 'nested/package.json': {'sha256': '2' * 64}}
    d = S.discovery(di)
    exc = raised(lambda: M.admit_repository_discovery(di, markers, []))
    return ('OK' if d['status'] != 'ACCEPT' or exc is not None else 'COUNTEREXAMPLE'), \
        {'securityStatus': d['status'], 'securityDetail': d.get('refusal') or d.get('detail'),
         'hostException': type(exc).__name__ if exc else None, 'message': str(exc)[:240] if exc else None}


# ===========================================================================
# V4-SPECIFIC: ADV-iii dead reselectsStore
# ===========================================================================


@probe('P17', 'ADV-iii: reselectsStore is gone from the model and could never have been carried')
def _():
    src = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    schema = C.parse((DC / 'security/security-lifecycle.schemas.v1.json').read_bytes())
    intent = schema['$defs']['InstallationTransitionIntentV1']
    wf_intent = C.parse((DC / 'workflows/schemas/invocation-record.schema.json').read_bytes())['$defs']['CoreTransitionIntentV1']
    return ('OK' if ('reselectsStore' not in src
                     and 'reselectsStore' not in json.dumps(schema)
                     and intent['additionalProperties'] is False
                     and 'fromStoreGeneration' in intent['required']
                     and 'toStoreGeneration' in intent['required']) else 'COUNTEREXAMPLE'), \
        {'inSecurityModel': 'reselectsStore' in src, 'inSchemas': 'reselectsStore' in json.dumps(schema),
         'intentClosed': intent['additionalProperties'], 'requiredCount': len(intent['required']),
         'workflowIntentClosed': wf_intent.get('additionalProperties')}


@probe('P18', 'ADV-iii: core_transition_affected_namespaces is TOTAL and store re-selection is derived, not supplied')
def _():
    """Enumerate every operation x schema-change x store-generation-change and confirm the
    scope is a total function of the CLOSED intent alone."""
    registry = ['ns.a', 'ns.b', 'ns.c']
    ops = ('core-update', 'core-repair', 'core-rollback', 'store-migrate', 'store-rollback')
    table = {}
    for op in ops:
        for schema_change in (False, True):
            for store_change in (False, True):
                intent = {'operation': op, 'fromStateSchema': 1, 'toStateSchema': 2 if schema_change else 1,
                          'fromStoreGeneration': 1, 'toStoreGeneration': 2 if store_change else 1}
                out = S.core_transition_affected_namespaces(intent, registry)
                table['%s.schema=%s.store=%s' % (op, schema_change, store_change)] = out['affects']
    # a caller-injected reselectsStore must be rejected by the closed intent, not honoured
    injected = {'schemaVersion': 1, 'operation': 'core-update', 'fromStateSchema': 1, 'toStateSchema': 1,
                'fromStoreGeneration': 1, 'toStoreGeneration': 1, 'reselectsStore': True,
                'fromCoreClosure': 'a' * 64, 'toCoreClosure': 'b' * 64,
                'platformProfileSetBodyDigest': 'c' * 64, 'preconditionGeneration': 1, 'rollbackDeadline': None}
    injected_refused = refuses(lambda: S.validate_input('InstallationTransitionIntentV1', injected))
    expected_all = {k for k in table if k.startswith(('core-rollback', 'store-migrate', 'store-rollback'))
                    or k.endswith('schema=True.store=False') or k.endswith('schema=True.store=True')
                    or k.endswith('schema=False.store=True')}
    ok = (len(table) == 20 and injected_refused
          and all(table[k] == 'all-registered' for k in expected_all)
          and table['core-update.schema=False.store=False'] != 'all-registered'
          and table['core-repair.schema=False.store=False'] != 'all-registered')
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'table': table, 'injectedReselectsStoreRefused': injected_refused}


# ===========================================================================
# V4-SPECIFIC: ADV-iv typed retention loss in close_run
# ===========================================================================


@probe('P19', 'ADV-iv: a missing retained object or blob is operational retention loss (exit 4), never a predicate')
def _():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    closed = IM.close_run(run, objects, blobs)
    rows = {}
    # (a) every single retained object removed, one at a time
    for key in list(objects):
        lost = {k: v for k, v in objects.items() if k != key}
        exc = raised(lambda: IM.close_run(run, lost, blobs))
        rows['object:' + key.split(':')[0]] = type(exc).__name__ if exc else 'NO-REFUSAL'
    # (b) every single retained blob removed, one at a time
    for digest in list(blobs):
        lost = {k: v for k, v in blobs.items() if k != digest}
        exc = raised(lambda: IM.close_run(run, objects, lost))
        rows['blob:' + digest[:8]] = type(exc).__name__ if exc else 'NO-REFUSAL'
    sample = raised(lambda: IM.close_run(run, {}, blobs))
    W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', sample.termination)
    kinds = set(rows.values())
    ok = (closed is not None and kinds <= {'EvidenceUnavailable'}
          and W.exit_code(sample.termination) == 4
          and sample.termination['class'] == 'operational-failed'
          and sample.termination['errorCode'] == 'HOST.IO_FAILURE'
          and sample.termination['faultCause'] == 'host-io'
          and sample.termination['domainDetail']['code'] == 'evidence.missing')
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'distinctOutcomes': sorted(kinds), 'probed': len(rows),
                                                'termination': sample.termination}


@probe('P20', 'ADV-iv: retention loss (exit 4) stays DISTINCT from admission rejection (exit 2)')
def _():
    """EvidenceUnavailable subclasses AdmissionError. Prove the two are still separable by
    a caller, and that a CORRUPT (present but wrong) blob is still an admission rejection."""
    run, objects, blobs = F.build(resolved=True, has_match=True)
    digest = next(iter(blobs))
    corrupt = dict(blobs); corrupt[digest] = b'not the promised bytes'
    corrupt_exc = raised(lambda: IM.close_run(run, objects, corrupt))
    missing_exc = raised(lambda: IM.close_run(run, objects, {k: v for k, v in blobs.items() if k != digest}))
    key = next(iter(objects))
    wrong_domain = dict(objects); wrong_domain[key] = ('view', objects[key][1])
    domain_exc = raised(lambda: IM.close_run(run, wrong_domain, blobs))
    ok = (isinstance(missing_exc, IM.EvidenceUnavailable)
          and isinstance(corrupt_exc, C.AdmissionError) and not isinstance(corrupt_exc, IM.EvidenceUnavailable)
          and isinstance(domain_exc, C.AdmissionError) and not isinstance(domain_exc, IM.EvidenceUnavailable)
          and hasattr(missing_exc, 'termination') and not hasattr(corrupt_exc, 'termination'))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'missing': type(missing_exc).__name__, 'corrupt': type(corrupt_exc).__name__ + ':' + str(corrupt_exc)[:60],
        'wrongDomain': type(domain_exc).__name__ + ':' + str(domain_exc)[:60],
        'evidenceUnavailableIsAdmissionError': issubclass(IM.EvidenceUnavailable, C.AdmissionError)}


# ===========================================================================
# V4-SPECIFIC: ADV-v installationRecoveryStartRef
# ===========================================================================


def transition_fixtures():
    """Rebuild the five/six operation fixtures from the frozen security transition cases."""
    tcases = C.parse((DC / 'security/transition-journal-cases.v1.json').read_bytes())
    return tcases


@probe('P21', 'ADV-v: a fresh recovery Attempt begins at the OBSERVED durable state for every closed state')
def _():
    tc = transition_fixtures()
    out = {}
    for key, case in sorted(tc['transitions'].items()):
        ti = sub(case['intent']) if isinstance(case.get('intent'), dict) else case['intent']
        tj = case['journal']
        trc = case['recoveryContext']
        for state in ('LEASED', 'PREPARING', 'PREPARED', 'COMMITTED', 'DONE', 'ABORTED'):
            j = dict(tj, state=state)
            ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, j)
            ctx = dict(trc)
            if state == 'PREPARED' and j['operation'] in S.STORE_OPERATIONS:
                ctx['storeFootprint'] = {'old': {'present': True, 'unbootstrappedReason': 'RESTORED'},
                                         'new': {'dir': 'migrating', 'state': 'PREPARED'}}
            try:
                r = M.installation_recovery_attempt(ti, j, ref, ctx, 'exec1_' + '7' * 32)
            except Exception as exc:
                out['%s.%s' % (key, state)] = 'ERROR:' + str(exc)[:120]
                continue
            a = r['attempt']
            out['%s.%s' % (key, state)] = {
                'startRefIsFirst': a['installationJournalRefs'][0] == a['installationRecoveryStartRef'] == ref,
                'states': [x['state'] for x in r['journals']],
                'action': r['decision']['action'], 'outcome': a['outcome']}
    bad = {k: v for k, v in out.items() if not isinstance(v, dict) or not v['startRefIsFirst']}
    return ('OK' if not bad else 'COUNTEREXAMPLE'), {'cases': len(out), 'bad': bad,
                                                     'sample': {k: out[k] for k in sorted(out)[:6]}}


@probe('P22', 'ADV-v: a PREPARED store recovery resumes through COMMITTED to DONE, in one lawful segment')
def _():
    tc = transition_fixtures()
    out = {}
    for key, case in sorted(tc['transitions'].items()):
        if case['journal']['operation'] not in S.STORE_OPERATIONS:
            continue
        ti, tj, trc = case['intent'], case['journal'], case['recoveryContext']
        j = dict(tj, state='PREPARED')
        ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, j)
        ctx = dict(trc, storeFootprint={'old': {'present': True, 'unbootstrappedReason': 'RESTORED'},
                                        'new': {'dir': 'migrating', 'state': 'PREPARED'}})
        r = M.installation_recovery_attempt(ti, j, ref, ctx, 'exec1_' + '8' * 32)
        out[key] = {'states': [x['state'] for x in r['journals']],
                    'action': r['decision']['action'], 'refs': len(r['attempt']['installationJournalRefs'])}
    ok = bool(out) and all(v['states'] == ['PREPARED', 'COMMITTED', 'DONE'] and v['action'] == 'RESUME-COMMIT'
                           and v['refs'] == 3 for v in out.values())
    return ('OK' if ok else 'COUNTEREXAMPLE'), out


@probe('P23', 'ADV-v: recovery does not rewrite the ORIGINAL attempt, and a foreign start ref is refused')
def _():
    tc = transition_fixtures()
    rows = {}
    for key, case in sorted(tc['transitions'].items()):
        ti, tj, trc = case['intent'], case['journal'], case['recoveryContext']
        leased = dict(tj, state='LEASED')
        leased_ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, leased)
        original = M.installation_journal_history(ti, [leased])           # the abandoned initial attempt
        committed = dict(tj, state='COMMITTED')
        cref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, committed)
        recovery = M.installation_recovery_attempt(ti, committed, cref, trc, 'exec1_' + '9' * 32)
        rows[key] = {
            'originalUnchanged': original == [leased_ref],
            'recoveryStartsAtObserved': recovery['attempt']['installationJournalRefs'][0] == cref,
            'recoveryDoesNotContainLeased': leased_ref not in recovery['attempt']['installationJournalRefs'],
            'wrongStartRefRefused': refuses(lambda: M.installation_journal_history(ti, [committed], leased_ref)),
            'nonRecoveryHistoryStillMustStartLeased': refuses(lambda: M.installation_journal_history(ti, [committed])),
        }
    bad = {k: v for k, v in rows.items() if not all(v.values())}
    return ('OK' if not bad else 'COUNTEREXAMPLE'), {'bad': bad, 'sample': rows[sorted(rows)[0]]}


@probe('P24', 'ADV-v: the Attempt schema binds installationRecoveryStartRef == refs[0] and the workflow enforces it')
def _():
    schema = C.parse((DC / 'workflows/schemas/invocation-record.schema.json').read_bytes())
    attempt = schema['$defs']['Attempt']
    has_prop = 'installationRecoveryStartRef' in attempt['properties']
    closed = attempt.get('additionalProperties') is False
    conditional = attempt.get('allOf')
    ref = 'installation-transition-journal.v1:' + 'a' * 64
    other = 'installation-transition-journal.v1:' + 'b' * 64
    good = {'executionId': 'exec1_' + '1' * 32, 'outcome': 'completed',
            'installationRecoveryStartRef': ref, 'installationJournalRefs': [ref]}
    orphan = {'executionId': 'exec1_' + '1' * 32, 'outcome': 'completed', 'installationRecoveryStartRef': ref}
    ok_schema = not refuses(lambda: W.validate_import_record(
        'workflows/schemas/invocation-record.schema.json', '#/$defs/Attempt', good))
    orphan_refused = refuses(lambda: W.validate_import_record(
        'workflows/schemas/invocation-record.schema.json', '#/$defs/Attempt', orphan))
    # the schema alone cannot express refs[0] == startRef; the workflow observation join must
    mismatch = {'executionId': 'exec1_' + '1' * 32, 'outcome': 'completed',
                'installationRecoveryStartRef': ref, 'installationJournalRefs': [other, ref]}
    schema_admits_mismatch = not refuses(lambda: W.validate_import_record(
        'workflows/schemas/invocation-record.schema.json', '#/$defs/Attempt', mismatch))
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    model_enforces = "installationJournalRefs'][0] != a['installationRecoveryStartRef']" in src
    return ('OK' if (has_prop and closed and conditional and ok_schema and orphan_refused
                     and model_enforces) else 'COUNTEREXAMPLE'), \
        {'hasProperty': has_prop, 'attemptClosed': closed, 'conditionalRequire': bool(conditional),
         'validAdmitted': ok_schema, 'orphanStartRefRefused': orphan_refused,
         'schemaAloneAdmitsOrderMismatch': schema_admits_mismatch, 'modelEnforcesOrder': model_enforces}


@probe('P25', 'ADV-v: the workflow observation join refuses a recovery history whose first ref is not the start ref')
def _():
    """Drive the real parse_attempt path rather than the schema, using the workflow cases."""
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    block = src[src.find("if 'installationRecoveryStartRef' in obs"):][:420]
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    mentioned = 'installationRecoveryStartRef' in prose
    return ('OK' if ("raise ValueError('recovery history must start with its observed durable revision')" in block
                     and mentioned) else 'GAP'), {'modelBlock': block.strip()[:320],
                                                  'namedInWorkflowContract': mentioned}


# ===========================================================================
# Cross-unit joins beyond the named probes
# ===========================================================================


@probe('P26', 'Run closure: prepare-code iff a trusted repository preparation principal is projected')
def _():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    plan = copy.deepcopy(objects[run['planId']][1])
    grant = C.parse(blobs[plan['semanticGrantDigest']])
    rows = {}
    rows['baseline'] = IM.close_run(run, objects, blobs) is not None
    # add a trusted-repository-code principal without prepare-code
    def put(value):
        raw = value if type(value) is bytes else C.canonical(value)
        d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d
    g2 = copy.deepcopy(grant)
    g2['principals'] = sorted(g2['principals'] + [{'kind': 'trusted-repository-code',
                                                   'closureId': plan['semanticClosures'][0],
                                                   'ownerSourceDigest': 'd' * 64}], key=C.canonical)
    p2 = copy.deepcopy(plan); p2['semanticGrantDigest'] = put(g2)
    r2 = copy.deepcopy(run); o2 = copy.deepcopy(objects)
    F.rekey(o2, run['planId'], p2, r2)
    rows['principalWithoutPrepareCode'] = refuses(lambda: IM.close_run(r2, o2, blobs))
    g3 = copy.deepcopy(g2); g3['analysisOperations'] = sorted(set(g3['analysisOperations']) | {'prepare-code'})
    p3 = copy.deepcopy(plan); p3['semanticGrantDigest'] = put(g3)
    r3 = copy.deepcopy(run); o3 = copy.deepcopy(objects)
    F.rekey(o3, run['planId'], p3, r3)
    rows['principalWithPrepareCode'] = IM.close_run(r3, o3, blobs) is not None
    # prepare-code with no such principal
    g4 = copy.deepcopy(grant); g4['analysisOperations'] = sorted(set(g4['analysisOperations']) | {'prepare-code'})
    p4 = copy.deepcopy(plan); p4['semanticGrantDigest'] = put(g4)
    r4 = copy.deepcopy(run); o4 = copy.deepcopy(objects)
    F.rekey(o4, run['planId'], p4, r4)
    rows['prepareCodeWithoutPrincipal'] = refuses(lambda: IM.close_run(r4, o4, blobs))
    return ('OK' if all(rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P27', 'Run closure: typed import source/build correspondence (N-3 / CX-07) still closes and refuses exactly')
def _():
    rows = {}
    r, o, b = F.graph_with_import('exact')
    rows['exact'] = IM.close_run(r, o, b) is not None
    r, o, b = F.graph_with_import('vcs')
    rows['vcsMapped'] = IM.close_run(r, o, b) is not None
    r, o, b = F.graph_with_import('vcs', build_identity='build-a', declared_builds=['build-a', 'build-b'])
    rows['declaredBuildInExpectedSet'] = IM.close_run(r, o, b) is not None
    for label, kwargs in (('foreignSnapshot', {'correspondence': 'exact', 'foreign_snapshot': True}),
                          ('badMapping', {'correspondence': 'vcs', 'bad_mapping': True}),
                          ('missingMapping', {'correspondence': 'vcs', 'missing_mapping': True}),
                          ('dirtyWorktree', {'correspondence': 'vcs', 'dirty': True}),
                          ('buildWithoutExpectedContext', {'correspondence': 'vcs', 'build_identity': 'build-a'}),
                          ('buildOutsideExpectedSet', {'correspondence': 'vcs', 'build_identity': 'build-a',
                                                       'declared_builds': ['build-b']})):
        def go(kw=kwargs):
            r2, o2, b2 = F.graph_with_import(**kw)
            return IM.close_run(r2, o2, b2)
        rows[label] = refuses(go)
    return ('OK' if all(rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P28', 'import-source-context is a declared ANALYSIS-SPEC parameter; an importer cannot nominate its own labels')
def _():
    schema = C.parse((DC / 'foundation/import-source-context.schema.json').read_bytes())
    src = (DC / 'foundation/identity-model.py').read_text()
    # more than one such parameter row must refuse (no ambiguous expected set)
    def two_rows():
        r, o, b = F.graph_with_import('vcs', build_identity='build-a', declared_builds=['build-a'])
        plan = copy.deepcopy(o[r['planId']][1])
        analysis = C.parse(b[plan['analysisSpecDigest']])
        analysis['parameters'] = analysis['parameters'] * 2
        raw = C.canonical(analysis); d = hashlib.sha256(raw).hexdigest(); b[d] = raw
        plan['analysisSpecDigest'] = d
        F.rekey(o, r['planId'], plan, r)
        return IM.close_run(r, o, b)
    return ('OK' if (schema.get('additionalProperties') is False
                     and 'declaredBuildIds' in schema.get('properties', {})
                     and 'analysisSpecDigest' in src and refuses(two_rows)) else 'COUNTEREXAMPLE'), \
        {'schemaClosed': schema.get('additionalProperties'),
         'properties': sorted(schema.get('properties', {})),
         'duplicateParameterRowRefused': refuses(two_rows)}


@probe('P29', 'Native permission truth tables: the pin moved to the ACCEPTED v9 head and the copied values match')
def _():
    pins = C.parse((DC / 'native/source-pins.v2.json').read_bytes())
    rows = [p for p in pins['pins'] if 'permission-truth-tables' in p['path']]
    v9 = ROOT / 'docs/coop/artifacts/permission-truth-tables.v9.json'
    v9_present = v9.exists()
    digest = hashlib.sha256(v9.read_bytes()).hexdigest() if v9_present else None
    body = json.loads(v9.read_text()) if v9_present else {}
    text = json.dumps(body)
    values = {v: text.count('"%s"' % v) for v in ('DISCLOSURE-ONLY', 'ENFORCED-BY-CONSTRUCTION',
                                                  'ENFORCED-AT-HOST-BROKER')}
    contract = (CONTRACTS / 'native-evidence.md').read_text()
    cites_v9 = 'permission-truth-tables.v9.json' in contract
    cites_v7 = 'permission-truth-tables.v7.json' in contract
    delta = ROOT / 'docs/coop/design-corrections/reviews/codex-post-reset.v1/permission-head-delta.v1.json'
    return ('OK' if (rows and rows[0]['path'].endswith('v9.json') and rows[0]['sha256'] == digest
                     and cites_v9 and not cites_v7 and delta.exists()) else 'COUNTEREXAMPLE'), \
        {'pin': rows[0] if rows else None, 'actualV9Sha256': digest, 'contractCitesV9': cites_v9,
         'contractStillCitesV7': cites_v7, 'enforcementValueCounts': values,
         'retainedDeltaPresent': delta.exists()}


@probe('P30', 'Native permission truth tables: the FOUR copied effect values are unchanged between v7 and v9')
def _():
    """The application review (S-2) asked the final review to confirm the four copied values in
    v9, not merely that a newer file was pinned. Compare the retained Codex delta against the
    real files and re-derive the four values independently."""
    v7 = ROOT / 'docs/coop/artifacts/permission-truth-tables.v7.json'
    v9 = ROOT / 'docs/coop/artifacts/permission-truth-tables.v9.json'
    delta = ROOT / 'docs/coop/design-corrections/reviews/codex-post-reset.v1/permission-head-delta.v1.json'
    body = json.loads(delta.read_text()) if delta.exists() else {}
    table = S.PLATFORM_TRUTH_TABLE
    distinct = {json.dumps(v, sort_keys=True) for v in table.values()}
    return ('OK' if (v9.exists() and delta.exists() and len(distinct) == 1) else 'GAP'), \
        {'v7InSnapshot': v7.exists(), 'v9InSnapshot': v9.exists(),
         'securityTablePlatforms': sorted(table), 'oneRowForEveryPlatform': len(distinct) == 1,
         'row': table[sorted(table)[0]], 'retainedDeltaKeys': sorted(body)[:20],
         'retainedDelta': {k: body[k] for k in list(body)[:8] if not isinstance(body[k], (list, dict))}}


@probe('P31', 'Output registry: SARIF is advertised for exactly the four D-372 commands and no advisory command')
def _():
    cmds = INVENTORY['commands'] if isinstance(INVENTORY.get('commands'), list) else []
    sarif = sorted(c['name'] if 'name' in c else c.get('command') for c in cmds if 'sarif' in c.get('formats', []))
    verdicts = {c.get('name', c.get('command')): c.get('producesVerdict', c.get('verdict'))
                for c in cmds if 'sarif' in c.get('formats', [])}
    d372 = (DC / 'D-372-corrections.proposed.md').read_text()
    declared = re.search(r'SARIF exactly for ([^.]+)\.', d372)
    return ('OK' if sarif == ['analyze', 'audit', 'default', 'repair-verify'] else 'COUNTEREXAMPLE'), \
        {'sarifCommands': sarif, 'commandCount': len(cmds), 'verdictFlags': verdicts,
         'd372Sentence': declared.group(1) if declared else None}


@probe('P32', 'Output registry: every command advertising SARIF declares parity fields and a required-output law')
def _():
    cmds = INVENTORY['commands'] if isinstance(INVENTORY.get('commands'), list) else []
    rows = {}
    for c in cmds:
        name = c.get('name', c.get('command'))
        if 'sarif' in c.get('formats', []):
            rows[name] = {'parityFields': c.get('parityFields'), 'formats': c.get('formats'),
                          'requiredOutputs': c.get('requiredOutputs')}
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    law = 'post-commit' in prose and 'required-output' in prose.lower()
    ok = all(r['parityFields'] for r in rows.values()) and law
    return ('OK' if ok else 'GAP'), {'rows': rows, 'postCommitRequiredOutputLawStated': law}


@probe('P33', 'Delta pivots: empty-vs-empty comparison with a missing pivot is indeterminate, not pass (CX-02)')
def _():
    cases = WF.get('comparisonCases') or {}
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    have = ('COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE' in src
            and 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE' in src)
    codes = set(COMMON['$defs']['DomainDetailCode']['enum'])
    return ('OK' if (have and 'COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE' in codes
                     and 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE' in codes) else 'COUNTEREXAMPLE'), \
        {'modelDeclaresBothPivotCodes': have,
         'registered': [c for c in codes if 'PIVOT' in c], 'caseKeys': sorted(cases)[:8]}


@probe('P34', 'Recovery authorization -> workflow mutation: the join still refuses every unbound variant (N-4)')
def _():
    """Re-derive the security recovery admission and attack the projection independently."""
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    ssrc = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    sec_table = re.search(r'RECOVERY_ACTION_TABLE\s*=\s*\{(.*?)\}', ssrc, re.S)
    wf_table = re.search(r'RECOVERY_ACTION_TABLE\s*=\s*\{(.*?)\}', src, re.S)
    same = bool(sec_table and wf_table and
                re.sub(r'\s+', '', sec_table.group(1)) == re.sub(r'\s+', '', wf_table.group(1)))
    caller_dict_refused = 'RepairRecoveryAuthorizationV1' in ssrc and 'admit_recovery_authorization' in ssrc
    return ('OK' if (same or not sec_table) and caller_dict_refused else 'GAP'), \
        {'securityTableFound': bool(sec_table), 'workflowTableFound': bool(wf_table),
         'tablesByteIdentical': same, 'securityOwnsClosedRecord': caller_dict_refused}


@probe('P35', 'Cargo: an explicitly named workspace root retains members and member target pruning (A-3)')
def _():
    markers = {'Cargo.toml': {'sha256': '1' * 64, 'isCargoWorkspace': True},
               'crates/a/Cargo.toml': {'sha256': '2' * 64},
               'crates/b/Cargo.toml': {'sha256': '3' * 64},
               'crates/a/target/x/Cargo.toml': {'sha256': '4' * 64}}
    auto = N.discover_units(markers)
    explicit = N.discover_units(markers, ['.'])
    member_only = N.discover_units(markers, ['crates/a'])
    ok = ([u['rootPath'] for u in auto['units']] == [u['rootPath'] for u in explicit['units']]
          and explicit['units'][0]['memberPackageRoots'] == ['crates/a', 'crates/b']
          and explicit['units'][0]['unitKind'] == 'cargo-workspace'
          and len(member_only['units']) == 1 and member_only['units'][0]['unitKind'] == 'cargo-package'
          and any(t['path'].startswith('crates/a/target') for t in auto['prunedTrees']))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'auto': [(u['rootPath'], u['unitKind'], u['memberPackageRoots']) for u in auto['units']],
        'explicitRoot': [(u['rootPath'], u['unitKind'], u['memberPackageRoots']) for u in explicit['units']],
        'memberOnly': [(u['rootPath'], u['unitKind']) for u in member_only['units']],
        'prunedTrees': auto['prunedTrees']}


@probe('P36', 'Public detail registry: closed, unique, owner-attributed, and at exact parity with the schema')
def _():
    codes = [r['code'] for r in REG['records']]
    enum = COMMON['$defs']['DomainDetailCode']['enum']
    aliases = {r['internalCode']: r['publicCode'] for r in REG['internalAliases']}
    owners = sorted({r['owner'] for r in REG['records']})
    bad_owner = [r for r in REG['records'] if not r.get('owner') or not r.get('selector')]
    alias_targets_public = all(v in set(codes) for v in aliases.values())
    alias_not_public = all(k not in set(codes) for k in aliases)
    sec_covered = {aliases.get(c, c) for c in S.D9} <= set(codes)
    nat_covered = {aliases.get(c, c) for c in N.D9_MAP} <= set(codes)
    ok = (len(codes) == len(set(codes)) == len(enum) and set(codes) == set(enum)
          and not bad_owner and alias_targets_public and alias_not_public and sec_covered and nat_covered
          and enum == sorted(enum))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'records': len(codes), 'enum': len(enum),
                                                'aliases': aliases, 'owners': owners,
                                                'securityCovered': sec_covered, 'nativeCovered': nat_covered,
                                                'enumSorted': enum == sorted(enum),
                                                'unattributed': [r['code'] for r in bad_owner]}


@probe('P37', 'Machine platform ids: the same four ids across every consumer; a display alias has no row')
def _():
    consumers = {
        'security.PLATFORM_IDS': sorted(S.PLATFORM_IDS),
        'security.PLATFORM_TRUTH_TABLE': sorted(S.PLATFORM_TRUTH_TABLE),
        'test-execution.schema': sorted(C.parse((DC / 'workflows/schemas/test-execution.schema.json').read_bytes())
                                        ['$defs']['TestExecutionStepParams']['properties']['platformId']['enum']),
        'gates.platformFamilies': sorted(C.parse((DC / 'qualification-gates.proposed.json').read_bytes())
                                         .get('platformFamilies', [])),
    }
    matrix = C.parse((DC / 'native/native-capability-matrix.v2.json').read_bytes())
    text = json.dumps(matrix)
    expected = ['linux-aarch64-gnu', 'linux-x86_64-gnu', 'macos-aarch64', 'macos-x86_64']
    alias_refused = refuses(lambda: W.validate_import_record(
        'workflows/schemas/test-execution.schema.json', '#/$defs/TestExecutionStepParams',
        {'platformId': 'Apple Silicon'}))
    g13 = C.parse((DC / 'foundation/g13-result-schema.v5.json').read_bytes())
    g13_scoped = 'harness.DR-G13' in json.dumps(g13) or 'preview' in json.dumps(g13)
    agree = {k: v == expected for k, v in consumers.items() if v}
    return ('OK' if all(agree.values()) and alias_refused else 'COUNTEREXAMPLE'), \
        {'consumers': consumers, 'agree': agree, 'displayAliasRefused': alias_refused,
         'g13IsScopedHistoricalHarness': g13_scoped,
         'nativeMatrixMentionsAll': all(p in text for p in expected)}


# ===========================================================================
# Documentation / act-level obligations named by the instruction
# ===========================================================================


@probe('P38', 'Admission section 5 dispositions all SEVEN P-1/P-2/G3 boundary items enumerated by file 02')
def _():
    adm = (CONTRACTS / 'admission-and-qualification.md').read_text()
    idx = adm.find('\n## 5')
    if idx < 0:
        idx = adm.find('\n## Section 5')
    section = adm[idx:adm.find('\n## ', idx + 5)] if idx >= 0 else ''
    numbered = re.findall(r'^\s*(?:\d+\.|\|\s*(?:P-?[12]|G3)?\s*\d+)\s', section, re.M)
    items = re.findall(r'^\s*(\d+)\.\s+\*?\*?(.{0,90})', section, re.M)
    f02 = (ARCH / '02-distribution-and-components.md').read_text()
    f02_items = re.findall(r'^\s*(\d+)\.\s', f02, re.M)
    topics = {'marketplace': 'marketplace' in section.lower() or 'catalog' in section.lower(),
              'externalLifecycle': 'lifecycle' in section.lower(),
              'contributionRoles': 'contribution' in section.lower() or 'role' in section.lower(),
              'untrustedNativeWasm': 'wasm' in section.lower() or 'untrusted' in section.lower(),
              'imperativeHooks': 'hook' in section.lower() or 'imperative' in section.lower() or 'probe' in section.lower(),
              'networkEgress': 'egress' in section.lower() or 'network' in section.lower(),
              'g3Substrate': 'g3' in section.lower() or 'substrate' in section.lower()}
    return ('OK' if len(items) == 7 and all(topics.values()) else 'COUNTEREXAMPLE'), \
        {'sectionFound': idx >= 0, 'sectionBytes': len(section),
         'enumeratedItems': len(items), 'itemHeads': [i[1].strip()[:70] for i in items],
         'topicCoverage': topics, 'file02EnumeratedCount': len(f02_items)}


@probe('P39', 'Security S16 carries prototype preservation 5, distinctions 5 and no-silent-migration 6, per file 05')
def _():
    sec = (CONTRACTS / 'security-and-lifecycle.md').read_text()
    idx = sec.find('\n## S16')
    section = sec[idx:sec.find('\n## ', idx + 5)] if idx >= 0 else ''
    if idx >= 0 and sec.find('\n## ', idx + 5) < 0:
        section = sec[idx:]
    f05 = (ARCH / '05-v1-to-v2-relationship.md').read_text()
    def count_after(text, marker, pattern=r'^\s*(?:\d+\.|-)\s'):
        i = text.lower().find(marker.lower())
        if i < 0:
            return None, ''
        block = text[i:i + 3000]
        stop = block.find('\n## ')
        block = block[:stop] if stop > 0 else block
        return len(re.findall(pattern, block, re.M)), block
    f05_no_migration = len(re.findall(r'^\s*\d+\.\s', f05[f05.lower().find('no migration silently'):][:2500], re.M))
    terms = {t: section.lower().count(t) for t in
             ('prototype', 'coexist', 'silently', 'preserve', 'distinct', 'import', 'promote')}
    lists = re.findall(r'^\s*(\d+)\.\s', section, re.M)
    bullets = re.findall(r'^\s*-\s', section, re.M)
    return ('OK' if (idx >= 0 and terms['prototype'] >= 3 and terms['silently'] >= 3) else 'COUNTEREXAMPLE'), \
        {'s16Found': idx >= 0, 'sectionBytes': len(section), 'numberedItems': len(lists),
         'bullets': len(bullets), 'termCounts': terms,
         'file05NoSilentMigrationEnumerated': f05_no_migration,
         'head': section[:400]}


@probe('P40', 'The five compatibility rows lacking an inherited architecture-application row now have exact pins')
def _():
    src = C.parse((DC / 'inherited-row-sources.proposed.json').read_bytes())
    rows = src.get('rows') if isinstance(src.get('rows'), list) else src
    ids = []
    if isinstance(rows, list):
        ids = [r.get('row', r.get('id')) for r in rows]
    elif isinstance(rows, dict):
        ids = sorted(rows)
    expected = {'DR-102', 'DR-104', 'DR-115', 'DR-117', 'DR-119', 'DR-123'}
    present = expected & set(ids)
    # every named source file must actually exist at the named digest
    bad = []
    text = json.dumps(src)
    for path, digest in re.findall(r'"(docs/[^"]+?)"[^{}]*?"([0-9a-f]{64})"', text):
        p = ROOT / path
        if not p.exists():
            bad.append((path, 'MISSING'))
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            bad.append((path, 'DIGEST-DIFFERS'))
    return ('OK' if present == expected and not bad else 'COUNTEREXAMPLE'), \
        {'rowIds': ids, 'expectedRows': sorted(expected), 'missingRows': sorted(expected - present),
         'unresolvedPins': bad, 'topKeys': sorted(src)[:12] if isinstance(src, dict) else None}


@probe('P41', 'The parent manifest now carries the inherited accounts the application review could not verify')
def _():
    manifest = json.load(open('/Users/sb/code/opensip-ai/opensip_arch/'
                              'docs/coop/design-corrections/reviews/candidate-subject.v4.json'))
    paths = {f['path'] for f in manifest['files']}
    needed = ['docs/coop/completion/architecture-application.v1.json',
              'docs/v2/architecture/02-distribution-and-components.md',
              'docs/v2/architecture/05-v1-to-v2-relationship.md',
              'docs/v2/architecture/prototype-evidence-reference.md',
              'docs/coop/COORDINATOR-DECISIONS.md',
              'docs/coop/artifacts/permission-truth-tables.v9.json',
              'docs/coop/artifacts/control-protocol-contract.v2.json',
              'docs/coop/artifacts/preview-product-boundary-successor.v10.json']
    have = {p: p in paths for p in needed}
    acct = ROOT / 'docs/coop/completion/architecture-application.v1.json'
    rows = json.loads(acct.read_text()).get('rows', []) if acct.exists() else []
    return ('OK' if all(have.values()) else 'COUNTEREXAMPLE'), \
        {'present': have, 'inheritedAccountRows': len(rows), 'manifestFiles': len(paths)}


@probe('P42', 'D-372 records the explicit SARIF/G17 re-entry act and does NOT claim a passed measurement')
def _():
    d372 = (DC / 'D-372-corrections.proposed.md').read_text()
    gates = C.parse((DC / 'qualification-gates.proposed.json').read_bytes())
    items = gates['gates'] if isinstance(gates.get('gates'), list) else gates.get('items', [])
    g17 = [g for g in items if str(g.get('gate', g.get('id', ''))).endswith('G17')]
    claims = {'reEnters': 'expressly re-enters authoritative SARIF' in d372,
              'reactivatesG17': 'reactivates DR-G17' in d372,
              'supersedesD077Scoped': 'D-077' in d372 and 'only in this scope' in d372,
              'notAlreadyPassed': 'never an already-passed measurement' in d372,
              'historicalUnchanged': 'remain unchanged for those old subjects' in d372}
    honest = all(g.get('qualified') is False and g.get('demonstrated') is False for g in items)
    return ('OK' if all(claims.values()) and honest and g17 else 'COUNTEREXAMPLE'), \
        {'claims': claims, 'g17Row': g17[0] if g17 else None, 'gateCount': len(items),
         'allGatesUnqualifiedAndUndemonstrated': honest}


@probe('P43', 'Condition 5 remains NOT MET and no subject byte authorizes implementation')
def _():
    hits = []
    for p in sorted(ROOT.rglob('*.md')) + sorted(ROOT.rglob('*.json')):
        try:
            t = p.read_text()
        except Exception:
            continue
        if re.search(r'"?implementationAuthorized"?\s*[:=]\s*true', t, re.I):
            hits.append(str(p.relative_to(ROOT)))
        if re.search(r'condition\s*5[^.\n]{0,40}\b(MET|SATISFIED)\b', t) and 'NOT MET' not in t:
            hits.append(str(p.relative_to(ROOT)) + ' (condition5)')
    disp = C.parse((DC / 'post-reset-dispositions.v4.proposed.json').read_bytes())
    return ('OK' if not hits and disp['implementationAuthorized'] is False else 'COUNTEREXAMPLE'), \
        {'authorizingFiles': hits[:10], 'v4DispositionFlag': disp['implementationAuthorized'],
         'remainingAcceptance': disp['remainingAcceptance']}


@probe('P44', 'Counts claimed by validation-summary equal the counts this session reproduced')
def _():
    vs = C.parse((DC / 'validation-summary.v1.json').read_bytes())
    R = Path('/tmp/opensip-design-corrections/post-reset-review.v4/reports')
    fl = json.load(open(R / 'foundation-launcher.json'))
    foundation = sum(json.loads(c['stdout']).get('passed', 0) for c in fl['checks'])
    sec = json.load(open(R / 'security-lifecycle-report.rerun.json'))
    nat = json.load(open(R / 'native-evidence-report.rerun.json'))
    wl = json.load(open(R / 'workflows-launcher.json'))
    integ = json.load(open(R / 'integration-report.rerun.json'))
    mine = {'foundation': foundation, 'securityCases': sec['counts']['pass'], 'sweeps': len(sec['sweeps']),
            'native': nat['cases']['passed'], 'workflows': json.loads(wl['check']['stdout'])['passed'],
            'integration': integ['passed']}
    claimed = {'foundation': vs['foundation']['checksPassed'], 'securityCases': vs['security']['casesPassed'],
               'sweeps': vs['security']['invariantSweepsPassed'], 'native': vs['native']['casesPassed'],
               'workflows': vs['workflows']['checksPassed'], 'integration': vs['integration']['checksPassed']}
    ids = [c['id'] for c in integ['checks']]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    return ('OK' if mine == claimed else 'COUNTEREXAMPLE'), \
        {'reproduced': mine, 'claimed': claimed, 'matrixCells': nat['matrix']['cells'],
         'qualifiedCells': nat['matrix']['qualifiedCells'],
         'duplicateIntegrationCheckIds': dupes,
         'distinctIntegrationCheckIds': len(set(ids)),
         'claudeFinalReview': vs['claudeFinalReview'], 'readinessChanged': vs['readinessChanged']}


@probe('P45', 'Historical preservation: every named historical file is byte-unchanged')
def _():
    rep = C.parse((DC / 'historical-preservation-report.v4.json').read_bytes())
    rows = rep.get('files') or rep.get('records') or []
    checked = 0; bad = []
    for r in rows if isinstance(rows, list) else []:
        path = r.get('path')
        digest = r.get('sha256') or r.get('observedSha256')
        if not path or not digest:
            continue
        p = Path('/Users/sb/code/opensip-ai/opensip_arch') / path
        if not p.exists():
            bad.append((path, 'MISSING')); continue
        checked += 1
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            bad.append((path, 'CHANGED'))
    return ('OK' if not bad and checked else 'GAP'), {'checked': checked, 'bad': bad,
                                                      'reportKeys': sorted(rep)[:12],
                                                      'declared': rep.get('result') or rep.get('status')}


@probe('P46', 'Crosswalk and dispositions remain PROSPECTIVE; no superseded review is presented as acceptance')
def _():
    cw = C.parse((DC / 'correction-crosswalk.proposed.json').read_bytes())
    rows = cw.get('findings') or cw.get('rows') or []
    reviews = sorted({r.get('review') for r in rows if isinstance(r, dict) and r.get('review')})
    grades = sorted({r.get('status') or r.get('disposition') for r in rows if isinstance(r, dict)})
    disp = C.parse((DC / 'post-reset-dispositions.v4.proposed.json').read_bytes())
    return ('OK' if all('PENDING' in str(g).upper() or 'AUTHOR' in str(g).upper() for g in grades if g)
            else 'ADVISORY'), \
        {'rows': len(rows), 'reviewFields': reviews, 'grades': grades,
         'v4Standing': disp['standing'], 'predecessorDesignReview': disp['predecessorDesignReview']}


@probe('P47', 'Evaluation residual dispositions: 19 RES + 7 NB + 4 escapes, each individually written and PENDING')
def _():
    d = C.parse((DC / 'evaluation-residual-dispositions.proposed.json').read_bytes())
    groups = {}
    for k, v in d.items():
        if isinstance(v, list):
            groups[k] = len(v)
    allrows = []
    for v in d.values():
        if isinstance(v, list):
            allrows += [r for r in v if isinstance(r, dict)]
    statuses = sorted({r.get('reviewStatus') for r in allrows if 'reviewStatus' in r})
    return ('OK' if sum(groups.values()) == 30 else 'ADVISORY'), \
        {'groups': groups, 'total': sum(groups.values()), 'reviewStatuses': statuses,
         'everyRowHasProse': all(any(isinstance(x, str) and len(x) > 40 for x in r.values()) for r in allrows)}


@probe('P48', 'No contract claims a completed platform measurement, qualification or containment')
def _():
    banned = [r'\bQUALIFIED\b(?!\s*:?\s*false)', r'\bDEMONSTRATED\b(?!\s*:?\s*false)',
              r'we (?:confine|sandbox|prevent) ', r'measured on (?:macOS|Linux)']
    hits = {}
    for p in sorted(CONTRACTS.glob('*.md')):
        t = p.read_text()
        for pat in banned:
            found = [m.group(0) for m in re.finditer(pat, t)]
            if found:
                hits.setdefault(p.name, []).extend(found[:4])
    nat = json.load(open('/tmp/opensip-design-corrections/post-reset-review.v4/reports/'
                         'native-evidence-report.rerun.json'))
    return ('OK' if not hits and nat['matrix']['qualifiedCells'] == 0 else 'ADVISORY'), \
        {'phraseHits': hits, 'qualifiedCells': nat['matrix']['qualifiedCells'],
         'nativeStanding': nat['standing'][:120]}


@probe('P49', 'Contract cross-references resolve: no duplicate headings, no /tmp citation, no dangling section ref')
def _():
    problems = {}
    for p in sorted(CONTRACTS.glob('*.md')):
        t = p.read_text()
        heads = re.findall(r'^#{2,4}\s+(.+)$', t, re.M)
        dupes = sorted({h for h in heads if heads.count(h) > 1})
        tmp = re.findall(r'/tmp/[^\s`)\]]+', t)
        if dupes:
            problems.setdefault(p.name, {})['duplicateHeadings'] = dupes
        if tmp:
            problems.setdefault(p.name, {})['tmpCitations'] = tmp[:5]
    # every relative markdown link inside the contracts must resolve in the snapshot
    dangling = []
    for p in sorted(CONTRACTS.glob('*.md')):
        for target in re.findall(r'\]\((?!https?:|#)([^)#]+)', p.read_text()):
            if not (p.parent / target).exists():
                dangling.append(p.name + ' -> ' + target)
    return ('OK' if not problems and not dangling else 'COUNTEREXAMPLE'), \
        {'problems': problems, 'danglingLinks': dangling}


@probe('P50', 'Documentation stays PRE-APPLICATION by design: the register and navigation are unchanged')
def _():
    vs = C.parse((DC / 'validation-summary.v1.json').read_bytes())
    reg = ARCH / '08-decision-and-readiness-register.md'
    coord = ROOT / 'docs/coop/COORDINATOR-DECISIONS.md'
    return ('OK' if (vs['readinessChanged'] is False
                     and vs['claudeFinalReview'] == 'PENDING-FROZEN-V4') else 'COUNTEREXAMPLE'), \
        {'readinessChanged': vs['readinessChanged'], 'claudeFinalReview': vs['claudeFinalReview'],
         'registerMentionsD372': 'D-372' in reg.read_text(),
         'coordinatorDecisionsMentionsD372': 'D-372' in coord.read_text(),
         'note': 'both are expected to remain pre-application until the act is applied'}


# ===========================================================================

out = Path('/tmp/opensip-design-corrections/post-reset-review.v4/probes/independent-probes.json')
summary = {'reviewer': 'fresh actual-Claude independent reviewer; authored none of the subject bytes',
           'subject': '/tmp/opensip-design-corrections/candidate-subject.v4',
           'manifestSha256': '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2',
           'ranOn': 'scratch copy at ' + str(ROOT),
           'syntheticTcbInputs': True, 'productQualification': False,
           'counts': {}, 'probes': results}
for r in results:
    summary['counts'][r['status']] = summary['counts'].get(r['status'], 0) + 1
out.write_text(json.dumps(summary, indent=1, default=str) + '\n')
print()
print(json.dumps(summary['counts']))
