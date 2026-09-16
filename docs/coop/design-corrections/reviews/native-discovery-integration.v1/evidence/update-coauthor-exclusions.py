from pathlib import Path
import hashlib,json,importlib.util,sys,tempfile
A=Path('/tmp/opensip-design-corrections/application-successor-root.v2');O=Path(__file__).parent/'application-coauthor-exclusions';O.mkdir()
names=['coverage_contract.py','bind-review-receipts.v1.py','assemble-records.successor.v1.py','review_envelope.py'];rows=[]
sessions=('eaa8276c-dc65-4d26-8ca2-703b345698f9','36a89be8-3442-4edb-90d8-a6fd959a437c','0aa529b3-0da1-44b1-b2b9-dbcd9f1bd206','329a5132-ee66-4303-97a9-b9ebd1b7ffc0')
for n in names:
 p=A/n;raw=p.read_bytes();(O/('before-'+n)).write_bytes(raw);s=raw.decode()
 if n=='coverage_contract.py':
  s+='\n# Actual Claude origins that authored successor deltas in the September return review.\nKNOWN_CLAUDE_COAUTHOR_SESSIONS = '+repr(sessions)+'\nKNOWN_COAUTHOR_SESSIONS = KNOWN_GROK_COAUTHOR_SESSIONS + KNOWN_CLAUDE_COAUTHOR_SESSIONS\n'
 else:s=s.replace('KNOWN_GROK_COAUTHOR_SESSIONS','KNOWN_COAUTHOR_SESSIONS').replace('known Grok coauthor session','known coauthor session')
 p.write_text(s);(O/n).write_bytes(p.read_bytes());rows.append({'path':n,'beforeSha256':hashlib.sha256(raw).hexdigest(),'afterSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
sys.path.insert(0,str(A));spec=importlib.util.spec_from_file_location('receipt_binder',A/'bind-review-receipts.v1.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
work=O/'synthetic-controls';work.mkdir();results=[];subject='a'*64
review={'verdict':'ACCEPT','subjectManifestSha256':subject,'newMustIssues':[],'newShouldIssues':[]}
(work/'review.json').write_text(json.dumps(review))
for sid in (*sessions,'synthetic-fresh-shape-control'):
 (work/'public.json').write_text(json.dumps({'is_error':False,'session_id':sid,'result':'SYNTHETIC shape control, never an actual review'}))
 spec={'reviewPath':'review.json','reviewSha256':hashlib.sha256((work/'review.json').read_bytes()).hexdigest(),'requiredVerdict':'ACCEPT','publicResponsePath':'public.json','publicResponseSha256':hashlib.sha256((work/'public.json').read_bytes()).hexdigest(),'role':'independent-design'}
 try:m.bind_one(work,spec,'claude',subject,'synthetic');refused=False
 except AssertionError as e:refused=True;assert 'known coauthor' in str(e),str(e)
 assert refused==(sid in sessions);results.append({'session':sid,'refused':refused})
 if sid in sessions:
  try:m.E.refuse_coauthor_process({'command':['claude','--resume',sid]},'independent-design');raise RuntimeError('resume admitted')
  except AssertionError:pass
(O/'assessment.json').write_text(json.dumps({'standing':'Preparation guard correction, not actual review receipts or acceptance; known coauthor sessions cannot be bound as independent','files':rows,'controls':results},indent=2)+'\n');print('PASS: four actual author origins refused by envelope binding and resume guard; synthetic fresh shape allowed')
