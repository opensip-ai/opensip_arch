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

# The pinned inherited body recipe this bundle REUSES rather than restates. Blind kits must
# carry it: without these selectors bodyIdentity cannot be reconstructed at all.
FACT_IDENTITY_POLICY=json.loads((H.parents[1]/'artifacts/fact-identity-policy.v2.json').read_text())
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
            'package-lock.json':b'{"lockfileVersion":3}\n',
            # The workspace package manifest: an ordinary inventoried repository source, and the
            # subject a `package` relation fact declares.
            'package.json':b'{"name":"fixture-workspace","version":"1.0.0"}\n',
            # A JavaScript source the SAME TypeScript engine reads. Native 6.3 makes its normalized
            # body a `javascript` fact, not a `typescript` one, even with identical bytes.
            'legacy.js':b'export const foo = 1;\n'}
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

# The registered references@resolved-binding payload: exactly the inherited field set
# {referrer, name, resolvedBinding} with SubjectIdV1 / CanonicalText values.
REFERENCES_PAYLOAD={'referrer':'symbol:foo','name':'foo','resolvedBinding':'symbol:foo'}
# The policy DSL's closed FieldFilter vocabulary (subject/target/...) projected onto the registered
# relation payload's own field names. The projection is the detector closure's, not the encoder's,
# and it is PER RELATION: a `file` payload has no `referrer`, so one flat table across relations was
# a fixture-only fiction. A relation with no projection for a field simply matches nothing.
FILTER_FIELD_OF={
 'references':{'subject':'referrer','target':'name','resolution':'name',
               'universe':'name','subjectKind':'name','targetKind':'name','observability':'name'},
 'file':{'subject':'path','target':'path'},
 'clones':{'subject':'bodyIdentity','target':'bodyIdentity'},
 'package':{'subject':'packageName','target':'packageName'},
 'vcs-change':{'subject':'path','target':'path'},
 'declares':{'subject':'declared','target':'declared'},
 'imports':{'subject':'importer','target':'specifier'},
 'calls':{'subject':'caller','target':'calleeText'},
 'types':{'subject':'subject','target':'typeText'},
 'reachability':{'subject':'origin','target':'reachable'}}

def coverage_result(scope_descriptor,universe,resolved,blobs=None,inventory_paths=None):
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
    # The (deficiency, nativeCause) pair is DERIVED by the owning producer unit from the COMMITTED
    # ownership and THIS scope's subjects, recovered from the RETAINED frames exactly as the Run
    # closure reaches them: the universe h-frame, then the nested source-unit-ownership h-frame the
    # universe names. It is never read from the claim being judged, and Run closure re-derives the
    # same pair independently, so this helper cannot define the law by emitting whatever it likes.
    disclosure={'deficiency':None if resolved else 'resolution-incomplete','nativeCause':None}
    # A request this universe CANNOT serve is disclosed, not answered. The producer derives the
    # published unavailable pair from the admitted selected grammars and the committed examined
    # extent, exactly as the Run closure re-derives it; a scope that claims `complete` for an
    # unavailable capability is refused there. Support is decided by the closed per-language
    # registry, never by whether facts happen to exist.
    unavailable=None
    if blobs is not None and inventory_paths is not None:
        try:_d,_u,_r=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_d,_u,_r=None,None,None
        if _d=='native.semantic-universe.syntax.v2':
            _ctx=blobs.get(_u[_r['contextField'][0]].removeprefix('sha256:'))
            if _ctx is not None:
                _context=M.parse_h_frame(_ctx,'native-context')[1]
                _selected=set(_u['selectedGrammarIds'])
                _languages={g['languageId'] for g in _context['grammarBundle']['grammars']
                            if g['grammarId'] in _selected}
                unavailable=N.syntax_capability_support(_languages,scope_descriptor['relation'],
                    scope_descriptor['resolution'],list(inventory_paths),False)
    if unavailable is not None:
        disclosure=dict(unavailable)
    elif scope_descriptor['relation']=='clones' and blobs is not None:
        try:_domain,_universe,_row=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_universe,_row=None,None
        # The ownership prerequisite is derived from the ACTUAL UNIVERSE KIND: it applies only where
        # the universe declares the compilation-ownership dialect axis, which is the Rust universe.
        # A grammar-only interpretation has no compilation unit and therefore no ownership
        # obligation at all - the syntax-universe contract says so - and an earlier revision of this
        # helper conflated a missing AXIS with a missing RECORD: it passed ownership=None for a
        # syntax universe, and None is defined in clone_ownership_disclosure as `no committed
        # ownership`, a genuine Rust fault. That produced complete + input-closure-incomplete /
        # body-language-ownership-missing on a healthy compiler-free clone control. The Run-closure
        # guard was already correct; only this producer helper was wrong.
        if _row is not None and 'ownership' in (_row.get('languageVersionBinding',{}).get('dialect') or {}):
            ownership,edition_map=None,(_universe.get('edition') or {})
            reference=_universe.get('sourceUnitOwnershipId')
            frame=None if reference is None else blobs.get(reference.removeprefix('sha256:'))
            if frame is not None:ownership=M.parse_h_frame(frame,'native-nested')[1]
            owed=N.clone_ownership_disclosure(ownership,scope_descriptor['subjects'],edition_map)
            if owed is not None:
                disclosure={'deficiency':owed['deficiency'],'nativeCause':owed['nativeCause']}
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
               'derivationKinds':[],'confidenceMillionths':1000000,**disclosure}}

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

# One retained grammar definition per BUNDLED language, derived FROM the host's own table so the
# fixture bundle cannot drift from what the host actually bundles. The host bundles seven languages,
# not three: an earlier revision declared only tsjs and rust, and its single tsjs row also claimed
# languageId `typescript` for the `.js/.jsx/.mjs/.cjs` suffixes the table routes to `javascript`.
# Self-contained on purpose: this declaration is extracted by name into the shared integration
# fixture, so it must not depend on another module-level name that the extraction does not carry.
GRAMMAR_FILES={**{'grammar/%s.grammar'%language:('// fixture %s grammar\n'%language).encode()
                  for language in sorted(set(N.BUNDLED_GRAMMARS.values()))},
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
        # Derived from the host's own BUNDLED_GRAMMARS so the bundle cannot drift from what the
        # host actually bundles. section 6.3 gives body spans and an L1-L3 normalisation table to
        # the code languages only, so those are `code` and the data/document grammars are not; the
        # class is read from the foundation body-language domain rather than restated here.
        'grammars':sorted(({'grammarId':language+'.v1','grammarVersion':'1.0.0','languageId':language,
             'syntaxClass':N.GRAMMAR_CAPABILITY_REGISTRY['languages'][language]['syntaxClass'],
             'suffixes':sorted((s for s,l in N.BUNDLED_GRAMMARS.items() if l==language),
                               key=lambda s:s.encode()),
             'grammarDigest':members['grammar/%s.grammar'%language]}
            for language in sorted(set(N.BUNDLED_GRAMMARS.values()))),
            key=lambda g:g['grammarId'].encode()),
        'normalizer':{'normalizerId':'opensip-normalizer','normalizerVersion':'1.0.0',
                      'specificationDigest':members['grammar/normalize.l0.spec']}}}
    admission=N.admit_native_context('syntax',context,{closure:objects[closure][1]})
    if admission['refusals']:raise C.AdmissionError('FIXTURE_SYNTAX_CONTEXT:'+','.join(admission['refusals']))
    universe={'schemaVersion':2,'nativeContextId':admission['nativeContextId'],
              # Every bundled grammar is selected: the analysis parses code AND data/document
              # members. Selection stays explicit and part of the universe identity.
              'selectedGrammarIds':sorted(g['grammarId'] for g in context['grammarBundle']['grammars']),
              'resolutionAttempted':False}
    binding=N.bind_syntax_universe(universe,admission,context,{},[])
    if binding['result']!='ADMIT':raise C.AdmissionError('FIXTURE_SYNTAX_UNIVERSE:'+','.join(binding['refusals']))
    context_digest=M.native_context_frame('native.context.syntax.v2',context,blobs)
    universe_digest=M.native_universe_frame('native.semantic-universe.syntax.v2',universe,blobs)
    if context_digest!=admission['planNativeContextDigest'] or universe_digest!=binding['sourceUniverse']:
        raise C.AdmissionError('FIXTURE_SYNTAX_IDENTITY')
    return {'contextDigest':context_digest,'universeDigest':universe_digest,'context':context,
            'universe':universe,'admission':admission,'closure':closure,'members':members,
            'closures':{closure:objects[closure][1]}}

LANGUAGE_FIXTURE={
 'typescript':{'languageMode':'ts-tsconfig','sourcePath':'a.ts','sourceBytes':b'export const foo = 1;\n'},
 'rust':{'languageMode':'rust-cargo','sourcePath':'src/lib.rs','sourceBytes':RUST_SOURCES['src/lib.rs']},
 # The syntax-only mode. Its source path is deliberately a .rs file: under the syntax universe that
 # body is read by the bundled grammar with NO Cargo, no edition and no ownership record, which is
 # exactly the case the compiler universes cannot represent.
 'syntax':{'languageMode':'syntax-only','sourcePath':'src/lib.rs','sourceBytes':RUST_SOURCES['src/lib.rs']}}

# A fixture stand-in for the RETAINED canonical level specification of one normalisation level. Its
# CONTENT is FACT-IDENTITY's to write; what this bundle demonstrates is custody and joining, so what
# matters here is that these exact bytes are retained and that normalisationVersion is their raw
# SHA-256 rather than a version label or an opaque caller hash.
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
    # The four remaining SEMANTIC relations. They were previously unconstructible here, so a probe
    # asking for them under a syntax universe failed at FIXTURE_RELATION_UNKNOWN before Run
    # admission - a constructor limitation, never a negative admission result and never evidence
    # that the guard works. Each carries its registered payload and a top rung, so the capability
    # guard is actually REACHED and its refusal is the one under test.
    SEMANTIC_SHAPES={
     'imports':('resolved-target',{'importer':'symbol:m','specifier':'./x','resolvedTarget':'symbol:foo'}),
     'calls':('resolved-callee',{'caller':'symbol:m','calleeText':'foo','resolvedCallee':'symbol:foo'}),
     'types':('checked',{'subject':'symbol:foo','typeText':'number','checkedType':'symbol:number'}),
     'reachability':('from-resolved-calls',{'origin':'symbol:m','reachable':'symbol:foo'})}
    if relation in SEMANTIC_SHAPES:
        rung,payload=SEMANTIC_SHAPES[relation]
        return {'resolution':rung,'subjects':['symbol:foo'],'subjectKind':'symbol','payload':payload,
                'minResolution':rung,'filter':('subject','symbol:foo'),
                'anchors':[{'path':source_path,'blobDigest':source,'startByte':0,'endByte':len(source_body)}]}
    raise C.AdmissionError('FIXTURE_RELATION_UNKNOWN:'+relation)

def build(resolved=True,has_match=False,source_path=None,with_finding=False,stdlib_body=b'declare const es2022: unknown;\n',universe_language='typescript',prepared=None,grant_operations=None,relation='references',workspace=None,pure_syntax=False):
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
    # `pure_syntax` builds a GRAMMAR-ONLY REPOSITORY: the snapshot carries only grammar-bearing
    # source files and NO Cargo.toml/tsconfig.json/package.json, and the Plan names only the syntax
    # native context. The ordinary path unions TS_SOURCES and RUST_SOURCES into the inventory and
    # puts all three contexts in the Plan, so changing only `source_path` to a .md file does NOT
    # demonstrate a repository without compiler units - it demonstrates a file-inventory Run inside a
    # mixed repository. Both are useful; only this one is evidence about a compiler-free repository.
    SYNTAX_ONLY_SOURCES={'docs/guide.md':b'# fixture guide\n','data/settings.json':b'{"a":1}\n',
                         'config/app.yaml':b'a: 1\n','build/opts.toml':b'a = 1\n'}
    sources=dict(SYNTAX_ONLY_SOURCES) if pure_syntax else {**TS_SOURCES,**RUST_SOURCES}
    inventory=sorted([{'path':p,'sha256':blob(b),'bytes':len(b)}
        for p,b in {**sources,source_path:source_body}.items()],key=lambda r:r['path'].encode())
    if pure_syntax:
        def tree(files):return sorted(({'path':p,'sha256':blob(v),'bytes':len(v)} for p,v in files.items()),
                                      key=lambda r:r['path'].encode())
        _syntax=syntax_inputs(objects,blobs,add,blob,tree)
        native={'syntaxContextDigest':_syntax['contextDigest'],'syntaxContext':_syntax['context'],
                'syntaxUniverseDigest':_syntax['universeDigest'],'syntaxUniverse':_syntax['universe'],
                'contextDigests':[_syntax['contextDigest']]}
    else:
        native=native_inputs(objects,blobs,add,blob,stdlib_body,prepared,inventory,source_path,workspace)
        native['contextDigests']=[native['contextDigest'],native['rustContextDigest'],native['syntaxContextDigest']]
    typescript=universe_language=='typescript'
    # Three registered universes now, not two. The syntax-only universe reaches the SAME
    # relation_fixture and the SAME Run closure: representability must be demonstrated by a real
    # graph that closes, not asserted by a registry row.
    # Selected lazily: under `pure_syntax` the compiler universes are never built at all, so
    # evaluating their entries would fail rather than simply going unused.
    if universe_language=='typescript':
        universe,universe_record,universe_domain,context_record,retained_inputs=(
            native['universeDigest'],native['universe'],'native.semantic-universe.typescript.v2',
            native['context'],None)
    elif universe_language=='rust':
        universe,universe_record,universe_domain,context_record,retained_inputs=(
            native['rustUniverseDigest'],native['rustUniverse'],'native.semantic-universe.rust.v2',
            native['rustContext'],{'sourceUnitOwnership':native['rust'].get('ownership')})
    else:
        # No ownership record is passed: a grammar-only interpretation has no compilation unit to
        # own the body, and the syntax dialect axis is the suffix, so none is consulted.
        universe,universe_record,universe_domain,context_record,retained_inputs=(
            native['syntaxUniverseDigest'],native['syntaxUniverse'],'native.semantic-universe.syntax.v2',
            native['syntaxContext'],None)
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
    plan=add('plan',snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=sorted({closure,enumerator}),analysisSpecDigest=spec_payload,resolvedConfigDigest=config,nativeContextDigests=sorted(set(native['contextDigests'])),importIds=[],policyDigest=policy_digest,waiverDigest=waiver_digest,scopeDigest=scope_payload,budget={'unit':'work-units','limit':1000},semanticGrantDigest=grant)
    scope=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation=relation,resolution=shape['resolution'],enumeratorClosure=enumerator,subjects=shape['subjects'])
    # The REAL registered Coverage payload, minted through the actual native producer boundary, and
    # the REAL registered relation payload for references@resolved-binding.
    coverage_schema=blob(NATIVE_DOCUMENT_BYTES);fact_schema=blob(RELATION_DOCUMENT_BYTES)
    scope_descriptor=objects[scope][1]
    coverage_payload=coverage_result(scope_descriptor,universe,resolved,blobs,[r['path'] for r in inventory])
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
        _paths=[r['path'] for r in objects[scope['snapshotId']][1]['sourceInventory']]
        coverage['payloadDigest']=put_blob(blobs,coverage_result(scope,scope['sourceUniverse'],resolved,blobs,_paths))
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
# Auxiliary-asset cardinality is 0..4096, proved through a COMPLETE Run rather than descriptor
# validation alone. A zero-asset import is the self-contained normalized payload case: its payload
# bytes and its exact registered schema document bytes are still retained and re-hashed, so custody
# is unaffected. An earlier revision required one asset on the theory that adapterClosure implied
# custody of bytes named by sourcePath; sourcePath is a UserInputPath that never enters a content
# identity and has no join to this array, so that theory was withdrawn.
check('import-zero-auxiliary-assets-closes-a-run',
      M.close_run(*graph_with_import(assets=[])).startswith('run2:'))
def zero_asset_wrapper():
    run,objects,blobs=graph_with_import(assets=[])
    return next(v for k,(d,v) in objects.items() if d=='import')
_ZERO=zero_asset_wrapper()
check('import-zero-asset-wrapper-still-retains-its-payload-and-schema',
      _ZERO['blobs']==[] and len(_ZERO['payloadDigest'])==64 and len(_ZERO['payloadSchemaDigest'])==64)
MIRROR_DOCS=[('foundation/identity-schemas.v2.json','#/$defs/import'),
             ('workflows/schemas/imported-evidence.schema.json','#/$defs/ImportWrapperV2')]
def mirror_admits(document,selector,value):
    """Same instance, both documents. Returns None on admission or the refusal text."""
    W=M.workflow_admission()
    try:W.validate_import_record(document,selector,value);return None
    except W.Refusal as exc:return str(exc.detail)
for _doc,_sel in MIRROR_DOCS:
    check('import-zero-asset-admitted-by.'+_sel.rpartition('/')[2],
          mirror_admits(_doc,_sel,_ZERO) is None)
# The published maximum still bites, on the same instance, through both documents.
_OVER=dict(_ZERO,blobs=[{'path':'a/%05d'%i,'sha256':'a'*64,'bytes':1} for i in range(4097)])
for _doc,_sel in MIRROR_DOCS:
    check('import-4097-assets-refused-by.'+_sel.rpartition('/')[2],
          mirror_admits(_doc,_sel,_OVER) is not None)
rejects('review-import-foreign-exact-source',lambda:M.close_run(*graph_with_import(foreign_snapshot=True)))
check('review-import-current-vcs-mapping',M.close_run(*graph_with_import(correspondence='vcs')).startswith('run2:'))
check('review-import-declared-build-context',M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a',declared_builds=['build-a'])).startswith('run2:'))
rejects('review-import-build-label-cannot-self-authorize',lambda:M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a')))
rejects('review-import-wrong-build-context',lambda:M.close_run(*graph_with_import(correspondence='vcs',build_identity='build-a',declared_builds=['build-b'])))
for kw in ({'foreign_snapshot':True},{'bad_mapping':True},{'dirty':True},{'missing_mapping':True}):
    rejects('review-import-vcs-refused-'+str(kw),lambda kwargs=kw:M.close_run(*graph_with_import(correspondence='vcs',**kwargs)))

# ------------------------------------------- ScopeDocumentV1 as a registered analysis-spec parameter
# comparison-result EvaluationContext.scopeDigest is the workflow glob SCOPE-POLICY document and its
# contract requires it to be bound as an analysis-spec parameter. The parameter class was closed to
# one document, so that binding refused at Plan admission and the comparison scope axis could not be
# populated at all. The row exists now; these cases prove the binding closes, that the two scope
# records stay distinct, and that the class is still closed against anything unregistered.
SCOPE_DOCUMENT={'schemaFamily':'opensip.product.scope','schemaMajor':1,
                'include':['src/**/*.ts'],'exclude':['src/**/*.test.ts']}
POLICY_DOCUMENT_BYTES=(H.parent/'workflows/schemas/policy-document.schema.json').read_bytes()
def run_with_parameter(schema_bytes,payload_value):
    run,objects,blobs=build(resolved=True,has_match=True)
    put=lambda value:put_blob(blobs,value)
    plan=copy.deepcopy(objects[run['planId']][1])
    analysis=C.parse(blobs[plan['analysisSpecDigest']])
    analysis['parameters']=[{'schemaDigest':put(schema_bytes),'payloadDigest':put(payload_value)}]
    plan['analysisSpecDigest']=put(analysis)
    rekey_plan(objects,blobs,run,plan)
    return M.close_run(run,objects,blobs)
check('scope-document-parameter-binding-closes',
      run_with_parameter(POLICY_DOCUMENT_BYTES,SCOPE_DOCUMENT).startswith('run2:'))
rejects_because('scope-document-parameter-must-satisfy-its-selector',
    lambda:run_with_parameter(POLICY_DOCUMENT_BYTES,{'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':[],'exclude':[]}),
    'PAYLOAD_RECORD:#/$defs/ScopeDocumentV1')
# The repository extent and the policy glob selection are different records under different rows.
rejects_because('foundation-scope-descriptor-is-not-a-scope-document',
    lambda:run_with_parameter(POLICY_DOCUMENT_BYTES,{'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]}),
    'PAYLOAD_RECORD:#/$defs/ScopeDocumentV1')
rejects_because('scope-document-is-not-an-import-source-context',
    lambda:run_with_parameter((H/'import-source-context.schema.json').read_bytes(),SCOPE_DOCUMENT),
    'PAYLOAD_RECORD:')
check('scope-document-and-plan-scope-descriptor-are-distinct-digests',
      hashlib.sha256(C.canonical(SCOPE_DOCUMENT)).hexdigest()!=
      hashlib.sha256(C.canonical({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})).hexdigest())
# The class is still closed: a real but unregistered document, and a permissive one, both refuse.
rejects_because('parameter-class-still-refuses-an-unregistered-real-document',
    lambda:run_with_parameter((H/'identity-schemas.v2.json').read_bytes(),SCOPE_DOCUMENT),
    'PAYLOAD_PARAMETER_UNREGISTERED')
rejects_because('parameter-class-still-refuses-a-caller-chosen-permissive-document',
    lambda:run_with_parameter(C.canonical({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:hostile:permissive-parameter','type':'object'}),SCOPE_DOCUMENT),
    'PAYLOAD_PARAMETER_UNREGISTERED')
check('parameter-registry-rows-have-distinct-document-digests',
      len({hashlib.sha256((H.parent/row['document']).read_bytes()).hexdigest()
           for row in M.PAYLOADS['classes']['parameter']['rows'].values()})
      ==len(M.PAYLOADS['classes']['parameter']['rows']))

# --------------------------------------------------- policy atom relation/rung closed AT THE CLOSURE
# The Run closure admits the Plan's PolicyDocumentV1 and the proof's compiled RuleProgramV1. Their
# atoms name a relation and a minimum rung, and the SCHEMA can only say `relation` is a canonical
# identifier and `minResolution` is a member of the flat rung vocabulary. That vocabulary is shared
# across relations, so `resolved-callee` reads as a well-formed value on a `references` atom. If the
# rung were closed only in the evaluator, a sealed Run could assert a predicate that was never
# admissible. These cases re-mint the policy AND the compiled program so the refusal is the atom,
# not a compilation-join staleness.
def run_with_atom(atom,program_only=False,policy_only=False,evidence_use=None):
    run,objects,blobs=build(resolved=True,has_match=True)
    put=lambda value:put_blob(blobs,value)
    plan=copy.deepcopy(objects[run['planId']][1])
    policy=C.parse(blobs[plan['policyDigest']])
    program=compiled_program(policy)
    if not program_only:
        policy['rules'][0]['emitWhen']=copy.deepcopy(atom)
    if evidence_use is not None:
        policy['rules'][0]['evidenceUse']=copy.deepcopy(evidence_use)
    if not policy_only:
        program=compiled_program(policy)
        program['rules'][0]['emitWhen']=copy.deepcopy(atom)
        program['policyDigest']=hashlib.sha256(C.canonical(policy)).hexdigest()
    else:
        program=compiled_program(policy)
    plan['policyDigest']=put(policy)
    program_digest=put(program)
    pk=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pk][1])
    proof['ruleProgramDigest']=program_digest
    # The witness addresses a node OF that program, so the address record must be re-derived; a
    # stale one refuses on the addressing join and the case would prove nothing about the atom.
    for pred in proof['predicateProofs']:
        witness=C.parse(blobs[pred['witnessDigest']])
        record=C.parse(blobs[witness['programPredicateDigest']])
        node=M.predicate_node_at(
            next(r for r in program['rules'] if r['ruleId']==record['ruleId'])['emitWhen'],
            record['predicateId'])
        record.update(ruleProgramDigest=program_digest,operation=node['op'],
                      nodeDigest=hashlib.sha256(C.canonical(node)).hexdigest())
        witness['programPredicateDigest']=put(record)
        pred['witnessDigest']=put(witness);pred['operation']=node['op']
    rekey(objects,pk,proof,run)
    # The seal carries the selected policy too; leaving it stale would refuse on VERDICT_JOIN.
    seal_key=run['evaluationSealId'];seal=copy.deepcopy(objects[seal_key][1])
    seal['policyDigest']=plan['policyDigest'];rekey(objects,seal_key,seal,run)
    rekey_plan(objects,blobs,run,plan)
    return M.close_run(run,objects,blobs)
LAWFUL_ATOM={'op':'none','relation':'references','minResolution':'resolved-binding',
             'filters':[{'field':'target','cmp':'eq','value':'foo'}]}
check('policy-atom-positive-control-closes',run_with_atom(LAWFUL_ATOM).startswith('run2:'))

# ------------------- the two policy-admission boundaries must give ONE answer (Codex M2 follow-up)
# An earlier revision had this closure call `admit_atom` alone while `resolve_policy` additionally
# enforced the rule-level evidenceUse obligation. The same policy was therefore refused by policy
# admission (IMPORT.ABSENT_FOR_PREDICATE) and admitted by the Run closure. Whether an atom may
# consume imported evidence is part of whether the atom is admissible, so the closure now reuses the
# COMPLETE per-rule admission. Both examples below are empty/indeterminate with absent runtime
# evidence: this is a declaration-admission law, not a claim about findings.
EVIDENCE_ATOM={'op':'exists','relation':'runtime-observation','minResolution':'observed',
               'filters':[],'evidence':'runtime'}
DECLARED=[{'kind':'runtime','requirement':'required'}]
def policy_admission_refusal(atom,evidence_use):
    """resolve_policy's answer for a one-rule policy carrying this atom and declaration."""
    rule=dict(rule_for('typescript',copy.deepcopy(atom),'symbol'),evidenceUse=copy.deepcopy(evidence_use))
    W=M.workflow_admission()
    try:W.resolve_policy({'schemaFamily':'opensip.product.policy','schemaMajor':1,
                          'gateSeverityAtLeast':'error','rules':[rule]});return None
    except W.Refusal as exc:return str(exc.detail)
def closure_refusal(atom,evidence_use):
    try:run_with_atom(atom,evidence_use=evidence_use);return None
    except C.AdmissionError as exc:return str(exc)
for label,atom,use in [('declared-evidence-atom',EVIDENCE_ATOM,DECLARED),
                       ('undeclared-evidence-atom',EVIDENCE_ATOM,[]),
                       ('wrong-kind-declaration',EVIDENCE_ATOM,[{'kind':'history','requirement':'required'}]),
                       ('native-atom-needs-no-declaration',LAWFUL_ATOM,[])]:
    _policy_answer=policy_admission_refusal(atom,use)
    _closure_answer=closure_refusal(atom,use)
    check('policy-admission-and-run-closure-agree.'+label,
          (_policy_answer is None)==(_closure_answer is None))
check('an-undeclared-evidence-atom-is-refused-by-policy-admission',
      policy_admission_refusal(EVIDENCE_ATOM,[])=='IMPORT.ABSENT_FOR_PREDICATE')
rejects_because('an-undeclared-evidence-atom-is-refused-at-the-run-closure-too',
    lambda:run_with_atom(EVIDENCE_ATOM,evidence_use=[]),
    'POLICY_RULE_NOT_ADMISSIBLE:policy:')
check('a-declared-evidence-atom-still-closes-a-run',
      run_with_atom(EVIDENCE_ATOM,evidence_use=DECLARED).startswith('run2:'))
check('policy-atom-weaker-rung-of-same-ladder-closes',
      run_with_atom(dict(LAWFUL_ATOM,minResolution='syntactic-name-match')).startswith('run2:'))
# The withdrawn abstract tiers are refused one layer EARLIER than the rest: they are no longer
# members of the rung vocabulary at all, so PolicyDocumentV1 schema admission rejects them before
# the ladder question is asked. That is the stronger refusal and is asserted as such; the cases
# below are the ones the schema cannot decide, because their values ARE well-formed rung names.
for tier in ['syntax','resolved','type','external']:
    rejects_because('policy-atom-withdrawn-tier-'+tier+'-is-not-even-vocabulary',
        lambda t=tier:run_with_atom(dict(LAWFUL_ATOM,minResolution=t)),'FOREIGN_RECORD:#/$defs/PolicyDocumentV1')
BAD_ATOMS=[('cross-relation-rung',dict(LAWFUL_ATOM,minResolution='resolved-callee')),
           ('single-rung-relations-rung',dict(LAWFUL_ATOM,minResolution='enumerated')),
           ('unregistered-relation',dict(LAWFUL_ATOM,relation='not-a-relation')),
           ('evidence-relation-without-kind',dict(LAWFUL_ATOM,relation='runtime-observation',minResolution='observed'))]
for label,bad_atom in BAD_ATOMS:
    # The POLICY path now runs the COMPLETE per-rule admission, so its refusal is
    # POLICY_RULE_NOT_ADMISSIBLE; the atom fault is still the reason, and it is still at the closure.
    rejects_because('policy-atom-'+label+'-refused-at-closure',
        lambda a=bad_atom:run_with_atom(a),'POLICY_RULE_NOT_ADMISSIBLE:policy:')
    # Checking the policy is sufficient for the compiled program because the program is not a free
    # artifact: it must be the EXACT projection of the selected policy's rules, so a program
    # carrying an atom its policy does not carry cannot reach the atom check at all. The refusal is
    # the compilation join, which is the stronger guarantee; asserting it here keeps that reasoning
    # honest instead of leaving a test that looks like it proves atom admission and does not.
    rejects_because('policy-atom-'+label+'-cannot-be-smuggled-into-the-compiled-program',
        lambda a=bad_atom:run_with_atom(a,program_only=True),'RULE_PROGRAM_COMPILATION_JOIN')
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
LANGUAGE_OF={'native.context.typescript.v2':'typescript','native.context.rust.v2':'rust','native.context.syntax.v2':'syntax'}
frames={d:M.parse_h_frame(blobs[d],'native-context') for d in plan['nativeContextDigests']}
retained_closures={k:v for k,(d,v) in objects.items() if d=='closure'}
check('native-context-all-registered-domains-close',
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

# ------------------------------------------------------------- syntax-only universe (CB3-MUST-3)
# The capability matrix advertises declares/literal/control-flow@syntactic and
# clones@normalized-body-hash for the syntax-only mode, and inventory facts (file, package,
# vcs-change) must be representable in a repository with NO TypeScript and NO Rust unit at all.
# fact2 and subject-scope both REQUIRE a universe h-identity from a closed domain set that held only
# the two compiler universes, so every one of those advertised cells could mint no fact and no
# scope. This is the positive Run that proves the third registered universe closes the gap; the
# controls below prove it did not open a hole while doing so.
syrun,syobjects,syblobs=build(resolved=False,has_match=True,universe_language='syntax',relation='declares')
syntax_run_id=M.close_run(syrun,syobjects,syblobs)
check('syntax-only-universe-complete-run-closes',syntax_run_id.startswith('run2:'))
syscope=next(v for k,(d,v) in syobjects.items() if d=='subject-scope')
syfact=next(v for k,(d,v) in syobjects.items() if d=='fact')
syntax_frame=M.parse_h_frame(syblobs[syscope['sourceUniverse']],'native-semantic-universe')
check('syntax-run-scope-and-fact-carry-the-syntax-universe',
      syntax_frame[0]=='native.semantic-universe.syntax.v2' and
      syfact['sourceUniverse']==syscope['sourceUniverse']==syscope['targetUniverse'])
check('syntax-run-fact-is-a-syntactic-rung-of-its-own-relation',
      syfact['relation']=='declares' and syfact['resolution']=='syntactic')
check('syntax-run-coverage-binds-the-syntax-scope',
      next(v for k,(d,v) in syobjects.items() if d=='coverage')['scopeId'] in
      next(v for k,(d,v) in syobjects.items() if d=='view')['scopeIds'])
check('syntax-universe-declares-no-resolution-attempt',syntax_frame[1]['resolutionAttempted'] is False)
check('syntax-run-is-a-different-run-from-both-compiler-runs',
      syntax_run_id!=rust_run_id and syntax_run_id!=M.close_run(*build(resolved=True,has_match=True)))
# Inventory relations in a grammar-only universe: the ADV-3 half of this finding. `file`, `package`
# and `vcs-change` name no compiler at all, and these are the facts a repository with no TypeScript
# and no Rust unit consists of.
for inventory_relation in ('file','package','vcs-change'):
    check('syntax-universe-carries-inventory-relation-'+inventory_relation,
          M.close_run(*build(resolved=False,has_match=True,universe_language='syntax',
                             relation=inventory_relation)).startswith('run2:'))

SYNTAX_ROW=M.DIGESTS['domainSets']['native-semantic-universe']['native.semantic-universe.syntax.v2']
def _syntax_fixture_specimen():
    """One admitted syntax context, built in its own store, so the grammar-class controls below can
    mutate a real admitted bundle instead of a hand-written stand-in."""
    objects,blobs={},{}
    blob=lambda value:put_blob(blobs,value)
    def add(domain,**fields):
        value=dict(fields,schemaVersion=2);key=M.identifier(domain,value)
        objects[key]=(domain,value);return key
    def tree(files):return sorted(({'path':p,'sha256':blob(v),'bytes':len(v)} for p,v in files.items()),
                                  key=lambda r:r['path'].encode())
    return syntax_inputs(objects,blobs,add,blob,tree)
_SYNTAX_SPECIMEN=_syntax_fixture_specimen()
SYNTAX_FIXTURE_CONTEXT=_SYNTAX_SPECIMEN['context']
SYNTAX_FIXTURE_BUNDLE=SYNTAX_FIXTURE_CONTEXT['grammarBundle']
SYNTAX_FIXTURE_CLOSURES=_SYNTAX_SPECIMEN['closures']

# ------------------------------- the ALREADY BUNDLED data/document grammars (root's M3 recheck)
# The host bundles seven languages, not three. An earlier revision's grammar descriptor admitted
# only typescript/javascript/rust and asserted equality with the body-language-version enum as a
# positive drift check; that could not express `.json`, `.toml`, `.md` or `.yaml`, all of which
# `assign_membership` already routes to membership `syntax-only`, reason `grammar-only`. The promise
# in native-evidence 1.2 - ANY file whose extension maps to a bundled grammar - was therefore
# unrepresentable for four grammars the host has always shipped.
check('every-bundled-language-is-representable-in-the-grammar-descriptor',
      {g['languageId'] for g in SYNTAX_FIXTURE_BUNDLE['grammars']}==set(N.BUNDLED_GRAMMARS.values())
      and len(set(N.BUNDLED_GRAMMARS.values()))==7)
check('every-bundled-suffix-is-claimed-by-exactly-one-grammar-row',
      sorted(s for g in SYNTAX_FIXTURE_BUNDLE['grammars'] for s in g['suffixes'])
      ==sorted(N.BUNDLED_GRAMMARS))
# The exact distinction the original contracts already draw, now machine-readable: section 6.3 gives
# body spans and an L1-L3 normalisation table to the code languages only, and the clone preimage
# languageId is closed to them. Data/document grammars are bundled and accounted, never `unsupported`.
check('code-grammars-are-exactly-the-clone-body-identity-languages',
      {g['languageId'] for g in SYNTAX_FIXTURE_BUNDLE['grammars'] if g['syntaxClass']=='code'}
      ==set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum']))
check('data-document-grammars-claim-no-clone-body-identity',
      {g['languageId'] for g in SYNTAX_FIXTURE_BUNDLE['grammars'] if g['syntaxClass']=='data-document'}
      =={'json','toml','markdown','yaml'})
# A COMPLETE Run over a GRAMMAR-ONLY REPOSITORY: the snapshot carries only grammar-bearing data and
# document files - no Cargo.toml, no tsconfig.json, no package.json - and the Plan names ONLY the
# syntax native context. This is the compiler-free case. Simply pointing the ordinary builder at a
# .md path does NOT demonstrate it: that builder unions TS_SOURCES and RUST_SOURCES into the
# snapshot and puts all three contexts in the Plan, so it is a file-inventory Run inside a MIXED
# repository. Both shapes are exercised, and only this one is evidence about the compiler-free case.
PURE=build(resolved=False,has_match=True,universe_language='syntax',relation='file',
           source_path='docs/guide.md',pure_syntax=True)
check('a-grammar-only-repository-closes-a-complete-run',M.close_run(*PURE).startswith('run2:'))
_PURE_PLAN=PURE[1][PURE[0]['planId']][1]
check('a-grammar-only-repository-plan-names-only-the-syntax-context',
      [M.parse_h_frame(PURE[2][d],'native-context')[0] for d in _PURE_PLAN['nativeContextDigests']]
      ==['native.context.syntax.v2'])
_PURE_INVENTORY=[r['path'] for r in PURE[1][PURE[0]['snapshotId']][1]['sourceInventory']]
check('a-grammar-only-repository-snapshot-has-no-compiler-unit-marker',
      not any(p.endswith(('Cargo.toml','tsconfig.json','package.json','jsconfig.json','Cargo.lock',
                          'package-lock.json')) for p in _PURE_INVENTORY))
check('a-grammar-only-repository-snapshot-is-entirely-bundled-grammar-files',
      _PURE_INVENTORY and all(N.BUNDLED_GRAMMARS.get('.'+p.rpartition('.')[2]) for p in _PURE_INVENTORY))
check('a-grammar-only-repository-carries-only-data-document-members',
      {N.BUNDLED_GRAMMARS['.'+p.rpartition('.')[2]] for p in _PURE_INVENTORY}
      =={'markdown','json','yaml','toml'})
check('a-grammar-only-repository-still-produces-its-inventory-fact',
      next(v for k,(d,v) in PURE[1].items() if d=='fact')['relation']=='file')
# The same repository shape, one code file added, exercises the code-grammar-without-a-compiler
# path: real syntax and clone facts under the grammar, with no Cargo and no tsconfig anywhere.
for _relation,_rung in [('declares','syntactic'),('clones','normalized-body-hash')]:
    _cr,_co,_cb=build(resolved=False,has_match=True,universe_language='syntax',relation=_relation,
                      source_path='src/lib.rs',pure_syntax=True)
    check('a-code-grammar-without-a-compiler-produces-'+_relation,
          M.close_run(_cr,_co,_cb).startswith('run2:'))
    _cf=next(v for k,(d,v) in _co.items() if d=='fact')
    check('a-code-grammar-without-a-compiler-carries-'+_relation+'-at-its-rung',
          _cf['relation']==_relation and _cf['resolution']==_rung)
    check('a-code-grammar-without-a-compiler-names-only-the-syntax-context.'+_relation,
          [M.parse_h_frame(_cb[d],'native-context')[0]
           for d in _co[_cr['planId']][1]['nativeContextDigests']]==['native.context.syntax.v2'])
# The mixed-repository file-inventory Runs are kept as their own, differently-scoped evidence.
for _path,_language in [('README.md','markdown'),('data/settings.json','json'),('config/app.yaml','yaml')]:
    _run,_objects,_blobs=build(resolved=False,has_match=True,universe_language='syntax',
                               relation='file',source_path=_path)
    check('data-document-grammar-run-closes.'+_language,
          M.close_run(_run,_objects,_blobs).startswith('run2:'))
    _fact=next(v for k,(d,v) in _objects.items() if d=='fact')
    check('data-document-grammar-run-carries-its-inventory-fact.'+_language,
          _fact['relation']=='file' and _fact['resolution']=='enumerated' and
          C.parse(_blobs[_fact['payloadDigest']])['path']==_path)
    check('data-document-grammar-run-is-under-the-syntax-universe.'+_language,
          M.parse_h_frame(_blobs[_fact['sourceUniverse']],'native-semantic-universe')[0]
          =='native.semantic-universe.syntax.v2')
    check('data-document-member-is-grammar-only-not-unsupported.'+_language,
          N.BUNDLED_GRAMMARS.get('.'+_path.rpartition('.')[2])==_language)
# ...and the control that keeps it honest: a data/document grammar cannot be promoted into the clone
# body-identity domain, in either direction.
check('a-data-document-language-is-not-a-clone-body-language',
      not {'json','toml','markdown','yaml'} &
      set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum']))
check('no-data-document-suffix-has-a-grammar-dialect-variant',
      not {s for s,l in N.BUNDLED_GRAMMARS.items() if l in ('json','toml','markdown','yaml')} &
      set(SYNTAX_ROW['languageVersionBinding']['dialect']['table']))
def grammar_class_case(mutate):
    context=copy.deepcopy(SYNTAX_FIXTURE_CONTEXT);mutate(context['grammarBundle'])
    return N.admit_native_context('syntax',context,SYNTAX_FIXTURE_CLOSURES)['refusals']
check('grammar-class-positive-control-admits',grammar_class_case(lambda b:None)==[])
# syntaxClass is registered, not chosen: the registry is the authority and both misdeclarations
# refuse, so a bundle cannot decide for itself what a language is capable of.
check('the-capability-registry-is-closed-over-exactly-the-bundled-languages',
      set(N.GRAMMAR_CAPABILITY_REGISTRY['languages'])==set(N.BUNDLED_GRAMMARS.values()))
check('the-registry-suffixes-are-exactly-the-bundled-suffixes',
      sorted(x for row in N.GRAMMAR_CAPABILITY_REGISTRY['languages'].values() for x in row['suffixes'])
      ==sorted(N.BUNDLED_GRAMMARS))
check('registered-code-languages-are-exactly-the-clone-body-languages',
      {l for l,row in N.GRAMMAR_CAPABILITY_REGISTRY['languages'].items() if row['syntaxClass']=='code'}
      ==set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum']))
check('no-registered-data-document-language-advertises-a-clone-or-code-capability',
      not any(cap.split('@')[0] in ('clones','declares','literal','control-flow')
              for l,row in N.GRAMMAR_CAPABILITY_REGISTRY['languages'].items()
              if row['syntaxClass']=='data-document' for cap in row['capabilities']))
check('every-registered-data-document-language-still-advertises-inventory',
      all('file@enumerated' in row['capabilities']
          for row in N.GRAMMAR_CAPABILITY_REGISTRY['languages'].values()
          if row['syntaxClass']=='data-document'))
check('a-grammar-row-declaring-an-unregistered-class-refuses',
      any(r.startswith('native.syntax-grammar-class-not-the-registered-one')
          for r in grammar_class_case(lambda b:next(
              g for g in b['grammars'] if g['languageId']=='markdown').update(syntaxClass='code'))))
# The registry is consulted FIRST, so a misdeclared class refuses as an unregistered class rather
# than as a body-enum disagreement. Both directions still refuse, which is the property that matters.
check('a-data-grammar-claiming-code-class-refuses',
      any(r.startswith('native.syntax-grammar-class-not-the-registered-one:yaml')
          for r in grammar_class_case(lambda b:next(
              g for g in b['grammars'] if g['languageId']=='yaml').update(syntaxClass='code'))))
check('a-code-grammar-demoted-to-data-class-refuses',
      any(r.startswith('native.syntax-grammar-class-not-the-registered-one:rust')
          for r in grammar_class_case(lambda b:next(
              g for g in b['grammars'] if g['languageId']=='rust').update(syntaxClass='data-document'))))
check('a-grammar-claiming-a-suffix-the-host-routes-elsewhere-refuses',
      any(r.startswith('native.syntax-grammar-suffix-not-bundled-for-language')
          for r in grammar_class_case(lambda b:next(
              g for g in b['grammars'] if g['languageId']=='rust').update(suffixes=['.py','.rs']))))
# Unknown grammar: `.py` is deliberately NOT bundled and must stay unsupported. Making the four
# bundled data grammars representable must not open the vocabulary to a language the host has no
# grammar for.
check('an-unbundled-language-is-not-representable-in-the-descriptor',
      'python' not in N.SCHEMAS['$defs']['SyntaxGrammarBundleV1']['properties']['grammars']
      ['items']['properties']['languageId']['enum'] and '.py' not in N.BUNDLED_GRAMMARS)
rejects('an-unbundled-language-grammar-row-refuses-schema-admission',
        lambda:N.validate_native('SyntaxGrammarBundleV1',
            {**copy.deepcopy(SYNTAX_FIXTURE_BUNDLE),
             'grammars':[dict(SYNTAX_FIXTURE_BUNDLE['grammars'][0],languageId='python',
                              suffixes=['.py'],syntaxClass='code')]}))
# Clones under the grammar: a .rs body read with NO Cargo, no edition and no ownership record - the
# exact case the compiler universes cannot represent.
syclone_run,syclone_objects,syclone_blobs=build(resolved=False,has_match=True,universe_language='syntax',relation='clones')
check('syntax-universe-clones-fact-closes-without-cargo-or-edition',
      M.close_run(syclone_run,syclone_objects,syclone_blobs).startswith('run2:'))
syclone_fact=next(v for k,(d,v) in syclone_objects.items() if d=='fact')
syclone_payload=C.parse(syclone_blobs[syclone_fact['payloadDigest']])
check('syntax-clone-body-identity-is-minted',syclone_payload is not None and
      syclone_payload['bodyIdentity'].startswith('sha256:'))
# The grammar-only dialect axis: a suffix variant, never an edition. A syntax-only body identity
# must NOT collide with a compiler-derived one over the same bytes, because a grammar parse and a
# compiler parse are different interpretations and equating them would be a false clone claim.
RUST_ROW=M.DIGESTS['domainSets']['native-semantic-universe']['native.semantic-universe.rust.v2']
check('syntax-dialect-axis-is-grammar-variant-not-edition',
      SYNTAX_ROW['languageVersionBinding']['dialect']['key']=='grammarVariant' and
      RUST_ROW['languageVersionBinding']['dialect']['key']=='edition')
check('syntax-dialect-table-covers-rust-and-tsjs-suffixes',
      set(SYNTAX_ROW['languageVersionBinding']['dialect']['table'])>= {'.rs','.ts','.js','.d.ts'})
check('syntax-body-languages-are-within-the-closed-language-id-enum',
      set(SYNTAX_ROW['languageVersionBinding']['bodyLanguages'])<=
      set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum']))
check('syntax-body-language-by-variant-covers-every-dialect-token',
      set(SYNTAX_ROW['languageVersionBinding']['bodyLanguageByVariant'])==
      set(SYNTAX_ROW['languageVersionBinding']['dialect']['table'].values()))
# The syntax universe must NOT widen semantic capability.
check('syntax-universe-language-mode-maps-to-syntax',
      M.DIGESTS['languageModes']['map']['syntax-only']=='syntax')
check('syntax-universe-binds-only-the-syntax-context-domain',
      SYNTAX_ROW['contextDomain']=='native.context.syntax.v2')

# Discriminating controls. A new registered universe is only safe if it refuses everything the two
# compiler universes refuse; each of these is a way the third domain could have opened a hole.
def syntax_admission_case(mutate_context=None,mutate_universe=None,context_arg='self',
                          admission_language=None):
    """Re-run the ACTUAL native syntax admission/binding over the fixture's own retained closure,
    with one thing changed. Returns the sorted refusal list (empty means ADMIT)."""
    objects,blobs={},{}
    def blob(value):return put_blob(blobs,value)
    def add(domain,**fields):
        value=dict(fields,schemaVersion=2);key=M.identifier(domain,value)
        objects[key]=(domain,value);return key
    def tree(files):return sorted(({'path':p,'sha256':blob(v),'bytes':len(v)} for p,v in files.items()),
                                  key=lambda r:r['path'].encode())
    base=syntax_inputs(objects,blobs,add,blob,tree)
    context=copy.deepcopy(base['context'])
    if mutate_context:mutate_context(context,base)
    admission=N.admit_native_context(admission_language or 'syntax',context,
                                     {k:v for k,(d,v) in objects.items() if d=='closure'})
    universe=copy.deepcopy(base['universe'])
    if mutate_universe:mutate_universe(universe,base,admission)
    passed=context if context_arg=='self' else (None if context_arg is None else context_arg)
    return N.bind_syntax_universe(universe,admission,passed,{},[])['refusals']
check('syntax-admission-positive-control-admits',syntax_admission_case()==[])
check('syntax-control-missing-context-refuses',
      'native.universe-context-not-supplied' in syntax_admission_case(context_arg=None))
check('syntax-control-context-bytes-not-the-admitted-ones-refuses',
      any(r.startswith('native.universe-context-binding-mismatch')
          for r in syntax_admission_case(
              mutate_universe=lambda u,b,a:u.update(nativeContextId='sha256:'+'e'*64))))
check('syntax-control-selection-naming-an-absent-grammar-refuses',
      'native.syntax-grammar-not-in-bundle:go.v1' in
      syntax_admission_case(mutate_universe=lambda u,b,a:u.update(selectedGrammarIds=sorted(u['selectedGrammarIds']+['go.v1']))))
check('syntax-control-parser-version-not-from-closure-manifest-refuses',
      'native.syntax-grammar-version-not-from-manifest' in
      syntax_admission_case(mutate_context=lambda c,b:c['grammarBundle'].update(parserVersion='9.9.9')))
check('syntax-control-grammar-not-in-retained-closure-refuses',
      any(r.startswith('native.syntax-grammar-not-in-closure')
          for r in syntax_admission_case(
              mutate_context=lambda c,b:c['grammarBundle']['grammars'][0].update(grammarDigest='b'*64))))
check('syntax-control-bundle-digest-not-in-retained-closure-refuses',
      'native.syntax-grammar-bundle-not-in-closure' in
      syntax_admission_case(mutate_context=lambda c,b:c['grammarBundle'].update(bundleDigest='c'*64)))
check('syntax-control-normalizer-spec-not-in-retained-closure-refuses',
      'native.syntax-normalizer-spec-not-in-closure' in
      syntax_admission_case(mutate_context=lambda c,b:c['grammarBundle']['normalizer'].update(specificationDigest='d'*64)))
check('syntax-control-unretained-grammar-closure-refuses',
      any(r.startswith('native.native-context-closure-unretained')
          for r in syntax_admission_case(
              mutate_context=lambda c,b:c['grammarBundle'].update(closureId='closure2:'+'f'*64))))
check('syntax-control-two-grammars-claiming-one-suffix-refuses',
      any(r.startswith('native.syntax-grammar-suffix-ambiguous')
          for r in syntax_admission_case(
              mutate_context=lambda c,b:c['grammarBundle']['grammars'][0].update(suffixes=['.rs','.ts']))))
check('syntax-control-wrong-context-language-refuses',
      any(r.startswith('native.native-context-language-mismatch')
          for r in syntax_admission_case(admission_language='typescript')))
# Cross-language: `declares` is universeRule same-only, so a fact that reads a body under the
# grammar and claims a TypeScript target universe must refuse. The grammar universe is not a
# universal donor.
def syntax_cross_universe():
    run,objects,blobs=build(resolved=False,has_match=True,universe_language='syntax',relation='declares')
    key=next(k for k,(d,v) in objects.items() if d=='fact');fact=copy.deepcopy(objects[key][1])
    other=next(v for k,(d,v) in objects.items() if d=='plan')
    ts_universe=M.native_universe_frame('native.semantic-universe.typescript.v2',
        M.parse_h_frame(blobs[next(v for k,(d,v) in objects.items() if d=='subject-scope')['sourceUniverse']],
                        'native-semantic-universe')[1] if False else
        copy.deepcopy(NATIVE_FIXTURES['tsUniverse']),blobs)
    fact.update(targetUniverse=ts_universe)
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    rekey(objects,scope_key,dict(objects[scope_key][1],targetUniverse=ts_universe),run)
    rekey(objects,key,fact,run);resync_coverage(objects,blobs,run,resolved=False);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
rejects('syntax-universe-cannot-be-mixed-with-a-compiler-universe-in-a-same-only-relation',
        syntax_cross_universe)
# A syntax universe record framed under a COMPILER universe domain is not the same object. The
# refusal is at CONSUMPTION, not at the retention helper: native_universe_frame only writes the
# frame ("a frame proves retention, never admission"), and parse_h_frame validates the payload
# against the domain row's own document and selector. Both halves are asserted so the layering is
# recorded rather than assumed.
SYNTAX_RECORD_UNDER_TS=M.native_universe_frame('native.semantic-universe.typescript.v2',
    {'schemaVersion':2,'nativeContextId':'sha256:'+'a'*64,'selectedGrammarIds':['typescript.v1'],
     'resolutionAttempted':False},(WRONG_DOMAIN_BLOBS:={}))
check('retention-helper-does-not-itself-admit-the-record',len(SYNTAX_RECORD_UNDER_TS)==64)
rejects_because('syntax-universe-record-refuses-under-the-typescript-universe-domain',
    lambda:M.parse_h_frame(WRONG_DOMAIN_BLOBS[SYNTAX_RECORD_UNDER_TS],'native-semantic-universe'),
    'H_FRAME_RECORD:native.semantic-universe.typescript.v2')
# ...and the converse: a TypeScript universe record does not pass as a syntax one either.
TS_RECORD_UNDER_SYNTAX=M.native_universe_frame('native.semantic-universe.syntax.v2',
    copy.deepcopy(NATIVE_FIXTURES['tsUniverse']),(WRONG_DOMAIN_BLOBS2:={}))
rejects_because('typescript-universe-record-refuses-under-the-syntax-universe-domain',
    lambda:M.parse_h_frame(WRONG_DOMAIN_BLOBS2[TS_RECORD_UNDER_SYNTAX],'native-semantic-universe'),
    'H_FRAME_RECORD:native.semantic-universe.syntax.v2')
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
    retained={'dependencySourceSet':parts['dependency'],'unifiedFeatures':parts['features'],
              'sourceUnitOwnership':parts['ownership']}
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

# --- v8-S2: a relation payload's claim about the snapshot is joined to the snapshot --------------
# The reviewer's finding was exact: a `file` payload's path, contentSha256 and byteLength were
# covered by no digest law and joined to nothing, so a fabricated file fact was schema-valid and
# admissible. The remedy is a per-relation snapshot-join registry ENFORCED at Run closure over the
# OWNING FACT's snapshot and retained bytes, plus the whole annotated field class, not one field.
FILE_RUN=build(resolved=True,has_match=True,relation='file')
store=M.EvidenceStore();eid='exec1_'+'b'*32
check('file-shaped-run-prepares',store.prepare(*FILE_RUN,eid,replay)==M.identifier('run',FILE_RUN[0]))
check('file-shaped-run-commits',store.commit(eid)=='committed')
check('file-shaped-run-seals-a-pass-verdict',
      FILE_RUN[1][FILE_RUN[0]['evaluationSealId']][1]['verdict']=='pass')
check('file-at-enumerated-is-a-not-applicable-rung-under-rc-1',
      (lambda p:p['entry']['resolutionCompleteness']['state']=='not-applicable' and
                p['entry']['resolutionCompleteness']['unresolvedEdgeCount']==0 and
                p['entry']['coverage']=='complete')
      (C.parse(FILE_RUN[2][next(v['payloadDigest'] for k,(d,v) in FILE_RUN[1].items() if d=='coverage')])))
CLONE_RUN=build(resolved=True,has_match=True,relation='clones')
store=M.EvidenceStore();eid='exec1_'+'c'*32
check('clone-shaped-run-prepares',store.prepare(*CLONE_RUN,eid,replay)==M.identifier('run',CLONE_RUN[0]))
check('clone-shaped-run-commits',store.commit(eid)=='committed')

def file_fact_mutation(mutate,relation='file',universe_language='typescript'):
    """Mutate the OWNING FACT and/or its payload, then re-close. Every control here changes real
    reachable bytes: the payload digest moves, so the fact identity moves, so the view, witness,
    proof and seal are re-minted. A no-op mutation would not be a bypass and is not claimed as one -
    the positive control below re-closes the same harness unchanged."""
    run,objects,blobs=build(resolved=True,has_match=True,relation=relation,universe_language=universe_language)
    key=next(k for k,(d,v) in objects.items() if d=='fact');fact=copy.deepcopy(objects[key][1])
    payload=C.parse(blobs[fact['payloadDigest']]);before=fact['payloadDigest']
    mutate(fact,payload,blobs,objects,run)
    fact['payloadDigest']=put_blob(blobs,payload)
    moved=fact['payloadDigest']!=before or C.canonical(fact)!=C.canonical(objects[key][1])
    if not moved:raise AssertionError('FIXTURE_NO_OP_MUTATION')
    rekey(objects,key,fact,run)
    if M.identifier('fact',fact)==key:raise AssertionError('FIXTURE_OWNING_IDENTITY_UNCHANGED')
    resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)

check('file-join-harness-positive-control-closes',
      file_fact_mutation(lambda f,p,b,o,r:f.update(confidenceMillionths=999999)).startswith('run2:'))
# The v8 case exactly: the fact is anchored in a REAL inventoried file, and its payload claims a
# file that does not exist. Before this join it closed; the anchors were never the claim.
rejects_because('a-fabricated-file-path-is-not-in-the-owning-snapshot-inventory',
    lambda:file_fact_mutation(lambda f,p,b,o,r:p.update(path='invented/not-in-snapshot.ts')),
    'RELATION_PATH_NOT_INVENTORIED:file:invented/not-in-snapshot.ts')
rejects_because('a-file-payload-content-hash-must-be-the-inventory-rows-hash',
    lambda:file_fact_mutation(lambda f,p,b,o,r:p.update(contentSha256=put_blob(b,b'other bytes entirely\n'))),
    'RELATION_FILE_CONTENT_JOIN')
rejects_because('a-file-payload-byte-length-must-be-the-inventory-rows-length',
    lambda:file_fact_mutation(lambda f,p,b,o,r:p.update(byteLength=p['byteLength']+1)),
    'RELATION_FILE_LENGTH_JOIN')
def file_claim_over_a_foreign_snapshot():
    """The claimed path and digest are real - in ANOTHER project's snapshot. The owning fact names
    this Run's snapshot, and that inventory is the only one its claim is judged against."""
    foreign=build(resolved=True,has_match=True,source_path='foreign/only-here.ts')
    foreign_row=next(r for r in foreign[1][foreign[0]['snapshotId']][1]['sourceInventory']
                     if r['path']=='foreign/only-here.ts')
    def mutate(f,p,b,o,r):
        b[foreign_row['sha256']]=foreign[2][foreign_row['sha256']]
        p.update(path=foreign_row['path'],contentSha256=foreign_row['sha256'],byteLength=foreign_row['bytes'])
    return file_fact_mutation(mutate)
rejects_because('a-file-claim-over-a-foreign-snapshots-path-refuses',file_claim_over_a_foreign_snapshot,
                'RELATION_PATH_NOT_INVENTORIED:file:foreign/only-here.ts')
def file_bytes_not_retained():
    """The inventory row agrees with the claim, but the bytes themselves are gone. An inventory row
    is a claim ABOUT bytes; a Run that cannot produce them has not closed over them."""
    run,objects,blobs=build(resolved=True,has_match=True,relation='file')
    payload=C.parse(blobs[next(v['payloadDigest'] for k,(d,v) in objects.items() if d=='fact')])
    del blobs[payload['contentSha256']]
    return M.close_run(run,objects,blobs)
def file_bytes_retention_class():
    try:file_bytes_not_retained()
    except M.EvidenceUnavailable:return 'retention'
    except C.AdmissionError:return 'refusal'
    return 'closed'
check('a-file-claim-whose-bytes-are-not-retained-is-custody-loss-not-a-false-claim',
      file_bytes_retention_class()=='retention')
def second_owner_borrows_a_file_payload():
    """The v8 second-owner case. The SAME admissible file payload under a second fact whose anchor
    lies in another file: the payload is untouched and still schema-valid, and the borrowed anchor
    cannot make its claim true. This is why the closure - not a payload-only helper - decides."""
    run,objects,blobs=build(resolved=True,has_match=True,relation='file')
    key=next(k for k,(d,v) in objects.items() if d=='fact');fact=copy.deepcopy(objects[key][1])
    other=copy.deepcopy(fact)
    row=next(r for r in objects[run['snapshotId']][1]['sourceInventory'] if r['path']=='tsconfig.json')
    other['anchors']=[{'path':row['path'],'blobDigest':row['sha256'],'startByte':0,'endByte':row['bytes']}]
    if other['payloadDigest']!=fact['payloadDigest']:raise AssertionError('FIXTURE_PAYLOAD_NOT_SHARED')
    other_key=M.identifier('fact',other)
    if other_key==key:raise AssertionError('FIXTURE_OWNING_IDENTITY_UNCHANGED')
    objects[other_key]=('fact',other)
    view_key=next(k for k,(d,v) in objects.items() if d=='view');view=copy.deepcopy(objects[view_key][1])
    view['facts']=sorted(set(view['facts']+[other_key]),key=C.canonical)
    rekey(objects,view_key,view,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
rejects_because('a-shared-file-payload-cannot-borrow-a-second-owners-anchor',
    second_owner_borrows_a_file_payload,'RELATION_ANCHOR_FOREIGN_PATH:tsconfig.json')
# The clone body identity: the INHERITED framed recipe, joined component by component.
check('clone-harness-positive-control-closes',
      file_fact_mutation(lambda f,p,b,o,r:f.update(confidenceMillionths=999999),relation='clones').startswith('run2:'))
def clone_mutation(mutate):return file_fact_mutation(mutate,relation='clones')
def reframed(payload,blobs,level=None,version=None,language=None,language_version=None,body=None):
    """Rebuild the retained body frame from its own retained components, changing exactly one.
    Decomposing the real frame keeps each negative pointed at ONE component instead of at a
    wholesale substitution that could refuse anywhere."""
    frame=blobs[payload['bodyIdentity'].removeprefix('sha256:')]
    was=M.parse_body_frame(frame)
    return 'sha256:'+put_blob(blobs,framed_body_preimage(
        was[1].decode() if level is None else level,
        was[2] if version is None else version,
        was[3].decode() if language is None else language,
        was[4] if language_version is None else language_version,
        was[5] if body is None else body))
rejects_because('a-clone-body-identity-must-be-the-retained-framed-preimages-hash',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity='sha256:'+put_blob(b,b'not a frame'))),
    'BODY_FRAME_TRUNCATED')
rejects_because('a-body-frame-carrying-hex-text-instead-of-the-raw-level-digest-refuses',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(
        bodyIdentity=reframed(p,b,version=p['normalisationVersion'].encode('ascii')))),
    'BODY_IDENTITY_LEVEL_VERSION_JOIN')
rejects_because('a-body-frame-must-name-the-owning-facts-own-language',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,language='rust'))),
    'BODY_IDENTITY_LANGUAGE_JOIN')
rejects_because('a-body-frame-must-carry-the-derived-language-version-and-not-a-raw-config-map',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(
        bodyIdentity=reframed(p,b,language_version=C.canonical({'languageMode':'ts-tsconfig','synthesizerVersion':'0.0.0'})))),
    'BODY_IDENTITY_LANGUAGE_VERSION_JOIN')
rejects_because('a-body-frames-level-must-be-the-payloads-own-level',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,level='L1-lexical'))),
    'BODY_IDENTITY_LEVEL_JOIN')
rejects_because('an-l0-body-payload-must-be-the-owning-facts-own-anchor-span',
    lambda:clone_mutation(lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,
        body=(lambda x:len(x).to_bytes(4,'big')+x)(b'export const foo = 2;\n')))),
    'BODY_IDENTITY_BODY_SPAN')
def unretained_level_specification():
    return clone_mutation(lambda f,p,b,o,r:p.update(
        normalisationVersion=hashlib.sha256(b'a level specification nobody retained').hexdigest()))
check('a-normalisation-version-must-name-retained-level-specification-bytes',
      not_admitted(unretained_level_specification))
rejects_because('a-clone-fact-carries-exactly-one-anchor',
    lambda:clone_mutation(lambda f,p,b,o,r:f.__setitem__('anchors',sorted(
        f['anchors']+[dict(f['anchors'][0],endByte=f['anchors'][0]['endByte']-1)],key=C.canonical))),
    'BODY_IDENTITY_ANCHOR_CARDINALITY')
# package and vcs-change: the other two relations that name a snapshot path, and the two
# EXEMPTIONS, which must be exercised positively or an over-strict join would silently refuse
# every honest delete and rename.
for shaped in ('package','vcs-change'):
    graph=build(resolved=True,has_match=True,relation=shaped)
    store=M.EvidenceStore();eid='exec1_'+('d' if shaped=='package' else 'e')*32
    check(shaped+'-shaped-run-prepares',store.prepare(*graph,eid,replay)==M.identifier('run',graph[0]))
    check(shaped+'-shaped-run-commits',store.commit(eid)=='committed')
rejects_because('a-package-manifest-path-must-be-in-the-owning-snapshot-inventory',
    lambda:file_fact_mutation(lambda f,p,b,o,r:p.update(manifestPath='node_modules/ghost/package.json'),relation='package'),
    'RELATION_PATH_NOT_INVENTORIED:package:node_modules/ghost/package.json')
rejects_because('a-vcs-change-path-must-be-in-the-owning-snapshot-inventory',
    lambda:file_fact_mutation(lambda f,p,b,o,r:p.update(path='never/existed.ts'),relation='vcs-change'),
    'RELATION_PATH_NOT_INVENTORIED:vcs-change:never/existed.ts')
check('a-deleted-path-is-absent-from-the-analysed-snapshot-and-still-closes',
      file_fact_mutation(lambda f,p,b,o,r:p.update(path='was/here.ts',changeKind='deleted'),
                         relation='vcs-change').startswith('run2:'))
check('a-pre-rename-path-is-a-historical-observation-and-is-not-joined',
      file_fact_mutation(lambda f,p,b,o,r:p.update(changeKind='renamed',previousPath='before/rename.ts'),
                         relation='vcs-change').startswith('run2:'))
# --- v5, root concerns 1 and 2: the body language version is the COMPILER identity, derived and
# --- bounded, and it is the same law for both languages ------------------------------------------
# Concern 1: my v4 binding used TypeScript's languageMode+synthesizerVersion (option synthesis, not
# the language) and Rust's whole per-crate edition map, and claimed Rust carried no toolchain
# identity. It does: the universe's own nativeContextId reaches the admitted retained context, whose
# toolchain has rustcVersion/rustCommitHash and compilerVersion/compilerPackageDigest. Withdrawn.
# Concern 2: C({edition: map}) is unbounded and exceeded the inherited u8 component maximum for an
# ordinary workspace. The component is now the RAW 32 digest bytes of a closed derived projection.
UNIVERSE_ROW={'typescript':M.DIGESTS['domainSets']['native-semantic-universe']['native.semantic-universe.typescript.v2'],
              'rust':M.DIGESTS['domainSets']['native-semantic-universe']['native.semantic-universe.rust.v2']}
BINDING={l:UNIVERSE_ROW[l]['languageVersionBinding'] for l in ('typescript','rust')}
def universe_and_context(fact,blobs):
    universe=M.parse_h_frame(blobs[fact['sourceUniverse']],'native-semantic-universe')[1]
    return universe,M.parse_h_frame(blobs[universe['nativeContextId'].removeprefix('sha256:')],'native-context')[1]
def projection_inputs(fact,blobs,language):
    """Everything the derived projection reads: the universe, its admitted context, the body's OWN
    anchor, and the retained ownership record the universe commits when it commits one."""
    universe,context=universe_and_context(fact,blobs)
    retained=None
    owner=universe.get('sourceUnitOwnershipId')
    if owner:retained={'sourceUnitOwnership':M.parse_h_frame(blobs[owner.removeprefix('sha256:')],'native-nested')[1]}
    return universe,context,UNIVERSE_ROW[language],fact['anchors'][0],retained
def restated_language_version(fact,blobs,language,**overrides):
    record=body_language_version(*projection_inputs(fact,blobs,language))
    record.update(overrides)
    return hashlib.sha256(C.canonical(record)).digest()

# Both languages close a COMPLETE clone Run through closure, replay and commit. The Rust branch is a
# whole Run, not a helper assertion.
CLONE_RUNS={}
for language in ('typescript','rust'):
    CLONE_RUNS[language]=build(resolved=True,has_match=True,relation='clones',universe_language=language)
    store=M.EvidenceStore();eid='exec1_'+('7' if language=='rust' else '6')*32
    check(language+'-clone-run-prepares',store.prepare(*CLONE_RUNS[language],eid,replay)==M.identifier('run',CLONE_RUNS[language][0]))
    check(language+'-clone-run-commits',store.commit(eid)=='committed')
def clone_frame_of(graph):
    run,objects,blobs=graph
    fact=next(v for k,(d,v) in objects.items() if d=='fact')
    payload=C.parse(blobs[fact['payloadDigest']])
    return fact,payload,M.parse_body_frame(blobs[payload['bodyIdentity'].removeprefix('sha256:')])
for language in ('typescript','rust'):
    _fact,_payload,_parts=clone_frame_of(CLONE_RUNS[language])
    check(language+'-body-language-version-component-is-32-raw-bytes',len(_parts[4])==32)
    check(language+'-body-frame-component-lengths-fit-the-inherited-u8-prefix',
          all(len(part)<=255 for part in _parts[:5]))
    check(language+'-body-language-version-is-the-compiler-identity-not-config',
          (lambda record:record['compilerVersion'] in ('5.6.3','1.83.0') and
                         record['compilerName'] in ('typescript','rustc') and
                         'languageMode' not in record and 'synthesizerVersion' not in record and
                         (record['dialect']=={'edition':2021} if language=='rust'
                          else record['dialect']=={'sourceVariant':'ts'}))
          (body_language_version(*projection_inputs(_fact,CLONE_RUNS[language][2],language))))
# raw C, raw SHA-256 and H are three different things and none may stand in for another.
_fact,_payload,_parts=clone_frame_of(CLONE_RUNS['rust'])
_universe,_context=universe_and_context(_fact,CLONE_RUNS['rust'][2])
_record=body_language_version(*projection_inputs(_fact,CLONE_RUNS['rust'][2],'rust'))
check('body-language-version-component-is-raw-sha256-of-C-not-C-itself',
      _parts[4]==hashlib.sha256(C.canonical(_record)).digest() and _parts[4]!=C.canonical(_record)[:32])
check('body-language-version-component-is-not-an-H-identity',
      _parts[4].hex()!=C.identity('native.semantic-universe.rust.v2',_record) and
      _parts[4]!=bytes.fromhex(C.identity('native.semantic-universe.rust.v2',_record)))
check('body-language-version-raw-bytes-are-not-the-hex-text',
      _parts[4]!=hashlib.sha256(C.canonical(_record)).hexdigest().encode('ascii') and
      len(hashlib.sha256(C.canonical(_record)).hexdigest().encode('ascii'))==64)

# An actual version or dialect change must move the component; a stale body identity is refused.
def clone_mutation_in(language,mutate):return file_fact_mutation(mutate,relation='clones',universe_language=language)
# The control for the negatives below: an INDEPENDENT restatement of the projection reproduces the
# component byte for byte, so each refusal underneath is caused by its one overridden field and not
# by the act of rebuilding the frame. (Restating it unchanged is deliberately not run as a Run
# mutation: it would be a no-op, and the harness refuses to call a no-op a bypass.)
for language in ('typescript','rust'):
    _f,_p,_parts=clone_frame_of(CLONE_RUNS[language])
    check('restating-the-'+language+'-projection-reproduces-the-identical-component',
          restated_language_version(_f,CLONE_RUNS[language][2],language)==_parts[4])
for language,field,value in [('rust','compilerVersion','9.9.9'),('rust','compilerBuild','f'*40),
                             ('rust','compilerName','not-rustc'),
                             ('typescript','compilerVersion','9.9.9'),('typescript','compilerBuild','e'*64)]:
    rejects_because('a-changed-'+field+'-invalidates-a-stale-'+language+'-body-identity',
        lambda language=language,field=field,value=value:clone_mutation_in(language,
            lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,
                language_version=restated_language_version(f,b,language,**{field:value})))),
        'BODY_IDENTITY_LANGUAGE_VERSION_JOIN')
rejects_because('a-changed-rust-dialect-invalidates-a-stale-body-identity',
    lambda:clone_mutation_in('rust',lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,
        language_version=restated_language_version(f,b,'rust',dialect={'edition':2015})))),
    'BODY_IDENTITY_LANGUAGE_VERSION_JOIN')

def clone_run_with_universe(mutate_universe,language='rust',mutate_ownership=None,source_path=None,workspace=None):
    """Re-frame the universe of a complete clone Run and re-key everything that names it, so a
    universe change is exercised through an actual Run rather than through a helper call."""
    run,objects,blobs=build(resolved=True,has_match=True,relation='clones',universe_language=language,
                            source_path=source_path,workspace=workspace)
    fact_key=next(k for k,(d,v) in objects.items() if d=='fact')
    universe=M.parse_h_frame(blobs[objects[fact_key][1]['sourceUniverse']],'native-semantic-universe')[1]
    if mutate_ownership is not None:
        # The body identity was minted under the ownership the universe committed at build time.
        # Re-frame ONLY that record and re-point the universe at it: the frame is now stale, and the
        # closure has to say so. The fixture builder is deliberately not re-run.
        owned=M.parse_h_frame(blobs[universe['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')[1]
        mutate_ownership(owned)
        owned['ownership']=sorted(owned['ownership'],key=lambda r:(r['path'].encode(),r['unitId'].encode()))
        owned['units']=sorted(owned['units'],key=lambda u:u['unitId'].encode())
        owned['selectedUnitIds']=sorted(owned['selectedUnitIds'],key=lambda x:x.encode())
        universe['sourceUnitOwnershipId']='sha256:'+M.retain_h_identity(N.SOURCE_UNIT_OWNERSHIP_DOMAIN,owned,blobs)
    mutate_universe(universe)
    new=M.retain_h_identity('native.semantic-universe.'+language+'.v2',universe,blobs)
    scope_key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    rekey(objects,scope_key,dict(objects[scope_key][1],sourceUniverse=new,targetUniverse=new),run)
    rekey(objects,fact_key,dict(objects[fact_key][1],sourceUniverse=new,targetUniverse=new),run)
    resync_coverage(objects,blobs,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs),C.parse(blobs[next(v['payloadDigest'] for k,(d,v) in objects.items() if d=='fact')])
check('universe-reframe-harness-positive-control-closes',
      clone_run_with_universe(lambda u:None)[0].startswith('run2:'))
# ROOT'S EXACT VECTOR: 21 schema-admitted edition entries. C({edition: map}) is 723 bytes, past the
# inherited u8 maximum of 255; the derived component is 32 bytes and the Run closes.
LARGE_EDITION={'fixture-root':2021,**{'ordinary_workspace_crate_%d'%i:2021 for i in range(20)}}
check('root-vector-raw-edition-map-would-exceed-the-inherited-u8-component',
      len(LARGE_EDITION)==21 and len(C.canonical({'edition':LARGE_EDITION}))==723>255)
LARGE_RUN,LARGE_PAYLOAD=clone_run_with_universe(lambda u:u.update(edition=dict(LARGE_EDITION)))
check('a-large-single-edition-workspace-yields-a-bounded-component-and-closes',
      LARGE_RUN.startswith('run2:'))
LARGE_FRAME=CLONE_RUNS['rust'][2][LARGE_PAYLOAD['bodyIdentity'].removeprefix('sha256:')]
check('the-large-workspace-component-is-still-32-raw-bytes',
      len(M.parse_body_frame(LARGE_FRAME)[4])==32 and
      all(len(part)<=255 for part in M.parse_body_frame(LARGE_FRAME)[:5]))
# No leak: renaming crates changes the universe identity and must NOT change the body identity.
BASE_PAYLOAD=clone_frame_of(CLONE_RUNS['rust'])[1]
check('unrelated-crate-names-do-not-leak-into-a-body-language-version',
      LARGE_PAYLOAD['bodyIdentity']==BASE_PAYLOAD['bodyIdentity'])
# Renaming the owning crate CONSISTENTLY - in the edition map and in the ownership relation - leaves
# the effective edition untouched, so the body identity must be byte identical. Renaming it in only
# one of the two is an inconsistent universe and is refused below.
RENAMED_RUN,RENAMED_PAYLOAD=clone_run_with_universe(
    lambda u:u.update(edition={'renamed-crate':2021}),
    mutate_ownership=lambda o:[u.update(crateName='renamed-crate') for u in o['units']])
check('renaming-the-owning-crate-does-not-change-the-body-identity',
      RENAMED_RUN.startswith('run2:') and RENAMED_PAYLOAD['bodyIdentity']==BASE_PAYLOAD['bodyIdentity'])
rejects_because('renaming-the-crate-in-only-one-of-the-two-committed-places-refuses',
    lambda:clone_run_with_universe(lambda u:u.update(edition={'renamed-crate':2021}))[0],
    'BODY_LANGUAGE_OWNER_AMBIGUOUS:unknown-crate:fixture-root')
# An operational TARGET CONFIGURATION change: a real, lawful universe difference that must not
# reach a body language version. (A crateRootPaths change is not usable as a control here: the
# universe's own snapshot join already refuses an uninventoried crate root, which is correct.)
NOISE_RUN,NOISE_PAYLOAD=clone_run_with_universe(lambda u:u.update(cfgSets=sorted(
    u['cfgSets']+[{'cfgSetId':'primary+bench','cfg':sorted(u['cfgSets'][0]['cfg']+['bench'])}],
    key=lambda row:C.canonical(row))))
check('operational-target-configuration-does-not-leak-into-a-body-language-version',
      NOISE_RUN.startswith('run2:') and NOISE_PAYLOAD['bodyIdentity']==BASE_PAYLOAD['bodyIdentity'])
# Mixed editions: the owning crate decides and nothing committed joins an anchor path to a crate
# name, so this REFUSES. It does not guess a module layout.
rejects_because('a-universe-that-commits-no-ownership-admits-no-clone-whatever-its-package-map',
    lambda:clone_run_with_universe(lambda u:u.update(sourceUnitOwnershipId=None)),
    'BODY_LANGUAGE_OWNERSHIP_REQUIRED:1')
rejects_because('a-rust-universe-with-no-edition-refuses-rather-than-defaulting',
    lambda:clone_run_with_universe(lambda u:u.update(edition={})),
    'BODY_LANGUAGE_DIALECT_ABSENT:rust')

# --- root's v5 requirement: an ORDINARY mixed-edition workspace has a representable valid form ----
# Each body is dialected by the compilation unit that owns its path, so bodies of BOTH editions
# close in the SAME universe. The relation is committed, not inferred: a crate-name-to-root map
# cannot resolve #[path], shared files or several compilation contexts of one crate.
MIXED_WORKSPACE={'edition':{'fixture-root':2021,'legacy-crate':2015},
  'enumeration':'complete',
  'units':[unit('Cargo.toml','lib','fixture-root','fixture-root'),
           unit('Cargo.toml','test','root-it','fixture-root'),
           unit('vendor/fixture-dep/Cargo.toml','lib','legacy-crate','legacy-crate')],
  'selectedUnitIds':[UID('Cargo.toml','lib','fixture-root'),UID('Cargo.toml','test','root-it'),
                     UID('vendor/fixture-dep/Cargo.toml','lib','legacy-crate')],
  'ownership':[{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')},
               {'path':'src/lib.rs','unitId':UID('Cargo.toml','test','root-it')},
               {'path':'vendor/fixture-dep/src/lib.rs','unitId':UID('vendor/fixture-dep/Cargo.toml','lib','legacy-crate')}]}
MIXED_RUNS={}
for _path,_expected in [('src/lib.rs',2021),('vendor/fixture-dep/src/lib.rs',2015)]:
    graph=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
                workspace=MIXED_WORKSPACE,source_path=_path)
    MIXED_RUNS[_path]=graph
    store=M.EvidenceStore();eid='exec1_'+('8' if _expected==2021 else '9')*32
    check('mixed-edition-workspace-body-at-%d-prepares'%_expected,
          store.prepare(*graph,eid,replay)==M.identifier('run',graph[0]))
    check('mixed-edition-workspace-body-at-%d-commits'%_expected,store.commit(eid)=='committed')
    _f,_p,_parts=clone_frame_of(graph)
    check('mixed-edition-body-at-%d-takes-its-owning-units-dialect'%_expected,
          body_language_version(*projection_inputs(_f,graph[2],'rust'))['dialect']=={'edition':_expected})
# --- root v5 addendum: the actual TARGET edition, not merely the package default -----------------
# Cargo documents a per-target edition defaulting to package.edition, so a package map whose values
# all agree can still contain a target that does not. Same package, two targets, two editions.
TARGET_OVERRIDE_WORKSPACE={'edition':{'fixture-root':2021},'enumeration':'complete',
  'units':[unit('Cargo.toml','lib','fixture-root','fixture-root'),
           unit('Cargo.toml','bin','legacy','fixture-root',2015)],
  'selectedUnitIds':[UID('Cargo.toml','bin','legacy'),UID('Cargo.toml','lib','fixture-root')],
  'ownership':[{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')},
               {'path':'vendor/fixture-dep/src/lib.rs','unitId':UID('Cargo.toml','bin','legacy')}]}
check('the-package-map-alone-would-not-distinguish-these-two-bodies',
      len(set(TARGET_OVERRIDE_WORKSPACE['edition'].values()))==1)
TARGET_RUNS={}
for _path,_expected in [('src/lib.rs',2021),('vendor/fixture-dep/src/lib.rs',2015)]:
    graph=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
                workspace=TARGET_OVERRIDE_WORKSPACE,source_path=_path)
    TARGET_RUNS[_path]=graph
    store=M.EvidenceStore();eid='exec1_'+('a' if _expected==2021 else 'b')*32
    check('same-package-target-at-%d-prepares'%_expected,
          store.prepare(*graph,eid,replay)==M.identifier('run',graph[0]))
    check('same-package-target-at-%d-commits'%_expected,store.commit(eid)=='committed')
    _f,_p,_parts=clone_frame_of(graph)
    check('a-target-edition-overrides-its-package-default-at-%d'%_expected,
          body_language_version(*projection_inputs(_f,graph[2],'rust'))['dialect']=={'edition':_expected})
check('a-target-override-and-a-package-default-body-do-not-share-an-identity',
      clone_frame_of(TARGET_RUNS['src/lib.rs'])[1]['bodyIdentity']!=
      clone_frame_of(TARGET_RUNS['vendor/fixture-dep/src/lib.rs'])[1]['bodyIdentity'])
def target_override_stale(mutate,source_path='vendor/fixture-dep/src/lib.rs'):
    return clone_run_with_universe(lambda u:None,mutate_ownership=mutate,
        source_path=source_path,workspace=TARGET_OVERRIDE_WORKSPACE)[0]
check('target-override-harness-positive-control-closes',
      target_override_stale(lambda o:None).startswith('run2:'))
rejects_because('withdrawing-a-target-edition-override-invalidates-the-body-identity',
    lambda:target_override_stale(lambda o:[u.update(targetEdition=None) for u in o['units']
                                           if u['unitId']==UID('Cargo.toml','bin','legacy')]),
    'BODY_IDENTITY_LANGUAGE_VERSION_JOIN')
rejects_because('two-selected-targets-of-one-package-disagreeing-over-one-path-refuse',
    lambda:target_override_stale(lambda o:(
        o['units'].append(unit('Cargo.toml','bin','modern','fixture-root',2024)),
        o['selectedUnitIds'].append(UID('Cargo.toml','bin','modern')),
        o['ownership'].append({'path':'vendor/fixture-dep/src/lib.rs','unitId':UID('Cargo.toml','bin','modern')}))),
    'BODY_LANGUAGE_OWNER_AMBIGUOUS:vendor/fixture-dep/src/lib.rs:2')

# --- v6, root's required representation decision: ONE physical path, TWO editions ---------------
# The same physical src/lib.rs is compiled by a 2021 lib target and a 2015 bin target of the same
# package. Each explicitly SELECTED unit is a valid analysis of that body, with its own dialect and
# its own body identity. Because selectedUnitIds is committed inside the ownership record whose H
# identity the universe names, the two selections are two DIFFERENT sourceUniverse values - not two
# readings of one - and no relation payload changed to make that so.
SHARED_UNITS=[unit('Cargo.toml','lib','fixture-root','fixture-root'),
              unit('Cargo.toml','bin','legacy','fixture-root',2015)]
SHARED_ROWS=[{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')},
             {'path':'src/lib.rs','unitId':UID('Cargo.toml','bin','legacy')}]
def shared_workspace(selected,enumeration='complete',units=None,rows=None):
    return {'edition':{'fixture-root':2021},'enumeration':enumeration,
            'units':copy.deepcopy(units if units is not None else SHARED_UNITS),
            'selectedUnitIds':list(selected),
            'ownership':copy.deepcopy(rows if rows is not None else SHARED_ROWS)}
SHARED_RUNS={}
for _unit,_expected,_slot in [(UID('Cargo.toml','lib','fixture-root'),2021,'1'),(UID('Cargo.toml','bin','legacy'),2015,'2')]:
    graph=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
                source_path='src/lib.rs',workspace=shared_workspace([_unit]))
    SHARED_RUNS[_unit]=graph
    store=M.EvidenceStore();eid='exec1_'+(_slot*32)
    check('shared-path-under-selected-%s-prepares'%_expected,
          store.prepare(*graph,eid,replay)==M.identifier('run',graph[0]))
    check('shared-path-under-selected-%s-commits'%_expected,store.commit(eid)=='committed')
    _f,_p,_parts=clone_frame_of(graph)
    check('shared-path-under-selected-%s-takes-that-targets-dialect'%_expected,
          body_language_version(*projection_inputs(_f,graph[2],'rust'))['dialect']=={'edition':_expected})
    check('shared-path-under-selected-%s-anchors-the-shared-path'%_expected,
          _f['anchors'][0]['path']=='src/lib.rs')
_lib,_bin=SHARED_RUNS[UID('Cargo.toml','lib','fixture-root')],SHARED_RUNS[UID('Cargo.toml','bin','legacy')]
check('one-physical-body-under-two-selections-has-two-distinct-correct-identities',
      clone_frame_of(_lib)[1]['bodyIdentity']!=clone_frame_of(_bin)[1]['bodyIdentity'] and
      clone_frame_of(_lib)[0]['anchors']==clone_frame_of(_bin)[0]['anchors'] and
      _lib[2][clone_frame_of(_lib)[0]['anchors'][0]['blobDigest']]
      ==_bin[2][clone_frame_of(_bin)[0]['anchors'][0]['blobDigest']])
check('each-selection-is-a-different-source-universe',
      clone_frame_of(_lib)[0]['sourceUniverse']!=clone_frame_of(_bin)[0]['sourceUniverse'])
check('and-neither-clone-payload-field-set-changed',
      set(C.parse(_lib[2][clone_frame_of(_lib)[0]['payloadDigest']]))==
      {'bodyIdentity','normalisationLevel','normalisationVersion'})
# The three refusals below are judged at CLOSURE over an already-minted body identity: each starts
# from the valid lib-selected Run and re-frames only the committed ownership record. (The fixture
# builder refuses these inputs too, with its own FIXTURE_* causes, because an honest producer cannot
# mint a frame for a body it has no dialect for; that is not the interesting direction.)
def shared_selection_stale(mutate):
    return clone_run_with_universe(lambda u:None,mutate_ownership=mutate,source_path='src/lib.rs',
                                   workspace=shared_workspace([UID('Cargo.toml','lib','fixture-root')]))[0]
check('shared-selection-harness-positive-control-closes',
      shared_selection_stale(lambda o:None).startswith('run2:'))
rejects_because('selecting-both-conflicting-targets-of-a-shared-path-refuses',
    lambda:shared_selection_stale(lambda o:o['selectedUnitIds'].append(UID('Cargo.toml','bin','legacy'))),
    'BODY_LANGUAGE_OWNER_AMBIGUOUS:src/lib.rs:2')
rejects_because('a-path-owned-only-by-an-unselected-target-refuses-rather-than-borrowing-its-edition',
    lambda:shared_selection_stale(lambda o:(o.__setitem__('selectedUnitIds',[UID('Cargo.toml','bin','legacy')]),
        o.__setitem__('ownership',[r for r in o['ownership'] if r['unitId']!=UID('Cargo.toml','bin','legacy')]))),
    'BODY_LANGUAGE_OWNER_NOT_SELECTED:src/lib.rs')
# SELECTED SCOPE is not INCOMPLETE ENUMERATION. Partial discovery is refused BEFORE any row is read,
# so it can never hide a conflicting owner and thereby act as an implicit edition selection.
rejects_because('partial-enumeration-admits-no-dialect-even-with-a-valid-selected-row',
    lambda:shared_selection_stale(lambda o:o.update(enumeration='partial')),
    'BODY_LANGUAGE_OWNER_UNENUMERATED:src/lib.rs')
rejects_because('partial-enumeration-refuses-before-the-row-lookup-so-it-cannot-hide-an-owner',
    lambda:shared_selection_stale(lambda o:(o.update(enumeration='partial'),
        o.__setitem__('ownership',[r for r in o['ownership'] if r['path']!='src/lib.rs']))),
    'BODY_LANGUAGE_OWNER_UNENUMERATED:src/lib.rs')
# Same-edition agreeing owners stay valid: two selected targets that agree are the ordinary
# shared-file and lib-plus-test-target case.
check('two-selected-targets-that-agree-remain-valid',
      shared_selection_stale(lambda o:(o['selectedUnitIds'].append(UID('Cargo.toml','bin','legacy')),
          [u.update(targetEdition=2021) for u in o['units']
           if u['unitId']==UID('Cargo.toml','bin','legacy')])).startswith('run2:'))
# ROOT'S STABILITY REQUIREMENT, verified rather than assumed. Moving the same effective edition into
# a selected units table must NOT move the body identity: the projection deliberately excludes unit
# ids, names, paths, the selection and the ownership record id. What DOES move is the ownership
# identity and therefore the sourceUniverse. Same span, same level specification, same compiler,
# same effective edition -> byte-identical projection, version component and body identity.
STABLE_RUN=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
                 workspace=shared_workspace([UID('Cargo.toml','lib','fixture-root')]))
_base_f,_base_p,_base_parts=clone_frame_of(CLONE_RUNS['rust'])
_stab_f,_stab_p,_stab_parts=clone_frame_of(STABLE_RUN)
check('a-richer-ownership-record-does-not-move-an-unchanged-body-identity',
      C.canonical(body_language_version(*projection_inputs(_base_f,CLONE_RUNS['rust'][2],'rust')))
      ==C.canonical(body_language_version(*projection_inputs(_stab_f,STABLE_RUN[2],'rust'))) and
      _base_parts[4]==_stab_parts[4] and _base_p['bodyIdentity']==_stab_p['bodyIdentity'])
check('but-the-ownership-identity-and-the-source-universe-do-move',
      _base_f['sourceUniverse']!=_stab_f['sourceUniverse'] and
      M.parse_h_frame(CLONE_RUNS['rust'][2][_base_f['sourceUniverse']],'native-semantic-universe')[1]['sourceUnitOwnershipId']
      !=M.parse_h_frame(STABLE_RUN[2][_stab_f['sourceUniverse']],'native-semantic-universe')[1]['sourceUnitOwnershipId'])
check('and-changing-the-actual-selected-edition-still-moves-the-body-identity',
      clone_frame_of(SHARED_RUNS[UID('Cargo.toml','lib','fixture-root')])[1]['bodyIdentity']
      !=clone_frame_of(SHARED_RUNS[UID('Cargo.toml','bin','legacy')])[1]['bodyIdentity'])
# A complete Run over a marker under a '#'-containing directory, so the path admission is preserved
# end to end and not only at the schema.
HASH_WORKSPACE={'edition':{'interop':2021},'enumeration':'complete',
  'units':[unit('crates/c#interop/Cargo.toml','lib','interop','interop')],
  'selectedUnitIds':[UID('crates/c#interop/Cargo.toml','lib','interop')],
  'ownership':[{'path':'crates/c#interop/src/lib.rs',
                'unitId':UID('crates/c#interop/Cargo.toml','lib','interop')}]}
HASH_RUN=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
               source_path='crates/c#interop/src/lib.rs',workspace=HASH_WORKSPACE)
_store=M.EvidenceStore();_eid='exec1_'+'4'*32
check('a-body-under-a-hash-containing-directory-prepares-and-commits',
      _store.prepare(*HASH_RUN,_eid,replay)==M.identifier('run',HASH_RUN[0]) and
      _store.commit(_eid)=='committed')
check('its-marker-and-body-paths-survive-the-canonical-path-admission',
      clone_frame_of(HASH_RUN)[0]['anchors'][0]['path']=='crates/c#interop/src/lib.rs' and
      M.parse_h_frame(HASH_RUN[2][M.parse_h_frame(HASH_RUN[2][clone_frame_of(HASH_RUN)[0]['sourceUniverse']],
          'native-semantic-universe')[1]['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')[1]
      ['units'][0]['markerPath']=='crates/c#interop/Cargo.toml')
# The selected-clones SCOPE and COVERAGE boundary, not only body-frame positives. A universe whose
# ownership is partial mints no clone body identity - but that must not void the Run. The existing
# facts/Coverage/indeterminate law carries it: the clones scope reports its own incompleteness, the
# view holds NO facts, the predicate is indeterminate and the seal is indeterminate. Schema validity
# is not a completeness claim about a real repository, and this fixture asserts neither.
EMPTY_CLONE=build(resolved=False,has_match=False,relation='clones',universe_language='rust',
                  source_path='src/lib.rs',
                  workspace=shared_workspace([UID('Cargo.toml','lib','fixture-root')],enumeration='partial'))
_store=M.EvidenceStore();_eid='exec1_'+'3'*32
check('a-partial-ownership-clones-scope-still-prepares-and-commits',
      _store.prepare(*EMPTY_CLONE,_eid,replay)==M.identifier('run',EMPTY_CLONE[0]) and
      _store.commit(_eid)=='committed')
check('a-partial-ownership-clones-scope-mints-no-body-identity-and-holds-no-facts',
      EMPTY_CLONE[1][EMPTY_CLONE[1][EMPTY_CLONE[0]['evidenceId']][1]['viewIds'][0]][1]['facts']==[])
EMPTY_COVERAGE=C.parse(EMPTY_CLONE[2][next(v['payloadDigest'] for k,(d,v) in EMPTY_CLONE[1].items()
                                           if d=='coverage')])
# The disclosure is TYPED, not merely non-null. Under partial ownership the owed pair is
# input-closure-incomplete / body-language-owner-unenumerated, DERIVED from the committed ownership
# record. The earlier revision asserted `resolution-incomplete` with a null cause here, which is what
# let an unrelated deficiency and a missing cause pass: the entry said something was wrong without
# saying what, and nothing compared it to what the universe actually owed.
check('its-coverage-reports-the-incompleteness-rather-than-claiming-complete',
      EMPTY_COVERAGE['entry']['coverage']=='unknown' and
      EMPTY_COVERAGE['entry']['deficiency']=='input-closure-incomplete' and
      EMPTY_COVERAGE['entry']['nativeCause']=='body-language-owner-unenumerated' and
      EMPTY_COVERAGE['entry']['resolutionCompleteness']['state']=='not-applicable' and
      EMPTY_COVERAGE['entry']['resolutionCompleteness']['attempted'] is False)
# examinedExhaustive and resolutionCompleteness.state are DIFFERENT claims and must stay distinct:
# the host may have examined its committed partition exhaustively while resolution is not applicable
# at all. Neither one implies the other, and neither is the ownership disclosure.
check('examined-exhaustive-and-resolution-state-are-distinct-claims',
      EMPTY_COVERAGE['entry']['resolutionCompleteness']['examinedExhaustive'] is False and
      EMPTY_COVERAGE['entry']['resolutionCompleteness']['state']=='not-applicable' and
      EMPTY_COVERAGE['entry']['examinedUniverse']['subjectCount']>=0)
# ROOT'S EXECUTED COUNTEREXAMPLE, closed. The honest control above is not enough on its own: it
# only shows that an incomplete Run CAN be indeterminate, not that the host REFUSES the opposite
# claim. With the same partial ownership and the same empty view, a `complete` Coverage with no
# deficiency and a determinate seal used to close, replay and commit. body_language_version is never
# reached there - there are no facts - so the join has to live at the owning Run's Coverage
# admission, which is the only place with the universe in hand.
def contradictory_clone_coverage(enumeration='partial',ownership_present=True,resolved=True):
    graph=build(resolved=resolved,has_match=False,relation='clones',universe_language='rust',
                source_path='src/lib.rs',
                workspace=shared_workspace([UID('Cargo.toml','lib','fixture-root')],enumeration=enumeration))
    if not ownership_present:
        run,objects,blobs=graph
        key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
        universe=M.parse_h_frame(blobs[objects[key][1]['sourceUniverse']],'native-semantic-universe')[1]
        universe['sourceUnitOwnershipId']=None
        new=M.retain_h_identity('native.semantic-universe.rust.v2',universe,blobs)
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new,targetUniverse=new),run)
        resync_coverage(objects,blobs,run,resolved);resync_witness(objects,blobs,run)
    return M.close_run(*graph)
check('the-honest-incomplete-clone-run-still-closes',
      contradictory_clone_coverage(resolved=False).startswith('run2:'))
rejects_because('a-complete-clones-coverage-over-partial-ownership-is-contradictory-and-refuses',
    lambda:contradictory_clone_coverage(enumeration='partial',resolved=True),
    'COVERAGE_DIALECT_PREREQUISITE:clones:body-language-owner-unenumerated')
rejects_because('and-the-same-claim-over-absent-ownership-refuses-too',
    lambda:contradictory_clone_coverage(enumeration='complete',ownership_present=False,resolved=True),
    'COVERAGE_DIALECT_PREREQUISITE:clones:body-language-ownership-missing')
check('an-absent-ownership-clone-scope-is-still-admissible-when-it-discloses-itself',
      contradictory_clone_coverage(enumeration='complete',ownership_present=False,resolved=False)
      .startswith('run2:'))

# ------------------------------------------------- the disclosure is DERIVED, TYPED and ENFORCED
# Root's retained-Run counterexample showed the concrete bypass: the old prerequisite asked only
# `coverage != complete` and `deficiency is not null`, so an UNRELATED deficiency with a null cause
# admitted under partial ownership. Adding NativeCause members did not close it - a vocabulary that
# nothing derives and nothing compares is not a disclosure law. The expected pair is now derived by
# the owning producer unit from the COMMITTED ownership and THIS scope's subjects, and the Run
# closure re-derives it independently, so the claim cannot define its own correctness.
AMBIGUOUS_UNITS=[unit('Cargo.toml','lib','fixture-root','fixture-root',2021),
                 unit('Cargo.toml','bin','legacy','fixture-root',2015)]
AMBIGUOUS_ROWS=[{'path':'src/lib.rs','unitId':AMBIGUOUS_UNITS[0]['unitId']},
                {'path':'src/lib.rs','unitId':AMBIGUOUS_UNITS[1]['unitId']}]
DISCLOSURE_CASES=[
 ('absent-ownership',dict(enumeration='complete',ownership_present=False),
  'body-language-ownership-missing'),
 ('partial-enumeration',dict(enumeration='partial'),
  'body-language-owner-unenumerated'),
 ('ambiguous-selected-owners',dict(enumeration='complete',
   workspace=shared_workspace([u['unitId'] for u in AMBIGUOUS_UNITS],
                              units=AMBIGUOUS_UNITS,rows=AMBIGUOUS_ROWS)),
  'body-language-owner-ambiguous')]
def disclosure_graph(enumeration='complete',ownership_present=True,workspace=None,mutate=None):
    graph=build(resolved=False,has_match=False,relation='clones',universe_language='rust',
                source_path='src/lib.rs',
                workspace=workspace if workspace is not None else
                shared_workspace([UID('Cargo.toml','lib','fixture-root')],enumeration=enumeration))
    run,objects,blobs=graph
    if not ownership_present:
        key=next(k for k,(d,v) in objects.items() if d=='subject-scope')
        universe=M.parse_h_frame(blobs[objects[key][1]['sourceUniverse']],'native-semantic-universe')[1]
        universe['sourceUnitOwnershipId']=None
        new=M.retain_h_identity('native.semantic-universe.rust.v2',universe,blobs)
        rekey(objects,key,dict(objects[key][1],sourceUniverse=new,targetUniverse=new),run)
        resync_coverage(objects,blobs,run,False);resync_witness(objects,blobs,run)
    if mutate is not None:
        key=next(k for k,(d,v) in objects.items() if d=='coverage')
        coverage=copy.deepcopy(objects[key][1]);payload=C.parse(blobs[coverage['payloadDigest']])
        mutate(payload['entry'])
        coverage['payloadDigest']=put_blob(blobs,payload)
        rekey(objects,key,coverage,run);resync_witness(objects,blobs,run)
    return graph
def disclosed_pair(**kw):
    run,objects,blobs=disclosure_graph(**kw)
    entry=C.parse(blobs[next(v['payloadDigest'] for k,(d,v) in objects.items() if d=='coverage')])['entry']
    return entry['deficiency'],entry['nativeCause']
for label,kw,cause in DISCLOSURE_CASES:
    # The legal pair the producer derives ADMITS, and it is the typed pair - not merely non-null.
    check('clone-disclosure-legal-pair-admits.'+label,
          M.close_run(*disclosure_graph(**kw)).startswith('run2:'))
    check('clone-disclosure-pair-is-the-derived-one.'+label,
          disclosed_pair(**kw)==('input-closure-incomplete',cause))
    # A null cause, a wrong cause, a wrong deficiency and a false complete each refuse, and each
    # refuses for its OWN reason rather than collapsing into one generic fault.
    rejects_because('clone-disclosure-null-cause-refuses.'+label,
        lambda k=kw:M.close_run(*disclosure_graph(mutate=lambda e:e.update(nativeCause=None),**k)),
        'COVERAGE_DIALECT_CAUSE_MISMATCH')
    rejects_because('clone-disclosure-wrong-cause-refuses.'+label,
        lambda k=kw,c=cause:M.close_run(*disclosure_graph(
            mutate=lambda e:e.update(nativeCause=next(x for x in
                ('body-language-ownership-missing','body-language-owner-ambiguous',
                 'body-language-owner-unenumerated') if x!=c)),**k)),
        'COVERAGE_DIALECT_CAUSE_MISMATCH')
    rejects_because('clone-disclosure-wrong-deficiency-refuses.'+label,
        lambda k=kw:M.close_run(*disclosure_graph(
            mutate=lambda e:e.update(deficiency='budget-exhausted'),**k)),
        'COVERAGE_DIALECT_DEFICIENCY_MISMATCH')
    rejects_because('clone-disclosure-false-complete-refuses.'+label,
        lambda k=kw:M.close_run(*disclosure_graph(
            mutate=lambda e:e.update(coverage='complete',deficiency=None,nativeCause=None),**k)),
        'COVERAGE_DIALECT_PREREQUISITE:clones:')
    # The view stays empty and no body identity is fabricated to satisfy the disclosure.
    _r,_o,_b=disclosure_graph(**kw)
    check('clone-disclosure-preserves-empty-view-indeterminacy.'+label,
          _o[_o[_r['evidenceId']][1]['viewIds'][0]][1]['facts']==[] and
          not any(d=='fact' for d,v in _o.values()))
# A DELIBERATELY EXCLUDED selection is not an unfinished enumeration. The owner exists, enumeration
# is complete, and the analysed path is compiled only by a target outside the selection: the host
# examined that subject and correctly produced no fact, so `complete` stays lawful and NO ownership
# disclosure is owed. Collapsing this into the partial case would slander a lawful selection.
check('a-deliberately-excluded-selection-owes-no-ownership-disclosure',
      N.clone_ownership_disclosure(
          shared_workspace([UID('Cargo.toml','bin','legacy')],
              rows=[{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')}]),
          ['src/lib.rs'],{'fixture-root':2021}) is None)
check('a-healthy-complete-selection-owes-no-ownership-disclosure',
      N.clone_ownership_disclosure(
          shared_workspace([UID('Cargo.toml','lib','fixture-root')]),
          ['src/lib.rs'],{'fixture-root':2021}) is None)
check('an-unenumerated-workspace-owes-a-disclosure-even-when-every-row-looks-healthy',
      N.clone_ownership_disclosure(
          shared_workspace([UID('Cargo.toml','lib','fixture-root')],enumeration='partial'),
          ['src/lib.rs'],{'fixture-root':2021})['nativeCause']=='body-language-owner-unenumerated')
# The prerequisite is UNIVERSE level by design: a per-body refusal is compatible with `complete`,
# because the host examined that subject and correctly produced no fact for it.
check('a-per-body-refusal-does-not-invalidate-a-complete-clones-coverage',
      M.close_run(*build(resolved=True,has_match=False,relation='clones',universe_language='rust',
          source_path='src/lib.rs',
          workspace=shared_workspace([UID('Cargo.toml','bin','legacy')],
              rows=[{'path':'src/lib.rs','unitId':UID('Cargo.toml','lib','fixture-root')}]))).startswith('run2:'))
check('and-the-seal-is-indeterminate-not-a-false-pass',
      EMPTY_CLONE[1][EMPTY_CLONE[0]['evaluationSealId']][1]['verdict']=='indeterminate')
check('the-scope-that-produced-it-is-a-real-clones-scope-of-this-universe',
      (lambda scope:scope['relation']=='clones' and scope['resolution']=='normalized-body-hash'
                    and scope['subjects']==['src/lib.rs'])
      (next(v for k,(d,v) in EMPTY_CLONE[1].items() if d=='subject-scope')))
check('a-producer-that-cannot-mint-a-body-identity-cannot-assert-a-clone-fact-either',
      not_admitted(lambda:build(resolved=True,has_match=True,relation='clones',universe_language='rust',
          source_path='src/lib.rs',
          workspace=shared_workspace([UID('Cargo.toml','lib','fixture-root')],enumeration='partial'))))
check('omitting-a-conflicting-owner-is-not-a-selection-it-is-a-different-committed-record',
      M.retain_h_identity(N.SOURCE_UNIT_OWNERSHIP_DOMAIN,
          {'schemaVersion':1,'enumeration':'complete','units':sorted(SHARED_UNITS,key=lambda u:u['unitId'].encode()),
           'selectedUnitIds':[UID('Cargo.toml','lib','fixture-root')],
           'ownership':sorted(SHARED_ROWS,key=lambda r:(r['path'].encode(),r['unitId'].encode()))},{})
      !=M.retain_h_identity(N.SOURCE_UNIT_OWNERSHIP_DOMAIN,
          {'schemaVersion':1,'enumeration':'complete','units':[SHARED_UNITS[0]],
           'selectedUnitIds':[UID('Cargo.toml','lib','fixture-root')],
           'ownership':[SHARED_ROWS[0]]},{}))

# --- root v5 addendum: the BODY language is not the PROVIDER language ---------------------------
# Native 6.3 closes the normalized-body languageId to {typescript, javascript, rust} so a .ts and a
# .js body never group even with identical bytes. One TypeScript ENGINE universe produces both.
JS_RUN=build(resolved=True,has_match=True,relation='clones',source_path='legacy.js')
_store=M.EvidenceStore();_eid='exec1_'+'f'*32
check('a-javascript-clone-run-through-the-typescript-engine-prepares',
      _store.prepare(*JS_RUN,_eid,replay)==M.identifier('run',JS_RUN[0]))
check('a-javascript-clone-run-through-the-typescript-engine-commits',_store.commit(_eid)=='committed')
_jf,_jp,_jparts=clone_frame_of(JS_RUN)
check('a-javascript-body-carries-the-javascript-identifier-not-the-engines',
      _jparts[3]==b'javascript' and
      body_language_version(*projection_inputs(_jf,JS_RUN[2],'typescript'))['languageId']=='javascript' and
      UNIVERSE_ROW['typescript']['language']=='typescript')
check('identical-bytes-in-a-ts-and-a-js-body-do-not-share-an-identity',
      LANGUAGE_FIXTURE['typescript']['sourceBytes']==TS_SOURCES['legacy.js'] and
      clone_frame_of(CLONE_RUNS['typescript'])[1]['bodyIdentity']!=_jp['bodyIdentity'])
rejects_because('a-body-frame-naming-a-language-this-engine-does-not-produce-refuses',
    lambda:clone_mutation_in('typescript',lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,language='rust'))),
    'BODY_IDENTITY_LANGUAGE_JOIN:rust')
rejects_because('a-javascript-frame-over-a-typescript-body-refuses',
    lambda:clone_mutation_in('typescript',lambda f,p,b,o,r:p.update(bodyIdentity=reframed(p,b,language='javascript'))),
    'BODY_IDENTITY_LANGUAGE_JOIN:javascript')
check('the-registry-carries-the-derived-body-language-selector',
      set(BINDING['typescript']['bodyLanguageByVariant'].values())=={'typescript','javascript'} and
      BINDING['typescript']['bodyLanguages']==['typescript','javascript'] and
      BINDING['rust']['bodyLanguages']==['rust'] and
      set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum'])
      =={'typescript','javascript','rust'})
check('two-editions-in-one-universe-produce-two-different-body-identities',
      clone_frame_of(MIXED_RUNS['src/lib.rs'])[1]['bodyIdentity']!=
      clone_frame_of(MIXED_RUNS['vendor/fixture-dep/src/lib.rs'])[1]['bodyIdentity'])
check('several-agreeing-owners-of-one-path-are-admissible',
      len([r for r in MIXED_WORKSPACE['ownership'] if r['path']=='src/lib.rs'])==2)
def mixed_ownership(mutate,source_path='src/lib.rs'):
    """Re-frame ONLY the committed ownership record of a mixed-edition clone Run."""
    workspace=copy.deepcopy(MIXED_WORKSPACE);mutate(workspace)
    run,objects,blobs=build(resolved=True,has_match=True,relation='clones',universe_language='rust',
                            workspace=workspace,source_path=source_path)
    return M.close_run(run,objects,blobs)
check('ownership-harness-positive-control-closes',mixed_ownership(lambda w:None).startswith('run2:'))
# Wrong and missing owner claims, judged at CLOSURE over an already-minted body identity. Each
# re-frames only the committed ownership record; the positive control re-frames it unchanged.
def stale_ownership(mutate):
    return clone_run_with_universe(lambda u:None,mutate_ownership=mutate,
                                   source_path='src/lib.rs',workspace=MIXED_WORKSPACE)[0]
check('stale-ownership-harness-positive-control-closes',
      stale_ownership(lambda o:None).startswith('run2:'))
rejects_because('a-body-whose-owner-rows-are-withdrawn-under-complete-enumeration-is-not-compiled',
    lambda:stale_ownership(lambda o:o.__setitem__('ownership',
        [r for r in o['ownership'] if r['path']!='src/lib.rs'])),
    'BODY_LANGUAGE_OWNER_NOT_COMPILED:src/lib.rs')
rejects_because('the-same-absence-under-partial-enumeration-is-unenumerated-not-uncompiled',
    lambda:stale_ownership(lambda o:(o.update(enumeration='partial'),o.__setitem__('ownership',
        [r for r in o['ownership'] if r['path']!='src/lib.rs']))),
    'BODY_LANGUAGE_OWNER_UNENUMERATED:src/lib.rs')
rejects_because('selected-owners-that-disagree-about-the-edition-refuse-rather-than-picking-one',
    lambda:stale_ownership(lambda o:o['ownership'].append(
        {'path':'src/lib.rs','unitId':UID('vendor/fixture-dep/Cargo.toml','lib','legacy-crate')})),
    'BODY_LANGUAGE_OWNER_AMBIGUOUS:src/lib.rs:2')
rejects_because('a-selected-unit-naming-a-crate-the-universe-has-no-edition-for-refuses',
    lambda:stale_ownership(lambda o:[u.update(crateName='never-declared') for u in o['units']
                                     if u['unitId']==UID('Cargo.toml','lib','fixture-root')]),
    'BODY_LANGUAGE_OWNER_AMBIGUOUS:unknown-crate:never-declared')

# An ownership row naming a path outside the snapshot is refused TWICE, and the identity closure's
# own snapshot join reaches it first. Both are asserted, at the place each actually fires.
rejects_because('an-owner-row-naming-a-path-outside-the-snapshot-refuses-at-the-identity-join',
    lambda:stale_ownership(lambda o:o['ownership'].append(
        {'path':'not/in/snapshot.rs','unitId':UID('Cargo.toml','lib','fixture-root')})),
    'NATIVE_NESTED_PATH_NOT_INVENTORIED:not/in/snapshot.rs')
GHOST_OWNERSHIP={'schemaVersion':1,'enumeration':'complete',
  'units':[unit('Cargo.toml','lib','fixture-root','fixture-root')],
  'selectedUnitIds':[UID('Cargo.toml','lib','fixture-root')],
  'ownership':[{'path':'not/in/snapshot.rs','unitId':UID('Cargo.toml','lib','fixture-root')}]}
RINV={r['path']:r for r in RINVENTORY}
check('the-owning-native-contract-refuses-the-same-row-independently',
      'native.universe-retained-input-mismatch:sourceUnitOwnership.path' in
      N.source_unit_ownership_faults(GHOST_OWNERSHIP,RPARTS['universe'],RINV))
# Unit identity is DERIVED from its own metadata, so a caller label unbound to admitted metadata
# cannot pass and two contradictory rows for one purported unit cannot become two units by accident.
# The unit identity is recomputed INDEPENDENTLY here, from the published preimage and the foundation
# H recipe, rather than by calling the same helper twice.
def independent_unit_id(marker,kind,name):
    return 'sha256:'+C.identity('native.compilation-unit.v1',
        {'schemaVersion':1,'markerPath':marker,'targetKind':kind,'targetName':name})
check('a-unit-id-is-the-published-h-projection-of-its-own-metadata',
      N.source_unit_id(GHOST_OWNERSHIP['units'][0])==independent_unit_id('Cargo.toml','lib','fixture-root') and
      N.source_unit_id({'markerPath':'crates/a/Cargo.toml','targetKind':'test','targetName':'it'})
      ==independent_unit_id('crates/a/Cargo.toml','test','it'))
check('a-unit-id-is-fixed-width-for-every-admitted-path-and-name-length',
      len({len(independent_unit_id('a'*4000+'/Cargo.toml','bench','n'*250)),
           len(independent_unit_id('a/Cargo.toml','lib','n'))})==1)
# ROOT'S RETAINED COUNTEREXAMPLE: a '#' in a repository directory is admissible under the canonical
# repository-path contract, and the withdrawn delimiter recipe could stay injective only by
# forbidding it. The H projection admits it, and two units differing only inside that directory name
# still receive different identities.
HASH_DIR_UNIT={'markerPath':'crates/c#interop/Cargo.toml','targetKind':'lib','targetName':'interop'}
check('a-marker-under-a-hash-containing-directory-is-admitted-not-narrowed',
      N.validate_native('UnitIdentityV1',dict(HASH_DIR_UNIT,schemaVersion=1)) is not False and
      N.source_unit_id(HASH_DIR_UNIT)==independent_unit_id(*HASH_DIR_UNIT.values()))
check('two-markers-differing-only-inside-a-hash-directory-still-differ',
      N.source_unit_id({'markerPath':'crates/c#interop/Cargo.toml','targetKind':'lib','targetName':'interop'})
      !=N.source_unit_id({'markerPath':'crates/c-interop/Cargo.toml','targetKind':'lib','targetName':'interop'}))
check('a-caller-label-unbound-to-its-metadata-is-refused-by-the-owning-contract',
      'native.universe-retained-input-mismatch:sourceUnitOwnership.unitId' in
      N.source_unit_ownership_faults(
          {**GHOST_OWNERSHIP,'units':[dict(GHOST_OWNERSHIP['units'][0],unitId='whatever-i-like')],
           'selectedUnitIds':['whatever-i-like'],
           'ownership':[{'path':'src/lib.rs','unitId':'whatever-i-like'}]},RPARTS['universe'],RINV))
check('a-selection-naming-a-unit-the-table-does-not-declare-is-refused',
      'native.universe-retained-input-mismatch:sourceUnitOwnership.selectedUnitIds' in
      N.source_unit_ownership_faults({**GHOST_OWNERSHIP,'selectedUnitIds':[UID('Cargo.toml','bin','ghost')]},
          RPARTS['universe'],RINV))
check('a-unit-marker-outside-the-snapshot-is-refused',
      'native.universe-retained-input-mismatch:sourceUnitOwnership.markerPath' in
      N.source_unit_ownership_faults(
          {**GHOST_OWNERSHIP,
           'units':[unit('ghost/Cargo.toml','lib','x','fixture-root')],
           'selectedUnitIds':[UID('ghost/Cargo.toml','lib','x')],
           'ownership':[{'path':'src/lib.rs','unitId':UID('ghost/Cargo.toml','lib','x')}]},RPARTS['universe'],RINV))
check('a-deferring-unit-naming-a-crate-with-no-committed-edition-is-refused',
      'native.universe-retained-input-mismatch:sourceUnitOwnership.crateName' in
      N.source_unit_ownership_faults(
          {**GHOST_OWNERSHIP,'units':[dict(GHOST_OWNERSHIP['units'][0],crateName='never-declared')]},
          RPARTS['universe'],RINV))
check('two-contradictory-rows-for-one-purported-unit-cannot-become-two-units',
      not_admitted(lambda:N.validate_native('SourceUnitOwnershipV1',
          {**GHOST_OWNERSHIP,'units':[GHOST_OWNERSHIP['units'][0],
              dict(GHOST_OWNERSHIP['units'][0],crateName='other-crate')]})))
check('ownership-establishes-the-join-and-does-not-enter-the-record',
      set(body_language_version(*projection_inputs(*clone_frame_of(MIXED_RUNS['src/lib.rs'])[:1],
          MIXED_RUNS['src/lib.rs'][2],'rust')))=={'schemaVersion','languageId','compilerName',
          'compilerVersion','compilerBuild','dialect'})
check('the-binding-names-its-exclusions-with-reasons',
      set(BINDING['rust']['excluded'])>={'targetTriple','hostTriple','cargoVersion','crateRootPaths','editionMapKeys'} and
      set(BINDING['typescript']['excluded'])>={'languageMode','synthesizerVersion','libSelection'} and
      all(isinstance(v,str) and v for v in BINDING['rust']['excluded'].values()) and
      all(isinstance(v,str) and v for v in BINDING['typescript']['excluded'].values()))
check('every-field-of-the-derived-record-is-supplied-by-every-language-binding',
      all(set(M.SCHEMA['$defs']['body-language-version']['required'])==
          {'schemaVersion','languageId','dialect'}|set(BINDING[l]['fields'])
          for l in ('typescript','rust')))
check('every-compiler-field-is-read-from-the-admitted-context-or-is-a-declared-constant',
      all(('const' in source) or source['source']=='native-context'
          for l in ('typescript','rust') for source in BINDING[l]['fields'].values()))
check('every-language-declares-an-explicit-dialect-axis-with-a-selection-law',
      all(BINDING[l]['dialect'] is not None and len(BINDING[l]['dialect']['selectionLaw'])>200
          for l in ('typescript','rust')) and
      BINDING['typescript']['dialect']['form']=='closed-suffix-table' and
      BINDING['rust']['dialect']['form']=='selected-compilation-target-edition')
check('the-typescript-variant-table-covers-the-normal-variants-and-is-longest-suffix',
      set(BINDING['typescript']['dialect']['table'])>={'.ts','.tsx','.js','.jsx','.mts','.cts','.mjs','.cjs','.d.ts'} and
      BINDING['typescript']['dialect']['table']['.d.ts']!=BINDING['typescript']['dialect']['table']['.ts'])
for _suffix,_variant in [('.tsx','tsx'),('.d.ts','ts-declaration'),('.mts','mts'),('.js','js')]:
    check('a-'+_variant+'-body-takes-its-own-source-variant',
          body_language_version(*universe_and_context(*[clone_frame_of(CLONE_RUNS['typescript'])[0],
              CLONE_RUNS['typescript'][2]]),UNIVERSE_ROW['typescript'],
              {'path':'x'+_suffix})['dialect']=={'sourceVariant':_variant})
check('two-typescript-variants-of-one-body-do-not-collide',
      len({C.canonical(body_language_version(*universe_and_context(clone_frame_of(CLONE_RUNS['typescript'])[0],
              CLONE_RUNS['typescript'][2]),UNIVERSE_ROW['typescript'],{'path':'x'+s}))
           for s in ('.ts','.tsx','.d.ts','.js')})==4)
# The MODEL's own refusal, not the fixture's restatement of it.
rejects_because('an-unlisted-typescript-suffix-refuses-rather-than-being-folded-into-a-neighbour',
    lambda:M.body_language_version(*universe_and_context(clone_frame_of(CLONE_RUNS['typescript'])[0],
        CLONE_RUNS['typescript'][2]),UNIVERSE_ROW['typescript'],{'path':'x.vue'}),
    'BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN:x.vue')
check('the-model-and-the-independent-fixture-agree-on-every-listed-variant',
      all(C.canonical(M.body_language_version(*universe_and_context(clone_frame_of(CLONE_RUNS['typescript'])[0],
              CLONE_RUNS['typescript'][2]),UNIVERSE_ROW['typescript'],{'path':'x'+suffix}))
          ==C.canonical(body_language_version(*universe_and_context(clone_frame_of(CLONE_RUNS['typescript'])[0],
              CLONE_RUNS['typescript'][2]),UNIVERSE_ROW['typescript'],{'path':'x'+suffix}))
          for suffix in BINDING['typescript']['dialect']['table']))

# The law is CONSUMED, not counted: a newly annotated field with no join refuses the Run.
def unjoined_annotated_field():
    """A HYPOTHETICAL document, not a mutated module: the question "would this document be lawful"
    is asked of a copy, so the registered law and this process are left exactly as they were."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['$defs']['FilePayloadV1']['properties']['byteLength']['x-opensip-digest']={
        'representation':'raw-artifact','retention':'preimage'}
    document['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0].pop('lengthField')
    return M.relation_annotation_closure('file',document)
def join_naming_a_field_the_schema_lacks():
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]['anchorPathField']='inventedField'
    return M.relation_annotation_closure('file',document)
rejects_because('a-join-naming-a-field-the-selector-lacks-is-inadmissible',join_naming_a_field_the_schema_lacks,
                'RELATION_JOIN_FIELD_UNKNOWN:file:inventedField')
rejects_because('an-annotated-relation-field-with-no-join-is-inadmissible',unjoined_annotated_field,
                'RELATION_DIGEST_LAW_RESIDUE:file:byteLength')
# v9-S1. The check below used to carry this name while asserting only that the closure returns
# non-None and that the join-bearing relation set is the expected four. The independent reviewer
# reproduced that assertion verbatim against a document carrying an unannotated CanonicalPath and it
# still evaluated True, then injected an unannotated governed field into all 13 selectors x 3
# governed forms and had all 39 ADMITTED. The name asserted a property nothing tested. It now tests
# it: the sweep is the consumed third limb, and the ANNOTATED half of the name is a measurement.
RELATION_COVERAGE=M.relation_digest_annotation_coverage()
check('every-relation-payload-digest-and-path-field-is-annotated-and-joined',
      RELATION_COVERAGE['unannotated']==[] and RELATION_COVERAGE['total']==RELATION_COVERAGE['annotated']
      and RELATION_COVERAGE['total']==7 and
      all(M.relation_annotation_closure(name) is not None for name in M.RELATIONS) and
      {name for name,row in M.RELATIONS.items() if row['snapshotJoins'] or 'bodyIdentityJoin' in row}
      =={'file','package','vcs-change','clones'})
check('the-sweep-finds-exactly-the-governed-fields-and-does-not-invent-others',
      RELATION_COVERAGE['governedForms']==['DigestHex','Sha256Text','CanonicalPath'] and
      {r:v['annotated'] for r,v in RELATION_COVERAGE['byRelation'].items() if v['annotated']}
      =={'file':2,'package':1,'vcs-change':2,'clones':2})
# byteLength is ANNOTATED but not governed - it refs UInt64. The sweep must not count it, or the
# totals would silently drift and the law would appear to cover a field it does not govern.
check('an-annotated-non-governed-field-is-not-counted-as-governed',
      'x-opensip-digest' in M.RELATION_DOCUMENT['$defs']['FilePayloadV1']['properties']['byteLength'] and
      not any(path.startswith('file.byteLength') for path in
              [p for v in RELATION_COVERAGE['byRelation'].values() for p in v['unannotated']]) and
      RELATION_COVERAGE['byRelation']['file']['annotated']==2)

# THE THIRD LIMB, exercised as the reviewer exercised it: all 13 relations x all 3 governed forms.
def stray_governed(relation,form,annotate=False,shape='ref'):
    """Inject one governed field into one relation's selector, in one of the shapes the traversal
    must handle, and ask the closure about THAT relation - the ordering artifact p03 recorded."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    selector=document['$defs'][M.RELATIONS[relation]['selector'].split('/')[-1]]
    node={'ref':{'$ref':'#/$defs/'+form},
          'inline':dict(document['$defs'][form]),
          'nullable':{'oneOf':[{'$ref':'#/$defs/'+form},{'type':'null'}]},
          'aliased':{'$ref':'#/$defs/StrayAliasV1'},
          'nested':{'type':'object','additionalProperties':False,'required':['inner'],
                    'properties':{'inner':{'$ref':'#/$defs/'+form}}},
          'array':{'type':'array','items':{'$ref':'#/$defs/'+form}},
          # A $ref to a CONTAINER def, whose member is governed. My first v7 control matrix missed
          # this exact shape and root's executed counterexample found it admitted; the traversal now
          # follows a referenced container rather than stopping at a ref it cannot resolve to a
          # governed scalar.
          'container-ref':{'$ref':'#/$defs/StrayContainerV1'},
          # A container that refers to itself. The chain guard must terminate rather than recurse.
          'cyclic-container-ref':{'$ref':'#/$defs/StrayCycleV1'}}[shape]
    if shape=='aliased':document['$defs']['StrayAliasV1']={'$ref':'#/$defs/'+form}
    if shape=='container-ref':
        document['$defs']['StrayContainerV1']={'type':'object','additionalProperties':False,
            'required':['hidden'],'properties':{'hidden':{'$ref':'#/$defs/'+form}}}
    if shape=='cyclic-container-ref':
        document['$defs']['StrayCycleV1']={'type':'object','additionalProperties':False,
            'properties':{'hidden':{'$ref':'#/$defs/'+form},'again':{'$ref':'#/$defs/StrayCycleV1'}}}
    if annotate:node=dict(node,**{'x-opensip-digest':{'representation':'raw-artifact',
        'retention':'not-joined','authority':'test','reason':'a control, not a shipped field'}})
    selector['properties']['strayGoverned']=node
    return M.relation_annotation_closure(relation,document)
_admitted=[]
for _relation in sorted(M.RELATIONS):
    for _form in ('DigestHex','Sha256Text','CanonicalPath'):
        try:
            stray_governed(_relation,_form);_admitted.append(_relation+'/'+_form)
        except C.AdmissionError:pass
check('all-13-relations-times-3-governed-forms-refuse-an-unannotated-field',_admitted==[])
rejects_because('an-unannotated-governed-field-names-its-relation-field-and-form',
    lambda:stray_governed('file','DigestHex'),
    'RELATION_DIGEST_UNANNOTATED:file:file.strayGoverned:DigestHex')
# The POSITIVE control for the same injection: annotate it and declare it not-joined, and the very
# same field is admissible. So the refusals above are caused by the missing annotation and by
# nothing else about injecting a field.
check('the-same-injected-field-is-admissible-once-it-is-annotated',
      all(stray_governed(relation,form,annotate=True) is not None
          for relation in sorted(M.RELATIONS) for form in ('DigestHex','Sha256Text','CanonicalPath')))
# The shapes the traversal has to see through. Each is a real form this document or its native
# sibling already uses, or a form a future edit could reach for.
for _shape in ('ref','inline','nullable','aliased','nested','array','container-ref','cyclic-container-ref'):
    rejects_because('an-unannotated-governed-field-in-'+_shape+'-form-is-still-seen',
        lambda shape=_shape:stray_governed('file','CanonicalPath',shape=shape),
        'RELATION_DIGEST_UNANNOTATED:file:')
    check('and-'+_shape+'-form-is-admissible-once-annotated',
          stray_governed('file','CanonicalPath',annotate=True,shape=_shape) is not None)
# REMOVING an existing annotation is the same defect arriving by deletion rather than addition, and
# it is the reviewer's p03 case that previously reached only 'any refusal'.
for _relation,_field in [('clones','bodyIdentity'),('clones','normalisationVersion'),
                         ('file','path'),('file','contentSha256'),('package','manifestPath'),
                         ('vcs-change','path'),('vcs-change','previousPath')]:
    def _stripped(relation=_relation,field=_field):
        document=copy.deepcopy(M.RELATION_DOCUMENT)
        document['$defs'][M.RELATIONS[relation]['selector'].split('/')[-1]]['properties'][field].pop('x-opensip-digest')
        return M.relation_annotation_closure(relation,document)
    rejects_because('removing-the-annotation-from-'+_relation+'-'+_field+'-is-inadmissible',_stripped,
        'RELATION_DIGEST_UNANNOTATED:'+_relation+':'+_relation+'.'+_field)
# ROOT'S EXECUTED TRAVERSAL COUNTEREXAMPLE, closed. Two disjoint oneOf branches share one field:
# an annotation on ONE of them says nothing about the other, so admissibility must not depend on
# which branch is written last. The draft collapsed both branches onto one path key and the later
# write won; each branch now carries its own path and uncovered evidence is never overwritten.
def stray_two_branches(reverse=False):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    uncovered={'$ref':'#/$defs/DigestHex','enum':['a'*64]}
    covered={'$ref':'#/$defs/CanonicalPath','enum':['src/a.rs'],
             'x-opensip-digest':{'representation':'raw-artifact','retention':'not-joined',
                                 'authority':'test','reason':'a control, not a shipped field'}}
    branches=[covered,uncovered] if reverse else [uncovered,covered]
    document['$defs']['FilePayloadV1']['properties']['stray']={'oneOf':branches}
    return M.relation_annotation_closure('file',document)
for _reverse in (False,True):
    rejects_because('an-unannotated-branch-is-seen-whichever-order-it-sits-in-'+str(_reverse),
        lambda reverse=_reverse:stray_two_branches(reverse),
        'RELATION_DIGEST_UNANNOTATED:file:file.stray|oneOf[')
check('branch-order-does-not-decide-admissibility',
      not_admitted(lambda:stray_two_branches(False)) and not_admitted(lambda:stray_two_branches(True)))
check('and-a-parent-annotation-still-covers-every-branch-of-a-nullable-field',
      stray_governed('file','CanonicalPath',annotate=True,shape='nullable') is not None)
# ROOT'S ALIAS-LOCATION COUNTEREXAMPLE, closed. The rule is that an annotation ANYWHERE ON THE PATH
# covers the leaf, and a ref chain is part of the path, so an annotation on an INTERMEDIATE alias
# definition must count. An annotation on the TERMINAL governed def deliberately does not: that would
# blanket-cover every field of that form in every relation, which is the hole this limb closes.
def alias_annotation(where):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    annotation={'representation':'raw-artifact','retention':'not-joined','authority':'test',
                'reason':'a control, not a shipped field'}
    document['$defs']['StrayAliasV1']={'$ref':'#/$defs/DigestHex'}
    document['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/StrayAliasV1'}
    if where=='field':document['$defs']['FilePayloadV1']['properties']['stray']['x-opensip-digest']=annotation
    if where=='alias':document['$defs']['StrayAliasV1']['x-opensip-digest']=annotation
    if where=='terminal':document['$defs']['DigestHex']=dict(document['$defs']['DigestHex'],**{'x-opensip-digest':annotation})
    return M.relation_annotation_closure('file',document)
rejects_because('an-unannotated-field-behind-an-alias-is-inadmissible',lambda:alias_annotation('nowhere'),
                'RELATION_DIGEST_UNANNOTATED:file:file.stray:DigestHex')
check('an-annotation-on-the-field-covers-a-leaf-behind-an-alias',alias_annotation('field') is not None)
check('an-annotation-on-the-intermediate-alias-definition-covers-it-too',alias_annotation('alias') is not None)
rejects_because('but-an-annotation-on-the-terminal-governed-def-is-not-a-blanket-exemption',
    lambda:alias_annotation('terminal'),'RELATION_DIGEST_UNANNOTATED:file:file.stray:DigestHex')
# ROOT'S INHERITED-LIMB CONSISTENCY COUNTEREXAMPLE, closed. v7 gave the COVERAGE limb an inherited
# notion of "annotated" - property, enclosing branch parent, or intermediate alias $def - while
# retention and residue still read properties[field]['x-opensip-digest'] directly. So exactly at the
# locations the revised traversal newly accepted, a field escaped both earlier limbs: root's nine
# vectors showed the three FIELD cases behaving while all six ALIAS and BRANCH cases admitted,
# including a dangling preimage with no join and an invented retention. Every limb now reads one
# account of effective annotations, so all three locations reach the SAME cause.
def stray_at(location,retention):
    """Root's nine vectors: the same governed `stray` field, annotated at one of three supported
    locations, with one of three retentions."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['$defs']['ProbeAliasV1']={'$ref':'#/$defs/DigestHex'}
    annotation={'representation':'raw-artifact','retention':retention,'authority':'test',
                'reason':'a control, not a shipped field'}
    field={'$ref':'#/$defs/ProbeAliasV1'}
    if location=='field':field['x-opensip-digest']=annotation
    elif location=='alias':document['$defs']['ProbeAliasV1']['x-opensip-digest']=annotation
    else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
    document['$defs']['FilePayloadV1']['properties']['stray']=field
    return M.relation_annotation_closure('file',document)
for _location in ('field','alias','branch'):
    rejects_because('a-dangling-preimage-annotation-at-the-'+_location+'-location-is-residue',
        lambda location=_location:stray_at(location,'preimage'),
        'RELATION_DIGEST_LAW_RESIDUE:file:stray')
    rejects_because('an-invented-retention-at-the-'+_location+'-location-is-refused',
        lambda location=_location:stray_at(location,'invented-retention'),
        'RELATION_DIGEST_RETENTION:file.stray')
    check('and-the-lawful-not-joined-control-at-the-'+_location+'-location-still-admits',
          stray_at(_location,'not-joined') is not None)
check('every-supported-annotation-location-reaches-the-same-cause',
      all(not_admitted(lambda location=l:stray_at(location,'preimage')) for l in ('field','alias','branch')) and
      all(not_admitted(lambda location=l:stray_at(location,'invented-retention')) for l in ('field','alias','branch')) and
      all(stray_at(l,'not-joined') is not None for l in ('field','alias','branch')))
# A joinable sighting whose owning field IS named by a join is admissible at every location - so the
# refusals above are caused by the missing join and the bad retention, not by using an alias or a
# branch at all. This is the control that stops "reject every alias and branch" passing for a fix.
def stray_joined(location):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['$defs']['ProbeAliasV1']={'$ref':'#/$defs/DigestHex'}
    annotation={'representation':'raw-artifact','retention':'preimage','authority':'test',
                'reason':'a control, not a shipped field'}
    field={'$ref':'#/$defs/ProbeAliasV1'}
    if location=='field':field['x-opensip-digest']=annotation
    elif location=='alias':document['$defs']['ProbeAliasV1']['x-opensip-digest']=annotation
    else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
    document['$defs']['FilePayloadV1']['properties']['stray']=field
    document['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]['digestField']='stray'
    document['$defs']['FilePayloadV1']['properties']['contentSha256']['x-opensip-digest']=dict(
        document['$defs']['FilePayloadV1']['properties']['contentSha256']['x-opensip-digest'],retention='not-joined')
    return M.relation_annotation_closure('file',document)
for _location in ('field','alias','branch'):
    check('a-joined-preimage-annotation-at-the-'+_location+'-location-admits',
          stray_joined(_location) is not None)
# BOUNDARY, stated and enforced rather than claimed away: a join row reads value[field], which never
# reaches a nested member or an array element. Such a sighting must declare not-joined.
def stray_unjoinable(shape,retention):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    annotation={'representation':'raw-artifact','retention':retention,'authority':'test',
                'reason':'a control, not a shipped field'}
    inner=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':annotation})
    document['$defs']['FilePayloadV1']['properties']['stray']=(
        {'type':'object','additionalProperties':False,'required':['inner'],'properties':{'inner':inner}}
        if shape=='nested' else {'type':'array','items':inner})
    return M.relation_annotation_closure('file',document)
for _shape,_path in (('nested','file.stray.inner'),('array','file.stray[]')):
    rejects_because('a-'+_shape+'-governed-leaf-cannot-claim-a-joinable-retention',
        lambda shape=_shape:stray_unjoinable(shape,'preimage'),
        'RELATION_DIGEST_UNJOINABLE_LOCATION:file:'+_path)
    check('but-a-'+_shape+'-governed-leaf-declaring-not-joined-admits',
          stray_unjoinable(_shape,'not-joined') is not None)
    rejects_because('and-an-invented-retention-there-is-still-refused-first-'+_shape,
        lambda shape=_shape:stray_unjoinable(shape,'invented-retention'),
        'RELATION_DIGEST_RETENTION:file.stray')
# BOUNDARY: the law states no precedence between an annotation on a property and one on the alias it
# refs, so none is invented. Two that DISAGREE refuse; two that are IDENTICAL do not.
def stray_two_annotations(same):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    first={'representation':'raw-artifact','retention':'not-joined','authority':'test','reason':'control'}
    second=dict(first) if same else dict(first,retention='preimage')
    document['$defs']['ProbeAliasV1']=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':second})
    document['$defs']['FilePayloadV1']['properties']['stray']=dict(
        {'$ref':'#/$defs/ProbeAliasV1'},**{'x-opensip-digest':first})
    return M.relation_annotation_closure('file',document)
rejects_because('two-disagreeing-annotations-on-one-sighting-are-a-conflict-not-a-silent-winner',
    lambda:stray_two_annotations(False),'RELATION_DIGEST_ANNOTATION_CONFLICT:file:file.stray')
check('but-two-identical-annotations-on-one-sighting-are-not-a-conflict',
      stray_two_annotations(True) is not None)
# The directly annotated NON-governed property stays inside retention and residue, which is what
# keeps file.byteLength (a UInt64) in those limbs while correctly outside the governed count.
check('a-directly-annotated-non-governed-property-is-still-a-sighting-for-the-earlier-limbs',
      any(s['path']=='file.byteLength' and s['form'] is None and s['annotations']
          for s in M.relation_digest_annotation_coverage()['byRelation']['file']['sightings']))
# The other two limbs must still reach their own causes with the third limb in front of them.# The other two limbs must still reach their own causes with the third limb in front of them.
# THE INDEPENDENT REVIEWER'S p02 ORDER-DEPENDENCE, closed. record() claimed "never let an annotated
# sighting erase an unannotated one at the same path", but it REBOUND the annotation list to the
# merged one before testing it, so the test was true only when both sides were empty and the rule
# collapsed to "poison iff the FIRST-recorded sighting was unannotated". The missing-annotation fact
# is now carried explicitly and monotonically, so no later sighting can undo it.
def same_path_pair(order,shape):
    """Two schemas reaching ONE path - one annotated, one not - with the visit order exchanged.

    `container` moves the annotation between a $ref'd container and the local sibling refinement, so
    the two documents genuinely differ. `keyorder` swaps only which JSON key is written first, so the
    two documents are CANONICALLY EQUAL and any verdict difference would be pure implementation
    artifact. Both are the independent reviewer's constructions."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    annotation={'representation':'raw-artifact','retention':'not-joined','authority':'test',
                'reason':'a control, not a shipped field'}
    bare={'$ref':'#/$defs/DigestHex'}
    marked=dict(bare,**{'x-opensip-digest':annotation})
    selector=document['$defs']['FilePayloadV1']['properties']
    if shape=='container':
        document['$defs']['ProbeContainerV1']={'type':'object','properties':{
            'leaf':bare if order=='unannotated-first' else marked}}
        selector['probe']={'$ref':'#/$defs/ProbeContainerV1',
                           'properties':{'leaf':marked if order=='unannotated-first' else bare}}
    else:
        selector['probe']=({'items':bare,'additionalProperties':marked} if order=='unannotated-first'
                           else {'additionalProperties':marked,'items':bare})
    return document
for _shape,_path in (('container','file.probe.leaf'),('keyorder','file.probe[]')):
    for _order in ('unannotated-first','annotated-first'):
        rejects_because('a-same-path-'+_shape+'-pair-refuses-with-'+_order,
            lambda order=_order,shape=_shape:M.relation_annotation_closure('file',same_path_pair(order,shape)),
            'RELATION_DIGEST_UNANNOTATED:file:'+_path)
    check('and-'+_shape+'-admissibility-does-not-depend-on-visit-order',
          not_admitted(lambda shape=_shape:M.relation_annotation_closure('file',same_path_pair('unannotated-first',shape))) and
          not_admitted(lambda shape=_shape:M.relation_annotation_closure('file',same_path_pair('annotated-first',shape))))
# The two shapes are different KINDS of counterexample and the suite says which is which: the key
# order swap produces canonically EQUAL documents, so a verdict difference there could only ever be
# an implementation artifact; the container placement genuinely changes the document.
check('the-key-order-pair-is-canonically-identical-and-the-container-pair-is-not',
      C.canonical(same_path_pair('unannotated-first','keyorder'))
      ==C.canonical(same_path_pair('annotated-first','keyorder')) and
      C.canonical(same_path_pair('unannotated-first','container'))
      !=C.canonical(same_path_pair('annotated-first','container')))
# A THIRD sighting arriving annotated AFTER a missing one must not rehabilitate the path: the
# monotonic fact is not undone by any later arrival, wherever among the three the missing one sits.
# The suite asserts all three positions, so a fix that only handled "first arrival missing" fails.
def three_sightings_with_one_missing(position):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    first={'representation':'raw-artifact','retention':'not-joined','authority':'test','reason':'control'}
    bare={'$ref':'#/$defs/DigestHex'}
    nodes=[dict(bare,**{'x-opensip-digest':first}),dict(bare,**{'x-opensip-digest':first}),dict(bare)]
    nodes.insert(position,nodes.pop(2))
    # THREE schemas on ONE path: a two-level $ref chain, each level contributing properties.leaf,
    # plus the field's own local refinement. An allOf branch would NOT do - it gets its own path, so
    # it would be a different sighting rather than a third arrival at the same one.
    document['$defs']['ProbeInnerV1']={'type':'object','properties':{'leaf':nodes[0]}}
    document['$defs']['ProbeOuterV1']={'$ref':'#/$defs/ProbeInnerV1','properties':{'leaf':nodes[1]}}
    document['$defs']['FilePayloadV1']['properties']['probe']={
        '$ref':'#/$defs/ProbeOuterV1','properties':{'leaf':nodes[2]}}
    return M.relation_annotation_closure('file',document)
for _position in (0,1,2):
    rejects_because('a-later-annotated-sighting-does-not-rehabilitate-a-missing-one-at-'+str(_position),
        lambda position=_position:three_sightings_with_one_missing(position),
        'RELATION_DIGEST_UNANNOTATED:file:file.probe.leaf')
# The positive control for the whole family: the SAME three-way shape with every sighting annotated
# and agreeing admits, so the refusals above are caused by the missing annotation and by nothing
# else about reaching one path several times.
def three_sightings_all_annotated():
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    annotation={'representation':'raw-artifact','retention':'not-joined','authority':'test','reason':'control'}
    marked=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':annotation})
    document['$defs']['ProbeInnerV1']={'type':'object','properties':{'leaf':marked}}
    document['$defs']['ProbeOuterV1']={'$ref':'#/$defs/ProbeInnerV1','properties':{'leaf':marked}}
    document['$defs']['FilePayloadV1']['properties']['probe']={
        '$ref':'#/$defs/ProbeOuterV1','properties':{'leaf':marked}}
    return M.relation_annotation_closure('file',document)
check('but-three-agreeing-annotated-sightings-at-one-path-still-admit',
      three_sightings_all_annotated() is not None)
# The merged list is kept ALONGSIDE the missing fact rather than replaced by it, which is what keeps
# "no new annotation" distinguishable from "already merged" and leaves a conflict diagnosable.
check('the-missing-fact-and-the-merged-list-are-separate-facts',
      all({'missing','annotations'}<=set(s)
          for s in M.relation_digest_annotation_coverage()['byRelation']['file']['sightings']))
# THE INDEPENDENT REVIEWER'S p10 TYPED-EQUALITY COLLAPSE, closed. Annotation equality is TYPED
# CANONICAL equality, which is what the contract says and what the conflict limb always used - but
# collection and alias inheritance still compared with Python `not in`. `1 == True` is true while
# C({...ordinal: 1}) and C({...ordinal: true}) are DIFFERENT registered bytes, so a typed-distinct
# annotation was dropped during collection and the conflict check never saw the pair: both
# orientations admitted and only one annotation survived. Every stage now routes through
# M.annotation_already_collected, so no early stage can silently collapse them.
TYPED_PAIRS=[('int-vs-true',1,True),('int-vs-false',0,False),
             ('nested-dict',{'k':1},{'k':True}),('nested-list',[1],[True]),
             ('deep-nested',{'a':{'b':[0]}},{'a':{'b':[False]}})]
def typed_annotation(value):
    return {'representation':'raw-artifact','retention':'not-joined','authority':'test',
            'reason':'a control, not a shipped field','ordinal':value}
TYPED_LOCATIONS=('property-alias','alias-chain','parent-nullable-branch',
                 'enclosing-container','container-ref-overlay','same-path-merge')
def typed_pair_document(location,first,second):
    """The SAME governed leaf reached twice, each arrival carrying one of a typed-distinct pair.

    Every supported propagation class, so this proves no stage collapses the pair rather than only
    the one the reviewer exercised. `property-alias` is the reviewer's own shape. Measured against
    frozen v11, the three EARLY-COLLECTION classes discriminate - `property-alias` through the
    ref-chain filter, `parent-nullable-branch` and `enclosing-container` through the inherited filter
    - while the three that reach record() as separate arrivals already behaved, because that merge
    already used typed equality. Keeping all six is what shows the rule is now uniform rather than
    patched at one site."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    bare={'$ref':'#/$defs/DigestHex'}
    a,b=typed_annotation(first),typed_annotation(second)
    selector=document['$defs']['FilePayloadV1']['properties']
    if location=='property-alias':
        document['$defs']['TypedAliasV1']=dict(bare,**{'x-opensip-digest':b})
        selector['probe']=dict({'$ref':'#/$defs/TypedAliasV1'},**{'x-opensip-digest':a})
    elif location=='alias-chain':
        document['$defs']['TypedAliasV2']=dict(bare,**{'x-opensip-digest':b})
        document['$defs']['TypedAliasV1']=dict({'$ref':'#/$defs/TypedAliasV2'},**{'x-opensip-digest':a})
        selector['probe']={'$ref':'#/$defs/TypedAliasV1'}
    elif location=='enclosing-container':
        # The annotation sits on the CONTAINER, so it reaches the leaf through `inherited` - an
        # early-collection arrival, not a second sighting. This is the class an earlier revision of
        # this matrix missed: what it called `enclosing-container` was the ref-overlay below, which
        # is a merge of two separate arrivals and therefore never exercised the inherited filter.
        selector['probe']={'type':'object','x-opensip-digest':a,
                           'properties':{'leaf':dict(bare,**{'x-opensip-digest':b})}}
    elif location=='container-ref-overlay':
        document['$defs']['TypedContainerV1']={'type':'object',
            'properties':{'leaf':dict(bare,**{'x-opensip-digest':b})}}
        selector['probe']={'$ref':'#/$defs/TypedContainerV1',
                           'properties':{'leaf':dict(bare,**{'x-opensip-digest':a})}}
    elif location=='same-path-merge':
        document['$defs']['TypedInnerV1']={'type':'object',
            'properties':{'leaf':dict(bare,**{'x-opensip-digest':b})}}
        document['$defs']['TypedOuterV1']={'$ref':'#/$defs/TypedInnerV1',
            'properties':{'leaf':dict(bare,**{'x-opensip-digest':a})}}
        selector['probe']={'$ref':'#/$defs/TypedOuterV1'}
    else:
        selector['probe']={'x-opensip-digest':a,
                           'oneOf':[dict(bare,**{'x-opensip-digest':b}),{'type':'null'}]}
    return document
for _location in TYPED_LOCATIONS:
    for _label,_first,_second in TYPED_PAIRS:
        for _orientation in (0,1):
            _pair=(_first,_second) if _orientation==0 else (_second,_first)
            rejects_because('a-typed-distinct-'+_label+'-pair-at-the-'+_location+'-location-conflicts-'+str(_orientation),
                lambda location=_location,pair=_pair:M.relation_annotation_closure(
                    'file',typed_pair_document(location,*pair)),
                'RELATION_DIGEST_ANNOTATION_CONFLICT:file:')
# Neither orientation may admit, and BOTH annotations must survive collection so the conflict limb
# can see them - the defect was that one silently disappeared before the check.
check('both-typed-distinct-annotations-survive-collection-at-every-location',
      all(len([x for x in M.relation_digest_annotation_coverage(
                   typed_pair_document(location,first,second))['byRelation']['file']['sightings']
               if 'probe' in x['path']][0]['annotations'])==2
          for location in TYPED_LOCATIONS
          for _l,first,second in TYPED_PAIRS))
# POSITIVE CONTROLS. Identical annotations - including ones carrying the SAME typed value, nested or
# not - are not a conflict; if they were, this "fix" would just be rejecting every alias and branch.
for _label,_first,_second in TYPED_PAIRS:
    for _location in TYPED_LOCATIONS:
        check('identical-'+_label+'-annotations-at-the-'+_location+'-location-still-admit',
              M.relation_annotation_closure('file',typed_pair_document(_location,_first,_first)) is not None)
check('and-the-shipped-document-is-still-coherent-for-every-relation',
      all(M.relation_annotation_closure(name) is not None for name in M.RELATIONS))
# The rule itself: one helper, typed canonical equality, and Python equality is NOT it.
check('annotation-equality-is-typed-canonical-not-python-equality',
      all((typed_annotation(a)==typed_annotation(b)) and
          (not C.equal_typed(typed_annotation(a),typed_annotation(b))) and
          C.canonical(typed_annotation(a))!=C.canonical(typed_annotation(b)) and
          M.annotation_already_collected(typed_annotation(a),[typed_annotation(a)]) and
          not M.annotation_already_collected(typed_annotation(a),[typed_annotation(b)])
          for _l,a,b in TYPED_PAIRS))
# And an ordinary disagreeing pair still conflicts, so the typed rule did not replace the plain one.
check('an-ordinary-disagreeing-pair-still-conflicts',
      not_admitted(lambda:M.relation_annotation_closure('file',(lambda d:(
          d['$defs'].__setitem__('TypedAliasV1',dict({'$ref':'#/$defs/DigestHex'},
              **{'x-opensip-digest':dict(typed_annotation(1),authority='other')})),
          d['$defs']['FilePayloadV1']['properties'].__setitem__('probe',
              dict({'$ref':'#/$defs/TypedAliasV1'},**{'x-opensip-digest':typed_annotation(1)})),
          d)[-1])(copy.deepcopy(M.RELATION_DOCUMENT)))))
check('the-three-limbs-report-three-distinct-causes',
      len({'RELATION_DIGEST_UNANNOTATED','RELATION_DIGEST_LAW_RESIDUE','RELATION_JOIN_FIELD_UNKNOWN'})==3)
check('the-pre-rename-path-is-the-one-declared-not-joined-exemption',
      M.RELATION_DOCUMENT['$defs']['VcsChangePayloadV1']['properties']['previousPath']
       ['x-opensip-digest']['retention']=='not-joined' and
      M.RELATIONS['vcs-change']['snapshotJoins'][0]['unless']=={'field':'changeKind','equals':'deleted'})
check('fact-identity-and-body-identity-are-never-equated',
      'never equal or substitute' in json.dumps(FACT_IDENTITY_POLICY['factRecordIdentityBoundaryV1']) and
      M.RELATION_DOCUMENT['$defs']['ClonesPayloadV1']['properties']['bodyIdentity']['x-opensip-digest']
       ['neverEquals'].startswith('FACT-ID-V1'))
check('the-body-frame-grammar-is-the-inherited-one-not-a-restatement',
      FACT_IDENTITY_POLICY['canonicalisationSchema']['byteGrammar']['levelVersionDefinition'].startswith(
          'raw 32-byte SHA-256 content digest of the canonical level specification') and
      M.RELATIONS['clones']['bodyIdentityJoin']['inheritedFrom'].startswith(
          'docs/coop/artifacts/fact-identity-policy.v2.json#/canonicalisationSchema'))

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
