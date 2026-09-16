
import argparse,importlib.util,json,sys,time,tracemalloc
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--label',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
D=a.source/'docs/coop/design-corrections'
DD=load('audit_dd',D/'discovery-defaults.py')
import inspect
sig=str(inspect.signature(DD.enumerate_units))
rows=[]
for n in [4096,4200,50000,200000]:
    markers=['pkg%07d/package.json'%i for i in range(n)]
    tracemalloc.start()
    t0=time.perf_counter(); out=DD.enumerate_units(markers); t1=time.perf_counter()
    cur,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    rows.append({'markers':n,'signature':sig,'refusal':out['refusal']['detail'] if out['refusal'] else None,
                 'unitDirsReturned':len(out['unitDirs']),'seconds':round(t1-t0,4),'peakKiB':round(peak/1024)})
    if 'enforce_limit' in sig:
        t0=time.perf_counter(); out2=DD.enumerate_units(markers,enforce_limit=False); t1=time.perf_counter()
        rows[-1]['noLimitSeconds']=round(t1-t0,4); rows[-1]['noLimitUnitDirs']=len(out2['unitDirs'])
a.out.write_text(json.dumps({'tree':a.label,'rows':rows},indent=2)+chr(10))
for r in rows: print(json.dumps(r))
