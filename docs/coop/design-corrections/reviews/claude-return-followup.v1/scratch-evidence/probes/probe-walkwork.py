
import argparse,importlib.util,json,sys,time,tracemalloc
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--label',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
D=a.source/'docs/coop/design-corrections'
K=load('audit_security_checks',D/'security/check-security-lifecycle.v1.py');S=K.model
rows=[]
for n in [4096,4200,20000,60000]:
    ctx=K._synthetic_repo(n,0)
    tracemalloc.start(); t0=time.perf_counter(); out=S.discovery(ctx); t1=time.perf_counter()
    cur,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    rows.append({'firstPartyDirs':n,'status':out['status'],'refusal':out.get('refusal'),'detail':out.get('detail'),
                 'units':len(out['provenance']['units']),'excluded':len(out['provenance']['excludedUnits']),
                 'discoverySeconds':round(t1-t0,4),'peakKiB':round(peak/1024)})
a.out.write_text(json.dumps({'tree':a.label,'rows':rows},indent=2)+chr(10))
for r in rows: print(json.dumps(r))
