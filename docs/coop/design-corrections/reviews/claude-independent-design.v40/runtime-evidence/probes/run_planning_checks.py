"""Current planning checks (--check only; never --write) on the verified probe copy, plus independent recounts of the
v9 normative-input layer (and the v8 intermediate), coverage/planning-source bindings, inventory, recovery cases,
milestones and the report-feature dispositions."""
import hashlib, json, os, re, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v40'
SRC = RT + '/work/source40-pkg'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest40-index.json'))
res = {'copy': SRC}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-3000:], 'stderr': p.stderr[-3000:]}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def layer(path):
    raw = open(SRC + '/' + path, 'rb').read()
    d = json.loads(raw)
    files = d['files']
    bad = [f['path'] for f in files if sha(open(SRC + '/' + f['path'], 'rb').read()) != f['sha256'] or os.path.getsize(SRC + '/' + f['path']) != f['bytes']]
    return raw, d, files, bad


v9path = 'docs/v2/architecture/implementation-normative-inputs.v9.json'
v8path = 'docs/v2/architecture/implementation-normative-inputs.v8.json'
v9raw, v9, files, bad = layer(v9path)
v8raw, v8, files8, bad8 = layer(v8path)
v7old = json.load(open(S39 + '/docs/v2/architecture/implementation-normative-inputs.v7.json'))
cov = json.load(open(A + 'implementation-coverage.v1.json'))
cov39 = json.load(open(S39 + '/docs/v2/architecture/implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
selfbound = [f['path'] for f in files if f['path'] in (v9path, v8path, 'docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json')]


def ids(c):
    return {r.get('id') or json.dumps(r, sort_keys=True)[:80]: r for g in c['groups'].values() for r in g}


i40, i39 = ids(cov), ids(cov39)
changed_rows = sorted(k for k in set(i40) & set(i39) if i40[k] != i39[k])
report_inv = open(A + 'prototype-report-inventory.md', encoding='utf-8').read()
res['counts'] = {
    'v9Sha256': sha(v9raw), 'v9ExpectedSha256': '75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de',
    'v9MatchesManifestIndex': IDX.get(v9path) == sha(v9raw), 'v9Inputs': len(files), 'v9Mismatched': bad, 'v9TopKeys': sorted(v9.keys()),
    'v9BindsItselfOrItsBindingRecords': selfbound,
    'v8Sha256': sha(v8raw), 'v8Inputs': len(files8), 'v8Mismatched': bad8,
    'v8InputsNotCurrent': sorted(f['path'] for f in files8 if IDX.get(f['path']) != f['sha256']),
    'v9VersusV7PathsAdded': sorted({f['path'] for f in files} - {f['path'] for f in v7old['files']}),
    'v9VersusV7PathsRemoved': sorted({f['path'] for f in v7old['files']} - {f['path'] for f in files}),
    'v9VersusV7ShaChanged': sorted(f['path'] for f in files for g in v7old['files'] if f['path'] == g['path'] and f['sha256'] != g['sha256']),
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectSha256': cov.get('subjectManifestSha256'),
    'coverageSubjectMatchesV9': cov.get('subjectManifestSha256') == sha(v9raw),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV9': (ps.get('architecture') or {}).get('manifestSha256') == sha(v9raw),
    'planningSourcesArchitectureFiles': len((ps.get('architecture') or {}).get('files') or []),
    'planningSourcesArchitectureFilesEqualV9': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in files),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': len(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageMappingsSource39': sum(len(v) for v in cov39['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'coverageGroupsSource39': {k: len(v) for k, v in cov39['groups'].items()},
    'coverageRowIdsAdded40': sorted(set(i40) - set(i39)), 'coverageRowIdsRemoved40': sorted(set(i39) - set(i40)), 'coverageRowsChanged40': len(changed_rows),
    'coverageRowsChanged40Sample': changed_rows[:40],
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reviewIssues': [(r.get('id'), r.get('standing')) for r in cov.get('reviewIssues', [])],
    'reportInventoryRowIds': sorted(set(re.findall(r'^\|\s*(R\d\d)\s*\|', report_inv, re.M))),
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:9000])
