import json,hashlib,os,collections
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
TREE=S+'/src25'
changed=['docs/coop/design-corrections/foundation/enumeration_model.v1.py',
         'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
         'docs/coop/design-corrections/native/native_evidence_model.v2.py']
delta=[]
for f in ['source-pins.v1.json','evaluator3-source-pins.v1.json']:
    pp=TREE+'/docs/coop/design-corrections/foundation/'+f
    raw=open(pp,'rb').read()
    pinbefore=hashlib.sha256(raw).hexdigest()
    d=json.loads(raw,object_pairs_hook=collections.OrderedDict)
    n=0
    for row in d['files']:
        if row['path'] in changed:
            old=row['sha256']
            new=hashlib.sha256(open(os.path.join(TREE,row['path']),'rb').read()).hexdigest()
            if old!=new:
                row['sha256']=new; n+=1
                delta.append({'pinFile':f,'path':row['path'],'beforeSha256':old,'afterSha256':new})
    out=json.dumps(d,indent=1)+chr(10)
    open(pp,'w',encoding='utf-8').write(out)
    print(f,'rows rebound',n,'| pin before',pinbefore,'| pin after',hashlib.sha256(out.encode()).hexdigest())
json.dump({'standing':'Scratch-only source-pin rebinding for the authored correction; frozen candidate25 pins are unchanged.','rebindings':delta},open(S+'/output/evidence/source-pin-rebinding.json','w'),indent=1)
print('delta rows:',len(delta))
