#!/usr/bin/env python3
"""Structural custody/application checker; never performs a semantic review.

Candidate mode still exits nonzero when evidence/review/application inputs are
pending. Final mode additionally requires an external independent whole review
binding the exact application SHA, every row grade and the exact register image.
No command writes the register. --report writes only the requested report.

Finalization additions to the draft shape:
  The pinned readiness-register.proposed-edits manifest supplies sourceSha256,
  proposedSha256, rowEdits and full byteEdits:[{before:str,after:str}, ...].
  --proposed-register selects the post-image (default: its retained v1 path).
  rows[].reviewerGradesRequired.<grade>.status = EXTERNAL-WHOLE-REVIEW
  rows[].MF6.status = EXTERNAL-WHOLE-REVIEW
  pendingFinalization = []; pendingUnitPinsOrReviews = [] throughout.

The external --whole-review JSON must contain documentClass
independent-whole-application-review, reviewer {id, authoredNoneOfSubjectBytes:
true}, subject {path,sha256}, verdict ACCEPT|CONSENT, mustFix:0, shouldFix:0,
findings:[], registerImage {sourceSha256,proposedSha256}, and rows[].grades with
application,D056_gate2,D056_gate3,SATISFIED, each {verdict:ACCEPT|CONSENT,
mustFix:0,shouldFix:0,findings:[]}, plus rows[].MF6 {beforeSha256,afterSha256,
verdict:ACCEPT|CONSENT,mustFix:0,shouldFix:0,findings:[]}.
It also supplies enactmentImage (exactly the checker's proposed-act image),
ownerActGrades for all seven ACT IDs and scopeApplicationGrades for SD-1..8.
Each grade has verdict ACCEPT|CONSENT, integer mustFix:0 and shouldFix:0, and
findings:[]. These approve prospective integrated acts, not prior enactment.
It also supplies documentationImage {proposalSha256,files:[{path,beforeSha256,
afterSha256}, ...]} and handoffImage {path,sha256}, exactly as this checker's
document-publication result derives from the pinned twelve-file proposal.
These are attestations by a real independent reviewer, not fields this checker
can legitimately author on their behalf. Keeping that verdict external avoids
a cryptographic cycle between the application and its review.
"""
from __future__ import annotations
import argparse,collections,difflib,hashlib,json,re,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
HEX=re.compile(r'[0-9a-f]{64}')
TARGET=set('DR-101 DR-103 DR-105 DR-107 DR-111 DR-112 DR-114 DR-118 DR-120 DR-121 DR-122 DR-124 DR-125 DR-126 DR-127 DR-131 DR-133'.split())
PRIOR=set('DR-102 DR-104 DR-115 DR-117 DR-119 DR-123'.split())
AFFECTED=TARGET|PRIOR
DEFERRED=set('DR-106 DR-108 DR-109 DR-110 DR-113 DR-116 DR-128 DR-129 DR-130'.split())
GATES_BEFORE={f'DR-G{i:02d}' for i in range(1,33)}-{'DR-G06','DR-G11','DR-G13','DR-G17'}
GATES_AFTER=GATES_BEFORE|{'DR-G13'}
GRADES=('application','D056_gate2','D056_gate3','SATISFIED')
DOCUMENT_PATHS=set(['README.md','docs/architecture/current/README.md','docs/architecture/current/00-status-and-authority.md','docs/architecture/current/01-semantic-model-and-host-authority.md','docs/architecture/current/02-distribution-and-components.md','docs/architecture/current/03-configuration-and-security.md','docs/architecture/current/04-lifecycle-delivery-and-operations.md','docs/architecture/current/12-architecture-completion-goal.md','BLOCKED-FOR-OWNER.md','DECISIONS-NEEDED.md','HANDOFF.D-000-orchestrator-live.txt','docs/architecture/record/ARCHITECTURE-TO-IMPLEMENTATION-PLAN.md'])
ACCEPTED=re.compile(r'(?:ACCEPT|CONSENT|NO-OBJECTION)(?:-[A-Z0-9-]+)?')

def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict(raw):
 def unique(pairs):
  out={}
  for k,v in pairs:
   if k in out:raise ValueError('duplicate JSON key: '+k)
   out[k]=v
  return out
 def bad(_):raise ValueError('nonfinite JSON number')
 v=json.loads(raw.decode('utf-8'),object_pairs_hook=unique,parse_constant=bad)
 if not isinstance(v,dict):raise ValueError('JSON object required')
 return v

def pointer(value,p):
 if not isinstance(p,str) or p and not p.startswith('/'):raise ValueError('not a JSON Pointer')
 if p=='':return value
 for part in p.split('/')[1:]:
  if re.search(r'~(?![01])',part):raise ValueError('invalid JSON Pointer escape')
  part=part.replace('~1','/').replace('~0','~')
  if isinstance(value,list):
   if not re.fullmatch(r'0|[1-9][0-9]*',part):raise ValueError('noncanonical array index')
   value=value[int(part)]
  elif isinstance(value,dict):value=value[part]
  else:raise ValueError('pointer crosses scalar')
 return value

def walk(value,where=''):
 yield where,value
 if isinstance(value,dict):
  for k,v in value.items():yield from walk(v,where+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from walk(v,where+'/'+str(i))

def full_hashes(value):return {v for _,v in walk(value) if isinstance(v,str) and HEX.fullmatch(v)}

def accepted(verdict,whole=False):
 return verdict in ['ACCEPT','CONSENT'] if whole else isinstance(verdict,str) and ACCEPTED.fullmatch(verdict) is not None

def zero_findings(value,whole=False):
 if whole:
  return all(type(value.get(k)) is int and value[k]==0 for k in ['mustFix','shouldFix']) and value.get('findings')==[]
 # Historical unit verdicts have several retained field dialects. Missing fields
 # are not silently interpreted as a numerical zero: the formal accepted verdict
 # remains the authority, and every declared rejecting list/count must be empty.
 for key in ['mustFix','shouldFix','mustFindings','should','mustFixCount','shouldFixCount','blockingFindings']:
  if key in value:
   v=value[key]
   if isinstance(v,list):
    if v:return False
   elif type(v) is not int or v!=0:return False
 return True

def apply_byte_edits(source,edits):
 if not isinstance(edits,list) or not edits:raise ValueError('complete nonempty byteEdits required')
 if all(isinstance(e,dict) and set(e)=={'before','after'} for e in edits):
  # Exact UTF-8 line blocks, as the retained proposed-edits manifest specifies.
  ranges=[];pairs=[]
  for e in edits:
   if not isinstance(e['before'],str) or not isinstance(e['after'],str):raise ValueError('text byte-edit values required')
   before,after=e['before'].encode('utf-8'),e['after'].encode('utf-8')
   if not before or source.count(before)!=1:raise ValueError('before must occur exactly once in original source')
   start=source.index(before);ranges.append((start,start+len(before)));pairs.append((before,after))
  ranges.sort()
  if any(left[1]>right[0] for left,right in zip(ranges,ranges[1:])):raise ValueError('overlapping original byte-edit ranges')
  result=source
  for before,after in pairs:
   if result.count(before)!=1:raise ValueError('sequential preimage ambiguous or missing')
   result=result.replace(before,after,1)
  return result
 cursor=0;out=[]
 for e in edits:
  if not isinstance(e,dict) or set(e)-{'startByte','endByte','beforeHex','afterHex','kind','id','rows'}:raise ValueError('closed byte edit required')
  start,end=e.get('startByte'),e.get('endByte')
  if type(start) is not int or type(end) is not int or not cursor<=start<=end<=len(source):raise ValueError('overlapping, unsorted or invalid byte offsets')
  for k in ['beforeHex','afterHex']:
   if not isinstance(e.get(k),str) or not re.fullmatch(r'(?:[0-9a-f]{2})*',e[k]):raise ValueError('canonical hex required')
  before,after=bytes.fromhex(e['beforeHex']),bytes.fromhex(e['afterHex'])
  if before!=source[start:end]:raise ValueError('byte edit preimage mismatch')
  out.extend([source[cursor:start],after]);cursor=end
 out.append(source[cursor:]);return b''.join(out)

def suggest_byte_edits(source,proposed):
 # An author aid only. A final reviewer must approve these bytes in the app.
 a=source.splitlines(keepends=True);b=proposed.splitlines(keepends=True)
 offsets=[0]
 for line in a:offsets.append(offsets[-1]+len(line))
 result=[]
 for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes():
  if tag!='equal':result.append({'startByte':offsets[i],'endByte':offsets[j],'beforeHex':b''.join(a[i:j]).hex(),'afterHex':b''.join(b[k:l]).hex()})
 return result

def register_rows(raw):
 out={}
 for line in raw.decode('utf-8').splitlines():
  m=re.match(r'^\| (DR-(?:G)?\d{2,3})(?:\s|\|)',line)
  if m:
   if m[1] in out:raise ValueError('duplicate register row '+m[1])
   out[m[1]]=line
 return out

def required_gates(rows):
 return {k for k,line in rows.items() if k.startswith('DR-G') and 'harness.'+k+'.' in line.split('|')[3] and 'not required-now' not in line.split('|')[3]}

class Audit:
 def __init__(self,root=ROOT):self.root=root.resolve();self.checks=[];self.cache={};self.pin_cache={};self.known_files=set();self.archives={};self.observed={}
 def add(self,id,ok,detail=None,pending=False):
  row={'id':id,'status':'PASS' if ok else 'PENDING' if pending else 'FAIL'}
  if detail is not None:row['detail']=detail
  self.checks.append(row);return ok
 def path(self,name,base=None):
  if not isinstance(name,str):raise ValueError('path is not text')
  p=Path(name)
  if not p.is_absolute():p=self.root/p if name.startswith('docs/') else (base or HERE)/p
  p=p.resolve()
  if not p.is_relative_to(self.root):raise ValueError('pinned path escapes workspace')
  return p
 def archive(self,logical,snapshot,expected=None):
  """Install an explicit historical-byte source, without changing logical paths."""
  if not isinstance(logical,str) or Path(logical).is_absolute() or Path(logical).as_posix()!=logical or '..' in Path(logical).parts:raise ValueError('canonical repository-relative snapshot path required')
  p=self.path(logical,base=self.root);snapshot=Path(snapshot).resolve();raw=snapshot.read_bytes();actual=sha(raw)
  if expected is not None and (not isinstance(expected,str) or not HEX.fullmatch(expected) or actual!=expected):raise ValueError('snapshot whole-file SHA mismatch: '+logical)
  if p in self.archives and self.archives[p][1]!=actual:raise ValueError('conflicting snapshot for '+logical)
  self.archives[p]=(snapshot,actual)
 def load_snapshot(self,manifest):
  manifest=manifest.resolve();data=strict(manifest.read_bytes())
  if set(data)!={'schemaVersion','files'} or type(data['schemaVersion']) is not int or data['schemaVersion']!=1 or not isinstance(data['files'],list):raise ValueError('closed snapshot manifest version 1 required')
  seen=set();entries=[]
  for e in data['files']:
   if not isinstance(e,dict) or set(e)!={'path','sha256','snapshotPath'} or not isinstance(e['path'],str) or not isinstance(e['snapshotPath'],str) or not e['snapshotPath']:raise ValueError('closed snapshot file entry required')
   if e['path'] in seen:raise ValueError('duplicate logical snapshot path')
   seen.add(e['path']);entries.append(e)
  for e in entries:self.archive(e['path'],manifest.parent/e['snapshotPath'],e['sha256'])
 def read(self,p):
  p=p.resolve()
  if p in self.archives:
   archive,expected=self.archives[p];raw=archive.read_bytes()
   if sha(raw)!=expected:raise ValueError('snapshot changed after admission: '+str(p.relative_to(self.root)))
  else:raw=p.read_bytes()
  if p in self.observed and self.observed[p]!=raw:raise ValueError('source changed during check: '+str(p.relative_to(self.root)))
  return raw
 def json(self,p):
  raw=self.read(p);key=(p,sha(raw))
  if key not in self.cache:self.cache[key]=strict(raw)
  return self.cache[key]
 def capture_snapshot(self,destination):
  # Capture only successfully pinned bytes. Pending pins are never promoted.
  # Existing directories are refused; callers must retain the resulting tree.
  captured=[]
  for p in sorted(self.known_files):
   raw=self.read(p)
   if self.observed[p]!=raw:raise ValueError('source changed before snapshot')
   captured.append((p,raw))
  destination=destination.resolve();destination.mkdir(parents=True,exist_ok=False);entries=[]
  for p,raw in captured:
   logical=p.relative_to(self.root).as_posix();relative='files/'+logical;target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
   entries.append({'path':logical,'sha256':sha(raw),'snapshotPath':relative})
  manifest=destination/'snapshot-manifest.json';manifest.write_text(json.dumps({'schemaVersion':1,'files':entries},indent=2)+'\n')
  return {'path':str(manifest),'sha256':sha(manifest.read_bytes()),'files':len(entries),'scope':'Successfully pinned historical inputs only; not an acceptance verdict. Live publication custody remains checked separately.'}
 def pin(self,r,id,base=None):
  if not isinstance(r,dict):self.add(id,False,'pinned reference missing',True);return None
  expected=r.get('pin',r.get('sha256'))
  if not isinstance(expected,str) or HEX.fullmatch(expected) is None:
   self.add(id,False,'final lowercase SHA-256 required; observedSha256 is not a final pin',True);return None
  try:
   if isinstance(r.get('source'),str) and str(r.get('path','')).startswith('/tmp/'):
    actual=sha(r['source'].encode('utf-8'));self.add(id,actual==expected,{'embeddedReviewerSource':r['path'],'expected':expected,'actual':actual});return None
   p=self.path(r['path'],base);raw=self.read(p);pinned_raw=raw
   if 'startHeading' in r or 'endHeading' in r:
    text=raw.decode('utf-8');start=r['startHeading'];end=r['endHeading']
    if text.count(start)!=1 or text.count(end)!=1 or text.index(start)>=text.index(end):raise ValueError('unambiguous ordered section delimiters required')
    pinned_raw=text[text.index(start):text.index(end)].encode('utf-8')
   actual=sha(pinned_raw)
   self.add(id,actual==expected,{'path':str(p.relative_to(self.root)),'expected':expected,'actual':actual})
   if actual!=expected:return None
   self.known_files.add(p);self.observed[p]=raw
   if 'selector' in r:self.selector(p,raw,r['selector'],id+'/selector')
   return p
  except (OSError,KeyError,ValueError) as e:self.add(id,False,str(e));return None
 def selector(self,p,raw,selector,id):
  try:
   if isinstance(selector,list):
    if not selector:raise ValueError('empty selector list')
    for i,v in enumerate(selector):self.selector(p,raw,v,id+'/'+str(i))
    return
   if p.suffix=='.json':pointer(self.json(p),selector)
   elif isinstance(selector,dict):
    lines=raw.decode().splitlines()
    if set(selector)=={'exactLine'}:
     if lines.count(selector['exactLine'])!=1:raise ValueError('exact line must match once')
    elif set(selector)=={'markdownTableKey'}:
     if sum(l.startswith('| '+selector['markdownTableKey']+' |') for l in lines)!=1:raise ValueError('table key must match once')
    elif set(selector)=={'exactText'}:
     if raw.decode().count(selector['exactText'])!=1:raise ValueError('exact text must match once')
    else:raise ValueError('unsupported closed selector object')
   elif selector=='':pass
   elif isinstance(selector,str) and selector.startswith('#'):
    if raw.decode().splitlines().count(selector)!=1:raise ValueError('exact heading must match once')
   elif isinstance(selector,str) and re.fullmatch(r'SD-[1-8]',selector):
    if sum(l.startswith('| '+selector+' |') for l in raw.decode().splitlines())!=1:raise ValueError('scope table key missing')
   else:raise ValueError('descriptive selector is not exact; use JSON Pointer, exact heading/text/line or empty whole-file selector')
   self.add(id,True)
  except (ValueError,KeyError,IndexError,TypeError,UnicodeError) as e:self.add(id,False,str(e))
 def pin_records(self,value,base,where,historical_context=False):
  """Recognize retained list and filename-keyed freeze/review pin dialects."""
  found=[]
  for pointer_,v in walk(value):
   if not isinstance(v,dict):continue
   if '/input/' in pointer_ and isinstance(v.get('path'),str) and not v['path'].startswith(('docs/','/')):
    # A retained probe's manifest member path is relative to its fixture
    # archive, not a repository source pin. The enclosing verdict bytes are
    # pinned; execution/admission of that member belongs to the unit checker.
    continue
   if 'path' in v and ('sha256' in v or 'pin' in v):found.append((pointer_,v))
   if isinstance(v.get('subject'),str) and 'subjectSha256' in v:found.append((pointer_+'/subject',{'path':v['subject'],'sha256':v['subjectSha256']}))
   for k,x in v.items():
    # Map keys are file paths, never opaque IDs or sha->bytes dictionaries.
    if '/' not in k and not re.search(r'\.(?:json|md|py|sql|cjs|txt|ts|tar|zst|hex|bin|csv|yaml|yml|cnf)$',k):continue
    if isinstance(x,str) and HEX.fullmatch(x):found.append((pointer_+'/'+k,{'path':k,'sha256':x}))
    elif isinstance(x,dict) and isinstance(x.get('sha256'),str) and 'path' not in x:found.append((pointer_+'/'+k,{'path':k,'sha256':x['sha256']}))
  seen=set();resolved=[]
  for loc,r in found:
   signature=(r.get('path'),r.get('pin',r.get('sha256')))
   if signature in seen:continue
   seen.add(signature)
   if historical_context and loc.startswith('/contextReadPins/'):
    # This explicitly named review-provenance field is not a frozen subject or
    # operative dependency. Never promote it to an active evidence check.
    try:actual=sha(self.path(r['path'],base).read_bytes())
    except (OSError,ValueError):actual=None
    self.checks.append({'id':where+loc,'status':'CONTEXT','detail':{'path':r['path'],'historicalPin':r.get('pin',r.get('sha256')),'currentSha256':actual,'activeEvidence':False}})
    continue
   p=self.pin(r,where+loc,base)
   if p:resolved.append((p,r.get('pin',r.get('sha256'))))
  return resolved

def check_exact_set(a,id,values,expected):
 a.add(id,isinstance(values,list) and len(values)==len(expected) and all(isinstance(v,str) for v in values) and set(values)==expected,{'expected':sorted(expected),'actual':values})

def source_inventory(a,app):
 candidates=[r for r in app.get('inputs',[]) if str(r.get('path','')).endswith('architecture-obligation-map.draft.json')]
 if len(candidates)!=1:a.add('source-obligation-map',False,'exact pinned inherited obligation map required');return None
 p=a.pin(candidates[0],'source-obligation-map')
 return a.json(p) if p else None

def check_structure(a,app):
 check_exact_set(a,'affected-exact-23',app.get('preservedAffectedSet'),AFFECTED)
 check_exact_set(a,'deferred-exact-9',app.get('preservedWholeRowDeferredSet'),DEFERRED)
 rows=app.get('rows',[])
 check_exact_set(a,'target-exact-17',[r.get('row') for r in rows if isinstance(r,dict)],TARGET)
 pairs=[(r['row'],o.get('id')) for r in rows for o in r.get('obligations',[])]
 a.add('obligations-47-unique',len(pairs)==47 and len(set(pairs))==47)
 deps=app.get('identityDependencyJoins',[]);keys=[d.get('key') for d in deps]
 a.add('qualified-dependencies-86-unique',len(keys)==86 and len(set(keys))==86)
 inherited=source_inventory(a,app)
 if inherited:
  expected={(r['row'],o['id']) for r in inherited['rows'] for o in r['obligations']}
  a.add('obligations-match-inherited-identities',set(pairs)==expected)
  originals={r['row']:r for r in inherited['rows']}
  for row in rows:
   original=originals.get(row.get('row'),{})
   for field,sourcefield in [('inheritedContract','inheritedContract'),('priorMeasuredJoin','priorJoin')]:
    ref=row.get(field);source=original.get(sourcefield)
    a.add('inherited/'+row['row']+'/'+field,(ref is None and source is None) or isinstance(ref,dict) and isinstance(source,dict) and ref.get('path')==source.get('path') and ref.get('pin')==source.get('sha256'))
 # The independently pinned evidence map enumerates the exact source-qualified
 # dependency identity set; labels alone or replacement IDs cannot satisfy it.
 maps=[r for r in app.get('inputs',[]) if str(r.get('path','')).endswith('architecture-evidence-map.draft.json')]
 if len(maps)==1:
  p=a.pin(maps[0],'source-dependency-map')
  if p:
   expected={(d['row']+':'+d['id'],d['source']['path'],d['source']['selector'],d['source']['sha256']) for d in a.json(p)['identityDependencies']}
   actual={(d.get('key'),d.get('source',{}).get('path'),d.get('source',{}).get('selector'),d.get('source',{}).get('pin')) for d in deps}
   a.add('dependency-source-identity-set',actual==expected)
 else:a.add('source-dependency-map',False,'exact pinned source-qualified dependency map required')
 targets=app.get('evidenceTargets',{});units=app.get('units',{})
 for key,t in targets.items():
  a.add('target/'+key+'/unit',t.get('unit') in units)
  a.add('target/'+key+'/clause',isinstance(t.get('clause'),str) and bool(t['clause'].strip()))
  a.add('target/'+key+'/sources',bool(t.get('sources')))
 for r in rows:
  rid=r['row']
  for o in r.get('obligations',[]):
   label=rid+'/'+str(o.get('id'));refs=o.get('evidenceTargets',[])
   a.add('obligation/'+label+'/targets',bool(refs) and all(v in targets for v in refs))
   a.add('obligation/'+label+'/disposition',o.get('proposedDisposition') in ['DESIGN-DECIDED','SCOPE-RIDE'])
   if o.get('proposedDisposition')=='SCOPE-RIDE':
    sd=app.get('scopeDispositions',{}).get(o.get('scopeDispositionId'),{})
    a.add('obligation/'+label+'/five-part-ride',all(sd.get(k) for k in ['source','exactObligationBranch','governingExcludedScopeAndPositiveWork','reentryTriggerAndOwner','activeEvidenceRequirement']))
  grades=r.get('reviewerGradesRequired',{})
  a.add('row/'+rid+'/four-grade-slots',set(grades)==set(GRADES))
  for g in GRADES:
   entry=grades.get(g,{})
   a.add('row/'+rid+'/'+g+'/declared',entry.get('status')=='EXTERNAL-WHOLE-REVIEW' or accepted(entry.get('verdict'),True),entry.get('status'),True)
  a.add('row/'+rid+'/MF6-declared',r.get('MF6',{}).get('status')=='EXTERNAL-WHOLE-REVIEW' or r.get('MF6',{}).get('status')=='INDEPENDENTLY-APPROVED',r.get('MF6',{}).get('status'),True)
 for d in deps:
  refs=d.get('proposedTargets',[])
  a.add('dependency/'+str(d.get('key'))+'/qualified',bool(d.get('sourceOwner')) and d.get('key')==d.get('sourceRow','')+':'+d.get('id','') and bool(refs) and all(v.get('clauseRef') in targets and v.get('unit')==targets[v['clauseRef']]['unit'] and bool(v.get('concreteClause')) for v in refs))
 for loc,v in walk(app):
  if isinstance(v,dict):
   if 'path' in v and ('pin' in v or 'sha256' in v):a.pin(v,'application-pin'+loc)
   for k in ['pendingUnitPinsOrReviews','pendingFinalization']:
    if k in v:a.add('no-pending'+loc+'/'+k,v[k]==[],v[k],True)
   for k in ['status','reviewStanding','adoption']:
    text=v.get(k)
    if isinstance(text,str) and re.search(r'\b(?:PENDING|DRAFT)\b',text):a.add('pending-state'+loc+'/'+k,False,text,True)
 a.add('checker-does-not-authorize-implementation',app.get('condition5Authorization') is False)
 a.add('checker-does-not-claim-qualification',app.get('qualificationClaim') is False)

def unit_subjects(freeze):
 files=freeze.get('subjects',freeze.get('files'))
 if isinstance(files,list):return {v.get('sha256') for v in files if isinstance(v,dict) and HEX.fullmatch(str(v.get('sha256','')))}
 if isinstance(files,dict):return {v if isinstance(v,str) else v.get('sha256') for v in files.values() if isinstance(v,(str,dict))}
 if HEX.fullmatch(str(freeze.get('subjectSha256',''))):return {freeze['subjectSha256']}
 return set()

def finding_ids(review):
 ids=[]
 for field in ['mustFix','shouldFix','mustFindings','should','blockingFindings']:
  items=review.get(field,[])
  if isinstance(items,list):
   for i,v in enumerate(items):ids.append(v.get('id',field+'/'+str(i)) if isinstance(v,dict) else str(v))
  elif type(items) is int and items:ids.append(field+':'+str(items))
 return ids

def check_resolution(a,unitid,resolution,original_review_hash):
 label='unit/'+unitid+'/resolution/'+str(resolution.get('findingId'))
 p=a.pin(resolution.get('review'),label+'/review')
 if not p:return False
 review=a.json(p);a.pin_records(review,p.parent,label+'/supplement-inputs',historical_context=True);ok=accepted(review.get('verdict')) and zero_findings(review)
 a.add(label+'/accepted-supplement',ok)
 bound=original_review_hash in full_hashes(review)
 if resolution.get('repairFreeze'):
  fp=a.pin(resolution['repairFreeze'],label+'/repair-freeze')
  if fp:
   freeze=a.json(fp);a.pin_records(freeze,fp.parent,label+'/repair-inputs')
   bound=bound or sha(a.read(fp)) in full_hashes(review) and original_review_hash in full_hashes(freeze)
 a.add(label+'/original-review-bound',bound)
 try:
  ptr=resolution['resolutionPointer'];value=pointer(review,ptr);fid=resolution['findingId']
  if isinstance(value,dict):resolved=value.get('findingId',value.get('id'))==fid and value.get('status') in ['RESOLVED','ADDRESSED','CLOSED']
  else:resolved=fid in ptr.split('/') and isinstance(value,str) and re.match(r'^(RESOLVED|ADDRESSED|CLOSED)(?:\b|:)',value) is not None
 except (KeyError,ValueError,TypeError,IndexError):resolved=False
 a.add(label+'/exact-finding-resolved',resolved)
 return ok and bound and resolved

def check_units(a,app):
 for id,u in app.get('units',{}).items():
  label='unit/'+id;fp=a.pin(u.get('freeze'),label+'/freeze');rp=a.pin(u.get('review'),label+'/review')
  if not fp or not rp:continue
  try:
   freeze=a.json(fp);review=a.json(rp)
   a.pin_records(freeze,fp.parent,label+'/frozen-inputs')
   a.pin_records(review,rp.parent,label+'/reviewed-inputs',historical_context=True)
   hashes=full_hashes(review);subjects=unit_subjects(freeze)
   a.add(label+'/review-binds-freeze-or-all-subjects',sha(a.read(fp)) in hashes or bool(subjects) and subjects<=hashes)
   a.add(label+'/accepted-verdict',accepted(review.get('verdict')),review.get('verdict'))
   unresolved=finding_ids(review);resolved=set()
   for r in u.get('findingResolutions',[]):
    if check_resolution(a,id,r,sha(a.read(rp))):resolved.add(r.get('findingId'))
   a.add(label+'/no-undisposed-findings',not (set(unresolved)-resolved),{'unresolved':sorted(set(unresolved)-resolved)})
   # A numeric nonzero count cannot be made empty by omitting item details.
   if not unresolved:a.add(label+'/declared-counts-consistent',zero_findings(review))
  except (OSError,ValueError,TypeError,KeyError) as e:a.add(label+'/parse',False,str(e))

def check_register(a,app,proposed_path):
 refs=[r for r in app.get('inputs',[]) if str(r.get('path','')).endswith('.json') and 'proposed-edits' in str(r.get('path',''))]
 if len(refs)!=1:a.add('register/manifest',False,'one exact pinned proposed-edits manifest required');return None
 p=a.pin(refs[0],'register/manifest')
 if not p:return None
 try:
  m=a.json(p)
  sp=a.pin({'path':m['destination'],'pin':m['sourceSha256']},'register/source')
  pp=a.pin({'path':str(proposed_path),'pin':m['proposedSha256']},'register/proposed')
  if not sp or not pp:return None
  source,proposed=a.read(sp),a.read(pp);before,after=register_rows(source),register_rows(proposed)
  current=sp.read_bytes();a.add('register/current-custody',current in [source,proposed],{'phase':'BEFORE' if current==source else 'AFTER' if current==proposed else 'DIVERGED'})
  edits=m.get('rowEdits',[]);byid={e['row']:e for e in edits}
  check_exact_set(a,'register/exact-17-plus-G13',[e.get('row') for e in edits],TARGET|{'DR-G13'})
  for r in app['rows']:
   rid=r['row'];mf=r.get('MF6',{});e=byid.get(rid,{})
   a.add('register/'+rid+'/exact-MF6',e.get('before')==mf.get('before')==before.get(rid) and e.get('after')==mf.get('after')==after.get(rid))
   a.add('register/'+rid+'/whole-image-pins',mf.get('expectedRegisterBeforeSha256')==m['sourceSha256'] and mf.get('draftWholeRegisterAfterSha256')==m['proposedSha256'])
  a.add('register/G13/exact-edit',byid.get('DR-G13',{}).get('before')==before.get('DR-G13') and byid.get('DR-G13',{}).get('after')==after.get('DR-G13'))
  a.add('register/other-row-bytes-preserved',all(before.get(k)==after.get(k) for k in set(before)|set(after) if k not in TARGET|{'DR-G13'}))
  a.add('register/23-SATISFIED-status-cells',all(re.match(r'^\*{0,2}SATISFIED\b',after.get(k,'').split('|')[6].strip()) is not None for k in AFFECTED))
  a.add('register/28-required-before',required_gates(before)==GATES_BEFORE,sorted(required_gates(before)))
  a.add('register/29-required-after',required_gates(after)==GATES_AFTER,sorted(required_gates(after)))
  g13=after.get('DR-G13','').split('|')
  a.add('register/G13/harness-and-owner',len(g13)>5 and 'harness.DR-G13.typescript-quality.preview' in g13[3] and all(s in g13[5] for s in ['Language quality','Product','Release engineering']))
  a.add('register/gate-summary-29','29 of 29 required gates' in proposed.decode())
  try:
   reproduced=apply_byte_edits(source,m.get('byteEdits'))
   a.add('register/byte-application-exact',reproduced==proposed and sha(reproduced)==m['proposedSha256'],{'reproducedSha256':sha(reproduced),'expectedSha256':m['proposedSha256']})
  except (KeyError,TypeError,ValueError,UnicodeError) as e:
   a.add('register/byte-application-exact',False,str(e),True)
  return {'sourceSha256':m['sourceSha256'],'proposedSha256':m['proposedSha256'],'rows':byid}
 except (ValueError,OSError,KeyError,TypeError) as e:a.add('register/parse',False,str(e));return None

def check_document_edits(a,app):
 d=app.get('documentationApplication',{})
 pp=a.pin(d.get('docEditsProposal'),'documents/proposal');hp=a.pin(d.get('handoff'),'documents/handoff');a.pin(d.get('normativeReview'),'documents/normative-review')
 check_exact_set(a,'documents/declared-exact-12',d.get('expectedDocumentPaths'),DOCUMENT_PATHS)
 a.add('documents/external-grade-declared',d.get('reviewerGradeRequired',{}).get('status')=='EXTERNAL-WHOLE-REVIEW',d.get('reviewerGradeRequired',{}).get('status'),True)
 if not pp or not hp:return None
 try:
  proposal=a.json(pp);edits=proposal.get('edits',[]);check_exact_set(a,'documents/proposal-exact-12',[e.get('path') for e in edits],DOCUMENT_PATHS);images=[]
  for e in edits:
   path=e['path'];before=e['before'].encode('utf-8');after=e['after'].encode('utf-8');sp=a.path(path,base=a.root);current=sp.read_bytes()
   a.add('documents/'+path+'/closed-edit',set(e)=={'path','beforeSha256','afterSha256','before','after'})
   a.add('documents/'+path+'/exact-preimage',HEX.fullmatch(str(e['beforeSha256'])) is not None and sha(before)==e['beforeSha256'])
   a.add('documents/'+path+'/exact-postimage',HEX.fullmatch(str(e['afterSha256'])) is not None and sha(after)==e['afterSha256'])
   # A retained proposal remains replayable after publication. The live file
   # must be exactly one of its two pinned images, never an unrelated edit.
   a.add('documents/'+path+'/current-custody',current in [before,after],{'phase':'BEFORE' if current==before else 'AFTER' if current==after else 'DIVERGED'})
   images.append({'path':path,'beforeSha256':e['beforeSha256'],'afterSha256':e['afterSha256']})
  return {'documentationImage':{'proposalSha256':sha(a.read(pp)),'files':sorted(images,key=lambda x:x['path'])},'handoffImage':{'path':str(hp.relative_to(a.root)),'sha256':sha(a.read(hp))}}
 except (OSError,ValueError,TypeError,KeyError,AttributeError) as e:a.add('documents/malformed',False,str(e));return None

OWNER_ACT_IDS={'ACT-FC-C1','ACT-SC-TRUST-CONCURRENCE','ACT-CLASS-A-DR131','ACT-CLASS-A-DR133','ACT-G13-ROSTER','ACT-SCOPE-RIDES','ACT-REFERENCE-AND-NUMERIC'}
SCOPE_IDS={f'SD-{i}' for i in range(1,9)}
PROPOSED_ENACTMENT='PROPOSED-FOR-INTEGRATED-ENACTMENT'
ENACTMENT_ORDER=['independent-whole-review','integrated-D369-enactment','verify-published-images','claim-design-complete']

def normalized_ref(ref):
 if not isinstance(ref,dict):return None
 return {'path':ref.get('path'),'sha256':ref.get('pin',ref.get('sha256')),'selector':ref.get('selector','')}

def validate_enactment_plan(app):
 """Validate a proposal snapshot; it never asserts that enactment occurred."""
 checks=[]
 def add(k,v):checks.append((k,bool(v)))
 def pinned(r):return isinstance(r,dict) and isinstance(r.get('path'),str) and bool(r['path']) and isinstance(r.get('pin',r.get('sha256')),str) and HEX.fullmatch(r.get('pin',r.get('sha256'))) is not None
 plan=app.get('enactmentPlan',{});acts=app.get('ownerActsRequired',{});scopes=app.get('scopeDispositions',{})
 add('proposal-snapshot',plan.get('status')==PROPOSED_ENACTMENT and plan.get('declarationKind')=='PROPOSAL-NOT-LIVE-ADOPTION-STATE')
 add('not-already-enacted',plan.get('alreadyEnacted') is False)
 add('review-before-enactment',plan.get('requiresWholeReview') is True and plan.get('requiresZeroFindings') is True and plan.get('recordingOrder')==ENACTMENT_ORDER)
 add('implementation-remains-separate',plan.get('implementationAuthorization') is False and app.get('condition5Authorization') is False)
 add('publication-not-claimed',app.get('registerMutation') is False and app.get('documentationApplication',{}).get('applied') is False)
 proposal=plan.get('proposal');add('exact-proposal',pinned(proposal))
 add('seven-owner-acts',set(acts)==OWNER_ACT_IDS)
 add('eight-scope-dispositions',set(scopes)==SCOPE_IDS)
 for id,r in acts.items():
  add('owner/'+id+'/prospective',r.get('status')==PROPOSED_ENACTMENT and r.get('enacted') is False and r.get('enactOnlyAfter')=='WHOLE-REVIEW-ACCEPT-0-0')
  add('owner/'+id+'/external-grade',r.get('reviewerGradeRequired',{}).get('status')=='EXTERNAL-WHOLE-REVIEW' and r.get('reviewerGradeRequired',{}).get('verdict') is None)
  add('owner/'+id+'/concrete-proposal',pinned(r.get('proposal')) and bool(r.get('requiredAct')) and bool(r.get('rows')) and all(x in TARGET for x in r.get('rows',[])))
  add('owner/'+id+'/same-integrated-act',isinstance(proposal,dict) and isinstance(r.get('proposal'),dict) and all(normalized_ref(r['proposal'])[k]==normalized_ref(proposal)[k] for k in ['path','sha256']))
  add('owner/'+id+'/evidence-targets',bool(r.get('evidenceTargets')) and all(x in app.get('evidenceTargets',{}) for x in r.get('evidenceTargets',[])))
 for id,r in scopes.items():
  add('scope/'+id+'/prospective',r.get('adoption')==PROPOSED_ENACTMENT and r.get('enacted') is False and r.get('enactOnlyAfter')=='WHOLE-REVIEW-ACCEPT-0-0')
  add('scope/'+id+'/external-grade',r.get('reviewerGradeRequired',{}).get('status')=='EXTERNAL-WHOLE-REVIEW' and r.get('reviewerGradeRequired',{}).get('verdict') is None)
  add('scope/'+id+'/concrete-proposal',pinned(r.get('enactmentProposal')) and pinned(r.get('source')) and all(r.get(k) for k in ['exactObligationBranch','governingExcludedScopeAndPositiveWork','reentryTriggerAndOwner','activeEvidenceRequirement']))
  add('scope/'+id+'/same-integrated-act',isinstance(proposal,dict) and isinstance(r.get('enactmentProposal'),dict) and all(normalized_ref(r['enactmentProposal'])[k]==normalized_ref(proposal)[k] for k in ['path','sha256']))
 image={'mode':'REVIEW-PROPOSED-ACTS-THEN-ENACT','proposal':normalized_ref(proposal),'recordingOrder':ENACTMENT_ORDER,'ownerActs':[{'id':id,'proposal':normalized_ref(r.get('proposal'))} for id,r in sorted(acts.items())],'scopeDispositions':[{'id':id,'source':normalized_ref(r.get('source')),'proposal':normalized_ref(r.get('enactmentProposal'))} for id,r in sorted(scopes.items())]}
 return checks,image

def check_enactment(a,app):
 try:
  checks,planned=validate_enactment_plan(app)
  for key,ok in checks:a.add('enactment/'+key,ok)
  a.pin(app.get('enactmentPlan',{}).get('proposal'),'enactment/proposal-pin')
  # General application traversal also checks these pins. Explicit checks here
  # keep this function meaningful in isolation and never waive a missing file.
  for id,r in app.get('ownerActsRequired',{}).items():a.pin(r.get('proposal'),'enactment/owner/'+id+'/proposal-pin')
  for id,r in app.get('scopeDispositions',{}).items():a.pin(r.get('enactmentProposal'),'enactment/scope/'+id+'/proposal-pin')
  return planned
 except (ValueError,TypeError,KeyError,AttributeError) as e:a.add('enactment/malformed',False,str(e));return None

def validate_whole_review(review,application_hash,application_path,rows,register,documents,enactment):
 """Pure checks, also used for adversarial selftests with clearly synthetic docs."""
 checks=[]
 def add(k,v):checks.append((k,bool(v)))
 add('class',review.get('documentClass')=='independent-whole-application-review')
 reviewer=review.get('reviewer',{})
 add('independence-attestation',isinstance(reviewer,dict) and isinstance(reviewer.get('id'),str) and bool(reviewer['id'].strip()) and reviewer.get('authoredNoneOfSubjectBytes') is True)
 subject=review.get('subject',{});subject=subject if isinstance(subject,dict) else {}
 add('exact-application-binding',subject.get('sha256')==application_hash and subject.get('path')==application_path)
 add('whole-zero-findings',accepted(review.get('verdict'),True) and zero_findings(review,True))
 rr=review.get('rows',[]);rr=rr if isinstance(rr,list) else [];names=[v.get('row') for v in rr if isinstance(v,dict)]
 add('exact-row-grade-set',len(names)==17 and set(names)==TARGET)
 indexed={v['row']:v for v in rr if isinstance(v,dict) and 'row' in v}
 for row in rows:
  rid=row['row'];r=indexed.get(rid,{});grades=r.get('grades',{});grades=grades if isinstance(grades,dict) else {}
  add(rid+'/exact-four-grades',set(grades)==set(GRADES))
  for g in GRADES:
   value=grades.get(g,{});value=value if isinstance(value,dict) else {}
   add(rid+'/'+g,accepted(value.get('verdict'),True) and zero_findings(value,True))
   declared=row.get('reviewerGradesRequired',{}).get(g,{})
   if declared.get('verdict') is not None:add(rid+'/'+g+'/declared-consistency',declared['verdict']==value.get('verdict'))
  mf=r.get('MF6',{});mf=mf if isinstance(mf,dict) else {};proposed=row.get('MF6',{})
  add(rid+'/MF6-zero-findings',accepted(mf.get('verdict'),True) and zero_findings(mf,True))
  add(rid+'/MF6-exact-bytes',mf.get('beforeSha256')==sha(proposed.get('before','').encode()) and mf.get('afterSha256')==sha(proposed.get('after','').encode()))
 add('register-image-bound',register is not None and review.get('registerImage')=={k:register[k] for k in ['sourceSha256','proposedSha256']})
 add('documentation-image-bound',documents is not None and review.get('documentationImage')==documents['documentationImage'])
 add('handoff-image-bound',documents is not None and review.get('handoffImage')==documents['handoffImage'])
 add('proposed-enactment-image-bound',enactment is not None and review.get('enactmentImage')==enactment)
 for field,ids in [('ownerActGrades',OWNER_ACT_IDS),('scopeApplicationGrades',SCOPE_IDS)]:
  values=review.get(field,{});values=values if isinstance(values,dict) else {}
  add(field+'/exact-set',set(values)==ids)
  for id in sorted(ids):
   grade=values.get(id,{});grade=grade if isinstance(grade,dict) else {}
   add(field+'/'+id,accepted(grade.get('verdict'),True) and zero_findings(grade,True))
 return checks

CLAIM_SOURCE_NAMES=('delivery.v2.json','d9-exit-contract.v1.14.json','fact-plane.v1.json','resolved-inputs.v2.json','operability.v10.json','evaluation-proof.v1.json','fact-identity-policy.v2.json')
SUPPLEMENT_SPECS={
 'additionalIdentityDependencies':[('control-protocol-contract.v2.json','/identityDependencies/dependencies','ID-DEP')],
 'namedOpenConditions':[('host-effect-authorization.v25.json','/failClosed/requiredConditions','NAMED-OPEN-CONDITION'),('canonical-json-profile.v1.json','/undeterminedRegister','NAMED-OPEN-CONDITION')],
 'inheritedClaimRides':[(n,'/decisionDependencies','INHERITED-CLAIM-RIDE') for n in CLAIM_SOURCE_NAMES]
}
SUPPLEMENT_COUNTS={'originalIdentityDependencies':86,'additionalIdentityDependencies':8,'totalIdentityDependencies':94,'namedOpenConditions':11,'inheritedClaimRides':38,'supplementalDefinitions':57,'hostConditionBranches':13,'productEnforcementFixtureClassesNotDefinitions':14,'evidenceCustodyEdgesNotOpenConditions':5}

def validate_supplement(supp,app,read_json):
 """Structural source-definition accounting only; no semantic scope verdict."""
 checks=[]
 def add(k,v):checks.append((k,bool(v)))
 add('class',supp.get('documentClass')=='architecture-incorporated-dependency-supplement' and type(supp.get('schemaVersion')) is int and supp['schemaVersion']==1)
 add('counts',supp.get('counts')==SUPPLEMENT_COUNTS and all(type(v) is int for v in supp.get('counts',{}).values()))
 add('no-qualification-or-register-mutation',supp.get('qualificationClaim') is False and supp.get('registerEdited') is False)
 catalog=supp.get('sourceCatalogue',[]);catalog_paths=[c.get('source',{}).get('path') for c in catalog]
 add('catalogue-unique',len(catalog_paths)==len(set(catalog_paths)))
 catalog_by={c['source']['path']:c for c in catalog if isinstance(c.get('source'),dict) and 'path' in c['source']}
 inherited=read_json(supp['originalBasis']['path'])['identityDependencies']
 old={(d['source']['path'],d['source']['selector'],d['source']['sha256']) for d in inherited}
 add('original86-source-universe',len(old)==86)
 listed_old={(c['source']['path'],p,c['source']['sha256']) for c in catalog for p in c.get('original86DefinitionSelectors',[])}
 add('catalogue-original86-exact',listed_old==old)
 required_extra={'delivery.v4.json','preview-product-boundary-successor.v10.json','anti-lockstep-contract.v7.json','compatibility-matrices-contract.v5.json','component-sdk-contract.v4.json','language-quality-matrix-contract.v13.json','platform-tcb-contract.v48.json','provider-only-output-contract.v3.json','state-class-contract.v11.json','preview-analyze-contract.v2.json','evidence.v10.json'}
 required_paths={d[0] for d in old}|{'docs/architecture/record/artifacts/'+n for specs in SUPPLEMENT_SPECS.values() for n,_,_ in specs}|{'docs/architecture/record/artifacts/'+n for n in required_extra}
 add('catalogue-explicit-source-basis',set(catalog_paths)==required_paths)
 targets=app.get('evidenceTargets',{});all_entries=[]
 for category,specs in SUPPLEMENT_SPECS.items():
  expected={}
  for name,container,kind in specs:
   path='docs/architecture/record/artifacts/'+name;source=read_json(path);c=catalog_by[path]
   for i,value in enumerate(pointer(source,container)):
    ptr=container+'/'+str(i);id=value.get('id',value.get('claim'))
    expected[(path,ptr,c['source']['sha256'],id)]=(kind,value)
  entries=supp.get(category,[]);all_entries.extend(entries)
  identities=[(r.get('source',{}).get('path'),r.get('source',{}).get('selector'),r.get('source',{}).get('sha256'),r.get('id')) for r in entries]
  add(category+'/exact-source-qualified-identities',len(identities)==len(expected) and len(set(identities))==len(identities) and set(identities)==set(expected))
  for i,r in enumerate(entries):
   identity=identities[i];pair=expected.get(identity);ref=r.get('source',{});label=category+'/'+str(i)
   add(label+'/definition-exact',pair is not None and r.get('kind')==pair[0] and r.get('definition')==pair[1])
   add(label+'/qualified-key',r.get('key')==str(ref.get('path'))+'#'+str(ref.get('selector')) and bool(r.get('sourceOwner')) and r.get('outsideOriginal86') is True)
   joins=r.get('proposedJoins',[])
   add(label+'/concrete-targets',bool(joins) and all(j.get('targetRef') in targets and j.get('unit')==targets[j['targetRef']]['unit'] and bool(j.get('concreteClause')) for j in joins))
   if category=='inheritedClaimRides':
    scope=r.get('scopeApplication',{});authorities=scope.get('governingSources',[])
    add(label+'/explicit-scope',scope.get('disposition') in ['ACTIVE-PREVIEW-PRESERVATION','ACTIVE-PREVIEW-REDUCED-RESULT','EXCLUDED-AUTHORITATIVE','EXCLUDED-CONTRIBUTION-RUNTIME','SPLIT-ACTIVE-PREVIEW-AND-EXCLUDED-AUTHORITATIVE'] and bool(scope.get('activeBranch')) and bool(authorities) and scope.get('newScopeRideInvented') is False and bool(scope.get('nonPromotionEvidence')))
    if scope.get('disposition')!='ACTIVE-PREVIEW-PRESERVATION':add(label+'/excluded-branch-explicit',bool(scope.get('excludedBranch')))
    add(label+'/recorded-D002-D018-scope',all(any(isinstance(a.get('selector'),str) and a['selector'].startswith('## '+d+' —') for a in authorities) for d in ['D-002','D-018']))
    if scope.get('disposition') in ['EXCLUDED-AUTHORITATIVE','SPLIT-ACTIVE-PREVIEW-AND-EXCLUDED-AUTHORITATIVE']:add(label+'/recorded-D077-D078-scope',all(any(isinstance(a.get('selector'),str) and a['selector'].startswith('## '+d+' —') for a in authorities) for d in ['D-077','D-078']))
 listed_new={(c['source']['path'],p,c['source']['sha256']) for c in catalog for p in c.get('supplementalDefinitionSelectors',[])}
 actual_new={(r['source']['path'],r['source']['selector'],r['source']['sha256']) for r in all_entries}
 add('catalogue-added57-exact',len(actual_new)==57 and listed_new==actual_new and not old.intersection(actual_new))
 for c in catalog:add('catalogue/'+c['source']['path']+'/count',type(c.get('countedDefinitions')) is int and c['countedDefinitions']==len(c.get('original86DefinitionSelectors',[]))+len(c.get('supplementalDefinitionSelectors',[])))
 add('host-branches13',len(supp.get('hostConditionBranches',[]))==13 and len({x.get('id') for x in supp.get('hostConditionBranches',[])})==13)
 product_path='docs/architecture/record/artifacts/preview-product-boundary-successor.v10.json';ee=read_json(product_path)['enforcementEvidence']['classes'];fixtures=supp.get('productEnforcementClassReferences',[])
 add('product-fixtures-not-definitions',len(fixtures)==14 and all(x.get('countedAsDependencyDefinition') is False for x in fixtures))
 add('product-fixture-exact-pointers',{(x.get('id'),x.get('source',{}).get('path'),x.get('source',{}).get('selector')) for x in fixtures}=={(x['id'],product_path,'/enforcementEvidence/classes/'+str(i)) for i,x in enumerate(ee)})
 host_path='docs/architecture/record/artifacts/host-effect-authorization.v25.json';host=read_json(host_path)
 expected_branches={('CA-1-SPAWN','/coveredActs/CA-1-host-head/subtypes/0'),('CA-1-IN_PROCESS','/coveredActs/CA-1-host-head/subtypes/1'),('CA-2','/coveredActs/CA-2'),('UNCLASSIFIED-HOST-PATH','/slice1EgressExecutionSide/remainderOwner')}|{('CA-3-'+d['id'],'/coveredActs/CA-3/subtypes/'+str(i)) for i,d in enumerate(host['coveredActs']['CA-3']['subtypes'])}|{(d['id'],'/slice1EgressExecutionSide/namedArchitecturePreviewPaths/'+str(i)) for i,d in enumerate(host['slice1EgressExecutionSide']['namedArchitecturePreviewPaths'])}
 add('host-branches-exact-pointers',{(x.get('id'),x.get('source',{}).get('selector')) for x in supp.get('hostConditionBranches',[])}==expected_branches and all(x.get('source',{}).get('path')==host_path and x.get('countedAsDefinition') is False for x in supp.get('hostConditionBranches',[])))
 lineage=supp.get('lineagePreservation',[])
 required_lineages={('component-manifest-schemas.v2.json','component-manifest-schemas.v11.json'),('permission-truth-tables.v1.json','permission-truth-tables.v9.json'),('permission-truth-tables.v2.json','permission-truth-tables.v9.json')}
 add('lineage-exact-pairs',{(Path(x['beforeSource']['path']).name,Path(x['selectedPackageSource']['path']).name) for x in lineage}==required_lineages and len(lineage)==3)
 for i,l in enumerate(lineage):
  before=pointer(read_json(l['beforeSource']['path']),'/identityDependencies/dependencies');after=pointer(read_json(l['selectedPackageSource']['path']),'/identityDependencies/dependencies');bm={d['id']:d for d in before};am={d['id']:d for d in after};members=l.get('members',[])
  add('lineage/'+str(i)+'/all-earlier-ids',len(members)==len(bm) and {m.get('id') for m in members}==set(bm) and l.get('onlyInBefore')==sorted(set(bm)-set(am)) and l.get('onlyInSelected')==sorted(set(am)-set(bm)))
  for j,m in enumerate(members):
   id=m.get('id');b=bm.get(id);v=am.get(id);changes=sorted(k for k in set(b or {})|set(v or {}) if (b or {}).get(k)!=(v or {}).get(k))
   add('lineage/'+str(i)+'/'+str(j)+'/exact-source-pointers',m.get('before',{}).get('path')==l['beforeSource']['path'] and m.get('after',{}).get('path')==l['selectedPackageSource']['path'] and m.get('before',{}).get('selector')=='/identityDependencies/dependencies/'+str(next((k for k,d in enumerate(before) if d['id']==id),-1)) and m.get('after',{}).get('selector')=='/identityDependencies/dependencies/'+str(next((k for k,d in enumerate(after) if d['id']==id),-1)))
   add('lineage/'+str(i)+'/'+str(j)+'/exact-carried-change',b is not None and v is not None and m.get('definitionBefore')==b and m.get('definitionAfter')==v and m.get('changedFields')==changes and m.get('disposition')==('CARRIED-WITH-EXPLICIT-SUCCESSOR-CHANGE' if changes else 'CARRIED-UNCHANGED'))
  expected_act='D-104' if 'manifest' in l['beforeSource']['path'] else 'D-128'
  add('lineage/'+str(i)+'/recorded-authority',str(l.get('recordingAuthority',{}).get('selector')).startswith('## '+expected_act+' —') and bool(l.get('adoptionStanding')))
 edges=supp.get('evidenceCustodyEdges',[]);evidence=read_json('docs/architecture/record/artifacts/evidence.v10.json')['dependencies'];expected_edges={k:v for k,v in evidence.items() if isinstance(v,dict)}
 add('evidence-custody-five',len(edges)==5 and {e.get('id') for e in edges}==set(expected_edges))
 for e in edges:
  v=expected_edges.get(e.get('id'),{});add('evidence/'+str(e.get('id'))+'/exact-edge',e.get('target',{}).get('path')=='docs/architecture/record/artifacts/'+str(v.get('artifact')) and e.get('target',{}).get('sha256')==v.get('sha256')==e.get('embeddedTargetSha256') and e.get('countedAsOpenCondition') is False and e.get('source',{}).get('path')=='docs/architecture/record/artifacts/evidence.v10.json' and e.get('source',{}).get('selector')=='/dependencies/'+str(e.get('id')))
 return checks

def check_supplement(a,app):
 p=a.pin(app.get('incorporatedDependencySupplement'),'incorporated-supplement/present')
 if not p:return None
 try:
  supp=a.json(p)
  a.add('incorporated-supplement/no-pending-finalization',supp.get('pendingFinalization')==[],supp.get('pendingFinalization'),True)
  # All source selectors, custody/authority references and existing evidence pins
  # remain exact, including archive-aware coordinator before-images.
  for loc,v in walk(supp):
   if isinstance(v,dict) and 'path' in v and ('sha256' in v or 'pin' in v):a.pin(v,'incorporated-supplement/pin'+loc)
  for key,ok in validate_supplement(supp,app,lambda name:a.json(a.path(name))):a.add('incorporated-supplement/'+key,ok)
  return {'path':str(p.relative_to(a.root)),'sha256':sha(a.read(p)),'counts':supp.get('counts'),'semanticReviewPerformed':False}
 except (OSError,ValueError,KeyError,TypeError,IndexError,AttributeError) as e:a.add('incorporated-supplement/malformed',False,str(e));return None

def check_whole(a,app,application_path,whole_path,register,documents,enactment):
 if whole_path is None:a.add('whole-review/present',False,'Independent whole review is not supplied; candidate mode cannot imply acceptance.',True);return None
 try:
  raw=whole_path.read_bytes();review=strict(raw)
  # Application cannot contain the bytes/hash of the verdict that must in turn
  # bind it; this catches accidental attempts to create a circular freeze.
  application_sha=sha(application_path.read_bytes())
  a.add('whole-review/separate-file',whole_path.resolve()!=application_path.resolve())
  for k,ok in validate_whole_review(review,application_sha,str(application_path.resolve().relative_to(a.root)),app.get('rows',[]),register,documents,enactment):a.add('whole-review/'+k,ok)
  return {'path':str(whole_path),'sha256':sha(raw)}
 except (OSError,ValueError,TypeError,KeyError,AttributeError) as e:a.add('whole-review/parse',False,str(e));return None

def selftest(report):
 results=[]
 def test(id,fn,expected=True):
  try:actual=fn();ok=actual==expected
  except Exception as e:actual=type(e).__name__;ok=actual==expected
  results.append({'id':id,'expected':expected,'actual':actual,'pass':ok})
 test('duplicate-JSON-rejected',lambda:strict(b'{"x":1,"x":2}'),'ValueError')
 test('pointer-resolves-escaped-slash',lambda:pointer({'a/b':[7]},'/a~1b/0')==7)
 test('pointer-leading-zero-refuses',lambda:pointer([7],'/00'),'ValueError')
 test('pointer-absent-refuses',lambda:pointer({},'/x'),'KeyError')
 test('byte-block-positive',lambda:apply_byte_edits(b'a\nb\nc\n',[{'before':'a\n','after':'A\n'},{'before':'c\n','after':'C\n'}])==b'A\nb\nC\n')
 test('byte-block-duplicate-preimage-refuses',lambda:apply_byte_edits(b'x\nx\n',[{'before':'x\n','after':'y\n'}]),'ValueError')
 test('byte-block-overlap-refuses',lambda:apply_byte_edits(b'abcde',[{'before':'abc','after':'x'},{'before':'cde','after':'y'}]),'ValueError')
 test('byte-block-missing-refuses',lambda:apply_byte_edits(b'a',[{'before':'b','after':'x'}]),'ValueError')
 test('byte-block-sequential-collision-refuses',lambda:apply_byte_edits(b'ab',[{'before':'a','after':'b'},{'before':'b','after':'z'}]),'ValueError')
 test('nonzero-should-is-not-consent',lambda:zero_findings({'verdict':'CONSENT','mustFix':0,'shouldFix':1}),False)
 test('named-should-is-not-consent',lambda:zero_findings({'verdict':'NO-OBJECTION','mustFindings':[],'should':[{'id':'S1'}]}),False)
 test('boolean-zero-not-numeric-zero',lambda:zero_findings({'mustFix':False,'shouldFix':0,'findings':[]},True),False)
 test('missing-whole-counts-refuse',lambda:zero_findings({'findings':[]},True),False)
 rows=[{'row':rid,'reviewerGradesRequired':{g:{'status':'EXTERNAL-WHOLE-REVIEW'} for g in GRADES},'MF6':{'before':'old '+rid,'after':'new '+rid}} for rid in sorted(TARGET)]
 good=lambda:{'verdict':'ACCEPT','mustFix':0,'shouldFix':0,'findings':[]}
 register={'sourceSha256':'a'*64,'proposedSha256':'b'*64}
 documents={'documentationImage':{'proposalSha256':'d'*64,'files':[{'path':'docs/synthetic-doc.md','beforeSha256':'e'*64,'afterSha256':'f'*64}]},'handoffImage':{'path':'docs/synthetic-handoff.md','sha256':'1'*64}}
 proposal={'path':'docs/synthetic-D369.md','pin':'9'*64,'selector':''}
 scope_source={'path':'docs/synthetic-scope.md','pin':'8'*64,'selector':''}
 grade={'status':'EXTERNAL-WHOLE-REVIEW'}
 synthetic_app={'condition5Authorization':False,'registerMutation':False,'documentationApplication':{'applied':False},'evidenceTargets':{'TEST':{}},'enactmentPlan':{'status':PROPOSED_ENACTMENT,'declarationKind':'PROPOSAL-NOT-LIVE-ADOPTION-STATE','alreadyEnacted':False,'requiresWholeReview':True,'requiresZeroFindings':True,'recordingOrder':ENACTMENT_ORDER,'implementationAuthorization':False,'proposal':proposal},'ownerActsRequired':{id:{'status':PROPOSED_ENACTMENT,'enacted':False,'reviewerGradeRequired':grade,'enactOnlyAfter':'WHOLE-REVIEW-ACCEPT-0-0','proposal':proposal,'requiredAct':'Synthetic proposed '+id,'rows':['DR-101'],'evidenceTargets':['TEST']} for id in OWNER_ACT_IDS},'scopeDispositions':{id:{'adoption':PROPOSED_ENACTMENT,'enacted':False,'reviewerGradeRequired':grade,'enactOnlyAfter':'WHOLE-REVIEW-ACCEPT-0-0','enactmentProposal':proposal,'source':scope_source,'exactObligationBranch':'synthetic branch','governingExcludedScopeAndPositiveWork':'synthetic excluded scope','reentryTriggerAndOwner':'synthetic named reentry','activeEvidenceRequirement':'synthetic retained negatives'} for id in SCOPE_IDS}}
 plan_checks,enactment=validate_enactment_plan(synthetic_app)
 test('unenacted-proposal-with-external-grades-positive',lambda:all(ok for _,ok in plan_checks))
 for id,mutate in [('owner-act-missing-proposal-refuses',lambda x:x['ownerActsRequired']['ACT-FC-C1'].pop('proposal')),('owner-act-missing-external-grade-refuses',lambda x:x['ownerActsRequired']['ACT-FC-C1'].pop('reviewerGradeRequired')),('owner-act-self-grades-acceptance-refuses',lambda x:x['ownerActsRequired']['ACT-FC-C1']['reviewerGradeRequired'].update(verdict='ACCEPT')),('owner-act-falsely-enacted-refuses',lambda x:x['ownerActsRequired']['ACT-FC-C1'].update(enacted=True)),('scope-falsely-adopted-refuses',lambda x:x['scopeDispositions']['SD-1'].update(enacted=True)),('scope-missing-application-grade-refuses',lambda x:x['scopeDispositions']['SD-1'].pop('reviewerGradeRequired')),('enact-before-review-order-refuses',lambda x:x['enactmentPlan'].update(recordingOrder=list(reversed(ENACTMENT_ORDER)))),('proposal-claims-live-recording-refuses',lambda x:x['enactmentPlan'].update(alreadyEnacted=True)),('publication-already-applied-claim-refuses',lambda x:x['documentationApplication'].update(applied=True)),('missing-owner-act-refuses',lambda x:x['ownerActsRequired'].pop('ACT-G13-ROSTER')),('different-owner-proposal-hash-refuses',lambda x:x['ownerActsRequired']['ACT-FC-C1']['proposal'].update(pin='7'*64))]:
  def probe(m=mutate):
   clone=json.loads(json.dumps(synthetic_app));m(clone);return all(ok for _,ok in validate_enactment_plan(clone)[0])
  test(id,probe,False)
 review={'documentClass':'independent-whole-application-review','reviewer':{'id':'SYNTHETIC-SELFTEST-NOT-A-REAL-REVIEW','authoredNoneOfSubjectBytes':True},'subject':{'path':'docs/synthetic-app.json','sha256':'c'*64},**good(),'registerImage':register,**documents,'enactmentImage':enactment,'ownerActGrades':{id:good() for id in OWNER_ACT_IDS},'scopeApplicationGrades':{id:good() for id in SCOPE_IDS},'rows':[{'row':r['row'],'grades':{g:good() for g in GRADES},'MF6':{**good(),'beforeSha256':sha(r['MF6']['before'].encode()),'afterSha256':sha(r['MF6']['after'].encode())}} for r in rows]}
 def reviewed(v):return all(ok for _,ok in validate_whole_review(v,'c'*64,'docs/synthetic-app.json',rows,register,documents,enactment))
 test('synthetic-whole-binding-positive',lambda:reviewed(review))
 for id,mutate in [('wrong-app-hash',lambda r:r['subject'].update(sha256='d'*64)),('missing-row',lambda r:r['rows'].pop()),('duplicate-row',lambda r:r['rows'].append(r['rows'][0])),('missing-gate2',lambda r:r['rows'][0]['grades'].pop('D056_gate2')),('nonzero-row-finding',lambda r:r['rows'][0]['grades']['SATISFIED'].update(shouldFix=1)),('wrong-MF6-image',lambda r:r['rows'][0]['MF6'].update(afterSha256='e'*64)),('wrong-register-hash',lambda r:r['registerImage'].update(proposedSha256='e'*64)),('author-review-refuses',lambda r:r['reviewer'].update(authoredNoneOfSubjectBytes=False))]:
  def probe(m=mutate):
   clone=json.loads(json.dumps(review));m(clone);return reviewed(clone)
  test(id,probe,False)
 for id,mutate in [('missing-doc-publication-binding',lambda r:r.pop('documentationImage')),('wrong-document-postimage',lambda r:r['documentationImage']['files'][0].update(afterSha256='0'*64)),('wrong-handoff-image',lambda r:r['handoffImage'].update(sha256='0'*64)),('whole-missing-owner-act-grade',lambda r:r['ownerActGrades'].pop('ACT-FC-C1')),('whole-missing-scope-grade',lambda r:r['scopeApplicationGrades'].pop('SD-1')),('whole-owner-act-nonzero-finding',lambda r:r['ownerActGrades']['ACT-FC-C1'].update(mustFix=1)),('whole-wrong-enactment-image',lambda r:r['enactmentImage']['proposal'].update(sha256='0'*64))]:
  def probe(m=mutate):
   clone=json.loads(json.dumps(review));m(clone);return reviewed(clone)
  test(id,probe,False)
 with tempfile.TemporaryDirectory(prefix='architecture-structural-test-') as td:
  root=Path(td);p=root/'pin.json';p.write_text('{"items":[1]}');audit=Audit(root)
  test('actual-file-pin-positive',lambda:audit.pin({'path':str(p),'pin':sha(p.read_bytes())},'positive')==p.resolve())
  test('actual-file-pin-mutation-refuses',lambda:audit.pin({'path':str(p),'pin':'0'*64},'negative') is None)
  test('pending-pin-never-accepts-observed-hash',lambda:audit.pin({'path':str(p),'pin':'PENDING','observedSha256':sha(p.read_bytes())},'pending') is None)
  before=len(audit.checks);audit.pin_records({'probes':[{'input':{'tree':{'path':'bin/entry','sha256':'a'*64}}}]},root,'fixture')
  test('fixture-archive-path-is-not-repository-pin',lambda:len(audit.checks)==before)
 with tempfile.TemporaryDirectory(prefix='architecture-snapshot-test-') as td:
  root=Path(td).resolve();logical='docs/source.md';source=root/logical;source.parent.mkdir();old=b'# Original\n| DR-101 | old qualification |\n## End\n';source.write_bytes(old)
  archived=root/'archive.md';archived.write_bytes(old);source.write_text('# Adopted\n')
  def archive_pin(expected=sha(old)):
   a=Audit(root);a.archive(logical,archived)
   a.pin({'path':logical,'pin':expected,'selector':{'exactLine':'| DR-101 | old qualification |'}},'application-pin/rows/0/qualificationRemainderProposed/0/source')
   return all(c['status']=='PASS' for c in a.checks)
  test('global-qualification-pin-and-selector-use-archive',archive_pin)
  test('archived-input-still-requires-original-pin',lambda:archive_pin('0'*64),False)
  a=Audit(root);a.archive(logical,archived);section=b'# Original\n| DR-101 | old qualification |\n'
  test('section-hash-from-archived-bytes',lambda:a.pin({'path':logical,'pin':sha(section),'startHeading':'# Original','endHeading':'## End'},'section')==source)
  archived.write_bytes(old+b'corrupt')
  test('archive-mutation-after-admission-refuses',lambda:a.pin({'path':logical,'pin':sha(section),'startHeading':'# Original','endHeading':'## End'},'mutated') is None)
  archived.write_bytes(old)
  jp=root/'docs/input.json';jp.write_text('{"original":{"value":7}}');ja=root/'input-archive.json';ja.write_bytes(jp.read_bytes());jp.write_text('{"adopted":true}')
  a=Audit(root);a.archive('docs/input.json',ja)
  test('JSON-pointer-and-parser-use-archived-object',lambda:a.pin({'path':'docs/input.json','pin':sha(ja.read_bytes()),'selector':'/original/value'},'json')==jp and a.json(jp)['original']['value']==7)
  entry={'path':logical,'sha256':sha(old),'snapshotPath':'archive.md'};manifest=root/'snapshot.json'
  def manifest_probe(data):
   manifest.write_text(json.dumps(data));a=Audit(root);a.load_snapshot(manifest);return a.read(source)==old
  test('snapshot-relative-location-positive',lambda:manifest_probe({'schemaVersion':1,'files':[entry]}))
  test('snapshot-duplicate-logical-path-refuses',lambda:manifest_probe({'schemaVersion':1,'files':[entry,entry]}),'ValueError')
  test('snapshot-wrong-whole-hash-refuses',lambda:manifest_probe({'schemaVersion':1,'files':[dict(entry,sha256='0'*64)]}),'ValueError')
  test('snapshot-logical-parent-traversal-refuses',lambda:manifest_probe({'schemaVersion':1,'files':[dict(entry,path='docs/../source.md')]}),'ValueError')
  test('snapshot-boolean-version-refuses',lambda:manifest_probe({'schemaVersion':True,'files':[entry]}),'ValueError')
  test('snapshot-unknown-field-refuses',lambda:manifest_probe({'schemaVersion':1,'files':[dict(entry,ignoreHash=True)]}),'ValueError')
  a=Audit(root);a.archive(logical,archived);a.pin({'path':logical,'pin':sha(old)},'capture-source');cap=root/'captured';captured=a.capture_snapshot(cap)
  b=Audit(root);b.load_snapshot(Path(captured['path']))
  test('captured-snapshot-replays-exact-old-bytes',lambda:b.pin({'path':logical,'pin':sha(old)},'captured')==source and b.read(source)==old and captured['files']==1)
  test('capture-refuses-existing-directory',lambda:a.capture_snapshot(cap),'FileExistsError')
  test('conflicting-register-and-snapshot-overrides-refuse',lambda:b.archive(logical,source),'ValueError')
  # Exercise the actual twelve-file publication routine against disk. Archived
  # preimages must never replace live after-image or drift observations here.
  edits=[]
  for name in sorted(DOCUMENT_PATHS):
   target=root/name;target.parent.mkdir(parents=True,exist_ok=True);before=('old '+name+'\n').encode();after=('new '+name+'\n').encode();target.write_bytes(before)
   edits.append({'path':name,'before':before.decode(),'after':after.decode(),'beforeSha256':sha(before),'afterSha256':sha(after)})
  proposal=root/'docs/proposal.json';proposal.write_text(json.dumps({'edits':edits}));handoff=root/'docs/handoff.md';handoff.write_text('synthetic handoff');norm=root/'docs/review.json';norm.write_text('{}')
  ref=lambda p:{'path':str(p),'pin':sha(p.read_bytes())}
  app={'documentationApplication':{'docEditsProposal':ref(proposal),'handoff':ref(handoff),'normativeReview':ref(norm),'expectedDocumentPaths':sorted(DOCUMENT_PATHS),'reviewerGradeRequired':{'status':'EXTERNAL-WHOLE-REVIEW'}}}
  def publication():
   a=Audit(root);a.archive(edits[0]['path'],docarchive);result=check_document_edits(a,app)
   return a,result
  docarchive=root/'docarchive';docarchive.write_text(edits[0]['before'])
  a,images=publication()
  test('twelve-document-before-images-pass',lambda:all(c['status']=='PASS' for c in a.checks))
  for e in edits:(root/e['path']).write_text(e['after'])
  a,postimages=publication()
  test('twelve-published-after-images-pass-with-historical-archive',lambda:all(c['status']=='PASS' for c in a.checks) and images==postimages and sum(c.get('detail',{}).get('phase')=='AFTER' for c in a.checks if isinstance(c.get('detail'),dict))==12)
  (root/edits[0]['path']).write_text('unrelated drift')
  a,_=publication()
  test('document-live-drift-not-masked-by-archive',lambda:any(c['status']=='FAIL' and c['id'].endswith('/current-custody') for c in a.checks))
 supplement_path=HERE/'architecture-incorporated-dependency-supplement.draft.json'
 if supplement_path.exists():
  supp=strict(supplement_path.read_bytes());app=strict((HERE/'architecture-application.draft.json').read_bytes())
  def valid_supp(v):return all(ok for _,ok in validate_supplement(v,app,lambda name:strict((ROOT/name).read_bytes())))
  test('supplement-exact-source-inventory-positive-not-review',lambda:valid_supp(supp))
  for id,mutate in [('supplement-missing-DR102-definition',lambda x:x['additionalIdentityDependencies'].pop()),('supplement-duplicate-FC-condition',lambda x:x['namedOpenConditions'].append(x['namedOpenConditions'][0])),('supplement-wrong-canonical-pointer',lambda x:x['namedOpenConditions'][-1]['source'].update(selector='/undeterminedRegister/0')),('supplement-false-total-count',lambda x:x['counts'].update(totalIdentityDependencies=86)),('supplement-absent-target',lambda x:x['inheritedClaimRides'][0]['proposedJoins'][0].update(targetRef='NO-SUCH-TARGET')),('supplement-omitted-lineage-member',lambda x:x['lineagePreservation'][0]['members'].pop()),('supplement-wrong-valid-lineage-pointer',lambda x:x['lineagePreservation'][0]['members'][0]['before'].update(selector='/identityDependencies/dependencies/1')),('supplement-fabricated-scope-without-authority',lambda x:x['inheritedClaimRides'][0]['scopeApplication'].update(governingSources=[]))]:
   def probe(m=mutate):
    clone=json.loads(json.dumps(supp));m(clone);return valid_supp(clone)
   test(id,probe,False)
 out={'evidenceClass':'SYNTHETIC CHECKER SELFTEST; NO REAL APPLICATION OR REVIEW ACCEPTANCE','passed':sum(v['pass'] for v in results),'total':len(results),'cases':results}
 report.write_text(json.dumps(out,indent=2)+'\n');print(f"SELFTEST {out['passed']}/{out['total']}: {report}");return 0 if out['passed']==out['total'] else 1

def main():
 p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 p.add_argument('--application',type=Path,default=HERE/'architecture-application.draft.json')
 p.add_argument('--report',type=Path,default=HERE/'architecture-application-structural-report.v1.json')
 p.add_argument('--proposed-register',type=Path,default=HERE/'readiness-register.proposed.v1.md')
 p.add_argument('--register-source',type=Path,help='Register-only historical-byte override used by ALL pins/selectors, not just register edits; exact original SHA remains required.')
 p.add_argument('--snapshot-manifest',type=Path,help='Explicit historical input map with whole-file hashes; all pinned reads use these bytes while live publication custody remains checked.')
 p.add_argument('--capture-snapshot',type=Path,help='Create a NEW directory containing all successfully pinned input bytes and snapshot-manifest.json; may capture a pending candidate without accepting it.')
 p.add_argument('--whole-review',type=Path)
 p.add_argument('--mode',choices=['candidate','final'],default='candidate')
 p.add_argument('--selftest',action='store_true');args=p.parse_args()
 if args.selftest:return selftest(args.report)
 audit=Audit();app_path=args.application.resolve();whole=None;reg=None;documents=None;snapshot=None;supplement=None;enactment=None
 try:
  if args.snapshot_manifest:audit.load_snapshot(args.snapshot_manifest)
  if args.register_source:audit.archive('docs/architecture/current/08-decision-and-readiness-register.md',args.register_source)
  app=strict(app_path.read_bytes());check_structure(audit,app);check_units(audit,app);supplement=check_supplement(audit,app);enactment=check_enactment(audit,app)
  reg=check_register(audit,app,args.proposed_register.resolve());documents=check_document_edits(audit,app);whole=check_whole(audit,app,app_path,args.whole_review,reg,documents,enactment)
 except (OSError,ValueError,TypeError,KeyError,IndexError,AttributeError) as e:audit.add('application/malformed',False,type(e).__name__+': '+str(e))
 if args.capture_snapshot:
  try:snapshot=audit.capture_snapshot(args.capture_snapshot)
  except (OSError,ValueError) as e:audit.add('snapshot/capture',False,str(e))
 counts=collections.Counter(c['status'] for c in audit.checks)
 passed=not counts['FAIL'] and not counts['PENDING']
 report={'status':'STRUCTURAL-CHECKS-PASS' if passed else 'STRUCTURAL-CHECKS-INCOMPLETE','mode':args.mode,'application':{'path':str(app_path.relative_to(ROOT)) if app_path.is_relative_to(ROOT) else str(app_path),'sha256':sha(app_path.read_bytes()) if app_path.exists() else None},'checkerSha256':sha(Path(__file__).read_bytes()),'wholeReview':whole,'enactmentImage':enactment,'incorporatedDependencySupplement':supplement,'historicalReplay':{'snapshotManifest':str(args.snapshot_manifest) if args.snapshot_manifest else None,'registerSource':str(args.register_source) if args.register_source else None,'archivedLogicalPaths':sorted(str(p.relative_to(audit.root)) for p in audit.archives),'capturedSnapshot':snapshot,'livePublicationCustodyChecked':True},'documentPublicationImages':documents,'counts':dict(counts),'checks':audit.checks,'registerWritten':False,'documentsWritten':False,'semanticReviewPerformed':False,'readinessGrade':None,'qualificationClaim':False,'meaning':'A zero exit proves these structural checks and presence of the pinned reviewer attestations only; it does not independently establish semantic correctness, reviewer honesty, live adoption, implementation authorization or product qualification.'}
 args.report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(f"{report['status']}: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['PENDING']} PENDING; {args.report}")
 return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
