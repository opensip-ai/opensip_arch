"""Independent check of root's behavioural claim for the two .py files in the patch: the executable
AST is unchanged once docstrings are stripped.

Docstrings are STRIPPED, not ignored wholesale - only a leading string-literal Expr in a
module/class/function body is removed - so any OTHER string literal or expression change would
still show as a difference. Comments never reach the AST, which is why they are invisible here and
must be reviewed as prose separately."""
import ast, hashlib, json, pathlib

BEFORE = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')
AFTER = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4/work')
PROP = json.loads((AFTER.parent / 'root-input/proposal.json').read_text())

def strip(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
               and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return tree

def dump(src):
    return ast.dump(strip(ast.parse(src)), annotate_fields=True, include_attributes=False)

rows = []
for f in PROP['files']:
    if not f['path'].endswith('.py'):
        continue
    b = (BEFORE / f['path']).read_bytes()
    a = (AFTER / f['path']).read_bytes()
    bh, ah = hashlib.sha256(b).hexdigest(), hashlib.sha256(a).hexdigest()
    db, da = dump(b.decode()), dump(a.decode())
    rows.append({
        'path': f['path'],
        'beforeSha256': bh, 'beforeMatchesProposal': bh == f['beforeSha256'],
        'afterSha256': ah, 'afterMatchesProposal': ah == f['afterSha256'],
        'bytesChanged': bh != ah,
        'executableAstIdenticalAfterStrippingDocstrings': db == da,
        'astWithDocstringsIdentical': ast.dump(ast.parse(b.decode())) == ast.dump(ast.parse(a.decode())),
    })
print(json.dumps({
 'standing': 'Coauthor verification of the proposal behavioural claim. AST equivalence over the two '
             'changed .py files only; it is not a semantic or host proof and says nothing about the '
             'three non-.py files.',
 'method': 'Leading string-literal Expr removed from module/class/function bodies; every other '
           'literal and expression retained. Comments are not AST nodes and are reviewed as prose.',
 'files': rows}, indent=1))
