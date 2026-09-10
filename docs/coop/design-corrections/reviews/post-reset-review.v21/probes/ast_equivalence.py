"""Independently test the claim that workflows_model.v1.py v20->v21 changed NO executable behaviour
(documentation only), and the same claim for run-reference-checks.py (which DID change code)."""
import ast,json,hashlib,sys,types
A='/tmp/opensip-design-corrections/candidate-subject.v20/docs/coop/design-corrections/'
B='/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections/'
def strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            body=node.body
            if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and isinstance(body[0].value.value,str):
                node.body=body[1:] or [ast.Pass()]
    return tree
def codeobj(path):
    return compile(open(path).read(),'<x>','exec')
def const_repr(co,depth=0):
    out=[co.co_name,co.co_names,co.co_varnames,co.co_argcount,list(co.co_code)]
    cs=[]
    for c in co.co_consts:
        if isinstance(c,types.CodeType): cs.append(const_repr(c,depth+1))
        elif isinstance(c,str) and depth>=0: cs.append(('STR',c))
        else: cs.append(repr(c))
    return (tuple(str(x) for x in out),tuple(str(x) for x in cs))
res={}
for f in ['workflows/workflows_model.v1.py','foundation/run-reference-checks.py','foundation/check-identity.py']:
    ta=strip_docstrings(ast.parse(open(A+f).read()))
    tb=strip_docstrings(ast.parse(open(B+f).read()))
    astEq=ast.dump(ta)==ast.dump(tb)
    coA,coB=codeobj(A+f),codeobj(B+f)
    # code objects INCLUDING docstrings (so a docstring change shows) and excluding them
    full=const_repr(coA)==const_repr(coB)
    res[f]={'sha20':hashlib.sha256(open(A+f,'rb').read()).hexdigest(),
            'sha21':hashlib.sha256(open(B+f,'rb').read()).hexdigest(),
            'bytes20':len(open(A+f,'rb').read()),'bytes21':len(open(B+f,'rb').read()),
            'astEqualModuloDocstrings':astEq,
            'codeObjectsFullyIdenticalIncludingDocstrings':full}
    # count comment-only vs code lines changed
    la=[l for l in open(A+f).read().splitlines()]
    lb=[l for l in open(B+f).read().splitlines()]
    import difflib
    added=[l for l in difflib.unified_diff(la,lb,lineterm='',n=0) if l.startswith('+') and not l.startswith('+++')]
    removed=[l for l in difflib.unified_diff(la,lb,lineterm='',n=0) if l.startswith('-') and not l.startswith('---')]
    def isnoncode(l):
        s=l[1:].strip()
        return s=='' or s.startswith('#')
    res[f]['diffAddedLines']=len(added); res[f]['diffRemovedLines']=len(removed)
    res[f]['addedNonCodeLines']=sum(1 for l in added if isnoncode(l))
    res[f]['removedNonCodeLines']=sum(1 for l in removed if isnoncode(l))
print(json.dumps(res,indent=1))
json.dump(res,open('/tmp/opensip-design-corrections/post-reset-review.v21/results/ast-equivalence.json','w'),indent=1)
