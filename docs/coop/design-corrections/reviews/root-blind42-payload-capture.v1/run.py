"""Capture owning schema/CBOR/buffer results on exact independent payload vectors.

This is scoped ANALYZING-entry evidence, not Plan/Run admission, post-terminal
capture, TypeScript handshake qualification, or a blind acceptance decision.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import shutil

B = Path('/tmp/opensip-design-corrections')
L = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O = Path(__file__).parent
C = B / 'consumer-b.v24-source42.v3'
S = B / 'candidate-subject.v42'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((C / 'process-completion.json').read_bytes())['exitCode'] == 0
assert (L / C.name / 'final-public-artifact-manifest.json').is_file()
manifest = L / 'candidate-subject.v42.json'
assert H(manifest) == 'f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307'
mf = json.loads(manifest.read_bytes())
for row in mf['files']:
    p = S / row['path']
    assert H(p) == row['sha256'] and p.stat().st_size == row['bytes']
model = S / 'docs/coop/design-corrections/foundation/provider_attribution_return_model.v2.py'
spec = importlib.util.spec_from_file_location('root_payload_owner42', model)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
vectors = C / 'output/traces/payload-vectors.json'
raw_hash = H(vectors)
d = json.loads(vectors.read_bytes())
results = []
for v in d['vectors']:
    payload = v['payload']
    neg = v['negotiation']['helloCarriesToken'] and v['negotiation']['helloAckCarriesToken']
    row = {'id': v['id'], 'class': v['class'], 'group': v['group'], 'negotiated': neg,
           'consumerObservation': v['observed']['result'], 'consumerFirstRefusal': v['observed']['firstRefusal']}
    if neg:
        try:
            M.validate_schema(M.BATCH_SCHEMA, copy.deepcopy(payload))
            row['owningV3Schema'] = 'ADMIT'
        except Exception as exc:
            row.update(owningV3Schema='REFUSE', schemaReason=str(exc))
    else:
        row['owningV3Schema'] = 'NOT-APPLICABLE-UNNEGOTIATED'
    cbors = []
    for i, candidate in enumerate(payload.get('candidates', []) if isinstance(payload, dict) else []):
        if not isinstance(candidate, dict):
            cbors.append({'index': i, 'outcome': 'NOT-OBJECT'})
            continue
        try:
            M.verify_candidate_cbor(copy.deepcopy(candidate))
            cbors.append({'index': i, 'outcome': 'EXACT-CBOR'})
        except Exception as exc:
            cbors.append({'index': i, 'outcome': 'REFUSE', 'key': getattr(exc, 'key', None), 'reason': str(exc)})
    row['candidateByteChecks'] = cbors
    try:
        row['ownerBufferResult'] = M.buffer_fact_batch_occupancy(
            copy.deepcopy(payload), negotiated_tokens=[M.TOKEN] if neg else [],
            dispatch=copy.deepcopy(v['observed']['dispatch']))
        row['ownerBufferOutcome'] = 'RETURNED'
    except Exception as exc:
        row.update(ownerBufferOutcome='REFUSE', bufferKey=getattr(exc, 'key', None), bufferReason=str(exc))
    results.append(row)
assert H(vectors) == raw_hash
valid_v3 = [r for r in results if r['class'] == 'valid' and r['negotiated']]
passed = all(r['owningV3Schema'] == 'ADMIT' and r['ownerBufferOutcome'] == 'RETURNED'
             and r['ownerBufferResult']['status'] == 'buffered'
             and all(c['outcome'] == 'EXACT-CBOR' for c in r['candidateByteChecks']) for r in valid_v3)
report = {'standing': 'Exact independent vector data; only owner V3 schema, exact CBOR re-encoding and ANALYZING buffer entry captured. No consumer helper imported, bytes repaired, identity reminted or dispatch filled. Buffer owns fewer checks than full provider admission; differing negative boundaries are not automatically defects. Unnegotiated buffer omission is not historical V2 payload admission. No Plan/Run/anchor/post-terminal/handshake qualification or root blind assent.',
          'sourceManifestSha256': H(manifest), 'vectorsSha256': raw_hash, 'ownerModelSha256': H(model),
          'vectors': len(results), 'claimedValidNegotiatedV3': len(valid_v3),
          'allClaimedValidNegotiatedV3PassScopedOwner': passed, 'rows': results}
(O / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
shutil.copytree(O, L / O.name)
print(json.dumps({k: v for k, v in report.items() if k != 'rows'}))
