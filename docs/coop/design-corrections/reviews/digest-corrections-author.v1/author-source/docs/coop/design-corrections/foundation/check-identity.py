"""Independent finite-relation replay and identity/lifecycle adversarial examples.
Not a full native protocol implementation or an OS durability qualification.
"""
import argparse,copy,hashlib,importlib.util,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('idmodel',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
W=load('identity_check_workflows',H.parent/'workflows/workflows_model.v1.py')
N=load('identity_check_native',H.parent/'native/native_evidence_model.v2.py')
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']
results=[]
def check(name,value):
    results.append({'id':name,'passed':bool(value)})
def rejects(name,fn):
    try:fn()
    except (ValueError,KeyError,TypeError,C.ValidationError):check(name,True)
    else:check(name,False)

# --------------------------------------------------------------------------- the closed policy DSL
# The fixture rule is a real PolicyDocumentV1 / RuleProgramV1 in the workflow contract's own closed
# DSL. Only the fixture INTERPRETER is small: it evaluates the single-atom subset below. There is no
# second policy language anywhere in the identity unit.
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

# The TypeScript context's config graph and lockfile are repository sources, so they must be in the
# snapshot inventory. identity-and-evidence section 3 already required snapshot/native-context source
# correspondence to agree; these are the rows that discharge it.
TS_SOURCES={'tsconfig.base.json':b'{"compilerOptions":{"target":"es2022"}}\n',
            'tsconfig.json':b'{"extends":"./tsconfig.base.json"}\n',
            'package-lock.json':b'{"lockfileVersion":3}\n'}

def native_inputs(objects,blobs,add,blob,stdlib_body=b'declare const es2022: unknown;\n'):
    """One admitted TypeScript native context and its universe, and one admitted Rust context,
    through the ACTUAL native admission functions, over retained (small) compiler and stdlib
    closure trees. A context the native boundary refuses cannot be re-framed into a Run."""
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
    context['lockfileIdentity']={'kind':'package-lock','path':'package-lock.json',
                                 'contentSha256':hashlib.sha256(TS_SOURCES['package-lock.json']).hexdigest()}
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
    inventory=sorted([{'path':source_path,'sha256':source,'bytes':22}]+
        [{'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in TS_SOURCES.items()],key=lambda r:r['path'].encode())
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

def replay(plan,objects,blobs,evaluation_refs):
    """Trusted reference adapter for this deliberately small rule fixture.
    Reads the ADMITTED PolicyDocumentV1, compiles it independently, addresses the predicate node
    itself, and reads the actual complete views. It never reads a claimed outcome, a claimed
    program-predicate digest or a claimed witness. The production declarative interpreter and the
    native/relation payload schema registries are separate gates.
    """
    pid=M.identifier('plan',plan)
    policy=C.parse(blobs[plan['policyDigest']]);program=compiled_program(policy)
    program_digest=hashlib.sha256(C.canonical(program)).hexdigest()
    rule=next(r for r in program['rules'] if r['ruleId']=='no-consumer')
    node=M.predicate_node_at(rule['emitWhen'],'p')
    if node['op']!='none' or len(node['filters'])!=1:raise C.AdmissionError('FIXTURE_RULE_SUBSET')
    field,value_wanted=node['filters'][0]['field'],node['filters'][0]['value']
    views=[('view2:'+r['digest'],objects['view2:'+r['digest']][1]) for r in evaluation_refs if r['domain']=='view']
    if len(views)!=1:raise C.AdmissionError('FIXTURE_INPUT_SET')
    vid,view=views[0];matches=[];complete=True
    for fid in view['facts']:
        fact=objects[fid][1];payload=C.parse(blobs[fact['payloadDigest']])
        if fact['relation']==node['relation'] and C.equal_typed(payload.get(field),value_wanted):matches.append(fid)
    for cid in view['coverageIds']:
        coverage=objects[cid][1];payload=C.parse(blobs[coverage['payloadDigest']])
        complete=complete and all(payload[x] is True for x in ['examined','resolved','closed'])
    # Independent truth table; do not call the model's predicate helper.
    value='false' if matches else ('true' if complete else 'indeterminate')
    verdict={'true':'fail','false':'pass','indeterminate':'indeterminate'}[value]
    execution=[k for k,(d,v) in objects.items() if d=='execution-plan' and v['planId']==pid]
    findings=sorted(k for k,(d,v) in objects.items() if d=='finding')
    program_predicate={'schemaVersion':2,'ruleProgramDigest':program_digest,'ruleId':'no-consumer','predicateId':'p',
                       'operation':node['op'],'nodeDigest':hashlib.sha256(C.canonical(node)).hexdigest()}
    witness={'schemaVersion':2,'programPredicateDigest':hashlib.sha256(C.canonical(program_predicate)).hexdigest(),
             'matchingFactIds':sorted(matches),'coverageIds':view['coverageIds'],'countLimit':None,
             'childPredicateIds':M.predicate_child_addresses(node,'p')}
    return {'schemaVersion':2,'planId':pid,'executionPlanId':execution[0],'evaluatorClosure':plan['semanticClosures'][0],'ruleProgramDigest':program_digest,'evaluationInputRefs':[{'domain':'view','digest':vid.split(':')[1]}],'predicateProofs':[{'ruleId':'no-consumer','subjectId':'foo','predicateId':'p','operation':node['op'],'inputRefs':[{'domain':'view','digest':vid.split(':')[1]}],'scopeIds':view['scopeIds'],'value':value,'witnessDigest':hashlib.sha256(C.canonical(witness)).hexdigest()}],'findingIds':findings,'verdict':verdict}

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

def resync_stage_spec(objects,blobs,run):
    """Re-derive the retained stage spec after anything re-mints plan2. rekey() rewrites typed
    objects only, so a stage spec left behind in blobs would still name the old Plan; a graph that
    refused on that staleness would not be evidence about the mutation under test."""
    ekey=objects[run['evaluationSealId']][1]['executionPlanId'];execution=copy.deepcopy(objects[ekey][1])
    spec=C.parse(blobs[execution['stages'][0]['stageSpecDigest']])
    if spec['planId']==run['planId']:return
    spec['planId']=run['planId']
    execution['stages'][0]['stageSpecDigest']=put_blob(blobs,spec)
    rekey(objects,ekey,execution,run)

def rekey_plan(objects,blobs,run,plan):
    """Re-mint plan2 and re-derive the stage spec that names it. The stage-spec planId join is
    real: a plan re-mint that left an old stage spec behind would not close."""
    rekey(objects,run['planId'],plan,run)
    resync_stage_spec(objects,blobs,run)

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

for resolved in [True,False]:
    for match in [True,False]:
        run,objects,blobs=build(resolved,match);store=M.EvidenceStore()
        rid=store.prepare(run,objects,blobs,'exec1_11111111111111111111111111111111',replay)
        check('valid-replay-%s-%s'%(resolved,match),rid==M.identifier('run',run))
        check('commit-%s-%s'%(resolved,match),store.commit('exec1_11111111111111111111111111111111')=='committed')
        seal=objects[run['evaluationSealId']][1]
        check('expected-verdict-%s-%s'%(resolved,match),seal['verdict']==('pass' if match else ('fail' if resolved else 'indeterminate')))
run,objects,blobs=build(source_path='run2:literal-filename')
check('logical-filename-is-not-an-identity-reference',M.close_run(run,objects,blobs)==M.identifier('run',run))
run,objects,blobs=build()
rejects('caller-verified-boolean-rejected',lambda:M.EvidenceStore().prepare(run,objects,blobs,'exec1_22222222222222222222222222222222',True))
rejects('wrong-project',lambda:M.close_run({**run,'projectId':'prj1-'+'b'*64},objects,blobs))
rejects('missing-blob',lambda:M.close_run(run,objects,{}))
bad=copy.deepcopy(blobs);first=next(iter(bad));bad[first]=b'corrupt'
rejects('corrupt-blob',lambda:M.close_run(run,objects,bad))
bad=copy.deepcopy(objects);pid=run['planId'];bad[pid][1]['policyDigest']='f'*64
rejects('unchanged-id-edited-plan',lambda:M.close_run(run,bad,blobs))
# Rehash a false proof, evidence, seal, and Run: identity consistency cannot pass replay.
run,bad,blobs=build();proof_id=bad[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(bad[proof_id][1]);proof['predicateProofs'][0]['value']='false'
rekey(bad,proof_id,proof,run)
rejects('self-consistently-rehashed-false-proof',lambda:M.EvidenceStore().prepare(run,bad,blobs,'exec1_22222222222222222222222222222222',replay))
for op,match,coverage,limit,expected in [('none',[],'complete',None,'true'),('none',[],'unknown',None,'indeterminate'),('exists',['f'],'unknown',None,'true'),('exists',[],'unknown',None,'indeterminate'),('count-at-most',['f'],'unknown',0,'false'),('count-at-most',[],'unknown',0,'indeterminate'),('count-at-most',[],'complete',0,'true'),('all-covered',[],'unknown',None,'indeterminate')]:
    check('predicate-'+op+'-'+str(match)+'-'+coverage,M.predicate(op,match,coverage,limit)==expected)
for op,values,expected in [('and',['false','indeterminate'],'false'),('and',['true','indeterminate'],'indeterminate'),('or',['true','indeterminate'],'true'),('not',['indeterminate'],'indeterminate')]:check('kleene-'+op+str(values),M.boolean(op,values)==expected)
for fault,expected in [('before-blobs','operational-failed'),('before-ledger','operational-failed'),('after-ledger-before-ack','durability-undetermined'),(None,'committed')]:
    run,objects,blobs=build();store=M.EvidenceStore();rid=store.prepare(run,objects,blobs,'exec1_33333333333333333333333333333333',replay)
    check('crash-'+str(fault),store.commit('exec1_33333333333333333333333333333333',fault)==expected)
    check('publication-'+str(fault),(rid in store.runs)==(fault in [None,'after-ledger-before-ack']))
run,objects,blobs=build();store=M.EvidenceStore();rid=store.prepare(run,objects,blobs,'exec1_33333333333333333333333333333333',replay);store.commit('exec1_33333333333333333333333333333333');original=C.canonical(store.query(rid))
store.prepare(run,objects,blobs,'exec1_44444444444444444444444444444444',replay);store.commit('exec1_44444444444444444444444444444444')
check('retry-same-run-new-attempt',len(store.runs)==1 and len(store.receipts)==2)
store.pins.add(rid);check('pinned-purge-refuses',store.purge(rid)=='pinned');check('explicit-purge-revokes-pin',store.purge(rid,True)=='purged' and rid not in store.pins)
check('purge-does-not-rewrite-run',C.canonical(store.query(rid))==original)
check('purged-required-evidence-refuses',store.query(rid,True)=='precondition-failed')
check('query-creates-no-run',len(store.runs)==1 and len(store.receipts)==2)
# Each declared semantic domain must reject unknown fields and schema 2.0.
for key,(domain,value) in objects.items():
    rejects('closed-'+domain,lambda d=domain,v=value:M.identifier(d,{**v,'unknown':0}))
    rejects('exact-version-'+domain,lambda d=domain,v=value:M.identifier(d,{**v,'schemaVersion':2.0}))
for state,choice,ephemeral,expected in [('detected',False,False,False),('detected',True,False,True),('detected',False,True,True),('unknown',False,False,True),('not-detected',False,False,True)]:
    check('storage-choice-'+str((state,choice,ephemeral)),M.storage_admission(state,choice,ephemeral)['admitted'] is expected)
check('backup-unknown-not-negative',M.storage_admission('unknown')['backupDisclosure']=='unknown')

# Actual Claude review MF-1..3: independent hostile closure mutations.
def bad_aux(field,value):
    run,objects,blobs=build();plan=copy.deepcopy(objects[run['planId']][1]);plan[field]=put_blob(blobs,value)
    rekey_plan(objects,blobs,run,plan);return M.close_run(run,objects,blobs)
for field in ['scopeDigest','analysisSpecDigest','semanticGrantDigest','resolvedConfigDigest','policyDigest','waiverDigest']:
    rejects('review-aux-not-json-'+field,lambda f=field:bad_aux(f,b'\x00not-json'))
    rejects('review-aux-empty-object-'+field,lambda f=field:bad_aux(f,{}))
run,objects,blobs=build();grant=C.parse(blobs[objects[run['planId']][1]['semanticGrantDigest']]);grant['projectId']='prj1-'+'b'*64
rejects('review-grant-wrong-project',lambda:bad_aux('semanticGrantDigest',grant))

def proof_mutation(fn):
    run,objects,blobs=build();key=objects[run['evaluationSealId']][1]['proofBundleId'];value=copy.deepcopy(objects[key][1]);fn(value,objects,blobs)
    rekey(objects,key,value,run);return M.close_run(run,objects,blobs)
for domain in ['run','evaluation-seal','semantic-evidence','proof-bundle','plan']:
    rejects('review-proof-forbidden-ref-'+domain,lambda d=domain:proof_mutation(lambda p,o,b:p['evaluationInputRefs'].append({'domain':d,'digest':'a'*64})))
rejects('review-hidden-predicate-input',lambda:proof_mutation(lambda p,o,b:p.update(evaluationInputRefs=[])))
rejects('review-witness-not-json',lambda:proof_mutation(lambda p,o,b:p['predicateProofs'][0].update(witnessDigest=put_blob(b,b'not-json'))))
def wrong_witness(p,o,b):
    w=C.parse(b[p['predicateProofs'][0]['witnessDigest']]);w['programPredicateDigest']='f'*64;p['predicateProofs'][0]['witnessDigest']=put_blob(b,w)
rejects('review-witness-missing-program',lambda:proof_mutation(wrong_witness))
def extra_coverage():
    run,o,b=build();cid=o[run['evidenceId']][1]['coverageIds'][0];cov=copy.deepcopy(o[cid][1]);cov['payloadDigest']=put_blob(b,{'examined':True,'resolved':False,'closed':True});new=M.identifier('coverage',cov);o[new]=('coverage',cov)
    eid=run['evidenceId'];ev=copy.deepcopy(o[eid][1]);ev['coverageIds']=sorted(set(ev['coverageIds']+[new]));rekey(o,eid,ev,run);return M.close_run(run,o,b)
rejects('review-extra-authoritative-coverage-root',extra_coverage)
def foreign_finding_ref(domain):
    run,o,b=build();foreign,other,bb=build(has_match=True,source_path='foreign.ts');o.update(other);b.update(bb)
    fid=next(k for k,(d,v) in other.items() if d==domain)
    fp={'schemaVersion':2,'ruleStableId':'no-consumer','detectorSemanticsMajor':2,'subjectKey':{'language':'typescript','kind':'symbol','logicalPath':'a.ts','qualifiedName':'foo','discriminator':'one'},'relatedSubjectKeys':[]}
    fk=M.identifier('finding-fingerprint',fp);o[fk]=('finding-fingerprint',fp)
    f={'schemaVersion':2,'fingerprint':fk,'ruleClosure':o[run['planId']][1]['semanticClosures'][0],'subjectId':'foo','messageCode':'unused','parameterDigest':put_blob(b,{'schemaVersion':2,'messageCode':'unused','parameters':{}}),'severity':'error','evidenceRefs':[{'domain':domain,'digest':fid.split(':')[1]}]}
    fkey=M.identifier('finding',f);o[fkey]=('finding',f)
    pk=o[run['evaluationSealId']][1]['proofBundleId'];p=copy.deepcopy(o[pk][1]);p['findingIds']=[fkey];rekey(o,pk,p,run)
    ek=run['evidenceId'];e=copy.deepcopy(o[ek][1]);e['findingIds']=[fkey];rekey(o,ek,e,run);return M.close_run(run,o,b)
rejects('review-finding-foreign-fact',lambda:foreign_finding_ref('fact'))
rejects('review-finding-forbidden-seal',lambda:foreign_finding_ref('evaluation-seal'))
# Project adoption is a separate custody act and never copies operational authority.
a='prj1-'+'a'*64;b='prj1-'+'b'*64
check('project-first-use',M.project_identity_admit(None,None,new_id=a)['projectId']==a)
check('project-agreement',M.project_identity_admit(a,a)['action']=='reuse')
for carrier,registry in [(a,None),(None,a),(a,b)]:rejects('project-unilateral-or-conflict-'+str((carrier,registry)),lambda c=carrier,r=registry:M.project_identity_admit(c,r))
check('project-explicit-adopt-no-operational-state',M.project_identity_admit(a,None,'adopt')=={'projectId':a,'action':'register-existing','importsCredentials':False,'importsOperationalState':False})
check('project-explicit-move',M.project_identity_admit(a,None,'move')['projectId']==a)
check('project-fork-new-id',M.project_identity_admit(a,a,'fork',b)['projectId']==b)
rejects('project-fork-cannot-reuse-id',lambda:M.project_identity_admit(a,a,'fork',a))
check('subject-stable-discriminator',M.subject_discriminator(['fn','foo','()'],[['fn','foo','()']])==hashlib.sha256(C.canonical(['fn','foo','()'])).hexdigest())
rejects('subject-ambiguous-no-encounter-suffix',lambda:M.subject_discriminator(['fn'],[['fn'],['fn']]))
run,o,b=build();store=M.EvidenceStore();eid='exec1_'+'9'*32;rid=store.prepare(run,o,b,eid,replay)
check('read-only-recovery-before-ledger',store.recover(eid)['state']=='uncommitted')
store.commit(eid,'after-ledger-before-ack');sealed=C.canonical(store.receipts[0]);runbytes=C.canonical(store.runs[rid])
check('read-only-recovery-after-lost-ack',store.recover(eid)['state']=='committed' and not store.recover(eid)['effectsRepeated'])
for i,state in enumerate(['partial','expired','corrupt','unavailable','purged'],1):
    value=store.set_availability(rid,state,[],state)
    check('availability-'+state,value['generation']==i and store.query(rid,True)=='precondition-failed')
check('sealed-assurance-and-run-immutable',C.canonical(store.receipts[0])==sealed and C.canonical(store.runs[rid])==runbytes)
bad=copy.deepcopy(b);bad[next(iter(bad))]=b'corrupt'
rejects('regeneration-corrupt-bytes-refuse',lambda:store.restore(rid,o,bad,replay))
try:
    store.restore(rid,o,b,lambda *args: {})
except M.RegenerationMismatch as exc:
    check('regeneration-mismatch-public-operational-detail',exc.termination['errorCode']=='HOST.IO_FAILURE' and exc.termination['domainDetail']['code']=='evidence.regeneration-mismatch' and C.canonical(store.runs[rid])==runbytes)
else:check('regeneration-mismatch-public-operational-detail',False)
check('verified-restoration-preserves-run',store.restore(rid,o,b,replay)['state']=='retained' and C.canonical(store.runs[rid])==runbytes)
rejects('attempt-id-reuse-refused',lambda:store.prepare(run,o,b,eid,replay))
# The closure's import source gate is exercised using the actual typed importer.
check('review-import-exact-source',M.close_run(*graph_with_import()).startswith('run2:'))
rejects('review-import-foreign-exact-source',lambda:M.close_run(*graph_with_import(foreign_snapshot=True)))
check('review-import-current-vcs-mapping',M.close_run(*graph_with_import(correspondence='vcs')).startswith('run2:'))
check('review-import-declared-build-context',M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a',declared_builds=['build-a'])).startswith('run2:'))
rejects('review-import-build-label-cannot-self-authorize',lambda:M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a')))
rejects('review-import-wrong-build-context',lambda:M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a',declared_builds=['build-b'])))
for kw in ({'foreign_snapshot':True},{'bad_mapping':True},{'dirty':True},{'missing_mapping':True}):
    rejects('review-import-vcs-refused-'+str(kw),lambda kwargs=kw:M.close_run(*graph_with_import(correspondence='vcs',**kwargs)))
def bad_preparation_operation():
    rr,oo,bb=build();pk=rr['planId'];pp=copy.deepcopy(oo[pk][1]);gg=C.parse(bb[pp['semanticGrantDigest']]);gg['analysisOperations'].append('prepare-code');gg['analysisOperations'].sort();raw=C.canonical(gg);dg=hashlib.sha256(raw).hexdigest();bb[dg]=raw;pp['semanticGrantDigest']=dg;rekey_plan(oo,bb,rr,pp);return M.close_run(rr,oo,bb)
rejects('review-prepare-operation-needs-consumed-principal',bad_preparation_operation)
# Blind B M3/S3: annotation admission is distinct from the pure encoder.
check('array-encoder-closing-default-is-sequence',C.canonical(['z','a','z'])==b'["z","a","z"]')
for order,positive,negative in [
    ('canonical-set',['a','z'],['z','a']),
    ('path',[{'path':'a'},{'path':'b'}],[{'path':'a','bytes':1},{'path':'a','bytes':2}]),
    ('numeric',[2,10],[10,2]),
    ('ordinal',[{'ordinal':0},{'ordinal':1}],[{'ordinal':1}]),
    ('predicate',[{'ruleId':'a','subjectId':'z','predicateId':'p'},{'ruleId':'b','subjectId':'a','predicateId':'p'}],[{'ruleId':'a','subjectId':'z','predicateId':'p'},{'ruleId':'a','subjectId':'z','predicateId':'p'}]),
    ('ruleId',[{'ruleId':'a'},{'ruleId':'b'}],[{'ruleId':'b'},{'ruleId':'a'}]),
    ('waiverId',[{'waiverId':'a'},{'waiverId':'b'}],[{'waiverId':'a'},{'waiverId':'a'}])]:
    schema={'type':'array','x-opensip-order':order}
    C.validate(schema,positive);check('array-order-positive-'+order,True)
    rejects('array-order-refused-'+order,lambda schema=schema,negative=negative:C.validate(schema,negative))
rr,oo,bb=build();snap=copy.deepcopy(oo[rr['snapshotId']][1]);dup=dict(snap['sourceInventory'][0],sha256='f'*64);snap['sourceInventory'].append(dup)
rejects('inventory-duplicate-path-different-bytes-refused',lambda:M.identifier('snapshot',snap))

# =========================================================================================
# NEW-MUST-1 / NEW-ADV-2: the closing digest law. Every 64-hex field in the bundle declares its
# representation; the closure checker dispatches on that annotation, never on a field NAME.
# =========================================================================================
SCHEMA=M.SCHEMA;HEXPAT='^[0-9a-f]{64}(?![\\s\\S])'
def digest_sites(node,path,out):
    if type(node) is dict:
        if node.get('pattern')==HEXPAT or node.get('$ref')=='#/$defs/Hash':
            out.append((path,node.get('x-opensip-digest')));return
        for key,child in node.items():
            digest_sites(child,path if key in ('properties','items','$defs','oneOf','additionalProperties') else path+'/'+key,out)
    elif type(node) is list:
        for child in node:digest_sites(child,path,out)
sites=[]
for name,node in SCHEMA['$defs'].items():
    if name!='Hash':digest_sites(node,name,sites)
check('digest-law-covers-every-64-hex-field',sites and all(a is not None for _,a in sites))
check('digest-law-has-no-unregistered-representation',
      {a['representation'] for _,a in sites if a}<= {'raw-artifact','canonical-record','h-identity','capability-manifest-id','by-domain'})
for field in ['programPredicateDigest','parameterDigest','stageSpecDigest','outputSchemaDigest','inventoryDigest']:
    check('digest-law-names-'+field,any(p.endswith('/'+field) and a is not None for p,a in sites))
check('digest-law-stage-spec-is-one-record-two-sites',
      len([p for p,a in sites if p.endswith('/stageSpecDigest')])==2 and
      len({C.canonical(a) for p,a in sites if p.endswith('/stageSpecDigest')})==1)
check('digest-law-registry-domains-cover-every-ref-enum',
      set(SCHEMA['$defs']['Ref']['properties']['domain']['enum'])<=set(M.DIGESTS['byDomain']))
for name in ['program-predicate','finding-parameters','stage-spec','commit-inventory','source-inventory','owner-source-set']:
    check('digest-law-record-registered-'+name,name in SCHEMA['$defs'])

# --- an independent canonical encoder, written here and not calling canonical.py -------------
def indep(value):
    if value is True:return b'true'
    if value is False:return b'false'
    if value is None:return b'null'
    if type(value) is int:return str(value).encode('ascii')
    if type(value) is str:
        out=bytearray(b'"')
        for ch in value:
            if ch=='"':out+=b'\\"'
            elif ch=='\\':out+=b'\\\\'
            elif ch in '\b\t\n\f\r':out+={'\b':b'\\b','\t':b'\\t','\n':b'\\n','\f':b'\\f','\r':b'\\r'}[ch]
            elif ord(ch)<0x20:out+=('\\u%04x'%ord(ch)).encode('ascii')
            else:out+=ch.encode('utf-8')
        return bytes(out+b'"')
    if type(value) is list:return b'['+b','.join(indep(v) for v in value)+b']'
    if type(value) is dict:
        items=sorted(value.items(),key=lambda kv:kv[0].encode('utf-8'))
        return b'{'+b','.join(indep(k)+b':'+indep(v) for k,v in items)+b'}'
    raise TypeError(type(value))
def indep_sha(value):return hashlib.sha256(indep(value)).hexdigest()
def indep_h(domain,value):
    raw=indep(value)
    return hashlib.sha256(b'opensip.product.v1\0'+domain.encode('ascii')+b'\0'+len(raw).to_bytes(8,'big')+raw).hexdigest()
VECTOR_PROGRAM_PREDICATE={'schemaVersion':2,'ruleProgramDigest':'0'*64,'ruleId':'r','predicateId':'p.1','operation':'and','nodeDigest':'1'*64}
VECTOR_FINDING_PARAMETERS={'schemaVersion':2,'messageCode':'m','parameters':{'b':1,'a':'x','c':False}}
VECTOR_STAGE_SPEC={'schemaVersion':2,'planId':'plan2:'+'2'*64,'producerClosure':'closure2:'+'3'*64,'operation':'derive',
                   'parameters':[],'outputDomains':['view'],'outputSchemaDigest':'4'*64}
VECTOR_COMMIT_INVENTORY={'schemaVersion':2,'runId':'run2:'+'5'*64,'objects':['view2:'+'6'*64],'blobDigests':['7'*64]}
VECTOR_OWNER_SOURCE=[{'ownerKey':'a','source':'repository','ownerFileManifestSha256':'8'*64},
                     {'ownerKey':'b','source':'repository','ownerFileManifestSha256':'9'*64}]
# Independently computed values; each literal is reproduced by the encoder above AND by canonical.py.
VECTORS={
 'program-predicate':(VECTOR_PROGRAM_PREDICATE,'d0402034ed9f6e2c4e113e36760a4889ec54b349b0a7951fcceb5bec8f591e09'),
 'finding-parameters':(VECTOR_FINDING_PARAMETERS,'ec8b5959e7d27b01817b6eb830787c8dc02281cf8758f74bcfdf336b25d6a73e'),
 'stage-spec':(VECTOR_STAGE_SPEC,'056a6dbac737e36856e7e6cd6c27aae85869f058bc2ec436511fdf09256553c8'),
 'commit-inventory':(VECTOR_COMMIT_INVENTORY,'d87ef7db470cd9d8531141beddaba1bb0d5ae3b82a07452e1ba7cab0f34c9a0b'),
 'owner-source-set':(VECTOR_OWNER_SOURCE,'c6190a240894608b027e9c85ea4079a55847e66cd010b2090b84b50475a02975'),
}
VECTOR_H_SAMPLE=({'schemaVersion':2,'x':'y'},'337ddc07b6ef1a161c63fc18e4c1a3900ccfc89a87a38952d3fe22740fb2badb',
                 '06786637e56951a14b4ae81e1328fc97914dcec404fb80b14253b89e554c72c5')
for name,(value,expected) in VECTORS.items():
    schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/'+name
    C.validate(schema,value)
    check('digest-vector-independent-encoder-agrees-'+name,indep_sha(value)==hashlib.sha256(C.canonical(value)).hexdigest())
    if expected:check('digest-vector-literal-'+name,indep_sha(value)==expected)
check('digest-vector-records-are-pairwise-distinct',
      len({indep_sha(v) for v,_ in VECTORS.values()})==len(VECTORS))
# Every single-field mutation of the closed records moves the digest.
for name,(value,_) in VECTORS.items():
    base=indep_sha(value)
    if type(value) is dict:
        variants=[{**value,k:(v+1 if type(v) is int and type(v) is not bool else ('z'+str(v) if type(v) is str else v))} for k,v in value.items() if k!='schemaVersion' and type(v) in (int,str)]
    else:
        variants=[[{**value[0],'ownerKey':'z'},value[1]]]
    check('digest-vector-mutation-sensitive-'+name,variants and all(indep_sha(x)!=base for x in variants))
# H frame vs raw canonical payload are different digests and are not interchangeable.
sample={'schemaVersion':2,'x':'y'}
check('h-frame-is-not-raw-canonical-sha',indep_h('native.context.typescript.v2',sample)!=indep_sha(sample))
check('digest-vector-literal-h-frame-and-raw-payload',
      (indep_h('native.context.typescript.v2',sample),indep_sha(sample))==VECTOR_H_SAMPLE[1:] and
      (C.identity('native.context.typescript.v2',sample),hashlib.sha256(C.canonical(sample)).hexdigest())==VECTOR_H_SAMPLE[1:])
check('h-frame-matches-the-joint-recipe',indep_h('native.context.typescript.v2',sample)==C.identity('native.context.typescript.v2',sample))
check('h-frame-preimage-hashes-to-the-identity',
      hashlib.sha256(M.h_preimage_frame('native.context.typescript.v2',sample)).hexdigest()==C.identity('native.context.typescript.v2',sample))

# --- programPredicateDigest: an address into the admitted rule program, not a free digest -----
check('rule-program-compiles-from-the-admitted-policy',
      W.rule_program_digest(POLICY)==hashlib.sha256(C.canonical(compiled_program(POLICY))).hexdigest())
W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/PolicyDocumentV1',POLICY)
W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/RuleProgramV1',compiled_program(POLICY))
check('predicate-address-root-is-the-rule-emit-when',M.predicate_node_at(ATOM,'p') is ATOM)
NESTED={'op':'and','operands':[ATOM,{'op':'not','operand':ATOM}]}
check('predicate-address-operands',M.predicate_node_at(NESTED,'p.1.0') is ATOM and M.predicate_node_at(NESTED,'p.0') is ATOM)
check('predicate-child-addresses',M.predicate_child_addresses(NESTED,'p')==['p.0','p.1'] and M.predicate_child_addresses(NESTED['operands'][1],'p.1')==['p.1.0'])
for bad_address in ['q','p.2','p.01','p.0.0','p.-1','']:
    rejects('predicate-address-refused-'+repr(bad_address),lambda a=bad_address:M.predicate_node_at(NESTED,a))
def witness_mutation(fn):
    run,objects,blobs=build();key=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[key][1])
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    record=C.parse(blobs[witness['programPredicateDigest']])
    fn(proof,witness,record,blobs)
    witness['programPredicateDigest']=put_blob(blobs,record)
    proof['predicateProofs'][0]['witnessDigest']=put_blob(blobs,witness)
    rekey(objects,key,proof,run);return M.close_run(run,objects,blobs)
check('program-predicate-positive-run-closes',witness_mutation(lambda p,w,r,b:None).startswith('run2:'))
rejects('program-predicate-altered-node-digest',lambda:witness_mutation(lambda p,w,r,b:r.update(nodeDigest='f'*64)))
rejects('program-predicate-wrong-operation',lambda:witness_mutation(lambda p,w,r,b:r.update(operation='exists')))
rejects('program-predicate-wrong-address',lambda:witness_mutation(lambda p,w,r,b:r.update(predicateId='p.0')))
rejects('program-predicate-wrong-rule',lambda:witness_mutation(lambda p,w,r,b:r.update(ruleId='other')))
rejects('program-predicate-foreign-rule-program',lambda:witness_mutation(lambda p,w,r,b:r.update(ruleProgramDigest=put_blob(b,compiled_program({**POLICY,'gateSeverityAtLeast':'warning'})))))
rejects('program-predicate-hidden-child',lambda:witness_mutation(lambda p,w,r,b:w.update(childPredicateIds=['p.0'])))
rejects('program-predicate-invented-count-limit',lambda:witness_mutation(lambda p,w,r,b:w.update(countLimit=3)))
def missing_program_predicate_preimage():
    run,objects,blobs=build();key=objects[run['evaluationSealId']][1]['proofBundleId'];proof=objects[key][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    blobs=dict(blobs);blobs.pop(witness['programPredicateDigest']);return M.close_run(run,objects,blobs)
rejects('program-predicate-missing-preimage-is-retention-loss',missing_program_predicate_preimage)
def hidden_rule_program():
    run,objects,blobs=build();pid=run['planId'];plan=copy.deepcopy(objects[pid][1])
    other={**POLICY,'gateSeverityAtLeast':'warning'};plan['policyDigest']=put_blob(blobs,other)
    seal_key=run['evaluationSealId'];seal=copy.deepcopy(objects[seal_key][1]);seal['policyDigest']=plan['policyDigest']
    rekey(objects,seal_key,seal,run);rekey_plan(objects,blobs,run,plan);return M.close_run(run,objects,blobs)
rejects('rule-program-must-compile-from-the-selected-policy',hidden_rule_program)
# The exact NEW-MUST-1 divergence: the second conforming reading now refuses, so one source and
# one policy admit exactly one programPredicateDigest, hence one proof2, evidence2, seal2 and run2.
def h_framed_program_predicate():
    run,objects,blobs=build();key=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[key][1])
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    record=C.parse(blobs[witness['programPredicateDigest']])
    witness['programPredicateDigest']=M.retain_h_identity('rule-program',record,blobs)
    proof['predicateProofs'][0]['witnessDigest']=put_blob(blobs,witness)
    rekey(objects,key,proof,run);return M.close_run(run,objects,blobs)
rejects('program-predicate-h-framed-reading-refused-so-one-reading-remains',h_framed_program_predicate)
run,objects,blobs=build()
witness_record=C.parse(blobs[C.parse(blobs[objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]['predicateProofs'][0]['witnessDigest']])['programPredicateDigest']])
check('program-predicate-two-readings-are-different-digests',
      hashlib.sha256(C.canonical(witness_record)).hexdigest()!=C.identity('rule-program',witness_record))
# A frame is not admissible where a canonical record is required, in either direction.
def frame_where_a_record_is_required():
    run,objects,blobs=build();plan=copy.deepcopy(objects[run['planId']][1])
    spec=C.parse(blobs[plan['analysisSpecDigest']])
    plan['analysisSpecDigest']=M.retain_h_identity('analysis-spec',spec,blobs)
    rekey_plan(objects,blobs,run,plan);return M.close_run(run,objects,blobs)
rejects('h-frame-refused-where-a-canonical-record-is-required',frame_where_a_record_is_required)

# --- parameterDigest ------------------------------------------------------------------------
run,objects,blobs=build(with_finding=True)
check('finding-parameters-positive-run-closes',M.close_run(run,objects,blobs).startswith('run2:'))
def finding_mutation(fn):
    run,objects,blobs=build(with_finding=True);fid=objects[run['evidenceId']][1]['findingIds'][0]
    finding=copy.deepcopy(objects[fid][1]);parameters=C.parse(blobs[finding['parameterDigest']])
    fn(finding,parameters,blobs);finding['parameterDigest']=put_blob(blobs,parameters)
    rekey(objects,fid,finding,run);return M.close_run(run,objects,blobs)
check('finding-parameters-rehashed-record-still-closes',finding_mutation(lambda f,p,b:None).startswith('run2:'))
rejects('finding-parameters-message-code-must-join',lambda:finding_mutation(lambda f,p,b:p.update(messageCode='other')))
rejects('finding-parameters-not-a-registered-record',lambda:finding_mutation(lambda f,p,b:p.pop('parameters')))
rejects('finding-parameters-open-value-type',lambda:finding_mutation(lambda f,p,b:p['parameters'].update(bad=[1])))
def finding_parameters_missing():
    run,objects,blobs=build(with_finding=True);fid=objects[run['evidenceId']][1]['findingIds'][0]
    blobs=dict(blobs);blobs.pop(objects[fid][1]['parameterDigest']);return M.close_run(run,objects,blobs)
rejects('finding-parameters-missing-preimage-is-retention-loss',finding_parameters_missing)

# --- stageSpecDigest and outputSchemaDigest, in the execution plan AND the cache/regen key ----
def stage_mutation(fn):
    run,objects,blobs=build();ekey=objects[run['evaluationSealId']][1]['executionPlanId'];execution=copy.deepcopy(objects[ekey][1])
    spec=C.parse(blobs[execution['stages'][0]['stageSpecDigest']])
    fn(execution,spec,blobs);execution['stages'][0]['stageSpecDigest']=put_blob(blobs,spec)
    rekey(objects,ekey,execution,run);return M.close_run(run,objects,blobs)
check('stage-spec-positive-run-closes',stage_mutation(lambda e,s,b:None).startswith('run2:'))
rejects('stage-spec-output-domains-must-join-the-stage',lambda:stage_mutation(lambda e,s,b:s.update(outputDomains=['fact'])))
rejects('stage-spec-foreign-plan',lambda:stage_mutation(lambda e,s,b:s.update(planId='plan2:'+'f'*64)))
rejects('stage-spec-unselected-producer',lambda:stage_mutation(lambda e,s,b:s.update(producerClosure='closure2:'+'f'*64)))
rejects('stage-spec-hidden-parameter',lambda:stage_mutation(lambda e,s,b:s.update(parameters=[{'schemaDigest':'a'*64,'payloadDigest':'b'*64}])))
rejects('stage-spec-missing-output-schema-bytes',lambda:stage_mutation(lambda e,s,b:s.update(outputSchemaDigest='c'*64)))
def stage_spec_missing_preimage():
    run,objects,blobs=build();ekey=objects[run['evaluationSealId']][1]['executionPlanId']
    blobs=dict(blobs);blobs.pop(objects[ekey][1]['stages'][0]['stageSpecDigest']);return M.close_run(run,objects,blobs)
rejects('stage-spec-missing-preimage-is-retention-loss',stage_spec_missing_preimage)
run,objects,blobs=build()
execution=objects[objects[run['evaluationSealId']][1]['executionPlanId']][1]
stage_digest=execution['stages'][0]['stageSpecDigest'];stage=C.parse(blobs[stage_digest])
scope_id=next(k for k,(d,v) in objects.items() if d=='subject-scope')
cache={'schemaVersion':2,'planId':run['planId'],'producerClosure':stage['producerClosure'],'stageSpecDigest':stage_digest,
       'scopeIds':[scope_id],'inputRefs':[{'domain':'view','digest':'a'*64}],'outputSchemaDigest':stage['outputSchemaDigest']}
cache_id=M.cache_identifier('cache-key',cache,objects,blobs,run['planId'])
regen_id=M.cache_identifier('regeneration-key',cache,objects,blobs,run['planId'])
check('cache-and-regen-share-one-stage-spec-record',cache_id.startswith('cache2:') and regen_id.startswith('regen2:') and cache_id.split(':')[1]!=regen_id.split(':')[1])
check('cache-stage-spec-is-the-same-digest-as-the-execution-plan-stage',cache['stageSpecDigest']==stage_digest)
rejects('cache-output-schema-cannot-diverge-from-the-stage-spec',lambda:M.cache_identifier('cache-key',{**cache,'outputSchemaDigest':'d'*64},objects,blobs,run['planId']))
rejects('cache-producer-cannot-diverge-from-the-stage-spec',lambda:M.cache_identifier('cache-key',{**cache,'producerClosure':'closure2:'+'f'*64},objects,blobs,run['planId']))
rejects('cache-foreign-plan-refused',lambda:M.cache_identifier('cache-key',{**cache,'planId':'plan2:'+'f'*64},objects,blobs,run['planId']))
rejects('cache-missing-stage-spec-bytes',lambda:M.cache_identifier('cache-key',{**cache,'stageSpecDigest':'e'*64},objects,blobs,run['planId']))

# --- commit-receipt inventoryDigest ----------------------------------------------------------
run,objects,blobs=build();store=M.EvidenceStore();eid='exec1_'+'a'*32
store.prepare(run,objects,blobs,eid,replay);store.commit(eid)
receipt=store.receipts[0];inventory=store.inventories[receipt['runId']]
check('receipt-inventory-is-a-registered-closed-record',
      receipt['inventoryDigest']==hashlib.sha256(C.canonical(inventory)).hexdigest() and
      indep_sha(inventory)==receipt['inventoryDigest'])
check('receipt-inventory-names-every-published-object-and-blob',
      set(inventory['objects'])==set(objects) and set(inventory['blobDigests'])==set(blobs) and inventory['runId']==receipt['runId'])
_,dropped=M.commit_inventory(receipt['runId'],{k:v for k,v in list(objects.items())[1:]},blobs)
_,extra=M.commit_inventory(receipt['runId'],objects,{**blobs,'f'*64:b''})
check('receipt-inventory-mutation-sensitive',len({receipt['inventoryDigest'],dropped,extra})==3)

# --- native contexts and semantic universes close through a COMPLETE Run ----------------------
run,objects,blobs=build()
plan=objects[run['planId']][1]
check('native-context-nonempty-plan-closes',plan['nativeContextDigests'] and M.close_run(run,objects,blobs).startswith('run2:'))
LANGUAGE_OF={'native.context.typescript.v2':'typescript','native.context.rust.v2':'rust'}
frames={d:M.parse_h_frame(blobs[d],'native-context') for d in plan['nativeContextDigests']}
retained_closures={k:v for k,(d,v) in objects.items() if d=='closure'}
check('native-context-both-registered-domains-close',
      {domain for domain,_,_ in frames.values()}==set(LANGUAGE_OF))
check('native-context-digest-is-the-native-admission-value',
      all(N.admit_native_context(LANGUAGE_OF[domain],value,retained_closures)['planNativeContextDigest']==digest
          for digest,(domain,value,_) in frames.items()))
def context_payload(blobs,digest):return M.parse_h_frame(blobs[digest],'native-context')[1]
def universe_payload(blobs,digest):return M.parse_h_frame(blobs[digest],'native-semantic-universe')[1]
def native_frame_mutation(fn):
    run,objects,blobs=build();fn(run,objects,blobs);return M.close_run(run,objects,blobs)
def drop_frame(run,objects,blobs):blobs.pop(objects[run['planId']][1]['nativeContextDigests'][0])
rejects('native-context-frame-missing-is-retention-loss',lambda:native_frame_mutation(drop_frame))
def raw_payload_instead_of_frame(run,objects,blobs):
    plan=copy.deepcopy(objects[run['planId']][1])
    context=context_payload(blobs,plan['nativeContextDigests'][0])
    plan['nativeContextDigests']=[put_blob(blobs,context)]     # raw SHA-256 of the canonical payload
    rekey_plan(objects,blobs,run,plan)
rejects('native-context-raw-payload-sha-is-not-an-h-identity',lambda:native_frame_mutation(raw_payload_instead_of_frame))
def foreign_domain_frame(run,objects,blobs):
    plan=copy.deepcopy(objects[run['planId']][1])
    context=context_payload(blobs,plan['nativeContextDigests'][0])
    plan['nativeContextDigests']=[M.retain_h_identity('native.context.made-up.v2',context,blobs)]
    rekey_plan(objects,blobs,run,plan)
rejects('native-context-unregistered-h-domain-refused',lambda:native_frame_mutation(foreign_domain_frame))
def truncated_frame(run,objects,blobs):
    digest=objects[run['planId']][1]['nativeContextDigests'][0]
    frame=blobs[digest];blobs[digest]=frame[:-1]
rejects('native-context-frame-bytes-must-hash-to-the-identity',lambda:native_frame_mutation(truncated_frame))
def unretained_stdlib_closure(run,objects,blobs):
    key=next(k for k,(d,v) in objects.items() if d=='closure' and v['kind']=='stdlib');objects.pop(key)
rejects('native-context-stdlib-closure-must-be-retained',lambda:native_frame_mutation(unretained_stdlib_closure))
def unretained_tool_closure(run,objects,blobs):
    key=next(k for k,(d,v) in objects.items() if d=='closure' and v['kind']=='toolchain');objects.pop(key)
rejects('native-context-tool-closure-must-be-retained',lambda:native_frame_mutation(unretained_tool_closure))
def dropped_context(run,objects,blobs):
    plan=copy.deepcopy(objects[run['planId']][1]);plan['nativeContextDigests']=[];rekey_plan(objects,blobs,run,plan)
rejects('universe-context-must-stay-plan-selected-when-the-plan-drops-it',lambda:native_frame_mutation(dropped_context))
def unretained_extra_context(run,objects,blobs):
    plan=copy.deepcopy(objects[run['planId']][1])
    plan['nativeContextDigests']=sorted(plan['nativeContextDigests']+['f'*64]);rekey_plan(objects,blobs,run,plan)
rejects('plan-named-context-without-a-retained-frame-refuses',lambda:native_frame_mutation(unretained_extra_context))
def universe_not_bound_to_a_selected_context(run,objects,blobs):
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=universe_payload(blobs,objects[scope_key][1]['sourceUniverse'])
    universe['nativeContextId']='sha256:'+'f'*64
    scope=copy.deepcopy(objects[scope_key][1])
    scope['sourceUniverse']=scope['targetUniverse']=M.retain_h_identity('native.semantic-universe.typescript.v2',universe,blobs)
    rekey(objects,scope_key,scope,run)
rejects('universe-must-bind-a-plan-selected-native-context',lambda:native_frame_mutation(universe_not_bound_to_a_selected_context))
# A changed stdlib byte moves the context identity, the universe identity and the Run.
one=build();two=build(stdlib_body=b'declare const es2022: never;\n')
check('changed-stdlib-byte-moves-context-universe-and-run',
      one[1][one[0]['planId']][1]['nativeContextDigests']!=two[1][two[0]['planId']][1]['nativeContextDigests'] and
      M.close_run(*one)!=M.close_run(*two))

# --- Codex probe v7: a context the NATIVE boundary refuses must not be re-frameable into a Run ---
# Frame admission proves retention, never admission. Run closure re-runs the owning contract's own
# admit_native_context / bind_typescript_universe over the retained frame and retained closures.
def rejects_because(name,fn,token):
    try:fn()
    except (ValueError,KeyError,TypeError,C.ValidationError) as exc:check(name,token in str(exc))
    else:check(name,False)

def reframe_context(mutate=lambda c:None,mutate_universe=None):
    """Fully re-frame and re-key a complete Run around a mutated TypeScript context: new context
    frame, new universe frame bound to it, re-keyed scope/coverage/view/proof/seal/evidence and a
    rebuilt witness and stage spec. A refusal here is a refusal of the mutation, not of staleness."""
    run,objects,blobs=build()
    plan=copy.deepcopy(objects[run['planId']][1])
    ts=next(d for d in plan['nativeContextDigests']
            if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')
    context=M.parse_h_frame(blobs[ts],'native-context')[1];mutate(context)
    new_context=M.retain_h_identity('native.context.typescript.v2',context,blobs)
    plan['nativeContextDigests']=sorted([d for d in plan['nativeContextDigests'] if d!=ts]+[new_context])
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    universe['nativeContextId']='sha256:'+new_context
    if mutate_universe:mutate_universe(universe)
    new_universe=M.retain_h_identity('native.semantic-universe.typescript.v2',universe,blobs)
    rekey(objects,scope_key,dict(objects[scope_key][1],sourceUniverse=new_universe,targetUniverse=new_universe),run)
    rekey_plan(objects,blobs,run,plan)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run)
    return M.close_run(run,objects,blobs)
check('reframe-harness-positive-control-closes',reframe_context().startswith('run2:'))
def flip_module_resolution(c):
    c['moduleResolutionMode']=next(x for x in N.SCHEMAS['$defs']['TypeScriptModuleResolutionMode']['enum'] if x!=c['moduleResolutionMode'])
rejects_because('reframed-context-contradicting-honored-options-refused',
    lambda:reframe_context(flip_module_resolution),'native.native-context-field-mismatch:moduleResolutionMode')
rejects_because('reframed-context-compiler-digest-not-in-tool-closure-refused',
    lambda:reframe_context(lambda c:c['toolchain'].update(compilerPackageDigest='b'*64)),
    'native.native-context-tool-not-in-closure:compilerPackageDigest')
rejects_because('reframed-context-runtime-not-in-tool-closure-refused',
    lambda:reframe_context(lambda c:c['toolClosure'].update(runtime='c'*64)),
    'native.native-context-tool-not-in-closure:runtime')
rejects_because('reframed-context-lib-selection-set-mismatch-refused',
    lambda:reframe_context(lambda c:c['toolchain'].update(libSelection=['dom'])),
    'native.native-context-field-mismatch:libSelection')
rejects_because('reframed-context-lib-selection-order-refused-by-the-native-schema',
    lambda:reframe_context(lambda c:c['toolchain']['libSelection'].reverse()),
    'H_FRAME_RECORD:native.context.typescript.v2')
rejects_because('reframed-context-stdlib-inventory-incomplete-refused',
    lambda:reframe_context(lambda c:c['toolchain']['standardLibraryComponentDigests'].pop()),
    'native.native-context-stdlib-inventory-incomplete')
rejects_because('reframed-context-stdlib-component-digest-mismatch-refused',
    lambda:reframe_context(lambda c:c['toolchain']['standardLibraryComponentDigests'][0].update(sha256='d'*64)),
    'native.native-context-stdlib-tree-mismatch')
rejects_because('reframed-context-compiler-version-not-from-manifest-refused',
    lambda:reframe_context(lambda c:c['toolchain'].update(compilerVersion='9.9.9')),
    'native.native-context-compiler-version-not-from-manifest')
for field in ['allowJs','checkJs']:
    rejects_because('reframed-universe-context-overlap-mismatch-'+field,
        lambda f=field:reframe_context(mutate_universe=lambda u,f=f:u.update({f:not u[f]})),
        'native.universe-context-field-mismatch:'+field)
rejects_because('reframed-universe-bound-to-other-context-bytes-refused',
    lambda:reframe_context(mutate_universe=lambda u:u.update(nativeContextId='sha256:'+'e'*64)),
    'UNIVERSE_CONTEXT_NOT_SELECTED')
# Native-context source correspondence must join the snapshot inventory.
rejects_because('reframed-context-config-graph-path-not-inventoried',
    lambda:reframe_context(lambda c:c['configProjection']['configGraphPaths'].append('zz-not-in-snapshot.json')),
    'NATIVE_CONTEXT_PATH_NOT_INVENTORIED:zz-not-in-snapshot.json')
rejects_because('reframed-context-lockfile-bytes-not-the-snapshot-bytes',
    lambda:reframe_context(lambda c:c['lockfileIdentity'].update(contentSha256='f'*64)),
    'NATIVE_CONTEXT_SOURCE_MISMATCH:package-lock.json')
rejects_because('reframed-context-lockfile-path-not-inventoried',
    lambda:reframe_context(lambda c:c['lockfileIdentity'].update(path='vendor/other-lock.json')),
    'NATIVE_CONTEXT_SOURCE_MISMATCH:vendor/other-lock.json')

# --- the Rust semantic-universe domain that native section 11 already registers ------------------
# native-evidence registers native.semantic-universe.rust.v2 and RustUniverseV2ResolvedInputs, so the
# identity registry must carry it or the promised Rust path would be refused as unregistered. The
# owning contract supplies no binding entry point for it yet, so a Rust universe refuses with a typed,
# named cause rather than closing unbound. This is a REQUIRED native-side follow-up, not an option.
UNIVERSE_SET=M.DIGESTS['domainSets']['native-semantic-universe']
check('rust-universe-domain-is-registered','native.semantic-universe.rust.v2' in UNIVERSE_SET)
check('rust-universe-binding-is-declared-required-and-missing',
      UNIVERSE_SET['native.semantic-universe.rust.v2']['binding']['status'].startswith('REQUIRED-NOT-YET-PROVIDED')
      and not hasattr(N,UNIVERSE_SET['native.semantic-universe.rust.v2']['binding']['entryPoint']))
RUST_SOURCES={'Cargo.lock':b'version = 3\n','src/lib.rs':b'pub fn f() {}\n'}
def rust_universe_run(mutate=lambda u:None):
    run,objects,blobs=build()
    plan=copy.deepcopy(objects[run['planId']][1])
    rust=next(d for d in plan['nativeContextDigests']
              if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')
    context=M.parse_h_frame(blobs[rust],'native-context')[1]
    snapshot_key=run['snapshotId'];snapshot=copy.deepcopy(objects[snapshot_key][1])
    snapshot['sourceInventory']=sorted(snapshot['sourceInventory']+
        [{'path':k,'sha256':put_blob(blobs,v),'bytes':len(v)} for k,v in RUST_SOURCES.items()],key=lambda r:r['path'].encode())
    inventory_digest=put_blob(blobs,snapshot['sourceInventory'])
    vcs=C.parse(blobs[snapshot['vcsDigest']]);vcs['sourceInventoryDigest']=inventory_digest
    snapshot['vcsDigest']=put_blob(blobs,vcs)
    universe={'schemaVersion':2,'edition':{'crate':2021},
      'lockfileIdentity':{'path':'Cargo.lock','contentSha256':hashlib.sha256(RUST_SOURCES['Cargo.lock']).hexdigest(),'lockfileVersion':3},
      'dependencySourceSetId':context['dependencySourceSetId'],'unifiedFeaturesId':context['unifiedFeaturesId'],
      'nativeContextId':'sha256:'+rust,'cfgSets':[{'cfgSetId':'default','cfg':[]}],
      'rustflags':context['configProjection']['rustflags'],'crateRootPaths':['src/lib.rs'],
      'configProjectionSha256':context['configProjection']['projectionSha256'],
      'executionCapableResolution':False,'preparedOutputSetId':context['preparedOutputSetId'],
      'preparedResolution':'none'}
    mutate(universe)
    universe_digest=M.native_universe_frame('native.semantic-universe.rust.v2',universe,blobs)
    rekey(objects,snapshot_key,snapshot,run);resync_stage_spec(objects,blobs,run)
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    rekey(objects,scope_key,dict(objects[scope_key][1],sourceUniverse=universe_digest,targetUniverse=universe_digest),run)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run)
    return M.close_run(run,objects,blobs)
rejects_because('rust-universe-refuses-until-native-provides-its-binding',rust_universe_run,
                'NATIVE_UNIVERSE_BINDING_UNAVAILABLE:bind_rust_universe')
rejects_because('rust-universe-crate-root-must-be-inventoried',
    lambda:rust_universe_run(lambda u:u.update(crateRootPaths=['src/absent.rs'])),
    'NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:src/absent.rs')
rejects_because('rust-universe-lockfile-bytes-must-be-the-snapshot-bytes',
    lambda:rust_universe_run(lambda u:u['lockfileIdentity'].update(contentSha256='a'*64)),
    'NATIVE_UNIVERSE_SOURCE_MISMATCH:Cargo.lock')
rejects_because('rust-universe-must-agree-with-its-context-dependency-set',
    lambda:rust_universe_run(lambda u:u.update(dependencySourceSetId='sha256:'+'b'*64)),
    'NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:dependencySourceSetId')
rejects_because('rust-universe-must-agree-with-its-context-unified-features',
    lambda:rust_universe_run(lambda u:u.update(unifiedFeaturesId='sha256:'+'c'*64)),
    'NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:unifiedFeaturesId')
# A universe may never bind a context of another language, whichever direction.
def ts_universe_on_rust_context():
    run,objects,blobs=build()
    plan=objects[run['planId']][1]
    rust=next(d for d in plan['nativeContextDigests']
              if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    universe['nativeContextId']='sha256:'+rust
    new=M.retain_h_identity('native.semantic-universe.typescript.v2',universe,blobs)
    rekey(objects,scope_key,dict(objects[scope_key][1],sourceUniverse=new,targetUniverse=new),run)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run);return M.close_run(run,objects,blobs)
rejects_because('typescript-universe-cannot-bind-a-rust-context',ts_universe_on_rust_context,
                'NATIVE_UNIVERSE_CONTEXT_LANGUAGE:native.context.rust.v2')

# --- ownerSourceDigest ------------------------------------------------------------------------
def repository_grant(rows,order_ok=True):
    run,objects,blobs=build();pid=run['planId'];plan=copy.deepcopy(objects[pid][1])
    grant=C.parse(blobs[plan['semanticGrantDigest']])
    owners=rows if order_ok else list(reversed(rows))
    grant['principals']=sorted(grant['principals']+[{'kind':'trusted-repository-code','closureId':plan['semanticClosures'][0],
        'ownerSourceDigest':put_blob(blobs,owners)}],key=C.canonical)
    grant['analysisOperations']=sorted(set(grant['analysisOperations'])|{'prepare-code'})
    plan['semanticGrantDigest']=put_blob(blobs,grant);rekey_plan(objects,blobs,run,plan)
    return M.close_run(run,objects,blobs)
ROWS=[{'ownerKey':'a','source':'repository','ownerFileManifestSha256':'8'*64},
      {'ownerKey':'b','source':'repository','ownerFileManifestSha256':'0'*64}]
check('owner-source-set-positive-run-closes',repository_grant(ROWS).startswith('run2:'))
rejects('owner-source-set-must-be-ordered-by-owner-key',lambda:repository_grant(ROWS,order_ok=False))
rejects('owner-source-set-duplicate-owner-key',lambda:repository_grant([ROWS[0],dict(ROWS[0])]))
rejects('owner-source-set-not-a-registered-record',lambda:repository_grant([{'ownerKey':'a'}]))
check('owner-source-set-order-is-schema-enforced',
      SCHEMA['$defs']['owner-source-set']['x-opensip-order']=={'by':['ownerKey']})
C.validate({'type':'array','x-opensip-order':{'by':['ownerKey']}},ROWS)
rejects('owner-source-set-schema-refuses-reversed-rows',
        lambda:C.validate({'type':'array','x-opensip-order':{'by':['ownerKey']}},list(reversed(ROWS))))

report={'standing':'design-reference-only','productQualification':False,'limits':[
    'finite single-atom rule interpreter over the REAL closed PolicyDocumentV1/RuleProgramV1 DSL; not full declarative-language qualification',
    'relation and Coverage payload schema REGISTRATION remains the native/workflow adapter boundary; identity checks retention, canonicality and validation under the retained document',
    'in-memory custody transition model; OS crash durability remains implementation gate',
    'replay callback is authenticated host/evaluator TCB assumption, not adversarial Python isolation',
    'both registered native-context domains and the TypeScript universe domain close through a complete Run over small retained closure trees; no compiler, cargo or repository code is executed and no platform is qualified',
    'the registered native.semantic-universe.rust.v2 domain cannot yet close a Run: the owning native contract supplies no bind_rust_universe entry point and does not name the producing domain for RustUniverseV2ResolvedInputs.configProjectionSha256. Identity refuses it with a typed named cause rather than admitting it unbound; this is a REQUIRED native-side follow-up, not optional later qualification',
    'nested native semantic identities inside a native context or universe (dependencySourceSetId, unifiedFeaturesId, preparedOutputSetId) are joined for context/universe agreement but their own H frames are not retained or re-admitted by this closure; that needs their record selectors registered in a domain set, which requires the owning native contract to name them',
    'owner-source-set ownerKey order uses the generic {by:[field]} x-opensip-order form in canonical.py; the closure checker enforces the same order independently'],
    'checks':results,'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results)}
a=argparse.ArgumentParser();a.add_argument('--report');args=a.parse_args()
if args.report:Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','failed','productQualification']}))
if report['failed']:print(json.dumps([x['id'] for x in results if not x['passed']],indent=1))
sys.exit(bool(report['failed']))
