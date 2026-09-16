"""Refresh evidence indexes after a successful joined verification; no approval."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;label=sys.argv[1]
def read(n):return json.loads((H/n).read_bytes())
d=read('integration-status.json');v=read('verification-'+label+'.json');assert v['complete'] and v['passed']
d['latestSourceCheck']=read('source-check-result.json')
paths={'ownerCarriers':'model-carrier-result.json','workflow':'workflow5-result.json','planning':'planning-result.json','document':'document-result.json','catalogueJoins':'catalogue-join-result.json','feature':'feature-integration-result.json','fitDocuments':'fit-document-result.json','queryCommands':'query-command-result.json','parentBases':'parent-bases-result.json','combined':'checks-'+label+'.json','sharedProjection':'shared-projection-result.json','identity':'identity-integration-result.json','metadata':'metadata-result.json','catalogueSources':'catalogue-source-result.json','outputIntegration':'output-integration-result.json','outputPolicy':'output-policy-result.json','inputIntegrity':'frozen-input-result.json','reproduction':'reproduction-'+label+'.json','candidateVerification':'verification-'+label+'.json','newPlan':'new-plan-result.json','commonSuccession':'common-succession-result.json','documentProvenance':'document-provenance-result.json'}
for key,name in paths.items():d['latestChecks'][key]=read(name)
for row in d['tasks']:
 if row['id']=='derive-whole-document-budget':row['status']='Derived proposed document27829365B, ledger19437554B, other mandatory roots2957B, shared exploration4194304B, conservative structural depth39. Separate Rust/TS codec candidate01 implements this fixed profile; source rebase, actual review and product qualification remain pending.'
 if row['id']=='final-source-and-generated-product-integration':row['status']='Current source map refreshed. Separate joint-generation candidate01 has eight outputs from40 schemas/857 explicit roots. Current provenance rebase, final source/package selection, actual review and real producer/consumer integration remain pending.'
findings=[{'id':'joint09-document-inventory-provenance','status':'proposed correction tested','finding':'Current composed report provenance still named inventory5 while the actual metadata owner selects6. The schema and fresh fixture constructors now derive the inventory6 marker; stale-marker documents refuse at schema admission. Frozen predecessor bytes remain unchanged.'},{'id':'joint09-check-runner-dependencies','status':'runner corrected; initial failed diagnoses preserved','finding':'Catalogue-source checks consumed parent-bases.fixture.json before its producer ran. Producer now precedes catalogue and output consumers. joint08/joint09 failed runs and the corrected diagnosis are preserved.'}]
for row in findings:
 d['newIntegrationFindings']=[r for r in d['newIntegrationFindings'] if r['id']!=row['id']]+[row]
(H/'integration-status.json').write_text(json.dumps(d,indent=2)+'\n')
