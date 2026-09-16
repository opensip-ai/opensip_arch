"""PROBE H — the planning source layer and the implementation-coverage account, traversed
completely and checked against the frozen manifest rather than the authors' counts."""
import hashlib, json, os, collections

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
man = {r['path']: r for r in json.load(open(MAN))['files']}
R = {}

s = json.load(open(os.path.join(ROOT, 'docs/v2/architecture/implementation-planning-sources.v1.json'), encoding='utf-8'))
R['planning_standing'] = s['standing']
R['prototype_commit'] = s['prototype']['commit']
R['prototype_files'] = len(s['prototype']['files'])
arch = s['architecture']
R['architecture_keys'] = list(arch) if isinstance(arch, dict) else ('list', len(arch))
rows = arch['files'] if isinstance(arch, dict) and 'files' in arch else (
    arch if isinstance(arch, list) else [])
R['architecture_rows'] = len(rows)

# every architecture-source pin must resolve INSIDE the frozen subject and match its bytes
bad, ok, notin = [], 0, []
for r in rows:
    p = r.get('path')
    if p is None:
        continue
    full = os.path.join(ROOT, p)
    if not os.path.isfile(full):
        notin.append(p)
        continue
    h = hashlib.sha256(open(full, 'rb').read()).hexdigest()
    if r.get('sha256') and h != r['sha256']:
        bad.append({'path': p, 'pinned': r['sha256'][:16], 'actual': h[:16]})
    else:
        ok += 1
R['architecture_pins_matching_frozen_bytes'] = ok
R['architecture_pins_mismatched'] = bad
R['architecture_pins_absent_from_subject'] = notin
R['originalArchitectureSource25'] = s.get('originalArchitectureSource25')

# prototype pins are OUTSIDE this repository by design (a separate prototype checkout)
R['prototype_pins_present_in_subject'] = sum(
    1 for f in s['prototype']['files'] if os.path.isfile(os.path.join(ROOT, f['path'])))
R['prototype_pins_note'] = ('prototype files are pinned in a separate repository at a named commit; '
                            'they are not members of this subject, so their digests are not '
                            'independently verifiable from these bytes')

cov = json.load(open(os.path.join(ROOT, 'docs/v2/architecture/implementation-coverage.v1.json'), encoding='utf-8'))
R['coverage_top_keys'] = sorted(cov.keys())
pops = {}
for k, v in cov.items():
    if isinstance(v, list):
        pops[k] = len(v)
    elif isinstance(v, dict) and all(isinstance(x, (dict, list)) for x in v.values()):
        pops[k] = len(v)
R['coverage_populations'] = pops
for name in ('commands', 'queryOperations', 'capabilityCells', 'qualificationGates',
             'sharedFlags', 'renderers', 'workflowGoldens', 'contractSections',
             'fallowConstraints', 'hydraProposals', 'reportFeatures'):
    v = cov.get(name)
    if isinstance(v, list):
        R.setdefault('declared_population_sizes', {})[name] = len(v)
        R.setdefault('declared_population_rowkeys', {})[name] = sorted(v[0].keys()) if v else []

# are any coverage rows claiming execution / qualification?
flat = json.dumps(cov)
R['coverage_claims_executed'] = flat.count('"executed": true')
R['coverage_claims_qualified'] = flat.count('"qualified": true')
R['coverage_claims_demonstrated'] = flat.count('"demonstrated": true')

# milestone schedule integrity
if isinstance(cov.get('commands'), list):
    ms = collections.Counter(c.get('milestone') for c in cov['commands'])
    R['command_milestones'] = dict(ms)
    R['command_count'] = len(cov['commands'])
if isinstance(cov.get('qualificationGates'), list):
    R['gate_milestones'] = dict(collections.Counter(g.get('milestone') for g in cov['qualificationGates']))

# every named owner module must be an inventory path
inv = json.load(open(os.path.join(ROOT, 'docs/v2/architecture/repository-file-inventory.v1.json'), encoding='utf-8'))
paths = {f['path'] for f in inv['files']}
missing_owner = set()
def owners(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('mainOwner', 'mainOwners', 'owners', 'owner', 'modules', 'verificationOwner'):
                for x in ([v] if isinstance(v, str) else (v if isinstance(v, list) else [])):
                    if isinstance(x, str) and ('/' in x) and x not in paths:
                        missing_owner.add(x)
            owners(v)
    elif isinstance(o, list):
        for v in o:
            owners(v)
owners(cov)
R['coverage_owner_paths_not_in_inventory'] = sorted(missing_owner)

print(json.dumps(R, indent=1)[:6000])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeH.json', 'w'), indent=1)
