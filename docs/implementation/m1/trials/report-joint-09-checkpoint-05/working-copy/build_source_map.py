"""Proposed registry/source map for later generator integration; selects nothing."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
check=json.loads((HERE/'source-check-result.json').read_bytes());assert check['passed']
composition=json.loads((HERE/'composition-result.json').read_bytes())
current=[]
for row in composition['outputs']:
 raw=(HERE/row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
 value=json.loads(raw);current.append({'schemaId':value['$id'],**row})
models=[]
for name in ['model-generation-result.json','metadata-composition-result.json','identity-composition-result.json']:
 for row in json.loads((HERE/name).read_bytes())['outputs']:
  raw=(HERE/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
  models.append({k:row[k] for k in ['path','bytes','sha256']})
for name in ['planning-composition-result.json','output-policy-composition-result.json']:
 row=json.loads((HERE/name).read_bytes())['output'];raw=(HERE/row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];models.append(row)
entrypoints={
 'newPlan':'new_plan_admission.bind(...).admit_new_plan; selected identity3 optional row + exact parameter bytes + native/common4 route sources; retained closure unchanged',
 'fit':'workflow5_replay.replay + fit_join.admit_page/interrupted + fit_output capture/project; one source-bound query with exact completed page custody',
 'report':'report_admission.admit with document_joins, joint_placement and actual feature/catalogue projection owners',
 'projection':'parent_projection.bind includes all reserved later states; joint_placement.append consumes the remaining shared allowance',
 'requiredOutput':'required-output01 Finalizer with exact already-admitted projection and the bounded selected codec; synthetic reference callback is not a product codec',
 'history':'history02 typed query4 run.show, exact selected Run and one retained read lease; actual snapshot/store implementation remains required'}
helpers={}
for path in ['new-plan-contract.md','new_plan_admission.py','new_plan_carriers.py','identity_carriers.py','report_carriers.py','catalog_carrier.py','metadata_carriers.py','workflow5_replay.py','fit_join.py','report_admission.py','document_joins.py','parent_projection.py','joint_placement.py']:
 raw=(HERE/path).read_bytes();helpers[path]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
result={'standing':'Root proposed current registry/source map for upcoming generator work; not an approved source lock, implementation inventory or frozen review target',
 'proposedMajors':composition['proposedMajors'],'currentSchemas':current,'registryDocuments':check['schemaSources'],
 'referenceModelsAndOwnerViews':models,'currentEntryPoints':entrypoints,'integrationSources':helpers,
 'compatibility':['Common3 stays exactly pinned; current carriers explicitly reference common4','Historical Runs need not contain a recognition parameter; new compiler Plans must select one','No legacy query/envelope bytes are relabeled as current records','Identity registry extension has unchanged wire shapes; actual predecessor/new Run closure is separately tested'],
 'pending':['Actual joint owner review and root source selection','Native/D9 base composition and output-policy criterion disposition together','Update generator entry roots and Rust/TS mappings for these current schemas without dropping required historical support','Final package/file inventory and product source lock','Real producer/consumer implementations and qualification']}
(HERE/'candidate-source-map.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'currentSchemas':len(current),'registryDocuments':len(check['schemaSources']),'modelAndOwnerOutputs':len(models)}))
