"""P17: compute the owner's expected-source census for the clones-fact accounts, and the
carrier the owner would derive, against the consumer's declared row."""
import base64, importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
FOUND = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation')
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'

spec = importlib.util.spec_from_file_location('owner', os.path.join(FOUND, 'execution_inputs_model.v1.py'))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def blobs_of(e):
    out = {}
    for d, b in e['blobs'].items():
        try:
            out[d] = base64.b64decode(b) if isinstance(b, str) else bytes(b)
        except Exception:
            pass
    return out


def jload(raw):
    try:
        return json.loads(raw)
    except Exception:
        return None


out = {}
for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    ex = json.load(open(os.path.join(RB, name, 'exact-export.json')))
    bl = blobs_of(ex)
    objects = {k: (v['domain'], v['record']) for k, v in ex['objectTable'].items()}
    ei = ep = None
    invs = {}
    for d, raw in bl.items():
        doc = jload(raw)
        if not isinstance(doc, dict):
            continue
        if 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            ei = doc
        if doc.get('schemaVersion') == 1 and 'cells' in doc and 'membershipDigest' in doc:
            ep = doc
        if doc.get('schemaVersion') == 1 and 'rows' in doc and 'examinedPaths' in doc:
            invs[d] = doc
    scopes = {k: v[1] for k, v in objects.items() if v[0] == 'subject-scope'}
    covs = {k.split(':', 1)[1]: v[1] for k, v in objects.items() if v[0] == 'coverage'}

    print('\n===', name)
    rows = []
    for r in ei['cellOutcomes']:
        if r['capabilityId'] != 'clones-fact':
            continue
        ci, po = r['cellOrdinal'], r['programOrdinal']
        cell = ep['cells'][ci]
        binding = next(b for b in cell['programBindings'] if b['ordinal'] == po)
        acc = next(a for a in ei['nativeCoverageAccounts']
                   if a['cellOrdinal'] == ci and a['programOrdinal'] == po
                   and a['relation'] == 'clones')
        expected = M.expected_source_census('clones', cell, binding, invs, r.get('inventoryDigests') or [])
        covered = set()
        recs = []
        for chx in acc['coverageIds']:
            env = covs.get(chx)
            if not env:
                continue
            sc = scopes.get(env['scopeId'])
            if sc:
                covered |= set(sc.get('subjects') or [])
            payload = jload(bl.get(env['payloadDigest'], b'')) or {}
            recs.append({'id': chx, 'entry': payload.get('entry') or {}})
        summary = M._summarize_coverage_records(recs, expected, covered)
        missing = sorted(expected - covered)
        row = {'run': name, 'cell': ci, 'program': po,
               'expectedCount': len(expected), 'coveredCount': len(covered),
               'missing': missing,
               'ownerAccountState': summary['accountState'],
               'ownerAccountDeficiency': summary['deficiency'],
               'ownerAccountNativeCause': summary['nativeCause'],
               'coverageRecordDeficiencies': [c['deficiency'] for c in summary['coverageRecords']],
               'consumerRowState': r['state'],
               'consumerRowPair': [r.get('deficiency'), r.get('nativeCause')]}
        rows.append(row)
        print('  c%s/p%s expected=%d covered=%d missing=%s' % (ci, po, len(expected), len(covered), missing))
        print('     owner account : state=%s deficiency=%s cause=%s (coverage record deficiencies=%s)' % (
            summary['accountState'], summary['deficiency'], summary['nativeCause'],
            row['coverageRecordDeficiencies']))
        print('     consumer row  : state=%s pair=%s' % (r['state'], tuple(row['consumerRowPair'])))
    out[name] = rows

json.dump(out, open(os.path.join(HERE, 'p17-clones-census.json'), 'w'), indent=2, default=str)
print('\nWROTE p17-clones-census.json')
