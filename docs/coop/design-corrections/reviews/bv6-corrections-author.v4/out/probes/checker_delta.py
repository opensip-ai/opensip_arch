"""What executable change the checker patch actually makes, beyond the removed control."""
import ast, json, pathlib
B = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')
A = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4/work')
P = 'docs/coop/design-corrections/workflows/check_workflows.v1.py'

def calls(src):
    t = ast.parse(src)
    out = []
    for n in ast.walk(t):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
           and n.func.id in ('check', 'must_valid', 'must_invalid', 'rejects_because'):
            first = n.args[0] if n.args else None
            out.append((n.func.id, first.value if isinstance(first, ast.Constant) else '<dynamic>'))
    return out
cb, ca = calls((B / P).read_text()), calls((A / P).read_text())
removed = [c for c in cb if c not in ca]
added = [c for c in ca if c not in cb]
# and the whole-AST statement counts, so a silent second edit would show
sb = sum(1 for _ in ast.walk(ast.parse((B / P).read_text())))
sa = sum(1 for _ in ast.walk(ast.parse((A / P).read_text())))
print(json.dumps({
 'standing': 'Static AST inspection of the checker patch. Literal control ids only; dynamic ids '
             '(f-string/concatenated) are reported as <dynamic> and are not enumerated here.',
 'staticCallSitesBefore': len(cb), 'staticCallSitesAfter': len(ca),
 'removedLiteralIds': [c[1] for c in removed], 'addedLiteralIds': [c[1] for c in added],
 'totalAstNodesBefore': sb, 'totalAstNodesAfter': sa,
 'note': 'A call-site count is not the runtime row count: several sites are inside loops and '
         'contribute many rows each.'}, indent=1))
