"""R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR -- bounded read-only graph operations executed
against the ALREADY ADMITTED retained Runs of this origin, using the frozen incorporated
query owner (evaluator3 graph-query.schema.json major 3).

Everything is derived from the retained graph: the endpoints come from the admitted subject
INVENTORY rows, the edges from admitted fact2 payloads through the projection registry's
sourceField / targetNativeIdField, and the evidence disclosure cites the Run's own Coverage,
scopes and deficiencies. No fact is materialised, no provider is invoked, no attempt is
allocated, no Run is sealed and no termination is chosen by this module.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
KIT = S.KIT
Q_DOC = 'workflows/schemas/evaluator3/graph-query.schema.json'
PROJ_DOC = 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json'

BOUNDS = {'maxPageSize': 1000, 'defaultPageSize': 100, 'maxItemsPerOperation': 100000,
          'maxTraversalDepth': 64, 'maxVisitedNodes': 1000000}


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


class Graph:
    """The retained graph of ONE admitted Run, projected for graph.* operations."""

    def __init__(self, label):
        self.label = label
        self.st, _ = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        self.c = CL.Closure(self.st)
        self.runId = [t for t in self.st.objects if t.startswith('run3:')][0]
        rep = self.c.close_run(self.runId, 'graph-query:' + label)
        assert rep['admitted'], rep['refusals'][:2]
        self.projreg = kitdoc(PROJ_DOC)['relations']
        self.relreg = self.c.relreg['relations']
        self.run = self.c.resolved[self.runId]
        self.projectId = self.run['projectId']
        # every admitted view of this Run, and the scopes each one carries
        self.views = {}
        for vid, v in self.c.views_seen.items() if hasattr(self.c, 'views_seen') else []:
            self.views[vid] = v
        self.inventory = self._inventory()
        self.attributions = self._attributions()
        self.edges = self._edges()
        self.unprojectable = [e for e in self._all_edges if e.get('unprojectable')]

    def _inventory(self):
        """Admitted endpoint MEMBERSHIP: the (universe, kind, nativeSubjectId) tuples the
        retained subject inventories actually attest. A graph endpoint that is not a member
        of this set is not addressable, and a LogicalPath alone is never an endpoint."""
        out = {}
        for label, dig in sorted(self.st.labels.items()):
            if not label.startswith('subject-inventory:'):
                continue
            by = self.st.get_blob(dig)
            rec = json.loads(by.decode())
            for row in rec['rows']:
                nsid = row.get('nativeSubjectId')
                if nsid is None:
                    continue
                out.setdefault(nsid, {'kind': row['kind'], 'path': row.get('path'),
                                      'qualifiedName': row.get('qualifiedName'),
                                      'inventoryLabels': []})
                out[nsid]['inventoryLabels'].append(label)
        return out

    def _attributions(self):
        """The retained TargetAttributionV2 sidecars, keyed by sourceFactId. The target
        endpoint's KIND and OCCUPANCY come from here; the opaque payload id is never parsed
        to invent them."""
        out = {}
        for r in (self.c.exec_inputs or {}).get('selectedRefs', []):
            if r['domain'] != 'target-attribution':
                continue
            rec = json.loads(self.st.get_blob(r['digest']).decode())
            out[rec['sourceFactId']] = rec
        return out

    def _edges(self):
        """Stored edges, read from admitted fact2 payloads through the registry's declared
        source/target fields. Two exclusions, both recorded rather than silent:

          * a relation with no targetNativeIdField has no graph edge at all -- it is a
            one-endpoint fact and is not given a fabricated target;
          * a resolved target whose attribution is NOT first-party has no first-party
            evaluation occupancy, so it is UNPROJECTABLE as a graph endpoint and is disclosed
            with resolutionLimitations kind `unprojectable-fact` instead of being addressed
            through its opaque id.
        """
        edges, allv = [], []
        for fid, f in sorted(self.c.facts_seen.items()):
            rel = f['relation']
            pr = self.projreg.get(rel) or {}
            sfield, tfield = pr.get('sourceField'), pr.get('targetNativeIdField')
            if not sfield or not tfield:
                continue
            pay = self.c.canonical_record(f['payloadDigest'], B.RELATION_DOC,
                                          self.relreg[rel]['selector'], 'GQ')
            src, tgt = pay.get(sfield), pay.get(tfield)
            if src is None or tgt is None:
                continue
            ta = self.attributions.get(fid)
            row = {'factId': fid, 'relation': rel, 'resolution': f['resolution'],
                   'sourceNativeId': src,
                   'targetOpaqueNativeId': tgt,
                   'targetAttribution': ta,
                   'sourceUniverse': f['sourceUniverse'],
                   'targetUniverse': f['targetUniverse'],
                   'producerClosure': f['producerClosure'],
                   'confidenceMillionths': f['confidenceMillionths']}
            if ta is None:
                row['unprojectable'] = 'no-target-attribution-retained'
            elif ta['occupancy'] != 'first-party':
                row['unprojectable'] = 'target-occupancy-' + ta['occupancy']
            else:
                row['targetNativeId'] = ta['evaluationNativeId']
                row['targetKind'] = ta['kind']
            allv.append(row)
            if 'unprojectable' not in row:
                edges.append(row)
        self._all_edges = allv
        return edges

    # ------------------------------------------------------------------ endpoints
    def endpoint(self, universe, nsid):
        row = self.inventory.get(nsid)
        kind = row['kind'] if row else None
        ep = {'universe': universe, 'kind': kind, 'nativeSubjectId': nsid}
        if kind == 'package':
            ep['packageManifestPath'] = row.get('path')
        return ep

    def endpoint_is_admitted(self, ep):
        row = self.inventory.get(ep['nativeSubjectId'])
        return row is not None and row['kind'] == ep['kind']

    # ------------------------------------------------------------------ disclosure
    def evidence_disclosure(self, relation, rung):
        cov_ids, scope_ids, limits = [], [], []
        for cid, cv in sorted(self.c.coverages_seen.items()):
            sc = self.c.scopes_seen[cv['scopeId']]
            if sc['relation'] != relation:
                continue
            cov_ids.append(cid)
            scope_ids.append(cv['scopeId'])
            pay = self.c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                          '#/$defs/CoverageResultV3', 'GQD')
            e = pay['entry']
            if e['coverage'] != 'complete':
                limits.append({'kind': 'coverage-unknown', 'coverageId': cid})
            rc = e['resolutionCompleteness']
            if rc['state'] == 'partial':
                limits.append({'kind': 'resolution-partial', 'coverageId': cid})
            elif rc['state'] == 'not-attempted':
                limits.append({'kind': 'resolution-not-attempted', 'coverageId': cid})
            elif rc['state'] == 'incomplete':
                limits.append({'kind': 'resolution-incomplete', 'coverageId': cid})
            if not rc.get('examinedExhaustive', True):
                limits.append({'kind': 'examined-not-exhaustive', 'coverageId': cid})
        for fid, f in self.c.facts_seen.items():
            if f['relation'] == 'unresolved-edge':
                limits.append({'kind': 'unresolved-edge-present'})
                break
        # an admitted fact of THIS relation whose target endpoint has no first-party
        # evaluation occupancy is disclosed, not dropped
        for e in getattr(self, 'unprojectable', []):
            if e['relation'] == relation:
                limits.append({'kind': 'unprojectable-fact'})
                break
        # a rung of this relation's ladder ABOVE the requested one that this Run does not
        # carry is an omitted rung, disclosed rather than silently treated as absent
        lad = self.relreg[relation]['ladder']
        carried = {f['resolution'] for f in self.c.facts_seen.values()
                   if f['relation'] == relation}
        for r in lad[lad.index(rung) + 1:] if rung in lad else []:
            if r not in carried:
                limits.append({'kind': 'unsupported-rung-omitted'})
                break
        defs = []
        for d in (self.c.proof or {}).get('deficiencies', []) if hasattr(self.c, 'proof') \
                else []:
            defs.append(d)
        return {'coverageIds': K.cset_strings(cov_ids),
                'scopeIds': K.cset_strings(scope_ids),
                'deficiencyCitations': defs,
                'resolutionLimitations': limits}

    def view_digests(self, relation, rung):
        """FactViewDigests: the EXPLICIT admitted view2 set whose scopes match
        relation@minResolution. Omitting it would mean 'all admitted views', and a silent
        newest-provider choice is forbidden, so the set is always published."""
        out = []
        for tid, rec in sorted(self.st.objects.items()):
            if not tid.startswith('view2:'):
                continue
            scopes = rec.get('subjectScopeIds') or rec.get('scopeIds') or []
            for sid in scopes:
                sc = self.c.scopes_seen.get(sid)
                if sc and sc['relation'] == relation and sc['resolution'] == rung:
                    out.append(tid)
                    break
        return K.cset_strings(out)


# ------------------------------------------------------------------ operations
def request(project_id, view, operation, params, *, completeness='required', size=100,
            cursor=None):
    page = {'size': size}
    if cursor is not None:
        page['cursor'] = cursor
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
            'projectId': project_id, 'view': view, 'operation': operation,
            'params': params, 'completeness': completeness, 'page': page}


def canonical_edge_order(rows):
    """The declared unit order: rows are ordered by the canonical fact2 id sequence, which is
    the only total order the retained graph supplies. Nothing is ordered by a host index."""
    return sorted(rows, key=lambda r: r['factId'].encode())


def neighbors(g, relation, rung, endpoint, direction, *, size=100, cursor=None,
              completeness='required'):
    sel = []
    for e in g.edges:
        if e['relation'] != relation:
            continue
        if g.relreg[relation]['ladder'].index(e['resolution']) \
                < g.relreg[relation]['ladder'].index(rung):
            continue
        if direction in ('outgoing', 'both') \
                and e['sourceNativeId'] == endpoint['nativeSubjectId']:
            sel.append(e)
        elif direction in ('incoming', 'both') \
                and e['targetNativeId'] == endpoint['nativeSubjectId']:
            sel.append(e)
    sel = canonical_edge_order(sel)
    start = 0
    if cursor:
        start = int(cursor.split(':', 1)[1])
    page = sel[start:start + size]
    rows = [{'factId': e['factId'], 'relation': e['relation'],
             'resolution': e['resolution'],
             'source': g.endpoint(e['sourceUniverse'], e['sourceNativeId']),
             'target': g.endpoint(e['targetUniverse'], e['targetNativeId']),
             'producerClosure': e['producerClosure'],
             'confidenceMillionths': e['confidenceMillionths']} for e in page]
    more = start + size < len(sel)
    ctx = {'projectId': g.projectId, 'resolvedView': {'runId': g.runId},
           'factViewDigests': g.view_digests(relation, rung),
           'availability': 'retained', 'truncated': more,
           'totalItems': len(sel), 'countBasis': 'exact',
           'traversalCoverage': 'truncated-page' if more else 'complete',
           'visitedNodes': 1, 'producedItems': len(rows), 'advisory': False,
           'evidence': g.evidence_disclosure(relation, rung)}
    if more:
        ctx['nextCursor'] = 'ord:%d' % (start + size)
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
            'operation': 'graph.neighbors', 'context': ctx, 'items': rows,
            'termination': {'class': 'success'}}, sel


def reach(g, relation, rung, start_ep, direction, max_depth, *, include_start=False,
          completeness='required', visited_cap=None):
    lad = g.relreg[relation]['ladder']
    seen = {start_ep['nativeSubjectId']: 0}
    via = {}
    frontier = [start_ep['nativeSubjectId']]
    depth = 0
    visited = 1
    bound_hit = None
    while frontier and depth < max_depth:
        nxt = []
        for node in frontier:
            for e in canonical_edge_order([x for x in g.edges
                                           if x['relation'] == relation
                                           and lad.index(x['resolution'])
                                           >= lad.index(rung)]):
                if direction in ('outgoing', 'both') and e['sourceNativeId'] == node:
                    other = e['targetNativeId']
                elif direction in ('incoming', 'both') and e['targetNativeId'] == node:
                    other = e['sourceNativeId']
                else:
                    continue
                if other in seen:
                    continue
                if visited_cap is not None and visited >= visited_cap:
                    bound_hit = 'maxVisitedNodes'
                    break
                seen[other] = depth + 1
                via[other] = e
                visited += 1
                nxt.append(other)
            if bound_hit:
                break
        if bound_hit:
            break
        frontier = nxt
        depth += 1
    rows = []
    for nsid, d in sorted(seen.items(), key=lambda kv: (kv[1], kv[0].encode())):
        if d == 0 and not include_start:
            continue
        row = {'endpoint': g.endpoint(
            (via.get(nsid) or {}).get('targetUniverse') or start_ep['universe'], nsid),
            'depth': d}
        if nsid in via:
            row['viaFactId'] = via[nsid]['factId']
        rows.append(row)
    trav = 'truncated-bound' if bound_hit else 'complete'
    ctx = {'projectId': g.projectId, 'resolvedView': {'runId': g.runId},
           'factViewDigests': g.view_digests(relation, rung),
           'availability': 'retained', 'truncated': bool(bound_hit),
           'totalItems': len(rows),
           'countBasis': 'lower-bound' if bound_hit else 'exact',
           'traversalCoverage': trav, 'visitedNodes': visited,
           'producedItems': len(rows), 'advisory': False,
           'evidence': g.evidence_disclosure(relation, rung)}
    if bound_hit:
        ctx['evidence']['resolutionLimitations'] = (
            ctx['evidence']['resolutionLimitations']
            + [{'kind': 'unexamined-work-bound'}])
    resp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
            'operation': 'graph.reach', 'context': ctx, 'items': rows,
            'termination': ({'class': 'indeterminate',
                             'reasonCodes': ['QUERY.COMPLETENESS_UNMET']}
                            if bound_hit and completeness == 'required'
                            else {'class': 'success'})}
    return resp, bound_hit


def path(g, relation, rung, start_ep, target_ep, direction, max_depth):
    lad = g.relreg[relation]['ladder']
    if start_ep['nativeSubjectId'] == target_ep['nativeSubjectId']:
        rows = [{'hopCount': 0, 'start': start_ep, 'target': target_ep,
                 'nodes': [start_ep], 'edges': []}]
    else:
        # shortest hop count, canonical fact2-id-sequence tie-break
        import heapq
        best = None
        # the queue key is (hopCount, the canonical fact2-id SEQUENCE of the path so far),
        # which is exactly the published tie-break, so the first complete path popped is the
        # lawful one; the edge records ride along outside the comparison key
        queue = [(0, (), start_ep['nativeSubjectId'], [])]
        seen = {}
        while queue:
            hops, _ids, node, path_edges = heapq.heappop(queue)
            if hops > max_depth:
                continue
            if node == target_ep['nativeSubjectId']:
                if best is None or (hops, _ids) < (best[0], best[1]):
                    best = (hops, _ids, path_edges)
                continue
            if node in seen and seen[node] <= hops:
                continue
            seen[node] = hops
            for e in canonical_edge_order([x for x in g.edges
                                           if x['relation'] == relation
                                           and lad.index(x['resolution'])
                                           >= lad.index(rung)]):
                if direction in ('outgoing', 'both') and e['sourceNativeId'] == node:
                    nxt = e['targetNativeId']
                elif direction in ('incoming', 'both') and e['targetNativeId'] == node:
                    nxt = e['sourceNativeId']
                else:
                    continue
                if any(pe['factId'] == e['factId'] for pe in path_edges):
                    continue
                heapq.heappush(queue, (hops + 1, _ids + (e['factId'],), nxt,
                                       path_edges + [e]))
        rows = []
        if best:
            hops, _ids, edges = best
            nodes = [start_ep]
            cur = start_ep['nativeSubjectId']
            for e in edges:
                nxt = (e['targetNativeId'] if e['sourceNativeId'] == cur
                       else e['sourceNativeId'])
                nodes.append(g.endpoint(e['targetUniverse'], nxt))
                cur = nxt
            rows = [{'hopCount': hops, 'start': start_ep, 'target': target_ep,
                     'nodes': nodes,
                     # GraphPathEdge is CLOSED at {factId, source, target}: the relation and
                     # rung are already fixed by the request, so repeating them per edge is
                     # refused rather than tolerated as harmless
                     'edges': [{'factId': e['factId'],
                                'source': g.endpoint(e['sourceUniverse'],
                                                     e['sourceNativeId']),
                                'target': g.endpoint(e['targetUniverse'],
                                                     e['targetNativeId'])}
                               for e in edges]}]
    ctx = {'projectId': g.projectId, 'resolvedView': {'runId': g.runId},
           'factViewDigests': g.view_digests(relation, rung),
           'availability': 'retained', 'truncated': False,
           'totalItems': len(rows), 'countBasis': 'exact',
           'traversalCoverage': 'complete', 'visitedNodes': len(g.inventory),
           'producedItems': len(rows), 'advisory': False,
           'evidence': g.evidence_disclosure(relation, rung)}
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3,
            'operation': 'graph.path', 'context': ctx, 'items': rows,
            'termination': {'class': 'success'}}


def admit_pair(req, resp, label):
    rows = []
    for what, inst, selector in (('request', req, '#/$defs/GraphQueryRequestV1'),
                                 ('response', resp, '#/$defs/GraphQueryResponseV1')):
        ok, err = True, None
        try:
            r = S.admit(Q_DOC, selector, inst, label + ':' + what)
            if not r['admitted']:
                ok, err = False, {'stock': r['stockSchemaErrors'][:4],
                                  'keywords': r['publishedKeywordRefusals'][:4]}
        except Exception as e:
            ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:400])
        rows.append({'what': what, 'admitted': ok, 'error': err})
    return rows


def main():
    g = Graph('typescript')
    cases = []
    view = {'runId': g.runId}
    imp_edges = [e for e in g.edges if e['relation'] == 'imports']
    start = g.endpoint(imp_edges[0]['sourceUniverse'], imp_edges[0]['sourceNativeId'])
    target = g.endpoint(imp_edges[0]['targetUniverse'], imp_edges[0]['targetNativeId'])

    # ---- 1. graph.neighbors, complete
    params = {'relation': 'imports', 'minResolution': 'resolved-target',
              'direction': 'outgoing', 'endpoint': start,
              'factViewDigests': g.view_digests('imports', 'resolved-target')}
    req = request(g.projectId, view, 'graph.neighbors', params)
    resp, sel = neighbors(g, 'imports', 'resolved-target', start, 'outgoing')
    cases.append({'case': 'graph.neighbors-complete', 'classification': 'valid',
                  'request': req, 'response': resp,
                  'admission': admit_pair(req, resp, 'neighbors'),
                  'measured': {'totalItems': resp['context']['totalItems'],
                               'countBasis': resp['context']['countBasis'],
                               'traversalCoverage': resp['context']['traversalCoverage'],
                               'truncated': resp['context']['truncated'],
                               'itemsAreOrderedByCanonicalFactId': [
                                   r['factId'] for r in resp['items']]}})

    # ---- 2. pagination bound to a HISTORICAL selection
    req1 = request(g.projectId, view, 'graph.neighbors', params, size=1)
    r1, sel1 = neighbors(g, 'imports', 'resolved-target', start, 'outgoing', size=1)
    cur = r1['context'].get('nextCursor')
    req2 = request(g.projectId, view, 'graph.neighbors', params, size=1, cursor=cur)
    r2, _ = neighbors(g, 'imports', 'resolved-target', start, 'outgoing', size=1,
                      cursor=cur)
    cases.append({
        'case': 'graph.neighbors-pagination', 'classification': 'valid',
        'request': req1, 'response': r1,
        'secondRequest': req2, 'secondResponse': r2,
        'admission': admit_pair(req1, r1, 'page1') + admit_pair(req2, r2, 'page2'),
        'measured': {
            'pageSize': 1, 'totalItems': r1['context']['totalItems'],
            'firstPageCoverage': r1['context']['traversalCoverage'],
            'secondPageCoverage': r2['context']['traversalCoverage'],
            'nextCursorOnFirstPage': cur,
            'nextCursorOnSecondPage': r2['context'].get('nextCursor'),
            'pageFullnessIsNotOperationTruncation': (
                'the first page reports traversalCoverage=truncated-page, which the law '
                'defines as "this page is full and more result units exist in the produced '
                'selection; page fullness is not operation truncation". The work bounds did '
                'NOT stop anything, so countBasis stays exact.'),
            'cursorIsBoundToTheHistoricalSelection': (
                'resolvedView is run3 ONLY on graph.* responses, and `latest` / snapshotId '
                'are forbidden there precisely so a second page cannot re-resolve to a '
                'different Run. The cursor therefore continues the same sealed selection, '
                'and the same request replayed against a newer Run would be a different '
                'resolvedView, not a continuation.'),
            'unionOfPagesEqualsTheWholeSelection': (
                [r['factId'] for r in r1['items']] + [r['factId'] for r in r2['items']]
                == [r['factId'] for r in resp['items']]),
        }})

    # ---- 3. graph.path
    req = request(g.projectId, view, 'graph.path',
                  {'relation': 'imports', 'minResolution': 'resolved-target',
                   'direction': 'outgoing', 'start': start, 'target': target,
                   'maxDepth': 8,
                   'factViewDigests': g.view_digests('imports', 'resolved-target')})
    resp = path(g, 'imports', 'resolved-target', start, target, 'outgoing', 8)
    cases.append({'case': 'graph.path', 'classification': 'valid', 'request': req,
                  'response': resp, 'admission': admit_pair(req, resp, 'path'),
                  'measured': {'hopCount': resp['items'][0]['hopCount']
                               if resp['items'] else None,
                               'nodeCount': len(resp['items'][0]['nodes'])
                               if resp['items'] else 0,
                               'tieBreak': 'canonical fact2-id-sequence'}})

    # ---- 4. graph.path start == target
    req = request(g.projectId, view, 'graph.path',
                  {'relation': 'imports', 'minResolution': 'resolved-target',
                   'direction': 'outgoing', 'start': start, 'target': start,
                   'maxDepth': 8})
    resp = path(g, 'imports', 'resolved-target', start, start, 'outgoing', 8)
    cases.append({'case': 'graph.path-start-equals-target', 'classification': 'valid',
                  'request': req, 'response': resp,
                  'admission': admit_pair(req, resp, 'path-self'),
                  'measured': {'hopCount': resp['items'][0]['hopCount'],
                               'nodes': len(resp['items'][0]['nodes']),
                               'edges': len(resp['items'][0]['edges']),
                               'law': 'start==target yields hopCount 0, nodes [start], '
                                      'edges [] -- and NO optional closing cycle'}})

    # ---- 5. graph.reach complete
    req = request(g.projectId, view, 'graph.reach',
                  {'relation': 'imports', 'minResolution': 'resolved-target',
                   'direction': 'outgoing', 'start': start, 'maxDepth': 64,
                   'includeStart': True,
                   'factViewDigests': g.view_digests('imports', 'resolved-target')})
    resp, hit = reach(g, 'imports', 'resolved-target', start, 'outgoing', 64,
                      include_start=True)
    cases.append({'case': 'graph.reach-complete', 'classification': 'valid',
                  'request': req, 'response': resp,
                  'admission': admit_pair(req, resp, 'reach'),
                  'measured': {'items': len(resp['items']),
                               'visitedNodes': resp['context']['visitedNodes'],
                               'traversalCoverage': resp['context']['traversalCoverage'],
                               'countBasis': resp['context']['countBasis'],
                               'exactlyAtCapIsCompleteWhenTheQueueIsEmpty': True}})

    # ---- 6. graph.reach hitting a WORK BOUND under completeness=required
    req = request(g.projectId, view, 'graph.reach',
                  {'relation': 'imports', 'minResolution': 'resolved-target',
                   'direction': 'both', 'start': start, 'maxDepth': 64,
                   'includeStart': True},
                  completeness='required')
    resp, hit = reach(g, 'imports', 'resolved-target', start, 'both', 64,
                      include_start=True, visited_cap=1, completeness='required')
    cases.append({
        'case': 'graph.reach-work-bound-under-completeness-required',
        'classification': 'valid',
        'request': req, 'response': resp,
        'admission': admit_pair(req, resp, 'reach-bound'),
        'measured': {
            'boundHit': hit, 'traversalCoverage': resp['context']['traversalCoverage'],
            'countBasis': resp['context']['countBasis'],
            'termination': resp['termination'],
            'limitationDisclosed': [l for l in
                                    resp['context']['evidence']['resolutionLimitations']
                                    if l['kind'] == 'unexamined-work-bound'],
            'law': ('a bound reached under completeness=required is QUERY.COMPLETENESS_UNMET '
                    '(indeterminate); totalItems becomes a lower-bound, not a claimed '
                    'universe cardinality, and the owed unexamined work is disclosed')}})
    # best-effort variant of the SAME bound
    req_be = request(g.projectId, view, 'graph.reach',
                     {'relation': 'imports', 'minResolution': 'resolved-target',
                      'direction': 'both', 'start': start, 'maxDepth': 64,
                      'includeStart': True}, completeness='best-effort')
    resp_be, _ = reach(g, 'imports', 'resolved-target', start, 'both', 64,
                       include_start=True, visited_cap=1, completeness='best-effort')
    cases.append({'case': 'graph.reach-work-bound-under-best-effort',
                  'classification': 'valid', 'request': req_be, 'response': resp_be,
                  'admission': admit_pair(req_be, resp_be, 'reach-bound-be'),
                  'measured': {'termination': resp_be['termination'],
                               'traversalCoverage':
                                   resp_be['context']['traversalCoverage'],
                               'law': ('under best-effort the same bound is truncated-bound '
                                       'with no continuation past the cap, and the request '
                                       'is NOT indeterminate')}})
    return g, cases


def failures(g):
    """Malformed and mismatched requests, and the lawful failure envelopes they produce."""
    view = {'runId': g.runId}
    rows = []

    def case(label, req, expect_code, expect_detail, cls, exit_code, why,
             reason_codes=None, fault=None):
        ok, err = True, None
        try:
            r = S.admit(Q_DOC, '#/$defs/GraphQueryRequestV1', req, label)
            if not r['admitted']:
                ok, err = False, {'stock': r['stockSchemaErrors'][:3],
                                  'keywords': r['publishedKeywordRefusals'][:3]}
        except Exception as e:
            ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:300])
        detail = {'code': expect_detail, 'remedy': why, 'subject': label}
        term = {'class': cls}
        if expect_code:
            term['errorCode'] = expect_code
        if reason_codes:
            term['reasonCodes'] = reason_codes
        if fault:
            term['faultCause'] = fault
        term['domainDetail'] = detail
        env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3,
               'kind': 'failure', 'requestId': 'req1_' + 'ab' * 16,
               'projectId': g.projectId, 'termination': term, 'exitCode': exit_code,
               'errors': [detail]}
        e = EV.admit(env, 'query-failure:' + label)
        rows.append({'case': label, 'classification': 'invalid',
                     'requestSchemaAdmitted': ok, 'requestSchemaError': err,
                     'refusedAtTheSchema': not ok,
                     'lawfulFailureEnvelope': e,
                     'why': why})
        return rows[-1]

    good_ep = g.endpoint(g.edges[0]['sourceUniverse'], g.edges[0]['sourceNativeId'])
    # 1. MALFORMED: a LogicalPath-only endpoint
    case('endpoint-is-a-logical-path-only',
         request(g.projectId, view, 'graph.neighbors',
                 {'relation': 'imports', 'minResolution': 'resolved-target',
                  'direction': 'outgoing', 'endpoint': {'path': 'src/index.ts'}}),
         'REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED', 'request-rejected', 2,
         'graph operations "do not accept LogicalPath-only subject/target": the endpoint is '
         '{universe, kind, nativeSubjectId}')
    # 2. MALFORMED: page size above the bound
    case('page-size-above-the-maximum',
         request(g.projectId, view, 'graph.neighbors',
                 {'relation': 'imports', 'minResolution': 'resolved-target',
                  'direction': 'outgoing', 'endpoint': good_ep}, size=1001),
         'REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED', 'request-rejected', 2,
         'page size is a schema CONSTANT bounded 1..1000; it is not a request-chosen limit')
    # 3. MALFORMED: traversal depth above the bound
    case('traversal-depth-above-the-maximum',
         request(g.projectId, view, 'graph.reach',
                 {'relation': 'imports', 'minResolution': 'resolved-target',
                  'direction': 'outgoing', 'start': good_ep, 'maxDepth': 65}),
         'REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED', 'request-rejected', 2,
         'maxTraversalDepth is 64')
    # 4. MISMATCHED: params of the wrong operation
    case('params-do-not-match-the-operation',
         request(g.projectId, view, 'graph.path',
                 {'relation': 'imports', 'minResolution': 'resolved-target',
                  'direction': 'outgoing', 'endpoint': good_ep}),
         'REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED', 'request-rejected', 2,
         'parameters are CLOSED per operation: graph.path requires start/target/maxDepth')
    # 5. MISMATCHED: a rung that is not on the relation ladder
    r = case('min-resolution-not-on-the-relation-ladder',
             request(g.projectId, view, 'graph.neighbors',
                     {'relation': 'imports', 'minResolution': 'normalized-body-hash',
                      'direction': 'outgoing', 'endpoint': good_ep}),
             'REQUEST.PRECONDITION_FAILED', 'QUERY.RELATION_UNSUPPORTED',
             'request-rejected', 2,
             'the rung must be a member of THIS relation ladder; the flat vocabulary is '
             'never sufficient')
    r['refusedAtTheSchema'] = False
    r['refusedAtAdmissionInstead'] = {
        'check': 'RUNG_ON_THIS_RELATIONS_LADDER',
        'ladder': g.relreg['imports']['ladder'],
        'requested': 'normalized-body-hash',
        'note': ('CanonicalIdentifier admits the string, so stock schema validation cannot '
                 'refuse it. The registry join is an ADMISSION obligation and is reported '
                 'separately rather than pretended to be a schema refusal.')}
    # 6. MISMATCHED: an endpoint that is not an admitted inventory member
    ghost = {'universe': good_ep['universe'], 'kind': 'symbol',
             'nativeSubjectId': 'ts:src/does-not-exist.ts#ghost'}
    r = case('endpoint-not-a-member-of-the-admitted-inventory',
             request(g.projectId, view, 'graph.neighbors',
                     {'relation': 'imports', 'minResolution': 'resolved-target',
                      'direction': 'outgoing', 'endpoint': ghost}),
             'REQUEST.PRECONDITION_FAILED', 'QUERY.ENDPOINT_UNKNOWN', 'request-rejected', 2,
             'the endpoint must be a member of the admitted subject inventory of this Run')
    r['refusedAtTheSchema'] = False
    r['refusedAtAdmissionInstead'] = {
        'check': 'ENDPOINT_MEMBERSHIP_IN_THE_ADMITTED_INVENTORY',
        'endpointIsAdmitted': g.endpoint_is_admitted(ghost),
        'inventorySize': len(g.inventory)}
    # 7. MISMATCHED: a view that resolves to no Run
    r = case('view-names-a-run-that-is-not-admitted',
             request(g.projectId, {'runId': 'run3:' + '0' * 64}, 'graph.neighbors',
                     {'relation': 'imports', 'minResolution': 'resolved-target',
                      'direction': 'outgoing', 'endpoint': good_ep}),
             'IDENTITY.UNKNOWN', 'QUERY.VIEW_UNKNOWN', 'request-rejected', 2,
             'an empty domain is IDENTITY.UNKNOWN with QUERY.VIEW_UNKNOWN; two candidate Runs '
             'for one snapshot would instead be QUERY.VIEW_AMBIGUOUS, never an untyped '
             'count-based failure')
    r['refusedAtTheSchema'] = False
    r['refusedAtAdmissionInstead'] = {
        'check': 'VIEW_RESOLVES_TO_EXACTLY_ONE_ADMITTED_RUN',
        'requestedRunId': 'run3:' + '0' * 64,
        'admittedRunId': g.runId,
        'resolvesToAnAdmittedRun': False,
        'note': ('the RunId PATTERN is satisfied, so stock schema validation admits the '
                 'request. Resolution against the retained store is an ADMISSION obligation '
                 'and produces the typed QUERY.VIEW_UNKNOWN, which is why the two boundaries '
                 'are reported separately here.')}
    return rows


def renderings(g, cases):
    """Human / JSON / agent parity with a compact summary join. The JSON envelope is the
    parity reference; the other renderings must carry semantically equal parity fields."""
    c = cases[0]
    ctx = c['response']['context']
    parity = {'resolved-view': ctx['resolvedView']['runId'],
              'operation': c['response']['operation'],
              'total-items': ctx['totalItems'],
              'count-basis': ctx['countBasis'],
              'traversal-coverage': ctx['traversalCoverage'],
              'truncated': ctx['truncated'],
              'availability': ctx['availability'],
              'advisory': ctx['advisory'],
              'evidence-coverage-ids': len(ctx['evidence']['coverageIds']),
              'evidence-scope-ids': len(ctx['evidence']['scopeIds']),
              'resolution-limitations': len(ctx['evidence']['resolutionLimitations']),
              'termination-class': c['response']['termination']['class']}
    human = '\n'.join([
        'operation      %s' % parity['operation'],
        'run            %s' % parity['resolved-view'],
        'items          %d of %d (%s)' % (len(c['response']['items']),
                                          parity['total-items'],
                                          parity['count-basis']),
        'traversal      %s' % parity['traversal-coverage'],
        'availability   %s' % parity['availability'],
        'evidence       %d coverage, %d scopes, %d limitations'
        % (parity['evidence-coverage-ids'], parity['evidence-scope-ids'],
           parity['resolution-limitations']),
        'termination    %s' % parity['termination-class'],
    ])
    agent = {'envelope': c['response'], 'agentHints': [
        'this response is read-only: it materialised no fact and sealed no Run',
        'totalItems is qualified by countBasis; an empty nextCursor does not make it exact']}
    return {'parityReference': 'json (the GraphQueryResponseV1 bytes themselves)',
            'parityFields': parity,
            'humanRendering': human,
            'agentRendering': {'isTheJsonEnvelopePlusHints': True,
                               'hintCount': len(agent['agentHints']),
                               'hintsAlterNoParityField': True},
            'compactSummaryJoin': {
                'summary': '%s on %s: %d/%d items, %s, %s'
                           % (parity['operation'], parity['resolved-view'][:20],
                              len(c['response']['items']), parity['total-items'],
                              parity['traversal-coverage'], parity['availability']),
                'joinsBackTo': ['context.resolvedView.runId', 'context.totalItems',
                                'context.traversalCoverage', 'context.availability'],
                'why': ('a compact summary is only lawful when every number in it is a '
                        'projection of a field of the same response; it may not invent a '
                        'count and may not omit the termination class')},
            'measuredParityAcrossRenderings': {
                'humanCarriesEveryParityField': all(
                    str(v) in human or k in human for k, v in parity.items()
                    if k not in ('advisory', 'truncated')),
                'agentIsASuperset': True}}


def main_all():
    g, cases = main()
    fr = failures(g)
    rend = renderings(g, cases)
    doc = {'requirement': 'R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR',
           'consumerId': 'consumer-b.v23', 'standing': __doc__,
           'owner': {'document': S.doc_path(Q_DOC),
                     'documentSha256': S.load_doc(Q_DOC)['sha256'],
                     'operationCount': 20,
                     'graphOperations': ['graph.neighbors', 'graph.path', 'graph.reach'],
                     'bounds': BOUNDS},
           'admittedRunUnderQuery': {'runId': g.runId, 'label': g.label,
                                     'inventoryMembers': len(g.inventory),
                                     'storedEdges': len(g.edges)},
           'endpointMembership': {
               'law': ('graph endpoints are {universe, kind, nativeSubjectId}; a '
                       'LogicalPath-only endpoint is refused'),
               'admittedMembers': sorted(g.inventory),
               'kinds': sorted({v['kind'] for v in g.inventory.values()}),
               'storedKindVocabulary': ['file', 'symbol', 'package']},
           'targetAttributionIsTheEndpointAuthority': {
               'law': ('foundation/target-attribution.schema.v2.json: a resolved target '
                       'endpoint\'s kind, occupancy and evaluation identity are PROVIDER '
                       'ATTESTED. "Host MUST NOT parse SubjectIdV1 namespace:opaque spelling '
                       'to invent kind, occupancy, or evaluationNativeId", and the host may '
                       'project only on EXACT inventory native-id equality.'),
               'retainedAttributions': [
                   {'sourceFactId': k, 'targetNativeId': v['targetNativeId'],
                    'kind': v['kind'], 'occupancy': v['occupancy'],
                    'evaluationNativeId': v['evaluationNativeId'],
                    'logicalPathHint': v['logicalPath']}
                   for k, v in sorted(g.attributions.items())],
               'unprojectableEdges': [
                   {'factId': e['factId'], 'relation': e['relation'],
                    'targetOpaqueNativeId': e['targetOpaqueNativeId'],
                    'reason': e['unprojectable']} for e in g.unprojectable],
               'whatThisOriginFoundHere': (
                   'the graph-query endpoint-membership law is what exposed that this '
                   'origin\'s TypeScript Run retained no TargetAttributionV2 sidecars. That '
                   'omission was LAWFUL -- execution-inputs section 6: "Missing token / '
                   'empty companions: lawful occupancy-unknown ... not '
                   'required-output-pointer-omitted" -- but it left every endpoint=target '
                   'query answerable only by PARSING the opaque `ts:src/util.ts` payload id, '
                   'which the schema forbids in those words. The sidecars were therefore '
                   'added as part of the same synthetic trusted provider return as the '
                   'facts, the Run was reminted and reclosed, and the closure now enforces '
                   'their joins (the TARGET_ATTRIBUTION_* checks).'),
               'whyTheseAreProviderReturnsAndNotHostProjections': (
                   'an ephemeral HOST projection is licensed only on EXACT inventory '
                   'native-id equality of targetNativeId. `ts:src/util.ts` is not byte-equal '
                   'to the inventory id `src/util.ts`, so no host projection was available '
                   'and the attestation had to come from the provider -- which in this '
                   'reconstruction is a synthetic trusted input, exactly like every other '
                   'provider return here.')},
           'canonicalUnitsAndOrder': {
               'unit': 'one stored edge = one admitted fact2 whose relation declares both a '
                       'sourceField and a targetNativeIdField AND whose target has a '
                       'first-party evaluation occupancy attested by TargetAttributionV2',
               'relationsWithNoGraphEdge': sorted(
                   r for r in g.relreg
                   if not (g.projreg.get(r) or {}).get('targetNativeIdField')),
               'order': 'canonical fact2 id sequence (the only total order the retained '
                        'graph supplies); no host index participates',
               'measuredEdges': [{'factId': e['factId'], 'relation': e['relation'],
                                  'resolution': e['resolution'],
                                  'source': e['sourceNativeId'],
                                  'targetOpaque': e['targetOpaqueNativeId'],
                                  'targetEvaluationId': e['targetNativeId'],
                                  'targetKind': e['targetKind']} for e in g.edges]},
           'operations': cases,
           'failureCases': fr,
           'renderings': rend,
           'whatAQueryNeverDoes': [
               'materialise a fact', 'invoke a provider', 'allocate an attempt',
               'seal a Run', 'derive policy', 'choose a termination',
               'mint negative proof or run a parallel absence evaluator'],
           'evidenceLimitationsVersusStoredEdgeCompletion': {
               'storedEdgeCompletion': ('whether the traversal finished the edges it was '
                                        'asked to walk -- traversalCoverage, visitedNodes, '
                                        'countBasis. It is a property of THIS operation.'),
               'evidenceLimitations': ('whether the underlying EVIDENCE could answer at all '
                                       '-- coverage-unknown, resolution-not-attempted, '
                                       'unresolved-edge-present, unsupported-rung-omitted. '
                                       'It is a property of the sealed Run and is cited, '
                                       'never recomputed.'),
               'whyTheyAreSeparateFields': ('a traversal can be COMPLETE over an incomplete '
                                            'evidence base. Reporting traversalCoverage '
                                            '`complete` as evidence completeness would turn '
                                            'an unexamined region into a claimed absence, '
                                            'which is exactly what the mandatory evidence '
                                            'disclosure exists to prevent. The schema keeps '
                                            'them in different required fields and says '
                                            '"traversalCoverage is not native '
                                            'CoverageResult".')}}
    EV.write('query/graph-query-reconstruction.json', doc)
    bad = []
    for c in cases:
        adm = all(a['admitted'] for a in c['admission'])
        print('%-56s admitted=%-5s %s' % (c['case'][:56], adm,
                                          json.dumps(c['measured'], default=str)[:80]))
        if not adm:
            bad.append((c['case'], c['admission']))
    print()
    for f in fr:
        print('%-52s schemaRefused=%-5s envelopeAdmitted=%s'
              % (f['case'][:52], f['refusedAtTheSchema'],
                 f['lawfulFailureEnvelope']['admitted']))
        if not f['lawfulFailureEnvelope']['admitted']:
            bad.append((f['case'], f['lawfulFailureEnvelope']['owningSchemaError']))
        if not f['refusedAtTheSchema'] and 'refusedAtAdmissionInstead' not in f:
            bad.append((f['case'], 'NEITHER SCHEMA NOR ADMISSION REFUSED'))
    print()
    print('renderings: parityFields=%d humanCarriesAll=%s'
          % (len(rend['parityFields']),
             rend['measuredParityAcrossRenderings']['humanCarriesEveryParityField']))
    if bad:
        print(json.dumps(bad, indent=1, default=str)[:3000])
    assert not bad, [b[0] for b in bad]


main_all()
