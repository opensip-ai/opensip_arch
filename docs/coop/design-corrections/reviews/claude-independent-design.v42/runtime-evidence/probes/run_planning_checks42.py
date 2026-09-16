"""Current planning checks (--check only; never --write) on the verified source42 probe copy, plus independent recounts of the
v11 normative-input layer, the historical v10/v9/v8 layers (bytes preserved), coverage/planning-source bindings and history
records, inventory, recovery cases, milestones and the report-feature dispositions, measured against source40 and source41."""
import hashlib, json, os, re, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
SRC = RT + '/work/source42-pkg'
S40 = '/tmp/opensip-design-corrections/candidate-subject.v40'
S41 = '/tmp/opensip-design-corrections/candidate-subject.v41'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest42-index.json'))
res = {'copy': SRC}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-3000:], 'stderr': p.stderr[-3000:]}


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
cov40 = json.load(open(S40 + '/docs/v2/architecture/implementation-coverage.v1.json'))
cov41 = json.load(open(S41 + '/docs/v2/architecture/implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
v11raw = layers['11'][0]
selfbound = [f['path'] for f in layers['11'][2] if f['path'] in list(L.values()) + ['docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json']]


def ids(c):
    return {r.get('id') or json.dumps(r, sort_keys=True)[:80]: r for g in c['groups'].values() for r in g}


i42, i40, i41 = ids(cov), ids(cov40), ids(cov41)
history_keys = [k for k, v in ps.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'manifestPath' in v[0]]
history = [(h['manifestPath'], h['manifestSha256']) for k in history_keys for h in ps[k]]
report_inv = open(A + 'prototype-report-inventory.md', encoding='utf-8').read()
res['counts'] = {
    'layerSha256': {v: sha(layers[v][0]) for v in layers}, 'layerInputs': {v: len(layers[v][2]) for v in layers},
    'layerMismatchedAgainstSource42': {v: layers[v][3] for v in layers},
    'v11ExpectedSha256': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de', 'v11MatchesManifestIndex': IDX.get(L['11']) == sha(v11raw),
    'v8PreservedSha256Expected': '99c8f8760c0eaff47b8de4b9b99e4ceb8304ffd1b4c6deb7d3c013e5dd65b490',
    'v8UnchangedFrom40': sha(layers['8'][0]) == sha(open(S40 + '/' + L['8'], 'rb').read()),
    'v9UnchangedFrom40': sha(layers['9'][0]) == sha(open(S40 + '/' + L['9'], 'rb').read()),
    'v10UnchangedFrom41': sha(layers['10'][0]) == sha(open(S41 + '/' + L['10'], 'rb').read()),
    'v9v10v11ByteIdentical': layers['9'][0] == layers['10'][0] == layers['11'][0],
    'v11BindsItselfOrItsBindingRecords': selfbound,
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectSha256': cov.get('subjectManifestSha256'),
    'coverageSubjectMatchesV11': cov.get('subjectManifest') == L['11'] and cov.get('subjectManifestSha256') == sha(v11raw),
    'planningSourcesStanding': ps.get('standing'),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV11': (ps.get('architecture') or {}).get('manifestSha256') == sha(v11raw),
    'planningSourcesArchitectureFilesEqualV11': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['11'][2]),
    'planningSourcesPrevious': ((ps.get('previousArchitectureInputLayer') or {}).get('manifestPath'), (ps.get('previousArchitectureInputLayer') or {}).get('manifestSha256')),
    'planningSourcesHistoryKeys': history_keys, 'planningSourcesHistory': history,
    'planningSourcesHistoryHashesMatchLayerBytes': all(sha(open(SRC + '/' + p, 'rb').read()) == s for p, s in history if os.path.exists(SRC + '/' + p)),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': len(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageMappingsSource41': sum(len(v) for v in cov41['groups'].values()),
    'coverageMappingsSource40': sum(len(v) for v in cov40['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'coverageRowIdsAddedVs40': sorted(set(i42) - set(i40)), 'coverageRowIdsRemovedVs40': sorted(set(i40) - set(i42)),
    'coverageRowsChangedVs40': sorted(k for k in set(i42) & set(i40) if i42[k] != i40[k]),
    'coverageRowsChangedVs41': sorted(k for k in set(i42) & set(i41) if i42[k] != i41[k]),
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reportInventoryRowIds': sorted(set(re.findall(r'^\|\s*(R\d\d)\s*\|', report_inv, re.M))),
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:9000])
