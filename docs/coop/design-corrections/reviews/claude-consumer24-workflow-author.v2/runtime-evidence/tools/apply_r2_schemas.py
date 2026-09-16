"""R2 + query-step mapping: closed public carriers for all nine query-class commands, closed query-step params,
command inventory dispatch/parity paths, and the REVIEW.CANDIDATE_UNKNOWN detail. Guarded JSON edits."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import edit_json  # noqa: E402

E3 = 'urn:opensip:product-v1:workflows:evaluator3:'
C3 = E3 + 'common:3#/$defs/'
GQ = E3 + 'graph-query:3'
INV = E3 + 'invocation:3'
WFD = 'docs/coop/design-corrections/workflows/'
SURFACES = ['graph-query-response', 'discovery-recommendation', 'baseline-inspection', 'effective-policy', 'policy-test-result',
            'candidate-list', 'candidate-inspection', 'review-brief', 'repair-preview']
RECORD_DEFS = {
    'discovery-recommendation': 'DiscoveryRecommendationRecordV1',
    'baseline-inspection': 'BaselineInspectionRecordV1',
    'effective-policy': 'EffectivePolicyRecordV1',
    'policy-test-result': 'PolicyTestResultRecordV1',
    'candidate-list': 'CandidateListRecordV1',
    'candidate-inspection': 'CandidateInspectionRecordV1',
    'review-brief': 'ReviewBriefRecordV1',
    'repair-preview': 'RepairPreviewRecordV1',
}
HOST_OPS = {
    'baseline.inspect': 'BaselineInspectRequestV1',
    'discovery.recommend': 'DiscoveryRecommendRequestV1',
    'policy.show': 'PolicyShowRequestV1',
    'policy.test': 'PolicyTestRequestV1',
    'review.produce-brief': 'ReviewBriefProduceRequestV1',
}
rows = []


def invocation(doc):
    d = doc['$defs']
    assert 'HostQueryOperation' not in d
    old = d['QueryParams']
    d['HostQueryOperation'] = {
        'type': 'string', 'enum': list(HOST_OPS),
        'description': ('Closed host-only query-step operations for query-class CLI commands whose request has no member of the public '
                        'graph-query:3 Operation/Params API. Never members of that public Operation enum and never public query operations.')}
    d['PublicQueryParams'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['kind', 'operation', 'completeness', 'page', 'request'],
        'properties': {'kind': {'const': 'query'}, 'operation': old['properties']['operation'], 'completeness': old['properties']['completeness'],
                       'page': old['properties']['page'], 'request': {'$ref': GQ + '#/$defs/GraphQueryRequestV1'}},
        'description': ('A query step over one of the twenty public graph-query:3 operations; request is the complete admitted '
                        'GraphQueryRequestV1 whose operation, completeness and page equal the step fields (cross-field join).')}
    d['HostQueryParams'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['kind', 'operation', 'request'],
        'properties': {'kind': {'const': 'query'}, 'operation': {'$ref': '#/$defs/HostQueryOperation'},
                       'request': {'oneOf': [{'$ref': '#/$defs/' + v} for v in HOST_OPS.values()]}},
        'allOf': [{'if': {'required': ['operation'], 'properties': {'operation': {'const': op}}},
                   'then': {'properties': {'request': {'$ref': '#/$defs/' + name}}}} for op, name in HOST_OPS.items()],
        'description': 'A query step over one closed host-only operation; request is the closed record of exactly that operation.'}
    d['BaselineInspectRequestV1'] = {'type': 'object', 'additionalProperties': False, 'required': ['operation', 'path'],
                                     'properties': {'operation': {'const': 'baseline.inspect'}, 'path': {'$ref': C3 + 'UserInputPath'}},
                                     'description': 'baseline show [PATH]: the tracked baseline artifact path (default opensip.baseline.json resolved by the host).'}
    d['DiscoveryRecommendRequestV1'] = {'type': 'object', 'additionalProperties': False, 'required': ['operation'],
                                        'properties': {'operation': {'const': 'discovery.recommend'}, 'emitConfigProposalPath': {'$ref': C3 + 'UserInputPath'}},
                                        'description': 'recommend [--emit-config-proposal PATH].'}
    d['PolicyShowRequestV1'] = {'type': 'object', 'additionalProperties': False, 'required': ['operation'],
                                'properties': {'operation': {'const': 'policy.show'}},
                                'description': 'policy show: tracked policy and waiver documents resolved at the admitted trust-clock date (host observation, not a request field).'}
    d['PolicyTestRequestV1'] = {'type': 'object', 'additionalProperties': False, 'required': ['operation', 'suitePath'],
                                'properties': {'operation': {'const': 'policy.test'}, 'suitePath': {'$ref': C3 + 'UserInputPath'}},
                                'description': 'policy test SUITE.'}
    d['ReviewBriefProduceRequestV1'] = {'type': 'object', 'additionalProperties': False, 'required': ['operation', 'view', 'producer'],
                                        'properties': {'operation': {'const': 'review.produce-brief'}, 'view': {'$ref': GQ + '#/$defs/View'},
                                                       'producer': {'$ref': E3 + 'review:2#/$defs/ReviewerPrincipal'}},
                                        'description': 'review brief [--producer model|heuristic]: model selects a ReviewerPrincipal of kind model with its admitted modelClosureId; heuristic selects kind policy-rule with id opensip.review.heuristic.'}
    d['QueryParams'] = {'oneOf': [{'$ref': '#/$defs/PublicQueryParams'}, {'$ref': '#/$defs/HostQueryParams'}],
                        'description': 'Closed query-step params: public graph-query:3 operations or the closed host-only extension. The command->operation mapping is command-inventory:3 queryDispatch.'}


def record(surface, required, props, description):
    return {'type': 'object', 'additionalProperties': False, 'required': ['surface'] + required,
            'properties': dict({'surface': {'const': surface}}, **props), 'description': description}


def envelope(doc):
    props = doc['properties']
    assert props['querySurface']['enum'] == ['graph-query-response', 'command-owned-summary'] and 'queryRecord' not in props
    props['querySurface'] = {'type': 'string', 'enum': SURFACES,
                             'description': ('Required exactly on kind=query and equal to the command inventory queryDispatch.surface. '
                                             'graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.')}
    new_props = {}
    for k, v in props.items():
        new_props[k] = v
        if k == 'queryResponse':
            new_props['queryRecord'] = {'oneOf': [{'$ref': '#/$defs/' + name} for name in RECORD_DEFS.values()],
                                        'description': 'Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.'}
    doc['properties'] = new_props
    doc['description'] = doc['description'].replace(
        'every other query-class command selects command-owned-summary and carries no queryResponse.',
        'every other query-class command selects its own surface and carries queryRecord of that closed record type.')
    br = doc['allOf']
    idx = next(i for i, b in enumerate(br) if b['if'].get('properties', {}).get('querySurface', {}).get('const') == 'command-owned-summary')
    del br[idx]
    idx = next(i for i, b in enumerate(br) if 'not' in b['if'] and b['if']['not'].get('properties', {}).get('kind', {}).get('const') == 'query')
    br[idx]['then'] = {'not': {'anyOf': [{'required': ['querySurface']}, {'required': ['queryResponse']}, {'required': ['queryRecord']}]}}
    br.append({'if': {'required': ['querySurface'], 'properties': {'querySurface': {'const': 'graph-query-response'}}},
               'then': {'not': {'required': ['queryRecord']}}})
    br.append({'if': {'required': ['querySurface'], 'properties': {'querySurface': {'not': {'const': 'graph-query-response'}}}},
               'then': {'required': ['queryRecord'], 'not': {'required': ['queryResponse']}}})
    for surface, name in RECORD_DEFS.items():
        br.append({'if': {'required': ['querySurface'], 'properties': {'querySurface': {'const': surface}}},
                   'then': {'properties': {'queryRecord': {'$ref': '#/$defs/' + name}}}})
    d = doc['$defs']
    d['Config2WorkspaceRootsProposalV1'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['key', 'workspaceRoots', 'unitOrdinals'],
        'properties': {'key': {'const': 'discovery.workspaceRoots'},
                       'workspaceRoots': {'type': 'array', 'minItems': 1, 'maxItems': 4096, 'uniqueItems': True,
                                          'items': {'type': 'string', 'minLength': 1, 'maxLength': 4096}, 'x-opensip-order': 'sequence'},
                       'unitOrdinals': {'type': 'array', 'minItems': 1, 'maxItems': 8192, 'uniqueItems': True,
                                        'items': {'type': 'integer', 'minimum': 0, 'maximum': 8191}, 'x-opensip-order': 'sequence'}},
        'description': ('The only config2 proposal this surface emits: explicit discovery.workspaceRoots (native explicit-root spelling) '
                        'pinning discovered units. Every root normalizes to a discovered unit rootPath and unitOrdinals are exactly those units. '
                        'Other config2 keys have no published config2 document schema and are not proposed.')}
    d['DiscoveryRecommendationRecordV1'] = record('discovery-recommendation', ['advisory', 'discovery', 'recommendations', 'config2Proposals'], {
        'advisory': {'const': True},
        'discovery': {'$ref': 'urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/UnitDiscoveryV2'},
        'recommendations': {'type': 'array', 'maxItems': 1024, 'items': {'$ref': C3 + 'DomainDetail'}, 'x-opensip-order': 'sequence'},
        'config2Proposals': {'type': 'array', 'maxItems': 1, 'items': {'$ref': '#/$defs/Config2WorkspaceRootsProposalV1'}, 'x-opensip-order': 'sequence'},
    }, 'recommend: native UnitDiscoveryV2 admitted under the security boundary inventory, registered advisory details, and config2 proposals. Advisory only.')
    d['PivotClosureAvailabilityV1'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['closureId', 'kind', 'state'],
        'properties': {'closureId': {'$ref': C3 + 'ClosureId'}, 'kind': {'$ref': E3 + 'baseline:2#/$defs/PivotClosureEntry/properties/kind'},
                       'state': {'type': 'string', 'enum': ['available', 'missing', 'revoked', 'incompatible']},
                       'trustOrigin': {'type': 'string', 'enum': ['retained-generation', 'installed-signed-release', 'signed-closure-bundle']}},
        'allOf': [{'if': {'properties': {'state': {'const': 'available'}}}, 'then': {'required': ['trustOrigin']}, 'else': {'not': {'required': ['trustOrigin']}}}],
        'description': ('Current-trust resolution of one pivot closure: missing (BASELINE.PIVOT_DETECTOR_UNAVAILABLE), revoked '
                        '(BASELINE.PIVOT_CLOSURE_REVOKED), incompatible protocol major or platform (BASELINE.PIVOT_CLOSURE_INCOMPATIBLE), or available with its trust origin.')}
    d['BaselineInspectionRecordV1'] = record('baseline-inspection', ['baseline', 'pivotClosureAvailability'], {
        'baseline': {'$ref': E3 + 'baseline:2'},
        'pivotClosureAvailability': {'type': 'array', 'maxItems': 256, 'items': {'$ref': '#/$defs/PivotClosureAvailabilityV1'}, 'x-opensip-order': 'sequence'},
    }, 'baseline show: the admitted baseline:2 artifact and one availability row per descriptor pivotClosure entry, in descriptor order.')
    d['EffectivePolicyRecordV1'] = record('effective-policy', ['policyDigest', 'policy', 'waiverSetDigest', 'effectiveWaivers', 'waiverResolution'], {
        'policyDigest': {'$ref': C3 + 'Sha256Hex'},
        'policy': {'$ref': 'urn:opensip:product-v1:policy-document:2#/$defs/PolicyDocumentV2'},
        'waiverSetDigest': {'$ref': C3 + 'Sha256Hex'},
        'effectiveWaivers': {'$ref': 'urn:opensip:product-v1:workflows:policy-document#/$defs/WaiverSetV1'},
        'waiverResolution': {'$ref': 'urn:opensip:product-v1:workflows:policy-document#/$defs/WaiverResolutionV1'},
    }, 'policy show: the admitted tracked policy, the resolved effective waiver set and its resolution disclosure, with their document digests.')
    d['PolicyTestResultRecordV1'] = record('policy-test-result', ['result'], {
        'result': {'$ref': 'urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1'},
    }, 'policy test: the complete PolicyTestResultV1.')
    d['EvidenceLevelCountsV1'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['proof-backed', 'partial-coverage', 'advisory-only'],
        'properties': {k: {'$ref': C3 + 'Uint53'} for k in ('proof-backed', 'partial-coverage', 'advisory-only')},
        'description': 'Count of listed candidates per review:2 EvidenceLevel.'}
    d['CandidateListRecordV1'] = record('candidate-list', ['context', 'includeSuppressed', 'candidates', 'evidenceLevels', 'suppressedCount'], {
        'context': {'$ref': GQ + '#/$defs/GraphQueryResponseContext'},
        'includeSuppressed': {'type': 'boolean'},
        'candidates': {'type': 'array', 'maxItems': 1000, 'items': {'$ref': E3 + 'review:2#/$defs/Candidate'}, 'x-opensip-order': {'by': ['candidateId']}},
        'evidenceLevels': {'$ref': '#/$defs/EvidenceLevelCountsV1'},
        'suppressedCount': {'$ref': C3 + 'Uint53'},
    }, 'candidates: review:2 Candidate records of one admitted Run with the owner non-graph context.')
    d['CandidateInspectionRecordV1'] = record('candidate-inspection', ['context', 'inspection'], {
        'context': {'$ref': GQ + '#/$defs/GraphQueryResponseContext'},
        'inspection': {'$ref': E3 + 'review:2#/$defs/InspectionBundle'},
    }, 'inspect: the review:2 InspectionBundle of one candidate of an admitted Run.')
    d['ReviewBriefRecordV1'] = record('review-brief', ['context', 'brief'], {
        'context': {'$ref': GQ + '#/$defs/GraphQueryResponseContext'},
        'brief': {'$ref': E3 + 'review:2#/$defs/ReviewBrief'},
    }, 'review brief: the review:2 ReviewBrief of one admitted Run.')
    d['RepairPreviewRecordV1'] = record('repair-preview', ['preview', 'plan'], {
        'preview': {'$ref': INV + '#/$defs/RepairPreviewResult'},
        'plan': {'$ref': E3 + 'repair:2#/$defs/RepairPlanV1'},
    }, 'repair preview: the invocation:3 RepairPreviewResult and the repair:2 RepairPlanV1 it names.')


def inventory_schema(doc):
    d = doc['$defs']
    assert 'QueryDispatch' not in d
    d['QueryDispatch'] = {
        'type': 'object', 'additionalProperties': False, 'required': ['surface', 'stepKind', 'operations', 'parityPaths'],
        'properties': {
            'surface': {'$ref': E3 + 'command-envelope:3#/properties/querySurface'},
            'stepKind': {'type': 'string', 'enum': ['query', 'repair-preview']},
            'operations': {'type': 'array', 'maxItems': 20, 'uniqueItems': True,
                           'items': {'oneOf': [{'$ref': GQ + '#/$defs/Operation'}, {'$ref': INV + '#/$defs/HostQueryOperation'}]}, 'x-opensip-order': 'sequence'},
            'parityPaths': {'type': 'object', 'minProperties': 1, 'maxProperties': 32, 'propertyNames': {'$ref': C3 + 'CanonicalIdentifier'},
                            'additionalProperties': {'type': 'string', 'pattern': '^(/[A-Za-z0-9-]+)+(?![\\s\\S])'}},
        },
        'allOf': [{'if': {'properties': {'stepKind': {'const': 'repair-preview'}}}, 'then': {'properties': {'operations': {'maxItems': 0}}}},
                  {'if': {'properties': {'stepKind': {'const': 'query'}}}, 'then': {'properties': {'operations': {'minItems': 1}}}}],
        'description': ('Closed dispatch of a query-class command: the envelope surface it selects, the step that produces it, the '
                        'query-step operations it may dispatch, and the exact JSON pointer into CommandEnvelope major 3 for every parity field.')}
    cmd = d['Command']
    assert 'queryDispatch' not in cmd['properties']
    cmd['properties']['queryDispatch'] = {'$ref': '#/$defs/QueryDispatch'}
    cmd.setdefault('allOf', []).append({'if': {'required': ['requestClass'], 'properties': {'requestClass': {'const': 'query'}}},
                                        'then': {'required': ['queryDispatch']}, 'else': {'not': {'required': ['queryDispatch']}}})


PUBLIC_OPS = None
DISPATCH = {
    'query': ('graph-query-response', 'query', 'ALL', {
        'resolved-view': '/queryResponse/context/resolvedView', 'availability': '/queryResponse/context/availability',
        'truncated': '/queryResponse/context/truncated', 'total-items': '/queryResponse/context/totalItems',
        'termination-class': '/termination/class', 'query-response': '/queryResponse'}),
    'recommend': ('discovery-recommendation', 'query', ['discovery.recommend'], {
        'recommendations': '/queryRecord/recommendations', 'discovery-units': '/queryRecord/discovery/units',
        'config2-proposals': '/queryRecord/config2Proposals', 'termination-class': '/termination/class'}),
    'baseline-show': ('baseline-inspection', 'query', ['baseline.inspect'], {
        'baseline-id': '/queryRecord/baseline/baselineId', 'pivot-closure-availability': '/queryRecord/pivotClosureAvailability',
        'termination-class': '/termination/class'}),
    'policy-show': ('effective-policy', 'query', ['policy.show'], {
        'policy-digest': '/queryRecord/policyDigest', 'waiver-resolution': '/queryRecord/waiverResolution', 'termination-class': '/termination/class'}),
    'policy-test': ('policy-test-result', 'query', ['policy.test'], {
        'policy-test-result-id': '/queryRecord/result/policyTestResultId', 'summary': '/queryRecord/result/summary',
        'resolver-accepted': '/queryRecord/result/resolverAccepted', 'overrides-applied': '/queryRecord/result/overridesApplied',
        'termination-class': '/termination/class'}),
    'candidates': ('candidate-list', 'query', ['candidate.list'], {
        'candidates': '/queryRecord/candidates', 'evidence-levels': '/queryRecord/evidenceLevels',
        'suppressed-count': '/queryRecord/suppressedCount', 'termination-class': '/termination/class'}),
    'inspect': ('candidate-inspection', 'query', ['inspection.show'], {
        'candidate-id': '/queryRecord/inspection/candidateId', 'facts': '/queryRecord/inspection/facts',
        'limitations': '/queryRecord/inspection/limitations', 'termination-class': '/termination/class'}),
    'review-brief': ('review-brief', 'query', ['review.produce-brief'], {
        'candidates': '/queryRecord/brief/candidates', 'producer': '/queryRecord/brief/producer',
        'truncated': '/queryRecord/brief/truncated', 'termination-class': '/termination/class'}),
    'repair-preview': ('repair-preview', 'repair-preview', [], {
        'repair-plan-id': '/queryRecord/preview/repairPlanId', 'snapshot-id': '/queryRecord/preview/snapshotId',
        'applicable': '/queryRecord/preview/applicable', 'unmet-preconditions': '/queryRecord/preview/unmetPreconditions',
        'termination-class': '/termination/class'}),
}


def inventory(doc):
    ops = json.loads((ROOT_GQ).read_text())['$defs']['Operation']['enum']
    for i, c in enumerate(doc['commands']):
        if c['requestClass'] != 'query':
            assert 'queryDispatch' not in c
            continue
        surface, step, operations, paths = DISPATCH[c['name']]
        assert set(paths) == set(c['parityFields']), c['name']
        nc = {}
        for k, v in c.items():
            nc[k] = v
            if k == 'parityFields':
                nc['queryDispatch'] = {'surface': surface, 'stepKind': step, 'operations': list(ops) if operations == 'ALL' else operations,
                                       'parityPaths': {f: paths[f] for f in c['parityFields']}}
        doc['commands'][i] = nc
    assert sorted(c['name'] for c in doc['commands'] if 'queryDispatch' in c) == sorted(DISPATCH)
    js = next(r for r in doc['renderers'] if r['format'] == 'json')
    js['parityRule'] = ('the CommandEnvelope major 3 is the parity reference for every other renderer; every query-class command carries '
                        'its complete typed result in the carrier its queryDispatch.surface selects (queryResponse for graph-query-response, '
                        'queryRecord otherwise) and every parity field is read at its queryDispatch.parityPaths pointer')


from textedit import ROOT  # noqa: E402
ROOT_GQ = ROOT / (WFD + 'schemas/evaluator3/graph-query.schema.json')
NEW_CODE = 'REVIEW.CANDIDATE_UNKNOWN'


def registry(doc):
    assert NEW_CODE not in {r['code'] for r in doc['records']}
    doc['records'].append({'code': NEW_CODE, 'owner': 'workflows', 'selector': 'workflows/schemas/common.schema.json#/$defs/DomainDetailCode'})
    doc['records'].sort(key=lambda r: r['code'])


def common(doc):
    enum = doc['$defs']['DomainDetailCode']['enum']
    assert enum == sorted(enum) and NEW_CODE not in enum
    doc['$defs']['DomainDetailCode']['enum'] = sorted(enum + [NEW_CODE])


rows.append(edit_json('R2 invocation query-step params', WFD + 'schemas/evaluator3/invocation-record.schema.json', invocation))
rows.append(edit_json('R2 envelope typed carriers', WFD + 'schemas/evaluator3/command-envelope.schema.json', envelope))
rows.append(edit_json('R2 inventory schema queryDispatch', WFD + 'schemas/evaluator3/command-inventory.schema.json', inventory_schema))
rows.append(edit_json('R2 inventory instance queryDispatch', WFD + 'command-inventory.v3.json', inventory))
rows.append(edit_json('R2 registry REVIEW.CANDIDATE_UNKNOWN', 'docs/coop/design-corrections/public-detail-registry.v1.json', registry))
rows.append(edit_json('R2 retained common detail', WFD + 'schemas/common.schema.json', common))
rows.append(edit_json('R2 evaluator3 common detail', WFD + 'schemas/evaluator3/common.schema.json', common))
print(json.dumps(rows, indent=1))
