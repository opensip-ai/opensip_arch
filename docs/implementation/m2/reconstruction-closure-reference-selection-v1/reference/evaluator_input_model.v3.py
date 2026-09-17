"""Reconstruct evaluator3 inputs from the owner's admitted retained closure.

The caller must first run identity-model.v3.open_run_closure. This module reads
no claimed findings, predicate values or witnesses. Native view and canonical input
roots are admitted evidence inputs. Full replay compares the resulting proof separately.
"""
import hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
E=load('input_composition3',HERE/'evaluator_composition_model.v3.py')
ENUM=load('input_enumeration1',HERE/'enumeration_model.v1.py')
C=E.C
UNIVERSES=E.M.SCHEMA['x-opensip-evaluator-profile']['policyUniverseMap']
MODE_DOMAIN={k:'native.semantic-universe.'+v+'.v2' for k,v in E.M.DIGESTS['languageModes']['map'].items() if v is not None}

def execution_input_account(plan_id, execution_id, evaluator_closure, input_refs,
                            objects, blobs, enumeration, inventories, spec, closures, M):
    """Admit the retained host capture and compare the complete input selection.

    Capture occurs before evaluator outputs exist. Its semantic input promises
    exclude the ambient physical store census. Owner admission precedes this join.
    """
    selected=[r for r in input_refs if r['domain']=='execution-inputs']
    if len(selected)!=1:raise C.AdmissionError('EVALUATOR_EXECUTION_INPUTS_REQUIRED')
    ref=selected[0];manifest=C.parse(blobs[ref['digest']])
    E.require_equal(E.cset(input_refs),E.cset(manifest['selectedRefs']+[ref]),'EVALUATOR_EXECUTION_INPUT_SELECTION')
    if manifest['evaluatorClosure']!=evaluator_closure:raise C.AdmissionError('EVALUATOR_EXECUTION_INPUTS_CLOSURE')
    X=load('input_execution1',HERE/'execution_inputs_model.v1.py')
    plan=objects[plan_id][1];execution=objects[execution_id][1]
    promised=X.promised_pointers(manifest,plan,execution,enumeration,objects=objects,blobs=blobs)
    def records(domain):return {r['digest']:C.parse(blobs[r['digest']]) for r in manifest['selectedRefs'] if r['domain']==domain}
    result=X.admit_execution_inputs(plan_id=plan_id,plan=plan,execution_plan_id=execution_id,
        execution_plan=execution,enumeration_plan=enumeration,analysis_spec=spec,
        execution_inputs=manifest,objects=objects,blobs=blobs,
        store_pointers=promised['store_pointers'],
        inventories={E.sha(i):i for i in inventories},closures=closures,
        imports={i.split(':',1)[1]:objects[i][1] for i in plan['importIds']},
        candidate_results=records('candidate-producer-result'),target_attributions=records('target-attribution'),
        incoming_searches=records('incoming-search'),
        stage_specs={s['stageSpecDigest']:C.parse(blobs[s['stageSpecDigest']]) for s in execution['stages']},
        vcs_observation=C.parse(blobs[objects[plan['snapshotId']][1]['vcsDigest']]))
    if result['result']!='ADMIT':raise C.AdmissionError('EVALUATOR_EXECUTION_INPUTS_JOIN:'+','.join(result['refusals']))
    deficiencies=[]
    for row in result['requiredCellDeficiencies']:
        binding=enumeration['cells'][row['cellOrdinal']]['programBindings'][row['programOrdinal']]
        cause=row.get('deficiency')
        if cause not in M.SCHEMA['x-opensip-evaluator-deficiency-registry']['sources']['execution']:
            if cause not in (None,'source-syntax-invalid'):raise C.AdmissionError('EVALUATOR_EXECUTION_CAUSE_UNREGISTERED')
            cause='required-cell-unsatisfied'
        deficiencies.append({'source':'execution','cause':cause,'subjectId':None,'predicateId':None,
            'inputRefs':E.cset([ref]+row['inputRefs']),'evidenceKind':None,
            'nativeCause':row['nativeCause'],'universe':binding['universe']})
    return ref['digest'],E.cset(deficiencies),result

def required_parameters(plan,spec,blobs,objects,M):
    selected={}
    for item in spec['parameters']:
        row=M.parameter_row_of(item['schemaDigest'])
        if row is None:raise C.AdmissionError('EVALUATOR_PARAMETER_UNREGISTERED')
        if row in selected:raise C.AdmissionError('EVALUATOR_PARAMETER_DUPLICATE')
        value=C.parse(blobs[item['payloadDigest']]);selected[row]=(item,value)
    for doc in ['foundation/enumeration-plan.schema.v1.json','foundation/evaluator-emission-plan.schema.v1.json']:
        if doc not in selected:raise C.AdmissionError('EVALUATOR_REQUIRED_PARAMETER_MISSING:'+doc)
    policy=C.parse(blobs[plan['policyDigest']]);emission=selected['foundation/evaluator-emission-plan.schema.v1.json'][1]
    if policy['schemaMajor']!=2 or emission['policyDigest']!=plan['policyDigest']:raise C.AdmissionError('EVALUATOR_POLICY_BINDING')
    bindings=emission['rules'];rules=policy['rules']
    if [b['ruleId'] for b in bindings]!=[r['ruleId'] for r in rules]:raise C.AdmissionError('EVALUATOR_EMISSION_RULE_TOTALITY')
    if len({(b['ruleStableId'],b['semanticsMajor']) for b in bindings})!=len(bindings):raise C.AdmissionError('EVALUATOR_EMISSION_FINGERPRINT_NAMESPACE')
    for rule,binding in zip(rules,bindings):
        if rule['subjectEnumeration']['universe'] not in UNIVERSES:raise C.AdmissionError('EVALUATOR_POLICY_UNIVERSE_UNREGISTERED')
        if any(rule['ruleProgramRef'][k]!=binding[k] for k in ('contributionId','ruleStableId','semanticsMajor')):raise C.AdmissionError('EVALUATOR_EMISSION_RULE_REF_JOIN')
        closure=binding['detectorClosure']
        if closure not in plan['semanticClosures'] or objects[closure][1]['kind']!='detector':raise C.AdmissionError('EVALUATOR_EMISSION_CLOSURE_KIND')
    return selected,policy,emission

def reconstruct(plan_id,execution_id,evaluator_closure,input_refs,objects,blobs,owner,M):
    """Return normalized composition inputs plus actual native/import scanner record maps.
    `input_refs` are the admitted evidence input selection, not claimed output values.
    Required Plan inputs are recomputed independently and cannot be omitted by this selection.
    """
    plan=owner['plan'];snapshot=owner['snapshot'];spec=owner['analysisSpec']
    selected,policy,emission=required_parameters(plan,spec,blobs,objects,M)
    enumeration=selected['foundation/enumeration-plan.schema.v1.json'][1]
    scope=C.parse(blobs[plan['scopeDigest']]);membership=C.parse(blobs[enumeration['membershipDigest']])
    source_bytes={r['path']:blobs[r['sha256']] for r in snapshot['sourceInventory']}
    inventories=[C.parse(blobs[r['digest']]) for r in input_refs if r['domain']=='subject-inventory']
    universe_domains={key:value[0] for key,value in owner['nativeUniverses'].items()}
    universes={key:value[1] for key,value in owner['nativeUniverses'].items()}
    contexts={key:value[1] for key,value in owner['nativeContexts'].items()}
    retained={key:value[3] for key,value in owner['nativeUniverses'].items()}
    closures={key:objects[key][1] for key in plan['semanticClosures']}
    # Exact owner domain -> capability cell join, including mixed-language Plans.
    for cell in enumeration['cells']:
        for binding in cell['programBindings']:
            if binding['universe'] is not None and universe_domains.get(binding['universe'])!=MODE_DOMAIN[cell['languageMode']]:raise C.AdmissionError('EVALUATOR_CELL_UNIVERSE_DOMAIN')
    args=dict(plan=plan,plan_id=plan_id,analysis_spec=spec,scope_descriptor=scope,membership=membership,
        enumeration_plan=enumeration,inventories=inventories,native_contexts=contexts,universes=universes,closures=closures,
        snapshot_inventory=snapshot['sourceInventory'],source_blobs=source_bytes,retained_inputs=retained,
        universe_domains=universe_domains)
    admitted=ENUM.admit_enumeration(**args)
    if admitted['result']!='ADMIT':raise C.AdmissionError('EVALUATOR_ENUMERATION_JOIN:'+','.join(admitted['refusals']))
    population={};by_locator={};inventory_refs={};by_u_kind={}
    for inv in inventories:
        ci,pi,kind=inv['cellOrdinal'],inv['programOrdinal'],inv['kind'];cell=enumeration['cells'][ci];binding=cell['programBindings'][pi]
        locator=(ci,pi,kind);by_locator[locator]=inv
        ref={'domain':'subject-inventory','digest':E.sha(inv)};inventory_refs[locator]=ref
        if binding['universe'] is not None:by_u_kind.setdefault((binding['universe'],kind),[]).append(inv)
        for row in inv['rows']:
            desc={'schemaVersion':3,'universe':binding['universe'],'kind':kind,'nativeSubjectId':row['nativeSubjectId']}
            if kind=='package':desc['packageManifestPath']=row['path']
            sid=M.identifier('evaluation-subject',desc)
            item={'subjectId':sid,'universe':binding['universe'],'kind':kind,'row':row,'collisionPopulationComplete':True}
            if sid in population and not C.equal_typed(population[sid]['row'],row):raise C.AdmissionError('EVALUATOR_POPULATION_ATTRIBUTION_CONFLICT')
            population[sid]=item
    for item in population.values():
        if item['kind']=='symbol':item['collisionPopulationComplete']=all(inv['state']=='complete' for inv in by_u_kind[(item['universe'],'symbol')])
    def deficiency(source,cause,refs=(),sid=None,evidence_kind=None,native_cause=None,universe=None):
        return {'source':source,'cause':cause,'subjectId':sid,'predicateId':None,'inputRefs':E.cset(refs),'evidenceKind':evidence_kind,'nativeCause':native_cause,'universe':universe}
    scope_policy=selected.get('workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1')
    scope_policy=scope_policy[1] if scope_policy else None
    W=M.workflow_admission()
    def selected_path(rule,path):
        enum=rule['subjectEnumeration'];included=enum.get('include') or ['**']
        return (any(W.glob_match(g,path) for g in included) and not any(W.glob_match(g,path) for g in enum.get('exclude',[]))
                and (scope_policy is None or W.in_scope(scope_policy,path)))
    enumerations={};enum_deficiencies={}
    for rule in policy['rules']:
        rid=rule['ruleId']
        if not rule['enabled']:
            enumerations[rid]={'state':'disabled','inventoryRefs':[],'selectedSubjectIds':[],'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]};enum_deficiencies[rid]=[];continue
        kind=rule['subjectEnumeration']['subjectKind'];primary='symbol' if kind=='export' else kind;domain=UNIVERSES[rule['subjectEnumeration']['universe']]
        relevant=[]
        for locator,inv in by_locator.items():
            cell=enumeration['cells'][locator[0]]
            if locator[2]==primary and MODE_DOMAIN[cell['languageMode']]==domain:relevant.append(locator)
        refs=[inventory_refs[loc] for loc in relevant];incomplete=[inventory_refs[loc] for loc in relevant if by_locator[loc]['state']!='complete'];known=[];unresolved=[];defs=[]
        if not relevant:defs.append(deficiency('enumeration','no-covering-program'))
        for loc in relevant:
            inv=by_locator[loc]
            if inv['state']!='complete':
                defs.append(deficiency('enumeration','incomplete-inventory',[inventory_refs[loc]],native_cause=inv['nativeCause']))
                if inv['deficiency']=='source-syntax-invalid':defs.append(deficiency('enumeration','source-syntax-invalid',[inventory_refs[loc]]))
            binding=enumeration['cells'][loc[0]]['programBindings'][loc[1]]
            for row in inv['rows']:
                if not selected_path(rule,row['path']):continue
                desc={'schemaVersion':3,'universe':binding['universe'],'kind':primary,'nativeSubjectId':row['nativeSubjectId']}
                if primary=='package':desc['packageManifestPath']=row['path']
                sid=M.identifier('evaluation-subject',desc)
                if kind=='export' and row['exported']=='unknown':
                    unresolved.append(sid);defs.append(deficiency('enumeration','unknown-export-membership',[inventory_refs[loc]],sid));continue
                if kind=='export' and row['exported']=='not-exported':continue
                known.append(sid)
        enumerations[rid]={'state':'incomplete' if defs else 'complete','inventoryRefs':E.cset(refs),'selectedSubjectIds':E.cset(known),'unresolvedSubjectIds':E.cset(unresolved),'incompleteInventoryRefs':E.cset(incomplete)};enum_deficiencies[rid]=E.cset(defs)
    execution_digest,execution,execution_account=execution_input_account(
        plan_id,execution_id,evaluator_closure,input_refs,objects,blobs,
        enumeration,inventories,spec,closures,M)
    views={M.PREFIX['view']+':'+r['digest']:objects[M.PREFIX['view']+':'+r['digest']][1] for r in input_refs if r['domain']=='view'}
    fact_ids={f for v in views.values() for f in v['facts']};scope_ids={s for v in views.values() for s in v['scopeIds']};coverage_ids={c for v in views.values() for c in v['coverageIds']}
    facts={fid:{**objects[fid][1],'factId':fid,'payload':C.parse(blobs[objects[fid][1]['payloadDigest']])} for fid in fact_ids}
    scopes={sid:objects[sid][1] for sid in scope_ids};coverages={cid:C.parse(blobs[objects[cid][1]['payloadDigest']]) for cid in coverage_ids}
    explicit_coverage_ids={'coverage2:'+r['digest'] for r in input_refs if r['domain']=='coverage'}
    if not explicit_coverage_ids<=coverage_ids:raise C.AdmissionError('EVALUATOR_COVERAGE_INPUT_NOT_IN_VIEW')
    imports={};payloads={};observations={};import_kinds={};import_scopes={};import_flags={}
    # Owner Run closure already checks current exact snapshot / clean mapped revision.
    # These classifications are derived from that actual owner admission, never input flags.
    for iid in plan['importIds']:
        wrapper=objects[iid][1];imports[iid]=wrapper;import_scopes[wrapper['scopeDigest']]=C.parse(blobs[wrapper['scopeDigest']]);import_flags[iid]={'staleness':'current','consumable':True}
        payloads[iid]=C.parse(blobs[wrapper['payloadDigest']]);observations[iid]=C.parse(blobs[wrapper['observationDigest']]);import_kinds[iid]=wrapper['kind']
        obs=observations[iid];payload=payloads[iid];kind=wrapper['kind']
        if obs['kind']!=kind:raise C.AdmissionError('EVALUATOR_IMPORT_OBSERVATION_KIND_JOIN')
        joins=({'window':payload['observationWindow'],'population':payload['observedPopulation']} if kind=='runtime' else
               {'selection':payload['selection']} if kind=='test' else
               {'revisionRange':{k:payload['revisionRange'][k] for k in ('from','to')}} if kind=='history' else {})
        for field in ('window','population','selection','revisionRange'):
            if obs[field] is not None and (field not in joins or not C.equal_typed(obs[field],joins[field])):raise C.AdmissionError('EVALUATOR_IMPORT_OBSERVATION_PAYLOAD_JOIN:'+field)

    # This evaluator consumes every selected import as an availability/root input, even when
    # no atom has a matching row. That canonical selection prevents producer-side omission.
    expected_import_refs=E.cset({'domain':'import','digest':iid.split(':',1)[1]} for iid in plan['importIds'])
    if E.cset(r for r in input_refs if r['domain']=='import')!=expected_import_refs:raise C.AdmissionError('EVALUATOR_IMPORT_INPUT_TOTALITY')
    required_evidence={}
    for rule in policy['rules']:
        defs=[]
        if rule['enabled']:
            for use in rule['evidenceUse']:
                if use['requirement']=='required' and use['kind'] not in set(import_kinds.values()):defs.append(deficiency('import','evidence-kind-unavailable',evidence_kind=use['kind']))
        required_evidence[rule['ruleId']]=defs
    observations_count=sum((len(p.get('subjects',[])) if import_kinds[iid] in ('runtime','history') else len(p.get('tests',[]))+1 if import_kinds[iid]=='test' else 0) for iid,p in payloads.items())
    normalized={'executionInputsDigest':execution_digest,'plan':plan,'planId':plan_id,'executionPlanId':execution_id,'evaluatorClosure':evaluator_closure,'policy':policy,'effectiveWaivers':C.parse(blobs[plan['waiverDigest']]),'emissionPlan':emission,'population':population,'enumerations':enumerations,'enumerationDeficiencies':enum_deficiencies,'requiredEvidenceDeficiencies':required_evidence,'executionDeficiencies':E.cset(execution),'evaluationInputRefs':E.cset(input_refs),'inventoryRowCount':sum(len(inv['rows']) for inv in inventories),'inventoryLocatorCount':admitted['expectedRecords'],'factCount':len(facts),'observationCount':observations_count,'coverageCount':len(coverages),'importKinds':import_kinds,'closures':closures}
    atom_inputs={'planId':plan_id,'enumerationPlan':enumeration,'inventories':inventories,'facts':facts,'scopes':scopes,'coverages':coverages,'universeDomains':universe_domains,'closures':closures,'evaluationInputRefs':E.cset(input_refs),'planSelectedImportIds':plan['importIds'],'imports':imports,'importPayloads':payloads,'importObservations':observations,'targetAttributions':{},'incomingSearchAttestations':[], 'importScopes':import_scopes,'importFlagsAdapter':import_flags,'coverageScopes':{cid:objects[cid][1]['scopeId'] for cid in coverage_ids},'blobs':blobs}
    for ref in input_refs:
        if ref['domain']=='target-attribution':
            value=C.parse(blobs[ref['digest']]);fid=value['sourceFactId']
            if value['planId']!=plan_id or fid not in facts:raise C.AdmissionError('EVALUATOR_TARGET_ATTRIBUTION_INPUT_JOIN')
            if fid in atom_inputs['targetAttributions']:raise C.AdmissionError('EVALUATOR_TARGET_ATTRIBUTION_DUPLICATE')
            atom_inputs['targetAttributions'][fid]=value
        elif ref['domain']=='incoming-search':atom_inputs['incomingSearchAttestations'].append(C.parse(blobs[ref['digest']]))
    return normalized,atom_inputs
