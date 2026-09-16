"""Bounded source/ref closure probe, not a selected product generator."""
from pathlib import Path
import copy, hashlib, json
ARCH=Path("/Users/sb/code/opensip-ai/opensip_arch")
HERE=Path(__file__).resolve().parent

def digest(raw): return hashlib.sha256(raw).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d: raise ValueError("duplicate key")
  d[k]=v
 return d

def load(raw): return json.loads(raw,object_pairs_hook=pairs)
paths=load((HERE/"schema-paths.json").read_bytes())
base=load((ARCH/"docs/coop/design-corrections/reviews/candidate-subject.v45.json").read_bytes())
app=load((ARCH/"docs/coop/design-corrections/reviews/application-subject.v46.json").read_bytes())
# Whole manifest pins are checked explicitly, not inferred from filenames.
assert digest((ARCH/"docs/coop/design-corrections/reviews/candidate-subject.v45.json").read_bytes())=="8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155"
assert digest((ARCH/"docs/coop/design-corrections/reviews/application-subject.v46.json").read_bytes())=="dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7"
effective={r["path"]:r for r in base["files"]}
effective.update({r["path"]:r for r in app["files"]})
schemas={};rows=[]
for path in paths:
 raw=(ARCH/path).read_bytes();assert digest(raw)==effective[path]["sha256"] and len(raw)==effective[path]["bytes"]
 d=load(raw);sid=d["$id"];assert isinstance(sid,str) and sid and sid not in schemas
 schemas[sid]=d;rows.append({"path":path,"sha256":digest(raw),"bytes":len(raw),"schemaId":sid})

def resolve(ref,current):
 if ref.startswith("#"): sid,fragment=current,ref[1:]
 else:
  sid,_,fragment=ref.partition("#")
  if sid not in schemas: raise ValueError("unregistered schema ID: "+sid)
 if fragment and not fragment.startswith("/"):raise ValueError("unregistered anchor")
 value=schemas[sid]
 for part in fragment.split("/")[1:]:value=value[part.replace("~1","/").replace("~0","~")]
 if not isinstance(value,(dict,bool)):raise ValueError("ref does not select a schema")
 return sid+"#"+fragment,value,sid

def refs(value,current):
 if isinstance(value,dict):
  if "$ref" in value:yield resolve(value["$ref"],current)
  for child in value.values():yield from refs(child,current)
 elif isinstance(value,list):
  for child in value:yield from refs(child,current)
allrefs={};failures=[]
for sid,value in schemas.items():
 try:
  for ref,target,owner in refs(value,sid):allrefs[ref]=(target,owner)
 except (KeyError,ValueError,TypeError) as error:
  failures.append({"schemaId":sid,"error":str(error)})
if failures:
 (HERE/"source-closure-results.json").write_text(json.dumps({"standing":"REFUSED: every-ID membership passes, but full-document pointer resolution fails; no complete closure or generation accepted","sources":rows,"failures":failures},indent=2)+"\n")
 raise SystemExit(json.dumps(failures))
negatives=[]
for ref in ["urn:opensip:unregistered:1","https://example.invalid/schema","file:///tmp/schema.json","../schema.json"]:
 try:resolve(ref,next(iter(schemas)))
 except ValueError:negatives.append(ref)
 else:raise AssertionError("unregistered lookup accepted")
# Typify's documented API takes a single RootSchema. This trial flattens every
# actually referenced schema into one definition keyed by sorted absolute ref.
# Targets/constraints stay structurally intact except ID/ref relocation. This
# adapter has not been reviewed or accepted as a product recipe.
for sid,value in schemas.items():allrefs[sid+"#"]=(value,sid)
names={ref:"T"+str(i).zfill(5) for i,ref in enumerate(sorted(allrefs))}
def rewrite(value,current):
 if isinstance(value,list):return [rewrite(v,current) for v in value]
 if not isinstance(value,dict):return value
 result={k:rewrite(v,current) for k,v in value.items() if k not in ("$id","$schema")}
 if "$ref" in value:result["$ref"]="#/definitions/"+names[resolve(value["$ref"],current)[0]]
 return result
bundle={"$schema":"http://json-schema.org/draft-07/schema#","definitions":{names[ref]:rewrite(target,owner) for ref,(target,owner) in sorted(allrefs.items())}}
# The tool's RootSchema is draft07-shaped. Do not claim dialect conversion or
# preserved unsupported keywords; the probe measures whether it refuses them.
(HERE/"inputs/flattened-trial.json").write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+"\n")
(HERE/"source-closure-results.json").write_text(json.dumps({"standing":"Reference closure passed; flattening adapter/dialect handling unaccepted","sources":rows,"uniqueTargets":len(allrefs),"negativeRefusals":negatives,"generatedBundleSha256":digest((HERE/"inputs/flattened-trial.json").read_bytes())},indent=2)+"\n")
print(json.dumps({"sources":len(rows),"uniqueTargets":len(allrefs),"negativeRefusals":len(negatives)}))
