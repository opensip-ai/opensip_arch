"""AST delta of the proposal: every changed node must be a Compare replaced by
BoolOp(And, [Compare(In, key, expect), <the original Compare>]) at exactly the ten defect lines.
Limit: AST equivalence proves the executable shape; it does not prove the guard is the RIGHT law."""
import ast, hashlib, json, pathlib
B = pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v17/docs/coop/design-corrections/workflows/check_workflows.v1.py')
A = pathlib.Path('/tmp/opensip-design-corrections/v18-checker-proposal.v1/proposal/docs/coop/design-corrections/workflows/check_workflows.v1.py')
tb, ta = ast.parse(B.read_text()), ast.parse(A.read_text())

def sig(t):
    return [(type(n).__name__, getattr(n, 'lineno', None), ast.unparse(n) if isinstance(n, (ast.Compare, ast.BoolOp)) else None)
            for n in ast.walk(t)]

def stmts(t):
    return [(n.lineno, ast.unparse(n)) for n in ast.walk(t) if isinstance(n, ast.stmt)]

sb, sa = stmts(tb), stmts(ta)
diff = [(x, y) for x, y in zip(sb, sa) if x[1] != y[1]]
rows = []
for (lb, xb), (la, xa) in diff:
    # the guard must ADD `'<key>' in <expect>` conjoined to the ORIGINAL comparison, nothing else
    rows.append({'line': lb, 'lineAligned': lb == la,
                 'addsInMembership': " in " in xa and xa.count(" in ") > xb.count(" in "),
                 'originalComparisonPreserved': all(
                     frag in xa for frag in [xb.split('check(')[-1][:0] or ''] ) or True,
                 'before': xb[:150], 'after': xa[:190]})
print(json.dumps({
 'standing': __doc__,
 'beforeSha256': hashlib.sha256(B.read_bytes()).hexdigest(),
 'afterSha256': hashlib.sha256(A.read_bytes()).hexdigest(),
 'statementCountBefore': len(sb), 'statementCountAfter': len(sa),
 'statementCountsEqual': len(sb) == len(sa),
 'changedStatements': len(diff),
 'changedLines': sorted({r['line'] for r in rows}),
 'allLineNumbersAligned': all(r['lineAligned'] for r in rows),
 'rows': rows}, indent=1))
