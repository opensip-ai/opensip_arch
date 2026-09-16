"""Apply the JSON corrections to the work tree with a byte-exact round-trip guard.

usage: python -I -B apply_json_edits.py
For each file: the unmodified bytes must re-serialize identically under one of the recorded serializer settings, or the
edit refuses. Before/after SHA-256 and the settings used are written to receipts/edits/json-edits.json.
"""
import hashlib, json, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
DC = RT / 'work/source38-work/docs/coop/design-corrections'
E3 = 'urn:opensip:product-v1:workflows:evaluator3:'
RECEIPT = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def edit(rel, fn):
    p = DC / rel
    raw = p.read_bytes()
    doc = json.loads(raw)
    setting = None
    for ascii_ in (True, False):
        for nl in ('\n', ''):
            if (json.dumps(doc, indent=2, ensure_ascii=ascii_) + nl).encode() == raw:
                setting = (ascii_, nl)
                break
        if setting:
            break
    if setting is None:
        raise SystemExit('round-trip guard refused ' + rel)
    fn(doc)
    new = (json.dumps(doc, indent=2, ensure_ascii=setting[0]) + setting[1]).encode()
    if new == raw:
        raise SystemExit('edit produced no change ' + rel)
    p.write_bytes(new)
    RECEIPT.append({'path': rel, 'beforeSha256': sha(raw), 'afterSha256': sha(new), 'ensureAscii': setting[0], 'trailingNewline': setting[1] == '\n'})


NEW_CODES = ['DELIVERY.REQUIRED_PROJECTION_FAILED', 'DOCTOR.REPORT_NOT_PRODUCIBLE', 'OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED']


def registry(doc):
    have = {r['code'] for r in doc['records']}
    assert not (set(NEW_CODES) & have)
    for code in NEW_CODES:
        doc['records'].append({'code': code, 'owner': 'workflows', 'selector': 'workflows/schemas/common.schema.json#/$defs/DomainDetailCode'})
    doc['records'].sort(key=lambda r: r['code'])


def detail_branch(code, then):
    return {'if': {'required': ['domainDetail'], 'properties': {'domainDetail': {'required': ['code'], 'properties': {'code': {'const': code}}}}}, 'then': then}


def common(doc):
    enum = doc['$defs']['DomainDetailCode']['enum']
    assert enum == sorted(enum) and not (set(NEW_CODES) & set(enum))
    doc['$defs']['DomainDetailCode']['enum'] = sorted(enum + NEW_CODES)
    st = doc['$defs']['StepTermination']
    st['description'] += (' Required-delivery detail law: DELIVERY.RENDERER_FAILED_AFTER_COMMIT names a failure after this invocation committed a Run and'
                          ' requires that runId; DELIVERY.REQUIRED_PROJECTION_FAILED names a required projection or renderer failure when no Run was'
                          ' committed and forbids runId. Both are operational-failed / DELIVERY.REQUIRED_FAILED; every other operational-failed'
                          ' termination keeps its existing optional runId.')
    st['allOf'].append(detail_branch('DELIVERY.RENDERER_FAILED_AFTER_COMMIT', {
        'required': ['errorCode', 'runId'],
        'properties': {'class': {'const': 'operational-failed'}, 'errorCode': {'const': 'DELIVERY.REQUIRED_FAILED'}}}))
    st['allOf'].append(detail_branch('DELIVERY.REQUIRED_PROJECTION_FAILED', {
        'required': ['errorCode'], 'not': {'required': ['runId']},
        'properties': {'class': {'const': 'operational-failed'}, 'errorCode': {'const': 'DELIVERY.REQUIRED_FAILED'}}}))


def envelope(doc):
    props = doc['properties']
    assert 'queryResponse' not in props and 'querySurface' not in props
    doc['description'] += (' Query carrier: kind=query requires querySurface. The query command (the twenty graph-query:3 operations) selects'
                           ' graph-query-response and carries the complete owner-admitted GraphQueryResponseV1 in queryResponse, which is its'
                           ' query-response parity field; every other query-class command selects command-owned-summary and carries no'
                           ' queryResponse. Unsupported envelope majors terminate REQUEST.SCHEMA_MAJOR_UNSUPPORTED with detail'
                           ' OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED.')
    new_props = {}
    for k, v in props.items():
        new_props[k] = v
        if k == 'query':
            new_props['querySurface'] = {
                'type': 'string', 'enum': ['graph-query-response', 'command-owned-summary'],
                'description': ('Required exactly on kind=query. graph-query-response is selected by the command whose inventory parityFields include'
                                ' query-response (the query command); command-owned-summary is selected by every other query-class command'
                                ' (recommend, baseline show, policy show, policy test, candidates, inspect, review brief, repair preview), whose'
                                ' own parity fields keep their owners.')}
            new_props['queryResponse'] = {
                '$ref': E3 + 'graph-query:3#/$defs/GraphQueryResponseV1',
                'description': ('The complete owner-admitted query response, required exactly when querySurface=graph-query-response. Cross-record'
                                ' joins beyond JSON Schema: context.projectId equals projectId; a present response termination equals termination;'
                                ' for graph.* the query summary is the owner projection of this response.')}
    doc['properties'] = new_props
    branches = doc['allOf']
    qb = next(b for b in branches if b['if'].get('properties', {}).get('kind', {}).get('const') == 'query')
    qb['then']['required'] = qb['then']['required'] + ['querySurface']
    branches.append({'if': {'required': ['querySurface'], 'properties': {'querySurface': {'const': 'graph-query-response'}}}, 'then': {'required': ['queryResponse']}})
    branches.append({'if': {'required': ['querySurface'], 'properties': {'querySurface': {'const': 'command-owned-summary'}}}, 'then': {'not': {'required': ['queryResponse']}}})
    branches.append({'if': {'not': {'properties': {'kind': {'const': 'query'}}}}, 'then': {'not': {'anyOf': [{'required': ['querySurface']}, {'required': ['queryResponse']}]}}})


def inventory_schema(doc):
    g = doc['$defs']['Golden']
    assert 'detailSuppliedBy' not in g['properties'] and 'allOf' not in g
    g['description'] = ('A failure golden (request-rejected or operational-failed) carries its actual domainDetail, unless detailSuppliedBy names the'
                        ' composition that supplies the failure envelope errors.')
    g['properties']['detailSuppliedBy'] = {'type': 'string', 'enum': ['native-route-composition'],
                                           'description': 'workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.'}
    g['allOf'] = [
        {'if': {'required': ['class'], 'properties': {'class': {'enum': ['request-rejected', 'operational-failed']}}},
         'then': {'anyOf': [{'required': ['domainDetail']}, {'required': ['detailSuppliedBy']}]}},
        {'if': {'required': ['detailSuppliedBy']}, 'then': {'not': {'required': ['domainDetail']}}}]


def comparison(doc):
    d = doc['$defs']
    pp = d['PivotPresence']
    pp['description'] = ('Presence knowledge of the fingerprint at each pivot. true = a known matched occurrence (waived included). false = absence'
                         " proved by that side's rule under the complete-hit-set law (enabled rule, evaluated, complete enumeration, every selected"
                         ' emitWhen root determinate, fingerprint absent from the emitted matched set, path inside the attested extent). null ='
                         ' not known. B is false only when the baseline RuleCoverage absenceKnowledge is complete-hit-set. waivedB/waivedC record'
                         ' waiver status on the two real sides.')
    for k in ('B', 'E4'):
        assert pp['properties'][k] == {'type': 'boolean'}
        pp['properties'][k] = {'oneOf': [{'type': 'boolean'}, {'type': 'null'}]}
    ir = d['IndeterminateReason']['enum']
    assert 'current-absence-unknown' not in ir
    ir.extend(['baseline-absence-unknown', 'current-absence-unknown'])
    rc = d['RuleCoverage']
    rc['required'].append('absenceKnowledge')
    rc['properties']['absenceKnowledge'] = {'type': 'string', 'enum': ['complete-hit-set', 'unknown'],
                                            'description': ('complete-hit-set when this side can prove absence of a non-emitted fingerprint of the rule:'
                                                            ' enabled, not budget-exhausted, outcome not indeterminate, complete enumeration and every'
                                                            ' selected emitWhen root determinate. Otherwise unknown (including disabled rules).'
                                                            ' Independent of requiredCoverage.')}
    ent = d['Entry']['properties']
    ent['gateReason']['description'] = ('code-net-new-policy-hidden: a gating CODE-NET-NEW entry that is not live in current because a later axis hid'
                                        ' it (a detector, policy or scope change, or a waiver added in the same change); subsequentDeltas names'
                                        ' the later axes.')
    ent['liveInCurrent']['description'] = 'true only when E4 is a known hit and the current occurrence is not waived'


def baseline(doc):
    d = doc['$defs']
    dce = d['DetectorClosureEntry']
    dce['description'] = ('Exactly one row per distinct contributionId of the origin EvaluatorEmissionPlanV1 rule rows (disabled rules included):'
                          ' detectorId equals contributionId; closureId and semanticsMajor are that contribution row detectorClosure and'
                          ' semanticsMajor. Rows sharing a contributionId with a different closure or major refuse'
                          ' (CONFIG.INVALID / EVALUATION.FINDING_JOIN_REFUSED).')
    dce['properties']['detectorId'] = dict(dce['properties']['detectorId'], description='equals contributionId')
    be = d['BaselineEntry']
    be['properties']['detectorId'] = dict(be['properties']['detectorId'], description="the entry rule's emission-binding contributionId; a member of detectorClosure detectorId")


def test_execution(doc):
    ev = doc['$defs']['EnforcementValue']
    assert ev['enum'] == ['DISCLOSURE-ONLY', 'ENFORCED-BY-CONSTRUCTION', 'ENFORCED-AT-HOST-BROKER']
    ev['description'] = ('Closed current test-execution vocabulary. Membership is necessary, not sufficient: each effect value must equal the'
                         ' selected security permission truth-table profile row for the platform (permission-truth-tables.v9 through'
                         ' security-and-lifecycle S10, child-process execution mode), otherwise TEST.CONFINEMENT_CLAIM_REFUSED. That profile'
                         ' has no measured platform-primitive row, so ENFORCED-PLATFORM:<primitiveId> cannot be claimed and is not a member.'
                         ' Security EnforcementV1 retains that future vocabulary; admitting it here requires a successor truth-table profile'
                         ' with a measured primitive and a successor of this schema.')


def inventory(doc):
    add = {'doctor-report-not-producible': 'DOCTOR.REPORT_NOT_PRODUCIBLE', 'query-latest-empty': 'QUERY.VIEW_UNKNOWN', 'envelope-major-unsupported': 'OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED'}
    for i, g in enumerate(doc['goldens']):
        if g['id'] in add:
            assert 'domainDetail' not in g
            ng = {}
            for k, v in g.items():
                if k == 'remedy':
                    ng['domainDetail'] = add[g['id']]
                ng[k] = v
            doc['goldens'][i] = ng
    js = next(r for r in doc['renderers'] if r['format'] == 'json')
    js['parityRule'] = ('the CommandEnvelope major 3 is the parity reference for every other renderer; the query command carries its complete'
                        ' query-response in queryResponse (querySurface=graph-query-response) and every other query-class command selects'
                        ' querySurface=command-owned-summary')


edit('public-detail-registry.v1.json', registry)
edit('workflows/schemas/common.schema.json', common)
edit('workflows/schemas/evaluator3/common.schema.json', common)
edit('workflows/schemas/evaluator3/command-envelope.schema.json', envelope)
edit('workflows/schemas/evaluator3/command-inventory.schema.json', inventory_schema)
edit('workflows/schemas/evaluator3/comparison-result.schema.json', comparison)
edit('workflows/schemas/evaluator3/baseline-artifact.schema.json', baseline)
edit('workflows/schemas/test-execution.schema.json', test_execution)
edit('workflows/command-inventory.v3.json', inventory)
out = RT / 'receipts/edits'
out.mkdir(parents=True, exist_ok=True)
(out / 'json-edits.json').write_text(json.dumps(RECEIPT, indent=1) + '\n')
print(json.dumps(RECEIPT, indent=1))
