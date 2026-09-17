from pathlib import Path
import argparse,json,hashlib,tarfile,lzma,importlib.util,sys,unicodedata,copy
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();S=Path(__file__).resolve().parent;O=Path(a.output);assert not O.exists();O.mkdir(parents=True)
assert sys.version_info[:3]==(3,12,13)and unicodedata.unidata_version=='15.0.0'and sys.flags.int_max_str_digits==0 and sys.get_int_max_str_digits()==0
rows=json.loads((S/'reference-fixture.json').read_bytes())['files'];assert len(rows)==159;expected={r['path']:r for r in rows};assert len(expected)==159
with tarfile.open(S/'reference-fixture.tar.xz','r:xz')as tar:
 members=tar.getmembers();assert len(members)==159 and {m.name for m in members}==set(expected)
 for m in members:
  assert m.isfile()and not m.name.startswith('/')and all(p not in ['','..','.']for p in m.name.split('/'));raw=tar.extractfile(m).read();r=expected[m.name];assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256']);p=O/'reference'/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
F=O/'reference/archroot/docs/coop/design-corrections/foundation';path=F/'evaluator_input_model.v3.py';old=path.read_bytes();assert old==(S/'predecessor.py').read_bytes();needle=b"closures={key:value for key,(domain,value) in objects.items() if domain=='closure'}";replacement=b"closures={key:objects[key][1] for key in plan['semanticClosures']}";assert old.count(needle)==1;new=(S/'candidate.py').read_bytes();assert new==old.replace(needle,replacement)
def load(name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
I=load('closure49_old');path.write_bytes(new);N=load('closure49_new');M=I.ENUM.IM
raw=lzma.decompress((S/'cases.ndjson.xz').read_bytes());r=json.loads((S/'cases-pin.json').read_bytes());assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256']);cases=[json.loads(l)for l in raw.splitlines()];changed=[];admit=0;refuse=0;original_owner_count=0
for q in cases:
 objects={r['id']:(r['domain'],r['descriptor'])for r in q['objects']};blobs={r['digest']:bytes.fromhex(r['hex'])for r in q['blobs']};owner=q['owner']
 if q['label'].endswith('-original'):
  run=q['ownerRun'];_,actual=M.open_run_closure(run,objects,blobs);actual={k:actual[k]for k in owner};assert json.loads(json.dumps(actual))==owner;original_owner_count+=1
 def derive(mod):
  try:
   normal,evidence=mod.reconstruct(q['planId'],q['executionId'],q['evaluatorClosure'],q['inputRefs'],objects,blobs,owner,M);evidence.pop('blobs');return {'normalized':normal,'evidence':evidence}
  except Exception as exc:
   if exc.__class__.__name__!='AdmissionError':raise
   return {'refused':str(exc)}
 before=derive(I);after=derive(N);assert before==q['before']and after==q['expected'],q['label']
 if 'refused'in after:assert before==after;refuse+=1
 else:
  admit+=1;selection=owner['plan']['semanticClosures']
  for section in ['normalized','evidence']:
   projected=copy.deepcopy(before[section]);projected['closures']={k:objects[k][1]for k in selection};assert projected==after[section]
  if q['label'].endswith('-named-only'):assert before==after
 if before!=after:changed.append(q['label'])
result={'cases':len(cases),'admitted':admit,'refused':refuse,'onlyChangedMaps':'normalized.closures and evidence.closures restricted to Plan semanticClosures','changedCases':changed,'unchangedCases':len(cases)-len(changed),'predecessorSha256':hashlib.sha256(old).hexdigest(),'candidateSha256':hashlib.sha256(new).hexdigest(),'standing':'Proposed reference correction, not selected. Preserves inventory/incoming occurrences; no other reconstruction field differs.'};assert result==json.loads((S/'comparison.json').read_bytes());assert original_owner_count==18;(O/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='changedCases'}))
