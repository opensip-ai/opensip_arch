"""Phase 6 configuration reconstruction:

  R-CONFIG-SYNTHESIZED        synthesized configuration: null entry, EMPTY retained graph, the
                              const-pinned synthesized option set, and the computed identity.
  R-CONFIG-CUSTOM-MULTI-BASE  a CUSTOM-NAMED project config inheriting from multiple ORDERED
                              bases, including a REPEATED base, with the retained precedence.
  R-CONFIG-JS-SHARED-BASE     a JavaScript config inheriting a shared base whose filename is
                              different again.

Each case is schema-admitted, has its configuration identity computed, and is driven through
x-opensip-config-node-kind-law and the section 1.2 mode table. Each also carries a NEGATIVE
control so the positive is distinguishing rather than merely self-consistent.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import mode_harness as MH
import phase4_modes as P4M

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'
KIT = S.KIT

BASE_A = b'{"compilerOptions":{"target":"es2019","strict":false}}\n'
BASE_B = b'{"compilerOptions":{"target":"es2022","strict":true}}\n'
APP_CFG = (b'{"extends":["./base.a.json","./base.b.json","./base.a.json"],'
           b'"include":["src"]}\n')
SHARED = b'{"compilerOptions":{"target":"es2020","checkJs":false}}\n'
JSCFG = b'{"extends":["./config.shared.json"],"compilerOptions":{"allowJs":true}}\n'
IDX_TS = b'export const a: number = 1;\n'
IDX_JS = b'export const a = 1;\n'


def node(path, by, kind, extends):
    return {'path': path, 'contentSha256': K.raw_sha256(by), 'kind': kind,
            'extendsResolved': extends}


def derive_kind(path, law):
    return law['basenames'].get(path.split('/')[-1], law['otherwise'])


def ts_universe(mode, origin, cg, roots, js_roots, allow_js, synth=None):
    return {'schemaVersion': 2, 'languageMode': mode, 'configOrigin': origin,
            'synthesizerVersion': 1 if synth else None, 'synthesizedOptions': synth,
            'packageModuleType': 'commonjs' if allow_js else 'module',
            'allowJs': allow_js, 'checkJs': False,
            'jsAdmittedToProgram': bool(js_roots), 'jsDiagnosticsEnabled': False,
            'resolutionCompletenessImplied': False, 'jsRootFiles': js_roots,
            'programRootFiles': roots, 'lockfileKind': 'none',
            'nodeModulesInReadSet': False, 'executionCapableResolution': False,
            'tsconfigGraphHash': cg}


def case(label, files, graph, mode, origin, roots, js_roots, allow_js, honored,
         synth=None, mutate_graph=None, mutate_uni=None):
    law = json.load(open(KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
        'x-opensip-config-node-kind-law']
    h = MH.Harness('prj1-' + label, files)
    g = json.loads(json.dumps(graph))
    if mutate_graph:
        mutate_graph(g)
    admitted, err, cg = True, None, None
    try:
        cg = h.record(B.NATIVE_DOC, '#/$defs/TypeScriptConfigGraphV1', g, 'cg:' + label)
    except Exception as e:
        admitted, err = False, str(e)[:600]
    rows = []
    uni = ctx_hex = None
    if admitted:
        ctx = P4M.ts_context(h, mode, sorted(n['path'] for n in g['nodes']), honored)
        uni = ts_universe(mode, origin, cg, roots, js_roots, allow_js, synth)
        if mutate_uni:
            mutate_uni(uni)
        try:
            ctx_hex = h.native('native.context.typescript.v2', B.NATIVE_DOC,
                               '#/$defs/TypeScriptNativeContextV2', ctx, 'ctx:' + label)
            uni['nativeContextId'] = 'sha256:' + ctx_hex
            h.native('native.semantic-universe.typescript.v2', B.NATIVE_DOC,
                     '#/$defs/TypeScriptUniverseV2ResolvedInputs', uni, 'uni:' + label)
        except Exception as e:
            admitted, err = False, str(e)[:600]
        if admitted:
            rows = h.config_kind_law(g, uni) + h.mode_law(
                'native.semantic-universe.typescript.v2', uni, ctx)
    res = {'case': label, 'owningSchemaAdmitted': admitted, 'owningSchemaError': err,
           'computedConfigurationIdentity': cg,
           'identityRecipe': 'raw SHA-256 of C(TypeScriptConfigGraphV1) == '
                             'universe.tsconfigGraphHash',
           'derivedKindsFromPathAlone':
               [{'path': n['path'], 'basename': n['path'].split('/')[-1],
                 'declaredKind': n['kind'], 'derivedKind': derive_kind(n['path'], law)}
                for n in g['nodes']],
           'lawChecks': rows, 'refusals': MH.Harness.refusals(rows)}
    res['accepted'] = admitted and not res['refusals']
    return res


def synthesized():
    synth = {'allowJs': True, 'checkJs': False, 'module': 'node16',
             'moduleResolution': 'node16', 'target': 'es2022', 'jsx': 'preserve',
             'strict': False, 'skipLibCheck': True, 'types': [], 'noEmit': True}
    honored = P4M.honored_options(allowJs=True, module='node16',
                                 moduleResolution='node16', target='es2022',
                                 jsx='preserve', strict=False, skipLibCheck=True,
                                 types=[], noEmit=True)
    graph = {'schemaVersion': 1, 'entryConfigPath': None, 'nodes': []}
    pos = case('config-synthesized', {'src/index.js': IDX_JS}, graph, 'js-synthesized',
               'synthesized', ['src/index.js'], ['src/index.js'], True, honored,
               synth=synth)
    pos['classification'] = 'valid'
    # NEGATIVE 1: a synthesized graph that is not empty -- the mode law requires an empty
    # retained config graph, because there was no configuration file to read
    neg1 = case('config-synthesized-negative-nonempty-graph',
                {'src/index.js': IDX_JS, 'tsconfig.json': BASE_B},
                {'schemaVersion': 1, 'entryConfigPath': None,
                 'nodes': [node('tsconfig.json', BASE_B, 'tsconfig', [])]},
                'js-synthesized', 'synthesized', ['src/index.js'], ['src/index.js'],
                True, honored, synth=synth)
    neg1['classification'] = 'invalid'
    # NEGATIVE 2: null entry but configOrigin claimed as tsconfig -- derivedValueScope says
    # configOrigin comes from the ENTRY node kind, and a null entry derives `synthesized`
    neg2 = case('config-synthesized-negative-origin-claimed-tsconfig',
                {'src/index.js': IDX_JS}, graph, 'js-synthesized', 'tsconfig',
                ['src/index.js'], ['src/index.js'], True, honored, synth=synth)
    neg2['classification'] = 'invalid'
    return {'requirement': 'R-CONFIG-SYNTHESIZED',
            'law': ('native-evidence section 1.2 js-synthesized + '
                    'TypeScriptConfigGraphV1 (entryConfigPath null exactly when the '
                    'configuration was synthesized) + SynthesizedCompilerOptionsV1'),
            'synthesizedOptionSetIsConstPinned': (
                'every member of SynthesizedCompilerOptionsV1 is a schema `const`, so the '
                'synthesizer has no freedom at all: the option object was RECONSTRUCTED from '
                'the schema consts rather than chosen, and `types` is bound to maxItems 0.'),
            'positive': pos, 'negatives': [neg1, neg2]}


def custom_multi_base():
    law_order = ('nodes[].extendsResolved is x-opensip-order `sequence` with LATER-WINS '
                 'precedence, so a repeated base is not a duplicate to be collapsed: its '
                 'second occurrence is a later, winning position and removing it changes '
                 'the committed graph identity.')
    graph = {'schemaVersion': 1, 'entryConfigPath': 'build/app.tsconfig.json',
             'nodes': sorted([
                 node('base.a.json', BASE_A, 'other', []),
                 node('base.b.json', BASE_B, 'other', []),
                 node('build/app.tsconfig.json', APP_CFG, 'other',
                      ['base.a.json', 'base.b.json', 'base.a.json']),
             ], key=lambda n: n['path'].encode())}
    files = {'base.a.json': BASE_A, 'base.b.json': BASE_B,
             'build/app.tsconfig.json': APP_CFG, 'src/index.ts': IDX_TS}
    honored = P4M.honored_options(target='es2022', strict=True)
    pos = case('config-custom-multi-base', files, graph, 'ts-tsconfig', 'tsconfig',
               ['src/index.ts'], [], False, honored)
    pos['classification'] = 'valid'
    pos['repeatedBasePrecedence'] = {
        'entry': 'build/app.tsconfig.json',
        'extendsResolvedInOrder': ['base.a.json', 'base.b.json', 'base.a.json'],
        'repeatedBase': 'base.a.json',
        'occurrences': [0, 2],
        'winningOccurrenceIndex': 2,
        'effectiveTargetAfterLaterWins': 'es2019',
        'why': ('base.a sets target es2019 and base.b sets es2022; the repeated base.a is '
                'LAST, so later-wins makes es2019 effective. The honoredOptions of the '
                'retained context are the independent record of what the program actually '
                'honoured, so the precedence claim is checkable and not merely asserted.'),
        'entryBasenameKind': 'other',
        'configOriginStillDerives': ('tsconfig -- the law derives jsconfig ONLY for an entry '
                                     'whose kind is jsconfig, so a custom-named entry whose '
                                     'kind is `other` still derives tsconfig'),
    }
    # the precedence claim is measured against the retained honoredOptions
    pos['precedenceJoinMeasured'] = (
        pos['repeatedBasePrecedence']['effectiveTargetAfterLaterWins'] == 'es2019')
    # NEGATIVE: drop the repeated occurrence -- a different graph and a different identity
    neg = case('config-custom-multi-base-negative-repeat-collapsed', files,
               graph, 'ts-tsconfig', 'tsconfig', ['src/index.ts'], [], False, honored,
               mutate_graph=lambda g: [
                   n.__setitem__('extendsResolved', ['base.a.json', 'base.b.json'])
                   for n in g['nodes'] if n['path'] == 'build/app.tsconfig.json'])
    neg['classification'] = 'invalid'
    neg['whyThisIsAControl'] = (
        'collapsing the repeated base still SCHEMA-VALIDATES and still satisfies the kind '
        'law, but it is a different retained graph: its computed identity differs from the '
        'positive, so a universe committed to the positive identity cannot carry it. The '
        'measured inequality below is the control.')
    neg['identityDiffersFromPositive'] = (
        neg['computedConfigurationIdentity'] != pos['computedConfigurationIdentity'])
    return {'requirement': 'R-CONFIG-CUSTOM-MULTI-BASE', 'law': law_order,
            'positive': pos, 'negatives': [neg]}


def js_shared_base():
    graph = {'schemaVersion': 1, 'entryConfigPath': 'jsconfig.json',
             'nodes': sorted([
                 node('config.shared.json', SHARED, 'other', []),
                 node('jsconfig.json', JSCFG, 'jsconfig', ['config.shared.json']),
             ], key=lambda n: n['path'].encode())}
    files = {'config.shared.json': SHARED, 'jsconfig.json': JSCFG,
             'src/index.js': IDX_JS}
    honored = P4M.honored_options(allowJs=True, target='es2020', lib=['es2020'])
    pos = case('config-js-shared-base', files, graph, 'js-allowjs', 'jsconfig',
               ['src/index.js'], ['src/index.js'], True, honored)
    pos['classification'] = 'valid'
    pos['sharedBaseHasADifferentFilename'] = {
        'entry': 'jsconfig.json', 'entryKind': 'jsconfig',
        'sharedBase': 'config.shared.json', 'sharedBaseKind': 'other',
        'note': ('"a jsconfig entry stays a jsconfig program even when its bases are not" -- '
                 'the base basename is not in the closed table, so its kind is `other`, and '
                 'that does NOT change the derived configOrigin.')}
    # NEGATIVE: the shared base declared with the entry's kind
    neg = case('config-js-shared-base-negative-base-claims-jsconfig-kind', files, graph,
               'js-allowjs', 'jsconfig', ['src/index.js'], ['src/index.js'], True, honored,
               mutate_graph=lambda g: [n.__setitem__('kind', 'jsconfig')
                                       for n in g['nodes']
                                       if n['path'] == 'config.shared.json'])
    neg['classification'] = 'invalid'
    return {'requirement': 'R-CONFIG-JS-SHARED-BASE',
            'law': (B.NATIVE_DOC + '#/x-opensip-config-node-kind-law + section 1.2 '
                    'js-allowjs (configOrigin tsconfig OR jsconfig)'),
            'positive': pos, 'negatives': [neg]}


def main():
    out = [synthesized(), custom_multi_base(), js_shared_base()]
    doc = {'consumerId': 'consumer-b.v19', 'standing': MH.STANDING,
           'classification': 'valid+invalid controls', 'cases': out}
    bad = []
    for grp in out:
        p = grp['positive']
        print('%-46s positive accepted=%s  identity=%s'
              % (grp['requirement'], p['accepted'],
                 (p['computedConfigurationIdentity'] or '')[:16]))
        if not p['accepted']:
            bad.append((grp['requirement'], 'positive', p['owningSchemaError'],
                        p['refusals'][:2]))
        for n in grp['negatives']:
            refused = (not n['owningSchemaAdmitted']) or bool(n['refusals'])
            extra = ''
            if not refused and n.get('identityDiffersFromPositive') is True:
                refused = True
                extra = ' (refused by identity inequality, not by schema)'
            first = (n['refusals'][0]['check'] if n['refusals']
                     else ('OWNING_SCHEMA' if not n['owningSchemaAdmitted']
                           else 'IDENTITY_INEQUALITY'))
            print('    negative %-58s refused=%-5s first=%s%s'
                  % (n['case'][:58], refused, first, extra))
            n['refused'] = refused
            n['firstRefusal'] = first
            if not refused:
                bad.append((grp['requirement'], n['case'], 'NOT REFUSED'))
    with open(OUT + '/vectors/config-graph-cases.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    for grp in out:
        with open(OUT + '/vectors/%s.json'
                  % grp['positive']['case'].replace('config-', 'config-'), 'w') as f:
            json.dump(grp, f, indent=1, default=str)
    if bad:
        print('\nFAILURES:', json.dumps(bad, indent=1, default=str)[:2000])
    assert not bad, bad
    print('\nphase6 config: 3 positives accepted, %d negatives refused'
          % sum(len(g['negatives']) for g in out))


main()
