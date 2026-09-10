"""Synthetic shared graph construction, extracted from the corrected coauthor reference fixture.
Source: foundation/check-identity.py SHA256 2973c5c4a7d7e09215bb09e247f049515cad1d4081bf413af07ae00613c4ca90.
No expected verdict or independent-review claim is derived from this builder.
"""
import copy,hashlib,json,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent/'foundation'
spec=importlib.util.spec_from_file_location('integration_fixture_identity',H/'identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C
W=M.workflow_admission()
spec=importlib.util.spec_from_file_location('integration_fixture_native',H.parent/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
NATIVE_FIXTURES=json.loads((H.parent/'native/native-cases.v2.json').read_text())['fixtures']

ATOM={'op':'none','relation':'references','minResolution':'resolved-binding','filters':[{'field':'target','cmp':'eq','value':'foo'}]}

def rule_for(language,atom=None,subject_kind='symbol'):
    """One rule, in the workflow contract's own DSL, enumerating subjects of the analysed
    language's universe. The requested capability, the analysed source and the rule's subject
    universe are one coherent request; they are not a Rust universe under a TypeScript question.

    `atom` and `subject_kind` are the rule's own closed-DSL vocabulary, so a rule about files is
    written in the SAME language as a rule about symbols. There is still no second policy DSL."""
    atom=ATOM if atom is None else atom
    return {'ruleId':'no-consumer','ruleProgramRef':{'contributionId':'fixture','ruleStableId':'no-consumer','semanticsMajor':2,
              'programDigest':hashlib.sha256(C.canonical(atom)).hexdigest()},
            'enabled':True,'severity':'error','gate':True,
            'subjectEnumeration':{'universe':language,'subjectKind':subject_kind},
            'emitWhen':atom,'evidenceUse':[],'messageCode':'no-consumer'}

def policy_for(language,atom=None,subject_kind='symbol'):
    return {'schemaFamily':'opensip.product.policy','schemaMajor':1,'gateSeverityAtLeast':'error',
            'rules':[rule_for(language,atom,subject_kind)]}

RULE=rule_for('typescript')

POLICY=policy_for('typescript')

WAIVERS={'schemaFamily':'opensip.product.waivers','schemaMajor':1,'waivers':[]}

def compiled_program(policy):
    return {'schemaVersion':1,'policyDigest':hashlib.sha256(C.canonical(policy)).hexdigest(),
            'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in policy['rules']]}

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

TS_SOURCES={'tsconfig.base.json':b'{"compilerOptions":{"target":"es2022"}}\n',
            'tsconfig.strict.json':b'{"compilerOptions":{"strict":true}}\n',
            'tsconfig.json':b'{"extends":["./tsconfig.base.json","./tsconfig.strict.json"]}\n',
            'package-lock.json':b'{"lockfileVersion":3}\n',
            # The workspace package manifest: an ordinary inventoried repository source, and the
            # subject a `package` relation fact declares.
            'package.json':b'{"name":"fixture-workspace","version":"1.0.0"}\n',
            # A JavaScript source the SAME TypeScript engine reads. Native 6.3 makes its normalized
            # body a `javascript` fact, not a `typescript` one, even with identical bytes.
            'legacy.js':b'export const foo = 1;\n'}

TS_NODE_MODULES={'node_modules/left-pad/package.json':b'{"name":"left-pad","version":"1.3.0"}\n',
                 'node_modules/@scope/util/package.json':b'{"name":"@scope/util","version":"2.0.1"}\n'}

RUST_TARGET='aarch64-apple-darwin'

RUST_DEP_KEY='fixture-dep 1.0.0 registry+https://github.com/rust-lang/crates.io-index'

RUST_DEP_FILE=b'pub fn dep() {}\n'

RUST_PROJECTED_CONFIG=b'[build]\nrustflags = ["--cfg", "fixture"]\n'

RUST_SOURCES={'Cargo.lock':('version = 3\n\n[[package]]\nname = "fixture-dep"\nversion = "1.0.0"\n'
                            'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
                            'checksum = "'+'a'*64+'"\n\n[[package]]\nname = "fixture-root"\nversion = "0.1.0"\n').encode(),
              '.cargo/config.toml':b'[build]\nrustflags = ["--cfg", "fixture"]\n',
              # The inventoried manifests that DECLARE the compilation targets. A unit names its
              # marker, the same markerPath vocabulary WorkspaceUnitV2 already uses.
              'Cargo.toml':b'[package]\nname = "fixture-root"\nedition = "2021"\n',
              'vendor/fixture-dep/Cargo.toml':b'[package]\nname = "legacy-crate"\nedition = "2015"\n',
              # A '#' in a repository directory is admissible under the canonical repository-path
              # contract. The withdrawn delimiter recipe could stay injective only by forbidding it.
              'crates/c#interop/Cargo.toml':b'[package]\nname = "interop"\nedition = "2021"\n',
              'crates/c#interop/src/lib.rs':b'pub fn interop() {}\n',
              'src/lib.rs':b'pub fn root() {}\n',
              'vendor/fixture-dep/src/lib.rs':RUST_DEP_FILE}

RUST_PREPARED_DIRECTIVES=b'cargo:rustc-cfg=fixture_prepared\n'

REFERENCES_PAYLOAD={'referrer':'symbol:foo','name':'foo','resolvedBinding':'symbol:foo'}

FILTER_FIELD_OF={
 'references':{'subject':'referrer','target':'name','resolution':'name',
               'universe':'name','subjectKind':'name','targetKind':'name','observability':'name'},
 'file':{'subject':'path','target':'path'},
 'clones':{'subject':'bodyIdentity','target':'bodyIdentity'},
 'package':{'subject':'packageName','target':'packageName'},
 'vcs-change':{'subject':'path','target':'path'},
 'declares':{'subject':'declared','target':'declared'}}

def coverage_result(scope_descriptor,universe,resolved,ownership=None,edition_map=None):
    """A real CoverageResultV3 over the host's own scope, with the resolution claim DERIVED FROM THE
    RUNG by the native producer's own helper rather than asserted by the fixture.

    RC-2: `complete` needs attempted, exhaustive examination, a complete stage terminal and zero
    admitted unresolved edges. RC-1: a rung outside RESOLVED_RUNGS - `file@enumerated` is the
    canonical case - must carry `not-applicable` with no counts, because there is no resolution for
    it to be complete about. The separate examined-partition claim `entry.coverage` may still be
    `complete`: the host did examine every subject it committed to. The v8 reviewer's file Run was
    blocked by a fixture that always emitted a resolution claim; RC-1 was right and is untouched."""
    commitment=N.subject_scope_commitment(scope_descriptor)
    completeness=N.completeness_from_stage(scope_descriptor['relation'],scope_descriptor['resolution'],
        scope_descriptor['subjects'],[],'complete' if resolved else None,resolved,resolved)
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
               **_clone_disclosure(scope_descriptor,resolved,ownership,edition_map)}}

def retained_clone_ownership(universe_digest,blobs):
    """Recover (ownership record, edition map) from the RETAINED frames, the same way the Run
    closure reaches them: the universe h-frame, then the nested source-unit-ownership h-frame the
    universe names. Returns (None, {}) for a universe with no ownership axis at all, which is every
    non-Rust universe. Nothing is invented and nothing is read from the Coverage claim."""
    try:domain,universe,row=M.parse_h_frame(blobs[universe_digest],'native-semantic-universe')
    except Exception:return None,{}
    if 'sourceUnitOwnershipId' not in universe:return None,{}
    edition_map=universe.get('edition') or {}
    reference=universe['sourceUnitOwnershipId']
    if reference is None:return None,edition_map
    frame=blobs.get(reference.removeprefix('sha256:'))
    if frame is None:return None,edition_map
    return M.parse_h_frame(frame,'native-nested')[1],edition_map

def _clone_disclosure(scope_descriptor,resolved,ownership,edition_map):
    """The (deficiency, nativeCause) pair this Coverage entry owes, DERIVED by the owning producer
    unit rather than asserted here. For a clones scope whose universe cannot yield a body dialect the
    pair is the typed ownership disclosure; otherwise it is the ordinary resolution claim. The Run
    closure re-derives the same pair independently and refuses a mismatch, so this helper cannot
    define the law by emitting whatever it likes."""
    if scope_descriptor['relation']=='clones':
        owed=N.clone_ownership_disclosure(ownership,scope_descriptor['subjects'],edition_map or {})
        if owed is not None:
            return {'deficiency':owed['deficiency'],'nativeCause':owed['nativeCause']}
    return {'deficiency':None if resolved else 'resolution-incomplete','nativeCause':None}

def rust_inputs(objects,blobs,add,blob,tree,dep_body=RUST_DEP_FILE,prepared=None,workspace=None):
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
    # EVERY Rust universe that could carry a clones fact commits the ownership relation, and that
    # record carries the EXPLICIT SELECTION of the compilation targets this universe analyses. There
    # is no single-edition fast path: Cargo documents a per-TARGET edition that defaults to the
    # package edition, so package defaults that all agree still do not determine a body's dialect.
    edition={'fixture-root':2021} if workspace is None else dict(workspace['edition'])
    units=(workspace['units'] if workspace is not None else
           [unit('Cargo.toml','lib','fixture-root','fixture-root')])
    rows=(workspace['ownership'] if workspace is not None else
          [{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')}])
    selected=(workspace['selectedUnitIds'] if workspace is not None else [UID('Cargo.toml','lib','fixture-root')])
    ownership={'schemaVersion':1,'enumeration':(workspace or {}).get('enumeration','complete'),
               'units':sorted(units,key=lambda u:u['unitId'].encode()),
               'selectedUnitIds':sorted(selected,key=lambda x:x.encode()),
               'ownership':sorted(rows,key=lambda r:(r['path'].encode(),r['unitId'].encode()))}
    ownership_id='sha256:'+M.retain_h_identity(N.SOURCE_UNIT_OWNERSHIP_DOMAIN,ownership,blobs)
    universe={'schemaVersion':2,'edition':edition,'sourceUnitOwnershipId':ownership_id,
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
            'features':features,'projection':projection,'manifestRows':manifest_rows,'ownership':ownership}

def native_inputs(objects,blobs,add,blob,stdlib_body=b'declare const es2022: unknown;\n',prepared=None,ts_inventory=(),ts_source_path='a.ts',workspace=None):
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
    rust=rust_inputs(objects,blobs,add,blob,tree,prepared=prepared,workspace=workspace)
    # The THIRD registered native-context domain: syntax-only. It exists because the capability
    # matrix advertises declares/literal/control-flow@syntactic and clones@normalized-body-hash for
    # that mode, and because file/package/vcs-change facts must be representable in a repository
    # with no TypeScript and no Rust unit - and fact2/subject-scope both REQUIRE a universe from the
    # closed domain set. It carries a grammar bundle and nothing else: no compiler, no stdlib, no
    # lockfile, no resolution inputs, because a grammar-only analysis reads none of them.
    syntax=syntax_inputs(objects,blobs,add,blob,tree)
    return {'contextDigest':context_digest,'universeDigest':universe_digest,'context':context,'universe':universe,
            'stdlib':stdlib,'toolchain':toolchain,'admission':admission,
            'rustContextDigest':rust['contextDigest'],'rustContext':rust['context'],
            'rustUniverseDigest':rust['universeDigest'],'rustUniverse':rust['universe'],
            'llvm':rust['llvm'],'rustTools':rust['toolClosure'],'rust':rust,
            'syntaxContextDigest':syntax['contextDigest'],'syntaxContext':syntax['context'],
            'syntaxUniverseDigest':syntax['universeDigest'],'syntaxUniverse':syntax['universe'],
            'syntaxGrammarClosure':syntax['closure'],'syntax':syntax}

GRAMMAR_FILES={'grammar/tsjs.grammar':b'// fixture tsjs grammar\n',
               'grammar/rust.grammar':b'// fixture rust grammar\n',
               'grammar/bundle.manifest':b'{"fixture":"grammar-bundle"}\n',
               'grammar/normalize.l0.spec':b'{"level":"L0-verbatim"}\n'}

def syntax_inputs(objects,blobs,add,blob,tree):
    """One admitted syntax-only native context and its universe, through the ACTUAL native
    admission and binding functions, over a retained kind=grammar closure tree.

    The grammar bundle is pinned exactly the way a toolchain is - admitted closure, version FROM the
    closure manifest, every grammar definition present in the retained tree - so the component that
    interprets a body span is closure-bound rather than a static constant or a fabricated compiler."""
    closure=add('closure',kind='grammar',manifestDigest=blob(b'fixture-grammar-manifest'),
                tree=tree(GRAMMAR_FILES),semanticVersion='1.4.0',protocolMajor=2,platform='any')
    members={r['path']:r['sha256'] for r in objects[closure][1]['tree']}
    context={'schemaVersion':2,'grammarBundle':{
        'schemaVersion':1,'closureId':closure,'parserName':'opensip-grammar-parser',
        'parserVersion':'1.4.0','bundleDigest':members['grammar/bundle.manifest'],
        'grammars':[
            {'grammarId':'rust.v1','grammarVersion':'1.0.0','languageId':'rust',
             'suffixes':['.rs'],'grammarDigest':members['grammar/rust.grammar']},
            {'grammarId':'tsjs.v1','grammarVersion':'1.0.0','languageId':'typescript',
             'suffixes':sorted(['.cjs','.cts','.js','.jsx','.mjs','.mts','.ts','.tsx'],key=lambda s:s.encode()),
             'grammarDigest':members['grammar/tsjs.grammar']}],
        'normalizer':{'normalizerId':'opensip-normalizer','normalizerVersion':'1.0.0',
                      'specificationDigest':members['grammar/normalize.l0.spec']}}}
    admission=N.admit_native_context('syntax',context,{closure:objects[closure][1]})
    if admission['refusals']:raise C.AdmissionError('FIXTURE_SYNTAX_CONTEXT:'+','.join(admission['refusals']))
    universe={'schemaVersion':2,'nativeContextId':admission['nativeContextId'],
              'selectedGrammarIds':['rust.v1','tsjs.v1'],'resolutionAttempted':False}
    binding=N.bind_syntax_universe(universe,admission,context,{},[])
    if binding['result']!='ADMIT':raise C.AdmissionError('FIXTURE_SYNTAX_UNIVERSE:'+','.join(binding['refusals']))
    context_digest=M.native_context_frame('native.context.syntax.v2',context,blobs)
    universe_digest=M.native_universe_frame('native.semantic-universe.syntax.v2',universe,blobs)
    if context_digest!=admission['planNativeContextDigest'] or universe_digest!=binding['sourceUniverse']:
        raise C.AdmissionError('FIXTURE_SYNTAX_IDENTITY')
    return {'contextDigest':context_digest,'universeDigest':universe_digest,'context':context,
            'universe':universe,'admission':admission,'closure':closure,'members':members}

LANGUAGE_FIXTURE={
 'typescript':{'languageMode':'ts-tsconfig','sourcePath':'a.ts','sourceBytes':b'export const foo = 1;\n'},
 'rust':{'languageMode':'rust-cargo','sourcePath':'src/lib.rs','sourceBytes':RUST_SOURCES['src/lib.rs']},
 # The syntax-only mode. Its source path is deliberately a .rs file: under the syntax universe that
 # body is read by the bundled grammar with NO Cargo, no edition and no ownership record, which is
 # exactly the case the compiler universes cannot represent.
 'syntax':{'languageMode':'syntax-only','sourcePath':'src/lib.rs','sourceBytes':RUST_SOURCES['src/lib.rs']}}

LEVEL_SPECIFICATION=(b'opensip.fact-identity.level-specification/L0-verbatim\n'
                     b'tokenisation: forbidden\npayload: the exact snapshot body-span bytes\n')

def framed_body_preimage(level,level_version,language_id,language_version,payload):
    """The inherited domainSeparatedPreimage of fact-identity-policy.v2, built exactly as written:
    five u8-length-prefixed components then `u32be len || payload`. `level_version` is the RAW 32
    digest bytes, never the hex text. At L0 the payload is itself `u32be raw_byte_len || span`, so
    the outer frame length and the L0 payload length are both present and both meant."""
    def prefixed(raw):
        if len(raw)>255:raise C.AdmissionError('FIXTURE_BODY_FRAME_COMPONENT')
        return bytes([len(raw)])+raw
    return (prefixed(b'opensip.fact-identity.v1')+prefixed(level.encode('utf8'))+prefixed(level_version)
            +prefixed(language_id.encode('ascii'))+prefixed(language_version)
            +len(payload).to_bytes(4,'big')+payload)

def body_language_version(universe_record,context_record,domain_row,anchor,retained=None):
    """Independent construction of the body language version, from the registry binding.

    Written here rather than called from the model: the checker builds the record from the SCHEMA's
    declared source paths, so if the model and the registry ever disagree the frame stops matching.
    The compiler identity comes through the universe's own admitted context reference; the dialect
    is the unique value of the per-crate edition map, and there is deliberately no fallback.
    """
    binding=domain_row['languageVersionBinding']
    record={'schemaVersion':1}
    for name,source in binding['fields'].items():
        if 'const' in source:record[name]=source['const'];continue
        node=context_record if source['source']=='native-context' else universe_record
        for step in source['path']:node=node[step]
        record[name]=node
    dialect=binding['dialect']
    if dialect['form']=='closed-suffix-table':
        matches=[x for x in dialect['table'] if anchor['path'].endswith(x)]
        if not matches:raise C.AdmissionError('FIXTURE_SOURCE_VARIANT_UNKNOWN:'+anchor['path'])
        variant=dialect['table'][max(matches,key=len)]
        record['dialect']={dialect['key']:variant}
        record['languageId']=binding['bodyLanguageByVariant'][variant]
    else:
        record['languageId']=binding['bodyLanguage']
        node=universe_record
        for step in dialect['path']:node=node[step]
        if not node:raise C.AdmissionError('FIXTURE_DIALECT_ABSENT')
        spec=dialect['ownership'];owned=(retained or {}).get(spec['retainedAs'])
        if owned is None:raise C.AdmissionError('FIXTURE_OWNERSHIP_REQUIRED')
        if owned[spec['enumerationField']]!='complete':raise C.AdmissionError('FIXTURE_OWNER_UNENUMERATED')
        units={u[spec['unitField']]:u for u in owned[spec['unitsField']]}
        rows=[r for r in owned['ownership'] if r[spec['pathField']]==anchor['path']]
        if not rows:raise C.AdmissionError('FIXTURE_OWNER_UNKNOWN:'+anchor['path'])
        chosen=[r for r in rows if r[spec['unitField']] in set(owned[spec['selectionField']])]
        if not chosen:raise C.AdmissionError('FIXTURE_OWNER_NOT_SELECTED:'+anchor['path'])
        effective=set()
        for row in chosen:
            unit=units[row[spec['unitField']]]
            effective.add(unit[spec['targetEditionField']] if unit[spec['targetEditionField']] is not None
                          else node[unit[spec['crateField']]])
        if len(effective)!=1:raise C.AdmissionError('FIXTURE_OWNER_AMBIGUOUS:'+anchor['path'])
        record['dialect']={dialect['key']:next(iter(effective))}
    return record

def unit(marker,kind,name,crate,edition=None):
    """A compilation target row whose unitId is the PUBLISHED H projection of its own metadata."""
    row={'markerPath':marker,'targetKind':kind,'targetName':name,'crateName':crate,'targetEdition':edition}
    return dict(row,unitId=N.source_unit_id(row))

UID=lambda marker,kind,name:N.source_unit_id({'markerPath':marker,'targetKind':kind,'targetName':name})

def relation_fixture(relation,source_path,source_body,source,universe_record,universe_domain,blob,context_record=None,ownership=None):
    """One real registered payload per relation, with the scope rung, the subjects, the anchors and
    the rule atom that relation actually owes. `file` and `clones` are the two relations whose
    payloads make a claim about the snapshot itself, which is exactly why they need a complete Run
    and not only a schema annotation."""
    row=M.DIGESTS['domainSets']['native-semantic-universe'][universe_domain]
    if relation=='references':
        return {'resolution':'resolved-binding','subjects':['foo'],'subjectKind':'symbol',
                'payload':REFERENCES_PAYLOAD,'minResolution':'resolved-binding','filter':('target','foo'),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)-1}]}
    if relation=='file':
        return {'resolution':'enumerated','subjects':[source_path],'subjectKind':'file',
                'payload':{'path':source_path,'contentSha256':source,'byteLength':len(source_body)},
                'minResolution':'enumerated','filter':('subject',source_path),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
    if relation=='clones':
        specification=blob(LEVEL_SPECIFICATION)
        # A clones SCOPE is admissible even where no body identity is: an unenumerated or unselected
        # universe simply yields no fact. The scope, its Coverage and the indeterminate verdict are
        # the existing law's job, and a producer that cannot mint a body identity must not pretend to.
        try:probe_dialect=body_language_version(universe_record,context_record,row,
            {'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)},ownership)
        except C.AdmissionError:
            return {'resolution':'normalized-body-hash','subjects':[source_path],'subjectKind':'file',
                    'payload':None,'minResolution':'normalized-body-hash','filter':('subject','no-admissible-body'),
                    'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
        # RAW 32 digest bytes of the canonical projection: fixed width, so the inherited u8 component
        # length holds for any valid universe, including a large single-edition workspace.
        anchor={'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}
        projection=body_language_version(universe_record,context_record,row,anchor,ownership)
        language_version=hashlib.sha256(C.canonical(projection)).digest()
        start,end=0,len(source_body)
        span=source_body[start:end]
        # The frame's languageId is the BODY's language from the same selector - a .js body read by
        # the TypeScript engine is a javascript body - not the provider universe's engine language.
        frame=framed_body_preimage('L0-verbatim',bytes.fromhex(specification),projection['languageId'],
                                   language_version,len(span).to_bytes(4,'big')+span)
        identity='sha256:'+blob(frame)
        return {'resolution':'normalized-body-hash','subjects':[source_path],'subjectKind':'file',
                'payload':{'bodyIdentity':identity,'normalisationLevel':'L0-verbatim','normalisationVersion':specification},
                'minResolution':'normalized-body-hash','filter':('subject',identity),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':start,'endByte':end}]}
    if relation=='package':
        return {'resolution':'manifest-declared','subjects':['fixture-workspace'],'subjectKind':'package',
                'payload':{'manifestPath':'package.json','packageName':'fixture-workspace','packageVersion':'1.0.0'},
                'minResolution':'manifest-declared','filter':('subject','fixture-workspace'),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
    if relation=='vcs-change':
        # A CURRENT source claim: the changed path is in the analysed snapshot.
        return {'resolution':'vcs-reported','subjects':[source_path],'subjectKind':'file',
                'payload':{'path':source_path,'changeKind':'modified'},
                'minResolution':'vcs-reported','filter':('subject',source_path),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
    if relation=='declares':
        # The canonical single-rung syntax relation: syntax is authoritative for what a file
        # declares, so its ladder has exactly one rung and it can never be reported as degraded.
        return {'resolution':'syntactic','subjects':['symbol:foo'],'subjectKind':'symbol',
                'payload':{'container':'symbol:m','declared':'symbol:foo','declarationKind':'function'},
                'minResolution':'syntactic','filter':('subject','symbol:foo'),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
    raise C.AdmissionError('FIXTURE_RELATION_UNKNOWN:'+relation)

def build(resolved=True,has_match=False,source_path=None,with_finding=False,stdlib_body=b'declare const es2022: unknown;\n',universe_language='typescript',prepared=None,grant_operations=None,relation='references',workspace=None):
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
    native=native_inputs(objects,blobs,add,blob,stdlib_body,prepared,inventory,source_path,workspace)
    typescript=universe_language=='typescript'
    # Three registered universes now, not two. The syntax-only universe reaches the SAME
    # relation_fixture and the SAME Run closure: representability must be demonstrated by a real
    # graph that closes, not asserted by a registry row.
    UNIVERSE_SELECTION={
        'typescript':(native['universeDigest'],native['universe'],'native.semantic-universe.typescript.v2',
                      native['context'],None),
        'rust':(native['rustUniverseDigest'],native['rustUniverse'],'native.semantic-universe.rust.v2',
                native['rustContext'],{'sourceUnitOwnership':native['rust'].get('ownership')}),
        # No ownership record is passed: a grammar-only interpretation has no compilation unit to
        # own the body, and the syntax dialect axis is the suffix, so none is consulted.
        'syntax':(native['syntaxUniverseDigest'],native['syntaxUniverse'],'native.semantic-universe.syntax.v2',
                  native['syntaxContext'],None)}
    universe,universe_record,universe_domain,context_record,retained_inputs=UNIVERSE_SELECTION[universe_language]
    shape=relation_fixture(relation,source_path,source_body,source,
        universe_record,universe_domain,blob,context_record,retained_inputs)
    config=blob({'analysis':{'profileId':'default','capabilities':['references'],'budget':{'unit':'work-units','limit':1000}},'components':{},'discovery':{},'policy':{},'evidence':{}})
    scope_payload=blob({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})
    vcs=blob({'schemaVersion':2,'kind':'none','commitId':None,'dirty':False,'sourceInventoryDigest':blob(inventory)})
    snapshot=add('snapshot',projectId='prj1-'+'a'*64,sourceInventory=inventory,resolvedConfigDigest=config,scopeDigest=scope_payload,vcsDigest=vcs)
    atom={'op':'none','relation':relation,'minResolution':shape['minResolution'],
          'filters':[{'field':shape['filter'][0],'cmp':'eq','value':shape['filter'][1]}]}
    policy=policy_for(universe_language,atom,shape['subjectKind'])
    policy_digest=blob(policy);waiver_digest=blob(WAIVERS)
    program=compiled_program(policy);program_digest=blob(program)
    spec_payload=blob({'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'references','languageMode':language_mode,'workspaceRoot':'.','required':True}],'policyPackIds':['fixture.no-consumer'],'parameters':[]})
    grant=blob({'schemaVersion':2,'projectId':'prj1-'+'a'*64,'principals':[{'kind':'first-party','closureId':closure,'ownerSourceDigest':None}],'analysisOperations':sorted(grant_operations or ['native-analysis','read-source']),'scopeDigest':scope_payload})
    plan=add('plan',snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=sorted({closure,enumerator}),analysisSpecDigest=spec_payload,resolvedConfigDigest=config,nativeContextDigests=sorted({native['contextDigest'],native['rustContextDigest'],native['syntaxContextDigest']}),importIds=[],policyDigest=policy_digest,waiverDigest=waiver_digest,scopeDigest=scope_payload,budget={'unit':'work-units','limit':1000},semanticGrantDigest=grant)
    scope=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation=relation,resolution=shape['resolution'],enumeratorClosure=enumerator,subjects=shape['subjects'])
    # The REAL registered Coverage payload, minted through the actual native producer boundary, and
    # the REAL registered relation payload for references@resolved-binding.
    coverage_schema=blob(NATIVE_DOCUMENT_BYTES);fact_schema=blob(RELATION_DOCUMENT_BYTES)
    scope_descriptor=objects[scope][1]
    _own,_editions=retained_clone_ownership(universe,blobs)
    coverage_payload=coverage_result(scope_descriptor,universe,resolved,_own,_editions)
    admission=N.admit_coverage_result_v3(coverage_payload,scope_descriptor,[],coverage_schema)
    if admission['result']!='ADMIT':raise C.AdmissionError('FIXTURE_COVERAGE:'+','.join(admission['refusals'])+str(admission['faults']))
    coverage=add('coverage',scopeId=scope,payloadSchemaDigest=coverage_schema,payloadDigest=blob(coverage_payload))
    if coverage!=admission['coverageId']:raise C.AdmissionError('FIXTURE_COVERAGE_IDENTITY')
    facts=[]
    if has_match:
        if shape['payload'] is None:raise C.AdmissionError('FIXTURE_NO_ADMISSIBLE_PAYLOAD:'+relation)
        facts=[add('fact',snapshotId=snapshot,relation=relation,resolution=shape['resolution'],sourceUniverse=universe,targetUniverse=universe,producerClosure=closure,payloadSchemaDigest=fact_schema,payloadDigest=blob(shape['payload']),anchors=shape['anchors'],confidenceMillionths=1000000)]
    view=add('view',planId=plan,scopeIds=[scope],facts=facts,coverageIds=[coverage],producerClosure=closure,schemaDigests=sorted({coverage_schema,fact_schema}))
    stage_spec=blob({'schemaVersion':2,'planId':plan,'producerClosure':closure,'operation':'derive-references-view','parameters':[],'outputDomains':['view'],'outputSchemaDigest':blob(STAGE_OUTPUT_SCHEMA)})
    execution=add('execution-plan',planId=plan,stages=[{'ordinal':0,'stageSpecDigest':stage_spec,'requires':[],'outputDomains':['view']}])
    program_predicate=blob({'schemaVersion':2,'ruleProgramDigest':program_digest,'ruleId':'no-consumer','predicateId':'p','operation':'none','nodeDigest':hashlib.sha256(C.canonical(atom)).hexdigest()})
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
        projection=FILTER_FIELD_OF[fact['relation']].get(field)
        if fact['relation']==node['relation'] and projection is not None and C.equal_typed(payload.get(projection),value_wanted):matches.append(fid)
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
        own,editions=retained_clone_ownership(scope['sourceUniverse'],blobs)
        coverage['payloadDigest']=put_blob(blobs,coverage_result(scope,scope['sourceUniverse'],resolved,own,editions))
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

def graph_with_import(correspondence='exact', foreign_snapshot=False, bad_mapping=False, dirty=False, missing_mapping=False, build_identity=None, declared_builds=None, assets=None):
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
    # `blobs` is the AUXILIARY ASSET inventory, not the import's mandatory custody: the payload
    # bytes and the exact registered schema document bytes are retained and re-hashed independently
    # of it. `assets=None` keeps the harness default of one real retained asset row (import blob
    # sha256 is `raw-artifact`, so the closure re-hashes it and an unretained row cannot close);
    # `assets=[]` is the lawful zero-asset import of a self-contained normalized payload.
    if assets is None:
        artifact=b'{"coverage":[]}';assets=[{'path':'coverage/v8.json','sha256':put(artifact),'bytes':len(artifact)}]
    record=W.build_import('runtime',payload,payload['payloadDomain'],schemas,corr,closure,closure,assets,scope,{})
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

def mirror_admits(document,selector,value):
    """Same instance, both documents. Returns None on admission or the refusal text."""
    W=M.workflow_admission()
    try:W.validate_import_record(document,selector,value);return None
    except W.Refusal as exc:return str(exc.detail)

SCOPE_DOCUMENT={'schemaFamily':'opensip.product.scope','schemaMajor':1,
                'include':['src/**/*.ts'],'exclude':['src/**/*.test.ts']}

def shared_workspace(selected,enumeration='complete',units=None,rows=None):
    return {'edition':{'fixture-root':2021},'enumeration':enumeration,
            'units':copy.deepcopy(units if units is not None else SHARED_UNITS),
            'selectedUnitIds':list(selected),
            'ownership':copy.deepcopy(rows if rows is not None else SHARED_ROWS)}
