"""Reproduce the three BLIND8 gaps against MY copy of the accepted19 reference.

Inputs are the root-captured object graphs and the root-captured analysis-spec from
/tmp/opensip-design-corrections/codex-post-reset.v1/blind8-gap-reproduction.v1 - I do not
re-run the blind consumer's own reconstruction, and nothing here reads its session.

Usage: reproduce.py [<base>]   base defaults to my work copy's design-corrections dir.
"""
import base64
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

KIT = Path('/tmp/opensip-design-corrections/codex-post-reset.v1/blind8-gap-reproduction.v1')
BASE = Path(sys.argv[1] if len(sys.argv) > 1 else
            '/tmp/opensip-design-corrections/v20-coauthor.v1/work/docs/coop/design-corrections')


def module(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = module('probe_identity', BASE / 'foundation/identity-model.py')
W = module('probe_workflow', BASE / 'workflows/workflows_model.v1.py')
N = module('probe_native', BASE / 'native/native_evidence_model.v2.py')


def load_graph(name):
    g = json.loads((KIT / name).read_text())
    blobs = {h: base64.b64decode(b) for h, b in g['blobs'].items()}
    for h, b in blobs.items():
        assert hashlib.sha256(b).hexdigest() == h, 'graph blob digest mismatch ' + h
    objects = {k: tuple(v) for k, v in g['objects'].items()}
    return g['runId'], objects, blobs


def attempt(fn):
    try:
        return {'result': 'ADMITTED', 'value': fn()}
    except BaseException as exc:                      # noqa: BLE001 - measuring, not handling
        return {'result': 'REFUSED', 'exception': type(exc).__name__, 'detail': str(exc)}


out = {'base': str(BASE), 'results': []}

# ---------------------------------------------------------------- CB-GAP-1
run_id, objects, blobs = load_graph('CB-GAP-1-root-computed-graph.json')
row = {'id': 'CB-GAP-1', 'runId': run_id}
row['retainedClosure'] = attempt(lambda: M.close_run(objects[run_id][1], objects, blobs))
spec_digest = objects[run_id][1]['planId']
plan = objects[spec_digest][1]
spec = json.loads(blobs[plan['analysisSpecDigest']])
row['specParameters'] = spec['parameters']
SCOPE_A = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": []}
SCOPE_B = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": ["src/generated/**"]}
row['bindingA'] = attempt(lambda: W.verify_scope_parameter_binding(spec, SCOPE_A))
row['bindingB'] = attempt(lambda: W.verify_scope_parameter_binding(spec, SCOPE_B))
row['prospectiveNativeAdmission'] = attempt(lambda: N.admit_analysis_spec(spec) and 'ADMIT')
out['results'].append(row)

# ---------------------------------------------------------------- CB-GAP-2
spec2 = json.loads((KIT / 'result.json').read_text())['results'][1]['spec']
row = {'id': 'CB-GAP-2', 'spec': spec2}
row['nativeAdmitAnalysisSpec'] = attempt(lambda: N.admit_analysis_spec(spec2) and 'ADMIT')
row['nativeAdmitRequestedCapabilities'] = attempt(
    lambda: N.admit_requested_capabilities(spec2['requestedCapabilities']) and 'ADMIT')
row['foundationSchema'] = attempt(lambda: N.validate_foundation('analysis-spec', spec2) or 'VALID')
out['results'].append(row)

# ---------------------------------------------------------------- CB-GAP-3
run_id, objects, blobs = load_graph('CB-GAP-3-root-computed-graph.json')
row = {'id': 'CB-GAP-3', 'runId': run_id}
row['retainedClosure'] = attempt(lambda: M.close_run(objects[run_id][1], objects, blobs))
entries = []
for key, (dom, desc) in objects.items():
    if dom != 'coverage':
        continue
    payload = json.loads(blobs[desc['payloadDigest']])
    e = payload['entry']
    if e['coverage'] == 'complete' and not e['resolutionCompleteness']['examinedExhaustive']:
        entries.append({'coverageId': key, 'relation': e['relation'], 'resolution': e['resolution'],
                        'coverage': e['coverage'],
                        'resolutionCompleteness': e['resolutionCompleteness']})
        row['producerBijection'] = N.coverage_bijection([dict(e, examinedSubjects=[])], [])
row['contradictoryEntries'] = entries
out['results'].append(row)

print(json.dumps(out, indent=1, sort_keys=True))
