"""p04: exact AST rollback proof restricted to the guard shape, plus an independent
sweep for EQUIVALENT unguarded defaulting expected-refusal comparisons still in v18."""
import ast, json

R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
BEFORE = R + 'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
AFTER = '/tmp/opensip-design-corrections/candidate-subject.v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
old_src, new_src = open(BEFORE).read(), open(AFTER).read()


def keys_read(node):
    """Constant string keys read out of any subscript or .get(...) inside node."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
            out.add(n.slice.value)
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'get'
                and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)):
            out.add(n.args[0].value)
    return out


class GuardRollback(ast.NodeTransformer):
    """Rewrite  (K in D and <rhs>) -> <rhs>  only where <rhs> actually reads key K.
    That is precisely the 'guard the key you are about to compare' shape."""

    def __init__(self):
        self.sites = []

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if (isinstance(node.op, ast.And) and len(node.values) == 2
                and isinstance(node.values[0], ast.Compare)
                and len(node.values[0].ops) == 1
                and isinstance(node.values[0].ops[0], ast.In)
                and isinstance(node.values[0].left, ast.Constant)
                and isinstance(node.values[0].left.value, str)):
            key = node.values[0].left.value
            if key in keys_read(node.values[1]):
                self.sites.append((node.lineno, ast.unparse(node.values[0]), key))
                return node.values[1]
        return node


new_t, old_t = ast.parse(new_src), ast.parse(old_src)
gn, go = GuardRollback(), GuardRollback()
new_rolled = ast.fix_missing_locations(gn.visit(new_t))
old_rolled = ast.fix_missing_locations(go.visit(old_t))
print('guardSitesInV18=%d  guardSitesInV17=%d' % (len(gn.sites), len(go.sites)))
for s in gn.sites:
    print('  V18 guard line=%-5s %s' % (s[0], s[1]))
print('rolledBack(V18) == parse(V17) :', ast.dump(new_rolled) == ast.dump(old_t))
print('rolledBack(V18) == rolledBack(V17):', ast.dump(new_rolled) == ast.dump(old_rolled))
print('guardKeys:', sorted({s[2] for s in gn.sites}))

# --------------------------------------------------------------------------------
# Independent sweep: any REMAINING comparison in v18 of the shape
#   <expdict>.get(K) == <exc>.detail     (or reversed)  that is NOT membership-guarded.
# These are the equivalent-missed candidates.
print('\n--- unguarded defaulting-comparison sweep over V18 ---')


def is_get(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'get'
            and len(n.args) == 1 and isinstance(n.args[0], ast.Constant))


def guarded_by(key, ancestors):
    for anc in ancestors:
        if isinstance(anc, ast.BoolOp) and isinstance(anc.op, ast.And):
            for v in anc.values:
                if (isinstance(v, ast.Compare) and len(v.ops) == 1 and isinstance(v.ops[0], ast.In)
                        and isinstance(v.left, ast.Constant) and v.left.value == key):
                    return True
    return False


findings = []
for handler in [n for n in ast.walk(new_t) if isinstance(n, ast.ExceptHandler)]:
    hname = handler.name
    stack = []

    def walk(node, anc):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Compare) and len(ch.ops) == 1 and isinstance(ch.ops[0], ast.Eq):
                for side, other in ((ch.left, ch.comparators[0]), (ch.comparators[0], ch.left)):
                    if is_get(side):
                        key = side.args[0].value
                        reads_exc = any(isinstance(x, ast.Name) and x.id == hname for x in ast.walk(other))
                        if reads_exc and not guarded_by(key, anc + [node, ch]):
                            findings.append({'line': ch.lineno, 'key': key,
                                             'expr': ast.unparse(ch), 'handlerVar': hname})
            walk(ch, anc + [node])

    walk(handler, [])

print('unguardedDefaultingComparisonsRemaining=%d' % len(findings))
for f in findings:
    print(' ', json.dumps(f))

# Also: every except-handler in the file, with whether it compares an expectation to exc detail.
handlers = [n for n in ast.walk(new_t) if isinstance(n, ast.ExceptHandler)]
print('\ntotalExceptHandlersInV18Checker=%d' % len(handlers))
refusal_handlers = []
for h in handlers:
    src = ast.unparse(h)
    if h.name and ('.detail' in src or 'detail' in src):
        refusal_handlers.append((h.lineno, h.name, src.splitlines()[0][:90]))
print('handlersReferencingDetail=%d' % len(refusal_handlers))
for x in refusal_handlers:
    print('  line=%-5s var=%-4s %s' % x)
