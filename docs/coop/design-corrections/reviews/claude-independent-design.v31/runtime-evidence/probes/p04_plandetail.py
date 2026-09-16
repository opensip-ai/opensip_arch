"""PROBE 04 (v31) — measure the actual planning decisions on frozen31: 198 paths / 20 groups /
320 coverage mappings / M0-M6 sequencing / 54 recovery cases / report boundaries, plus the
filename-directory-crate-module plan. Establishes ancestry as UNCHANGED rather than inventing a plan."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {}

inv = json.load(open(os.path.join(A, 'repository-file-inventory.v1.json')))
cov = json.load(open(os.path.join(A, 'implementation-coverage.v1.json')))
rec = json.load(open(os.path.join(A, 'commit-recovery-plan.v1.json')))

R['inventory'] = {'files': len(inv['files']), 'packages': len(inv['packages']),
                  'pendingDecisions': len(inv.get('pendingDecisions', [])),
                  'standing': str(inv.get('standing'))[:200]}
print('repository-file-inventory: %d files, %d packages, %d pendingDecisions'
      % (len(inv['files']), len(inv['packages']), len(inv.get('pendingDecisions', []))))
sample = inv['files'][0]
R['inventoryRowKeys'] = sorted(sample)
print('  row keys:', sorted(sample))
print('  sample  :', json.dumps(sample)[:300])
# crates / modules / directories
crates = sorted(set(f.get('package') or f.get('crate') or '' for f in inv['files']))
R['distinctPackages'] = [c for c in crates if c][:40]
R['distinctPackageCount'] = len([c for c in crates if c])
dirs = sorted(set(os.path.dirname(f['path']) for f in inv['files'] if 'path' in f))
R['distinctDirectories'] = len(dirs)
print('  distinct packages: %d  distinct directories: %d'
      % (R['distinctPackageCount'], R['distinctDirectories']))
print('  packages:', R['distinctPackages'][:12])

R['coverage'] = {'groups': len(cov['groups']),
                 'milestoneOrder': cov.get('milestoneOrder'),
                 'milestoneStanding': str(cov.get('milestoneStanding'))[:200],
                 'sources': len(cov.get('sources', [])),
                 'reviewIssues': len(cov.get('reviewIssues', [])),
                 'subjectManifestSha256': cov.get('subjectManifestSha256'),
                 'moduleFirstMilestoneCount': len(cov.get('moduleFirstMilestone', {}))}
print('\nimplementation-coverage: %d groups, milestoneOrder=%s'
      % (len(cov['groups']), cov.get('milestoneOrder')))
print('  subjectManifestSha256 pinned inside:', str(cov.get('subjectManifestSha256'))[:24])
# count mappings across groups
# cov['groups'] is a MAPPING keyed by group name, not a list of dicts. My first run assumed a
# list and raised AttributeError; that was my probe defect, preserved in the receipts.
total_map = 0
gnames = []
groups = cov['groups']
items = groups.items() if isinstance(groups, dict) else [(str(i), g) for i, g in enumerate(groups)]
for gname, g in items:
    gnames.append(gname)
    if isinstance(g, dict):
        for k, v in g.items():
            if isinstance(v, list):
                total_map += len(v)
    elif isinstance(g, list):
        total_map += len(g)
R['coverageGroupNames'] = gnames
R['coverageListItemsAcrossGroups'] = total_map
# a more precise mapping count: look for the source-bound mapping arrays
def deep_count(o, key):
    n = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key and isinstance(v, list):
                n += len(v)
            n += deep_count(v, key)
    elif isinstance(o, list):
        for v in o:
            n += deep_count(v, key)
    return n
for key in ('mappings', 'sourceMappings', 'modules', 'files', 'items', 'rows'):
    c = deep_count(cov, key)
    if c:
        R.setdefault('coverageDeepCounts', {})[key] = c
print('  deep counts:', json.dumps(R.get('coverageDeepCounts', {})))
print('  group names:', gnames)

R['recoveryCases'] = len(rec['cases'])
R['recoveryCaseKeys'] = sorted(rec['cases'][0])
executed = [c for c in rec['cases'] if any(
    str(c.get(k)).lower() in ('true', 'executed', 'passed') for k in c if 'execut' in k.lower())]
R['recoveryCasesExecuted'] = len(executed)
print('\ncommit-recovery-plan: %d cases, executed=%d' % (len(rec['cases']), len(executed)))
print('  case keys:', R['recoveryCaseKeys'])
print('  standing :', str(rec.get('conclusionStanding'))[:250])

# qualification gates
qg = os.path.join(SRC, 'docs/coop/design-corrections/qualification-gates.proposed.json')
q = json.load(open(qg))
gates = q['gates'] if isinstance(q, dict) and 'gates' in q else (q if isinstance(q, list) else q.get('items', []))
R['qualificationGates'] = len(gates)
qualified = sum(1 for g in gates if g.get('qualified'))
demo = sum(1 for g in gates if g.get('demonstrated'))
harness = sum(1 for g in gates if g.get('implementationHarnessAuthored'))
R['gatesQualified'], R['gatesDemonstrated'], R['gatesHarnessAuthored'] = qualified, demo, harness
R['gatesSha256'] = hashlib.sha256(open(qg, 'rb').read()).hexdigest()
print('\nqualification gates: %d  qualified=%d demonstrated=%d harnessAuthored=%d'
      % (len(gates), qualified, demo, harness))
standings = sorted(set(str(g.get('standing')) for g in gates))
R['gateStandings'] = standings[:5]
print('  standings:', standings[:3])

json.dump(R, open(os.path.join(OUT, 'p04-plandetail.json'), 'w'), indent=1)
print('\nwrote p04-plandetail.json')
