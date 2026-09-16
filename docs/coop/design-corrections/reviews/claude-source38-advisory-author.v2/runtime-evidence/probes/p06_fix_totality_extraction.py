"""p06: correct the harness defect found by p04_owner_checks.edited (exit 1, receipt retained).

The absent-carrier totality check collected every string constant anywhere inside `_s37_open`'s return expressions,
so the condition operand 'gj_seq_contiguous' of `return 'carrierFormat2' if 'gj_seq_contiguous' in names else
'carrierFormat1'` was counted as a dispatch result. The law and the map were right; the extraction was wrong. This
replaces the extraction with one that takes only result positions (a returned constant, or both arms of a returned
conditional expression). One counted replacement in v2 work/edited check-carrier-v3.py.
Output: receipts/p06-fix-totality-extraction.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
REL = 'docs/coop/design-corrections/security/check-carrier-v3.py'
P = BASE / 'work' / 'edited' / REL
OLD = ("_s37_results = {k.value for r in _s37_ast.walk(_s37_fn) if isinstance(r, _s37_ast.Return)\n"
       "                for k in _s37_ast.walk(r.value) if isinstance(k, _s37_ast.Constant) and isinstance(k.value, str)}\n")
NEW = ("\n\ndef _s37_returned(node):\n"
       "    \"\"\"Result positions only: a returned string constant, or both arms of a returned conditional expression.\"\"\"\n"
       "    if isinstance(node, _s37_ast.Constant) and isinstance(node.value, str):\n"
       "        return {node.value}\n"
       "    if isinstance(node, _s37_ast.IfExp):\n"
       "        return _s37_returned(node.body) | _s37_returned(node.orelse)\n"
       "    return set()\n"
       "\n\n"
       "_s37_results = set().union(*(_s37_returned(r.value) for r in _s37_ast.walk(_s37_fn) if isinstance(r, _s37_ast.Return)))\n")
text = P.read_text(encoding='utf-8')
before = hashlib.sha256(text.encode()).hexdigest()
out = {'path': REL, 'before': before, 'anchorCount': text.count(OLD)}
if text.count(OLD) != 1:
    out['written'] = False
else:
    new = text.replace(OLD, NEW)
    compile(new, REL, 'exec')
    P.write_text(new, encoding='utf-8')
    out.update(written=True, after=hashlib.sha256(P.read_bytes()).hexdigest())
(BASE / 'receipts' / 'p06-fix-totality-extraction.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if out['written'] else 1)
