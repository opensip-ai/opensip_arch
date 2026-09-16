import os,shutil,json,hashlib,collections
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
BASE=S+'/baseline25'; NC=S+'/nullchange25'
if os.path.isdir(NC): shutil.rmtree(NC)
shutil.copytree(BASE,NC)
SCHEMA_REL='docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
FIXTURE_REL='docs/coop/design-corrections/native/native-cases.v2.json'
def sha(fp): return hashlib.sha256(open(fp,'rb').read()).hexdigest()
old=sha(os.path.join(BASE,SCHEMA_REL))
d=json.loads(open(os.path.join(BASE,SCHEMA_REL),'rb').read(),object_pairs_hook=collections.OrderedDict)
d['$comment']='null-change control: semantically inert edit used to separate cause from correction'
open(os.path.join(NC,SCHEMA_REL),'w',encoding='utf-8').write(json.dumps(d,indent=1)+chr(10))
new=sha(os.path.join(NC,SCHEMA_REL))
print('schema old',old);print('schema new',new)
raw=open(os.path.join(BASE,FIXTURE_REL),encoding='utf-8').read()
open(os.path.join(NC,FIXTURE_REL),'w',encoding='utf-8').write(raw.replace(old,new))
changed=[SCHEMA_REL,FIXTURE_REL]
oldsha={r:sha(os.path.join(BASE,r)) for r in changed}
newsha={r:sha(os.path.join(NC,r)) for r in changed}
pinfiles=['docs/coop/design-corrections/foundation/source-pins.v1.json',
          'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
          'docs/coop/design-corrections/native/source-pins.v2.json',
          'docs/coop/design-corrections/security/source-pins.v1.json',
          'docs/coop/design-corrections/workflows/source-pins.v1.json']
for pf in pinfiles:
    dd=json.loads(open(os.path.join(BASE,pf),'rb').read(),object_pairs_hook=collections.OrderedDict)
    key='pins' if 'pins' in dd else 'files'
    for row in dd.get(key,[]):
        rel=row.get('path')
        if rel in oldsha and row.get('sha256')==oldsha[rel]: row['sha256']=newsha[rel]
    open(os.path.join(NC,pf),'w',encoding='utf-8').write(json.dumps(dd,indent=1)+chr(10))
EV3='docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json'
dd=json.loads(open(os.path.join(NC,EV3),'rb').read(),object_pairs_hook=collections.OrderedDict)
key='pins' if 'pins' in dd else 'files'
for row in dd.get(key,[]):
    rel=row.get('path')
    if rel in pinfiles and rel!=EV3: row['sha256']=sha(os.path.join(NC,rel))
open(os.path.join(NC,EV3),'w',encoding='utf-8').write(json.dumps(dd,indent=1)+chr(10))
print('null-change control tree built')
