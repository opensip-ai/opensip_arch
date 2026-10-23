from pathlib import Path
import json,hashlib,subprocess,re,datetime
ROOT=Path(__file__).parent;STAGE=ROOT/'architecture';A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=Path('/Users/sb/code/opensip-ai/opensip');REL=Path('docs/implementation/m3/status/2026-10-22-r124');B=STAGE/REL
load=lambda n:json.loads((B/n).read_text())
h=lambda b:hashlib.sha256(b).hexdigest()
ledger=load('accepted-work.json');baseline=json.loads((A/'docs/implementation/m3/status/2026-10-22-r123/accepted-work.json').read_text())
assert len(ledger['records'])==405 and ledger['records'][:404]==baseline['records']
assert ledger['records'][-1]['id']=='E405'
pins={};commits=[];historical_product_pins=[]
def walk(v,where=''):
 if isinstance(v,dict):
  if {'path','bytes','sha256'}<=set(v) and isinstance(v['path'],str):
   if (where.startswith('accepted-work.json/records/') or where.startswith('bindings-since-plan-cutoff.json/')) and not v['path'].startswith('docs/'):
    historical_product_pins.append({'path':v['path'],'where':where,'sha256':v['sha256']})
   else:pins[(v['path'],v['bytes'],v['sha256'])]=where
  for k,x in v.items():
   low=k.lower()
   if (low.endswith('architecturecommit') or low in ('architecturecommit','initialpublicationcommit')) and isinstance(x,str):commits.append(('architecture',x))
   if low in ('productcommit','productlockcommit','productcodecommit') and isinstance(x,str):commits.append(('product',x))
   if low=='commit' and '/productCommitReferences/' in where and isinstance(x,str):commits.append(('product',x))
   if low=='productcommitreferences' and isinstance(x,list):
    for s in x:
     if isinstance(s,str):commits.append(('product',s))
   walk(x,where+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,where+'/'+str(i))
for n in ['accepted-work.json','bindings-since-plan-cutoff.json','current-public-bindings.json','source.json','decisions.json']:walk(load(n),n)
matched=[];bad=[]
for (path,size,sha),where in pins.items():
 rel=Path(path)
 if rel.is_absolute():raise AssertionError('absolute pin requires explicit custody mapping: '+path)
 candidates=[STAGE/rel,A/rel,P/rel]
 found=None
 for q in candidates:
  q=q.resolve()
  if not any(q.is_relative_to(root.resolve()) for root in [STAGE,A,P]):continue
  if q.is_file() and not q.is_symlink():
   raw=q.read_bytes()
   if len(raw)==size and h(raw)==sha:found=q;break
 if found is None and where=='source.json/historicalAuthorityRepins/0/previous':
  raw=subprocess.check_output(['git','show','b92622d0b^:'+path],cwd=A)
  assert len(raw)==size and h(raw)==sha
  found=ROOT/'historical-authority/PROPOSAL-pre-ci-a3.md';found.parent.mkdir(exist_ok=True);found.write_bytes(raw)
  (found.parent/'evidence.json').write_text(json.dumps({'repository':'architecture','commit':subprocess.check_output(['git','rev-parse','b92622d0b^'],cwd=A).decode().strip(),'originalPath':path,'bytes':size,'sha256':sha,'scope':'historical authority, not current live path'},indent=2)+'\n')
 if found is None:bad.append({'path':path,'where':where,'sha':sha})
 else:matched.append({'path':path,'bytes':size,'sha256':sha,'resolved':str(found)})
if bad:raise AssertionError(json.dumps(bad[:8]))
ancestors={label:set(subprocess.check_output(['git','rev-list','HEAD'],cwd=repo).decode().splitlines()) for label,repo in [('architecture',A),('product',P)]}
commit_checked=[]
for label,ref in sorted(set(commits)):
 if not re.fullmatch('[0-9a-f]{7,40}',ref):raise AssertionError('unexpected commit reference '+repr(ref))
 possible=[x for x in ancestors[label] if x.startswith(ref)]
 if len(possible)!=1:raise AssertionError('commit not unique ancestor '+label+' '+ref)
 commit_checked.append({'repository':label,'reference':ref,'commit':possible[0]})
front=STAGE/'docs/implementation/m3/IMPLEMENTATION-STATUS.md';links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',front.read_text());relative=[]
for target in links:
 if target.startswith(('http:','https:','#')):continue
 target=target.split('#')[0]
 if not target:continue
 options=[front.parent/target,A/'docs/implementation/m3'/target]
 assert any(x.is_file() for x in options),'missing relative link '+target
 relative.append(target)
for card in load('decisions.json')['decisions']:assert card['owner'] and 'blocks' in card and card['nextAction']
source=load('source.json');checks=load('checks.json');assert source['acceptedScopedRecords']==405 and checks['scopedRecords']==405
assert source['productQualification'] is False and checks['entirePlanComplete'] is False
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=A).decode().strip()=='ca334cf73d0bde17680106d618c892c2c2fda3ef'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=P).decode().strip()=='e39cee850864df377d0a4d54287348b752257874'
assert not subprocess.check_output(['git','status','--porcelain=v1'],cwd=P)
protected=json.loads(Path('/tmp/opensip-implementation/d4factory-takeover-2026-10-21/protected-architecture-r2.json').read_text())
for f in protected:
 raw=(A/f['path']).read_bytes();assert len(raw)==f['bytes'] and h(raw)==f['sha256']
report={'passed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'acceptedScopedRecords':405,'prior404RecordsUnchanged':True,'uniquePublicPinsMatched':len(matched),'historicalProductPinsPreservedByValue':len(historical_product_pins),'commitReferencesVerified':len(commit_checked),'relativeLinksResolved':len(relative),'protectedDraftsUnchanged':len(protected),'planningOnlyE405':True,'newProductTestsRun':False,'nativeToolsRun':False,'unitAcceptance':False,'productQualification':False,'entireProjectComplete':False}
(B/'factual-checks.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'historical-product-pins-preserved.json').write_text(json.dumps(historical_product_pins,indent=2)+'\n')
(ROOT/'verified-public-pins.json').write_text(json.dumps(matched,indent=2)+'\n')
(ROOT/'commit-reference-checks.json').write_text(json.dumps(commit_checked,indent=2)+'\n')
(ROOT/'ancestry-at-cutoff.json').write_text(json.dumps({k:sorted(v) for k,v in ancestors.items()},indent=2)+'\n')
print(json.dumps(report))
