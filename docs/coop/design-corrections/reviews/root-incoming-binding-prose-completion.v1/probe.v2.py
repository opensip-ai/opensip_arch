from pathlib import Path
import importlib.util,json,hashlib,copy
B=Path('/tmp/opensip-design-corrections');F=B/'incoming-binding-successor.v1/source/docs/coop/design-corrections/foundation';O=B/'root-incoming-binding-prose-completion.v1'
paths=[F/n for n in ['atom_model.v1.py','check-atoms.v1.py','incoming-search.schema.v1.json']];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p):sha(p) for p in paths}
spec=importlib.util.spec_from_file_location('root_incoming_check',F/'check-atoms.v1.py');K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K)
rows=[]
for label,refs in [('empty',[]),('borrowed-other-program-scope',[K.scope2('1')])]:
 i=K.empty_program_inputs('none',attest=True);i['incomingSearchAttestations'][0]['scopeRefs']=refs
 try:K.AM.admit_atom_inputs(i);r={'case':label,'admission':'ADMIT'}
 except K.AM.AtomAdmissionError as e:r={'case':label,'admission':'REFUSE','key':e.key,'detail':str(e)}
 rows.append(r)
report={'standing':'Root two-case atom-input admission probe over synthetic author builders. Not native complete enumeration or retained Run admission. No consumer data.','inputs':before,'sourceUnchangedDuringProbe':True,'cases':rows,'passed':rows[0].get('key')=='INCOMING_SEARCH_SCHEMA' and rows[1].get('key')=='INCOMING_SEARCH_SCOPE_MISJOIN'}
(O/'probe.v2.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

assert rows[0]['key']=='INCOMING_SEARCH_SCHEMA';assert rows[1]['key']=='INCOMING_SEARCH_SCOPE_MISJOIN';assert before=={str(p):sha(p) for p in paths}
