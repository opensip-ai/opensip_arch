"""BV6-V4-CR-1 verification: the edit is comment-only and the new wording agrees with its owning
contexts. Limits: AST equality proves no executable change; it says nothing about whether the new
prose is CORRECT, which is reviewed by reading. No suite was run."""
import ast, hashlib, json, pathlib
B = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4/work')
A = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v5/work')
P = 'docs/coop/design-corrections/workflows/check_workflows.v1.py'
b, a = (B / P).read_text(), (A / P).read_text()

def calls(src):
    return [n.args[0].value for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in ('check', 'must_valid', 'must_invalid', 'rejects_because')
            and n.args and isinstance(n.args[0], ast.Constant)]

out = {
 'standing': __doc__,
 'file': P,
 'beforeSha256': hashlib.sha256(b.encode()).hexdigest(),
 'afterSha256': hashlib.sha256(a.encode()).hexdigest(),
 'bytesChanged': b != a,
 'fullAstIdenticalIncludingDocstrings': ast.dump(ast.parse(b)) == ast.dump(ast.parse(a)),
 'literalControlIdsIdentical': calls(b) == calls(a),
 'controlIdCount': len(calls(a)),
 'onlyCommentLinesDiffer': [i + 1 for i, (x, y) in enumerate(zip(b.split('\n'), a.split('\n'))) if x != y],
 'everyDifferingLineIsAComment': all(
     l.lstrip().startswith('#')
     for pair in zip(b.split('\n'), a.split('\n')) if pair[0] != pair[1] for l in pair),
 'lineCountUnchanged': len(b.split('\n')) == len(a.split('\n')),
}
print(json.dumps(out, indent=1))
