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
# Every negative that could plausibly refuse at an earlier join asserts its EXACT refusal cause,
# so a refusal at the wrong place is never counted as coverage of the intended one.
def not_admitted(fn):
    try:fn()
    except (ValueError,KeyError,TypeError,C.ValidationError):return True
    return False
def rejects_because(name,fn,token):
    try:fn()
    except (ValueError,KeyError,TypeError,C.ValidationError) as exc:check(name,token in str(exc))
    else:check(name,False)


# --------------------------------------------------------------------------- the closed policy DSL
# The fixture rule is a real PolicyDocumentV1 / RuleProgramV1 in the workflow contract's own closed
# DSL. Only the fixture INTERPRETER is small: it evaluates the single-atom subset below. There is no
# second policy language anywhere in the identity unit.
ATOM={'op':'none','relation':'references','minResolution':'resolved','filters':[{'field':'target','cmp':'eq','value':'foo'}]}
def rule_for(language):
    """One rule, in the workflow contract's own DSL, enumerating subjects of the analysed
    language's universe. The requested capability, the analysed source and the rule's subject
    universe are one coherent request; they are not a Rust universe under a TypeScript question."""
    return {'ruleId':'no-consumer','ruleProgramRef':{'contributionId':'fixture','ruleStableId':'no-consumer','semanticsMajor':2,
              'programDigest':hashlib.sha256(C.canonical(ATOM)).hexdigest()},
            'enabled':True,'severity':'error','gate':True,
            'subjectEnumeration':{'universe':language,'subjectKind':'symbol'},
            'emitWhen':ATOM,'evidenceUse':[],'messageCode':'no-consumer'}
def policy_for(language):
    return {'schemaFamily':'opensip.product.policy','schemaMajor':1,'gateSeverityAtLeast':'error',
            'rules':[rule_for(language)]}
RULE=rule_for('typescript')
POLICY=policy_for('typescript')
WAIVERS={'schemaFamily':'opensip.product.waivers','schemaMajor':1,'waivers':[]}
def compiled_program(policy):
    return {'schemaVersion':1,'policyDigest':hashlib.sha256(C.canonical(policy)).hexdigest(),
            'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in policy['rules']]}
# Positive Runs use the REAL registered payload documents through the closed payload registry.
# The former fixture-only FACT_PAYLOAD_SCHEMA={target} and COVERAGE_PAYLOAD_SCHEMA={examined,
# resolved,closed} were inventions standing in for product admission and are deleted: they proved
# nothing about whether a product payload is admissible (blind consumer Bv2 M-1/M-2).
# G6: a CURRENT capability manifest that declares the thirteenth relation. The inherited
# twelve-relation golden is still admitted (below), and delivery.v4's bytes are untouched.
DELIVERY=json.loads((H.parents[1]/'artifacts/delivery.v4.json').read_text())
CAPABILITY_RECIPE=next(v['value'] for v in DELIVERY['derivedFrom']['operations'] if v['path']=='capabilityManifestIdentity')
INHERITED_MANIFEST_BYTES=bytes.fromhex(CAPABILITY_RECIPE['vectors']['byId']['DCM-1-core']['committedBytesHex'])

def current_capability_manifest():
    """The inherited golden value, extended with a provider row declaring unresolved-edge@observed."""
    value=N.cve1_decode(INHERITED_MANIFEST_BYTES)
    provider=copy.deepcopy(value['providers'][0])
    provider['relations']=dict(provider['relations']);provider['relations']['unresolved-edge']='observed'
    value['providers']=[provider]+value['providers'][1:]
    return N.cve1_encode(value)
CURRENT_CAPABILITY_MANIFEST_BYTES=current_capability_manifest()

RELATION_DOCUMENT=H/'relation-payload-schemas.v2.json'
RELATION_DOCUMENT_BYTES=RELATION_DOCUMENT.read_bytes()
RELATION_DOCUMENT_DIGEST=hashlib.sha256(RELATION_DOCUMENT_BYTES).hexdigest()
NATIVE_DOCUMENT=H.parent/'native/native-evidence.schemas.v2.json'
NATIVE_DOCUMENT_BYTES=NATIVE_DOCUMENT.read_bytes()
NATIVE_DOCUMENT_DIGEST=hashlib.sha256(NATIVE_DOCUMENT_BYTES).hexdigest()
RELATION_REGISTRY=json.loads(RELATION_DOCUMENT.read_text())['x-opensip-relation-registry']['relations']
STAGE_OUTPUT_SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:stage-output',
    'type':'object','additionalProperties':False,'required':['viewId'],
    'properties':{'viewId':{'type':'string','pattern':'^view2:[0-9a-f]{64}(?![\\s\\S])'}}}

# The TypeScript context's config graph and lockfile are repository sources, so they must be in the
# snapshot inventory. identity-and-evidence section 3 already required snapshot/native-context source
# correspondence to agree; these are the rows that discharge it.
TS_SOURCES={'tsconfig.base.json':b'{"compilerOptions":{"target":"es2022"}}\n',
            'tsconfig.strict.json':b'{"compilerOptions":{"strict":true}}\n',
            'tsconfig.json':b'{"extends":["./tsconfig.base.json","./tsconfig.strict.json"]}\n',
            'package-lock.json':b'{"lockfileVersion":3}\n'}
# The ORDINARY TypeScript project: node_modules IS in the read set, so bare specifiers resolve.
# node_modules is pruned from the snapshot by the one shared discovery rule, so these are retained
# resolution-read-set observations, not snapshot inventory rows.
TS_NODE_MODULES={'node_modules/left-pad/package.json':b'{"name":"left-pad","version":"1.3.0"}\n',
                 'node_modules/@scope/util/package.json':b'{"name":"@scope/util","version":"2.0.1"}\n'}

# The Rust path's own minimal source observations. Every one is an explicit synthetic trusted
# observation; nothing here runs cargo, rustc, a build script, a proc macro or a filesystem read.
RUST_TARGET='aarch64-apple-darwin'
RUST_DEP_KEY='fixture-dep 1.0.0 registry+https://github.com/rust-lang/crates.io-index'
RUST_DEP_FILE=b'pub fn dep() {}\n'
RUST_PROJECTED_CONFIG=b'[build]\nrustflags = ["--cfg", "fixture"]\n'
RUST_SOURCES={'Cargo.lock':('version = 3\n\n[[package]]\nname = "fixture-dep"\nversion = "1.0.0"\n'
                            'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
                            'checksum = "'+'a'*64+'"\n\n[[package]]\nname = "fixture-root"\nversion = "0.1.0"\n').encode(),
              '.cargo/config.toml':b'[build]\nrustflags = ["--cfg", "fixture"]\n',
              'src/lib.rs':b'pub fn root() {}\n',
              'vendor/fixture-dep/src/lib.rs':RUST_DEP_FILE}

RUST_PREPARED_DIRECTIVES=b'cargo:rustc-cfg=fixture_prepared\n'

# The registered references@resolved-binding payload: exactly the inherited field set
# {referrer, name, resolvedBinding} with SubjectIdV1 / CanonicalText values.
REFERENCES_PAYLOAD={'referrer':'symbol:foo','name':'foo','resolvedBinding':'symbol:foo'}
# The policy DSL's closed FieldFilter vocabulary (subject/target/...) projected onto the registered
# relation payload's own field names. The projection is the detector closure's, not the encoder's.
FILTER_FIELD_OF={'subject':'referrer','target':'name','resolution':'name',
                 'universe':'name','subjectKind':'name','targetKind':'name','observability':'name'}

def coverage_result(scope_descriptor,universe,resolved):
    """A real CoverageResultV3 over the host's own scope. RC-2: `complete` needs attempted,
    exhaustive examination and a complete stage terminal, and zero admitted unresolved edges."""
    commitment=N.subject_scope_commitment(scope_descriptor)
    completeness=({'state':'complete','attempted':True,'examinedExhaustive':True,
                   'stageTerminal':'complete','unresolvedEdgeCount':0,'unresolvedEdgeClasses':[]}
                  if resolved else
                  {'state':'not-attempted','attempted':False,'examinedExhaustive':False,
                   'stageTerminal':None,'unresolvedEdgeCount':0,'unresolvedEdgeClasses':[]})
    return {'schemaVersion':3,
      'key':{'relation':scope_descriptor['relation'],'resolution':scope_descriptor['resolution'],
             'sourceUniverse':scope_descriptor['sourceUniverse'],'targetUniverse':scope_descriptor['targetUniverse'],
             'subjectScopeCommitment':commitment['subjectScopeCommitment']},
      'entry':{'relation':scope_descriptor['relation'],'resolution':scope_descriptor['resolution'],
               'coverage':'complete' if resolved else 'unknown',
               'examinedUniverse':{'subjectScopeCommitment':commitment['subjectScopeCommitment'],
                                   'subjectCount':commitment['subjectCount']},
               'resolutionCompleteness':completeness,
               'closedWorld':{'exportsClosed':'closed','entryPointsRecognized':'all','nonliteralLoading':'none',
                              'externalConsumers':'none-declared','dynamicDispatch':'not-applicable',
                              'reasons':[],'deadCodeRepairEligible':True},
               'derivationKinds':[],'confidenceMillionths':1000000,
               'deficiency':None if resolved else 'resolution-incomplete','nativeCause':None}}

def rust_inputs(objects,blobs,add,blob,tree,dep_body=RUST_DEP_FILE,prepared=None):
    """One admitted Rust native context and its OWN rust-v2 semantic universe, with every nested
    semantic identity a retained record of its registered domain: DependencySourceSetV1 (whose
    package file manifests are themselves DependencyFileManifestV1 identities over retained member
    bytes), UnifiedFeaturesV1 and CargoConfigProjectionV2. No dependency id is an opaque string."""
    llvm=add('closure',kind='rust-dev-llvm',manifestDigest=blob(b'fixture-llvm-manifest'),
             tree=tree({'lib/librustc_driver.so':b'\x7fELF fixture\n'}),semanticVersion='1.83.0',protocolMajor=3,platform='macos-aarch64')
    tools=add('closure',kind='toolchain',manifestDigest=blob(b'fixture-cargo-manifest'),
              tree=tree({'bin/cargo':b'#!fixture-cargo\n','bin/rustc':b'#!fixture-rustc\n',
                         'libexec/proc-macro-srv':b'#!fixture-proc-macro-srv\n'}),
              semanticVersion='1.83.0',protocolMajor=3,platform='macos-aarch64')
    tool_tree={r['path']:r['sha256'] for r in objects[tools][1]['tree']}
    # DependencySourceSetV1 through the ACTUAL DS-1..DS-6 admission over a sealed vendored tree.
    manifest_files={'src/lib.rs':{'sha256':blob(dep_body),'byteLength':len(dep_body)}}
    dependency=N.dependency_source_set_admit(
        RUST_SOURCES['Cargo.lock'].decode(),
        [{'name':'fixture-dep','version':'1.0.0','sourceId':'registry+https://github.com/rust-lang/crates.io-index',
          'acquisition':{'mode':'in-snapshot-vendored','vendorPath':'vendor/fixture-dep'},
          'files':manifest_files,'cargoChecksumJson':None,'crateTarballSha256':'a'*64}],
        [RUST_DEP_KEY])
    if not dependency['admitted']:raise C.AdmissionError('FIXTURE_RUST_DEPENDENCY_SET')
    # Retain the file-manifest frame the package identity names, and its member bytes.
    manifest_rows=sorted(({'path':p,'contentSha256':f['sha256'],'byteLength':f['byteLength']}
                          for p,f in manifest_files.items()),key=lambda r:r['path'].encode())
    M.retain_h_identity(N.DEPENDENCY_FILE_MANIFEST_DOMAIN,manifest_rows,blobs)
    dependency_id=M.retain_h_identity(N.DEPENDENCY_SOURCE_SET_DOMAIN,dependency['descriptor'],blobs)
    if 'sha256:'+dependency_id!=dependency['identity']:raise C.AdmissionError('FIXTURE_RUST_DEPENDENCY_IDENTITY')
    features={'schemaVersion':1,'resolverVersion':2,'targetTriple':RUST_TARGET,
              'activated':[{'packageKey':RUST_DEP_KEY,'features':['default']}],
              'computedBy':{'producer':'opensip-cargo-adapter','producerBuildId':'fixture-adapter-1'}}
    features_id=M.retain_h_identity(N.UNIFIED_FEATURES_DOMAIN,features,blobs)
    projection={'schemaVersion':2,'honoredKeys':['build.rustflags'],'strippedKeys':['build.rustc'],
                'replacedSnapshotConfigs':['.cargo/config.toml'],
                'rustflags':{'honored':['--cfg fixture'],'stripped':[],'executableSelected':False},
                'ancestorCarrierVerified':True,'cargoHome':'private-empty','environmentProjection':'none',
                'claimsCargoSwitch':False,'projectionSha256':blob(RUST_PROJECTED_CONFIG)}
    projection_id=M.retain_h_identity(N.CARGO_CONFIG_PROJECTION_DOMAIN,projection,blobs)
    context={'schemaVersion':2,'targetTriple':RUST_TARGET,'hostTriple':RUST_TARGET,
        'toolchain':{'rustCommitHash':'b'*40,'rustcVersion':'1.83.0','cargoVersion':'1.83.0',
                     'sysrootDigest':blob(b'fixture-sysroot'),'rustcDevLlvmDigest':llvm.removeprefix('closure2:'),
                     'standardLibraryComponentDigests':[{'component':'libcore.rlib','sha256':blob(b'fixture-libcore')},
                                                        {'component':'libstd.rlib','sha256':blob(b'fixture-libstd')}],
                     'targetTriple':RUST_TARGET},
        'toolClosure':{'rustc':tool_tree['bin/rustc'],'cargo':tool_tree['bin/cargo'],'linker':None,'ar':None,
                       'procMacroServer':tool_tree['libexec/proc-macro-srv'],'closureId':tools},
        'baseCfg':['target_arch="aarch64"','target_os="macos"'],'resolverVersion':2,
        'dependencySourceSetId':'sha256:'+dependency_id,'unifiedFeaturesId':'sha256:'+features_id,
        'preparedOutputSetId':None,'configProjection':projection}
    prepared_id=None
    if prepared is not None:
        # Inert prepared products consumed as DATA. The retained bytes never imply an execution
        # grant; the universe's preparedResolution projects the operational grant operation.
        toolchain_digest=blob(C.canonical(context['toolchain']))
        record={'schemaVersion':3,
            'preparation':{'kind':prepared,'authorizationId':None if prepared=='imported-descriptor' else 'sha256:'+blob(b'fixture-authorized-execution'),
                'importId':None,'toolchain':context['toolchain'],
                'dependencySourceSetId':'sha256:'+dependency_id,'cfgSetId':'primary',
                'producer':{'id':'opensip-native-prepare','version':'1.0.0'}},
            'rows':[{'kind':'build-script-directives','ownerKey':'fixture-root','configuration':[],
                'site':None,'generated':None,
                'inputBinding':{'ownerFileManifestSha256':blob(b'fixture-owner-manifest'),
                    'dependencySourceSetId':'sha256:'+dependency_id,'toolchainDigest':toolchain_digest,'cfgSetId':'primary'},
                'blob':{'sha256':blob(RUST_PREPARED_DIRECTIVES),'byteLength':len(RUST_PREPARED_DIRECTIVES),
                        'mediaType':'text/x-cargo-directives'},
                'status':'ok','failureDetail':None}]}
        prepared_id='sha256:'+M.retain_h_identity(N.PREPARED_OUTPUT_SET_DOMAIN,record,blobs)
        context['preparedOutputSetId']=prepared_id
    admission=N.admit_native_context('rust',context,{k:objects[k][1] for k in (llvm,tools)})
    if admission['refusals']:raise C.AdmissionError('FIXTURE_RUST_CONTEXT:'+','.join(admission['refusals']))
    universe={'schemaVersion':2,'edition':{'fixture-root':2021},
        'lockfileIdentity':{'path':'Cargo.lock','contentSha256':hashlib.sha256(RUST_SOURCES['Cargo.lock']).hexdigest(),'lockfileVersion':3},
        'dependencySourceSetId':'sha256:'+dependency_id,'unifiedFeaturesId':'sha256:'+features_id,
        'nativeContextId':admission['nativeContextId'],
        'cfgSets':[{'cfgSetId':'primary','cfg':context['baseCfg']},
                   {'cfgSetId':'primary+test','cfg':context['baseCfg']+['test']}],
        'rustflags':projection['rustflags'],'crateRootPaths':['src/lib.rs'],
        'configProjectionSha256':projection_id,'executionCapableResolution':prepared is not None,
        'preparedOutputSetId':prepared_id,
        'preparedResolution':'none' if prepared is None else ('imported-inert' if prepared=='imported-descriptor' else 'host-prepared')}
    context_digest=M.native_context_frame('native.context.rust.v2',context,blobs)
    universe_digest=M.native_universe_frame('native.semantic-universe.rust.v2',universe,blobs)
    if context_digest!=admission['planNativeContextDigest']:raise C.AdmissionError('FIXTURE_RUST_IDENTITY')
    return {'contextDigest':context_digest,'context':context,'universeDigest':universe_digest,'universe':universe,
            'llvm':llvm,'toolClosure':tools,'admission':admission,'dependency':dependency['descriptor'],
            'features':features,'projection':projection,'manifestRows':manifest_rows}

def native_inputs(objects,blobs,add,blob,stdlib_body=b'declare const es2022: unknown;\n',prepared=None,ts_inventory=(),ts_source_path='a.ts'):
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
    context['configProjection']['configGraphPaths']=sorted(['tsconfig.base.json','tsconfig.json','tsconfig.strict.json'])
    context['lockfileIdentity']={'kind':'package-lock','path':'package-lock.json',
                                 'contentSha256':hashlib.sha256(TS_SOURCES['package-lock.json']).hexdigest()}
    # G3: the retained resolution read-set layout the context commits to. Its presence is exactly
    # what makes nodeModulesInReadSet true, so the mainstream bare-specifier branch is constructible.
    layout={'schemaVersion':1,'entries':sorted(
        ({'packageName':json.loads(body)['name'],'packageVersion':json.loads(body)['version'],
          'installPath':path.rpartition('/package.json')[0],'realPath':path.rpartition('/package.json')[0],
          'contentSha256':blob(body)} for path,body in TS_NODE_MODULES.items()),
        key=lambda r:r['installPath'].encode())}
    context['nodeModulesLayoutDigest']=N.resolved_node_modules_layout_digest(layout)
    blob(C.canonical(layout))
    admission=N.admit_native_context('typescript',context,{k:objects[k][1] for k in (stdlib,toolchain)})
    if admission['refusals']:raise C.AdmissionError('FIXTURE_NATIVE_CONTEXT:'+','.join(admission['refusals']))
    # G5/G10: the retained tsconfig extends graph the universe key names, with configOrigin DERIVED.
    # An ORDINARY modern config: tsconfig.json extends TWO bases, later wins (TypeScript 5.0).
    graph={'schemaVersion':1,'entryConfigPath':'tsconfig.json','nodes':sorted([
        {'path':'tsconfig.base.json','contentSha256':hashlib.sha256(TS_SOURCES['tsconfig.base.json']).hexdigest(),
         'kind':'other','extendsResolved':[]},
        {'path':'tsconfig.strict.json','contentSha256':hashlib.sha256(TS_SOURCES['tsconfig.strict.json']).hexdigest(),
         'kind':'other','extendsResolved':[]},
        {'path':'tsconfig.json','contentSha256':hashlib.sha256(TS_SOURCES['tsconfig.json']).hexdigest(),
         'kind':'tsconfig','extendsResolved':['tsconfig.base.json','tsconfig.strict.json']}],
        key=lambda r:r['path'].encode())}
    graph_digest=N.typescript_config_graph_digest(graph);blob(C.canonical(graph))
    universe=copy.deepcopy(NATIVE_FIXTURES['tsUniverse']);universe['nativeContextId']=admission['nativeContextId']
    universe.update(tsconfigGraphHash=graph_digest,configOrigin=N.typescript_config_origin(graph),
                    nodeModulesInReadSet=True,programRootFiles=[ts_source_path],jsRootFiles=[])
    binding=N.bind_typescript_universe(universe,admission,context,
        {'configGraph':graph,'nodeModulesLayout':layout},ts_inventory)
    if binding['result']!='ADMIT':raise C.AdmissionError('FIXTURE_NATIVE_UNIVERSE:'+','.join(binding['refusals']))
    context_digest=M.native_context_frame('native.context.typescript.v2',context,blobs)
    universe_digest=M.native_universe_frame('native.semantic-universe.typescript.v2',universe,blobs)
    if context_digest!=admission['planNativeContextDigest'] or universe_digest!=binding['sourceUniverse']:
        raise C.AdmissionError('FIXTURE_NATIVE_IDENTITY')
    # The second registered native-context domain and its OWN semantic universe, over retained small
    # trees, real nested Rust semantic input records and the actual native admission and binding.
    rust=rust_inputs(objects,blobs,add,blob,tree,prepared=prepared)
    return {'contextDigest':context_digest,'universeDigest':universe_digest,'context':context,'universe':universe,
            'stdlib':stdlib,'toolchain':toolchain,'admission':admission,
            'rustContextDigest':rust['contextDigest'],'rustContext':rust['context'],
            'rustUniverseDigest':rust['universeDigest'],'rustUniverse':rust['universe'],
            'llvm':rust['llvm'],'rustTools':rust['toolClosure'],'rust':rust}

LANGUAGE_FIXTURE={
 'typescript':{'languageMode':'ts-tsconfig','sourcePath':'a.ts','sourceBytes':b'export const foo = 1;\n'},
 'rust':{'languageMode':'rust-cargo','sourcePath':'src/lib.rs','sourceBytes':RUST_SOURCES['src/lib.rs']}}

def build(resolved=True,has_match=False,source_path=None,with_finding=False,stdlib_body=b'declare const es2022: unknown;\n',universe_language='typescript',prepared=None,grant_operations=None):
    objects={};blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest
    def add(domain,**fields):
        value={'schemaVersion':2,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
    fixture=LANGUAGE_FIXTURE[universe_language]
    language_mode=fixture['languageMode'] if prepared is None else 'rust-cargo-prepared'
    source_body=b"export const foo = 1;\n" if source_path is not None else fixture['sourceBytes']
    source_path=source_path if source_path is not None else fixture['sourcePath']
    source=blob(source_body)
    cap_bytes=CURRENT_CAPABILITY_MANIFEST_BYTES
    cap_digest=blob(cap_bytes);cap_id=hashlib.sha256(b'opensip.capability-manifest.v1\0'+cap_bytes).hexdigest()
    closure=add('closure',kind='evaluator',manifestDigest=blob(b'fixture-evaluator-manifest'),tree=[],semanticVersion='2.0.0',protocolMajor=3,platform='macos-aarch64')
    enumerator=add('closure',kind='provider',manifestDigest=blob(b'fixture-provider-manifest'),tree=[],semanticVersion='2.0.0',protocolMajor=3,platform='macos-aarch64')
    inventory=sorted([{'path':p,'sha256':blob(b),'bytes':len(b)}
        for p,b in {**TS_SOURCES,**RUST_SOURCES,source_path:source_body}.items()],key=lambda r:r['path'].encode())
    native=native_inputs(objects,blobs,add,blob,stdlib_body,prepared,inventory,source_path)
    universe=native['universeDigest'] if universe_language=='typescript' else native['rustUniverseDigest']
    config=blob({'analysis':{'profileId':'default','capabilities':['references'],'budget':{'unit':'work-units','limit':1000}},'components':{},'discovery':{},'policy':{},'evidence':{}})
    scope_payload=blob({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})
    vcs=blob({'schemaVersion':2,'kind':'none','commitId':None,'dirty':False,'sourceInventoryDigest':blob(inventory)})
    snapshot=add('snapshot',projectId='prj1-'+'a'*64,sourceInventory=inventory,resolvedConfigDigest=config,scopeDigest=scope_payload,vcsDigest=vcs)
    policy=policy_for(universe_language)
    policy_digest=blob(policy);waiver_digest=blob(WAIVERS)
    program=compiled_program(policy);program_digest=blob(program)
    spec_payload=blob({'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'references','languageMode':language_mode,'workspaceRoot':'.','required':True}],'policyPackIds':['fixture.no-consumer'],'parameters':[]})
    grant=blob({'schemaVersion':2,'projectId':'prj1-'+'a'*64,'principals':[{'kind':'first-party','closureId':closure,'ownerSourceDigest':None}],'analysisOperations':sorted(grant_operations or ['native-analysis','read-source']),'scopeDigest':scope_payload})
    plan=add('plan',snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=sorted({closure,enumerator}),analysisSpecDigest=spec_payload,resolvedConfigDigest=config,nativeContextDigests=sorted({native['contextDigest'],native['rustContextDigest']}),importIds=[],policyDigest=policy_digest,waiverDigest=waiver_digest,scopeDigest=scope_payload,budget={'unit':'work-units','limit':1000},semanticGrantDigest=grant)
    scope=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation='references',resolution='resolved-binding',enumeratorClosure=enumerator,subjects=['foo'])
    # The REAL registered Coverage payload, minted through the actual native producer boundary, and
    # the REAL registered relation payload for references@resolved-binding.
    coverage_schema=blob(NATIVE_DOCUMENT_BYTES);fact_schema=blob(RELATION_DOCUMENT_BYTES)
    scope_descriptor=objects[scope][1]
    coverage_payload=coverage_result(scope_descriptor,universe,resolved)
    admission=N.admit_coverage_result_v3(coverage_payload,scope_descriptor,[],coverage_schema)
    if admission['result']!='ADMIT':raise C.AdmissionError('FIXTURE_COVERAGE:'+','.join(admission['refusals'])+str(admission['faults']))
    coverage=add('coverage',scopeId=scope,payloadSchemaDigest=coverage_schema,payloadDigest=blob(coverage_payload))
    if coverage!=admission['coverageId']:raise C.AdmissionError('FIXTURE_COVERAGE_IDENTITY')
    facts=[]
    if has_match:
        facts=[add('fact',snapshotId=snapshot,relation='references',resolution='resolved-binding',sourceUniverse=universe,targetUniverse=universe,producerClosure=closure,payloadSchemaDigest=fact_schema,payloadDigest=blob(REFERENCES_PAYLOAD),anchors=[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)-1}],confidenceMillionths=1000000)]
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
        # The rule's typed field filter over the REAL registered relation payload.
        if fact['relation']==node['relation'] and C.equal_typed(payload.get(FILTER_FIELD_OF[field]),value_wanted):matches.append(fid)
    for cid in view['coverageIds']:
        coverage=objects[cid][1];payload=C.parse(blobs[coverage['payloadDigest']])
        # The REAL CoverageResultV3: `complete` is the admitted entry's own coverage state, which
        # RC-2 already ties to attempted + exhaustive examination + a complete stage terminal.
        complete=complete and payload['entry']['coverage']=='complete'
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
    return {'schemaVersion':2,'planId':pid,'executionPlanId':execution[0],'evaluatorClosure':next(k for k in plan['semanticClosures'] if objects[k][1]['kind']=='evaluator'),'ruleProgramDigest':program_digest,'evaluationInputRefs':[{'domain':'view','digest':vid.split(':')[1]}],'predicateProofs':[{'ruleId':'no-consumer','subjectId':'foo','predicateId':'p','operation':node['op'],'inputRefs':[{'domain':'view','digest':vid.split(':')[1]}],'scopeIds':view['scopeIds'],'value':value,'witnessDigest':hashlib.sha256(C.canonical(witness)).hexdigest()}],'findingIds':findings,'verdict':verdict}

def sort_canonical_sets(domain,value):
    """Re-sort every array the schema annotates `canonical-set`. Substituting an identity inside a
    record can move an element's canonical bytes, and a canonical-set array must be re-ordered before
    the record is re-minted; this is bookkeeping for the fixture, never a semantic change."""
    def walk(node,item):
        node=dict(M.SCHEMA['$defs'][node['$ref'].split('/')[-1]],**{k:v for k,v in node.items() if k!='$ref'}) if type(node) is dict and '$ref' in node and node['$ref'].startswith('#/$defs/') else node
        if type(node) is not dict:return item
        if 'oneOf' in node:
            for branch in node['oneOf']:
                try:return walk(branch,item)
                except Exception:continue
            return item
        if type(item) is list and 'items' in node:
            item=[walk(node['items'],x) for x in item]
            if node.get('x-opensip-order')=='canonical-set':item=sorted(item,key=C.canonical)
            return item
        if type(item) is dict and 'properties' in node:
            return {k:(walk(node['properties'][k],v) if k in node['properties'] else v) for k,v in item.items()}
        return item
    return walk(M.SCHEMA['$defs'][domain],value)

def rekey(objects,old,changed,run):
    domain=objects[old][0];changed=sort_canonical_sets(domain,changed)
    new=M.identifier(domain,changed);objects.pop(old);objects[new]=(domain,changed)
    def replace(x):
        if type(x) is str:return new if x==old else x
        if type(x) is list:return [replace(y) for y in x]
        if type(x) is dict:
            if set(x)=={'domain','digest'} and x['domain']==domain and x['digest']==old.split(':')[1]:return {'domain':domain,'digest':new.split(':')[1]}
            return {k:replace(v) for k,v in x.items()}
        return x
    # Propagate all direct identities upward. Used to make self-consistent hostile claims.
    while True:
        changed=next(((key,replace(v)) for key,(d,v) in objects.items() if sort_canonical_sets(d,replace(v))!=v),None)
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

def resync_coverage(objects,blobs,run,resolved=True):
    """Rebuild every Coverage payload over the CURRENT retained scope. A re-key that moves a
    subject-scope moves its commitment, and the host re-runs the native producer admission at Run
    closure, so a fixture that left the old payload behind would (correctly) be refused."""
    for key in [k for k,(d,v) in objects.items() if d=='coverage']:
        coverage=copy.deepcopy(objects[key][1])
        scope=objects[coverage['scopeId']][1]
        coverage['payloadDigest']=put_blob(blobs,coverage_result(scope,scope['sourceUniverse'],resolved))
        rekey(objects,key,coverage,run)

def resync_witness(objects,blobs,run):
    """Rebuild the predicate witness and proof reference arrays over the CURRENT view, after a
    re-key moved a fact or coverage identity. Bookkeeping, not a semantic change."""
    key=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[key][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    proof['evaluationInputRefs']=sorted(proof['evaluationInputRefs'],key=C.canonical)
    rekey(objects,key,proof,run)

def resync_proof_refs(objects,blobs,run):
    """rekey() substitutes identities in place but cannot know an array is canonical-set ordered, so
    a re-mint can leave a proof's reference arrays out of order. Re-sort them."""
    key=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[key][1])
    proof['evaluationInputRefs']=sorted(proof['evaluationInputRefs'],key=C.canonical)
    for predicate in proof['predicateProofs']:
        predicate['inputRefs']=sorted(predicate['inputRefs'],key=C.canonical)
        predicate['scopeIds']=sorted(predicate['scopeIds'],key=C.canonical)
    if C.canonical(proof)!=C.canonical(objects[key][1]):rekey(objects,key,proof,run)

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
        vcs.update(kind='git',commitId='a'*40,dirty=dirty);snap['vcsDigest']=put(vcs)
        snap['sourceInventory']=snap['sourceInventory'];rekey(objects,sid,snap,run)
        resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run)
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
# --- cache / regeneration: key construction is not admission ----------------------------------
run,objects,blobs=build(resolved=True,has_match=True)
execution=objects[objects[run['evaluationSealId']][1]['executionPlanId']][1]
stage_digest=execution['stages'][0]['stageSpecDigest'];stage=C.parse(blobs[stage_digest])
scope_id=next(k for k,(d,v) in objects.items() if d=='subject-scope')
view_id=objects[objects[run['evidenceId']][1]['viewIds'][0]][0] if False else next(k for k,(d,v) in objects.items() if d=='view')
cache={'schemaVersion':2,'planId':run['planId'],'producerClosure':stage['producerClosure'],'stageSpecDigest':stage_digest,
       'scopeIds':[scope_id],'inputRefs':[{'domain':'view','digest':view_id.split(':')[1]}],
       'outputSchemaDigest':stage['outputSchemaDigest']}
# 1. Pure key construction: no bytes, no references, no authority.
cache_id=M.cache_key('cache-key',cache);regen_id=M.cache_key('regeneration-key',cache)
check('cache-and-regen-share-one-stage-spec-record',
      cache_id.startswith('cache2:') and regen_id.startswith('regen2:') and cache_id.split(':')[1]!=regen_id.split(':')[1])
check('cache-stage-spec-is-the-same-digest-as-the-execution-plan-stage',cache['stageSpecDigest']==stage_digest)
check('cache-key-construction-reads-no-bytes',
      M.cache_key('cache-key',{**cache,'stageSpecDigest':'e'*64}).startswith('cache2:') and
      M.cache_key('cache-key',{**cache,'inputRefs':[{'domain':'blob','digest':'f'*64}]}).startswith('cache2:'))
rejects('cache-key-still-refuses-an-unregistered-domain',
        lambda:M.cache_key('cache-key',{**cache,'inputRefs':[{'domain':'made-up','digest':'f'*64}]}))
rejects('cache-key-domain-must-be-a-cache-or-regeneration-key',lambda:M.cache_key('plan',cache))
# 2. Admitting a HIT: the same admitted closure the Run itself requires.
admitted=M.admit_cache_entry('cache-key',cache,run,objects,blobs)
check('cache-hit-admits-against-the-runs-own-closure',
      admitted['identity']==cache_id and admitted['runId']==M.close_run(run,objects,blobs))
check('cache-hit-grants-no-evidence-authority',admitted['grantsEvidenceAuthority'] is False)
check('cache-hit-records-every-consumed-reference',admitted['consumedRefs']==cache['inputRefs'])
for label,mutation,token in [
    ('output-schema',{'outputSchemaDigest':'d'*64},'CACHE_OUTPUT_SCHEMA_JOIN'),
    ('producer',{'producerClosure':'closure2:'+'f'*64},'CACHE_STAGE_SPEC_PRODUCER_JOIN'),
    ('plan',{'planId':'plan2:'+'f'*64},'CACHE_PLAN_JOIN'),
    ('stage-spec-bytes',{'stageSpecDigest':'e'*64},'CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN')]:
    rejects_because('cache-hit-refuses-'+label,
        lambda m=mutation:M.admit_cache_entry('cache-key',{**cache,**m},run,objects,blobs),token)
rejects_because('cache-hit-refuses-an-unretained-consumed-view',
    lambda:M.admit_cache_entry('cache-key',{**cache,'inputRefs':[{'domain':'view','digest':'a'*64}]},run,objects,blobs),
    'EVIDENCE_UNAVAILABLE')
rejects_because('cache-hit-refuses-an-unretained-consumed-blob',
    lambda:M.admit_cache_entry('cache-key',{**cache,'inputRefs':[{'domain':'blob','digest':'b'*64}]},run,objects,blobs),
    'EVIDENCE_UNAVAILABLE')
rejects_because('cache-hit-refuses-a-scope-from-another-source',
    lambda:M.admit_cache_entry('cache-key',{**cache,'scopeIds':['scope2:'+'c'*64]},run,objects,blobs),
    'EVIDENCE_UNAVAILABLE')
# No guessed payload-domain schema: a bare payload reference is not an authoritative root.
for domain in ['coverage-payload','import-payload','fact-payload']:
    rejects_because('cache-hit-refuses-a-bare-payload-reference-'+domain,
        lambda d=domain:M.admit_cache_entry('cache-key',{**cache,'inputRefs':[{'domain':d,'digest':'d'*64}]},run,objects,blobs),
        'CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT:'+domain)
# A consumed native context must be one this Plan selected; an unselected one is not reusable input.
rejects_because('cache-hit-refuses-an-unselected-native-context',
    lambda:M.admit_cache_entry('cache-key',{**cache,'inputRefs':[{'domain':'native-context','digest':'e'*64}]},run,objects,blobs),
    'EVIDENCE_UNAVAILABLE')
selected_context=objects[run['planId']][1]['nativeContextDigests'][0]
check('cache-hit-admits-a-plan-selected-native-context',
      M.admit_cache_entry('cache-key',{**cache,'inputRefs':sorted(cache['inputRefs']+[{'domain':'native-context','digest':selected_context}],key=C.canonical)},
                          run,objects,blobs)['grantsEvidenceAuthority'] is False)
# A regeneration key is the same record under a different H domain, admitted identically.
check('regeneration-hit-admits-the-same-way',
      M.admit_cache_entry('regeneration-key',cache,run,objects,blobs)['identity']==regen_id)
# Codex's foreign-object hypothesis, ASSESSED rather than assumed. A view or scope from another
# Plan/source is self-consistent and hashes correctly; it still refuses, because the closure's
# ordinary Plan and source joins apply to objects first reached through a cache reference too.
foreign_run,foreign_objects,foreign_blobs=build(resolved=True,has_match=True,source_path='foreign.ts')
foreign_view=next(k for k,(d,v) in foreign_objects.items() if d=='view')
foreign_scope=next(k for k,(d,v) in foreign_objects.items() if d=='subject-scope')
mixed_objects={**objects,**foreign_objects};mixed_blobs={**blobs,**foreign_blobs}
check('foreign-view-is-self-consistent-and-correctly-hashed',
      M.identifier('view',foreign_objects[foreign_view][1])==foreign_view and
      foreign_objects[foreign_view][1]['planId']!=run['planId'])
rejects_because('cache-hit-refuses-a-self-consistent-foreign-view',
    lambda:M.admit_cache_entry('cache-key',{**cache,'inputRefs':[{'domain':'view','digest':foreign_view.split(':')[1]}]},
                               run,mixed_objects,mixed_blobs),'REFERENCE_PLAN_JOIN')
rejects_because('cache-hit-refuses-a-self-consistent-foreign-scope',
    lambda:M.admit_cache_entry('cache-key',{**cache,'scopeIds':[foreign_scope]},run,mixed_objects,mixed_blobs),
    'CACHE_SCOPE_SOURCE_JOIN')
check('cache-hit-still-admits-the-runs-own-view-in-the-mixed-store',
      M.admit_cache_entry('cache-key',cache,run,mixed_objects,mixed_blobs)['identity']==cache_id)
# A miss is not a failure and a hit never replaces a sealed Run: both semantics are unchanged.
check('cache-miss-is-not-modelled-as-a-refusal',M.cache_key('cache-key',cache)==cache_id)

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

# =========================================================================================
# Blind consumer Bv2 M-1 / M-2: the payload registry, and one fact2 encoding law.
# =========================================================================================
REGISTRY=M.PAYLOADS
check('payload-registry-is-closed-and-has-no-default-row',
      set(REGISTRY['classes'])=={'relation','coverage','import','parameter'} and
      'no default row' in REGISTRY['law']['unregistered'])
check('payload-schema-digest-is-the-full-document-bytes-not-a-selected-def',
      'EXACT FULL' in REGISTRY['law']['payloadSchemaDigest'])
check('a-multi-record-bundle-needs-no-root-type',
      'NEVER validated against a whole multi-record bundle' in REGISTRY['law']['validation'] and
      'never required to carry a root type' in REGISTRY['law']['validation'])
# The bundles the reviewer measured really do lack a root type, and that is now lawful.
for document in ['native/native-evidence.schemas.v2.json','workflows/schemas/imported-evidence.schema.json',
                 'workflows/schemas/test-execution.schema.json','foundation/relation-payload-schemas.v2.json']:
    check('registered-bundle-has-no-root-type-and-is-still-admissible-'+document.split('/')[-1],
          'type' not in json.loads((H.parent/document).read_text()))
check('relation-registry-covers-all-thirteen-relations',
      set(RELATION_REGISTRY)==set(json.loads(NATIVE_DOCUMENT.read_text())['$defs']['Relation']['enum']))
check('relation-registry-includes-the-native-extension',
      'unresolved-edge' in RELATION_REGISTRY and
      RELATION_REGISTRY['unresolved-edge']['rungs']=={'observed':{'required':[],'forbidden':[]}})
# Every inherited required/optional/type/enum/rung/universe law is reproduced exactly.
FACT_PLANE=json.loads((H.parents[1]/'artifacts/fact-plane.v1.json').read_text())
INHERITED=FACT_PLANE['factRecordContractV1']['relationPayloadSchemaRegistryV1']['schemas']
RELATION_DEFS=json.loads(RELATION_DOCUMENT.read_text())['$defs']
mapping_ok=True
for relation,row in INHERITED.items():
    mine=RELATION_REGISTRY[relation];definition=RELATION_DEFS[mine['selector'].split('/')[-1]]
    mapping_ok&= (mine['schemaId']==row['schemaId'] and mine['schemaVersion']==row['schemaVersion']
        and mine['universeRule']==row['universeRule']
        and mine['inheritedRequired']==sorted(row['required'])
        and mine['inheritedOptional']==sorted(row['optional'])
        and set(mine['rungs'])==set(row['resolutionRules'])
        and all(sorted(row['resolutionRules'][k]['required'])==v['required'] and
                sorted(row['resolutionRules'][k]['forbidden'])==v['forbidden'] for k,v in mine['rungs'].items())
        and definition['required']==sorted(row['required'])
        and set(definition['properties'])==set(row['fields'])
        and definition['additionalProperties'] is False)
    for field,kind in row['fields'].items():
        node=definition['properties'][field]
        if kind in row.get('enums',{}):mapping_ok&= node.get('enum')==row['enums'][kind]
check('relation-payloads-reproduce-every-inherited-required-optional-type-enum-rung-and-universe-law',mapping_ok)
check('fact2-encoding-successor-is-stated-in-the-document',
      'canonical JSON C, not the inherited deterministic-CBOR profile'
      in json.loads(RELATION_DOCUMENT.read_text())['description'])

def fact_mutation(fn,relation='references',resolution='resolved-binding'):
    """Re-mint a complete Run around a mutated fact and its payload, re-keying everything."""
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='fact');fact=copy.deepcopy(objects[key][1])
    payload=C.parse(blobs[fact['payloadDigest']]);original=fact['payloadDigest']
    fn(fact,payload,blobs)
    if fact['payloadDigest']==original:fact['payloadDigest']=put_blob(blobs,payload)
    rekey(objects,key,fact,run)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run);return M.close_run(run,objects,blobs)
check('fact-mutation-harness-positive-control-closes',fact_mutation(lambda f,p,b:None).startswith('run2:'))
# Schema-selector swap: a payload valid under ANOTHER relation's selector is refused.
rejects_because('fact-payload-under-another-relations-selector-refused',
    lambda:fact_mutation(lambda f,p,b:p.clear() or p.update({'importer':'symbol:foo','specifier':'./x','resolvedTarget':'symbol:foo'})),
    'PAYLOAD_RECORD:#/$defs/ReferencesPayloadV1')
rejects_because('fact-relation-must-be-registered',
    lambda:fact_mutation(lambda f,p,b:f.update(relation='made-up-relation')),
    'PAYLOAD_RELATION_UNREGISTERED:made-up-relation')
rejects_because('fact-resolution-must-be-a-rung-of-that-relations-ladder',
    lambda:fact_mutation(lambda f,p,b:f.update(resolution='checked')),
    'RELATION_RUNG_NOT_IN_LADDER:references@checked')
rejects_because('fact-rung-forbidden-field-refused',
    lambda:fact_mutation(lambda f,p,b:(f.update(resolution='syntactic-name-match'))),
    'RELATION_RUNG_FORBIDDEN_FIELD:resolvedBinding')
rejects_because('fact-rung-required-field-refused',
    lambda:fact_mutation(lambda f,p,b:p.pop('resolvedBinding')),
    'RELATION_RUNG_REQUIRED_FIELD:resolvedBinding')
# A permissive root: the caller offers a schema document that admits anything.
PERMISSIVE={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:hostile:permissive','type':'object'}
rejects_because('fact-payload-schema-cannot-be-a-caller-chosen-permissive-document',
    lambda:fact_mutation(lambda f,p,b:f.update(payloadSchemaDigest=put_blob(b,PERMISSIVE))),
    'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT')
# An unknown registry: the caller cites a real but unregistered document.
rejects_because('fact-payload-schema-cannot-be-an-unregistered-real-document',
    lambda:fact_mutation(lambda f,p,b:f.update(payloadSchemaDigest=put_blob(b,(H/'identity-schemas.v2.json').read_bytes()))),
    'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT')
# CBOR vs CJSON: the superseded codec's bytes are not a fact2 preimage.
CBOR_REFERENCES=bytes.fromhex('a2686e616d6563666f6f687265666572726572')
rejects_because('deterministic-cbor-bytes-are-not-a-fact2-payload-preimage',
    lambda:fact_mutation(lambda f,p,b:f.update(payloadDigest=put_blob(b,CBOR_REFERENCES))),
    "'utf-8' codec can't decode")
check('cbor-and-canonical-json-digests-of-one-payload-differ',
      hashlib.sha256(CBOR_REFERENCES).hexdigest()!=hashlib.sha256(C.canonical(REFERENCES_PAYLOAD)).hexdigest())
# Type profile: the retained restrictions of the superseded CBOR profile still bite under C.
rejects_because('relation-payload-non-nfc-text-refused',
    lambda:fact_mutation(lambda f,p,b:p.update(name='é')),'RELATION_PAYLOAD_NOT_NFC')
check('canonical-encoder-still-admits-non-nfc-text-elsewhere',
      C.canonical({'x':'é'})!=C.canonical({'x':'é'}))
rejects_because('relation-payload-negative-integer-refused',
    lambda:fact_mutation(lambda f,p,b:p.clear() or p.update({'path':'a.ts','contentSha256':'a'*64,'byteLength':-1}) or f.update(relation='file',resolution='enumerated')),
    'PAYLOAD_RECORD:#/$defs/FilePayloadV1')
# universeRule same-only is enforced for a same-only relation.
def same_only_run():
    """A `declares` fact (universeRule same-only) whose two universes differ. The scope, view,
    witness and proof are all re-derived so the refusal is the universe rule, not staleness."""
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='fact');fact=copy.deepcopy(objects[key][1])
    universe=M.parse_h_frame(blobs[fact['sourceUniverse']],'native-semantic-universe')[1]
    other=M.retain_h_identity('native.semantic-universe.typescript.v2',{**universe,'jsRootFiles':['b.js']},blobs)
    fact.update(relation='declares',resolution='syntactic',targetUniverse=other,
                payloadDigest=put_blob(blobs,{'container':'symbol:m','declared':'symbol:foo','declarationKind':'function'}))
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    rekey(objects,scope_key,dict(objects[scope_key][1],relation='declares',resolution='syntactic'),run)
    rekey(objects,key,fact,run);resync_coverage(objects,blobs,run)
    view_key=next(k for k,(d,v) in objects.items() if d=='view');view=objects[view_key][1]
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run);return M.close_run(run,objects,blobs)
rejects_because('same-only-relation-refuses-two-universes',same_only_run,'RELATION_UNIVERSE_RULE:same-only')

# Coverage and import classes resolve through the same registry.
check('coverage-payload-is-the-registered-coverage-result-v3',
      C.parse(blobs[next(v for k,(d,v) in objects.items() if d=='coverage')['payloadDigest']])['schemaVersion']==3)
def coverage_schema_swap():
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='coverage');coverage=copy.deepcopy(objects[key][1])
    coverage['payloadSchemaDigest']=put_blob(blobs,PERMISSIVE)
    rekey(objects,key,coverage,run)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run);return run,objects,blobs
rejects_because('coverage-payload-schema-cannot-be-a-caller-chosen-document',
    lambda:M.close_run(*coverage_schema_swap()),'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT')
check('import-registry-rows-mirror-the-workflow-registry',
      all(REGISTRY['classes']['import']['rows'][k+'|'+d]['document']==row['schemaDocument'] and
          REGISTRY['classes']['import']['rows'][k+'|'+d]['selector']==row['selector']
          for (k,d),row in W.PAYLOAD_REGISTRY.items()))
check('real-import-wrapper-kind-closes-a-run',M.close_run(*graph_with_import()).startswith('run2:'))
check('the-real-import-uses-a-registered-kind-and-payload-domain',
      C.parse(graph_with_import()[2][next(v for k,(d,v) in graph_with_import()[1].items() if d=='import')['payloadDigest']])['payloadDomain']
      =='workflow.import-payload.runtime.v1')
def bad_parameter_document():
    run,objects,blobs=graph_with_import(correspondence='vcs',build_identity='build-a',declared_builds=['build-a'])
    plan=copy.deepcopy(objects[run['planId']][1]);spec=C.parse(blobs[plan['analysisSpecDigest']])
    spec['parameters']=[{'schemaDigest':put_blob(blobs,PERMISSIVE),'payloadDigest':put_blob(blobs,{'schemaVersion':1,'declaredBuildIds':[]})}]
    plan['analysisSpecDigest']=put_blob(blobs,spec);rekey_plan(objects,blobs,run,plan)
    resync_proof_refs(objects,blobs,run)
    return run,objects,blobs
rejects_because('parameter-schema-must-be-on-the-closed-list',
    lambda:M.close_run(*bad_parameter_document()),'PAYLOAD_PARAMETER_UNREGISTERED')

# =========================================================================================
# The Rust semantic-universe path (native section 2.1/3.3/3.4/11). native-evidence already
# registered native.semantic-universe.rust.v2 and RustUniverseV2ResolvedInputs; the identity
# registry now carries it, the owning contract now supplies bind_rust_universe, and a complete
# Rust universe / fact / Coverage Run closes. A Rust CONTEXT inside a TypeScript Run was never
# the Rust path.
# =========================================================================================
UNIVERSE_SET=M.DIGESTS['domainSets']['native-semantic-universe']
check('rust-universe-domain-is-registered','native.semantic-universe.rust.v2' in UNIVERSE_SET)
check('rust-universe-binding-entry-point-exists',
      hasattr(N,UNIVERSE_SET['native.semantic-universe.rust.v2']['binding']['entryPoint']))
check('both-universe-domains-native-section-11-names-are-registered',
      set(UNIVERSE_SET)==set(N.NATIVE_UNIVERSE_DOMAINS.values()))
check('cargo-config-projection-domain-is-named-and-shared',
      N.CARGO_CONFIG_PROJECTION_DOMAIN=='native.cargo-config-projection.v2' and
      N.CARGO_CONFIG_PROJECTION_DOMAIN in M.DIGESTS['domainSets']['native-nested'])
# A complete positive Rust Run: rust-v2 universe, its facts and its Coverage.
rrun,robjects,rblobs=build(resolved=True,has_match=True,universe_language='rust')
rust_run_id=M.close_run(rrun,robjects,rblobs)
check('rust-universe-complete-run-closes',rust_run_id.startswith('run2:'))
rscope=next(v for k,(d,v) in robjects.items() if d=='subject-scope')
rfact=next(v for k,(d,v) in robjects.items() if d=='fact')
rust_universe_digest=M.parse_h_frame(rblobs[rscope['sourceUniverse']],'native-semantic-universe')
check('rust-run-scope-and-fact-carry-the-rust-universe',
      rust_universe_digest[0]=='native.semantic-universe.rust.v2' and
      rfact['sourceUniverse']==rscope['sourceUniverse']==rscope['targetUniverse'])
check('rust-run-coverage-binds-the-rust-scope',
      next(v for k,(d,v) in robjects.items() if d=='coverage')['scopeId'] in
      next(v for k,(d,v) in robjects.items() if d=='view')['scopeIds'])
check('rust-and-typescript-runs-are-different-runs',rust_run_id!=M.close_run(*build(resolved=True,has_match=True)))
store=M.EvidenceStore();reid='exec1_'+'b'*32
check('rust-run-replays-and-commits',
      store.prepare(rrun,robjects,rblobs,reid,replay)==rust_run_id and store.commit(reid)=='committed')
# Every nested Rust semantic identity is a retained record of its registered domain.
NESTED=M.DIGESTS['domainSets']['native-nested']
rctx=M.parse_h_frame(rblobs[next(d for d in robjects[rrun['planId']][1]['nativeContextDigests']
    if M.parse_h_frame(rblobs[d],'native-context')[0]=='native.context.rust.v2')],'native-context')[1]
for field,domain in [('dependencySourceSetId','native.dependency-source-set.v1'),
                     ('unifiedFeaturesId','native.unified-features.rust.v1')]:
    check('rust-nested-identity-is-a-retained-record-'+field,
          M.parse_h_frame(rblobs[rctx[field].removeprefix('sha256:')],'native-nested')[0]==domain)
check('rust-config-projection-identity-is-the-named-domain',
      M.parse_h_frame(rblobs[rust_universe_digest[1]['configProjectionSha256']],'native-nested')[0]==N.CARGO_CONFIG_PROJECTION_DOMAIN)
check('rust-config-projection-file-digest-is-not-the-record-identity',
      rctx['configProjection']['projectionSha256']!=rust_universe_digest[1]['configProjectionSha256'] and
      rctx['configProjection']['projectionSha256']==hashlib.sha256(RUST_PROJECTED_CONFIG).hexdigest())
dependency=M.parse_h_frame(rblobs[rctx['dependencySourceSetId'].removeprefix('sha256:')],'native-nested')[1]
check('rust-dependency-package-file-manifest-is-a-retained-record',
      M.parse_h_frame(rblobs[dependency['packages'][0]['fileManifestSha256']],'native-nested')[0]
      =='native.dependency-file-manifest.v1')
check('rust-dependency-member-bytes-are-retained',
      all(row['contentSha256'] in rblobs and len(rblobs[row['contentSha256']])==row['byteLength']
          for row in M.parse_h_frame(rblobs[dependency['packages'][0]['fileManifestSha256']],'native-nested')[1]))

# The Rust positive is a coherent same-language request: the requested capability, the analysed
# source, the fact anchor and the rule's subject universe all name Rust.
rspec=C.parse(rblobs[robjects[rrun['planId']][1]['analysisSpecDigest']])
rpolicy=C.parse(rblobs[robjects[rrun['planId']][1]['policyDigest']])
check('rust-run-request-source-and-rule-are-one-language',
      rspec['requestedCapabilities'][0]['languageMode']=='rust-cargo' and
      rpolicy['rules'][0]['subjectEnumeration']['universe']=='rust' and
      rfact['anchors'][0]['path']=='src/lib.rs' and
      rblobs[rfact['anchors'][0]['blobDigest']]==RUST_SOURCES['src/lib.rs'])
check('typescript-run-request-source-and-rule-are-one-language',
      C.parse(blobs[objects[run['planId']][1]['analysisSpecDigest']])['requestedCapabilities'][0]['languageMode']=='ts-tsconfig' and
      C.parse(blobs[objects[run['planId']][1]['policyDigest']])['rules'][0]['subjectEnumeration']['universe']=='typescript')
# A universe of a language the Plan never requested is not analysis this Plan asked for.
def wrong_language_request(mode):
    def go():
        r,o,b=build(resolved=True,has_match=True,universe_language='rust')
        plan=copy.deepcopy(o[r['planId']][1]);spec=C.parse(b[plan['analysisSpecDigest']])
        spec['requestedCapabilities'][0]['languageMode']=mode
        plan['analysisSpecDigest']=put_blob(b,spec);rekey_plan(o,b,r,plan)
        return M.close_run(r,o,b)
    return go
rejects_because('rust-universe-needs-a-rust-language-mode-request',wrong_language_request('ts-tsconfig'),
                'UNIVERSE_LANGUAGE_NOT_REQUESTED:rust')
rejects_because('syntax-only-requests-no-semantic-universe',wrong_language_request('syntax-only'),
                'UNIVERSE_LANGUAGE_NOT_REQUESTED:rust')
rejects_because('an-unregistered-language-mode-refuses',wrong_language_request('cobol-classic'),
                'ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED:cobol-classic')

def rust_run(mutate_universe=None,mutate_context=None,retain=None):
    """Fully re-frame and re-key a complete Rust Run around a mutated context/universe. `retain`
    runs against the actual graph blobs first and its result is passed to the mutators, so an
    attack can point a field at a second GENUINELY retained record instead of an absent one. The
    positive control proves a refusal is attributable to the mutation, not to staleness."""
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust')
    extra=retain(blobs) if retain is not None else None
    plan=copy.deepcopy(objects[run['planId']][1])
    old_context=next(d for d in plan['nativeContextDigests']
                     if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')
    context=M.parse_h_frame(blobs[old_context],'native-context')[1]
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    if mutate_context is not None:
        mutate_context(context,extra)
        new_context=M.retain_h_identity('native.context.rust.v2',context,blobs)
        plan['nativeContextDigests']=sorted([d for d in plan['nativeContextDigests'] if d!=old_context]+[new_context])
        universe['nativeContextId']='sha256:'+new_context
    if mutate_universe is not None:mutate_universe(universe,extra)
    new_universe=M.retain_h_identity('native.semantic-universe.rust.v2',universe,blobs)
    for key in [k for k,(d,v) in objects.items() if d in ('fact','subject-scope')]:
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new_universe,targetUniverse=new_universe),run)
    rekey_plan(objects,blobs,run,plan)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run)
    return M.close_run(run,objects,blobs)
check('rust-run-harness-positive-control-closes',rust_run().startswith('run2:'))
# Universe/context overlap. Each attack points the universe at a SECOND genuinely retained record
# of the right registered domain, so the refusal is the overlap rule and not missing retention.
OTHER_FEATURES={'schemaVersion':1,'resolverVersion':2,'targetTriple':RUST_TARGET,
    'activated':[{'packageKey':RUST_DEP_KEY,'features':['default','extra']}],
    'computedBy':{'producer':'opensip-cargo-adapter','producerBuildId':'fixture-adapter-2'}}
OTHER_TARGET_FEATURES={**OTHER_FEATURES,'targetTriple':'x86_64-unknown-linux-gnu',
    'activated':[{'packageKey':RUST_DEP_KEY,'features':['default']}]}
OTHER_PROJECTION_MARK=b'[build]\nrustflags = ["--cfg", "other"]\n'
def retain_features(features):
    return lambda blobs:'sha256:'+M.retain_h_identity(N.UNIFIED_FEATURES_DOMAIN,features,blobs)
rejects_because('rust-universe-overlap-unifiedFeaturesId',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(unifiedFeaturesId=x),retain=retain_features(OTHER_FEATURES)),
    'NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:unifiedFeaturesId')
rejects_because('rust-universe-overlap-dependencySourceSetId',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(dependencySourceSetId=x),
                    retain=lambda blobs:'sha256:'+M.retain_h_identity(N.DEPENDENCY_SOURCE_SET_DOMAIN,
                        {'schemaVersion':1,'language':'rust',
                         'lockfileIdentity':{'path':'Cargo.lock','contentSha256':hashlib.sha256(RUST_SOURCES['Cargo.lock']).hexdigest(),'lockfileVersion':3},
                         'packages':[],'completeness':{'state':'complete','missing':[]}},blobs)),
    'NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH:dependencySourceSetId')
def retain_other_projection(blobs):
    projection={'schemaVersion':2,'honoredKeys':['build.rustflags'],'strippedKeys':['build.rustc'],
                'replacedSnapshotConfigs':['.cargo/config.toml'],
                'rustflags':{'honored':['--cfg fixture'],'stripped':[],'executableSelected':False},
                'ancestorCarrierVerified':True,'cargoHome':'private-empty','environmentProjection':'none',
                'claimsCargoSwitch':False,'projectionSha256':put_blob(blobs,OTHER_PROJECTION_MARK)}
    return M.retain_h_identity(N.CARGO_CONFIG_PROJECTION_DOMAIN,projection,blobs)
rejects_because('rust-universe-overlap-configProjectionSha256',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(configProjectionSha256=x),retain=retain_other_projection),
    'native.universe-context-field-mismatch:configProjectionSha256')
rejects_because('rust-universe-overlap-rustflags',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(rustflags={'honored':['--cfg other'],'stripped':[],'executableSelected':False})),
    'native.universe-context-field-mismatch:rustflags')
rejects_because('rust-universe-cfg-set-may-not-drop-a-base-cfg',
    lambda:rust_run(mutate_universe=lambda u,x:u['cfgSets'].__setitem__(0,{'cfgSetId':'primary','cfg':['target_os="macos"']})),
    'native.universe-context-field-mismatch:cfgSets.primary')
rejects_because('rust-universe-duplicate-cfg-set-refused-by-the-native-schema',
    lambda:rust_run(mutate_universe=lambda u,x:u['cfgSets'].__setitem__(1,dict(u['cfgSets'][0]))),
    'H_FRAME_RECORD:native.semantic-universe.rust.v2')
# executionCapableResolution is a statement about the resolution, never an execution grant.
rejects_because('rust-universe-execution-capable-must-match-prepared-resolution',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(executionCapableResolution=True)),
    'native.universe-context-field-mismatch:executionCapableResolution')
rejects_because('rust-universe-prepared-resolution-without-a-prepared-set',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(preparedResolution='host-prepared',executionCapableResolution=True)),
    'PREPARED_RESOLUTION_MODE_NOT_REQUESTED:rust-cargo-prepared')
# Source correspondence against the analysed snapshot.
rejects_because('rust-universe-crate-root-not-inventoried',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(crateRootPaths=['src/absent.rs'])),
    'NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:src/absent.rs')
rejects_because('rust-universe-lockfile-bytes-are-not-the-snapshot-bytes',
    lambda:rust_run(mutate_universe=lambda u,x:u['lockfileIdentity'].update(contentSha256='d'*64)),
    'NATIVE_UNIVERSE_SOURCE_MISMATCH:Cargo.lock')
rejects_because('rust-context-replaced-snapshot-config-not-inventoried',
    lambda:rust_run(mutate_context=lambda c,x:c['configProjection']['replacedSnapshotConfigs'].append('zz-absent-config.toml')),
    'NATIVE_CONTEXT_PATH_NOT_INVENTORIED:zz-absent-config.toml')
# Nested retained records must actually join their universe and context.
rejects_because('rust-universe-lockfile-must-match-the-dependency-set',
    lambda:rust_run(mutate_universe=lambda u,x:u['lockfileIdentity'].update(lockfileVersion=4)),
    'native.universe-retained-input-mismatch:lockfileIdentity')
rejects_because('rust-unified-features-must-be-for-the-context-target',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(unifiedFeaturesId=x),
                    mutate_context=lambda c,x:c.update(unifiedFeaturesId=x),
                    retain=retain_features(OTHER_TARGET_FEATURES)),
    'native.universe-retained-input-mismatch:unifiedFeatures.targetTriple')
# Missing retained data is operational retention loss, not a malformed record.
def drop_nested(field):
    def go():
        run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust')
        context=M.parse_h_frame(blobs[next(d for d in objects[run['planId']][1]['nativeContextDigests']
            if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')],'native-context')[1]
        blobs=dict(blobs);blobs.pop(context[field].removeprefix('sha256:'))
        return M.close_run(run,objects,blobs)
    return go
for field in ['dependencySourceSetId','unifiedFeaturesId']:
    rejects_because('rust-nested-frame-missing-is-retention-loss-'+field,drop_nested(field),'EVIDENCE_UNAVAILABLE')
def drop_dependency_member():
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust')
    blobs=dict(blobs);blobs.pop(hashlib.sha256(RUST_DEP_FILE).hexdigest())
    return M.close_run(run,objects,blobs)
rejects_because('rust-dependency-member-bytes-missing-is-retention-loss',drop_dependency_member,'EVIDENCE_UNAVAILABLE')
def malformed_nested():
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust')
    context=M.parse_h_frame(blobs[next(d for d in objects[run['planId']][1]['nativeContextDigests']
        if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')],'native-context')[1]
    digest=context['dependencySourceSetId'].removeprefix('sha256:')
    blobs=dict(blobs);blobs[digest]=b'\x00not a frame'
    return M.close_run(run,objects,blobs)
rejects_because('rust-nested-malformed-bytes-are-not-retention-loss',malformed_nested,'BLOB_DIGEST')
# raw C(X) is not H(D,X), in this domain set as in every other.
rejects_because('rust-nested-raw-canonical-sha-is-not-an-h-identity',
    lambda:rust_run(mutate_universe=lambda u,x:u.update(unifiedFeaturesId=x),
                    mutate_context=lambda c,x:c.update(unifiedFeaturesId=x),
                    retain=lambda blobs:'sha256:'+put_blob(blobs,OTHER_FEATURES)),
    'H_FRAME_PREFIX')

check('rust-nested-raw-and-h-digests-differ',
      hashlib.sha256(C.canonical(rctx)).hexdigest()!=C.identity('native.context.rust.v2',rctx))
# A universe may never bind a context of another language, in either direction.
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
def rust_universe_on_ts_context():
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust')
    ts=next(d for d in objects[run['planId']][1]['nativeContextDigests']
            if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')
    return rust_run(mutate_universe=lambda u,x:u.update(nativeContextId='sha256:'+ts))
rejects_because('rust-universe-cannot-bind-a-typescript-context',rust_universe_on_ts_context,
                'NATIVE_UNIVERSE_CONTEXT_LANGUAGE:native.context.typescript.v2')

# --- native-boundary unit checks for bind_rust_universe -----------------------------------------
# Rules the owning contract enforces that a Run closure cannot reach, because the closure always
# supplies exactly what the universe names. Exercised directly against the fixture's own admitted
# records. (These could equally live in native-cases.v2.json; they are here so that adding them does
# not churn the native suite's generated report while Codex finalizes pins.)
def rust_fixture():
    objects={};blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest
    def add(domain,**fields):
        value={'schemaVersion':2,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
    def tree(files):return sorted(({'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in files.items()),key=lambda r:r['path'].encode())
    sources={**TS_SOURCES,**RUST_SOURCES,'a.ts':b'export const foo = 1;\n'}
    inventory=sorted([{'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in sources.items()],key=lambda r:r['path'].encode())
    both=native_inputs(objects,blobs,add,blob,ts_inventory=inventory)
    parts=both['rust']
    retained={'dependencySourceSet':parts['dependency'],'unifiedFeatures':parts['features']}
    return parts,retained,inventory,both['admission']
RPARTS,RRETAINED,RINVENTORY,NATIVE_ADMISSION_TS=rust_fixture()
check('native-bind-rust-universe-admits-the-fixture',
      N.bind_rust_universe(RPARTS['universe'],RPARTS['admission'],RPARTS['context'],RRETAINED,RINVENTORY)['result']=='ADMIT')
check('native-bind-rust-universe-mints-the-registered-domain',
      N.bind_rust_universe(RPARTS['universe'],RPARTS['admission'],RPARTS['context'],RRETAINED,RINVENTORY)['universeId']
      =='sha256:'+RPARTS['universeDigest'])
def rust_binding_refusals(**overrides):
    args={'universe':RPARTS['universe'],'admission':RPARTS['admission'],'context':RPARTS['context'],
          'retained':RRETAINED,'snapshot_inventory':RINVENTORY}
    args.update(overrides)
    return N.bind_rust_universe(args['universe'],args['admission'],args['context'],args['retained'],args['snapshot_inventory'])['refusals']
check('native-bind-rust-universe-has-no-input-free-admit-path',
      'native.universe-retained-inputs-not-supplied' in rust_binding_refusals(retained=None) and
      'native.universe-retained-inputs-not-supplied' in rust_binding_refusals(snapshot_inventory=None))
check('native-bind-rust-universe-has-no-context-free-admit-path',
      'native.universe-context-not-supplied' in rust_binding_refusals(context=None))
check('native-bind-rust-universe-refuses-a-typescript-admission',
      any(x.startswith('native.native-context-language-mismatch:rust-universe-bound-to-')
          for x in rust_binding_refusals(admission=NATIVE_ADMISSION_TS)))
check('native-bind-rust-universe-refuses-an-unselected-prepared-set',
      'native.universe-retained-input-unselected:preparedOutputSet' in
      rust_binding_refusals(retained={**RRETAINED,'preparedOutputSet':{'schemaVersion':3,
          'preparation':{'kind':'imported-descriptor','authorizationId':None,'importId':None,
              'toolchain':RPARTS['context']['toolchain'],
              'dependencySourceSetId':RPARTS['context']['dependencySourceSetId'],'cfgSetId':'primary',
              'producer':{'id':'opensip-native-prepare','version':'1.0.0'}},'rows':[]}}))
check('native-bind-rust-universe-refuses-a-missing-required-input',
      'native.universe-retained-input-missing:unifiedFeatures' in
      rust_binding_refusals(retained={'dependencySourceSet':RRETAINED['dependencySourceSet']}))
check('native-bind-rust-universe-refuses-a-dependency-set-that-is-not-the-named-identity',
      'native.universe-retained-input-identity-mismatch:dependencySourceSetId' in
      rust_binding_refusals(retained={**RRETAINED,'dependencySourceSet':
          {**RRETAINED['dependencySourceSet'],'completeness':{'state':'incomplete','missing':[
              {'name':'x','version':'1','sourceId':'registry+https://example.invalid'}]}}}))
check('native-cargo-config-projection-identity-is-not-the-projected-file-digest',
      N.cargo_config_projection_identity(RPARTS['projection']).removeprefix('sha256:')
      !=RPARTS['projection']['projectionSha256'])
# The Plan-level language-mode join fires first inside a Run, so this rule is checked where it lives.
check('native-binding-refuses-a-prepared-resolution-with-no-prepared-set',
      'native.universe-context-field-mismatch:preparedOutputSetId' in
      N.bind_rust_universe({**RPARTS['universe'],'preparedResolution':'host-prepared','executionCapableResolution':True},
                           RPARTS['admission'],RPARTS['context'],RRETAINED,RINVENTORY)['refusals'])
check('native-cargo-config-projection-identity-is-not-raw-canonical-sha',
      N.cargo_config_projection_identity(RPARTS['projection']).removeprefix('sha256:')
      !=hashlib.sha256(C.canonical(RPARTS['projection'])).hexdigest())

# --- prepared products are inert data; execution authority stays operational -------------------
# The retained inert rows enter the resolution; the universe's preparedResolution projects the
# operational grant operation the native contract names. Retained bytes never imply a grant.
IMPORTED_OPS=['native-analysis','read-import','read-source']
prun,pobjects,pblobs=build(resolved=True,has_match=True,universe_language='rust',
                           prepared='imported-descriptor',grant_operations=IMPORTED_OPS)
check('rust-imported-inert-prepared-run-closes',M.close_run(prun,pobjects,pblobs).startswith('run2:'))
check('prepared-run-requests-the-prepared-language-mode',
      C.parse(pblobs[pobjects[prun['planId']][1]['analysisSpecDigest']])['requestedCapabilities'][0]['languageMode']=='rust-cargo-prepared')
pctx=M.parse_h_frame(pblobs[next(d for d in pobjects[prun['planId']][1]['nativeContextDigests']
    if M.parse_h_frame(pblobs[d],'native-context')[0]=='native.context.rust.v2')],'native-context')[1]
prepared_record=M.parse_h_frame(pblobs[pctx['preparedOutputSetId'].removeprefix('sha256:')],'native-nested')
check('prepared-output-set-is-a-retained-record-of-its-domain',
      prepared_record[0]=='native.prepared-output-set.v3')
check('prepared-inert-row-bytes-are-retained-with-their-exact-length',
      all(row['blob']['sha256'] in pblobs and len(pblobs[row['blob']['sha256']])==row['blob']['byteLength']
          for row in prepared_record[1]['rows']))
rejects_because('imported-inert-resolution-needs-read-import-in-the-grant',
    lambda:M.close_run(*build(resolved=True,has_match=True,universe_language='rust',
                              prepared='imported-descriptor',grant_operations=['native-analysis','read-source'])),
    'PREPARED_RESOLUTION_GRANT_JOIN:read-import')
rejects_because('host-prepared-resolution-needs-prepare-code-in-the-grant',
    lambda:M.close_run(*build(resolved=True,has_match=True,universe_language='rust',
                              prepared='authorized-execution',grant_operations=IMPORTED_OPS)),
    'PREPARED_RESOLUTION_GRANT_JOIN:prepare-code')
def drop_prepared_row_bytes():
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust',
                            prepared='imported-descriptor',grant_operations=IMPORTED_OPS)
    blobs=dict(blobs);blobs.pop(hashlib.sha256(RUST_PREPARED_DIRECTIVES).hexdigest())
    return M.close_run(run,objects,blobs)
rejects_because('prepared-inert-row-bytes-missing-is-retention-loss',drop_prepared_row_bytes,'EVIDENCE_UNAVAILABLE')
def wrong_prepared_dependency_set():
    return rust_run_prepared(lambda record:record['preparation'].update(dependencySourceSetId='sha256:'+'e'*64))
def rust_run_prepared(mutate_record):
    """Re-frame a prepared Run with a mutated prepared-output record, re-keying everything."""
    run,objects,blobs=build(resolved=True,has_match=True,universe_language='rust',
                            prepared='imported-descriptor',grant_operations=IMPORTED_OPS)
    plan=copy.deepcopy(objects[run['planId']][1])
    old_context=next(d for d in plan['nativeContextDigests']
                     if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.rust.v2')
    context=M.parse_h_frame(blobs[old_context],'native-context')[1]
    record=M.parse_h_frame(blobs[context['preparedOutputSetId'].removeprefix('sha256:')],'native-nested')[1]
    mutate_record(record)
    new_prepared='sha256:'+M.retain_h_identity(N.PREPARED_OUTPUT_SET_DOMAIN,record,blobs)
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    context['preparedOutputSetId']=new_prepared
    new_context=M.retain_h_identity('native.context.rust.v2',context,blobs)
    plan['nativeContextDigests']=sorted([d for d in plan['nativeContextDigests'] if d!=old_context]+[new_context])
    universe.update(nativeContextId='sha256:'+new_context,preparedOutputSetId=new_prepared)
    new_universe=M.retain_h_identity('native.semantic-universe.rust.v2',universe,blobs)
    for key in [k for k,(d,v) in objects.items() if d in ('fact','subject-scope')]:
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new_universe,targetUniverse=new_universe),run)
    rekey_plan(objects,blobs,run,plan)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    witness=C.parse(blobs[proof['predicateProofs'][0]['witnessDigest']])
    witness.update(matchingFactIds=view['facts'],coverageIds=view['coverageIds'])
    proof['predicateProofs'][0].update(witnessDigest=put_blob(blobs,witness),scopeIds=view['scopeIds'])
    rekey(objects,pk,proof,run)
    return M.close_run(run,objects,blobs)
check('prepared-run-harness-positive-control-closes',rust_run_prepared(lambda r:None).startswith('run2:'))
rejects_because('prepared-set-bound-to-another-dependency-set-refused',
    lambda:rust_run_prepared(lambda r:r['preparation'].update(dependencySourceSetId='sha256:'+'e'*64)),
    'native.universe-retained-input-mismatch:preparedOutputSet.dependencySourceSetId')
rejects_because('prepared-set-bound-to-another-cfg-set-refused',
    lambda:rust_run_prepared(lambda r:r['preparation'].update(cfgSetId='not-a-declared-set')),
    'native.universe-retained-input-mismatch:preparedOutputSet.cfgSetId')
rejects_because('prepared-set-kind-must-match-the-declared-resolution',
    lambda:rust_run_prepared(lambda r:r['preparation'].update(kind='authorized-execution',
        authorizationId='sha256:'+'f'*64)),
    'native.universe-retained-input-mismatch:preparedResolution')

# --- Root counterexamples v8: payload memo context, and Coverage producer re-admission ---------
# 1. Two facts sharing one canonical payload owe DIFFERENT admissions. Caching the decode must never
#    cache the admission, and the regression needs two facts, not the invalid one alone.
def two_fact_graph(second):
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='fact');valid=copy.deepcopy(objects[key][1])
    other=copy.deepcopy(valid);second(other,blobs)
    other_key=M.identifier('fact',other);objects[other_key]=('fact',other)
    view_key=next(k for k,(d,v) in objects.items() if d=='view');view=copy.deepcopy(objects[view_key][1])
    view['facts']=sorted(set(view['facts']+[other_key]),key=C.canonical)
    rekey(objects,view_key,view,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
check('two-fact-memo-harness-positive-control-closes',
      two_fact_graph(lambda f,b:f['anchors'][0].update(endByte=f['anchors'][0]['endByte']-1)).startswith('run2:'))
rejects_because('shared-payload-does-not-cache-a-second-facts-schema-admission',
    lambda:two_fact_graph(lambda f,b:(f['anchors'][0].update(endByte=f['anchors'][0]['endByte']-1),
                                      f.update(payloadSchemaDigest=put_blob(b,PERMISSIVE)))),
    'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT')
rejects_because('shared-payload-does-not-cache-a-second-facts-rung-admission',
    lambda:two_fact_graph(lambda f,b:(f['anchors'][0].update(endByte=f['anchors'][0]['endByte']-1),
                                      f.update(resolution='syntactic-name-match'))),
    'RELATION_RUNG_FORBIDDEN_FIELD:resolvedBinding')
# 2. Validating a Coverage payload under its registered selector proves shape, never admission. The
#    host re-runs the ACTUAL native producer admission over the retained scope and unresolved facts.
def coverage_payload_mutation(mutate):
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='coverage');coverage=copy.deepcopy(objects[key][1])
    payload=C.parse(blobs[coverage['payloadDigest']]);mutate(payload)
    coverage['payloadDigest']=put_blob(blobs,payload)
    rekey(objects,key,coverage,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
check('coverage-mutation-harness-positive-control-closes',coverage_payload_mutation(lambda p:None).startswith('run2:'))
rejects_because('self-rehashed-coverage-with-a-wrong-subject-count-refuses',
    lambda:coverage_payload_mutation(lambda p:p['entry']['examinedUniverse'].update(subjectCount=999)),
    'COVERAGE_PRODUCER_ADMISSION:native.examined-universe-subject-count-mismatch')
rejects_because('self-rehashed-coverage-claiming-complete-without-attempt-refuses',
    lambda:coverage_payload_mutation(lambda p:p['entry']['resolutionCompleteness'].update(attempted=False)),
    'RC-2: complete requires attempted')
rejects_because('self-rehashed-coverage-with-a-claimant-chosen-commitment-refuses',
    lambda:coverage_payload_mutation(lambda p:p['key'].update(subjectScopeCommitment='sha256:'+'a'*64)),
    'COVERAGE_PRODUCER_ADMISSION:native.subject-scope-commitment-mismatch')
rejects_because('self-rehashed-coverage-whose-key-leaves-its-scope-refuses',
    lambda:coverage_payload_mutation(lambda p:p['key'].update(relation='calls')),
    'native.coverage-key-scope-mismatch:relation')
# 3. ADV-B1: the two committed budgets must agree; neither source silently wins.
def budget_mismatch():
    run,objects,blobs=build(resolved=True,has_match=True)
    plan=copy.deepcopy(objects[run['planId']][1]);plan['budget']={'unit':'work-units','limit':999}
    rekey_plan(objects,blobs,run,plan);return M.close_run(run,objects,blobs)
rejects_because('plan-budget-must-equal-the-committed-resolved-configuration-budget',budget_mismatch,
                'PLAN_BUDGET_CONFIG_JOIN')
def budget_override_in_both():
    run,objects,blobs=build(resolved=True,has_match=True)
    plan=copy.deepcopy(objects[run['planId']][1]);config=C.parse(blobs[plan['resolvedConfigDigest']])
    config['analysis']['budget']={'unit':'work-units','limit':5000}
    plan['budget']={'unit':'work-units','limit':5000};plan['resolvedConfigDigest']=put_blob(blobs,config)
    snapshot_key=run['snapshotId'];snapshot=copy.deepcopy(objects[snapshot_key][1])
    snapshot['resolvedConfigDigest']=plan['resolvedConfigDigest']
    rekey(objects,snapshot_key,snapshot,run)
    plan['snapshotId']=run['snapshotId'];rekey_plan(objects,blobs,run,plan)
    resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
check('a-legitimate-budget-override-must-be-in-the-resolved-configuration-first',
      budget_override_in_both().startswith('run2:'))

# --- G6: the capability manifest can express the thirteenth relation, and admission bites --------
CAP_DOMAINS=json.loads((H.parent/'native/capability-manifest-domains.v2.json').read_text())
check('capability-relation-domain-successor-extends-the-inherited-twelve',
      CAP_DOMAINS['registries']['RELATION-DOMAIN-V2']['inheritedMemberCount']==12 and
      CAP_DOMAINS['registries']['RELATION-DOMAIN-V2']['memberCount']==13 and
      CAP_DOMAINS['registries']['RELATION-DOMAIN-V2']['addedMembers']==['unresolved-edge'])
check('capability-successor-keeps-cve1-and-the-inherited-identity-domain',
      CAP_DOMAINS['recipe']['value']=='SHA256(UTF8("opensip.capability-manifest.v1") || 0x00 || committedBytes)' and
      'resolved-inputs.v2.json' in CAP_DOMAINS['recipe']['encoding'])
check('capability-successor-separates-cve1-from-the-relation-payload-codec',
      'nothing to do with the relation PAYLOAD codec' in CAP_DOMAINS['recipe']['codecSeparation'])
# The inherited twelve-relation golden still admits, byte-for-byte, and reproduces its published id.
INHERITED_ADMISSION=N.admit_capability_manifest(INHERITED_MANIFEST_BYTES)
check('inherited-twelve-relation-golden-still-admits-and-reproduces-its-published-identity',
      INHERITED_ADMISSION['result']=='ADMIT' and
      INHERITED_ADMISSION['capabilityManifestId']==CAPABILITY_RECIPE['vectors']['byId']['DCM-1-core']['capabilityManifestId'])
check('cve1-round-trips-the-inherited-golden-byte-for-byte',
      N.cve1_encode(N.cve1_decode(INHERITED_MANIFEST_BYTES))==INHERITED_MANIFEST_BYTES)
CURRENT_ADMISSION=N.admit_capability_manifest(CURRENT_CAPABILITY_MANIFEST_BYTES)
check('current-manifest-declaring-unresolved-edge-admits',
      CURRENT_ADMISSION['result']=='ADMIT' and 'unresolved-edge' in CURRENT_ADMISSION['relations'])
check('the-current-manifest-is-the-one-bound-into-the-plan-closure',
      objects[run['planId']][1]['capabilityManifestId']==CURRENT_ADMISSION['capabilityManifestId'] and
      blobs[objects[run['planId']][1]['capabilityManifestBytesDigest']]==CURRENT_CAPABILITY_MANIFEST_BYTES)
check('extending-the-manifest-moves-its-identity',
      CURRENT_ADMISSION['capabilityManifestId']!=INHERITED_ADMISSION['capabilityManifestId'])
def manifest_run(mutate):
    run,objects,blobs=build(resolved=True,has_match=True)
    value=N.cve1_decode(CURRENT_CAPABILITY_MANIFEST_BYTES);mutate(value)
    raw=N.cve1_encode(value)
    plan=copy.deepcopy(objects[run['planId']][1])
    plan['capabilityManifestBytesDigest']=put_blob(blobs,raw)
    plan['capabilityManifestId']=hashlib.sha256(b'opensip.capability-manifest.v1\0'+raw).hexdigest()
    rekey_plan(objects,blobs,run,plan)
    run['capabilityManifestId']=plan['capabilityManifestId']
    return M.close_run(run,objects,blobs)
check('manifest-run-harness-positive-control-closes',manifest_run(lambda v:None).startswith('run2:'))
rejects_because('manifest-with-an-unknown-relation-refuses-not-just-a-hash-check',
    lambda:manifest_run(lambda v:v['providers'][0]['relations'].update({'made-up':'observed'})),
    'capability.adm-domain:relation:made-up')
rejects_because('manifest-with-a-rung-from-another-relations-ladder-refuses',
    lambda:manifest_run(lambda v:v['providers'][0]['relations'].update({'declares':'checked'})),
    'capability.adm-domain:rung:declares@checked')
rejects_because('manifest-absent-capability-with-an-unknown-relation-refuses',
    lambda:manifest_run(lambda v:v['coverageForAbsent'][0]['relationIds'].append('made-up')),
    'capability.adm-domain:relation:made-up')
check('cve1-refuses-a-non-canonical-map-order',
      not_admitted(lambda:N.cve1_decode(b'\x06\x00\x00\x00\x02'+N.cve1_encode('b')+N.cve1_encode(1)+N.cve1_encode('a')+N.cve1_encode(2))))
check('cve1-refuses-trailing-bytes-and-unknown-tags',
      not_admitted(lambda:N.cve1_decode(N.cve1_encode(1)+b'\x00')) and not_admitted(lambda:N.cve1_decode(b'\x7f')))
check('cve1-refuses-non-nfc-text',not_admitted(lambda:N.cve1_encode('é')))
check('cve1-encodes-all-eight-closed-types',
      [N.cve1_encode(v).hex() for v in (None,False,True,0,-1,'a',[],{})]==
      ['00','01','02','030000000000000000','07ffffffffffffffff','040000000161','0500000000','0600000000'])

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

# --- new native diagnostics are INTERNAL causes, not public DomainDetail codes -----------------
# The native contract keeps context/universe helper diagnostics as internal request-detail causes.
# Every string this session added is an internal AdmissionError cause; none is emitted as a public
# code, and none is added to the shared public registry.
PUBLIC_REGISTRY={r['code'] for r in json.loads((H.parents[1]/'design-corrections/public-detail-registry.v1.json').read_text())['records']}
NEW_INTERNAL_CAUSES_V3={'PAYLOAD_RELATION_UNREGISTERED','PAYLOAD_IMPORT_UNREGISTERED',
    'PAYLOAD_IMPORT_REGISTRY_DRIFT','PAYLOAD_COVERAGE_UNREGISTERED','PAYLOAD_PARAMETER_UNREGISTERED',
    'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT','PAYLOAD_RECORD','PAYLOAD_KEY_MISSING',
    'PAYLOAD_DOMAIN_REF_NOT_A_ROOT','RELATION_RUNG_NOT_IN_LADDER','RELATION_RUNG_REQUIRED_FIELD',
    'RELATION_RUNG_FORBIDDEN_FIELD','RELATION_UNIVERSE_RULE','RELATION_PAYLOAD_NEGATIVE_INTEGER',
    'RELATION_PAYLOAD_NOT_NFC','UNREGISTERED_DOCUMENT','REGISTERED_RECORD'}
NEW_INTERNAL_CAUSES=[
    'NATIVE_CONTEXT_ADMISSION','NATIVE_UNIVERSE_BINDING','NATIVE_UNIVERSE_BINDING_UNAVAILABLE',
    'NATIVE_UNIVERSE_CONTEXT_LANGUAGE','NATIVE_UNIVERSE_CONTEXT_FIELD_MISMATCH',
    'NATIVE_CONTEXT_PATH_NOT_INVENTORIED','NATIVE_UNIVERSE_PATH_NOT_INVENTORIED',
    'NATIVE_CONTEXT_SOURCE_MISMATCH','NATIVE_UNIVERSE_SOURCE_MISMATCH',
    'NATIVE_NESTED_NESTED_IDENTITY_REQUIRED','NATIVE_NESTED_MEMBER_LENGTH',
    'PREPARED_RESOLUTION_GRANT_JOIN','PREPARED_RESOLUTION_MODE_NOT_REQUESTED',
    'UNIVERSE_LANGUAGE_NOT_REQUESTED','ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED',
    'CACHE_STAGE_NOT_IN_THE_EXECUTION_PLAN','CACHE_INPUT_PAYLOAD_REF_NOT_A_ROOT',
    'CACHE_INPUT_DOMAIN_UNREGISTERED','CACHE_SCOPE_SOURCE_JOIN','CACHE_UNSELECTED_PRODUCER',
    'native.universe-retained-inputs-not-supplied','native.universe-retained-input-missing',
    'native.universe-retained-input-identity-mismatch','native.universe-retained-input-mismatch',
    'native.universe-retained-input-unselected','native.universe-source-mismatch',
    'native.universe-path-not-inventoried','native.universe-context-field-mismatch']
check('new-native-and-cache-causes-are-not-public-domain-detail-codes',
      not (set(NEW_INTERNAL_CAUSES)&PUBLIC_REGISTRY))
check('no-new-public-detail-code-was-added-by-this-session',
      NEW_INTERNAL_CAUSES_V3.isdisjoint(PUBLIC_REGISTRY))
# G9 is root's: the purge refusal now has a registered foundation-owned public code, and identity
# section 5 points at the workflow projection rather than restating it.
check('pinned-purge-refusal-has-a-registered-foundation-owned-public-code',
      'evidence.pinned' in PUBLIC_REGISTRY and
      next(r for r in json.loads((H.parents[1]/'design-corrections/public-detail-registry.v1.json').read_text())['records']
           if r['code']=='evidence.pinned')['owner']=='foundation')
check('identity-store-purge-api-is-unchanged',
      M.EvidenceStore.purge.__code__.co_varnames[:3]==('self','rid','force'))
# The only public terminations this unit emits remain the two already-registered ones.
check('identity-public-terminations-remain-the-registered-two',
      {M.EvidenceUnavailable('x').termination['domainDetail']['code'],
       M.RegenerationMismatch('run2:'+'a'*64).termination['domainDetail']['code']}
      =={'evidence.missing','evidence.regeneration-mismatch'} and
      {'evidence.missing','evidence.regeneration-mismatch'}<=PUBLIC_REGISTRY)

# --- G3/G5/G10 through a COMPLETE Run: the ordinary node_modules-resolving TypeScript project ---
run,objects,blobs=build(resolved=True,has_match=True)
ts_context=M.parse_h_frame(blobs[next(d for d in objects[run['planId']][1]['nativeContextDigests']
    if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')],'native-context')[1]
ts_universe=M.parse_h_frame(blobs[next(v for k,(d,v) in objects.items() if d=='subject-scope')['sourceUniverse']],
                            'native-semantic-universe')[1]
check('mainstream-node-modules-resolving-typescript-universe-closes-a-run',
      ts_universe['nodeModulesInReadSet'] is True and ts_context['nodeModulesLayoutDigest'] is not None and
      M.close_run(run,objects,blobs).startswith('run2:'))
layout=C.parse(blobs[ts_context['nodeModulesLayoutDigest']])
check('node-modules-layout-is-the-retained-record-its-digest-names',
      N.resolved_node_modules_layout_digest(layout)==ts_context['nodeModulesLayoutDigest'] and
      {r['packageName'] for r in layout['entries']}=={'left-pad','@scope/util'})
check('node-modules-layout-members-are-retained-but-not-snapshot-rows',
      all(r['contentSha256'] in blobs for r in layout['entries']) and
      not any(r['path'].startswith('node_modules/') for r in objects[run['snapshotId']][1]['sourceInventory']))
graph=C.parse(blobs[ts_universe['tsconfigGraphHash']])
check('tsconfig-graph-is-the-retained-record-its-key-names',
      N.typescript_config_graph_digest(graph)==ts_universe['tsconfigGraphHash'])
check('tsconfig-graph-retains-ordered-multiple-extends',
      next(n for n in graph['nodes'] if n['path']=='tsconfig.json')['extendsResolved']
      ==['tsconfig.base.json','tsconfig.strict.json'])
check('config-origin-is-derived-from-the-selected-entry',
      ts_universe['configOrigin']==N.typescript_config_origin(graph)=='tsconfig' and graph['entryConfigPath']=='tsconfig.json')
def ts_universe_run(mutate_universe=None,mutate_context=None,mutate_retained=None):
    run,objects,blobs=build(resolved=True,has_match=True)
    plan=copy.deepcopy(objects[run['planId']][1])
    old_context=next(d for d in plan['nativeContextDigests']
                     if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')
    context=M.parse_h_frame(blobs[old_context],'native-context')[1]
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    graph=C.parse(blobs[universe['tsconfigGraphHash']])
    if mutate_retained is not None:
        mutate_retained(graph);universe['tsconfigGraphHash']=put_blob(blobs,graph)
    if mutate_context is not None:
        mutate_context(context)
        new_context=M.retain_h_identity('native.context.typescript.v2',context,blobs)
        plan['nativeContextDigests']=sorted([d for d in plan['nativeContextDigests'] if d!=old_context]+[new_context])
        universe['nativeContextId']='sha256:'+new_context
    if mutate_universe is not None:mutate_universe(universe)
    new_universe=M.retain_h_identity('native.semantic-universe.typescript.v2',universe,blobs)
    for key in [k for k,(d,v) in objects.items() if d in ('fact','subject-scope')]:
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new_universe,targetUniverse=new_universe),run)
    rekey_plan(objects,blobs,run,plan);resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
check('typescript-universe-harness-positive-control-closes',ts_universe_run().startswith('run2:'))
rejects_because('rehashed-tsconfig-graph-with-a-wrong-source-digest-refuses',
    lambda:ts_universe_run(mutate_retained=lambda g:g['nodes'][0].update(contentSha256='e'*64)),
    'native.universe-source-mismatch:')
rejects_because('rehashed-tsconfig-graph-dropping-an-extends-edge-refuses',
    lambda:ts_universe_run(mutate_retained=lambda g:next(n for n in g['nodes'] if n['path']=='tsconfig.json').update(extendsResolved=['tsconfig.base.json'])),
    'native.config-graph-node-unreachable-from-entry:tsconfig.strict.json')
# Later-wins precedence is semantic, so reordering the edges is a DIFFERENT configuration: it closes,
# and it closes as a different universe and a different Run.
check('reordered-extends-edges-are-a-different-universe-and-a-different-run',
      ts_universe_run(mutate_retained=lambda g:next(n for n in g['nodes'] if n['path']=='tsconfig.json')
          .update(extendsResolved=['tsconfig.strict.json','tsconfig.base.json']))!=ts_universe_run())
rejects_because('config-origin-cannot-be-asserted-against-the-retained-entry',
    lambda:ts_universe_run(mutate_universe=lambda u:u.update(configOrigin='jsconfig')),
    'native.universe-context-field-mismatch:configOrigin')
rejects_because('node-modules-in-read-set-cannot-contradict-the-retained-layout',
    lambda:ts_universe_run(mutate_universe=lambda u:u.update(nodeModulesInReadSet=False)),
    'native.universe-context-field-mismatch:nodeModulesInReadSet')
rejects_because('a-context-naming-an-unretained-node-modules-layout-is-retention-loss',
    lambda:ts_universe_run(mutate_context=lambda c:c.update(nodeModulesLayoutDigest='f'*64)),
    'EVIDENCE_UNAVAILABLE')
def layout_not_a_record():
    run,objects,blobs=build(resolved=True,has_match=True)
    plan=copy.deepcopy(objects[run['planId']][1])
    old_context=next(d for d in plan['nativeContextDigests']
                     if M.parse_h_frame(blobs[d],'native-context')[0]=='native.context.typescript.v2')
    context=M.parse_h_frame(blobs[old_context],'native-context')[1]
    context['nodeModulesLayoutDigest']=put_blob(blobs,{'schemaVersion':1,'entries':[{'nope':1}]})
    new_context=M.retain_h_identity('native.context.typescript.v2',context,blobs)
    plan['nativeContextDigests']=sorted([d for d in plan['nativeContextDigests'] if d!=old_context]+[new_context])
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    universe=M.parse_h_frame(blobs[objects[scope_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    universe['nativeContextId']='sha256:'+new_context
    new_universe=M.retain_h_identity('native.semantic-universe.typescript.v2',universe,blobs)
    for key in [k for k,(d,v) in objects.items() if d in ('fact','subject-scope')]:
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new_universe,targetUniverse=new_universe),run)
    rekey_plan(objects,blobs,run,plan);resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run)
    return run,objects,blobs
rejects_because('a-node-modules-layout-that-is-not-a-registered-record-refuses',
    lambda:M.close_run(*layout_not_a_record()),'REGISTERED_RECORD:#/$defs/ResolvedNodeModulesLayoutV1')
check('native-digest-law-reaches-the-native-bundle',
      N.native_digest_annotation_coverage()['unannotated']==[] and
      N.native_digest_annotation_coverage()['annotated']>=68)

# --- G7: the ExecutionId successor grammar is end-anchored ------------------------------------
EXECUTION_ID=M.SCHEMA['$defs']['commit-receipt']['properties']['executionId']['pattern']
check('execution-id-successor-grammar-is-end-anchored',EXECUTION_ID.endswith('(?![\\s\\S])'))
for suffix in ('\n','\r\n',' ','\t'):
    rejects('execution-id-refuses-a-trailing-'+repr(suffix),
        lambda x=suffix:M.EvidenceStore().prepare(*build(),'exec1_'+'a'*32+x,replay))
check('execution-id-accepts-only-the-exact-grammar',
      M.EvidenceStore().prepare(*build(),'exec1_'+'a'*32,replay).startswith('run2:'))
check('c2-selector-is-named-as-provenance-not-as-the-admitting-grammar',
      'provenance' in (H.parents[2]/'v2/contracts/product-v1/identity-and-evidence.md').read_text().split('c2-plan-stage-schema.v4.json')[1][:400])
# --- G11: the enumerator closure kind is stated, and no new kind was invented -----------------
KINDS=M.DIGESTS['closureKinds']
check('enumerator-closure-kind-is-stated',KINDS['byField']['subject-scope.enumeratorClosure']=='provider')
check('no-enumerator-kind-was-invented','enumerator' not in M.SCHEMA['$defs']['closure']['properties']['kind']['enum'])
check('every-closure-bearing-field-declares-its-kind',
      set(KINDS['byField'])>= {'subject-scope.enumeratorClosure','view.producerClosure','fact.producerClosure',
                               'finding.ruleClosure','evaluation-seal.evaluatorClosure','stage-spec.producerClosure'})
def wrong_enumerator_kind():
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    evaluator=next(k for k,(d,v) in objects.items() if d=='closure' and v['kind']=='evaluator')
    rekey(objects,key,dict(objects[key][1],enumeratorClosure=evaluator),run)
    resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run);return M.close_run(run,objects,blobs)
rejects_because('enumerator-closure-of-the-wrong-kind-refused',wrong_enumerator_kind,'ENUMERATOR_CLOSURE_KIND')
def unselected_enumerator():
    run,objects,blobs=build(resolved=True,has_match=True)
    key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    record={'schemaVersion':2,'kind':'provider','manifestDigest':put_blob(blobs,b'unselected-provider-manifest'),
            'tree':[],'semanticVersion':'9.9.9','protocolMajor':3,'platform':'macos-aarch64'}
    other=M.identifier('closure',record);objects[other]=('closure',record)
    rekey(objects,key,dict(objects[key][1],enumeratorClosure=other),run)
    resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run);return M.close_run(run,objects,blobs)
rejects_because('enumerator-closure-must-be-plan-selected',unselected_enumerator,'UNSELECTED_ENUMERATOR')
# --- G12 acknowledged: the governance exclusion the consumer confirmed is correct --------------
check('governance-records-remain-outside-the-semantic-recipe-set',
      not any(name in json.dumps(M.PAYLOADS)+json.dumps(M.DIGESTS)
              for name in ('correction-crosswalk','readiness-register','COORDINATOR-DECISIONS')))
# --- G8 counterevidence, asserted rather than asserted-away -----------------------------------
BUDGET=M.SCHEMA['$defs']['plan']['properties']['budget']
check('plan-budget-was-already-closed-g8-premise-is-false',
      BUDGET.get('additionalProperties') is False and BUDGET.get('required')==['unit','limit'] and
      BUDGET['properties']['unit']=={'const':'work-units'} and
      BUDGET['properties']['limit']['type']=='integer')
rejects('plan-budget-refuses-an-extra-key',
        lambda:M.identifier('plan',dict(objects[run['planId']][1],budget={'unit':'work-units','limit':1,'x':1})))

report={'standing':'design-reference-only','productQualification':False,'limits':[
    'finite single-atom rule interpreter over the REAL closed PolicyDocumentV1/RuleProgramV1 DSL; not full declarative-language qualification',
    'relation and Coverage payload schema REGISTRATION remains the native/workflow adapter boundary; identity checks retention, canonicality and validation under the retained document',
    'in-memory custody transition model; OS crash durability remains implementation gate',
    'replay callback is authenticated host/evaluator TCB assumption, not adversarial Python isolation',
    'both registered native-context domains AND both registered native semantic-universe domains close through complete Runs over small retained closure trees; every compiler, cargo, lockfile, dependency and prepared-output observation is an explicit synthetic trusted input. No compiler, cargo, OS or repository code is executed, no real toolchain is measured and no platform is qualified: this is design/reference evidence, not native or platform qualification',
    'the Rust dependency source set is one vendored registry package over a two-package Cargo.lock; real crate graphs, workspace member enumeration, feature unification by an actual cargo metadata run and missing-crate Coverage remain the native unit\'s own cases and later qualification',
    'admit_cache_entry is a POST-CONSTRUCTION conformance check over an admitted Run, not the pre-analysis cache scheduling API, and it does not fetch or validate cached OUTPUT bytes or decide reuse policy; it validates a lookup key and its consumed input closure',
    'owner-source-set ownerKey order uses the generic {by:[field]} x-opensip-order form in canonical.py; the closure checker enforces the same order independently'],
    'checks':results,'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results)}
a=argparse.ArgumentParser();a.add_argument('--report');args=a.parse_args()
if args.report:Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','failed','productQualification']}))
if report['failed']:print(json.dumps([x['id'] for x in results if not x['passed']],indent=1))
sys.exit(bool(report['failed']))
