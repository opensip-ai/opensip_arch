"""PROBE E (v27) — INDEPENDENT re-execution of every author export.

I do not run the package's check-export.v4.py. I decode each store with my own reader and
drive the reference owner taken from FROZEN SNAPSHOT 27, distinguishing the two boundaries
explicitly:
    structural custody  = identity-model.v3.open_run_closure
    semantic authority  = identity-model.v3.close_run   (complete replay)

Expected, from the REFERENCE OWNERS (not from the package's claims):
  7 positives  -> structural ADMIT and semantic ADMIT, recomputed RunId == claimed
  3 false-result controls -> structural ADMIT, semantic REFUSE
  binding: lawful-default ADMIT, lawful-explicit-selection ADMIT,
           invalid-default-entry REFUSED somewhere
No export byte is repaired, reminted or substituted.
"""
import base64, hashlib, importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

owner_path = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner27_independent', owner_path)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
OWNER_SHA = hashlib.sha256(open(owner_path, 'rb').read()).hexdigest()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def nodup(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('duplicate export key ' + k)
        d[k] = v
    return d


def decode(raw):
    """My own reader. Verifies every retained blob and every frame's metadata, and
    supplies the owner ONLY descriptors the export actually placed in objectTable."""
    e = json.loads(raw, object_pairs_hook=nodup)
    blobs = {}
    for dg, v in e['blobs'].items():
        assert re.fullmatch('[0-9a-f]{64}', dg)
        p = base64.b64decode(v, validate=True)
        assert sha(p) == dg, 'blob digest mismatch'
        blobs[dg] = p
    objects, seen = {}, set()
    for dg, meta in e['frames'].items():
        assert re.fullmatch('[0-9a-f]{64}', dg)
        dom, ident = meta['domain'], meta['identity']
        assert ident not in seen
        seen.add(ident)
        cx = bytes.fromhex(meta['canonicalBytesHex'])
        assert sha(cx) == meta['canonicalSha256'], 'metadata digest mismatch'
        assert blobs.get(sha(cx)) == cx, 'canonical bytes not retained'
        present = ident in e['objectTable']
        desc = e['objectTable'][ident] if present else json.loads(cx, object_pairs_hook=nodup)
        if M.C.canonical(desc) != cx:
            # only the documented untyped raw-cache bookkeeping field is tolerated
            assert dom == 'canonical-record' and isinstance(desc, dict)
            assert desc.get('_digest') == ident
            assert M.C.canonical({k: v for k, v in desc.items() if k != '_digest'}) == cx
        if dom == 'canonical-record':
            assert dg == sha(cx) and ident == dg
        else:
            assert M.C.identity(dom, desc) == dg, 'H identity metadata mismatch'
            if dom in M.PREFIX:
                assert ident == M.PREFIX[dom] + ':' + dg
                if present:
                    objects[ident] = (dom, desc)
            else:
                assert ident == 'sha256:' + dg
    for ident in set(e['objectTable']) - seen:
        assert re.fullmatch('[0-9a-f]{64}', ident)
        cx = M.C.canonical(e['objectTable'][ident])
        assert sha(cx) == ident and blobs.get(ident) == cx
    return objects, blobs


GROUPS = [
    ('checkpoint3', 'positive'),
    ('normalized-examples6', 'positive'),
    ('rust-selection-examples1', 'positive'),
    ('semantic-controls1', 'false-result-control'),
    ('binding-controls', 'binding-control'),
]
BINDING_EXPECT = {'ts-lawful-default': 'ADMIT', 'ts-lawful-explicit-selection': 'ADMIT',
                  'ts-invalid-default-entry': 'REFUSE'}

rows = []
for grp, klass in GROUPS:
    gdir = os.path.join(PKG, grp)
    claims = json.load(open(os.path.join(gdir, 'claims.json')))
    for c in claims:
        raw = open(os.path.join(gdir, c['path']), 'rb').read()
        row = {'group': grp, 'class': klass, 'name': c.get('name', c['path']),
               'path': c['path'], 'exportSha256': sha(raw), 'exportBytes': len(raw),
               'claimedRunId': c['runId'],
               'structuralCustody': 'NOT-REACHED', 'semanticReplay': 'NOT-REACHED'}
        try:
            objects, blobs = decode(raw)
            dom, run = objects[c['runId']]
            assert dom == 'run'
            row['decodedObjects'] = len(objects)
            row['decodedBlobs'] = len(blobs)
            try:
                rid, _ = M.open_run_closure(run, objects, blobs)
                row['structuralCustody'] = 'ADMIT'
                row['structuralRunId'] = rid
                row['structuralRunIdMatchesClaim'] = (rid == c['runId'])
            except Exception as ex:
                row['structuralCustody'] = 'REFUSE'
                row['structuralReason'] = type(ex).__name__ + ': ' + str(ex)[:170]
            try:
                rid2 = M.close_run(run, objects, blobs)
                row['semanticReplay'] = 'ADMIT'
                row['semanticRunId'] = rid2
                row['semanticRunIdMatchesClaim'] = (rid2 == c['runId'])
            except Exception as ex:
                row['semanticReplay'] = 'REFUSE'
                row['semanticReason'] = type(ex).__name__ + ': ' + str(ex)[:170]
        except Exception as ex:
            row['decodeError'] = type(ex).__name__ + ': ' + str(ex)[:200]
        # my own expectation, derived from the reference owners' laws
        if klass == 'positive':
            row['meetsReferenceExpectation'] = (
                row['structuralCustody'] == 'ADMIT' and row['semanticReplay'] == 'ADMIT'
                and row.get('structuralRunIdMatchesClaim') and row.get('semanticRunIdMatchesClaim'))
        elif klass == 'false-result-control':
            row['meetsReferenceExpectation'] = (
                row['structuralCustody'] == 'ADMIT' and row['semanticReplay'] == 'REFUSE')
        else:
            want = BINDING_EXPECT[row['name']]
            got = 'ADMIT' if (row['structuralCustody'] == 'ADMIT'
                              and row['semanticReplay'] == 'ADMIT') else 'REFUSE'
            row['bindingExpected'] = want
            row['bindingObserved'] = got
            row['meetsReferenceExpectation'] = (got == want)
        rows.append(row)

res = {
    'standing': 'INDEPENDENT re-execution; my own store reader; reference owner taken from '
                'frozen snapshot27; package checkers not imported; no export repaired.',
    'ownerPath': 'docs/coop/design-corrections/foundation/identity-model.v3.py',
    'ownerSha256': OWNER_SHA,
    'structuralBoundary': 'identity-model.v3.open_run_closure',
    'semanticBoundary': 'identity-model.v3.close_run (complete replay)',
    'rows': rows,
    'positives': sum(1 for r in rows if r['class'] == 'positive'),
    'falseResultControls': sum(1 for r in rows if r['class'] == 'false-result-control'),
    'bindingControls': sum(1 for r in rows if r['class'] == 'binding-control'),
    'allMeetReferenceExpectation': all(r['meetsReferenceExpectation'] for r in rows),
}
json.dump(res, open(os.path.join(OUT, 'pE-exports.json'), 'w'), indent=1)

print('owner sha256 (from snapshot27):', OWNER_SHA)
print()
print('%-26s %-22s %-10s %-10s %s' % ('name', 'class', 'structural', 'semantic', 'meets ref expectation'))
for r in rows:
    print('%-26s %-22s %-10s %-10s %s' % (
        r['name'], r['class'], r['structuralCustody'], r['semanticReplay'],
        r['meetsReferenceExpectation']))
print()
print('positives=%d falseResult=%d binding=%d  allMeetReferenceExpectation=%s' % (
    res['positives'], res['falseResultControls'], res['bindingControls'],
    res['allMeetReferenceExpectation']))
for r in rows:
    if r['class'] == 'false-result-control':
        print('  %-24s semantic refusal: %s' % (r['name'], r.get('semanticReason', '')[:120]))
    if r['class'] == 'binding-control' and r['bindingExpected'] == 'REFUSE':
        print('  %-24s refusal: %s' % (r['name'],
              (r.get('semanticReason') or r.get('structuralReason') or '')[:140]))
