"""Measure the registry effect of the in-place native-evidence.schemas.v2.json edit (source38 3e37c7b7 -> source39 2d37b810).

Loads identity-model.v3 from the verified copy and asks the owner registry, not a restated list. Writes only
receipts/probes/schema-digest-effect.json."""
import hashlib, importlib.util, json, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39')
F = RT / 'work/source39-pkg/docs/coop/design-corrections/foundation'
spec = importlib.util.spec_from_file_location('p39_identity3', F / 'identity-model.v3.py')
M = importlib.util.module_from_spec(spec)
sys.modules['p39_identity3'] = M
spec.loader.exec_module(M)
OLD, NEW = '3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0', '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043'
v38 = Path('/tmp/opensip-design-corrections/candidate-subject.v38/docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_bytes()
v39 = (F.parent / 'native/native-evidence.schemas.v2.json').read_bytes()
registered = M.registered_schema_documents()
payload_rows = {cls: body.get('document') or sorted({r['document'] for r in body.get('rows', {}).values()})
                for cls, body in M.PAYLOADS['classes'].items()}
native_rows = {cls: doc for cls, doc in payload_rows.items() if 'native/native-evidence.schemas.v2.json' in (doc if isinstance(doc, list) else [doc])}
old_json, new_json = json.loads(v38), json.loads(v39)


def diff_paths(a, b, path='#'):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += [path + '/' + k] if (k not in a or k not in b) else diff_paths(a[k], b[k], path + '/' + k)
        return out
    if isinstance(a, list):
        return [path] if len(a) != len(b) else sum((diff_paths(x, y, path + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [path]


report = {
    'sha38': hashlib.sha256(v38).hexdigest(), 'sha39': hashlib.sha256(v39).hexdigest(),
    'expected': {'sha38': OLD, 'sha39': NEW},
    'registeredContainsSource39Digest': NEW in registered,
    'registeredContainsSource38Digest': OLD in registered,
    'payloadRegistryClassesNamingTheNativeDocument': native_rows,
    'jsonDifferencePaths': diff_paths(old_json, new_json),
    'enumerationPlanParameterRowFromSource38Digest': M.parameter_row_of('62ff499e024b83150fee7ce62c449553a3bc2021e0476975f922cdceef806237'),
    'contractText': 'native-evidence.md:3093-3096 says the registered document bytes are deliberately unchanged and an edit is a schema-document successor with its own re-registration',
}
out = RT / 'receipts/probes/schema-digest-effect.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))
