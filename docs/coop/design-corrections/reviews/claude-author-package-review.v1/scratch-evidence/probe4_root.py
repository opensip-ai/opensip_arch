
import importlib.util,json
from pathlib import Path
SRC=Path('/tmp/opensip-design-corrections/candidate-subject.v25')
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
DD=load('dd',SRC/'docs/coop/design-corrections/discovery-defaults.py')
N=load('nev',SRC/'docs/coop/design-corrections/native/native_evidence_model.v2.py')
print('INTERNAL_ROOT=',repr(DD.INTERNAL_ROOT),' ROOT_SENTINEL=',repr(DD.ROOT_SENTINEL))
print('spell_root(INTERNAL_ROOT)=',repr(DD.spell_root(DD.INTERNAL_ROOT)))
print('normalize_explicit_root(".")=',repr(DD.normalize_explicit_root('.')))
files=['src/a.ts','src/b.ts','index.ts']
print()
print('membership containment _under_unit(path, root):')
for root in ['', '.']:
    res=[(f,N._under_unit(f,root)) for f in files]
    print('  rootPath='+repr(root),'->',res)
print()
print('relative path _rel(path, root):')
for root in ['', '.']:
    try: print('  rootPath='+repr(root),'->',[N._rel(f,root) for f in files])
    except Exception as e: print('  rootPath='+repr(root),'-> ERROR',e)
print()
print('enumerate_units over marker tsconfig.json at top level:')
print(' ',DD.enumerate_units(['tsconfig.json']))
print()
print('depth tiebreak key len(rootPath): root-as-empty=',len(''),' root-as-dot=',len('.'),' sibling unit "a"=',len('a'))
print('  -> with ".", the root unit ties in depth with a real one-character unit dir.')
import jsonschema
sch=json.loads((SRC/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())
wu=sch['$defs']['WorkspaceUnitV2']
base={k:v for k,v in sch.items() if k.startswith('$')}
for root in ['', '.']:
    unit={'unitOrdinal':0,'rootPath':root,'languageFamily':'tsjs','languageMode':'ts-tsconfig',
      'unitKind':'ts-program','markerPath':'tsconfig.json','markerSha256':'0'*64,
      'recognizerId':'ts','recognizerVersion':1,'provenance':'DISCOVERED','memberPackageRoots':[]}
    v=dict(base);v.update(wu)
    try:
        jsonschema.Draft202012Validator(v).validate(unit);print('  schema accepts rootPath='+repr(root),'-> VALID')
    except Exception as e:
        print('  schema rejects rootPath='+repr(root),'->',str(e)[:120])
