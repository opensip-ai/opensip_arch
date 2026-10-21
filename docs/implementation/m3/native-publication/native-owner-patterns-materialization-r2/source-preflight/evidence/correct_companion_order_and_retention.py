from pathlib import Path
import os,json,hashlib,copy,shutil,importlib.util
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip'
spec=importlib.util.spec_from_file_location('reference',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=B/'focused-attempt1';assert not E.exists();E.mkdir()
changes=[]
def save(rel,value):
 original=(S/rel).read_bytes();assert (W/rel).read_bytes()==original
 dst=E/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(original)
 raw=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()+b'\n';assert len(raw)<=4*1024*1024
 (S/rel).write_bytes(raw);(W/rel).write_bytes(raw)
# These two fields have deliberately different laws: the normalized execution
# deficiencies are E.cset; admission deficiencies retain coverage traversal
# encounter order, where returned partitions are ordered by their new digest.
def normalize_expected(value,path=()):
 if isinstance(value,list):return [normalize_expected(v,path+(str(i),)) for i,v in enumerate(value)]
 if not isinstance(value,dict):return value
 value={k:normalize_expected(v,path+(k,)) for k,v in value.items()}
 if 'coverageRecords' in value:
  rows=value['coverageRecords']
  if rows and all(isinstance(r,dict) and 'coverageId' in r for r in rows):value['coverageRecords']=sorted(rows,key=lambda r:r['coverageId'])
 if 'sources' in value:
  rows=value['sources']
  if rows and all(isinstance(r,dict) and 'coverageId' in r for r in rows):value['sources']=sorted(rows,key=lambda r:r['coverageId'])
 if 'inputRefs' in value:value['inputRefs']=sorted(value['inputRefs'],key=g.can)
 if 'executionDeficiencies' in value:value['executionDeficiencies']=sorted(value['executionDeficiencies'],key=g.can)
 if 'requiredCellDeficiencies' in value:
  rows=value['requiredCellDeficiencies'];groups={}
  for i,r in enumerate(rows):
   refs=r.get('inputRefs',[])
   if r.get('cause')=='native-work-incomplete' and len(refs)==1 and refs[0].get('domain')=='coverage':
    key=g.can({k:v for k,v in r.items() if k!='inputRefs'});groups.setdefault(key,[]).append(i)
  for indices in groups.values():
   ordered=sorted((rows[i] for i in indices),key=lambda r:r['inputRefs'][0]['digest'])
   for i,r in zip(indices,ordered):rows[i]=r
 return value
for name in ['execution-input','reconstruction']:
 rel='crates/host/tests/fixtures/'+name+'-fixtures.native-owner-r1.json';value=json.loads((S/rel).read_text());before=copy.deepcopy(value)
 if 'expectedPool' in value:
  for key,x in value['expectedPool'].items():value['expectedPool'][key]=normalize_expected(x)
 if 'cases' in value:
  cases=value['cases'].values() if isinstance(value['cases'],dict) else value['cases']
  for case in cases:
   if isinstance(case.get('expected'),dict):case['expected']=normalize_expected(case['expected'])
 assert value!=before,name;save(rel,value);changes.append(dict(path=rel,change='Published canonical normalized execution-deficiency set and digest-ordered coverage encounter carriers; all members and verdicts retained',authority=['execution_inputs.rs returned_partitions/check_accounts/uniq encounter sequence','execution_inputs_model.v1.py returned coverage/uniq','evaluator_input_model.v3.py executionDeficiencies=E.cset(execution)']))
rel='crates/host/tests/fixtures/full-walk-fixtures.native-owner-r1.json';value=json.loads((S/rel).read_text());old=json.loads((P/'crates/host/tests/fixtures/full-walk-fixtures.current.json').read_text());pool={r['id']:(k,r) for k,r in value['objectPool'].items()};added=[]
for label,case in value['cases'].items():
 if not label.startswith('semantic-fact-') or case['expected']['result']!='invalid':continue
 selected={value['objectPool'][k]['id'] for k in case['request']['objects']};missing=set();witnesses=[]
 def scan(x,path=()):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ('matchingFactIds','uncertainFactIds') and isinstance(v,list):
     for identity in v:
      if identity in pool and identity not in selected:missing.add(identity);witnesses.append(dict(field='/'.join(path+(k,)),identity=identity))
    scan(v,path+(k,))
  elif isinstance(x,list):
   for i,v in enumerate(x):scan(v,path+(str(i),))
 for key in case['request']['blobs']:
  try:scan(json.loads(bytes.fromhex(value['blobPool'][key]['hex'])),(key,))
  except (ValueError,UnicodeError):pass
 for identity in sorted(missing):
  key,row=pool[identity];assert row['domain']=='fact' and g.hid('fact',row['descriptor'])==identity
  assert key not in case['request']['objects'];case['request']['objects'].append(key)
  added.append(dict(case=label,addedExistingPoolKey=key,addedValidIdentity=identity,referencedByExistingObservation=witnesses,originalMutantStillSelected=True,reason='Preserve the intended semantic fact refusal while closing incidental observation references after current digest ordering changes. No object/blob is invented or replaced.'))
assert len(added)==8
label='semantic-fact-foreign-and-missing-child';single=value['cases']['semantic-fact-foreign-snapshotId'];coupled=value['cases'][label]
assert coupled['expected']==old['cases'][label]['expected'] and coupled['expected']['result']=='invalid'
assert coupled['request']['objects']==single['request']['objects']
removed=[k for k in single['request']['blobs'] if k not in coupled['request']['blobs']];assert len(removed)==1
digest=value['blobPool'][removed[0]]['digest'];assert any(value['objectPool'][r['addedExistingPoolKey']]['descriptor']['payloadDigest']==digest for r in added if r['case']==label)
assert digest not in [value['blobPool'][k]['digest'] for k in coupled['request']['blobs']]
coupled['expected']=dict(result='unavailable',cause='EVIDENCE_UNAVAILABLE:'+digest,missingBlobDigest=digest)
assert single['expected']['result']=='invalid' and single['expected']['cause']=='REFERENCE_SOURCE_JOIN'
save(rel,value)
changes.append(dict(path=rel,existingBaseFactsRetainedForSingleSemanticFaultControls=added,explicitCoupledCaseAdaptation=dict(label=label,oldExpected=old['cases'][label]['expected'],newExpected=coupled['expected'],intendedMissingChildPreserved=removed[0],noSuccessfulAdmission=True,independentForeignSnapshotRefusalStillRequired=True,authority='Published H canonical typed-reference traversal; observations retain matchingFactIds and payload byte dependencies. Under current hash order the observed base fact is reached before the foreign fact; the same deliberately absent payload is required.')))
# Strengthen the coupled control: a generic unavailable refusal is insufficient.
p=W/'crates/host/src/native_owner_tests.rs';text=p.read_text();needle='''                if let Some(cause) = expected.get("cause") {
                    let cause = string(cause);
                    if [
                        "REFERENCE_SOURCE_JOIN",'''
assert text.count(needle)==1
replacement='''                if let Some(digest) = expected.get("missingBlobDigest") {
                    let digest = bytes(string(digest));
                    assert_eq!(digest.len(), 32);
                    assert!(detail.contains(&format!("MissingBlob({digest:?})")), "{name}: {detail}");
                }
'''+needle
before=text;text=text.replace(needle,replacement);(E/'native_owner_tests.rs').write_text(before);p.write_text(text)
manifest=json.loads((B/'staged-companions.json').read_text())
for row in manifest['newFiles']:
 raw=(S/row['path']).read_bytes();row['candidate']=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
manifest['expectedVerdictsNotRewritten']=False;manifest['explicitCoupledNegativePrecedenceAdaptation']=changes[-1]['explicitCoupledCaseAdaptation'];manifest['allOtherVerdictsPreserved']=True
(B/'staged-companions.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'ordering-and-refusal-adaptations.json').write_text(json.dumps(changes,indent=2)+'\n');print(json.dumps(dict(expectedOrderingFixtures=2,existingBaseFactSelectionsAdded=8,coupledCase=label,missingBlobDigest=digest,allOriginalFilesUnchanged=True),indent=2))
