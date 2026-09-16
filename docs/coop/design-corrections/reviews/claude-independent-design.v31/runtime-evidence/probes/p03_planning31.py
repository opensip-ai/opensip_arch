"""PROBE 03 (v31) — planning layer bindings and the planning decisions reviewed in 26/27.

Verifies every layer-2 pin against frozen31, establishes the layer-1/layer-2 relationship, and
re-measures the planning decisions (filename/dir/crate/module plan, report boundaries, M0-M6,
198 paths / 20 groups / 320 coverage mappings / 54 recovery cases) against ACTUAL 31 counts.
This corrects the stale DR-204 basis (12892 files / v26 layer 1) in my v27 record.
"""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {'frozen31FileCount': len(man),
     'frozen31TotalBytes': sum(f['bytes'] for f in man.values())}
print('frozen31: %d files, %d bytes' % (R['frozen31FileCount'], R['frozen31TotalBytes']))

# ---- layer 2 ----
L2 = os.path.join(A, 'implementation-normative-inputs.v2.json')
l2 = json.load(open(L2))
R['layer2Path'] = 'docs/v2/architecture/implementation-normative-inputs.v2.json'
R['layer2Sha256'] = hashlib.sha256(open(L2, 'rb').read()).hexdigest()
R['layer2PinCount'] = len(l2['files'])
R['layer2Standing'] = l2['standing']
bad = []
for f in l2['files']:
    rec = man.get(f['path'])
    if rec is None:
        bad.append((f['path'], 'NOT-IN-FROZEN31'))
    elif rec['sha256'] != f['sha256'] or rec['bytes'] != f['bytes']:
        bad.append((f['path'], 'PIN-MISMATCH frozen=%s pinned=%s' % (rec['sha256'][:12], f['sha256'][:12])))
R['layer2PinsUnresolvedOrStale'] = bad
R['layer2AllPinsResolveAgainstFrozen31'] = not bad
print('layer2: %d pins, all resolve against frozen31: %s' % (len(l2['files']), not bad))
for b in bad:
    print('   STALE/UNRESOLVED:', b)
R['layer2ChangedIn27to31'] = R['layer2Path'] in [c['path'] for c in json.load(
    open(os.path.join(OUT, 'p01-delta.json')))['cumulative']['changed']]

# ---- layer 1 and the previousArchitectureInputLayer relationship ----
L1 = os.path.join(A, 'implementation-planning-sources.v1.json')
l1 = json.load(open(L1))
R['layer1Sha256'] = hashlib.sha256(open(L1, 'rb').read()).hexdigest()
R['layer1TopKeys'] = sorted(l1) if isinstance(l1, dict) else '<list>'
prev = l1.get('previousArchitectureInputLayer')
R['previousArchitectureInputLayerPresent'] = prev is not None
if prev:
    R['previousArchitectureInputLayer'] = prev if not isinstance(prev, dict) else {
        k: (str(v)[:120]) for k, v in prev.items()}
    print('\npreviousArchitectureInputLayer:', json.dumps(R['previousArchitectureInputLayer'])[:600])
# does layer1 name the ORIGINAL source25 layer, preserved?
s = json.dumps(l1)
R['layer1MentionsNormativeInputsV1'] = 'implementation-normative-inputs.v1.json' in s
R['layer1MentionsNormativeInputsV2'] = 'implementation-normative-inputs.v2.json' in s
v1p = 'docs/v2/architecture/implementation-normative-inputs.v1.json'
R['normativeInputsV1StillInFrozen31'] = v1p in man
print('layer1 names v1 / v2 :', R['layer1MentionsNormativeInputsV1'], R['layer1MentionsNormativeInputsV2'])
print('original v1 layer preserved in frozen31 :', R['normativeInputsV1StillInFrozen31'])

# ---- planning decisions reviewed in 26/27 ----
def count_records(path, keys):
    p = os.path.join(SRC, path)
    if not os.path.isfile(p):
        return {'present': False}
    d = json.load(open(p))
    out = {'present': True,
           'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest(),
           'bytes': os.path.getsize(p),
           'changedIn27to31': path in [c['path'] for c in json.load(
               open(os.path.join(OUT, 'p01-delta.json')))['cumulative']['changed']]}
    for k in keys:
        cur = d
        try:
            for part in k.split('.'):
                cur = cur[part]
            out[k] = len(cur) if isinstance(cur, (list, dict)) else cur
        except Exception:
            pass
    out['topKeys'] = sorted(d) if isinstance(d, dict) else '<list>'
    return out


R['repositoryFileInventory'] = count_records(
    'docs/v2/architecture/repository-file-inventory.v1.json', ['files', 'groups', 'paths', 'entries'])
R['implementationCoverage'] = count_records(
    'docs/v2/architecture/implementation-coverage.v1.json', ['mappings', 'coverage', 'rows', 'items'])
R['commitRecoveryPlan'] = count_records(
    'docs/v2/architecture/commit-recovery-plan.v1.json', ['cases', 'items', 'rows'])
for k in ('repositoryFileInventory', 'implementationCoverage', 'commitRecoveryPlan'):
    print('\n%s:' % k, json.dumps(R[k])[:400])

json.dump(R, open(os.path.join(OUT, 'p03-planning31.json'), 'w'), indent=1)
print('\nwrote p03-planning31.json')
