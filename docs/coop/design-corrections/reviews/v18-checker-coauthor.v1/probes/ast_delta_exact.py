"""Decisive AST check: enumerate every Compare node in both files. The proposal must (a) preserve
every original Compare unchanged as a sub-expression, and (b) add exactly ten new
Compare(In, <key literal>, <expectation dict>) nodes, each conjoined by a BoolOp(And) whose second
operand is the original comparison. Nothing else may change."""
import ast, json, pathlib
B = pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v17/docs/coop/design-corrections/workflows/check_workflows.v1.py')
A = pathlib.Path('/tmp/opensip-design-corrections/v18-checker-proposal.v1/proposal/docs/coop/design-corrections/workflows/check_workflows.v1.py')
tb, ta = ast.parse(B.read_text()), ast.parse(A.read_text())

def compares(t):
    return sorted(ast.unparse(n) for n in ast.walk(t) if isinstance(n, ast.Compare))
cb, ca = compares(tb), compares(ta)
added = sorted((ca_ := list(ca)) and [c for c in ca if ca.count(c) > cb.count(c)] or [])
removed = [c for c in cb if cb.count(c) > ca.count(c)]

# the ten new guards, as BoolOp(And) whose FIRST operand is an `in` membership test
guards = []
for n in ast.walk(ta):
    if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.And) and len(n.values) == 2:
        first = n.values[0]
        if isinstance(first, ast.Compare) and len(first.ops) == 1 and isinstance(first.ops[0], ast.In) \
           and isinstance(first.left, ast.Constant):
            if ast.unparse(n) not in [ast.unparse(x) for x in ast.walk(tb) if isinstance(x, ast.BoolOp)]:
                guards.append({'line': n.lineno, 'key': first.left.value,
                               'membershipOn': ast.unparse(first.comparators[0]),
                               'secondOperandIsOriginalComparison': ast.unparse(n.values[1]) in cb,
                               'guard': ast.unparse(n)[:150]})
guards.sort(key=lambda g: g['line'])
print(json.dumps({
 'standing': __doc__,
 'comparesBefore': len(cb), 'comparesAfter': len(ca),
 'originalComparesRemoved': removed,
 'newGuards': len(guards),
 'guardLines': [g['line'] for g in guards],
 'everyGuardKeyMatchesTheGetKey': all(g['key'] in ('refusal', 'recoverRefusal') for g in guards),
 'everyGuardPreservesOriginalComparison': all(g['secondOperandIsOriginalComparison'] for g in guards),
 'guards': guards}, indent=1))
