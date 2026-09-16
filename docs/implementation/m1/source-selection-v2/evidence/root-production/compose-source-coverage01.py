from pathlib import Path
import ast,copy,hashlib,json,types,shutil
A=Path('/Users/sb/code/opensip-ai/opensip_arch');D=A/'docs/implementation/m1/source-selection-v2';B=Path('/tmp/opensip-implementation')
def read(p):return json.loads(p.read_bytes())
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p):b=p.read_bytes();return {'path':str(p.relative_to(A)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
checker=A/'docs/operations/check_implementation_planning.py';target=D/'reference-tools/check_implementation_planning.py';shutil.copy2(checker,target);P=types.ModuleType('planning');P.__file__=str(target);exec(compile(target.read_bytes(),str(target),'exec'),P.__dict__)
overlay=read(D/'owners/report/implementation-coverage-successor.v1.json');base=A/overlay['base']['path'];assert pin(base)['sha256']==overlay['base']['sha256'];before=read(base)
# Use only the original pure overlay function; no author module top-level runs.
owner=B/'m1-report-projection-subject-08/build_owner.py';text=owner.read_text();node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='apply_overlay');fn=ast.get_source_segment(text,node)
(D/'reference-tools/coverage_overlay.py').write_text('import copy\n\n'+fn+'\n');namespace={'copy':copy};exec(compile(ast.Module(body=[node],type_ignores=[]),str(owner)+'#apply_overlay','exec'),namespace);coverage=namespace['apply_overlay'](before,overlay)
sources={}
for key,row in before['sources'].items():
 p=A/row['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];sources[key]=read(p) if p.suffix=='.json' else p.read_text()
raw=sources['workflows-and-surfaces'];lines=raw.splitlines();edits=[]
for r in read(D/'owners/report/passage-overrides.v1.json')['overrides']:
 if r['path']==before['sources']['workflows-and-surfaces']['path']:
  assert lines[r['line']-1]==r['before'];edits.append((r['line'],r['line'],r['after']))
for r in read(D/'owners/interruption/passage-overrides.json')['overrides']:
 first,last=r['selector']['startLine'],r['selector']['endLine'];assert '\n'.join(lines[first-1:last])==r['before'];edits.append((first,last,r['after'].replace('selected\nenvelope6 interruption form','selected\nenvelope7 interruption form')))
for first,last,after in sorted(edits,reverse=True):lines[first-1:last]=after.splitlines()
effective=D/'reference/effective-workflows-and-surfaces.md';effective.write_text('\n'.join(lines)+'\n')
selected={'commands':D/'reference/composed-owners/command-inventory.proposed.json','query':D/'schemas/sources/graph-query.v4.schema.json','workflows-and-surfaces':effective}
for key,p in selected.items():
 sources[key]=read(p) if p.suffix=='.json' else p.read_text();coverage['sources'][key]=pin(p)
expected=P.expected_groups(sources);changed=[]
for group,rows in coverage['groups'].items():
 assert {r['id'] for r in rows}==set(expected[group]),group
 for row in rows:
  key,selector,value=expected[group][row['id']];ref={'key':key,'selector':selector,'valueSha256':P.digest(value)}
  if row['source']!=ref:changed.append(group+':'+row['id'])
  row['source']=ref
  if group=='commands':
   for f in ['requestClass','authorizationClass','formats','parityFields']:row[f]=copy.deepcopy(value[f])
  row['verification']['method']=row['verification']['method'].replace('over envelope6','over selected envelope7').replace('no truncation, empty account or invented 130/4 precedence until the capacity owner decides.','use the selected complete-output-or-operational-failure policy: successful required output preserves the settled aggregate; serialization/write/flush failure yields OUTPUT.SERIALIZATION_FAILED exit4 while prior commits and aggregate remain preserved. No truncation or invented atomic stdout guarantee.')
for issue in coverage['reviewIssues']:
 if issue['id']=='RP-OBL-L02':issue['standing']='Root policy selected on actual combined reference review; exact source adoption and product bounded encoding/delivery still pending.'
source_issue={'id':'RP-OBL-R11-LOCATION','kind':'report-source-custody-and-delivery-duty','standing':'open before M4 qualification; no source-location carrier or delivered feature inferred from endpoint IDs','finding':'Current graph endpoints identify universe/kind/nativeSubjectId (package endpoints additionally carry packageManifestPath). These IDs alone do not carry symbol source spans. R11 still requires exact retained occurrence location, copyable paths and relationship/cross-view navigation. Add an owned bounded retained-source projection or select an already-owned exact embedded carrier before claiming R11 delivery. Never derive a location from a body hash or current checkout.','affects':['reportFeatures:R11']}
coverage['reviewIssues'].append(source_issue);r11=next(r for r in coverage['groups']['reportFeatures'] if r['id']=='R11');r11['reviewIssues']=sorted(set(r11['reviewIssues'])|{source_issue['id']});r11['verification']['method']+=' Verify retained occurrence source locations and copyable paths under RP-OBL-R11-LOCATION; an unavailable message does not satisfy R11.'
coverage['standing']='Proposed combined source-selection coverage over acceptedv3 and report08 overlay; current inventory6/query4/workflow clauses bound. All product verification remains not-executed; no source or milestone acceptance.'
inventory=read(A/'docs/implementation/m1/repository-file-inventory.v4.json');P.validate_coverage(coverage,sources,inventory)
assert all(r['verification']['standing']=='not-executed' for rows in coverage['groups'].values() for r in rows)
assert coverage['moduleFirstMilestone']==before['moduleFirstMilestone'] and coverage['moduleFirstMilestone']['crates/reporting/src/assets.rs']=='M1'
save(D/'implementation-coverage.v4.json',coverage)
save(D/'coverage-composition.json',{'standing':'Root source-planning composition, independent review/source adoption pending','base':pin(base),'overlay':pin(D/'owners/report/implementation-coverage-successor.v1.json'),'ownedValidator':pin(target),'overlayFunctionSha256':hashlib.sha256(fn.encode()).hexdigest(),'currentSources':{k:pin(p) for k,p in selected.items()},'rows':sum(len(v) for v in coverage['groups'].values()),'sourceMappingsChanged':changed,'scopedTextEdits':len(edits),'allVerificationNotExecuted':True,'modulePrerequisitesUnchanged':True,'newR11Duty':source_issue['id'],'productModified':False})
s=read(D/'scoped-owner-succession.json');s['notClosed'][0]='Current inventory6/query4 coverage composition is root-checked but requires independent source review and final integration';save(D/'scoped-owner-succession.json',s)
print(json.dumps({'passed':True,'rows':sum(len(v) for v in coverage['groups'].values()),'changedSourceMappings':len(changed),'scopedTextEdits':len(edits),'verificationNotExecuted':True}))
