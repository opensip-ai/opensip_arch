import sys,json,importlib.util
from pathlib import Path
b=Path('/tmp/opensip-design-corrections')
sys.path.insert(0,str(b/'claude-planning-owner-correction.v3/scratch/controls'))
import lineage_law as L
spec=importlib.util.spec_from_file_location('owner',b/'candidate-subject.v25/docs/coop/design-corrections/security/security_lifecycle_model_v1.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
f=json.loads((b/'candidate-subject.v25/docs/coop/design-corrections/security/transition-journal-cases.v1.json').read_text())['records']
i=f['intentStoreMigrate']; assert M.admit_transition_intent(i)==[]
d=M.transition_intent_digest(i); reg=['ns-a','ns-b','ns-c'];j=M.transition_journal_record(i,reg)
a=L.node('a'*32,3,1,None,None)
old=L.node('b'*32,4,2,L.node_triple(a),'1'*64)
nodes=[a,old]; assert not L.invariants(nodes)
ctx={'namespaceRegistry':reg,'fenceHeld':True,'leasesReacquired':j['leaseSet'],'storeFootprint':None}
marks={'predecessorStoreRoot':'a'*32,'selectedStoreRoot':'e'*32}
results=[]
for state in ['LEASED','COMMITTED']:
 own=M.recover_transition_journal(dict(j,state=state),ctx)
 rec=L.recover_nodes(own,i,d,nodes,L.node_triple(a),marks)
 results.append({'state':state,'ownerResult':own,'companion':rec})
# Broken predecessor is also admitted by the forward reconstruction branch.
own=M.recover_transition_journal(dict(j,state='COMMITTED'),ctx)
missing=L.recover_nodes(own,i,d,[],L.node_triple(a),marks)
print(json.dumps({'standing':'Root design-reference counterexample; numeric generation is not globally unique; retained old branch and fresh target have different storeInstanceIds. Owner intent shape admitted; no claim of executed native lifecycle.', 'ownerIntent':i,'retainedNodes':nodes,'repeatedGeneration':results,'missingPredecessor':missing,'missingPredecessorInvariantProblems':L.invariants(missing['nodes'])},indent=2))
