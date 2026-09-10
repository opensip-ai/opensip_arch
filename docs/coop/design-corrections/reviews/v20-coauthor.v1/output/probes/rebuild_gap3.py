"""CB-GAP-3 under the CHANGED bytes: rebuild the blind's vector shape and close it.

The root-computed graph cannot be replayed after this correction, because
native-evidence.schemas.v2.json is a CHANGED source and its raw digest is
coverage2.payloadSchemaDigest - so every frozen coverage2 identity in that graph now
refuses at PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT, one guard BEFORE the one under
test. That is an artifact of editing the schema document, not evidence about RC-6, and
reporting the frozen replay as an RC-6 refusal would be false.

So the same SHAPE is rebuilt here from the identity unit's own fixture builder over the
changed bytes: a self-consistent retained Run whose file@enumerated Coverage claims
coverage=complete while its own record says the examined partition was not exhaustive.
"""
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path

B = Path('/tmp/opensip-design-corrections/v20-coauthor.v1/work/docs/coop/design-corrections')
sys.argv = [sys.argv[0]]                       # check-identity parses --report itself
sys.path.insert(0, str(B / 'foundation'))

import contextlib
spec = importlib.util.spec_from_file_location('checkidentity', B / 'foundation/check-identity.py')
CI = importlib.util.module_from_spec(spec)
_own_output = io.StringIO()
with contextlib.redirect_stdout(_own_output):          # its own report line is not my result
    try:
        spec.loader.exec_module(CI)
    except SystemExit:
        pass

M, C, N = CI.M, CI.C, CI.N
out = {'note': __doc__.strip(), 'results': []}


def attempt(fn):
    try:
        return {'result': 'ADMITTED', 'value': fn()}
    except BaseException as exc:                                    # noqa: BLE001
        return {'result': 'REFUSED', 'exception': type(exc).__name__, 'detail': str(exc)}


BUILDS = {'references': dict(resolved=True, has_match=True),
          'file': dict(resolved=True, has_match=True, relation='file'),
          'file@syntax-universe': dict(resolved=True, has_match=True, relation='file',
                                       universe_language='syntax')}
run, objects, blobs = CI.build(**BUILDS['file'])
coverages = {}
for key, (dom, desc) in objects.items():
    if dom != 'coverage':
        continue
    entry = C.parse(blobs[desc['payloadDigest']])['entry']
    coverages[key] = (entry['relation'], entry['resolution'], entry['coverage'],
                      entry['resolutionCompleteness']['examinedExhaustive'])
out['coveragesInTheRebuiltRun'] = {k: list(v) for k, v in coverages.items()}


def close_with(label, mutate):
    run, objects, blobs = CI.build(**BUILDS[label])
    key = next(k for k, (d, v) in objects.items() if d == 'coverage')
    coverage = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[coverage['payloadDigest']])
    mutate(payload)
    coverage['payloadDigest'] = CI.put_blob(blobs, payload)
    CI.rekey(objects, key, coverage, run)
    CI.resync_witness(objects, blobs, run)
    return M.close_run(run, objects, blobs)


for label in BUILDS:
    row = {'build': label}
    _r, _o, _b = CI.build(**BUILDS[label])
    _e = C.parse(_b[next(v for k, (d, v) in _o.items() if d == 'coverage')['payloadDigest']])['entry']
    row['entry'] = {k: _e[k] for k in ('relation', 'resolution', 'coverage')}
    row['entry']['examinedExhaustive'] = _e['resolutionCompleteness']['examinedExhaustive']
    row['entry']['state'] = _e['resolutionCompleteness']['state']
    row['positiveControl'] = attempt(lambda l=label: close_with(l, lambda p: None))
    row['contradictoryEntry'] = attempt(lambda l=label: close_with(
        l, lambda p: p['entry']['resolutionCompleteness'].update(examinedExhaustive=False)))
    if row['contradictoryEntry']['result'] == 'REFUSED':
        row['rc6IsTheNamedReason'] = 'RC-6' in row['contradictoryEntry']['detail']
    out['results'].append(row)

print(json.dumps(out, indent=1, sort_keys=True))
