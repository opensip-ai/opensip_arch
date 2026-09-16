from pathlib import Path
import types,json
HERE=Path(__file__).resolve().parent
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');R=load(HERE/'retained_fixture.py','r')
with R.world(V.read_unit,V.subjects) as w:
 plan=w['objects'][w['run']['planId']][1]
 print(json.dumps({'runId':w['rid'],'plan':plan,'findingIds':w['objects'][w['run']['evidenceId']][1]['findingIds'],'configurationBlob':plan['resolvedConfigDigest'] in w['blobs'],'blobType':type(w['blobs'].get(plan['resolvedConfigDigest'])).__name__},indent=2))
