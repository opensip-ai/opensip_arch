from pathlib import Path
import importlib.util,json,hashlib,copy
F=Path('/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections/foundation')
s=importlib.util.spec_from_file_location('K',F/'check-atoms.v1.py');K=importlib.util.module_from_spec(s);s.loader.exec_module(K)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pins={n:sha(F/n) for n in ['atom_model.v1.py','check-atoms.v1.py','incoming-search.schema.v1.json']}
n='ts-symbol:src/a.ts#f';atom={'op':'none','relation':'references','minResolution':'resolved-binding','endpoint':'target','filters':[]};subj={'universe':K.U1,'kind':'symbol','nativeSubjectId':n};sid,sc=K.scope('references','resolved-binding',K.U1,K.U1,[n],sid='1');invs=[K.inv_symbol()]
base=K.base_inputs(enumerationPlan=K.plan_one(cap='references'),inventories=invs,scopes={sid:sc})
att=K.incoming_att('references','resolved-binding',K.U1,K.U1,[sid],invs,completeSearch=False,examinedExhaustive=False,coverage='unknown',resolutionCompleteness=K.rc_for('resolved-binding',state='partial',cov='unknown'))
rows=[]
for name in ['no-scope-no-attestation','scope-no-coverage-no-attestation','scope-no-coverage-nonproving-attestation','scope-other-target-coverage','invalid-attestation']:
 i=copy.deepcopy(base)
 if name=='no-scope-no-attestation':i['scopes']={}
 if name in ['scope-no-coverage-nonproving-attestation','invalid-attestation']:i['incomingSearchAttestations']=[copy.deepcopy(att)]
 if name=='invalid-attestation':i['incomingSearchAttestations'][0]['completeSearch']=True
 if name=='scope-other-target-coverage':
  i['scopes']={};K.install_pair(i,*K.paired('references','resolved-binding',K.U1,K.U2,[n],tag='1'))
 try:
  r=K.AM.evaluate_atom(atom,subj,i);out={'case':name,'atomAdmission':'ADMIT','value':r['value'],'causes':r['causes']}
 except K.AM.AtomAdmissionError as e:out={'case':name,'atomAdmission':'REFUSE','reason':e.key}
 rows.append(out)
assert 'source-target-search-unattested' in {c['code'] for c in rows[0]['causes']}
assert 'scope-without-coverage' in {c['code'] for c in rows[1]['causes']}
assert rows[2]['atomAdmission']=='ADMIT' and 'scope-without-coverage' in {c['code'] for c in rows[2]['causes']} and 'source-target-search-unattested' not in {c['code'] for c in rows[2]['causes']}
assert 'source-target-search-unattested' in {c['code'] for c in rows[3]['causes']}
assert rows[4]['atomAdmission']=='REFUSE' and rows[4]['reason']=='INCOMING_SEARCH_SCHEMA'
assert pins=={n:sha(F/n) for n in pins}
print(json.dumps({'standing':'Synthetic atom API reference inputs. Owning attestation schema/joins and atom evaluation exercised; NOT full native/retained Run admission or product qualification.','sourceHashes':pins,'cases':rows,'passed':True},indent=2))
