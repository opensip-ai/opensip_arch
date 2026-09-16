"""R04b — record the limits that come with this bounded pass, in the same voice as the existing ones."""
import hashlib, json, os

P = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/review.json'
R = json.load(open(P))
NEW = [
    'The newly measured optional selected-U missing-candidate full-Run control is a ROOT-AUTHORED '
    'control that I independently executed and verified; it is not a new independent consumer '
    'implementation, not blind reconstruction, and not provider, compiler or OS qualification. It says '
    'nothing about REQUIRED candidate cells, which still refuse EXECUTION_INPUTS_CANDIDATE_REQUIRED '
    'without an envelope.',
    'extra-candidate-ref-no-outcome refuses with BOTH CANDIDATE_REQUIRED and REF_INVALID_BYTES, so the '
    'first refusal masks the second condition and that control does not isolate a missing matching '
    'outcome or envelope under otherwise valid joins. Recorded as an observed limit; no control was '
    'built to raise a count.',
    'This pass corrected the review RECORD and added exactly one measured scope. It re-ran no unchanged '
    'suite, so every preserved figure carries the standing it had in the source33 pass.',
]
for n in NEW:
    if n not in R['limitations']:
        R['limitations'].append(n)
json.dump(R, open(P, 'w'), indent=1, default=str)
print('limitations:', len(R['limitations']))
print('sha256:', hashlib.sha256(open(P, 'rb').read()).hexdigest())
print('bytes:', os.path.getsize(P))
