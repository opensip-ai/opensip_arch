"""Apply feature02's exact optional identity parameter successor."""
import copy,hashlib,json

def compose(schema_raw,model_raw,parameter_raw,patch):
    for key,raw in [('identitySchemas',schema_raw),('identityModel',model_raw)]:
        row=patch['parents'][key]
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    schema=json.loads(schema_raw);rows=schema['x-opensip-payload-registry']['classes']['parameter']['rows']
    assert len(patch['ops'])==1
    op=patch['ops'][0];key='foundation/framework-recognition-plan.schema.v1.json'
    assert op['op']=='add' and op['precondition']=='absent' and op['path']=='/x-opensip-payload-registry/classes/parameter/rows/foundation~1framework-recognition-plan.schema.v1.json'
    assert key not in rows and 'requiredForEvaluatorMajors' not in op['value']
    rows[key]=copy.deepcopy(op['value'])
    text=model_raw.decode()
    assert len(patch['sourceTransforms'])==1
    transform=patch['sourceTransforms'][0];assert text.count(transform['old'])==1
    text=text.replace(transform['old'],transform['new']);model=text.encode();compile(model,'proposed-identity-model.v3.py','exec')
    parameter=json.loads(parameter_raw);assert parameter['$id']=='opensip.product.framework-recognition-plan.1'
    return schema,model,parameter
