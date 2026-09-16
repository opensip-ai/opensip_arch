
import argparse,importlib.util,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
D=a.source/'docs/coop/design-corrections'
K=load('audit_security_checks',D/'security/check-security-lifecycle.v1.py');S=K.model
N=load('audit_native',D/'native/native_evidence_model.v2.py')
DD=load('audit_dd',D/'discovery-defaults.py')
R='/home/alice/big'
def markers_of(ctx):
    return {k[len(R)+1:]:{'sha256':'a'*64} for k in ctx['fs'] if k.startswith(R+'/') and k.endswith('/package.json')}
rows=[]
def run(label,mutate):
    ctx=K._synthetic_repo(1,0); mutate(ctx)
    sec=S.discovery(ctx)
    row={'case':label,'securityStatus':sec['status'],'prunedTrees':sec['provenance']['prunedTrees'],'units':len(sec['provenance']['units'])}
    if sec['status']=='ACCEPT':
        b=S.boundary_inventory(sec); row['boundaryPruned']=b['prunedTrees']
        nat=N.discover_units(markers_of(ctx),None,b)
        row['nativePruned']=nat['prunedTrees']; row['nativeUnits']=len(nat['units'])
        row['boundaryMismatchIfHostAddsAnchor']=None
    rows.append(row)
def empty_nm(ctx):
    ctx['fs'][R+'/node_modules']={'kind':'dir','uid':1000,'mode':'0755','dev':1}
    ctx['fs'][R+'/node_modules/dep0000']={'kind':'dir','uid':1000,'mode':'0755','dev':1}
def nm_with_marker(ctx):
    empty_nm(ctx)
    ctx['fs'][R+'/node_modules/dep0000/package.json']={'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}
def nm_nonmarker_only(ctx):
    empty_nm(ctx)
    ctx['fs'][R+'/node_modules/dep0000/index.js']={'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}
run('node_modules dir present, no descendant at all',empty_nm)
run('node_modules with one package.json',nm_with_marker)
run('node_modules with only non-marker files',nm_nonmarker_only)
mism=None
try:
    ctx=K._synthetic_repo(1,0); nm_with_marker(ctx); sec=S.discovery(ctx); b=S.boundary_inventory(sec)
    b2=json.loads(json.dumps(b)); b2['prunedTrees'][0]['markerCount']=99
    nat=N.discover_units(markers_of(ctx),None,b2)
    mism=nat['refused']['detail'] if nat['refused'] else 'ACCEPTED-MISMATCH'
except Exception as e: mism=type(e).__name__+':'+str(e)[:100]
rows.append({'case':'markerCount tampered in boundary inventory','nativeResult':mism})
a.out.write_text(json.dumps({'standing':'CLAUDE follow-up','rows':rows},indent=2)+chr(10))
for r in rows: print(json.dumps(r))
