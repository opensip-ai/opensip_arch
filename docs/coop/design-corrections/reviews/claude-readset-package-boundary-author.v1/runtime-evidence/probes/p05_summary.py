"""p05 [final]: delta and custody summary.

- full delta of work/source against the baseline copy (receipts/baseline-file-hashes.json = prior captured review
  source): every changed file (must be only the owned files), unified diff (delta-vs-prior-review-source.diff) and
  before/after hashes;
- prior review work/source and deliverables unchanged against p00; hybrid trees are disposable and not the delivered tree;
- the exact owner selectors changed (function names, prose anchors, checker case names);
- receipt exits and digests; with 'final', review.md/review.json digests (review.json parsed).
Output: receipts/p05-summary[.final].json.
"""
import difflib, hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
PRIOR = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
W = BASE / 'work' / 'source'
R = BASE / 'receipts'
final = len(sys.argv) > 1 and sys.argv[1] == 'final'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
baseline = json.loads((R / 'baseline-file-hashes.json').read_text())
p00 = json.loads((R / 'p00-copy.json').read_text())
current = {str(p.relative_to(W)): sha(p) for p in (W / 'docs').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
changed = sorted(p for p in current if baseline.get(p) != current[p])
added, removed = sorted(set(current) - set(baseline)), sorted(set(baseline) - set(current))
diff, rows = '', []
for p in changed:
    a, b = (PRIOR / 'work/source' / p).read_bytes(), (W / p).read_bytes()
    diff += ''.join(difflib.unified_diff(a.decode().splitlines(True), b.decode().splitlines(True), 'prior-review-source/' + p, 'author/' + p))
    rows.append({'path': p, 'before': baseline[p], 'after': current[p], 'priorReviewCopyStillBefore': sha(PRIOR / 'work/source' / p) == baseline[p]})
(BASE / 'delta-vs-prior-review-source.diff').write_text(diff, encoding='utf-8')
OWNED = set(p00['ownedBaseline'])
out = {'changedFiles': rows, 'added': added, 'removed': removed, 'onlyOwnedFilesChanged': set(changed) <= OWNED and not added and not removed,
       'delta': {'path': 'delta-vs-prior-review-source.diff', 'sha256': hashlib.sha256(diff.encode()).hexdigest(), 'lines': diff.count('\n')},
       'priorReviewUnchanged': all(sha(PRIOR / n) == h for n, h in p00['priorReview'].items()),
       'priorReviewSourceUnchangedForOwned': all(r['priorReviewCopyStillBefore'] for r in rows)}
out['ownerSelectors'] = {
    'docs/coop/design-corrections/foundation/identity-model.v3.py': ['snapshot_pruned_tree_faults (docstring and package authorization call)', 'listed_package_authorizes_read (new helper)'],
    'docs/v2/contracts/product-v1/identity-and-evidence.md': ['section 3 "What sourceInventory contains (consumer24 A4)": "Nested packages have explicit custody" and "What replay decides and what it does not prove"'],
    'docs/v2/contracts/product-v1/security-and-lifecycle.md': ['S3 "Pruned trees and the read set (A-5)": nested installed package sentence'],
    'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py': ['a4(): 12 helper rows after nested-vcs-lookalike-segments-remain-lawful-package-reads', 'a4(): ts_run(extra, packages) and ts_context_layout', 'a4(): 7 real-Run rows after the existing real-run-refuses loop'],
}
out['receiptExits'] = {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}
out['receiptDigests'] = {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()}
if final:
    json.loads((BASE / 'review.json').read_text())
    out['review'] = {n: sha(BASE / n) for n in ('review.md', 'review.json')}
name = 'p05-summary.final.json' if final else 'p05-summary.json'
(R / name).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'receiptDigests'}, indent=1))
print(diff)
sys.exit(0 if out['onlyOwnedFilesChanged'] and out['priorReviewUnchanged'] and out['priorReviewSourceUnchangedForOwned'] else 1)
