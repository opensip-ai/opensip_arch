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

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
RUN_ID_LABEL = 'syntax-code'

import opensip_fixture as FX
PROJECT_ID = FX.PROJECT_ID['syntax-code']

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

# Negative-control hook. The driver sets ONE named mutation before build(); the mutation is
# applied at BUILD time so every downstream identity is legitimately reminted and the ENTIRE
# graph is reclosed, rather than a post-hoc patch that only breaks a hash.
MUTATE = {}


def build():
    b = B.Builder(PROJECT_ID)
    st = b.st
    notes = {}

    # retain every registered schema document this graph pins
    for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.POLICY_V2_DOC, B.POLICY_V1_DOC,
              B.ENUM_PLAN_DOC, B.EMIT_PLAN_DOC, B.SUBJ_INV_DOC, B.EXEC_IN_DOC):
        b.retain_schema_doc(d)

    # ---------------------------------------------------------------- closures
    #
    # native-evidence section 1.2: "every grammar definition, the bundle manifest and the
    # normalizer specification PRESENT IN THE RETAINED TREE". Global CAS retention (the
    # schema annotations' `retention: preimage`) is a DIFFERENT obligation from membership
    # in this selected kind=grammar closure tree, so the exact bytes whose raw SHA-256 the
    # bundle names are MEMBERS of this tree, not separate blobs.
    GRAMMAR_DEFS = {'javascript': b'{"grammar":"javascript","rev":7}',
                    'json': b'{"grammar":"json","rev":3}',
                    'markdown': b'{"grammar":"markdown","rev":2}'}
    BUNDLE_MANIFEST = (b'{"bundle":"opensip-grammar-bundle","grammars":3,'
                       b'"parser":"opensip-grammar","rev":7}')
    NORMALIZER_SPEC = (b'opensip normalizer specification\nnormalizerId: opensip-normalizer\n'
                       b'normalizerVersion: 1.1.0\n'
                       b'levels: L0-verbatim L1-lexical L2-comment-insensitive '
                       b'L3-identifier-insensitive\n'
                       b'levelSpecifications: normalizer/L0-verbatim.spec '
                       b'normalizer/L1-lexical.spec\n')
    grammar_tree = ([('grammars/%s.json' % lid, by) for lid, by in GRAMMAR_DEFS.items()]
                    + [('bundle-manifest.json', BUNDLE_MANIFEST),
                       ('normalizer/spec.json', NORMALIZER_SPEC),
                       ('normalizer/L0-verbatim.spec', L0_SPEC),
                       ('normalizer/L1-lexical.spec', L1_SPEC),
                       ('bin/opensip-grammar', b'\x7fELF-synthetic-grammar-bundle')])
    grammar_tid, grammar_rec, _ = b.closure(
        'grammar', '3.1.0', 3, 'macos-aarch64', grammar_tree, 'opensip-grammar-bundle')
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
        FILES, config, scope_desc, vcs_kind='none', commit_id=None, dirty=False)

    # ---------------------------------------------------------------- native context (syntax)
    greg = json.load(open(B.KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
        'x-opensip-grammar-capability-registry']
    langs = greg['languages']
    gram_rows = []
    for lid in ('javascript', 'json', 'markdown'):
        gb = GRAMMAR_DEFS[lid]      # the exact bytes that are members of the grammar tree
        gram_rows.append({'grammarId': 'g.' + lid, 'grammarVersion': '1.0.0',
                          'languageId': lid, 'syntaxClass': langs[lid]['syntaxClass'],
                          'suffixes': sorted(langs[lid]['suffixes'],
                                             key=lambda s: s.encode()),
                          'grammarDigest': K.raw_sha256(gb)})
    gram_rows.sort(key=lambda r: r['grammarId'].encode())
    # a digest that IS globally retained in the store but is NOT a grammar-tree member:
    # used by the negative controls that separate the two obligations
    NON_TREE_BUT_RETAINED = K.raw_sha256(FILES['README.md'])
    if MUTATE.get('syntaxClass-mismatch'):
        for r in gram_rows:
            if r['languageId'] == 'json':
                r['syntaxClass'] = 'code'
    if MUTATE.get('suffix-ambiguous'):
        for r in gram_rows:
            if r['languageId'] == 'json':
                r['suffixes'] = sorted(set(r['suffixes']) | {'.js'}, key=lambda s: s.encode())
    if MUTATE.get('grammarDigest-not-in-tree'):
        for r in gram_rows:
            if r['languageId'] == 'javascript':
                r['grammarDigest'] = NON_TREE_BUT_RETAINED
    bundle = {'schemaVersion': 1, 'closureId': grammar_tid,
              'parserName': 'opensip-grammar', 'parserVersion': grammar_rec['semanticVersion'],
              'bundleDigest': K.raw_sha256(BUNDLE_MANIFEST), 'grammars': gram_rows,
              'normalizer': {'normalizerId': 'opensip-normalizer',
                             'normalizerVersion': '1.1.0',
                             'specificationDigest': K.raw_sha256(NORMALIZER_SPEC)}}
    if MUTATE.get('bundleDigest-not-in-tree'):
        bundle['bundleDigest'] = NON_TREE_BUT_RETAINED
    if MUTATE.get('normalizerSpec-not-in-tree'):
        bundle['normalizer']['specificationDigest'] = NON_TREE_BUT_RETAINED
    if MUTATE.get('parserVersion-mismatch'):
        bundle['parserVersion'] = '9.9.9'
    if MUTATE.get('grammar-closure-kind-wrong'):
        bundle['closureId'] = provider_tid
    ctx = {'schemaVersion': 2, 'grammarBundle': bundle}
    ctx_hex = b.native_framed('native.context.syntax.v2', B.NATIVE_DOC,
                              '#/$defs/SyntaxNativeContextV2', ctx, 'native-context:syntax')

    sel_ids = sorted([r['grammarId'] for r in gram_rows], key=lambda s: s.encode())
    if MUTATE.get('selection-not-in-bundle'):
        sel_ids = sorted(sel_ids + ['g.yaml'], key=lambda s: s.encode())
    universe = {'schemaVersion': 2, 'nativeContextId': 'sha256:' + ctx_hex,
                'selectedGrammarIds': sel_ids,
                'resolutionAttempted': False}
    uni_hex = b.native_framed('native.semantic-universe.syntax.v2', B.NATIVE_DOC,
                              '#/$defs/SyntaxUniverseV2ResolvedInputs', universe,
                              'native-universe:syntax')

    # ---------------------------------------------------------------- capability manifest
    A = CM.CapabilityManifestAdmitter()
    cap = {'schemaVersion': 1, 'profile': FX.PROFILE['syntax-code'],
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
    # the `syntax` capability covers declares/literal/control-flow, so the provider returns
    # every one of those relations rather than leaving an unreturned pair that the
    # execution-inputs derivation would read as native-work-incomplete
    for path, src, sym in (('src/a.js', A_SRC, 'js:src/a.js#f'),
                           ('src/b.js', B_SRC, 'js:src/b.js#g')):
        lit = src.index(b'1')
        mk_fact('literal', 'syntactic',
                {'owner': sym, 'literalKind': 'number', 'valueText': '1'},
                [anchor(path, (lit, lit + 1))], 'literal:' + path)
        ret = src.index(b'return')
        mk_fact('control-flow', 'syntactic',
                {'from': sym, 'to': sym, 'edgeKind': 'return'},
                [anchor(path, (ret, ret + len(b'return')))], 'control-flow:' + path)
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
    SYMS2 = ['js:src/a.js#f', 'js:src/b.js#g']
    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', SYMS2, 'declares-syntactic')
    s_lit, c_lit = mk_scope_cov('literal', 'syntactic', SYMS2, 'literal-syntactic')
    s_cf, c_cf = mk_scope_cov('control-flow', 'syntactic', SYMS2, 'control-flow-syntactic')
    s_clone, c_clone = mk_scope_cov('clones', 'normalized-body-hash',
                                    ['src/a.js', 'src/b.js'], 'clones-normalized')
    # this subject is an unpacked source tree with no version control, so the admitted
    # vcs-observation is kind=none -- which is exactly the published basis for the
    # `inapplicable-vcs` account applicability
    s_vcs = c_vcs = None

    # ---------------------------------------------------------------- enumeration plan
    # CORRECTED (V18-D2). native-evidence section 1.4 U-1 yields exactly one `tsjs` unit for a
    # directory holding tsconfig.json > jsconfig.json > package.json, and this subject holds
    # package.json -- so a unit IS derivable here and the record must say so. Two further
    # clauses decide the rest:
    #   U-3 "A file's family is fixed by EXTENSION (.rs -> rust; .ts/.tsx/.mts/.cts/.js/.mjs/
    #       .cjs/.jsx -> tsjs)" -- so the .js files belong to that unit, while .json/.md and an
    #       extensionless file have NO family and therefore no unit;
    #   U-4 a file with no family unit is `syntax-only` with `unitOrdinal: null` -- "not a
    #       member of an invented unit".
    # The earlier record invented a single unit of family `none` and pointed EVERY row at it,
    # which is the shape U-4 names and forbids. The `syntax-only` ANALYSIS needs no compilation
    # unit ("syntax-only carries no such prerequisite"), so membership being snapshot-derived
    # and selection-independent is not a contradiction. The charter's
    # R-RUN-NO-COMPILER-UNIT exhibit moves to the syntax-data Run, whose snapshot holds NO U-1
    # marker at all and therefore genuinely derives no unit.
    TSJS_SUFFIX = ('.ts', '.tsx', '.mts', '.cts', '.js', '.mjs', '.cjs', '.jsx')
    membership = {
        'schemaVersion': 1,
        'units': [{'unitOrdinal': 0, 'rootPath': '', 'languageFamily': 'tsjs',
                   'languageMode': 'js-synthesized', 'unitKind': 'js-program',
                   'markerPath': 'package.json',
                   'markerSha256': K.raw_sha256(FILES['package.json']),
                   'recognizerId': 'opensip-tsjs-recognizer', 'recognizerVersion': 1,
                   'provenance': 'DISCOVERED', 'memberPackageRoots': []}],
        'rows': [{'path': p,
                  'languageFamily': 'tsjs' if p.endswith(TSJS_SUFFIX) else 'none',
                  'unitOrdinal': 0 if p.endswith(TSJS_SUFFIX) else None,
                  'membership': ('program-member' if p.endswith(TSJS_SUFFIX)
                                 else 'syntax-only'
                                 if p.split('.')[-1] in ('json', 'md') and '.' in p
                                 else 'unsupported-file'),
                  'reason': ('deepest-unit-in-language' if p.endswith(TSJS_SUFFIX)
                             else 'grammar-only'
                             if p.split('.')[-1] in ('json', 'md') and '.' in p
                             else 'no-bundled-grammar')}
                 for p in sorted(FILES, key=lambda s: s.encode())],
        'unsupportedFiles': ['LICENSE'],
        'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    if MUTATE.get('invent-a-unit-no-marker-derives'):
        membership['units'] = membership['units'] + [
            {'unitOrdinal': 1, 'rootPath': 'src', 'languageFamily': 'none',
             'languageMode': 'syntax-only', 'unitKind': 'syntax-only',
             'markerPath': '', 'markerSha256': None,
             'recognizerId': 'opensip-syntax-recognizer', 'recognizerVersion': 1,
             'provenance': 'DEFAULTED', 'memberPackageRoots': []}]
    if MUTATE.get('row-family-not-fixed-by-extension'):
        for r in membership['rows']:
            if r['path'] == 'package.json':
                r['languageFamily'] = 'tsjs'
                r['unitOrdinal'] = 0
    if MUTATE.get('membership-row-missing-for-a-snapshot-path'):
        # section 8: "Membership rows must EXACTLY COVER snapshot paths (host TCB); a missing
        # row is not a silent exclude."
        membership['rows'] = [r for r in membership['rows'] if r['path'] != 'LICENSE']
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    def binding(ordinal, extents, candidate_paths=None, unavailable=None):
        r = {'ordinal': ordinal, 'provenance': 'default-unit' if ordinal == 0
             else 'explicit-plan-selection',
             'enumerator': {'status': 'selected', 'closureId': provider_tid},
             'nativeContextDigest': ctx_hex, 'universe': uni_hex,
             # a default-unit binding carries a NULL programEntry (U-1 default uses null);
             # the control below asserts a non-null one is refused
             'programEntry': ('README.md'
                              if (ordinal == 0
                                  and MUTATE.get('default-unit-names-a-program-entry'))
                              else None),
             'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                for k, v in extents.items()],
                               key=lambda e: e['kind'].encode())}
        if candidate_paths is not None:
            r['candidateSourcePaths'] = sorted(candidate_paths, key=lambda s: s.encode())
        if unavailable:
            # CORRECTED (V17-D5): enumeration-contract section 1, UNAVAILABLE binding --
            # "`extents` STILL POPULATED from host membership so expected file/package paths
            # are not lost", and for symbol the unavailable-program extent is "the
            # membership-fallback code extent (explicit law), never arbitrary caller paths".
            # The earlier `extents: []` here lost the expected paths and, with the missing
            # inventory below, made the unavailable cell look like work that was never owed.
            r = {'ordinal': ordinal,
                 'provenance': 'default-unit' if ordinal == 0 else 'explicit-plan-selection',
                 'enumerator': {'status': 'unselected', 'reason': 'optional-unselected'},
                 'nativeContextDigest': ctx_hex, 'universe': None, 'programEntry': None,
                 'extents': sorted([{'kind': k,
                                     'paths': sorted(v, key=lambda s: s.encode())}
                                    for k, v in (extents or {}).items()],
                                   key=lambda e: e['kind'].encode()),
                 'deficiency': unavailable[0], 'nativeCause': unavailable[1]}
        return r

    all_paths = sorted(FILES, key=lambda s: s.encode())
    code_paths = ['src/a.js', 'src/b.js']
    # ---- enumeration-law negative-control hooks, applied at BUILD time so the whole graph
    # is reminted and reclosed. Each one is a lawful-looking record that a specific published
    # enumeration clause refuses.
    EM = MUTATE
    file_extent = code_paths if EM.get('file-extent-compiler-filtered') else all_paths
    pkg_extent = (['package.json', 'workspace-only.json']
                  if EM.get('package-extent-includes-a-nameless-manifest')
                  else ['package.json'])
    cells = [
        # CORRECTED (V17-D4): the FILE kind extent is first-party scoped snapshot MEMBERSHIP,
        # independent of which paths a grammar or compiler can read
        {'capabilityId': 'clones-fact', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': ['file'],
         'programBindings': [binding(0, {'file': file_extent})]},
        {'capabilityId': 'inventory', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True,
         'kinds': (['file'] if EM.get('inventory-cell-kinds-consumer-subset')
                   else sorted(['file', 'package'], key=lambda s: K.C(s))),
         'programBindings': [binding(0, ({'file': all_paths}
                                         if EM.get('inventory-cell-kinds-consumer-subset')
                                         else {'file': all_paths,
                                               'package': pkg_extent}))]},
        {'capabilityId': 'syntax', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'],
         'programBindings': [binding(0, {'symbol': code_paths})]},
        {'capabilityId': 'unresolved-edge', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': False, 'kinds': ['symbol'],
         'programBindings': [binding(0, ({} if EM.get('unavailable-binding-drops-extents')
                                         else {'symbol': code_paths}),
                                     # CORRECTED (V18-D5): the deficiency-cause registry row
                                     # for `language-tier-unsupported` is carrier
                                     # `entry.nativeCause`, nativeCause REQUIRED, with
                                     # allowedCauses ['capability-missing']. A null cause here
                                     # was an unmade disclosure, and section 1 says the
                                     # binding's nativeCause is "a NativeCause member OR null
                                     # AS THAT DEFICIENCY'S CARRIER LAW REQUIRES".
                                     unavailable=(
                                         ('language-tier-unsupported', None)
                                         if MUTATE.get('binding-carrier-required-cause-null')
                                         else ('language-tier-unsupported',
                                               'capability-missing')))]},
    ]
    if EM.get('duplicate-universe-inside-one-cell'):
        for c in cells:
            if c['capabilityId'] == 'clones-fact':
                dup = dict(c['programBindings'][0])
                dup['ordinal'] = 1
                dup['provenance'] = 'explicit-plan-selection'
                c['programBindings'] = c['programBindings'] + [dup]
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
               native_cause=None, prog=0):
        inv = {'schemaVersion': 1, 'planId': 'plan2:' + '0' * 64,
               'parameterDigest': enum_plan_dig, 'cellOrdinal': cell_ord[cap_id],
               'programOrdinal': prog, 'kind': kind, 'state': state,
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

    inv_specs = [('inventory', 'file',
                  ([r for r in file_rows if r['path'] != 'README.md']
                   if EM.get('file-inventory-drops-an-extent-path') else file_rows),
                  all_paths),
                 ('inventory', 'package', pkg_rows, ['package.json']),
                 ('syntax', 'symbol', sym_rows, code_paths),
                 # CORRECTED (V17-D4): the clones-fact FILE inventory owes the WHOLE file
                 # extent (section 4 file totality), not the code subset
                 ('clones-fact', 'file', file_rows, all_paths),
                 # CORRECTED (V17-D5): enumeration-contract sections 3/4 and
                 # execution-inputs section 6 require EXACTLY ONE SubjectInventoryV1 per
                 # (cellOrdinal, programOrdinal, kind) of cell.kinds with NO available-only
                 # qualifier, and section 4 gives the unavailable shape: rows=[],
                 # examinedPaths=[], deficiency non-null matching the binding carrier.
                 # "Unselected or `universe=null` does not discard same-cell inventory
                 # items." A MISSING record is not a retained unavailable record.
                 ('unresolved-edge', 'symbol', [], [], 'unavailable',
                  # the inventory carries its OWN pair, and it must satisfy the same owner
                  # carrier law (V18-D5)
                  'language-tier-unsupported', 'capability-missing')]
    if EM.get('drop-the-unavailable-inventory'):
        inv_specs = [s for s in inv_specs if s[0] != 'unresolved-edge']
    if EM.get('duplicate-universe-inside-one-cell'):
        # the duplicated binding owes its OWN inventory; supplying it is what makes the
        # DUPLICATE-UNIVERSE law the first refusal instead of a missing-record prerequisite
        inv_specs = inv_specs + [('clones-fact', 'file', file_rows, all_paths, 'complete',
                                  None, None, 1)]
    # ---- carrier-pair controls (area 2). Each replaces ONE inventory's own (state,
    # deficiency, nativeCause) triple, leaving every other record lawful, so the refusal that
    # appears is the carrier law and not a prerequisite.
    CARRIER = {
        'carrier-required-cause-is-null': ('unresolved-edge', 'symbol', 'unavailable',
                                           'language-tier-unsupported', None),
        'carrier-cause-not-in-allowed-set': ('unresolved-edge', 'symbol', 'unavailable',
                                             'language-tier-unsupported', 'lockfile-missing'),
        'carrier-must-be-null-cause-present': ('unresolved-edge', 'symbol', 'unavailable',
                                               'budget-exhausted', 'capability-missing'),
        'carrier-local-member-with-a-cause': ('unresolved-edge', 'symbol', 'unavailable',
                                              'source-syntax-invalid', 'capability-missing'),
        'carrier-complete-inventory-with-a-deficiency': ('inventory', 'file', 'complete',
                                                         'budget-exhausted', None),
        'carrier-cause-without-a-deficiency': ('inventory', 'file', 'complete', None,
                                               'capability-missing'),
    }
    for key, (cap, kind, state_, dfc, cause) in CARRIER.items():
        if not EM.get(key):
            continue
        patched = []
        for spec in inv_specs:
            if spec[0] == cap and spec[1] == kind:
                patched.append((spec[0], spec[1], spec[2], spec[3], state_, dfc, cause)
                               + tuple(spec[7:]))
            else:
                patched.append(spec)
        inv_specs = patched
    if EM.get('two-inventories-for-one-cell-program-kind'):
        # a SECOND, byte-DIFFERENT inventory at the same (cell, program, kind): a duplicate of
        # identical bytes would collapse to one digest and be caught by the schema's
        # uniqueItems instead of by the cardinality law
        inv_specs = inv_specs + [
            ('inventory', 'file', [r for r in file_rows if r['path'] != 'LICENSE'],
             [p for p in all_paths if p != 'LICENSE'])]
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
                view_parts=dict(scopes=[s_file, s_pkg, s_decl, s_lit, s_cf, s_clone],
                                coverages=[c_file, c_pkg, c_decl, c_lit, c_cf, c_clone]),
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
