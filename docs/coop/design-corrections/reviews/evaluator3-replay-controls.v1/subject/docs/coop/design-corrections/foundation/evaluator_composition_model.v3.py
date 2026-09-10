"""Pure evaluator3 output composition; NOT by itself input admission or full atom replay.

`compose` consumes a normalized population from enumeration admission and an atom
scanner supplied by the full reference driver. Unit tests may substitute scanners,
but such tests are composition tests, never complete retained-Run replay. No claimed
finding, witness, verdict or output identifier is an input to this function.
"""
import copy,hashlib,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('composition_identity3',HERE/'identity-model.v3.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
SEVERITY={'note':0,'warning':1,'error':2}

def sha(value):return hashlib.sha256(C.canonical(value)).hexdigest()
def cset(values):return sorted({C.canonical(v):v for v in values}.values(),key=C.canonical)
def truth(op,values):
    if any(v not in ('true','false','indeterminate') for v in values):raise C.AdmissionError('EVALUATOR_TRUTH_VALUE')
    if op=='not':
        if len(values)!=1:raise C.AdmissionError('EVALUATOR_NOT_ARITY')
        return {'true':'false','false':'true','indeterminate':'indeterminate'}[values[0]]
    if op=='and':return 'false' if 'false' in values else ('true' if all(v=='true' for v in values) else 'indeterminate')
    if op=='or':return 'true' if 'true' in values else ('false' if all(v=='false' for v in values) else 'indeterminate')
    raise C.AdmissionError('EVALUATOR_BOOLEAN_OPERATION')

def nodes(node):
    yield node
    if node['op'] in ('and','or'):
        for child in node['operands']:yield from nodes(child)
    elif node['op']=='not':yield from nodes(node['operand'])

def require_equal(a,b,key):
    if not C.equal_typed(a,b):raise C.AdmissionError(key)

def correspondence(rule,binding,subject,population):
    row=subject['row'];kind=subject['kind'];u=subject['universe']
    if kind in ('file','package'):tokens=[]
    else:
        candidates=[p for p in row['projections'] if p['closureId']==binding['detectorClosure']]
        if len(candidates)>1:raise C.AdmissionError('EVALUATOR_DUPLICATE_DETECTOR_PROJECTION')
        if not candidates or not candidates[0]['signatureTokens']:return None,'projection-unavailable'
        tokens=candidates[0]['signatureTokens']
        if not subject['collisionPopulationComplete']:return None,'population-incomplete'
        same=[]
        for other in population.values():
            r=other['row']
            if (other['universe'],other['kind'],r['subjectLanguage'],r['path'],r['qualifiedName'])!=(u,kind,row['subjectLanguage'],row['path'],row['qualifiedName']):continue
            for projection in r['projections']:
                if projection['closureId']==binding['detectorClosure'] and C.equal_typed(projection['signatureTokens'],tokens):same.append(other['subjectId'])
        if len(set(same))!=1:return None,'signature-ambiguous'
    return {'schemaVersion':2,'ruleStableId':rule['ruleProgramRef']['ruleStableId'],
        'detectorSemanticsMajor':rule['ruleProgramRef']['semanticsMajor'],
        'subjectKey':{'language':row['subjectLanguage'],'kind':kind,'logicalPath':row['path'],
                      'qualifiedName':row['qualifiedName'],'discriminator':sha(tokens)},'relatedSubjectKeys':[]},None

def is_waived(finding,waivers):
    for waiver in waivers['waivers']:
        target=waiver['target']
        if 'fingerprint' in target:
            if finding['fingerprint'] is not None and target['fingerprint']==finding['fingerprint']:return True
        elif target=={'ruleId':finding['ruleId'],'subjectPath':finding['subject']['logicalPath']}:return True
    return False

def compose(inputs,scan_atom):
    """Build all predicate/finding/proof output preimages from independently derived inputs.

    Required normalized inputs: plan,planId,executionPlanId,evaluatorClosure,policy,
    effectiveWaivers,emissionPlan,population(subject3 -> metadata),enumerations(ruleId ->
    exact rule-enumeration),enumerationDeficiencies(ruleId -> records),executionDeficiencies,
    evaluationInputRefs,inventoryRowCount,inventoryLocatorCount,factCount,observationCount,
    coverageCount,importKinds(import2 -> kind). Counts MUST be derived by the full input
    driver; this function does not claim to establish them. `scan_atom(rule,subject,node,pid)`
    is the independent native/import full scanner, returning a complete atom result.
    """
    policy=inputs['policy'];plan=inputs['plan'];population=inputs['population']
    require_equal(sha(policy),plan['policyDigest'],'EVALUATOR_POLICY_JOIN')
    require_equal(sha(inputs['effectiveWaivers']),plan['waiverDigest'],'EVALUATOR_WAIVER_JOIN')
    require_equal(inputs['emissionPlan']['policyDigest'],plan['policyDigest'],'EVALUATOR_EMISSION_POLICY_JOIN')
    bindings={b['ruleId']:b for b in inputs['emissionPlan']['rules']}
    if len(bindings)!=len(inputs['emissionPlan']['rules']):raise C.AdmissionError('EVALUATOR_EMISSION_DUPLICATE_RULE')
    require_equal(sorted(bindings),sorted(r['ruleId'] for r in policy['rules']),'EVALUATOR_EMISSION_RULE_TOTALITY')
    if policy['schemaMajor']!=2:raise C.AdmissionError('EVALUATOR_POLICY_MAJOR')
    namespaces=[(b['ruleStableId'],b['semanticsMajor']) for b in bindings.values()]
    if len(set(namespaces))!=len(namespaces):raise C.AdmissionError('EVALUATOR_EMISSION_FINGERPRINT_NAMESPACE')
    program={'schemaVersion':2,'policyDigest':sha(policy),'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in policy['rules']]}
    objects={};blobs={}
    def blob(v):
        key=sha(v);blobs[key]=C.canonical(v);return key
    def add(domain,v):
        key=M.identifier(domain,v);objects[key]=(domain,copy.deepcopy(v));return key
    program_digest=blob(program)
    addressed_subjects={sid for r in policy['rules'] if r['enabled'] for key in ('selectedSubjectIds','unresolvedSubjectIds') for sid in inputs['enumerations'][r['ruleId']][key]}
    for sid in addressed_subjects:
        subject=population[sid]
        desc={'schemaVersion':3,'universe':subject['universe'],'kind':subject['kind'],'nativeSubjectId':subject['row']['nativeSubjectId']}
        if subject['kind']=='package':desc['packageManifestPath']=subject['row']['path']
        require_equal(add('evaluation-subject',desc),sid,'EVALUATOR_SUBJECT_ID_JOIN')
    for rule in policy['rules']:
        b=bindings[rule['ruleId']]
        require_equal({k:b[k] for k in ('contributionId','ruleStableId','semanticsMajor')},
                      {k:rule['ruleProgramRef'][k] for k in ('contributionId','ruleStableId','semanticsMajor')},'EVALUATOR_EMISSION_RULE_REF_JOIN')
        if b['detectorClosure'] not in plan['semanticClosures']:raise C.AdmissionError('EVALUATOR_EMISSION_CLOSURE_UNSELECTED')
        if inputs['closures'][b['detectorClosure']]['kind']!='detector':raise C.AdmissionError('EVALUATOR_EMISSION_CLOSURE_KIND')
        if b['emissionProfile']!='declarative-subject-v1' or b['stabilityClass']!='path-stable':raise C.AdmissionError('EVALUATOR_EMISSION_PROFILE')
    cost=inputs['inventoryRowCount']+inputs['inventoryLocatorCount']
    for rule in policy['rules']:
        if not rule['enabled']:continue
        ns=list(nodes(rule['emitWhen']));atoms=sum(n['op'] not in ('and','or','not') for n in ns)
        cost+=len(inputs['enumerations'][rule['ruleId']]['selectedSubjectIds'])*(len(ns)+atoms*(inputs['factCount']+inputs['observationCount']+inputs['coverageCount']))
    # Python integers do not wrap; crossing U64 is still the normative budget-exceeded case.
    exhausted=cost>min(plan['budget']['limit'],18446744073709551615)
    predicate_bound=sum(len(inputs['enumerations'][r['ruleId']]['selectedSubjectIds'])*sum(1 for _ in nodes(r['emitWhen'])) for r in policy['rules'] if r['enabled'])
    finding_bound=sum(len(inputs['enumerations'][r['ruleId']]['selectedSubjectIds']) for r in policy['rules'] if r['enabled'])
    if not exhausted and (predicate_bound>100000 or finding_bound>100000):raise C.AdmissionError('EVALUATION.OUTPUT_BOUND_EXCEEDED')
    predicates=[];findings=[];waived=[];rule_results=[];execution=copy.deepcopy(inputs['executionDeficiencies'])
    def deficiency(source,cause,sid=None,pid=None,refs=()):return {'source':source,'cause':cause,'subjectId':sid,'predicateId':pid,'inputRefs':cset(refs),'evidenceKind':None,'nativeCause':None,'universe':None}
    if exhausted:execution.append(deficiency('execution','work-budget-exhausted',refs=inputs['evaluationInputRefs']))
    def blocks(rule,d):
        if d['source']!='import':return d['source'] in ('native','enumeration','execution')
        required={v['kind'] for v in rule['evidenceUse'] if v['requirement']=='required'}
        return d['evidenceKind'] in required
    def eval_node(rule,subject,node,pid):
        child_ids=M.predicate_child_addresses(node,pid)
        children_nodes=node.get('operands',[node['operand']] if node['op']=='not' else [])
        children=[eval_node(rule,subject,n,c) for n,c in zip(children_nodes,child_ids)]
        addressed={'schemaVersion':2,'ruleProgramDigest':program_digest,'ruleId':rule['ruleId'],
            'predicateId':pid,'operation':node['op'],'nodeDigest':sha(node)}
        ad=blob(addressed)
        if node['op'] in ('and','or','not'):
            value=truth(node['op'],[x['value'] for x in children])
            result={'kind':'boolean','value':value,'matchingFactIds':[],'uncertainFactIds':[],
                    'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[],
                    'scopeIds':cset([v for x in children for v in x['scopeIds']]),
                    'inputRefs':cset([v for x in children for v in x['inputRefs']]),
                    'deficiencies':cset([v for x in children for v in x['deficiencies']])}
            blocking=cset([v for x in children if x['value']=='indeterminate' for v in x['blocking']]) if value=='indeterminate' else []
        else:
            result=scan_atom(rule,subject,node,pid)
            blocking=result['deficiencies'] if result['value']=='indeterminate' else []
        witness={'schemaVersion':3,'programPredicateDigest':ad,'matchingFactIds':cset(result['matchingFactIds']),
            'uncertainFactIds':cset(result['uncertainFactIds']),'matchingImportRows':cset(result['matchingImportRows']),
            'uncertainImportRows':cset(result['uncertainImportRows']),'coverageIds':cset(result['coverageIds']),
            'countLimit':node.get('n') if node['op']=='count-at-most' else None,'childPredicateIds':cset(child_ids),
            'kind':result['kind'],'deficiencies':cset(result['deficiencies'])}
        wd=blob(witness)
        predicates.append({'ruleId':rule['ruleId'],'subjectId':subject['subjectId'],'predicateId':pid,
            'operation':node['op'],'inputRefs':cset(result['inputRefs']),'scopeIds':cset(result['scopeIds']),
            'value':result['value'],'witnessDigest':wd})
        descendants=[result]+[d for x in children for d in x['descendants']]
        return {**result,'witnessDigest':wd,'blocking':blocking,'descendants':descendants}
    for rule in policy['rules']:
        rid=rule['ruleId'];enumeration=copy.deepcopy(inputs['enumerations'][rid]);binding=bindings[rid]
        gating=rule['enabled'] and rule['gate'] and SEVERITY[rule['severity']]>=SEVERITY[policy['gateSeverityAtLeast']]
        if not rule['enabled']:
            disabled={'state':'disabled','inventoryRefs':[],'selectedSubjectIds':[],'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}
            require_equal(enumeration,disabled,'EVALUATOR_DISABLED_ENUMERATION')
            rule_results.append({'ruleId':rid,'enumeration':disabled,'outcome':'disabled','findingIds':[],'deficiencies':[]});continue
        deficiencies=copy.deepcopy(inputs['enumerationDeficiencies'][rid])+copy.deepcopy(inputs['requiredEvidenceDeficiencies'][rid]);live=False;unknown=enumeration['state']=='incomplete' or bool(inputs['requiredEvidenceDeficiencies'][rid]);rule_findings=[]
        if exhausted:
            deficiencies.append(deficiency('execution','work-budget-exhausted'));unknown=True
        else:
            for sid in enumeration['selectedSubjectIds']:
                subject=population[sid];result=eval_node(rule,subject,rule['emitWhen'],'p')
                deficiencies.extend(result['deficiencies'])
                if result['value']=='indeterminate':unknown=unknown or any(blocks(rule,d) for d in result['blocking'])
                if result['value']!='true':continue
                row=subject['row'];fingerprint,reason=correspondence(rule,binding,subject,population)
                fp=add('finding-fingerprint',fingerprint) if fingerprint is not None else None
                matching_facts=cset([v for n in result['descendants'] for v in n['matchingFactIds']])
                matching_imports=cset([v for n in result['descendants'] for v in n['matchingImportRows']])
                citations=[{'domain':'predicate-witness','digest':result['witnessDigest']}]
                for n in result['descendants']:
                    citations.extend({'domain':'fact','digest':v.split(':',1)[1]} for v in n['matchingFactIds']+n['uncertainFactIds'])
                    citations.extend({'domain':'coverage','digest':v.split(':',1)[1]} for v in n['coverageIds'])
                    citations.extend({'domain':'import','digest':v['importId'].split(':',1)[1]} for v in n['matchingImportRows']+n['uncertainImportRows'])
                    citations.extend(v for v in n['inputRefs'] if v['domain']=='import')
                code=rule.get('messageCode',rid)
                parameters={'schemaVersion':2,'messageCode':code,'parameters':{'ruleId':rid,'subjectPath':row['path'],
                    'qualifiedName':row['qualifiedName'],'subjectKind':subject['kind'],'subjectLanguage':row['subjectLanguage'],
                    'matchingFactCount':len(matching_facts),'matchingImportCount':len(matching_imports)}}
                finding={'schemaVersion':3,'fingerprint':fp,'ruleClosure':binding['detectorClosure'],'ruleId':rid,
                    'subjectId':sid,'subject':{'language':row['subjectLanguage'],'kind':subject['kind'],'logicalPath':row['path'],'qualifiedName':row['qualifiedName']},
                    'correspondence':{'state':'matched' if fp else 'unmatched','reason':reason},'messageCode':code,
                    'parameterDigest':blob(parameters),'severity':rule['severity'],'evidenceRefs':cset(citations)}
                fid=add('finding',finding);findings.append(fid);rule_findings.append(fid)
                if is_waived(finding,inputs['effectiveWaivers']):waived.append(fid)
                else:live=True
                if reason:deficiencies.append(deficiency('correspondence',reason,sid,'p',enumeration['inventoryRefs']))
        outcome='fail' if gating and live else ('indeterminate' if gating and unknown else 'pass')
        rule_results.append({'ruleId':rid,'enumeration':enumeration,'outcome':outcome,'findingIds':cset(rule_findings),'deficiencies':cset(deficiencies)})
    verdict='fail' if any(r['outcome']=='fail' for r in rule_results) else ('indeterminate' if execution or any(r['outcome']=='indeterminate' for r in rule_results) else 'pass')
    proof={'schemaVersion':3,'planId':inputs['planId'],'executionPlanId':inputs['executionPlanId'],'evaluatorClosure':inputs['evaluatorClosure'],
        'ruleProgramDigest':program_digest,'evaluationInputRefs':cset(inputs['evaluationInputRefs']),
        'predicateProofs':sorted(predicates,key=lambda x:tuple(x[k].encode() for k in ('ruleId','subjectId','predicateId'))),
        'findingIds':cset(findings),'verdict':verdict,'evaluationState':'budget-exhausted' if exhausted else 'evaluated',
        'ruleResults':sorted(rule_results,key=lambda r:r['ruleId'].encode()),'waivedFindingIds':cset(waived),'executionDeficiencies':cset(execution)}
    proof_id=add('proof-bundle',proof)
    return {'proofBundleId':proof_id,'proof':proof,'objects':objects,'blobs':blobs,'workUnits':cost}

def compare_complete_replay(actual,expected,objects,blobs):
    """Exact recomputed proof and every recomputed output preimage, not count-only matching.
    Owner closure admission and exact authoritative output-root selection are separate prerequisites.
    """
    require_equal(actual,expected['proof'],'EVALUATOR_COMPLETE_PROOF_REPLAY')
    for key,value in expected['objects'].items():require_equal(objects.get(key),value,'EVALUATOR_COMPLETE_OBJECT_REPLAY:'+key)
    for key,value in expected['blobs'].items():
        if blobs.get(key)!=value:raise C.AdmissionError('EVALUATOR_COMPLETE_BLOB_REPLAY:'+key)
    return True
