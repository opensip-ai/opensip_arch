"""W01: complete unified diffs of every changed file + assertion / test-id census."""
import ast
import difflib
import os

V2 = '/tmp/opensip-design-corrections/claude-application-tools-review.v2/inputs'
V3 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v3/inputs'
CHANGED = ['assemble-records.successor.v1.py', 'check-retain-public.v1.py',
           'freeze-application.py', 'prepare-validation.py',
           'retain-application-review.successor.v1.py', 'retain_public.py']


def asserts(src):
    return [ast.unparse(n.test) for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assert)]


def testids(src):
    ids = []
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in ('record', 'catch', 'negative') and n.args
                and isinstance(n.args[0], ast.Constant)):
            ids.append(n.args[0].value)
    return ids


BIG = {'assemble-records.successor.v1.py', 'check-retain-public.v1.py'}
tot_p = tot_m = 0
for name in CHANGED:
    a = open(os.path.join(V2, name)).read()
    b = open(os.path.join(V3, name)).read()
    al, bl = a.splitlines(), b.splitlines()
    d = list(difflib.unified_diff(al, bl, 'v2', 'v3', lineterm='', n=2))
    p = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    m = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    tot_p += p
    tot_m += m
    aa, ba = asserts(a), asserts(b)
    lost = [x for x in aa if x not in ba]
    gained = [x for x in ba if x not in aa]
    ai, bi = testids(a), testids(b)
    lost_t = [x for x in ai if x not in bi]
    gained_t = [x for x in bi if x not in ai]
    print('=' * 80)
    print('%s | +%d/-%d | asserts %d->%d | testids %d->%d' % (name, p, m, len(aa), len(ba), len(ai), len(bi)))
    if lost:
        print('  ASSERTS REMOVED (%d):' % len(lost))
        for x in lost:
            print('    -', x[:160])
    if gained:
        print('  asserts added (%d):' % len(gained))
        for x in gained:
            print('    +', x[:160])
    if lost_t:
        print('  TEST IDS REMOVED (%d): %s' % (len(lost_t), lost_t))
    if gained_t:
        print('  test ids added (%d): %s' % (len(gained_t), gained_t))
    if name not in BIG:
        print('  --- full diff ---')
        for l in d:
            print('   ', l)
    else:
        print('  --- diff hunks (headers only; regions read in full separately) ---')
        for l in d:
            if l.startswith('@@'):
                print('   ', l)
print('=' * 80)
print('TOTAL +%d / -%d across %d changed files' % (tot_p, tot_m, len(CHANGED)))
