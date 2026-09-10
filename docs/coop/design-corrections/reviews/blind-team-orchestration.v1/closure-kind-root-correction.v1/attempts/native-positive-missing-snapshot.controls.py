"""Retained descriptor role controls, separate from Plan membership and replay.

Record controls exercise actual owner get/payload admission on reminted records.
Whole import graphs have all enclosing identities minted from hostile inputs;
they refuse on role, while ordinary imported graphs pass complete replay.
No compiler, provider or product implementation is qualified.
"""
import copy,hashlib

def run_controls(T):
    M,C,F=T.M,T.C,T.F
    rows=[]
    history={'kind':'history','payload':{'payloadDomain':'workflow.import-payload.history.v1','vcsSystem':'git','revisionRange':{'from':None,'to':'a'*40,'commitCount':0,'truncated':False},'collectionScope':'all-paths','subjects':[]},'observation':{'revisionRange':{'from':None,'to':'a'*40}}}
    base=T.positive(import_specs=[history])
    run,objects,blobs=base
    accepted=T.R.replay(*base)
    rows.append({'case':'closure-kinds-import-full-replay-positive','boundary':'complete Run replay','result':accepted})
    _,owner=M.open_run_closure(*base)
    plan=objects[run['planId']][1]
    imp=objects[plan['importIds'][0]][1]
    # Transitive import dependency need not be a direct semanticClosures member.
    assert imp['adapterClosure'] not in plan['semanticClosures']
    assert objects[imp['producerClosure']][1]['kind']=='provider'
    assert objects[imp['adapterClosure']][1]['kind']=='adapter'
    rows.append({'case':'import-adapter-retained-through-import-not-direct-selected','boundary':'complete Run replay','result':'ADMIT'})
    closure_ids={record['kind']:key for key,(domain,record) in objects.items() if domain=='closure'}
    record_kinds={'subject-scope','view','fact','finding','evaluation-seal','proof-bundle','import'}
    covered=set()
    def refuse(case,fn,expected,boundary):
        try:fn()
        except M.C.AdmissionError as exc:
            assert str(exc)==expected,(case,str(exc),expected)
            rows.append({'case':case,'boundary':boundary,'result':'REFUSE','detail':str(exc)})
        else:raise AssertionError('Wrong-kind record admitted: '+case)
    for name,want in M.DIGESTS['closureKinds']['byField'].items():
        domain,field=name.split('.',1)
        if domain not in record_kinds:continue
        key,record=next((key,record) for key,(d,record) in objects.items() if d==domain)
        assert owner['get'](key,domain)==record
        changed=copy.deepcopy(record)
        changed[field]=closure_ids['evaluator' if want!='evaluator' else 'provider']
        hostile=M.identifier(domain,changed);objects[hostile]=(domain,changed)
        detail='ENUMERATOR_CLOSURE_KIND' if name=='subject-scope.enumeratorClosure' else 'CLOSURE_FIELD_KIND:'+name+':'+want
        refuse('retained-record-role-'+name,lambda k=hostile,d=domain:owner['get'](k,d),detail,'retained owning-record admission, not whole Run')
        covered.add(name)
    # The stage-spec is a canonical-record blob, so the get-only guard cannot cover it.
    stage=owner['execution']['stages'][0]
    spec=copy.deepcopy(owner['payload'](stage['stageSpecDigest'],'stage-spec'))
    bad=copy.deepcopy(spec);bad['producerClosure']=closure_ids['detector']
    raw=C.canonical(bad);digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw
    for n in range(2):
        refuse('stage-spec-role-retry-'+str(n),lambda:owner['payload'](digest,'stage-spec'),'CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider','retained canonical-record admission, not whole Run')
    covered.add('stage-spec.producerClosure')
    # Cache/regeneration admission is a real strong-Run boundary and an external key.
    key={'schemaVersion':2,'planId':run['planId'],'producerClosure':spec['producerClosure'],'stageSpecDigest':stage['stageSpecDigest'],'scopeIds':[],'inputRefs':[],'outputSchemaDigest':spec['outputSchemaDigest']}
    # The local negative records above are retained extras, never Run roots.
    for domain in ('cache-key','regeneration-key'):
        accepted=M.admit_cache_entry(domain,key,*base)
        assert accepted['runId']==M.identifier('run',run)
        rows.append({'case':domain+'-provider-positive','boundary':'strong Run plus key admission','result':'ADMIT'})
        changed=copy.deepcopy(key);changed['producerClosure']=closure_ids['detector']
        refuse(domain+'-wrong-kind',lambda d=domain,k=changed:M.admit_cache_entry(d,k,*base),'CLOSURE_FIELD_KIND:cache-key.producerClosure:provider','strong Run plus key admission')
    covered.add('cache-key.producerClosure')
    for field,kw in [('producerClosure',{'import_producer_kind':'adapter'}),('adapterClosure',{'import_adapter_kind':'provider'})]:
        g=F.build_file_inputs(import_specs=[history],**kw)
        hostile_run,hostile_objects,hostile_blobs,_=F.seal_fixture(g)
        # Check every H record's own constructor before the graph admission call.
        for hid,(domain,record) in hostile_objects.items():assert M.identifier(domain,record)==hid
        required='provider' if field=='producerClosure' else 'adapter'
        refuse('whole-import-graph-wrong-'+field,lambda:M.open_run_closure(hostile_run,hostile_objects,hostile_blobs),'CLOSURE_FIELD_KIND:import.'+field+':'+required,'fully reminted graph structural admission; semantic replay not reached')
    native_fields={'TypeScriptToolClosureV1.closureId','ToolClosureV1.closureId','toolchain.typescriptStdlibMerkleRoot','toolchain.rustcDevLlvmDigest','SyntaxGrammarBundleV1.closureId'}
    H=F.fixture_helpers();native_objects={};native_blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();native_blobs[digest]=raw;return digest
    def add(domain,**fields):
        record={'schemaVersion':2,**fields};key=M.identifier(domain,record)
        native_objects[key]=(domain,record);return key
    native=H.native_inputs(native_objects,native_blobs,add,blob)
    contexts={'typescript':native['context'],'rust':native['rustContext'],'syntax':native['syntaxContext']}
    native_closures={key:record for key,(domain,record) in native_objects.items() if domain=='closure'}
    N=M.native_admission()
    for language,context in contexts.items():
        result=N.admit_native_context(language,context,native_closures)
        assert not result['refusals'],result
        rows.append({'case':'native-closure-kind-positive-'+language,'boundary':'native context admission; not complete Run or extraction qualification','result':'ADMIT'})
    native_sites=[
        ('TypeScriptToolClosureV1.closureId','typescript','toolClosure','closureId',False),
        ('ToolClosureV1.closureId','rust','toolClosure','closureId',False),
        ('toolchain.typescriptStdlibMerkleRoot','typescript','toolchain','typescriptStdlibMerkleRoot',True),
        ('toolchain.rustcDevLlvmDigest','rust','toolchain','rustcDevLlvmDigest',True),
        ('SyntaxGrammarBundleV1.closureId','syntax','grammarBundle','closureId',False),
    ]
    for name,language,parent,field,suffix in native_sites:
        context=copy.deepcopy(contexts[language]);cid=context[parent][field]
        if suffix:cid='closure2:'+cid
        descriptor=copy.deepcopy(native_closures[cid]);descriptor['kind']='provider'
        wrong=M.identifier('closure',descriptor);closures={**native_closures,wrong:descriptor}
        context[parent][field]=wrong.split(':',1)[1] if suffix else wrong
        result=N.admit_native_context(language,context,closures)
        expected='native.native-context-closure-kind-mismatch:'+parent+'.'+field
        assert expected in result['refusals'],(name,result)
        rows.append({'case':'native-retained-closure-role-'+name,'boundary':'native context admission with reminted closure identity; not whole Run','result':'REFUSE','detail':expected})
    assert covered|native_fields==set(M.DIGESTS['closureKinds']['byField'])
    rows.append({'case':'published-closure-field-partition','boundary':'registry audit; execution boundary stated per control','locallyExercisedFields':sorted(covered),'nativeOwnerFields':sorted(native_fields),'nativeFieldsStanding':'All five native field kind negatives executed through owning admit_native_context above.'})
    return rows
