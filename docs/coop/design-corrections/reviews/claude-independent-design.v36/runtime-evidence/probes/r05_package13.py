"""R05 — package13 on FROZEN source36: artifact manifest, every member hash (custody hashing only; consumer-custody
members are hashed, never parsed), binding and construction provenance, exports equal to the package12 exports I
verified on source35, residual assessment binding, 13 exact cases through BOTH open_run_closure and close_run with my own
decoder and the frozen36 identity owner, the verifier's 7 queries on frozen36, and whether retained Runs reach the
changed dependency/history/runtime branches. Root verification is compared, never adopted."""
import base64, hashlib, importlib.util, json, os, shutil, subprocess, sys

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/verify13')
PY = '/tmp/opensip-architecture-review-env/bin/python'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
MAN36 = os.path.join(REV, 'candidate-subject.v36.json')
MAN35 = os.path.join(REV, 'candidate-subject.v35.json')
ROOTV = '/tmp/opensip-design-corrections/author-package-final36-verification.v1/verification.json'
R05_35 = '/tmp/opensip-design-corrections/claude-independent-design.v35/receipts/r05-package12.json'
LIVE_BINDING = os.path.join(REV, 'claude-author-package-successor.v13/source-binding.v36.json')
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R['rootVerificationSha256'] = sha(ROOTV)
R['rootVerificationMatchesDeclared'] = R['rootVerificationSha256'] == 'f3842836c45c7318fb76e43f8617f0b225dcf50e29c5da656d7c8d94faa21836'
rv = json.load(open(ROOTV))
amp = os.path.join(PKG, 'artifact-manifest.json')
R['artifactManifestSha256'] = sha(amp)
R['matchesDeclaredManifest'] = R['artifactManifestSha256'] == '47dbe7818672704c017a07780b71624166dd8778f85c25c92727a93415902dc1'
R['matchesRootVerifiedManifest'] = R['artifactManifestSha256'] == rv['packageManifestSha256']


def manrows(path):
    am = json.load(open(path))
    return {r['path']: r['sha256'] for r in (am['files'] if isinstance(am, dict) else am)}


m13 = manrows(amp)
pred = os.path.join(PKG, 'predecessor-artifact-manifest.json')
R['predecessorManifestSha256'] = sha(pred) if os.path.isfile(pred) else None
R['predecessorIsPackage12IVerified'] = R['predecessorManifestSha256'] == 'fb35036f2fc9646b5bb5e03d460f46324ecf455af5f86d3f05bd9217b758cd32'
m12 = manrows(pred) if os.path.isfile(pred) else {}
ok = bad = miss = 0
badl = []
for p, d in m13.items():
    fp = os.path.join(PKG, p)
    if not os.path.isfile(fp):
        miss += 1; badl.append(p)
    elif sha(fp) == d:
        ok += 1
    else:
        bad += 1; badl.append(p)
unlisted = sorted(os.path.relpath(os.path.join(d, f), PKG) for d, _, fs in os.walk(PKG) for f in fs
                  if os.path.relpath(os.path.join(d, f), PKG) not in m13 and f != 'artifact-manifest.json')
R.update(declaredMembers=len(m13), verified=ok, mismatched=bad, missing=miss, badList=badl[:10], filesOnDiskNotInManifest=unlisted)
R['package12To13'] = {'added': sorted(p for p in m13 if p not in m12), 'removed': sorted(p for p in m12 if p not in m13),
                      'changedCommon': sorted(p for p in m13 if p in m12 and m12[p] != m13[p]),
                      'identicalCommon': sum(1 for p in m13 if p in m12 and m12[p] == m13[p])}
R['sourceManifestEqualsFrozen36'] = sha(os.path.join(PKG, 'source-manifest.json')) == sha(MAN36)
sb = json.load(open(os.path.join(PKG, 'source-binding.v36.json')))
R['sourceBinding'] = sb
R['liveBindingCopyEqual'] = sha(os.path.join(PKG, 'source-binding.v36.json')) == sha(LIVE_BINDING)
R['bindingNamesFrozen36'] = sb.get('sourceManifestSha256') == sha(MAN36)
R['bindingParentIsPackage12'] = sb.get('parentPackageManifestSha256') == 'fb35036f2fc9646b5bb5e03d460f46324ecf455af5f86d3f05bd9217b758cd32'
R['constructionAccountsIdenticalToPackage12'] = {a: (a in m13 and m12.get(a) == m13.get(a)) for a in sb.get('constructionAccounts') or []}
R['constructionProvenance'] = {'constructionSourceVersion': sb.get('constructionSourceVersion'), 'exportsChanged': sb.get('exportsChanged'),
                               'currentVerificationSourceVersion': sb.get('currentVerificationSourceVersion'),
                               'mixed33TS30NormalizedRust': sb.get('constructionSourceVersion') == {'typescriptDerivedGroups': 33, 'normalizedAndRustGroups': 30}}
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
verd = {}
for it in era.get('items', []):
    verd[it.get('authorAssessment')] = verd.get(it.get('authorAssessment'), 0) + 1
dep = era.get('sharedReviewDependencies') or []
R['residualAssessment'] = {'bindsFrozen36': era.get('subjectManifestSha256') == sha(MAN36), 'subjectManifestSha256': era.get('subjectManifestSha256'),
                           'rows': len(era.get('items', [])), 'verdicts': verd, 'grades': sorted({str(it.get('independentGrade')) for it in era.get('items', [])}),
                           'tcbDependents': len(dep[0]['dependentResidualIds']) if dep else None, 'tcbIds': [d.get('id') for d in dep],
                           'evidenceResolveAgainst': sorted({e.get('resolveAgainst') for it in era.get('items', []) for e in it.get('evidence', [])})}
print('manifest declared/root-verified: %s/%s | members %d verified %d bad %d missing %d unlisted %s' % (
    R['matchesDeclaredManifest'], R['matchesRootVerifiedManifest'], len(m13), ok, bad, miss, unlisted))
print('predecessor=package12 %s | source-manifest=frozen36 %s | binding names 36 %s parent=12 %s live copy equal %s | construction accounts identical %s' % (
    R['predecessorIsPackage12IVerified'], R['sourceManifestEqualsFrozen36'], R['bindingNamesFrozen36'], R['bindingParentIsPackage12'],
    R['liveBindingCopyEqual'], R['constructionAccountsIdenticalToPackage12']))
print('construction provenance:', R['constructionProvenance'])
print('package12->13:', {k: (v if isinstance(v, int) else len(v)) for k, v in R['package12To13'].items()}, R['package12To13']['added'], R['package12To13']['changedCommon'], R['package12To13']['removed'])
print('residual assessment:', R['residualAssessment'])

op = os.path.join(SRC, 'docs/coop/design-corrections/foundation/identity-model.v3.py')
R['ownerSha256'] = sha(op)
m36rows = {f['path']: f['sha256'] for f in json.load(open(MAN36))['files']}
m35rows = {f['path']: f['sha256'] for f in json.load(open(MAN35))['files']}
R['ownerEqualsFrozen36AndUnchangedFrom35'] = R['ownerSha256'] == m36rows['docs/coop/design-corrections/foundation/identity-model.v3.py'] == m35rows['docs/coop/design-corrections/foundation/identity-model.v3.py']
spec = importlib.util.spec_from_file_location('owner36', op)
M = importlib.util.module_from_spec(spec); sys.modules['owner36'] = M; spec.loader.exec_module(M)


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
    st = {'incomingEndpointAtoms': 0, 'incomingSearchRecords': 0, 'atoms': {}, 'historyOrRuntimeImports': 0}
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('op'), str) and isinstance(o.get('relation'), str) and isinstance(o.get('minResolution'), str):
                k = '%s/%s/%s' % (o['op'], o['relation'], o.get('endpoint', 'source'))
                st['atoms'][k] = st['atoms'].get(k, 0) + 1
                if o.get('endpoint') == 'target':
                    st['incomingEndpointAtoms'] += 1
            if o.get('evidenceKind') in ('runtime', 'history') or o.get('kind') in ('runtime', 'history') and 'importId' in o:
                st['historyOrRuntimeImports'] += 1
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


prior = {r['name']: r['exportSha256'] for r in json.load(open(R05_35))['rows']}
R['priorReceiptSha256'] = sha(R05_35)
GROUPS = [('checkpoint3', 'positive'), ('normalized-examples6', 'positive'), ('rust-selection-examples1', 'positive'),
          ('semantic-controls1', 'false-result-control'), ('binding-controls', 'binding-control')]
rows = []
for g, klass in GROUPS:
    for c in json.load(open(os.path.join(PKG, g, 'claims.json'))):
        raw = open(os.path.join(PKG, g, c['path']), 'rb').read()
        row = {'group': g, 'class': klass, 'name': c.get('name'), 'exportSha256': hashlib.sha256(raw).hexdigest(), 'claimedRunId': c['runId']}
        row['exportEqualsPackage12'] = prior.get(c.get('name')) == row['exportSha256']
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
        print('%-28s %-21s struct=%-6s sem=%-6s idOk=%-5s eqPkg12=%-5s %s' % (row['name'], klass, row['structural'], row['semantic'],
              row.get('semanticIdMatches', row.get('structuralIdMatches')), row['exportEqualsPackage12'], str(row.get('semanticReason', ''))[:80]), flush=True)
R['rows'] = rows
pos = [r for r in rows if r['class'] == 'positive']
neg = [r for r in rows if r['class'] == 'false-result-control']
bind = [r for r in rows if r['class'] == 'binding-control']
R['allThirteenAsExpected'] = (len(rows) == 13 and all(r['structural'] == r['semantic'] == 'ADMIT' and r.get('semanticIdMatches') and r.get('structuralIdMatches') for r in pos)
                              and all(r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE' and 'EVALUATOR_COMPLETE_PROOF_REPLAY' in r.get('semanticReason', '') for r in neg)
                              and any(r['name'] == 'ts-invalid-default-entry' and r['structural'] == 'ADMIT' and r['semantic'] == 'REFUSE'
                                      and 'ENUMERATION_BINDING_PROGRAM_ENTRY' in r.get('semanticReason', '') for r in bind)
                              and all(r['structural'] == r['semantic'] == 'ADMIT' for r in bind if r['name'] != 'ts-invalid-default-entry'))
R['allExportsEqualPackage12'] = all(r['exportEqualsPackage12'] for r in rows)
R['retainedRunsReach'] = {'incomingEndpointAtoms': sum(r['reach']['incomingEndpointAtoms'] for r in rows),
                          'incomingSearchRecords': sum(r['reach']['incomingSearchRecords'] for r in rows),
                          'atomKinds': sorted({k for r in rows for k in r['reach']['atoms']}),
                          'reachabilityOrClonesAllCoveredAtoms': sorted({k for r in rows for k in r['reach']['atoms'] if k.split('/')[1] in ('reachability', 'clones') and k.split('/')[0] in ('all-covered', 'count-at-most', 'none')}),
                          'historyOrRuntimeImportMarkers': sum(r['reach']['historyOrRuntimeImports'] for r in rows)}
print('\nall 13 as expected %s | exports equal package12 %s | reach %s' % (R['allThirteenAsExpected'], R['allExportsEqualPackage12'], R['retainedRunsReach']))
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
cmd = [PY, '-I', '-B', os.path.join(PKG, 'verify-package.py'), '--source', SRC, '--out', WORK]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
open(os.path.join(OUT, 'r05-verify-package.stdout'), 'w').write(r.stdout)
open(os.path.join(OUT, 'r05-verify-package.stderr'), 'w').write(r.stderr or '')
R['verifier'] = {'command': cmd, 'returncode': r.returncode, 'stdoutSha256': hashlib.sha256(r.stdout.encode()).hexdigest(),
                 'stdoutTail': r.stdout[-500:], 'stderrTail': (r.stderr or '')[-500:]}
vp = os.path.join(WORK, 'verification.json')
if os.path.isfile(vp):
    v = json.load(open(vp))
    R['verification'] = {k: v.get(k) for k in ('sourceManifestSha256', 'packageManifestSha256', 'sourceFilesVerified', 'packageFilesVerified', 'passed')}
    R['verificationGroups'] = [{k: g.get(k) for k in ('group', 'passed', 'count', 'reportSha256', 'exitCode', 'observed')} for g in v['groups']]
    R['queryChecks'] = next((g['count'] for g in v['groups'] if g['group'] == 'query'), None)
    mine = {g['group']: (g['passed'], g['count'], g.get('reportSha256'), json.dumps(g.get('observed'), sort_keys=True)) for g in v['groups']}
    theirs = {g['group']: (g['passed'], g['count'], g.get('reportSha256'), json.dumps(g.get('observed'), sort_keys=True)) for g in rv['groups']}
    R['myGroupsObservedAndReportDigestsMatchRoot'] = mine == theirs
    R['myVerificationJsonEqualsRootBytes'] = sha(vp) == R['rootVerificationSha256']
    print('verify-package rc=%d passed=%s src=%s pkg=%s queries=%s groups+observed+digests=root %s | bytes equal root %s' % (
        r.returncode, v.get('passed'), v.get('sourceFilesVerified'), v.get('packageFilesVerified'), R['queryChecks'],
        R['myGroupsObservedAndReportDigestsMatchRoot'], R['myVerificationJsonEqualsRootBytes']))
qa = os.path.join(WORK, 'query-assessment.json')
if os.path.isfile(qa):
    q = json.load(open(qa))
    R['queryAssessment'] = {'passed': q.get('passed'), 'checks': [(c.get('name'), c.get('passed')) for c in q.get('checks', [])]}
    print('query assessment:', R['queryAssessment'])
R['frozen36DeviationsAfter'] = sum(1 for f in json.load(open(MAN36))['files'] if sha(os.path.join(SRC, f['path'])) != f['sha256'])
R['packageDeviationsAfter'] = sum(1 for p, d in m13.items() if not os.path.isfile(os.path.join(PKG, p)) or sha(os.path.join(PKG, p)) != d)
print('frozen36 drift after:', R['frozen36DeviationsAfter'], '| package drift after:', R['packageDeviationsAfter'])
json.dump(R, open(os.path.join(OUT, 'r05-package13.json'), 'w'), indent=1, default=str)
print('wrote r05-package13.json')
