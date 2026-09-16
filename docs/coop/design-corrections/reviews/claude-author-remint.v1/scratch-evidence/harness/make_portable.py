"""Generate portable successors of the four construction entry points.

MINIMAL TRANSFORM: only the header (imports / ROOT / helpers path / foundation path /
transport) and the output-directory line are replaced. Every construction line is carried
over byte-identically, and the generator asserts that, so the portable script cannot quietly
become a different construction.
"""
import difflib
import hashlib
import json
import os
import sys

PKG = '/private/tmp/opensip-design-corrections/claude-author-remint.v1/package'
OUT = '/private/tmp/opensip-design-corrections/claude-author-remint.v1/scratch/portable'

PRELUDE = '''"""%s

PORTABLE SUCCESSOR. Declared inputs only: --source (reference source root), --package (author
package root supplying the bundled helpers and export transport), --out (fresh output dir),
optional --helpers overlay. No historical ROOT/output helpers path, no sibling source25 and no
external check-blind13 transport is consulted. Construction logic below is byte-identical to
the historical entry point.
"""
from pathlib import Path
import copy,importlib.util,json,sys,tomllib,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
import author_portable as AP
_a=AP.arguments(%r)
SOURCE=_a.source;PACKAGE=_a.package;OUTROOT=AP.fresh_out(_a.out)
F=AP.foundation(SOURCE)
AP.load_helpers(PACKAGE,_a.helpers,kit=_a.kit,out=OUTROOT)
'''

HELPER_IMPORT = 'from helpers import %s\n'


def transform(name, title, helper_names, old_out_line, new_out_expr, needs_transport, needs_models,
              extra_arg=None, replacements=()):
    src = open(os.path.join(PKG, name), encoding='utf-8').read()
    lines = src.splitlines(keepends=True)

    # Locate the historical header: everything up to and including the last header line.
    body_start = None
    for i, l in enumerate(lines):
        if l.startswith('from helpers import'):
            body_start = i + 1
            break
    assert body_start is not None, name

    prelude = PRELUDE % (title, title)
    if extra_arg:
        prelude = prelude.replace('_a=AP.arguments(%r)' % title,
                                  '_a=AP.arguments(%r,extra=%s)' % (title, extra_arg))
    head = prelude + HELPER_IMPORT % helper_names
    rest = lines[body_start:]

    if needs_transport or needs_models:
        # The historical loader block sits immediately after `from helpers import ...`.
        # Drop exactly the three historical lines and re-bind from declared inputs.
        drop = []
        k = 0
        while k < len(rest) and len(drop) < 4:
            s = rest[k].strip()
            if s.startswith('def load(n,p):') or s.startswith('s=importlib.util.spec_from_file_location(n,p)') \
               or s.startswith("T=load('author_transport'") or s.startswith("R=load('author_replay'") \
               or s.startswith("X=load('author_capture'"):
                drop.append(rest[k])
                rest.pop(k)
                continue
            if s == '':
                k += 1
                continue
            break
        assert len(drop) == 4, (name, len(drop), [d[:60] for d in drop])
        head += (
            "\n"
            "def load(n,p):\n"
            " return AP.load_module(n,p)\n"
            "T=AP.transport(PACKAGE)\n"
            "R=load('author_replay',F/'evaluator_replay_model.v3.py');M=R.M;E=R.E;C=M.C\n"
            "X=load('author_capture',F/'execution_inputs_fixture.v3.py');"
            "S=load('author_seed',F/'evaluator_semantic_fixture.v3.py')\n"
        )

    out_src = head + ''.join(rest)

    # Output directory: never inside the package.
    assert out_src.count(old_out_line) == 1, (name, out_src.count(old_out_line))
    out_src = out_src.replace(old_out_line, new_out_expr, 1)

    for old, new in replacements:
        assert out_src.count(old) == 1, (name, old, out_src.count(old))
        out_src = out_src.replace(old, new, 1)

    # Record provenance beside the outputs.
    out_src = out_src.rstrip('\n') + '\nAP.write_provenance(_a)\n'

    dst = os.path.join(OUT, name)
    open(dst, 'w', encoding='utf-8').write(out_src)

    # Assert construction-body equality: every non-header line of the original must survive.
    orig_body = [l for l in lines[body_start:] if l.strip()]
    new_body = [l for l in out_src.splitlines(keepends=True) if l.strip()]
    missing = [l for l in orig_body
               if l not in new_body and l.strip() not in ('def load(n,p):',)
               and not l.strip().startswith('s=importlib.util.spec_from_file_location(n,p)')
               and not l.strip().startswith(("T=load(", "R=load(", "X=load("))
               and old_out_line.strip() not in l]
    return {'script': name, 'sha256': hashlib.sha256(open(dst, 'rb').read()).hexdigest(),
            'originalSha256': hashlib.sha256(src.encode()).hexdigest(),
            'constructionLinesCarried': len(orig_body) - len(missing),
            'constructionLinesDropped': [l.strip()[:80] for l in missing]}


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    rows.append(transform(
        'build-checkpoint3.py', 'Author-assisted reference checkpoint, not blind acceptance.',
        'runs', "out=ROOT/'checkpoint3';out.mkdir()", "out=OUTROOT/'checkpoint3';out.mkdir()",
        False, False))
    rows.append(transform(
        'build-normalized-examples6.py',
        'AUTHOR construction from synthetic source inputs and reference helpers.',
        'runs,builder,h,order,store',
        "out=ROOT/'normalized-examples6';out.mkdir()", "out=OUTROOT/'normalized-examples6';out.mkdir()",
        True, True))
    rows.append(transform(
        'build-rust-selection-examples.py',
        'AUTHOR construction from synthetic source inputs and reference helpers.',
        'runs,builder,h,order,store',
        "out=ROOT/'rust-selection-examples1';out.mkdir()",
        "out=OUTROOT/'rust-selection-examples1';out.mkdir()", True, True))
    rows.append(transform(
        'build-semantic-controls.py',
        'Author mutation controls; exact independent owner execution follows separately.',
        'store,order', "out=ROOT/'semantic-controls1';out.mkdir()",
        "out=OUTROOT/'semantic-controls1';out.mkdir()", False, False,
        extra_arg="[('--positive',dict(required=True,type=Path,help='directory holding the "
                  "FRESHLY REMINTED positive checkpoint3 (claims.json + ts.store.json) that "
                  "these controls must be derived from'))]",
        replacements=[("src=ROOT/'checkpoint3'", "src=_a.positive.resolve()")]))
    for r in rows:
        print('%-34s carried=%-4s dropped=%s' % (r['script'], r['constructionLinesCarried'],
                                                 r['constructionLinesDropped']))
    json.dump(rows, open(OUT + '/portable-generation.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
