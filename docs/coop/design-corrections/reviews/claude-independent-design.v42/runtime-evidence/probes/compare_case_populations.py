"""Historical case-population accounting: run each tree's OWN check-execution-inputs.v1.py (source40, source41, source42) and
check-enumeration.v1.py (source41, source42) on the verified disposable copies in this runtime (stdout JSON only; enumeration
receipts go to explicit files under work/), then compare every shared case field by field (path-bearing receipt fields
excluded) and every full-run runId. Writes receipts/case-populations.json and preserves each checker stdout."""
import hashlib, json, os, subprocess
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
PY = '/tmp/opensip-architecture-review-env/bin/python'
TREES = {'source40': RT / 'work/base40', 'source41': RT / 'work/base41', 'source42': RT / 'work/source42-pkg'}
OUTDIR = RT / 'receipts/case-populations'
OUTDIR.mkdir(parents=True, exist_ok=True)
PATHY = {'ownedHashes', 'receiptPath', 'hashes', 'report', 'receipt', 'v8ReceiptMisplaced', 'v10ReceiptPreserved'}


def run(label, tree, script, extra):
    fdir = tree / 'docs/coop/design-corrections/foundation'
    cmd = [PY, '-I', '-B', str(fdir / script)] + extra
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(fdir), timeout=7200)
    base = OUTDIR / (label + '.' + script.replace('.py', ''))
    Path(str(base) + '.stdout').write_text(p.stdout)
    Path(str(base) + '.stderr').write_text(p.stderr)
    try:
        doc = json.loads(p.stdout)
    except ValueError:
        doc = None
    return {'command': cmd, 'exitCode': p.returncode, 'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest(), 'stdout': str(base) + '.stdout'}, doc


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in PATHY}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def cases_of(doc):
    return {c['case']: c for c in (doc or {}).get('cases') or [] if isinstance(c, dict) and 'case' in c}


def run_ids(x, acc):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == 'runId' and isinstance(v, str):
                acc.append(v)
            run_ids(v, acc)
    elif isinstance(x, list):
        for v in x:
            run_ids(v, acc)
    return acc


res = {'executionInputs': {}, 'enumeration': {}}
docs = {}
for label, tree in TREES.items():
    meta, doc = run(label, tree, 'check-execution-inputs.v1.py', [])
    docs[label] = doc
    res['executionInputs'][label] = dict(meta, cases=len(cases_of(doc)), mismatches=len((doc or {}).get('mismatches') or []),
                                         oracles=len((doc or {}).get('oracles') or []) if isinstance((doc or {}).get('oracles'), list) else (doc or {}).get('oracles'))


def compare(a, b):
    ca, cb = cases_of(docs[a]), cases_of(docs[b])
    shared = sorted(set(ca) & set(cb))
    differing = {}
    for n in shared:
        x, y = strip(ca[n]), strip(cb[n])
        if x != y:
            differing[n] = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
    ra = sorted(set(run_ids([ca[n] for n in shared], [])))
    rb = sorted(set(run_ids([cb[n] for n in shared], [])))
    return {'shared': len(shared), 'onlyA': sorted(set(ca) - set(cb)), 'onlyB': sorted(set(cb) - set(ca)), 'differingSharedCases': differing,
            'sharedRunIdsA': len(ra), 'sharedRunIdsEqual': ra == rb}


res['executionInputs']['compare40to41'] = compare('source40', 'source41')
res['executionInputs']['compare41to42'] = compare('source41', 'source42')
res['executionInputs']['compare40to42'] = compare('source40', 'source42')
edocs = {}
for label in ('source41', 'source42'):
    tree = TREES[label]
    receipt = RT / ('work/enumeration-receipt.' + label + '.json')
    meta, doc = run(label, tree, 'check-enumeration.v1.py', ['--receipt', str(receipt)])
    edocs[label] = doc
    res['enumeration'][label] = dict(meta, cases=len(cases_of(doc)), mismatches=len((doc or {}).get('mismatches') or []))
ca, cb = cases_of(edocs['source41']), cases_of(edocs['source42'])
shared = sorted(set(ca) & set(cb))
res['enumeration']['compare41to42'] = {'shared': len(shared), 'onlyA': sorted(set(ca) - set(cb)), 'onlyB': sorted(set(cb) - set(ca)),
                                       'differingSharedCases': {n: sorted(k for k in set(strip(ca[n])) | set(strip(cb[n])) if strip(ca[n]).get(k) != strip(cb[n]).get(k))
                                                                for n in shared if strip(ca[n]) != strip(cb[n])}}
(RT / 'receipts/case-populations.json').write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:10000])
