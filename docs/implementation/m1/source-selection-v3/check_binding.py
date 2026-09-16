"""Read-only candidate binding structure check; never creates an approval."""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def pin(path, architecture):
    raw = path.read_bytes()
    return {'path': path.relative_to(architecture).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def structure(architecture, verifier, record, manifest, record_pin, accepted):
    members = verifier.pin_rows(manifest['files'], 'contract subject')
    member_map = {row['path']: row for row in members}
    for row in members:
        verifier.pinned_bytes(architecture, row)
    assert member_map.get(record_pin['path']) == record_pin, 'record is not a subject member'
    candidates = verifier.pin_rows(record['candidates'], 'contract candidates')
    assert {r['path'] for r in candidates} == set(member_map) - {record_pin['path']}, 'candidate coverage'
    for row in candidates:
        assert member_map[row['path']] == row, 'candidate pin differs'
        verifier.pinned_bytes(architecture, row)
    parents = verifier.pin_rows(record['parents'], 'contract parents')
    parent_map = {row['path']: row for row in parents}
    for row in parents:
        assert accepted.get(row['path']) == row, 'parent not accepted'
        assert row['path'] not in member_map, 'parent overwritten'
        verifier.pinned_bytes(architecture, row)
    if 'previousCandidate' in record:
        verifier.pinned_bytes(architecture, record['previousCandidate'])
    seen = set()
    assert type(record['passageOverrides']) is list
    for override in record['passageOverrides']:
        assert set(override) == {'parent', 'selector', 'before', 'after'}, 'override fields'
        parent = override['parent']
        assert parent_map.get(parent['path']) == parent, 'override parent'
        key = (parent['path'], json.dumps(override['selector'], sort_keys=True))
        assert key not in seen, 'duplicate override'
        seen.add(key)
        before, after = override['before'], override['after']
        assert type(before) is str and type(after) is str and after and before != after
        raw = verifier.pinned_bytes(architecture, parent)
        assert verifier.selected_passage(raw, override['selector']) == before, 'passage before differs'
    return len(candidates)


def check(architecture, product):
    original = architecture / 'docs/implementation/m1/source-selection-v2'
    current = architecture / 'docs/implementation/m1/source-selection-v3'
    verifier = module(original / 'reference-tools/verify_design.py', 'binding_verifier')
    source = module(original / 'check_selection.py', 'original_source_checker')
    result = source.check(architecture, product, original)
    load = lambda p: json.loads(p.read_bytes())
    base = load(original / 'base-design-lock.json')
    accepted = {}
    for name in ['sourceManifest', 'applicationManifest']:
        for row in load(architecture / base['approvals'][name]['path'])['files']:
            accepted[row['path']] = {k: row[k] for k in ['path', 'bytes', 'sha256']}
    for binding in base['inventorySuccessors']:
        accepted[binding['candidate']['path']] = binding['candidate']
    for binding in base['contractSuccessors']:
        for row in load(architecture / binding['subjectManifest']['path'])['files']:
            accepted[row['path']] = row
    record = load(current / 'successor.json')
    manifest = load(architecture / 'docs/implementation/m1/source-selection-v3-subject.json')
    record_pin = pin(current / 'successor.json', architecture)
    count = structure(architecture, verifier, record, manifest, record_pin, accepted)
    old = load(original / 'successor.json')
    old_members = {r['path']:r for r in old['candidates']}
    new_members = {r['path']:r for r in record['candidates']}
    assert all(new_members.get(path) == row for path,row in old_members.items())
    assert len(old_members) == 136
    assert record['parents'] == old['parents'] and record['passageOverrides'] == old['passageOverrides']
    try:
        verifier.pin_rows(old['candidates'], 'original unsorted contract candidates')
    except verifier.DesignError as exc:
        assert 'sorted and unique' in str(exc)
    else:
        raise AssertionError('original ordering defect no longer reproduced')
    mutations = []
    value = copy.deepcopy(record); value['candidates'].reverse(); mutations.append(('reverse candidates', value))
    value = copy.deepcopy(record); value['candidates'].append(value['candidates'][-1]); mutations.append(('duplicate candidates', value))
    value = copy.deepcopy(record); value['candidates'].pop(); mutations.append(('missing member', value))
    value = copy.deepcopy(record); value['candidates'][0]['sha256']='0'*64; mutations.append(('different member pin', value))
    value = copy.deepcopy(record); value['parents'].reverse(); mutations.append(('reverse parents', value))
    value = copy.deepcopy(record); value['parents'][0]['sha256']='0'*64; mutations.append(('unaccepted parent', value))
    value = copy.deepcopy(record); value['passageOverrides'][0]['before']='wrong'; mutations.append(('wrong before image', value))
    value = copy.deepcopy(record); value['passageOverrides'].append(value['passageOverrides'][0]); mutations.append(('duplicate override', value))
    for name, value in mutations:
        try:
            structure(architecture, verifier, value, manifest, record_pin, accepted)
        except (AssertionError, verifier.DesignError):
            pass
        else:
            raise AssertionError('mutation survived: '+name)
    return {'passed':True, 'originalSourceCheck':result, 'inheritedSourceMembersUnchanged':136,
            'candidateMembers':count, 'originalOrderingDefectReproduced':True,
            'negativeControlsRefused':[name for name,_ in mutations],
            'approvalFabricated':False, 'productModified':False, 'sourceSelected':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--architecture', required=True, type=Path)
    parser.add_argument('--product', required=True, type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.architecture.resolve(),args.product.resolve()),indent=2))
