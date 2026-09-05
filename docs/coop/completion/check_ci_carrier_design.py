"""Reference CI carrier validation. Does not run GitHub Actions or qualify G16."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parent
schema = json.loads((BASE / 'ci-ownership-schema.v1.json').read_text())
validator = Draft202012Validator(schema)
example = json.loads((BASE / 'ci-ownership-example.v1.json').read_text())

def admit(x, observed):
    if list(validator.iter_errors(x)):
        return 'REFUSE'
    # Observations are independently read from pinned Git trees and verified
    # manifests by the production selector; fixtures supply those observations.
    if x['baseTree'] != observed['baseTree'] or x['headTree'] != observed['headTree']:
        return 'REFUSE'
    if any(x[k] != observed[k] for k in ['previousRecordDigest', 'currentRecordDigest', 'fixtureDomainBasisDigest', 'consumers', 'roles', 'platforms']):
        return 'REFUSE'
    for when in ['previous', 'current']:
        if set(x[when + 'Units']) != set(observed[when + 'Units']):
            return 'REFUSE'
        if set(x[when + 'Owners']) != set(x[when + 'Units']):
            return 'REFUSE'
        if x[when + 'Owners'] != observed[when + 'Owners']:
            return 'REFUSE'
        if set(x[when + 'Components']) != set(observed[when + 'Components']):
            return 'REFUSE'
    components = set(x['previousComponents']) | set(x['currentComponents'])
    if any(set(x[k]) != components for k in ['dependencies', 'roles', 'platforms', 'dependencyManifestDigests']):
        return 'REFUSE'
    if x['dependencyManifestDigests'] != observed['dependencyManifestDigests'] or x['dependencies'] != observed['dependencies']:
        return 'REFUSE'
    known = components | set(x['consumers'])
    if any(not v or not set(v) <= known for k in ['previousOwners', 'currentOwners'] for v in x[k].values()):
        return 'REFUSE'
    if any(not set(v) <= components for k in ['dependencies', 'consumers'] for v in x[k].values()):
        return 'REFUSE'
    if any(not v for v in x['platforms'].values()):
        return 'REFUSE'
    changed = set(observed['changedUnits'])
    if x['previousRecordDigest'] != x['currentRecordDigest']:
        changed |= set(x['previousUnits']) | set(x['currentUnits'])
    if any(len(x['currentOwners'].get(u, x['previousOwners'].get(u, []))) > 1 for u in changed):
        return 'SELECT-ALL'
    return 'ADMIT-TO-SELECTOR'

def run():
    observed = copy.deepcopy(example)
    observed['changedUnits'] = ['core/main.rs']
    cases = [('valid', example, observed, 'ADMIT-TO-SELECTOR')]
    def case(name, edit, expected='REFUSE', observed_edit=None):
        x = copy.deepcopy(example)
        edit(x)
        obs = copy.deepcopy(observed)
        if observed_edit:
            observed_edit(obs)
        cases.append((name, x, obs, expected))
    first = example['currentComponents'][0]
    case('missing-owner', lambda x: x['currentOwners'].pop('core/main.rs'))
    case('omitted-unit-and-owner', lambda x: (x['currentOwners'].pop('core/main.rs'), x['currentUnits'].remove('core/main.rs')))
    case('missing-dependency', lambda x: x['dependencies'].pop(first))
    case('changed-dependency', lambda x: x['dependencies'][first].append(first))
    case('missing-role', lambda x: x['roles'].pop(first))
    case('missing-platform-axis', lambda x: x['platforms'].pop(first))
    case('empty-platform', lambda x: x['platforms'].__setitem__(first, []))
    case('wrong-predicate', lambda x: x.__setitem__('multiComponentPredicate', 3))
    case('wrong-manifest', lambda x: x['dependencyManifestDigests'].__setitem__(first, 'd'*64))
    case('wrong-base', lambda x: x.__setitem__('baseTree', 'e'*40))
    case('unknown-field', lambda x: x.__setitem__('trustMe', True))
    case('label-is-not-uuid', lambda x: x['currentComponents'].__setitem__(0, 'opensip.typescript'))
    case('conflict', lambda x: x['currentOwners']['core/main.rs'].append(first), 'SELECT-ALL',
         lambda obs: obs['currentOwners']['core/main.rs'].append(first))
    case('conflict-plus-missing', lambda x: (x['currentOwners']['core/main.rs'].append(first), x['dependencies'].pop(first)))
    case('wrong-corpus-basis', lambda x: x.__setitem__('fixtureDomainBasisDigest', 'f'*64))
    case('missing-corpus-basis', lambda x: x.pop('fixtureDomainBasisDigest'))
    case('consumer-omission', lambda x: x['consumers'].pop('LOCK'))
    case('changed-consumer', lambda x: x['consumers']['LOCK'].append(first))
    case('forged-roleless', lambda x: x['roles'].__setitem__(first, []))
    case('platform-silently-removed', lambda x: x['platforms'][first].pop())
    case('forged-exclusive-owner', lambda x: x['currentOwners'].__setitem__('core/main.rs', [first]))
    case('forged-previous-owner', lambda x: x['previousOwners'].__setitem__('core/main.rs', [first]))
    case('forged-complete-conflict', lambda x: x['currentOwners']['core/main.rs'].append(first))
    results = [{'id': n, 'input': x, 'trustedObservation': obs, 'expected': want, 'observed': admit(x, obs)} for n, x, obs, want in cases]
    assert all(r['expected'] == r['observed'] for r in results)
    files = [Path(__file__), BASE / 'ci-ownership-schema.v1.json', BASE / 'ci-ownership-example.v1.json']
    report = {'productQualification': False, 'count': len(results), 'passed': len(results), 'sourcePins': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}, 'trustedObservation': observed, 'results': results}
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, default=BASE / 'ci-carrier-design-report.v1.json')
    parser.parse_args().report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'count': len(results), 'passed': len(results)}))

if __name__ == '__main__':
    run()
