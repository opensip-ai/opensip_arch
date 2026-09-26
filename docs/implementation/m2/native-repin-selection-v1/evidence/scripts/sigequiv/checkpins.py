import json,hashlib,os,sys
R='/Users/sb/code/opensip-ai/opensip/tools/contracts/'
items=[]
d=json.load(open(R+'native-python-profile.json'))
items+=[(x['path'],x['sha256']) for x in d['nativeLibraries']]+[(d['executable']['path'],d['executable']['sha256'])]+[(x['path'],x['sha256']) for x in d['files']]
p=json.load(open(R+'python-profile.json')); items+=[(x['path'],x['sha256']) for x in p['files']]
b=json.load(open(R+'build-receipt.json')); items+=[(v['path'],v['sha256']) for v in b['tools'].values()]
seen=set(); ok=bad=miss=0
for path,h in items:
    if path in seen: continue
    seen.add(path)
    if not os.path.exists(path): miss+=1; continue
    got=hashlib.sha256(open(path,'rb').read()).hexdigest()
    if got==h: ok+=1
    else: bad+=1; print('MISMATCH',path)
print(f'ok={ok} mismatch={bad} missing={miss}')
