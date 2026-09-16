"""Pure, explicit unaccepted inventory6 successor of report08 inventory5."""
import copy

def compose(inventory,schema,flags,detail_registry):
    inventory=copy.deepcopy(inventory);schema=copy.deepcopy(schema)
    assert inventory['schemaMajor']==schema['properties']['schemaMajor']['const']==5
    assert schema['$id'].endswith(':command-inventory:5')
    inventory['schemaMajor']=schema['properties']['schemaMajor']['const']=6
    schema['$id']=schema['$id'].rsplit(':',1)[0]+':6'
    inventory['standing']='Proposed joint report09 inventory6: eight explicit HTML history selectors, source-bound fit dispatch, envelope7 parity reference. Unaccepted; no CLI or metadata implementation qualification.'
    schema['title']='Proposed command inventory6 with explicit history and source-bound fit'
    schema['description']='Unaccepted successor of report08 inventory5. Existing authorization, format applicability and parity pointers remain unchanged. New query steps use invocation5 and query4; the complete envelope7 remains the parity reference.'
    commands={c['name']:c for c in inventory['commands']}
    assert [r['command'] for r in flags['rows']]==['default','analyze','fit','audit','candidates','inspect','review-brief','repair-preview']
    for row in flags['rows']:
        c=commands[row['command']]
        assert 'html' in c['formats'] and not any(f['flag']=='--history-run' for f in c['flags'])
        c['flags'].append(copy.deepcopy(row['appendFlag']))
    fit=commands['fit']['advisoryDispatch']
    assert fit==schema['$defs']['AdvisoryDispatch']['const']
    fit['sourceBinding']={'plannedParams':{'kind':'query','operation':'candidate.list','sourceStep':0},
        'resolution':'completed-analysis-step-exact-run','requestSchemaMajor':4,
        'completedResponseCustody':'exact-request-response-and-step-summary-through-required-output-settlement',
        'ephemeral':'unavailable-ephemeral-analysis','noncompletedQuery':'unavailable-query-result'}
    schema['$defs']['AdvisoryDispatch']['const']=copy.deepcopy(fit)
    schema['$defs']['AdvisoryDispatch']['description']='Fit plans an invocation5 source-bound query; the host constructs query4 after the exact analysis completes. Completed response custody and unavailable forms use envelope7 parity pointers.'
    renderer=next(r for r in inventory['renderers'] if r['format']=='json')
    assert renderer['version']==6 and renderer['parityRule'].count('CommandEnvelope major 6')==1
    renderer['version']=7;renderer['parityRule']=renderer['parityRule'].replace('CommandEnvelope major 6','CommandEnvelope major 7')
    mapping={'invocation:3':'invocation:5','graph-query:3':'graph-query:4','command-envelope:3':'command-envelope:7','command-inventory:5':'command-inventory:6'}
    changes=[]
    def walk(value,path=''):
        if isinstance(value,dict):
            if isinstance(value.get('$ref'),str):
                before=value['$ref']
                for old,new in mapping.items():
                    prefix='urn:opensip:product-v1:workflows:evaluator3:'+old
                    if before==prefix or before.startswith(prefix+'#'):
                        value['$ref']=prefix[:-len(old)]+new+before[len(prefix):]
                        changes.append({'path':path+'/$ref','before':before,'after':value['$ref']});break
            for k,v in value.items():walk(v,path+'/'+k)
        elif isinstance(value,list):
            for i,v in enumerate(value):walk(v,path+'/'+str(i))
    walk(schema)
    return inventory,schema,copy.deepcopy(detail_registry),changes
