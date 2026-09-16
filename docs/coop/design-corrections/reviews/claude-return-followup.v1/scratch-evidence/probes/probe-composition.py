
import argparse,importlib.util,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
D=a.source/'docs/coop/design-corrections'
K=load('audit_security_checks',D/'security/check-security-lifecycle.v1.py');S=K.model
N=load('audit_native',D/'native/native_evidence_model.v2.py')
R='/home/alice/big'
def markers_of(ctx):
    return {k[len(R)+1:]:{'sha256':'a'*64} for k in ctx['fs'] if k.startswith(R+'/') and k.endswith('/package.json')}
rows=[]
ctx=K._synthetic_repo(4200,0)
names=sorted(k for k in ctx['fs'] if k.startswith(R+'/pkg') and k.endswith('/package.json'))
for i in range(150): ctx['fs'][names[i].rsplit('/',1)[0]]['mode']='0757'
sec=S.discovery(ctx); b=S.boundary_inventory(sec)
withb=N.discover_units(markers_of(ctx),None,b)
without=N.discover_units(markers_of(ctx),None,None)
rows.append({'case':'custody150','securityUnits':len(sec['provenance']['units']),
             'nativeWithBoundary':len(withb['units']),'nativeWithBoundaryRefused':withb['refused'],
             'nativeNoBoundary':len(without['units']),'nativeNoBoundaryRefused':without['refused']['detail'] if without['refused'] else None})
deep=K._synthetic_repo(3,0)
seg='/'.join('d%03d'%i for i in range(300))
dd={'kind':'dir','uid':1000,'mode':'0755','dev':1}
acc=R
for part in seg.split('/'):
    acc=acc+'/'+part; deep['fs'][acc]=dict(dd)
deep['fs'][acc+'/package.json']={'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}
sec2=S.discovery(deep); b2=S.boundary_inventory(sec2)
n2=N.discover_units(markers_of(deep),None,b2)
n2b=N.discover_units(markers_of(deep),None,None)
rows.append({'case':'depth300','securityStatus':sec2['status'],'securityUnits':len(sec2['provenance']['units']),
             'securityExcludedReasons':sorted({r['reason'] for r in sec2['provenance']['excludedUnits']}),
             'boundaryCustodyExcluded':len(b2['custodyExcludedUnits']),
             'nativeWithBoundary':len(n2['units']),'nativeNoBoundary':len(n2b['units'])})
a.out.write_text(json.dumps({'standing':'CLAUDE follow-up','rows':rows},indent=2)+chr(10))
for r in rows: print(json.dumps(r))
