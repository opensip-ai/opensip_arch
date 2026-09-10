"""Measured properties of exact author exports; no fixture metadata assertions."""
from pathlib import Path
import importlib.util,json,base64,hashlib
ROOT=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('author_identity',ROOT.parent/'candidate-subject.v25/docs/coop/design-corrections/foundation/identity-model.v3.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def read(sub,name):
 d=json.loads((ROOT/sub/(name+'.store.json')).read_text());claim=next(x for x in json.loads((ROOT/sub/'claims.json').read_text()) if x['name']==name);o=d['objectTable'];b={k:base64.b64decode(v) for k,v in d['blobs'].items()};run=o[claim['runId']];e=o[run['evidenceId']];proof=o[e['proofBundleId']];facts=[o[f] for v in e['viewIds'] for f in o[v]['facts']];covers=[json.loads(b[o[c]['payloadDigest']]) for c in e['coverageIds']];return d,o,b,run,e,proof,facts,covers
rust={}
for label,sub,name in [('lib','normalized-examples6','rust'),('bin','rust-selection-examples1','rust-bin'),('lib-only','rust-selection-examples1','rust-lib-only')]:
 d,o,b,run,e,proof,facts,covers=read(sub,name)
 clones=[f for f in facts if f['relation']=='clones'];assert len(clones)==1;f=clones[0];payload=json.loads(b[f['payloadDigest']]);bodyid=payload['bodyIdentity'];frame=M.parse_body_frame(b[bodyid.split(':')[1]]);assert len(frame[4])==32
 domains=next(k for k,v in M.DIGESTS['domainSets'].items() if 'native.semantic-universe.rust.v2' in v)
 _,u,_=M.parse_h_frame(b[f['sourceUniverse']],domains)
 assert u['edition']['alpha']==2018 and u['edition']['hashy']==2021 and len(u['edition'])==10
 snapshot=o[run['snapshotId']];assert any(x['path']=='crates/foo#bar/Cargo.toml' for x in snapshot['sourceInventory'])
 rust[label]={'runId':M.identifier('run',run),'universe':f['sourceUniverse'],'bodyIdentity':bodyid,'sourceDigest':f['anchors'][0]['blobDigest'],'sourcePath':f['anchors'][0]['path'],'boundedVersionHex':frame[4].hex(),'bodyPayloadSha256':hashlib.sha256(frame[5]).hexdigest(),'editionMap':u['edition']}
assert rust['lib']['sourceDigest']==rust['bin']['sourceDigest']==rust['lib-only']['sourceDigest']
assert rust['lib']['bodyPayloadSha256']==rust['bin']['bodyPayloadSha256']==rust['lib-only']['bodyPayloadSha256']
assert rust['lib']['bodyIdentity']!=rust['bin']['bodyIdentity'] and rust['lib']['boundedVersionHex']!=rust['bin']['boundedVersionHex']
assert rust['lib']['universe']!=rust['lib-only']['universe'] and rust['lib']['bodyIdentity']==rust['lib-only']['bodyIdentity']
_,o,b,run,e,proof,facts,covers=read('normalized-examples6','rust-partial')
assert proof['verdict']=='indeterminate' and not any(f['relation']=='clones' for f in facts)
unknown=[p for p in covers if p['entry']['relation']=='clones'];assert unknown and all(p['entry']['coverage']=='unknown' and p['entry']['nativeCause']=='body-language-owner-unenumerated' and p['entry']['deficiency']=='input-closure-incomplete' for p in unknown)
report={'standing':'Author synthetic reference measurements. All selected Runs separately pass frozen full replay. No compiler extraction qualification or blind acceptance.','passed':True,'rustComparisons':rust,'partialRust':{'runId':M.identifier('run',run),'verdict':proof['verdict'],'selectedCloneFacts':0,'coveragePayloads':unknown},'checks':['mixed 2018/2021 ten-entry edition map','literal # marker path retained','same physical body under different selected target editions changes body identity/version component','selection change preserving effective edition changes universe but preserves body identity','version component is exactly 32 bytes','partial ownership has no clone fact, unknown coverage, input-closure-incomplete/body-language-owner-unenumerated, and indeterminate verdict']}
(ROOT/'author-properties.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'checks':report['checks']},indent=2))
