"""StepTermination admission at every identified boundary over the byte-verified BASELINE copy."""
import importlib.util, json
from pathlib import Path

HERE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/probes')
spec = importlib.util.spec_from_file_location('boundaries', HERE / 'boundaries.py')
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)
record = B.run('baseline', 'p01-baseline-boundaries.json')
print(json.dumps({'summary': record['summary'], 'producerCounts': record['producers']['counts'],
                  'illegalOrAdvisoryEmissions': record['producers']['illegalOrAdvisoryEmissions'],
                  'publicTerminationDroppedInputCodes': len(record['producers']['publicTerminationDroppedInputCodes']),
                  'fixtureScan': {'scanned': record['fixtureScan']['terminationShapedObjects'],
                                  'flagged': record['fixtureScan']['flagged']},
                  'digestConsequence': record['digestConsequence']}, indent=2))
# Probe validity: controls must discriminate, otherwise the observation is not usable.
s = record['summary']
if s['lawfulRefusedAt'] or s['existingRefusalAdmittedAt']:
    raise SystemExit(1)
