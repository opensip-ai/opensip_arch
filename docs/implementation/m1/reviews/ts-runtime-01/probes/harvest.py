import json,importlib.util,glob,random,time
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('meta',root/'docs/implementation/m1/metadata-v2/check_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ref,registry,docs=m.load(root)
seen={};files=0
for f in sorted(glob.glob(str(root/'docs/**/*.json'),recursive=True)):
    try: v=ref.parse(Path(f).read_bytes())
    except Exception: continue
    if isinstance(v,dict) and '$schema' in v: continue
    files+=1
    def walk(x):
        if isinstance(x,(dict,list)):
            try: k=ref.canonical(x)
            except Exception: return
            if len(k)<=20000: seen.setdefault(k,x)
            for c in (x.values() if isinstance(x,dict) else x): walk(c)
        elif isinstance(x,str) and len(x)<200: seen.setdefault(ref.canonical(x),x)
    walk(v)
vals=list(seen.values()); random.Random(7).shuffle(vals)
print('files',files,'distinct',len(vals))
refs=list(json.loads(Path('/tmp/opensip-implementation/m1-full-generator-trial-01/source-map.json').read_bytes())['selectedTargets'])
# prefilter: object values only against refs whose resolved top node mentions a shared property; others all refs
vs={r:ref.ExactValidator({'$ref':r},registry=registry) for r in refs}
chosen=vals[:2500]; rows=[]; t=time.time()
for i,x in enumerate(chosen):
    for r in refs:
        try: ok=vs[r].is_valid(x)
        except Exception as e: ok='PY '+type(e).__name__
        rows.append([r,i,ok])
    if time.time()-t>420: break
Path('harvest-cases.json').write_text(json.dumps({'values':chosen[:i+1],'rows':rows}))
print('values',i+1,'rows',len(rows),'valid',sum(1 for r in rows if r[2] is True),'refsValid',len({r[0] for r in rows if r[2] is True}),'pyExc',sum(1 for r in rows if isinstance(r[2],str)))
