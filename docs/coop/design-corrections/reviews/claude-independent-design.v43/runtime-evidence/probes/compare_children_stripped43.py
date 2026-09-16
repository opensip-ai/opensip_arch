"""For every evaluator3 child stdout that is not byte-equal to the root source43 reference (or to this reviewer's historical
source42 receipt), report exactly which JSON keys differ, recursively, and whether the stdouts are equal after removing only
path/receipt-location fields. Also records whether codex runner-original-reference-checks equals the root reference-checks.
Writes only receipts/reference-children-stripped.json."""
import hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
MINE = RT / 'receipts/reference/evaluator3'
ROOT = Path('/tmp/opensip-design-corrections/root-source43-final-reference.v1')
MINE42 = Path('/tmp/opensip-design-corrections/claude-independent-design.v42/receipts/reference/evaluator3')
CODEX = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v43')
PATHY = {'ownedHashes', 'receiptPath', 'hashes', 'report', 'receipt', 'v8ReceiptMisplaced', 'v10ReceiptPreserved'}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in PATHY}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def diff_paths(a, b, at=''):
    if type(a) is not type(b):
        return [at or '/']
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(at + '/' + k)
            else:
                out += diff_paths(a[k], b[k], at + '/' + k)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [at + '[len %d!=%d]' % (len(a), len(b))]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff_paths(x, y, at + '[%d]' % i)
        return out
    return [] if a == b else [at]


out = {'codexRunnerOriginalEqualsRoot': sha(CODEX / 'runner-original-reference-checks.json') == sha(ROOT / 'reference-checks.json'),
       'codexRunnerOriginalSha256': sha(CODEX / 'runner-original-reference-checks.json'), 'rootReferenceChecksSha256': sha(ROOT / 'reference-checks.json')}
codex = json.load(open(CODEX / 'reference-checks.json'))
root = json.load(open(ROOT / 'reference-checks.json'))
out['codexMinusRootTopLevelKeys'] = sorted(k for k in set(codex) | set(root) if codex.get(k) != root.get(k))
for name in ('enumeration.stdout', 'execution-inputs.stdout', 'query-projection.stdout'):
    m = json.load(open(MINE / name))
    rec = {'mineSha256': sha(MINE / name)}
    for label, base in (('root', ROOT / 'evaluator3'), ('historicalMine42', MINE42)):
        o = json.load(open(base / name))
        raw = diff_paths(m, o)
        rec[label] = {'sha256': sha(base / name), 'byteEqual': sha(MINE / name) == sha(base / name), 'rawDifferingPaths': raw[:60], 'rawDifferingPathCount': len(raw),
                      'equalAfterStrippingPathFieldsOnly': strip(m) == strip(o), 'strippedDifferingPaths': diff_paths(strip(m), strip(o))[:80]}
    if isinstance(m.get('cases'), list):
        rec['caseCount'] = len(m['cases'])
        rec['mismatches'] = m.get('mismatches')
    if isinstance(m.get('checks'), list):
        rec['checkCount'] = len(m['checks'])
        rec['failedChecks'] = [c['id'] for c in m['checks'] if not c.get('ok')]
        o42 = json.load(open(MINE42 / name))
        ids43, ids42 = [c['id'] for c in m['checks']], [c['id'] for c in o42.get('checks', [])]
        rec['checkIdsAddedVs42'] = [i for i in ids43 if i not in ids42]
        rec['checkIdsRemovedVs42'] = [i for i in ids42 if i not in ids43]
        rec['checkCountHistorical42'] = len(ids42)
    out[name] = rec
(RT / 'receipts/reference-children-stripped.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1)[:12000])
