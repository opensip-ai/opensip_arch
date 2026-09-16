"""Q08 — package11 on source34. Verify the artifact manifest, the source binding and the claim that
its exports are the exact package10 bytes; replay all 13 exact Run/control cases through BOTH
open_run_closure and close_run with my own decoder and the frozen34 owner; run the package verifier
for the 7 queries; and measure whether any retained Run even reaches the changed atom branches.
Root's verification is evidence to compare, never authority."""
import base64, hashlib, importlib.util, json, os, shutil, subprocess, sys

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v11'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v34'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verify11')
PY = '/tmp/opensip-architecture-review-env/bin/python'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN34 = os.path.join(REV, 'candidate-subject.v34.json')
ROOTV = os.path.join(REV, 'author-package-final34-verification.v1/verification.json')
P12 = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts/p12-package10.json'
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


rv = json.load(open(ROOTV))
amp = os.path.join(PKG, 'artifact-manifest.json')
R['artifactManifestSha256'] = sha(amp)
R['matchesRootVerifiedPackageManifest'] = R['artifactManifestSha256'] == rv['packageManifestSha256']
am = json.load(open(amp))
rows = am['files'] if isinstance(am, dict) else am
ok = bad = miss = 0
badl = []
for r in rows:
    p = os.path.join(PKG, r['path'])
    if not os.path.isfile(p):
        miss += 1; badl.append(('MISSING', r['path']))
    elif sha(p) == r['sha256']:
        ok += 1
    else:
        bad += 1; badl.append(('MISMATCH', r['path']))
listed = {r['path'] for r in rows}
unlisted = []
for d, _, fs in os.walk(PKG):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), PKG)
        if rel not in listed and rel != 'artifact-manifest.json':
            unlisted.append(rel)
R.update(declaredMembers=len(rows), verified=ok, mismatched=bad, missing=miss, badList=badl[:10],
         filesOnDiskNotInManifest=unlisted)
print('artifact manifest sha %s… matches root-verified package manifest: %s' % (R['artifactManifestSha256'][:12], R['matchesRootVerifiedPackageManifest']))
print('members %d verified %d mismatched %d missing %d | on disk but unlisted: %s' % (len(rows), ok, bad, miss, unlisted))

R['sourceManifestEqualsFrozen34'] = sha(os.path.join(PKG, 'source-manifest.json')) == sha(MAN34)
sb = json.load(open(os.path.join(PKG, 'source-binding.v34.json')))
R['sourceBinding'] = sb
R['sourceBindingNamesFrozen34'] = sb.get('sourceManifestSha256') == sha(MAN34)
R['parentIsMyVerifiedPackage10'] = sb.get('parentPackageManifestSha256') == '88c38b160e8b3af2702c0975271e10a765cd551b7245e8ac6f963887ef3551d2'
print('source-manifest byte-equal frozen34: %s | binding names frozen34: %s | parent = package10 I verified: %s'
      % (R['sourceManifestEqualsFrozen34'], R['sourceBindingNamesFrozen34'], R['parentIsMyVerifiedPackage10']))
for acct in sb.get('constructionAccounts') or []:
    p = os.path.join(PKG, acct)
    if os.path.isfile(p):
        d = json.load(open(p))
        R.setdefault('constructionAccounts', {})[acct] = {
            'sha256': sha(p), 'inManifest': acct in listed,
            'standing': str(d.get('standing'))[:400],
            'keys': list(d)[:20]}
        print('construction account %-24s inManifest=%s standing=%s' % (acct, acct in listed, str(d.get('standing'))[:150]))

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner34', op)
M = importlib.util.module_from_spec(spec)
sys.modules['owner34'] = M
spec.loader.exec_module(M)
R['ownerSha256'] = sha(op)
R['ownerEqualsFrozen34Row'] = R['ownerSha256'] == {f['path']: f['sha256'] for f in json.load(open(MAN34))['files']}['docs/coop/design-corrections/foundation/identity-model.v3.py']


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
    objects, alldesc = {}, []
    for dg, meta in e['frames'].items():
        dom, ident = meta['domain'], meta['identity']
        cx = bytes.fromhex(meta['canonicalBytesHex'])
        desc = e['objectTable'][ident] if ident in e['objectTable'] else json.loads(cx, object_pairs_hook=nodup)
        alldesc.append((dom, desc))
        if dom != 'canonical-record' and dom in M.PREFIX and ident in e['objectTable']:
            objects[ident] = (dom, desc)
    return e, objects, blobs, alldesc


def atom_reach(alldesc, blobs):
    """Does this retained Run even reach the changed atom branches?"""
    st = {'atoms': {}, 'coverageByRelation': {}, 'incomingSearchRecords': 0, 'scopeRecords': 0}

    def walk(o):
        if isinstance(o, dict):
            if 'op' in o and 'relation' in o and 'minResolution' in o:
                k = '%s/%s/%s' % (o['op'], o['relation'], o.get('endpoint', 'source'))
                st['atoms'][k] = st['atoms'].get(k, 0) + 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for dom, desc in alldesc:
        walk(desc)
    for b in blobs.values():
        try:
            j = json.loads(b)
        except Exception:
            continue
        if isinstance(j, dict):
            walk(j)
            if 'completeSearch' in j and 'scopeRefs' in j:
                st['incomingSearchRecords'] += 1
            key = j.get('key') if isinstance(j.get('key'), dict) else None
            if key and 'sourceUniverse' in key and 'relation' in key and 'entry' in j:
                k = '%s|%s|%s' % (key['relation'], key['sourceUniverse'][:8], str(key.get('targetUniverse'))[:8])
                st['coverageByRelation'][k] = st['coverageByRelation'].get(k, 0) + 1
            if j.get('schemaVersion') == 2 and 'subjects' in j and 'relation' in j:
                st['scopeRecords'] += 1
    st['anySameKeyMultiPartition'] = any(v > 1 for v in st['coverageByRelation'].values())
    st['reachesDependencyRelations'] = any(a.split('/')[1] in ('reachability', 'clones') for a in st['atoms'])
    st['reachesIncomingEndpoint'] = any(a.endswith('/target') for a in st['atoms'])
    return st


p10 = {r['name']: r['exportSha256'] for r in json.load(open(P12))['rows']}
GROUPS = [('checkpoint3', 'positive'), ('normalized-examples6', 'positive'),
          ('rust-selection-examples1', 'positive'), ('semantic-controls1', 'false-result-control'),
          ('binding-controls', 'binding-control')]
out = []
for g, klass in GROUPS:
    d = os.path.join(PKG, g)
    for c in json.load(open(os.path.join(d, 'claims.json'))):
        raw = open(os.path.join(d, c['path']), 'rb').read()
        row = {'group': g, 'class': klass, 'name': c.get('name'), 'exportSha256': hashlib.sha256(raw).hexdigest(),
               'claimedRunId': c['runId']}
        row['exportEqualsPackage10'] = p10.get(c.get('name')) == row['exportSha256']
        e, objects, blobs, alldesc = decode(raw)
        dom, run = objects[c['runId']]
        try:
            rid, _ = M.open_run_closure(run, objects, blobs)
            row['structural'], row['structuralIdMatches'] = 'ADMIT', rid == c['runId']
        except Exception as ex:
            row['structural'], row['structuralReason'] = 'REFUSE', '%s: %s' % (type(ex).__name__, ex)
        try:
            rid2 = M.close_run(run, objects, blobs)
            row['semantic'], row['semanticIdMatches'] = 'ADMIT', rid2 == c['runId']
        except Exception as ex:
            row['semantic'], row['semanticReason'] = 'REFUSE', '%s: %s' % (type(ex).__name__, str(ex)[:300])
        row['atomReach'] = atom_reach(alldesc, blobs)
        out.append(row)
        print('%-28s %-21s struct=%-6s sem=%-6s idOk=%-5s eqPkg10=%-5s atoms=%s multiPart=%s %s'
              % (row['name'], klass, row['structural'], row['semantic'],
                 row.get('semanticIdMatches', row.get('structuralIdMatches')), row['exportEqualsPackage10'],
                 sorted(row['atomReach']['atoms'])[:4], row['atomReach']['anySameKeyMultiPartition'],
                 str(row.get('semanticReason', ''))[:60]), flush=True)
R['rows'] = out
pos = [r for r in out if r['class'] == 'positive']
neg = [r for r in out if r['class'] == 'false-result-control']
bind = [r for r in out if r['class'] == 'binding-control']
R['counts'] = {'positives': len(pos), 'negatives': len(neg), 'bindingControls': len(bind), 'total': len(out)}
R['positivesAdmitBoth'] = all(r['structural'] == 'ADMIT' and r['semantic'] == 'ADMIT' and r.get('semanticIdMatches') for r in pos)
R['negativesAdmitThenRefuse'] = all(r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' for r in neg)
R['bindingInvalidRefused'] = any(r['name'] == 'ts-invalid-default-entry' and r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' for r in bind)
R['bindingLawfulAdmitted'] = all(r['semantic'] == 'ADMIT' for r in bind if r['name'] != 'ts-invalid-default-entry')
R['allThirteenAsExpected'] = len(out) == 13 and R['positivesAdmitBoth'] and R['negativesAdmitThenRefuse'] and R['bindingInvalidRefused'] and R['bindingLawfulAdmitted']
R['allExportsEqualPackage10'] = all(r['exportEqualsPackage10'] for r in out)
R['anyRunReachesChangedAtomBranches'] = {
    'dependencyRelationAtoms': any(r['atomReach']['reachesDependencyRelations'] for r in out),
    'incomingEndpointAtoms': any(r['atomReach']['reachesIncomingEndpoint'] for r in out),
    'sameKeyMultiPartitionCoverage': any(r['atomReach']['anySameKeyMultiPartition'] for r in out),
    'incomingSearchRecords': sum(r['atomReach']['incomingSearchRecords'] for r in out)}
print('\ncounts %s | all 13 as expected: %s | all exports equal package10 bytes: %s'
      % (R['counts'], R['allThirteenAsExpected'], R['allExportsEqualPackage10']))
print('retained Runs reaching the changed atom branches:', R['anyRunReachesChangedAtomBranches'])

if os.path.isdir(WORK):
    shutil.rmtree(WORK)
r = subprocess.run([PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'), '--source', SRC, '--out', WORK],
                   capture_output=True, text=True, timeout=5400)
R['verifier'] = {'command': [PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'), '--source', SRC, '--out', WORK],
                 'returncode': r.returncode, 'stdoutTail': r.stdout[-600:], 'stderrTail': (r.stderr or '')[-600:]}
vp = os.path.join(WORK, 'verification.json')
if os.path.isfile(vp):
    v = json.load(open(vp))
    R['verification'] = v
    R['queryChecks'] = next((g['count'] for g in v['groups'] if g['group'] == 'query'), None)
    mine = {g['group']: (g['passed'], g['count'], g.get('reportSha256')) for g in v['groups']}
    root_g = {g['group']: (g['passed'], g['count'], g.get('reportSha256')) for g in rv['groups']}
    R['myGroupsIncludingReportDigestsMatchRoot'] = mine == root_g
    R['verifierPassed'] = v.get('passed')
    print('verify-package rc=%d passed=%s sourceFiles=%s packageFiles=%s queries=%s | groups+report digests equal root: %s'
          % (r.returncode, v.get('passed'), v.get('sourceFilesVerified'), v.get('packageFilesVerified'),
             R['queryChecks'], R['myGroupsIncludingReportDigestsMatchRoot']))
qa = os.path.join(WORK, 'query-assessment.json')
if os.path.isfile(qa):
    q = json.load(open(qa))
    R['queryAssessment'] = {'passed': q.get('passed'), 'checks': [(c.get('name'), c.get('passed')) for c in q.get('checks', [])]}
    print('query assessment:', R['queryAssessment'])
dev = sum(1 for f in json.load(open(MAN34))['files']
          if sha(os.path.join(SRC, f['path'])) != f['sha256'])
R['frozen34DeviationsAfter'] = dev
print('frozen34 deviations after:', dev)
json.dump(R, open(os.path.join(OUT, 'q08-package11.json'), 'w'), indent=1, default=str)
print('wrote q08-package11.json')
