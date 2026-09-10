from pathlib import Path
import importlib.util,json
b=Path('/tmp/opensip-design-corrections');src=b/'candidate-subject.v24/docs/coop/design-corrections/workflows/query_projection_model.v3.py';s=importlib.util.spec_from_file_location('M',src);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
q=json.loads((b/'consumer-b.v11/output/queries/graph-query.json').read_text());rows=[]
for name,value in q.items():
 if not isinstance(value,dict) or not value.get('ok') or 'response' not in value:continue
 row={'case':name,'claimedValid':value.get('classification')}
 try:M.validate_schema(M.SCHEMA_ID+'#/$defs/GraphQueryResponseV1',value['response']);row['admission']='ADMIT'
 except Exception as e:row.update(admission='REFUSE',exceptionType=type(e).__name__,reason=str(e).split('\n')[0],detail=str(e.__cause__)[:1800])
 rows.append(row)
r={'standing':'Exact final consumer query response shape validation via owning frozen registered schema. Not retained Run admission (all5alreadyrefused), not semantic query acceptance.','checks':rows};(b/'blind11-query-schema-root-check.v2.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
