"""p06: final digests. Parses review.json, hashes review.md/review.json/correction.diff and every receipt, re-verifies
the captured corrected files and dependencies against p00, and reports whether root's correction artifacts and the
live successor files changed since capture (report only). Output: receipts/p06-final.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
SRC = Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
R = BASE / 'receipts'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
p00 = json.loads((R / 'p00-capture.json').read_text())
review = json.loads((BASE / 'review.json').read_text())
out = {'verdict': review['verdict'],
       'deliverables': {n: sha(BASE / n) for n in ('review.md', 'review.json', 'correction.diff')},
       'capturedCorrectedUnchanged': all(sha(BASE / 'work/source' / r['path']) == r['captured'] for r in p00['correctedFiles']),
       'capturedDependenciesUnchanged': all(sha(BASE / 'work/source' / p) == v['captured'] for p, v in p00['dependencies'].items()),
       'liveCorrectedFilesUnchangedSinceCapture': all(sha(SRC / r['path']) == r['captured'] for r in p00['correctedFiles']),
       'rootArtifactsUnchangedSinceCapture': {k: sha(ROOT / k) == v for k, v in p00['rootArtifacts'].items()},
       'receiptExits': {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))},
       'receiptDigests': {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()}}
(R / 'p06-final.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'receiptDigests'}, indent=1))
sys.exit(0 if out['capturedCorrectedUnchanged'] and out['capturedDependenciesUnchanged'] else 1)
