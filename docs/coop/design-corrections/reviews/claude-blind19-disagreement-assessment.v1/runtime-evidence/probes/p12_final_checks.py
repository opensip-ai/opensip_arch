"""P12: MutationReplayScopeV1 id law, full contract section 5, and whether the Run actually
has an external import target the query artifact omitted."""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
CB = '/tmp/opensip-design-corrections/consumer-b.v19'
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'

out = {}

# --- MutationReplayScopeV1 id law
rep = json.load(open(os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json')))
common = json.load(open(os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json')))


def find_def(doc, name):
    for p, o in [(k, v) for k, v in (doc.get('$defs') or {}).items()]:
        if p == name:
            return o
    return None


mrs = find_def(rep, 'MutationReplayScopeV1') or find_def(common, 'MutationReplayScopeV1')
print('=== MutationReplayScopeV1 (evaluator3)')
print(json.dumps(mrs, indent=1)[:1600] if mrs else 'NOT FOUND in repair/common evaluator3 $defs')
out['mutationReplayScopeV1'] = mrs

# search every schema for the definition
if mrs is None:
    base = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas')
    for dp, _d, fs in os.walk(base):
        for n in fs:
            if not n.endswith('.json'):
                continue
            doc = json.load(open(os.path.join(dp, n)))
            d = find_def(doc, 'MutationReplayScopeV1')
            if d:
                rel = os.path.relpath(os.path.join(dp, n), ROOT32)
                print('found in', rel)
                print(json.dumps(d, indent=1)[:1600])
                out['mutationReplayScopeV1'] = {'file': rel, 'def': d}

rid_pat = (common.get('$defs') or {}).get('RequestId', {}).get('pattern')
sid_def = (common.get('$defs') or {}).get('StepId')
print('\nRequestId pattern:', rid_pat)
print('StepId def       :', json.dumps(sid_def)[:300])
mk = json.load(open(os.path.join(CB, 'output/vectors/mutation-keys.json')))
pre = mk['genericMutation']['preimage']
checks = {'requestId': pre.get('requestId'), 'stepId': pre.get('stepId'),
          'requestIdMatchesCommonPattern': bool(re.match(rid_pat, str(pre.get('requestId')))) if rid_pat else None,
          'stepIdType': type(pre.get('stepId')).__name__,
          'commonStepIdDef': sid_def}
print('\n=== mutation-keys genericMutation preimage ids')
print(json.dumps(checks, indent=1))
out['mutationPreimageIdChecks'] = checks

# --- full contract section 5
CONTRACT = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md')
lines = open(CONTRACT, encoding='utf-8', errors='ignore').read().split('\n')
i = next(i for i, l in enumerate(lines) if l.startswith('## 5. Cursor'))
j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
sec = '\n'.join(lines[i:j])
print('\n=== contract section 5 verbatim')
print(sec)
out['contractSection5Full'] = sec

# --- does the typescript Run have an external import target?
ex = json.load(open(os.path.join(RB, 'typescript', 'exact-export.json')))
bl = {}
for d, b in ex['blobs'].items():
    try:
        bl[d] = base64.b64decode(b) if isinstance(b, str) else bytes(b)
    except Exception:
        pass
objects = {k: (v['domain'], v['record']) for k, v in ex['objectTable'].items()}
imports = []
for oid, rec in objects.items():
    if rec[0] != 'fact' or rec[1].get('relation') != 'imports':
        continue
    try:
        p = json.loads(bl[rec[1]['payloadDigest']])
    except Exception:
        continue
    imports.append({'factId': oid[:24], 'payload': p})
print('\n=== typescript imports facts:', len(imports))
for f in imports:
    print('   ', json.dumps(f['payload'])[:260])
out['typescriptImportFacts'] = imports

json.dump(out, open(os.path.join(HERE, 'p12-final-checks.json'), 'w'), indent=2, default=str)
print('\nWROTE p12-final-checks.json')
