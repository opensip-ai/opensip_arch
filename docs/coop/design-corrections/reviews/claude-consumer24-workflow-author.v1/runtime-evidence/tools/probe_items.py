"""Item probes over a work tree (records outcomes; never asserts). Run once on the unmodified copy and again after edits.

usage: python -I -B probe_items.py LABEL
All inputs are owner fixtures built in-process (check-replay.v3 positive graphs, owner schemas). Nothing is written into
the tree; the receipt goes to receipts/probes/probe-items.LABEL.json.
"""
import copy, hashlib, importlib.util, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
DC = RT / 'work/source38-work/docs/coop/design-corrections'
LABEL = sys.argv[1]
sys.path.insert(0, str(DC / 'foundation'))
import canonical  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P = load('probe_proj', DC / 'workflows/workflow_projection_model.v3.py')
RC = load('probe_rc', DC / 'foundation/check-replay.v3.py')
E = load('probe_comp', DC / 'foundation/evaluator_composition_model.v3.py')
SCHEMAS = {}
for p in sorted((DC / 'workflows/schemas/evaluator3').glob('*.schema.json')) + [DC / 'workflows/schemas' / n for n in ('common.schema.json', 'imported-evidence.schema.json', 'policy-document.schema.json', 'policy-document.v2.schema.json', 'test-execution.schema.json')]:
    d = json.loads(p.read_text())
    SCHEMAS[d['$id']] = d
REG = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()])
U = 'urn:opensip:product-v1:workflows:evaluator3:'
OUT = {'label': LABEL, 'tree': str(DC), 'sections': {}}


def valid(ref, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': ref}, registry=REG).validate(value)
        return {'result': 'ADMIT'}
    except Exception as exc:
        return {'result': 'REFUSE', 'message': str(exc).splitlines()[0][:200]}


def attempt(fn):
    try:
        return {'result': 'OK', 'value': fn()}
    except Exception as exc:
        return {'result': 'RAISED', 'type': type(exc).__name__, 'errorCode': getattr(exc, 'error_code', None),
                'detail': getattr(exc, 'detail', None), 'message': str(exc).splitlines()[0][:240] if str(exc) else ''}


def section(name, fn):
    try:
        OUT['sections'][name] = fn()
    except Exception as exc:
        OUT['sections'][name] = {'sectionError': type(exc).__name__ + ': ' + str(exc)[:400], 'trace': traceback.format_exc()[-1500:]}


SCOPE_ALL = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['**'], 'exclude': []}
CUSTODY = {'exportedAtUtc': '2026-09-08T00:00:00Z', 'exportedByHostRelease': '1.0.0'}


def host_from_graph(run_id, objects):
    closures, majors, platform = {}, set(), None
    for key, (dom, val) in objects.items():
        if dom != 'closure':
            continue
        closures[key] = {'bytes': 'ok', 'trust': 'admitted', 'protocolMajor': val['protocolMajor'], 'platform': val['platform']}
        majors.add(val['protocolMajor'])
        if val['kind'] == 'evaluator':
            platform = val['platform']
        elif platform is None and val['kind'] == 'detector' and val['platform'] != 'any':
            platform = val['platform']
    return {'closures': closures, 'protocolMajors': sorted(majors), 'platform': platform or 'linux', 'pivotRunId': run_id, 'recipeMajors': [2]}


def summarize_cmp(res):
    d = res['descriptor']
    return {'comparisonResultId': res['comparisonResultId'], 'verdict': d.get('verdict'), 'comparisonPerformed': d.get('comparisonPerformed'),
            'pivotsAvailable': d.get('pivotsAvailable'), 'contextDelta': d.get('contextDelta'), 'ruleDeficiencies': d.get('ruleDeficiencies'),
            'remedy': d.get('remedy'), 'unmatchedCount': len(d.get('unmatchedOccurrences') or []),
            'entries': [{k: e.get(k) for k in ('fingerprint', 'classification', 'direction', 'indeterminateReason', 'gates', 'gateReason', 'liveInCurrent', 'subsequentDeltas', 'presence')} for e in d.get('entries', [])],
            'schema': valid(U + 'comparison:2', {'comparisonResultId': res['comparisonResultId'], 'descriptor': d})}


X1 = {'nativeSubjectId': 'symbol:x1'}
X2 = {'nativeSubjectId': 'symbol:x2', 'signatureTokens': ['function', 'x', '(', 'number', ')']}


def s7():
    out = {}
    for gate in (True, False):
        base = RC.positive(symbol_rows=[X1, X2], scope_document=SCOPE_ALL, gate=gate)
        art = P.adopt_admitted_baseline_v3(*base, CUSTODY)
        host = host_from_graph(art['descriptor']['runId'], base[1])
        rows = {'baselineEntries': [e['fingerprint'] for e in art['descriptor']['entries']], 'baselineId': art['baselineId']}
        currents = {
            'complete-x1-removed': dict(symbol_rows=[X2]),
            'partial-inventory-x1-missing': dict(symbol_rows=[X2], symbol_state='partial'),
            'budget-exhausted-both-rows': dict(symbol_rows=[X1, X2], budget_limit=1),
            'complete-unchanged': dict(symbol_rows=[X1, X2]),
        }
        for name, opts in currents.items():
            cur = RC.positive(scope_document=SCOPE_ALL, gate=gate, **opts)
            view = P.project_admitted_run_v3(*cur)
            rr = view['ruleResults'][0]
            facts = {'currentVerdict': view['proof']['verdict'], 'evaluationState': view['evaluationState'], 'enumerationState': rr['enumeration']['state'],
                     'outcome': rr['outcome'], 'matchedFingerprints': sorted(o['finding']['fingerprint'] for o in view['occurrences'] if o['finding']['fingerprint']),
                     'unmatched': sum(1 for o in view['occurrences'] if not o['finding']['fingerprint']),
                     'ruleHasCompleteHitSet': P.rule_has_complete_hit_set(view, rr['ruleId']),
                     'samePolicyDigest': view['plan']['policyDigest'] == base[1][base[0]['planId']][1]['policyDigest']}
            cmp = attempt(lambda: summarize_cmp(P.compare_admitted_v3(baseline_artifact=art, current_run=cur[0], current_objects=cur[1], current_blobs=cur[2], host=host, profile_name='code-regression')))
            rows[name] = {'current': facts, 'comparison': cmp}
        out['gate-' + str(gate).lower()] = rows
    return out


def m4():
    base = RC.positive(scope_document=SCOPE_ALL)
    art = P.adopt_admitted_baseline_v3(*base, CUSTODY)
    d = art['descriptor']
    res = {'original': {'detectorClosure': d['detectorClosure'], 'entryDetectorIds': sorted({e['detectorId'] for e in d['entries']}), 'verify': attempt(lambda: P.verify_baseline_artifact_v3(art))}}

    def remint(mut):
        a = copy.deepcopy(art)
        mut(a['descriptor'])
        a['baselineId'] = P.wid('baseline2', 'workflow.baseline', a['descriptor'])
        return a

    def rename(desc):
        for row in desc['detectorClosure']:
            row['detectorId'] = 'renamed-detector'
        for e in desc['entries']:
            e['detectorId'] = 'renamed-detector'
    renamed = remint(rename)
    stale = copy.deepcopy(art)
    rename(stale['descriptor'])
    res['remintedRename'] = {'baselineId': renamed['baselineId'], 'schema': valid(U + 'baseline:2', renamed), 'verify': attempt(lambda: P.verify_baseline_artifact_v3(renamed)),
                             'e0JoinAgainstOriginal': attempt(lambda: P.require_exact_detector_map(renamed['descriptor']['detectorClosure'], d['detectorClosure'], 'E0'))}
    res['staleHashRename'] = {'verify': attempt(lambda: P.verify_baseline_artifact_v3(stale))}

    def entry_outside(desc):
        for e in desc['entries']:
            e['detectorId'] = 'not-in-closure'
    eo = remint(entry_outside)
    res['remintedEntryDetectorOutsideClosure'] = {'schema': valid(U + 'baseline:2', eo), 'verify': attempt(lambda: P.verify_baseline_artifact_v3(eo))}

    def dup_row(desc):
        row = copy.deepcopy(desc['detectorClosure'][0])
        row['semanticsMajor'] = row['semanticsMajor'] + 1
        desc['detectorClosure'].append(row)
    dup = remint(dup_row)
    res['remintedConflictingContributionRow'] = {'schema': valid(U + 'baseline:2', dup), 'verify': attempt(lambda: P.verify_baseline_artifact_v3(dup))}
    return res


def envelopes():
    H = 'ab' * 32
    term_rej = lambda code, detail=None: dict({'class': 'request-rejected', 'errorCode': code}, **({'domainDetail': {'code': detail, 'remedy': 'r'}} if detail else {}))
    env = lambda term, **extra: dict({'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'failure', 'requestId': 'req1_' + 'ef' * 16, 'termination': term, 'exitCode': P.W.EXIT[term['class']]}, **extra)
    doc_term = {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io'}
    codes = set(SCHEMAS[U + 'common:3']['$defs']['DomainDetailCode']['enum'])
    res = {'registeredNewCodes': {c: c in codes for c in ('DOCTOR.REPORT_NOT_PRODUCIBLE', 'OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED', 'DELIVERY.REQUIRED_PROJECTION_FAILED')}}
    res['goldenFailureEnvelopesWithoutErrors'] = {
        'doctor-report-not-producible': valid(U + 'command-envelope:3', env(doc_term)),
        'query-latest-empty': valid(U + 'command-envelope:3', env(term_rej('IDENTITY.UNKNOWN'))),
        'envelope-major-unsupported': valid(U + 'command-envelope:3', env(term_rej('REQUEST.SCHEMA_MAJOR_UNSUPPORTED')))}
    after = {'class': 'operational-failed', 'errorCode': 'DELIVERY.REQUIRED_FAILED', 'faultCause': 'delivery-required', 'domainDetail': {'code': 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT', 'remedy': 'r'}}
    res['afterCommitDetailWithoutRunId'] = valid(U + 'common:3#/$defs/StepTermination', after)
    res['afterCommitDetailWithRunId'] = valid(U + 'common:3#/$defs/StepTermination', dict(after, runId='run3:' + H))
    q = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'query', 'requestId': 'req1_' + 'ef' * 16, 'projectId': 'prj1-' + H,
         'termination': {'class': 'success'}, 'exitCode': 0, 'query': {'kind': 'query', 'items': 0, 'truncated': False, 'completenessMet': True, 'advisory': False}}
    resp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'coverage.show', 'context': {'projectId': 'prj1-' + H, 'resolvedView': {'runId': 'run3:' + H}, 'coverage': 'complete', 'availability': 'retained', 'truncated': False, 'totalItems': 0, 'advisory': False}}
    res['queryEnvelopeCompactOnly'] = valid(U + 'command-envelope:3', q)
    res['queryEnvelopeWithQueryResponse'] = valid(U + 'command-envelope:3', dict(q, queryResponse=resp))
    res['queryEnvelopeWithSelectorAndResponse'] = valid(U + 'command-envelope:3', dict(q, querySurface='graph-query-response', queryResponse=resp))
    res['envelopeHasQueryResponseProperty'] = 'queryResponse' in SCHEMAS[U + 'command-envelope:3']['properties']
    return res


def a6():
    rows = {}
    cases = {
        'projection-unavailable+population-incomplete': dict(symbol_rows=[{'nativeSubjectId': 'symbol:x', 'projectionAvailable': False}], symbol_state='partial'),
        'population-incomplete+signature-shared': dict(symbol_rows=[{'nativeSubjectId': 'symbol:x1'}, {'nativeSubjectId': 'symbol:x2'}], symbol_state='partial'),
        'signature-shared-complete': dict(symbol_rows=[{'nativeSubjectId': 'symbol:x1'}, {'nativeSubjectId': 'symbol:x2'}]),
        'projection-unavailable-with-signature-peer-complete': dict(symbol_rows=[{'nativeSubjectId': 'symbol:x1', 'projectionAvailable': False}, {'nativeSubjectId': 'symbol:x2'}]),
    }
    for name, opts in cases.items():
        def run(opts=opts):
            g = RC.positive(**opts)
            replay = RC.R.replay(*g)
            run_, objects, blobs = g
            proof = objects[objects[run_['evaluationSealId']][1]['proofBundleId']][1]
            findings = [objects[f][1] for f in proof['findingIds']]
            corr = [d for r in proof['ruleResults'] for d in r['deficiencies'] if d['source'] == 'correspondence']
            return {'verdict': replay['verdict'], 'findings': [{'subjectId': f['subjectId'], 'state': f['correspondence']['state'], 'reason': f['correspondence']['reason']} for f in findings],
                    'correspondenceDeficiencies': [{'subjectId': d['subjectId'], 'cause': d['cause']} for d in corr],
                    'onePerUnmatched': sorted((f['subjectId'], f['correspondence']['reason']) for f in findings if f['correspondence']['state'] == 'unmatched') == sorted((d['subjectId'], d['cause']) for d in corr)}
        rows[name] = attempt(run)
    return rows


def a9():
    rows = {}
    none_file = {'op': 'none', 'relation': 'file', 'minResolution': 'enumerated', 'filters': []}
    cases = {
        'required-runtime-unavailable-known-hits-gating': dict(evidence_use=[{'kind': 'runtime', 'requirement': 'required'}]),
        'required-runtime-unavailable-root-false-gating': dict(atom_override=none_file, evidence_use=[{'kind': 'runtime', 'requirement': 'required'}]),
        'required-runtime-unavailable-root-false-nongating': dict(atom_override=none_file, evidence_use=[{'kind': 'runtime', 'requirement': 'required'}], gate=False),
        'optional-runtime-unavailable-root-false-gating': dict(atom_override=none_file, evidence_use=[{'kind': 'runtime', 'requirement': 'optional'}]),
    }
    for name, opts in cases.items():
        def run(opts=opts):
            g = RC.positive(**opts)
            replay = RC.R.replay(*g)
            run_, objects, blobs = g
            proof = objects[objects[run_['evaluationSealId']][1]['proofBundleId']][1]
            rr = proof['ruleResults'][0]
            roots = sorted({p['value'] for p in proof['predicateProofs'] if p['predicateId'] == 'p'})
            return {'verdict': replay['verdict'], 'findingCount': replay.get('findingCount'), 'outcome': rr['outcome'], 'rootValues': roots,
                    'requiredImportDeficiencies': [d['cause'] + ':' + str(d['evidenceKind']) for d in rr['deficiencies'] if d['source'] == 'import']}
        rows[name] = attempt(run)
    return rows


def a11_a12():
    te = SCHEMAS['urn:opensip:product-v1:workflows:test-execution']['$defs']['EnforcementValue']
    tt = (DC.parent / 'artifacts/permission-truth-tables.v9.json').read_text()
    W = P.W
    presence = {'B': False, 'E0': True, 'E1': False, 'E2': False, 'E3': False, 'E4': False, 'waivedB': False, 'waivedC': False}
    rule = {'enabled': True, 'gating': True, 'evidenceUse': []}
    disp = {'detectorId': 'd', 'method': 'identical-closure'}
    entry, sig = W.classify('finding-key2:' + 'a' * 64, 'r', presence, rule, rule, {'imports': []}, {'imports': []}, disp, W.AUDIT_PROFILES['code-regression'])
    return {'enforcementValue': te, 'truthTableEnforcedPlatformOccurrences': tt.count('ENFORCED-PLATFORM'),
            'classifyDetectionHiddenCodeNetNew': {k: entry.get(k) for k in ('classification', 'gates', 'gateReason', 'subsequentDeltas')}}


def s5():
    C = canonical
    raw = lambda v: hashlib.sha256(C.canonical(v)).hexdigest()
    joined = lambda v: hashlib.sha256(' '.join(v).encode()).hexdigest()
    pairs = {'space-inside-vs-split': (['run', 'a b'], ['run', 'a', 'b']), 'trailing-empty-vs-none': (['run', 'x', ''], ['run', 'x']),
             'repeat-vs-single': (['run', '-v', '-v'], ['run', '-v']), 'order': (['run', 'a', 'b'], ['run', 'b', 'a'])}
    return {k: {'canonicalDigestsDiffer': raw(a) != raw(b), 'shellJoinedCollide': joined(a) == joined(b)} for k, (a, b) in pairs.items()}


for name, fn in (('M4', m4), ('M5-S6-A13-envelopes', envelopes), ('S7', s7), ('A6', a6), ('A9', a9), ('A11-A12', a11_a12), ('S5', s5)):
    section(name, fn)
dest = RT / 'receipts/probes'
dest.mkdir(parents=True, exist_ok=True)
(dest / ('probe-items.' + LABEL + '.json')).write_text(json.dumps(OUT, indent=1, default=str) + '\n')
print(json.dumps({k: (v if k in ('M5-S6-A13-envelopes', 'A11-A12', 'S5') else ('error' if isinstance(v, dict) and 'sectionError' in v else 'recorded')) for k, v in OUT['sections'].items()}, indent=1, default=str)[:6000])
