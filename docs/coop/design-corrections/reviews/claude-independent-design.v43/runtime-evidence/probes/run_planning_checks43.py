"""Current planning checks (--check only; never --write) on the verified source43 probe copy, plus independent recounts of the
v11 normative-input layer, the historical v10/v9/v8 layers (bytes preserved), coverage/planning-source bindings and history
records, inventory, recovery cases, milestones and the report-feature dispositions, measured against the exact parent source42."""
import hashlib, json, os, re, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v43'
SRC = RT + '/work/source43-pkg'
S42 = RT + '/work/base42'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest43-index.json'))
res = {'copy': SRC, 'parentCopy': S42}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-3000:], 'stderr': p.stderr[-3000:],
                 'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest()}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def layer(root, path):
    raw = open(root + '/' + path, 'rb').read()
    d = json.loads(raw)
    files = d['files']
    bad = [f['path'] for f in files if sha(open(SRC + '/' + f['path'], 'rb').read()) != f['sha256'] or os.path.getsize(SRC + '/' + f['path']) != f['bytes']]
    return raw, d, files, bad


L = {v: 'docs/v2/architecture/implementation-normative-inputs.v%s.json' % v for v in ('8', '9', '10', '11')}
layers = {v: layer(SRC, p) for v, p in L.items()}
cov = json.load(open(A + 'implementation-coverage.v1.json'))
cov42 = json.load(open(S42 + '/docs/v2/architecture/implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
v11raw = layers['11'][0]
v11_paths = [f['path'] for f in layers['11'][2]]
changed43 = ['docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json', 'docs/coop/design-corrections/foundation/source-pins.v1.json',
             'docs/coop/design-corrections/native/source-pins.v2.json', 'docs/coop/design-corrections/security/source-pins.v1.json',
             'docs/coop/design-corrections/workflows/check-query-projection.v3.py', 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
             'docs/coop/design-corrections/workflows/query_projection_model.v3.py', 'docs/coop/design-corrections/workflows/source-pins.v1.json',
             'docs/coop/design-corrections/workflows/workflows-report.v1.json']


def ids(c):
    return {r.get('id') or json.dumps(r, sort_keys=True)[:80]: r for g in c['groups'].values() for r in g}


i43, i42 = ids(cov), ids(cov42)
history_keys = [k for k, v in ps.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'manifestPath' in v[0]]
history = [(h['manifestPath'], h['manifestSha256']) for k in history_keys for h in ps[k]]
report_inv = open(A + 'prototype-report-inventory.md', encoding='utf-8').read()
arch_files = sorted(os.path.relpath(os.path.join(d, f), SRC) for d, _, fs in os.walk(A) for f in fs)
res['counts'] = {
    'layerSha256': {v: sha(layers[v][0]) for v in layers}, 'layerInputs': {v: len(layers[v][2]) for v in layers},
    'layerMismatchedAgainstSource43': {v: layers[v][3] for v in layers},
    'v11ExpectedSha256': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de', 'v11MatchesManifestIndex': IDX.get(L['11']) == sha(v11raw),
    'layersByteEqualToSource42': {v: sha(layers[v][0]) == sha(open(S42 + '/' + L[v], 'rb').read()) for v in L},
    'v11InputsIntersectingThe9ChangedFiles': sorted(set(v11_paths) & set(changed43)),
    'coverageSourcesIntersectingThe9ChangedFiles': sorted({v['path'] for v in cov['sources'].values()} & set(changed43)),
    'architectureDirFilesByteEqualToSource42': all(sha(open(SRC + '/' + r, 'rb').read()) == sha(open(S42 + '/' + r, 'rb').read()) for r in arch_files if os.path.exists(S42 + '/' + r)),
    'architectureDirFileCount': len(arch_files),
    'operationsCheckersByteEqualToSource42': {n: sha(open(SRC + '/docs/operations/' + n, 'rb').read()) == sha(open(S42 + '/docs/operations/' + n, 'rb').read())
                                              for n in ('check_implementation_planning.py', 'check_repository_file_inventory.py')},
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectSha256': cov.get('subjectManifestSha256'),
    'coverageSubjectMatchesV11': cov.get('subjectManifest') == L['11'] and cov.get('subjectManifestSha256') == sha(v11raw),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV11': (ps.get('architecture') or {}).get('manifestSha256') == sha(v11raw),
    'planningSourcesArchitectureFilesEqualV11': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['11'][2]),
    'planningSourcesHistoryKeys': history_keys, 'planningSourcesHistoryCount': len(history),
    'planningSourcesHistoryHashesMatchLayerBytes': all(sha(open(SRC + '/' + p, 'rb').read()) == s for p, s in history if os.path.exists(SRC + '/' + p)),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': len(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageMappingsSource42': sum(len(v) for v in cov42['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'coverageRowIdsAddedVs42': sorted(set(i43) - set(i42)), 'coverageRowIdsRemovedVs42': sorted(set(i42) - set(i43)),
    'coverageRowsChangedVs42': sorted(k for k in set(i43) & set(i42) if i43[k] != i42[k]),
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reportInventoryRowIds': sorted(set(re.findall(r'^\|\s*(R\d\d)\s*\|', report_inv, re.M))),
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:9000])
