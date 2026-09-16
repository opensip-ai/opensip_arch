"""P4: examine the exact retained records behind each observed difference."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'


def blobs_of(export):
    out = {}
    for d, b in export['blobs'].items():
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


matrix = json.load(open(os.path.join(ROOT32, 'docs/coop/design-corrections/native/native-capability-matrix.v2.json')))
cells = matrix['cells']
print('matrix cells:', len(cells))


def matrix_cell(cap, mode):
    for c in cells:
        if c.get('capability') == cap and c.get('mode') == mode:
            return c
    return None


out = {'standing': 'read-only record inspection over exact exports and frozen matrix'}

# ---- CLASS D: syntax-data imports@resolved-target under syntax-only
mc = matrix_cell('imports', 'syntax-only')
print('\n=== matrix cell (imports, syntax-only)')
print(json.dumps(mc, indent=1)[:900])
out['matrixImportsSyntaxOnly'] = mc

sd = json.load(open(os.path.join(RB, 'syntax-data', 'exact-export.json')))
sdb = blobs_of(sd)
objects = {k: (v['domain'], v['record']) for k, v in sd['objectTable'].items()}

target = '35347f62513d44fea34de28f6a5ab85c814729c7b272e3ab38496331995072ea'
found = None
for oid, rec in objects.items():
    if isinstance(rec, (list, tuple)) and len(rec) == 2 and rec[0] == 'coverage':
        if target in oid:
            found = (oid, rec[1])
print('\n=== syntax-data coverage envelope named by the imports account')
print(found[0] if found else 'NOT FOUND in object table')
if found:
    env = found[1]
    print(json.dumps(env, indent=1)[:500])
    payload = jload(sdb.get(env.get('payloadDigest'), b''))
    print('payload key  :', json.dumps((payload or {}).get('key'), indent=1))
    entry = (payload or {}).get('entry') or {}
    print('entry coverage           :', entry.get('coverage'))
    print('entry deficiency         :', entry.get('deficiency'))
    print('entry nativeCause        :', entry.get('nativeCause'))
    print('entry resolutionCompleteness:', json.dumps(entry.get('resolutionCompleteness')))
    out['syntaxDataImportsCoverage'] = {
        'coverageId': found[0], 'key': (payload or {}).get('key'),
        'coverage': entry.get('coverage'), 'deficiency': entry.get('deficiency'),
        'nativeCause': entry.get('nativeCause'),
        'resolutionCompleteness': entry.get('resolutionCompleteness'),
    }

# ---- CLASS B: syntax-code cell3 unresolved-edge binding carrier + matrix pair
mcb = matrix_cell('unresolved-edge', 'syntax-only')
print('\n=== matrix cell (unresolved-edge, syntax-only)')
print(json.dumps(mcb, indent=1)[:700])
out['matrixUnresolvedEdgeSyntaxOnly'] = mcb

sc = json.load(open(os.path.join(RB, 'syntax-code', 'exact-export.json')))
scb = blobs_of(sc)
ep = None
for d, raw in scb.items():
    doc = jload(raw)
    if isinstance(doc, dict) and doc.get('schemaVersion') == 1 and 'cells' in doc and 'membershipDigest' in doc:
        ep = doc
for ci, cell in enumerate(ep['cells']):
    if cell['capabilityId'] == 'unresolved-edge':
        b = cell['programBindings'][0]
        print('\n=== syntax-code cell %d unresolved-edge binding' % ci)
        print(json.dumps({k: b.get(k) for k in
                          ('ordinal', 'universe', 'enumerator', 'deficiency', 'nativeCause')}, indent=1))
        out['syntaxCodeUnresolvedEdgeBinding'] = {
            'cellOrdinal': ci, 'required': cell.get('required'),
            'binding': {k: b.get(k) for k in ('ordinal', 'universe', 'enumerator', 'deficiency', 'nativeCause')},
            'matrixDeficiency': (mcb or {}).get('deficiency'),
            'bindingCarrierEqualsMatrixPair':
                b.get('deficiency') == (mcb or {}).get('deficiency'),
        }

# ---- the cellOutcomes rows, for the OUTCOME_DERIVE / CAUSE_CARRIER faults
for name in ('syntax-code', 'syntax-data'):
    ex = json.load(open(os.path.join(RB, name, 'exact-export.json')))
    bl = blobs_of(ex)
    ei = None
    for d, raw in bl.items():
        doc = jload(raw)
        if isinstance(doc, dict) and 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            ei = doc
    print('\n=== %s cellOutcomes' % name)
    rows = []
    for r in ei['cellOutcomes']:
        rows.append({k: r.get(k) for k in
                     ('cellOrdinal', 'programOrdinal', 'capabilityId', 'languageMode', 'required',
                      'enumeratorStatus', 'universe', 'state', 'deficiency', 'nativeCause',
                      'stageOrdinal', 'stageOrdinalNullReason', 'candidateResultDigest')})
        print('   c%s/p%s %-16s %-12s sel=%-10s U=%s state=%-11s def=%-26s cause=%s' % (
            r.get('cellOrdinal'), r.get('programOrdinal'), r.get('capabilityId'),
            r.get('languageMode'), r.get('enumeratorStatus'),
            (str(r.get('universe'))[:8] if r.get('universe') else 'null'),
            r.get('state'), r.get('deficiency'), r.get('nativeCause')))
    out.setdefault('cellOutcomes', {})[name] = rows

json.dump(out, open(os.path.join(HERE, 'p4-records.json'), 'w'), indent=2, default=str)
print('\nWROTE p4-records.json')
