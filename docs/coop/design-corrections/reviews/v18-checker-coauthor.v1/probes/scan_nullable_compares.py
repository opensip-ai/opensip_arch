"""Systematic AST scan of THIS checker for every comparison that can false-match on None==None,
whether or not it sits in an exception handler. The proposal fixes ten; this asks whether ten is
the complete set. Limit: static analysis. It flags shapes that CAN false-match; whether each is
reachable is judged by reading the case corpus."""
import ast, json, sys, pathlib
SRC = pathlib.Path(sys.argv[1])
tree = ast.parse(SRC.read_text())
lines = SRC.read_text().split('\n')

def is_get(n):
    return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == 'get' and len(n.args) == 1)

handlers = {}
for node in ast.walk(tree):
    if isinstance(node, ast.ExceptHandler):
        for sub in ast.walk(node):
            handlers[id(sub)] = node.lineno

rows = []
for node in ast.walk(tree):
    if not isinstance(node, ast.Compare) or len(node.ops) != 1 or not isinstance(node.ops[0], ast.Eq):
        continue
    left, right = node.left, node.comparators[0]
    sides = [(left, 'left'), (right, 'right')]
    getsides = [(n, s) for n, s in sides if is_get(n)]
    if not getsides:
        continue
    # a .get with an explicit default cannot yield an implicit None
    defaulted = any(len(n.args) > 1 for n, _ in getsides)
    other = [n for n, _ in sides if not is_get(n)]
    # a literal on the other side can never be None, so no false match
    other_is_literal = other and isinstance(other[0], ast.Constant) and other[0].value is not None
    rows.append({
        'line': node.lineno,
        'source': lines[node.lineno - 1].strip()[:150],
        'inExceptHandlerAtLine': handlers.get(id(node)),
        'getKeys': [n.args[0].value for n, _ in getsides if isinstance(n.args[0], ast.Constant)],
        'otherSideIsNonNoneLiteral': bool(other_is_literal),
        'hasExplicitDefault': defaulted,
        'canFalseMatchOnNone': not other_is_literal and not defaulted,
    })
rows.sort(key=lambda r: r['line'])
risky = [r for r in rows if r['canFalseMatchOnNone']]
print(json.dumps({
 'standing': __doc__,
 'file': str(SRC), 'totalGetEqComparisons': len(rows),
 'canFalseMatchOnNone': len(risky),
 'inExceptHandler': len([r for r in risky if r['inExceptHandlerAtLine']]),
 'outsideExceptHandler': len([r for r in risky if not r['inExceptHandlerAtLine']]),
 'rows': risky}, indent=1))
