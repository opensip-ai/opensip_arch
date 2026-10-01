"""Build the X12-0 contract successor record: the one PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]
string, widened by law X12 r3 item 7 (RF-2), in both selected copies of the native reference model.
Run with python3 -I -B from any directory. Deterministic: rerunning reproduces the same bytes."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
D = M + 'config-remedy-x12-0/'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
# The frozen v2 source, and the selected reference that capability-totality-reference-selection-v1
# made current ("Current selected native reference becomes reference/native_evidence_model.py").
MODELS = [
    'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py',
]
LINE = 1158
BEFORE = ('    "CONFIG.INVALID": "the configured capability selection is invalid: name a registered capability id'
          ' from the native capability matrix, and state at most one row per (capabilityId, languageMode,'
          ' workspaceRoot)",')
REMEDY = ('the configured capability or policy selection is invalid: for capabilities, name a registered'
          ' capability id from the native capability matrix, and state at most one row per (capabilityId,'
          ' languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly'
          ' as name:version, and supply no policy document of your own or from a third party')
AFTER = '    "CONFIG.INVALID": ' + json.dumps(REMEDY) + ','
overrides, parents = [], []
for path in MODELS:
    parent = pin(path); parents.append(parent)
    lines = (A / path).read_bytes().decode('utf-8').splitlines()
    assert lines[LINE - 1] == BEFORE, path
    assert sum('"CONFIG.INVALID": "' in line for line in lines) == 1, path
    overrides.append({'parent': parent, 'selector': {'line': LINE}, 'before': BEFORE, 'after': AFTER})
EVIDENCE = ['evidence/build_x12_0.py', 'evidence/check_remedy.py', 'evidence/verify_scratch.py']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED X12-0 remedy-text contract successor (law X12 r3 item 7, RF-2): the one PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"] string, widened in the frozen v2 native reference model and in the selected capability-totality reference copy so it stays true for the three external-configuration capability keys and for X12 rows 1, 2 and 3a; text-only, no code, class, exit, route, schema, registry, generated code, inventory or product change; exact frozen candidate requires actual independent review and root assent.',
    'parents': sorted(parents, key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': sorted([pin(D + 'README.md')] + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'successor.json')]
           + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path'])}
(A / M / 'config-remedy-x12-0-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'overrides': len(overrides), 'parents': len(parents), 'remedyChars': len(REMEDY)}))
