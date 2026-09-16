"""p05: exact correction diff, root's retained before-files -> captured after-files (work/source), for the three changed
files only. Records per-file hunk counts, added/removed line counts, the diff text (correction.diff) and its sha256.
Output: receipts/p05-diff.json and correction.diff in the runtime root.
"""
import difflib, hashlib, json
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
files = [f['path'] for f in json.loads((ROOT / 'correction.json').read_text())['files']]
text, rows = '', []
for p in files:
    a = (ROOT / 'before-files' / p).read_text(encoding='utf-8').splitlines(True)
    b = (BASE / 'work/source' / p).read_text(encoding='utf-8').splitlines(True)
    d = list(difflib.unified_diff(a, b, 'before/' + p, 'after/' + p))
    text += ''.join(d)
    rows.append({'path': p, 'hunks': sum(1 for l in d if l.startswith('@@')),
                 'added': sum(1 for l in d if l.startswith('+') and not l.startswith('+++')),
                 'removed': sum(1 for l in d if l.startswith('-') and not l.startswith('---'))})
(BASE / 'correction.diff').write_text(text, encoding='utf-8')
out = {'files': rows, 'diffSha256': hashlib.sha256(text.encode()).hexdigest(), 'lines': text.count('\n')}
(BASE / 'receipts' / 'p05-diff.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
print(text)
