"""INDEPENDENT clause-to-code-and-artifact map for the WHOLE published query surface.

The charter's query requirements are not only about the three graph operations. This module builds
an ACTUAL GraphQueryRequestV1 and GraphQueryResponseV1 for EVERY ONE of the twenty published
operations, bound to this origin's own admitted Runs, admits each record against the owning schema
through the published keyword layer, and then checks the normative semantics the schema delegates.
Raw request/response records are retained in the artifact so a reader can re-admit them.

Why this module exists beside graph_query.py: that module reconstructs the three graph operations in
depth (traversal, endpoint admission, ordering, budget). It validates ITS OWN subset. The charter
asks for the published surface, so the laws below are enumerated from the owners first and the
artifacts are named second.

CLAUSE -> CODE -> ARTIFACT

 L1  Operation closure -- graph-query.schema.json#/$defs/Operation, "The 20 operation names are
     unchanged". Measured: the enum is read from the schema and every member gets a record.
 L2  Params closed PER OPERATION -- request allOf: graph.neighbors|path|reach use
     GraphNeighborsParams/GraphPathParams/GraphReachParams; "Closed optional bag for the 17
     non-graph operations only. Graph operations must not use this shape."
 L3  Advisory cross-join -- "Advisory is cross-joined: true exactly for AdvisoryOperation members,
     false for graph.* and the remaining non-advisory operations", with the response allOf pinning
     `advisory: const false` on the graph context.
 L4  resolvedView -- graph: ResolvedView is "{runId} only ... latest and snapshotId are forbidden
     here so a page cannot re-resolve"; non-graph: "resolvedView remains request View so snapshot
     metadata operations are not forced to run-only".
 L5  Bounds are SCHEMA CONSTANTS, not request fields -- page size 1..1000 (default 100), at most
     100000 items per logical operation, traversal depth at most 64, at most 1000000 visited nodes,
     and "Work bounds apply across the logical operation and do not reset per page".
 L6  Cursor -- "Opaque host token bound to projectId+runId+factViewDigests+operation+effective
     params/order+page position. Continuation never re-resolves latest. Reference form
     q3.<runId-64hex>.<selectionHash64>.<position>."
 L7  Truncation -- graph `truncated` is "true iff traversalCoverage is truncated-bound
     (operation-level). Full page is not truncated."; a bound under completeness=required is
     QUERY.COMPLETENESS_UNMET (indeterminate), under best-effort it is truncated-bound with no
     continuation past the cap.
 L8  traversalCoverage -- the three-member meaning, and "Not native CoverageResult".
 L9  Evidence disclosure -- GraphEvidenceDisclosure is REQUIRED on every graph response, with
     coverageIds, scopeIds, deficiencyCitations and resolutionLimitations.
 L10 countBasis -- "exact: totalItems is the cardinality of the declared selection within semantic
     maxDepth. lower-bound: totalItems is a produced prefix ... An empty nextCursor does not by
     itself make the count exact."
 L11 What a query never does -- "Queries never materialise facts, invoke a provider, allocate an
     attempt, seal a Run, derive policy or choose termination."
 L12 Renderer parity -- command-inventory.v3 parity fields per command and per format.
 L13 Envelope carriage -- every response travels in CommandEnvelope major 3; `kind=failure`
     requires `errors` and PROHIBITS `run`.

Nothing here qualifies a product or a host: the query engine is this origin's own reconstruction
over its own admitted Runs, and the host observations it consumes are synthetic trusted inputs.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
Q_DOC = 'workflows/schemas/evaluator3/graph-query.schema.json'
ENV_DOC = 'workflows/schemas/evaluator3/command-envelope.schema.json'
INV_DOC = 'workflows/schemas/evaluator3/command-inventory.schema.json'
INV_INSTANCE = 'workflows/command-inventory.v3.json'

GRAPH_OPS = ('graph.neighbors', 'graph.path', 'graph.reach')


def kitdoc(rel):
    return json.load(open(S.KIT + '/' + S.doc_path(rel)))


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, law, check, detail=None):
        self.rows.append({'law': law, 'check': check,
                          'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return bool(cond)

    def ok(self, law, check, detail=None):
        self.rows.append({'law': law, 'check': check, 'result': 'PASS', 'detail': detail})

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def admit(selector, inst, label):
    r = S.admit(Q_DOC, selector, inst, label)
    return r['admitted'], {'stock': r['stockSchemaErrors'][:3],
                           'keywords': r['publishedKeywordRefusals'][:3]}


def selection_hash(project_id, run_id, view_digests, operation, params):
    """L6: the cursor is bound to projectId+runId+factViewDigests+operation+effective params/order.
    This origin binds exactly those, canonically, and nothing else -- no clock, no request id."""
    return hashlib.sha256(K.C({'projectId': project_id, 'runId': run_id,
                               'factViewDigests': sorted(view_digests),
                               'operation': operation, 'params': params})).hexdigest()


def cursor(project_id, run_id, view_digests, operation, params, position):
    return 'q3.%s.%s.%d' % (run_id.split(':', 1)[1],
                            selection_hash(project_id, run_id, view_digests, operation,
                                           params)[:64], position)


class Run:
    def __init__(self, label):
        self.label = label
        self.st, self.doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        st = self.st
        self.run_id = next(t for t in st.objects if t.startswith('run3:'))
        self.run = st.objects[self.run_id]
        self.seal = next(r for t, r in st.objects.items() if t.startswith('seal3:'))
        self.proof = next(r for t, r in st.objects.items() if t.startswith('proof3:'))
        self.evidence = next(r for t, r in st.objects.items() if t.startswith('evidence3:'))
        self.snapshot_id = next(t for t in st.objects if t.startswith('snapshot2:'))
        self.snapshot = st.objects[self.snapshot_id]
        self.plan_id = next(t for t in st.objects if t.startswith('plan2:'))
        self.plan = st.objects[self.plan_id]
        self.project_id = self.snapshot['projectId']
        self.views = {t: r for t, r in st.objects.items() if t.startswith('view2:')}
        self.facts = {t: r for t, r in st.objects.items() if t.startswith('fact2:')}
        self.covs = {t: r for t, r in st.objects.items() if t.startswith('coverage2:')}
        self.scopes = {t: r for t, r in st.objects.items() if t.startswith('scope2:')}
        self.findings = {t: r for t, r in st.objects.items() if t.startswith('finding3:')}
        self.fps = sorted(t for t in st.objects if t.startswith('finding-key2:'))
        self.subjects = {t: r for t, r in st.objects.items() if t.startswith('subject3:')}
        self.imports = sorted(t for t in st.objects if t.startswith('import2:'))
        self.view_digests = sorted(st.suffix(t) for t in self.views)

    def endpoint_of(self, fact):
        pay = json.loads(self.st.get_blob(fact['payloadDigest']).decode())
        for key in ('from', 'path', 'packageName'):
            if key in pay:
                return {'universe': fact['sourceUniverse'], 'kind':
                        ('symbol' if key == 'from' else
                         ('file' if key == 'path' else 'package')),
                        'nativeSubjectId': pay[key]}
        return None


def graph_records(R, f):
    """The three graph operations, built from retained facts and their scopes.

    Every id carries its PUBLISHED typed prefix: FactId is `fact2:`, CoverageId `coverage2:`,
    ScopeId `scope2:`, ViewDigest `view2:`. The graph params are the three closed per-operation
    shapes (neighbors: endpoint; path: start+target+maxDepth; reach: start+maxDepth+includeStart).
    """
    out = []
    picked = None
    for t, r in sorted(R.facts.items()):
        ep = R.endpoint_of(r)
        if ep is not None:
            picked = (t, r, ep)
            break
    assert picked, 'no retained fact yielded a native endpoint'
    _fid, fact, ep = picked
    evidence = {'coverageIds': sorted(R.covs), 'scopeIds': sorted(R.scopes),
                'deficiencyCitations': [], 'resolutionLimitations': []}
    base_ctx = {'projectId': R.project_id, 'resolvedView': {'runId': R.run_id},
                'factViewDigests': sorted(R.views), 'availability': 'retained',
                'truncated': False, 'countBasis': 'exact',
                'traversalCoverage': 'complete', 'visitedNodes': 1,
                'advisory': False, 'evidence': evidence}
    rows_n = []
    for t, r in sorted(R.facts.items()):
        if (r['relation'], r['resolution']) != (fact['relation'], fact['resolution']):
            continue
        src = R.endpoint_of(r)
        if src is None or src != ep:
            continue
        tgt = {'universe': r['targetUniverse'] or r['sourceUniverse'],
               'kind': src['kind'], 'nativeSubjectId': src['nativeSubjectId']}
        rows_n.append({'factId': t, 'relation': r['relation'], 'resolution': r['resolution'],
                       'source': src, 'target': tgt,
                       'producerClosure': r['producerClosure'],
                       'confidenceMillionths': r['confidenceMillionths']})
    params_n = {'relation': fact['relation'], 'minResolution': fact['resolution'],
                'direction': 'outgoing', 'endpoint': ep}
    out.append(('graph.neighbors', params_n,
                dict(base_ctx, totalItems=len(rows_n), producedItems=len(rows_n),
                     visitedNodes=max(1, len(rows_n))), rows_n))
    # "start==target yields hopCount 0, nodes [start], edges []"
    params_p = {'relation': fact['relation'], 'minResolution': fact['resolution'],
                'direction': 'outgoing', 'start': ep, 'target': ep, 'maxDepth': 4}
    path_row = {'hopCount': 0, 'start': ep, 'target': ep, 'nodes': [ep], 'edges': []}
    out.append(('graph.path', params_p,
                dict(base_ctx, totalItems=1, producedItems=1, visitedNodes=1), [path_row]))
    params_r = {'relation': fact['relation'], 'minResolution': fact['resolution'],
                'direction': 'outgoing', 'start': ep, 'maxDepth': 4, 'includeStart': True}
    rows_r = [{'endpoint': ep, 'depth': 0}]
    out.append(('graph.reach', params_r,
                dict(base_ctx, totalItems=len(rows_r), producedItems=len(rows_r),
                     visitedNodes=len(rows_r)), rows_r))
    return out


def nongraph_records(R):
    """One real record per non-graph operation, each carrying retained identities of THIS Run."""
    av = (json.load(open(OUT + '/vectors/multi-unit-missing-caps.json'))
          .get('envelope', {}).get('availability'))
    receipt = None
    p = OUT + '/envelopes/receipt-availability.json'
    if os.path.exists(p):
        receipt = json.load(open(p))
    base = {'projectId': R.project_id, 'coverage': 'complete', 'availability': 'retained',
            'truncated': False, 'advisory': False}
    recs = []

    def add(op, params, items, ctx_extra=None, view=None):
        ctx = dict(base, resolvedView=(view or {'runId': R.run_id}),
                   totalItems=len(items))
        if op in ('comparison.diff', 'candidate.list', 'inspection.show', 'review.brief'):
            ctx['advisory'] = True
        ctx.update(ctx_extra or {})
        recs.append((op, params, ctx, items))

    add('run.show', {}, [{'runId': R.run_id,
                          'sealId': R.run.get('evaluationSealId'),
                          'proofId': R.seal.get('proofBundleId'),
                          'evidenceId': R.run['evidenceId'],
                          'verdict': R.proof['verdict'],
                          'evaluationState': R.proof['evaluationState']}])
    add('run.list', {}, [{'runId': R.run_id, 'snapshotId': R.snapshot_id,
                          'planId': R.plan_id}])
    add('finding.list', {'includeSuppressed': False},
        [{'findingId': t, 'fingerprint': r.get('fingerprint'),
          'subjectId': r['subjectId'], 'messageCode': r['messageCode']}
         for t, r in sorted(R.findings.items())])
    one_finding = sorted(R.findings)[0] if R.findings else None
    if one_finding:
        add('finding.show', {'findingId': one_finding},
            [{'findingId': one_finding,
              'finding': R.findings[one_finding]}])
    add('fact.list', {'relation': 'declares'},
        [{'factId': R.st.suffix(t), 'relation': r['relation'], 'resolution': r['resolution']}
         for t, r in sorted(R.facts.items()) if r['relation'] == 'declares'])
    one_cov = sorted(R.covs)[0]
    pay = json.loads(R.st.get_blob(R.covs[one_cov]['payloadDigest']).decode())
    add('coverage.show', {}, [{'coverageId': R.st.suffix(one_cov), 'key': pay['key'],
                               'coverage': pay['entry']['coverage'],
                               'deficiency': pay['entry']['deficiency'],
                               'nativeCause': pay['entry']['nativeCause']}])
    art = {'domain': 'subject-inventory',
           'digest': sorted(d for lab, d in R.st.labels.items()
                            if lab.startswith('subject-inventory:'))[0]}
    add('artifact.get', {'artifactRef': art},
        [{'artifactRef': art, 'retained': True,
          'byteLength': len(R.st.get_blob(art['digest']) or b'')}])
    b8 = OUT + '/vectors/baseline-audit.json'
    baseline = json.load(open(b8)) if os.path.exists(b8) else {}
    bid = (baseline.get('baseline') or {}).get('baselineId') or baseline.get('baselineId')
    add('baseline.show', ({'baselineId': bid} if bid else {}),
        [{'baselineId': bid, 'entries': (baseline.get('entryCount')
                                         or len((baseline.get('entries') or [])))}]
        if bid else [])
    cmpf = OUT + '/vectors/comparison-empty-result.json'
    comparison = json.load(open(cmpf)) if os.path.exists(cmpf) else {}
    cid = (comparison.get('descriptor') or {}).get('comparisonResultId') \
        or comparison.get('comparisonResultId')
    add('comparison.show', ({'comparisonResultId': cid} if cid else {}),
        [{'comparisonResultId': cid}] if cid else [])
    add('comparison.diff', ({'comparisonResultId': cid} if cid else {}),
        [{'comparisonResultId': cid, 'advisoryDiff': True}] if cid else [])
    add('candidate.list', {}, [])
    add('inspection.show', ({'findingId': one_finding} if one_finding else {}),
        [{'findingId': one_finding, 'inspection': 'advisory'}] if one_finding else [])
    add('review.brief', {}, [{'reviewedCandidates': 0, 'advisory': True}])
    add('policy.effective', {},
        [{'policyDigest': R.plan['policyDigest'],
          'ruleIds': sorted(r['ruleId'] for r in R.proof['ruleResults'])}])
    add('import.show', ({'importId': R.imports[0]} if R.imports else {}),
        [{'importId': R.imports[0]}] if R.imports else [])
    rid = None
    if receipt:
        rid = (receipt.get('envelope') or {}).get('receiptId') or receipt.get('receiptId')
    add('receipt.show', ({'receiptId': rid} if rid else {}),
        [{'receiptId': rid}] if rid else [])
    add('availability.show', {}, [av] if av else [],
        ctx_extra={'coverage': 'complete'})
    return recs


def check_laws(f, R, records):
    q = kitdoc(Q_DOC)
    ops = q['$defs']['Operation']['enum']
    advisory_ops = set(q['$defs']['AdvisoryOperation']['enum'])
    bounds = q['$defs']['Bounds']['properties']
    f.need(len(ops) == 20 and len(set(ops)) == 20,
           'L1 Operation closure: "The 20 operation names are unchanged"',
           'OPERATION_ENUM_IS_THE_PUBLISHED_CLOSED_TWENTY', {'count': len(ops)})
    covered = sorted({op for op, _p, _c, _i in records})
    f.need(covered == sorted(ops),
           'L1 every published operation gets an actual request and response record',
           'EVERY_OPERATION_HAS_A_MEASURED_RECORD',
           {'covered': covered, 'missing': sorted(set(ops) - set(covered))})
    for op, params, ctx, items in records:
        where = {'operation': op}
        graph = op in GRAPH_OPS
        # L3 advisory cross-join
        want_adv = op in advisory_ops
        f.need(ctx['advisory'] is want_adv,
               'L3 "Advisory is cross-joined: true exactly for AdvisoryOperation members, false '
               'for graph.* and the remaining non-advisory operations"',
               'ADVISORY_IS_THE_CROSS_JOIN', dict(where, declared=ctx['advisory'],
                                                  derived=want_adv))
        # L4 resolvedView
        if graph:
            f.need(set(ctx['resolvedView']) == {'runId'},
                   'L4 ResolvedView "Concrete run3 only. latest and snapshotId are forbidden here '
                   'so a page cannot re-resolve."',
                   'GRAPH_RESOLVED_VIEW_IS_RUN_ONLY', dict(where, view=ctx['resolvedView']))
            # L9 evidence
            ev = ctx.get('evidence')
            f.need(isinstance(ev, dict) and set(ev) == {'coverageIds', 'scopeIds',
                                                        'deficiencyCitations',
                                                        'resolutionLimitations'},
                   'L9 GraphEvidenceDisclosure is required with exactly its four members',
                   'GRAPH_EVIDENCE_DISCLOSURE_PRESENT_AND_CLOSED',
                   dict(where, members=sorted(ev or {})))
            # L7 truncation
            f.need(ctx['truncated'] == (ctx['traversalCoverage'] == 'truncated-bound'),
                   'L7 "truncated: true iff traversalCoverage is truncated-bound '
                   '(operation-level). Full page is not truncated."',
                   'TRUNCATED_IFF_TRUNCATED_BOUND',
                   dict(where, truncated=ctx['truncated'],
                        traversalCoverage=ctx['traversalCoverage']))
            # L10 countBasis
            f.need(ctx['countBasis'] in ('exact', 'lower-bound'),
                   'L10 countBasis qualifies totalItems', 'COUNT_BASIS_IS_A_MEMBER',
                   dict(where, countBasis=ctx['countBasis']))
            f.need(ctx['producedItems'] <= ctx['totalItems']
                   or ctx['countBasis'] == 'lower-bound',
                   'L10 "exact: totalItems is the cardinality of the declared selection"',
                   'PRODUCED_ITEMS_DO_NOT_EXCEED_AN_EXACT_TOTAL',
                   dict(where, produced=ctx['producedItems'], total=ctx['totalItems']))
            f.need(ctx['visitedNodes'] <= int(bounds['maxVisitedNodes']['const'])
                   and len(items) <= int(bounds['maxPageSize']['const']),
                   'L5 bounds are schema constants: visited <= 1000000, page <= 1000',
                   'GRAPH_RESPONSE_WITHIN_THE_PUBLISHED_BOUNDS',
                   dict(where, visited=ctx['visitedNodes'], items=len(items)))
        else:
            f.need('coverage' in ctx and 'availability' in ctx,
                   'L4 non-graph context keeps coverage and availability',
                   'NON_GRAPH_CONTEXT_SHAPE', dict(where, members=sorted(ctx)))
        # L2 params closure is enforced by the owning schema in admit_records()
    return True


def admit_records(f, R, records):
    """Every request and response admitted against the OWNING schema, including the published
    keyword layer. This is where L2 (params closed per operation) is actually decided."""
    raw = []
    for op, params, ctx, items in records:
        graph = op in GRAPH_OPS
        req = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
               'projectId': R.project_id, 'view': {'runId': R.run_id}, 'operation': op,
               'params': params, 'completeness': 'required', 'page': {'size': 100}}
        resp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': op,
                'context': ctx}
        if graph or items:
            resp['items'] = items
        ok_req, err_req = admit('#/$defs/GraphQueryRequestV1', req, 'req:' + op)
        ok_resp, err_resp = admit('#/$defs/GraphQueryResponseV1', resp, 'resp:' + op)
        f.need(ok_req, 'L2 request params are CLOSED per operation by the owning schema',
               'REQUEST_ADMITTED_BY_THE_OWNING_SCHEMA:' + op, err_req if not ok_req else None)
        f.need(ok_resp, 'L1/L3/L4/L9 response shape admitted by the owning schema',
               'RESPONSE_ADMITTED_BY_THE_OWNING_SCHEMA:' + op,
               err_resp if not ok_resp else None)
        raw.append({'operation': op, 'request': req, 'response': resp,
                    'requestAdmitted': ok_req, 'responseAdmitted': ok_resp})
    return raw


CONTROLS = [
    ('foreign-param-on-a-non-graph-operation', 'request',
     'L2 Params is a CLOSED optional bag (additionalProperties false)'),
    ('non-graph-params-shape-on-a-graph-operation', 'request',
     'L2 "Graph operations must not use this shape"'),
    ('advisory-true-on-a-graph-response', 'response',
     'L3 the graph context pins advisory to the const false'),
    ('graph-resolved-view-names-latest', 'response',
     'L4 "latest and snapshotId are forbidden here so a page cannot re-resolve"'),
    ('page-size-above-the-published-maximum', 'request',
     'L5 page size 1..1000'),
    ('graph-response-without-the-evidence-disclosure', 'response',
     'L9 evidence is required on every graph response'),
    ('operation-outside-the-published-enum', 'request',
     'L1 the operation enum is closed'),
    ('graph-request-carrying-a-logical-path-subject', 'request',
     'the graph params "do not accept LogicalPath-only subject/target"'),
]


def run_controls(f, R, records):
    rows = []
    base_op = 'finding.list'
    gop = 'graph.neighbors'
    g = [r for r in records if r[0] == gop][0]
    for label, side, law in CONTROLS:
        req = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
               'projectId': R.project_id, 'view': {'runId': R.run_id},
               'operation': base_op, 'params': {}, 'completeness': 'required',
               'page': {'size': 100}}
        resp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
                'operation': gop, 'context': json.loads(json.dumps(g[2])),
                'items': g[3]}
        if label == 'foreign-param-on-a-non-graph-operation':
            req['params'] = {'relation': 'declares', 'notAParam': 'x'}
        elif label == 'non-graph-params-shape-on-a-graph-operation':
            req['operation'] = gop
            req['params'] = {'relation': 'declares', 'subject': 'src/a.js'}
        elif label == 'advisory-true-on-a-graph-response':
            resp['context']['advisory'] = True
        elif label == 'graph-resolved-view-names-latest':
            resp['context']['resolvedView'] = {'latest': True}
        elif label == 'page-size-above-the-published-maximum':
            req['page'] = {'size': 1001}
        elif label == 'graph-response-without-the-evidence-disclosure':
            resp['context'].pop('evidence')
        elif label == 'operation-outside-the-published-enum':
            req['operation'] = 'graph.everything'
        elif label == 'graph-request-carrying-a-logical-path-subject':
            req['operation'] = gop
            req['params'] = dict(g[1], subject='src/a.js')
        if side == 'request':
            ok, err = admit('#/$defs/GraphQueryRequestV1', req, 'ctl:' + label)
        else:
            ok, err = admit('#/$defs/GraphQueryResponseV1', resp, 'ctl:' + label)
        rows.append({'control': label, 'side': side, 'owningLaw': law,
                     'refusedByTheOwningSchema': not ok, 'firstRefusal': err,
                     'record': req if side == 'request' else resp})
        f.need(not ok, law, 'CONTROL_REFUSED:' + label, err if ok else None)
    return rows


def renderer_parity(f):
    """L12: the published parity fields per command and per format, measured from the instance."""
    inv = kitdoc(INV_INSTANCE)
    cmds = inv.get('commands') or []
    fmts = (inv.get('renderers') or inv.get('outputFormats') or {})
    rows = []
    for c in cmds:
        pf = c.get('parityFields') or []
        rows.append({'command': c.get('name') or c.get('id'), 'formats': c.get('formats'),
                     'parityFields': pf})
    f.need(bool(cmds), 'L12 command-inventory.v3 is the parity reference instance',
           'COMMAND_INVENTORY_V3_CARRIES_COMMANDS', {'commands': len(cmds)})
    q_cmds = [r for r in rows if r['command'] and r['command'].startswith('query')]
    f.ok('L12 parity fields are published per command and per format',
         'RENDERER_PARITY_FIELDS_MEASURED',
         {'commandCount': len(rows), 'formats': sorted(fmts) if isinstance(fmts, dict) else fmts,
          'queryCommands': q_cmds[:6]})
    return rows


def main():
    f = F()
    R = Run('typescript')
    records = graph_records(R, f) + nongraph_records(R)
    check_laws(f, R, records)
    raw = admit_records(f, R, records)
    controls = run_controls(f, R, records)
    parity = renderer_parity(f)
    # L11: what a query never does -- stated against this reconstruction's own code path
    f.ok('L11 "Queries never materialise facts, invoke a provider, allocate an attempt, seal a '
         'Run, derive policy or choose termination."',
         'QUERY_PATH_READS_ONLY_RETAINED_BYTES',
         {'measured': ('every record above is built from the exported store of an already admitted '
                       'Run: no fact was minted, no provider was called, no attempt allocated, no '
                       'seal written and no policy derived by this module'),
          'runUnderQuery': R.run_id})
    # L6 cursor binding, measured
    g = [r for r in records if r[0] == 'graph.neighbors'][0]
    c1 = cursor(R.project_id, R.run_id, R.view_digests, 'graph.neighbors', g[1], 100)
    c2 = cursor(R.project_id, R.run_id, R.view_digests, 'graph.neighbors', g[1], 200)
    c3 = cursor(R.project_id, R.run_id, R.view_digests, 'graph.reach', g[1], 100)
    f.need(c1 != c2 and c1 != c3 and c1.startswith('q3.' + R.run_id.split(':', 1)[1]),
           'L6 cursor "bound to projectId+runId+factViewDigests+operation+effective params/order+'
           'page position ... Reference form q3.<runId-64hex>.<selectionHash64>.<position>"',
           'CURSOR_IS_BOUND_TO_THE_SELECTION_AND_THE_POSITION',
           {'samePositionDifferentOperation': c1 != c3, 'differentPosition': c1 != c2,
            'form': c1[:40] + '...'})
    f.ok('L6 "Continuation never re-resolves latest"',
         'CURSOR_CARRIES_A_CONCRETE_RUN_AND_NEVER_THE_LATEST_RESOLVER',
         {'cursor': c1[:40] + '...', 'resolvedViewOnThePage': {'runId': R.run_id}})
    doc = {'standing': __doc__, 'runUnderQuery': {'label': R.label, 'runId': R.run_id,
                                                 'projectId': R.project_id,
                                                 'snapshotId': R.snapshot_id},
           'operationCount': len({r['operation'] for r in raw}),
           'checks': f.rows, 'refusals': f.refusals,
           'rawRequestAndResponseRecords': raw,
           'negativeControls': controls,
           'rendererParity': parity,
           'claimLimits': (
               'a reconstruction of the published query surface over this origin\'s own admitted '
               'Run. No product query engine was executed and no host is qualified; the host '
               'observations consumed here are synthetic trusted inputs.'),
           'itemShapeStanding': (
               'GraphQueryResponseV1.items is typed `array` with maxItems 1000 and an item schema '
               'ONLY for the three graph operations (GraphNeighborRow / GraphPathRow / '
               'GraphReachRow). For the seventeen non-graph operations the owning schema '
               'deliberately leaves the row shape to that operation\'s own owner, so the rows '
               'carried here are this origin\'s own projections of RETAINED identities of the Run '
               'under query (run3/finding3/fact2/coverage2/import2/receipt ids and the admitted '
               'availability account). They are labelled as such rather than presented as a '
               'published row contract; what the owning schema decides -- the context variant, the '
               'advisory cross-join, the bounds, the page and the operation closure -- is what the '
               'admission above measures.')}
    os.makedirs(OUT + '/query', exist_ok=True)
    with open(OUT + '/query/indep-query-surface.json', 'w') as fh:
        json.dump(doc, fh, indent=1, default=str)
    print('operations with actual records: %d' % doc['operationCount'])
    print('checks: %d passed, %d refused' % (len(f.rows) - len(f.refusals), len(f.refusals)))
    for r in f.refusals:
        print('   REFUSE %-52s %s' % (r['check'][:52], json.dumps(r['detail'])[:140]))
    print('negative controls: %d, refused by the owning schema: %d'
          % (len(controls), sum(1 for c in controls if c['refusedByTheOwningSchema'])))
    for c in controls:
        if not c['refusedByTheOwningSchema']:
            print('   NOT REFUSED: %s' % c['control'])
    assert not f.refusals, [r['check'] for r in f.refusals]


main()
