"""V01: full diffs of every changed file, plus an assertion-census to detect any
weakened or silenced check (removed assert / removed test case / loosened operator).
"""
import ast
import difflib
import os

V1 = '/tmp/opensip-design-corrections/claude-application-tools-review.v1/inputs'
V2 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v2/inputs'
CHANGED = ['assemble-records.successor.v1.py', 'check-review-envelope.v2.py',
           'launch-application-review.successor.v1.py', 'prepare-validation.py',
           'retain-application-review.successor.v1.py', 'retain_public.py',
           'review_envelope.py', 'verify-applied.py']


def asserts(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Assert):
            out.append(ast.unparse(n.test))
    return out


def testids(src):
    """record('id',...) / catch('id',...) identifiers in the disposable suites."""
    ids = []
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in ('record', 'catch') and n.args
                and isinstance(n.args[0], ast.Constant)):
            ids.append(n.args[0].value)
    return ids


total_added = total_removed = 0
for name in CHANGED:
    a = open(os.path.join(V1, name)).read()
    b = open(os.path.join(V2, name)).read()
    al, bl = a.splitlines(), b.splitlines()
    d = [l for l in difflib.unified_diff(al, bl, lineterm='', n=0)]
    plus = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    total_added += plus
    total_removed += minus
    aa, ba = asserts(a), asserts(b)
    lost = [x for x in aa if x not in ba]
    gained = [x for x in ba if x not in aa]
    ai, bi = testids(a), testids(b)
    lost_tests = [x for x in ai if x not in bi]
    gained_tests = [x for x in bi if x not in ai]
    print('=' * 78)
    print(name, '| +%d/-%d lines | asserts %d -> %d' % (plus, minus, len(aa), len(ba)))
    if lost:
        print('  ASSERTS REMOVED (%d):' % len(lost))
        for x in lost:
            print('    -', x[:150])
    if gained:
        print('  asserts added (%d):' % len(gained))
        for x in gained:
            print('    +', x[:150])
    if lost_tests:
        print('  TEST IDS REMOVED (%d): %s' % (len(lost_tests), lost_tests))
    if gained_tests:
        print('  test ids added (%d): %s' % (len(gained_tests), gained_tests))
print('=' * 78)
print('total +%d / -%d lines across %d changed files' % (total_added, total_removed, len(CHANGED)))
