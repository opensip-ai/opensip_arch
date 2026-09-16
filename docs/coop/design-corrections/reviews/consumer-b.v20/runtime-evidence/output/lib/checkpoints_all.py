"""Write checkpoints/phase-{N}.json for every phase, derived from requirement-status.json,
using the checkpoint schema's OWN required field names and its declared merge rule.

Phases 0-2 already had checkpoints from the earlier stages of this origin; they are
REGENERATED here from the same derived status so no checkpoint can drift from the evidence.
The phase membership comes from requirements.json `phases[].ids`, not from a guess.
"""
import json
import os
import sys

ROOT = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = ROOT + '/output'


def main():
    reqfile = json.load(open(ROOT + '/requirements.json'))
    status = json.load(open(OUT + '/requirement-status.json'))
    schema = reqfile['checkpointSchema']
    helpers = json.load(open(OUT + '/helper-corrections.json'))
    required_fields = schema['requiredFields']
    written, cumulative = [], []
    for ph in reqfile['phases']:
        n, name, ids = ph['n'], ph['name'], ph['ids']
        rows = {rid: status.get(rid, {'status': 'unexecuted'}) for rid in ids}
        cumulative = sorted(set(cumulative) | set(ids))
        doc = {
            'phase': n,
            'phaseName': name,
            'consumerId': 'consumer-b.v20',
            'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
            'requirementIdsRequired': sorted(ids),
            'requirementIdsExecuted': sorted(r for r in ids
                                             if rows[r]['status'] == 'executed'),
            'requirementIdsUnexecuted': sorted(r for r in ids
                                               if rows[r]['status'] == 'unexecuted'),
            'requirementIdsFailed': sorted(r for r in ids
                                           if rows[r]['status'] == 'failed'),
            'requirementIdsFutureQualification': sorted(
                r for r in ids if rows[r]['status'] == 'futureQualification'),
            'artifacts': sorted({json.dumps(rows[r].get('artifact'), default=str)[:240]
                                 for r in ids}),
            'helperCorrections': [h for h in helpers['helperCorrections']],
            'notes': ('derived from requirement-status.json, which is itself derived from '
                      'the artifacts; no row is ticked from a helper pass line'),
            'requirementIdsRequiredCumulative': cumulative,
            'mergeRule': schema['mergeRule'],
        }
        missing = [f for f in required_fields if f not in doc]
        assert not missing, ('checkpoint is missing a declared required field', n, missing)
        with open(OUT + '/checkpoints/phase-%d.json' % n, 'w') as f:
            json.dump(doc, f, indent=1, default=str)
        written.append((n, name, len(ids), len(doc['requirementIdsUnexecuted']),
                        len(doc['requirementIdsFailed'])))
    covered = set()
    for ph in reqfile['phases']:
        covered |= set(ph['ids'])
    uncovered = sorted(set(status) - covered)
    for n, name, tot, un, fail in written:
        print('phase-%-2d %-44s required=%-3d unexecuted=%d failed=%d'
              % (n, name[:44], tot, un, fail))
    print('requirement ids not claimed by any phase: %s' % (uncovered or 'none'))
    bad = [n for n, _, _, un, fail in written if un or fail]
    if bad:
        print('PHASES WITH UNEXECUTED OR FAILED REQUIREMENTS:', bad)
        sys.exit(1)


main()
