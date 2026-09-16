"""Write a checkpoint from a small JSON spec on argv[1]."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checkpoint as CK

spec = json.load(open(sys.argv[1]))
rows = CK.read_status()
CK.mark(rows, spec['executed'], 'executed', artifacts=spec.get('artifacts', []),
        note=spec.get('note', ''))
for i in spec.get('failed', []):
    CK.mark(rows, [i], 'failed', artifacts=spec.get('artifacts', []),
            note=spec.get('failNote', ''))
CK.write_status(rows)
cp = CK.write_checkpoint(spec['phase'], spec['executed'], spec.get('failed', []),
                         spec.get('artifacts', []), spec.get('helperCorrections', []),
                         spec.get('notes', ''), spec.get('extraRequired', []))
print('phase', cp['phase'], 'required', len(cp['requirementIdsRequired']),
      'executed', len(cp['requirementIdsExecuted']),
      'unexecuted', len(cp['requirementIdsUnexecuted']),
      'failed', len(cp['requirementIdsFailed']))
print('unexecuted:', cp['requirementIdsUnexecuted'][:40])
