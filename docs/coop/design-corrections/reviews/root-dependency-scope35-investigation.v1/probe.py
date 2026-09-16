from pathlib import Path
import json,hashlib,importlib.util,copy
S=Path('/tmp/opensip-design-corrections/candidate-subject.v35');O=Path(__file__).parent;P=S/'docs/coop/design-corrections/foundation';sp=importlib.util.spec_from_file_location('root_dep_check',P/'check-atoms.v1.py');K=importlib.util.module_from_spec(sp);sp.loader.exec_module(K);A=K.AM
atom={'op':'all-covered','relation':'reachability','minResolution':'from-resolved-calls','filters':[]};sub=K.F_SUBJ
base=K.base_inputs(enumerationPlan=K.plan_one(cap='reachability'));K.install_pair(base,*K.paired('reachability','from-resolved-calls',K.U1,K.U1,[K.F_SYM],tag='1'));K.install_pair(base,*K.paired('calls','resolved-callee',K.U1,K.U1,[K.F_SYM],tag='2'));sid=K.scope2('2')
def ev(inp):
 try:
  x=A.evaluate_atom(atom,sub,inp);return {'admission':'ADMIT',**{k:x[k] for k in ['value','causes','coverageIds','scopeIds']}}
 except A.AtomAdmissionError as e:return {'admission':'REFUSE','key':e.key,'detail':str(e)}
rows=[]
for field,other in [('sourceUniverse',K.U2),('relation','references'),('resolution','resolved-binding')]:
 for mode in ['absent','null','different']:
  i=copy.deepcopy(base)
  if mode=='absent':i['scopes'][sid].pop(field)
  else:i['scopes'][sid][field]=None if mode=='null' else other
  try:A._derive_scope_commitment(i['scopes'][sid]);native={'admission':'ADMIT'}
  except A.AtomAdmissionError as e:native={'admission':'REFUSE','key':e.key}
  rows.append({'field':field,'mode':mode,'derivedCarrierAdmission':native,'atomResult':ev(i),'scopedInputs':i['scopes'][sid]})
deleted=copy.deepcopy(base);deleted['scopes'].pop(sid);deleted['coverageScopes'].pop(K.cov2('2'))
result={'standing':'Root independent reproduction on synthetic atom inputs and direct native scope commitment only. No closed enumeration or retained Run admission, no product reachability/qualification claim. No consumer data or source mutation.','sourceManifestSha256':'eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85','sourceHashes':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['atom_model.v1.py','check-atoms.v1.py']},'baseline':ev(base),'deletedScopeControl':ev(deleted),'cases':rows}
(O/'probe.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'baseline':result['baseline']['value'],'deleted':result['deletedScopeControl']['value'],'cases':[{k:x[k] for k in ['field','mode','derivedCarrierAdmission','atomResult']} for x in rows]},indent=2))
