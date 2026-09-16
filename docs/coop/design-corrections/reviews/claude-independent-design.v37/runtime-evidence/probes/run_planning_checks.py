"""Run the two planning checkers in check mode against a verified exact copy and independently recount
planning5 populations (inputs, paths, packages, mappings, recovery cases, milestones)."""
import hashlib, json, os, subprocess
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SRC = BASE + '/work/source37-pkg'
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = BASE + '/receipts/planning-checks.json'
res = {'copy': SRC}
for name, cmd in [
    ('check_implementation_planning', [PY, '-I', '-B', SRC + '/docs/operations/check_implementation_planning.py', '--source', SRC, '--check']),
    ('check_repository_file_inventory', [PY, '-I', '-B', SRC + '/docs/operations/check_repository_file_inventory.py', '--check']),
]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
    res[name] = {'command': cmd, 'exitCode': p.returncode, 'stdout': p.stdout[-2000:], 'stderr': p.stderr[-2000:]}
A = SRC + '/docs/v2/architecture/'
ni = json.load(open(A + 'implementation-normative-inputs.v5.json'))
inv = json.load(open(A + 'repository-file-inventory.v1.json'))
cov = json.load(open(A + 'implementation-coverage.v1.json'))
rec = json.load(open(A + 'commit-recovery-plan.v1.json'))
bad_inputs = []
for f in ni['files']:
    b = open(SRC + '/' + f['path'], 'rb').read()
    if hashlib.sha256(b).hexdigest() != f['sha256'] or len(b) != f['bytes']:
        bad_inputs.append(f['path'])
gen_paths = [r['path'] for r in inv['files'] if r['generated']]
res['counts'] = {
    'normativeInputs': len(ni['files']), 'normativeInputsMismatched': bad_inputs,
    'normativeInputsManifestSha256': hashlib.sha256(open(A + 'implementation-normative-inputs.v5.json', 'rb').read()).hexdigest(),
    'inventoryPaths': len(inv['files']), 'inventoryPackages': len(inv['packages']),
    'generatedInventoryPaths': gen_paths,
    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
    'coverageGroups': {k: len(v) for k, v in cov['groups'].items()},
    'recoveryCases': len(rec['cases']), 'recoveryCasesNotExecuted': sum(1 for c in rec['cases'] if c['executionStanding'] == 'not-executed'),
    'milestoneOrder': cov['milestoneOrder'],
    'coverageVerificationStandings': sorted({r['verification']['standing'] for g in cov['groups'].values() for r in g}),
    'reviewIssues': [r['id'] for r in cov.get('reviewIssues', [])],
}
gq = SRC + '/docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'
L = open(gq, encoding='utf-8').read().split('\n')
res['graphQuerySchemaLines'] = {'lines': len(L), 'maxLen': max(len(x) for x in L)}
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res, indent=1)[:6000])
