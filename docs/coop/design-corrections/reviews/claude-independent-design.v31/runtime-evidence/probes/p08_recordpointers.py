"""PROBE 08 (v31) — do the native bundle's x-opensip-digest record pointers RESOLVE on frozen31?

The source29 note says identity-schemas.v3 is named current. Two references to
foundation/identity-schemas.v2.json remain in the bundle. I check whether every annotation's
record.document exists in frozen31 and whether its selector resolves inside that document, so I can
say whether the remaining v2 pointers are dangling or a deliberate historical owner.
"""
import json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
N = os.path.join(SRC, 'docs/coop/design-corrections/native')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
sch = json.load(open(os.path.join(N, 'native-evidence.schemas.v2.json')))
R = {}

sites = []
def walk(o, path='$'):
    if isinstance(o, dict):
        if 'x-opensip-digest' in o:
            sites.append({'path': path, 'a': o['x-opensip-digest']})
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
walk(sch)

docs = {}
for s in sites:
    a = s['a']
    for key in ('record', 'frame', 'artifact', 'closure', 'owner'):
        blk = a.get(key)
        if isinstance(blk, dict) and 'document' in blk:
            docs.setdefault((blk['document'], blk.get('selector')), []).append(s['path'])
R['pointerCount'] = sum(len(v) for v in docs.values())
print('annotation sites: %d | distinct (document, selector) pointers: %d'
      % (len(sites), len(docs)))


def resolve(doc, selector):
    """doc is a path relative to docs/coop/design-corrections (or a full docs/ path)."""
    cands = ['docs/coop/design-corrections/' + doc, doc, 'docs/' + doc]
    rel = next((c for c in cands if c in man), None)
    if rel is None:
        return {'documentInFrozen31': False, 'resolvedPath': None}
    out = {'documentInFrozen31': True, 'resolvedPath': rel}
    if not selector or not selector.startswith('#/'):
        return out
    if not rel.endswith('.json'):
        out['selectorResolves'] = None
        return out
    d = json.load(open(os.path.join(SRC, rel)))
    cur = d
    try:
        for part in selector[2:].split('/'):
            part = part.replace('~1', '/').replace('~0', '~')
            cur = cur[part]
        out['selectorResolves'] = True
    except Exception as e:
        out['selectorResolves'] = False
        out['selectorError'] = str(e)[:100]
    return out


rows = []
for (doc, sel), paths in sorted(docs.items()):
    info = resolve(doc, sel)
    info.update(document=doc, selector=sel, siteCount=len(paths), samplePath=paths[0])
    rows.append(info)
    flag = ''
    if not info['documentInFrozen31']:
        flag = '  <-- DOCUMENT NOT IN FROZEN31'
    elif info.get('selectorResolves') is False:
        flag = '  <-- SELECTOR DOES NOT RESOLVE'
    print('%-52s %-34s sites=%-3d inFrozen=%-5s selector=%s%s'
          % (doc[:52], str(sel)[:34], len(paths), info['documentInFrozen31'],
             info.get('selectorResolves'), flag))
R['pointers'] = rows
R['documentsNotInFrozen31'] = [r for r in rows if not r['documentInFrozen31']]
R['selectorsNotResolving'] = [r for r in rows if r.get('selectorResolves') is False]
R['allPointersResolve'] = not R['documentsNotInFrozen31'] and not R['selectorsNotResolving']
print('\nall record pointers resolve on frozen31 :', R['allPointersResolve'])

# is owner-source-set ALSO in identity-schemas.v3?
v3 = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-schemas.v3.json')))
R['ownerSourceSetInV3'] = 'owner-source-set' in v3.get('$defs', {})
R['importInV3'] = 'import' in v3.get('$defs', {})
v2p = 'docs/coop/design-corrections/foundation/identity-schemas.v2.json'
R['identitySchemasV2InFrozen31'] = v2p in man
print('identity-schemas.v2.json present in frozen31 :', R['identitySchemasV2InFrozen31'])
print('owner-source-set defined in v3               :', R['ownerSourceSetInV3'])
print('import defined in v3                         :', R['importInV3'])

json.dump(R, open(os.path.join(OUT, 'p08-recordpointers.json'), 'w'), indent=1, default=str)
print('\nwrote p08-recordpointers.json')
