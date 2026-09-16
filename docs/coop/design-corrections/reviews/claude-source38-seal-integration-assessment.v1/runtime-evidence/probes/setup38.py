"""Exact input copy for the source38 SEAL integration assessment. Writes only under this runtime.

usage: python -I -B setup38.py snapshot   -> inventories of read-only inputs + verified copies
       python -I -B setup38.py verify     -> re-inventory read-only inputs and compare to the snapshot
Read-only inputs: root successor source, root seal correction, root fault-check correction, root final38 reference,
own v1/v2 runtimes. Copies: work/source38-integrated (exact successor bytes) and work/source38-seal-before
(hardlinked from the integrated copy; ONLY the two root seal files are unlinked and rewritten with root before bytes).
"""
import hashlib, json, os, shutil, sys

RT = '/private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1'
SUCC = '/tmp/opensip-design-corrections/termination-exclusivity-successor.v1/source'
SEAL = '/tmp/opensip-design-corrections/root-final38-seal-correction.v1'
FAULT = '/tmp/opensip-design-corrections/root-source38-fault-check-correction.v1'
REF = '/tmp/opensip-design-corrections/root-final38-reference.v1'
V1 = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
V2 = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
READ_ONLY = {'successor': SUCC, 'sealCorrection': SEAL, 'faultCorrection': FAULT, 'final38Reference': REF, 'v1': V1, 'v2': V2}
if len(sys.argv) > 2:
    READ_ONLY = {k: READ_ONLY[k] for k in sys.argv[2].split(',')}
SUFFIX = ('.' + sys.argv[2].replace(',', '-')) if len(sys.argv) > 2 else ''
INTEGRATED = RT + '/work/source38-integrated'
SEAL_BEFORE = RT + '/work/source38-seal-before'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def inventory(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = sha(p)
    return out


def write(name, value):
    os.makedirs(RT + '/receipts', exist_ok=True)
    json.dump(value, open(RT + '/receipts/' + name, 'w'), indent=1)


mode = sys.argv[1]
if mode == 'verify':
    prior = json.load(open(RT + '/receipts/read-only-inventory.snapshot' + SUFFIX + '.json'))
    res = {}
    for k, root in READ_ONLY.items():
        now = inventory(root)
        was = prior[k]['files']
        res[k] = {'files': len(now), 'equal': now == was, 'changed': sorted(p for p in was if now.get(p) != was[p])[:20],
                  'extra': sorted(p for p in now if p not in was)[:20]}
    write('read-only-inventory.verify' + SUFFIX + '.json', res)
    print(json.dumps(res, indent=1))
    sys.exit(0 if all(v['equal'] for v in res.values()) else 1)

assert mode == 'snapshot'
snap = {k: {'root': root, 'files': inventory(root)} for k, root in READ_ONLY.items()}
write('read-only-inventory.snapshot' + SUFFIX + '.json', snap)
if 'successor' not in READ_ONLY:
    print(json.dumps({k: len(v['files']) for k, v in snap.items()}))
    sys.exit(0)
proposal = json.load(open(SEAL + '/proposal.json'))
fault = json.load(open(FAULT + '/assessment.json'))
succ = snap['successor']['files']
checks = {'sealProposal': [], 'faultCorrection': {}, 'v2SixFiles': []}
for f in proposal['files']:
    p = f['path']
    row = {'path': p, 'beforeFile': sha(SEAL + '/before/' + p) == f['beforeSha256'], 'afterFile': sha(SEAL + '/after/' + p) == f['afterSha256'],
           'successorEqualsAfter': succ.get(p) == f['afterSha256'], 'beforeSha256': f['beforeSha256'], 'afterSha256': f['afterSha256']}
    assert row['beforeFile'] and row['afterFile'] and row['successorEqualsAfter'], row
    checks['sealProposal'].append(row)
fp = fault['path']
checks['faultCorrection'] = {'path': fp, 'beforeFile': sha(FAULT + '/before.py') == fault['beforeSha256'], 'afterFile': sha(FAULT + '/after.py') == fault['afterSha256'],
                             'successorEqualsAfter': succ.get(fp) == fault['afterSha256'], 'beforeSha256': fault['beforeSha256'], 'afterSha256': fault['afterSha256']}
assert checks['faultCorrection']['beforeFile'] and checks['faultCorrection']['afterFile'] and checks['faultCorrection']['successorEqualsAfter']
for f in json.load(open(V2 + '/receipts/edit-hashes.json'))['files']:
    row = {'path': f['path'], 'v2AfterSha256': f['afterSha256'], 'successorEqualsV2After': succ.get(f['path']) == f['afterSha256']}
    assert row['successorEqualsV2After'], row
    checks['v2SixFiles'].append(row)
# Production fault law files unchanged from the verified source37 input overlay used in v2.
v2p = V2 + '/work/source37-pristine/'
for p in ('docs/coop/design-corrections/foundation/evaluator_fault_model.v3.py',
          'docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json',
          'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
          'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json',
          'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'):
    checks.setdefault('faultLawVersusSource37Overlay', []).append({'path': p, 'successorSha256': succ.get(p), 'source37OverlaySha256': sha(v2p + p),
                                                                 'equal': succ.get(p) == sha(v2p + p)})
for label in (INTEGRATED, SEAL_BEFORE):
    if os.path.exists(label):
        sys.exit('refusing to reuse ' + label)
for p in succ:
    d = os.path.join(INTEGRATED, p)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(os.path.join(SUCC, p), d)
integ = inventory(INTEGRATED)
checks['integratedCopy'] = {'files': len(integ), 'equalsSuccessor': integ == succ}
assert checks['integratedCopy']['equalsSuccessor']
for p in succ:
    d = os.path.join(SEAL_BEFORE, p)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    os.link(os.path.join(INTEGRATED, p), d)
for f in proposal['files']:
    d = os.path.join(SEAL_BEFORE, f['path'])
    os.unlink(d)
    shutil.copyfile(SEAL + '/before/' + f['path'], d)
before_inv = inventory(SEAL_BEFORE)
checks['sealBeforeVariant'] = {'files': len(before_inv), 'differsFromSuccessor': sorted(p for p in succ if before_inv.get(p) != succ[p]),
                               'integratedStillEqualsSuccessor': inventory(INTEGRATED) == succ}
assert checks['sealBeforeVariant']['differsFromSuccessor'] == sorted(f['path'] for f in proposal['files'])
assert checks['sealBeforeVariant']['integratedStillEqualsSuccessor']
checks['readOnlyInventoryCounts'] = {k: len(v['files']) for k, v in snap.items()}
write('setup38.json', checks)
print(json.dumps(checks, indent=1))
