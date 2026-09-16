"""PROBE F3 (v27) — identify exactly which retained blobs differ between the shipped and
the freshly built exports, whether any DIFFERING blob is reachable from the admitted
closure, and whether the freshly built exports themselves pass structural custody and
complete semantic replay through the snapshot27 owner."""
import base64, glob, hashlib, importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
arb = sorted(glob.glob('/tmp/indep27-arbitrary-*/deep/nested/elsewhere'))[-1]

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner27_f3', op)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def sha(b):
    return hashlib.sha256(b).hexdigest()


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
        p = base64.b64decode(v, validate=True)
        assert sha(p) == dg
        blobs[dg] = p
    objects, seen = {}, set()
    for dg, meta in e['frames'].items():
        dom, ident = meta['domain'], meta['identity']
        seen.add(ident)
        cx = bytes.fromhex(meta['canonicalBytesHex'])
        desc = e['objectTable'][ident] if ident in e['objectTable'] else json.loads(cx, object_pairs_hook=nodup)
        if dom != 'canonical-record' and dom in M.PREFIX and ident in e['objectTable']:
            objects[ident] = (dom, desc)
    for ident in set(e['objectTable']) - seen:
        pass
    return e, objects, blobs


CASES = [
    ('checkpoint3/ts.store.json', os.path.join(arb, 'a-checkpoint3/checkpoint3/ts.store.json')),
    ('normalized-examples6/rust.store.json', os.path.join(arb, 'b-normalized/normalized-examples6/rust.store.json')),
    ('rust-selection-examples1/rust-bin.store.json', os.path.join(arb, 'c-rust-selection/rust-selection-examples1/rust-bin.store.json')),
    ('semantic-controls1/severity.store.json', os.path.join(arb, 'd-controls/semantic-controls1/severity.store.json')),
    ('binding-controls/ts-lawful-default.store.json', os.path.join(arb, 'e-binding-controls/ts-lawful-default.store.json')),
]
HEX = re.compile(r'[0-9a-f]{64}')
res = {'arbitraryRoot': arb, 'cases': []}
for rel, freshpath in CASES:
    shipped_raw = open(os.path.join(PKG, rel), 'rb').read()
    fresh_raw = open(freshpath, 'rb').read()
    se, sobj, sblob = decode(shipped_raw)
    fe, fobj, fblob = decode(fresh_raw)
    only_shipped = sorted(set(sblob) - set(fblob))
    only_fresh = sorted(set(fblob) - set(sblob))
    # which digests are referenced anywhere in the descriptor graph text?
    graph_text = json.dumps(se['objectTable']) + json.dumps(se['frames'])
    referenced = set(HEX.findall(graph_text))
    graph_text_f = json.dumps(fe['objectTable']) + json.dumps(fe['frames'])
    referenced_f = set(HEX.findall(graph_text_f))
    row = {
        'file': rel,
        'blobsOnlyInShipped': len(only_shipped), 'blobsOnlyInFresh': len(only_fresh),
        'sharedBlobsAllIdentical': all(sblob[d] == fblob[d] for d in set(sblob) & set(fblob)),
        'onlyShippedReferencedByGraph': sorted(d for d in only_shipped if d in referenced)[:6],
        'onlyFreshReferencedByGraph': sorted(d for d in only_fresh if d in referenced_f)[:6],
        'countOnlyShippedReferenced': sum(1 for d in only_shipped if d in referenced),
        'countOnlyFreshReferenced': sum(1 for d in only_fresh if d in referenced_f),
        'sampleOnlyShippedBytes': [sblob[d][:110].decode('utf-8', 'replace') for d in only_shipped[:2]],
        'sampleOnlyFreshBytes': [fblob[d][:110].decode('utf-8', 'replace') for d in only_fresh[:2]],
    }
    res['cases'].append(row)
    print('### %s' % rel)
    for k, v in row.items():
        if k == 'file':
            continue
        print('    %-34s %s' % (k, json.dumps(v)[:230]))
    print()

# ---- replay the FRESH exports through the snapshot27 owner ----
print('--- fresh-build replay through snapshot27 owner ---')
import importlib
sys.path.insert(0, '/tmp/opensip-design-corrections/claude-independent-design.v27/probes')
replay = []
GROUPS = [(os.path.join(arb, 'a-checkpoint3/checkpoint3'), 'positive'),
          (os.path.join(arb, 'b-normalized/normalized-examples6'), 'positive'),
          (os.path.join(arb, 'c-rust-selection/rust-selection-examples1'), 'positive'),
          (os.path.join(arb, 'd-controls/semantic-controls1'), 'false-result-control'),
          (os.path.join(arb, 'e-binding-controls'), 'binding-control')]
EX = importlib.import_module('pE_exports') if False else None
for gdir, klass in GROUPS:
    claims = json.load(open(os.path.join(gdir, 'claims.json')))
    for c in claims:
        raw = open(os.path.join(gdir, c['path']), 'rb').read()
        r = {'group': os.path.basename(gdir), 'name': c.get('name'), 'class': klass,
             'claimedRunId': c['runId']}
        try:
            e, objects, blobs = decode(raw)
            dom, run = objects[c['runId']]
            try:
                rid, _ = M.open_run_closure(run, objects, blobs)
                r['structural'] = 'ADMIT'
                r['structuralIdMatches'] = rid == c['runId']
            except Exception as ex:
                r['structural'] = 'REFUSE'
                r['structuralReason'] = str(ex)[:110]
            try:
                rid2 = M.close_run(run, objects, blobs)
                r['semantic'] = 'ADMIT'
                r['semanticIdMatches'] = rid2 == c['runId']
            except Exception as ex:
                r['semantic'] = 'REFUSE'
                r['semanticReason'] = str(ex)[:110]
        except Exception as ex:
            r['decodeError'] = str(ex)[:160]
        replay.append(r)
        print('%-30s %-22s structural=%-7s semantic=%-7s' % (
            r.get('name'), klass, r.get('structural'), r.get('semantic')))
res['freshBuildReplay'] = replay
res['freshPositivesAllAdmit'] = all(
    r.get('structural') == 'ADMIT' and r.get('semantic') == 'ADMIT'
    for r in replay if r['class'] == 'positive')
res['freshControlsAllStructuralAdmitSemanticRefuse'] = all(
    r.get('structural') == 'ADMIT' and r.get('semantic') == 'REFUSE'
    for r in replay if r['class'] == 'false-result-control')
print()
print('fresh positives all admit            :', res['freshPositivesAllAdmit'])
print('fresh controls admit-then-replay-fail:', res['freshControlsAllStructuralAdmitSemanticRefuse'])
json.dump(res, open(os.path.join(OUT, 'pF3-blobdelta.json'), 'w'), indent=1)
