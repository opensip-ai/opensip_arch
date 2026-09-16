from pathlib import Path
import json,importlib.util,sys
sys.path.insert(0,str(Path(__file__).parent));import lineage_law as L
b=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/security')
spec=importlib.util.spec_from_file_location('owner',b/'security_lifecycle_model_v1.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
f=json.loads((b/'transition-journal-cases.v1.json').read_text())['records'];i=f['intentStoreMigrate'];assert M.admit_transition_intent(i)==[]
reg=['ns-a','ns-b','ns-c'];j=M.transition_journal_record(i,reg);d=M.transition_intent_digest(i)
ctx={'namespaceRegistry':reg,'fenceHeld':True,'leasesReacquired':j['leaseSet'],'storeFootprint':None}
own=M.recover_transition_journal(dict(j,state='LEASED'),ctx)
a=L.node('a'*32,3,1,None,None)
rec=L.recover_nodes(own,i,d,[a],L.node_triple(a),{'predecessorStoreRoot':'a'*32})
# Idempotent recovery still must validate the predecessor chain, not just key equality.
pred=L.node('a'*32,3,1,L.triple('f'*32,2,1),'2'*64)
target=L.node('e'*32,4,2,L.node_triple(pred),d)
own2=M.recover_transition_journal(dict(j,state='COMMITTED'),ctx)
rec2=L.recover_nodes(own2,i,d,[pred,target],L.node_triple(pred),{'predecessorStoreRoot':'a'*32,'selectedStoreRoot':'e'*32})
print(json.dumps({'standing':'Root design-reference controls using exact copied v4 law and actual owner functions. LEASED precedes store materialization; no selected marker yet is lawful. No native lifecycle/crash claim.','earlyAbort':{'owner':own,'companion':rec},'brokenExistingAncestry':{'companion':rec2,'invariantProblems':L.invariants(rec2['nodes'])}},indent=2))
