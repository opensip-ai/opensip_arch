"""Static inventory of every control id passed to check()/rejects()/rejects_because()/... in a
check-*.py source, taken from the AST (not a text grep), so ordering and duplicates are exact."""
import ast,sys,collections
from pathlib import Path
def ids(path):
    tree=ast.parse(Path(path).read_text());out=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.args:
            a=n.args[0]
            if isinstance(a,ast.Constant) and isinstance(a.value,str) and n.func.id in (
                    'check','rejects','rejects_because','not_admitted_because','admits','refuses'):
                out.append((n.func.id,a.value))
    return out
A,B=ids(sys.argv[1]),ids(sys.argv[2])
print('A',sys.argv[1],'call sites',len(A),'distinct ids',len({x[1] for x in A}))
print('B',sys.argv[2],'call sites',len(B),'distinct ids',len({x[1] for x in B}))
sa,sb=collections.Counter(x[1] for x in A),collections.Counter(x[1] for x in B)
only_a=sorted((sa-sb).elements());only_b=sorted((sb-sa).elements())
print('ONLY IN A (removed):',len(only_a));[print('   -',x) for x in only_a]
print('ONLY IN B (added):  ',len(only_b));[print('   +',x) for x in only_b]
common=[x for x in A if sb.get(x[1])]
print('order of shared ids preserved:',[x for x in A if x[1] not in only_a]==[x for x in B if x[1] not in only_b])
print('duplicate ids in B:',{k:v for k,v in sb.items() if v>1})
