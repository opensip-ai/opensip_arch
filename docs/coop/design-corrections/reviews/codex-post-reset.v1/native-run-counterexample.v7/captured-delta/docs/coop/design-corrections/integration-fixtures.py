"""Synthetic shared graph construction, copied from the corrected coauthor reference fixture.
Source: foundation/check-identity.py SHA256 b91c7f6ad95240a77ccc2b760f70d277dbd0e276955ffa400877c0909d97e0e4.
Copied declarations: ATOM, COVERAGE_PAYLOAD_SCHEMA, FACT_PAYLOAD_SCHEMA, POLICY, RULE, STAGE_OUTPUT_SCHEMA, WAIVERS, build, compiled_program, graph_with_import, native_inputs, put_blob, rekey, rekey_plan.
No expected verdict or independent-review claim is derived from this builder.
Shared import/source mutations retain their own explicit preimage propagation.
"""
import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('integration_fixture_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('integration_fixture_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']

ATOM={'op':'none','relation':'references','minResolution':'resolved','filters':[{'field':'target','cmp':'eq','value':'foo'}]}

RULE={'ruleId':'no-consumer','ruleProgramRef':{'contributionId':'fixture','ruleStableId':'no-consumer','semanticsMajor':2,
        'programDigest':hashlib.sha256(C.canonical(ATOM)).hexdigest()},
      'enabled':True,'severity':'error','gate':True,
      'subjectEnumeration':{'universe':'typescript','subjectKind':'symbol'},
      'emitWhen':ATOM,'evidenceUse':[],'messageCode':'no-consumer'}

POLICY={'schemaFamily':'opensip.product.policy','schemaMajor':1,'gateSeverityAtLeast':'error','rules':[RULE]}

WAIVERS={'schemaFamily':'opensip.product.waivers','schemaMajor':1,'waivers':[]}

def compiled_program(policy):
    return {'schemaVersion':1,'policyDigest':hashlib.sha256(C.canonical(policy)).hexdigest(),
            'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in policy['rules']]}

COVERAGE_PAYLOAD_SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:coverage-payload',
    'type':'object','additionalProperties':False,'required':['examined','resolved','closed'],
    'properties':{k:{'type':'boolean'} for k in ('examined','resolved','closed')}}

FACT_PAYLOAD_SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:references-payload',
    'type':'object','additionalProperties':False,'required':['target'],
    'properties':{'target':{'type':'string','minLength':1,'maxLength':4096}}}

STAGE_OUTPUT_SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:stage-output',
    'type':'object','additionalProperties':False,'required':['viewId'],
    'properties':{'viewId':{'type':'string','pattern':'^view2:[0-9a-f]{64}(?![\\s\\S])'}}}

def native_inputs(objects,blobs,add,blob,stdlib_body=b'declare const es2022: unknown;\n'):
    """One admitted TypeScript native context and its universe, through the ACTUAL native
    admission functions, over retained (small) compiler and stdlib closure trees."""
    stdlib_files={'lib/lib.dom.d.ts':b'declare const dom: unknown;\n','lib/lib.es2022.d.ts':stdlib_body}
    tool_files={'bin/node':b'#!fixture-runtime\n','lib/tsc.js':b'// fixture compiler\n'}
    def tree(files):return sorted(({'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in files.items()),key=lambda r:r['path'].encode())
    stdlib=add('closure',kind='stdlib',manifestDigest=blob(b'fixture-stdlib-manifest'),tree=tree(stdlib_files),
               semanticVersion='5.6.3',protocolMajor=2,platform='any')
    toolchain=add('closure',kind='toolchain',manifestDigest=blob(b'fixture-toolchain-manifest'),tree=tree(tool_files),
                  semanticVersion='5.6.3',protocolMajor=2,platform='macos-aarch64')
    tool_tree={r['path']:r['sha256'] for r in objects[toolchain][1]['tree']}
    context=copy.deepcopy(NATIVE_FIXTURES['tsNativeContext'])
    context['toolchain'].update(
        compilerVersion='5.6.3',compilerPackageDigest=tool_tree['lib/tsc.js'],
        typescriptStdlibMerkleRoot=stdlib.removeprefix('closure2:'),
        libSelection=['dom','es2022'],
        standardLibraryComponentDigests=sorted(({'component':p.rpartition('/')[2],'sha256':blob(b)}
            for p,b in stdlib_files.items()),key=lambda r:r['component'].encode()))
    context['toolClosure']={'closureId':toolchain,'compiler':tool_tree['lib/tsc.js'],'runtime':tool_tree['bin/node']}
    context['configProjection']['honoredOptions']['lib']=['DOM','ES2022']
    admission=N.admit_native_context('typescript',context,{k:objects[k][1] for k in (stdlib,toolchain)})
    if admission['refusals']:raise C.AdmissionError('FIXTURE_NATIVE_CONTEXT:'+','.join(admission['refusals']))
    universe=copy.deepcopy(NATIVE_FIXTURES['tsUniverse']);universe['nativeContextId']=admission['nativeContextId']
    binding=N.bind_typescript_universe(universe,admission,context)
    if binding['result']!='ADMIT':raise C.AdmissionError('FIXTURE_NATIVE_UNIVERSE:'+','.join(binding['refusals']))
    context_digest=M.native_context_frame('native.context.typescript.v2',context,blobs)
    universe_digest=M.native_universe_frame('native.semantic-universe.typescript.v2',universe,blobs)
    if context_digest!=admission['planNativeContextDigest'] or universe_digest!=binding['sourceUniverse']:
        raise C.AdmissionError('FIXTURE_NATIVE_IDENTITY')
    # The second registered native-context domain, with its own closure-join table
    # (rustcDevLlvmDigest -> kind rust-dev-llvm), over retained small trees.
    llvm=add('closure',kind='rust-dev-llvm',manifestDigest=blob(b'fixture-llvm-manifest'),
             tree=tree({'lib/librustc_driver.so':b'\x7fELF fixture\n'}),semanticVersion='1.83.0',protocolMajor=3,platform='macos-aarch64')
    rust_tools=add('closure',kind='toolchain',manifestDigest=blob(b'fixture-cargo-manifest'),
             tree=tree({'bin/cargo':b'#!fixture-cargo\n','bin/rustc':b'#!fixture-rustc\n'}),semanticVersion='1.83.0',protocolMajor=3,platform='macos-aarch64')
    rust=copy.deepcopy(NATIVE_FIXTURES['rustContextOfferedAsTypescript'])
    rust['configProjection']={'schemaVersion':2,'honoredKeys':[],'strippedKeys':[],'replacedSnapshotConfigs':[],
        'rustflags':{'honored':[],'stripped':[],'executableSelected':False},'ancestorCarrierVerified':True,
        'cargoHome':'private-empty','environmentProjection':'none','claimsCargoSwitch':False,
        'projectionSha256':hashlib.sha256(b'fixture-cargo-config-projection').hexdigest()}
    rust['toolchain']['rustcDevLlvmDigest']=llvm.removeprefix('closure2:')
    rust['toolClosure']['closureId']=rust_tools
    rust_admission=N.admit_native_context('rust',rust,{k:objects[k][1] for k in (llvm,rust_tools)})
    if rust_admission['refusals']:raise C.AdmissionError('FIXTURE_RUST_CONTEXT:'+','.join(rust_admission['refusals']))
    rust_digest=M.native_context_frame('native.context.rust.v2',rust,blobs)
    if rust_digest!=rust_admission['planNativeContextDigest']:raise C.AdmissionError('FIXTURE_RUST_IDENTITY')
    return {'contextDigest':context_digest,'universeDigest':universe_digest,'context':context,'universe':universe,
            'stdlib':stdlib,'toolchain':toolchain,'admission':admission,
            'rustContextDigest':rust_digest,'rustContext':rust,'llvm':llvm,'rustTools':rust_tools}

def build(resolved=True,has_match=False,source_path='a.ts',with_finding=False,stdlib_body=b'declare const es2022: unknown;\n'):
    objects={};blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest
    def add(domain,**fields):
        value={'schemaVersion':2,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
    source=blob(b"export const foo = 1;\n")
    delivery=json.loads((H.parents[1]/'artifacts/delivery.v4.json').read_text())
    cap_recipe=next(v['value'] for v in delivery['derivedFrom']['operations'] if v['path']=='capabilityManifestIdentity')
    cap_bytes=bytes.fromhex(cap_recipe['vectors']['byId']['DCM-1-core']['committedBytesHex'])
    cap_digest=blob(cap_bytes);cap_id=hashlib.sha256(b'opensip.capability-manifest.v1\0'+cap_bytes).hexdigest()
    closure=add('closure',kind='evaluator',manifestDigest=blob(b'fixture-evaluator-manifest'),tree=[],semanticVersion='2.0.0',protocolMajor=3,platform='macos-aarch64')
    native=native_inputs(objects,blobs,add,blob,stdlib_body)
    universe=native['universeDigest']
    inventory=[{'path':source_path,'sha256':source,'bytes':22}]
    config=blob({'analysis':{'profileId':'default','capabilities':['references'],'budget':{'unit':'work-units','limit':1000}},'components':{},'discovery':{},'policy':{},'evidence':{}})
    scope_payload=blob({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})
    vcs=blob({'schemaVersion':2,'kind':'none','commitId':None,'dirty':False,'sourceInventoryDigest':blob(inventory)})
    snapshot=add('snapshot',projectId='prj1-'+'a'*64,sourceInventory=inventory,resolvedConfigDigest=config,scopeDigest=scope_payload,vcsDigest=vcs)
    policy_digest=blob(POLICY);waiver_digest=blob(WAIVERS)
    program=compiled_program(POLICY);program_digest=blob(program)
    spec_payload=blob({'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'references','languageMode':'ts-tsconfig','workspaceRoot':'.','required':True}],'policyPackIds':['fixture.no-consumer'],'parameters':[]})
    grant=blob({'schemaVersion':2,'projectId':'prj1-'+'a'*64,'principals':[{'kind':'first-party','closureId':closure,'ownerSourceDigest':None}],'analysisOperations':['native-analysis','read-source'],'scopeDigest':scope_payload})
    plan=add('plan',snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=[closure],analysisSpecDigest=spec_payload,resolvedConfigDigest=config,nativeContextDigests=sorted({native['contextDigest'],native['rustContextDigest']}),importIds=[],policyDigest=policy_digest,waiverDigest=waiver_digest,scopeDigest=scope_payload,budget={'unit':'work-units','limit':1000},semanticGrantDigest=grant)
    scope=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation='references',resolution='resolved-binding',enumeratorClosure=closure,subjects=['foo'])
    coverage_schema=blob(COVERAGE_PAYLOAD_SCHEMA);fact_schema=blob(FACT_PAYLOAD_SCHEMA)
    coverage=add('coverage',scopeId=scope,payloadSchemaDigest=coverage_schema,payloadDigest=blob({'examined':True,'resolved':resolved,'closed':True}))
    facts=[]
    if has_match:
        facts=[add('fact',snapshotId=snapshot,relation='references',resolution='resolved-binding',sourceUniverse=universe,targetUniverse=universe,producerClosure=closure,payloadSchemaDigest=fact_schema,payloadDigest=blob({'target':'foo'}),anchors=[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':21}],confidenceMillionths=1000000)]
    view=add('view',planId=plan,scopeIds=[scope],facts=facts,coverageIds=[coverage],producerClosure=closure,schemaDigests=sorted({coverage_schema,fact_schema}))
    stage_spec=blob({'schemaVersion':2,'planId':plan,'producerClosure':closure,'operation':'derive-references-view','parameters':[],'outputDomains':['view'],'outputSchemaDigest':blob(STAGE_OUTPUT_SCHEMA)})
    execution=add('execution-plan',planId=plan,stages=[{'ordinal':0,'stageSpecDigest':stage_spec,'requires':[],'outputDomains':['view']}])
    program_predicate=blob({'schemaVersion':2,'ruleProgramDigest':program_digest,'ruleId':'no-consumer','predicateId':'p','operation':'none','nodeDigest':hashlib.sha256(C.canonical(ATOM)).hexdigest()})
    witness=blob({'schemaVersion':2,'programPredicateDigest':program_predicate,'matchingFactIds':facts,'coverageIds':[coverage],'countLimit':None,'childPredicateIds':[]})
    value='false' if has_match else ('true' if resolved else 'indeterminate')
    verdict='fail' if value=='true' else ('pass' if value=='false' else 'indeterminate')
    finding_ids=[]
    if with_finding:
        fingerprint=add('finding-fingerprint',ruleStableId='no-consumer',detectorSemanticsMajor=2,
            subjectKey={'language':'typescript','kind':'symbol','logicalPath':source_path,'qualifiedName':'foo','discriminator':'one'},relatedSubjectKeys=[])
        parameters=blob({'schemaVersion':2,'messageCode':'no-consumer','parameters':{'subject':'foo','count':0,'exported':True}})
        finding_ids=[add('finding',fingerprint=fingerprint,ruleClosure=closure,subjectId='foo',messageCode='no-consumer',
            parameterDigest=parameters,severity='error',evidenceRefs=[{'domain':'predicate-witness','digest':witness}])]
    proof=add('proof-bundle',planId=plan,executionPlanId=execution,evaluatorClosure=closure,ruleProgramDigest=program_digest,evaluationInputRefs=[{'domain':'view','digest':view.split(':')[1]}],predicateProofs=[{'ruleId':'no-consumer','subjectId':'foo','predicateId':'p','operation':'none','inputRefs':[{'domain':'view','digest':view.split(':')[1]}],'scopeIds':[scope],'value':value,'witnessDigest':witness}],findingIds=finding_ids,verdict=verdict)
    evidence=add('semantic-evidence',planId=plan,viewIds=[view],coverageIds=[coverage],importIds=[],findingIds=finding_ids,proofBundleId=proof)
    seal=add('evaluation-seal',planId=plan,executionPlanId=execution,evidenceId=evidence,evaluatorClosure=closure,policyDigest=policy_digest,proofBundleId=proof,verdict=verdict)
    run={'schemaVersion':2,'projectId':'prj1-'+'a'*64,'snapshotId':snapshot,'planId':plan,'evidenceId':evidence,'evaluationSealId':seal,'capabilityManifestId':cap_id}
    return run,objects,blobs

def rekey(objects,old,changed,run):
    domain=objects[old][0];new=M.identifier(domain,changed);objects.pop(old);objects[new]=(domain,changed)
    def replace(x):
        if type(x) is str:return new if x==old else x
        if type(x) is list:return [replace(y) for y in x]
        if type(x) is dict:
            if set(x)=={'domain','digest'} and x['domain']==domain and x['digest']==old.split(':')[1]:return {'domain':domain,'digest':new.split(':')[1]}
            return {k:replace(v) for k,v in x.items()}
        return x
    # Propagate all direct identities upward. Used to make self-consistent hostile claims.
    while True:
        changed=next(((key,replace(v)) for key,(d,v) in objects.items() if replace(v)!=v),None)
        if changed is None:break
        rekey(objects,changed[0],changed[1],run)
    run.update(replace(run))
    return new

def put_blob(blobs,value):
    raw=value if type(value) is bytes else C.canonical(value);digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest

def rekey_plan(objects,blobs,run,plan):
    """Re-mint plan2 and re-derive the stage spec that names it. The stage-spec planId join is
    real: a plan re-mint that left an old stage spec behind would not close."""
    rekey(objects,run['planId'],plan,run)
    ekey=objects[run['evaluationSealId']][1]['executionPlanId'];execution=copy.deepcopy(objects[ekey][1])
    spec=C.parse(blobs[execution['stages'][0]['stageSpecDigest']]);spec['planId']=run['planId']
    execution['stages'][0]['stageSpecDigest']=put_blob(blobs,spec)
    rekey(objects,ekey,execution,run)

def graph_with_import(correspondence='exact', foreign_snapshot=False, bad_mapping=False, dirty=False, missing_mapping=False, build_identity=None, declared_builds=None):
    """Actual typed importer -> self-consistent Run graph. Synthetic payload/source observations
    only; this builder supplies no expected verdict."""
    run,objects,blobs=build(resolved=True,has_match=True)
    put=lambda value:put_blob(blobs,value)
    if correspondence=='vcs':
        sid=run['snapshotId'];snap=copy.deepcopy(objects[sid][1]);vcs=C.parse(blobs[snap['vcsDigest']])
        vcs.update(kind='git',commitId='a'*40,dirty=dirty);snap['vcsDigest']=put(vcs);rekey(objects,sid,snap,run)
        pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1]);view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
        witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']]);witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds']);proof['predicateProofs'][0]['witnessDigest']=put(witness);rekey(objects,pk,proof,run)
    closure=objects[run['planId']][1]['semanticClosures'][0]
    target='snapshot2:'+'f'*64 if foreign_snapshot else run['snapshotId']
    corr={'kind':'exact-snapshot','snapshotId':target}
    if correspondence=='vcs':
        item=objects[run['snapshotId']][1]['sourceInventory'][0]
        mapping={'schemaFamily':'opensip.product.source-mapping','schemaMajor':1,'snapshotId':target,'producerClosure':closure,
                 'entries':[{'generatedPath':'a.js','generatedSha256':'b'*64,'sourcePath':item['path'],'sourceSha256':'f'*64 if bad_mapping else item['sha256']}]}
        corr={'kind':'vcs-revision','vcsRevision':{'system':'git','commit':'a'*40,'dirty':dirty},'buildIdentity':build_identity,
              'sourceMappingDigest':None if missing_mapping else put(mapping)}
    wf=C.parse((H.parent/'workflows/workflow-cases.v1.json').read_bytes())
    def sub(value):
        if isinstance(value,str) and value.startswith('$'):return wf['constants'][value[1:]]
        if isinstance(value,list):return [sub(v) for v in value]
        if isinstance(value,dict):return {k:sub(v) for k,v in value.items()}
        return value
    payload=sub(wf['runtimePayload']);payload['subjects']=[]
    scope={'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]}
    schemas={domain:(H.parent/row['schemaDocument']).read_bytes() for (_,domain),row in W.PAYLOAD_REGISTRY.items()}
    record=W.build_import('runtime',payload,payload['payloadDomain'],schemas,corr,closure,closure,[],scope,{})
    imp=record['wrapper'];put(schemas[payload['payloadDomain']]);put(payload)
    for raw in record['retainedPreimages'].values():put(raw)
    iid=M.identifier('import',imp);objects[iid]=('import',imp)
    plan=copy.deepcopy(objects[run['planId']][1]);plan['importIds']=[iid]
    grant=C.parse(blobs[plan['semanticGrantDigest']]);grant['analysisOperations']=sorted(set(grant['analysisOperations'])|{'read-import'});plan['semanticGrantDigest']=put(grant)
    if declared_builds is not None:
        analysis=C.parse(blobs[plan['analysisSpecDigest']]);analysis['parameters']=[{'schemaDigest':put((H/'import-source-context.schema.json').read_bytes()),'payloadDigest':put({'schemaVersion':1,'declaredBuildIds':declared_builds})}];plan['analysisSpecDigest']=put(analysis)
    rekey_plan(objects,blobs,run,plan)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    proof['evaluationInputRefs']=sorted(proof['evaluationInputRefs']+[{'domain':'import','digest':iid.split(':')[1]}],key=C.canonical);rekey(objects,pk,proof,run)
    ek=run['evidenceId'];evidence=copy.deepcopy(objects[ek][1]);evidence['importIds']=[iid];rekey(objects,ek,evidence,run)
    return run,objects,blobs
