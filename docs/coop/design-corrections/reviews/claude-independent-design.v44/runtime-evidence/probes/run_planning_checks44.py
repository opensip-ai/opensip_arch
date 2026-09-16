"""Current planning checks (--check only; never --write) on the verified source44 probe copy, plus independent recounts of the
current v12 normative-input layer against v11, the preserved v11/v10/v9/v8 layers, coverage/planning-source bindings and history
records, inventory, recovery cases, milestones and report features, measured against the exact parent source43. Also records every
changed normative/reference document of the 43->44 delta that the current layer does NOT bind."""
import hashlib, json, os, re, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v44'
SRC = RT + '/work/source44-pkg'
S43 = RT + '/work/base43'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest44-index.json'))
SV = json.load(open(RT + '/receipts/subject-verification.json'))
res = {'copy': SRC, 'parentCopy': S43}
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
    bad = [f['path'] for f in files if not os.path.exists(SRC + '/' + f['path']) or sha(open(SRC + '/' + f['path'], 'rb').read()) != f['sha256'] or os.path.getsize(SRC + '/' + f['path']) != f['bytes']]
    return raw, d, files, bad


L = {v: 'docs/v2/architecture/implementation-normative-inputs.v%s.json' % v for v in ('8', '9', '10', '11', '12')}
layers = {v: layer(SRC, p) for v, p in L.items()}
cov = json.load(open(A + 'implementation-coverage.v1.json'))
cov43 = json.load(open(S43 + '/docs/v2/architecture/implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
v12raw, v11raw = layers['12'][0], layers['11'][0]
v12 = {f['path']: f for f in layers['12'][2]}
v11 = {f['path']: f for f in layers['11'][2]}
delta = SV['delta']['43to44']
changed_paths = sorted({r['path'] for k in ('changed', 'added') for r in delta[k]})


def ids(c):
    return {r.get('id') or json.dumps(r, sort_keys=True)[:80]: r for g in c['groups'].values() for r in g}


i44, i43 = ids(cov), ids(cov43)
history_keys = [k for k, v in ps.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'manifestPath' in v[0]]
history = [(h['manifestPath'], h['manifestSha256']) for k in history_keys for h in ps[k]]
report_inv = open(A + 'prototype-report-inventory.md', encoding='utf-8').read()
arch_files = sorted(os.path.relpath(os.path.join(d, f), SRC) for d, _, fs in os.walk(A) for f in fs)
normative_markers = {}
for p in changed_paths:
    if p in v12 or not os.path.isfile(SRC + '/' + p):
        continue
    text = open(SRC + '/' + p, 'rb').read()[:6000].decode('utf-8', 'replace')
    normative_markers[p] = {'selfDeclaresNormativeOrCurrent': bool(re.search(r'NORMATIVE|CURRENT selected|normative', text)), 'boundByV12': False,
                            'boundByV11': p in v11, 'coverageSource': any(v['path'] == p for v in cov['sources'].values())}
res['counts'] = {
    'layerSha256': {v: sha(layers[v][0]) for v in layers}, 'layerInputs': {v: len(layers[v][2]) for v in layers},
    'layerMismatchedAgainstSource44': {v: layers[v][3] for v in layers},
    'v12ExpectedSha256': '2ef6d70f900181990813e8d12a609aed93f3d031f5d9efe15c014d487ccbbf7c', 'v12MatchesHeader': sha(v12raw) == '2ef6d70f900181990813e8d12a609aed93f3d031f5d9efe15c014d487ccbbf7c',
    'v12MatchesManifestIndex': IDX.get(L['12']) == sha(v12raw),
    'v12AddedVsV11': sorted(set(v12) - set(v11)), 'v12RemovedVsV11': sorted(set(v11) - set(v12)),
    'v12ChangedVsV11': sorted(p for p in set(v12) & set(v11) if v12[p]['sha256'] != v11[p]['sha256']),
    'priorLayersByteEqualToSource43': {v: sha(layers[v][0]) == sha(open(S43 + '/' + L[v], 'rb').read()) for v in ('8', '9', '10', '11')},
    'v12InputsInTheDelta': sorted(set(v12) & set(changed_paths)),
    'deltaDocumentsNotBoundByV12': normative_markers,
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectMatchesV12': cov.get('subjectManifest') == L['12'] and cov.get('subjectManifestSha256') == sha(v12raw),
    'coverageSourcesAllBoundByV12': all(v.get('location') == 'working-tree' or (v['path'] in v12 and v12[v['path']]['sha256'] == v['sha256']) for v in cov['sources'].values()),
    'coverageSourceKeysAddedVs43': sorted(set(cov['sources']) - set(cov43['sources'])), 'coverageSourceKeysRemovedVs43': sorted(set(cov43['sources']) - set(cov['sources'])),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV12': (ps.get('architecture') or {}).get('manifestSha256') == sha(v12raw),
    'planningSourcesArchitectureFilesEqualV12': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['12'][2]),
    'planningSourcesPrevious': ((ps.get('previousArchitectureInputLayer') or {}).get('manifestPath'), (ps.get('previousArchitectureInputLayer') or {}).get('manifestSha256')),
    'planningSourcesPreviousFilesEqualV11': sorted((f['path'], f['sha256']) for f in ((ps.get('previousArchitectureInputLayer') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['11'][2]),
    'planningSourcesHistoryKeys': history_keys, 'planningSourcesHistoryCount': len(history), 'planningSourcesHistory': history,
    'planningSourcesHistoryHashesMatchLayerBytes': all(sha(open(SRC + '/' + p, 'rb').read()) == s for p, s in history if os.path.exists(SRC + '/' + p)),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': len(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()), 'coverageMappingsSource43': sum(len(v) for v in cov43['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'coverageRowIdsAddedVs43': sorted(set(i44) - set(i43)), 'coverageRowIdsRemovedVs43': sorted(set(i43) - set(i44)),
    'coverageRowsChangedVs43': sorted(k for k in set(i44) & set(i43) if i44[k] != i43[k]),
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'architectureDirFileCount': len(arch_files),
    'architectureDirFilesChangedVs43': sorted(r for r in arch_files if not os.path.exists(S43 + '/' + r) or sha(open(SRC + '/' + r, 'rb').read()) != sha(open(S43 + '/' + r, 'rb').read())),
    'operationsCheckersByteEqualToSource43': {n: sha(open(SRC + '/docs/operations/' + n, 'rb').read()) == sha(open(S43 + '/docs/operations/' + n, 'rb').read())
                                              for n in ('check_implementation_planning.py', 'check_repository_file_inventory.py')},
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:12000])
