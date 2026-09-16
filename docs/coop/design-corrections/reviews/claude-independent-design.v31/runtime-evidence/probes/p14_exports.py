"""PROBE 14 (v31) — INDEPENDENT decode and replay of all 13 exact stored cases through BOTH
identity-model.v3.open_run_closure (structural custody) and identity-model.v3.close_run (complete
semantic replay), using the snapshot31 owner. My own store decoder; the package's checkers are not
imported; root's expected outcomes are not treated as correctness evidence and no export is repaired.
"""
import base64, hashlib, importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner31', op)
M = importlib.util.module_from_spec(spec)
sys.modules['owner31'] = M
spec.loader.exec_module(M)

R = {'standing': ('INDEPENDENT re-execution: my own decoder, owner taken from frozen snapshot31, '
                  'package checkers not imported, no export repaired.'),
     'ownerPath': 'docs/coop/design-corrections/foundation/identity-model.v3.py',
     'ownerSha256': hashlib.sha256(open(op, 'rb').read()).hexdigest(),
     'structuralBoundary': 'identity-model.v3.open_run_closure',
     'semanticBoundary': 'identity-model.v3.close_run (complete replay)'}


def nodup(pairs):
    d = {}
    for k, v in pairs:
        assert k not in d, 'duplicate key ' + k
        d[k] = v
    return d


def decode(raw):
    e = json.loads(raw, object_pairs_hook=nodup)
    blobs = {}
    for dg, v in e['blobs'].items():
        p = base64.b64decode(v, validate=True)
        assert hashlib.sha256(p).hexdigest() == dg, 'blob digest mismatch'
        blobs[dg] = p
    objects = {}
    for dg, meta in e['frames'].items():
        dom, ident = meta['domain'], meta['identity']
        cx = bytes.fromhex(meta['canonicalBytesHex'])
        desc = e['objectTable'][ident] if ident in e['objectTable'] else json.loads(cx, object_pairs_hook=nodup)
        if dom != 'canonical-record' and dom in M.PREFIX and ident in e['objectTable']:
            objects[ident] = (dom, desc)
    return e, objects, blobs


GROUPS = [('checkpoint3', 'positive'), ('normalized-examples6', 'positive'),
          ('rust-selection-examples1', 'positive'), ('semantic-controls1', 'false-result-control'),
          ('binding-controls', 'binding-control')]
rows = []
for g, klass in GROUPS:
    d = os.path.join(PKG, g)
    claims = json.load(open(os.path.join(d, 'claims.json')))
    for c in claims:
        path = os.path.join(d, c['path'])
        raw = open(path, 'rb').read()
        row = {'group': g, 'class': klass, 'name': c.get('name'), 'path': c['path'],
               'exportSha256': hashlib.sha256(raw).hexdigest(), 'exportBytes': len(raw),
               'claimedRunId': c['runId']}
        try:
            e, objects, blobs = decode(raw)
            row['decodedObjects'] = len(objects)
            row['decodedBlobs'] = len(blobs)
            dom, run = objects[c['runId']]
            try:
                rid, _ = M.open_run_closure(run, objects, blobs)
                row['structuralCustody'] = 'ADMIT'
                row['structuralRunId'] = rid
                row['structuralRunIdMatchesClaim'] = rid == c['runId']
            except Exception as ex:
                row['structuralCustody'] = 'REFUSE'
                row['structuralReason'] = '%s: %s' % (type(ex).__name__, ex)
            try:
                rid2 = M.close_run(run, objects, blobs)
                row['semanticReplay'] = 'ADMIT'
                row['semanticRunId'] = rid2
                row['semanticRunIdMatchesClaim'] = rid2 == c['runId']
            except Exception as ex:
                row['semanticReplay'] = 'REFUSE'
                row['semanticReason'] = '%s: %s' % (type(ex).__name__, ex)
        except Exception as ex:
            row['decodeError'] = '%s: %s' % (type(ex).__name__, ex)
        rows.append(row)
        print('%-30s %-21s struct=%-7s sem=%-7s idOk=%-5s %s' % (
            row['name'], klass, row.get('structuralCustody'), row.get('semanticReplay'),
            row.get('semanticRunIdMatchesClaim', row.get('structuralRunIdMatchesClaim')),
            str(row.get('semanticReason', ''))[:60]))

R['rows'] = rows
pos = [r for r in rows if r['class'] == 'positive']
neg = [r for r in rows if r['class'] == 'false-result-control']
bind = [r for r in rows if r['class'] == 'binding-control']
R['counts'] = {'positives': len(pos), 'falseResultControls': len(neg), 'bindingControls': len(bind),
               'total': len(rows)}
R['positivesAllAdmitBoth'] = all(r.get('structuralCustody') == 'ADMIT'
                                 and r.get('semanticReplay') == 'ADMIT'
                                 and r.get('semanticRunIdMatchesClaim') for r in pos)
R['negativesAdmitStructurallyThenReplayRefuse'] = all(
    r.get('structuralCustody') == 'ADMIT' and r.get('semanticReplay') == 'REFUSE' for r in neg)
R['bindingInvalidDefaultRefused'] = any(
    r['name'] == 'ts-invalid-default-entry' and r.get('structuralCustody') == 'ADMIT'
    and r.get('semanticReplay') == 'REFUSE' for r in bind)
R['bindingLawfulAdmitted'] = all(
    r.get('semanticReplay') == 'ADMIT' for r in bind if r['name'] != 'ts-invalid-default-entry')
R['allRunIdsDistinct'] = len({r['claimedRunId'] for r in rows}) == len(
    {r['claimedRunId'] for r in rows})
print('\ncounts:', json.dumps(R['counts']))
print('positives admit both boundaries         :', R['positivesAllAdmitBoth'])
print('negatives admit then replay-refuse      :', R['negativesAdmitStructurallyThenReplayRefuse'])
print('binding invalid-default refused         :', R['bindingInvalidDefaultRefused'])
print('binding lawful default+explicit admitted:', R['bindingLawfulAdmitted'])
print('\nrefusal reasons (controls):')
for r in neg + [x for x in bind if x.get('semanticReplay') == 'REFUSE']:
    print('   %-30s %s' % (r['name'], str(r.get('semanticReason'))[:110]))
json.dump(R, open(os.path.join(OUT, 'p14-exports.json'), 'w'), indent=1)
print('\nwrote p14-exports.json')
