
"""Claude follow-up: CR-12 custody-divergence counterexample through the real composition."""
import argparse,importlib.util,json,sys,copy
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--label',required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
D=a.source/'docs/coop/design-corrections'
K=load('audit_security_checks',D/'security/check-security-lifecycle.v1.py');S=K.model
N=load('audit_native',D/'native/native_evidence_model.v2.py')
DD=load('audit_dd',D/'discovery-defaults.py')
R='/home/alice/big'
def scenario(total,bad_dir=0,bad_marker=0):
    ctx=K._synthetic_repo(total,0)
    names=sorted(k for k in ctx['fs'] if k.startswith(R+'/pkg') and k.endswith('/package.json'))
    for i in range(bad_dir):
        d=names[i].rsplit('/',1)[0]; ctx['fs'][d]['mode']='0757'
    for i in range(bad_dir,bad_dir+bad_marker):
        ctx['fs'][names[i]]['nlink']=2
    return ctx
def markers_of(ctx):
    return {k[len(R)+1:]:{'sha256':'a'*64} for k in ctx['fs'] if k.startswith(R+'/') and k.endswith('/package.json')}
rows=[]
for label,total,bd,bm in [('4200-clean',4200,0,0),('4200-150-dir-custody',4200,150,0),('4200-150-marker-custody',4200,0,150),('4096-clean',4096,0,0),('4200-150-mixed',4200,75,75)]:
    ctx=scenario(total,bd,bm)
    sec=S.discovery(ctx)
    row={'scenario':label,'markerDirsSupplied':total+1,'securityStatus':sec['status'],'securityRefusal':sec.get('refusal'),'securityDetail':sec.get('detail')}
    if sec['status']=='ACCEPT':
        prov=sec['provenance']
        row['securityUnits']=len(prov['units'])
        row['securityExcluded']=len(prov['excludedUnits'])
        try:
            b=S.boundary_inventory(sec)
            row['boundaryCustodyExcluded']=len(b['custodyExcludedUnits'])
            row['boundaryPruned']=len(b['prunedTrees'])
            nat=N.discover_units(markers_of(ctx),None,b)
            row['nativeUnits']=len(nat['units']);row['nativeRefused']=nat['refused']['detail'] if nat['refused'] else None
            row['nativeBoundaryExcluded']=len(nat['boundaries']['excludedUnits']) if nat.get('boundaries') else None
        except Exception as e:
            row['compositionError']=type(e).__name__+':'+str(e)[:120]
    else:
        row['securityUnits']=len(sec['provenance']['units'])
        try:
            S.boundary_inventory(sec); row['boundaryOnRefuse']='EXPORTED'
        except Exception as e:
            row['boundaryOnRefuse']=type(e).__name__+':'+str(e)[:80]
        nat=N.discover_units(markers_of(ctx),None,None)
        row['nativeUnitsNoBoundary']=len(nat['units']);row['nativeRefusedNoBoundary']=nat['refused']['detail'] if nat['refused'] else None
    rows.append(row)
a.out.write_text(json.dumps({'standing':'CLAUDE follow-up observation','tree':a.label,'source':str(a.source),'rows':rows},indent=2)+chr(10))
for r in rows: print(json.dumps(r))
