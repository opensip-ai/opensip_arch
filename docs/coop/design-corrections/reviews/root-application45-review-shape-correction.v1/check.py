from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,sys
B=Path('/tmp/opensip-design-corrections');H=B/'application-successor-root.v2';O=Path(__file__).parent
sys.path.insert(0,str(H));import review_envelope as E
s=importlib.util.spec_from_file_location('binder45',H/'bind-review-receipts.v1.py');binder=importlib.util.module_from_spec(s);s.loader.exec_module(binder)
j=json.loads((B/'claude-independent-design.v45/review.json').read_text());b=json.loads((B/'consumer-b.v24-source45.v1/output/blind-review.json').read_text())
checks=[]
def ck(label,fn,refuse=False):
 try:fn();observed='ADMIT'
 except (AssertionError,KeyError,TypeError):observed='REFUSE'
 assert observed==('REFUSE' if refuse else 'ADMIT'),(label,observed)
 checks.append({'case':label,'outcome':observed,'passed':True})
eids={r['id'] for r in j['evaluationResidualDispositions']}
ck('actual45-five-array-collections-exact-required-ids',lambda:binder.require_coverage(j,eids))
keyed=copy.deepcopy(j)
for key in ('arDispositions','fwDispositions','inheritedResidualDispositions','scopedReviewOwnerDispositions','evaluationResidualDispositions'):
 rows,pointers=E.disposition_rows(j,key);keyed[key]=rows
 for rid,p in pointers.items():assert j[key][int(p.split('/')[-1])]==rows[rid]
ck('equivalent-keyed-row-collections',lambda:binder.require_coverage(keyed,eids))
for label,rows in [('duplicate',[{'id':'A'},{'id':'A'}]),('missing-id',[{}]),('wrong-row',[None]),('wrong-type',None),('conflicting-key',{'A':{'id':'B'}}),('pointer-injection',[{'id':'A/B'}]),('wrong-id-type',[{'id':1}])]:
 ck(label,lambda rows=rows:E.disposition_rows({'x':rows},'x'),True)
for key in ('arDispositions','fwDispositions','inheritedResidualDispositions','scopedReviewOwnerDispositions','evaluationResidualDispositions'):
 missing=copy.deepcopy(j);missing[key].pop();ck('missing-required-'+key,lambda m=missing:binder.require_coverage(m,eids),True)
ck('actual45-blind-kit-parent',lambda: E.review_subject_digest(b))
for label,val in [('null',None),('non-object',[]),('missing-parent',{}),('subset-only',{'consumerInputManifestSha256':'a'*64}),('bad-parent',{'parentSubjectSha256':'bad'})]:
 ck('kit-'+label,lambda val=val:E.review_subject_digest({'kit':val}),True)
ck('conflicting-kit-parent',lambda:E.review_subject_digest({'subjectManifestSha256':'b'*64,'kit':{'parentSubjectSha256':'a'*64}}),True)
ck('matching-parent-aliases',lambda:E.review_subject_digest({'subjectManifestSha256':'a'*64,'kit':{'parentSubjectSha256':'a'*64}}))
for n in ['review_envelope.py','bind-review-receipts.v1.py','assemble-records.successor.v1.py']:
 compile((H/n).read_text(),str(H/n),'exec');shutil.copyfile(H/n,O/n)
report={'standing':'Root tooling compatibility tests only. Exact reviewer artifacts unchanged; no grade or acceptance inferred. Actual array pointers resolve to original rows; duplicate/missing/conflicting ids refuse. Final actual Claude application review must assess these three changed helpers.','priorAttempt':'One ad-hoc import command used nonexistent bind_review_receipts_dummy and exited1 before checks or writes; corrected by loading the real script by path.','checks':checks,'result':'PASS'}
(O/'checks.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(O,Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')/O.name)
print(json.dumps({'checks':len(checks),'result':'PASS'}))
