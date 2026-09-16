"""V06: F5 - the root design assent digest must be re-verified BEFORE any assembly output.

(a) Machine-checked line-order proof over the assembler AST: the assent assertion precedes
    every output-producing statement in this straight-line module.
(b) Executed refusal: bind a real synthetic receipt, tamper the assent on disk, then run the
    assembler prologue (truncated before out.mkdir) and confirm it raises and creates no out/.
(c) The second re-check before advisory use, and which path it resolves against.
"""
import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(HERE))
import fixture as F  # noqa: E402

REF = '/tmp/opensip-architecture-review-env/bin/python'
ASM = INPUTS / 'assemble-records.successor.v1.py'
src = ASM.read_text()
tree = ast.parse(src)
out = {}

# ---------- (a) line-order proof ----------
assent_asserts = [n.lineno for n in ast.walk(tree)
                  if isinstance(n, ast.Assert) and 'codexDesignAssent' in ast.unparse(n.test)]
recheck = [n.lineno for n in ast.walk(tree)
           if isinstance(n, ast.Assert) and "ref(assent_ref['path'])" in ast.unparse(n.test)]
output_ops = []
for n in ast.walk(tree):
    if isinstance(n, ast.Call):
        t = ast.unparse(n.func)
        if t in ('out.mkdir', 'shutil.copytree', 'shutil.copyfile', 'writej', 'writet',
                 'row_support.mkdir') or t.endswith('.write_text') or t.endswith('.mkdir'):
            output_ops.append((n.lineno, ast.unparse(n)[:80]))
output_ops.sort()
first_out = output_ops[0][0]
out['a_lineOrder'] = {
    'assentBindDigestAssertLine': assent_asserts,
    'assentRecheckBeforeAdvisoryUseLine': recheck,
    'firstOutputProducingStatement': {'line': first_out, 'code': output_ops[0][1]},
    'assentAssertPrecedesAllOutput': min(assent_asserts) < first_out,
    'outMkdirLine': [n.lineno for n in ast.walk(tree)
                     if isinstance(n, ast.Call) and ast.unparse(n.func) == 'out.mkdir'],
    'firstFiveOutputOps': output_ops[:5],
}

# ---------- (b) executed refusal at the prologue ----------
lines = src.splitlines()
cut = next(i for i, l in enumerate(lines) if l.startswith('accepted_files = {r['))
prologue = '\n'.join(lines[:cut + 5])  # through the frozen-design drift loop
out['b_prologueCutLine'] = cut + 5
cases = []


def run_prologue(tamper):
    with tempfile.TemporaryDirectory(prefix='opensip-f5-') as td:
        rp, bound_path, _ = F.build(td)
        r = subprocess.run([REF, '-I', '-B', str(INPUTS / 'bind-review-receipts.v1.py'),
                            '--receipt', str(rp), '--out', str(bound_path)],
                           capture_output=True, text=True, cwd=str(HERE))
        assert r.returncode == 0, 'fixture bind failed: ' + r.stderr[-300:]
        receipt = json.loads(rp.read_text())
        root = Path(receipt['root'])
        assent_file = root / receipt['codexDesignAssent']['path']
        if tamper:
            d = json.loads(assent_file.read_text())
            d['advisoryApplicationAccount'] = [{'id': 'SMUGGLED-ADVISORY'}]
            assent_file.write_text(json.dumps(d, indent=2) + '\n')
        out_dir = Path(td) / 'assembled'
        g = {'__file__': str(ASM), '__name__': '__main__'}
        argv = ['assemble', '--root', str(root), '--out', str(out_dir),
                '--bound-receipt', str(bound_path), '--design-version', 'v22',
                '--consumer-version', 'v10', '--application-version', 'v3',
                '--draft', str(Path(td) / 'draft'), '--source-delta', str(Path(td) / 'delta.json')]
        old = sys.argv
        sys.argv = argv
        err = ''
        try:
            exec(compile(prologue, str(ASM), 'exec'), g)
        except Exception as e:  # noqa: BLE001
            err = f'{type(e).__name__}: {e}'[:160]
        finally:
            sys.argv = old
        return err, out_dir.exists()


err, made = run_prologue(False)
cases.append({'id': 'control-untampered-assent-passes-prologue', 'refused': bool(err),
              'expected': 'PASS', 'outDirCreated': made, 'detail': err})
err, made = run_prologue(True)
cases.append({'id': 'tampered-assent-refuses-before-any-output', 'refused': bool(err),
              'expected': 'REFUSE', 'outDirCreated': made, 'detail': err})
out['b_executed'] = cases

# ---------- (c) which path the re-check resolves against ----------
out['c_recheckResolution'] = {
    'note': ('ref() resolves via source_path(), which returns snapshotRoot/rel when rel is in '
             'accepted_files and root/rel otherwise. accepted_files is EMPTY at the first check '
             '(line %d) and POPULATED by the time of the re-check (line %d).'
             % (min(assent_asserts), recheck[0] if recheck else -1)),
    'acceptedFilesAssignedAtLines': [n.lineno for n in ast.walk(tree)
                                     if isinstance(n, ast.Assign)
                                     and any(getattr(t, 'id', '') == 'accepted_files'
                                             for t in n.targets)],
}

(HERE / 'v06_f5.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
