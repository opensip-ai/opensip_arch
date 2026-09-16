"""Complete positive syntax-only Run over a BUNDLED DATA/DOCUMENT grammar set.

  R-RUN-SYNTAX-DATA          inventory capability present; every capability the class does
                             not support is an EXPLICIT UNAVAILABILITY disclosure, never a
                             complete empty result
  R-RUN-UNAVAILABLE-SEMANTIC the published deficiency / nativeCause pairing on each
                             unsupported request
  R-RUN-UNSUPPORTED-GRAMMAR  an unbundled language (`tool/main.py`) is inventoried and
                             accounted as unsupported-file / no-bundled-grammar, with NO
                             TypeScript compiler anywhere in the graph

native-evidence section 1.2 `data-document`: "Their files are grammar-only members --
accounted, inventoried, and never `unsupported-file` -- bearing file/package/vcs-change
inventory evidence under the syntax universe. They mint NO body identity ... A clone or
code-construct request against it is explicitly UNAVAILABLE (language-tier-unsupported for
that capability), never a complete empty clone result, which would read as a finding of no
clones."
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
import opensip_closure as CL
import opensip_capmanifest as CM
import run_ts_full as TSF

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
MUTATE = {}

import opensip_fixture as FX
PROJECT_ID = FX.PROJECT_ID['syntax-data']

FILES = {
    'LICENSE': b'MIT\n',
    'README.md': b'# data-only subject\n\nNo TypeScript and no Rust unit exists here.\n',
    'data/config.yaml': b'retention:\n  mode: durable\n',
    'data/values.json': b'{"threshold":3,"mode":"strict"}\n',
    'settings.toml': b'[limits]\nmax = 10\n',
    'tool/main.py': b'def main():\n    return 0\n',
}

L0_SPEC = (b'opensip level specification\nlevel: L0-verbatim\n'
           b'lexical-boundary: none (tokenisation forbidden)\n'
           b'token-kind-registry: none\ndirective-classification: none\n'
           b'transform-order: []\nreplacement-bytes: none\nlanguages: none\n')
NORMALIZER_SPEC = (b'opensip normalizer specification\nnormalizerId: opensip-normalizer\n'
                   b'normalizerVersion: 1.1.0\n'
                   b'levels: L0-verbatim L1-lexical\n'
                   b'levelSpecifications: normalizer/L0-verbatim.spec\n')
DATA_LANGS = ('json', 'markdown', 'toml', 'yaml')


def build():
    b = B.Builder(PROJECT_ID)
    st = b.st
    for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.POLICY_V2_DOC, B.POLICY_V1_DOC,
              B.ENUM_PLAN_DOC, B.EMIT_PLAN_DOC, B.SUBJ_INV_DOC, B.EXEC_IN_DOC):
        b.retain_schema_doc(d)

    # ---- grammar closure: every grammar definition, the bundle manifest and the normalizer
    # specification are MEMBERS of this retained tree (native-evidence section 1.2), as well
    # as globally retained.
    GRAMMAR_DEFS = {lid: b'{"grammar":"%s","rev":4}' % lid.encode() for lid in DATA_LANGS}
    BUNDLE_MANIFEST = (b'{"bundle":"opensip-grammar-bundle","grammars":4,'
                       b'"parser":"opensip-grammar","rev":11}')
    tree = ([('grammars/%s.json' % lid, by) for lid, by in GRAMMAR_DEFS.items()]
            + [('bundle-manifest.json', BUNDLE_MANIFEST),
               ('normalizer/spec.json', NORMALIZER_SPEC),
               ('normalizer/L0-verbatim.spec', L0_SPEC),
               ('bin/opensip-grammar', b'\x7fELF-synthetic-grammar-bundle')])
    grammar_tid, grammar_rec, _ = b.closure('grammar', '3.1.0', 3, 'macos-aarch64', tree,
                                            'opensip-grammar-bundle')
    provider_tid, _, _ = b.closure(
        'provider', '2.4.0', 3, 'macos-aarch64',
        [('bin/opensip-syntax-provider', b'\x7fELF-synthetic-syntax-provider')],
        'opensip-syntax-provider')
    evaluator_tid, _, _ = b.closure(
        'evaluator', '3.0.0', 3, 'macos-aarch64',
        [('bin/opensip-evaluator', b'\x7fELF-synthetic-pure-evaluator')], 'opensip-evaluator')
    detector_tid, _, _ = b.closure(
        'detector', '1.0.0', 3, 'macos-aarch64',
        [('rules/data-hygiene.json', b'{"detector":"data-hygiene","rev":1}')],
        'opensip-data-hygiene-detector')

    config = {
        'analysis': {'profileId': 'syntax-only-data',
                     'capabilities': sorted(['inventory', 'syntax', 'clones-fact', 'imports'],
                                            key=lambda s: K.C(s)),
                     'budget': {'unit': 'work-units', 'limit': 5000000}},
        'components': {'request': [{'stableId': '44444444-5555-4666-8777-888888888888',
                                    'version': '3.1.0'}],
                       'allowedScopes': ['project', 'global']},
        'discovery': {'workspaceRoots': ['.']},
        'policy': {'packIds': ['pack.data-hygiene']}, 'evidence': {},
    }
    scope_desc = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': [],
                  'excludedPathPrefixes': []}
    snapshot_id, snapshot, sh = b.snapshot(FILES, config, scope_desc, vcs_kind='none',
                                           commit_id=None, dirty=False)

    greg = json.load(open(B.KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
        'x-opensip-grammar-capability-registry']
    langs = greg['languages']
    gram_rows = sorted([{'grammarId': 'g.' + lid, 'grammarVersion': '1.0.0',
                         'languageId': lid, 'syntaxClass': langs[lid]['syntaxClass'],
                         'suffixes': sorted(langs[lid]['suffixes'], key=lambda s: s.encode()),
                         'grammarDigest': K.raw_sha256(GRAMMAR_DEFS[lid])}
                        for lid in DATA_LANGS], key=lambda r: r['grammarId'].encode())
    bundle = {'schemaVersion': 1, 'closureId': grammar_tid, 'parserName': 'opensip-grammar',
              'parserVersion': grammar_rec['semanticVersion'],
              'bundleDigest': K.raw_sha256(BUNDLE_MANIFEST), 'grammars': gram_rows,
              'normalizer': {'normalizerId': 'opensip-normalizer',
                             'normalizerVersion': '1.1.0',
                             'specificationDigest': K.raw_sha256(NORMALIZER_SPEC)}}
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

    A = CM.CapabilityManifestAdmitter()
    cap = {'schemaVersion': 1, 'profile': FX.PROFILE['syntax-data'],
           'providers': [{'providerId': 'opensip.provider.syntax', 'language': 'syntax',
                          'providerVersionSource': 'closure2.semanticVersion',
                          'toolchainIdentitySource': 'grammar-bundle',
                          'relations': {'file': 'enumerated',
                                        'package': 'manifest-declared',
                                        'vcs-change': 'vcs-reported'},
                          'platformIds': ['macos-aarch64']}],
           'coverageForAbsent': [{'providerId': 'opensip.provider.syntax',
                                  'language': 'syntax',
                                  'relationIds': sorted(
                                      ['calls', 'clones', 'control-flow', 'declares',
                                       'imports', 'literal', 'reachability', 'references',
                                       'types', 'unresolved-edge'],
                                      key=lambda s: s.encode()),
                                  'coverageState': 'unavailable',
                                  'deficiency': 'language-tier-unsupported'}]}
    capres = A.admit(cap)
    assert capres['admitted']
    st.put_blob(capres['committedBytes'], label='capability-manifest-artifact')

    # ---- facts: INVENTORY ONLY. No body identity, no code-construct fact.
    facts, fact_payloads = {}, {}
    all_paths = sorted(FILES, key=lambda s: s.encode())
    for p in all_paths:
        row = [r for r in sh['inventory'] if r['path'] == p][0]
        fid = b.fact(snapshot_id, 'file', 'enumerated', uni_hex, uni_hex, provider_tid,
                     {'path': p, 'contentSha256': row['sha256'], 'byteLength': row['bytes']},
                     [], 1000000, 'file:' + p)
        facts[fid] = st.objects[fid]
        fact_payloads[fid] = {'path': p, 'contentSha256': row['sha256'],
                              'byteLength': row['bytes']}

    scopes, coverages, coverage_payloads = {}, {}, {}

    def mk(relation, rung, subjects, label, cov, deficiency, native_cause, rc=None,
           exhaustive=True):
        sid = b.scope(snapshot_id, relation, rung, uni_hex, uni_hex, provider_tid,
                      subjects, label)
        scopes[sid] = st.objects[sid]
        r = rc or B.rc_not_applicable()
        r['examinedExhaustive'] = exhaustive
        ent = B.entry(cov, B.closed_world_open(
            ['grammar-only data/document analysis; no resolution attempted']),
            deficiency=deficiency, native_cause=native_cause, rc=r)
        cid = b.coverage(sid, ent, label)
        coverages[cid] = st.objects[cid]
        coverage_payloads[cid] = json.loads(
            st.get_blob(st.objects[cid]['payloadDigest']).decode())
        return sid, cid

    # inventory capability: genuinely COMPLETE, with no deficiency
    s_file, c_file = mk('file', 'enumerated', all_paths, 'file-enumerated',
                        'complete', None, None)
    # a first-party manifest inventory with no manifests is a lawful COMPLETE-EMPTY
    # inventory result -- contrast this with the unsupported capabilities below
    s_pkg, c_pkg = mk('package', 'manifest-declared', [], 'package-declared-empty',
                      'complete', None, None)
    # capabilities this class cannot serve: EXPLICIT UNAVAILABILITY, never complete-empty
    s_clone, c_clone = mk('clones', 'normalized-body-hash', all_paths, 'clones-unavailable',
                          'unknown', 'language-tier-unsupported', 'capability-missing',
                          exhaustive=False)
    s_decl, c_decl = mk('declares', 'syntactic', [], 'declares-unavailable',
                        'unknown', 'language-tier-unsupported', 'capability-missing',
                        exhaustive=False)
    # the `syntax` capability covers three relations; every one of them is disclosed, so no
    # pair is left unreturned for the derivation to read as native-work-incomplete
    s_lit, c_lit = mk('literal', 'syntactic', [], 'literal-unavailable',
                      'unknown', 'language-tier-unsupported', 'capability-missing',
                      exhaustive=False)
    s_cf, c_cf = mk('control-flow', 'syntactic', [], 'control-flow-unavailable',
                    'unknown', 'language-tier-unsupported', 'capability-missing',
                    exhaustive=False)
    # a RESOLVED rung under a syntax universe: RC-1 forbids not-applicable, and
    # resolutionAttempted=false makes `not-attempted` the honest state
    s_imp, c_imp = mk('imports', 'resolved-target', [], 'imports-unavailable',
                      'unknown', 'language-tier-unsupported', 'capability-missing',
                      rc={'state': 'not-attempted', 'attempted': False,
                          'examinedExhaustive': False, 'stageTerminal': None,
                          'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []},
                      exhaustive=False)
    return dict(b=b, st=st, snapshot_id=snapshot_id, snapshot=snapshot, sh=sh,
                closures=dict(grammar=grammar_tid, provider=provider_tid,
                              evaluator=evaluator_tid, detector=detector_tid),
                ctx_hex=ctx_hex, uni_hex=uni_hex, universe_digests=[uni_hex],
                cap=cap, capres=capres, config=config, files=FILES, all_paths=all_paths,
                facts=facts, fact_payloads=fact_payloads, scopes=scopes,
                coverages=coverages, coverage_payloads=coverage_payloads,
                gram_rows=gram_rows, bundle=bundle,
                view_parts=dict(
                    scopes=[s_file, s_pkg, s_clone, s_decl, s_lit, s_cf, s_imp],
                    coverages=[c_file, c_pkg, c_clone, c_decl, c_lit, c_cf, c_imp]))


def policy_document():
    rules = [
        {'ruleId': 'rule.a-no-duplicate-body',
         'ruleProgramRef': {'contributionId': 'contrib.data-hygiene',
                            'ruleStableId': 'data-hygiene.no-duplicate-body',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'data.no-duplicate-body.v1')},
         'enabled': True, 'severity': 'error', 'gate': True,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
         'emitWhen': {'op': 'none', 'relation': 'clones',
                      'minResolution': 'normalized-body-hash', 'filters': []},
         'evidenceUse': [], 'messageCode': 'clones.duplicate-body'},
        {'ruleId': 'rule.b-file-inventoried',
         'ruleProgramRef': {'contributionId': 'contrib.data-hygiene',
                            'ruleStableId': 'data-hygiene.file-inventoried',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'data.file-inventoried.v1')},
         'enabled': True, 'severity': 'note', 'gate': False,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
         'emitWhen': {'op': 'exists', 'relation': 'file', 'minResolution': 'enumerated',
                      'filters': []},
         'evidenceUse': [], 'messageCode': 'file.inventoried'},
    ]
    rules.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2,
            'gateSeverityAtLeast': 'warning', 'rules': rules}


def complete(g):
    b, st, sh = g['b'], g['st'], g['sh']
    cl, snapshot_id, uni, ctx_hex = (g['closures'], g['snapshot_id'], g['uni_hex'],
                                     g['ctx_hex'])
    policy = policy_document()
    policy_dig = b.record(B.POLICY_V2_DOC, '#/$defs/PolicyDocumentV2', policy, 'policy')
    waivers = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}
    waiver_dig = b.record(B.POLICY_V1_DOC, '#/$defs/WaiverSetV1', waivers, 'waivers')
    rule_program = CO.build_rule_program(policy)
    b.record(B.POLICY_V2_DOC, '#/$defs/RuleProgramV2', rule_program, 'rule-program')
    emit = {'schemaVersion': 1, 'policyDigest': K.rec_digest(policy),
            'rules': sorted([{'ruleId': r['ruleId'],
                              'contributionId': r['ruleProgramRef']['contributionId'],
                              'ruleStableId': r['ruleProgramRef']['ruleStableId'],
                              'semanticsMajor': r['ruleProgramRef']['semanticsMajor'],
                              'detectorClosure': cl['detector'],
                              'stabilityClass': 'path-stable',
                              'emissionProfile': 'declarative-subject-v1'}
                             for r in policy['rules']],
                            key=lambda r: r['ruleId'].encode())}
    emit_dig = b.record(B.EMIT_PLAN_DOC, '#', emit, 'emission-plan')

    all_paths = g['all_paths']
    DATA_SUFFIX = {'.json': 'json', '.md': 'markdown', '.toml': 'toml',
                   '.yaml': 'yaml', '.yml': 'yaml'}

    def subj_lang(p):
        for suf, lid in sorted(DATA_SUFFIX.items(), key=lambda t: -len(t[0])):
            if p.endswith(suf):
                return lid
        return 'unspecified'

    def membership_of(p):
        if subj_lang(p) != 'unspecified':
            return 'syntax-only', 'grammar-only'
        return 'unsupported-file', 'no-bundled-grammar'

    # CORRECTED (V18-D2). This snapshot holds NO U-1 marker -- no tsconfig.json, no
    # jsconfig.json, no package.json, no Cargo.toml -- so native-evidence section 1.4 derives
    # NO unit, and section 1.4 states the consequence directly: "A file reached that way is
    # `syntax-only` membership with `unitOrdinal: null` under U-4, NOT A MEMBER OF AN INVENTED
    # UNIT." The earlier record invented a `syntax-only` unit of family `none` and pointed every
    # row at it. THIS Run is therefore the honest carrier of the charter's
    # R-RUN-NO-COMPILER-UNIT property: no compilation unit is derivable from its snapshot at
    # all, rather than merely unused.
    membership = {
        'schemaVersion': 1,
        'units': [],
        'rows': [{'path': p, 'languageFamily': 'none', 'unitOrdinal': None,
                  'membership': membership_of(p)[0], 'reason': membership_of(p)[1]}
                 for p in all_paths],
        'unsupportedFiles': sorted([p for p in all_paths
                                    if membership_of(p)[0] == 'unsupported-file'],
                                   key=lambda s: s.encode()),
        'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    def binding(extents):
        return {'ordinal': 0, 'provenance': 'default-unit',
                'enumerator': {'status': 'selected', 'closureId': cl['provider']},
                'nativeContextDigest': ctx_hex, 'universe': uni, 'programEntry': None,
                'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                   for k, v in extents.items()],
                                  key=lambda e: e['kind'].encode())}

    cells = [
        {'capabilityId': 'clones-fact', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': False, 'kinds': ['file'],
         'programBindings': [binding({'file': all_paths})]},
        # GENERATION 20: this cell is now REQUESTED AS REQUIRED, deliberately. The matrix cell
        # (imports, syntax-only) is UNSUPPORTED-TYPED, so under the newly frozen first-match order
        # its account is `unsupported-typed` with EMPTY coverageIds, and section 5 says such an
        # account is ANSWERED: the cell outcome derives to `complete`. Making it required exercises
        # the distinctive consequence the same clause publishes -- "a required such cell
        # additionally emits a requiredCellDeficiencies row that bridges to proof (section 9.6) and
        # holds the Run at indeterminate" -- i.e. a COMPLETE execution row that still carries a
        # required-execution deficiency. No positive Run exercised that before.
        {'capabilityId': 'imports', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'], 'programBindings': [binding({'symbol': []})]},
        {'capabilityId': 'inventory', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': True, 'kinds': sorted(['file', 'package'], key=lambda s: K.C(s)),
         'programBindings': [binding({'file': all_paths, 'package': []})]},
        {'capabilityId': 'syntax', 'languageMode': 'syntax-only', 'workspaceRoot': '.',
         'required': False, 'kinds': ['symbol'], 'programBindings': [binding({'symbol': []})]},
    ]
    cells.sort(key=lambda c: (c['capabilityId'].encode(), c['languageMode'].encode(),
                              c['workspaceRoot'].encode()))
    enum_plan = {'schemaVersion': 1, 'snapshotId': snapshot_id,
                 'scopeDigest': sh['scopeDigest'], 'membershipDigest': membership_dig,
                 'cells': cells}
    enum_plan_dig = b.record(B.ENUM_PLAN_DOC, '#', enum_plan, 'enumeration-plan')
    cell_ord = {c['capabilityId']: i for i, c in enumerate(cells)}
    reqcaps = sorted([{'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
                       'workspaceRoot': c['workspaceRoot'], 'required': c['required']}
                      for c in cells], key=lambda r: K.C(r))
    params = sorted([
        {'schemaDigest': B.doc_sha(B.ENUM_PLAN_DOC), 'payloadDigest': enum_plan_dig},
        {'schemaDigest': B.doc_sha(B.EMIT_PLAN_DOC), 'payloadDigest': emit_dig},
    ], key=lambda r: K.C(r))
    spec = {'schemaVersion': 2, 'requestedCapabilities': reqcaps,
            'policyPackIds': ['pack.data-hygiene'], 'parameters': params}
    spec_dig = b.record(B.IDENTITY_DOC, '#/$defs/analysis-spec', spec, 'analysis-spec')
    grant = {'schemaVersion': 2, 'projectId': g['snapshot']['projectId'],
             'principals': K.cset([{'kind': 'first-party', 'closureId': cl['provider'],
                                    'ownerSourceDigest': None},
                                   {'kind': 'first-party', 'closureId': cl['evaluator'],
                                    'ownerSourceDigest': None}]),
             'analysisOperations': sorted(['read-source', 'native-analysis'],
                                          key=lambda s: K.C(s)),
             'scopeDigest': sh['scopeDigest']}
    grant_dig = b.record(B.IDENTITY_DOC, '#/$defs/semantic-grant', grant, 'semantic-grant')
    plan = {'schemaVersion': 2, 'snapshotId': snapshot_id,
            'capabilityManifestId': g['capres']['capabilityManifestId'],
            'semanticClosures': K.cset_strings([cl['provider'], cl['evaluator'],
                                                cl['detector']]),
            'analysisSpecDigest': spec_dig, 'resolvedConfigDigest': sh['configDigest'],
            'nativeContextDigests': [ctx_hex], 'importIds': [],
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDigest': sh['scopeDigest'],
            'budget': dict(g['config']['analysis']['budget']),
            'semanticGrantDigest': grant_dig,
            'capabilityManifestBytesDigest': g['capres']['committedBytesSha256']}
    plan_id = b.framed('plan', B.IDENTITY_DOC, '#/$defs/plan', plan, 'plan')

    file_rows = sorted([{'nativeSubjectId': p, 'kind': 'file', 'path': p,
                         'qualifiedName': p, 'subjectLanguage': subj_lang(p),
                         'signatureTokens': [], 'projections': []} for p in all_paths],
                       key=lambda r: r['nativeSubjectId'].encode())
    inventories = []
    for cap_id, kind, rows, examined in (('inventory', 'file', file_rows, all_paths),
                                         ('inventory', 'package', [], []),
                                         ('clones-fact', 'file', file_rows, all_paths),
                                         ('syntax', 'symbol', [], []),
                                         ('imports', 'symbol', [], [])):
        inv = {'schemaVersion': 1, 'planId': plan_id, 'parameterDigest': enum_plan_dig,
               'cellOrdinal': cell_ord[cap_id], 'programOrdinal': 0, 'kind': kind,
               'state': 'complete', 'deficiency': None, 'nativeCause': None,
               'examinedPaths': sorted(examined, key=lambda s: K.C(s)), 'rows': rows}
        b.admit(B.SUBJ_INV_DOC, '#', inv, 'subject-inventory:%s:%s' % (cap_id, kind))
        d = st.put_record(inv, label='subject-inventory:%s:%s' % (cap_id, kind))
        inventories.append((d, inv))

    view_id = b.view(plan_id, g['view_parts']['scopes'], list(g['facts']),
                     g['view_parts']['coverages'], cl['provider'],
                     [B.doc_sha(B.RELATION_DOC), B.doc_sha(B.NATIVE_DOC)], 'syntax-data')
    stage_spec = {'schemaVersion': 2, 'planId': plan_id, 'producerClosure': cl['provider'],
                  'operation': 'syntax.analyze.v1',
                  'parameters': [p for p in params
                                 if p['schemaDigest'] == B.doc_sha(B.ENUM_PLAN_DOC)],
                  'outputDomains': sorted(['coverage', 'view'], key=lambda s: K.C(s)),
                  'outputSchemaDigest': B.doc_sha(B.NATIVE_DOC)}
    stage_dig = b.record(B.IDENTITY_DOC, '#/$defs/stage-spec', stage_spec, 'stage-spec')
    exec_plan = {'schemaVersion': 2, 'planId': plan_id,
                 'stages': [{'ordinal': 0, 'stageSpecDigest': stage_dig, 'requires': [],
                             'outputDomains': stage_spec['outputDomains']}]}
    exec_plan_id = b.framed('execution-plan', B.IDENTITY_DOC, '#/$defs/execution-plan',
                            exec_plan, 'execution-plan')
    host_derived = K.cset([{'domain': 'subject-inventory', 'digest': d}
                           for d, _ in inventories])
    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(view_id)}]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])
    selected = K.cset(stage_out + host_derived)
    rel_for_cap = {'inventory': [('file', 'enumerated'), ('package', 'manifest-declared'),
                                 ('vcs-change', 'vcs-reported')],
                   'syntax': [('declares', 'syntactic'), ('literal', 'syntactic'),
                              ('control-flow', 'syntactic')],
                   'imports': [('imports', 'resolved-target')],
                   'clones-fact': [('clones', 'normalized-body-hash')]}
    # CORRECTED (V18-D8, V19-D3): the partial rows were asserted with a hand-written pair; the
    # shared section 4/5 derivation now reads them off this Run's own Coverage entries, which is
    # where `language-tier-unsupported` / `capability-missing` actually live for the data subject.
    cov_by = {}
    for cid in g['view_parts']['coverages']:
        k = g['coverage_payloads'][cid]['key']
        cov_by[(k['relation'], k['resolution'], k['sourceUniverse'])] = cid
    cell_outcomes, accounts = B.build_accounts_and_outcomes(
        st, cells, rel_for_cap, inventories, cov_by, g['coverage_payloads'],
        {uni: view_id}, cl['provider'], stage_ordinal=0, vcs_kind='none')
    exec_inputs = {
        'schemaVersion': 1, 'planId': plan_id, 'executionPlanId': exec_plan_id,
        'evaluatorClosure': cl['evaluator'], 'enumerationPlanDigest': enum_plan_dig,
        'analysisSpecDigest': spec_dig,
        'hostCapture': {'custody': 'host-tcb-evidence-store', 'observation': 'stage-return',
                        'stageReceipts': [{'ordinal': 0, 'stageSpecDigest': stage_dig,
                                           'producerClosure': cl['provider'],
                                           'outputDomains': stage_spec['outputDomains'],
                                           'outputRefs': stage_out, 'state': 'complete',
                                           'unavailableReason': None}],
                        'hostDerivedRefs': host_derived},
        'selectedRefs': selected, 'cellOutcomes': cell_outcomes,
        'nativeCoverageAccounts': accounts, 'candidateResultRefs': [],
    }
    b.admit(B.EXEC_IN_DOC, '#', exec_inputs, 'execution-inputs')
    exec_in_dig = st.put_record(exec_inputs, label='execution-inputs')

    inp = E.Inputs(st, plan_id, plan, exec_plan_id, cl['evaluator'], policy, rule_program,
                   waivers, emit, enum_plan, inventories,
                   {view_id: st.objects[view_id]}, g['facts'], g['scopes'], g['coverages'],
                   g['coverage_payloads'], g['fact_payloads'],
                   {uni: ('native.semantic-universe.syntax.v2',
                          st.objects['native.semantic-universe.syntax.v2#' + uni])},
                   {ctx_hex: ('native.context.syntax.v2',
                              st.objects['native.context.syntax.v2#' + ctx_hex])},
                   exec_inputs, snapshot=g['snapshot'])
    inp.analysis_spec = spec
    out = CO.compose(inp, st, emit, exec_in_dig, snapshot_id)
    TSF.retain_outputs(b, st, out)
    g.update(dict(policy=policy, waivers=waivers, plan=plan, plan_id=plan_id, spec=spec,
                  inventories=inventories, view_id=view_id, exec_inputs=exec_inputs,
                  exec_in_dig=exec_in_dig, out=out, inp=inp, enum_plan=enum_plan,
                  emit=emit, rule_program=rule_program))
    g['exhibits'] = exhibits(g)
    return g


def exhibits(g):
    out = g['out']
    by_rel = {}
    for cid in g['view_parts']['coverages']:
        pay = g['coverage_payloads'][cid]
        by_rel['%s@%s' % (pay['key']['relation'], pay['key']['resolution'])] = {
            'coverageId': cid, 'coverage': pay['entry']['coverage'],
            'deficiency': pay['entry']['deficiency'],
            'nativeCause': pay['entry']['nativeCause'],
            'subjectCount': pay['entry']['examinedUniverse']['subjectCount'],
            'resolutionCompletenessState':
                pay['entry']['resolutionCompleteness']['state'],
            'examinedExhaustive':
                pay['entry']['resolutionCompleteness']['examinedExhaustive']}
    clone_pred = [pp for pp in out['proof']['predicateProofs']
                  if pp['ruleId'] == 'rule.a-no-duplicate-body']
    return {
        'R-RUN-SYNTAX-DATA': {
            'selectedGrammarSyntaxClasses': sorted({r['syntaxClass'] for r in g['gram_rows']}),
            'selectedGrammarLanguages': sorted(r['languageId'] for r in g['gram_rows']),
            'noCodeGrammarSelected': all(r['syntaxClass'] == 'data-document'
                                         for r in g['gram_rows']),
            'inventoryCapabilityPresent': by_rel['file@enumerated'],
            'firstPartyManifestInventoryIsLawfullyCompleteEmpty':
                by_rel['package@manifest-declared'],
            'unsupportedCapabilityDisclosures': {
                k: v for k, v in by_rel.items()
                if k not in ('file@enumerated', 'package@manifest-declared')},
            'completeEmptyDoesNotConcealUnsupportedAnalysis': {
                'clonesFactCount': 0,
                'clonesCoverage': by_rel['clones@normalized-body-hash']['coverage'],
                'gatingPredicateValues': sorted({pp['value'] for pp in clone_pred}),
                'gatingRuleOutcome': [rr['outcome'] for rr in out['proof']['ruleResults']
                                      if rr['ruleId'] == 'rule.a-no-duplicate-body'][0],
                'sealedVerdict': out['proof']['verdict'],
                'law': ('"A clone or code-construct request against it is explicitly '
                        'UNAVAILABLE (language-tier-unsupported for that capability), never '
                        'a complete empty clone result, which would read as a finding of no '
                        'clones." Measured: zero clones facts AND coverage unknown, so the '
                        'universal-negative predicate is INDETERMINATE, not true.')}},
        'R-RUN-UNAVAILABLE-SEMANTIC': {
            'pairing': {k: {'deficiency': v['deficiency'], 'nativeCause': v['nativeCause'],
                            'coverage': v['coverage']}
                        for k, v in by_rel.items() if v['deficiency']},
            'registrySelector': ('native/native-evidence.schemas.v2.json'
                                 '#/x-opensip-deficiency-cause-registry/deficiencies/'
                                 'language-tier-unsupported'),
            'carrier': 'entry.nativeCause',
            'nativeCauseMode': 'required',
            'allowedCauses': ['capability-missing'],
            'disclosureSelector': ('native/native-evidence.schemas.v2.json'
                                   '#/x-opensip-grammar-capability-registry/'
                                   'unavailableRequestDisclosure'),
            'resolvedRungUnderASyntaxUniverse': {
                'pair': 'imports@resolved-target',
                'resolutionCompletenessState':
                    by_rel['imports@resolved-target']['resolutionCompletenessState'],
                'law': ('RC-1: a resolved rung must never claim not-applicable. With '
                        'resolutionAttempted=false the honest state is not-attempted, '
                        'attempted=false, unresolvedEdgeCount 0.')}},
        'R-RUN-UNSUPPORTED-GRAMMAR': {
            'unbundledPath': 'tool/main.py',
            'inventoried': 'tool/main.py' in g['all_paths'],
            'fileFactMinted': True,
            'membership': 'unsupported-file',
            'reason': 'no-bundled-grammar',
            'noTypeScriptCompilerAssumed': {
                'nativeContextDomain': 'native.context.syntax.v2',
                'contextHasToolchain': False, 'contextHasStdlib': False,
                'contextHasLockfile': False, 'contextHasNodeModulesLayout': False,
                'contextHasConfigGraph': False,
                'law': ('native-evidence section 1.2: a syntax-only context "has no '
                        'toolchain, no stdlib, no lockfile, no node_modules layout and no '
                        'config graph ... A syntax-only context that named a compiler would '
                        'assert semantics the mode never computes."')},
            'inventoryIsNotGrammarGated': (
                'tool/main.py carries a file@enumerated fact and is a subject of the '
                'complete file@enumerated Coverage, because the three inventory '
                'capabilities are exempt from grammar ownership at BOTH registry '
                'enforcement boundaries.')},
    }


def main():
    g = complete(build())
    out = g['out']
    print('runId', out['runId'], 'verdict', out['proof']['verdict'])
    for rr in out['proof']['ruleResults']:
        print('  %-26s outcome=%-14s findings=%d defs=%s'
              % (rr['ruleId'], rr['outcome'], len(rr['findingIds']),
                 sorted({d['cause'] for d in rr['deficiencies']})))
    print(json.dumps(g['exhibits']['R-RUN-SYNTAX-DATA'][
        'completeEmptyDoesNotConcealUnsupportedAnalysis'], indent=1))
    c = CL.Closure(g['st'])
    rep = c.close_run(out['runId'], 'syntax-data')
    print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
          'n/a', rep['checksNotApplicable'], 'refused', rep['checksRefused'])
    for r in rep['refusals'][:20]:
        print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:240])


if __name__ == '__main__':
    main()
