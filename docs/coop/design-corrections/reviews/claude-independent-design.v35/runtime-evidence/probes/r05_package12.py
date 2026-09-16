"""R05 — package12 on source35: artifact manifest, binding, exports equal to the package I verified
before, package11->12 member delta, residual assessment binding, 13 exact cases through BOTH boundaries
with my own decoder and the frozen35 owner, the verifier's 7 queries, and whether retained Runs reach
the changed atom branches. Root verification is compared, never adopted."""
import base64, hashlib, importlib.util, json, os, shutil, subprocess, sys

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v12'
P11 = '/tmp/opensip-design-corrections/claude-author-package-successor.v11'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v35'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v35'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verify12')
PY = '/tmp/opensip-architecture-review-env/bin/python'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN35 = os.path.join(REV, 'candidate-subject.v35.json')
ROOTV = '/tmp/opensip-design-corrections/author-package-final35-verification.v1/verification.json'
Q08 = '/tmp/opensip-design-corrections/claude-independent-design.v34/receipts/q08-package11.json'
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R['rootVerificationSha256'] = sha(ROOTV)
R['rootVerificationMatchesDeclared'] = R['rootVerificationSha256'] == '8323794cb147d1a804a9f2161dc8b1e1cd6ae10c7cf12f817d92ea8f2bc9d0ee'
rv = json.load(open(ROOTV))
amp = os.path.join(PKG, 'artifact-manifest.json')
R['artifactManifestSha256'] = sha(amp)
R['matchesDeclaredManifest'] = R['artifactManifestSha256'] == 'fb35036f2fc9646b5bb5e03d460f46324ecf455af5f86d3f05bd9217b758cd32'
R['matchesRootVerifiedManifest'] = R['artifactManifestSha256'] == rv['packageManifestSha256']


def manrows(pkg):
    am = json.load(open(os.path.join(pkg, 'artifact-manifest.json')))
    return {r['path']: r['sha256'] for r in (am['files'] if isinstance(am, dict) else am)}


m12, m11 = manrows(PKG), manrows(P11)
ok = bad = miss = 0
for p, d in m12.items():
    fp = os.path.join(PKG, p)
    if not os.path.isfile(fp):
        miss += 1
    elif sha(fp) == d:
        ok += 1
    else:
        bad += 1
unlisted = [os.path.relpath(os.path.join(d, f), PKG) for d, _, fs in os.walk(PKG) for f in fs
            if os.path.relpath(os.path.join(d, f), PKG) not in m12 and f != 'artifact-manifest.json']
R.update(declaredMembers=len(m12), verified=ok, mismatched=bad, missing=miss, filesOnDiskNotInManifest=unlisted)
R['package11To12'] = {'added': sorted(p for p in m12 if p not in m11), 'removed': sorted(p for p in m11 if p not in m12),
                      'changedCommon': sorted(p for p in m12 if p in m11 and m11[p] != m12[p]),
                      'identicalCommon': sum(1 for p in m12 if p in m11 and m11[p] == m12[p])}
R['sourceManifestEqualsFrozen35'] = sha(os.path.join(PKG, 'source-manifest.json')) == sha(MAN35)
sb = json.load(open(os.path.join(PKG, 'source-binding.v35.json')))
R['sourceBinding'] = sb
R['bindingNamesFrozen35'] = sb.get('sourceManifestSha256') == sha(MAN35)
R['parentIsPackage11IVerified'] = sb.get('parentPackageManifestSha256') == '38f7ce94ee0ee9a2de9eecd36777e25b336d2ff3c231445032a8afc7df3fd871'
R['constructionAccountsIdenticalToPackage11'] = {a: m11.get(a) == m12.get(a) for a in sb.get('constructionAccounts') or []}
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
verd = {}
for it in era.get('items', []):
    verd[it.get('authorAssessment')] = verd.get(it.get('authorAssessment'), 0) + 1
dep = era.get('sharedReviewDependencies') or []
R['residualAssessment'] = {'bindsFrozen35': era.get('subjectManifestSha256') == sha(MAN35), 'rows': len(era.get('items', [])),
                           'verdicts': verd, 'grades': sorted({str(it.get('independentGrade')) for it in era.get('items', [])}),
                           'tcbDependents': len(dep[0]['dependentResidualIds']) if dep else None,
                           'evidenceResolveAgainst': sorted({e.get('resolveAgainst') for it in era.get('items', []) for e in it.get('evidence', [])})}
print('manifest declared/root-verified: %s/%s | members %d verified %d bad %d missing %d unlisted %s' % (
    R['matchesDeclaredManifest'], R['matchesRootVerifiedManifest'], len(m12), ok, bad, miss, unlisted))
print('source-manifest=frozen35 %s | binding names 35 %s | parent=package11 %s | construction accounts identical %s' % (
    R['sourceManifestEqualsFrozen35'], R['bindingNamesFrozen35'], R['parentIsPackage11IVerified'], R['constructionAccountsIdenticalToPackage11']))
print('package11->12:', {k: (v if isinstance(v, int) else len(v)) for k, v in R['package11To12'].items()}, R['package11To12']['added'], R['package11To12']['changedCommon'])
print('residual assessment:', R['residualAssessment'])

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
spec = importlib.util.spec_from_file_location('owner35', op)
M = importlib.util.module_from_spec(spec); sys.modules['owner35'] = M; spec.loader.exec_module(M)
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
        desc = e['objectTable'][ident] if ident in e['objectTable'] else json.loads(bytes.fromhex(meta['canonicalBytesHex']), object_pairs_hook=nodup)
        if dom != 'canonical-record' and dom in M.PREFIX and ident in e['objectTable']:
            objects[ident] = (dom, desc)
    return objects, blobs


def reach(blobs):
    st = {'incomingEndpointAtoms': 0, 'incomingSearchRecords': 0, 'atoms': {}}
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('op'), str) and isinstance(o.get('relation'), str) and isinstance(o.get('minResolution'), str):
                k = '%s/%s/%s' % (o['op'], o['relation'], o.get('endpoint', 'source'))
                st['atoms'][k] = st['atoms'].get(k, 0) + 1
                if o.get('endpoint') == 'target':
                    st['incomingEndpointAtoms'] += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for b in blobs.values():
        try:
            j = json.loads(b)
        except Exception:
            continue
        walk(j)
        if isinstance(j, dict) and 'completeSearch' in j and 'scopeRefs' in j:
            st['incomingSearchRecords'] += 1
    return st


prior = {r['name']: r['exportSha256'] for r in json.load(open(Q08))['rows']}
GROUPS = [('checkpoint3', 'positive'), ('normalized-examples6', 'positive'), ('rust-selection-examples1', 'positive'),
          ('semantic-controls1', 'false-result-control'), ('binding-controls', 'binding-control')]
rows = []
for g, klass in GROUPS:
    for c in json.load(open(os.path.join(PKG, g, 'claims.json'))):
        raw = open(os.path.join(PKG, g, c['path']), 'rb').read()
        row = {'group': g, 'class': klass, 'name': c.get('name'), 'exportSha256': hashlib.sha256(raw).hexdigest(), 'claimedRunId': c['runId']}
        row['exportEqualsPackage11'] = prior.get(c.get('name')) == row['exportSha256']
        objects, blobs = decode(raw)
        dom, run = objects[c['runId']]
        try:
            rid, _ = M.open_run_closure(run, objects, blobs)
            row['structural'], row['structuralIdMatches'] = 'ADMIT', rid == c['runId']
        except Exception as ex:
            row['structural'], row['structuralReason'] = 'REFUSE', '%s: %s' % (type(ex).__name__, str(ex)[:200])
        try:
            rid2 = M.close_run(run, objects, blobs)
            row['semantic'], row['semanticIdMatches'] = 'ADMIT', rid2 == c['runId']
        except Exception as ex:
            row['semantic'], row['semanticReason'] = 'REFUSE', '%s: %s' % (type(ex).__name__, str(ex)[:200])
        row['reach'] = reach(blobs)
        rows.append(row)
        print('%-28s %-21s struct=%-6s sem=%-6s idOk=%-5s eqPkg11=%-5s %s' % (row['name'], klass, row['structural'], row['semantic'],
              row.get('semanticIdMatches', row.get('structuralIdMatches')), row['exportEqualsPackage11'], str(row.get('semanticReason', ''))[:70]), flush=True)
R['rows'] = rows
pos = [r for r in rows if r['class'] == 'positive']
neg = [r for r in rows if r['class'] == 'false-result-control']
bind = [r for r in rows if r['class'] == 'binding-control']
R['allThirteenAsExpected'] = (len(rows) == 13 and all(r['structural'] == r['semantic'] == 'ADMIT' and r.get('semanticIdMatches') for r in pos)
                              and all(r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' for r in neg)
                              and any(r['name'] == 'ts-invalid-default-entry' and r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' for r in bind)
                              and all(r['semantic'] == 'ADMIT' for r in bind if r['name'] != 'ts-invalid-default-entry'))
R['allExportsEqualPackage11'] = all(r['exportEqualsPackage11'] for r in rows)
R['retainedRunsReachIncoming'] = {'incomingEndpointAtoms': sum(r['reach']['incomingEndpointAtoms'] for r in rows),
                                  'incomingSearchRecords': sum(r['reach']['incomingSearchRecords'] for r in rows),
                                  'atomKinds': sorted({k for r in rows for k in r['reach']['atoms']})}
print('\nall 13 as expected %s | exports equal package11 %s | reach %s' % (R['allThirteenAsExpected'], R['allExportsEqualPackage11'], R['retainedRunsReachIncoming']))
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
cmd = [PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'), '--source', SRC, '--out', WORK]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
R['verifier'] = {'command': cmd, 'returncode': r.returncode, 'stdoutTail': r.stdout[-500:], 'stderrTail': (r.stderr or '')[-500:]}
vp = os.path.join(WORK, 'verification.json')
if os.path.isfile(vp):
    v = json.load(open(vp))
    R['verification'] = {k: v.get(k) for k in ('sourceManifestSha256', 'packageManifestSha256', 'sourceFilesVerified', 'packageFilesVerified', 'passed')}
    R['queryChecks'] = next((g['count'] for g in v['groups'] if g['group'] == 'query'), None)
    mine = {g['group']: (g['passed'], g['count'], g.get('reportSha256')) for g in v['groups']}
    theirs = {g['group']: (g['passed'], g['count'], g.get('reportSha256')) for g in rv['groups']}
    R['myGroupsIncludingReportDigestsMatchRoot'] = mine == theirs
    print('verify-package rc=%d passed=%s src=%s pkg=%s queries=%s groups+digests=root %s' % (
        r.returncode, v.get('passed'), v.get('sourceFilesVerified'), v.get('packageFilesVerified'), R['queryChecks'], R['myGroupsIncludingReportDigestsMatchRoot']))
qa = os.path.join(WORK, 'query-assessment.json')
if os.path.isfile(qa):
    q = json.load(open(qa))
    R['queryAssessment'] = {'passed': q.get('passed'), 'checks': [(c.get('name'), c.get('passed')) for c in q.get('checks', [])]}
R['frozen35DeviationsAfter'] = sum(1 for f in json.load(open(MAN35))['files'] if sha(os.path.join(SRC, f['path'])) != f['sha256'])
print('frozen35 drift after:', R['frozen35DeviationsAfter'])
json.dump(R, open(os.path.join(OUT, 'r05-package12.json'), 'w'), indent=1, default=str)
print('wrote r05-package12.json')
