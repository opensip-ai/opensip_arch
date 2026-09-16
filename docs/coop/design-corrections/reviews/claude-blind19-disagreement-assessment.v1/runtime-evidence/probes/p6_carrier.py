"""P6: isolate the outcome/carrier difference (root's 'class C')."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'


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


out = {'standing': 'read-only inspection of retained inventories/coverage behind each cell outcome'}
for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    ex = json.load(open(os.path.join(RB, name, 'exact-export.json')))
    bl = blobs_of(ex)
    objects = {k: (v['domain'], v['record']) for k, v in ex['objectTable'].items()}
    ei = None
    invs = {}
    for d, raw in bl.items():
        doc = jload(raw)
        if not isinstance(doc, dict):
            continue
        if 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            ei = doc
        if doc.get('schemaVersion') == 1 and 'rows' in doc and 'examinedPaths' in doc:
            invs[d] = doc
    cov_payload = {}
    for oid, rec in objects.items():
        if rec[0] == 'coverage':
            p = jload(bl.get(rec[1]['payloadDigest'], b'')) or {}
            cov_payload[oid.split(':', 1)[1]] = p
    acc_by = {(a['cellOrdinal'], a['programOrdinal']): [] for a in ei['nativeCoverageAccounts']}
    for a in ei['nativeCoverageAccounts']:
        acc_by[(a['cellOrdinal'], a['programOrdinal'])].append(a)

    print('\n===', name)
    rows = []
    for r in ei['cellOutcomes']:
        ci, po = r['cellOrdinal'], r['programOrdinal']
        inv_states = []
        for d in r.get('inventoryDigests') or []:
            iv = invs.get(d)
            if iv:
                inv_states.append({'digest': d[:12], 'kind': iv.get('kind'), 'state': iv.get('state'),
                                   'deficiency': iv.get('deficiency'), 'nativeCause': iv.get('nativeCause')})
        cov_states = []
        for a in acc_by.get((ci, po), []):
            for c in a['coverageIds']:
                p = cov_payload.get(c, {})
                e = p.get('entry') or {}
                cov_states.append({'rel': a['relation'], 'rung': a['resolution'],
                                   'coverage': e.get('coverage'), 'deficiency': e.get('deficiency'),
                                   'nativeCause': e.get('nativeCause')})
        row = {'cell': ci, 'program': po, 'capabilityId': r['capabilityId'],
               'required': r.get('required'), 'hostState': r['state'],
               'hostDeficiency': r.get('deficiency'), 'hostNativeCause': r.get('nativeCause'),
               'inventories': inv_states, 'coverageEntries': cov_states}
        rows.append(row)
        print('  c%s/p%s %-15s req=%-5s hostState=%-11s hostPair=(%s,%s)' % (
            ci, po, r['capabilityId'], r.get('required'), r['state'],
            r.get('deficiency'), r.get('nativeCause')))
        for iv in inv_states:
            print('        inv  %-8s state=%-10s pair=(%s,%s)' % (iv['kind'], iv['state'],
                                                                  iv['deficiency'], iv['nativeCause']))
        for c in cov_states:
            print('        cov  %-14s@%-20s coverage=%-8s pair=(%s,%s)' % (
                c['rel'], c['rung'], c['coverage'], c['deficiency'], c['nativeCause']))
    out.setdefault('runs', {})[name] = rows

json.dump(out, open(os.path.join(HERE, 'p6-carrier.json'), 'w'), indent=2)
print('\nWROTE p6-carrier.json')
