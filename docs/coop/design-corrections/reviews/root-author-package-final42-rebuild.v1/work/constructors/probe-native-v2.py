"""AUTHOR evidence probe: native-v2 construction properties of every positive export, read through the owner.

Portable: --source (successor source root), --package (package root holding the export groups), --out (fresh JSON path).
For each positive Run (checkpoint3, normalized-examples6, rust-selection-examples1 and the two ADMIT binding controls):
  * opens the exact export with the owner's structural open_run_closure (no admission is re-implemented here);
  * S1  every execution-plan stage's outputSchemaDigest is the producer closure's registered member digest;
  * S2  every clone fact in the Run's views names a level/specification that its INTERPRETING closure (universe row
        languageVersionBinding.normalizationClosure) maps, and both the map and the specification are tree members;
  * S4  every ExecutionInputsV1 native coverage account has targetUniverse null;
  * U-4b the retained UnitMembershipV1 equals the owner's assign_membership over the retained units and snapshot paths,
        and its units are compared with the owner's discover_units over the snapshot's marker files.
This is author self-consistency evidence over owner functions; it is not an independent implementation or acceptance.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys, tomllib

p = argparse.ArgumentParser()
p.add_argument('--source', required=True, type=Path)
p.add_argument('--package', required=True, type=Path)
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()
if a.out.exists():
    raise SystemExit('--out exists')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = a.source / 'docs/coop/design-corrections/foundation'
M = load('probe_identity3', F / 'identity-model.v3.py')
N = M.native_admission()
T = load('probe_transport', a.package / 'check-export.v4.py')
ENUM_SCHEMA = hashlib.sha256((F / 'enumeration-plan.schema.v1.json').read_bytes()).hexdigest()
MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')
TARGETS = [('checkpoint3', None), ('normalized-examples6', None), ('rust-selection-examples1', None),
           ('binding-controls', {'ts-lawful-default', 'ts-lawful-explicit-selection'})]


def check_run(group, claim):
    raw = (a.package / group / claim['path']).read_bytes()
    objects, blobs = T.decode_store(raw, M)
    run = objects[claim['runId']][1]
    rid, owner = M.open_run_closure(run, objects, blobs)
    faults, notes = [], {}
    parse = lambda d: json.loads(blobs[d])
    plan = objects[run['planId']][1]
    # S1
    seal = objects[run['evaluationSealId']][1]
    execution = objects[seal['executionPlanId']][1]
    stages = []
    for stage in execution['stages']:
        spec = parse(stage['stageSpecDigest'])
        closure = objects[spec['producerClosure']][1]
        path = 'opensip-interface/stage-output/' + spec['operation'] + '.schema.json'
        member = next((r for r in closure['tree'] if r['path'] == path), None)
        ok = member is not None and member['sha256'] == spec['outputSchemaDigest']
        stages.append({'operation': spec['operation'], 'registered': ok})
        if not ok:
            faults.append('S1:' + spec['operation'])
    notes['stages'] = stages
    # S2
    evidence = objects[run['evidenceId']][1]
    clones = []
    for vid in evidence['viewIds']:
        for fid in objects[vid][1]['facts']:
            fact = objects[fid][1]
            if fact['relation'] != 'clones':
                continue
            payload = parse(fact['payloadDigest'])
            domain, universe, row, _retained = owner['nativeUniverses'][fact['sourceUniverse']]
            ref = universe
            for step in row['contextField']:
                ref = ref[step]
            context = owner['nativeContexts'][ref.removeprefix('sha256:')][1]
            interp = context
            for step in row['languageVersionBinding']['normalizationClosure']['path']:
                interp = interp[step]
            tree = {r['path']: r['sha256'] for r in objects[interp][1]['tree']}
            map_digest = tree.get(M.NORMALIZATION_MAP_PATH)
            levels = {r['level']: r['specificationDigest'] for r in parse(map_digest)['levels']} if map_digest else {}
            ok = (map_digest is not None and levels.get(payload['normalisationLevel']) == payload['normalisationVersion']
                  and payload['normalisationVersion'] in tree.values())
            clones.append({'fact': fid, 'universeDomain': domain, 'interpretingClosure': interp,
                           'closureKind': objects[interp][1]['kind'], 'level': payload['normalisationLevel'],
                           'mapMember': map_digest is not None, 'mapped': ok})
            if not ok:
                faults.append('S2:' + fid)
    notes['clones'] = clones
    # S4
    proof = objects[seal['proofBundleId']][1]
    ei = parse(proof['executionInputsDigest'])
    non_null = [acc for acc in ei['nativeCoverageAccounts'] if acc['targetUniverse'] is not None]
    notes['accounts'] = len(ei['nativeCoverageAccounts'])
    if non_null:
        faults.append('S4:%d' % len(non_null))
    # U-4b
    spec = parse(plan['analysisSpecDigest'])
    enumeration = parse(next(r['payloadDigest'] for r in spec['parameters'] if r['schemaDigest'] == ENUM_SCHEMA))
    membership = parse(enumeration['membershipDigest'])
    snapshot = objects[run['snapshotId']][1]
    paths = [r['path'] for r in snapshot['sourceInventory']]
    derived = N.assign_membership(membership['units'], paths)
    rows_agree = M.C.equal_typed(derived, membership)
    if not rows_agree:
        faults.append('U-4b:assign_membership')
    markers = {}
    for r in snapshot['sourceInventory']:
        name = r['path'].rsplit('/', 1)[-1]
        if name not in MARKERS:
            continue
        info = {'sha256': r['sha256']}
        body = blobs[r['sha256']]
        if name == 'Cargo.toml':
            info['isCargoWorkspace'] = 'workspace' in tomllib.loads(body.decode())
        if name in ('tsconfig.json', 'jsconfig.json'):
            info['allowJs'] = bool(json.loads(body).get('compilerOptions', {}).get('allowJs', False))
        markers[r['path']] = info
    discovered = N.discover_units(markers)
    units_agree = discovered['refused'] is None and M.C.equal_typed(discovered['units'], membership['units'])
    notes['membership'] = {'rows': len(membership['rows']), 'unsupportedFiles': membership['unsupportedFiles'],
                           'assignMembershipAgrees': rows_agree, 'discoverUnitsAgrees': units_agree,
                           'retainedUnits': membership['units'], 'ownerDiscoveredUnits': discovered['units']}
    return {'group': group, 'name': claim['name'], 'runId': rid, 'faults': faults, 'unitsVsDiscoveryAgree': units_agree, **notes}


results = []
for group, only in TARGETS:
    for claim in json.loads((a.package / group / 'claims.json').read_text()):
        if only is not None and claim['name'] not in only:
            continue
        try:
            results.append(check_run(group, claim))
        except Exception as exc:  # recorded, never skipped
            results.append({'group': group, 'name': claim['name'], 'faults': ['error:%s:%s' % (type(exc).__name__, str(exc)[:400])]})
out = {'standing': 'Author self-consistency probe over owner functions; not independent implementation or acceptance.',
       'runs': results, 'passed': all(not r['faults'] for r in results),
       'unitsVsDiscoveryDisagreements': [r['name'] for r in results if r.get('unitsVsDiscoveryAgree') is False]}
a.out.write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({'passed': out['passed'], 'runs': [(r['name'], r['faults']) for r in results],
                  'unitsVsDiscoveryDisagreements': out['unitsVsDiscoveryDisagreements']}, indent=1))
raise SystemExit(0 if out['passed'] else 1)
