"""Complete positive TypeScript Run.

Exhibited properties (all on THIS exported Run):
  R-RUN-TS                          TS universe/fact/Coverage path
  R-RUN-TS-NODE-MODULES             ordinary project that reads node_modules and resolves
                                    bare specifiers (retained ResolvedNodeModulesLayoutV1 +
                                    nodeModulesInReadSet + imports@resolved-target on a bare
                                    specifier)
  R-RUN-TS-CONFIG-DEPS              retained configuration graph (multi-node extends) and
                                    dependency layout preimages
  R-RUN-NONCEMPTY-CONTEXT           plan.nativeContextDigests nonempty and retained
  R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC  a real ScopeDocumentV1 bound as the registered
                                    analysis-spec parameter row
  R-IMPORTED-PAYLOAD-IN-GRAPH       actual import2 wrapper + RuntimePayloadV1 as graph
                                    members, beside registered relation facts and native
                                    Coverage
  R-JS-CLONE-BODY-THROUGH-TS        a JavaScript clone body through the TypeScript analyzer
                                    universe (body language != provider identity)
  R-NATIVE-PREIMAGE-JOINS           config-graph and node_modules-layout H/record preimages

Every byte is a synthetic trusted observation of this origin.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import opensip_capmanifest as CM

PROJECT_ID = 'prj1-' + '7c1d9e4fa2b86035cd17e2f4a5b6c7d8e9f0a1b2c3d4e5f60718293a4b5c6d7e8'[:64]

TS_BASE = b'{"compilerOptions":{"target":"es2022","strict":true,"noEmit":true}}\n'
TS_ROOT = b'{"extends":["./tsconfig.base.json"],"compilerOptions":{"allowJs":true},"include":["src"]}\n'
PKG = b'{"name":"app","version":"1.0.0","type":"module","dependencies":{"left-pad":"^1.3.0"}}\n'
LOCK = b'{"lockfileVersion":3,"packages":{"node_modules/left-pad":{"version":"1.3.0"}}}\n'
INDEX_TS = (b'import pad from "left-pad";\nimport { pad2 } from "./util";\n'
            b'export function main(n: number) { return pad(String(n), 4); }\n')
UTIL_TS = b'export function pad2(s: string) { return s.padStart(2, "0"); }\n'
LEGACY_JS = b'export function pad2(s) { return s.padStart(2, "0"); }\n'

FILES = {
    'package-lock.json': LOCK,
    'package.json': PKG,
    'src/index.ts': INDEX_TS,
    'src/legacy.js': LEGACY_JS,
    'src/util.ts': UTIL_TS,
    'tsconfig.base.json': TS_BASE,
    'tsconfig.json': TS_ROOT,
}
# node_modules bytes are RETAINED but deliberately NOT snapshot-inventoried: the file
# membership extent law excludes them (reason host-ignore-convention) and the package kind
# is first-party manifests only. They enter the graph through the resolved layout record.
NODE_MODULES = {
    'node_modules/left-pad/package.json': b'{"name":"left-pad","version":"1.3.0"}\n',
    'node_modules/left-pad/index.d.ts': b'declare function pad(s: string, n: number): string;\nexport default pad;\n',
}

L0_SPEC = (b'opensip level specification\nlevel: L0-verbatim\n'
           b'lexical-boundary: none (tokenisation forbidden)\n'
           b'token-kind-registry: none\ndirective-classification: none\n'
           b'transform-order: []\nreplacement-bytes: none\n'
           b'languages: typescript javascript\n')

TS_BODY = b'{ return s.padStart(2, "0"); }'

MUTATE = {}   # negative-control hook; applied at BUILD time so the graph is reminted

# The section 1.2 mode of record for this subject, shared with the enumeration cells so the
# cell languageMode, the WorkspaceUnitV2 languageMode and the context/universe all agree.
LANGUAGE_MODE_OF_RECORD = 'js-allowjs'


def build():
    b = B.Builder(PROJECT_ID)
    st = b.st
    for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.POLICY_V2_DOC, B.POLICY_V1_DOC,
              B.ENUM_PLAN_DOC, B.EMIT_PLAN_DOC, B.SUBJ_INV_DOC, B.EXEC_IN_DOC,
              B.IMPORTED_DOC, B.COMMON_DOC):
        b.retain_schema_doc(d)

    # ---------------------------------------------------------------- closures
    TSC = b'\x7fELF-synthetic-tsc-5.6.2'
    NODE = b'\x7fELF-synthetic-node-22'
    TSPKG = b'synthetic-typescript-package-5.6.2'
    tool_tid, tool_rec, _ = b.closure(
        'toolchain', '5.6.2', 3, 'macos-aarch64',
        [('node_modules/typescript/lib/tsc.js', TSC), ('bin/node', NODE),
         ('node_modules/typescript/package.json', TSPKG)],
        'opensip-typescript-toolchain')
    LIBS = {'lib/lib.dom.d.ts': b'// synthetic lib.dom.d.ts\n',
            'lib/lib.es2022.d.ts': b'// synthetic lib.es2022.d.ts\n',
            'lib/lib.es5.d.ts': b'// synthetic lib.es5.d.ts\n'}
    stdlib_tid, stdlib_rec, _ = b.closure(
        'stdlib', '5.6.2', 3, 'macos-aarch64', sorted(LIBS.items()),
        'opensip-typescript-stdlib')
    provider_tid, provider_rec, _ = b.closure(
        'provider', '2.4.0', 3, 'macos-aarch64',
        [('bin/opensip-ts-provider', b'\x7fELF-synthetic-typescript-provider')],
        'opensip-typescript-provider')
    evaluator_tid, _, _ = b.closure(
        'evaluator', '3.0.0', 3, 'macos-aarch64',
        [('bin/opensip-evaluator', b'\x7fELF-synthetic-pure-evaluator')],
        'opensip-evaluator')
    detector_tid, _, _ = b.closure(
        'detector', '1.4.0', 3, 'macos-aarch64',
        [('rules/ts-hygiene.json', b'{"detector":"ts-hygiene","rev":9}')],
        'opensip-ts-hygiene-detector')
    adapter_tid, _, _ = b.closure(
        'adapter', '1.0.1', 3, 'macos-aarch64',
        [('bin/opensip-v8-coverage-adapter', b'\x7fELF-synthetic-v8-adapter')],
        'opensip-v8-coverage-adapter')
    import_producer_tid, _, _ = b.closure(
        'provider', '1.0.0', 3, 'macos-aarch64',
        [('bin/opensip-runtime-capture', b'\x7fELF-synthetic-runtime-capture')],
        'opensip-runtime-capture')

    # ---------------------------------------------------------------- snapshot
    config = {
        'analysis': {'profileId': 'ts-default',
                     'capabilities': sorted(['inventory', 'syntax', 'imports',
                                             'clones-fact'], key=lambda s: K.C(s)),
                     'budget': {'unit': 'work-units', 'limit': 20000000}},
        'components': {'request': [{'stableId': '22222222-3333-4444-8555-666666666666',
                                    'version': '5.6.2'}],
                       'allowedScopes': ['project', 'global']},
        'discovery': {'workspaceRoots': ['.'], 'ignorePaths': ['node_modules']},
        'policy': {'packIds': ['pack.ts-hygiene']},
        'evidence': {},
    }
    scope_desc = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': [],
                  'excludedPathPrefixes': ['node_modules']}
    snapshot_id, snapshot, sh = b.snapshot(
        FILES, config, scope_desc, vcs_kind='git',
        commit_id='a1b2c3d4e5f60718293a4b5c6d7e8f9012345678', dirty=False)
    for p, by in NODE_MODULES.items():
        st.put_blob(by, label='node_modules:' + p)
    st.put_blob(L0_SPEC, label='level-spec:L0-verbatim')

    # ---------------------------------------------------------------- native context
    layout = {'schemaVersion': 1, 'entries': sorted([
        {'packageName': 'left-pad', 'packageVersion': '1.3.0',
         'installPath': 'node_modules/left-pad/package.json',
         'realPath': 'node_modules/left-pad/package.json',
         'contentSha256': K.raw_sha256(NODE_MODULES['node_modules/left-pad/package.json'])},
        {'packageName': 'left-pad', 'packageVersion': '1.3.0',
         'installPath': 'node_modules/left-pad/index.d.ts',
         'realPath': 'node_modules/left-pad/index.d.ts',
         'contentSha256': K.raw_sha256(NODE_MODULES['node_modules/left-pad/index.d.ts'])},
    ], key=lambda e: K.C(e))}
    layout_dig = b.record(B.NATIVE_DOC, '#/$defs/ResolvedNodeModulesLayoutV1', layout,
                          'node-modules-layout')

    honored = {
        'allowJs': True, 'checkJs': False,
        'allowSyntheticDefaultImports': True, 'esModuleInterop': True,
        'resolveJsonModule': False, 'baseUrl': None, 'customConditions': [],
        'jsx': None, 'lib': ['dom', 'es2022'], 'module': 'es2022',
        'moduleResolution': 'nodenext', 'noEmit': True, 'paths': [], 'rootDirs': [],
        'skipLibCheck': False, 'strict': True, 'target': 'es2022', 'types': None,
    }
    config_projection = {
        'schemaVersion': 2, 'ancestorCarrierVerified': True,
        'environmentSanitized': True, 'typeAcquisitionEnabled': False,
        'executableSelected': False, 'honoredOptions': honored,
        'strippedOptions': [{'option': 'outDir', 'reason': 'emits-output'},
                            {'option': 'typeRoots', 'reason':
                             'acquires-types-from-the-network'}],
        'configGraphPaths': sorted(
            ['tsconfig.json', 'tsconfig.base.json']
            + (['tsconfig.not-in-snapshot.json']
               if MUTATE.get('configGraphPath-outside-snapshot') else []),
            key=lambda s: s.encode()),
    }
    lib_rows = sorted([{'component': os.path.basename(p), 'sha256': K.raw_sha256(by)}
                       for p, by in LIBS.items()], key=lambda r: r['component'].encode())
    # a digest that IS globally retained but is NOT a member of the named closure tree
    NON_TREE_BUT_RETAINED = K.raw_sha256(LOCK)
    if MUTATE.get('libComponent-not-in-tree'):
        lib_rows = sorted([dict(r, sha256=NON_TREE_BUT_RETAINED)
                           if r['component'] == 'lib.dom.d.ts' else r for r in lib_rows],
                          key=lambda r: r['component'].encode())
    toolchain = {
        'compilerName': 'typescript', 'compilerVersion': tool_rec['semanticVersion'],
        'compilerPackageDigest': (NON_TREE_BUT_RETAINED
                                  if MUTATE.get('compilerPackageDigest-not-in-tree')
                                  else K.raw_sha256(TSPKG)),
        'typescriptStdlibMerkleRoot': (st.suffix(tool_tid)
                                       if MUTATE.get('stdlibMerkleRoot-wrong-kind')
                                       else st.suffix(stdlib_tid)),
        'standardLibraryComponentDigests': lib_rows,
        'libSelection': sorted(['dom', 'es2022'], key=lambda s: s.encode()),
    }
    # native-evidence section 1.2: `ts-tsconfig` requires `allowJs` absent/false and states
    # that "JavaScript files are not program roots". This subject has tsconfig.json with
    # allowJs:true and admits src/legacy.js as a program root, so its mode IS `js-allowjs`.
    # (The clause-to-implementation audit refused the earlier `ts-tsconfig` label here:
    # section1.2:TS_TSCONFIG_REQUIRES_ALLOWJS_ABSENT_OR_FALSE and
    # section1.2:TS_TSCONFIG_JAVASCRIPT_FILES_ARE_NOT_PROGRAM_ROOTS.)
    LANGUAGE_MODE = LANGUAGE_MODE_OF_RECORD
    ctx = {'schemaVersion': 2, 'languageMode': LANGUAGE_MODE, 'toolchain': toolchain,
           'toolClosure': {'closureId': tool_tid, 'compiler': K.raw_sha256(TSC),
                           'runtime': K.raw_sha256(NODE)},
           'configProjection': config_projection, 'moduleResolutionMode': 'nodenext',
           'packageModuleType': 'module', 'nodeModulesLayoutDigest': layout_dig,
           'lockfileIdentity': {'kind': 'package-lock', 'path': 'package-lock.json',
                                'contentSha256': (K.raw_sha256(PKG)
                                                  if MUTATE.get('lockfile-digest-mismatch')
                                                  else K.raw_sha256(LOCK))}}
    ctx_hex = b.native_framed('native.context.typescript.v2', B.NATIVE_DOC,
                              '#/$defs/TypeScriptNativeContextV2', ctx,
                              'native-context:typescript')

    config_graph = {'schemaVersion': 1, 'entryConfigPath': 'tsconfig.json',
                    'nodes': sorted([
                        {'path': 'tsconfig.json', 'contentSha256': K.raw_sha256(TS_ROOT),
                         'kind': 'tsconfig', 'extendsResolved': ['tsconfig.base.json']},
                        {'path': 'tsconfig.base.json',
                         'contentSha256': K.raw_sha256(TS_BASE),
                         'kind': 'tsconfig', 'extendsResolved': []},
                    ], key=lambda n: n['path'].encode())}
    cg_dig = b.record(B.NATIVE_DOC, '#/$defs/TypeScriptConfigGraphV1', config_graph,
                      'ts-config-graph')
    universe = {
        'schemaVersion': 2, 'languageMode': LANGUAGE_MODE, 'configOrigin': 'tsconfig',
        'synthesizerVersion': None, 'synthesizedOptions': None,
        'packageModuleType': 'module', 'allowJs': True, 'checkJs': False,
        'jsAdmittedToProgram': True, 'jsDiagnosticsEnabled': False,
        'resolutionCompletenessImplied': False,
        'jsRootFiles': ['src/legacy.js'],
        'programRootFiles': ['src/index.ts', 'src/legacy.js', 'src/util.ts'],
        'lockfileKind': 'package-lock', 'nodeModulesInReadSet': True,
        'executionCapableResolution': False, 'tsconfigGraphHash': cg_dig,
        'nativeContextId': 'sha256:' + ctx_hex,
    }
    uni_hex = b.native_framed('native.semantic-universe.typescript.v2', B.NATIVE_DOC,
                              '#/$defs/TypeScriptUniverseV2ResolvedInputs', universe,
                              'native-universe:typescript')

    # ---------------------------------------------------------------- capability manifest
    A = CM.CapabilityManifestAdmitter()
    cap = {'schemaVersion': 1, 'profile': 'ts-default',
           'providers': [{'providerId': 'opensip.provider.typescript',
                          'language': 'typescript',
                          'providerVersionSource': 'closure2.semanticVersion',
                          'toolchainIdentitySource': 'TypeScriptToolchainIdentityV1',
                          'relations': {'file': 'enumerated',
                                        'package': 'manifest-declared',
                                        'vcs-change': 'vcs-reported',
                                        'declares': 'syntactic', 'literal': 'syntactic',
                                        'control-flow': 'syntactic',
                                        'clones': 'normalized-body-hash',
                                        'imports': 'resolved-target',
                                        'references': 'resolved-binding',
                                        'calls': 'resolved-callee', 'types': 'checked',
                                        'reachability': 'from-resolved-calls',
                                        'unresolved-edge': 'observed'},
                          'platformIds': ['macos-aarch64']}],
           'coverageForAbsent': []}
    capres = A.admit(cap)
    assert capres['admitted']
    st.put_blob(capres['committedBytes'], label='capability-manifest-artifact')

    # ---------------------------------------------------------------- body identities
    def blv_for(variant, language_id):
        rec = {'schemaVersion': 1, 'languageId': language_id,
               'compilerName': toolchain['compilerName'],
               'compilerVersion': toolchain['compilerVersion'],
               'compilerBuild': toolchain['compilerPackageDigest'],
               'dialect': {'sourceVariant': variant}}
        b.admit(B.IDENTITY_DOC, '#/$defs/body-language-version', rec,
                'body-language-version:' + variant)
        st.put_blob(K.C(rec), label='body-language-version:' + variant)
        return rec, bytes.fromhex(K.rec_digest(rec))

    blv_ts, lv_ts = blv_for('ts', 'typescript')
    blv_js, lv_js = blv_for('js', 'javascript')

    def clone_payload(level_id, spec_bytes, payload_bytes, language_id, lv_raw):
        frame = B.body_identity_frame(level_id, K.raw_sha256(spec_bytes), language_id,
                                     lv_raw, payload_bytes)
        bid = K.raw_sha256(frame)
        st.put_blob(frame, label='body-identity-frame:%s:%s' % (level_id, bid[:8]))
        return {'bodyIdentity': 'sha256:' + bid, 'normalisationLevel': level_id,
                'normalisationVersion': K.raw_sha256(spec_bytes)}, bid

    # ---------------------------------------------------------------- facts
    facts, fact_payloads = {}, {}

    def mk_fact(relation, rung, payload, anchors, label, confidence=1000000):
        fid = b.fact(snapshot_id, relation, rung, uni_hex, uni_hex, provider_tid,
                     payload, anchors, confidence, label)
        facts[fid] = st.objects[fid]
        fact_payloads[fid] = payload
        return fid

    def anchor(path, span):
        row = [r for r in sh['inventory'] if r['path'] == path][0]
        return {'path': path, 'blobDigest': row['sha256'],
                'startByte': span[0], 'endByte': span[1]}

    for p in sorted(FILES, key=lambda s: s.encode()):
        row = [r for r in sh['inventory'] if r['path'] == p][0]
        mk_fact('file', 'enumerated',
                {'path': p, 'contentSha256': row['sha256'], 'byteLength': row['bytes']},
                [], 'file:' + p)
    mk_fact('package', 'manifest-declared',
            {'packageName': 'app', 'packageVersion': '1.0.0',
             'manifestPath': 'package.json'}, [], 'package:app')
    SYMS = {'ts:src/index.ts#main': ('src/index.ts', 'main'),
            'ts:src/util.ts#pad2': ('src/util.ts', 'pad2'),
            'js:src/legacy.js#pad2': ('src/legacy.js', 'pad2')}
    for sid, (path, name) in sorted(SYMS.items()):
        src = FILES[path]
        mk_fact('declares', 'syntactic',
                {'container': sid.split('#')[0], 'declared': sid,
                 'declarationKind': 'function'},
                [anchor(path, (0, len(src) - 1))], 'declares:' + sid)
    # bare specifier resolved into node_modules, and a relative specifier
    i_src = INDEX_TS
    mk_fact('imports', 'resolved-target',
            {'importer': 'ts:src/index.ts#main', 'specifier': 'left-pad',
             'resolvedTarget': 'ts:node_modules/left-pad/index.d.ts'},
            [anchor('src/index.ts', (0, i_src.index(b'\n')))], 'imports:left-pad')
    mk_fact('imports', 'resolved-target',
            {'importer': 'ts:src/index.ts#main', 'specifier': './util',
             'resolvedTarget': 'ts:src/util.ts'},
            [anchor('src/index.ts', (i_src.index(b'\n') + 1,
                                    i_src.index(b'\n', i_src.index(b'\n') + 1)))],
            'imports:relative-util')
    # clone bodies: a TypeScript body and a JavaScript body through the SAME TS engine
    ts_span = (UTIL_TS.index(TS_BODY), UTIL_TS.index(TS_BODY) + len(TS_BODY))
    js_span = (LEGACY_JS.index(TS_BODY), LEGACY_JS.index(TS_BODY) + len(TS_BODY))
    idx_body = b'{ return pad(String(n), 4); }'
    idx_span = (INDEX_TS.index(idx_body), INDEX_TS.index(idx_body) + len(idx_body))
    p_ts, bid_ts = clone_payload('L0-verbatim', L0_SPEC, B.l0_payload(TS_BODY),
                                'typescript', lv_ts)
    p_js, bid_js = clone_payload('L0-verbatim', L0_SPEC, B.l0_payload(TS_BODY),
                                'javascript', lv_js)
    p_idx, bid_idx = clone_payload('L0-verbatim', L0_SPEC, B.l0_payload(idx_body),
                                  'typescript', lv_ts)
    mk_fact('clones', 'normalized-body-hash', p_ts, [anchor('src/util.ts', ts_span)],
            'clones:util-ts')
    mk_fact('clones', 'normalized-body-hash', p_js, [anchor('src/legacy.js', js_span)],
            'clones:legacy-js')
    mk_fact('clones', 'normalized-body-hash', p_idx, [anchor('src/index.ts', idx_span)],
            'clones:index-ts')

    # ---------------------------------------------------------------- scopes + coverage
    scopes, coverages, coverage_payloads = {}, {}, {}

    def mk_scope_cov(relation, rung, subjects, label, cov='complete', rc=None,
                     deficiency=None, native_cause=None, cw=None):
        sid = b.scope(snapshot_id, relation, rung, uni_hex, uni_hex, provider_tid,
                      subjects, label)
        scopes[sid] = st.objects[sid]
        ent = B.entry(cov, cw or B.closed_world_open(['synthetic trusted observation']),
                      deficiency=deficiency, native_cause=native_cause,
                      rc=rc or B.rc_not_applicable())
        cid = b.coverage(sid, ent, label)
        coverages[cid] = st.objects[cid]
        coverage_payloads[cid] = json.loads(
            st.get_blob(st.objects[cid]['payloadDigest']).decode())
        return sid, cid

    CODE = ['src/index.ts', 'src/legacy.js', 'src/util.ts']
    s_file, c_file = mk_scope_cov('file', 'enumerated', sorted(FILES), 'file-enumerated')
    s_pkg, c_pkg = mk_scope_cov('package', 'manifest-declared', ['app'], 'package-declared')
    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', sorted(SYMS), 'declares-syntactic')
    s_clone, c_clone = mk_scope_cov('clones', 'normalized-body-hash', CODE, 'clones-normalized')
    rc_resolved = {'state': 'complete', 'attempted': True, 'examinedExhaustive': True,
                   'stageTerminal': 'complete', 'unresolvedEdgeCount': 0,
                   'unresolvedEdgeClasses': []}
    cw_closed = {'exportsClosed': 'closed', 'entryPointsRecognized': 'all',
                 'nonliteralLoading': 'none', 'externalConsumers': 'none-declared',
                 'dynamicDispatch': 'resolved',
                 'reasons': ['package.json private-less but no published subpath in this '
                             'synthetic subject'],
                 'deadCodeRepairEligible': True}
    s_imp, c_imp = mk_scope_cov('imports', 'resolved-target', sorted(SYMS),
                                'imports-resolved', rc=rc_resolved, cw=cw_closed)
    return dict(b=b, st=st, snapshot_id=snapshot_id, snapshot=snapshot, sh=sh,
                closures=dict(tool=tool_tid, stdlib=stdlib_tid, provider=provider_tid,
                              evaluator=evaluator_tid, detector=detector_tid,
                              adapter=adapter_tid, importProducer=import_producer_tid),
                ctx_hex=ctx_hex, uni_hex=uni_hex, cap=cap, capres=capres, config=config,
                facts=facts, fact_payloads=fact_payloads, scopes=scopes,
                coverages=coverages, coverage_payloads=coverage_payloads,
                files=FILES, node_modules=NODE_MODULES, syms=SYMS, code=CODE,
                layout=layout, layout_dig=layout_dig, config_graph=config_graph,
                cg_dig=cg_dig, toolchain=toolchain, ctx=ctx, universe=universe,
                blv=dict(ts=blv_ts, js=blv_js), bodies=dict(ts=bid_ts, js=bid_js,
                                                            idx=bid_idx),
                l0_spec=L0_SPEC,
                view_parts=dict(scopes=[s_file, s_pkg, s_decl, s_clone, s_imp],
                                coverages=[c_file, c_pkg, c_decl, c_clone, c_imp]))


if __name__ == '__main__':
    g = build()
    print('snapshot', g['snapshot_id'])
    print('context ', g['ctx_hex'])
    print('universe', g['uni_hex'])
    print('facts   ', len(g['facts']), 'scopes', len(g['scopes']))
    print('admissions', len(g['b'].admissions),
          'all admitted', all(a['admitted'] for a in g['b'].admissions))
