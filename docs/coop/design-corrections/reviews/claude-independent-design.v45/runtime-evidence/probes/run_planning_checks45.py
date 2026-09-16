"""Current planning checks (--check only; never --write) on the verified source45 probe copy, plus independent recounts of the
current v13 normative-input layer against v12, the preserved v12/v11/v10/v9/v8 layers, coverage/planning-source bindings and history
records, inventory, recovery cases, milestones and report features, measured against the exact parent source44. Also records every
changed normative/reference document of the 44->45 delta that the current layer does NOT bind, and whether the protocol3 table and
fact-batch v3 (ADV44-01) are bound."""
import hashlib, json, os, re, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v45'
SRC = RT + '/work/source45-pkg'
S44 = RT + '/work/base44'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest45-index.json'))
SV = json.load(open(RT + '/receipts/subject-verification.json'))
res = {'copy': SRC, 'parentCopy': S44}
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


L = {v: 'docs/v2/architecture/implementation-normative-inputs.v%s.json' % v for v in ('8', '9', '10', '11', '12', '13')}
layers = {v: layer(SRC, p) for v, p in L.items()}
cov = json.load(open(A + 'implementation-coverage.v1.json'))
cov44 = json.load(open(S44 + '/docs/v2/architecture/implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
v13raw = layers['13'][0]
v13 = {f['path']: f for f in layers['13'][2]}
v12 = {f['path']: f for f in layers['12'][2]}
delta = SV['delta']['44to45']
changed_paths = sorted({r['path'] for k in ('changed', 'added') for r in delta[k]})


def ids(c):
    return {r.get('id') or json.dumps(r, sort_keys=True)[:80]: r for g in c['groups'].values() for r in g}


def strip_selector_lines(r):
    x = json.loads(json.dumps(r))
    src = x.get('source') or {}
    sel = src.get('selector')
    if isinstance(sel, dict):
        sel.pop('firstLine', None)
        sel.pop('lastLine', None)
    return x


i45, i44 = ids(cov), ids(cov44)
history_keys = [k for k, v in ps.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'manifestPath' in v[0]]
history = [(h['manifestPath'], h['manifestSha256']) for k in history_keys for h in ps[k]]
arch_files = sorted(os.path.relpath(os.path.join(d, f), SRC) for d, _, fs in os.walk(A) for f in fs)
normative_markers = {}
for p in changed_paths:
    if p in v13 or not os.path.isfile(SRC + '/' + p):
        continue
    text = open(SRC + '/' + p, 'rb').read()[:6000].decode('utf-8', 'replace')
    normative_markers[p] = {'selfDeclaresNormativeOrCurrent': bool(re.search(r'NORMATIVE|CURRENT selected|normative', text)), 'boundByV13': False,
                            'boundByV12': p in v12, 'coverageSource': any(v['path'] == p for v in cov['sources'].values())}
changed_rows = sorted(k for k in set(i45) & set(i44) if i45[k] != i44[k])
res['counts'] = {
    'layerSha256': {v: sha(layers[v][0]) for v in layers}, 'layerInputs': {v: len(layers[v][2]) for v in layers},
    'layerMismatchedAgainstSource45': {v: layers[v][3] for v in layers},
    'v13ExpectedSha256': 'af228325492828b0ea5d6779601725a981bb467d0195e976a4247350c972c153',
    'v13MatchesHeader': sha(v13raw) == 'af228325492828b0ea5d6779601725a981bb467d0195e976a4247350c972c153',
    'v13MatchesManifestIndex': IDX.get(L['13']) == sha(v13raw),
    'v13AddedVsV12': sorted(set(v13) - set(v12)), 'v13RemovedVsV12': sorted(set(v12) - set(v13)),
    'v13ChangedVsV12': sorted(p for p in set(v13) & set(v12) if v13[p]['sha256'] != v12[p]['sha256']),
    'priorLayersByteEqualToSource44': {v: sha(layers[v][0]) == sha(open(S44 + '/' + L[v], 'rb').read()) for v in ('8', '9', '10', '11', '12')},
    'v13InputsInTheDelta': sorted(set(v13) & set(changed_paths)),
    'deltaDocumentsNotBoundByV13': normative_markers,
    'adv4401': {p: p in v13 for p in ('docs/coop/design-corrections/native/protocol3-transitions.v1.json', 'docs/coop/design-corrections/native/fact-batch.schema.v3.json')},
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectMatchesV13': cov.get('subjectManifest') == L['13'] and cov.get('subjectManifestSha256') == sha(v13raw),
    'coverageSourcesAllBoundByV13': all(v.get('location') == 'working-tree' or (v['path'] in v13 and v13[v['path']]['sha256'] == v['sha256']) for v in cov['sources'].values()),
    'coverageSourceKeysAddedVs44': sorted(set(cov['sources']) - set(cov44['sources'])), 'coverageSourceKeysRemovedVs44': sorted(set(cov44['sources']) - set(cov['sources'])),
    'coverageSourcesChangedVs44': sorted(k for k in set(cov['sources']) & set(cov44['sources']) if cov['sources'][k] != cov44['sources'][k]),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV13': (ps.get('architecture') or {}).get('manifestSha256') == sha(v13raw),
    'planningSourcesArchitectureFilesEqualV13': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['13'][2]),
    'planningSourcesPrevious': ((ps.get('previousArchitectureInputLayer') or {}).get('manifestPath'), (ps.get('previousArchitectureInputLayer') or {}).get('manifestSha256')),
    'planningSourcesPreviousFilesEqualV12': sorted((f['path'], f['sha256']) for f in ((ps.get('previousArchitectureInputLayer') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in layers['12'][2]),
    'planningSourcesHistoryKeys': history_keys, 'planningSourcesHistoryCount': len(history), 'planningSourcesHistory': history,
    'planningSourcesHistoryHashesMatchLayerBytes': all(sha(open(SRC + '/' + p, 'rb').read()) == s for p, s in history if os.path.exists(SRC + '/' + p)),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': len(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()), 'coverageMappingsSource44': sum(len(v) for v in cov44['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'coverageRowIdsAddedVs44': sorted(set(i45) - set(i44)), 'coverageRowIdsRemovedVs44': sorted(set(i44) - set(i45)),
    'coverageRowsChangedVs44': changed_rows,
    'coverageRowsChangedOtherThanSelectorLinesAndValueDigest': sorted(k for k in changed_rows if json.dumps(strip_selector_lines({kk: vv for kk, vv in i45[k].items()}), sort_keys=True).replace(i45[k].get('source', {}).get('valueSha256', '') or '§', '§') != json.dumps(strip_selector_lines({kk: vv for kk, vv in i44[k].items()}), sort_keys=True).replace(i44[k].get('source', {}).get('valueSha256', '') or '§', '§')),
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'architectureDirFileCount': len(arch_files),
    'architectureDirFilesChangedVs44': sorted(r for r in arch_files if not os.path.exists(S44 + '/' + r) or sha(open(SRC + '/' + r, 'rb').read()) != sha(open(S44 + '/' + r, 'rb').read())),
    'operationsCheckersByteEqualToSource44': {n: sha(open(SRC + '/docs/operations/' + n, 'rb').read()) == sha(open(S44 + '/docs/operations/' + n, 'rb').read())
                                              for n in ('check_implementation_planning.py', 'check_repository_file_inventory.py')},
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:14000])
