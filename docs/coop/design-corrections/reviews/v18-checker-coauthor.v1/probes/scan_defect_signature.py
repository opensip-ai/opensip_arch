"""The defect signature, encoded precisely: a comparison is FALSE-PASS-CAPABLE only when the
EXPECTATION side is a defaulting .get (absent key silently becomes None) AND the comparison is
control-flow-selected by an exception having been raised. Where the expectation is INDEXED, an
absent key raises KeyError and fails loudly instead.

Limit: static analysis over one file. It identifies shapes; reachability is judged from the corpus."""
import ast, json, sys, pathlib
SRC = pathlib.Path(sys.argv[1]); tree = ast.parse(SRC.read_text())
lines = SRC.read_text().split('\n')
EXPECT_ROOTS = {'exp', 'expect', 'g', 'ex'}

def get_call(n):
    return n if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and n.func.attr == 'get' and len(n.args) == 1) else None

def names_expectation(n):
    """Does this expression read the CASE EXPECTATION rather than the observed result?"""
    src = ast.unparse(n)
    return (src.split('.')[0].split('[')[0] in EXPECT_ROOTS
            or "['expect']" in src or '"expect"' in src)

in_handler = {}
for node in ast.walk(tree):
    if isinstance(node, ast.ExceptHandler):
        for sub in ast.walk(node):
            in_handler[id(sub)] = node.lineno

rows = []
for node in ast.walk(tree):
    if not isinstance(node, ast.Compare) or len(node.ops) != 1 or not isinstance(node.ops[0], ast.Eq):
        continue
    for side in (node.left, node.comparators[0]):
        g = get_call(side)
        if not g:
            continue
        expectation_side = names_expectation(g.func.value)
        rows.append({'line': node.lineno,
                     'expectationSideIsDefaultingGet': expectation_side,
                     'inExceptHandlerAtLine': in_handler.get(id(node)),
                     'defectSignature': bool(expectation_side and in_handler.get(id(node))),
                     'key': g.args[0].value if isinstance(g.args[0], ast.Constant) else None,
                     'source': lines[node.lineno - 1].strip()[:120]})
hit = [r for r in rows if r['defectSignature']]
other_exp = [r for r in rows if r['expectationSideIsDefaultingGet'] and not r['inExceptHandlerAtLine']]
print(json.dumps({'standing': __doc__, 'file': str(SRC),
 'matchingDefectSignature': len(hit), 'lines': sorted(r['line'] for r in hit),
 'keys': sorted({r['key'] for r in hit}),
 'expectationSideGetOutsideHandler': [{'line': r['line'], 'source': r['source']} for r in other_exp],
 'rows': hit}, indent=1))
