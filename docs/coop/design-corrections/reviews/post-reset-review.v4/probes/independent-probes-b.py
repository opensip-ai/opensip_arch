"""Independent reviewer probes, part B: corrected fixture shapes plus deeper joins.

Part A (independent-probes.py) contained ten probes that failed on MY fixture shapes,
not on the subject. Those are re-run here against the real frozen case records, together
with additional joins the instruction names. Same standing: synthetic TCB inputs,
no product qualification, no acceptance.
"""
import copy
import hashlib
import importlib.util
import json
import re
import traceback
from pathlib import Path

from jsonschema import ValidationError

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v4/scratch')
DC = ROOT / 'docs/coop/design-corrections'
CONTRACTS = ROOT / 'docs/v2/contracts/product-v1'
ARCH = ROOT / 'docs/v2/architecture'

spec = importlib.util.spec_from_file_location('probe_host_b', DC / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S, N, W, C = M.S, M.N, M.W, M.C
IM = N.IM
F = M.load('probe_fixtures_b', 'integration-fixtures.py')

results = []
ERRORS = (ValueError, ValidationError, C.AdmissionError, W.Refusal, N.C.AdmissionError,
          IM.C.AdmissionError, KeyError)


def rec(pid, title, status, detail):
    results.append({'probe': pid, 'title': title, 'status': status, 'detail': detail})
    print('%-6s %-14s %s' % (pid, status, title))
    if status != 'OK':
        print('        ' + json.dumps(detail, default=str)[:2200])


def probe(pid, title):
    def deco(fn):
        try:
            out = fn()
        except Exception as exc:
            rec(pid, title, 'PROBE-ERROR', {'exception': ''.join(
                traceback.format_exception_only(type(exc), exc)).strip(),
                'trace': traceback.format_exc()[-1200:]})
            return
        status, detail = out if isinstance(out, tuple) else (('OK' if out else 'COUNTEREXAMPLE'), out)
        rec(pid, title, status, detail)
    return deco


def refuses(fn):
    try:
        fn()
    except ERRORS:
        return True
    return False


def raised(fn):
    try:
        fn()
    except Exception as exc:
        return exc
    return None


WF = C.parse((DC / 'workflows/workflow-cases.v1.json').read_bytes())
TF = C.parse((DC / 'security/transition-journal-cases.v1.json').read_bytes())
DCASES = C.parse((DC / 'security/discovery-cases.v1.json').read_bytes())
SCHEMAS = C.parse((DC / 'security/security-lifecycle.schemas.v1.json').read_bytes())
INV = C.parse((DC / 'workflows/command-inventory.v1.json').read_bytes())
REG = C.parse((DC / 'public-detail-registry.v1.json').read_bytes())
OPS = ('UpdateSchemaChange', 'UpdateSameSchema', 'Repair', 'CoreRollback', 'StoreMigrate', 'StoreRollback')


def sub(v):
    if isinstance(v, str) and v.startswith('$'):
        return WF['constants'][v[1:]]
    if isinstance(v, list):
        return [sub(x) for x in v]
    if isinstance(v, dict):
        return {k: sub(x) for k, x in v.items()}
    return v


def base_discovery():
    case = next(c for c in DCASES['cases']
                if c['id'].startswith('installed-dependencies-and-cargo-build-output'))
    return copy.deepcopy(case['input'])


# ===========================================================================


@probe('P6b', 'ADV-i: the ONE mapping table equals all three real closed enums (corrected selectors)')
def _():
    text = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    rows = re.findall(r'^\|\s*(interactive-explicit|policy-record)\s*\|\s*([a-z-]+)\s*\|\s*([a-z-]+)\s*\|$',
                      text, re.M)
    table = {r[0]: (r[1], r[2]) for r in rows}
    sec_modes = set(SCHEMAS['$defs']['Consent']['properties']['mode']['enum'])
    te = C.parse((DC / 'workflows/schemas/test-execution.schema.json').read_bytes())
    te_modes = set(te['$defs']['TestExecutionStepParams']['properties']['consentSource']['enum'])
    rp = C.parse((DC / 'workflows/schemas/repair.schema.json').read_bytes())
    rp_defs = json.dumps(rp)
    rp_modes = set(re.search(r'"consentSource":\s*\{\s*"enum":\s*\[([^\]]+)\]', rp_defs).group(1)
                   .replace('"', '').replace(' ', '').split(','))
    ok = (set(table) == sec_modes == {'interactive-explicit', 'policy-record'}
          and {v[0] for v in table.values()} == te_modes
          and {v[1] for v in table.values()} == rp_modes
          and table['policy-record'] == ('pre-existing-policy', 'policy')
          and table['interactive-explicit'] == ('interactive-consent', 'interactive'))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'table': table, 'securityEnum': sorted(sec_modes),
                                                'testEnum': sorted(te_modes), 'repairEnum': sorted(rp_modes)}


@probe('P7b', 'ADV-i: repair consent/CI is carried by the ADMITTED projection and compared by repair_apply')
def _():
    """Re-derive the whole chain from the frozen workflow repair scenario, then attack the
    two conjuncts added in v4 independently of the unit fixture's expectations."""
    sc = sub(copy.deepcopy(WF['repairScenario']))
    keys = sorted(sc) if isinstance(sc, dict) else []
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    conj = "if authorization.get('consentSource') != consent or authorization.get('ci') is not ci:"
    ci_law = "if ci and consent != 'policy':"
    proj = (DC / 'integration-host-model.py').read_text()
    carries = ("'ci': bound['ci']" in proj
               and "'consentSource': 'policy' if authorization['consent']['mode'] == 'policy-record' else 'interactive'" in proj)
    # exhaustively: which (admittedMode, admittedCi, claimedConsent, claimedCi) tuples can pass?
    admits = {}
    for a_mode in ('policy-record', 'interactive-explicit'):
        for a_ci in (False, True):
            for claim in ('policy', 'interactive'):
                for c_ci in (False, True):
                    auth = {'consentSource': 'policy' if a_mode == 'policy-record' else 'interactive', 'ci': a_ci}
                    passes_new = auth['consentSource'] == claim and auth['ci'] is c_ci
                    passes_old = not (c_ci and claim != 'policy')
                    admits['%s.aCi=%s.claim=%s.cCi=%s' % (a_mode, a_ci, claim, c_ci)] = passes_new and passes_old
    lawful = {k for k, v in admits.items() if v}
    expected = {'policy-record.aCi=False.claim=policy.cCi=False',
                'policy-record.aCi=True.claim=policy.cCi=True',
                'interactive-explicit.aCi=False.claim=interactive.cCi=False'}
    return ('OK' if (conj in src and ci_law in src and carries and lawful == expected)
            else 'COUNTEREXAMPLE'), {'newConjunctPresent': conj in src, 'ciLawRetained': ci_law in src,
                                     'projectionCarriesBoth': carries,
                                     'admittedTuples': sorted(lawful), 'scenarioKeys': keys}


@probe('P10b', 'SHOULD-A: the 1025-root band is reached through the OPERATIONAL host composition')
def _():
    """The unit case and the integration case both drive the STANDALONE instrument
    (boundaries=None), which native section 1.4 U-8 says is not an operational composition.
    Drive the same band through real security discovery -> admitted boundaries -> native."""
    di = base_discovery()
    root = next(iter(sorted(p for p, r in di['fs'].items() if r['kind'] == 'dir')), None)
    d0 = S.discovery(copy.deepcopy(di))
    root = d0['provenance']['selectedRoot']
    dirrow = next(r for p, r in di['fs'].items() if r['kind'] == 'dir' and p != root)
    filerow = next(r for p, r in di['fs'].items() if r['kind'] == 'file')
    big = copy.deepcopy(di)
    for i in range(1025):
        big['fs']['%s/u%04d' % (root, i)] = dict(dirrow)
        big['fs']['%s/u%04d/package.json' % (root, i)] = dict(filerow)
    d = S.discovery(copy.deepcopy(big))
    markers = {p[len(root) + 1:]: {'sha256': '1' * 64} for p, r in big['fs'].items()
               if p.startswith(root + '/') and r['kind'] == 'file'
               and p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}
    exc = raised(lambda: M.admit_repository_discovery(big, markers, []))
    typed = isinstance(exc, N.ScopeRefusal)
    return ('OK' if typed else 'COUNTEREXAMPLE'), {
        'securityDiscoveryStatus': d['status'], 'securityUnits': len(d['provenance']['units']),
        'markerDirs': len(markers),
        'hostException': type(exc).__name__ if exc else None,
        'detail': getattr(exc, 'detail', None), 'subject': getattr(exc, 'subject', None),
        'd9': getattr(exc, 'd9', None)}


@probe('P15b', 'ADV-ii: PROJECT.DISCOVERY_INVENTORY_MISMATCH has a real host emitter reachable pre-native')
def _():
    di = base_discovery()
    d0 = S.discovery(copy.deepcopy(di))
    root = d0['provenance']['selectedRoot']
    files = [p[len(root) + 1:] for p, r in di['fs'].items() if p.startswith(root + '/') and r['kind'] == 'file']
    markers = {p: {'sha256': '1' * 64} for p in files if p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}
    good = M.admit_repository_discovery(copy.deepcopy(di), markers, files)
    variants = {
        'markerSecurityNeverObserved': lambda: M.admit_repository_discovery(
            copy.deepcopy(di), dict(markers, **{'ghost/package.json': {'sha256': '2' * 64}}), files),
        'markerSecurityObservedButNativeDropped': lambda: M.admit_repository_discovery(
            copy.deepcopy(di), {k: v for k, v in list(markers.items())[1:]}, files),
        'fileOutsideObservedInventory': lambda: M.admit_repository_discovery(
            copy.deepcopy(di), markers, files + ['ghost.ts']),
    }
    rows = {}
    for name, fn in variants.items():
        e = raised(fn)
        if isinstance(e, M.DiscoveryInventoryMismatch):
            t = M.public_termination(e.d9, e.detail, 'Re-admit one consistent repository inventory.')
            rows[name] = (t['domainDetail']['code'], t['errorCode'], W.exit_code(t))
        else:
            rows[name] = 'NOT-THE-TYPED-HOST-CLASS: ' + type(e).__name__ if e else 'NO-REFUSAL'
    ok = (good['native']['units'] and
          all(v == ('PROJECT.DISCOVERY_INVENTORY_MISMATCH', 'REQUEST.PRECONDITION_FAILED', 2)
              for v in rows.values()))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'baselineUnits': len(good['native']['units']), 'variants': rows}


@probe('P16b', 'ADV-ii: a boundary-crossing explicit root is reported ONCE, under the security spelling')
def _():
    di = base_discovery()
    d0 = S.discovery(copy.deepcopy(di))
    root = d0['provenance']['selectedRoot']
    dirrow = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}
    filerow = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    b = copy.deepcopy(di)
    for p in ('apps', 'apps/site'):
        b['fs'][root + '/' + p] = dict(dirrow)
    for p in ('apps/site/opensip.json', 'apps/site/package.json'):
        b['fs'][root + '/' + p] = dict(filerow)
    b['config'] = {'discovery': {'workspaceRoots': ['apps/site']}}
    d = S.discovery(copy.deepcopy(b))
    files = [p[len(root) + 1:] for p, r in b['fs'].items() if p.startswith(root + '/') and r['kind'] == 'file']
    markers = {p: {'sha256': '1' * 64} for p in files if p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}
    exc = raised(lambda: M.admit_repository_discovery(b, markers, files))
    # the native standalone instrument would produce its own (now internal) spelling
    boundaries = {'schemaVersion': 1, 'source': 'security-discovery',
                  'nestedProjects': ['apps/site'], 'nestedRepositories': [], 'custodyExcludedUnits': [],
                  'prunedTrees': [], 'excludedPathPrefixes': ['apps/site'],
                  'disclosure': 'synthetic reviewer inventory'}
    standalone = None
    try:
        standalone = N.discover_units(markers, ['apps/site'], boundaries)
    except Exception as e:
        standalone = {'error': str(e)[:200]}
    internal = (standalone or {}).get('refused', {}).get('detail') if isinstance(standalone, dict) else None
    aliases = {r['internalCode']: r['publicCode'] for r in REG['internalAliases']}
    return ('OK' if d['status'] != 'ACCEPT' or exc is not None else 'COUNTEREXAMPLE'), {
        'securityStatus': d['status'],
        'securityRefusal': d.get('refusal') or d.get('detail') or d.get('reason'),
        'hostRefusalType': type(exc).__name__ if exc else None,
        'hostMessage': str(exc)[:200] if exc else None,
        'standaloneInternalDetail': internal,
        'internalDetailIsAliasedNotPublic': aliases.get(internal) if internal else None}


@probe('P17b', 'ADV-iii: reselectsStore is gone and the closed intent could never have carried it')
def _():
    src = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    intent = SCHEMAS['schemas']['InstallationTransitionIntentV1']
    wf = C.parse((DC / 'workflows/schemas/invocation-record.schema.json').read_bytes())
    wf_intent = wf['$defs']['CoreTransitionIntentV1']
    everywhere = {}
    for p in sorted(DC.rglob('*.py')) + sorted(DC.rglob('*.json')) + sorted(CONTRACTS.glob('*.md')):
        if 'reviews/' in str(p):
            continue
        try:
            if 'reselectsStore' in p.read_text():
                everywhere[str(p.relative_to(ROOT))] = p.read_text().count('reselectsStore')
        except Exception:
            pass
    ok = (not everywhere and intent['additionalProperties'] is False
          and {'fromStoreGeneration', 'toStoreGeneration'} <= set(intent['required'])
          and wf_intent.get('additionalProperties') is False
          and len(intent['required']) == 11)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'remainingOccurrences': everywhere, 'intentClosed': intent['additionalProperties'],
        'requiredFields': intent['required'], 'workflowIntentClosed': wf_intent.get('additionalProperties'),
        'securityModelMentions': src.count('reselectsStore')}


@probe('P20b', 'ADV-iv: retention loss (exit 4) stays distinct from admission rejection (exit 2)')
def _():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    digest = next(iter(blobs))
    corrupt = dict(blobs); corrupt[digest] = b'not the promised bytes'
    corrupt_exc = raised(lambda: IM.close_run(run, objects, corrupt))
    missing_exc = raised(lambda: IM.close_run(run, objects, {k: v for k, v in blobs.items() if k != digest}))
    key = next(iter(objects))
    wrong = dict(objects); wrong[key] = ('view', objects[key][1])
    wrong_exc = raised(lambda: IM.close_run(run, wrong, blobs))
    ok = (isinstance(missing_exc, IM.EvidenceUnavailable)
          and issubclass(IM.EvidenceUnavailable, IM.C.AdmissionError)
          and hasattr(missing_exc, 'termination')
          and W.exit_code(missing_exc.termination) == 4
          and not isinstance(corrupt_exc, IM.EvidenceUnavailable) and not hasattr(corrupt_exc, 'termination')
          and not isinstance(wrong_exc, IM.EvidenceUnavailable) and not hasattr(wrong_exc, 'termination'))
    # identity section 4/5's stated distinction
    prose = (CONTRACTS / 'identity-and-evidence.md').read_text()
    stated = ('missing witness bytes is retention loss' in prose or
              'retention loss' in prose) and 'HOST.IO_FAILURE' in prose
    return ('OK' if ok and stated else 'COUNTEREXAMPLE'), {
        'missing': type(missing_exc).__name__, 'missingExit': W.exit_code(missing_exc.termination),
        'corrupt': type(corrupt_exc).__name__ + ':' + str(corrupt_exc)[:40],
        'wrongDomain': type(wrong_exc).__name__ + ':' + str(wrong_exc)[:40],
        'subclassOfIdentityAdmissionError': issubclass(IM.EvidenceUnavailable, IM.C.AdmissionError),
        'contractStatesTheDistinction': stated}


def transition_case(key):
    ti = TF['records']['intent' + key]
    tj = S.transition_journal_record(ti, TF['ctxBase']['namespaceRegistry'])
    tc = dict(TF['ctxBase'], currentStateSchema=ti['fromStateSchema'],
              currentStoreGeneration=ti['fromStoreGeneration'],
              currentCoreGeneration=ti['preconditionGeneration'], leasesHeld=tj['leaseSet'])
    trc = dict(TF['rctx'], leasesReacquired=tj['leaseSet'])
    return ti, tj, tc, trc


@probe('P21b', 'ADV-v: a fresh recovery Attempt begins at the OBSERVED durable state, all ops x all closed states')
def _():
    out = {}
    for key in OPS:
        ti, tj, tc, trc = transition_case(key)
        for state in ('LEASED', 'PREPARING', 'PREPARED', 'COMMITTED', 'DONE', 'ABORTED'):
            j = dict(tj, state=state)
            ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, j)
            ctx = dict(trc)
            if state == 'PREPARED' and j['operation'] in S.STORE_OPERATIONS:
                ctx['storeFootprint'] = {'old': {'present': True, 'unbootstrappedReason': 'RESTORED'},
                                         'new': {'dir': 'migrating', 'state': 'PREPARED'}}
            r = M.installation_recovery_attempt(ti, j, ref, ctx, 'exec1_' + '7' * 32)
            a = r['attempt']
            out['%s.%s' % (key, state)] = {
                'ok': a['installationRecoveryStartRef'] == ref == a['installationJournalRefs'][0],
                'states': [x['state'] for x in r['journals']],
                'action': r['decision']['action'], 'after': r['decision']['journalStateAfter'],
                'outcome': a['outcome'],
                'lastEqualsDecision': (r['decision']['journalStateAfter'] is None
                                       or r['journals'][-1]['state'] == r['decision']['journalStateAfter'])}
    bad = {k: v for k, v in out.items() if not (v['ok'] and v['lastEqualsDecision'])}
    return ('OK' if not bad and len(out) == 36 else 'COUNTEREXAMPLE'), {
        'cases': len(out), 'bad': bad,
        'stateSequences': sorted({tuple(v['states']) for v in out.values()}),
        'actions': sorted({v['action'] for v in out.values()}),
        'outcomes': sorted({v['outcome'] for v in out.values()})}


@probe('P22b', 'ADV-v: PREPARED store recovery resumes through COMMITTED to DONE in one lawful segment')
def _():
    out = {}
    for key in OPS:
        ti, tj, tc, trc = transition_case(key)
        if tj['operation'] not in S.STORE_OPERATIONS:
            continue
        j = dict(tj, state='PREPARED')
        ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, j)
        ctx = dict(trc, storeFootprint={'old': {'present': True, 'unbootstrappedReason': 'RESTORED'},
                                        'new': {'dir': 'migrating', 'state': 'PREPARED'}})
        r = M.installation_recovery_attempt(ti, j, ref, ctx, 'exec1_' + '8' * 32)
        out[key] = {'states': [x['state'] for x in r['journals']], 'action': r['decision']['action'],
                    'refs': len(r['attempt']['installationJournalRefs']),
                    'firstIsObserved': r['attempt']['installationJournalRefs'][0] == ref}
        # a core operation in the same PREPARED state must ABORT, not resume
    core = {}
    for key in OPS:
        ti, tj, tc, trc = transition_case(key)
        if tj['operation'] in S.STORE_OPERATIONS:
            continue
        j = dict(tj, state='PREPARED')
        ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, j)
        r = M.installation_recovery_attempt(ti, j, ref, trc, 'exec1_' + '8' * 32)
        core[key] = [x['state'] for x in r['journals']]
    ok = (out and all(v['states'] == ['PREPARED', 'COMMITTED', 'DONE'] and v['action'] == 'RESUME-COMMIT'
                      and v['refs'] == 3 and v['firstIsObserved'] for v in out.values())
          and all(v == ['PREPARED', 'ABORTED'] for v in core.values()))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'storeOperations': out, 'coreOperations': core}


@probe('P23b', 'ADV-v: recovery never rewrites the original Attempt; a foreign start ref is refused')
def _():
    rows = {}
    for key in OPS:
        ti, tj, tc, trc = transition_case(key)
        leased = dict(tj, state='LEASED')
        lref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, leased)
        original = M.installation_journal_history(ti, [leased])
        committed = dict(tj, state='COMMITTED')
        cref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, committed)
        rec_attempt = M.installation_recovery_attempt(ti, committed, cref, trc, 'exec1_' + '9' * 32)
        refs = rec_attempt['attempt']['installationJournalRefs']
        rows[key] = {
            'originalUnchanged': original == [lref],
            'recoveryStartsAtObserved': refs[0] == cref,
            'recoveryExcludesOriginalRevision': lref not in refs,
            'foreignStartRefRefused': refuses(lambda: M.installation_journal_history(ti, [committed], lref)),
            'nonRecoveryStillMustStartLeased': refuses(lambda: M.installation_journal_history(ti, [committed])),
            'immutableFieldsEnforced': refuses(lambda: M.installation_journal_history(
                ti, [committed, dict(committed, state='DONE', requestId='req1_' + '0' * 32)], cref)),
            'illegalTransitionRefused': refuses(lambda: M.installation_journal_history(
                ti, [dict(tj, state='LEASED'), dict(tj, state='DONE')], lref)),
        }
    bad = {k: {kk: vv for kk, vv in v.items() if not vv} for k, v in rows.items()
           if not all(v.values())}
    return ('OK' if not bad else 'COUNTEREXAMPLE'), {'bad': bad, 'sample': rows['StoreMigrate']}


@probe('P24b', 'ADV-v: the Attempt schema admits the recovery pair and refuses an orphan start ref')
def _():
    ref = 'security.installation-transition-journal.v1:' + 'a' * 64
    other = 'security.installation-transition-journal.v1:' + 'b' * 64
    eid = 'exec1_' + '1' * 32
    def val(rec):
        return W.validate_import_record('workflows/schemas/invocation-record.schema.json',
                                        '#/$defs/Attempt', rec)
    good = {'executionId': eid, 'outcome': 'completed',
            'installationRecoveryStartRef': ref, 'installationJournalRefs': [ref]}
    orphan = {'executionId': eid, 'outcome': 'completed', 'installationRecoveryStartRef': ref}
    initial = {'executionId': eid, 'outcome': 'completed', 'installationJournalRefs': [ref]}
    mismatch = {'executionId': eid, 'outcome': 'completed',
                'installationRecoveryStartRef': ref, 'installationJournalRefs': [other, ref]}
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    model = "a['installationJournalRefs'][0] != a['installationRecoveryStartRef']" in src
    return ('OK' if (not refuses(lambda: val(good)) and refuses(lambda: val(orphan))
                     and not refuses(lambda: val(initial)) and model) else 'COUNTEREXAMPLE'), {
        'recoveryPairAdmitted': not refuses(lambda: val(good)),
        'orphanStartRefRefused': refuses(lambda: val(orphan)),
        'initialAttemptStillAdmitted': not refuses(lambda: val(initial)),
        'schemaAloneAdmitsOrderMismatch': not refuses(lambda: val(mismatch)),
        'modelEnforcesOrderInObservationJoin': model}


@probe('P26b', 'Run closure: prepare-code iff a trusted repository preparation principal is projected (A-1)')
def _():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    plan0 = objects[run['planId']][1]
    grant0 = C.parse(blobs[plan0['semanticGrantDigest']])

    def put(value, store):
        raw = value if type(value) is bytes else C.canonical(value)
        d = hashlib.sha256(raw).hexdigest(); store[d] = raw; return d

    def variant(principals, ops):
        r = copy.deepcopy(run); o = copy.deepcopy(objects); b = dict(blobs)
        plan = copy.deepcopy(o[r['planId']][1])
        g = copy.deepcopy(grant0)
        g['principals'] = sorted(principals, key=C.canonical)
        g['analysisOperations'] = sorted(set(ops))
        owner_blob = put(b'owner manifest bytes', b)
        for p in g['principals']:
            if p.get('ownerSourceDigest') == 'PUT':
                p['ownerSourceDigest'] = owner_blob
        plan['semanticGrantDigest'] = put(g, b)
        F.rekey(o, r['planId'], plan, r)
        return lambda: IM.close_run(r, o, b)

    first = grant0['principals']
    repo = [{'kind': 'trusted-repository-code', 'closureId': plan0['semanticClosures'][0],
             'ownerSourceDigest': 'PUT'}]
    base_ops = ['native-analysis', 'read-source']
    rows = {
        'baseline': not refuses(variant(first, base_ops)),
        'repoPrincipalWithoutPrepareCode': refuses(variant(first + repo, base_ops)),
        'repoPrincipalWithPrepareCode': not refuses(variant(first + repo, base_ops + ['prepare-code'])),
        'prepareCodeWithoutRepoPrincipal': refuses(variant(first, base_ops + ['prepare-code'])),
    }
    # read-import iff the Plan selects imports
    r2, o2, b2 = F.graph_with_import('exact')
    plan2 = copy.deepcopy(o2[r2['planId']][1])
    g2 = C.parse(b2[plan2['semanticGrantDigest']])
    g2['analysisOperations'] = [x for x in g2['analysisOperations'] if x != 'read-import']
    plan2['semanticGrantDigest'] = put(g2, b2)
    F.rekey(o2, r2['planId'], plan2, r2)
    rows['importsWithoutReadImport'] = refuses(lambda: IM.close_run(r2, o2, b2))
    return ('OK' if all(rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P33b', 'Delta pivots: the two pivot codes are registered and the empty-vs-empty law is stated (CX-02)')
def _():
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    codes = set(C.parse((DC / 'workflows/schemas/common.schema.json').read_bytes())
                ['$defs']['DomainDetailCode']['enum'])
    cases = WF.get('comparisonCases')
    ids = []
    if isinstance(cases, list):
        ids = [c.get('id') for c in cases]
    elif isinstance(cases, dict):
        ids = sorted(cases)
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    both = ('COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE' in src
            and 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE' in src)
    registered = {'COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE', 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE'} <= codes
    stated = ('indeterminate' in prose and 'pivot' in prose.lower())
    return ('OK' if both and registered and stated else 'COUNTEREXAMPLE'), {
        'modelDeclaresBoth': both, 'registered': registered, 'contractStatesIndeterminatePivot': stated,
        'comparisonCaseIds': ids[:12], 'comparisonCaseCount': len(ids)}


@probe('P32b', 'Output registry: SARIF commands, parity fields, verdicts and the advisory boundary')
def _():
    cmds = INV['commands']
    sarif = sorted(c['name'] for c in cmds if 'sarif' in c['formats'])
    advisory_with_sarif = sorted(c['name'] for c in cmds if c.get('advisory') and 'sarif' in c['formats'])
    no_parity = sorted(c['name'] for c in cmds if 'sarif' in c['formats'] and not c.get('parityFields'))
    verdict_fields = {c['name']: ('verdict' in (c.get('parityFields') or []))
                      for c in cmds if 'sarif' in c['formats']}
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    law = ('required output' in prose.lower() or 'required-output' in prose.lower())
    postcommit = 'post-commit' in prose.lower()
    ok = (sarif == ['analyze', 'audit', 'default', 'repair-verify']
          and not advisory_with_sarif and not no_parity and law and postcommit)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        'sarifCommands': sarif, 'advisoryCommandsWithSarif': advisory_with_sarif,
        'sarifCommandsWithoutParityFields': no_parity, 'verdictInParity': verdict_fields,
        'requiredOutputLawStated': law, 'postCommitStated': postcommit,
        'commandCount': len(cmds), 'advisoryCount': sum(1 for c in cmds if c.get('advisory'))}


@probe('P39b', 'Security S16 matches file 05 item-for-item: preserve 5, distinctions 5, prohibitions 6')
def _():
    sec = (CONTRACTS / 'security-and-lifecycle.md').read_text()
    i = sec.find('\n## S16.')
    j = sec.find('\n## ', i + 5)
    s16 = sec[i:j if j > 0 else len(sec)]
    f05 = (ARCH / '05-v1-to-v2-relationship.md').read_text()
    k = f05.find('## Migration constraints')
    mc = f05[k:f05.find('\n## ', k + 5)]
    # file 05's own enumerations
    f05_preserve = [x.strip() for x in re.search(
        r'must preserve (.+?)\.\s*It must distinguish', mc, re.S).group(1).replace('\n', ' ').split(',')]
    f05_distinguish = re.findall(r'^-\s+(.+?)[;.]$', mc, re.M)
    f05_prohibit = re.search(r'No migration silently (.+?)\.', mc, re.S).group(1).replace('\n', ' ')
    # S16's enumerations
    s16_preserve = re.findall(r'^\d+\.\s+\*\*(.+?):\*\*', s16, re.M)
    s16_distinct = re.findall(r'\((\d)\)\s', s16)
    s16_prohibit = re.findall(r'\*\*([a-z /-]+?)\*\*', s16)
    topics = {
        'trackedIntent': 'tracked' in s16.lower(),
        'noWritePreInit': 'no-write pre-initialization' in s16,
        'perValueProvenance': 'provenance' in s16.lower(),
        'historicalIdentities': 'historical' in s16.lower(),
        'offlineBehavior': 'offline' in s16.lower(),
        'distributionVsUserState': 'distribution migration' in s16 and 'user-custody' in s16,
        'managementVsAuthoritative': 'management-only' in s16 and 'authoritative closure' in s16,
        'coexistenceVsMutation': 'immutable coexistence' in s16 and 'package mutation' in s16,
        'removalVsPurge': 'removal' in s16.lower() and 'purge' in s16.lower(),
        'replayVsDegradation': 'replay pinning' in s16 and 'degradation' in s16,
        'noDownload': 'download' in s16, 'noIndexRefresh': 'index refresh' in s16,
        'noLockMutation': 'lock mutation' in s16, 'noReplacementIdentity': 'replacement historical identity' in s16,
        'noEvidenceRewrite': 'evidence-meaning rewrite' in s16,
        'noTelemetryRequired': 'telemetry' in s16,
        'foreignStateRefusal': 'foreign' in s16.lower() and 'refused' in s16.lower(),
        'prototypeCommitPinned': 'a62509d623173155d0946e9f5d5ca90c839893e0' in s16,
        'noSilentImportOrPromotion': 'never be applied to a prototype' in s16 or 'no prototype Run/baseline/state importer' in s16,
    }
    prototype_ref = (ARCH / 'prototype-evidence-reference.md')
    commit_in_baseline = 'a62509d623173155d0946e9f5d5ca90c839893e0' in prototype_ref.read_text() if prototype_ref.exists() else False
    ok = (len(s16_preserve) == 5 and len(set(s16_distinct)) == 5 and len(f05_distinguish) == 5
          and all(topics.values()) and commit_in_baseline)
    return ('OK' if ok else 'COUNTEREXAMPLE'), {
        's16PreserveItems': s16_preserve, 's16DistinctionMarkers': sorted(set(s16_distinct)),
        'file05DistinguishBullets': f05_distinguish, 'file05Prohibitions': f05_prohibit,
        'file05PreserveClause': f05_preserve, 'topicCoverage': topics,
        'prototypeCommitAlsoInBaselineDoc': commit_in_baseline, 's16Bytes': len(s16)}


@probe('P40b', 'inherited-row-sources supplies exact resolvable pins for the six unpinned compatibility rows')
def _():
    src = C.parse((DC / 'inherited-row-sources.proposed.json').read_bytes())
    records = src['records'] if isinstance(src.get('records'), list) else []
    keys = sorted(records[0]) if records else []
    ids = [r.get('row') or r.get('id') or r.get('readinessRow') for r in records]
    expected = ['DR-102', 'DR-104', 'DR-115', 'DR-117', 'DR-119', 'DR-123']
    bad = []
    resolved = 0
    text = json.dumps(src)
    for path, digest in re.findall(r'"((?:docs|\.\./)[^"]+?)"\s*,?\s*"?[^"]*?"?\s*:?\s*"([0-9a-f]{64})"', text):
        pass
    for r in records:
        for k, v in r.items():
            if isinstance(v, dict) and 'path' in v and 'sha256' in v:
                p = ROOT / v['path']
                if not p.exists():
                    bad.append((v['path'], 'MISSING-IN-SNAPSHOT'))
                elif hashlib.sha256(p.read_bytes()).hexdigest() != v['sha256']:
                    bad.append((v['path'], 'DIGEST-DIFFERS'))
                else:
                    resolved += 1
    # fall back to a generic scan for path/sha256 pairs anywhere in the record set
    if resolved == 0:
        for path in re.findall(r'"(docs/[^"]+)"', text):
            p = ROOT / path
            if p.exists():
                resolved += 1
            else:
                bad.append((path, 'MISSING-IN-SNAPSHOT'))
    return ('OK' if sorted(set(i for i in ids if i)) == expected and not bad else 'COUNTEREXAMPLE'), {
        'recordKeys': keys, 'rowIds': ids, 'expected': expected,
        'resolvedPins': resolved, 'unresolved': bad[:12], 'standing': src.get('standing', '')[:160]}


@probe('P45b', 'Historical preservation: every named historical file is byte-unchanged in the repository')
def _():
    rep = C.parse((DC / 'historical-preservation-report.v4.json').read_bytes())
    files = rep.get('files')
    repo = Path('/Users/sb/code/opensip-ai/opensip_arch')
    checked = 0; bad = []
    rows = files if isinstance(files, list) else ([{'path': k, **v} for k, v in files.items()]
                                                 if isinstance(files, dict) else [])
    for r in rows:
        path = r.get('path') if isinstance(r, dict) else r
        digest = (r.get('sha256') or r.get('observedSha256') or r.get('expectedSha256')) if isinstance(r, dict) else None
        if not path:
            continue
        p = repo / path
        if not p.exists():
            bad.append((path, 'MISSING')); continue
        if digest and hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            bad.append((path, 'CHANGED')); continue
        checked += 1
    return ('OK' if checked and not bad else 'COUNTEREXAMPLE'), {
        'checked': checked, 'bad': bad, 'declaredUnchanged': rep.get('unchanged'),
        'declaredChanged': rep.get('changed'), 'rowShape': sorted(rows[0]) if rows and isinstance(rows[0], dict) else None}


@probe('P51', 'One default authoritative invocation, no implicit tracked-intent write, and metadata-only surfaces')
def _():
    cmds = INV['commands']
    default_auth = [c['name'] for c in cmds if c.get('authority') == 'authoritative-default']
    writes_intent = [c['name'] for c in cmds if c.get('writesTrackedIntent')]
    first_write = sorted(c['name'] for c in cmds if c.get('firstSourceWrite'))
    no_first_write = sorted(c['name'] for c in cmds if not c.get('firstSourceWrite'))
    repo_exec = {c['name']: c.get('repositoryExecution') for c in cmds
                 if c.get('repositoryExecution') not in (None, 'never')}
    default = next(c for c in cmds if c['name'] == 'default')
    prose = (CONTRACTS / 'identity-and-evidence.md').read_text()
    disclosure = 'DEFAULTED' in prose and 'CD-RT-5' in prose
    return ('OK' if (default['authority'] == 'authoritative-default'
                     and not writes_intent and disclosure and no_first_write) else 'COUNTEREXAMPLE'), {
        'authoritativeDefaultCommands': default_auth, 'commandsWritingTrackedIntent': writes_intent,
        'firstSourceWriteCommands': first_write, 'noFirstSourceWriteCount': len(no_first_write),
        'repositoryExecutionCommands': repo_exec,
        'defaultDiscloses_CDRT5_DEFAULTED': disclosure}


@probe('P52', 'Admission section 5: each of the seven boundary items has a disposition, not a deferral')
def _():
    adm = (CONTRACTS / 'admission-and-qualification.md').read_text()
    i = adm.find('\n## 5')
    j = adm.find('\n## ', i + 5)
    s5 = adm[i:j if j > 0 else len(adm)]
    items = re.findall(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*(.*)$', s5, re.M)
    f02 = (ARCH / '02-distribution-and-components.md').read_text()
    deferrals = [m for m in re.findall(r'(deferred|later stage|out of scope for now|to be decided)', s5, re.I)]
    excl = {'marketplace/catalog': bool(re.search(r'marketplace|catalog', s5, re.I)),
            'external lifecycle parity/discovery': bool(re.search(r'lifecycle', s5, re.I)),
            'contribution roles': bool(re.search(r'contribut', s5, re.I)),
            'untrusted native/WASM': bool(re.search(r'wasm|untrusted native', s5, re.I)),
            'imperative contributions/probes/hooks/root commands': bool(re.search(r'hook|imperativ|probe|root command', s5, re.I)),
            'network-granted analysis and egress defaults': bool(re.search(r'egress|network', s5, re.I)),
            'replacement of the G3 substrate': bool(re.search(r'G3|substrate', s5, re.I))}
    return ('OK' if len(items) == 7 and all(excl.values()) and not deferrals else 'COUNTEREXAMPLE'), {
        'itemCount': len(items), 'itemTitles': [t.strip() for _, t, _ in items],
        'topicCoverage': excl, 'deferralPhrases': deferrals, 'sectionBytes': len(s5),
        'file02Cited': '02-distribution-and-components' in adm or 'file 02' in adm.lower()}


@probe('P53', 'Foreign/prototype root refusal actually exists in the security root/schema admission')
def _():
    src = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    sec = (CONTRACTS / 'security-and-lifecycle.md').read_text()
    codes = {r['code'] for r in REG['records']}
    markers = {'foreignRootRefusalCodeRegistered': any('FOREIGN' in c or 'ROOT_CUSTODY' in c
                                                       or 'MIGRATION' in c for c in codes),
               'securityModelRefusesForeignSchema': bool(re.search(r'foreign|MIGRATION\.CORRUPT', src)),
               'contractStatesRefusalBeforeWrite': 'refused by the existing root/schema admission before a write' in sec}
    relevant = sorted(c for c in codes if 'MIGRATION' in c or 'ROOT' in c or 'STATE' in c or 'STORE' in c)
    return ('OK' if all(markers.values()) else 'COUNTEREXAMPLE'), {
        'markers': markers, 'relatedRegisteredCodes': relevant}


@probe('P54', 'Native sufficiency / resolution completeness: unresolved edges are not silent completeness')
def _():
    nat = json.load(open('/tmp/opensip-design-corrections/post-reset-review.v4/reports/'
                         'native-evidence-report.rerun.json'))
    src = (DC / 'native/native_evidence_model.v2.py').read_text()
    contract = (CONTRACTS / 'native-evidence.md').read_text()
    markers = {'coverage3Present': 'Coverage3' in src or 'coverage3' in src.lower(),
               'unresolvedEdgeVocabulary': 'unresolved' in src.lower(),
               'examinedVersusResolutionStated': 'resolution complete' in contract.lower()
                                                 or 'resolution-complete' in contract.lower(),
               'noSilentFallback': 'no-silent-fallback' in contract.lower() or 'never silently' in contract.lower(),
               'qualifiedCellsZero': nat['matrix']['qualifiedCells'] == 0,
               'allCellsPresent': nat['matrix']['missingCells'] == []}
    return ('OK' if all(markers.values()) else 'COUNTEREXAMPLE'), {
        'markers': markers, 'matrix': nat['matrix'],
        'negativeCases': nat['cases']['negative'], 'positiveCases': nat['cases']['positive']}


@probe('P55', 'Core transition namespace scope: the lease set is derived, all-or-nothing, and re-derived on recovery')
def _():
    rows = {}
    for key in OPS:
        ti, tj, tc, trc = transition_case(key)
        scope = M.core_transition_scope(ti, tc['namespaceRegistry'])
        narrowed = dict(tj, leaseSet=tj['leaseSet'][:-1] if len(tj['leaseSet']) > 1 else [])
        nref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, narrowed)
        widened = dict(tj, leaseSet=sorted(set(tj['leaseSet']) | {'ns-zz'}))
        wref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, widened)
        rows[key] = {
            'affects': scope['affects'], 'namespaces': scope['namespaces'],
            'journalMatchesDerivedScope': tj['leaseSet'] == scope['namespaces'],
            'narrowedLeaseSetRefused': refuses(lambda: M.recover_installation_transition(narrowed, nref, trc)),
            'widenedLeaseSetRefused': refuses(lambda: M.recover_installation_transition(widened, wref, trc)),
            'incompleteLocksRefused': refuses(lambda: M.admit_installation_transition(
                ti, tj, dict(tc, leasesHeld=tj['leaseSet'][:-1]))),
        }
    bad = {k: v for k, v in rows.items() if not (v['journalMatchesDerivedScope']
                                                 and v['narrowedLeaseSetRefused']
                                                 and v['widenedLeaseSetRefused']
                                                 and v['incompleteLocksRefused'])}
    return ('OK' if not bad else 'COUNTEREXAMPLE'), {'bad': bad, 'rows': rows}


@probe('P56', 'D-372 DR-003 timing disposition claims no measurement and keeps every release gate mandatory')
def _():
    d = (DC / 'D-372-corrections.proposed.md').read_text()
    gates = C.parse((DC / 'qualification-gates.proposed.json').read_bytes())
    items = gates.get('gates') or gates.get('items') or []
    named = {'DR-G09', 'DR-G18', 'DR-G19', 'DR-G21', 'DR-G22'}
    ids = {str(g.get('gate') or g.get('id')) for g in items}
    claims = {
        'scopedCondition1Only': 'scoped condition-1 disposition' in d,
        'notSatisfiedOrDemonstrated': 'not a SATISFIED or DEMONSTRATED claim' in d,
        'demonstrationStillMandatory': 'remains mandatory at DR-G09/G18/G19/G21/G22 and DR-012' in d,
        'failedMeasurementReopens': 'cannot be waived by the synthetic reference result' in d,
        'historicalIntact': 'leaves the historical DR-003 requirement and its evidence standing intact' in d,
        'noCondition5': 'grants no condition-5 implementation authorization' in d,
    }
    present = {g for g in named if any(g in i for i in ids)}
    honest = all(g.get('qualified') is False and g.get('demonstrated') is False
                 and g.get('implementationHarnessAuthored') is False for g in items)
    return ('OK' if all(claims.values()) and present == named and honest else 'COUNTEREXAMPLE'), {
        'claims': claims, 'namedGatesPresent': sorted(present), 'gateCount': len(items),
        'allGatesHonest': honest}


@probe('P57', 'FW-14 real-configuration-corpus obligation is stated as an obligation, not claimed satisfied')
def _():
    res = (DC / 'inherited-residuals.proposed.md').read_text()
    row = re.search(r'\| FW-14 (.+?)\n', res)
    text = row.group(1) if row else ''
    return ('OK' if ('must add' in text and 'Synthetic design cases are not that corpus' in text)
            else 'COUNTEREXAMPLE'), {'row': text[:400]}


@probe('P58', 'Every source-pin manifest verifies against the frozen snapshot bytes')
def _():
    repo = Path('/Users/sb/code/opensip-ai/opensip_arch')
    rows = {}
    for unit in ('foundation/source-pins.v1.json', 'security/source-pins.v1.json',
                 'native/source-pins.v2.json', 'workflows/source-pins.v1.json'):
        pins = C.parse((DC / unit).read_bytes())
        entries = pins.get('pins') or pins.get('files') or []
        bad = []
        for p in entries:
            path = p.get('path'); digest = p.get('sha256')
            if not path or not digest:
                continue
            f = ROOT / path
            if not f.exists():
                f = repo / path
            if not f.exists():
                bad.append((path, 'MISSING')); continue
            if hashlib.sha256(f.read_bytes()).hexdigest() != digest:
                bad.append((path, 'DIGEST-DIFFERS'))
        rows[unit] = {'pins': len(entries), 'bad': bad[:5], 'badCount': len(bad)}
    return ('OK' if all(r['badCount'] == 0 for r in rows.values()) else 'COUNTEREXAMPLE'), rows


@probe('P59', 'ADV-vi: the crosswalk stays prospective and names no superseded review as acceptance')
def _():
    cw = C.parse((DC / 'correction-crosswalk.proposed.json').read_bytes())
    text = json.dumps(cw)
    rows = cw.get('findings') or cw.get('rows') or cw.get('ar') or []
    if isinstance(rows, dict):
        rows = list(rows.values())
    grades = sorted({str(r.get('status') or r.get('disposition') or r.get('standing'))
                     for r in rows if isinstance(r, dict)})
    reviews = sorted(set(re.findall(r'post-reset-review\.v\d/review\.json', text)))
    accepts = re.findall(r'"(?:verdict|grade|independentGrade)"\s*:\s*"ACCEPT[^"]*"', text)
    return ('OK' if not accepts else 'ADVISORY'), {
        'rowCount': len(rows), 'grades': grades[:6], 'reviewsNamed': reviews,
        'acceptClaims': accepts[:5],
        'standing': str(cw.get('standing'))[:200]}


@probe('P60', 'Contracts declare their enforcement/measurement boundary honestly (no confinement claim)')
def _():
    rows = {}
    for p in sorted(CONTRACTS.glob('*.md')):
        t = p.read_text()
        rows[p.name] = {
            'saysNotConfinement': bool(re.search(r'not a sandbox|does not prevent|no confinement|confinementClaimed', t, re.I)),
            'qualifiedOccurrences': len(re.findall(r'\bQUALIFIED\b', t)),
            'qualifiedContexts': [m for m in re.findall(r'.{60}\bQUALIFIED\b.{60}', t)][:2],
        }
    return ('OK' if all(r['saysNotConfinement'] for r in rows.values()) else 'ADVISORY'), rows


out = Path('/tmp/opensip-design-corrections/post-reset-review.v4/probes/independent-probes-b.json')
summary = {'reviewer': 'fresh actual-Claude independent reviewer; authored none of the subject bytes',
           'part': 'B (corrected fixture shapes plus deeper joins)',
           'manifestSha256': '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2',
           'syntheticTcbInputs': True, 'productQualification': False,
           'counts': {}, 'probes': results}
for r in results:
    summary['counts'][r['status']] = summary['counts'].get(r['status'], 0) + 1
out.write_text(json.dumps(summary, indent=1, default=str) + '\n')
print()
print(json.dumps(summary['counts']))
