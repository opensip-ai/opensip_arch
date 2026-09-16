"""R-ADVERTISED-MODE-PATHS -- every advertised language mode has a REPRESENTABLE analysis
path, with the chosen grammar documented.

native-evidence section 1.2 publishes a CLOSED mode table. For each of its modes this file
constructs the actual (native context, resolved-inputs universe) pair that mode requires,
admits both against their owning schemas, and executes the section 1.2 mode law from the kit
with the same closure code the complete Runs use. The table then states, per mode, whether
this origin ALSO exercised it end-to-end on a complete sealed Run -- those two claims are not
merged.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import mode_harness as MH

OUT = '/tmp/opensip-design-corrections/consumer-b.v16/output'
KIT = S.KIT

TS_BASE = b'{"compilerOptions":{"target":"es2022","strict":true,"noEmit":true}}\n'
TS_STRICT = b'{"extends":["./tsconfig.base.json"],"include":["src"]}\n'
JSCFG = b'{"extends":["./config.shared.json"],"compilerOptions":{"allowJs":true}}\n'
SHARED = b'{"compilerOptions":{"target":"es2020","checkJs":false}}\n'
IDX_TS = b'export const a: number = 1;\n'
IDX_JS = b'export const a = 1;\n'
CARGO = b'[package]\nname="app1"\nversion="0.1.0"\nedition="2021"\n'
MAIN_RS = b'fn main() { println!("x"); }\n'
DATA = b'{"k":1}\n'


def tool():
    return {'compilerName': 'typescript', 'compilerVersion': '5.6.2',
            'compilerPackageDigest': K.raw_sha256(b'synthetic-typescript-package-5.6.2'),
            'typescriptStdlibMerkleRoot': K.raw_sha256(b'synthetic-stdlib-root'),
            'standardLibraryComponentDigests':
                [{'component': 'lib.es2022.d.ts',
                  'sha256': K.raw_sha256(b'// synthetic lib.es2022.d.ts\n')}],
            'libSelection': ['es2022']}


def honored_options(**over):
    """The schema's honoredOptions object is CLOSED and fully required: every option is
    spelled, with an absent value written as null rather than omitted."""
    h = {'allowJs': False, 'checkJs': False, 'allowSyntheticDefaultImports': True,
         'esModuleInterop': True, 'resolveJsonModule': False, 'baseUrl': None,
         'customConditions': [], 'jsx': None, 'lib': ['es2022'], 'module': 'es2022',
         'moduleResolution': 'nodenext', 'noEmit': True, 'paths': [], 'rootDirs': [],
         'skipLibCheck': False, 'strict': True, 'target': 'es2022', 'types': None}
    h.update(over)
    return h


def ts_context(h, mode, graph_paths, honored):
    ctx = {'schemaVersion': 2, 'languageMode': mode, 'toolchain': tool(),
           'toolClosure': {'closureId': 'closure2:' + '0' * 64,
                           'compiler': K.raw_sha256(b'\x7fELF-synthetic-tsc-5.6.2'),
                           'runtime': K.raw_sha256(b'\x7fELF-synthetic-node-22')},
           'configProjection': {'schemaVersion': 2, 'ancestorCarrierVerified': True,
                                'environmentSanitized': True,
                                'typeAcquisitionEnabled': False,
                                'executableSelected': False,
                                'honoredOptions': honored, 'strippedOptions': [],
                                'configGraphPaths': graph_paths},
           'moduleResolutionMode': 'nodenext', 'packageModuleType': 'module',
           'nodeModulesLayoutDigest': None,
           'lockfileIdentity': None}
    return ctx


def admit_pair(h, dom_ctx, sel_ctx, ctx, dom_uni, sel_uni, uni, label):
    ctx_hex = h.native(dom_ctx, B.NATIVE_DOC, sel_ctx, ctx, 'ctx:' + label)
    uni = dict(uni)
    uni['nativeContextId'] = 'sha256:' + ctx_hex
    uni_hex = h.native(dom_uni, B.NATIVE_DOC, sel_uni, uni, 'uni:' + label)
    return ctx_hex, uni_hex, uni


def mode_ts_tsconfig():
    """ts-tsconfig: tsconfig.json at the unit root, allowJs absent/false, and JavaScript
    files are NOT program roots. Chosen grammar: the TypeScript compiler's own program --
    a compiler mode, so the bundled syntax grammars are not the analysis path here."""
    files = {'tsconfig.base.json': TS_BASE, 'tsconfig.json': TS_STRICT,
             'src/index.ts': IDX_TS}
    h = MH.Harness('prj1-mode-ts-tsconfig', files)
    graph = {'schemaVersion': 1, 'entryConfigPath': 'tsconfig.json',
             'nodes': [{'path': 'tsconfig.base.json',
                        'contentSha256': K.raw_sha256(TS_BASE), 'kind': 'other',
                        'extendsResolved': []},
                       {'path': 'tsconfig.json', 'contentSha256': K.raw_sha256(TS_STRICT),
                        'kind': 'tsconfig', 'extendsResolved': ['tsconfig.base.json']}]}
    cg = h.record(B.NATIVE_DOC, '#/$defs/TypeScriptConfigGraphV1', graph, 'cg')
    ctx = ts_context(h, 'ts-tsconfig', ['tsconfig.base.json', 'tsconfig.json'],
                     honored_options())
    uni = {'schemaVersion': 2, 'languageMode': 'ts-tsconfig', 'configOrigin': 'tsconfig',
           'synthesizerVersion': None, 'synthesizedOptions': None,
           'packageModuleType': 'module', 'allowJs': False, 'checkJs': False,
           'jsAdmittedToProgram': False, 'jsDiagnosticsEnabled': False,
           'resolutionCompletenessImplied': False, 'jsRootFiles': [],
           'programRootFiles': ['src/index.ts'], 'lockfileKind': 'none',
           'nodeModulesInReadSet': False, 'executionCapableResolution': False,
           'tsconfigGraphHash': cg}
    ch, uh, uni = admit_pair(h, 'native.context.typescript.v2',
                             '#/$defs/TypeScriptNativeContextV2', ctx,
                             'native.semantic-universe.typescript.v2',
                             '#/$defs/TypeScriptUniverseV2ResolvedInputs', uni,
                             'ts-tsconfig')
    rows = h.mode_law('native.semantic-universe.typescript.v2', uni, ctx)
    rows += h.config_kind_law(graph, uni)
    return dict(mode='ts-tsconfig', harness=h, rows=rows, ctx=ch, uni=uh,
                grammar=('TypeScript compiler program from the admitted '
                         'TypeScriptNativeContextV2 toolchain; no bundled syntax grammar '
                         'participates in a compiler mode'),
                language='typescript')


def mode_js_allowjs():
    files = {'config.shared.json': SHARED, 'jsconfig.json': JSCFG, 'src/index.js': IDX_JS}
    h = MH.Harness('prj1-mode-js-allowjs', files)
    graph = {'schemaVersion': 1, 'entryConfigPath': 'jsconfig.json',
             'nodes': [{'path': 'config.shared.json', 'contentSha256': K.raw_sha256(SHARED),
                        'kind': 'other', 'extendsResolved': []},
                       {'path': 'jsconfig.json', 'contentSha256': K.raw_sha256(JSCFG),
                        'kind': 'jsconfig', 'extendsResolved': ['config.shared.json']}]}
    cg = h.record(B.NATIVE_DOC, '#/$defs/TypeScriptConfigGraphV1', graph, 'cg')
    ctx = ts_context(h, 'js-allowjs', ['config.shared.json', 'jsconfig.json'],
                     honored_options(allowJs=True, target='es2020', lib=['es2020']))
    uni = {'schemaVersion': 2, 'languageMode': 'js-allowjs', 'configOrigin': 'jsconfig',
           'synthesizerVersion': None, 'synthesizedOptions': None,
           'packageModuleType': 'commonjs', 'allowJs': True, 'checkJs': False,
           'jsAdmittedToProgram': True, 'jsDiagnosticsEnabled': False,
           'resolutionCompletenessImplied': False, 'jsRootFiles': ['src/index.js'],
           'programRootFiles': ['src/index.js'], 'lockfileKind': 'none',
           'nodeModulesInReadSet': False, 'executionCapableResolution': False,
           'tsconfigGraphHash': cg}
    ch, uh, uni = admit_pair(h, 'native.context.typescript.v2',
                             '#/$defs/TypeScriptNativeContextV2', ctx,
                             'native.semantic-universe.typescript.v2',
                             '#/$defs/TypeScriptUniverseV2ResolvedInputs', uni,
                             'js-allowjs')
    rows = h.mode_law('native.semantic-universe.typescript.v2', uni, ctx)
    rows += h.config_kind_law(graph, uni)
    return dict(mode='js-allowjs', harness=h, rows=rows, ctx=ch, uni=uh,
                grammar=('TypeScript compiler program with allowJs honoured; .js/.mjs/.cjs/'
                         '.jsx are program roots'), language='typescript')


def mode_js_synthesized():
    files = {'src/index.js': IDX_JS}
    h = MH.Harness('prj1-mode-js-synth', files)
    graph = {'schemaVersion': 1, 'entryConfigPath': None, 'nodes': []}
    cg = h.record(B.NATIVE_DOC, '#/$defs/TypeScriptConfigGraphV1', graph, 'cg')
    # SynthesizedCompilerOptionsV1 is fully CONST-PINNED by the kit: the synthesizer has no
    # freedom, so the option object is reconstructed from the schema's own consts rather than
    # chosen. `jsx` is the one optional member and is spelled at its const value.
    synth = {'allowJs': True, 'checkJs': False, 'module': 'node16',
             'moduleResolution': 'node16', 'target': 'es2022', 'jsx': 'preserve',
             'strict': False, 'skipLibCheck': True, 'types': [], 'noEmit': True}
    ctx = ts_context(h, 'js-synthesized', [],
                     honored_options(allowJs=True, module='node16',
                                     moduleResolution='node16', target='es2022',
                                     jsx='preserve', strict=False, skipLibCheck=True,
                                     types=[], noEmit=True))
    uni = {'schemaVersion': 2, 'languageMode': 'js-synthesized',
           'configOrigin': 'synthesized', 'synthesizerVersion': 1,
           'synthesizedOptions': synth,
           'packageModuleType': 'commonjs', 'allowJs': True, 'checkJs': False,
           'jsAdmittedToProgram': True, 'jsDiagnosticsEnabled': False,
           'resolutionCompletenessImplied': False, 'jsRootFiles': ['src/index.js'],
           'programRootFiles': ['src/index.js'], 'lockfileKind': 'none',
           'nodeModulesInReadSet': False, 'executionCapableResolution': False,
           'tsconfigGraphHash': cg}
    ch, uh, uni = admit_pair(h, 'native.context.typescript.v2',
                             '#/$defs/TypeScriptNativeContextV2', ctx,
                             'native.semantic-universe.typescript.v2',
                             '#/$defs/TypeScriptUniverseV2ResolvedInputs', uni,
                             'js-synthesized')
    rows = h.mode_law('native.semantic-universe.typescript.v2', uni, ctx)
    rows += h.config_kind_law(graph, uni)
    return dict(mode='js-synthesized', harness=h, rows=rows, ctx=ch, uni=uh,
                grammar=('no configuration file exists, so the analysis path is the '
                         'SYNTHESIZED option set at synthesizerVersion 1 and an EMPTY '
                         'retained config graph'), language='typescript')


def rust_modes():
    """The Rust universe carries NO `languageMode` field: section 1.2 decides its mode from
    `preparedOutputSetId` / `preparedResolution`. So both Rust rows are applied to the REAL
    admitted records of the exported Rust Run -- `rust-cargo` exactly as sealed, and
    `rust-cargo-prepared` as the same context with a prepared output set, re-admitted against
    its owning schema. Nothing is invented about the context: the prepared posture changes
    only the two fields the mode table reads.
    """
    import opensip_store as ST
    import opensip_closure as CL
    st, doc = ST.Store.load(OUT + '/runs/rust.store.json')
    uni = ctx = None
    for tid, rec in st.objects.items():
        if tid.startswith('native.semantic-universe.rust.v2#') and uni is None:
            uni = rec
        if tid.startswith('native.context.rust.v2#'):
            ctx = rec
    c = CL.Closure(st)
    rows_plain = []
    before = len(c.checks)
    c.check_language_mode_recognition('native.semantic-universe.rust.v2', uni, ctx)
    rows_plain = [MH.Harness._row(x) for x in c.checks[before:]]

    prep_set = {'schemaVersion': 1, 'units': [], 'generatedFiles': []}
    prep_hex = None
    h = MH.Harness('prj1-mode-rust-prepared', {'Cargo.toml': CARGO, 'src/main.rs': MAIN_RS})
    uni2 = dict(uni)
    uni2['preparedOutputSetId'] = 'sha256:' + K.raw_sha256(K.C(prep_set))
    # the enum is closed: ['none','host-prepared','imported-inert']. `host-prepared` is the
    # posture that corresponds to the rust-cargo-prepared mode with a host-produced set.
    uni2['preparedResolution'] = 'host-prepared'
    rows_prep = []
    admitted_prep, prep_err = True, None
    try:
        h.b.admit(B.NATIVE_DOC, '#/$defs/RustUniverseV2ResolvedInputs', uni2,
                  'uni:rust-cargo-prepared')
    except Exception as e:
        admitted_prep, prep_err = False, str(e)[:800]
    if admitted_prep:
        before = len(c.checks)
        c.check_language_mode_recognition('native.semantic-universe.rust.v2', uni2, ctx)
        rows_prep = [MH.Harness._row(x) for x in c.checks[before:]]
    return (rows_plain, rows_prep, admitted_prep, prep_err,
            uni2['preparedResolution'], uni2['preparedOutputSetId'])


def rust_pair(h, prepared):
    cfgproj = {'schemaVersion': 1, 'configFiles': [], 'mergedKeys': [],
               'rustflags': [], 'honoredKeys': [], 'ignoredKeys': []}
    ctx = {'schemaVersion': 2,
           'toolchain': {'compilerName': 'rustc', 'rustcVersion': '1.84.0',
                         'rustCommitHash': '0123456789abcdef0123456789abcdef01234567',
                         'cargoVersion': '1.84.0', 'targetTriple': 'aarch64-apple-darwin',
                         'hostTriple': 'aarch64-apple-darwin',
                         'sysrootDigest': K.raw_sha256(b'sysroot'),
                         'rustcDevLlvmDigest': None,
                         'standardLibraryComponentDigests':
                             [{'component': 'libcore.rlib',
                               'sha256': K.raw_sha256(b'libcore')}]},
           'configProjection': cfgproj, 'targetTriple': 'aarch64-apple-darwin',
           'baseCfg': ['target_arch="aarch64"'],
           'dependencyFileManifestId': None, 'dependencySourceSetId': None,
           'preparedOutputSetId': None}
    return ctx


def mode_rust(prepared):
    mode = 'rust-cargo-prepared' if prepared else 'rust-cargo'
    files = {'Cargo.toml': CARGO, 'src/main.rs': MAIN_RS}
    h = MH.Harness('prj1-mode-' + mode, files)
    ctx = rust_pair(h, prepared)
    uni = {'schemaVersion': 2,
           'editionMap': [{'crateName': 'app1', 'edition': 2021}],
           'resolverVersion': 2,
           'preparedOutputSetId': ('sha256:' + K.raw_sha256(b'prepared-set')
                                   if prepared else None),
           'preparedResolution': 'generated-sources' if prepared else 'none',
           'nativeContextId': None}
    return dict(mode=mode, harness=h, universeDraft=uni, ctx=ctx,
                grammar=('rustc/cargo resolved inputs from the admitted '
                         'RustNativeContextV2; `preparedOutputSetId` '
                         + ('non-null with a prepared resolution'
                            if prepared else 'null with preparedResolution none')
                         + ' is what separates the two Rust modes'),
                language='rust')


def mode_syntax_only():
    """syntax-only: grammar-only, no compiler. The chosen grammar set is the decision that
    matters here, so it is documented explicitly rather than implied."""
    return dict(mode='syntax-only',
                grammar=('bundled syntax grammars selected by the universe '
                         '`selectedGrammarIds`; this origin exercised BOTH syntaxClasses: '
                         'javascript (code) on the syntax-code Run and json/markdown '
                         '(data-document) on the syntax-data Run'),
                language='syntax')


def main():
    nat = json.load(open(KIT + '/' + S.doc_path(B.NATIVE_DOC)))
    idj = json.load(open(KIT + '/' + S.doc_path(B.IDENTITY_DOC)))
    advertised = sorted(idj['x-opensip-digest-domains']['languageModes']['map'].items())
    exercised = {
        'js-allowjs': ['typescript (complete sealed Run, runs/typescript.store.json)'],
        'rust-cargo': ['rust (complete sealed Run, runs/rust.store.json)',
                       'rust-partial (complete sealed Run)'],
        'syntax-only': ['syntax-code (complete sealed Run)',
                        'syntax-data (complete sealed Run)'],
    }
    out = []
    for fn in (mode_ts_tsconfig, mode_js_allowjs, mode_js_synthesized):
        r = fn()
        ref = MH.Harness.refusals(r['rows'])
        out.append({'mode': r['mode'], 'universeLanguage': r['language'],
                    'chosenGrammarOrProgram': r['grammar'],
                    'representablePath': {
                        'kind': 'record-level harness (schema admission + section 1.2 law)',
                        'contextDigest': r['ctx'], 'universeDigest': r['uni'],
                        'lawChecksExecuted': len(r['rows']),
                        'lawChecks': r['rows'], 'refusals': ref},
                    'endToEndOnACompleteSealedRun': exercised.get(r['mode'], []),
                    'admitted': not ref})
    # the two Rust modes: the mode is not a universe FIELD, it is decided by
    # preparedOutputSetId / preparedResolution, so the law is applied to both postures
    rp, rq, prep_ok, prep_err, prep_res, prep_id = rust_modes()
    out.append({'mode': 'rust-cargo', 'universeLanguage': 'rust',
                'chosenGrammarOrProgram': (
                    'rustc/cargo resolved inputs from the admitted NativeContextV2; '
                    'preparedOutputSetId null with preparedResolution none'),
                'representablePath': {
                    'kind': 'the REAL sealed records of runs/rust.store.json',
                    'preparedOutputSetId': None, 'preparedResolution': 'none',
                    'lawChecksExecuted': len(rp), 'lawChecks': rp,
                    'refusals': MH.Harness.refusals(rp)},
                'endToEndOnACompleteSealedRun': exercised['rust-cargo'],
                'admitted': not MH.Harness.refusals(rp)})
    out.append({'mode': 'rust-cargo-prepared', 'universeLanguage': 'rust',
                'chosenGrammarOrProgram': (
                    'the same rustc/cargo inputs plus a PREPARED output set: generated '
                    'sources enter the analysis through preparedOutputSetId, and '
                    'preparedResolution stops being `none`'),
                'representablePath': {
                    'kind': ('the sealed Rust context with the two mode-deciding fields '
                             'set, re-admitted against RustUniverseV2ResolvedInputs'),
                    'owningSchemaAdmitted': prep_ok,
                    'owningSchemaError': prep_err,
                    'preparedOutputSetId': prep_id, 'preparedResolution': prep_res,
                    'lawChecksExecuted': len(rq), 'lawChecks': rq,
                    'refusals': MH.Harness.refusals(rq)},
                'endToEndOnACompleteSealedRun': [],
                'admitted': prep_ok and not MH.Harness.refusals(rq)})
    r = mode_syntax_only()
    out.append({'mode': 'syntax-only', 'universeLanguage': 'syntax',
                'chosenGrammarOrProgram': r['grammar'],
                'representablePath': {
                    'kind': 'exercised end-to-end; no separate harness needed',
                    'lawChecksExecuted': None,
                    'note': ('section1.2:SYNTAX_ONLY_MODE_RECOGNISED is executed inside '
                             'check_universe on both syntax Runs')},
                'endToEndOnACompleteSealedRun': exercised['syntax-only'],
                'admitted': True})
    have = {r['mode'] for r in out}
    missing = [m for m, _ in advertised if m not in have]
    doc = {'classification': 'measured', 'consumerId': 'consumer-b.v16',
           'standing': MH.STANDING,
           'law': B.NATIVE_DOC + ' section 1.2 + ' + B.IDENTITY_DOC
                  + '#/x-opensip-digest-domains/languageModes/map',
           'advertisedModes': dict(advertised),
           'modeCount': len(advertised),
           'modePaths': sorted(out, key=lambda r: r['mode']),
           'modesWithNoRepresentablePath': missing,
           'modesRepresentedButNotExercisedEndToEnd':
               sorted(r['mode'] for r in out if not r['endToEndOnACompleteSealedRun']),
           'distinction': ('a representable path is an admitted (context, universe) pair '
                           'that the section 1.2 table recognises. It is NOT the same claim '
                           'as a complete sealed Run, and this table never merges them.')}
    p = OUT + '/vectors/advertised-mode-paths.json'
    with open(p, 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    for r in doc['modePaths']:
        print('%-22s admitted=%-5s lawChecks=%-4s endToEnd=%s'
              % (r['mode'], r['admitted'], r['representablePath']['lawChecksExecuted'],
                 len(r['endToEndOnACompleteSealedRun'])))
    bad = [r['mode'] for r in out if not r['admitted']]
    print('advertised=%d represented=%d missing=%s notExercisedEndToEnd=%s'
          % (len(advertised), len(out), missing,
             doc['modesRepresentedButNotExercisedEndToEnd']))
    if bad:
        for r in out:
            if r['mode'] in bad:
                print('REFUSED', r['mode'], json.dumps(
                    r['representablePath']['refusals'], indent=1, default=str)[:900])
    assert not bad and not missing, (bad, missing)


if __name__ == '__main__':
    main()
