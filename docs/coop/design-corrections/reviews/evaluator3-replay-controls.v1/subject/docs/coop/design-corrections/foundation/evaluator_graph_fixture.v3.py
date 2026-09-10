"""Synthetic retained-input fixture for evaluator3; no compiler or repository execution.

Reuses ONLY definitions of historical native-input fixture helpers. It does not execute
historical test suites or reuse their claimed proofs. Every new proof/output is composed
from the new input graph. Native tool/grammar observations remain synthetic, as in the
parent reference; native qualification is expressly not claimed.
"""
import ast,copy,hashlib,importlib.util,json,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('graph_composition3',HERE/'evaluator_composition_model.v3.py');E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
M=E.M;C=M.C

def fixture_helpers():
    p=HERE/'check-identity.py';tree=ast.parse(p.read_text());body=[]
    for node in tree.body:
        # The first top-level suite loop is a boundary, not a line-number dependency.
        if isinstance(node,ast.For):break
        body.append(node)
    scope={'__file__':str(p),'__name__':'historical_fixture_definitions_only'}
    exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),scope)
    return types.SimpleNamespace(**scope)

def build_file_inputs(*, atom_override=None, enabled=True, gate=True, budget_limit=10000, enumeration_filter=None, waiver_rows=None, import_specs=None, evidence_use=None, multiple_universes=False):
    H=fixture_helpers();N=H.N;objects={};blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest
    def add(domain,**fields):
        record={'schemaVersion':2,**fields};key=M.identifier(domain,record);objects[key]=(domain,record);return key
    def tree(files):return sorted(({'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in files.items()),key=lambda r:r['path'].encode())
    evaluator=add('closure',kind='evaluator',manifestDigest=blob(b'evaluator3 fixture manifest'),tree=[],semanticVersion='3.0.0',protocolMajor=3,platform='macos-aarch64')
    provider=add('closure',kind='provider',manifestDigest=blob(b'enumerator fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='macos-aarch64')
    detector=add('closure',kind='detector',manifestDigest=blob(b'declarative detector fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='any')
    native=H.syntax_inputs(objects,blobs,add,blob,tree)
    sources={'README.md':b'# Synthetic fixture\n','src/index.ts':b'export const x = 1;\n','extensionless':b'fixture\n'}
    universe_ids=[native['universeDigest']]
    if multiple_universes:
        alternate=copy.deepcopy(native['universe']);alternate['selectedGrammarIds']=['typescript.v1']
        bound=N.bind_syntax_universe(alternate,native['admission'],native['context'],{},[])
        if bound['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_ALTERNATE_NATIVE_UNIVERSE')
        digest=M.native_universe_frame('native.semantic-universe.syntax.v2',alternate,blobs)
        assert digest==bound['sourceUniverse'] and digest!=universe_ids[0]
        universe_ids.append(digest)
    inventory=tree(sources);paths=[r['path'] for r in inventory]
    config=blob({'analysis':{'profileId':'default','capabilities':['inventory'],'budget':{'unit':'work-units','limit':budget_limit}},'components':{},'discovery':{},'policy':{},'evidence':{}})
    scope=blob({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})
    vcs=blob({'schemaVersion':2,'kind':'none','commitId':None,'dirty':False,'sourceInventoryDigest':blob(inventory)})
    project='prj1-'+hashlib.sha256(b'fixture project').hexdigest()
    snapshot=add('snapshot',projectId=project,sourceInventory=inventory,resolvedConfigDigest=config,scopeDigest=scope,vcsDigest=vcs)
    # Empty admitted boundary list for the synthetic source; no real filesystem discovery claim.
    membership=N.assign_membership([],paths)
    enum={'schemaVersion':1,'snapshotId':snapshot,'scopeDigest':scope,'membershipDigest':blob(membership),'cells':[{'capabilityId':'inventory','languageMode':'syntax-only','workspaceRoot':'.','required':True,'kinds':['file','package'],
        'programBindings':[{'ordinal':0,'provenance':'default-unit','enumerator':{'status':'selected','closureId':provider},'nativeContextDigest':native['contextDigest'],'universe':native['universeDigest'],'programEntry':None,'extents':[{'kind':'file','paths':E.cset(paths)},{'kind':'package','paths':[]}]}]}]}
    if multiple_universes:
        binding=copy.deepcopy(enum['cells'][0]['programBindings'][0]);binding.update(ordinal=1,provenance='explicit-plan-selection',universe=universe_ids[1]);enum['cells'][0]['programBindings'].append(binding)
    enum_digest=blob(enum)
    atom=atom_override or {'op':'exists','relation':'file','minResolution':'enumerated','filters':[]}
    rule={'ruleId':'file-observed','ruleProgramRef':{'contributionId':'fixture','ruleStableId':'file-observed','semanticsMajor':2,'programDigest':blob(atom)},'enabled':enabled,'severity':'error','gate':gate,'subjectEnumeration':{'universe':'syntax','subjectKind':'file'},'emitWhen':atom,'evidenceUse':evidence_use or []}
    if enumeration_filter:rule['subjectEnumeration'].update(enumeration_filter)
    policy={'schemaFamily':'opensip.product.policy','schemaMajor':2,'gateSeverityAtLeast':'error','rules':[rule]};policy_digest=blob(policy)
    waivers={'schemaFamily':'opensip.product.waivers','schemaMajor':1,'waivers':waiver_rows or []}
    emission={'schemaVersion':1,'policyDigest':policy_digest,'rules':[{'ruleId':rule['ruleId'],'contributionId':'fixture','ruleStableId':'file-observed','semanticsMajor':2,'detectorClosure':detector,'stabilityClass':'path-stable','emissionProfile':'declarative-subject-v1'}]}
    parameters=E.cset([{'schemaDigest':blob((HERE/'enumeration-plan.schema.v1.json').read_bytes()),'payloadDigest':enum_digest},
                      {'schemaDigest':blob((HERE/'evaluator-emission-plan.schema.v1.json').read_bytes()),'payloadDigest':blob(emission)}])
    spec_record={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'inventory','languageMode':'syntax-only','workspaceRoot':'.','required':True}],'policyPackIds':['fixture.file-observed'],'parameters':parameters}
    cap=H.CURRENT_CAPABILITY_MANIFEST_BYTES;cap_digest=blob(cap);cap_id=hashlib.sha256(b'opensip.capability-manifest.v1\0'+cap).hexdigest()
    import_ids=[]
    W=M.workflow_admission()
    for item in import_specs or []:
        kind=item['kind'];payload=item['payload'];schema_doc=W.registry_row(kind,payload['payloadDomain'])['schemaDocument'];raw=(HERE.parent/schema_doc).read_bytes()
        built=W.build_import(kind,payload,payload['payloadDomain'],{payload['payloadDomain']:raw},{'kind':'exact-snapshot','snapshotId':snapshot},provider,provider,[],item.get('scope') or C.parse(blobs[scope]),item['observation'])
        blob(raw);blob(payload)
        for body in item.get('extra_blobs',[]):blob(body)
        for retained in built['retainedPreimages'].values():blob(retained)
        iid=M.identifier('import',built['wrapper']);objects[iid]=('import',built['wrapper']);import_ids.append(iid)
    import_ids=E.cset(import_ids)
    grant=blob({'schemaVersion':2,'projectId':project,'principals':[{'kind':'first-party','closureId':evaluator,'ownerSourceDigest':None}],'analysisOperations':sorted(['native-analysis','read-source']+(['read-import'] if import_ids else [])),'scopeDigest':scope})
    plan_fields=dict(snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=sorted([evaluator,provider,detector]),analysisSpecDigest=blob(spec_record),resolvedConfigDigest=config,nativeContextDigests=[native['contextDigest']],importIds=import_ids,policyDigest=policy_digest,waiverDigest=blob(waivers),scopeDigest=scope,budget={'unit':'work-units','limit':budget_limit},semanticGrantDigest=grant)
    plan_id=add('plan',**plan_fields);plan=objects[plan_id][1]
    inventory_results=[];population={}
    languages={'README.md':'markdown','src/index.ts':'typescript','extensionless':'unspecified'}
    for program_ordinal,universe in enumerate(universe_ids):
        for kind in ['file','package']:
            rows=[{'nativeSubjectId':path,'kind':'file','path':path,'qualifiedName':path,'subjectLanguage':languages[path],'signatureTokens':[],'projections':[]} for path in paths] if kind=='file' else []
            inv={'schemaVersion':1,'planId':plan_id,'parameterDigest':enum_digest,'cellOrdinal':0,'programOrdinal':program_ordinal,'kind':kind,'state':'complete','deficiency':None,'nativeCause':None,'examinedPaths':E.cset(paths) if kind=='file' else [],'rows':sorted(rows,key=lambda r:r['nativeSubjectId'].encode())}
            digest=blob(inv);inventory_results.append((digest,inv))
            for row in rows:
                sid=M.identifier('evaluation-subject',{'schemaVersion':3,'universe':universe,'kind':'file','nativeSubjectId':row['nativeSubjectId']})
                population[sid]={'subjectId':sid,'universe':universe,'kind':'file','row':row,'collisionPopulationComplete':True}
    view_ids=[];scope_ids=[];coverage_ids=[];all_facts=[]
    for universe in universe_ids:
        scope_id=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation='file',resolution='enumerated',enumeratorClosure=provider,subjects=E.cset(paths))
        facts=[]
        relation_schema=blob((HERE/'relation-payload-schemas.v2.json').read_bytes());coverage_schema=blob((HERE.parent/'native/native-evidence.schemas.v2.json').read_bytes())
        for row in inventory:
            facts.append(add('fact',snapshotId=snapshot,relation='file',resolution='enumerated',sourceUniverse=universe,targetUniverse=universe,producerClosure=provider,payloadSchemaDigest=relation_schema,payloadDigest=blob({'path':row['path'],'contentSha256':row['sha256'],'byteLength':row['bytes']}),anchors=[],confidenceMillionths=1000000))
        coverage_payload=H.coverage_result(objects[scope_id][1],universe,True,blobs,paths)
        admitted=N.admit_coverage_result_v3(coverage_payload,objects[scope_id][1],[],coverage_schema)
        if admitted['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_NATIVE_COVERAGE:'+str(admitted))
        coverage_id=add('coverage',scopeId=scope_id,payloadSchemaDigest=coverage_schema,payloadDigest=blob(coverage_payload))
        view_id=add('view',planId=plan_id,scopeIds=[scope_id],facts=E.cset(facts),coverageIds=[coverage_id],producerClosure=provider,schemaDigests=sorted([relation_schema,coverage_schema]))
        view_ids.append(view_id);scope_ids.append(scope_id);coverage_ids.append(coverage_id);all_facts.extend(facts)
    stage_schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:evaluator3-view-output','type':'object','additionalProperties':False,'required':['viewId'],'properties':{'viewId':{'type':'string','pattern':'^view2:[0-9a-f]{64}(?![\\s\\S])'}}}
    stage=blob({'schemaVersion':2,'planId':plan_id,'producerClosure':provider,'operation':'derive-inventory-view','parameters':parameters,'outputDomains':['view'],'outputSchemaDigest':blob(stage_schema)})
    execution_id=add('execution-plan',planId=plan_id,stages=[{'ordinal':0,'stageSpecDigest':stage,'requires':[],'outputDomains':['view']}])
    refs=E.cset([{'domain':'view','digest':v.split(':',1)[1]} for v in view_ids]+[{'domain':'import','digest':iid.split(':',1)[1]} for iid in import_ids]+[{'domain':'subject-inventory','digest':d} for d,inv in inventory_results])
    enum_refs=[{'domain':'subject-inventory','digest':d} for d,inv in inventory_results if inv['kind']=='file']
    inputs={'plan':plan,'planId':plan_id,'executionPlanId':execution_id,'evaluatorClosure':evaluator,'policy':policy,'effectiveWaivers':waivers,'emissionPlan':emission,'population':population,
        'enumerations':{rule['ruleId']:{'state':'complete','inventoryRefs':E.cset(enum_refs),'selectedSubjectIds':E.cset(population),'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}},'enumerationDeficiencies':{rule['ruleId']:[]},'requiredEvidenceDeficiencies':{rule['ruleId']:[]},'executionDeficiencies':[],'evaluationInputRefs':refs,'inventoryRowCount':len(paths)*len(universe_ids),'inventoryLocatorCount':2*len(universe_ids),'factCount':len(all_facts),'observationCount':0,'coverageCount':len(coverage_ids),'importKinds':{iid:objects[iid][1]['kind'] for iid in import_ids},'closures':{k:v for k,(dom,v) in objects.items() if dom=='closure'}}
    if not enabled:inputs['enumerations'][rule['ruleId']]={'state':'disabled','inventoryRefs':[],'selectedSubjectIds':[],'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}
    return {'objects':objects,'blobs':blobs,'inputs':inputs,'native':native,'snapshot':objects[snapshot][1],'membership':membership,'enumerationPlan':enum,'inventoryResults':inventory_results,'viewId':view_id,'scopeId':scope_id,'coverageId':coverage_id,'viewIds':E.cset(view_ids),'scopeIds':E.cset(scope_ids),'coverageIds':E.cset(coverage_ids),'coveragePayload':coverage_payload}

def fixture_file_scanner(graph):
    """Bootstrap file scanner for owner-closure input admission only; ignores filters. Its claimed output is never used by full replay or exported as a semantic positive."""
    objects,blobs=graph['objects'],graph['blobs'];scope=objects[graph['scopeId']][1];view=objects[graph['viewId']][1]
    def scan(rule,subject,node,pid):
        if node.get('evidence'):
            return {'kind':'imported-atom','value':'indeterminate','matchingFactIds':[],'uncertainFactIds':[],'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[],'scopeIds':[],'inputRefs':graph['inputs']['evaluationInputRefs'],'deficiencies':[]}
        if node.get('relation')!='file' or node.get('minResolution')!='enumerated':raise C.AdmissionError('FIXTURE3_ATOM_SUBSET')
        matches=[]
        for fid in view['facts']:
            fact=objects[fid][1];payload=C.parse(blobs[fact['payloadDigest']])
            if fact['sourceUniverse']==subject['universe'] and fact['relation']=='file' and payload['path']==subject['row']['nativeSubjectId']:matches.append(fid)
        return {'kind':'native-atom','value':('true' if matches else 'false') if node['op']=='exists' else ('false' if matches else 'true') if node['op']=='none' else ('true' if len(matches)<=node['n'] else 'false') if node['op']=='count-at-most' else 'true','matchingFactIds':E.cset(matches),'uncertainFactIds':[],'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[graph['coverageId']],'scopeIds':[graph['scopeId']],'inputRefs':[{'domain':'view','digest':graph['viewId'].split(':',1)[1]}],'deficiencies':[]}
    return scan

def seal_fixture(graph):
    out=E.compose(graph['inputs'],fixture_file_scanner(graph));objects=copy.deepcopy(graph['objects']);blobs=copy.deepcopy(graph['blobs']);objects.update(out['objects']);blobs.update(out['blobs']);i=graph['inputs']
    def add(domain,fields):
        value={'schemaVersion':3,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
    evidence=add('semantic-evidence',{'planId':i['planId'],'viewIds':graph['viewIds'],'coverageIds':graph['coverageIds'],'importIds':i['plan']['importIds'],'findingIds':out['proof']['findingIds'],'proofBundleId':out['proofBundleId']})
    seal=add('evaluation-seal',{'planId':i['planId'],'executionPlanId':i['executionPlanId'],'evidenceId':evidence,'evaluatorClosure':i['evaluatorClosure'],'policyDigest':i['plan']['policyDigest'],'proofBundleId':out['proofBundleId'],'verdict':out['proof']['verdict']})
    run={'schemaVersion':3,'projectId':graph['snapshot']['projectId'],'snapshotId':i['plan']['snapshotId'],'planId':i['planId'],'evidenceId':evidence,'evaluationSealId':seal,'capabilityManifestId':i['plan']['capabilityManifestId']}
    return run,objects,blobs,out
