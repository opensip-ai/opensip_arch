"""Completes the TypeScript Run: policy (with a boolean tree and an imported atom), the
ScopeDocumentV1 analysis-spec parameter, an actual import2 graph member, Plan, inventories,
view, execution plan, ExecutionInputsV1, composed outputs and export."""
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
import run_ts as RT

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'
BASE = 'run_ts'


def policy_document():
    rules = [
        {'ruleId': 'rule.a-no-clone-in-src',
         'ruleProgramRef': {'contributionId': 'contrib.ts-hygiene',
                            'ruleStableId': 'ts-hygiene.no-clone-in-src',
                            'semanticsMajor': 3,
                            'programDigest': K.raw_sha256(b'ts-hygiene.no-clone-in-src.v3')},
         'enabled': True, 'severity': 'error', 'gate': True,
         'subjectEnumeration': {'universe': 'typescript', 'subjectKind': 'file',
                                'include': ['src/**/*']},
         'emitWhen': {'op': 'none', 'relation': 'clones',
                      'minResolution': 'normalized-body-hash', 'filters': []},
         'evidenceUse': [], 'messageCode': 'clones.duplicate-body'},
        {'ruleId': 'rule.b-declares-without-import',
         'ruleProgramRef': {'contributionId': 'contrib.ts-hygiene',
                            'ruleStableId': 'ts-hygiene.declares-without-import',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(
                                b'ts-hygiene.declares-without-import.v1')},
         'enabled': True, 'severity': 'warning', 'gate': False,
         'subjectEnumeration': {'universe': 'typescript', 'subjectKind': 'symbol'},
         'emitWhen': {'op': 'and', 'operands': [
             {'op': 'exists', 'relation': 'declares', 'minResolution': 'syntactic',
              'filters': []},
             {'op': 'not', 'operand': {'op': 'exists', 'relation': 'imports',
                                       'minResolution': 'resolved-target',
                                       'filters': []}}]},
         'evidenceUse': [], 'messageCode': 'declares.without-import'},
        {'ruleId': 'rule.c-runtime-observed',
         'ruleProgramRef': {'contributionId': 'contrib.ts-hygiene',
                            'ruleStableId': 'ts-hygiene.runtime-observed',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'ts-hygiene.runtime-observed.v1')},
         'enabled': True, 'severity': 'note', 'gate': False,
         'subjectEnumeration': {'universe': 'typescript', 'subjectKind': 'file',
                                'include': ['src/**/*']},
         'emitWhen': {'op': 'exists', 'relation': 'runtime-observation',
                      'minResolution': 'observed', 'filters': [], 'evidence': 'runtime'},
         'evidenceUse': [{'kind': 'runtime', 'requirement': 'optional'}],
         'messageCode': 'runtime.observed'},
        {'ruleId': 'rule.d-disabled-probe',
         'ruleProgramRef': {'contributionId': 'contrib.ts-hygiene',
                            'ruleStableId': 'ts-hygiene.disabled-probe',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'ts-hygiene.disabled-probe.v1')},
         'enabled': False, 'severity': 'note', 'gate': True,
         'subjectEnumeration': {'universe': 'typescript', 'subjectKind': 'package'},
         'emitWhen': {'op': 'count-at-most', 'n': 0, 'relation': 'package',
                      'minResolution': 'manifest-declared', 'filters': []},
         'evidenceUse': [], 'messageCode': 'package.too-many'},
    ]
    rules.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2,
            'gateSeverityAtLeast': 'warning', 'rules': rules}


def complete(g):
    b, st, sh = g['b'], g['st'], g['sh']
    cl = g['closures']
    snapshot_id, uni_hex, ctx_hex = g['snapshot_id'], g['uni_hex'], g['ctx_hex']

    policy = policy_document()
    policy_dig = b.record(B.POLICY_V2_DOC, '#/$defs/PolicyDocumentV2', policy, 'policy')
    waivers = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1,
               'waivers': [{'waiverId': 'waiver.legacy-js-clone',
                            'target': {'ruleId': 'rule.b-declares-without-import',
                                       'subjectPath': 'src/legacy.js'},
                            'reason': 'legacy shim retained deliberately for this subject',
                            'expires': None}]}
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

    # ---------------------------------------------------------------- import2 graph member
    runtime_payload = {
        'payloadDomain': 'workflow.import-payload.runtime.v1', 'format': 'v8-json',
        'observationWindow': {'startUtc': '2026-09-01T00:00:00Z',
                              'endUtc': '2026-09-02T00:00:00Z'},
        'observedPopulation': 'test-suite',
        'subjects': [
            {'path': 'src/index.ts', 'observability': 'observed-hit', 'hits': 41},
            {'path': 'src/legacy.js', 'observability': 'unobservable',
             'mappingGap': 'no source map emitted for the legacy shim'},
            {'path': 'src/util.ts', 'observability': 'observable-unhit', 'hits': 0},
        ],
        'mappingGaps': ['src/legacy.js'],
    }
    ipay_dig = b.record(B.IMPORTED_DOC, '#/$defs/RuntimePayloadV1', runtime_payload,
                        'import-payload:runtime')
    corr = {'kind': 'exact-snapshot', 'snapshotId': snapshot_id}
    corr_dig = b.record(B.COMMON_DOC, '#/$defs/SourceCorrespondence', corr,
                        'import-source-correspondence')
    build_id = {'schemaVersion': 1, 'buildIdentity': None}
    build_dig = b.record(B.IMPORTED_DOC, '#/$defs/BuildIdentityV1', build_id,
                         'import-build-identity')
    obs = {'schemaVersion': 1, 'kind': 'runtime',
           'window': runtime_payload['observationWindow'],
           'population': runtime_payload['observedPopulation'],
           'selection': None, 'revisionRange': None}
    obs_dig = b.record(B.IMPORTED_DOC, '#/$defs/ImportObservationV1', obs,
                       'import-observation')
    import_scope = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': ['src'],
                    'excludedPathPrefixes': []}
    iscope_dig = b.record(B.IDENTITY_DOC, '#/$defs/scope-descriptor', import_scope,
                          'import-scope-descriptor')
    imp = {'schemaVersion': 2, 'kind': 'runtime',
           'payloadSchemaDigest': B.doc_sha(B.IMPORTED_DOC), 'payloadDigest': ipay_dig,
           'sourceCorrespondenceDigest': corr_dig, 'buildDigest': build_dig,
           'producerClosure': cl['importProducer'], 'adapterClosure': cl['adapter'],
           'blobs': [], 'scopeDigest': iscope_dig, 'observationDigest': obs_dig,
           'completeness': 'complete', 'omissions': []}
    import_id = b.framed('import', B.IDENTITY_DOC, '#/$defs/import', imp, 'import:runtime')

    # ---------------------------------------------------------------- ScopeDocumentV1
    scope_doc = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1,
                 'include': ['src/**/*'], 'exclude': ['src/**/*.test.ts']}
    scope_doc_dig = b.record(B.POLICY_V1_DOC, '#/$defs/ScopeDocumentV1', scope_doc,
                             'scope-document')

    # ---------------------------------------------------------------- enumeration plan
    membership = {
        'schemaVersion': 1,
        'units': [{'unitOrdinal': 0, 'rootPath': '', 'languageFamily': 'tsjs',
                   'languageMode': RT.LANGUAGE_MODE_OF_RECORD, 'unitKind': 'js-program',
                   'markerPath': 'tsconfig.json',
                   'markerSha256': K.raw_sha256(g['files']['tsconfig.json']),
                   'recognizerId': 'opensip-ts-recognizer', 'recognizerVersion': 2,
                   'provenance': 'DISCOVERED', 'memberPackageRoots': []}],
        # CORRECTED (V18-D4). native-evidence section 1.4 U-3: "A file's family is fixed by
        # EXTENSION (.rs -> rust; .ts/.tsx/.mts/.cts/.js/.mjs/.cjs/.jsx -> tsjs). It belongs to
        # the deepest unit of ITS OWN family. Units of another family never claim it." So
        # package.json, package-lock.json and both tsconfigs have NO family: they are
        # `syntax-only` / `grammar-only` rows with `unitOrdinal: null`, not members of the tsjs
        # unit. The earlier record gave every path family `tsjs` and unitOrdinal 0, which let
        # the unit claim files no clause assigns to it.
        'rows': [{'path': p,
                  'languageFamily': 'tsjs' if p.endswith(
                      ('.ts', '.tsx', '.mts', '.cts', '.js', '.mjs', '.cjs', '.jsx'))
                  else 'none',
                  'unitOrdinal': 0 if p.endswith(
                      ('.ts', '.tsx', '.mts', '.cts', '.js', '.mjs', '.cjs', '.jsx'))
                  else None,
                  'membership': ('program-member' if p in g['code'] else 'syntax-only'),
                  'reason': ('deepest-unit-in-language' if p in g['code']
                             else 'grammar-only')}
                 for p in sorted(g['files'], key=lambda s: s.encode())],
        'unsupportedFiles': [], 'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    all_paths = sorted(g['files'], key=lambda s: s.encode())

    def binding(extents):
        # CORRECTED (V18-D3). enumeration-plan.schema.v1.json
        # #/$defs/AvailableProgramBindingV1/properties/programEntry: "TS/JS extra program:
        # non-null LogicalPath of the selected inventoried config (snapshot member). **U-1
        # DEFAULT USES NULL**; admission derives the actual U-1 marker/synthesized entry and
        # compares it to retained TypeScriptConfigGraphV1.entryConfigPath (the graph entry need
        # not be null)." This binding's provenance is `default-unit`, so its programEntry is
        # null and the ENTRY is derived: the U-1 marker precedence picks tsconfig.json at the
        # unit root, which the retained config graph's entryConfigPath already names. Writing
        # the filename here asserted a Plan-selected extra program that was never selected.
        return {'ordinal': 0, 'provenance': 'default-unit',
                'enumerator': {'status': 'selected', 'closureId': cl['provider']},
                'nativeContextDigest': ctx_hex, 'universe': uni_hex,
                'programEntry': None,
                'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                   for k, v in extents.items()],
                                  key=lambda e: e['kind'].encode())}

    cells = [
        # CORRECTED (V17-D4): the FILE kind extent is first-party scoped SNAPSHOT MEMBERSHIP
        # -- "Every remaining inventoried first-party snapshot path in the cell
        # workspace/scope ... REGARDLESS of compiler-mode program-member. Inventory is not
        # grammar-gated." The earlier `g['code']` here was the compiler program-root set, so
        # the clones-fact file extent silently dropped package.json, the lockfile and both
        # tsconfigs. The capability does not narrow the kind's extent.
        {'capabilityId': 'clones-fact', 'languageMode': RT.LANGUAGE_MODE_OF_RECORD, 'workspaceRoot': '.',
         'required': True, 'kinds': ['file'], 'programBindings': [binding({'file': all_paths})]},
        {'capabilityId': 'imports', 'languageMode': RT.LANGUAGE_MODE_OF_RECORD, 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'],
         'programBindings': [binding({'symbol': g['code']})]},
        {'capabilityId': 'inventory', 'languageMode': RT.LANGUAGE_MODE_OF_RECORD, 'workspaceRoot': '.',
         'required': True, 'kinds': sorted(['file', 'package'], key=lambda s: K.C(s)),
         'programBindings': [binding({'file': all_paths, 'package': ['package.json']})]},
        {'capabilityId': 'syntax', 'languageMode': RT.LANGUAGE_MODE_OF_RECORD, 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'],
         'programBindings': [binding({'symbol': g['code']})]},
    ]
    cells.sort(key=lambda c: (c['capabilityId'].encode(), c['languageMode'].encode(),
                              c['workspaceRoot'].encode()))
    enum_plan = {'schemaVersion': 1, 'snapshotId': snapshot_id,
                 'scopeDigest': sh['scopeDigest'], 'membershipDigest': membership_dig,
                 'cells': cells}
    enum_plan_dig = b.record(B.ENUM_PLAN_DOC, '#', enum_plan, 'enumeration-plan')
    cell_ord = {c['capabilityId']: i for i, c in enumerate(cells)}

    # ---------------------------------------------------------------- analysis spec / plan
    reqcaps = sorted([{'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
                       'workspaceRoot': c['workspaceRoot'], 'required': c['required']}
                      for c in cells], key=lambda r: K.C(r))
    params = sorted([
        {'schemaDigest': B.doc_sha(B.ENUM_PLAN_DOC), 'payloadDigest': enum_plan_dig},
        {'schemaDigest': B.doc_sha(B.EMIT_PLAN_DOC), 'payloadDigest': emit_dig},
        {'schemaDigest': B.doc_sha(B.POLICY_V1_DOC), 'payloadDigest': scope_doc_dig},
    ], key=lambda r: K.C(r))
    spec = {'schemaVersion': 2, 'requestedCapabilities': reqcaps,
            'policyPackIds': ['pack.ts-hygiene'], 'parameters': params}
    spec_dig = b.record(B.IDENTITY_DOC, '#/$defs/analysis-spec', spec, 'analysis-spec')
    grant = {'schemaVersion': 2, 'projectId': g['snapshot']['projectId'],
             'principals': K.cset([{'kind': 'first-party', 'closureId': cl['provider'],
                                    'ownerSourceDigest': None},
                                   {'kind': 'first-party', 'closureId': cl['evaluator'],
                                    'ownerSourceDigest': None}]),
             'analysisOperations': sorted(['read-source', 'read-import', 'native-analysis'],
                                          key=lambda s: K.C(s)),
             'scopeDigest': sh['scopeDigest']}
    grant_dig = b.record(B.IDENTITY_DOC, '#/$defs/semantic-grant', grant, 'semantic-grant')
    plan = {'schemaVersion': 2, 'snapshotId': snapshot_id,
            'capabilityManifestId': g['capres']['capabilityManifestId'],
            'semanticClosures': K.cset_strings([cl['provider'], cl['evaluator'],
                                                cl['detector']]),
            'analysisSpecDigest': spec_dig, 'resolvedConfigDigest': sh['configDigest'],
            'nativeContextDigests': [ctx_hex], 'importIds': [import_id],
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDigest': sh['scopeDigest'],
            'budget': dict(g['config']['analysis']['budget']),
            'semanticGrantDigest': grant_dig,
            'capabilityManifestBytesDigest': g['capres']['committedBytesSha256']}
    plan_id = b.framed('plan', B.IDENTITY_DOC, '#/$defs/plan', plan, 'plan')

    # ---------------------------------------------------------------- inventories
    lang = {'.ts': 'typescript', '.js': 'javascript', '.json': 'json'}

    def subj_lang(p):
        for suf, l in sorted(lang.items(), key=lambda t: -len(t[0])):
            if p.endswith(suf):
                return l
        return 'unspecified'

    file_rows = sorted([{'nativeSubjectId': p, 'kind': 'file', 'path': p,
                         'qualifiedName': p, 'subjectLanguage': subj_lang(p),
                         'signatureTokens': [], 'projections': []} for p in all_paths],
                       key=lambda r: r['nativeSubjectId'].encode())
    code_rows = sorted([r for r in file_rows if r['path'] in g['code']],
                       key=lambda r: r['nativeSubjectId'].encode())
    pkg_rows = [{'nativeSubjectId': 'app', 'kind': 'package', 'path': 'package.json',
                 'qualifiedName': 'app', 'subjectLanguage': 'json',
                 'signatureTokens': [], 'projections': []}]
    sym_rows = sorted([
        {'nativeSubjectId': sid, 'kind': 'symbol', 'path': path, 'qualifiedName': qn,
         'subjectLanguage': subj_lang(path), 'exported': 'exported',
         'signatureTokens': [subj_lang(path), 'function', qn, '(', ')'],
         'projections': [{'closureId': cl['detector'],
                          'signatureTokens': [subj_lang(path), 'function', qn, '(', ')']}]}
        for sid, (path, qn) in g['syms'].items()],
        key=lambda r: r['nativeSubjectId'].encode())

    inventories = []
    for cap_id, kind, rows, examined in (('inventory', 'file', file_rows, all_paths),
                                         ('inventory', 'package', pkg_rows,
                                          ['package.json']),
                                         ('syntax', 'symbol', sym_rows, g['code']),
                                         ('imports', 'symbol', sym_rows, g['code']),
                                         # the clones-fact FILE inventory owes the whole file
                                         # extent (section 4 totality), not the code subset
                                         ('clones-fact', 'file', file_rows, all_paths)):
        inv = {'schemaVersion': 1, 'planId': plan_id, 'parameterDigest': enum_plan_dig,
               'cellOrdinal': cell_ord[cap_id], 'programOrdinal': 0, 'kind': kind,
               'state': 'complete', 'deficiency': None, 'nativeCause': None,
               'examinedPaths': sorted(examined, key=lambda s: K.C(s)), 'rows': rows}
        b.admit(B.SUBJ_INV_DOC, '#', inv, 'subject-inventory:%s:%s' % (cap_id, kind))
        d = st.put_record(inv, label='subject-inventory:%s:%s' % (cap_id, kind))
        inventories.append((d, inv))

    # ---------------------------------------------------------------- view / exec plan
    view_id = b.view(plan_id, g['view_parts']['scopes'], list(g['facts']),
                     g['view_parts']['coverages'], cl['provider'],
                     [B.doc_sha(B.RELATION_DOC), B.doc_sha(B.NATIVE_DOC)], 'typescript')
    stage_spec = {'schemaVersion': 2, 'planId': plan_id, 'producerClosure': cl['provider'],
                  'operation': 'typescript.analyze.v2',
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

    # ------------------------------------------------- target attribution sidecars
    # evaluator-projection-registry: `imports` declares endpointTarget `admitted-at-rung`
    # with targetKinds {file,symbol,package}, and the target's kind/occupancy is carried by a
    # TargetAttributionV2 sidecar -- NOT by parsing the opaque payload id. "Host MUST NOT
    # parse SubjectIdV1 namespace:opaque spelling to invent kind, occupancy, or
    # evaluationNativeId", so the attestation is retained here and the graph-query endpoint
    # projection reads it instead of guessing.
    #
    # STANDING: execution-inputs section 6 makes these PROVIDER returns -- host projections of
    # a worker OccupancyCompanionV1 on a negotiated FactBatchV3 -- and an ephemeral host
    # projection is licensed only on EXACT inventory native-id equality, which
    # `ts:src/util.ts` vs `src/util.ts` does not satisfy. These records are therefore part of
    # the same SYNTHETIC TRUSTED PROVIDER RETURN as every fact of this Run, and are labelled
    # so. Omitting them entirely would also have been lawful: "Missing token / empty
    # companions: lawful occupancy-unknown ... not required-output-pointer-omitted". They are
    # retained because the graph-query endpoint law is what this origin had to reconstruct.
    target_attrs = []
    for fid in g['facts']:
        f = st.objects[fid]
        if f['relation'] != 'imports' or f['resolution'] != 'resolved-target':
            continue
        pay = g['fact_payloads'][fid] if 'fact_payloads' in g else None
        tgt = pay['resolvedTarget'] if pay else None
        if tgt is None:
            continue
        first_party = tgt.startswith('ts:') and not tgt.startswith('ts:node_modules/')
        logical = tgt.split(':', 1)[1] if ':' in tgt else tgt
        rec = {'schemaVersion': 2, 'planId': plan_id, 'sourceFactId': fid,
               'producerClosure': f['producerClosure'],
               'targetUniverse': f['targetUniverse'],
               'targetNativeId': tgt, 'kind': 'file',
               'occupancy': 'first-party' if first_party else 'external',
               'exported': None,
               # the hint is permitted ONLY for external/unknown occupancy and is null for a
               # first-party subject, whose identity is evaluationNativeId instead
               'logicalPath': None if first_party else logical,
               'packageManifestPath': None,
               'evaluationNativeId': logical if first_party else None}
        b.admit('docs/coop/design-corrections/foundation/target-attribution.schema.v2.json',
                '#', rec, 'target-attribution:' + fid[:14])
        d = st.put_record(rec, label='target-attribution:' + fid[:14])
        target_attrs.append(d)

    host_derived = K.cset([{'domain': 'subject-inventory', 'digest': d}
                           for d, _ in inventories]
                          + [{'domain': 'target-attribution', 'digest': d}
                             for d in target_attrs])
    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(view_id)}]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])
    selected = K.cset(stage_out + host_derived
                      + [{'domain': 'import', 'digest': st.suffix(import_id)}])
    rel_for_cap = {'inventory': [('file', 'enumerated'), ('package', 'manifest-declared'),
                                 ('vcs-change', 'vcs-reported')],
                   'syntax': [('declares', 'syntactic'), ('literal', 'syntactic'),
                              ('control-flow', 'syntactic')],
                   'imports': [('imports', 'resolved-target')],
                   'clones-fact': [('clones', 'normalized-body-hash')]}
    cov_by_rel = {}
    for cid in g['view_parts']['coverages']:
        pay = g['coverage_payloads'][cid]
        cov_by_rel[(pay['key']['relation'], pay['key']['resolution'])] = st.suffix(cid)
    cell_outcomes, accounts = [], []
    for i, c in enumerate(cells):
        invs = sorted([d for d, inv in inventories if inv['cellOrdinal'] == i],
                      key=lambda s: K.C(s))
        cell_outcomes.append({
            'ordinal': i, 'cellOrdinal': i, 'programOrdinal': 0,
            'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
            'workspaceRoot': c['workspaceRoot'], 'required': c['required'],
            'kinds': c['kinds'], 'universe': uni_hex, 'enumeratorStatus': 'selected',
            'enumeratorClosure': cl['provider'], 'state': 'complete', 'deficiency': None,
            'nativeCause': None, 'stageOrdinal': 0, 'stageOrdinalNullReason': None,
            'inventoryDigests': invs, 'viewDigests': [st.suffix(view_id)],
            'candidateResultDigest': None})
        for rel, rung in rel_for_cap[c['capabilityId']]:
            if (rel, rung) in cov_by_rel:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': uni_hex,
                                 'targetUniverse': uni_hex,
                                 'applicability': 'supported-available',
                                 'coverageIds': [cov_by_rel[(rel, rung)]]})
            elif rel == 'vcs-change':
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'inapplicable-vcs', 'coverageIds': []})
            else:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unsupported-typed', 'coverageIds': []})
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
                   {uni_hex: ('native.semantic-universe.typescript.v2',
                              st.objects['native.semantic-universe.typescript.v2#' + uni_hex])},
                   {ctx_hex: ('native.context.typescript.v2',
                              st.objects['native.context.typescript.v2#' + ctx_hex])},
                   exec_inputs, imports={import_id: imp},
                   import_payloads={import_id: runtime_payload},
                   import_observations={import_id: obs},
                   import_flags={import_id: {'consumable': True, 'staleness': 'current'}},
                   import_scopes={import_id: import_scope}, snapshot=g['snapshot'])
    inp.analysis_spec = spec
    out = CO.compose(inp, st, emit, exec_in_dig, snapshot_id)
    retain_outputs(b, st, out)
    g.update(dict(policy=policy, waivers=waivers, plan=plan, plan_id=plan_id, spec=spec,
                  inventories=inventories, view_id=view_id, exec_inputs=exec_inputs,
                  exec_in_dig=exec_in_dig, out=out, inp=inp, import_id=import_id,
                  import_record=imp, runtime_payload=runtime_payload,
                  scope_doc=scope_doc, scope_doc_dig=scope_doc_dig,
                  enum_plan=enum_plan, enum_plan_dig=enum_plan_dig, emit=emit,
                  rule_program=rule_program))
    return g


def retain_outputs(b, st, out):
    for wd, w in out['witnesses'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/predicate-witness', w, 'witness:' + wd[:8])
        st.put_record(w, label='witness:' + wd[:8])
    for pp in out['proof']['predicateProofs']:
        node = node_at(out['ruleProgram'], pp['ruleId'], pp['predicateId'])
        rec = {'schemaVersion': 2, 'ruleProgramDigest': out['ruleProgramDigest'],
               'ruleId': pp['ruleId'], 'predicateId': pp['predicateId'],
               'operation': pp['operation'], 'nodeDigest': K.rec_digest(node)}
        b.admit(B.IDENTITY_DOC, '#/$defs/program-predicate', rec,
                'program-predicate:%s:%s' % (pp['ruleId'], pp['predicateId']))
        st.put_record(rec, label='program-predicate:%s:%s' % (pp['ruleId'],
                                                             pp['predicateId']))
    for fid, frec in out['findings'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/finding', frec, 'finding:' + fid[:18])
        st.put_framed('finding', frec, label='finding:' + fid[:18])
        aux = out['findingAux'][fid]
        b.admit(B.IDENTITY_DOC, '#/$defs/finding-parameters', aux['parameters'],
                'finding-parameters:' + fid[:18])
        st.put_record(aux['parameters'], label='finding-parameters:' + fid[:18])
        if aux['fingerprint']:
            b.admit(B.IDENTITY_DOC, '#/$defs/finding-fingerprint', aux['fingerprint'],
                    'finding-fingerprint:' + fid[:18])
            st.put_framed('finding-fingerprint', aux['fingerprint'],
                          label='finding-fingerprint:' + fid[:18])
    for sid, srec in out['subjects'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/evaluation-subject', srec,
                'evaluation-subject:' + sid[:18])
        st.put_framed('evaluation-subject', srec, label='evaluation-subject:' + sid[:18])
    for dom, sel, obj, lbl in (
            ('proof-bundle', '#/$defs/proof-bundle', out['proof'], 'proof-bundle'),
            ('semantic-evidence', '#/$defs/semantic-evidence', out['evidence'],
             'semantic-evidence'),
            ('evaluation-seal', '#/$defs/evaluation-seal', out['seal'], 'evaluation-seal'),
            ('run', '#/$defs/run', out['run'], 'run'),
            ('policy-derivation', '#/$defs/policy-derivation', out['policyDerivation'],
             'policy-derivation')):
        b.admit(B.IDENTITY_DOC, sel, obj, lbl)
        st.put_framed(dom, obj, label=lbl)


def node_at(rule_program, rule_id, addr):
    root = [r for r in rule_program['rules'] if r['ruleId'] == rule_id][0]['emitWhen']
    for a, n in E.address_nodes(root):
        if a == addr:
            return n
    raise KeyError(addr)


def main():
    g = complete(RT.build())
    out = g['out']
    print('planId ', g['plan_id'])
    print('runId  ', out['runId'], 'verdict', out['proof']['verdict'])
    print('findings', len(out['findings']), 'waived', out['proof']['waivedFindingIds'])
    print('predicateProofs', len(out['proof']['predicateProofs']))
    print('execDeficiencies', len(out['proof']['executionDeficiencies']))
    for rr in out['proof']['ruleResults']:
        print('  %-34s outcome=%-13s findings=%d defs=%s'
              % (rr['ruleId'], rr['outcome'], len(rr['findingIds']),
                 sorted({d['cause'] for d in rr['deficiencies']})))
    c = CL.Closure(g['st'])
    rep = c.close_run(out['runId'], 'typescript')
    print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
          'n/a', rep['checksNotApplicable'], 'refused', rep['checksRefused'])
    for r in rep['refusals'][:20]:
        print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:240])


if __name__ == '__main__':
    main()
