"""Additional internal report joins. Source custody is separately admitted by host."""
import copy


def require(condition,code):
    if not condition:raise ValueError(code)


def disclosures(panels,selection,model,history,current_run,validate):
    visible=copy.deepcopy(panels)
    if selection is not None:
        require(selection==history.plan_selection({'mode':'explicit','runIds':selection['requestedRunIds']},current_run),'HISTORY-SELECTION-ANCHOR')
        visible.pop('history',None)
        if panels.get('history',{}).get('state')=='present':
            panel=panels['history']['data']
            history.validate_panel(panel,current_run,validate)
            require(panel['selection']==selection,'HISTORY-SELECTION-DISCLOSURE')
    elif panels.get('history',{}).get('state')=='present':
        require(panels['history']['data']['selection'].get('policy')!='explicit-run-ids.1','HISTORY-EXPLICIT-SELECTION-MISSING')
    out=model.document_disclosures(visible);out['explicitHistorySelection']=copy.deepcopy(selection)
    return out


def timing(ledger,timing_owner,equal):
    seen=set()
    for step in ledger['steps']:
        if not step['recorded']:
            expected={'state':'not-finalized','reason':'render-in-progress' if step['kind']=='render' else 'step-result-not-recorded'}
        else:
            attempts=[]
            for a in step['attempts']:
                require(a['executionId'] not in seen,'TIMING-DUPLICATE-EXECUTION')
                seen.add(a['executionId'])
                attempts.append({k:copy.deepcopy(v) for k,v in a.items() if k not in ['faultCause','retried']})
            expected=timing_owner.summarize_attempts(attempts)
        require(equal(step['attemptServiceTime'],expected),'TIMING-SERVICE-SUM')


def receipt(selection,value,catalog,equal):
    require(selection['closureId']==value['closureId'],'DESCRIPTION-CLOSURE')
    if value['state']=='unavailable':return
    tree=value['tree'];paths=[r['path'] for r in tree]
    require(len(paths)==len(set(paths)),'DESCRIPTION-TREE-DUPLICATE')
    authority=value['capabilityAuthority']
    if authority is not None:
        require(authority['closureId']==value['closureId'] and authority['platform']==value['platform'],'DESCRIPTION-CAPABILITY-ASSOCIATION')
    if selection['capabilities']:require(authority is not None,'DESCRIPTION-CAPABILITY-AUTHORITY')
    listing=[r for r in tree if r['path']==catalog.CATALOG_PATH]
    if value['state']=='no-catalogue-declared':
        require(not listing,'DESCRIPTION-ABSENCE-TREE');return
    require(len(listing)==1 and equal(listing[0],value['listing']),'DESCRIPTION-LISTING-TREE')
    for group in catalog.GROUPS:
        keys=[list(catalog.entry_key(group,r['descriptor'])) if r['state']=='present' else r['key'] for r in value[group]]
        require(equal(keys,selection[group]),'DESCRIPTION-SELECTED-KEYS')


def descriptions(panel,run_anchor,preview,catalog,equal):
    if panel['state']!='present':return
    data=panel['data']
    if data['run']['state']=='present':
        row=data['run']['data']
        require(run_anchor is not None and (row['runId'],row['planId'])==(run_anchor['runId'],run_anchor['planId']),'DESCRIPTION-RUN-PLAN')
        selection=row['selection'];receipts=row['receipts']
        require(len(selection)==len(receipts),'DESCRIPTION-RECEIPT-COUNT')
        require(len({r['closureId'] for r in selection})==len(selection),'DESCRIPTION-DUPLICATE-CLOSURE')
        for selected,value in zip(selection,receipts):
            require(not selected['recipes'],'DESCRIPTION-RUN-RECIPE-SELECTION')
            receipt(selected,value,catalog,equal)
    if data['recipe']['state']=='present':
        row=data['recipe']['data']
        require(preview is not None and row['repairPlanId']==preview['repairPlanId'] and equal(row['recipe'],preview['descriptor']['recipe']),'DESCRIPTION-PREVIEW-RECIPE')
        selected=row['selection'];recipe=row['recipe']
        require(not selected['capabilities'] and not selected['rules'] and selected['closureId']==recipe['closureId'],'DESCRIPTION-RECIPE-SELECTION')
        require(selected['recipes']==[[recipe[k] for k in ['contributionId','recipeId','recipeVersion']]],'DESCRIPTION-RECIPE-KEY')
        receipt(selected,row['receipt'],catalog,equal)


def additions(doc,current_run,run_anchor,preview,model,history,timing_owner,catalog,canonical,validate_history):
    expected=disclosures(doc['panels'],doc['disclosures']['explicitHistorySelection'],model,history,current_run,validate_history)
    require(canonical.equal_typed(expected,doc['disclosures']),'REPORT-DISCLOSURES')
    timing(doc['invocationLedger'],timing_owner,canonical.equal_typed)
    configuration=doc['panels']['configuration']
    if configuration['state']=='present':
        require(run_anchor is not None and configuration['data']['source']['planId']==run_anchor['planId'],'CONFIGURATION-RUN-PLAN')
    descriptions(doc['panels']['descriptions'],run_anchor,preview,catalog,canonical.equal_typed)
