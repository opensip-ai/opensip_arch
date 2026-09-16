"""Current planning checks (--check only) on the verified probe copy, plus independent recounts of the v6 layer."""
import hashlib, json, os, subprocess

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
SRC = RT + '/work/source38-pkg'
PY = '/tmp/opensip-architecture-review-env/bin/python'
A = SRC + '/docs/v2/architecture/'
res = {'copy': SRC}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-3000:], 'stderr': p.stderr[-3000:]}


def sha(b):
    return hashlib.sha256(b).hexdigest()


v6raw = open(A + 'implementation-normative-inputs.v6.json', 'rb').read()
v6 = json.loads(v6raw)
bad = [f['path'] for f in v6['files'] if sha(open(SRC + '/' + f['path'], 'rb').read()) != f['sha256'] or os.path.getsize(SRC + '/' + f['path']) != f['bytes']]
cov = json.load(open(A + 'implementation-coverage.v1.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
ps = json.load(open(A + 'implementation-planning-sources.v1.json'))
res['counts'] = {
    'v6Sha256': sha(v6raw), 'v6Inputs': len(v6['files']), 'v6Mismatched': bad,
    'coverageSubjectManifest': cov.get('subjectManifest'), 'coverageSubjectSha256': cov.get('subjectManifestSha256'),
    'coverageSubjectMatchesV6': cov.get('subjectManifestSha256') == sha(v6raw),
    'planningSourcesArchitectureManifest': (ps.get('architecture') or {}).get('manifestPath'),
    'planningSourcesArchitectureSha256MatchesV6': (ps.get('architecture') or {}).get('manifestSha256') == sha(v6raw),
    'planningSourcesArchitectureFiles': len((ps.get('architecture') or {}).get('files') or []),
    'coverageSourcesStale': sorted(k for k, v in cov['sources'].items() if sha(open(SRC + '/' + v['path'], 'rb').read()) != v['sha256']),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'verificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reviewIssues': [(r['id'], r['standing']) for r in cov.get('reviewIssues', [])],
}
json.dump(res, open(RT + '/receipts/planning-checks.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:6000])
