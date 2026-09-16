from pathlib import Path
import argparse,importlib.util,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists()
f=a.source/'docs/coop/design-corrections/foundation/check-provider-attribution-return.v2.py';s=importlib.util.spec_from_file_location('fixture',f);F=importlib.util.module_from_spec(s);s.loader.exec_module(F);rows=[]
for kind in ['unknown','file','symbol']:
 for occ in ['external','unknown']:
  for logical in [None,'src/hint.ts']:
   resolved='mod:opaque-thing';fid=F.fact2('1');args=F.owners(fid,resolved=resolved);c=F.companion(0,resolved=resolved,kind=kind,occupancy=occ,logical=logical,exported='unknown' if kind=='symbol' else None);batch=F.batch([F.candidate(0,resolved)],[c]);row={'kind':kind,'occupancy':occ,'logicalPath':logical,'contractAllows':logical is None or kind in ['file','symbol'],'fixtureTCB':'synthetic stage/fact/custody inputs; this is actual buffer/bind/capture/atom boundary, not full Run or authenticated provider execution'}
   try:
    out=F.M.bind_worker_occupancy(batch,**args);row.update(result=out['status'],capturedRecords=out['records'],hostDerivedRefs=out['hostDerivedRefs']);assert out['status']=='admitted';assert out['records'][0]['logicalPath']==logical
   except F.M.ProviderReturnAdmissionError as e:row.update(result='refused',key=e.key,detail=e.detail)
   rows.append(row)
a.out.write_text(json.dumps({'standing':'Root actual provider-return and atom admission counterexample; precise boundary only, no full retained Run identity claim.','sourceRoot':str(a.source),'fixtureSha256':hashlib.sha256(f.read_bytes()).hexdigest(),'rows':rows},indent=2)+'\n');print([(x['kind'],x['occupancy'],x['logicalPath'],x['result'],x.get('key')) for x in rows])
