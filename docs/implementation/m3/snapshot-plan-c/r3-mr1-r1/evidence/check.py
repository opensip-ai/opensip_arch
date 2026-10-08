"""Read-only design schema/byte controls, not owner or product admission."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys

parser = argparse.ArgumentParser()
parser.add_argument('--architecture', type=Path, required=True)
parser.add_argument('--deps', type=Path, required=True)
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
sys.path.insert(0, str(args.deps))
here = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('canonical', args.architecture / 'docs/coop/design-corrections/foundation/canonical.py')
canonical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(canonical)
schema = json.loads((here / 'owner-file-manifest-recipes.schema.json').read_text())
identity = json.loads((args.architecture / 'docs/coop/design-corrections/foundation/identity-schemas.v3.json').read_text())
native = json.loads((args.architecture / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())
for local, original in [('Blob', identity['$defs']['Blob']), ('LogicalPath', identity['$defs']['LogicalPath']), ('SnapshotOwnerFileManifestV1', identity['$defs']['source-inventory']), ('DependencyOwnerFileManifestV1', native['$defs']['DependencyFileManifestV1'])]:
    assert schema['$defs'][local] == original, local
cases = []
file_digest = hashlib.sha256(b'abc').hexdigest()
for source, selector, row, length_key in [('snapshot-member', 'SnapshotOwnerFileManifestV1', {'path':'src/lib.rs', 'sha256':file_digest, 'bytes':3}, 'bytes'), ('dependency-closure-member', 'DependencyOwnerFileManifestV1', {'path':'src/lib.rs', 'contentSha256':file_digest, 'byteLength':3}, 'byteLength')]:
    selected = dict(schema, **{'$ref':'#/$defs/' + selector})
    canonical.validate(selected, [row])
    encoded = canonical.canonical([row])
    vector = {'id':source+'-abc', 'source':source, 'preimage':[row], 'canonicalUtf8':encoded.decode(), 'bytes':len(encoded), 'rawSha256':hashlib.sha256(encoded).hexdigest(), 'expected':'admit-shape-and-byte-recipe-only'}
    if source == 'dependency-closure-member':
        vector['nativeDomainDigest'] = canonical.identity('native.dependency-file-manifest.v1', [row])
        assert vector['nativeDomainDigest'] != vector['rawSha256']
    cases.append(vector)
    malformed = [('duplicate', [row,row]), ('reverse', [dict(row,path='z.rs'),dict(row,path='a.rs')]), ('unknown-member', [dict(row,extra=True)]), ('negative-length', [dict(row, **{length_key:-1})]), ('float-length', [dict(row, **{length_key:3.0})]), ('boolean-length', [dict(row, **{length_key:True})]), ('uint64-overflow', [dict(row, **{length_key:2**64})])]
    for label, value in malformed:
        try:
            canonical.validate(selected, value)
            canonical.canonical(value)
        except (canonical.AdmissionError, canonical.ValidationError) as exc:
            cases.append({'id':source+'-'+label, 'source':source, 'preimage':value, 'expected':'refuse', 'observedType':type(exc).__name__})
        else:
            raise AssertionError(label)
assert cases[0]['rawSha256'] != cases[8]['rawSha256']
report = {'standing':'Design-level exact source schema/custom-order/canonical byte controls only. No actual owner witness, native admission, security library, harness parity or product qualification.', 'cases':cases, 'positiveCases':2, 'negativeCases':14, 'schemaCopiesEqualByValue':4, 'R3Resolved':False, 'productExecuted':False, 'productQualification':False}
target = here / 'evidence/recipe-controls.json'
if args.write:
    target.write_text(json.dumps(report, indent=2)+'\n')
else:
    assert json.loads(target.read_text()) == report
print('Four exact schema copies, two byte vectors and fourteen malformed-row controls pass; no product admission asserted.')
