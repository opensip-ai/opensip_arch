"""P06: machine-checked static selectors.

(a) Which bound-receipt artefacts are digest-re-verified in assemble-records.
(b) Which staged sources are copied from an unpinned absolute path.
(c) Coauthor-exclusion constant used at each enforcement point.
(d) Which shipped evidence reports carry a tested-source digest binding.
"""
import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
out = {}


def seg(node):
    """Render a subscript chain like bound['x']['y'] as text."""
    try:
        return ast.unparse(node)
    except Exception:  # noqa: BLE001
        return '<?>'


# ---- (a) assemble-records: bound[...] sha256 custody ----
asm_src = (INPUTS / 'assemble-records.successor.v1.py').read_text()
asm = ast.parse(asm_src)
bound_sha_refs = set()
for n in ast.walk(asm):
    if isinstance(n, ast.Compare):
        for side in [n.left] + list(n.comparators):
            t = seg(side)
            if t.startswith('bound[') and t.endswith("['sha256']"):
                bound_sha_refs.add(t)
bound_keys = sorted({seg(n) for n in ast.walk(asm)
                     if isinstance(n, ast.Subscript) and seg(n).startswith('bound[')
                     and seg(n).endswith("['sha256']")})
out['a_assembleBoundDigestCustody'] = {
    'boundSha256FieldsReferenced': bound_keys,
    'boundSha256FieldsCompared': sorted(bound_sha_refs),
    'referencedButNeverCompared': sorted(set(bound_keys) - bound_sha_refs),
}
# where is codexDesignAssent consumed?
out['a_assembleAssentConsumption'] = [
    {'line': n.lineno, 'code': ast.unparse(n)[:120]}
    for n in ast.walk(asm)
    if isinstance(n, (ast.Assign, ast.Expr))
    and 'codexDesignAssent' in ast.unparse(n)
] + [{'line': n.lineno, 'code': ast.unparse(n)[:120]}
     for n in ast.walk(asm) if isinstance(n, ast.Subscript)
     and ast.unparse(n).startswith("assent[")]

# ---- (b) unpinned absolute staged sources ----
abs_copies = []
for n in ast.walk(asm):
    if isinstance(n, ast.Call) and ast.unparse(n.func).endswith('copyfile'):
        txt = ast.unparse(n)
        if "Path('/" in txt or '"/' in txt.split('(', 1)[-1][:2]:
            abs_copies.append({'line': n.lineno, 'code': txt[:200]})
out['b_unpinnedAbsoluteStagedCopies'] = abs_copies
out['b_absolutePathLiterals'] = sorted({
    n.value for f in sorted(INPUTS.glob('*.py')) for n in ast.walk(ast.parse(f.read_text()))
    if isinstance(n, ast.Constant) and isinstance(n.value, str)
    and n.value.startswith('/') and len(n.value) > 6 and ' ' not in n.value
})

# ---- (c) coauthor-exclusion constant at each enforcement point ----
points = []
for f in sorted(INPUTS.glob('*.py')):
    src = f.read_text()
    for i, line in enumerate(src.splitlines(), 1):
        if 'COAUTHOR_SESSIONS' in line or 'EXCLUDED_SESSION' in line:
            points.append({'file': f.name, 'line': i, 'code': line.strip()[:150]})
out['c_coauthorExclusionPoints'] = points

# ---- (d) evidence reports: tested-source digest binding ----
reports = {}
for f in sorted(INPUTS.glob('*.json')):
    try:
        d = json.loads(f.read_text())
    except Exception:  # noqa: BLE001
        continue
    if isinstance(d, dict) and 'checks' in d:
        reports[f.name] = {'hasSourceSha256': 'sourceSha256' in d,
                           'topLevelKeys': sorted(d)[:14],
                           'passed': d.get('passed'), 'failed': d.get('failed')}
out['d_shippedEvidenceReports'] = reports
# freeze-application.py: which selftest reports are digest-bound to their subject?
frz = (INPUTS / 'freeze-application.py').read_text()
out['d_freezeSourceBindingLines'] = [
    l.strip() for l in frz.splitlines()
    if 'selftest' in l or 'sourceSha256' in l or 'check-retain' in l or 'check-review-envelope' in l]

(HERE / 'p06_static.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2)[:6000])
