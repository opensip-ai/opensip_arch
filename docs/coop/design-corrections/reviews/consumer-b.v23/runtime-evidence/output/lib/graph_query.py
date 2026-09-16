"""R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR -- generation 23 rebuild of graph.neighbors|path|reach
over this origin's ADMITTED TypeScript Run, against workflows/query-projection-contract.v3.md and
evaluator3 graph-query.schema.json major 3.

Why it was rebuilt (V23-D7; the failing generation-22 artifact is preserved at
predecessors.v22/query/graph-query-reconstruction.json). Read against the contract, that artifact
was schema-admitted but behaviourally wrong in these places:
  * an EXTERNAL resolved target (left-pad) was dropped as unprojectable; section 3 projects it as
    a lawful vertex with the opaque payload id;
  * neighbor rows were ordered by fact2 id alone, not by the section-3 endpoint tuple;
  * a full page reported truncated=true, which section 5 forbids;
  * cursors were `ord:N`, not the q3 reference form bound to the selection;
  * visitedNodes counted the whole inventory on graph.path, and path was a priority search, not
    the section-4 FIFO BFS with the cap checked before entry;
  * deficiencyCitations read a proof key that does not exist, so the Run's executionDeficiencies
    were never cited, and `unsupported-rung-omitted` was emitted for a rung the Run merely lacks;
  * fault codes were typed by hand per case instead of being produced by an executor.

What this module does. `execute(graph, request, host)` performs the section-8 steps in order:
request admission, the graph-specific availability selector, the close_run result, view join,
relation table, fact-view selection, cursor binding, endpoint admission, the bounded walk and the
Q3 disclosure. Each case retains its request, its host observations (synthetic trusted inputs,
labelled) and the executor's actual outcome. lib/indep_query_surface.py recomputes every outcome
from the same premises with separately written code.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST
import opensip_closure as CL
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
KIT = S.KIT
Q_DOC = 'workflows/schemas/evaluator3/graph-query.schema.json'
PROJ_DOC = 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json'
CONTRACT_DOC = 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md'
ENUM_PLAN_DOC_SUFFIX = 'enumeration-plan.schema.v1.json'

BOUNDS = {'maxPageSize': 1000, 'defaultPageSize': 100, 'maxItemsPerOperation': 100000,
          'maxTraversalDepth': 64, 'maxVisitedNodes': 1000000}
GRAPH_OPS = ('graph.neighbors', 'graph.path', 'graph.reach')
KINDS = ('file', 'symbol', 'package')
ENDPOINT_KEYS = {'universe', 'kind', 'nativeSubjectId', 'packageManifestPath'}
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
PROJECT_ID = re.compile(r'prj1-[0-9a-f]{64}\Z')
REQUEST_ID = re.compile(r'req1_[0-9a-f]{32}\Z')
CURSOR = re.compile(r'q3\.([0-9a-f]{64})\.([0-9a-f]{64})\.(0|[1-9][0-9]*)\Z')
EXIT = {'success': 0, 'request-rejected': 2, 'indeterminate': 3, 'operational-failed': 4}

# section 3, transcribed; `registry_join` re-reads the registry and refuses a disagreement
TABLE = {
    ('calls', 'resolved-callee'): ('caller', 'symbol', 'resolvedCallee', ['symbol'], 'admitted-target'),
    ('references', 'resolved-binding'): ('referrer', 'symbol', 'resolvedBinding', ['symbol'],
                                         'admitted-target'),
    ('imports', 'resolved-target'): ('importer', 'symbol', 'resolvedTarget',
                                     ['file', 'symbol', 'package'], 'admitted-target'),
    ('control-flow', 'syntactic'): ('from', 'symbol', 'to', ['symbol'], 'same-only'),
    ('reachability', 'from-resolved-calls'): ('origin', 'symbol', 'reachable', ['symbol'],
                                              'same-only'),
}
ORDER = {'graph.neighbors': 'utf8(source tuple, target tuple, fact2 id)',
         'graph.path': 'FIFO BFS, fact2-id adjacency, first target entry',
         'graph.reach': 'utf8(endpoint tuple)'}

DECLARED_INTERPRETATIONS = [
    {'id': 'I-Q1', 'clause': 'section 6 "coverageIds / scopeIds from selected views and other '
     'retained Coverage whose key relation is the declared query relation"',
     'reading': 'every coverageId/scopeId the selected views carry, plus each Coverage of the '
                'Run\'s admitted views whose key.relation is the query relation (with its scope)'},
    {'id': 'I-Q2', 'clause': 'section 5 produced-item law; schema producedItems/totalItems',
     'reading': 'producedItems is the canonical produced prefix of the LOGICAL operation (at most '
                'maxItemsPerOperation), the same on every page; totalItems equals it, qualified '
                'by countBasis'},
    {'id': 'I-Q3', 'clause': 'section 7 has no row for a page size or depth outside the schema',
     'reading': 'a request refused by the owning schema for any reason other than schemaMajor or '
                'the package coordinate is QUERY.PARAMS_MALFORMED'},
    {'id': 'I-Q4', 'clause': 'section 2 fault precedence step 2 versus the GraphEndpoint schema, '
     'which also REQUIRES packageManifestPath on kind=package',
     'reading': 'the section-2 precedence decides the detail: a request whose only schema fault '
                'is the missing package coordinate (re-admitted with a placeholder coordinate) is '
                'QUERY.ENDPOINT_AMBIGUOUS; both boundaries are retained'},
    {'id': 'I-Q5', 'clause': 'TargetAttributionV2 derivation "across admitted SubjectInventoryV1 '
     'rows of this Plan has size 1"',
     'reading': 'the exact-id set is taken over the Run\'s selected inventory rows; the projected '
                'endpoint universe follows the section-3 universe rule'},
    {'id': 'I-Q6', 'clause': 'resolutionLimitations is x-opensip-order sequence with no '
     'published order', 'reading': 'coverage-derived (by coverageId), incoming-search, '
     'unresolved-edge (by factId), fact omissions (by factId), native-evidence-unavailable, '
     'unexamined-work-bound -- algorithm freedom, not a claimed public order'},
    {'id': 'I-Q7', 'clause': 'section 5 cursor binding',
     'reading': 'selectionHash64 = SHA-256 of C({projectId, runId, factViewDigests, operation, '
                'params (includeStart materialised), order}); position is the third field'},
    {'id': 'I-Q8', 'clause': 'section 8 step order',
     'reading': 'admission, availability selector, close_run result, view join (projectId first), '
                'relation table, fact views, cursor, endpoints, walk, disclosure'},
]


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


def tkey(ep):
    return tuple(x.encode() for x in (ep['universe'], ep['kind'], ep['nativeSubjectId'],
                                      ep.get('packageManifestPath') or ''))


def endpoint(universe, kind, nsid, pmp=None):
    ep = {'universe': universe, 'kind': kind, 'nativeSubjectId': nsid}
    if kind == 'package':
        ep['packageManifestPath'] = pmp
    return ep


class Refusal(Exception):
    def __init__(self, cls, code, detail, remedy, subject, fault=None, step=None, note=None):
        super().__init__(detail)
        self.cls, self.code, self.detail, self.remedy = cls, code, detail, remedy
        self.subject, self.fault, self.step, self.note = subject, fault, step, note

    def row(self):
        return {'class': self.cls, 'errorCode': self.code, 'domainDetail': self.detail,
                'faultCause': self.fault, 'exitCode': EXIT[self.cls], 'step': self.step,
                'note': self.note}


def rejected(code, detail, remedy, subject, step, note=None):
    return Refusal('request-rejected', code, detail, remedy, subject, step=step, note=note)


class Graph:
    """The admitted Run and the inputs its proof selected. Nothing ambient is read."""

    def __init__(self, label):
        self.label = label
        self.st, self.doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        self.c = CL.Closure(self.st)
        self.runId = self.doc['claim']['runId']
        rep = self.c.close_run(self.runId, 'graph-query:' + label)
        self.closeRunAdmitted = bool(rep['admitted'])
        assert self.closeRunAdmitted, rep['refusals'][:2]
        o = self.st.objects
        self.run = o[self.runId]
        self.projectId, self.snapshotId = self.run['projectId'], self.run['snapshotId']
        self.proof = o[o[self.run['evaluationSealId']]['proofBundleId']]
        self.views = {vid: o[vid] for vid in o[self.run['evidenceId']]['viewIds']}
        self.registry = kitdoc(PROJ_DOC)['relations']
        self.relreg = self.c.relreg['relations']
        refs = self.proof['evaluationInputRefs']
        self.inventories = [(r['digest'], self.json(r['digest'])) for r in refs
                            if r['domain'] == 'subject-inventory']
        self.attributions = {}
        for r in refs:
            if r['domain'] == 'target-attribution':
                rec = self.json(r['digest'])
                self.attributions[rec['sourceFactId']] = (r['digest'], rec)
        self.incoming = [(r['digest'], self.json(r['digest'])) for r in refs
                         if r['domain'] == 'incoming-search']
        eps = [p for (doc, _sel), ps in self.c.spec_parameters.items()
               if doc.endswith(ENUM_PLAN_DOC_SUFFIX) for p in ps]
        assert len(eps) == 1, 'exactly one selected enumeration-plan parameter'
        self.enumeration_plan = self.json(eps[0]['payloadDigest'])
        self.vertices, self.unbound_inventories = self._inventory_vertices()
        self.coverages = {}
        for v in self.views.values():
            for cid in v['coverageIds']:
                self.coverages[cid] = self.json(o[cid]['payloadDigest'])
        self.unresolved_edges = sorted({fid for v in self.views.values() for fid in v['facts']
                                        if o[fid]['relation'] == 'unresolved-edge'},
                                       key=str.encode)

    def json(self, digest):
        return json.loads(self.st.get_blob(digest.split(':')[-1]).decode())

    def registry_join(self):
        rows = []
        for (rel, rung), (sf, sk, tf, tks, ur) in sorted(TABLE.items()):
            r = self.registry[rel]
            rows.append({'relation': rel, 'minResolution': rung, 'sourceField': sf,
                         'sourceKind': sk, 'targetField': tf, 'targetKinds': tks,
                         'universeRule': ur,
                         'registryAgrees': (r['sourceField'] == sf and r['sourceSubjectKind'] == sk
                                            and r['targetNativeIdField'] == tf
                                            and r['targetKinds'] == tks
                                            and r['universeRule'] == ur
                                            and rung in r['ladder'])})
        return rows

    def _inventory_vertices(self):
        """Section 2 item 1: selected inventory rows, universe from the program binding."""
        out, unbound = set(), []
        for dig, inv in self.inventories:
            cell = self.enumeration_plan['cells'][inv['cellOrdinal']]
            pb = [b for b in cell['programBindings'] if b['ordinal'] == inv['programOrdinal']]
            if len(pb) != 1 or not pb[0].get('universe'):
                unbound.append(dig)
                continue
            for row in inv['rows']:
                out.add((pb[0]['universe'], row['kind'], row['nativeSubjectId'],
                         row['path'] if row['kind'] == 'package' else ''))
        return out, unbound

    # ---------------------------------------------------------------- section 3 projection
    def occupancy(self, fid, target_native):
        ids = sorted({v for v in self.vertices if v[2] == target_native})
        if len(ids) == 1:
            u, k, n, p = ids[0]
            return {'occupancy': 'first-party', 'kind': k, 'nativeId': n,
                    'packageManifestPath': p or None, 'from': 'ephemeral-exact-id'}
        sc = self.attributions.get(fid)
        if sc is None:
            return {'occupancy': 'unknown', 'kind': 'unknown', 'from': 'no-sidecar-no-exact-id'}
        rec = sc[1]
        occ = {'occupancy': rec['occupancy'], 'kind': rec['kind'],
               'packageManifestPath': rec['packageManifestPath'], 'from': 'sidecar',
               'sidecarDigest': sc[0]}
        if rec['occupancy'] == 'first-party':
            occ['nativeId'] = rec['evaluationNativeId']
        return occ

    def project(self, relation, rung, selected):
        sf, sk, tf, tks, ur = TABLE[(relation, rung)]
        ladder = self.relreg[relation]['ladder']
        edges, omissions, seen = [], [], set()
        for vid in selected:
            for fid in self.views[vid]['facts']:
                f = self.st.objects[fid]
                if f['relation'] != relation or fid in seen:
                    continue
                seen.add(fid)
                if ladder.index(f['resolution']) < ladder.index(rung):
                    omissions.append(('unsupported-rung-omitted', fid))
                    continue
                pay = self.json(f['payloadDigest'])
                src, tgt = pay.get(sf), pay.get(tf)
                if not (isinstance(src, str) and src and isinstance(tgt, str) and tgt):
                    omissions.append(('unprojectable-fact', fid))
                    continue
                tu = f['targetUniverse'] if ur == 'admitted-target' else f['sourceUniverse']
                occ = self.occupancy(fid, tgt)
                if occ['occupancy'] == 'first-party':
                    target = endpoint(tu, occ['kind'], occ['nativeId'], occ['packageManifestPath'])
                elif occ['occupancy'] == 'external' and occ['kind'] in KINDS \
                        and (occ['kind'] != 'package' or occ['packageManifestPath']):
                    target = endpoint(tu, occ['kind'], tgt, occ['packageManifestPath'])
                elif len(tks) == 1:
                    target = endpoint(tu, tks[0], tgt)
                else:
                    omissions.append(('unprojectable-fact', fid))
                    continue
                if target['kind'] not in tks:
                    omissions.append(('unprojectable-fact', fid))
                    continue
                edges.append({'factId': fid, 'relation': relation, 'resolution': f['resolution'],
                              'source': endpoint(f['sourceUniverse'], sk, src), 'target': target,
                              'producerClosure': f['producerClosure'],
                              'confidenceMillionths': f['confidenceMillionths'],
                              'targetOccupancy': occ})
        edges.sort(key=lambda e: e['factId'].encode())
        return edges, sorted(omissions, key=lambda x: x[1].encode())

    def view_matches(self, vid, relation, rung):
        return any(self.st.objects[s]['relation'] == relation
                   and self.st.objects[s]['resolution'] == rung
                   for s in self.views[vid]['scopeIds'])

    # ---------------------------------------------------------------- section 6 disclosure
    def disclosure(self, relation, rung, selected, matching, omissions, bound):
        cov, scopes = set(), set()
        for vid in selected:
            cov |= set(self.views[vid]['coverageIds'])
            scopes |= set(self.views[vid]['scopeIds'])
        for cid, pay in self.coverages.items():
            if pay['key']['relation'] == relation:
                cov.add(cid)
                scopes.add(self.st.objects[cid]['scopeId'])
        lim = []
        for cid in sorted(cov, key=str.encode):
            e = (self.coverages.get(cid) or self.json(self.st.objects[cid]['payloadDigest']))['entry']
            rc = e['resolutionCompleteness']
            base = {'coverageId': cid, 'resolutionState': rc['state'],
                    'unresolvedEdgeCount': rc['unresolvedEdgeCount'],
                    'examinedExhaustive': rc['examinedExhaustive'], 'attempted': rc['attempted'],
                    'coverage': e['coverage']}
            if e.get('deficiency') is not None:
                base['note'] = 'deficiency=%s' % e['deficiency']
            kinds = {'unknown': ['coverage-unknown'], 'partial': ['coverage-partial']}.get(
                e['coverage'], [])
            kinds += {'incomplete': ['resolution-incomplete'], 'partial': ['resolution-partial'],
                      'not-attempted': ['resolution-not-attempted']}.get(rc['state'], [])
            if not rc['examinedExhaustive']:
                kinds.append('examined-not-exhaustive')
            lim += [dict({'kind': k}, **base) for k in kinds]
        for dig, rec in self.incoming:
            if rec['relation'] == relation and rec['minResolution'] == rung and not (
                    rec['completeSearch'] and rec['examinedExhaustive']
                    and rec['coverage'] == 'complete'
                    and rec['resolutionCompleteness']['state'] in ('complete', 'not-applicable')):
                lim.append({'kind': 'incoming-search-incomplete', 'incomingSearchDigest': dig,
                            'relation': relation, 'minResolution': rung,
                            'coverage': rec['coverage'],
                            'examinedExhaustive': rec['examinedExhaustive'],
                            'resolutionState': rec['resolutionCompleteness']['state']})
        lim += [{'kind': 'unresolved-edge-present', 'factId': fid} for fid in self.unresolved_edges]
        lim += [{'kind': k, 'factId': fid} for k, fid in omissions]
        if not matching:
            lim.append({'kind': 'native-evidence-unavailable', 'relation': relation,
                        'minResolution': rung})
        if bound:
            lim.append({'kind': 'unexamined-work-bound'})
        cites = [{k: d[k] for k in ('source', 'cause', 'subjectId', 'predicateId', 'inputRefs',
                                    'coverageId', 'nativeCause') if k in d}
                 for d in self.proof['executionDeficiencies']]
        return {'coverageIds': sorted(cov, key=str.encode), 'scopeIds': sorted(scopes, key=str.encode),
                'deficiencyCitations': cites, 'resolutionLimitations': lim}


# -------------------------------------------------------------------- endpoint admission
def endpoint_syntax(e):
    """Section 2 fault precedence, steps 1 and 2 (the syntactic part)."""
    if not isinstance(e, dict) or set(e) - ENDPOINT_KEYS \
            or not {'universe', 'kind', 'nativeSubjectId'} <= set(e):
        return 'QUERY.PARAMS_MALFORMED'
    if not isinstance(e['universe'], str) or not HEX64.match(e['universe']) \
            or e['kind'] not in KINDS or not isinstance(e['nativeSubjectId'], str) \
            or not e['nativeSubjectId'] \
            or ('packageManifestPath' in e and e['kind'] != 'package'):
        return 'QUERY.PARAMS_MALFORMED'
    if e['kind'] == 'package' and not e.get('packageManifestPath'):
        return 'QUERY.ENDPOINT_AMBIGUOUS'
    return None


def selection_hash(project_id, run_id, views, operation, params):
    return hashlib.sha256(K.C({'projectId': project_id, 'runId': run_id,
                               'factViewDigests': list(views), 'operation': operation,
                               'params': params, 'order': ORDER[operation]})).hexdigest()


def hops(edges, v, direction):
    for e in edges:
        s, t = tkey(e['source']), tkey(e['target'])
        if direction == 'outgoing' and s == v:
            yield e, e['target']
        elif direction == 'incoming' and t == v:
            yield e, e['source']
        elif direction == 'both' and (s == v or t == v):
            yield e, (e['target'] if s == v else e['source'])


# -------------------------------------------------------------------- the executor
def execute(g, req, host):
    rid = host.get('requestId')
    if not isinstance(rid, str) or not REQUEST_ID.match(rid):
        return {'kind': 'reference-call-precondition',
                'reason': 'host.requestId is missing or is not req1_ + 32 hex; section 7 makes '
                          'this a reference-call precondition, distinct from a public refusal',
                'publicEnvelope': None}
    try:
        return {'kind': 'response', 'response': _execute(g, req, host)}
    except Refusal as r:
        detail = {'code': r.detail, 'remedy': r.remedy, 'subject': r.subject}
        term = {'class': r.cls, 'errorCode': r.code, 'domainDetail': detail}
        if r.fault:
            term['faultCause'] = r.fault
        env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'failure',
               'requestId': rid, 'termination': term, 'exitCode': EXIT[r.cls],
               'errors': [detail]}
        if isinstance(req.get('projectId'), str) and PROJECT_ID.match(req['projectId']):
            env['projectId'] = req['projectId']
        return {'kind': 'failure', 'refusal': r.row(), 'envelope': env,
                'envelopeAdmission': EV.admit(env, 'graph-query-failure')}


def _execute(g, req, host):
    op = req.get('operation')
    # 1. request admission
    if req.get('schemaMajor') != 3:
        raise rejected('REQUEST.SCHEMA_MAJOR_UNSUPPORTED', 'QUERY.SCHEMA_MAJOR_UNSUPPORTED',
                       'send schemaMajor 3', 'schemaMajor', 'admission')
    adm = S.admit(Q_DOC, '#/$defs/GraphQueryRequestV1', req, 'graph-query-request')
    params = req.get('params') if isinstance(req.get('params'), dict) else {}
    faults = [endpoint_syntax(params[k]) for k in ('endpoint', 'start', 'target') if k in params]
    if op in GRAPH_OPS and 'QUERY.PARAMS_MALFORMED' in faults:
        raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED',
                       'graph endpoints are {universe, kind, nativeSubjectId, '
                       '(packageManifestPath)}', 'params endpoint', 'admission')
    if not adm['admitted']:
        if 'QUERY.ENDPOINT_AMBIGUOUS' in faults:
            patched = json.loads(json.dumps(req))
            for k in ('endpoint', 'start', 'target'):
                e = patched['params'].get(k)
                if isinstance(e, dict) and e.get('kind') == 'package' and not e.get('packageManifestPath'):
                    e['packageManifestPath'] = 'package.json'
            if S.admit(Q_DOC, '#/$defs/GraphQueryRequestV1', patched, 'gq-i-q4')['admitted']:
                raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.ENDPOINT_AMBIGUOUS',
                               'name the package manifest path', 'params endpoint', 'admission',
                               note='I-Q4: the owning schema also refuses this request')
        raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED',
                       'correct the request to the closed graph-query shape', 'request',
                       'admission', note={'stock': adm['stockSchemaErrors'][:2],
                                          'keywords': adm['publishedKeywordRefusals'][:2]})
    if 'QUERY.ENDPOINT_AMBIGUOUS' in faults:
        raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.ENDPOINT_AMBIGUOUS',
                       'name the package manifest path', 'params endpoint', 'admission')
    assert op in GRAPH_OPS, 'this executor serves the three graph operations only'
    # 2. graph-specific availability selector (identity section 5), before replay is consulted
    av = host.get('availability')
    if av in ('purged', 'expired', 'corrupt', 'missing'):
        raise Refusal('operational-failed', 'HOST.IO_FAILURE', 'evidence.' + av,
                      'the required evidence of this Run is %s; the sealed manifest remains' % av,
                      g.runId, fault='host-io', step='availability')
    # 3. close_run
    assert g.closeRunAdmitted
    # 4. view join
    view = req['view']
    unknown = lambda why: rejected('IDENTITY.UNKNOWN', 'QUERY.VIEW_UNKNOWN',
                                   'name the admitted Run', 'view', 'view-join', note=why)
    if req['projectId'] != g.projectId:
        raise unknown('projectId is not the admitted Run\'s project')
    if 'runId' in view:
        if view['runId'] != g.runId:
            raise unknown('runId is not the close_run identity')
    elif 'snapshotId' in view:
        obs = (host.get('runsForSnapshot') or {}).get(view['snapshotId'])
        if not obs:
            raise unknown('no complete trusted host.runsForSnapshot observation')
        if len(set(obs)) > 1:
            raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.VIEW_AMBIGUOUS',
                           'select one Run by runId', 'view', 'view-join')
        if obs[0] != g.runId or view['snapshotId'] != g.snapshotId:
            raise unknown('the observation does not name the admitted Run for this snapshot')
    elif host.get('latestRunId') != g.runId:
        raise unknown('trusted host.latestRunId is missing or is not the admitted Run')
    # 5. relation table
    relation, rung = params['relation'], params['minResolution']
    if (relation, rung) not in TABLE:
        raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.RELATION_UNSUPPORTED',
                       'use a graph-projectable relation@rung', relation + '@' + rung,
                       'relation-table')
    # 6. fact views
    if 'factViewDigests' in params:
        bad = [d for d in params['factViewDigests'] if d not in g.views]
        if bad:
            raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.FACT_VIEW_UNAVAILABLE',
                           'name admitted views of this Run', bad[0], 'fact-views')
        selected = sorted(params['factViewDigests'], key=str.encode)
    else:
        selected = sorted((v for v in g.views if g.view_matches(v, relation, rung)), key=str.encode)
    matching = [v for v in selected if g.view_matches(v, relation, rung)]
    # 7. cursor
    eff = dict(params)
    if op == 'graph.reach':
        eff.setdefault('includeStart', False)
    sh = selection_hash(g.projectId, g.runId, selected, op, eff)
    pos, cur = 0, req['page'].get('cursor')
    if cur is not None:
        m = CURSOR.match(cur)
        if not m or 'runId' not in view or m.group(1) != g.runId.split(':', 1)[1] \
                or m.group(2) != sh:
            raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.CURSOR_MISMATCH',
                           'continue with the same view {runId}, fact views and params',
                           'page.cursor', 'cursor')
        pos = int(m.group(3))
    # 8. projection and endpoint admission
    edges, omissions = g.project(relation, rung, selected)
    domain = set(g.vertices) | {tuple(x.decode() for x in tkey(e[k]))
                                for e in edges for k in ('source', 'target')}

    def admit(e):
        t = (e['universe'], e['kind'], e['nativeSubjectId'], e.get('packageManifestPath') or '')
        if t not in domain:
            raise rejected('REQUEST.PRECONDITION_FAILED', 'QUERY.ENDPOINT_UNKNOWN',
                           'name a vertex of this Run\'s domain', 'params endpoint', 'endpoints')
        return tuple(x.encode() for x in t)

    bounds = dict(BOUNDS)
    for k, v in (host.get('testBounds') or {}).items():
        bounds[k] = min(bounds[k], v)
    vcap, icap = bounds['maxVisitedNodes'], bounds['maxItemsPerOperation']
    # 9. the walk
    bound = False
    if op == 'graph.neighbors':
        v = admit(params['endpoint'])
        visited = 1
        units = [e for e in edges
                 if (params['direction'] in ('outgoing', 'both') and tkey(e['source']) == v)
                 or (params['direction'] in ('incoming', 'both') and tkey(e['target']) == v)]
        units.sort(key=lambda e: (tkey(e['source']), tkey(e['target']), e['factId'].encode()))
        units = [{k: e[k] for k in ('factId', 'relation', 'resolution', 'source', 'target',
                                    'producerClosure', 'confidenceMillionths')} for e in units]
    elif op == 'graph.reach':
        start = admit(params['start'])
        first = {start: (0, None, params['start'])}
        queue, visited = [start], 1
        while queue and not bound:
            v = queue.pop(0)
            d = first[v][0]
            if d >= params['maxDepth']:
                continue
            for e, w_ep in hops(edges, v, params['direction']):
                w = tkey(w_ep)
                if w in first:
                    continue
                if visited >= vcap:
                    bound = True
                    break
                first[w] = (d + 1, e['factId'], w_ep)
                visited += 1
                queue.append(w)
        units = []
        for w in sorted(first):
            d, via, w_ep = first[w]
            if d == 0 and not eff['includeStart']:
                continue
            row = {'endpoint': w_ep, 'depth': d}
            if via:
                row['viaFactId'] = via
            units.append(row)
    else:
        start, target = admit(params['start']), admit(params['target'])
        if start == target:
            visited = 1
            units = [{'hopCount': 0, 'start': params['start'], 'target': params['target'],
                      'nodes': [params['start']], 'edges': []}]
        else:
            parent = {start: None}
            depth = {start: 0}
            queue, visited, found = [start], 1, False
            while queue and not found and not bound:
                v = queue.pop(0)
                if depth[v] >= params['maxDepth']:
                    continue
                for e, w_ep in hops(edges, v, params['direction']):
                    w = tkey(w_ep)
                    if w in parent:
                        continue
                    if visited >= vcap:
                        bound = True
                        break
                    parent[w], depth[w] = (v, e, w_ep), depth[v] + 1
                    visited += 1
                    if w == target:
                        found = True
                        break
                    queue.append(w)
            units = []
            if found:
                chain, w = [], target
                while parent[w] is not None:
                    chain.append(parent[w])
                    w = parent[w][0]
                chain.reverse()
                units = [{'hopCount': len(chain), 'start': params['start'],
                          'target': params['target'],
                          'nodes': [params['start']] + [c[2] for c in chain],
                          'edges': [{'factId': c[1]['factId'], 'source': c[1]['source'],
                                     'target': c[1]['target']} for c in chain]}]
    if len(units) > icap:
        units, bound = units[:icap], True
    # 10. response
    size = req['page']['size']
    page = units[pos:pos + size]
    more = pos + size < len(units)
    ctx = {'projectId': g.projectId, 'resolvedView': {'runId': g.runId},
           'factViewDigests': selected, 'availability': 'retained', 'truncated': bound,
           'totalItems': len(units), 'countBasis': 'lower-bound' if bound else 'exact',
           'traversalCoverage': ('truncated-bound' if bound else
                                 'truncated-page' if more else 'complete'),
           'visitedNodes': visited, 'producedItems': len(units), 'advisory': False,
           'evidence': g.disclosure(relation, rung, selected, matching, omissions, bound)}
    if more:
        ctx['nextCursor'] = 'q3.%s.%s.%d' % (g.runId.split(':', 1)[1], sh, pos + size)
    term = ({'class': 'indeterminate', 'reasonCodes': ['QUERY.COMPLETENESS_UNMET'],
             'runId': g.runId}
            if bound and req['completeness'] == 'required' else {'class': 'success'})
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': op,
            'context': ctx, 'items': page, 'termination': term}


def request(g, operation, params, *, view=None, completeness='required', size=100, cursor=None,
            major=3):
    page = {'size': size}
    if cursor is not None:
        page['cursor'] = cursor
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': major,
            'projectId': g.projectId, 'view': view or {'runId': g.runId},
            'operation': operation, 'params': params, 'completeness': completeness,
            'page': page}


_REQ = [0]


def host(**obs):
    """Synthetic trusted host observations. The RequestId is a reserved counter, never hashed
    from request bytes."""
    _REQ[0] += 1
    return dict({'requestId': 'req1_%032x' % _REQ[0], 'standing': 'synthetic trusted host '
                 'observation (no host qualified)'}, **obs)


def admit_pair(req, resp):
    out = []
    for what, inst, sel in (('request', req, '#/$defs/GraphQueryRequestV1'),
                            ('response', resp, '#/$defs/GraphQueryResponseV1')):
        r = S.admit(Q_DOC, sel, inst, 'graph-query-' + what)
        out.append({'what': what, 'admitted': r['admitted'],
                    'error': None if r['admitted'] else {'stock': r['stockSchemaErrors'][:3],
                                                         'keywords': r['publishedKeywordRefusals'][:3]}})
    return out


def cases(g):
    ops, fails = [], []
    main = [v for v in g.vertices if v[1] == 'symbol' and v[2] == 'ts:src/index.ts#main'][0]
    U = main[0]
    MAIN = endpoint(U, 'symbol', 'ts:src/index.ts#main')
    UTIL_FILE = endpoint(U, 'file', 'src/util.ts')
    LEFTPAD = endpoint(U, 'file', 'ts:node_modules/left-pad/index.d.ts')
    APP = endpoint(U, 'package', 'app', 'package.json')
    IMP = {'relation': 'imports', 'minResolution': 'resolved-target'}

    def run(label, req, h, cls, why, into, chain=None):
        out = execute(g, req, h)
        row = {'case': label, 'classification': cls, 'why': why, 'host': h, 'request': req,
               'outcome': out}
        if out['kind'] == 'response':
            row['admission'] = admit_pair(req, out['response'])
        if chain:
            row['continues'] = chain
        into.append(row)
        return out

    run('graph.neighbors-outgoing-first-party-and-external',
        request(g, 'graph.neighbors', dict(IMP, direction='outgoing', endpoint=MAIN)), host(),
        'valid', 'section 3: two first-party file targets (sidecar evaluationNativeId) and one '
        'EXTERNAL file target projected with its opaque payload id', ops)
    p = dict(IMP, direction='outgoing', endpoint=MAIN)
    o1 = run('graph.neighbors-page-1', request(g, 'graph.neighbors', p, size=1), host(), 'valid',
             'section 5: a full page is truncated-page with truncated=false and a q3 cursor', ops)
    c1 = o1['response']['context'].get('nextCursor')
    o2 = run('graph.neighbors-page-2', request(g, 'graph.neighbors', p, size=1, cursor=c1), host(),
             'valid', 'continuation of the same selection', ops, chain='graph.neighbors-page-1')
    c2 = o2['response']['context'].get('nextCursor') if o2['kind'] == 'response' else None
    run('graph.neighbors-page-3', request(g, 'graph.neighbors', p, size=1, cursor=c2), host(),
        'valid', 'the last page is complete and carries no cursor', ops,
        chain='graph.neighbors-page-2')
    run('graph.neighbors-incoming-at-an-external-vertex',
        request(g, 'graph.neighbors', dict(IMP, direction='incoming', endpoint=LEFTPAD)), host(),
        'valid', 'section 2 item 2: an external resolved target of a projected fact is a lawful '
        'vertex', ops)
    run('graph.neighbors-isolated-inventory-vertex',
        request(g, 'graph.neighbors', dict(IMP, direction='both', endpoint=APP)), host(), 'valid',
        'section 2 item 4: an isolated inventory vertex is lawful and has no neighbors', ops)
    view_ids = sorted(g.views)
    run('graph.neighbors-explicit-fact-views',
        request(g, 'graph.neighbors', dict(IMP, direction='outgoing', endpoint=MAIN,
                                           factViewDigests=view_ids)), host(), 'valid',
        'section 1: an explicit admitted view set', ops)
    run('graph.neighbors-no-selected-view-matches',
        request(g, 'graph.neighbors', {'relation': 'calls', 'minResolution': 'resolved-callee',
                                       'direction': 'outgoing', 'endpoint': MAIN}), host(),
        'valid', 'section 6: no selected view carries calls@resolved-callee, so the disclosure '
        'says native-evidence-unavailable; zero rows are not "no callees"', ops)
    run('graph.neighbors-view-by-snapshot',
        request(g, 'graph.neighbors', dict(IMP, direction='outgoing', endpoint=MAIN),
                view={'snapshotId': g.snapshotId}),
        host(runsForSnapshot={g.snapshotId: [g.runId]}), 'valid',
        'section 1: a snapshot selector with a complete trusted resolver observation', ops)
    run('graph.neighbors-view-latest',
        request(g, 'graph.neighbors', dict(IMP, direction='outgoing', endpoint=MAIN),
                view={'latest': True}), host(latestRunId=g.runId), 'valid',
        'section 1: latest with an explicit trusted observation', ops)
    run('graph.path-one-hop',
        request(g, 'graph.path', dict(IMP, direction='outgoing', start=MAIN, target=UTIL_FILE,
                                      maxDepth=8)), host(), 'valid',
        'section 4: FIFO BFS; the target is entered after src/legacy.js, so three endpoints are '
        'entered', ops)
    run('graph.path-incoming',
        request(g, 'graph.path', dict(IMP, direction='incoming', start=UTIL_FILE, target=MAIN,
                                      maxDepth=8)), host(), 'valid', 'incoming follows reverse',
        ops)
    run('graph.path-start-equals-target',
        request(g, 'graph.path', dict(IMP, direction='outgoing', start=MAIN, target=MAIN,
                                      maxDepth=8)), host(), 'valid', 'the zero-hop law', ops)
    run('graph.path-zero-hop-exactly-at-cap',
        request(g, 'graph.path', dict(IMP, direction='outgoing', start=MAIN, target=MAIN,
                                      maxDepth=8)), host(testBounds={'maxVisitedNodes': 1}),
        'valid', 'section 5: zero-hop with maxVisitedNodes=1 is exactly-at-cap complete', ops)
    run('graph.path-one-edge-under-cap-1-required',
        request(g, 'graph.path', dict(IMP, direction='outgoing', start=MAIN, target=UTIL_FILE,
                                      maxDepth=8)), host(testBounds={'maxVisitedNodes': 1}),
        'valid', 'section 5: the target is not entered, visitedNodes=1, truncated-bound, no path '
        'claimed, QUERY.COMPLETENESS_UNMET', ops)
    run('graph.path-unreachable-within-depth',
        request(g, 'graph.path', dict(IMP, direction='outgoing', start=UTIL_FILE, target=MAIN,
                                      maxDepth=8)), host(), 'valid',
        'no outgoing import leaves src/util.ts: the walk completes with no path, exact zero', ops)
    run('graph.reach-outgoing-default-include-start',
        request(g, 'graph.reach', dict(IMP, direction='outgoing', start=MAIN, maxDepth=64)),
        host(), 'valid', 'section 4: includeStart defaults to false; rows sort by endpoint tuple',
        ops)
    run('graph.reach-both-depth-2-include-start',
        request(g, 'graph.reach', dict(IMP, direction='both', start=UTIL_FILE, maxDepth=2,
                                       includeStart=True)), host(), 'valid',
        'first-discovery depth and viaFactId over an undirected walk', ops)
    run('graph.reach-both-depth-1',
        request(g, 'graph.reach', dict(IMP, direction='both', start=UTIL_FILE, maxDepth=1)),
        host(), 'valid', 'maxDepth is semantic: endpoints at depth 2 are not owed', ops)
    run('graph.reach-visited-cap-required',
        request(g, 'graph.reach', dict(IMP, direction='outgoing', start=MAIN, maxDepth=64,
                                       includeStart=True)),
        host(testBounds={'maxVisitedNodes': 2}), 'valid',
        'reach stops at the first owed endpoint that cannot enter; required -> indeterminate', ops)
    run('graph.reach-visited-cap-best-effort',
        request(g, 'graph.reach', dict(IMP, direction='outgoing', start=MAIN, maxDepth=64,
                                       includeStart=True), completeness='best-effort'),
        host(testBounds={'maxVisitedNodes': 2}), 'valid',
        'best-effort: the same truncated-bound, success class, no continuation past the cap', ops)
    run('graph.reach-produced-item-cap',
        request(g, 'graph.reach', dict(IMP, direction='outgoing', start=MAIN, maxDepth=64)),
        host(testBounds={'maxItemsPerOperation': 2}), 'valid',
        'section 5 produced-item law: the canonical prefix, countBasis lower-bound', ops)

    # ---- failures (the executor decides every code)
    def fail(label, req, h, why):
        run(label, req, h, 'invalid', why, fails)

    good = dict(IMP, direction='outgoing', endpoint=MAIN)
    fail('schema-major-2', request(g, 'graph.neighbors', good, major=2), host(),
         'section 7 row 1')
    fail('endpoint-is-a-logical-path-only',
         request(g, 'graph.neighbors', dict(IMP, direction='outgoing',
                                            endpoint={'path': 'src/index.ts'})), host(),
         'LogicalPath-only endpoint')
    fail('endpoint-universe-not-hex',
         request(g, 'graph.neighbors', dict(good, endpoint=dict(MAIN, universe='U'))), host(),
         'section 2 step 1')
    fail('package-coordinate-on-a-symbol',
         request(g, 'graph.neighbors', dict(good, endpoint=dict(MAIN, packageManifestPath='a'))),
         host(), 'section 2 step 1')
    fail('params-extra-property', request(g, 'graph.neighbors', dict(good, subject='src/a.ts')),
         host(), 'closed params')
    fail('params-of-another-operation',
         request(g, 'graph.path', dict(IMP, direction='outgoing', endpoint=MAIN)), host(),
         'graph.path requires start/target/maxDepth')
    fail('page-size-above-the-maximum', request(g, 'graph.neighbors', good, size=1001), host(),
         'I-Q3')
    fail('traversal-depth-above-the-maximum',
         request(g, 'graph.reach', dict(IMP, direction='outgoing', start=MAIN, maxDepth=65)),
         host(), 'I-Q3')
    fail('package-endpoint-without-manifest-path',
         request(g, 'graph.neighbors', dict(good, endpoint={'universe': U, 'kind': 'package',
                                                            'nativeSubjectId': 'app'})), host(),
         'section 2 step 2, I-Q4')
    fail('non-projectable-rung', request(g, 'graph.neighbors',
                                         dict(good, minResolution='syntactic-specifier')),
         host(), 'section 3: imports@syntactic-specifier is not graph-projectable')
    fail('non-graph-relation', request(g, 'graph.neighbors',
                                       dict(good, relation='declares', minResolution='syntactic')),
         host(), 'section 3: declares is not graph-projectable')
    fail('endpoint-unknown', request(g, 'graph.neighbors',
                                     dict(good, endpoint=endpoint(U, 'symbol', 'ts:src/ghost.ts#g'))),
         host(), 'section 2 step 3')
    fail('endpoint-same-native-id-other-universe',
         request(g, 'graph.neighbors', dict(good, endpoint=dict(MAIN, universe='0' * 64))),
         host(), 'section 2 step 3: another universe does not make it ambiguous')
    fail('endpoint-kind-disagrees-with-the-vertex',
         request(g, 'graph.neighbors', dict(good, endpoint=endpoint(U, 'file', 'ts:src/index.ts#main'))),
         host(), 'a complete tuple that is no vertex')
    fail('view-run-not-admitted', request(g, 'graph.neighbors', good,
                                          view={'runId': 'run3:' + '0' * 64}), host(),
         'section 7 VIEW_UNKNOWN')
    fail('view-snapshot-without-observation',
         request(g, 'graph.neighbors', good, view={'snapshotId': g.snapshotId}), host(),
         'one admitted Run does not prove uniqueness')
    fail('view-snapshot-two-runs',
         request(g, 'graph.neighbors', good, view={'snapshotId': g.snapshotId}),
         host(runsForSnapshot={g.snapshotId: [g.runId, 'run3:' + 'f' * 64]}),
         'section 7 VIEW_AMBIGUOUS')
    fail('view-latest-without-observation',
         request(g, 'graph.neighbors', good, view={'latest': True}), host(),
         'golden query-latest-empty: IDENTITY.UNKNOWN exit 2')
    fail('fact-view-not-on-this-run',
         request(g, 'graph.neighbors', dict(good, factViewDigests=['view2:' + '0' * 64])), host(),
         'section 7 FACT_VIEW_UNAVAILABLE')
    fail('cursor-bound-to-other-params',
         request(g, 'graph.neighbors', dict(good, direction='both'), size=1, cursor=c1), host(),
         'section 5: the token binds the effective params')
    fail('cursor-continued-under-latest',
         request(g, 'graph.neighbors', p, view={'latest': True}, size=1, cursor=c1),
         host(latestRunId=g.runId), 'section 5: continuation requires view {runId}')
    fail('evidence-purged', request(g, 'graph.neighbors', good), host(availability='purged'),
         'identity section 5 + contract section 7: graph ops are operational-failed exit 4')
    fail('evidence-corrupt', request(g, 'graph.neighbors', good), host(availability='corrupt'),
         'section 7 corrupt retained bytes')
    rc = execute(g, request(g, 'graph.neighbors', good), {'standing': 'no requestId observed'})
    fails.append({'case': 'host-request-id-missing', 'classification': 'invalid',
                  'why': 'section 7: a reference-call precondition, not a public refusal',
                  'host': {'standing': 'no requestId observed'},
                  'request': request(g, 'graph.neighbors', good), 'outcome': rc})
    return ops, fails


def renderings(case):
    """command-inventory.v3 `query` parity fields in human / json / agent."""
    resp = case['outcome']['response']
    ctx = resp['context']
    parity = {'resolved-view': ctx['resolvedView']['runId'], 'availability': ctx['availability'],
              'truncated': ctx['truncated'], 'total-items': ctx['totalItems'],
              'termination-class': resp['termination']['class'],
              'query-response': hashlib.sha256(K.C(resp)).hexdigest()}
    human = '\n'.join('%-18s %s' % (k, json.dumps(v) if isinstance(v, bool) else v)
                      for k, v in parity.items())
    agent = {'response': resp, 'hints': ['read-only: no fact, attempt or Run was created',
                                         'totalItems is qualified by countBasis']}
    from_agent = {'resolved-view': agent['response']['context']['resolvedView']['runId'],
                  'availability': agent['response']['context']['availability'],
                  'truncated': agent['response']['context']['truncated'],
                  'total-items': agent['response']['context']['totalItems'],
                  'termination-class': agent['response']['termination']['class'],
                  'query-response': hashlib.sha256(K.C(agent['response'])).hexdigest()}
    from_human = dict(line.split(None, 1) for line in human.splitlines())
    return {'source': case['case'], 'parityReference': 'json (the response bytes)',
            'parityFields': parity, 'humanRendering': human,
            'agentHints': agent['hints'],
            'measured': {'agentEqualsJson': from_agent == parity,
                         'humanEqualsJson': all(from_human[k] == (json.dumps(v) if isinstance(v, bool)
                                                                  else str(v))
                                                for k, v in parity.items())}}


def main():
    g = Graph('typescript')
    ops, fails = cases(g)
    edges, omissions = g.project('imports', 'resolved-target', sorted(g.views))
    doc = {'requirement': 'R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR',
           'consumerId': 'consumer-b.v23', 'standing': __doc__,
           'owner': {'schema': S.doc_path(Q_DOC), 'schemaSha256': S.load_doc(Q_DOC)['sha256'],
                     'contract': CONTRACT_DOC, 'bounds': BOUNDS},
           'predecessor': 'predecessors.v22/query/graph-query-reconstruction.json',
           'admittedRunUnderQuery': {'label': g.label, 'runId': g.runId,
                                     'snapshotId': g.snapshotId, 'projectId': g.projectId,
                                     'closeRunAdmitted': g.closeRunAdmitted},
           'projectionTable': g.registry_join(),
           'vertexDomain': {
               'inventoryVertices': [list(v) for v in sorted(g.vertices)],
               'unboundInventories': g.unbound_inventories,
               'importsProjection': [{'factId': e['factId'], 'source': e['source'],
                                      'target': e['target'], 'targetOccupancy': e['targetOccupancy']}
                                     for e in edges],
               'importsOmissions': [{'kind': k, 'factId': f} for k, f in omissions]},
           'declaredInterpretations': DECLARED_INTERPRETATIONS,
           'operations': ops, 'failureCases': fails,
           'renderings': renderings(ops[0]),
           'whatAQueryNeverDoes': ['materialise a fact', 'invoke a provider',
                                   'allocate an attempt', 'seal a Run', 'derive policy',
                                   'choose a termination', 'run a parallel absence evaluator'],
           'evidenceLimitationsVersusStoredEdgeCompletion': {
               'storedEdgeCompletion': 'traversalCoverage, visitedNodes and countBasis describe '
                                       'THIS operation',
               'evidenceLimitations': 'the Q3 disclosure cites the sealed Run\'s Coverage, '
                                      'deficiencies and limitations; it is never recomputed',
               'whyTheyAreSeparateFields': 'a traversal can be complete over incomplete evidence; '
                                           'the schema says "traversalCoverage is not native '
                                           'CoverageResult"'},
           'layersMeasured': {
               'schema': 'every request and response re-admitted against graph-query:3 and every '
                         'failure envelope against command-envelope:3',
               'behaviour': 'each outcome is the executor\'s result for the retained request and '
                            'host observations; lib/indep_query_surface.py recomputes it',
               'notMeasured': 'no product query engine, backend index or host was executed'}}
    EV.write('query/graph-query-reconstruction.json', doc)
    bad = []
    for c in ops:
        adm = all(a['admitted'] for a in c.get('admission', []))
        o = c['outcome']
        ctx = (o.get('response') or {}).get('context') or {}
        print('%-52s %-9s adm=%-5s items=%s total=%s %s visited=%s %s' % (
            c['case'][:52], o['kind'], adm, len(o['response']['items']) if o['kind'] == 'response'
            else '-', ctx.get('totalItems'), ctx.get('traversalCoverage'), ctx.get('visitedNodes'),
            (o.get('response') or {}).get('termination', {}).get('class')))
        if o['kind'] != 'response' or not adm:
            bad.append((c['case'], o.get('refusal'), c.get('admission')))
    print()
    for f in fails:
        o = f['outcome']
        print('%-44s %-28s %s' % (f['case'][:44], o['kind'],
                                   (o.get('refusal') or {}).get('domainDetail')))
        if o['kind'] == 'failure' and not o['envelopeAdmission']['admitted']:
            bad.append((f['case'], o['envelopeAdmission'].get('owningSchemaError')))
        if o['kind'] == 'response':
            bad.append((f['case'], 'AN INVALID REQUEST PRODUCED A RESPONSE'))
    print('renderings', doc['renderings']['measured'])
    if bad:
        print(json.dumps(bad, indent=1, default=str)[:3000])
    assert not bad, [b[0] for b in bad]


main()
