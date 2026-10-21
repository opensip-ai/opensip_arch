"""Independent invariants over the staged public companions; no product execution."""
from pathlib import Path
import json,hashlib,importlib.util,copy
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
spec=importlib.util.spec_from_file_location('reference',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
manifest=json.loads((B/'staged-companions.json').read_text());reports=[]
def records(value):
 out=[]
 def scan(x):
  if isinstance(x,dict):
   if {'id','domain','descriptor'}<=x.keys():out.append(x)
   for key,v in x.items():
    if key!='hex':scan(v)
  elif isinstance(x,list):
   for v in x:scan(v)
 scan(value);return out
def blobs(value):
 out=[]
 def scan(x):
  if isinstance(x,dict):
   if {'digest','hex'}<=x.keys():out.append(x)
   if x and all(isinstance(k,str) and len(k)==64 and isinstance(v,str) for k,v in x.items()):
    try:rows=[dict(digest=k,hex=v) for k,v in x.items()];valid=all(hashlib.sha256(bytes.fromhex(r['hex'])).hexdigest()==r['digest'] for r in rows)
    except ValueError:valid=False
    if valid:out.extend(rows)
   for key,v in x.items():
    if key!='hex':scan(v)
  elif isinstance(x,list):
   for v in x:scan(v)
 scan(value);return out
for row in manifest['newFiles']:
 rel=row['path'];old=json.loads((P/row['priorPath']).read_text());new=json.loads((S/rel).read_text());raw=(S/rel).read_bytes();assert len(raw)<=4*1024*1024
 if '/src/' in rel:continue
 name=Path(rel).name
 if name.startswith('replay-fixtures'):mp=B/'replay-identity-map.json'
 elif name.startswith('cycle-'):mp=B/'cycle-identity-map.json'
 elif name.startswith('journal-'):mp=B/'replay-identity-map.json'
 elif name.startswith('native-context'):mp=B/'native-context-candidate/native-context-identity-map.json'
 else:mp=B/'pooled-candidates-r1'/(name.split('-fixtures.')[0]+'-identity-map.json')
 mapping=json.loads(mp.read_text());reverse={v:k for k,v in mapping.items()};assert len(reverse)==len(mapping),'identity mapping collision'
 def inverse(x):
  if isinstance(x,str):return reverse.get(x,x)
  if isinstance(x,list):return [inverse(v) for v in x]
  if isinstance(x,dict):return {reverse.get(k,k):inverse(v) for k,v in x.items()}
  return x
 oldrecords=records(old);newrecords=records(new);assert len(oldrecords)==len(newrecords)
 valid=invalid=0
 for a,b in zip(oldrecords,newrecords):
  assert a['domain']==b['domain'] and b['id']==mapping.get(a['id'],a['id'])
  av=g.hid(a['domain'],a['descriptor'])==a['id'];bv=g.hid(b['domain'],b['descriptor'])==b['id'];assert av==bv,(rel,a['id'],'object fault changed')
  assert g.order_identity(inverse(b['descriptor']))==g.order_identity(a['descriptor']),(rel,a['id'],'descriptor content changed')
  valid+=int(av);invalid+=int(not av)
 oldblobs=blobs(old);newblobs=blobs(new);assert len(oldblobs)==len(newblobs)
 source_changes=opaque=canonical=bad=0
 remaining=list(newblobs)
 for a in oldblobs:
  ar=bytes.fromhex(a['hex']);av=hashlib.sha256(ar).hexdigest()==a['digest'];expected=mapping.get(a['digest'],a['digest'])
  hits=[i for i,b in enumerate(remaining) if b['digest']==expected and (hashlib.sha256(bytes.fromhex(b['hex'])).hexdigest()==b['digest'])==av and (av or b['hex']==a['hex'])]
  assert hits,(rel,a['digest'],'mapped blob occurrence absent')
  b=remaining.pop(hits[0]);br=bytes.fromhex(b['hex'])
  if not av:assert ar==br;bad+=1;continue
  if a['digest'] in g.replacement_blobs:assert br==g.replacement_blobs[a['digest']];source_changes+=1;continue
  try:aj=json.loads(ar)
  except (ValueError,UnicodeError):assert ar==br;opaque+=1;continue
  if g.can(aj)!=ar:assert ar==br;opaque+=1;continue
  bj=json.loads(br);assert g.can(bj)==br;assert g.order_blob(inverse(bj))==g.order_blob(aj),(rel,'canonical blob content changed');canonical+=1
 # Labels, fixed verdict/result/cause classes and population are never inferred from runtime output.
 def outcomes(x):
  out=[]
  def scan(v):
   if isinstance(v,dict):
    for k,w in v.items():
     if k in ('label','result','verdict','expectedVerdict') and isinstance(w,(str,bool,int)):out.append((k,w))
     scan(w)
   elif isinstance(v,list):
    for w in v:scan(w)
  scan(x);return out
 expected_outcomes=copy.deepcopy(old);adapted=False
 if name.startswith('full-walk') and 'explicitCurrentRefusalAdaptations' in manifest:
  changes=manifest['explicitCurrentRefusalAdaptations'];assert len(changes)==2
  for entry in changes:
   label=entry['label'];assert old['cases'][label]['expected']['result']=='unavailable' and entry['newExpected']['result']=='invalid'
   assert new['cases'][label]['expected']==entry['newExpected'];expected_outcomes['cases'][label]['expected']=entry['newExpected']
  adapted=True
 if name.startswith('full-walk') and 'explicitSingleFaultRetentions' in manifest:
  entries=manifest['explicitSingleFaultRetentions'];assert len(entries)==14;by_label={}
  for e in entries:by_label.setdefault(e['label'],[]).append(e)
  assert len(by_label)==12
  for label,c in old['cases'].items():
   extra=[e['addedExistingPoolKey'] for e in by_label.get(label,[])]
   assert new['cases'][label]['request']['objects']==c['request']['objects']+extra
   if label in by_label:
    for entry in by_label[label]:
     assert '-and-' not in label and 'missing' not in label and new['cases'][label]['expected']==entry['expectedUnchanged']
     added=new['objectPool'][entry['addedExistingPoolKey']];assert added['id']==entry['addedValidIdentity'] and g.hid('fact',added['descriptor'])==added['id']
 if name.startswith('full-walk') and 'explicitSingleFaultRetention' in manifest:
  entry=manifest['explicitSingleFaultRetention'];label=entry['label']
  for case,c in old['cases'].items():
   expected=c['request']['objects']+([entry['addedExistingPoolKey']] if case==label else [])
   assert new['cases'][case]['request']['objects']==expected
  assert new['cases'][label]['expected']==entry['oldAndNewExpected']
  added=new['objectPool'][entry['addedExistingPoolKey']];assert added['id']==entry['addedValidIdentity'] and g.hid('fact',added['descriptor'])==added['id']
 if name.startswith('full-walk') and 'explicitCoupledNegativePrecedenceAdaptation' in manifest:
  declaration=manifest['explicitCoupledNegativePrecedenceAdaptation'];label=declaration['label']
  assert old['cases'][label]['expected']==declaration['oldExpected']
  assert new['cases'][label]['expected']==declaration['newExpected']
  assert declaration['oldExpected']['result']=='invalid' and declaration['newExpected']['result']=='unavailable'
  assert new['cases']['semantic-fact-foreign-snapshotId']['expected']==old['cases']['semantic-fact-foreign-snapshotId']['expected']
  expected_outcomes['cases'][label]['expected']=new['cases'][label]['expected'];adapted=True
  adaptations=json.loads((B/'ordering-and-refusal-adaptations.json').read_text())[-1]
  selections=adaptations['existingBaseFactsRetainedForSingleSemanticFaultControls'];assert len(selections)==8
  for entry in selections:
   case=entry['case'];prior=old['cases'][case]['request']['objects'];now=new['cases'][case]['request']['objects'];assert now==prior+[entry['addedExistingPoolKey']]
   added=new['objectPool'][entry['addedExistingPoolKey']];assert added['id']==entry['addedValidIdentity'] and g.hid('fact',added['descriptor'])==added['id']
 assert outcomes(expected_outcomes)==outcomes(new),(rel,'undeclared label/verdict population changed')
 assert (P/row['priorPath']).read_bytes()==(W/row['priorPath']).read_bytes()
 reports.append(dict(path=rel,objectOccurrences=len(oldrecords),validObjects=valid,deliberateInvalidObjects=invalid,blobOccurrences=len(oldblobs),sourceDocumentReplacements=source_changes,canonicalBlobsComparedByInverseRecipe=canonical,opaqueBytesExact=opaque,deliberateInvalidBlobs=bad,labelsVerdictsPopulationEqual=not adapted,explicitCurrentRefusalPrecedenceChanges=(2 if manifest.get('explicitCurrentRefusalAdaptations') and adapted else int(adapted)),allOtherLabelsVerdictsEqual=True,noSuccessfulAdmissionAdded=True,inverseGraphContentEqual=True,originalsUnchanged=True))
report=dict(standing='INDEPENDENT STAGED SYNTHETIC CORRESPONDENCE INVARIANTS; NOT RUNTIME ACCEPTANCE',fixtures=len(reports),reports=reports,sourceGuardUnchanged=True,testsPassed=False,unitAccepted=False,productQualification=False)
(B/'correspondence-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(fixtures=len(reports),valid=True,objectOccurrences=sum(r['objectOccurrences'] for r in reports),blobOccurrences=sum(r['blobOccurrences'] for r in reports)),indent=2))
