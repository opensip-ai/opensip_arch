"""P09 — verify author package 8 and independently replay all 13 exact Run/control outcomes
through BOTH open_run_closure and close_run with my own decoder and the snapshot32 owner."""
import base64, hashlib, importlib.util, json, os, sys

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v8'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
MAN32 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
EXP_AM = '116a0f301f92f5cdca9f2824efd3b701036870e2a1484457208641caf8dbcab4'
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


amp = os.path.join(PKG, 'artifact-manifest.json')
R['artifactManifestSha256'] = sha(amp)
R['artifactManifestMatchesDeclared'] = R['artifactManifestSha256'] == EXP_AM
am = json.load(open(amp))
rows = am['files'] if isinstance(am, dict) else am
ok = bad = miss = 0
for r in rows:
    p = os.path.join(PKG, r['path'])
    if not os.path.isfile(p):
        miss += 1
    elif sha(p) == r['sha256']:
        ok += 1
    else:
        bad += 1
R.update(declaredMembers=len(rows), verified=ok, mismatched=bad, missing=miss)
print('package8 manifest matches declared:', R['artifactManifestMatchesDeclared'])
print('members %d verified %d mismatched %d missing %d' % (len(rows), ok, bad, miss))

smp = os.path.join(PKG, 'source-manifest.json')
R['sourceManifestSha256'] = sha(smp)
R['sourceManifestEqualsFrozen32Manifest'] = R['sourceManifestSha256'] == sha(MAN32)
print('package source-manifest is byte-equal to the frozen32 manifest:',
      R['sourceManifestEqualsFrozen32Manifest'])

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner32', op)
M = importlib.util.module_from_spec(spec)
sys.modules['owner32'] = M
spec.loader.exec_module(M)
R['ownerSha256'] = sha(op)


def nodup(pairs):
    d = {}
    for k, v in pairs:
        assert k not in d
        d[k] = v
    return d


def decode(raw):
    e = json.loads(raw, object_pairs_hook=nodup)
    blobs = {}
    for dg, v in e['blobs'].items():
        b = base64.b64decode(v, validate=True)
        assert hashlib.sha256(b).hexdigest() == dg
        blobs[dg] = b
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
out = []
for g, klass in GROUPS:
    d = os.path.join(PKG, g)
    for c in json.load(open(os.path.join(d, 'claims.json'))):
        raw = open(os.path.join(d, c['path']), 'rb').read()
        row = {'group': g, 'class': klass, 'name': c.get('name'),
               'exportSha256': hashlib.sha256(raw).hexdigest(), 'claimedRunId': c['runId']}
        e, objects, blobs = decode(raw)
        dom, run = objects[c['runId']]
        try:
            rid, _ = M.open_run_closure(run, objects, blobs)
            row['structural'] = 'ADMIT'
            row['structuralIdMatches'] = rid == c['runId']
        except Exception as ex:
            row['structural'] = 'REFUSE'
            row['structuralReason'] = '%s: %s' % (type(ex).__name__, ex)
        try:
            rid2 = M.close_run(run, objects, blobs)
            row['semantic'] = 'ADMIT'
            row['semanticIdMatches'] = rid2 == c['runId']
        except Exception as ex:
            row['semantic'] = 'REFUSE'
            row['semanticReason'] = '%s: %s' % (type(ex).__name__, ex)
        out.append(row)
        print('%-30s %-21s struct=%-7s sem=%-7s idOk=%-5s %s'
              % (row['name'], klass, row['structural'], row['semantic'],
                 row.get('semanticIdMatches', row.get('structuralIdMatches')),
                 str(row.get('semanticReason', ''))[:52]))
R['rows'] = out
pos = [r for r in out if r['class'] == 'positive']
neg = [r for r in out if r['class'] == 'false-result-control']
bind = [r for r in out if r['class'] == 'binding-control']
R['counts'] = {'positives': len(pos), 'negatives': len(neg), 'bindingControls': len(bind),
               'total': len(out)}
R['positivesAdmitBoth'] = all(r['structural'] == 'ADMIT' and r['semantic'] == 'ADMIT'
                              and r.get('semanticIdMatches') for r in pos)
R['negativesAdmitThenRefuse'] = all(r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE'
                                    for r in neg)
R['bindingInvalidRefused'] = any(r['name'] == 'ts-invalid-default-entry'
                                 and r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE'
                                 for r in bind)
R['bindingLawfulAdmitted'] = all(r['semantic'] == 'ADMIT' for r in bind
                                 if r['name'] != 'ts-invalid-default-entry')
print('\ncounts %s' % json.dumps(R['counts']))
print('positives admit both        :', R['positivesAdmitBoth'])
print('negatives admit then refuse :', R['negativesAdmitThenRefuse'])
print('binding invalid refused     :', R['bindingInvalidRefused'])
print('binding lawful admitted     :', R['bindingLawfulAdmitted'])
json.dump(R, open(os.path.join(OUT, 'p09-package8.json'), 'w'), indent=1, default=str)
print('\nwrote p09-package8.json')
