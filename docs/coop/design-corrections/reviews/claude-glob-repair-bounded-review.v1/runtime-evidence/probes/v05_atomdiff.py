"""V05 — what changed in the atom contract and check-atoms, and do the 30 new prescribed vectors
agree with the published contract table and with the unchanged reference?"""
import ast, difflib, importlib.util, json, os, re, sys

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1/source'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
R = {}

# ---------- atom contract prose diff ----------
rel = 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md'
before = open(os.path.join(SNAP, rel), encoding='utf-8').read().splitlines()
after = open(os.path.join(G, rel), encoding='utf-8').read().splitlines()
d = list(difflib.unified_diff(before, after, lineterm='', n=2))
R['atomContractDiff'] = d
print('--- atom-evaluation-contract.v1.md diff (%d lines) ---' % len(d))
for l in d:
    print(l[:200])

# ---------- check-atoms diff, summarised ----------
relc = 'docs/coop/design-corrections/foundation/check-atoms.v1.py'
cb = open(os.path.join(SNAP, relc), encoding='utf-8').read()
ca = open(os.path.join(G, relc), encoding='utf-8').read()
fb = {n.name for n in ast.walk(ast.parse(cb)) if isinstance(n, ast.FunctionDef)}
fa = {n.name for n in ast.walk(ast.parse(ca)) if isinstance(n, ast.FunctionDef)}
R['newFunctions'] = sorted(fa - fb)
R['removedFunctions'] = sorted(fb - fa)
R['functionCountBefore'] = len(fb)
R['functionCountAfter'] = len(fa)
print('\ncheck-atoms functions: %d -> %d | new: %s | removed: %s'
      % (len(fb), len(fa), sorted(fa - fb), sorted(fb - fa)))

# ---------- the prescribed vectors inside the new checker ----------
tree = ast.parse(ca)
vectors = []
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name in (fa - fb):
        for sub in ast.walk(node):
            if isinstance(sub, (ast.Tuple, ast.List)) and len(getattr(sub, 'elts', [])) in (2, 3):
                try:
                    val = ast.literal_eval(sub)
                except Exception:
                    continue
                if (len(val) == 3 and isinstance(val[0], str) and isinstance(val[1], str)
                        and isinstance(val[2], bool)):
                    vectors.append(val)
R['prescribedVectors'] = vectors
R['prescribedVectorCount'] = len(vectors)
print('\nprescribed (pattern, candidate, expected) vectors found in the new functions: %d'
      % len(vectors))

# ---------- do they agree with the unchanged reference? ----------
spec = importlib.util.spec_from_file_location(
    'wfm', os.path.join(SNAP, 'docs/coop/design-corrections/workflows/workflows_model.v1.py'))
W = importlib.util.module_from_spec(spec)
sys.modules['wfm'] = W
spec.loader.exec_module(W)
bad = []
for pat, cand, want in vectors:
    got = W.glob_match(pat, cand)
    if got != want:
        bad.append({'pattern': pat, 'candidate': cand, 'expected': want, 'reference': got})
R['vectorsDisagreeingWithReference'] = bad
print('vectors disagreeing with the unchanged reference: %d' % len(bad))
for b in bad[:10]:
    print('   %-18r %-24r expected=%-5s reference=%s'
          % (b['pattern'], b['candidate'], b['expected'], b['reference']))

# ---------- are the contract's 22 documented examples covered by the vectors? ----------
contract = open(os.path.join(G, 'docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md'),
                encoding='utf-8').read()
tbl = re.findall(r'^\|\s*`([^`]+)`\s*\|\s*`?([^`|]+?)`?\s*\|\s*(true|false)\s*\|', contract, re.M)
R['contractTableRows'] = len(tbl)
vecset = {(p, c) for p, c, _ in vectors}
covered = [t for t in tbl if (t[0], t[1].strip()) in vecset]
R['contractRowsAlsoInVectors'] = len(covered)
print('\ncontract table rows: %d | also present as prescribed vectors: %d'
      % (len(tbl), len(covered)))

json.dump(R, open(os.path.join(OUT, 'v05-atomdiff.json'), 'w'), indent=1, default=str)
print('\nwrote v05-atomdiff.json')
