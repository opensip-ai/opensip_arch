"""P18: re-run every probe under the reference interpreter and capture exact receipts."""
import hashlib, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REF = '/tmp/opensip-architecture-review-env/bin/python'
RT = os.path.dirname(HERE)
os.makedirs(os.path.join(HERE, 'receipts'), exist_ok=True)

PROBES = ['p1_inventory.py', 'p2_accounts.py', 'p3_normative.py', 'p4_records.py',
          'p5_outcomes.py', 'p6_carrier.py', 'p7_cellstate.py', 'p8_candidate_carrier.py',
          'p9_selection_law.py', 'p10_query_mutation.py', 'p11_query_detail.py',
          'p12_final_checks.py', 'p13_corrective_route.py', 'p14_mutation_validate.py',
          'p15_clones.py', 'p16_census.py', 'p17_clones_census.py']

rows = []
for name in PROBES:
    path = os.path.join(HERE, name)
    cmd = [REF, '-I', '-B', path]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=RT, timeout=1800)
    rec = {'probe': name, 'command': cmd, 'cwd': RT, 'exitCode': p.returncode,
           'probeSha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
           'stdout': p.stdout, 'stderr': p.stderr}
    json.dump(rec, open(os.path.join(HERE, 'receipts', name.replace('.py', '.receipt.json')), 'w'), indent=2)
    rows.append({k: rec[k] for k in ('probe', 'command', 'exitCode', 'probeSha256')})
    print(('PASS ' if p.returncode == 0 else 'EXIT%d' % p.returncode), name)

# evidence hashes for every artifact this diagnosis relied on
EV = {
    'manifest': '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json',
    'rootSummary': '/tmp/opensip-design-corrections/root-blind19-final-source32.v1/summary.json',
    'rootTraceSyntaxCode': '/tmp/opensip-design-corrections/root-blind19-execution-disagreement.v1/syntax-code.json',
    'rootTraceSyntaxData': '/tmp/opensip-design-corrections/root-blind19-execution-disagreement.v1/syntax-data.json',
    'execInputsModel': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/foundation/execution_inputs_model.v1.py',
    'execInputsContract': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
    'execInputsSchema': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json',
    'capabilityMatrix': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/native/native-capability-matrix.v2.json',
    'nativeEvidenceContract': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/v2/contracts/product-v1/native-evidence.md',
    'enumerationContract': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/foundation/enumeration-contract.v1.md',
    'queryContract': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
    'graphQuerySchema': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
    'invocationRecordSchema': '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json',
    'consumerQueryArtifact': '/tmp/opensip-design-corrections/consumer-b.v19/output/query/graph-query-reconstruction.json',
    'consumerMutationKeys': '/tmp/opensip-design-corrections/consumer-b.v19/output/vectors/mutation-keys.json',
    'consumerHelperCorrections': '/tmp/opensip-design-corrections/consumer-b.v19/output/helper-corrections.json',
}
for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    EV['export:' + name] = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1/%s/exact-export.json' % name

ev = {}
for k, p in EV.items():
    ev[k] = {'path': p, 'exists': os.path.exists(p),
             'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None,
             'bytes': os.path.getsize(p) if os.path.exists(p) else None}

json.dump({'probeReceipts': rows, 'evidenceHashes': ev},
          open(os.path.join(RT, 'receipts.json'), 'w'), indent=2)
print('\nevidence hashes:', len(ev))
print('WROTE receipts.json')
