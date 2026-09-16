"""Apply the proposed minimal edits to the DISPOSABLE edited copy only and emit the exact diff against baseline.

JSON documents are edited structurally and written only when the untouched document round-trips byte-exactly
through the same serializer, so the diff contains nothing but the proposal. Text edits require exactly one anchor.
Refuses to run when the edited copy already differs from baseline (no double application).
"""
import copy, difflib, hashlib, importlib.util, json
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1')
BL, ED = BASE / 'disposable/baseline', BASE / 'disposable/edited'
DC = 'docs/coop/design-corrections/'
SCHEMAS = [DC + 'workflows/schemas/common.schema.json', DC + 'workflows/schemas/evaluator3/common.schema.json']
CASES = DC + 'workflows/workflow-cases.v1.json'
CHECK = DC + 'workflows/check_workflows.v1.py'
PROSE = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
CHANGED = SCHEMAS + [CASES, CHECK, PROSE]


def sha(b):
    return hashlib.sha256(b).hexdigest()


for rel in CHANGED:
    if (ED / rel).read_bytes() != (BL / rel).read_bytes():
        raise SystemExit('edited copy already differs from baseline: ' + rel)

spec = importlib.util.spec_from_file_location('baseline_workflows1', BL / DC / 'workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)


def serializer(raw):
    for ascii_only in (False, True):
        if (json.dumps(json.loads(raw), indent=2, ensure_ascii=ascii_only) + '\n').encode() == raw:
            return lambda doc, a=ascii_only: (json.dumps(doc, indent=2, ensure_ascii=a) + '\n').encode()
    raise SystemExit('no byte-exact JSON round trip; structural edit would reformat')


def req(field):
    return {'required': [field]}


DESCRIPTION_ADDITION = (
    ' Retained D9 class/code legality (X1, X3, X4 and codeDerivation) is schema-enforced on the same branches:'
    ' faultCause appears only on operational-failed and pairs with errorCode exactly as the fault map'
    ' (D9 codeMaps.faultCauseToErrorCode plus the successor host-invariant member); reasonCodes appear only on'
    ' indeterminate.')

edited_defs = []
for rel in SCHEMAS:
    raw = (BL / rel).read_bytes()
    dump = serializer(raw)
    doc = json.loads(raw)
    st = doc['$defs']['StepTermination']
    branch = {b['if']['properties']['class']['const']: b['then'] for b in st['allOf']
              if 'class' in b.get('if', {}).get('properties', {})}
    assert set(branch) == set(W.EXIT), sorted(branch)
    st['description'] += DESCRIPTION_ADDITION
    branch['success']['not']['anyOf'].append(req('faultCause'))
    branch['policy-failed']['not']['anyOf'] += [req('reasonCodes'), req('faultCause')]
    assert branch['request-rejected']['not'] == req('signal')
    branch['request-rejected']['not'] = {'anyOf': [req('signal'), req('reasonCodes'), req('faultCause')]}
    operational = branch['operational-failed']
    assert 'anyOf' not in operational and 'not' not in operational
    operational['anyOf'] = [{'properties': {'faultCause': {'const': cause}, 'errorCode': {'const': error}}}
                            for cause, error in W.FAULT_TO_ERROR.items()]
    operational['not'] = req('reasonCodes')
    branch['indeterminate']['not']['anyOf'].append(req('faultCause'))
    assert branch['interrupted']['not'] == req('errorCode')
    branch['interrupted']['not'] = {'anyOf': [req('errorCode'), req('reasonCodes'), req('faultCause')]}
    (ED / rel).write_bytes(dump(doc))
    edited_defs.append(st)
assert edited_defs[0] == edited_defs[1]

raw = (BL / CASES).read_bytes()
dump = serializer(raw)
doc = json.loads(raw)
RP = ['COVERAGE.PROVIDER_UNAVAILABLE']
doc['terminationVectors']['reject'] += [
    {'class': 'success', 'faultCause': 'host-io'},
    {'class': 'success', 'faultCause': 'none'},
    {'class': 'policy-failed', 'authority': 'ephemeral', 'reasonCodes': RP},
    {'class': 'policy-failed', 'authority': 'ephemeral', 'faultCause': 'host-io'},
    {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID', 'faultCause': 'host-io'},
    {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID', 'reasonCodes': RP},
    {'class': 'indeterminate', 'reasonCodes': RP, 'faultCause': 'host-io'},
    {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'reasonCodes': RP},
    {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'ledger-busy'},
    {'class': 'operational-failed', 'errorCode': 'SYSTEM.OUTCOME.ILLEGAL_STATE', 'faultCause': 'host-io'},
    {'class': 'interrupted', 'signal': 'SIGINT', 'faultCause': 'host-io'},
    {'class': 'interrupted', 'signal': 'SIGINT', 'reasonCodes': RP},
]
(ED / CASES).write_bytes(dump(doc))


def replace_once(rel, old, new):
    text = (BL / rel).read_text()
    if text.count(old) != 1:
        raise SystemExit('anchor count %d in %s' % (text.count(old), rel))
    (ED / rel).write_text(text.replace(old, new))


replace_once(CHECK,
    "for i, t in enumerate(CASES['terminationVectors']['reject']):\n"
    "    must_invalid(f'termination.reject.{i}', U + 'common#/$defs/StepTermination', t)\n",
    "for i, t in enumerate(CASES['terminationVectors']['reject']):\n"
    "    must_invalid(f'termination.reject.{i}', U + 'common#/$defs/StepTermination', t)\n"
    "# The schema's operational faultCause/errorCode pairs are exactly the host fault map, so the retained D9\n"
    "# codeDerivation cannot drift between the public carrier and the host projection.\n"
    "_OPERATIONAL = next(b['then'] for b in SCHEMAS[U + 'common']['$defs']['StepTermination']['allOf']\n"
    "                    if b['if'].get('properties', {}).get('class', {}).get('const') == 'operational-failed')\n"
    "check('termination.fault-pairs-equal-host-fault-map',\n"
    "      [(r['properties']['faultCause']['const'], r['properties']['errorCode']['const']) for r in _OPERATIONAL['anyOf']]\n"
    "      == list(M.FAULT_TO_ERROR.items()))\n")

replace_once(PROSE,
    "when a Run was committed before the interrupt. `DomainDetailCode` is explanatory\n",
    "when a Run was committed before the interrupt. The same schema enforces the retained\n"
    "D9 cause/code exclusivity: `faultCause` appears only on operational-failed and pairs\n"
    "with its `errorCode` by the fault map, and `reasonCodes` appear only on indeterminate.\n"
    "`DomainDetailCode` is explanatory\n")

diff = []
files = []
for rel in CHANGED:
    a, b = (BL / rel).read_bytes(), (ED / rel).read_bytes()
    files.append({'path': rel, 'baselineSha256': sha(a), 'editedSha256': sha(b)})
    diff += difflib.unified_diff(a.decode().splitlines(keepends=True), b.decode().splitlines(keepends=True),
                                 fromfile='a/' + rel, tofile='b/' + rel, n=3)
patch = ''.join(diff).encode()
(BASE / 'proposed-edits.diff').write_bytes(patch)
record = {'files': files, 'diffSha256': sha(patch), 'diffLines': patch.count(b'\n'),
          'faultPairs': list(W.FAULT_TO_ERROR.items())}
(BASE / 'probes' / 'p02-apply-edits.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
