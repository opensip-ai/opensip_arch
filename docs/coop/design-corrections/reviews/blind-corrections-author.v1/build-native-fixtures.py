"""Disposable: build the M-1 / M-2 fixtures and print the exact expected values for native-cases.v2.json."""
import hashlib, importlib.util, json, sys
from pathlib import Path
R = Path(sys.argv[1])
N = R / 'docs/coop/design-corrections/native'
spec = importlib.util.spec_from_file_location('m', N / 'native_evidence_model.v2.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

h = lambda s: hashlib.sha256(s.encode()).hexdigest()

# ---- retained closures (trusted admitted inputs) -------------------------------------------------
LIBS = ['lib.es2022.d.ts', 'lib.dom.d.ts', 'lib.decorators.d.ts']
stdlib = {'schemaVersion': 2, 'kind': 'stdlib', 'manifestDigest': h('ts-stdlib-manifest'),
          'tree': sorted(({'path': 'lib/' + n, 'sha256': h('stdlib/' + n), 'bytes': 4096 + i} for i, n in enumerate(LIBS)),
                         key=lambda b: b['path'].encode()),
          'semanticVersion': '5.6.3', 'protocolMajor': 2, 'platform': 'any'}
stdlib_id = M.IM.identifier('closure', stdlib)

tools = {'schemaVersion': 2, 'kind': 'toolchain', 'manifestDigest': h('ts-toolchain-manifest'),
         'tree': sorted(({'path': p, 'sha256': h(p), 'bytes': b} for p, b in
                         (('bin/node', 90000000), ('lib/tsc.js', 8000000), ('package/typescript.tgz', 12000000))),
                        key=lambda b: b['path'].encode()),
         'semanticVersion': '5.6.3', 'protocolMajor': 2, 'platform': 'linux-x86_64-gnu'}
tools_id = M.IM.identifier('closure', tools)

rustdev = {'schemaVersion': 2, 'kind': 'rust-dev-llvm', 'manifestDigest': h('rust-dev-llvm-manifest'),
           'tree': [{'path': 'lib/librustc_driver.so', 'sha256': h('librustc_driver'), 'bytes': 180000000}],
           'semanticVersion': '1.83.0', 'protocolMajor': 3, 'platform': 'linux-x86_64-gnu'}
rustdev_id = M.IM.identifier('closure', rustdev)

closure_trees = {stdlib_id: stdlib, tools_id: tools, rustdev_id: rustdev}

toolchain = {'compilerName': 'typescript', 'compilerVersion': '5.6.3',
             'compilerPackageDigest': h('package/typescript.tgz'),
             'typescriptStdlibMerkleRoot': stdlib_id.removeprefix('closure2:'),
             'standardLibraryComponentDigests': sorted(({'component': n, 'sha256': h('stdlib/' + n)} for n in LIBS),
                                                       key=lambda c: c['component'].encode()),
             'libSelection': ['DOM', 'ES2022']}
tool_closure = {'compiler': h('lib/tsc.js'), 'runtime': h('bin/node'), 'closureId': tools_id}
config_projection = {
    'schemaVersion': 2, 'ancestorCarrierVerified': True, 'environmentSanitized': True,
    'typeAcquisitionEnabled': False, 'executableSelected': False,
    'honoredOptions': {'allowJs': False, 'checkJs': False, 'module': 'node16', 'moduleResolution': 'node16',
                       'target': 'es2022', 'strict': True, 'skipLibCheck': True, 'noEmit': True,
                       'types': None, 'lib': ['DOM', 'ES2022'], 'baseUrl': None, 'paths': [],
                       'rootDirs': [], 'resolveJsonModule': True, 'allowSyntheticDefaultImports': True,
                       'esModuleInterop': True, 'customConditions': [], 'jsx': None},
    'strippedOptions': [{'option': 'outDir', 'reason': 'emits-output'},
                        {'option': 'typeAcquisition', 'reason': 'acquires-types-from-the-network'}],
    'configGraphPaths': ['tsconfig.base.json', 'tsconfig.json']}
ctx = M.typescript_native_context(toolchain, tool_closure, config_projection, 'ts-tsconfig',
                                  'node16', 'module', h('node_modules-layout'),
                                  {'kind': 'package-lock', 'path': 'package-lock.json', 'contentSha256': h('package-lock')})
adm = M.admit_native_context('typescript', ctx, closure_trees)

universe = {
    'schemaVersion': 2, 'languageMode': 'ts-tsconfig', 'configOrigin': 'tsconfig', 'synthesizerVersion': None,
    'synthesizedOptions': None, 'packageModuleType': 'module', 'allowJs': False, 'checkJs': False,
    'jsAdmittedToProgram': False, 'jsDiagnosticsEnabled': False, 'resolutionCompletenessImplied': False,
    'jsRootFiles': [], 'programRootFiles': ['src/a.ts', 'src/b.ts'], 'lockfileKind': 'package-lock',
    'nodeModulesInReadSet': True, 'executionCapableResolution': False,
    'tsconfigGraphHash': h('tsconfig-graph'), 'nativeContextId': adm['nativeContextId']}
bound = M.bind_typescript_universe(universe, adm)

out = {
    'closures': {'stdlib': stdlib, 'tools': tools, 'rustdev': rustdev},
    'closureIds': {'stdlib': stdlib_id, 'tools': tools_id, 'rustdev': rustdev_id},
    'tsContext': ctx, 'admission': adm, 'universe': universe, 'bound': bound,
}

# stdlib change / compiler change propagation
ctx_stdlib = json.loads(json.dumps(ctx))
new_stdlib = json.loads(json.dumps(stdlib))
new_stdlib['tree'][2]['sha256'] = h('stdlib/lib.es2022.d.ts@next')
new_stdlib_id = M.IM.identifier('closure', new_stdlib)
ctx_stdlib['toolchain']['typescriptStdlibMerkleRoot'] = new_stdlib_id.removeprefix('closure2:')
ctx_stdlib['toolchain']['standardLibraryComponentDigests'] = sorted(
    ({'component': b['path'].rpartition('/')[2], 'sha256': b['sha256']} for b in new_stdlib['tree']),
    key=lambda c: c['component'].encode())
adm_stdlib = M.admit_native_context('typescript', ctx_stdlib, dict(closure_trees, **{new_stdlib_id: new_stdlib}))
out['stdlibChanged'] = {'closure': new_stdlib, 'closureId': new_stdlib_id, 'context': ctx_stdlib, 'admission': adm_stdlib}

ctx_compiler = json.loads(json.dumps(ctx))
new_tools = json.loads(json.dumps(tools)); new_tools['semanticVersion'] = '5.7.2'
new_tools['tree'] = sorted([{'path': 'bin/node', 'sha256': h('bin/node'), 'bytes': 90000000},
                            {'path': 'lib/tsc.js', 'sha256': h('lib/tsc.js@5.7.2'), 'bytes': 8300000},
                            {'path': 'package/typescript.tgz', 'sha256': h('package/typescript.tgz@5.7.2'), 'bytes': 12400000}],
                           key=lambda b: b['path'].encode())
new_tools_id = M.IM.identifier('closure', new_tools)
ctx_compiler['toolchain']['compilerVersion'] = '5.7.2'
ctx_compiler['toolchain']['compilerPackageDigest'] = h('package/typescript.tgz@5.7.2')
ctx_compiler['toolClosure'] = {'compiler': h('lib/tsc.js@5.7.2'), 'runtime': h('bin/node'), 'closureId': new_tools_id}
adm_compiler = M.admit_native_context('typescript', ctx_compiler, dict(closure_trees, **{new_tools_id: new_tools}))
out['compilerChanged'] = {'closure': new_tools, 'closureId': new_tools_id, 'context': ctx_compiler, 'admission': adm_compiler}

# malformed: merkle root is not a retained closure suffix
ctx_bad = json.loads(json.dumps(ctx)); ctx_bad['toolchain']['typescriptStdlibMerkleRoot'] = h('not-a-closure')
out['malformed'] = M.admit_native_context('typescript', ctx_bad, closure_trees)
# mismatched: a tool digest outside the named closure tree
ctx_tool = json.loads(json.dumps(ctx)); ctx_tool['toolClosure']['compiler'] = h('some/other/tsc.js')
out['toolMismatch'] = M.admit_native_context('typescript', ctx_tool, closure_trees)
# mismatched: stdlib component digest disagrees with the retained tree
ctx_tree = json.loads(json.dumps(ctx)); ctx_tree['toolchain']['standardLibraryComponentDigests'][0]['sha256'] = h('tampered')
out['treeMismatch'] = M.admit_native_context('typescript', ctx_tree, closure_trees)
# fake Rust context offered as a TypeScript one
rust_ctx = {'schemaVersion': 2, 'targetTriple': 'x86_64-unknown-linux-gnu', 'hostTriple': 'x86_64-unknown-linux-gnu',
            'toolchain': {'rustCommitHash': 'a' * 40, 'rustcVersion': '1.83.0', 'cargoVersion': '1.83.0',
                          'sysrootDigest': h('sysroot'), 'rustcDevLlvmDigest': rustdev_id.removeprefix('closure2:'),
                          'standardLibraryComponentDigests': [{'component': 'libstd.rlib', 'sha256': h('libstd')}],
                          'targetTriple': 'x86_64-unknown-linux-gnu'},
            'toolClosure': {'rustc': h('rustc'), 'cargo': h('cargo'), 'linker': h('ld'), 'ar': h('ar'),
                            'procMacroServer': h('pms'), 'closureId': tools_id},
            'baseCfg': ['target_arch="x86_64"'], 'resolverVersion': 2,
            'dependencySourceSetId': 'sha256:' + h('dss'), 'unifiedFeaturesId': 'sha256:' + h('uf'),
            'preparedOutputSetId': None,
            'configProjection': None}
out['rustContextSkeleton'] = rust_ctx
print(json.dumps(out, indent=1))
