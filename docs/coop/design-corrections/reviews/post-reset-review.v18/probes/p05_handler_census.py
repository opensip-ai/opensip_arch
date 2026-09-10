"""p05: fix the ancestor predicate, then census EVERY except-handler in the v18 checker for
any expected-vs-actual refusal comparison, in ANY shape, and classify its null-safety."""
import ast, json

AFTER = '/tmp/opensip-design-corrections/candidate-subject.v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
BEFORE = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
          'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py')


def analyse(path, label):
    tree = ast.parse(open(path).read())
    parent = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            parent[c] = n

    def ancestors(n):
        out = []
        while n in parent:
            n = parent[n]
            out.append(n)
        return out

    def guarded(key, node):
        for a in ancestors(node):
            if isinstance(a, ast.BoolOp) and isinstance(a.op, ast.And):
                for v in a.values:
                    if (isinstance(v, ast.Compare) and len(v.ops) == 1
                            and isinstance(v.ops[0], ast.In)
                            and isinstance(v.left, ast.Constant) and v.left.value == key):
                        return True
            if isinstance(a, ast.If):  # an enclosing `if 'refusal' in exp:` also guards
                t = a.test
                if (isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], ast.In)
                        and isinstance(t.left, ast.Constant) and t.left.value == key):
                    return True
        return False

    rows = []
    for h in [n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)]:
        hv = h.name
        reads = []
        for n in ast.walk(h):
            if not (isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq)):
                continue
            other_has_exc = lambda e: any(isinstance(x, ast.Name) and x.id == hv for x in ast.walk(e))
            for side, other in ((n.left, n.comparators[0]), (n.comparators[0], n.left)):
                if not other_has_exc(other):
                    continue
                key, form = None, None
                if (isinstance(side, ast.Call) and isinstance(side.func, ast.Attribute)
                        and side.func.attr == 'get' and side.args
                        and isinstance(side.args[0], ast.Constant)):
                    key, form = side.args[0].value, 'get-defaulting'
                elif (isinstance(side, ast.Subscript) and isinstance(side.slice, ast.Constant)
                      and isinstance(side.slice.value, str)):
                    key, form = side.slice.value, 'subscript-raises'
                if key is None:
                    continue
                reads.append({'line': n.lineno, 'key': key, 'form': form,
                              'guarded': guarded(key, n), 'expr': ast.unparse(n)[:110]})
        rows.append({'handlerLine': h.lineno, 'var': hv,
                     'firstStmt': ast.unparse(h.body[0]).splitlines()[0][:80],
                     'expectedComparisons': reads})

    print('=== %s ===' % label)
    print('handlers=%d' % len(rows))
    risky = []
    for r in rows:
        cmps = r['expectedComparisons']
        if not cmps:
            print('  line %-5s var=%-4s NO expected-refusal comparison | %s'
                  % (r['handlerLine'], r['var'], r['firstStmt']))
            continue
        for c in cmps:
            flag = 'GUARDED' if c['guarded'] else ('SAFE(raises)' if c['form'] == 'subscript-raises' else 'UNGUARDED-DEFAULTING')
            if flag == 'UNGUARDED-DEFAULTING':
                risky.append((r['handlerLine'], c))
            print('  line %-5s var=%-4s %-20s key=%-15s %s'
                  % (c['line'], r['var'], flag, c['key'], c['expr']))
    print('%s: unguardedDefaulting=%d' % (label, len(risky)))
    return rows, risky


rows_new, risky_new = analyse(AFTER, 'V18 (candidate)')
print()
rows_old, risky_old = analyse(BEFORE, 'V17 (predecessor)')
print('\nSUMMARY unguardedDefaulting  V17=%d  V18=%d' % (len(risky_old), len(risky_new)))
