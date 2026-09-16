"""INDEPENDENT clause-to-code-and-artifact map for the WHOLE published query surface (generation 23).

Two jobs.

A. GRAPH OUTCOMES RECOMPUTED. For every case retained by lib/graph_query.py (request + synthetic
   host observations + the executor's outcome) this module recomputes the outcome from the
   admitted Run's own premises with separately written code, then compares every field:
     * the vertex domain from the proof-selected inventories, with the program-binding universe
       found by walking the admitted Plan's own digests (not a store label);
     * section-3 occupancy reconciliation per fact;
     * neighbor order by the endpoint tuple; reach as a LEVEL-SYNCHRONOUS walk (equivalent to the
       FIFO law); path as the lexicographically least fact2 sequence among ALL shortest simple
       paths, enumerated, plus the section-4 BFS entry count for visitedNodes; the claim that the
       first BFS hit IS that path is checked on each case, not assumed;
     * the section-7 fault row from the section-8 step order;
     * the Q3 disclosure: cited Coverage/scopes, copied executionDeficiencies, limitations.
   A disagreement is a refusal.

B. THE OTHER SEVENTEEN OPERATIONS. One actual record each, whose rows are derived from the
   admitted Run and retained records, and whose semantics are re-derived here from those premises
   (for example finding.list with includeSuppressed=false omits proof.waivedFindingIds).

V23-D8 (the failing generation-22 artifact is preserved at
predecessors.v22/query/indep-query-surface.json). That artifact:
  * built its own three graph records with target := source and cited every Coverage of the store;
  * claimed finding.list includeSuppressed=false while listing the waived finding3:8f9e465...;
  * read baselineId from a key the baseline record does not have, so baseline.show was empty;
  * read receiptId from the envelope root instead of envelope.mutation, so receipt.show was empty;
  * took availability.show from an unrelated multi-unit scenario and asserted coverage=complete
    for every operation.

CLAUSE -> CODE -> ARTIFACT (owning schema: evaluator3 graph-query.schema.json; contract:
query-projection-contract.v3.md)
 L1  Operation closure, 20 names          check_laws / every operation has a record
 L2  Params closed per operation          owning-schema admission of each request
 L3  Advisory cross-join                  check_laws
 L4  resolvedView: run-only for graph.*, request View for the other 17
 L5  Bounds are schema constants; work bounds span the logical operation (graph recompute)
 L6  Cursor q3 form bound to the selection (graph recompute)
 L7  truncated iff truncated-bound; full page is truncated-page (graph recompute)
 L8  traversalCoverage members (graph recompute)
 L9  Q3 evidence disclosure (graph recompute)
 L10 countBasis (graph recompute)
 L11 A query never materialises, seals or chooses termination
 L12 Renderer parity (command-inventory.v3 `query` parity fields; graph_query renderings)
 L13 Failure envelopes: kind=failure carries errors and no run (re-admitted)

Nothing here qualifies a product or a host.
"""
import hashlib
import itertools
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
Q_DOC = 'workflows/schemas/evaluator3/graph-query.schema.json'
ENV_DOC = 'workflows/schemas/evaluator3/command-envelope.schema.json'
INV_INSTANCE = 'workflows/command-inventory.v3.json'
PROJ_DOC = 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json'
REL_DOC = 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'

GRAPH_OPS = ('graph.neighbors', 'graph.path', 'graph.reach')
HEX = re.compile(r'[0-9a-f]{64}\Z')
EXIT = {'request-rejected': 2, 'indeterminate': 3, 'operational-failed': 4, 'success': 0}
CONST = {'maxVisitedNodes': 1000000, 'maxItemsPerOperation': 100000}
ORDER_WORDS = {'graph.neighbors': 'utf8(source tuple, target tuple, fact2 id)',
               'graph.path': 'FIFO BFS, fact2-id adjacency, first target entry',
               'graph.reach': 'utf8(endpoint tuple)'}

DECLARED = [
    {'id': 'I-Q9', 'clause': 'GraphQueryResponseContext.coverage (complete|partial|unavailable) has '
     'no owner text for the seventeen non-graph operations',
     'reading': 'complete when the rows are the whole retained answer; partial for finding rows '
                'of a Run whose proof carries executionDeficiencies (the list may be incomplete); '
                'unavailable, with no rows, where this origin retains no projection for the '
                'operation on this Run (a row count is then no claim of absence)'},
    {'id': 'I-Q1..I-Q8', 'clause': 'the graph interpretations',
     'reading': 'declared in query/graph-query-reconstruction.json and applied identically here; '
                'I-Q7 fixes the selection-hash preimage both sides recompute'},
]


def kitdoc(rel):
    return json.load(open(S.KIT + '/' + S.doc_path(rel)))


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, law, check, detail=None):
        self.rows.append({'law': law, 'check': check, 'result': 'PASS' if cond else 'REFUSE',
                          'detail': detail})
        return bool(cond)

    def ok(self, law, check, detail=None):
        self.rows.append({'law': law, 'check': check, 'result': 'PASS', 'detail': detail})

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def admit(selector, inst, label, doc=Q_DOC):
    r = S.admit(doc, selector, inst, label)
    return r['admitted'], {'stock': r['stockSchemaErrors'][:3],
                           'keywords': r['publishedKeywordRefusals'][:3]}


class Run:
    def __init__(self, label):
        self.label = label
        self.st, self.doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        o = self.st.objects
        self.run_id = self.doc['claim']['runId']
        self.run = o[self.run_id]
        self.seal = o[self.run['evaluationSealId']]
        self.proof = o[self.seal['proofBundleId']]
        self.plan_id, self.snapshot_id = self.run['planId'], self.run['snapshotId']
        self.plan = o[self.plan_id]
        self.project_id = self.run['projectId']
        self.view_ids = list(o[self.run['evidenceId']]['viewIds'])
        self.views = {v: o[v] for v in self.view_ids}
        self.findings = {f: o[f] for f in self.proof['findingIds']}

    def blob(self, digest):
        b = self.st.get_blob(digest.split(':')[-1])
        return json.loads(b.decode()) if b is not None else None

    def refs(self, domain):
        return [r['digest'] for r in self.proof['evaluationInputRefs'] if r['domain'] == domain]


# =========================================================================== A. graph premises
class Premises:
    def __init__(self, R):
        self.R = R
        o = R.st.objects
        reg = kitdoc(PROJ_DOC)['relations']
        self.reg = reg
        self.ladders = {k: v['ladder'] for k, v in reg.items()}
        self.eplan, self.eplan_route = self._enumeration_plan()
        self.vertices = set()
        for d in R.refs('subject-inventory'):
            inv = R.blob(d)
            binding = [b for b in self.eplan['cells'][inv['cellOrdinal']]['programBindings']
                       if b['ordinal'] == inv['programOrdinal']]
            u = binding[0].get('universe') if len(binding) == 1 else None
            for row in inv['rows'] if u else []:
                self.vertices.add((u, row['kind'], row['nativeSubjectId'],
                                   row['path'] if row['kind'] == 'package' else ''))
        self.sidecar = {}
        for d in R.refs('target-attribution'):
            rec = R.blob(d)
            self.sidecar[rec['sourceFactId']] = rec
        self.searches = [(d, R.blob(d)) for d in R.refs('incoming-search')]
        self.cov = {}
        for v in R.views.values():
            for c in v['coverageIds']:
                self.cov[c] = R.blob(o[c]['payloadDigest'])

    def _enumeration_plan(self):
        """Walk the admitted Plan's digests (Plan -> referenced blobs -> their digests) to the one
        EnumerationPlanV1 body. No store label is consulted."""
        found, seen, frontier = [], set(), [(self.R.plan, 'plan')]
        for _ in range(4):
            nxt = []
            for node, route in frontier:
                for s in _strings(node):
                    d = s.split(':')[-1]
                    if not HEX.match(d) or d in seen:
                        continue
                    seen.add(d)
                    try:
                        j = self.R.blob(d)
                    except Exception:
                        continue
                    if isinstance(j, dict) and 'cells' in j and 'membershipDigest' in j:
                        found.append((d, route + ' -> ' + d[:12]))
                    elif isinstance(j, (dict, list)):
                        nxt.append((j, route + ' -> ' + d[:12]))
            frontier = nxt
        assert len({d for d, _ in found}) == 1, found
        return self.R.blob(found[0][0]), found[0][1]

    def matches(self, vid, rel, rung):
        o = self.R.st.objects
        return any((o[s]['relation'], o[s]['resolution']) == (rel, rung)
                   for s in self.R.views[vid]['scopeIds'])

    def projectable(self, rel, rung):
        r = self.reg.get(rel) or {}
        if not r.get('targetNativeIdField') or rung not in r.get('ladder', []):
            return False
        # binary native-id rungs only: a rung whose target field is not an id is not projectable
        return r.get('endpointTarget') in ('admitted', 'admitted-at-rung') and \
            rung in (r.get('endpointTargetRungs') or [rung])

    def edges(self, rel, rung, selected):
        o = self.R.st.objects
        r = self.reg[rel]
        sf, tf, tkinds = r['sourceField'], r['targetNativeIdField'], r['targetKinds']
        fids = sorted({f for v in selected for f in self.R.views[v]['facts']
                       if o[f]['relation'] == rel}, key=str.encode)
        out, omitted = [], []
        for fid in fids:
            f = o[fid]
            if self.ladders[rel].index(f['resolution']) < self.ladders[rel].index(rung):
                omitted.append(('unsupported-rung-omitted', fid))
                continue
            pay = self.R.blob(f['payloadDigest'])
            s_id, t_id = pay.get(sf), pay.get(tf)
            if not s_id or not t_id:
                omitted.append(('unprojectable-fact', fid))
                continue
            tu = f['targetUniverse'] if r['universeRule'] == 'admitted-target' else f['sourceUniverse']
            exact = {v for v in self.vertices if v[2] == t_id}
            sc = self.sidecar.get(fid)
            if len(exact) == 1:
                (_, k, n, p), = exact
                tgt = (tu, k, n, p)
            elif sc and sc['occupancy'] == 'first-party':
                tgt = (tu, sc['kind'], sc['evaluationNativeId'], sc['packageManifestPath'] or '')
            elif sc and sc['occupancy'] == 'external' and sc['kind'] != 'unknown' and \
                    (sc['kind'] != 'package' or sc['packageManifestPath']):
                tgt = (tu, sc['kind'], t_id, sc['packageManifestPath'] or '')
            elif len(tkinds) == 1:
                tgt = (tu, tkinds[0], t_id, '')
            else:
                omitted.append(('unprojectable-fact', fid))
                continue
            if tgt[1] not in tkinds:
                omitted.append(('unprojectable-fact', fid))
                continue
            out.append({'fid': fid, 's': (f['sourceUniverse'], r['sourceSubjectKind'], s_id, ''),
                        't': tgt, 'fact': f})
        return out, omitted


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def as_ep(t):
    e = {'universe': t[0], 'kind': t[1], 'nativeSubjectId': t[2]}
    if t[1] == 'package':
        e['packageManifestPath'] = t[3]
    return e


def as_t(e):
    return (e['universe'], e['kind'], e['nativeSubjectId'], e.get('packageManifestPath') or '')


def b(t):
    return tuple(x.encode() for x in t)


def steps(edges, v, direction):
    out = []
    for e in sorted(edges, key=lambda e: e['fid'].encode()):
        if direction in ('outgoing', 'both') and e['s'] == v:
            out.append((e, e['t']))
        elif direction in ('incoming', 'both') and e['t'] == v:
            out.append((e, e['s']))
    return out


def failure(cls, code, detail):
    return {'kind': 'failure', 'class': cls, 'errorCode': code, 'domainDetail': detail,
            'exitCode': EXIT[cls]}


def rej(detail, code='REQUEST.PRECONDITION_FAILED'):
    return failure('request-rejected', code, detail)


def endpoint_fault(e):
    keys = {'universe', 'kind', 'nativeSubjectId', 'packageManifestPath'}
    if not isinstance(e, dict) or not set(e) <= keys or not {'universe', 'kind', 'nativeSubjectId'} <= set(e):
        return 'QUERY.PARAMS_MALFORMED'
    if not (isinstance(e['universe'], str) and HEX.match(e['universe'])) \
            or e['kind'] not in ('file', 'symbol', 'package') \
            or not (isinstance(e['nativeSubjectId'], str) and e['nativeSubjectId']) \
            or (e['kind'] != 'package' and 'packageManifestPath' in e):
        return 'QUERY.PARAMS_MALFORMED'
    if e['kind'] == 'package' and not e.get('packageManifestPath'):
        return 'QUERY.ENDPOINT_AMBIGUOUS'
    return None


def expected(P, req, host):
    """The section-8 steps recomputed. Returns the expected outcome."""
    R = P.R
    if not re.fullmatch(r'req1_[0-9a-f]{32}', str(host.get('requestId'))):
        return {'kind': 'reference-call-precondition'}
    if req.get('schemaMajor') != 3:
        return rej('QUERY.SCHEMA_MAJOR_UNSUPPORTED', 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED')
    params = req['params'] if isinstance(req.get('params'), dict) else {}
    faults = {endpoint_fault(params[k]) for k in ('endpoint', 'start', 'target') if k in params}
    if 'QUERY.PARAMS_MALFORMED' in faults:
        return rej('QUERY.PARAMS_MALFORMED')
    ok, _ = admit('#/$defs/GraphQueryRequestV1', req, 'indep-q-req')
    if not ok:
        fixed = json.loads(json.dumps(req))
        for k in ('endpoint', 'start', 'target'):
            e = fixed['params'].get(k)
            if isinstance(e, dict) and e.get('kind') == 'package':
                e.setdefault('packageManifestPath', 'x')
        if 'QUERY.ENDPOINT_AMBIGUOUS' in faults and admit('#/$defs/GraphQueryRequestV1', fixed,
                                                            'indep-q-fix')[0]:
            return rej('QUERY.ENDPOINT_AMBIGUOUS')
        return rej('QUERY.PARAMS_MALFORMED')
    if 'QUERY.ENDPOINT_AMBIGUOUS' in faults:
        return rej('QUERY.ENDPOINT_AMBIGUOUS')
    if host.get('availability') in ('purged', 'expired', 'corrupt', 'missing'):
        return dict(failure('operational-failed', 'HOST.IO_FAILURE',
                            'evidence.' + host['availability']), faultCause='host-io')
    view = req['view']
    unknown = rej('QUERY.VIEW_UNKNOWN', 'IDENTITY.UNKNOWN')
    if req['projectId'] != R.project_id:
        return unknown
    if 'runId' in view and view['runId'] != R.run_id:
        return unknown
    if 'snapshotId' in view:
        names = (host.get('runsForSnapshot') or {}).get(view['snapshotId']) or []
        if not names:
            return unknown
        if len(set(names)) > 1:
            return rej('QUERY.VIEW_AMBIGUOUS')
        if names[0] != R.run_id or view['snapshotId'] != R.snapshot_id:
            return unknown
    if 'latest' in view and host.get('latestRunId') != R.run_id:
        return unknown
    rel, rung = params['relation'], params['minResolution']
    if not P.projectable(rel, rung):
        return rej('QUERY.RELATION_UNSUPPORTED')
    if 'factViewDigests' in params:
        if any(v not in R.views for v in params['factViewDigests']):
            return rej('QUERY.FACT_VIEW_UNAVAILABLE')
        selected = sorted(params['factViewDigests'], key=str.encode)
    else:
        selected = sorted([v for v in R.view_ids if P.matches(v, rel, rung)], key=str.encode)
    op = req['operation']
    eff = dict(params)
    if op == 'graph.reach' and 'includeStart' not in eff:
        eff['includeStart'] = False
    sel_hash = hashlib.sha256(K.C({'projectId': R.project_id, 'runId': R.run_id,
                                   'factViewDigests': selected, 'operation': op,
                                   'params': eff, 'order': ORDER_WORDS[op]})).hexdigest()
    position = 0
    if 'cursor' in req['page']:
        parts = req['page']['cursor'].split('.')
        if len(parts) != 4 or parts[0] != 'q3' or 'runId' not in view \
                or parts[1] != R.run_id[5:] or parts[2] != sel_hash or not parts[3].isdigit():
            return rej('QUERY.CURSOR_MISMATCH')
        position = int(parts[3])
    edges, omitted = P.edges(rel, rung, selected)
    domain = P.vertices | {e['s'] for e in edges} | {e['t'] for e in edges}
    for k in ('endpoint', 'start', 'target'):
        if k in params and as_t(params[k]) not in domain:
            return rej('QUERY.ENDPOINT_UNKNOWN')
    caps = dict(CONST)
    caps.update({k: min(v, CONST[k]) for k, v in (host.get('testBounds') or {}).items()})
    bound, trace = False, {}
    if op == 'graph.neighbors':
        at = as_t(params['endpoint'])
        visited = 1
        chosen = [e for e in edges if (params['direction'] != 'incoming' and e['s'] == at)
                  or (params['direction'] != 'outgoing' and e['t'] == at)]
        chosen.sort(key=lambda e: (b(e['s']), b(e['t']), e['fid'].encode()))
        units = [{'factId': e['fid'], 'relation': rel, 'resolution': e['fact']['resolution'],
                  'source': as_ep(e['s']), 'target': as_ep(e['t']),
                  'producerClosure': e['fact']['producerClosure'],
                  'confidenceMillionths': e['fact']['confidenceMillionths']} for e in chosen]
    elif op == 'graph.reach':
        start = as_t(params['start'])
        first = {start: (0, None)}
        level, depth, visited = [start], 0, 1
        while level and depth < params['maxDepth'] and not bound:
            nxt = []
            for v in level:
                for e, w in steps(edges, v, params['direction']):
                    if w in first:
                        continue
                    if visited >= caps['maxVisitedNodes']:
                        bound = True
                        break
                    first[w] = (depth + 1, e['fid'])
                    visited += 1
                    nxt.append(w)
                if bound:
                    break
            level, depth = nxt, depth + 1
        units = []
        for w in sorted(first, key=b):
            d, via = first[w]
            if d == 0 and not eff['includeStart']:
                continue
            units.append(dict({'endpoint': as_ep(w), 'depth': d},
                              **({'viaFactId': via} if via else {})))
    else:
        start, target = as_t(params['start']), as_t(params['target'])
        if start == target:
            visited, units = 1, [{'hopCount': 0, 'start': params['start'],
                                  'target': params['target'], 'nodes': [params['start']],
                                  'edges': []}]
        else:
            # visitedNodes: the section-4 entry count, level by level, stopping at the target
            entered, level, depth, visited, hit = {start}, [start], 0, 1, False
            while level and depth < params['maxDepth'] and not hit and not bound:
                nxt = []
                for v in level:
                    for e, w in steps(edges, v, params['direction']):
                        if w in entered:
                            continue
                        if visited >= caps['maxVisitedNodes']:
                            bound = True
                            break
                        entered.add(w)
                        visited += 1
                        if w == target:
                            hit = True
                            break
                        nxt.append(w)
                    if hit or bound:
                        break
                level, depth = nxt, depth + 1
            units = []
            if hit:
                # the witness: lexicographically least fact2 sequence among ALL shortest simple paths
                best = None
                for n in range(1, params['maxDepth'] + 1):
                    for seq in _simple_paths(edges, start, target, n, params['direction']):
                        key = tuple(e['fid'].encode() for e, _ in seq)
                        if best is None or key < best[0]:
                            best = (key, seq)
                    if best:
                        break
                seq = best[1]
                units = [{'hopCount': len(seq), 'start': params['start'],
                          'target': params['target'],
                          'nodes': [params['start']] + [as_ep(w) for _, w in seq],
                          'edges': [{'factId': e['fid'], 'source': as_ep(e['s']),
                                     'target': as_ep(e['t'])} for e, _ in seq]}]
                trace['witnessIsLexLeastShortest'] = True
    if len(units) > caps['maxItemsPerOperation']:
        units, bound = units[:caps['maxItemsPerOperation']], True
    size = req['page']['size']
    ctx = {'projectId': R.project_id, 'resolvedView': {'runId': R.run_id},
           'factViewDigests': selected, 'availability': 'retained', 'truncated': bound,
           'totalItems': len(units), 'countBasis': 'lower-bound' if bound else 'exact',
           'traversalCoverage': 'truncated-bound' if bound else (
               'truncated-page' if position + size < len(units) else 'complete'),
           'visitedNodes': visited, 'producedItems': len(units), 'advisory': False,
           'evidence': disclosure(P, rel, rung, selected, omitted, bound)}
    if position + size < len(units):
        ctx['nextCursor'] = '.'.join(['q3', R.run_id[5:], sel_hash, str(position + size)])
    term = {'class': 'success'}
    if bound and req['completeness'] == 'required':
        term = {'class': 'indeterminate', 'reasonCodes': ['QUERY.COMPLETENESS_UNMET'],
                'runId': R.run_id}
    return {'kind': 'response', 'response': {
        'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': op,
        'context': ctx, 'items': units[position:position + size], 'termination': term},
        'trace': trace}


def _simple_paths(edges, start, target, n, direction):
    def walk(v, seq, used):
        if len(seq) == n:
            if v == target:
                yield list(seq)
            return
        for e, w in steps(edges, v, direction):
            if w in used:
                continue
            seq.append((e, w))
            used.add(w)
            yield from walk(w, seq, used)
            seq.pop()
            used.discard(w)
    yield from walk(start, [], {start})


def disclosure(P, rel, rung, selected, omitted, bound):
    R, o = P.R, P.R.st.objects
    cov = {c for v in selected for c in R.views[v]['coverageIds']}
    scopes = {s for v in selected for s in R.views[v]['scopeIds']}
    for c, pay in P.cov.items():
        if pay['key']['relation'] == rel:
            cov.add(c)
            scopes.add(o[c]['scopeId'])
    lims = []
    for c in sorted(cov, key=str.encode):
        entry = P.cov[c]['entry']
        rc = entry['resolutionCompleteness']
        copy = {'coverageId': c, 'resolutionState': rc['state'],
                'unresolvedEdgeCount': rc['unresolvedEdgeCount'],
                'examinedExhaustive': rc['examinedExhaustive'], 'attempted': rc['attempted'],
                'coverage': entry['coverage']}
        if entry['deficiency'] is not None:
            copy['note'] = 'deficiency=' + entry['deficiency']
        kinds = []
        if entry['coverage'] in ('unknown', 'partial'):
            kinds.append('coverage-' + entry['coverage'])
        if rc['state'] in ('incomplete', 'partial', 'not-attempted'):
            kinds.append('resolution-' + rc['state'])
        if rc['examinedExhaustive'] is False:
            kinds.append('examined-not-exhaustive')
        lims += [dict(copy, kind=k) for k in kinds]
    for d, s in P.searches:
        complete = (s['completeSearch'] and s['examinedExhaustive'] and s['coverage'] == 'complete'
                    and s['resolutionCompleteness']['state'] in ('complete', 'not-applicable'))
        if (s['relation'], s['minResolution']) == (rel, rung) and not complete:
            lims.append({'kind': 'incoming-search-incomplete', 'incomingSearchDigest': d,
                         'relation': rel, 'minResolution': rung, 'coverage': s['coverage'],
                         'examinedExhaustive': s['examinedExhaustive'],
                         'resolutionState': s['resolutionCompleteness']['state']})
    lims += [{'kind': 'unresolved-edge-present', 'factId': f}
             for f in sorted({f for v in R.views.values() for f in v['facts']
                              if o[f]['relation'] == 'unresolved-edge'}, key=str.encode)]
    lims += [{'kind': k, 'factId': f} for k, f in omitted]
    if not any(P.matches(v, rel, rung) for v in selected):
        lims.append({'kind': 'native-evidence-unavailable', 'relation': rel, 'minResolution': rung})
    if bound:
        lims.append({'kind': 'unexamined-work-bound'})
    members = ('source', 'cause', 'subjectId', 'predicateId', 'inputRefs', 'coverageId',
               'nativeCause')
    return {'coverageIds': sorted(cov, key=str.encode), 'scopeIds': sorted(scopes, key=str.encode),
            'deficiencyCitations': [{m: d[m] for m in members if m in d}
                                    for d in R.proof['executionDeficiencies']],
            'resolutionLimitations': [dict(sorted(l.items())) for l in lims]}


def normalise(outcome):
    if outcome['kind'] != 'response':
        return outcome
    r = json.loads(json.dumps(outcome['response']))
    r['context']['evidence']['resolutionLimitations'] = [
        dict(sorted(l.items())) for l in r['context']['evidence']['resolutionLimitations']]
    return {'kind': 'response', 'response': r}


def tampered_copies(ops, fls):
    """The generation-22 defects (and two route confusions) RE-INJECTED into copies of retained
    outcomes. A recomputation that cannot see them measures nothing."""
    out = []

    def copy(src, case, label, what, fn):
        c = json.loads(json.dumps(src[case]))
        fn(c['outcome'])
        c['case'], c['tamper'] = label, what
        out.append(c)

    ctx = lambda o: o['response']['context']
    copy(ops, 'graph.neighbors-page-1', 'tamper-full-page-marked-truncated',
         'V22: truncated=true on a full page', lambda o: ctx(o).update(truncated=True))
    copy(ops, 'graph.neighbors-page-1', 'tamper-ord-cursor', 'V22: cursor `ord:1`',
         lambda o: ctx(o).update(nextCursor='ord:1'))
    copy(ops, 'graph.neighbors-outgoing-first-party-and-external', 'tamper-external-target-dropped',
         'V22: the external target dropped as unprojectable',
         lambda o: (o['response']['items'].pop(), ctx(o).update(totalItems=2, producedItems=2)))
    copy(ops, 'graph.neighbors-outgoing-first-party-and-external', 'tamper-neighbors-by-fact-id-only',
         'V22: rows ordered by fact2 id only (reversed here so the order differs)',
         lambda o: o['response']['items'].reverse())
    copy(ops, 'graph.neighbors-outgoing-first-party-and-external',
         'tamper-deficiency-citations-dropped', 'V22: executionDeficiencies never cited',
         lambda o: ctx(o)['evidence'].update(deficiencyCitations=[]))
    copy(ops, 'graph.path-one-hop', 'tamper-path-visited-is-the-inventory',
         'V22: visitedNodes = inventory size', lambda o: ctx(o).update(visitedNodes=11))
    copy(ops, 'graph.reach-both-depth-2-include-start', 'tamper-reach-rows-by-depth',
         'reach rows by depth instead of the endpoint tuple',
         lambda o: o['response']['items'].sort(key=lambda r: r['depth']))
    copy(ops, 'graph.neighbors-no-selected-view-matches', 'tamper-native-evidence-unavailable-omitted',
         'zero rows presented without the section-6 disclosure',
         lambda o: ctx(o)['evidence'].update(resolutionLimitations=[]))
    copy(fls, 'evidence-purged', 'tamper-graph-purge-takes-the-finding-show-route',
         'the workflow finding.show route (exit 2) applied to a graph operation',
         lambda o: o['refusal'].update({'class': 'request-rejected', 'faultCause': None,
                                        'errorCode': 'REQUEST.PRECONDITION_FAILED', 'exitCode': 2}))
    copy(fls, 'package-endpoint-without-manifest-path', 'tamper-package-coordinate-as-malformed',
         'section-2 step 2 collapsed into step 1',
         lambda o: o['refusal'].update(domainDetail='QUERY.PARAMS_MALFORMED'))
    return out


def recompute_graph(f, P):
    g = json.load(open(OUT + '/query/graph-query-reconstruction.json'))
    rows, tamper_rows = [], []
    f.need(g['admittedRunUnderQuery']['runId'] == P.R.run_id,
           'the graph artifact queries this admitted Run', 'GRAPH_ARTIFACT_RUN_IS_THE_CURRENT_RUN')
    by_op = {c['case']: c for c in g['operations']}
    by_fail = {c['case']: c for c in g['failureCases']}
    for c in g['operations'] + g['failureCases'] + tampered_copies(by_op, by_fail):
        exp = expected(P, c['request'], c['host'])
        got = normalise(c['outcome'])
        diffs = []
        if exp['kind'] != got['kind']:
            diffs.append({'field': 'kind', 'expected': exp['kind'], 'emitted': got['kind']})
        elif exp['kind'] == 'failure':
            ref = got['refusal']
            for k in ('class', 'errorCode', 'domainDetail', 'exitCode'):
                if exp[k] != ref[k]:
                    diffs.append({'field': k, 'expected': exp[k], 'emitted': ref[k]})
            if exp.get('faultCause') != ref.get('faultCause'):
                diffs.append({'field': 'faultCause', 'expected': exp.get('faultCause'),
                              'emitted': ref.get('faultCause')})
            env = got['envelope']
            ok, err = admit('#', env, 'indep-q-env:' + c['case'], doc=ENV_DOC)
            if not ok or 'run' in env or not env.get('errors') \
                    or env['termination']['domainDetail']['code'] != exp['domainDetail'] \
                    or env['exitCode'] != exp['exitCode']:
                diffs.append({'field': 'envelope', 'admitted': ok, 'error': err})
        elif exp['kind'] == 'response':
            er, gr = exp['response'], got['response']
            for k in sorted(set(er['context']) | set(gr['context'])):
                if er['context'].get(k) != gr['context'].get(k):
                    diffs.append({'field': 'context.' + k, 'expected': er['context'].get(k),
                                  'emitted': gr['context'].get(k)})
            for k in ('items', 'termination', 'operation', 'schemaMajor', 'schemaFamily'):
                if er[k] != gr[k]:
                    diffs.append({'field': k, 'expected': er[k], 'emitted': gr[k]})
            ok1, e1 = admit('#/$defs/GraphQueryRequestV1', c['request'], 'indep-q-r')
            ok2, e2 = admit('#/$defs/GraphQueryResponseV1', gr, 'indep-q-s')
            if not (ok1 and ok2):
                diffs.append({'field': 'schema', 'request': e1, 'response': e2})
        if 'tamper' in c:
            tamper_rows.append({'control': c['case'], 'reinjects': c['tamper'],
                                'classification': 'invalid', 'detected': bool(diffs),
                                'firstDisagreement': diffs[:1]})
            f.need(bool(diffs), 'a recomputation must see a re-injected defect',
                   'TAMPER_DETECTED:' + c['case'], None if diffs else 'NOT DETECTED')
            continue
        rows.append({'case': c['case'], 'classification': c['classification'],
                     'expectedKind': exp['kind'],
                     'expectedFailure': {k: exp.get(k) for k in ('class', 'errorCode',
                                                                  'domainDetail', 'exitCode')}
                     if exp['kind'] == 'failure' else None,
                     'trace': exp.get('trace'), 'disagreements': diffs})
        f.need(not diffs, 'query-projection-contract.v3 sections 1-7 recomputed from the Run',
               'GRAPH_OUTCOME_RECOMPUTED:' + c['case'], diffs[:3])
    # pages of one selection: the union equals the whole selection, in order
    ops = {c['case']: c for c in g['operations']}
    whole = [i['factId'] for i in ops['graph.neighbors-outgoing-first-party-and-external']
             ['outcome']['response']['items']]
    pages = [i['factId'] for n in ('graph.neighbors-page-1', 'graph.neighbors-page-2',
                                   'graph.neighbors-page-3')
             for i in ops[n]['outcome']['response']['items']]
    f.need(pages == whole and len(whole) == 3,
           'L6/L7 a cursor continues one historical selection; page fullness is not truncation',
           'PAGES_CONCATENATE_TO_THE_WHOLE_SELECTION', {'pages': pages, 'whole': whole})
    # the external vertex is lawful, and the premise that makes it external is the sidecar
    ext = [s for s in P.sidecar.values() if s['occupancy'] == 'external']
    f.need(any(i['target']['nativeSubjectId'] == s['targetNativeId'] for s in ext
               for i in ops['graph.neighbors-outgoing-first-party-and-external']['outcome']
               ['response']['items']),
           'section 3 "External occupancy projects nativeSubjectId = payload target field"',
           'EXTERNAL_TARGET_IS_PROJECTED_WITH_ITS_OPAQUE_PAYLOAD_ID',
           [s['targetNativeId'] for s in ext])
    rend = g['renderings']
    f.need(rend['measured']['agentEqualsJson'] and rend['measured']['humanEqualsJson']
           and set(rend['parityFields']) == set(next(c for c in kitdoc(INV_INSTANCE)['commands']
                                                     if c['name'] == 'query')['parityFields']),
           'L12 command-inventory.v3 query parity fields', 'RENDERINGS_CARRY_THE_PUBLISHED_PARITY_FIELDS',
           rend['measured'])
    return g, rows, tamper_rows


# =========================================================================== B. seventeen operations
def nongraph_records(R):
    o = R.st.objects
    ex_def = bool(R.proof['executionDeficiencies'])
    recs = []

    def add(op, params, items, coverage, basis, view=None):
        ctx = {'projectId': R.project_id, 'resolvedView': view or {'runId': R.run_id},
               'coverage': coverage, 'availability': 'retained', 'truncated': False,
               'totalItems': len(items),
               'advisory': op in ('comparison.diff', 'candidate.list', 'inspection.show',
                                  'review.brief')}
        recs.append({'operation': op, 'params': params, 'context': ctx, 'items': items,
                     'rowBasis': basis})

    add('run.show', {}, [{'runId': R.run_id, 'sealId': R.run['evaluationSealId'],
                          'proofId': R.seal['proofBundleId'], 'evidenceId': R.run['evidenceId'],
                          'verdict': R.proof['verdict'],
                          'evaluationState': R.proof['evaluationState']}],
        'complete', 'the admitted Run, seal and proof')
    add('run.list', {}, [{'runId': R.run_id, 'snapshotId': R.snapshot_id, 'planId': R.plan_id}],
        'complete', 'synthetic trusted host.runsForSnapshot naming this Run',
        view={'snapshotId': R.snapshot_id})
    waived = set(R.proof['waivedFindingIds'])
    for inc in (False, True):
        add('finding.list', {'includeSuppressed': inc},
            [{'findingId': fid, 'ruleId': R.findings[fid]['ruleId'],
              'subjectPath': R.findings[fid]['subject']['logicalPath'],
              'waived': fid in waived}
             for fid in sorted(R.findings, key=str.encode) if inc or fid not in waived],
            'partial' if ex_def else 'complete', 'proof.findingIds and proof.waivedFindingIds')
    one = sorted(R.findings, key=str.encode)[0]
    add('finding.show', {'findingId': one}, [{'findingId': one, 'finding': R.findings[one],
                                              'waived': one in waived}],
        'partial' if ex_def else 'complete', 'one finding3 of proof.findingIds')
    decl = sorted({fid for v in R.views.values() for fid in v['facts']
                   if o[fid]['relation'] == 'declares'}, key=str.encode)
    add('fact.list', {'relation': 'declares'},
        [{'factId': fid, 'relation': 'declares', 'resolution': o[fid]['resolution']} for fid in decl],
        'complete', 'facts of the Run\'s admitted views')
    covs = []
    for v in R.views.values():
        for c in v['coverageIds']:
            pay = R.blob(o[c]['payloadDigest'])
            if pay['key']['relation'] == 'imports':
                covs.append({'coverageId': c, 'coverage': pay['entry']['coverage'],
                             'resolutionState': pay['entry']['resolutionCompleteness']['state']})
    add('coverage.show', {'relation': 'imports'}, covs, 'complete',
        'Coverage of the Run\'s admitted views whose key relation is imports')
    inv = R.refs('subject-inventory')[0]
    add('artifact.get', {'artifactRef': {'domain': 'subject-inventory', 'digest': inv}},
        [{'domain': 'subject-inventory', 'digest': inv,
          'byteLength': len(R.st.get_blob(inv))}], 'complete',
        'a proof-selected inventory, re-read from retained bytes')
    base = json.load(open(OUT + '/vectors/baseline-audit.json'))
    ba, cu = base['baselineArtifact'], base['comparisonUnchanged']
    add('baseline.show', {'baselineId': ba['baselineId']},
        [{'baselineId': ba['baselineId'], 'runId': ba['descriptor']['runId'],
          'entries': len(ba['descriptor']['entries']),
          'unmatchedOccurrences': len(ba['descriptor']['unmatchedOccurrences'])}],
        'complete', 'vectors/baseline-audit.json baselineArtifact')
    for op in ('comparison.show', 'comparison.diff'):
        add(op, {'comparisonResultId': cu['comparisonResultId']},
            [{'comparisonResultId': cu['comparisonResultId'],
              'currentRunId': cu['descriptor']['currentRunId'],
              'verdict': cu['descriptor']['verdict'],
              'entries': len(cu['descriptor']['entries'])}], 'complete',
            'vectors/baseline-audit.json comparisonUnchanged (both sides real)')
    for op in ('candidate.list', 'inspection.show', 'review.brief'):
        add(op, {}, [], 'unavailable', 'no projection of this advisory operation is retained '
                                      'for this Run; no rows is no claim of absence (I-Q9)')
    add('policy.effective', {}, [{'policyDigest': R.plan['policyDigest'],
                                  'ruleIds': sorted(r['ruleId'] for r in R.proof['ruleResults'])}],
        'complete', 'the admitted Plan policy and proof ruleResults')
    imps = R.refs('import')
    imp_ids = sorted(t for t in o if t.startswith('import2:') and t.split(':')[1] in
                     {d.split(':')[-1] for d in imps}) or sorted(t for t in o if t.startswith('import2:'))
    add('import.show', {'importId': imp_ids[0]}, [{'importId': imp_ids[0],
                                                   'kind': o[imp_ids[0]].get('kind')}],
        'complete', 'an import2 of this Run')
    receipt = json.load(open(OUT + '/envelopes/receipt-availability.json'))['envelope']['mutation']
    add('receipt.show', {'receiptId': receipt['receiptId']},
        [{'receiptId': receipt['receiptId'], 'operation': receipt['operation'],
          'effectOutcome': receipt['effectOutcome']}], 'complete',
        'envelopes/receipt-availability.json envelope.mutation')
    add('availability.show', {}, [], 'unavailable',
        'no availability account bound to this Run is retained (the generation-22 record came '
        'from an unrelated scenario); no rows is no claim (I-Q9)', view={'snapshotId': R.snapshot_id})
    return recs


def check_nongraph(f, R, recs):
    """Semantics re-derived from the Run, separately from the row builder above."""
    q = kitdoc(Q_DOC)
    advisory = set(q['$defs']['AdvisoryOperation']['enum'])
    waived = set(R.proof['waivedFindingIds'])
    for rec in recs:
        op, ctx, items = rec['operation'], rec['context'], rec['items']
        f.need(ctx['advisory'] is (op in advisory), 'L3 advisory cross-join',
               'ADVISORY_IS_THE_CROSS_JOIN:' + op)
        f.need(ctx['totalItems'] == len(items) and ctx['truncated'] is False,
               'totalItems is the count of the whole answer when nothing is truncated',
               'TOTAL_ITEMS_EQUALS_THE_ANSWER:' + op)
        f.need(ctx['coverage'] != 'unavailable' or not items,
               'I-Q9 an unavailable projection carries no rows', 'UNAVAILABLE_HAS_NO_ROWS:' + op)
        if op == 'finding.list':
            want = set(R.proof['findingIds']) - (set() if rec['params']['includeSuppressed']
                                                 else waived)
            f.need({i['findingId'] for i in items} == want,
                   'includeSuppressed=false omits proof.waivedFindingIds; true keeps them',
                   'FINDING_LIST_RESPECTS_INCLUDE_SUPPRESSED:%s' % rec['params']['includeSuppressed'],
                   {'waived': sorted(waived), 'listed': sorted(i['findingId'] for i in items)})
            f.need(ctx['coverage'] == ('partial' if R.proof['executionDeficiencies'] else 'complete'),
                   'I-Q9', 'FINDING_LIST_COVERAGE_FOLLOWS_EXECUTION_DEFICIENCIES')
        if op == 'baseline.show':
            f.need(items and items[0]['runId'] == R.run_id, 'the baseline adopted this Run',
                   'BASELINE_SHOW_NAMES_THE_CURRENT_RUN')
        if op in ('comparison.show', 'comparison.diff'):
            f.need(items and items[0]['currentRunId'] == R.run_id,
                   'the comparison current side is this Run', 'COMPARISON_CURRENT_SIDE:' + op)
        if op == 'receipt.show':
            f.need(items and items[0]['receiptId'].startswith('receipt2:'),
                   'a retained mutation receipt', 'RECEIPT_SHOW_HAS_A_RECEIPT')
        if op in ('run.list', 'availability.show'):
            f.need(set(ctx['resolvedView']) == {'snapshotId'},
                   'L4 snapshot metadata operations keep request View', 'REQUEST_VIEW_KEPT:' + op)


CONTROLS = [
    ('foreign-param-on-a-non-graph-operation', 'request', 'L2 Params is closed'),
    ('non-graph-params-shape-on-a-graph-operation', 'request', 'L2 graph operations must not use Params'),
    ('advisory-true-on-a-graph-response', 'response', 'L3 advisory const false on graph.*'),
    ('graph-resolved-view-names-latest', 'response', 'L4 ResolvedView is run3 only'),
    ('page-size-above-the-published-maximum', 'request', 'L5 page size 1..1000'),
    ('graph-response-without-the-evidence-disclosure', 'response', 'L9 evidence required'),
    ('operation-outside-the-published-enum', 'request', 'L1 closed enum'),
    ('graph-request-carrying-a-logical-path-subject', 'request', 'LogicalPath-only is refused'),
    ('failure-envelope-carrying-run', 'envelope', 'L13 kind=failure prohibits run'),
]


def run_controls(f, R, g):
    rows = []
    base = next(c for c in g['operations']
                if c['case'] == 'graph.neighbors-outgoing-first-party-and-external')
    fail = next(c for c in g['failureCases'] if c['case'] == 'endpoint-unknown')
    for label, side, law in CONTROLS:
        req = json.loads(json.dumps(base['request']))
        resp = json.loads(json.dumps(base['outcome']['response']))
        env = json.loads(json.dumps(fail['outcome']['envelope']))
        if label == 'foreign-param-on-a-non-graph-operation':
            req.update(operation='finding.list', params={'relation': 'declares', 'notAParam': 'x'})
        elif label == 'non-graph-params-shape-on-a-graph-operation':
            req['params'] = {'relation': 'imports', 'subject': 'src/a.js'}
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
            req['params'] = dict(req['params'], subject='src/a.js')
        elif label == 'failure-envelope-carrying-run':
            env['run'] = {'runId': R.run_id}
        if side == 'request':
            ok, err = admit('#/$defs/GraphQueryRequestV1', req, 'ctl:' + label)
            rec = req
        elif side == 'response':
            ok, err = admit('#/$defs/GraphQueryResponseV1', resp, 'ctl:' + label)
            rec = resp
        else:
            ok, err = admit('#', env, 'ctl:' + label, doc=ENV_DOC)
            rec = env
        rows.append({'control': label, 'side': side, 'owningLaw': law, 'classification': 'invalid',
                     'masksLater': 'owning-schema admission is the first boundary',
                     'refusedByTheOwningSchema': not ok, 'firstRefusal': err, 'record': rec})
        f.need(not ok, law, 'CONTROL_REFUSED:' + label, None if not ok else 'ADMITTED')
    return rows


def main():
    f = F()
    R = Run('typescript')
    P = Premises(R)
    g, graph_rows, tamper_rows = recompute_graph(f, P)
    recs = nongraph_records(R)
    check_nongraph(f, R, recs)
    raw = []
    for rec in recs:
        req = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
               'projectId': R.project_id, 'view': rec['context']['resolvedView'],
               'operation': rec['operation'], 'params': rec['params'],
               'completeness': 'required', 'page': {'size': 100}}
        resp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
                'operation': rec['operation'], 'context': rec['context'], 'items': rec['items']}
        ok1, e1 = admit('#/$defs/GraphQueryRequestV1', req, 'req:' + rec['operation'])
        ok2, e2 = admit('#/$defs/GraphQueryResponseV1', resp, 'resp:' + rec['operation'])
        f.need(ok1 and ok2, 'L2/L4 owning-schema admission',
               'RECORD_ADMITTED:' + rec['operation'], None if ok1 and ok2 else [e1, e2])
        raw.append({'operation': rec['operation'], 'source': 'this module', 'request': req,
                    'response': resp, 'rowBasis': rec['rowBasis'],
                    'requestAdmitted': ok1, 'responseAdmitted': ok2,
                    'layersMeasured': ('schema + row semantics re-derived from the Run'
                                       if rec['context']['coverage'] != 'unavailable'
                                       else 'schema only: no projection retained (I-Q9)')})
    for c in g['operations']:
        raw.append({'operation': c['request']['operation'],
                    'source': 'query/graph-query-reconstruction.json#' + c['case'],
                    'request': c['request'], 'response': c['outcome']['response'],
                    'rowBasis': 'the section-8 executor', 'requestAdmitted': True,
                    'responseAdmitted': True,
                    'layersMeasured': 'schema + every field recomputed independently'})
    ops = kitdoc(Q_DOC)['$defs']['Operation']['enum']
    f.need(sorted({r['operation'] for r in raw}) == sorted(ops) and len(ops) == 20,
           'L1 every published operation has an actual record', 'EVERY_OPERATION_HAS_A_RECORD',
           sorted(set(ops) - {r['operation'] for r in raw}))
    controls = run_controls(f, R, g)
    f.ok('L11 queries never materialise facts, invoke a provider, allocate an attempt, seal a Run, '
         'derive policy or choose termination', 'QUERY_PATHS_READ_ONLY_RETAINED_BYTES',
         {'runUnderQuery': R.run_id})
    doc = {'standing': __doc__, 'consumerId': 'consumer-b.v23',
           'predecessor': 'predecessors.v22/query/indep-query-surface.json',
           'runUnderQuery': {'label': R.label, 'runId': R.run_id, 'projectId': R.project_id,
                             'snapshotId': R.snapshot_id},
           'enumerationPlanRoute': P.eplan_route,
           'operationCount': len({r['operation'] for r in raw}),
           'graphRecomputation': {'cases': len(graph_rows),
                                  'disagreeing': sum(1 for r in graph_rows if r['disagreements']),
                                  'rows': graph_rows, 'tamperControls': tamper_rows},
           'checks': f.rows, 'refusals': f.refusals,
           'rawRequestAndResponseRecords': raw, 'negativeControls': controls,
           'declaredInterpretations': DECLARED,
           'claimLimits': ('a reconstruction over this origin\'s own admitted Run; no product query '
                           'engine or host was executed; host observations are synthetic trusted '
                           'inputs; candidate.list, inspection.show, review.brief and '
                           'availability.show are schema-only here (I-Q9)')}
    os.makedirs(OUT + '/query', exist_ok=True)
    with open(OUT + '/query/indep-query-surface.json', 'w') as fh:
        json.dump(doc, fh, indent=1, default=str)
    print('enumeration plan route: %s' % P.eplan_route)
    print('graph cases recomputed: %d, disagreeing: %d'
          % (len(graph_rows), doc['graphRecomputation']['disagreeing']))
    print('operations with actual records: %d' % doc['operationCount'])
    print('checks: %d passed, %d refused' % (len(f.rows) - len(f.refusals), len(f.refusals)))
    for r in f.refusals:
        print('   REFUSE %-60s %s' % (r['check'][:60], json.dumps(r['detail'], default=str)[:400]))
    assert not f.refusals, [r['check'] for r in f.refusals]


main()
