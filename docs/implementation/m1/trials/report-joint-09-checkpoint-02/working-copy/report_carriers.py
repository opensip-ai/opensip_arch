"""Proposed report carriers for the selected owner candidates; semantic joins pending."""
import copy


def closed(properties,required=None,**extra):
    return {'type':'object','additionalProperties':False,'required':list(properties) if required is None else required,'properties':properties,**extra}


def ref(value):return {'$ref':value}


def integrate(report,invocation,configuration_id,history_selection_id,history_panel_id):
    report=copy.deepcopy(report);defs=report['$defs']
    duration=invocation['$id']+'#/$defs/AttemptDurationV1'
    common='urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/'
    defs['ConfigurationPanelStateV1']={'oneOf':[closed({'state':{'const':'present'},'data':ref(configuration_id)}),ref('#/$defs/PanelNotPresentV1')]}
    defs['PanelsV1']['properties']['configuration']=ref('#/$defs/ConfigurationPanelStateV1')
    defs['BudgetProfileV1']['properties']['profileId']['const']='opensip.report-projection.development-caps.5'
    priority=defs['BudgetProfileV1']['properties']['projectionPriority']['const']
    assert 'configuration' not in priority
    # Preserve the old seven-panel prefix and its existing priority decisions.
    priority.append('configuration')
    commands=[]
    for condition in report['allOf']:
        command=condition.get('if',{}).get('properties',{}).get('command',{}).get('const')
        if not command:continue
        required=condition['then']['properties']['panels']['required']
        assert 'configuration' not in required;required.append('configuration');commands.append(command)
    assert len(commands)==8 and len(set(commands))==8

    cancellation=defs['InvocationLedgerV1']['properties']['cancellation']
    defs['InvocationLedgerV1']['properties']['cancellation']={'oneOf':[
        {'const':{'requested':False,'phase':'none'}},
        {'allOf':[copy.deepcopy(cancellation),{'properties':{'requested':{'const':True}}}]}],
        'description':'No observed cancellation has no signal value. A requested cancellation carries the invocation owner signal/phase. Absence of the optional InvocationRecord.cancellation projects to the explicit none state.'}

    original_history=defs['HistoryPanelV1'];assert 'AutomaticHistoryPanelV1' not in defs
    defs['AutomaticHistoryPanelV1']=original_history
    defs['HistoryPanelV1']={'oneOf':[ref('#/$defs/AutomaticHistoryPanelV1'),ref(history_panel_id)]}
    disclosures=defs['DisclosuresV1']
    assert 'explicitHistorySelection' not in disclosures['properties']
    disclosures['properties']['explicitHistorySelection']={'oneOf':[{'type':'null'},ref(history_selection_id)],
        'description':'Mandatory exact explicit history selection, or null in automatic mode. Never removed with an omitted/unavailable history panel; echoed by the script-independent disclosure section.'}
    disclosures['required'].append('explicitHistorySelection')

    step=defs['LedgerStepV1'];attempt=step['properties']['attempts']['items']
    attempt['required']+=['sourceSchemaMajor','duration']
    attempt['properties']['sourceSchemaMajor']={'enum':[3,4,5]}
    attempt['properties']['duration']={'oneOf':[ref(duration),{'const':{'state':'unavailable','reason':'not-retained'}}]}
    supervisor_lost={'const':{'state':'unavailable','reason':'supervisor-lost'}}
    forbid_supervisor_lost={'not':{'required':['reason'],'properties':{'reason':{'const':'supervisor-lost'}}}}
    outcome_join={
        'if':{'properties':{'outcome':{'const':'abandoned'}}},
        'then':{'properties':{'duration':supervisor_lost}},
        'else':{'properties':{'duration':forbid_supervisor_lost}},
    }
    attempt['allOf']=[{
        'if':{'properties':{'sourceSchemaMajor':{'const':3}}},
        'then':{'properties':{'duration':{'const':{'state':'unavailable','reason':'not-retained'}}}},
        'else':{'properties':{'duration':ref(duration)},'allOf':[outcome_join]},
    }]
    count={'type':'integer','minimum':1,'maximum':3}
    defs['AttemptServiceTimeV1']={'oneOf':[
        closed({'state':{'const':'no-attempts'},'attemptCount':{'const':0}}),
        closed({'state':{'const':'measured'},'attemptCount':count,'milliseconds':{'type':'integer','minimum':0,'maximum':18446744073709551615}}),
        closed({'state':{'const':'unavailable'},'attemptCount':count,'unavailableAttemptCount':{'type':'integer','minimum':1,'maximum':3},'reason':{'const':'incomplete-observations'}}),
        closed({'state':{'const':'unavailable'},'attemptCount':count,'unavailableAttemptCount':{'const':0},'reason':{'const':'duration-overflow'}}),
        closed({'state':{'const':'not-finalized'},'reason':{'enum':['render-in-progress','step-result-not-recorded']}})],
        'description':'Sum of terminal attempt service observations, never step wall time. Exact source/ExecutionId/summary and unrecorded reason joins are mandatory.'}
    step['required'].append('attemptServiceTime')
    step['properties']['attemptServiceTime']=ref('#/$defs/AttemptServiceTimeV1')
    step.setdefault('allOf',[]).append({'if':{'properties':{'recorded':{'const':False}}},
        'then':{'properties':{'attemptServiceTime':{'properties':{'state':{'const':'not-finalized'}}}}},
        'else':{'properties':{'attemptServiceTime':{'not':{'properties':{'state':{'const':'not-finalized'}}}}}}})

    remove={'declared-configuration','step-duration','explicit-older-run-selection'}
    assert remove <= set(defs['FeatureId']['enum'])
    defs['FeatureId']['enum']=[v for v in defs['FeatureId']['enum'] if v not in remove]
    for condition in report['allOf']:
        states=condition.get('then',{}).get('properties',{}).get('featureStates',{}).get('const')
        if states is not None:states[:]=[v for v in states if v['featureId'] not in remove]
    report['description']+=' Joint candidate adds configuration, explicit history selection and attempt service observations. Present data requires its owner joins; complete composed budget derivation and actual fixture integration remain pending.'
    return report
