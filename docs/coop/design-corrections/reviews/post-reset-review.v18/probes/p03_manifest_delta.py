"""p03: independent v17->v18 manifest delta, and exact AST equality proof of the checker
outside the ten guarded comparisons."""
import ast, hashlib, json

R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
v17 = json.load(open(R + 'candidate-subject.v17.json'))
v18 = json.load(open(R + 'candidate-subject.v18.json'))
print('v17 predecessor decl:', v17.get('predecessorManifestSha256'))
print('v18 declares predecessor:', v18['predecessorManifestSha256'])
print('actual sha256 of v17 manifest:',
      hashlib.sha256(open(R + 'candidate-subject.v17.json', 'rb').read()).hexdigest())

a = {e['path']: (e['sha256'], e['bytes']) for e in v17['files']}
b = {e['path']: (e['sha256'], e['bytes']) for e in v18['files']}
added = sorted(set(b) - set(a))
removed = sorted(set(a) - set(b))
changed = sorted(p for p in set(a) & set(b) if a[p] != b[p])
print('v17 files=%d  v18 files=%d' % (len(a), len(b)))
print('added=%d removed=%d changed=%d' % (len(added), len(removed), len(changed)))
for p in added:
    print('ADDED  ', p, b[p][1])
for p in removed:
    print('REMOVED', p, a[p][1])
for p in changed:
    print('CHANGED', p, a[p], '->', b[p])

# ---- exact AST proof: rewrite each new guard back to its old defaulting form and
# require the resulting AST to be identical to the v17 file's AST.
BEFORE = R + 'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
AFTER = '/tmp/opensip-design-corrections/candidate-subject.v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
old_src, new_src = open(BEFORE).read(), open(AFTER).read()


class Rollback(ast.NodeTransformer):
    """Rewrite  ('k' in D and <cmp>)  ->  <cmp>  , counting each rollback."""

    def __init__(self):
        self.n = 0
        self.sites = []

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if (isinstance(node.op, ast.And) and len(node.values) == 2
                and isinstance(node.values[0], ast.Compare)
                and len(node.values[0].ops) == 1
                and isinstance(node.values[0].ops[0], ast.In)
                and isinstance(node.values[0].left, ast.Constant)):
            self.n += 1
            self.sites.append((node.lineno, ast.unparse(node.values[0])))
            return node.values[1]
        return node


tree_new = ast.parse(new_src)
rb = Rollback()
tree_rolled = ast.fix_missing_locations(rb.visit(tree_new))
tree_old = ast.parse(old_src)
eq = ast.dump(tree_rolled) == ast.dump(tree_old)
print('\nrollbacksApplied=%d' % rb.n)
for ln, s in rb.sites:
    print('  guardSite line=%s test=%s' % (ln, s))
print('rolledBackNewAST == oldAST :', eq)

# how many "'k' in D and ..." forms already existed in v17 (must be 0 for the count to mean 10 new)
pre = Rollback()
pre.visit(ast.parse(old_src))
print('preExistingSameShapeInV17=%d' % pre.n)
