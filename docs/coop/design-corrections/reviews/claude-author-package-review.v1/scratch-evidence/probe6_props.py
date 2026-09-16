
import importlib.util,json,base64,hashlib
from pathlib import Path
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
F=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/foundation')
s=importlib.util.spec_from_file_location('mi',F/'identity-model.v3.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def read(sub,name):
    d=json.loads((PKG/sub/(name+'.store.json')).read_text())
    claim=next(x for x in json.loads((PKG/sub/'claims.json').read_text()) if x['name']==name)
    o=d['objectTable'];b={k:base64.b64decode(v) for k,v in d['blobs'].items()}
    run=o[claim['runId']];e=o[run['evidenceId']];proof=o[e['proofBundleId']]
    facts=[o[f] for v in e['viewIds'] for f in o[v]['facts']]
    covers=[json.loads(b[o[c]['payloadDigest']]) for c in e['coverageIds']]
    return d,o,b,run,e,proof,facts,covers
rust={};uni_payloads={}
for label,sub,name in [('lib','normalized-examples6','rust'),('bin','rust-selection-examples1','rust-bin'),('lib-only','rust-selection-examples1','rust-lib-only')]:
    d,o,b,run,e,proof,facts,covers=read(sub,name)
    clones=[f for f in facts if f['relation']=='clones'];assert len(clones)==1;f=clones[0]
    payload=json.loads(b[f['payloadDigest']]);bodyid=payload['bodyIdentity']
    frame=M.parse_body_frame(b[bodyid.split(':')[1]]);assert len(frame[4])==32
    domains=next(k for k,v in M.DIGESTS['domainSets'].items() if 'native.semantic-universe.rust.v2' in v)
    _,u,_=M.parse_h_frame(b[f['sourceUniverse']],domains)
    uni_payloads[label]=u
    assert u['edition']['alpha']==2018 and u['edition']['hashy']==2021 and len(u['edition'])==10
    snapshot=o[run['snapshotId']];assert any(x['path']=='crates/foo#bar/Cargo.toml' for x in snapshot['sourceInventory'])
    rust[label]={'runId':M.identifier('run',run),'universe':f['sourceUniverse'],'bodyIdentity':bodyid,
      'sourceDigest':f['anchors'][0]['blobDigest'],'sourcePath':f['anchors'][0]['path'],
      'boundedVersionHex':frame[4].hex(),'bodyPayloadSha256':hashlib.sha256(frame[5]).hexdigest(),'editionMap':u['edition']}
print('assert same sourceDigest:',rust['lib']['sourceDigest']==rust['bin']['sourceDigest']==rust['lib-only']['sourceDigest'])
print('assert same bodyPayloadSha256:',rust['lib']['bodyPayloadSha256']==rust['bin']['bodyPayloadSha256']==rust['lib-only']['bodyPayloadSha256'])
print('assert lib!=bin bodyIdentity:',rust['lib']['bodyIdentity']!=rust['bin']['bodyIdentity'],'version:',rust['lib']['boundedVersionHex']!=rust['bin']['boundedVersionHex'])
print('assert lib!=lib-only universe:',rust['lib']['universe']!=rust['lib-only']['universe'],'bodyIdentity equal:',rust['lib']['bodyIdentity']==rust['lib-only']['bodyIdentity'])
print()
print('=== universe payload differences ===')
keys=sorted(set(k for u in uni_payloads.values() for k in u))
for k in keys:
    vals={lab:json.dumps(u.get(k),sort_keys=True) for lab,u in uni_payloads.items()}
    if len(set(vals.values()))>1:
        print(' FIELD DIFFERS:',k)
        for lab in ['lib','bin','lib-only']: print('   ',lab,'=',vals[lab][:300])
    else:
        print(' same:',k,'=',vals['lib'][:110])
print()
print('=== compare to packaged author-properties.json ===')
pub=json.loads((PKG/'author-properties.json').read_text())
same=json.dumps(pub['rustComparisons'],sort_keys=True)==json.dumps(rust,sort_keys=True)
print('rustComparisons reproduce exactly:',same)
if not same:
    for lab in rust:
        for k in rust[lab]:
            if pub['rustComparisons'][lab][k]!=rust[lab][k]: print('  DIFF',lab,k)
_,o,b,run,e,proof,facts,covers=read('normalized-examples6','rust-partial')
unknown=[p for p in covers if p['entry']['relation']=='clones']
print('partial: verdict',proof['verdict'],'cloneFacts',sum(1 for f in facts if f['relation']=='clones'),'unknownCov',len(unknown))
print('partialRust reproduces:',json.dumps(pub['partialRust']['coveragePayloads'],sort_keys=True)==json.dumps(unknown,sort_keys=True))
