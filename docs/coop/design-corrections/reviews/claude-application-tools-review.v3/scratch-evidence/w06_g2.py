"""W06: G2 - the second assent check must read the LIVE ROOT, not route through
ref()/source_path()/accepted_files; and the initial pre-output bound read must still govern.

(a) static: what the line 480 expression references now.
(b) differential: evaluate the v2 and v3 expressions side by side, using the assembler's own
    digest/source_path/ref definitions, in a namespace where the assent IS inside
    accepted_files and the snapshot copy differs from the live copy.
(c) executed: the pre-output refusal at line 124 still governs against v3 bytes.
"""
import ast
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
V2INPUTS = Path('/tmp/opensip-design-corrections/claude-application-tools-review.v2/inputs')
REF = '/tmp/opensip-architecture-review-env/bin/python'
ASM = INPUTS / 'assemble-records.successor.v1.py'
sys.path.insert(0, str(HERE))
import fixture as F  # noqa: E402

src = ASM.read_text()
tree = ast.parse(src)
out = {}

# ---------- (a) static ----------
recheck = [(n.lineno, ast.unparse(n.test)) for n in ast.walk(tree)
           if isinstance(n, ast.Assert) and 'assent_ref' in ast.unparse(n.test)]
first_out = min(n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call)
                and (ast.unparse(n.func) in ('out.mkdir', 'shutil.copytree', 'writej', 'writet')
                     or ast.unparse(n.func).endswith('.write_text')))
out['a_static'] = {
    'assentAssertions': recheck,
    'firstOutputProducingLine': first_out,
    'preOutputCheckPrecedesOutput': min(l for l, _ in recheck) < first_out,
    'recheckUsesLiveRoot': any('root /' in e for l, e in recheck if l > 400),
    'recheckAvoidsRefAndSourcePath': all(
        'ref(' not in e and 'source_path' not in e for l, e in recheck if l > 400),
}

# ---------- (b) differential against the v2 expression ----------
defs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)
        and n.name in ('digest', 'source_path', 'ref')}
ns = {'hashlib': hashlib, 'Path': Path}
exec(compile(ast.Module(body=[defs['digest'], defs['source_path'], defs['ref']],
                        type_ignores=[]), str(ASM), 'exec'), ns)
td = Path(tempfile.mkdtemp(prefix='opensip-g2-'))
root, snap = td / 'root', td / 'snap'
assent_rel = 'docs/coop/design-corrections/reviews/codex-post-reset.v1/design-assent.v22.json'
for base, body in ((root, '{"live":"bound bytes"}\n'), (snap, '{"snapshot":"different"}\n')):
    p = base / assent_rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
live_sha = hashlib.sha256((root / assent_rel).read_bytes()).hexdigest()
snap_sha = hashlib.sha256((snap / assent_rel).read_bytes()).hexdigest()
ns['root'] = root
ns['design_manifest'] = {'snapshotRoot': str(snap)}
# The assent IS inside the accepted subject - the condition G2 was about.
ns['accepted_files'] = {assent_rel: {'sha256': snap_sha}}
assent_ref = {'path': assent_rel, 'sha256': live_sha}  # digest bound at line 124 (live root)
ns['assent_ref'] = assent_ref
v2_expr = "ref(assent_ref['path'])['sha256'] == assent_ref['sha256']"
v3_expr = "digest(root / assent_ref['path']) == assent_ref['sha256']"
out['b_differential'] = {
    'assentInsideAcceptedSubject': True,
    'liveRootSha256': live_sha[:16], 'snapshotSha256': snap_sha[:16],
    'v2Expression': v2_expr, 'v2Result': bool(eval(v2_expr, ns)),
    'v3Expression': v3_expr, 'v3Result': bool(eval(v3_expr, ns)),
    'v2ReadsSnapshotNotBoundCopy': not bool(eval(v2_expr, ns)),
    'v3ReadsLiveBoundCopy': bool(eval(v3_expr, ns)),
    'note': ('With the assent inside accepted_files the v2 expression resolves to the frozen '
             'snapshot and no longer compares the bytes bind actually verified; the v3 '
             'expression reads the live root unconditionally.'),
}
# and the converse: a tampered live root must now be caught
(root / assent_rel).write_text('{"live":"TAMPERED"}\n')
out['b_differential']['v3CatchesLiveTamper'] = not bool(eval(v3_expr, ns))
out['b_differential']['v2MissesLiveTamper'] = bool(eval(v2_expr, ns)) is False  # still snapshot-based

# ---------- (c) executed pre-output refusal against v3 bytes ----------
lines = src.splitlines()
cut = next(i for i, l in enumerate(lines) if l.startswith('accepted_files = {r[')) + 5
prologue = '\n'.join(lines[:cut])
cases = []


def run_prologue(tamper):
    with tempfile.TemporaryDirectory(prefix='opensip-g2-pro-') as t:
        rp, bound_path, _ = F.build(t)
        r = subprocess.run([REF, '-I', '-B', str(INPUTS / 'bind-review-receipts.v1.py'),
                            '--receipt', str(rp), '--out', str(bound_path)],
                           capture_output=True, text=True, cwd=str(HERE))
        assert r.returncode == 0, 'fixture bind failed: ' + r.stderr[-300:]
        receipt = json.loads(rp.read_text())
        aroot = Path(receipt['root'])
        af = aroot / receipt['codexDesignAssent']['path']
        if tamper:
            d = json.loads(af.read_text())
            d['advisoryApplicationAccount'] = [{'id': 'SMUGGLED'}]
            af.write_text(json.dumps(d, indent=2) + '\n')
        out_dir = Path(t) / 'assembled'
        g = {'__file__': str(ASM), '__name__': '__main__'}
        old = sys.argv
        sys.argv = ['assemble', '--root', str(aroot), '--out', str(out_dir),
                    '--bound-receipt', str(bound_path), '--design-version', 'v22',
                    '--consumer-version', 'v10', '--application-version', 'v3',
                    '--draft', str(Path(t) / 'draft'), '--source-delta', str(Path(t) / 'd.json')]
        err = ''
        try:
            exec(compile(prologue, str(ASM), 'exec'), g)
        except Exception as e:  # noqa: BLE001
            err = f'{type(e).__name__}: {e}'[:160]
        finally:
            sys.argv = old
        return err, out_dir.exists()


e, made = run_prologue(False)
cases.append({'id': 'control-untampered-assent-passes', 'refused': bool(e),
              'outDirCreated': made, 'detail': e})
e, made = run_prologue(True)
cases.append({'id': 'tampered-assent-refuses-before-any-output', 'refused': bool(e),
              'outDirCreated': made, 'detail': e})
out['c_executedPreOutput'] = cases

(HERE / 'w06_g2.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
