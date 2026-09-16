"""P8: all _carrier call sites, and the candidate records behind the clones-fact outcomes."""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
MODEL = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py')
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'

src = open(MODEL).read()
lines = src.split('\n')
print('=== _carrier call sites')
sites = []
for m in re.finditer(r'_carrier\(', src):
    ln = src[:m.start()].count('\n') + 1
    if lines[ln - 1].strip().startswith('def '):
        continue
    sites.append({'line': ln, 'text': lines[ln - 1].strip()})
    print('  %d  %s' % (ln, lines[ln - 1].strip()[:170]))

print('\n=== CAUSE_CARRIER raise sites')
cc = []
for m in re.finditer(r'EXECUTION_INPUTS_CAUSE_CARRIER', src):
    ln = src[:m.start()].count('\n') + 1
    cc.append({'line': ln, 'text': lines[ln - 1].strip()})
    print('  %d  %s' % (ln, lines[ln - 1].strip()[:170]))


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


print('\n=== candidate records behind clones-fact outcomes')
cand_out = {}
for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    ex = json.load(open(os.path.join(RB, name, 'exact-export.json')))
    bl = blobs_of(ex)
    ei = None
    for d, raw in bl.items():
        doc = jload(raw)
        if isinstance(doc, dict) and 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            ei = doc
    print('---', name)
    rows = []
    for r in ei['cellOutcomes']:
        cd = r.get('candidateResultDigest')
        if not cd and r['capabilityId'] not in ('clones-fact', 'clones-near', 'clones-cross-tsjs'):
            continue
        rec = jload(bl.get(cd, b'')) if cd else None
        row = {'cell': r['cellOrdinal'], 'program': r['programOrdinal'],
               'capabilityId': r['capabilityId'], 'required': r.get('required'),
               'hostState': r['state'], 'hostPair': [r.get('deficiency'), r.get('nativeCause')],
               'candidateResultDigest': cd,
               'candidateState': (rec or {}).get('state'),
               'candidateDeficiency': (rec or {}).get('deficiency'),
               'candidateNativeCause': (rec or {}).get('nativeCause'),
               'candidateKeys': sorted(rec.keys()) if isinstance(rec, dict) else None}
        rows.append(row)
        print('   c%s/p%s %-16s hostState=%-9s hostPair=%s | candidate state=%s pair=(%s,%s)' % (
            row['cell'], row['program'], row['capabilityId'], row['hostState'],
            tuple(row['hostPair']), row['candidateState'],
            row['candidateDeficiency'], row['candidateNativeCause']))
    cand_out[name] = rows

json.dump({'carrierCallSites': sites, 'causeCarrierSites': cc, 'candidates': cand_out},
          open(os.path.join(HERE, 'p8-candidate-carrier.json'), 'w'), indent=2)
print('\nWROTE p8-candidate-carrier.json')
