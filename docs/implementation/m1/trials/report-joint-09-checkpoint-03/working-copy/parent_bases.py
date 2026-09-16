"""Construct all parent positive fixtures under the proposed report contracts.

Domain rows are pinned synthetic fixture material, not external stored envelopes.
Graph queries are reissued by the current mock owner. Legacy ledger attempts
explicitly have source major3 and unavailable timing. No new host authority,
Run replay, elapsed clocks or product delivery is inferred from these fixtures.
"""
import copy,hashlib,json


def build(validation,model,source_builder,fit_builder):
    parent=json.loads(validation.read_unit('report-projection','fixtures.json'))
    inventory=json.loads(validation.read_unit('report-projection','owner/command-inventory.v5.json'))
    context,material=source_builder.build(validation.read_unit,model,validation.report)
    result={}
    for name,original in parent['bases'].items():
        if name in ['fit-sealed','fit-sealed-truncated-150','fit-ephemeral']:
            result[name]=fit_builder.make(name)[0];continue
        doc=copy.deepcopy(original);command=doc['command']
        # New envelope constructor with the same admitted-shape synthetic
        # domain observations. This helper is only a fixture generator.
        doc['envelope']={**{k:copy.deepcopy(v) for k,v in original['envelope'].items() if k!='schemaMajor'},'schemaMajor':7}
        ledger=doc['invocationLedger']
        if not ledger['cancellation']['requested']:ledger['cancellation']={'requested':False,'phase':'none'}
        for step in ledger['steps']:
            if step['recorded']:
                projections=[]
                for attempt in step['attempts']:
                    row=validation.T.project_attempt(3,attempt)
                    for k in ['faultCause','retried']:
                        if k in attempt:row[k]=attempt[k]
                    projections.append(row)
                step['attempts']=projections
                step['attemptServiceTime']=validation.T.summarize_attempts([{k:v for k,v in a.items() if k not in ['faultCause','retried']} for a in projections])
            else:step['attemptServiceTime']={'state':'not-finalized','reason':'render-in-progress' if step['kind']=='render' else 'step-result-not-recorded'}
        if doc['panels'].get('graph',{}).get('state')=='present':
            comparison='comparisonResultId' in doc['envelope'].get('run',{})
            projected=context['exploration'](doc['envelope'],command,comparison,ledger)
            doc['panels']['graph']=projected['graph']
        reason='no-admitted-result' if doc['envelope']['kind']=='failure' else 'evidence-purged'
        for k in ['configuration','descriptions']:doc['panels'][k]={'state':'unavailable','reason':reason}
        condition=next(c for c in validation.report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')==command)
        for key in ['featureStates','supportedReportViews']:doc[key]=copy.deepcopy(condition['then']['properties'][key]['const'])
        doc['budgetProfile']={k:copy.deepcopy(v['const']) for k,v in validation.report['$defs']['BudgetProfileV1']['properties'].items()}
        doc['disclosures']=model.document_disclosures(doc['panels']);doc['disclosures']['explicitHistorySelection']=None
        row=next(c for c in inventory['commands'] if c['name']==command)
        text=model.static_parity_text(doc['envelope'],row,doc['disclosures']).encode()
        doc['staticParity']={'format':model.STATIC_FORMAT,'textSha256':hashlib.sha256(text).hexdigest(),'textBytes':len(text)}
        result[name]=doc
    return result,material
