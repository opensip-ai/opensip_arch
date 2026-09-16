"""P08 — planning layer4 retention on frozen36: the populations are measured from the (35->36 byte-unchanged) planning owners,
not copied from earlier records. Unique repository paths, packages, source-bound coverage mappings, planned recovery/failure
cases and executed cases. Structure is discovered, printed and recorded; nothing is assumed."""
import hashlib, json, os

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v36/receipts'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
m35 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v35.json')))['files']}
m36 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v36.json')))['files']}
R = {}


def shape(o, depth=0):
    if isinstance(o, dict):
        return {k: shape(v, depth + 1) if depth < 1 else (type(v).__name__ + ('[%d]' % len(v) if isinstance(v, (list, dict)) else '')) for k, v in o.items()}
    if isinstance(o, list):
        return 'list[%d]' % len(o)
    return type(o).__name__


for rel in ('docs/v2/architecture/repository-file-inventory.v1.json', 'docs/v2/architecture/implementation-coverage.v1.json',
            'docs/v2/architecture/implementation-planning-sources.v1.json', 'docs/v2/architecture/implementation-normative-inputs.v4.json'):
    d = json.load(open(os.path.join(S36, rel)))
    R.setdefault('owners', {})[rel] = {'sha36': m36[rel], 'unchanged35to36': m35.get(rel) == m36[rel], 'shape': shape(d)}
    print('\n==', rel, 'unchanged 35->36:', m35.get(rel) == m36[rel])
    print(json.dumps(shape(d), indent=1)[:1500])
inv = json.load(open(os.path.join(S36, 'docs/v2/architecture/repository-file-inventory.v1.json')))
paths, packages = set(), set()


def walk(o, parent=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'path' and isinstance(v, str):
                paths.add(v)
            if k in ('package', 'packageName', 'owningPackage') and isinstance(v, str):
                packages.add(v)
            walk(v, k)
    elif isinstance(o, list):
        for v in o:
            if parent in ('paths', 'files') and isinstance(v, str):
                paths.add(v)
            walk(v, parent)


walk(inv)
pk_lists = {k: len(v) for k, v in inv.items() if isinstance(v, (list, dict)) and 'package' in k.lower()}
R['inventory'] = {'uniquePathStrings': len(paths), 'packageNamesReferenced': len(packages), 'packageCollections': pk_lists,
                  'topLevelListLengths': {k: len(v) for k, v in inv.items() if isinstance(v, (list, dict))}}
cov = json.load(open(os.path.join(S36, 'docs/v2/architecture/implementation-coverage.v1.json')))
R['coverage'] = {'topLevelListLengths': {k: len(v) for k, v in cov.items() if isinstance(v, (list, dict))}}
cases = []


def find_cases(o, path='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, list) and any(w in k.lower() for w in ('case', 'failure', 'recovery')):
                cases.append((path + '.' + k, len(v)))
            find_cases(v, path + '.' + k)
    elif isinstance(o, list):
        for n, v in enumerate(o[:3]):
            find_cases(v, '%s[%d]' % (path, n))


for rel in ('docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-planning-sources.v1.json'):
    find_cases(json.load(open(os.path.join(S36, rel))), rel)
R['caseLists'] = cases
print('\ninventory:', R['inventory'])
print('coverage:', R['coverage'])
print('case lists:', cases)
json.dump(R, open(os.path.join(OUT, 'p08-planning-population.json'), 'w'), indent=1, default=str)
print('wrote p08-planning-population.json')
