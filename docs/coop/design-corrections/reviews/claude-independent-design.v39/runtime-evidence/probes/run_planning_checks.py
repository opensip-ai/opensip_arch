"""Current planning checks (--check only; never --write) on the verified probe copy, plus independent recounts of the
v7 normative-input layer, coverage/planning-source bindings, inventory, recovery cases and milestones."""
import hashlib, json, os, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
SRC = RT + '/work/source39-pkg'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
IDX = json.load(open(RT + '/receipts/manifest39-index.json'))
res = {'copy': SRC}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-3000:], 'stderr': p.stderr[-3000:]}


def sha(b):
    return hashlib.sha256(b).hexdigest()


v7path = 'docs/v2/architecture/implementation-normative-inputs.v7.json'
v7raw = open(SRC + '/' + v7path, 'rb').read()
v7 = json.loads(v7raw)
files = v7['files']
bad = [f['path'] for f in files if sha(open(SRC + '/' + f['path'], 'rb').read()) != f['sha256'] or os.path.getsize(SRC + '/' + f['path']) != f['bytes']]
cov = json.load(open(A + 'implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
selfbound = [f['path'] for f in files if f['path'] in (v7path, 'docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json')]
res['counts'] = {
    'v7Sha256': sha(v7raw), 'v7ExpectedSha256': '8543d29f7047b7228f98eef12b2ae1f2d5738ec7447c8cd9605b259da029900f',
    'v7MatchesManifestIndex': IDX.get(v7path) == sha(v7raw), 'v7Inputs': len(files), 'v7Mismatched': bad,
    'v7BindsItselfOrItsBindingRecords': selfbound, 'v7TopKeys': sorted(v7.keys()),
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectSha256': cov.get('subjectManifestSha256'),
    'coverageSubjectMatchesV7': cov.get('subjectManifestSha256') == sha(v7raw),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV7': (ps.get('architecture') or {}).get('manifestSha256') == sha(v7raw),
    'planningSourcesArchitectureFiles': len((ps.get('architecture') or {}).get('files') or []),
    'planningSourcesArchitectureFilesEqualV7': sorted((f['path'], f['sha256']) for f in ((ps.get('architecture') or {}).get('files') or [])) == sorted((f['path'], f['sha256']) for f in files),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'coverageSourceKeys': sorted(cov['sources']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reviewIssues': [(r['id'], r['standing']) for r in cov.get('reviewIssues', [])],
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:8000])
