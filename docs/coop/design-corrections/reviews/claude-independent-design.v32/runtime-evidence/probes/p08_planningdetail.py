"""P08 — planning detail: which EXISTING module rows carry the new work, which two coverage
verification methods changed, chapter 14 regeneration, and that no new package/filename appears."""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {}

inv = json.load(open(os.path.join(A, 'repository-file-inventory.v1.json')))
rows = [f for f in inv['files']
        if re.search(r'glob|repair|policy\.rs', f['path'] + ' ' + str(f.get('description', '')), re.I)]
R['inventoryRowsTouchingNewWork'] = [{'path': f['path'], 'package': f.get('package'),
                                      'generated': f.get('generated'),
                                      'description': str(f.get('description'))[:260]} for f in rows]
print('--- inventory rows naming glob / repair / policy.rs ---')
for f in R['inventoryRowsTouchingNewWork']:
    print('  %-36s %-20s gen=%s' % (f['path'][:36], f['package'], f['generated']))
    print('      %s' % f['description'][:230])

# no new package or planned filename versus the declared counts
R['paths'] = len(inv['files'])
R['packages'] = len(inv['packages'])
R['countsUnchanged'] = (len(inv['files']) == 198 and len(inv['packages']) == 20)
print('\npaths=%d packages=%d unchanged-counts=%s' % (R['paths'], R['packages'], R['countsUnchanged']))

cov = json.load(open(os.path.join(A, 'implementation-coverage.v1.json')))
meth = []


def walk(o, path='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('verification', 'verificationMethod', 'method') and isinstance(v, str):
                meth.append({'at': path, 'text': v})
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)


walk(cov)
hits = [m for m in meth if re.search(r'glob|repair|closed.?world|portable', m['text'], re.I)]
R['coverageVerificationMethodsTouchingNewWork'] = hits
print('\n--- coverage verification methods naming the new work (%d) ---' % len(hits))
for h in hits:
    print('  %s' % h['at'][-80:])
    print('      %s' % h['text'][:250])

# chapter 14
ch14 = os.path.join(A, '14-repository-and-module-layout.md')
t = open(ch14, encoding='utf-8').read()
R['chapter14Sha256'] = hashlib.sha256(open(ch14, 'rb').read()).hexdigest()
lines = [l.strip() for l in t.splitlines() if re.search(r'glob|repair\.rs|policy\.rs', l, re.I)]
R['chapter14LinesTouchingNewWork'] = lines[:12]
print('\n--- chapter 14 lines naming the new work ---')
for l in lines[:10]:
    print('   %s' % l[:210])

# layer3 vs pin-only distinction
l3 = json.load(open(os.path.join(A, 'implementation-normative-inputs.v3.json')))
p3 = {f['path'] for f in l3['files']}
REPAIR = 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py'
GLOB = 'docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md'
R['layer3HasGlobContract'] = GLOB in p3
R['layer3HasRepairReferenceModule'] = REPAIR in p3
R['pyFilesInLayer3'] = sorted(p for p in p3 if p.endswith('.py'))
print('\nlayer3 contains the glob CONTRACT      :', R['layer3HasGlobContract'])
print('layer3 contains the repair .py module  :', R['layer3HasRepairReferenceModule'])
print('any .py at all in layer3               :', R['pyFilesInLayer3'])
R['referencePyIsNotANormativeInput'] = not R['pyFilesInLayer3']

json.dump(R, open(os.path.join(OUT, 'p08-planningdetail.json'), 'w'), indent=1, default=str)
print('\nwrote p08-planningdetail.json')
