import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, DC, load, jload, Recorder

S = ROOT / 'm1-config-disclosure-subject-01'
pins = {p['role']: Path(p['path']) for p in jload(S / 'input-pins.json')['files']}
ref = load(pins['canonical'], 'canonical_owner')
identity = jload(pins['identity'])
schema = jload(S / 'configuration-disclosure.schema.json')
policy = jload(S / 'field-policy.json')
disc = load(S / 'disclosure.py', 'disclosure_subject')
R = Recorder('m1-config-disclosure-subject-01')


def digest(c):
    return hashlib.sha256(ref.canonical(c)).hexdigest()


def project(c, plan_id='plan2:' + '1' * 64, plan=None):
    return disc.project(plan_id, plan or {'resolvedConfigDigest': digest(c)}, c, policy, ref, identity, schema)


def base():
    return {'analysis': {'profileId': 'p', 'capabilities': ['a'], 'budget': {'unit': 'work-units', 'limit': 5}},
            'components': {}, 'discovery': {}, 'policy': {}, 'evidence': {}}


# Control: actual pinned resolver output feeds the projection with equal digest
model = load(pins['configuration-model'], 'config_model_owner')
layer = {'schemaVersion': 2, 'analysis': {'profileId': 'secret.profile', 'capabilities': ['zeta', 'alpha'], 'budget': {'unit': 'work-units', 'limit': 77}},
         'components': {'allowedScopes': ['project', 'global']}, 'discovery': {'entryPoints': ['src/secret-main.ts']}}
o = R.outcome(lambda: model.resolve({'project': json.dumps(layer).encode()}, {'profiles': ['secret.profile'], 'capabilities': ['zeta', 'alpha'], 'packs': []}))
if 'returned' in o:
    res = o['returned']
    out = R.outcome(lambda: project(res['semantic'], plan={'resolvedConfigDigest': res['resolvedConfigDigest']}))
    ok = 'returned' in out and out['returned']['source']['resolvedConfigDigest'] == res['resolvedConfigDigest'] and b'secret' not in ref.canonical(out['returned'])
    R.record('CFG-C1', 'control-valid', 'pinned resolver semantic output + its resolvedConfigDigest project without leaking profile/path', out, ok)
    R.record('CFG-C1b', 'derivation', 'resolver winning-layer provenance exists but is not accepted by project()', res['provenance'], True)
else:
    R.record('CFG-C1', 'control-valid', 'pinned resolver runs', o, False, 'resolver layer fixture refused; see observed')

# Control: current-settings fallback impossible - digest mismatch refuses
c = base(); plan = {'resolvedConfigDigest': digest(c)}; c2 = copy.deepcopy(c); c2['analysis']['budget']['limit'] = 6
o = R.outcome(lambda: project(c2, plan=plan))
R.record('CFG-C2', 'control-invalid', 'today\'s changed configuration against an older Plan digest refuses', o, 'SOURCE-DIGEST' in o.get('message', ''))

# Noninterference sweep over every redacted slot with equal cardinalities
variants = []
for prof, caps, req, ep, packs in itertools.product(['p', 'q.very.long.profile'], [['a'], ['zz']],
        [[{'stableId': '00000000-0000-0000-0000-000000000001', 'version': '1.0.0'}],
         [{'stableId': 'ffffffff-0000-0000-0000-000000000001', 'versionConstraint': {'min': '1.0.0', 'max': '2.0.0', 'includeMin': True, 'includeMax': False}}]],
        [['x'], ['a/very/long/private/path.ts']], [['k'], ['secret.pack']]):
    c = base(); c['analysis']['profileId'] = prof; c['analysis']['capabilities'] = caps
    c['components'] = {'request': req}; c['discovery'] = {'entryPoints': ep}; c['policy'] = {'packIds': packs}
    out = project(c); del out['source']['resolvedConfigDigest']; variants.append(ref.canonical(out))
R.record('CFG-C3', 'control-valid', '32 variants differing only in redacted values/lengths/shapes (version vs versionConstraint) produce byte-identical carriers except the source digest',
         {'variants': len(variants), 'distinct': len(set(variants))}, len(set(variants)) == 1)

# Control: missing / empty / present distinct
c = base(); rows = []
rows.append(project(c)['fields']['policy.waiverIds'])
c['policy']['waiverIds'] = []; rows.append(project(c)['fields']['policy.waiverIds'])
R.record('CFG-C4', 'control-valid', 'not-present vs redacted itemCount 0 are distinct', rows, rows[0]['state'] == 'not-present' and rows[1].get('itemCount') == 0)

# F: PlanId not bound to the admitted Plan
c = base()
outs = [project(c, plan_id='plan2:' + d * 64)['source']['planId'] for d in '1a']
R.record('CFG-F1', 'finding', 'projection binds planId to the admitted Plan (recompute or explicit host-asserted provenance)', outs, len(set(outs)) == 2,
         'any syntactically valid plan2 id is accepted for the same Plan dict; the Plan dict itself is not validated (only resolvedConfigDigest read)')
o = R.outcome(lambda: project(c, plan={'resolvedConfigDigest': digest(c), 'unrelated': True}))
R.record('CFG-F1b', 'finding', 'admitted_plan must be a Plan', o, 'returned' in o)

# F: carrier has no verifiedInDocument/hostAsserted provenance like sibling report carriers
report = jload(ROOT / 'm1-report-projection-subject-07/report-projection.schema.json')
R.record('CFG-F2', 'finding', 'disclosure carrier states host-asserted source association (report owner provenance convention)',
         {'disclosureTopLevel': sorted(schema['properties']), 'ruleCatalogProvenance': report['$defs']['RuleCatalogV1']['properties']['provenance']},
         'provenance' not in schema['properties'])

# F: schema itemCount lower bound ignores owner minItems for components.request
rows = schema['properties']['fields']['properties']['components.request']
R.record('CFG-F3', 'finding', 'redacted itemCount bounds equal owner array bounds (request minItems 1)', rows,
         json.dumps(rows).find('"minimum": 0') >= 0, 'minor: schema admits itemCount 0 for a field whose owner requires minItems 1')

# Derivation: identity v2 and v3 semantic-configuration equal (resolver reads v2)
i2 = jload(DC / 'foundation/identity-schemas.v2.json')
R.record('CFG-D1', 'derivation', 'resolver-validated v2 semantic-configuration equals pinned v3 selector', None,
         i2['$defs']['semantic-configuration'] == identity['$defs']['semantic-configuration'])
R.dump(Path(__file__).resolve().parent / 'config-results.json')
