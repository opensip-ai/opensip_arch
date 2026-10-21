from pathlib import Path
import os,json,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
rel='crates/host/tests/fixtures/full-walk-fixtures.native-owner-r1.json';value=json.loads((S/rel).read_text());old=json.loads((B/'focused-attempt1'/rel).read_text());assert (S/rel).read_bytes()==(W/rel).read_bytes();E=B/'single-semantic-retention-attempt4';E.mkdir();shutil.copyfile(S/rel,E/'full-walk-fixtures.native-owner-r1.json');shutil.copyfile(B/'staged-companions.json',E/'staged-companions.json')
pool={r['id']:(k,r) for k,r in value['objectPool'].items()};adaptations=[]
for label,case in value['cases'].items():
 if not label.startswith('semantic-') or '-and-' in label or 'missing' in label or case['expected']['result']!='invalid':continue
 # Derive the required retained facts from the existing observation payloads,
 # not from a test verdict. Every added record must already exist in the pool.
 originally={value['objectPool'][k]['id'] for k in old['cases'][label]['request']['objects']};missing=set();witnesses=[]
 def scan(x,path=()):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ('matchingFactIds','uncertainFactIds') and isinstance(v,list):
     for identity in v:
      if identity in pool and identity not in originally:missing.add(identity);witnesses.append(dict(field='/'.join(path+(k,)),identity=identity))
    scan(v,path+(k,))
  elif isinstance(x,list):
   for i,v in enumerate(x):scan(v,path+(str(i),))
 for key in case['request']['blobs']:
  try:scan(json.loads(bytes.fromhex(value['blobPool'][key]['hex'])),(key,))
  except (ValueError,UnicodeError):pass
 for identity in sorted(missing):
  key,row=pool[identity];assert row['domain']=='fact'
  if key not in case['request']['objects']:case['request']['objects'].append(key)
  adaptations.append(dict(label=label,addedExistingPoolKey=key,addedValidIdentity=identity,referencedByExistingObservation=witnesses,originalMutantStillSelected=True,expectedUnchanged=case['expected']))
assert len(adaptations)==14 and len({a['label'] for a in adaptations})==12
labels={r['label'] for r in adaptations}
for label,case in value['cases'].items():
 assert case['expected']==old['cases'][label]['expected']
 if label not in labels:assert case['request']==old['cases'][label]['request']
raw=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()+b'\n';(S/rel).write_bytes(raw);(W/rel).write_bytes(raw)
manifest=json.loads((B/'staged-companions.json').read_text());manifest.pop('explicitSingleFaultRetention',None);manifest['explicitSingleFaultRetentions']=adaptations;manifest['expectedVerdictsNotRewritten']=True
for row in manifest['newFiles']:
 if row['path']==rel:row['candidate']=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(B/'staged-companions.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'final-retention-scope.json').write_text(json.dumps(dict(standing='FRESH SYNTHETIC SINGLE-FACT FAULT ISOLATION; NO VERDICT OR COUPLED-CASE CHANGES',retentions=adaptations,allOtherCaseRequestsUnchanged=True,allExpectedValuesUnchanged=True,independentlyDerivedFromExistingObservationFactReferences=True,allAddedRowsAlreadyInPool=True,earlierCoupledExpectedChangeRejectedAndPreserved=True,allOriginalFixturesPreserved=True),indent=2)+'\n');print(json.dumps(dict(singleSemanticCasesClosed=len({a['label'] for a in adaptations}),existingFactSelectionsAdded=len(adaptations),allExpectedValuesPreserved=True,allCoupledCasesUnchanged=True),indent=2))
