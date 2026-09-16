"""Probe 04 — verify the new planning layer 2: that `architecture` is rebound to
implementation-normative-inputs.v2.json and every pin matches the CURRENT frozen 27 bytes,
that `previousArchitectureInputLayer` preserves the v1 layer exactly, and that
originalArchitectureSource25 provenance is untouched."""
import hashlib, json, os

R = '/tmp/opensip-design-corrections/candidate-subject.v27'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
m27 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v27.json')))['files']}
m26 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v26.json')))['files']}
R26 = '/tmp/opensip-design-corrections/candidate-subject.v26'

s = json.load(open(os.path.join(R, 'docs/v2/architecture/implementation-planning-sources.v1.json')))
res = {'standing': s['standing']}


def check_layer(name, blk, against, label):
    rows = blk['files']
    ok = bad = absent = 0
    detail = []
    for r in rows:
        p = r['path']
        if p not in against:
            absent += 1
            detail.append({'path': p, 'issue': 'not-in-' + label})
            continue
        if against[p]['sha256'] == r['sha256'] and against[p]['bytes'] == r['bytes']:
            ok += 1
        else:
            bad += 1
            detail.append({'path': p, 'pinned': r['sha256'][:16], label: against[p]['sha256'][:16]})
    return {'subject': blk.get('subject'), 'manifestPath': blk.get('manifestPath'),
            'manifestSha256': blk.get('manifestSha256'), 'rows': len(rows),
            'matching': ok, 'mismatched': bad, 'absent': absent, 'detail': detail[:12]}


res['architecture_vs_frozen27'] = check_layer('architecture', s['architecture'], m27, 'frozen27')
res['previousLayer_vs_frozen26'] = check_layer('previous', s['previousArchitectureInputLayer'], m26, 'frozen26')
res['source25_vs_frozen27'] = check_layer('src25', s['originalArchitectureSource25'], m27, 'frozen27')
res['source25_vs_frozen26'] = check_layer('src25', s['originalArchitectureSource25'], m26, 'frozen26')

# the named current manifest must exist in 27 and hash to the declared value
mp = s['architecture']['manifestPath']
fp = os.path.join(R, mp)
res['architectureManifestPresentInSubject'] = os.path.isfile(fp)
if os.path.isfile(fp):
    h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
    res['architectureManifestActualSha256'] = h
    res['architectureManifestMatchesDeclared'] = h == s['architecture']['manifestSha256']

# previous layer must name the v1 manifest, which must still exist unchanged in 27
pp = s['previousArchitectureInputLayer']['manifestPath']
pfp = os.path.join(R, pp)
res['previousManifestPath'] = pp
res['previousManifestPresentInSubject'] = os.path.isfile(pfp)
if os.path.isfile(pfp):
    h = hashlib.sha256(open(pfp, 'rb').read()).hexdigest()
    res['previousManifestActualSha256'] = h
    res['previousManifestMatchesDeclared'] = h == s['previousArchitectureInputLayer']['manifestSha256']
    res['previousManifestUnchangedFrom26'] = (pp in m26 and m26[pp]['sha256'] == h)

# v1 vs v2 normative-inputs content delta
v1 = json.load(open(os.path.join(R, 'docs/v2/architecture/implementation-normative-inputs.v1.json')))
v2 = json.load(open(os.path.join(R, 'docs/v2/architecture/implementation-normative-inputs.v2.json')))
a = {r['path']: r for r in v1['files']}
b = {r['path']: r for r in v2['files']}
res['normativeInputs_v1_rows'] = len(a)
res['normativeInputs_v2_rows'] = len(b)
res['normativeInputs_added'] = sorted(set(b) - set(a))
res['normativeInputs_removed'] = sorted(set(a) - set(b))
res['normativeInputs_changed'] = sorted(p for p in set(a) & set(b) if a[p]['sha256'] != b[p]['sha256'])
res['normativeInputs_v2_allMatchFrozen27'] = all(
    p in m27 and m27[p]['sha256'] == r['sha256'] and m27[p]['bytes'] == r['bytes'] for p, r in b.items())
res['normativeInputs_v1_allMatchFrozen26'] = all(
    p in m26 and m26[p]['sha256'] == r['sha256'] for p, r in a.items())
res['v2_standing'] = v2.get('standing')

json.dump(res, open(os.path.join(OUT, 'p04-planning-layer2.json'), 'w'), indent=1)
print(json.dumps(res, indent=1)[:4800])
