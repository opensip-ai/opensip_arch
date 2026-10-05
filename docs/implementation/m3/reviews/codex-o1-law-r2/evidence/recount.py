"""Recount M3-O1 r2's corrected baselines (NB-02, NB-03) at product b7b87b7, read-only.

Usage: recount.py [--product PATH] [--rev REV]; defaults /Users/sb/code/opensip-ai/opensip and b7b87b7.
Run with python3 -I -B. It runs only `git grep` on the named commit, writes nothing, and runs no cargo.
The path rule is item 19's: production paths are .rs files under crates/ and apps/ that are not under
a tests/ or benches/ directory and do not end in _tests.rs. Inline cfg(test) text is counted.
"""
import json, re, subprocess, sys
from collections import Counter

args = sys.argv[1:]
W = args[args.index('--product') + 1] if '--product' in args else '/Users/sb/code/opensip-ai/opensip'
REV = args[args.index('--rev') + 1] if '--rev' in args else 'b7b87b7'
TEST = re.compile(r'(^|/)(tests|benches)/|_tests\.rs$')


def grep(pattern, extended=False):
    cmd = ['git', '-C', W, 'grep', '-n'] + (['-E'] if extended else ['-F']) + [pattern, REV, '--', 'crates', 'apps']
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()
    rows = []
    for line in out:
        _, path, number, text = line.split(':', 3)
        if path.endswith('.rs'):
            rows.append((path, int(number), text))
    return rows


let_all = grep('let _ =')
let_prod = [r for r in let_all if not TEST.search(r[0])]
by_crate = Counter('/'.join(r[0].split('/')[:2]) for r in let_prod)
macros = [r for r in grep(r'debug_assert(_eq|_ne)?!', extended=True) if not TEST.search(r[0])]
text = [r for r in grep('debug_assert') if not TEST.search(r[0])]
print(json.dumps({
    'rev': REV,
    'letUnderscore': {'total': len(let_all), 'files': len({r[0] for r in let_all}),
                      'production': len(let_prod), 'testOnly': len(let_all) - len(let_prod),
                      'productionByCrate': dict(sorted(by_crate.items())),
                      'platformPlusSecurity': by_crate['crates/platform'] + by_crate['crates/security'],
                      'installationReadFixtureLines': sum(1 for r in let_prod if r[0].endswith('installation_read_fixture.rs'))},
    'debugAssert': {'macroSites': ['%s:%d' % (p, n) for p, n, _ in macros],
                    'allTextMatches': len(text),
                    'otherTextMatches': ['%s:%d' % (p, n) for p, n, _ in text if (p, n) not in {(m[0], m[1]) for m in macros}]},
}, indent=1))
