"""PILOT complete positive Run -- compiler-free SYNTAX-ONLY Run over a supported CODE
grammar, in a repository with no TypeScript and no Rust compilation unit.

Satisfies (as exhibited properties of this one exported Run):
  R-RUN-SYNTAX-CODE            supported code grammar with inventory and syntax/clone facts
  R-RUN-NO-COMPILER-UNIT       no tsconfig / no Cargo.toml; exact context/universe/
                               provider/grammar custody retained
  R-RUN-FILE-FACT-INVENTORY    file facts with inventoried path/hash/length joins
  R-RUN-CLONES-L0-AND-NORMALIZED  clone body identities at L0-verbatim and L1-lexical
  R-RUN-CLONES-CUSTODY         level-specification bytes + language-version derivation inputs

All repository bytes, grammar bundles, provider returns and inventories are this origin's
own SYNTHETIC TRUSTED OBSERVATIONS. They are assumptions about a future host and are never
native enforcement proof.
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

OUT = '/tmp/opensip-design-corrections/consumer-b.v14/output'
RUN_ID_LABEL = 'syntax-code'

PROJECT_ID = 'prj1-' + '4b7f2c91a3e85d06fa1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f708192a3b4c5d6e'[:64]

# ------------------------------------------------------------------ repository bytes
A_SRC = b'export function f(x) { return x + 1; }\n'
B_SRC = b'export function g(x) { return x + 1; }\n'
BODY = b'{ return x + 1; }'
A_SPAN = (A_SRC.index(BODY), A_SRC.index(BODY) + len(BODY))
B_SPAN = (B_SRC.index(BODY), B_SRC.index(BODY) + len(BODY))

FILES = {
    'LICENSE': b'MIT\n',
    'README.md': b'# demo\n\nsyntax-only reconstruction subject.\n',
    'package.json': b'{"name":"demo","private":true,"version":"0.1.0"}\n',
    'src/a.js': A_SRC,
    'src/b.js': B_SRC,
}

# level specifications (retained; normalisationVersion is their raw SHA-256)
L0_SPEC = (b'opensip level specification\nlevel: L0-verbatim\n'
           b'lexical-boundary: none (tokenisation forbidden)\n'
           b'token-kind-registry: none\ndirective-classification: none\n'
           b'transform-order: []\nreplacement-bytes: none\n'
           b'languages: javascript typescript rust\n')
L1_SPEC = (b'opensip level specification\nlevel: L1-lexical\n'
           b'lexical-boundary: javascript ECMA-262 punctuator/identifier/numeric/string\n'
           b'token-kind-registry: keyword ident number string punct\n'
           b'directive-classification: none\n'
           b'transform-order: [strip-insignificant-whitespace, normalise-line-endings]\n'
           b'replacement-bytes: none\nlanguages: javascript\n')

SUFFIX_TABLE_SYNTAX = None   # read from the registry at build time


def build():
    b = B.Builder(PROJECT_ID)
    st = b.st
    notes = {}

    # retain every registered schema document this graph pins
    for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.POLICY_V2_DOC, B.POLICY_V1_DOC,
              B.ENUM_PLAN_DOC, B.EMIT_PLAN_DOC, B.SUBJ_INV_DOC, B.EXEC_IN_DOC):
        b.retain_schema_doc(d)

    # ---------------------------------------------------------------- closures
    grammar_tid, grammar_rec, _ = b.closure(
        'grammar', '3.1.0', 3, 'macos-aarch64',
        [('grammars/javascript.json', b'{"grammar":"javascript","rev":7}'),
         ('grammars/json.json', b'{"grammar":"json","rev":3}'),
         ('grammars/markdown.json', b'{"grammar":"markdown","rev":2}'),
         ('bin/opensip-grammar', b'\x7fELF-synthetic-grammar-bundle')],
        'opensip-grammar-bundle')
    provider_tid, provider_rec, _ = b.closure(
        'provider', '2.4.0', 3, 'macos-aarch64',
        [('bin/opensip-syntax-provider', b'\x7fELF-synthetic-syntax-provider')],
        'opensip-syntax-provider')
    evaluator_tid, evaluator_rec, _ = b.closure(
        'evaluator', '3.0.0', 3, 'macos-aarch64',
        [('bin/opensip-evaluator', b'\x7fELF-synthetic-pure-evaluator')],
        'opensip-evaluator')
    detector_tid, detector_rec, _ = b.closure(
        'detector', '1.2.0', 3, 'macos-aarch64',
        [('rules/clone-hygiene.json', b'{"detector":"clone-hygiene","rev":4}')],
        'opensip-clone-hygiene-detector')

    # ---------------------------------------------------------------- snapshot
    config = {
        'analysis': {'profileId': 'syntax-only', 'capabilities':
                     sorted(['inventory', 'syntax', 'clones-fact', 'unresolved-edge'],
                            key=lambda s: K.C(s)),
                     'budget': {'unit': 'work-units', 'limit': 5000000}},
        'components': {'request': [{'stableId': '11111111-2222-4333-8444-555555555555',
                                    'version': '3.1.0'}],
                       'allowedScopes': ['project', 'global']},
        'discovery': {'workspaceRoots': ['.']},
        'policy': {'packIds': ['pack.clone-hygiene']},
        'evidence': {},
    }
    scope_desc = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': [],
                  'excludedPathPrefixes': []}
    snapshot_id, snapshot, sh = b.snapshot(
        FILES, config, scope_desc, vcs_kind='git',
        commit_id='3f1c0a9d5e2b47c8a6102d3e4f5061728394a5b6', dirty=False)

    # ---------------------------------------------------------------- native context (syntax)
    greg = json.load(open(B.KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
        'x-opensip-grammar-capability-registry']
    langs = greg['languages']
    gram_rows = []
    for lid in ('javascript', 'json', 'markdown'):
        gb = b'{"grammar":"%s","rev":1}' % lid.encode()
        st.put_blob(gb, label='grammar-def:' + lid)
        gram_rows.append({'grammarId': 'g.' + lid, 'grammarVersion': '1.0.0',
                          'languageId': lid, 'syntaxClass': langs[lid]['syntaxClass'],
                          'suffixes': sorted(langs[lid]['suffixes'],
                                             key=lambda s: s.encode()),
                          'grammarDigest': K.raw_sha256(gb)})
    gram_rows.sort(key=lambda r: r['grammarId'].encode())
    bundle_manifest = b'{"bundle":"opensip-grammar-bundle","grammars":3,"rev":7}'
    st.put_blob(bundle_manifest, label='grammar-bundle-manifest')
    st.put_blob(L0_SPEC, label='level-spec:L0-verbatim')
    st.put_blob(L1_SPEC, label='level-spec:L1-lexical')
    bundle = {'schemaVersion': 1, 'closureId': grammar_tid,
              'parserName': 'opensip-grammar', 'parserVersion': grammar_rec['semanticVersion'],
              'bundleDigest': K.raw_sha256(bundle_manifest), 'grammars': gram_rows,
              'normalizer': {'normalizerId': 'opensip-normalizer',
                             'normalizerVersion': '1.1.0',
                             'specificationDigest': K.raw_sha256(L1_SPEC)}}
    ctx = {'schemaVersion': 2, 'grammarBundle': bundle}
    ctx_hex = b.native_framed('native.context.syntax.v2', B.NATIVE_DOC,
                              '#/$defs/SyntaxNativeContextV2', ctx, 'native-context:syntax')

    universe = {'schemaVersion': 2, 'nativeContextId': 'sha256:' + ctx_hex,
                'selectedGrammarIds': sorted([r['grammarId'] for r in gram_rows],
                                             key=lambda s: s.encode()),
                'resolutionAttempted': False}
    uni_hex = b.native_framed('native.semantic-universe.syntax.v2', B.NATIVE_DOC,
                              '#/$defs/SyntaxUniverseV2ResolvedInputs', universe,
                              'native-universe:syntax')

    # ---------------------------------------------------------------- capability manifest
    A = CM.CapabilityManifestAdmitter()
    cap = {'schemaVersion': 1, 'profile': 'syntax-only',
           'providers': [{'providerId': 'opensip.provider.syntax', 'language': 'syntax',
                          'providerVersionSource': 'closure2.semanticVersion',
                          'toolchainIdentitySource': 'grammar-bundle',
                          'relations': {'file': 'enumerated',
                                        'package': 'manifest-declared',
                                        'vcs-change': 'vcs-reported',
                                        'declares': 'syntactic', 'literal': 'syntactic',
                                        'control-flow': 'syntactic',
                                        'clones': 'normalized-body-hash'},
                          'platformIds': ['macos-aarch64']}],
           'coverageForAbsent': [{'providerId': 'opensip.provider.syntax',
                                  'language': 'syntax',
                                  'relationIds': sorted(['imports', 'references', 'calls',
                                                         'types', 'reachability',
                                                         'unresolved-edge'],
                                                        key=lambda s: s.encode()),
                                  'coverageState': 'unavailable',
                                  'deficiency': 'language-tier-unsupported'}]}
    capres = A.admit(cap)
    assert capres['admitted']
    st.put_blob(capres['committedBytes'], label='capability-manifest-artifact')

    # ---------------------------------------------------------------- body identities
    blv_base = {'schemaVersion': 1, 'languageId': 'javascript',
                'compilerName': bundle['parserName'],
                'compilerVersion': bundle['parserVersion'],
                'compilerBuild': bundle['bundleDigest']}
    blv = dict(blv_base, dialect={'grammarVariant': 'js'})
    b.admit(B.IDENTITY_DOC, '#/$defs/body-language-version', blv, 'body-language-version:js')
    blv_bytes = K.C(blv)
    st.put_blob(blv_bytes, label='body-language-version:js')
    lang_ver_raw32 = bytes.fromhex(K.raw_sha256(blv_bytes))

    def clone_payload(level_id, spec_bytes, payload_bytes):
        frame = B.body_identity_frame(level_id, K.raw_sha256(spec_bytes), 'javascript',
                                      lang_ver_raw32, payload_bytes)
        bid = K.raw_sha256(frame)
        st.put_blob(frame, label='body-identity-frame:%s:%s' % (level_id, bid[:8]))
        return {'bodyIdentity': 'sha256:' + bid, 'normalisationLevel': level_id,
                'normalisationVersion': K.raw_sha256(spec_bytes)}, bid, frame

    L1_TOKENS = [('punct', '{'), ('keyword', 'return'), ('ident', 'x'), ('punct', '+'),
                 ('number', '1'), ('punct', ';'), ('punct', '}')]
    l1_stream = B.token_stream(L1_TOKENS)
    st.put_blob(l1_stream, label='l1-token-stream')

    a_l0, a_l0_bid, _ = clone_payload('L0-verbatim', L0_SPEC, B.l0_payload(BODY))
    a_l1, a_l1_bid, _ = clone_payload('L1-lexical', L1_SPEC, l1_stream)

    # ---------------------------------------------------------------- facts
    facts = {}
    fact_payloads = {}

    def mk_fact(relation, rung, payload, anchors, label, confidence=1000000):
        fid = b.fact(snapshot_id, relation, rung, uni_hex, uni_hex, provider_tid,
                     payload, anchors, confidence, label)
        facts[fid] = st.objects[fid]
        fact_payloads[fid] = payload
        return fid

    for p in sorted(FILES, key=lambda s: s.encode()):
        row = [r for r in sh['inventory'] if r['path'] == p][0]
        mk_fact('file', 'enumerated',
                {'path': p, 'contentSha256': row['sha256'], 'byteLength': row['bytes']},
                [], 'file:' + p)
    mk_fact('package', 'manifest-declared',
            {'packageName': 'demo', 'packageVersion': '0.1.0',
             'manifestPath': 'package.json'}, [], 'package:demo')

    def anchor(path, span):
        row = [r for r in sh['inventory'] if r['path'] == path][0]
        return {'path': path, 'blobDigest': row['sha256'],
                'startByte': span[0], 'endByte': span[1]}

    mk_fact('declares', 'syntactic',
            {'container': 'js:src/a.js', 'declared': 'js:src/a.js#f',
             'declarationKind': 'function'},
            [anchor('src/a.js', (0, len(A_SRC) - 1))], 'declares:a')
    mk_fact('declares', 'syntactic',
            {'container': 'js:src/b.js', 'declared': 'js:src/b.js#g',
             'declarationKind': 'function'},
            [anchor('src/b.js', (0, len(B_SRC) - 1))], 'declares:b')
    for path, span, lbl in (('src/a.js', A_SPAN, 'a'), ('src/b.js', B_SPAN, 'b')):
        mk_fact('clones', 'normalized-body-hash', a_l0, [anchor(path, span)],
                'clones-L0:' + lbl)
        mk_fact('clones', 'normalized-body-hash', a_l1, [anchor(path, span)],
                'clones-L1:' + lbl)

    # ---------------------------------------------------------------- scopes + coverage
    scopes, coverages, coverage_payloads = {}, {}, {}

    def mk_scope_cov(relation, rung, subjects, label, cov='complete', deficiency=None,
                     native_cause=None, exhaustive=True):
        sid = b.scope(snapshot_id, relation, rung, uni_hex, uni_hex, provider_tid,
                      subjects, label)
        scopes[sid] = st.objects[sid]
        rc = B.rc_not_applicable()
        rc['examinedExhaustive'] = exhaustive
        ent = B.entry(cov, B.closed_world_open(['syntax-only analysis: no resolution attempted']),
                      deficiency=deficiency, native_cause=native_cause, rc=rc)
        cid = b.coverage(sid, ent, label)
        coverages[cid] = st.objects[cid]
        coverage_payloads[cid] = json.loads(
            st.get_blob(st.objects[cid]['payloadDigest']).decode())
        return sid, cid

    s_file, c_file = mk_scope_cov('file', 'enumerated', sorted(FILES), 'file-enumerated')
    s_pkg, c_pkg = mk_scope_cov('package', 'manifest-declared', ['demo'], 'package-declared')
    s_decl, c_decl = mk_scope_cov('declares', 'syntactic',
                                  ['js:src/a.js#f', 'js:src/b.js#g'], 'declares-syntactic')
    s_clone, c_clone = mk_scope_cov('clones', 'normalized-body-hash',
                                    ['src/a.js', 'src/b.js'], 'clones-normalized')

    # ---------------------------------------------------------------- enumeration plan
    membership = {
        'schemaVersion': 1,
        'units': [{'unitOrdinal': 0, 'rootPath': '', 'languageFamily': 'none',
                   'languageMode': 'syntax-only', 'unitKind': 'syntax-only',
                   'markerPath': '', 'markerSha256': None,
                   'recognizerId': 'opensip-syntax-recognizer', 'recognizerVersion': 1,
                   'provenance': 'DEFAULTED', 'memberPackageRoots': []}],
        'rows': [{'path': p, 'languageFamily': 'none', 'unitOrdinal': 0,
                  'membership': ('syntax-only' if p.split('.')[-1] in ('js', 'json', 'md')
                                 and '.' in p else 'unsupported-file'),
                  'reason': ('grammar-only' if p.split('.')[-1] in ('js', 'json', 'md')
                             and '.' in p else 'no-bundled-grammar')}
                 for p in sorted(FILES, key=lambda s: s.encode())],
        'unsupportedFiles': ['LICENSE'],
        'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    def binding(ordinal, extents, candidate_paths=None, unavailable=None):
        r = {'ordinal': ordinal, 'provenance': 'default-unit' if ordinal == 0
             else 'explicit-plan-selection',
             'enumerator': {'status': 'selected', 'closureId': provider_tid},
             'nativeContextDigest': ctx_hex, 'universe': uni_hex,
             'programEntry': None,
             'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                for k, v in extents.items()],
                               key=lambda e: e['kind'].encode())}
        if candidate_paths is not None:
            r['candidateSourcePaths'] = sorted(candidate_paths, key=lambda s: s.encode())
        if unavailable:
            r = {'ordinal': ordinal,
                 'provenance': 'default-unit' if ordinal == 0 else 'explicit-plan-selection',
                 'enumerator': {'status': 'unselected', 'reason': 'optional-unselected'},
                 'nativeContextDigest': ctx_hex, 'universe': None, 'programEntry': None,
                 'extents': [], 'deficiency': unavailable[0], 'nativeCause': unavailable[1]}
        return r

    all_paths = sorted(FILES, key=lambda s: s.encode())
    code_paths = ['src/a.js', 'src/b.js']
    cells = [
        {'capabilityId': 'clones-fact', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': ['file'],
         'programBindings': [binding(0, {'file': code_paths})]},
        {'capabilityId': 'inventory', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': sorted(['file', 'package'], key=lambda s: K.C(s)),
         'programBindings': [binding(0, {'file': all_paths, 'package': ['package.json']})]},
        {'capabilityId': 'syntax', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'],
         'programBindings': [binding(0, {'symbol': code_paths})]},
        {'capabilityId': 'unresolved-edge', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': False, 'kinds': ['symbol'],
         'programBindings': [binding(0, {}, unavailable=('language-tier-unsupported', None))]},
    ]
    cells.sort(key=lambda c: (c['capabilityId'].encode(), c['languageMode'].encode(),
                              c['workspaceRoot'].encode()))
    enum_plan = {'schemaVersion': 1, 'snapshotId': snapshot_id,
                 'scopeDigest': sh['scopeDigest'], 'membershipDigest': membership_dig,
                 'cells': cells}
    enum_plan_dig = b.record(B.ENUM_PLAN_DOC, '#', enum_plan, 'enumeration-plan')
    cell_ord = {c['capabilityId']: i for i, c in enumerate(cells)}

    # ---------------------------------------------------------------- subject inventories
    lang_table = {'.js': 'javascript', '.json': 'json', '.md': 'markdown'}

    def subj_lang(path):
        for suf, lid in sorted(lang_table.items(), key=lambda t: -len(t[0])):
            if path.endswith(suf):
                return lid
        return 'unspecified'

    inventories = []

    def mk_inv(cap_id, kind, rows, examined, state='complete', deficiency=None,
               native_cause=None):
        inv = {'schemaVersion': 1, 'planId': 'plan2:' + '0' * 64,
               'parameterDigest': enum_plan_dig, 'cellOrdinal': cell_ord[cap_id],
               'programOrdinal': 0, 'kind': kind, 'state': state,
               'deficiency': deficiency, 'nativeCause': native_cause,
               'examinedPaths': sorted(examined, key=lambda s: K.C(s)),
               'rows': rows}
        return inv

    file_rows = sorted([{'nativeSubjectId': p, 'kind': 'file', 'path': p,
                         'qualifiedName': p, 'subjectLanguage': subj_lang(p),
                         'signatureTokens': [], 'projections': []}
                        for p in all_paths],
                       key=lambda r: r['nativeSubjectId'].encode())
    pkg_rows = [{'nativeSubjectId': 'demo', 'kind': 'package', 'path': 'package.json',
                 'qualifiedName': 'demo', 'subjectLanguage': 'json',
                 'signatureTokens': [], 'projections': []}]
    sym_rows = sorted([
        {'nativeSubjectId': 'js:src/a.js#f', 'kind': 'symbol', 'path': 'src/a.js',
         'qualifiedName': 'f', 'subjectLanguage': 'javascript', 'exported': 'exported',
         'signatureTokens': ['javascript', 'function', 'f', '(', 'x', ')'],
         'projections': [{'closureId': detector_tid,
                          'signatureTokens': ['javascript', 'function', 'f', '(', 'x', ')']}]},
        {'nativeSubjectId': 'js:src/b.js#g', 'kind': 'symbol', 'path': 'src/b.js',
         'qualifiedName': 'g', 'subjectLanguage': 'javascript', 'exported': 'exported',
         'signatureTokens': ['javascript', 'function', 'g', '(', 'x', ')'],
         'projections': [{'closureId': detector_tid,
                          'signatureTokens': ['javascript', 'function', 'g', '(', 'x', ')']}]},
    ], key=lambda r: r['nativeSubjectId'].encode())

    inv_specs = [('inventory', 'file', file_rows, all_paths),
                 ('inventory', 'package', pkg_rows, ['package.json']),
                 ('syntax', 'symbol', sym_rows, code_paths),
                 ('clones-fact', 'file', sorted([{'nativeSubjectId': p, 'kind': 'file',
                                                  'path': p, 'qualifiedName': p,
                                                  'subjectLanguage': subj_lang(p),
                                                  'signatureTokens': [], 'projections': []}
                                                 for p in code_paths],
                                                key=lambda r: r['nativeSubjectId'].encode()),
                  code_paths)]
    return dict(b=b, st=st, notes=notes, snapshot_id=snapshot_id, snapshot=snapshot, sh=sh,
                closures=dict(grammar=grammar_tid, provider=provider_tid,
                              evaluator=evaluator_tid, detector=detector_tid),
                ctx_hex=ctx_hex, uni_hex=uni_hex, cap=cap, capres=capres, config=config,
                scope_desc=scope_desc, facts=facts, fact_payloads=fact_payloads,
                scopes=scopes, coverages=coverages, coverage_payloads=coverage_payloads,
                enum_plan=enum_plan, enum_plan_dig=enum_plan_dig, cell_ord=cell_ord,
                inv_specs=inv_specs, mk_inv=mk_inv, bundle=bundle, blv=blv,
                body=dict(l0=a_l0, l1=a_l1, l0_bid=a_l0_bid, l1_bid=a_l1_bid,
                          l0_spec=L0_SPEC, l1_spec=L1_SPEC, tokens=L1_TOKENS,
                          l1_stream=l1_stream, lang_ver_raw32=lang_ver_raw32),
                view_parts=dict(scopes=[s_file, s_pkg, s_decl, s_clone],
                                coverages=[c_file, c_pkg, c_decl, c_clone]),
                files=FILES, spans={'src/a.js': A_SPAN, 'src/b.js': B_SPAN},
                membership=membership, membership_dig=membership_dig)


if __name__ == '__main__':
    g = build()
    print('snapshot', g['snapshot_id'])
    print('context ', g['ctx_hex'])
    print('universe', g['uni_hex'])
    print('facts   ', len(g['facts']))
    print('scopes  ', len(g['scopes']))
    print('cap id  ', g['capres']['capabilityManifestId'])
    print('admissions', len(g['b'].admissions),
          'all admitted', all(a['admitted'] for a in g['b'].admissions))
